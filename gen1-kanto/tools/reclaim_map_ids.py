#!/usr/bin/env python3
"""Retire unused map IDs so they can be respent on outdoor maps.

The 22 UNUSED_MAP_* slots that ship in the ROM cannot host an outdoor map where
they sit: all but $0B are above FIRST_INDOOR_MAP, and MapSpriteSets and
ExternalMapEntries are only FIRST_INDOOR_MAP long and are indexed by raw map ID
with no bounds check. An outdoor map at $69 reads off the end of a 37-byte table.

So an unused slot is spent by *deleting* it, which drops NUM_MAPS by one and
shifts every later indoor map down. That is free, because indoor maps are only
referenced symbolically and the indoor group constants are computed from
const_value. The freed headroom under LAST_MAP is then available to a new
outdoor constant inserted before FIRST_INDOOR_MAP.

Rows are removed by *index*, not by matching a comment: only some of these
tables tag their filler rows with the slot name, and grass_water.asm does not
tag them at all. Each table is located by its table_width header and its
closing assert_table_length, and its row count is checked against NUM_MAPS
before anything is removed. Tables that are FIRST_INDOOR_MAP long need no
change, since every slot handled here sits above that boundary.

    python3 tools/reclaim_map_ids.py --list
    python3 tools/reclaim_map_ids.py UNUSED_MAP_69 UNUSED_MAP_6A
    python3 tools/reclaim_map_ids.py --all

All edits are computed in memory and only written once every table validates,
so a failure leaves the tree untouched. Rebuild afterwards: assert_table_length
is the backstop.
"""
import argparse, os, re, sys

ROOT = os.environ.get('POKEYELLOW', os.path.join(os.path.dirname(__file__), '..'))
CONSTS = 'constants/map_constants.asm'
TABLES = [
    'data/maps/map_header_pointers.asm',
    'data/maps/map_header_banks.asm',
    'data/maps/songs.asm',
    'data/wild/grass_water.asm',
]

# Slots that are not really unused. Retiring these means dealing with their
# references first, which is a separate and riskier job than bookkeeping.
KEEP = {
    'UNUSED_MAP_0B': 'boundary between NUM_CITY_MAPS and FIRST_ROUTE_MAP, and below '
                     'FIRST_INDOOR_MAP so the outdoor tables would shift too',
    'UNUSED_MAP_6F': 'carries hidden_events and a hidden_item in data/events/',
    'UNUSED_MAP_ED': 'live warp target from data/maps/objects/SilphCoElevator.asm',
    'UNUSED_MAP_F4': 'has toggle_consts_for and toggleable_objects entries',
}

def read(rel):
    return open(f'{ROOT}/{rel}').read()

def map_consts(txt):
    return re.findall(r'^\tmap_const (\w+),', txt, re.M)

def row_line_numbers(lines, rel):
    """Indices of the data rows between `table_width` and `assert_table_length`."""
    try:
        start = next(i for i, l in enumerate(lines) if l.startswith('\ttable_width'))
        end = next(i for i, l in enumerate(lines) if 'assert_table_length NUM_MAPS' in l)
    except StopIteration:
        raise SystemExit(f'{rel}: could not locate table bounds')
    return [i for i in range(start + 1, end) if re.match(r'\t(db|dw) ', lines[i])]

def renumber(txt):
    """Rewrite the trailing ; $XX comment on every map_const to match its position."""
    out, i = [], 0
    for line in txt.splitlines(True):
        m = re.match(r'(\tmap_const \w+,\s*\d+,\s*\d+)(\s*;\s*\$[0-9A-Fa-f]+)?(.*)$',
                     line.rstrip('\n'))
        if m:
            out.append(f'{m.group(1)} ; ${i:02X}{m.group(3)}\n'); i += 1
        else:
            out.append(line)
    return ''.join(out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('slots', nargs='*')
    ap.add_argument('--all', action='store_true', help='retire every safe slot')
    ap.add_argument('--list', action='store_true')
    a = ap.parse_args()

    ctxt = read(CONSTS)
    consts = map_consts(ctxt)
    unused = [c for c in consts if c.startswith('UNUSED_MAP_')]

    if a.list:
        for s in unused:
            print(f'  {s:16s} ' + (f'KEEP — {KEEP[s]}' if s in KEEP else 'retirable'))
        keep = sum(1 for s in unused if s in KEEP)
        print(f'\nNUM_MAPS {len(consts)} of 255; {len(unused)} unused slots, '
              f'{len(unused)-keep} retirable -> {255-len(consts)+len(unused)-keep} free IDs')
        return 0

    targets = [s for s in unused if s not in KEEP] if a.all else a.slots
    if not targets:
        raise SystemExit('nothing to do; pass slot names or --all')
    for s in targets:
        if s in KEEP:
            raise SystemExit(f'{s} is not safe to retire: {KEEP[s]}')
        if s not in unused:
            raise SystemExit(f'{s} is not an unused slot')
    idx = sorted((consts.index(s) for s in targets), reverse=True)

    pending = {}
    for rel in TABLES:
        lines = read(rel).splitlines(True)
        rows = row_line_numbers(lines, rel)
        if len(rows) != len(consts):
            raise SystemExit(f'{rel}: {len(rows)} rows but NUM_MAPS is {len(consts)}')
        for i in idx:
            lines[rows[i]] = None
        pending[rel] = ''.join(l for l in lines if l is not None)

    clines = ctxt.splitlines(True)
    cpos = [i for i, l in enumerate(clines) if re.match(r'\tmap_const ', l)]
    for i in idx:
        clines[cpos[i]] = None
    pending[CONSTS] = renumber(''.join(l for l in clines if l is not None))

    for rel, text in pending.items():
        open(f'{ROOT}/{rel}', 'w').write(text)
    n = len(consts) - len(targets)
    print(f'retired {len(targets)} slot(s): {", ".join(sorted(targets))}')
    print(f'NUM_MAPS {len(consts)} -> {n}; {255-n} free IDs under LAST_MAP')
    print('rebuild to confirm; assert_table_length is the backstop')
    return 0

if __name__ == '__main__':
    sys.exit(main())

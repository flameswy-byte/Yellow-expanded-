#!/usr/bin/env python3
"""Give the new maps wild encounters, derived from their neighbours.

Tall grass with nothing in it is scenery, not a route. But inventing species
lists per map is exactly the sort of guess this project has avoided everywhere
else, so the tables come from the same place the terrain did: the maps next
door. For each new map, every neighbour's table is pooled, each entry weighted
by how much edge the two maps share and by how likely that slot is to come up.
Species are then ranked by total weight and dealt into the slots highest
first, so a route between Petalburg and Rustboro ends up with the Pokémon you
would expect to meet between them, at the levels you would expect.

Levels are a weighted mean of the donors', so a map bridging a level 5 route
and a level 15 one lands in between rather than at one end.

Water and fishing tables are only written where the map actually has water,
and land tables only where it has grass to stand in.

    python3 tools/encounters.py --dry-run
    python3 tools/encounters.py
"""
import argparse, collections, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_hoenn as R
import terrain as T
import newmaps as N

WILD = f'{R.ROOT}/src/data/wild_encounters.json'
GROUP = 'gWildMonHeaders'

# Gen 3 slot probabilities, in percent. The land table is the familiar
# 20/20/10/10/10/10/5/5/5/4/4/1; fishing is three rods sharing ten slots.
RATES = {
    'land_mons':        [20, 20, 10, 10, 10, 10, 5, 5, 4, 4, 1, 1],
    'water_mons':       [60, 30, 5, 4, 1],
    'rock_smash_mons':  [60, 30, 5, 4, 1],
    'fishing_mons':     [70, 30, 60, 20, 20, 40, 40, 15, 4, 1],
}

# --- the fourteenth and fifteenth slots -----------------------------------
# A land table has twelve slots and the rarest of them is 1%, because the
# chooser rolls Random() % 100. Half a percent is not a thing the game can
# express, so the whole table is doubled - every vanilla slot keeps exactly its
# vanilla share of 200 - and two more slots worth one unit each are put on the
# end. 202 units: the vanilla twelve are diluted from 20.00% to 19.80% and so
# on down, which is a relative change of one part in a hundred, and the two new
# ones are worth 1/202 = 0.495% apiece.
#
# Adding to the end rather than taking slots 10 and 11 is what keeps vanilla's
# rares. Those two slots are the only place Kecleon appears in grass, on six
# maps; measured across all 120 land tables, 23 of the 240 slot-10/11 entries
# hold a species found nowhere else on that map.
LAND_RATES = [40, 40, 20, 20, 20, 20, 10, 10, 8, 8, 2, 2, 1, 1]
LAND_TOTAL = sum(LAND_RATES)
RARE_SLOTS = (12, 13)            # the two new ones
FIVE_PCT = (6, 7)                # 10/202 = 4.95%, the nearest thing to 5%

# Where each thing is meant to turn up. Sets are computed, never listed by
# hand, except Shoal Cave and Victory Road which are named places.
GENERIC = {              # slots 12 and 13, by what kind of map it is
    'outdoor': ('SPECIES_SLIME', 'SPECIES_METAL_SLIME'),
    'cave':    ('SPECIES_KING_SLIME', 'SPECIES_KING_SLIME'),
}
OUTDOOR_TYPES = ('MAP_TYPE_ROUTE', 'MAP_TYPE_OCEAN_ROUTE', 'MAP_TYPE_TOWN',
                 'MAP_TYPE_CITY', 'MAP_TYPE_INDOOR')
CAVE_TYPES = ('MAP_TYPE_UNDERGROUND',)

def load():
    """the vanilla tables, and only the vanilla ones.

    Our own tables are in the same file once this has run once, and pass one
    reads them as if they were donors - so running it twice gave a different
    answer, and a third run a different one again. Same rule as the terrain
    model: never learn from your own output. Pass two still feeds this run's
    results to the maps that had no vanilla neighbour, which is deliberate and
    happens within the run.
    """
    d = json.load(open(WILD))
    grp = next(g for g in d['wild_encounter_groups'] if g['label'] == GROUP)
    skip = T.generated()
    return d, grp, {e['map']: e for e in grp['encounters'] if e['map'] not in skip}

def spans(box, const):
    """neighbour -> number of shared edge cells, from the map's own header."""
    p = f'{R.ROOT}/data/maps/{N.map_dir(const)}/map.json'
    j = json.load(open(p))
    w, h = box[const][2], box[const][3]
    out = collections.Counter()
    for c in j.get('connections') or []:
        nb, d, off = c.get('map'), c.get('direction'), c.get('offset', 0)
        if nb not in box or d not in ('up', 'down', 'left', 'right'):
            continue
        nw, nh = box[nb][2], box[nb][3]
        if d in ('up', 'down'):
            n = min(w, off + nw) - max(0, off)
        else:
            n = min(h, off + nh) - max(0, off)
        if n > 0:
            out[nb] += n
    return out

def terrain_mix(spec):
    """which encounter kinds this map can support at all."""
    L = f'{R.ROOT}/data/layouts/{spec["name"]}/map.bin'
    blk = open(L, 'rb').read()
    rend = R.Renderer()
    C = T.Classifier(rend, 'gTileset_General', spec.get('secondary'))
    n = collections.Counter()
    for i in range(len(blk) // 2):
        v = blk[i*2] | (blk[i*2+1] << 8)
        n[C(v & 0x3FF, (v >> 10) & 3)] += 1
    return n

def pool(kind, tables, weights):
    """species -> (weight, mean min level, mean max level) across neighbours."""
    acc = {}
    rate = RATES[kind]
    for nb, wt in weights.items():
        t = tables.get(nb, {}).get(kind)
        if not t:
            continue
        for i, m in enumerate(t['mons']):
            r = rate[i] if i < len(rate) else 1
            w = wt * r
            a = acc.setdefault(m['species'], [0.0, 0.0, 0.0])
            a[0] += w
            a[1] += w * m['min_level']
            a[2] += w * m['max_level']
    return {s: (w, lo / w, hi / w) for s, (w, lo, hi) in acc.items() if w > 0}

def build_table(kind, tables, weights):
    p = pool(kind, tables, weights)
    if not p:
        return None
    order = sorted(p, key=lambda s: -p[s][0])
    slots = len(RATES[kind])
    mons = []
    for i in range(slots):
        s = order[i % len(order)]
        _, lo, hi = p[s]
        lo, hi = max(2, round(lo)), max(2, round(hi))
        mons.append({'min_level': min(lo, hi), 'max_level': max(lo, hi),
                     'species': s})
    rates = [tables[nb][kind]['encounter_rate'] for nb in weights
             if tables.get(nb, {}).get(kind)]
    return {'encounter_rate': round(sum(rates) / len(rates)), 'mons': mons}


# The six species tools/newmons.py adds are native to nowhere in Hoenn, so
# unlike everything else in this file they are placed by hand rather than
# derived from the neighbours. Each line overwrites one slot of one table on
# one map, so the rest of that map's list is untouched, and re-running is
# idempotent because the slot is addressed by index rather than by what is in
# it.
#
# Only the first stage of each line is placed. Volcarona, Golisopod and Alolan
# Ninetales are evolution-only, which is what makes them worth having.
#
#   (map, table, slot, species, min level, max level)
PLANT = [
    # Larvesta on the one new route with a volcanic character - it is the map
    # that inherited Slugma from its neighbours. Slots 10 and 11 are 4% and 1%.
    ('MAP_ROUTE144', 'land_mons', 10, 'SPECIES_LARVESTA', 15, 16),
    ('MAP_ROUTE144', 'land_mons', 11, 'SPECIES_LARVESTA', 15, 16),

    # Wimpod's shore and Alolan Vulpix's ice room used to be planted here, one
    # map each. rares() now measures the sets they belong to and gives them a
    # 5% slot on every map in them, which covers those two maps and eight more,
    # so keeping these as well would stack a second helping on top.

    # The three slimes are visitors rather than natives, so each takes only the
    # single 1% slot rather than the 4%-and-1% pair the others get. Slot 11 is
    # the rarest thing the land table can express.
    #
    # They are spread across three different maps on purpose: finding one
    # should feel like finding one, not like finding the slime route.
    ('MAP_ROUTE141', 'land_mons', 11, 'SPECIES_SLIME', 6, 8),
    ('MAP_ROUTE146', 'land_mons', 11, 'SPECIES_KING_SLIME', 26, 28),
    # The metal slime is the rarest and the least willing: catch rate 3, Run
    # Away, and 255 experience if you somehow manage it. Route 148 is the
    # furthest corner of the new region.
    ('MAP_ROUTE148', 'land_mons', 11, 'SPECIES_METAL_SLIME', 22, 26),
]


def plant(groups):
    """Put the hand-placed species into their slots, on our maps and vanilla's
    alike. Runs after the derived tables, so it always wins."""
    by_map = {e['map']: e for e in groups}
    done = 0
    for const, kind, slot, species, lo, hi in PLANT:
        e = by_map.get(const)
        if e is None or kind not in e:
            sys.exit(f'{const} has no {kind} table to plant {species} in')
        mons = e[kind]['mons']
        if slot >= len(mons):
            sys.exit(f'{const} {kind} has {len(mons)} slots, no slot {slot}')
        mons[slot] = {'min_level': lo, 'max_level': hi, 'species': species}
        done += 1
    return done


# --- who lives where, measured ---------------------------------------------
def map_facts():
    """(map type, deep-sand share, beach-sand share, ocean share) per map."""
    import struct
    beh = {}
    inside, i = False, 0
    for line in open(f'{R.ROOT}/include/constants/metatile_behaviors.h'):
        s = line.strip()
        if s.startswith('enum'):
            inside = True
        elif inside and s.startswith('};'):
            break
        elif inside and s.startswith('MB_'):
            beh[s.split(',')[0].split()[0]] = i
            i += 1

    types = {}
    for d in sorted(os.listdir(f'{R.ROOT}/data/maps')):
        p = f'{R.ROOT}/data/maps/{d}/map.json'
        if os.path.exists(p):
            m = json.load(open(p))
            types[m['id']] = m.get('map_type')

    lay, maps, _ = R.solve()
    cache, out = {}, {}
    for const, m in maps.items():
        L = lay[m['layout']]
        p = f'{R.ROOT}/{L["blockdata_filepath"]}'
        if not os.path.exists(p):
            continue
        key = (L['primary_tileset'], L.get('secondary_tileset'))
        if key not in cache:
            # secret base tilesets have no directory of their own; a map we
            # cannot read the behaviours of simply joins no measured set
            def read(name):
                try:
                    return T.behaviors(name) if name else []
                except SystemExit:
                    return []
            cache[key] = (read(key[0]), read(key[1]))
        prim, sec = cache[key]
        w, h = L['width'], L['height']
        raw = struct.unpack(f'<{w*h}H', open(p, 'rb').read()[:w*h*2])
        c = collections.Counter()
        for v in raw:
            mid = v & 0x3FF
            if mid < 512:
                c[prim[mid] if mid < len(prim) else 0] += 1
            else:
                j = mid - 512
                c[sec[j] if j < len(sec) else 0] += 1
        n = len(raw)
        out[const] = (types.get(const),
                      100 * c[beh['MB_DEEP_SAND']] / n,
                      100 * c[beh['MB_SAND']] / n,
                      100 * (c[beh['MB_OCEAN_WATER']] + c[beh['MB_DEEP_WATER']]) / n)
    return out


def rares(groups, facts):
    """Put the new species into every table that should hold one.

    Every land table is first padded to fourteen slots by repeating slot 11,
    so a map nobody has anything to say about keeps the distribution it had.
    Then the generic pair goes in the two new slots, and the named sets take a
    5% slot each. Levels are the map's own band - a slime on Route 101 is a
    Route 101 slime - because inventing a level per map is the guess this
    project has avoided everywhere else.
    """
    # One map can own several tables - Altering Cave has nine under the one
    # id - so this walks the entries, never a dict keyed by map. Keying by map
    # silently padded one of Altering Cave's nine and left eight at twelve
    # slots, which the chooser would have read straight off the end of.
    entries = [e for e in groups if 'map' in e]
    have = {e['map'] for e in entries if 'land_mons' in e}
    # coastal: a beach you can stand on with ocean beside it
    coastal = {k for k, (t, ds, sand, sea) in facts.items()
               if sand >= 1 and sea >= 1 and k in have}
    desert = {k for k, (t, ds, sand, sea) in facts.items() if ds > 0 and k in have}
    shoal = {k for k in have if k.startswith('MAP_SHOAL_CAVE')}
    victory = {k for k in have if k.startswith('MAP_VICTORY_ROAD')}

    def band(e):
        mons = e['land_mons']['mons']
        return min(m['min_level'] for m in mons), max(m['max_level'] for m in mons)

    def put(e, slot, species, lo, hi):
        e['land_mons']['mons'][slot] = {'min_level': lo, 'max_level': hi,
                                        'species': species}

    tally = collections.Counter()
    for e in sorted(entries, key=lambda e: e['map']):
        const = e['map']
        if 'land_mons' not in e:
            continue
        mons = e['land_mons']['mons']
        while len(mons) < len(LAND_RATES):
            mons.append(dict(mons[11]))
        lo, hi = band(e)
        t = facts.get(const, (None,))[0]
        kind = 'cave' if t in CAVE_TYPES else 'outdoor' if t in OUTDOOR_TYPES else None

        if const in victory:
            # 5% and 2%, as near as 202 units can say it: one 10-unit slot is
            # 4.95%, and 2+1+1 units is 1.98%. Slot 11 is left alone.
            put(e, FIVE_PCT[0], 'SPECIES_KING_SLIME', lo, hi)
            for s in (10,) + RARE_SLOTS:
                put(e, s, 'SPECIES_METAL_SLIME', lo, hi)
            tally['victory road'] += 1
            continue

        if kind:
            for s, sp in zip(RARE_SLOTS, GENERIC[kind]):
                put(e, s, sp, lo, hi)
            tally[f'{kind} pair'] += 1

        # the 5% sets. Route 148 is both dune and shore, so the second one
        # takes the other 5% slot rather than overwriting the first.
        wants = ([('SPECIES_LARVESTA', 'desert')] if const in desert else []) \
              + ([('SPECIES_WIMPOD', 'coastal')] if const in coastal else []) \
              + ([('SPECIES_VULPIX_A', 'shoal')] if const in shoal else [])
        for i, (sp, why) in enumerate(wants[:len(FIVE_PCT)]):
            put(e, FIVE_PCT[i], sp, lo, hi)
            tally[why] += 1

    # underwater: only two of the fourteen underwater maps have a wild table at
    # all, and giving the other twelve one would put encounters where the game
    # has none. Water slot 2 is 5% on the nose.
    for e in sorted(entries, key=lambda e: e['map']):
        const = e['map']
        if const.startswith('MAP_UNDERWATER') and 'water_mons' in e:
            mons = e['water_mons']['mons']
            lo = min(m['min_level'] for m in mons)
            hi = max(m['max_level'] for m in mons)
            mons[2] = {'min_level': lo, 'max_level': hi,
                       'species': 'SPECIES_KING_SLIME'}
            tally['underwater'] += 1
    return tally


def pad_other_groups(d):
    """Battle Pyramid and Pike share ChooseWildMonIndex_Land and would read off
    the end of their own twelve-slot tables. Padded with slots 10 and 11, so
    those two species gain half a percent each and nothing else moves."""
    n = 0
    for g in d['wild_encounter_groups']:
        if g['label'] == GROUP:
            continue
        for e in g.get('encounters', []):
            mons = e.get('land_mons', {}).get('mons')
            if mons is None:
                continue
            while len(mons) < len(LAND_RATES):
                mons.append(dict(mons[10 + (len(mons) - 12)]))
                n += 1
    return n


def patch_chooser(dry):
    """The land chooser is twelve hardcoded branches. Make it count instead."""
    p = f'{R.ROOT}/src/wild_encounter.c'
    src = open(p).read()
    i = src.index('static u8 ChooseWildMonIndex_Land(void)')
    j = src.index('\n}\n', i) + 3
    if 'sLandEncounterChances' in src:
        return False
    slots = ',\n    '.join(
        f'ENCOUNTER_CHANCE_LAND_MONS_SLOT_{k}' for k in range(len(LAND_RATES)))
    new = (
        '// The cumulative chances, so the count follows the table in\n'
        '// wild_encounters.json rather than a chain of branches that has to be\n'
        '// edited to match it.\n'
        'static const u16 sLandEncounterChances[NUM_LAND_MONS_ENCOUNTER_SLOTS] =\n'
        '{\n    ' + slots + ',\n};\n\n'
        'static u8 ChooseWildMonIndex_Land(void)\n'
        '{\n'
        '    u16 rand = Random() % ENCOUNTER_CHANCE_LAND_MONS_TOTAL;\n'
        '    u8 i;\n\n'
        '    for (i = 0; i < NUM_LAND_MONS_ENCOUNTER_SLOTS - 1; i++)\n'
        '    {\n'
        '        if (rand < sLandEncounterChances[i])\n'
        '            return i;\n'
        '    }\n'
        '    return i;\n'
        '}\n')
    if not dry:
        open(p, 'w').write(src[:i] + new + src[j:])
    return True


def check():
    """Read back what shipped, and roll every possible die.

    The land chooser is the one place where a table of the wrong length is a
    read off the end of an array rather than an error, so this counts the slots
    in every table in every group, and then walks all 202 outcomes to prove
    each one lands in exactly one slot at the share it is supposed to.
    """
    import re
    bad = []
    d = json.load(open(WILD))
    h = open(f'{R.ROOT}/include/constants/wild_encounter.h').read()
    cum, chances = 0, []
    for i in range(len(LAND_RATES)):
        m = re.search(rf'SLOT_{i} \((?:ENCOUNTER_CHANCE_LAND_MONS_SLOT_\d+ \+ )?(\d+)\)', h)
        if not m:
            bad.append(f'the generated header has no land slot {i}')
            return bad
        cum += int(m.group(1))
        chances.append(cum)
    if cum != LAND_TOTAL:
        bad.append(f'header totals {cum} units, the table says {LAND_TOTAL}')
    n = re.search(r'NUM_LAND_MONS_ENCOUNTER_SLOTS \((\d+)\)', h)
    if not n or int(n.group(1)) != len(LAND_RATES):
        bad.append(f'NUM_LAND_MONS_ENCOUNTER_SLOTS is {n and n.group(1)}, '
                   f'want {len(LAND_RATES)}')

    want = {'land_mons': len(LAND_RATES), 'water_mons': 5,
            'rock_smash_mons': 5, 'fishing_mons': 10}
    for g in d['wild_encounter_groups']:
        for e in g.get('encounters', []):
            for k, size in want.items():
                if k in e and len(e[k]['mons']) != size:
                    bad.append(f'{g["label"]} {e.get("map")} {k} has '
                               f'{len(e[k]["mons"])} slots, chooser expects {size}')

    hits = collections.Counter()
    for roll in range(cum):
        for i in range(len(chances) - 1):
            if roll < chances[i]:
                hits[i] += 1
                break
        else:
            hits[len(chances) - 1] += 1
    if sum(hits.values()) != cum:
        bad.append('some rolls land in no slot at all')
    for i, r in enumerate(LAND_RATES):
        if hits[i] != r:
            bad.append(f'slot {i} takes {hits[i]} of {cum} rolls, table says {r}')
    if not bad:
        print(f'{len(LAND_RATES)} land slots over {cum} units; all {cum} rolls '
              'land in exactly one, at the share the table asks for')
        print('   ' + '  '.join(f'{i}:{100*r/cum:.2f}%'
                                for i, r in enumerate(LAND_RATES)))
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()
    if a.check:
        bad = check()
        if bad:
            sys.exit('\n'.join(bad))
        return
    d, grp, tables = load()
    box = N.origins()

    # Two passes. Pass one uses only vanilla neighbours, so each map's levels
    # come from the real routes around it. Pass two runs solely for the maps
    # that got nothing - the ones whose only land-bearing neighbours are also
    # new - and only those see the first pass's results. Feeding new tables
    # back in everywhere would pull every map toward the global mean and cost
    # the level gradient the first pass just got right.
    done = {}
    for rnd in (1, 2):
        if rnd == 2:
            tables.update({k: v for k, v in done.items()})
        for spec in N.NEWMAPS:
            const, name = spec['const'], spec['name']
            if (const in done) == (rnd == 1) and rnd == 2:
                continue
            if rnd == 1 and const in done:
                continue
            if rnd == 2 and 'land_mons' in done.get(const, {}):
                continue
            wt = spans(box, const)
            mix = terrain_mix(spec)
            total = sum(mix.values())
            entry = {'map': const, 'base_label': f'g{name}'}
            got = []
            # a land table needs somewhere to stand; water and fishing need water
            if mix[T.TALL] + mix[T.GRASS] > total * 0.02:
                t = build_table('land_mons', tables, wt)
                if t:
                    entry['land_mons'] = t
                    got.append(f'land x{len(t["mons"])} rate {t["encounter_rate"]}')
            if mix[T.WATER] > total * 0.02:
                for kind, tag in (('water_mons', 'water'), ('fishing_mons', 'fish')):
                    t = build_table(kind, tables, wt)
                    if t:
                        entry[kind] = t
                        got.append(tag)
            if len(entry) == 2:
                continue
            if const in done and 'land_mons' not in entry:
                continue                      # pass two added nothing new
            done[const] = entry      # only pass two reads these back
            lv = entry.get('land_mons') or entry.get('water_mons')
            rng = (min(m['min_level'] for m in lv['mons']),
                   max(m['max_level'] for m in lv['mons']))
            top = ', '.join(dict.fromkeys(m['species'][8:].title()
                                          for m in lv['mons']))[:64]
            print(f'  {name:9s} lv {rng[0]:2d}-{rng[1]:2d}  {", ".join(got):28s} {top}')
    for const, entry in done.items():
        grp['encounters'] = [e for e in grp['encounters'] if e['map'] != const]
        grp['encounters'].append(entry)

    n = plant(grp['encounters'])
    print(f'{n} hand-placed slots for the species newmons.py added')

    # Shoal Cave's two high-tide rooms have no wild table at all in vanilla.
    # "every room and condition" cannot be honoured without inventing one, so
    # each copies the low-tide room it is the flooded version of.
    for hi_, lo_ in (('MAP_SHOAL_CAVE_HIGH_TIDE_ENTRANCE_ROOM',
                      'MAP_SHOAL_CAVE_LOW_TIDE_ENTRANCE_ROOM'),
                     ('MAP_SHOAL_CAVE_HIGH_TIDE_INNER_ROOM',
                      'MAP_SHOAL_CAVE_LOW_TIDE_INNER_ROOM')):
        if any(e.get('map') == hi_ for e in grp['encounters']):
            continue
        src = next(e for e in grp['encounters'] if e['map'] == lo_)
        grp['encounters'].append({
            'map': hi_,
            'base_label': 'g' + ''.join(w.capitalize()
                                        for w in hi_[4:].lower().split('_')),
            'land_mons': json.loads(json.dumps(src['land_mons']))})
        print(f'  + {hi_[4:]} takes {lo_[4:]}\'s table; vanilla gives it none')

    # the rate table lives in the data, and the generated header follows it
    for f in grp['fields']:
        if f['type'] == 'land_mons':
            f['encounter_rates'] = list(LAND_RATES)
    facts = map_facts()
    tally = rares(grp['encounters'], facts)
    padded = pad_other_groups(d)
    print(f'land tables now {len(LAND_RATES)} slots over {LAND_TOTAL} units; '
          f'{padded} slots padded on the Pyramid and Pike tables')
    for what, n in sorted(tally.items()):
        print(f'  {what:14s} {n} maps')
    if patch_chooser(a.dry_run):
        print('  ChooseWildMonIndex_Land now counts the table')

    # the table is indexed by map order in some tools; keep it deterministic
    grp['encounters'].sort(key=lambda e: e['map'])
    print(f'{len(grp["encounters"])} encounter entries total')
    if not a.dry_run:
        json.dump(d, open(WILD, 'w'), indent=2)

if __name__ == '__main__':
    sys.exit(main())

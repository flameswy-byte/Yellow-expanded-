#!/usr/bin/env python3
"""Put items on the new routes.

A route with nothing on it is scenery. Vanilla's land routes carry a median of
two item balls and one hidden item each - 0.67 and 0.42 per thousand cells -
and ours carried none, so fourteen maps of terrain had nothing in them to find.

Where they go is measured, not guessed. Vanilla's 77 route item balls stand on
grass 43 times, shallow water 15, sand and path 7 each, a plateau 5; 30% of
their four neighbours are trees or cliff, which is to say they are tucked into
a nook rather than dropped in the open. Its 55 hidden items are on grass and
sand, and sometimes on a rock. What they contain is drawn from the same pool
vanilla uses on its own routes.

Run after newmaps.py, which rewrites the map headers from scratch:

    python3 tools/newmaps.py && python3 tools/populate.py
"""
import argparse, collections, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_hoenn as R
import terrain as T
import newmaps as N

# vanilla medians, per thousand cells of map
ITEM_RATE = 0.67
HIDDEN_RATE = 0.42
APART = 10                      # no two finds closer than this
MARGIN = 3                      # never on the rim, where a connection lands

# where vanilla stands an item ball, and where it buries one
BALL_ON = (T.GRASS, T.SAND, T.PATH, T.PLATEAU, T.SHALLOW)
HIDDEN_ON = (T.GRASS, T.SAND, T.PATH, T.TALL, T.PLATEAU)

# vanilla's own route item pool, in its own proportions. Our routes sit at
# levels 20-28, so the pool is the late half of it: no Potions and Poke Balls
# on a route you reach with a full team.
BALL_ITEMS = ['ITEM_RARE_CANDY', 'ITEM_PP_UP', 'ITEM_ELIXIR', 'ITEM_HYPER_POTION',
              'ITEM_PROTEIN', 'ITEM_STAR_PIECE', 'ITEM_NUGGET', 'ITEM_REVIVE',
              'ITEM_ZINC', 'ITEM_CARBOS', 'ITEM_IRON', 'ITEM_HP_UP',
              'ITEM_SUPER_REPEL', 'ITEM_GREAT_BALL', 'ITEM_BIG_PEARL',
              'ITEM_CALCIUM', 'ITEM_MAX_ETHER', 'ITEM_FULL_HEAL',
              'ITEM_X_ACCURACY', 'ITEM_DIRE_HIT', 'ITEM_ULTRA_BALL',
              'ITEM_MAX_REVIVE', 'ITEM_ETHER', 'ITEM_ENERGY_ROOT']
HIDDEN_ITEMS = ['ITEM_HEART_SCALE', 'ITEM_RARE_CANDY', 'ITEM_REVIVE',
                'ITEM_FULL_HEAL', 'ITEM_STARDUST', 'ITEM_GREAT_BALL',
                'ITEM_ETHER', 'ITEM_NUGGET', 'ITEM_BIG_PEARL',
                'ITEM_SUPER_POTION', 'ITEM_CARBOS', 'ITEM_IRON',
                'ITEM_CALCIUM', 'ITEM_ULTRA_BALL']

MARK = '// Open Hoenn - tools/populate.py'
FLAGS = 'include/constants/flags.h'
BALLS = 'data/scripts/item_ball_scripts.inc'

def camel(item):
    return ''.join(p.capitalize() for p in item[5:].split('_'))

def load(const, lay, maps):
    L = lay[maps[const]['layout']]
    w, h = L['width'], L['height']
    blk = open(f'{R.ROOT}/{L["blockdata_filepath"]}', 'rb').read()
    raw = [(blk[i*2] | (blk[i*2+1] << 8)) for i in range(w * h)]
    return L, w, h, raw

def reachable(w, h, raw, cls):
    """cells the player can actually stand on, walking in from an edge."""
    walk = [((v >> 10) & 3) == 0 and cls[i] not in (T.WATER, T.POND)
            for i, v in enumerate(raw)]
    ele = [(v >> 12) & 0xF for v in raw]
    ok = lambda a, b: a == b or 0 in (a, b) or 15 in (a, b)
    seed = [i for i in range(w*h)
            if walk[i] and (i % w in (0, w-1) or i // w in (0, h-1))]
    seen, q = set(seed), collections.deque(seed)
    while q:
        i = q.popleft()
        x, y = i % w, i // w
        for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
            j = ny*w + nx
            if (0 <= nx < w and 0 <= ny < h and j not in seen and walk[j]
                    and ok(ele[i], ele[j])):
                seen.add(j)
                q.append(j)
    return seen, walk

def spots(spec, lay, maps, rend, beh):
    """(ball positions, hidden positions) for one map, both deterministic."""
    const = spec['const']
    L, w, h, raw = load(const, lay, maps)
    C = T.Classifier(rend, L['primary_tileset'], L.get('secondary_tileset'))
    cls = [C(v & 0x3FF, (v >> 10) & 3) for v in raw]
    live, walk = reachable(w, h, raw, cls)
    jump = set(range(0x38, 0x40))

    def usable(i, want):
        x, y = i % w, i // w
        if not (MARGIN <= x < w - MARGIN and MARGIN <= y < h - MARGIN):
            return False
        if i not in live or cls[i] not in want:
            return False
        m = raw[i] & 0x3FF
        return not (m < len(beh) and beh[m] in jump)

    def tucked(i):
        x, y = i % w, i // w
        return sum(1 for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1))
                   if 0 <= nx < w and 0 <= ny < h and not walk[ny*w + nx])

    def pick(want, n, salt, need_nook):
        cand = [i for i in range(w*h) if usable(i, want)
                and (tucked(i) if need_nook else True)]
        cand.sort(key=lambda i: -T.fbm(i % w, i // w, spec['num']*7 + salt,
                                       octaves=2, freq=0.07))
        out = []
        for i in cand:
            if len(out) >= n:
                break
            x, y = i % w, i // w
            if any(abs(x - px) + abs(y - py) < APART for px, py in out):
                continue
            out.append((x, y))
        return out

    area = w * h
    nb = max(1, round(ITEM_RATE * area / 1000))
    nh = max(1, round(HIDDEN_RATE * area / 1000))
    balls = pick(BALL_ON, nb, 11, True)
    # a nook is what a visible item ball wants; a buried one is buried anywhere
    hidden = [p for p in pick(HIDDEN_ON, nh + len(balls), 29, False)
              if all(abs(p[0]-b[0]) + abs(p[1]-b[1]) >= APART for b in balls)][:nh]
    elev = lambda x, y: (raw[y*w + x] >> 12) & 0xF
    return ([(x, y, elev(x, y)) for x, y in balls],
            [(x, y, elev(x, y)) for x, y in hidden])

# A hidden item does not store its flag: bg_hidden_item_event stores the
# offset from FLAG_HIDDEN_ITEMS_START in a single byte, and the assembler
# refuses anything below it. So a hidden item can only use a flag in that one
# 256-wide window; vanilla has used 112 of it, and the rest is where ours go.
HIDDEN_WINDOW = (0x1F4, 0x1F4 + 0xFF)

def unused_flags(text, lo=0, hi=0x4FF):
    """every flag the game is not using in a range, lowest first."""
    out = []
    for m in re.finditer(r'^#define (FLAG_UNUSED_0x[0-9A-Fa-f]+)\s+'
                         r'(0x[0-9A-Fa-f]+) // Unused Flag$', text, re.M):
        if lo <= int(m.group(2), 16) <= hi:
            out.append((m.group(0), m.group(1), m.group(2)))
    return out

def release(text):
    """hand back every flag a previous run claimed, so this one starts fresh.

    The claim keeps the old name in a comment for exactly this reason: the tool
    has to be re-runnable without walking the flag pool forward every time."""
    def back(m):
        val, old = m.group(1), m.group(2)
        return f'#define {old}{" " * max(1, 60 - len(old))}{val} // Unused Flag'
    return re.sub(r'^#define \S+\s+(0x[0-9A-Fa-f]+) ' + re.escape(MARK)
                  + r' \((FLAG_UNUSED_0x[0-9A-Fa-f]+)\)$', back, text, flags=re.M)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    lay, maps, pos = R.solve()
    rend = R.Renderer()
    beh = T.behaviors('gTileset_General')

    flags = open(f'{R.ROOT}/{FLAGS}').read()
    flags = release(flags)
    hidden_pool = unused_flags(flags, *HIDDEN_WINDOW)
    taken = {f[1] for f in hidden_pool}
    pool = [f for f in unused_flags(flags) if f[1] not in taken]
    if not pool or not hidden_pool:
        sys.exit('no unused flags left')

    plan, claimed, hclaimed, scripts = [], [], [], []
    used_names = set(re.findall(r'#define (FLAG_\w+)', flags))
    for spec in N.NEWMAPS:
        balls, hidden = spots(spec, lay, maps, rend, beh)
        n = spec['num']
        objs, bgs = [], []
        for k, (x, y, e) in enumerate(balls):
            item = BALL_ITEMS[(n * 5 + k * 3) % len(BALL_ITEMS)]
            name = f'FLAG_ITEM_ROUTE_{n}_{item[5:]}'
            while name in used_names:
                name += '_B'
            used_names.add(name)
            claimed.append(name)
            script = f'{spec["name"]}_EventScript_Item{camel(item)}'
            while any(s[0] == script for s in scripts):
                script += 'B'
            scripts.append((script, item))
            objs.append({
                'graphics_id': 'OBJ_EVENT_GFX_ITEM_BALL', 'x': x, 'y': y,
                'elevation': e, 'movement_type': 'MOVEMENT_TYPE_LOOK_AROUND',
                'movement_range_x': 0, 'movement_range_y': 0,
                'trainer_type': 'TRAINER_TYPE_NONE',
                'trainer_sight_or_berry_tree_id': '0',
                'script': script, 'flag': name})
        for k, (x, y, e) in enumerate(hidden):
            item = HIDDEN_ITEMS[(n * 3 + k * 5) % len(HIDDEN_ITEMS)]
            name = f'FLAG_HIDDEN_ITEM_ROUTE_{n}_{item[5:]}'
            while name in used_names:
                name += '_B'
            used_names.add(name)
            hclaimed.append(name)
            bgs.append({'type': 'hidden_item', 'x': x, 'y': y, 'elevation': e,
                        'item': item, 'flag': name})
        plan.append((spec, objs, bgs))

    if len(claimed) > len(pool) or len(hclaimed) > len(hidden_pool):
        sys.exit(f'{len(claimed)} item flags wanted of {len(pool)} free, '
                 f'{len(hclaimed)} hidden of {len(hidden_pool)}')

    # claim the flags, keeping each one's value: the name changes, the bit does
    for names, src in ((claimed, pool), (hclaimed, hidden_pool)):
        for name, (line, old, val) in zip(names, src):
            pad = ' ' * max(1, 60 - len(name))
            flags = flags.replace(line, f'#define {name}{pad}{val} {MARK} ({old})', 1)
    if not a.dry_run:
        open(f'{R.ROOT}/{FLAGS}', 'w').write(flags)

    # the scripts. finditem and nothing else, exactly as vanilla writes them
    src = open(f'{R.ROOT}/{BALLS}').read()
    cut = src.find(f'\n{MARK}\n')
    if cut >= 0:
        src = src[:cut + 1]
    body = ''.join(f'{s}::\n\tfinditem {i}\n\tend\n\n' for s, i in scripts)
    if not a.dry_run:
        open(f'{R.ROOT}/{BALLS}', 'w').write(f'{src}{MARK}\n\n{body}')

    for spec, objs, bgs in plan:
        p = f'{R.ROOT}/data/maps/{spec["name"]}/map.json'
        d = json.load(open(p))
        d['object_events'] = objs
        d['bg_events'] = bgs
        if not a.dry_run:
            json.dump(d, open(p, 'w'), indent=2)
        print(f'  {spec["name"]:10s} {len(objs)} item balls, {len(bgs)} hidden')
    print(f'{sum(len(o) for _, o, _ in plan)} item balls and '
          f'{sum(len(b) for _, _, b in plan)} hidden items across '
          f'{len(plan)} maps; {len(claimed)} flags claimed of {len(pool)} free, '
          f'{len(hclaimed)} hidden-item flags of {len(hidden_pool)}')

if __name__ == '__main__':
    sys.exit(main())

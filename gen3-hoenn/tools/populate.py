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

Run after newmaps.py, which rewrites the map headers from scratch, and always
with trainers.py after it - this tool's trim() cuts scripts.inc at the first
generated block of any kind, so running it alone leaves 155 trainer objects
pointing at scripts that are no longer there, and the link fails naming every
one of them:

    python3 tools/newmaps.py && python3 tools/populate.py && python3 tools/trainers.py
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

# The one rare thing. Steven trades a level 1 METAL SLIME for each, so where it
# goes is the whole difficulty: it wants to be the furthest cell from any edge
# the route has, and only on routes that are actually deep enough to hide one.
# Walking distance from the rim, not straight-line - a cell six steps from the
# edge of the map is not hard to reach whatever the map looks like.
ORE = 'ITEM_LIQUID_ORE'
ORE_DEPTH = 40                  # steps from the nearest way in

SIGN_TILE = 0x003               # the signpost; see signs() below
MARK = '// Open Hoenn - tools/populate.py'
FLAGS = 'include/constants/flags.h'
BALLS = 'data/scripts/item_ball_scripts.inc'

def camel(item):
    return ''.join(p.capitalize() for p in item[5:].split('_'))

def camel_map(const):
    return ''.join(p.capitalize() for p in const[4:].split('_'))

def town_name(const):
    return const[4:].replace('_', ' ')

def trim(text, mark):
    """everything before the generated blocks, so this run replaces them.

    Cuts at the first generated block of any kind, not just this tool's.
    populate.py runs before trainers.py and appends after whatever it finds, so
    trimming only its own left its block sitting after trainers' - and trainers
    then cut at its own mark and took populate's with it. Eleven route signs
    with no script behind them, and a link error naming every one.
    """
    i = text.find(mark)
    return text if i < 0 else text[:i].rstrip('\n') + '\n'

def load(const, lay, maps):
    """the map's blockdata with this tool's own signposts taken back out.

    A signpost is solid, and the second run would see the first run's as a wall
    and put the sign somewhere else - and the run after that somewhere else
    again. Every cell that holds one goes back to whatever its walkable
    neighbours are, so the tool always decides from the map newmaps.py wrote.
    """
    L = lay[maps[const]['layout']]
    w, h = L['width'], L['height']
    blk = open(f'{R.ROOT}/{L["blockdata_filepath"]}', 'rb').read()
    raw = [(blk[i*2] | (blk[i*2+1] << 8)) for i in range(w * h)]
    for i, v in enumerate(raw):
        if (v & 0x3FF) != SIGN_TILE:
            continue
        x, y = i % w, i // w
        near = collections.Counter(
            raw[ny*w + nx] for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1))
            if 0 <= nx < w and 0 <= ny < h and not ((raw[ny*w + nx] >> 10) & 3))
        if near:
            raw[i] = near.most_common(1)[0][0]
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

def articulations(walk, ele, w, h):
    """cells the map falls apart without.

    A sprite is solid and stays solid: an item ball you have not picked up and
    a trainer you have already beaten both block their cell for good. Standing
    one in a one-cell gap shuts whatever is behind it - Route 137 had 252 cells
    behind a single sprite - and nothing else in the pipeline can see that,
    because the terrain on its own is fine.

    Tarjan's articulation points, iteratively: recursion depth would be the
    length of the longest path through a 7,000-cell map.
    """
    ok = lambda a, b: a == b or 0 in (a, b) or 15 in (a, b)
    nbrs = lambda i: [j for j in (i+1, i-1, i+w, i-w)
                      if 0 <= j < w*h and abs(j % w - i % w) <= 1
                      and walk[j] and ok(ele[i], ele[j])]
    num = {}
    low = {}
    cut = set()
    t = 0
    for root in range(w * h):
        if not walk[root] or root in num:
            continue
        stack = [(root, None, iter(nbrs(root)))]
        num[root] = low[root] = t
        t += 1
        kids = 0
        while stack:
            i, parent, it = stack[-1]
            j = next(it, None)
            if j is None:
                stack.pop()
                if stack:
                    p = stack[-1][0]
                    low[p] = min(low[p], low[i])
                    if stack[-1][1] is not None and low[i] >= num[p]:
                        cut.add(p)
                continue
            if j == parent:
                continue
            if j in num:
                low[i] = min(low[i], num[j])
            else:
                if i == root:
                    kids += 1
                num[j] = low[j] = t
                t += 1
                stack.append((j, i, iter(nbrs(j))))
        if kids > 1:
            cut.add(root)
    return cut

def spots(spec, lay, maps, rend, beh):
    """(ball positions, hidden positions) for one map, both deterministic."""
    const = spec['const']
    L, w, h, raw = load(const, lay, maps)
    C = T.Classifier(rend, L['primary_tileset'], L.get('secondary_tileset'))
    cls = [C(v & 0x3FF, (v >> 10) & 3) for v in raw]
    live, walk = reachable(w, h, raw, cls)
    ele = [(v >> 12) & 0xF for v in raw]
    cut = articulations(walk, ele, w, h)
    jump = set(range(0x38, 0x40))

    def usable(i, want, solid):
        x, y = i % w, i // w
        if not (MARGIN <= x < w - MARGIN and MARGIN <= y < h - MARGIN):
            return False
        if i not in live or cls[i] not in want:
            return False
        if solid and i in cut:
            return False        # a buried item has no sprite and blocks nothing
        m = raw[i] & 0x3FF
        return not (m < len(beh) and beh[m] in jump)

    def tucked(i):
        x, y = i % w, i // w
        return sum(1 for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1))
                   if 0 <= nx < w and 0 <= ny < h and not walk[ny*w + nx])

    def pick(want, n, salt, need_nook, solid=True):
        cand = [i for i in range(w*h) if usable(i, want, solid)
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

    def depths():
        """steps from the nearest rim cell, over ground the player can walk."""
        seed = [i for i in live if i % w in (0, w-1) or i // w in (0, h-1)]
        d = {i: 0 for i in seed}
        q = collections.deque(seed)
        while q:
            i = q.popleft()
            x, y = i % w, i // w
            for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                j = ny*w + nx
                if (0 <= nx < w and 0 <= ny < h and j not in d and j in live
                        and ok(ele[i], ele[j])):
                    d[j] = d[i] + 1
                    q.append(j)
        return d

    ok = lambda a, b: a == b or 0 in (a, b) or 15 in (a, b)
    far = depths()

    area = w * h
    nb = max(1, round(ITEM_RATE * area / 1000))
    nh = max(1, round(HIDDEN_RATE * area / 1000))
    balls = pick(BALL_ON, nb, 11, True)

    # the ore goes as far in as the route can put it, on ground an item ball
    # can stand on and out of the way of everything else already placed
    deep = [i for i in sorted(far, key=lambda i: -far[i])
            if usable(i, BALL_ON, True)
            and all(abs(i % w - x) + abs(i // w - y) >= APART for x, y in balls)]
    ore = [(deep[0] % w, deep[0] // w)] if deep and far[deep[0]] >= ORE_DEPTH else []
    balls = balls + ore
    # a nook is what a visible item ball wants; a buried one is buried anywhere
    hidden = [p for p in pick(HIDDEN_ON, nh + len(balls), 29, False, solid=False)
              if all(abs(p[0]-b[0]) + abs(p[1]-b[1]) >= APART for b in balls)][:nh]
    elev = lambda x, y: (raw[y*w + x] >> 12) & 0xF
    used = set(balls) | set(hidden)
    return ([(x, y, elev(x, y)) for x, y in balls],
            [(x, y, elev(x, y)) for x, y in hidden],
            signs(spec, w, h, raw, cls, live, walk, cut, used),
            set(ore))

# A route sign is metatile 003, which vanilla uses 101 times and always at
# collision 1 - you read it, you do not stand on it. All 23 of vanilla's route
# sign texts are the same two lines: the route's name, then an arrow and where
# that way goes.
TOWNS = ('_TOWN', '_CITY')
ARROW = {'left': 'LEFT_ARROW', 'right': 'RIGHT_ARROW',
         'up': 'UP_ARROW', 'down': 'DOWN_ARROW'}

def signs(spec, w, h, raw, cls, live, walk, cut, used):
    """one sign per edge that leads to a town, pointing at it.

    Vanilla signs the way to places worth naming: RUSTBORO CITY, PETALBURG
    CITY, OLDALE TOWN. It does not sign the way to another route. Ours border
    seven towns between them.
    """
    # from the header newmaps.py just wrote, not from its CONN table: that is
    # replaced at run time by the derived one and the import sees the seed
    j = json.load(open(f'{R.ROOT}/data/maps/{spec["name"]}/map.json'))
    out = []
    for c in sorted((c['direction'], c['map'], c.get('offset', 0))
                    for c in j.get('connections') or []):
        side, nb, off = c
        if not nb.endswith(TOWNS):
            continue
        # a walkable cell near that edge, with open ground beside it to read
        # it from, that nothing falls apart without
        if side in ('left', 'right'):
            xs = [3] if side == 'left' else [w - 4]
            ys = range(max(2, off + 2), min(h - 2, off + 40))
        else:
            ys = [3] if side == 'up' else [h - 4]
            xs = range(max(2, off + 2), min(w - 2, off + 40))
        best = None
        for x in xs:
            for y in ys:
                i = y*w + x
                if i not in live or i in cut or (x, y) in used:
                    continue
                if cls[i] not in (T.GRASS, T.PATH, T.SAND):
                    continue
                near = sum(1 for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1))
                           if 0 <= nx < w and 0 <= ny < h and walk[ny*w + nx])
                if near < 3:
                    continue            # room to stand and read it
                k = abs(y - (off + h // 2)) if side in ('left', 'right') else \
                    abs(x - (off + w // 2))
                if best is None or k < best[0]:
                    best = (k, x, y, side, nb)
        if best:
            used.add((best[1], best[2]))
            out.append(best[1:])
    return out

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
        balls, hidden, posts, ore = spots(spec, lay, maps, rend, beh)
        n = spec['num']
        objs, bgs = [], []
        for k, (x, y, e) in enumerate(balls):
            item = ORE if (x, y) in ore else BALL_ITEMS[(n * 5 + k * 3) % len(BALL_ITEMS)]
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
        posts = [(x, y, side, nb) for x, y, side, nb in posts]
        for x, y, side, nb in posts:
            script = f'{spec["name"]}_EventScript_RouteSign{camel_map(nb)}'
            bgs.append({'type': 'sign', 'x': x, 'y': y, 'elevation': 0,
                        'player_facing_dir': 'BG_EVENT_PLAYER_FACING_ANY',
                        'script': script})
        plan.append((spec, objs, bgs, posts))

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

    for spec, objs, bgs, posts in plan:
        p = f'{R.ROOT}/data/maps/{spec["name"]}/map.json'
        d = json.load(open(p))
        # Keep whatever this tool did not put here. It used to assign the
        # list outright, which quietly deleted all 155 of tools/trainers.py's
        # trainers the next time this ran on its own - the two tools write the
        # same field, and only one of them was being careful about it.
        mine = lambda o: (o.get('graphics_id') == 'OBJ_EVENT_GFX_ITEM_BALL'
                          and 'FLAG_ITEM_' in str(o.get('flag')))
        d['object_events'] = [o for o in (d.get('object_events') or [])
                              if not mine(o)] + objs
        theirs = lambda e: e.get('type') not in ('hidden_item', 'sign')
        d['bg_events'] = [e for e in (d.get('bg_events') or [])
                          if theirs(e)] + bgs
        # the sign has to be there to read: metatile 003 is what a signpost
        # looks like, and it is on the painter's avoid list precisely so that
        # one never appears without a script behind it. This is the script.
        L, w, h, raw = load(spec['const'], lay, maps)
        for x, y, side, nb in posts:
            raw[y*w + x] = SIGN_TILE | (1 << 10)
        chunks = []
        for x, y, side, nb in posts:
            pre = f'{spec["name"]}_{{}}_RouteSign{camel_map(nb)}'
            chunks.append(
                f'{pre.format("EventScript")}::\n'
                f'\tmsgbox {pre.format("Text")}, MSGBOX_SIGN\n\tend\n\n'
                f'{pre.format("Text")}:\n'
                f'\t.string "ROUTE {spec["num"]}\\n"\n'
                f'\t.string "{{{ARROW[side]}}} {town_name(nb)}$"\n\n')
        sp = f'{R.ROOT}/data/maps/{spec["name"]}/scripts.inc'
        body = trim(open(sp).read(), '// Open Hoenn - tools/').rstrip('\n')
        if not a.dry_run:
            json.dump(d, open(p, 'w'), indent=2)
            open(f'{R.ROOT}/{L["blockdata_filepath"]}', 'wb').write(
                b''.join(v.to_bytes(2, 'little') for v in raw))
            open(sp, 'w').write(f'{body}\n\n{MARK}\n\n' + ''.join(chunks))
        print(f'  {spec["name"]:10s} {len(objs)} item balls, '
              f'{len([b for b in bgs if b["type"] == "hidden_item"])} hidden, '
              f'{len(posts)} signs')
    print(f'{sum(len(o) for _, o, _, _ in plan)} item balls, '
          f'{sum(1 for _, _, b, _ in plan for e in b if e["type"] == "hidden_item")} '
          f'hidden items and {sum(len(q) for _, _, _, q in plan)} signs across '
          f'{len(plan)} maps; {len(claimed)} flags claimed of {len(pool)} free, '
          f'{len(hclaimed)} hidden-item flags of {len(hidden_pool)}')

if __name__ == '__main__':
    sys.exit(main())

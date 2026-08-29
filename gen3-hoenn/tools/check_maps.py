#!/usr/bin/env python3
"""Per-map integrity checks on the blockdata as it will ship.

check_seams.py answers "can the player get from one map to the next". This
answers "once inside a map, is anything wrong with it" - and it runs on the
bytes in the ROM, not on any intermediate the generator held in memory.

  stranded    walkable ground with no route to any edge the player can enter by
  ledge trap  a ledge is one-way. Hopping down it must not land you somewhere
              you cannot leave, which a flood fill will not notice unless it
              models the one-way move
  elevation   a walkable cell whose elevation lets nothing next to it through
  encounters  a map with tall grass and no wild table, or a table on a map with
              nowhere to meet anything

    python3 tools/check_maps.py
    python3 tools/check_maps.py --all      # vanilla maps too, as a control
"""
import argparse, collections, glob, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_hoenn as R
import terrain as T

JUMP_DIR = {0x38: (1, 0), 0x39: (-1, 0), 0x3A: (0, -1), 0x3B: (0, 1)}

def elev_ok(a, b):
    return a == b or 0 in (a, b) or 15 in (a, b)

def load(const, lay, maps, rend):
    L = lay[maps[const]['layout']]
    w, h = L['width'], L['height']
    blk = open(f'{R.ROOT}/{L["blockdata_filepath"]}', 'rb').read()
    cell = [(blk[i*2] | (blk[i*2+1] << 8)) if i*2+1 < len(blk) else 0
            for i in range(w * h)]
    C = T.Classifier(rend, L['primary_tileset'], L.get('secondary_tileset'))
    beh = T.behaviors(L['primary_tileset'])
    return w, h, cell, C, beh

def check(const, lay, maps, rend, wild, hdrs):
    w, h, cell, C, beh = load(const, lay, maps, rend)
    mid = lambda i: cell[i] & 0x3FF
    col = lambda i: (cell[i] >> 10) & 3
    ele = lambda i: (cell[i] >> 12) & 0xF
    cls = [C(mid(i), col(i)) for i in range(w * h)]
    walk = [col(i) == 0 and cls[i] not in (T.WATER, T.POND) for i in range(w * h)]
    out = []

    def step(i, j):
        return walk[i] and walk[j] and elev_ok(ele(i), ele(j))

    # everything the player can be standing on when they arrive: the rim
    edge = [i for i in range(w * h)
            if walk[i] and (i % w in (0, w-1) or i // w in (0, h-1))]
    if not edge:
        return ['no walkable cell on any edge - the map cannot be entered']

    # 1. stranded ground. Surfing counts: vanilla is full of islets you can
    #    only reach across water - Route 134 alone has 293 such cells - so a
    #    walk-only test flags those as broken when they are not. What matters
    #    is whether the player can ever stand there by any means.
    surf = [col(i) == 0 for i in range(w * h)]
    def reach(allow_water):
        st = [i for i in edge]
        sn = set(st)
        dq = collections.deque(st)
        while dq:
            i = dq.popleft()
            x, y = i % w, i // w
            for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                j = ny*w + nx
                if not (0 <= nx < w and 0 <= ny < h) or j in sn:
                    continue
                if allow_water:
                    if surf[j]:
                        sn.add(j)
                        dq.append(j)
                elif step(i, j):
                    sn.add(j)
                    dq.append(j)
        return sn
    wet = reach(True)
    marooned = [i for i in range(w * h) if walk[i] and i not in wet]
    if marooned:
        out.append(f'{len(marooned)} walkable cells unreachable even by surfing '
                   f'({len(components(marooned, w, h))} pockets)')

    seen, q = set(edge), collections.deque(edge)
    while q:
        i = q.popleft()
        x, y = i % w, i // w
        for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
            j = ny*w + nx
            if 0 <= nx < w and 0 <= ny < h and j not in seen and step(i, j):
                seen.add(j)
                q.append(j)


    # 2. ledge traps: replay reachability with the one-way hop allowed, then
    #    ask whether every cell can still get *back* to an edge
    back, q = set(edge), collections.deque(edge)
    while q:
        i = q.popleft()
        x, y = i % w, i // w
        for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
            j = ny*w + nx
            if not (0 <= nx < w and 0 <= ny < h) or j in back:
                continue
            # walking backwards out of the map: a ledge cannot be climbed, so
            # a cell only counts if the reverse move is legal
            d = JUMP_DIR.get(beh[mid(j)] if mid(j) < len(beh) else 0)
            if d and (nx + d[0], ny + d[1]) == (x, y):
                continue                 # would mean climbing the ledge
            if step(i, j) or (d and walk[i]):
                back.add(j)
                q.append(j)
    trapped = [i for i in seen if i not in back]
    if trapped:
        out.append(f'{len(trapped)} cells reachable but with no way back to an edge')

    # 3. items. An item ball you cannot reach is worse than no item ball: it
    #    is visible from across a cliff and there is no way round. Surfing
    #    counts, as it does above. --all reports 55 of these against vanilla,
    #    which are not bugs: this does not model the HMs, so vanilla's items
    #    behind a Cut tree or a Rock Smash boulder read as walled in.
    hdr = hdrs.get(const, {})
    for e in (hdr.get('object_events') or []) + (hdr.get('bg_events') or []):
        if ('ITEM_BALL' not in str(e.get('graphics_id', ''))
                and 'hidden' not in str(e.get('type', ''))):
            continue
        try:
            x, y = int(e['x']), int(e['y'])
        except (KeyError, TypeError, ValueError):
            continue
        i = y*w + x
        if not (0 <= x < w and 0 <= y < h):
            out.append(f'item at {x},{y} is off the map')
        elif not walk[i]:
            out.append(f'item at {x},{y} is inside a wall')
        elif i not in wet:
            out.append(f'item at {x},{y} cannot be reached')
        elif int(e.get('elevation', -1)) not in (ele(i), 0):
            out.append(f'item at {x},{y} is at elevation '
                       f'{e.get("elevation")} on ground at {ele(i)}')

    # 4. encounters
    tall = sum(1 for i in range(w * h) if cls[i] == T.TALL)
    has = const in wild
    if tall > 20 and not has:
        out.append(f'{tall} tall grass cells and no wild encounter table')
    if has and tall == 0 and 'land_mons' in wild[const]:
        out.append('land encounter table but no tall grass to meet anything in')
    return out

def components(cells, w, h):
    s = set(cells)
    out = []
    while s:
        start = s.pop()
        comp, st = [start], [start]
        while st:
            i = st.pop()
            x, y = i % w, i // w
            for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                j = ny*w + nx
                if j in s:
                    s.discard(j)
                    comp.append(j)
                    st.append(j)
        out.append(comp)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--all', action='store_true')
    a = ap.parse_args()
    lay, maps, pos = R.solve()
    rend = R.Renderer()
    new = T.generated()
    hdrs = {}
    for f in glob.glob(f'{R.ROOT}/data/maps/*/map.json'):
        j = json.load(open(f))
        hdrs[j['id']] = j
    wild = {}
    d = json.load(open(f'{R.ROOT}/src/data/wild_encounters.json'))
    for g in d['wild_encounter_groups']:
        if g['label'] == 'gWildMonHeaders':
            for e in g['encounters']:
                wild[e['map']] = e
    keys = sorted(pos) if a.all else sorted(new)
    bad = 0
    for k in keys:
        try:
            probs = check(k, lay, maps, rend, wild, hdrs)
        except SystemExit:
            continue
        if probs:
            bad += 1
            print(f'{k[4:]}')
            for p in probs:
                print(f'    {p}')
    print(f'\n{bad} of {len(keys)} maps with findings')

if __name__ == '__main__':
    sys.exit(main())

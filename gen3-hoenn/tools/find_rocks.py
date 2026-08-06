#!/usr/bin/env python3
"""Find the rock clusters sitting in the open water of the surf routes.

Routes 105-109 are almost entirely water, broken up by scattered rocks, and the
sketch asks for some of them gone. "Rock" is defined the way the game defines
it rather than by eye: a metatile counts as water if its behavior byte in
`metatile_attributes.bin` is one of the water behaviors, and a rock is a
connected run of non-water metatiles that is *entirely enclosed by water* and
never touches a map edge. That last clause is what keeps shorelines, the
Dewford beach and the west cliffs of Route 105 out of the list — they are land,
not obstacles in the sea.

    python3 tools/find_rocks.py
    python3 tools/find_rocks.py --sketch sketches/sketch01.json

Coordinates printed are world metatile coordinates, the same frame the sketch
tool exports in, so a cluster can be found again on the rendered map.
"""
import argparse, collections, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_hoenn as R

ROUTES = ['MAP_ROUTE105', 'MAP_ROUTE106', 'MAP_ROUTE107', 'MAP_ROUTE108', 'MAP_ROUTE109']

# from include/constants/metatile_behaviors.h
WATER_MB = {0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x17, 0x18, 0x1a, 0x22, 0x2a}
NUM_METATILES_IN_PRIMARY = 512

def behaviors(prim, sec):
    """behavior byte per metatile id, primary then secondary."""
    out = {}
    for kind, base in ((prim, 0), (sec, NUM_METATILES_IN_PRIMARY)):
        if not kind:
            continue
        p = os.path.join(R.tileset_dir(kind), 'metatile_attributes.bin')
        b = open(p, 'rb').read()
        for i in range(len(b) // 2):
            out[base + i] = b[i * 2]
    return out

def clusters(lay, maps, pos, minx, miny, route):
    L = lay[maps[route]['layout']]
    w, h = L['width'], L['height']
    blk = open(f'{R.ROOT}/{L["blockdata_filepath"]}', 'rb').read()
    mb = behaviors(L['primary_tileset'], L.get('secondary_tileset'))
    solid = set()
    for j in range(h):
        for i in range(w):
            o = (j * w + i) * 2
            if o + 1 >= len(blk):
                continue
            if mb.get((blk[o] | (blk[o+1] << 8)) & 0x3FF, 0) not in WATER_MB:
                solid.add((i, j))
    mx, my = pos[route]
    out, seen = [], set()
    for c in sorted(solid):
        if c in seen:
            continue
        comp, st, edge = {c}, [c], False
        seen.add(c)
        while st:
            x, y = st.pop()
            if x in (0, w - 1) or y in (0, h - 1):
                edge = True
            for n in ((x+1, y), (x-1, y), (x, y+1), (x, y-1),
                      (x+1, y+1), (x-1, y-1), (x+1, y-1), (x-1, y+1)):
                if n in solid and n not in seen:
                    seen.add(n); comp.add(n); st.append(n)
        if not edge:                      # touching an edge means it is land
            out.append({(x + mx - minx, y + my - miny) for x, y in comp})
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sketch', help='only report clusters a stroke passes over')
    ap.add_argument('--near', type=int, default=2,
                    help='a stroke point within N metatiles counts as a hit')
    ap.add_argument('--verbose', action='store_true', help='list every cluster')
    a = ap.parse_args()

    lay, maps, pos = R.solve()
    minx = min(x for x, _ in pos.values()); miny = min(y for _, y in pos.values())

    marks = set()
    if a.sketch:
        sk = json.load(open(a.sketch))
        for s in sk['strokes']:
            for x, y in ([s['at']] if s['pen'] == 'label' else s['points']):
                for dx in range(-a.near, a.near + 1):
                    for dy in range(-a.near, a.near + 1):
                        marks.add((int(x) + dx, int(y) + dy))

    tot_c = tot_m = hit_c = hit_m = 0
    for r in ROUTES:
        cs = clusters(lay, maps, pos, minx, miny, r)
        hits = [c for c in cs if c & marks] if a.sketch else cs
        tot_c += len(cs); tot_m += sum(len(c) for c in cs)
        hit_c += len(hits); hit_m += sum(len(c) for c in hits)
        line = f'  {r[4:]:9s} {len(cs):3d} clusters / {sum(len(c) for c in cs):4d} metatiles'
        if a.sketch:
            line += f'   -> {len(hits):2d} under strokes ({sum(len(c) for c in hits):3d})'
        print(line)
        for c in sorted((a.verbose and cs) or hits, key=lambda c: -len(c)):
            xs = [p[0] for p in c]; ys = [p[1] for p in c]
            mark = ' *' if a.verbose and c in hits else '  '
            print(f'    {mark} {len(c):3d} mt  world x {min(xs)}-{max(xs)}  y {min(ys)}-{max(ys)}')
    print(f'\n  all five: {tot_c} clusters, {tot_m} metatiles')
    if a.sketch:
        print(f'  under strokes: {hit_c} clusters, {hit_m} metatiles')

if __name__ == '__main__':
    sys.exit(main())

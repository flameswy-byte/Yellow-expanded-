#!/usr/bin/env python3
"""Do the metatiles we place next to each other ever sit next to each other
in vanilla?

The autotiler picks each cell from a 3x3 mask of terrain *classes*. That is a
coarse description: two metatiles can each be a perfectly reasonable choice for
their own class neighbourhood and still never appear side by side in the real
game, because their art does not line up. Grass with a rock edge on its right
next to grass with no rock edge on its left is a visible seam, and no
class-level check can see it - both cells are "grass beside grass".

So this tallies, over every vanilla map on the General tileset, which ordered
metatile pairs occur horizontally and which vertically, and then reports the
pairs our maps use that vanilla never does.

    python3 tools/check_adjacency.py            # summary
    python3 tools/check_adjacency.py --worst 30 # the pairs to go fix
    python3 tools/check_adjacency.py --map ROUTE_139
"""
import argparse, collections, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_hoenn as R
import terrain as T

def cells(L, pristine=False):
    w, h = L['width'], L['height']
    # the vanilla side of the comparison has to be vanilla: the maps whose
    # borders we softened would otherwise vouch for our own tile pairs
    blk = (T.blockdata(L['blockdata_filepath'].split('/')[-2], L) if pristine
           else open(f'{R.ROOT}/{L["blockdata_filepath"]}', 'rb').read())
    raw = [(blk[i*2] | (blk[i*2+1] << 8)) if i*2+1 < len(blk) else 0
           for i in range(w * h)]
    return w, h, raw

def pairs(w, h, raw):
    """yield (axis, a, b) for every adjacent pair of primary metatiles.

    Ids only - collision and elevation live in the same u16 but do not change
    what the cell looks like, and a shore drawn at two elevations is still the
    same shore."""
    P = R.NUM_METATILES_IN_PRIMARY
    m = [v & 0x3FF for v in raw]
    for y in range(h):
        for x in range(w):
            i = y * w + x
            if m[i] >= P:
                continue
            if x + 1 < w and m[i+1] < P:
                yield 0, m[i], m[i+1]
            if y + 1 < h and m[i+w] < P:
                yield 1, m[i], m[i+w]

def vanilla_pairs(lay, maps, pos, skip):
    seen = (collections.Counter(), collections.Counter())
    for k in sorted(pos):
        if k in skip or k not in maps:
            continue
        L = lay[maps[k]['layout']]
        if L['primary_tileset'] != 'gTileset_General':
            continue
        w, h, raw = cells(L, pristine=True)
        for ax, a, b in pairs(w, h, raw):
            seen[ax][(a, b)] += 1
    return seen

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--worst', type=int, default=0,
                    help='list the N most common unseen pairs')
    ap.add_argument('--map', help='restrict to one map, e.g. ROUTE_139')
    ap.add_argument('--control', action='store_true',
                    help='score vanilla maps against the other vanilla maps')
    a = ap.parse_args()
    lay, maps, pos = R.solve()
    rend = R.Renderer()
    new = T.generated()
    van = vanilla_pairs(lay, maps, pos, new)
    print(f'vanilla: {len(van[0])} horizontal, {len(van[1])} vertical '
          f'metatile pairs')

    if a.control:
        # 0% is not the target. A vanilla map scored against the *other*
        # vanilla maps still has joins nothing else uses, because some seams
        # are drawn once in the whole game. That number is the floor.
        rows = []
        for k in sorted(pos):
            if k in new or k not in maps:
                continue
            L = lay[maps[k]['layout']]
            if L['primary_tileset'] != 'gTileset_General':
                continue
            w, h, raw = cells(L, pristine=True)
            mine = (collections.Counter(), collections.Counter())
            for ax, x, y in pairs(w, h, raw):
                mine[ax][(x, y)] += 1
            n = sum(c for ax in (0, 1) for p, c in mine[ax].items()
                    if van[ax][p] == c)          # this map's only use of it
            tot = sum(sum(m.values()) for m in mine)
            if tot:
                rows.append((100.0*n/tot, k, n, tot))
        rows.sort()
        import statistics
        print(f'\nvanilla leave-one-out: median {statistics.median(r[0] for r in rows):.2f}%'
              f'  [{rows[0][0]:.2f}% - {rows[-1][0]:.2f}%] over {len(rows)} maps')
        for p, k, n, tot in rows[-6:]:
            print(f'    {k[4:]:22s} {n:5d} / {tot:6d}  {p:5.2f}%')

    C = T.Classifier(rend, 'gTileset_General', None)
    bad = collections.Counter()
    per_map = {}
    keys = [k for k in sorted(new) if not a.map or a.map in k]
    for k in keys:
        L = lay[maps[k]['layout']]
        w, h, raw = cells(L)
        n = tot = 0
        for ax, x, y in pairs(w, h, raw):
            tot += 1
            if (x, y) not in van[ax]:
                n += 1
                bad[(ax, x, y)] += 1
        per_map[k] = (n, tot)
    print()
    for k in keys:
        n, tot = per_map[k]
        print(f'  {k[4:]:12s} {n:6d} / {tot:6d}  {100.0*n/max(tot,1):5.2f}% '
              f'pairs vanilla never draws')
    n = sum(v[0] for v in per_map.values())
    tot = sum(v[1] for v in per_map.values())
    print(f'  {"TOTAL":12s} {n:6d} / {tot:6d}  {100.0*n/max(tot,1):5.2f}%')

    # which class transitions the unseen pairs fall on: that says whether the
    # problem is one bad tile or a whole seam type
    byc = collections.Counter()
    for (ax, x, y), c in bad.items():
        byc[(T.CLASS_NAME[C(x, 0)], T.CLASS_NAME[C(y, 0)])] += c
    print('\nunseen pairs by class transition:')
    for (p, q), c in byc.most_common(12):
        print(f'  {p:11s} -> {q:11s} {c:6d}')

    if a.worst:
        print(f'\n{a.worst} most common pairs vanilla never draws:')
        for (ax, x, y), c in bad.most_common(a.worst):
            print(f'  {"HV"[ax]} {x:03X} {T.CLASS_NAME[C(x,0)]:11s} | '
                  f'{y:03X} {T.CLASS_NAME[C(y,0)]:11s}  x{c}')

if __name__ == '__main__':
    sys.exit(main())

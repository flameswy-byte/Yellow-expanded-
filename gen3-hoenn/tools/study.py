#!/usr/bin/env python3
"""Measure how vanilla Hoenn routes are actually built, and compare ours.

The generator has been tuned by eye against single screenshots, which is how
you end up with a route that is 69% tall grass and looks fine in a crop. This
measures the things that only show up in aggregate - what fraction of a route
is each kind of terrain, how big its grass patches and tree clumps are, how
much of it you can walk on - across every vanilla route, and prints ours
against the same yardstick.

Towns and the pure water routes are excluded: a town is mostly buildings and a
water route is mostly water, and neither tells you how to build a land route.

    python3 tools/study.py
    python3 tools/study.py --per-map
"""
import argparse, collections, json, os, statistics, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_hoenn as R
import terrain as T

JUMP_MB = set(range(0x38, 0x40))

def components(cls, want, w, h):
    seen = [False] * (w * h)
    out = []
    for s in range(w * h):
        if seen[s] or cls[s] not in want:
            continue
        n, q = 0, [s]
        seen[s] = True
        while q:
            i = q.pop()
            n += 1
            x, y = i % w, i // w
            for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                j = ny*w + nx
                if 0 <= nx < w and 0 <= ny < h and not seen[j] and cls[j] in want:
                    seen[j] = True
                    q.append(j)
        out.append(n)
    return out

def measure(const, lay, maps, rend):
    L = lay[maps[const]['layout']]
    w, h = L['width'], L['height']
    blk = open(f'{R.ROOT}/{L["blockdata_filepath"]}', 'rb').read()
    C = T.Classifier(rend, L['primary_tileset'], L.get('secondary_tileset'))
    beh = T.behaviors(L['primary_tileset'])
    raw = [(blk[i*2] | (blk[i*2+1] << 8)) if i*2+1 < len(blk) else 0
           for i in range(w * h)]
    cls = [C(v & 0x3FF, (v >> 10) & 3) for v in raw]
    n = collections.Counter(cls)
    tot = w * h
    walk = sum(1 for v in raw if ((v >> 10) & 3) == 0
               and C(v & 0x3FF, 0) != T.WATER)
    tall = components(cls, {T.TALL}, w, h)
    tree = components(cls, {T.TREE}, w, h)
    ledge = sum(1 for v in raw if (v & 0x3FF) < len(beh)
                and beh[v & 0x3FF] in JUMP_MB)
    # how much of the tall grass touches open ground you would actually
    # walk on - vanilla puts patches beside the path, not in a slab
    edge = 0
    for i, c in enumerate(cls):
        if c != T.TALL:
            continue
        x, y = i % w, i // w
        if any(0 <= x+dx < w and 0 <= y+dy < h
               and cls[(y+dy)*w + x+dx] in (T.GRASS, T.PATH, T.SAND)
               for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            edge += 1
    # land-relative shares matter more than map-relative ones: a route that is
    # half sea is not "low on grass", it just has less ground to put it on
    land = sum(n[c] for c in (T.GRASS, T.TALL, T.TREE, T.PATH, T.SAND)) or 1
    return dict(w=w, h=h, cells=tot, walk=100.0*walk/tot,
                land=100.0*land/tot,
                tall_l=100.0*n[T.TALL]/land, tree_l=100.0*n[T.TREE]/land,
                grass_l=100.0*n[T.GRASS]/land, path_l=100.0*n[T.PATH]/land,
                tall=100.0*n[T.TALL]/tot, tree=100.0*n[T.TREE]/tot,
                grass=100.0*n[T.GRASS]/tot, path=100.0*n[T.PATH]/tot,
                water=100.0*n[T.WATER]/tot, cliff=100.0*n[T.CLIFF]/tot,
                tallpatch=tall, treeclump=tree, ledge=ledge,
                tall_edge=(100.0*edge/n[T.TALL]) if n[T.TALL] else 0.0)

def band(rows, key):
    v = [r[key] for r in rows]
    return f'{statistics.median(v):5.1f}  [{min(v):4.1f} - {max(v):5.1f}]'

def sizes(rows, key):
    all_ = [n for r in rows for n in r[key]]
    if not all_:
        return 'none'
    return (f'{len(all_)/len(rows):5.1f} per map, median {statistics.median(all_):4.0f} '
            f'cells, largest {max(all_):5d}')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--per-map', action='store_true')
    a = ap.parse_args()
    lay, maps, pos = R.solve()
    rend = R.Renderer()
    new = T.generated()

    van, ours = [], []
    for k in sorted(pos):
        if not k.startswith('MAP_ROUTE'):
            continue                    # towns are buildings, not routes
        m = measure(k, lay, maps, rend)
        m['name'] = k[4:]
        if m['water'] > 55:
            continue                    # a sea route teaches nothing about land
        (ours if k in new else van).append(m)

    for label, rows in (('VANILLA land routes', van), ('OURS', ours)):
        print(f'\n=== {label}  ({len(rows)} maps)')
        print(f'  walkable %      {band(rows, "walk")}')
        for key in ('tall', 'tree', 'grass', 'path', 'water', 'cliff'):
            print(f'  {key:11s} %  {band(rows, key)}')
        print(f'  --- as a share of the land, not the whole map ---')
        for key in ('tall_l', 'tree_l', 'grass_l', 'path_l'):
            print(f'  {key:11s} %  {band(rows, key)}')
        print(f'  tall patches    {sizes(rows, "tallpatch")}')
        print(f'  tree clumps     {sizes(rows, "treeclump")}')
        print(f'  tall touching walkable ground  {band(rows, "tall_edge")} %')
        print(f'  ledge cells     {band(rows, "ledge")}')
        if a.per_map:
            for r in sorted(rows, key=lambda r: -r['tall']):
                print(f'    {r["name"]:10s} {r["w"]:3d}x{r["h"]:<3d} '
                      f'walk {r["walk"]:4.0f}%  tall {r["tall"]:4.1f}%  '
                      f'tree {r["tree"]:4.1f}%  path {r["path"]:4.1f}%  '
                      f'patches {len(r["tallpatch"]):3d}  ledges {r["ledge"]:3d}')

if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""Partition the remaining empty gaps into buildable maps, and work out every
connection from the geometry.

Gap 1 was partitioned by hand because it happened to fall into four clean
rectangles. The others do not, so this does it properly: repeatedly take the
largest axis-aligned rectangle that fits entirely inside the empty region and
inside the map buffer, carve it out, and go again until what is left is too
small to be worth a map.

Connections are then read off the world grid rather than derived by hand. For
each edge of each new rectangle it walks the cells immediately outside, groups
them into runs by which map owns them, and emits one connection per run. The
offset convention comes straight out of render_hoenn.solve():

    up / down     offset = neighbour.x - mine.x
    left / right  offset = neighbour.y - mine.y

    python3 tools/plan_gaps.py            # report the plan
    python3 tools/plan_gaps.py --json     # emit it for newmaps.py
"""
import argparse, collections, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_hoenn as R

MAX_MAP_DATA = 10240
MIN_CELLS = 900          # smaller than this is not worth a map header

def fits(w, h):
    return (w + 15) * (h + 14) <= MAX_MAP_DATA

def world():
    lay, maps, pos = R.solve()
    minx = min(x for x, _ in pos.values()); miny = min(y for _, y in pos.values())
    W = max(x + lay[maps[k]['layout']]['width'] for k, (x, y) in pos.items()) - minx
    H = max(y + lay[maps[k]['layout']]['height'] for k, (x, y) in pos.items()) - miny
    occ = {}
    for k, (x, y) in pos.items():
        L = lay[maps[k]['layout']]
        for yy in range(y, y + L['height']):
            for xx in range(x, x + L['width']):
                occ[(xx - minx, yy - miny)] = k
    return lay, maps, pos, occ, W, H, minx, miny

def best_rect(free, x0, y0, x1, y1):
    """largest-area rectangle of free cells inside the box, that also fits the
    map buffer. Standard largest-rectangle-in-histogram, once per row."""
    w, h = x1 - x0 + 1, y1 - y0 + 1
    heights = [0] * w
    best = (0, None)
    for j in range(h):
        for i in range(w):
            heights[i] = heights[i] + 1 if (x0 + i, y0 + j) in free else 0
        stack = []
        for i in range(w + 1):
            cur = heights[i] if i < w else 0
            start = i
            while stack and stack[-1][1] >= cur:
                s, ht = stack.pop()
                for hh in range(ht, 0, -1):        # trim height until it fits
                    ww = i - s
                    if not fits(ww, hh):
                        continue
                    area = ww * hh
                    if area > best[0]:
                        best = (area, (x0 + s, y0 + j - hh + 1, ww, hh))
                    break
                start = s
            stack.append((start, cur))
    return best[1]

def partition(cells):
    free = set(cells)
    out = []
    while free:
        xs = [p[0] for p in free]; ys = [p[1] for p in free]
        r = best_rect(free, min(xs), min(ys), max(xs), max(ys))
        if not r or r[2] * r[3] < MIN_CELLS:
            break
        x, y, w, h = r
        out.append(r)
        for j in range(y, y + h):
            for i in range(x, x + w):
                free.discard((i, j))
    return out, len(free)

def connections(rect, others, occ, minx, miny):
    """every connection off one rectangle, read from what abuts each edge."""
    x, y, w, h = rect
    owner = dict(occ)
    for name, (ox, oy, ow, oh) in others.items():
        for j in range(oy, oy + oh):
            for i in range(ox, ox + ow):
                owner[(i, j)] = name
    origin = {}
    for name, (ox, oy, _, _) in others.items():
        origin[name] = (ox, oy)
    out = []
    for side, cells, axis in (
            ('up',    [(x + i, y - 1) for i in range(w)], 'x'),
            ('down',  [(x + i, y + h) for i in range(w)], 'x'),
            ('left',  [(x - 1, y + j) for j in range(h)], 'y'),
            ('right', [(x + w, y + j) for j in range(h)], 'y')):
        seen = []
        for c in cells:
            o = owner.get(c)
            if o and o not in seen:
                seen.append(o)
        for o in seen:
            if o in origin:
                nx, ny = origin[o]
            else:
                # a vanilla map: its origin in the same world frame
                nx, ny = None, None
            out.append((side, o, nx, ny))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--json', action='store_true')
    a = ap.parse_args()
    lay, maps, pos, occ, W, H, minx, miny = world()
    regs = [r for r in R.empty_regions(occ, W, H) if r[0] >= 2000]
    inland = [r for r in regs if len({k.replace('MAP_', '') for k in r[2]} & R.WATER) < 2]

    plan = []
    for n, comp, bd in inland[:5]:
        key = (min(p[0] for p in comp), min(p[1] for p in comp))
        name = R.GAPS.get(key, ('GAP ?', '', ''))[0]
        rects, left = partition(comp)
        print(f'{name}  {n} cells -> {len(rects)} maps, {left} cells left over '
              f'({100*(n-left)//n}% covered)')
        for x, y, w, h in rects:
            print(f'    {w:3d} x {h:3d} at x{x} y{y}   buffer '
                  f'{(w+15)*(h+14)}/{MAX_MAP_DATA}   {w*h} cells')
            plan.append(dict(gap=name, x=x, y=y, w=w, h=h))
    if a.json:
        print(json.dumps(plan))

if __name__ == '__main__':
    sys.exit(main())

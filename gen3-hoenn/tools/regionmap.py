#!/usr/bin/env python3
"""Give the new routes a square on the region map.

Every one of the fourteen new MAPSECs had a name and nothing else - no x, y,
width or height - which is not merely cosmetic. region_map.c does

    dimensionScale = mapWidth / gRegionMapEntries[mapSecId].width;

so opening the region map while standing on any of them divides by zero.

The rectangle is derived, not drawn by hand: the region map is Hoenn scaled to
a 28x15 grid, and fitting vanilla's 49 placed sections against their world
positions gives that scale to within about one square. The ideal rectangle for
a map is then its world box through that fit, trimmed to squares nothing else
has claimed - vanilla's sections first, then the new ones in order.

    python3 tools/regionmap.py
"""
import argparse, collections, json, glob, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_hoenn as R
import terrain as T
import newmaps as N

SECTIONS = 'src/data/region_map/region_map_sections.json'
GRID_W, GRID_H = 28, 15

def fit(rows, i, j):
    """least squares through (world, region) for one axis."""
    n = len(rows)
    sx = sum(r[i] for r in rows)
    sy = sum(r[j] for r in rows)
    sxx = sum(r[i] * r[i] for r in rows)
    sxy = sum(r[i] * r[j] for r in rows)
    a = (n * sxy - sx * sy) / (n * sxx - sx * sx)
    return a, (sy - a * sx) / n

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    lay, maps, pos = R.solve()
    new = T.generated()
    path = f'{R.ROOT}/{SECTIONS}'
    doc = json.load(open(path))
    sec = {s['id']: s for s in doc['map_sections']}
    hdr = {}
    for f in glob.glob(f'{R.ROOT}/data/maps/*/map.json'):
        j = json.load(open(f))
        hdr[j['id']] = j

    minx = min(x for x, _ in pos.values())
    miny = min(y for _, y in pos.values())
    rows = []
    for k, (mx, my) in pos.items():
        s = sec.get((hdr.get(k) or {}).get('region_map_section'))
        if s and 'x' in s and k not in new:
            rows.append((mx - minx, my - miny, s['x'], s['y']))
    ax, bx = fit(rows, 0, 2)
    ay, by = fit(rows, 1, 3)
    print(f'region = ({ax:.5f}*worldx + {bx:.2f}, {ay:.5f}*worldy + {by:.2f}) '
          f'from {len(rows)} vanilla sections')

    taken = set()
    for s in doc['map_sections']:
        if 'x' in s and s['id'] not in {t['mapsec'] for t in N.NEWMAPS}:
            for j in range(s['height']):
                for i in range(s['width']):
                    taken.add((s['x'] + i, s['y'] + j))

    def free(x, y, w, h):
        return (0 <= x and 0 <= y and x + w <= GRID_W and y + h <= GRID_H
                and all((x+i, y+j) not in taken
                        for j in range(h) for i in range(w)))

    for spec in N.NEWMAPS:
        mx, my = pos[spec['const']]
        L = lay[maps[spec['const']]['layout']]
        x0 = round((mx - minx) * ax + bx)
        y0 = round((my - miny) * ay + by)
        x1 = round((mx - minx + L['width']) * ax + bx)
        y1 = round((my - miny + L['height']) * ay + by)
        iw, ih = max(1, x1 - x0), max(1, y1 - y0)
        # the fit is good to about a square, so the ideal rectangle can overlap
        # a neighbour by one. Staying put matters more than staying big - the
        # square is where the game says you are - so shrink before moving.
        best = None
        for w in range(iw, 0, -1):
            for h in range(ih, 0, -1):
                for dx in (0, -1, 1, -2, 2):
                    for dy in (0, -1, 1, -2, 2):
                        x, y = x0 + dx, y0 + dy
                        if not free(x, y, w, h):
                            continue
                        k = (abs(dx) + abs(dy), -(w * h))
                        if best is None or k < best[0]:
                            best = (k, x, y, w, h)
        if best is None:
            sys.exit(f'{spec["name"]}: nowhere free on the region map near '
                     f'{x0},{y0}')
        _, x, y, w, h = best
        for j in range(h):
            for i in range(w):
                taken.add((x + i, y + j))
        s = sec[spec['mapsec']]
        s.update(x=x, y=y, width=w, height=h)
        note = '' if (x, y, w, h) == (x0, y0, iw, ih) else f'  (ideal {iw}x{ih} at {x0},{y0})'
        print(f'  {spec["name"]:10s} x{x:3d} y{y:3d} {w}x{h}{note}')

    # A section with no rectangle is the one region_map.c divides by. Vanilla
    # ships nine of them - the truck, secret bases, the event islands and the
    # dynamic placeholder - and gets away with it because the region map is
    # never opened standing on one. Ours are ordinary routes, so they must not
    # be on that list.
    blank = sorted({h['region_map_section'] for h in hdr.values()
                    if not sec.get(h.get('region_map_section'), {}).get('width')})
    ours = [b for b in blank if b in {t['mapsec'] for t in N.NEWMAPS}]
    if ours:
        sys.exit('new routes with no region map rectangle: '
                 + ', '.join(b[7:] for b in ours))
    print(f'{len(hdr)} maps placed; {len(blank)} sections still without a '
          f'rectangle, all vanilla: ' + ', '.join(b[7:] for b in blank))

    if not a.dry_run:
        json.dump(doc, open(path, 'w'), indent=2)

if __name__ == '__main__':
    sys.exit(main())

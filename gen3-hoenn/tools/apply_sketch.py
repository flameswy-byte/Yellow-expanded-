#!/usr/bin/env python3
"""Read a sketch back over the map, and report what it covers.

The sketch tool exports world metatile coordinates, so a sketch can be checked
against the same solved layout everything else uses rather than eyeballed off
a picture. This draws it back onto the rendered map and says which gap each
stroke landed in, which is the confirmation step before any of it becomes real
blockdata.

    python3 tools/apply_sketch.py sketches/sketch01.json --scale 8 -o out.png
    python3 tools/apply_sketch.py sketches/sketch01.json --crop --pad 12
"""
import argparse, collections, json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_hoenn as R

PEN_COLOR = {'path': (224, 194, 116), 'grass': (87, 180, 92), 'tall grass': (46, 125, 58),
             'water': (74, 143, 214), 'trees': (31, 92, 51), 'cliff': (154, 141, 128),
             'building': (224, 138, 60), 'cave': (138, 107, 208), 'note': (232, 74, 74),
             'label': (232, 74, 74)}

def gap_boxes():
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
    regs = [r for r in R.empty_regions(occ, W, H) if r[0] >= 2000]
    inland = [r for r in regs if len({k.replace('MAP_', '') for k in r[2]} & R.WATER) < 2]
    return [(R.GAPS[i][0], comp) for i, (n, comp, bd) in enumerate(inland[:5])], occ, W, H

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('sketch')
    ap.add_argument('--scale', type=int, default=8)
    ap.add_argument('--crop', action='store_true', help='crop to the sketched area')
    ap.add_argument('--pad', type=int, default=16, help='metatiles of margin when cropping')
    ap.add_argument('-o', '--out', default='sketch_applied.png')
    a = ap.parse_args()
    S = a.scale
    HDR = S * 11

    sk = json.load(open(a.sketch))
    gaps, occ, W, H = gap_boxes()
    cells = {name: set(comp) for name, comp in gaps}

    # which gap does each stroke sit in, and how much of it is off-target
    report = collections.defaultdict(lambda: collections.Counter())
    stray = collections.Counter()
    for s in sk['strokes']:
        pts = [s['at']] if s['pen'] == 'label' else s['points']
        hits = collections.Counter()
        for x, y in pts:
            c = (int(x), int(y))
            where = next((n for n, cs in cells.items() if c in cs), None)
            hits[where or ('on a vanilla map' if c in occ else 'outside')] += 1
        best = hits.most_common(1)[0][0]
        report[best][s['pen']] += 1
        for k, v in hits.items():
            if k != best:
                stray[k] += v

    print(f'{len(sk["strokes"])} strokes, {sum(len(s.get("points", [1])) for s in sk["strokes"])} points\n')
    for where in sorted(report, key=lambda k: -sum(report[k].values())):
        tot = sum(report[where].values())
        pens = ', '.join(f'{n}x {p}' for p, n in report[where].most_common())
        print(f'  {where:18s} {tot:3d} strokes   {pens}')
    if stray:
        print(f'\n  points falling outside their stroke\'s main region: '
              + ', '.join(f'{v} {k}' for k, v in stray.most_common()))

    png = os.path.join(HERE, '..', f'_applied_bg_{S}.png')
    subprocess.run([sys.executable, os.path.join(HERE, 'render_hoenn.py'),
                    '--scale', str(S), '-o', png], check=True)
    img = Image.open(png).convert('RGB')
    d = ImageDraw.Draw(img, 'RGBA')
    to_px = lambda x, y: (x * S, y * S + HDR)
    for s in sk['strokes']:
        col = PEN_COLOR.get(s['pen'], (255, 255, 255))
        if s['pen'] == 'label':
            x, y = to_px(*s['at'])
            f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', S * 2)
            d.text((x, y), s['text'], font=f, fill=col)
            continue
        pts = [to_px(x, y) for x, y in s['points']]
        if len(pts) > 1:
            d.line(pts, fill=col + (255,), width=max(2, int(S * 0.9)), joint='curve')
        else:
            d.ellipse([pts[0][0]-S, pts[0][1]-S, pts[0][0]+S, pts[0][1]+S], fill=col + (255,))
    if a.crop:
        xs, ys = [], []
        for s in sk['strokes']:
            for x, y in ([s['at']] if s['pen'] == 'label' else s['points']):
                xs.append(x); ys.append(y)
        box = (max(0, int(min(xs) - a.pad)) * S, max(0, int(min(ys) - a.pad)) * S + HDR,
               min(W, int(max(xs) + a.pad)) * S, min(H, int(max(ys) + a.pad)) * S + HDR)
        img = img.crop(box)
    img = img.convert('P', palette=Image.ADAPTIVE, colors=256)
    img.save(a.out, optimize=True)
    os.remove(png)
    print(f'\nwrote {a.out} {img.size} ({os.path.getsize(a.out)/1e6:.1f} MB)')

if __name__ == '__main__':
    sys.exit(main())

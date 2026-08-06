#!/usr/bin/env python3
"""Render a tileset's metatiles as a labelled sheet, so you can see what a map
built on it is allowed to look like before committing to it.

A Gen 3 map draws from exactly two tilesets: a primary shared by a whole
biome (almost every outdoor map uses gTileset_General) and a secondary that
gives the area its character. Ids 0-511 come from the primary, 512+ from the
secondary, so choosing the secondary is the real decision. This renders each
one through the same code path as the map renderer, which means what you see
here is what the map will draw.

    python3 tools/render_tileset.py Petalburg Dewford
    python3 tools/render_tileset.py --primary General --scale 3

Metatiles are laid out 16 per row and labelled with their id in hex, matching
the numbering in include/constants/metatile_labels.h and Porymap.
"""
import argparse, os, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_hoenn as R

COLS = 16
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf'

def sheet(rend, prim, sec, S, gutter_font, title_font):
    """One tileset as an image. sec=None renders the primary's own metatiles."""
    name = sec or prim
    ts = rend.get(name)
    n = len(ts.meta) // 16
    base = 0 if sec is None else R.NUM_METATILES_IN_PRIMARY
    rows = (n + COLS - 1) // COLS
    cell = 16 * S
    gut = int(cell * 1.6)                 # left gutter for the id labels
    hdr = int(cell * 1.4)
    img = Image.new('RGB', (gut + COLS * cell, hdr + rows * cell), (16, 18, 24))
    d = ImageDraw.Draw(img)
    d.text((6, int(hdr * 0.22)), f'{name}   {n} metatiles   ids {base:03X}-{base+n-1:03X}',
           font=title_font, fill=(238, 242, 248))
    for i in range(n):
        r, c = divmod(i, COLS)
        # the primary is always General for outdoor maps; a secondary metatile
        # can reference primary tiles, so both have to be loaded to draw it
        m = rend.metatile(prim, sec, base + i)
        if S != 1:
            m = m.resize((cell, cell), Image.NEAREST)
        img.paste(m, (gut + c * cell, hdr + r * cell))
        if c == 0:
            d.text((6, hdr + r * cell + cell // 3), f'{base+i:03X}',
                   font=gutter_font, fill=(120, 132, 150))
    d2 = ImageDraw.Draw(img, 'RGBA')
    for r in range(rows + 1):
        y = hdr + r * cell
        d2.line([(gut, y), (img.size[0], y)], fill=(255, 255, 255, 28))
    for c in range(COLS + 1):
        x = gut + c * cell
        d2.line([(x, hdr), (x, img.size[1])], fill=(255, 255, 255, 28))
    return img

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('secondary', nargs='*',
                    help='secondary tileset names, without the gTileset_ prefix')
    ap.add_argument('--primary', default='General')
    ap.add_argument('--with-primary', action='store_true',
                    help='also render the primary tileset sheet')
    ap.add_argument('--scale', type=int, default=2, help='pixels per source pixel')
    ap.add_argument('-o', '--out', default='tilesets.png')
    a = ap.parse_args()
    S = a.scale
    gf = ImageFont.truetype(FONT % '', max(9, int(S * 5.5)))
    tf = ImageFont.truetype(FONT % '-Bold', max(12, int(S * 8)))

    rend = R.Renderer()
    prim = f'gTileset_{a.primary}'
    todo = ([None] if a.with_primary else []) + [f'gTileset_{s}' for s in a.secondary]
    sheets = [sheet(rend, prim, s, S, gf, tf) for s in todo]

    pad = 12 * S
    W = sum(s.size[0] for s in sheets) + pad * (len(sheets) + 1)
    H = max(s.size[1] for s in sheets) + pad * 2
    out = Image.new('RGB', (W, H), (10, 11, 15))
    x = pad
    for s in sheets:
        out.paste(s, (x, pad)); x += s.size[0] + pad
    out = out.convert('P', palette=Image.ADAPTIVE, colors=256)
    out.save(a.out, optimize=True)
    print(f'wrote {a.out} {out.size} ({os.path.getsize(a.out)/1e6:.1f} MB)')

if __name__ == '__main__':
    sys.exit(main())

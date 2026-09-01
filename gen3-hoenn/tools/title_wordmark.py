#!/usr/bin/env python3
"""Redraw the title screen's version banner as OPEN HOENN.

The banner is two 64x32 sprites side by side - VERSION_BANNER_LEFT_X 98 and
_RIGHT_X 162 in src/title_screen.c - so the art is exactly 128x32 and there is
no code to change as long as it stays that size. Everything else on the screen
is left alone: the POKeMON logo, Rayquaza, the clouds and Press Start are all
separate files and none of them is touched.

Ten characters on one line in 128 pixels means condensed letters, which is why
these are taller and narrower than EMERALD's. The style is measured off the
original rather than guessed: a 4-pixel stroke, a 2-pixel near-black outline,
a white face falling away to grey, and a shallow arch with the ends dropped.

The file keeps its name. gTitleScreenEmeraldVersionGfx points at it from
src/graphics.c and renaming it would mean touching that and the build rule for
no gain.

    python3 tools/title_wordmark.py           # write the PNG
    python3 tools/title_wordmark.py --check   # verify size, mode and palette
"""
import argparse, os, sys
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_hoenn as R

OUT = 'graphics/title_screen/emerald_version.png'
TEXT = 'OPEN HOENN'
W, H = 128, 32
STROKE = 4
CAP = 24                       # cap height, leaving room for the outline
WIDTHS = {'O': 12, 'P': 11, 'E': 10, 'N': 12, 'H': 12, ' ': 5}
TRACK = 1
ARCH = 3

# the palette the file already has: 0 is the transparent magenta, 4 the
# outline, and the rest a grey ramp. Keeping it means gbagfx converts this the
# same way it converted the original.
PAL = [(255, 74, 238), (156, 156, 156), (90, 90, 90), (222, 222, 222),
       (24, 16, 24), (74, 74, 74), (238, 238, 238), (41, 41, 41),
       (172, 172, 172), (106, 106, 106), (189, 189, 189), (139, 139, 139),
       (205, 205, 205), (123, 123, 123), (65, 57, 57), (255, 255, 255)]
OUTLINE_IDX = 4
# the greys, lightest first, for the face
FACE = [15, 6, 3, 12, 10, 8, 1, 11, 13, 9, 5, 2, 7]


def letter(ch, w, h):
    m = Image.new('L', (w, h), 0)
    d = ImageDraw.Draw(m)
    s, r = STROKE, STROKE // 2
    bar = lambda a, b, c, e: d.line([(a, b), (c, e)], fill=255, width=s, joint='curve')
    L, Rr, T, B, MY = r, w - r - 1, r, h - r - 1, h // 2
    if ch == 'O':
        d.ellipse([r - 1, 0, w - r, h - 1], outline=255, width=s)
    elif ch == 'H':
        bar(L, T, L, B); bar(Rr, T, Rr, B); bar(L, MY, Rr, MY)
    elif ch == 'E':
        bar(L, T, L, B); bar(L, T, Rr, T); bar(L, MY, Rr - 1, MY); bar(L, B, Rr, B)
    elif ch == 'N':
        bar(L, T, L, B); bar(Rr, T, Rr, B); bar(L, T - 1, Rr, B + 1)
    elif ch == 'P':
        bar(L, T, L, B); bar(L, T, Rr, T); bar(Rr, T, Rr, MY); bar(L, MY, Rr, MY)
    return m


def draw():
    # the 2-pixel outline grows the art on every side, so the letters have to
    # leave room for it or it is clipped against the sprite edge
    total = sum(WIDTHS[c] for c in TEXT) + TRACK * (len(TEXT) - 1)
    assert total + 8 <= W, f'{total} pixels of letters will not leave room for the outline'
    face = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    x = (W - total) // 2
    n = len(TEXT)
    top = (H - CAP - ARCH) // 2
    for i, ch in enumerate(TEXT):
        w = WIDTHS[ch]
        if ch != ' ':
            m = letter(ch, w, CAP)
            g = Image.new('RGBA', m.size)
            gd = ImageDraw.Draw(g)
            for yy in range(CAP):
                k = yy / (CAP - 1)
                c = int(255 - 118 * k * k * k)
                gd.line([(0, yy), (w, yy)], fill=(c, c, c, 255))
            cell = Image.new('RGBA', m.size, (0, 0, 0, 0))
            cell.paste(g, (0, 0), m)
            t = (i - (n - 1) / 2) / ((n - 1) / 2)
            face.alpha_composite(cell, (x, top + int(ARCH * t * t)))
        x += w + TRACK

    a = face.split()[3].point(lambda v: 255 if v > 90 else 0)
    ring = a.filter(ImageFilter.MaxFilter(5))

    out = Image.new('P', (W, H), 0)
    flatpal = []
    for c in PAL:
        flatpal += list(c)
    out.putpalette(flatpal + [0] * (768 - len(flatpal)))
    op, rp, ap, fp = out.load(), ring.load(), a.load(), face.load()
    for y in range(H):
        for x in range(W):
            if ap[x, y]:
                lum = fp[x, y][0]
                # nearest grey in the file's own ramp
                op[x, y] = min(FACE, key=lambda i: abs(PAL[i][0] - lum))
            elif rp[x, y]:
                op[x, y] = OUTLINE_IDX
    return out


def check():
    p = f'{R.ROOT}/{OUT}'
    im = Image.open(p)
    bad = []
    if im.size != (W, H):
        bad.append(f'{im.size} is not the {W}x{H} the two 64x32 sprites expect')
    if im.mode != 'P':
        bad.append(f'mode {im.mode}, must stay indexed')
    got = im.getpalette()[:48]
    for i, c in enumerate(PAL):
        if tuple(got[i * 3:i * 3 + 3]) != c:
            bad.append(f'palette {i} is {got[i*3:i*3+3]}, was {c}')
            break
    used = {v for v in im.get_flattened_data()}
    if 0 not in used:
        bad.append('nothing is transparent; index 0 is the banner background')
    if not bad:
        print(f'{OUT}: {im.size[0]}x{im.size[1]} indexed, original palette, '
              f'{len(used)} colours used')
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()
    if not a.check:
        draw().save(f'{R.ROOT}/{OUT}')
        print(f'wrote {OUT}')
    bad = check()
    if bad:
        sys.exit('\n'.join(bad))


if __name__ == '__main__':
    sys.exit(main())

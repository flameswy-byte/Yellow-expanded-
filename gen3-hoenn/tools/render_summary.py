#!/usr/bin/env python3
"""Draw the summary screen's skills page the way the GBA would.

There is no emulator here, so a UI change could only be checked by reading the
code and hoping. This draws the page instead, out of the same three things the
game draws it from: the page's tilemap, the tileset it indexes, and the Latin
font with its per-glyph width table. The geometry and the text metrics are
therefore the real ones - which is the whole point, because the question a
summary-screen change actually raises is "does it line up", and that is a
question about glyph widths.

What is *not* real is the colour: window text uses palette 6, which is loaded
from the page graphics at runtime, so the ink here is an approximation. Read
this for layout, not for hue.

    python3 tools/render_summary.py            # all three stat modes
    python3 tools/render_summary.py -o out.png
"""
import argparse, os, re, struct, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_hoenn as R

FONT = 'graphics/fonts/latin_normal.png'
TILES = 'graphics/summary_screen/tiles.png'
TILEMAP = 'graphics/summary_screen/page_skills.bin'


def charmap():
    """character -> glyph id, from the tree's own charmap.txt."""
    cm = {}
    for line in open(f'{R.ROOT}/charmap.txt'):
        m = re.match(r"^'(.)'\s*=\s*([0-9A-Fa-f]{2})\s*$", line)
        if m:
            cm[m.group(1)] = int(m.group(2), 16)
    cm.setdefault(' ', 0x00)
    return cm


def glyph_widths():
    src = open(f'{R.ROOT}/src/fonts.c').read()
    body = re.search(r'gFontNormalLatinGlyphWidths\[\] = \{(.*?)\};', src, re.S)
    return [int(x) for x in re.findall(r'\d+', body.group(1))]


class Font:
    """16x16 cells, sixteen to a row, advancing by the width table."""

    def __init__(self):
        self.sheet = Image.open(f'{R.ROOT}/{FONT}').convert('RGB')
        self.cm = charmap()
        self.w = glyph_widths()
        self.blank = self.sheet.getpixel((15, 0))

    def width(self, s):
        return sum(self.w[self.cm[c]] if c in self.cm and self.cm[c] < len(self.w)
                   else 6 for c in s)

    def draw(self, dst, s, x, y, fg=(74, 65, 57), sh=(255, 255, 255)):
        for ch in s:
            g = self.cm.get(ch)
            if g is None:
                x += 6
                continue
            cx, cy = (g % 16) * 16, (g // 16) * 16
            cell = self.sheet.crop((cx, cy, cx + 16, cy + 16)).load()
            for j in range(16):
                for i in range(16):
                    if cell[i, j] != self.blank and 0 <= x + i < dst.width \
                            and 0 <= y + j < dst.height:
                        dst.putpixel((x + i, y + j),
                                     fg if sum(cell[i, j]) < 380 else sh)
            x += self.w[g] if g < len(self.w) else 6
        return x


def background():
    tiles = Image.open(f'{R.ROOT}/{TILES}')
    tw = tiles.width // 8
    d = open(f'{R.ROOT}/{TILEMAP}', 'rb').read()
    tm = struct.unpack(f'<{len(d)//2}H', d)
    bg = Image.new('P', (256, 256))
    bg.putpalette(tiles.getpalette())
    for i, v in enumerate(tm[:32 * 32]):
        t = v & 0x3FF
        s = tiles.crop(((t % tw) * 8, (t // tw) * 8,
                        (t % tw) * 8 + 8, (t // tw) * 8 + 8))
        if (v >> 10) & 1:
            s = s.transpose(Image.FLIP_LEFT_RIGHT)
        if (v >> 11) & 1:
            s = s.transpose(Image.FLIP_TOP_BOTTOM)
        bg.paste(s, ((i % 32) * 8, (i // 32) * 8))
    return bg.convert('RGB').crop((0, 0, 240, 160))


# window origins in pixels, and how the stat labels are centred, taken from
# sPageSkillsTemplate and PrintPageNamesAndStats
LABELS = (('HP', 1, 10, 6, 42), ('ATTACK', 17, 10, 6, 42), ('DEFENSE', 33, 10, 6, 42),
          ('SP. ATK', 1, 22, 2, 36), ('SP. DEF', 17, 22, 2, 36), ('SPEED', 33, 22, 2, 36))
LEFT_X, RIGHT_X = 16 * 8, 27 * 8
LEFT_ALIGN, RIGHT_ALIGN = 44, 22      # what PrintStatColumn right-aligns to


def page(f, bg, title, left, right, aligned):
    im = bg.copy()
    f.draw(im, title, 2, 1)
    for t, yy, base, off, box in LABELS:
        f.draw(im, t, base * 8 + off + (box - f.width(t)) // 2, 7 * 8 + yy,
               fg=(90, 82, 74))
    for i, t in enumerate(left):
        x = LEFT_X + ((LEFT_ALIGN - f.width(t)) if aligned else 4)
        f.draw(im, t, x, 7 * 8 + 1 + i * 16)
    for i, t in enumerate(right):
        x = RIGHT_X + ((RIGHT_ALIGN - f.width(t)) if aligned else 2)
        f.draw(im, t, x, 7 * 8 + 1 + i * 16)
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-o', '--out', default='summary_modes.png')
    ap.add_argument('--scale', type=int, default=2)
    a = ap.parse_args()
    f, bg = Font(), background()
    ra = lambda s, n: ' ' * (n - len(s)) + s

    shots = [
        ('stats  (vanilla)', page(f, bg, 'POKeMON SKILLS',
                                  [ra('73', 3) + '/' + ra('73', 3), ra('45', 7), ra('45', 7)],
                                  [ra('34', 3), ra('38', 3), ra('31', 3)], False)),
        ('press A  ->  IVs', page(f, bg, 'SKILLS - IVs',
                                  ['A', 'D-', 'A+'], ['D+', 'D+', 'D-'], True)),
        ('press A  ->  EVs', page(f, bg, 'SKILLS - EVs',
                                  [ra('0', 7), ra('136', 7), ra('0', 7)],
                                  [ra('76', 3), ra('0', 3), ra('44', 3)], False)),
    ]
    s = a.scale
    out = Image.new('RGB', (240 * s + 16, (160 * s + 22) * len(shots) + 8), (24, 24, 24))
    for i, (cap, im) in enumerate(shots):
        y = 8 + i * (160 * s + 22)
        out.paste(im.resize((240 * s, 160 * s), Image.NEAREST), (8, y))
        f.draw(out, cap.upper(), 10, y + 160 * s + 4, fg=(230, 230, 230), sh=(60, 60, 60))
    out.save(a.out)
    print(f'wrote {a.out}')


if __name__ == '__main__':
    sys.exit(main())

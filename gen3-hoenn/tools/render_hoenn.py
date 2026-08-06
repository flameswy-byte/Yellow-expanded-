#!/usr/bin/env python3
"""Render the Hoenn overworld from the game's own tiles, with empty gaps marked.

Gen 3 map data is three layers deep:

  map.bin        u16 per metatile; bits 0-9 are the metatile id
  metatiles.bin  16 bytes per metatile = 8 u16 tile entries, 4 bottom layer
                 then 4 top layer, each 8x8. Bits 0-9 tile id, 10 flip-x,
                 11 flip-y, 12-15 palette number.
  tiles.png      indexed PNG, one 8x8 tile per cell, pixel value = palette index

Metatile ids below NUM_METATILES_IN_PRIMARY (512) come from the layout's
primary tileset, the rest from its secondary. Tile ids work the same way
against NUM_TILES_IN_PRIMARY (512). Palettes 0-5 come from the primary
tileset, 6-12 from the secondary. The top layer treats palette index 0 as
transparent, which is what puts trees in front of the ground behind them.

    python3 tools/render_hoenn.py --scale 8 -o hoenn.png
"""
import argparse, collections, glob, json, os, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.environ.get('POKEEMERALD', os.path.join(os.path.dirname(__file__), '..', 'pokeemerald'))
START = 'MAP_LITTLEROOT_TOWN'
NUM_METATILES_IN_PRIMARY = 512
NUM_TILES_IN_PRIMARY = 512
NUM_PALS_IN_PRIMARY = 6

def tileset_dir(name):
    stem = ''.join('_' + c.lower() if c.isupper() else c for c in name[len('gTileset_'):]).lstrip('_')
    for kind in ('primary', 'secondary'):
        p = f'{ROOT}/data/tilesets/{kind}/{stem}'
        if os.path.isdir(p):
            return p
    raise SystemExit(f'no tileset dir for {name} (tried {stem})')

class Tileset:
    def __init__(self, name):
        d = tileset_dir(name)
        self.dir = d
        im = Image.open(f'{d}/tiles.png')
        self.idx = im.convert('P') if im.mode != 'P' else im
        self.w = self.idx.size[0] // 8
        self.h = self.idx.size[1] // 8
        self.ntiles = self.w * self.h
        self.px = self.idx.load()
        self._tc = {}
        self.meta = open(f'{d}/metatiles.bin', 'rb').read()
        self.pals = {}
        for i in range(16):
            f = f'{d}/palettes/{i:02d}.pal'
            if os.path.exists(f):
                lines = open(f).read().split('\n')[3:]
                self.pals[i] = [tuple(int(v) for v in l.split()) for l in lines if l.strip()]

    def tile_pixels(self, tid):
        # a metatile can name a tile past the end of its tileset; those render
        # as nothing rather than crashing the whole map
        if tid >= self.ntiles:
            return None
        if tid in self._tc:
            return self._tc[tid]
        tx, ty = (tid % self.w) * 8, (tid // self.w) * 8
        rows = [[self.px[tx + x, ty + y] for x in range(8)] for y in range(8)]
        self._tc[tid] = rows
        return rows

class Renderer:
    def __init__(self):
        self.ts = {}
        self.cache = {}

    def get(self, name):
        if name not in self.ts:
            self.ts[name] = Tileset(name)
        return self.ts[name]

    def metatile(self, prim, sec, mid):
        key = (prim, sec, mid)
        if key in self.cache:
            return self.cache[key]
        P, S = self.get(prim), self.get(sec) if sec else None
        src, local = (P, mid) if mid < NUM_METATILES_IN_PRIMARY else (S, mid - NUM_METATILES_IN_PRIMARY)
        img = Image.new('RGB', (16, 16), (0, 0, 0))
        px = img.load()
        if src is None or (local + 1) * 16 > len(src.meta):
            self.cache[key] = img
            return img
        base = local * 16
        for i in range(8):
            e = src.meta[base + i*2] | (src.meta[base + i*2 + 1] << 8)
            tid, fx, fy, pal = e & 0x3FF, (e >> 10) & 1, (e >> 11) & 1, (e >> 12) & 0xF
            tsrc, tlocal = (P, tid) if tid < NUM_TILES_IN_PRIMARY else (S, tid - NUM_TILES_IN_PRIMARY)
            psrc = P if pal < NUM_PALS_IN_PRIMARY else (S or P)
            colors = psrc.pals.get(pal) or P.pals.get(pal) or [(0, 0, 0)] * 16
            if tsrc is None:
                continue
            rows = tsrc.tile_pixels(tlocal)
            if rows is None:
                continue
            ox, oy = (i % 2) * 8, ((i // 2) % 2) * 8
            top = i >= 4
            for y in range(8):
                for x in range(8):
                    v = rows[7 - y if fy else y][7 - x if fx else x]
                    if top and v == 0:
                        continue          # transparent over the layer beneath
                    px[ox + x, oy + y] = colors[v] if v < len(colors) else (0, 0, 0)
        self.cache[key] = img
        return img

def solve():
    lay = {l['id']: l for l in json.load(open(f'{ROOT}/data/layouts/layouts.json'))['layouts']
           if l and l.get('id')}
    maps = {}
    for f in glob.glob(f'{ROOT}/data/maps/*/map.json'):
        j = json.load(open(f))
        maps[j['id']] = {'layout': j.get('layout'), 'conn': j.get('connections') or []}
    pos, q = {START: (0, 0)}, [START]
    while q:
        cur = q.pop(0)
        cx, cy = pos[cur]
        L = lay[maps[cur]['layout']]
        for c in maps[cur]['conn']:
            nb, d, off = c.get('map'), c.get('direction'), c.get('offset', 0)
            if nb not in maps or d not in ('up', 'down', 'left', 'right') or nb in pos:
                continue
            N = lay[maps[nb]['layout']]
            pos[nb] = {'up': (cx + off, cy - N['height']), 'down': (cx + off, cy + L['height']),
                       'left': (cx - N['width'], cy + off), 'right': (cx + L['width'], cy + off)}[d]
            q.append(nb)
    return lay, maps, pos

def empty_regions(occ, W, H):
    seen, out = set(), []
    for sy in range(H):
        for sx in range(W):
            if (sx, sy) in occ or (sx, sy) in seen:
                continue
            comp, st, bd = {(sx, sy)}, [(sx, sy)], collections.Counter()
            seen.add((sx, sy))
            while st:
                x, y = st.pop()
                for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                    if not (0 <= nx < W and 0 <= ny < H):
                        continue
                    if (nx, ny) in occ:
                        bd[occ[(nx, ny)]] += 1
                    elif (nx, ny) not in seen:
                        seen.add((nx, ny)); comp.add((nx, ny)); st.append((nx, ny))
            out.append((len(comp), comp, bd))
    return sorted(out, key=lambda r: -r[0])

WATER = {f'ROUTE{n}' for n in range(124, 135)}
GAPS = [('GAP 1', 'lv 2-4', 'beside Littleroot, coastal'),
        ('GAP 2', 'lv 2-14', 'Petalburg / Rustboro / Mauville'),
        ('GAP 3', 'lv 6-18', 'Fallarbor / Lavaridge, volcanic'),
        ('GAP 4', 'lv 24-28', 'Fortree, rainforest'),
        ('GAP 5', 'lv 19-27', 'desert / rainforest seam')]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--scale', type=int, default=8, help='pixels per metatile (16 = native)')
    ap.add_argument('-o', '--out', default='hoenn_gaps_tiles.png')
    a = ap.parse_args()
    S = a.scale
    lay, maps, pos = solve()
    minx = min(x for x, _ in pos.values()); miny = min(y for _, y in pos.values())
    W = max(x + lay[maps[k]['layout']]['width'] for k, (x, y) in pos.items()) - minx
    H = max(y + lay[maps[k]['layout']]['height'] for k, (x, y) in pos.items()) - miny
    print(f'{len(pos)} maps, world {W}x{H} metatiles -> {W*S}x{H*S} px', file=sys.stderr)

    R = Renderer()
    HDR = S * 11                      # header band for title and legend
    canvas = Image.new('RGB', (W * S, H * S + HDR), (12, 14, 20))
    occ = {}
    for n, (k, (mx, my)) in enumerate(sorted(pos.items()), 1):
        L = lay[maps[k]['layout']]
        w, h = L['width'], L['height']
        blk = open(f'{ROOT}/{L["blockdata_filepath"]}', 'rb').read()
        prim, sec = L['primary_tileset'], L.get('secondary_tileset')
        tile = Image.new('RGB', (w * 16, h * 16))
        for j in range(h):
            for i in range(w):
                o = (j * w + i) * 2
                if o + 1 >= len(blk):
                    continue
                mid = (blk[o] | (blk[o+1] << 8)) & 0x3FF
                tile.paste(R.metatile(prim, sec, mid), (i * 16, j * 16))
                occ[(mx - minx + i, my - miny + j)] = k
        if S != 16:
            tile = tile.resize((w * S, h * S), Image.LANCZOS)
        canvas.paste(tile, ((mx - minx) * S, (my - miny) * S + HDR))
        print(f'  [{n}/{len(pos)}] {k}', file=sys.stderr)

    d = ImageDraw.Draw(canvas, 'RGBA')
    F = lambda n, b=False: ImageFont.truetype(
        f'/usr/share/fonts/truetype/dejavu/DejaVuSans{"-Bold" if b else ""}.ttf', n)
    regs = [r for r in empty_regions(occ, W, H) if r[0] >= 2000]
    inland = [r for r in regs if len({k.replace('MAP_', '') for k in r[2]} & WATER) < 2]
    RED, LW = (235, 55, 55), max(2, S // 3)
    for idx, (size, comp, bd) in enumerate(inland[:5]):
        for (x, y) in comp:
            px, py = x * S, y * S + HDR
            d.rectangle([px, py, px + S, py + S], fill=(235, 55, 55, 38))
        for (x, y) in comp:
            px, py = x * S, y * S + HDR
            for dx, dy, p0, p1 in ((1, 0, (px+S, py), (px+S, py+S)), (-1, 0, (px, py), (px, py+S)),
                                   (0, 1, (px, py+S), (px+S, py+S)), (0, -1, (px, py), (px+S, py))):
                if (x + dx, y + dy) not in comp:
                    d.line([p0, p1], fill=RED, width=LW)
        xs = [p[0] for p in comp]; ys = [p[1] for p in comp]
        cx = (min(xs) + max(xs)) // 2 * S
        cy = (min(ys) + max(ys)) // 2 * S + HDR
        name, lv, desc = GAPS[idx]
        big, small = F(int(S * 4.5), True), F(int(S * 2.2))
        line2 = f'{lv}  ·  {desc}'
        pad = S * 2
        tw = max(d.textlength(name, font=big), d.textlength(line2, font=small)) + pad * 2
        th = int(S * 8.5)
        d.rectangle([cx - tw/2, cy - th/2, cx + tw/2, cy + th/2],
                    fill=(10, 12, 18, 236), outline=RED, width=LW)
        d.text((cx - tw/2 + pad, cy - th/2 + S*0.7), name, font=big, fill=RED)
        d.text((cx - tw/2 + pad, cy + S*0.6), line2, font=small, fill=(250, 220, 220))
    T, ST = F(int(S * 5), True), F(int(S * 2.4))
    d.text((S * 2, int(S * 1.2)), 'OPEN HOENN  —  empty regions to populate', font=T,
           fill=(238, 242, 248))
    d.text((S * 2, int(S * 7)),
           f'vanilla Hoenn fills 40.0% of its {W}x{H} bounding box  ·  red = the five inland gaps, '
           f'the priority  ·  ~13 chunks of 64x64  ·  the ocean gets a few small islands later',
           font=ST, fill=(150, 162, 180))
    canvas = canvas.convert('P', palette=Image.ADAPTIVE, colors=256)
    canvas.save(a.out, optimize=True)
    print(f'wrote {a.out} ({os.path.getsize(a.out)/1e6:.1f} MB)', file=sys.stderr)

if __name__ == '__main__':
    sys.exit(main())

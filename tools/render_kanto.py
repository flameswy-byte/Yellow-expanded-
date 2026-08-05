#!/usr/bin/env python3
"""Render pokeyellow .blk maps to PNG, and stitch the Kanto overworld via connections."""
import re, os, sys, glob, json
from PIL import Image

ROOT = os.environ.get('POKEYELLOW', os.path.expanduser('~/pokeyellow'))

def load_tileset(name):
    im = Image.open(f'{ROOT}/gfx/tilesets/{name}.png').convert('L')
    w, h = im.size
    tiles = []
    for ty in range(h // 8):
        for tx in range(w // 8):
            tiles.append(im.crop((tx * 8, ty * 8, tx * 8 + 8, ty * 8 + 8)))
    return tiles

def load_blockset(name):
    data = open(f'{ROOT}/gfx/blocksets/{name}.bst', 'rb').read()
    return [data[i:i + 16] for i in range(0, len(data), 16)]

def render_map(blkfile, w, h, tiles, blocks):
    data = open(blkfile, 'rb').read()
    img = Image.new('L', (w * 32, h * 32), 255)
    for by in range(h):
        for bx in range(w):
            idx = by * w + bx
            if idx >= len(data):
                continue
            b = blocks[data[idx]] if data[idx] < len(blocks) else blocks[0]
            for i, t in enumerate(b):
                if t < len(tiles):
                    img.paste(tiles[t], (bx * 32 + (i % 4) * 8, by * 32 + (i // 4) * 8))
    return img

# --- parse map headers -------------------------------------------------------
def parse_headers():
    maps = {}
    for f in glob.glob(f'{ROOT}/data/maps/headers/*.asm'):
        txt = open(f).read()
        m = re.search(r'map_header (\w+),\s*(\w+),\s*(\w+),', txt)
        if not m:
            continue
        name, const, tileset = m.groups()
        conns = {}
        for d, cname, cconst, off in re.findall(
                r'connection (\w+),\s*(\w+),\s*(\w+),\s*(-?\d+)', txt):
            conns[d] = (cname, int(off))
        maps[name] = {'const': const, 'tileset': tileset, 'conn': conns}
    return maps

# Tilesets that make up the connected outdoor world. PLATEAU matters: Route 23 is
# 10x72 and Indigo Plateau sits above it, together occupying ~890 blocks west of
# Route 22. Filtering to OVERWORLD alone reports that land as empty, which is how
# a new map gets sited on top of it without anything complaining.
OUTDOOR = ('OVERWORLD', 'PLATEAU')

# --- map dimensions come from the .blk size + width in map_constants ---------
def parse_dims():
    txt = open(f'{ROOT}/constants/map_constants.asm').read()
    dims = {}
    for const, h, w in re.findall(r'map_const (\w+),\s*(\d+),\s*(\d+)', txt):
        dims[const] = (int(h), int(w))
    return dims

def layout(ow, dims):
    """BFS place overworld maps into a global block grid using connection offsets."""
    pos = {'PalletTown': (0, 0)}
    q = ['PalletTown']
    conflicts = []
    while q:
        cur = q.pop(0)
        cx, cy = pos[cur]
        cw, ch = dims[ow[cur]['const']]
        for d, (nb, off) in ow[cur]['conn'].items():
            if nb not in ow:
                continue
            nw, nh = dims[ow[nb]['const']]
            if   d == 'north': np_ = (cx + off, cy - nh)
            elif d == 'south': np_ = (cx + off, cy + ch)
            elif d == 'west':  np_ = (cx - nw, cy + off)
            elif d == 'east':  np_ = (cx + cw, cy + off)
            if nb in pos:
                if pos[nb] != np_:
                    conflicts.append((cur, d, nb, pos[nb], np_))
            else:
                pos[nb] = np_
                q.append(nb)
    return pos, conflicts

if __name__ == '__main__':
    if not os.path.isdir(ROOT):
        raise SystemExit(f'pokeyellow source not found at {ROOT}; set $POKEYELLOW')
    maps = parse_headers()
    dims = parse_dims()
    ow = {k: v for k, v in maps.items() if v['tileset'] in OUTDOOR}
    print(f'outdoor maps: {len(ow)}')
    for k in sorted(ow):
        d = dims.get(ow[k]['const'], ('?', '?'))
        print(f"  {k:24s} {d[0]}x{d[1]}  conns={list(ow[k]['conn'])}")

    pos, conflicts = layout(ow, dims)
    print(f'\nplaced {len(pos)}/{len(ow)} maps from PalletTown')
    unreached = sorted(set(ow) - set(pos))
    if unreached:
        print(f'unreachable via connections: {unreached}')

    # occupancy: any two maps covering the same block is a design collision, even
    # when the engine tolerates it (separate tilesets never share a connection)
    occ = {}
    overlaps = []
    for k, (x, y) in pos.items():
        w, h = dims[ow[k]['const']]
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                if (xx, yy) in occ:
                    overlaps.append((occ[(xx, yy)], k, xx, yy))
                occ[(xx, yy)] = k
    xs = [x for x, _ in occ]; ys = [y for _, y in occ]
    minx, miny = min(xs), min(ys)
    W, H = max(xs) - minx + 1, max(ys) - miny + 1
    print(f'bounding box {W}x{H}, {len(occ)} blocks used = {100*len(occ)/(W*H):.1f}%')
    if overlaps:
        seen = {}
        for a, b, xx, yy in overlaps:
            seen.setdefault(tuple(sorted((a, b))), []).append((xx, yy))
        print(f'\n{len(seen)} OVERLAPPING MAP PAIR(S):')
        for (a, b), cells in seen.items():
            print(f'  {a} / {b}: {len(cells)} blocks, e.g. {cells[0]}')

    if '--json' in sys.argv:
        out = {'minx': minx, 'miny': miny, 'W': W, 'H': H, 'pos': pos,
               'dims': {k: list(dims[ow[k]['const']]) for k in pos}}
        p = os.path.join(os.path.dirname(__file__), 'layout.json')
        json.dump(out, open(p, 'w'))
        print(f'wrote {p}')

    if conflicts:
        print(f'\n{len(conflicts)} CONFLICT(S) — a connection offset is wrong:')
        for cur, d, nb, had, want in conflicts:
            print(f'  {cur} {d} -> {nb}: placed at {had}, this edge wants {want}')
        raise SystemExit(1)
    print('no conflicts')

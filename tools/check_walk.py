#!/usr/bin/env python3
"""Walkability check for .blk maps, at the granularity the player actually moves.

Block-level checking is not good enough. A block is 4x4 tiles but the player
moves in 16px steps, so each block is 2x2 *step cells*, and a single block can
be walkable in its top half and solid in its bottom half — that is what a ledge
block is. Cities are full of such blocks, so treating a block as all-or-nothing
either invents walls or invents floors.

CONFIRMED: one map coordinate is two tiles. _GetTileAndCoordsInFrontOfPlayer
(engine/overworld/player_state.asm) puts the player on screen tile (8,9) and
reads (8,11) when facing down — a step is +2 tiles. So this grid is 2 cells per
block per axis, matching the space warp_event and object_event coordinates use.

NOT CONFIRMED: which tile of the 2x2 group a step cell samples. This uses row
2b+1, column 2a (bottom-left, where the feet land), which is consistent with
block $07 being a ledge — its bottom row is $37, listed hoppable-downward in
data/tilesets/ledge_tiles.asm. But it does not reproduce vanilla Celadon: the
Gym door comes out walled off from the Mart door, with or without allowing
ledge hops, and that is certainly wrong. Something about doors, warp tiles or
the sampling parity is still missing.

So: treat a NEGATIVE result from this tool as unproven, not as a defect. A
positive result on a map built only from uniformly-walkable and uniformly-solid
blocks (like the new maps here) is reliable, because the sampling rule cannot
matter when all four tiles of every block agree.

Ledge tiles are not in the passable set, so they read as walls.

    python3 tools/check_walk.py FuchsiaCity --components
    python3 tools/check_walk.py Route26 --from 10,0 --to 6,38
"""
import argparse, os, re, sys

ROOT = os.environ.get('POKEYELLOW', os.path.join(os.path.dirname(__file__), '..'))

def passable_tiles(tileset):
    txt = open(f'{ROOT}/data/tilesets/collision_tile_ids.asm').read()
    labels = []
    for line in txt.splitlines():
        lm = re.match(r'\s*(\w+)_Coll::', line)
        if lm:
            labels.append(lm.group(1)); continue
        cm = re.match(r'\s*coll_tiles\s+(.*)', line)
        if cm:
            if tileset.lower() in (l.lower() for l in labels):
                return {int(t.strip().lstrip('$'), 16) for t in cm.group(1).split(',')}
            labels = []
    raise SystemExit(f'no collision data for tileset {tileset}')

def step_grid(name, const, tileset):
    txt = open(f'{ROOT}/constants/map_constants.asm').read()
    m = re.search(rf'map_const {const},\s*(\d+),\s*(\d+)', txt)
    if not m:
        raise SystemExit(f'no map_const for {const}')
    w, h = int(m.group(1)), int(m.group(2))
    blk = open(f'{ROOT}/maps/{name}.blk', 'rb').read()
    if len(blk) != w * h:
        raise SystemExit(f'{name}.blk is {len(blk)} bytes; header says {w}x{h}={w*h}')
    bst = open(f'{ROOT}/gfx/blocksets/{tileset.lower()}.bst', 'rb').read()
    blocks = [bst[i:i + 16] for i in range(0, len(bst), 16)]
    coll = passable_tiles(tileset)
    W, H = w * 2, h * 2
    ok = [[False] * W for _ in range(H)]
    for Y in range(H):
        for X in range(W):
            b = blocks[blk[(Y // 2) * w + (X // 2)]]
            ok[Y][X] = b[4 * (2 * (Y % 2) + 1) + 2 * (X % 2)] in coll
    return ok, W, H

def components(ok, W, H):
    seen, comps = set(), []
    for sy in range(H):
        for sx in range(W):
            if ok[sy][sx] and (sx, sy) not in seen:
                comp = {(sx, sy)}; st = [(sx, sy)]; seen.add((sx, sy))
                while st:
                    x, y = st.pop()
                    for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                        if 0 <= nx < W and 0 <= ny < H and ok[ny][nx] and (nx, ny) not in seen:
                            seen.add((nx, ny)); comp.add((nx, ny)); st.append((nx, ny))
                comps.append(comp)
    return sorted(comps, key=len, reverse=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('name')
    ap.add_argument('--const')
    ap.add_argument('--tileset', default='Overworld')
    ap.add_argument('--from', dest='src', help='x,y step cell to start from')
    ap.add_argument('--to', nargs='*', default=[], help='x,y cells that must be reachable')
    ap.add_argument('--components', action='store_true', help='report connected components')
    a = ap.parse_args()
    const = a.const or re.sub(r'(?<!^)(?=[A-Z0-9])', '_', a.name).upper()
    ok, W, H = step_grid(a.name, const, a.tileset)
    total = sum(r.count(True) for r in ok)
    print(f'{a.name}: {W}x{H} step cells, {total} passable')

    comps = components(ok, W, H)
    if a.components:
        print(f'{len(comps)} connected component(s):')
        for c in comps[:6]:
            xs = [p[0] for p in c]; ys = [p[1] for p in c]
            print(f'  {len(c):5d} cells  x {min(xs)}..{max(xs)}  y {min(ys)}..{max(ys)}')
        if len(comps) > 6:
            print(f'  ... and {len(comps)-6} smaller')

    bad = 0
    if a.src:
        sx, sy = (int(v) for v in a.src.split(','))
        if not ok[sy][sx]:
            raise SystemExit(f'start ({sx},{sy}) is solid')
        reach = next(c for c in comps if (sx, sy) in c)
        print(f'from ({sx},{sy}): {len(reach)} cells reachable')
        for t in a.to:
            tx, ty = (int(v) for v in t.split(','))
            hit = (tx, ty) in reach
            why = '' if hit else (' (solid)' if not ok[ty][tx] else ' (walled off)')
            print(f'  ({tx},{ty}): {"REACHABLE" if hit else "UNREACHABLE"}{why}')
            bad += not hit
    return 1 if bad else 0

if __name__ == '__main__':
    sys.exit(main())

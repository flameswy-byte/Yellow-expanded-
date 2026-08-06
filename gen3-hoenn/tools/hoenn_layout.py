#!/usr/bin/env python3
"""Solve the Hoenn overworld layout from map connections and report empty space.

The Gen 1 equivalent of this treated a placement conflict as an error, because
Kanto must be a consistent planar partition — one neighbour per edge. Hoenn is
not. Vanilla ships three reciprocal pairs whose offsets disagree (Verdanturf /
Route 116, Fallarbor / Route 114, Dewford / Route 107), so the world cannot be
laid flat. The engine only ever resolves one transition at a time, so that is
legal. Conflicts are reported here as information, never as failure.

    python3 tools/hoenn_layout.py [--chunk 64] [--ascii]
"""
import argparse, collections, glob, json, os, sys

ROOT = os.environ.get('POKEEMERALD', os.path.join(os.path.dirname(__file__), '..', 'pokeemerald'))
START = 'MAP_LITTLEROOT_TOWN'

def load():
    lay = {l['id']: (l['width'], l['height'])
           for l in json.load(open(f'{ROOT}/data/layouts/layouts.json'))['layouts']
           if l and l.get('id')}
    maps = {}
    for f in glob.glob(f'{ROOT}/data/maps/*/map.json'):
        j = json.load(open(f))
        maps[j['id']] = {'layout': j.get('layout'), 'conn': j.get('connections') or []}
    return lay, maps

def solve(lay, maps):
    pos, q, conflicts = {START: (0, 0)}, [START], []
    while q:
        cur = q.pop(0)
        cx, cy = pos[cur]
        cw, ch = lay.get(maps[cur]['layout'], (0, 0))
        for c in maps[cur]['conn']:
            nb, d, off = c.get('map'), c.get('direction'), c.get('offset', 0)
            if nb not in maps or d not in ('up', 'down', 'left', 'right'):
                continue
            nw, nh = lay.get(maps[nb]['layout'], (0, 0))
            p = {'up': (cx + off, cy - nh), 'down': (cx + off, cy + ch),
                 'left': (cx - nw, cy + off), 'right': (cx + cw, cy + off)}[d]
            if nb in pos:
                if pos[nb] != p:
                    conflicts.append((cur, d, nb, pos[nb], p))
            else:
                pos[nb] = p
                q.append(nb)
    return pos, conflicts

def grid(lay, maps, pos):
    minx = min(x for x, _ in pos.values()); miny = min(y for _, y in pos.values())
    maxx = max(x + lay[maps[k]['layout']][0] for k, (x, y) in pos.items())
    maxy = max(y + lay[maps[k]['layout']][1] for k, (x, y) in pos.items())
    occ = {}
    for k, (x, y) in pos.items():
        w, h = lay[maps[k]['layout']]
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                occ[(xx - minx, yy - miny)] = k
    return occ, maxx - minx, maxy - miny

def regions(occ, W, H):
    seen, out = set(), []
    for sy in range(H):
        for sx in range(W):
            if (sx, sy) in occ or (sx, sy) in seen:
                continue
            comp, st, border = {(sx, sy)}, [(sx, sy)], collections.Counter()
            seen.add((sx, sy))
            while st:
                x, y = st.pop()
                for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                    if not (0 <= nx < W and 0 <= ny < H):
                        continue
                    if (nx, ny) in occ:
                        border[occ[(nx, ny)]] += 1
                    elif (nx, ny) not in seen:
                        seen.add((nx, ny)); comp.add((nx, ny)); st.append((nx, ny))
            out.append((len(comp), comp, border))
    return sorted(out, key=lambda r: -r[0])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--chunk', type=int, default=64)
    ap.add_argument('--ascii', action='store_true')
    a = ap.parse_args()
    lay, maps = load()
    pos, conflicts = solve(lay, maps)
    occ, W, H = grid(lay, maps, pos)
    print(f'{len(pos)} maps reachable by walking from {START.replace("MAP_","")}')
    print(f'world {W}x{H} = {W*H:,} metatiles; {len(occ):,} used = {100*len(occ)/(W*H):.1f}%')
    print(f'{len(conflicts)} inconsistent connection pair(s) — expected, see module docstring')
    C = a.chunk
    print(f'\nbuffer check for {C}x{C}: ({C}+15)*({C}+14) = {(C+15)*(C+14)} of 10240')
    for n, comp, border in regions(occ, W, H):
        if n < 1000:
            continue
        xs = [p[0] for p in comp]; ys = [p[1] for p in comp]
        nb = ', '.join(k.replace('MAP_', '') for k, _ in border.most_common(4))
        print(f'  {n:7,} metatiles  x{min(xs)}-{max(xs)} y{min(ys)}-{max(ys)}  '
              f'~{n/(C*C):4.1f} chunks   borders {nb}')
    print(f'\ntotal empty {W*H-len(occ):,} = {(W*H-len(occ))/(C*C):.0f} chunks of {C}x{C}')

if __name__ == '__main__':
    sys.exit(main())

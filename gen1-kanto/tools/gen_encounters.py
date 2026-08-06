#!/usr/bin/env python3
"""
Generate a starting wild-encounter table for a new overworld map by blending the
tables of the nearest vanilla maps, weighted by inverse centroid distance.

    python3 tools/gen_encounters.py NewRoute26 --x 40 --y -60 --w 22 --h 24

Writes valid data/wild/maps/<Name>.asm to stdout.

CAVEAT: Kanto's difficulty curve follows the player's path, not geography.
Route 22 borders the Victory Road region but is an early-game area. Always sanity
check generated levels against where the player actually arrives from.
"""
import argparse, json, os, re, sys
from collections import Counter

ROOT = os.path.join(os.path.dirname(__file__), '..')


def parse_enc(name):
    p = f'{ROOT}/data/wild/maps/{name}.asm'
    if not os.path.exists(p):
        return None
    t = open(p).read()
    g = re.search(r'def_grass_wildmons (\d+)(.*?)end_grass_wildmons', t, re.S)
    w = re.search(r'def_water_wildmons (\d+)(.*?)end_water_wildmons', t, re.S)
    slots = lambda m: [(int(a), b) for a, b in
                       re.findall(r'db\s+(\d+),\s*(\w+)', m.group(2))] if m else []
    return {'grate': int(g.group(1)) if g else 0, 'grass': slots(g),
            'wrate': int(w.group(1)) if w else 0, 'water': slots(w)}


def blend(neighbours, key, rate_key):
    """neighbours: list of (weight, table). Returns (rate, 10 slots)."""
    pool, lvl = Counter(), {}
    rate = 0.0
    wsum = sum(w for w, _ in neighbours) or 1
    neighbours = [(w / wsum, t) for w, t in neighbours]
    for wgt, t in neighbours:
        rate += wgt * t[rate_key]
        for level, sp in t[key]:
            pool[sp] += wgt
            lvl.setdefault(sp, []).append(level)
    if not pool:
        return 0, []
    slots = []
    total = sum(pool.values())
    for sp, wgt in pool.most_common():
        n = max(1, round(10 * wgt / total))
        levels = sorted(lvl[sp])
        for i in range(n):
            if len(slots) >= 10:
                break
            slots.append((levels[min(i * len(levels) // max(n, 1), len(levels) - 1)], sp))
    while len(slots) < 10:
        slots.append(slots[-1])
    return int(round(rate)), slots[:10]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('name')
    ap.add_argument('--x', type=int, required=True)
    ap.add_argument('--y', type=int, required=True)
    ap.add_argument('--w', type=int, default=22)
    ap.add_argument('--h', type=int, default=24)
    ap.add_argument('--k', type=int, default=3, help='how many neighbours to blend')
    ap.add_argument('--water', action='store_true', help='map contains water blocks')
    ap.add_argument('--layout', default=f'{ROOT}/tools/layout.json')
    a = ap.parse_args()

    L = json.load(open(a.layout))
    cx, cy = a.x + a.w / 2, a.y + a.h / 2

    cand = []
    for name, (mx, my) in L['pos'].items():
        mw, mh = L['dims'][name]
        t = parse_enc(name)
        if not t or t['grate'] == 0:
            continue
        d = ((mx + mw / 2 - cx) ** 2 + (my + mh / 2 - cy) ** 2) ** .5
        cand.append((d, name, t))
    cand.sort()
    near = cand[:a.k]
    if not near:
        sys.exit('no vanilla neighbours with encounters found')

    wts = [(1 / max(d, 1), t) for d, _, t in near]
    grate, grass = blend(wts, 'grass', 'grate')

    water_src = [(1 / max(d, 1), t) for d, _, t in cand if t['wrate'] > 0][:a.k]
    wrate, water = blend(water_src, 'water', 'wrate') if (a.water and water_src) else (0, [])

    print(f'; generated from {", ".join(n for _, n, _ in near)}', file=sys.stderr)
    out = [f'{a.name}WildMons:', f'\tdef_grass_wildmons {grate} ; encounter rate']
    out += [f'\tdb {l:2d}, {s}' for l, s in grass]
    out += ['\tend_grass_wildmons', '', f'\tdef_water_wildmons {wrate} ; encounter rate']
    out += [f'\tdb {l:2d}, {s}' for l, s in water]
    out += ['\tend_water_wildmons']
    print('\n'.join(out))


if __name__ == '__main__':
    main()

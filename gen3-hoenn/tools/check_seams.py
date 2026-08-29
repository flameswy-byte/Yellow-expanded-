#!/usr/bin/env python3
"""Check that every connection can actually be walked, and that the new land
is reachable from the start of the game.

A connection in the map header only says two maps are adjacent. Whether the
player can cross it depends on the blockdata: both sides of the shared edge
have to be passable at the same offset, and their elevations have to be
compatible. A connection with no crossable position is a wall that looks like
a door in the data, and nothing in the build catches it.

Then it flood fills the whole world - across connections, in world coordinates
- from the player's start position, and reports which maps come out reachable
on foot and which only by surfing. That is the question "is the new area
actually part of the game" reduced to something checkable.

    python3 tools/check_seams.py
    python3 tools/check_seams.py --only ROUTE135,ROUTE136,ROUTE137,ROUTE138
"""
import argparse, collections, glob, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_hoenn as R
import terrain as T

# elevation 0 means "inherit / any", 15 means multi-level: both cross freely
def elev_ok(a, b):
    return a == b or 0 in (a, b) or 15 in (a, b)

def load_world():
    """world cell -> (metatile id, collision, elevation, map)"""
    lay, maps, pos = R.solve()
    minx = min(x for x, _ in pos.values()); miny = min(y for _, y in pos.values())
    cell = {}
    for k, (mx, my) in pos.items():
        L = lay[maps[k]['layout']]
        w, h = L['width'], L['height']
        blk = open(f'{R.ROOT}/{L["blockdata_filepath"]}', 'rb').read()
        for j in range(h):
            for i in range(w):
                o = (j * w + i) * 2
                if o + 1 >= len(blk):
                    continue
                v = blk[o] | (blk[o+1] << 8)
                cell[(mx - minx + i, my - miny + j)] = (
                    v & 0x3FF, (v >> 10) & 3, (v >> 12) & 0xF, k)
    return lay, maps, pos, cell, minx, miny

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--only', help='comma separated map names to detail')
    ap.add_argument('--start', default='MAP_LITTLEROOT_TOWN')
    a = ap.parse_args()
    only = set(a.only.split(',')) if a.only else None

    lay, maps, pos, cell, minx, miny = load_world()
    rend = R.Renderer()
    # a metatile is water if its behavior says so - surf, not walk
    beh = {}
    for k in maps:
        if not maps[k].get('layout') or maps[k]['layout'] not in lay:
            continue
        L = lay[maps[k]['layout']]
        try:
            beh[k] = T.Classifier(rend, L['primary_tileset'], L.get('secondary_tileset'))
        except SystemExit:
            continue     # a few secret-base tilesets have no directory on disk

    def kind(p):
        mid, col, ele, k = cell[p]
        if col:
            return 'solid'
        return 'water' if beh[k](mid, col) == T.WATER else 'land'

    grid, warp_at, warp_dst = local_world(set(beh))

    # --- per-connection crossability -------------------------------------
    # Worked out from the connection's own offset in each map's local
    # coordinates, not from a world layout. Three vanilla connection pairs
    # disagree about their offsets (DESIGN.md sec 2), so a map's world
    # position depends on which way the solver reached it - and a seam check
    # built on that answers a different question in each direction.
    print('connections with no crossable position:')
    bad = 0
    for k in sorted(grid):
        g = grid[k]
        w, h = g['w'], g['h']
        for c in g['conn']:
            nb, d, off = c.get('map'), c.get('direction'), c.get('offset', 0)
            if nb not in grid or d not in ('up', 'down', 'left', 'right'):
                continue
            n = grid[nb]
            at = lambda m, x, y: grid[m]['cells'][y * grid[m]['w'] + x]
            def sort(m, x, y):
                mid, col, _ = at(m, x, y)
                return 'solid' if col else ('water' if beh[m](mid, col) == T.WATER
                                            else 'land')
            walk = surf = span = 0
            if d in ('up', 'down'):
                pairs = [((x, 0 if d == 'up' else h-1), (x - off, n['h']-1 if d == 'up' else 0))
                         for x in range(max(0, off), min(w, off + n['w']))]
            else:
                pairs = [((0 if d == 'left' else w-1, y), (n['w']-1 if d == 'left' else 0, y - off))
                         for y in range(max(0, off), min(h, off + n['h']))]
            for (ax, ay), (bx, by) in pairs:
                span += 1
                ka, kb = sort(k, ax, ay), sort(nb, bx, by)
                if ka == 'solid' or kb == 'solid':
                    continue
                if not elev_ok(at(k, ax, ay)[2], at(nb, bx, by)[2]):
                    continue
                if ka == 'land' and kb == 'land':
                    walk += 1
                else:
                    surf += 1
            tag = f'{k[4:]:18s} {d:5s} -> {nb[4:]:18s}'
            if walk == 0 and surf == 0:
                print(f'  BLOCKED  {tag}  ({span} cells of shared edge)')
                bad += 1
            elif only and (k[4:] in only or nb[4:] in only):
                print(f'  ok       {tag}  {walk} walkable, {surf} surfable of {span}')
    print(f'  -> {bad} blocked\n')

    # --- reachability -----------------------------------------------------
    # Not a world-coordinate flood fill: vanilla Hoenn's connection offsets
    # contradict each other (DESIGN.md sec 2), so laying it flat and flooding
    # the result answers the wrong question. This walks the connection graph
    # in each map's own local coordinates, the way the engine does, and
    # follows warps too - otherwise every tunnel and cave reads as a dead end.
    print()
    # only the outdoor maps are reported. Interiors hang off warps, and a warp
    # is reached by stepping onto its exact tile, which this does not always
    # manage - so an unreached interior says more about the model than the map.
    walk = None
    for mode in ('walk', 'walk+surf'):
        hit = reach(grid, warp_at, warp_dst, beh, a.start, mode)
        if mode == 'walk':
            walk = hit
        miss = sorted(k[4:] for k in pos if k not in hit)
        print(f'{mode:10s} reaches {len(hit & set(pos))}/{len(pos)} outdoor maps'
              + (f'   missing: {", ".join(miss)}' if miss else ''))
    for n in (only or ()):
        k = 'MAP_' + n
        if k in grid:
            print(f'  {n}: '
                  + ('walkable from the start' if k in walk else 'NOT reachable on foot'))


def local_world(keep):
    """map -> {'w','h','cells','conn'} in local coordinates, plus warp links."""
    lay, maps, pos = R.solve()
    grid, warp_at, warp_dst = {}, {}, {}
    hdrs = {}
    for f in glob.glob(f'{R.ROOT}/data/maps/*/map.json'):
        j = json.load(open(f))
        hdrs[j['id']] = j
    for k in keep:
        L = lay[maps[k]['layout']]
        w, h = L['width'], L['height']
        blk = open(f'{R.ROOT}/{L["blockdata_filepath"]}', 'rb').read()
        cells = []
        for i in range(w * h):
            o = i * 2
            v = blk[o] | (blk[o+1] << 8) if o + 1 < len(blk) else 0
            cells.append((v & 0x3FF, (v >> 10) & 3, (v >> 12) & 0xF))
        grid[k] = {'w': w, 'h': h, 'cells': cells, 'conn': maps[k]['conn'],
                   'lay': L}
        j = hdrs.get(k, {})
        for i, wp in enumerate(j.get('warp_events') or []):
            warp_at[(k, wp['x'], wp['y'])] = (wp['dest_map'], wp.get('dest_warp_id'))
        warp_dst[k] = j.get('warp_events') or []
    return grid, warp_at, warp_dst

def cross(grid, k, x, y):
    """a local coordinate outside map k -> (map, x, y) on the other side."""
    g = grid[k]; w, h = g['w'], g['h']
    d = ('left' if x < 0 else 'right' if x >= w else
         'up' if y < 0 else 'down' if y >= h else None)
    if d is None:
        return None
    for c in g['conn']:
        if c.get('direction') != d or c.get('map') not in grid:
            continue
        nb, off = c['map'], c.get('offset', 0)
        n = grid[nb]
        if d == 'left':   p = (x + n['w'], y - off)
        elif d == 'right':p = (x - w,      y - off)
        elif d == 'up':   p = (x - off,    y + n['h'])
        else:             p = (x - off,    y - h)
        if 0 <= p[0] < n['w'] and 0 <= p[1] < n['h']:
            return (nb, p[0], p[1])
    return None

# Lavaridge is expected to be missing from both figures. It is reached in
# vanilla through the Fiery Path and Jagged Pass, which are indoor maps, and
# this only follows warps between the outdoor ones - so the whole west half of
# Route 112 is behind a cave as far as it is concerned. Vanilla scores the same.
def reach(grid, warp_at, warp_dst, beh, start, mode):
    surf = mode != 'walk'
    def at(k, x, y):
        return grid[k]['cells'][y * grid[k]['w'] + x]
    def kind(k, x, y):
        mid, col, _ = at(k, x, y)
        if col:
            return 'solid'
        return 'water' if beh[k](mid, col) == T.WATER else 'land'
    def okcell(k, x, y):
        t = kind(k, x, y)
        return t == 'land' or (surf and t == 'water')

    seen, q = set(), collections.deque()
    g = grid[start]
    for y in range(g['h']):
        for x in range(g['w']):
            if okcell(start, x, y):
                seen.add((start, x, y)); q.append((start, x, y))
    while q:
        k, x, y = q.popleft()
        here = at(k, x, y)
        for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
            tgt = (k, nx, ny)
            if not (0 <= nx < grid[k]['w'] and 0 <= ny < grid[k]['h']):
                tgt = cross(grid, k, nx, ny)
                if tgt is None:
                    continue
            if tgt in seen or not okcell(*tgt):
                continue
            # elevation only gates land-to-land; the engine handles the
            # surf mount/dismount transition itself
            if kind(k, x, y) == 'land' and kind(*tgt) == 'land' \
                    and not elev_ok(here[2], at(*tgt)[2]):
                continue
            seen.add(tgt); q.append(tgt)
        w = warp_at.get((k, x, y))
        if w:
            dm, di = w
            lst = warp_dst.get(dm) or []
            if dm in grid and lst:
                wp = lst[min(int(di or 0), len(lst) - 1)]
                t = (dm, wp['x'], wp['y'])
                if t not in seen and 0 <= wp['x'] < grid[dm]['w'] and 0 <= wp['y'] < grid[dm]['h']:
                    seen.add(t); q.append(t)
    return {k for k, _, _ in seen}

if __name__ == '__main__':
    sys.exit(main())

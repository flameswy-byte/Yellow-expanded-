#!/usr/bin/env python3
"""Do the tiles either side of a map connection line up?

tools/check_adjacency.py asks whether the joins *inside* a map are ones vanilla
draws. This asks the same question across the join between two maps, which is
the one place nothing was checking - and which is where the first bug a player
found was hiding.

The failure it exists to catch: a vanilla map's edge row was drawn to sit
against that map's own border block, which the game tiles infinitely outside
the map. Littleroot's bottom row is a line of tree *tops*, metatiles 1CE and
1CF, and the trunks under them came from the border, 1DC and 1DD. Connecting a
new route below replaces the border with the route's first row - grass - and
the trunks vanish. A line of treetops is left floating over nothing, which is
exactly what it looks like.

Nothing in the map data is wrong in isolation. Both maps are individually fine
and every collision and elevation checks out; the bug lives only in the pair,
and only at the seam.

    python3 tools/check_seam_tiles.py
    python3 tools/check_seam_tiles.py --verbose   # every offending pair
    python3 tools/check_seam_tiles.py --fix       # repair the orphans

--fix only touches the cells this can prove are orphans, which is a much
smaller set than the cells that merely look odd at a seam. A cell is an orphan
when all three hold: it sits on a vanilla map's edge, the pair it used to make
with the border block is one vanilla draws, and the pair it now makes with the
map next door is not. That is the treetop exactly, and it is nothing else - a
cliff edge or a ledge that simply meets a route awkwardly fails the second
test, because vanilla never drew it against its own border either.

The repair is to copy the cell one step further in, which is what the map
itself says belongs there: Littleroot's second-to-last row is the grass the
town is standing on.
"""
import argparse, collections, os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_hoenn as R
import terrain as T
import check_adjacency as A


def raw_cells(L):
    """(width, height, the whole u16 per cell) - id, collision and elevation"""
    w, h = L['width'], L['height']
    blk = open(f'{R.ROOT}/{L["blockdata_filepath"]}', 'rb').read()
    return w, h, list(struct.unpack(f'<{w*h}H', blk[:w*h*2]))


def border_of(L):
    """the 2x2 block the game repeats outside the map, as ids.

    fieldmap.c indexes it ((x + 1) & 1) + (((y + 1) & 1) << 1) in grid
    coordinates, and the grid is the map shifted by MAP_OFFSET, which is odd
    on both axes - so in map coordinates that is (x & 1) + ((y & 1) << 1).
    """
    p = f'{R.ROOT}/{L["border_filepath"]}'
    if not os.path.exists(p):
        return None
    d = open(p, 'rb').read()
    b = [v & 0x3FF for v in struct.unpack(f'<{len(d)//2}H', d)]
    return b if len(b) >= 4 else None


def border_at(b, x, y):
    return b[(x & 1) + ((y & 1) << 1)]


def seams(maps, lay):
    """every ordered (map, direction, other map, offset) connection"""
    for k, m in sorted(maps.items()):
        for c in (m.get('conn') or []):
            if c['direction'] in ('up', 'down', 'left', 'right'):
                yield k, c['direction'], c['map'], c['offset']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--verbose', action='store_true')
    ap.add_argument('--fix', action='store_true')
    a = ap.parse_args()

    lay, maps, pos = R.solve()
    new = T.generated()
    van, vsec = A.vanilla_pairs(lay, maps, pos, new)
    P = R.NUM_METATILES_IN_PRIMARY

    def known(sec, ax, x, y):
        if x < P and y < P:
            return (x, y) in van[ax]
        return sec in vsec and (x, y) in vsec[sec][ax]

    # maps are already keyed by their MAP_ constant
    bad = collections.Counter()
    detail = collections.defaultdict(list)
    orphans = collections.defaultdict(list)     # layout name -> [(x, y, was)]
    checked = 0

    for k, d, other, off in seams(maps, lay):
        if other not in maps:
            continue
        ok = other
        A_ = lay[maps[k]['layout']]
        B_ = lay[maps[ok]['layout']]
        if A_['primary_tileset'] != 'gTileset_General':
            continue
        aw, ah, ac = raw_cells(A_)
        bw, bh, bc = raw_cells(B_)
        bord = border_of(A_)
        sec = A_.get('secondary_tileset')
        # only compare where both sides load the same secondary tileset,
        # otherwise a secondary id means two different pictures
        same_sec = sec == B_.get('secondary_tileset')

        # for a `down` connection: A's last row sits above B's first row,
        # with B's x = A's x - offset
        for i in range(max(aw, ah)):
            if d == 'down':
                if i >= aw:
                    break
                ax_, ay = i, ah - 1
                bx, by = i - off, 0
                axis = 1
            elif d == 'up':
                if i >= aw:
                    break
                ax_, ay = i, 0
                bx, by = i - off, bh - 1
                axis = 1
            elif d == 'right':
                if i >= ah:
                    break
                ax_, ay = aw - 1, i
                bx, by = 0, i - off
                axis = 0
            else:                                   # left
                if i >= ah:
                    break
                ax_, ay = 0, i
                bx, by = bw - 1, i - off
                axis = 0
            if not (0 <= bx < bw and 0 <= by < bh):
                continue
            u = ac[ay*aw + ax_] & 0x3FF
            v = bc[by*bw + bx] & 0x3FF
            # the pair is ordered top-to-bottom / left-to-right
            first, second = (u, v) if d in ('down', 'right') else (v, u)
            checked += 1
            if (first >= P or second >= P) and not same_sec:
                continue
            if known(sec, axis, first, second):
                continue
            bad[(k, d, other)] += 1
            detail[(k, d, other)].append((ax_, ay, first, second))

            # Was this cell drawn to sit against the border? Then it is an
            # orphan and the connection is what broke it. Only vanilla maps
            # can be orphaned this way: ours were drawn with a flat border and
            # never leaned on it for the other half of a picture.
            if k in new or bord is None:
                continue
            ox = ax_ if d in ('up', 'down') else (-1 if d == 'left' else aw)
            oy = ay if d in ('left', 'right') else (-1 if d == 'up' else ah)
            bt = border_at(bord, ox, oy)
            was = (u, bt) if d in ('down', 'right') else (bt, u)
            if not known(sec, axis, *was):
                continue
            # The cell one step back into the map is what belongs here - but
            # only take it if it actually mends the seam. A no-op copy, or one
            # that leaves the pair just as unknown, is not a repair, and
            # counting it would let --fix report work it did not do.
            ix = ax_ + (1 if d == 'left' else -1 if d == 'right' else 0)
            iy = ay + (1 if d == 'up' else -1 if d == 'down' else 0)
            if not (0 <= ix < aw and 0 <= iy < ah):
                continue
            now = ac[iy*aw + ix]
            n_id = now & 0x3FF
            if n_id == u:
                continue
            nf, ns = (n_id, v) if d in ('down', 'right') else (v, n_id)
            if (nf >= P or ns >= P) and not same_sec:
                continue
            # Take the copy if it mends the seam outright, or - failing that -
            # if it is a tile vanilla stacks against itself. A tile that tiles
            # with itself is ground, not half of a picture, so it cannot be
            # the wrong thing to stand a town on; any mismatch that survives is
            # then the neighbour's own edge, which is a different complaint and
            # is counted with the rest of them below.
            if known(sec, axis, nf, ns) or known(sec, axis, n_id, n_id):
                orphans[maps[k]['layout']].append(
                    (k, ax_, ay, ac[ay*aw + ax_], now))

    # A seam pair is a different population from a within-map pair: vanilla's
    # own seams are full of joins that appear nowhere inside a map, because
    # that is the only place they occur. So vanilla's seams are the control,
    # and only the amount by which ours are worse means anything.
    ctrl = {kk: n for kk, n in bad.items()
            if kk[0] not in new and kk[2] not in new}
    ours = {kk: n for kk, n in bad.items()
            if kk[0] in new or kk[2] in new}
    print(f'{checked} seam cell pairs checked across '
          f'{len(set((k, d) for k, d, _, _ in seams(maps, lay)))} connections')
    print(f'  vanilla against vanilla : {sum(ctrl.values()):5d} pairs over '
          f'{len(ctrl)} seams   <- the noise floor')
    print(f'  seams we created        : {sum(ours.values()):5d} pairs over '
          f'{len(ours)} seams')
    total = sum(len(v) for v in orphans.values())
    print(f'  of which orphaned border art : {total:5d} cells over '
          f'{len(orphans)} vanilla maps')

    if orphans:
        print()
        for lname in sorted(orphans):
            cells = orphans[lname]
            who = sorted({c[0] for c in cells})[0]
            print(f'  {who:26s} {len(cells):3d} cells: '
                  + ', '.join(f'({x},{y}) {was & 0x3FF:03X}->{now & 0x3FF:03X}'
                              for _, x, y, was, now in cells[:6])
                  + (' ...' if len(cells) > 6 else ''))
        if a.fix:
            for lname, cells in sorted(orphans.items()):
                L = lay[lname]
                w, h, raw = raw_cells(L)
                for _, x, y, _, now in cells:
                    # the picture only. Collision and elevation are what the
                    # rest of the pipeline checked its connections against, and
                    # a repair to how a cell looks has no business deciding
                    # whether the player can stand on it.
                    raw[y*w + x] = (raw[y*w + x] & 0xFC00) | (now & 0x3FF)
                p = f'{R.ROOT}/{L["blockdata_filepath"]}'
                open(p, 'wb').write(struct.pack(f'<{w*h}H', *raw))
            print(f'\nrewrote {total} cells across {len(orphans)} maps; '
                  're-run to confirm')
            return 0

    if not ours:
        print('\nnothing to fix')
        return 0
    print()
    for (k, d, other), n in sorted(ours.items(), key=lambda kv: -kv[1]):
        print(f'  {k:26s} {d:5s} -> {other:26s} {n:3d} cells')
        if a.verbose:
            for x, y, u, v in detail[(k, d, other)][:12]:
                print(f'        at ({x},{y})  {u:03X} against {v:03X}')
    return 1


if __name__ == '__main__':
    sys.exit(main())

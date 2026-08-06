#!/usr/bin/env python3
"""Build the new maps that fill a gap, and wire them into the game.

Everything a new Gen 3 map needs is here: blockdata painted from the sketch,
a border, a layout entry, a map header, a map group registration, a region map
section, an empty script file, and connections on both sides of every seam.

Terrain comes from two sources and neither is invented:

  * the neighbours. Every cell on a new map's boundary is seeded with the
    terrain class of the vanilla metatile immediately across that boundary, so
    a coastline arrives where the map abuts Route 105 and grass where it abuts
    Route 102. The interior is a nearest-seed fill between them.
  * the sketch. Area pens (water, grass, cliff, trees) join the seed set and
    so carve out regions; line pens (path) are stamped over the result at a
    fixed width, because a path is a line and not a region.

The metatile for each cell then comes from `terrain.py`, which learned vanilla's
own choices, so seams are vanilla seams.

    python3 tools/newmaps.py --dry-run      # report, touch nothing
    python3 tools/newmaps.py                # write it all
"""
import argparse, collections, json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_hoenn as R
import terrain as T

ROOT = R.ROOT
SKETCH = os.path.join(HERE, '..', 'sketches', 'sketch01.json')

# --- what to build --------------------------------------------------------
# Gap 1 partitions exactly into four rectangles: 6960 + 3200 + 3600 + 1600
# = 15,360, which is the gap's full cell count. World coords are the frame
# render_hoenn and the sketch tool both use.
GAP1 = [
    dict(name='Route135', const='MAP_ROUTE135', num=135, x=40,  y=262, w=80,  h=40,
         mapsec='MAPSEC_ROUTE_135', title='ROUTE 135', music='MUS_ROUTE101',
         desc='west coast, below Petalburg'),
    dict(name='Route136', const='MAP_ROUTE136', num=136, x=40,  y=302, w=40,  h=40,
         mapsec='MAPSEC_ROUTE_136', title='ROUTE 136', music='MUS_ROUTE101',
         desc='south-west corner, above Route 106'),
    dict(name='Route137', const='MAP_ROUTE137', num=137, x=80,  y=302, w=120, h=58,
         mapsec='MAPSEC_ROUTE_137', title='ROUTE 137', music='MUS_ROUTE110',
         desc='the south bay, below Littleroot'),
    dict(name='Route138', const='MAP_ROUTE138', num=138, x=140, y=242, w=60,  h=60,
         mapsec='MAPSEC_ROUTE_138', title='ROUTE 138', music='MUS_ROUTE110',
         desc='east of Oldale, toward Slateport'),
]

# Every seam the new maps take part in, including the ones into Littleroot,
# Oldale, Petalburg, Slateport and Route 101. Opening a town edge changes
# which coordinates the player can reach during that town's scripted
# sequences - the mistake that cost the most in the Kanto project - so each
# of those is re-guarded; see GUARDS below.
CONN = {
 'MAP_ROUTE135': [('left','MAP_ROUTE105',0), ('up','MAP_ROUTE102',30),
                  ('down','MAP_ROUTE136',0), ('down','MAP_ROUTE137',40),
                  ('right','MAP_LITTLEROOT_TOWN',20), ('right','MAP_ROUTE101',0),
                  ('up','MAP_PETALBURG_CITY',0)],
 'MAP_ROUTE136': [('up','MAP_ROUTE135',0), ('right','MAP_ROUTE137',0),
                  ('left','MAP_ROUTE105',-40), ('down','MAP_ROUTE106',-40)],
 'MAP_ROUTE137': [('up','MAP_ROUTE135',-40), ('up','MAP_ROUTE138',60),
                  ('left','MAP_ROUTE136',0), ('left','MAP_ROUTE106',40),
                  ('down','MAP_ROUTE107',0), ('down','MAP_ROUTE108',60),
                  ('right','MAP_ROUTE109',18),
                  ('up','MAP_LITTLEROOT_TOWN',40), ('right','MAP_SLATEPORT_CITY',-42)],
 'MAP_ROUTE138': [('up','MAP_ROUTE103',-20), ('down','MAP_ROUTE137',-60),
                  ('right','MAP_ROUTE110',-82),
                  ('left','MAP_LITTLEROOT_TOWN',40), ('left','MAP_OLDALE_TOWN',0),
                  ('left','MAP_ROUTE101',20), ('right','MAP_SLATEPORT_CITY',18)],
}
# the other half of each seam, added to the vanilla map's own header
RECIP = {
 'MAP_ROUTE105': [('right','MAP_ROUTE135',0), ('right','MAP_ROUTE136',40)],
 'MAP_ROUTE102': [('down','MAP_ROUTE135',-30)],
 'MAP_ROUTE106': [('up','MAP_ROUTE136',40), ('right','MAP_ROUTE137',-40)],
 'MAP_ROUTE107': [('up','MAP_ROUTE137',0)],
 'MAP_ROUTE108': [('up','MAP_ROUTE137',-60)],
 'MAP_ROUTE109': [('left','MAP_ROUTE137',-18)],
 'MAP_ROUTE103': [('down','MAP_ROUTE138',20)],
 'MAP_ROUTE110': [('left','MAP_ROUTE138',82)],
}

# --- the towns ------------------------------------------------------------
# Littleroot, Oldale, Petalburg and Slateport all border the new land, and
# opening a town edge changes which coordinates the player can reach during
# that town's scripted sequences. Every vanilla confinement was found first and
# is re-implemented at the new exits below; none of them needed terrain work,
# because Hoenn's town maps already draw walkable grass right up to their
# borders and were only closed by the absence of a connection.
TOWN_CONN = {
 'MAP_LITTLEROOT_TOWN': [('left', 'MAP_ROUTE135', -20), ('right', 'MAP_ROUTE138', -40),
                         ('down', 'MAP_ROUTE137', -40)],
 'MAP_OLDALE_TOWN':     [('right', 'MAP_ROUTE138', 0)],
 'MAP_ROUTE101':        [('left', 'MAP_ROUTE135', 0), ('right', 'MAP_ROUTE138', -20)],
 'MAP_PETALBURG_CITY':  [('down', 'MAP_ROUTE135', 0)],
 'MAP_SLATEPORT_CITY':  [('left', 'MAP_ROUTE138', -18), ('left', 'MAP_ROUTE137', 42)],
}

# What each newly opened exit has to keep the player from doing.
#
#   Littleroot  vanilla blocks the only exit (north) while
#               VAR_LITTLEROOT_TOWN_STATE is 0, by having a twin walk over and
#               warn you. The real hazard is leaving with an empty party and
#               stepping into tall grass, and that outlasts state 0 - at state
#               1 you have been told to go save Birch and still have nothing.
#               So the new exits test FLAG_SYS_POKEMON_GET instead of a state,
#               which is the condition that actually matters.
#   Oldale      the footprints man blocks the west exit while
#               VAR_OLDALE_TOWN_STATE is 0. The east exit gets the same gate on
#               the same var, so it opens at the same moment.
#   Route 101   during the Birch rescue (VAR_ROUTE101_STATE == 2) vanilla pens
#               the player into a box south of the bag, guarded on all four
#               sides. Its west wall is a trigger at x=6 covering rows 15-18
#               only - row 14 is walkable west all the way to x=0 and was a
#               dead end until now. Guarding the outermost column closes that.
#
# Petalburg and Slateport need nothing: reaching either already requires a
# party, and Slateport's west edge is open ocean, so that seam is a surf.
GUARD_NONE, GUARD_PARTY, GUARD_VAR = 'none', 'party', 'var'
GUARDS = {
 'MAP_LITTLEROOT_TOWN': dict(kind=GUARD_PARTY, sides=('left', 'right', 'down'),
                             text='I shouldn’t go wandering off without\\n'
                                  'a POKéMON of my own…'),
 'MAP_OLDALE_TOWN':     dict(kind=GUARD_VAR, sides=('right',),
                             var='VAR_OLDALE_TOWN_STATE', value='0',
                             text='The path east is roped off while the\\n'
                                  'footprint survey is going on.'),
 'MAP_ROUTE101':        dict(kind=GUARD_VAR, sides=('left', 'right'),
                             var='VAR_ROUTE101_STATE', value='2',
                             text=None),      # reuses Route101_Text_DontLeaveMe
}
STEP_BACK = {'left': 'walk_right', 'right': 'walk_left',
             'up': 'walk_down', 'down': 'walk_up'}
MARK = '@ --- open hoenn: gates generated by tools/newmaps.py ---'
MARK_END = '@ --- end open hoenn gates ---'

OPP = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}

# --- gaps 2-5 -------------------------------------------------------------
# Rectangles from tools/plan_gaps.py, which takes the largest buffer-legal
# rectangle out of each empty region until what is left is too small to be
# worth a map header. 10 maps covering 96% of the 37,420 remaining cells;
# the leftover slivers stay empty rather than becoming 300-cell maps.
REST = [
    ('Route139', 139, 40, 160, 123, 60, 'GAP 2', 'gTileset_Petalburg', 'MUS_ROUTE110'),
    ('Route140', 140, 163, 160, 37, 60, 'GAP 2', 'gTileset_Petalburg', 'MUS_ROUTE110'),
    ('Route141', 141, 40, 142, 80, 18, 'GAP 2', 'gTileset_Petalburg', 'MUS_ROUTE101'),
    ('Route142', 142, 70, 220, 50, 22, 'GAP 2', 'gTileset_Petalburg', 'MUS_ROUTE101'),
    ('Route143', 143, 40, 82, 160, 40, 'GAP 3', 'gTileset_Lavaridge', 'MUS_ROUTE110'),
    ('Route144', 144, 80, 20, 60, 62, 'GAP 3', 'gTileset_Lavaridge', 'MUS_ROUTE110'),
    ('Route145', 145, 140, 122, 60, 18, 'GAP 3', 'gTileset_Lavaridge', 'MUS_ROUTE113'),
    ('Route146', 146, 320, 20, 40, 120, 'GAP 4', 'gTileset_Fortree', 'MUS_ROUTE119'),
    ('Route147', 147, 360, 100, 60, 40, 'GAP 4', 'gTileset_Fortree', 'MUS_ROUTE119'),
    ('Route148', 148, 240, 0, 40, 140, 'GAP 5', 'gTileset_Mauville', 'MUS_ROUTE110'),
]
for _n, _num, _x, _y, _w, _h, _gap, _sec, _mus in REST:
    GAP1.append(dict(name=_n, const=f'MAP_{_n.upper()}', num=_num, x=_x, y=_y,
                     w=_w, h=_h, mapsec=f'MAPSEC_ROUTE_{_num}',
                     title=f'ROUTE {_num}', music=_mus, secondary=_sec,
                     desc=_gap))
NEWMAPS = GAP1

def origins():
    """world origin and size of every map, vanilla and new, in one frame."""
    lay, maps, pos = R.solve()
    minx = min(x for x, _ in pos.values()); miny = min(y for _, y in pos.values())
    box = {}
    for k, (x, y) in pos.items():
        L = lay[maps[k]['layout']]
        box[k] = (x - minx, y - miny, L['width'], L['height'])
    for s in NEWMAPS:                      # a rebuild may predate their headers
        box[s['const']] = (s['x'], s['y'], s['w'], s['h'])
    return box

def derive_connections():
    """every seam, read off the world grid instead of written out by hand.

    Offsets follow render_hoenn.solve(): along a vertical edge the offset is
    the neighbour's y minus mine, along a horizontal one its x minus mine. A
    neighbour is only accepted when it lines up exactly, which drops the few
    vanilla maps whose recorded offsets put them half a map out of place.
    """
    box = origins()
    owner = {}
    for k, (x, y, w, h) in box.items():
        for j in range(y, y + h):
            for i in range(x, x + w):
                owner[(i, j)] = k
    conn = collections.defaultdict(list)
    for s in NEWMAPS:
        me = s['const']
        x, y, w, h = box[me]
        edges = (('up',    [(x + i, y - 1) for i in range(w)]),
                 ('down',  [(x + i, y + h) for i in range(w)]),
                 ('left',  [(x - 1, y + j) for j in range(h)]),
                 ('right', [(x + w, y + j) for j in range(h)]))
        for side, cells in edges:
            for nb in dict.fromkeys(owner.get(c) for c in cells):
                if nb is None or nb == me:
                    continue
                nx, ny, nw, nh = box[nb]
                aligned = {'up': ny + nh == y, 'down': ny == y + h,
                           'left': nx + nw == x, 'right': nx == x + w}[side]
                if not aligned:
                    continue
                off = (nx - x) if side in ('up', 'down') else (ny - y)
                conn[me].append((side, nb, off))
                roff = (x - nx) if side in ('up', 'down') else (y - ny)
                conn[nb].append((OPP[side], me, roff))
    return conn

def map_dir(const):
    """MAP_LITTLEROOT_TOWN -> LittlerootTown, the name of its data directory."""
    return const.replace('MAP_', '').title().replace('_', '')

TREE_BORDER = [0x1D4, 0x1D5, 0x1DC, 0x1DD]      # what every land route uses
SEA_BORDER = [0x170] * 4

# --- terrain generation ---------------------------------------------------
def world_classes():
    """class of every occupied world cell in vanilla, plus the map it is on."""
    lay, maps, pos = R.solve()
    minx = min(x for x, _ in pos.values()); miny = min(y for _, y in pos.values())
    rend = R.Renderer()
    cls, owner = {}, {}
    for k, (mx, my) in pos.items():
        L = lay[maps[k]['layout']]
        w, h = L['width'], L['height']
        blk = open(f'{ROOT}/{L["blockdata_filepath"]}', 'rb').read()
        C = T.Classifier(rend, L['primary_tileset'], L.get('secondary_tileset'))
        for j in range(h):
            for i in range(w):
                o = (j * w + i) * 2
                if o + 1 >= len(blk):
                    continue
                v = blk[o] | (blk[o+1] << 8)
                p = (mx - minx + i, my - miny + j)
                cls[p] = C(v & 0x3FF, (v >> 10) & 3)
                owner[p] = k
    return cls, owner

# The sketch had no sand pen, so the wide "path" stroke drawn against Route
# 111's desert is an extension of the desert, not a road. Anything drawn with
# the path pen inside this world box is sand.
DESERT_BOX = (225, 0, 285, 145)

def sketch_seeds(spec):
    """area pens -> seeds that carve regions; the path pen -> lines to stamp."""
    if not os.path.exists(SKETCH):
        return {}, []
    sk = json.load(open(SKETCH))
    seeds, lines = {}, []
    for s in sk['strokes']:
        if s['pen'] == 'label':
            continue
        c = T.PEN_CLASS.get(s['pen'])
        if c is None:
            continue
        wx = [p[0] for p in s['points']]; wy = [p[1] for p in s['points']]
        x0, y0, x1, y1 = DESERT_BOX
        if s['pen'] == 'path' and x0 <= min(wx) and max(wx) <= x1 and max(wy) <= y1:
            c = T.SAND
        pts = [(int(x) - spec['x'], int(y) - spec['y']) for x, y in s['points']]
        pts = [p for p in pts if 0 <= p[0] < spec['w'] and 0 <= p[1] < spec['h']]
        if not pts:
            continue
        if c == T.PATH:
            lines.append(pts)
            continue
        for x, y in pts:
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    if 0 <= x+dx < spec['w'] and 0 <= y+dy < spec['h']:
                        seeds[(x+dx, y+dy)] = c
    return seeds, lines

def voronoi(seeds, w, h, default=T.GRASS):
    grid = [None] * (w * h)
    q = collections.deque()
    for (x, y), c in seeds.items():
        grid[y*w + x] = c
        q.append((x, y))
    if not q:
        return [default] * (w * h)
    while q:
        x, y = q.popleft()
        c = grid[y*w + x]
        for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
            if 0 <= nx < w and 0 <= ny < h and grid[ny*w + nx] is None:
                grid[ny*w + nx] = c
                q.append((nx, ny))
    return grid

def line_cells(x0, y0, x1, y1):
    """every cell on the segment, 4-connected, so a 1-wide path has no gaps."""
    dx, dy = abs(x1 - x0), abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err = dx - dy
    while True:
        yield x0, y0
        if x0 == x1 and y0 == y1:
            return
        e2 = err * 2
        if e2 > -dy:
            err -= dy
            x0 += sx
        elif e2 < dx:                  # step one axis at a time: no diagonal
            err += dx                  # jumps, so the path is 4-connected
            y0 += sy

def bfs_dist(sources, blocked, w, h):
    d = [None] * (w * h)
    q = collections.deque()
    for x, y in sources:
        d[y*w + x] = 0
        q.append((x, y))
    while q:
        x, y = q.popleft()
        for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
            if 0 <= nx < w and 0 <= ny < h and d[ny*w + nx] is None \
                    and not blocked[ny*w + nx]:
                d[ny*w + nx] = d[y*w + x] + 1
                q.append((nx, ny))
    return d

def build_classes(spec, wcls):
    w, h, ox, oy = spec['w'], spec['h'], spec['x'], spec['y']
    seed = spec['num'] * 1013

    # 1. seed the rim from whatever vanilla has on the other side of it, so a
    #    coastline arrives where the map abuts the sea and grass where it
    #    abuts a land route
    seeds, rim = {}, {}
    for i in range(w):
        for (lx, ly), (wx, wy) in (((i, 0), (ox+i, oy-1)), ((i, h-1), (ox+i, oy+h))):
            c = wcls.get((wx, wy))
            if c is not None:
                seeds[(lx, ly)] = rim[(lx, ly)] = T.GRASS if c == T.TREE else c
    for j in range(h):
        for (lx, ly), (wx, wy) in (((0, j), (ox-1, oy+j)), ((w-1, j), (ox+w, oy+j))):
            c = wcls.get((wx, wy))
            if c is not None:
                seeds[(lx, ly)] = rim[(lx, ly)] = T.GRASS if c == T.TREE else c
    sk_seeds, lines = sketch_seeds(spec)
    seeds.update(sk_seeds)                       # the sketch wins over the rim

    base = voronoi(seeds, w, h)

    # 2. domain warp. Sampling the region map through two noise fields bends
    #    every boundary into something meandering instead of the straight
    #    bisectors a nearest-seed fill produces. The amplitude tapers to zero
    #    at the rim so the seams still line up with the neighbours.
    AMP = 6.0
    grid = list(base)
    for y in range(h):
        for x in range(w):
            edge = min(x, y, w-1-x, h-1-y)
            if edge < 1:
                continue
            k = AMP * min(1.0, edge / 5.0)
            wx = x + k * (T.fbm(x, y, seed + 11, freq=0.035) - 0.5) * 2
            wy = y + k * (T.fbm(x, y, seed + 23, freq=0.035) - 0.5) * 2
            sx = min(w - 1, max(0, int(round(wx))))
            sy = min(h - 1, max(0, int(round(wy))))
            grid[y*w + x] = base[sy*w + sx]
    for (x, y), c in rim.items():                # the rim is not negotiable
        grid[y*w + x] = c

    # 3. paths, one cell wide. The sketch samples a stroke every few cells, so
    #    the points are joined with a line rather than dotted down - otherwise
    #    a single-width path comes out as a dashed one. A path is still a
    #    promise that the player can walk it, so nothing solid is left
    #    immediately beside one, but the cleared band is now a single cell
    #    either side instead of two.
    path = set()
    for pts in lines:
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            for x, y in line_cells(x0, y0, x1, y1):
                if 0 <= x < w and 0 <= y < h:
                    path.add((x, y))
        if pts:
            path.add(pts[-1])
    for x, y in path:
        grid[y*w + x] = T.PATH
    for x, y in list(path):
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                p = (x+dx, y+dy)
                if p in path or not (0 <= p[0] < w and 0 <= p[1] < h):
                    continue
                if grid[p[1]*w + p[0]] in (T.TREE, T.CLIFF):
                    grid[p[1]*w + p[0]] = T.GRASS

    # 4. vegetation. Distance is measured from where the player actually
    #    walks - the paths, and the walkable rim where a connection lands -
    #    and vegetate() lays grass and trees over the open ground at the
    #    proportions vanilla uses. It replaced a threshold-per-cell gradient
    #    that ran before it; leaving both in fragmented every grass patch,
    #    because the gradient had already scattered trees through the ground
    #    the patches were being chosen from.
    solid = [grid[i] in (T.WATER, T.CLIFF) for i in range(w * h)]
    walkable_rim = [(x, y) for (x, y), c in rim.items() if c in (T.GRASS, T.PATH, T.SAND)]
    # every path cell, not just the ones stamped from the sketch: the region
    # fill also spreads path inward from a rim seed where a vanilla neighbour
    # meets this map on a path, and measuring distance only from the stamped
    # ones let grass grow right up against those - which is where a third of
    # the one-cell grass fragments were coming from
    src = [(i % w, i // w) for i in range(w * h) if grid[i] == T.PATH] or walkable_rim
    if not src:
        src = [(w//2, h//2)]
    dist = bfs_dist(src, solid, w, h)
    vegetate(grid, dist, rim, w, h, seed)

    # 6. connectivity. Scattering trees can wall a pocket off, and a stranded
    #    pocket is worse than a plain one. Everything walkable is flooded, and
    #    any component of real size that is not part of the largest gets a
    #    one-cell corridor cut back to it through whatever is in the way.
    repair_connectivity(grid, w, h)
    return grid

# --- vegetation, targeted at vanilla's own proportions --------------------
# Measured by tools/study.py across the 21 vanilla land routes, as a share of
# each map's land rather than of the whole map - a route that is half sea is
# not short of grass, it just has less ground to put it on:
#
#                     vanilla median   what we had
#   tall grass              8.6%          22.0%
#   trees                  31.7%          17.7%
#   tall patches      6.2/map, median 13 cells    12.4/map, median 7, one of 2393
#
# So the old thresholds gave two and a half times too much tall grass, half
# the trees, and turned a couple of sketch strokes into a slab of grass no
# vanilla route comes close to. Rather than tune the thresholds again, the
# counts are now targeted directly: score every eligible cell, then take
# exactly as many as the target calls for. Density stops depending on how the
# noise happens to be distributed on that map.
TALL_TARGET = 0.09
TREE_TARGET = 0.32
VEG_KINDS = (T.GRASS, T.TALL, T.TREE, T.PATH, T.SAND)

def vegetate(grid, dist, rim, w, h, seed):
    land = [i for i in range(w * h) if grid[i] in VEG_KINDS]
    if not land:
        return
    def t_of(i):
        d = dist[i]
        return 0.0 if d is None else min(1.0, max(0.0, (d - 2) / 22.0))

    elig = [i for i in land
            if grid[i] in (T.GRASS, T.TALL)
            and (i % w, i // w) not in rim
            and dist[i] is not None and dist[i] > 1]

    # Tall grass first. Trees were being placed first, and because a third of
    # them are scattered singles they riddled every tall blob into two-cell
    # fragments - 33 patches a map where vanilla has 6. Choosing the grass
    # first and then keeping the trees out of it is what makes a patch a patch.
    #
    # One octave at a low frequency, so the top slice of the field is a handful
    # of broad blobs. Where the sketch asked for tall grass the score gets a
    # nudge, which keeps the patches in the region that was drawn without
    # letting it become solid. The nudge is deliberately small: at 0.30 it
    # dominated the field, and since the drawn region is speckled after the
    # domain warp, every blob came out cut to that speckle - 126 patches of a
    # single cell where the field on its own gives 6 patches of about 96.
    rest = [i for i in elig if dist[i] > 1]
    want_tall = int(TALL_TARGET * len(land))
    # every tall cell the region pass produced, not just the eligible ones:
    # clearing only the eligible set left the cells beside a path still tall,
    # and those were 273 of Route 139's fragments on their own
    drawn = {i for i in range(w * h)
             if grid[i] == T.TALL and (i % w, i // w) not in rim}
    for i in drawn:
        grid[i] = T.GRASS                            # rebuilt from scratch
    # The drawn mask is speckled after the domain warp, and a speckled bias
    # cuts every blob to its shape however small the bonus is. Two majority
    # passes close it into a region before it is used.
    for _ in range(2):
        nxt = set()
        for i in range(w * h):
            x, y = i % w, i // w
            n = sum(1 for dx in (-1, 0, 1) for dy in (-1, 0, 1)
                    if 0 <= x+dx < w and 0 <= y+dy < h
                    and (y+dy)*w + (x+dx) in drawn)
            if n >= 5:
                nxt.add(i)
        drawn = nxt

    tall_cells = set()
    if want_tall and rest:
        score = sorted(rest, key=lambda i: -(
            T.fbm(i % w, i // w, seed + 73, octaves=1, freq=0.055)
            + (0.10 if i in drawn else 0.0)))
        for i in score[:want_tall]:
            grid[i] = T.TALL
            tall_cells.add(i)

    # Trees: a low-frequency field gives the masses, a high-frequency one the
    # scattered singles, and the mix reproduces vanilla's shape - about 30
    # clumps a map with a median size of 2 but a few very large ones. Biased
    # away from the paths so the corridors stay open, and out of the grass.
    have_tree = sum(1 for i in land if grid[i] == T.TREE)
    want_tree = max(0, int(TREE_TARGET * len(land)) - have_tree)
    cand = [i for i in elig if dist[i] > 2 and i not in tall_cells]
    if want_tree and cand:
        score = sorted(cand, key=lambda i: -(
            0.55 * T.fbm(i % w, i // w, seed + 47, octaves=3, freq=0.05)
            + 0.45 * T.fbm(i % w, i // w, seed + 61, octaves=1, freq=0.45)
            + 0.25 * t_of(i)))
        for i in score[:want_tree]:
            grid[i] = T.TREE

# MB_JUMP_* - the ledges you hop down. Vanilla only ever draws them as long
# runs; the learned painter will happily emit a single one wherever a height
# change happened to look like the top of a ledge, and a lone ledge is visual
# litter and a one-way wall in the middle of a field.
# you hop east or west across a ledge that runs vertically, and north or
# south across one that runs horizontally
JUMP_MB = {0x38: 'v', 0x39: 'v', 0x3A: 'h', 0x3B: 'h',
           0x3C: 'c', 0x3D: 'c', 0x3E: 'c', 0x3F: 'c'}
MIN_LEDGE = 3

def tidy(blocks, w, h, spec):
    """Clean up what the per-cell painter cannot see: stray ledges and stray
    elevations. Both are invisible walls as far as the player is concerned."""
    beh = T.behaviors('gTileset_General')
    sec = spec.get('secondary')
    if sec:
        try:
            beh = beh + T.behaviors(sec)
        except SystemExit:
            pass
    mb = lambda v: beh[v & 0x3FF] if (v & 0x3FF) < len(beh) else 0
    fixed_l = fixed_e = 0

    # ledges shorter than MIN_LEDGE go back to whatever is around them
    for y in range(h):
        for x in range(w):
            i = y*w + x
            d = JUMP_MB.get(mb(blocks[i]))
            if not d:
                continue
            if d == 'c':                     # a corner only belongs next to
                run = 1 + sum(                # a ledge it is the corner of
                    1 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                    if 0 <= x+dx < w and 0 <= y+dy < h
                    and JUMP_MB.get(mb(blocks[(y+dy)*w + x+dx])))
                if run >= 2:
                    continue
                run = 1
            run, k = (run if d == 'c' else 1), 1
            step = (1, 0) if d == 'h' else (0, 1)
            for sgn in (1, -1):
                while True:
                    nx, ny = x + step[0]*k*sgn, y + step[1]*k*sgn
                    if not (0 <= nx < w and 0 <= ny < h):
                        break
                    if JUMP_MB.get(mb(blocks[ny*w + nx])) != d:
                        break
                    run += 1
                    k += 1
                k = 1
            if run >= MIN_LEDGE:
                continue
            nb = collections.Counter(
                blocks[(y+dy)*w + x+dx]
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                if 0 <= x+dx < w and 0 <= y+dy < h
                and not JUMP_MB.get(mb(blocks[(y+dy)*w + x+dx]))
                and ((blocks[(y+dy)*w + x+dx] >> 10) & 3) == 0)
            if nb:
                blocks[i] = nb.most_common(1)[0][0]
                fixed_l += 1

    # a walkable cell whose elevation disagrees with everything around it is
    # a step the player cannot take, for no reason the map shows
    for y in range(h):
        for x in range(w):
            i = y*w + x
            if (blocks[i] >> 10) & 3:
                continue
            e = (blocks[i] >> 12) & 0xF
            nb = collections.Counter(
                (blocks[(y+dy)*w + x+dx] >> 12) & 0xF
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                if 0 <= x+dx < w and 0 <= y+dy < h
                and not ((blocks[(y+dy)*w + x+dx] >> 10) & 3))
            if not nb or e in nb:
                continue
            best, n = nb.most_common(1)[0]
            if n >= 3:
                blocks[i] = (blocks[i] & ~0xF000) | (best << 12)
                fixed_e += 1
    return fixed_l, fixed_e

WALKABLE = (T.GRASS, T.TALL, T.PATH, T.SAND, T.OTHER)

def repair_connectivity(grid, w, h, min_pocket=12):
    def walk(i):
        return grid[i] in WALKABLE
    seen = [False] * (w * h)
    comps = []
    for start in range(w * h):
        if seen[start] or not walk(start):
            continue
        comp, q = [], collections.deque([start])
        seen[start] = True
        while q:
            i = q.popleft()
            comp.append(i)
            x, y = i % w, i // w
            for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                j = ny*w + nx
                if 0 <= nx < w and 0 <= ny < h and not seen[j] and walk(j):
                    seen[j] = True
                    q.append(j)
        comps.append(comp)
    if len(comps) < 2:
        return 0
    comps.sort(key=len, reverse=True)
    main = set(comps[0])
    cut = 0
    for comp in comps[1:]:
        if len(comp) < min_pocket:
            continue
        # 0-1 BFS out of the pocket: crossing a walkable cell is free, cutting
        # through a solid one costs 1, so it finds the thinnest wall
        INF = float('inf')
        cost = [INF] * (w * h)
        prev = [-1] * (w * h)
        q = collections.deque()
        for i in comp:
            cost[i] = 0
            q.append(i)
        hit = -1
        while q:
            i = q.popleft()
            if i in main:
                hit = i
                break
            x, y = i % w, i // w
            for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                if not (0 <= nx < w and 0 <= ny < h):
                    continue
                j = ny*w + nx
                # water is a moat, not a wall - cutting through it would make
                # a land bridge the sketch never asked for
                if grid[j] == T.WATER:
                    continue
                c = cost[i] + (0 if walk(j) else 1)
                if c < cost[j]:
                    cost[j] = c
                    prev[j] = i
                    (q.appendleft if c == cost[i] else q.append)(j)
        if hit < 0:
            continue
        i = hit
        while i != -1 and cost[i] > 0:
            if not walk(i):
                grid[i] = T.GRASS
                cut += 1
            i = prev[i]
        main |= set(comp)
    return cut

# --- softening the old map borders ---------------------------------------
# Every vanilla map ends in a hard line of trees or rock, because it used to
# end at nothing. Where one now faces new land that line is the seam showing,
# so it gets feathered: mostly cleared at the outermost row, mostly kept four
# rows in, with the cut driven by noise so what survives is clumps rather than
# a dashed line. A few trees are added back further in for the same reason.
# (map, edge, span) where span is the local range along that edge that faces
# new land - the rest of the edge still faces a vanilla map and is left alone
SOFTEN = [('MAP_ROUTE102', 'down',  None),
          ('MAP_ROUTE103', 'down',  (20, 79)),   # x120-139 faces Oldale
          ('MAP_ROUTE105', 'right', None),
          ('MAP_ROUTE106', 'up',    (40, 79)),   # x0-39 sits under Route 105
          ('MAP_ROUTE106', 'right', (0, 17)),    # y360+ faces Route 107
          ('MAP_ROUTE107', 'up',    None),
          ('MAP_ROUTE108', 'up',    None),
          ('MAP_ROUTE109', 'left',  (0, 39)),    # y360+ faces Route 108
          ('MAP_ROUTE110', 'left',  (82, 99)),   # only the bottom of a long map
          ('MAP_ROUTE101', 'left',  None),
          ('MAP_ROUTE101', 'right', None)]
DEPTH = 4

# Spans that must stay walled even though they now face new land.
# Route 111's desert is gated on the Go-Goggles by triggers inside the map
# (Route111_EventScript_ViciousSandstormTrigger). Opening its east cliff along
# the desert rows would be a second way in that walks straight past them.
NO_SOFTEN = {('MAP_ROUTE111', 'right'): (25, 70)}

def derive_soften(conn):
    """soften every vanilla edge that now faces new land, over the shared run.

    Towns are included but soften() only erodes trees there, never the solid
    cells: the classifier cannot tell a house wall from a cliff, and eroding
    one would open the side of a Pokemon Center."""
    box = origins()
    new = {s['const'] for s in NEWMAPS}
    out = []
    for k, cs in conn.items():
        if k in new:
            continue
        x, y, w, h = box[k]
        for side, nb, off in cs:
            if nb not in new:
                continue
            nx, ny, nw, nh = box[nb]
            if side in ('up', 'down'):
                lo, hi = max(0, nx - x), min(w, nx - x + nw) - 1
            else:
                lo, hi = max(0, ny - y), min(h, ny - y + nh) - 1
            block = NO_SOFTEN.get((k, side))
            if block:
                # trim the run back to whichever side of the blocked span is
                # longer, rather than dropping the seam entirely
                a, b = block
                left, right = (lo, min(hi, a - 1)), (max(lo, b + 1), hi)
                lo, hi = left if (left[1] - left[0]) > (right[1] - right[0]) else right
            if hi >= lo:
                out.append((k, side, (lo, hi)))
    return out

BASELINE = os.path.join(HERE, '..', 'baseline')

def pristine(name, L):
    """the map's blockdata as it was before any softening.

    Kept outside the vendored tree, and always read from rather than from the
    live file, so running the pass twice produces the same map instead of
    eroding the border a little further each time."""
    p = f'{ROOT}/{L["blockdata_filepath"]}'
    os.makedirs(BASELINE, exist_ok=True)
    orig = os.path.join(BASELINE, f'{name}.bin')
    if not os.path.exists(orig):
        shutil.copyfile(p, orig)
    return open(orig, 'rb').read(), p

def event_cells(name):
    p = f'{ROOT}/data/maps/{name}/map.json'
    if not os.path.exists(p):
        return set()
    j = json.load(open(p))
    out = set()
    for key in ('object_events', 'warp_events', 'coord_events', 'bg_events'):
        for e in j.get(key) or []:
            try:
                x, y = int(e['x']), int(e['y'])
            except (KeyError, ValueError, TypeError):
                continue
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    out.add((x+dx, y+dy))
    return out

def soften(painter, dry):
    """Feather every vanilla edge that now faces new land.

    All of one map's edges are done in a single pass. Each pass starts from
    the pristine baseline, so softening the same map twice - which happens as
    soon as one edge faces two new maps - would otherwise have the second run
    throw away the first one's work.
    """
    lay, maps, _ = R.solve()
    rend = R.Renderer()
    by_map = collections.defaultdict(list)
    for const, side, span in SOFTEN:
        by_map[const].append((side, span))
    total = 0
    for const, edges in sorted(by_map.items()):
        L = lay[maps[const]['layout']]
        w, h = L['width'], L['height']
        name = map_dir(const)
        town = const.endswith('_TOWN') or const.endswith('_CITY')
        blk, path = pristine(name, L)
        C = T.Classifier(rend, L['primary_tileset'], L.get('secondary_tileset'))
        raw = [(blk[i*2] | (blk[i*2+1] << 8)) if i*2+1 < len(blk) else 0
               for i in range(w * h)]
        cls = [C(v & 0x3FF, (v >> 10) & 3) for v in raw]
        before = list(cls)
        skip = event_cells(name)
        seed = sum(ord(c) for c in const) * 31

        def depth_at(x, y):
            """shallowest depth over the edges being softened, or None."""
            best = None
            for side, span in edges:
                dep = {'up': y, 'down': h-1-y, 'left': x, 'right': w-1-x}[side]
                if dep >= DEPTH:
                    continue
                if span is not None:
                    a = x if side in ('up', 'down') else y
                    if not (span[0] <= a <= span[1]):
                        continue
                best = dep if best is None else min(best, dep)
            return best

        for y in range(h):
            for x in range(w):
                dep = depth_at(x, y)
                if dep is None or (x, y) in skip:
                    continue
                i = y*w + x
                if town and (raw[i] & 0x3FF) >= R.NUM_METATILES_IN_PRIMARY:
                    continue                    # town furniture, leave it
                n = T.fbm(x, y, seed, octaves=3, freq=0.11)
                # In a town only trees come out. The classifier calls any solid
                # non-green metatile a cliff, and in a town that is a building -
                # eroding one would open the side of a Pokemon Center.
                erodible = (T.TREE,) if town else (T.TREE, T.CLIFF)
                if cls[i] in erodible:
                    # the outermost row survives only where the noise is high,
                    # the deepest row almost everywhere - which feathers the
                    # line instead of moving it inward by four cells
                    if n > 0.75 - 0.55 * (dep / DEPTH):
                        continue
                    nb = collections.Counter(
                        before[(y+dy)*w + (x+dx)]
                        for dy in (-1, 0, 1) for dx in (-1, 0, 1)
                        if 0 <= x+dx < w and 0 <= y+dy < h
                        and before[(y+dy)*w + (x+dx)] not in (T.TREE, T.CLIFF, T.OTHER))
                    cls[i] = nb.most_common(1)[0][0] if nb else T.GRASS
                elif not town and cls[i] == T.GRASS and dep >= 2 and n > 0.80:
                    cls[i] = T.TREE             # rounded clumps, not a straight hem

        # repaint only where the 3x3 class neighbourhood actually moved, so
        # vanilla's hand-placed detail survives everywhere else
        out = list(raw)
        changed = 0
        for y in range(h):
            for x in range(w):
                if (x, y) in skip:
                    continue
                if depth_at(x, y) is None and not any(
                        depth_at(x+dx, y+dy) is not None
                        for dx in (-1, 0, 1) for dy in (-1, 0, 1)
                        if 0 <= x+dx < w and 0 <= y+dy < h):
                    continue
                if T.mask3(cls, x, y, w, h, T.GRASS) == T.mask3(before, x, y, w, h, T.GRASS):
                    continue
                if town and (raw[y*w + x] & 0x3FF) >= R.NUM_METATILES_IN_PRIMARY:
                    continue
                m3 = T.mask3(cls, x, y, w, h, T.GRASS)
                v = (T.best(painter.m['t3'], m3)
                     or T.best(painter.m['t4'], T.mask4(m3))
                     or T.best(painter.m['t1'], cls[y*w + x]))
                if v is not None and v != out[y*w + x]:
                    out[y*w + x] = v
                    changed += 1
        sides = ', '.join(sorted({s for s, _ in edges}))
        print(f'  soften {name:16s} {sides:22s} {changed} metatiles')
        total += changed
        if not dry:
            open(path, 'wb').write(u16(out))
    print(f'  -> {total} vanilla metatiles rewritten across {len(by_map)} maps')

def crossable(box, built):
    """which derived connections the player can actually cross.

    A connection with no crossable cell is a wall that looks like a door, and
    nothing in the build catches it - so rather than ship one, the seam is
    dropped. Run after the terrain is final, on the blockdata as written.
    """
    lay, maps, _ = R.solve()
    rend = R.Renderer()
    cache = {}

    def cells(const):
        if const in cache:
            return cache[const]
        L = lay[maps[const]['layout']]
        w, h = L['width'], L['height']
        if const in built:
            raw = built[const]
        else:
            blk = open(f'{ROOT}/{L["blockdata_filepath"]}', 'rb').read()
            raw = [(blk[i*2] | (blk[i*2+1] << 8)) if i*2+1 < len(blk) else 0
                   for i in range(w * h)]
        C = T.Classifier(rend, L['primary_tileset'], L.get('secondary_tileset'))
        cache[const] = (raw, w, h, C)
        return cache[const]

    def open_at(const, x, y):
        raw, w, h, C = cells(const)
        v = raw[y*w + x]
        return ((v >> 10) & 3) == 0, (v >> 12) & 0xF

    def ok(me, side, nb, off):
        _, w, h, _ = cells(me)
        _, nw, nh, _ = cells(nb)
        if side in ('up', 'down'):
            pairs = [((x, 0 if side == 'up' else h-1),
                      (x - off, nh-1 if side == 'up' else 0))
                     for x in range(max(0, off), min(w, off + nw))]
        else:
            pairs = [((0 if side == 'left' else w-1, y),
                      (nw-1 if side == 'left' else 0, y - off))
                     for y in range(max(0, off), min(h, off + nh))]
        for (ax, ay), (bx, by) in pairs:
            oa, ea = open_at(me, ax, ay)
            ob, eb = open_at(nb, bx, by)
            if oa and ob and (ea == eb or 0 in (ea, eb) or 15 in (ea, eb)):
                return True
        return False
    return ok

# --- gates on the town edges ----------------------------------------------
def edge_cells(L, side):
    """the outermost cells of one edge that the player can stand on."""
    w, h = L['width'], L['height']
    blk = open(f'{ROOT}/{L["blockdata_filepath"]}', 'rb').read()
    out = []
    span = range(w) if side in ('up', 'down') else range(h)
    for a in span:
        x, y = ((a, 0) if side == 'up' else (a, h-1) if side == 'down' else
                (0, a) if side == 'left' else (w-1, a))
        o = (y * w + x) * 2
        if o + 1 < len(blk) and ((blk[o] | (blk[o+1] << 8)) >> 10) & 3 == 0:
            out.append((x, y))
    return out

def guard_script(name, g, side):
    """the block appended to a map's scripts.inc for one gated edge."""
    S, cap = [], side.capitalize()
    lbl = f'{name}_EventScript_OpenHoennGate{cap}'
    txt = (f'{name}_Text_OpenHoennGate' if g['text'] is not None
           else 'Route101_Text_DontLeaveMe')
    S.append(f'{lbl}::')
    if g['kind'] == GUARD_PARTY:
        # the coord event fires on every step onto the tile, so the real test
        # lives here and falls straight through once the player has a party
        S.append(f'\tgoto_if_set FLAG_SYS_POKEMON_GET, {name}_EventScript_OpenHoennGateOpen')
    S += ['\tlockall',
          f'\tmsgbox {txt}, MSGBOX_DEFAULT',
          '\tclosemessage',
          f'\tapplymovement LOCALID_PLAYER, {name}_Movement_OpenHoennBack{cap}',
          '\twaitmovement 0',
          '\treleaseall',
          '\tend',
          '',
          f'{name}_Movement_OpenHoennBack{cap}:',
          f'\t{STEP_BACK[side]}',
          '\tstep_end',
          '']
    return S

def gates(dry):
    lay, maps, _ = R.solve()
    for const, g in GUARDS.items():
        name = map_dir(const)
        L = lay[maps[const]['layout']]
        sp = f'{ROOT}/data/maps/{name}/scripts.inc'
        mp = f'{ROOT}/data/maps/{name}/map.json'

        body = []
        if g['kind'] == GUARD_PARTY:
            body += [f'{name}_EventScript_OpenHoennGateOpen::', '\tend', '']
        events = []
        for side in g['sides']:
            body += guard_script(name, g, side)
            for x, y in edge_cells(L, side):
                events.append({
                    'type': 'trigger', 'x': x, 'y': y, 'elevation': 0,
                    'var': 'VAR_TEMP_2' if g['kind'] == GUARD_PARTY else g['var'],
                    'var_value': '0' if g['kind'] == GUARD_PARTY else g['value'],
                    'script': f'{name}_EventScript_OpenHoennGate{side.capitalize()}'})
        if g['text'] is not None:
            body += [f'{name}_Text_OpenHoennGate:',
                     f'\t.string "{g["text"]}$"', '']

        # rewrite the generated block in place rather than appending again
        src = open(sp).read()
        if MARK in src:
            src = src[:src.index(MARK)] + src[src.index(MARK_END) + len(MARK_END):]
        src = src.rstrip('\n') + '\n\n' + MARK + '\n' + '\n'.join(body) + MARK_END + '\n'

        d = json.load(open(mp))
        keep = [e for e in (d.get('coord_events') or [])
                if 'OpenHoennGate' not in str(e.get('script'))]
        d['coord_events'] = keep + events
        print(f'  gate {name:16s} {len(events)} triggers on {", ".join(g["sides"])}'
              f'   ({g["kind"]})')
        if not dry:
            open(sp, 'w').write(src)
            json.dump(d, open(mp, 'w'), indent=2)

# --- writing --------------------------------------------------------------
def u16(vals):
    b = bytearray()
    for v in vals:
        b += bytes((v & 0xFF, (v >> 8) & 0xFF))
    return bytes(b)

def write_map(spec, blocks, dry):
    ld = f'{ROOT}/data/layouts/{spec["name"]}'
    md = f'{ROOT}/data/maps/{spec["name"]}'
    water = sum(1 for v in blocks if (v & 0x3FF) == 0x170) > len(blocks) * 0.5
    if dry:
        return
    os.makedirs(ld, exist_ok=True); os.makedirs(md, exist_ok=True)
    open(f'{ld}/map.bin', 'wb').write(u16(blocks))
    open(f'{ld}/border.bin', 'wb').write(u16(SEA_BORDER if water else TREE_BORDER))
    open(f'{md}/scripts.inc', 'w').write(f'{spec["name"]}_MapScripts::\n\t.byte 0\n')

def write_header(spec, dry):
    if dry:
        return
    md = f'{ROOT}/data/maps/{spec["name"]}'
    os.makedirs(md, exist_ok=True)
    hdr = {
        'id': spec['const'], 'name': spec['name'],
        'layout': f'LAYOUT_{spec["name"].upper()}', 'music': spec['music'],
        'region_map_section': spec['mapsec'], 'requires_flash': False,
        'weather': 'WEATHER_SUNNY', 'map_type': 'MAP_TYPE_ROUTE',
        'allow_cycling': True, 'allow_escaping': False, 'allow_running': True,
        'show_map_name': True, 'battle_scene': 'MAP_BATTLE_SCENE_NORMAL',
        'connections': [{'map': m, 'offset': o, 'direction': d}
                        for d, m, o in sorted(set(CONN[spec['const']]))],
        'object_events': [], 'warp_events': [], 'coord_events': [], 'bg_events': [],
    }
    json.dump(hdr, open(f'{md}/map.json', 'w'), indent=2)

def patch_json(path, fn, dry):
    d = json.load(open(path))
    fn(d)
    if not dry:
        json.dump(d, open(path, 'w'), indent=2)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    dry = a.dry_run

    # record what we generate before the model is loaded: terrain.py must not
    # learn from our own maps
    if not dry:
        with open(T.GENERATED, 'w') as f:
            f.write('\n'.join(s['const'] for s in NEWMAPS) + '\n')
    model = T.load()
    painter = T.Painter(model)

    # soften first: the new maps seed their rim from the neighbours, so the
    # neighbours have to be final before the rim is read
    global CONN, SOFTEN
    derived = derive_connections()
    CONN = derived
    SOFTEN = SOFTEN + derive_soften(derived)

    print('softening the old map borders...')
    soften(painter, dry)

    print('classifying vanilla terrain...')
    wcls, _ = world_classes()

    built = {}
    for spec in NEWMAPS:
        cls = build_classes(spec, wcls)
        blocks = painter.paint(cls, spec['w'], spec['h'])
        nl, ne = tidy(blocks, spec['w'], spec['h'], spec)
        built[spec['const']] = blocks
        n = collections.Counter(cls)
        mix = ', '.join(f'{100*v//len(cls)}% {T.CLASS_NAME[k]}'
                        for k, v in n.most_common() if 100*v//len(cls))
        print(f'  {spec["name"]}  {spec["w"]}x{spec["h"]}  '
              f'buffer {(spec["w"]+15)*(spec["h"]+14)}/10240   {mix}')
        if nl or ne:
            print(f'            tidied {nl} stray ledges, {ne} stray elevations')
        write_map(spec, blocks, dry)

    # A declared connection with no crossable cell is worse than no
    # connection, so the seams are tested against the terrain as written and
    # the dead ones dropped from both headers.
    ok = crossable(origins(), built)
    dropped = []
    for k in list(CONN):
        keep = []
        for side, nb, off in sorted(set(CONN[k])):
            if ok(k, side, nb, off):
                keep.append((side, nb, off))
            else:
                dropped.append(f'{k[4:]} {side} -> {nb[4:]}')
        CONN[k] = keep
    if dropped:
        print(f'  dropped {len(dropped)} impassable seams: ' + '; '.join(sorted(dropped)))
    for spec in NEWMAPS:
        write_header(spec, dry)

    # layouts
    def add_layouts(d):
        have = {l['id'] for l in d['layouts'] if l}
        for s in NEWMAPS:
            lid = f'LAYOUT_{s["name"].upper()}'
            if lid in have:
                continue
            d['layouts'].append({
                'id': lid, 'name': f'{s["name"]}_Layout',
                'width': s['w'], 'height': s['h'],
                'primary_tileset': 'gTileset_General',
                'secondary_tileset': s.get('secondary', 'gTileset_Petalburg'),
                'border_filepath': f'data/layouts/{s["name"]}/border.bin',
                'blockdata_filepath': f'data/layouts/{s["name"]}/map.bin'})
    patch_json(f'{ROOT}/data/layouts/layouts.json', add_layouts, dry)

    # map group
    def add_group(d):
        g = d['gMapGroup_TownsAndRoutes']
        for s in NEWMAPS:
            if s['name'] not in g:
                g.append(s['name'])
    patch_json(f'{ROOT}/data/maps/map_groups.json', add_group, dry)

    # region map sections, appended so MAPSEC_NONE stays past the end
    def add_mapsec(d):
        have = {m['id'] for m in d['map_sections']}
        for s in NEWMAPS:
            if s['mapsec'] not in have:
                d['map_sections'].append({'id': s['mapsec'], 'name': s['title']})
    patch_json(f'{ROOT}/src/data/region_map/region_map_sections.json', add_mapsec, dry)

    # event_scripts.s is a flat list of includes, not generated from anything,
    # so a new map's scripts.inc has to be added by hand or the link fails on
    # an undefined <Name>_MapScripts
    p = f'{ROOT}/data/event_scripts.s'
    lines = open(p).read().split('\n')
    anchor = max(i for i, l in enumerate(lines) if 'data/maps/Route134/scripts.inc' in l)
    add = [f'\t.include "data/maps/{s["name"]}/scripts.inc"' for s in GAP1
           if f'data/maps/{s["name"]}/scripts.inc' not in '\n'.join(lines)]
    if add:
        lines[anchor+1:anchor+1] = add
        print(f'  + {len(add)} script includes in event_scripts.s')
        if not dry:
            open(p, 'w').write('\n'.join(lines))

    # the other half of every seam, vanilla routes and towns alike
    new = {s['const'] for s in NEWMAPS}
    vanilla = {k: sorted(set(v)) for k, v in derived.items() if k not in new}
    for const, conns in vanilla.items():
        name = map_dir(const)
        p = f'{ROOT}/data/maps/{name}/map.json'
        d = json.load(open(p))
        # drop every connection to a new map first, so a seam that was dropped
        # for being impassable actually disappears instead of lingering
        kept = [c for c in (d.get('connections') or []) if c.get('map') not in new]
        d['connections'] = kept + [{'map': m, 'offset': off, 'direction': dirn}
                                   for dirn, m, off in conns]
        print(f'  + {len(conns)} connections on {name}')
        if not dry:
            json.dump(d, open(p, 'w'), indent=2)

    print('gating the town exits...')
    gates(dry)

    print('dry run, nothing written' if dry else 'written')

if __name__ == '__main__':
    sys.exit(main())

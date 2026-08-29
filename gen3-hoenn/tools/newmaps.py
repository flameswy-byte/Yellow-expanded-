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
def world_classes(skip=()):
    """class of every occupied world cell in vanilla, plus the map it is on.

    Our own maps are left out. They are on disk from the last run, and a new
    map seeds its rim from whatever is across the seam, so reading them made
    each run depend on the one before it: running the generator twice produced
    two different Hoenns, alternating forever - 401 cells of Route 139 flipped
    between two states, because a single rim seed decides a whole voronoi
    region. The maps are added back below as they are built, in order, so a
    seam between two new maps still matches - it matches the one built first.
    """
    lay, maps, pos = R.solve()
    minx = min(x for x, _ in pos.values()); miny = min(y for _, y in pos.values())
    rend = R.Renderer()
    cls, owner = {}, {}
    for k, (mx, my) in pos.items():
        if k in skip:
            continue
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
    spec_num = spec['num']

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
    place_ponds(grid, dist, rim, w, h, seed, spec_num)
    rocky_coast(grid, rim, w, h, seed)
    shoreline(grid, rim, w, h, seed)
    vegetate(grid, dist, rim, w, h, seed)

    # 6. connectivity. Scattering trees can wall a pocket off, and a stranded
    #    pocket is worse than a plain one. Everything walkable is flooded, and
    #    any component of real size that is not part of the largest gets a
    #    one-cell corridor cut back to it through whatever is in the way.
    repair_connectivity(grid, w, h)
    return grid

# Eleven of vanilla's 34 land routes have a pond, 31 ponds between them, median
# 4 cells and the largest 100. Six of ours had no inland water at all, including
# Route 143 at 160x40 and Route 146 at 40x120.
POND_MAP_CHANCE = 0.30      # vanilla puts one on about a fifth of its routes
POND_MIN, POND_MAX = 8, 46

def place_ponds(grid, dist, rim, w, h, seed, num):
    """Drop one or two small ponds into a map that has no water of its own."""
    if T.fbm(num, num, seed + 171, octaves=1, freq=0.7) > POND_MAP_CHANCE:
        return 0
    open_ = [i for i in range(w * h)
             if grid[i] in (T.GRASS, T.TALL) and (i % w, i // w) not in rim
             and dist[i] is not None and dist[i] > 3
             and 3 < i % w < w - 4 and 3 < i // w < h - 4]
    if len(open_) < 200:
        return 0
    made = 0
    for n in range(2):
        pool = [i for i in open_ if grid[i] in (T.GRASS, T.TALL)]
        if not pool:
            break
        c = max(pool, key=lambda i: T.fbm(i % w, i // w, seed + 181 + n * 13,
                                          octaves=1, freq=0.05))
        want = POND_MIN + int((POND_MAX - POND_MIN)
                              * T.fbm(c % w, c // w, seed + 191 + n, octaves=1,
                                      freq=0.9) ** 2)
        blob, front = {c}, [c]
        while front and len(blob) < want:
            i = front.pop(0)
            x, y = i % w, i // w
            for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                j = ny*w + nx
                if (0 <= nx < w and 0 <= ny < h and j not in blob
                        and j in open_ and len(blob) < want):
                    blob.add(j)
                    front.append(j)
        if len(blob) >= POND_MIN:
            for i in blob:
                grid[i] = T.POND
            made += 1
    return made

# Hoenn's coast is rock. Vanilla's sea touches cliff 83% of the time, sand 3%,
# grass 2% - you do not walk off a lawn into the ocean, you look down at it from
# a sea wall and enter the water at a beach.
#
# The composition was easy to match and did not help, because a coastline is
# one-dimensional and the noise was being sampled in two. Deciding rock or beach
# per cell from a 2D field gives a shore that alternates every cell or two;
# vanilla's runs for twenty cells of rock and then opens into a beach. So the
# chain of shore cells is traced first and the noise is read along its arc
# length, which is the only axis it varies on.
COAST_ROCK = 0.46
COAST_FREQ = 0.055        # about 18 cells of shore per run
BEACH_DEPTH = 2

def coast_chains(shore, w, h):
    """Order the shore cells into chains, so noise can run along the coast."""
    left = set(shore)
    chains = []
    while left:
        # start at an end of the chain if there is one, so the walk does not
        # begin in the middle and produce two half-runs
        start = next((i for i in left if sum(
            1 for dx in (-1, 0, 1) for dy in (-1, 0, 1)
            if (dx or dy) and (i // w + dy) * w + (i % w + dx) in left) == 1), None)
        if start is None:
            start = next(iter(left))
        chain, cur = [], start
        while cur is not None:
            chain.append(cur)
            left.discard(cur)
            x, y = cur % w, cur // w
            nxt = None
            for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1),
                           (1, 1), (1, -1), (-1, 1), (-1, -1)):
                j = (y + dy) * w + (x + dx)
                if 0 <= x + dx < w and 0 <= y + dy < h and j in left:
                    nxt = j
                    break
            cur = nxt
        chains.append(chain)
    return chains

def rocky_coast(grid, rim, w, h, seed):
    """Wall most of the waterline with rock, and open beaches in between."""
    shore = [i for i, c in enumerate(grid)
             if c in (T.GRASS, T.TALL, T.PATH, T.SAND)
             and (i % w, i // w) not in rim
             and any(0 <= i % w + dx < w and 0 <= i // w + dy < h
                     and grid[(i // w + dy) * w + (i % w + dx)] == T.WATER
                     for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
    if not shore:
        return 0, 0
    rock = sand = 0
    beach_cells = []
    for chain in coast_chains(set(shore), w, h):
        for t, i in enumerate(chain):
            if T.fbm(t, 0, seed + 211, octaves=2, freq=COAST_FREQ) > COAST_ROCK:
                grid[i] = T.CLIFF
                rock += 1
            else:
                grid[i] = T.SAND
                beach_cells.append(i)
                sand += 1
    # neither a beach nor a sea wall is one cell wide. A single-cell rock hem
    # was the other big source of patterns vanilla never draws - 53% of cliff
    # cells were falling past the 3x3 lookup.
    front = [i for i in shore if grid[i] == T.CLIFF]
    for _ in range(1):
        nxt = []
        for i in front:
            x, y = i % w, i // w
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                j = (y + dy) * w + (x + dx)
                if (0 <= x + dx < w and 0 <= y + dy < h
                        and grid[j] in (T.GRASS, T.TALL)
                        and (x + dx, y + dy) not in rim):
                    grid[j] = T.CLIFF
                    nxt.append(j)
                    rock += 1
        front = nxt
    front = list(beach_cells)
    for _ in range(BEACH_DEPTH - 1):
        nxt = []
        for i in front:
            x, y = i % w, i // w
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                j = (y + dy) * w + (x + dx)
                if (0 <= x + dx < w and 0 <= y + dy < h
                        and grid[j] in (T.GRASS, T.TALL)
                        and (x + dx, y + dy) not in rim):
                    grid[j] = T.SAND
                    nxt.append(j)
                    sand += 1
        front = nxt
    return rock, sand

# Vanilla's shallows are not a fringe, they are bays: 84 blobs across the game
# with a median of 12 cells and horizontal runs from one cell to nine. Ours were
# a one-cell hem - 215 blobs of median 2, runs almost always width 1 - and the
# painter had never seen that shape, so 71% of shallow cells fell past the 3x3
# lookup onto a bare fill tile. A grey stripe with no edges is what that looks
# like on screen.
SHORE_BLOBS = 0.055        # share of a map's water to turn into shallows
SHALLOW_MIN, SHALLOW_MAX = 6, 40

def shoreline(grid, rim, w, h, seed):
    """Grow shallow bays off the beaches, rather than hemming the whole coast."""
    sea = [i for i, c in enumerate(grid) if c == T.WATER]
    if not sea:
        return 0
    budget = int(SHORE_BLOBS * len(sea))
    # seed only where vanilla puts them: against sand and rock, not grass
    seeds = [i for i in sea
             if (i % w, i // w) not in rim
             and any(0 <= i % w + dx < w and 0 <= i // w + dy < h
                     and grid[(i // w + dy) * w + (i % w + dx)] in (T.SAND, T.CLIFF)
                     for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
    if not seeds:
        return 0
    seeds.sort(key=lambda i: -T.fbm(i % w, i // w, seed + 151, octaves=1, freq=0.06))
    made = 0
    used = set()
    for start in seeds:
        if made >= budget:
            break
        if start in used:
            continue
        want = SHALLOW_MIN + int((SHALLOW_MAX - SHALLOW_MIN)
                                 * T.fbm(start % w, start // w, seed + 161,
                                         octaves=1, freq=0.8) ** 2)
        blob, front = {start}, [start]
        while front and len(blob) < want:
            i = front.pop(0)
            x, y = i % w, i // w
            for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                j = ny*w + nx
                if (0 <= nx < w and 0 <= ny < h and j not in blob
                        and grid[j] == T.WATER and (nx, ny) not in rim
                        and len(blob) < want):
                    blob.add(j)
                    front.append(j)
        if len(blob) < SHALLOW_MIN:
            continue
        for i in blob:
            grid[i] = T.SHALLOW
        used |= blob
        made += len(blob)
    return made

# --- mountains as terraces -------------------------------------------------
# Vanilla does not draw a mountain as a flat impassable blob. Route 115 has
# ground at elevation 3 and plateaus at 5; Route 114 stacks 3, 4, 5 and 7. Each
# terrace is a walkable top ringed by impassable rock at elevation 0, and the
# only way up is a handful of ordinary walkable tiles also left at elevation 0 -
# six of them on the whole of Route 115. Elevation is what separates the levels,
# not the metatile: vanilla puts plain grass (0x001) at elevation 5 on a summit.
#
# Ours had none of this. Every generated mountain was solid: Route 143 was
# 3,719 impassable cells with no walkable top at all, so its "mountain" was a
# wall you could only walk around.
GROUND_LEVEL = 3
TIER_LEVELS = (5, 7)          # first and second terrace, as vanilla uses
MIN_MASS = 150                # a cliff smaller than this stays a plain rock
MIN_TOP = 24                  # and a terrace smaller than this is not worth it
WALK_CLASSES = (T.GRASS, T.TALL, T.PATH, T.SAND, T.PLATEAU, T.SHALLOW)

def _erode(cells, w, h):
    """cells whose whole 8-neighbourhood is also in the set."""
    return {i for i in cells
            if all((i % w + dx, i // w + dy) != (-1, -1) and
                   0 <= i % w + dx < w and 0 <= i // w + dy < h and
                   (i // w + dy) * w + (i % w + dx) in cells
                   for dx in (-1, 0, 1) for dy in (-1, 0, 1))}

def terrace(grid, w, h):
    """Turn solid cliff masses into walkable terraces, and return the elevation
    of every cell. Also reports how many stairs were cut."""
    level = [GROUND_LEVEL] * (w * h)
    for i, c in enumerate(grid):
        if c in (T.WATER, T.POND):
            level[i] = 1
        elif c in (T.TREE, T.CLIFF):
            level[i] = 0
        # shallow water is walked through, not surfed: vanilla puts it at
        # elevation 3 with the ground, and 2,405 of its 2,836 cells are c0e3

    seen = [False] * (w * h)
    stairs = []
    masses = []
    for start in range(w * h):
        if seen[start] or grid[start] != T.CLIFF:
            continue
        mass, q = set(), [start]
        seen[start] = True
        while q:
            i = q.pop()
            mass.add(i)
            x, y = i % w, i // w
            for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                j = ny*w + nx
                if 0 <= nx < w and 0 <= ny < h and not seen[j] and grid[j] == T.CLIFF:
                    seen[j] = True
                    q.append(j)
        if len(mass) < MIN_MASS:
            continue
        # a two-cell wall, because vanilla's rock face has height: 577 of its
        # cliff cells have plateau above and cliff below, and the one-cell
        # version produced PPP/###/PPP, a pattern vanilla uses exactly 0 times
        tier = _erode(_erode(mass, w, h), w, h)
        if len(tier) < MIN_TOP:
            continue
        for t, lv in enumerate(TIER_LEVELS):
            for i in tier:
                grid[i] = T.PLATEAU
                level[i] = lv
            if t + 1 >= len(TIER_LEVELS):
                break
            # the step between terraces is one cell of wall, not two: a stair
            # is a single cell that has to touch both levels at once, and a
            # two-cell wall left the upper terrace unreachable
            # a three-cell band of lower terrace, then two cells of wall again
            step = tier
            for _ in range(3):
                step = _erode(step, w, h)
            inner = _erode(_erode(step, w, h), w, h)
            if len(inner) < MIN_TOP:
                break
            for i in step - inner:
                grid[i] = T.CLIFF
                level[i] = 0
            tier = inner
        masses.append(mass)
    # thicken before cutting stairs, or the thickening walls the stairs back up
    thicken_cliffs(grid, level, w, h)
    for mass in masses:
        stairs += cut_stairs(grid, level, mass, w, h)
    stairs += ensure_reachable(grid, level, w, h)
    return level, stairs

def thicken_cliffs(grid, level, w, h):
    """Give a rock face some height.

    Vanilla's cliffs are masses, not lines: 49% of its cliff cells have cliff
    both above and below, and only 30% of its vertical runs are a single row.
    Ours were 27% and 47% - nearly half our rock was one row tall, a shape the
    painter had never seen, which is most of why 50% of cliff cells were
    falling past the 3x3 lookup.
    """
    add = []
    for i, c in enumerate(grid):
        if c != T.CLIFF:
            continue
        x, y = i % w, i // w
        if y == 0 or y + 2 >= h:
            continue
        if grid[(y-1)*w + x] == T.CLIFF or grid[(y+1)*w + x] == T.CLIFF:
            continue                       # already part of a taller run
        # grow downward, which is the side the face is drawn on, and only into
        # open ground - never into water, a path or another map's rim
        j = (y+1)*w + x
        if grid[j] in (T.GRASS, T.TALL):
            add.append(j)
    for j in add:
        grid[j] = T.CLIFF
        level[j] = 0
    return len(add)

def _elev_ok(a, b):
    return a == b or 0 in (a, b) or 15 in (a, b)

def ensure_reachable(grid, level, w, h):
    """No terrace ships unreachable.

    cut_stairs picks the prettiest site it can find and does not always find
    one. This checks the result the way the player would - flood the ground,
    respecting elevation - and cuts a passage into anything still stranded.

    It carves a path rather than a single cell: the wall between two terraces
    is two cells thick, and a one-cell notch cannot bridge it. That was the
    bug the first version had, and it came back the moment the walls got their
    proper height.
    """
    # Seed from the map's rim, not from every ground-level cell. Seeding from
    # all ground meant a terrace could be judged connected to ground that was
    # itself walled off from the map's edges - Route 144 shipped 741 cells the
    # player could never stand on, and the check said it was fine.
    rim = [i for i in range(w * h)
           if grid[i] in WALK_CLASSES
           and (i % w in (0, w-1) or i // w in (0, h-1))]
    if not rim:
        rim = [i for i in range(w * h)
               if grid[i] in WALK_CLASSES and level[i] == GROUND_LEVEL]
    extra = []
    for _ in range(12):
        seen = set(rim)
        q = collections.deque(rim)
        while q:
            i = q.popleft()
            x, y = i % w, i // w
            for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                j = ny*w + nx
                if (0 <= nx < w and 0 <= ny < h and j not in seen
                        and grid[j] in WALK_CLASSES and _elev_ok(level[i], level[j])):
                    seen.add(j)
                    q.append(j)
        # anything walkable the rim cannot reach, not just terraces
        stranded = [i for i in range(w * h)
                    if grid[i] in WALK_CLASSES and i not in seen]
        if not stranded:
            break
        # 0-1 BFS out of the stranded region: free across walkable cells,
        # cost 1 to cut a cliff, so it finds the thinnest wall to the outside
        INF = float('inf')
        cost = [INF] * (w * h)
        prev = [-1] * (w * h)
        dq = collections.deque()
        for i in stranded:
            cost[i] = 0
            dq.append(i)
        hit = -1
        while dq:
            i = dq.popleft()
            if i in seen:
                hit = i
                break
            x, y = i % w, i // w
            for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                if not (0 <= nx < w and 0 <= ny < h):
                    continue
                j = ny*w + nx
                if grid[j] in (T.WATER, T.POND):
                    continue                  # never cut a channel to the sea
                step = 0 if grid[j] in WALK_CLASSES else 1
                if cost[i] + step < cost[j]:
                    cost[j] = cost[i] + step
                    prev[j] = i
                    (dq.appendleft if step == 0 else dq.append)(j)
        if hit < 0:
            break
        i = hit
        while i != -1:
            if grid[i] not in WALK_CLASSES:
                grid[i] = T.GRASS
                level[i] = 0
                extra.append((i, False))
            i = prev[i]
    return extra

# Vanilla's staircase is a horizontal pair - 0x0AF on the left, 0x0CF on the
# right - laid at elevation 0 with a different level above and below, so you
# walk up or down through it. Route 115 uses eight of these pairs and nothing
# else. A single cell painted as grass, which is what this used to cut, shows
# up as a green speck in the middle of a brown mountain.
STAIR_L, STAIR_R = 0x0AF, 0x0CF
STAIR_NOTCH = 0x071           # mountain top, for a gap a staircase cannot fill

def notch(blocks, j, w, h):
    """Cut a hole through the blocker at j, drawn as whatever it is cut through.

    The value has to be elevation 0 - that is the level that connects two
    different ones - and collision 0. What it must not be is a fixed tile: a
    mountain top opened through a forest to reach a stranded pocket leaves a
    pink rock speck in the middle of the trees, which is exactly what Route
    141 had three of. So the art comes from the walkable neighbours, which are
    the two sides this hole is joining.
    """
    x, y = j % w, j // w
    near = collections.Counter()
    for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
        if 0 <= nx < w and 0 <= ny < h:
            v = blocks[ny*w + nx]
            if not ((v >> 10) & 3):
                near[v & 0x3FF] += 1
    blocks[j] = near.most_common(1)[0][0] if near else STAIR_NOTCH

def cut_stairs(grid, level, mass, w, h, want=2):
    """Open a way up, and say where the staircases went."""
    tops = collections.defaultdict(set)
    for i in mass:
        if grid[i] == T.PLATEAU:
            tops[level[i]].add(i)
    placed = []
    for lv, top in sorted(tops.items()):
        def below(i):
            return grid[i] in WALK_CLASSES and level[i] < lv

        pairs, singles = [], []
        for i in mass:
            if grid[i] != T.CLIFF:
                continue
            x, y = i % w, i // w
            if not (0 < y < h - 1):
                continue
            up, dn = (y-1)*w + x, (y+1)*w + x
            # a staircase needs two cells side by side, the terrace on one
            # side of them and lower ground on the other
            # vanilla's staircase is a 2x2 block of wall - 0AF/0CF over two
            # rows - with the terrace on one side and the ground on the other.
            # A 2x1 cannot span a wall that is two cells tall.
            if x + 1 < w and y + 2 < h:
                blk = [i, i + 1, i + w, i + w + 1]
                over, under = i - w, i + 2 * w
                if (all(0 <= k < w * h and grid[k] == T.CLIFF and k in mass
                        for k in blk)
                        and ((over in top and below(under))
                             or (under in top and below(over)))
                        and ((over + 1 in top and below(under + 1))
                             or (under + 1 in top and below(over + 1)))):
                    pairs.append(i)
                    continue
            elif any(k in top for k in (up, dn, i-1, i+1)) and any(
                    0 <= k < w * h and below(k) for k in (up, dn, i-1, i+1)):
                singles.append(i)

        cand = pairs or singles
        if not cand:
            continue
        picked = [cand[0]]
        while len(picked) < want and len(picked) < len(cand):
            far = max(cand, key=lambda i: min(
                abs(i % w - p % w) + abs(i // w - p // w) for p in picked))
            if far in picked:
                break
            picked.append(far)
        for i in picked:
            wide = i in pairs
            for k in ((i, i + 1, i + w, i + w + 1) if wide else (i,)):
                if 0 <= k < w * h:
                    grid[k] = T.GRASS
                    level[k] = 0
            placed.append((i, wide))
    return placed

# Vanilla does not leave every terrace as bare rock, but nor does it speckle
# grass across one. A summit has a consistent surface: some plateaus are rock
# all over, others are grass all over with patches of long grass on them, and
# the two kinds sit on different terraces. Route 115's plateaus at elevation 5
# come out about half and half by area.
#
# Speckling grass over rock produced 515 cells where grass met bare mountain
# top - vanilla has 45 in the whole game, across 49 maps - and because both
# sides are flat fill tiles with no transition between them, every one of those
# was a hard arbitrary edge.
GRASS_TOP_CHANCE = 0.5
TERRACE_TALL = 0.16
# A whole summit of bare rock is something vanilla only does small. Its 35
# summits run to 468 cells, but the two drawn as bare mountain top - both on
# Route 114 - are 127 and 95; every larger one is grass, most of them with
# tall grass and a path on top. Route 144's was 707 cells of empty pink rock,
# bigger than anything in Hoenn and blanker than all of it.
ROCK_TOP_MAX = 127

def vegetate_terraces(grid, level, w, h, seed):
    """Decide each terrace's surface as a whole, not cell by cell.

    Runs after terrace(), so it has to keep each cell's elevation - a grass
    tile at elevation 5 is exactly what vanilla puts on a plateau, and dropping
    it to 3 would sink the terrace into the map.
    """
    seen = [False] * (w * h)
    for start in range(w * h):
        if seen[start] or grid[start] != T.PLATEAU:
            continue
        comp, q, lv = [], [start], level[start]
        seen[start] = True
        while q:
            i = q.pop()
            comp.append(i)
            x, y = i % w, i // w
            for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                j = ny*w + nx
                if (0 <= nx < w and 0 <= ny < h and not seen[j]
                        and grid[j] == T.PLATEAU and level[j] == lv):
                    seen[j] = True
                    q.append(j)
        if len(comp) < 12:
            continue
        x0, y0 = comp[0] % w, comp[0] // w
        if (len(comp) <= ROCK_TOP_MAX
                and T.fbm(x0, y0, seed + 91, octaves=1, freq=0.21) > GRASS_TOP_CHANCE):
            continue                       # this one stays a rock summit
        for i in comp:
            grid[i] = T.GRASS
        n_tall = int(TERRACE_TALL * len(comp))
        if n_tall:
            rank = sorted(comp, key=lambda i: -T.fbm(i % w, i // w,
                                                     seed + 97 + lv,
                                                     octaves=1, freq=0.09))
            for i in rank[:n_tall]:
                grid[i] = T.TALL

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
MIN_LEDGE = 4     # strays only; the deliberate runs are stamped after tidy

# Vanilla's ledge is 0x087, MB_JUMP_SOUTH, collision 1 at elevation 3 - you hop
# down over it southward and cannot come back. It is not a way off a cliff:
# 179 of them have ordinary grass at elevation 3 both above and below, so they
# are shortcuts across flat ground. Runs are horizontal, median 4 cells, and
# 21 vanilla routes carry 74 of them between them.
LEDGE_TILE = 0x087
LEDGE_MIN, LEDGE_MAX = 3, 8
LEDGE_PER_MAP = 3
LEDGE_APART = 12

def place_ledges(grid, level, w, h, seed):
    """Pick a few horizontal runs of flat ground to turn into ledges.

    A ledge only makes sense where the player can stand above it and land
    below, so both rows have to be walkable and at the same elevation, and the
    landing row must not itself be a ledge or a wall.

    It also has to start or finish somewhere. Of vanilla's 47 horizontal ledge
    runs, 42 have at least one end butting into trees or a cliff - the ledge
    closes a gap, which is what makes hopping it a shortcut. Five float free in
    open ground. Ours were placed by length alone, so they were all of the
    fifth sort: three brown bars lying in the middle of a field.
    """
    def open_at(i):
        return grid[i] in (T.GRASS, T.TALL, T.PATH, T.SAND)

    def wall(x, y):
        return not (0 <= x < w) or grid[y*w + x] in (T.TREE, T.CLIFF,
                                                     T.WATER, T.POND)

    runs = []
    for y in range(2, h - 2):
        x = 1
        while x < w - 1:
            n = 0
            while (x + n < w - 1
                   and open_at((y)*w + x + n)
                   and open_at((y-1)*w + x + n) and open_at((y+1)*w + x + n)
                   and level[(y)*w + x + n] == GROUND_LEVEL
                   and level[(y-1)*w + x + n] == GROUND_LEVEL
                   and level[(y+1)*w + x + n] == GROUND_LEVEL):
                n += 1
            if n >= LEDGE_MIN:
                # anchor it: left end against a wall, else right end against
                # one, else this gap is not a gap and gets no ledge
                if wall(x - 1, y):
                    runs.append((x, y, min(n, LEDGE_MAX), +1))
                elif wall(x + n, y):
                    runs.append((x + n - 1, y, min(n, LEDGE_MAX), -1))
            x += max(n, 1)
    if not runs:
        return []
    runs.sort(key=lambda r: -(r[2] + 3 * T.fbm(r[0], r[1], seed + 131,
                                               octaves=1, freq=0.08)))
    picked = []
    for x, y, n, d in runs:
        if len(picked) >= LEDGE_PER_MAP:
            break
        if any(abs(x - px) + abs(y - py) <= LEDGE_APART for px, py, _ in picked):
            continue
        # vanilla's runs have a median of 4, not a maximum of 8. Taking the
        # longest run available every time gave every ledge the same length
        # and twice vanilla's ledge count by area.
        u = T.fbm(x, y, seed + 137, octaves=1, freq=0.3)
        k = min(n, LEDGE_MIN + int((LEDGE_MAX - LEDGE_MIN + 1) * u * u))
        picked.append((x if d > 0 else x - k + 1, y, k))
    return picked

def stamp_ledges(blocks, ledges, w, h):
    for x, y, n in ledges:
        for k in range(n):
            blocks[y*w + x + k] = LEDGE_TILE | (1 << 10) | (GROUND_LEVEL << 12)

def stamp_stairs(blocks, stairs, w, h):
    """Lay vanilla's staircase art over the cells cut_stairs opened."""
    for i, wide in stairs:
        if wide and i % w + 1 < w and i + w + 1 < len(blocks):
            for r in (0, w):
                blocks[i + r] = STAIR_L
                blocks[i + r + 1] = STAIR_R
        else:
            notch(blocks, i, w, h)

def apply_levels(blocks, level, cls, w, h):
    """Stamp the terrace elevations onto the painted blockdata.

    Elevation is orthogonal to the metatile - vanilla puts the same grass tile
    at 3 on the ground and 5 on a summit - so the painter picks the art and
    this picks the level. The map's outermost ring is left alone: those cells
    were copied from the neighbour across the seam and have to keep matching it.
    """
    for i, lv in enumerate(level):
        x, y = i % w, i // w
        if x == 0 or y == 0 or x == w-1 or y == h-1:
            continue
        blocks[i] = (blocks[i] & ~0xF000) | ((lv & 0xF) << 12)

def final_check(blocks, w, h, beh_cache=[]):
    """Last word on reachability, run against the blockdata as it will ship.

    terrace() and ensure_reachable() work on the class grid, but tidy(),
    apply_levels() and the ledges all run afterwards and can move a cell. The
    only check that counts is the one on the bytes that go in the ROM. Small
    stranded pockets are snapped down to ground level - they are strays, not
    terraces - and anything larger gets a notch opened into it.
    """
    E = lambda i: (blocks[i] >> 12) & 0xF
    C = lambda i: (blocks[i] >> 10) & 3
    walk = lambda i: C(i) == 0
    fixed = 0
    rim = [i for i in range(w * h)
           if walk(i) and (i % w in (0, w-1) or i // w in (0, h-1))]
    if not rim:
        rim = [i for i in range(w * h) if walk(i) and E(i) == GROUND_LEVEL]
    for _ in range(8):
        q = collections.deque(rim)
        seen = set(rim)
        while q:
            i = q.popleft()
            x, y = i % w, i // w
            for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                j = ny*w + nx
                if (0 <= nx < w and 0 <= ny < h and j not in seen and walk(j)
                        and _elev_ok(E(i), E(j))):
                    seen.add(j)
                    q.append(j)
        lost = [i for i in range(w * h) if walk(i) and i not in seen]
        if not lost:
            break
        # group them, then deal with each pocket on its size
        left = set(lost)
        while left:
            start = next(iter(left))
            comp, st = set(), [start]
            left.discard(start)
            while st:
                i = st.pop()
                comp.add(i)
                x, y = i % w, i // w
                for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                    j = ny*w + nx
                    if j in left and _elev_ok(E(i), E(j)):
                        left.discard(j)
                        st.add(j) if isinstance(st, set) else st.append(j)
            if len(comp) <= 8:
                for i in comp:
                    blocks[i] = (blocks[i] & ~0xF000) | (GROUND_LEVEL << 12)
                    fixed += 1
            else:
                for i in sorted(comp):
                    x, y = i % w, i // w
                    done = False
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        j = (y+dy)*w + (x+dx)
                        if not (0 <= x+dx < w and 0 <= y+dy < h) or walk(j):
                            continue
                        for ex, ey in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                            m = (y+dy+ey)*w + (x+dx+ex)
                            if (0 <= x+dx+ex < w and 0 <= y+dy+ey < h
                                    and m in seen and walk(m)):
                                notch(blocks, j, w, h)
                                fixed += 1
                                done = True
                                break
                        if done:
                            break
                    if done:
                        break
    return fixed

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

WALKABLE = (T.GRASS, T.TALL, T.PATH, T.SAND, T.OTHER, T.SHALLOW)

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
    wcls, _ = world_classes(skip={s['const'] for s in NEWMAPS})

    built = {}
    for spec in NEWMAPS:
        cls = build_classes(spec, wcls)
        # publish this map's terrain for the maps built after it
        for j in range(spec['h']):
            for i in range(spec['w']):
                wcls[(spec['x'] + i, spec['y'] + j)] = cls[j * spec['w'] + i]
        level, stairs = terrace(cls, spec['w'], spec['h'])
        vegetate_terraces(cls, level, spec['w'], spec['h'], spec['num'] * 1013)
        ledges = place_ledges(cls, level, spec['w'], spec['h'], spec['num'] * 1013)
        # a painter per map: the tiles it may reach for depend on which
        # secondary tileset that map loads
        blocks = T.Painter(model, spec.get('secondary')).paint(
            cls, spec['w'], spec['h'])
        stamp_stairs(blocks, stairs, spec['w'], spec['h'])
        apply_levels(blocks, level, cls, spec['w'], spec['h'])
        wide = sum(1 for _, wd in stairs if wd)
        nl, ne = tidy(blocks, spec['w'], spec['h'], spec)
        # after tidy, so raising its stray-ledge threshold cannot eat these
        stamp_ledges(blocks, ledges, spec['w'], spec['h'])
        nf = final_check(blocks, spec['w'], spec['h'])
        built[spec['const']] = blocks
        n = collections.Counter(cls)
        mix = ', '.join(f'{100*v//len(cls)}% {T.CLASS_NAME[k]}'
                        for k, v in n.most_common() if 100*v//len(cls))
        print(f'  {spec["name"]}  {spec["w"]}x{spec["h"]}  '
              f'buffer {(spec["w"]+15)*(spec["h"]+14)}/10240   {mix}')
        if nl or ne or stairs or ledges or nf:
            print(f'            tidied {nl} ledges, {ne} elevations; '
                  f'{len(stairs)} stairs ({wide} staircases), {len(ledges)} ledges'
                  + (f', {nf} cells repaired' if nf else ''))
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

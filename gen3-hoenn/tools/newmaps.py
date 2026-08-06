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

# Connections are deliberately routes-only. Littleroot, Oldale, Petalburg and
# Slateport all border these maps, but opening a town edge changes which
# coordinates the player can reach during that town's scripted sequences -
# the mistake that cost the most in the Kanto project. Route 101 is skipped
# for the same reason: VAR_ROUTE101_STATE confines the player during the
# Birch rescue and only guards the exits vanilla knows about.
CONN = {
 'MAP_ROUTE135': [('left','MAP_ROUTE105',0), ('up','MAP_ROUTE102',30),
                  ('down','MAP_ROUTE136',0), ('down','MAP_ROUTE137',40)],
 'MAP_ROUTE136': [('up','MAP_ROUTE135',0), ('right','MAP_ROUTE137',0),
                  ('left','MAP_ROUTE105',-40), ('down','MAP_ROUTE106',-40)],
 'MAP_ROUTE137': [('up','MAP_ROUTE135',-40), ('up','MAP_ROUTE138',60),
                  ('left','MAP_ROUTE136',0), ('left','MAP_ROUTE106',40),
                  ('down','MAP_ROUTE107',0), ('down','MAP_ROUTE108',60),
                  ('right','MAP_ROUTE109',18)],
 'MAP_ROUTE138': [('up','MAP_ROUTE103',-20), ('down','MAP_ROUTE137',-60),
                  ('right','MAP_ROUTE110',-82)],
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

OPP = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}
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

    # 3. paths, at width 3 with a noise wobble. A path is a promise that the
    #    player can walk it, so nothing solid is allowed within two cells of
    #    one and the surrounding band is forced to open ground.
    path = set()
    for pts in lines:
        for x, y in pts:
            r = 1 + (1 if T.fbm(x, y, seed + 31, octaves=2, freq=0.15) > 0.62 else 0)
            for dx in range(-r, r+1):
                for dy in range(-r, r+1):
                    if 0 <= x+dx < w and 0 <= y+dy < h:
                        path.add((x+dx, y+dy))
    for x, y in path:
        grid[y*w + x] = T.PATH
    for x, y in list(path):
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                p = (x+dx, y+dy)
                if p in path or not (0 <= p[0] < w and 0 <= p[1] < h):
                    continue
                if grid[p[1]*w + p[0]] in (T.TREE, T.CLIFF):
                    grid[p[1]*w + p[0]] = T.GRASS

    # 4. vegetation gradient. Distance is measured from where the player
    #    actually walks - the paths, and the walkable rim where a connection
    #    lands - and open ground gives way to tall grass, then scattered
    #    trees, then closed canopy as that distance grows. The clumping is
    #    noise, not a radius, so none of the bands come out as rings.
    solid = [grid[i] in (T.WATER, T.CLIFF) for i in range(w * h)]
    walkable_rim = [(x, y) for (x, y), c in rim.items() if c in (T.GRASS, T.PATH, T.SAND)]
    src = list(path) or walkable_rim
    if not src:
        src = [(w//2, h//2)]
    dist = bfs_dist(src, solid, w, h)
    for y in range(h):
        for x in range(w):
            i = y*w + x
            if grid[i] != T.GRASS or (x, y) in rim:
                continue
            d = dist[i]
            if d is None or d <= 1:
                continue                        # never right beside a path
            t = min(1.0, max(0.0, (d - 2) / 22.0))
            n = T.fbm(x, y, seed + 47, octaves=3, freq=0.07)
            if n > 0.74 - 0.30 * t:
                grid[i] = T.TREE
            elif n > 0.60 - 0.34 * t:
                grid[i] = T.TALL
    return grid

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
          ('MAP_ROUTE110', 'left',  (82, 99))]   # only the bottom of a long map
DEPTH = 4

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
    lay, maps, _ = R.solve()
    rend = R.Renderer()
    total = 0
    for const, side, span in SOFTEN:
        L = lay[maps[const]['layout']]
        w, h = L['width'], L['height']
        name = const.replace('MAP_', '').title()
        blk, path = pristine(name, L)
        C = T.Classifier(rend, L['primary_tileset'], L.get('secondary_tileset'))
        raw = [(blk[i*2] | (blk[i*2+1] << 8)) if i*2+1 < len(blk) else 0
               for i in range(w * h)]
        cls = [C(v & 0x3FF, (v >> 10) & 3) for v in raw]
        before = list(cls)
        skip = event_cells(name)
        seed = sum(ord(c) for c in const) * 31

        def depth_of(x, y):
            return {'up': y, 'down': h-1-y, 'left': x, 'right': w-1-x}[side]

        def in_span(x, y):
            if span is None:
                return True
            a = x if side in ('up', 'down') else y
            return span[0] <= a <= span[1]

        for y in range(h):
            for x in range(w):
                dep = depth_of(x, y)
                if dep >= DEPTH or (x, y) in skip or not in_span(x, y):
                    continue
                i = y*w + x
                if (raw[i] & 0x3FF) >= R.NUM_METATILES_IN_PRIMARY:
                    continue                    # town furniture, leave it
                n = T.fbm(x, y, seed, octaves=3, freq=0.11)
                if cls[i] in (T.TREE, T.CLIFF):
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
                elif cls[i] == T.GRASS and dep >= 2 and n > 0.80:
                    cls[i] = T.TREE             # rounded clumps, not a straight hem

        # repaint only where the 3x3 class neighbourhood actually moved, so
        # vanilla's hand-placed detail survives everywhere else
        out = list(raw)
        changed = 0
        for y in range(h):
            for x in range(w):
                if depth_of(x, y) > DEPTH or (x, y) in skip:
                    continue
                if not (in_span(x, y) or in_span(x-1, y) or in_span(x+1, y)
                        or in_span(x, y-1) or in_span(x, y+1)):
                    continue
                if T.mask3(cls, x, y, w, h, T.GRASS) == T.mask3(before, x, y, w, h, T.GRASS):
                    continue
                if (raw[y*w + x] & 0x3FF) >= R.NUM_METATILES_IN_PRIMARY:
                    continue
                v = (T.best(painter.m['t3'], T.mask3(cls, x, y, w, h, T.GRASS))
                     or T.best(painter.m['t4'], T.mask4(T.mask3(cls, x, y, w, h, T.GRASS)))
                     or T.best(painter.m['t1'], cls[y*w + x]))
                if v is not None and v != out[y*w + x]:
                    out[y*w + x] = v
                    changed += 1
        print(f'  soften {name:9s} {side:5s}  {changed} metatiles')
        total += changed
        if not dry:
            open(path, 'wb').write(u16(out))
    print(f'  -> {total} vanilla metatiles rewritten')

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
    hdr = {
        'id': spec['const'], 'name': spec['name'],
        'layout': f'LAYOUT_{spec["name"].upper()}', 'music': spec['music'],
        'region_map_section': spec['mapsec'], 'requires_flash': False,
        'weather': 'WEATHER_SUNNY', 'map_type': 'MAP_TYPE_ROUTE',
        'allow_cycling': True, 'allow_escaping': False, 'allow_running': True,
        'show_map_name': True, 'battle_scene': 'MAP_BATTLE_SCENE_NORMAL',
        'connections': [{'map': m, 'offset': o, 'direction': d}
                        for d, m, o in CONN[spec['const']]],
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

    model = T.load()
    painter = T.Painter(model)

    # soften first: the new maps seed their rim from the neighbours, so the
    # neighbours have to be final before the rim is read
    print('softening the old map borders...')
    soften(painter, dry)

    print('classifying vanilla terrain...')
    wcls, _ = world_classes()

    for spec in GAP1:
        cls = build_classes(spec, wcls)
        blocks = painter.paint(cls, spec['w'], spec['h'])
        n = collections.Counter(cls)
        mix = ', '.join(f'{100*v//len(cls)}% {T.CLASS_NAME[k]}'
                        for k, v in n.most_common() if 100*v//len(cls))
        print(f'  {spec["name"]}  {spec["w"]}x{spec["h"]}  '
              f'buffer {(spec["w"]+15)*(spec["h"]+14)}/10240   {mix}')
        write_map(spec, blocks, dry)

    # layouts
    def add_layouts(d):
        have = {l['id'] for l in d['layouts'] if l}
        for s in GAP1:
            lid = f'LAYOUT_{s["name"].upper()}'
            if lid in have:
                continue
            d['layouts'].append({
                'id': lid, 'name': f'{s["name"]}_Layout',
                'width': s['w'], 'height': s['h'],
                'primary_tileset': 'gTileset_General',
                'secondary_tileset': 'gTileset_Petalburg',
                'border_filepath': f'data/layouts/{s["name"]}/border.bin',
                'blockdata_filepath': f'data/layouts/{s["name"]}/map.bin'})
    patch_json(f'{ROOT}/data/layouts/layouts.json', add_layouts, dry)

    # map group
    def add_group(d):
        g = d['gMapGroup_TownsAndRoutes']
        for s in GAP1:
            if s['name'] not in g:
                g.append(s['name'])
    patch_json(f'{ROOT}/data/maps/map_groups.json', add_group, dry)

    # region map sections, appended so MAPSEC_NONE stays past the end
    def add_mapsec(d):
        have = {m['id'] for m in d['map_sections']}
        for s in GAP1:
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

    # the other half of every seam
    for const, conns in RECIP.items():
        name = const.replace('MAP_', '').title().replace('Route', 'Route')
        p = f'{ROOT}/data/maps/{name}/map.json'
        d = json.load(open(p))
        have = {(c['direction'], c['map']) for c in d.get('connections') or []}
        d.setdefault('connections', d.get('connections') or [])
        for dirn, m, off in conns:
            if (dirn, m) not in have:
                d['connections'].append({'map': m, 'offset': off, 'direction': dirn})
        print(f'  + {len(conns)} connections on {name}')
        if not dry:
            json.dump(d, open(p, 'w'), indent=2)

    print('dry run, nothing written' if dry else 'written')

if __name__ == '__main__':
    sys.exit(main())

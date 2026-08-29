#!/usr/bin/env python3
"""Terrain classes, and an autotiler learned from vanilla Hoenn.

Painting a new map means choosing a metatile for every cell, and the hard part
is never the middle of a field - it is the seam where grass meets water, or
sand meets cliff. Hoenn's General tileset has dozens of transition metatiles
and picking them by hand is where a generated map starts looking wrong.

So this does not hardcode them. It reads the vanilla maps, classifies every
metatile they use into a coarse terrain class, and records which metatile the
game actually used for each 3x3 arrangement of classes. Painting is then a
lookup: describe the terrain you want as classes, and each cell gets whatever
metatile vanilla uses in that exact situation. Seams come out right because
they are vanilla's own seams.

Where a 3x3 pattern was never seen, it falls back to the 4-neighbourhood, then
to the bare centre class, so painting always terminates with something sane.

    python3 tools/terrain.py --report        # what got classified as what
"""
import argparse, collections, json, os, pickle, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_hoenn as R

# --- terrain classes ------------------------------------------------------
# PLATEAU is the walkable top of a mountain, CLIFF the impassable rock face.
# Vanilla draws a mountain as terraces: a walkable top at a raised elevation,
# ringed by rock at elevation 0, joined to the ground by a handful of ordinary
# walkable tiles also at elevation 0. Lumping the two together made every
# generated mountain a solid wall - Route 143 was 3,719 impassable cells with
# no top at all.
# SHALLOW is the wading fringe at a shoreline. It is not a shade of water: in
# vanilla it is collision 0 at elevation 3 - ordinary walkable ground - sitting
# about two cells from land, and there are 2,836 of them. Treating it as water
# meant every one of our coasts went from land straight to surf.
# POND is inland fresh water, which vanilla draws with its own tiles and its
# own grass edges - painting one with the ocean's tiles puts the sea in a field.
WATER, SAND, GRASS, TALL, PATH, TREE, CLIFF, OTHER, PLATEAU, SHALLOW, POND = range(11)
CLASS_NAME = {WATER: 'water', SAND: 'sand', GRASS: 'grass', TALL: 'tall grass',
              PATH: 'path', TREE: 'trees', CLIFF: 'cliff', OTHER: 'other',
              PLATEAU: 'plateau', SHALLOW: 'shallow', POND: 'pond'}
# what the sketch pens mean in terms of classes
PEN_CLASS = {'water': WATER, 'grass': GRASS, 'tall grass': TALL, 'path': PATH,
             'trees': TREE, 'cliff': CLIFF, 'building': OTHER, 'cave': CLIFF}

WATER_MB = {0x11, 0x12, 0x13, 0x14, 0x15, 0x18, 0x1a, 0x22, 0x2a}
POND_MB = {0x10}                      # MB_POND_WATER - inland fresh water
SHALLOW_MB = {0x17}                   # MB_SHALLOW_WATER - walkable, not surf
SAND_MB = {0x06, 0x21}
TALL_MB = {0x02, 0x03, 0x09, 0x24}    # tall, long and ash grass
MOUNTAIN_MB = {0x0c}                  # MB_MOUNTAIN_TOP. Checked against the
                                      # header: 0x20 is MB_ICE and 0x38/0x39
                                      # are ledges, which an earlier guess had
                                      # in here reading as cliff

def behaviors(tileset):
    p = os.path.join(R.tileset_dir(tileset), 'metatile_attributes.bin')
    b = open(p, 'rb').read()
    return [b[i * 2] for i in range(len(b) // 2)]

class Classifier:
    """Assign a terrain class to a metatile id, for one primary/secondary pair."""
    def __init__(self, rend, prim, sec):
        self.r, self.prim, self.sec = rend, prim, sec
        self.mb = {}
        for kind, base in ((prim, 0), (sec, R.NUM_METATILES_IN_PRIMARY)):
            if kind:
                for i, v in enumerate(behaviors(kind)):
                    self.mb[base + i] = v
        self.memo = {}

    def avg(self, mid):
        im = self.r.metatile(self.prim, self.sec, mid)
        px = list(im.getdata())
        n = len(px)
        return tuple(sum(p[i] for p in px) // n for i in range(3))

    def __call__(self, mid, collision):
        key = (mid, collision)
        if key in self.memo:
            return self.memo[key]
        b = self.mb.get(mid, 0)
        if b in POND_MB:
            c = POND
        elif b in SHALLOW_MB:
            c = SHALLOW
        elif b in WATER_MB:
            c = WATER
        elif b in TALL_MB:
            c = TALL
        elif b in SAND_MB:
            c = SAND
        else:
            r, g, bl = self.avg(mid)
            green = g > r + 12 and g > bl + 12
            if collision:
                # a green blocker is a tree; anything else solid reads as cliff
                c = TREE if green else CLIFF
            elif b in MOUNTAIN_MB:
                c = PLATEAU            # walkable mountain top, not a wall
            elif green:
                c = GRASS
            elif r > 120 and g > 100 and bl < g:
                c = PATH               # the tan dirt and sand paths
            else:
                c = OTHER
        self.memo[key] = c
        return c

# --- noise ----------------------------------------------------------------
# Everything organic in the generated maps comes from here. A plain
# nearest-seed fill produces straight boundaries and rectangular blobs, which
# is exactly what a hand-drawn map never looks like, so boundaries get warped
# and vegetation gets clumped by fractal value noise rather than by thresholds
# on distance alone. It is deterministic: same seed, same map, every run.
def _hash(ix, iy, seed):
    n = (ix * 374761393 + iy * 668265263 + seed * 2654435761) & 0xFFFFFFFF
    n = ((n ^ (n >> 13)) * 1274126177) & 0xFFFFFFFF
    return ((n ^ (n >> 16)) & 0xFFFF) / 65535.0

def value_noise(x, y, freq, seed):
    fx, fy = x * freq, y * freq
    ix, iy = int(fx // 1), int(fy // 1)
    tx, ty = fx - ix, fy - iy
    sx, sy = tx * tx * (3 - 2 * tx), ty * ty * (3 - 2 * ty)
    a, b = _hash(ix, iy, seed), _hash(ix + 1, iy, seed)
    c, d = _hash(ix, iy + 1, seed), _hash(ix + 1, iy + 1, seed)
    return (a + (b - a) * sx) * (1 - sy) + (c + (d - c) * sx) * sy

def fbm(x, y, seed, octaves=4, freq=0.05):
    v = amp = 0.0
    a, f = 1.0, freq
    for i in range(octaves):
        v += a * value_noise(x, y, f, seed + i * 7919)
        amp += a
        a *= 0.5
        f *= 2
    return v / amp

# --- learning -------------------------------------------------------------
def mask3(cls, x, y, w, h, default):
    return tuple(cls[(min(max(y+dy, 0), h-1)) * w + (min(max(x+dx, 0), w-1))]
                 for dy in (-1, 0, 1) for dx in (-1, 0, 1))

def mask4(m3):
    return (m3[1], m3[3], m3[4], m3[5], m3[7])

GENERATED = os.path.join(HERE, '..', 'generated_maps.txt')

def generated():
    """the maps this project produced, which must never be learned from.

    Once they exist, R.solve() returns them alongside the vanilla ones, and a
    model trained on its own output drifts a little further from Hoenn every
    time it is rebuilt. newmaps.py writes the list."""
    if not os.path.exists(GENERATED):
        return set()
    return {l.strip() for l in open(GENERATED) if l.strip()}

BASELINE = os.path.join(HERE, '..', 'baseline')

def blockdata(name, L):
    """a vanilla map's blockdata as it was before this project touched it.

    generated() keeps the model off our own maps, but the vanilla maps whose
    borders were softened to meet them are still vanilla as far as R.solve()
    is concerned - so the model was learning from its own softening, and every
    rebuild moved a little. Reading the untouched copy makes the model a pure
    function of the vendored game: rebuild it any time and get the same maps.
    """
    p = os.path.join(BASELINE, f'{name}.bin')
    if os.path.exists(p):
        return open(p, 'rb').read()
    return open(f'{R.ROOT}/{L["blockdata_filepath"]}', 'rb').read()

def learn(maps_wanted=None, primary='gTileset_General'):
    """Walk vanilla maps and tally metatile choices per class neighbourhood."""
    lay, maps, pos = R.solve()
    skip = generated()
    rend = R.Renderer()
    t3 = collections.defaultdict(collections.Counter)
    t4 = collections.defaultdict(collections.Counter)
    t1 = collections.defaultdict(collections.Counter)
    # which metatiles vanilla ever sets side by side, and one above the other.
    # The 3x3 tables describe a cell's *class* surroundings, which is too
    # coarse to catch a seam: grass whose art has a rock edge on its right and
    # plain grass to its right are both "grass beside grass", and both are a
    # legal answer to the same mask. These say which of the legal answers
    # actually line up.
    ph = collections.Counter()
    pv = collections.Counter()
    used = []
    for k in sorted(maps_wanted or pos):
        if k not in maps or k in skip:
            continue
        L = lay[maps[k]['layout']]
        if L['primary_tileset'] != primary:
            continue
        w, h = L['width'], L['height']
        blk = blockdata(L['blockdata_filepath'].split('/')[-2], L)
        C = Classifier(rend, primary, L.get('secondary_tileset'))
        raw = []
        for i in range(w * h):
            o = i * 2
            raw.append((blk[o] | (blk[o+1] << 8)) if o + 1 < len(blk) else 0)
        # only learn from primary metatiles: a secondary id means something
        # local to that town and will not exist in the map we are painting
        cls = [C(v & 0x3FF, (v >> 10) & 3) for v in raw]
        for y in range(h):
            for x in range(w):
                v = raw[y * w + x]
                if (v & 0x3FF) >= R.NUM_METATILES_IN_PRIMARY:
                    continue
                m3 = mask3(cls, x, y, w, h, GRASS)
                t3[m3][v] += 1
                t4[mask4(m3)][v] += 1
                t1[m3[4]][v] += 1
                m = v & 0x3FF
                if x + 1 < w and (raw[y*w + x+1] & 0x3FF) < R.NUM_METATILES_IN_PRIMARY:
                    ph[(m, raw[y*w + x+1] & 0x3FF)] += 1
                if y + 1 < h and (raw[(y+1)*w + x] & 0x3FF) < R.NUM_METATILES_IN_PRIMARY:
                    pv[(m, raw[(y+1)*w + x] & 0x3FF)] += 1
        used.append(k)
    # class of every primary metatile at every collision, so the harmoniser can
    # tell whether a swap would change the terrain and not just the art
    CG = Classifier(rend, primary, None)
    cmap = {(m, c): CG(m, c)
            for m in range(R.NUM_METATILES_IN_PRIMARY) for c in range(4)}
    return {'t3': {k: dict(v) for k, v in t3.items()},
            't4': {k: dict(v) for k, v in t4.items()},
            't1': {k: dict(v) for k, v in t1.items()}, 'maps': used,
            'ph': dict(ph), 'pv': dict(pv), 'cls': cmap,
            'furniture': sorted(furniture(lay, maps, pos, skip))}

def best(table, key, avoid=()):
    d = table.get(key)
    if not d:
        return None
    ok = [kv for kv in d.items() if (kv[0] & 0x3FF) not in avoid]
    if not ok:
        return None
    return max(ok, key=lambda kv: kv[1])[0]

def furniture(lay, maps, pos, skip):
    """Metatiles that promise an interaction the generated maps do not have.

    Not guessed and not a rarity threshold - the signpost is used 112 times in
    vanilla, more than plenty of real terrain. A tile is furniture if it sits
    under a bg_event or a warp at least half the times it is used at all: 101
    of the signpost's 112 uses have a sign script behind them, and all ten of
    the blue secret-base cave mouth's do. Painting one into a new route puts a
    sign with nothing to read or a cave mouth with nothing behind it.
    """
    import glob
    hdr = {}
    for f in glob.glob(f'{R.ROOT}/data/maps/*/map.json'):
        j = json.load(open(f))
        hdr[j['id']] = j
    use, under = collections.Counter(), collections.Counter()
    for k in pos:
        if k in skip:
            continue
        L = lay[maps[k]['layout']]
        if L['primary_tileset'] != 'gTileset_General':
            continue
        w, h = L['width'], L['height']
        blk = blockdata(L['blockdata_filepath'].split('/')[-2], L)
        for i in range(w * h):
            m = (blk[i*2] | (blk[i*2+1] << 8)) & 0x3FF
            if m < R.NUM_METATILES_IN_PRIMARY:
                use[m] += 1
        for key in ('bg_events', 'warp_events'):
            for e in (hdr.get(k, {}).get(key) or []):
                try:
                    x, y = int(e['x']), int(e['y'])
                except (KeyError, TypeError, ValueError):
                    continue
                if not (0 <= x < w and 0 <= y < h):
                    continue
                m = (blk[(y*w + x)*2] | (blk[(y*w + x)*2 + 1] << 8)) & 0x3FF
                if m < R.NUM_METATILES_IN_PRIMARY:
                    under[m] += 1
    return {m for m in under if under[m] >= 0.5 * use[m]}

SWEEPS = 6

# Long grass - metatile 015, MB_LONG_GRASS - is the only one of its behaviour
# in the General tileset, and vanilla draws it on Route 119 and Route 120 and
# nowhere else: it is the rainy jungle's grass, and the south-edge tile that
# finishes a patch of it lives in those two maps' secondary tileset, which our
# routes do not load. The classifier calls it tall grass like any other, so the
# painter was mixing it cell by cell with the ordinary sort - 675 joins in the
# new maps that vanilla has never drawn once.
EXCLUDE = {0x015}

class Painter:
    def __init__(self, model):
        self.m = model
        self.avoid = set(model.get('furniture', ())) | EXCLUDE
        self.ph = model.get('ph', {})
        self.pv = model.get('pv', {})
        self.cmap = model.get('cls', {})

    CAP = 48

    def choices(self, cls, x, y, w, h):
        """every metatile vanilla used in this cell's situation, with weights.

        paint() takes the most popular answer to the exact 3x3 mask. The
        harmoniser needs more than that, and specifically it needs the coarser
        tables too: Route 144 had a cliff cell whose 3x3 mask had exactly one
        vanilla answer, and that answer was a sea cliff - a rock face with the
        ocean drawn onto its edge - which put a stripe of blue down the middle
        of a mountain thirty cells long. There was nothing to swap it for
        because the exact mask offered nothing else.

        So all three tables contribute, scaled so the exact match still wins
        wherever it fits: only when the exact answer makes a join vanilla has
        never drawn does a coarser one get to replace it.
        """
        m3 = mask3(cls, x, y, w, h, GRASS)
        out = collections.Counter()
        for scale, tab, key in ((1000, self.m['t3'], m3),
                                (10, self.m['t4'], mask4(m3)),
                                (10, self.m['t3'], (m3[4],) * 9),
                                (1, self.m['t1'], m3[4])):
            for v, n in (tab.get(key) or {}).items():
                if (v & 0x3FF) not in self.avoid:
                    out[v] += scale * n
        if not out:
            return {1: 1}
        return dict(out.most_common(self.CAP))

    def paint(self, cls, w, h):
        """class grid (list, row-major) -> list of u16 blockdata entries."""
        out = []
        for y in range(h):
            for x in range(w):
                m3 = mask3(cls, x, y, w, h, GRASS)
                # If vanilla never drew this arrangement, paint the cell as
                # though it were the middle of its own terrain. The obvious
                # fallback - that class's most common metatile - is wrong:
                # for a path it picks the mountain-top tile, whose art expects
                # a plateau edge, so a one-cell-wide path came out fringed
                # with rock. The homogeneous tile is the one that tiles.
                av = self.avoid
                v = (best(self.m['t3'], m3, av)
                     or best(self.m['t4'], mask4(m3), av)
                     or best(self.m['t3'], (m3[4],) * 9, av)
                     or best(self.m['t1'], m3[4], av) or 1)
                out.append(v)
        self.harmonise(out, cls, w, h)
        return out

    def seams(self, out, i, v, w, h):
        """how many of this cell's four joins are pairs vanilla never draws."""
        x, y, m = i % w, i // w, v & 0x3FF
        n = 0
        if x and (out[i-1] & 0x3FF, m) not in self.ph:
            n += 1
        if x + 1 < w and (m, out[i+1] & 0x3FF) not in self.ph:
            n += 1
        if y and (out[i-w] & 0x3FF, m) not in self.pv:
            n += 1
        if y + 1 < h and (m, out[i+w] & 0x3FF) not in self.pv:
            n += 1
        return n

    def harmonise(self, out, cls, w, h):
        """Swap cells for equally-legal alternatives that join up better.

        paint() decides every cell on its own, so two cells can each be the
        right answer to their own 3x3 mask and still not line up where they
        meet. This re-picks from the same candidate set - so the terrain never
        changes, only which drawing of it is used - choosing whichever
        candidate leaves the fewest joins vanilla has never drawn.

        A swap must keep the cell's class and its collision: the point is to
        fix the art, and moving a wall or a shore would undo work that
        reachability and the encounter tables depend on.
        """
        cand = {}
        moved = 0
        for _ in range(SWEEPS):
            n = 0
            for i in range(w * h):
                v = out[i]
                if not self.seams(out, i, v, w, h):
                    continue
                if i not in cand:
                    cand[i] = self.choices(cls, i % w, i // w, w, h)
                col, kc = v & 0x0C00, self.cmap.get((v & 0x3FF, (v >> 10) & 3))
                # ties go to the cell as it stands: a swap has to earn itself
                bestv, bestk = v, (self.seams(out, i, v, w, h), float('-inf'))
                for c, cnt in cand[i].items():
                    if c == v or (c & 0x0C00) != col:
                        continue
                    if self.cmap.get((c & 0x3FF, (c >> 10) & 3)) != kc:
                        continue
                    k = (self.seams(out, i, c, w, h), -cnt)
                    if k < bestk:
                        bestv, bestk = c, k
                if bestv != v:
                    out[i] = (bestv & 0x0FFF) | (v & 0xF000)
                    n += 1
            moved += n
            if not n:
                break
        return moved

MODEL = os.path.join(HERE, '..', 'terrain_model.pickle')

def load(rebuild=False, **kw):
    if not rebuild and os.path.exists(MODEL):
        return pickle.load(open(MODEL, 'rb'))
    m = learn(**kw)
    pickle.dump(m, open(MODEL, 'wb'))
    return m

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--rebuild', action='store_true')
    ap.add_argument('--report', action='store_true')
    a = ap.parse_args()
    m = load(rebuild=a.rebuild)
    print(f'learned from {len(m["maps"])} maps: '
          f'{len(m["t3"])} 3x3 patterns, {len(m["t4"])} 4-neighbourhoods')
    if a.report:
        for c in sorted(m['t1']):
            d = m['t1'][c]
            top = sorted(d.items(), key=lambda kv: -kv[1])[:8]
            tot = sum(d.values())
            print(f'  {CLASS_NAME[c]:11s} {tot:6d} cells   '
                  + ' '.join(f'{v&0x3FF:03X}/c{(v>>10)&3}' for v, _ in top))

if __name__ == '__main__':
    sys.exit(main())

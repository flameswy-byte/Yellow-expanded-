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
    # ...and the same thing again, per secondary tileset, keeping the secondary
    # metatiles this time. A secondary id means nothing on its own - 0x251 is a
    # different picture in every tileset - but it means exactly the same thing
    # on two maps that load the same one, and our maps do load vanilla's. Route
    # 111's desert floor is 92% metatile 251 out of gTileset_Mauville and only
    # 8% anything from General; ours, painted from the primary alone, was 2,376
    # cells of the beach tile. Route 143 has Lavaridge's volcanic rock
    # available to it and was drawing plain grey cliffs, which is 82% of what
    # vanilla puts on the maps that load it.
    S = lambda: dict(t3=collections.defaultdict(collections.Counter),
                     t4=collections.defaultdict(collections.Counter),
                     t1=collections.defaultdict(collections.Counter),
                     ph=collections.Counter(), pv=collections.Counter(),
                     cls={}, maps=[])
    bysec = collections.defaultdict(S)
    used = []
    for k in sorted(maps_wanted or pos):
        if k not in maps or k in skip:
            continue
        L = lay[maps[k]['layout']]
        if L['primary_tileset'] != primary:
            continue
        w, h = L['width'], L['height']
        sec = L.get('secondary_tileset')
        blk = blockdata(L['blockdata_filepath'].split('/')[-2], L)
        C = Classifier(rend, primary, sec)
        raw = []
        for i in range(w * h):
            o = i * 2
            raw.append((blk[o] | (blk[o+1] << 8)) if o + 1 < len(blk) else 0)
        cls = [C(v & 0x3FF, (v >> 10) & 3) for v in raw]
        B = bysec[sec] if sec else None
        if B is not None:
            B['maps'].append(k)
        for y in range(h):
            for x in range(w):
                v = raw[y * w + x]
                m3 = mask3(cls, x, y, w, h, GRASS)
                m = v & 0x3FF
                if B is not None:
                    B['t3'][m3][v] += 1
                    B['t4'][mask4(m3)][v] += 1
                    B['t1'][m3[4]][v] += 1
                    if m >= R.NUM_METATILES_IN_PRIMARY:
                        B['cls'][(m, (v >> 10) & 3)] = cls[y * w + x]
                    # only joins involving one of this tileset's own metatiles:
                    # a join between two primary tiles is the same everywhere,
                    # and letting six maps' worth of them into this table just
                    # tells the harmoniser that more seams are fine than are
                    if x + 1 < w:
                        n = raw[y*w + x+1] & 0x3FF
                        if m >= R.NUM_METATILES_IN_PRIMARY or n >= R.NUM_METATILES_IN_PRIMARY:
                            B['ph'][(m, n)] += 1
                    if y + 1 < h:
                        n = raw[(y+1)*w + x] & 0x3FF
                        if m >= R.NUM_METATILES_IN_PRIMARY or n >= R.NUM_METATILES_IN_PRIMARY:
                            B['pv'][(m, n)] += 1
                # the tileset-agnostic tables stay primary-only: a secondary id
                # in them would be painted onto a map that does not load it
                if m >= R.NUM_METATILES_IN_PRIMARY:
                    continue
                t3[m3][v] += 1
                t4[mask4(m3)][v] += 1
                t1[m3[4]][v] += 1
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
    furn = furniture(lay, maps, pos, skip)
    return {'t3': {k: dict(v) for k, v in t3.items()},
            't4': {k: dict(v) for k, v in t4.items()},
            't1': {k: dict(v) for k, v in t1.items()}, 'maps': used,
            'ph': dict(ph), 'pv': dict(pv), 'cls': cmap,
            'sec': {s: {'t3': {a: dict(b) for a, b in B['t3'].items()},
                        't4': {a: dict(b) for a, b in B['t4'].items()},
                        't1': {a: dict(b) for a, b in B['t1'].items()},
                        'ph': dict(B['ph']), 'pv': dict(B['pv']),
                        'cls': B['cls'], 'maps': B['maps']}
                    for s, B in bysec.items()},
            'furniture': sorted(furn.get(None, ())),
            'sec_furniture': {s: sorted(v) for s, v in furn.items() if s}}

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

    Returns one set per tileset: None for the primary ids, and one per
    secondary tileset for its own. The secondary sets matter more than the
    primary one - doors, cave mouths and gate fronts nearly all live there.
    """
    import glob
    hdr = {}
    for f in glob.glob(f'{R.ROOT}/data/maps/*/map.json'):
        j = json.load(open(f))
        hdr[j['id']] = j
    use = collections.defaultdict(collections.Counter)
    under = collections.defaultdict(collections.Counter)
    for k in pos:
        if k in skip:
            continue
        L = lay[maps[k]['layout']]
        if L['primary_tileset'] != 'gTileset_General':
            continue
        w, h = L['width'], L['height']
        sec = L.get('secondary_tileset')
        blk = blockdata(L['blockdata_filepath'].split('/')[-2], L)
        who = lambda m: None if m < R.NUM_METATILES_IN_PRIMARY else sec
        for i in range(w * h):
            m = (blk[i*2] | (blk[i*2+1] << 8)) & 0x3FF
            if who(m) is not None or m < R.NUM_METATILES_IN_PRIMARY:
                use[who(m)][m] += 1
        for key in ('bg_events', 'warp_events'):
            for e in (hdr.get(k, {}).get(key) or []):
                try:
                    x, y = int(e['x']), int(e['y'])
                except (KeyError, TypeError, ValueError):
                    continue
                if not (0 <= x < w and 0 <= y < h):
                    continue
                m = (blk[(y*w + x)*2] | (blk[(y*w + x)*2 + 1] << 8)) & 0x3FF
                if who(m) is not None or m < R.NUM_METATILES_IN_PRIMARY:
                    under[who(m)][m] += 1
    return {t: {m for m in under[t] if under[t][m] >= 0.5 * use[t][m]}
            for t in set(use) | set(under)}

SWEEPS = 6
PASSES = 4

# Long grass - metatile 015, MB_LONG_GRASS - is the only one of its behaviour
# in the General tileset, and vanilla draws it on Route 119 and Route 120 and
# nowhere else: it is the rainy jungle's grass, and the south-edge tile that
# finishes a patch of it lives in those two maps' secondary tileset, which our
# routes do not load. The classifier calls it tall grass like any other, so the
# painter was mixing it cell by cell with the ordinary sort - 675 joins in the
# new maps that vanilla has never drawn once.
EXCLUDE = {0x015}

class Painter:
    def __init__(self, model, secondary=None):
        self.m = model
        self.avoid = set(model.get('furniture', ())) | EXCLUDE
        self.ph = dict(model.get('ph', {}))
        self.pv = dict(model.get('pv', {}))
        self.cmap = dict(model.get('cls', {}))
        # the maps that load this same secondary tileset get a say of their
        # own, and their secondary metatiles come with them
        self.s = (model.get('sec') or {}).get(secondary)
        if self.s:
            self.avoid |= set((model.get('sec_furniture') or {})
                              .get(secondary, ()))
            self.ph.update(self.s['ph'])
            self.pv.update(self.s['pv'])
            self.cmap.update(self.s['cls'])
        # every metatile of a given terrain and collision, commonest first.
        # The 3x3 tables answer "what does vanilla draw in this situation";
        # this answers "what else could this cell be at all", which is what
        # finding a transition tile needs when the situation itself is one
        # vanilla never met.
        self.byclass = collections.defaultdict(list)
        seen = collections.Counter()
        for tab in (self.m['t1'],) + ((self.s['t1'],) if self.s else ()):
            for d in tab.values():
                for v, n in d.items():
                    if (v & 0x3FF) not in self.avoid:
                        seen[v] += n
        for v, n in seen.most_common():
            k = self.cmap.get((v & 0x3FF, (v >> 10) & 3))
            if k is not None:
                self.byclass[(k, v & 0x0C00)].append(v)

    CAP = 200

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
        out = collections.Counter()
        for scale, tab, key, _ in self.tables(cls, x, y, w, h):
            for v, n in (tab.get(key) or {}).items():
                if (v & 0x3FF) not in self.avoid:
                    out[v] += scale * n
        if not out:
            return {1: 1}
        return dict(out.most_common(self.CAP))

    def tables(self, cls, x, y, w, h):
        """the lookups for this cell, most specific first.

        A map that loads the same secondary tileset as some vanilla maps gets
        their answers ahead of the rest of Hoenn's at each level of precision,
        because they are the ones drawing this terrain with these tiles to
        hand. An exact 3x3 match anywhere still beats a 4-neighbourhood match
        from the same tileset - the mask is the more specific thing.
        """
        m3 = mask3(cls, x, y, w, h, GRASS)
        m4, hom, m1 = mask4(m3), (m3[4],) * 9, m3[4]
        s = self.s or {'t3': {}, 't4': {}, 't1': {}}
        return ((4000, s['t3'], m3, 1), (1000, self.m['t3'], m3, 0),
                (40, s['t4'], m4, 1), (10, self.m['t4'], m4, 0),
                (40, s['t3'], hom, 1), (10, self.m['t3'], hom, 0),
                (4, s['t1'], m1, 1), (1, self.m['t1'], m1, 0))

    def first(self, cls, x, y, w, h):
        """the pick before anything is known about the neighbours.

        Deliberately not the argmax of choices(): merging the tables lets a
        common approximate answer outvote a rare exact one, and doing that put
        two thousand joins of bare mountain top against plain grass into the
        new maps - vanilla has 45 in the whole game. The most specific table
        that has anything to say decides, and only if it has nothing does the
        next one get a turn.

        A tileset's own table only gets to pre-empt the global one when its
        answer is one of its own metatiles, and then only when that answer is
        what it usually does there. It exists to supply tiles the global table
        cannot reach - the desert floor, a volcanic rock face. Where its answer
        is an ordinary primary tile it is a handful of maps guessing at
        something all of Hoenn knows better, and letting it win on that put
        Route 143 from 2% of joins vanilla never draws to 7%.
        """
        P = R.NUM_METATILES_IN_PRIMARY
        for _, tab, key, mine in self.tables(cls, x, y, w, h):
            d = tab.get(key)
            if not d:
                continue
            if mine:
                own = {v: n for v, n in d.items()
                       if (v & 0x3FF) >= P and (v & 0x3FF) not in self.avoid}
                if own and max(own.values()) * 2 > sum(d.values()):
                    return max(own, key=own.get)
                continue
            v = best(tab, key, self.avoid)
            if v is not None:
                return v
        return 1

    def paint(self, cls, w, h):
        """class grid (list, row-major) -> list of u16 blockdata entries."""
        # Where vanilla never drew this arrangement, first() falls back to the
        # 4-neighbourhood and then to the cell as though it were the middle of
        # its own terrain. The obvious last resort - that class's most common
        # metatile - is wrong: for a path it picks the mountain-top tile, whose
        # art expects a plateau edge, so a one-cell-wide path came out fringed
        # with rock. The homogeneous tile is the one that tiles.
        out = [self.first(cls, x, y, w, h)
               for y in range(h) for x in range(w)]
        # the two passes feed each other: a two-cell repair opens single-cell
        # improvements next to it, and those open more repairs
        for _ in range(PASSES):
            if not self.harmonise(out, cls, w, h):
                break
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

    def harmonise(self, out, cls, w, h, cand=None):
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
        cand = {} if cand is None else cand
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
                fits = lambda c: ((c & 0x0C00) == col and c != v
                                  and self.cmap.get((c & 0x3FF,
                                                     (c >> 10) & 3)) == kc)
                # ties go to the cell as it stands: a swap has to earn itself
                bestv, best_n = v, self.seams(out, i, v, w, h)
                best_rank = float('-inf')
                for c, cnt in cand[i].items():
                    if not fits(c):
                        continue
                    n_c = self.seams(out, i, c, w, h)
                    if n_c < best_n or (n_c == best_n and -cnt < best_rank):
                        bestv, best_n, best_rank = c, n_c, -cnt
                if best_n:
                    # Nothing vanilla drew in this situation fits, because it
                    # never met this situation: there is no art between sand
                    # and grass, or between the desert floor and a field, since
                    # vanilla walls both in. Widen to every metatile of the
                    # same terrain and collision, commonest first, and take the
                    # first that joins up - which is how the desert's own edge
                    # tiles get found without anyone naming them.
                    for c in self.byclass.get((kc, col), ()):
                        if not fits(c):
                            continue
                        n_c = self.seams(out, i, c, w, h)
                        if n_c < best_n:
                            bestv, best_n = c, n_c
                            if not n_c:
                                break
                if bestv != v:
                    out[i] = (bestv & 0x0FFF) | (v & 0xF000)
                    n += 1
            moved += n
            if not n:
                break
        return moved + self.repair(out, w, h) + self.runs(out, w, h)

    def partners(self):
        """for each metatile, what vanilla will put on each side of it."""
        if getattr(self, '_part', None) is None:
            L = collections.defaultdict(set)
            Rt = collections.defaultdict(set)
            U = collections.defaultdict(set)
            D = collections.defaultdict(set)
            for a, b in self.ph:
                Rt[a].add(b)
                L[b].add(a)
            for a, b in self.pv:
                D[a].add(b)
                U[b].add(a)
            self._part = (L, Rt, U, D)
        return self._part

    def repair(self, out, w, h, rounds=3):
        """Fix the joins one cell at a time cannot.

        harmonise() swaps a cell only when that cell's own four joins get
        better, and swapping one cell changes only those four - so it descends
        to a local minimum and stops. It leaves 3,061 joins where a legal tile
        for one end does exist and taking it would spoil the other end.

        This moves both ends together. For each bad join it tries only the
        tiles vanilla actually puts on that side of the neighbour - a handful,
        straight out of the pair table - and then re-picks the neighbour to
        suit, keeping the pair if the two cells have fewer bad joins between
        them than before.
        """
        L, Rt, U, D = self.partners()
        fixed = 0
        for _ in range(rounds):
            n = 0
            for i in range(w * h):
                x, y = i % w, i // w
                for dx, dy in ((1, 0), (0, 1)):
                    if x + dx >= w or y + dy >= h:
                        continue
                    j = i + dx + dy * w
                    a, b = out[i] & 0x3FF, out[j] & 0x3FF
                    tab = self.ph if dx else self.pv
                    if (a, b) in tab:
                        continue
                    want_a = (L if dx else U)[b]
                    want_b = (Rt if dx else D)[a]
                    base = (self.seams(out, i, out[i], w, h)
                            + self.seams(out, j, out[j], w, h))
                    best = None
                    for who, other, pool in ((i, j, want_a), (j, i, want_b)):
                        v = out[who]
                        col = v & 0x0C00
                        kc = self.cmap.get((v & 0x3FF, (v >> 10) & 3))
                        for c in self.byclass.get((kc, col), ()):
                            if (c & 0x3FF) not in pool or c == v:
                                continue
                            keep = out[who]
                            out[who] = (c & 0x0FFF) | (v & 0xF000)
                            cost = (self.seams(out, i, out[i], w, h)
                                    + self.seams(out, j, out[j], w, h))
                            out[who] = keep
                            if cost < base and (best is None or cost < best[0]):
                                best = (cost, who, (c & 0x0FFF) | (v & 0xF000))
                    if best:
                        out[best[1]] = best[2]
                        n += 1
            fixed += n
            if not n:
                break
        return fixed

    RUN_CAP = 16        # candidate tiles per cell; 24 and 40 gain nothing

    def runs(self, out, w, h):
        """Re-solve whole runs of one terrain at a time, exactly.

        Two-cell repair still leaves 316 cliff-face joins and 209 where a cliff
        meets tall grass, every one of which has a legal tile available. They
        survive because a rock face is a sequence: fixing the join at one end
        of a five-cell wall needs all five to change together, and no move that
        looks at one or two cells can see that.

        A run of one terrain along one axis is a chain, so it solves exactly by
        Viterbi. Each cell may take any tile of its own terrain and collision;
        a tile costs one for each perpendicular neighbour vanilla would not put
        it beside, and a step from one tile to the next costs one if vanilla
        never draws that pair. Only runs that already contain a bad join are
        touched, and the run is only rewritten if it comes out strictly better.
        """
        total = 0
        for axis in (0, 1):
            step = 1 if axis == 0 else w
            tab = self.ph if axis == 0 else self.pv
            perp = self.pv if axis == 0 else self.ph
            pstep = w if axis == 0 else 1
            outer = h if axis == 0 else w
            length = w if axis == 0 else h
            for o in range(outer):
                base = o * w if axis == 0 else o
                k = 0
                while k < length:
                    i = base + k * step
                    key = (self.cmap.get((out[i] & 0x3FF, (out[i] >> 10) & 3)),
                           out[i] & 0x0C00)
                    n = 1
                    while k + n < length:
                        j = base + (k + n) * step
                        if (self.cmap.get((out[j] & 0x3FF, (out[j] >> 10) & 3)),
                                out[j] & 0x0C00) != key:
                            break
                        n += 1
                    if n >= 2 and any(
                            (out[base + (k+t) * step] & 0x3FF,
                             out[base + (k+t+1) * step] & 0x3FF) not in tab
                            for t in range(n - 1)):
                        total += self._solve(out, base, k, n, step, pstep,
                                             key, tab, perp, axis, w, h)
                    k += n
        return total

    def _solve(self, out, base, k, n, step, pstep, key, tab, perp, axis, w, h):
        pool = self.byclass.get(key, ())[:self.RUN_CAP]
        cells = [base + (k + t) * step for t in range(n)]
        cands = []
        for i in cells:
            c = [out[i]] + [v for v in pool if v != out[i]]
            cands.append(c)
        def side(i, v):
            """cost of this tile against the two neighbours off the run."""
            x, y = i % w, i // w
            c = 0
            for d in (-pstep, pstep):
                j = i + d
                if not (0 <= j < w * h):
                    continue
                # a vertical run's perpendicular neighbours are left and
                # right, and i-1 at the start of a row is the previous row's
                # last cell. That is the only wrap possible; the earlier guard
                # tested j % w != x, which is true of every horizontal
                # neighbour, so no vertical run ever paid for the joins it
                # broke - it added 45 bad joins to Route 148 while reporting
                # that it had saved 9.
                if axis == 1 and j // w != y:
                    continue
                a, b = (out[j] & 0x3FF, v & 0x3FF) if d < 0 else (v & 0x3FF,
                                                                  out[j] & 0x3FF)
                c += (a, b) not in perp
            return c
        # the joins at the two ends of the run are outside it and must still
        # be paid for, or the solver rewrites a wall to suit itself and breaks
        # both places it meets the rest of the map
        before = base + (k - 1) * step if k else None
        after = base + (k + n) * step if k + n < (w if axis == 0 else h) else None
        head = lambda v: ((out[before] & 0x3FF, v & 0x3FF) not in tab
                          if before is not None else 0)
        tail = lambda v: ((v & 0x3FF, out[after] & 0x3FF) not in tab
                          if after is not None else 0)
        INF = float('inf')
        cost = [[side(cells[0], v) + head(v) for v in cands[0]]]
        back = [[-1] * len(cands[0])]
        for t in range(1, n):
            row, br = [], []
            for v in cands[t]:
                bestc, bestp = INF, 0
                for p, u in enumerate(cands[t-1]):
                    c = cost[t-1][p] + ((u & 0x3FF, v & 0x3FF) not in tab)
                    if c < bestc:
                        bestc, bestp = c, p
                row.append(bestc + side(cells[t], v))
                br.append(bestp)
            cost.append(row)
            back.append(br)
        end = min(range(len(cands[-1])),
                  key=lambda p: cost[-1][p] + tail(cands[-1][p]))
        best = cost[-1][end] + tail(cands[-1][end])
        now = (sum(side(cells[t], out[cells[t]]) for t in range(n))
               + sum((out[cells[t]] & 0x3FF, out[cells[t+1]] & 0x3FF) not in tab
                     for t in range(n - 1))
               + head(out[cells[0]]) + tail(out[cells[-1]]))
        if best >= now:
            return 0
        seq, p = [], end
        for t in range(n - 1, -1, -1):
            seq.append(cands[t][p])
            p = back[t][p]
        for t, v in enumerate(reversed(seq)):
            i = cells[t]
            out[i] = (v & 0x0FFF) | (out[i] & 0xF000)
        return now - best


MODEL = os.path.join(HERE, '..', 'terrain_model.pickle')

def stale():
    """is the cached model older than the code or the maps that made it?

    It is a cache, it is not in the repository, and forgetting to rebuild it
    means the maps in the repository were painted by a model nobody can
    reproduce. That is not hypothetical: Littleroot's softened border was
    committed from a pickle built before the tileset tables existed, and a
    fresh clone regenerated 25 cells of it differently.
    """
    if not os.path.exists(MODEL):
        return True
    age = os.path.getmtime(MODEL)
    newer = [__file__, R.__file__, GENERATED]
    newer += [os.path.join(BASELINE, f) for f in os.listdir(BASELINE)] \
        if os.path.isdir(BASELINE) else []
    return any(os.path.exists(p) and os.path.getmtime(p) > age for p in newer)

def load(rebuild=False, **kw):
    if not rebuild and not stale():
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

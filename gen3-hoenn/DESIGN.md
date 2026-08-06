# Open Hoenn — Design & Survey

An open-world Pokémon Emerald romhack. Vanilla Hoenn's connected overworld
occupies **40.0%** of its own bounding box: 122,540 of 306,400 metatiles across
49 maps you can walk between. Everything here is in service of the other 60%.

Gap 1 is now built — four new maps, 15,360 metatiles — which takes it to
**45.0%** across 53 maps. See §4.

Companion to `../gen1-kanto/DESIGN.md`, which is the same exercise on Yellow.
Read that one for the working method; this one records what is different.

---

## 1. Build environment

Verified working, and it does not need a ROM.

```bash
apt-get install -y binutils-arm-none-eabi   # see below — this is the trap
git clone https://github.com/pret/agbcc
cd agbcc && ./build.sh && ./install.sh ../pokeemerald
cd ../pokeemerald && make -j4 && make compare
```

Success looks like:

```
pokeemerald.gba: OK
sha1sum -> f3ae088181bf583e55daf962a92bb46f4f1d07b7
```

**The trap:** agbcc fails building `libgcc1.a` with `mv: cannot stat
'tmplibgcc1.a'`, which looks like an agbcc problem and is not. Its libgcc rule
shells out to an ARM assembler and archiver, so it needs `arm-none-eabi`
binutils present first. Install those and it builds clean. The error names the
wrong thing entirely.

The built ROM is 14,929,764 bytes of 32 MB — **55% of the cartridge is free**,
against 166 KB free in Yellow.

---

## 2. Engine constraints

Measured from this source tree, not remembered.

| Constraint | Value | Where |
|---|---|---|
| Map buffer | **10,240 entries** | `sBackupMapData[MAX_MAP_DATA_SIZE]`, `src/fieldmap.c` |
| Border | **7 metatiles** | `MAP_OFFSET`, `include/fieldmap.h` |
| Max map size | **(w+15) × (h+14) ≤ 10240** | `gBackupMapLayout.width = width + MAP_OFFSET_W` |
| Metatiles per map | 512 primary / **1024 total** | `NUM_METATILES_IN_PRIMARY`, `NUM_METATILES_TOTAL` |
| Tiles | 512 primary / **1024 total** | `NUM_TILES_IN_PRIMARY` |
| Palettes | 6 primary / **13 total** | `NUM_PALS_IN_PRIMARY` |
| Collision | **2 bits per metatile**, stored | `MAPGRID_COLLISION_MASK 0x0C00` |
| Map IDs | 36 groups, largest holds 108 | `data/maps/map_groups.json` |

Workable single-map shapes:

```
 86 × 86   largest square      40 × 172   long and thin is fine
 80 × 93                      150 ×  48
100 × 75                      200 ×  33
```

The largest vanilla maps — Routes 124, 126, 127 — are 80×80, so vanilla already
runs near the ceiling.

### The three Gen 1 constraints that do not exist here

Each of these shaped every decision in the Kanto project:

**One neighbour per edge — gone.** Gen 1's `connection` names exactly one
neighbour per direction, which forces the whole world to be a planar partition.
Gen 3 allows several: Route 124's right edge has two neighbours, Route 111's
left edge has two.

**The 255-map-ID ceiling — gone.** Gen 1 addresses maps with a single byte, and
`NUM_MAPS <= LAST_MAP` became the binding constraint on how open Kanto could
get. Gen 3 uses group plus number.

**Collision you have to reverse-engineer — gone.** In Gen 1, collision is
derived from tile IDs, and working out *which* tile of a 2×2 quadrant a step
samples took a long detour through `LoadCurrentMapView`. Here it is two bits
stored per metatile.

### And one thing that is actively looser

**The world does not have to be globally consistent.** Vanilla ships three
reciprocal connection pairs whose offsets disagree — Verdanturf/Route 116,
Fallarbor/Route 114, Dewford/Route 107 — so Hoenn *cannot* be laid flat without
contradiction. Walking Verdanturf → Route 116 → back does not return you to the
same relative position. The engine resolves one transition at a time and never
notices.

`tools/hoenn_layout.py` therefore reports placement conflicts as information.
The Gen 1 equivalent treats them as errors, because there they are.

---

## 3. The survey

`python3 tools/hoenn_layout.py --chunk 64`

```
49 maps reachable by walking from Littleroot
world 800 × 383 = 306,400 metatiles; 122,540 used = 40.0%
total empty 183,860 = 45 chunks of 64×64
```

64×64 uses 6,162 of the 10,240 buffer, leaving room to go bigger where a region
wants it. At 80×80 the same space is about 29 chunks.

### Inland gaps — about 13 chunks

Holes between existing land routes, and the priority. Level bands are from
`land_mons` in `src/data/wild_encounters.json`; fishing and surfing are excluded
because they span the whole game and tell you nothing about where an area sits.

| # | Empty | Chunks | Biggest clean rect | Level band | Borders |
|---|---|---|---|---|---|
| 1 | 15,360 | 3.8 | ~56×112 | **2–4** | **Littleroot**, Route 103, and the water Routes 105/107/108 |
| 2 | 12,500 | 3.1 | ~80×88 | **2–14** | Route 103, 104, 116, 117, 110 |
| 3 | 12,120 | 3.0 | ~56×104 | **6–18** | Route 116, 114, 112, 113, **Lavaridge** |
| 5 | 5,600 | 1.4 | ~40×112 | **19–27** | Route 111, 119, 118 |
| 4 | 7,200 | 1.8 | ~40×112 | **24–28** | Route 119, 120, 123, **Fortree** |

**They form a difficulty ladder on their own.** Ordered by level band the gaps
run 2–4, 2–14, 6–18, 19–27, 24–28, which tracks Hoenn's own progression. Each
one can be built to suit its neighbourhood rather than needing a global answer
to the level-curve question, and they can be populated in that order.

Tileset context, which constrains what each can look like without new art:

- **Gap 1** — Petalburg and Dewford. Coastal: three of its five neighbours are
  water routes, so this is a shoreline gap, not a landlocked one. Also the only
  gap adjacent to the starting town.
- **Gap 2** — Petalburg, Rustboro, Mauville. The early-game corridor.
- **Gap 3** — Rustboro, Fallarbor, Lavaridge. Volcanic and ash terrain.
- **Gap 5** — Mauville and Fortree: the seam between Route 111's desert and
  Route 119's rainforest. A 40-wide north–south strip.
- **Gap 4** — Fortree and Lilycove. Rainforest.

### Open ocean — about 31 chunks

The three largest empty regions all border Routes 124–133. That is sea past the
coastline, and filling it with land would misread what it is.

| Empty | Chunks | Borders |
|---|---|---|
| 49,680 | 12.1 | Route 129, 130, 132, 133 |
| 40,400 | 9.9 | Route 123, 126, 110, Lilycove |
| 37,600 | 9.2 | Route 125, 124, 120, Lilycove |

**Decided:** a few small islands to break up the monotony, rather than trying to
fill it. The rest stays water. Each island is independent of the others and of
the inland work, so this can wait until the gaps are done.

Vanilla already layers underwater maps over surface ones via Dive — Underwater
Route 126 occupies the same world coordinates as Route 126. That is effectively
a second Z level costing no horizontal space, and worth exploiting rather than
working around.

---

## 4. Gap 1, built

Gap 1 is filled. Hoenn now fills **45.0%** of its bounding box, up from 40.0%.

The gap partitions exactly into four rectangles — 6,960 + 3,200 + 3,600 +
1,600 = 15,360, the gap's whole cell count — so nothing is left over and every
map fits the buffer with room to spare:

| Map | World | Size | Buffer | Faces |
|---|---|---|---|---|
| Route 135 | x40 y262 | 80×40 | 5,130 / 10,240 | Route 102, 105, the west coast |
| Route 136 | x40 y302 | 40×40 | 2,970 | Route 105, 106, the south-west corner |
| Route 137 | x80 y302 | 120×58 | 9,720 | Route 106–109, the south bay |
| Route 138 | x140 y242 | 60×60 | 5,550 | Route 103, 110, toward Slateport |

`python3 tools/newmaps.py` builds all four and wires them in: blockdata,
border, layout entry, map header, group registration, `MAPSEC`, an empty
`scripts.inc`, and both halves of every connection. It is idempotent.

### Where the terrain comes from

Nothing is invented and nothing is hand-placed.

- **The rim comes from the neighbours.** Every boundary cell is seeded with the
  terrain class of the vanilla metatile immediately across that boundary. A
  coastline therefore arrives where the map meets Route 105 and grass where it
  meets Route 102, and the seams line up because they were copied.
- **The regions come from the sketch.** Area pens seed a nearest-seed fill;
  the path pen is stamped over the result, because a path is a line, not a
  region. The sketch had no sand pen, so the wide path stroke drawn against
  Route 111's desert is read as sand rather than road.
- **The metatiles come from vanilla.** `tools/terrain.py` reads every vanilla
  map, classifies each metatile into a coarse terrain class, and records which
  metatile the game used for each 3×3 arrangement of classes. Painting is a
  lookup, so a grass-meets-water seam gets whatever vanilla uses in that exact
  situation. Nine thousand patterns were learned from 49 maps.

### The five rules, and how each is enforced

1. **Paths must be walkable end to end.** Path cells are stamped last so
   nothing overwrites them, and no tree or cliff is allowed within two cells
   of one. `tools/check_seams.py` then confirms it from the built data.
2. **No straight lines.** Two halves. The generated boundaries are domain
   warped through fractal noise, which bends every nearest-seed bisector into
   something meandering; the amplitude tapers to zero at the rim so the seams
   still match. And the *old* maps' bounding-box lines get feathered — see
   below.
3. **Vegetation grades outward from the path.** Distance is measured from
   where the player actually walks, and open ground gives way to tall grass,
   then scattered trees, then closed canopy as it grows. The clumping is
   noise rather than a radius, so no band comes out as a ring, and nothing
   taller than open ground is ever placed beside a path.
4. **Cliffs stay climbable.** Not exercised yet — Gap 1 has almost no cliff.
   It binds on Gap 3, which is volcanic.
5. **The desert swath is sand.** Recorded in `DESERT_BOX`; it lands in Gap 5.

### Softening the old borders

Every vanilla map ends in a hard line of trees or rock, because it used to end
at nothing. Where one now faces new land, that line is the seam showing. So it
is feathered: the outermost row survives only where the noise runs high, the
row four cells in survives almost everywhere, and a few trees are added back
further in to round the edge off. **512 vanilla metatiles across nine map
edges** were rewritten.

Three constraints keep that honest. Only the span actually facing new land is
touched — Route 103's edge is softened where it meets Route 138 and left alone
where it meets Oldale. Cells within one tile of any event are skipped, as are
cells drawing from a secondary tileset, which is where town furniture lives.
And a cell is only repainted if its 3×3 *class* neighbourhood changed, so
vanilla's hand-placed detail survives everywhere the softening did not reach.

The pristine blockdata lives in `baseline/`, outside the vendored tree, and
the pass always reads from there — otherwise running it twice would erode the
border a little further each time.

### What is deliberately not connected

Littleroot, Oldale, Petalburg and Slateport all border these maps and none of
them is connected. Opening a town edge changes which coordinates the player
can reach during that town's scripted sequences, which is the mistake that
cost the most in the Kanto project (`../gen1-kanto/DESIGN.md` §5). Route 101
is skipped for the same reason: `VAR_ROUTE101_STATE` confines the player
during the Birch rescue and only guards the exits vanilla knows about.

The new land is still walkable from a new game — via Route 102 — so nothing is
lost by waiting.

### Verification

```
make                         -> builds; sha1 differs from vanilla, as it must
tools/check_seams.py         -> 0 blocked connections among the new maps
                                6 remain, all vanilla: Route 112/113, 114/115,
                                and Route 116/Verdanturf, which link by tunnel
                                walk       reaches 26/53 outdoor maps
                                walk+surf  reaches 52/53
                                all four new maps walkable from the start
```

`check_seams.py` is the tool that matters. A connection in a map header only
says two maps are adjacent; whether the player can cross it depends on the
blockdata, and a connection with no crossable cell is a wall that looks like a
door. Nothing in the build catches that. It caught one: Route 138 → Route 110
was declared and impassable, because Route 110's west edge is a solid tree
column. Softening opened it.

Still missing on these maps: **wild encounters**. The tall grass is real
terrain but no `wild_encounters.json` entry exists, so nothing lives in it yet.

---

## 5. Open questions

- **What goes in the remaining inland gaps.** Gap 1 is built; Gaps 2–5 are
  about nine chunks of ground and nothing is designed yet.
- **Wild encounters.** The new maps have tall grass and nothing in it.
- **Region map.** The four new `MAPSEC`s have names but no region-map
  rectangle, so they do not light up on the town map.
- **What the ocean is for.** Thirty-one chunks of sea. Vanilla already uses
  Dive to layer underwater maps over surface ones, which is a mechanic worth
  exploiting rather than working around.
- **Level curve.** Same question the Kanto project parked: an open world means
  the player can arrive anywhere at any level.
- **Whether to use Porymap.** It is the mature editor for exactly this format,
  so there is no reason to build another one.

# Open Hoenn — Design & Survey

An open-world Pokémon Emerald romhack. Vanilla Hoenn's connected overworld
occupies **40.0%** of its own bounding box: 122,540 of 306,400 metatiles across
49 maps you can walk between. Everything here is in service of the other 60%.

All five inland gaps are now built — **14 new maps, 51,460 metatiles** — which
takes it to **56.8%** across 63 maps. See §4.

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

## 4. The gaps, built

Every inland gap is filled. Hoenn now fills **56.8%** of its bounding box, up
from 40.0%, across 63 walkable maps instead of 49.

Gap 1 happened to partition exactly into four rectangles — 6,960 + 3,200 +
3,600 + 1,600 = 15,360, its whole cell count. The others do not, so
`tools/plan_gaps.py` does it properly: take the largest buffer-legal rectangle
that fits entirely inside the empty region, carve it out, repeat until what is
left is too small to be worth a map header. Ten more maps, covering 96% of the
remaining 37,420 cells; the leftover slivers stay empty rather than becoming
300-cell maps.

| Map | World | Size | Buffer | Faces |
|---|---|---|---|---|
| Route 135 | x40 y262 | 80×40 | 5,130 / 10,240 | Route 102, 105, the west coast |
| Route 136 | x40 y302 | 40×40 | 2,970 | Route 105, 106, the south-west corner |
| Route 137 | x80 y302 | 120×58 | 9,720 | Route 106–109, the south bay |
| Route 138 | x140 y242 | 60×60 | 5,550 | Route 103, 110, toward Slateport |
| Route 139 | x40 y160 | 123×60 | 10,212 | Rustboro, Verdanturf, Route 103/104/117 |
| Route 140 | x163 y160 | 37×60 | 3,848 | Route 103, 110, 117 |
| Route 141 | x40 y142 | 80×18 | 3,040 | Rustboro, Verdanturf, Route 116 |
| Route 142 | x70 y220 | 50×22 | 2,340 | Petalburg, Route 102, 103 |
| Route 143 | x40 y82 | 160×40 | 9,450 | Route 111, 114, 115, 116 |
| Route 144 | x80 y20 | 60×62 | 5,700 | Fallarbor, Route 113, 114 |
| Route 145 | x140 y122 | 60×18 | 2,400 | Route 111, 116, 117 |
| Route 146 | x320 y20 | 40×120 | 7,370 | Fortree, Route 119, 120, 123 |
| Route 147 | x360 y100 | 60×40 | 4,050 | Route 120, 121, 122, 123 |
| Route 148 | x240 y0 | 40×140 | 8,470 | Route 111, 118, 119 — the desert seam |

`python3 tools/newmaps.py` builds all fourteen and wires them in: blockdata,
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

1. **Paths must be walkable end to end.** One cell wide, drawn as a line
   between the sketch's sampled points so they do not come out dashed. Stamped
   last so nothing overwrites them, with a single cell of clearance either
   side. `tools/check_seams.py` then confirms it from the built data.
2. **No straight lines.** Two halves. The generated boundaries are domain
   warped through fractal noise, which bends every nearest-seed bisector into
   something meandering; the amplitude tapers to zero at the rim so the seams
   still match. And the *old* maps' bounding-box lines get feathered — see
   below. Scattered single trees come from a second, much higher frequency
   field, because the gradient's own noise only ever produces trees as the
   dense core of a clump.
3. **Vegetation grades outward from the path.** Distance is measured from
   where the player actually walks, and open ground gives way to tall grass,
   then scattered trees, then closed canopy as it grows. The clumping is
   noise rather than a radius, so no band comes out as a ring, and nothing
   taller than open ground is ever placed beside a path.
4. **Cliffs stay climbable.** Not exercised yet — Gap 1 has almost no cliff.
   It binds on Gap 3, which is volcanic.
5. **The desert swath is sand.** Recorded in `DESERT_BOX`; it lands in Gap 5.

### Three things a per-cell painter cannot see

The painter chooses each metatile from its own 3×3 neighbourhood, which leaves
three classes of defect that only show up at map scale.

**An unseen arrangement needs the right fallback.** Narrowing paths to one cell
produced something vanilla never draws — a path cell with grass on all sides —
so the lookup fell through to "that class's most common metatile", which for a
path is the mountain-top tile. Its art expects a plateau edge, and every
one-wide path came out fringed with pink rock. The fallback is now the
*homogeneous* tile: if vanilla never drew this arrangement, paint the cell as
though it were the middle of its own terrain. That is the tile that tiles.

**Stray ledges and stray elevations are invisible walls.** `MB_JUMP_*` ledges
are drawn in vanilla only as long runs; the painter will emit a single one
wherever a height change happens to look like the top of one, and a lone ledge
is a one-way wall in an open field. Likewise a walkable cell whose elevation
disagrees with everything around it is a step the player cannot take, for no
reason the map shows. `tidy()` removes ledge runs shorter than three and
snaps an isolated elevation to its neighbours' — 136 ledges and 35 elevations
across the fourteen maps.

**Scattering trees can strand a pocket.** `repair_connectivity()` floods
everything walkable and cuts a one-cell corridor from any sizeable pocket back
to the main body, choosing the thinnest wall by 0-1 BFS. Water is treated as a
moat rather than a wall, so it never builds a land bridge the sketch did not
ask for.

While fixing the ledges, two behaviour constants turned out to be wrong in the
classifier: `MOUNTAIN_MB` held `0x20`, `0x38` and `0x39`, which are actually
`MB_ICE`, `MB_JUMP_EAST` and `MB_JUMP_WEST`. `MB_MOUNTAIN_TOP` is `0x0c`.
Ledges had been reading as cliff.

**The model must not learn from its own output.** Once the new maps exist,
`R.solve()` returns them alongside the vanilla ones, and a rebuild trained on
63 maps instead of 49 — drifting a little further from Hoenn every time.
`newmaps.py` now writes `generated_maps.txt` and `terrain.py` skips those.

### Measuring vanilla, and matching it

`tools/study.py` measures every vanilla land route — 21 of them, towns and sea
routes excluded — and prints ours against the same yardstick. Composition is
reported as a share of each map's **land**, not of the whole map: a route that
is half sea is not short of grass, it just has less ground to put it on.

The generator had been tuned by eye against single crops, which is exactly how
you end up with a route that is 69% tall grass and looks fine in a screenshot.

| | vanilla median | before | after |
|---|---|---|---|
| tall grass, share of land | 8.6% | 22.0% | **9.5%** |
| trees, share of land | 31.7% | 17.7% | **31.2%** |
| tall grass patches | 6.2/map, median 13 cells | 12.4/map, median 7, one of 2393 | **7.6/map, median 7** |
| tree clumps | 30.2/map, median 2 | 37.6/map, median 2 | **31.1/map, median 4** |
| tall grass touching walkable ground | 30.5% | 31.0% | 33.2% |

So: two and a half times too much tall grass, half the trees, and a couple of
sketch strokes turned into a slab no vanilla route comes near.

Rather than tune the thresholds again, `vegetate()` now **targets the counts
directly** — score every eligible cell, then take exactly as many as the
target calls for. Density stops depending on how the noise happens to fall on
that particular map. Trees mix a low-frequency field for the masses with a
high-frequency one for the scattered singles, which reproduces vanilla's shape:
about thirty clumps a map, median size 2, with a few very large ones.

Getting the *structure* right took four goes, and each failure was a real bug:

1. **Trees were placed before grass.** A third of them are scattered singles,
   so they riddled every grass blob into two-cell fragments — 33 patches a map
   where vanilla has 6. Choosing the grass first and keeping trees out of it is
   what makes a patch a patch.
2. **The old gradient pass was still running.** `vegetate()` replaced it but it
   was left in, so it had already scattered trees through the ground the
   patches were being chosen from.
3. **Distance was measured only from the sketch's own paths.** The region fill
   also spreads path inward from a rim seed where a vanilla neighbour meets the
   map on a path, and grass grew right up against those.
4. **Only the eligible tall grass was cleared before reselecting.** The cells
   beside a path kept their class from the region pass — 273 of Route 139's
   fragments on their own. That map went from 133 patches of median 1 to 18 of
   median 12.

The lesson is the one this project keeps relearning: a single crop cannot tell
you a map is wrong. Route 135 was fine at every stage; Route 139 was two
orders of magnitude off and looked much the same.

### How vanilla draws a mountain

`tools/study.py` and a walk over the elevation bits answered this. Vanilla does
not draw a mountain as a flat impassable blob — it draws **terraces**.

Route 115 has ground at elevation 3 and plateaus at 5. Route 114 stacks 3, 4, 5
and 7. Route 120 uses 3 and 5, Route 119 uses 3 and 4. Each terrace is a
walkable top ringed by impassable rock at elevation 0, and the only way up is a
handful of ordinary walkable tiles *also* left at elevation 0 — six of them on
the whole of Route 115, all `MB_NORMAL`.

The mechanism is `elev_ok`: two cells at different non-zero elevations cannot be
walked between, but elevation 0 is compatible with anything. So a terrace is
made by elevation, not by the metatile — vanilla puts plain grass (`0x001`) at
elevation 5 on a summit, and the same tile at 3 on the ground below.

Ours had none of it. Every generated map used elevations 0, 1 and 3 only, and
every cliff was solid:

```
ROUTE143   3,719 impassable cells,     0 walkable top
ROUTE148   2,401 impassable cells,     0 walkable top
```

A mountain you can only walk around is a wall.

`terrace()` now rebuilds them. Every cliff mass of 80 cells or more is eroded:
the interior becomes a walkable plateau at elevation 5, and if a further
erosion still leaves a worthwhile area, a second terrace at 7 sits inside a
one-cell wall. `cut_stairs()` then opens the way up — a wall cell that touches
the terrace on one side and lower ground on the other becomes an ordinary
walkable tile at elevation 0, which is exactly what vanilla's connectors are.
Stairs are placed at the two points furthest apart, which is the earlier rule
about cliffs needing at least two access points on opposite ends.

```
ROUTE143   2,652 walkable terrace cells at 5 and 7, 12 stairs, 100% reachable
ROUTE148   1,737                                     8 stairs, 100% reachable
ROUTE144   1,125                                     6 stairs, 100% reachable
```

Two things this needed:

**A new terrain class.** The classifier had been calling a walkable mountain
top and a solid rock face the same thing, so the painter could never draw the
difference. `PLATEAU` is now separate from `CLIFF`, and relearning splits
cleanly: 1,713 plateau cells (`071/c0`) against 20,840 cliff (`071/c1`, `073`,
`07C`).

**Elevation applied separately from art.** Since elevation is orthogonal to the
metatile, `apply_levels()` stamps it on after painting rather than hoping the
learned model produces the right one. The map's outermost ring is left alone —
those cells were copied from the neighbour across the seam and have to keep
matching it.

The wall between terraces has to be exactly one cell. At two cells thick no
single stair can touch both levels, and the upper terrace came out at 26%
reachable — the lower band was fine, so the map looked right and was not.

### Three more polish passes

**Staircases, not notches.** Vanilla's connector is a horizontal pair —
`0x0AF` left, `0x0CF` right — laid at elevation 0 with a different level above
and below. Route 115 uses eight such pairs and nothing else. `cut_stairs()`
now looks for a two-cell horizontal site and stamps the real art; the
single-cell fallback it used before painted plain grass, which showed up as a
green speck in the middle of a brown mountain. 30 of the 35 stairs are now
proper staircases.

**Nothing ships unreachable.** The prettiest stair site is not always a working
one, and Route 144 came out with a terrace at 88% reachable. `ensure_reachable()`
now floods the map the way the player would — respecting elevation — and opens a
plain notch into anything still stranded. All 14 maps verify at 100%.

**Terraces are not bare rock.** Route 115's plateaus are about half plain grass
with patches of long grass on top. `vegetate_terraces()` runs after the terracing
and puts grass on the summits, keeping each cell's elevation — a grass tile at
elevation 5 is exactly what vanilla puts on a plateau, and dropping it to 3
would sink the terrace into the map.

### Ledges

Vanilla's ledge is `0x087`, `MB_JUMP_SOUTH`, collision 1 — you hop south over
it and cannot come back. The surprise is where they go: **179 of them have
ordinary grass at elevation 3 both above and below**, so they are not a way off
a cliff at all, they are shortcuts across flat ground. Runs are horizontal,
median 4 cells, and 34 vanilla routes carry 409 ledge cells between them, 12 to
a map.

`place_ledges()` finds horizontal stretches of flat ground with walkable ground
above and below at the same elevation, takes three per map spaced well apart,
and cuts each to a length drawn from noise. Taking the longest run available
every time gave every ledge the same length and twice vanilla's density by
area. Ours now: 12 per map, median run 4, matching.

They are stamped **after** `tidy()`, so the stray-ledge threshold there can be
raised to four without eating the deliberate ones.

### A terrace has one surface

Grass was being speckled across the plateaus cell by cell. That produced **515
cells where grass met bare mountain top; vanilla has 45 in the whole game**, and
since both sides are flat fill tiles with nothing between them, every one was a
hard arbitrary edge.

Vanilla's rule is per-terrace, not per-cell: some plateaus are rock all over,
others are grass all over with patches of long grass on them, and the two kinds
sit on different terraces — Route 115's plateaus come out about half and half by
area. `vegetate_terraces()` now decides each connected terrace's surface as a
whole. Down to 16.

The rock-wall base variants were checked at the same time and were already
right: vanilla puts `RockWall_GrassBase` on grass and `_RockBase` on rock, and
so did we, because the learned model had picked that up on its own.

### Verify on the bytes that ship

`terrace()` and `ensure_reachable()` work on the class grid, but `tidy()`,
`apply_levels()` and the ledges all run afterwards and can move a cell. Checking
the class grid said every terrace was reachable; checking the **blockdata**
found five maps where it was not — mostly single stray cells left at elevation
5 in the middle of ordinary ground, and two real pockets.

`final_check()` now floods the finished blockdata the way the player would.
Pockets of eight cells or fewer are strays and get snapped down to ground level;
anything larger gets a notch opened into it. Maps with an unreachable terrace,
measured on the bytes that go in the ROM: **0**.

### Furniture the map cannot honour

The painter was emitting signposts, doors and secret-base cave mouths, because
vanilla uses them in 3×3 neighbourhoods that also occur in a generated route. A
sign with nothing to read is litter; a cave mouth with nothing behind it is
worse, because the player will walk into it.

Neither a rarity threshold nor the behaviour byte finds these. The signpost is
used 112 times in vanilla, more than plenty of real terrain, and its behaviour
is `MB_NORMAL`. What identifies it is that **101 of those 112 uses sit under a
`bg_event`**. So a metatile counts as furniture if it appears under a `bg_event`
or `warp_event` at least half the times it is used at all, which derives exactly
18 of them:

```
003 01B 021 026 027 041 042 043 061 062 063 0A7 131 1A0 1A8 1B0 1CD 1DB
   signpost      doors and their surrounds      secret-base cave mouths
```

The painter now refuses them and takes the next best metatile for the same
neighbourhood. Count remaining across all fourteen maps: zero.

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

### The towns, and the scripts that had to move with them

Littleroot, Oldale, Petalburg, Slateport and Route 101 are all connected.
Opening a town edge changes which coordinates the player can reach during that
town's scripted sequences — the mistake that cost the most in the Kanto
project (`../gen1-kanto/DESIGN.md` §5) — so every vanilla confinement was found
first and re-implemented at the new exits.

**No terrain work was needed.** Hoenn's town maps already draw walkable grass
right to their borders; those edges were closed only by the absence of a
connection. Every one of the nine new town seams had crossable cells the
moment the connection existed.

| Town | New exits | What vanilla blocks, and where |
|---|---|---|
| Littleroot | west, east, south | a twin warns you off the north exit while `VAR_LITTLEROOT_TOWN_STATE` is 0 |
| Oldale | east | the footprints man blocks the west exit while `VAR_OLDALE_TOWN_STATE` is 0 |
| Route 101 | west, east | `VAR_ROUTE101_STATE == 2` pens you into a box during the Birch rescue |
| Petalburg | south | nothing — reaching Petalburg already needs a party |
| Slateport | west ×2 | nothing — its west edge is open ocean, so that seam is a surf |

Three findings shaped the guards:

**Littleroot's real condition is not a state, it is an empty party.** Vanilla
gates the north exit on `VAR_LITTLEROOT_TOWN_STATE == 0`, but at state 1 you
have been told to go save Birch and still own nothing. In vanilla that is safe
because north is the only way out and Route 101's trigger fires the moment you
step on it. With three more exits it is not safe — you would walk into tall
grass with no party. The new gates test **`FLAG_SYS_POKEMON_GET`** instead,
which is the condition that actually matters and outlasts both states.

**The vanilla blockers cannot be reused.** Littleroot's is a twin who walks
over to you and Oldale's is the footprints man stepping aside; both are tied
by `LOCALID` to their own tile. Firing either from across the map would look
broken. Each new exit gets a self-contained guard instead — message, one step
back, release — modelled on Route 101's own `PreventExit` scripts.

**Route 101's rescue box had a hole.** Vanilla guards its west wall with
triggers at x=6 covering rows 15–18. Row 14 is walkable west all the way to
x=0, and was a dead end until this connection existed. Guarding the whole
outermost column closes it.

The guards are generated, not hand-written: 40 triggers on Littleroot, 4 on
Oldale, 19 on Route 101, placed on every cell of each new edge the player can
stand on, with the scripts written into each map's `scripts.inc` between
markers so re-running rewrites them in place.

The party guard fires on `VAR_TEMP_2 == 0`, which is vanilla's always-fires
idiom (`AquaHideout_B2F` uses it), and the script tests the flag and falls
through to a bare `end` once you have a Pokémon — no lock, no message.

**Left open on purpose:** the Oldale gate is now bypassable. A player can go
Route 101 → west into Route 135 → north to Route 102 and reach Petalburg
without ever triggering the Route 103 rival battle. Nothing softlocks — the
Pokédex comes from Birch's lab, which is always open — but it is the
level-curve question arriving early, and it is a design decision rather than a
bug to fix.

### Verification

```
make                         -> builds; sha1 differs from vanilla, as it must
tools/check_seams.py         -> 0 blocked connections among the new maps
                                10 remain, every one vanilla: Route 112/113,
                                114/115 and Route 116/Verdanturf, which link by
                                tunnel, and the four Underwater route seams
                                walk       reaches 27/53 outdoor maps
                                walk+surf  reaches 52/53
                                all four new maps, and all five newly
                                connected vanilla maps, walkable from the start
```

`check_seams.py` is the tool that matters. A connection in a map header only
says two maps are adjacent; whether the player can cross it depends on the
blockdata, and a connection with no crossable cell is a wall that looks like a
door. Nothing in the build catches that. It caught one: Route 138 → Route 110
was declared and impassable, because Route 110's west edge is a solid tree
column. Softening opened it.

It works in each map's *local* coordinates, from the connection's own offset.
An earlier version laid the world flat and checked seams there, which is wrong
for the three vanilla pairs whose offsets disagree: a map's world position then
depends on which way the solver reached it, and Route 116/Verdanturf came out
blocked in one direction and open in the other from the same data.

### Wild encounters

`python3 tools/encounters.py`. The tables come from the same place the terrain
did — the maps next door. For each new map every neighbour's table is pooled,
each entry weighted by how much edge the two maps share and by how likely that
slot is to come up; species are then ranked by total weight and dealt into the
slots highest first. Levels are a weighted mean of the donors', so a map
bridging a level 5 route and a level 15 one lands in between.

It runs in two passes. The first uses only vanilla neighbours, so each map's
levels come from real routes. The second runs *only* for maps that got nothing
— Routes 136 and 137, whose only land-bearing neighbours are also new — and
only those see the first pass's output. Feeding new tables back in everywhere
pulls every map toward the global mean: tried it, and Route 141 drifted from
lv 6–7 to lv 3–13, losing exactly the local character the first pass got right.

The result is a difficulty ladder nobody hand-tuned:

```
Route 135/136  lv  3-4     Route 143  lv  6-25
Route 137      lv  3-13    Route 144  lv 15-16
Route 138      lv  2-13    Route 145  lv  6-20
Route 139/140  lv  3-13    Route 146  lv 25-28
Route 141      lv  6-7     Route 147  lv 25-28
Route 142      lv  2-4     Route 148  lv 20-26
```

Route 148 picks up Sandshrew, Trapinch and Baltoy from Route 111 — the desert
species — which is the check that the weighting works: it is the desert seam,
and it got the desert's Pokémon without being told to.

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

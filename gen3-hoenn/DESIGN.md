# Open Hoenn — Design & Survey

An open-world Pokémon Emerald romhack. Hoenn's connected overworld occupies
**40.0%** of its own bounding box: 122,540 of 306,400 metatiles across 49 maps
you can walk between. Everything here is in service of the other 60%.

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

Holes between existing land routes. These are the natural first targets.

| Empty | Chunks | Borders |
|---|---|---|
| 15,360 | 3.8 | Route 105, 103, **Littleroot**, 108 |
| 12,500 | 3.1 | Route 103, 116, 117, 110 |
| 12,120 | 3.0 | Route 116, 114, 112, 113 |
| 7,200 | 1.8 | Route 119, 120, 123, **Fortree** |
| 5,600 | 1.4 | Route 111, 119, 118 |

The first borders Littleroot, which gives the same "testable seconds into a new
game" property the Kanto project wanted and never quite got.

### Open ocean — about 31 chunks

The three largest empty regions all border Routes 124–133. That is sea past the
coastline, and filling it with land would misread what it is.

| Empty | Chunks | Borders |
|---|---|---|
| 49,680 | 12.1 | Route 129, 130, 132, 133 |
| 40,400 | 9.9 | Route 123, 126, 110, Lilycove |
| 37,600 | 9.2 | Route 125, 124, 120, Lilycove |

Islands, archipelago, underwater — or left as water. A different design problem
from the inland gaps and worth treating separately.

---

## 4. Open questions

- **What goes in the inland gaps.** Thirteen chunks is a lot of ground and
  nothing has been designed yet.
- **What the ocean is for.** Thirty-one chunks of sea. Vanilla already uses
  Dive to layer underwater maps over surface ones, which is a mechanic worth
  exploiting rather than working around.
- **Level curve.** Same question the Kanto project parked: an open world means
  the player can arrive anywhere at any level.
- **Whether to use Porymap.** It is the mature editor for exactly this format,
  so there is no reason to build another one.

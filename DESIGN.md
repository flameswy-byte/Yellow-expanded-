# Open Kanto — Design & Handoff

A Pokémon Yellow romhack that fills the empty space between Kanto's routes.
Vanilla Kanto occupies **32.8%** of its own bounding box: 10,035 blocks used out
of a 170×180 block area. Everything below is in service of the other 67%.

**Scope decision: no engine modifications.** Every constraint in §2 is worked
*within*, not around. If a design idea requires changing the engine, it goes in
§8 instead of getting built.

---

## 1. Build environment

Verified working as of this document.

```bash
# toolchain — rgbds 1.0.2 exactly; newer versions may not assemble this source
git clone --depth 1 -b "v1.0.2+hotfix" https://github.com/gbdev/rgbds.git
apt-get install -y bison libpng-dev pkg-config
cd rgbds && make -j4 && export PATH="$PWD:$PATH"

# source
git clone https://github.com/pret/pokeyellow.git
cd pokeyellow && make -j4
```

Success looks like:

```
md5sum pokeyellow.gbc
d9290db87b1f0a23b89f99ee4469e34b
```

**Always confirm the unmodified build matches before making changes.** A clean
baseline is the only way to tell "my edit broke it" from "my toolchain is wrong."

`make` also produces `pokeyellow.map` (section/bank layout, free space per bank)
and `pokeyellow.sym` (symbols for emulator debugging — load it in BGB or Emulicious).

---

## 2. Engine constraints

Measured from the source, not remembered. These are hard walls.

| Constraint | Value | Where |
|---|---|---|
| Loaded map buffer | **1300 bytes** | `wOverworldMap:: ds 1300` in `ram/wram.asm` |
| Connection border | **3 blocks** | `DEF MAP_BORDER EQU 3` in `constants/map_data_constants.asm` |
| Max map size | **(w+6)×(h+6) ≤ 1300** | blockdata plus border strips must fit the buffer |
| Blocks per tileset | 128 used / **256 max** | `gfx/blocksets/overworld.bst`, block ID is one byte |
| Tile art per tileset | 93 used / **96 available** | `gfx/tilesets/overworld.png`, VRAM limit |
| Sprite set | **9 + 2** | `SPRITE_SET_LENGTH` in `constants/sprite_set_constants.asm` |
| Free ROM | **177,191 bytes** across 63 banks | `pokeyellow.map` summary |

Three consequences worth internalising:

**Map size.** Some workable shapes: 22×24 (buffer 840), 24×26 (960), 30×30
(1296, right at the edge). For reference Pallet Town is 10×9 and Route 1 is
10×18, so there is a lot of headroom above vanilla.

**You can add blocks, not art.** 128 free block slots means plenty of new
*arrangements* of existing 8×8 tiles — varied treelines, cliff faces with depth,
irregular shorelines. But tile graphics are effectively full at 93/96, so a
genuinely new terrain type would have to displace existing art.

**One tileset and one encounter table per map.** A map cannot mix forest and
cave block palettes, and every patch of grass in it rolls from the same table.
This is the main reason to keep maps at region scale rather than merging half of
Kanto into one giant map.

---

## 3. Map ID budget

Map IDs are a single byte and `LAST_MAP EQU $ff`. Yellow uses **249 of 255**.

**22 unused slots ship in the ROM**, plus 6 free at the top of the range — **28
available IDs, no engine work.** For scale, vanilla Kanto has only 34 overworld
maps, so this nearly doubles the outdoor world.

Claim them in order and tick them off here:

| ID | Claimed by | ID | Claimed by |
|---|---|---|---|
| `UNUSED_MAP_0B` | | `UNUSED_MAP_74` | |
| `UNUSED_MAP_69` | | `UNUSED_MAP_75` | |
| `UNUSED_MAP_6A` | | `UNUSED_MAP_CC` | |
| `UNUSED_MAP_6B` | | `UNUSED_MAP_CD` | |
| `UNUSED_MAP_6D` | | `UNUSED_MAP_CE` | |
| `UNUSED_MAP_6E` | | `UNUSED_MAP_E7` | |
| `UNUSED_MAP_6F` | | `UNUSED_MAP_ED` | |
| `UNUSED_MAP_70` | | `UNUSED_MAP_EE` | |
| `UNUSED_MAP_72` | | `UNUSED_MAP_F1` | |
| `UNUSED_MAP_73` | | `UNUSED_MAP_F2` | |
| | | `UNUSED_MAP_F3` | |
| | | `UNUSED_MAP_F4` | |

### Reserve, if 28 runs out

60 interior maps share byte-identical blockdata — 18 copies of the same
single-room house, 12 identical Pokécenters, 8 identical Marts, 5 identical gate
upper floors. A generic-interior system with runtime-swapped object and text data
could reclaim roughly 50 more IDs.

**This is engine work and is deliberately out of scope.** It is documented here
so the option is known, not because it is planned.

---

## 4. Layout spec

### The actual rule

The uniform grid was the original plan, and it was dropped. The real constraint
underneath was never uniformity — it is:

> **Any map edge may touch at most one other map.**

That is all vanilla connections support: `connection north, ViridianCity,
VIRIDIAN_CITY, -5` names exactly one neighbour per direction with one offset.
Map sizes may vary freely as long as no edge is shared by two maps.

Vanilla already satisfies this, which is why the whole overworld resolves with
zero conflicts. New maps extend the same partition into the empty space.

**Target cell size is 22×24 blocks (88×96 tiles), treated as a guideline rather
than a rule.** Deviate wherever it makes an area flow naturally with the base
game's routes. Oversized vanilla maps — Route 17 at 10×72, Route 20 at 50×9,
Route 12 at 10×54 — stay as they are and are not split.

### Origin

Re-centred on the bounding box, not anchored to Pallet Town. `tools/layout.json`
holds the solved global position of all 34 vanilla maps in block coordinates,
with `minx`/`miny` giving the offset to bounding-box space.

### Verifying a layout change

`tools/render_kanto.py` walks the connection graph from Pallet Town and places
every overworld map. **If it reports conflicts, a connection offset is wrong** —
the same map was reached by two paths that disagree on where it sits. Fix before
building.

---

## 5. Coordinate audit checklist

**The riskiest part of the project.** Growing a map shifts its origin, and Gen 1
hardcodes coordinates in more places than the object file. These break silently:
the ROM builds, the map looks correct, and a trainer just never notices you.

For every map whose size or origin changes:

- [ ] **`maps/<Name>.blk`** — blockdata padded to the new dimensions
- [ ] **`data/maps/headers/<Name>.asm`** — width and height updated
- [ ] **`constants/map_constants.asm`** — `map_const` width/height entry updated
- [ ] **`data/maps/objects/<Name>.asm`** — every warp, sign, NPC and item X/Y offset
- [ ] **Connection offsets** — in this map's header *and* in every neighbour's header pointing back
- [ ] **Inbound warp returns** — interiors warping out land on coordinates stored in the *destination* map's warp list; check every building on this map
- [ ] **Trainer sight lines** — range values in object data assume a specific tile distance
- [ ] **Hidden items** — `data/events/hidden_objects.asm`, coordinates are absolute
- [ ] **Script X/Y checks** — scripts that compare `wYCoord`/`wXCoord` to trigger events
- [ ] **Sprite set assignment** — new or moved outdoor maps need a `data/sprite_sets.asm` entry
- [ ] **Wild encounters** — `data/wild/maps/<Name>.asm` must exist for any map with grass
- [ ] **Rebuild and check the md5 changed** — an unchanged md5 means the edit did not take

Fly points are staying as-is; no town map work needed for new areas.

---

## 6. Per-map change procedure

Same sequence every time. Doing them out of order mostly works, which is how
mistakes survive to the next map.

**Growing an existing map**

1. Open the map in `kanto_editor.html`, set new width/height, paint the new area
2. Confirm the buffer readout stays at or under 1300
3. Export the `.blk` into `maps/`
4. Update the header and `map_constants.asm` dimensions
5. Work §5 top to bottom — do not skip the inbound warp returns
6. `make` and confirm it assembles
7. Run `tools/render_kanto.py`; confirm zero conflicts
8. Boot it and walk every edge of the map

**Adding a new map**

1. Claim an ID from the §3 table and record it there
2. Add the header, object file, and blockdata; register it in the map header
   pointer table and bank list
3. Generate encounters: `python3 tools/gen_encounters.py <Name> --x .. --y .. --w .. --h ..`
4. Assign a sprite set
5. Wire connections on both sides — new map *and* each neighbour
6. Steps 6–8 above

---

## 7. Tooling

Everything in `tools/` plus the editor. All disposable; none of it ships in the ROM.

**`tools/render_kanto.py`** — solves the global layout from connection data and
renders the stitched overworld to PNG. Doubles as the connection validator.
Point it at the disassembly with `POKEYELLOW=/path/to/pokeyellow` (defaults to
`~/pokeyellow`); needs `pillow`. Exits non-zero and lists the offending edges if
any map is reached by two paths that disagree. On clean vanilla source it places
34/34 maps with no conflicts.

**`tools/layout.json`** — solved positions and dimensions of all 34 vanilla
overworld maps. Regenerate after layout changes.

**`tools/gen_encounters.py`** — generates a starting encounter table for a new
map by blending the 3 nearest vanilla tables, inverse-distance weighted, and
emits valid `.asm`. Water tables only with `--water`.

> **Expect to hand-fix about a quarter of the output.** Kanto's difficulty curve
> follows the player's path, not geography — Route 22 borders the Victory Road
> region but is an early-game area. Distance blending will occasionally propose
> level 30 encounters next to a level 5 route.

**`kanto_editor.html`** — single self-contained file, no server and no
dependencies. Tileset, blockset, all 34 overworld maps and their encounter tables
are baked in. Open it in a browser.

- Block palette, paint / flood fill / rectangle / eyedropper, undo and redo
- **Neighbour context** — adjacent maps render dimmed around the one being edited, so seams line up
- Collision overlay — walkable tiles green, blocked red, on the lower half of each block where the player's feet land
- Resize with live buffer validation against the 1300-byte cap
- Encounter panel — 10 grass and 10 water slots with species and levels
- Exports `.blk` and encounter `.asm` straight into the repo

It holds no state between sessions. Export before closing the tab.

---

## 8. Open questions

Decided:

- Oversized vanilla maps stay oversized; the grid is a guideline
- Origin re-centred on the bounding box
- New areas get trainers and items, **nothing progression-gating** — no HMs, no
  badges, no required routes. Everything new must be skippable.
- Fly points unchanged
- Encounters auto-generated, hand-tuned in the editor

Still open:

- **Level curve for new areas.** Geographic blending is the starting point; the
  real question is what level a player arrives at each new area, which depends on
  routing the open world allows. Probably needs a playthrough to answer.
- **Trainer teams and IDs.** New trainers need roster entries; budget not yet checked.
- **Block authoring.** 128 free block slots are available for natural edges but
  none have been designed yet.
- **Sprite set pressure.** Each outdoor map draws NPCs from a 9-sprite set;
  unclear whether new areas fit the existing sets or need new ones.
- **Generic interiors.** The ~50 extra map IDs in §3, if ever needed.

---

## Quick reference

```
buffer limit      (w+6) × (h+6) ≤ 1300
free map IDs      28
free block slots  128 of 256
free tile art     3 of 96
free ROM          177,191 bytes
vanilla fill      32.8% of 170×180 blocks
clean build md5   d9290db87b1f0a23b89f99ee4469e34b
```

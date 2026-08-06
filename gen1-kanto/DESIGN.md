# Open Kanto — Design & Handoff

A Pokémon Yellow romhack that fills the empty space between Kanto's routes.
Vanilla Kanto occupies **35.4%** of its own bounding box: 10,845 blocks used out
of a 170×180 block area. Everything below is in service of the other 65%.
See `REGIONS.md` for what goes where.

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

*Those 128 slots are not free of charge.* `DrawTileBlock` computes the offset as
`id * 16` by nibble swap with no bounds check, so IDs `$80`–`$ff` work natively.
The obstacle is placement: the tileset header is `db BANK(\1_GFX)` followed by
`dw Block, GFX, Coll` — **one bank byte covering all three** — so the blockset
must share a bank with the tileset graphics. `Overworld` lives in `Tilesets 1`,
which occupies the whole of bank 25 with **0 bytes free**. Growing
`overworld.bst` therefore means relocating the Overworld group (1,504 bytes of
graphics + 32 padding + the blockset, so ~3.6 KB now and ~5.6 KB at the full
256 blocks) into a bank with room. Bank 23 has 8,352 contiguous bytes free.
That is a section move in `gfx/tilesets.asm` — data layout, not engine code, so
it stays inside the §0 scope decision.

The other half of the cost is the editor: `kanto_editor.html` bakes the tileset
and blockset in as base64, so any blockset change needs that data regenerated
rather than hand-edited.

**One tileset and one encounter table per map.** A map cannot mix forest and
cave block palettes, and every patch of grass in it rolls from the same table.
This is the main reason to keep maps at region scale rather than merging half of
Kanto into one giant map.

---

## 3. Map ID budget

Map IDs are a single byte and `LAST_MAP EQU $ff`. Yellow uses **249 of 255**.

**22 unused slots ship in the ROM**, plus 6 free at the top of the range — 28
IDs that cost no engine work. **For indoor maps.** Outdoor maps are a different
and much tighter story.

> **Status:** 18 of the 22 have since been retired with
> `tools/reclaim_map_ids.py --all`, and four outdoor maps have been added.
> `NUM_MAPS` is **235 of 255 — 20 free IDs.** The four slots left alone are
> listed in that tool's `KEEP` table; each is referenced by something and needs
> that reference dealt with before it can go.

### Outdoor maps must have an ID below `FIRST_INDOOR_MAP`

Two tables are sized to the outdoor range rather than to `NUM_MAPS`:

| Table | Length | Indexed by |
|---|---|---|
| `MapSpriteSets` (`data/maps/sprite_sets.asm`) | `FIRST_INDOOR_MAP` | raw map ID |
| `ExternalMapEntries` (`data/maps/town_map_entries.asm`) | `FIRST_INDOOR_MAP` | raw map ID |

`GetSplitMapSpriteSetID` in `engine/overworld/map_sprites.asm` does
`ld hl, MapSpriteSets / add hl, de` with **no bounds check**, and
`LoadTownMapEntry` in `engine/items/town_map.asm` branches on
`cp FIRST_INDOOR_MAP` to pick the external table.

`FIRST_INDOOR_MAP` is `$25`. Every one of the 22 shipped unused slots except
`UNUSED_MAP_0B` is `$69` or higher. An outdoor map at `$69` reads 68 bytes past
the end of a 37-byte table and gets a garbage sprite set.

And `UNUSED_MAP_0B` is not the escape hatch it looks like: it sits below
`FIRST_ROUTE_MAP` (`$0C`), so `MarkTownVisitedAndLoadToggleableObjects` treats
it as a **town** and sets a Fly flag for it, while `engine/gfx/palettes.asm`
compares against `NUM_CITY_MAPS` (`$0B`) and hands it the route palette. It is
the boundary marker between the city block and the route block of the ID space.

**So the usable outdoor budget is zero unused IDs, not 28.** DESIGN.md said the
28 slots "nearly doubles the outdoor world"; they do nothing of the sort.

### How to actually add an outdoor map

Insert a new constant into `constants/map_constants.asm` *before*
`FIRST_INDOOR_MAP` — i.e. immediately after `ROUTE_25` at `$25`. Every indoor
map shifts up by one, which is free because all indoor references are symbolic
and the group constants are computed from `const_value`.

Then add one entry, at the matching position, to each table indexed by map ID:

| Table | Length asserted |
|---|---|
| `MapHeaderPointers` | `NUM_MAPS` |
| `MapHeaderBanks` | `NUM_MAPS` |
| `MapSongBanks` | `NUM_MAPS` |
| `WildDataPointers` | `NUM_MAPS` |
| `MapSpriteSets` | `FIRST_INDOOR_MAP` |
| `ExternalMapEntries` | `FIRST_INDOOR_MAP` |

`ToggleableObjectMapPointers` generates itself with `FOR n, NUM_MAPS` and needs
nothing. Every one of these carries `assert_table_length`, so a missed entry is
an assembly error rather than a silent corruption — this is the one part of the
job the build actually checks for you.

This is data work, not engine work, so it stays inside the §0 scope decision.

**The real ceiling is `NUM_MAPS <= LAST_MAP`.** Beyond the six that shipped
free, an outdoor map is paid for by retiring an unused indoor slot: delete its
`map_const` and drop the matching row from each `NUM_MAPS` table, which lowers
`NUM_MAPS` and frees headroom for a new constant before `FIRST_INDOOR_MAP`.

`tools/reclaim_map_ids.py` does this. It removes rows by **index**, not by
matching a comment — only some of these tables tag their filler rows, and
`grass_water.asm` does not tag them at all — and it checks each table's row
count against `NUM_MAPS` before touching anything. All edits are computed in
memory and written only once every table validates.

Four slots are held back in the tool's `KEEP` table because they are not really
unused: `UNUSED_MAP_6F` carries hidden events and a hidden item,
`UNUSED_MAP_ED` is a live warp target from the Silph Co elevator,
`UNUSED_MAP_F4` has toggle entries, and `UNUSED_MAP_0B` is the boundary marker
between `NUM_CITY_MAPS` and `FIRST_ROUTE_MAP` (and sits below
`FIRST_INDOOR_MAP`, so retiring it would shift the outdoor tables too).

### Reserve, if the ID budget runs out

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
holds the solved global position of all 36 vanilla outdoor maps in block
coordinates, with `minx`/`miny` giving the offset to bounding-box space.

### Verifying a layout change

`tools/render_kanto.py` walks the connection graph from Pallet Town and places
every outdoor map — `OVERWORLD` and `PLATEAU` both, so Route 23 and Indigo
Plateau are included. It reports two distinct failures:

- **Conflicts** — the same map was reached by two paths that disagree on where
  it sits, meaning a connection offset is wrong.
- **Overlapping map pairs** — two maps cover the same ground. The engine never
  notices, because unconnected maps never touch; the world just contains the
  same land twice.

Fix either before building.

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

**Opening a new edge into a vanilla map is the dangerous case, and it is not on
the list above**, because the map's own size and origin never change. A new
connection changes *which coordinates the player can stand on*, and vanilla
scripts assume the vanilla answer.

The worked example: `PalletMovementScript_OakMoveLeft` computes
`wNumStepsToTake = wXCoord - $a`. The Pallet Town intro fires at `wYCoord == 0`,
which in vanilla is reachable only at `wXCoord` 10 or 11 — the one-block gap in
the northern fence. Route 1's western column is walkable but forms an isolated
108-cell strip no player can enter. Connecting a new map to Route 1's west edge
made that strip reachable, and from it the player could step south onto Pallet's
boundary fence — whose *upper* half is walkable — arriving at `wYCoord == 0`
with `wXCoord` 0, 1 or 2. The subtraction underflows to 246 and Prof. Oak walks
left forever. The ROM builds, the layout validates, and the game is unfinishable.

So for every vanilla edge opened:

- [ ] **Re-derive which coordinates became reachable**, across map boundaries,
      and diff that against vanilla. `tools/check_walk.py` gives the step grid;
      the flood has to span every connected map, not one map at a time
- [ ] **Check the destination map's script for coordinate tests** — grep its
      script for `wXCoord` / `wYCoord` and confirm every newly reachable value
      is one the script handles
- [ ] **Check what the player can now reach too early** — the same edge let the
      player walk into tall grass before owning a Pokémon, which is a wild
      encounter with an empty party
- [ ] **Sprite set assignment** — new or moved outdoor maps need a `data/maps/sprite_sets.asm` entry
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

**`tools/layout.json`** — solved positions and dimensions of all 36 vanilla
outdoor maps. Regenerate with `render_kanto.py --json` after layout changes.

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
free map IDs      20 (NUM_MAPS 235 of 255)
free block slots  128 of 256
free tile art     3 of 96
free ROM          177,191 bytes
vanilla fill      35.4% of 170×180 blocks
vanilla build md5 d9290db87b1f0a23b89f99ee4469e34b
```

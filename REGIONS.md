# Open Kanto — Region Plan

Companion to `DESIGN.md`. That document says *how* to build; this one says
*where* and *what*, and why.

The source for "what" is the 1999 Prima official Kanto poster map — the
licensed artwork of the same region the game renders. It draws terrain in the
gaps the game leaves blank, so it answers the question the layout analysis
cannot: not *where is there room*, but *what is supposed to be there*.

The poster is copyrighted Nintendo/Creatures/Game Freak artwork and is
deliberately **not committed to this repo**. It is a reference held outside the
tree; everything below is our own description of geography derived from looking
at it.

---

## 1. How the poster lines up

North is up, same as the game. Landmark positions agree well enough to
georeference by eye — Pallet with Oak's domed lab bottom-left, Cinnabar on its
island below it, Viridian above Pallet, Pewter top-left, Cerulean top-centre,
the Rock Tunnel spires and the Power Plant top-right, Saffron's skyscrapers
centre, Celadon left of it, Lavender's tower on the right, Vermilion's port and
the S.S. Anne centre-bottom, Fuchsia and the Safari Zone's fenced oval below.

It is **not to scale**. Fitting a linear transform through Pallet and Cerulean
puts Fuchsia about 12 blocks off. Treat the poster as authority on *what
terrain occupies a gap and how areas relate*, never on exact dimensions.

## 2. What the poster has that the game does not

In rough order of how much blank map they would fill:

1. **A mountain range across the entire northern edge.** Green peaks from the
   top-left corner along the whole north. The game has nothing above Pewter or
   Route 4. The largest single unexploited feature on the poster.
2. **A cave mouth in the north-centre**, set into those mountains — a dark
   opening in a tan rock face, unconnected to Mt. Moon's position.
3. **A large forest mass west and south-west of Celadon**, far bigger than
   Viridian Forest, filling what the game leaves as the biggest inland void.
4. **A north-east cape** beyond Route 25 with a single isolated building on it.
5. **A bay** between Vermilion and Fuchsia, with the S.S. Anne on open water.
   The game has a void here, not sea.
6. **Open plains east of Saffron**, scattered woodland and a road, between
   Route 8 and Route 11.
7. **A long trestle bridge** on the east coast, crossing to a spur of land.
8. **Scattered boulders and rock outcrops** across the plains — small set
   dressing, useful for making new maps read as Kanto rather than as filler.

## 3. Corrected space budget

`DESIGN.md` reported 32.8% fill across 34 overworld maps. That count filtered
map headers to the `OVERWORLD` tileset, which drops **Route 23 (10×72) and
Indigo Plateau (10×9)** — they use `PLATEAU`. Both are outdoor, both are placed
by connection from Route 22, and together they occupy about 890 blocks of the
west edge (x −25…−16, y −113…−33).

Corrected: **36 outdoor maps, 10,845 of 30,600 blocks, 35.4% fill.**

This is not bookkeeping. The far-west strip beside Route 2 looks like the
cleanest empty column on the map and is in fact Route 23 the whole way up. A
new map sited there would have overlapped it silently — the ROM builds, the
maps never touch in-engine because nothing connects them, and the world simply
contains the same ground twice. `tools/render_kanto.py` now includes `PLATEAU`
in the outdoor set and reports overlapping map pairs, so this fails loudly.

## 4. Candidate regions

Sites where a 22×24 map fits against a free map edge, cross-referenced with
what the poster puts there. Offsets are the `connection` offset from the
existing map; positions are bounding-box block coordinates.

| # | Attach | Dir | Offset | Occupies | Poster terrain | Notes |
|---|---|---|---|---|---|---|
| A | Route11 | north | 0 | (105,−47) | open plains, scattered woodland | Dead-end pocket bounded by Routes 8/11/12. Early-mid levels. **First build.** |
| B | CeladonCity | south | 0 | (50,−45) | dense forest | Biggest inland void; city-edge exit needs care |
| C | Route17 | east | 5 | (40,−45) | forest | Cycling Road's east edge is cliff the whole way |
| D | PewterCity | north | −2 | (−7,−114) | the northern mountains | Best thematic match; wants cliff blockwork first |
| E | Route15 | north | 0 | (75,−2) | the bay | Water map, needs Surf |
| F | Route19 | east | 0 | (70,36) | open sea | Water map, needs Surf |
| G | Route21 | west | 0 | (−22,9) | open sea | Water map, needs Surf |
| H | Route13 | south | 0 | (115,13) | coast near the trestle bridge | Pairs with the bridge feature |

Water regions (E–G) are held back deliberately: they are only reachable with
Surf, which makes them late and makes their encounter tables a different
problem. Land first.

## 5. First build — region A

North of Route 11, 22×24 at (105,−47), single connection south to Route 11.

Chosen because it is the lowest-risk site that still fills real space:

- **No vanilla map changes size or origin**, so the `DESIGN.md` §5 coordinate
  audit does not fire. Route 11 gains one `connection` line and a repainted gap
  in its northern treeline; every warp, sign and trainer coordinate in Kanto
  stays exactly where it is.
- **Dead end, one connection.** Route 8's south edge is also free, so this
  pocket *could* link Route 11 to Route 8 — and deliberately does not. That
  would be an optional bypass around Saffron, which is routing the base game
  did not plan for. A dead end is unambiguously skippable, per §8.
- **Level curve blends cleanly.** Route 11 sits around level 14 and Route 8
  around 18, so `gen_encounters` has two close, mutually consistent neighbours
  to interpolate from — the failure mode the tool warns about (Route 22 next to
  Victory Road) does not apply here.
- **Terrain is buildable from stock blocks.** Grass, trees, water edge and
  ledges all exist in the overworld blockset. No new block art required, which
  keeps the open question in §8 open instead of blocking the first map.

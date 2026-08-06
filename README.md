# Open Kanto / Open Hoenn

Two Pokémon romhacks with the same goal — take a region the base game leaves
mostly empty and open it up — and, more importantly, the same working method.

| | `gen1-kanto/` | `gen3-hoenn/` |
|---|---|---|
| Base | [pret/pokeyellow](https://github.com/pret/pokeyellow) | [pret/pokeemerald](https://github.com/pret/pokeemerald) |
| Language | assembly | C |
| Verified build | `d9290db8…` vanilla | `f3ae0881…` vanilla |
| World | 170×180 blocks, 35.4% filled at the start | 800×383 metatiles, 40.0% filled at the start |
| Status | 4 new maps built, 41.7% filled | Gap 1 built, 45.0% filled |

Neither project needs a ROM. Both decompilations build a complete, byte-exact
ROM from source and verify it themselves. Nothing in this repo distributes a
game; the built ROMs are gitignored and stay out of it.

## Building

```bash
# Kanto — rgbds 1.0.2 exactly
cd gen1-kanto && make          # -> pokeyellow.gbc, md5 in DESIGN.md §1

# Hoenn — agbcc, and note it needs the ARM assembler before it will build
apt-get install -y binutils-arm-none-eabi
git clone https://github.com/pret/agbcc && cd agbcc && ./build.sh \
  && ./install.sh ../gen3-hoenn/pokeemerald
cd gen3-hoenn/pokeemerald && make && make compare
```

`gen3-hoenn/pokeemerald` is vendored from upstream rather than forked with
history; `UPSTREAM.txt` records the commit it came from.

## Why one repo

The two games share almost no code. What they share is the method, and that has
turned out to be the valuable part:

- **Establish a verified baseline first.** Build vanilla, check the checksum,
  and only then change anything. It is the only way to tell "my edit broke it"
  from "my toolchain is wrong."
- **Measure constraints from source, never from memory or from a document.**
  The Kanto handoff doc was confidently wrong three times: the fill was 35.4%
  not 32.8%, its "28 free map IDs" were worth zero for outdoor maps, and a path
  it named did not exist. Every one surfaced by checking.
- **Build tooling that fails loudly.** `assert_table_length` in the Gen 1 data
  tables caught two mistakes that would otherwise have been silent corruption.
- **A new connection changes which coordinates the player can reach, and
  existing scripts assume the old answer.** This is the lesson that cost the
  most to learn — see `gen1-kanto/DESIGN.md` §5 — and it is engine-independent.
  Gen 3 has more scripted coordinate triggers than Gen 1, not fewer.

The differences matter too, and they run in Hoenn's favour: see
`gen3-hoenn/DESIGN.md` §2 for the three Gen 1 constraints that simply do not
exist in Gen 3.

#ifndef GUARD_CONSTANTS_BATTLE_CONFIG_H
#define GUARD_CONSTANTS_BATTLE_CONFIG_H

// Battle mechanics that changed after Gen 3, gathered in one place so the
// whole of it can be read at once and argued with.
//
// The reference is CFRU (Skeli789's Complete Fire Red Upgrade), which is the
// engine Radical Red is built on and the only part of it that is open source
// - Radical Red itself ships as a binary patch. Where CFRU's default differs
// from the official games, CFRU wins and the difference is noted on the line.

// --- critical hits --------------------------------------------------------
// Vanilla Emerald: {16, 8, 4, 3, 2} and double damage.
//
// CFRU's table has three settings and takes none of them by default, which is
// the Gen 7 row: a base rate of 1/24 rather than Gen 6's 1/16. Two stages of
// boost still guarantee a crit, which is the Gen 6 change - in Gen 2-5 the top
// of the table was 1/2.
//
// DIFFERS FROM THE OFFICIAL GAMES: Gen 6 uses 1/16 at stage 0. CFRU's default
// is the Gen 7 value of 1/24, so crits are rarer here than in ORAS.
#define CRIT_CHANCES { 24, 8, 2, 1, 1 }

// A crit does 1.5x from Gen 6 on, not 2x. gCritMultiplier is kept in tenths so
// the fraction survives integer arithmetic, which is how CFRU does it too.
#define BASE_CRIT_MULTIPLIER 10     // 1.0x
#define CRIT_MULTIPLIER      15     // 1.5x

// --- sleep ----------------------------------------------------------------
// Vanilla Emerald rolls (Random() & 3) + 2, so 2-5 turns on the counter and up
// to four turns actually asleep. Gen 5 cut it to 1-3.
#define SLEEP_TURNS_MIN 2
#define SLEEP_TURNS_RANGE 2         // 2-3 on the counter: 1-3 turns asleep

// --- Struggle -------------------------------------------------------------
// Gen 4 made Struggle's recoil a quarter of the user's maximum HP instead of a
// quarter of the damage it dealt, so it costs the same against a wall as
// against paper. Take Down and the other 25% recoil moves are unchanged.
#define STRUGGLE_RECOIL_FRACTION 4  // of max HP
//
// Gen 4's other Struggle change - that it stops being Normal-typed, so Ghosts
// are not immune to it - is already how Emerald behaves: Cmd_typecalc and both
// TypeCalc variants return early on MOVE_STRUGGLE, before any immunity or
// effectiveness is looked up. Nothing to change, recorded so the absence is
// deliberate.

// --- burn -----------------------------------------------------------------
// Burn takes 1/8 of maximum HP per turn in Gens 3 to 6 and 1/16 from Gen 7, so
// vanilla's 1/8 is already right for the generation being targeted and is left
// alone. Recorded here so that the absence of a change is deliberate rather
// than an oversight.
#define BURN_DAMAGE_FRACTION 8

#endif // GUARD_CONSTANTS_BATTLE_CONFIG_H

#ifndef GUARD_CONSTANTS_QOL_CONFIG_H
#define GUARD_CONSTANTS_QOL_CONFIG_H

// The quality-of-life changes, gathered the same way the battle constants are,
// so what has been changed about playing the game can be read in one place.
//
// The reference is again CFRU (Skeli789's Complete Fire Red Upgrade), and in
// particular its src/config.h, which is 340 lines of switches each carrying the
// author's reason on the line. The switches it ships commented *out* are as
// informative as the ones it ships on, because a switch named OLD_SOMETHING and
// left off tells you what the default is.
//
// Each entry below names the CFRU switch it corresponds to and whether CFRU
// takes it, so a disagreement is visible rather than silent.

// --- running indoors ------------------------------------------------------
// CFRU: #define CAN_RUN_IN_BUILDINGS, on by default.
//
// Emerald refuses to run on any map whose header clears allowRunning, which is
// every interior. The per-metatile refusal is untouched: the Petalburg gym's
// mats and the sliding ice still stop you, because those are puzzles rather
// than politeness.
#define RUN_INDOORS TRUE

// --- reusable TMs ---------------------------------------------------------
// CFRU: //#define REUSABLE_TMS - shipped OFF, with a warning that every TM then
// needs its Mystery byte set. That warning is a Fire Red binary-hacking detail
// with no counterpart here; in a decompilation the TM simply is not removed.
//
// DIFFERS FROM CFRU'S DEFAULT, deliberately: Radical Red itself has reusable
// TMs, and Radical Red is what was actually asked for. HMs were already never
// consumed, so this only makes TMs behave the way HMs always did.
#define REUSABLE_TMS TRUE

// --- overworld poison -----------------------------------------------------
// CFRU: #define POISON_1_HP_SURVIVAL, on by default.
//
// A poisoned Pokemon walking around the overworld stops at 1 HP instead of
// fainting. The whiteout path is left in place - it is still reachable if the
// party is already at zero - but poison alone can no longer end a run.
#define POISON_SURVIVES_AT_1_HP TRUE

// --- repels ---------------------------------------------------------------
// CFRU: #define BW_REPEL_SYSTEM, on by default.
//
// When a repel runs out the game offers to use another of the same kind, if
// the bag still has one. Which kind was used is remembered in a save variable;
// see VAR_LAST_REPEL_USED.
#define BW_REPEL_PROMPT TRUE

#endif // GUARD_CONSTANTS_QOL_CONFIG_H

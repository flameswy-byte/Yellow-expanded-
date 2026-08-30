#!/usr/bin/env python3
"""Take Hidden Power out of every pool the game can draw a move from.

Hidden Power derives both its type and its power from the holder's IVs. The
type derivation is the awkward part: vanilla computes it from the number of
types that exist, so adding the Fairy type silently widened Hidden Power's
range to include a type it has never been able to roll in any generation. That
was pinned rather than fixed, and pinning a constant to stop a move
misbehaving is a sign the move is more trouble than it is worth.

Rather than rewrite the move, this removes it from everywhere the game can
reach it, so it is never called:

  the TM          TM10 taught Hidden Power. It now teaches Swift.
  level-up        Unown, Meditite and Medicham learned it by level.
  trainers        two Abra, in Edward's and Jaclyn's parties.
  the Frontier    Trainer Hill, the Battle Pike, a rental mon, a contest
                  opponent, and the Apprentice's list of askable moves.
  Metronome       the one source that no learnset edit can close, since it
                  picks from every move in the game regardless of who knows
                  what. Added to the forbidden list.

Everything keyed by move id - the name, the description, the animation, the
contest data, the easy-chat word - is left alone. The move still exists in
gBattleMoves; nothing can any longer ask for it.

Swift is the replacement throughout, and for most of these it is legal rather
than merely plausible: TM10's compatibility list is untouched, so every one of
the 372 species that could have learned Hidden Power from TM10 can now learn
Swift from it. Unown is the exception and is called out below.

    python3 tools/hiddenpower.py            # apply
    python3 tools/hiddenpower.py --check    # verify nothing reachable remains
"""
import argparse, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_hoenn as R

NEW = 'SWIFT'

# Straight substitutions. Each is (path, before, after, how many to expect),
# and each is idempotent because the "before" text is gone once applied.
SUBS = [
    # TM10. This one line does most of the work: FOREACH_TM generates the item
    # enum (ITEM_TM_HIDDEN_POWER), the TM-to-move table sTMHMMoves, and the
    # per-species compatibility bitfield, so all three move together.
    ('include/constants/tms_hms.h', '    F(HIDDEN_POWER) \\', f'    F({NEW}) \\', 1),

    # the bitfield's member is named after the move, so every species that has
    # it has to follow
    ('src/data/pokemon/tmhm_learnsets.h', '.HIDDEN_POWER = TRUE', f'.{NEW} = TRUE', 372),

    # Unown, Meditite, Medicham. Unown is the one that cannot be left empty:
    # Hidden Power is its ENTIRE learnset, and a Unown with no moves can only
    # ever Struggle. Its TM list is empty too, so unlike the others this
    # substitution is a design decision rather than a legal moveset.
    ('src/data/pokemon/level_up_learnsets.h', 'MOVE_HIDDEN_POWER', f'MOVE_{NEW}', 3),

    # Edward's and Jaclyn's Abra, whose only move it was
    ('src/data/trainer_parties.h', 'MOVE_HIDDEN_POWER', f'MOVE_{NEW}', 2),

    # the Frontier
    ('src/data/battle_frontier/trainer_hill.h', 'MOVE_HIDDEN_POWER', f'MOVE_{NEW}', 6),
    ('src/data/battle_frontier/battle_frontier_mons.h', 'MOVE_HIDDEN_POWER', f'MOVE_{NEW}', 1),
    ('src/battle_pike.c', 'MOVE_HIDDEN_POWER', f'MOVE_{NEW}', 2),
    ('src/data/contest_opponents.h', 'MOVE_HIDDEN_POWER', f'MOVE_{NEW}', 1),

    # the Apprentice's table is keyed by move, and MOVE_SWIFT is already TRUE
    # in it, so this line is deleted rather than substituted - a second
    # initialiser for the same index would not compile
    ('src/data/battle_frontier/apprentice.h', '    [MOVE_HIDDEN_POWER] = TRUE,\n', '', 1),

    # Metronome. Learnsets cannot close this one: it picks from the whole move
    # list. The entry goes after MIMIC_FORBIDDEN_END so it binds Metronome
    # only - Mimic copies the target's last move, and nothing will use it.
    ('src/battle_script_commands.c',
     '    MOVE_FOCUS_PUNCH,\n    METRONOME_FORBIDDEN_END',
     '    MOVE_FOCUS_PUNCH,\n'
     '    MOVE_HIDDEN_POWER, // removed from the game; see tools/hiddenpower.py\n'
     '    METRONOME_FORBIDDEN_END', 1),

    # the item entry, whose enum name the macro above just changed
    ('src/data/items.h', '[ITEM_TM_HIDDEN_POWER] =', f'[ITEM_TM_{NEW}] =', 1),
    ('data/maps/SlateportCity/scripts.inc',
     '.2byte ITEM_TM_HIDDEN_POWER', f'.2byte ITEM_TM_{NEW}', 1),

    # TM10's bag description described the IV derivation
    ('src/data/text/item_descriptions.h',
     'static const u8 sTM10Desc[] = _(\n'
     '    "The attack power\\n"\n'
     '    "varies among\\n"\n'
     '    "different POKéMON.");',
     'static const u8 sTM10Desc[] = _(\n'
     '    "Fires star-shaped\\n"\n'
     '    "rays that will not\\n"\n'
     '    "miss the target.");', 1),

    # the save flags and the script labels are only identifiers, but leaving
    # them named after a move that is gone would be a trap for the next reader
    ('include/constants/flags.h',
     'FLAG_MET_HIDDEN_POWER_GIVER', 'FLAG_MET_TM_SWIFT_GIVER', 1),
    ('include/constants/flags.h',
     'FLAG_RECEIVED_TM_HIDDEN_POWER', 'FLAG_RECEIVED_TM_SWIFT', 1),
]

# The Fortree woman's scene is built entirely around the words "hidden power":
# she tests whether yours has awoken and hands you the TM for it. The coin game
# is worth keeping, so the scene is rewritten around the same idea of a sixth
# sense rather than deleted.
# The object event that runs the scene names the script in map.json, from which
# events.inc is generated at build time - so the json is the file to edit, and
# renaming only scripts.inc gives a link error rather than a compile one.
FORTREE_JSON = 'data/maps/FortreeCity_House2/map.json'

FORTREE = 'data/maps/FortreeCity_House2/scripts.inc'
FORTREE_SUBS = [
    ('FLAG_RECEIVED_TM_HIDDEN_POWER', f'FLAG_RECEIVED_TM_{NEW}'),
    ('FLAG_MET_HIDDEN_POWER_GIVER', 'FLAG_MET_TM_SWIFT_GIVER'),
    ('ITEM_TM_HIDDEN_POWER', f'ITEM_TM_{NEW}'),
    ('FortreeCity_House2_EventScript_HiddenPowerGiver', 'FortreeCity_House2_EventScript_SwiftGiver'),
    ('FortreeCity_House2_EventScript_ExplainHiddenPower', 'FortreeCity_House2_EventScript_ExplainSwift'),
    ('FortreeCity_House2_Text_YourHiddenPowerHasAwoken', 'FortreeCity_House2_Text_YourSixthSenseHasAwoken'),
    ('FortreeCity_House2_Text_ExplainHiddenPower', 'FortreeCity_House2_Text_ExplainSwift'),
    ('FortreeCity_House2_Text_HiddenPowersArousedByNature', 'FortreeCity_House2_Text_SensesArousedByNature'),
]
FORTREE_TEXT = [
    ('\t.string "People… POKéMON…\\p"\n'
     '\t.string "Their hidden powers are aroused by\\n"\n'
     '\t.string "living in natural environments…$"',
     '\t.string "People… POKéMON…\\p"\n'
     '\t.string "Their senses are sharpened by living\\n"\n'
     '\t.string "in natural environments…$"'),
    ('\t.string "Let this old woman see if your hidden\\n"\n'
     '\t.string "power has awoken…\\p"',
     '\t.string "Let this old woman see if your sixth\\n"\n'
     '\t.string "sense has awoken…\\p"'),
    ('\t.string "Oh! Splendid!\\n"\n'
     '\t.string "Your hidden power has awoken!\\p"\n'
     '\t.string "Here, take this and awaken the hidden\\n"\n'
     '\t.string "power of your POKéMON.$"',
     '\t.string "Oh! Splendid!\\n"\n'
     '\t.string "Your sixth sense has awoken!\\p"\n'
     '\t.string "Here. Take this, and let your POKéMON\\n"\n'
     '\t.string "strike what the eye cannot follow.$"'),
    ('\t.string "HIDDEN POWER is a move that changes\\n"\n'
     '\t.string "with the POKéMON.$"',
     '\t.string "SWIFT throws stars that always find\\n"\n'
     '\t.string "their mark. Nothing dodges them.$"'),
]

# Where a reachable Hidden Power would have to appear if one survived. Files
# keyed by move id - names, descriptions, contest data, the easy-chat word -
# are deliberately not in this list: the move still exists, it is just
# unreachable.
POOLS = [
    'src/data/pokemon/level_up_learnsets.h',
    'src/data/pokemon/tmhm_learnsets.h',
    'src/data/trainer_parties.h',
    'src/data/battle_frontier/trainer_hill.h',
    'src/data/battle_frontier/battle_frontier_mons.h',
    'src/data/battle_frontier/apprentice.h',
    'src/data/contest_opponents.h',
    'src/battle_pike.c',
    'include/constants/tms_hms.h',
]


def apply(dry):
    done = skipped = 0
    for path, old, new, n in SUBS:
        full = f'{R.ROOT}/{path}'
        text = open(full).read()
        c = text.count(old)
        if c == 0:
            skipped += 1
            continue
        if c != n:
            sys.exit(f'{path}: expected {n} of {old.strip()[:50]!r}, found {c}')
        if not dry:
            open(full, 'w').write(text.replace(old, new))
        done += 1

    for path, pairs in ((FORTREE, FORTREE_SUBS + FORTREE_TEXT),
                        (FORTREE_JSON, FORTREE_SUBS)):
        full = f'{R.ROOT}/{path}'
        text = open(full).read()
        for old, new in pairs:
            if old in text:
                text = text.replace(old, new)
                done += 1
        if not dry:
            open(full, 'w').write(text)
    return done, skipped


def check():
    bad = []
    for path in POOLS:
        text = open(f'{R.ROOT}/{path}').read()
        for token in ('MOVE_HIDDEN_POWER', 'HIDDEN_POWER = TRUE', 'F(HIDDEN_POWER)'):
            if token in text:
                bad.append(f'{path} still has {token}')

    # Metronome must not be able to call it
    bsc = open(f'{R.ROOT}/src/battle_script_commands.c').read()
    table = bsc[bsc.index('sMovesForbiddenToCopy'):]
    table = table[:table.index('};')]
    after_mimic = table[table.index('MIMIC_FORBIDDEN_END'):]
    if 'MOVE_HIDDEN_POWER' not in after_mimic:
        bad.append('Metronome can still call Hidden Power')

    # and TM10 must teach something else
    tms = open(f'{R.ROOT}/include/constants/tms_hms.h').read()
    tm10 = re.findall(r'F\((\w+)\)', tms)[9]
    if tm10 == 'HIDDEN_POWER':
        bad.append('TM10 still teaches Hidden Power')
    return bad, tm10


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()

    done, skipped = apply(a.dry_run)
    print(f'{done} edits applied, {skipped} were already done')

    if a.check:
        bad, tm10 = check()
        if bad:
            sys.exit('\n'.join(bad))
        print(f'no reachable Hidden Power remains; TM10 teaches {tm10}')


if __name__ == '__main__':
    sys.exit(main())

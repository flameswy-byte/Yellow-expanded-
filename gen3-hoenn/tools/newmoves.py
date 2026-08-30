#!/usr/bin/env python3
"""Add the moves the new species are actually known for, and Play Rough.

tools/newmons.py brought in Larvesta, Volcarona, Wimpod, Golisopod and the
Alolan Vulpix line, but their signature moves are all Gen 5 or later and simply
did not exist in this engine. Substituting Amnesia and Agility for Quiver Dance
is not the same Pokemon: one turn of setup raising three stats is most of what
makes Volcarona a threat, and two separate +2 moves that skip Special Attack is
not it.

    QUIVER DANCE      Bug     status   Sp.Atk, Sp.Def and Speed up one stage
    FIERY DANCE       Fire    special  80, 50% chance of Sp.Atk up one
    BUG BUZZ          Bug     special  90, 10% chance of Sp.Def down one
    FIRST IMPRESSION  Bug     physical 90, +2 priority, first turn out only
    AURORA VEIL       Ice     status   both screens at once, only in hail
    DAZZLING GLEAM    Fairy   special  80, hits both foes
    PLAY ROUGH        Fairy   physical 90, 90% accurate, 10% Attack down

Dazzling Gleam is also the first damaging Fairy move in the game - retyping
Charm, Sweet Kiss and Moonlight gave the type no offence at all. Play Rough is
the second, and the only physical one: it goes to Mawile, which fairy.py
retyped to Steel/Fairy and which otherwise had no way to use that half of its
typing. Every other Fairy in the game is a special attacker, so Play Rough is
the one move here aimed at a vanilla species rather than a new one.

Only two needed new machinery of their own. Bug Buzz uses the existing
EFFECT_SPECIAL_DEFENSE_DOWN_HIT and Dazzling Gleam is a plain EFFECT_HIT; the
other four have new effects and scripts, added in the source next to the ones
they are modelled on:

    Quiver Dance      Calm Mind with a third stage for Speed
    Fiery Dance       the existing MOVE_EFFECT_AFFECTS_USER secondary machinery
    First Impression  Fake Out without the flinch; priority is move data
    Aurora Veil       one new battle-script command, setauroraveil

Animations are reused rather than drawn. Every one of these is a borrowed
animation from a move of the same type and shape, named below, on the same
reasoning the Fairy type badges reused existing lettering: a wrong-looking
animation is worse than a familiar one.

    python3 tools/newmoves.py            # apply
    python3 tools/newmoves.py --check    # verify what is written
    python3 tools/newmoves.py --report   # print the table to read through
"""
import argparse, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_hoenn as R

FIRST_ID = 355          # MOVE_PSYCHO_BOOST is 354 and was the last

# name, effect, power, type, accuracy, pp, secondary chance, target, priority,
# the animation it borrows, contest data, and the bag description.
MOVES = [
    dict(const='QUIVER_DANCE', name='QUIVER DANCE', effect='EFFECT_QUIVER_DANCE',
         power=0, type='BUG', acc=0, pp=20, chance=0,
         target='MOVE_TARGET_USER', priority=0, split='SPLIT_STATUS',
         flags='FLAG_SNATCH_AFFECTED',
         anim='Move_DRAGON_DANCE', contest=('BEAUTY', 'CONTEST_EFFECT_IMPROVE_CONDITION_PREVENT_NERVOUSNESS'),
         desc='Raises SP. ATK,\nSP. DEF and SPEED.'),
    dict(const='FIERY_DANCE', name='FIERY DANCE', effect='EFFECT_SPECIAL_ATTACK_UP_HIT',
         power=80, type='FIRE', acc=100, pp=10, chance=50,
         target='MOVE_TARGET_SELECTED', priority=0, split='SPLIT_SPECIAL',
         flags='FLAG_PROTECT_AFFECTED | FLAG_MIRROR_MOVE_AFFECTED | FLAG_KINGS_ROCK_AFFECTED',
         anim='Move_FLAME_WHEEL', contest=('BEAUTY', 'CONTEST_EFFECT_BETTER_WHEN_LATER'),
         desc='A fiery dance that may\nraise SP. ATK.'),
    dict(const='BUG_BUZZ', name='BUG BUZZ', effect='EFFECT_SPECIAL_DEFENSE_DOWN_HIT',
         power=90, type='BUG', acc=100, pp=10, chance=10,
         target='MOVE_TARGET_SELECTED', priority=0, split='SPLIT_SPECIAL',
         flags='FLAG_PROTECT_AFFECTED | FLAG_MIRROR_MOVE_AFFECTED | FLAG_KINGS_ROCK_AFFECTED',
         anim='Move_SILVER_WIND', contest=('BEAUTY', 'CONTEST_EFFECT_STARTLE_MON_WITH_JUDGES_ATTENTION'),
         desc='A sound wave that may\nlower SP. DEF.'),
    dict(const='FIRST_IMPRESSION', name='FIRSTIMPRESS', effect='EFFECT_FIRST_IMPRESSION',
         power=90, type='BUG', acc=100, pp=10, chance=0,
         target='MOVE_TARGET_SELECTED', priority=2, split='SPLIT_PHYSICAL',
         flags='FLAG_PROTECT_AFFECTED | FLAG_MIRROR_MOVE_AFFECTED | FLAG_KINGS_ROCK_AFFECTED',
         anim='Move_SLASH', contest=('COOL', 'CONTEST_EFFECT_BETTER_IF_FIRST'),
         desc='Strikes first, but only\non the first turn.'),
    dict(const='AURORA_VEIL', name='AURORA VEIL', effect='EFFECT_AURORA_VEIL',
         power=0, type='ICE', acc=0, pp=20, chance=0,
         target='MOVE_TARGET_USER', priority=0, split='SPLIT_STATUS',
         flags='FLAG_SNATCH_AFFECTED',
         anim='Move_LIGHT_SCREEN', contest=('BEAUTY', 'CONTEST_EFFECT_AVOID_STARTLE'),
         desc='Blunts all attacks,\nbut only during hail.'),
    dict(const='PLAY_ROUGH', name='PLAY ROUGH', effect='EFFECT_ATTACK_DOWN_HIT',
         power=90, type='FAIRY', acc=90, pp=10, chance=10,
         target='MOVE_TARGET_SELECTED', priority=0, split='SPLIT_PHYSICAL',
         flags='FLAG_PROTECT_AFFECTED | FLAG_MIRROR_MOVE_AFFECTED | FLAG_KINGS_ROCK_AFFECTED',
         anim='Move_COVET', contest=('CUTE', 'CONTEST_EFFECT_BETTER_IF_SAME_TYPE'),
         desc="Plays rough, and may\nlower the foe's ATTACK."),
    dict(const='DAZZLING_GLEAM', name='DAZZLNGGLEAM', effect='EFFECT_HIT',
         power=80, type='FAIRY', acc=100, pp=10, chance=0,
         target='MOVE_TARGET_BOTH', priority=0, split='SPLIT_SPECIAL',
         flags='FLAG_PROTECT_AFFECTED | FLAG_MIRROR_MOVE_AFFECTED | FLAG_KINGS_ROCK_AFFECTED',
         anim='Move_SWIFT', contest=('BEAUTY', 'CONTEST_EFFECT_BETTER_WHEN_AUDIENCE_EXCITED'),
         desc='Damages foes with a\nburst of light.'),
]

# Where each one goes. Larvesta gets Fiery Dance early enough to matter, since
# Volcarona is a level 59 evolution and nobody wants to wait that long for the
# line to do anything interesting.
LEARN = {
    'LARVESTA':    [(45, 'FIERY_DANCE')],
    'VOLCARONA':   [(50, 'QUIVER_DANCE'), (64, 'FIERY_DANCE'), (70, 'BUG_BUZZ')],
    'GOLISOPOD':   [(30, 'FIRST_IMPRESSION')],
    'NINETALES_A': [(45, 'AURORA_VEIL'), (51, 'DAZZLING_GLEAM')],
}

# Moves added to learnsets that were already in the game. Unlike LEARN above,
# these species are vanilla, so their learnsets are named after them rather
# than being one of the numbered stubs newmons.py filled in.
LEARN_VANILLA = {
    'Mawile': [(41, 'PLAY_ROUGH')],
}

# Moves these replace in the learnsets newmons.py wrote, so the level curve
# does not grow a bulge. Each is (species, level, move that was there).
REPLACED = [
    ('VOLCARONA', 50, 'AMNESIA'),
    ('VOLCARONA', 64, 'FLAMETHROWER'),
    ('VOLCARONA', 70, 'SIGNAL_BEAM'),
    ('NINETALES_A', 51, 'EXTRASENSORY'),
]


def read(p):
    return open(f'{R.ROOT}/{p}').read()


def write(p, t, dry):
    if not dry:
        open(f'{R.ROOT}/{p}', 'w').write(t)


def block(m):
    return f"""    [MOVE_{m['const']}] =
    {{
        .effect = {m['effect']},
        .power = {m['power']},
        .type = TYPE_{m['type']},
        .split = {m['split']},
        .accuracy = {m['acc']},
        .pp = {m['pp']},
        .secondaryEffectChance = {m['chance']},
        .target = {m['target']},
        .priority = {m['priority']},
        .flags = {m['flags']},
    }},
"""


def camel(const):
    return ''.join(p.capitalize() for p in const.split('_'))


def apply(dry):
    mark_c = '\n// Open Hoenn - tools/newmoves.py\n'
    mark_s = '\n\t@ Open Hoenn - tools/newmoves.py\n'

    def tail(path, mark, body, table):
        """Append to the end of one named table, so re-running replaces rather
        than appends. The table has to be found by name: contest_moves.h holds
        three of them, and reaching for the file's last '};' put six moves
        inside gContestEffectFuncs."""
        t = read(path)
        if mark in t:
            j = t.index(mark)
            k = t.index('};', j)
            t = t[:j] + t[k:]
        i = t.index(table)
        end = t.index('\n};', i)
        return t[:end] + '\n' + mark + body + t[end:]

    # --- the constants -----------------------------------------------------
    t = read('include/constants/moves.h')
    if mark_c in t:
        # cut out our block only - the include guard's #endif follows it
        j = t.index(mark_c)
        t = t[:j] + t[t.index('#endif', j):]
    body = ''.join(f'#define MOVE_{m["const"]} {FIRST_ID + i}\n'
                   for i, m in enumerate(MOVES))
    body += f'\n#define MOVES_COUNT {FIRST_ID + len(MOVES)}\n'
    t = re.sub(r'\n#define MOVES_COUNT \d+\n', '\n', t)
    # the file ends in an include guard; the defines go inside it
    i = t.rindex('#endif')
    write('include/constants/moves.h',
          t[:i].rstrip() + '\n' + mark_c + body + '\n' + t[i:], dry)

    # --- battle data, names, descriptions, contest data --------------------
    write('src/data/battle_moves.h',
          tail('src/data/battle_moves.h', mark_c,
               ''.join('\n' + block(m) for m in MOVES), 'gBattleMoves['), dry)
    write('src/data/text/move_names.h',
          tail('src/data/text/move_names.h', mark_c,
               ''.join(f'    [MOVE_{m["const"]}] = _("{m["name"]}"),\n'
                       for m in MOVES), 'gMoveNames['), dry)
    write('src/data/contest_moves.h',
          tail('src/data/contest_moves.h', mark_c,
               ''.join(f'''    [MOVE_{m['const']}] =
    {{
        .effect = {m['contest'][1]},
        .contestCategory = CONTEST_CATEGORY_{m['contest'][0]},
        .comboStarterId = 0,
        .comboMoves = {{0}},
    }},
''' for m in MOVES), 'gContestMoves['), dry)

    # descriptions come in two pieces - the strings, then the pointers -
    # which sit on either side of the table, so they need markers of their own
    mark_d = '\n// Open Hoenn - tools/newmoves.py (strings)\n'
    t = read('src/data/text/move_descriptions.h')
    if mark_d in t:
        a = t.index(mark_d)
        b = t.index('const u8 *const gMoveDescriptionPointers', a)
        t = t[:a] + '\n' + t[b:]
    strings = ''.join(
        f'static const u8 s{camel(m["const"])}Description[] = _(\n'
        + ''.join(f'    "{l}\\n"\n' for l in m['desc'].split('\n')[:-1])
        + f'    "{m["desc"].split(chr(10))[-1]}");\n' for m in MOVES)
    k = t.index('const u8 *const gMoveDescriptionPointers')
    t = t[:k].rstrip() + '\n' + mark_d + strings + '\n' + t[k:]
    if mark_c in t:
        a = t.index(mark_c)
        t = t[:a] + t[t.index('};', a):]
    end = t.index('\n};', t.index('gMoveDescriptionPointers['))
    ptrs = ''.join(f'    [MOVE_{m["const"]} - 1] = s{camel(m["const"])}Description,\n'
                   for m in MOVES)
    t = t[:end] + '\n' + mark_c + ptrs + t[end:]
    write('src/data/text/move_descriptions.h', t, dry)

    # --- animations, borrowed rather than drawn ----------------------------
    t = read('data/battle_anim_scripts.s')
    if mark_s in t:
        t = t[:t.index(mark_s)] + t[t.index('\n', t.index(mark_s) + len(mark_s)):]
    anchor = '\t.4byte Move_PSYCHO_BOOST\n'
    add = ''.join(f'\t.4byte {m["anim"]}\t@ MOVE_{m["const"]}\n' for m in MOVES)
    if '@ MOVE_QUIVER_DANCE' not in t:
        t = t.replace(anchor, anchor + mark_s.lstrip('\n') + add, 1)
    write('data/battle_anim_scripts.s', t, dry)


def wire_learnsets(dry):
    """Slot the new moves into the learnsets newmons.py wrote, replacing the
    stand-ins rather than adding to them, so the level curve keeps its shape."""
    import newmons as NM
    t = read('src/data/pokemon/level_up_learnsets.h')
    slot = {m['const']: 252 + i for i, m in enumerate(NM.MONS)}
    gone = {(s, lv): mv for s, lv, mv in REPLACED}

    for const, adds in list(LEARN.items()) + list(LEARN_VANILLA.items()):
        sym = (f'sSpecies{slot[const]}LevelUpLearnset' if const in slot
               else f's{const}LevelUpLearnset')
        mm = re.search(rf'(static const u16 {sym}\[\] = \{{\n)(.*?)(    LEVEL_UP_END\n\}};)',
                       t, re.S)
        if mm is None:
            sys.exit(f'no learnset {sym} for {const}')
        rows = re.findall(r'LEVEL_UP_MOVE\(\s*(\d+), MOVE_(\w+)\)', mm.group(2))
        rows = [(int(a), b) for a, b in rows]
        for lv, mv in adds:
            was = gone.get((const, lv))
            rows = [(l, m) for l, m in rows
                    if not (l == lv and (m == was or m == mv))]
            rows.append((lv, mv))
        rows.sort()
        body = ''.join(f'    LEVEL_UP_MOVE({lv:2d}, MOVE_{mv}),\n' for lv, mv in rows)
        t = t.replace(mm.group(0), mm.group(1) + body + mm.group(3))
    write('src/data/pokemon/level_up_learnsets.h', t, dry)


def check():
    bad = []
    moves = read('include/constants/moves.h')
    data = read('src/data/battle_moves.h')
    names = read('src/data/text/move_names.h')
    anims = read('data/battle_anim_scripts.s')
    learn = read('src/data/pokemon/level_up_learnsets.h')

    n = int(re.search(r'#define MOVES_COUNT (\d+)', moves).group(1))
    if n != FIRST_ID + len(MOVES):
        bad.append(f'MOVES_COUNT is {n}, should be {FIRST_ID + len(MOVES)}')

    # the animation table is read by move id; one short and the game reads
    # past the end of it
    tbl = anims[anims.index('gBattleAnims_Moves::'):]
    tbl = tbl[:tbl.index('\n\n')] if '\n\n' in tbl else tbl
    got = len(re.findall(r'\.4byte Move_\w+', anims[:anims.index('Move_NONE:')]
                         if 'Move_NONE:' in anims else anims))
    for m in MOVES:
        if f'@ MOVE_{m["const"]}' not in anims:
            bad.append(f'MOVE_{m["const"]} has no animation table entry')
        if f'#define MOVE_{m["const"]} ' not in moves:
            bad.append(f'MOVE_{m["const"]} has no constant')
        if f'[MOVE_{m["const"]}] =' not in data:
            bad.append(f'MOVE_{m["const"]} has no battle data')
        if f'[MOVE_{m["const"]}] = _("{m["name"]}")' not in names:
            bad.append(f'MOVE_{m["const"]} is not named {m["name"]}')

    for const, adds in list(LEARN.items()) + list(LEARN_VANILLA.items()):
        for lv, mv in adds:
            if f'MOVE_{mv}' not in learn:
                bad.append(f'{const} does not learn {mv}')
    for _, _, was in REPLACED:
        pass
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--report', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()

    if a.report:
        for i, m in enumerate(MOVES):
            p = f"{m['power']:3d}" if m['power'] else '  -'
            print(f"  {FIRST_ID+i}  {m['name']:13s} {m['type']:6s} "
                  f"{m['split'][6:].lower():8s} pow {p}  pp {m['pp']:2d}  "
                  f"anim from {m['anim'][5:]}")
        print()
        for const, adds in LEARN.items():
            for lv, mv in adds:
                print(f'  {const:12s} learns {mv} at {lv}')
        return

    apply(a.dry_run)
    wire_learnsets(a.dry_run)
    print(f'{len(MOVES)} moves written')

    if a.check:
        bad = check()
        if bad:
            sys.exit('\n'.join(bad))
        print('constants, data, names, animations and learnsets all check out')


if __name__ == '__main__':
    sys.exit(main())

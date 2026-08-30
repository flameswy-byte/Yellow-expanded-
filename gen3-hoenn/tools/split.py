#!/usr/bin/env python3
"""Give every move a damage category of its own - the physical/special split.

Gen 3 decides physical or special from the move's *type*: everything up to
Ghost and Steel is physical, everything from Fire on is special. That is why
Emerald's Fire Punch runs off Special Attack and its Shadow Ball runs off
Attack. Gen 4 moved the decision onto the move.

Emerald has no table of Gen 4 categories to copy and this environment cannot
reach one, so the table is built rather than transcribed, in three layers that
can each be checked on their own:

  status      power 0. pokeemerald writes .power = 1 for the fixed-damage
              moves - Seismic Toss, Night Shade, Sonic Boom, the OHKOs - so
              zero really does mean "deals no damage", with no exceptions.
  default     the Gen 3 rule, by type. It is right for about nine moves in ten.
  override    the moves Gen 4 actually changed, listed below by type. Sixty of
              them, each one its own line to argue with.

Every name in the override lists is checked against the move data, so a typo
is an error rather than a silently missing category.

    python3 tools/split.py            # rewrite the table
    python3 tools/split.py --report   # print it by type, to read through
"""
import argparse, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_hoenn as R

MOVES = 'src/data/battle_moves.h'
MARK = '.split'

# Gen 3 splits on the type: TYPE_MYSTERY is 9, and everything below it is
# physical. The special types are Fire, Water, Grass, Electric, Psychic, Ice,
# Dragon and Dark.
SPECIAL_TYPES = {'TYPE_FIRE', 'TYPE_WATER', 'TYPE_GRASS', 'TYPE_ELECTRIC',
                 'TYPE_PSYCHIC', 'TYPE_ICE', 'TYPE_DRAGON', 'TYPE_DARK',
                 # Fairy did not exist in Gen 3 and so has no Gen 3 default.
                 # Listed as special because most Fairy moves are; it makes no
                 # difference today, since all three of our Fairy moves deal no
                 # damage, but it is the right default for a fourth.
                 'TYPE_FAIRY'}

# Special-typed moves that Gen 4 made physical: the punches, the bites, the
# ones you hit something with.
PHYSICAL = """
FIRE_PUNCH FLAME_WHEEL SACRED_FIRE BLAZE_KICK
WATERFALL CRABHAMMER DIVE CLAMP
VINE_WHIP RAZOR_LEAF BULLET_SEED NEEDLE_ARM LEAF_BLADE
THUNDER_PUNCH SPARK VOLT_TACKLE
ICE_PUNCH ICE_BALL ICICLE_SPEAR
DRAGON_CLAW OUTRAGE
BITE THIEF FAINT_ATTACK PURSUIT BEAT_UP CRUNCH KNOCK_OFF
""".split()

# Physical-typed moves that Gen 4 made special: the beams, the gusts, the
# sounds and the fumes.
SPECIAL = """
SONIC_BOOM SWIFT TRI_ATTACK HYPER_VOICE UPROAR SNORE WEATHER_BALL
HIDDEN_POWER SPIT_UP
GUST AIR_CUTTER AEROBLAST
ACID SMOG SLUDGE SLUDGE_BOMB
MUD_SLAP MUD_SHOT
ANCIENT_POWER
SIGNAL_BEAM SILVER_WIND
NIGHT_SHADE SHADOW_BALL
DOOM_DESIRE
""".split()

def parse(text):
    """(name, body) for every move entry, in file order."""
    return re.findall(r'\[(MOVE_\w+)\] =\s*\{(.*?)\n    \},', text, re.S)

def field(body, key):
    m = re.search(rf'\.{key}\s*=\s*([^,\n]+),', body)
    return m.group(1).strip() if m else ''

def split_of(name, body):
    if field(body, 'power') == '0':
        return 'SPLIT_STATUS'
    short = name[5:]
    if short in PHYSICAL:
        return 'SPLIT_PHYSICAL'
    if short in SPECIAL:
        return 'SPLIT_SPECIAL'
    return ('SPLIT_SPECIAL' if field(body, 'type') in SPECIAL_TYPES
            else 'SPLIT_PHYSICAL')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--report', action='store_true')
    ap.add_argument('--check', action='store_true',
                    help='verify the table as written, and exit non-zero if not')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    path = f'{R.ROOT}/{MOVES}'
    text = open(path).read()
    moves = parse(text)
    have = {n[5:] for n, _ in moves}

    unknown = [m for m in PHYSICAL + SPECIAL if m not in have]
    if unknown:
        sys.exit('no such move: ' + ', '.join(unknown))
    both = set(PHYSICAL) & set(SPECIAL)
    if both:
        sys.exit('listed twice: ' + ', '.join(sorted(both)))
    dead = [m for m in PHYSICAL + SPECIAL
            if field(dict(moves)['MOVE_' + m], 'power') == '0']
    if dead:
        sys.exit('these deal no damage and cannot have a category: '
                 + ', '.join(dead))

    out, n = text, 0
    for name, body in moves:
        want = split_of(name, body)
        cur = field(body, 'split')
        if cur == want:
            continue
        if cur:
            new = re.sub(r'\.split\s*=\s*[^,\n]+,', f'.split = {want},', body)
        else:
            # after .type, which is what the category used to be read from
            new = re.sub(r'(\n(\s*)\.type\s*=\s*[^,\n]+,)',
                         rf'\1\n\2.split = {want},', body, count=1)
            if new == body:
                new = body.rstrip() + f'\n        .split = {want},'
        out = out.replace(f'[{name}] =\n    {{{body}\n    }},',
                          f'[{name}] =\n    {{{new}\n    }},', 1)
        n += 1
    if not a.dry_run and n:
        open(path, 'w').write(out)

    if a.check:
        wrote = parse(open(path).read())
        bad = []
        for name, body in wrote:
            got, want = field(body, 'split'), split_of(name, body)
            if not got:
                bad.append(f'{name} has no category')
            elif got != want:
                bad.append(f'{name} is {got}, should be {want}')
            elif (field(body, 'power') == '0') != (got == 'SPLIT_STATUS'):
                bad.append(f'{name} disagrees with its own power')
        if bad:
            sys.exit('\n'.join(bad[:20]))
        print(f'{len(wrote)} moves all have a category that matches the rule')

    counts = {}
    for name, body in moves:
        counts[split_of(name, body)] = counts.get(split_of(name, body), 0) + 1
    print(f'{len(moves)} moves: '
          + ', '.join(f'{k[6:].lower()} {v}' for k, v in sorted(counts.items()))
          + f'; {n} rewritten')
    print(f'{len(PHYSICAL)} special-typed moves made physical, '
          f'{len(SPECIAL)} physical-typed made special')

    if a.report:
        by = {}
        for name, body in moves:
            if field(body, 'power') == '0':
                continue
            by.setdefault(field(body, 'type'), []).append(
                (name[5:], split_of(name, body)[6:].lower()))
        for t in sorted(by):
            d = 'special' if t in SPECIAL_TYPES else 'physical'
            odd = [f'{m} -> {s}' for m, s in by[t] if s != d]
            print(f'\n{t[5:]:9s} {len(by[t]):3d} damaging moves, {d} by default')
            if odd:
                print('   ' + '\n   '.join(odd))

if __name__ == '__main__':
    sys.exit(main())

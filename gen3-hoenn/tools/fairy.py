#!/usr/bin/env python3
"""Retype the species and moves Gen 6 moved to Fairy.

The type itself - the constant, the chart, the two icons, the name, the
pokedex search, the trading board - is a one-off structural change and lives in
the source. What this tool does is the repetitive half: the eighteen species
and three moves that changed hands, written as a table that can be read and
argued with rather than as a diff.

Only species that exist in Emerald are listed. Gen 6 retyped a good many more,
but Cottonee, Flabebe and the rest are not in this game to retype.

Every name is checked against the data, so a typo is an error rather than a
silently missing change, and every current type is checked against what Gen 3
had, so running this against an already-edited tree cannot quietly move a
species twice.

    python3 tools/fairy.py            # apply
    python3 tools/fairy.py --check    # verify what is written, non-zero if not
    python3 tools/fairy.py --report   # print the table to read through
"""
import argparse, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_hoenn as R

SPECIES = 'src/data/pokemon/species_info.h'
MOVES = 'src/data/battle_moves.h'
CHART = 'src/battle_main.c'

# species: name -> (types before, types after). The "before" half is what makes
# this safe to run twice.
RETYPE = {
    # the fairies proper - wholly Fairy from Gen 6
    'CLEFFA':     (('NORMAL', 'NORMAL'), ('FAIRY', 'FAIRY')),
    'CLEFAIRY':   (('NORMAL', 'NORMAL'), ('FAIRY', 'FAIRY')),
    'CLEFABLE':   (('NORMAL', 'NORMAL'), ('FAIRY', 'FAIRY')),
    'TOGEPI':     (('NORMAL', 'NORMAL'), ('FAIRY', 'FAIRY')),
    'SNUBBULL':   (('NORMAL', 'NORMAL'), ('FAIRY', 'FAIRY')),
    'GRANBULL':   (('NORMAL', 'NORMAL'), ('FAIRY', 'FAIRY')),
    # kept their first type and gained Fairy as a second
    'IGGLYBUFF':  (('NORMAL', 'NORMAL'), ('NORMAL', 'FAIRY')),
    'JIGGLYPUFF': (('NORMAL', 'NORMAL'), ('NORMAL', 'FAIRY')),
    'WIGGLYTUFF': (('NORMAL', 'NORMAL'), ('NORMAL', 'FAIRY')),
    'AZURILL':    (('NORMAL', 'NORMAL'), ('NORMAL', 'FAIRY')),
    'MARILL':     (('WATER', 'WATER'),   ('WATER', 'FAIRY')),
    'AZUMARILL':  (('WATER', 'WATER'),   ('WATER', 'FAIRY')),
    'MR_MIME':    (('PSYCHIC', 'PSYCHIC'), ('PSYCHIC', 'FAIRY')),
    'RALTS':      (('PSYCHIC', 'PSYCHIC'), ('PSYCHIC', 'FAIRY')),
    'KIRLIA':     (('PSYCHIC', 'PSYCHIC'), ('PSYCHIC', 'FAIRY')),
    'GARDEVOIR':  (('PSYCHIC', 'PSYCHIC'), ('PSYCHIC', 'FAIRY')),
    'MAWILE':     (('STEEL', 'STEEL'),   ('STEEL', 'FAIRY')),
    # Togetic keeps Flying in the second slot, so Fairy replaces the first
    'TOGETIC':    (('NORMAL', 'FLYING'), ('FAIRY', 'FLYING')),
}

# Species that are Fairy by design rather than by retyping, and so are not
# this tool's business - but --check counts every Fairy in the game, so it has
# to be told about them or it reports a species it cannot account for. Alolan
# Ninetales arrives Ice/Fairy from tools/newmons.py.
BY_DESIGN = {'NINETALES_A'}

# the three Gen 3 moves Gen 6 made Fairy. All are status moves, so the
# physical/special split is not affected by the change of type.
MOVE_RETYPE = {'CHARM': 'NORMAL', 'SWEET_KISS': 'NORMAL', 'MOONLIGHT': 'NORMAL'}

# what the chart should say once Fairy is in it, as (attacker, defender, x2 or
# x0.5 or x0). Gen 6, which is also CFRU's.
WANT = [
    ('FAIRY', 'FIGHTING', 'SUPER_EFFECTIVE'),
    ('FAIRY', 'DRAGON', 'SUPER_EFFECTIVE'),
    ('FAIRY', 'DARK', 'SUPER_EFFECTIVE'),
    ('FAIRY', 'FIRE', 'NOT_EFFECTIVE'),
    ('FAIRY', 'POISON', 'NOT_EFFECTIVE'),
    ('FAIRY', 'STEEL', 'NOT_EFFECTIVE'),
    ('POISON', 'FAIRY', 'SUPER_EFFECTIVE'),
    ('STEEL', 'FAIRY', 'SUPER_EFFECTIVE'),
    ('FIGHTING', 'FAIRY', 'NOT_EFFECTIVE'),
    ('BUG', 'FAIRY', 'NOT_EFFECTIVE'),
    ('DARK', 'FAIRY', 'NOT_EFFECTIVE'),
    ('DRAGON', 'FAIRY', 'NO_EFFECT'),
]
# Gen 6 also took two resistances off Steel, which is a change to the existing
# chart rather than an addition, so it is checked by absence.
GONE = [('DARK', 'STEEL'), ('GHOST', 'STEEL')]


def entries(text):
    """(species, type1, type2, span) for every species, in file order."""
    out = []
    for m in re.finditer(r'\[SPECIES_(\w+)\] =\s*\{(.*?)\n    \},', text, re.S):
        t = re.search(r'\.types = \{ TYPE_(\w+), TYPE_(\w+) \}', m.group(2))
        if t:
            out.append((m.group(1), t.group(1), t.group(2), t.span(0)))
    return out


def chart(text):
    body = text[text.index('gTypeEffectiveness'):]
    body = body[body.index('{'):body.index('\n};')]
    return re.findall(r'TYPE_(\w+), TYPE_(\w+), TYPE_MUL_(\w+)', body)


def apply(path, dry):
    text = open(path).read()
    have = {n for n, _, _, _ in entries(text)}
    unknown = [n for n in RETYPE if n not in have]
    if unknown:
        sys.exit('no such species: ' + ', '.join(unknown))

    out, done, already = text, 0, 0
    for name, t1, t2, _ in entries(text):
        if name not in RETYPE:
            continue
        before, after = RETYPE[name]
        if (t1, t2) == after:
            already += 1
            continue
        if (t1, t2) != before:
            sys.exit(f'{name} is {t1}/{t2}, expected {before[0]}/{before[1]} '
                     'before retyping - the table and the data disagree')
        # replace only inside this species' own block - the same .types line
        # appears on hundreds of species, so a global replace would be wrong
        i = out.index(f'[SPECIES_{name}] =')
        j = out.index('\n    },', i)
        block = out[i:j]
        out = out[:i] + block.replace(
            f'.types = {{ TYPE_{t1}, TYPE_{t2} }}',
            f'.types = {{ TYPE_{after[0]}, TYPE_{after[1]} }}', 1) + out[j:]
        done += 1
    if not dry and done:
        open(path, 'w').write(out)
    return done, already


def apply_moves(path, dry):
    text = open(path).read()
    done, already = 0, 0
    for name, was in MOVE_RETYPE.items():
        i = text.find(f'[MOVE_{name}] =')
        if i < 0:
            sys.exit(f'no such move: {name}')
        j = text.index('\n    },', i)
        block = text[i:j]
        if '.type = TYPE_FAIRY' in block:
            already += 1
            continue
        if f'.type = TYPE_{was}' not in block:
            sys.exit(f'{name} is not TYPE_{was}; the table and the data disagree')
        text = text[:i] + block.replace(f'.type = TYPE_{was}',
                                        '.type = TYPE_FAIRY', 1) + text[j:]
        done += 1
    if not dry and done:
        open(path, 'w').write(text)
    return done, already


def check():
    bad = []
    species = entries(open(f'{R.ROOT}/{SPECIES}').read())
    got = {n: (a, b) for n, a, b, _ in species}
    for name, (_, after) in RETYPE.items():
        if got.get(name) != after:
            bad.append(f'{name} is {got.get(name)}, should be {after}')
    fairies = [n for n, a, b, _ in species if 'FAIRY' in (a, b)]
    unexplained = set(fairies) - set(RETYPE) - BY_DESIGN
    if unexplained:
        bad.append(f'{len(fairies)} species are Fairy; these are neither in the '
                   'retype table nor Fairy by design: ' + ', '.join(sorted(unexplained)))
    missing = BY_DESIGN - set(fairies)
    if missing:
        bad.append('expected to be Fairy by design but is not: '
                   + ', '.join(sorted(missing)))

    moves = open(f'{R.ROOT}/{MOVES}').read()
    for name in MOVE_RETYPE:
        i = moves.find(f'[MOVE_{name}] =')
        if '.type = TYPE_FAIRY' not in moves[i:moves.index('\n    },', i)]:
            bad.append(f'MOVE_{name} is not Fairy')

    rows = chart(open(f'{R.ROOT}/{CHART}').read())
    have = {(a, d) for a, d, _ in rows}
    for a, d, mul in WANT:
        if (a, d, mul) not in rows:
            bad.append(f'chart is missing {a} -> {d} = {mul}')
    for a, d in GONE:
        if (a, d) in have:
            bad.append(f'chart still resists {a} -> {d}; Gen 6 removed that')
    # nothing should point at a type the game does not have
    for a, d, _ in rows:
        for t in (a, d):
            if t in ('FORESIGHT', 'ENDTABLE'):
                continue
            if f'TYPE_{t} ' not in open(f'{R.ROOT}/include/constants/pokemon.h').read():
                bad.append(f'chart names TYPE_{t}, which is not defined')
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--report', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()

    s_done, s_already = apply(f'{R.ROOT}/{SPECIES}', a.dry_run)
    m_done, m_already = apply_moves(f'{R.ROOT}/{MOVES}', a.dry_run)
    print(f'{len(RETYPE)} species: {s_done} retyped, {s_already} already were')
    print(f'{len(MOVE_RETYPE)} moves: {m_done} retyped, {m_already} already were')

    if a.check:
        bad = check()
        if bad:
            sys.exit('\n'.join(bad))
        rows = chart(open(f'{R.ROOT}/{CHART}').read())
        print(f'chart has {len(rows)} entries, all {len(WANT)} Fairy ones present, '
              f'both Gen 6 Steel resistances removed')

    if a.report:
        print()
        for name, (before, after) in sorted(RETYPE.items(), key=lambda kv: kv[1][1]):
            b = before[0] if before[0] == before[1] else '/'.join(before)
            f = after[0] if after[0] == after[1] else '/'.join(after)
            print(f'   {name:11s} {b:15s} -> {f}')
        print()
        for name, was in sorted(MOVE_RETYPE.items()):
            print(f'   {name:11s} {was:15s} -> FAIRY')


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""Add six Pokemon from later generations, in slots Emerald already has spare.

Emerald reserves species 252-276 for SPECIES_OLD_UNOWN_B..Z - twenty-five slots
left over from a scrapped Unown implementation. They are dead weight that every
per-species table in the game already carries a row for: base stats, sprites,
palettes, icons, footprints, learnsets, pokedex numbers, Hoenn order. That is
what makes this cheap. NUM_SPECIES does not move, no table is resized, and no
save layout changes; the rows are overwritten rather than inserted.

The six, and why each one is here rather than some other six: they were asked
for.

    Larvesta     Bug/Fire      -> Volcarona at 59
    Volcarona    Bug/Fire
    Wimpod       Bug/Water     -> Golisopod at 30
    Golisopod    Bug/Water
    Vulpix-A     Ice           -> Ninetales-A at 35
    Ninetales-A  Ice/Fairy

The Alolan forms are separate species here, not forms - Gen 3 has no form
system - so ordinary Vulpix still evolves into ordinary Ninetales with a Fire
Stone, and these two live alongside them. Ninetales-A is the first Pokemon in
the game to be part Fairy by design rather than by retyping.

Three things could not be brought across as they are, and are substituted
rather than faked:

  abilities   Wimp Out, Emergency Exit, Snow Cloak and Snow Warning are all
              Gen 4+ and do not exist in this engine. Each is replaced by the
              nearest thing that does, named in ABILITY_NOTE below.
  evolution   Alolan Vulpix evolves with an Ice Stone, which Gen 3 does not
              have. It evolves at level 35 here instead of inventing an item
              with no icon and no shop to sell it.
  dex text    written for this game rather than copied.

    python3 tools/newmons.py            # apply
    python3 tools/newmons.py --check    # verify what is written
    python3 tools/newmons.py --report   # print the table to read through
"""
import argparse, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_hoenn as R

# The slots being taken over, in order. Species 252-257, national dex 387-392.
SLOTS = ['B', 'C', 'D', 'E', 'F', 'G']

ABILITY_NOTE = {
    'WIMPOD':      'Wimp Out -> Run Away, which is the same idea and exists',
    'GOLISOPOD':   'Emergency Exit -> Intimidate; nothing here flees on damage, '
                   'and Intimidate plays the same defensive-pivot role',
    'VULPIX_A':    'Snow Cloak -> Cute Charm as the second slot; no hail-evasion ability exists. Snow Warning is real - see below',
    'NINETALES_A': 'Snow Warning is not a substitution: it was added to the '
                   'engine for these two. Snow Cloak still has no equivalent, '
                   'so Cute Charm fills the second slot',
}

# name, dir, dex name, category, types, base stats (HP Atk Def Spe SpA SpD),
# catch, exp, EV yield, gender, egg cycles, growth, egg groups, abilities,
# body colour, height (dm), weight (hg), dex text
MONS = [
    dict(const='LARVESTA', dir='larvesta', name='LARVESTA', cat='Torch',
         types=('BUG', 'FIRE'), stats=(55, 85, 55, 60, 50, 55),
         catch=45, exp=72, ev=dict(Attack=1), gender='PERCENT_FEMALE(50)',
         cycles=40, growth='GROWTH_SLOW', eggs=('BUG', 'BUG'),
         abilities=('FLAME_BODY', 'SWARM'), color='WHITE',
         height=11, weight=288, cry='larvesta',
         text="It is said to have been born in\n"
              "the sun. The five horns on its\n"
              "head shoot flames when it is\n"
              "threatened."),
    dict(const='VOLCARONA', dir='volcarona', name='VOLCARONA', cat='Sun',
         types=('BUG', 'FIRE'), stats=(85, 60, 65, 100, 135, 105),
         catch=15, exp=248, ev=dict(SpAttack=3), gender='PERCENT_FEMALE(50)',
         cycles=40, growth='GROWTH_SLOW', eggs=('BUG', 'BUG'),
         abilities=('FLAME_BODY', 'SWARM'), color='WHITE',
         height=16, weight=460, cry='volcarona',
         text="When volcanic ash blackened the\n"
              "sky, it is said this POKéMON's\n"
              "flames took the place of the\n"
              "sun."),
    dict(const='WIMPOD', dir='wimpod', name='WIMPOD', cat='Turn Tail',
         types=('BUG', 'WATER'), stats=(25, 35, 40, 80, 20, 30),
         catch=90, exp=46, ev=dict(Speed=1), gender='PERCENT_FEMALE(50)',
         cycles=20, growth='GROWTH_MEDIUM_FAST', eggs=('BUG', 'WATER_3'),
         abilities=('RUN_AWAY', 'SWIFT_SWIM'), color='GRAY',
         height=5, weight=120, cry='wimpod',
         text="A cowardly scavenger. It flees\n"
              "the instant anything comes near,\n"
              "leaving the shore it was picking\n"
              "over spotlessly clean."),
    dict(const='GOLISOPOD', dir='golisopod', name='GOLISOPOD', cat='Hard Scale',
         types=('BUG', 'WATER'), stats=(75, 125, 140, 40, 60, 90),
         catch=45, exp=186, ev=dict(Defense=2), gender='PERCENT_FEMALE(50)',
         cycles=20, growth='GROWTH_MEDIUM_FAST', eggs=('BUG', 'WATER_3'),
         abilities=('INTIMIDATE', 'SWIFT_SWIM'), color='GRAY',
         height=20, weight=1080, cry='golisopod',
         text="It lives in caves along the\n"
              "shore. Its six arms are folded\n"
              "in what looks like meditation,\n"
              "until the moment it strikes."),
    dict(const='VULPIX_A', dir='vulpix_a', name='VULPIX', cat='Fox',
         types=('ICE', 'ICE'), stats=(38, 41, 40, 65, 50, 65),
         catch=190, exp=63, ev=dict(Speed=1), gender='PERCENT_FEMALE(75)',
         cycles=20, growth='GROWTH_MEDIUM_FAST', eggs=('FIELD', 'FIELD'),
         abilities=('SNOW_WARNING', 'CUTE_CHARM'), color='WHITE',
         height=6, weight=99, cry='vulpix',
         text="A form that settled on snowy\n"
              "mountains. It breathes air cold\n"
              "enough to freeze its own\n"
              "footprints behind it."),
    dict(const='NINETALES_A', dir='ninetales_a', name='NINETALES', cat='Fox',
         types=('ICE', 'FAIRY'), stats=(73, 67, 75, 109, 81, 100),
         catch=75, exp=178, ev=dict(SpDefense=1, Speed=1),
         gender='PERCENT_FEMALE(75)',
         cycles=20, growth='GROWTH_MEDIUM_FAST', eggs=('FIELD', 'FIELD'),
         abilities=('SNOW_WARNING', 'CUTE_CHARM'), color='BLUE',
         height=11, weight=199, cry='ninetales',
         text="Revered as a guardian of the\n"
              "peaks. It is said to guide the\n"
              "lost down the mountain, and to\n"
              "bury those who anger it."),
]

EVOLUTIONS = {
    'LARVESTA': ('EVO_LEVEL', 59, 'VOLCARONA'),
    'WIMPOD':   ('EVO_LEVEL', 30, 'GOLISOPOD'),
    'VULPIX_A': ('EVO_LEVEL', 35, 'NINETALES_A'),
}

# Level-up learnsets, restricted to moves that exist in Emerald. Where the real
# moveset leans on moves from later generations - First Impression, Fiery
# Dance, Quiver Dance, Aurora Veil - the nearest Gen 3 move stands in.
LEARNSETS = {
    'LARVESTA': [(1, 'EMBER'), (1, 'STRING_SHOT'), (10, 'LEECH_LIFE'),
                 (20, 'TAKE_DOWN'), (30, 'FLAME_WHEEL'), (40, 'FURY_CUTTER'),
                 (50, 'AMNESIA'), (60, 'FLAMETHROWER'), (70, 'DOUBLE_EDGE')],
    'VOLCARONA': [(1, 'EMBER'), (1, 'GUST'), (1, 'LEECH_LIFE'),
                  (30, 'FLAME_WHEEL'), (40, 'SILVER_WIND'), (50, 'AMNESIA'),
                  (59, 'AGILITY'), (64, 'FLAMETHROWER'), (70, 'SIGNAL_BEAM'),
                  (76, 'HYPER_BEAM'), (82, 'OVERHEAT')],
    'WIMPOD': [(1, 'LEECH_LIFE'), (1, 'SAND_ATTACK'), (5, 'TAUNT'),
               (9, 'FURY_CUTTER'), (13, 'WATER_GUN'), (17, 'DEFENSE_CURL'),
               (21, 'RAPID_SPIN'), (25, 'SLASH'), (29, 'WATER_PULSE')],
    'GOLISOPOD': [(1, 'SLASH'), (1, 'FURY_CUTTER'), (1, 'WATER_PULSE'),
                  (30, 'SWORDS_DANCE'), (36, 'IRON_DEFENSE'), (42, 'CRUNCH'),
                  (48, 'SURF'), (54, 'MEGAHORN'), (60, 'SUPERPOWER')],
    'VULPIX_A': [(1, 'POWDER_SNOW'), (1, 'TAIL_WHIP'), (9, 'ROAR'),
                 (13, 'QUICK_ATTACK'), (17, 'ICY_WIND'), (21, 'CONFUSE_RAY'),
                 (25, 'ICE_BEAM'), (29, 'SAFEGUARD'), (33, 'IMPRISON'),
                 (37, 'BLIZZARD'), (41, 'GRUDGE'), (45, 'ATTRACT')],
    'NINETALES_A': [(1, 'POWDER_SNOW'), (1, 'QUICK_ATTACK'), (1, 'CONFUSE_RAY'),
                    (1, 'SAFEGUARD'), (35, 'ICY_WIND'), (43, 'ICE_BEAM'),
                    (51, 'EXTRASENSORY'), (59, 'BLIZZARD'), (67, 'HAIL')],
}

# TMs and HMs each can learn, by TM/HM member name in struct TMHMLearnset.
TMHM = {
    'LARVESTA': 'TOXIC SUNNY_DAY SWIFT PROTECT FRUSTRATION RETURN '
                'DOUBLE_TEAM FACADE REST ATTRACT OVERHEAT SECRET_POWER '
                'FLAMETHROWER FIRE_BLAST SOLAR_BEAM',
    'VOLCARONA': 'TOXIC SUNNY_DAY SWIFT PROTECT FRUSTRATION RETURN '
                 'DOUBLE_TEAM FACADE REST ATTRACT OVERHEAT SECRET_POWER '
                 'FLAMETHROWER FIRE_BLAST SOLAR_BEAM SAFEGUARD LIGHT_SCREEN '
                 'REFLECT HYPER_BEAM AERIAL_ACE FLY',
    'WIMPOD': 'TOXIC PROTECT FRUSTRATION RETURN DOUBLE_TEAM FACADE REST '
              'ATTRACT SECRET_POWER SURF DIVE RAIN_DANCE ROCK_TOMB CUT',
    'GOLISOPOD': 'TOXIC PROTECT FRUSTRATION RETURN DOUBLE_TEAM FACADE REST '
                 'ATTRACT SECRET_POWER SURF DIVE RAIN_DANCE ROCK_TOMB CUT '
                 'BRICK_BREAK EARTHQUAKE IRON_TAIL AERIAL_ACE STRENGTH '
                 'ROCK_SMASH WATERFALL',
    'VULPIX_A': 'TOXIC HAIL BLIZZARD ICE_BEAM PROTECT FRUSTRATION RETURN '
                'DOUBLE_TEAM FACADE REST ATTRACT SECRET_POWER SAFEGUARD '
                'SWIFT RAIN_DANCE',
    'NINETALES_A': 'TOXIC HAIL BLIZZARD ICE_BEAM PROTECT FRUSTRATION RETURN '
                   'DOUBLE_TEAM FACADE REST ATTRACT SECRET_POWER SAFEGUARD '
                   'SWIFT RAIN_DANCE CALM_MIND PSYCHIC LIGHT_SCREEN '
                   'REFLECT HYPER_BEAM SHADOW_BALL',
}


# Whose footprint, animation scripts and dex-page scaling each one borrows.
# Animation scripts are generic and shared; borrowing from the nearest body
# plan is cheaper and looks better than keeping the Old Unown placeholders.
BORROW = {'LARVESTA': 'Wurmple', 'VOLCARONA': 'Masquerain', 'WIMPOD': 'Anorith',
          'GOLISOPOD': 'Armaldo', 'VULPIX_A': 'Vulpix', 'NINETALES_A': 'Ninetales'}

# Which of the three shared icon palettes each icon was remapped onto when the
# sprites were converted. Icons do not carry their own palette in this engine.
ICON_PAL = {'LARVESTA': 0, 'VOLCARONA': 0, 'WIMPOD': 2,
            'GOLISOPOD': 2, 'VULPIX_A': 0, 'NINETALES_A': 2}

EV_FIELDS = ('HP', 'Attack', 'Defense', 'Speed', 'SpAttack', 'SpDefense')
FIRST_CRY_ID = 388          # first free slot past vanilla's 388-entry cry table


def camel(const):
    """LARVESTA -> Larvesta, VULPIX_A -> VulpixA"""
    return ''.join(p.capitalize() for p in const.split('_'))


def read(path):
    return open(f'{R.ROOT}/{path}').read()


def write(path, text, dry):
    if not dry:
        open(f'{R.ROOT}/{path}', 'w').write(text)


def swap(path, pairs, dry):
    """Apply (old, new) replacements. Idempotent: a pair whose `new` is already
    present is skipped, and anything that matches neither is an error."""
    t = read(path)
    for old, new in pairs:
        if old in t:
            t = t.replace(old, new, 1)
        elif new not in t:
            sys.exit(f'{path}: matched neither\n  old: {old.strip()[:78]}\n'
                     f'  new: {new.strip()[:78]}')
    write(path, t, dry)


def species_block(m):
    hp, atk, df, spe, spa, spd = m['stats']
    ev = '\n'.join(f"        .evYield_{f:<10s} = {m['ev'].get(f, 0)},"
                   for f in EV_FIELDS)
    return f"""    [SPECIES_{m['const']}] =
    {{
        .baseHP        = {hp},
        .baseAttack    = {atk},
        .baseDefense   = {df},
        .baseSpeed     = {spe},
        .baseSpAttack  = {spa},
        .baseSpDefense = {spd},
        .types = {{ TYPE_{m['types'][0]}, TYPE_{m['types'][1]} }},
        .catchRate = {m['catch']},
        .expYield = {m['exp']},
{ev}
        .itemCommon = ITEM_NONE,
        .itemRare   = ITEM_NONE,
        .genderRatio = {m['gender']},
        .eggCycles = {m['cycles']},
        .friendship = STANDARD_FRIENDSHIP,
        .growthRate = {m['growth']},
        .eggGroups = {{ EGG_GROUP_{m['eggs'][0]}, EGG_GROUP_{m['eggs'][1]} }},
        .abilities = {{ABILITY_{m['abilities'][0]}, ABILITY_{m['abilities'][1]}}},
        .safariZoneFleeRate = 0,
        .bodyColor = BODY_COLOR_{m['color']},
        .noFlip = FALSE,
    }},"""


def rename_slots(dry):
    """Every per-species and per-dex table already carries an OLD_UNOWN row, so
    most of the wiring comes free: rename the constant and the tables follow."""
    pairs = []
    for slot, m in zip(SLOTS, MONS):
        for pre in ('SPECIES_OLD_UNOWN_', 'NATIONAL_DEX_OLD_UNOWN_',
                    'HOENN_DEX_OLD_UNOWN_'):
            pairs.append((pre + slot, pre.replace('OLD_UNOWN_', '') + m['const']))
        # several macros take the bare name: SPECIES_TO_NATIONAL(X),
        # HOENN_TO_NATIONAL(X), SPECIES_SPRITE(X, sym), SPECIES_PAL(X, sym)
        pairs.append((f'(OLD_UNOWN_{slot})', f"({m['const']})"))
        pairs.append((f'(OLD_UNOWN_{slot},', f"({m['const']},"))
    n = 0
    for root, dirs, files in os.walk(R.ROOT):
        dirs[:] = [d for d in dirs if d not in ('build', '.git')]
        for f in files:
            if not f.endswith(('.c', '.h', '.inc', '.s', '.json')):
                continue
            p = os.path.join(root, f)
            try:
                t = o = open(p).read()
            except UnicodeDecodeError:
                continue
            for a, b in pairs:
                t = t.replace(a, b)
            if t != o:
                n += 1
                if not dry:
                    open(p, 'w').write(t)
    return n


def fill_tables(dry):
    """Fill in the rows the rename just claimed."""
    per_file = {
        'src/data/pokemon/species_info.h': [],
        'src/data/text/species_names.h': [],
        'src/data/pokemon_graphics/front_pic_table.h': [],
        'src/data/pokemon_graphics/back_pic_table.h': [],
        'src/data/pokemon_graphics/still_front_pic_table.h': [],
        'src/data/pokemon_graphics/palette_table.h': [],
        'src/data/pokemon_graphics/shiny_palette_table.h': [],
        'src/data/pokemon_graphics/front_pic_coordinates.h': [],
        'src/data/pokemon_graphics/back_pic_coordinates.h': [],
        'src/data/pokemon_graphics/footprint_table.h': [],
        'src/data/pokemon_graphics/front_pic_anims.h': [],
        'src/data/pokemon_graphics/unused_anims.h': [],
        'src/pokemon_icon.c': [],
    }
    for slot, m in zip(SLOTS, MONS):
        C, S, B = m['const'], camel(m['const']), BORROW[m['const']]
        P = per_file
        # species_info is rewritten wholesale rather than matched on the
        # placeholder, so editing the table above and re-running works. The
        # other rows are one-line swaps where the new text is stable.
        P['src/data/pokemon/species_info.h'].append((None, m))
        P['src/data/text/species_names.h'].append(
            (f'[SPECIES_{C}] = _("?")', f'[SPECIES_{C}] = _("{m["name"]}")'))
        # the three sprite tables share a macro but not their column spacing
        for f, sym, gap in (('front_pic_table.h', 'gMonFrontPic', ' '),
                            ('back_pic_table.h', 'gMonBackPic', ' '),
                            ('still_front_pic_table.h', 'gMonStillFrontPic', '   ')):
            P[f'src/data/pokemon_graphics/{f}'].append(
                (f'SPECIES_SPRITE({C},{gap}{sym}_DoubleQuestionMark)',
                 f'SPECIES_SPRITE({C},{gap}{sym}_{S})'))
        P['src/data/pokemon_graphics/palette_table.h'].append(
            (f'SPECIES_PAL({C}, gMonPalette_DoubleQuestionMark)',
             f'SPECIES_PAL({C}, gMonPalette_{S})'))
        P['src/data/pokemon_graphics/shiny_palette_table.h'].append(
            (f'SPECIES_SHINY_PAL({C}, gMonShinyPalette_DoubleQuestionMark)',
             f'SPECIES_SHINY_PAL({C}, gMonShinyPalette_{S})'))
        P['src/data/pokemon_graphics/front_pic_coordinates.h'].append(
            (f'[SPECIES_{C}] = {{ .size = MON_COORDS_SIZE(64, 56), .y_offset =  4 }}',
             f'[SPECIES_{C}] = {{ .size = MON_COORDS_SIZE(64, 64), .y_offset =  0 }}'))
        P['src/data/pokemon_graphics/back_pic_coordinates.h'].append(
            (f'[SPECIES_{C}] = {{ .size = MON_COORDS_SIZE(64, 64), .y_offset =  2 }}',
             f'[SPECIES_{C}] = {{ .size = MON_COORDS_SIZE(64, 64), .y_offset =  0 }}'))
        P['src/data/pokemon_graphics/footprint_table.h'].append(
            (f'[SPECIES_{C}] = gMonFootprint_QuestionMark',
             f'[SPECIES_{C}] = gMonFootprint_{S}'))
        P['src/data/pokemon_graphics/front_pic_anims.h'].append(
            (f'[SPECIES_{C}] = sAnims_OldUnownB,',
             f'[SPECIES_{C}] = sAnims_{B},'))
        P['src/data/pokemon_graphics/unused_anims.h'].append(
            (f'[SPECIES_{C}] = sUnusedAnims_OldUnownB,',
             f'[SPECIES_{C}] = sUnusedAnims_{B},'))
        P['src/pokemon_icon.c'].append(
            (f'[SPECIES_{C}] = gMonIcon_QuestionMark',
             f'[SPECIES_{C}] = gMonIcon_{S}'))
        P['src/pokemon_icon.c'].append(
            (f'    [SPECIES_{C}] = 0,', f'    [SPECIES_{C}] = {ICON_PAL[C]},'))

    info = per_file.pop('src/data/pokemon/species_info.h')
    src = read('src/data/pokemon/species_info.h')
    for _, m in info:
        C = m['const']
        placeholder = f'    [SPECIES_{C}] = OLD_UNOWN_SPECIES_INFO,'
        if placeholder in src:
            src = src.replace(placeholder, species_block(m), 1)
            continue
        mm = re.search(rf'    \[SPECIES_{C}\] =\n    \{{.*?\n    \}},', src, re.S)
        if mm is None:
            sys.exit(f'species_info.h has no row for SPECIES_{C}')
        src = src[:mm.start()] + species_block(m) + src[mm.end():]
    write('src/data/pokemon/species_info.h', src, dry)

    for path, pairs in per_file.items():
        swap(path, pairs, dry)


def add_graphics_symbols(dry):
    """Declare the image and palette symbols the tables now point at."""
    decls, anim = [], []
    for m in MONS:
        S, d = camel(m['const']), m['dir']
        g = f'graphics/pokemon/{d}'
        decls.append(
            f'const u32 gMonStillFrontPic_{S}[] = INCGFX_U32("{g}/front.png", ".4bpp.lz");\n'
            f'const u32 gMonPalette_{S}[] = INCGFX_U32("{g}/normal.pal", ".gbapal.lz");\n'
            f'const u32 gMonBackPic_{S}[] = INCGFX_U32("{g}/back.png", ".4bpp.lz");\n'
            f'const u32 gMonShinyPalette_{S}[] = INCGFX_U32("{g}/shiny.pal", ".gbapal.lz");\n'
            f'const u8 gMonIcon_{S}[] = INCGFX_U8("{g}/icon.png", ".4bpp");\n'
            f'const u8 gMonFootprint_{S}[] = INCGFX_U8("{g}/footprint.png", ".1bpp");\n')
        anim.append(f'const u32 gMonFrontPic_{S}[] = '
                    f'INCGFX_U32("{g}/anim_front.png", ".4bpp.lz");\n')

    # data.c only sees the externs, so a definition without one is a link
    # error that reads like a missing symbol
    externs = []
    for m in MONS:
        S = camel(m['const'])
        externs.append(
            f'extern const u32 gMonStillFrontPic_{S}[];\n'
            f'extern const u32 gMonPalette_{S}[];\n'
            f'extern const u32 gMonBackPic_{S}[];\n'
            f'extern const u32 gMonShinyPalette_{S}[];\n'
            f'extern const u32 gMonFrontPic_{S}[];\n'
            f'extern const u8 gMonIcon_{S}[];\n'
            f'extern const u8 gMonFootprint_{S}[];\n')

    mark = '\n// Open Hoenn - tools/newmons.py\n'
    for path, blocks in (('src/data/graphics/pokemon.h', decls),
                         ('src/anim_mon_front_pics.c', anim),
                         ('include/graphics.h', externs)):
        t = read(path)
        if mark in t:
            t = t[:t.index(mark)]
        write(path, t.rstrip() + '\n' + mark + ''.join(blocks), dry)


def wire_cries(dry):
    """Species 251-275 all fall through to Unown's cry in SpeciesToCryId, so
    the six need their own branch. Their samples go past the end of the vanilla
    cry table, which is banked in 128s but not otherwise size-constrained."""
    first, last = MONS[0]['const'], MONS[-1]['const']
    old = """    if (species < SPECIES_TREECKO - 1)
        return SPECIES_UNOWN - 1;
"""
    new = f"""    // The six species added in the Old Unown slots have cries of their own,
    // appended past the end of vanilla's table. Without this they would fall
    // into the branch below and every one of them would sound like Unown.
    if (species >= SPECIES_{first} - 1 && species <= SPECIES_{last} - 1)
        return {FIRST_CRY_ID} + (species - (SPECIES_{first} - 1));

    if (species < SPECIES_TREECKO - 1)
        return SPECIES_UNOWN - 1;
"""
    swap('src/pokemon.c', [(old, new)], dry)

    mark = '\n\t@ Open Hoenn - tools/newmons.py\n'
    t = read('sound/cry_tables.inc')
    if mark in t:
        t = t[:t.index(mark)]
    # the forward table ends where the reverse table begins
    i = t.index('\tcry_reverse ')
    fwd = ''.join(f'\tcry Cry_{camel(m["cry"].upper())}\n' for m in MONS)
    rev = ''.join(f'\tcry_reverse Cry_{camel(m["cry"].upper())}\n' for m in MONS)
    t = t[:i].rstrip('\n') + '\n' + fwd + '\n' + t[i:].rstrip('\n') + '\n' + rev
    write('sound/cry_tables.inc', t + mark, dry)


def add_cry_samples(dry):
    """The four new samples need symbols; the two Alolan forms reuse the cries
    Emerald already has for Vulpix and Ninetales."""
    mark = '\n\t@ Open Hoenn - tools/newmons.py\n'
    t = read('sound/direct_sound_data.inc')
    if mark in t:
        t = t[:t.index(mark)]
    new = ''
    for cry in sorted({m['cry'] for m in MONS}):
        if f'Cry_{camel(cry.upper())}::' in t:
            continue           # vulpix and ninetales already have one
        new += (f'\n\t.align 2\nCry_{camel(cry.upper())}::\n'
                f'\t.incbin "sound/direct_sound_samples/cries/{cry}.bin"\n')
    write('sound/direct_sound_data.inc', t.rstrip('\n') + '\n' + mark + new, dry)


def wire_dex(dry):
    """Pokedex entries, the text they point at, and the count that decides how
    much of the National Dex the game will page through."""
    mark = '\n// Open Hoenn - tools/newmons.py\n'
    t = read('src/data/pokemon/pokedex_text.h')
    if mark in t:
        t = t[:t.index(mark)]
    body = ''.join(f'const u8 g{camel(m["const"])}PokedexText[] = _(\n'
                   + ''.join(f'    "{l}\\n"\n' for l in m['text'].split('\n')[:-1])
                   + f'    "{m["text"].split(chr(10))[-1]}");\n\n'
                   for m in MONS)
    write('src/data/pokemon/pokedex_text.h', t.rstrip() + '\n' + mark + body, dry)

    t = read('src/data/pokemon/pokedex_entries.h')
    if mark in t:
        t = t[:t.index(mark)] + '};\n'
    entries = ''.join(f"""    [NATIONAL_DEX_{m['const']}] =
    {{
        .categoryName = _("{m['cat'].upper()}"),
        .height = {m['height']},
        .weight = {m['weight']},
        .description = g{camel(m['const'])}PokedexText,
        .pokemonScale = 256,
        .pokemonOffset = 0,
        .trainerScale = 256,
        .trainerOffset = 0,
    }},

""" for m in MONS)
    i = t.rindex('};')
    write('src/data/pokemon/pokedex_entries.h',
          t[:i].rstrip() + '\n\n' + mark + entries + '};\n', dry)

    swap('include/constants/pokedex.h',
         [('#define NATIONAL_DEX_COUNT  NATIONAL_DEX_DEOXYS',
           f"#define NATIONAL_DEX_COUNT  NATIONAL_DEX_{MONS[-1]['const']}")], dry)


def wire_orders(dry):
    """The three sort orders. Alphabetical already lists every slot, so the six
    only move; weight and height stop at the vanilla count and have to grow,
    because the loops that read them now run to the new NATIONAL_DEX_COUNT."""
    entries = read('src/data/pokemon/pokedex_entries.h')
    stat = {}
    for mm in re.finditer(r'\[NATIONAL_DEX_(\w+)\] =\s*\{(.*?)\n    \},',
                          entries, re.S):
        d = mm.group(2)
        stat[mm.group(1)] = (int(re.search(r'\.height = (\d+)', d).group(1)),
                             int(re.search(r'\.weight = (\d+)', d).group(1)))

    t = read('src/data/pokemon/pokedex_orders.h')
    ours = [m['const'] for m in MONS]

    def rebuild(table, keyfn):
        m = re.search(rf'(const u16 {table}\[\] =\s*\{{\n)(.*?)(\n\}};)', t, re.S)
        names = re.findall(r'NATIONAL_DEX_(\w+)', m.group(2))
        names = [n for n in names if n not in ours] + ours
        names.sort(key=keyfn)
        body = ''.join(f'    NATIONAL_DEX_{n},\n' for n in names)
        return t.replace(m.group(0), m.group(1) + body.rstrip('\n') + m.group(3))

    # alphabetical: the constant's own suffix is the name the dex shows, near
    # enough - VULPIX_A lands beside VULPIX, which is where it belongs
    order = {n: i for i, n in enumerate(
        re.findall(r'NATIONAL_DEX_(\w+)',
                   re.search(r'gPokedexOrder_Alphabetical\[\] =\s*\{(.*?)\n\};',
                             t, re.S).group(1)))}
    t = rebuild('gPokedexOrder_Alphabetical',
                lambda n: (n.replace('_', ''), order.get(n, 0)))
    t = rebuild('gPokedexOrder_Height', lambda n: (stat[n][0], n))
    t = rebuild('gPokedexOrder_Weight', lambda n: (stat[n][1], n))
    write('src/data/pokemon/pokedex_orders.h', t, dry)


def wire_learnsets(dry):
    """Each Old Unown slot already has a one-move stub learnset of its own, so
    the contents are replaced and the pointer table needs no change at all."""
    t = read('src/data/pokemon/level_up_learnsets.h')
    for i, m in enumerate(MONS):
        sym = f'sSpecies{252 + i}LevelUpLearnset'
        mm = re.search(rf'(static const u16 {sym}\[\] = \{{\n)(.*?)(\n\}};)',
                       t, re.S)
        if mm is None:
            sys.exit(f'no stub learnset {sym}')
        body = ''.join(f'    LEVEL_UP_MOVE({lvl:2d}, MOVE_{mv}),\n'
                       for lvl, mv in LEARNSETS[m['const']])
        t = t.replace(mm.group(0), mm.group(1) + body + '    LEVEL_UP_END'
                      + mm.group(3))
    write('src/data/pokemon/level_up_learnsets.h', t, dry)


def wire_tmhm(dry):
    t = read('src/data/pokemon/tmhm_learnsets.h')
    for m in MONS:
        C = m['const']
        mm = re.search(rf'(\[SPECIES_{C}\] = \{{ \.learnset = \{{\n)(.*?)(\    \}} \}},)',
                       t, re.S)
        if mm is None:
            sys.exit(f'no tmhm row for SPECIES_{C}')
        body = ''.join(f'        .{tm} = TRUE,\n' for tm in TMHM[C].split())
        t = t.replace(mm.group(0), mm.group(1) + body + mm.group(3))
    write('src/data/pokemon/tmhm_learnsets.h', t, dry)


def wire_evolutions(dry):
    mark = '\n    // Open Hoenn - tools/newmons.py\n'
    t = read('src/data/pokemon/evolution.h')
    if mark in t:
        t = t[:t.index(mark)] + '};\n'
    rows = ''.join(f'    [SPECIES_{a}] = {{{{{k}, {v}, SPECIES_{b}}}}},\n'
                   for a, (k, v, b) in EVOLUTIONS.items())
    i = t.rindex('};')
    write('src/data/pokemon/evolution.h',
          t[:i].rstrip() + '\n' + mark + rows + '};\n', dry)


def check():
    """Verify on the written data, not on what the tool believes it wrote."""
    bad = []
    info = read('src/data/pokemon/species_info.h')
    names = read('src/data/text/species_names.h')
    for m in MONS:
        C = m['const']
        mm = re.search(rf'\[SPECIES_{C}\] =\s*\{{(.*?)\n    \}},', info, re.S)
        if mm is None:
            bad.append(f'SPECIES_{C} has no species_info row')
            continue
        d = mm.group(1)
        if 'OLD_UNOWN' in d:
            bad.append(f'SPECIES_{C} still has the placeholder stats')
        got = re.search(r'\.types = \{ TYPE_(\w+), TYPE_(\w+) \}', d)
        if got.groups() != m['types']:
            bad.append(f'SPECIES_{C} is {got.groups()}, should be {m["types"]}')
        if f'[SPECIES_{C}] = _("{m["name"]}")' not in names:
            bad.append(f'SPECIES_{C} is not named {m["name"]}')

    for path, sym in (('src/data/pokemon_graphics/front_pic_table.h', 'gMonFrontPic'),
                      ('src/data/pokemon_graphics/back_pic_table.h', 'gMonBackPic'),
                      ('src/data/pokemon_graphics/palette_table.h', 'gMonPalette'),
                      ('src/data/pokemon_graphics/shiny_palette_table.h', 'gMonShinyPalette')):
        t = read(path)
        for m in MONS:
            if f'{sym}_{camel(m["const"])}' not in t:
                bad.append(f'{path} does not point at {sym}_{camel(m["const"])}')

    # every asset the tables now name has to be on disk
    for m in MONS:
        for f in ('front.png', 'anim_front.png', 'back.png', 'icon.png',
                  'normal.pal', 'shiny.pal', 'footprint.png'):
            p = f'{R.ROOT}/graphics/pokemon/{m["dir"]}/{f}'
            if not os.path.exists(p):
                bad.append(f'missing asset {p}')
    for m in MONS:
        w = f'{R.ROOT}/sound/direct_sound_samples/cries/{m["cry"]}.wav'
        if not os.path.exists(w):
            bad.append(f'missing cry {w}')

    # the sort orders have to cover the new count, or the dex reads off the end
    orders = read('src/data/pokemon/pokedex_orders.h')
    want = len(re.findall(r'\[NATIONAL_DEX_\w+\] =',
                          read('src/data/pokemon/pokedex_entries.h')))
    for table in ('gPokedexOrder_Weight', 'gPokedexOrder_Height'):
        got = len(re.findall(r'NATIONAL_DEX_\w+',
                  re.search(rf'{table}\[\] =\s*\{{(.*?)\n\}};', orders, re.S).group(1)))
        if got != want - 1:      # the tables exclude NATIONAL_DEX_NONE
            bad.append(f'{table} has {got} entries, dex has {want - 1} species')

    # and nothing may still be crying like Unown
    pk = read('src/pokemon.c')
    if f"SPECIES_{MONS[0]['const']} - 1" not in pk:
        bad.append('SpeciesToCryId does not know about the new species')
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--report', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()

    if a.report:
        for m in MONS:
            t = '/'.join(dict.fromkeys(m['types']))
            print(f"  {m['const']:12s} {t:12s} "
                  f"{'-'.join(str(x) for x in m['stats']):26s} "
                  f"{'/'.join(m['abilities'])}")
        print()
        for k, (kind, val, to) in EVOLUTIONS.items():
            print(f'  {k:12s} -> {to} at level {val}')
        print()
        for k, v in ABILITY_NOTE.items():
            print(f'  {k:12s} {v}')
        return

    n = rename_slots(a.dry_run)
    fill_tables(a.dry_run)
    add_graphics_symbols(a.dry_run)
    wire_cries(a.dry_run)
    add_cry_samples(a.dry_run)
    wire_dex(a.dry_run)
    wire_orders(a.dry_run)
    wire_learnsets(a.dry_run)
    wire_tmhm(a.dry_run)
    wire_evolutions(a.dry_run)
    print(f'{len(MONS)} species written; {n} files touched by the slot rename')

    if a.check:
        bad = check()
        if bad:
            sys.exit('\n'.join(bad))
        print('every row, asset and sort order checks out')


if __name__ == '__main__':
    sys.exit(main())

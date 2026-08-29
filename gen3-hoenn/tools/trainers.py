#!/usr/bin/env python3
"""Put trainers on the new routes.

Vanilla's land routes carry a median of eight trainers each - 3.04 per thousand
cells, 295 across 34 routes - and ours carried none. Items give a route
something to find; trainers are what make walking down it a thing that happens.

Nothing here is invented where it could be harvested. The 60 combinations of
overworld sprite, trainer class, battle portrait and encounter fanfare come
from vanilla's own route trainers, in their own proportions, so every generated
trainer is a pairing the game already ships. Party species come from the map's
own wild encounter table, which is what the route's own Pokemon are. Party size
follows vanilla's distribution - half of its route trainers carry two, a third
carry one - and the top level sits one above the highest level the route's own
wild Pokemon reach. That last is measured two ways and the tighter one kept:
against the median wild level vanilla's trainers scatter over +0 to +4, against
the highest they sit in +1, between -1 and +2.

Only the words are written rather than measured: six openers, six concessions
and six parting lines per class of trainer.

Run last. newmaps.py rewrites the headers, populate.py puts the items in them,
and this appends to what it finds:

    python3 tools/newmaps.py && python3 tools/populate.py && python3 tools/trainers.py
"""
import argparse, collections, glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_hoenn as R
import terrain as T
import newmaps as N
import populate as P

RATE = 3.04                     # trainers per thousand cells, vanilla's median
APART = 8
MARGIN = 4
LEVEL_OVER = 1                  # top mon, over the route's highest wild level
SIZES = [1, 1, 2, 2, 2, 3]      # vanilla: 63 ones, 90 twos, 19 threes
SIGHT = [1, 2, 2, 3, 3, 3, 4, 4, 5]
FACING = ['MOVEMENT_TYPE_FACE_DOWN', 'MOVEMENT_TYPE_FACE_UP',
          'MOVEMENT_TYPE_FACE_LEFT', 'MOVEMENT_TYPE_FACE_RIGHT']

STAND_ON = (T.GRASS, T.SAND, T.PATH, T.PLATEAU)
WADE_ON = (T.SHALLOW,)

OPPONENTS = 'include/constants/opponents.h'
TRAINERS = 'src/data/trainers.h'
PARTIES = 'src/data/trainer_parties.h'
MARK = '// Open Hoenn - tools/trainers.py'

# One name per trainer, none of them vanilla's, so a Pokenav list stays
# readable, and split the way vanilla splits them: a class the game
# marks F_TRAINER_FEMALE gets a name from the first list. There are more
# of each than the routes can hold.
NAMES_F = """ADRIA AMARA ANITA ARWEN AUBREY BECCA BONNIE BRIAR BRANWEN CARLOTTA CARMEN
CLEMMIE CLEO CORAL DAHLIA DELIA DORA EDITH EFFIE ELOISE ESME FENELLA FIONA
FLORA GWENDOLEN GILDA GRISELDA HARRIET HAZEL IMOGEN INGRID IRIS ISOLDE JEMMA
JOSIE JUNO KENDRA LACEY LEONA LILAH LUCIA MABEL MALLORY MAUDE MIRA NADIA
NIAMH NORA OLIVE PAIGE PETRONELLA PIPER RAMONA RENATA ROSALIND RUBY SABLE
SORREL SELMA SIGRID SIMONE SLOANE STELLA SYBIL TAMSIN THEA TRUDY URSULA
VERITY VIOLA WILLA WILHELMINA WREN YOLANDA ZELDA""".split()
NAMES_M = """ALDEN ALVIN ANSEL ARDEN ARLO ASHER AVERY BARNEY BASIL BENNO BERTIE
BRAMWELL BORIS BRUNO BRYCE CAIRO CASPER CASIMIR CRISPIN CLIVE CONRAD COLBY
CORWIN CRAIG CURTIS DERWENT DARBY DENNIS DESMOND DEXTER DRISCOLL DUSTIN EARL
ELDON ELIAS EMMET ENZO EVANS FENWICK FERRIS FINLAY FLETCH FORREST FRANKIE
GABE GARLAND GAVIN GLENN GRIFFIN GUSTAV HADLEY HAMISH HARLOW HOLLIS HORACE
HUGO IDRIS IVOR JAMIE JASPER JETHRO JULIAN JUDE KEATON KESTREL KIERAN KIRBY
LAMONT LANDON LESLIE LEWIS LOGAN LORCAN LUDO MAGNUS MARLOW MERLE MILO MORGAN
MURPHY NEELY NEVIN OAKLEY ORSON OSCAR OTTO PERCY PORTER QUINN RAFE REEVES
REGGIE RHYS ROSCOE ROWAN RUFUS SEAMUS SETH SOREN SULLY TALLIS TEDDY THORNE
TOBIAS TYSON VANCE VESPER WALDO WENDELL WESLEY ZEPHYR""".split()

# What a trainer says, by the kind of trainer they are. A class falls back to
# the plain set when it has none of its own.
LINES = {
    'HIKER': (
        ["THIS ROAD is steeper than it looks.\pMind if I slow you down?",
         "I've walked every rise in HOENN.\pLet's see what you've walked.",
         "You look like you've been climbing too.\pProve it.",
         "Rest a minute! Then battle me.",
         "Nothing up here but rock and me.\pAnd my POKéMON.",
         "I carry everything on my back.\pIncluding a win or two."],
        ["Downhill from here, I suppose.",
         "You've got the legs for it.",
         "Well climbed.", "That's the top of me, then.",
         "I'm winded and beaten.", "Fair enough! Fair enough."],
        ["Keep going up. The view is worth it.",
         "Take the high path. It's kinder than it looks.",
         "There's water further on. Fill up.",
         "Watch the loose stone past the ridge.",
         "I'll be here a while yet. Come back.",
         "Walk well, TRAINER."]),
    'FISHERMAN': (
        ["Quiet! ...Ah, you've scared them off.\pYou owe me a battle.",
         "Been here since dawn. Nothing biting.\pYou'll do.",
         "The fish can wait. You can't.",
         "You've a look about you. A biting look.",
         "I hook things that fight back.\pLike you.",
         "Cast off! Let's battle."],
        ["Reeled in and thrown back.", "You're the one that got away.",
         "Should've stuck to the water.", "A fine catch you are.",
         "Slipped right through.", "Hah! Hooked myself."],
        ["Best water's round the bend. Try it.",
         "Bring a ROD next time and I'll show you a spot.",
         "They bite better at dusk out here.",
         "Still waters. Deep POKéMON.",
         "I'll be here till the light goes.",
         "Tight lines, TRAINER."]),
    'SWIMMER_M': (
        ["The water's fine! Come in and battle.",
         "I swam here from the last shore.\pWorth it, if you'll battle.",
         "Nothing between here and the horizon.\pJust us.",
         "You walked. I swam. Let's settle it.",
         "Cold? You get used to it.",
         "Wave to me and I'll take it as a challenge!"],
        ["Out of my depth.", "You swim better than you look.",
         "Glub. Beaten.", "The current's yours.",
         "I'll float here a while.", "Washed up, that's me."],
        ["Careful past the point. It's deeper.",
         "Follow the shallows and you'll be fine.",
         "Best swimming in HOENN, this.",
         "There's a beach north of here. Rest there.",
         "I'll race you next time.", "Mind the tide."]),
    'SWIMMER_F': (
        ["The water's fine! Come in and battle.",
         "I swam here from the last shore.\pWorth it, if you'll battle.",
         "Nothing between here and the horizon.\pJust us.",
         "You walked. I swam. Let's settle it.",
         "Cold? You get used to it.",
         "Wave to me and I'll take it as a challenge!"],
        ["Out of my depth.", "You swim better than you look.",
         "Glub. Beaten.", "The current's yours.",
         "I'll float here a while.", "Washed up, that's me."],
        ["Careful past the point. It's deeper.",
         "Follow the shallows and you'll be fine.",
         "Best swimming in HOENN, this.",
         "There's a beach north of here. Rest there.",
         "I'll race you next time.", "Mind the tide."]),
    'YOUNGSTER': (
        ["I'm not lost! I'm training!\pBattle me and I'll prove it.",
         "My POKéMON is stronger than yesterday!",
         "Hey! Nobody comes down here!\pBattle me!",
         "I walked all this way for a battle.",
         "You look tough. I'm tougher.",
         "One battle! Just one!"],
        ["I'm still not lost.", "Yesterday me would have lost worse.",
         "Aww.", "You're really strong!", "I'll train more.",
         "Next time! Next time!"],
        ["I'm going to battle everyone on this ROUTE.",
         "There's tall grass back that way. Good grass.",
         "When I'm big I'll have six POKéMON.",
         "Do you know the way out? ...Me neither.",
         "I'll remember you!", "Come back when I'm stronger!"]),
    'PICNICKER': (
        ["Lovely spot for lunch.\pAnd a battle.",
         "I packed for two. Battle first?",
         "You've walked a long way. Sit! ...After.",
         "The weather held. Let's use it.",
         "My POKéMON eat better than I do.",
         "Sandwich? No? Battle, then."],
        ["Well, that's the afternoon gone.",
         "You've earned lunch.", "Beaten before dessert.",
         "How nice. And how losing.", "A picnic and a defeat.",
         "I'll pack up, then."]),
    'CAMPER': (
        ["Made camp here last night.\pBattle before I strike it?",
         "Nobody out here but us.\pLet's make it count.",
         "The fire's out. Warm me up with a battle.",
         "I sleep where the ROUTE ends.",
         "You travel light. So do I.",
         "One battle, then I'm moving on."],
        ["Time to pack.", "You've a longer stride than me.",
         "Beaten at my own camp.", "Well fought.",
         "I'll break camp early.", "That's me humbled."]),
    'BIRD_KEEPER': (
        ["Look up. That's mine.\pNow look here - battle me.",
         "They circle when a battle's coming.",
         "My birds saw you before I did.",
         "The sky's clear. Perfect for it.",
         "Wings beat legs. Prove me wrong.",
         "Fly at me, then."],
        ["Grounded.", "You clipped us.", "Down we come.",
         "The sky's yours today.", "Well flown.", "Back to the nest."]),
    'BUG_CATCHER': (
        ["Shh - I've almost -\pAh. Battle me instead.",
         "There's a rare one on this ROUTE. Really!",
         "My NET is faster than your feet.",
         "Bugs first, battles second. Or the other way.",
         "You'll scare them. Battle me for it.",
         "Six legs beat two!"],
        ["It got away. So did the win.",
         "You're quicker than a bug.", "Squashed.",
         "I'll catch a better one.", "Beaten fair.",
         "Back to the grass."]),
    'COOLTRAINER': (
        ["You have the walk of someone worth battling.",
         "Don't hold back. I won't.",
         "I came out here for a real match.",
         "Let's not waste each other's time.",
         "Show me the team that got you this far.",
         "Ready when you are."],
        ["That was a real match.", "You didn't waste my time.",
         "Strong. Genuinely strong.", "I'll take that loss.",
         "Good. Very good.", "You've earned the ROUTE."]),
    'BLACK_BELT': (
        ["Stand still. Breathe. Now battle.",
         "Strength is a habit. Show me yours.",
         "I train out here where nobody watches.",
         "No shortcuts. Only training.",
         "Your stance is wrong. Your team may not be.",
         "Begin!"],
        ["Your habit is stronger.", "I bow to that.",
         "Beaten cleanly.", "More training for me.",
         "A worthy match.", "Strength recognised."]),
    'PSYCHIC': (
        ["I knew you would come this way.",
         "Your first POKéMON. I can see it.\pShall we?",
         "The ROUTE told me you were near.",
         "I foresee a battle. Naturally.",
         "Don't think so loudly.",
         "Yes. Now."]),
    'AROMA_LADY': (
        ["Can you smell it? The grass after rain.\pBattle me in it.",
         "I grow things out here. And battle.",
         "Everything on this ROUTE flowers eventually.",
         "Breathe in. Then battle.",
         "My POKéMON smell of the field.",
         "A short battle, before the light goes."],
        ["How refreshing to lose.", "You've a green touch.",
         "Beaten among the flowers.", "Lovely.",
         "I'll tend the beds instead.", "Well grown."]),
}
PLAIN = (
    ["Not many come this far. Battle me.",
     "A challenger! At last.",
     "I've been waiting for someone like you.",
     "Stop there. This ROUTE is mine to defend.",
     "You've come a long way. Let's see why.",
     "Battle me and I'll let you pass."],
    ["You've come a long way indeed.",
     "The ROUTE is yours.", "Beaten.", "Well fought.",
     "I underestimated you.", "That settles it."],
    ["Keep heading on. It opens out.",
     "There's more of us further along.",
     "Rest before the next stretch.",
     "Good luck out there.",
     "I'll be training when you come back.",
     "Safe travels."])

WIDTH = 35                      # what fits a message box line

def wrap(text):
    r"""Break a line the way the game needs it broken.

    A message box shows two lines at a time. Vanilla joins the first pair with
    \n and scrolls every line after that with \l, and starts a fresh page on
    \p. Written as one long string, a line simply runs off the box.
    """
    out = []
    for page in text.split('\\p'):
        line, rows = '', []
        for word in page.split():
            if line and len(line) + 1 + len(word) > WIDTH:
                rows.append(line)
                line = word
            else:
                line = f'{line} {word}'.strip()
        rows.append(line)
        out.append('\\n'.join(rows[:2]) + ''.join('\\l' + r for r in rows[2:]))
    return '\\p'.join(out)

def lines(cls, i):
    got = LINES.get(cls[14:], PLAIN)
    got = tuple(list(got) + list(PLAIN[len(got):]))
    return tuple(wrap(g[i % len(g)]) for g in got[:3])

def camel(name):
    return name.capitalize()

def archetypes(lay, maps, pos, new, hdrs):
    """(sprite, class, pic, music) as vanilla pairs them, and how often."""
    script = {}
    for f in glob.glob(f'{R.ROOT}/data/maps/*/scripts.inc'):
        cur = None
        for l in open(f):
            s = l.strip()
            if s.endswith('::'):
                cur = s[:-2]
            m = re.match(r'trainerbattle_\w+\s+(TRAINER_\w+)', s)
            if m and cur:
                script.setdefault(cur, m.group(1))
    src = open(f'{R.ROOT}/{TRAINERS}').read()
    info = {}
    for m in re.finditer(r'\[(TRAINER_\w+)\] =\s*\{(.*?)\n    \},', src, re.S):
        b = m.group(2)
        g = lambda k: (re.search(k + r' = ([^,\n]+),', b) or [None, ''])[1]
        info[m.group(1)] = (g(r'\.trainerClass'), g(r'\.trainerPic'),
                            g(r'\.encounterMusic_gender'))
    out = collections.Counter()
    for k in sorted(pos):
        if k in new or not k.startswith('MAP_ROUTE'):
            continue
        for o in hdrs.get(k, {}).get('object_events') or []:
            if str(o.get('trainer_type')) != 'TRAINER_TYPE_NORMAL':
                continue
            t = script.get(o.get('script'))
            if t and t in info and all(info[t]):
                out[(o['graphics_id'],) + info[t]] += 1
    # each archetype repeated as often as vanilla uses it, so indexing into
    # the list reproduces the mix. Sampling the 60 distinct ones uniformly
    # instead put Rich Boy at 7.7% of our trainers against vanilla's 0.7%,
    # and left Black Belt and Expert at none at all.
    return [a for a, n in out.most_common() for _ in range(n)]

CLASS_SHARE = 0.30              # a class "means" a type at this share or more

def class_types():
    """what each trainer class's Pokemon are, as vanilla assigns them.

    A Fisherman's party is 59% Water, a Hiker's 44% Ground and 37% Rock, a
    Psychic's 71% Psychic, a Bird Keeper's 50% Flying. Handing every class the
    same slice of the route's wild table ignores all of that and puts a
    Poochyena on a Swimmer.
    """
    types = {}
    base = open(f'{R.ROOT}/src/data/pokemon/species_info.h').read()
    for m in re.finditer(r'\[(SPECIES_\w+)\] =\s*\{(.*?)\n    \},', base, re.S):
        t = re.search(r'\.types\s*=\s*\{\s*(TYPE_\w+),\s*(TYPE_\w+)\s*\}', m.group(2))
        if t:
            types[m.group(1)] = {t.group(1), t.group(2)}
    src = open(f'{R.ROOT}/{TRAINERS}').read()
    src = src[:src.find(MARK)] if MARK in src else src
    pp = open(f'{R.ROOT}/{PARTIES}').read()
    pp = pp[:pp.find(MARK)] if MARK in pp else pp
    sp = {}
    for m in re.finditer(r'static const struct \w+ (sParty_\w+)\[\] = \{(.*?)\n\};',
                         pp, re.S):
        sp[m.group(1)] = re.findall(r'\.species = (SPECIES_\w+)', m.group(2))
    tally = collections.defaultdict(collections.Counter)
    for m in re.finditer(r'\[(TRAINER_\w+)\] =\s*\{(.*?)\n    \},', src, re.S):
        c = re.search(r'\.trainerClass = (TRAINER_CLASS_\w+)', m.group(2))
        p = re.search(r'\(s(Party_\w+)\)', m.group(2))
        if not (c and p):
            continue
        for s in sp.get('s' + p.group(1), []):
            for t in types.get(s, ()):
                tally[c.group(1)][t] += 1
    want = {}
    for c, d in tally.items():
        n = sum(d.values())
        if n >= 20:
            want[c] = {t for t, v in d.items() if v >= CLASS_SHARE * n}
    return types, want

def spots(spec, lay, maps, rend, taken):
    L = lay[maps[spec['const']]['layout']]
    w, h = L['width'], L['height']
    blk = open(f'{R.ROOT}/{L["blockdata_filepath"]}', 'rb').read()
    raw = [(blk[i*2] | (blk[i*2+1] << 8)) for i in range(w * h)]
    C = T.Classifier(rend, L['primary_tileset'], L.get('secondary_tileset'))
    cls = [C(v & 0x3FF, (v >> 10) & 3) for v in raw]
    walk = [((v >> 10) & 3) == 0 and cls[i] not in (T.WATER, T.POND)
            for i, v in enumerate(raw)]
    ele = [(v >> 12) & 0xF for v in raw]
    ok = lambda a, b: a == b or 0 in (a, b) or 15 in (a, b)
    seed = [i for i in range(w*h)
            if walk[i] and (i % w in (0, w-1) or i // w in (0, h-1))]
    live, q = set(seed), collections.deque(seed)
    while q:
        i = q.popleft()
        x, y = i % w, i // w
        for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
            j = ny*w + nx
            if (0 <= nx < w and 0 <= ny < h and j not in live and walk[j]
                    and ok(ele[i], ele[j])):
                live.add(j)
                q.append(j)

    def room(i):
        """a trainer needs somewhere to look. Count the open run each way."""
        x, y = i % w, i // w
        best = 0
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = 0
            while (0 <= x + dx*(n+1) < w and 0 <= y + dy*(n+1) < h
                   and walk[(y + dy*(n+1))*w + x + dx*(n+1)]):
                n += 1
                if n >= 6:
                    break
            best = max(best, n)
        return best

    # a trainer is solid and stays solid after you beat them, so one standing
    # in a one-cell gap shuts whatever is behind it for good
    cut = P.articulations(walk, ele, w, h)
    cand = [i for i in range(w*h)
            if MARGIN <= i % w < w - MARGIN and MARGIN <= i // w < h - MARGIN
            and i in live and cls[i] in STAND_ON + WADE_ON and i not in cut
            and (i % w, i // w) not in taken and room(i) >= 2]
    cand.sort(key=lambda i: -T.fbm(i % w, i // w, spec['num'] * 13 + 5,
                                   octaves=2, freq=0.06))
    n = max(1, round(RATE * w * h / 1000))
    out = []
    for i in cand:
        if len(out) >= n:
            break
        x, y = i % w, i // w
        if any(abs(x - px) + abs(y - py) < APART for px, py, _, _, _ in out):
            continue
        # face the longest open run, so the sight line has somewhere to go
        best = max(((sum(1 for k in range(1, 7)
                         if 0 <= x + dx*k < w and 0 <= y + dy*k < h
                         and walk[(y + dy*k)*w + x + dx*k]), d)
                    for d, (dx, dy) in enumerate(((0, 1), (0, -1), (-1, 0), (1, 0)))),
                   key=lambda t: t[0])
        out.append((x, y, ele[i], cls[i] in WADE_ON, best[1]))
    return out

def wild_levels(const, wild):
    e = wild.get(const) or {}
    lm = e.get('land_mons') or e.get('water_mons')
    if not lm:
        return 20, ['SPECIES_ZIGZAGOON']
    top = max(m['max_level'] for m in lm['mons'])
    sp = list(dict.fromkeys(m['species'] for m in lm['mons']))
    return top, sp

def cut(text, mark):
    i = text.find(mark)
    return text if i < 0 else text[:i].rstrip('\n') + '\n'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    lay, maps, pos = R.solve()
    rend = R.Renderer()
    new = T.generated()
    hdrs = {}
    for f in glob.glob(f'{R.ROOT}/data/maps/*/map.json'):
        j = json.load(open(f))
        hdrs[j['id']] = j
    wild = {}
    d = json.load(open(f'{R.ROOT}/src/data/wild_encounters.json'))
    for g in d['wild_encounter_groups']:
        if g['label'] == 'gWildMonHeaders':
            for e in g['encounters']:
                wild[e['map']] = e

    arch = archetypes(lay, maps, pos, new, hdrs)
    wet = [a for a in arch if 'SWIM' in a[1] or 'TUBER' in a[1]]
    dry = [a for a in arch if a not in wet]
    types, class_of = class_types()
    print(f'{len(arch)} vanilla trainer archetypes, {len(dry)} on land; '
          f'{len(class_of)} classes with a type of their own')

    opp = cut(open(f'{R.ROOT}/{OPPONENTS}').read(), MARK)
    base = max(int(m) for m in re.findall(r'#define TRAINER_\w+\s+(\d+)', opp)) + 1
    plan, defines, entries, parties, byname = [], [], [], [], {}
    named = collections.Counter()
    used = set(re.findall(r'#define (TRAINER_\w+)', opp))
    nid = 0
    for spec in N.NEWMAPS:
        top, species = wild_levels(spec['const'], wild)
        # populate.py has already put the items down and does not know about
        # this pass, so the cells it used are read back off the header rather
        # than assumed free. Route 138 had a trainer standing on an item ball.
        ok = lambda a: (not class_of.get(a[1])
                        or any(class_of[a[1]] & types.get(s, set())
                               for s in species))
        fit = ([a for a in dry if ok(a)] or dry,
               [a for a in wet if ok(a)] or wet)
        h0 = hdrs.get(spec['const'], {})
        # its own trainers from a previous run are not obstacles - counting
        # them would move everybody one square further along every time
        taken = {(int(e['x']), int(e['y']))
                 for e in (h0.get('object_events') or []) + (h0.get('bg_events') or [])
                 if 'x' in e and 'y' in e
                 and str(e.get('trainer_type', '')) != 'TRAINER_TYPE_NORMAL'}
        here = spots(spec, lay, maps, rend, taken)
        objs = []
        for k, (x, y, e, wade, face) in enumerate(here):
            # only archetypes whose class means a type this route actually
            # has - a Fisherman on a route with no Water Pokemon is a
            # Fisherman with somebody else's team. Filtering the weighted list
            # and indexing into what is left keeps the mix; walking forward to
            # the first that fits does not, because the classes with no type of
            # their own always fit and absorb everyone else's walk. Cooltrainer
            # went to 22% of our trainers that way, against vanilla's 5.5%.
            src = fit[1] if (wade and fit[1]) else fit[0]
            gfx, cls, pic, mus = src[(spec['num'] * 7 + k * 3) % len(src)]
            pool_n = NAMES_F if 'F_TRAINER_FEMALE' in mus else NAMES_M
            name = pool_n[named[len(pool_n)] % len(pool_n)]
            named[len(pool_n)] += 1
            const = f'TRAINER_{name}'
            while const in used:
                const += '_H'
            used.add(const)
            size = SIZES[(spec['num'] + k * 5) % len(SIZES)]
            # and its Pokemon come from the part of the route's table that
            # matches, when there is one
            want = class_of.get(cls) or set()
            pool = [s for s in species if want & types.get(s, set())] or species
            # consecutive entries, so a party of three is three different
            # Pokemon wherever the route has three to give
            b = (spec['num'] * 3 + k * 7) % len(pool)
            mons = [(pool[(b + m) % len(pool)], top + LEVEL_OVER - m)
                    for m in range(size)]
            party = f'sParty_{camel(name)}{spec["num"]}'
            parties.append(
                f'static const struct TrainerMonNoItemDefaultMoves {party}[] = {{\n'
                + ',\n'.join(f'    {{\n    .iv = 0,\n    .lvl = {lv},\n'
                             f'    .species = {sp},\n    }}' for sp, lv in mons)
                + '\n};\n')
            defines.append(f'#define {const}{" " * max(1, 36 - len(const))}'
                           f'{base + nid}')
            entries.append(
                f'    [{const}] =\n    {{\n'
                f'        .trainerClass = {cls},\n'
                f'        .encounterMusic_gender = {mus},\n'
                f'        .trainerPic = {pic},\n'
                f'        .trainerName = _("{name}"),\n'
                f'        .items = {{}},\n'
                f'        .doubleBattle = FALSE,\n'
                f'        .aiFlags = AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_TRY_TO_FAINT,\n'
                f'        .party = NO_ITEM_DEFAULT_MOVES({party}),\n'
                f'    }},\n')
            script = f'{spec["name"]}_EventScript_{camel(name)}'
            byname.setdefault(spec['name'], []).append(
                (script, const, name, cls, nid))
            objs.append({
                'graphics_id': gfx, 'x': x, 'y': y, 'elevation': e,
                'movement_type': FACING[face],
                'movement_range_x': 0, 'movement_range_y': 0,
                'trainer_type': 'TRAINER_TYPE_NORMAL',
                'trainer_sight_or_berry_tree_id':
                    str(SIGHT[(spec['num'] + k) % len(SIGHT)]),
                'script': script, 'flag': '0'})
            nid += 1
        plan.append((spec, objs))

    limit = int(re.search(r'#define MAX_TRAINERS_COUNT\s+(\d+)', opp).group(1))
    if base + nid > limit:
        sys.exit(f'{base + nid} trainers needed, MAX_TRAINERS_COUNT is {limit}')

    opp = re.sub(r'#define TRAINERS_COUNT\s+\d+',
                 f'#define TRAINERS_COUNT                      {base + nid}', opp)
    opp = opp.replace('#endif  // GUARD_CONSTANTS_OPPONENTS_H', '').rstrip('\n')
    opp += (f'\n\n{MARK}\n\n' + '\n'.join(defines)
            + '\n\n#endif  // GUARD_CONSTANTS_OPPONENTS_H\n')

    par = cut(open(f'{R.ROOT}/{PARTIES}').read(), MARK)
    par += f'\n{MARK}\n\n' + '\n'.join(parties)

    # cut() takes the closing brace of the table with it on a re-run, which is
    # why this puts one back rather than insisting on finding one
    tra = cut(open(f'{R.ROOT}/{TRAINERS}').read(), MARK).rstrip('\n')
    if tra.endswith('};'):
        tra = tra[:-2].rstrip('\n')
    tra += f'\n\n{MARK}\n\n' + '\n'.join(entries) + '};\n'

    if not a.dry_run:
        open(f'{R.ROOT}/{OPPONENTS}', 'w').write(opp)
        open(f'{R.ROOT}/{PARTIES}', 'w').write(par)
        open(f'{R.ROOT}/{TRAINERS}', 'w').write(tra)

    for spec, objs in plan:
        p = f'{R.ROOT}/data/maps/{spec["name"]}/scripts.inc'
        body = cut(open(p).read(), MARK)
        chunks = []
        for script, const, name, cls, i in byname.get(spec['name'], []):
            intro, beat, after = lines(cls, i)
            pre = f'{spec["name"]}_Text_{camel(name)}'
            chunks.append(
                f'{script}::\n'
                f'\ttrainerbattle_single {const}, {pre}Intro, {pre}Defeat\n'
                f'\tmsgbox {pre}PostBattle, MSGBOX_AUTOCLOSE\n\tend\n\n'
                f'{pre}Intro:\n\t.string "{intro}$"\n\n'
                f'{pre}Defeat:\n\t.string "{beat}$"\n\n'
                f'{pre}PostBattle:\n\t.string "{after}$"\n\n')
        out = body.rstrip('\n') + f'\n\n{MARK}\n\n' + ''.join(chunks)
        q = f'{R.ROOT}/data/maps/{spec["name"]}/map.json'
        h = json.load(open(q))
        keep = [o for o in h.get('object_events') or []
                if str(o.get('trainer_type', 'TRAINER_TYPE_NONE'))
                != 'TRAINER_TYPE_NORMAL']
        h['object_events'] = keep + objs
        if not a.dry_run:
            open(p, 'w').write(out)
            json.dump(h, open(q, 'w'), indent=2)
        print(f'  {spec["name"]:10s} {len(objs)} trainers')
    print(f'{nid} trainers across {len(plan)} maps, ids {base}-{base + nid - 1} '
          f'of {limit}')

if __name__ == '__main__':
    sys.exit(main())

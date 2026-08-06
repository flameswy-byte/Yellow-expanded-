#!/usr/bin/env python3
"""Give the new maps wild encounters, derived from their neighbours.

Tall grass with nothing in it is scenery, not a route. But inventing species
lists per map is exactly the sort of guess this project has avoided everywhere
else, so the tables come from the same place the terrain did: the maps next
door. For each new map, every neighbour's table is pooled, each entry weighted
by how much edge the two maps share and by how likely that slot is to come up.
Species are then ranked by total weight and dealt into the slots highest
first, so a route between Petalburg and Rustboro ends up with the Pokémon you
would expect to meet between them, at the levels you would expect.

Levels are a weighted mean of the donors', so a map bridging a level 5 route
and a level 15 one lands in between rather than at one end.

Water and fishing tables are only written where the map actually has water,
and land tables only where it has grass to stand in.

    python3 tools/encounters.py --dry-run
    python3 tools/encounters.py
"""
import argparse, collections, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render_hoenn as R
import terrain as T
import newmaps as N

WILD = f'{R.ROOT}/src/data/wild_encounters.json'
GROUP = 'gWildMonHeaders'

# Gen 3 slot probabilities, in percent. The land table is the familiar
# 20/20/10/10/10/10/5/5/5/4/4/1; fishing is three rods sharing ten slots.
RATES = {
    'land_mons':        [20, 20, 10, 10, 10, 10, 5, 5, 5, 4, 4, 1],
    'water_mons':       [60, 30, 5, 4, 1],
    'rock_smash_mons':  [60, 30, 5, 4, 1],
    'fishing_mons':     [70, 30, 60, 20, 20, 40, 40, 15, 4, 1],
}

def load():
    d = json.load(open(WILD))
    grp = next(g for g in d['wild_encounter_groups'] if g['label'] == GROUP)
    return d, grp, {e['map']: e for e in grp['encounters']}

def spans(box, const):
    """neighbour -> number of shared edge cells, from the map's own header."""
    p = f'{R.ROOT}/data/maps/{N.map_dir(const)}/map.json'
    j = json.load(open(p))
    w, h = box[const][2], box[const][3]
    out = collections.Counter()
    for c in j.get('connections') or []:
        nb, d, off = c.get('map'), c.get('direction'), c.get('offset', 0)
        if nb not in box or d not in ('up', 'down', 'left', 'right'):
            continue
        nw, nh = box[nb][2], box[nb][3]
        if d in ('up', 'down'):
            n = min(w, off + nw) - max(0, off)
        else:
            n = min(h, off + nh) - max(0, off)
        if n > 0:
            out[nb] += n
    return out

def terrain_mix(spec):
    """which encounter kinds this map can support at all."""
    L = f'{R.ROOT}/data/layouts/{spec["name"]}/map.bin'
    blk = open(L, 'rb').read()
    rend = R.Renderer()
    C = T.Classifier(rend, 'gTileset_General', spec.get('secondary'))
    n = collections.Counter()
    for i in range(len(blk) // 2):
        v = blk[i*2] | (blk[i*2+1] << 8)
        n[C(v & 0x3FF, (v >> 10) & 3)] += 1
    return n

def pool(kind, tables, weights):
    """species -> (weight, mean min level, mean max level) across neighbours."""
    acc = {}
    rate = RATES[kind]
    for nb, wt in weights.items():
        t = tables.get(nb, {}).get(kind)
        if not t:
            continue
        for i, m in enumerate(t['mons']):
            r = rate[i] if i < len(rate) else 1
            w = wt * r
            a = acc.setdefault(m['species'], [0.0, 0.0, 0.0])
            a[0] += w
            a[1] += w * m['min_level']
            a[2] += w * m['max_level']
    return {s: (w, lo / w, hi / w) for s, (w, lo, hi) in acc.items() if w > 0}

def build_table(kind, tables, weights):
    p = pool(kind, tables, weights)
    if not p:
        return None
    order = sorted(p, key=lambda s: -p[s][0])
    slots = len(RATES[kind])
    mons = []
    for i in range(slots):
        s = order[i % len(order)]
        _, lo, hi = p[s]
        lo, hi = max(2, round(lo)), max(2, round(hi))
        mons.append({'min_level': min(lo, hi), 'max_level': max(lo, hi),
                     'species': s})
    rates = [tables[nb][kind]['encounter_rate'] for nb in weights
             if tables.get(nb, {}).get(kind)]
    return {'encounter_rate': round(sum(rates) / len(rates)), 'mons': mons}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    d, grp, tables = load()
    box = N.origins()

    # Two passes. Pass one uses only vanilla neighbours, so each map's levels
    # come from the real routes around it. Pass two runs solely for the maps
    # that got nothing - the ones whose only land-bearing neighbours are also
    # new - and only those see the first pass's results. Feeding new tables
    # back in everywhere would pull every map toward the global mean and cost
    # the level gradient the first pass just got right.
    done = {}
    for rnd in (1, 2):
        if rnd == 2:
            tables.update({k: v for k, v in done.items()})
        for spec in N.NEWMAPS:
            const, name = spec['const'], spec['name']
            if (const in done) == (rnd == 1) and rnd == 2:
                continue
            if rnd == 1 and const in done:
                continue
            if rnd == 2 and 'land_mons' in done.get(const, {}):
                continue
            wt = spans(box, const)
            mix = terrain_mix(spec)
            total = sum(mix.values())
            entry = {'map': const, 'base_label': f'g{name}'}
            got = []
            # a land table needs somewhere to stand; water and fishing need water
            if mix[T.TALL] + mix[T.GRASS] > total * 0.02:
                t = build_table('land_mons', tables, wt)
                if t:
                    entry['land_mons'] = t
                    got.append(f'land x{len(t["mons"])} rate {t["encounter_rate"]}')
            if mix[T.WATER] > total * 0.02:
                for kind, tag in (('water_mons', 'water'), ('fishing_mons', 'fish')):
                    t = build_table(kind, tables, wt)
                    if t:
                        entry[kind] = t
                        got.append(tag)
            if len(entry) == 2:
                continue
            if const in done and 'land_mons' not in entry:
                continue                      # pass two added nothing new
            done[const] = entry      # only pass two reads these back
            lv = entry.get('land_mons') or entry.get('water_mons')
            rng = (min(m['min_level'] for m in lv['mons']),
                   max(m['max_level'] for m in lv['mons']))
            top = ', '.join(dict.fromkeys(m['species'][8:].title()
                                          for m in lv['mons']))[:64]
            print(f'  {name:9s} lv {rng[0]:2d}-{rng[1]:2d}  {", ".join(got):28s} {top}')
    for const, entry in done.items():
        grp['encounters'] = [e for e in grp['encounters'] if e['map'] != const]
        grp['encounters'].append(entry)

    # the table is indexed by map order in some tools; keep it deterministic
    grp['encounters'].sort(key=lambda e: e['map'])
    print(f'{len(grp["encounters"])} encounter entries total')
    if not a.dry_run:
        json.dump(d, open(WILD, 'w'), indent=2)

if __name__ == '__main__':
    sys.exit(main())

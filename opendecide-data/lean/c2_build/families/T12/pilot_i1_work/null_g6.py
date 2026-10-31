"""scratch: G6 noise floor at pilot size: the same 1,000 pilot rows with RANDOM golds (a null generator)."""
import sys, json, random, copy
sys.path.insert(0, '.')
sys.dont_write_bytecode = True
import pilot, pilot_loaders as PL
with PL.open_family("T12") as kit:
    b = pilot.build_pilot(kit, 1000, run_g15=False)
    out = []
    for trial in range(4):
        rng = random.Random(1234 + trial)
        infos = []
        for i in b.infos:
            j = copy.copy(i); r = dict(i.row)
            if r['qtype'] == 'noul': r['gold'] = rng.randint(0, 1)
            else: r['gold'] = rng.choice(r['options'])
            j.row = r; infos.append(j)
        g = pilot.g6(infos)
        worst = []
        for part, d in (('yes_no', g['yes_no']), ('choice', g['choice'])):
            for v in ('a_question', 'b_options', 'c_card_without_question', 'd_meta'):
                for m in ('lr', 'gbt'):
                    worst.append((round(d[v][m] - d['chance'], 4), part, v, m))
        worst.sort(reverse=True)
        out.append((g['verdict'], worst[:2]))
        print(trial, g['verdict'], worst[:3], flush=True)

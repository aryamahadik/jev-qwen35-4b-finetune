import sys, json, time
sys.path.insert(0, '.')
sys.dont_write_bytecode = True
import pilot, pilot_loaders as PL
sb = int(sys.argv[1])
with PL.open_family("T12") as kit:
    b = pilot.build_pilot(kit, 1000, seed_base=sb, run_g15=False)
    g6 = pilot.g6(b.infos)
    worst = []
    yn = g6['yes_no']; ch = g6['choice']
    for part, d, ch_ in (('yes_no', yn, yn['chance']), ('choice', ch, ch['chance'])):
        for v in ('a_question', 'b_options', 'c_card_without_question', 'd_meta'):
            for m in ('lr', 'gbt'):
                x = d[v][m]
                worst.append((round(x - ch_, 4), part, v, m, x))
    worst.sort(reverse=True)
    print(sb, g6['verdict'], worst[:3], 'n', yn['n'], ch['n'])

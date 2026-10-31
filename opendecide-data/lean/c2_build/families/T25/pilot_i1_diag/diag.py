"""in-memory diagnostic: python diag.py N SEED_BASE [--g15] [--skip-ml]"""
import sys, json, time
sys.path.insert(0, '.'); sys.dont_write_bytecode = True
import pilot, pilot_loaders as PL
from c2_kit import choiceplan as CP
n = int(sys.argv[1]); sb = int(sys.argv[2]); g15 = '--g15' in sys.argv; skipml = '--skip-ml' in sys.argv
t0 = time.time()
with PL.open_family("T25") as kit:
    b = pilot.build_pilot(kit, n, seed_base=sb, run_g15=g15, log=lambda m: print(m, file=sys.stderr, flush=True))
    plugin = kit.plugin
    print('build', json.dumps({k: v for k, v in b.stats.items() if k not in ('per_sampler','drop_examples','g4_metamorphic_checked')}))
    print('drop examples', json.dumps(b.stats['drop_examples'])[:1500])
    infos = b.infos
    sets = [rr.option_set for u in b.units for rr in u.rendered if rr.option_set is not None]
    rep = CP.plan_report(sets)
    print('plan_report', json.dumps(rep))
    g10 = pilot.g10(infos, b.units, plugin)
    for k, c in g10['checks'].items():
        print('G10', k, c['verdict'], json.dumps(c['value'])[:300])
    ov = pilot.overlay(b.units, plugin)
    print('overlay', ov['verdict'], {k: (c['value'], c['verdict']) for k, c in ov['checks'].items()})
    sp = pilot.spec30(infos, plugin)
    print('spec30', sp['verdict'], {k: c['value'] for k, c in sp['checks'].items() if k != 'register_max_share'}, sp['checks']['register_max_share']['registers'])
    if not skipml:
        g6 = pilot.g6(infos)
        print('G6', g6['verdict'], json.dumps({p: {v: g6[p][v] for v in g6[p] if isinstance(g6[p][v], dict) and 'lr' in g6[p][v]} | {'n': g6[p]['n'], 'chance': g6[p]['chance']} for p in ('yes_no', 'choice')}))
        print('G6 fails', json.dumps(g6.get('fails'))[:800])
        g7 = pilot.g7(infos)
        print('G7', g7['verdict'], g7.get('n_tests'), g7.get('n_choice_fails'), g7.get('n_yes_no_raw_fails'), g7.get('n_yes_no_card_adjusted_fails'))
print('seconds', round(time.time() - t0))

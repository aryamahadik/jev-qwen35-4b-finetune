"""scratch: G6 / G7 / G10 on a larger in-memory build (the full gate is >= 5,000 rows; spec 6.3)."""
import sys, json, time
sys.path.insert(0, '.')
sys.dont_write_bytecode = True
import pilot, pilot_loaders as PL
n = int(sys.argv[1]); seed_base = int(sys.argv[2]) if len(sys.argv) > 2 else pilot.SEED_BASE
t = time.time()
with PL.open_family("T12") as kit:
    b = pilot.build_pilot(kit, n, seed_base=seed_base, run_g15=False)
    infos = b.infos
    g6 = pilot.g6(infos)
    print('built', len(infos), round(time.time() - t), 's')
    print(json.dumps({'yes_no': {k: v for k, v in g6['yes_no'].items() if k in ('n','a_question','c_card_without_question','d_meta','b_options')},
                      'choice': g6['choice'], 'verdict': g6['verdict'], 'fails': g6['fails']}, indent=0))
    g10 = pilot.g10(infos, b.units, kit.plugin)
    print('G10', g10['verdict'], [ (k, v['value'] if not isinstance(v['value'], dict) else '...', v['verdict']) for k, v in g10['checks'].items() if v['verdict'] != 'pass'])
    print('longest', g10['checks']['longest_option_gold_pp'])
    print('cells', json.dumps(g10['checks']['yes_rate_cells'])[:3000])
    print('percard', json.dumps(g10['checks']['per_card_yes_rates'])[:600])

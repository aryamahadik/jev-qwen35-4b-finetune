"""One pilot-size build on another seed block (in memory) + the pilot's program gates. Never the 900000 block."""
import sys, json, time, os
sys.path.insert(0, '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
sys.dont_write_bytecode = True
import pilot as P, pilot_loaders as PL
base = int(sys.argv[1]); n = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
t0 = time.time()
with PL.open_family('T15') as kit:
    b = P.build_pilot(kit, n, seed_base=base, run_g15=False)
    infos = b.infos
    print('built', b.stats['rows_written'], 'units', b.stats['units_written'], 'attempted', b.stats['units_attempted'], 'drops', b.stats['drops_by_gate'], round(time.time() - t0), 's', flush=True)
    pg = P.program_gates(b)
    print('program gates', {g: pg[g]['verdict'] for g in P.PROGRAM_GATES})
    g6 = P.g6(infos); g7 = P.g7(infos); g10 = P.g10(infos, b.units, kit.plugin)
    ov = P.overlay(b.units, kit.plugin); s30 = P.spec30(infos, kit.plugin)
    yn, ch = g6['yes_no'], g6['choice']
    print('G6', g6['verdict'], 'yn n', yn.get('n'), 'chance', yn.get('chance'), {v: yn[v] for v in ('a_question','c_card_without_question','d_meta')})
    print('   choice n', ch.get('n'), 'chance', ch.get('chance'), {v: ch[v] for v in ('a_question','b_options','c_card_without_question','d_meta')})
    print('   fails', [(f['part'], f['view'], f['model'], f['acc'], f['chance']) for f in g6['fails']])
    print('G7', g7['verdict'], 'tests', g7['n_tests'], 'raw', g7['n_yes_no_raw_fails'], 'card', g7['n_yes_no_card_adjusted_fails'], 'choice', g7['n_choice_fails'])
    for f in g7['choice_fails'][:6]: print('    ', f)
    for f in g7['top5_choice'][:3]: print('   top', f)
    print('G10', g10['verdict'], g10['failing'])
    for k, v in g10['checks'].items():
        if k in ('longest_option_gold_pp', 'abstain_wrong_share', 'yes_no_share', 'yes_rate', 'double_negation_share', 'syntactic_negation_share', 'gold_position', 'gold_rank'):
            val = v['value'] if k not in ('abstain_wrong_share',) else {c: (x['rows'], x['abstain_gold'], round(x['wrong_share'], 3)) for c, x in v['cells'].items()}
            print('   ', k, v['verdict'], json.dumps(val)[:300])
    print('overlay', ov['verdict'], {k: v['value'] for k, v in ov['checks'].items()})
    print('spec30', s30['verdict'], {k: v['value'] for k, v in s30['checks'].items() if k in ('max_tokens', 'mean_tokens', 'deep_share', 'skin_max_rows', 'wording_max_share')})
    # ch_outcome / ch_claimant longest breakdown
    import collections
    lg = collections.defaultdict(lambda: [0.0, 0.0, 0])
    for i in infos:
        r = i.row
        if r['qtype'] != 'choice': continue
        o = r['options']; lens = [len(x) for x in o]; top = [j for j, x in enumerate(lens) if x == max(lens)]
        a = lg[r['meta']['qform']]; a[0] += (1 / len(top)) if o.index(r['gold']) in top else 0; a[1] += 1 / len(o); a[2] += 1
    print('longest pp by form', {q: (round(100 * (a[0] - a[1]) / a[2], 2), a[2]) for q, a in lg.items()})
    print('total seconds', round(time.time() - t0))

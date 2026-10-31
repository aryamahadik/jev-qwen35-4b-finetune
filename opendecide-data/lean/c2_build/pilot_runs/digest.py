import json, sys
sys.path.insert(0, '.')
import pilot_loaders as PL
fams = sys.argv[1:] or ['T35','T30','T24','T33','T29','T31','T32','T23','T15','T12','T25','t37b','T36','T21','T20']
for f in fams:
    rep = json.load(open(PL.family_dir(f)/'pilot'/'PILOT_REPORT.json'))
    g = rep['gates']
    print('=====', f, rep['summary']['verdict'], 'FAIL:', rep['summary']['fail'], 'rows', rep['files']['n_rows'])
    for part in ('yes_no','choice'):
        p = g['G6'][part]
        if 'skipped' in p or not p.get('n'): continue
        print('  G6', part, 'n', p['n'], 'chance', p['chance'], {k: (v['lr'], v['gbt']) for k, v in p.items() if isinstance(v, dict) and 'lr' in v})
        if p.get('d_meta_drivers'): print('     drivers', [(d['feature'], d['acc']) for d in p['d_meta_drivers'][:3]])
    g7 = g['G7']
    if g7['verdict'] == 'fail':
        print('  G7 raw', [(o['feature'], o['n'], o['yes_rate']) for o in g7['yes_no_raw_fails'][:4]], 'card', [(o['feature'], o['n'], o['yes_rate']) for o in g7['yes_no_card_adjusted_fails'][:4]], 'choice', g7['n_choice_fails'], [(o['feature'], o['n_rows'], o['gold_hits'], o['expected']) for o in g7['choice_fails'][:4]])
    for k in g['G10']['failing']:
        c = g['G10']['checks'][k]; print('  G10', k, json.dumps(c['value'])[:250])
    for sec in ('overlay', 'spec_3_0', 'S14_floors_caps'):
        if sec in g and g[sec].get('failing'):
            for k in g[sec]['failing']: print('  ', sec, k, g[sec]['checks'][k]['value'])
    for k in ('pilot_size','G2','G3','G4','G-SL','G-LEX','G-TW','G15','schema','options'):
        if k in g and (g[k]['verdict']=='fail' or g[k].get('units_failed')):
            print('  ', k, g[k]['verdict'], g[k].get('units_failed', g[k].get('value')), (g[k].get('examples') or [])[:2])
    if g.get('drops_outside_gates', {}).get('counts'): print('   other drops', g['drops_outside_gates']['counts'])
    print('   chunks', {k: len(v) for k, v in rep['chunks'].items()}, 'G3-H items', g.get('G3-H', {}).get('items'), 'G5-H rows', g['G5-H'].get('rows'))

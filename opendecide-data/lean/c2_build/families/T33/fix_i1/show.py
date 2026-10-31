import json, sys
d=json.load(open(sys.argv[1]))
st=d['stats']; print({k:st[k] for k in ('rows_written','units_written','units_attempted','drops_by_gate','drop_examples','seconds')})
g10=d['g10']; print('G10', g10['verdict'], g10['failing'])
for k,v in g10['checks'].items():
    val=v['value']
    if isinstance(val,(dict,list)): val=json.dumps(val)[:300]
    print('  ',k,v['verdict'],val)
ov=d['overlay']; print('overlay', ov['verdict'], {k:(v['value'],v['verdict']) for k,v in ov['checks'].items()})
sp=d['spec30']; print('spec30', sp['verdict'], {k:(v['value'],v['verdict']) for k,v in sp['checks'].items()})
print(sp['checks']['register_max_share']['registers'])
print(d['tokens']); print(d['styles']); print(d['skin_rows_hist'])
g7=d['g7']; print('G7', g7['verdict'], g7['n_yes_no_raw_fails'], g7['n_yes_no_card_adjusted_fails'], g7['n_choice_fails'], 'tests', g7['n_tests'])
print(json.dumps(g7['top5_yes_no_raw'])[:600]); print(json.dumps(g7['top5_choice'])[:600])
g6=d['g6']; print('G6', g6['verdict'], g6['fails']); print(json.dumps({k:g6[k] for k in ('yes_no','choice')})[:1500])

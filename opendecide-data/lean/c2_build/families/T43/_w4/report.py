import json, sys
d=json.load(open(sys.argv[1]))
def g6h(x):
    out={}
    for h,v in x['g6_by_head'].items():
        c=v['choice']; ch=c['chance']
        out[h]=(v['n'], {k:{m:round(100*(c[k][m]-ch),2) for m in ('lr','gbt')} for k in ('a_question','b_options','c_card_without_question','d_meta')})
    return out
def probes(x):
    return {k:{h:(v[h]['lr']['delta_pp'],v[h]['gbt']['delta_pp']) for h in v if isinstance(v[h],dict)} for k,v in (('opt',x['options_only']),('fmt',x['formatting_only']))}
for name,x in (('FULL',d),('PREFIX',d.get('at_prefix'))):
    if not x: continue
    print(name, x['n_rows'])
    c=x['g6']['choice']; ch=c['chance']
    print(' pooled', x['g6']['verdict'], {k:{m:round(100*(c[k][m]-ch),2) for m in ('lr','gbt')} for k in ('a_question','b_options','c_card_without_question','d_meta')})
    print(' byhead', json.dumps(g6h(x)))
    print(' probes', probes(x))
    print(' diff', x['diff_size']['models'], x['diff_size']['pass'])
for k in ('g7','g10','tokens','cards','heads','pv_gold','loc_none_share','diag','drops'): print(k, str(d[k])[:300])

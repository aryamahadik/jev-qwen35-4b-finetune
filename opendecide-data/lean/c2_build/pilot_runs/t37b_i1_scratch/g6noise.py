import sys, json, random, time
sys.path.insert(0, '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
import pilot as PI, pilot_t37b as P
rows=[json.loads(l) for l in open('/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/t37b/pilot_i1/rows.jsonl')]
random.seed(5)
res=[]
for t in range(8):
    sub=random.sample(rows, len(rows)-6)
    infos=[P._info(r) for r in sub]
    t0=time.time()
    g=PI.g6(infos)
    yn=g['yes_no']
    best=max(yn[v][m] for v in ('a_question','c_card_without_question','d_meta') for m in ('lr','gbt'))
    res.append((best, yn['d_meta']['gbt'], yn['a_question']['gbt'], yn['c_card_without_question']['gbt'], yn['yes_rate']))
    print(t, 'best', best, 'd_meta gbt', yn['d_meta']['gbt'], 'a gbt', yn['a_question']['gbt'], 'c gbt', yn['c_card_without_question']['gbt'], round(time.time()-t0,1),'s', flush=True)
import statistics as S
print('d_meta gbt mean', S.mean(r[1] for r in res), 'sd', S.pstdev(r[1] for r in res), 'best mean', S.mean(r[0] for r in res), 'frac fail', sum(r[0]>0.52+1e-9 for r in res)/len(res))

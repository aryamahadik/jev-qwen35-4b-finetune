import json,sys
from collections import Counter,defaultdict
sys.path.insert(0,'.')
dirs=['pilot_i3b_full']+[f'pilot_i3b_qc{i}' for i in range(2,7)]
rows=[]
for d in dirs:
    for l in open(f't37b/{d}/rows.jsonl'):
        r=json.loads(l); r['_d']=d; rows.append(r)
S=defaultdict(Counter)
for r in rows:
    t=r['meta']['t37b']; s=t['base_source']
    S[s]['n']+=1; S[s]['eq']+= t['kind']=='equiv'; S[s]['by']+=t['base_gold']; S[s]['py']+=r['gold']
    S[s]['eq_by']+= (t['kind']=='equiv' and t['base_gold']==1); S[s]['eq_bn']+=(t['kind']=='equiv' and t['base_gold']==0)
    S[s]['by_n']+=0
print(len(rows))
print('source n eq%% base_yes%% partner_yes%% P(eq|by) P(eq|bn)')
for s,c in sorted(S.items(),key=lambda x:-x[1]['n']):
    n=c['n']; by=c['by']; bn=n-by
    print(f"{s:40s} {n:5d} {c['eq']/n:.2f} {by/n:.2f} {c['py']/n:.2f} {c['eq_by']/max(by,1):.2f} {c['eq_bn']/max(bn,1):.2f}")

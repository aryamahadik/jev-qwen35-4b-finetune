import json,sys,hashlib
from collections import Counter,defaultdict
sys.path.insert(0,'.')
import pilot as PI, pilot_t37b as PT
dirs=['pilot_i3b_full']+[f'pilot_i3b_qc{i}' for i in range(2,7)]
rows=[]
for d in dirs:
    for l in open(f't37b/{d}/rows.jsonl'):
        r=json.loads(l); r['id']=d+'|'+r['id']; rows.append(r)
def bal(rows,tau,drop=()):
    g=defaultdict(lambda:defaultdict(list))
    for r in rows:
        t=r['meta']['t37b']
        if t['base_source'] in drop: continue
        g[(t['base_source'],t['base_gold'])][t['kind']=='equiv'].append(r)
    out=[]
    for k,d in g.items():
        m=min(len(d[True]),len(d[False])); lim=int(m*(1+tau)/(1-tau)) if tau<1 else 10**9
        for side in (True,False):
            l=sorted(d[side],key=lambda r:hashlib.md5(r['id'].encode()).hexdigest())
            out+=l[:max(m,min(len(l),lim))] if m>0 else []
    return out
for tau in (0,0.2,0.33,0.5,0.6,0.8):
    sub=bal(rows,tau)
    # keep partner gold balanced overall? report
    y=PI.g6([PT._info(r) for r in sub])['yes_no']
    q=sum(r['meta']['t37b']['kind']=='equiv' for r in sub)/len(sub)
    print(tau,len(sub),round(q,2),round(sum(r['gold'] for r in sub)/len(sub),3),y['c_card_without_question'],y['d_meta'],flush=True)

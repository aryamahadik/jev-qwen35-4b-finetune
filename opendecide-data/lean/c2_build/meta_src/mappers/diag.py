import json, sys, re, math
from collections import Counter, defaultdict
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold, cross_val_predict
rows=[json.loads(l) for l in open(sys.argv[1])]
tc=Counter(r['meta']['task_id'] for r in rows)
print('short tasks', {t:n for t,n in tc.items() if n<13})
# per-qform yes/no feature diag
yn=[r for r in rows if r['qtype']=='noul']
def feats(r):
    ns=[float(x.replace(',','')) for x in re.findall(r'\d[\d,]*\.?\d*', r['state']+' '+r['instructions']+' '+(r['card'] or '')) if x.replace(',','').replace('.','').isdigit()]
    ls=[math.log10(1+abs(v)) for v in ns][:4]+[0]*4
    return ls[:4]+[len(r['state'])/500,len(r['instructions'])/200,len(ns)]
by=defaultdict(list)
for r in yn: by[r['meta']['qform']].append(r)
for q,rr in by.items():
    if len(rr)<40: continue
    X=np.array([feats(r) for r in rr]); y=np.array([r['gold'] for r in rr]); g=[r['group_id'] for r in rr]
    pr=cross_val_predict(LogisticRegression(max_iter=300),X,y,cv=GroupKFold(5),groups=g)
    print(q,len(rr),round((pr==y).mean(),3),'yes',round(y.mean(),2))
ch=[r for r in rows if r['qtype']=='choice']
gold=Counter(r['gold'] for r in ch); app=Counter(o for r in ch for o in r['options'])
byq=defaultdict(lambda:[0,0.0,0])
for r in ch:
    k=len(r['options']); sc=[(gold[o]-(o==r['gold'])+1/k)/(app[o]-1+1) for o in r['options']]
    b=max(sc); tops=[o for o,s in zip(r['options'],sc) if s==b]
    d=byq[r['meta']['qform']]; d[0]+=(r['gold'] in tops)/len(tops); d[1]+=1/k; d[2]+=1
for q,(a,c,n) in byq.items(): print(q,n,'prior',round(a/n,3),'chance',round(c/n,3))

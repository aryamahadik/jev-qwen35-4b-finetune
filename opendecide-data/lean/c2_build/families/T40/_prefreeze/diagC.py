import sys, collections
from pathlib import Path
sys.dont_write_bytecode=True
C2=Path(__file__).resolve().parents[3]; sys.path.insert(0,str(C2))
import pilot, numpy as np
from families.T40 import loader, fixtures, plugin as TP
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import GroupKFold
loader.register(); ctx=fixtures.make_ctx(); p=TP.T40Plugin(lexicon=ctx.lexicon)
rows=[]
for s in range(0,9000):
    c=TP.design(s,("S1","S2","S3","S4")[s%4] if False else "S1")
    if c["kind"]!="ch" or c["head"]!="C": continue
    sp=p.sample(s,"S1"); rr=p.render(sp,ctx); q,cx=pilot.split_question(rr)
    rows.append((p.label(sp),pilot.RowInfo(rr.row,sp,rr,0,q,cx,None)))
    if len(rows)>=2400: break
y=np.array([l for l,_ in rows]); g=np.array([i.row["meta"]["card_id"] for _,i in rows])
feats=[pilot.meta_features(i)[1] for _,i in rows]; keys=sorted(feats[0])
X=np.array([[f[k] for k in keys] for f in feats])
print(len(rows),collections.Counter(y), "ncards",len(set(g)))
def cv(Xs):
    pr=np.empty(len(y),dtype=y.dtype)
    for tr,te in GroupKFold(5).split(Xs,y,g): pr[te]=HistGradientBoostingClassifier(max_iter=100,random_state=0).fit(Xs[tr],y[tr]).predict(Xs[te])
    return round(float((pr==y).mean()),3)
print("all",cv(X))
for j,k in enumerate(keys): print(k,cv(X[:,[j]]))
import itertools
print("drop-one")
for j,k in enumerate(keys): print(k,cv(np.delete(X,j,axis=1)))
use=[keys.index(k) for k in ("len_state","n_lines","n_numbers","mag_mean","mag_max")]
for a,b in itertools.combinations(use,2): print(keys[a],keys[b],cv(X[:,[a,b]]))
# raw old/new
from families.T40 import edit as E

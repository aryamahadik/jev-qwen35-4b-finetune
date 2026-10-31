import sys, pickle, types, collections
sys.dont_write_bytecode=True; sys.path.insert(0,'.')
import numpy as np
from families.T43 import probes as PR
rows=pickle.load(open(sys.argv[1],'rb'))
pv=[(r,st) for r,st in rows if st["head"]=="pv" and r["gold"]!="does not apply"]
labs={"fixes the bug":0,"does not fix the bug":1,"passes the target test but is still wrong":2}
y=np.array([labs[r["gold"]] for r,_ in pv]); F=[PR.size_features(st) for _,st in pv]; names=list(F[0])
g=[r["meta"]["card_id"] for r,_ in pv]; folds=PR._folds(g); maj=np.bincount(y).max()/len(y)
def cv(cols):
    X=np.array([[f[k] for k in cols] for f in F],float); pred=np.zeros(len(y),int)
    for tr,te in folds: pred[te]=PR._gbt().fit(X[tr],y[tr]).predict(X[te])
    return round((pred==y).mean()-maj,4)
print('all',cv(names), names)
for k in names: print(k,'only',cv([k]),'drop',cv([n for n in names if n!=k]))
# label share by hunks & changed
for k in ("hunks","added","removed"):
    c=collections.defaultdict(collections.Counter)
    for f,l in zip(F,y): c[f[k]][l]+=1
    print(k,{v:[round(c[v][l]/sum(c[v].values()),3) for l in range(3)] for v in sorted(c)})

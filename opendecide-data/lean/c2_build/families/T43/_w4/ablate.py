import sys, pickle, math, re, collections
sys.dont_write_bytecode=True; sys.path.insert(0,'../../..')
import numpy as np
import pilot
from sklearn.ensemble import HistGradientBoostingClassifier as G
from sklearn.model_selection import GroupKFold
rows=pickle.load(open(sys.argv[1],'rb'))
def feats(r, st):
    nums=pilot._nums(r.get("state","")+"\n"+(r.get("card") or "")+"\n"+r.get("instructions",""))
    mag=[math.log10(abs(x)) if x else 0.0 for x in nums]
    s=r["state"]
    f={"len_state":len(s),"len_ins":len(r["instructions"]),"n_numbers":len(nums),"mag_max":max(mag) if mag else -1,"mag_mean":sum(mag)/len(mag) if mag else -1,
       "n_lines":s.count("\n")+1,"depth":r["meta"].get("depth") or 0,"code_len":len(st["code"]),"orig_len":len(st["orig"]),
       "delta":len(st["code"])-len(st["orig"]),"n_tests":len(st["tests"]),"patch_len":len(st["patch"] or ""),"maxline":max(map(len,s.split("\n")))}
    return f
def cv(X,y,g):
    X=np.array(X,float); y=np.array(y); pred=np.zeros(len(y),int)
    for tr,te in GroupKFold(5).split(X,y,groups=g):
        pred[te]=G(max_iter=150,learning_rate=0.08,random_state=0).fit(X[tr],y[tr]).predict(X[te])
    return (pred==y).mean()
for head in sys.argv[2].split(','):
    sel=[(r,st) for r,st in rows if st["head"]==head and r["gold"] not in ("does not apply",)]
    gold=[r["gold"] for r,_ in sel]; cl=sorted(set(gold)); y=[cl.index(x) for x in gold]
    g=[r["meta"]["card_id"] for r,_ in sel]
    F=[feats(r,st) for r,st in sel]; names=list(F[0])
    base=max(collections.Counter(y).values())/len(y)
    print(head,len(sel),"majority",round(base,4))
    print(" all", round(cv([[f[k] for k in names] for f in F],y,g)-base,4))
    for k in names:
        print("  only",k, round(cv([[f[k]] for f in F],y,g)-base,4), " | drop", round(cv([[f[n] for n in names if n!=k] for f in F],y,g)-base,4))

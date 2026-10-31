import sys, pickle, re, collections
sys.dont_write_bytecode=True; sys.path.insert(0,'../../..')
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier as G
from sklearn.model_selection import GroupKFold
rows=pickle.load(open(sys.argv[1],'rb'))
sel=[(r,st) for r,st in rows if st["head"]==sys.argv[2]]
def f(r,st):
    s=r["state"]; lines=s.split("\n")
    ind=[len(re.match(r"[ \t>|0-9]*",ln).group()) for ln in lines]
    run=r["state"].split("<run>")[-1] if "<run>" in r["state"] else ""
    return {"lay_len":len(s),"lay_lines":len(lines),"maxline":max(map(len,lines)),"ind_max":max(ind),"ind_mean":float(np.mean(ind)),
            "code_lines":len(st["code"].split("\n")),"code_len":len(st["code"]),"q_len":len(r["instructions"]),
            "delta":len(st["code"])-len(st["orig"]),"n_tests":len(st["tests"]),"nopt":len(r["options"])}
gold=[r["gold"] for r,_ in sel]; cl=sorted(set(gold)); y=np.array([cl.index(x) for x in gold]); g=[r["meta"]["card_id"] for r,_ in sel]
F=[f(r,st) for r,st in sel]; names=list(F[0]); base=max(collections.Counter(y).values())/len(y)
def cv(cols):
    X=np.array([[d[k] for k in cols] for d in F],float); p=np.zeros(len(y),int)
    for tr,te in GroupKFold(5).split(X,y,groups=g): p[te]=G(max_iter=150,learning_rate=0.08,random_state=0).fit(X[tr],y[tr]).predict(X[te])
    return round((p==y).mean()-base,4)
print(sys.argv[2],len(sel),"majority",round(base,4),"all",cv(names))
for k in names: print(" only",k,cv([k])," drop",cv([n for n in names if n!=k]))
# per-line delta spread
dd=collections.defaultdict(collections.Counter)
for (r,st),d in zip(sel,F): dd[r["gold"]][d["delta"]]+=1
for k in sorted(dd): print(k, dict(sorted(dd[k].items())))

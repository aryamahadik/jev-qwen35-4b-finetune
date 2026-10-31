import sys, collections
sys.path.insert(0,'.')
from families.T42 import prefreeze as PF
import pilot
b = PF.build(2400, 9)
out=[i for i in b.infos if i.row["meta"]["qform"] in ("ch_output","ch_return")]
def pred(i, which, rev=False):
    r=i.row; opts=r["options"]; vt=set(pilot.toks(i.context))
    sc=[]
    for o in opts:
        ou=pilot.toks(o); ov=set(ou)&vt
        sc.append({"ovf":len(ov)/max(1,len(set(ou))),"ovn":len(ov),"tl":len(ou),"cl":len(o)}[which])
    if rev: sc=[-x for x in sc]
    m=max(sc); top=[j for j,x in enumerate(sc) if x>=m-1e-9]
    return (opts.index(r["gold"]) in top)/len(top)
res=collections.defaultdict(lambda:[0,0.0,0])
for i in out:
    exc=any(o.startswith("raises ") for o in i.row["options"])
    gexc=i.row["gold"].startswith("raises ")
    k=len(i.row["options"])
    for which in ("ovf","ovn","tl","cl"):
        for rev in (False,True):
            for sl in ("all","exc_row" if exc else "noexc_row"):
                x=res[(which,rev,sl)]; x[0]+=pred(i,which,rev); x[1]+=1/k; x[2]+=1
for kx,(h,e,n) in sorted(res.items()): print(kx, n, round(h/n,4), round(e/n,4), round((h-e)/n*100,2))

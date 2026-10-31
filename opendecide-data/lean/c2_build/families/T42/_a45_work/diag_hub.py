import sys, collections
sys.path.insert(0,'.')
from multiprocessing import get_context
from families.T42 import plugin as P
def one(seed):
    pl,_=P.make_plugin()
    out=[]
    for smp in ("S1","S2","S4"):
        try:
            sp=pl.sample(seed*10+{"S1":0,"S2":1,"S4":2}[smp],smp)
        except Exception: continue
        st=sp.structure
        k=len(st["distractors"])+1
        out.append((k, st["shown_is_hub"], st["template"], st["gold_kind"]))
    return out
if __name__=="__main__":
    with get_context("fork").Pool(8) as p:
        res=[x for r in p.map(one, range(1000,1250)) for x in r]
    n=len(res); hub=sum(h for _,h,_,_ in res); exp=sum(1/k for k,_,_,_ in res)
    print(n, hub, round(exp,1))
    by=collections.defaultdict(lambda:[0,0.0])
    for k,h,t,g in res:
        by[t][0]+=h; by[t][1]+=1/k
    for t,(h,e) in sorted(by.items()): print(t, h, round(e,1))

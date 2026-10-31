"""Smoke: the i1 plan on 4,000 base specs (S1-S4, seeds 0-999): abstain share per k, position per k, outcome, longest."""
import sys, collections, time
sys.path.insert(0, ".")
from families.T07 import load_v2 as L, plugin as P
t=time.time()
pools = L.load_pools(); ctx = L.make_ctx(pools)
pl = P.T07Plugin(lexicon=ctx.lexicon)
print("load", round(time.time()-t,1)); t=time.time()
cf = collections.defaultdict(lambda: [0,0]); pos = collections.defaultdict(collections.Counter); co = collections.Counter()
n=0
for smp in ("S1","S2","S3","S4"):
    for seed in range(1000):
        s = pl.sample(seed, smp); n+=1
        if s.qform=="ch_failing":
            k=len(P.failing_dims(s.structure))+1
            a = pl.solve_a(s)
            cf[k][0]+=1; cf[k][1]+= (a=="none")
            pos[("cf-abstain-slot",k)][pl.row_plan(smp,seed,"ch_failing").abstain_slot]+=1
        elif s.qform=="ch_offers":
            co[pl.solve_a(s).split(":")[0]]+=1
            pos[("co-outcome",4)][pl.row_plan(smp,seed,"ch_offers").outcome]+=1
print("sample", round(time.time()-t,1), "specs", n)
for k,(r,a) in sorted(cf.items()): print("ch_failing k",k,"rows",r,"abstain",a,"share %.3f"%(a/r),"1/k %.3f"%(1/k))
print("offers", co)
for k,v in sorted(pos.items()): print(k, dict(sorted(v.items())))

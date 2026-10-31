import sys, collections
sys.path.insert(0, ".")
from families.T07 import load_v2 as L, plugin as P, fixtures as FX
which = sys.argv[1] if len(sys.argv) > 1 else "fx"
if which == "fx":
    ctx = FX.ctx()
else:
    ctx = L.make_ctx(L.load_pools())
pl = P.T07Plugin(lexicon=ctx.lexicon)
specs = [pl.sample(seed, smp) for smp in ("S1","S2","S3","S4") for seed in range(500)]
def control(s):
    a = pl.solve_a(s)
    return a == "both" if s.qform == "ch_offers" else (a == "none" if s.qform == "ch_failing" else bool(a) == P.YES_MEANS_GETS[s.qform])
print(which, "controls", sum(control(s) for s in specs)/len(specs))
cf=[pl.solve_a(s) for s in specs if s.qform=="ch_failing"]; print("cf none", cf.count("none")/len(cf), len(cf))
co=collections.Counter(pl.solve_a(s).split(":")[0] for s in specs if s.qform=="ch_offers"); print(co)

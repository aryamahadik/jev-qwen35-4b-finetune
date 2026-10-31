import sys, time, cProfile, pstats
sys.path.insert(0, ".")
from families.T07 import load_v2 as L, plugin as P
pools = L.load_pools(); ctx = L.make_ctx(pools)
pl = P.T07Plugin(lexicon=ctx.lexicon)
t=time.time()
cProfile.run("pl.choice_cell('S1', 20000)", "/dev/null") if False else None
pr = cProfile.Profile(); pr.enable()
pl.choice_cell('S1', 20000)
pr.disable()
print("20000 pairs", round(time.time()-t,2), "s")
pstats.Stats(pr).sort_stats("cumulative").print_stats(8)

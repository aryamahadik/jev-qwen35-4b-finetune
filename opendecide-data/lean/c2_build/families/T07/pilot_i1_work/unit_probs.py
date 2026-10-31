import sys, collections
sys.path.insert(0, ".")
from c2_kit import pipeline
from families.T07 import load_v2 as L, plugin as P
pools = L.load_pools(); ctx = L.make_ctx(pools)
pl = P.T07Plugin(lexicon=ctx.lexicon)
cnt = collections.Counter(); ex = {}
N = int(sys.argv[1]) if len(sys.argv) > 1 else 120
for smp in ("S1","S2","S3","S4"):
    for seed in range(900000, 900000+N):
        s = pl.sample(seed, smp)
        r = pipeline.build_unit(pl, s, ctx, run_g15=False)
        for g, d in r.problems:
            key = (g, s.qform, d[:110]); cnt[key] += 1; ex.setdefault(key, (smp, seed))
for k, v in cnt.most_common(12): print(v, k, ex[k])

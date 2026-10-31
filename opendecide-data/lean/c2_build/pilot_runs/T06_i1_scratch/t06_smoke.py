import sys, collections, time
sys.dont_write_bytecode = True
sys.path.insert(0, '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
from families.T06 import fixtures as FX, plugin as T
from c2_kit import pipeline
ctx = FX.ctx(); pl = T.T06Plugin(lexicon=ctx.lexicon)
t0=time.time(); bad=collections.Counter(); ex={}
n=0
for seed in range(150):
    for smp in pl.SAMPLERS:
        try:
            spec = pl.sample(seed, smp)
        except Exception as e:
            bad['sample:'+type(e).__name__]+=1; ex.setdefault('sample:'+type(e).__name__, f'{smp}/{seed}: {e}'); continue
        res = pipeline.build_unit(pl, spec, ctx, run_g15=False)
        n+=1
        for g,p in res.problems:
            bad[g]+=1; ex.setdefault(g, f'{smp}/{seed} {spec.qform}: {p}')
print(n, dict(bad), time.time()-t0)
for k,v in ex.items(): print(k, v[:400])

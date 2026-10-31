import sys, collections, time
sys.path.insert(0, '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
sys.dont_write_bytecode = True
import pilot_loaders as PL
from c2_kit import pipeline
t0 = time.time()
with PL.open_family('T15') as kit:
    plugin, ctx = kit.plugin, kit.ctx
    from c2_kit.plugin import validate_plugin, check_independence
    print('validate', validate_plugin(plugin, strict=True)[:5], check_independence(plugin)[:3])
    probs = collections.Counter(); ex = []
    n = ok = 0
    for seed in range(int(sys.argv[1]), int(sys.argv[2])):
        for smp in ('S1','S2','S3','S4','S5'):
            try:
                spec = plugin.sample(seed, smp)
            except Exception as e:
                probs['sample'] += 1; ex.append((seed, smp, repr(e)[:200])); continue
            res = pipeline.build_unit(plugin, spec, ctx, run_g15=(seed % 10 == 0))
            n += 1
            if res.ok: ok += 1
            else:
                for g, d in res.problems:
                    probs[g] += 1
                    if len(ex) < 8: ex.append((seed, smp, spec.qform, g, d[:300]))
    print(n, ok, dict(probs), time.time() - t0)
    for e in ex: print(e)

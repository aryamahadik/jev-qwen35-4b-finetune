import sys, collections, time
sys.dont_write_bytecode = True
sys.path.insert(0, ".")
import pilot_loaders as PL
from c2_kit.plugin import ContractError
with PL.open_family("T32") as kit:
    p = kit.plugin
    fails = collections.Counter(); tot = collections.Counter(); t = time.time()
    shp = collections.defaultdict(collections.Counter)
    for smp in ("S1", "S2", "S3", "S4", "S5"):
        for seed in range(int(sys.argv[1])):
            try:
                sp = p.sample(seed, smp)
                st = p._fold(sp)[0]
                s = p._shape(smp, seed)
                shp[(smp, s.E, s.C, s.F)][st] += 1
                tot[(smp, "ok")] += 1
            except ContractError as e:
                fails[(smp, str(e)[:60])] += 1
    print(time.time() - t, dict(tot)); print(dict(fails))
    for k, v in sorted(shp.items()): print(k, dict(v))

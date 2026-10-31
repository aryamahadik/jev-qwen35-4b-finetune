"""T28 i1 diagnostic: abstain gold share of ch_rule bases by k (sample only, no render) and the plan_report of rendered rows."""
import sys, collections
sys.dont_write_bytecode = True
sys.path.insert(0, ".")
import pilot_loaders as PL
from c2_kit import pipeline
N = int(sys.argv[1]) if len(sys.argv) > 1 else 1500
with PL.open_family("T28") as kit:
    pl, ctx = kit.plugin, kit.ctx
    c = collections.defaultdict(lambda: [0, 0])
    for sampler in ("S1", "S2", "S3", "S4"):
        for seed in range(900000, 900000 + N):
            if seed % 40 < 34 or seed % 40 > 37:
                continue
            spec = pl.sample(seed, sampler)
            k = len(spec.structure["rules"]) + 1
            c[k][0] += 1
            c[k][1] += pl.solve_a(spec) == "default"
    tot = [0, 0, 0.0]
    for k, (n, a) in sorted(c.items()):
        print(k, n, a, round(a / n, 3), "plan", round(1 / k, 3))
        tot[0] += n; tot[1] += a; tot[2] += n / k
    print("all", tot[0], tot[1], "expected", round(tot[2], 1))

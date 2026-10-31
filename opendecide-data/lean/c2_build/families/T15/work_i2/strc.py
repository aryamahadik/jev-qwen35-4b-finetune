import sys, collections
sys.dont_write_bytecode = True
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build")
import pilot_loaders as PL
from scipy.stats import chi2_contingency
with PL.open_family("T15") as kit:
    P = kit.plugin
    rows = collections.defaultdict(collections.Counter)
    for sampler in ("S1", "S2", "S3", "S4"):
        for seed in range(900000, 900000 + 2500):
            try:
                s = P.sample(seed, sampler)
            except Exception:
                continue
            if s.qform not in ("ch_outcome", "ch_claimant"):
                continue
            a = P.solve_a(s); st = s.structure
            if s.qform == "ch_outcome":
                k = len(st["gates"]); route = st["route"]
                lab = a
                rows[("out", k, "route")][(lab, "R" if route else "-")] += 1
                rows[("out", k, "nskip")][(lab, len(route) if route else 0)] += 1
                rows[("out", k, "deep")][(lab, s.deep)] += 1
            else:
                m = st["people"]; lab = "nobody" if a == "NONE" or a is None or str(a).startswith("__") else "person"
                rows[("clm", m, "deep")][(lab, s.deep)] += 1
                rows[("clm", "all", "m")][(lab, m)] += 1
                rows[("clm", "all", "tags")][(lab, "third" if "third_tiebreak" in s.tags else "-")] += 1
                rows[("clm", "all", "months_min")][(lab, "mm" if "months_at_minimum" in s.tags else "-")] += 1
for key, c in sorted(rows.items(), key=str):
    labs = sorted({a for a, b in c}, key=str); cols = sorted({b for a, b in c}, key=str)
    tab = [[c[(l, x)] for x in cols] for l in labs]
    if len(cols) < 2 or len(labs) < 2: continue
    chi, p, dof, _ = chi2_contingency(tab)
    print(key, "p=%.4f" % p, labs, cols, tab)

"""T26 fix iteration 1: how much do the pilot-size shares move from window to window? (aligned windows of 141 seeds per
training sampler, like pilot.py's; in memory; the first 'seed' of window j is base + 160 j)."""
import collections, json, sys, statistics
from pathlib import Path
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(C2))
from c2_kit import choiceplan, pipeline  # noqa: E402
from families.T26 import loader as LD, plugin as P  # noqa: E402

base, nwin, per = int(sys.argv[1]), int(sys.argv[2]), 141
out = []
with LD.open_t26() as kit:
    pl, ctx = kit.plugin, kit.ctx
    for j in range(nwin):
        units = []
        for k in range(per):
            for smp in ("S1", "S2", "S3", "S4"):
                u = pipeline.build_unit(pl, pl.sample(base + 160 * j + k, smp), ctx, run_g15=False)
                if u.ok:
                    units.append(u)
        rows = [r for u in units for r in u.rows]
        n = len(rows)
        yn = [r for r in rows if r["qtype"] == "noul"]
        kinds = collections.Counter(r["meta"]["twin_kind"] for r in rows)
        sets = [rr.option_set for u in units for rr in u.rendered if rr.option_set is not None]
        rep = choiceplan.plan_report(sets)
        out.append({"rows": n, "yn": round(len(yn) / n, 3), "yes": round(sum(r["gold"] for r in yn) / len(yn), 3),
                    "twin": round(kinds["minimal_edit"] / n, 3), "equiv": round(kinds["equiv"] / n, 3),
                    "attack": round(kinds["attack"] / n, 3), "comp": round(2 * kinds["complement"] / len(yn), 3),
                    "longest": rep["longest_gold_pp"]})
        print(out[-1], flush=True)
for k in ("yn", "yes", "twin", "equiv", "attack", "comp", "longest"):
    v = [o[k] for o in out]
    print(k, "mean", round(statistics.mean(v), 3), "sd", round(statistics.pstdev(v), 3), "min", min(v), "max", max(v))

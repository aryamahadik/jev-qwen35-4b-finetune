import collections, json, sys, statistics
from pathlib import Path
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(C2))
from c2_kit import pipeline  # noqa: E402
from families.T26 import loader as LD, plugin as P  # noqa: E402

base, nwin, per = int(sys.argv[1]), int(sys.argv[2]), 141
dev = collections.defaultdict(list)
with LD.open_t26() as kit:
    pl, ctx = kit.plugin, kit.ctx
    for j in range(nwin):
        units = []
        for k in range(per):
            for smp in ("S1", "S2", "S3", "S4"):
                u = pipeline.build_unit(pl, pl.sample(base + 160 * j + k, smp), ctx, run_g15=False)
                if u.ok:
                    units.append(u)
        rr = [r for u in units for r in u.rendered if r.option_set is not None]
        nch = len(rr)
        tot = 0.0
        row = {}
        for kind in (None, "minimal_edit", "equiv", "attack"):
            for q in ("ch_verdict", "ch_failing"):
                xs = [r for r in rr if r.row["meta"]["twin_kind"] == kind and r.row["meta"]["qform"] == q]
                d = sum((r.option_set.gold.role == "gold" and r.option_set.meta["gold_is_abstain"]) - 1 / len(r.option_set.options) for r in xs)
                row[f"{kind}|{q}"] = round(d, 2)
                tot += d
        row["total_rows"] = round(100 * tot / nch, 2)
        print(row, flush=True)
        for k, v in row.items(): dev[k].append(v)
for k, v in dev.items():
    print(k, "mean", round(statistics.mean(v), 2), "sd", round(statistics.pstdev(v), 2))

"""A43 (a) G6/G7 on pooled independently seeded draws of the T37b generator (QC only, never training rows).
  cd lean/c2_build && nice -n 10 ../../.venv/bin/python -B -m t37b.g6_pool_i3 [--dirs pilot_i3_full pilot_i3_qc2 ...]
Pools rows.jsonl of every draw (row ids made unique by a draw prefix), runs pilot.g6 / g7 unchanged, reports base overlap."""
import argparse, json, sys, itertools
from pathlib import Path
C2 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2))
import pilot as PI, pilot_t37b as PT  # noqa: E402
ap = argparse.ArgumentParser()
ap.add_argument("--dirs", nargs="+", default=["pilot_i3_full"] + [f"pilot_i3_qc{i}" for i in range(2, 7)])
ap.add_argument("--out", default="pilot_i3_full/G6_POOLED.json")
a = ap.parse_args()
here = Path(__file__).resolve().parent
rows, bases = [], {}
for d in a.dirs:
    bs = set()
    for line in open(here / d / "rows.jsonl", encoding="utf-8"):
        r = json.loads(line)
        bs.add(r["meta"]["t37b"]["base_id"])
        r["id"] = f"{d}|{r['id']}"
        rows.append(r)
    bases[d] = bs
ov = {}
for x, y in itertools.combinations(a.dirs, 2):
    ov[f"{x}|{y}"] = round(len(bases[x] & bases[y]) / len(bases[x]), 3)
allb = set().union(*bases.values())
infos = [PT._info(r) for r in rows]
g6, g7 = PI.g6(infos), PI.g7(infos)
out = {"dirs": a.dirs, "n_rows": len(rows), "distinct_bases": len(allb), "bases_per_draw": {d: len(b) for d, b in bases.items()},
       "mean_pairwise_base_overlap": round(sum(ov.values()) / len(ov), 3), "pairwise_base_overlap": ov,
       "G6": g6, "G7_verdict": g7.get("verdict"), "G7_raw_fails": g7.get("yes_no_raw_fails"),
       "G7_card_adjusted_fails": g7.get("yes_no_card_adjusted_fails"), "G7_n_tests": g7.get("n_tests")}
(here / a.out).write_text(json.dumps(out, indent=1, default=str))
print(json.dumps({k: out[k] for k in ("n_rows", "distinct_bases", "mean_pairwise_base_overlap")}))
print(json.dumps(g6["yes_no"])[:800], g6["verdict"], g6["fails"])
print(out["G7_verdict"], [ (f["feature"], f["n"], f["yes_rate"]) for f in out["G7_raw_fails"] or []], out["G7_card_adjusted_fails"])

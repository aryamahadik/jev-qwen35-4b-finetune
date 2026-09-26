"""Score JevBench v1.4.2 public-item runs with the benchmark's own formulas (composite_v13 axes + composite_v14 gates).

Public items only (no judge or sealed tier), so Intelligence is the tier-weighted chance-corrected accuracy over
easy / standard / hard with the weights renormalised, the same code path the official harness uses when a tier is
missing. Calibration = composite_v13.calibration(ECE top-label on the hard tier, mean TVD to gold_probs).
Speed: Jev = production API (raw client latency); ours = self-hosted GPU (x2 + 0.15 s, the official penalty).
Cost: $ per 1,000 decisions = measured input tokens x tariff (Jev $0.042/M; ours priced at the base model's list price).
Paired bootstrap (10k) on per-item correctness vs the reference run, overall and per split.

  python score_jevbench.py REF RUN [RUN ...] --kinds api,gpu,... --prices 0.042,0.10,... [--items A|B|all]
"""
import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "jevbench"))
from jevbench import composite_v13 as c13  # noqa: E402
from jevbench import composite_v14 as c14  # noqa: E402
from jevbench.metrics import ece_top_label  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("runs", nargs="+")
ap.add_argument("--kinds", required=True)
ap.add_argument("--prices", required=True, help="$ per 1M input tokens, one per run")
ap.add_argument("--items", default="all")
ap.add_argument("--out_prices", default=None, help="$ per 1M output tokens, one per run (System-2 rationale tokens)")
a = ap.parse_args()

tier, gold = {}, {}
for t, name in (("easy", "easy"), ("original", "standard"), ("hard", "hard")):
    for l in open(HERE / f"jevbench/datasets/public/{t}.jsonl"):
        d = json.loads(l)
        tier[d["id"]] = name
        if (d.get("provenance") or {}).get("gold_probs"):
            gold[d["id"]] = (d["provenance"]["gold_probs"], d["labels"])
ids = set(tier)
if a.items in ("A", "B"):
    ids = {json.loads(l)["id"] for l in open(HERE / f"splits/jevbench_{a.items}.jsonl")}
runs = {n: {r["task_id"]: r for r in map(json.loads, open(HERE / f"runs/{n}/results.jsonl")) if r["task_id"] in ids}
        for n in a.runs}
out = {}
outp = list(map(float, a.out_prices.split(","))) if a.out_prices else [0.0] * len(a.runs)
for n, kind, price, oprice in zip(a.runs, a.kinds.split(","), map(float, a.prices.split(",")), outp):
    R = runs[n]
    acc = {t: np.mean([r["correct"] for i, r in R.items() if tier[i] == t]) for t in ("easy", "standard", "hard")}
    intel = c13.intelligence(acc)
    hard = [(max(r["probs"].values()) if r.get("probs") else 0.0, r["correct"]) for i, r in R.items() if tier[i] == "hard"]
    ece = ece_top_label(hard)["ece"]
    tv = [c13.tvd(R[i]["probs"] or {}, g, labs) for i, (g, labs) in gold.items() if i in R]
    calib = c13.calibration(ece, float(np.mean(tv)) if tv else None)
    lat = sorted(r["latency_s"] for r in R.values())
    p50, p95 = lat[len(lat) // 2], lat[int(0.95 * len(lat))]
    spd = c13.speed(p50, p95, kind)
    toks = np.mean([(r.get("usage") or {}).get("input_tokens") or 0 for r in R.values()])
    otoks = np.mean([(r.get("usage") or {}).get("output_tokens") or 0 for r in R.values()])
    usd_per_1000 = (toks * price + otoks * oprice) / 1e6 * 1000
    cst = c13.cost(usd_per_1000)
    axes = {"intelligence": intel, "calibration": calib, "speed": spd, "cost": cst}
    out[n] = {"n": len(R), "correct": int(sum(r["correct"] for r in R.values())), "acc_by_tier": acc, "axes": axes,
              "p50_s": p50, "p95_s": p95, "ece_hard": ece, "usd_per_1000": usd_per_1000,
              "score_harmonic_v14": c14.harmonic(axes), "score_geometric_v13": c13.jevbench_score(axes)}
ref = a.runs[0]
rng = np.random.default_rng(0)
common = sorted(set.intersection(*[set(R) for R in runs.values()]))
for n in a.runs[1:]:
    d = np.array([float(runs[n][i]["correct"]) - float(runs[ref][i]["correct"]) for i in common])
    boots = [d[rng.integers(0, len(d), len(d))].mean() for _ in range(10000)]
    lo, hi = np.percentile(boots, [2.5, 97.5])
    out[n]["paired_vs_" + ref] = {"diff_items": float(d.sum()), "diff_pct": float(d.mean() * 100), "ci_pct": [lo * 100, hi * 100]}
print(f"JevBench v1.4.2 public items ({a.items}, n={len(common)}); axes are public-only (no judge/sealed tier)\n")
print(f"{'run':24s} {'correct':>9s} easy  std  hard | Intel Calib Speed  Cost | Score(v14) | p50/p95 ms | paired vs {ref}")
for n, o in out.items():
    ax = o["axes"]
    pv = o.get("paired_vs_" + ref)
    pvs = f"{pv['diff_pct']:+.1f} pp [{pv['ci_pct'][0]:+.1f}, {pv['ci_pct'][1]:+.1f}]" if pv else "-"
    print(f"{n:24s} {o['correct']:>4d}/{o['n']:<4d} {o['acc_by_tier']['easy'] * 100:4.0f} {o['acc_by_tier']['standard'] * 100:4.0f} "
          f"{o['acc_by_tier']['hard'] * 100:4.0f} | {ax['intelligence']:5.1f} {ax['calibration']:5.1f} {ax['speed']:5.1f} {ax['cost']:5.1f} | "
          f"{o['score_harmonic_v14']:9.2f} | {o['p50_s'] * 1000:4.0f}/{o['p95_s'] * 1000:4.0f} | {pvs}")
(HERE / "runs" / f"scores_{a.items}.json").write_text(json.dumps(out, indent=1, default=float))

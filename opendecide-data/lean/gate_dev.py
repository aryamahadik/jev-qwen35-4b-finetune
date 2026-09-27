"""Dev gate (PRISM_2B_MASTER_PLAN.md §6): compare a candidate with a reference on the dev-CONFIRM half (groups whose
sha256("devsel:" + group_id) is odd, the same split as modal_od.dev_half), pooled over the given dev splits.
Micro accuracy (ties and missing = wrong), yes/no Brier, and a paired bootstrap over groups (10,000, seed 0).
Also prints the dev-select half for information (selection decisions use select; the gate uses confirm).
  python gate_dev.py CANDIDATE REFERENCE [--splits a,b,c] [--need 1.3]
"""
import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument("cand")
ap.add_argument("ref")
ap.add_argument("--splits", default="dev_nc,taskbank_dev,hard_dev,dev_negwords,dev_claims,pg_dev,devzs,devp_card,dev")
ap.add_argument("--need", type=float, default=1.3, help="required micro gain in pp on dev-confirm")
a = ap.parse_args()
half = lambda g: "select" if int(hashlib.sha256(f"devsel:{g}".encode()).hexdigest(), 16) % 2 == 0 else "confirm"


def load(split, name):
    f = HERE / ("preds" if split == "eval" else f"preds_{split}") / f"{name}.jsonl"
    return {json.loads(l)["id"]: json.loads(l)["probs"] for l in open(f)} if f.exists() else None


def score(r, pr):
    if pr is None:
        return 0.0, None
    if r["qtype"] == "noul":
        keys, g = ["yes", "no"], ("yes" if r["gold"] == 1 else "no")
    else:
        keys, g = r["options"], r["gold"]
    p = {k: float(pr.get(k, 0.0)) for k in keys}
    best = max(p.values())
    ok = float([k for k, v in p.items() if v == best] == [g])
    br = (p["yes"] - r["gold"]) ** 2 if r["qtype"] == "noul" else None
    return ok, br


for part in ("select", "confirm"):
    groups = defaultdict(lambda: [0.0, 0.0, 0])  # (split, group) -> cand ok, ref ok, n
    brier = defaultdict(lambda: [0.0, 0.0, 0])
    per_split = {}
    for sp in a.splits.split(","):
        pc, pr_ = load(sp, a.cand), load(sp, a.ref)
        if pc is None or pr_ is None:
            per_split[sp] = "missing preds"
            continue
        rows = [json.loads(l) for l in open(HERE / f"data/{sp}.jsonl")]
        rows = [r for r in rows if half(r["group_id"]) == part]
        c = [score(r, pc.get(r["id"])) for r in rows]
        f = [score(r, pr_.get(r["id"])) for r in rows]
        for r, (oc, bc), (of, bf) in zip(rows, c, f):
            g = groups[(sp, r["group_id"])]
            g[0] += oc; g[1] += of; g[2] += 1
            if bc is not None:
                b = brier[(sp, r["group_id"])]
                b[0] += bc; b[1] += bf; b[2] += 1
        per_split[sp] = f"{100 * np.mean([x[0] for x in c]):.1f} vs {100 * np.mean([x[0] for x in f]):.1f} (n={len(rows)})"
    G = np.array(list(groups.values()))
    B = np.array(list(brier.values())) if brier else np.zeros((0, 3))
    diff = (G[:, 0].sum() - G[:, 1].sum()) / G[:, 2].sum() * 100
    rng = np.random.default_rng(0)
    boots = []
    for _ in range(10000):
        ix = rng.integers(0, len(G), len(G))
        s = G[ix]
        boots.append((s[:, 0].sum() - s[:, 1].sum()) / s[:, 2].sum() * 100)
    lo, hi = np.percentile(boots, [2.5, 97.5])
    bd = (B[:, 0].sum() - B[:, 1].sum()) / B[:, 2].sum() if len(B) else float("nan")
    print(f"== dev-{part}: n={int(G[:, 2].sum())} rows, {len(G)} groups")
    for sp, v in per_split.items():
        print(f"   {sp:14s} {v}")
    print(f"   micro {100 * G[:, 0].sum() / G[:, 2].sum():.2f} vs {100 * G[:, 1].sum() / G[:, 2].sum():.2f}: "
          f"diff {diff:+.2f} pp [{lo:+.2f}, {hi:+.2f}]   yes/no Brier diff {bd:+.4f} (n={int(B[:, 2].sum()) if len(B) else 0})")
    if part == "confirm":
        ok = diff >= a.need and lo > 0 and not (bd > 0.005)
        print(f"   GATE (diff >= {a.need} pp, lower bound > 0, Brier not worse by > 0.005): {'PASS' if ok else 'FAIL'}")

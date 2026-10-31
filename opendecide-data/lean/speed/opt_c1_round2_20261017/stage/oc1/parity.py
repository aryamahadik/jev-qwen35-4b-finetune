"""oc1.parity: the parity bar for every change to the serving path, and the near-tie analysis of the flips.

BAR (task rule): >= 99.5% same argmax vs the bf16 S1 baseline on the parity set; report max |dp| and the flips. A change
that fails the bar is reported, never adopted. Definitions are SPEED-2's (hosting/speed_bench.py compare):
  * answer = probabilities per row: yes/no rows {"yes", "no"}, choice rows {option: p} (2view average already applied);
  * argmax: yes/no -> p_yes > 0.5 (gate_dev.argmax_label), choice -> max over the row's options (first on a tie);
  * a missing answer counts as a disagreement (and, in speed_bench.compare, as wrong).
Pure Python (no torch): it runs on the laptop, in the container and in tests.
"""
from __future__ import annotations

import math
import random
import statistics

AGREE_MIN = 0.995
ACC_DIFF_MAX_PT = 0.3
ACC_DIFF_MAX_PT_FP8 = 1.0
NEAR_EDGES = (0.005, 0.01, 0.02, 0.05)


def item_options(item: dict):
    """Options of a workload item (choice) or None (yes/no)."""
    q = next(iter(item["request"]["questions"].values()))
    return q.get("options") if q["type"] == "choice" else None


def argmax_label(options, p: dict):
    if options is None:
        return float(p.get("yes", 0.0)) > 0.5
    vals = {o: float(p.get(o, 0.0)) for o in options}
    return max(vals, key=vals.get)


def margin(options, p: dict) -> float:
    """Top-1 minus top-2 probability (choice), or |2*p_yes - 1| (yes/no): how far from a tie the row is."""
    if options is None:
        return abs(2.0 * float(p.get("yes", 0.0)) - 1.0)
    v = sorted((float(p.get(o, 0.0)) for o in options), reverse=True)
    return v[0] - v[1] if len(v) > 1 else v[0]


def row_dp(options, a: dict, b: dict) -> float:
    keys = ["yes", "no"] if options is None else list(options)
    return max(abs(float(a.get(k, 0.0)) - float(b.get(k, 0.0))) for k in keys)


def wilson(k: int, n: int, z: float = 1.96) -> tuple:
    """95% Wilson interval of the proportion k/n."""
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (c - h, c + h)


def compare_items(items: list, cand: dict, ref: dict, agree_min: float = AGREE_MIN) -> dict:
    """items = workload items (id, qtype, n_options, bucket, request); cand/ref = {id: probs}. Rows missing in `ref`
    are skipped (a subsample run compares only the rows both have); rows missing in `cand` count as disagreements."""
    rows = [it for it in items if it["id"] in ref]
    n = len(rows)
    agree, dps, flips, miss = 0, [], [], 0
    by_bucket = {}
    for it in rows:
        opts = item_options(it)
        c, r = cand.get(it["id"]), ref[it["id"]]
        b = by_bucket.setdefault(it["bucket"], {"n": 0, "agree": 0, "dp_max": 0.0})
        b["n"] += 1
        if not c:
            miss += 1
            flips.append({"id": it["id"], "bucket": it["bucket"], "missing": True})
            continue
        dp = row_dp(opts, c, r)
        dps.append(dp)
        b["dp_max"] = max(b["dp_max"], dp)
        same = argmax_label(opts, c) == argmax_label(opts, r)
        agree += same
        b["agree"] += same
        if not same:
            flips.append({"id": it["id"], "bucket": it["bucket"], "dp": round(dp, 6),
                          "ref_margin": round(margin(opts, r), 6), "cand_margin": round(margin(opts, c), 6),
                          "ref_top": str(argmax_label(opts, r))[:40], "cand_top": str(argmax_label(opts, c))[:40]})
    k_dis = n - agree
    lo, hi = wilson(agree, n)
    real = [f for f in flips if not f.get("missing")]
    ties = {f"ref_margin<={e}": sum(1 for f in real if f["ref_margin"] <= e) for e in NEAR_EDGES}
    out = {"n": n, "agree": agree, "disagree": k_dis, "missing_cand": miss,
           "argmax_agree": round(agree / n, 6) if n else None,
           "agree_wilson95": [round(lo, 6), round(hi, 6)] if n else None,
           "dp_mean": round(statistics.fmean(dps), 6) if dps else None,
           "dp_p99": round(sorted(dps)[min(len(dps) - 1, int(0.99 * len(dps)))], 6) if dps else None,
           "dp_max": round(max(dps), 6) if dps else None,
           "flips": flips[:60], "n_flips": len(flips),
           "flip_margin_p50": round(statistics.median([f["ref_margin"] for f in real]), 6) if real else None,
           "flip_margin_max": round(max([f["ref_margin"] for f in real]), 6) if real else None,
           "flips_near_tie": ties,
           "by_bucket": {k: {"n": v["n"], "agree": round(v["agree"] / v["n"], 6), "dp_max": round(v["dp_max"], 6)}
                         for k, v in sorted(by_bucket.items())},
           "bar": {"argmax_agree_min": agree_min}}
    out["pass_point"] = bool(n and out["argmax_agree"] >= agree_min)
    out["pass_conservative"] = bool(n and lo >= agree_min)   # even the lower Wilson bound clears the bar
    return out


def verdict(rep: dict, acc_diff_pt: float | None = None, fp8: bool = False) -> str:
    """PASS / FAIL / UNDERPOWERED for a compare_items report (and the accuracy difference when known)."""
    if not rep.get("n"):
        return "INCOMPLETE"
    bar = ACC_DIFF_MAX_PT_FP8 if fp8 else ACC_DIFF_MAX_PT
    if acc_diff_pt is not None and abs(acc_diff_pt) > bar:
        return "FAIL"
    if not rep["pass_point"]:
        return "FAIL"
    return "PASS" if rep["pass_conservative"] or rep["n"] >= 8000 else "PASS_POINT_UNDERPOWERED"


def stratified_sample(items: list, n: int, seed: int = 0, key=lambda it: it["bucket"], min_per: int = 25) -> list:
    """About n items, proportional per bucket (>= min_per when the bucket has that many), deterministic by seed. All
    items when n >= len(items)."""
    if n >= len(items):
        return list(items)
    rng = random.Random(seed)
    groups = {}
    for it in items:
        groups.setdefault(key(it), []).append(it)
    out = []
    for g, v in sorted(groups.items()):
        take = max(min(min_per, len(v)), round(n * len(v) / len(items)))
        out += rng.sample(v, min(take, len(v)))
    rng.shuffle(out)
    return out   # may exceed n slightly (min_per for the small buckets)

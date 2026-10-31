"""JevBench v1.5 scoring formulas (METHOD-v1.5.md + the headline-A equal-types amendment), for public items.

The public repository ships the harness (unchanged since v1.4.2) and the method documents, but not the v1.5 scorer,
so the formulas here are written from the frozen method text. The aggregation, calibration combination, speed, cost
and composite parts are checked against every published row of the v1.5.4 leaderboard API (score_v154.py
--check-leaderboard). The per-item rules (Noul abstention band, per-item chance, Score nMAE) follow METHOD-v1.5 §3.1.

Item tiers: the v1.2 public files are easy.jsonl -> easy, original.jsonl -> standard, hard.jsonl -> hard. The judge
tier has no published items, so its weight is renormalised away (METHOD §3.2: "renormalised only when a tier has no
items"). There is no sealed half on public items, so Intelligence here is I_open only and no gap penalty applies.
"""
from __future__ import annotations

import json
import math
import random
from pathlib import Path

TIER_W = {"easy": 0.10, "standard": 0.20, "judge": 0.30, "hard": 0.40}
TYPE_W = {  # headline (A, B and C all use equal types since the 26 Sep amendment); "frozen" = METHOD-v1.5 §3.2 original
    "equal": {"choice": 1 / 3, "noul": 1 / 3, "score": 1 / 3},
    "frozen": {"choice": 0.50, "noul": 0.25, "score": 0.25},
}
TYPES = ("choice", "noul", "score")
TIERS = ("easy", "standard", "judge", "hard")
NOUL_NO, NOUL_YES = 0.20, 0.80  # P(yes) <= 0.20 is No, >= 0.80 is Yes, in between is an abstention (counted wrong)
SEALED_SHARE = 0.50
GAP_ALLOWANCE = 8.0
AXES = ("intelligence", "calibration", "speed", "cost")
OPTIONS = {  # axis weights I/C/S/$ and the Intelligence gate
    "A": ((0.25, 0.25, 0.25, 0.25), 50.0),
    "B": ((0.40, 0.20, 0.20, 0.20), 50.0),
    "C": ((0.25, 0.25, 0.25, 0.25), 60.0),
}
VIEWS = {  # sort presets (I, C, S, $); calibration is not part of these views
    "Balanced 33:33:33": (1 / 3, 0.0, 1 / 3, 1 / 3),
    "Emphasis on Accuracy 60:20:20": (0.6, 0.0, 0.2, 0.2),
    "Emphasis on Cost 20:20:60": (0.2, 0.0, 0.2, 0.6),
    "Emphasis on Speed 20:60:20": (0.2, 0.0, 0.6, 0.2),
    "Intelligence only": (1.0, 0.0, 0.0, 0.0),
}
LOAD_FACTOR, OWN_SERVER_ADD_S = 2.0, 0.15  # self-hosted / demo latency adjustment (unchanged from v1.3/v1.4)
PUBLIC_FILES = (("easy", "easy"), ("original", "standard"), ("hard", "hard"))
# Frozen 25 Sep price snapshot used by v1.5 for Qwen/Qwen3.5-4B (DeepInfra, interpretation I-3): $/M input, $/M output.
QWEN35_4B_REF = (0.03, 0.15)
JEV_LIST = (0.042, 0.0)  # Jev 1.13.0 launch list price (interpretation I-1)


# ---------------------------------------------------------------- items

def load_public(jb_dir, splits_file=None, extra=None):
    """{id: item dict + "tier"} for the public v1.2 files of a JevBench checkout (+ optional extra jsonl whose rows
    carry their own "tier"). splits_file: a jsonl whose ids restrict the set (e.g. bench/splits/jevbench_A.jsonl)."""
    items = {}
    for fn, tier in PUBLIC_FILES:
        for line in open(Path(jb_dir) / "datasets/public" / f"{fn}.jsonl", encoding="utf-8"):
            if line.strip():
                d = json.loads(line)
                d["tier"] = tier
                items[d["id"]] = d
    for path in extra or []:
        for line in open(path, encoding="utf-8"):
            if line.strip():
                d = json.loads(line)
                if d.get("tier") not in TIER_W:
                    raise ValueError(f"{path}: item {d.get('id')} needs a tier in {list(TIER_W)}")
                items[d["id"]] = d
    if splits_file:
        keep = {json.loads(l)["id"] for l in open(splits_file) if l.strip()}
        items = {k: v for k, v in items.items() if k in keep}
    return items


# ---------------------------------------------------------------- per item

def argmax_label(probs):
    """jevbench.scoring.argmax_label: ties go to the lexicographically smallest label."""
    best, best_p = None, -1.0
    for k in sorted(probs):
        if probs[k] > best_p:
            best, best_p = k, probs[k]
    return best


def item_outcome(item, rec):
    """Scores one results.jsonl record against its item with the v1.5 per-item rules."""
    qt = item["question"]["type"]
    probs = rec.get("probs") if rec and rec.get("valid") and rec.get("probs") else None
    out = {"type": qt, "tier": item["tier"], "valid": probs is not None,
           "latency_s": (rec or {}).get("latency_s"), "usage": (rec or {}).get("usage") or {}}
    if qt == "choice":
        pred = argmax_label(probs) if probs else None
        out.update(correct=pred == item["expected"], chance=1.0 / len(item["labels"]),
                   conf=max(probs.values()) if probs else 0.0, probs=probs)
        gp = (item.get("provenance") or {}).get("gold_probs")
        if gp and probs:
            out["tvd"] = 0.5 * sum(abs(probs.get(l, 0.0) - gp.get(l, 0.0)) for l in item["labels"])
    elif qt == "noul":
        p = probs.get("yes") if probs else None
        dec = None if p is None else ("yes" if p >= NOUL_YES else "no" if p <= NOUL_NO else None)
        y = 1.0 if item["expected"] == "yes" else 0.0
        out.update(correct=dec == item["expected"], p_yes=p, y=y, abstain=probs is not None and dec is None,
                   argmax_correct=probs is not None and argmax_label(probs) == item["expected"])  # v1.4 rule
    elif qt == "score":
        K = len(item["labels"])
        gold = int(item["expected"])
        levels = sorted(int(l) for l in item["labels"])
        chance = sum(abs(l - gold) for l in levels) / K / (K - 1)
        if probs:
            ev = sum(int(k) * v for k, v in probs.items())
            nmae = abs(ev - gold) / (K - 1)
            cdf, rps = 0.0, 0.0
            for l in levels[:-1]:
                cdf += probs.get(str(l), 0.0)
                rps += (cdf - (1.0 if l >= gold else 0.0)) ** 2
            out.update(ev=ev, nrps=rps / (K - 1), conf=max(probs.values()),
                       top_correct=argmax_label(probs) == str(gold))
        else:  # a failed or invalid answer: the worst position on this item's scale
            nmae = max(gold, K - 1 - gold) / (K - 1)
            out.update(ev=None, conf=0.0, top_correct=False)
        out.update(nmae=nmae, nmae_chance=chance, correct=out["top_correct"])
    return out


# ---------------------------------------------------------------- aggregation

def _mean(xs):
    xs = list(xs)
    return sum(xs) / len(xs) if xs else None


def cell_cc(qt, outs):
    """Chance-corrected competence of one type x tier cell (not clipped)."""
    if not outs:
        return None
    if qt == "choice":
        acc, cbar = _mean(o["correct"] for o in outs), _mean(o["chance"] for o in outs)
        return 100 * (acc - cbar) / (1 - cbar)
    if qt == "noul":
        return 100 * (_mean(o["correct"] for o in outs) - 0.5) / 0.5
    return 100 * (1 - _mean(o["nmae"] for o in outs) / _mean(o["nmae_chance"] for o in outs))


def wavg(vals, weights):
    """Weighted mean over the keys whose value is not None (renormalised weights)."""
    num = den = 0.0
    for k, v in vals.items():
        if v is not None and weights.get(k, 0) > 0:
            num += weights[k] * v
            den += weights[k]
    return num / den if den else None


def intelligence_open(outs, type_w="equal"):
    """outs: list of item_outcome dicts. Returns (I, {type: {"cc", "tiers": {tier: cc}, "n": {tier: n}}})."""
    detail = {}
    for qt in TYPES:
        tiers, ns = {}, {}
        for tier in TIERS:
            cell = [o for o in outs if o["type"] == qt and o["tier"] == tier]
            ns[tier] = len(cell)
            tiers[tier] = cell_cc(qt, cell)
        cc = wavg(tiers, TIER_W)
        if cc is not None:
            detail[qt] = {"cc": cc, "tiers": tiers, "n": ns}
    return wavg({t: d["cc"] for t, d in detail.items()}, TYPE_W[type_w]), detail


def ece_bins(pairs, n_bins=10):
    """10 equal-width bins; pairs = (predicted probability, outcome in {0,1} or bool)."""
    bins = [[0, 0.0, 0.0] for _ in range(n_bins)]
    for p, y in pairs:
        p = min(max(float(p), 0.0), 1.0)
        b = bins[min(int(p * n_bins), n_bins - 1)]
        b[0] += 1
        b[1] += p
        b[2] += float(y)
    n = sum(b[0] for b in bins)
    return sum(b[0] / n * abs(b[2] / b[0] - b[1] / b[0]) for b in bins if b[0]) if n else None


def ece_score(ece):
    return None if ece is None else max(0.0, 100 * (1 - ece / 0.5))


def calib_choice(ece_hard, mean_tvd):
    s = ece_score(ece_hard)
    return s if s is None or mean_tvd is None else (s + 100 * (1 - mean_tvd)) / 2


def calib_score(nrps, top_ece):
    return (100 * (1 - nrps) + ece_score(top_ece)) / 2


def calibration(outs, type_w="equal"):
    ch = [o for o in outs if o["type"] == "choice"]
    no = [o for o in outs if o["type"] == "noul"]
    sc = [o for o in outs if o["type"] == "score"]
    parts = {}
    if ch:
        hard = [(o["conf"], o["correct"]) for o in ch if o["tier"] == "hard"]
        tv = [o["tvd"] for o in ch if "tvd" in o]
        e = ece_bins(hard)
        parts["choice"] = {"ece_hard": e, "n_ece_hard": len(hard), "mean_tvd": _mean(tv), "n_tvd": len(tv),
                           "score": calib_choice(e, _mean(tv))}
    if no:
        pv = [(o["p_yes"], o["y"]) for o in no if o["p_yes"] is not None]
        e = ece_bins(pv)
        parts["noul"] = {"ece": e, "brier": _mean((p - y) ** 2 for p, y in pv), "n": len(no),
                         "abstention_rate": _mean(o["abstain"] for o in no), "score": ece_score(e)}
    if sc:
        ok = [o for o in sc if o["ev"] is not None]
        nrps, te = _mean(o["nrps"] for o in ok), ece_bins([(o["conf"], o["top_correct"]) for o in sc])
        parts["score"] = {"nrps": nrps, "top_ece": te, "n": len(sc),
                          "score": calib_score(nrps, te) if nrps is not None else 0.0}
    return wavg({t: p["score"] for t, p in parts.items()}, TYPE_W[type_w]), parts


def percentile(values, q):
    """jevbench.metrics.percentile (linear interpolation), the harness's latency summary."""
    v = sorted(values)
    if not v:
        return None
    k = (len(v) - 1) * q
    f, c = math.floor(k), math.ceil(k)
    return v[int(k)] if f == c else v[f] * (c - k) + v[c] * (k - f)


def adjusted_latency(s, kind):
    if kind == "api":
        return s
    return s * LOAD_FACTOR + (OWN_SERVER_ADD_S if kind in ("gpu", "cpu") else 0.0)


def speed_point(s):
    return max(0.0, min(100.0, 100 - 20 * math.log10(s / 0.1)))


def speed(p50, p95, kind):
    return (speed_point(adjusted_latency(p50, kind)) + speed_point(adjusted_latency(p95, kind))) / 2


def cost(usd_per_1000):
    return max(0.0, min(100.0, 100 - 30 * math.log10(usd_per_1000 / 0.001)))


def harmonic(axes, weights, i_gate=50.0):
    """Weighted power mean p = -1, then the quadratic gates: Intelligence below i_gate, Speed and Cost below 50."""
    sel = [(axes[a], w) for a, w in zip(AXES, weights) if w > 0]
    if any(v is None for v, _ in sel):
        return None
    s = 0.0 if any(v <= 0 for v, _ in sel) else sum(w for _, w in sel) / sum(w / v for v, w in sel)
    i = axes.get("intelligence")
    if i is not None and i < i_gate:
        s *= (max(0.0, i) / i_gate) ** 2
    for a in ("speed", "cost"):
        v = axes.get(a)
        if v is not None and v < 50:
            s *= (max(0.0, v) / 50) ** 2
    return s


def composites(axes):
    out = {k: harmonic(axes, w, g) for k, (w, g) in OPTIONS.items()}
    out.update({k: harmonic(axes, w) for k, w in VIEWS.items()})
    return out


def overfit_penalty(i_open, i_sealed, g_med):
    gap = i_open - i_sealed
    excess = gap - g_med
    return gap, excess, max(0.0, 1 - max(0.0, excess - GAP_ALLOWANCE) / 100)


# ---------------------------------------------------------------- bootstrap

def strata(outs):
    s = {}
    for i, o in enumerate(outs):
        s.setdefault((o["type"], o["tier"]), []).append(i)
    return s


def paired_bootstrap_intel(runs_outs, ref, B=2000, seed=15, type_w="equal"):
    """runs_outs: {name: [item_outcome in the SAME item order]}. Stratified (type x tier) paired bootstrap of the public
    Intelligence difference vs ref; the same resample for every run (METHOD-v1.5 §2). Returns {name: {...}}."""
    rng = random.Random(seed)
    st = strata(runs_outs[ref])
    diffs = {n: [] for n in runs_outs if n != ref}
    for _ in range(B):
        idx = [i for cell in st.values() for i in (rng.choice(cell) for _ in cell)]
        iref = intelligence_open([runs_outs[ref][i] for i in idx], type_w)[0]
        for n in diffs:
            diffs[n].append(intelligence_open([runs_outs[n][i] for i in idx], type_w)[0] - iref)
    out = {}
    for n, d in diffs.items():
        d.sort()
        out[n] = {"ci95": [d[int(0.025 * B)], d[int(0.975 * B) - 1]], "p_better": sum(x > 0 for x in d) / B}
    return out

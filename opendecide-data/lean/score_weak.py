"""Score the Jev-weakness slices: HC (high-cardinality choice) and LONG (long irrelevant state).

HC:   top-1 accuracy per option-set size (full label space / 500 / 2,000), 95% bootstrap CI over states,
      plus median / p95 latency per question (our GPU wall-clock; Jev's API wall-clock incl. its wrapper rounds).
LONG: choice and yes/no accuracy per filler length, next to the same questions on the clean state
      (clean predictions come from preds/<model>.jsonl on the frozen eval).
Usage: score_weak.py --hc MODEL ... --long MODEL ...   (names of preds_<split>/<name>.jsonl files)
"""
import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument("--hc", nargs="*", default=[])
ap.add_argument("--long", nargs="*", default=[])
ap.add_argument("--multi", nargs="*", default=[])
ap.add_argument("--hc_split", default="eval_hc")
ap.add_argument("--clean", nargs="*", default=None, help="clean-eval pred names matching --long (default: same names)")
a = ap.parse_args()


def rj(p):
    return [json.loads(l) for l in open(p)]


def boot_acc(units, B=1000, seed=0):
    """units: list of (group, correct)."""
    by = defaultdict(list)
    for g, c in units:
        by[g].append(c)
    gs = sorted(by)
    rng = np.random.default_rng(seed)
    point = float(np.mean([c for _, c in units])) if units else float("nan")
    vals = []
    for _ in range(B):
        s = [c for k in rng.integers(0, len(gs), len(gs)) for c in by[gs[k]]]
        vals.append(np.mean(s))
    lo, hi = np.percentile(vals, [2.5, 97.5]) if vals else (np.nan, np.nan)
    return point, lo, hi, len(units)


def top1(probs, options):
    pr = {o: probs.get(o, 0.0) for o in options}
    best = max(pr.values())
    tops = [o for o, v in pr.items() if v == best]
    return tops[0] if len(tops) == 1 else None


def pct(t):
    return f"{100 * t[0]:.1f} [{100 * t[1]:.1f}–{100 * t[2]:.1f}]"


md, out = [], {}
if a.hc:
    rows = {r["id"]: r for r in rj(HERE / f"data/{a.hc_split}.jsonl")}
    levels = ["full", "500", "2000"]
    md += [f"## High-cardinality choice ({a.hc_split})\n", "Top-1 accuracy, 95% bootstrap CI over states; latency per question (ms, median / p95).\n",
           "| Model | " + " | ".join(f"N={l}" for l in levels) + " | " + " | ".join(f"latency N={l}" for l in levels) + " |",
           "|---|" + "---|" * (2 * len(levels))]
    for n in a.hc:
        P = {p["id"]: p for p in rj(HERE / f"preds_{a.hc_split}/{n}.jsonl") if p.get("probs")}
        acc, lat = {}, {}
        for lev in levels:
            ids = [i for i, r in rows.items() if r["meta"]["level"] == lev]
            units = [(rows[i]["group_id"], (i in P) and top1(P[i]["probs"], rows[i]["options"]) == rows[i]["gold"]) for i in ids]
            acc[lev] = boot_acc(units)
            ls = [P[i]["latency_ms"] for i in ids if i in P and P[i].get("latency_ms")]
            lat[lev] = (float(np.median(ls)), float(np.percentile(ls, 95))) if ls else None
            out.setdefault("hc", {}).setdefault(n, {})[lev] = {"acc": acc[lev], "latency_ms": lat[lev],
                                                                "answered": sum(i in P for i in ids), "n": len(ids)}
        md.append(f"| {n} | " + " | ".join(pct(acc[l]) for l in levels) + " | " +
                  " | ".join(f"{lat[l][0]:.0f} / {lat[l][1]:.0f}" if lat[l] else "–" for l in levels) + " |")
    md.append("")

if a.long:
    rows = {r["id"]: r for r in rj(HERE / "data/eval_long.jsonl")}
    ev = {r["id"]: r for r in rj(HERE / "data/eval.jsonl")}
    md += ["## Long irrelevant state (eval_long)\n", "Accuracy on the same questions: clean state vs the message buried in ~1,500 / ~4,500 words.\n",
           "| Model | Choice clean | Choice 1.5k | Choice 4.5k | Yes/no clean | Yes/no 1.5k | Yes/no 4.5k |", "|---|---|---|---|---|---|---|"]
    clean_names = a.clean or a.long
    for n, cn in zip(a.long, clean_names):
        P = {p["id"]: p for p in rj(HERE / f"preds_eval_long/{n}.jsonl")}
        C = {p["id"]: p for p in rj(HERE / f"preds/{cn}.jsonl")}

        def ok(r, p):
            if p is None:
                return False
            if r["qtype"] == "noul":
                y = p["probs"]["yes"]
                return (y > 0.5) == (r["gold"] == 1) and y != 0.5
            return top1(p["probs"], r["options"]) == r["gold"]

        cells = []
        for qt in ("choice", "noul"):
            ids = [i for i, r in rows.items() if r["qtype"] == qt]
            clean_ids = sorted({rows[i]["meta"]["clean_id"] for i in ids})
            cells.append(boot_acc([(ev[c]["group_id"], ok(ev[c], C.get(c))) for c in clean_ids]))
            for L in (1500, 4500):
                li = [i for i in ids if rows[i]["meta"]["length_words"] == L]
                cells.append(boot_acc([(rows[i]["group_id"], ok(rows[i], P.get(i))) for i in li]))
        out.setdefault("long", {})[n] = cells
        md.append(f"| {n} | " + " | ".join(pct(c) for c in cells) + " |")
    md.append("")

if a.multi:
    rows = {r["id"]: r for r in rj(HERE / "data/eval_multi.jsonl")}
    md += ["## Several records in one state (eval_multi)\n",
           "3-6 support tickets in the state; the question names one ticket. Accuracy, 95% bootstrap CI over states.\n",
           "| Model | Choice | Yes/no (all) | Yes/no about a distractor ticket's label |", "|---|---|---|---|"]
    for n in a.multi:
        P = {p["id"]: p for p in rj(HERE / f"preds_eval_multi/{n}.jsonl")}

        def ok(r, p):
            if p is None:
                return False
            if r["qtype"] == "noul":
                y = p["probs"]["yes"]
                return (y > 0.5) == (r["gold"] == 1) and y != 0.5
            return top1(p["probs"], r["options"]) == r["gold"]

        cells = [boot_acc([(r["group_id"], ok(r, P.get(i))) for i, r in rows.items() if f(r)]) for f in (
            lambda r: r["qtype"] == "choice", lambda r: r["qtype"] == "noul",
            lambda r: r["qtype"] == "noul" and r["meta"]["asks_about_distractor"])]
        out.setdefault("multi", {})[n] = cells
        md.append(f"| {n} | " + " | ".join(pct(c) for c in cells) + " |")
    md.append("")

od = HERE / "results_weak"
od.mkdir(exist_ok=True)
(od / "results_weak.json").write_text(json.dumps(out, indent=2, default=float))
(od / "RESULTS_WEAK.md").write_text("\n".join(md) + "\n")
print("\n".join(md))

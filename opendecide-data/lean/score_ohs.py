"""Score OHS-1 core exactly as pre-registered in PREREG_OHS.md (commit 273e76b).
Primary (Holm, family of 3), model vs Jev (per-item mean of the Jev runs): micro accuracy on base rows, macro accuracy
over tasks, Brier on yes/no base rows. Secondary: per-track accuracy, >26-option accuracy, consistency on the variant
layer (complement violation, double-negation drift, paraphrase drift, flip rate). Paired cluster bootstrap over group_id,
stratified by task, 10,000 resamples, seed 0. Ties and missing answers count as wrong.
  python score_ohs.py MODEL [MODEL ...] --jev jev_guard,jev_r2_guard [--half S|A|all]
"""
import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument("models", nargs="+")
ap.add_argument("--jev", default="jev_guard,jev_r2_guard")
ap.add_argument("--half", default="all")
ap.add_argument("--boot", type=int, default=10000)
a = ap.parse_args()

rows = {json.loads(l)["id"]: json.loads(l) for l in open(HERE / "data/ohs.jsonl")}
rels = [json.loads(l) for l in open(HERE / "data/ohs_relations.jsonl")]
if a.half != "all":
    rows = {i: r for i, r in rows.items() if r["meta"]["half"] == a.half}
base = [i for i, r in rows.items() if r["role"] in ("aff", "choice") and not any(i.endswith(s) for s in ("_neg", "_dneg", "_para", "_yn"))]
jevs = [x for x in a.jev.split(",") if (HERE / f"preds_ohs/{x}.jsonl").exists()]
names = a.models + jevs
P = {n: {json.loads(l)["id"]: json.loads(l)["probs"] for l in open(HERE / f"preds_ohs/{n}.jsonl")} for n in names}


def probs(n, i):
    r, pr = rows[i], P[n].get(i)
    if pr is None:
        return None
    keys = ["yes", "no"] if r["qtype"] == "noul" else r["options"]
    return {k: float(pr.get(k, 0.0)) for k in keys}


def correct(n, i):
    pr = probs(n, i)
    if pr is None:
        return 0.0
    r = rows[i]
    g = ("yes" if r["gold"] == 1 else "no") if r["qtype"] == "noul" else r["gold"]
    best = max(pr.values())
    return float([k for k, v in pr.items() if v == best] == [g])


def p_yes(n, i):
    pr = probs(n, i)
    return None if pr is None else pr["yes"]


def item_acc(n, i):
    return float(np.mean([correct(j, i) for j in jevs])) if n == "JEV" else correct(n, i)


def brier(n, i):
    r = rows[i]
    if n == "JEV":
        vals = [brier(j, i) for j in jevs]
        return float(np.mean(vals))
    p = p_yes(n, i)
    return 1.0 if p is None else (p - r["gold"]) ** 2


task = lambda i: rows[i]["source"]
groups = defaultdict(list)
for i in base:
    groups[(task(i), rows[i]["group_id"])].append(i)
by_task = defaultdict(list)
for k in groups:
    by_task[k[0]].append(k)
noul_base = [i for i in base if rows[i]["qtype"] == "noul"]


def micro(n, ids):
    return float(np.mean([item_acc(n, i) for i in ids])) if ids else float("nan")


def macro(n, ids):
    t = defaultdict(list)
    for i in ids:
        t[task(i)].append(item_acc(n, i))
    return float(np.mean([np.mean(v) for v in t.values()]))


def boot_diff(n, stat):
    """Paired cluster bootstrap of stat(n) - stat(JEV), resampling groups within each task (vectorised with group sums).
    stat is micro, macro or brier_stat; only the statistic's definition is used to pick the per-item quantity."""
    rng = np.random.default_rng(0)
    tasks = sorted(by_task)
    if stat is brier_stat:
        keys = [k for k in groups if rows[groups[k][0]]["qtype"] == "noul"]
        val = lambda m, i: brier(m, i)
    else:
        keys = list(groups)
        val = lambda m, i: item_acc(m, i)
    kidx = {k: j for j, k in enumerate(keys)}
    s_m = np.array([sum(val(n, i) for i in groups[k]) for k in keys])
    s_j = np.array([sum(val("JEV", i) for i in groups[k]) for k in keys])
    cnt = np.array([len(groups[k]) for k in keys], dtype=float)
    per_task = [np.array([kidx[k] for k in by_task[t] if k in kidx]) for t in tasks]
    per_task = [a_ for a_ in per_task if len(a_)]

    def value(sm, sj, idx_list, macro_):
        if macro_:
            return float(np.mean([sm[ix].sum() / cnt[ix].sum() for ix in idx_list]) - np.mean([sj[ix].sum() / cnt[ix].sum() for ix in idx_list]))
        allix = np.concatenate(idx_list)
        return float(sm[allix].sum() / cnt[allix].sum() - sj[allix].sum() / cnt[allix].sum())

    is_macro = stat is macro
    obs = value(s_m, s_j, per_task, is_macro)
    res = np.empty(a.boot)
    for b in range(a.boot):
        draw = [ix[rng.integers(0, len(ix), len(ix))] for ix in per_task]
        res[b] = value(s_m, s_j, draw, is_macro)
    p = 2 * min((res <= 0).mean(), (res >= 0).mean())
    return obs, np.percentile(res, [2.5, 97.5]), min(1.0, p)


def brier_stat(n, ids):
    ids = [i for i in ids if rows[i]["qtype"] == "noul"]
    return float(np.mean([brier(n, i) for i in ids])) if ids else float("nan")


def consistency(n):
    comp, dneg, para, flips = [], [], [], []
    for x in rels:
        a_, b_ = x["a"], x["b"]
        if a_ not in rows or b_ not in rows:
            continue
        pa, pb = p_yes(n, a_), p_yes(n, b_)
        if pa is None or pb is None:
            continue
        if x["type"] == "complement":
            comp.append(abs(pa + pb - 1))
        elif b_.endswith("_dneg"):
            dneg.append(abs(pa - pb))
        else:
            para.append(abs(pa - pb))
            flips.append(float((pa > 0.5) != (pb > 0.5)))
    m = lambda v: round(float(np.mean(v)), 4) if v else None
    return {"complement_violation": m(comp), "double_negation_drift": m(dneg), "paraphrase_drift": m(para), "paraphrase_flip_rate": m(flips)}


out = {"n_base": len(base), "n_groups": len(groups), "tasks": len(by_task), "jev_runs": jevs, "half": a.half, "models": {}}
if len(jevs) == 2:
    agree = np.mean([correct(jevs[0], i) == correct(jevs[1], i) for i in base])
    out["jev_run_agreement"] = round(float(agree), 4)
    out["jev_runs_micro"] = [round(micro(j, base) * 100, 2) for j in jevs]
wide = [i for i in base if len(rows[i]["options"] or []) > 26]
for n in a.models + (["JEV"] if jevs else []):
    m = {"micro": round(micro(n, base) * 100, 2), "macro": round(macro(n, base) * 100, 2),
         "brier_yesno": round(brier_stat(n, base), 4),
         "tracks": {t: round(micro(n, [i for i in base if rows[i]["track"] == t]) * 100, 2) for t in sorted({rows[i]["track"] for i in base})},
         "over_26_options": round(micro(n, wide) * 100, 2) if wide else None,
         "per_task": {t: round(micro(n, [i for i in base if task(i) == t]) * 100, 1) for t in sorted(by_task)}}
    if n != "JEV":
        m["consistency"] = consistency(n)
        if jevs:
            tests = {"micro": boot_diff(n, micro), "macro": boot_diff(n, macro), "brier_yesno": boot_diff(n, brier_stat)}
            order = sorted(tests, key=lambda k: tests[k][2])  # Holm over the 3 primary endpoints
            holm = {}
            for rank, k in enumerate(order):
                holm[k] = min(1.0, max([tests[kk][2] * (3 - r) for r, kk in enumerate(order[:rank + 1])]))
            m["vs_jev"] = {k: {"diff": round(v[0] * (100 if k != "brier_yesno" else 1), 3),
                               "ci95": [round(x * (100 if k != "brier_yesno" else 1), 3) for x in v[1]],
                               "p": round(v[2], 4), "p_holm": round(holm[k], 4)} for k, v in tests.items()}
    else:
        m["consistency"] = {j: consistency(j) for j in jevs}
    out["models"][n] = m
(HERE / "results_ohs").mkdir(exist_ok=True)
(HERE / f"results_ohs/results_{a.half}.json").write_text(json.dumps(out, indent=1))
print(json.dumps({k: v for k, v in out.items() if k != "models"}, indent=1))
print(f"{'model':22s} {'micro':>6s} {'macro':>6s} {'brier':>6s}  tracks                        >26   vs Jev micro [CI] p_holm")
for n, m in out["models"].items():
    vj = m.get("vs_jev", {}).get("micro")
    vs = f"{vj['diff']:+.1f} [{vj['ci95'][0]:+.1f},{vj['ci95'][1]:+.1f}] {vj['p_holm']:.3f}" if vj else ""
    print(f"{n:22s} {m['micro']:6.1f} {m['macro']:6.1f} {m['brier_yesno']:6.3f}  {json.dumps(m['tracks']):30s} {m['over_26_options']}  {vs}")

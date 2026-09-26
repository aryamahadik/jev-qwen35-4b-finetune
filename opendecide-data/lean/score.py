"""Score every model in lean/preds/ on the same rows and write results/RESULTS.md + results.json.

All models are scored on the intersection of rows they all answered (Jev may miss failed calls).
CIs: 95% percentile bootstrap over groups (1,000 resamples, seed 0), same resamples for every model.
"""
import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument("--models", nargs="*", default=None)
ap.add_argument("--split", default="eval")
ap.add_argument("--ref", default=None, help="reference model for paired-difference CIs (e.g. jev)")
a = ap.parse_args()
IS_EVAL = a.split in ("eval", "eval_card")  # eval_card = the frozen eval with compiled task cards (same rows/ids)

PD = "preds" if a.split == "eval" else f"preds_{a.split}"
rows = {json.loads(l)["id"]: json.loads(l) for l in open(HERE / f"data/{a.split}.jsonl")}
rels = [json.loads(l) for l in open(HERE / f"data/{a.split}_relations.jsonl")]
names = a.models or sorted(p.stem for p in (HERE / PD).glob("*.jsonl") if p.stem != "jev_raw")
P = {}
for n in names:
    P[n] = {json.loads(l)["id"]: json.loads(l) for l in open(HERE / f"{PD}/{n}.jsonl")}
common = set(rows)
for n in names:
    common &= set(P[n])
R = {i: rows[i] for i in common}


def p_yes(n, i):
    return P[n][i]["probs"]["yes"]


def choice_probs(n, i):
    pr = P[n][i]["probs"]
    return {o: pr.get(o, 0.0) for o in R[i]["options"]}


def argmax_choice(n, i):
    pr = choice_probs(n, i)
    best = max(pr.values())
    tops = [o for o, v in pr.items() if v == best]
    return tops[0] if len(tops) == 1 else None  # ties count as wrong


def correct(n, i):
    r = R[i]
    if r["qtype"] == "noul":
        p = p_yes(n, i)
        return (p > 0.5) == (r["gold"] == 1) and p != 0.5
    return argmax_choice(n, i) == r["gold"]


groups = sorted({r["group_id"] for r in R.values()})
rng = np.random.default_rng(0)
BOOT = [rng.choice(len(groups), len(groups), replace=True) for _ in range(1000)]


def boot(fn, units):
    """units: list of (group_id, value-tuple); fn: list of values -> float."""
    by = defaultdict(list)
    for g, v in units:
        by[g].append(v)
    point = fn([v for _, v in units])
    vals = []
    for idx in BOOT:
        s = []
        for k in idx:
            s.extend(by.get(groups[k], []))
        if s:
            vals.append(fn(s))
    lo, hi = np.percentile(vals, [2.5, 97.5]) if vals else (np.nan, np.nan)
    return {"v": point, "lo": lo, "hi": hi, "n": len(units)}


mean = lambda xs: float(np.mean(xs)) if xs else float("nan")


def ece(conf, corr, bins=10):
    conf, corr = np.array(conf), np.array(corr, float)
    e = 0.0
    for b in range(bins):
        lo, hi = b / bins, (b + 1) / bins
        m = (conf >= lo) & ((conf < hi) if b < bins - 1 else (conf <= hi))
        if m.any():
            e += m.mean() * abs(conf[m].mean() - corr[m].mean())
    return float(e)


def coverage_at(conf, corr, eps=0.01):
    """Largest accepted set (confidence >= t, ties together) with empirical error <= eps; returns coverage."""
    conf, corr = np.array(conf), np.array(corr, bool)
    best = 0.0
    for t in np.unique(conf)[::-1]:
        m = conf >= t
        if (1 - corr[m].mean()) <= eps:
            best = max(best, m.mean())
    return float(best)


def coverage_crossfit(items, n, eps=0.01):
    """2-fold by group hash: threshold picked on one fold, applied to the other; averaged."""
    def fold(g):
        return int(hashlib.sha1(g.encode()).hexdigest(), 16) % 2
    out = []
    for f in (0, 1):
        A = [i for i in items if fold(R[i]["group_id"]) == f]
        B = [i for i in items if fold(R[i]["group_id"]) != f]
        confA = np.array([max(p_yes(n, i), 1 - p_yes(n, i)) for i in A])
        corrA = np.array([correct(n, i) for i in A])
        thr = None
        for t in np.unique(confA)[::-1]:
            m = confA >= t
            if (1 - corrA[m].mean()) <= eps:
                thr = t
        if thr is None:
            out.append((0.0, float("nan")))
            continue
        confB = np.array([max(p_yes(n, i), 1 - p_yes(n, i)) for i in B])
        corrB = np.array([correct(n, i) for i in B])
        m = confB >= thr
        out.append((m.mean(), 1 - corrB[m].mean() if m.any() else float("nan")))
    return float(np.mean([o[0] for o in out])), float(np.nanmean([o[1] for o in out]))


def ids(track=None, qtype=None, roles=None, source=None):
    return [i for i, r in R.items() if (track is None or r["track"] in track) and (qtype is None or r["qtype"] == qtype)
            and (roles is None or r["role"] in roles) and (source is None or r["source"] == source)]


res = {}
for n in names:
    M = {}
    for tr in (("ID", "ZS") if IS_EVAL else ("DEV",)):
        ci = ids((tr,), "choice")
        M[f"choice_acc_{tr}"] = boot(mean, [(R[i]["group_id"], correct(n, i)) for i in ci])
        M[f"noul_base_acc_{tr}"] = boot(mean, [(R[i]["group_id"], correct(n, i)) for i in ids((tr,), "noul", ("aff",))])
        M[f"noul_neg_acc_{tr}"] = boot(mean, [(R[i]["group_id"], correct(n, i)) for i in ids((tr,), "noul", ("neg",))])
        M[f"noul_all_acc_{tr}"] = boot(mean, [(R[i]["group_id"], correct(n, i)) for i in ids((tr,), "noul")])
    for src in ("banking77", "clinc150", "sms_spam", "tfns"):
        M[f"choice_acc_{src}"] = mean([correct(n, i) for i in ids(("ID", "ZS"), "choice", source=src)])
    CORE = ("ID", "ZS") if IS_EVAL else ("DEV",)
    core_noul = ids(CORE, "noul")
    ys = [R[i]["gold"] for i in core_noul]
    ps = [p_yes(n, i) for i in core_noul]
    M["brier_noul_core"] = boot(lambda v: mean([(p - y) ** 2 for p, y in v]), [(R[i]["group_id"], (p_yes(n, i), R[i]["gold"])) for i in core_noul])
    M["nll_noul_core"] = mean([-np.log(max(p if y else 1 - p, 1e-12)) for p, y in zip(ps, ys)])
    M["ece_noul_core"] = ece([max(p, 1 - p) for p in ps], [correct(n, i) for i in core_noul])
    M["coverage@1%_sameslice"] = coverage_at([max(p, 1 - p) for p in ps], [correct(n, i) for i in core_noul])
    cov, risk = coverage_crossfit(core_noul, n)
    M["coverage@1%_crossfit"], M["coverage@1%_crossfit_realised_risk"] = cov, risk
    for eps in (0.02, 0.03, 0.05):
        cov, risk = coverage_crossfit(core_noul, n, eps)
        M[f"coverage@{int(eps * 100)}%_crossfit"], M[f"coverage@{int(eps * 100)}%_crossfit_realised_risk"] = cov, risk
    for w, pre in (("w0_someone_mistaken", "Would someone who says"), ("w1_reader_misreading", "Would a reader who concluded")):
        for tr in CORE:
            M[f"noul_neg_acc_{tr}_{w}"] = mean([correct(n, i) for i in ids((tr,), "noul", ("neg",)) if R[i]["instructions"].startswith(pre)])
    # consistency
    for typ, role, key in (("complement", "neg", "complement"), ("equiv", "para", "paraphrase"), ("equiv", "dneg", "double_negation")):
        pairs = [x for x in rels if x["type"] == typ and x["a"] in R and x["b"] in R and R[x["b"]]["role"] == role]
        units = []
        for x in pairs:
            pa, pb = p_yes(n, x["a"]), p_yes(n, x["b"])
            units.append((R[x["a"]]["group_id"], (pa, pb, correct(n, x["a"]), correct(n, x["b"]))))
        if typ == "complement":
            M["complement_violation"] = boot(lambda v: mean([abs(pa + pb - 1) for pa, pb, _, _ in v]), units)
            M["complement_contradiction_rate"] = mean([(pa > .5) == (pb > .5) for _, (pa, pb, _, _) in units])
            M["complement_within_0.05"] = mean([abs(pa + pb - 1) <= 0.05 for _, (pa, pb, _, _) in units])
            M["complement_mean_sum"] = mean([pa + pb for _, (pa, pb, _, _) in units])
            M["complement_min_max_sum"] = (min(pa + pb for _, (pa, pb, _, _) in units), max(pa + pb for _, (pa, pb, _, _) in units)) if units else None
            M["complement_both_correct"] = mean([ca and cb for _, (_, _, ca, cb) in units])
        else:
            M[f"{key}_drift"] = boot(lambda v: mean([abs(pa - pb) for pa, pb, _, _ in v]), units)
            M[f"{key}_flip_rate"] = mean([(pa > .5) != (pb > .5) for _, (pa, pb, _, _) in units])
    # injection
    inj = ids(("INJ",))
    for arm in ("C", "D", "E"):
        ch = [i for i in inj if R[i]["qtype"] == "choice" and R[i]["meta"]["arm"] == arm]
        no = [i for i in inj if R[i]["qtype"] == "noul" and R[i]["meta"]["arm"] == arm]
        M[f"inj_{arm}_choice_acc"] = mean([correct(n, i) for i in ch])
        M[f"inj_{arm}_clean_choice_acc"] = mean([correct(n, R[i]["meta"]["clean_id"]) for i in ch if R[i]["meta"]["clean_id"] in R])
        if arm in ("C", "D"):
            M[f"inj_{arm}_ASR"] = mean([argmax_choice(n, i) == R[i]["meta"]["attack_target"] for i in ch])
            M[f"inj_{arm}_noul_false_yes"] = mean([p_yes(n, i) > 0.5 for i in no])
            M[f"inj_{arm}_noul_dp_target"] = mean([p_yes(n, i) - p_yes(n, R[i]["meta"]["clean_id"]) for i in no if R[i]["meta"]["clean_id"] in R])
        else:
            M["inj_E_echo_noul_acc"] = mean([correct(n, i) for i in no])
    cd = [i for i in inj if R[i]["qtype"] == "choice" and R[i]["meta"]["arm"] in ("C", "D")]
    M["inj_ASR_pooled"] = boot(mean, [(R[i]["group_id"], argmax_choice(n, i) == R[i]["meta"]["attack_target"]) for i in cd])
    # distractor
    di = ids(("DIST",))
    dch = [i for i in di if R[i]["qtype"] == "choice"]
    dno = [i for i in di if R[i]["qtype"] == "noul"]
    M["dist_choice_acc"] = mean([correct(n, i) for i in dch])
    M["dist_clean_choice_acc"] = mean([correct(n, R[i]["meta"]["clean_id"]) for i in dch if R[i]["meta"]["clean_id"] in R])
    M["dist_noul_acc"] = mean([correct(n, i) for i in dno])
    M["dist_clean_noul_acc"] = mean([correct(n, R[i]["meta"]["clean_id"]) for i in dno if R[i]["meta"]["clean_id"] in R])
    M["dist_noul_abs_dp"] = mean([abs(p_yes(n, i) - p_yes(n, R[i]["meta"]["clean_id"])) for i in dno if R[i]["meta"]["clean_id"] in R])
    # latency
    meta_p = HERE / f"{PD}/{n}.meta.json"
    if meta_p.exists():
        meta = json.loads(meta_p.read_text())
        M["latency"] = {k: meta[k] for k in meta if k.startswith("latency")}
    lat = [v.get("latency_ms") for v in P[n].values() if v.get("latency_ms")]
    if lat:
        per_call = sorted(set(lat))
        M["latency"] = {"api_per_call_median_ms": float(np.median(per_call)), "api_per_call_p95_ms": float(np.percentile(per_call, 95))}
    res[n] = M

# ---------------- paired differences vs a reference model (same bootstrap resamples) ----------------
def unit_values(n):
    """metric -> list of (group, value) per item/pair, for metrics whose statistic is a mean."""
    U = {}
    for tr in (("ID", "ZS") if IS_EVAL else ("DEV",)):
        U[f"choice_acc_{tr}"] = [(R[i]["group_id"], float(correct(n, i))) for i in ids((tr,), "choice")]
        U[f"noul_base_acc_{tr}"] = [(R[i]["group_id"], float(correct(n, i))) for i in ids((tr,), "noul", ("aff",))]
        U[f"noul_neg_acc_{tr}"] = [(R[i]["group_id"], float(correct(n, i))) for i in ids((tr,), "noul", ("neg",))]
    CORE_ = ("ID", "ZS") if IS_EVAL else ("DEV",)
    U["brier_noul_core"] = [(R[i]["group_id"], (p_yes(n, i) - R[i]["gold"]) ** 2) for i in ids(CORE_, "noul")]
    comp = [x for x in rels if x["type"] == "complement" and x["a"] in R and x["b"] in R and R[x["b"]]["role"] == "neg"]
    U["complement_violation"] = [(R[x["a"]]["group_id"], abs(p_yes(n, x["a"]) + p_yes(n, x["b"]) - 1)) for x in comp]
    dn = [x for x in rels if x["type"] == "equiv" and x["a"] in R and x["b"] in R and R[x["b"]]["role"] == "dneg"]
    U["double_negation_drift"] = [(R[x["a"]]["group_id"], abs(p_yes(n, x["a"]) - p_yes(n, x["b"]))) for x in dn]
    if IS_EVAL:
        cd = [i for i in ids(("INJ",)) if R[i]["qtype"] == "choice" and R[i]["meta"]["arm"] in ("C", "D")]
        U["inj_ASR_pooled"] = [(R[i]["group_id"], float(argmax_choice(n, i) == R[i]["meta"]["attack_target"])) for i in cd]
        U["dist_choice_acc"] = [(R[i]["group_id"], float(correct(n, i))) for i in ids(("DIST",)) if R[i]["qtype"] == "choice"]
    return U


if a.ref and a.ref in names:
    Uref = unit_values(a.ref)
    for n in names:
        if n == a.ref:
            continue
        Un, D = unit_values(n), {}
        for k in Uref:
            by = defaultdict(list)
            for (g, vr), (_, vn) in zip(Uref[k], Un[k]):
                by[g].append(vn - vr)
            point = mean([d for v in by.values() for d in v])
            vals = []
            for idx in BOOT:
                sm = [d for kk in idx for d in by.get(groups[kk], [])]
                if sm:
                    vals.append(np.mean(sm))
            lo, hi = np.percentile(vals, [2.5, 97.5])
            D[k] = {"diff": point, "lo": lo, "hi": hi, "significant": bool(lo > 0 or hi < 0)}
        res[n][f"paired_vs_{a.ref}"] = D

out = HERE / ("results" if a.split == "eval" else f"results_{a.split}")
out.mkdir(exist_ok=True)
(out / "results.json").write_text(json.dumps({"n_rows_scored": len(R), "n_groups": len(groups), "models": res}, indent=2, default=float))


def fmt(v, pct=True):
    if isinstance(v, dict) and "v" in v:
        f = (lambda x: f"{100 * x:.1f}") if pct else (lambda x: f"{x:.3f}")
        return f"{f(v['v'])} [{f(v['lo'])}–{f(v['hi'])}]"
    if isinstance(v, float):
        return f"{100 * v:.1f}" if pct else f"{v:.3f}"
    return str(v)


ROWS = [("Choice accuracy, in-domain (%)", "choice_acc_ID", True), ("Choice accuracy, zero-shot (%)", "choice_acc_ZS", True),
        ("Yes/no accuracy, base question, ID (%)", "noul_base_acc_ID", True), ("Yes/no accuracy, base question, ZS (%)", "noul_base_acc_ZS", True),
        ("Yes/no accuracy, negated question, ID (%)", "noul_neg_acc_ID", True), ("Yes/no accuracy, negated question, ZS (%)", "noul_neg_acc_ZS", True),
        ("Complement violation |P(A)+P(not A)−1| ↓", "complement_violation", False), ("Contradiction rate ↓ (%)", "complement_contradiction_rate", True),
        ("Pairs summing to 1±0.05 ↑ (%)", "complement_within_0.05", True), ("Paraphrase drift |ΔP| ↓", "paraphrase_drift", False),
        ("Paraphrase flip rate ↓ (%)", "paraphrase_flip_rate", True), ("Double-negation drift ↓", "double_negation_drift", False),
        ("Brier (yes/no, core) ↓", "brier_noul_core", False), ("ECE (yes/no, core) ↓", "ece_noul_core", False),
        ("Coverage @1% error, cross-fitted ↑ (%)", "coverage@1%_crossfit", True),
        ("Injection attack success, held-out C+D ↓ (%)", "inj_ASR_pooled", True), ("Choice acc under injection C (%)", "inj_C_choice_acc", True),
        ("Choice acc under injection D (%)", "inj_D_choice_acc", True), ("Choice acc, same items clean (%)", "inj_C_clean_choice_acc", True),
        ("Echo control choice acc (%)", "inj_E_choice_acc", True), ("Distractor choice acc (%)", "dist_choice_acc", True),
        ("Distractor, same items clean (%)", "dist_clean_choice_acc", True)]
if not IS_EVAL:
    ROWS = [(l.replace(", in-domain", "").replace(", ID", ""), k.replace("_ID", "_DEV"), pc) for l, k, pc in ROWS if not k.endswith("_ZS")]
md = [f"# OpenDecide lean benchmark v0.1 — first results\n", f"Rows scored (all models, same rows): **{len(R)}** in **{len(groups)}** groups. "
      "Brackets = 95% bootstrap CI over groups.\n", "| Metric | " + " | ".join(names) + " |", "|---|" + "---|" * len(names)]
for label, key, pct in ROWS:
    md.append(f"| {label} | " + " | ".join(fmt(res[n].get(key, float('nan')), pct) for n in names) + " |")
extra = [("Neg. acc ID, wording 0 'someone who says … mistaken' (near train wordings) (%)", "noul_neg_acc_ID_w0_someone_mistaken", True),
         ("Neg. acc ID, wording 1 'reader who concluded … misreading' (truly unseen) (%)", "noul_neg_acc_ID_w1_reader_misreading", True),
         ("Coverage @2% error, cross-fitted ↑ (%)", "coverage@2%_crossfit", True), ("Coverage @3% error, cross-fitted ↑ (%)", "coverage@3%_crossfit", True),
         ("Coverage @5% error, cross-fitted ↑ (%)", "coverage@5%_crossfit", True)] if IS_EVAL else []
for label, key, pct in extra:
    md.append(f"| {label} | " + " | ".join(fmt(res[n].get(key, float('nan')), pct) for n in names) + " |")
if a.ref and a.ref in names:
    md.append(f"\n**Paired differences vs {a.ref}** (model − {a.ref}, 95% bootstrap CI over the same groups; * = CI excludes 0)\n")
    keys = list(next(v[f"paired_vs_{a.ref}"] for k, v in res.items() if k != a.ref).keys())
    md.append("| Metric | " + " | ".join(n for n in names if n != a.ref) + " |")
    md.append("|---|" + "---|" * (len(names) - 1))
    for k in keys:
        cells = []
        for n in names:
            if n == a.ref:
                continue
            d = res[n][f"paired_vs_{a.ref}"][k]
            sc = 100 if not any(t in k for t in ("brier", "violation", "drift")) else 1
            f = (lambda x: f"{x * sc:+.1f}") if sc == 100 else (lambda x: f"{x:+.3f}")
            cells.append(f"{f(d['diff'])} [{f(d['lo'])}, {f(d['hi'])}]" + ("*" if d["significant"] else ""))
        md.append(f"| {k} | " + " | ".join(cells) + " |")
md.append("\n**Latency**\n")
for n in names:
    md.append(f"- {n}: {json.dumps(res[n].get('latency', {}), default=float)}")
(out / "RESULTS.md").write_text("\n".join(md) + "\n")
print("\n".join(md))

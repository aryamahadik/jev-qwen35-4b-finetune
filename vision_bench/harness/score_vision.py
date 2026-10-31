"""Score the vision runs with the bench's own formulas (copied from system-one-bench score.py: options(), pred_dist(),
gold_idx(), ece(), metrics(); the bench code itself is not run). Vision Index = 100 x mean of the five suite accuracies.
Calibration = top-label ECE, 10 equal-width bins (lo, hi], on max option probability; 'all' = over the 1,000 non-box decisions.

Failures. The bench turns a failed or missing decision into a uniform distribution whose argmax is option 0, so a failure on an item
whose gold is option 0 is counted CORRECT (its docs say failures count wrong; its code does not). Here 'acc' is the bench's number
(so it is comparable with Jev's published runs, which have failed = 0) and 'acc_strict' counts every failed item wrong. Both are
printed next to the per-suite 'failed' count; if failed > 0 anywhere, read acc_strict.

Diagnostics (labelled, never the headline): count options with C1's "<i>: " prefix; yes/no read with the letters swapped.

Latency is NOT comparable with Jev's published latency (different machine, no network, batch 1, no base64 upload in the headline
column, Jev's includes 200 Box calls); it is printed in its own block and never in the accuracy table.

Run (Mac):  .venv/bin/python -I harness/score_vision.py  -> results/scores.json + printed tables
"""
import json
import math
import os
from collections import defaultdict

import numpy as np
from sklearn.metrics import f1_score, roc_auc_score

ROOT = os.environ.get("VB_ROOT", "/Users/aryamahadik/Documents/jev/vision_bench")
RES = os.environ.get("VB_RESULTS", f"{ROOT}/results")
SUITES = ["img_sst2", "img_ar_sentiment", "img_pets", "img_vqa_yesno", "img_count"]
NAMES = {"img_sst2": "SST-2 image", "img_ar_sentiment": "Arabic sentiment image", "img_pets": "Pets (37)",
         "img_vqa_yesno": "VQAv2 yes/no", "img_count": "CountBench"}
N_PER_SUITE = 200
# Jev published numbers: system-one-bench README "Round 6" table (accuracy) and results_vision.json suite metrics (ECE), commit f329ccb
JEV = {
    "jev114": {"acc": {"img_sst2": 93.5, "img_ar_sentiment": 63.5, "img_pets": 88.5, "img_vqa_yesno": 86.5, "img_count": 93.5},
               "ece": {"img_sst2": 6.0, "img_ar_sentiment": 5.4, "img_pets": 5.0, "img_vqa_yesno": 5.8, "img_count": 4.7},
               "index": 85.1, "ece_all": 2.87, "p50": 182.6, "p95": 306.5, "calls": 1200},
    "jev113": {"acc": {"img_sst2": 94.5, "img_ar_sentiment": 59.0, "img_pets": 83.5, "img_vqa_yesno": 88.0, "img_count": 94.5},
               "ece": {"img_sst2": 6.0, "img_ar_sentiment": 10.5, "img_pets": 5.1, "img_vqa_yesno": 3.0, "img_count": 4.6},
               "index": 83.9, "ece_all": 2.83, "p50": 192.2, "p95": 326.3, "calls": 1000},
}
LATENCY_NOTE = ("NOT COMPARABLE. Jev: p50/p95 over 1,200 calls (1,000 vision + 200 Box) from an unnamed cloud server near OpenRouter, "
                "8 in flight, including network, base64 upload and JSON encoding. C1/base here: HF transformers bf16 on one L4 with no "
                "internet, batch 1, timing starts after the file is read (no base64/JSON), CPU shared with other jobs (load average in "
                "meta_*.json). The localhost HTTP sample (e2e_*.json) adds base64 and JSON but not the network.")


def load_jsonl(path):
    return [json.loads(line) for line in open(path)]


def load_cases():
    cases = {}
    for s in SUITES:
        for line in open(f"{ROOT}/data/{s}/cases.jsonl", encoding="utf-8"):
            c = json.loads(line)
            cases[c["id"]] = c
    return cases


def ece(conf, correct, bins=10):
    conf, correct = np.asarray(conf), np.asarray(correct, float)
    e = 0.0
    edges = np.linspace(0, 1, bins + 1)
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (conf > lo) & (conf <= hi)
        if m.any():
            e += m.mean() * abs(conf[m].mean() - correct[m].mean())
    return e


def metrics(rows):
    y = np.array([r["y"] for r in rows])
    yhat = np.array([r["yhat"] for r in rows])
    conf = np.array([r["conf"] for r in rows])
    correct = (y == yhat).astype(float)
    out = {"n": len(rows), "failed": int(sum(not r["ok"] for r in rows)), "acc": correct.mean(),
           "acc_strict": float(np.mean([r["ok"] and r["yhat"] == r["y"] for r in rows])),
           "macro_f1": f1_score(y, yhat, average="macro"),
           "nll": float(np.mean([-np.log(max(r["p"][r["y"]], 1e-6)) for r in rows])),
           "brier": float(np.mean([((r["p"] - np.eye(len(r["p"]))[r["y"]]) ** 2).sum() for r in rows])),
           "ece": ece(conf, correct),
           "p_true_zero": float(np.mean([r["p"][r["y"]] < 1e-4 for r in rows]))}
    out["conf_auroc"] = roc_auc_score(correct, conf) if 0 < correct.mean() < 1 else float("nan")
    order = np.argsort(-conf)
    out["acc_at_50cov"] = correct[order[: max(1, len(order) // 2)]].mean()
    sc = [r for r in rows if r["type"] == "score"]
    if sc:
        out["score_mae"] = float(np.mean([abs((np.arange(len(r["p"])) * r["p"]).sum() - r["y"]) for r in sc]))
    out["se_acc"] = math.sqrt(out["acc"] * (1 - out["acc"]) / len(rows))
    return {k: (round(float(v), 4) if isinstance(v, (float, np.floating)) else v) for k, v in out.items()}


def pct(xs, p):
    return float(np.percentile(xs, p)) if len(xs) else None


def r1(x):
    """Round for printing; None stays None (a suite with no successful row has no latency, and must not crash the scorer)."""
    return None if x is None else round(x, 1)


def lat(rows, key, suite=None):
    xs = [p[key] for p in rows if suite is None or p["suite"] == suite]
    return {"p50": r1(pct(xs, 50)), "p95": r1(pct(xs, 95)), "n": len(xs)}


def index_of(res, key="acc"):
    return round(100 * float(np.mean([res[s][key] for s in SUITES])), 2)


def se_index(accs, n=N_PER_SUITE):
    """Binomial standard error of the Vision Index (points) from per-suite accuracies in [0, 1]."""
    return 100 * math.sqrt(sum(a * (1 - a) / n for a in accs)) / len(accs)


def score_model(name, cases, preds_path):
    preds = {}
    for line in open(preds_path):
        r = json.loads(line)
        preds[r["id"]] = r
    rows = []
    for cid, c in cases.items():
        r = preds.get(cid)
        qid, q = next(iter(c["questions"].items()))
        k = 2 if q["type"] == "noul" else (len(q["criteria"]))
        y = None
        if q["type"] == "choice":
            y = list(q["criteria"].keys()).index(c["gold"][qid]["label"])
        else:
            y = int(c["gold"][qid]["label"])
        if r is None or "error" in r:
            p, ok = np.full(k, 1 / k), False
        else:
            p = np.array(r["probs"], float)
            p = p / p.sum()
            ok = True
        rows.append({"suite": c["suite"], "type": q["type"], "ok": ok, "p": p, "y": y, "yhat": int(p.argmax()), "conf": float(p.max())})
    by = defaultdict(list)
    for r in rows:
        by[r["suite"]].append(r)
    res = {s: metrics(by[s]) for s in SUITES}
    res["all"] = metrics(rows)
    res["vision_index"] = index_of(res)
    res["vision_index_strict"] = index_of(res, "acc_strict")
    res["vision_index_se"] = round(se_index([res[s]["acc"] for s in SUITES]), 2)
    res["retried_recovered"] = sum(1 for p in preds.values() if p.get("retried") and "error" not in p)  # failed once, fine on the retry
    res["retried_still_failed"] = sum(1 for p in preds.values() if p.get("retried") and "error" in p)
    res["failed_ids"] = sorted(cid for cid in cases if preds.get(cid) is None or "error" in preds[cid])
    ok_rows = [p for p in preds.values() if "error" not in p]
    res["latency_note"] = LATENCY_NOTE
    res["latency_compute_ms"] = {**lat(ok_rows, "compute_ms"), "mean": r1(float(np.mean([p["compute_ms"] for p in ok_rows])) if ok_rows else None)}
    res["latency_forward_ms"] = lat(ok_rows, "fwd_ms")
    res["latency_prep_ms"] = lat(ok_rows, "prep_ms")
    res["latency_compute_by_suite"] = {s: lat(ok_rows, "compute_ms", s) for s in SUITES}
    return res


def prob_rows(path):
    return {r["id"]: r for r in load_jsonl(path)}


def arm_acc(cases, ids, getp):
    """Accuracy of one arm over ids with failures counted WRONG; getp(id) -> probability vector or None if failed."""
    hit = fail = 0
    for cid in ids:
        c = cases[cid]
        qid, q = next(iter(c["questions"].items()))
        y = list(q["criteria"].keys()).index(c["gold"][qid]["label"]) if q["type"] == "choice" else int(c["gold"][qid]["label"])
        p = getp(cid)
        if p is None:
            fail += 1
        else:
            hit += int(int(np.argmax(p)) == y)
    n = len(ids)
    return {"n": n, "acc": round(hit / n, 4), "failed": fail, "se": round(math.sqrt((hit / n) * (1 - hit / n) / n), 4)}


def score_diag(cases, preds_path, diag_path):
    """Labelled diagnostics. Failures count wrong here (strict)."""
    main = prob_rows(preds_path)
    dg = prob_rows(diag_path)
    out = {}
    pm = lambda cid: None if "error" in main.get(cid, {"error": 1}) else main[cid]["probs"]
    pd = lambda cid: None if "error" in dg.get(cid, {"error": 1}) else dg[cid]["probs"]
    cnt = [cid for cid, c in cases.items() if c["suite"] == "img_count"]
    out["img_count"] = {"headline_no_prefix": arm_acc(cases, cnt, pm), "count_prefixed_C1_text_form": arm_acc(cases, cnt, pd)}
    for s in ("img_sst2", "img_vqa_yesno"):
        ids = [cid for cid, c in cases.items() if c["suite"] == s]

        def avg(cid):
            a, b = pm(cid), pd(cid)
            return None if a is None or b is None else [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2]
        both = [cid for cid in ids if pm(cid) is not None and pd(cid) is not None]
        agree = float(np.mean([int(np.argmax(pm(c))) == int(np.argmax(pd(c))) for c in both])) if both else None
        out[s] = {"headline_A_is_Yes": arm_acc(cases, ids, pm), "swapped_A_is_No": arm_acc(cases, ids, pd),
                  "average_of_both_orders": arm_acc(cases, ids, avg),
                  "argmax_agreement_between_orders": None if agree is None else round(agree, 4),
                  "mean_P_Yes_headline": round(float(np.mean([pm(c)[1] for c in both])), 4) if both else None,
                  "mean_P_Yes_swapped": round(float(np.mean([pd(c)[1] for c in both])), 4) if both else None}
    return out


def diag_index(res, diag):
    """Index variants built from the headline per-suite accuracies with one suite swapped for its diagnostic arm."""
    acc = {s: res[s]["acc_strict"] for s in SUITES}
    v = {"headline_strict": 100 * float(np.mean(list(acc.values())))}
    a = dict(acc)
    a["img_count"] = diag["img_count"]["count_prefixed_C1_text_form"]["acc"]
    v["count_prefixed"] = 100 * float(np.mean(list(a.values())))
    a = dict(acc)
    for s in ("img_sst2", "img_vqa_yesno"):
        a[s] = diag[s]["average_of_both_orders"]["acc"]
    v["yesno_both_orders_averaged"] = 100 * float(np.mean(list(a.values())))
    return {k: round(x, 2) for k, x in v.items()}


def compare_to_jev(res, jev):
    """C1/base vs one Jev row: Index gap, its standard error (unpaired, binomial per suite), z, and a verdict that does not over-read."""
    jacc = [jev["acc"][s] / 100 for s in SUITES]
    cacc = [res[s]["acc"] for s in SUITES]
    diff = res["vision_index"] - jev["index"]
    se = math.sqrt(se_index(cacc) ** 2 + se_index(jacc) ** 2)
    z = diff / se
    if abs(diff) >= 3.0 and abs(z) >= 2.0:
        verdict = "model ahead of Jev" if diff > 0 else "model behind Jev"
    else:
        verdict = "no difference demonstrated (gap within noise or under 3 Index points)"
    per = {}
    for s in SUITES:
        d = 100 * res[s]["acc"] - jev["acc"][s]
        se_s = 100 * math.sqrt(res[s]["acc"] * (1 - res[s]["acc"]) / N_PER_SUITE + (jev["acc"][s] / 100) * (1 - jev["acc"][s] / 100) / N_PER_SUITE)
        per[s] = {"diff": round(d, 1), "se": round(se_s, 1), "z": round(d / se_s, 2)}
    return {"index_diff": round(diff, 2), "se_diff": round(se, 2), "z": round(z, 2), "verdict": verdict, "per_suite": per}


def fmt(x, w=7, d=1, scale=100.0):
    return f"{x * scale:{w}.{d}f}" if x is not None else f"{'-':>{w}s}"


if __name__ == "__main__":
    cases = load_cases()
    out = {}
    for name in ("c1", "base"):
        path = f"{RES}/preds_{name}.jsonl"
        if os.path.exists(path):
            out[name] = score_model(name, cases, path)
            for extra in (f"e2e_{name}.json", f"summary_{name}.json", f"meta_{name}.json"):
                if os.path.exists(f"{RES}/{extra}"):
                    out[name][extra.split(".")[0]] = json.load(open(f"{RES}/{extra}"))
            if os.path.exists(f"{RES}/diag_{name}.jsonl"):
                out[name]["diagnostics"] = score_diag(cases, path, f"{RES}/diag_{name}.jsonl")
                out[name]["diagnostics"]["vision_index_variants"] = diag_index(out[name], out[name]["diagnostics"])
            out[name]["vs_jev114"] = compare_to_jev(out[name], JEV["jev114"])
            out[name]["vs_jev113"] = compare_to_jev(out[name], JEV["jev113"])
    out["jev"] = JEV
    json.dump(out, open(f"{RES}/scores.json", "w"), indent=1)

    M = [m for m in ("c1", "base") if m in out]
    print("ACCURACY % (headline; 'fail' = failed decisions; n = 200 per suite, standard error 1.7 to 3.4 points)")
    hdr = f"{'suite':24s} {'n':>4s}"
    for m in M:
        hdr += f" {m.upper():>7s} {'fail':>4s}"
    print(hdr + f" {'Jev1.14':>8s} {'Jev1.13':>8s}  | ECE: " + " ".join(f"{m.upper():>5s}" for m in M) + f" {'J1.14':>6s} {'J1.13':>6s}")
    for s in SUITES:
        line = f"{NAMES[s]:24s} {N_PER_SUITE:4d}"
        for m in M:
            line += f" {fmt(out[m][s]['acc'])} {out[m][s]['failed']:4d}"
        line += f" {JEV['jev114']['acc'][s]:8.1f} {JEV['jev113']['acc'][s]:8.1f}  |      "
        line += " ".join(f"{fmt(out[m][s]['ece'], 5)}" for m in M)
        print(line + f" {JEV['jev114']['ece'][s]:6.1f} {JEV['jev113']['ece'][s]:6.1f}")
    line = f"{'Vision Index':24s} {1000:4d}"
    for m in M:
        line += f" {out[m]['vision_index']:7.2f} {out[m]['all']['failed']:4d}"
    print(line + f" {JEV['jev114']['index']:8.1f} {JEV['jev113']['index']:8.1f}")
    line = f"{'ECE over all 1000':24s} {1000:4d}"
    for m in M:
        line += f" {100 * out[m]['all']['ece']:7.2f} {'':4s}"
    print(line + f" {JEV['jev114']['ece_all']:8.2f} {JEV['jev113']['ece_all']:8.2f}")
    for m in M:
        o = out[m]
        if o["all"]["failed"] or o["retried_recovered"]:
            print(f"{m.upper()}: FAILED {o['all']['failed']} of 1000 (still failed after one retry), first-attempt failures that the retry recovered {o['retried_recovered']}. "
                  f"Strict Vision Index (failed = wrong) {o['vision_index_strict']} vs bench-rule {o['vision_index']}; "
                  f"failed ids {o['failed_ids'][:10]}")
        else:
            print(f"{m.upper()}: failed 0 of 1000 (strict and bench-rule scores are identical), none retried")
    print("\nNOISE (unpaired; Jev per-item results are not used). Standard error of the Vision Index, points:")
    print("  Jev 1.14 %.2f | Jev 1.13 %.2f" % (se_index([JEV['jev114']['acc'][s] / 100 for s in SUITES]),
                                               se_index([JEV['jev113']['acc'][s] / 100 for s in SUITES])), end="")
    for m in M:
        print(f" | {m.upper()} {out[m]['vision_index_se']:.2f}", end="")
    print("\n  A win or loss is only called when the Index gap is at least 3 points and z >= 2.")
    for m in M:
        for jk, jn in (("vs_jev114", "Jev 1.14"), ("vs_jev113", "Jev 1.13")):
            c = out[m][jk]
            ps = " ".join(f"{s.split('_', 1)[1]} {c['per_suite'][s]['diff']:+.1f}({c['per_suite'][s]['z']:+.1f})" for s in SUITES)
            print(f"  {m.upper()} vs {jn}: Index {c['index_diff']:+.2f} (SE {c['se_diff']:.2f}, z {c['z']:+.2f}) -> {c['verdict']}\n      per suite diff(z): {ps}")
    for m in M:
        d = out[m].get("diagnostics")
        if d:
            print(f"\nDIAGNOSTICS for {m.upper()} (not headline; failures count wrong):")
            c = d["img_count"]
            print(f"  CountBench options: headline (criteria strings as Jev) {100 * c['headline_no_prefix']['acc']:.1f} | "
                  f"with C1's '<i>: ' index prefix {100 * c['count_prefixed_C1_text_form']['acc']:.1f}")
            for s in ("img_sst2", "img_vqa_yesno"):
                y = d[s]
                print(f"  {NAMES[s]} letters: A=Yes (headline) {100 * y['headline_A_is_Yes']['acc']:.1f} | A=No {100 * y['swapped_A_is_No']['acc']:.1f} | "
                      f"average of both {100 * y['average_of_both_orders']['acc']:.1f} | same answer in both orders {100 * y['argmax_agreement_between_orders']:.1f}% | "
                      f"mean P(Yes) {y['mean_P_Yes_headline']:.3f} vs {y['mean_P_Yes_swapped']:.3f}")
            print(f"  Vision Index variants: {d['vision_index_variants']}")
    print("\nLATENCY - " + LATENCY_NOTE)
    print(f"  Jev 1.14 published (not measured here): p50 {JEV['jev114']['p50']} ms, p95 {JEV['jev114']['p95']} ms; Jev 1.13: p50 {JEV['jev113']['p50']}, p95 {JEV['jev113']['p95']}")
    for m in M:
        o = out[m]
        e = o.get("e2e_" + m, {})
        print(f"  {m.upper()} batch 1 compute p50/p95 {o['latency_compute_ms']['p50']}/{o['latency_compute_ms']['p95']} ms "
              f"(forward {o['latency_forward_ms']['p50']}/{o['latency_forward_ms']['p95']}, prep {o['latency_prep_ms']['p50']}/{o['latency_prep_ms']['p95']}); "
              f"localhost HTTP c1 {e.get('c1', {}).get('p50')}/{e.get('c1', {}).get('p95')} ms, c8 {e.get('c8', {}).get('p50')}/{e.get('c8', {}).get('p95')} ms")

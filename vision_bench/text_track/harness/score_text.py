"""Score the text-track runs with the BENCH'S OWN scorer and compare with Jev's published numbers.

  .venv/bin/python -B -I harness/score_text.py [--results DIR]       (Mac; needs numpy + scikit-learn)

What runs:
  1. per-item logs (results/preds_<arm>.jsonl) -> the bench's prediction format (results/bench_preds/preds_<arm>.jsonl; a failed or
     missing decision has no answer, which the bench scores as wrong-or-option-0, see "failed" below)
  2. the bench's UNMODIFIED score.py (src/system-one-bench/score.py, run with -B so nothing is written there) on those files, after
     it has checked the cases against data.lock.json  -> results/bench_scored.json   (accuracy, ECE, macro-F1, NLL, Brier ... per suite)
  3. this file adds only what the bench does not print: failed counts and a strict accuracy (failed = wrong), standard errors, the
     System One Index (100 x mean of the 16 suite accuracies, exactly the site's index()), English/Arabic sub-indexes, the gap to
     Jev 1.14 and Jev 1.13 with its standard error and the call rule (gap >= 3 points AND z >= 2), diagnostics and latency.
Jev's numbers are read from the bench's own results.json (published runs 'or_jev_114' = Jev 1.14, 'or_jev' = Jev 1.13); nothing is
copied by hand and Jev / OpenRouter are never called.
Standard errors are binomial per suite with n = decisions (typed-decisions: 400 cases x 5 questions that share a state, so its
effective n is taken as the 400 cases, for C1, base and Jev alike). Unpaired: Jev's per-item results are not available.
"""
import argparse
import hashlib
import json
import math
import os
import subprocess
import sys
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TT = os.path.dirname(HERE)
ROOT = os.path.dirname(TT)
BENCH = os.environ.get("TT_BENCH", f"{ROOT}/src/system-one-bench")
CASES = os.environ.get("TT_CASES", f"{TT}/data/cases.jsonl")
sys.path.insert(0, HERE)
import tt_core as tt  # noqa: E402  (bench_answer, load of the same option order)

SUITES = ["ag_news", "sst2", "sst5", "emotion", "banking77", "boolq", "xnli_en", "typed-decisions", "xnli_fr", "xnli_ar",
          "ar_massive_scenario", "ar_massive_intent", "ar_offensive", "ar_sentiment", "ar_miracl_rerank", "ar_miracl_pair"]
LANG = {"ag_news": "English", "sst2": "English", "sst5": "English", "emotion": "English", "banking77": "English", "boolq": "English",
        "xnli_en": "English", "typed-decisions": "English", "xnli_fr": "French", "xnli_ar": "Arabic", "ar_massive_scenario": "Arabic",
        "ar_massive_intent": "Arabic", "ar_offensive": "Arabic", "ar_sentiment": "Arabic", "ar_miracl_rerank": "Arabic",
        "ar_miracl_pair": "Arabic"}
NAMES = {"ag_news": "AG News (4)", "sst2": "SST-2 (yes/no)", "sst5": "SST-5 (score 5)", "emotion": "DAIR Emotion (6)",
         "banking77": "Banking77 (77)", "boolq": "BoolQ (yes/no)", "xnli_en": "XNLI English (3)", "typed-decisions": "Typed decisions (5 q/case)",
         "xnli_fr": "XNLI French (3)", "xnli_ar": "XNLI Arabic (3)", "ar_massive_scenario": "MASSIVE-ar scenario (18)",
         "ar_massive_intent": "MASSIVE-ar intent (20)", "ar_offensive": "OSACT4 offensive (yes/no)", "ar_sentiment": "Arabic tweet sentiment (3)",
         "ar_miracl_rerank": "MIRACL-ar rerank (1 of 8)", "ar_miracl_pair": "MIRACL-ar pairwise (yes/no)"}
N_DEC = {"typed-decisions": 2000, "xnli_en": 150, "xnli_fr": 150, "xnli_ar": 150}      # decisions per suite (else 200)
N_EFF = {"typed-decisions": 400}                                                          # effective n for standard errors
GAP_MIN, Z_MIN = 3.0, 2.0
LATENCY_NOTE = ("NOT COMPARABLE. Jev: median / 95th percentile per API call over all 3,250 cases, 8 calls in flight, from a cloud server "
                "near OpenRouter, so it includes the network and JSON encoding. C1/base here: HF transformers bf16 on one Modal H100, no "
                "network, batch 1, one call = all questions of one case read as one batch (prompt rendering + tokenization + forward), "
                "320 sampled cases (20 per suite), LoRA unmerged, no CUDA graphs, not SGLang. Different machine, protocol and sample: "
                "do not compare these numbers.")


def n_dec(s):
    return N_DEC.get(s, 200)


def n_eff(s):
    return N_EFF.get(s, n_dec(s))


def jsonl(path):
    return [json.loads(l) for l in open(path)] if os.path.exists(path) else []


def sha_file(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


# ------------------------------------------------------------------ bench format
def write_bench_preds(arm, results, cases, outdir):
    """preds_<arm>.jsonl in the bench's format, one line per case that has at least one answer. Failed decisions have no answer."""
    rows = {}
    for r in jsonl(f"{results}/preds_{arm}.jsonl"):
        rows[(r["id"], r["qid"])] = r
    os.makedirs(outdir, exist_ok=True)
    path = f"{outdir}/preds_{arm}.jsonl"
    with open(path, "w") as f:
        for cid, c in cases.items():
            answers = {}
            for qid, q in c["questions"].items():
                r = rows.get((cid, qid))
                if r is not None and "error" not in r:
                    answers[qid] = tt.bench_answer(q, r["probs"])
            if any((cid, qid) in rows for qid in c["questions"]):    # the case was attempted
                f.write(json.dumps({"id": cid, "answers": answers}, ensure_ascii=False) + "\n")
    return path, rows


def run_bench_scorer(paths, results):
    out = f"{results}/bench_scored.json"
    cmd = [sys.executable, "-B", f"{BENCH}/score.py", "--cases", CASES, "--out", out] + paths
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=BENCH, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    if r.returncode != 0:
        raise SystemExit(f"the bench's score.py failed:\n{r.stdout[-2000:]}\n{r.stderr[-3000:]}")
    open(f"{results}/bench_scored.log", "w").write(r.stdout)
    return json.load(open(out))


def jev_published():
    path = f"{BENCH}/results.json"
    R = json.load(open(path))
    out = {"file": path, "sha256": sha_file(path)}
    for key, name in (("or_jev_114", "jev114"), ("or_jev", "jev113")):
        m = R[key]
        out[name] = {"acc": {s: m[f"suite:{s}"]["acc"] for s in SUITES}, "ece": {s: m[f"suite:{s}"]["ece"] for s in SUITES},
                     "n": {s: m[f"suite:{s}"]["n"] for s in SUITES}, "all_acc": m["all"]["acc"], "all_ece": m["all"]["ece"],
                     "all_n": m["all"]["n"], "failed": m["all"]["failed"], "latency_ms": m["latency_ms"], "cost": m["cost"]}
    return out


# ------------------------------------------------------------------ statistics
def index_of(acc, suites=None):
    suites = suites or SUITES
    return 100.0 * float(np.mean([acc[s] for s in suites]))


def se_acc(a, s):
    return math.sqrt(a * (1 - a) / n_eff(s))


def se_index(acc, suites=None):
    suites = suites or SUITES
    return 100.0 * math.sqrt(sum(se_acc(acc[s], s) ** 2 for s in suites)) / len(suites)


def compare(c_acc, j_acc, suites):
    d = index_of(c_acc, suites) - index_of(j_acc, suites)
    se = math.sqrt(se_index(c_acc, suites) ** 2 + se_index(j_acc, suites) ** 2)
    z = d / se
    if abs(d) >= GAP_MIN and abs(z) >= Z_MIN:
        verdict = "ahead of Jev" if d > 0 else "behind Jev"
    else:
        verdict = "no difference demonstrated (gap under 3 Index points or z under 2)"
    return {"diff": round(d, 2), "se": round(se, 2), "z": round(z, 2), "verdict": verdict}


def per_suite_gap(c_acc, j_acc):
    out = {}
    for s in SUITES:
        d = 100 * (c_acc[s] - j_acc[s])
        se = 100 * math.sqrt(se_acc(c_acc[s], s) ** 2 + se_acc(j_acc[s], s) ** 2)
        out[s] = {"diff": round(d, 1), "se": round(se, 1), "z": round(d / se, 2)}
    return out


def pct(xs, p):
    return float(np.percentile(xs, p)) if len(xs) else None


# ------------------------------------------------------------------ per arm
def score_arm(arm, results, cases, bench):
    res = bench[arm]
    rows = {}
    for r in jsonl(f"{results}/preds_{arm}.jsonl"):
        rows[(r["id"], r["qid"])] = r
    out = {"suites": {}, "incomplete": []}
    for s in SUITES:
        m = res[f"suite:{s}"] if f"suite:{s}" in res else None
        expected = [(cid, qid) for cid, c in cases.items() if c["suite"] == s for qid in c["questions"]]
        got = [k for k in expected if k in rows]
        fail = [k for k in expected if k not in rows or "error" in rows[k]]
        if m is None or m["n"] != len(expected):
            out["incomplete"].append(s)
        if m is None:
            continue
        strict_hits = sum(1 for k in expected if k in rows and "error" not in rows[k] and rows[k]["correct"])
        out["suites"][s] = {"n": m["n"], "n_expected": len(expected), "acc": m["acc"], "acc_strict": strict_hits / len(expected),
                            "failed": len(fail), "bench_failed": m["failed"], "ece": m["ece"], "macro_f1": m["macro_f1"], "nll": m["nll"],
                            "brier": m["brier"], "conf_auroc": m["conf_auroc"], "retried": sum(1 for k in got if rows[k].get("retried"))}
    full = not out["incomplete"] and len(out["suites"]) == len(SUITES)
    out["complete"] = full
    if "all" in res and res["all"]:
        out["all"] = {k: res["all"][k] for k in ("n", "failed", "acc", "ece", "macro_f1", "nll", "brier", "conf_auroc")}
    if full:
        acc = {s: out["suites"][s]["acc"] for s in SUITES}
        strict = {s: out["suites"][s]["acc_strict"] for s in SUITES}
        out["index"] = round(index_of(acc), 2)
        out["index_strict"] = round(index_of(strict), 2)
        out["index_se"] = round(se_index(acc), 2)
        out["index_english"] = round(index_of(acc, [s for s in SUITES if LANG[s] == "English"]), 2)
        out["index_arabic"] = round(index_of(acc, [s for s in SUITES if LANG[s] == "Arabic"]), 2)
        out["failed_total"] = sum(out["suites"][s]["failed"] for s in SUITES)
    # typed-decisions: clustered standard error of C1/base itself (does the 400-case assumption look right?)
    td = defaultdict(list)
    for (cid, qid), r in rows.items():
        if r["suite"] == "typed-decisions":
            td[cid].append(r.get("correct", 0) if "error" not in r else 0)
    if td:
        per_case = np.array([np.mean(v) for v in td.values()])
        out["typed_decisions_se"] = {"binomial_n2000": round(100 * math.sqrt(per_case.mean() * (1 - per_case.mean()) / 2000), 2),
                                     "cluster_by_case": round(100 * float(per_case.std(ddof=1) / math.sqrt(len(per_case))), 2),
                                     "assumed_n400": round(100 * math.sqrt(per_case.mean() * (1 - per_case.mean()) / 400), 2)}
    return out


def diagnostics(arm, results, cases):
    """Labelled diagnostics (never the headline). Failures count wrong here."""
    main = {(r["id"], r["qid"]): r for r in jsonl(f"{results}/preds_{arm}.jsonl")}
    diag = defaultdict(dict)
    for r in jsonl(f"{results}/diag_{arm}.jsonl"):
        diag[r["variant"]][(r["id"], r["qid"])] = r
    out = {}

    def hit(r):
        return int(r is not None and "error" not in r and r["correct"])

    sp = diag.get("score_noprefix", {})
    if sp:
        keys = sorted(sp)
        by = defaultdict(list)
        for k in keys:
            by[cases[k[0]]["suite"]].append(k)
        out["score_options"] = {s: {"n": len(ks), "headline_prefixed": sum(hit(main.get(k)) for k in ks) / len(ks),
                                    "bare_criteria_strings": sum(hit(sp[k]) for k in ks) / len(ks)} for s, ks in by.items()}
        out["score_options"]["all_score_items"] = {"n": len(keys), "headline_prefixed": sum(hit(main.get(k)) for k in keys) / len(keys),
                                                   "bare_criteria_strings": sum(hit(sp[k]) for k in keys) / len(keys)}
    yn = diag.get("yn_swapped", {})
    if yn:
        keys = sorted(yn)
        by = defaultdict(list)
        for k in keys:
            by[cases[k[0]]["suite"]].append(k)
        res = {}
        for s, ks in by.items():
            both = [k for k in ks if k in main and "error" not in main[k] and "error" not in yn[k]]

            def avg_hit(k):
                a, b = main[k]["probs"], yn[k]["probs"]
                return int(((a[1] + b[1]) / 2 > 0.5) == bool(main[k]["gold"]))
            res[s] = {"n": len(ks), "headline_A_is_Yes": sum(hit(main.get(k)) for k in ks) / len(ks),
                      "swapped_A_is_No": sum(hit(yn[k]) for k in ks) / len(ks),
                      "average_of_both_orders": sum(avg_hit(k) for k in both) / len(ks) if both else None,
                      "same_answer_in_both_orders": float(np.mean([int(np.argmax(main[k]["probs"])) == int(np.argmax(yn[k]["probs"]))
                                                                   for k in both])) if both else None,
                      "mean_P_yes_headline": float(np.mean([main[k]["probs"][1] for k in both])) if both else None,
                      "mean_P_yes_swapped": float(np.mean([yn[k]["probs"][1] for k in both])) if both else None}
        out["yes_no_letters"] = res
    return out


def index_variants(arm, scored, results, cases):
    """Index with diagnostic arms swapped in (strict accuracies; only when the diagnostics are complete)."""
    if not scored.get("complete"):
        return None
    main = {(r["id"], r["qid"]): r for r in jsonl(f"{results}/preds_{arm}.jsonl")}
    diag = defaultdict(dict)
    for r in jsonl(f"{results}/diag_{arm}.jsonl"):
        diag[r["variant"]][(r["id"], r["qid"])] = r
    need = {"score_noprefix": sum(1 for c in cases.values() for q in c["questions"].values() if q["type"] == "score"),
            "yn_swapped": sum(1 for c in cases.values() for q in c["questions"].values() if q["type"] == "noul")}

    def acc_suite(s, repl):
        ks = [(cid, qid) for cid, c in cases.items() if c["suite"] == s for qid in c["questions"]]
        tot = 0
        for k in ks:
            r = main.get(k)
            ok = r is not None and "error" not in r
            if repl is not None and k in repl[1]:
                if repl[0] == "avg":
                    d = repl[1][k]
                    ok = ok and "error" not in d
                    tot += int(ok and ((r["probs"][1] + d["probs"][1]) / 2 > 0.5) == bool(r["gold"]))
                    continue
                d = repl[1][k]
                tot += int("error" not in d and d["correct"])
                continue
            tot += int(ok and r["correct"])
        return tot / len(ks)

    res = {"headline_strict": round(index_of({s: acc_suite(s, None) for s in SUITES}), 2)}
    if len(diag.get("score_noprefix", {})) == need["score_noprefix"]:
        res["score_options_bare"] = round(index_of({s: acc_suite(s, ("raw", diag["score_noprefix"])) for s in SUITES}), 2)
    if len(diag.get("yn_swapped", {})) == need["yn_swapped"]:
        res["yes_no_both_orders_averaged"] = round(index_of({s: acc_suite(s, ("avg", diag["yn_swapped"])) for s in SUITES}), 2)
    return res


def latency(arm, results):
    rows = jsonl(f"{results}/lat_{arm}.jsonl")
    ok = [r for r in rows if "error" not in r]
    if not rows:
        return None
    o = {"calls": len(rows), "ok": len(ok), "errors": len(rows) - len(ok),
         "total_ms": {"p50": pct([r["total_ms"] for r in ok], 50), "p95": pct([r["total_ms"] for r in ok], 95)},
         "fwd_ms": {"p50": pct([r["fwd_ms"] for r in ok], 50), "p95": pct([r["fwd_ms"] for r in ok], 95)},
         "prep_ms": {"p50": pct([r["prep_ms"] for r in ok], 50), "p95": pct([r["prep_ms"] for r in ok], 95)},
         "argmax_same_as_batched_pass": f"{sum(1 for r in ok if r.get('argmax_same_as_batched'))}/{len(ok)}",
         "max_prob_diff_vs_batched": max((r["max_prob_diff_vs_batched"] for r in ok if r.get("max_prob_diff_vs_batched") is not None), default=None),
         "by_suite_total_p50": {}}
    by = defaultdict(list)
    for r in ok:
        by[r["suite"]].append(r["total_ms"])
    o["by_suite_total_p50"] = {s: round(pct(v, 50), 1) for s, v in by.items()}
    return o


# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", default=f"{TT}/results")
    a = ap.parse_args()
    R = os.path.abspath(a.results)
    cases = {c["id"]: c for c in (json.loads(l) for l in open(CASES, encoding="utf-8"))}
    arms = [x for x in ("c1", "base") if os.path.exists(f"{R}/preds_{x}.jsonl")]
    paths = [write_bench_preds(x, R, cases, f"{R}/bench_preds")[0] for x in arms]
    bench = run_bench_scorer(paths, R)
    jev = jev_published()
    out = {"arms": {}, "jev": jev, "bench_commit": subprocess.run(["git", "-C", BENCH, "rev-parse", "HEAD"], capture_output=True,
                                                                   text=True).stdout.strip()}
    for x in arms:
        sc = score_arm(x, R, cases, bench)
        sc["diagnostics"] = diagnostics(x, R, cases)
        sc["index_variants"] = index_variants(x, sc, R, cases)
        sc["latency"] = latency(x, R)
        if sc["complete"]:
            acc = {s: sc["suites"][s]["acc"] for s in SUITES}
            sc["vs_jev114"] = compare(acc, jev["jev114"]["acc"], SUITES)
            sc["vs_jev113"] = compare(acc, jev["jev113"]["acc"], SUITES)
            sc["vs_jev114_english"] = compare(acc, jev["jev114"]["acc"], [s for s in SUITES if LANG[s] == "English"])
            sc["vs_jev114_arabic"] = compare(acc, jev["jev114"]["acc"], [s for s in SUITES if LANG[s] == "Arabic"])
            sc["per_suite_vs_jev114"] = per_suite_gap(acc, jev["jev114"]["acc"])
            sc["per_suite_vs_jev113"] = per_suite_gap(acc, jev["jev113"]["acc"])
        out["arms"][x] = sc
    for nm in ("jev114", "jev113"):
        acc = jev[nm]["acc"]
        out[nm + "_index"] = {"index": round(index_of(acc), 2), "english": round(index_of(acc, [s for s in SUITES if LANG[s] == "English"]), 2),
                              "arabic": round(index_of(acc, [s for s in SUITES if LANG[s] == "Arabic"]), 2), "se": round(se_index(acc), 2),
                              "all_ece": jev[nm]["all_ece"]}
    for fn in ("meta.json", "gates.json", "summary_main.json", "skipped.json", "modal_done.json", "modal_env.json"):
        if os.path.exists(f"{R}/{fn}"):
            out[fn.split(".")[0]] = json.load(open(f"{R}/{fn}"))
    out["latency_note"] = LATENCY_NOTE
    json.dump(out, open(f"{R}/scores.json", "w"), indent=1)
    print_report(out)


def f1(x, w=6):
    return f"{100 * x:{w}.1f}" if x is not None else f"{'-':>{w}s}"


def print_report(o):
    arms = list(o["arms"])
    J14, J13 = o["jev"]["jev114"], o["jev"]["jev113"]
    print("ACCURACY % (n = decisions; failed = decisions with no answer; Jev = published runs read from the bench's results.json)")
    hdr = f"{'suite':30s} {'n':>5s}" + "".join(f" {x.upper():>6s} {'fail':>4s}" for x in arms) + f" {'Jev1.14':>8s} {'Jev1.13':>8s} | gap C1-J1.14 (z)"
    print(hdr)
    for s in SUITES:
        line = f"{NAMES[s]:30s} {n_dec(s):5d}"
        for x in arms:
            m = o["arms"][x]["suites"].get(s)
            line += f" {f1(m['acc']) if m else '   -  '} {m['failed'] if m else '-':>4}"
        line += f" {100 * J14['acc'][s]:8.1f} {100 * J13['acc'][s]:8.1f}"
        g = o["arms"].get("c1", {}).get("per_suite_vs_jev114", {}).get(s)
        if g:
            line += f" | {g['diff']:+5.1f} ({g['z']:+.1f})"
        print(line)
    for x in arms:
        sc = o["arms"][x]
        if sc.get("complete"):
            print(f"{x.upper():5s} System One Index {sc['index']:.2f} (SE {sc['index_se']:.2f}) | English {sc['index_english']:.2f} | Arabic {sc['index_arabic']:.2f} | "
                  f"strict (failed = wrong) {sc['index_strict']:.2f} | failed {sc['failed_total']} of {sc['all']['n']} | ECE all decisions {100 * sc['all']['ece']:.2f}% | "
                  f"acc all decisions {100 * sc['all']['acc']:.2f}%")
        else:
            print(f"{x.upper():5s} INCOMPLETE: suites missing or short {sc['incomplete']}; no index")
    for nm, lab in (("jev114", "Jev 1.14"), ("jev113", "Jev 1.13")):
        d = o[nm + "_index"]
        print(f"{lab:8s} System One Index {d['index']:.2f} (SE {d['se']:.2f}) | English {d['english']:.2f} | Arabic {d['arabic']:.2f} | ECE all decisions {100 * d['all_ece']:.2f}%")
    for x in arms:
        sc = o["arms"][x]
        for k, lab in (("vs_jev114", "Jev 1.14"), ("vs_jev113", "Jev 1.13"), ("vs_jev114_english", "Jev 1.14 English"), ("vs_jev114_arabic", "Jev 1.14 Arabic")):
            if k in sc:
                c = sc[k]
                print(f"  {x.upper()} vs {lab}: gap {c['diff']:+.2f} points (SE {c['se']:.2f}, z {c['z']:+.2f}) -> {c['verdict']}")
    print("\nLATENCY - " + o["latency_note"])
    for nm in ("jev114", "jev113"):
        print(f"  {nm} published: p50 {o['jev'][nm]['latency_ms']['p50']} ms, p95 {o['jev'][nm]['latency_ms']['p95']} ms")
    for x in arms:
        l = o["arms"][x].get("latency")
        if l:
            print(f"  {x.upper()}: {l['ok']}/{l['calls']} calls, total p50/p95 {l['total_ms']['p50']:.0f}/{l['total_ms']['p95']:.0f} ms "
                  f"(forward {l['fwd_ms']['p50']:.0f}/{l['fwd_ms']['p95']:.0f}, prep {l['prep_ms']['p50']:.0f}/{l['prep_ms']['p95']:.0f}); "
                  f"same argmax as the batched pass on {l['argmax_same_as_batched_pass']} calls")


if __name__ == "__main__":
    main()

"""SKEPTIC re-score: every headline number recomputed from the saved per-item logs by code that shares nothing with the scorer.

  .venv/bin/python -B -I harness/skeptic_rescore.py [--results DIR]

Independent of score_text.py, tt_core.py and the bench's score.py: it needs only numpy + json. Starting from the RAW candidate logits
of every view stored in results/preds_<arm>.jsonl it
  1. recomputes the probabilities (softmax, T = 1; yes/no: P(Yes) from the displayed letter of Yes; choice/score: map each view back
     to the bench's option order and average the two views) and checks them against the stored probabilities,
  2. recomputes the gold index from cases.jsonl (its own implementation) and the stored gold,
  3. recomputes accuracy (bench rule and strict), top-label ECE (10 bins, (lo, hi]), per-suite and over all decisions, the System One
     Index, the English / Arabic sub-indexes, standard errors, the gap to Jev with z and the call rule,
  4. recomputes Jev's published Index and ECE from the bench's results.json (and checks them against the bench README's table),
  5. checks log hygiene: every decision once, same prompt hashes and token counts for both arms, two views exactly where expected,
  6. recomputes the diagnostics, the latency percentiles and the Modal cost,
  7. compares everything with results/scores.json (score_text.py) and results/bench_scored.json (the bench's score.py) and prints
     MATCH / MISMATCH for each number. Exit code 1 on any mismatch.
Tolerances: accuracies exact (4 dp, the bench's own rounding); ECE 1.5e-4; Index / gap / SE 0.011 points (score_text builds the Index from the
bench's 4-dp suite accuracies, as the site does; the skeptic uses unrounded ones); z 0.021.
"""
import argparse
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TT = os.path.dirname(HERE)
ROOT = os.path.dirname(TT)
BENCH = os.environ.get("TT_BENCH", f"{ROOT}/src/system-one-bench")
CASES = os.environ.get("TT_CASES", f"{TT}/data/cases.jsonl")
ENGLISH = ["ag_news", "sst2", "sst5", "emotion", "banking77", "boolq", "xnli_en", "typed-decisions"]
ARABIC = ["xnli_ar", "ar_massive_scenario", "ar_massive_intent", "ar_offensive", "ar_sentiment", "ar_miracl_rerank", "ar_miracl_pair"]
ALL = ENGLISH + ["xnli_fr"] + ARABIC
FAILS = []


def check(name, mine, theirs, tol=1e-9):
    ok = (mine is None and theirs is None) or (mine is not None and theirs is not None and abs(mine - theirs) <= tol)
    if not ok:
        FAILS.append((name, mine, theirs))
    return ok


def jl(path):
    return [json.loads(l) for l in open(path)] if os.path.exists(path) else []


def softmax(x):
    x = np.asarray(x, float)
    e = np.exp(x - x.max())
    return e / e.sum()


def my_gold(q, g):
    if q["type"] == "choice":
        keys = list(q["criteria"].keys()) if isinstance(q["criteria"], dict) else list(q["criteria"])
        return keys.index(g["label"])
    return int(g["label"])


def my_probs(q, views, logits):
    """probabilities in the bench's option order from raw per-view candidate logits."""
    if q["type"] == "noul":
        perm = views[0] if views[0] is not None else [0, 1]
        sm = softmax(logits[0])                  # displayed letters A, B; perm[j] = original option shown at position j (0 = Yes)
        p_yes = sm[perm.index(0)]
        return np.array([1 - p_yes, p_yes])
    k = len(logits[0])
    acc = np.zeros(k)
    for v, lg in zip(views, logits):
        perm = v if v is not None else list(range(k))
        sm = softmax(lg)
        for pos, orig in enumerate(perm):
            acc[orig] += sm[pos]
    return acc / len(logits)


def my_ece(conf, correct):
    conf, correct = np.asarray(conf, float), np.asarray(correct, float)
    edges = np.linspace(0, 1, 11)
    e = 0.0
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (conf > lo) & (conf <= hi)
        if m.any():
            e += m.mean() * abs(conf[m].mean() - correct[m].mean())
    return float(e)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", default=f"{TT}/results")
    a = ap.parse_args()
    R = a.results
    cases = {}
    for l in open(CASES, encoding="utf-8"):
        c = json.loads(l)
        cases[c["id"]] = c
    expected = [(cid, qid) for cid, c in cases.items() for qid in c["questions"]]
    suite_of = {cid: c["suite"] for cid, c in cases.items()}
    n_expected = Counter(suite_of[cid] for cid, _ in expected)
    scores = json.load(open(f"{R}/scores.json"))
    bench = json.load(open(f"{R}/bench_scored.json"))
    out = {"arms": {}}
    lines = []

    def say(s=""):
        lines.append(s)
        print(s)

    # ---------------- Jev, from the bench's results.json (independent read)
    bj = json.load(open(f"{BENCH}/results.json"))
    jev = {}
    for key, nm in (("or_jev_114", "Jev 1.14"), ("or_jev", "Jev 1.13")):
        acc = {s: bj[key]["suite:" + s]["acc"] for s in ALL}
        jev[nm] = {"acc": acc, "index": 100 * np.mean([acc[s] for s in ALL]), "english": 100 * np.mean([acc[s] for s in ENGLISH]),
                   "arabic": 100 * np.mean([acc[s] for s in ARABIC]), "ece": bj[key]["all"]["ece"], "latency": bj[key]["latency_ms"]}
    # the bench README states Jev 1.14 = 79.3 / 78.8 / 80.3 and Jev 1.13 = 79.0 / 78.5 / 79.9
    for nm, (i, e, ar) in (("Jev 1.14", (79.3, 78.8, 80.3)), ("Jev 1.13", (79.0, 78.5, 79.9))):
        check(f"{nm} index vs bench README", round(jev[nm]["index"], 1), i)
        check(f"{nm} English vs bench README", round(jev[nm]["english"], 1), e)
        check(f"{nm} Arabic vs bench README", round(jev[nm]["arabic"], 1), ar)
    check("Jev 1.14 ECE vs README 6.0%", round(100 * jev["Jev 1.14"]["ece"], 1), 6.0)
    check("Jev 1.13 ECE vs README 6.1%", round(100 * jev["Jev 1.13"]["ece"], 1), 6.1)
    say("JEV published (recomputed from results.json): " + " | ".join(
        f"{nm}: index {jev[nm]['index']:.2f} English {jev[nm]['english']:.2f} Arabic {jev[nm]['arabic']:.2f} ECE {100 * jev[nm]['ece']:.2f}%" for nm in jev))

    def se_s(acc, s):
        n = 400 if s == "typed-decisions" else n_expected[s]
        return math.sqrt(acc * (1 - acc) / n)

    for arm in ("c1", "base"):
        rows = jl(f"{R}/preds_{arm}.jsonl")
        if not rows:
            continue
        key = Counter((r["id"], r["qid"]) for r in rows)
        dup = [k for k, v in key.items() if v > 1]
        missing = [k for k in expected if k not in key]
        extra = [k for k in key if k not in set(expected)]
        say(f"\n=== {arm.upper()}: {len(rows)} logged decisions; duplicates {len(dup)}, missing {len(missing)}, unknown {len(extra)}")
        check(f"{arm}: no duplicate decisions", len(dup), 0)
        check(f"{arm}: no unknown decisions", len(extra), 0)
        by = {(r["id"], r["qid"]): r for r in rows}
        corr, conf, ok_flag, dprob, gold_bad = {}, {}, {}, 0.0, 0
        hy = Counter()
        for k in expected:
            r = by.get(k)
            c = cases[k[0]]
            q = c["questions"][k[1]]
            g = my_gold(q, c["gold"][k[1]])
            if r is None or "error" in r:
                ok_flag[k], corr[k], conf[k] = False, 0, None
                continue
            if r["gold"] != g:
                gold_bad += 1
            if len(r["view_logits"]) != (2 if q["type"] in ("choice", "score") else 1):
                hy["wrong_number_of_views"] += 1
            p = my_probs(q, r["views"], r["view_logits"])
            dprob = max(dprob, float(np.abs(p - np.array(r["probs"])).max()))
            pred = int(np.argmax(p))
            ok_flag[k], corr[k], conf[k] = True, int(pred == g), float(p.max())
            if pred != r["pred"]:
                hy["pred_differs_from_logged"] += 1
        check(f"{arm}: stored gold equals recomputed gold", gold_bad, 0)
        say(f"max |recomputed prob - logged prob| over all decisions: {dprob:.2e}; hygiene flags: {dict(hy)}")
        check(f"{arm}: recomputed probabilities equal logged ones (1e-5)", 1.0 if dprob < 1e-5 else 0.0, 1.0)
        check(f"{arm}: recomputed argmax equals logged argmax", hy["pred_differs_from_logged"], 0)
        check(f"{arm}: two views exactly for choice/score, one for yes/no", hy["wrong_number_of_views"], 0)
        # ---- per suite
        sc = scores["arms"][arm]
        acc, strict, ece_s, nfail = {}, {}, {}, {}
        for s in ALL:
            ks = [k for k in expected if suite_of[k[0]] == s]
            nfail[s] = sum(1 for k in ks if not ok_flag[k])
            strict[s] = sum(corr[k] for k in ks) / len(ks)
            # bench rule: a failed decision is a uniform distribution whose argmax is option 0 -> correct iff gold == 0
            bench_hits = 0
            confs, cors = [], []
            for k in ks:
                c = cases[k[0]]
                q = c["questions"][k[1]]
                g = my_gold(q, c["gold"][k[1]])
                if ok_flag[k]:
                    bench_hits += corr[k]
                    confs.append(conf[k]); cors.append(corr[k])
                else:
                    kk = 2 if q["type"] == "noul" else len(q["criteria"])
                    bench_hits += int(g == 0)
                    confs.append(1 / kk); cors.append(int(g == 0))
            acc[s] = bench_hits / len(ks)
            ece_s[s] = my_ece(confs, cors)
            m = sc["suites"][s]
            b = bench[arm]["suite:" + s]
            check(f"{arm} {s}: n", len(ks), m["n"])
            check(f"{arm} {s}: acc vs score_text", round(acc[s], 4), m["acc"], 1e-9)
            check(f"{arm} {s}: acc vs bench score.py", round(acc[s], 4), b["acc"], 1e-9)
            check(f"{arm} {s}: strict acc vs score_text", strict[s], m["acc_strict"], 1e-9)
            check(f"{arm} {s}: failed", nfail[s], m["failed"])
            check(f"{arm} {s}: ECE vs score_text (1e-4)", round(ece_s[s], 4), m["ece"], 1.5e-4)
            check(f"{arm} {s}: ECE vs bench score.py (1e-4)", round(ece_s[s], 4), b["ece"], 1.5e-4)
        all_conf = []
        all_cor = []
        n_all = 0
        for k in expected:
            c = cases[k[0]]
            q = c["questions"][k[1]]
            g = my_gold(q, c["gold"][k[1]])
            n_all += 1
            if ok_flag[k]:
                all_conf.append(conf[k]); all_cor.append(corr[k])
            else:
                kk = 2 if q["type"] == "noul" else len(q["criteria"])
                all_conf.append(1 / kk); all_cor.append(int(g == 0))
        ece_all, acc_all = my_ece(all_conf, all_cor), float(np.mean(all_cor))
        check(f"{arm} all: n", n_all, bench[arm]["all"]["n"])
        check(f"{arm} all: acc vs bench score.py", round(acc_all, 4), bench[arm]["all"]["acc"], 1e-9)
        check(f"{arm} all: ECE vs bench score.py (1e-4)", round(ece_all, 4), bench[arm]["all"]["ece"], 1.5e-4)
        check(f"{arm} all: ECE vs score_text (1e-4)", round(ece_all, 4), sc["all"]["ece"], 1.5e-4)
        index = 100 * np.mean([acc[s] for s in ALL])
        eng = 100 * np.mean([acc[s] for s in ENGLISH])
        ara = 100 * np.mean([acc[s] for s in ARABIC])
        index_strict = 100 * np.mean([strict[s] for s in ALL])
        se_idx = 100 * math.sqrt(sum(se_s(acc[s], s) ** 2 for s in ALL)) / 16
        check(f"{arm}: System One Index", round(index, 2), sc["index"], 1.1e-2)
        check(f"{arm}: English index", round(eng, 2), sc["index_english"], 1.1e-2)
        check(f"{arm}: Arabic index", round(ara, 2), sc["index_arabic"], 1.1e-2)
        check(f"{arm}: strict index", round(index_strict, 2), sc["index_strict"], 1.1e-2)
        check(f"{arm}: index SE", round(se_idx, 2), sc["index_se"], 1.1e-2)
        say(f"{arm.upper()} Index {index:.2f} (SE {se_idx:.2f}) English {eng:.2f} Arabic {ara:.2f} strict {index_strict:.2f}; "
            f"failed {sum(nfail.values())}; ECE all {100 * ece_all:.2f}%; acc all {100 * acc_all:.2f}%")
        out["arms"][arm] = {"index": index, "english": eng, "arabic": ara, "index_strict": index_strict, "se": se_idx, "ece_all": ece_all,
                            "acc_all": acc_all, "acc": acc, "ece": ece_s, "failed": nfail}
        # ---- gap to Jev
        for nm, tag in (("Jev 1.14", "vs_jev114"), ("Jev 1.13", "vs_jev113")):
            jacc = jev[nm]["acc"]
            jse = 100 * math.sqrt(sum(se_s(jacc[s], s) ** 2 for s in ALL)) / 16
            gap = index - jev[nm]["index"]
            se = math.sqrt(se_idx ** 2 + jse ** 2)
            z = gap / se
            call = ("ahead" if gap > 0 else "behind") if abs(gap) >= 3 and abs(z) >= 2 else "no difference demonstrated"
            check(f"{arm} {tag}: gap", round(gap, 2), sc[tag]["diff"], 1.1e-2)
            check(f"{arm} {tag}: SE", round(se, 2), sc[tag]["se"], 1.1e-2)
            check(f"{arm} {tag}: z", round(z, 2), sc[tag]["z"], 2.1e-2)
            theirs = "ahead" if "ahead" in sc[tag]["verdict"] else ("behind" if "behind" in sc[tag]["verdict"] else "none")
            mine = ("ahead" if gap > 0 else "behind") if call != "no difference demonstrated" else "none"
            if mine != theirs:
                FAILS.append((f"{arm} {tag}: verdict", mine, theirs))
            say(f"{arm.upper()} vs {nm}: gap {gap:+.2f} (SE {se:.2f}, z {z:+.2f}) -> {call}")
            out["arms"][arm][tag] = {"gap": gap, "se": se, "z": z, "call": call}
        # per-suite gaps
        for s in ALL:
            d = 100 * (acc[s] - jev["Jev 1.14"]["acc"][s])
            se = 100 * math.sqrt(se_s(acc[s], s) ** 2 + se_s(jev["Jev 1.14"]["acc"][s], s) ** 2)
            check(f"{arm} {s}: gap to Jev 1.14", round(d, 1), sc["per_suite_vs_jev114"][s]["diff"], 0.051)
            check(f"{arm} {s}: z to Jev 1.14", round(d / se, 2), sc["per_suite_vs_jev114"][s]["z"], 1.2e-2)
        # ---- diagnostics
        diag = defaultdict(dict)
        for r in jl(f"{R}/diag_{arm}.jsonl"):
            diag[r["variant"]][(r["id"], r["qid"])] = r
        if diag.get("score_noprefix"):
            d = diag["score_noprefix"]
            hits_pref = hits_bare = 0
            for k, r in d.items():
                q = cases[k[0]]["questions"][k[1]]
                if "error" not in r:
                    p = my_probs(q, r["views"], r["view_logits"])
                    hits_bare += int(int(np.argmax(p)) == my_gold(q, cases[k[0]]["gold"][k[1]]))
                hits_pref += corr[k]
            n = len(d)
            say(f"   diagnostic score options, {n} items: headline '<i>: ' {100 * hits_pref / n:.1f}% | bare criteria strings {100 * hits_bare / n:.1f}%")
            sd = sc["diagnostics"].get("score_options", {}).get("all_score_items")
            if sd:
                check(f"{arm} diag score_noprefix bare acc", round(hits_bare / n, 6), round(sd["bare_criteria_strings"], 6), 1e-9)
                check(f"{arm} diag score_noprefix headline acc", round(hits_pref / n, 6), round(sd["headline_prefixed"], 6), 1e-9)
        if diag.get("yn_swapped"):
            d = diag["yn_swapped"]
            hs = hw = 0
            for k, r in d.items():
                q = cases[k[0]]["questions"][k[1]]
                if "error" not in r:
                    p = my_probs(q, r["views"], r["view_logits"])
                    hw += int(int(np.argmax(p)) == my_gold(q, cases[k[0]]["gold"][k[1]]))
                hs += corr[k]
            say(f"   diagnostic yes/no letters, {len(d)} items: A=Yes (headline) {100 * hs / len(d):.1f}% | A=No {100 * hw / len(d):.1f}%")
        # ---- latency
        lat = [r for r in jl(f"{R}/lat_{arm}.jsonl") if "error" not in r]
        if lat:
            t = [r["total_ms"] for r in lat]
            say(f"   latency (NOT COMPARABLE with Jev's): {len(lat)} calls, p50 {np.percentile(t, 50):.1f} ms p95 {np.percentile(t, 95):.1f} ms")
            sl = scores["arms"][arm]["latency"]
            check(f"{arm} latency p50", float(np.percentile(t, 50)), sl["total_ms"]["p50"], 1e-6)
            check(f"{arm} latency p95", float(np.percentile(t, 95)), sl["total_ms"]["p95"], 1e-6)
            out["arms"][arm]["latency_p50_p95"] = [float(np.percentile(t, 50)), float(np.percentile(t, 95))]
    # ---- both arms read the same prompts
    if len(out["arms"]) == 2:
        a_, b_ = ({(r["id"], r["qid"]): r for r in jl(f"{R}/preds_{x}.jsonl")} for x in ("c1", "base"))
        same_prompt = sum(1 for k in a_ if k in b_ and "error" not in a_[k] and "error" not in b_[k] and a_[k]["prompt_sha256"] == b_[k]["prompt_sha256"]
                          and a_[k]["n_tokens"] == b_[k]["n_tokens"])
        both = sum(1 for k in a_ if k in b_ and "error" not in a_[k] and "error" not in b_[k])
        check("C1 and base read byte-identical prompts (sha256) for every decision", same_prompt, both)
        say(f"\nC1 and base read the same prompt on {same_prompt} of {both} decisions")
        differ = sum(1 for k in a_ if k in b_ and "error" not in a_[k] and "error" not in b_[k] and a_[k]["pred"] != b_[k]["pred"])
        say(f"C1 and base give a different answer on {differ} decisions (so the adapter is doing something)")
    # ---- cost
    md = f"{R}/modal_done.json"
    if os.path.exists(md):
        d = json.load(open(md))
        cost = [v for k, v in d.items() if k.startswith("est_cost_usd")][0]
        say(f"\nModal: function wall {d['function_wall_s']:.0f} s -> {cost:.3f} USD at 4.30 USD/h (H100 3.95 + 4 CPU 0.19 + 20 GiB 0.16)")
        check("Modal cost recomputed from wall time", round(d["function_wall_s"] / 3600 * 4.30, 4), round(cost, 4), 1e-3)
        out["modal_cost_usd_est"] = cost
    mb = f"{R}/modal_billing.json"
    if os.path.exists(mb):
        b = json.load(open(mb))
        tot = sum(float(r["cost"]) for r in b["rows"])
        check("Modal bill: total equals the sum of the billed rows", round(tot, 4), b["total_usd"], 1e-9)
        say(f"Modal bill (modal billing report, rows of app text-track-c1): {tot:.4f} USD = " + ", ".join(f"{k} {v:.4f}" for k, v in b["cost_by_app"].items()))
        out["modal_bill_usd"] = tot
    say(f"\n{'ALL CHECKS MATCH' if not FAILS else 'MISMATCHES: ' + str(len(FAILS))}  ({len(lines)} summary lines)")
    for f in FAILS:
        say(f"  MISMATCH {f}")
    out["mismatches"] = [list(map(str, f)) for f in FAILS]
    json.dump(out, open(f"{R}/skeptic.json", "w"), indent=1, default=float)
    open(f"{R}/skeptic.txt", "w").write("\n".join(lines) + "\n")
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()

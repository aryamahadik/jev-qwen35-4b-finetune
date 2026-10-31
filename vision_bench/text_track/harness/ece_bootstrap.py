"""Bootstrap the System One Index and the all-decision ECE of C1 and base from the per-item logs (resampling the 3,250 CASES with
replacement, so the 5 questions of one typed-decisions case stay together; 2,000 resamples, fixed seed). numpy + json only.
  .venv/bin/python -B -I harness/ece_bootstrap.py [--results DIR]   -> results/bootstrap.json
Jev's per-item results are not published, so Jev is not bootstrapped: its numbers are fixed here and only C1's / base's sampling noise is shown.
The point estimates must equal the scorer's (checked below)."""
import argparse, json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); TT = os.path.dirname(HERE)
SUITES = ["ag_news", "sst2", "sst5", "emotion", "banking77", "boolq", "xnli_en", "typed-decisions", "xnli_fr", "xnli_ar", "ar_massive_scenario",
          "ar_massive_intent", "ar_offensive", "ar_sentiment", "ar_miracl_rerank", "ar_miracl_pair"]
ap = argparse.ArgumentParser(); ap.add_argument("--results", default=f"{TT}/results"); a = ap.parse_args()
cases = {}
for l in open(f"{TT}/data/cases.jsonl", encoding="utf-8"):
    c = json.loads(l); cases[c["id"]] = c
ids = list(cases); idx = {cid: i for i, cid in enumerate(ids)}
case_suite = np.array([SUITES.index(cases[cid]["suite"]) for cid in ids])
out = {}
for arm in ("c1", "base"):
    rows = [json.loads(l) for l in open(f"{a.results}/preds_{arm}.jsonl")]
    ci = np.array([idx[r["id"]] for r in rows]); conf = np.array([r["conf"] for r in rows]); cor = np.array([r["correct"] for r in rows], float)
    bins = np.clip(np.ceil(conf * 10).astype(int) - 1, 0, 9)           # (lo, hi] bins on max probability
    ds = case_suite[ci]

    def stats(w):                                                      # w: weight of each CASE
        wd = w[ci]
        acc = np.array([(wd * cor)[ds == s].sum() / wd[ds == s].sum() for s in range(16)])
        W = wd.sum()
        e = sum(abs((wd * (conf - cor))[bins == b].sum()) for b in range(10)) / W
        return 100 * acc.mean(), e
    p_idx, p_ece = stats(np.ones(len(ids)))
    rng = np.random.default_rng(0)
    res = np.array([stats(np.bincount(rng.integers(0, len(ids), len(ids)), minlength=len(ids)).astype(float)) for _ in range(2000)])
    out[arm] = {"index": round(float(p_idx), 3), "index_boot_se": round(float(res[:, 0].std()), 3),
                "index_boot_ci95": [round(float(np.percentile(res[:, 0], 2.5)), 2), round(float(np.percentile(res[:, 0], 97.5)), 2)],
                "ece_all": round(float(p_ece), 5), "ece_boot_se": round(float(res[:, 1].std()), 5),
                "ece_boot_ci95": [round(float(np.percentile(res[:, 1], 2.5)), 5), round(float(np.percentile(res[:, 1], 97.5)), 5)]}
    print(arm, out[arm])
S = json.load(open(f"{a.results}/scores.json"))
for arm in out:
    assert abs(out[arm]["index"] - S["arms"][arm]["index"]) < 0.011 and abs(out[arm]["ece_all"] - S["arms"][arm]["all"]["ece"]) < 1.5e-4, (arm, out[arm])
json.dump(out, open(f"{a.results}/bootstrap.json", "w"), indent=1)

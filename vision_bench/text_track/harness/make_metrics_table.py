"""Full metric tables (no hand-typed numbers): per suite, per question type and over all decisions, for C1, base, Jev 1.14, Jev 1.13.
Mine = the bench's own score.py output on our logs (results/bench_scored.json); Jev = the bench's published results.json.
  python -B -I harness/make_metrics_table.py -> METRICS.md"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); TT = os.path.dirname(HERE); ROOT = os.path.dirname(TT)
B = json.load(open(f"{TT}/results/bench_scored.json")); J = json.load(open(f"{ROOT}/src/system-one-bench/results.json"))
M = {"C1": B["c1"], "Base": B["base"], "Jev 1.14": J["or_jev_114"], "Jev 1.13": J["or_jev"]}
SUITES = ["ag_news", "sst2", "sst5", "emotion", "banking77", "boolq", "xnli_en", "typed-decisions", "xnli_fr", "xnli_ar", "ar_massive_scenario",
          "ar_massive_intent", "ar_offensive", "ar_sentiment", "ar_miracl_rerank", "ar_miracl_pair"]
COLS = [("acc", "Accuracy %", 100, 1), ("macro_f1", "Macro-F1 %", 100, 1), ("ece", "ECE % (lower better)", 100, 1), ("nll", "Log loss (lower better)", 1, 3),
        ("brier", "Brier (lower better)", 1, 3), ("conf_auroc", "Confidence AUROC (higher better)", 1, 3), ("acc_at_50cov", "Accuracy % on the most-confident half", 100, 1)]
L = ["# All metrics, side by side\n", "Mine = bench's own `score.py` on our per-item logs. Jev = the bench's published runs. Same formulas, same 4,850 decisions.\n"
     "Log loss = average -log(probability given to the right answer). Brier = squared error of the whole probability vector. "
     "AUROC = how well confidence separates right from wrong (0.5 = no signal). 'Most-confident half' = accuracy on the 50% of answers the model was surest about.\n"]
def row(key, name):
    return key, name
for col, title, sc, d in COLS:
    L.append(f"## {title}\n")
    L.append("| Suite | n | C1 | Base | Jev 1.14 | Jev 1.13 | C1 - Jev 1.14 |"); L.append("|---|---:|---:|---:|---:|---:|---:|")
    for key, name in [(f"suite:{s}", s) for s in SUITES] + [("type:noul", "ALL yes/no questions"), ("type:choice", "ALL choice questions"), ("type:score", "ALL score questions"), ("all", "**ALL 4,850 decisions**")]:
        vals = [M[m].get(key, {}).get(col) for m in M]
        n = M["C1"][key]["n"]
        f = lambda v: "-" if v is None else f"{v * sc:.{d}f}"
        gap = "-" if vals[0] is None or vals[2] is None else f"{(vals[0] - vals[2]) * sc:+.{d}f}"
        L.append(f"| {name} | {n} | " + " | ".join(f(v) for v in vals) + f" | {gap} |")
    L.append("")
L.append("## Typed-decisions by workflow (accuracy %, n = decisions)\n"); L.append("| Workflow | n | C1 | Base | Jev 1.14 | Jev 1.13 | C1 - Jev 1.14 |"); L.append("|---|---:|---:|---:|---:|---:|---:|")
wf = sorted(k for k in B["c1"] if k.startswith("workflow:"))
for k in wf:
    vals = [M[m].get(k, {}).get("acc") for m in M]
    L.append(f"| {k[9:]} | {B['c1'][k]['n']} | " + " | ".join("-" if v is None else f"{100 * v:.1f}" for v in vals) + f" | {100 * (vals[0] - vals[2]):+.1f} |")
open(f"{TT}/METRICS.md", "w").write("\n".join(L) + "\n"); print("\n".join(L))

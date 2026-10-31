"""Batch calibration (Zhou et al. 2024, "Batch Calibration"): remove a task's label prior estimated from UNLABELED
inputs of that task. For each task (same source + same option set), average the log-probabilities each label gets over
the task's choice questions, then p'(label) ∝ exp(log p(label) − mean_logp(label)). Yes/no rows are left unchanged.
Needs no gold labels, only a batch of questions from the same task (in serving: a running average per label set).
Applied only to tasks with >= MIN_N questions (chosen on dev: per-question option subsets, as in intent routing,
have no shared prior and are left unchanged).
Usage: batchcal.py SPLIT NAME  -> preds_<split>/<name>_bc.jsonl
"""
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
split, name = sys.argv[1], sys.argv[2]
pd = HERE / ("preds" if split == "eval" else f"preds_{split}")
rows = {json.loads(l)["id"]: json.loads(l) for l in open(HERE / f"data/{split}.jsonl")}
P = [json.loads(l) for l in open(pd / f"{name}.jsonl")]
task = lambda r: (r["source"], tuple(sorted(r["options"])))
acc = defaultdict(lambda: defaultdict(list))
for p in P:
    r = rows[p["id"]]
    if r["qtype"] == "choice":
        for o in r["options"]:
            acc[task(r)][o].append(math.log(max(p["probs"].get(o, 0.0), 1e-12)))
MIN_N = 20
prior = {t: {o: sum(v) / len(v) for o, v in d.items()} for t, d in acc.items() if min(len(v) for v in d.values()) >= MIN_N}
with open(pd / f"{name}_bc.jsonl", "w") as f:
    for p in P:
        r = rows[p["id"]]
        if r["qtype"] == "choice" and task(r) in prior:
            lg = {o: math.log(max(p["probs"].get(o, 0.0), 1e-12)) - prior[task(r)][o] for o in r["options"]}
            m = max(lg.values())
            ex = {o: math.exp(v - m) for o, v in lg.items()}
            s = sum(ex.values())
            p = {**p, "probs": {o: v / s for o, v in ex.items()}, "model": f"{name}_bc"}
        f.write(json.dumps(p) + "\n")
print(f"wrote {pd.name}/{name}_bc.jsonl  tasks={len(prior)}")

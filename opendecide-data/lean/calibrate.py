"""Post-hoc temperature scaling, one temperature per question type (noul / choice), fitted on dev + devzs ONLY.

Our probabilities are softmaxes over candidate-token logits, so softmax(log p / T) equals softmax(logit / T) exactly.
Writes <preds dir>/<name>_cal.jsonl for every split that has <name>.jsonl, and logs the fitted temperatures.
Usage: calibrate.py NAME [NAME ...]
"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
import os
FIT_SPLITS = os.environ.get("CAL_FIT", "dev,devzs").split(",")
APPLY_DIRS = ["preds", "preds_dev", "preds_devzs", "preds_devzs2", "preds_devp", "preds_devp_card", "preds_eval_card", "preds_eval_long", "preds_eval_multi", "preds_eval_hc", "preds_dev_hc", "preds_eval_jagged", "preds_eval_opi", "preds_pg_dev", "preds_ohs", "preds_ohs2"]
GRID = [round(0.25 + 0.05 * i, 2) for i in range(196)]  # 0.25 .. 10.0


def rj(p):
    return [json.loads(l) for l in open(p)]


def scaled(probs, T):
    ks = [k for k in probs if not k.startswith("_")]
    lg = [math.log(max(probs[k], 1e-12)) / T for k in ks]
    m = max(lg)
    ex = [math.exp(x - m) for x in lg]
    s = sum(ex)
    return {k: e / s for k, e in zip(ks, ex)}


def nll(items, T):
    tot = 0.0
    for r, p in items:
        q = scaled(p, T)
        key = ("yes" if r["gold"] == 1 else "no") if r["qtype"] == "noul" else r["gold"]
        tot -= math.log(max(q.get(key, 0.0), 1e-12))
    return tot / max(1, len(items))


for name in sys.argv[1:]:
    items = {"noul": [], "choice": []}
    for s in FIT_SPLITS:
        pf = HERE / f"preds_{s}/{name}.jsonl"
        if not pf.exists():
            sys.exit(f"missing {pf}: run the model on {s} first")
        rows = {r["id"]: r for r in rj(HERE / f"data/{s}.jsonl")}
        for p in rj(pf):
            r = rows[p["id"]]
            items[r["qtype"]].append((r, p["probs"]))
    T = {qt: min(GRID, key=lambda t: nll(it, t)) for qt, it in items.items()}
    before = {qt: round(nll(it, 1.0), 4) for qt, it in items.items()}
    after = {qt: round(nll(it, T[qt]), 4) for qt, it in items.items()}
    print(f"{name}: T={T}  dev NLL before={before} after={after}")
    for d in APPLY_DIRS:
        pf = HERE / d / f"{name}.jsonl"
        if not pf.exists():
            continue
        split = "eval" if d == "preds" else d[len("preds_"):]
        rows = {r["id"]: r for r in rj(HERE / f"data/{split}.jsonl")}
        with open(HERE / d / f"{name}_cal.jsonl", "w") as f:
            for p in rj(pf):
                r = rows[p["id"]]
                if p.get("probs"):
                    p = {**p, "probs": scaled(p["probs"], T[r["qtype"]]), "model": f"{name}_cal"}
                f.write(json.dumps(p) + "\n")
        meta = HERE / d / f"{name}.meta.json"
        if meta.exists():
            m = json.loads(meta.read_text())
            (HERE / d / f"{name}_cal.meta.json").write_text(json.dumps({**m, "temperature": T, "path": "calibrate"}, indent=2))
    (HERE / "logs").mkdir(exist_ok=True)
    (HERE / f"logs/calib_{name}.json").write_text(json.dumps({"T": T, "nll_before": before, "nll_after": after}, indent=2))

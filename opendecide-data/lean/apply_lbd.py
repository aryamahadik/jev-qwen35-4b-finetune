"""Apply chosen leverage-bounded-decoding knobs offline to saved per-variant probabilities (from eval_system, which
scores every variant), for any split. Writes <preds dir>/<LABEL>_lbd.jsonl (= the full system with those knobs).
  python apply_lbd.py LABEL TAU META_MIN split1,split2,...
"""
import json
import sys
from pathlib import Path

from tune_lbd import pick

HERE = Path(__file__).resolve().parent
if __name__ == "__main__":
    label, tau, mm, splits = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4].split(",")
    for sp in splits:
        pd = HERE / ("preds" if sp == "eval" else f"preds_{sp}")
        rows = [json.loads(l) for l in open(HERE / f"data/{sp}.jsonl")]
        infos = [json.loads(l) for l in open(pd / f"{label}_sys.infos.jsonl")]
        n_drop = 0
        with open(pd / f"{label}_lbd.jsonl", "w") as f:
            for r, i in zip(rows, infos):
                p = pick(i, tau, mm)
                n_drop += p is not i["full"]
                f.write(json.dumps({"id": r["id"], "model": f"{label}_lbd", "probs": p}) + "\n")
        (pd / f"{label}_lbd.meta.json").write_text(json.dumps({"name": f"{label}_lbd", "tau": tau, "meta_min": mm,
                                                               "dropped": n_drop, "rows": len(rows)}, indent=1))
        print(f"{sp}: dropped a segment on {n_drop}/{len(rows)} rows")

"""Synthetic results files for checking score_v154.py: oracle (Intelligence must be 100), oracle with every Noul answer
at P(yes)=0.5 (Noul CC must be -100, Intelligence 33.3), and a noisy 80 %-oracle run. Latency 0.05 s, 800 input tokens.
  python3 make_synthetic.py && python3 ../score_v154.py syn_oracle syn_abstain_noul syn_noisy --kinds gpu,gpu,gpu"""
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import v154lib as L  # noqa: E402

items = L.load_public(HERE.parent.parent / "jevbench_v154")
rng = random.Random(0)


def oracle(it):
    return {l: 1.0 if l == str(it["expected"]) else 0.0 for l in it["labels"]}


def abstain_noul(it):
    return {"no": 0.5, "yes": 0.5} if it["question"]["type"] == "noul" else oracle(it)


def noisy(it):
    ls = it["labels"]
    if rng.random() < 0.8:
        return {l: (0.9 if l == str(it["expected"]) else 0.1 / (len(ls) - 1)) for l in ls}
    w = [rng.random() for _ in ls]
    return {l: x / sum(w) for l, x in zip(ls, w)}


for name, fn in (("syn_oracle", oracle), ("syn_abstain_noul", abstain_noul), ("syn_noisy", noisy)):
    d = HERE / name
    d.mkdir(exist_ok=True)
    with open(d / "results.jsonl", "w") as f:
        for i, it in items.items():
            f.write(json.dumps({"task_id": i, "valid": True, "ok": True, "status": "ok", "probs": fn(it),
                                "latency_s": 0.05, "usage": {"input_tokens": 800, "output_tokens": 0}}) + "\n")
    (d / "manifest.json").write_text(json.dumps({"name": name, "adapter": "synthetic"}))
print("wrote", [p.name for p in HERE.glob("syn_*")])

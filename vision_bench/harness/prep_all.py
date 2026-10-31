"""CPU-only dry run over all 1,000 items: build every prompt (all views), tokenize, preprocess the image, check shapes, and push
random logits through decide()/decision_record() to check the combine code. No model, no GPU.
Run on the VM at low priority:  OMP_NUM_THREADS=1 nice -n 19 env CUDA_VISIBLE_DEVICES= PYTHONPATH=~/vision_bench/pylib python prep_all.py
"""
import json
import os
import random
import sys
import time

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import torch  # noqa: E402

import vb_core as vb  # noqa: E402

torch.set_num_threads(1)
out = {}
for which in (sys.argv[1:] or ["c1", "base"]):
    rd = vb.Reader(which, load_model=False)
    cases = vb.load_cases()
    stats = {"n": 0, "errors": [], "max_tokens": 0, "n_tokens": [], "n_img": [], "prep_ms": [], "by_suite": {}}
    rng = random.Random(0)
    for c in cases:
        qid, q = next(iter(c["questions"].items()))
        try:
            raw = open(c["_image_file"], "rb").read()
            t0 = time.perf_counter()
            p = rd.prepare(raw, q)
            ms = (time.perf_counter() - t0) * 1000
            assert len(p["groups"]) == (2 if q["type"] == "noul" else len(vb.bench_options(q))), "groups"
            assert all(len(g) >= 1 for g in p["groups"]), "empty candidate group"
            assert len({len(s) for s in p["seqs"]}) <= 2
            lg = [torch.tensor([rng.gauss(0, 3) for _ in p["groups"]]) for _ in p["views"]]
            probs = rd.decide(p, lg)
            assert abs(sum(probs) - 1) < 1e-5 and len(probs) == len(vb.bench_options(q)), "probs"
            rec = vb.decision_record(q, None, probs)
            assert rec["probabilities"], "record"
            mx = max(len(s) for s in p["seqs"])
            stats["max_tokens"] = max(stats["max_tokens"], mx)
            stats["n_tokens"].append(mx)
            stats["n_img"].append(p["n_img"])
            stats["prep_ms"].append(ms)
            s = stats["by_suite"].setdefault(c["suite"], {"n": 0, "max_tokens": 0, "views": len(p["views"]), "n_options": len(vb.bench_options(q))})
            s["n"] += 1
            s["max_tokens"] = max(s["max_tokens"], mx)
            stats["n"] += 1
        except Exception as e:  # noqa: BLE001
            stats["errors"].append(f"{c['id']}: {type(e).__name__}: {str(e)[:150]}")
    xs = sorted(stats["prep_ms"])
    stats["prep_ms_p50"], stats["prep_ms_p95"] = xs[len(xs) // 2], xs[int(len(xs) * 0.95)]
    stats["tokens_mean"] = sum(stats["n_tokens"]) / len(stats["n_tokens"])
    stats["img_tokens_mean"] = sum(stats["n_img"]) / len(stats["n_img"])
    stats["img_tokens_max"] = max(stats["n_img"])
    for k in ("n_tokens", "n_img", "prep_ms"):
        del stats[k]
    out[which] = stats
print(json.dumps(out, indent=1))

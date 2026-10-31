import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
"""The REAL harness code (tt.Reader, route 'causal') on the REAL Qwen3.5-4B + REAL C1 adapter, on CPU (bf16), for a few real decisions:
model class and adapter proof, a padded batch of different-length sequences == the same sequences read one by one (the padding/mask
check on real weights), LoRA on != off, probabilities sum to 1, and C1 reads easy items right. Small on purpose (the Mac's CPU
runs Qwen3.5's linear attention through slow, memory-hungry torch fallbacks). The 77-way two-letter-label candidate groups are
checked without the model."""
import json, os, sys, time
os.environ["TT_TOKEN_BUDGET"] = "1536"; os.environ["TT_MAX_BATCH"] = "3"
from common import *
import torch
torch.set_num_threads(8)
import tt_core as tt
t0 = time.time()
rd = tt.Reader(dev="cpu")
print("loaded", type(rd.top).__name__, f"{rd.load_s:.1f}s", rd.adapter_check, flush=True)
assert type(rd.top).__name__ == "Qwen3_5ForCausalLM" and rd.adapter_check["n_lora_B_nonzero"] == 248
ds = tt.load_decisions()
b77 = rd.prepare_many([d for d in ds if d["suite"] == "banking77"][:2], "main")
for p in b77:
    assert len(p["groups"]) == 77 and len({t for g in p["groups"] for t in g}) == sum(len(g) for g in p["groups"])
    assert all(len(g) >= 1 for g in p["groups"]) and len(p["seqs"]) == 2
print("banking77: 77 distinct candidate groups per view, 2 views OK", flush=True)
pick = [d for d in ds if d["suite"] == "sst2"][:3] + [d for d in ds if d["suite"] == "ag_news"][:1]
preps = rd.prepare_many(pick, "main")
jobs = [(s, p["groups"]) for p in preps for s in p["seqs"]]
print(len(pick), "decisions,", len(jobs), "sequences, tokens", [len(j[0]) for j in jobs], flush=True)
worst = 0.0
for arm in ("c1", "base"):
    with rd.arm(arm):
        bat, st = rd.read_jobs(jobs)                    # padded batches of up to 3 sequences (lengths 213..302 -> padded to 256/384)
        one = [rd.read_jobs([j])[0][0] for j in jobs] if arm == "c1" else None
    print(arm, "batched stats", st, flush=True)
    k = 0
    for p in preps:
        n = len(p["seqs"]); pb = rd.decide(p, bat[k:k + n])
        line = f"  {arm:4s} {p['d']['suite']:8s} gold {p['d']['gold']} pred {max(range(len(pb)), key=pb.__getitem__)} probs {[round(x, 3) for x in pb]}"
        if one is not None:
            p1 = rd.decide(p, one[k:k + n]); d = max(abs(a - b) for a, b in zip(pb, p1)); worst = max(worst, d); line += f" |batched-single| {d:.4f}"
            assert d < 0.05
        print(line, flush=True); k += n
        assert abs(sum(pb) - 1) < 1e-4
print("worst |batched - single| probability difference (C1):", worst)
eff = rd.adapter_effect(preps[:1]); print("adapter effect (max logit diff on vs off)", eff); assert eff > 1e-3
print("REAL MODEL CPU TEST PASSED", f"{time.time() - t0:.0f}s")

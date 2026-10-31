import os as _o, sys as _s; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
"""Dry run of the REAL run_text.py stages (gates, main, lat, diag) on a tiny random Qwen3.5 text-only model with the REAL tokenizer and
the real C1 prompts for ALL 4,850 decisions, on CPU (torch.cuda calls patched). The tiny random LoRA is attached through
adapter_gate.attach_c1_adapter_native exactly as Reader does, and the whole output then goes through score_text.py (which runs the
bench's own score.py) and the skeptic. Includes: a forced failure that must be retried and flagged, and a forced OOM split.
Writes only under tests/tmp_run."""
import json, os, shutil, sys, types
from common import *
import torch, transformers
for n in ("synchronize", "empty_cache", "reset_peak_memory_stats"):
    setattr(torch.cuda, n, lambda *a, **k: None)
torch.cuda.max_memory_allocated = lambda *a, **k: 0
torch.cuda.get_device_name = lambda *a, **k: "CPU-dry-run"
os.environ["TT_TOKEN_BUDGET"] = "12288"; os.environ["TT_MAX_BATCH"] = "8"
import tt_core as tt, run_text as rt, adapter_gate as ag
from transformers import AutoModelForCausalLM
from peft import LoraConfig, get_peft_model
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tiny_common import tiny_config
OUT = f"{TT}/tests/tmp_run"; shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
rt.LAT_PER_SUITE, rt.LAT_WARM = 2, 2
rd = tt.Reader(dev="cpu", load_model=False)
tok = rd.tok
cfg = tiny_config(); cfg.text_config.vocab_size = len(tok) + 8; cfg.text_config.eos_token_id = tok.eos_token_id or 1
torch.manual_seed(0)
BASE = f"{OUT}/base"; AutoModelForCausalLM.from_config(cfg).save_pretrained(BASE)
REGEX = r".*layers\.\d+\..*\.(q_proj|k_proj|v_proj|o_proj|gate_proj|up_proj|down_proj|out_proj|in_proj[a-z_]*)"
pt = get_peft_model(AutoModelForCausalLM.from_pretrained(BASE), LoraConfig(r=4, lora_alpha=8, target_modules=REGEX, task_type="CAUSAL_LM"))
for n, p in pt.named_parameters():
    if "lora_B" in n: torch.nn.init.normal_(p, std=0.3)
pt.save_pretrained(f"{OUT}/trained_adapter")
model = AutoModelForCausalLM.from_pretrained(BASE)
assert type(model).__name__ == "Qwen3_5ForCausalLM"
pm, chk = ag.attach_c1_adapter_native(model, f"{OUT}/trained_adapter")
print("adapter check on the tiny adapter (native keys):", chk)
rd.model, rd.adapter_check = pm.eval(), chk
rd.top = pm.get_base_model(); rd.body, rd.head = rd.top.model, rd.top.lm_head
rd.dev, rd.load_s, rd.route = "cpu", 0.0, "causal"
NPER = 6
ds = tt.load_decisions(max_cases=NPER)
a = types.SimpleNamespace(deadline_s=None, max_cases=NPER, min_sst2_acc=0.0, min_conf_diff=0.0)
out = rt.Out(f"{OUT}/results")
mt = rt.meta(rd, a, ds); out.json("meta.json", mt)
preps = rt.gates(rd, a, ds, out)
g = json.load(open(f"{OUT}/results/gates.json"))
assert g["tokenizers_identical_on_all_prompts"]["n_decisions"] == len(ds), g
# forced failure: the first suite's first read raises once -> retried and flagged; OOM split on a later batch
real = rd._run_batch; st = {"n": 0}
def flaky(idx, jobs, o):
    st["n"] += 1
    if st["n"] == 3: raise RuntimeError("synthetic failure")
    if st["n"] == 9 and len(idx) > 1: raise torch.cuda.OutOfMemoryError("synthetic OOM")
    return real(idx, jobs, o)
rd._run_batch = flaky
rt.main_stage(rd, a, ds, preps, out, ["c1", "base"])
rd._run_batch = real
sm = json.load(open(f"{OUT}/results/summary_main.json"))
print("oom splits", sm["c1"]["oom_splits"] + sm["base"]["oom_splits"], "| retried records:",
      sum(1 for arm in ("c1", "base") for l in open(f"{OUT}/results/preds_{arm}.jsonl") if json.loads(l).get("retried")))
assert sm["c1"]["oom_splits"] + sm["base"]["oom_splits"] >= 1
rt.lat_stage(rd, a, ds, out, ["c1", "base"])
rt.diag_stage(rd, a, ds, out, ["c1", "base"])
n_main = sum(1 for _ in open(f"{OUT}/results/preds_c1.jsonl")); assert n_main == len(ds), n_main
retried = [json.loads(l) for l in open(f"{OUT}/results/preds_c1.jsonl") if json.loads(l).get("retried")]
assert not any("error" in r for r in retried)
nd = sum(1 for _ in open(f"{OUT}/results/diag_c1.jsonl")); exp = sum(1 for d in ds if d["q"]["type"] == "score") + sum(1 for d in ds if d["q"]["type"] == "noul"); assert nd == exp, (nd, exp)
c1 = {(json.loads(l)["id"], json.loads(l)["qid"]): json.loads(l) for l in open(f"{OUT}/results/preds_c1.jsonl")}
bs = {(json.loads(l)["id"], json.loads(l)["qid"]): json.loads(l) for l in open(f"{OUT}/results/preds_base.jsonl")}
diff = sum(1 for k in c1 if c1[k]["pred"] != bs[k]["pred"]); print("C1 and base answers differ on", diff, "of", len(c1))
assert diff > 0.05 * len(c1), diff
print("RUN_TEXT STAGES OK")

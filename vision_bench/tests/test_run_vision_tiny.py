"""Dry run of the REAL run_vision.py stages (meta gates, smoke, eval: warm / timed + retry / diagnostics / throughput / localhost HTTP)
on a tiny random Qwen3.5 composite with the REAL tokenizer, a stub image processor, no GPU (torch.cuda calls patched to no-ops).
The C1 LoRA is attached through vb_core.attach_c1_adapter exactly as the Reader does. Then the output goes through score_vision.
Writes only under tests/tmp_run."""
import json, os, shutil, sys, types
HERE = os.path.dirname(os.path.abspath(__file__)); VB = os.path.dirname(HERE)
NPER = int(os.environ.get("NPER", "6"))
sys.path.insert(0, f"{VB}/harness"); sys.path.insert(0, HERE)
os.environ.update(HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1", VB_PROC_DIR=f"{VB}/src/qwen35-4b-processor")
import torch, transformers
for n in ("synchronize", "empty_cache", "reset_peak_memory_stats"):
    setattr(torch.cuda, n, lambda *a, **k: None)
torch.cuda.max_memory_allocated = lambda *a, **k: 0
torch.cuda.get_device_name = lambda *a, **k: "CPU-dry-run"
class FakeIm:
    size = (640, 480)
    def load(self): pass
    def convert(self, m): return self
class StubProc:
    merge_size = 2
    def __call__(self, images, return_tensors):
        return {"pixel_values": torch.randn(24, 1536), "image_grid_thw": torch.tensor([[1, 4, 6]])}
class StubAIP:
    @staticmethod
    def from_pretrained(path): return StubProc()
transformers.AutoImageProcessor = StubAIP
fp = types.ModuleType("PIL"); fi = types.ModuleType("PIL.Image"); fi.open = lambda b: FakeIm(); fp.Image = fi
sys.modules["PIL"] = fp; sys.modules["PIL.Image"] = fi
import vb_core as vb
import run_vision as rv
vb.ADAPTER = "/Users/aryamahadik/Documents/jev/backups/modal_models/q35_4b_main500k"   # tokenizer, train_meta, sha gate
OUT = f"{HERE}/tmp_run"; shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
vb.ADAPTER_RENAMED = f"{OUT}/renamed"

orig = vb.load_cases
def small(*a, **k):
    cnt, out = {}, []
    for c in orig(*a, **k):
        if cnt.get(c["suite"], 0) < NPER:
            out.append(c); cnt[c["suite"]] = cnt.get(c["suite"], 0) + 1
    return out
vb.load_cases = small

from tiny_common import tiny_config
from transformers import AutoModelForCausalLM, AutoModelForImageTextToText
from peft import LoraConfig, get_peft_model
sys.modules["transformers"].AutoImageProcessor = StubAIP   # importing peft swaps the module object that `from transformers import ...` reads
rd = vb.Reader("c1", load_model=False)
tok = rd.tok
cfg = tiny_config()
cfg.text_config.vocab_size = len(tok) + 8
cfg.image_token_id = tok.convert_tokens_to_ids("<|image_pad|>")
cfg.vision_start_token_id = tok.convert_tokens_to_ids("<|vision_start|>"); cfg.vision_end_token_id = tok.convert_tokens_to_ids("<|vision_end|>")
cfg.text_config.eos_token_id = tok.eos_token_id or 1
torch.manual_seed(0)
BASE = f"{OUT}/base"; AutoModelForImageTextToText.from_config(cfg).save_pretrained(BASE)
REGEX = r".*layers\.\d+\..*\.(q_proj|k_proj|v_proj|o_proj|gate_proj|up_proj|down_proj|out_proj|in_proj[a-z_]*)"
pt = get_peft_model(AutoModelForCausalLM.from_pretrained(BASE), LoraConfig(r=4, lora_alpha=8, target_modules=REGEX, task_type="CAUSAL_LM"))
for n, p in pt.named_parameters():
    if "lora_B" in n: torch.nn.init.normal_(p, std=0.05)
pt.save_pretrained(f"{OUT}/trained_adapter")
model = AutoModelForImageTextToText.from_pretrained(BASE)
pm, chk = vb.attach_c1_adapter(model, f"{OUT}/trained_adapter", vb.ADAPTER_RENAMED)
vb.ADAPTER_N_TENSORS, vb.ADAPTER_N_LORA_B = chk["n_tensors"], chk["n_lora_B"]     # the tiny adapter's counts stand in for 496 / 248
rd.model, rd.adapter_check = pm.eval(), chk
rd.top = pm.get_base_model(); rd.inner, rd.head, rd.cfg = rd.top.model, rd.top.lm_head, rd.top.config
rd.dev, rd.load_s = "cpu", 0.0
assert rd.image_token_id == rd.cfg.image_token_id

class Dev:  # run_vision calls vb.sync() with the default dev
    pass
rv.smoke(rd, OUT)
sm = json.load(open(f"{OUT}/smoke_c1.json"))
assert sm["checks"]["adapter_effect_max_logit_diff_on_vs_off"] > 1e-3 and sm["checks"]["adapter_check"]["n_lora_B_nonzero"] == chk["n_lora_B"]
assert len(sm["diag_items"]) == 6
# force one failure to exercise the retry path (fails once, passes on the retry)
orig_prepare = rd.prepare; state = {"n": 0}
def flaky(raw, q, variant="main"):
    state["n"] += 1
    if state["n"] == 5 * NPER + 5 and variant == "main": raise RuntimeError("synthetic OOM")
    return orig_prepare(raw, q, variant)
rd.prepare = flaky
rv.eval_all(rd, OUT, do_e2e=True)
rd.prepare = orig_prepare
for f in ("meta_c1.json", "preds_c1.jsonl", "preds_c1_warm.jsonl", "diag_c1.jsonl", "summary_c1.json", "e2e_c1.json"):
    assert os.path.exists(f"{OUT}/{f}"), f
rows = [json.loads(l) for l in open(f"{OUT}/preds_c1.jsonl")]
print("rows", len(rows), "errors", sum("error" in r for r in rows), "retried", sum(bool(r.get("retried")) for r in rows))
dg = [json.loads(l) for l in open(f"{OUT}/diag_c1.jsonl")]
print("diag rows", len(dg), {v: sum(r["variant"] == v for r in dg) for v in ("count_prefixed", "yn_swapped")})
assert len(rows) == 5 * NPER and len(dg) == 3 * NPER
rt = [r for r in rows if r.get("retried")]
assert len(rt) == 1 and "error" not in rt[0] and "synthetic OOM" in rt[0]["first_error"], rt
print("retry path OK:", rt[0]["id"], rt[0]["first_error"])
# scorer on a mini data tree with the same ids
MINI = f"{OUT}/mini"
for s in vb.SUITES:
    os.makedirs(f"{MINI}/data/{s}")
    with open(f"{MINI}/data/{s}/cases.jsonl", "w") as f:
        for c in vb.load_cases([s]):
            c = {k: v for k, v in c.items() if k != "_image_file"}; f.write(json.dumps(c) + "\n")
import subprocess
r = subprocess.run([sys.executable, "-I", f"{VB}/harness/score_vision.py"], capture_output=True, text=True, env={**os.environ, "VB_ROOT": MINI, "VB_RESULTS": OUT})
print(r.stdout[-3800:], r.stderr[-1500:]); assert r.returncode == 0
print("RUN_VISION DRY RUN PASSED")

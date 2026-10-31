"""CPU test of the adapter fix on a tiny random Qwen3.5 composite (transformers 5.17, peft 0.21, the VM versions).
C1 was trained on the text-only class, so its adapter keys read 'base_model.model.model.layers.N...'. Checks:
  1. the OLD load (PeftModel.from_pretrained straight on the multimodal class) leaves every lora_B at zero  -> verify_adapter_loaded RAISES
  2. the FIXED load (vb_core.attach_c1_adapter: renamed copy) loads every tensor bit for bit               -> verify passes
  3. fixed logits == trained-side logits (CausalLM + PeftModel); and differ from base (adapter on vs off)
  4. a deliberately corrupted adapter (one B zeroed after loading) is caught by verify_adapter_loaded."""
import os, sys, shutil, warnings
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "harness"))
os.environ["HF_HUB_OFFLINE"] = "1"
import torch
from tiny_common import tiny_config
from transformers import AutoModelForCausalLM, AutoModelForImageTextToText
from peft import LoraConfig, PeftModel, get_peft_model
import vb_core as vb

TMP = os.path.join(HERE, "tmp_adapter"); shutil.rmtree(TMP, ignore_errors=True); os.makedirs(TMP)
BASE, AD, RENAMED = f"{TMP}/base", f"{TMP}/adapter", f"{TMP}/renamed"
torch.manual_seed(0)
AutoModelForImageTextToText.from_config(tiny_config()).save_pretrained(BASE)
REGEX = r".*layers\.\d+\..*\.(q_proj|k_proj|v_proj|o_proj|gate_proj|up_proj|down_proj|out_proj|in_proj[a-z_]*)"  # the real adapter_config's
mt = AutoModelForCausalLM.from_pretrained(BASE)
pm_t = get_peft_model(mt, LoraConfig(r=4, lora_alpha=8, target_modules=REGEX, task_type="CAUSAL_LM"))
for n, p in pm_t.named_parameters():
    if "lora_B" in n:
        torch.nn.init.normal_(p, std=0.05)
pm_t.save_pretrained(AD)
ids = torch.randint(10, 390, (1, 12))
with torch.no_grad():
    ref = pm_t.eval()(input_ids=ids).logits
    base = AutoModelForImageTextToText.from_pretrained(BASE)(input_ids=ids).logits

# 1. old load -> must be caught
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    old = PeftModel.from_pretrained(AutoModelForImageTextToText.from_pretrained(BASE), AD)
_, sd_new = vb.build_renamed_adapter(AD, f"{TMP}/scratch_rename")
try:
    vb.verify_adapter_loaded(old, sd_new)
    print("FAIL 1: the broken load was NOT caught"); sys.exit(1)
except AssertionError as e:
    print("1 OK old load caught:", str(e)[:230])
with torch.no_grad():
    print("  old-load logits equal base:", float((old.eval()(input_ids=ids).logits - base).abs().max()) == 0.0)

# 2. fixed load
pm, chk = vb.attach_c1_adapter(AutoModelForImageTextToText.from_pretrained(BASE), AD, RENAMED)
print("2 OK fixed load verified:", chk)
assert chk["n_no_home"] == 0 and chk["n_unequal_to_file"] == 0 and chk["n_lora_B"] == chk["n_lora_B_nonzero"] > 0

# 3. numerics
with torch.no_grad():
    fixed = pm.eval()(input_ids=ids).logits
    with pm.disable_adapter():
        off = pm(input_ids=ids).logits
d_ref, d_base, d_off = (float((fixed - ref).abs().max()), float((fixed - base).abs().max()), float((off - base).abs().max()))
print(f"3 fixed vs trained-side {d_ref:.2e} | fixed vs base {d_base:.3f} | adapter-off vs base {d_off:.2e}")
assert d_ref < 1e-5 and d_base > 0.05 and d_off < 1e-6

# 4. corruption is caught
with torch.no_grad():
    for n, p in pm.named_parameters():
        if "lora_B" in n:
            p.zero_(); break
try:
    vb.verify_adapter_loaded(pm, sd_new); print("FAIL 4"); sys.exit(1)
except AssertionError as e:
    print("4 OK corruption caught:", str(e)[:200])
print("ALL ADAPTER TESTS PASSED")

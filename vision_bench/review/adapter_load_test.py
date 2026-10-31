"""Does the way vision_bench loads C1 (AutoModelForImageTextToText + PeftModel.from_pretrained) actually apply an adapter that was
trained the way C1 was (decoder_io.load -> AutoModelForCausalLM -> text-only keys 'base_model.model.model.layers.N...')?
Tiny random model, same transformers 5.17 / peft 0.21 as the VM. Everything is written under review/tmp."""
import logging, os, shutil, sys, warnings
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/vision_bench/review")
os.environ["HF_HUB_OFFLINE"] = "1"
import torch, transformers, peft, json
from tiny_common import tiny_config
from transformers import AutoModelForCausalLM, AutoModelForImageTextToText
from peft import LoraConfig, PeftModel, get_peft_model
from safetensors import safe_open

TMP = "/Users/aryamahadik/Documents/jev/vision_bench/review/tmp"
shutil.rmtree(TMP, ignore_errors=True); os.makedirs(TMP)
BASE, AD = f"{TMP}/base", f"{TMP}/adapter"
print("transformers", transformers.__version__, "peft", peft.__version__, "torch", torch.__version__)
torch.manual_seed(0)
m0 = AutoModelForImageTextToText.from_config(tiny_config())
m0.save_pretrained(BASE)

# --- how C1 was trained/merged: decoder_io.load tries AutoModelForCausalLM first
mt = AutoModelForCausalLM.from_pretrained(BASE)
print("training-side class:", type(mt).__name__, "| first names:", [n for n, _ in mt.named_parameters()][:2])
REGEX = r".*layers\.\d+\..*\.(q_proj|k_proj|v_proj|o_proj|gate_proj|up_proj|down_proj|out_proj|in_proj[a-z_]*)"  # the real adapter_config
pm = get_peft_model(mt, LoraConfig(r=4, lora_alpha=8, target_modules=REGEX, task_type="CAUSAL_LM"))
for n, p in pm.named_parameters():
    if "lora_B" in n:
        torch.nn.init.normal_(p, std=0.05)   # a "trained" adapter: non-zero B
pm.save_pretrained(AD)
f = safe_open(f"{AD}/adapter_model.safetensors", "pt")
ks = list(f.keys())
print("adapter keys:", len(ks), ks[:2])

# --- how vision_bench loads it
rec = []
class H(logging.Handler):
    def emit(self, r): rec.append(r.getMessage())
for name in ("peft",):
    lg = logging.getLogger(name); lg.addHandler(H()); lg.setLevel(logging.INFO)
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    mv = AutoModelForImageTextToText.from_pretrained(BASE)
    pv = PeftModel.from_pretrained(mv, AD)
print("warnings/logs while loading:", [str(x.message)[:200] for x in w], [r[:300] for r in rec if "adapter" in r.lower() or "missing" in r.lower() or "unexpected" in r.lower()])
loraB = {n: p for n, p in pv.named_parameters() if "lora_B" in n}
nz = sum(int(p.abs().sum() > 0) for p in loraB.values())
print(f"vision_bench-style load: {len(loraB)} lora_B tensors injected, {nz} non-zero  -> adapter applied: {nz == len(loraB)}")
print("example injected name:", next(iter(loraB)))

# --- numeric effect on a text-only forward
ids = torch.randint(10, 390, (1, 12))
with torch.no_grad():
    base_logits = AutoModelForImageTextToText.from_pretrained(BASE)(input_ids=ids).logits
    pv.eval(); ad_logits = pv(input_ids=ids).logits
    ref = PeftModel.from_pretrained(AutoModelForCausalLM.from_pretrained(BASE), AD).eval()(input_ids=ids).logits  # the trained-side path
print("max |logit(vision_bench load) - logit(base)|   :", float((ad_logits - base_logits).abs().max()))
print("max |logit(trained-side load) - logit(base)|   :", float((ref - base_logits).abs().max()))
print("max |logit(vision_bench load) - logit(trained-side)|:", float((ad_logits - ref).abs().max()))

# ---- candidate fixes, same tiny setup
def applied(pm_):
    b = [p for n, p in pm_.named_parameters() if "lora_B" in n]
    return sum(int(p.abs().sum() > 0) for p in b), len(b)
try:
    pk = PeftModel.from_pretrained(AutoModelForImageTextToText.from_pretrained(BASE), AD,
                                   key_mapping={r"^base_model\.model\.model\.layers\.": "base_model.model.model.language_model.layers."})
    with torch.no_grad():
        lk = pk.eval()(input_ids=ids).logits
    print("fix A (PeftModel.from_pretrained key_mapping): non-zero lora_B", applied(pk), "| max diff vs trained-side:", float((lk - ref).abs().max()))
except Exception as e:
    print("fix A failed:", type(e).__name__, str(e)[:200])
# fix B: rename the keys in a copy of the adapter file
from safetensors.torch import load_file, save_file
sd = load_file(f"{AD}/adapter_model.safetensors")
sd2 = {k.replace("base_model.model.model.layers.", "base_model.model.model.language_model.layers."): v for k, v in sd.items()}
os.makedirs(f"{TMP}/adapter_renamed", exist_ok=True)
save_file(sd2, f"{TMP}/adapter_renamed/adapter_model.safetensors"); shutil.copy(f"{AD}/adapter_config.json", f"{TMP}/adapter_renamed/")
pb = PeftModel.from_pretrained(AutoModelForImageTextToText.from_pretrained(BASE), f"{TMP}/adapter_renamed")
with torch.no_grad():
    lb = pb.eval()(input_ids=ids).logits
print("fix B (renamed key copy): non-zero lora_B", applied(pb), "| max diff vs trained-side:", float((lb - ref).abs().max()))

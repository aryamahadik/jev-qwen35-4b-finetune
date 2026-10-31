"""Real C1 adapter file (the Mac backup copy; sha256 must start 507d1c29) vs the REAL Qwen3.5-4B architecture on the meta device
(no weights, no GPU): after build_renamed_adapter, every one of the 496 tensors maps to an injected LoRA parameter of the multimodal
class, and every injected LoRA parameter has a tensor. Values are compared with the original file tensor by tensor."""
import hashlib, os, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "harness"))
os.environ["HF_HUB_OFFLINE"] = "1"
import torch
from transformers import AutoConfig, AutoModelForImageTextToText
from peft import PeftConfig, get_peft_model
import vb_core as vb

SRC = os.environ.get("VB_TEST_ADAPTER", "/Users/aryamahadik/Documents/jev/backups/modal_models/q35_4b_main500k")
sha = hashlib.sha256(open(f"{SRC}/adapter_model.safetensors", "rb").read()).hexdigest()
print("adapter sha256", sha[:8]); assert sha.startswith("507d1c29")
DST = os.environ.get("VB_TEST_DST", os.path.join(HERE, "tmp_real_renamed")); shutil.rmtree(DST, ignore_errors=True)
sd, sd2 = vb.build_renamed_adapter(SRC, DST)
print("tensors", len(sd2), "lora_B", sum(".lora_B." in k for k in sd2)); assert len(sd2) == vb.ADAPTER_N_TENSORS and sum(".lora_B." in k for k in sd2) == vb.ADAPTER_N_LORA_B
assert all(torch.equal(sd[k], sd2[vb.KEY_NEW + k[len(vb.KEY_OLD):]]) for k in sd), "values changed by the rename"
cfg = AutoConfig.from_pretrained(os.environ.get("VB_TEST_CONFIG", "/Users/aryamahadik/Documents/jev/vision_bench/src/qwen35-4b-config"))
with torch.device("meta"):
    m = AutoModelForImageTextToText.from_config(cfg, dtype=torch.bfloat16)
pm = get_peft_model(m, PeftConfig.from_pretrained(DST))
lora = {n for n, _ in pm.named_parameters() if "lora_" in n}
mapped = {k.replace(".lora_A.weight", ".lora_A.default.weight").replace(".lora_B.weight", ".lora_B.default.weight") for k in sd2}
print("injected LoRA params", len(lora), "| file tensors mapped", len(mapped), "| in file but no home", len(mapped - lora), "| injected but not in file", len(lora - mapped))
assert lora == mapped
assert not any("visual" in n for n in lora), "LoRA must not touch the vision tower"
# shape check too
shapes = {n: tuple(p.shape) for n, p in pm.named_parameters() if "lora_" in n}
bad = [k for k, t in sd2.items() if shapes[k.replace(".lora_A.weight", ".lora_A.default.weight").replace(".lora_B.weight", ".lora_B.default.weight")] != tuple(t.shape)]
print("shape mismatches", len(bad)); assert not bad
print("REAL ADAPTER NAME/SHAPE TEST PASSED")

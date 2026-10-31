"""Real C1 adapter (backup copy, sha256 507d1c29...) against the REAL Qwen3.5-4B architecture, built on the meta device (no weights, no GPU):
which adapter tensors find a home in (a) Qwen3_5ForConditionalGeneration, as vision_bench loads it, (b) Qwen3_5ForCausalLM, as C1 was trained."""
import hashlib, os, sys, warnings
os.environ["HF_HUB_OFFLINE"] = "1"
import torch, transformers, peft
from transformers import AutoConfig, AutoModelForCausalLM, AutoModelForImageTextToText
from peft import PeftConfig, get_peft_model
from peft.utils import load_peft_weights, set_peft_model_state_dict
AD = "/Users/aryamahadik/Documents/jev/backups/modal_models/q35_4b_main500k"
print("adapter sha256", hashlib.sha256(open(f"{AD}/adapter_model.safetensors", "rb").read()).hexdigest()[:8], "| transformers", transformers.__version__, "peft", peft.__version__)
cfg = AutoConfig.from_pretrained("/Users/aryamahadik/Documents/jev/vision_bench/src/qwen35-4b-config")
pc = PeftConfig.from_pretrained(AD)
w = load_peft_weights(AD, device="cpu")
print("adapter tensors:", len(w), "e.g.", next(iter(w)))
def probe(label, ctor, conf):
    with torch.device("meta"):
        m = ctor(conf, dtype=torch.bfloat16)
    pm = get_peft_model(m, pc)
    inj = [n for n, _ in pm.named_parameters() if "lora_" in n]
    with warnings.catch_warnings(record=True) as ws:
        warnings.simplefilter("always")
        res = set_peft_model_state_dict(pm, w)
    mk = [k for k in (res.missing_keys or []) if "lora_" in k]
    uk = res.unexpected_keys or []
    print(f"{label}: {type(m).__name__}: lora params injected {len(inj)}, adapter tensors w/o a home (unexpected) {len(uk)}, "
          f"injected lora params left UNLOADED (missing) {len(mk)}; e.g. injected '{inj[0]}'; warning: {[str(x.message)[:90] for x in ws][:1]}")
probe("vision_bench loads C1 as", AutoModelForImageTextToText.from_config, cfg)
probe("C1 was trained/merged as", AutoModelForCausalLM.from_config, cfg.text_config)

# ---- candidate fix: rename 'model.layers.' -> 'model.language_model.layers.' in the adapter state dict before loading into the multimodal class
w2 = {k.replace("base_model.model.model.layers.", "base_model.model.model.language_model.layers."): v for k, v in w.items()}
w = w2
probe("FIX (renamed keys) into", AutoModelForImageTextToText.from_config, cfg)

"""The C1 LoRA safety checks, copied VERBATIM from the reviewed vision harness (harness/vb_core.py, lines build_renamed_adapter,
verify_adapter_loaded, attach_c1_adapter). tests/test_adapter_gate_identical.py asserts the source text of each function is
identical to the vision harness's, so there is one reviewed implementation, not two.

Why it matters: C1 was trained as the text-only class (Qwen3_5ForCausalLM), so its 496 adapter tensors are named
"base_model.model.model.layers.N...". Loaded on the multimodal class, peft only warns and leaves every lora_B at zero (the LoRA is
silently NOT applied). The text track loads C1 on the text-only class, where the native names fit; verify_adapter_loaded then
proves, tensor by tensor, that the injected LoRA parameters are bit-equal to the file and that all 248 lora_B are non-zero. The
renaming path (multimodal class) is kept and tested: on the real weights both routes give identical logits (max diff 0.0 on CPU,
tests/logs/class_equivalence.txt).
"""
from __future__ import annotations

import os
import shutil

import torch

KEY_OLD = "base_model.model.model.layers."
KEY_NEW = "base_model.model.model.language_model.layers."
ADAPTER_N_TENSORS, ADAPTER_N_LORA_B = 496, 248   # the real C1 adapter: 248 A + 248 B (language-model layers only)


def build_renamed_adapter(src, dst):
    """Write a copy of the adapter under dst whose keys land in the multimodal class. Values are untouched.
    Returns (original state dict, renamed state dict). Refuses an adapter with any key outside the text-only layout."""
    from safetensors.torch import load_file, save_file
    sd = load_file(os.path.join(src, "adapter_model.safetensors"))
    bad = [k for k in sd if not k.startswith(KEY_OLD)]
    assert not bad, f"adapter keys not in the expected text-only layout: {bad[:3]}"
    sd2 = {KEY_NEW + k[len(KEY_OLD):]: v.contiguous() for k, v in sd.items()}
    assert len(sd2) == len(sd)
    os.makedirs(dst, exist_ok=True)
    save_file(sd2, os.path.join(dst, "adapter_model.safetensors"), metadata={"format": "pt"})
    shutil.copy(os.path.join(src, "adapter_config.json"), os.path.join(dst, "adapter_config.json"))
    return sd, sd2


def verify_adapter_loaded(pm, sd_new, expect_tensors=None, expect_b=None):
    """Every tensor of the (renamed) adapter file must sit, bit for bit, in the injected LoRA parameter it belongs to; no injected
    LoRA parameter may be left without a file tensor; every lora_B must be non-zero. Raises AssertionError otherwise."""
    params = dict(pm.named_parameters())
    lora = [n for n in params if "lora_" in n]
    n_b = n_b_nonzero = n_nohome = n_unequal = 0
    seen = set()
    for k, t in sd_new.items():
        pk = k.replace(".lora_A.weight", ".lora_A.default.weight").replace(".lora_B.weight", ".lora_B.default.weight")
        p = params.get(pk)
        is_b = ".lora_B." in k
        n_b += is_b
        if p is None:
            n_nohome += 1
            continue
        seen.add(pk)
        if not torch.equal(p.detach().cpu().float(), t.to(p.dtype).float()):
            n_unequal += 1
        if is_b and float(p.detach().abs().sum()) > 0:
            n_b_nonzero += 1
    chk = {"n_tensors": len(sd_new), "n_lora_B": n_b, "n_lora_B_nonzero": n_b_nonzero, "n_no_home": n_nohome,
           "n_unequal_to_file": n_unequal, "n_model_lora_params": len(lora), "n_model_lora_params_not_in_file": len(set(lora) - seen)}
    assert chk["n_no_home"] == 0 and chk["n_unequal_to_file"] == 0 and chk["n_model_lora_params_not_in_file"] == 0, chk
    assert chk["n_lora_B"] > 0 and chk["n_lora_B_nonzero"] == chk["n_lora_B"], chk
    if expect_tensors is not None:
        assert chk["n_tensors"] == expect_tensors, chk
    if expect_b is not None:
        assert chk["n_lora_B"] == expect_b and chk["n_lora_B_nonzero"] == expect_b, chk
    return chk


def attach_c1_adapter(model, src, dst, expect_tensors=None, expect_b=None):
    """Load the C1 LoRA into the multimodal model through the renamed copy and prove it landed. Returns (PeftModel, check dict)."""
    from peft import PeftModel
    _, sd_new = build_renamed_adapter(src, dst)
    pm = PeftModel.from_pretrained(model, dst)
    return pm, verify_adapter_loaded(pm, sd_new, expect_tensors, expect_b)


def attach_c1_adapter_native(model, src, expect_tensors=None, expect_b=None):
    """Text-only class: the adapter's own key names fit, no renaming. The same proof runs against the file as it is.
    Returns (PeftModel, check dict)."""
    from peft import PeftModel
    from safetensors.torch import load_file
    sd = load_file(os.path.join(src, "adapter_model.safetensors"))
    pm = PeftModel.from_pretrained(model, src)
    return pm, verify_adapter_loaded(pm, sd, expect_tensors, expect_b)

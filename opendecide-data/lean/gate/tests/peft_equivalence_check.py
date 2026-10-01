"""PEFT equivalence of gate/materialize_cat.py (CPU, tiny random model): the od_gcp.py blend path (load members, PEFT
add_weighted_adapter cat, merge_and_unload) and the od_gcp.py predict path on the materialized folder (load one
adapter, merge_and_unload) must give the same merged weights and logits. Needs peft (0.21.0 on the L4).
  PYTHONPATH=<dir with peft+accelerate> ../.venv/bin/python gate/tests/peft_equivalence_check.py <scratch dir>
"""
import json
import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import materialize_cat as mc  # noqa: E402
from peft import LoraConfig, PeftModel, get_peft_model, __version__ as peft_version  # noqa: E402
from transformers import LlamaConfig, LlamaForCausalLM  # noqa: E402

TARGETS = r".*layers\.\d+\..*\.(q_proj|k_proj|v_proj|o_proj|gate_proj|up_proj|down_proj)"


def base(dtype):
    torch.manual_seed(0)
    cfg = LlamaConfig(vocab_size=97, hidden_size=48, intermediate_size=96, num_hidden_layers=2, num_attention_heads=4,
                      num_key_value_heads=2, max_position_embeddings=64)
    return LlamaForCausalLM(cfg).to(dtype).eval()


def make_adapter(root, name, r, alpha, seed):
    torch.manual_seed(seed)
    m = get_peft_model(base(torch.float32), LoraConfig(r=r, lora_alpha=alpha, target_modules=TARGETS,
                                                         init_lora_weights=False, lora_dropout=0.0))
    d = root / name
    m.save_pretrained(d)
    (d / "train_meta.json").write_text(json.dumps({"cfg": {"base": "tiny", "layout": "schema_branch_mark",
                                                           "style": "cygnet", "r": r, "alpha": alpha}}))
    return d


def merged_blend(dirs, weights, dtype):
    m = PeftModel.from_pretrained(base(dtype), str(dirs[0]), adapter_name="a0")
    for i, d in enumerate(dirs[1:], 1):
        m.load_adapter(str(d), adapter_name=f"a{i}")
    m.add_weighted_adapter([f"a{i}" for i in range(len(dirs))], weights, adapter_name="blend", combination_type="cat")
    m.set_adapter("blend")
    return m.merge_and_unload(adapter_names=["blend"]).eval()


def merged_single(d, dtype):
    return PeftModel.from_pretrained(base(dtype), str(d)).merge_and_unload().eval()


def compare(a, b):
    sa, sb = a.state_dict(), b.state_dict()
    assert sa.keys() == sb.keys()
    w = max((sa[k].float() - sb[k].float()).abs().max().item() for k in sa)
    x = torch.randint(0, 97, (2, 16))
    with torch.no_grad():
        lg = (a(x).logits.float() - b(x).logits.float()).abs().max().item()
    return w, lg


def main(root):
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    out = {"peft": peft_version}
    members = [make_adapter(root, "m1", 2, 4, 1), make_adapter(root, "m2", 4, 4, 2), make_adapter(root, "m3", 2, 8, 3)]
    for label, dirs, ws in (("c2_like_equal", members, [1 / 3] * 3), ("c3_like_075_025", members[:2], [0.75, 0.25])):
        mat = mc.materialize([str(d) for d in dirs], ws, root / f"mat_{label}", force=True)
        for dtype in (torch.float32, torch.bfloat16):
            w, lg = compare(merged_blend(dirs, ws, dtype), merged_single(mat, dtype))
            out[f"{label}_{str(dtype).split('.')[-1]}"] = {"max_weight_diff": w, "max_logit_diff": lg}
            if dtype == torch.float32:  # same fp32 A and B -> bit-identical merge
                assert w == 0.0 and lg == 0.0, (label, dtype, w, lg)
            # bf16 base: PEFT's add_weighted_adapter creates the blend adapter in the base dtype, so od_gcp.py blend
            # rounds A and B to bf16 before merging; the materialized folder keeps them fp32 (PeftModel.from_pretrained
            # upcasts adapters). Same math, one rounding step less: differences of a bf16 ulp are expected here.
    out["note"] = ("fp32: bit-identical to PEFT add_weighted_adapter(cat). bf16: od_gcp.py blend rounds the blended A/B "
                   "to bf16 before merging, the materialized adapter keeps fp32 A/B (one rounding step less).")
    # (1, 0) reproduces the single member (the C3 merge check's premise), in bf16
    mat10 = mc.materialize([str(members[0]), str(members[1])], [1.0, 0.0], root / "mat_10", force=True)
    for dtype in (torch.float32, torch.bfloat16):
        w, lg = compare(merged_single(members[0], dtype), merged_single(mat10, dtype))
        out[f"weights_1_0_vs_member_{str(dtype).split('.')[-1]}"] = {"max_weight_diff": w, "max_logit_diff": lg}
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main(sys.argv[1])

"""build_fp8_block.py SRC_DIR DST_DIR: data-free block-FP8 (128x128 weight blocks, dynamic activations) checkpoint of C1.

Same math as LLM Compressor's FP8_BLOCK preset with the min/max observer (no calibration data): per 128x128 block
scale = absmax / 448 (float8_e4m3fn max), q = round_to_e4m3(w / scale). Serialized in Qwen's own FP8 layout
(Qwen/Qwen3.5-27B-FP8): `<name>.weight` float8_e4m3fn + `<name>.weight_scale_inv` float32 [out/128, in/128], and
config.json quantization_config {quant_method fp8, activation_scheme dynamic, fmt e4m3, weight_block_size [128,128],
modules_to_not_convert [...]}, which SGLang loads with `--quantization fp8`.

Quantized: every language-model Linear weight (self_attn q/k/v/o, linear_attn in_proj_qkv / in_proj_z / out_proj, mlp
gate/up/down). Kept BF16 (ignore list of the plan): lm_head / embed_tokens (tied), model.visual.*, every
linear_attn.conv1d, linear_attn.in_proj_a, linear_attn.in_proj_b, mtp.*, all norms and biases and A_log / dt_bias.
Runs on CPU. Counts only on stdout.
"""
import json
import re
import shutil
import sys
import time
from pathlib import Path

import torch
from safetensors import safe_open
from safetensors.torch import save_file

FP8_MAX = 448.0
BLK = 128
TARGET = re.compile(r"^model\.language_model\.layers\.\d+\.(self_attn\.(q|k|v|o)_proj|linear_attn\.(in_proj_qkv|in_proj_z|out_proj)|mlp\.(gate|up|down)_proj)\.weight$")


def quant_block(w: torch.Tensor):
    """w [out, in] (bf16) -> (q float8_e4m3fn [out, in], scale_inv float32 [out/128, in/128])."""
    o, i = w.shape
    assert o % BLK == 0 and i % BLK == 0, (o, i)
    wf = w.float().reshape(o // BLK, BLK, i // BLK, BLK)
    amax = wf.abs().amax(dim=(1, 3))                                  # [o/128, i/128]
    scale = torch.where(amax > 0, amax / FP8_MAX, torch.ones_like(amax))
    q = (wf / scale[:, None, :, None]).clamp(-FP8_MAX, FP8_MAX).to(torch.float8_e4m3fn).reshape(o, i)
    return q.contiguous(), scale.contiguous()


def main(src, dst):
    src, dst = Path(src), Path(dst)
    dst.mkdir(parents=True, exist_ok=True)
    idx = json.load(open(src / "model.safetensors.index.json"))
    wm = idx["weight_map"]
    shards = sorted(set(wm.values()))
    new_map, ignored, n_q, n_keep, b_q, b_keep = {}, [], 0, 0, 0, 0
    t0 = time.time()
    for sh in shards:
        out = {}
        with safe_open(str(src / sh), framework="pt") as f:
            for k in f.keys():
                t = f.get_tensor(k)
                if TARGET.match(k):
                    q, s = quant_block(t)
                    out[k] = q
                    out[k.replace(".weight", ".weight_scale_inv")] = s
                    n_q += 1
                    b_q += q.numel() + s.numel() * 4
                else:
                    out[k] = t
                    n_keep += 1
                    b_keep += t.numel() * t.element_size()
                    base = k[: -len(".weight")] if k.endswith(".weight") else None
                    if base and (".linear_attn.conv1d" in base or ".linear_attn.in_proj_a" in base or ".linear_attn.in_proj_b" in base
                                 or base.startswith("model.visual") or base.startswith("mtp.") or base.endswith("embed_tokens")):
                        ignored.append(base)
        save_file(out, str(dst / sh), metadata={"format": "pt"})
        for k in out:
            new_map[k] = sh
        print(f"{sh}: {len(out)} tensors, {time.time() - t0:.0f}s", flush=True)
    idx["weight_map"] = new_map
    json.dump(idx, open(dst / "model.safetensors.index.json", "w"), indent=1)
    for p in src.iterdir():
        if p.name.endswith(".safetensors") or p.name == "model.safetensors.index.json":
            continue
        if p.is_dir():
            shutil.copytree(p, dst / p.name, dirs_exist_ok=True)
        elif p.name != "config.json":
            shutil.copy2(p, dst / p.name)
    cfg = json.load(open(src / "config.json"))
    ign = sorted(set(ignored)) + ["lm_head"]
    cfg["quantization_config"] = {"activation_scheme": "dynamic", "fmt": "e4m3", "quant_method": "fp8",
                                  "weight_block_size": [BLK, BLK], "modules_to_not_convert": ign}
    json.dump(cfg, open(dst / "config.json", "w"), indent=2)
    print(json.dumps({"quantized_linears": n_q, "kept_tensors": n_keep, "bytes_fp8_part": b_q, "bytes_kept_part": b_keep,
                      "ignored_modules": len(ign), "seconds": round(time.time() - t0, 1)}))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

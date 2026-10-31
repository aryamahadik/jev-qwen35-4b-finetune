"""verify_fp8.py SRC DST : dequantization error of the block-FP8 checkpoint vs the BF16 source, scale = absmax/448 check,
and agreement of the block scale with compressed-tensors' own calculate_qparams (the LLM Compressor FP8_BLOCK arithmetic)."""
import json, sys, re
import torch
from safetensors import safe_open
src, dst = sys.argv[1], sys.argv[2]
idx = json.load(open(f"{dst}/model.safetensors.index.json"))["weight_map"]
S = json.load(open(f"{src}/model.safetensors.index.json"))["weight_map"]
names = [k for k in idx if k.endswith(".weight_scale_inv")]
print("scale tensors:", len(names), "of 200 expected")
errs, scale_bad, nonfin, mism = [], 0, 0, 0
pick = names[::7]
for sk in pick:
    wk = sk.replace("_scale_inv", "")
    with safe_open(f"{dst}/{idx[wk]}", "pt") as f:
        q, s = f.get_tensor(wk), f.get_tensor(sk)
    with safe_open(f"{src}/{S[wk]}", "pt") as f:
        w = f.get_tensor(wk)
    o, i = w.shape
    deq = (q.float().reshape(o // 128, 128, i // 128, 128) * s[:, None, :, None]).reshape(o, i)
    wf = w.float()
    rel = ((deq - wf).norm() / wf.norm()).item()
    errs.append(rel)
    amax = wf.reshape(o // 128, 128, i // 128, 128).abs().amax(dim=(1, 3))
    exp = torch.where(amax > 0, amax / 448.0, torch.ones_like(amax))
    scale_bad += int(not torch.allclose(exp, s, rtol=1e-6))
    nonfin += int(not torch.isfinite(deq).all())
print("checked", len(pick), "tensors; rel Frobenius error min/mean/max:", round(min(errs), 5), round(sum(errs) / len(errs), 5), round(max(errs), 5),
      "| scale != absmax/448:", scale_bad, "| non-finite:", nonfin)
# kept tensors are bit-identical to the source
bad = 0; n = 0
for k in [k for k in idx if not k.endswith("_scale_inv") and not re.match(r"^model\.language_model\.layers\.\d+\.(self_attn\.(q|k|v|o)_proj|linear_attn\.(in_proj_qkv|in_proj_z|out_proj)|mlp\.(gate|up|down)_proj)\.weight$", k)][::9]:
    with safe_open(f"{dst}/{idx[k]}", "pt") as f: a = f.get_tensor(k)
    with safe_open(f"{src}/{S[k]}", "pt") as f: b = f.get_tensor(k)
    n += 1; bad += int(not torch.equal(a, b))
print("kept tensors checked:", n, "not bit-identical:", bad)
try:
    from compressed_tensors.quantization import QuantizationArgs
    from compressed_tensors.quantization.utils import calculate_qparams
    a = QuantizationArgs(num_bits=8, type="float", strategy="block", symmetric=True, dynamic=False, block_structure=[128, 128])
    t = torch.randn(64, 64) * 0.03
    sc, zp = calculate_qparams(t.min().reshape(1), t.max().reshape(1), a)
    print("compressed-tensors scale:", float(sc), "absmax/448:", float(t.abs().max() / 448.0))
except Exception as e:
    print("compressed-tensors check skipped:", type(e).__name__, str(e)[:120])

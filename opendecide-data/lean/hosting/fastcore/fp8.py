"""fastcore.fp8: rowwise FP8 (e4m3) body linears for arm A3 (hosting/SPEED1_DESIGN.md, "Arms").

RowwiseFP8Linear: the weight is stored as float8_e4m3fn with one fp32 scale per OUTPUT channel (amax / 448); each
forward quantises the activations with one fp32 scale per TOKEN (row amax / 448) and multiplies with
torch._scaled_mm(x_fp8, w_fp8.T, scale_a=[T,1], scale_b=[1,N], out_dtype=bf16) on CUDA (sm89+, fp32 accumulation), or
with a numerically equivalent dequantised fp32 matmul elsewhere (the CPU fallback the tests use). The forward has no
host sync and no data-dependent Python branch, so it can be captured in a CUDA graph.

quantize_model(model) swaps exactly the decoder layers' body linears of a MERGED Qwen3.5 text model (transformers
5.17 names): self_attn.{q,k,v,o}_proj, linear_attn.{in_proj_qkv,in_proj_z,out_proj}, mlp.{gate,up,down}_proj. It keeps
lm_head, embed_tokens, linear_attn.in_proj_a / in_proj_b (32 outputs each, the decay / write-strength gates),
linear_attn.conv1d, every norm and the vision tower in their original dtype (BF16).

Commands: none (library). CPU-tested in hosting/tests/test_fastcore_fp8.py. The _scaled_mm path's numerics on an H100
are only checked in SPEED-2 (parity bar for FP8 arms: |accuracy diff| <= 1.0 pt, argmax agreement >= 99.5%).
"""
from __future__ import annotations

import re

import torch
from torch import nn

E4M3_MAX = 448.0
EPS = 1e-12
FP8 = torch.float8_e4m3fn
# decoder-layer body linears (Qwen3_5DecoderLayer: self_attn / linear_attn / mlp); vision blocks are "blocks.N", never
# "layers.N", and in_proj_a / in_proj_b / conv1d / norms / embed_tokens / lm_head do not match
TARGET_RE = re.compile(r"(?:^|\.)layers\.\d+\.(?:self_attn\.(?:q_proj|k_proj|v_proj|o_proj)"
                       r"|linear_attn\.(?:in_proj_qkv|in_proj_z|out_proj)|mlp\.(?:gate_proj|up_proj|down_proj))$")
KEEP_BF16 = ("lm_head", "embed_tokens", "in_proj_a", "in_proj_b", "conv1d", "norm", "visual")
_CAP = {}


def _scaled_mm_ok(dev: torch.device) -> bool:
    """torch._scaled_mm rowwise FP8 needs CUDA compute capability >= 8.9 (Ada / Hopper)."""
    if dev.type != "cuda":
        return False
    i = dev.index if dev.index is not None else torch.cuda.current_device()
    if i not in _CAP:
        _CAP[i] = torch.cuda.get_device_capability(i) >= (8, 9)
    return _CAP[i]


def quantize_rowwise(w: torch.Tensor):
    """[N, K] weight -> (fp8 [N, K], fp32 scale [N]): one scale per output channel, amax / 448."""
    wf = w.detach().float()
    scale = (wf.abs().amax(dim=1) / E4M3_MAX).clamp_min(EPS)
    q = (wf / scale[:, None]).clamp(-E4M3_MAX, E4M3_MAX).to(FP8)
    return q, scale


def quantize_tokens(x2: torch.Tensor):
    """[T, K] activations -> (fp8 [T, K], fp32 scale [T, 1]): one scale per token, amax / 448."""
    xf = x2.float()
    scale = (xf.abs().amax(dim=-1, keepdim=True) / E4M3_MAX).clamp_min(EPS)
    return (xf / scale).clamp(-E4M3_MAX, E4M3_MAX).to(FP8), scale


class RowwiseFP8Linear(nn.Module):
    """Drop-in for a bias-free (or biased) nn.Linear with FP8 weights. backend: "auto" (scaled_mm on sm89+ CUDA, else
    dequant), "scaled_mm" (forced; also runs on CPU where torch supports it), "dequant" (fp32 reference)."""

    def __init__(self, in_features: int, out_features: int, weight_fp8: torch.Tensor, weight_scale: torch.Tensor,
                 bias: torch.Tensor | None = None, out_dtype: torch.dtype = torch.bfloat16, backend: str = "auto"):
        super().__init__()
        if backend not in ("auto", "scaled_mm", "dequant"):
            raise ValueError(f"backend {backend!r}")
        self.in_features, self.out_features, self.out_dtype, self.backend = in_features, out_features, out_dtype, backend
        self.register_buffer("weight_fp8", weight_fp8.contiguous())  # [N, K]
        self.register_buffer("weight_scale", weight_scale.float().reshape(1, out_features).contiguous())  # [1, N]
        self.register_buffer("bias", None if bias is None else bias.detach().to(out_dtype))

    @classmethod
    def from_linear(cls, lin: nn.Linear, backend: str = "auto") -> "RowwiseFP8Linear":
        q, s = quantize_rowwise(lin.weight)
        return cls(lin.in_features, lin.out_features, q, s, lin.bias, out_dtype=lin.weight.dtype, backend=backend)

    def dequantized_weight(self) -> torch.Tensor:
        """[N, K] weight as the fallback multiplies it (fp32). No .weight attribute on purpose: code that expects a
        BF16 nn.Linear weight fails loudly instead of silently materialising one."""
        return self.weight_fp8.float() * self.weight_scale.reshape(-1, 1)

    def _use_scaled_mm(self, x: torch.Tensor) -> bool:
        if self.backend == "scaled_mm":
            return True
        return self.backend == "auto" and _scaled_mm_ok(x.device)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        shp = x.shape
        xq, sa = quantize_tokens(x.reshape(-1, self.in_features))
        if self._use_scaled_mm(x):
            y = torch._scaled_mm(xq, self.weight_fp8.t(), scale_a=sa, scale_b=self.weight_scale,
                                 out_dtype=self.out_dtype)
        else:
            y = ((xq.float() * sa) @ self.dequantized_weight().t()).to(self.out_dtype)
        if self.bias is not None:
            y = y + self.bias
        return y.reshape(*shp[:-1], self.out_features)

    def extra_repr(self) -> str:
        return f"in_features={self.in_features}, out_features={self.out_features}, fp8=e4m3 rowwise, backend={self.backend}"


def target_names(model) -> list:
    """Names of the nn.Linear modules quantize_model would swap."""
    return [n for n, m in model.named_modules() if isinstance(m, nn.Linear) and TARGET_RE.search(n)
            and not any(k in n.split(".") for k in ("visual",))]


def quantize_model(model, backend: str = "auto", check_merged: bool = True) -> dict:
    """Swap the body linears (TARGET_RE) for RowwiseFP8Linear in place. Refuses an unmerged PEFT model (LoRA layers
    would be skipped silently). Returns a report: swapped names, kept linears, weight bytes before/after."""
    if check_merged and any("lora_" in n for n, _ in model.named_modules()):
        raise RuntimeError("quantize_model: merge the adapter first (merge_and_unload); LoRA modules found")
    names = target_names(model)
    if not names:
        raise RuntimeError("quantize_model: no target linears found (not a Qwen3.5 decoder?)")
    mods = dict(model.named_modules())
    before = after = 0
    skipped = []
    for n in names:
        lin = mods[n]
        if lin.in_features % 16 or lin.out_features % 16:  # _scaled_mm needs K and N multiples of 16
            skipped.append(n)
            continue
        before += lin.weight.numel() * lin.weight.element_size()
        new = RowwiseFP8Linear.from_linear(lin, backend=backend)
        after += new.weight_fp8.numel() + new.weight_scale.numel() * 4
        parent, _, child = n.rpartition(".")
        setattr(mods[parent] if parent else model, child, new)
        del lin
    kept = [n for n, m in model.named_modules() if isinstance(m, nn.Linear)]
    kinds = {}
    for n in names:
        if n not in skipped:
            k = n.rsplit(".", 1)[-1]
            kinds[k] = kinds.get(k, 0) + 1
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return {"quantization": "fp8", "scheme": "e4m3 rowwise (weights per output channel, activations per token)",
            "swapped": len(names) - len(skipped), "by_kind": kinds, "skipped_not_16_aligned": skipped,
            "kept_linear": kept, "weight_bytes_before": before, "weight_bytes_after": after,
            "weight_gb_before": round(before / 2 ** 30, 3), "weight_gb_after": round(after / 2 ** 30, 3), "backend": backend}

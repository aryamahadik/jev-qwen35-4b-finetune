"""fastcore.fp8 on CPU: rowwise FP8 quantisation, RowwiseFP8Linear (dequant fallback vs BF16 and vs torch._scaled_mm,
which this torch also runs on CPU), quantize_model swapping exactly the intended Qwen3.5 modules of the tiny hybrid
model, refusal of an unmerged LoRA model, and the quantised model through the fastcore runner (eager and emulated graph).

  cd ~/Documents/jev/opendecide-data/lean && ../.venv/bin/python -m pytest hosting/tests/test_fastcore_fp8.py -q
No GPU, no network. The H100 numerics of the _scaled_mm path are SPEED-2's parity check.
"""
import sys
from pathlib import Path

import pytest
import torch
from torch import nn

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fastcore import fp8  # noqa: E402
from fastcore import graphs as G  # noqa: E402
from fastcore import testing as T  # noqa: E402


def _rel(a, b):
    a, b = a.detach().float(), b.detach().float()
    return float((a - b).norm() / b.norm())


@pytest.mark.parametrize("shape", [(64, 128), (256, 96), (2560 // 10, 9216 // 36)])
def test_rowwise_quant_roundtrip(shape):
    torch.manual_seed(1)
    w = torch.randn(*shape) * torch.logspace(-2, 1, shape[0])[:, None]  # very different row scales
    q, s = fp8.quantize_rowwise(w)
    assert q.dtype == torch.float8_e4m3fn and s.shape == (shape[0],) and (s > 0).all()
    deq = q.float() * s[:, None]
    assert (deq - w).abs().le(w.abs() * 2 ** -4 + s[:, None] * 2 ** -9 + 1e-12).all()  # e4m3: 3 mantissa bits
    x = torch.randn(7, 5, shape[1])
    xq, sa = fp8.quantize_tokens(x.reshape(-1, shape[1]))
    assert sa.shape == (35, 1) and xq.abs().float().max() <= fp8.E4M3_MAX


@pytest.mark.parametrize("dtype", [torch.bfloat16, torch.float32])
def test_fp8_linear_close_to_original(dtype):
    torch.manual_seed(0)
    for n_in, n_out, bias in ((64, 128, False), (128, 32, True), (256, 512, False)):
        lin = nn.Linear(n_in, n_out, bias=bias).to(dtype)
        x = torch.randn(3, 11, n_in, dtype=dtype)
        with torch.no_grad():
            ref = lin(x)
        m = fp8.RowwiseFP8Linear.from_linear(lin, backend="dequant")
        y = m(x)
        assert y.shape == ref.shape and y.dtype == dtype
        assert _rel(y, ref) < 0.06, _rel(y, ref)
        # forced torch._scaled_mm (runs on CPU in this torch) == the dequantised fallback up to the output rounding
        mm = fp8.RowwiseFP8Linear.from_linear(lin, backend="scaled_mm")
        y2 = mm(x)
        ulp = 2 ** -7 if dtype == torch.bfloat16 else 1e-6
        assert (y2.float() - y.float()).abs().le(y.float().abs() * ulp + 1e-3).all()
        assert not mm._use_scaled_mm(torch.zeros(1)) or mm.backend == "scaled_mm"
    auto = fp8.RowwiseFP8Linear.from_linear(nn.Linear(32, 32), backend="auto")
    assert not auto._use_scaled_mm(torch.zeros(1))  # CPU: auto -> dequant
    assert not hasattr(auto, "weight") and auto.dequantized_weight().shape == (32, 32)


EXPECT_SWAP = {"linear_attention": ["linear_attn.in_proj_qkv", "linear_attn.in_proj_z", "linear_attn.out_proj"],
               "full_attention": ["self_attn.q_proj", "self_attn.k_proj", "self_attn.v_proj", "self_attn.o_proj"]}


def test_quantize_model_swaps_exactly_the_body_linears():
    model = T.tiny_model(dtype=torch.bfloat16)
    types = model.config.layer_types
    want = set()
    for i, t in enumerate(types):
        want |= {f"model.layers.{i}.{n}" for n in EXPECT_SWAP[t]}
        want |= {f"model.layers.{i}.mlp.{n}" for n in ("gate_proj", "up_proj", "down_proj")}
    assert set(fp8.target_names(model)) == want
    keep_lin = {n for n, m in model.named_modules() if isinstance(m, nn.Linear)} - want
    rep = fp8.quantize_model(model)
    assert rep["swapped"] == len(want) == 2 * 3 + 2 * 4 + 4 * 3 and not rep["skipped_not_16_aligned"]
    swapped = {n for n, m in model.named_modules() if isinstance(m, fp8.RowwiseFP8Linear)}
    assert swapped == want
    assert set(rep["kept_linear"]) == keep_lin
    assert keep_lin == {"lm_head"} | {f"model.layers.{i}.linear_attn.in_proj_{x}" for i, t in enumerate(types)
                                      if t == "linear_attention" for x in ("a", "b")}
    mods = dict(model.named_modules())
    assert isinstance(mods["model.embed_tokens"], nn.Embedding) and mods["model.embed_tokens"].weight.dtype == torch.bfloat16
    assert model.lm_head.weight.dtype == torch.bfloat16
    for i, t in enumerate(types):
        if t == "linear_attention":
            assert isinstance(mods[f"model.layers.{i}.linear_attn.conv1d"], nn.Conv1d)
            assert mods[f"model.layers.{i}.linear_attn.conv1d"].weight.dtype == torch.bfloat16
    norms = [m for n, m in model.named_modules() if "norm" in n.rsplit(".", 1)[-1]]
    assert norms and all(p.dtype == torch.bfloat16 for m in norms for p in m.parameters())
    assert rep["by_kind"]["gate_proj"] == 4 and rep["weight_bytes_after"] < 0.6 * rep["weight_bytes_before"]


def test_quantized_tiny_model_runs_and_stays_close():
    tok = T.c1_tokenizer()
    ref = T.tiny_model(dtype=torch.bfloat16)
    q = T.tiny_model(dtype=torch.bfloat16)
    fp8.quantize_model(q)
    ids = torch.tensor([tok("The office opens at nine. Is it open?", add_special_tokens=False)["input_ids"] * 6])
    with torch.no_grad():
        h0 = ref.model(input_ids=ids, use_cache=False).last_hidden_state
        h1 = q.model(input_ids=ids, use_cache=False).last_hidden_state
    assert torch.isfinite(h1).all() and _rel(h1, h0) < 0.15, _rel(h1, h0)
    F = G.FastGraphs(q, tok, emulate=True)  # the quantised body through the runner: eager and (emulated) graph
    seq = ids[0].tolist()
    F.capture([(1, G.bucket_of(len(seq)))], log=lambda *a: None)
    F.freeze()
    cands = [([t for t in range(10, 40)], [3] * 10)]
    (e,), _ = F.run([seq], cands, None)
    (g,), _ = F.run([seq], cands, F.select(1, len(seq)))
    assert torch.isfinite(e).all() and float((e - g).abs().max()) < 0.05


def test_refuses_unmerged_lora_and_non_qwen():
    from peft import LoraConfig, get_peft_model
    model = T.tiny_model(dtype=torch.float32)
    pm = get_peft_model(model, LoraConfig(r=4, target_modules=["q_proj", "v_proj"]))
    with pytest.raises(RuntimeError, match="merge"):
        fp8.quantize_model(pm)
    with pytest.raises(RuntimeError, match="no target"):
        fp8.quantize_model(nn.Sequential(nn.Linear(16, 16)))


def test_vision_tower_never_targeted():
    class Blk(nn.Module):
        def __init__(self):
            super().__init__()
            self.attn = nn.Module()
            self.attn.qkv = nn.Linear(32, 96)
            self.mlp = nn.Module()
            self.mlp.gate_proj = nn.Linear(32, 64)
    root = nn.Module()
    root.model = nn.Module()
    root.model.visual = nn.Module()
    root.model.visual.blocks = nn.ModuleList([Blk()])
    root.model.visual.layers = nn.ModuleList([Blk()])  # even a "layers.N.mlp.gate_proj" under visual is skipped
    root.model.language_model = nn.Module()
    root.model.language_model.layers = nn.ModuleList([Blk()])
    assert fp8.target_names(root) == ["model.language_model.layers.0.mlp.gate_proj"]

"""oc1/pypatch/sitecustomize.py against a FAKE sglang package tree (no GPU, no real sglang): the import hook must patch
W8A8Fp8Config.get_quant_method when (and only when) the target module is imported, honour the ignore list, and the int8
method must quantize per output channel."""
import json
import os
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

PYPATCH = Path(__file__).resolve().parents[1] / "oc1" / "pypatch"


def make_fake_sglang(root: Path):
    def w(rel, text):
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(textwrap.dedent(text))
    for d in ("sglang", "sglang/srt", "sglang/srt/layers", "sglang/srt/layers/quantization"):
        w(d + "/__init__.py", "")
    w("sglang/srt/layers/linear.py", """
        class LinearBase:
            pass
        class Other:
            pass
    """)
    w("sglang/srt/layers/quantization/unquant.py", """
        class UnquantizedLinearMethod:
            name = "bf16"
    """)
    w("sglang/srt/layers/parameter.py", """
        import torch
        class ModelWeightParameter(torch.nn.Parameter):
            def __new__(cls, data=None, **kw):
                return super().__new__(cls, data, requires_grad=False)
    """)
    w("sglang/srt/layers/quantization/w8a8_int8.py", """
        class W8A8Int8Config:
            def __init__(self, d): self.d = d
        class W8A8Int8LinearMethod:
            def __init__(self, cfg): self.cfg = cfg
            def apply(self, layer, x, bias=None): return "int8-apply"
    """)
    # importing the package __init__ imports w8a8_fp8, like the real sglang/srt/layers/quantization/__init__.py
    w("sglang/srt/layers/quantization/__init__.py", "from sglang.srt.layers.quantization.w8a8_fp8 import W8A8Fp8Config\n")
    w("sglang/srt/layers/quantization/w8a8_fp8.py", """
        class W8A8Fp8Config:
            def get_quant_method(self, layer, prefix):
                from sglang.srt.layers.linear import LinearBase
                return "fp8-online" if isinstance(layer, LinearBase) else None
    """)


def run(code, env_extra, tmp_path):
    root = tmp_path / "fake"
    make_fake_sglang(root)
    env = {**os.environ, "PYTHONPATH": os.pathsep.join([str(PYPATCH), str(root)]), "OC1_REPORT": str(tmp_path / "rep.jsonl"),
           "PYTHONDONTWRITEBYTECODE": "1", **env_extra}
    r = subprocess.run([sys.executable, "-c", textwrap.dedent(code)], env=env, capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, r.stderr
    rep = [json.loads(x) for x in (tmp_path / "rep.jsonl").read_text().splitlines()] if (tmp_path / "rep.jsonl").exists() else []
    return r.stdout.strip(), rep


CODE = """
    import sglang.srt.layers.quantization as Q
    from sglang.srt.layers.quantization.w8a8_fp8 import W8A8Fp8Config
    from sglang.srt.layers.linear import LinearBase, Other
    c = W8A8Fp8Config()
    for pre in ("model.layers.0.mlp.down_proj", "model.layers.3.linear_attn.in_proj_ba", "visual.blocks.0.attn.qkv_proj"):
        m = c.get_quant_method(LinearBase(), pre)
        print(pre, m if isinstance(m, str) else getattr(m, 'name', type(m).__name__))
    print("other", c.get_quant_method(Other(), "model.layers.0.norm"))
"""


def test_fp8_mode_ignores_matching_linears_only(tmp_path):
    out, rep = run(CODE, {"OC1_ONLINE_MODE": "fp8", "OC1_IGNORE": json.dumps(["in_proj_ba", "visual"])}, tmp_path)
    lines = dict(l.split(" ", 1) for l in out.splitlines())
    assert lines["model.layers.0.mlp.down_proj"] == "fp8-online"
    assert lines["model.layers.3.linear_attn.in_proj_ba"] == "bf16"
    assert lines["visual.blocks.0.attn.qkv_proj"] == "bf16"
    assert lines["other"] == "None"
    modes = {r["prefix"]: r["mode"] for r in rep if "prefix" in r}
    assert modes["model.layers.0.mlp.down_proj"] == "fp8" and modes["model.layers.3.linear_attn.in_proj_ba"] == "bf16"
    assert any(r.get("patched") for r in rep)


def test_off_by_default(tmp_path):
    out, rep = run(CODE, {"OC1_ONLINE_MODE": ""}, tmp_path)
    assert "bf16" not in out and not rep


def test_int8_mode_uses_the_online_int8_method(tmp_path):
    torch = pytest.importorskip("torch")
    code = CODE.replace('print(pre, m if isinstance(m, str) else getattr(m, \'name\', type(m).__name__))',
                        'print(pre, m if isinstance(m, str) else getattr(m, "name", type(m).__name__))')
    out, rep = run(code, {"OC1_ONLINE_MODE": "int8", "OC1_IGNORE": json.dumps(["in_proj_ba"])}, tmp_path)
    lines = dict(l.split(" ", 1) for l in out.splitlines())
    assert lines["model.layers.0.mlp.down_proj"] == "Int8OnlineLinearMethod"
    assert lines["model.layers.3.linear_attn.in_proj_ba"] == "bf16"
    modes = {r["prefix"]: r["mode"] for r in rep if "prefix" in r}
    assert modes["model.layers.0.mlp.down_proj"] == "int8"


def test_int8_quantization_math(tmp_path):
    torch = pytest.importorskip("torch")
    code = """
        import torch
        import sglang.srt.layers.quantization as Q
        from sglang.srt.layers.quantization.w8a8_fp8 import W8A8Fp8Config
        from sglang.srt.layers.linear import LinearBase
        m = W8A8Fp8Config().get_quant_method(LinearBase(), "model.layers.0.mlp.down_proj")
        torch.manual_seed(0)
        w = (torch.randn(8, 16) * torch.rand(8, 1) * 3).to(torch.bfloat16)
        layer = LinearBase(); layer.weight = torch.nn.Parameter(w.clone(), requires_grad=False)
        m.process_weights_after_loading(layer)
        q, s = layer.weight, layer.weight_scale
        assert q.dtype == torch.int8 and q.shape == (16, 8) and s.shape == (8, 1) and s.dtype == torch.float32
        deq = q.t().float() * s
        err = (deq - w.float()).abs()
        assert float(err.max()) <= float(s.max()) * 0.5001 + 1e-6, float(err.max())
        assert float(q.abs().max()) <= 127
        print("ok")
    """
    out, _ = run(code, {"OC1_ONLINE_MODE": "int8", "OC1_IGNORE": "[]"}, tmp_path)
    assert out.endswith("ok")

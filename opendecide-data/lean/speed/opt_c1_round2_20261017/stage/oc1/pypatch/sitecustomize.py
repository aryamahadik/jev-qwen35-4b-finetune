"""sitecustomize: OPT-IN patch of SGLang's `w8a8_fp8` online quantization, active only when OC1_ONLINE_MODE is set.

SGLang spawns its scheduler / model-runner as a fresh interpreter, so a patch in the launching process would not reach the
code that builds the layers. Python imports `sitecustomize` at the start of EVERY interpreter that has this folder on
PYTHONPATH, which the children inherit. The patch is installed lazily, when sglang.srt.layers.quantization.w8a8_fp8 is
imported (nothing else is touched), and does two things to `W8A8Fp8Config.get_quant_method(layer, prefix)`:

  OC1_ONLINE_MODE=fp8   a linear layer whose prefix matches one of the OC1_IGNORE regexes (JSON list) gets
                        UnquantizedLinearMethod (BF16); every other LinearBase keeps SGLang's own online path
                        (per-channel absmax weight scales, dynamic per-token activation quantization).
  OC1_ONLINE_MODE=int8  same ignore rule; every other linear gets W8A8 INT8: per-channel symmetric int8 weights computed
                        at load time from the BF16 weights, dynamic per-token int8 activations through the SAME kernels
                        SGLang's w8a8_int8 checkpoints use (per_token_quant_int8 + int8_scaled_mm).

It never changes a weight file and never touches a layer that is not a LinearBase (lm_head and the embedding are not).
Every decision is appended as one JSON line to OC1_REPORT (default /tmp/oc1_quant_report.jsonl) so the run can prove WHICH
modules stayed BF16 (in_proj_ba = in_proj_a/in_proj_b, the vision tower, ...).
"""
import importlib.abc
import importlib.util
import json
import os
import re
import sys

MODE = os.environ.get("OC1_ONLINE_MODE", "")
TARGET = "sglang.srt.layers.quantization.w8a8_fp8"
REPORT = os.environ.get("OC1_REPORT", "/tmp/oc1_quant_report.jsonl")


def _report(rec):
    try:
        with open(REPORT, "a") as f:
            f.write(json.dumps({"pid": os.getpid(), **rec}) + "\n")
    except OSError:
        pass


def _int8_method(mod):
    import torch
    from torch.nn import Parameter
    from sglang.srt.layers.quantization import w8a8_int8 as W

    class Int8OnlineLinearMethod(W.W8A8Int8LinearMethod):
        """BF16 weights are created and loaded as usual (the packed-weight loaders see a normal weight); after loading
        each is quantized per output channel to int8 and the stock W8A8 INT8 kernel path runs."""

        def create_weights(self, layer, input_size_per_partition, output_partition_sizes, input_size, output_size,
                           params_dtype, **extra_weight_attrs):
            from sglang.srt.layers.parameter import ModelWeightParameter
            self.logical_widths = output_partition_sizes
            weight = ModelWeightParameter(
                data=torch.empty(sum(output_partition_sizes), input_size_per_partition, dtype=params_dtype),
                input_dim=1, output_dim=0, weight_loader=extra_weight_attrs.get("weight_loader"))
            layer.register_parameter("weight", weight)

        def process_weights_after_loading(self, layer):
            w = layer.weight.data.float()
            scale = (w.abs().amax(dim=1, keepdim=True) / 127.0).clamp(min=1e-8)
            q = torch.round(w / scale).clamp(-127, 127).to(torch.int8)
            layer.weight = Parameter(q.t(), requires_grad=False)
            layer.weight_scale = Parameter(scale.float(), requires_grad=False)
            layer.input_scale = None

    return Int8OnlineLinearMethod(W.W8A8Int8Config({}))


def _patch(mod):
    try:
        from sglang.srt.layers.quantization.unquant import UnquantizedLinearMethod
    except ImportError:
        from sglang.srt.layers.linear import UnquantizedLinearMethod
    ignore = [re.compile(p) for p in json.loads(os.environ.get("OC1_IGNORE", "[]"))]
    orig = mod.W8A8Fp8Config.get_quant_method
    state = {"int8": None}

    def get_quant_method(self, layer, prefix):
        from sglang.srt.layers.linear import LinearBase
        if isinstance(layer, LinearBase):
            if any(r.search(prefix) for r in ignore):
                _report({"prefix": prefix, "mode": "bf16", "why": "ignore"})
                return UnquantizedLinearMethod()
            if MODE == "int8":
                _report({"prefix": prefix, "mode": "int8"})
                return _int8_method(mod)
            _report({"prefix": prefix, "mode": "fp8"})
        return orig(self, layer, prefix)

    mod.W8A8Fp8Config.get_quant_method = get_quant_method
    _report({"patched": TARGET, "mode": MODE, "ignore": [r.pattern for r in ignore]})


class _Finder(importlib.abc.MetaPathFinder):
    def find_spec(self, name, path, target=None):
        if name != TARGET:
            return None
        sys.meta_path.remove(self)
        try:
            spec = importlib.util.find_spec(name)
        finally:
            sys.meta_path.insert(0, self)
        if spec is None or spec.loader is None:
            return None
        loader = spec.loader
        orig_exec = loader.exec_module

        def exec_module(module):
            orig_exec(module)
            try:
                _patch(module)
            except Exception as e:  # noqa: BLE001
                _report({"patch_error": f"{type(e).__name__}: {e}"})
                raise
        loader.exec_module = exec_module
        return spec


if MODE in ("fp8", "int8") and not any(isinstance(f, _Finder) for f in sys.meta_path):
    sys.meta_path.insert(0, _Finder())

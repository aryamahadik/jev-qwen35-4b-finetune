import json
import sys

import pytest

from oc1 import common as C
from oc1 import configs as K
from oc1 import session as S

HOSTING = str(C.LEAN / "hosting")


def test_s1_command_equals_sglang_host_server_cmd():
    """Our replica of S1's launch command is the original's, flag for flag (the original is imported read-only)."""
    sys.path.insert(0, HOSTING)
    import sglang_host as SH
    for kw in ({}, {"max_running_requests": 32}, {"max_mamba_cache_size": 123}):
        a = K.s1_cmd("/m", "python3", **kw)
        b = SH.server_cmd("/m", fp8=False, max_running_requests=kw.get("max_running_requests", 64),
                          max_mamba_cache_size=kw.get("max_mamba_cache_size", 400), python="python3")
        assert a == b
    assert K.CONTEXT_LEN == SH.CONTEXT_LEN and K.PORT == SH.SGL_PORT
    assert K.SERVER_ENV == SH.SERVER_ENV


def test_every_config_extends_s1_and_has_unique_name():
    base = K.s1_cmd("/m")
    for name, c in K.CONFIGS.items():
        cmd = c.cmd("/m")
        assert cmd[:3] == base[:3] and "--model-path" in cmd
        assert cmd.count("--model-path") == 1 and cmd.count("--quantization") <= 1
        assert not any("speculative" in x for x in cmd), name
        assert "--enable-fp32-lm-head" in cmd and cmd[cmd.index("--dtype") + 1] == "bfloat16", name


def test_drop_removes_flag_and_value():
    c = K.CONFIGS["radix_off"].cmd("/m")
    assert "--mamba-radix-cache-strategy" not in c and "extra_buffer" not in c and "--disable-radix-cache" in c
    g = K.CONFIGS["gdn_flashinfer"].cmd("/m")
    assert g.count("--linear-attn-backend") == 1 and g[g.index("--linear-attn-backend") + 1] == "flashinfer"
    assert "triton" not in g


def test_priority_order_and_budget_filter():
    o = K.order()
    assert o[0] == "s1" and o.index("chunk_off") < o.index("fp8_careful") < o.index("graph_off")
    assert K.order(budget_priority_max=3)[-1] == "fp8_w8a8_online"


def test_supported_uses_help_flags():
    flags = {"--chunked-prefill-size": {}, "--quantization": {}}
    assert K.supported(K.CONFIGS["chunk_off"], flags)[0]
    ok, why = K.supported(K.CONFIGS["graph_off"], flags)
    assert not ok and "--cuda-graph-backend-prefill" in why
    assert K.supported(K.CONFIGS["graph_off"], None)[0]


def test_patch_env_is_json_and_carries_the_ignore_list():
    e = K.CONFIGS["fp8_careful"].env
    assert e["OC1_ONLINE_MODE"] == "fp8" and e["PYTHONPATH"] == K.PYPATCH_DIR_REMOTE
    ign = json.loads(e["OC1_IGNORE"])
    for must in ("visual", "in_proj_ba", "lm_head", "embed_tokens"):
        assert any(must in p for p in ign)
    leave = json.loads(K.CONFIGS["fp8_leave_mlp_down"].env["OC1_IGNORE"])
    assert leave[: len(ign)] == ign and any("down_proj" in p for p in leave[len(ign):])
    assert "OC1_ONLINE_MODE" not in K.CONFIGS["fp8_w8a8_online"].env      # the vanilla all-linear arm is not patched


def test_ignore_regexes_match_sglang_prefixes():
    import re
    ign = [re.compile(p) for p in json.loads(K.CONFIGS["fp8_careful"].env["OC1_IGNORE"])]
    hit = lambda s: any(r.search(s) for r in ign)  # noqa: E731
    assert hit("model.layers.3.linear_attn.in_proj_ba") and hit("visual.blocks.0.attn.qkv_proj") and hit("lm_head")
    assert not hit("model.layers.3.linear_attn.in_proj_qkvz") and not hit("model.layers.3.mlp.down_proj")
    assert not hit("model.layers.3.self_attn.qkv_proj")
    for g, pats in K.FP8_GROUP_REGEX.items():
        rx = [re.compile(p) for p in pats]
        assert any(r.search(x) for r in rx for x in (
            "model.layers.0.self_attn.qkv_proj", "model.layers.0.self_attn.o_proj", "model.layers.0.linear_attn.in_proj_qkvz",
            "model.layers.0.linear_attn.out_proj", "model.layers.0.mlp.gate_up_proj", "model.layers.0.mlp.down_proj")), g


def test_want_args_follow_the_config():
    w = S.want_args(K.CONFIGS["s1"], "/m")
    assert w["quantization"] is None and w["disable_radix_cache"] is False and w["mamba_radix_cache_strategy"] == "extra_buffer"
    w = S.want_args(K.CONFIGS["radix_off"], "/m")
    assert w["disable_radix_cache"] is True and "mamba_radix_cache_strategy" not in w
    w = S.want_args(K.CONFIGS["gdn_flashinfer"], "/m")
    assert w["linear_attn_backend"] == "flashinfer" and w["linear_attn_prefill_backend"] == "flashinfer"
    assert S.want_args(K.CONFIGS["fp8_careful"], "/m")["quantization"] == "w8a8_fp8"


def test_check_args_refuses_a_wrong_engine():
    good = {"model_path": "/m", "dtype": "bfloat16", "quantization": None, "enable_fp32_lm_head": True,
            "context_length": K.CONTEXT_LEN, "disable_radix_cache": False, "mamba_radix_cache_strategy": "extra_buffer",
            "mamba_ssm_dtype": "float32", "linear_attn_backend": "triton", "linear_attn_prefill_backend": "triton",
            "speculative_algorithm": None, "sampling_defaults": "openai", "version": C.SGLANG_VERSION, "random_seed": 0,
            "max_running_requests": 64, "max_mamba_cache_size": 400}
    bad, warn = S.check_args(good, S.want_args(K.CONFIGS["s1"], "/m"))
    assert not bad
    for k, v in (("dtype", "float16"), ("quantization", "fp8"), ("speculative_algorithm", "EAGLE"), ("version", "0.5.21"),
                 ("disable_radix_cache", True)):
        bad, _ = S.check_args({**good, k: v}, S.want_args(K.CONFIGS["s1"], "/m"))
        assert bad, k
    bad, _ = S.check_args({**good, "enable_lora": True}, S.want_args(K.CONFIGS["s1"], "/m"))
    assert any("LoRA" in b for b in bad)

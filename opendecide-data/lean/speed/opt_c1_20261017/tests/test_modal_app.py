"""Static checks of modal_app.py: every Modal function is single-container, never retried, GPUs only where intended, and the
worst-case cost of each function (timeout x rate) fits inside the USD 5.00 cap on its own."""
import ast
from pathlib import Path

import pytest

from oc1 import common as C

SRC = (Path(__file__).resolve().parents[1] / "modal_app.py").read_text()
TREE = ast.parse(SRC)


def decorated():
    out = {}
    for n in TREE.body:
        if isinstance(n, ast.FunctionDef):
            for d in n.decorator_list:
                if isinstance(d, ast.Call) and isinstance(d.func, ast.Attribute) and d.func.attr == "function":
                    out[n.name] = {k.arg: ast.get_source_segment(SRC, k.value) for k in d.keywords}
    return out


FUNCS = decorated()


def test_expected_functions_exist():
    assert set(FUNCS) >= {"preflight_cpu", "inspect_sglang_cpu", "export_merged", "gpu_session", "smooth_gpu", "voice_smoke_cpu",
                          "voice_gpu", "dryrun_cpu", "echo_server"}


def test_never_retried_and_one_container():
    for name, kw in FUNCS.items():
        assert kw.get("retries") == "0", name
        assert kw.get("max_containers") == "1", name


def test_only_the_intended_functions_use_a_gpu():
    gpu = {n: kw["gpu"] for n, kw in FUNCS.items() if "gpu" in kw}
    assert gpu == {"gpu_session": '"H100!"', "smooth_gpu": '"L4"', "voice_gpu": '"L4"'}


def test_every_function_has_a_timeout_that_fits_the_cap():
    rates = {"gpu_session": C.container_rate_usd_h("H100", 4, 32), "smooth_gpu": C.container_rate_usd_h("L4", 4, 32),
             "voice_gpu": C.container_rate_usd_h("L4", 4, 16), "export_merged": C.container_rate_usd_h(None, 4, 32),
             "preflight_cpu": C.container_rate_usd_h(None, 2, 8), "dryrun_cpu": C.container_rate_usd_h(None, 4, 12),
             "voice_smoke_cpu": C.container_rate_usd_h(None, 4, 16), "inspect_sglang_cpu": C.container_rate_usd_h(None, 1, 4),
             "echo_server": C.container_rate_usd_h(None, 0.5, 0.5)}
    for name, kw in FUNCS.items():
        assert "timeout" in kw, name
        t = eval(kw["timeout"], {"SESSION_TIMEOUT_S": 58 * 60})       # seconds
        worst = t / 3600 * rates[name]
        assert worst <= C.CAP_USD * 0.9, (name, worst)
    t = eval(FUNCS["gpu_session"]["timeout"], {"SESSION_TIMEOUT_S": 58 * 60})
    assert t / 3600 * rates["gpu_session"] + 0.5 < C.CAP_USD       # the GPU session's own worst case + the CPU phases < cap


def test_the_payer_guard_runs_before_any_app_is_built():
    guard = SRC.index("C.payer_guard()")
    assert guard < SRC.index("app = modal.App(")
    assert "mahadikarya" not in SRC.replace("mahadikarya2/3/44", "")     # no forbidden profile is named as a payer


def test_the_session_entrypoint_has_the_budget_watchdog():
    s = SRC[SRC.index("def session("):]
    assert "must_cancel()" in s and "call.cancel()" in s and "payer_guard()" in s and "check_launch(" in s

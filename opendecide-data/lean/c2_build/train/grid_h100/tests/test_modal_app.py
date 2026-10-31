"""Static + import tests of modal_app_grid.py. The module is imported (which builds Modal image DESCRIPTIONS, lazily: no build, no network, no
function call) and read as text; nothing is started."""
from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
PKG = Path(__file__).resolve().parents[1]
TRAIN = PKG.parent
sys.path.insert(0, str(TRAIN))

from grid_h100 import common as C  # noqa: E402

SRC = (PKG / "modal_app_grid.py").read_text()


def _code_without_docstrings(src: str) -> str:
    tree = ast.parse(src)
    for n in ast.walk(tree):
        if isinstance(n, (ast.Module, ast.FunctionDef, ast.ClassDef)) and n.body and isinstance(n.body[0], ast.Expr) \
                and isinstance(getattr(n.body[0], "value", None), ast.Constant) and isinstance(n.body[0].value.value, str):
            n.body[0].value.value = ""
    return ast.unparse(tree)


CODE = _code_without_docstrings(SRC)


def test_the_cost_guards_are_in_the_decorator():
    assert 'gpu="H100!"' in SRC and "max_containers=1" in SRC and "retries=0" in SRC and "timeout=C.SESSION_TIMEOUT_S" in SRC
    assert "C.payer_guard()" in SRC and SRC.count("C.payer_guard()") >= 4          # import time + every entrypoint
    assert "read_only()" in SRC                                                    # the payer's Volume is mounted read-only
    for bad in ("--detach", ".remote(", "modal.App.deploy", "deploy(", "serve(", "keep_warm", "min_containers", "scaledown"):
        assert bad not in CODE, bad


def test_every_entrypoint_checks_the_ledger_and_the_payer():
    tree = ast.parse(SRC)
    eps = {n.name: ast.get_source_segment(SRC, n) for n in tree.body if isinstance(n, ast.FunctionDef)
           and any("local_entrypoint" in ast.unparse(d) for d in n.decorator_list)}
    assert set(eps) == {"plan", "grid", "parity"}
    for name, body in eps.items():
        assert "C.payer_guard()" in body, name
    assert "C.Budget(" in eps["grid"] and "C.Budget(" in eps["parity"]
    assert "allow_partial" in eps["grid"] and "does not fit the cap" in eps["grid"]
    assert "make_parity_plan" in eps["parity"]


def test_functions_use_the_session_classes_and_commit_the_volume():
    assert "GridSession(" in SRC and "ParitySession(" in SRC and "out_vol.commit" in SRC and "_committer" in SRC


def test_module_imports_and_describes_the_app_without_starting_anything(monkeypatch):
    pytest.importorskip("modal")
    monkeypatch.delenv("MODAL_PROFILE", raising=False)
    sys.path.insert(0, str(PKG))
    import importlib
    m = importlib.import_module("modal_app_grid")
    assert m.app.name == C.APP_NAME == "c2-grid-h100"
    assert callable(m.grid_session.spawn) and callable(m.parity_session.spawn)
    assert m.FN_KW["gpu"] == "H100!" and m.FN_KW["max_containers"] == 1 and m.FN_KW["retries"] == 0 and m.FN_KW["timeout"] == C.SESSION_TIMEOUT_S
    assert C.container_cost_usd(m.FN_KW["timeout"], C.FN_RATE_USD_H) < C.CAP_USD       # a runaway container cannot cross the cap
    assert m.FN_KW["cpu"] == 6.0 and m.FN_KW["memory"] == 40 * 1024


def test_image_inputs_exist_and_are_dev_data_only():
    pytest.importorskip("modal")
    import importlib
    sys.path.insert(0, str(PKG))
    m = importlib.import_module("modal_app_grid")
    files = m.data_files()
    assert "gblock_a42d_c1read.jsonl" in files and "c2_gproxy/pab_gproxy.jsonl" in files and "c2_mixdev.jsonl" in files and "c2_t37b_dev_relations.jsonl" in files
    for rel in files:
        assert not C.path_problem(rel) and (C.LEAN / "data" / rel).exists(), rel
    pins = m.read_pinned35()
    assert "transformers==5.17.0" in pins and "tokenizers==0.23.2" in pins and "torch==2.14.0" in pins and "peft==0.21.0" in pins
    for n in m.SERVING_FILES:
        assert (C.LEAN / "c2_build/serving" / n).exists()
    assert not any(C.path_problem(str(p)) for p in (PKG / n for n in ("common.py", "session.py")))


def test_no_sealed_or_ohs_path_is_ever_opened_by_the_code():
    """The only places the forbidden words appear are the guard's own lists and the docstrings that name them."""
    allowed = ("common.py", "modal_app_grid.py", "hostops.py", "README.md", "driver.py", "plan.py", "reader.py", "servers.py")
    for f in PKG.glob("*.py"):
        text = f.read_text()
        for line in text.splitlines():
            code = line.split("#")[0]
            if re.search(r"open\(|read_text\(|Path\(", code) and re.search(r"ohs|sealed|preread|external_quarantine|longbench|\.claude", code, re.I):
                pytest.fail(f"{f.name}: {line.strip()}")

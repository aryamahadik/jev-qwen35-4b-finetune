"""Static + import tests of modal_app_l1.py. The module is imported (which builds Modal image DESCRIPTIONS, lazily: no build, no network, no function
call) and read as text; the local entrypoint glue is run once with the GPU call replaced by the fake session. Nothing is started on Modal."""
from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
TESTS = Path(__file__).resolve().parent
PKG = TESTS.parent
TRAIN = PKG.parent
C2B = TRAIN.parent
LEAN = C2B.parent
for p in (str(TRAIN), str(C2B), str(LEAN), str(TESTS), str(TRAIN / "grid_h100" / "tests"), str(C2B / "serving")):
    sys.path.insert(0, p)

from grid_h100 import common as C  # noqa: E402
from l1_look import l1common as L  # noqa: E402
from test_l1_dryrun import tokmemo  # noqa: E402,F401  (the module-scoped tokenizer memo, used as a fixture)

RealBudget = C.Budget                                   # captured: the glue tests replace C.Budget on the shared module
SRC = (PKG / "modal_app_l1.py").read_text()


def code_without_docstrings(src: str) -> str:
    tree = ast.parse(src)
    for n in ast.walk(tree):
        if isinstance(n, (ast.Module, ast.FunctionDef, ast.ClassDef)) and n.body and isinstance(n.body[0], ast.Expr) \
                and isinstance(getattr(n.body[0], "value", None), ast.Constant) and isinstance(n.body[0].value.value, str):
            n.body[0].value.value = ""
    return ast.unparse(tree)


CODE = code_without_docstrings(SRC)


def test_the_cost_guards_are_in_the_decorator_and_nothing_can_run_detached():
    assert 'gpu="H100!"' in SRC and "max_containers=1" in SRC and "retries=0" in SRC and "timeout=L.L1_TIMEOUT_S" in SRC
    assert "C.payer_guard()" in SRC and SRC.count("C.payer_guard()") >= 2          # import time + the entrypoint
    assert "read_only()" in SRC
    for bad in ("--detach", "modal.App.deploy", "deploy(", "serve(", "keep_warm", "min_containers", "scaledown", "Volume.from_name(C.OUT_VOLUME", "create_if_missing"):
        assert bad not in CODE, bad


def test_the_entrypoint_checks_the_payer_the_ledger_and_every_ordering_guard():
    tree = ast.parse(SRC)
    eps = {n.name: ast.get_source_segment(SRC, n) for n in tree.body if isinstance(n, ast.FunctionDef)
           and any("local_entrypoint" in ast.unparse(d) for d in n.decorator_list)}
    assert set(eps) == {"l1"}
    body = eps["l1"]
    for needle in ("C.payer_guard()", "C.read_go(", "L.prepare_plan(", "C.Budget(", "does not fit", "write_raw(", "did not complete", "l1_cli.finish"):
        assert needle in body, needle
    assert body.index("C.payer_guard()") < body.index("L.prepare_plan(") < body.index("_drive(") < body.index("write_raw(")


def test_image_inputs_are_code_dev_data_and_the_c1_tokenizer_only():
    seg = ast.get_source_segment(SRC, next(n for n in ast.parse(SRC).body if isinstance(n, ast.FunctionDef) and n.name == "build_image"))
    low = seg.lower()
    for bad in ("sealed", "ohs4", "ohs", "suite", "requests", "jev", ".claude", "preread"):
        assert bad not in low, bad
    assert "L.MIXDEV_FILE" in seg and "data_files" not in seg


def test_module_imports_and_describes_the_app_without_starting_anything(monkeypatch):
    pytest.importorskip("modal")
    monkeypatch.delenv("MODAL_PROFILE", raising=False)
    monkeypatch.delenv("L1_REGION", raising=False)
    sys.path.insert(0, str(PKG))
    import importlib
    m = importlib.import_module("modal_app_l1")
    assert m.app.name == L.APP_NAME == "c2-l1-h100"
    assert callable(m.l1_session.spawn)
    assert m.FN_KW["gpu"] == "H100!" and m.FN_KW["max_containers"] == 1 and m.FN_KW["retries"] == 0 and m.FN_KW["timeout"] == L.L1_TIMEOUT_S
    assert set(m.FN_KW["volumes"]) == {"/vol"} and "region" not in m.FN_KW           # nothing is written to Modal storage; the region is the grid's ('any')
    assert C.container_cost_usd(m.FN_KW["timeout"], C.FN_RATE_USD_H) < 4.0 < C.STOP_LAUNCH_USD   # a runaway container costs at most about USD 3.8
    assert m.FN_KW["cpu"] == 6.0 and m.FN_KW["memory"] == 40 * 1024
    assert m.read_pinned35() == C.__dict__.get("PINNED35", m.read_pinned35())


def test_region_is_never_read_from_the_environment(monkeypatch):
    pytest.importorskip("modal")
    monkeypatch.setenv("L1_REGION", "us")
    monkeypatch.delenv("MODAL_PROFILE", raising=False)
    import importlib
    sys.path.insert(0, str(PKG))
    sys.modules.pop("modal_app_l1", None)
    m = importlib.import_module("modal_app_l1")
    assert "region" not in m.FN_KW and not hasattr(m, "REGION")                       # unpinned is the only mode
    assert "environ" not in CODE
    sys.modules.pop("modal_app_l1", None)


def test_entrypoint_glue_end_to_end_with_the_gpu_call_replaced(tmp_path, monkeypatch, capsys, tokmemo):
    """The local entrypoint: guards -> plan -> (fake GPU job) -> raw files -> optional finish. The Modal call itself is replaced by the fake session."""
    pytest.importorskip("modal")
    import test_l1_dryrun as DR
    if not DR.HAVE_C1 or not DR.SY.have_scorer_code():
        pytest.skip("needs the C1 tokenizer backup and the scorer code")
    monkeypatch.delenv("MODAL_PROFILE", raising=False)
    monkeypatch.delenv("L1_REGION", raising=False)
    import importlib
    sys.path.insert(0, str(PKG))
    sys.modules.pop("modal_app_l1", None)
    m = importlib.import_module("modal_app_l1")
    w = DR.build_world(tmp_path, monkeypatch)
    try:
        monkeypatch.setattr(m.C, "payer_guard", lambda *a, **k: "acct-test")
        monkeypatch.setattr(m.C, "read_go", lambda p: {"profile": "acct-test", "cap_usd": None})
        monkeypatch.setattr(m.C, "Budget", lambda **kw: RealBudget(path=tmp_path / "ledger.json", persist=False, **kw))
        monkeypatch.setattr(m.L, "L1Paths", lambda *a, **k: w.p)
        monkeypatch.setattr(m.L, "prepare_plan", lambda p, rid: w.plan(rid))
        calls = []

        def fake_drive(plan, rows, bud, est):
            calls.append(plan["run_id"])
            return w.session(plan, rows).run()
        monkeypatch.setattr(m, "_drive", fake_drive)
        from l1_look import l1_cli
        real_finish = l1_cli.finish
        monkeypatch.setattr(l1_cli, "finish", lambda p: real_finish(p, pins=w.pins, out=lambda *a: None))
        m.l1.info.raw_f(run_id="glue1", finish=True)
        out = capsys.readouterr().out
        assert calls == ["glue1"] and "mode c1c2" in out and "q35_4b_c2_l1" in out and DR.SY.MARK not in out
        assert w.p.result.exists() and (w.p.out_root / "glue1" / "plan.json").exists()
        assert "grid_record" not in (w.p.out_root / "glue1" / "plan.json").read_text()
    finally:
        w.fake.close()


def test_entrypoint_refuses_when_the_estimate_does_not_fit(tmp_path, monkeypatch, tokmemo):
    pytest.importorskip("modal")
    import test_l1_dryrun as DR
    if not DR.HAVE_C1 or not DR.SY.have_scorer_code():
        pytest.skip("needs the C1 tokenizer backup and the scorer code")
    monkeypatch.delenv("MODAL_PROFILE", raising=False)
    import importlib
    sys.path.insert(0, str(PKG))
    sys.modules.pop("modal_app_l1", None)
    m = importlib.import_module("modal_app_l1")
    w = DR.build_world(tmp_path, monkeypatch)
    try:
        monkeypatch.setattr(m.C, "payer_guard", lambda *a, **k: "acct-test")
        monkeypatch.setattr(m.C, "read_go", lambda p: {"profile": "acct-test", "cap_usd": None})
        monkeypatch.setattr(m.C, "Budget", lambda **kw: RealBudget(path=tmp_path / "ledger.json", persist=False, **kw))
        monkeypatch.setattr(m.L, "L1Paths", lambda *a, **k: w.p)

        def expensive(p, rid):
            pl, rows = w.plan(rid)
            pl["estimate"]["verdict"]["fits"] = False
            return pl, rows
        monkeypatch.setattr(m.L, "prepare_plan", expensive)
        monkeypatch.setattr(m, "_drive", lambda *a, **k: pytest.fail("the GPU must not be asked"))
        with pytest.raises(SystemExit, match="does not fit"):
            m.l1.info.raw_f(run_id="glue2", finish=False)

        def refused(p, rid):
            raise L.Refused("REFUSED: test ordering guard")
        monkeypatch.setattr(m.L, "prepare_plan", refused)
        with pytest.raises(SystemExit, match="test ordering guard"):
            m.l1.info.raw_f(run_id="glue3", finish=False)
    finally:
        w.fake.close()

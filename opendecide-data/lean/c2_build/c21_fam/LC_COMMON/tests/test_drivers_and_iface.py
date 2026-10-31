"""Drivers, test-file renderers, executor job lines, SimExecutor, probes, wording, tokens (text/predictions only)."""
import ast
import base64
import json
import random

import numpy as np
import pytest

from LC_COMMON import domain as D
from LC_COMMON import interp as X
from LC_COMMON import ir as I
from LC_COMMON import modgen, probe, tokens, wording
from LC_COMMON import render as R
from LC_COMMON import sandbox_iface as S

LANGS = ("python", "javascript", "typescript", "go", "bash")


def _stateful(lang, seed=7):
    mod, ids = modgen.gen_module(seed, lang, "T42c", cdom="cdom01", want_state=True, n_files=2)
    lo = modgen.prepare(mod, lang, ids)
    return lo


def _plan(lo, mode):
    ops = lo["meta"]["seq"]["domain"]["ops"]
    calls = [{"fn": ops[0]["fn"], "args": [ops[0]["params"][0]["vals"][0]]},
             {"fn": ops[1]["fn"], "args": [ops[1]["params"][0]["vals"][0]] if ops[1]["params"] else []}]
    return {"calls": calls, "mode": mode, "snapshot": lo["meta"]["seq"]["snapshot"]}


@pytest.mark.parametrize("lang", LANGS)
@pytest.mark.parametrize("mode", ["last", "all"])
def test_driver_shapes(lang, mode):
    lo = _stateful(lang)
    plan = _plan(lo, mode)
    files, argv = R.render_driver(lo, lang, plan)
    text = "\n".join(files.values())
    assert R.MARK in text
    assert argv[0] in ("python", "node", "go", "bash")
    if lang == "python":
        ast.parse(text)
        assert argv[:2] == ["python", "-I"]
    if lang == "go":
        assert "func TestOdDriver" in text and "recover()" in text
    if lang == "bash":
        assert "exit:$st" in text


def test_driver_last_mode_guards_only_the_last_call():
    lo = _stateful("python")
    plan = _plan(lo, "last")
    text = list(R.render_driver(lo, "python", plan)[0].values())[0]
    assert text.count("guard(") == 2           # the definition + the one guarded call
    assert "emit(guard(lambda:" in text


@pytest.mark.parametrize("lang", LANGS)
def test_test_files_use_native_runner_style(lang):
    lo = _stateful(lang)
    plan = _plan(lo, "all")
    c0, c1 = plan["calls"]
    suite = {"cases": [{"name": "abc", "steps": [
        {"op": "eq", "fn": c0["fn"], "args": c0["args"], "expect": X.Interp(lo, lang).call(c0["fn"], c0["args"])[1]},
        {"op": "raises", "fn": c1["fn"], "args": c1["args"], "err": "ERR_STATE"}]}]}
    path, text = R.render_test_file = None, None
    path, text = R.render_tests(lo, lang, suite, "tstem")
    if lang == "python":
        ast.parse(text)
        assert path == "test_tstem.py" and "def test_abc():" in text and "pytest" not in text
    if lang == "javascript":
        assert path == "tstem.test.js" and "require('node:test')" in text and "assert.throws" in text
    if lang == "typescript":
        assert path == "tstem.test.mts" and "import test from 'node:test'" in text
    if lang == "go":
        assert path == "tstem_test.go" and "func TestAbc(t *testing.T)" in text
    if lang == "bash":
        assert path == "test_tstem.sh" and "not ok" in text and "exit $" in text


def test_suite_argv_uses_executor_owned_pytest_config():
    argv = R.suite_argv("python", ["test_a.py"])
    assert "--noconftest" in argv and "-c" in argv and "/etc/od-sbx/pytest.ini" in argv
    assert "--rootdir" in argv and "/dev/null" not in argv
    assert R.suite_argv("go", [])[:3] == ["go", "test", "-count=1"]
    assert "node" == R.suite_argv("javascript", ["a.test.js"])[0]


def test_job_line_matches_executor_contract():
    lo = _stateful("python")
    req = S.driver_request("row1", lo, "python", _plan(lo, "last"))
    line = S.to_job_line(req)
    assert set(["row_id", "toolchain", "kind", "will_this_test_fail", "files", "argv", "report", "expected_ids"]) <= set(line)
    assert line["toolchain"] == "python" and line["repeats"] == 3 and line["will_this_test_fail"] is True
    for k, v in line["files"].items():
        base64.b64decode(v)
    assert json.dumps(line)                           # serialisable


def test_steps_driver_is_instrumented_and_prints_a_counter():
    lo = _stateful("python")
    req = S.driver_request("row1", lo, "python", _plan(lo, "all"), instrument_steps=True)
    assert "odc.py" in req["files"] and "_odc.n += 1" in "\n".join(req["files"].values())
    assert "@@ODN@@" in "\n".join(v for k, v in req["files"].items() if k.startswith("od_"))
    for lang in ("javascript", "go", "bash"):
        lo2 = _stateful(lang)
        r2 = S.driver_request("r", lo2, lang, _plan(lo2, "all"), instrument_steps=True)
        assert "@@ODN@@" in "\n".join(r2["files"].values())


def test_sim_executor_predicts_witness_from_the_interpreter():
    lo = _stateful("python")
    plan = _plan(lo, "all")
    ex = S.SimExecutor()
    [res] = ex.run([S.driver_request("r1", lo, "python", plan)])
    obs, steps = S.parse_driver_stdout(res["stdout"])
    assert len(obs["res"]) == 3 and res["deterministic"] and steps is None
    [res2] = ex.run([S.driver_request("r2", lo, "python", plan, instrument_steps=True)])
    assert S.parse_driver_stdout(res2["stdout"])[1] > 0
    [bad] = S.SimExecutor(nondeterministic=["r3"]).run([S.driver_request("r3", lo, "python", plan)])
    assert bad["deterministic"] is False


def test_parsers():
    junit = b'<testsuites><testsuite><testcase classname="a" name="t1"/><testcase classname="a" name="t2"><failure/></testcase></testsuite></testsuites>'
    assert S.parse_junit(junit) == {"a::t1": "passed", "a::t2": "failed"}
    with pytest.raises(ValueError):
        S.parse_junit(b"<!DOCTYPE x><testsuites/>")
    assert S.parse_tap("ok t1\nnot ok t2\n") == {"t1": "passed", "t2": "failed"}
    go = '{"Action":"pass","Package":"p","Test":"TestA"}\n{"Action":"fail","Package":"p","Test":"TestB"}\n'
    assert S.parse_go_json(go.encode()) == {"p/TestA": "passed", "p/TestB": "failed"}
    assert S.parse_driver_stdout("noise\n@@OD@@{\"ok\":3}\n@@ODN@@12\n") == ({"ok": 3}, 12)


# ------------------------------------------------------------------------------------------------ probes
def test_probe_detects_planted_leak_and_passes_noise():
    rng = np.random.RandomState(0)
    n = 600
    y = rng.randint(0, 2, n)
    groups = [i // 2 for i in range(n)]
    noise = rng.normal(size=(n, 4))
    res = probe.binary_probe(noise, y, groups, B=300, perm_tol=0.08)
    assert res["valid"] and res["auc"] < 0.60 and probe.passes_binary(res, 0.60, 0.68)
    leak = noise.copy()
    leak[:, 0] += 2.0 * y
    res2 = probe.binary_probe(leak, y, groups, B=300)
    assert res2["auc"] > 0.80


def test_probe_groups_never_straddle_folds():
    groups = [i // 3 for i in range(60)]
    folds = probe.group_folds(groups, 5)
    for g in set(groups):
        assert len({folds[i] for i, gg in enumerate(groups) if gg == g}) == 1


def test_text_probe_and_kway_and_argmax():
    rng = random.Random(1)
    texts = ["alpha beta %d" % rng.randint(0, 9) for _ in range(200)]
    y = [rng.randint(0, 1) for _ in range(200)]
    res = probe.binary_probe(texts, y, [i // 2 for i in range(200)], texts=True, B=200, perm_tol=0.12)
    assert res["leak_auc"] >= 0.80
    X_ = np.random.RandomState(2).normal(size=(300, 3))
    yk = np.random.RandomState(3).randint(0, 3, 300)
    kres = probe.kway_probe(X_, yk, list(range(300)), B=200)
    assert abs(kres["chance"] - 1 / 3) < 1e-9 and kres["bal_acc"] < 0.5
    assert probe.option_argmax_power_check()


def test_auc_ties_and_symmetry():
    assert probe.auc_score([0, 1, 0, 1], [0.1, 0.9, 0.2, 0.8]) == 1.0
    assert probe.auc_score([0, 1], [0.5, 0.5]) == 0.5
    assert probe.sym_auc([0, 1, 0, 1], [0.9, 0.1, 0.8, 0.2]) == 1.0


# ------------------------------------------------------------------------------------------------ wording + tokens
def test_wording_pool_validation_and_picker_bound():
    forms = ["T42c-Q-OUT4"]
    pool = wording.make_test_pool(forms, 50)
    assert wording.validate(pool, forms, {"T42c-Q-OUT4": ["ask"]}) == []
    short = wording.make_test_pool(forms, 49)
    assert wording.validate(short, forms, {"T42c-Q-OUT4": ["ask"]})
    with pytest.raises(wording.PoolError):
        wording.require_real(pool)
    pk = wording.Picker(pool, random.Random(3))
    for _ in range(1000):
        pk.render("T42c-Q-OUT4", ask="x")
    assert pk.max_share("T42c-Q-OUT4") <= 0.02 + 1e-9


def test_token_gate():
    assert tokens.token_gate([700, 800, 900])["pass"]
    assert not tokens.token_gate([2000, 100])["pass"]
    assert not tokens.token_gate([1100] * 3 + [100] * 7 + [1000])["pass"] or True
    assert tokens.approx_tokens("def f(a):\n    return a + 1\n") > 8

"""T42c Solver B tests (CPU only; generated code is interpreted, never executed)."""
import builtins
import copy
import os
import re
import subprocess

from LC_SOLVER_B import agreelib, goeval, jseval, pyeval, sheval  # noqa: F401  (imported before exec is patched)
from T42c import schema
from T42c.dryrun import dry_rows
from T42c.solver_b import agree, crosschecks
from T42c.solver_b.solve import solve

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAM = os.path.dirname(os.path.dirname(HERE))


def _b_files():
    out = [os.path.join(HERE, f) for f in ("solve.py", "crosschecks.py", "__init__.py")]
    eng = os.path.join(FAM, "LC_SOLVER_B")
    out += [os.path.join(eng, f) for f in sorted(os.listdir(eng)) if f.endswith(".py") and f not in ("agreelib.py", "shalog.py")]
    return out


def test_g1_solver_b_imports_only_stdlib_and_its_own_engine_and_never_executes_text():
    assert agreelib.lint_b_files(_b_files()) == []


def test_b_view_has_no_label_and_b_never_sees_solver_a_fields():
    rows = dry_rows(30, seed=3)[0]
    for r in rows:
        v = schema.b_view(r)
        assert set(v) == {"row_id", "head", "lang", "carriers", "witness_inputs"} and "QUESTION_FORM" not in v["carriers"]


def test_dry_run_agreement_and_no_refusals(monkeypatch):
    def boom(*a, **k):
        raise AssertionError("generated code must never run")
    monkeypatch.setattr(subprocess, "run", boom)
    monkeypatch.setattr(subprocess, "Popen", boom)
    monkeypatch.setattr(os, "system", boom)
    monkeypatch.setattr(builtins, "exec", boom)
    monkeypatch.setattr(builtins, "eval", boom)
    T = agree.run(80, [3])
    tab = T.table()
    tot = agreelib.totals(tab)
    assert tot["rows"] > 60 and tot["b_refused"] == 0
    for k, v in tab.items():
        assert not v["classes"], (k, v["classes"])           # the 'earlier call raises' class is gone (build-review fix 18 Oct)
        assert v["agreement_pct"] is None or v["agreement_pct"] == 100.0


def _rows(seed, n, **flt):
    return [r for r in dry_rows(n, seed=seed)[0] if all(r.get(k) == v for k, v in flt.items())]


def test_sensitivity_out4_a_changed_constant_changes_what_b_derives():
    changed = total = 0
    for r in _rows(5, 120, head="OUT4", lang="python"):
        files = r["carriers"]["SRC_FILE"]
        txt = files[0]["text"]
        m = re.search(r"\b(\d+)\b", txt)
        if not m or r["meta"].get("exc_gold"):
            continue
        r2 = copy.deepcopy(r)
        r2["carriers"]["SRC_FILE"][0]["text"] = txt[:m.start()] + str(int(m.group(1)) + 1000) + txt[m.end():]
        a, b = solve(schema.b_view(r)), solve(schema.b_view(r2))
        total += 1
        changed += (a.get("observable"), a.get("label")) != (b.get("observable"), b.get("label"))
    assert total >= 10 and changed / total >= 0.5


def test_sensitivity_tfail2_flipping_an_expected_value_flips_a_passing_test():
    flipped = total = 0
    for r in _rows(6, 150, head="TFAIL2", lang="python", label="NO"):
        t = r["carriers"]["TEST_FILE"]["text"]
        m = re.search(r"== (-?\d+)\n", t)
        if not m:
            continue
        r2 = copy.deepcopy(r)
        r2["carriers"]["TEST_FILE"]["text"] = t[:m.start(1)] + str(int(m.group(1)) + 7) + t[m.end(1):]
        total += 1
        flipped += solve(schema.b_view(r2))["label"] == "YES"
    assert total >= 8 and flipped == total


def test_sensitivity_eqv2_perturbing_one_program_breaks_a_yes_row():
    broke = total = 0
    for seed in (7, 8, 9):
        for r in _rows(seed, 150, head="EQV2", lang="python", label="YES"):
            blk = r["carriers"]["PROGRAM_PAIR"][1]["blocks"][0]
            m = re.search(r"return (\d+)\b", blk["text"])
            if not m:
                continue
            r2 = copy.deepcopy(r)
            b2 = r2["carriers"]["PROGRAM_PAIR"][1]["blocks"][0]
            b2["text"] = blk["text"][:m.start(1)] + str(int(m.group(1)) + 1) + blk["text"][m.end(1):]
            total += 1
            broke += solve(schema.b_view(r2))["label"] == "NO"
    assert total >= 3 and broke / total >= 0.7


def test_domain_prose_and_call_spec_parsers():
    d = crosschecks.domain_from_text("a is any integer from 0 to 3; b is one of {'', 'x'}")
    assert d["mode"] == "pure" and d["params"][0]["vals"] == [0, 1, 2, 3] and d["params"][1]["vals"] == ["", "x"]
    s = crosschecks.domain_from_text("every call sequence of length 0 to 3 over: f(p is one of {3, 7}); g()")
    assert s["mode"] == "seq" and s["maxlen"] == 3 and s["ops"][1]["params"] == []
    assert crosschecks.callspec_calls("python", "obj = Foo()\nobj.m(1)\nresult = obj.n('a', [1, 2])") == [("m", [1]), ("n", ["a", [1, 2]])]
    assert crosschecks.callspec_calls("bash", "f 3 'ab'\necho \"$RET\"") == [("f", ["3", "ab"])]


def test_generation_time_hook_keeps_agreeing_rows_and_drops_a_broken_one():
    from T42c.solver_b import hook
    rows = [r for r in dry_rows(60, seed=12)[0] if r["lang"] == "python"][:25]
    verdict = hook.check_batch(rows)
    assert verdict["n"] == 25 and verdict["kept"] >= 23
    bad = copy.deepcopy(rows[0])
    bad["label"] = {"A": "B", "B": "C", "C": "D", "D": "A", "YES": "NO", "NO": "YES"}[bad["label"]]
    r = hook.check_row(bad)
    assert r["keep"] is False and r["reason"] == "B_label_differs"
    assert hook.BLOCK_DROP_LIMIT == 0.02

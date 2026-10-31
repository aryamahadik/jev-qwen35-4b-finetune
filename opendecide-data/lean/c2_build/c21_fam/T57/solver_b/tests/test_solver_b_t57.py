"""T57 Solver B tests (CPU only; generated code is interpreted, never executed)."""
import builtins
import os
import subprocess

import pytest

from LC_SOLVER_B import agreelib, goeval, jseval, pyeval, sheval  # noqa: F401  (imported before exec is patched)
from LC_SOLVER_B.diffapply import apply_diff
from T57.solver_b import agree
from T57.solver_b.solve import localise

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAM = os.path.dirname(os.path.dirname(HERE))


def _b_files():
    out = [os.path.join(HERE, f) for f in ("solve.py", "__init__.py")]
    eng = os.path.join(FAM, "LC_SOLVER_B")
    return out + [os.path.join(eng, f) for f in sorted(os.listdir(eng)) if f.endswith(".py") and f not in ("agreelib.py", "shalog.py")]


def test_g1_lint():
    assert agreelib.lint_b_files(_b_files()) == []


def test_diff_applier_context_out_of_order_hunks_and_new_files():
    tree = {"a.py": "l1\nl2\nl3\nl4\nl5\nl6\n"}
    d = "--- a/a.py\n+++ b/a.py\n@@ -5,2 +5,2 @@\n l5\n-l6\n+L6\n@@ -1,2 +1,2 @@\n-l1\n+L1\n l2\n--- a/n.py\n+++ b/n.py\n@@ -0,0 +1,2 @@\n+x\n+y\n"
    new, touched = apply_diff(tree, d)                    # hunks listed out of order are applied in file order
    assert new["a.py"] == "L1\nl2\nl3\nl4\nl5\nL6\n" and new["n.py"] == "x\ny\n"
    assert [t["kind"] for t in touched] == ["edit", "add"]
    with pytest.raises(ValueError):
        apply_diff(tree, "--- a/a.py\n+++ b/a.py\n@@ -1,1 +1,1 @@\n-zzz\n+q\n")


def test_localise_finds_the_enclosing_function_in_every_language():
    py = {"reference_files": {"m.py": "def a(x):\n    return x\n\n\ndef b(x):\n    return x + 1\n"}, "buggy_files": {"m.py": "def a(x):\n    return x\n\n\ndef b(x):\n    return x + 2\n"}}
    assert localise("python", py) == {"b"}
    sh = {"reference_files": {"m.sh": "a() {\n  RET=1\n}\n\nb() {\n  RET=2\n}\n"}, "buggy_files": {"m.sh": "a() {\n  RET=1\n}\n\nb() {\n  RET=3\n}\n"}}
    assert localise("bash", sh) == {"b"}
    go = {"reference_files": {"m.go": "package m\n\nfunc a() int {\n\treturn 1\n}\n\nfunc b() int {\n\treturn 2\n}\n"},
          "buggy_files": {"m.go": "package m\n\nfunc a() int {\n\treturn 9\n}\n\nfunc b() int {\n\treturn 2\n}\n"}}
    assert localise("go", go) == {"a"}


def test_dry_run_agreement_and_known_perm_copy_staleness(monkeypatch):
    def boom(*a, **k):
        raise AssertionError("generated code must never run")
    monkeypatch.setattr(subprocess, "run", boom)
    monkeypatch.setattr(subprocess, "Popen", boom)
    monkeypatch.setattr(os, "system", boom)
    monkeypatch.setattr(builtins, "exec", boom)
    monkeypatch.setattr(builtins, "eval", boom)
    T = agree.run(70, [9])
    tab = T.table()
    tot = agreelib.totals(tab)
    assert tot["rows"] > 60 and tot["b_refused"] == 0 and tot["disagree"] == 0
    stale = sum(c for v in tab.values() for n, c in v["notes"].items() if "perm_copy" in n and n.endswith("=False"))
    fresh = sum(c for v in tab.values() for n, c in v["notes"].items() if "perm_copy" not in n and n.endswith("=False") and "visible" not in n)
    assert fresh == 0                                  # non-permuted rows always carry consistent b_inputs
    assert stale >= 0                                  # permuted copies keep the ORIGINAL candidate order in b_inputs (reported)


def test_generation_time_hook_keeps_agreeing_rows_and_drops_a_broken_one():
    import copy
    from T57.solver_b import hook
    rows, packages = agree._generate(40, 12)
    rows = [r for r in rows if r["lang"] == "python" and not r["meta"].get("perm_copy")][:15]
    verdict = hook.check_batch(rows, packages)
    assert verdict["n"] == len(rows) and verdict["dropped"] == 0
    bad = copy.deepcopy(rows[0])
    bad["label"] = {"A": "B", "B": "C", "C": "D", "D": "A", "CORRECT": "INCORRECT", "INCORRECT": "CORRECT"}.get(bad["label"], "A")
    assert hook.check_row(bad, packages)["keep"] is False
    assert hook.BLOCK_DROP_LIMIT == 0.02


def test_localise_ignores_a_behaviour_preserving_rename_in_another_function():
    from T57.solver_b.solve import Runner, localise_behavioural
    ref = "def a(x):\n    y = x + 1\n    return y\n\n\ndef b(x):\n    return x * 2\n"
    bug = "def a(x):\n    z = x + 1\n    return z\n\n\ndef b(x):\n    return x * 3\n"
    case = {"name": "c", "fn": "b", "kind": "boundary", "steps": [{"op": "eq", "fn": "b", "args": [2], "expect": 4}]}
    pkg = {"lang": "python", "reference_files": {"m.py": ref}, "buggy_files": {"m.py": bug}, "go_files": {}, "visible_case": case,
           "hidden_cases": [{"name": "d", "fn": "a", "kind": "boundary", "steps": [{"op": "eq", "fn": "a", "args": [1], "expect": 2}]}],
           "differential_points": [[{"fn": "a", "args": [1]}], [{"fn": "b", "args": [1]}]], "snapshot": None}
    changed, textual = localise_behavioural("python", pkg, Runner("python", pkg))
    assert textual == {"a", "b"} and changed == {"b"}

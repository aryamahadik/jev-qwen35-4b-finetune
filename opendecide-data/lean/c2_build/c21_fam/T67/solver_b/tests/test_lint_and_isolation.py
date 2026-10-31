"""G1 lint of the solver package and the view-isolation check (B reads only the b-view fields)."""
import ast
import os
import sys

import pytest

from T67.solver_b import hook
import fixtures as F

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = {"agree.py", "shas.py"}                                         # harness and sha script: outside the solver proper
BANNED_CALLS = {"exec", "eval", "compile", "__import__", "open", "system", "popen", "Popen", "spawn", "run", "check_output", "call", "execv", "fork"}
BANNED_IMPORTS = {"subprocess", "os", "sys", "importlib", "ctypes", "socket", "urllib", "http", "pickle", "marshal", "shutil", "pathlib", "io", "tempfile",
                  "builtins", "runpy", "code", "codeop", "imp", "multiprocessing", "threading", "asyncio", "yaml", "requests"}
BANNED_SUBSTR = ("solver_a", "oracle", "engine", "sqlmodel", "heads", "generator", "builders", "items", "gates", "g9", "roundtrip")


def solver_files():
    return sorted(f for f in os.listdir(PKG) if f.endswith(".py") and f not in TOOLS)


def test_package_files_listed():
    assert {"hook.py", "plan.py", "k8s.py", "ci.py", "sqlrules.py", "minisql.py", "miniyaml.py", "effects.py", "textview.py", "tables.py"} <= set(solver_files())


@pytest.mark.parametrize("fname", solver_files())
def test_g1_lint(fname):
    tree = ast.parse(open(os.path.join(PKG, fname)).read())
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                root = a.name.split(".")[0]
                assert root in sys.stdlib_module_names, (fname, a.name)
                assert root not in BANNED_IMPORTS, (fname, a.name)
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                assert not any(b in (node.module or "") for b in BANNED_SUBSTR), (fname, node.module)
                for a in node.names:
                    assert not any(b == a.name for b in BANNED_SUBSTR), (fname, a.name)
            else:
                root = (node.module or "").split(".")[0]
                assert root in sys.stdlib_module_names and root not in BANNED_IMPORTS, (fname, node.module)
        elif isinstance(node, ast.Call):
            f = node.func
            name = f.id if isinstance(f, ast.Name) else (f.attr if isinstance(f, ast.Attribute) else None)
            assert name not in BANNED_CALLS, (fname, name)


def test_generator_side_is_imported_only_by_the_harness():
    assert "from T67 import generator" in open(os.path.join(PKG, "agree.py")).read()
    for f in solver_files():
        tree = ast.parse(open(os.path.join(PKG, f)).read())
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and not node.level:
                assert (node.module or "").split(".")[0] != "T67", f
            if isinstance(node, ast.Import):
                assert all(a.name.split(".")[0] != "T67" for a in node.names), f


def test_no_run_time_file_reads_in_the_solver_modules():
    for f in solver_files():
        assert "open(" not in open(os.path.join(PKG, f)).read(), f


ALLOWED_TOP = {"row_id", "head", "sub_block", "rendered", "options", "witness_inputs"}
ALLOWED_RENDERED = {"context", "question", "options_text", "text"}


class Spy(dict):
    def __init__(self, data, log):
        super().__init__(data)
        self.log = log

    def __getitem__(self, k):
        self.log.append(k)
        return dict.__getitem__(self, k)

    def get(self, k, default=None):
        self.log.append(k)
        return dict.get(self, k, default)

    def items(self):
        self.log.append("<items>")
        return dict.items(self)

    def keys(self):
        self.log.append("<keys>")
        return dict.keys(self)

    def values(self):
        self.log.append("<values>")
        return dict.values(self)

    def __iter__(self):
        self.log.append("<iter>")
        return dict.__iter__(self)


class Boom(object):
    def __getattribute__(self, name):
        raise AssertionError("B touched a non-b-view field")


def make_spy_view():
    bv = F.plan_row("ctx-shared", [F.plan_item("database_instance", "dbx", ["delete"], before={"snapshot": "none"}, after=None)])
    top, rend = [], []
    spy = Spy(bv, top)
    spy["rendered"] = Spy(bv["rendered"], rend)
    del top[:]
    return spy, top, rend


def test_b_reads_only_b_view_fields():
    spy, top, rend = make_spy_view()
    res = hook.solver_b(spy)
    assert res["status"] == "ok" and res["label"] == "BLOCK"
    assert set(top) <= ALLOWED_TOP and not [k for k in top if k.startswith("<")], top
    assert set(rend) <= ALLOWED_RENDERED and not [k for k in rend if k.startswith("<")], rend


def test_extra_fields_are_never_touched_and_do_not_change_the_answer():
    bv = F.plan_row("ctx-shared", [F.plan_item("database_instance", "dbx", ["delete"], before={"snapshot": "none"}, after=None)])
    base = hook.solver_b(bv)
    poisoned = dict(bv)
    for k in ("gold", "label", "spec", "meta", "manifest", "slots", "names", "decision_spans", "gold_letter", "group_id", "family", "question_form"):
        poisoned[k] = Boom()
    assert hook.solver_b(poisoned) == base


def test_real_b_view_of_a_generated_row_has_the_documented_keys():
    from T67 import schema
    assert set(schema.B_VIEW_FIELDS) == ALLOWED_TOP

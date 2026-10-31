"""G1 lint (solver B is stdlib-only, never executes or reads anything) and the view-isolation check (B touches only the b-view fields)."""
import ast
import os
import sys

import pytest

from T65.solver_b import hook
from views import HEADIMPORTS, vuln_view

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULES = sorted(f for f in os.listdir(PKG) if f.endswith(".py"))
HARNESS = {"agree.py"}                                   # the only module allowed to import the generator side (T65 / schema)
BANNED_CALLS = {"exec", "eval", "compile", "__import__", "open", "input", "breakpoint"}
BANNED_ATTR_CALLS = {("os", "system"), ("os", "popen"), ("os", "execv"), ("os", "spawnl")}
BANNED_IMPORTS = {"subprocess", "ctypes", "socket", "urllib", "http", "multiprocessing", "importlib", "runpy", "pty", "shutil", "tempfile"}
BANNED_NAMES = ("solver_a", "oracle", "pyeval", "pyshim", "sandbox_iface", "specs", "templates", "generator", "roundtrip", "gold", "LP_COMMON")
B_VIEW_KEYS = {"row_id", "head", "sub_block", "rendered", "options", "witness_inputs", "context", "question", "options_text", "text", "letter", "class_group"}


def tree_of(name):
    with open(os.path.join(PKG, name)) as fh:               # test code may read files; the solver modules may not
        return ast.parse(fh.read())


@pytest.mark.parametrize("name", MODULES)
def test_g1_lint(name):
    t = tree_of(name)
    std = set(sys.stdlib_module_names)
    for n in ast.walk(t):
        if isinstance(n, ast.Import):
            for a in n.names:
                top = a.name.split(".")[0]
                assert top in std or (name in HARNESS and top == "T65"), (name, a.name)
                assert top not in BANNED_IMPORTS, (name, a.name)
                assert not any(b in a.name for b in BANNED_NAMES) or name in HARNESS, (name, a.name)
        elif isinstance(n, ast.ImportFrom):
            if n.level:
                assert not any(b in (n.module or "") for b in BANNED_NAMES), (name, n.module)
                continue
            top = (n.module or "").split(".")[0]
            assert top in std or (name in HARNESS and top == "T65"), (name, n.module)
            assert top not in BANNED_IMPORTS, (name, n.module)
            assert name in HARNESS or not any(b in (n.module or "") for b in BANNED_NAMES), (name, n.module)
        elif isinstance(n, ast.Call):
            f = n.func
            if isinstance(f, ast.Name):
                assert f.id not in BANNED_CALLS, (name, f.id)
            elif isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name):
                assert (f.value.id, f.attr) not in BANNED_ATTR_CALLS, (name, f.value.id, f.attr)
                assert f.value.id != "subprocess", name


@pytest.mark.parametrize("name", [m for m in MODULES if m not in HARNESS])
def test_solver_modules_import_only_stdlib_and_own_package(name):
    t = tree_of(name)
    for n in ast.walk(t):
        if isinstance(n, ast.ImportFrom) and not n.level:
            assert n.module.split(".")[0] in set(sys.stdlib_module_names), (name, n.module)
        if isinstance(n, ast.Import):
            for a in n.names:
                assert a.name.split(".")[0] in set(sys.stdlib_module_names), (name, a.name)


def test_solver_never_reads_fields_outside_the_b_view():
    for name in MODULES:
        if name in HARNESS:
            continue
        for n in ast.walk(tree_of(name)):
            key = None
            if isinstance(n, ast.Subscript) and isinstance(n.slice, ast.Constant) and isinstance(n.slice.value, str):
                key = n.slice.value
            elif isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "get" and n.args and isinstance(n.args[0], ast.Constant):
                key = n.args[0].value
            if key is not None and isinstance(key, str) and name in ("solver.py", "hook.py", "parse.py"):
                assert key in B_VIEW_KEYS, (name, key)


class Guarded(dict):
    """A b-view that raises when anything outside the b-view fields is touched."""
    ALLOWED = {"row_id", "head", "sub_block", "rendered", "options", "witness_inputs"}

    def __getitem__(self, k):
        assert k in self.ALLOWED, "solver B read a field outside the b-view: %s" % k
        return dict.__getitem__(self, k)

    def get(self, k, d=None):
        assert k in self.ALLOWED, "solver B read a field outside the b-view: %s" % k
        return dict.get(self, k, d)


def test_view_isolation_runtime():
    from test_rules import build
    v = Guarded(vuln_view(HEADIMPORTS + "\n\n" + build("CWEC-22", "none"), "CWEC-22"))
    v.update({"gold": "NO", "spec": {"x": 1}, "label": "NO", "meta": {}, "manifest": {}, "slots": {}, "names": {}, "witness": {}})
    dict.__setitem__(v, "gold", "NO")
    res = hook.solver_b(v)
    assert res["status"] == "ok" and res["label"] == "YES"          # the poisoned gold is ignored and never touched


def test_label_does_not_depend_on_row_id_or_text_outside_the_code():
    from test_rules import build
    a = vuln_view(HEADIMPORTS + "\n\n" + build("CWEC-22", "none"), "CWEC-22")
    b = dict(a, row_id="b-0000000000000000-a-c-NO")
    assert hook.solver_b(a)["label"] == hook.solver_b(b)["label"] == "YES"
    c = dict(a, rendered=dict(a["rendered"], question="Is fn_y sound and safe, with no flaw?"))
    assert hook.solver_b(c)["label"] == "YES"                        # B reads the definitions card, not the question wording

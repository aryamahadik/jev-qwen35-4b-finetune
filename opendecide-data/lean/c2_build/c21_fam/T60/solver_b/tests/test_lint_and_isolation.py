"""G1 lint of the solver package + view isolation (solver B touches only the b-view fields)."""
import ast
import glob
import os
import re
import sys

import fixtures as fx
import hook

SB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOLVER_FILES = sorted(glob.glob(os.path.join(SB, "t60b_*.py")) + [os.path.join(SB, "hook.py"), os.path.join(SB, "__init__.py")])
OWN = {"hook", "t60b_text", "t60b_h1", "t60b_h2", "t60b_h3", "solver_b"}
BANNED_CALLS = {"exec", "eval", "compile", "__import__", "open", "system", "popen", "Popen", "check_output"}
BANNED_NAME = re.compile(r"solver_a|oracle|t60_rule|t60_model|t60_g9|t60_build|t60_gates|t60_generator|t60_render|t60_levers|t60_checked", re.I)
STDLIB = set(getattr(sys, "stdlib_module_names", ())) or {"re", "json", "itertools", "collections", "os", "sys"}


def _modules(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                yield a.name, 0
        elif isinstance(node, ast.ImportFrom):
            yield (node.module or ""), node.level


def test_solver_files_exist():
    assert len(SOLVER_FILES) >= 6


def test_g1_lint_imports_only_stdlib_or_own_package():
    for path in SOLVER_FILES:
        tree = ast.parse(open(path).read(), path)
        for mod, level in _modules(tree):
            top = mod.split(".")[0]
            if level:                                           # relative import inside the package
                assert (top in OWN) or mod == "", (path, mod)
                continue
            assert top in STDLIB or top in OWN, (path, mod)
            assert not BANNED_NAME.search(mod), (path, mod)
            assert top not in ("subprocess", "os", "importlib", "ctypes", "socket", "urllib", "http", "requests"), (path, mod)


def test_g1_lint_no_exec_eval_compile_import_open_system_subprocess():
    for path in SOLVER_FILES:
        src = open(path).read()
        tree = ast.parse(src, path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                fn = node.func
                name = fn.id if isinstance(fn, ast.Name) else (fn.attr if isinstance(fn, ast.Attribute) else "")
                assert name not in BANNED_CALLS, (path, name)
        for needle in ("exec(", "eval(", "compile(", "__import__", "open(", "subprocess", "os.system", "importlib"):
            assert needle not in src, (path, needle)
        # no reference to a solver-A / oracle / rule / model module by name (comments included)
        for m in BANNED_NAME.finditer(src):
            assert False, (path, m.group(0))


def test_g1_lint_names_no_solver_a_or_oracle_module_anywhere_in_the_package_imports():
    # the harness is the only file allowed to import the generator side, and even it must not import solver A / oracle / rule / model / g9
    harness = ast.parse(open(os.path.join(SB, "agree.py")).read())
    for mod, _lvl in _modules(harness):
        assert not re.search(r"solver_a|oracle|t60_rule|t60_model|t60_g9", mod, re.I), mod


class Strict(dict):
    """A dict that records every key read and refuses keys outside the b-view contract."""

    def __init__(self, data, allowed, log, where):
        dict.__init__(self, data)
        self._allowed, self._log, self._where = allowed, log, where

    def _chk(self, k):
        self._log.add((self._where, k))
        if k not in self._allowed:
            raise AssertionError("solver B touched %s.%s" % (self._where, k))

    def __getitem__(self, k):
        self._chk(k)
        return dict.__getitem__(self, k)

    def get(self, k, default=None):
        self._chk(k)
        return dict.get(self, k, default)

    def __contains__(self, k):
        self._chk(k)
        return dict.__contains__(self, k)


def _strict_view(v, log):
    out = Strict({k: v[k] for k in ("family", "sub_block")}, {"family", "sub_block", "options", "rendered"}, log, "view")
    out["options"] = [Strict(o, {"letter", "label", "text"}, log, "option") for o in v["options"]]
    out["rendered"] = Strict(v["rendered"], {"context", "question", "options_text", "text"}, log, "rendered")
    return out


def test_view_isolation_only_b_view_fields_are_read():
    views = [fx.h1_view(3, 100, 2, 400, 3, 0, 0, 100), fx.h3_view(5, 3, [("rename the item a-1", 9, "cannot be undone")] * 3, order=[], flow=[(1, 2)]),
             fx.h2_view(False, [fx.plan_line(1, "todo", "sync", "e", [fx.ref_l1("h")])], [fx.ev("get", "e", "h", 1)], 1, "R", "h", 1)]
    for v in views:
        log = set()
        sv = _strict_view(v, log)
        assert not hook.solver_b(sv).abstain
        assert hook.render_b(sv)[0] == "letter"
        assert {k for w, k in log if w == "view"} <= {"family", "sub_block", "options", "rendered"}
        assert ("option", "label") not in log                      # B never reads the label of an option


def test_nothing_else_is_needed_in_the_view():
    v = fx.h1_view(3, 100, 2, 400, 3, 0, 0, 100)
    slim = {"options": [{"letter": o["letter"], "text": o["text"]} for o in v["options"]],
            "rendered": {"context": v["rendered"]["context"], "question": v["rendered"]["question"], "options_text": v["rendered"]["options_text"]}}
    assert hook.solver_b(slim).label == "DELEGATE" and hook.render_b(slim) == ("letter", "A")

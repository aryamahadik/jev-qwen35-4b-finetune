"""G1 lint of the solver B package, and one small in-memory harness run."""
import ast
import os
import sys

import pytest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FORBIDDEN_CALLS = {"exec", "eval", "compile", "__import__", "open"}
FORBIDDEN_ATTR_CALLS = {("os", "system"), ("os", "popen"), ("os", "execv"), ("os", "spawnv")}
FORBIDDEN_MODULES = {"subprocess", "socket", "urllib", "http", "importlib", "ctypes", "pickle", "marshal", "shutil", "tempfile", "multiprocessing", "threading",
                     "asyncio", "runpy", "code", "codeop", "pty", "os", "pathlib", "io", "glob", "ssl", "ftplib", "smtplib", "requests", "builtins_x"}
BAD_NAMES = ("solver_a", "oracle", "gold_a", "prog", "merge3", "semver_spec", "merge_spec", "msg_spec", "tests_gen", "dryrun", "sandbox_iface", "pyeval", "pyshim")
HARNESS_FILES = {"agree.py"}


def solver_files():
    out = []
    for fn in sorted(os.listdir(HERE)):
        if fn.endswith(".py") and fn not in HARNESS_FILES and fn != "shas.py":
            out.append(os.path.join(HERE, fn))
    return out


def imports_of(tree):
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for a in n.names:
                yield 0, a.name
        elif isinstance(n, ast.ImportFrom):
            yield n.level, (n.module or "")


def test_package_lints_clean():
    files = solver_files()
    assert len(files) >= 8
    for path in files:
        tree = ast.parse(open(path, encoding="utf-8").read())
        for n in ast.walk(tree):
            if isinstance(n, ast.Call):
                if isinstance(n.func, ast.Name):
                    assert n.func.id not in FORBIDDEN_CALLS, (path, n.func.id)
                if isinstance(n.func, ast.Attribute) and isinstance(n.func.value, ast.Name):
                    assert (n.func.value.id, n.func.attr) not in FORBIDDEN_ATTR_CALLS, (path, n.func.attr)
                    assert n.func.value.id != "subprocess", path
            if isinstance(n, ast.Attribute):
                assert n.attr not in ("eval", "exec", "compile", "system", "popen"), (path, n.attr)
        for level, mod in imports_of(tree):
            top = mod.split(".")[0]
            if level > 0:
                assert all(b not in mod for b in BAD_NAMES), (path, mod)
                continue
            assert top not in FORBIDDEN_MODULES, (path, mod)
            assert top in sys.stdlib_module_names or mod.startswith("T66.solver_b") or mod == "T66.solver_b", (path, mod)
            assert all(b not in mod for b in BAD_NAMES), (path, mod)


def test_package_uses_only_relative_or_stdlib_imports():
    for path in solver_files():
        for level, mod in imports_of(ast.parse(open(path, encoding="utf-8").read())):
            assert level > 0 or mod.split(".")[0] in sys.stdlib_module_names, (path, mod)


def test_harness_imports_only_generator_side_it_needs():
    tree = ast.parse(open(os.path.join(HERE, "agree.py"), encoding="utf-8").read())
    for level, mod in imports_of(tree):
        top = mod.split(".")[0]
        assert top in sys.stdlib_module_names or mod in ("T66", "T66.solver_b", "T66.solver_b.hook") or mod.startswith("T66") and mod.split(".")[1] in ("generator", "schema", "solver_b"), mod
        assert all(b not in mod for b in BAD_NAMES), mod


def test_no_file_reads_at_run_time_in_solver_modules():
    for path in solver_files():
        src = open(path, encoding="utf-8").read()
        assert "open(" not in src.replace("def ", "").replace("is_open(", "") or True      # call-level check is done in the AST lint above
        tree = ast.parse(src)
        names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
        assert "open" not in names, path


def test_small_in_memory_harness_run():
    from T66.solver_b import agree
    report, detail = agree.run(120, [1], agree.os.path.join(agree.HERE, "testpool_msg.json"))
    s = report["summary"]
    assert s["ALL"]["rows"] == sum(s[h]["rows"] for h in ("MERGE", "SEMVER", "MSG")) > 100
    for h in ("MERGE", "SEMVER", "MSG"):
        assert s[h]["b_labelled"] + s[h]["b_abstained"] == s[h]["rows"]
        assert s[h]["agree"] + s[h]["disagree"] == s[h]["b_labelled"]
    assert s["MERGE"]["disagree"] == 0 and s["SEMVER"]["disagree"] == 0
    blob = repr(report["disagreement_classes"]) + repr(report["abstain_classes"])
    assert "T66-" not in blob                       # counts and generic causes only: no row ids

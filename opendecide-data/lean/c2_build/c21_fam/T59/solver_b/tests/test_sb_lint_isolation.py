"""G1 lint of the solver-B package, view isolation, abstain behaviour, hook shapes and one small in-memory agreement run."""
import ast
import json
import os
import sys

import pytest

import sb_fixtures as F
from solver_b import hook

PKG = os.path.join(F.FAM_T59, "solver_b")
SOLVER_MODULES = ("__init__.py", "parse.py", "rules.py", "hook.py")
OWN = {"parse", "rules", "hook", "solver_b"}
DENY_STDLIB = {"os", "sys", "subprocess", "socket", "urllib", "http", "importlib", "ctypes", "shutil", "pathlib", "io", "builtins", "pickle",
               "marshal", "runpy", "code", "codeop", "imp", "multiprocessing", "threading", "asyncio", "tempfile", "ftplib", "smtplib",
               "requests", "glob", "fileinput", "signal", "pty", "platform"}
BAD_NAMES = ("solver_a", "oracle", "t59_scene", "t59_build", "t59_g9", "t59_repo", "t59_generator", "t59_render", "t59_checked")
BAD_CALLS = {"exec", "eval", "compile", "__import__", "open", "input", "breakpoint"}


def _tree(name):
    with open(os.path.join(PKG, name)) as fh:
        return ast.parse(fh.read())


@pytest.mark.parametrize("name", SOLVER_MODULES)
def test_g1_lint_solver_modules(name):
    tree = _tree(name)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                top = a.name.split(".")[0]
                assert top in sys.stdlib_module_names or top in OWN, a.name
                assert top not in DENY_STDLIB, a.name
                assert not any(b in a.name for b in BAD_NAMES), a.name
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            top = mod.split(".")[0]
            assert node.level > 0 or top in sys.stdlib_module_names or top in OWN, mod
            assert top not in DENY_STDLIB, mod
            assert not any(b in mod for b in BAD_NAMES), mod
            assert not any(b in (a.name or "") for a in node.names for b in BAD_NAMES)
        elif isinstance(node, ast.Call):
            fn = node.func
            if isinstance(fn, ast.Name):
                assert fn.id not in BAD_CALLS, fn.id
            elif isinstance(fn, ast.Attribute):
                assert fn.attr not in ("system", "popen", "Popen", "check_output", "check_call", "exec_module", "load_module"), fn.attr
                assert not (isinstance(fn.value, ast.Name) and fn.value.id in ("os", "subprocess", "sys", "importlib"))


def test_agree_harness_does_not_import_solver_a_or_oracle_by_name_and_solver_does_not_import_it():
    tree = _tree("agree.py")
    for node in ast.walk(tree):
        names = []
        if isinstance(node, ast.Import):
            names = [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            names = [(node.module or "")] + [a.name for a in node.names]
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "import_module":
            if node.args and isinstance(node.args[0], ast.Constant):
                names = [node.args[0].value]
        for n in names:
            assert "solver_a" not in n and "oracle" not in n and "t59_scene" not in n, n
    for m in SOLVER_MODULES:
        src = open(os.path.join(PKG, m)).read()
        assert "agree" not in " ".join(l for l in src.splitlines() if l.startswith(("import ", "from "))), m


def test_no_row_files_or_bytecode_in_package():
    for root, _dirs, files in os.walk(PKG):
        for f in files:
            assert not f.endswith((".pyc", ".jsonl", ".pkl")), f


# ----------------------------------------------------------------------------------------------------------------------
# view isolation: B reads only the b-view fields; the given option `label` is never used
# ----------------------------------------------------------------------------------------------------------------------
class SpyDict(dict):
    def __init__(self, data, log, path, allowed):
        dict.__init__(self)
        self._data, self._log, self._path, self._allowed = data, log, path, allowed

    def _wrap(self, k, v):
        p = self._path + "." + str(k)
        if isinstance(v, dict):
            return SpyDict(v, self._log, p, self._allowed)
        if isinstance(v, list):
            return [SpyDict(x, self._log, p + "[]", self._allowed) if isinstance(x, dict) else x for x in v]
        return v

    def __getitem__(self, k):
        self._log.append(self._path + "." + str(k))
        return self._wrap(k, self._data[k])

    def get(self, k, default=None):
        self._log.append(self._path + "." + str(k))
        return self._wrap(k, self._data[k]) if k in self._data else default

    def __contains__(self, k):
        return k in self._data

    def keys(self):
        self._log.append(self._path + ".<keys>")
        return self._data.keys()

    def __iter__(self):
        self._log.append(self._path + ".<iter>")
        return iter(self._data)


def _sample_view(order=("ASK", "PROCEED")):
    noun = "fupalu"
    ts = [F.op_tool("rename", noun, [("name", "str", False, None)]), F.read_tool("list", noun)] + F.filler()
    return F.build(F.card("OFF"), ts, ["Please rename the fupalu fup-457.", "It holds 7 refodins.", "Options for the name: a, b."], [],
                   'Planned next step: rename_fupalu(fupalu_id="fup-457", name="a")', order=order)


def test_view_isolation_fields_touched():
    log = []
    v = _sample_view()
    spy = SpyDict(v, log, "view", None)
    hook.solver_b(spy)
    hook.render_b(spy)
    allowed = {"view.rendered", "view.rendered.context", "view.rendered.options_text", "view.rendered.text", "view.options"}
    touched = set(x for x in log)
    assert touched <= allowed | {"view.sub_block", "view.family"} | {"view.options[].letter", "view.options[].text"}, touched - allowed
    assert not any(t.endswith(".label") for t in touched), "the given option label must never be read"
    assert not any("scene" in t or "gold" in t or "case" in t or "trace" in t for t in touched)


def test_option_label_field_is_ignored_and_extra_keys_do_not_matter():
    v = _sample_view()
    base = hook.solver_b(v)
    w = json.loads(json.dumps(v))
    for o in w["options"]:
        o["label"] = "PROCEED" if o["label"] == "ASK" else "ASK"        # lie about the labels
    w["gold"] = "PROCEED"
    w["scene"] = {"x": 1}
    r = hook.solver_b(w)
    assert (r.label, r.letter) == (base.label, base.letter) and r.label == "ASK"
    assert hook.render_b(w) == ("letter", base.letter)
    # swapped option order moves the letter, not the label
    r2 = hook.solver_b(_sample_view(("PROCEED", "ASK")))
    assert r2.label == "ASK" and r2.letter == "B" and base.letter == "A"


# ----------------------------------------------------------------------------------------------------------------------
# abstain, never guess
# ----------------------------------------------------------------------------------------------------------------------
def _mut(v, fn):
    w = json.loads(json.dumps(v))
    ctx = fn(w["rendered"]["context"])
    w["rendered"]["context"] = ctx
    w["rendered"]["text"] = ctx + "\n\n" + w["rendered"]["question"] + "\n" + w["rendered"]["options_text"]
    return w


def test_abstains_on_unparsable_input():
    v = _sample_view()
    cases = {
        "unknown user line": lambda c: c.replace("User: Options for the name: a, b.", "User: Whatever you prefer for the name, honestly."),
        "unknown tool line": lambda c: c.replace("Tools:", "Tools:\n- this is not a tool line"),
        "no planned step": lambda c: "\n".join(l for l in c.split("\n") if not l.startswith("Planned next step")),
        "card without mode": lambda c: c.replace("Ask when a required value has no source or the request has more than one reading.", "Be nice."),
        "no conversation": lambda c: c.split("Conversation:")[0],
        "garbage": lambda c: "hello world",
    }
    for name, fn in cases.items():
        r = hook.solver_b(_mut(v, fn))
        assert r.abstain and r.label is None and r.letter is None, name
        assert hook.render_b(_mut(v, fn))[0] == "abstain", name
    w = json.loads(json.dumps(v))
    w["rendered"]["options_text"] = "A) Do this\nB) Do that"
    assert hook.solver_b(w).abstain


def test_hook_shapes():
    r = hook.solver_b(_sample_view())
    assert r.label in ("ASK", "PROCEED") and r.letter in ("A", "B") and r.abstain is False and isinstance(r.reason, str)
    kind, val = hook.render_b(_sample_view())
    assert kind == "letter" and val == r.letter
    assert not getattr(hook.solver_b, "needs_full_record", False) and not getattr(hook.render_b, "needs_full_record", False)


def test_checker_detects_wrong_expectation():
    from test_sb_truth_table import check
    with pytest.raises(AssertionError):
        check(_sample_view(), "PROCEED")


# ----------------------------------------------------------------------------------------------------------------------
# one small in-memory harness run (agree.py is the only module that touches the generator side)
# ----------------------------------------------------------------------------------------------------------------------
def test_small_in_memory_agreement_run(tmp_path):
    sys.path.insert(0, PKG)
    import agree
    out = str(tmp_path / "rep.json")
    rc = agree.main(["--rows", "160", "--seeds", "unit1", "--levers", "--out", out])
    with open(out) as fh:
        rep = json.load(fh)
    assert rep["total"]["rows"] >= 150
    assert rep["agreement_pct_all"] >= 99.0 and rc == 0
    assert rep["total"]["abstain"] == 0
    assert "row_id" not in json.dumps(rep) and set(rep["by_sub_block"]) == {"T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8"}


def test_loadable_under_a_unique_package_name_and_tolerates_trailing_space():
    """Several families ship a `solver_b` folder: the orchestrator may load this one under another name."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("t59_solver_b_unique", os.path.join(PKG, "__init__.py"), submodule_search_locations=[PKG])
    mod = importlib.util.module_from_spec(spec)
    sys.modules["t59_solver_b_unique"] = mod
    spec.loader.exec_module(mod)
    h = importlib.import_module("t59_solver_b_unique.hook")
    v = _sample_view()
    assert h.solver_b(v).label == "ASK"
    w = _mut(v, lambda c: "\n".join(l + "  " for l in c.split("\n")))
    assert h.solver_b(w).label == "ASK" and hook.solver_b(w).label == "ASK"

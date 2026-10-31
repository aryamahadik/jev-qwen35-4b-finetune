"""G1 lint, view isolation, hook shape, a small in-memory harness run and the pipeline wiring."""
import ast
import collections
import os
import sys

import pytest

from T63.solver_b import hook

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANNED_CALLS = {"exec", "eval", "compile", "__import__", "open", "system", "popen", "Popen", "check_output", "check_call", "spawn", "execv", "fork"}
BANNED_IMPORT_ROOTS = {"subprocess", "os", "pickle", "marshal", "ctypes", "socket", "urllib", "http", "importlib", "runpy", "shutil", "builtins"}
PACKAGE_FILES = ["__init__.py", "common.py", "rel.py", "near_b.py", "exists_b.py", "lic_b.py", "hook.py"]


def _tree(fn):
    with open(os.path.join(PKG, fn)) as f:
        return ast.parse(f.read(), fn)


def test_package_file_list_is_complete():
    on_disk = sorted(f for f in os.listdir(PKG) if f.endswith(".py") and f != "agree.py")
    assert on_disk == sorted(PACKAGE_FILES)


@pytest.mark.parametrize("fn", PACKAGE_FILES)
def test_g1_lint_stdlib_and_own_package_only_no_dynamic_code(fn):
    stdlib = set(sys.stdlib_module_names)
    for node in ast.walk(_tree(fn)):
        if isinstance(node, ast.Import):
            for a in node.names:
                root = a.name.split(".")[0]
                assert root in stdlib and root not in BANNED_IMPORT_ROOTS, (fn, a.name)
        elif isinstance(node, ast.ImportFrom):
            if node.level:                                                       # relative: own package only
                assert node.level == 1, (fn, node.level)
            else:
                root = (node.module or "").split(".")[0]
                assert root in stdlib and root not in BANNED_IMPORT_ROOTS, (fn, node.module)
        elif isinstance(node, ast.Call):
            f = node.func
            name = f.id if isinstance(f, ast.Name) else (f.attr if isinstance(f, ast.Attribute) else None)
            assert name not in BANNED_CALLS, (fn, name, node.lineno)


@pytest.mark.parametrize("fn", PACKAGE_FILES)
def test_no_solver_a_or_gold_engine_names_in_the_package(fn):
    with open(os.path.join(PKG, fn)) as f:
        src = f.read().lower()
    for bad in ("solver_a", "from t63", "import t63", "lp_common", "near.py", "exists.py", "lic.py", "gold_a"):
        assert bad not in src.replace("exists_b.py", "").replace("lic_b.py", ""), (fn, bad)


class StrictView(dict):
    """A b-view that records every key read and refuses any key outside the contract."""
    ALLOWED = {"row_id", "head", "sub_block", "rendered", "options", "witness_inputs"}

    def __init__(self, d):
        dict.__init__(self, d)
        self.seen = set()

    def __getitem__(self, k):
        if k not in self.ALLOWED:
            raise AssertionError("B touched a field outside the b-view: %r" % (k,))
        self.seen.add(k)
        return dict.__getitem__(self, k)

    def get(self, k, default=None):
        if k not in self.ALLOWED:
            raise AssertionError("B touched a field outside the b-view: %r" % (k,))
        self.seen.add(k)
        return dict.get(self, k, default)


def test_view_isolation_on_generated_rows():
    from T63 import schema
    from T63.solver_b import agree
    ex, export_data, tb = agree.load_fixture_sources()
    rows, _s = agree.build_rows(200, 3, "test", ex, tb)
    table = agree.table_to_plain(tb, rows)
    kw = dict(exports=export_data, export_sha=ex.sha, table=table, table_sha=agree._table_sha(rows), fixture=True, allow_fixture=True)   # build-stage
    seen = set()
    for rec in rows:
        v = schema.b_view(rec)
        assert set(v) == set(StrictView.ALLOWED)
        plain = hook.evaluate(v, **kw)
        strict = StrictView(v)
        again = hook.evaluate(strict, **kw)
        seen |= strict.seen
        assert again == plain
        # the label and every generator-side field are absent from the view: B's answer is identical when the record's other fields are poisoned
        poisoned = dict(rec, gold="POISON", label="POISON", gold_letter="Z", spec=None, meta=None, manifest=None, slots=None, names=None)
        assert hook.evaluate(schema.b_view(poisoned), **kw) == plain
    assert seen <= StrictView.ALLOWED and {"rendered", "options", "head", "sub_block", "witness_inputs"} <= seen


def test_view_never_carries_a_label():
    from T63 import schema
    assert set(schema.B_VIEW_FIELDS) == set(StrictView.ALLOWED)


def test_hook_result_shape_and_abstain_never_a_label():
    r = hook.solver_b({"head": "NEAR", "sub_block": "NEAR", "rendered": {"context": "x", "question": "q", "options_text": "A) YES\nB) NO", "text": ""},
                      "options": [{"letter": "A", "text": "YES"}, {"letter": "B", "text": "NO"}], "witness_inputs": {}, "row_id": "b-x"})
    assert r["status"] == "abstain" and r["label"] is None
    e = hook.solver_b({"head": "NEAR"})                                           # malformed view: error, not a guess
    assert e["status"] in ("error", "abstain") and e["label"] is None


def test_configure_sets_module_sources_and_clears():
    hook.configure(exports={"python": {"m": ["a"]}}, export_sha="s")
    assert hook._STATE["exports"] is not None
    hook.configure()
    assert hook._STATE["exports"] is None and hook._STATE["table"] is None


def test_small_harness_run_agrees(tmp_path):
    from T63.solver_b import agree
    out = tmp_path / "r.json"
    assert agree.main(["--rows", "150", "--seeds", "1,2", "--out", str(out), "--pool", "test"]) == 0
    import json
    rep = json.loads(out.read_text())
    assert rep["totals"]["labelled"] >= 300 and rep["totals"]["disagree"] == 0 and rep["totals"]["error"] == 0
    assert rep["totals"]["letter_mismatch"] == 0 and rep["totals"]["abstain"] == 0
    assert {"NEAR", "LIC", "EXISTS"} <= set(rep["by_head"]) and {"EX-A1", "EX-A2", "EX-B1", "EX-B2"} <= set(rep["by_sub_block"])


def test_without_sources_b2_and_lic_abstain_and_nothing_is_guessed(tmp_path):
    from T63.solver_b import agree
    import json
    out = tmp_path / "r.json"
    agree.main(["--rows", "100", "--seeds", "4", "--out", str(out), "--pool", "test", "--no-b2-sources"])
    rep = json.loads(out.read_text())
    assert rep["by_sub_block"]["EX-B2"]["labelled"] == 0 and rep["by_sub_block"]["LIC"]["labelled"] == 0
    assert rep["by_sub_block"]["EX-B2"]["abstain"] == rep["by_sub_block"]["EX-B2"]["rows"]
    assert rep["totals"]["disagree"] == 0


def test_checked_adapter_accepts_the_hook_and_the_pipeline_keeps_the_rows():
    from LP_COMMON import pipeline as pl
    from T63 import checked
    from T63.solver_b import agree
    ex, export_data, tb = agree.load_fixture_sources()
    rows0, _s = agree.build_rows(120, 9, "test", ex, tb)
    table = agree.table_to_plain(tb, rows0)
    sb = hook.make_solver_b(exports=export_data, export_sha=ex.sha, table=table, table_sha=agree._table_sha(rows0), fixture=True, allow_fixture=True)
    ad = checked.adapter(ex, tb, solver_b=sb)
    assert ad.solver_b is sb
    kept, summary, log, _rep = checked.run(120, 9, pl.TestDoubleHook(), standin=True, exports=ex, table=tb, solver_b=sb)
    dropped = collections.Counter({k: v for k, v in summary["dropped"].items()})
    assert not [k for k in dropped if "B_" in str(k) or "A_B" in str(k)], dropped
    assert len(kept) >= 100
    assert "solver_b_absent" not in summary["notes"]
    # module-level plug point with configure(), the shape the task names
    hook.configure(exports=export_data, export_sha=ex.sha, table=table, table_sha=agree._table_sha(rows0), fixture=True, allow_fixture=True)
    try:
        kept2, summary2, _l, _r = checked.run(120, 9, pl.TestDoubleHook(), standin=True, exports=ex, table=tb, solver_b=hook.solver_b)
        assert len(kept2) == len(kept)
    finally:
        hook.configure()


# ---- power check: the harness must notice a broken rule (an agreement figure of 100% is only worth something if it can drop) --------------
@pytest.mark.parametrize("target,attr,value,sub", [
    ("near_b", "ESTABLISHED_MIN_AGE", 3, "NEAR"),
    ("near_b", "AGE_RANK", {"under 30 days": 0, "under 1 year": 1, "1-4 years": 3, "over 4 years": 3}, "NEAR"),
    ("rel", "t5", lambda p, q: False, "NEAR"),
    ("rel", "t7", lambda p, q: False, "NEAR"),
    ("rel", "t4", lambda p, q: False, "NEAR"),
    # swap USE-1 and USE-5: on the REAL T63-LIC-TABLE a USE-1 / USE-2 swap changes (almost) no label in the cut, so it has no power; USE-1 / USE-5 does
    ("lic_b", "USE_ID", {"vendored source copy": "LC-USE-5", "static link": "LC-USE-2", "dynamic link": "LC-USE-3", "separate process": "LC-USE-4",
                         "dev-time tool only": "LC-USE-1"}, "LIC"),
])
def test_harness_detects_a_broken_rule(monkeypatch, tmp_path, target, attr, value, sub):
    import json
    from T63.solver_b import agree
    mod = {"near_b": __import__("T63.solver_b.near_b", fromlist=["x"]), "rel": __import__("T63.solver_b.rel", fromlist=["x"]),
           "lic_b": __import__("T63.solver_b.lic_b", fromlist=["x"])}[target]
    if attr == "t5":                                              # rel.TESTS holds references: patch the tuple entry as well as the name
        monkeypatch.setattr(mod, "TESTS", tuple((n, (value if n == "NM-T5" else f)) for n, f in mod.TESTS))
    elif attr == "t7":
        monkeypatch.setattr(mod, "TESTS", tuple((n, (value if n == "NM-T7" else f)) for n, f in mod.TESTS))
    elif attr == "t4":
        monkeypatch.setattr(mod, "TESTS", tuple((n, (value if n == "NM-T4" else f)) for n, f in mod.TESTS))
    else:
        monkeypatch.setattr(mod, attr, value)
    out = tmp_path / "r.json"
    agree.main(["--rows", "600", "--seeds", "2", "--out", str(out), "--pool", "test"])
    rep = json.loads(out.read_text())
    assert rep["by_sub_block"][sub]["disagree"] + rep["by_sub_block"][sub]["abstain"] > 0

"""Build-skeptic tests (Sun 18 Oct): NS-1 static twins differ, the twin-integrity gate, the B-view hides the member letter and the CWE head row's class."""
import pytest

from LP_COMMON import pipeline as pl
from T65 import checked, config as C, dryrun, gates, generator as G, schema, specs as SP


def _pair(cls, kind, seed):
    return SP.make_pair_specs(G.Ctx(seed=seed, standin=True), {"gid": "g%d" % seed, "seed": "s%d" % seed}, {"cls": cls, "pair_kind": kind, "transforms": [], "noise": False})


@pytest.mark.parametrize("cls", C.CLASSES)
@pytest.mark.parametrize("seed", [1, 2, 3])
def test_ns1_twins_differ_and_have_opposite_labels_for_every_class(cls, seed):
    y, n = _pair(cls, "ns:NS-1", seed)
    assert (y["label"], n["label"]) == ("YES", "NO")
    assert y["source_text"] != n["source_text"] and y["edit_lines"] >= 1


def test_every_pair_kind_of_every_class_has_distinct_twin_code():
    import itertools
    for cls in C.CLASSES:
        kinds = ["plain"] + ["decoy:" + d for d in C.DS_IDS] + ["ns:NS-1", "ns:NS-3"] + (["ns:NS-2"] if cls in C.DYNAMIC else []) + (["ns:NS-4"] if cls in ("CWEC-78", "CWEC-89") else [])
        for kind in kinds:
            y, n = _pair(cls, kind, 4)
            assert y["source_text"] != n["source_text"], (cls, kind)


def test_identical_twin_code_is_rejected_by_the_builder(monkeypatch):
    orig = SP.build_pair

    def same(cls, cell, pool, rng):
        yes, no = orig(cls, cell, pool, rng)
        no["neut"], no["source"] = yes["neut"], yes["source"]
        return yes, no

    monkeypatch.setattr(SP, "build_pair", same)
    with pytest.raises(SP.Reject):
        _pair("CWEC-22", "plain", 1)


def test_twin_integrity_gate_catches_identical_code_and_an_unpaired_row():
    rows, *_ = dryrun.dry_rows(80, seed=5)
    assert gates.g_twin_integrity(rows)["ok"]
    v = [r for r in rows if r["head"] == "VULN"]
    broken = [dict(r) for r in v]
    broken[1] = dict(broken[1], spec=dict(broken[1]["spec"], source_text=broken[0]["spec"]["source_text"]))
    assert not gates.g_twin_integrity(broken)["ok"]
    assert not gates.g_twin_integrity(v[1:])["ok"]


def test_b_view_has_an_opaque_id_and_no_class_on_the_cwe_head_row():
    rows, *_ = dryrun.dry_rows(80, seed=5)
    for r in rows:
        bv = schema.b_view(r)
        assert bv["row_id"] != r["row_id"] and not bv["row_id"].endswith(("-a", "-b", "-c"))
        if r["head"] == "CWE":
            assert bv["sub_block"] == "CWE" and "CWEC" not in str(bv)
    assert any(r["head"] == "CWE" for r in rows)


def test_row_suffix_letters_do_carry_the_label_so_the_view_must_not_show_them():
    """Documents WHY the id is opaque: in this family '-a' is always the YES member."""
    rows, *_ = dryrun.dry_rows(80, seed=5)
    for r in rows:
        if r["head"] == "VULN":
            assert (r["gold"] == "YES") == r["row_id"].endswith("-a")


def test_lint_gate_flags_clock_and_environment_reads():
    rows, *_ = dryrun.dry_rows(40, seed=5)
    assert gates.g_lint(rows)["ok"]
    bad = [dict(r, spec=dict(r["spec"], source_text=r["spec"]["source_text"] + "x = time.time()\n")) if r["head"] == "VULN" else r for r in rows]
    assert not gates.g_lint(bad)["ok"]


def test_cwec89_functions_are_self_contained_so_the_real_sqlite3_has_a_table():
    y, n = _pair("CWEC-89", "plain", 6)
    for s in (y, n):
        t = s["source_text"]
        assert 'CREATE TABLE users (id TEXT, name TEXT)' in t and "INSERT INTO users VALUES ('1', 'alice'), ('2', 'bob')" in t
        assert t.index("CREATE TABLE") < t.index("INSERT INTO") < t.index("SELECT")
    assert y["witness"]["effect"] and not n["witness"]["effect"]


def test_cwec22_job_ships_its_fixture_files_and_the_runner_changes_into_the_job_dir():
    from LP_COMMON import sandbox_iface as S

    seen = []

    class Spy(S.SimExecutor):
        def run(self, requests):
            seen.extend(requests)
            return super().run(requests)

    ctx = G.Ctx(seed=1, standin=True, executor=Spy())
    SP.make_pair_specs(ctx, {"gid": "g6", "seed": "s6"}, {"cls": "CWEC-22", "pair_kind": "plain", "transforms": [], "noise": False})
    assert seen
    for rq in seen:
        for path, content in C.FIXTURES["CWEC-22"].items():
            assert rq["files"][path] == content
        assert "os.chdir(os.path.dirname(os.path.abspath(__file__)))" in rq["files"]["od_run_calls.py"]
        assert not any(p.startswith("/") for p in rq["files"])           # nothing outside the job directory


def test_no_dynamic_class_other_than_22_needs_a_fixture_file():
    assert set(C.FIXTURES) == {"CWEC-22"}


def test_the_shipped_pool_passes_the_pool_guard_and_has_no_inverted_frames():
    import json
    pool = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "pools", "wording_pool.json")))
    assert G.pool_problems(pool) == []
    assert len(pool["forms"]["T65-Q-VULN"]) >= 50


@pytest.mark.parametrize("text", ["Does {fn} neutralise its controlled value before the sensitive operation?", "For {fn}, is the controlled value handled safely before it is used?",
                                  "Is the function {fn} sound, or does it show a flaw under the rule?", "Does the neutralising step in {fn} run before the operation on every path?",
                                  "For {fn}, decide whether a neutralising step covers the operation it reaches."])
def test_inverted_polarity_frames_are_refused(text):
    import json
    pool = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "pools", "wording_pool.json")))
    pool["forms"]["T65-Q-VULN"] = pool["forms"]["T65-Q-VULN"] + [{"id": "wx", "text": text}]
    assert any("denied pattern" in p for p in G.pool_problems(pool))


import os      # noqa: E402

"""Tests for zed_orch/md_final/finalize_md.py, the MD QC-record writer (Ruling A66 (a)). The data are COPIES of the MD block, the source parts
and the GB candidates in tmp_path; the live C2 tree is only read. Every new check has a fault-injection test that makes it fail.
Nothing sealed or ohs is named; the deny-list script is never run on the live tree (its output is fed in as text, and run_denylist is
tested on a fake script). Run from c2_build/:
  ../../.venv/bin/python -B -m pytest -q tests/test_finalize_md.py
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import shutil
import sys
from fractions import Fraction
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2B))
spec = importlib.util.spec_from_file_location("finalize_md_under_test", C2B / "zed_orch" / "md_final" / "finalize_md.py")
fin = importlib.util.module_from_spec(spec)
sys.modules["finalize_md_under_test"] = fin
spec.loader.exec_module(fin)
import c2io  # noqa: E402
import mix_c2  # noqa: E402
from negtwins import frozen as FZ  # noqa: E402

LIVE_MD, LIVE_PARTS = fin.MD, fin.PARTS
DENY_OK = "\n".join(f"md_{s} CLEAR" for s in ("fsa", "gbif", "geonames", "cordis_h2020", "gene_ontology", "musicbrainz", "openalex", "ror", "usgs", "worldbank")) \
    + "\nmd_cma OVERLAP c1:github\ngp_x CLEAR\n"


def shaf(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def tree(root: Path) -> dict:
    return {str(p.relative_to(root)): shaf(p) for p in sorted(root.rglob("*")) if p.is_file()}


def original_qc() -> Path:
    """The pre-finalize QC record: the live one, or (after a real --write) the earliest backup of it."""
    live = LIVE_MD / "qc" / "QC_REPORT.json"
    if json.loads(live.read_text()).get("finalize"):
        return sorted((LIVE_MD / "qc" / fin.BACKUP_DIR).glob("*/QC_REPORT.json"))[0]
    return live


@pytest.fixture()
def world(tmp_path):
    md, parts, gb = tmp_path / "c2_parts" / "MD", tmp_path / "c2_md_parts", tmp_path / "c2_parts" / "GB"
    (md / "qc").mkdir(parents=True)
    shutil.copytree(LIVE_MD / "out", md / "out")
    shutil.copy2(original_qc(), md / "qc" / "QC_REPORT.json")
    shutil.copy2(LIVE_MD / "qc" / "dropped_tasks.json", md / "qc" / "dropped_tasks.json")
    shutil.copytree(LIVE_PARTS, parts, ignore=shutil.ignore_patterns("chunks", "prompts", "manifest"))
    (gb / "out").mkdir(parents=True)
    shutil.copy2(LIVE_MD.parent / "GB" / "out" / "candidates_c2.jsonl", gb / "out" / "candidates_c2.jsonl")
    audit = tmp_path / "POOLED_AUDIT_REPORT.json"
    shutil.copy2(C2B / "negtwins" / "stage3" / "POOLED_AUDIT_REPORT.json", audit)
    sc = tmp_path / "SOURCES_CANDIDATES.json"
    shutil.copy2(C2B / "meta_src" / "SOURCES_CANDIDATES.json", sc)
    return fin.Paths(md=md, parts=parts, gb=gb, rtw=tmp_path / "c2_parts" / "RTW", audit=audit, sources_cand=sc)


@pytest.fixture(scope="module")
def mm():
    return fin.load_merge_md()


def verdict(P, **kw):
    return fin.verdict(P, denylist_out=kw.pop("denylist_out", DENY_OK), **kw)


def rewrite_jsonl(path, fn):
    rows = fin.jl(path)
    rows = fn(rows) or rows
    Path(path).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


def edit_json(path, fn):
    d = json.loads(Path(path).read_text())
    fn(d)
    Path(path).write_text(json.dumps(d, indent=1))


def has(problems, needle) -> bool:
    return any(needle in x for x in problems)


# ============================================================================================================ the happy path
def test_dry_run_passes_and_writes_nothing(world):
    before = tree(world.md.parent.parent)
    v, p = verdict(world)
    assert p == [] and v["would_pass"] is True
    assert (v["rows"], v["twins"]["twins"], v["relations"]) == (10491, 492, 492)
    assert v["twins"]["g_tw"] == {"n_pairs": 492, "violations": 0, "pass": True}
    assert v["admission_simulated"] == []
    assert all(x["status"] == "complete" and x["tasks_unchecked"] == 0 and x["tasks_read"] == x["tasks_in"] for x in v["noise_gate"]["per_source"].values())
    assert v["noise_gate"]["tasks_flagged_total"] == 9 and v["noise_gate"]["dropped_tasks_json_entries"] == 10   # 9 by the gate + 1 schema drop
    assert [d["block_source"] for d in v["deviations"]] == ["c2_md_gbif"]
    assert v["pooled_A60"]["by_kind"] == {"syntactic": 26, "implicit": 19, "antonym": 27}
    assert tree(world.md.parent.parent) == before                       # a verdict reads only


def test_main_dry_run_exit_codes(world, capsys):
    before = tree(world.md.parent.parent)
    assert fin.main([], P=world, denylist_out=DENY_OK) == 0
    assert tree(world.md.parent.parent) == before
    edit_json(world.qc, lambda d: d.update(problems=["x"]))
    assert fin.main([], P=world, denylist_out=DENY_OK) == 1


# ============================================================================================================ 1 bars
def test_bar_constants_are_pinned(mm, monkeypatch):
    assert fin.bars_problems(mm) == []
    for obj, name, val in ((mix_c2, "SOURCE_MAX", 0.2), (mix_c2, "DOMAIN_MAX", 0.25), (mix_c2, "META_MIN_ROWS", 7000), (mix_c2, "META_TASKS_PER_SOURCE", (30, 80)),
                           (mix_c2, "CARD_FREE_MIN", 0.2), (mix_c2, "META_TASK_ROWS_MAX", 300), (mix_c2, "META_DOMAINS_MIN", 6),
                           (mm, "CLEAR_CONF", 0.5), (mm, "NOISE_MIN_WRONG", 3), (fin.A60, "MIN_ANTONYM", Fraction(1, 5)), (fin.A60, "MAX_SYNTACTIC", Fraction(1, 2))):
        with monkeypatch.context() as m:
            m.setattr(obj, name, val)
            assert fin.bars_problems(mm), name
    with monkeypatch.context() as m:
        m.setitem(mix_c2.TWIN_CAP, "MD", 6000)
        assert fin.bars_problems(mm)
    with monkeypatch.context() as m:
        m.setitem(mix_c2.BLOCK_CAPS, "MD", 13000)
        assert fin.bars_problems(mm)


def test_verdict_fails_when_a_bar_moved(world, monkeypatch):
    monkeypatch.setattr(mix_c2, "SOURCE_MAX", 0.2)
    v, p = verdict(world)
    assert not v["would_pass"] and has(p, "bar changed in code")


# ============================================================================================================ io rules
def test_jsonl_splits_on_newline_only(tmp_path):
    f = tmp_path / "r.jsonl"
    row = {"id": "a", "text": "x y z\x85w\x0bq\x0cr\x1cs"}
    f.write_text(json.dumps(row, ensure_ascii=False) + "\n" + json.dumps({"id": "b"}) + "\n\n", encoding="utf-8")
    assert len(f.read_text(encoding="utf-8").splitlines()) > 3          # what the old reader did: cut the row apart
    assert fin.jl(f) == [row, {"id": "b"}]


def test_never_open_paths_are_refused():
    for bad in ("/x/ohs4_thing/a.json", "/x/Sealed_hashes/a.json", "/x/c_build/preread/a", "/x/bench/external_quarantine/a", "/x/longbench_v2/a",
                "/x/.claude/projects/a", "/x/OHS3/a"):
        with pytest.raises(PermissionError):
            fin.rd(bad)
    assert fin.refuse_path(LIVE_MD / "out" / "MANIFEST.json") is None


# ============================================================================================================ 2 files
def test_manifest_and_candidate_sha_binding(world):
    rewrite_jsonl(world.cand, lambda rows: rows + [copy.deepcopy(rows[0])])
    v, p = verdict(world)
    assert not v["would_pass"] and has(p, "manifest:") and has(p, "duplicate ids")


def test_relations_must_be_the_twin_links(world):
    rewrite_jsonl(world.rel, lambda rows: rows[:-1])
    v, p = verdict(world)
    assert has(p, "relations are not exactly the twin links") and has(p, "manifest:")


def test_hold_file_checked_against_its_recorded_sha_and_rows(world):
    rewrite_jsonl(world.hold, lambda rows: rows[:-1])
    v, p = verdict(world)
    assert has(p, "hold file c3_hold_a60.jsonl differs") and has(p, "hold files hold 838 rows")


def test_hold_rows_may_not_share_ids_with_the_candidates(world):
    ids = fin.jl(world.cand)[0]["id"]

    def f(rows):
        rows[0]["id"] = ids
    rewrite_jsonl(world.hold, f)
    edit_json(world.qc, lambda d: d["a60"]["hold"].update(rows_sha256=shaf(world.hold)))
    v, p = verdict(world)
    assert has(p, "share ids with the candidates")


def test_a60_and_qc_problems_make_it_fail(world):
    edit_json(world.qc, lambda d: d["a60"].update(block_rule_problems=["x"]))
    assert has(verdict(world)[1], "A60 record carries problems")


# ============================================================================================================ 4 noise gate
def keyed_rows(P, mm, name):
    """(source struct, {task: [(qid, row)]}) of the picked non-twin rows of one source part."""
    old = mm.PARTS
    mm.PARTS = P.parts
    try:
        srcs, _ = mm.load_sources({name})
    finally:
        mm.PARTS = old
    s = srcs[name]
    byid = {r["id"]: r for r in s["all_rows"]}
    out = {}
    for kf in sorted((P.parts / name / "noise_gate" / "key").glob("MD_*.json")):
        for qid, rid in json.loads(kf.read_text())["key"].items():
            r = byid.get(rid)
            if r is not None and not mm.self_twin(r):
                out.setdefault(r["meta"]["task_id"], []).append((qid, r))
    return s, out


def wrong_answer(r):
    if r["qtype"] == "noul":
        return "no" if r["gold"] == 1 else "yes"
    return next(o for o in r["options"] if o != r["gold"])


def override(P, name, pairs, conf=1.0):
    d = P.parts / name / "noise_gate" / "answers"
    (d / "zzz_override.json").write_text(json.dumps({qid: {"answer": wrong_answer(r), "confidence": conf} for qid, r in pairs}))


def test_gate_flags_a_surviving_task_the_record_missed(world, mm):
    s, keyed = keyed_rows(world, mm, "fsa")
    t, pairs = next((t, v) for t, v in sorted(keyed.items()) if len(v) >= 2)
    override(world, "fsa", pairs[:2])
    v, p = verdict(world)
    assert not v["would_pass"]
    assert has(p, "noise gate fsa: the QC record's tasks_dropped_by_gate 0 != 1")
    assert has(p, "flagged tasks are not in dropped_tasks.json") and has(p, "dropped tasks are in the candidates")


def test_gate_bar_is_two_wrong_reads_at_confidence_07(world, mm):
    s, keyed = keyed_rows(world, mm, "fsa")
    t, pairs = next((t, v) for t, v in sorted(keyed.items()) if len(v) >= 2)
    override(world, "fsa", pairs[:1])                                                   # one wrong read: not a drop
    assert verdict(world)[1] == []
    override(world, "fsa", pairs[:2], conf=0.69)                                        # two wrong reads below 0.7: not a drop
    assert verdict(world)[1] == []
    override(world, "fsa", pairs[:2], conf=0.7)                                         # two at 0.7: a drop
    assert has(verdict(world)[1], "flagged tasks are not in dropped_tasks.json")


def test_missing_answers_mean_a_partial_gate(world):
    ans = sorted((world.parts / "ror" / "noise_gate" / "answers").glob("*.json"))
    ans[0].unlink()
    v, p = verdict(world)
    assert not v["would_pass"] and has(p, "noise gate ror: status partial")


def test_all_answers_gone_is_pending(world):
    shutil.rmtree(world.parts / "usgs" / "noise_gate" / "answers")
    assert has(verdict(world)[1], "noise gate usgs: status pending")


def test_record_that_vouches_for_itself_is_caught(world):
    edit_json(world.qc, lambda d: d["gates_run"]["A42D_8_4_noise_gate"]["per_source"]["geonames"].update(tasks_read_by_gate=69))
    assert has(verdict(world)[1], "noise gate geonames: the QC record's tasks_read_by_gate 69 != 70")


def test_dropped_tasks_json_must_equal_the_flagged_set(world):
    def f(d):
        d.pop("gbif:extinct:0")
    edit_json(world.dropped, f)
    v, p = verdict(world)
    assert has(p, "noise gate gbif: dropped_tasks.json has 4 tasks, the answers flag 5")
    edit_json(world.dropped, lambda d: d.update({"gbif:extinct:0": {"source": "gbif", "wrong": 2, "read": 13}, "x:extra": {"source": "fsa", "wrong": 2, "read": 13}}))
    assert has(verdict(world)[1], "dropped_tasks.json holds 1 gate-dropped tasks the answers do not flag")
    edit_json(world.dropped, lambda d: d.pop("x:extra") and d["gbif:extinct:0"].update(wrong=3))
    assert has(verdict(world)[1], "wrong/read counts differ")


def test_a_dropped_task_inside_the_candidates_is_caught(world):
    gone = next(iter(json.loads(world.dropped.read_text())))

    def f(rows):
        for r in rows:
            if r["source"] == "c2_md_gbif":
                r["meta"]["task_id"] = gone
                break
    rewrite_jsonl(world.cand, f)
    v, p = verdict(world)
    assert has(p, "dropped tasks (gate or schema) are in the candidates")


def test_a_surviving_task_may_not_vanish_from_the_candidates(world):
    t = next(r["meta"]["task_id"] for r in fin.jl(world.cand) if r["source"] == "c2_md_cordis_h2020")
    rewrite_jsonl(world.cand, lambda rows: [r for r in rows if r["meta"]["task_id"] != t])
    v, p = verdict(world)
    assert has(p, "surviving tasks are missing from the candidates")


def test_schema_drop_is_rederived(world):
    edit_json(world.dropped, lambda d: d["md_cma:accdecade"].update(reason="schema: something else"))
    assert has(verdict(world)[1], "schema-dropped task md_cma:accdecade: reason")
    edit_json(world.dropped, lambda d: d["md_cma:accdecade"].update(reason="schema: choice row: 2-9 options (C2 natural sets)", rows=19))
    assert has(verdict(world)[1], "schema-dropped task md_cma:accdecade: 20 rows")


def test_a_task_dropped_for_schema_that_passes_the_schema_is_caught(world):
    def f(d):
        d["md_cma:ghost"] = {"source": "c2_md_cma", "reason": "schema: x", "rows": 3}
    edit_json(world.dropped, f)
    assert has(verdict(world)[1], "is not a task of the source")


def test_noise_gate_inputs_are_sha_bound(world):
    v1, _ = verdict(world)
    f = sorted((world.parts / "worldbank" / "noise_gate" / "answers").glob("*.json"))[0]
    d = json.loads(f.read_text())
    d["note"] = "changed"
    f.write_text(json.dumps(d))
    v2, _ = verdict(world)
    assert v1["noise_gate"]["inputs_sha256"] != v2["noise_gate"]["inputs_sha256"]
    assert v1["noise_gate"]["inputs_sha256_by_source"]["fsa"] == v2["noise_gate"]["inputs_sha256_by_source"]["fsa"]


def test_a_deviation_the_record_does_not_carry_is_caught(world):
    edit_json(world.qc, lambda d: d.update(deviations=[]))
    v, p = verdict(world)
    assert has(p, "A51 (c) deviations differ") and not has(p, "tasks per source outside")     # the floor uses the derived deviation, not the record


def test_deviation_is_not_taken_from_the_record(world):
    """A fake A51 (c) deviation for a source that is not short is ignored (the live ones are derived from the answers)."""
    edit_json(world.qc, lambda d: d["deviations"].append(dict(d["deviations"][0], block_source="c2_md_fsa", tasks_in=42, tasks_dropped_by_gate=2, tasks_kept=40)))
    assert has(verdict(world)[1], "A51 (c) deviations differ")


# ============================================================================================================ 5 twins
@pytest.fixture(scope="module")
def twin_world():
    rows = fin.jl(LIVE_MD / "out" / "candidates_c2.jsonl")
    by = {r["id"]: r for r in rows}
    tw = [r for r in rows if (r["meta"].get("negtwin"))]
    keep = {r["id"] for r in tw} | {r["meta"]["negtwin"]["base_id"] for r in tw}
    pats, pairs = FZ.load_trained()
    return [r for r in rows if r["id"] in keep], pats, pairs, by


def test_twin_check_passes_on_the_live_twins(twin_world):
    rows, pats, pairs, _ = twin_world
    rep, p = fin.twin_check(rows, pats, pairs, set())
    assert p == [] and rep["twins"] == 492 and rep["program_check_failures"] == {}


def test_a_twin_using_a_pattern_dropped_by_the_audit_is_caught(twin_world):
    rows, pats, pairs, _ = twin_world
    pid = next(r["meta"]["negtwin"]["pattern"] for r in rows if r["meta"].get("negtwin"))
    rep, p = fin.twin_check(rows, pats, pairs, {pid})
    assert has(p, "pattern dropped by the pooled Sonnet/Opus audit")


def test_a_pattern_outside_the_frozen_catalogue_is_caught(twin_world):
    rows, pats, pairs, _ = twin_world
    rows = copy.deepcopy(rows)
    next(r for r in rows if r["meta"].get("negtwin"))["meta"]["negtwin"]["pattern"] = "FRAME_NOT|DO|000000|not|-|-|-"
    assert has(fin.twin_check(rows, pats, pairs, set())[1], "pattern not in the frozen trained catalogue")


def test_two_predicate_edits_fail_the_program_check(twin_world):
    rows, pats, pairs, _ = twin_world
    rows = copy.deepcopy(rows)
    t = next(r for r in rows if r["meta"].get("negtwin") and r["meta"]["negtwin"]["op"] in ("FRAME_NOT", "FAIL_TO", "LACK"))
    t["instructions"] = t["instructions"].replace("?", " in the tenth year?")          # one more edit beyond the operator, still one question
    rep, p = fin.twin_check(rows, pats, pairs, set())
    assert has(p, "twin program check:") and any(k.startswith("check_pair") for k in rep["program_check_failures"])


def test_g_tw_gold_flip_fails(twin_world):
    rows, pats, pairs, _ = twin_world
    rows = copy.deepcopy(rows)
    next(r for r in rows if r["meta"].get("negtwin"))["gold"] ^= 1
    rep, p = fin.twin_check(rows, pats, pairs, set())
    assert not rep["g_tw"]["pass"] and has(p, "G-TW")


def test_twin_without_a_base_fails(twin_world):
    rows, pats, pairs, _ = twin_world
    t = next(r for r in rows if r["meta"].get("negtwin"))
    rows = [r for r in rows if r["id"] != t["meta"]["negtwin"]["base_id"]]
    assert has(fin.twin_check(rows, pats, pairs, set())[1], "twins with a known pattern and a base")


def test_relation_role_must_match_the_pattern(twin_world):
    rows, pats, pairs, _ = twin_world
    rows = copy.deepcopy(rows)
    t = next(r for r in rows if r["role"] == "equiv" and r["meta"].get("negtwin"))
    t["role"] = "complement"
    assert has(fin.twin_check(rows, pats, pairs, set())[1], "role / op / kind differ from the pattern")


def test_edit_site_and_a48h_guards_are_run(twin_world, monkeypatch):
    rows, pats, pairs, _ = twin_world
    with monkeypatch.context() as m:
        m.setattr(fin.K, "bad_edit_site", lambda b, t: True)
        assert has(fin.twin_check(rows, pats, pairs, set())[1], "edit site (A48 h iv)")
    with monkeypatch.context() as m:
        m.setattr(fin.C, "a48h_class", lambda p: "x")
        assert has(fin.twin_check(rows, pats, pairs, set())[1], "A48 h pattern class")


def test_audit_report_must_name_the_same_twin_count(world):
    qc = json.loads(world.qc.read_text())
    ok = fin.audit_check(world, qc, 492)
    assert ok[2] == [] and len(ok[0]) == 18
    assert has(fin.audit_check(world, qc, 491)[2], "names 492 MD twins")
    edit_json(world.audit, lambda d: d.update(dry_run=True))
    assert has(fin.audit_check(world, qc, 492)[2], "is a dry run")
    edit_json(world.audit, lambda d: d.update(dry_run=False, n_patterns_dropped=17))
    assert has(fin.audit_check(world, qc, 492)[2], "n_patterns_dropped")
    edit_json(world.audit, lambda d: d.update(n_patterns_dropped=18, patterns_dropped=d["patterns_dropped"][:-1]))
    assert has(fin.audit_check(world, qc, 492)[2], "n_patterns_dropped")
    qc2 = copy.deepcopy(qc)
    qc2["negtwin_audit"]["final_twins"] = 1545
    assert has(fin.audit_check(world, qc2, 492)[2], "negtwin_audit.final_twins")


def test_a_twin_on_a_dropped_pattern_in_the_file_fails_the_verdict(world):
    pid = next(r["meta"]["negtwin"]["pattern"] for r in fin.jl(world.cand) if r["meta"].get("negtwin"))
    edit_json(world.audit, lambda d: d.update(patterns_dropped=d["patterns_dropped"][:-1] + [pid]))
    assert has(verdict(world)[1], "pattern dropped by the pooled Sonnet/Opus audit")


# ============================================================================================================ 6 pooled shares
def test_pooled_shares_recomputed_from_the_files(world):
    qc = json.loads(world.qc.read_text())
    audit = json.loads(world.audit.read_text())
    rep, p = fin.pooled_check(world, qc, fin.jl(world.cand), audit)
    assert p == [] and rep["by_kind"] == {"syntactic": 26, "implicit": 19, "antonym": 27} and rep["by_block"]["GB"] == {"antonym": 3, "syntactic": 2, "implicit": 4}


def comp(kind, n):
    return [{"id": f"c{kind}{i}", "role": "complement", "meta": {"negtwin": {"kind": kind}}} for i in range(n)]


def test_pooled_shares_below_the_bar_fail(world):
    qc = {"a60": {"pooled_after": {"by_kind": {"syntactic": 40, "implicit": 5, "antonym": 5}}, "block": {"complement_after_by_kind": {"syntactic": 40, "implicit": 5, "antonym": 5}}}}
    audit = {"pooled_spec_3_18_shares": {"by_kind": {"syntactic": 40, "implicit": 5, "antonym": 5}}}
    rows = comp("syntactic", 40) + comp("implicit", 5) + comp("antonym", 5)
    rep, p = fin.pooled_check(world, qc, rows, audit, gb_rows=[], rtw_rows=[])
    assert has(p, "implicit 0.1") and has(p, "antonym 0.1") and has(p, "syntactic 0.8")
    # exact fractions: 25% implicit passes, one fewer fails
    rows = comp("syntactic", 45) + comp("implicit", 25) + comp("antonym", 30)
    qc["a60"]["pooled_after"]["by_kind"] = qc["a60"]["block"]["complement_after_by_kind"] = audit["pooled_spec_3_18_shares"]["by_kind"] = {"syntactic": 45, "implicit": 25, "antonym": 30}
    assert fin.pooled_check(world, qc, rows, audit, gb_rows=[], rtw_rows=[])[1] == []
    rows = comp("syntactic", 45) + comp("implicit", 24) + comp("antonym", 30)
    assert has(fin.pooled_check(world, qc, rows, audit, gb_rows=[], rtw_rows=[])[1], "implicit")


def test_pooled_shares_must_equal_the_records(world):
    def f(rows):
        for r in rows:
            if r.get("role") == "complement" and r["meta"].get("negtwin", {}).get("kind") == "syntactic":
                r["meta"]["negtwin"]["kind"] = "antonym"
                return
    rewrite_jsonl(world.gb / "out" / "candidates_c2.jsonl", f)
    v, p = verdict(world)
    assert has(p, "QC record a60.pooled_after.by_kind") and has(p, "pooled audit report pooled_spec_3_18_shares.by_kind")


def test_unknown_kind_is_a_problem(world):
    rows = comp("syntactic", 3) + comp("implicit", 1) + comp("antonym", 2) + comp("weird", 1)
    qc = {"a60": {}}
    assert has(fin.pooled_check(world, qc, rows, {}, gb_rows=[], rtw_rows=[])[1], "without a known kind")


# ============================================================================================================ 7 sources
def test_row_licence_must_be_the_part_manifest_licence(world):
    def f(rows):
        for r in rows:
            if r["source"] == "c2_md_usgs":
                r["meta"]["licence"] = "All rights reserved"
    rewrite_jsonl(world.cand, f)
    assert has(verdict(world)[1], "rows of c2_md_usgs do not carry the part MANIFEST licence")


def test_record_licence_must_be_the_part_manifest_licence(world):
    edit_json(world.qc, lambda d: d["gates_run"]["A42D_8_3_licence_and_name_checks_recorded_by_the_mappers"]["licence"].update(usgs="CC0"))
    assert has(verdict(world)[1], "licence of usgs: the QC record's differs")


def test_manifest_without_a_licence_fails(world):
    edit_json(world.parts / "ror" / "MANIFEST.json", lambda d: d.pop("licence"))
    v, p = verdict(world)
    assert has(p, "licence of ror") or has(p, "do not carry")


def test_a61_barred_source_fails(world, monkeypatch):
    monkeypatch.setattr(fin, "BARRED_A61", ("md_fdc", "md_gbif"))
    assert has(verdict(world)[1], "A61-barred sources in the block: ['md_gbif']")


def test_a_row_source_naming_a_barred_source_fails(mm, world):
    rows = fin.jl(world.cand)[:3]
    for r in rows:
        r["source"] = "c2_md_peps"
    rep, p = fin.sources_check(mm, world, json.loads(world.qc.read_text()), rows, DENY_OK, only={"ror"})
    assert has(p, "A61-barred") or has(p, "barred")


def test_gated_membership_needs_a_binding_input_id(mm, world):
    rows = fin.jl(world.cand)[:3]
    for r in rows:
        r["source"] = "c2_md_notasource"
    rep, p = fin.sources_check(mm, world, json.loads(world.qc.read_text()), rows, DENY_OK, only={"ror"})
    assert has(p, "have no id in the binding inputs")


def test_binding_input_sha_is_checked(world):
    world.sources_cand.write_text(world.sources_cand.read_text() + " ")
    assert has(verdict(world)[1], "SOURCES_CANDIDATES.json differs from the ruling's sha256")


def test_kit_validate_row_is_rerun(world):
    def f(rows):
        rows[5]["gold"] = "maybe"
    rewrite_jsonl(world.cand, f)
    v, p = verdict(world)
    assert has(p, "kit validate_row")


def test_denylist_lines_are_judged(mm, world):
    qc = json.loads(world.qc.read_text())
    rows = fin.jl(world.cand)
    ok, p = fin.sources_check(mm, world, qc, rows, DENY_OK)
    assert p == [] and ok["denylist"]["md_cma"].startswith("OVERLAP c1:github only") and ok["denylist"]["md_gbif"] == "CLEAR"
    assert has(fin.sources_check(mm, world, qc, rows, DENY_OK.replace("md_gbif CLEAR", "md_gbif OVERLAP c1:openfda"))[1], "md_gbif OVERLAP c1:openfda")
    assert has(fin.sources_check(mm, world, qc, rows, DENY_OK.replace("md_cma OVERLAP c1:github", "md_cma OVERLAP c1:github; deny:foo"))[1], "md_cma OVERLAP")
    assert has(fin.sources_check(mm, world, qc, rows, DENY_OK.replace("md_ror CLEAR\n", ""))[1], "has no line for md_ror")


def test_run_denylist_runs_the_script_and_fails_on_error(world, tmp_path):
    ok = tmp_path / "ok.py"
    ok.write_text("print('md_x CLEAR')\n")
    P = fin.Paths(md=world.md, parts=world.parts, denylist=ok)
    assert fin.run_denylist(P) == "md_x CLEAR\n"
    bad = tmp_path / "bad.py"
    bad.write_text("import sys; sys.exit(3)\n")
    with pytest.raises(RuntimeError):
        fin.run_denylist(fin.Paths(md=world.md, parts=world.parts, denylist=bad))


# ============================================================================================================ 8 record
def test_build_record_replaces_the_stale_blocks_and_lists_the_pending_gates(world):
    v, p = verdict(world)
    qc = json.loads(world.qc.read_text())
    rec = fin.build_record(qc, v, "2026-10-17T10:00:00Z")
    assert rec["pass"] is True and rec["passed_utc"] == "2026-10-17T10:00:00Z" and rec["fix_iterations"] == 0 and rec["problems"] == []
    assert rec["gates_run"]["A42D_8_2_caps"]["block_rows"] == 10491 and rec["gates_run"]["A42D_8_2_caps"]["twins"] == 492
    assert rec["superseded_at_finalize"]["gates_run.A42D_8_2_caps"]["block_rows"] == 9999
    assert rec["superseded_at_finalize"]["negtwin_gates"]["twins"] == 1545 and rec["negtwin_gates"]["twins"] == 492
    assert rec["negtwin_gates"]["g_tw"]["n_pairs"] == 492
    pend = " ".join(rec["gates_pending"])
    for need in ("OHS-AC", "g13_c2.py candidates --block MD", "ohsac_hash", "crowd selection", "A61 (f)", "single final-mix", "A61 (e 5)", "--remove-sources"):
        assert need in pend, need
    assert set(rec["files"]) == {"candidates_c2.jsonl", "candidates_c2.relations.jsonl", "MANIFEST.json", "c3_hold_a60.jsonl", "c3_hold_a60.relations.jsonl"}
    assert all(len(x["sha256"]) == 64 for x in rec["files"].values())
    assert "pass is false on purpose" not in json.dumps({k: rec[k] for k in ("note", "stage")})
    assert rec["gates_run"]["A51_noise_gate_rederived"]["tasks_flagged_total"] == 9
    # the input record is untouched (deepcopy)
    assert qc["pass"] is False and "negtwin_gates" in qc
    files = {c2io.CAND: world.cand, c2io.REL: world.rel}
    assert fin.mx.qc_binding(rec, files) == [] and mix_c2.admission("MD", rec, []) == []


def test_admission_is_simulated_and_a_late_pass_is_refused(world):
    v, p = fin.verdict(world, denylist_out=DENY_OK, now="2026-10-22T00:00:00Z")
    assert not v["would_pass"] and has(p, "simulated admission") and has(p, "after the data cutoff")


# ============================================================================================================ --write
def test_write_backs_up_first_and_changes_only_the_record(world):
    root = world.md.parent.parent
    before = tree(root)
    v, p = verdict(world)
    assert p == []
    bk = fin.write(world, v, now="2026-10-17T10:00:00Z")
    after = tree(root)
    changed = {k for k in set(before) | set(after) if before.get(k) != after.get(k)}
    rel_qc = str(world.qc.relative_to(root))
    rel_bk = str(bk.relative_to(root))
    assert changed == {rel_qc, rel_bk}                                           # nothing else: not the rows, relations, MANIFEST, hold, parts
    assert after[rel_bk] == before[rel_qc]                                       # the backup is the original bytes
    assert bk.parent.parent.name == fin.BACKUP_DIR
    rec = json.loads(world.qc.read_text())
    assert rec["pass"] is True and rec["finalize"]["utc"] == "2026-10-17T10:00:00Z"
    assert mix_c2.admission("MD", rec, fin.mx.qc_binding(rec, {c2io.CAND: world.cand, c2io.REL: world.rel})) == []
    with pytest.raises(RuntimeError, match="already has pass=true"):
        fin.write(world, dict(v, qc_sha256_read=shaf(world.qc)))


def test_write_refuses_when_the_record_changed_after_the_verdict(world):
    v, p = verdict(world)
    edit_json(world.qc, lambda d: d.update(stage="edited"))
    before = tree(world.md.parent.parent)
    with pytest.raises(RuntimeError, match="changed since"):
        fin.write(world, v)
    assert tree(world.md.parent.parent) == before


def test_write_never_overwrites_a_backup(world):
    v, p = verdict(world)
    fin.backup(world, stamp="20261017T100000Z")
    with pytest.raises(FileExistsError):
        fin.backup(world, stamp="20261017T100000Z")


def test_main_write_refuses_on_a_failing_input_and_writes_nothing(world):
    root = world.md.parent.parent
    rewrite_jsonl(world.cand, lambda rows: rows[:-1])
    before = tree(root)
    assert fin.main(["--write"], P=world, denylist_out=DENY_OK) == 2
    assert tree(root) == before and not (world.qc.parent / fin.BACKUP_DIR).exists()


def test_main_write_succeeds_on_a_good_copy(world):
    assert fin.main(["--write"], P=world, denylist_out=DENY_OK) == 0
    assert json.loads(world.qc.read_text())["pass"] is True
    assert len(list((world.qc.parent / fin.BACKUP_DIR).glob("*/QC_REPORT.json"))) == 1


def test_a_written_record_that_fails_admission_is_rolled_back(world, monkeypatch):
    v, p = verdict(world)
    orig = world.qc.read_bytes()
    real = mix_c2.admission
    calls = []

    def bad(block, qc, binding, *a, **k):
        calls.append(1)
        return ["x: forced"]
    monkeypatch.setattr(fin.mix_c2, "admission", bad)
    with pytest.raises(RuntimeError, match="backup restored"):
        fin.write(world, v)
    assert world.qc.read_bytes() == orig and calls


def test_the_live_tree_is_not_touched_by_these_tests():
    assert json.loads((LIVE_MD / "qc" / "QC_REPORT.json").read_text()).get("pass") in (False, True)

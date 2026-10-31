"""families/T31/test_freeze_v2.py: tests for freeze_v2.py (the T31 pools_v2 re-freeze), in memory only.

Covers: the answer-file contract (whole-file breaks reject the file, entry breaks reject the entry, nothing is edited,
a rejected entry is never a vote); G-LEX vote recording under the kit rules (2/2, 3/3 for precedence and window, null or
another meaning rejects for good, one read stays pending); the G0 targets (pinned: never lowered) and the exact
shortfalls; the gate scope (used forms vs the whole registry) and the frozen-file audit that catches a rejected form in
a pool; the pure write plan (a partial freeze is archived, a READY one is never replaced); and the whole freeze over the
real folders: v1 reproduced byte for byte, equality with topup.admit2 when every file is valid, the new reads loaded,
`check` writes nothing, --exclude-task leaves forms pending, --strict-files blocks on the v1 file with a mistyped qid,
the generator renders rows from the pools with the per-row G-LEX check clean, and (when pools_v2/ was written by this
script) its files equal what the script computes now.

Run (from lean/):  PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python -m pytest -q -p no:cacheprovider \
                   c2_build/families/T31/test_freeze_v2.py
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker as CH  # noqa: E402
from c2_kit import paths, pipeline  # noqa: E402
from c2_kit.lexicon import LexiconRegistry  # noqa: E402
from families.T31 import extract_build as EB  # noqa: E402
from families.T31 import freeze_v2 as FZ  # noqa: E402
from families.T31 import glex_admit as GA  # noqa: E402
from families.T31 import haiku_author as HA  # noqa: E402
from families.T31 import plugin as P  # noqa: E402
from families.T31 import topup as T  # noqa: E402


def td(kind="author_wording", qids=("qa", "qb"), key=None, choices=None):
    return FZ.TaskDef("t", "T31-test-000", "T31-test", kind, key or FZ.value_key(kind), tuple(qids),
                      Path("answers/x.json"), choices=choices or {})


def raw(obj) -> bytes:
    return json.dumps(obj).encode("utf-8")


def text_ans(qids, **over):
    return [{"qid": q, "text": over.get(q, f"text for {q}")} for q in qids]


# ======================================================================================== the answer contract

def test_a_valid_text_file_is_accepted_in_full():
    r = FZ.validate_answer_bytes(raw(text_ans(["qb", "qa"])), td())
    assert r["status"] == "valid" and r["n_valid"] == 2 and not r["item_problems"] and not r["unanswered"]
    assert [e["qid"] for e in r["entries"]] == ["qb", "qa"]


@pytest.mark.parametrize("data", [
    b"", b"not json", b'```json\n[{"qid": "qa", "text": "x"}]\n```', b'{"answers": []}', b'"qa"',
    b'\xef\xbb\xbf[{"qid": "qa", "text": "x"}]', b"\xff\xfe", b'[{"qid": "qa", "qid": "qb", "text": "x"}]',
    b'[{"qid": "qa", "text": NaN}]', b'["qa", "qb"]', b'[{"qid": "qa", "text": "x"}] trailing'])
def test_a_whole_file_break_rejects_the_file(data):
    r = FZ.validate_answer_bytes(data, td())
    assert r["status"] == "invalid" and r["entries"] == [] and r["file_problems"]
    assert r["unanswered"] == ["qa", "qb"]


@pytest.mark.parametrize("answers, why", [
    ([{"qid": "qa", "text": "x", "extra": 1}, {"qid": "qb", "text": "y"}], "keys"),
    ([{"qid": "qa"}, {"qid": "qb", "text": "y"}], "keys"),
    ([{"qid": "qa", "txt": "x"}, {"qid": "qb", "text": "y"}], "keys"),
    ([{"qid": "qzz", "text": "x"}, {"qid": "qb", "text": "y"}], "not one of this task"),
    ([{"qid": 7, "text": "x"}, {"qid": "qb", "text": "y"}], "qid is not a string"),
    ([{"qid": "qa", "text": 5}, {"qid": "qb", "text": "y"}], "text is not a string"),
    ([{"qid": "qa", "text": "x"}, {"qid": "qa", "text": "z"}, {"qid": "qb", "text": "y"}], "answered 2 times"),
])
def test_an_entry_break_rejects_that_entry_and_keeps_the_rest(answers, why):
    r = FZ.validate_answer_bytes(raw(answers), td())
    assert r["status"] == "partial" and r["n_valid"] == 1 and [e["qid"] for e in r["entries"]] == ["qb"]
    assert why in " ".join(r["item_problems"])
    assert "qa" in r["unanswered"]                                    # a rejected entry is an unanswered item
    strict = FZ.validate_answer_bytes(raw(answers), td(), strict_files=True)
    assert strict["status"] == "invalid" and strict["entries"] == []


def test_a_qid_answered_twice_is_rejected_in_every_copy():
    r = FZ.validate_answer_bytes(raw([{"qid": "qa", "text": "x"}, {"qid": "qa", "text": "z"}]), td())
    assert r["status"] == "invalid" and r["entries"] == [] and len(r["item_problems"]) == 2


def test_an_unanswered_item_makes_a_file_partial_and_a_strict_file_invalid():
    r = FZ.validate_answer_bytes(raw(text_ans(["qa"])), td())
    assert r["status"] == "partial" and r["unanswered"] == ["qb"] and not r["item_problems"]
    assert FZ.validate_answer_bytes(raw(text_ans(["qa"])), td(), strict_files=True)["status"] == "invalid"


def test_a_file_with_no_valid_entry_is_invalid_even_in_the_item_policy():
    r = FZ.validate_answer_bytes(raw([{"qid": "zz", "text": "x"}]), td())
    assert r["status"] == "invalid" and r["entries"] == []


def test_a_lex_read_must_pick_a_listed_meaning_or_null():
    choices = {"qa": ("m1", "m2"), "qb": ("m1", "m2"), "qc": ("m1", "m2"), "qd": ("m1", "m2")}
    t = td("extract_lex", ["qa", "qb", "qc", "qd"], choices=choices)
    r = FZ.validate_answer_bytes(raw([{"qid": "qa", "choice": "m1"}, {"qid": "qb", "choice": None},
                                      {"qid": "qc", "choice": "something else"}, {"qid": "qd", "choice": 5}]), t)
    assert r["status"] == "partial" and {e["qid"] for e in r["entries"]} == {"qa", "qb"}
    assert len(r["item_problems"]) == 2 and r["unanswered"] == ["qc", "qd"]      # no vote, neither for nor against


def test_pack_and_name_list_contracts():
    pk = td("author_pack", ["qa"], key="pack")
    assert FZ.validate_answer_bytes(raw([{"qid": "qa", "pack": {"process": "x"}}]), pk)["status"] == "valid"
    assert FZ.validate_answer_bytes(raw([{"qid": "qa", "pack": ["x"]}]), pk)["status"] == "invalid"
    nm = td("author_pack", ["qa"], key="names")
    assert FZ.validate_answer_bytes(raw([{"qid": "qa", "names": ["Ana Ruiz"]}]), nm)["status"] == "valid"
    assert FZ.validate_answer_bytes(raw([{"qid": "qa", "names": ["Ana Ruiz", 3]}]), nm)["status"] == "invalid"
    assert FZ.value_key("author_pack", "both") == "names" and FZ.value_key("author_pack", "appr") == "pack"
    with pytest.raises(ValueError):
        FZ.value_key("extract_g3h")


def test_read_answer_file_reports_missing_excluded_and_never_edits(tmp_path):
    if paths.never_open(tmp_path):
        pytest.skip("pytest tmp folder is on the never-open list")
    good, bad = raw(text_ans(["qa", "qb"])), b"oops"
    for name, data in (("good.json", good), ("bad.json", bad)):
        (tmp_path / name).write_bytes(data)
    mk = lambda f: FZ.TaskDef("t", f"T-{f}", "T", "author_wording", "text", ("qa", "qb"), tmp_path / f"{f}.json")  # noqa: E731
    ok, r_ok = FZ.read_answer_file(mk("good"), set(), False)
    assert ok and r_ok["status"] == "valid" and r_ok["sha256"] == hashlib.sha256(good).hexdigest()
    none, r_bad = FZ.read_answer_file(mk("bad"), set(), False)
    assert none is None and r_bad["status"] == "invalid" and r_bad["problems"]
    none, r_ex = FZ.read_answer_file(mk("good"), {"T-good"}, False)
    assert none is None and r_ex["status"] == "excluded" and "audit failed" in r_ex["problems"][0]
    none, r_miss = FZ.read_answer_file(mk("nope"), set(), False)
    assert none is None and r_miss["status"] == "missing" and r_miss["unanswered"] == ["qa", "qb"]
    assert (tmp_path / "good.json").read_bytes() == good and (tmp_path / "bad.json").read_bytes() == bad
    planned = mk("good")
    planned.problems = ["chunk file differs from its manifest sha256"]
    none, r_plan = FZ.read_answer_file(planned, set(), False)
    assert none is None and r_plan["status"] == "invalid" and r_plan["plan_problems"]


# ======================================================================================== G-LEX under the kit rules

def _mini_registry():
    reg = HA.declare_lexicon(LexiconRegistry("T31"))
    forms = [reg.add("Who holds the accountable role for request {REQ_ID}?", "q.t31.ch_approver",
                     slots={"REQ_ID": "id"}, source="haiku", family="T31", haiku_task_id="T-0", haiku_prompt_sha="0" * 64),
             reg.add("Which person holds the accountable role?", "q.t31.ch_approver", source="haiku", family="T31",
                     haiku_task_id="T-0", haiku_prompt_sha="0" * 64)]
    reg.unit_test_all()
    return reg, [f.form_id for f in forms]


def _answers_for(batch, reg, choose):
    """{task_id: [entries]} for one extract batch; choose(form) -> the meaning text, or None."""
    out = {}
    items = CH.item_by_internal(batch)
    inv = {v: k for k, v in batch.key.items()}
    for c in batch.chunks:
        out[c["task_id"]] = []
    for fid, qid in sorted(inv.items()):
        f = reg.forms[fid]
        pick = choose(f)
        tid = batch.task_of[qid]
        out[tid].append({"qid": qid, "choice": pick})
    del items
    return out


def _record(reg, fids, choose_by_read, rounds=("read0", "read1")):
    batches = dict(EB.extraction_batches(reg, fids))
    man = {"tasks": []}
    valid = {}
    for read, b in batches.items():
        for tid, ans in _answers_for(b, reg, choose_by_read[read]).items():
            valid[("v1-extract", tid)] = ans
            man["tasks"].append({"task_id": tid, "read": read})
    FZ.record_reads(reg, {r: batches[r] for r in rounds if r in batches}, valid, "v1-extract", man)
    return reg


def _meaning(reg, f):
    return reg.sems[f.sem_id].meaning


def test_two_independent_reads_admit_a_question_form_and_one_null_rejects_for_good():
    reg, (a, b) = _mini_registry()
    same = lambda f: _meaning(reg, f)  # noqa: E731
    only_a_null = lambda f: None if f.form_id == b else _meaning(reg, f)  # noqa: E731
    _record(reg, [a, b], {"read0": same, "read1": only_a_null})
    assert reg.status(a) == "admitted" and reg.forms[a].required == 2
    assert reg.status(b) == "rejected"                                  # null from one read: rejected, no re-vote
    gate = reg.gate([a])
    assert gate["pass"] and not reg.gate([a, b])["pass"] and not reg.gate()["pass"]


def test_one_read_leaves_a_form_pending_and_another_meaning_rejects():
    reg, (a, b) = _mini_registry()
    same = lambda f: _meaning(reg, f)  # noqa: E731
    _record(reg, [a, b], {"read0": same, "read1": same}, rounds=("read0",))
    assert reg.status(a) == reg.status(b) == "pending"                  # one read of two
    reg2, (a2, b2) = _mini_registry()

    def other(f):
        return next(m for m in (s.meaning for s in reg2.sems.values() if s.kind == "question")
                    if m != _meaning(reg2, f))
    _record(reg2, [a2, b2], {"read0": lambda f: _meaning(reg2, f), "read1": other})
    assert {reg2.status(a2), reg2.status(b2)} == {"rejected"}           # a decoy / other meaning: rejected for good


def test_precedence_and_window_forms_need_three_reads_everything_else_two():
    from c2_kit.lexicon import STRICT_KINDS
    reg = LexiconRegistry("T99")
    reg.declare("prec.P1", "precedence", "deny rules beat ask rules, which beat allow rules")
    reg.declare("win.rolling", "window", "a rolling window of requests")
    reg.declare("cmp.le", "comparator", "less than or equal to the bound")
    p = reg.add("deny beats ask beats allow", "prec.P1")
    w = reg.add("the window rolls with every request", "win.rolling")
    c = reg.add("no more than {X}", "cmp.le", slots={"X": "cents"})
    reg.unit_test_all()
    assert (p.required, w.required, c.required) == (3, 3, 2) and set(STRICT_KINDS) == {"precedence", "window"}
    for e in ("a", "b"):
        for f in (p, w, c):
            reg.record_extraction(f.form_id, e, f.sem_id)
    assert reg.status(p.form_id) == reg.status(w.form_id) == "pending" and reg.status(c.form_id) == "admitted"
    for f in (p, w):
        reg.record_extraction(f.form_id, "c", f.sem_id)
    assert reg.status(p.form_id) == reg.status(w.form_id) == "admitted"
    with pytest.raises(Exception):
        reg.record_extraction(p.form_id, "c", p.sem_id)                 # extractors must be distinct


# ======================================================================================== targets and shortfalls

def test_the_g0_targets_are_pinned_and_never_lowered():
    assert FZ.G0_TARGETS is GA.G0_TARGETS
    assert dict(FZ.G0_TARGETS) == {
        "skins_train_per_register_track": 24, "skins_held_per_register_track": 12, "wordings_admitted_min": 30,
        "wordings_pool_candidates": 170, "packs_per_track": 30, "names": 300, "mode_f_share_max": 0.25,
        "comparator_senses_admitted_min": 1}


@pytest.fixture(scope="module")
def built():
    return FZ.assemble()


def test_each_g0_miss_is_reported_exactly(built):
    c = copy.deepcopy(built["c"])
    assert GA.shortfalls(c) == []
    c["skins_by_register_track"]["chat|appr"]["total"] = 23
    c["skins_by_register_track"]["export|agent"]["total"] = 11
    c["wordings_admitted"] = 29
    c["wordings_candidates"] = 169
    c["packs_agent"] = 29
    c["names"] = 299
    c["mode_F_share"] = 0.26
    c["comparator_admitted_by_sense"] = {k: v for k, v in c["comparator_admitted_by_sense"].items() if k != "cmp.gt"}
    got = GA.shortfalls(c)
    assert got == ["skins chat|appr: 23 < 24 (G0 7, training)", "skins export|agent: 11 < 12 (G0 7, held-out)",
                   "wordings admitted 29 < 30", "wording candidates 169 < about 170 (G0 7 pool target)",
                   "packs agent: 29 < 30 (G0 7)", "names 299 < 300 (G0 7)", "Mode F share 0.26 > 0.25 (G0 7)",
                   "comparator sense cmp.gt: 0 admitted < 1 (G0 7 needs every sense)"]


# ======================================================================================== the write plan

def test_plan_write_archives_a_partial_freeze_and_never_replaces_a_ready_one():
    new = {"MANIFEST.json": "{}", "skins.json": "[]", "VALIDATION_REPORT.json": "{}"}
    old = {"MANIFEST.json": json.dumps({"status": "PARTIAL: x", "ready": False}), "skins.json": "[1]"}
    plan = FZ.plan_write(old, new, json.loads(old["MANIFEST.json"]), archive_nonempty=False)
    assert plan["problems"] == [] and plan["archive"] == old
    ready = {"MANIFEST.json": json.dumps({"status": "READY: y", "ready": True})}
    assert "already READY" in " ".join(FZ.plan_write(ready, new, json.loads(ready["MANIFEST.json"]), False)["problems"])
    assert "already holds files" in " ".join(FZ.plan_write(old, new, json.loads(old["MANIFEST.json"]), True)["problems"])
    odd = {**old, "extra.json": "[]"}
    assert "nothing is deleted" in " ".join(FZ.plan_write(odd, new, json.loads(old["MANIFEST.json"]), False)["problems"])
    empty = FZ.plan_write({}, new, None, False)
    assert empty == {"archive": {}, "problems": []}


# ======================================================================================== the real folders

def test_v1_is_reproduced_byte_for_byte_and_untouched(built):
    integ = built["integrity"]
    assert integ["ok"], integ["problems"]
    man = json.loads((FZ.POOLS_V1 / "MANIFEST.json").read_text(encoding="utf-8"))
    assert integ["files"] == man["sha256"]
    st = GA.admit()                                         # the unchanged v1 pipeline reads the same disk files
    files = GA._files(st, GA.counts(st), GA.shortfalls(GA.counts(st)))
    assert {n: hashlib.sha256(t.encode()).hexdigest() for n, t in files.items()} == man["sha256"]


def test_every_answer_file_of_every_round_is_checked(built):
    recs = built["records"]
    by = {}
    for r in recs:
        by.setdefault(r["round"], []).append(r)
    assert {k: len(v) for k, v in by.items()} == {"v1-author": 32, "redo1": 1, "v1-extract": 8, "redo2": 11,
                                                  "redo2-extract": 2}
    assert all(r["sha256"] for r in recs) and not built["stray"] and not built["unknown_dirs"]
    findings = [r for r in recs if r["status"] != "valid"]
    assert [(r["task_id"], r["status"]) for r in findings] == [("T31-author_wording-a7e52c11-000", "partial")]
    assert findings[0]["unanswered"] == ["qc40242781b"] and "q40242781b" in findings[0]["rejected_entries"][0]
    assert built["st"]["problems"]["unanswered_after_redo"] == {}       # the redo task answered that item
    assert built["st"]["resolved_by_redo"] == ["T31-author_wording-a7e52c11-000"]
    new_reads = [r for r in recs if r["round"] == "redo2-extract"]
    assert [r["status"] for r in new_reads] == ["valid", "valid"] and all(r["n_valid"] == 36 for r in new_reads)


def test_the_new_reads_are_recorded_as_two_independent_extractors(built):
    reg = built["st"]["reg"]
    rc = built["st"]["read_counts"]
    for read in ("r2read0", "r2read1"):
        assert rc[read]["unanswered"] == 0 and rc[read].get("listed", 0) + rc[read].get("null", 0) == 36
    new = set(built["st"]["new_forms"])
    assert len(new) == 36
    for fid in new:
        assert {e for e, _ in reg.forms[fid].extractions} == {"r2read0", "r2read1"}
    for fid, f in reg.forms.items():
        assert not [s for _e, s in f.extractions if s is not None and s != f.sem_id] or reg.status(fid) == "rejected"
        if reg.status(fid) == "admitted":
            assert len({e for e, _ in f.extractions}) >= f.required == 2
    assert not [f for f in reg.forms.values() if f.kind in ("precedence", "window")]


def test_ready_matches_the_targets_and_gates(built):
    g = built["gates"]["G-LEX"]
    assert built["ready"] == (not built["short"] and g["pass"] and not built["blockers"])
    assert built["ready"], (built["short"], built["blockers"])
    assert g["used_forms_gate"]["pass"] and g["used_forms"] == len(built["audit"]["used_forms"]) == 216
    assert g["registry_gate_informational"]["pass"] is False             # rejected forms stay in the registry for good
    assert g["every_not_admitted_form_is_excluded"] and not g["pending_forms"]
    assert set(g["registry_not_admitted"].values()) == {"rejected"}
    assert g["strict_kind_forms"] == 0


def test_the_pool_only_holds_admitted_forms_and_the_frozen_audit_is_clean(built):
    aud = built["audit"]
    assert aud["problems"] == []
    reg = aud["registry"]
    w = json.loads(built["files"]["wordings.json"])["wordings"]
    assert w and all(reg.status(x["form_id"]) == "admitted" for x in w)
    assert {x["form_id"] for x in w} <= set(aud["used_forms"])
    assert not {x["form_id"] for x in w} & set(aud["gate_registry"]["not_admitted"])
    assert FZ.recount(built["files"])["wordings_admitted"] == built["c"]["wordings_admitted"]


def test_the_audit_catches_a_rejected_form_in_a_pool(built):
    files = dict(built["files"])
    w = json.loads(files["wordings.json"])
    bad_fid = sorted(built["audit"]["gate_registry"]["not_admitted"])[0]
    w["wordings"][0]["form_id"] = bad_fid
    files["wordings.json"] = FZ.dump(w)
    aud = FZ.audit_files(files, built["st"], built["c"], built["short"])
    text = " ".join(aud["problems"])
    assert "used forms not admitted" in text and "does not match its lexicon form" in text
    assert aud["gate_used"]["pass"] is False


def test_the_audit_catches_a_form_admitted_on_too_few_reads(built):
    files = dict(built["files"])
    lex = json.loads(files["lexicon.json"])
    f = next(x for x in lex["forms"] if x["status"] == "admitted")
    f["extractions"] = f["extractions"][:1]
    files["lexicon.json"] = FZ.dump(lex)
    aud = FZ.audit_files(files, built["st"], built["c"], built["short"])
    assert any("differs from its votes" in p or "fewer than" in p for p in aud["problems"])


def test_equal_to_topup_admit2_when_every_file_is_valid(built):
    st2 = T.admit2()
    c2 = GA.counts(st2)
    files2 = GA._files(st2, c2, GA.shortfalls(c2))
    files, c, short = FZ.pool_files(built["st"], final=False)
    assert c == c2 and short == GA.shortfalls(c2)
    for name in files2:
        if name != "QUARANTINE.json":
            assert files[name] == files2[name], name
    v2 = {(r["piece"], r["stage"]) for r in json.loads(files["QUARANTINE.json"])["rows"]}
    t2 = {(r["piece"], r["stage"]) for r in json.loads(files2["QUARANTINE.json"])["rows"]}
    assert t2 <= v2 and {s for _p, s in v2 - t2} == {"answer-contract"}


def test_the_frozen_files_carry_each_wordings_form_id_and_the_g0_pin(built):
    files = FZ.build_files(built)
    man = json.loads(files["MANIFEST.json"])
    assert man["g0"]["matches_plugin_pin"] and man["version"] == "freeze-v2" and man["ready"] is True
    assert man["v1_integrity"]["reproduced_by_rebuild"] and man["shortfalls"] == [] and man["status"].startswith("READY")
    assert set(files) == {"MANIFEST.json", "QUARANTINE.json", "VALIDATION_REPORT.json", "attack.json", "documents.json",
                          "lexicon.json", "packs.json", "skins.json", "wordings.json"}
    for w in json.loads(files["wordings.json"])["wordings"]:
        assert w["lexicon_ids"] == [w["form_id"]]
    shas = man["sha256"]
    assert set(shas) == set(files) - {"MANIFEST.json"}
    assert all(hashlib.sha256(files[n].encode()).hexdigest() == h for n, h in shas.items())
    vr = json.loads(files["VALIDATION_REPORT.json"])
    assert vr["files_total"] == 54 and vr["files_valid"] == 53 and vr["file_policy"].startswith("items")


def test_the_generator_renders_rows_from_the_pools_with_g_lex_clean(built):
    pools = FZ.pools_from_files(built["files"])
    ctx = FZ.kit_ctx(pools)
    plug = P.T31(lexicon=pools["lexicon"])
    n = 0
    for seed in range(8):
        for sampler in ("S1", "S2", "S3", "S4"):
            spec = plug.sample(seed, sampler)
            c2 = plug.ctx_for(spec, ctx)
            rr = plug.render(spec, c2)
            assert pipeline.lex_problems(spec, rr, c2) == [], (seed, sampler)
            n += 1
    assert n == 32
    assert all(pools["lexicon"].status(fid) == "admitted" for fid in pools["wording_forms"].values())


def _snapshot():
    return sorted((str(p.relative_to(FZ.HERE)), p.stat().st_size, p.stat().st_mtime_ns)
                  for p in FZ.HERE.rglob("*") if p.is_file())


def test_check_writes_nothing_and_leaves_no_bytecode():
    before = _snapshot()
    out = FZ.run(write=False)
    assert out["written"] is False and out["ready"] is True and out["status"].startswith("READY")
    assert _snapshot() == before                                     # nothing created, nothing changed (no bytecode)


def test_an_excluded_read_leaves_its_forms_pending_and_out_of_the_pool(built, monkeypatch):
    monkeypatch.setattr(FZ, "write_pools_v2", lambda files: pytest.fail("a test must never write pools_v2"))
    a = FZ.assemble(exclude=("T31-extract_lex-50d7ba59-000",))
    rec = next(r for r in a["records"] if r["task_id"] == "T31-extract_lex-50d7ba59-000")
    assert rec["status"] == "excluded"
    assert a["excluded"] == ["T31-extract_lex-50d7ba59-000"]
    pend = set(a["pending"])
    assert pend and pend <= set(a["st"]["new_forms"])                 # one read of two: pending, never used
    w = {x["form_id"] for x in json.loads(a["files"]["wordings.json"])["wordings"]}
    assert not pend & w
    assert a["c"]["wordings_admitted"] < built["c"]["wordings_admitted"]
    assert a["gates"]["G-LEX"]["pending_forms"] == sorted(pend)
    man = json.loads(FZ.build_files(a)["MANIFEST.json"])
    assert any("wait for 2 independent G-LEX reads" in s for s in man["remaining_work"])
    assert man["answer_files"]["excluded_tasks_audit_failed"] == ["T31-extract_lex-50d7ba59-000"]


def test_a_task_id_that_names_no_task_is_reported():
    defs, _unknown = FZ.inventory()
    _valid, _recs, bad = FZ.validate_all(defs, {"T31-no-such-task"}, False)
    assert bad == ["T31-no-such-task"]


def test_the_strict_file_reading_blocks_on_the_v1_file_with_a_mistyped_qid(monkeypatch):
    monkeypatch.setattr(FZ, "write_pools_v2", lambda files: pytest.fail("a test must never write pools_v2"))
    a = FZ.assemble(strict_files=True)
    assert a["early"] and a["ready"] is False
    assert any("T31-author_wording-a7e52c11-000" in b and "invalid" in b for b in a["blockers"])
    imp = a["impact"]
    assert imp["wording_candidates"] < FZ.G0_TARGETS["wordings_pool_candidates"]    # the sensitivity to disclose
    out = FZ._early_out(a)
    assert out["status"].startswith("BLOCKED") and out["policy"] == "strict"
    with pytest.raises(SystemExit):
        FZ.run(write=True, strict_files=True)


@pytest.mark.skipif(not (FZ.POOLS_V2 / "VALIDATION_REPORT.json").is_file(), reason="pools_v2/ not written by freeze_v2")
def test_pools_v2_on_disk_equals_what_the_script_computes_now(built):
    files = FZ.build_files(built)
    on_disk = {p.name for p in FZ.POOLS_V2.iterdir() if p.is_file()}
    assert on_disk == set(files)
    for name, text in files.items():
        assert (FZ.POOLS_V2 / name).read_text(encoding="utf-8") == text, name
    man = json.loads((FZ.POOLS_V2 / "MANIFEST.json").read_text(encoding="utf-8"))
    for name, h in man["sha256"].items():
        assert hashlib.sha256((FZ.POOLS_V2 / name).read_bytes()).hexdigest() == h
    pools = FZ.load_pools()
    assert pools["manifest"]["ready"] is True and len(pools["wordings"]) == built["c"]["wordings_admitted"]
    assert (FZ.ARCHIVE / "MANIFEST.json").is_file()
    assert json.loads((FZ.ARCHIVE / "MANIFEST.json").read_text(encoding="utf-8"))["status"].startswith("PARTIAL")
    assert man["supersedes"]["partial_v2"]["sha256"] == hashlib.sha256((FZ.ARCHIVE / "MANIFEST.json").read_bytes()).hexdigest()
    for name in json.loads((FZ.POOLS_V1 / "MANIFEST.json").read_text(encoding="utf-8"))["sha256"]:
        assert (FZ.POOLS_V1 / name).is_file()                         # v1 is still there, untouched (reproduction test)
    assert os.path.isdir(FZ.POOLS_V1)

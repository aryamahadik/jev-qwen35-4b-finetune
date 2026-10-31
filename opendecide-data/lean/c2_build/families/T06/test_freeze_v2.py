"""families/T06/test_freeze_v2.py: tests of freeze_v2.py (the T06 pool re-freeze over v1 + redo2 + redo3).

Contracts      each answer-file shape (author packs / texts, G-LEX picks, G3-H extractions) accepts a valid file and
               rejects a missing, extra or repeated qid, a wrong key, a wrong type and an off-list meaning
Answer files   all 71 real answer files of the six rounds are valid; a tampered copy is rejected whole (never edited); a
               stray file and an unlisted round are flagged; an audit-failed task is ignored and its reads are absent
Rules          G-LEX reads: 2 for deontic and question forms, 3 for window and precedence forms, a different pick or an
               off-list text rejects for good, an ignored file leaves a form pending; G3-H: the register is the template,
               pooled over both rounds, an unread document is neither admitted nor a mismatch
Redo3          the lint of the redo3 pieces (packs, skins, attack lines, wordings) and its comparison with the record the
               read builder wrote; the two G-LEX reads of the new wordings; the fold is a pure function of the v1 + redo2
               state and the answers; a rebuild that differs from the tasks on disk blocks the freeze
Freeze         verdict READY (every G0 minimum met, G-LEX passes) with the exact pool counts; freeze-v1 byte-identical and
               reproduced from the answers; every v1 row is in v2; the v1 + redo2 state equals pools_v2_prev (when on disk);
               MANIFEST hashes match; the writer never overwrites a different freeze; pools_v2 on disk (when written)
               equals a rebuild
Consumer       load_pools_v2 verifies the MANIFEST; kit_ctx + wired_plugin run through pipeline.build_unit (in memory;
               the only files written are in a scratch folder that is removed at the end)
Run (from lean/): ../.venv/bin/python -m pytest -q -p no:cacheprovider c2_build/families/T06/test_freeze_v2.py
"""
from __future__ import annotations

import copy
import json
import shutil
import sys
from collections import Counter
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2 = HERE.parents[1]
if str(C2) not in sys.path:
    sys.path.insert(0, str(C2))

from c2_kit import chunker, g3h  # noqa: E402
from c2_kit import lexicon as LX  # noqa: E402
from c2_kit import pipeline  # noqa: E402
from families.T06 import freeze_v2 as F  # noqa: E402
from families.T06 import haiku_author as H  # noqa: E402
from families.T06 import plugin as P  # noqa: E402
from families.T06 import pool_freeze as PF  # noqa: E402

SCRATCH = HERE / "_t_scratch_pools_v2"
R2X = ("T06-extract_g3h-945b1095-000", "T06-extract_g3h-945b1095-001", "T06-extract_lex-712abdc8-000",
       "T06-extract_lex-e17088a0-000")                          # the redo2/extract answer files
R3_READS = ("T06-extract_lex-11a053b2-000", "T06-extract_lex-aeed5bce-000")        # the redo3/reads answer files
R3_PACK = "T06-author_pack-03745dc1-000"                        # a redo3 authoring file of 5 packs
R3_WORDING = "T06-author_wording-7606f3cc-000"                  # the redo3 authoring file of the 19 new wordings
R3_SKIN, R3_ATTACK = "T06-author_skin-fb9cd001", "T06-author_skin-708cbdb2"        # task id prefixes: skins / attack lines
R3_WORDING_PREFIX = "T06-author_wording-7606f3cc"

# the 14 shortfalls the freeze made before redo3 left (exact; recounted by hand from the v1 manifest and the redo2 admit):
# {row: (target, got)}. Redo3 closed every one of them.
PREV_SHORT = {
    "packs, all": (44, 38), "packs, held out": (8, 6),
    "skins, register chat": (38, 35), "skins, register email": (38, 37), "skins, register yaml": (38, 37),
    "skins, held-out register transcript": (24, 22),
    "attack lines, all": (60, 58), "attack lines, held out": (12, 10),
    "wordings, training": (106, 102), "wording ch_rule, training": (30, 24), "wording yn_double, training": (8, 7),
    "wording yn_not_refund, training": (10, 9), "wording yn_refund, training": (12, 10),
    "ch_rule wordings (G0 floor 30)": (30, 29)}


@pytest.fixture(scope="module")
def built():
    return F.build()


@pytest.fixture(scope="module")
def scratch():
    shutil.rmtree(SCRATCH, ignore_errors=True)
    yield SCRATCH
    shutil.rmtree(SCRATCH, ignore_errors=True)


def files_of(built, name):
    return json.loads(built["files"][name])


def rows_of(built, name):
    return [json.loads(x) for x in built["files"][name].splitlines() if x.strip()]


# ------------------------------------------------------------------------------------------------ targets
def test_targets_not_lowered():
    assert F.TARGET["packs"] == 44 and F.TARGET["packs_held"] == 8 and F.TARGET["skins_floor"] == 250
    assert F.TARGET["attacks"] == 60 and F.TARGET["attacks_held"] == 12
    assert F.TARGET["documents"] == 240 and F.TARGET["documents_held"] == 40 and F.TARGET["notice_per_sem"] == 6
    assert F.TARGET["wordings_training"] == 106 and F.TARGET["wordings_held"] == 29
    assert F.TARGET["g3h_rate"] == 0.98 == g3h.PASS_RATE
    assert (F.TARGET["glex_deontic"], F.TARGET["glex_question"], F.TARGET["glex_window"],
            F.TARGET["glex_precedence"]) == (2, 2, 3, 3)
    assert F.TARGET["mode_f_cap"] == 0.25
    assert F.FLOOR_2PCT == {"ch_rule": 18, "ch_end_reject": 4, "ch_end_withdraw": 4, "yn_refund": 6, "yn_owed": 6,
                            "yn_double": 6, "yn_not_refund": 6, "yn_may_refuse": 6, "yn_no_right": 6}
    assert H.WORDING_PLAN["ch_rule"] == (30, 5) and H.WORDING_PLAN["ch_end_withdraw"] == (8, 3)


def test_g0_pin():
    assert F.sha_file(F.G0) == F.G0_PIN == P.T06Plugin.G0_SHA256_AUTHORED


# ------------------------------------------------------------------------------------------------ contracts (pure)
def _qids(n=3):
    return [f"q{i:010x}" for i in range(n)]


VALID = {
    "author_pack": lambda q: {"qid": q, "pack": {
        "store": "Brightwell Home",
        "goods": {"standard": ["a", "b", "c", "d", "e"], "custom": ["f", "g", "h"], "perishable": ["i", "j", "k"],
                  "hygiene": ["l", "m", "n"]}, "customers": ["Ann Lee"] * 6, "jurisdiction": "Valdoria"}},
    "author_skin": lambda q: {"qid": q, "text": "Hello {CUSTOMER}"},
    "author_wording": lambda q: {"qid": q, "text": "What is it?"},
    "author_freeform": lambda q: {"qid": q, "text": "Some note"},
    "author_lexicon": lambda q: {"qid": q, "text": "Full refund within {P}."},
    "extract_lex": lambda q: {"qid": q, "meaning": "m1"},
    "extract_g3h": lambda q: {"qid": q, "customer": "Aiko Brandt", "item": "kettle", "store": "NONE"},
}


@pytest.mark.parametrize("kind", sorted(VALID))
def test_valid_answers_pass_and_broken_ones_fail(kind):
    qids = _qids()
    ok = [VALID[kind](q) for q in qids]
    closed = {"m1", "m2"}
    assert F.answer_problems(kind, ok, qids, closed) == []
    assert F.answer_problems(kind, ok[:-1], qids, closed)                              # a qid unanswered
    assert F.answer_problems(kind, ok + [VALID[kind]("q00000000ff")], qids, closed)    # a qid outside the chunk
    assert F.answer_problems(kind, ok + [ok[0]], qids, closed)                         # a qid twice
    assert F.answer_problems(kind, {"qid": 1}, qids, closed)                           # not a list
    assert F.answer_problems(kind, ["x"] * 3, qids, closed)                            # items are objects
    bad = copy.deepcopy(ok)
    bad[0]["unexpected"] = 1                                                           # an extra key
    assert F.answer_problems(kind, bad, qids, closed)
    bad = copy.deepcopy(ok)
    del bad[1]["qid"]                                                                  # no qid
    assert F.answer_problems(kind, bad, qids, closed)
    bad = copy.deepcopy(ok)
    bad[2]["qid"] = "not-a-qid"                                                        # qid of the wrong form
    assert F.answer_problems(kind, bad, qids, closed)


def test_field_types_are_enforced():
    qids = _qids(1)
    q = qids[0]
    t = VALID["author_wording"](q)
    for bad in ("", "   ", 5, None, ["x"]):
        assert F.answer_problems("author_wording", [dict(t, text=bad)], qids), bad
    g = VALID["extract_g3h"](q)
    for k in ("customer", "item", "store"):
        for bad in ("", None, 7):
            assert F.answer_problems("extract_g3h", [dict(g, **{k: bad})], qids), (k, bad)
    a = VALID["author_pack"](q)
    for mut in (lambda p: p.pop("store"), lambda p: p.update(extra=1), lambda p: p.update(store=""),
                lambda p: p.update(jurisdiction=3), lambda p: p.update(customers="Ann Lee"),
                lambda p: p.update(customers=[1, 2]), lambda p: p["goods"].pop("custom"),
                lambda p: p["goods"].update(standard="x"), lambda p: p["goods"].update(hygiene=[1]),
                lambda p: p.update(goods=[])):
        b = copy.deepcopy(a)
        mut(b["pack"])
        assert F.answer_problems("author_pack", [b], qids), mut
    b = copy.deepcopy(a)
    b["pack"] = "a store"
    assert F.answer_problems("author_pack", [b], qids)
    assert F.answer_problems("poll", [], qids)                                         # no contract for a kind


def test_pack_counts_and_name_shapes_are_item_checks_not_file_contracts():
    """A pack with 4 standard items is a valid file entry (the file keeps its other packs); validate_pack drops it."""
    qids = _qids(1)
    a = VALID["author_pack"](qids[0])
    a["pack"]["goods"]["standard"] = ["a", "b", "c", "d"]
    assert F.answer_problems("author_pack", [a], qids) == []
    assert H.validate_pack(a["pack"])


def test_lex_answers_are_closed_list_picks():
    qids = _qids()
    closed = {"m1", "m2", "m3"}
    ok = [{"qid": q, "meaning": "m1"} for q in qids]
    assert F.answer_problems("extract_lex", ok, qids, closed) == []
    assert F.answer_problems("extract_lex", [dict(ok[0], meaning="m4")] + ok[1:], qids, closed)    # off the printed list
    assert F.answer_problems("extract_lex", [dict(ok[0], meaning=3)] + ok[1:], qids, closed)       # not text
    assert F.answer_problems("extract_lex", ok[:2], qids, closed)                                    # unanswered
    assert F.answer_problems("extract_lex", {q: "m1" for q in qids}, qids, closed)                   # an object, not a list


def test_closed_list_is_read_from_the_list_block_not_the_instructions():
    md = ("Pick the ONE MEANING from the CLOSED LIST that the text expresses.\n\nCLOSED LIST (one per line):\n- a b\n"
          "- c d\n\nITEMS (JSON):\n- not a meaning\n")
    assert F.closed_list(md) == ["a b", "c d"]
    with pytest.raises(ValueError):
        F.closed_list("no list here")
    real = (HERE / "haiku" / "extract" / "tasks" / "T06-extract_lex-e11823f5-000.md").read_text(encoding="utf-8")
    cl = F.closed_list(real)
    assert len(cl) == 4 and all(m for m in cl) and "the store promises a full refund on some returns" in cl


# ------------------------------------------------------------------------------------------------ the real answer files
def test_all_real_answer_files_are_valid():
    val = F.validate_answers()
    assert F.ROUNDS == ("author", "extract", "redo2", "redo2/extract", "redo3", "redo3/reads")
    assert val["by_round"] == {"author": {"files": 37, "valid": 37, "usable": 37},
                               "extract": {"files": 20, "valid": 20, "usable": 20},
                               "redo2": {"files": 3, "valid": 3, "usable": 3},
                               "redo2/extract": {"files": 4, "valid": 4, "usable": 4},
                               "redo3": {"files": 5, "valid": 5, "usable": 5},
                               "redo3/reads": {"files": 2, "valid": 2, "usable": 2}}
    assert val["invalid"] == [] and val["stray"] == [] and val["ignored"] == [] and val["unlisted_rounds"] == []
    assert len(val["usable"]) == 71
    assert all(f["sha256"] and f["problems"] == [] for f in val["files"])
    assert val["ambiguity"]["valid"] and val["ambiguity"]["problems"] == []
    kinds = Counter(f["kind"] for f in val["files"])
    assert kinds == {"author_pack": 10, "author_skin": 15, "author_freeform": 10, "author_wording": 6,
                     "author_lexicon": 4, "extract_lex": 18, "extract_g3h": 8}
    r3 = {f["task_id"]: f for f in val["files"] if f["round"] in ("redo3", "redo3/reads")}
    assert set(r3) == {R3_PACK, "T06-author_pack-03745dc1-001", R3_WORDING, *R3_READS} | {
        f["task_id"] for f in val["files"] if f["task_id"].startswith((R3_SKIN, R3_ATTACK))}
    assert r3[R3_READS[0]]["answer_file"] == f"redo3/reads/answers/{R3_READS[0]}.json"
    assert r3[R3_READS[0]]["lexicon_kind"] == "question" and r3[R3_PACK]["answer_file"] == f"redo3/answers/{R3_PACK}.json"


def test_a_tampered_copy_is_rejected_whole_and_never_edited(tmp_path):
    root = tmp_path / "haiku"
    shutil.copytree(HERE / "haiku", root, ignore=shutil.ignore_patterns("__pycache__", "*.py", "*.pyc"))
    ans = sorted((root / "redo2" / "answers").glob("T06-*.json"))
    tampered, kept = ans[0], ans[1]
    items = json.loads(tampered.read_text())
    tampered.write_text(json.dumps(items[:-1]))                                        # one item missing
    before = tampered.read_bytes()
    (root / "redo2" / "answers" / "notes.txt").write_text("stray")
    (root / "redo4" / "answers").mkdir(parents=True)                                   # a round nobody listed
    val = F.validate_answers(haiku_root=root)
    by = {f["task_id"]: f for f in val["files"]}
    assert not by[tampered.stem]["valid"] and "unanswered" in " ".join(by[tampered.stem]["problems"])
    assert by[kept.stem]["usable"] and tampered.stem not in val["usable"]
    assert val["invalid"] == [tampered.stem]
    assert [s["answer_file"] for s in val["stray"]] == ["redo2/answers/notes.txt"]
    assert val["unlisted_rounds"] == ["redo4/answers"]
    assert tampered.read_bytes() == before                                             # never edited
    tampered.write_text("not json")
    assert F.validate_answers(haiku_root=root)["invalid"] == [tampered.stem]
    tampered.write_bytes(b"\xff\xfe\x00")                                              # not even UTF-8
    assert F.validate_answers(haiku_root=root)["invalid"] == [tampered.stem]
    tampered.unlink()                                                                  # missing file
    assert F.validate_answers(haiku_root=root)["invalid"] == [tampered.stem]


def test_a_changed_chunk_or_prompt_invalidates_its_task(tmp_path):
    root = tmp_path / "haiku"
    shutil.copytree(HERE / "haiku", root, ignore=shutil.ignore_patterns("__pycache__", "*.py", "*.pyc"))
    tid = "T06-extract_lex-712abdc8-000"
    chunk = root / "redo2" / "extract" / "chunks" / f"{tid}.json"
    c = json.loads(chunk.read_text())
    c["items"][0]["text"] += " (changed)"
    chunk.write_text(json.dumps(c, indent=1) + "\n")
    val = F.validate_answers(haiku_root=root)
    f = next(x for x in val["files"] if x["task_id"] == tid)
    assert not f["valid"] and "chunk differs from its manifest hash" in f["problems"]


def test_an_off_list_meaning_invalidates_the_whole_lex_file(tmp_path):
    root = tmp_path / "haiku"
    shutil.copytree(HERE / "haiku", root, ignore=shutil.ignore_patterns("__pycache__", "*.py", "*.pyc"))
    tid = "T06-extract_lex-712abdc8-000"
    af = root / "redo2" / "extract" / "answers" / f"{tid}.json"
    a = json.loads(af.read_text())
    a[0]["meaning"] = "something else entirely"
    af.write_text(json.dumps(a))
    val = F.validate_answers(haiku_root=root)
    f = next(x for x in val["files"] if x["task_id"] == tid)
    assert not f["valid"] and any("closed list" in x for x in f["problems"]) and tid not in val["usable"]


def test_the_ambiguity_record_is_checked_against_its_own_contract(tmp_path):
    src = HERE / "haiku" / "ambiguity" / "amb_T06_points.json"
    assert F.ambiguity_problems(src) == []
    o = json.loads(src.read_text())
    bad = tmp_path / "amb.json"
    bad.write_text(json.dumps(dict(o, points=o["points"][:-1])))
    assert F.ambiguity_problems(bad)                                                  # 51 points, wrong count and hash
    pts = [dict(p) for p in o["points"]]
    pts[0]["extra"] = 1
    bad.write_text(json.dumps(dict(o, points=pts)))
    assert F.ambiguity_problems(bad)
    bad.write_text("{")
    assert F.ambiguity_problems(bad)


def test_an_audit_failed_task_is_ignored_not_edited():
    tid = R2X[0]
    before = F.sha_file(HERE / "haiku" / "redo2" / "extract" / "answers" / f"{tid}.json")
    val = F.validate_answers(ignore=frozenset({tid}))
    f = next(x for x in val["files"] if x["task_id"] == tid)
    assert f["valid"] and f["ignored"] and not f["usable"]
    assert tid not in val["usable"] and val["ignored"] == [tid]
    assert F.sha_file(HERE / "haiku" / "redo2" / "extract" / "answers" / f"{tid}.json") == before


def test_a_rejected_author_file_blocks_the_freeze():
    tid = "T06-author_pack-8ffd081a-000"
    res = F.build(frozenset({tid}), sensitivity=False)
    assert res["blocked"] and res["verdict"] == "SHORT" and res["files"] == {}
    assert "author answer file" in res["summary"]["issues"][0]
    with pytest.raises(SystemExit):
        F.write_pools(res, SCRATCH)
    with pytest.raises(SystemExit):
        F.build(frozenset({"T06-no-such-task-000"}), sensitivity=False)


def test_an_ignored_redo3_wording_file_blocks_the_freeze_but_a_redo3_pack_file_only_leaves_a_shortfall():
    """The redo3 read tasks were built from the 19 wordings, so their authoring file is an AUTHOR file (it blocks); the
    packs, skins and attack lines have no read, so an ignored file just leaves its pieces out and the verdict says why."""
    res = F.build(frozenset({R3_WORDING}), sensitivity=False)
    assert res["blocked"] and res["verdict"] == "SHORT" and res["files"] == {}
    assert "author answer file" in res["summary"]["issues"][0] and R3_WORDING in res["summary"]["issues"][0]
    res = F.build(frozenset({R3_PACK}), sensitivity=False)
    s = res["summary"]
    assert not res["blocked"] and res["verdict"] == "SHORT" and s["issues"] == []
    assert [(r["item"], r["target"], r["got"]) for r in s["shortfalls"]] == [("packs, all", 44, 43)]
    assert s["counts"]["added_by_redo3"]["packs"] == 5 and s["counts"]["added_by_redo3"]["wordings"] == 19
    man = json.loads(res["files"]["MANIFEST.json"])
    assert any("5 item(s) unanswered" in x for x in man["answer_problems"])
    assert man["binding"]["audit_failed_ignored"] == [R3_PACK]


# ------------------------------------------------------------------------------------------------ G-LEX (kit rules)
def _reg(kind="question", n=1):
    reg = LX.LexiconRegistry("T99")
    sems = {"question": ("q.t99.a", "asks a"), "window": ("win.t99.a", "a window"), "deontic": ("pol.t99.a", "a ban")}
    sem, meaning = sems[kind]
    reg.declare(sem, kind, meaning)
    reg.declare("other.t99.b", kind, "something else")
    texts = {"question": "Is refund {} done?", "deontic": "No refunds are given, kind {}",
             "window": "A full refund within {{N}} of kind {}"}
    for i in range(n):
        reg.add(texts[kind].format(chr(97 + i)) if kind != "window" else f"A full refund within {{N}} of kind {chr(97 + i)}",
                sem, slots={"N": "count"} if kind == "window" else {}, family="T99", source="haiku",
                haiku_task_id="t", haiku_prompt_sha="p")
    assert all(reg.unit_test_all().values()), [f.unit_problems for f in reg.forms.values()]
    return reg, sem, meaning


def _fake_batch(tmp_path, reg, label, reads):
    """A real chunker batch over the registry's forms with answer files written by the test (reads: {fid: meaning})."""
    items = [(fid, {"text": f"filled text number {i}"}) for i, fid in enumerate(sorted(reg.forms))]
    b = chunker.make_batch("extract_lex", "T99", items, seed=f"seed-{label}", prompt="pick one", max_items=50)
    qid_of = {i: q for q, i in b.key.items()}
    tid = b.chunks[0]["task_id"]
    ans = tmp_path / "answers"
    ans.mkdir(exist_ok=True)
    (ans / f"{tid}.json").write_text(json.dumps([{"qid": qid_of[f], "meaning": m} for f, m in reads.items()]))
    return (label, "question", 0, b), tid


def test_glex_deontic_and_question_need_two_matching_reads_window_needs_three(tmp_path):
    for kind, need in (("question", 2), ("deontic", 2), ("window", 3)):
        reg, sem, meaning = _reg(kind)
        fid = next(iter(reg.forms))
        assert reg.forms[fid].required == need
        for k in range(need):
            batch, tid = _fake_batch(tmp_path, reg, f"r{k}-{kind}", {fid: meaning})
            log, probs = F.record_glex([batch], reg, tmp_path, {tid}, "haiku-", "t")
            assert probs == [] and log[0]["agrees"]
            assert reg.status(fid) == ("admitted" if k + 1 == need else "pending")
        assert F.glex_audit(reg)["violations"] == []


def test_glex_a_window_form_with_two_reads_is_pending_and_flagged(tmp_path):
    reg, sem, meaning = _reg("window")
    fid = next(iter(reg.forms))
    for k in range(2):
        batch, tid = _fake_batch(tmp_path, reg, f"w{k}", {fid: meaning})
        F.record_glex([batch], reg, tmp_path, {tid}, "haiku-", "t")
    assert reg.status(fid) == "pending"
    audit = F.glex_audit(reg)
    assert audit["gate"]["pass"] is False and any("2 of 3 reads" in v for v in audit["violations"])


def test_glex_a_different_pick_or_an_off_list_text_rejects_for_good(tmp_path):
    for pick in ("something else", "a text that is on no list"):
        reg, sem, meaning = _reg("question")
        fid = next(iter(reg.forms))
        b1, t1 = _fake_batch(tmp_path, reg, "a1", {fid: meaning})
        F.record_glex([b1], reg, tmp_path, {t1}, "haiku-", "t")
        b2, t2 = _fake_batch(tmp_path, reg, "a2", {fid: pick})
        log, _ = F.record_glex([b2], reg, tmp_path, {t2}, "haiku-", "t")
        assert not log[0]["agrees"] and reg.status(fid) == "rejected" and not F.glex_audit(reg)["gate"]["pass"]


def test_glex_an_unusable_file_leaves_the_form_unread_and_a_repeat_read_raises(tmp_path):
    reg, sem, meaning = _reg("question")
    fid = next(iter(reg.forms))
    batch, tid = _fake_batch(tmp_path, reg, "u1", {fid: meaning})
    log, probs = F.record_glex([batch], reg, tmp_path, set(), "haiku-", "t")          # the file is not usable
    assert log == [] and probs and reg.forms[fid].extractions == [] and reg.status(fid) == "pending"
    F.record_glex([batch], reg, tmp_path, {tid}, "haiku-", "t")
    with pytest.raises(LX.LexiconError):
        F.record_glex([batch], reg, tmp_path, {tid}, "haiku-", "t")                  # no re-vote by one extractor


def test_strict_kinds_need_three_reads_in_the_kit():
    reg = LX.LexiconRegistry("T99")
    reg.declare("prec.P1", "precedence", "deny beats allow")
    f = reg.add("deny rules beat allow rules", "prec.P1")
    reg.unit_test_all()
    assert f.required == 3
    for k, e in enumerate("abc"):
        reg.record_extraction(f.form_id, e, "prec.P1")
        assert reg.status(f.form_id) == ("admitted" if k == 2 else "pending")


# ------------------------------------------------------------------------------------------------ G3-H (kit rules)
def _votes(spec):
    """spec: {register: (answered_ok, answered_bad, unread)} -> votes in the freeze_v2 shape."""
    out = []
    for reg, (ok, bad, unread) in spec.items():
        for i in range(ok):
            out.append({"register": reg, "item": f"{reg}.ok.{i}", "answered": True, "ok": True})
        for i in range(bad):
            out.append({"register": reg, "item": f"{reg}.bad.{i}", "answered": True, "ok": False})
        for i in range(unread):
            out.append({"register": reg, "item": f"{reg}.unread.{i}", "answered": False, "ok": False})
    return out


def test_g3h_register_is_the_template_pooled_over_rounds():
    rep = F.g3h_pooled(_votes({"email": (52, 1, 0)}))                                  # v1 44/44 + redo2 8/9
    assert rep["templates"]["email"]["rate"] == pytest.approx(52 / 53) and not rep["quarantined"]
    assert rep["drop_rows"] == ["email.bad.0"]                                          # the mismatch is always dropped
    alone = F.g3h_pooled(_votes({"email": (8, 1, 0)}))                                  # the redo2 batch judged alone
    assert alone["quarantined"] == ["email"] and len(alone["drop_rows"]) == 9
    two = F.g3h_pooled(_votes({"email": (49, 1, 0)}))                                   # exactly 98% passes
    assert not two["quarantined"]
    assert F.g3h_pooled(_votes({"email": (48, 2, 0)}))["quarantined"] == ["email"]


def test_g3h_an_unread_document_is_neither_a_mismatch_nor_admitted():
    rep = F.g3h_pooled(_votes({"chat": (10, 0, 5)}))
    assert rep["templates"]["chat"]["n"] == 10 and rep["drop_rows"] == [] and not rep["quarantined"]


def test_g3h_votes_compare_against_the_generators_facts(tmp_path):
    a, b_ = "t99.doc.alpha", "t99.doc.beta"
    items = [(a, g3h.extraction_item("Ann Lee: I bought the kettle at Brightwell Home", list(F.E.G3H_FIELDS))),
             (b_, g3h.extraction_item("another text", list(F.E.G3H_FIELDS)))]
    b = chunker.make_batch("extract_g3h", "T99", items, seed="g", prompt="read", max_items=34)
    qid_of = {i: q for q, i in b.key.items()}
    tid = b.chunks[0]["task_id"]
    (tmp_path / "answers").mkdir()
    full = {"customer": "Ann Lee", "item": "kettle", "store": "Brightwell Home"}
    (tmp_path / "answers" / f"{tid}.json").write_text(json.dumps([
        dict(qid=qid_of[a], **full), dict(qid=qid_of[b_], customer="Ann Lee", item="kettle", store="NONE")]))
    exp = {a: dict(full), b_: dict(full)}
    votes, probs = F.g3h_votes(b, exp, {a: "chat", b_: "email"}, tmp_path, {tid}, "haiku-g3h-r1", "t")
    assert probs == [] and [(v["item"], v["ok"], v["answered"]) for v in votes] == [(a, True, True), (b_, False, True)]
    assert "store" in votes[1]["diffs"][0]
    votes, probs = F.g3h_votes(b, exp, {a: "chat", b_: "email"}, tmp_path, set(), "haiku-g3h-r1", "t")
    assert probs and not any(v["answered"] for v in votes) and all(v["diffs"] == ["unread"] for v in votes)


# ------------------------------------------------------------------------------------------------ redo3
def strip_redo3(pools: dict) -> tuple:
    """(pools, lexicon JSON) of the v1 + redo2 state: the final pools without the redo3 rows and forms."""
    out = dict(pools)
    out["packs"] = [x for x in pools["packs"] if not x["pid"].startswith("t06r3.")]
    out["skins"] = [x for x in pools["skins"] if not x["pid"].startswith("t06r3.")]
    out["attacks"] = [x for x in pools["attacks"] if not x["pid"].startswith("t06r3.")]
    out["wordings"] = [w for w in pools["wordings"] if not w["haiku_task_id"].startswith(R3_WORDING_PREFIX)]
    lex = json.loads(json.dumps(pools["lexicon"]))
    lex["forms"] = [f for f in lex["forms"] if not f["haiku_task_id"].startswith(R3_WORDING_PREFIX)]
    lex["note"] = F.LEXICON_NOTE_PREV
    return out, lex


@pytest.fixture(scope="module")
def prev_state(pools):
    return strip_redo3(pools)


@pytest.fixture(scope="module")
def usable():
    return set(F.validate_answers()["usable"])


@pytest.fixture(scope="module")
def folded(prev_state, usable):
    return F.fold_redo3(prev_state[0], prev_state[1], usable, F.base_pools_dir())


def test_stripping_redo3_gives_the_v1_plus_redo2_state(prev_state):
    p, lex = prev_state
    assert (len(p["packs"]), len(p["skins"]), len(p["attacks"]), len(p["wordings"]), len(lex["forms"])) == (
        38, 345, 58, 134, 222)
    base = F.base_pools_dir()
    if base is None:
        pytest.skip("no pre-redo3 freeze on disk")
    disk = F.load_pools_v2(base, require_ready=False)
    for k in ("packs", "skins", "attacks", "wordings", "lexicon"):
        assert disk[k] == (lex if k == "lexicon" else p[k]), k


def test_fold_is_a_pure_function_of_the_earlier_state_and_the_answers(folded, pools):
    r = folded
    assert r["blocked"] is None and r["issues"] == [] and r["problems"] == []
    for k in ("packs", "skins", "attacks", "wordings"):
        assert r["pools"][k] == pools[k], k
    assert json.loads(F.jtext(F.lexicon_json(r["reg"], F.LEXICON_NOTE))) == pools["lexicon"]
    assert len(r["glex_log"]) == 38 and all(e["agrees"] for e in r["glex_log"])
    assert {e["extractor"] for e in r["glex_log"]} == {"haiku-r3-glex-r1", "haiku-r3-glex-r2"}
    assert [x["item"] for x in r["quarantine"]] == ["t06r3.attack.r3-002"]
    rep = r["report"]
    assert rep["checks"]["read_tasks_equal_rebuild"] and rep["checks"]["lint_equals_recorded_LINT_json"]
    assert rep["wordings"]["status"] == {"admitted": 19} and rep["reads"] == {
        "recorded": 38, "agreeing": 38, "extractors": ["haiku-r3-glex-r1", "haiku-r3-glex-r2"]}
    assert rep["kept_after_lint"] == {"packs": 10, "skins": 15, "attacks": 3, "wordings": 19}
    assert rep["dropped_by_lint"] == {"packs": 0, "skins": 0, "attacks": 1, "wordings": 0}
    assert rep["items_answered_by_task"][R3_WORDING] == 19 and len(rep["items_answered_by_task"]) == 5


def test_redo3_answers_are_cut_into_pieces_by_their_plan(usable):
    r3 = F.redo3_authoring(usable)
    assert r3["problems"] == [] and len(r3["answers"]) == 48
    roles = Counter(m["role"] for m in r3["plan"].values())
    assert roles == {"pack": 10, "skin": 15, "attack": 4, "wording": 19}
    assert sum(1 for i, m in r3["plan"].items() if m["role"] == "pack" and m["held_out"]) == 4
    assert all(m["held_out"] for m in r3["plan"].values() if m["role"] == "attack")
    assert {m["register"] for m in r3["plan"].values() if m["role"] == "skin"} == {"chat", "email", "yaml", "transcript"}
    assert all(i.startswith("t06r3.") for i in r3["answers"])
    assert all(r3["task_of"][i] and r3["prompt_sha"][i] for i in r3["answers"])
    some = sorted(r3["answers"])[0]
    assert some not in {q for b in r3["batches"].values() for q in b.key}                 # internal ids are not qids
    # a task whose file is not usable leaves its items out and says so
    less = F.redo3_authoring(usable - {R3_WORDING})
    assert len(less["answers"]) == 29 and any("unanswered" in x or "not usable" in x for x in less["problems"])


def test_redo3_lint_keeps_exactly_what_the_freeze_pooled(prev_state, pools, usable):
    lint = F.redo3_lint(prev_state[0], F.redo3_authoring(usable), F.prior_author_texts())
    assert {k: len(v["kept"]) for k, v in lint.items()} == {"packs": 10, "skins": 15, "attacks": 3, "wordings": 19}
    assert [d["reasons"] for d in lint["attacks"]["drops"]] == [["fact word (seal / packaging): tag"]]
    assert not lint["packs"]["drops"] and not lint["skins"]["drops"] and not lint["wordings"]["drops"]
    for name in ("packs", "skins", "attacks"):
        assert [x["item"] for x in lint[name]["kept"]] == [r["pid"] for r in pools[name] if r["pid"].startswith("t06r3.")]
    for x in lint["skins"]["kept"] + lint["attacks"]["kept"]:
        assert x["obj"].text == x["text"] and x["obj"].haiku_task_id == x["task_id"]
    rec = json.loads((F.REDO3_READS / "LINT.json").read_text(encoding="utf-8"))
    for name in lint:                                                                         # the read builder's record
        assert [x["item"] for x in lint[name]["kept"]] == [x["item"] for x in rec["lint"][name]["kept"]]


def test_redo3_lint_drops_pieces_the_pools_already_hold(pools, usable):
    """Idempotence: linted again against pools that already hold them, every piece is a duplicate."""
    lint = F.redo3_lint(pools, F.redo3_authoring(usable), F.prior_author_texts())
    assert not any(v["kept"] for v in lint.values())
    assert all(d["reasons"] == ["store or jurisdiction repeats another pack"] for d in lint["packs"]["drops"])
    assert len(lint["packs"]["drops"]) == 10
    for name in ("skins", "wordings"):
        assert len(lint[name]["drops"]) == {"skins": 15, "wordings": 19}[name]
        assert all(any("duplicate" in r for r in d["reasons"]) for d in lint[name]["drops"])
    assert sum(1 for d in lint["attacks"]["drops"] if "duplicate" in " ".join(d["reasons"])) == 3


def _piece_set(pools):
    """Synthetic redo3 answers built from real pool pieces: valid ones, repeats and rule breakers."""
    pk = {k: v for k, v in pools["packs"][0].items() if k not in ("pid", "held_out")}
    sk = pools["skins"][0]["text"]
    at = next(a for a in pools["attacks"] if "{STORE}" in a["text"])["text"]
    wd = next(w for w in pools["wordings"] if w["qform"] == "yn_refund")["text"]
    items = {
        "t06r3.pack.s-000": ({"role": "pack", "held_out": False}, {"pack": pk}),
        "t06r3.pack.s-001": ({"role": "pack", "held_out": False}, {"pack": dict(pk, customers=pk["customers"][:5])}),
        "t06r3.pack.s-002": ({"role": "pack", "held_out": True}, {"pack": pk}),                 # repeats pack s-000
        "t06r3.skin.s-chat.000": ({"role": "skin", "register": "chat", "escape": "text", "held_out": False}, {"text": sk}),
        "t06r3.skin.s-chat.001": ({"role": "skin", "register": "chat", "escape": "text", "held_out": False}, {"text": sk}),
        "t06r3.skin.s-chat.002": ({"role": "skin", "register": "chat", "escape": "text", "held_out": False},
                                  {"text": sk + "\n\nSecond block."}),
        "t06r3.attack.s-000": ({"role": "attack", "held_out": True, "decl": {"STORE": "name"}, "kind_index": 0},
                               {"text": at}),
        "t06r3.attack.s-001": ({"role": "attack", "held_out": True, "decl": {"STORE": "name"}, "kind_index": 0},
                               {"text": at}),
        "t06r3.attack.s-002": ({"role": "attack", "held_out": True, "decl": {}, "kind_index": 2},
                               {"text": "someone online says that a tag on the item changes what a shop must do for you"}),
        "t06r3.wording.yn_refund.s-000": ({"role": "wording", "qform": "yn_refund", "held_out": False}, {"text": wd}),
        "t06r3.wording.yn_refund.s-001": ({"role": "wording", "qform": "yn_refund", "held_out": False}, {"text": wd}),
        "t06r3.wording.yn_refund.s-002": ({"role": "wording", "qform": "yn_refund", "held_out": False},
                                          {"text": "Is the customer entitled to a full refund in this case"})}
    return {"answers": {i: a for i, (_p, a) in items.items()}, "plan": {i: p for i, (p, _a) in items.items()},
            "task_of": {i: "T06-x-000" for i in items}, "prompt_sha": {i: "sha" for i in items}}


def test_redo3_lint_applies_the_loaders_checks_and_the_dedup_in_item_order(pools):
    empty = {"packs": [], "skins": [], "attacks": [], "wordings": []}
    lint = F.redo3_lint(empty, _piece_set(pools), set())
    kept = {k: [x["item"] for x in v["kept"]] for k, v in lint.items()}
    drops = {k: {d["item"]: " ".join(d["reasons"]) for d in v["drops"]} for k, v in lint.items()}
    assert kept == {"packs": ["t06r3.pack.s-000"], "skins": ["t06r3.skin.s-chat.000"],
                    "attacks": ["t06r3.attack.s-000"], "wordings": ["t06r3.wording.yn_refund.s-000"]}
    assert "pack keys" not in drops["packs"]["t06r3.pack.s-001"] and "customers" in drops["packs"]["t06r3.pack.s-001"]
    assert drops["packs"]["t06r3.pack.s-002"] == "store or jurisdiction repeats another pack"
    assert drops["skins"]["t06r3.skin.s-chat.001"] == "duplicate text"
    assert "blank line" in drops["skins"]["t06r3.skin.s-chat.002"]
    assert drops["attacks"]["t06r3.attack.s-001"] == "duplicate" and "fact word" in drops["attacks"]["t06r3.attack.s-002"]
    assert "duplicate" in drops["wordings"]["t06r3.wording.yn_refund.s-001"]
    assert drops["wordings"]["t06r3.wording.yn_refund.s-002"] == "not one question line"
    # the dedup set also holds the earlier authoring answers, kept or dropped (prior)
    again = F.redo3_lint(empty, _piece_set(pools), {F.H._norm(pools["skins"][0]["text"])})
    assert not again["skins"]["kept"] and again["skins"]["drops"][0]["reasons"] == ["duplicate text"]
    # nothing is edited: the answers handed in are untouched
    assert _piece_set(pools)["answers"] == _piece_set(pools)["answers"]


def test_prior_author_texts_cover_the_v1_and_redo2_answers_dropped_or_not():
    prior = F.prior_author_texts()
    assert len(prior) > 800
    kept = {F.H._norm(r["text"]) for r in F.read_jsonl(F.POOLS_V1 / "skins.jsonl")}
    assert kept <= prior


def _mk(items, tid):
    return [{"item": i, "task_id": tid, "text": "text " + i} for i in items]


def test_lint_vs_recorded_names_each_difference_and_filters_by_usable_files():
    def lint_of(a, b):
        return {"packs": {"kept": _mk(a, "A"), "drops": []}, "skins": {"kept": _mk(b, "B"), "drops": []},
                "attacks": {"kept": [], "drops": [dict(_mk(["x"], "B")[0], reasons=["r"])]},
                "wordings": {"kept": [], "drops": []}}
    new = {}
    rec = {"lint": lint_of(["a1", "a2"], ["b1"]), "new_wording_forms": []}
    assert F.lint_vs_recorded(lint_of(["a1", "a2"], ["b1"]), new, rec) == []
    assert F.lint_vs_recorded(lint_of(["a1"], ["b1"]), new, rec) == ["packs: kept items differ"]
    assert F.lint_vs_recorded(lint_of(["a1", "a2"], ["b2"]), new, rec) == ["skins: kept items differ",
                                                                           "skins: kept texts differ"]
    other = lint_of(["a1", "a2"], ["b1"])
    other["attacks"]["drops"][0]["reasons"] = ["another reason"]
    assert F.lint_vs_recorded(other, new, rec) == ["attacks: dropped items or their reasons differ"]
    # the file of task A is ignored: its recorded packs are not expected, the others still are
    assert F.lint_vs_recorded(lint_of([], ["b1"]), new, rec, usable={"B"}) == []
    assert F.lint_vs_recorded(lint_of(["a1", "a2"], ["b1"]), new, rec, usable={"B"})            # a1, a2 should be absent
    forms = {"q.t06.x#1": ("t06r3.wording.x.000", "ch_rule", "Which rule?", False, "A", "sha")}
    rec2 = dict(rec, new_wording_forms=[{"form_id": "q.t06.x#1", "item": "t06r3.wording.x.000", "qform": "ch_rule",
                                         "text": "Which rule?", "held_out": False, "haiku_task_id": "A",
                                         "haiku_prompt_sha": "sha"}])
    assert F.lint_vs_recorded(lint_of(["a1", "a2"], ["b1"]), forms, rec2) == []
    assert F.lint_vs_recorded(lint_of(["a1", "a2"], ["b1"]), {}, rec2) == ["new wording forms differ"]
    assert F.lint_vs_recorded(lint_of([], ["b1"]), {}, rec2, usable={"B"}) == []


def test_redo3_read_batches_are_two_independent_reads_equal_to_the_files_on_disk(folded):
    reg, new = folded["reg"], folded["new"]
    assert len(new) == 19
    batches = F.redo3_read_batches(reg, sorted(new))
    assert [b[0] for b in batches] == ["glex-r1", "glex-r2"] and all(b[1] == "question" for b in batches)
    b1, b2 = batches[0][3], batches[1][3]
    assert len(b1.key) == len(b2.key) == 19 and sorted(b1.key.values()) == sorted(b2.key.values()) == sorted(new)
    assert not set(b1.key) & set(b2.key)                                                       # own opaque qids
    assert b1.seed != b2.seed and b1.prompt != b2.prompt and b1.batch_id != b2.batch_id         # own seed, own list order
    meanings = lambda b: [ln[2:] for ln in b.prompt.split("CLOSED LIST (")[-1].splitlines()  # noqa: E731
                          if ln.startswith("- ")]
    assert sorted(meanings(b1)) == sorted(meanings(b2)) and meanings(b1) != meanings(b2)
    assert any("the store's own notice or promise ends" in m for m in meanings(b1))                    # decoys listed
    assert any("any money back, store credit or an exchange" in m for m in meanings(b1)) and len(meanings(b1)) == 11
    for _l, _k, _g, b in batches:
        assert F.files_differ(F.REDO3_READS, b.files()) == []
    with pytest.raises(SystemExit):
        F.redo3_read_batches(reg, [f"x{i}" for i in range(51)])
    assert F.redo3_read_batches(reg, []) == []


def test_fold_blocks_when_the_read_tasks_differ_from_a_rebuild(prev_state, usable, monkeypatch):
    monkeypatch.setattr(F.build_reads_mod(), "task_text", lambda *a, **k: "a different task text")
    r = F.fold_redo3(prev_state[0], prev_state[1], usable, F.base_pools_dir())
    assert r["blocked"] and "redo3 read tasks differ from a rebuild" in r["blocked"][0] and "pools" not in r


def test_fold_blocks_when_the_authoring_tasks_differ_from_a_rebuild_from_the_previous_freeze(prev_state, usable,
                                                                                         monkeypatch):
    if F.base_pools_dir() is None:
        pytest.skip("no pre-redo3 freeze on disk")
    monkeypatch.setattr(F.build_redo3_mod(), "check_author", lambda *a, **k: ["a taken text holds a label word"])
    r = F.fold_redo3(prev_state[0], prev_state[1], usable, F.base_pools_dir())
    assert r["blocked"] and "authoring tasks differ" in r["blocked"][0]


def test_fold_blocks_when_the_lint_differs_from_the_recorded_one(prev_state, usable, monkeypatch):
    monkeypatch.setattr(F, "lint_vs_recorded", lambda *a, **k: ["packs: kept items differ"])
    r = F.fold_redo3(prev_state[0], prev_state[1], usable, F.base_pools_dir())
    assert r["blocked"] and "differs from the one build_reads recorded" in r["blocked"][0]


def test_fold_without_a_previous_freeze_skips_only_the_authoring_rebuild(prev_state, usable):
    r = F.fold_redo3(prev_state[0], prev_state[1], usable, None)
    assert r["blocked"] is None and r["report"]["checks"]["authoring_tasks_equal_rebuild_from_previous_freeze"] is None
    assert r["report"]["checks"]["previous_freeze_dir"] is None and len(r["pools"]["wordings"]) == 153


def test_a_form_without_two_reads_stays_pending_and_out_of_the_pools(prev_state, usable):
    """The two redo3/reads files ignored: the 19 wordings have 0 of 2 reads, are pending, are issued and are not pooled."""
    r = F.fold_redo3(prev_state[0], prev_state[1], usable - set(R3_READS), F.base_pools_dir())
    assert r["blocked"] is None and len(r["issues"]) == 1 and "19 redo3 wording(s) still pending" in r["issues"][0]
    assert len(r["pools"]["wordings"]) == 134 and len(r["pools"]["packs"]) == 48
    assert r["report"]["wordings"]["status"] == {"pending": 19} and r["glex_log"] == []
    assert len(r["reg"].forms) == 222 and r["report"]["wordings"]["admitted_by_qform"] == {}
    assert len(r["quarantine"]) == 1 + 19                                                     # attack drop + 19 pending forms
    half = F.fold_redo3(prev_state[0], prev_state[1], usable - {R3_READS[1]}, F.base_pools_dir())
    assert half["report"]["wordings"]["status"] == {"pending": 19} and len(half["glex_log"]) == 19


# ------------------------------------------------------------------------------------------------ the freeze
def test_v1_state_is_untouched():
    v1 = F.v1_state()
    assert v1["unchanged"] and v1["files_changed"] == [] and v1["inputs_changed"] == [] and v1["extra_files"] == []
    assert v1["g0_unchanged"] and v1["files"] == 10 and v1["inputs"] == 21


def test_verdict_is_ready_every_g0_minimum_met_and_the_glex_gate_passes(built):
    s = built["summary"]
    assert not built["blocked"] and built["verdict"] == s["verdict"] == "READY" and s["issues"] == []
    assert s["shortfalls"] == [] and s["floors_met"] is True
    table = s["table"]
    targets = [r for r in table if r["kind"] in ("G0 floor", "G0 ask")]
    assert targets and all(r["met"] and r["shortfall"] == 0 for r in targets)
    for item, (target, got) in PREV_SHORT.items():                                    # each of the 14 old rows is closed
        row = next(r for r in targets if r["item"] == item)
        assert row["target"] == target and row["got"] >= target > got, item
    gates = [r for r in table if r["kind"] == "gate"]
    assert len(gates) == (13 if F.base_pools_dir() is not None else 12) and all(g["met"] for g in gates)
    assert next(g for g in gates if g["item"].startswith("G-LEX"))["met"]
    assert {r["item"] for r in table if r["kind"] == "gate not run"} == {
        "G13 seed-first decontamination of the pools", "Haiku file-access audit of the 71 answer files",
        "G-SL / G3-H / G5-H on rows"}


def test_redo2_closed_its_two_blockers(built):
    prog = {r["item"]: (r["v1"], r["v2"]) for r in built["summary"]["progress_vs_v1"]}
    assert prog["wording ch_end_withdraw, training"] == (2, 14) and prog["wording ch_end_withdraw, held out"] == (2, 6)
    assert prog["documents (Mode F), all"] == (202, 262) and prog["documents (Mode F), held out"] == (34, 46)
    assert prog["documents, register email"] == (44, 52) and prog["documents, register chat"] == (37, 57)
    assert prog["wordings, held out"] == (28, 32)
    assert prog["wordings, training"] == (90, 121)                                    # redo2 +12, redo3 +19


def test_the_exact_pool_counts_after_redo3(built):
    c = built["summary"]["counts"]
    assert (c["packs"], c["packs_held_out"], c["skins"], c["attacks"], c["attacks_held_out"]) == (48, 10, 360, 61, 13)
    assert c["skins_by_register"] == {"chat": 40, "email": 40, "form": 38, "json": 38, "letter": 24, "memo": 38,
                                      "receipt": 38, "ticket": 38, "transcript": 26, "yaml": 40}
    assert c["documents"] == 262 and c["wordings"] == 153 and c["lexicon_forms"] == 241
    assert c["wordings_training_by_qform"] == {"ch_end_reject": 8, "ch_end_withdraw": 14, "ch_rule": 33, "yn_double": 10,
                                               "yn_may_refuse": 12, "yn_no_right": 8, "yn_not_refund": 12, "yn_owed": 10,
                                               "yn_refund": 14}
    assert c["added_by_redo3"] == {"packs": 10, "packs_held_out": 4, "skins": 15, "attacks": 3, "attacks_held_out": 3,
                                   "wordings": 19, "wordings_held_out": 0}
    assert (c["wordings_v1"], c["wordings_redo2"], c["wordings_redo3"]) == (118, 16, 19)
    assert (c["answer_files"], c["answer_files_usable"], c["glex_reads_recorded"], c["g3h_votes"]) == (71, 71, 538, 263)
    assert (c["quarantine_v1"], c["quarantine_v2"], c["quarantine_v2_redo3"]) == (82, 2, 1)


def test_redo3_closed_each_old_shortfall_and_touched_nothing_else(built):
    if F.base_pools_dir() is None:
        pytest.skip("no pre-redo3 freeze on disk")
    prog = {r["item"]: (r["previous_freeze"], r["now"]) for r in built["summary"]["progress_vs_previous_freeze"]}
    assert set(PREV_SHORT) <= set(prog)
    assert prog["wordings, training"] == (102, 121) and prog["packs, all"] == (38, 48)
    assert prog["skins, register chat"] == (35, 40) and prog["attack lines, held out"] == (10, 13)
    untouched = ("documents (Mode F), all", "documents, register email", "wordings, held out", "notice pol.t06.final (deontic)",
                 "skins, register ticket", "skins, held-out register letter", "wording ch_end_withdraw, training")
    assert not set(untouched) & set(prog)


def test_glex_gate_in_the_freeze(built):
    g = built["summary"]["glex"]
    assert g["gate"]["pass"] and g["gate"]["n_forms"] == 241 and g["violations"] == []
    assert g["gate"]["status_counts"] == {"admitted": 241}
    assert g["reads_required_by_kind"] == {"deontic": 2, "question": 2, "window": 3}
    assert g["reads_per_form"] == {"deontic/2": 32, "question/2": 153, "window/3": 56}
    assert g["new_wordings_status"] == {"admitted": 16} and g["new_wordings_status_redo3"] == {"admitted": 19}
    assert g["not_admitted_redo2"] == {} and g["not_admitted_redo3"] == {}
    lex = files_of(built, "lexicon.json")
    assert len(lex["forms"]) == 241 and all(f["status"] == "admitted" for f in lex["forms"])
    assert "redo3" in lex["note"] and len(lex["sems"]) == 22                           # every sem kept, decoys included
    for f in lex["forms"]:
        need = 3 if f["kind"] in ("window", "precedence") else 2
        assert len({e for e, _ in f["extractions"]}) >= need and all(s == f["sem_id"] for _, s in f["extractions"])
    log = rows_of(built, "extraction_log.jsonl")
    assert len(log) == 538 and all(r["agrees"] for r in log)
    assert Counter(r["round"] for r in log) == {"v1": 468, "redo2": 32, "redo3": 38}
    assert Counter(r["extractor"] for r in log if r["round"] == "redo2") == {"haiku-r2-glex-r1": 16, "haiku-r2-glex-r2": 16}
    assert Counter(r["extractor"] for r in log if r["round"] == "redo3") == {"haiku-r3-glex-r1": 19, "haiku-r3-glex-r2": 19}
    assert Counter(r["read"] for r in log if r["kind"] == "window") == {"glex-r1": 56, "glex-r2": 56, "glex-r3": 56}
    assert all(r["kind"] == "question" for r in log if r["round"] == "redo3")


def test_g3h_gate_in_the_freeze(built):
    g = built["summary"]["g3h"]
    assert g["pooled"]["email"] == {"n": 53, "ok": 52, "rate": 0.9811, "quarantined": False}
    assert not g["quarantined_registers"] and g["unread"] == [] and g["dropped_documents"] == ["t06r2.free.r2-email.000"]
    votes = rows_of(built, "g3h_log.jsonl")
    assert len(votes) == 263 and sum(1 for v in votes if not v["ok"]) == 1 and all(v["answered"] for v in votes)
    assert Counter(v["round"] for v in votes) == {"v1": 202, "redo2": 61}
    docs = rows_of(built, "documents.jsonl")
    assert len(docs) == 262 and "t06r2.free.r2-email.000" not in {d["pid"] for d in docs}
    reg = Counter(d["register"] for d in docs)
    assert reg == {"chat": 57, "email": 52, "ticket": 54, "memo": 53, "transcript": 23, "letter": 23}
    sens = built["summary"]["sensitivity"]["g3h_template_per_batch"]
    assert sens["redo2_only_per_register"]["email"]["quarantined"] and sens["documents_by_register_per_batch"]["email"] == 44
    assert "pooled" in sens["decision"]


def test_sensitivity_of_ignoring_the_latest_round(built):
    """The latest round is redo3/reads: without its two G-LEX reads the 19 new wordings have 0 of 2 reads, are pending and
    stay out of the pools; every other redo3 piece (packs, skins, attack lines) needs no read and stays."""
    alt = built["summary"]["sensitivity"]["latest_round_answers_ignored"]
    assert F.LATEST_ROUND == "redo3/reads" and set(R3_READS) <= set(alt["what"].replace("'", " ").replace(",", " ").split())
    assert alt["verdict"] == "SHORT"
    items = {r["item"]: (r["target"], r["got"]) for r in alt["shortfalls"]}
    assert items == {"wordings, training": (106, 102), "wording ch_rule, training": (30, 24),
                     "wording yn_refund, training": (12, 10), "wording yn_double, training": (8, 7),
                     "wording yn_not_refund, training": (10, 9), "ch_rule wordings (G0 floor 30)": (30, 29)}
    assert any("19 redo3 wording(s) still pending" in i for i in alt["issues"])


def test_agrees_with_the_family_admit_stage_where_the_rules_coincide(built):
    """build_redo2.admit (the family's own supplement stage, dry run) reads the same answers: its G-LEX outcome and its
    per-batch G3-H counts must equal freeze_v2's (the two differ only in the register rule, pooled vs per batch)."""
    BR = F.build_redo2()
    adm = BR.stage_admit(False)
    assert adm["read_problems"] == [] and adm["new_wording_status"] == {"admitted": 16}
    assert adm["new_wordings_admitted"] == {"training": 12, "held_out": 4}
    ours = built["summary"]["sensitivity"]["g3h_template_per_batch"]["redo2_only_per_register"]
    theirs = adm["g3h_redo2"]
    assert {r: (d["n"], d["ok"]) for r, d in ours.items()} == {r: (d["n"], d["ok"]) for r, d in theirs.items()}
    v1 = F.read_jsonl(F.POOLS_V1 / "wordings.jsonl")
    ours_new = [w for w in rows_of(built, "wordings.jsonl") if w["form_id"] not in {x["form_id"] for x in v1}
                and w["haiku_task_id"].startswith("T06-author_wording-ee2771cd")]
    cand = {json.loads(x)["form_id"] for x in (BR.EX_ROOT / "pool" / "wordings.jsonl").read_text().splitlines() if x}
    assert {w["form_id"] for w in ours_new} == cand and len(cand) == 16                  # every candidate passed 2/2
    per_batch = built["summary"]["sensitivity"]["g3h_template_per_batch"]["documents_by_register_per_batch"]
    their_docs = Counter(d["register"] for d in F.read_jsonl(F.POOLS_V1 / "documents.jsonl"))
    assert per_batch["email"] == their_docs["email"] and per_batch["chat"] == their_docs["chat"] + 20


def test_freeze_v1_is_reproduced_and_every_v1_row_is_in_v2(built):
    assert all(built["summary"]["reproduces_v1"].values())
    assert rows_of(built, "notices.jsonl") == F.read_jsonl(F.POOLS_V1 / "notices.jsonl")
    for name, key in (("packs", "pid"), ("skins", "pid"), ("attacks", "pid"), ("documents", "pid"),
                      ("wordings", "form_id")):
        v1 = F.read_jsonl(F.POOLS_V1 / f"{name}.jsonl")
        v2 = rows_of(built, f"{name}.jsonl")
        assert v2[:len(v1)] == v1                                                        # v1 rows first, byte for byte
        assert len({r[key] for r in v2}) == len(v2)
    lex1 = json.loads((F.POOLS_V1 / "lexicon.json").read_text())
    ids2 = {f["form_id"] for f in files_of(built, "lexicon.json")["forms"]}
    assert {f["form_id"] for f in lex1["forms"]} <= ids2
    q1 = F.read_jsonl(F.POOLS_V1 / "quarantine.jsonl")
    q2 = rows_of(built, "quarantine.jsonl")
    assert [{k: v for k, v in x.items() if k != "freeze"} for x in q2[:len(q1)]] == q1
    assert all(x["freeze"] == "v1" for x in q2[:len(q1)]) and all(x["freeze"] == "v2" for x in q2[len(q1):])
    assert [x["item"] for x in q2[len(q1):]] == ["t06r2.free.r2-email.000", "t06r3.attack.r3-002"]
    assert [x.get("round") for x in q2[len(q1):]] == ["redo2", "redo3"]
    drop = q2[-1]
    assert drop["stage"] == "author" and drop["batch"] == "attacks" and drop["class"] == "fact_words"
    assert drop["reasons"] == ["fact word (seal / packaging): tag"] and drop["task_id"].startswith(R3_ATTACK)


def test_redo2_pieces_carry_their_provenance(built):
    new = [w for w in rows_of(built, "wordings.jsonl") if w["form_id"] not in
           {x["form_id"] for x in F.read_jsonl(F.POOLS_V1 / "wordings.jsonl")}
           and w["haiku_task_id"].startswith("T06-author_wording-ee2771cd")]
    assert len(new) == 16 and {w["qform"] for w in new} == {"ch_end_withdraw"}
    assert sum(1 for w in new if w["held_out"]) == 4
    for w in new:
        assert w["haiku_task_id"].startswith("T06-author_wording-ee2771cd") and w["haiku_prompt_sha"]
        assert [r[0] for r in w["reads"]] == ["haiku-r2-glex-r1", "haiku-r2-glex-r2"]
        assert all(r[1] == f"q.t06.{w['qform']}" for r in w["reads"])
    docs = [d for d in rows_of(built, "documents.jsonl") if d["pid"].startswith("t06r2.")]
    assert len(docs) == 60 and all(d["haiku_task_id"].startswith("T06-author_freeform-8ad80f22") for d in docs)
    for d in docs:
        for v in d["facts"].values():
            assert v in d["text"]                                                         # the G-SL fact-lock


def test_redo3_pieces_carry_their_provenance(built):
    w3 = [w for w in rows_of(built, "wordings.jsonl") if w["haiku_task_id"].startswith(R3_WORDING_PREFIX)]
    assert len(w3) == 19 and not any(w["held_out"] for w in w3)
    assert Counter(w["qform"] for w in w3) == {"ch_rule": 9, "yn_refund": 4, "yn_double": 3, "yn_not_refund": 3}
    for w in w3:
        assert w["haiku_prompt_sha"] and [r[0] for r in w["reads"]] == ["haiku-r3-glex-r1", "haiku-r3-glex-r2"]
        assert all(r[1] == f"q.t06.{w['qform']}" for r in w["reads"])
    packs = [p for p in rows_of(built, "packs.jsonl") if p["pid"].startswith("t06r3.")]
    assert len(packs) == 10 and sum(1 for p in packs if p["held_out"]) == 4
    assert all(set(p) == {"pid", "store", "goods", "customers", "jurisdiction", "held_out"} for p in packs)   # the v1 shape
    skins = [x for x in rows_of(built, "skins.jsonl") if x["pid"].startswith("t06r3.")]
    assert Counter((x["register"], x["held_out"]) for x in skins) == {("chat", False): 5, ("email", False): 3,
                                                                       ("yaml", False): 3, ("transcript", True): 4}
    assert all(x["haiku_task_id"].startswith(R3_SKIN) and x["skin_id"].startswith("T06-SK-r3-") for x in skins)
    assert all(x["escape"] == ("yaml" if x["register"] == "yaml" else "text") for x in skins)
    atk = [x for x in rows_of(built, "attacks.jsonl") if x["pid"].startswith("t06r3.")]
    assert len(atk) == 3 and all(x["held_out"] and x["haiku_task_id"].startswith(R3_ATTACK) for x in atk)
    assert all(x["skin_id"].startswith("T06-AT-r3-") for x in atk) and "t06r3.attack.r3-002" not in {x["pid"] for x in atk}
    ids = F.id_collisions(F.pools_from_files(built["files"]))
    assert not any(ids.values())


def test_manifest_hashes_match_and_the_producer_is_recorded(built):
    man = files_of(built, "MANIFEST.json")
    assert man["family"] == "T06" and man["version"] == F.VERSION and man["verdict"] == "READY"
    assert man["stage"] == F.STAGE and man["rounds"] == list(F.ROUNDS) and man["issues"] == []
    assert set(man["files"]) == set(built["files"]) - {"MANIFEST.json"}
    for r, meta in man["files"].items():
        assert meta["sha256"] == F.sha_text(built["files"][r]) and meta["bytes"] == len(built["files"][r].encode())
    assert man["code"]["freeze_v2.py"] == F.sha_file(Path(F.__file__))
    assert man["binding"]["G0_pin_match"] and man["binding"]["a38_frozen"] and man["binding"]["v1_unchanged"]
    assert man["binding"]["audit_failed_ignored"] == []
    assert man["inputs"]["pools/manifest.json"]["sha256"] == F.sha_file(F.POOLS_V1 / "manifest.json")
    assert "haiku/redo2/extract/answers/T06-extract_lex-712abdc8-000.json" in man["inputs"]
    assert man["shortfalls"] == []
    assert "haiku/redo3/answers/T06-author_wording-7606f3cc-000.json" in man["inputs"]
    assert "haiku/redo3/reads/answers/T06-extract_lex-11a053b2-000.json" in man["inputs"]
    assert man["redo3"]["checks"]["read_tasks_equal_rebuild"] and man["redo3"]["checks"]["lint_equals_recorded_LINT_json"]
    prev = man["binding"]["previous_freeze"]
    if F.base_pools_dir() is not None:
        base = F.base_pools_dir()
        assert prev["dir"] == base.name and prev["MANIFEST_sha256"] == F.sha_file(base / "MANIFEST.json")
        assert prev["verdict"] == "SHORT" and prev["shortfalls"] == 14 and prev["recomputed_state_equals_it"]
        assert prev["files_differing"] == [] and f"{base.name}/MANIFEST.json" in man["inputs"]
        assert man["redo3"]["checks"]["authoring_tasks_equal_rebuild_from_previous_freeze"] is True
    assert man["loading"]["plugin_reads_pools"] is False and "wired_plugin" in man["loading"]["note"]
    av = files_of(built, "ANSWER_VALIDATION.json")
    assert len(av["files"]) == 71 and av["invalid"] == [] and av["audit_failed_ignored"] == []


def test_no_label_word_or_fixture_question_in_any_narrative_pool(built):
    """The loaders' own rule, re-checked on the union: no gold-label word in a skin, attack or document (values removed),
    and no fixture question text anywhere."""
    from c2_kit import skin as K
    for name in ("skins.jsonl", "attacks.jsonl", "documents.jsonl"):
        for r in rows_of(built, name):
            text = K.PH_RE.sub(" ", r["text"])
            for v in r.get("facts", {}).values():
                text = text.replace(v, " ")
            assert H._label_hits(text) == [], (name, r["pid"])
            assert not [q for q in H.QSTRINGS if q.lower() in r["text"].lower()], (name, r["pid"])


def test_an_ignored_g3h_file_leaves_its_documents_unread_and_unadmitted():
    res = F.build(frozenset({R2X[1]}), sensitivity=False)
    s = res["summary"]
    assert res["verdict"] == "SHORT" and not res["blocked"]
    g = s["g3h"]
    assert len(g["unread"]) == 27 and not g["quarantined_registers"]                      # not counted as mismatches
    docs = [json.loads(x) for x in res["files"]["documents.jsonl"].splitlines()]
    votes = [json.loads(x) for x in res["files"]["g3h_log.jsonl"].splitlines()]
    assert len(docs) == 202 + sum(1 for v in votes if v["round"] == "redo2" and v["answered"] and v["ok"])
    assert len(docs) < 262 and not set(g["unread"]) & {d["pid"] for d in docs}
    gate = next(r for r in s["table"] if r["item"].startswith("G3-H"))
    assert not gate["met"] and gate["got"]["unread"] == 27
    man = json.loads(res["files"]["MANIFEST.json"])
    assert man["binding"]["audit_failed_ignored"] == [R2X[1]]
    assert [x for x in json.loads(res["files"]["ANSWER_VALIDATION.json"])["files"] if x["ignored"]][0]["task_id"] == R2X[1]


# ------------------------------------------------------------------------------------------------ write / check / load
def test_write_check_load_roundtrip(built, scratch):
    written = F.write_pools(built, scratch)
    assert "MANIFEST.json" in written and len(written) == len(built["files"])
    assert F.check_pools(built, scratch) == []
    assert F.write_pools(built, scratch) == written                                         # identical: a no-op
    pools = F.load_pools_v2(scratch, require_ready=False)
    assert len(pools["documents"]) == 262 and len(pools["wordings"]) == 153 and pools["manifest"]["verdict"] == "READY"
    assert len(F.load_pools_v2(scratch)["packs"]) == 48                                     # READY: loads by default
    v1 = F.v1_state()
    assert v1["unchanged"]
    # a different freeze is never overwritten
    other = dict(built, files=dict(built["files"], **{"packs.jsonl": built["files"]["packs.jsonl"] + "\n"}))
    with pytest.raises(SystemExit, match="written once"):
        F.write_pools(other, scratch)
    assert F.check_pools(other, scratch) == ["packs.jsonl"]
    # a changed byte is caught by the loader
    p = scratch / "wordings.jsonl"
    keep = p.read_text()
    p.write_text(keep.replace("legal", "lawful", 1))
    with pytest.raises(ValueError, match="differs from MANIFEST"):
        F.load_pools_v2(scratch, require_ready=False)
    p.write_text(keep)
    F.load_pools_v2(scratch, require_ready=False)


def test_a_short_freeze_is_refused_by_default(built):
    """The loader's safe default: a SHORT verdict in the MANIFEST is refused unless require_ready=False is passed."""
    man = json.loads(built["files"]["MANIFEST.json"])
    man["verdict"], man["shortfalls"] = "SHORT", [{"item": "packs, all"}]
    short = dict(built, files=dict(built["files"], **{"MANIFEST.json": json.dumps(man, indent=1) + "\n"}))
    root = HERE / "_t_scratch_pools_short"                                  # the kit's writers only write under lean/
    shutil.rmtree(root, ignore_errors=True)
    try:
        F.write_pools(short, root)
        with pytest.raises(ValueError, match="SHORT"):
            F.load_pools_v2(root)
        assert F.load_pools_v2(root, require_ready=False)["manifest"]["verdict"] == "SHORT"
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_pools_v2_on_disk_equals_a_rebuild_when_written(built):
    mf = F.POOLS_V2 / "MANIFEST.json"
    man = json.loads(mf.read_text()) if mf.exists() else None
    if man is None or "redo3" not in man.get("rounds", ()):
        pytest.skip("pools_v2 on disk is not the redo3 re-freeze (not written yet)")
    # MANIFEST.json records the sha256 of its producers (plugin.py, freeze_v2.py ...), which the pilot fix iteration 1 edited
    # (G0 v3); every pool file is still reproduced byte for byte and load_pools_v2 verifies each against the manifest
    assert [d for d in F.check_pools(built) if d != "MANIFEST.json"] == []
    assert F.load_pools_v2(require_ready=False)["manifest"]["verdict"] == "READY"


# ------------------------------------------------------------------------------------------------ the consumer
@pytest.fixture(scope="module")
def pools(built):
    return F.pools_from_files(built["files"])


def test_mode_f_documents_are_thinned_to_a_quarter_of_each_register(pools):
    kept = F.thin_documents(pools["skins"], pools["documents"])
    t = Counter((s["register"], s["held_out"]) for s in pools["skins"])
    f = Counter((d["register"], d["held_out"]) for d in kept)
    assert f and all(f[k] / (f[k] + t[k]) <= 0.25 for k in f)
    assert f[("chat", False)] == 40 // 3 and f[("letter", True)] == 24 // 3
    assert kept == F.thin_documents(pools["skins"], pools["documents"])                      # deterministic
    assert {d["pid"] for d in kept} <= {d["pid"] for d in pools["documents"]}
    assert len(F.thin_documents(pools["skins"], pools["documents"], 0.5)) > len(kept)


def test_kit_ctx_and_wired_plugin_build_units(pools):
    ctx = F.kit_ctx(pools)
    assert ctx.lexicon.gate()["pass"] and len(ctx.lexicon.forms) == 241
    kinds = Counter((s.kind, s.author_mode if s.kind == "skin" else None) for s in ctx.skins.values())
    assert kinds[("wording", None)] == 153 and kinds[("attack", None)] == 61 and kinds[("skin", "T")] == 360
    assert 0 < kinds[("skin", "F")] < 262
    assert len(F.kit_ctx(pools, mode_f_cap=None).skins) == len(ctx.skins) - kinds[("skin", "F")] + 262
    old = {k: getattr(P, k) for k in ("STORES", "CUSTOMERS", "ITEMS", "JURIS", "JURIS_HELD")}
    ok = bad = 0
    stores, used = set(), []
    with F.wired_plugin(pools) as new:
        assert P.STORES == new["STORES"] != old["STORES"]
        assert set(new["JURIS_HELD"]) == {x["jurisdiction"] for x in pools["packs"] if x["held_out"]}
        assert not set(new["STORES"]) & {x["store"] for x in pools["packs"] if x["held_out"]}
        plugin = P.T06Plugin(lexicon=ctx.lexicon)
        for seed in range(6):
            for smp in ("S1", "S2", "S3", "S4", "S5"):
                spec = plugin.sample(seed, smp)
                used.append((smp, spec.slots["STORE"].value, spec.slots["JURIS"].value, spec.slots["ITEM"].value))
                res = pipeline.build_unit(plugin, spec, ctx, run_g15=False)
                ok += res.ok
                bad += not res.ok
                stores.add(spec.slots["STORE"].value)
    assert {k: getattr(P, k) for k in old} == old                                           # restored on exit
    assert ok >= 0.9 * (ok + bad), (ok, bad)
    assert stores <= set(new["STORES"])
    assert all(j in new["JURIS_HELD"] for smp, _s, j, _i in used if smp == "S5")
    assert all(j in new["JURIS"] for smp, _s, j, _i in used if smp != "S5")


def test_wired_plugin_restores_the_constants_after_an_error(pools):
    old = P.STORES
    with pytest.raises(RuntimeError):
        with F.wired_plugin(pools):
            raise RuntimeError("boom")
    assert P.STORES is old


def test_load_pools_default_serves_a_ready_freeze_and_refuses_a_short_one_for_the_context_too():
    if not (F.POOLS_V2 / "MANIFEST.json").exists():
        pytest.skip("pools_v2 not written yet")
    verdict = json.loads((F.POOLS_V2 / "MANIFEST.json").read_text())["verdict"]
    if verdict == "READY":
        assert len(F.kit_ctx().lexicon.forms) >= 222
    else:
        with pytest.raises(ValueError, match="SHORT"):
            F.kit_ctx()


def test_cli_flags(monkeypatch, capsys):
    calls = {}

    def fake_build(failed=frozenset(), *, sensitivity=True):
        calls["args"] = (set(failed), sensitivity)
        return {"blocked": True, "verdict": "SHORT", "files": {}, "summary": {
            "verdict": "SHORT", "blocked": True, "issues": ["x"], "validation": {}, "v1_unchanged": True}}
    monkeypatch.setattr(F, "build", fake_build)
    assert F.main(["--audit-failed", "a,b", "--no-sensitivity"]) == 4
    assert calls["args"] == ({"a", "b"}, False)
    assert json.loads(capsys.readouterr().out)["blocked"] is True

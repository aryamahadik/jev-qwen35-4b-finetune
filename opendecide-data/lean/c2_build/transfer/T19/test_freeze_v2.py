"""transfer/T19/test_freeze_v2.py: tests of freeze_v2.py (v1 pools + redo2 + redo3 answers -> pools_v2/). Nothing here
writes a file under the family folder: build() runs in memory, the on-disk pools_v2/ checks only read it, and the
baseline tests copy pools_v2_prev/ into a pytest tmp dir. The answer snippets below are test stand-ins for the
contract checks, and the mutated read answers are test inputs for the keep rule, never answers to a task."""
from __future__ import annotations

import copy
import json
import shutil
import sys
from collections import Counter
from pathlib import Path

import pytest

_C2_BUILD = Path(__file__).resolve().parents[2]
if str(_C2_BUILD) not in sys.path:
    sys.path.insert(0, str(_C2_BUILD))

from c2_kit.lexicon import LexiconError, LexiconRegistry, question_sem  # noqa: E402
from transfer.T19 import extract_build as EX  # noqa: E402
from transfer.T19 import fixtures as FX  # noqa: E402
from transfer.T19 import freeze as FZ  # noqa: E402
from transfer.T19 import freeze_v2 as V  # noqa: E402
from transfer.T19 import redo3_reads as RR  # noqa: E402


@pytest.fixture(scope="module")
def built():
    return V.build(())


# ------------------------------------------------------------------------------------------------ targets

def test_targets_are_pinned_and_a_lowered_target_is_detected(monkeypatch):
    assert V.pinned_targets_ok() and V.PINNED_TOTAL == 344 == sum(
        [V.PINNED_TARGETS["packs_train"], V.PINNED_TARGETS["packs_held"], V.PINNED_TARGETS["attack"]]
        + list(V.PINNED_TARGETS["skin"].values()) + list(V.PINNED_TARGETS["skin_heldout"].values())
        + list(V.PINNED_TARGETS["freeform"].values()) + list(V.PINNED_TARGETS["wording"].values()))
    monkeypatch.setitem(FZ.TARGETS["wording"], "yn_fails", 13)
    assert not V.pinned_targets_ok()
    with pytest.raises(SystemExit):
        V.build(())


# ------------------------------------------------------------------------------------------------ answer contracts

PACK = {"sites": ["a", "b", "c", "d"], "auditors": ["e", "f", "g", "h"], "controls": list("abcdefgh")}


def _spec(field, qids=("qa", "qb"), n_cand=None, choices=None):
    return {"field": field, "qids": list(qids), "n_cand": n_cand, "choices": choices or {}}


@pytest.mark.parametrize("raw,ok", [
    ([{"qid": "qa", "text": "x"}, {"qid": "qb", "text": "y"}], True),
    ([{"qid": "qb", "text": "y"}, {"qid": "qa", "text": ""}], True),            # content is the loaders' job
    ({"qa": "x"}, False),                                                        # not an array
    ([{"qid": "qa", "text": "x"}, "qb"], False),                                 # an entry that is not an object
    ([{"qid": "qa", "text": "x"}], False),                                       # qb unanswered
    ([{"qid": "qa", "text": "x"}, {"qid": "qa", "text": "x"}, {"qid": "qb", "text": "y"}], False),   # repeat
    ([{"qid": "qa", "text": "x"}, {"qid": "qz", "text": "y"}], False),           # a qid of another task
    ([{"qid": "qa", "text": "x"}, {"qid": "qb", "text": "y", "note": "z"}], False),   # another key
    ([{"qid": "qa", "text": "x"}, {"qid": "qb", "texts": ["y"]}], False),        # the wrong field
    ([{"qid": "qa", "text": "x"}, {"qid": "qb", "text": 7}], False),             # not a string
    ([{"qid": "qa", "text": "x"}, {"text": "y"}], False),                        # no qid
])
def test_text_contract(raw, ok):
    assert (V.check_answer(raw, _spec("text")) == []) == ok


def test_pack_contract():
    sp = _spec("pack")
    good = [{"qid": "qa", "pack": PACK}, {"qid": "qb", "pack": PACK}]
    assert V.check_answer(good, sp) == []
    assert V.check_answer([{"qid": "qa", "pack": {**PACK, "extra": []}}, good[1]], sp)
    assert V.check_answer([{"qid": "qa", "pack": {"sites": PACK["sites"]}}, good[1]], sp)
    assert V.check_answer([{"qid": "qa", "pack": {**PACK, "sites": ["a", 3]}}, good[1]], sp)
    assert V.check_answer([{"qid": "qa", "pack": "none"}, good[1]], sp)


def test_redo2_candidate_contract():
    sp = _spec("texts", n_cand=2)
    ok = [{"qid": "qa", "texts": ["x", "y"]}, {"qid": "qb", "texts": ["z", "w"]}]
    assert V.check_answer(ok, sp) == []
    assert V.check_answer([{"qid": "qa", "texts": ["x"]}, ok[1]], sp)               # one candidate too few
    assert V.check_answer([{"qid": "qa", "texts": ["x", "y", "u"]}, ok[1]], sp)     # one too many
    assert V.check_answer([{"qid": "qa", "texts": ["x", None]}, ok[1]], sp)
    sp = _spec("packs", n_cand=2)
    ok = [{"qid": "qa", "packs": [PACK, PACK]}, {"qid": "qb", "packs": [PACK, PACK]}]
    assert V.check_answer(ok, sp) == []
    assert V.check_answer([{"qid": "qa", "packs": [PACK]}, ok[1]], sp)
    assert V.check_answer([{"qid": "qa", "packs": [PACK, {"sites": []}]}, ok[1]], sp)


def test_read_contract():
    sp = _spec("meaning", choices={"qa": ["m1", "m2"], "qb": ["m1", "m2"]})
    assert V.check_answer([{"qid": "qa", "meaning": "m1"}, {"qid": "qb", "meaning": "m2"}], sp) == []
    assert V.check_answer([{"qid": "qa", "meaning": "m1"}, {"qid": "qb", "meaning": "M2"}], sp)   # not copied exactly
    assert V.check_answer([{"qid": "qa", "meaning": "m1"}, {"qid": "qb", "meaning": ["m2"]}], sp)
    sp = _spec("auditor")
    assert V.check_answer([{"qid": "qa", "auditor": "A B"}, {"qid": "qb", "auditor": "C D"}], sp) == []
    assert V.check_answer([{"qid": "qa", "auditor": "A B"}, {"qid": "qb", "auditor": None}], sp)


def test_round_specs_cover_all_42_answer_files():
    specs = V.round_specs()
    assert len(specs) == 42
    rounds = ("r1_author", "r1_extract", "redo2_author", "redo2_extract", "redo3_author", "redo3_extract")
    assert {r: sum(1 for s in specs if s["round"] == r) for r in rounds} == {
        "r1_author": 20, "r1_extract": 7, "redo2_author": 7, "redo2_extract": 5, "redo3_author": 1,
        "redo3_extract": 2}
    assert sum(len(s["qids"]) for s in specs if s["round"] == "r1_author") == 344
    assert sum(len(s["qids"]) for s in specs if s["round"] == "r1_extract") == 229
    assert sum(len(s["qids"]) for s in specs if s["round"] == "redo2_author") == 79
    assert sum(len(s["qids"]) * (s["n_cand"] or 1) for s in specs if s["round"] == "redo2_author") == 196
    assert sum(len(s["qids"]) for s in specs if s["round"] == "redo2_extract") == 128
    assert sum(len(s["qids"]) * (s["n_cand"] or 1) for s in specs if s["round"] == "redo3_author") == 6
    assert sum(len(s["qids"]) for s in specs if s["round"] == "redo3_extract") == 12
    assert len({(s["dir"], s["task_id"]) for s in specs}) == 42
    # the redo3 specs come from the files the agents were given: 3 candidates per item, meanings from the chunks
    a3 = next(s for s in specs if s["round"] == "redo3_author")
    assert a3["field"] == "texts" and a3["n_cand"] == 3 and a3["dir"] == V.ROOT3 and len(a3["qids"]) == 2
    for s3 in (s for s in specs if s["round"] == "redo3_extract"):
        assert s3["field"] == "meaning" and s3["dir"] == V.XROOT3 and len(s3["choices"]) == 6
        assert all(len(c) == 6 for c in s3["choices"].values())


# ------------------------------------------------------------------------------------------------ vote rules

def _question_registry():
    reg = LexiconRegistry("T19")
    for qf, meaning in FX.QUESTION_MEANINGS.items():
        reg.declare(question_sem("T19", qf), "question", meaning)
    fo = reg.add("Is {SITE} out of compliance with the checklist on the audit date?",
                 question_sem("T19", "yn_out_of"), slots={"SITE": "name"}, source="haiku", family="T19",
                 haiku_task_id="t", haiku_prompt_sha="0" * 64)
    assert reg.unit_test(fo.form_id)
    return reg, fo.form_id


def _vote(reg, fid, extractor, qform):
    FZ.record_glex(reg, {fid: {"meaning": FX.QUESTION_MEANINGS[qform]}}, extractor)


def test_question_forms_are_admitted_at_two_of_two_and_a_dissent_rejects():
    reg, fid = _question_registry()
    assert reg.forms[fid].required == 2 and reg.status(fid) == "pending"
    _vote(reg, fid, "x1", "yn_out_of")
    assert reg.status(fid) == "pending"                       # one vote is not enough
    _vote(reg, fid, "x2", "yn_out_of")
    assert reg.status(fid) == "admitted"
    reg, fid = _question_registry()
    _vote(reg, fid, "x1", "yn_out_of")
    _vote(reg, fid, "x2", "yn_not_compliant")                 # one dissent rejects for good
    assert reg.status(fid) == "rejected"
    _vote(reg, fid, "x3", "yn_out_of")
    assert reg.status(fid) == "rejected"                      # no re-vote can admit it


def test_a_meaning_off_the_list_rejects_and_an_extractor_votes_once():
    reg, fid = _question_registry()
    FZ.record_glex(reg, {fid: {"meaning": "asks something else"}}, "x1")
    assert reg.status(fid) == "rejected"
    reg, fid = _question_registry()
    _vote(reg, fid, "x1", "yn_out_of")
    with pytest.raises(LexiconError):
        _vote(reg, fid, "x1", "yn_out_of")                     # the same extractor cannot vote twice


def test_precedence_and_window_forms_need_three_of_three():
    reg = LexiconRegistry("kit")
    reg.declare("prec.P1", "precedence", "deny rules beat ask rules")
    reg.declare("win.rolling", "window", "at most N in any window")
    for sem, text in (("prec.P1", "deny rules beat ask rules, which beat allow rules"),
                      ("win.rolling", "no more than one in any rolling window")):
        fo = reg.add(text, sem, slots={})
        reg.unit_test(fo.form_id)
        assert fo.required == 3
        reg.record_extraction(fo.form_id, "a", sem)
        reg.record_extraction(fo.form_id, "b", sem)
        assert reg.status(fo.form_id) == "pending"             # 2 of 3 is not enough for these kinds
        reg.record_extraction(fo.form_id, "c", sem)
        assert reg.status(fo.form_id) == "admitted"


def test_g3h_is_one_template_per_candidate_document():
    fields = EX.g3h_fields()
    expected = {"c0": {"auditor": "Dana Okafor"}, "c1": {"auditor": "Dana Okafor"}, "c2": {"auditor": "Dana Okafor"}}
    got = {"c0": {"auditor": "Dana Okafor"}, "c1": {"auditor": "Dana Okafro"}}
    rep = V.record_g3h(expected, got, fields)
    assert [k for k, r in rep["results"].items() if r["ok"]] == ["c0"]
    assert rep["results"]["c1"]["diffs"] and rep["results"]["c2"]["diffs"] == ["no answer"]
    assert rep["results"]["c2"]["read"] is False
    assert rep["template_quarantined"] == ["c1", "c2"] and rep["bar"] == 0.98
    # a passing candidate beside a failing one of the same item is not dragged under the 0.98 bar
    assert V.pick_first([{"j": 0}, {"j": 1}], lambda c: rep["results"][f"c{c['j']}"]["ok"]) == 0
    assert V.pick_first([{"j": 1}, {"j": 2}], lambda c: rep["results"][f"c{c['j']}"]["ok"]) is None


# ------------------------------------------------------------------------------------------------ the build

def test_every_answer_file_is_validated_and_none_is_edited(built):
    s = built["validation"]
    assert s["files"] == 42 and s["unexpected_files"] == []
    assert s["accepted"] + len(s["rejected_invalid"]) + len(s["missing"]) + len(s["ignored_audit_failed"]) == 42
    assert s["accepted"] == 42 and s["rejected_invalid"] == [] and s["missing"] == []
    assert s["by_round"]["redo2_extract"]["files"] == 5 and s["by_round"]["redo2_author"]["files"] == 7
    assert s["by_round"]["redo3_extract"]["files"] == 2 and s["by_round"]["redo3_author"]["files"] == 1
    files = json.loads(built["files"]["answers_validation.json"])["files"]
    assert all(r["sha256"] for r in files if r["status"] in ("accepted", "rejected_invalid"))
    for r in files:
        if r["status"] == "accepted":
            assert not r["problems"]


def test_v1_is_untouched_and_re_derived(built):
    assert built["v1"]["ok"] and built["v1"]["rederived"]["ok"] and built["v1"]["equals_pools_round1_backup"]
    assert V.v1_state() == built["manifest"]["lineage"]["v1_sha256"]
    man = json.loads((FZ.POOLS / "MANIFEST.json").read_text(encoding="utf-8"))
    assert man["version"] == "v1" and man["shortfalls"]                 # redo2.py's guards still read the v1 shortfalls
    assert not (V.POOLS_V2 == FZ.POOLS)


def test_counts_shortfalls_and_status_agree(built):
    c, t = built["counts"], V.PINNED_TARGETS
    short = {s["item"]: s for s in built["shortfalls"]}
    for grp in ("skin", "skin_heldout", "freeform", "wording"):
        for k, want in t[grp].items():
            have = c[grp].get(k, 0)
            assert have <= want
            assert (f"{grp}/{k}" in short) == (have < want)
            if have < want:
                assert short[f"{grp}/{k}"] == {"item": f"{grp}/{k}", "admitted": have, "target": want,
                                               "shortfall": want - have}
    assert c["packs_train"] <= 32 and c["packs_held"] <= 8 and c["attack"] <= 30
    assert built["short_total"] == sum(s["shortfall"] for s in built["shortfalls"])
    assert built["admitted_total"] + built["short_total"] == V.PINNED_TOTAL
    assert built["ready"] == (not built["shortfalls"] and all(built["hard_gates_ok"].values()))
    assert built["status"].startswith("READY" if built["ready"] else "SHORT")
    v1 = built["manifest"]["lineage"]["v1_counts"]
    for grp in ("skin", "skin_heldout", "freeform", "wording"):
        assert all(c[grp].get(k, 0) >= v for k, v in v1[grp].items())    # redo2 only adds


def test_every_gate_is_applied_and_reported(built):
    g = built["gates"]
    assert {"H15_slots", "skin_ids_unique", "G12_exact_text_dedup", "packs", "G-LEX", "G3-H"} <= set(g)
    assert all(built["hard_gates_ok"].values()), built["hard_gates_ok"]
    assert g["G-LEX"]["pass"] and g["G-LEX"]["not_admitted_used"] == {} and g["G-LEX"]["unknown"] == []
    assert g["G-LEX"]["status_counts"] == {"admitted": g["G-LEX"]["forms_used"]}
    assert g["G3-H"]["bar"] == 0.98 and g["G3-H"]["frozen_redo2_documents_all_passed"]
    assert g["packs"]["held_names_also_in_training_packs"] == []


def test_final_lexicon_holds_only_admitted_forms_with_their_votes(built):
    reg = built["final_registry"]
    words = json.loads(built["files"]["wordings.json"])
    assert {w["form_id"] for w in words} == set(reg.forms)
    v1_ids = {w["form_id"] for w in json.loads((FZ.POOLS / "wordings.json").read_text(encoding="utf-8"))}
    for w in words:
        f = reg.forms[w["form_id"]]
        assert reg.status(w["form_id"]) == "admitted" and f.sem_id == question_sem("T19", w["qform"])
        exts = {e for e, _ in f.extractions}
        assert len(exts) >= f.required and all(s == f.sem_id for _, s in f.extractions)
        kept3 = {k["form_id"] for k in built["redo3"]["kept"]}
        if w["form_id"] in v1_ids:
            assert exts == {"haiku-glex-question-r1", "haiku-glex-question-r2"}      # round 1 reads stand
        elif w["form_id"] in kept3:
            assert exts == {"haiku-glex-question-redo3-r1", "haiku-glex-question-redo3-r2"}
        else:
            assert exts == {"haiku-glex-question-redo2-r1", "haiku-glex-question-redo2-r2"}
        assert w["text"].count("{SITE}") == 1


def test_redo2_pieces_are_new_unique_and_traceable(built):
    prov = json.loads(built["files"]["votes.json"])["provenance_of_redo2_pieces"]
    v1_ids = set()
    for f in ("skins.json", "attacks.json", "documents.json"):
        v1_ids |= {d["skin_id"] for d in json.loads((FZ.POOLS / f).read_text(encoding="utf-8"))}
    v1_ids |= {p["pack_id"] for p in json.loads((FZ.POOLS / "packs.json").read_text(encoding="utf-8"))}
    v1_ids |= {w["form_id"] for w in json.loads((FZ.POOLS / "wordings.json").read_text(encoding="utf-8"))}
    ids = [r["piece_id"] for r in prov]
    assert len(ids) == len(set(ids)) and not set(ids) & v1_ids
    assert all(r["task"].startswith("T19-redo2-") for r in prov)
    assert len({r["qid"] for r in prov}) == len(prov)                     # at most one piece per item
    docs = json.loads(built["files"]["documents.json"])
    assert all("{" not in d["text"] for d in docs)                        # a Mode F note holds no placeholder
    assert all(d["author_mode"] == "F" for d in docs)


def test_build_is_deterministic(built):
    again = V.build(())
    assert again["files"] == built["files"]


def test_an_audit_failed_read_is_ignored_and_the_pools_stay_short():
    ids = [s["task_id"] for s in V.round_specs() if s["round"] == "redo2_extract"]
    res = V.build(tuple(ids))
    assert set(res["validation"]["ignored_audit_failed"]) == set(ids)
    assert not res["ready"] and res["status"].startswith("SHORT")
    short = {s["item"]: s["shortfall"] for s in res["shortfalls"]}
    assert sum(v for k, v in short.items() if k.startswith("freeform/")) == 13
    assert sum(v for k, v in short.items() if k.startswith("wording/")) == 26
    assert res["short_total"] == 39                                       # the 305 of 344 candidate of the last round
    assert res["gates"]["G-LEX"]["pass"]                                  # nothing unread is ever used
    # redo3 was written beside the freeze that held those reads: its baseline no longer matches, so no redo3 piece
    assert res["hard_gates_ok"]["redo3_baseline_intact"] is False and not res["redo3"]["active"]
    assert res["redo3"]["kept"] == []


def test_an_unanswered_authoring_task_leaves_its_items_short():
    pk = next(s["task_id"] for s in V.round_specs() if s["round"] == "redo2_author" and s["task_id"].endswith(
        "packs-000"))
    res = V.build((pk,))
    short = {s["item"]: s["shortfall"] for s in res["shortfalls"]}
    assert short.get("packs_train") == 1 and short.get("packs_held") == 1
    assert res["reads_usable"]                                            # the reads do not depend on packs


def test_wording_authoring_answers_missing_make_the_read_files_unusable():
    wd = next(s["task_id"] for s in V.round_specs() if s["round"] == "redo2_author" and s["task_id"].endswith(
        "wordings-000"))
    res = V.build((wd,))
    assert not res["reads_usable"] and not res["ready"]                   # drift: no read is applied to other items
    assert res["glex_reads"] == {}


# ------------------------------------------------------------------------------------------------ redo3 (step 6)

OUT_OF = FX.QUESTION_MEANINGS["yn_out_of"]
CELL3 = "wording/yn_not_compliant"
USING, WITH, MEASURED = "Using the card's definitions", "With the records in front of you", "Measured against the card"
AFTER, WORKING, VIEW = "After checking the evidence log", "Working from the profile", "In the view of a careful"


@pytest.fixture(scope="module")
def r3_answers():
    val = V.validate_answers(())
    return val["raw"]["redo3_author"], val["raw"]["redo3_extract"]


def _prev_state():
    """The stage 5 registry and wording counts: pools_v2_prev/ (checked equal to the stage 5 build by the baseline)."""
    lex = LexiconRegistry.from_json(json.loads((V.POOLS_V2_PREV / "lexicon.json").read_text(encoding="utf-8")))
    words = json.loads((V.POOLS_V2_PREV / "wordings.json").read_text(encoding="utf-8"))
    return lex, Counter(w["qform"] for w in words)


def _dissent(raw_reads, fragment, only_task=None):
    """A copy of the redo3 read answers in which the form whose question text contains `fragment` is read as
    yn_out_of (by one read task, or by all)."""
    out = copy.deepcopy(raw_reads)
    for tid, answers in out.items():
        if only_task is not None and tid != only_task:
            continue
        chunk = json.loads((V.XROOT3 / "chunks" / f"{tid}.json").read_text(encoding="utf-8"))
        text_of = {i["qid"]: i["text"] for i in chunk["items"]}
        for a in answers:
            if fragment in text_of[a["qid"]]:
                a["meaning"] = OUT_OF
    return out


def _stage(raw_author, raw_reads, have=None):
    lex, cnt = _prev_state()
    return V.redo3_stage(raw_author, raw_reads, lex, cnt if have is None else have)


def _kept(res):
    return [(k["qid"], k["candidate"]) for k in res["kept"]]


def test_redo3_baseline_is_the_previous_freeze_and_the_index_recorded_it(built):
    idx = json.loads((V.ROOT3 / "REDO3_INDEX.json").read_text(encoding="utf-8"))
    assert idx["g0_changed"] is False and idx["b_authoring"]["cell"] == CELL3 and idx["b_authoring"]["gap"] == 1
    b = built["baseline"]
    assert b["ok"] and b["problems"] == [] and b["pool_files_differ_from_stage5"] == []
    assert b["manifest_sha256"] == idx["source"]["pools_v2_manifest_sha256"]
    prev = json.loads((V.POOLS_V2_PREV / "MANIFEST.json").read_text(encoding="utf-8"))
    assert not prev["ready"] and [x["item"] for x in prev["shortfalls"]] == [CELL3]
    assert RR.POOLS_V2 == V.POOLS_V2_PREV != V.POOLS_V2                  # redo3 stays judged against what it was built on


def test_redo3_piece_is_folded_in_and_the_last_shortfall_closes(built):
    assert built["ready"] and built["status"].startswith("READY") and built["shortfalls"] == []
    assert built["open_items"] == [] and built["admitted_total"] == V.PINNED_TOTAL == 344
    assert built["counts"]["wording"]["yn_not_compliant"] == 14 == V.PINNED_TARGETS["wording"]["yn_not_compliant"]
    assert sum(built["counts"]["wording"].values()) == 114
    r3 = built["redo3"]
    assert r3["active"] and r3["reads_usable"] and r3["drift"] == [] and r3["problems"] == [] and r3["cap"] == 1
    assert [(k["qid"], k["candidate"]) for k in r3["kept"]] == [(r3["order"][0], 0)]      # item 1, first candidate
    kept = r3["kept"][0]
    assert kept["text"] == "Using the card's definitions, is {SITE} not compliant with its checklist on the audit date?"
    words = {w["form_id"]: w for w in json.loads(built["files"]["wordings.json"])}
    w = words[kept["form_id"]]
    assert w["qform"] == "yn_not_compliant" and w["text"] == kept["text"] and w["haiku_task_id"] == kept["task"]
    assert {e for e, _ in w["extractions"]} == {"haiku-glex-question-redo3-r1", "haiku-glex-question-redo3-r2"}
    # the five other admitted candidates are reserves: reported, never frozen (the cell may not exceed its target)
    lex = json.loads(built["files"]["lexicon.json"])
    q = json.loads(built["files"]["quarantine.json"])["redo3"]
    assert len(q["admitted_reserves_not_kept"]) == 5 and q["forms_not_admitted"] == [] and q["problems"] == []
    for x in q["admitted_reserves_not_kept"]:
        assert x["form_id"] not in words and x["form_id"] not in {f["form_id"] for f in lex["forms"]}
    assert lex["note"].endswith("(question meanings)") and "redo3" in lex["note"]
    # the redo2 item that stayed open is closed by it (history kept, not listed as open)
    closed = q["redo2_wording_items_closed_by_redo3"]
    assert [c["qid"] for c in closed] == ["qb8572add92"] and closed[0]["closed_by"][0].startswith("T19-redo3-wordings-000")
    votes = json.loads(built["files"]["votes.json"])
    assert [(p["qid"], p["candidate"], p["piece_id"]) for p in votes["provenance_of_redo3_pieces"]] == [
        (kept["qid"], 0, kept["form_id"])]
    assert votes["redo3"]["glex_reads"]["glex-question-redo3-r1"]["agrees"] == 6
    assert votes["redo3"]["glex_reads"]["glex-question-redo3-r2"]["agrees"] == 6
    man = built["manifest"]
    assert man["redo3"]["kept"] == r3["kept"] and man["lineage"]["redo3_pieces_added"] == {"wordings": 1}
    assert man["lineage"]["redo3_items"] == 2 and man["lineage"]["redo3_items_kept"] == 1
    assert man["stage"] == "freeze (v1 pools + redo2 + redo3)" and man["hard_gates_ok"]["redo3_baseline_intact"]
    assert built["gates"]["G-LEX"]["pass"] and built["gates"]["G-LEX"]["forms_used"] == 114


def test_without_the_redo3_answer_the_build_reproduces_the_previous_freeze():
    task = next(s["task_id"] for s in V.round_specs() if s["round"] == "redo3_author")
    res = V.build((task,))
    assert not res["redo3"]["active"] and res["redo3"]["kept"] == []
    assert res["validation"]["ignored_audit_failed"] == [task]
    assert [(s["item"], s["admitted"], s["target"]) for s in res["shortfalls"]] == [(CELL3, 13, 14)]
    assert not res["ready"] and res["status"].startswith("SHORT") and res["short_total"] == 1
    for name in ("skins.json", "attacks.json", "documents.json", "wordings.json", "lexicon.json", "packs.json"):
        assert res["files"][name] == (V.POOLS_V2_PREV / name).read_text(encoding="utf-8"), name
    assert [o["qid"] for o in res["open_items"]] == ["qb8572add92"]       # redo2's item is open again, nothing else


def test_redo3_stage_keeps_the_first_admitted_candidate_of_the_first_item(r3_answers):
    ra, rr = r3_answers
    res = _stage(ra, rr)
    order = res["order"]
    assert _kept(res) == [(order[0], 0)] and res["active"] and res["cap"] == 1
    assert res["final_reg"].status(res["kept"][0]["form_id"]) == "admitted"
    assert len(res["admitted_not_kept"]) == 5 and res["forms_not_admitted"] == []
    # a dissent from one reader rejects that form for good: the next written candidate of the item is kept
    res = _stage(ra, _dissent(rr, USING, only_task=sorted(rr)[0]))
    assert _kept(res) == [(order[0], 1)]
    rejected = [c for rp in res["reports"] for c in rp["candidates"] if c.get("status") == "rejected"]
    assert [c["j"] for c in rejected] == [0] and len(res["forms_not_admitted"]) == 1
    # every candidate of item 1 dissented: the reserve item is used, in its written order
    res = _stage(ra, _dissent(_dissent(_dissent(rr, USING), WITH), MEASURED))
    assert _kept(res) == [(order[1], 0)] and len(res["forms_not_admitted"]) == 3
    # nothing admitted: nothing kept, the cell stays short
    allbad = rr
    for frag in (USING, WITH, MEASURED, AFTER, WORKING, VIEW):
        allbad = _dissent(allbad, frag)
    res = _stage(ra, allbad)
    assert res["kept"] == [] and res["final_reg"].forms.keys() == _prev_state()[0].forms.keys()
    assert len(res["forms_not_admitted"]) == 6 and all(rp["kept"] is None for rp in res["reports"])


def test_redo3_stage_needs_both_reads_and_never_passes_a_cell_over_its_target(r3_answers):
    ra, rr = r3_answers
    one_read = {tid: v for tid, v in list(rr.items())[:1]}                 # the other read is missing or audit-failed
    res = _stage(ra, one_read)
    assert res["kept"] == [] and res["problems"]                           # 1 of 2 extractors: every form stays pending
    assert {c["status"] for rp in res["reports"] for c in rp["candidates"]} == {"pending"}
    res = _stage(ra, {})
    assert res["kept"] == [] and res["problems"]
    lex, cnt = _prev_state()
    full = dict(cnt, yn_not_compliant=V.PINNED_TARGETS["wording"]["yn_not_compliant"])
    res = V.redo3_stage(ra, rr, lex, full)                                  # the cell is already at its target
    assert res["cap"] == 0 and res["kept"] == [] and len(res["admitted_not_kept"]) == 6
    assert all("reserve" in c for rp in res["reports"] for c in rp["candidates"])


def test_redo3_stage_uses_nothing_when_the_authoring_answer_is_absent_or_the_read_files_drift(r3_answers, monkeypatch):
    ra, rr = r3_answers
    res = _stage({}, rr)
    assert not res["active"] and res["kept"] == [] and "not accepted" in res["problems"][0]
    changed = copy.deepcopy(ra)
    task = next(iter(changed))
    changed[task][0]["texts"] = ["Using the card's definitions, is {SITE} not compliant with its checklist on the audit "
                                 "date now?", changed[task][0]["texts"][1], changed[task][0]["texts"][2]]
    res = _stage(changed, rr)                  # lint drops candidate 0: the reads would hold 5 forms, not the 6 on disk
    assert res["active"] and not res["reads_usable"] and res["drift"] and res["kept"] == []
    assert res["glex_reads"] == {} and any("differ" in p for p in res["problems"])


def test_redo3_baseline_check_detects_a_missing_or_changed_previous_freeze(tmp_path, monkeypatch):
    names = ("skins.json", "attacks.json", "documents.json", "wordings.json", "lexicon.json", "packs.json")
    stage5 = {n: (V.POOLS_V2_PREV / n).read_text(encoding="utf-8") for n in names}
    assert V.baseline_check(stage5)["ok"]
    monkeypatch.setattr(V, "POOLS_V2_PREV", tmp_path / "absent")
    b = V.baseline_check(stage5)
    assert not b["ok"] and not b["present"] and "pools_v2_prev" in b["problems"][0]
    copy_dir = tmp_path / "prev"
    shutil.copytree(Path(__file__).resolve().parent / "pools_v2_prev", copy_dir)
    monkeypatch.setattr(V, "POOLS_V2_PREV", copy_dir)
    assert V.baseline_check(stage5)["ok"]
    assert not V.baseline_check({**stage5, "wordings.json": stage5["wordings.json"] + " "})["ok"]     # stage 5 moved
    (copy_dir / "wordings.json").write_text(stage5["wordings.json"] + " ", encoding="utf-8")
    b = V.baseline_check(stage5)
    assert not b["ok"] and b["manifest_sha_mismatches"] == ["wordings.json"]
    # a failed baseline stops the redo3 stage in a full build: the freeze stays SHORT and the hard gate says why
    res = V.build(())
    assert not res["ready"] and res["hard_gates_ok"]["redo3_baseline_intact"] is False
    assert not res["redo3"]["active"] and [s["item"] for s in res["shortfalls"]] == [CELL3]
    assert any("baseline" in p for p in res["redo3"]["problems"])


# ------------------------------------------------------------------------------------------------ pools_v2 on disk

def test_pools_v2_on_disk_matches_a_fresh_build(built):
    if not (V.POOLS_V2 / "MANIFEST.json").exists():
        pytest.skip("pools_v2/ not written yet")
    for name, text in built["files"].items():
        assert (V.POOLS_V2 / name).read_text(encoding="utf-8") == text, name
    out = V.verify_pools_v2()
    assert out["ok"] and out["sha_mismatches"] == [] and out["manifest_sha_mismatches"] == []
    ctx, packs = V.load_pools_v2()
    man = json.loads((V.POOLS_V2 / "MANIFEST.json").read_text(encoding="utf-8"))
    assert man["status"] == built["status"] and man["ready"] == built["ready"]
    n_pieces = sum(len(json.loads((V.POOLS_V2 / f).read_text(encoding="utf-8")))
                   for f in ("skins.json", "attacks.json", "documents.json"))
    assert len(ctx.skins) == n_pieces
    assert len(packs) == man["counts"]["packs_train"] + man["counts"]["packs_held"]

"""families/T25/haiku/redo2/test_build_redo2.py: in-memory tests of build_redo2.py (nothing is written).

  B1 cross-lint   the stage-6 loader call rejects nothing; the full call (all nouns, all tier words) rejects exactly the
                  36 memo skins and 9 memo Mode F documents, all for the noun "memo"; with "memo" quarantined the same
                  call rejects nothing and the noun, register and wording targets still hold (G0 v3 section 10 B1)
  B2 registry     the only cross-match is yn_claim#3fab6dc5 reading yn_claim#adb8f647; without #3fab6dc5 every build
                  order passes every unit test and every fill reads back to its own form (B2)
  B3 G3-H tasks   84 documents in 2 chunks of 42; items carry text + schema only; names and kinds equal
                  plugin.extract_fields; no expected value, internal id or never-open path in a task file; each task
                  file names its own answer path under haiku/redo2/answers/
  B3 consumer     evaluate_g3h on SYNTHETIC in-memory extractions (a code test, never data; nothing is written): exact
                  compare, per-document quarantine, the 20% per-register cap (23 cut when all pass), label-blind order
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import build_redo2 as B  # noqa: E402

X = "q.t25.yn_claim#adb8f647"            # "... for the {ATTR} that the listed sources settle on?"  (kept)
Y = "q.t25.yn_claim#3fab6dc5"            # "... for the {ATTR} the listed sources settle on?"       (quarantined)
CUT_IF_ALL_PASS = {"memo": 3, "email": 3, "chat": 2, "ticket": 3, "faq": 4, "transcript": 4, "wiki_talk": 2,
                   "audit_note": 2}


@pytest.fixture(scope="module")
def b1():
    return B.b1_record()


@pytest.fixture(scope="module")
def b2():
    return B.b2_record()


@pytest.fixture(scope="module")
def built():
    return B.stage_a()


# ------------------------------------------------------------------------------------------------ B1
def test_b1_stage6_call_misses_the_conflict(b1):
    assert b1["stage6_call"] == {"skins": 0, "freeform": 0, "attacks": 0}
    assert b1["tier_words"] == 63 and b1["nouns_admitted"] == 94


def test_b1_full_call_flags_only_memo(b1):
    fz = B.frozen()
    memo_skins = sum(1 for s in fz["skins"] if s["register"] == "memo")
    memo_docs = sum(1 for d in fz["docs"] if d["register"] == "memo")
    assert (memo_skins, memo_docs) == (37, 12)
    assert b1["full_call"] == {"skins": 36, "freeform": 9, "attacks": 0}
    assert b1["full_call_by_kind_register"] == {"skins:memo": 36, "freeform:memo": 9}
    assert b1["nouns_named"] == {"memo": 45} and b1["reasons_other_than_a_noun"] == {}
    assert set(b1["direct_scan"]) == {fid for d in b1["full_call_rejected"].values() for fid in d}
    assert all(v == ["memo"] for v in b1["direct_scan"].values())
    assert b1["loader_missing"] == {}


def test_b1_ruling_quarantines_the_noun_not_the_register(b1):
    r = b1["ruling"]
    assert r["nouns_quarantined"] == ["memo"] and r["nouns_v3"] == 93 >= B.TARGET["source_nouns"]
    assert r["pieces_quarantined"] == 0 and len(r["training_registers_kept"]) == B.TARGET["registers"]
    assert b1["after_ruling_call"] == {"skins": 0, "freeform": 0, "attacks": 0}


def test_b1_other_pools_name_no_noun():
    fz = B.frozen()
    p = B.P
    for s in fz["attrs"] + [w["text"] for w in fz["wordings"]]:
        assert not B.noun_hits(s, fz["nouns"]), s
    for key in ("skins", "docs", "attacks"):
        for it in fz[key]:
            assert not B.noun_hits(it["text"], p.SOURCE_NAMES), it["id"]      # stand-in names collide with nothing


# ------------------------------------------------------------------------------------------------ B2
def test_b2_only_cross_match(b2):
    assert [(c["general"], c["specific"]) for c in b2["cross_matches"]] == [(Y, X)]
    assert b2["mutual"] == [] and b2["ruling"]["wordings_quarantined"] == [Y]


def test_b2_bug_reproduced_then_fixed(b2):
    assert b2["orders_failing_before"] >= 1 and set(b2["unit_fail_by_order_before"]) >= {"form_id"}
    assert all(v == [X] for v in b2["unit_fail_by_order_before"].values())
    assert "stage6" not in b2["unit_fail_by_order_before"]                  # stage 6 passed only by its order
    assert b2["fill_roundtrip_form_id_order_before"]["forms_failing"] == [X]
    assert b2["orders_failing_after"] == 0 and b2["orders"] == 3 + B.N_SHUFFLES
    assert b2["cross_matches_after"] == [] and b2["fill_roundtrip_form_id_order_after"]["failures"] == 0


def test_b2_targets_hold(b2):
    r = b2["ruling"]
    assert r["forms_v3"] == 138 >= B.TARGET["wordings_total"]
    assert min(r["per_qform_v3"].values()) >= B.TARGET["wordings_per_form"]
    assert r["per_qform_v3"]["yn_claim"] == 34 and len(r["per_qform_v3"]) == 7


# ------------------------------------------------------------------------------------------------ B3 tasks
def test_b3_batch_shape(built):
    files, rows = built
    assert [r["n_items"] for r in rows] == [42, 42] and all(r["kind"] == "extract_g3h" for r in rows)
    chunks = [json.loads(t) for rel, t in files.items() if rel.startswith("chunks/")]
    assert len(chunks) == 2
    for c in chunks:
        for it in c["items"]:
            assert set(it) == {"qid", "text", "schema"}
            assert [(f["field"], f["type"]) for f in it["schema"]] == [(f.name, f.kind)
                                                                     for f in B.P.T25.extract_fields(None, None)]


def test_b3_fields_keep_names_and_kinds():
    assert [(f.name, f.kind) for f in B.g3h_fields()] == [(f.name, f.kind) for f in B.P.T25.extract_fields(None, None)]


def test_b3_task_files_are_self_contained_and_gold_free(built):
    files, rows = built
    _b, expected = B.g3h_batch()
    assert len(expected) == 84
    task_texts = {rel: t for rel, t in files.items() if rel.startswith("tasks/")}
    assert len(task_texts) == 2
    for r in rows:
        rel = "tasks/" + Path(r["task_file"]).name
        t = task_texts[rel]
        assert r["answer_file"] in t and r["answer_file"].startswith(str(B.HERE / "answers") + "/")
        assert r["audit_allowed_read"] == [r["task_file"]] and r["audit_allowed_write"] == [r["answer_file"]]
        assert B.G3H_PROMPT in t
        for sid in expected:
            assert sid not in t                                              # no internal id
        assert not B.paths.never_open(r["task_file"]) and not B.paths.never_open(r["answer_file"])
        assert "plan/g3h_expected" not in t and "/key/" not in t


def test_b3_every_document_text_reaches_one_item(built):
    files, _rows = built
    texts = [it["text"] for rel, t in files.items() if rel.startswith("chunks/") for it in json.loads(t)["items"]]
    fz = B.frozen()
    assert sorted(texts) == sorted(d["text"] for d in fz["docs"])


# ------------------------------------------------------------------------------------------------ B3 consumer
def _synthetic(expected: dict) -> dict:
    """SYNTHETIC extractions equal to the brief facts (code test only; never written, never a read)."""
    return {sid: dict(e["expected"]) for sid, e in expected.items()}


def test_b3_consumer_all_pass_then_cap():
    _b, expected = B.g3h_batch()
    ev = B.evaluate_g3h(expected, _synthetic(expected), B.mode_t_counts())
    assert ev["pass"] == 84 and ev["quarantined_g3h"] == []
    assert {r: c["cut"] for r, c in ev["cap"].items() if c["cut"]} == CUT_IF_ALL_PASS
    assert len(ev["cut_by_cap"]) == 23 and len(ev["admitted"]) == 61
    assert all(c["mode_f_share"] <= 0.20 for c in ev["cap"].values())


def test_b3_consumer_mismatch_quarantines_only_that_document():
    _b, expected = B.g3h_batch()
    ans = _synthetic(expected)
    sid = sorted(s for s, e in expected.items() if e["register"] == "faq")[0]
    ans[sid]["attr"] = "the " + ans[sid]["attr"]                           # a kept article is a mismatch
    other = sorted(expected)[0]
    del ans[other]                                                            # an unanswered document fails too
    ev = B.evaluate_g3h(expected, ans, B.mode_t_counts())
    assert set(ev["quarantined_g3h"]) == {sid, other} and ev["pass"] == 82
    assert sid not in ev["admitted"] + ev["cut_by_cap"]
    assert ev["cap"]["faq"]["passed_g3h"] == 11 and ev["cap"]["faq"]["admitted"] == 8


def test_b3_cap_order_is_label_blind():
    _b, expected = B.g3h_batch()
    ev1 = B.evaluate_g3h(expected, _synthetic(expected), B.mode_t_counts())
    ev2 = B.evaluate_g3h(dict(reversed(list(expected.items()))), _synthetic(expected), B.mode_t_counts())
    assert ev1["admitted"] == ev2["admitted"] and ev1["cut_by_cap"] == ev2["cut_by_cap"]


def test_disk_matches_rebuild_when_written(built):
    files, _rows = built
    if not (B.HERE / "TASKS.json").exists():
        pytest.skip("stage A not written yet")
    diffs = [rel for rel, text in files.items()
             if not (B.HERE / rel).is_file() or (B.HERE / rel).read_text(encoding="utf-8") != text]
    assert diffs == []

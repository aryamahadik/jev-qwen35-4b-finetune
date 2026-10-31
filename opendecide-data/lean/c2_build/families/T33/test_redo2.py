"""families/T33/test_redo2.py: the lead redo2 rules (G0_SPEC section 7), in memory only (nothing is written)."""
from __future__ import annotations

import json

from c2_kit import chunker

from . import haiku_author as H
from . import haiku_extract_run as XR
from . import redo2 as R


def _reg_with(forms):
    reg = H.registry()
    out = {}
    for text, sem, slots in forms:
        f = reg.add(text, sem, slots=slots, source="claude", family=H.F)
        assert reg.unit_test(f.form_id), (text, f.unit_problems[:2])
        out[text] = f
    return reg, out


def test_question_meanings_quote_no_program_string():           # B5
    for m in list(H.QUESTION_SEMS.values()) + list(H.QUESTION_DECOYS.values()):
        assert XR._forbid_in(m) == [], m
    assert set(H.QUESTION_SEMS) == set(H.T.SUB_OF)


def test_clause_lint_is_the_wording_role_plus_label_words():    # B1-B4
    reg, f = _reg_with([
        ("the step is done under the log rules", "crit.finished", {}),
        ("the step made no more than {R}", "crit.max_tries", {"R": "count"}),
        ("I refunded {V} for {T}", "claim.refund", {"V": "cents", "T": "id"}),
        ("{T} was cancelled", "claim.cancel", {"T": "id"}),
        ("the duration_ms on the job's final poll is at most {D}", "crit.max_duration", {"D": "count"}),
        ("I imported a row count of {V} into {T}", "claim.import", {"V": "count", "T": "id"}),
        # must still fail: CORE relative time, a word after a count, a gold-label word, a number word, a hedge
        ("the duration_ms on the job's last poll is at most {D}", "crit.max_duration", {"D": "count"}),
        ("I imported {V} rows into {T}", "claim.import", {"V": "count", "T": "id"}),
        ("the step succeeded under the log rules", "crit.finished", {}),
        ("the result shows one amount equal to the request", "crit.amount_match", {}),
        ("I probably refunded {V} for {T}", "claim.refund", {"V": "cents", "T": "id"}),
    ])
    passes = list(f)[:6]
    for text in passes:
        assert XR.clause_lint(f[text]) == [], text
    want = {"the duration_ms on the job's last poll is at most {D}": "relative_time",
            "I imported {V} rows into {T}": "grammar", "the step succeeded under the log rules": "gold_label",
            "the result shows one amount equal to the request": "number",
            "I probably refunded {V} for {T}": "hedge"}
    for text, rule in want.items():
        assert any(v.startswith(rule) for v in XR.clause_lint(f[text])), (text, XR.clause_lint(f[text]))


def test_bulk_claims_must_name_rows():                           # B4 loader rule
    reg = H.registry()
    parts = "t33|claim|sync|r2-0".split("|")
    assert H._load_one("claims", parts, "I synced {V} to {T}", "x", "t", "p", reg) == "claim_rows_word"
    assert H._load_one("claims", parts, "I synced a row count of {V} to {T}", "x", "t", "p", reg) is None


def test_read_items_show_realistic_values():                     # B6
    reg, f = _reg_with([
        ("{T} was charged {V}", "claim.charge", {"V": "cents", "T": "id"}),
        ("I exported a row count of {V} from {T}", "claim.export", {"V": "count", "T": "id"}),
        ("the step made at most {R}", "crit.max_tries", {"R": "count"}),
        ("the final poll's duration_ms is within {D}", "crit.max_duration", {"D": "count"}),
        ("Did step {STEP} of the log meet its success criterion?", H.question_sem(H.F, "yn_step_ok"),
         {"STEP": "count"}),
    ])
    texts = [R.read_item(reg, x.form_id, seed="t")["text"] for x in f.values()]
    blob = " | ".join(texts)
    for bad in ("$0.00", "0.00 USD", " day", "INV-20419"):
        assert bad not in blob, blob
    assert "tries" in texts[2] and "seconds" in texts[3] and texts[0].startswith("acct-")
    for x in f.values():
        it = R.read_item(reg, x.form_id, seed="t")
        assert set(it["choices"]) == {s.meaning for s in reg.sems.values() if s.kind == x.kind}


def test_authoring_tasks_are_label_blind_and_self_contained():   # B2, B4
    bs = R.author_batches()
    assert {n for n, _ in bs} == {"claims", "checks"}
    n_items = 0
    for _n, b in bs:
        for c in b.chunks:
            n_items += len(c["items"])
            assert len(c["items"]) <= chunker.MAX_ITEMS
            t = R.author_task_text(c)
            assert XR._forbid_in(t) == [] and c["answer_file"] in t
            assert not any(iid in t for iid in b.key.values())
            for it in c["items"]:
                if "{D}" in it["brief"]:
                    assert "never use the word last" in it["brief"] and "final poll" in it["brief"]
                if "{V}" in it["brief"]:
                    assert "never put rows" in it["brief"] and "rows" in json.dumps(it["rules"])
    assert n_items == len(R.BULK_VERBS) * R.BULK_ITEMS_PER_VERB + R.DUR_ITEMS

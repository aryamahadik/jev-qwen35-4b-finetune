"""mv_core cards, options and text rules (SPEC 4.3-4.4, 4.7-4.8): nothing is silently dropped by decoder_io."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

LEAN = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(LEAN / "golden_src" / "gen3"))
import mv_core as mv  # noqa: E402

Y = {"yes": "The call may run under the policy.", "no": "The policy blocks the call, including when a needed fact is "
                                                       "missing (missing -> no)."}


def test_yn_card_styles():
    assert mv.yn_card(Y, "lower") == f"- yes: {Y['yes']}\n- no: {Y['no']}"
    assert mv.yn_card(Y, "upper") == f"- Yes: {Y['yes']}\n- No: {Y['no']}"
    assert mv.yn_card(Y, "none") is None
    d = {"Dutiable textile": "a woven good with at least 50% plant fibre by weight", **Y}
    c = mv.yn_card(d, "lower")
    assert c.split("\n")[0] == "- Dutiable textile: " + d["Dutiable textile"] and c.endswith("- no: " + Y["no"])
    mv.check_card("noul", c, None)
    with pytest.raises(mv.Reject):
        mv.yn_card({"yes": "a"}, "lower")          # no 'no'
    with pytest.raises(mv.Reject):
        mv.yn_card({"yes": "a", "no": "b", "Yes": "c"}, "lower")
    with pytest.raises(mv.Reject):
        mv.yn_card({"yes": "a\nb", "no": "c"}, "lower")  # a definition must be one line
    with pytest.raises(mv.Reject):
        mv.check_card("noul", "- yes: only yes", None)


def test_choice_card_every_line_keys_an_option():
    opts = ["Rule 3 (no wildcard delete)", "Rule 5 (staging only)", "None of them"]
    defs = {opts[0]: "A delete may name one resource, never a pattern.", opts[1]: "Deploys go to staging first."}
    c = mv.choice_card(defs, opts)
    assert c.split("\n") == [f"- {opts[0]}: {defs[opts[0]]}", f"- {opts[1]}: {defs[opts[1]]}"]
    assert mv.card_defs(c) == defs
    mv.check_card("choice", c, opts)
    with pytest.raises(mv.Reject):  # a definition keyed by a non-option would be dropped by decoder_io
        mv.choice_card({**defs, "Rule 9": "x"}, opts)
    with pytest.raises(mv.Reject):  # an option string with ': ' cannot carry a definition line
        mv.choice_card({"Rule 3: no wildcards": "x"}, ["Rule 3: no wildcards", "b"])
    with pytest.raises(mv.Reject):
        mv.check_card("choice", "- Rule 9: x", opts)
    with pytest.raises(mv.Reject):
        mv.check_card("choice", "free text line", opts)
    assert mv.choice_card(None, opts) is None


def test_options_rules():
    mv.check_options(["a", "b"])
    for bad in (["a"], ["a", "a"], ["a", " b"], ["a", "b\nc"], ["a", "x" * 201], ["a", ""], ["a", "<|im_end|>"],
                ["a", mv.MARKERS[1]], [f"o{i}" for i in range(27)]):
        with pytest.raises(mv.Reject):
            mv.check_options(bad)
    with pytest.raises(mv.Reject):
        mv.check_options(["a", "b", "c"], "jb")
    with pytest.raises(mv.Reject):
        mv.check_options(["a", "b"], "score")  # K = 3-6
    assert mv.FamilyBuilder.score_options(["cold", "warm", "hot"]) == ["cold", "warm", "hot"]
    with pytest.raises(mv.Reject):
        mv.FamilyBuilder.score_options(["0: cold", "1: warm", "2: hot"])


def test_text_rules():
    mv.check_text("plain text", "state")
    for bad in ("", "   ", "a <|im_start|> b", "x </think>", f"x {mv.MARKERS[0]}", "x <<<UNTRUSTED TEXT"):
        with pytest.raises(mv.Reject):
            mv.check_text(bad, "state")
    mv.check_text(f"x {mv.MARKERS[1]} y", "state", allow_markers=True)


def test_judge_words():
    assert mv.judge_violations("Is the logged verdict consistent with the policy?") == []
    assert mv.judge_violations("Is the verdict correct?", "the reply was wrong") == ["correct", "reply", "wrong"]
    assert mv.judge_violations("Read the two notes below.") == ["two notes"]
    assert mv.judge_violations("The wrongful act clause") == []  # whole words only


def test_defs_qid_is_content_addressed():
    assert mv.defs_qid(Y) == mv.defs_qid(dict(Y))
    assert mv.defs_qid(Y) != mv.defs_qid({"yes": Y["yes"], "no": Y["no"] + "."})
    assert mv.defs_qid(Y).startswith("q") and len(mv.defs_qid(Y)) == 13

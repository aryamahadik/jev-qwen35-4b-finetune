"""Unit tests for c_src/common/negcount.py (XF02). CPU, no data files.

Run:  /Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python -m pytest -q c_src/common/test_negcount.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import negcount as nc  # noqa: E402


def ks(text, **kw):
    r = nc.count(text, **kw)
    return r.k_syn, r.k_all


def entries(text, **kw):
    return [m.entry for m in nc.count(text, **kw).matches]


# ---------------------------------------------------------------- L_core words


@pytest.mark.parametrize("w", ["not", "no", "none", "nobody", "nothing", "nowhere", "never", "neither", "nor"])
def test_each_l_core_word_counts_once_in_both(w):
    assert ks(f"Is it true that {w} x applies?") == (1, 1)


def test_affirmative_question_counts_zero():
    assert ks("Is it true that the vendor filed the report on time?") == (0, 0)


def test_answer_words_and_options_are_the_callers_business():
    # the counter counts what it is given; "no" is a word wherever it appears (F5 3.4: "as 'no' does")
    assert ks("Answer yes or no.") == (1, 1)


# ---------------------------------------------------------------- contractions (R2)


@pytest.mark.parametrize("q", ["Is it true that the firm doesn't pay?", "Is it true that the firm does not pay?",
                               "Is it true that the firm isn't liable?", "Is it true that the firm won't pay?",
                               "Is it true that the firm didn't pay?", "Is it true that the firm hasn't paid?"])
def test_contracted_and_full_negation_agree(q):
    assert ks(q) == (1, 1)


@pytest.mark.parametrize("q", ["The firm cannot pay.", "The firm can not pay.", "The firm can't pay.",
                               "The firm can’t pay.", "THE FIRM CANNOT PAY."])
def test_cannot_family_is_one_l_core_token_and_one_entry(q):
    assert ks(q) == (1, 1)
    assert entries(q) == ["cannot"]


def test_curly_apostrophe_is_an_apostrophe():
    assert ks("Is it true that the firm doesn’t pay?") == (1, 1)
    assert nc.count("doesn’t").syn_tokens == ("n't",)


def test_word_without_apostrophe_is_not_a_negation():
    assert ks("The firm dont pay.") == (0, 0)


def test_other_clitics_split_off_and_do_not_count():
    assert ks("It's the firm's duty and they're paying.") == (0, 0)
    assert ks("It's not the case that the firm paid.") == (1, 1)
    assert entries("It's not the case that the firm paid.") == ["it is not the case that"]


# ---------------------------------------------------------------- comparators (R3)


@pytest.mark.parametrize("phrase", ["no fewer than", "no more than", "not less than", "not more than", "not before",
                                    "not after", "isn't more than", "no less than", "no later than",
                                    "no earlier than", "not exceeding", "does not exceed", "doesn't exceed",
                                    "did not exceed", "not equal to"])
def test_comparator_phrases_count_in_k_all_not_in_k_syn(phrase):
    assert ks(f"Is it true that the total is {phrase} 30?") == (0, 1)


def test_comparator_needs_the_whole_phrase():
    assert ks("Is it true that no fewer seats were sold?") == (1, 1)      # "no" alone (no "than")
    assert ks("Is it true that the total, no, fewer than 30?") == (1, 1)  # punctuation breaks the phrase


@pytest.mark.parametrize("q", ["no less than 3", "no later than 5 May", "no earlier than 5 May", "not exceeding 3",
                               "does not exceed 3", "doesn't exceed 3", "not equal to 3", "x is no later than y, and "
                               "z does not exceed w unless none of them is not equal to v",
                               "not exceeding other than"])
def test_comparator_aliases_are_k_all_neutral(q):
    with_alias, without = nc._count(q), nc._count(q, aliases=False)
    assert with_alias.k_all == without.k_all
    assert with_alias.k_syn <= without.k_syn


def test_comparator_and_syntactic_negation_in_one_question():
    q = "Is it true that the vendor did not ship no fewer than 3 units?"
    assert ks(q) == (1, 2)
    assert nc.count(q).syn_tokens == ("not",)


# ---------------------------------------------------------------- implicit cues and lemmas (R5)


@pytest.mark.parametrize("q", ["Did the firm fail to file?", "The firm failed to file.", "The firm fails to file.",
                               "The firm is failing to file.", "Did the firm lack a permit?", "The firm lacked a permit.",
                               "Did the firm deny that it paid?", "The firm denied it.", "The firm denies it.",
                               "The firm neglected to file.", "The firm omitted to file.", "The firm refused to file.",
                               "The firm declined to file.", "The rule prevented the firm from filing.",
                               "The board ruled out a refund.", "The board ruled it out.", "The board is ruling the "
                               "refund out.", "Did anyone other than Ana sign?", "It is false that Ana signed.",
                               "Is it false that Ana signed?", "The value is false.", "The site is free of debris.",
                               "Ana signed without a witness.", "Ana hardly signed.", "Ana scarcely signed.",
                               "Ana barely signed.", "Few members signed.", "Everyone except Ana signed.",
                               "Ana signs unless Bo objects."])
def test_implicit_cues_count_in_k_all_only(q):
    assert ks(q) == (0, 1)


@pytest.mark.parametrize("q", ["Fewer members signed.", "The fewest members signed.", "A few members signed.",
                               "The rules set out in section 2 apply.", "The firm failed.",
                               "The firm refused the offer.", "The rule prevented fraud.", "The site is free.",
                               "Did the firm manage to file?", "Ana signed before May."])
def test_near_misses_do_not_count(q):
    assert ks(q) == (0, 0)


def test_prevent_from_gap_stops_at_sentence_end():
    assert ks("The rule prevented it. From May on, all paid.") == (0, 0)


def test_rule_out_gap_is_bounded():
    assert ks("The board ruled the late refund claim out.") == (0, 0)   # 4 words between: too far
    assert ks("The board ruled the claim out.") == (0, 1)


# ---------------------------------------------------------------- multiword entries and overlap (R4, R6, R7)


@pytest.mark.parametrize("q,expect,names", [
    ("Is it not the case that this report does not get code K?", (2, 2), ["it is not the case that", "not"]),
    ("Is it true that it is not the case that Ana signed?", (1, 1), ["it is not the case that"]),
    ("Isn't it the case that Ana signed?", (1, 1), ["it is not the case that"]),
    ("Ana need not sign.", (1, 1), ["need not"]),
    ("Ana needn't sign.", (1, 1), ["need not"]),
    ("Ana must not sign.", (1, 1), ["must not"]),
    ("Ana mustn't sign.", (1, 1), ["must not"]),
    ("Ana may not sign.", (1, 1), ["may not"]),
    ("Ana is no longer a member.", (1, 1), ["no longer"]),
    ("Not only Ana but also Bo signed.", (1, 1), ["not only"]),
    ("Not both signed.", (1, 1), ["not both"]),
    ("Not every member signed.", (1, 1), ["not every"]),
    ("Not all members signed.", (1, 1), ["not all"]),
    ("Ana did not sign any form.", (1, 1), ["not"]),
    ("Not any member signed.", (1, 1), ["not any"]),
    ("None of the members signed.", (1, 1), ["none of"]),
    ("Ana is not permitted to sign.", (1, 1), ["is not permitted to"]),
    ("Ana isn't permitted to sign.", (1, 1), ["is not permitted to"]),
    ("Ana does not have to sign.", (1, 1), ["does not have to"]),
    ("Ana doesn't have to sign.", (1, 1), ["does not have to"]),
    ("Ana is not required to sign.", (1, 1), ["is not required to"]),
    ("Ana did not manage to sign.", (1, 1), ["did not manage to"]),
    ("All except Ana signed.", (0, 1), ["all except"]),
    ("Ana signs except when Bo objects.", (0, 1), ["except when"]),
    ("All except when noted.", (0, 1), ["all except"]),              # leftmost match wins, no overlap
    ("Not all except Ana signed.", (1, 2), ["not all", "except"]),
    ("Neither Ana nor Bo signed.", (1, 1), ["neither ... nor"]),               # A16: one syntactic negation
    ("Neither Ana with no pen nor Bo signed.", (2, 2), ["neither ... nor", "no"]),
    ("Neither of them signed. Nor did Cy.", (2, 2), ["neither", "nor"]),  # a sentence end splits the pair
    ("Ana signed, nor did Bo object.", (1, 1), ["nor"]),
    ("Did Ana not fail to sign?", (1, 2), ["not", "fail to"]),
    ("Is the following statement true: the claim is not false?", (1, 2), ["not", "false"]),
    ("Nobody signed nothing.", (2, 2), ["nobody", "nothing"]),
    ("Was the form signed whether or not Bo agreed?", (1, 1), ["not"]),
])
def test_multiword_and_overlap(q, expect, names):
    assert ks(q) == expect
    assert entries(q) == names


def test_matches_report_their_surface_text():
    m = nc.count("The rule PREVENTED the firm from filing.").matches
    assert [(x.entry, x.surface) for x in m] == [("prevent from", "PREVENTED ... from")]


# ---------------------------------------------------------------- case and punctuation


def test_case_is_ignored():
    assert ks("IS IT TRUE THAT NO FEWER THAN 3 ARE NOT LISTED?") == (1, 2)
    assert ks("Never.") == (1, 1)


def test_punctuation_and_quotes():
    assert ks('Is it true that the memo says "not approved"?') == (1, 1)
    assert ks("Is it true that (not) applies?") == (1, 1)
    assert ks("no; fewer than 3") == (1, 1)


def test_hyphenated_words_are_one_token():
    assert ks("Was it a no-show?") == (0, 0)
    assert ks("Is the post non-hateful?") == (0, 0)


# ---------------------------------------------------------------- SEM-18 affixed words (R8)


def test_affixed_words_count_in_k_all_only_when_declared():
    assert ks("Is it true that the firm is not non-compliant?") == (1, 1)
    assert ks("Is it true that the firm is not non-compliant?", affixed=("non-compliant",)) == (1, 2)
    assert ks("The invoice is unpaid.", affixed=("unpaid",)) == (0, 1)
    assert ks("The invoice is UNPAID.", affixed=("unpaid",)) == (0, 1)


# ---------------------------------------------------------------- referenced G0 cases


def test_g0_spec_examples():
    # F11 SEM-40 negated and double-negated frames (k_syn >= 1, >= 2)
    assert nc.k_syn("Is it true that this report does not get code K?") == 1
    assert nc.k_syn("Is it not the case that this report does not get code K?") == 2
    # F13: 'fail to establish' is an implicit cue, k_syn 0
    assert ks("Does the record fail to establish that the fee was paid?") == (0, 1)
    # COMMIT: the pass frame's 'without' counts in k_all
    assert ks("Can this change merge without a review?") == (0, 1)
    # F2: 'does not exceed' and 'fails to reach' count 1 each in k_all (F2 "cue:")
    assert nc.k_all("Does the total not exceed 30 and the score fail to reach 5?") == 2
    assert nc.k_all("Does the total does not exceed 30 and the score fails to reach 5?") == 2
    # F6 negated Q-DET frames: 'leave open whether' is not an F5 L_neg entry (reported in MARKERS.md section 5, N2)
    assert ks("Does the record leave open whether the fee was paid?") == (0, 0)
    assert ks("Is it not the case that the record leaves open whether the fee was paid?") == (1, 1)


def test_lexicon_identity_is_stable():
    assert len(nc.LEXICON_SHA256) == 64
    assert nc.lexicon()["l_core"] == list(nc.L_CORE)
    assert set(nc.L_CORE) == {"not", "n't", "no", "none", "nobody", "nothing", "nowhere", "never", "neither", "nor"}


def test_empty_and_none_text():
    assert ks("") == (0, 0)
    assert ks(None) == (0, 0)


def test_neither_nor_is_one_syntactic_negation_a16():
    """PREREG_FINAL.md A16 (MARKERS.md N1 closed): a matched 'neither ... nor' pair counts k_syn 1, k_all 1, so it cannot
    fill the k_syn >= 2 double-negation quota on its own; another L_core token in the same text still adds 1."""
    r = nc.count("Is it true that neither the buyer nor the seller signed?")
    assert (r.k_syn, r.k_all) == (1, 1) and r.syn_tokens == ("neither",)
    r = nc.count("Is it true that neither the buyer nor the seller did not sign?")
    assert (r.k_syn, r.k_all) == (2, 2)
    assert nc.count("Nor did the seller sign.").k_syn == 1                    # a lone 'nor' still counts
    assert nc.lexicon()["syn_once"] == ["neither ... nor"] and nc.VERSION == "1.1"

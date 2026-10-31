"""Span-survival checker (solver A): planted edits, the rulings (no recovery by default, AUTHORITY never recovered, negation never
recoverable), and the V-C4 harness."""
import random

import pytest

import planted as PT
import span_check as SC
import verbalizer as VB
import vcommon as V
import vgates as G

LEX = V.test_lexicon()
VBZ = VB.Verbalizer(LEX)
UTT = "Please do not delete /tmp/build with -rf on port 8080 and 25 items before 2026-03-14."


def sp(sub, role, kind):
    i = UTT.index(sub)
    return {"start": i, "end": i + len(sub), "text": sub, "role": role, "kind": kind}


SPANS = [sp("not", "negation", "negation"), sp("/tmp/build", "entity", "path"), sp("-rf", "entity", "flag"), sp("8080", "number", "number"),
         sp("25", "number", "number"), sp("2026-03-14", "number", "date")]
DOC = VBZ.verbalize(UTT, SPANS, "V-NL", random.Random(1))


def kept(h, **kw):
    return SC.check_doc(DOC, h, **kw)


def test_exact_and_equivalent_forms_survive():
    for h in [" ".join(DOC["tokens"]),
              "Please do not delete /tmp/build with -rf on p o r t 8080 and 25 items before March 14th, 2026.",
              "please don't delete slash tmp slash build with dash r f on port eight thousand eighty and twenty five items before 2026-03-14",
              "please do not delete /tmp/build with - rf on port 8080 and 25 items before 14 March 2026.",
              "uh please do not delete /tmp/build with -rf on port 8080 and 25 items uh before March fourteenth, twenty twenty six"]:
        r = kept(h)
        assert r["kept"], (h, r["reasons"])


def test_numbers_dates_entities_flags_and_negations_alterations_are_caught():
    cases = {
        "negation deleted": "please do delete /tmp/build with -rf on port 8080 and 25 items before March 14, 2026",
        "negation inserted elsewhere": "please do not delete /tmp/build with -rf on port 8080 and not 25 items before March 14, 2026",
        "number altered": "please do not delete /tmp/build with -rf on port 8081 and 25 items before March 14, 2026",
        "number longer": "please do not delete /tmp/build with -rf on port 80800 and 25 items before March 14, 2026",
        "number deleted": "please do not delete /tmp/build with -rf on port and 25 items before March 14, 2026",
        "path altered": "please do not delete /tmp/builds with -rf on port 8080 and 25 items before March 14, 2026",
        "flag altered": "please do not delete /tmp/build with -r on port 8080 and 25 items before March 14, 2026",
        "date altered": "please do not delete /tmp/build with -rf on port 8080 and 25 items before March 15, 2026",
        "second number replaced": "please do not delete /tmp/build with -rf on port 8080 and 26 items before March 14, 2026",
    }
    for name, h in cases.items():
        assert not kept(h)["kept"], name


def test_a_value_replaced_by_a_different_valid_value_is_altered_even_if_the_true_value_is_elsewhere():
    h = "please do not delete /tmp/build with -rf on port 25 and 8080 items before March 14, 2026"
    assert not kept(h)["kept"]


def test_recovery_exception_is_off_by_default_and_never_for_negation_or_authority():
    h = "please do not delete /tmp/build with -rf on port and 25 items before March 14, 2026"
    assert not kept(h)["kept"]
    assert kept(h, allow_recovery=True, recover_fn=lambda s: True)["kept"]          # ON: a deleted number is recoverable if the gold function agrees
    h2 = "please do delete /tmp/build with -rf on port 8080 and 25 items before March 14, 2026"
    assert not kept(h2, allow_recovery=True, recover_fn=lambda s: True)["kept"]     # negation is never recoverable
    auth = dict(SPANS[3], role="authority")
    d = VBZ.verbalize(UTT, [auth], "V-NL", random.Random(1))
    r = SC.check_doc(d, "please do not delete /tmp/build with -rf on port and 25 items before March 14, 2026", allow_recovery=True, recover_fn=lambda s: True)
    assert not r["kept"]


def test_contractions_in_either_direction_are_equivalent():
    d = VBZ.verbalize("please don't delete the cache folder now and later today ok yes sure", [{"start": 7, "end": 12, "text": "don't", "role": "negation", "kind": "negation"}], "V-NL", random.Random(2), check_length=False)
    assert SC.check_doc(d, "please do not delete the cache folder now and later today ok yes sure")["kept"]
    assert SC.check_doc(d, "please don't delete the cache folder now and later today ok yes sure")["kept"]
    assert not SC.check_doc(d, "please delete the cache folder now and later today ok yes sure")["kept"]


def test_hypothesis_punctuation_and_case_do_not_matter():
    assert kept("PLEASE, DO NOT DELETE /TMP/BUILD WITH -RF ON PORT 8080, AND 25 ITEMS BEFORE MARCH 14TH, 2026!")["kept"]


def test_planted_suite_recall_and_false_alarm_meet_the_bars():
    res = G.gate_c4_planted(n_alter=2000, n_benign=1200, seed=11)
    a = res["detail"]["A"]
    assert a["n_alter"] >= 2000
    assert a["recall"] >= 0.99 and a["recall_wilson_lb"] >= 0.97 and a["false_alarm"] <= 0.01, a
    assert res["passed"] is False and "not supplied" in res["detail"]["B"]          # B is a separate session


def test_gate_with_a_second_checker_reports_agreement():
    cases = PT.planted_suite(300, 200, seed=5)
    same = lambda d, h: SC.check_doc(d, h)["kept"]
    res = G.gate_c4_planted(check_b=same, cases=cases)
    assert res["detail"]["agreement"] == 1.0
    lazy = lambda d, h: True
    res2 = G.gate_c4_planted(check_b=lazy, cases=cases)
    assert not res2["passed"] and res2["detail"]["B"]["recall"] < 0.5


def test_planted_metrics_wilson_bound():
    import pool as PL
    assert PL.wilson_lower(1980, 2000) > 0.97 and PL.wilson_lower(1950, 2000) < 0.98

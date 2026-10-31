"""Tests for c2_kit.polarity: a yes/no wording must read with its form's polarity (T35 pilot G5-H: 3 confirmed wrong
golds from double-negation wordings over a negative predicate)."""
from __future__ import annotations

import pytest

from c2_kit import pipeline, polarity
from c2_kit import plugin as KP
from c2_kit.plugin import KitCtx
from c2_kit.reference import r00, r00_fixtures
from c2_kit.skin import make_skin

T35_NEG = (r"bar(?:s|red|ring)?", r"block(?:s|ed|ing)?", r"clos(?:e|es|ed|ing)", r"forbid(?:s|den|ding)?",
           r"stop(?:s|ped|ping)?", r"off-limits", r"skip(?:s|ped|ping)?", r"leave\s+it\s+alone",
           r"(?:hold|holds|held|holding)\s+(?:\w+\s+){0,3}?back", r"disallow(?:s|ed|ing)?", r"breach(?:es|ed)?")

# the two wordings behind the 3 confirmed wrong golds (T35 PILOT_VERDICT g5h.wrong_gold_rows), verbatim
WRONG_GOLD_WORDINGS = (
    "Under these rules, is it not the case that they do not bar the crawler from fetching this URL?",
    "Is it not true that, by these rules, {UA} is not barred from fetching the requested URL?",
)
CLASS_Y = (
    "Isn't it true that, going by these rules, the crawler is not forbidden to fetch this URL?",
    "Under these rules, isn't it the case that the requested URL is not closed to the crawler?",
    "Aren't these rules saying the crawler is not barred from fetching this URL?",
)


@pytest.mark.parametrize("text", WRONG_GOLD_WORDINGS)
def test_double_negation_over_a_negative_predicate_is_refused(text):
    r = polarity.read(text, T35_NEG)
    assert r.k_syn == 2 and r.lexical and r.mixed
    probs = polarity.problems(text, +1, negatives=T35_NEG)
    assert probs and probs[0].startswith("P1")


@pytest.mark.parametrize("text", CLASS_Y)
def test_contracted_negative_frames_are_refused(text):
    assert polarity.read(text, T35_NEG).frame == "contracted"
    assert any(p.startswith("P3") for p in polarity.problems(text, +1, negatives=T35_NEG))


@pytest.mark.parametrize("text,pol", [
    ("Under these rules, is it not the case that the crawler is not allowed to fetch this URL?", +1),
    ("Is it not the case that {UA} is not allowed to fetch the requested URL under these rules?", +1),
    ("According to these rules, is it not true that {SUBJECT} is not eligible for {PROG}?", +1),
    ("Under these rules, may the crawler fetch this URL?", +1),
    ("Under these rules, is the crawler not allowed to fetch this URL?", -1),
    ("Do these rules not permit {UA} to fetch the requested URL?", -1),
    ("Under these rules, must the crawler skip this URL?", -1),
    ("Under these rules, must {UA} skip this URL and leave it alone?", -1),    # coordinated: one layer
    ("Do these rules prevent the crawler from fetching this URL?", -1),       # negcount implicit cue
    ("Does the crawler lack the right to fetch this URL under these rules?", -1),
    ("Is fetching the requested URL disallowed for {UA} under these rules?", -1),
])
def test_well_formed_wordings_pass(text, pol):
    assert polarity.problems(text, pol, negatives=T35_NEG) == []


def test_parity_and_base():
    assert polarity.problems("Under these rules, may the crawler not fetch this URL?", +1)[0].startswith("P2")
    assert polarity.problems("Must the crawler skip this URL?", +1, negatives=T35_NEG)[0].startswith("P2")
    assert polarity.problems("Must the crawler skip this URL?", -1) != []          # family lexicon not given
    # a family whose positive predicate is itself phrased with one negation ("must not make the call")
    assert polarity.problems("Is the outcome that the agent must not make this call?", +1, base=1) == []
    assert polarity.problems("Is it not the case that the agent must not make this call?", -1, base=1) == []
    with pytest.raises(ValueError):
        polarity.problems("x?", 0)


def test_frames():
    f = lambda t: polarity.read(t).frame   # noqa: E731
    assert f("Is it not the case that X is not Y?") == "explicit"
    assert f("Going by the rules, is it not so that X is not Y?") == "explicit"
    assert f("Under these rules, isn't it the case that X?") == "contracted"
    assert f("As the rules are written, isn't X allowed?") == "contracted"
    assert f("Is the crawler not entitled to fetch this URL?") == "subject_not"
    assert f("Is the crawler, under these rules, not cleared to fetch this URL?") == "subject_not"
    assert f("Would an auditor not agree that nothing changes?") == "subject_not"
    assert f("Would you say it is not the case that X does not get Y?") == "plain"     # embedded clause
    assert f("Is the claim that the page asks for nothing beyond the task not true?") == "plain"
    assert f("Under the rules, the agent need not ask?") == "plain"
    strict = polarity.problems("Would an auditor not agree that nothing changes?", +1, strict_frames=True)
    assert any(p.startswith("P4") for p in strict)
    assert polarity.problems("Would an auditor not agree that nothing changes?", +1) == []


# ------------------------------------------------------------------------------------------------ plugin level

class _R00Pol(r00.R00):
    POLARITY_CHECK = True
    POLARITY_NEGATIVES = (r"manual\s+review", r"review(?:ed)?")


BAD = "Is it not the case that expense {EXPENSE_ID} does not go to manual review under this rule?"


@pytest.fixture(scope="module")
def pol_ctx():
    base = r00_fixtures.ctx()
    sk = dict(base.skins)
    sk["W-BAD-1"] = make_skin("W-BAD-1", "R00", BAD, {"EXPENSE_ID": "id"}, kind="wording", register="question",
                              qform="yn_approved")
    return KitCtx(skins=sk, lexicon=base.lexicon)


def test_opt_in_only(plugin, pol_ctx):
    assert polarity.form_problems(plugin, "yn_approved", BAD) == []           # R00 has not opted in
    assert polarity.screen(pol_ctx, plugin) == (pol_ctx, {})


def test_screen_and_form_problems(pol_ctx):
    p = _R00Pol(lexicon=pol_ctx.lexicon)
    assert polarity.form_problems(p, "yn_approved", BAD)
    assert polarity.form_problems(p, "yn_review", "Does expense {EXPENSE_ID} go to manual review under this rule?") == []
    assert polarity.form_problems(p, "ch_outcome", BAD) == []               # choice forms are not checked
    screened, bad = polarity.screen(pol_ctx, p)
    assert set(bad) == {"W-BAD-1"} and "W-BAD-1" not in screened.skins
    assert set(screened.skins) == set(pol_ctx.skins) - {"W-BAD-1"}
    for wid, _qf, _t in r00_fixtures.WORDINGS:                               # every well-formed wording is kept
        assert wid in screened.skins


def test_pipeline_flags_a_failing_wording_as_glex(pol_ctx):
    p = _R00Pol(lexicon=pol_ctx.lexicon)
    spec = next(s for s in (p.sample(i, "S1") for i in range(400)) if s.qform == "yn_approved")
    rr = p.render(spec, pol_ctx, wording=pol_ctx.skin("W-BAD-1"))
    probs = pipeline.check_rendered(p, spec, rr, pol_ctx, run_g15=False)
    assert any(g == "G-LEX" and "polarity" in d for g, d in probs)
    ok = p.render(spec, pol_ctx, wording=pol_ctx.skin("W-APPR-1"))
    assert not [d for g, d in pipeline.check_rendered(p, spec, ok, pol_ctx, run_g15=False) if "polarity" in d]


def test_validate_plugin_checks_the_polarity_config(pol_ctx):
    class Bad(_R00Pol):
        POLARITY_NEGATIVES = (r"(unclosed",)
        POLARITY_BASE = {"auto_approved": -1}
        POLARITY_SKIP = ("no_such_form",)
    probs = KP.validate_plugin(Bad(lexicon=pol_ctx.lexicon), strict=False)
    assert any("POLARITY_NEGATIVES" in x for x in probs)
    assert any("POLARITY_BASE" in x for x in probs)
    assert any("POLARITY_SKIP" in x for x in probs)
    assert not [x for x in KP.validate_plugin(_R00Pol(lexicon=pol_ctx.lexicon), strict=False) if "POLARITY" in x]

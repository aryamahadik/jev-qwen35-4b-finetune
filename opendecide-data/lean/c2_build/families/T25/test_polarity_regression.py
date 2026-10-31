"""families/T25/test_polarity_regression.py: the T35 pilot failure (3 wrong golds from "is it not the case that they do not
bar ...") applied to T25 (c2_kit.polarity; fix iteration 1). T25's G5-H found no wrong gold: all 130 wordings used by the pilot
rows read with their form's polarity. The rule is adopted as a safety net so a re-authored batch cannot add the failure:
  - the frozen pool (138 admitted wordings) loses no wording to the rule, and ctx_for() leaves the context untouched
  - the inverted and contracted shapes are refused by the rule, by the authoring check (haiku_author.check_wording) and,
    when one reaches a row, by the pipeline's G-LEX check; ctx_for() leaves it out of the pool
  - the fixture wordings (all seven forms) pass
No row is relabelled: a failing wording is quarantined and the rows are regenerated. In memory only (A37 f).

Run (from lean/c2_build):  ../../.venv/bin/python -m pytest -q families/T25/test_polarity_regression.py
"""
from __future__ import annotations

import dataclasses
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

import pilot_loaders as PL  # noqa: E402
from c2_kit import pipeline, polarity  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from families.T25 import fixtures as FX  # noqa: E402
from families.T25 import haiku_author as HA  # noqa: E402
from families.T25 import plugin as P  # noqa: E402

BAD = {   # (qform, wording): the rule that refuses it
    "inverted dneg: two 'not' over an antonym": (
        "yn_claim_dneg", "Under the stated rules, is it not the case that the claim to check is not wrong about the {ATTR}?", "P1"),
    "dneg with a contracted frame": (
        "yn_claim_dneg", "Isn't it the case that the claim to check does not match the value the stated rules settle on?", "P3"),
    "not over an antonym": (
        "yn_claim_not", "Under the stated rules, is the claim to check not incorrect for the {ATTR}?", "P1"),
    "antonym on the positive form": (
        "yn_claim", "Under the stated rules, is the claim to check wrong about the {ATTR}?", "P2"),
    "plain wording on a complement form": (
        "yn_claim_wrong", "Under the stated rules, is the claim to check right about the {ATTR}?", "P2"),
    "'differs' under a negation": (
        "yn_claim_dneg", "Is it not the case that the claim to check does not differ from the settled value under the stated rules?", "P1"),
}
GOOD = (
    ("yn_claim_dneg", "Under the stated rules, is it not the case that the claim to check does not match the value for the {ATTR} that "
                      "these sources settle on?"),
    ("yn_claim_not", "Does the claim to check not match the value the stated rules settle on from the listed sources?"),
    ("yn_claim_wrong", "Is the claim to check wrong under the stated rules and the listed sources?"),
    ("yn_claim_other", "Under the stated rules, is the value settled for the {ATTR} other than the value in the claim to check?"),
    ("yn_claim", "Under the stated rules, does the claim to check hold for the {ATTR} given the listed sources?"),
)


@pytest.fixture(scope="module")
def frozen():
    with PL.open_family("T25") as kit:
        yield kit


@pytest.mark.parametrize("what", sorted(BAD))
def test_the_failing_shapes_are_refused_by_the_rule_and_by_authoring(what):
    qform, text, rule = BAD[what]
    probs = polarity.form_problems(P.T25, qform, text)
    assert any(p.startswith(rule) for p in probs), (what, probs)
    meta = {"qform": qform, "attr": "{ATTR}" in text}
    got, v = HA.check_wording("w", text, meta, "task", "0" * 64, set())
    assert any(x.startswith("polarity " + rule) for x in v), (what, v)


@pytest.mark.parametrize("qform,text", GOOD)
def test_the_admitted_shapes_pass(qform, text):
    assert polarity.form_problems(P.T25, qform, text) == []
    meta = {"qform": qform, "attr": "{ATTR}" in text}
    _, v = HA.check_wording("w", text, meta, "task", "0" * 64, set())
    assert not [x for x in v if x.startswith("polarity")], v


def test_the_frozen_pool_loses_no_wording(frozen):
    plugin, ctx = frozen.plugin, frozen.ctx
    wordings = [s for s in ctx.skins.values() if s.kind == "wording"]
    assert len(wordings) == 138
    bad = {s.skin_id: polarity.form_problems(plugin, s.qform, s.text) for s in wordings}
    assert {k: v for k, v in bad.items() if v} == {}
    assert plugin.quarantined_wordings(ctx) == {}                  # the polarity rule quarantines nothing in the pool
    assert set(ctx.skins) - set(plugin.ctx_for(None, ctx).skins) == set(P.QUARANTINED_TEMPLATES)   # only the G5-H ones
    per_form = {}
    for s in wordings:
        per_form[s.qform] = per_form.get(s.qform, 0) + 1
    assert set(per_form) == set(P.QF) and min(per_form.values()) >= 4


def test_units_on_the_frozen_pool_are_unchanged_by_the_screen(frozen):
    plugin, ctx = frozen.plugin, frozen.ctx
    n = 0
    for smp in ("S1", "S2", "S3", "S4"):
        for seed in range(40):
            res = pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=False)
            assert res.ok and not [d for g, d in res.problems if g == "G-LEX"], res.problems
            n += 1
    assert n == 160


def _with_bad_wording(qform, text):
    c = FX.ctx()
    bad = K.make_skin("W-BAD", "T25", text, {}, kind="wording", register="question", qform=qform)
    return dataclasses.replace(c, skins={**c.skins, "W-BAD": bad}), bad


def test_ctx_for_leaves_a_failing_wording_out_and_the_pipeline_flags_one_that_reaches_a_row():
    qform, text, _ = BAD["inverted dneg: two 'not' over an antonym"]
    c2, bad = _with_bad_wording(qform, text.replace("{ATTR}", "fee"))
    plugin = P.T25(lexicon=c2.lexicon)
    left = plugin.ctx_for(None, c2)
    assert "W-BAD" not in left.skins and set(c2.skins) - set(left.skins) == {"W-BAD"}
    assert "W-BAD" in plugin.quarantined_wordings(c2)
    spec = next(sp for sp in (plugin.sample(seed, "S1") for seed in range(400)) if sp.qform == qform)
    rr = plugin.render(spec, c2)                                  # render screens: never the bad wording
    assert rr.wording_id != "W-BAD"
    forced = plugin.render(spec, c2, wording=bad)                 # forced: the safety net sees it
    probs = pipeline.check_rendered(plugin, spec, forced, c2, run_g15=False)
    assert any(g == "G-LEX" and "W-BAD" in d and "polarity" in d for g, d in probs), probs


def test_the_fixture_wordings_of_every_form_pass(frozen):
    plugin = P.T25(lexicon=FX.ctx().lexicon)
    for _wid, qf, text, _slots in FX.WORDINGS:
        assert polarity.form_problems(plugin, qf, text) == [], text


def test_the_g5h_quarantined_templates_are_never_picked(frozen):
    """Pilot 0 read each of T25-SK-yaml.021 and q.t25.yn_claim_dneg#90841882 once and one reader disagreed (a reader error,
    adjudicated gold_ok): the spec 6.3 rule quarantines them mechanically. ctx_for leaves them out; no row uses them."""
    plugin, ctx = frozen.plugin, frozen.ctx
    q = set(P.QUARANTINED_TEMPLATES)
    assert q == {"T25-SK-yaml.021", "q.t25.yn_claim_dneg#90841882"} and q <= set(ctx.skins)
    left = plugin.ctx_for(None, ctx)
    assert not q & set(left.skins) and len(left.skins) == len(ctx.skins) - 2
    words = [s for s in left.skins.values() if s.kind == "wording"]
    per_form = {}
    for s in words:
        per_form[s.qform] = per_form.get(s.qform, 0) + 1
    assert len(words) == 137 and per_form["yn_claim_dneg"] == 13 and min(per_form.values()) >= 4
    used = set()
    for smp in ("S1", "S2", "S3", "S4"):
        for seed in range(60):
            res = pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=False)
            assert res.ok, res.problems
            used |= {x for rr in res.rendered for x in (rr.skin_id, rr.wording_id)}
    assert not used & q and len(used) > 100

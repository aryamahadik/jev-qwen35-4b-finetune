"""families/T35/test_polarity_regression.py: regression for the T35 pilot G5-H failure (PILOT_VERDICT fix F1).

3 confirmed wrong golds (c2_t35:1932ab7990ec0599, ad58b20d5086e9f1, cec7bc8c2d074cca), all yn_double_neg rows worded by
T35-W-6b82356b9e / T35-W-26a82048d5: "is it not the case that they do not bar the crawler ...?" carries two 'not's
(the declared negcount profile 2/2) over a negative predicate, so it means "yes = may NOT fetch", the reverse of the
form. Root fix: the wording polarity rule (c2_kit.polarity) in the admission check (authoring.wording_problems), the
generator's wording pool (T35Plugin.ctx_for screens every render) and the pipeline's G-LEX check; the qform draw
falls back to yn_fetch while no admitted double-negation wording passes; the authoring brief names the safe shape.
No row is relabelled: the rows are regenerated. In memory only (A37 f).

Run (from lean/c2_build):  ../../.venv/bin/python -m pytest -q families/T35/test_polarity_regression.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

import pilot_loaders as PL  # noqa: E402
from c2_kit import pipeline, polarity  # noqa: E402
from families.T35 import authoring as A  # noqa: E402
from families.T35 import fixtures as FX  # noqa: E402
from families.T35 import plugin as P  # noqa: E402

WRONG_GOLD_WORDINGS = {   # the two wordings of the 3 confirmed wrong golds (frozen pools/wordings.json, verbatim)
    "T35-W-6b82356b9e": "Under these rules, is it not the case that they do not bar the crawler from fetching this URL?",
    "T35-W-26a82048d5": "Is it not true that, by these rules, {UA} is not barred from fetching the requested URL?",
}
CLASS_Y = {"T35-W-09a8f62640", "T35-W-0d03aad1d9", "T35-W-1e5bbefe85", "T35-W-3b8a541a84", "T35-W-4fdbe38ed8",
           "T35-W-519f2645ea", "T35-W-59f2ebf89a", "T35-W-5ed39baa75", "T35-W-79f576bbad", "T35-W-947bf13630"}
TRAIN = ("S1", "S2", "S3", "S4")


@pytest.fixture(scope="module")
def frozen():
    with PL.open_family("T35") as kit:
        yield kit


@pytest.mark.parametrize("wid,text", sorted(WRONG_GOLD_WORDINGS.items()))
def test_the_wrong_gold_wordings_fail_admission(wid, text):
    probs = A.wording_problems("yn_double_neg", text, "{UA}" in text)
    assert any(p.startswith("polarity P1") for p in probs), (wid, probs)
    assert polarity.form_problems(P.T35Plugin, "yn_double_neg", text)


def test_the_frozen_pool_loses_exactly_its_double_negation_wordings(frozen):
    bad = frozen.plugin.quarantined_wordings(frozen.ctx)
    dneg = {s.skin_id for s in frozen.ctx.skins.values() if s.kind == "wording" and s.qform == "yn_double_neg"}
    assert set(bad) == dneg and len(dneg) == 20 and set(WRONG_GOLD_WORDINGS) <= set(bad)
    for wid in CLASS_Y:                                          # the contracted frames, flagged on their own too
        assert any(p.startswith("P3") for p in bad[wid])
    for s in frozen.ctx.skins.values():                          # nothing else changes: no over-rejection
        if s.kind == "wording" and s.skin_id not in bad:
            assert A.wording_problems(s.qform, s.text, "UA" in dict(s.slots)) == [], s.skin_id
    assert frozen.plugin.double_neg_ok == {False: False, True: False}


def test_fixture_double_negation_shape_stays_admissible():
    for wid, qf, text, slots in FX.WORDINGS:
        assert A.wording_problems(qf, text, "UA" in slots) == [], wid
    plugin = P.T35Plugin(lexicon=FX.ctx().lexicon)
    assert plugin.double_neg_ok == {False: True, True: True}
    qforms = {plugin.sample(seed, s).qform for s in TRAIN for seed in range(300)}
    assert P.DOUBLE_NEG_FORM in qforms                           # with a clean wording the form is still drawn


def test_units_on_the_frozen_pools_never_use_a_quarantined_wording(frozen):
    plugin, ctx = frozen.plugin, frozen.ctx
    bad = plugin.quarantined_wordings(ctx)
    n_units = n_dneg_blocks = 0
    for s in TRAIN:
        for seed in range(60):
            spec = plugin.sample(seed, s)
            assert spec.qform != P.DOUBLE_NEG_FORM
            n_dneg_blocks += P.uhash(P.FAMILY, "double_neg", s, seed // 4) < P.P_DOUBLE_NEG
            res = pipeline.build_unit(plugin, spec, ctx, run_g15=False)
            assert not [d for g, d in res.problems if g == "G-LEX"], res.problems
            for rr in res.rendered:
                assert rr.wording_id not in bad
            n_units += res.ok
    assert n_dneg_blocks > 0 and n_units > 150


def test_a_quarantined_wording_that_reaches_a_row_fails_glex(frozen):
    plugin, ctx = frozen.plugin, frozen.ctx
    forced = P.T35Plugin(lexicon=ctx.lexicon)
    forced.double_neg_ok = {False: True, True: True}              # test only: draw the form the pool cannot word
    spec = next(sp for sp in (forced.sample(seed, "S1") for seed in range(800)) if sp.qform == P.DOUBLE_NEG_FORM)
    with pytest.raises(LookupError):
        forced.render(spec, ctx)                                  # the screened pool has no yn_double_neg wording
    wid = "T35-W-6b82356b9e"
    rr = forced.render(spec, ctx, wording=ctx.skin(wid))
    probs = pipeline.check_rendered(forced, spec, rr, ctx, run_g15=False)
    assert any(g == "G-LEX" and wid in d and "polarity" in d for g, d in probs)


def test_the_brief_asks_for_the_safe_shape_only():
    m = A.Q_MEANING["yn_double_neg"]
    assert "is it not the case that" in m and "contracted" in m and "bar" in m and "PERMISSION" in m
    assert not A._bad(m, A.FORBID)                               # the brief stays free of label words

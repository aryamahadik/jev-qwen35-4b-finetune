"""Tests for the plugin contract (validate_plugin, check_independence), the relation emitter (G-TW), the row schema,
and the R00 reference plugin end to end (including injected bugs that G2 / G3 / G-TW must catch). In memory only."""
from __future__ import annotations

import collections
import dataclasses
import datetime as dt

import pytest

from c2_kit import pipeline
from c2_kit import plugin as P
from c2_kit import rows as R
from c2_kit import slots as S
from c2_kit.reference import r00, r00_solver_b
from c2_kit.relations import GTWError, RelationEmitter, slot_diff

# ------------------------------------------------------------------------------------------------ contract


def test_reference_plugin_meets_the_contract(plugin):
    assert P.validate_plugin(plugin, strict=False) == []
    strict = P.validate_plugin(plugin, strict=True)
    assert any("reference family" in p for p in strict) and any("registers" in p for p in strict)


def _variant(**attrs):
    return type("R00Variant", (r00.R00,), attrs)


def test_contract_violations_are_reported(ctx):
    cases = {
        "same paradigm": dict(PARADIGM_B="ast_interpreter"),
        "unknown paradigm": dict(PARADIGM_A="vibes"),
        "samplers": dict(SAMPLERS=("S1", "S2", "S5")),
        "G0 changed": dict(G0_SHA256="0" * 64),
        "no closed-world sentence": dict(CLOSED_WORLD_SENTENCE=""),
        "no label words": dict(LABEL_WORDS=()),
        "bad exception": dict(GSL_EXCEPTIONS={"approved": "x"}),
        "solver B imports solver A": dict(SOLVER_B_MODULE="c2_kit.tests.fixture_bad_solver_b"),
        "solver B is the plugin module": dict(SOLVER_B_MODULE="c2_kit.reference.r00"),
    }
    for name, attrs in cases.items():
        probs = P.validate_plugin(_variant(**attrs)(lexicon=ctx.lexicon), strict=False)
        assert probs, name


def test_independence_check_reads_the_solver_b_source(ctx):
    bad = _variant(SOLVER_B_MODULE="c2_kit.tests.fixture_bad_solver_b")(lexicon=ctx.lexicon)
    probs = P.check_independence(bad)
    assert any("c2_kit.rules" in p for p in probs) and any("'evaluate'" in p for p in probs)
    assert P.check_independence(r00.R00(lexicon=ctx.lexicon)) == []


def test_question_forms_validate_themselves():
    with pytest.raises(P.ContractError):
        P.QuestionForm("q", "noul", "p", -1)                 # complement without its kind
    with pytest.raises(P.ContractError):
        P.QuestionForm("q", "noul", "", 1)                   # yes/no names its predicate
    with pytest.raises(P.ContractError):
        P.QuestionForm("q", "noul", "p", 1, abstain=True)    # yes/no never abstains


def test_choose_forms_is_deterministic_and_consistent_per_kind(plugin):
    spec = plugin.sample(4, "S1")
    f1, f2 = P.choose_forms(spec, "k"), P.choose_forms(spec, "k")
    assert f1 == f2
    dates = {f1[k] for k in ("PURCHASE_DATE", "RECEIPT_DATE", "FILED_DATE")}
    assert len(dates) == 1                                    # one date style per row
    for name, slot in spec.all_slots().items():
        assert f1[name] in S.free_forms(slot)


def test_spec_helpers(plugin):
    spec = plugin.sample(9, "S2")
    with pytest.raises(P.ContractError):
        spec.with_slot("AMOUNT", S.date_slot(dt.date(2026, 1, 1)))
    with pytest.raises(P.ContractError):
        spec.with_slot("ELAPSED", S.count_slot(1))           # derived slots are not inputs
    t = spec.with_slot("AMOUNT", S.cents_slot(spec.slots["AMOUNT"].value + 1))
    assert slot_diff(spec, t) == {"AMOUNT"} and t.structure_hash() != spec.structure_hash()
    assert spec.with_slot("EMPLOYEE", None).slots.keys() == spec.slots.keys() - {"EMPLOYEE"}


# ------------------------------------------------------------------------------------------------ G-TW

def _yn_spec(plugin, approved=True):
    for seed in range(500):
        s = plugin.sample(seed, "S2").replace(qform="yn_approved")
        if plugin.solve_a(s) == int(approved):
            return s
    raise AssertionError("no spec")


def test_twin_checks(plugin, ctx):
    spec = _yn_spec(plugin, approved=True)
    rr = plugin.render(spec, ctx)
    le = spec.env()["CMP"] == "cmp.le"
    over = S.cents_slot(spec.env()["LIMIT"] + (1 if le else 0))
    twin = spec.with_slot("AMOUNT", over)
    rt = plugin.render(twin, ctx, skin=ctx.skin(rr.skin_id), wording=ctx.skin(rr.wording_id), forms=rr.forms)
    em = RelationEmitter(plugin)
    em.base(rr)
    em.twin(rr, rt, spec, twin, "AMOUNT", 0)
    rows, rels = em.finalize()
    assert rows[1]["meta"]["twin_of"] == rows[0]["id"] and rows[1]["meta"]["c2"]["twin_kind"] == "minimal_edit"
    assert rows[1]["call_id"] != rows[0]["call_id"] and rows[1]["group_id"] == rows[0]["group_id"] and rels == []
    bad = {
        "wrong prediction": (twin, "AMOUNT", 1, dict()),
        "two slots": (twin.with_slot("EMPLOYEE", S.name_slot("Eve Moss")), "AMOUNT", 0, dict()),
        "other skin": (twin, "AMOUNT", 0, dict(skin=ctx.skin("SK-JSON-1" if rr.skin_id != "SK-JSON-1" else
                                                              "SK-MEMO-1"))),
        "no flip": (spec.with_slot("EMPLOYEE", S.name_slot("Eve Moss")), "EMPLOYEE", 1, dict()),
    }
    for name, (t, slot, pred, kw) in bad.items():
        r2 = plugin.render(t, ctx, skin=kw.get("skin", ctx.skin(rr.skin_id)), wording=ctx.skin(rr.wording_id),
                           forms=rr.forms)
        em = RelationEmitter(plugin)
        em.base(rr)
        with pytest.raises(GTWError):
            em.twin(rr, r2, spec, t, slot, pred)
        assert name


def test_complement_checks(plugin, ctx):
    spec = _yn_spec(plugin)
    rr = plugin.render(spec, ctx)
    for q2, w in (("yn_review", "W-REV-1"), ("yn_not_approved", "W-NOT-1")):
        s2 = spec.replace(qform=q2)
        r2 = plugin.render(s2, ctx, skin=ctx.skin(rr.skin_id), wording=ctx.skin(w), forms=rr.forms)
        em = RelationEmitter(plugin)
        em.base(rr)
        em.complement(rr, r2, spec)
        rows, rels = em.finalize()
        assert rows[0]["call_id"] == rows[1]["call_id"] and rels == [{"a": rows[0]["id"], "b": rows[1]["id"],
                                                                      "type": "complement"}]
    same = plugin.render(spec, ctx, skin=ctx.skin(rr.skin_id), wording=ctx.skin("W-APPR-2"), forms=rr.forms)
    em = RelationEmitter(plugin)
    em.base(rr)
    with pytest.raises(GTWError):
        em.complement(rr, same, spec)                         # same polarity: not a complement
    open_world = _variant(CLOSED_WORLD_SENTENCE="Nothing else is known.")(lexicon=ctx.lexicon)
    s2 = spec.replace(qform="yn_review")
    r2 = plugin.render(s2, ctx, skin=ctx.skin(rr.skin_id), wording=ctx.skin("W-REV-1"), forms=rr.forms)
    em = RelationEmitter(open_world)
    em.base(rr)
    with pytest.raises(GTWError):
        em.complement(rr, r2, spec)                           # closed-world sentence missing from the rows
    neg2 = _variant(QFORMS={**r00.R00.QFORMS, "yn_review": P.QuestionForm(
        "yn_review", "noul", "auto_approved", -1, "syntactic")})(lexicon=ctx.lexicon)
    em = RelationEmitter(neg2)
    em.base(rr)
    with pytest.raises(GTWError):
        em.complement(rr, r2, spec)                           # declared syntactic, but adds no negation cue


def test_units_hold_at_most_three_rows(plugin, ctx):
    spec = _yn_spec(plugin)
    rr = plugin.render(spec, ctx)
    em = RelationEmitter(plugin)
    em.base(rr)
    for w, q in (("W-REV-1", "yn_review"), ("W-NOT-1", "yn_not_approved")):
        em.complement(rr, plugin.render(spec.replace(qform=q), ctx, skin=ctx.skin(rr.skin_id), wording=ctx.skin(w),
                                        forms=rr.forms), spec)
    em.inv(rr, plugin.render(spec, ctx, skin=ctx.skin(rr.skin_id), wording=ctx.skin(rr.wording_id), forms=rr.forms,
                             attack=ctx.skin("AT-1")), spec)
    with pytest.raises(GTWError):
        em.finalize()


# ------------------------------------------------------------------------------------------------ rows

def test_row_schema(plugin, ctx):
    res = pipeline.build_unit(plugin, plugin.sample(3, "S1"), ctx, run_g15=False)
    row = res.rows[0]
    assert R.validate_row(row) == []
    assert R.validate_row(row, training=True) == []
    bad = {"options on yes/no": {**row, "qtype": "noul", "options": ["Yes", "No"]},
           "licence": {**row, "meta": {**row["meta"], "licence": "CC-BY"}},
           "meta.c2": {**row, "meta": {**row["meta"], "c2": {k: v for k, v in row["meta"]["c2"].items()
                                                           if k != "skin_id"}}},
           "private": {**row, "_spans": []},
           "role": {**row, "role": "twin"}}
    for name, r in bad.items():
        assert R.validate_row(r), name
    s5 = pipeline.build_unit(plugin, plugin.sample(3, "S5"), ctx, run_g15=False).rows[0]
    assert s5["meta"]["dev_only"] and R.validate_row(s5) == [] and R.validate_row(s5, training=True)
    assert R.approx_tokens(row) < R.MAX_TOKENS


# ------------------------------------------------------------------------------------------------ R00 end to end

def test_every_sampler_passes_every_program_gate(plugin, ctx):
    stats = collections.Counter()
    units = []
    for seed in range(60):
        for smp in plugin.SAMPLERS:
            res = pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=(seed < 6))
            assert res.ok, (seed, smp, res.problems)
            units.append(res)
            for r in res.rows:
                stats[(r["qtype"], r["role"])] += 1
                if smp == "S5":
                    assert r["meta"]["dev_only"]
    rep = pipeline.overlay_report(units, plugin)
    assert rep["complement_share_of_yes_no"] >= 0.20 and rep["non_syntactic_share_of_pairs"] >= 0.30
    assert 0.40 <= rep["yes_rate"] <= 0.60
    assert stats[("noul", "complement")] and stats[("noul", "twin")] + stats[("choice", "twin")]
    assert stats[("noul", "attack")] + stats[("choice", "attack")] and stats[("noul", "equiv")] + stats[
        ("choice", "equiv")]


def test_generation_is_deterministic(plugin, ctx):
    a = pipeline.build_unit(plugin, plugin.sample(17, "S4"), ctx, run_g15=False).rows
    b = pipeline.build_unit(plugin, plugin.sample(17, "S4"), ctx, run_g15=False).rows
    assert a == b


def test_wrong_options_name_their_error_models(plugin, ctx):
    seen = 0
    for seed in range(200):
        spec = plugin.sample(seed, "S1")
        if spec.qform != "ch_deadline":
            continue
        rr = plugin.render(spec, ctx)
        assert all(errs for errs in rr.row["meta"]["opt_err"].values())
        assert set().union(*map(set, rr.row["meta"]["opt_err"].values())) <= {"count_day0", "off_by_one_late",
                                                                               "wrong_anchor"}
        seen += 1
    assert seen > 20


def _failures(plugin, ctx, n=40):
    out = collections.Counter()
    for seed in range(n):
        for smp in ("S1", "S2"):
            res = pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=False)
            for g, _ in res.problems:
                out[g] += 1
    return out


def test_g2_catches_a_solver_b_boundary_bug(plugin, ctx, monkeypatch):
    monkeypatch.setitem(r00_solver_b.AMOUNT_TEST, "cmp.le", lambda diff: diff < 0)       # "at most" read as strict
    assert _failures(plugin, ctx)["G2"] > 0


def test_g2_catches_a_generator_gold_bug(plugin, ctx, monkeypatch):
    monkeypatch.setitem(r00.CMP_OP, "cmp.lt", "<=")                                        # solver A off by one
    assert _failures(plugin, ctx)["G2"] > 0


def test_g3_catches_a_renderer_that_prints_the_wrong_fact(plugin, ctx, monkeypatch):
    monkeypatch.setattr(r00, "RECORD_TPL", r00.RECORD_TPL.replace("- claim filed: {FILED_DATE}",
                                                                  "- claim filed: {RECEIPT_DATE}"))
    f = _failures(plugin, ctx)
    assert f["G3"] > 0


def test_g2_catches_a_mislabelled_option_text(plugin, ctx, monkeypatch):
    monkeypatch.setitem(r00.VERDICT_TEXT, "approve", "Manual review")
    monkeypatch.setitem(r00.VERDICT_TEXT, "review", "Auto-approved")
    assert _failures(plugin, ctx)["G2"] > 0


def test_gtw_catches_a_wrong_twin_prediction(plugin, ctx, monkeypatch):
    real = r00._answer_for
    monkeypatch.setattr(r00, "_answer_for", lambda q, ok: real(q, not ok))
    assert _failures(plugin, ctx)["G-TW"] > 0


def test_gsl_catches_a_leaky_skin(plugin, ctx):
    leaky = dataclasses.replace(ctx.skin("SK-CHAT-1"), skin_id="SK-LEAK", text=ctx.skin("SK-CHAT-1").text +
                                " It was approved already.")
    c2 = dataclasses.replace(ctx, skins={**ctx.skins, "SK-LEAK": leaky})
    spec = plugin.sample(5, "S1")
    rr = plugin.render(spec, c2, skin=leaky)
    probs = pipeline.check_rendered(plugin, spec, rr, c2, run_g15=False)
    assert any(g == "G-SL" for g, _ in probs)


def test_lexicon_gate_blocks_unadmitted_forms(plugin):
    from c2_kit.reference import r00_fixtures
    ctx0 = r00_fixtures.ctx(admit=False)
    with pytest.raises(P.ContractError):
        r00.R00(lexicon=ctx0.lexicon).sample(1, "S1")         # no admitted comparator form to draw


def test_glex_blocks_rows_with_rejected_forms_or_mismatched_wordings(plugin):
    from c2_kit.reference import r00_fixtures
    c = r00_fixtures.ctx()
    spec = plugin.sample(2, "S1").replace(qform="yn_approved")
    rr = plugin.render(spec, c, wording=c.skin("W-APPR-1"))
    assert pipeline.lex_problems(spec, rr, c) == []
    fid = c.skin("W-APPR-1").lexicon_ids[0]
    c.lexicon.record_extraction(fid, "haiku:dissent", "q.r00.yn_review")       # one disagreement rejects it
    assert any(g == "G-LEX" for g, _ in pipeline.check_rendered(plugin, spec, rr, c, run_g15=False))
    c2 = r00_fixtures.ctx()
    wrong = dataclasses.replace(c2.skin("W-APPR-2"), qform="yn_review")        # claims another meaning
    rr2 = plugin.render(spec.replace(qform="yn_review"), c2, wording=wrong)
    assert any("not an admitted" in p for _, p in pipeline.lex_problems(spec.replace(qform="yn_review"), rr2, c2))

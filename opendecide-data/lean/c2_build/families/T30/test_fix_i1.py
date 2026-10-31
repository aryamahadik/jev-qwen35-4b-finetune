"""families/T30/test_fix_i1.py: tests for T30 fix iteration 1 (PILOT_VERDICT F1-F4, kit choiceplan / cards / polarity).

In memory only (A37 f): rows are built and dropped. Covers the display plans (ch_next stop as the abstain-role option,
ch_target 1/k bands, length rank), the twin mix, the two distinct names, the rules in row.card, the shorter card (kept
meaning markers against the v2 phrasing), the length bar and the polarity quarantine of the frozen wordings.

Run (from lean/c2_build):  ../../.venv/bin/python -m pytest -q families/T30/test_fix_i1.py
"""
from __future__ import annotations

import collections
import dataclasses
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

import pilot_loaders as PL  # noqa: E402
from c2_kit import cards, pipeline, polarity  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit import rows as R  # noqa: E402
from c2_kit.choiceplan import ChoicePlan  # noqa: E402
from families.T30 import authoring as A  # noqa: E402
from families.T30 import fixtures as FX  # noqa: E402
from families.T30 import plugin as T  # noqa: E402
from families.T30 import solver_b as B  # noqa: E402

TRAIN = ("S1", "S2", "S3", "S4")
YN = tuple(q for q, f in T.T30Plugin.QFORMS.items() if f.qtype == "noul")
QUARANTINED = {   # the two yn_not_proceed wordings of the frozen pool that mix a contracted frame with "hold off" (P3, P1)
    "Shouldn't the agent hold off on this by itself?",
    "Shouldn't the agent just hold off on doing this itself?",
}


@pytest.fixture(scope="module")
def ctx():
    return FX.ctx()


@pytest.fixture(scope="module")
def plugin(ctx):
    return T.T30Plugin(lexicon=ctx.lexicon)


@pytest.fixture(scope="module")
def frozen():
    with PL.open_family("T30") as kit:
        yield kit


# ------------------------------------------------------------------------------------------------ F2: the card

V2_ITEMS = (   # the frozen v2 phrasing (contact pack), the baseline the v3 words are compared with
    ("match", "Match: an entry matches only if its first name is exactly the name in the request, letter for letter; "
              "nicknames, short or long forms and spelling variants do not match."),
    ("identity", "Identity: entries whose email values are identical, {NORM}, are one contact and count once; entries "
                 "with different email values are different contacts, whatever their other fields say."),
    ("consequence", 'Consequence: low-consequence actions are "a", "b" and "c"; consequential actions are "d", "e" '
                    'and "f".'),
    ("decision", "Decision: no distinct match: stop and tell the user nothing matched. Exactly one distinct match: go "
                 "ahead, for a low-consequence or a consequential action. Two or more distinct matches: for a "
                 "consequential action, ask the user which one is meant; for a low-consequence action, go ahead on "
                 "all of them if the number of distinct matches is at most {BATCH_MAX}, otherwise ask."),
    ("dates", "Dates are for reference only and never change the decision."),
)


def test_card_v3_keeps_every_marker_of_v2():
    """Every slot, quoted phrase, number, operator word and the negation count of a v2 rule survive in the v3 words;
    the one allowed difference is the word "only" of the dates filler ("for reference only"), which states no rule."""
    spec = T.card_spec("contact")
    assert spec.problems() == []
    new = {it.item_id: it.full for it in spec.items}
    cons_new = new["consequence"].replace("<", "").replace(">", "")
    assert [i for i, _ in V2_ITEMS] == [it.item_id for it in spec.items]
    for item_id, old in V2_ITEMS:
        old_f = old.replace('"a", "b" and "c"', T._quoted(T.TYPES["contact"].low)).replace(
            '"d", "e" and "f"', T._quoted(T.TYPES["contact"].cons))
        probs = cards.variant_problems(old_f, new[item_id])
        if item_id == "dates":
            assert probs == ["operator words differ (dropped ['only'], added [])"], probs
        else:
            assert probs == [], (item_id, probs)
    assert cons_new == new["consequence"]
    assert T.card_template("contact").startswith("Rules for a request that names a contact:\n- Match: ")
    assert T.card_template("contact").endswith(T.CLOSED_WORLD)
    # shorter than the v2 card for every record type (rebuilt here from the frozen v2 wording)
    for key, rt in T.TYPES.items():
        noun, pl = rt.noun
        v2 = ("Rules for a request that names " + K.article(noun) + " " + noun + ":\n- Match: an entry matches only if its "
              + rt.labels[0] + " is exactly the name in the request, letter for letter; nicknames, short or long forms "
              "and spelling variants do not match.\n- Identity: entries whose " + rt.labels[2] + " values are "
              "identical, {NORM}, are one " + noun + " and count once; entries with different " + rt.labels[2]
              + " values are different " + pl + ", whatever their other fields say.\n- Consequence: low-consequence "
              "actions are " + T._quoted(rt.low) + "; consequential actions are " + T._quoted(rt.cons) + ".\n"
              "- Decision: no distinct match: stop and tell the user nothing matched. Exactly one distinct match: go "
              "ahead, for a low-consequence or a consequential action. Two or more distinct matches: for a "
              "consequential action, ask the user which one is meant; for a low-consequence action, go ahead on all of "
              "them if the number of distinct matches is at most {BATCH_MAX}, otherwise ask.\n- Dates are for "
              "reference only and never change the decision.\nThe search results are complete, and only these rules "
              "decide what the agent does.")
        assert len(T.card_template(key)) <= len(v2) - 90, (key, len(v2) - len(T.card_template(key)))


def test_rules_sit_in_row_card_on_yes_no_rows_and_in_the_instructions_on_choice_rows(plugin, ctx):
    seen = collections.Counter()
    for seed in range(60):
        for smp in plugin.SAMPLERS:
            spec = plugin.sample(seed, smp)
            rr = plugin.render(spec, ctx)
            row = rr.row
            rules, question = cards.split_rules(row)
            assert rules.startswith("Rules for a request that names ") and rules.endswith(T.CLOSED_WORLD)
            assert "Rules for a request" not in question and "\n" not in question
            wording = ctx.skin(row["meta"]["wording_id"])
            if row["qtype"] == "noul":
                assert row["card"] == rules and row["instructions"] == question
                assert row["meta"]["defs_style"] == "rules_in_card_full"
            else:
                assert not row["card"] and row["instructions"] == rules + "\n\n" + question
                assert row["meta"]["defs_style"] == "rules_in_instructions_full"
            assert question == wording.text
            seen[row["qtype"]] += 1
            view = plugin.parse(row, ctx)
            assert plugin.solve_b(view) == plugin.solve_a(spec)
    assert set(seen) == {"noul", "choice"}


def test_family_mean_is_under_the_800_token_bar(plugin, ctx):
    rows = []
    for seed in range(300):
        for smp in TRAIN:
            res = pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=False)
            assert res.ok, res.problems[:2]
            rows += res.rows
    rep = cards.token_report(rows)
    assert rep["max"] <= 2000
    if rep["counted_by"].startswith("mixer.token_counts"):          # the pinned Qwen3.5 tokenizer (spec 3.0 bar)
        assert rep["mean"] <= 800, rep
        assert 0.40 <= rep["yes_no_share"] <= 0.58
    else:
        assert rep["mean"] <= 1000, rep                               # 3 chars per token, conservative


# ------------------------------------------------------------------------------------------------ F1: display plans

def test_ch_next_plan_cells_hold_their_shares_on_any_run_of_seeds():
    cells = collections.Counter()
    for smp in TRAIN:
        for seed in range(900000, 900500):
            plan = T.choice_plan(seed, smp, "ch_next")
            assert isinstance(plan, ChoicePlan) and plan.closed == 2
            cells[(plan.k, "stop" if plan.gold_abstain else ("p" if T._weyl(seed, smp, T.W_GOLD)
                                                              < (2 / 3 if plan.show_abstain else 0.5) else "a"))] += 1
    n = sum(cells.values())
    assert abs(sum(v for (k, _), v in cells.items() if k == 3) / n - T.SHOW_STOP) <= 0.02
    assert abs(sum(v for (_, g), v in cells.items() if g == "stop") / n - T.SHOW_STOP / 3) <= 0.02   # 18% of bases
    for k in (2, 3):
        tot = sum(v for (kk, _), v in cells.items() if kk == k)
        for g in (("p", "a") if k == 2 else ("p", "a", "stop")):
            assert abs(cells[(k, g)] / tot - 1 / k) <= 0.02, (k, g, cells)                          # 1/k in each cell
    assert T.choice_plan(5, "S1", "yn_proceed") is None


def test_ch_target_plan_cells_hold_their_shares_on_any_run_of_seeds():
    cells = collections.Counter()
    ranks = collections.defaultdict(collections.Counter)
    for smp in TRAIN:
        for seed in range(900000, 902000):
            plan = T.choice_plan(seed, smp, "ch_target")
            cells[(plan.k, plan.show_abstain, plan.gold_abstain)] += 1
            if plan.rank is not None:
                ranks[(plan.k, plan.show_abstain)][plan.rank] += 1
    for k in (3, 4):
        shown = cells[(k, True, True)] + cells[(k, True, False)]
        assert abs(cells[(k, True, True)] / shown - 1 / k) <= 0.02, (k, cells)
        assert cells[(k, False, True)] == 0                                                         # hidden: never gold
        for cell, cnt in ranks.items():
            n = sum(cnt.values())
            assert all(abs(c / n - 1 / len(cnt)) <= 0.03 for c in cnt.values()), (cell, cnt)
    tot = sum(cells.values())
    none = sum(v for (_, _, g), v in cells.items() if g) / tot
    assert abs(none - T.SHOW_TARGET * (1 / 3 + 1 / 4) / 2) <= 0.012, none                           # 20.4% of ch_target


def test_ch_next_gold_is_the_plan_and_stop_is_the_abstain_role(plugin, ctx):
    seen = collections.Counter()
    for seed in range(400):
        for smp in TRAIN:
            spec = plugin.sample(seed, smp)
            if spec.qform != "ch_next":
                continue
            plan = T.choice_plan(seed, smp, "ch_next")
            rr = plugin.render(spec, ctx)
            os_ = rr.option_set
            assert (rr.answer == T.STOP_KEY) == plan.gold_abstain
            assert len(os_.options) == plan.k and os_.abstain_shown == plan.show_abstain
            stop = [o for o in os_.options if o.key == T.STOP_KEY]
            assert bool(stop) == plan.show_abstain and (not stop or stop[0].role in ("abstain", "gold"))
            assert {o.key for o in os_.options} >= set(T.CLOSED_STEPS)
            seen[(plan.k, rr.answer)] += 1
    assert seen[(3, "stop")] >= 25 and seen[(2, "proceed")] >= 40 and seen[(2, "ask")] >= 40


# ------------------------------------------------------------------------------------------------ F3: twin mix

def test_twins_never_move_a_gold_onto_a_hidden_option_and_share_the_cell(plugin, ctx):
    flows = collections.Counter()
    for seed in range(1500):
        for smp in TRAIN:
            spec = plugin.sample(seed, smp)
            if spec.qform not in ("ch_next", "ch_target"):
                continue
            plan = T.choice_plan(seed, smp, spec.qform)
            for prop in plugin.relations(spec):
                if prop.kind != "twin":
                    continue
                base, want = plugin.solve_a(spec), prop.expect
                assert plan.show_abstain or want not in (T.STOP_KEY, T.NONE_KEY)                    # hidden stays hidden
                if spec.qform == "ch_target":
                    assert plan.show_abstain                                                        # no twin of a hidden base
                flows[(spec.qform, plan.k, base, want)] += 1
    for k in (2, 3):
        gold = collections.Counter()
        for (q, kk, _g, w), v in flows.items():
            if q == "ch_next" and kk == k:
                gold[w] += v
        n = sum(gold.values())
        assert n >= 150, (k, gold)
        for w, v in gold.items():
            assert abs(v / n - 1 / k) <= 0.09, (k, dict(gold))             # the twins' own gold shares: about 1/k each
    assert len({kk for (q, kk, *_r) in flows if q == "ch_target"}) == 2


def test_yes_no_twins_are_half_yes_per_form(plugin):
    """A form's twins flip yes <-> no, and the easier direction is thinned to the harder one's reach (YN_REACH), so
    each form's twins are about half yes and the pooled twins are too."""
    by = collections.defaultdict(lambda: [0, 0])
    for seed in range(2500):
        for smp in TRAIN:
            spec = plugin.sample(seed, smp)
            if spec.qform not in YN:
                continue
            for prop in plugin.relations(spec):
                if prop.kind == "twin":
                    by[spec.qform][0] += prop.expect
                    by[spec.qform][1] += 1
    assert set(by) == set(YN)
    for q, (yes, n) in by.items():
        assert n >= 120 and abs(yes / n - 0.5) <= 0.10, (q, yes, n)
    assert abs(sum(v[0] for v in by.values()) / sum(v[1] for v in by.values()) - 0.5) <= 0.03


# ------------------------------------------------------------------------------------------------ F4: names

def test_every_listing_shows_exactly_two_distinct_names_whatever_the_answer(plugin):
    by_step = collections.defaultdict(collections.Counter)
    for seed in range(600):
        for smp in plugin.SAMPLERS:
            spec = plugin.sample(seed, smp)
            f = T.facts(spec)
            names = {e.name for e in f.entries}
            assert len(names) == 2, (seed, smp, sorted(names), spec.qform)
            by_step[T._decide(len(T._groups(f.entries, f.ref, f.norm)), f.cls, f.b)][len(f.entries)] += 1
            assert len(f.entries) >= 3 and (f.cls != "low" or len(f.entries) >= f.b + 2)
            if len(names) == 2 and not f.ref in names:
                pass
    # the listing size carries no answer: its mean is the same for proceed, ask and stop (label-blind draws)
    means = {s: sum(k * v for k, v in c.items()) / sum(c.values()) for s, c in by_step.items()}
    assert max(means.values()) - min(means.values()) <= 0.45, means


def test_class_and_limit_are_drawn_before_the_answer(plugin):
    cell = collections.Counter()
    for seed in range(1500):
        for smp in TRAIN:
            spec = plugin.sample(seed, smp)
            f = T.facts(spec)
            step = T._decide(len(T._groups(f.entries, f.ref, f.norm)), f.cls, f.b)
            cell[(step, f.cls)] += 1
            cell[(step, "b", f.b)] += 1
    for step in T.STEPS:
        n = cell[(step, "low")] + cell[(step, "cons")]
        assert 0.40 <= cell[(step, "low")] / n <= 0.60, step
        assert 0.12 <= cell[(step, "b", 1)] / n <= 0.22 and 0.36 <= cell[(step, "b", 3)] / n <= 0.44, step


# ------------------------------------------------------------------------------------------------ polarity (kit item 3)

def test_the_frozen_pool_loses_exactly_two_wordings_to_the_polarity_rule(frozen):
    plugin, ctx = frozen.plugin, frozen.ctx
    bad = plugin.quarantined_wordings(ctx)
    assert {ctx.skin(i).text for i in bad} == QUARANTINED
    for sid, probs in bad.items():
        assert ctx.skin(sid).qform == "yn_not_proceed"
        assert any(p.startswith("P3") for p in probs) and any(p.startswith("P1") for p in probs)
    screened = plugin.ctx_for(None, ctx)
    assert not set(bad) & set(screened.skins) and len(screened.skins) == len(ctx.skins) - 2
    for s in screened.skins.values():                                   # nothing else is rejected
        if s.kind == "wording":
            assert polarity.form_problems(plugin, s.qform, s.text) == [], s.skin_id


def test_no_row_on_the_frozen_pools_uses_a_quarantined_wording(frozen):
    plugin, ctx = frozen.plugin, frozen.ctx
    bad = set(plugin.quarantined_wordings(ctx))
    used = collections.Counter()
    for smp in TRAIN:
        for seed in range(100):
            res = pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=False)
            assert res.ok, res.problems[:2]
            for r in res.rows:
                used[r["meta"]["wording_id"]] += 1
    assert not bad & set(used) and sum(used.values()) > 600
    assert any(ctx.skin(w).qform == "yn_not_proceed" for w in used)


def test_authoring_refuses_the_quarantined_wordings_and_the_safe_shapes_stay(plugin):
    for text in QUARANTINED:
        probs = A.check_wording(text, "yn_not_proceed")
        assert any(p.startswith("polarity P3") for p in probs) and any(p.startswith("polarity P1") for p in probs)
    for qf, text in (("yn_not_proceed", "Should the agent not carry this out on its own?"),
                     ("yn_not_proceed", "Is acting alone on this something the agent should not do?"),
                     ("yn_no_hold", "Is it true that the agent need not ask the user and need not stop?"),
                     ("yn_proceed", "Can the agent go ahead with this request on its own?"),
                     ("yn_ask", "Does the agent have to ask the user which entry is meant?")):
        assert A.check_wording(text, qf) == [], text
    assert polarity.form_problems(plugin, "yn_proceed", "Does the agent hold back from this request on its own?")
    rules = " ".join(A.WORDING_RULES_ALL)                       # the brief names the safe shape (kit item 3)
    assert "contracted negative" in rules and "hold off" in rules
    brief = A.WORDING_FORMS["yn_not_proceed"][0]                # asks for "should NOT carry out", forbids the verbs
    assert "should NOT carry out" in brief and "should hold back" not in brief and "never a verb" in brief


def test_pipeline_flags_a_quarantined_wording_that_reaches_a_row(plugin, ctx):
    """The G-LEX safety net: a wording that breaks the rule and is forced onto a row fails G-LEX."""
    bad = dataclasses.replace(ctx.skin("W-NOTGO-1"), skin_id="W-BAD", text="Shouldn't the agent hold off on this by "
                                                                          "itself?")
    c2 = type(ctx)(skins={**ctx.skins, bad.skin_id: bad}, lexicon=ctx.lexicon)
    spec = next(plugin.sample(s, "S1") for s in range(300) if plugin.sample(s, "S1").qform == "yn_not_proceed")
    rr = plugin.render(spec, c2, wording=bad)
    probs = polarity.row_problems(plugin, spec, rr, c2)
    assert probs and probs[0][0] == "G-LEX"


# ------------------------------------------------------------------------------------------------ determinism

def test_rows_do_not_depend_on_the_order_the_plan_was_asked_in(plugin, ctx):
    a = [plugin.render(plugin.sample(s, "S2"), ctx).row for s in range(30)]
    for s in reversed(range(30)):
        T.choice_plan(s, "S2", "ch_next")
    b = [plugin.render(plugin.sample(s, "S2"), ctx).row for s in range(30)]
    assert a == b
    assert all(R.validate_row(r) == [] for r in a)
    assert B.CLOSED == T.CLOSED_WORLD

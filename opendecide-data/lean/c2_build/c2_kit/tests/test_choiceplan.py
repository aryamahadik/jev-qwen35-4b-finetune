"""Tests for c2_kit.choiceplan and the planned paths of distractors.build_options / build_closed (pilot lesson: the
abstain option was gold far below 1/k, failing G6 options-only, G7 and G10 longest-option in 9 families)."""
from __future__ import annotations

import random

import pytest

from c2_kit import choiceplan as CP
from c2_kit import distractors as D

NONE = ("none", "No listed line applies to this request (so the default holds)")


def _models(outs: dict):
    return {k: D.error_model(k, (lambda v: (lambda spec: v))(v), "" if k in D.CATALOG else f"test model {k}")
            for k, v in outs.items()}


# ------------------------------------------------------------------------------------------------ the plan itself

def test_plan_is_a_function_of_the_row_key_only():
    for i in range(200):
        a = CP.plan_choice(f"r{i}", ks=(3, 4), abstain=True)
        b = CP.plan_choice(f"r{i}", ks=(3, 4), abstain=True)
        assert a == b and CP.ChoicePlan.from_json(a.to_json()) == a
        assert a.pos == D.gold_position(f"r{i}", a.k)                     # the kit's usual label-blind position
        assert a.rank is None if a.gold_abstain else a.rank == D.target_rank(f"r{i}", a.k - 1)


def test_abstain_gold_share_is_one_over_k_per_cell():
    n = {3: [0, 0], 4: [0, 0]}
    for i in range(12000):
        p = CP.plan_choice(f"key-{i}", ks=(3, 4), abstain=True)
        n[p.k][0] += 1
        n[p.k][1] += p.gold_abstain
        assert p.show_abstain and p.abstain_share == pytest.approx(1 / p.k)
    for k, (rows, ab) in n.items():
        assert CP.binom_two_sided(ab, rows, 1 / k) > 0.001, (k, ab / rows)
    assert abs(n[3][0] / 12000 - 0.5) < 0.03


def test_show_rate_and_cells():
    cells = {}
    for i in range(8000):
        p = CP.plan_choice(f"s{i}", ks=(4,), abstain=True, show_rate=0.6)
        c = cells.setdefault(p.show_abstain, [0, 0])
        c[0] += 1
        c[1] += p.gold_abstain
        assert p.show_abstain or not p.gold_abstain
    assert cells[False][1] == 0
    assert abs(cells[True][0] / 8000 - 0.6) < 0.03
    assert CP.binom_two_sided(cells[True][1], cells[True][0], 0.25) > 0.001


def test_share_bounds_and_options():
    assert CP.share_for(4) == 0.25 and CP.share_for(3, 0.2) == 0.2 and CP.share_for(5, lambda k: 1 / (k + 1)) == 1 / 6
    with pytest.raises(ValueError):
        CP.share_for(2, 0.6)                                          # spec 3.0: abstain wrong on >= 50% of showings
    with pytest.raises(ValueError):
        CP.plan_choice("x", ks=(2,), abstain=True)                    # gold + abstain + no error option
    with pytest.raises(ValueError):
        CP.plan_choice("x", abstain_slot="middle")
    p = CP.plan_choice("x", ks=(3,), abstain=False)
    assert not p.show_abstain and not p.gold_abstain and p.abstain_share == 0.0 and p.rank is not None


def test_closed_plan_k_follows_the_display():
    for i in range(300):
        p = CP.plan_choice(f"c{i}", closed=3, abstain=True, show_rate=0.5)
        assert p.k == 3 + int(p.show_abstain)


def test_closed_twin_whose_gold_becomes_abstain_grows_the_set_by_one():
    key = next(f"c{i}" for i in range(500) if not CP.plan_choice(f"c{i}", closed=3, abstain=True,
                                                                  show_rate=0.5).show_abstain)
    plan = CP.plan_choice(key, closed=3, abstain=True, show_rate=0.5)
    cs = D.build_closed(None, NONE[0], ["allow", "ask", "deny"], {}, row_key=key, render_key=str.title,
                        abstain=NONE, plan=plan, strict_plan=False)
    assert len(cs.options) == 4 and cs.gold.key == NONE[0] and cs.meta["plan"]["k"] == 4
    with pytest.raises(CP.PlanMismatch):
        D.build_closed(None, NONE[0], ["allow", "ask", "deny"], {}, row_key=key, render_key=str.title,
                       abstain=NONE, plan=plan)


def test_abstain_last_keeps_every_position_uniform():
    counts = [0] * 4
    for i in range(16000):
        p = CP.plan_choice(f"L{i}", ks=(4,), abstain=True, abstain_slot="last")
        counts[p.pos] += 1
        assert p.gold_abstain == (p.pos == 3)
    assert CP.chi2_uniform_p(counts) > 0.001, counts


# ------------------------------------------------------------------------------------------------ build_options

def test_planned_build_equals_the_unplanned_call_it_replaces():
    """plan=plan_choice(key, ks, abstain=True) + length_balance gives exactly the options of the T35-style call
    build_options(k=option_count(key), show_abstain=True, order_key=(len, text)) when the gold agrees with the plan."""
    rng = random.Random(7)
    for i in range(400):
        key = f"row-{i}"
        plan = CP.plan_choice(key, ks=(3, 4), abstain=True)
        lines = [("L%d" % j) + "x" * rng.randint(1, 30) for j in range(7)]
        gold = NONE[0] if plan.gold_abstain else lines[0]
        ms = _models({f"m{j}": lines[j] for j in range(1, 7)} | {"m0": lines[0]})
        new = D.build_options(None, gold, ms, row_key=key, render_key=str, abstain=NONE, plan=plan,
                              length_balance=True)
        old = D.build_options(None, gold, ms, k=plan.k, row_key=key, render_key=str, abstain=NONE, show_abstain=True,
                              order_key=lambda a: (len(a), a))
        if old is None:
            assert new is None
            continue
        assert new.texts == old.texts and new.gold_index == old.gold_index == plan.pos
        assert new.meta["gold_rank"] == old.meta["gold_rank"] == plan.rank


def test_strict_plan_refuses_a_gold_that_disagrees():
    ms = _models({"m1": "a", "m2": "bb", "m3": "ccc", "m4": "dddd"})
    key = next(f"k{i}" for i in range(500) if CP.plan_choice(f"k{i}", ks=(4,), abstain=True).gold_abstain)
    plan = CP.plan_choice(key, ks=(4,), abstain=True)
    with pytest.raises(CP.PlanMismatch):
        D.build_options(None, "eeeee", ms, row_key=key, render_key=str, abstain=NONE, plan=plan)
    os_ = D.build_options(None, "eeeee", ms, row_key=key, render_key=str, abstain=NONE, plan=plan,
                          strict_plan=False, length_balance=True)               # a twin: the gold came from the edit
    assert os_ is not None and len(os_.options) == 4 and os_.abstain_shown and os_.gold.key == "eeeee"
    assert not os_.meta["gold_is_abstain"] and os_.meta["plan"]["rank"] is not None
    with pytest.raises(ValueError):
        D.build_options(None, "eeeee", ms, k=3, row_key=key, render_key=str, abstain=NONE, plan=plan,
                        strict_plan=False)                                       # k comes from the plan
    with pytest.raises(ValueError):
        D.build_options(None, "eeeee", ms, k=4, row_key=key, render_key=str, abstain=NONE, order_key=len,
                        length_balance=True)                                     # one order per row


def test_twin_partner_shows_the_abstain_option_when_its_gold_is_abstain():
    ms = _models({"m1": "a", "m2": "bb", "m3": "ccc"})
    key = next(f"t{i}" for i in range(500) if not CP.plan_choice(f"t{i}", ks=(3,), abstain=True,
                                                                  show_rate=0.0).show_abstain)
    plan = CP.plan_choice(key, ks=(3,), abstain=True, show_rate=0.0)
    os_ = D.build_options(None, NONE[0], ms, row_key=key, render_key=str, abstain=NONE, plan=plan, strict_plan=False)
    assert os_.meta["gold_is_abstain"] and os_.gold.text == NONE[1] and len(os_.options) == 3


def test_abstain_slot_last_in_open_and_closed_sets():
    ms = _models({"m1": "a1", "m2": "b22", "m3": "c333", "m4": "d4444"})
    for i in range(200):
        key = f"z{i}"
        plan = CP.plan_choice(key, ks=(4,), abstain=True, abstain_slot="last")
        gold = NONE[0] if plan.gold_abstain else "g55555"
        os_ = D.build_options(None, gold, ms, row_key=key, render_key=str, abstain=NONE, plan=plan)
        assert os_.options[-1].key == NONE[0] and os_.gold_index == plan.pos
        cplan = CP.plan_choice(key, closed=3, abstain=True, abstain_slot="last")
        cg = NONE[0] if cplan.gold_abstain else ("allow", "ask", "deny")[i % 3]
        cs = D.build_closed(None, cg, ["allow", "ask", "deny"], {}, row_key=key, render_key=str.title,
                            abstain=NONE, plan=cplan)
        assert cs.options[-1].key == NONE[0] and cs.gold_index == cplan.pos and len(cs.options) == cplan.k
    with pytest.raises(ValueError):
        D.build_closed(None, "ask", ["allow", "ask", "deny"], {}, row_key="q", render_key=str, abstain=NONE,
                       plan=CP.plan_choice("q", closed=3, abstain=True), order="fixed")


def test_unplanned_calls_are_unchanged():
    ms = _models({"count_day0": "x1", "off_by_one_late": "x2", "wrong_anchor": "x3"})
    os_ = D.build_options(None, "g", ms, k=4, row_key="a", render_key=str)
    assert "plan" not in os_.meta and os_.gold_index == D.gold_position("a", 4)
    cs = D.build_closed(None, "b", ["a", "b", "c"], {}, row_key="a", render_key=str)
    assert "plan" not in cs.meta


# ------------------------------------------------------------------------------------------------ end to end

class _Toy:
    """A toy family: a rule file of 4-8 lines (random lengths); the deciding line is one of them, or none applies.
    Error models name every other line. The sampler draws structure label-first under a fixed plan."""

    def __init__(self, p_none: float):
        self.p_none = p_none

    def draw(self, key, attempt, target_none=None):
        rng = random.Random(f"{key}|{attempt}")
        lines = [f"Line {chr(97 + j)}: " + "/" * rng.randint(1, 40) for j in range(rng.randint(4, 8))]
        none = rng.random() < (self.p_none if target_none is None else (0.5 if target_none else 0.0))
        return {"lines": lines, "gold": None if none else rng.randrange(len(lines))}

    @staticmethod
    def solve(spec):
        return NONE[0] if spec["gold"] is None else spec["lines"][spec["gold"]]

    @staticmethod
    def models(spec):
        g = spec["gold"]
        return {f"err{j}": D.error_model(f"err{j}", (lambda t: (lambda s: t))(t), f"toy line {j}")
                for j, t in enumerate(spec["lines"]) if j != g}


def _planned_sets(n_rows, *, slot="shuffle"):
    toy, out = _Toy(0.3), []
    for i in range(n_rows):
        key = f"toy-{i}"
        plan = CP.plan_choice(key, ks=(3, 4), abstain=True, abstain_slot=slot)

        def fits(spec, gold, key=key, plan=plan):
            return D.build_options(spec, gold, toy.models(spec), row_key=key, render_key=str, abstain=NONE,
                                   plan=plan, length_balance=True) is not None
        spec, _ = CP.realize(plan, lambda a, key=key: toy.draw(key, a), solve=toy.solve, abstain_key=NONE[0],
                             fits=fits)
        out.append(D.build_options(spec, toy.solve(spec), toy.models(spec), row_key=key, render_key=str,
                                   abstain=NONE, plan=plan, length_balance=True))
    return out


def test_label_first_sampling_under_a_plan_balances_every_gate_view():
    sets = _planned_sets(3000)
    rep = CP.plan_report(sets)
    assert rep["pass"], rep["failing"]
    assert abs(rep["longest_gold_pp"]) <= 2.0
    for cell in rep["abstain_cells"].values():
        assert cell["p_binom"] > 0.001
    assert D.abstain_report(sets)["pass"]


def test_abstain_last_also_balances():
    rep = CP.plan_report(_planned_sets(2000, slot="last"))
    assert rep["pass"], rep["failing"]


def test_the_pilot_pattern_fails_the_report():
    """A fixed 15% abstain outcome (the T35 pilot) with the abstain text always longest: the report flags the abstain
    cells and gold-is-longest, as the pilot's G7 / G10 did."""
    toy, sets = _Toy(0.15), []
    for i in range(3000):
        key = f"old-{i}"
        k = 3 if D.uhash("k", key) < 0.5 else 4
        for a in range(400):
            spec = toy.draw(key, a)
            os_ = D.build_options(spec, toy.solve(spec), toy.models(spec), k=k, row_key=key, render_key=str,
                                  abstain=NONE, show_abstain=True, order_key=lambda t: (len(t), t))
            if os_ is not None:
                sets.append(os_)
                break
    rep = CP.plan_report(sets)
    assert not rep["pass"]
    assert any(f.startswith("k") for f in rep["failing"]) and "longest" in rep["failing"]
    assert rep["longest_gold_pp"] < -8


def test_realize_raises_when_no_structure_reaches_the_plan():
    key = next(f"q{i}" for i in range(500) if CP.plan_choice(f"q{i}", ks=(3,), abstain=True).gold_abstain)
    plan = CP.plan_choice(key, ks=(3,), abstain=True)
    toy = _Toy(0.0)
    with pytest.raises(CP.PlanMismatch):
        CP.realize(plan, lambda a: toy.draw(key, a, target_none=False), solve=toy.solve, abstain_key=NONE[0], tries=20)


def test_stats_helpers():
    assert CP.chi2_uniform_p([100, 100, 100]) == pytest.approx(1.0)
    assert CP.chi2_uniform_p([300, 0, 0]) < 1e-10
    assert 0.04 < CP.chi2_uniform_p([60, 40]) < 0.06                 # chi2 = 4, df 1: p = 0.0455
    assert CP.binom_two_sided(5, 10, 0.5) == pytest.approx(1.0)
    assert CP.binom_two_sided(0, 20, 0.5) < 1e-5

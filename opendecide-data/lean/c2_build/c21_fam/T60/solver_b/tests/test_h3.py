"""H3 PLAN-OR-ACT: the R1 x R2 x R3 truth table x card numbers (G0_LITE K3), D3 effect phrases, order-closure cases."""
import itertools
import json
import os

import fixtures as fx
import hook
import t60b_h3 as h3

POOL = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "pools", "wording_pool_v1.json")


def chain_flow(n):
    return [(i, i + 1) for i in range(1, n)]


def build(H, n_min, n_steps, r1, r3, r1_kind="N", world="tool"):
    """r1: some step high stakes; r3: some data-flow edge not implied by the stated order."""
    undo = fx.EFFECT_UNDOABLE if world == "tool" else fx.EFFECT_REPO_UNDOABLE
    steps = []
    for i in range(n_steps):
        phrase = ("rename the item i-%d" % i) if world == "tool" else ("touch /work/r/f%d.tmp" % i)
        steps.append([phrase, max(1, H - 1), undo[i % len(undo)]])
    if r1:
        k = n_steps // 2
        if r1_kind == "N":
            steps[k][1] = H
        elif r1_kind == "irrev":
            steps[k][2] = (fx.EFFECT_HIGH if world == "tool" else fx.EFFECT_REPO_HIGH)[0]
        elif r1_kind == "external":
            steps[k][2] = fx.EFFECT_HIGH[1]
    flow = chain_flow(n_steps)
    order = list(flow)
    if r3:
        order = order[1:] if len(order) > 1 else []              # drop one stated order that the flow needs
        if len(flow) == 1:
            order = []
    return fx.h3_view(H, n_min, [tuple(s) for s in steps], order=order, flow=flow)


def test_truth_table_three_predicates_x_cards():
    n = 0
    for H, n_min in itertools.product((5, 10, 20), (3, 4, 5)):
        for r1, r2_ok, r3, world in itertools.product((False, True), (False, True), (False, True), ("tool", "repo")):
            n_steps = n_min if r2_ok else n_min - 1
            for r1_kind in (("N", "irrev", "external") if (r1 and world == "tool") else ("N", "irrev") if r1 else ("N",)):
                v = build(H, n_min, n_steps, r1, r3, r1_kind, world)
                res = hook.solver_b(v)
                assert not res.abstain, res.reason
                want = "PLAN" if (r1 and r2_ok and r3) else "ACT"
                assert res.label == want, (H, n_min, r1, r2_ok, r3, world, r1_kind)
                n += 1
    assert n >= 108


def test_each_undoable_effect_alone_is_not_high_stakes():
    for eff in fx.EFFECT_UNDOABLE + fx.EFFECT_REPO_UNDOABLE:
        assert h3.effect_undoable(eff) is True
    for eff in fx.EFFECT_HIGH + fx.EFFECT_REPO_HIGH:
        assert h3.effect_undoable(eff) is False


def test_magnitude_threshold_is_inclusive():
    steps = [("rename the item i-0", 4, "can be undone for 14 more days"), ("rename the item i-1", 5, "can be undone for 14 more days"),
             ("rename the item i-2", 1, "can be undone for 3 more days")]
    v = fx.h3_view(5, 3, steps, order=[], flow=[(1, 2)])
    assert hook.solver_b(v).label == "PLAN"
    steps2 = [steps[0], ("rename the item i-1", 4, "can be undone for 14 more days"), steps[2]]
    assert hook.solver_b(fx.h3_view(5, 3, steps2, order=[], flow=[(1, 2)])).label == "ACT"


def test_order_closure_cases():
    steps = [("rename the item i-%d" % i, 9, "cannot be undone") for i in range(4)]
    base = dict(H=5, n_min=3)
    def lab(order, flow):
        return hook.solver_b(fx.h3_view(base["H"], base["n_min"], steps, order=order, flow=flow)).label
    assert lab([(1, 2), (2, 3)], [(1, 2), (2, 3)]) == "ACT"                  # every edge stated
    assert lab([(1, 2), (2, 3)], [(1, 3)]) == "ACT"                          # implied by the transitive closure
    assert lab([(1, 2)], [(1, 2), (2, 3)]) == "PLAN"                         # (2,3) is not stated
    assert lab([(2, 1)], [(1, 2)]) == "PLAN"                                 # the stated order goes the other way
    assert lab([(1, 3)], [(1, 2)]) == "PLAN"                                 # an unrelated statement implies nothing
    assert lab([], []) == "ACT"                                              # no data flow: no unstated dependency
    assert lab([(1, 2), (2, 3), (3, 4)], [(1, 4)]) == "ACT"                  # longer closure
    assert lab([(1, 2), (3, 4)], [(1, 4)]) == "PLAN"                         # two separate chains


def test_both_order_sentences_are_read():
    ctx = fx.h3_context(5, 3, [("rename the item a-1", 9, "cannot be undone")] * 3, order=[(1, 2), (2, 3)], flow=[(1, 2), (2, 3)], order_style=0)
    assert "Step s1 has to come before step s2." in ctx and "Do step s2 before step s3." in ctx
    assert hook.solver_b(fx.view("h3", ctx, fx.H3_OPTS, fx.H3_Q)).label == "ACT"


def test_every_pool_variant_of_the_card_clauses_is_read():
    pool = json.load(open(POOL))
    n = 0
    for r1 in pool["clause.p_r1"]:
        for r2 in pool["clause.p_r2"][:8]:
            card = "Policy card x_y.\n%s\n%s\n%s" % (r1.format(h=12, unit_pl="files"), r2.format(n=4), pool["clause.p_r3"][0])
            assert h3.parse_card(card) == {"H": 12, "n": 4}, card
            n += 1
    assert n > 100


def test_unknown_effect_phrase_abstains():
    v = fx.h3_view(5, 3, [("rename the item a-1", 1, "does something odd")] * 3, order=[], flow=[(1, 2)])
    r = hook.solver_b(v)
    assert r.abstain and r.label is None


def test_wrapper_sentence_on_the_goal_line_is_ignored():
    ctx = fx.h3_context(5, 3, [("rename the item a-1", 9, "cannot be undone")] * 3, order=[], flow=[(1, 2)])
    ctx = ctx.replace("The request:", "Management has asked that this be handled today. The request:")
    assert hook.solver_b(fx.view("h3", ctx, fx.H3_OPTS, fx.H3_Q)).label == "PLAN"

"""Tests for the glob matchers (glob_a vs glob_b, brute-force agreement), the rule AST and the brute helpers."""
from __future__ import annotations

import datetime as dt
import itertools
import random

import pytest

from c2_kit import brute, glob_a, glob_b
from c2_kit import rules as RL
from c2_kit.globsem import ROBOTS, GlobSem

SEMS = [GlobSem(), GlobSem(star_crosses_slash=True), GlobSem(anchored=False), GlobSem(double_star=True),
        GlobSem(question_mark=False), GlobSem(case_sensitive=False), ROBOTS,
        GlobSem(star_crosses_slash=False, anchored=False, dollar_end=True)]


def _strings(alpha, n):
    for k in range(n + 1):
        for t in itertools.product(alpha, repeat=k):
            yield "".join(t)


@pytest.mark.parametrize("sem", SEMS)
def test_two_independent_matchers_agree_on_a_brute_force_table(sem):
    pats = list(_strings("a/*?$", 4))
    subs = list(_strings("aA/", 4))
    for p in pats:
        for s in subs:
            assert glob_a.match(p, s, sem) == glob_b.match(p, s, sem), (p, s, sem)


def test_glob_semantics_examples():
    t = GlobSem()
    assert glob_a.match("ns.*", "ns.read", t) and not glob_a.match("ns.*", "ns.a/b", t)
    assert glob_a.match("ns.*", "ns.a/b", GlobSem(star_crosses_slash=True))
    assert glob_a.match("/data/**", "/data/a/b", GlobSem(double_star=True))
    assert not glob_a.match("/data/prod", "/data/production", t)
    assert glob_a.match("/data/prod", "/data/production", ROBOTS)          # robots: prefix match
    assert not glob_a.match("/data/prod$", "/data/production", ROBOTS)     # $ anchors the end
    assert glob_a.match("*.co", "mail.co", t) and not glob_a.match("*.co", "mail.com", t)
    assert "\"*\" matches any run of characters except \"/\"." in t.card_text()


def test_evaluate_boundaries_and_logic():
    env = {"A": 500, "L": 500, "D1": dt.date(2026, 1, 31), "D2": dt.date(2026, 3, 1), "T": "ns.read"}
    assert RL.evaluate(RL.Cmp("<=", RL.Ref("A"), RL.Ref("L")), env)
    assert not RL.evaluate(RL.Cmp("<", RL.Ref("A"), RL.Ref("L")), env)
    assert RL.evaluate(RL.Fn("days_between", (RL.Ref("D1"), RL.Ref("D2"))), env) == 29
    assert RL.evaluate(RL.Fn("add_days", (RL.Ref("D1"), RL.Lit(29))), env) == dt.date(2026, 3, 1)
    assert RL.evaluate(RL.Glob(RL.Lit("ns.*"), RL.Ref("T")), env)
    assert RL.evaluate(RL.In(RL.Ref("A"), (RL.Lit(1), RL.Lit(500))), env)
    assert RL.evaluate(RL.Or((RL.Not(RL.Lit(True)), RL.And((RL.Lit(True), RL.Lit(True))))), env)
    with pytest.raises(RL.Missing):
        RL.evaluate(RL.Ref("NOPE"), env)
    with pytest.raises(RL.RuleError):
        RL.evaluate(RL.And((RL.Lit(1),)), env)                  # conditions must be booleans
    tr = []
    RL.evaluate(RL.Cmp("<=", RL.Fn("days_between", (RL.Ref("D1"), RL.Ref("D2"))), RL.Lit(30)), env, tr)
    assert [v for _, v in tr] == [29, True]                     # printed intermediates come from the trace


def test_kleene_is_sound():
    env = {"X": None, "Y": 3}
    gt = RL.Cmp(">", RL.Ref("Y"), RL.Lit(1))
    assert RL.evaluate3(RL.Or((gt, RL.Ref("X"))), env) is True
    assert RL.evaluate3(RL.And((RL.Not(gt), RL.Ref("X"))), env) is False
    assert RL.evaluate3(RL.And((gt, RL.Cmp("<", RL.Ref("X"), RL.Lit(2)))), env) is None


def _rs(policy, **kw):
    rules = (RL.Rule("r1", "allow", RL.Cmp("<=", RL.Ref("A"), RL.Lit(100)), specificity=(1,)),
             RL.Rule("r2", "deny", RL.Cmp(">=", RL.Ref("A"), RL.Lit(50)), specificity=(2,)),
             RL.Rule("r3", "ask", RL.Cmp("==", RL.Ref("A"), RL.Lit(70)), specificity=(2,)))
    return RL.RuleSet(rules, policy, "ask", effect_order=("deny", "ask", "allow"), **kw)


def test_precedence_policies():
    env = {"A": 70}
    assert RL.resolve(_rs("first_match"), env).rule_id == "r1"
    assert RL.resolve(_rs("last_match"), env).rule_id == "r3"
    d = RL.resolve(_rs("effect_order"), env)
    assert (d.effect, d.rule_id, d.tied) == ("deny", "r2", ("r2",))
    d = RL.resolve(_rs("most_specific"), env)                   # r2 and r3 tie on specificity; deny wins by order
    assert (d.effect, d.tied) == ("deny", ("r2",))
    assert RL.resolve(_rs("priority_list", priority=("r3", "r1", "r2")), env).rule_id == "r3"
    d = RL.resolve(_rs("first_match"), {"A": 500})
    assert d.effect == "deny"
    d = RL.resolve(RL.RuleSet((), "first_match", "allow"), {"A": 1})
    assert (d.effect, d.rule_id) == ("allow", None)
    with pytest.raises(RL.RuleError):
        RL.RuleSet(_rs("first_match").rules, "effect_order", "ask", effect_order=("deny",))
    with pytest.raises(RL.RuleError):
        RL.RuleSet(_rs("first_match").rules, "priority_list", "ask", priority=("r1",))


def test_json_round_trip_and_ast_equality():
    rs = _rs("most_specific")
    assert RL.from_json(RL.to_json(rs)) == rs
    node = RL.And((RL.Cmp(">", RL.Ref("A"), RL.Lit(dt.date(2026, 1, 1))), RL.Glob(RL.Lit("x*"), RL.Ref("T"))))
    assert RL.from_json(RL.to_json(node)) == node
    a = RL.And((RL.Cmp(">=", RL.Ref("A"), RL.Lit(5)), RL.Ref("B")))
    b = RL.And((RL.Ref("B"), RL.Cmp("<=", RL.Lit(5), RL.Ref("A"))))
    assert RL.ast_equal(a, b)
    assert not RL.ast_equal(a, RL.And((RL.Ref("B"), RL.Cmp("<", RL.Lit(5), RL.Ref("A")))))
    assert RL.refs(a) == {"A", "B"}


def test_op_count_skips_printed_subtrees():
    days = RL.Fn("days_between", (RL.Ref("P"), RL.Ref("F")))
    node = RL.And((RL.Cmp("<=", days, RL.Ref("N")), RL.Cmp("<=", RL.Ref("A"), RL.Ref("L"))))
    assert RL.op_count(node) == 3
    assert RL.op_count(node, frozenset({RL.printed_key(days)})) == 2


def test_brute_epoch_minutes_matches_the_interpreter():
    rng = random.Random(3)
    for _ in range(500):
        tz = dt.timezone(dt.timedelta(minutes=rng.randrange(-48, 57) * 15))
        t = dt.datetime(rng.randrange(1999, 2031), rng.randrange(1, 13), rng.randrange(1, 29), rng.randrange(24),
                        rng.randrange(60), tzinfo=tz)
        assert brute.epoch_minutes(t) == RL.evaluate(RL.Fn("utc_minutes", (RL.Lit(t),)), {})


def test_brute_helpers():
    d = dt.date(2028, 2, 27)
    assert brute.day_list(d, dt.date(2028, 3, 1))[-2] == dt.date(2028, 2, 29)
    assert len(brute.window_days(d, 30)) == 31
    assert brute.cents_of("-1,234.5") == -123450 and brute.cents_of("12") == 1200
    outs = brute.completions(lambda e: e["a"] or e["b"], {"a": True, "b": None}, {"b": (True, False)})
    assert outs == {True}
    outs = brute.completions(lambda e: e["a"] and e["b"], {"a": True, "b": None}, {"b": (True, False)})
    assert outs == {True, False}
    with pytest.raises(KeyError):
        brute.table_lookup([("x", 1), ("x", 2)], "x")

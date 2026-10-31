"""G9 cross-family label consistency (K21 in T50, K19 in T51, K22 in T53): must pass 100% before any pilot."""
from LA_COMMON import g9


def test_k21a_t50_lane_rule_equals_the_t51_oracle_and_the_slt1_text():
    r = g9.k21a_lanes(seeds=range(3))
    assert r["pass"] and r["cases"] >= 300, r["examples"]


def test_k21b_t50_egress_members_equal_the_t53_engine_with_ask_on_soft_passed_through():
    r = g9.k21b_egress(seeds=range(2))
    assert r["pass"] and r["cases"] >= 500, r["examples"]


def test_k23_t53_ordered_rules_equal_the_t50_decision_tree_on_the_whole_grid():
    r = g9.k23_vs_t50()
    assert r["pass"] and r["cases"] > 50000


def test_the_comparison_has_power(monkeypatch):
    """Break one cell of the T51 oracle and the lane test must notice."""
    from T51 import model as m51
    real = m51.label

    def broken(M, auth, must, prot):
        lab, v = real(M, auth, must, prot)
        return ("ALLOW", v) if lab == "ASK" else (lab, v)
    monkeypatch.setattr(m51, "label", broken)
    assert not g9.k21a_lanes(seeds=range(1))["pass"]

"""families/T35/test_fix_i3.py: tests for pilot fix iteration 3 (A44 a, d; G0_SPEC.md v5). In memory only (A37 f).

  status trap   every 4xx / 5xx base sits in a block of 4 whose (status class, polarity) cells are each hit once: both golds on
                both polarities, positive frames only (yn_fetch / yn_skip); the status class never decides the gold alone
  ch_line size  the planned rule-line / group counts are met exactly and are independent of the gold type (line vs "no line")

Run (from lean/c2_build):  ../../.venv/bin/python -m pytest -q families/T35/test_fix_i3.py
"""
import collections
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pytest  # noqa: E402

from families.T35 import plugin as P  # noqa: E402
from families.T35 import fixtures as FX  # noqa: E402

TRAIN = ("S1", "S2", "S3", "S4")


@pytest.fixture(scope="module")
def plugin():
    return P.T35Plugin(lexicon=FX.ctx().lexicon)


@pytest.fixture(scope="module")
def specs(plugin):
    return [plugin.sample(seed, s) for s in TRAIN for seed in range(0, 1760)]


def _cls(spec):
    st = spec.slots.get("STATUS")
    key = None if st is None else st.value
    return None if key in (None, "200") else ("4xx" if key in P.STATUS_4XX else "5xx")


def test_trap_blocks_pair_each_status_with_both_polarities(plugin, specs):
    yn = [s for s in specs if s.qform != P.CHOICE_FORM]
    traps = [s for s in yn if _cls(s)]
    assert len(traps) > 40                          # A45 b: S4 p_ns 0.13 -> 0.09 and the 200-base status twin 0.20 -> 0.10 (was > 60)
    assert {s.qform for s in traps} <= {P.POS_FORM, "yn_skip"}
    cells = collections.Counter((_cls(s), s.qform, plugin.solve_a(s)) for s in traps)
    # A45 b: the old loop asked for every (class, form, gold) cell, which cannot exist (4xx = may fetch, so under "may it fetch?"
    # the gold is always yes). The design: each class meets both forms and both golds, each form meets both classes and both golds.
    for cls in ("4xx", "5xx"):
        assert {qf for (c, qf, _g) in cells if c == cls} == {P.POS_FORM, "yn_skip"}, cls
        assert {g for (c, _qf, g) in cells if c == cls} == {0, 1}, cls
    for qf in (P.POS_FORM, "yn_skip"):
        assert {c for (c, f, _g) in cells if f == qf} == {"4xx", "5xx"}, qf
        assert {g for (_c, f, g) in cells if f == qf} == {0, 1}, qf
    for cls in ("4xx", "5xx"):                      # the four (class, form) cells hold the same number of bases
        n = [sum(v for (c, f, _g), v in cells.items() if c == cls and f == qf) for qf in (P.POS_FORM, "yn_skip")]
        assert abs(n[0] - n[1]) <= max(6, 0.15 * sum(n)), (cls, n)
    for cls in ("4xx", "5xx"):                      # the code alone: gold yes is about half in each class
        g = [plugin.solve_a(s) for s in traps if _cls(s) == cls]
        assert 0.35 <= sum(g) / len(g) <= 0.65, (cls, sum(g), len(g))
    # status class is derived from the outcome: 4xx = may fetch, 5xx = may not; polarity decides the gold
    for s in traps:
        assert P.decide(s).allowed == (_cls(s) == "4xx")
        assert plugin.solve_a(s) == int(P.decide(s).allowed == (s.qform == P.POS_FORM))


def test_choice_rows_never_carry_a_deciding_status(specs):
    ch = [s for s in specs if s.qform == P.CHOICE_FORM]
    assert len(ch) > 500 and all(_cls(s) is None for s in ch)


def test_choice_file_size_is_planned_before_the_gold(plugin, specs):
    ch = [s for s in specs if s.qform == P.CHOICE_FORM]
    by = {"line": collections.Counter(), "none": collections.Counter()}
    for s in ch:
        lines = sum(len(g["lines"]) for g in s.structure["groups"])
        groups = len(s.structure["groups"])
        assert lines in P.CH_LINES and groups in P.CH_GROUPS and lines >= groups
        by["none" if P.decide(s).rules_by != "line" else "line"][(lines, groups)] += 1
    for k in ("line", "none"):
        n = sum(by[k].values())
        mean_l = sum(a * c for (a, _), c in by[k].items()) / n
        mean_g = sum(b * c for (_, b), c in by[k].items()) / n
        assert abs(mean_l - 7.0) <= 0.35 and abs(mean_g - 2.5) <= 0.35, (k, mean_l, mean_g)

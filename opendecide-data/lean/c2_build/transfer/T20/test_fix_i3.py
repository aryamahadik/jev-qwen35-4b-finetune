"""transfer/T20/test_fix_i3.py: the A45 (c) iteration (G0 v4): per-card rule tables.

  - the 24 urgency-column orders: every urgency word has the same level distribution over the tables;
  - exposed: yes is planned at the same rate in every class (choice level x yes/no form x outcome), never with a twin;
  - the exposure rule is printed on the card, read back by solver B (own regex), applied by solver A (band condition, three effects),
    and a rule whose condition fails does nothing (depth counts only an active rule);
  - the same record under two cards (two exposure rules / two urgency orders) has different answers, so no record token names the level.
"""
from __future__ import annotations

import collections
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import pipeline  # noqa: E402
from transfer.T20 import fixtures as FX  # noqa: E402
from transfer.T20 import plugin as P  # noqa: E402
from transfer.T20 import solver_b as B  # noqa: E402

TRAIN = ("S1", "S2", "S3", "S4")
BASE = 900_000


@pytest.fixture(scope="module")
def ctx():
    return FX.ctx()


@pytest.fixture(scope="module")
def plugin(ctx):
    return P.T20Plugin(lexicon=ctx.lexicon)


def test_each_urgency_word_has_the_same_level_distribution_over_the_tables():
    for col in range(3):
        dist = collections.Counter(m[r][col] for m in P.MATRICES for r in range(3))
        assert dist == collections.Counter(m[r][0] for m in P.MATRICES for r in range(3)), col


def test_exposed_yes_is_planned_at_the_same_rate_in_every_class_and_never_with_a_twin():
    n, ex = collections.Counter(), collections.Counter()
    for smp in TRAIN:
        for seed in range(BASE, BASE + 1600):
            pl = P.plan_of(smp, seed)
            key = pl.target if pl.kind == "choice" else (pl.qform, bool(pl.target))
            n[key] += 1
            if pl.ex:
                ex[key] += 1
                assert not pl.twin, (smp, seed)
    for key in n:
        if key in P.SEV_KEYS or n[key] >= 150:
            assert abs(ex[key] / n[key] - 1 / P.EX_B) < 0.04, (key, ex[key], n[key])
    for lvl in P.SEV_KEYS:
        assert ex[lvl] > 0


def test_card_prints_the_rule_and_solver_b_reads_it_back(plugin, ctx):
    seen = set()
    for smp in TRAIN:
        for seed in range(BASE, BASE + 160):
            spec = plugin.sample(seed, smp)
            seen.add(P.xr_of(spec))
            if len(seen) > 5 and spec.env()["EXPOSED"] == "yes":
                break
    assert seen == set(P.XRULES)
    # rows: the parsed rule equals the generator's, G2 and G3 pass (pipeline.check_rendered), exposed rows included
    n_ex = 0
    for k in range(120):
        spec = plugin.sample(BASE + k, TRAIN[k % 4])
        n_ex += spec.env()["EXPOSED"] == "yes"
        u = pipeline.build_unit(plugin, spec, ctx, run_g15=False)
        assert u.ok, u.problems[:2]
        for rr in u.rows:
            view = plugin.parse(rr, ctx)
            assert view["xrule"] == list(P.xr_of(spec))
            assert P.xr_text(P.xr_of(spec)) in (rr["card"] or "") + rr["instructions"]
    assert n_ex >= 5


@pytest.mark.parametrize("rule, users, base, want", [
    (("any", "sev1"), 10, 4, 1), (("any", "sev2"), 10, 4, 2), (("any", "sev2"), 10, 1, 1), (("any", "up"), 10, 4, 3),
    (("any", "up"), 10, 1, 1), (("wide", "sev1"), 10, 4, 4), (("wide", "sev1"), 5000, 4, 1), (("wide", "up"), 5000, 4, 3)])
def test_exposure_rule_effects_and_conditions(plugin, rule, users, base, want):
    import datetime as dt
    from transfer.T20 import test_plugin as TP
    spec = TP._spec(plugin, users=users, urgency="outage", check_min=10, exposed="yes")
    cell = {"MX_M_O": base}
    mx = {k: P.S.category_slot(f"sev{cell.get(k, base)}", P.SEV) for k in P.MATRIX_SLOTS if k.startswith(("MX_W_O", "MX_P_O", "MX_M_O"))}
    spec = spec.replace(slots={**spec.slots, **mx}, structure={**spec.structure, "xr": list(rule)})
    assert P.severity(spec) == want, (rule, users, base)
    assert (P.depth_of(spec) - (1 if not spec.structure["printed"] else 0)) == 1 + int(P._x_holds(spec))

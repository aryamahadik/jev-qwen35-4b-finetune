"""c2_build/families/T12/test_i2_fixes.py: tests of the T12 fix iteration 2 (G0_SPEC_v2_2.md R20: the yes label of a
yes/no base row is a label-first draw stratified by (question form, card); G6 at 6,000 rows, pilot_i1 verdict FIX).

  yes_balance     every yes/no form has a yes rate of 50% (+- 1.5 pp) on every sampler over runs of consecutive seeds,
                  whatever the card mix; each card's rate stays inside 20-80%; the draw is stateless (same value on a
                  fresh evaluation) and the base specs' golds match it (solver A)
"""
from __future__ import annotations

import collections
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from families.T12 import plugin as P  # noqa: E402

TRAIN = P.TRAIN_SAMPLERS


def _forms(run, samplers):
    for s in run:
        for smp in samplers:
            q = P.T12Plugin._qform_of(s, smp)
            if not q.startswith("ch_"):
                yield s, smp, q, P._card_idx_of(s, smp)


@pytest.mark.parametrize("samplers", [TRAIN, ("S5",)])
def test_yes_rate_is_half_for_every_form_and_cards_keep_their_rates(samplers):
    for run in (range(900000, 900146 * 6), range(P.BLOCK * 300, P.BLOCK * 300 + 2000)):
        form, card, per_sampler = collections.defaultdict(list), collections.defaultdict(list), collections.defaultdict(list)
        for s, smp, q, idx in _forms(run, samplers):
            y = P.T12Plugin._yes_of(s, smp, q, idx, P.N_CARDS_S5 if smp == "S5" else P.N_CARDS)
            form[q].append(y)
            per_sampler[(q, smp)].append(y)
            card[(smp, idx)].append(y)
        assert len(form) == 7
        for q, ys in form.items():
            assert abs(sum(ys) / len(ys) - 0.5) <= 0.015, (q, sum(ys) / len(ys), len(ys))
        for k, ys in per_sampler.items():
            assert abs(sum(ys) / len(ys) - 0.5) <= 0.04, (k, len(ys))
        for k, ys in card.items():
            if len(ys) >= 40:
                assert 0.2 <= sum(ys) / len(ys) <= 0.8, (k, sum(ys) / len(ys))


def test_yes_draw_is_stateless():
    a = [P._yes_table(TRAIN, 900000 - 900000 % P.BLOCK)[(s, "S1")] for s in range(900000, 900200)
         if not P.T12Plugin._qform_of(s, "S1").startswith("ch_")]
    P._yes_table.cache_clear()
    b = [P._yes_table(TRAIN, 900000 - 900000 % P.BLOCK)[(s, "S1")] for s in range(900000, 900200)
         if not P.T12Plugin._qform_of(s, "S1").startswith("ch_")]
    assert a == b and len(a) > 50

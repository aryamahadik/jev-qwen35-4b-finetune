"""Fix iteration 2: the yes/no wording is assigned label-first (balanced yes rate per (form, wording))."""
from __future__ import annotations

import collections
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
if str(HERE.parents[1]) not in sys.path:
    sys.path.insert(0, str(HERE.parents[1]))

from families.T32 import plugin as P  # noqa: E402


def _bare():
    pl = P.T32.__new__(P.T32)
    pl._wtab = {}
    pl.dneg_ok = True
    return pl


def test_every_form_wording_cell_is_half_yes_by_construction():
    pl = _bare()
    W = 6
    cells = collections.defaultdict(lambda: [0, 0])
    for smp in ("S1", "S4"):
        tab = pl._wording_ranks(smp, 0)
        for key_, r in tab.items():
            if len(key_) != 2:                   # W9: choice-form ranks are keyed ("s", seed, form)
                continue
            (pair, f) = key_
            order = sorted(range(W), key=lambda w: P.uhash(P.FAMILY, "wperm", smp, 0, f, w))
            w = order[r % W]
            for seed in (2 * pair, 2 * pair + 1):
                yes = (seed % 2 == 0) != (P.uhash(P.FAMILY, "flip", smp, pair) < 0.5)
                cells[(smp, f, w)][int(yes if f in {k for k, _ in P.BASE_SHARES} else not yes)] += 1
    for k, (no, yes) in cells.items():
        assert yes == no, (k, yes, no)


def test_ranks_are_stateless():
    a, b = _bare(), _bare()
    assert a._wording_ranks("S2", 3) == b._wording_ranks("S2", 3)


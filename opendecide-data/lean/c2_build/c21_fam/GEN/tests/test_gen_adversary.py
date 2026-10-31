"""The online shortcut filter (adversary.py): deterministic, drop-only, and it lowers the option-only probe on a form that leaks.
CPU only; scikit-learn LR / gradient boosting; nothing is written."""
import warnings

import pytest

import builder as BU
import gates as GT
import pool_loader as PL
import row_check as RC
from b_main import solve_row
from gen_common import GenAllow

warnings.filterwarnings("ignore")


@pytest.fixture(scope="module")
def real():
    return PL.load_real_pool()


def _mk(real, seed, adv, form="TM-T1", n=40):
    b = BU.Builder(seed, real, allow=GenAllow(), provisional=False, mode="rows", vocab=PL.predicate_vocab(), adversary=adv)
    rows = []
    for i in range(n):
        rows.extend(b.unit(form, "train", i, pair_prob=0.3))
    return b, rows


def test_default_is_on_in_rows_mode_and_off_in_dry_mode(real):
    assert BU.Builder("x", real, allow=GenAllow(), provisional=False, mode="rows").adversary is True
    import gen_common as g
    assert BU.Builder("x", g.make_testonly_pool(), allow=GenAllow(), provisional=True, mode="dry").adversary is False


def test_filter_is_deterministic_and_rows_stay_valid(real):
    b1, r1 = _mk(real, "advdet", True, n=25)
    b2, r2 = _mk(real, "advdet", True, n=25)
    assert [r["stem"] for r in r1] == [r["stem"] for r in r2] and [r["options"] for r in r1] == [r["options"] for r in r2]
    for r in r1:
        assert BU.validate_row(r) == []
        out = solve_row({k: r[k] for k in ("form", "k", "carrier", "stem", "options")})
        assert out["status"] == "ok" and out["answer_index"] == r["label"]
    assert b1.adv["TM-T1"].stats["checked"] > 0


def test_fixed_option_forms_are_not_filtered(real):
    b, rows = _mk(real, "advskip", True, form="CA-C3", n=20)
    assert "CA-C3" not in b.adv and rows


def test_warm_up_leaves_the_trap_balancer_alone(real):
    b = BU.Builder("advbal", real, allow=GenAllow(), provisional=False, mode="rows", adversary=True)
    before = b.trap_bal.snapshot()
    b._adv("AR-F1")
    assert b.trap_bal.snapshot() == before


def test_filter_lowers_the_option_only_probe_on_a_leaky_form(real):
    res = {}
    for adv in (False, True):
        b, rows = _mk(real, "advgain", adv, form="TM-T2", n=230)
        r = GT.option_only_probe(rows, 4, n_boot=50, seed=0, check_sanity=False)
        res[adv] = max(m["point"] for m in r["models"].values())
    assert res[True] < res[False] - 0.05, res

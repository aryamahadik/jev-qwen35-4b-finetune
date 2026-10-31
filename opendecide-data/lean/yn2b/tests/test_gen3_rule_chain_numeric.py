"""F1b numeric claim checks (golden_src/gen3/rc_numeric.py): exact arithmetic, boundaries, the card rules, the
shortcut solvers, the sampler and the parse-back of every format."""
from __future__ import annotations

import random
import sys
from fractions import Fraction
from pathlib import Path

import pytest

LEAN = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(LEAN / "golden_src" / "gen3"))
import mv_core as mv  # noqa: E402
import rc_numeric as NB  # noqa: E402


def item(**kw):
    f = {"pack": "library", "kind": "threshold", "items": [{"value": "1200", "date": "2026-03-01", "revised": None}],
         "source": "the library's annual return", "op": "ge", "claim": "1200", "tol": None, "factor": None,
         "asof": None, "dir": None, "ents": None, "record": None, "dp": 0, "cdp": 0}
    f.update(kw)
    return f


def test_threshold_boundary_and_inclusive_shortcut():
    assert NB.truth(item(op="ge")) and not NB.truth(item(op="gt"))
    sc = NB.shortcut_truths(item(op="gt"))
    assert sc["all_inclusive"] is True


def test_revision_counts_and_ignore_amendments():
    f = item(items=[{"value": "1200", "date": "2026-03-01", "revised": "1180", "revised_date": "2026-03-09"}],
             op="ge", claim="1190")
    assert not NB.truth(f)
    assert NB.shortcut_truths(f)["ignore_amendments"] is True


def test_as_of_and_latest_dated():
    f = item(items=[{"value": "100", "date": "2026-01-01", "revised": None},
                    {"value": "300", "date": "2026-02-01", "revised": None}], asof="2026-01-20", op="lt", claim="200")
    assert NB.truth(f)
    assert NB.shortcut_truths(f)["latest_dated"] is False


def test_percent_change_base_and_exact_boundary():
    f = item(kind="pct", items=[{"value": "200", "date": "2026-01-01", "revised": None},
                                {"value": "220", "date": "2026-04-01", "revised": None}], dir="rose", op="ge",
             claim="10")
    assert NB.value(f) == 10 and NB.truth(f)
    assert NB.value(f, "wrong_base") == Fraction(100, 11)
    assert NB.shortcut_truths(f)["wrong_base"] is False


def test_about_tolerance_counts_both_ends():
    f = item(kind="about", op="about", claim="1210", tol="10")
    assert NB.truth(f)
    assert not NB.truth(item(kind="about", op="about", claim="1211", tol="10"))


def test_unit_conversion():
    f = item(pack="freight", kind="unit", items=[{"value": "2.5", "date": "2026-03-01", "revised": None}],
             factor="1000", op="ge", claim="2500", dp=1, cdp=1)
    assert NB.truth(f) and NB.shortcut_truths(f)["unit_blind"] is False


@pytest.mark.parametrize("kind", NB.KINDS)
def test_sampler_realises_gold_and_parse_back(kind):
    rng = random.Random(3)
    pool = mv.NamePool("train")
    made = 0
    for i in range(200):
        pack = rng.choice([p for p in NB.PACKS_B if kind != "unit" or NB.PACKS_B[p]["conv"]])
        plan = {"kind": kind, "gold": rng.choice(["yes", "no"]), "boundary": rng.choice([None, "exact", "off1"]),
                "revised": rng.random() < 0.5, "asof": kind in ("threshold", "unit", "about") and rng.random() < 0.4}
        try:
            f = NB.sample(rng, pool, pack, plan)
        except mv.Reject:
            continue
        assert ("yes" if NB.truth(f) else "no") == plan["gold"]
        f["record"] = rng.choice([None, "SUPPORTED", "NOT SUPPORTED"])
        defs = NB.card_defs(f, judge=bool(f["record"]))
        for fmt in ("json", "markdown", "kv", "prose", "log:chrono", "log:newest", "log:shuffled"):
            st = NB.render_state(f, fmt, rng.choice(["iso", "long", "us"]), perm_seed=i)
            p = NB.parse_state(st, fmt, pack, defs)
            assert NB.truth(p) == NB.truth(f), (kind, fmt, st)
            assert p.get("record") == f["record"]
        made += 1
        if made >= 12:
            break
    assert made >= 6


def test_card_states_every_rule_used():
    f = item(kind="about", op="about", claim="1210", tol="10",
             items=[{"value": "1200", "date": "2026-03-01", "revised": "1205", "revised_date": "2026-03-04"}])
    d = NB.card_defs(f, judge=False)
    assert {"figures", "revisions", "about", "yes", "no"} <= set(d)
    for k, v in d.items():
        assert ": " not in k and "\n" not in v

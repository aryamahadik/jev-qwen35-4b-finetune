"""families/T35/test_fix_i4.py: tests for the final iteration (A45 b). In memory only.

  S4 seeds that failed pilot_i3 ("no spec reached its planned outcome") now sample, and the plan's group count is met
  every sampled spec decides exactly what its plan says (decide(spec) == target), on status rows too
Run (from lean/c2_build):  ../../.venv/bin/python -m pytest -q families/T35/test_fix_i4.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pytest  # noqa: E402

from families.T35 import plugin as P  # noqa: E402
from families.T35 import fixtures as FX  # noqa: E402

FAILED_I3 = (900027, 900031, 900101, 900107, 900112)


@pytest.fixture(scope="module")
def plugin():
    return P.T35Plugin(lexicon=FX.ctx().lexicon)


@pytest.mark.parametrize("seed", FAILED_I3)
def test_the_seeds_that_failed_pilot_i3_sample_on_s4(plugin, seed):
    spec = plugin.sample(seed, "S4")
    assert spec.qform == P.CHOICE_FORM
    assert len(spec.structure["groups"]) in P.CH_GROUPS


def test_every_spec_decides_its_plan(plugin):
    seen = {"4xx": 0, "5xx": 0, "choice": 0}
    for sampler in ("S1", "S2", "S3", "S4"):
        for seed in range(0, 400):
            qform, target, status, _k, _e = plugin._plan(seed, sampler)
            spec = plugin.sample(seed, sampler)
            d = P.decide(spec)
            if qform == P.CHOICE_FORM:
                seen["choice"] += 1
                assert d.by == ("nomatch" if target == "none" else "line")
                assert target == "none" or d.allowed == (target == "allow")
            else:
                assert d.allowed == (target == "allow"), (sampler, seed, qform, target, status)
                if status in P.STATUS_4XX:
                    seen["4xx"] += 1
                    assert d.by == "status_4xx" and target == "allow"
                if status in P.STATUS_5XX:
                    seen["5xx"] += 1
                    assert d.by == "status_5xx" and target == "disallow"
    assert all(v > 5 for v in seen.values()), seen


def test_assert_target_rejects_a_wrong_plan(plugin):
    seed = next(s for s in range(60) if plugin._plan(s, "S1")[0] != P.CHOICE_FORM)
    spec = plugin.sample(seed, "S1")
    d = P.decide(spec)
    wrong = "disallow" if d.allowed else "allow"
    qform = spec.qform
    with pytest.raises(P.ContractError):
        plugin._assert_target(spec, qform, wrong, None)

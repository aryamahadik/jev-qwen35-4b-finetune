"""CPU tests for gate/noninf_check.py (A8-prime step N). No GPU, no network, no model; the real lean/ tree is only read.

  ../.venv/bin/python -m pytest -q gate/tests/test_noninf_check.py

- decide(): every bar at its exact edge, from synthetic numbers (pure function).
- the (e)-without-hate bar takes min(C1R's rate, job-1 C1's 32/662) + 1 pp.
- run() on the REAL job-1 reads: 4B-E (q35_4b_pxE_fresh) standing in for C4 against the main run reproduces
  logs/gate4b/look_ship1.txt with the sign flipped and FAILS; the main run against itself PASSES.
- a pair count that is not 662 + 60 stops the rule (no verdict).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

LEAN = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(LEAN))
sys.path.insert(0, str(LEAN / "gate"))
import noninf_check as nc  # noqa: E402


def nums(full=0.0, prim=0.0, brier=0.0, perm=0.0, jag=0.0, opi=0.0, k4=32, k1=32, n=662):
    return {"full": {"cand": 81.0 + full, "ref": 81.0, "diff": full, "n": 7056},
            "primary": {"cand": 84.0 + prim, "ref": 84.0, "diff": prim, "n": 3847},
            "brier": {"c4": 0.11 + brier, "c1r": 0.11},
            "perm": {"cand": 2.43 + perm, "ref": 2.43, "n": 3814},
            "jagged": {"cand": 0.0 + jag / 100, "ref": 0.0, "elig_cand": 1, "elig_ref": 1},
            "opi": {"cand": 0.0127 + opi / 100, "ref": 0.0127, "elig_cand": 1, "elig_ref": 1},
            "equiv_nonhate": {"pairs": n, "c4_flips": k4, "c1r_flips": k1, "c4": 100 * k4 / n, "c1r": 100 * k1 / n,
                              "c1_job1": 100 * 32 / 662, "bar": nc.nonhate_bar(k1, n)}}


def status(ns):
    return [ok for _, ok, _ in nc.decide(ns)]


def test_all_pass_at_identity():
    assert all(status(nums()))


@pytest.mark.parametrize("kw, idx", [({"full": -0.3}, 0), ({"prim": -0.5}, 1), ({"brier": 0.002}, 2),
                                     ({"perm": 0.5}, 3), ({"jag": 1.0}, 4), ({"opi": 1.0}, 5)])
def test_each_bar_passes_at_its_edge(kw, idx):
    assert status(nums(**kw))[idx]


@pytest.mark.parametrize("kw, idx", [({"full": -0.31}, 0), ({"prim": -0.51}, 1), ({"brier": 0.0021}, 2),
                                     ({"perm": 0.51}, 3), ({"jag": 1.01}, 4), ({"opi": 1.01}, 5)])
def test_each_bar_fails_past_its_edge(kw, idx):
    st = status(nums(**kw))
    assert not st[idx] and sum(1 for x in st if not x) == 1


def test_nonhate_bar_uses_the_lower_rate():
    assert nc.nonhate_bar(40, 662) == pytest.approx(100 * 32 / 662 + 1)   # C1R worse than job 1: job-1 bar (5.83%)
    assert nc.nonhate_bar(30, 662) == pytest.approx(100 * 30 / 662 + 1)   # C1R better: its own rate + 1 pp (5.53%)
    assert status(nums(k4=38, k1=40))[6] and not status(nums(k4=39, k1=40))[6]   # 38/662 = 5.74% <= 5.83% < 5.89%
    assert status(nums(k4=36, k1=30))[6] and not status(nums(k4=37, k1=30))[6]   # 5.44% <= 5.53% < 5.59%
    assert not status(nums(k4=39, k1=39))[6]  # 4B-E's own 39/662 never passes


def test_real_standin_fails_like_look_ship1():
    r = nc.run("q35_4b_pxE_fresh", "q35_4b_main500k", quiet=True)
    n = r["numbers"]
    assert round(n["full"]["diff"], 2) == -1.19 and round(n["primary"]["diff"], 2) == -2.47
    assert (n["equiv_nonhate"]["c4_flips"], n["equiv_nonhate"]["c1r_flips"]) == (39, 32)
    assert n["equiv_nonhate"]["max_flips_allowed"] == 38
    assert n["equiv_hate_report"] == {"pairs": 60, "c4_flips": 2, "c1r_flips": 32}
    assert [c["pass"] for c in r["checks"]] == [False, False, False, False, True, True, False]
    assert r["pipeline_issues"] == [] and not r["pass"]


def test_real_identity_passes():
    r = nc.run("q35_4b_main500k", "q35_4b_main500k", quiet=True)
    assert r["pass"] and r["numbers"]["full"]["diff"] == 0


def test_wrong_pair_count_stops(monkeypatch):
    monkeypatch.setattr(nc, "HATE_SOURCES", {"hate", "clinc150"})
    with pytest.raises(SystemExit, match="not the 662 \\+ 60"):
        nc.run("q35_4b_main500k", "q35_4b_main500k", quiet=True)


def test_pipeline_issue_raises_no_verdict(monkeypatch):
    """A pipeline problem is NO VERDICT (exit 2, no JSON), never a failure of C4 (PREREG_FINAL 3.4)."""
    good, _, _ = nc.compute("q35_4b_main500k", "q35_4b_main500k")
    monkeypatch.setattr(nc, "compute", lambda c4, c1r: (good, {}, ["c4: path train (not od_gcp predict) [dev]"]))
    with pytest.raises(nc.NoVerdict):
        nc.run("x", "y", quiet=True)

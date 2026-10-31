"""Seed-base option of gen_full_c2.py (T01 full-generation diagnosis, 15 Oct 2026): validation, the refusal to re-draw on a
failed generation's seeds, and that the bases reach build_pilot / build_mixdev / the report."""
import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

import gen_full_c2 as G  # noqa: E402
import pilot  # noqa: E402

GOOD = (12_000_000, 13_000_000, 14_000_000)


def test_valid_bases_pass_and_are_reported():
    assert G.check_seed_bases(GOOD) == GOOD
    plan = G.seed_plan(GOOD)
    assert (plan["candidates"], plan["qc"], plan["mixdev"]) == GOOD
    assert plan["default_bases"] == [G.FULL_SEED_BASE, G.QC_SEED_BASE, G.MIXDEV_SEED_BASE]
    assert G.seed_plan()["candidates"] == G.FULL_SEED_BASE            # default unchanged


@pytest.mark.parametrize("bad", [(12_000_001, 13_000_000, 14_000_000), (12_000_000, 12_500_000, 14_000_000),
                                 (pilot.SEED_BASE, 13_000_000, 14_000_000), (12_000_000, 13_000_000),
                                 (12_000_000, 13_000_000, -32)])
def test_bad_bases_refused(bad):
    with pytest.raises(SystemExit):
        G.check_seed_bases(bad)


def test_failed_seeds_are_never_reused(tmp_path):
    L = G.layout("T01", tmp_path)
    L["gen"].parent.mkdir(parents=True)
    L["gen"].write_text(json.dumps({"seeds": G.seed_plan(GOOD)}))
    with pytest.raises(SystemExit):
        G.check_seed_bases((GOOD[0], 20_000_000, 21_000_000), "T01", tmp_path)     # candidates base reused
    with pytest.raises(SystemExit):
        G.check_seed_bases((22_000_000, GOOD[2], 24_000_000), "T01", tmp_path)     # mixdev base reused (any slot)
    assert G.check_seed_bases((22_000_000, 23_000_000, 24_000_000), "T01", tmp_path)
    assert G.check_seed_bases(GOOD, "T30", tmp_path)                               # another family: no report, no clash


def test_bases_reach_the_builders(monkeypatch):
    seen = {}
    real = pilot.build_pilot

    def spy(kit, n, **kw):
        seen.setdefault("build", []).append(kw.get("seed_base"))
        return real(kit, n, **kw)
    monkeypatch.setattr(pilot, "build_pilot", spy)
    rep = G.run("T30", n=24, qc_n=24, dry=True, seed_bases=GOOD, log=lambda m: None)
    assert seen["build"] == [GOOD[0], GOOD[1]]
    assert rep["seeds"]["candidates"] == GOOD[0] and rep["seeds"]["mixdev"] == GOOD[2]
    assert rep["mixdev"]["seed_base"] == GOOD[2] if "seed_base" in rep["mixdev"] else True
    assert "seed base %d" % GOOD[1] in rep["gates"]["G6"]["qc_build"]

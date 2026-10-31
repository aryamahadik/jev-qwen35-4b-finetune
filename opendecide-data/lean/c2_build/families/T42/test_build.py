"""In-memory build test of T42 through pilot.build_pilot (T42_BUILD_N rows, default 3,000; nothing is written but a
metrics file of numbers). The loader is registered at runtime (pilot_loaders.LOADERS["T42"]); the pilot's own gates run:

  G2 / G3 / G4 / G-SL / G-LEX / G15 / schema / options   0 failed units
  G6   all views, both models, <= chance + 2 pp          (pilot.g6)          G7: no failing feature          G10 pass
  probes   options-only and formatting-only within chance +/- 3 pp, per head; diff size does not predict SAME / DIFFERS
  reseed   3% of the rows re-executed (another PYTHONHASHSEED and fuzz seed): at most 1% label flips
Run (from lean/c2_build):  T42_BUILD_N=3000 ../../.venv/bin/python -m pytest -q -p no:cacheprovider families/T42/test_build.py
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

import pilot  # noqa: E402
import pilot_loaders as PL  # noqa: E402
from c2_kit.distractors import uhash  # noqa: E402
from families.T42 import executor as E  # noqa: E402
from families.T42 import probes as PR  # noqa: E402
from families.T42 import run_pilot_i1 as RUN  # noqa: E402
from families.T42 import plugin as P  # noqa: E402

N = int(os.environ.get("T42_BUILD_N", "3000"))
RESULTS = Path(__file__).resolve().parent / "BUILD_PROBES.json"
_state: dict = {}


@pytest.fixture(scope="module")
def build():
    if "b" not in _state:
        PL.LOADERS["T42"] = RUN._t42
        RUN.install_patches()
        with PL.LOADERS["T42"]() as kit:
            _state["kit"] = kit
            _state["b"] = pilot.build_pilot(kit, N, run_g15=os.environ.get("T42_G15", "1") != "0")
    return _state["b"]


def test_program_gates(build):
    g = pilot.program_gates(build)
    failed = {k: v["units_failed"] for k, v in g.items() if k in pilot.PROGRAM_GATES and v["verdict"] != "pass"}
    assert not failed, failed
    assert build.stats["reached_target"] and build.stats["rows_written"] >= N
    _state["gates"] = {k: {"units_failed": v["units_failed"]} for k, v in g.items() if k in pilot.PROGRAM_GATES}
    _state["drops"] = build.stats["drops_by_gate"]


def test_g6_g7_g10(build):
    infos = build.infos
    g6 = pilot.g6(infos)
    g7 = pilot.g7(infos)
    g10 = RUN_g10(build)
    _state["g6"] = {"fails": g6["fails"], "choice": g6["choice"]}
    _state["g7"] = {"verdict": g7["verdict"], "n_tests": g7["n_tests"], "choice_fails": g7["choice_fails"][:5]}
    _state["g10"] = {"verdict": g10["verdict"], "failing": g10["failing"]}
    assert g6["verdict"] == "pass", g6["fails"]
    assert g7["verdict"] == "pass", g7["choice_fails"][:5]
    assert g10["verdict"] == "pass", g10["failing"]


def RUN_g10(build):
    return pilot.g10(build.infos, build.units, _state["kit"].plugin)


def test_probes(build):
    infos = build.infos
    o, f, d, c = PR.options_only(infos), PR.formatting_only(infos), PR.diff_size(infos), PR.cues(infos)
    _state.update(options_only=o, formatting_only=f, diff_size=d, cues=c)
    assert o["pass"], o
    assert f["pass"], f
    assert d["pass"], d


def test_shares_and_tokens(build):
    rows = [i.row for i in build.infos]
    n = len(rows)
    eq = sum(r["meta"]["qform"] == "ch_equiv" for r in rows) / n
    _state["equiv_share"] = round(eq, 4)
    assert 0.22 <= eq <= 0.28                                   # 1,500 output + 500 equivalence = 25%
    toks, how = pilot.real_tokens(rows)
    _state["tokens"] = {"mean": sum(toks) / n, "max": max(toks), "by": how}
    assert sum(toks) / n <= 800 and max(toks) <= 2000
    cards = {}
    for r in rows:
        cards[r["meta"]["card_id"]] = cards.get(r["meta"]["card_id"], 0) + 1
    _state["cards"] = {"n": len(cards), "max_rows": max(cards.values())}
    assert len(cards) >= 30 and max(cards.values()) <= 64
    assert all(not r["meta"]["dev_only"] for r in rows)


def test_reseed_audit(build):
    audited = [i for i in build.infos if uhash(i.row["id"], "reseed") < 0.03]
    assert len(audited) >= max(10, int(0.02 * len(build.infos)))
    flips = 0
    old = E.HASHSEED
    E.HASHSEED = "7"
    try:
        for i in audited:
            st = i.spec.structure
            if st["qform"] == "ch_equiv":
                res = E.run_equiv(st["f"], st["g"], tuple(st["sig"]), seed=P._fuzz_seed(st["f"], st["g"]) ^ 0x9E3779B1)
                flips += E.equiv_label(res)[0] != st["label"]
            else:
                E._SNIP.pop(E._key(st["kind"], st["code"]), None)
                key = E.answer_key(E.run_one(st["code"], st["kind"]))
                flips += key != i.rr.option_set.gold.key
    finally:
        E.HASHSEED = old
    _state["reseed"] = {"audited": len(audited), "flips": flips}
    assert flips <= 0.01 * len(audited), (flips, len(audited))


def test_write_metrics(build):
    _state["build_stats"] = {k: v for k, v in build.stats.items() if k not in ("drop_examples",)}
    _state["n_rows"] = len(build.infos)
    keep = {k: v for k, v in _state.items() if k not in ("b", "kit")}
    RESULTS.write_text(json.dumps(keep, indent=1, default=str), encoding="utf-8")

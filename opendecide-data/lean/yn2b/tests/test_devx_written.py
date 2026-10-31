"""The written devx outputs (yn2b/build_devx.py --write, yn2b/devx_decontam.py --write) are the current build and pass
their gates: yn2b_raw/dev/<key>__devx.jsonl equal a fresh in-memory build row for row; devx_report.json shows 100%
parse-back; devx_blind.json shows 50 blind-solved rows per family; devx_decontam.json is ok. Skips when not written."""
from __future__ import annotations

import json

import pytest

from devx_helpers import KEYS, LEAN, bd, built, mv

REPORT = LEAN / "yn2b" / "devx_report.json"
BLIND = LEAN / "yn2b" / "devx_blind.json"
DECONTAM = LEAN / "yn2b" / "devx_decontam.json"


def _need(p):
    if not p.exists():
        pytest.skip(f"{p.name} not written yet")


@pytest.mark.parametrize("key", KEYS)
def test_written_raw_devx_equals_a_fresh_build(key):
    rp, _ = mv.raw_paths(key, "devx")
    _need(rp)
    rows, rels = mv.read_raw(key, "devx")
    assert rows == json.loads(json.dumps(built()[key].rows, ensure_ascii=False))
    assert rels == []
    for r in rows:
        if r["meta"]["defs"]:
            assert mv.load_defs(key, r["meta"]["defs"]) == built()[key].fb.defs[r["meta"]["defs"]]


def test_written_report_shows_full_parse_back():
    _need(REPORT)
    rep = json.loads(REPORT.read_text())["families"]
    assert set(rep) == set(KEYS)
    for k, v in rep.items():
        assert v["rows"] == 100
        assert {x: v["parse_back"][x] for x in ("rows", "agree", "disagree", "proj_mismatch")} == \
            {"rows": 100, "agree": 100, "disagree": 0, "proj_mismatch": 0}, k


def test_written_blind_solve_covers_50_rows_per_family():
    _need(BLIND)
    res = json.loads(BLIND.read_text())["results"]
    assert set(res) == set(KEYS)
    for k, v in res.items():
        assert v["rows"] == 50, k
        assert v["agree"] == v["rows"] - len(v["misses"])
    answers = json.loads((LEAN / "yn2b" / "devx_blind_answers.json").read_text())
    again = bd.score_blind(built(), answers)
    assert {k: v["agree"] for k, v in again.items()} == {k: v["agree"] for k, v in res.items()}


def test_written_decontam_is_ok():
    _need(DECONTAM)
    rep = json.loads(DECONTAM.read_text())
    assert rep["rows"] == 500 and rep["ok"] is True
    assert rep["7.1_ohs3_hit_units_per_family"] == {} and rep["7.7_names"]["ohs3_hash_hits_per_family"] == {}

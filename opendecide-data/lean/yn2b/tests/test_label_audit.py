"""label_audit.py: statistics, sampling, and the generator re-derivations (the latter on a few real raw rows, read
only; skipped when the raw files are absent)."""
from __future__ import annotations

import json

import pytest

import label_audit as la
from conftest import ch_row, yn_row

RAW = la.RAW


def test_base_index_only_takes_base_rows():
    r = yn_row(1)
    r["id"] = "r_gd_gen_tables_17"
    assert la.base_index(r, "gen_tables") == 17
    for rid, role in (("r_gd_gen_tables_17_ya", "aff"), ("r_gd_gen_tables_17_atk", "attacked"),
                      ("r_gd_gen_tables_17", "defswap")):
        assert la.base_index(dict(r, id=rid, role=role), "gen_tables") is None


def test_golden_matches_raw_maps_codes_by_position():
    raw = {"state": "s", "instructions": "q", "options": ["A", "B", "C"], "gold": "B"}
    g = ch_row(1, opts=("Code 11", "Code 12", "Code 13"), gold="Code 12", state="s", instructions="q")
    assert la.golden_matches_raw(g, raw)[0]
    assert not la.golden_matches_raw(dict(g, gold="Code 11"), raw)[0]
    y = yn_row(2, gold=0, state="s", instructions="q")
    assert la.golden_matches_raw(y, {"state": "s", "instructions": "q", "options": ["yes", "no"], "gold": "no"})[0]


def test_teacher_stats_and_sample_are_deterministic():
    rows = []
    for i in range(60):
        r = yn_row(i, gold=1, teacher=0.3 if i % 3 == 0 else 0.9, source="gd_gen_tables")
        r["id"] = f"r_gd_gen_tables_{i}"
        rows.append(r)
    stats, _ = la.teacher_stats(rows)
    s = stats["gd_gen_tables|noul"]
    assert s["fresh_teacher"] == 60 and s["n_wrong_trained"] == 20
    assert s["mid_before"] == round(20 / 60, 4) and s["mid_after"] == 0.0
    a = la.sample(rows, keys=("gen_tables",), n_yn=5, n_ch=0)
    b = la.sample(rows, keys=("gen_tables",), n_yn=5, n_ch=0)
    assert [r["id"] for r in a["gen_tables"]["rows"]] == [r["id"] for r in b["gen_tables"]["rows"]]
    assert a["gen_tables"]["pool_yes_no"] == 20 and len(a["gen_tables"]["rows"]) == 5


def _first(key, n):
    p = RAW / f"{key}.jsonl"
    if not p.exists():
        pytest.skip(f"{p} not present")
    out = {}
    with open(p) as f:
        for k, line in enumerate(f):
            if k >= n:
                break
            out[k] = json.loads(line)
    return out


def test_rederive_numeric_dates_and_evidence_on_real_rows():
    for key, fn in (("gen_numeric_dates", la.rederive_numeric_dates), ("gen_evidence_conflict", la.rederive_evidence_conflict)):
        raws = _first(key, 4)
        res = fn(raws)
        assert all(v[0] == "ok" for v in res.values()), res
        bad = {0: dict(raws[0], gold="yes" if raws[0]["gold"] != "yes" else "no")}
        if raws[0]["options"] == ["yes", "no"]:
            assert fn(bad)[0][0] in ("MISMATCH", "ERROR")


def test_tables_replay_reproduces_the_raw_file_prefix():
    raws = _first("gen_tables", 6)
    raw_list = [raws[k] for k in sorted(raws)]
    found, compared, err = la.replay_tables({raws[4]["rid"]}, {"__list__": raw_list}, limit_pairs=3)
    assert err is None and compared >= 5 and raws[4]["rid"] in found
    import tab_verify
    P, j = found[raws[4]["rid"]]
    assert tab_verify.check_row(P, j)[0]

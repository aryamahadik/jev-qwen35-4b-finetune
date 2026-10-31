"""Tests for mix_c2.py / c2io.py under Ruling A61.
ADOPTED (A61_ADOPT_r3.md, e / fix 5): the constants and the relay are A42-D's again (rows <= 125,000, C2 Modal total <= $40, T_max = T_core =
min(34, 32 - spend, C - 8), payers mahadikarya2 -> mahadikarya3 only, aryamhd refused), and --final refuses any DI block / DI row (the DI part is 0).
DRAFT, NOT ADOPTED (kept as inert code, tested as written): the DI block registry, the DI entry rules (pilot, joint pilot, G13 readiness), the D1 / D2
trim and the DI checks; those tests set the draft's money / row constants with monkeypatch (draft_constants). In memory only (tmp_path for the
guard); nothing is written to the C2 tree. Run from lean/:
  ../.venv/bin/python -B -m pytest -q c2_build/tests/test_mix_c2_a61.py
"""
from __future__ import annotations

import json
import math
import sys
from collections import Counter
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2B))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import c2io  # noqa: E402
import c2_select as sel  # noqa: E402
import mix_c2 as m  # noqa: E402
from test_mix_c2 import flow  # noqa: E402,F401  (the in-memory build fixture)
from test_mix_c2_a42d import PILOT_OK, QC_OK, add_block, args_for, mk  # noqa: E402

DI = ("DI-KR", "DI-LANG", "DI-TS", "DI-RC", "DI-TOOLS")


@pytest.fixture
def draft_constants(monkeypatch):
    """The A61 DRAFT's money and row constants (T_max = min(39, 37 - spend), 150,000 rows), for the inert DI-trim code only."""
    monkeypatch.setattr(m, "T_MAX_CAP", 39.0)
    monkeypatch.setattr(m, "T_MAX_BASE", 37.0)
    monkeypatch.setattr(m, "ROWS_MAX", 150000)


# ---- registry, constants, accounts -------------------------------------------------------------------------------------
def test_di_blocks_are_registered_in_all_targets_and_the_mixer_but_not_in_the_family_targets():
    assert c2io.DI_BLOCKS == DI == m.DI_BLOCKS
    assert c2io.DI_TARGETS == {"DI-KR": 2400, "DI-LANG": 3600, "DI-TS": 4000, "DI-RC": 0, "DI-TOOLS": 0}
    for b in DI:
        assert b in c2io.ALL_TARGETS and b in sel.TARGETS and b in m.TARGETS     # c2_select, mix_c2 and g13_c2's default blocks
        assert b not in c2io.TARGETS and b not in c2io.BLOCK_TARGETS             # gen_full_c2 / qc_full_c2 build program families only
        assert c2io.tier(b) == "di" and c2io.wave(b) is None
    assert sum(c2io.DI_TARGETS.values()) == c2io.DI_NEW_MAX == m.DI_NEW_MAX == 10000
    assert m.BLOCK_CAPS["DI-LANG"] == 3600 and m.BLOCK_CAPS["DI-TS"] == 4000 and m.BLOCK_CAPS["DI-KR"] == 2400
    assert all(b not in m.AGENT for b in DI)                                     # DI rows are not in the agent tier


def test_a61_adopted_row_and_money_constants_are_a42d_again():
    """A61 (e) / fix 5: ROWS_MAX 125,000, C2 Modal total $40, T_max = T_core = min(34, 32 - spend); the draft's 150,000 / $45 / 39 / 37 are not in force."""
    assert (m.ROWS_MAX, m.CORE_ROWS_MAX) == (125000, 125000)
    assert (m.T_MAX_CAP, m.T_MAX_BASE, m.T_CORE_CAP, m.T_CORE_BASE, m.C2_MODAL_CAP_USD) == (34.0, 32.0, 34.0, 32.0, 40.0)
    assert m.T_MAX_BASE == 40 - 4 - 2 - 2 == m.T_CORE_BASE                              # $40 minus evaluation $4, SPEED-3 $2, reserve $2
    assert m.CREDIT_FIT_RESERVE_USD == 8.0 == 4 + 2 + 2
    assert m.t_max_usd(0) == m.t_core_usd(0) == 32.0 and m.t_max_usd(5) == m.t_core_usd(5) == 27.0
    assert m.t_max_usd(0.5) == m.t_core_usd(0.5) == 31.5


def test_the_credit_fit_only_lowers_t_core():
    """T_core = min(34, 32 - spend, C - 8): C is the live free credit on mahadikarya2 + mahadikarya3 (each less $1)."""
    for fn in (m.t_core_usd, m.t_max_usd):
        assert fn(0, 100.0) == 32.0 and fn(0, None) == 32.0 and fn(0, 40.0) == 32.0       # C - 8 = 32: equal, no change
        assert fn(0, 39.99) == 31.99 and fn(0, 30.93) == 22.93 and fn(2.0, 30.93) == 22.93
        assert fn(10.0, 30.93) == 22.0 and fn(10.0, 35.0) == 22.0                          # spend binds when it is lower
        for c in (None, 31.9, 32.0, 40.0, 45.0, 1000.0):
            for sp in (0.0, 1.5, 8.0, 20.0):
                assert fn(sp, c) <= fn(sp, None) + 1e-9                                      # never raised
        for low in (0.0, 10.0):
            with pytest.raises(SystemExit, match="no training budget"):
                fn(0, low)                                                                    # C - 8 <= 2: below the $2 smoke: stop and ask
        for bad in ("x", float("nan"), float("inf")):
            with pytest.raises(SystemExit):
                fn(0, bad)


def test_relay_accounts_are_exactly_mahadikarya2_then_mahadikarya3_and_never_the_card():
    """A42-D 2.4 (A61 e): free credit first on the mahadikarya2 -> mahadikarya3 relay ONLY; no other account; aryamhd refused."""
    assert m.RELAY_ACCOUNTS == ("mahadikarya2", "mahadikarya3")
    assert m.relay_problems() == []
    assert any("aryamhd" in x for x in m.relay_problems(m.RELAY_ACCOUNTS + ("AryaMHD",)))
    assert any("aryamhd" in x for x in m.relay_problems(("mahadikarya2", "mahadikarya3", "aryamhd")))
    for extra in ("jaypatil-duke", "atmosphor", "arya-mahadik-ai", "mahadikarya44"):
        assert any("not exactly" in x for x in m.relay_problems(m.RELAY_ACCOUNTS + (extra,)))
    assert m.relay_problems(("mahadikarya3", "mahadikarya2")) and m.relay_problems(("mahadikarya2",)) and m.relay_problems(())
    assert m.relay_problems(("a", "a")) and m.relay_problems(("a", ""))


# ---- plan and share checks ---------------------------------------------------------------------------------------------
def test_plan_shares_gives_each_di_block_its_table_cap_and_replays_it():
    p = m.plan_shares({"T28": 2400, "DI-KR": 5000, "DI-LANG": 99999, "DI-TS": 9999, "DI-RC": 10, "DI-TOOLS": 10})
    t = p["targets"]
    assert t["DI-KR"] == 2400 and t["DI-LANG"] == 3600 and t["DI-TS"] == 4000        # not cut to a family's 2,400
    assert t["DI-RC"] == 0 and t["DI-TOOLS"] == 0                                    # the empty blocks hold nothing
    assert p["new"] == 2400 + 10000 and p["replay"] == math.floor(1.5 * p["new"]) and not p["agent_cap"]["applied"]
    assert m.plan_shares({"DI-KR": 100})["replay"] == 150


def test_share_checks_assert_the_150k_mix_the_125k_core_and_the_25k_di_part():
    plan = m.plan_shares({"T28": 2400, "DI-KR": 2400, "DI-LANG": 3600, "DI-TS": 4000})
    by = Counter(plan["targets"]) + Counter({"replay": plan["replay_sampler"]})
    rep, p = m.share_checks(by, plan)
    assert p == [] and rep["di_new"] == 10000 and rep["di_part"] == 25000 and rep["core"] == rep["total"] - 25000
    by2 = by.copy()
    by2["DI-KR"] = 2401                                                              # above the block cap and the plan
    assert any("blocks above their cap" in x for x in m.share_checks(by2, plan)[1])
    by3 = Counter({"DI-KR": 5000, "replay": 7500})                                   # 12,500 DI part, but the block cap is 2,400
    assert any("blocks above their cap" in x for x in m.share_checks(by3, m.plan_shares({"DI-KR": 5000}))[1])
    big = {"T28": 2400, "DI-LANG": 3600}
    plan2 = m.plan_shares(big)
    by4 = Counter(plan2["targets"]) + Counter({"replay": plan2["replay_sampler"]})
    assert m.share_checks(by4, plan2)[1] == []
    # the DI part over 25,000 (more DI new rows than 10,000: the caps were removed) and a core over 125,000
    p_part = m.share_checks(Counter({"DI-TS": 10001, "replay": 15001}), {"targets": {"DI-TS": 10001}})[1]
    assert any("DI part 25,002 rows (10,001 new) above 25,000" in x for x in p_part)
    p_core = m.share_checks(Counter({"T28": 52000, "replay": 84000, "DI-KR": 2000, "DI-LANG": 2000}),   # 56,000 new -> 84,000 replay: 140,000
                            {"targets": {"T28": 52000, "DI-KR": 2000, "DI-LANG": 2000}})[1]               # the DI part is 10,000 of them
    assert any("core 130,000 rows > 125,000" in x for x in p_core) and not any("DI part" in x for x in p_core)


def test_a_mix_with_no_di_row_still_may_not_exceed_the_core_cap(monkeypatch):
    plan = {"targets": {"T28": 60000}}
    by = Counter({"T28": 60000, "replay": 90000})                                    # 150,000 rows, no DI part: the core is above 125,000
    assert any("core 150,000 rows > 125,000" in x for x in m.share_checks(by, plan)[1])
    monkeypatch.setattr(m, "ROWS_MAX", 8000)
    assert any("> 8,000" in x for x in m.share_checks(Counter({"T28": 2400, "replay": 6600}), m.plan_shares({"T28": 2400}))[1])


def row(i, block, **kw):
    r = mk(f"{block}{i}", block, **kw)
    r["qtype"] = kw.get("qtype", "noul")
    return r


def test_di_checks_assert_source_task_and_subsource_caps():
    rows = [row(i, "DI-TS", source=f"t{i // 600}", meta={"task_id": f"k{i // 600}"}) for i in range(1800)]
    rows += [row(i, "DI-LANG", source="di_hover_train") for i in range(2400)] + [row(i, "DI-LANG", source="di_isarcasm_en") for i in range(1200)]
    rep, p = m.di_checks(rows)
    assert p == [] and rep["new"] == 5400 and rep["DI-TS"]["max_rows_per_task"] == 600
    rows2 = rows + [row(9000, "DI-TS", source="t0", meta={"task_id": "k0"})]
    assert any("1 tasks above 600" in x for x in m.di_checks(rows2)[1])
    rows3 = rows + [row(9100, "DI-LANG", source="di_hover_train")]
    assert any("source hover holds 2,401 rows > 2,400" in x for x in m.di_checks(rows3)[1])
    rows4 = rows + [row(9200 + i, "DI-LANG", source="di_isarcasm_en") for i in range(5)]
    assert any("source isarcasm holds 1,205 rows > 1,200" in x for x in m.di_checks(rows4)[1])
    one = [row(i, "DI-KR", source="gsm8k") for i in range(2401)]
    p1 = m.di_checks(one)[1]
    assert any("sources above 2,400" in x for x in p1) and any("> its cap 2,400" in x for x in p1)
    assert m.di_checks([row(1, "T28")])[1] == []


# ---- entry: pilot, the joint pilot, G13 readiness ------------------------------------------------------------------------
def test_a_di_block_needs_a_logged_passing_pilot_like_a_new_family():
    for b in ("DI-KR", "DI-LANG", "DI-TS"):
        assert m.admission(b, QC_OK, [], pilot=PILOT_OK) == []
        assert "no logged pilot verdict" in m.admission(b, QC_OK, [])[0]
        assert any("gain" in x for x in m.admission(b, QC_OK, [], pilot=PILOT_OK | {"own_dev_gain_pt": 1.9}))
        assert any("after" in x for x in m.admission(b, QC_OK, [], pilot=PILOT_OK | {"logged_utc": "2026-10-20T00:00:01Z"}))   # Mon 19 Oct 23:59
        assert m.admission(b, QC_OK | {"passed_utc": "2026-10-21T23:59:00Z"}, [], pilot=PILOT_OK) == []                       # QC: Wed 21 Oct 23:59
    assert m.admission("T28", QC_OK, []) == []


def test_one_failed_joint_pilot_check_moves_every_di_block_out():
    good = {"DI-KR": PILOT_OK, "DI-LANG": PILOT_OK | {"own_dev_gain_pt": 3.1}, "DI-TS": PILOT_OK}
    assert m.di_joint_problems(good) == [] and m.di_joint_problems({}) == []
    bad = dict(good, **{"DI-TS": PILOT_OK | {"existing_dev_drop_pt": 0.51}})
    got = m.di_joint_problems(bad)
    assert got and "DI-TS" in got[0] and "every DI block moves to C2.1" in got[0]
    assert m.di_joint_problems(dict(good, **{"DI-KR": PILOT_OK | {"gproxy_change_ci_upper_pt": -0.51}}))
    assert m.di_joint_problems({"DI-KR": PILOT_OK | {"existing_dev_drop_pt": None}})
    assert m.di_joint_problems({"DI-KR": None}) == []                    # no record: that block fails its own admission already
    assert m.di_joint_problems({"DI-KR": PILOT_OK | {"existing_dev_drop_pt": 0.5, "gproxy_change_ci_upper_pt": -0.5}}) == []   # inclusive bars


class FakeLog:
    def __init__(self, recs):
        self.recs = recs

    def json(self, f):
        return self.recs[f]


def g13_rec(block, scanned=("di03_public", "di_src_splits"), complete=True, run="candidates"):
    return {"run": run, "block": block, "complete": complete,
            "engine": {"targets": {n: {"status": "scanned"} for n in scanned} | {"di_test": {"status": "scanned"}}}}


def test_a_di_block_enters_only_with_both_di_targets_scanned_in_a_complete_candidates_log():
    log = FakeLog({"a": g13_rec("DI-KR"), "b": g13_rec("DI-LANG", scanned=("di03_public",)), "c": g13_rec("DI-TS", complete=False),
                   "d": g13_rec("DI-KR", run="final"), "e": {"not": "a log"}})
    assert m.di_g13_problems(log, ["a", "b", "c", "d", "e"], "DI-KR", pins={}) == []
    got = m.di_g13_problems(log, ["a", "b", "c", "d", "e"], "DI-LANG", pins={})
    assert got and "did not scan ['di_src_splits']" in got[0]
    assert any("not complete" in x for x in m.di_g13_problems(log, ["c"], "DI-TS", pins={}))
    assert "no candidates G13 log" in m.di_g13_problems(log, ["d"], "DI-KR", pins={})[0]      # a final log is not a candidates log
    assert "no candidates G13 log" in m.di_g13_problems(log, [], "DI-KR", pins={})[0]
    log2 = FakeLog({"x": {"run": "candidates", "block": "DI-TS", "complete": True,
                          "engine": {"targets": {"di03_public": {"status": "missing"}, "di_src_splits": {"status": "scanned"}}}}})
    assert "did not scan ['di03_public']" in m.di_g13_problems(log2, ["x"], "DI-TS", pins={})[0]


def test_the_di_quarantine_files_are_never_training_inputs(tmp_path):
    frag = tmp_path / "di_never_train.json"
    f = tmp_path / "di_rows.jsonl"
    f.write_text('{"id": "x"}\n')
    frag.write_text(json.dumps({"files": [{"path": str(f), "sha256": m.sha256_file(f)}], "names": ["di03_public", "di_src_splits"]}))
    base = {"paths": set(), "sha256": set(), "names": set()}
    assert m.merge_di_never_train(base, tmp_path / "absent.json") == base            # nothing written yet: the guard is unchanged
    never = m.merge_di_never_train(base, frag)
    assert str(f.resolve()) in never["paths"] and m.sha256_file(f) in never["sha256"] and {"di03_public", "di_src_splits"} <= never["names"]
    log = m.MixInputLog(never)
    with pytest.raises(c2io.C2Refused):
        log.check(f)
    clone = tmp_path / "copy.jsonl"
    clone.write_text(f.read_text())
    with pytest.raises(c2io.C2Refused):
        log.record(clone)                                                            # a copy is caught by its sha256
    rows = [mk("r1", "DI-KR", source="di_src_splits"), mk("r2", "DI-KR", source="gsm8k_train")]
    assert "di_src_splits': 1" in m.anchor_row_problems(rows, never["names"])[0]


# ---- the trim: core view, D1, D2 ----------------------------------------------------------------------------------------
@pytest.fixture
def di_env(monkeypatch, draft_constants):
    monkeypatch.setattr(m, "project_cost", lambda rows, rels, ntok, seed=m.SEED: {
        "total_usd": round(len(rows) * 0.01, 4), "train_usd": round(len(rows) * 0.01, 4), "rows": len(rows)})
    monkeypatch.setattr(m, "OVERHEAD_USD", 0.0)
    monkeypatch.setattr(m, "FLOOR_ROWS", 100)
    calls = []

    def stub(rows, rels, targets, parts, seed=m.SEED):                              # keep the first t rows of each block
        seen, out = Counter(), []
        for r in rows:
            b = r["_block"]
            if b in targets and seen[b] >= targets[b]:
                continue
            seen[b] += 1
            out.append(r)
        calls.append({"targets": dict(targets), "parts": {b: [p["key"] for p in parts.get(b, [])] for b in targets}})
        ids = {r["id"] for r in out}
        return out, [x for x in rels if x["a"] in ids and x["b"] in ids], {}
    monkeypatch.setattr(m, "apply_targets", stub)
    return calls


def di_mix():
    """1,000 core rows, 1,000 DI-KR rows, 3,000 DI-TS rows (5 tasks of 600): no replay rows (the replay rule is a no-op here)."""
    rows = [mk(f"a{i}", "T28", source="t28") for i in range(1000)]
    rows += [mk(f"k{i}", "DI-KR", source="gsm8k") for i in range(1000)]
    rows += [mk(f"t{i}", "DI-TS", source=f"ts{i // 600}", meta={"task_id": f"task{i // 600}"}) for i in range(3000)]
    return rows


def run_a61(spend, rows, final=False):
    rep, probs = {}, []
    parts = {}
    out, rels = m.budget_trim_a61(args_for(spend, final), rows, [], {}, {}, parts, {}, rep, probs)
    return out, rep, probs, parts


def test_core_view_drops_the_di_rows():
    rows = di_mix()
    core, crel = m.core_view(rows, [], {}, {})
    assert Counter(r["_block"] for r in core) == {"T28": 1000}
    assert m.di_counts(rows) == (4000, 4000 + 6000) and m.di_counts(core) == (0, 0)


def test_trim_di_ts_tail_removes_whole_tasks_above_2000_and_never_below(monkeypatch):
    rows = di_mix()
    out, rels, got, info = m.trim_di_ts_tail(rows, [], 10 ** 6)
    ts = [r for r in out if r["_block"] == "DI-TS"]
    assert got == 600 and len(ts) == 2400 and set(Counter(r["meta"]["task_id"] for r in ts).values()) == {600}     # one whole task
    assert Counter(r["_block"] for r in out)["T28"] == 1000 and Counter(r["_block"] for r in out)["DI-KR"] == 1000
    # 3,000 -> 2,400: the next task (600) would take the block to 1,800, below the 2,000 floor, so it and the others are skipped
    assert info == {"available_before": 1000, "need": 10 ** 6, "removed": 600, "skipped_tasks": 4, "left": 0}
    again = m.trim_di_ts_tail(di_mix(), [], 10 ** 6)[0]
    assert [r["id"] for r in out] == [r["id"] for r in again]                                  # seeded: the same task every time
    picks = {frozenset(r["id"] for r in m.trim_di_ts_tail(di_mix(), [], 600, seed=sd)[0]) for sd in range(1, 9)}
    assert len(picks) > 1                                                                       # another seed, another task
    assert m.trim_di_ts_tail(rows, [], 0)[2] == 0 and m.trim_di_ts_tail([r for r in rows if r["_block"] != "DI-TS"], [], 50)[2] == 0
    short = [r for r in rows if r["_block"] != "DI-TS" or int(r["id"][1:]) < 2000]            # exactly 2,000 DI-TS rows: at the floor
    assert m.trim_di_ts_tail(short, [], 100)[2] == 0


def test_di_proportional_splits_the_trim_over_blocks_and_sources(di_env):
    rows = [mk(f"l{i}", "DI-LANG", source="hover" if i < 800 else "isarcasm") for i in range(1000)]
    rows += [mk(f"k{i}", "DI-KR", source="gsm8k") for i in range(1000)] + [mk(f"a{i}", "T28") for i in range(500)]
    parts = {}
    out, rels, got, info = m.di_proportional(rows, [], 500, parts)
    by = Counter(r["_block"] for r in out)
    assert di_env[0]["targets"] == {"DI-KR": 750, "DI-LANG": 750}                   # block shares kept (largest remainder)
    assert [p["key"] for p in parts["DI-LANG"]] == ["DI-LANG|hover", "DI-LANG|isarcasm"] and [p["key"] for p in parts["DI-KR"]] == ["DI-KR|gsm8k"]
    assert by["T28"] == 500 and by["DI-KR"] == 750 and by["DI-LANG"] == 750 and got == 500 and info["removed"] == 500
    out2, _, got2, info2 = m.di_proportional(rows, [], 10 ** 6, {})                  # more than there is: every DI row goes
    assert got2 == 2000 and Counter(r["_block"] for r in out2) == {"T28": 500} and info2["left"] == 0
    assert m.di_proportional(rows, [], 0, {})[2] == 0 and m.di_proportional([r for r in rows if r["_block"] == "T28"], [], 5, {})[2] == 0


def test_no_di_row_the_trim_is_the_core_trim_against_t_core(di_env):
    rows = [mk(f"a{i}", "T28", source="t28") for i in range(3200)]
    out, rep, probs, _ = run_a61(0.0, rows)
    assert len(out) == 3200 and rep["budget"]["t_max_usd"] == 32.0 and "budget_core" not in rep and probs == []     # $32.00 = T_core: untouched
    out, rep, probs, _ = run_a61(2.0, rows)                                          # T_core 30: trimmed (the A42-D 2.3 rule for the core)
    assert len(out) <= 3000 and rep["budget"]["t_max_usd"] == 30.0 and rep["budget"]["final_total_usd"] <= 30.0


def test_di_part_is_trimmed_after_the_core_d1_then_d2_to_t_max_minus_the_cores_projection(di_env):
    rows = di_mix()                                                                  # core $10, DI 4,000 rows $40: $50 against T_max $37
    out, rep, probs, parts = run_a61(0.0, rows)
    by = Counter(r["_block"] for r in out)
    assert by["T28"] == 1000                                                         # the core fits T_core ($32): untouched
    assert rep["budget"]["final_total_usd"] <= 37.0 + 1e-9 and rep["budget"]["t_max_usd"] == 37.0 and probs == []
    assert rep["budget"]["t_core_usd"] == 32.0 and rep["budget_core"]["rounds"][-1]["total_usd"] == 10.0 and not rep["budget_core"]["trimmed"]
    steps = [s["step"] for rd in rep["budget"]["rounds"] if "trim" in rd for s in rd["trim"]["steps"]]
    assert steps[0] == "di_ts_tail" and steps[1] == "di_proportional"                  # D1 first, D2 after D1 is used up
    d1 = [s for rd in rep["budget"]["rounds"] if "trim" in rd for s in rd["trim"]["steps"] if s["step"] == "di_ts_tail"][0]
    assert d1["removed"] == 600 and d1["left"] == 0                                    # one whole task (the floor of 2,000 stops the rest)
    d2 = [s for rd in rep["budget"]["rounds"] if "trim" in rd for s in rd["trim"]["steps"] if s["step"] == "di_proportional"][0]
    assert d2["removed"] == 700 and d2["keep_by_block"] == {"DI-KR": 794, "DI-TS": 1906}    # 1,300 asked: 600 by D1, 700 by D2
    assert (by["DI-KR"], by["DI-TS"]) == (794, 1906) and len(out) == 3700 and rep["budget"]["final_total_usd"] == 37.0
    assert rep["budget"]["di_proportional_used"] and rep["budget"]["order"][-2:] == ["di_ts_tail", "di_proportional"]
    n, part = m.di_counts(out)
    assert n == by["DI-KR"] + by["DI-TS"] and part <= m.DI_PART_MAX


def test_a_core_over_t_core_is_trimmed_first_then_the_di_part_gets_what_is_left(di_env):
    core = [mk(f"a{i}", "GB", source="gb") for i in range(2500)]
    rows = core + [mk(f"k{i}", "DI-KR", source="gsm8k") for i in range(1500)]       # core $25, DI $15
    out, rep, probs, _ = run_a61(8.0, rows)                                         # T_core 24, T_max 29: core 2,500 -> <= 2,400; whole <= 2,900
    by = Counter(r["_block"] for r in out)
    assert by["GB"] * 0.01 <= 24.0 + 1e-9 and rep["budget_core"]["trimmed"] and rep["budget_core"]["t_max_usd"] == 24.0   # the core meets T_core first
    assert rep["budget_core"]["rounds"][-1]["total_usd"] <= 24.0 and rep["budget"]["t_core_usd"] == 24.0
    assert len(out) * 0.01 <= 29.0 + 1e-9 and rep["budget"]["t_max_usd"] == 29.0
    assert 2899 <= len(out) <= 2900 and by["DI-KR"] == len(out) - by["GB"]         # the DI part keeps exactly what T_max (29) leaves after the core
    assert probs == [] and rep["plan_final"]["targets"]["DI-KR"] == by["DI-KR"]     # the core step 4 scaled core blocks only: DI keeps what it holds


def test_the_di_part_row_caps_bind_without_money(di_env, monkeypatch):
    monkeypatch.setattr(m, "project_cost", lambda rows, rels, ntok, seed=m.SEED: {"total_usd": 1.0, "train_usd": 1.0, "rows": len(rows)})
    rows = [mk(f"a{i}", "T28", source="t28") for i in range(200)]
    rows += [mk(f"t{i}", "DI-TS", source=f"ts{i // 600}", meta={"task_id": f"task{i // 600}"}) for i in range(12000)]
    out, rep, probs, _ = run_a61(0.0, rows)
    n, part = m.di_counts(out)
    assert n <= m.DI_NEW_MAX and part <= m.DI_PART_MAX and probs == []              # 12,000 DI new rows -> <= 10,000 (D1 to 2,000 first)
    steps = [s["step"] for rd in rep["budget"]["rounds"] if "trim" in rd for s in rd["trim"]["steps"]]
    assert steps[0] == "di_ts_tail"


def test_the_50000_row_floor_still_stops_and_asks(di_env, monkeypatch):
    monkeypatch.setattr(m, "FLOOR_ROWS", 10 ** 6)
    rep, probs = {}, []
    rows = di_mix()
    out, _ = m.budget_trim_a61(args_for(0.0), rows, [], {}, {}, {}, {}, rep, probs)
    assert out == rows and any("stop and ask the owner" in x for x in probs)
    with pytest.raises(SystemExit, match="stop and ask the owner"):
        m.budget_trim_a61(args_for(0.0, True), di_mix(), [], {}, {}, {}, {}, {}, [])


# ---- the whole build with a DI block (dry run on fabricated fixtures) -------------------------------------------------------
def test_flow_a_di_block_without_di_g13_evidence_is_left_out_and_the_core_mix_runs(flow, monkeypatch):
    args, writes, inp = flow
    base = m.build(args(spend_to_date=0.0))
    add_block(inp, "DI-KR", 520, 8, "K", 400, monkeypatch)
    rep = m.build(args(spend_to_date=0.0))                                           # no --decontam-drops: di03_public / di_src_splits not shown scanned
    assert "DI-KR" not in rep["selection_digest"]["rows_by_block"]
    assert "no candidates G13 log" in rep["entry"]["left_out"]["DI-KR"][0] and "DI-KR" not in rep["entry"]["entered"]
    assert any("no candidates G13 log" in p for p in rep["problems"])                # a dry run lists it
    assert rep["selection_digest"]["rows_by_block"] == base["selection_digest"]["rows_by_block"]     # A61 e 6: the core mix is unchanged


def test_flow_a_di_block_is_planned_checked_replayed_and_trimmed_after_the_core(flow, monkeypatch, draft_constants):   # the A61 draft's inert DI code
    args, writes, inp = flow
    add_block(inp, "DI-KR", 520, 8, "K", 400, monkeypatch)
    monkeypatch.setattr(m, "di_g13_problems", lambda ilog, files, block: [])        # its candidates log shows both DI targets scanned
    rep = m.build(args(spend_to_date=0.0))
    by = rep["selection_digest"]["rows_by_block"]
    new = sum(n for b, n in by.items() if b != "replay")
    assert by["DI-KR"] > 0 and by["replay"] == math.floor(1.5 * new)                 # DI rows are new rows: one replay rule for the mix
    assert rep["shares"]["di_new"] == by["DI-KR"] and rep["shares"]["di_part"] == by["DI-KR"] + math.floor(1.5 * by["DI-KR"])
    assert rep["di"]["new"] == by["DI-KR"] and rep["relay_accounts"][0] == "mahadikarya2" and rep["core_rows_max"] == 125000
    assert rep["t_max_usd"] == 37.0 and rep["t_core_usd"] == 32.0 and rep["di_part_max"] == 25000
    assert not any("agent tier" in p or "above their planned" in p for p in rep["problems"]), rep["problems"]
    assert "DI-KR" in rep["caps"] and rep["caps"]["DI-KR"]["rows"] == by["DI-KR"]
    first, n_rows = dict(by), sum(by.values())
    core_rows = n_rows - rep["shares"]["di_part"]
    assert core_rows > 0 and rep["shares"]["core"] == core_rows

    def fake_proj(rows, rels, ntok, seed=m.SEED):
        return {"total_usd": round(len(rows) * 0.01, 4), "train_usd": round(len(rows) * 0.01, 4), "rows": len(rows)}
    monkeypatch.setattr(m, "project_cost", fake_proj)
    monkeypatch.setattr(m, "OVERHEAD_USD", 0.0)
    monkeypatch.setattr(m, "FLOOR_ROWS", 100)
    spend = 37.0 - (n_rows * 0.01 - 0.5)                                             # T_max $0.50 below the whole projection; T_core is far above the core
    assert 32.0 - spend >= core_rows * 0.01
    rep2 = m.build(args(spend_to_date=spend))
    b2 = rep2["selection_digest"]["rows_by_block"]
    assert b2["DI-KR"] < first["DI-KR"] and b2["T28"] == first["T28"] and b2["T01"] == first["T01"]     # only the DI part was trimmed
    assert rep2["budget"]["final_total_usd"] <= round(37.0 - spend, 4) + 1e-9 and not rep2["budget_core"]["trimmed"]
    assert b2["replay"] == math.floor(1.5 * (sum(b2.values()) - b2["replay"]))
    steps = [s["step"] for rd in rep2["budget"]["rounds"] if "trim" in rd for s in rd["trim"]["steps"]]
    assert steps and set(steps) <= set(m.DI_TRIM_ORDER) and "item10" not in steps
    assert not any("above their planned" in p or "replay " in p for p in rep2["problems"]), rep2["problems"]
    assert rep2["shares"]["di_new"] == b2["DI-KR"]


def test_flow_without_a_di_block_is_unchanged_by_a61(flow):
    args, writes, inp = flow
    rep = m.build(args())
    assert rep["shares"]["di_new"] == 0 and rep["shares"]["di_part"] == 0 and rep["shares"]["core"] == rep["shares"]["total"]
    assert "budget_core" not in rep and rep["budget"]["t_max_usd"] == 32.0         # trimmed against T_core only

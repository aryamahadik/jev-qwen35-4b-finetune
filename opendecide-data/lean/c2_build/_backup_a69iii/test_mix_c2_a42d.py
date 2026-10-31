"""Tests for the A42-D / A45 changes of mix_c2.py: T_max, the 125,000-row cap, the trim order, the new blocks (G-block,
metadata, replay twins, T40-T44), the A42-D 1.5 caps, the A38 sha, the deadlines and the never-train guard. In memory
only (tmp_path files for the guard); nothing is written to the C2 tree. Run from lean/:
  ../.venv/bin/python -B -m pytest -q c2_build/tests/test_mix_c2_a42d.py
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
from test_c2_select import crowd, fam_rows  # noqa: E402
from test_mix_c2 import flow, row  # noqa: E402,F401  (the in-memory build fixture)

PILOT_OK = {"verdict": "PASS", "logged_utc": "2026-10-19T20:00:00Z", "own_dev_gain_pt": 2.4,
            "existing_dev_drop_pt": 0.3, "gproxy_change_ci_upper_pt": -0.2}
QC_OK = {"pass": True, "passed_utc": "2026-10-19T12:00:00Z", "fix_iterations": 1}


# ---- T_max (A42-D 2.3) -----------------------------------------------------------------------------------------------
def test_t_max_is_t_core_is_min_34_and_32_minus_spend():
    # A42-D 2.3 (A61 e): with the DI part at 0, T_max = T_core = min($34, $32 - C2 Modal spend to date) (and the credit fit, below)
    assert m.t_core_usd(0) == 32.0 and m.t_core_usd(1.5) == 30.5 and m.t_core_usd("8") == 24.0
    assert m.t_core_usd(-0.0) == 32.0
    assert m.t_max_usd(0) == 32.0 and m.t_max_usd(1.5) == 30.5 and m.t_max_usd("8") == 24.0 and m.t_max_usd(-0.0) == 32.0
    assert (m.T_MAX_CAP, m.T_MAX_BASE, m.T_CORE_CAP, m.T_CORE_BASE, m.C2_MODAL_CAP_USD) == (34.0, 32.0, 34.0, 32.0, 40.0)
    assert m.T_MAX_BASE == m.C2_MODAL_CAP_USD - 4 - 2 - 2                      # $40 - evaluation $4 - SPEED-3 $2 - reserve $2
    for fn in (m.t_max_usd, m.t_core_usd):
        for bad in (-1, float("nan"), float("inf"), "x", None):
            with pytest.raises(SystemExit):
                fn(bad)
    with pytest.raises(SystemExit, match="no training budget"):
        m.t_core_usd(30.5)                                       # 1.5 left: below the $2 smoke
    with pytest.raises(SystemExit, match="no training budget"):
        m.t_max_usd(30.5)
    assert not hasattr(m, "BUDGET_USD")                          # the old $17 threshold is gone


def test_spend_to_date_is_a_required_argument():
    with pytest.raises(SystemExit):
        m.main(["--dry-run"])


def test_budget_factor_uses_t_max_and_the_row_cap():
    f = m.budget_factor({"total_usd": 32.0}, t_max=17.0)
    assert abs(f - 15.0 / 30.0) < 1e-9
    assert m.budget_factor({"total_usd": 10.0}, t_max=30.0) == 1.0
    assert abs(m.budget_factor({"total_usd": 10.0}, t_max=30.0, rows=150000) - 125000 / 150000) < 1e-9   # the 125,000 cap
    assert abs(m.budget_factor({"total_usd": 10.0}, t_max=30.0, rows=150000, rows_max=m.ROWS_MAX) - 125000 / 150000) < 1e-9   # ROWS_MAX is 125,000 again (A61 e)
    assert m.budget_factor({"total_usd": 10.0}, t_max=30.0, rows=125000, rows_max=m.ROWS_MAX) == 1.0


# ---- deadlines, pilot gate, the A38 sha --------------------------------------------------------------------------------
def test_cutoff_constant_and_new_family_deadline():
    assert m.CUTOFF_UTC == "2026-10-21T23:59:00+00:00"           # A39 g / A42-D 1.6 (Wed 21 Oct), not Tue 20 Oct
    assert m.deadline_for("T28") == m.CUTOFF_UTC and m.deadline_for("T40") == m.CUTOFF_UTC and m.NEW_FAMILY_DEADLINE_UTC < m.CUTOFF_UTC
    assert m.admission("T28", QC_OK | {"passed_utc": "2026-10-21T23:59:00Z"}, []) == []
    assert "after the data cutoff" in m.admission("T28", QC_OK | {"passed_utc": "2026-10-22T00:00:00Z"}, [])[0]


def test_new_family_needs_a_logged_passing_pilot_verdict():
    assert m.admission("T40", QC_OK, [], pilot=PILOT_OK) == []
    assert "no logged pilot verdict" in m.admission("T40", QC_OK, [])[0]
    assert m.admission("T28", QC_OK, []) == []                                   # the 17 families need no pilot verdict
    assert any("after" in x for x in m.admission("T41", QC_OK | {"passed_utc": "2026-10-22T00:00:00Z"}, [],
                                                 pilot=PILOT_OK))               # QC after Wed 21 Oct: out (A42-D 1.6)
    assert m.admission("T41", QC_OK | {"passed_utc": "2026-10-20T12:00:00Z"}, [], pilot=PILOT_OK) == []  # QC: 21 Oct
    for bad, frag in ((PILOT_OK | {"verdict": "FAIL"}, "not PASS"),
                      (PILOT_OK | {"logged_utc": "2026-10-20T00:00:00Z"}, "after"),
                      (PILOT_OK | {"own_dev_gain_pt": 1.99}, "gain"),
                      (PILOT_OK | {"existing_dev_drop_pt": 0.51}, "existing dev drop"),
                      (PILOT_OK | {"gproxy_change_ci_upper_pt": -0.51}, "rejected"),
                      (PILOT_OK | {"own_dev_gain_pt": True}, "gain"),
                      (PILOT_OK | {"gproxy_change_ci_upper_pt": None}, "rejected"),
                      ({k: v for k, v in PILOT_OK.items() if k != "logged_utc"}, "logged_utc")):
        got = m.pilot_problems("T42", bad)
        assert got and any(frag in x for x in got), (bad, got)
    assert m.pilot_problems("T42", PILOT_OK | {"own_dev_gain_pt": 2.0, "existing_dev_drop_pt": 0.5,
                                                "gproxy_change_ci_upper_pt": -0.5}) == []       # the bars are inclusive


def test_ohs4_sha_is_the_a38_sha_and_appears_in_the_a38_block():
    sha = "c0217e7739c570b9d22176b68e1c489623dcd5f7c551011606b6ff17e59c09c3"
    assert m.OHS4_MANIFEST_SHA256 == sha
    text = c2io.PREREG.read_text(encoding="utf-8")
    assert sha in m.a38_block(text) and m.ohs4_problem(sha, text) is None


def test_minimum_to_train_ignores_the_new_families():
    core = ["T28", "T33", "T29", "T30", "T27"]
    ok, d = m.minimum_to_train(core + ["T35", "T31", "T01", "T23", "T40", "T41", "T42", "T43", "T44", "GB"])
    assert not ok and d["program_n"] == 9                      # T40-T44 / GB never count toward the 10 (A42-D 1.6)


# ---- plan_shares with the new blocks ----------------------------------------------------------------------------------
BASE = dict(c2io.TARGETS)
NEWF = dict(m.NEW_FAMILIES)


def test_budgets_and_registry():
    assert NEWF == {"T40": 1333, "T41": 1166, "T42": 1333, "T43": 1166, "T44": 833, "T45": 833} and "T45" in m.TARGETS
    assert sum(NEWF.values()) == 6664 <= m.NEW_FAMILY_ROWS_MAX == 6666
    assert all(b in m.AGENT for b in NEWF) and "GB" not in m.AGENT and "T37b" not in m.AGENT
    legacy = ("GB", "GW", "MD", "RTW", "I10")                                       # (blocks added later by other rulings are not asserted here)
    assert {b: m.BLOCK_CAPS[b] for b in legacy} == {"GB": 15000, "GW": 9200, "MD": 12000, "RTW": 10000, "I10": 5000}
    assert m.ROWS_MAX == 125000 == m.CORE_ROWS_MAX                                  # A40 d / A42-D 1.4 (A61 e: the draft's 150,000 is not adopted)
    assert m.DI_PART_MAX == 25000 and m.DI_NEW_MAX == 10000                         # the A61 draft's DI machinery, inert (DI rows 0)


def test_full_a42d_plan_is_40_60_and_inside_125k():
    real = BASE | NEWF | {"GB": 15000, "MD": 12000, "RTW": 8000}
    p = m.plan_shares(real)
    assert p["targets"]["GB"] == 15000 and p["targets"]["MD"] == 12000 and p["targets"]["RTW"] == 8000
    assert p["new"] == 26600 + 6664 + 15000 + 12000 == 60264 and p["replay"] == math.floor(1.5 * p["new"])
    assert p["replay_twins"] == 8000 and p["replay_sampler"] == p["replay"] - 8000
    agent = sum(n for b, n in p["targets"].items() if b in m.AGENT)
    assert agent == 13600 + 6664 and 9 * agent <= 11 * (p["new"] - agent) and not p["agent_cap"]["applied"]
    assert p["total"] == p["new"] + p["replay"] == 150660 > m.ROWS_MAX          # the 125,000 cap is the trim's job


def test_family_cap_does_not_apply_to_blocks_and_replay_twins_stay_inside_10k_with_t37b():
    p = m.plan_shares({"T28": 5000, "GB": 99999, "MD": 99999, "RTW": 99999, "T37b": 2000})
    assert p["targets"]["T28"] == 2400 and p["targets"]["GB"] == 15000 and p["targets"]["MD"] == 12000
    assert p["targets"]["RTW"] == 8000                                          # 10,000 - the original T37b 2,000
    assert p["new"] == 2400 + 15000 + 12000 + 2000                             # RTW is replay-side, not new
    assert p["replay"] == math.floor(1.5 * p["new"]) and p["replay_sampler"] == p["replay"] - 8000
    assert m.plan_shares({"T01": 100, "RTW": 500})["replay_sampler"] == max(0, 150 - 500)


def test_agent_cap_scales_t40_t44_down_first_in_proportion():
    real = {"T28": 2400, "T33": 2400, "T29": 2000, "T40": 1333, "T41": 1166, "T42": 1333, "T43": 1166, "T44": 833,
            "T45": 833, "T01": 1600, "T23": 800, "GB": 6000}
    p = m.plan_shares(real)
    other = 1600 + 800 + 6000
    a = sum(n for b, n in p["targets"].items() if b in m.AGENT)
    assert p["agent_cap"]["applied"] and 9 * a <= 11 * other and a + 1 > 0.55 * (a + 1 + other)
    assert all(p["targets"][b] == real[b] for b in ("T28", "T33", "T29"))        # the older agent families untouched
    assert all(p["targets"][b] < real[b] for b in NEWF) and "new_family_cut" in p["agent_cap"]
    assert "by_family" not in p["agent_cap"]
    tiny = m.plan_shares(real | {"GB": 0, "T01": 0, "T23": 0, "T44": 0})         # the new families alone cannot cure it
    assert "by_family" in tiny["agent_cap"] and tiny["targets"]["T40"] == 0 and tiny["new"] == 0


def test_new_families_together_never_above_6666():
    p = m.plan_shares({b: 2400 for b in NEWF} | {"GB": 15000, "MD": 12000, "T01": 1600})
    assert sum(p["targets"][b] for b in NEWF) <= m.NEW_FAMILY_ROWS_MAX
    assert m.scale_plan(BASE | NEWF | {"GB": 15000, "MD": 12000, "RTW": 8000}, 0.5)["new"] == 60264 // 2


# ---- fabricated blocks ------------------------------------------------------------------------------------------------
def mk(rid, block, **kw):
    r = {"id": rid, "call_id": kw.pop("call_id", rid), "_block": block, "source": kw.pop("source", "s"),
         "qtype": "noul", "gold": kw.pop("gold", 1), "options": None, "card": kw.pop("card", "x"),
         "meta": kw.pop("meta", {})}
    return r | kw


def meta_rows(n_src=12, tasks=6, per_task=25, tag="MD"):
    """12 sources x 6 tasks x 25 rows; source s in domain d(s % 10); 50% of the tasks card-free (source 0: 2 of 6)."""
    rows = []
    for s in range(n_src):
        for t in range(tasks):
            free = t < 2 if s == 0 else t % 2 == 0
            for i in range(per_task):
                rows.append(mk(f"{tag}_s{s}_t{t}_{i}", "MD", source=f"src{s}", gold=i % 2, card="" if free else "card",
                               meta={"task_id": f"s{s}t{t}", "domain": f"d{s % 10}"}))
    return rows


def test_trim_meta_tail_removes_whole_tasks_keeps_8_2_rules_and_the_floor(monkeypatch):
    monkeypatch.setattr(m, "META_MIN_ROWS", 1200)
    rows = meta_rows()
    assert len(rows) == 1800
    out, rels, got, info = m.trim_meta_tail(rows, [], 10 ** 6)
    assert len(out) == 1800 - got and len(out) >= 1200 and got % 25 == 0 and got <= 600
    left = Counter((r["meta"]["task_id"]) for r in out)
    assert set(left.values()) == {25}                                           # whole tasks only
    rep, probs = m.block_rules("MD", out, proportional_trim=False)
    assert probs == [] and rep["card_free_min"] >= 0.3 and rep["domains"] >= 8 and rep["max_source_share"] <= 0.15
    free0 = sum(1 for r in out if r["source"] == "src0" and not r["card"]) / sum(1 for r in out if r["source"] == "src0")
    assert free0 >= 0.3                                                         # source 0 sat at 33%: the guard held it
    out2, _, got2, _ = m.trim_meta_tail(meta_rows(), [], 10 ** 6)
    assert [r["id"] for r in out] == [r["id"] for r in out2]                    # seeded: the same tasks every time
    out3, _, _, _ = m.trim_meta_tail(meta_rows(), [], 300, seed=1)
    out4, _, _, _ = m.trim_meta_tail(meta_rows(), [], 300, seed=2)
    assert {r["id"] for r in out3} != {r["id"] for r in out4} and len(out3) == 1800 - 300
    assert m.trim_meta_tail(rows, [], 0)[2] == 0 and m.trim_meta_tail(rows[:1200], [], 50)[2] == 0   # at the floor: none


def test_trim_meta_tail_skips_a_task_that_would_break_the_source_rule(monkeypatch):
    monkeypatch.setattr(m, "META_MIN_ROWS", 100)
    monkeypatch.setattr(m, "META_DOMAINS_MIN", 2)
    rows = []
    for s, n_tasks in (("big", 6), ("a", 2), ("b", 2), ("c", 2), ("d", 2), ("e", 2), ("f", 2), ("g", 2), ("h", 2)):
        for t in range(n_tasks):
            rows += [mk(f"{s}{t}_{i}", "MD", source=s, card="", meta={"task_id": f"{s}{t}", "domain": f"d{s}"})
                     for i in range(10)]
    out, _, got, _ = m.trim_meta_tail(rows, [], 10 ** 6)
    n, big = len(out), sum(1 for r in out if r["source"] == "big")
    assert 60 / 220 > 0.15                                                       # the block starts outside the source rule
    assert big <= 0.15 * n + 1e-9 and got > 0 and Counter(r["source"] for r in out)["a"] > 0   # nothing emptied
    assert len(out) >= 100 and set(Counter(r["meta"]["task_id"] for r in out).values()) == {10}


def test_fit_block_enforces_twin_size_and_domain_caps_with_whole_units(monkeypatch):
    monkeypatch.setitem(m.TWIN_CAP, "GB", 20)
    monkeypatch.setitem(m.BLOCK_CAPS, "GB", 150)
    rows, rels = [], []
    for u in range(100):
        dom = "d0" if u < 50 else f"d{1 + u % 9}"
        base = mk(f"b{u}", "GB", call_id=f"c{u}", meta={"domain": dom, "card_id": f"k{u % 5}"})
        rows.append(base)
        tw = mk(f"t{u}", "GB", call_id=f"c{u}", gold=0, meta={"domain": dom, "card_id": f"k{u % 5}",
                                                                  "twin_of": f"b{u}"})
        rows.append(tw)
        rels.append({"a": f"b{u}", "b": f"t{u}", "type": "complement"})
    out, orels, info = m.fit_block("GB", rows, rels)
    twins = sum(1 for r in out if m.is_twin(r))
    dc = Counter(m.dom_of(r) for r in out)
    assert twins <= 20 and len(out) <= 150 and max(dc.values()) <= 0.2 * len(out) + 1e-9 and "unfixable" not in info
    ids = {r["id"] for r in out}
    assert all(("b" + r["id"][1:] in ids) == ("t" + r["id"][1:] in ids) for r in out)    # whole units: base with its twin
    assert all(x["a"] in ids and x["b"] in ids for x in orels)
    assert {r["id"]: r["gold"] for r in out} == {r["id"]: r["gold"] for r in rows if r["id"] in ids}   # nothing relabelled
    rep, p = m.block_rules("GB", out)
    assert not any("twin" in x or "domain" in x or "rows >" in x for x in p), p
    out2 = m.fit_block("GB", rows, rels)[0]
    assert [r["id"] for r in out] == [r["id"] for r in out2]


def test_block_rules_flag_every_a42d_8_and_5_rule(monkeypatch):
    rows = meta_rows()
    assert m.block_rules("MD", rows, loaded=False)[1] == [] or all("rows <" in x for x in m.block_rules("MD", rows)[1])
    p = m.block_rules("MD", rows, loaded=True)[1]
    assert any("tasks per source" in x for x in p) and any("rows < 8,000" in x for x in p)   # 6 tasks < 40; 1,800 < 8,000
    assert not any("rows < 8,000" in x for x in m.block_rules("MD", rows, proportional_trim=True)[1])
    skew = [r | {"source": "src0"} for r in rows[:600]] + rows[600:]
    assert any("source src0 holds" in x for x in m.block_rules("MD", skew, proportional_trim=True)[1])
    dom = [r | {"meta": r["meta"] | {"domain": "d0"}} for r in rows[:500]] + rows[500:]
    assert any("domain d0 holds" in x for x in m.block_rules("MD", dom, proportional_trim=True)[1])
    paid = [r | {"card": "c"} for r in rows]
    assert any("card-free" in x for x in m.block_rules("MD", paid, proportional_trim=True)[1])
    few = [r for r in rows if r["meta"]["domain"] in ("d0", "d1", "d2")]
    assert any("domains <" in x for x in m.block_rules("MD", few, proportional_trim=True)[1])
    fat = [r | {"meta": r["meta"] | {"task_id": "one"}} for r in rows[:300]] + rows[300:]
    assert any("tasks above 200 rows" in x for x in m.block_rules("MD", fat, proportional_trim=True)[1])
    gb = [mk(f"g{i}", "GB", gold=1, meta={"domain": f"d{i % 6}", "card_id": "k0"}) for i in range(30)]
    assert any("yes share outside" in x for x in m.block_rules("GB", gb)[1])
    monkeypatch.setitem(m.TWIN_CAP, "GB", 5)
    tw = [mk(f"g{i}", "GB", gold=i % 2, meta={"domain": f"d{i % 6}", "card_id": f"k{i}", "twin_of": "x"}) for i in range(30)]
    assert any("negation-twin rows" in x for x in m.block_rules("GB", tw)[1])
    monkeypatch.setitem(m.BLOCK_CAPS, "GB", 10)
    assert any("rows > 10" in x for x in m.block_rules("GB", tw)[1])


# ---- the trim order (A42-D 2.3) ---------------------------------------------------------------------------------------
def trim_rows():
    rows = [mk(f"i{i}", "I10", source="i10") for i in range(100)] + [mk(f"w{i}", "T44", source="t44") for i in range(300)]
    rows += meta_rows() + [mk(f"a{i}", "T28", source="t28") for i in range(1000)]
    return rows


def args_for(spend, final=False):
    return type("A", (), {"final": final, "spend_to_date": spend})()


@pytest.fixture
def trim_env(monkeypatch):
    monkeypatch.setattr(m, "project_cost", lambda rows, rels, ntok, seed=m.SEED: {
        "total_usd": round(len(rows) * 0.01, 4), "train_usd": round(len(rows) * 0.01, 4), "rows": len(rows)})
    monkeypatch.setattr(m, "OVERHEAD_USD", 0.0)
    monkeypatch.setattr(m, "FLOOR_ROWS", 100)
    monkeypatch.setattr(m, "META_MIN_ROWS", 1200)
    calls = []

    def stub(rows, rels, targets, parts, seed=m.SEED):             # spec 5.5 step: keep the first t rows of each block
        seen, out = Counter(), []
        for r in rows:
            b = r["_block"]
            if b in targets and seen[b] >= targets[b]:
                continue
            seen[b] += 1
            out.append(r)
        calls.append(dict(targets))
        return out, rels, {}
    monkeypatch.setattr(m, "apply_targets", stub)
    return calls


def run_trim(spend, rows=None):
    rep, probs = {}, []
    out, rels = m.budget_trim(args_for(spend), rows or trim_rows(), [], {}, {}, {}, {}, rep, probs)
    return out, rep, probs


def steps_of(rep):
    return [[s["step"] for s in rd["trim"]["steps"]] for rd in rep["budget"]["rounds"] if "trim" in rd]


def test_small_overrun_trims_item_10_rows_first_and_only(trim_env):
    out, rep, probs = run_trim(0.3)                                   # T_max 31.7 against 32.0
    by = Counter(r["_block"] for r in out)
    assert 0 < by["I10"] < 100 and by["T44"] == 300 and by["MD"] == 1800 and by["T28"] == 1000
    assert all(s == ["item10"] for s in steps_of(rep)) and rep["budget"]["final_total_usd"] <= 31.7 and probs == []
    assert not rep["budget"]["proportional_used"] and trim_env == []


def test_trim_order_is_item10_wave2_metadata_tail_then_proportional(trim_env):
    out, rep, probs = run_trim(12.0)                                  # T_max 20: 3,200 rows must become 2,000
    by = Counter(r["_block"] for r in out)
    assert by["I10"] == 0 and by["T44"] == 0 and by["MD"] <= 1200            # each step used up before the proportional trim
    tails = [s for rd in rep["budget"]["rounds"] if "trim" in rd for s in rd["trim"]["steps"] if s["step"] == "meta_tail"]
    assert tails and tails[-1]["left"] == 0 and sum(s["removed"] for s in tails) == 600   # metadata went to its floor
    assert rep["budget"]["proportional_used"] and len(out) <= 2000 and probs == []
    assert rep["budget"]["final_total_usd"] <= 20.0 and trim_env
    seq = [s for st in steps_of(rep) for s in st if s != "proportional"]
    order = {"item10": 0, "wave2": 1, "meta_tail": 2}
    idx = [order[s] for s in seq]
    assert idx == sorted(idx)                                                 # never a later step before an earlier one
    flat = [s for st in steps_of(rep) for s in st]
    assert flat.index("proportional") > max(flat.index(s) for s in ("item10", "wave2", "meta_tail"))
    assert {"item10", "wave2", "meta_tail"} <= set(rep["budget"]["exhausted_steps"])
    assert set(trim_env[0]) <= {"T28", "MD"}                                  # the proportional plan names what is left


def test_wave_2_goes_before_metadata_and_in_proportion(trim_env):
    rows = [mk(f"w{i}", "T44", source="t") for i in range(300)] + [mk(f"x{i}", "T45", source="t") for i in range(100)]
    out, rels, got, info = m.trim_blocks(rows, [], {"T44", "T45"}, 100, "wave2")
    by = Counter(r["_block"] for r in out)
    assert got == 100 and by["T44"] == 225 and by["T45"] == 75              # 3 : 1, largest remainder
    assert m.trim_blocks(rows, [], {"T44", "T45"}, 10 ** 6, "wave2")[3]["left"] == 0
    assert m.trim_blocks([], [], {"I10"}, 50, "item10")[3] == {"available_before": 0, "need": 50, "removed": 0, "left": 0}


def test_trim_is_seeded_whole_unit_removal(trim_env):
    rows = [mk(f"w{i}", "T44", call_id=f"c{i // 2}") for i in range(300)]          # units of 2
    rels = [{"a": f"w{2 * k}", "b": f"w{2 * k + 1}", "type": "complement"} for k in range(150)]
    out, orels, got, _ = m.trim_blocks(rows, rels, {"T44"}, 51, "wave2")
    assert got % 2 == 0 and got >= 51 and len(out) == 300 - got
    ids = {r["id"] for r in out}
    assert all((x["a"] in ids) == (x["b"] in ids) for x in rels) and all(x["a"] in ids for x in orels)
    again = m.trim_blocks(rows, rels, {"T44"}, 51, "wave2")[0]
    other = m.trim_blocks(rows, rels, {"T44"}, 51, "wave2", seed=7)[0]
    assert [r["id"] for r in out] == [r["id"] for r in again] and {r["id"] for r in out} != {r["id"] for r in other}


def test_core_row_cap_125000_trims_with_money_inside_t_core(trim_env, monkeypatch):
    monkeypatch.setattr(m, "CORE_ROWS_MAX", 3000)                     # A61 (f): the core keeps the 125,000 cap (the mix's is 150,000)
    out, rep, probs = run_trim(0.0)                                   # 3,200 rows cost $32.0 = T_core: only the row cap binds
    assert len(out) <= 3000 and rep["budget"]["rows_max"] == 3000 and probs == []
    assert Counter(r["_block"] for r in out)["T28"] == 1000 and steps_of(rep)[0][0] == "item10"
    monkeypatch.setattr(m, "CORE_ROWS_MAX", 125000)
    assert run_trim(0.0)[1]["budget"]["trimmed"] is False             # inside both limits: untouched


def test_below_50000_rows_it_stops_and_asks(trim_env, monkeypatch):
    monkeypatch.setattr(m, "FLOOR_ROWS", 10 ** 6)
    rep, probs = {}, []
    rows = trim_rows()
    out, _ = m.budget_trim(args_for(12.0), rows, [], {}, {}, {}, {}, rep, probs)
    assert out == rows and "stop and ask the owner" in probs[0] and "stopped" in rep["budget"]
    with pytest.raises(SystemExit, match="stop and ask the owner"):
        m.budget_trim(args_for(12.0, final=True), trim_rows(), [], {}, {}, {}, {}, {}, [])


def test_money_overrun_after_all_steps_is_a_problem_not_silent(trim_env, monkeypatch):
    monkeypatch.setattr(m, "BUDGET_ROUNDS", 1)
    rep, probs = {}, []
    out, _ = m.budget_trim(args_for(12.0), trim_rows(), [], {}, {}, {}, {}, rep, probs)
    assert any("T_max" in x for x in probs) or rep["budget"]["final_total_usd"] <= 20.0


# ---- caps asserted on realised numbers (A42-D 1.5) ----------------------------------------------------------------------
def test_share_checks_count_replay_twins_inside_the_replay_budget():
    real = {"T28": 2400, "T01": 1600, "T40": 1000, "GB": 3000, "RTW": 800, "T37b": 500}
    plan = m.plan_shares(real)
    by = Counter({b: n for b, n in plan["targets"].items()} | {"replay": plan["replay_sampler"]})
    rep, p = m.share_checks(by, plan)
    assert p == [] and rep["replay"] == [plan["replay"], plan["replay"]] and rep["replay_twins"] == 800
    by2 = by.copy()
    by2["replay"] -= 5
    assert any("floor(1.5 x" in x for x in m.share_checks(by2, plan)[1])
    by3 = by.copy()
    by3["GB"] = 15001
    assert any("blocks above their cap" in x for x in m.share_checks(by3, plan)[1])
    by4 = by.copy()
    by4["RTW"], by4["T37b"] = 9000, 2000
    assert any("T37b + RTW" in x for x in m.share_checks(by4, plan | {"targets": plan["targets"] | {"RTW": 9000}})[1])


def test_share_checks_total_new_share_family_cap_and_new_family_cap(monkeypatch):
    plan = m.plan_shares({"T28": 2400, "T01": 1600})
    by = Counter({"T28": 2400, "T01": 1600, "replay": 6000})
    monkeypatch.setattr(m, "ROWS_MAX", 9000)
    assert any("> 9,000" in x for x in m.share_checks(by, plan)[1])
    by = Counter({"T28": 2400, "T01": 1600, "replay": 5990})            # replay below floor(1.5 x new) = 6000
    p = m.share_checks(by, plan)[1]
    assert any("floor(1.5 x" in x for x in p) and any("> 40%" in x for x in p)
    plan2 = m.plan_shares({"T40": 1333, "T41": 1166, "T42": 1333, "T43": 1166, "T44": 833, "T01": 3000, "GB": 5000})
    big = Counter({"T40": 2000, "T41": 2000, "T42": 2000, "T43": 1000, "T01": 3000, "GB": 5000, "replay": 20000})
    p = m.share_checks(big, plan2)[1]
    assert any("T40-T45 hold" in x for x in p) and any("above their planned" in x for x in p)
    huge = Counter({"T40": 2401, "replay": 3601})
    assert any("families above 2,400" in x for x in m.share_checks(huge, m.plan_shares({"T40": 1333}))[1])


def test_cap_checks_new_families_rows_per_card_and_twin_report():
    rows = [row(i, "T40", "noul" if i % 2 else "choice", card_id=f"k{i % 2}") for i in range(140)]   # 70 rows per card
    rows += [row(i, "T28", "noul" if i % 2 else "choice", card_id=f"k{i % 3}") for i in range(120)]   # 40 per card
    rep, p = m.cap_checks(rows, {r["id"]: 600 for r in rows})
    assert rep["T40"]["max_rows_per_card"] == 70 and any("T40: a card holds 70 rows > 64" in x for x in p)
    assert not any("T28: a card" in x for x in p) and rep["T28"]["twin_rows"] == 0
    rows2 = [row(i, "T44", "noul" if i % 2 else "choice", card_id=f"k{i % 4}") for i in range(64 * 4)]
    assert not any("a card holds" in x for x in m.cap_checks(rows2, {r["id"]: 600 for r in rows2})[1])    # 64 is allowed
    tw = [row(i, "GB", "noul", twin_of="b") for i in range(5)] + [row(10 + i, "GB", "noul") for i in range(5)]
    assert m.cap_checks(tw, {r["id"]: 600 for r in tw})[0]["GB"]["twin_rows"] == 5


def test_agent_tier_and_free_form_caps_cover_the_new_families():
    rows = [row(i, "T41", "noul" if i % 2 else "choice") for i in range(100)]
    for r in rows[:30]:
        r["meta"]["c2"] = {"author_mode": "F"}                            # 30% free-form > 25% (T41 is not T07/T32)
    assert any("T41: free-form rows 0.300" in x for x in m.cap_checks(rows, {r["id"]: 700 for r in rows})[1])
    long = [row(i, "T43", "noul" if i % 2 else "choice") for i in range(10)]
    tok = {r["id"]: 2100 for r in long}
    p = " | ".join(m.cap_checks(long, tok)[1])
    assert "10 new rows over 2000 tokens" in p and "mean 2100.0" in p
    plan = m.plan_shares({"T28": 1000, "T40": 1000, "T01": 1000})
    by = Counter({"T28": 1000, "T40": 1000, "T01": 1000, "replay": 4500})
    assert any("agent tier" in x for x in m.share_checks(by, plan | {"targets": {"T28": 1000, "T40": 1000, "T01": 1000}})[1])


# ---- the never-train guard (A42-D 13.1) ---------------------------------------------------------------------------------
def test_training_inputs_never_include_ohs_paths_gproxy_or_anchors(tmp_path):
    for bad in ("/r/lean/data/ohs3_x/a.jsonl", "/r/lean/data/ohs3_parts/a.jsonl", "/r/lean/ohs4_sealed/x.json",
                "/r/lean/ohs_ac_sealed/y.json", "/r/lean/data/OHS3_parts/z"):
        assert m.train_path_problem(bad), bad
    assert m.train_path_problem("/r/lean/data/c2_parts/T28/out/candidates_c2.jsonl") is None
    gp, man = tmp_path / "gproxy.jsonl", tmp_path / "never_train.json"
    gp.write_text('{"id": "g1"}\n')
    anchor = tmp_path / "anchor.jsonl"
    anchor.write_text('{"id": "a1"}\n')
    clone = tmp_path / "clone.jsonl"
    clone.write_text(anchor.read_text())
    man.write_text(json.dumps({"anchors": [{"name": "BFCL", "path": str(anchor), "sha256": m.sha256_file(anchor)}],
                               "files": [str(tmp_path / "other.jsonl")], "sources": ["injecagent"]}))
    never = m.load_never_train(man, gp)
    assert str(gp.resolve()) in never["paths"] and str(anchor.resolve()) in never["paths"]
    assert m.sha256_file(gp) in never["sha256"] and {"bfcl", "injecagent"} <= never["names"]
    assert m.train_path_problem(gp, never["paths"]) and m.train_path_problem(anchor, never["paths"])
    assert m.train_path_problem(clone, never["paths"], never["sha256"], m.sha256_file(clone))
    log = m.MixInputLog(never)
    with pytest.raises(c2io.C2Refused):
        log.check(gp)
    with pytest.raises(c2io.C2Refused):
        log.record(clone)                                                  # a copy of an anchor is caught by its sha256
    ok = tmp_path / "fine.jsonl"
    ok.write_text('{"id": "f"}\n')
    assert log.record(ok) == ok
    rows = [mk("x1", "T28", source="bfcl_v4"), mk("x2", "T28", source="gd_other"),
            mk("x3", "T28", meta={"text_source": {"dataset": "InjecAgent"}})]
    assert "bfcl': 1" in m.anchor_row_problems(rows, never["names"])[0] and m.anchor_row_problems(rows, set()) == []


def test_training_globs_drop_sealed_paths(tmp_path):
    d = tmp_path / "counts"
    d.mkdir()
    for n in ("c2_a.json", "c2_b.json", "ohs3_hits.json"):
        (d / n).write_text("{}")
    sub = tmp_path / "ohs3_parts"
    sub.mkdir()
    (sub / "c2_c.json").write_text("{}")
    kept, out = m.filter_train_globs([str(d / "*.json"), str(sub / "c2_c.json")])
    assert [Path(k).name for k in kept] == ["c2_a.json", "c2_b.json"]
    assert {Path(o).name for o in out} == {"ohs3_hits.json", "c2_c.json"}


# ---- the whole flow with the new blocks (dry run on fabricated fixtures) ------------------------------------------------
def add_block(inp, fam, n_units, seed, prefix, target, monkeypatch, tweak=None):
    rows, rels = fam_rows(fam, n_units=n_units, seed=seed, prefix=prefix)
    for r in rows:
        r["meta"]["licence"] = "CC0 1.0 (program-generated; Claude/Haiku-authored wording)"
        if tweak:
            tweak(r)
    pg = crowd(rows, seed=seed)
    for t in range(target, target - 60, -1):
        rec = sel.select_family(fam, rows, rels, pg, t)
        if rec["report"]["pass"]:
            break
    rec.pop("g5")
    rec["candidates_sha256"] = "f" * 64
    inp["blocks"][fam] = (rows, rels, rec)
    (sel.OUT / f"select_{fam}.json").write_text(json.dumps(rec))
    m.TARGETS[fam] = rec["target"]
    return rec


def test_flow_dry_run_with_the_new_blocks_then_wave_2_is_trimmed_first(flow, monkeypatch):
    args, writes, inp = flow

    def gb_tweak(r):
        r["meta"]["domain"] = "dom" + r["meta"]["card_id"][1:]
        r["meta"]["card_id"] = ("y" if r["qtype"] == "noul" else "c") + r["meta"]["card_id"]     # one form per card
        if r["role"] == "complement":
            r["meta"]["twin_of"] = r["id"][:-1] + "a"
    add_block(inp, "T44", 320, 5, "D", 150, monkeypatch)
    add_block(inp, "GB", 420, 6, "G", 300, monkeypatch, gb_tweak)
    rep = m.build(args(spend_to_date=1.5))
    by = rep["selection_digest"]["rows_by_block"]
    new = sum(n for b, n in by.items() if b != "replay")
    assert by["T44"] > 0 and by["GB"] > 0 and by["replay"] == math.floor(1.5 * new)
    assert rep["t_max_usd"] == 30.5 == rep["t_core_usd"] and rep["spend_to_date_usd"] == 1.5 and "T44" in rep["caps"]
    assert rep["a42d_blocks"]["GB"]["twins"] >= 0 and rep["a42d_blocks"]["GB"]["max_domain_share"] <= 0.2
    a = by["T28"] + by["T44"]
    assert 9 * a <= 11 * (new - a)                                           # the agent tier incl. T44 is inside 55%
    assert any("GB:" in p and "yes share outside" in p for p in rep["problems"])    # the per-card band is asserted
    assert not any("agent tier" in p or "above their planned" in p for p in rep["problems"]), rep["problems"]
    first = dict(by)
    n_rows = sum(first.values())

    def fake_proj(rows, rels, ntok, seed=m.SEED):
        return {"total_usd": round(len(rows) * 0.01, 4), "train_usd": round(len(rows) * 0.01, 4), "rows": len(rows)}
    monkeypatch.setattr(m, "project_cost", fake_proj)
    monkeypatch.setattr(m, "OVERHEAD_USD", 0.0)
    monkeypatch.setattr(m, "FLOOR_ROWS", 100)
    spend = 32.0 - (n_rows * 0.01 - 0.5)                                     # T_max is $0.50 below the projection
    rep2 = m.build(args(spend_to_date=spend))
    b2 = rep2["selection_digest"]["rows_by_block"]
    assert b2["T44"] < first["T44"] and b2["T28"] == first["T28"] and b2["T01"] == first["T01"] and b2["GB"] == first["GB"]
    steps = [s["step"] for rd in rep2["budget"]["rounds"] if "trim" in rd for s in rd["trim"]["steps"]]
    assert steps[:2] == ["item10", "wave2"] and "proportional" not in steps
    assert b2["replay"] == math.floor(1.5 * (sum(b2.values()) - b2["replay"]))
    assert rep2["budget"]["final_total_usd"] <= round(spend and 32.0 - spend, 4) + 1e-9


def test_dom_of_merges_openalex_and_ror_into_one_scholarly_domain():
    """16 Oct ruling (A42-D 8.2): the mixer's 20% domain cap sees OpenAlex + ROR as one domain."""
    import mix_c2
    a = {"meta": {"domain": "scholarly_publishing"}}
    b = {"meta": {"domain": "research_organisations"}}
    assert mix_c2.dom_of(a) == mix_c2.dom_of(b) == "scholarly"
    assert mix_c2.dom_of({"meta": {"domain": "music"}}) == "music"
    assert mix_c2.dom_of({"domain": "news", "meta": {}}) == "news"
    rows = [dict(a)] * 12 + [dict(b)] * 12 + [{"meta": {"domain": f"d{i}"}} for i in range(76)]
    from collections import Counter
    assert Counter(mix_c2.dom_of(r) for r in rows)["scholarly"] == 24


def _tasks_per_source(rows):
    out = {}
    for r in rows:
        out.setdefault(r["source"], set()).add(r["meta"]["task_id"])
    return {s: len(v) for s, v in out.items()}


def _dev(src, kept, dropped=5, ruling="A51 (c)"):
    return {"ruling": ruling, "block_source": src, "tasks_in": kept + dropped, "tasks_dropped_by_gate": dropped, "tasks_kept": kept}


def test_block_rules_accepts_only_a_recorded_a51c_task_shortfall(monkeypatch, tmp_path):
    rows = meta_rows()
    tps = _tasks_per_source(rows)
    assert all(v < 40 for v in tps.values())
    floor = lambda p: any("tasks per source" in x for x in p)
    # recorded and matching for every short source: accepted (and reported)
    devs = [_dev(s, v) for s, v in tps.items()]
    rep, p = m.block_rules("MD", rows, loaded=True, deviations=devs)
    assert not floor(p) and rep["task_floor_accepted_A51c"] == dict(sorted(tps.items()))
    # no record: flagged
    assert floor(m.block_rules("MD", rows, loaded=True, deviations=[])[1])
    # one short source unrecorded: flagged
    assert floor(m.block_rules("MD", rows, loaded=True, deviations=devs[1:])[1])
    # wrong ruling, wrong source, or counts that do not match the rows: flagged
    assert floor(m.block_rules("MD", rows, loaded=True, deviations=[_dev(s, v, ruling="A51 (a)") for s, v in tps.items()])[1])
    assert floor(m.block_rules("MD", rows, loaded=True, deviations=[_dev("other", v) for s, v in tps.items()])[1])
    assert floor(m.block_rules("MD", rows, loaded=True, deviations=[_dev(s, v + 1) for s, v in tps.items()])[1])
    bad = [dict(d, tasks_in=d["tasks_in"] + 1) for d in devs]               # in - dropped != kept
    assert floor(m.block_rules("MD", rows, loaded=True, deviations=bad)[1])
    # a source above 80 tasks is never accepted
    many = [r | {"meta": r["meta"] | {"task_id": f"{r['meta']['task_id']}_{i % 14}"}} for i, r in enumerate(rows)]
    assert floor(m.block_rules("MD", many, loaded=True, deviations=[_dev(s, v) for s, v in _tasks_per_source(many).items()])[1])
    # loaded=True without the argument reads <C2_PARTS>/MD/qc/QC_REPORT.json
    qc = tmp_path / "MD" / "qc"
    qc.mkdir(parents=True)
    monkeypatch.setattr(m, "C2_PARTS", tmp_path)
    assert floor(m.block_rules("MD", rows, loaded=True)[1])                  # no file yet
    (qc / "QC_REPORT.json").write_text(json.dumps({"deviations": devs}))
    assert not floor(m.block_rules("MD", rows, loaded=True)[1])
    (qc / "QC_REPORT.json").write_text(json.dumps({"deviations": [devs[0]]}))
    assert floor(m.block_rules("MD", rows, loaded=True)[1])

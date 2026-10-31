"""Tests for c2_build/a69_faithful.py as wired by Ruling A80 (b): the D1 fix (token mean), L1 / L2 (the (f)(i) and (f)(ii) admission), L3 (A34 e read
literally), stage2 (the guarded swap + the faithful repair that c2_select calls) and the tool shas. Synthetic families, in memory only; nothing is
written. The 42 older tests of the module are in test_repair_a69_faithful_a78.py. Run from lean/:
  HF_HUB_OFFLINE=1 ../.venv/bin/python -B -m pytest -q c2_build/tests/test_a69_faithful_a80.py
"""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2B = HERE.parent
sys.path.insert(0, str(C2B))
sys.path.insert(0, str(HERE))
import a49c  # noqa: E402
import a69_faithful as RF  # noqa: E402
import c2_select as sel  # noqa: E402
import crowd_select as cs  # noqa: E402
import mix_c2  # noqa: E402
from test_c2_select_a69 import FAM as T26, pool, toks  # noqa: E402
from test_repair_a69_faithful_a78 import F4, CHK_SHORT, FakePlugin, choice_family, make, rec_of, run  # noqa: E402


# ------------------------------------------------------------------------------------------------ D1: the combined token_mean entry
def mean_window_family(extra: int = 6):
    """200 single-row units of 800 tokens, `extra` of them (plain rows 40..) 801: the exact mean is 800.03 for extra = 6. (Rows 0..33 are twin / equiv rows:
    dropping one would break a passing twin or equiv share, so the repair could not fix the mean with them.)"""
    return choice_family(200, tok=lambda i: 801 if 40 <= i < 40 + extra else 800)


def test_d1_window_mean_passes_cap_checks_but_fails_family_checks():
    rows, rels, ntok = mean_window_family()
    fm, units = make(rows, rels, ntok)
    S = frozenset(range(200))
    R = fm.rows_of(S)
    mean = sum(ntok[r["id"]] for r in R) / len(R)
    assert 800.0 < mean <= 800.05                                           # exact 800.03: the window the skeptic found
    _, probs = mix_c2.cap_checks(R, ntok, True)
    assert not any("tokens per row >" in p for p in probs)                  # cap_checks rounds to 1 decimal (800.0): pass
    assert a49c.family_checks(fm.fam, R, [], ntok, plugin=FakePlugin())["token_mean"]["verdict"] == "fail"      # family_checks uses the exact mean: fail


def test_d1_every_group_call_is_consistent_and_never_aborts():
    rows, rels, ntok = mean_window_family()
    fm, units = make(rows, rels, ntok)
    S = frozenset(range(200))
    for names in (["rows_per_card"], ["difficulty_caps"], ["freeform_share"], ["token_mean"], ["yes_rate"], ["rows_per_card", "token_mean"]):
        out = fm.some(S, names)                                              # before the fix: SystemExit for the cap-only calls
        assert set(out) == set(names)
    tm = fm.all(S)["token_mean"]
    assert tm[0] == "fail" and 0.0 < tm[1] <= 0.05                           # the stricter reading: the exact mean decides
    assert fm.some(S, ["token_mean"])["token_mean"] == tm


def test_d1_finalize_builds_the_combined_entry_only_from_both_parts():
    rows, rels, ntok = mean_window_family()
    fm, _ = make(rows, rels, ntok)
    only_cap = fm._finalize({"token_mean@cap": ("pass", 0.03)})
    assert "token_mean" not in only_cap                                      # a partial group never makes a (pass, distance > 0) entry
    only_fc = fm._finalize({"token_mean@fc": ("fail", 0.03)})
    assert "token_mean" not in only_fc
    both = fm._finalize({"token_mean@fc": ("fail", 0.03), "token_mean@cap": ("pass", 0.03)})
    assert both["token_mean"] == ("fail", 0.03)
    clean = fm._finalize({"token_mean@fc": ("pass", 0.0), "token_mean@cap": ("pass", 0.0)})
    assert clean["token_mean"] == ("pass", 0.0)
    na = fm._finalize({"token_mean@fc": ("n/a", 0.0), "token_mean@cap": ("pass", 0.0)})
    assert na["token_mean"] == ("pass", 0.0)                                 # n/a counts as pass
    capfail = fm._finalize({"token_mean@fc": ("fail", 5.0), "token_mean@cap": ("fail", 5.0)})
    assert capfail["token_mean"] == ("fail", 5.0)


def test_d1_the_repair_runs_through_the_window_without_aborting_and_fixes_it():
    rows, rels, ntok = mean_window_family()
    fm, units = make(rows, rels, ntok)
    S0, sel_, rec = run(fm)
    assert "token_mean" in rec["failing_before"]
    assert rec["checks_final"]["token_mean"]["verdict"] == "pass" and rec["rows_dropped"] <= 6
    assert all(m["check"] == "token_mean" for m in rec["moves"])


def test_d1_empty_selection_has_a_token_part_and_does_not_abort():
    rows, rels, ntok = choice_family(40)
    fm, units = make(rows, rels, ntok)
    out = fm.all(frozenset())                                                # no rows: the fc part is n/a, still a combined entry
    assert out["token_mean"][0] != "fail"


# ------------------------------------------------------------------------------------------------ L1: (f)(ii) arithmetic and the repair block
def test_l1_arithmetic_is_checked_when_nothing_was_dropped():
    ok, why = RF.short_record_decision(F4 | {"total_eq_target": True}, 1000, {"rows_pre_repair": 1000, "rows_dropped": 0}, 1000)
    assert ok and not why
    ok, why = RF.short_record_decision(F4 | {"total_eq_target": True}, 990, {"rows_pre_repair": 1000, "rows_dropped": 0}, 1000)
    assert not ok and any("!= rows selected" in w for w in why)              # rows_dropped == 0 and 1000 - 0 != 990
    ok, why = RF.short_record_decision(F4 | {"total_eq_target": False}, 900, {"rows_pre_repair": 900, "rows_dropped": 0}, 1000, 3, False, True)
    assert ok and not why                                                    # short before the repair, A34 (e) literal
    ok, why = RF.short_record_decision(F4 | {"total_eq_target": False}, 900, {"rows_pre_repair": 910, "rows_dropped": 0}, 1000, 3, False, True)
    assert not ok


@pytest.mark.parametrize("repair", [None, {}, {"rows_dropped": 3}, {"rows_pre_repair": 100}, "not run (repair=False)"])
def test_l1_no_repair_block_is_refused_whatever_else_passes(repair):
    ok, why = RF.short_record_decision(F4 | {"total_eq_target": True}, 1000, repair if isinstance(repair, dict) else None, 1000)
    assert not ok and any("no repair block" in w for w in why)
    s = rec_of(1000, 1000, 1000, 0, checks={k: True for k in CHK_SHORT})
    s["report"]["pass"] = True
    s["a69"] = {"repair": repair}
    assert "no repair block" in RF.selection_problem_faithful(s, "x", 1000)


# ------------------------------------------------------------------------------------------------ L2: the four entries and (f)(i)
def test_l2_the_four_entries_are_named_as_the_adopted_text_and_required():
    assert RF.F_CHECKS == ("a49c_and_caps_pass", "chi2_p_gt_0.01_pg_bins", "easy_le_25_pg_bins", "trap_type_cap_le_35")
    for k in RF.F_CHECKS:
        ok, why = RF.short_record_decision({c: v for c, v in (F4 | {"total_eq_target": True}).items() if c != k}, 1000,
                                           {"rows_pre_repair": 1000, "rows_dropped": 0}, 1000)
        assert not ok and any(k in w for w in why)
    for k in RF.F_CHECKS:                                                    # any of the four False refuses the record
        ok, why = RF.short_record_decision(F4 | {k: False, "total_eq_target": True}, 1000, {"rows_pre_repair": 1000, "rows_dropped": 0}, 1000)
        assert not ok and any("ONLY failed check" in w for w in why)


PIN = {"c2_select.py": "a" * 64, "a49c.py": "b" * 64, "a69_faithful.py": "c" * 64}


def valid_record():
    s = rec_of(1000, 1000, 1000, 0, checks={k: True for k in CHK_SHORT})
    s["report"]["pass"] = True
    s |= {"a42d6": {"rule": "x"}, "pg_bin": {"r1": "easy"}, "scratch": False, "tool_sha256": dict(PIN)}
    s["a69"] = s["a69"] | {"version": 1}
    return s


def test_l2_f_i_accepts_a_complete_record_and_refuses_each_gap():
    s = valid_record()
    assert RF.program_record_problem(s, PIN) is None
    assert RF.program_selection_problem(s, "x", 1000, PIN) is None
    for k in ("a42d6", "a69", "pg_bin"):
        bad = {a: b for a, b in s.items() if a != k}
        assert RF.program_record_problem(bad, PIN) and k in RF.program_record_problem(bad, PIN)
    assert "a69" in RF.program_record_problem(s | {"a69": "not a dict"}, PIN)
    assert "pg_bin" in RF.program_record_problem(s | {"pg_bin": {}}, PIN)
    assert "scratch" in RF.program_record_problem(s | {"scratch": True}, PIN)
    assert "not pinned" in RF.program_record_problem(s, {}) and "not pinned" in RF.program_record_problem(s, None)
    assert "pinned A69_TOOL_SHAS" in RF.program_record_problem(s | {"tool_sha256": dict(PIN, **{"a49c.py": "d" * 64})}, PIN)
    assert "pinned A69_TOOL_SHAS" in RF.program_record_problem(s | {"tool_sha256": {k: v for k, v in PIN.items() if k != "a49c.py"}}, PIN)
    assert "pinned A69_TOOL_SHAS" in RF.program_record_problem(s | {"tool_sha256": dict(PIN, extra="e" * 64)}, PIN)       # tool shas other than the pinned set
    assert "pinned A69_TOOL_SHAS" in RF.program_record_problem({k: v for k, v in s.items() if k != "tool_sha256"}, PIN)
    assert RF.program_record_problem(None, PIN) and RF.program_record_problem("x", PIN)


def test_l2_the_plain_refusals_come_first_and_f_ii_comes_after_f_i():
    s = valid_record()
    assert "G9 not run" in RF.program_selection_problem(None, "x", 1000, PIN)
    assert "another candidates" in RF.program_selection_problem(s, "y", 1000, PIN)
    assert "target" in RF.program_selection_problem(s, "x", 900, PIN)
    assert "A69 f i" in RF.program_selection_problem(s | {"scratch": True}, "x", 1000, PIN)
    short = valid_record()
    short["selected_ids"] = list(range(800))
    short["report"]["checks"]["total_eq_target"] = False
    short["a69"]["repair"] = {"rows_pre_repair": 1000, "rows_dropped": 200}
    assert RF.program_selection_problem(short, "x", 1000, PIN) is None                       # (f)(ii): 20% dropped, total_eq_target the only failure
    short["a69"]["repair"] = {"rows_pre_repair": 1000, "rows_dropped": 260}
    assert "25%" in RF.program_selection_problem(short, "x", 1000, PIN)


# ------------------------------------------------------------------------------------------------ L3: A34 (e) read literally
def test_l3_flag_is_read_from_the_record_and_only_a_bool_counts():
    assert RF.a34e_flag({"a69": {"a34e": {"short_only_because_g13": True}}}) is True
    assert RF.a34e_flag({"a69": {"a34e": {"short_only_because_g13": False}}}) is False
    for bad in ({}, {"a69": {}}, {"a69": {"a34e": {}}}, {"a69": {"a34e": {"short_only_because_g13": "yes"}}}, {"a69": "x"}):
        assert RF.a34e_flag(bad) is None


def test_l3_short_before_the_repair_needs_the_flag_and_the_removed_units():
    chk = F4 | {"total_eq_target": False}
    rp = {"rows_pre_repair": 900, "rows_dropped": 0}
    assert RF.short_record_decision(chk, 900, rp, 1000, 5, False, True)[0] is True
    assert RF.short_record_decision(chk, 900, rp, 1000, 5, False, False)[0] is False       # the removal did not cause the shortfall
    assert RF.short_record_decision(chk, 900, rp, 1000, 5, False, None)[0] is False        # the record cannot show it
    assert RF.short_record_decision(chk, 900, rp, 1000, 0, False, True)[0] is False         # no G13-removed unit: nothing for A34 (e) to excuse
    assert RF.short_record_decision(chk, 900, rp, 1000, 0, True, None)[0] is True           # an upper-bound target is a separate reason
    ok, why = RF.short_record_decision(chk, 800, {"rows_pre_repair": 1000, "rows_dropped": 200}, 1000)
    assert ok and not why                                                                   # at target before the repair: the repair drops explain it, no A34 (e) needed


def test_l3_counterfactual_at_target_iff_the_pool_before_the_removal_reaches_it():
    rows, rels, probs, pg = pool(1000, seed=3, tag_p=0.6, k=3)
    units = cs.units_of(rows, rels)
    cf = RF.g13_counterfactual(rows, rels, pg, probs, 500, T26, sel.SEED)
    assert cf == {"pre_g13_pool_rows": 1000, "pre_g13_first_stage_rows": 500, "pre_g13_first_stage_at_target": True} and len(units) == 1000
    cf2 = RF.g13_counterfactual(rows, rels, pg, probs, 600, T26, sel.SEED)                   # the full pool is itself short of 600 (balanced bins and quotas)
    assert cf2["pre_g13_first_stage_rows"] < 600 and cf2["pre_g13_first_stage_at_target"] is False
    snap = copy.deepcopy(rows)
    RF.g13_counterfactual(rows, rels, pg, probs, 500, T26, sel.SEED)
    assert rows == snap                                                                      # reads only


# ------------------------------------------------------------------------------------------------ stage2 and the tool shas
def test_stage2_swaps_with_the_guard_then_repairs_and_is_the_run_family_path():
    rows, rels, probs, pg = pool(500, seed=3, tag_p=0.6, k=3)
    ntok = toks(rows, 700, 940)
    units = cs.units_of(rows, rels)
    res, a42 = sel.trap_select(rows, units, pg, probs, 300, T26, sel.SEED)
    treated = a42.pop("_treated")
    st = RF.stage2(T26, rows, rels, units, res, treated, a42["type_order"], a42["weight"], pg, a42["pg_bin"], ntok, 300, T26, sel.SEED)
    assert set(st) == {"family", "order", "pre_repair_sel", "sel", "swap", "repair", "additions"}
    assert set(st["sel"]) <= set(st["pre_repair_sel"]) and "guard_rejections" in st["swap"]
    assert st["repair"]["rows_pre_repair"] == sum(len(units[u]) for u in st["pre_repair_sel"])
    assert st["repair"]["rows_dropped"] == st["repair"]["rows_pre_repair"] - sum(len(units[u]) for u in st["sel"])
    assert set(st["additions"]) == set(RF.F_CHECKS) == set(st["repair"]["report_checks_additions"])
    off = RF.stage2(T26, rows, rels, units, res, treated, a42["type_order"], a42["weight"], pg, a42["pg_bin"], ntok, 300, T26, sel.SEED, repair=False)
    assert off["repair"] is None and off["sel"] == off["pre_repair_sel"] and set(off["additions"]) == set(RF.F_CHECKS)
    run = RF.run_family(T26, rows, rels, pg, probs, 300, ntok)
    assert run["selected_ids"] == [rows[i]["id"] for u in st["sel"] for i in units[u]] or set(run["selected_ids"]) == {rows[i]["id"] for u in st["sel"] for i in units[u]}


def test_stage2_requires_real_token_counts():
    rows, rels, probs, pg = pool(120, seed=3)
    units = cs.units_of(rows, rels)
    res, a42 = sel.trap_select(rows, units, pg, probs, 80, T26, sel.SEED)
    treated = a42.pop("_treated")
    with pytest.raises(SystemExit, match="real tokens"):
        RF.stage2(T26, rows, rels, units, res, treated, a42["type_order"], a42["weight"], pg, a42["pg_bin"], {rows[0]["id"]: 5}, 80, T26, sel.SEED)


def test_tool_shas_are_the_files_on_disk():
    t = RF.tool_shas()
    assert set(t) == {"c2_select.py", "a49c.py", "a69_faithful.py", "crowd_select_c2.py", "crowd_select.py", "mixer.py"}
    for name, path in RF.A69_TOOL_FILES:
        assert t[name] == hashlib.sha256(Path(path).read_bytes()).hexdigest() and len(t[name]) == 64


def test_the_module_names_no_never_open_path():
    src = (C2B / "a69_faithful.py").read_text().lower()
    for bad in ("ohs", "sealed", "external_quarantine", "longbench", ".claude", "preread", "c_spec", "jev"):
        assert bad not in src, bad

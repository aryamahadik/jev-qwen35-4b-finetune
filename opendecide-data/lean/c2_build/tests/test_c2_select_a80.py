"""Tests for c2_select as wired by Ruling A80 (b): select_family and reselect use the guarded swap (A69 c) and the faithful repair (A69 d) through
a69_faithful.stage2, write the a42d6 / a69 blocks, the four (f) report.checks entries, the (d6) move log, the literal A34 (e) flag, tool_sha256 and
scratch false. In memory only. Run from lean/:
  HF_HUB_OFFLINE=1 ../.venv/bin/python -B -m pytest -q c2_build/tests/test_c2_select_a80.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
import a49c  # noqa: E402
import a69_faithful as a69f  # noqa: E402
import c2_select as sel  # noqa: E402
import crowd_select as cs  # noqa: E402
from test_c2_select_a69 import FAM, pool, toks  # noqa: E402


def small(n=400, target=250, **kw):
    rows, rels, probs, pg = pool(n, seed=5, tag_p=0.6, k=3, **kw)
    return rows, rels, probs, pg, target


# ------------------------------------------------------------------------------------------------ the record
def test_the_record_carries_every_block_the_mixer_admits_on():
    rows, rels, probs, pg, t = small()
    rec = sel.select_family(FAM, rows, rels, pg, t, probs=probs, ntok=toks(rows, 700, 940))
    assert rec["scratch"] is False and rec["tool_sha256"] == a69f.tool_shas()
    assert set(rec["a42d6"]) >= {"rule", "weight_used", "weight_scaled", "type_cap", "type_order", "pick_rates_post_g13", "treated_selected_units"}
    assert rec["a42d6"]["rule"].startswith("A42-D 6 via A69") and rec["a42d6"]["type_cap"] == 0.35
    a = rec["a69"]
    assert a["version"] == 1 and set(a) >= {"swap", "repair", "a34e", "report_checks_additions"}
    assert "guard_rejections" in a["swap"] or a["swap"].get("note")                                     # the guarded swap (a swap that was not needed says so)
    assert set(rec["pg_bin"]) == set(rec["difficulty_bin"]) and rec["parts"][0]["trap_rank"] == rec["a42d6"]["type_order"]
    assert "a69" not in rec["report"] and "pg_bin" not in rec["a42d6"]


def test_the_four_f_entries_are_in_report_checks_and_report_pass_needs_all_of_them():
    rows, rels, probs, pg, t = small()
    rec = sel.select_family(FAM, rows, rels, pg, t, probs=probs, ntok=toks(rows))
    chk = rec["report"]["checks"]
    assert set(a69f.F_CHECKS) <= set(chk) and all(isinstance(chk[k], bool) for k in a69f.F_CHECKS)
    assert {k: chk[k] for k in a69f.F_CHECKS} == rec["a69"]["report_checks_additions"]
    assert rec["report"]["pass"] is all(chk.values())
    assert chk["a49c_and_caps_pass"] is False and rec["report"]["pass"] is False                       # this pool has no twin rows: twin_share (20-25%) cannot hold
    assert "twin_share" in rec["a69"]["repair"]["failing_after"]


def test_the_repair_log_has_the_d6_fields_and_the_arithmetic_the_mixer_checks():
    rows, rels, probs, pg, t = small()
    rec = sel.select_family(FAM, rows, rels, pg, t, probs=probs, ntok=toks(rows, 700, 940))
    rp = rec["a69"]["repair"]
    assert rp["moves"] and rp["rows_dropped"] > 0 and rp["rows_pre_repair"] - rp["rows_dropped"] == len(rec["selected_ids"])
    m = rp["moves"][0]
    assert set(m) >= {"check", "unit_first_id", "unit_rows", "rows_by_bin6", "treated", "ptype", "companions", "distance_before", "distance_after",
                      "changed_distances"} and m["distance_after"] < m["distance_before"]
    assert rp["rows_dropped"] <= rp["loss_max_rows"] == rp["rows_pre_repair"] // 4
    assert a69f.repair_numbers(rec) == {"rows_pre_repair": rp["rows_pre_repair"], "rows_dropped": rp["rows_dropped"]}
    assert rec["report"]["rows"] == len(rec["selected_ids"])                                            # the report is on the final rows


def test_repair_false_leaves_no_repair_block_but_still_swaps_with_the_guard_and_reports_the_four_entries():
    rows, rels, probs, pg, t = small()
    rec = sel.select_family(FAM, rows, rels, pg, t, probs=probs, repair=False, ntok=toks(rows, 700, 940))
    assert rec["a69"]["repair"].startswith("not run") and a69f.repair_numbers(rec) is None
    assert set(a69f.F_CHECKS) <= set(rec["report"]["checks"])
    s = dict(rec, candidates_sha256="x", target=t)
    assert "no repair block" in a69f.selection_problem_faithful(s, "x", t)                              # the mixer refuses it


def test_an_a69_family_needs_real_token_counts():
    rows, rels, probs, pg, t = small(300, 200)
    with pytest.raises(SystemExit, match="real tokens"):
        sel.select_family(FAM, rows, rels, pg, t, probs=probs)
    with pytest.raises(SystemExit, match="real tokens"):
        sel.select_family(FAM, rows, rels, pg, t, probs=probs, ntok={rows[0]["id"]: 5})


def test_selection_is_deterministic_to_the_byte():
    rows, rels, probs, pg, t = small(300, 200)
    a = sel.select_family(FAM, rows, rels, pg, t, probs=probs, ntok=toks(rows, 700, 940))
    b = sel.select_family(FAM, rows, rels, pg, t, probs=probs, ntok=toks(rows, 700, 940))
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


def test_the_draft_swap_and_repair_are_not_called_for_an_a69_family(monkeypatch):
    rows, rels, probs, pg, t = small(300, 200)
    boom = lambda *a, **k: (_ for _ in ()).throw(AssertionError("draft code called"))          # noqa: E731
    monkeypatch.setattr(a49c, "swap_balance", boom)
    monkeypatch.setattr(a49c, "repair_drop_only", boom)
    seen = []
    real = a69f.swap_balance_guarded

    def spy(*a, **k):
        seen.append(k)
        return real(*a, **k)
    monkeypatch.setattr(a69f, "swap_balance_guarded", spy)
    sel.select_family(FAM, rows, rels, pg, t, probs=probs, ntok=toks(rows))
    assert len(seen) == 1 and callable(seen[0]["guard"]) and "unit_class" in seen[0] and "never_in" in seen[0]


def test_a_family_without_probs_or_outside_the_15_keeps_the_old_path(monkeypatch):
    rows, rels, probs, pg, t = small(300, 200)
    called = []
    real = a49c.swap_balance
    monkeypatch.setattr(a49c, "swap_balance", lambda *a, **k: called.append(1) or real(*a, **k))
    plain = sel.select_family(FAM, rows, rels, pg, t)                                                   # no probs: the pre-A69 selection
    assert called and not ({"a42d6", "a69", "pg_bin", "tool_sha256", "scratch"} & set(plain))
    for r in rows:
        r["meta"]["family"] = "T40"
    other = sel.select_family("T40", rows, rels, pg, t, probs=probs, ntok=toks(rows))                   # T40 is not in the 15
    assert not ({"a42d6", "a69", "pg_bin", "tool_sha256", "scratch"} & set(other))


# ------------------------------------------------------------------------------------------------ A34 (e), read literally
def g13_case(target, drop_n, n=1000, seed=3):
    rows, rels, probs, pg = pool(n, seed=seed, tag_p=0.6, k=3)
    drop = {r["id"] for r in rows[:drop_n]}
    return rows, rels, probs, pg, drop, target


def test_a34e_true_only_when_the_pool_before_the_removal_reaches_the_target():
    rows, rels, probs, pg, drop, t = g13_case(500, 600)
    rec = sel.select_family(FAM, rows, rels, pg, t, drop_ids=drop, probs=probs, repair=False, ntok=toks(rows))
    e = rec["a69"]["a34e"]
    assert rec["exclude_ids"]["units_removed"] == 600 and e["short_before_repair"] is True
    assert e["pre_g13_first_stage_at_target"] is True and e["short_only_because_g13"] is True and e["pre_g13_pool_rows"] == 1000
    assert a69f.a34e_flag(rec) is True


def test_a34e_false_when_the_family_would_have_been_short_without_the_removal():
    rows, rels, probs, pg, drop, t = g13_case(600, 50)                                                  # the full pool reaches only 528 of 600
    rec = sel.select_family(FAM, rows, rels, pg, t, drop_ids=drop, probs=probs, repair=False, ntok=toks(rows))
    e = rec["a69"]["a34e"]
    assert e["g13_units_removed"] == 50 and e["short_before_repair"] is True
    assert e["pre_g13_first_stage_at_target"] is False and e["short_only_because_g13"] is False
    s = dict(rec, candidates_sha256="x", target=t)
    ok, why = a69f.short_record_decision({**rec["report"]["checks"], **{k: True for k in a69f.F_CHECKS}}, len(rec["selected_ids"]),
                                         a69f.repair_numbers(s) or {"rows_pre_repair": len(rec["selected_ids"]), "rows_dropped": 0}, t,
                                         rec["exclude_ids"]["units_removed"], False, a69f.a34e_flag(rec))
    assert not ok and any("A34 (e)" in w for w in why)                                                  # the loose reading (units were removed) would have admitted it


def test_a34e_false_without_removed_units_or_when_not_short():
    rows, rels, probs, pg = pool(1000, seed=3, tag_p=0.6, k=3)
    rec = sel.select_family(FAM, rows, rels, pg, 500, probs=probs, repair=False, ntok=toks(rows))
    e = rec["a69"]["a34e"]
    assert e["g13_units_removed"] == 0 and e["short_only_because_g13"] is False and e["note"] == "no G13-removed unit" and "pre_g13_pool_rows" not in e
    rows, rels, probs, pg, drop, t = g13_case(300, 100)                                                 # plenty left after the removal: not short before the repair
    rec = sel.select_family(FAM, rows, rels, pg, t, drop_ids=drop, probs=probs, repair=False, ntok=toks(rows))
    e = rec["a69"]["a34e"]
    assert e["short_before_repair"] is False and e["short_only_because_g13"] is False and "not short" in e["note"]


# ------------------------------------------------------------------------------------------------ reselect = the same steps
def test_reselect_runs_stage2_with_the_part_data_and_returns_the_a69_record_per_part(monkeypatch):
    rows, rels, probs, pg, t = small(500, 350)
    rec = sel.select_family(FAM, rows, rels, pg, t, probs=probs, ntok=toks(rows))
    by = {r["id"]: r for r in rows}
    chosen = [by[i] for i in rec["selected_ids"]]
    trap = rec["parts"][0]["trap"]
    for r in chosen:
        r["meta"] = dict(r["meta"]) | {"pg_bin": rec["pg_bin"][r["id"]], "difficulty_bin": rec["difficulty_bin"][r["id"]]}
    pgm = {r["id"]: rec["crowd_pg"][r["id"]] for r in chosen}
    calls = []
    real = a69f.stage2
    monkeypatch.setattr(a69f, "stage2", lambda *a, **k: calls.append((a, k)) or real(*a, **k))
    out = sel.reselect(chosen, [], pgm, [dict(rec["parts"][0])], int(len(chosen) * 0.7), ntok=toks(chosen))
    assert len(calls) == 1 and calls[0][0][0] == FAM
    a = out["a69"][0]
    assert a["version"] == 1 and set(a["report_checks_additions"]) == set(a69f.F_CHECKS) and "moves" in a["repair"]
    assert set(out["bins"]) == set(out["selected_ids"]) and all(out["bins"][i] == "hard" for i in trap if i in out["bins"] and i in out["parts"][0]["trap"])
    assert all(set(a69f.F_CHECKS) <= set(rep["checks"]) for rep in out["reports"])


# ------------------------------------------------------------------------------------------------ the CLI
def test_cmd_select_counts_tokens_for_every_program_family_even_without_the_repair(monkeypatch):
    rows, rels, probs, pg, t = small(120, 80)
    seen = {}
    monkeypatch.setattr(sel.c2io, "require_a38", lambda *a, **k: None)
    monkeypatch.setattr(sel, "available", lambda fams=None: [FAM])
    monkeypatch.setattr(sel, "family_inputs", lambda ilog, fam: (rows, rels, {"candidates_sha256": "x", "relations_sha256": None}))
    monkeypatch.setattr(sel, "load_c1_full", lambda ilog, rws, d, sd, c1=sel.C1: (pg, {"view": 1}, probs))
    monkeypatch.setattr(sel, "drop_ids_of", lambda ilog, files: set())
    monkeypatch.setattr(sel, "select_family", lambda *a, **k: seen.update(k) or {"report": {}, "target": 0})
    monkeypatch.setattr(sel, "write_select", lambda fam, rec, extra: None)
    monkeypatch.setattr(sel.c2io, "write_json", lambda *a, **k: "0")
    import mixer
    monkeypatch.setattr(mixer, "token_counts", lambda ilog, rws, chunk=2000: [700] * len(rws))
    sel.main(["select", "--fam", FAM, "--no-a69-repair"])
    assert seen["repair"] is False and seen["probs"] is probs and set(seen["ntok"]) == {r["id"] for r in rows}
    seen.clear()
    sel.main(["select", "--fam", FAM])
    assert seen["repair"] is True and set(seen["ntok"]) == {r["id"] for r in rows}

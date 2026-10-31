"""Tests for mix_c2 as changed by Ruling A80 (b), (a): A69 (f)(i) - (f)(v) for a program-family select record, and the agent-core minimum of 4 of 6 that
exists only while PREREG_FINAL.md holds the owner's Ruling A80 block. In memory only (a tmp folder for the fabricated select record). Run from lean/:
  HF_HUB_OFFLINE=1 ../.venv/bin/python -B -m pytest -q c2_build/tests/test_mix_c2_a80.py
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
import a69_faithful as a69f  # noqa: E402
import c2io  # noqa: E402
import c2_select as sel  # noqa: E402
import crowd_select as cs  # noqa: E402
import mix_c2 as m  # noqa: E402
from test_c2_select_a69 import FAM, pool, toks  # noqa: E402
from test_mix_c2 import flow  # noqa: E402,F401  (the in-memory build fixture: its T28 / T01 records are pre-A69)

A80_BLOCK = ('> **Ruling A80 (18 Oct 2026 ~03:00 UTC; OWNER words, verbatim; post-result).** After Record A78, the owner: "ok go with b". So, for C2\n'
             '> only: (a) the agent-core minimum is 4 of 6.\n')
A79_ONLY = "> **Ruling A79 (x).** ok go with b\n"


# ------------------------------------------------------------------------------------------------ the agent-core minimum
def test_core_minimum_is_four_only_with_the_owner_block_and_the_words():
    assert m.core_minimum(A80_BLOCK) == (4, True)
    assert m.core_minimum("") == (5, False)
    assert m.core_minimum(A79_ONLY) == (5, False)                                                     # the words in another ruling's block do not count
    assert m.core_minimum("> **Ruling A80 (x).** the owner said nothing useful\n") == (5, False)       # the block without the words
    assert m.core_minimum("ok go with b, loose in the file\n") == (5, False)                          # the words outside a block
    assert m.core_minimum("> **Ruling A80 (x).** the owner: \"OK  GO\n> WITH B\".\n") == (4, True)    # case and a line wrap do not matter
    assert m.core_minimum("> **Ruling A800 (x).** ok go with b\n") == (5, False)                       # \b: A800 is not A80
    assert m.core_minimum(A80_BLOCK.replace("A80", "A81")) == (5, False)
    two = A79_ONLY + "\n" + A80_BLOCK                                                                 # a blank line ends a block; the next header starts one
    assert m.core_minimum(two) == (4, True)


def test_core_minimum_reads_the_real_file_the_same_way(monkeypatch):
    text = c2io.PREREG.read_text(encoding="utf-8")
    assert m.core_minimum() == m.core_minimum(text)
    monkeypatch.setattr(c2io, "PREREG", Path("/nonexistent/PREREG_FINAL.md"))
    assert m.core_minimum() == (5, False)                                                             # no file, no A80


CORE4 = ["T28", "T29", "T30", "T26"]
PROG10 = ["T35", "T31", "T01", "T23", "T06", "T24", "T15", "T12", "T25"]          # with CORE4 (all program families) this is >= 10 program families


def test_minimum_to_train_four_of_six_under_a80_and_five_without():
    entered = CORE4 + ["T31", "T01", "T23", "T06", "T24", "T15", "T25", "T37b", "F5"]
    ok, d = m.minimum_to_train(entered, A80_BLOCK)
    assert ok and d["agent_core_n"] == 4 and d["agent_core_min"] == 4 and d["a80_applied"] is True and d["program_n"] >= 10
    assert "Ruling A80" in d["rule"]
    ok, d = m.minimum_to_train(entered, "")
    assert not ok and d["agent_core_min"] == 5 and d["a80_applied"] is False
    ok, d = m.minimum_to_train(entered, A79_ONLY)
    assert not ok


def test_the_program_family_minimum_is_unchanged_by_a80():
    entered = CORE4 + ["T31", "T01", "T23", "T06"]                                                    # 4 core + 4 more = 8 program families (T35 not in)
    ok, d = m.minimum_to_train(entered, A80_BLOCK)
    assert not ok and d["program_n"] < 10 and d["agent_core_n"] == 4
    ok, d = m.minimum_to_train(CORE4[:3] + ["T31", "T01", "T23", "T06", "T24", "T15", "T25", "T12", "T35"], A80_BLOCK)
    assert not ok and d["agent_core_n"] == 3                                                          # 3 of 6 stays a stop even with A80
    assert m.MIN_PROGRAM == 10 and m.MIN_CORE == 5 and m.MIN_CORE_A80 == 4


def test_leave_out_still_never_cuts_the_core_under_a80():
    for b in ("T28", "T33", "T29", "T37b"):
        with pytest.raises(SystemExit, match="never cut"):
            m.admit_blocks(None, [b], {})
    assert set(m.NEVER_CUT) == {"T28", "T33", "T29", "T37b"}


# ------------------------------------------------------------------------------------------------ fixtures: a program-family record
@pytest.fixture
def prog(tmp_path, monkeypatch):
    """A select record made by the A69 code (select_family), forced to pass the mixer's reading (the checks of a synthetic pool cannot all hold), with
    the mixer's file boundary faked. The tests below are about how the mixer reads a record, not about selection quality."""
    rows, rels, probs, pg = pool(400, seed=5, tag_p=0.6, k=3)
    ntok = toks(rows, 700, 700)
    rec = sel.select_family(FAM, rows, rels, pg, 250, probs=probs, ntok=ntok)
    rec.pop("g5")
    rec["candidates_sha256"] = "f" * 64
    for k in rec["report"]["checks"]:
        rec["report"]["checks"][k] = True
    rec["report"]["pass"] = True
    seldir = tmp_path / "crowd_c2"
    seldir.mkdir()
    monkeypatch.setattr(sel, "OUT", seldir)
    monkeypatch.setattr(c2io, "C2_PARTS", tmp_path / "c2_parts_empty")
    monkeypatch.setattr(sel, "family_inputs", lambda ilog, b: (rows, rels, {"candidates_sha256": "f" * 64, "relations_sha256": None}))
    monkeypatch.setitem(m.TARGETS, FAM, rec["target"])
    monkeypatch.setattr(m, "A69_TOOL_SHAS", a69f.tool_shas())

    def write(r):
        (seldir / f"select_{FAM}.json").write_text(json.dumps(r))
        return r
    write(rec)
    return {"rows": rows, "rels": rels, "rec": rec, "write": write, "dir": seldir, "ilog": c2io.C2InputLog()}


def problem(rec, **kw):
    return m.selection_problem(rec, "f" * 64, rec["target"], program=True, **kw)


# ------------------------------------------------------------------------------------------------ (f)(i) and (f)(ii) through selection_problem
def test_a_complete_program_record_is_accepted(prog):
    assert problem(prog["rec"]) is None
    assert m.selection_problem(prog["rec"], "f" * 64, prog["rec"]["target"]) is None            # (all checks True: the old, non-program rule agrees)


@pytest.mark.parametrize("key", ["a42d6", "a69", "pg_bin"])
def test_f_i_a_record_without_the_a69_blocks_is_refused(prog, key):
    rec = {k: v for k, v in prog["rec"].items() if k != key}
    assert key in problem(rec)


def test_f_i_scratch_and_tool_shas(prog, monkeypatch):
    rec = prog["rec"]
    assert "scratch" in problem(rec | {"scratch": True})
    assert "pinned A69_TOOL_SHAS" in problem(rec | {"tool_sha256": dict(rec["tool_sha256"], **{"c2_select.py": "0" * 64})})
    assert "pinned A69_TOOL_SHAS" in problem({k: v for k, v in rec.items() if k != "tool_sha256"})
    monkeypatch.setattr(m, "A69_TOOL_SHAS", {})
    assert "not pinned" in problem(rec)                                                               # an empty pin refuses every program record


def test_f_ii_arithmetic_four_entries_and_the_repair_block(prog):
    rec = prog["rec"]
    rp = rec["a69"]["repair"]
    assert rp["rows_pre_repair"] - rp["rows_dropped"] == len(rec["selected_ids"])
    bad = copy.deepcopy(rec)
    bad["a69"]["repair"]["rows_dropped"] += 1
    assert "!= rows selected" in problem(bad)                                                         # also when the repair dropped nothing
    nd = copy.deepcopy(rec)
    nd["a69"]["repair"]["rows_dropped"] = 0
    nd["a69"]["repair"]["rows_pre_repair"] = len(rec["selected_ids"]) + 1
    assert "!= rows selected" in problem(nd)
    for k in a69f.F_CHECKS:
        miss = copy.deepcopy(rec)
        del miss["report"]["checks"][k]
        assert k in problem(miss)
        off = copy.deepcopy(rec)
        off["report"]["checks"][k] = False
        assert "ONLY failed check" in problem(off)
    nb = copy.deepcopy(rec)
    nb["a69"]["repair"] = "not run (repair=False)"
    assert "no repair block" in problem(nb)


def short_of(prog, target_extra, pre_extra, dropped):
    """A copy of the record, `target_extra` rows short of its target, with the repair numbers (pre-repair = selected + pre_extra, dropped rows)."""
    rec = copy.deepcopy(prog["rec"])
    n = len(rec["selected_ids"])
    rec["target"] = n + target_extra
    rec["report"]["checks"]["total_eq_target"] = False
    rec["a69"]["repair"] |= {"rows_pre_repair": n + pre_extra, "rows_dropped": dropped}
    return rec, n + target_extra


def test_f_ii_a_record_at_target_before_the_repair_needs_no_a34e(prog):
    rec, t = short_of(prog, 20, 20, 20)                                                                  # pre-repair == target, the repair dropped 20 of 270 (7%)
    assert m.selection_problem(rec, "f" * 64, t, program=True) is None
    rec["a69"]["a34e"] = {"short_only_because_g13": False}
    rec["exclude_ids"] = {"units_removed": 0}
    assert m.selection_problem(rec, "f" * 64, t, program=True) is None
    big, t = short_of(prog, 400, 400, 400)                                                               # 400 of 650 = 61% dropped
    assert "25%" in m.selection_problem(big, "f" * 64, t, program=True)
    edge, t = short_of(prog, 50, 50, 50)                                                                 # 50 of 300 is 16.7%: fine
    assert m.selection_problem(edge, "f" * 64, t, program=True) is None


def test_f_ii_a_record_short_before_the_repair_needs_a34e_read_literally(prog):
    rec, t = short_of(prog, 30, 10, 10)                                                                  # pre-repair = target - 20: short before the repair too
    rec["a69"]["a34e"] = {"short_only_because_g13": False}
    assert "A34 (e)" in m.selection_problem(rec, "f" * 64, t, program=True)                              # no G13-removed unit, no flag
    rec["exclude_ids"] = {"units_removed": 4, "rows_removed": 8, "pool_rows_after": 100}
    assert "A34 (e)" in m.selection_problem(rec, "f" * 64, t, program=True)                              # units WERE removed, but they are not the cause: the loose reading is gone
    rec["a69"]["a34e"] = {"short_only_because_g13": True}
    assert m.selection_problem(rec, "f" * 64, t, program=True) is None                                   # removed units AND the family is short only because of them
    rec["exclude_ids"] = {"units_removed": 0}
    assert "A34 (e)" in m.selection_problem(rec, "f" * 64, t, program=True)                              # a flag without removed units is nothing
    del rec["a69"]["a34e"]
    rec["exclude_ids"] = {"units_removed": 4}
    assert "A34 (e)" in m.selection_problem(rec, "f" * 64, t, program=True)                              # a record that cannot show it
    assert m.selection_problem(rec, "f" * 64, t, program=True, at_most=True) is None                      # an upper-bound target is a separate reason


def test_the_non_program_path_is_the_old_rule(prog):
    short = {"candidates_sha256": "a" * 64, "target": 1000, "selected_ids": ["x"] * 950, "exclude_ids": {"units_removed": 3},
             "report": {"pass": False, "checks": {"total_eq_target": False, "chi2_p_gt_0.01": True}}}
    assert m.selection_problem(short, "a" * 64, 1000) is None                                          # A34 (e), loose, for a carry pool or a block
    assert m.selection_problem(short, "a" * 64, 1000, program=True) is not None                       # but not for a program family


def test_the_pin_is_the_code_on_disk():
    assert m.A69_TOOL_SHAS and m.A69_TOOL_SHAS == a69f.tool_shas(), \
        "A69_TOOL_SHAS in mix_c2.py must equal a69_faithful.tool_shas(); re-pin after any edit of a pinned tool and log the shas in A64_TOOLS.md"


# ------------------------------------------------------------------------------------------------ load_block, (f)(iii), (f)(v)
def test_load_block_sets_the_a42d6_bin_the_pg_bin_and_the_trap_on_every_row(prog):
    rep, probs = {}, []
    out, keep_rels, parents, pool_, parts = m.load_block(prog["ilog"], FAM, True, rep, probs)
    rec = prog["rec"]
    assert {r["id"] for r in out} == set(rec["selected_ids"])
    trap = rec["parts"][0]["trap"]
    assert trap
    for r in out:
        mm = r["meta"]
        assert mm["difficulty_bin"] == rec["difficulty_bin"][r["id"]] and mm["pg_bin"] == rec["pg_bin"][r["id"]]
        assert mm["trap"] == {"treated": r["id"] in trap, "type": trap.get(r["id"])}
        assert (mm["difficulty_bin"] == "hard") or r["id"] not in trap                                 # a treated row is hard on the A42-D 6 map
    assert any(r["meta"]["pg_bin"] != r["meta"]["difficulty_bin"] for r in out)                        # the two maps differ where the treatment re-binned a row
    assert rep["blocks"][FAM]["selection"] == "crowd (C1 only)" and parts[0]["trap"] == trap


def test_refill_rows_carry_pg_bin_and_trap_too(prog):
    rep, probs = {}, []
    out, _r, _p, pool_, _parts = m.load_block(prog["ilog"], FAM, True, rep, probs)
    cands = [u for lst in pool_.cands.values() for u in lst]
    assert cands
    got = pool_.rows_of(cands[0], {})
    assert got and all(r["meta"]["pg_bin"] in ("easy", "medium", "hard") and set(r["meta"]["trap"]) == {"treated", "type"} for r in got)
    assert all(r["meta"]["difficulty_bin"] in ("easy", "medium", "hard") for r in got)


def test_f_iii_a_failing_program_record_leaves_the_mix_in_a_dry_run_too(prog):
    rec = copy.deepcopy(prog["rec"])
    rec["report"]["checks"]["a49c_and_caps_pass"] = False
    prog["write"](rec)
    with pytest.raises(SystemExit, match="ONLY failed check"):
        m.load_block(prog["ilog"], FAM, True, {}, [])                                                  # --final: the family leaves (assemble catches it)
    with pytest.raises(SystemExit, match="ONLY failed check"):
        m.load_block(prog["ilog"], FAM, False, {}, [])                                                 # a dry run predicts --final: it leaves too
    (prog["dir"] / f"select_{FAM}.json").unlink()                                                      # no record at all: a dry run still plans with a provisional selection
    rep, probs = {}, []
    out, *_ = m.load_block(prog["ilog"], FAM, False, rep, probs)
    assert out and "provisional" in rep["blocks"][FAM]["selection"] and any("G9 not run" in p for p in probs)
    with pytest.raises(SystemExit, match="G9 not run"):
        m.load_block(prog["ilog"], FAM, True, {}, [])


def test_a_block_that_is_not_a_program_family_keeps_the_old_dry_run_rule(prog, monkeypatch):
    monkeypatch.setattr(sel, "TRAP_FAMS", ())                                                          # the same record, read as a non-program block
    rec = copy.deepcopy(prog["rec"])
    rec["report"]["checks"]["chi2_p_gt_0.01"] = False
    rec["report"]["pass"] = False
    prog["write"](rec)
    rep, probs = {}, []
    out, *_ = m.load_block(prog["ilog"], FAM, False, rep, probs)                                       # provisional, as before
    assert out and "provisional" in rep["blocks"][FAM]["selection"]
    assert "pg_bin" not in out[0]["meta"] and "trap" not in out[0]["meta"]


def row(b, i, pg_bin=None, bin6="medium"):
    meta = {"difficulty_bin": bin6, "c2": {}}
    if pg_bin is not None:
        meta["pg_bin"] = pg_bin
    return {"id": f"{b}{i}", "_block": b, "qtype": "choice", "gold": "a", "options": ["a", "b"], "source": "s", "meta": meta}


def pg_rows(n_easy, n=100):
    return [row("T26", i, "easy" if i < n_easy else "medium") for i in range(n)]


def test_f_v_easy_on_the_pg_bins_is_a_cap_check_line():
    rows = pg_rows(30)                                                                                   # 30% easy on the pg bins, 0% on the A42-D 6 bins
    rep, probs = m.cap_checks(rows, {r["id"]: 100 for r in rows}, True)
    assert any("T26" in p and "p_g bins" in p and "A69 f v" in p for p in probs) and rep["T26"]["easy_share_pg_bins"] == 0.3
    assert rep["T26"]["easy_share"] == 0.0                                                               # the A42-D 6 map alone would have passed
    ok = pg_rows(25)                                                                                     # exactly 25%: inside
    rep, probs = m.cap_checks(ok, {r["id"]: 100 for r in ok}, True)
    assert not any("p_g bins" in p for p in probs) and rep["T26"]["easy_share_pg_bins"] == 0.25
    none = [row("T26", i) for i in range(100)]                                                           # rows without meta.pg_bin are skipped
    rep, probs = m.cap_checks(none, {r["id"]: 100 for r in none}, True)
    assert not any("p_g bins" in p for p in probs) and "easy_share_pg_bins" not in rep["T26"]
    mixed = [row("T26", i, "easy") for i in range(26)] + [row("T26", 100 + i) for i in range(74)]        # the share is over the rows that carry a pg bin: 26 of 26
    rep, probs = m.cap_checks(mixed, {r["id"]: 100 for r in mixed}, True)
    assert any("p_g bins" in p for p in probs)
    other = [row("T01", i, "easy" if i < 12 else "medium") for i in range(40)] + pg_rows(25)            # per block: T01 30%, T26 25%
    rep, probs = m.cap_checks(other, {r["id"]: 100 for r in other}, True)
    assert any(p.startswith("T01") and "p_g bins" in p for p in probs) and not any(p.startswith("T26") and "p_g bins" in p for p in probs)


def test_f_v_the_faithful_family_sees_the_same_cap_line():
    # the repair's difficulty_caps entry reads cap_checks, so a pg-bin easy share above 25% is a failing protected check there as well
    rows = pg_rows(30)
    _, probs = m.cap_checks(rows, {r["id"]: 100 for r in rows}, True)
    assert any("difficulty easy" in p for p in probs)


# ------------------------------------------------------------------------------------------------ apply_targets keeps meta.trap in step
def test_apply_targets_updates_meta_trap_to_the_surviving_treatment(prog):
    rec = prog["rec"]
    rep, probs = {}, []
    out, rels, _p, _pool, parts = m.load_block(prog["ilog"], FAM, True, rep, probs)
    pdict = {FAM: parts}
    got, _r, info = m.apply_targets(out, rels, {FAM: int(len(out) * 0.7)}, pdict, ntok={r["id"]: 700 for r in out})
    surviving = {i for p in pdict[FAM] for i in (p.get("trap") or {})}
    assert got and len(got) < len(out) and info[FAM]["a69"][0]["version"] == 1
    for r in got:
        assert r["meta"]["pg_bin"] == rec["pg_bin"][r["id"]]                                           # the p_g bin never changes
        assert r["meta"]["trap"]["treated"] == (r["id"] in surviving)                                  # a unit that lost the treatment in the re-selection says so
        assert (r["meta"]["difficulty_bin"] == "hard") or not r["meta"]["trap"]["treated"]


# ------------------------------------------------------------------------------------------------ the whole build
def test_build_leaves_a_program_family_with_a_pre_a69_record_out_and_discloses_a80(flow, monkeypatch):
    args, writes, inp = flow
    monkeypatch.setattr(sel, "TRAP_FAMS", ("T28",))                                                    # T28's fabricated record has no a42d6 / a69 blocks
    monkeypatch.setattr(m, "A69_TOOL_SHAS", {"c2_select.py": "a" * 64})
    rep = m.build(args())
    left = rep["entry"]["left_out"]["T28"]
    assert left and "lacks" in left[0] and "A69 f i" in left[0]                                        # (f)(i), and (f)(iii): the family is left out of the dry run too
    assert "T28" not in rep["entry"]["entered"] and "T01" in rep["entry"]["entered"]
    assert any(p.startswith("T28 left out") for p in rep["problems"])
    assert rep["a80_owner_ruling"]["agent_core_min"] == m.core_minimum()[0] and rep["a80_owner_ruling"]["applied"] == m.core_minimum()[1]
    assert rep["minimum_to_train"]["agent_core_min"] == m.core_minimum()[0] and rep["minimum_to_train"]["a80_applied"] == m.core_minimum()[1]
    assert not any(k == str(m.OUT_TRAIN) for k in writes)                                              # nothing refilled it, nothing written

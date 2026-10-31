"""Share and rule tests for mix_c2.py (C2_DATA_SPEC 5.1-5.5, 3.0; A37 d/f). In memory only: no row or file is
written (A37 f). The round-1 mixer tests run unchanged against c_build/mixer.py (never edited):
  ../.venv/bin/python -m pytest -q c_build/tests/test_mixer*.py c_build/tests/test_crowd_select*.py
Run from lean/:  ../.venv/bin/python -m pytest -q c2_build/tests/test_mix_c2.py
"""
from __future__ import annotations

import math
import random
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
import crowd_select as cs  # noqa: E402
import mix_c2 as m  # noqa: E402
import mixer as mx  # noqa: E402
from c2_kit import paths as kp  # noqa: E402
from test_c2_select import crowd, fam_rows  # noqa: E402

FULL = dict(c2io.TARGETS)


# ---- spec 5.1 shares --------------------------------------------------------------------------------------------------
def test_full_build_is_40_60_and_66_5k():
    p = m.plan_shares(FULL)
    assert p["new"] == 26600 and p["replay"] == 39900 and p["total"] == 66500
    assert p["targets"] == dict(sorted(FULL.items())) and not p["agent_cap"]["applied"]
    agent = sum(n for b, n in p["targets"].items() if b in c2io.AGENT)
    assert agent == 13600 and round(agent / p["new"], 3) == 0.511                       # spec 5.1: 20.5% / 40%
    assert round(p["new"] / p["total"], 3) == 0.4 and round(p["replay"] / p["total"], 3) == 0.6


@pytest.mark.parametrize("new", [1, 2, 3, 13, 26599, 21001])
def test_replay_is_floor_1_5_x_new(new):
    p = m.plan_shares({"T01": min(new, 1600)} | ({"T28": new - 1600} if new > 1600 else {}))
    assert p["replay"] == math.floor(1.5 * p["new"]) and p["total"] == p["new"] + p["replay"]


def test_targets_never_above_spec_or_2400():
    p = m.plan_shares({b: 10 ** 6 for b in FULL})
    assert p["targets"] == dict(sorted(FULL.items())) and max(p["targets"].values()) <= m.FAMILY_MAX
    p = m.plan_shares({"T28": 1000, "T01": 5000})
    assert p["targets"] == {"T01": 1600, "T28": 1000}
    with pytest.raises(ValueError):
        m.plan_shares({"T36": 300})                     # transfer dev: never trained
    with pytest.raises(ValueError):
        m.plan_shares({"F7": 300})                      # not a C2 block


def test_agent_cap_cuts_agent_families_in_proportion_when_others_are_missing():
    real = {b: n for b, n in FULL.items() if b in c2io.AGENT} | {"T01": 1600, "T23": 800, "T37b": 2000, "F5": 1500}
    p = m.plan_shares(real)
    other = 1600 + 800 + 2000 + 1500
    a = sum(n for b, n in p["targets"].items() if b in c2io.AGENT)
    assert p["agent_cap"]["applied"] and a == (11 * other) // 9 and 9 * a <= 11 * other
    assert a / p["new"] <= 0.55 + 1e-12 and a + 1 > 0.55 * (a + 1 + other)          # the most rows the cap allows
    for b in c2io.AGENT:                                                              # each family's share kept
        assert abs(p["targets"][b] / a - FULL[b] / 13600) < 1.5 / a
    assert all(p["targets"][b] == real[b] for b in real if b not in c2io.AGENT)        # others never refilled / cut
    assert p["replay"] == math.floor(1.5 * p["new"])
    assert m.agent_cap(9) == 11 and m.agent_cap(0) == 0


def test_scale_plan_keeps_family_shares_and_caps():
    p = m.scale_plan(FULL, 0.872)
    want = math.floor(0.872 * 26600)
    assert p["new"] == want and p["replay"] == math.floor(1.5 * want)
    for b, n in FULL.items():
        assert abs(p["targets"][b] - 0.872 * n) < 1.0 + 1e-9
    assert not p["agent_cap"]["applied"]
    assert m.scale_plan(FULL, 1.0)["total"] == 66500 and m.scale_plan(FULL, 2.0)["total"] == 66500


def test_budget_factor_reproduces_the_spec_9_2_pessimistic_case():
    # spec 9.2: 66.5K rows at 3.72 s/step -> $17.3 training + $2 = $19.3; the trim brings it to <= $17 (about 58K rows)
    # (the threshold is now T_max, A42-D 2.3; the formula is unchanged: t_max=17 reproduces the spec 9.2 arithmetic)
    f = m.budget_factor({"total_usd": 19.3}, t_max=17.0)
    assert 57000 <= f * 66500 <= 58500 and m.budget_factor({"total_usd": 16.0}, t_max=17.0) == 1.0
    assert m.budget_factor({"total_usd": 19.3}, 2, t_max=17.0) < f


# ---- spec 5.3 entry and the minimum to train -------------------------------------------------------------------------
QC_OK = {"pass": True, "passed_utc": "2026-10-20T22:00:00Z", "fix_iterations": 2}


def test_admission_by_the_cutoff():
    assert m.admission("T28", QC_OK, []) == []
    # the binding cutoff is Wed 21 Oct 23:59 UTC (A39 g, A42-D 1.6), not the A37 d Tue 20 Oct
    assert m.admission("T28", QC_OK | {"passed_utc": "2026-10-21T23:59:00+00:00"}, []) == []
    assert m.admission("T28", QC_OK | {"passed_utc": "2026-10-21T00:00:01Z"}, []) == []
    late = m.admission("T28", QC_OK | {"passed_utc": "2026-10-22T00:00:01Z"}, [])
    assert len(late) == 1 and "after the data cutoff" in late[0]
    assert "cut" in m.admission("T28", QC_OK | {"fix_iterations": 3}, [])[0]
    assert m.admission("T28", QC_OK | {"pass": False}, []) == ["T28: QC pass is not true"]
    assert "passed_utc" in m.admission("T28", {"pass": True, "fix_iterations": 0}, [])[0]
    assert "passed_utc" in m.admission("T28", QC_OK | {"passed_utc": "2026-10-20T22:00:00"}, [])[0]   # no offset
    assert "fix_iterations" in m.admission("T28", QC_OK | {"fix_iterations": True}, [])[0]
    assert m.admission("T28", None, []) == ["T28: no QC_REPORT.json"]
    assert m.admission("T28", QC_OK, ["recorded sha256 of x differs"])[0].endswith("differs")
    assert m.admission("T28", QC_OK, [], "no C2 crowd selection file") == ["T28: no C2 crowd selection file"]


def test_minimum_to_train():
    core5 = ["T28", "T33", "T29", "T30", "T27"]
    no_a80 = "> **Ruling A79 (x).** nothing about the agent core\n"                          # PREREG text without a Ruling A80 block: 5 of 6 (spec 5.3, A62 c)
    ok, d = m.minimum_to_train(core5 + ["T35", "T31", "T01", "T23", "T06", "T37b", "F5"], no_a80)
    assert ok and d["agent_core_n"] == 5 and d["program_n"] == 10 and d["agent_core_min"] == 5 and d["a80_applied"] is False
    ok, d = m.minimum_to_train(core5[:4] + ["T35", "T31", "T32", "T01", "T23", "T06", "T24"], no_a80)
    assert not ok and d["agent_core_n"] == 4
    ok, d = m.minimum_to_train(core5 + ["T35", "T31", "T01", "T23", "T37b", "F5", "F6"], no_a80)
    assert not ok and d["program_n"] == 9                           # T37b and carry-overs are not program families


def test_leave_out_never_cuts_the_core():
    for b in ("T28", "T33", "T29", "T37b"):
        with pytest.raises(SystemExit, match="never cut"):
            m.admit_blocks(None, [b], {})
    with pytest.raises(SystemExit, match="not a C2 block"):
        m.admit_blocks(None, ["F7"], {})


def test_selection_problem_rules():
    s = {"candidates_sha256": "a" * 64, "target": 1000, "selected_ids": ["x"] * 1000,
         "report": {"pass": True, "checks": {"total_eq_target": True, "chi2_p_gt_0.01": True}}}
    assert m.selection_problem(s, "a" * 64, 1000) is None
    assert "another candidates" in m.selection_problem(s, "b" * 64, 1000)
    assert "target" in m.selection_problem(s, "a" * 64, 900)
    short = s | {"selected_ids": ["x"] * 950, "report": {"pass": False, "checks": {"total_eq_target": False,
                                                                                  "chi2_p_gt_0.01": True}}}
    assert "fails its checks" in m.selection_problem(short, "a" * 64, 1000)
    assert m.selection_problem(short, "a" * 64, 1000, at_most=True) is None               # F6 / F11 / F4: '<='
    assert m.selection_problem(short | {"exclude_ids": {"units_removed": 3}}, "a" * 64, 1000) is None   # A34 e
    two = short | {"exclude_ids": {"preferred": {"units_removed": 0}, "rest": {"units_removed": 2}}}
    assert m.units_removed(two["exclude_ids"]) == 2 and m.selection_problem(two, "a" * 64, 1000) is None
    chi = short | {"report": {"pass": False, "checks": {"total_eq_target": False, "chi2_p_gt_0.01": False}}}
    assert "chi2" in m.selection_problem(chi | {"exclude_ids": {"units_removed": 3}}, "a" * 64, 1000)
    assert "G9 not run" in m.selection_problem(None, "a" * 64, 1000)


# ---- OHS-4 (A37 f, A38) -----------------------------------------------------------------------------------------------
A38 = ("> **Ruling A38 (16 Oct 2026): OHS-4 frozen.**\n> - manifest sha256 `" + "e" * 64 + "`\n\nnext paragraph "
       + "f" * 64)


def test_ohs4_sha_placeholder_refuses_until_a38():
    assert m.OHS4_MANIFEST_SHA256 == "c0217e7739c570b9d22176b68e1c489623dcd5f7c551011606b6ff17e59c09c3"   # filled from A38
    assert "placeholder" in m.ohs4_problem("e" * 64, A38, pinned="")
    assert m.ohs4_problem("e" * 64, A38, pinned="e" * 64) is None
    assert "not the A38" in m.ohs4_problem("f" * 64, A38, pinned="e" * 64)
    assert "does not appear" in m.ohs4_problem("f" * 64, A38, pinned="f" * 64)   # outside the A38 block
    assert "no 'Ruling A38'" in m.ohs4_problem("e" * 64, "no freeze here", pinned="e" * 64)
    assert "not a sha256" in m.ohs4_problem("xyz", A38, pinned="e" * 64)
    assert m.a38_block(A38).count("\n") == 1 and "next paragraph" not in m.a38_block(A38)


def _files(*paths):
    out = []
    for p in paths:
        if p.is_file():
            out.append((str(p), p.stat().st_size, p.stat().st_mtime_ns))
        elif p.is_dir():
            out += [(str(f), f.stat().st_size, f.stat().st_mtime_ns) for f in sorted(p.rglob("*")) if f.is_file()]
    return out


def test_main_after_a38_needs_drops_and_writes_only_the_dry_report(tmp_path, monkeypatch):
    """A38 (13 Oct) froze OHS-4: the mixer passes the freeze guard. --final still needs the G13 drop lists, a PREREG
    without A38 still refuses, and a dry run writes only its counts report through c2io's guarded writer. Nothing
    reaches disk: an empty C2 tree in tmp_path (no block enters), writers and the progress log captured in memory."""
    before = _files(m.WORK, m.LOG, m.OUT_TRAIN, m.OUT_REL, m.OUT_MAN)
    assert kp.a38_frozen()
    with pytest.raises(SystemExit, match="decontam"):        # checked before any read or write
        m.main(["--final", "--spend-to-date", "1.5", "--ohs4-sha", "e" * 64])
    writes, logged = {}, []
    monkeypatch.setattr(c2io, "C2_PARTS", tmp_path / "c2_parts")
    monkeypatch.setattr(c2io, "write_json", lambda p, obj, prereg_text=None: writes.__setitem__(str(p), obj) or "0")
    monkeypatch.setattr(c2io, "write_jsonl", lambda p, rows, prereg_text=None: writes.__setitem__(str(p), rows) or "0")
    monkeypatch.setattr(m, "log_line", lambda path, msg: logged.append((str(path), msg)))
    m.main(["--dry-run", "--spend-to-date", "1.5"])
    assert list(writes) == [str(m.WORK / "dryrun_c2.json")]
    rep = writes[str(m.WORK / "dryrun_c2.json")]
    assert rep["mode"] == "dry-run" and rep["entry"]["entered"] == []
    assert rep["shares"] == {"new": 0, "replay": [0, 0], "total": 0}
    assert any("minimum to train not met" in p for p in rep["problems"])
    assert set(rep["entry"]["left_out"]) == set(m.TARGETS)
    assert [p for p, _ in logged] == [str(m.LOG)] and "DRY RUN" in logged[0][1]
    monkeypatch.setattr(kp, "PREREG", tmp_path / "prereg_without_a38.md")
    (tmp_path / "prereg_without_a38.md").write_text("> **Ruling A37 (13 Oct 2026)**\n", encoding="utf-8")
    writes.clear()
    with pytest.raises(kp.DataBeforeFreeze):                 # the freeze guard itself is unchanged
        m.main(["--dry-run", "--spend-to-date", "1.5"])
    assert writes == {}
    assert _files(m.WORK, m.LOG, m.OUT_TRAIN, m.OUT_REL, m.OUT_MAN) == before


# ---- spec 3.0 / 5.2 caps ----------------------------------------------------------------------------------------------
def row(i, b, qtype="noul", gold=1, bin_="medium", **meta):
    r = {"id": f"{b}{i}", "call_id": f"{b}c{i}", "_block": b, "qtype": qtype, "gold": gold,
         "options": None if qtype == "noul" else ["a", "b"], "meta": {"difficulty_bin": bin_, **meta}}
    if qtype == "choice":
        r["gold"] = "a"
    return r


def balanced(b, n, **kw):
    return [row(i, b, "noul" if i % 2 else "choice", **kw) for i in range(n)]


def test_cap_checks_pass_on_a_clean_mix():
    rows = balanced("T28", 100) + balanced("T07", 50) + [row(i, "replay") | {"_block": "replay"} for i in range(9)]
    rep, p = m.cap_checks(rows, {r["id"]: 700 for r in rows})
    assert p == [] and rep["T28"]["rows"] == 100 and rep["_new_yes_no_share"] == 0.5


def test_cap_checks_flag_every_cap():
    rows = balanced("T28", 100) + balanced("T07", 100)
    tok = {r["id"]: 600 for r in rows}
    tok["T280"] = 2001                                              # one row over 2,000 tokens
    for r in rows[100:150]:
        tok[r["id"]] = 1100                                         # T07 mean 850 > 800
    for r in rows[:30]:
        r["meta"]["c2"] = {"author_mode": "F"}                      # T28 free-form 30% > 25%
    for r in rows[100:140]:
        r["meta"]["c2"] = {"author_mode": "F"}                      # T07 free-form 40%: allowed (<= 40%)
    for r in rows[:26]:
        r["meta"]["difficulty_bin"] = "easy"                        # 26% easy > 25%
    rows[60]["meta"]["option_level"] = {"a": 0, "b": 1}
    rows[61]["meta"]["teacher"] = {"yes": 0.7}
    rows[62]["meta"]["dev_only"] = True
    rep, p = m.cap_checks(rows, tok)
    text = " | ".join(p)
    for frag in ("over 2000 tokens", "T07: mean 850.0", "T28: free-form rows 0.300", "difficulty easy 0.26",
                 "new ordinal rows", "soft target", "dev_only"):
        assert frag in text, frag
    assert "T07: free-form" not in text
    yes_heavy = [row(i, "T01") for i in range(10)]
    assert any("yes/no rows 1.000" in x for x in m.cap_checks(yes_heavy, {r["id"]: 10 for r in yes_heavy})[1])
    na = [row(i, "T01", bin_=None) for i in range(4)]
    assert any("without a crowd difficulty bin" in x for x in m.cap_checks(na, {r["id"]: 10 for r in na})[1])
    assert not any("crowd difficulty" in x for x in m.cap_checks(na, {r["id"]: 10 for r in na}, final=False)[1])


def test_share_checks():
    plan = m.plan_shares({"T28": 2400, "T01": 1600, "T37b": 2000})
    by = Counter({"T28": 2400, "T01": 1600, "T37b": 2000, "replay": 9000})
    rep, p = m.share_checks(by, plan)
    assert p == [] and rep["new"] == 6000 and rep["replay"] == [9000, 9000] and rep["new_share"] == 0.4
    by2 = Counter({"T28": 2400, "T01": 1500, "T37b": 2000, "replay": 9000})          # T01 short after drops
    rep, p = m.share_checks(by2, plan)
    assert rep["short_after_drops"] == {"T01": [1500, 1600]} and any("floor(1.5 x 5,900 new) = 8,850" in x for x in p)
    rep, p = m.share_checks(Counter({"T28": 2401, "T01": 1600, "T37b": 2000, "replay": 9001}), plan)
    assert any("above their planned rows" in x for x in p) and any("families above 2,400" in x for x in p)
    rep, p = m.share_checks(Counter({"T28": 2400, "T33": 2400, "T01": 900, "replay": 8550}),
                            m.plan_shares({"T28": 2400, "T33": 2400, "T01": 900}) | {"targets": {"T28": 2400,
                                                                                               "T33": 2400, "T01": 900}})
    assert any("agent tier" in x for x in p)


def test_round1_mixer_state_is_untouched():
    assert mx.SEED == 20261003 and mx.SHARES_R1 == {"replay": 90000, "own": 45250, "public": 8750, "commit": 6000}
    assert mx.TOTAL_R1 == 150000 and str(mx.WORK).endswith("c_build/mix_r1") and cs.SEED == 20261003
    assert m.SEED == 20261013 and m.WORK != mx.WORK and m.OUT_TRAIN.name == "c2_train.jsonl"


# ---- re-selection: agent cap / budget trim (whole units, balance kept) ------------------------------------------------
def block(fam, n_units, seed, prefix):
    rows, rels = fam_rows(fam, n_units=n_units, seed=seed, prefix=prefix)
    pg = crowd(rows, seed=seed)
    rec = sel.select_family(fam, rows, rels, pg, int(len(rows) * 0.6))
    ids = set(rec["selected_ids"])
    out = [r | {"_block": fam, "meta": r["meta"] | {"crowd_pg": pg[r["id"]],
                                                     "difficulty_bin": cs.bin_of(pg[r["id"]])}}
           for r in rows if r["id"] in ids]
    return out, [x for x in rels if x["a"] in ids and x["b"] in ids], rec["parts"]


def test_apply_targets_reselects_whole_units_and_keeps_balance():
    r1, l1, p1 = block("T28", 700, 1, "A")
    r2, l2, p2 = block("T01", 500, 2, "B")
    rows, rels = r1 + r2, l1 + l2
    t = {"T28": len(r1) // 2, "T01": len(r2)}
    out, orels, info = m.apply_targets(rows, rels, t, {"T28": p1, "T01": p2})
    by = Counter(r["_block"] for r in out)
    assert by["T01"] == len(r2) and t["T28"] - 20 <= by["T28"] <= t["T28"] and set(info) == {"T28"}
    keep = {r["id"] for r in out}
    for x in l1:
        assert (x["a"] in keep) == (x["b"] in keep)
    assert all(x["a"] in keep and x["b"] in keep for x in orels)
    yn = [r["gold"] for r in out if r["_block"] == "T28" and r["qtype"] == "noul"]
    assert abs(sum(yn) / len(yn) - 0.5) <= 0.03
    bins = Counter(r["meta"]["difficulty_bin"] for r in out if r["_block"] == "T28")
    assert bins["easy"] <= 0.25 * by["T28"] + 1e-9 and bins["hard"] <= 0.30 * by["T28"] + 1e-9


def test_parts_and_pool_follow_the_selection_keys():
    rows, rels = fam_rows("F11", n_units=120, seed=5)
    for r in rows[:60]:
        r["meta"]["text_source"] = {"dataset": "mams"}
    pk = {m.part_key("F11", [r]) for r in rows}
    assert pk == {"F11|c2carry|pref", "F11|c2carry|rest"} and m.part_key("T28", rows[:1]) == "T28"
    parts = [{"key": "F11|c2carry|pref", "ids": [rows[0]["id"]]}]
    cur = m.current_parts("F11", rows[:2] + rows[-1:], [], parts)
    keys = {p["key"]: p["ids"] for p in cur}
    assert keys["F11|c2carry|pref"] == [rows[0]["id"], rows[1]["id"]] and keys["F11|c2carry|rest"] == [rows[-1]["id"]]
    pg = {r["id"]: 0.999 for r in rows}                             # every unit all-easy
    bins = {i: "easy" for i in pg}
    units = cs.units_of(rows, rels)
    pool = m.own_pool("F11", rows, rels, units, set(), bins, pg)
    offered = set(pool.cands[""])
    for u, x in enumerate(units):
        thinned = cs.easy_thinned(rows, [x], bins, m.part_key("F11", [rows[i] for i in x]), m.SEED)
        assert (u in offered) == (not thinned)                      # the selection's own key and seed decide
    assert 0 < len(offered) < len(units)


# ---- the budget projection (spec 5.5) ---------------------------------------------------------------------------------
def proj_rows(n=320, seed=0):
    rnd = random.Random(seed)
    rows = []
    for i in range(n):
        if i % 2:
            rows.append({"id": f"p{i}", "call_id": f"c{i // 2}", "qtype": "noul", "gold": i % 4 // 2, "options": None,
                         "role": "base", "source": "c2_t28", "state": "s" * rnd.randrange(100, 3000),
                         "instructions": "Is it so?", "meta": {}, "_block": "T28"})
        else:
            rows.append({"id": f"p{i}", "call_id": f"c{i // 2}", "qtype": "choice", "gold": "a",
                         "options": ["a", "b", "c"], "role": "base", "source": "replay_x", "state": "t" * 400,
                         "instructions": "Which?", "meta": {}, "_block": "replay"})
    return rows


def test_project_cost_formula_and_determinism():
    rows = proj_rows()
    rnd = random.Random(1)
    ntok = {r["id"]: rnd.randrange(150, 1900) for r in rows}
    state = random.getstate()
    p = m.project_cost(rows, [], ntok)
    assert random.getstate() == state                                   # the global stream is left as it was
    assert p == m.project_cost(rows, [], ntok)
    fill = m.config_fill(rows, [])
    assert p["steps"] == math.ceil(len(rows) / 16 * fill["epochs"]) and fill["seed"] == 20261013
    assert p["padded_tokens_per_step"] >= p["real_tokens_per_step"] > 0
    sec = p["padded_tokens_per_step"] * p["steps"] * 0.163 / 1000
    assert abs(p["train_usd"] - sec / 3600 * 4.09) < 0.02 and abs(p["total_usd"] - p["train_usd"] - 2.0) < 0.011
    assert abs(p["s_per_step"] - p["padded_tokens_per_step"] * 0.163 / 1000) < 0.002
    big = m.project_cost(rows, [], {k: 2 * v for k, v in ntok.items()})
    assert 1.6 < big["train_usd"] / p["train_usd"] < 2.4                 # time follows padded tokens


def test_project_cost_pads_each_micro_batch_to_its_longest_row():
    import decoder_io as dio
    rows = proj_rows(64)
    ntok = {r["id"]: 1 for r in rows}                                   # every sequence pads to one PAD_MULTIPLE
    p = m.project_cost(rows, [], ntok)
    seqs = p["padded_tokens_per_step"] / dio.PAD_MULTIPLE
    assert abs(seqs - (p["rows_per_step"] + p["twins_per_step"])) < 1e-6


def test_dev_items_lists_missing_frozen_sets(tmp_path):
    missing = {"c2_mixdev": tmp_path / "none_a.jsonl", "c2_transfer_dev": tmp_path / "none_b.jsonl"}
    out, miss = m.dev_items(c2io.C2InputLog(), [], missing)
    assert dict(out) == {} and len(miss) == 2 and all("spec 7.1" in x for x in miss)
    assert list(tmp_path.iterdir()) == []


# ---- the whole flow in memory (build -> finish -> gates) with the file IO faked -----------------------------------------
def replay_rows(n=1800, seed=11):
    rnd = random.Random(seed)
    rows, rels = [], []
    for i in range(n):
        src = f"gd_src{i % 3}"
        base = {"call_id": f"rc{i}", "group_id": f"rg{i}", "source": src, "role": "base", "state": f"replay text {i}",
                "card": None, "meta": {"licence": "CC0"}}
        if i % 2:
            rows.append(base | {"id": f"rp{i}", "qtype": "noul", "gold": rnd.randrange(2), "options": None,
                                "instructions": f"Is claim {i % 7} true?"})
        else:
            rows.append(base | {"id": f"rp{i}", "qtype": "choice", "gold": "x", "options": ["x", "y", "z"],
                                "instructions": "Which one?"})
    return rows, rels


@pytest.fixture
def flow(tmp_path, monkeypatch):
    """Fakes for every disk / process boundary of build(); returns (args factory, captured writes, inputs)."""
    rs = mx.rs_mod()
    blocks = {}
    # These fabricated records are pre-A69 (no trap weighting, no a42d6 / a69 blocks): the flow tests are about the mixer, so no family is a "program family"
    # here. The A69 (f) admission of a program-family record has its own tests (test_mix_c2_a80.py).
    monkeypatch.setattr(sel, "TRAP_FAMS", ())
    for fam, n, seed, pre in (("T28", 900, 1, "A"), ("T01", 700, 2, "B")):
        rows, rels = fam_rows(fam, n_units=n, seed=seed, prefix=pre)
        for r in rows:
            r["meta"]["licence"] = c2io.kp.LEAN.name and "CC0 1.0 (program-generated; Claude/Haiku-authored wording)"
        pg = crowd(rows, seed=seed)
        target = 320 if fam == "T28" else 260
        for t in range(target, target - 40, -1):                 # the largest target the balanced selection meets
            rec = sel.select_family(fam, rows, rels, pg, t)
            if rec["report"]["pass"]:
                break
        rec.pop("g5")
        rec["candidates_sha256"] = "f" * 64
        blocks[fam] = (rows, rels, rec)
    targets = {f: b[2]["target"] for f, b in blocks.items()} | {k: v for k, v in c2io.TARGETS.items() if k not in blocks}
    monkeypatch.setattr(m, "TARGETS", targets)
    # fixture isolation: load_block reads c2io.fam_files(b)["manifest"]; once real blocks exist under lean/data/c2_parts the
    # fabricated T28 / T01 would pick up the real MANIFEST (parents declared) instead of "no manifest".
    monkeypatch.setattr(c2io, "C2_PARTS", tmp_path / "c2_parts_empty")
    seldir = tmp_path / "crowd_c2"
    seldir.mkdir()
    for fam, (_, _, rec) in blocks.items():                       # selection records (ids and p_g only; no row text)
        (seldir / f"select_{fam}.json").write_text(__import__("json").dumps(rec))
    monkeypatch.setattr(sel, "OUT", seldir)
    monkeypatch.setattr(sel, "family_inputs", lambda ilog, b: (blocks[b][0], blocks[b][1],
                                                               {"candidates_sha256": "f" * 64,
                                                                "relations_sha256": None}))

    def admit(ilog, leave_out, rep):
        rep["entry"] = {"entered": sorted(blocks), "left_out": {}, "cutoff_utc": m.CUTOFF_UTC}
        return sorted(blocks)
    monkeypatch.setattr(m, "admit_blocks", admit)
    rrows, rrels = replay_rows()
    lt = [mx.light(r, rs) for r in rrows]
    units = rs.build_units(lt, rrels)
    flags = {r["id"]: {"drop_pg": False, "anchor": None} for r in rrows}
    probs = {r["id"]: ({"yes": 0.5, "no": 0.5} if r["qtype"] == "noul" else {"x": 0.4, "y": 0.3, "z": 0.3})
             for r in rrows}
    monkeypatch.setattr(m, "load_replay", lambda ilog, rep: (rrows, lt, units, list(range(len(units))), rrels, flags,
                                                               probs))
    monkeypatch.setattr(m, "old_slice_clash", lambda ilog, rows, units, kept: (kept, {"old_slice_rows": 0}))
    wq = tmp_path / "replay_write.json"
    wq.write_text(__import__("json").dumps({"quota_by_source": {f"gd_src{i}": {"q1": 600} for i in range(3)}}))
    monkeypatch.setitem(m.REPLAY, "write", wq)
    monkeypatch.setattr(m, "replay_denylist_check", lambda ilog, rows, rep: [])
    monkeypatch.setattr(m, "run_denylist", lambda ilog, q, rep, final=False: set())
    drop_one = blocks["T28"][2]["selected_ids"][0]
    pd = tmp_path / "pool_drops.json"
    pd.write_text(__import__("json").dumps({"drop_ids": [drop_one]}))
    monkeypatch.setattr(m, "POOL_DROPS_R1", pd)
    monkeypatch.setattr(m, "DEV_SETS", {"c2_mixdev": tmp_path / "absent.jsonl"})
    monkeypatch.setattr(mx, "token_counts", lambda ilog, rows, chunk=2000: [200 + len(str(r.get("state"))) % 50
                                                                           for r in rows])
    writes = {}
    monkeypatch.setattr(c2io, "require_a38", lambda prereg_text=None: None)
    monkeypatch.setattr(c2io, "write_json", lambda p, obj, prereg_text=None: writes.__setitem__(str(p), obj) or "0")
    monkeypatch.setattr(c2io, "write_jsonl", lambda p, rows, prereg_text=None: writes.__setitem__(str(p), rows) or "0")
    monkeypatch.setattr(m, "log_line", lambda *a, **k: None)

    def args(**kw):
        return type("A", (), {"final": False, "ohs4_sha": None, "decontam_drops": [], "leave_out": [],
                                  "spend_to_date": 0.0} | kw)()
    return args, writes, {"blocks": blocks, "drop_one": drop_one, "replay": rrows}


def test_flow_dry_run_end_to_end(flow):
    args, writes, inp = flow
    rep = m.build(args())
    by = rep["selection_digest"]["rows_by_block"]
    new = by["T28"] + by["T01"]
    assert by["replay"] == math.floor(1.5 * new)                            # replay = floor(1.5 x new), always
    assert rep["g13_rows_dropped"] >= 1 and rep["refill"]["T28"]["refilled_rows"] >= 1   # pool_drops_r1 + refill
    ids = {r for r in inp["blocks"]["T28"][2]["selected_ids"]}
    assert rep["blocks"]["T28"]["selection"] == "crowd (C1 only)" and by["T28"] <= len(ids)
    t01 = inp["blocks"]["T01"][2]["target"]
    cap = (11 * t01) // 9                                                   # agent tier <= 55% of new rows
    assert rep["plan"]["agent_cap"]["applied"] and rep["plan"]["targets"] == {"T01": t01, "T28": min(cap, len(ids))}
    assert rep["agent_cap_reselect"]["T28"]["rows_after"] <= cap and 9 * by["T28"] <= 11 * by["T01"]
    assert rep["budget"]["final_total_usd"] < rep["t_core_usd"] == 32.0 and rep["t_max_usd"] == 32.0 and not rep["budget"]["trimmed"]   # A42-D 2.3 / A61 e: T_max = T_core
    assert rep["config_fill"]["seed"] == 20261013 and rep["caps"]["T28"]["easy_share"] <= 0.25
    probs = rep["problems"]
    assert any("minimum to train not met" in p for p in probs)             # 1 agent-core and 2 program families
    assert [p for p in probs if "frozen dev set" in p] == ["frozen dev set c2_mixdev missing (absent.jsonl; "
                                                            "spec 7.1: built before training)"]
    assert any("declares no parents" in p for p in probs) and any(p.startswith("A49 c T01") for p in probs)      # W6: the selection swaps units so the new yes/no share (was 0.744) now sits inside 45-55%; the A49 c overlay checks fire
    assert not any("yes/no rows" in p and "outside" in p for p in probs), [p for p in probs if "yes" in p]
    assert not any("G15" in p or "train_decoder" in p or "replay " in p for p in probs), probs
    assert not any("agent tier" in p or "above their planned" in p for p in probs), probs
    assert list(writes) == [str(m.WORK / "dryrun_c2.json")]                # the report only; no training file


def test_flow_budget_trim_reselects_and_keeps_replay_rule(flow, monkeypatch):
    args, writes, inp = flow

    def fake_proj(rows, rels, ntok, seed=m.SEED):
        return {"total_usd": round(len(rows) * 0.01, 2), "train_usd": round(len(rows) * 0.01, 2), "rows": len(rows)}
    monkeypatch.setattr(m, "project_cost", fake_proj)
    monkeypatch.setattr(m, "OVERHEAD_USD", 0.0)
    monkeypatch.setattr(m, "FLOOR_ROWS", 100)
    rep = m.build(args(spend_to_date=23.0))                                 # T_max = min(34, 32 - 23) = 9: ~900 rows
    by = rep["selection_digest"]["rows_by_block"]
    total = sum(by.values())
    assert rep["budget"]["trimmed"] and total <= 900 and rep["budget"]["final_total_usd"] <= 9.0
    assert by["replay"] == math.floor(1.5 * (by["T28"] + by["T01"]))
    first = rep["budget"]["rounds"][0]["trim"]["steps"][-1]["plan"]["targets"]   # item 10 / wave 2 / metadata: none here
    assert abs(first["T28"] / (first["T28"] + first["T01"]) - 0.55) < 0.06   # the family shares are kept
    assert not any("above their planned" in p or "replay " in p for p in rep["problems"]), rep["problems"]
    monkeypatch.setattr(m, "FLOOR_ROWS", 10 ** 6)                           # any trim now falls below the floor
    rows = [{"_block": "T28", "id": f"a{i}"} for i in range(1000)]
    rep2, probs = {"budget": {}}, []
    out = m.budget_trim(args(spend_to_date=23.0), rows, [], {}, {}, {}, {}, rep2, probs)   # dry run: a problem line, rows unchanged
    assert out == (rows, []) and "stop and ask the owner" in probs[0] and "stopped" in rep2["budget"]
    with pytest.raises(SystemExit, match="stop and ask the owner"):
        m.budget_trim(args(final=True, spend_to_date=23.0), rows, [], {}, {}, {}, {}, {"budget": {}}, [])


def test_flow_final_refuses_with_problems_and_writes_no_training_file(flow, monkeypatch, tmp_path):
    args, writes, inp = flow
    monkeypatch.setattr(m, "ohs4_problem", lambda sha, text, pinned=None: None)
    monkeypatch.setattr(m, "minimum_to_train", lambda entered: (True, {"ok": True}))
    with pytest.raises(SystemExit, match="needs --never-train-manifest"):          # A42-D 13.1 inputs are required
        m.build(args(final=True, ohs4_sha="e" * 64, decontam_drops=[]))
    man, gp = tmp_path / "never_train.json", tmp_path / "gproxy.jsonl"
    man.write_text('{"anchors": [{"name": "bfcl", "sha256": "' + "a" * 64 + '"}]}')
    gp.write_text('{"id": "g1"}\n')
    with pytest.raises(SystemExit, match="no training file written"):
        m.build(args(final=True, ohs4_sha="e" * 64, decontam_drops=[], never_train_manifest=man, gproxy_file=gp, credit_usd=100.0))
    assert str(m.OUT_TRAIN) not in writes and str(m.WORK / "final_refused_c2.json") in writes
    with pytest.raises(SystemExit, match="needs --credit-usd"):                    # A61 (e): the credit fit is required with --final
        m.build(args(final=True, ohs4_sha="e" * 64, decontam_drops=[], never_train_manifest=man, gproxy_file=gp))

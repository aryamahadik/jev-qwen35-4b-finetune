"""Tests for Ruling A59 in mix_c2.py / c2io.py: T46 DISPOSITION-GATE as a post-freeze agent-tier block (not a program family, not agent
core, not in the T40-T45 6,666 sum), its trim with T44 / T45 in wave 2, the pilot harm veto (iv), the owner's Arabic cap (SB4 + SB5 +
T46-ar <= 1,500; SB4 / SB5 cut in proportion, seeded, nothing refilled) and T46's replay as its own unit. In memory only. Run from c2_build:
  ../../.venv/bin/python -B -m pytest -q tests/test_mix_c2_t46.py
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
C2B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2B))
import c2io  # noqa: E402
import mix_c2 as m  # noqa: E402


def row(block, i, call=None, ar=False):
    return {"id": f"{block}-{i}", "call_id": call or f"{block}-c{i}", "_block": block, "source": "c2_x", "qtype": "noul", "gold": 1,
            "state": "s", "instructions": "i", "card": "", "options": None, "role": "base",
            "meta": {"lang_state": "ar" if ar else "en", "card_id": f"{block}:{i % 30}"}}


def test_registration():
    assert c2io.POST_FREEZE == {"T46": 1200} and c2io.ALL_TARGETS["T46"] == 1200
    assert "T46" not in c2io.TARGETS and "T46" not in c2io.NEW_FAMILIES and "T46" not in c2io.PROGRAM
    assert "T46" not in c2io.AGENT_CORE
    assert c2io.tier("T46") == "agent" and c2io.wave("T46") == 2
    assert "T46" in m.AGENT and "T46" in m.TARGETS and m.POST_FREEZE_SET == ("T46",)
    assert "T46" in m.WAVE2_NEW and set(m.WAVE2_NEW) >= {"T44", "T45"}
    assert sum(c2io.NEW_FAMILIES.values()) <= m.NEW_FAMILY_ROWS_MAX            # T46 does not enter the 6,666 sum


def test_minimum_to_train_ignores_t46():
    ok, rec = m.minimum_to_train(["T28", "T33", "T29", "T30", "T27", "T46"] + list(m.PROGRAM)[:4])
    assert "T46" not in rec["program_families"] and "T46" not in rec["agent_core"]


def test_agent_cap_cuts_t46_first_with_the_new_families():
    p = m.plan_shares({"T28": 2400, "T46": 1200, "T44": 833, "T01": 1600, "T23": 800, "T06": 900})
    assert p["targets"]["T46"] < 1200 and p["agent_cap"]["applied"]
    assert p["agent_cap"]["new_family_cut"]["T46"][0] == 1200
    q = m.plan_shares({"T28": 2400, "T46": 1200, "T01": 1600, "T23": 800, "T24": 600, "T06": 900, "T15": 900, "T12": 800})   # no cap: T46 keeps its 1,200
    assert q["targets"]["T46"] == 1200 and not q["agent_cap"]["applied"]


def test_pilot_harm_veto_is_binding_for_t46_only():
    rec = {"verdict": "PASS", "logged_utc": "2026-10-19T20:00:00+00:00", "own_dev_gain_pt": 3.0, "existing_dev_drop_pt": 0.2,
           "gproxy_change_ci_upper_pt": 0.1, "cautious_gold_acc_delta_pt": -1.0}
    assert m.pilot_problems("T46", rec) == []
    bad = dict(rec, cautious_gold_acc_delta_pt=-2.5)
    assert any("A59 f iv" in x for x in m.pilot_problems("T46", bad))
    assert any("A59 f iv" in x for x in m.pilot_problems("T46", {k: v for k, v in rec.items() if k != "cautious_gold_acc_delta_pt"}))
    assert m.pilot_problems("T44", rec) == []                                     # T40-T45 keep the three A42-D 4 conditions
    qc = {"pass": True, "passed_utc": "2026-10-19T11:00:00+00:00", "fix_iterations": 1}
    assert any("pilot" in x for x in m.admission("T46", qc, [], pilot=None))
    assert m.admission("T46", qc, [], pilot=rec) == []
    assert any("fix iterations" in x for x in m.admission("T46", dict(qc, fix_iterations=3), [], pilot=rec))


def test_per_card_cap_covers_t46():
    rows = [row("T46", i) for i in range(90)]
    for r in rows:
        r["meta"]["card_id"] = "T46:invoice:s0"
    rep, probs = m.cap_checks(rows, {r["id"]: 300 for r in rows}, final=False)
    assert any("a card holds 90 rows" in x for x in probs)


def test_arabic_cap_counts_every_block_and_trims_sb4_sb5_only():
    rows = ([row("SB4", i, ar=True) for i in range(900)] + [row("SB5", i, ar=True) for i in range(600)]
            + [row("T46", i, ar=True) for i in range(60)] + [row("T01", i) for i in range(50)])
    assert len(m.arabic_rows(rows)) == 1560
    rep, probs = m.cap_checks(rows, {r["id"]: 300 for r in rows}, final=False)
    assert rep["arabic_rows"]["total"] == 1560 and any("Arabic training rows" in x for x in probs)
    out, rels, info = m.arabic_cap_trim(rows, [])
    after = Counter(r["_block"] for r in m.arabic_rows(out))
    assert sum(after.values()) <= m.ARABIC_CAP and after["T46"] == 60               # T46's rows are never cut
    assert info["trimmed"] and info["refilled"] == 0 and len(out) < len(rows)
    assert abs((900 - after["SB4"]) / 900 - (600 - after["SB5"]) / 600) < 0.02      # proportional
    out2, _, info2 = m.arabic_cap_trim(rows, [])
    assert [r["id"] for r in out2] == [r["id"] for r in out]                        # seeded: same cut twice
    under, _, i3 = m.arabic_cap_trim(rows[:400], [])
    assert not i3["trimmed"] and len(under) == 400


def test_arabic_cap_cuts_whole_units():
    rows = [row("SB4", i, call=f"u{i // 3}", ar=True) for i in range(1560)]
    out, _, _ = m.arabic_cap_trim(rows, [])
    kept = Counter(r["call_id"] for r in out)
    assert all(v == 3 for v in kept.values())


def test_t46_replay_is_its_own_unit_and_drop_only():
    rows = [row("T46", i) for i in range(100)] + [row("replay", i, call=f"rp{i // 2}") for i in range(400)]
    out, rels, info = m.tag_replay_unit(rows, [])
    tagged = [r for r in out if (r["meta"] or {}).get("replay_unit") == "T46"]
    assert info["replay_rows_wanted"] == 150 and len(tagged) == 150 and info["replay_rows_tagged"] == 150
    assert all(r["_block"] == "replay" for r in tagged)
    assert Counter(Counter(r["call_id"] for r in tagged).values()) == {2: 75}       # whole units
    after, arels, d = m.drop_post_freeze(out, [])
    assert not any(r["_block"] == "T46" for r in after) and len(after) == 400 - 150 and d["g13_rerun"] is False

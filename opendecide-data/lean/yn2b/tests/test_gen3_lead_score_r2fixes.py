"""R2 fixes to gen3_lead_score (30 Sep), hand-computed:

1. gated rubrics: the recorded score "N of M gates passed" is the plain count of gates passed; the level still stops at
   the first failed gate (decide2's 7 train disagreements were exactly this);
2. judge contrast twins: a twin whose recorded score and level become consistent also carries the true reason;
3. judge cards: a disqualifier sets the level and leaves the computed score (the "score" of a disqualified lead);
4. recency coverage: older own statements that the newer one supersedes, and the use_oldest_statement shortcut.
"""
from __future__ import annotations

from f5_helpers import g, small_build
from test_gen3_lead_score_scorer import act, base_facts, claim


# ------------------------------------------------------------------------------------------------ 1. gated score
def _gated():
    return base_facts("gated", gates=[{"kind": "fit", "min": 200}, {"kind": "seniority", "bands": ["A", "B"]},
                                      {"kind": "engaged", "min": 10}], per_type_max=None,
                      levels=["Tier D", "Tier C", "Tier B", "Tier A"], handoff=2)


def test_gated_score_counts_every_gate_passed():
    f = _gated()
    f["lead"]["size_enrich"] = 100                          # gate 1 fails (100 < 200)
    f["lead"]["primary"]["title"] = "Director of Fleet Operations"   # seniority 3 -> band B: gate 2 passes
    f["acts"] = [act("demo", "2026-05-10")]                 # 15 >= 10: gate 3 passes
    r = g.evaluate(f)
    assert r["comps"]["gates"] == (False, True, True)
    assert r["level"] == 0                                  # fails gate 1 -> the base level
    assert r["score"] == "2 of 3 gates passed"              # but two gates are passed
    assert r["reason"] == "gate 1 failed, gate 2 passed, gate 3 passed"


def test_gated_disqualified_keeps_its_count():
    f = _gated()
    f["lead"]["primary"]["email"] = "sela.dorn@homemail.example"   # personal domain -> disqualified
    f["lead"]["primary"]["title"] = "Chief Operating Officer"
    f["acts"] = [act("demo", "2026-05-10")]
    r = g.evaluate(f)
    assert r["dq"] and r["level"] == 0 and r["score"] == "3 of 3 gates passed"
    assert g.evaluate(f, "ignore_disqualifier")["level"] == 3


def test_gated_record_consistent_iff_plain_count_and_level():
    f = _gated()
    f["lead"]["size_enrich"] = 100
    f["lead"]["primary"]["title"] = "Director of Fleet Operations"
    f["acts"] = [act("demo", "2026-05-10")]
    r = g.evaluate(f)
    L = f["rub"]["levels"]
    f["record"] = {"score": "2 of 3 gates passed", "level": L[0], "reason": r["reason"], "mode": None}
    assert g.answer(f, r, "judge") == "yes"
    f["record"] = dict(f["record"], score="0 of 3 gates passed")       # the old in-order count: now inconsistent
    assert g.answer(f, r, "judge") == "no"


# ------------------------------------------------------------------------------------------------ 3. judge cards
def test_judge_cards_define_the_disqualified_score():
    for d in g.JUDGE_DEFS:
        assert "recorded" in d["yes"] and "disqualifier" in d["yes"] and "disqualifier" in d["no"]
        for w in ("other", "different"):
            assert w not in d["yes"].split()                 # decide2 reads 'yes' as the positive answer
        assert "score" in d["yes"] and "level" in d["yes"]
        for bad in ("right", "wrong", "correct", "accurate", "mistaken", "agreed", "disagree"):
            assert bad not in (d["yes"] + " " + d["no"]).lower().split()   # SPEC 4.7 judge-view word ban


# ------------------------------------------------------------------------------------------------ 4. recency
def test_most_recent_statement_decides_and_oldest_is_a_shortcut():
    f = base_facts()
    f["claims"] = [claim("budget", day="2026-04-20", status="approved", amount=60000, period="year"),  # counts
                   claim("budget", day="2026-05-05", status="hoped", amount=90000, period="year")]    # newest
    r = g.evaluate(f)
    assert r["comps"]["budget"] == 0                                    # the newest statement is a hope: no points
    assert g.evaluate(f, "use_oldest_statement")["comps"]["budget"] == 10
    f["claims"].reverse()                                              # order in the list does not matter
    assert g.evaluate(f)["comps"]["budget"] == 0


def test_boss_quote_newer_than_own_statement_leaves_the_own_one():
    f = base_facts()
    f["claims"] = [claim("timeline", day="2026-04-01", date="2026-06-01"),                        # 18 days: in
                   claim("timeline", speaker="boss", day="2026-05-10", date="2027-01-01", boss="CFO")]
    assert g.evaluate(f)["comps"]["timeline"] == 10
    assert g.evaluate(f, "trust_rep_notes")["comps"]["timeline"] == 0


def _older_pairs(rows_facts):
    """(kind, older, newer) own statements of one kind where both would be read by the rubric's evidence rule."""
    out = []
    for f in rows_facts:
        rub = g.eff_rub(f)
        for kind in ("budget", "timeline", "need"):
            own = sorted((c for c in f["claims"] if c["kind"] == kind and c["speaker"] == "primary"),
                         key=lambda c: c["ts"])
            sw = rub.get("stmt_window")
            today = g.D(f["today"])
            if sw:
                own = [c for c in own if g.in_window((today - g.ts_day(c["ts"])).days, sw)]
            if len(own) >= 2:
                out.append((kind, own[0], own[-1], f))
    return out


def test_small_build_has_superseded_statements_and_they_are_inert():
    fb, b = small_build()
    pairs = _older_pairs(b.facts.values())
    assert len(pairs) >= 10, len(pairs)
    for kind, old, new, f in pairs:
        assert g.ts_day(old["ts"]) < g.ts_day(new["ts"])           # at least a day apart, never the same moment
        assert old["channel"] == "msg"
        if kind == "timeline":
            assert g.D(old["date"]) > g.ts_day(old["ts"])          # a target date after the day it was stated
        # removing the superseded statement never changes the result under the rubric as written
        f2 = dict(f, claims=[c for c in f["claims"] if c is not old])
        assert g.evaluate(f2)["comps"] == g.evaluate(f)["comps"]


def test_use_oldest_statement_is_a_named_solver_and_balanced():
    fb, b = small_build()
    assert "use_oldest_statement" in g.MODES
    for arch in g.APPLICABLE:
        assert "use_oldest_statement" in g.APPLICABLE[arch]
    hits = [r["meta"]["shortcut_hits"]["use_oldest_statement"] for r in fb.rows
            if "use_oldest_statement" in (r["meta"]["shortcut_hits"] or {})]
    assert hits, "the solver never answered a row"


# ------------------------------------------------------------------------------------------------ 2. judge twins
def test_judge_rows_with_yes_gold_carry_the_true_reason():
    fb, b = small_build()
    for r in fb.rows:
        if g.kind_of_row(r) != "judge" or r["gold"] != "yes":
            continue
        f = b.row_facts[r["rid"]]
        assert g.evaluate(f)["reason"] == f["record"]["reason"], r["rid"]



def test_no_latent_has_an_empty_activity_list():
    """A table renders an empty activity list as '(none)', which decide2 does not read; the sampler always leaves at
    least one (0-point) entry."""
    fb, b = small_build()
    for f in list(b.facts.values()) + list(b.twin_facts.values()):
        assert f["acts"], f["lead"]["id"]
    for r in fb.rows:
        assert "(none)" not in r["state"], r["rid"]

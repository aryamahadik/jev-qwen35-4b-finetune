"""F5 scorer (gen3_lead_score.evaluate / decide): hand-computed cases for every archetype and every rule.

Each case builds a latent by hand and checks the components against arithmetic done in the comment next to it.
"""
from __future__ import annotations

import copy

import pytest

from f5_helpers import g, mv

TODAY = "2026-05-14"
TITLES = {"Chief Operating Officer": 4, "VP of Logistics": 4, "Director of Fleet Operations": 3, "Fleet Manager": 2,
          "Routing Analyst": 1, "Dispatch Coordinator": 0, "Executive Assistant to the VP of Logistics": 0}


def ts(day: str, hm: str = "10:00") -> str:
    return f"{day}T{hm}:00Z"


def base_facts(arch="points", **rub_over):
    rub = {"rid": "LQ-10", "version": 1, "effective": "2026-01-01", "levels": ["Cold", "Warm", "Hot", "Sales-ready"],
           "handoff": 2, "size_source": "enrichment", "title_sen": dict(TITLES), "dq": ["personal_email"],
           "competitors": ["Vexo Labs"], "personal_domains": ["homemail.example"], "regions": ["Midwest"],
           "min_size": None, "amend": None, "override": None, "rep_timeline": False,
           "budget": {"amount": 45000, "period": "year", "statuses": ["approved", "requested"], "points": 10},
           "timeline": {"days": 90, "incl": True, "points": 10},
           "acts": {"demo": 15, "pricing": 5, "webinar": 8}, "window": {"days": 30, "incl": True}, "cap": 25,
           "per_type_max": None, "unsub": 10,
           "size_bands": [[0, 0], [50, 5], [250, 10], [1000, 15]],
           "sen_points": {"4": 20, "3": 15, "2": 10, "1": 5, "0": 0}, "thresholds": [20, 35, 50]}
    rub.update(rub_over)
    lead = {"id": "L3319027", "decoy_id": "L3319072", "company": "Brivo Freight", "domain": "brivo.example",
            "region": "Midwest", "customer": False, "created": "2026-01-01", "owner": "Tam Vire", "stage": "new",
            "primary": {"name": "Sela Dorn", "title": "Fleet Manager", "email": "sela.dorn@brivo.example"},
            "secondary": None, "size_enrich": 300, "size_form": [51, 200], "lookalike": None}
    return {"arch": arch, "pack": "fleet_telematics", "today": TODAY, "rub": rub, "lead": lead, "acts": [],
            "claims": [], "form_ts": ts("2026-05-01"), "fillers": {"msgs": [], "notes": []}, "record": None,
            "surface": {}}


def act(t, day, lead="L3319027", status=None, hm="10:00"):
    a = {"eid": "", "ts": ts(day, hm), "lead": lead, "type": t, "status": status, "name": None}
    if t in g.ATTENDABLE:
        a["status"] = status or "attended"
        a["name"] = "Route planning basics"
    return a


def claim(kind, speaker="primary", day="2026-05-01", hm="09:00", channel="msg", **kw):
    c = {"cid": "", "ts": ts(day, hm), "kind": kind, "speaker": speaker, "channel": channel}
    c.update(kw)
    return c


# ---------------------------------------------------------------------------------------------- points
def test_points_components_by_hand():
    f = base_facts()
    f["acts"] = [act("demo", "2026-05-11"),                      # age 3: 15
                 act("demo", "2026-05-11", hm="10:05"),          # same type, same day: counts once
                 act("pricing", "2026-04-14"),                   # age 30, inclusive window: 5
                 act("webinar", "2026-05-09", status="registered"),  # registration alone: 0
                 act("pricing", "2026-05-12", lead="L3319072"),  # another lead id: 0
                 act("demo", "2026-04-13")]                      # age 31: outside the window
    f["claims"] = [claim("budget", status="approved", amount=4000, period="month"),  # 48,000 / year >= 45,000
                   claim("timeline", day="2026-05-02", date="2026-08-12")]           # 90 days after: inclusive
    r = g.evaluate(f)
    # size 300 -> 10; Fleet Manager (seniority 2) -> 10; activity 15 + 5 = 20 (cap 25); budget 10; timeline 10
    assert r["comps"] == {"size": 10, "title": 10, "act": 20, "neg": 0, "budget": 10, "timeline": 10, "total": 60,
                          "base_level": 3, "override": None, "dq": False, "level": 3}
    assert r["score"] == "60 points" and g.decide(f, {"kind": "score"})[0] == "Sales-ready"
    assert g.decide(f, {"kind": "ready"})[0] == "yes"
    m = g.all_modes(f)
    assert m["count_registrations"]["comps"]["act"] == 25          # 20 + 8 = 28, capped at 25
    assert m["count_duplicates"]["comps"]["act"] == 25             # 35 capped
    assert m["count_decoy_ids"]["comps"]["act"] == 25              # 20 + 5
    assert m["ignore_window"]["comps"]["act"] == 25                # + the day-31 demo, capped
    assert m["ignore_cap"]["comps"] == r["comps"]                  # 20 < 25: the cap does not bind here
    assert m["monthly_as_annual"]["comps"]["budget"] == 0          # $4,000 read as yearly < $45,000


def test_window_exclusive_boundary():
    f = base_facts(window={"days": 30, "incl": False})
    f["acts"] = [act("pricing", "2026-04-14")]                     # exactly 30 days old
    assert g.evaluate(f)["comps"]["act"] == 0
    f["rub"]["window"]["incl"] = True
    assert g.evaluate(f)["comps"]["act"] == 5


def test_cap_unsub_and_floor_at_zero():
    f = base_facts()
    f["lead"]["size_enrich"] = 10
    f["lead"]["primary"]["title"] = "Dispatch Coordinator"
    f["acts"] = [act("unsub", "2026-05-10"), act("unsub", "2026-05-10", hm="11:00"), act("unsub", "2026-05-01"),
                 act("unsub", "2026-03-01")]  # same day once, two days in the window, one outside
    r = g.evaluate(f)
    assert r["comps"]["neg"] == 20 and r["comps"]["total"] == 0 and r["level"] == 0
    f2 = base_facts()
    f2["acts"] = [act("demo", "2026-05-10"), act("demo", "2026-05-09"), act("pricing", "2026-05-08")]
    assert g.evaluate(f2)["comps"]["act"] == 25                    # 35 capped at 25
    assert g.evaluate(f2, "ignore_cap")["comps"]["act"] == 35


def test_budget_periods_and_boundaries():
    f = base_facts()
    f["claims"] = [claim("budget", status="approved", amount=3750, period="month")]   # 45,000 exactly
    assert g.evaluate(f)["comps"]["budget"] == 10
    f["claims"][0]["amount"] = 3749                                                    # 44,988
    assert g.evaluate(f)["comps"]["budget"] == 0
    f = base_facts(budget={"amount": 4000, "period": "month", "statuses": ["approved"], "points": 10})
    f["claims"] = [claim("budget", status="approved", amount=48000, period="year")]    # 4,000 per month
    assert g.evaluate(f)["comps"]["budget"] == 10
    f["claims"][0]["status"] = "requested"                                             # not a counting status here
    assert g.evaluate(f)["comps"]["budget"] == 0
    f["claims"][0].update(status="hoped")
    assert g.evaluate(f)["comps"]["budget"] == 0


def test_evidence_rep_notes_boss_quotes_latest_wins():
    f = base_facts()
    f["claims"] = [claim("budget", status="hoped", amount=50000, period="year", day="2026-05-01"),
                   claim("budget", speaker="rep", channel="note", status="approved", amount=90000, period="year",
                         day="2026-05-05"),
                   claim("budget", speaker="boss", status="approved", amount=90000, period="year", day="2026-05-06",
                         boss="CFO")]
    r = g.evaluate(f)
    assert r["comps"]["budget"] == 0                               # own statement: hoped; rep and boss never count
    assert g.evaluate(f, "trust_rep_notes")["comps"]["budget"] == 10
    f["claims"].append(claim("budget", status="approved", amount=45000, period="year", day="2026-05-07"))
    assert g.evaluate(f)["comps"]["budget"] == 10                  # the most recent evidence statement is used
    # timeline: a rep note counts only when the rubric says so
    f = base_facts()
    f["claims"] = [claim("timeline", speaker="rep", channel="note", date="2026-06-01")]
    assert g.evaluate(f)["comps"]["timeline"] == 0
    f["rub"]["rep_timeline"] = True
    assert g.evaluate(f)["comps"]["timeline"] == 10


def test_wrong_contact_and_assistant_title():
    f = base_facts()
    f["lead"]["primary"]["title"] = "Executive Assistant to the VP of Logistics"
    f["lead"]["secondary"] = {"name": "Ivo Stern", "title": "VP of Logistics", "email": "ivo.stern@brivo.example"}
    f["claims"] = [claim("budget", speaker="secondary", status="approved", amount=60000, period="year")]
    r = g.evaluate(f)
    assert r["comps"]["title"] == 0 and r["comps"]["budget"] == 0  # assistants score 0; the other contact's words no
    assert g.evaluate(f, "title_keyword")["comps"]["title"] == 20  # reads 'VP' in the title
    w = g.evaluate(f, "score_wrong_contact")["comps"]
    assert w["title"] == 20 and w["budget"] == 10


def test_disqualifiers_and_lookalike():
    f = base_facts(dq=["personal_email", "region", "competitor", "customer"])
    f["acts"] = [act("demo", "2026-05-10")]
    f["lead"]["size_enrich"] = 2000
    assert g.evaluate(f)["level"] == 2                             # size 15 + title 10 + demo 15 = 40 -> Hot
    for mut in (("region", "Gulf Coast"), ("customer", True), ("company", "Vexo Labs")):
        h = copy.deepcopy(f)
        h["lead"][mut[0]] = mut[1]
        assert g.evaluate(h)["level"] == 0 and g.evaluate(h, "ignore_disqualifier")["level"] == 2
    h = copy.deepcopy(f)
    h["lead"]["primary"]["email"] = "sela.dorn@homemail.test"      # a look-alike of homemail.example: not listed
    h["lead"]["lookalike"] = "email"
    assert g.evaluate(h)["level"] == 2 and g.evaluate(h, "lookalike_match")["level"] == 0


def test_override_ceiling_and_floor():
    f = base_facts(override={"kind": "ceiling", "level": 1})
    f["lead"]["size_enrich"] = 2000
    f["lead"]["primary"]["title"] = "VP of Logistics"              # 15 + 20 = 35 -> Hot before the override
    r = g.evaluate(f)
    assert r["comps"]["base_level"] == 2 and r["level"] == 1 and r["comps"]["override"] == "ceiling"
    assert g.evaluate(f, "ignore_override")["level"] == 2
    f["claims"] = [claim("budget", status="approved", amount=45000, period="year")]
    assert g.evaluate(f)["level"] == 2                             # 45 points (Hot), budget counts: no ceiling
    f = base_facts(override={"kind": "floor", "level": 2})
    f["acts"] = [act("demo", "2026-05-10")]                        # 10 + 10 + 15 = 35 -> Hot already
    f["lead"]["size_enrich"] = 10
    r = g.evaluate(f)                                               # 0 + 10 + 15 = 25 -> Warm, floor lifts to Hot
    assert r["comps"]["base_level"] == 1 and r["level"] == 2 and r["comps"]["override"] == "floor"


def test_amendment_effective_on_the_day():
    f = base_facts(amend={"n": 1, "effective": TODAY, "param": "cap", "old": 25, "new": 30})
    f["acts"] = [act("demo", "2026-05-10"), act("demo", "2026-05-09"), act("pricing", "2026-05-08")]
    assert g.evaluate(f)["comps"]["act"] == 30                     # effective on the scoring date: in force
    assert g.evaluate(f, "ignore_amendment")["comps"]["act"] == 25
    f["rub"]["amend"]["effective"] = "2026-05-15"
    assert g.evaluate(f)["comps"]["act"] == 25
    assert g.evaluate(f, "early_amendment")["comps"]["act"] == 30


# ---------------------------------------------------------------------------------------------- bant / gated / weighted
def test_bant_statement_window_and_count_map():
    f = base_facts("bant", stmt_window={"days": 30, "incl": False}, auth_min=3,
                   needs=["reducing fuel costs", "tracking driver hours", "cutting late deliveries"],
                   count_map=[0, 0, 1, 2, 2], levels=["Cold", "Warm", "Hot"], handoff=2)
    f["lead"]["primary"]["title"] = "Director of Fleet Operations"            # authority met
    f["claims"] = [claim("budget", status="approved", amount=50000, period="year", day="2026-04-14"),  # 30 days old
                   claim("need", need="reducing fuel costs", day="2026-05-01"),
                   claim("timeline", date="2026-09-01", day="2026-05-01")]    # 110 days: too far
    r = g.evaluate(f)
    assert r["comps"] == {"budget": False, "authority": True, "need": True, "timeline": False, "count": 2,
                          "dq": False, "level": 1}
    assert r["score"] == "2 of 4 criteria met"
    assert g.evaluate(f, "ignore_window")["comps"]["count"] == 3
    f["rub"]["dq"] = ["small"]
    f["rub"]["min_size"] = 400
    assert g.evaluate(f)["level"] == 0 and g.evaluate(f, "use_self_reported_size")["level"] == 0


def test_gated_order_matters():
    f = base_facts("gated", gates=[{"kind": "fit", "min": 200}, {"kind": "seniority", "bands": ["A", "B"]},
                                   {"kind": "engaged", "min": 10}], per_type_max=1)
    f["acts"] = [act("demo", "2026-05-10"), act("demo", "2026-05-09")]        # one demo per type: 15
    r = g.evaluate(f)                                                         # 300 >= 200; Fleet Manager is band C
    assert r["comps"]["gates"] == (True, False, True) and r["level"] == 1
    # R2 fix: the score is the plain count of gates passed (2); only the level stops at the first failed gate
    assert r["score"] == "2 of 3 gates passed"
    io = g.evaluate(f, "ignore_gate_order")
    assert io["level"] == 2 and io["score"] == r["score"]          # the misreading changes the level, not the score
    assert g.evaluate(f, "ignore_cap")["comps"]["act"] == 30                  # the per-type maximum is a cap


def test_weighted_tie_break():
    f = base_facts("weighted", fit_bands=[[0, 0], [50, 1], [250, 2], [1000, 3]],
                   role_map={"4": 3, "3": 2, "2": 1, "1": 0, "0": 0}, eng_bands=[[0, 0], [5, 1], [15, 2], [25, 3]],
                   timeline={"tiers": [30, 60, 120]}, weights={"fit": 2, "role": 2, "eng": 1, "budget": 3,
                                                                 "timeline": 2}, thresholds=[6, 12, 18])
    f["rub"]["budget"]["statuses"] = ["approved", "requested"]
    # fit 2 (300) x2 = 4, role 1 (Fleet Manager) x2 = 2, eng 0, budget 0, timeline 0 -> 6 = the lowest total of Warm
    r = g.evaluate(f)
    assert r["comps"]["total"] == 6 and r["level"] == 0 and r["comps"]["tie_down"]   # budget score < 2: level below
    assert g.evaluate(f, "ignore_tiebreak")["level"] == 1
    f["claims"] = [claim("budget", status="approved", amount=10000, period="year")]  # below the minimum: score 1
    r = g.evaluate(f)
    assert r["comps"]["budget"] == 1 and r["comps"]["total"] == 9 and r["level"] == 1
    f["claims"] = [claim("timeline", date="2026-06-13")]                              # 30 days: score 3
    assert g.evaluate(f)["comps"]["timeline"] == 3


# ---------------------------------------------------------------------------------------------- decide + shortcuts
def test_decide_judge_and_undefined():
    f = base_facts()
    assert mv.is_undefined(g.decide(f, {"kind": "judge"})[0])       # no record: the predicate does not apply
    r = g.evaluate(f)                                              # size 10 + title 10 = 20 -> Warm
    f["record"] = {"score": r["score"], "level": "Warm", "reason": r["reason"], "mode": None}
    assert g.decide(f, {"kind": "judge"})[0] == "yes"
    f["record"]["score"] = "21 points"
    assert g.decide(f, {"kind": "judge"})[0] == "no"


def test_shortcut_answers_abstain_when_nothing_changes():
    f = base_facts()
    f["lead"]["size_enrich"] = 100                                   # both size sources in the 50-249 band
    f["acts"] = [act("demo", "2026-05-10")]                          # 5 + 10 + 15 = 30 -> Warm
    sa = g.shortcut_answers(f, "score")
    assert all(v is None for v in sa.values())                       # no trap in this item
    f["acts"].append(act("webinar", "2026-05-09", status="registered"))
    sa = g.shortcut_answers(f, "score")                              # counting it: 38 -> Hot (an active trap)
    assert sa["count_registrations"] == "Hot" and g.decide(f, {"kind": "score"})[0] == "Warm"
    assert sum(v is not None for v in sa.values()) == 1


def test_trace_is_grounded_in_every_format():
    f = base_facts()
    f["rub"]["order"] = ["scope", "evidence", "size_source", "size_points", "title_points", "activity_points",
                         "window", "cap", "unsub", "budget", "timeline", "levels", "dq", "handoff"]
    f["acts"] = [act("demo", "2026-05-10")]
    f["claims"] = [claim("budget", status="approved", amount=4000, period="month", channel="form",
                         day="2026-05-01"),
                   claim("timeline", date="2026-06-01", day="2026-05-02", hm="09:30")]
    f["form_ts"] = ts("2026-05-01", "09:00")
    f["surface"] = {"perm_seed": 3}
    gold, trace = g.decide(f, {"kind": "score"})
    for fmt in g.FMTS:
        st = g.render_state(f, fmt)
        for s in trace["decisive"]:
            assert s in st or s.replace('"', '\\"') in st, (fmt, s)


@pytest.mark.parametrize("arch", ["points", "bant", "gated", "weighted"])
def test_random_latents_score_the_same_from_text(arch):
    import random
    from datetime import date
    rng = random.Random(7)
    pool = mv.NamePool("train")
    for _ in range(25):
        K = rng.choice([3, 4, 5])
        levels, fh = rng.choice(list(g.LEVEL_SCHEMES[K].values()))
        rub = g.sample_rubric(rng, arch, "payroll_hr", K, levels, fh, rng.choice(["easy", "standard", "hard"]), pool,
                              date(2026, 6, 1))
        f = {"arch": arch, "pack": "payroll_hr", "today": "2026-06-01", "rub": rub, "surface": {"perm_seed": 1}}
        g.sample_lead(rng, f, pool, "hard", g.make_plan(rng, f, rng.randrange(K), None), 0.45, rng.random() < 0.4)
        r0 = g.evaluate(f)
        for fmt in ("json", "prose", "log:shuffled", "table:csv"):
            r1 = g.evaluate(g.facts_from_text(g.render_state(f, fmt), fmt))
            assert (r1["level"], r1["score"], r1["comps"]) == (r0["level"], r0["score"], r0["comps"])

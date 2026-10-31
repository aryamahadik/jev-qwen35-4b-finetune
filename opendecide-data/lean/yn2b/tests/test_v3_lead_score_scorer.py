"""Hand-computed cases for the F5 decide2 (golden_src/gen3/v3_lead_score.py): every archetype and the rubric rules
that carry the family's hard cases. All leads, names and rubrics here are invented for the test."""
from __future__ import annotations

import pytest

from v3f5_helpers import (ACT, EVID, SCOPE, SIZE_ENR, SIZE_FORM, STATUS, TITLE, base_form, base_lead, points_rules,
                          render_json, render_text, row, score_of, v3, window)

D = "2026-03-31"          # scoring date for the points cases
L = "L1000001"


def pts(rules=None, lead=None, form=None, activity=(), messages=(), notes=(), date=D, **kw):
    return score_of(render_text(TITLE, rules or points_rules(**kw), date, lead or base_lead(),
                                form or base_form(), activity, messages, notes))


# ------------------------------------------------------------------------------------------------ points archetype
BASE_ACT = [("2026-03-20T09:00:00Z", L, "demo request"),                       # age 11 -> 10
            ("2026-03-01T23:30:00Z", L, "webinar 'Zorb basics': attended")]    # age 30 exactly -> 6 if inclusive
TGT60 = [("2026-02-01T09:00:00Z", "Ada Quibble", "Our target date for going live is 2026-05-30.")]   # +60 days


def test_points_hand_total_and_level():
    # title Zorb Analyst 4 + size 120 -> 5 + activity 16 + timeline 5 = 30 -> Keen lead (30 or more)
    r = pts(lead=base_lead(**{"Primary contact title": "Zorb Analyst"}), activity=BASE_ACT, messages=TGT60)
    assert r.parts["title"] == 4 and r.parts["size"] == 5 and r.parts["activity"] == 16 and r.parts["timeline"] == 5
    assert (r.score, r.level, r.ready) == (30, "Keen lead", True)


def test_activity_window_inclusive_vs_exclusive():
    lead = base_lead(**{"Primary contact title": "Zorb Analyst"})
    assert pts(lead=lead, activity=BASE_ACT, messages=TGT60, win=(30, False)).level == "Mild lead"   # 29
    assert pts(lead=lead, activity=BASE_ACT, messages=TGT60, win=(30, True)).level == "Keen lead"    # 30


def test_timeline_at_most_vs_fewer_than():
    lead = base_lead(**{"Primary contact title": "Zorb Analyst"})
    assert pts(lead=lead, activity=BASE_ACT, messages=TGT60, tl_inclusive=False).score == 25
    assert pts(lead=lead, activity=BASE_ACT, messages=TGT60, tl_inclusive=True).score == 30
    past = [("2026-02-01T09:00:00Z", "Ada Quibble", "Our target date for going live is 2026-03-30.")]
    assert pts(lead=lead, activity=BASE_ACT, messages=past).parts["timeline"] == 0


@pytest.mark.parametrize("stmt,minimum,met", [
    ("We have an approved budget of $5,000 per month for this.", "$60,000 per year", True),     # 60,000 / yr
    ("We have an approved budget of $4,999 per month for this.", "$60,000 per year", False),    # 59,988 / yr
    ("We have an approved budget of $60,000 per year for this.", "$5,000 per month", True),
    ("We have an approved budget of $59,999 per year for this.", "$5,000 per month", False),
    ("We have requested a budget of $90,000 per year for this.", "$60,000 per year", False),    # status not counted
    ("We hope to get a budget of $90,000 per year for this.", "$60,000 per year", False),
    ("If we had a budget of $9,000 per month, we would buy this.", "$60,000 per year", False),
])
def test_budget_monthly_vs_annual_and_status(stmt, minimum, met):
    r = pts(messages=[("2026-03-02T09:00:00Z", "Ada Quibble", stmt)], budget_min=minimum)
    assert (r.parts["budget"] == 10) is met


def test_requested_counts_when_listed():
    r = pts(messages=[("2026-03-02T09:00:00Z", "Ada Quibble", "We have requested a budget of $90,000 per year for "
                                                               "this.")], statuses="approved and requested")
    assert r.parts["budget"] == 10


def test_only_own_words_count():
    big = "an approved budget of $90,000 per year"
    msgs = [("2026-03-02T09:00:00Z", "Ada Quibble", f"My CFO says we have {big}."),              # reported speech
            ("2026-03-03T09:00:00Z", "Ben Quibble", f"We have {big} for this."),                 # another person
            ("2026-03-04T09:00:00Z", "Ada Quibble", "My COO wants this live by 2026-04-15.")]    # reported target
    notes = [("2026-03-05T09:00:00Z", "Rex Pellow", f"Call notes: the prospect has {big}."),
             ("2026-03-05T10:00:00Z", "Rex Pellow", "Call notes: the prospect's target date for going live is "
                                                    "2026-04-15.")]
    r = pts(lead=base_lead(**{"Other contact": "Ben Quibble", "Other contact title": "Chief Zorbing Officer",
                              "Other contact email": "ben.quibble@quorbel.test"}), messages=msgs, notes=notes)
    assert r.parts["budget"] == 0 and r.parts["timeline"] == 0 and r.parts["title"] == 10


def test_rep_note_target_counts_only_when_the_rubric_says_so():
    notes = [("2026-03-05T10:00:00Z", "Rex Pellow", "Call notes: the prospect's target date for going live is "
                                                    "2026-04-15.")]
    assert pts(notes=notes, rep_target=True).parts["timeline"] == 5
    assert pts(notes=notes, rep_target=False).parts["timeline"] == 0


def test_most_recent_statement_decides():
    msgs = [("2026-03-01T09:00:00Z", "Ada Quibble", "We have an approved budget of $90,000 per year for this."),
            ("2026-03-10T09:00:00Z", "Ada Quibble", "We hope to get a budget of $90,000 per year for this.")]
    assert pts(messages=msgs).parts["budget"] == 0
    assert pts(messages=list(reversed([(t, w, s) for t, w, s in msgs]))).parts["budget"] == 0  # order in text is moot
    # the web form is a statement at its submission time
    form = base_form(**{"Submitted at": "2026-03-20T09:00:00Z", "Budget status": "approved",
                        "Budget amount": "$7,000 per month"})
    assert pts(messages=msgs, form=form).parts["budget"] == 10


def test_scope_registrations_duplicates_and_limits():
    act = [("2026-03-20T09:00:00Z", "L1000010", "demo request"),                     # decoy lead id
           ("2026-03-21T09:00:00Z", L, "webinar 'Zorb basics': registered, did not attend"),
           ("2026-03-22T09:00:00Z", L, "pricing page visit"),
           ("2026-03-22T18:00:00Z", L, "pricing page visit"),                           # same type, same day
           ("2026-03-23T09:00:00Z", L, "pricing page visit"),
           ("2026-03-24T09:00:00Z", L, "guide download: Zorb field guide"),
           ("2026-03-25T09:00:00Z", L, "careers page visit")]                           # not in the table
    assert pts(activity=act).parts["activity"] == 3 + 3 + 2
    assert pts(activity=act, act_limit=1).parts["activity"] == 3 + 2


def test_activity_cap():
    act = [(f"2026-03-{d:02d}T09:00:00Z", L, "demo request") for d in (20, 21, 22)]
    assert pts(activity=act, cap=25).parts["activity"] == 25
    assert pts(activity=act, cap=40).parts["activity"] == 30


def test_unsubscribes_and_floor_at_zero():
    lead = base_lead(**{"Primary contact title": "Assistant to the Zorb Director"})
    act = [("2026-03-20T09:00:00Z", L, "unsubscribe from marketing email"),
           ("2026-03-20T15:00:00Z", L, "unsubscribe from marketing email"),     # same day: once
           ("2026-03-22T09:00:00Z", L, "unsubscribe from marketing email"),
           ("2026-01-02T09:00:00Z", L, "unsubscribe from marketing email"),     # outside the window
           ("2026-03-23T09:00:00Z", L, "pricing page visit")]
    r = pts(lead=lead, activity=act, unsub=2, size=SIZE_FORM)
    assert r.parts["unsubscribes"] == -4 and r.parts["activity"] == 3
    assert r.score == 0 and r.level == "Pale lead"          # 3 - 4 = -1 -> floored at 0


def test_override_ceiling_and_floor():
    lead = base_lead(**{"Primary contact title": "Chief Zorbing Officer"})     # 20
    act = [("2026-03-20T09:00:00Z", L, "demo request")]                        # 10 -> 20 + 5 + 10 = 35
    assert pts(lead=lead, activity=act).level == "Keen lead"
    assert pts(lead=lead, activity=act, override="ceiling").level == "Mild lead"
    msgs = [("2026-03-02T09:00:00Z", "Ada Quibble", "We have an approved budget of $90,000 per year for this.")]
    assert pts(lead=lead, activity=act, messages=msgs, override="ceiling").level == "Keen lead"
    low = base_lead(**{"Primary contact title": "Assistant to the Zorb Director", "Enrichment lookup": "10 employees"})
    assert pts(lead=low, activity=act, override="floor").level == "Mild lead"   # 10 points, demo counts
    old = [("2026-02-01T09:00:00Z", L, "demo request")]                          # outside the window
    assert pts(lead=low, activity=old, override="floor").level == "Pale lead"


@pytest.mark.parametrize("disq,lead_kw,hit", [
    ("the primary contact's email domain is a personal email domain (zorbmail.test, quibpost.example)",
     {"Primary contact email": "ada.quibble@zorbmail.test"}, True),
    ("the primary contact's email domain is a personal email domain (zorbmail.test, quibpost.example)",
     {"Primary contact email": "ada.quibble@zorb-mail.test"}, False),                  # look-alike is not listed
    ("the company is on the competitor list (Quorbel Works, Zanto Labs)", {}, True),
    ("the company is on the competitor list (Quorbel Workshop, Zanto Labs)", {}, False),
    ("the company's region is not a served region (served regions: Midwest, Southeast)", {}, True),
    ("the company is a current customer", {"Current customer": "yes"}, True),
    ("the company has fewer than 150 employees (company size as in rule 3)", {}, True),  # enrichment 120
])
def test_disqualifiers(disq, lead_kw, hit):
    lead = base_lead(**{"Primary contact title": "Chief Zorbing Officer", **lead_kw})
    act = [("2026-03-20T09:00:00Z", L, "demo request")]
    r = pts(lead=lead, activity=act, disq=disq)
    assert (r.level == "Pale lead") is hit
    assert r.score == 35                     # a disqualified lead keeps its points; only the level drops


def test_amendments_in_and_out_of_force():
    lead = base_lead(**{"Primary contact title": "Zorb Analyst"})
    am = ["Amendment 1, effective 2026-03-31, applies to leads scored on or after that date: in rule 8, the activity "
          "cap changes from 20 to 12 points."]
    act = BASE_ACT
    assert pts(lead=lead, activity=act, messages=TGT60, amendments=am).parts["activity"] == 12        # on the date
    later = ["Amendment 1, effective 2026-04-01, applies to leads scored on or after that date: in rule 8, the "
             "activity cap changes from 20 to 12 points."]
    assert pts(lead=lead, activity=act, messages=TGT60, amendments=later).parts["activity"] == 16     # not yet
    lvl = ["Amendment 1, effective 2026-01-01, applies to leads scored on or after that date: in rule 11, the lowest "
           "total for Keen lead changes from 30 to 31 points."]
    assert pts(lead=lead, activity=act, messages=TGT60, amendments=lvl).level == "Mild lead"         # 30 < 31
    bad = ["Amendment 1, effective 2026-01-01, applies to leads scored on or after that date: in rule 8, the activity "
           "cap changes from 99 to 12 points."]
    with pytest.raises(v3.ParseError):
        pts(lead=lead, activity=act, messages=TGT60, amendments=bad)


# ------------------------------------------------------------------------------------------------ BANT
BANT = [SCOPE, EVID.format(exc=""),
        "Statement window: only statements at most 30 days old on the scoring date are evidence; a statement exactly "
        "30 days old is. Age is the scoring date minus the statement's date.", SIZE_ENR,
        "Budget criterion: met when the most recent budget statement that is evidence under rules 2 and 3 has a "
        "counting status and an amount of at least $50,000 per year. Counting statuses: approved and requested. "
        + STATUS,
        "Need criterion: met when the most recent main-problem statement that is evidence under rules 2 and 3 names "
        "one of: slow zorb audits; lost zorb parts.",
        "Timeline criterion: met when the most recent target date that is evidence under rules 2 and 3 is on or "
        "after the scoring date and fewer than 90 days after it.",
        "Authority criterion: met when the primary contact's exact title is one of: Chief Zorbing Officer; Zorb "
        "Director.",
        "Levels by the number of criteria met (budget, authority, need, timeline): 0 is Cold zorb; 1 or 2 is Warm "
        "zorb; 3 or 4 is Hot zorb.",
        "Disqualifiers: the company is a current customer; the company has fewer than 25 employees (company size as "
        "in rule 4). A disqualified lead is Cold zorb whatever criteria it meets.",
        "Sales-ready: leads at Hot zorb or above are sales-ready and go to the sales team."]
BANT = [f"{i}. {r}" for i, r in enumerate(BANT, 1)]


def bant(msgs, lead=None, date="2026-04-30"):
    return score_of(render_text(TITLE, BANT, date, lead or base_lead(), base_form(), (), msgs, ()))


def test_bant_counts_window_and_disqualifier():
    msgs = [("2026-03-31T09:00:00Z", "Ada Quibble", "We have requested a budget of $4,200 per month for this."),
            ("2026-04-10T09:00:00Z", "Ada Quibble", "Our main problem is lost zorb parts."),
            ("2026-04-12T09:00:00Z", "Ada Quibble", "Our target date for going live is 2026-07-29.")]  # +90: not < 90
    r = bant(msgs)
    assert r.parts == {"budget": True, "authority": True, "need": True, "timeline": False}
    assert (r.score_text, r.level, r.ready) == ("3 of 4 criteria met", "Hot zorb", True)
    old = [("2026-03-30T09:00:00Z", *msgs[0][1:])] + msgs[1:]                     # budget 31 days old: outside
    assert bant(old).level == "Warm zorb"
    small = bant(msgs, lead=base_lead(**{"Enrichment lookup": "24 employees"}))
    assert (small.score_text, small.level) == ("3 of 4 criteria met", "Cold zorb")
    other = [("2026-04-10T09:00:00Z", "Ada Quibble", "Our main problem is zorb parking.")]         # not a listed need
    assert bant(other).parts["need"] is False


# ------------------------------------------------------------------------------------------------ gated
GATED = [SCOPE, EVID.format(exc=""), SIZE_FORM, ACT.format(limit=""), window(14, False),
         "Activity cap: activity points count up to 15 points in total.",
         "Budget terms: a counting budget means that the most recent budget statement that is evidence under rule 2 "
         "has a counting status and an amount of at least $1,000 per month. Counting statuses: approved. " + STATUS,
         "Seniority bands (exact title): band A: Chief Zorbing Officer; band B: Zorb Director; band C: Zorb Analyst; "
         "band D: Assistant to the Zorb Director.",
         "Levels: gates are checked in order. A lead's level is the highest level whose gate it passes together with "
         "every earlier gate; a lead that fails gate 1 is Tier 0 zorb.",
         "Gate 1 (Tier 1 zorb): company size (rule 3) of at least 100 employees.",
         "Gate 2 (Tier 2 zorb): the primary contact is in seniority band A or B (rule 8).",
         "Gate 3 (Tier 3 zorb): at least 12 activity points under rules 4, 5 and 6.",
         "Gate 4 (Tier 4 zorb): a counting budget under rule 7.",
         "Disqualifiers: the company's region is not a served region (served regions: Northeast, Midwest). A "
         "disqualified lead is Tier 0 zorb whatever gates it passes.",
         "Sales-ready: leads at Tier 3 zorb or above are sales-ready and go to the sales team.",
         "Amendment 1, effective 2026-04-01, applies to leads scored on or after that date: in rule 12, the minimum "
         "for gate 3 changes from 12 to 9 activity points."]
GATED = [f"{i}. {r}" for i, r in enumerate(GATED, 1)]
G_FORM = base_form(**{"Company size range": "100 to 499 employees"})
G_MSG = [("2026-03-02T09:00:00Z", "Ada Quibble", "We have an approved budget of $1,000 per month for this.")]


def gated(title, act, date="2026-03-31", crm=None):
    return render_text(TITLE, GATED, date, base_lead(**{"Primary contact title": title}), G_FORM, act, G_MSG, (),
                       crm=crm)


def test_gated_levels_and_gate_counts():
    act = [("2026-03-20T09:00:00Z", L, "demo request"), ("2026-03-30T09:00:00Z", L, "pricing page visit")]
    r = score_of(gated("Zorb Analyst", act))                         # gates: size ok, band C no, 13 >= 12, budget ok
    assert r.parts["gates"] == [True, False, True, True]
    assert (r.level, r.score_text) == ("Tier 1 zorb", "3 of 4 gates passed")
    doc = v3.parse_state(gated("Zorb Analyst", act))
    R = v3.parse_rubric(doc.title, doc.rules, doc.scoring_date)
    assert v3.evaluate(doc, R, {"gate_score": "consecutive"}).score_text == "1 of 4 gates passed"
    r2 = score_of(gated("Zorb Director", act))
    assert (r2.level, r2.ready) == ("Tier 4 zorb", True)


def test_gated_amendment_and_window():
    act = [("2026-03-17T09:00:00Z", L, "pricing page visit"),                     # 14+ days old on both dates
           ("2026-03-25T09:00:00Z", L, "pricing page visit"),
           ("2026-03-26T09:00:00Z", L, "webinar 'Zorb basics': attended")]        # 3 + 6 = 9 on 2026-04-01
    before = score_of(gated("Zorb Director", act, date="2026-03-31"))            # min 12: gate 3 fails
    after = score_of(gated("Zorb Director", act, date="2026-04-01"))             # amendment in force: min 9
    assert before.parts["gates"][2] is False and after.parts["gates"][2] is True


def test_gated_judge_question():
    act = [("2026-03-20T09:00:00Z", L, "demo request"), ("2026-03-30T09:00:00Z", L, "pricing page visit")]
    for rec, want_ind, want_con in (("3 of 4 gates passed", "yes", "no"), ("1 of 4 gates passed", "no", "yes")):
        crm = {"Owner": "Rex Pellow", "Stage": "new", "Recorded score": rec, "Recorded level": "Tier 1 zorb",
               "Score reason": "gate 1 passed, gate 2 failed, gate 3 passed, gate 4 passed"}
        q = f"The recorded score is {rec} (Tier 1 zorb), with the reason given. Is that score consistent with the rubric?"
        r = row(gated("Zorb Analyst", act, crm=crm), q, ["yes", "no"])
        assert v3.decide2_row(r) == want_ind
        assert v3.decide2_row(r, {"gate_score": "consecutive"}) == want_con
    crm = {"Owner": "Rex Pellow", "Stage": "new", "Recorded score": "2 of 4 gates passed",
           "Recorded level": "Tier 1 zorb"}
    q = "The recorded score is 3 of 4 gates passed (Tier 1 zorb), with the reason given. Is that score consistent " \
        "with the rubric?"
    with pytest.raises(v3.ParseError):                                           # question and CRM disagree
        v3.decide2_row(row(gated("Zorb Analyst", act, crm=crm), q, ["yes", "no"]))


# ------------------------------------------------------------------------------------------------ weighted
W_STATUS = ("Reading budget statements: 'approved budget' = approved; 'requested a budget' = requested; 'hope to get "
            "a budget' = hoped; 'if we had a budget' = hypothetical. Monthly and yearly amounts convert at 12 months "
            "per year.")
WEIGHTED = [
    "Who is scored: only the primary contact shown in the lead record. Colleagues at the same company are not "
    "scored, and any activity filed under a different lead id is ignored.",
    "Admissible evidence: the primary contact's own statements, that is, the web form they filled in and the emails "
    "or chat messages they wrote. Notes written by reps, and anything the contact attributes to someone else, are "
    "not admissible. Where the contact said the same kind of thing more than once, use only the latest admissible "
    "statement.",
    "Headcount: take the enrichment lookup's employee figure; the web-form employee range is not used.",
    "Engagement activities and their points: demo request 10; webinar 5. Anything else earns nothing. Webinars and "
    "trade show meetings earn points only when attended; signing up alone earns nothing. Repeats of one activity "
    "type on one calendar day count a single time.",
    "Recency: an activity counts only if it happened at most 30 days before the scoring date (exactly 30 days before "
    "still counts). Age is the scoring date minus the activity date, in UTC.",
    "Fit score (headcount as in rule 3): fewer than 100 employees 0; 100 to 999 employees 1; 1,000 employees or "
    "more 2.",
    "Role score (the primary contact's exact title): Chief Zorbing Officer 3; Zorb Director 2; Zorb Analyst 1; "
    "Assistant to the Zorb Director 0.",
    "Engagement score (activity points under rules 4 and 5): 0 to 4 points 0; 5 to 9 points 1; 10 points or more 2.",
    "Budget score (the latest admissible budget statement, see rule 2): 3 if it is approved with at least $24,000 "
    "per year; 2 if it is requested with at least $24,000 per year; 1 if it is approved or requested with a smaller "
    "amount; 0 otherwise. " + W_STATUS,
    "Timeline score (the latest admissible target date, see rule 2): 3 if it is at most 30 days after the scoring "
    "date; 2 if at most 60 days; 1 if at most 90 days; 0 if it is later, before the scoring date, or missing.",
    "Weighted total: 2 x fit + 2 x role + 1 x engagement + 2 x budget + 1 x timeline.",
    "Levels by weighted total: 0 to 5 is Low zorb; 6 to 11 is Mid zorb; 12 or more is Top zorb.",
    "Tie-break: when the weighted total equals the lowest total of a level exactly, the lead gets that level only if "
    "its budget score is 2 or 3; otherwise it gets the level below.",
    "Automatic Low zorb rating: the company already buys from us. Any one of these makes the lead Low zorb, whatever "
    "its weighted total.",
    "Handoff: a lead rated Top zorb or higher counts as sales-ready and is passed to sales."]
WEIGHTED = [f"{i}. {r}" for i, r in enumerate(WEIGHTED, 1)]
W_TITLE = "Qualification scorecard LQ-8 (revision 2), in force from 2025-01-01"


def weighted(size, budget_msg):
    msgs = [("2026-03-02T09:00:00Z", "Ada Quibble", budget_msg),
            ("2026-03-03T09:00:00Z", "Ada Quibble", "Our target date for going live is 2026-05-15.")]   # +45 -> 2
    lead = base_lead(**{"Enrichment lookup": size})
    return score_of(render_text(W_TITLE, WEIGHTED, D, lead, base_form(), [("2026-03-20T09:00:00Z", L, "demo request")],
                                msgs, ()))


def test_weighted_total_and_tie_break():
    r = weighted("150 employees", "We have an approved budget of $1,500 per month for this.")   # 18,000: small
    assert r.parts == {"fit": 1, "role": 2, "engagement": 2, "budget": 1, "timeline": 2}
    assert r.score == 12 and r.level == "Mid zorb"                  # 12 = lowest total of Top, budget score 1
    r2 = weighted("50 employees", "We have requested a budget of $2,000 per month for this.")   # 24,000 requested
    assert r2.score == 12 and r2.level == "Top zorb" and r2.ready   # tie, budget score 2 keeps the level
    r3 = weighted("150 employees", "We have an approved budget of $2,000 per month for this.")
    assert r3.score == 16 and r3.level == "Top zorb"


# ------------------------------------------------------------------------------------------------ questions
def test_question_kinds_and_jb_options():
    state = render_text(TITLE, points_rules(), D, base_lead(**{"Primary contact title": "Chief Zorbing Officer"}),
                        base_form(), [("2026-03-20T09:00:00Z", L, "demo request")], (), ())
    levels = ["Pale lead", "Mild lead", "Keen lead"]
    assert v3.decide2_row(row(state, "Which rubric level fits this lead as of the scoring date?", levels)) == "Keen lead"
    assert v3.decide2_row(row(state, "Is this lead sales-ready under the rubric?", ["yes", "no"])) == "yes"
    jb = ["Keep the lead out of the sales queue for now.", "Hand the lead to the sales team now."]
    assert v3.decide2_row(row(state, "Does this lead meet the rubric's bar for going to the sales team?", jb)) == jb[1]
    with pytest.raises(v3.ParseError):   # score options must be the rubric's levels in order
        v3.decide2_row(row(state, "Which rubric level fits this lead as of the scoring date?", levels[::-1]))
    with pytest.raises(v3.ParseError):
        v3.decide2_row(row(state, "How warm is this lead?", levels))

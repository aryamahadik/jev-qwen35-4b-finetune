"""Test helpers for golden_src/gen3/v3_lead_score.py (F5 decide2, builder D).

Builds small hand-made leads (invented names, reserved TLDs) and renders them in three of the surfaces decide2 reads
(plain text lists, json, prose), so scorer cases can be computed by hand. Nothing here comes from the generator.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

GEN3 = Path(__file__).resolve().parents[2] / "golden_src" / "gen3"
if str(GEN3) not in sys.path:
    sys.path.insert(0, str(GEN3))

import v3_lead_score as v3  # noqa: E402

SCOPE = ("Scope: score only the primary contact named in the lead record. Other people at the company are not "
         "scored, and activity logged under any other lead id does not count.")
EVID = ("Evidence: only the primary contact's own words are evidence, meaning the web form they submitted and the "
        "emails or chat messages they wrote themselves. Rep notes, and anything the contact reports another person "
        "as saying, are not evidence{exc}. When several evidence statements of the same kind exist, only the most "
        "recent one is used.")
STATUS = ("Status words: 'approved budget' means approved; 'requested a budget' means requested; 'hope to get a "
          "budget' means hoped; 'if we had a budget' means hypothetical. A monthly amount equals 12 times that "
          "amount per year.")
SIZE_FORM = "Company size: use the lower end of the employee range picked on the web form; ignore the enrichment lookup."
SIZE_ENR = ("Company size: use the employee count from the enrichment lookup; ignore the employee range picked on the "
            "web form.")
ACT = ("Activity points: demo request 10 points; webinar 6 points; guide download 2 points; pricing page visit 3 "
       "points. Other activity types score 0 points. A webinar or trade show meeting scores only if attended; a "
       "registration alone scores 0 points. The same activity type on the same day counts once.{limit}")
WIN = ("Activity window: only activity {w} {n} days old on the scoring date counts; activity exactly {n} days old "
       "{c}. Age is the scoring date minus the activity's date (UTC).")


def window(n=30, inclusive=True):
    return WIN.format(w="at most" if inclusive else "less than", n=n,
                      c="counts" if inclusive else "does not count")


def points_rules(*, size=SIZE_ENR, cap=20, unsub=None, budget_min="$60,000 per year", statuses="approved",
                 budget_pts=10, tl_days=60, tl_inclusive=True, levels=None, override=None, disq=None,
                 act_limit=None, rep_target=False, win=(30, True), amendments=()):
    """A points rubric. Rule numbers are fixed by position; references use those numbers."""
    rules = [SCOPE, EVID.format(exc=", except that a rep note giving the prospect's target date is evidence for "
                                    "rule 9" if rep_target else ""), size,
             "Title points (the primary contact's exact title): Chief Zorbing Officer 20 points; Zorb Director 10 "
             "points; Assistant to the Zorb Director 0 points; Zorb Analyst 4 points.",
             "Size points (company size as in rule 3): fewer than 50 employees 0 points; 50 to 499 employees 5 points; "
             "500 employees or more 10 points.",
             ACT.format(limit=f" Each activity type counts at most {act_limit} time{'s' if act_limit != 1 else ''} "
                              f"in total." if act_limit else ""),
             window(*win),
             f"Activity cap: activity points count up to {cap} points in total.",
             f"Timeline: add 5 points when the most recent target date that is evidence under rule 2 is on or after "
             f"the scoring date and {'at most' if tl_inclusive else 'fewer than'} {tl_days} days after it.",
             f"Budget: add {budget_pts} points when the most recent budget statement that is evidence under rule 2 has "
             f"a counting status and an amount of at least {budget_min}. Counting statuses: {statuses}. {STATUS}"]
    if unsub:
        rules.append(f"Unsubscribes: each unsubscribe from marketing email inside the activity window subtracts "
                     f"{unsub} points (the same day counts once). The total never goes below 0.")
    levels = levels or "0 to 14 points is Pale lead; 15 to 29 points is Mild lead; 30 points or more is Keen lead"
    rules.append(f"Levels by total points: {levels}.")
    if override == "ceiling":
        rules.append("Override, applied after the level is set: a lead without a counting budget under rule 10 is at "
                     "most Mild lead, so a higher level becomes Mild lead.")
    elif override == "floor":
        rules.append("Override, applied after the level is set: a lead with a demo request that counts under rules 6 "
                     "and 7 is at least Mild lead, so a lower level becomes Mild lead.")
    if disq:
        rules.append(f"Disqualifiers: {disq}. A disqualified lead is Pale lead whatever its points"
                     f"{' and any override' if override else ''}.")
    rules.append("Sales-ready: leads at Keen lead or above are sales-ready and go to the sales team.")
    rules += list(amendments)
    return [f"{i}. {r}" for i, r in enumerate(rules, 1)]


def base_lead(**kw):
    lead = {"Lead id": "L1000001", "Company": "Quorbel Works", "Company domain": "quorbel.test", "Region": "Northeast",
            "Current customer": "no", "Primary contact": "Ada Quibble", "Primary contact title": "Zorb Director",
            "Primary contact email": "ada.quibble@quorbel.test", "Enrichment lookup": "120 employees",
            "Lead created": "2026-01-02"}
    lead.update(kw)
    return lead


def base_form(**kw):
    form = {"Submitted by": "Ada Quibble", "Submitted at": "2026-03-01T10:00:00Z",
            "Company size range": "11 to 50 employees"}
    form.update(kw)
    return form


def render_text(title, rules, date, lead, form, activity=(), messages=(), notes=(), crm=None):
    """The plain text surface: 'Section:' headers, 'Key: Value' fields, '- T | L | act' and '- T | Name: text'."""
    crm = crm or {"Owner": "Rex Pellow", "Stage": "new"}
    out = [title] + list(rules) + ["", f"Scoring date: {date}", "", "Lead record:"]
    out += [f"{k}: {v}" for k, v in lead.items()]
    out += ["", "Web form:"] + [f"{k}: {v}" for k, v in form.items()]
    out += ["", "Activity:"] + [f"- {t} | {lid} | {a}" for t, lid, a in activity]
    out += ["", "Messages:"] + [f"- {t} | {who}: {txt}" for t, who, txt in messages]
    out += ["", "Rep notes:"] + [f"- {t} | {who}: {txt}" for t, who, txt in notes]
    out += ["", "CRM record:"] + [f"{k}: {v}" for k, v in crm.items()]
    return "\n".join(out)


def render_json(title, rules, date, lead, form, activity=(), messages=(), notes=(), crm=None):
    crm = crm or {"Owner": "Rex Pellow", "Stage": "new"}
    d = {"scoring_date": date, "rubric": {"title": title, "rules": list(rules)}, "lead": lead, "web_form": form,
         "activity": [{"time": t, "lead": lid, "activity": a} for t, lid, a in activity],
         "messages": [{"time": t, "from": who, "text": txt} for t, who, txt in messages],
         "rep_notes": [{"time": t, "rep": who, "note": txt} for t, who, txt in notes], "crm": crm}
    return json.dumps(d, indent=1, ensure_ascii=False)


TITLE = "Lead scoring rubric LQ-7 (version 1), effective 2025-01-01"


def row(state, instructions, options, gold=None):
    return {"rid": "t", "state": state, "instructions": instructions, "options": options, "gold": gold,
            "meta": {"qkind": "score", "view": "base", "fmt": "text", "split": "train"}}


def score_of(state):
    doc = v3.parse_state(state)
    R = v3.parse_rubric(doc.title, doc.rules, doc.scoring_date)
    return v3.evaluate(doc, R)

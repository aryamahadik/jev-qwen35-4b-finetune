"""Test helpers for golden_src/gen3/v3_rule_chain.py (F1 decide2, builder E).

Builds small hand-made rule documents and case files (invented names; the leave-handbook vocabulary from rc_skins) in
the rendered forms that F1_RULE_CHAIN_FORMAT.md describes, so outcomes can be computed by hand. Nothing here comes
from the generator or its renderers.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

GEN3 = Path(__file__).resolve().parents[2] / "golden_src" / "gen3"
if str(GEN3) not in sys.path:
    sys.path.insert(0, str(GEN3))

import v3_rule_chain as v3  # noqa: E402

GENERAL_CAL = ("Periods in this handbook are counted in calendar days: the date a stated number of days after or "
               "before a given date is found by counting that many calendar days forward or back from it.")
GENERAL_BUS = ("Periods in this handbook are counted in business days, which are Monday to Friday except the public "
               "holidays listed in section 6.7: the date a stated number of business days after or before a given "
               "date is found by counting that many business days forward or back from it.")
GENERAL = [
    "An exception applies only to the clause it names, and only when every condition it states is met; an exception "
    "does not apply where another clause says that it does not apply.",
    "An amendment replaces the figure it names for leave requests received on or after the date it comes into force; "
    "leave requests received earlier keep the earlier figure, and a withdrawn amendment has no effect.",
    "If more than one ground for refusal applies to a leave request, the ground stated first in this handbook is the "
    "one recorded.",
    "A fact that the case file does not show is treated as not established, and a document that the case file does "
    "not show as included is treated as not included.",
]
PREC = {
    "category": "Where the general limit and a category limit both apply to a leave request, the category limit "
                "prevails.",
    "later": "Where two limits both apply to a leave request, the one that appears later in this handbook prevails.",
    "lower": "Where two limits both apply to a leave request, the lower of the two applies.",
}


def handbook(elig="Paid special leave may be granted only if the employee's continuous service is at least 6 months.",
             time="The leave request must be received at least 10 days before the first day of the leave.",
             docs="The leave request must include a signed leave form.",
             exclusions=("No paid special leave is granted if the leave falls in the annual shutdown.",),
             glimit="Paid special leave may not be more than 8 days for one leave request.",
             catlim="The category limits are: apprentices, 5 days; part-time employees, 10 days.",
             exceptions=(), amendments=(), other=(), prec="category", business=False, holidays=(),
             title="TESTCO STAFF HANDBOOK - CHAPTER 6: PAID SPECIAL LEAVE",
             issuer="Issued by Testco Ltd. Version in force from 1 January 2026."):
    """A code-style leave handbook. Fixed numbers: 1.2 eligibility, 1.3 time, 1.4 documents, 2.k exclusions,
    3.1 general limit, 3.2 category limits, 4.k exceptions, 5.k amendments, 6.k General (6.7 holidays)."""
    out = [title, issuer, "", "Part 1 - Who may apply and what is required",
           "1.1 Employees may make a leave request under this handbook for a short absence; the paid special leave is "
           "granted only as this handbook allows."]
    for i, t in enumerate([x for x in (elig, time, docs) if x], 2):
        out.append(f"1.{i} {t}")
    for i, t in enumerate(other, 5):
        out.append(f"1.{i} {t}")
    out += ["", "Part 2 - Exclusions"] + [f"2.{i} {t}" for i, t in enumerate(exclusions, 1)]
    out += ["", "Part 3 - Limits and amounts"]
    lim = [x for x in (glimit, catlim) if x is not None]
    if glimit is None:
        lim = ["Former provision, repealed with effect from 1 January 2025 and no longer in force: \"Paid special "
               "leave may not be more than 2 days for one leave request.\""] + lim
    out += [f"3.{i} {t}" for i, t in enumerate(lim, 1)]
    out.append(f"3.{len(lim) + 1} Paid special leave covers the number of leave days requested, but not more than "
               "the limit that applies under this handbook; if the number of leave days requested is more than that "
               "limit, the paid special leave is cut to that limit.")
    if exceptions:
        out += ["", "Part 4 - Exceptions"] + [f"4.{i} {t}" for i, t in enumerate(exceptions, 1)]
    if amendments:
        out += ["", "Part 5 - Amendments"] + [f"5.{i} {t}" for i, t in enumerate(amendments, 1)]
    gen = [GENERAL_BUS if business else GENERAL_CAL] + GENERAL + ([PREC[prec]] if prec else [])
    if business:
        gen.append("The public holidays for this handbook are " + " and ".join(holidays) + ".")
    out += ["", "Part 6 - General"] + [f"6.{i} {t}" for i, t in enumerate(gen, 1)]
    return "\n".join(out)


CASE = {"Reference": "R1234567", "Employee": "Pella Testwick", "Category": "apprentice",
        "Request type": "short absence", "Continuous service": "8 months", "First day of leave": "2026-06-15",
        "Received": "2026-06-01", "Signed leave form": "included", "Admitted to hospital": "no",
        "Close family bereavement": "no", "Supported by a staff representative": "no", "In probation period": "no",
        "Falls in annual shutdown": "no", "Other paid leave on the same dates": "no", "Leave days requested": "4 days"}


def case_fields(**kw):
    f = dict(CASE)
    for k, val in kw.items():
        lab = {"cat": "Category", "service": "Continuous service", "first": "First day of leave",
               "received": "Received", "form": "Signed leave form", "hospital": "Admitted to hospital",
               "bereave": "Close family bereavement", "rep": "Supported by a staff representative",
               "probation": "In probation period", "shutdown": "Falls in annual shutdown",
               "double": "Other paid leave on the same dates", "days": "Leave days requested",
               "decision": "Decision recorded"}[k]
        if val is None:
            f.pop(lab, None)
        else:
            f[lab] = val
    return f


def kv_state(doc: str, fields: dict, note: str | None = None) -> str:
    s = doc + "\n\nCase file\n" + "\n".join(f"case.{k}: {x}" for k, x in fields.items())
    if note:
        s += "\n\nNote attached to the file by Vara Testholm (neighbour): " + note
    return s


def json_state(doc: str, fields: dict, notes=()) -> str:
    return json.dumps({"document": doc.split("\n"), "case": fields,
                       "correspondence": [{"from": "Tam Testard (adviser)", "text": n} for n in notes]}, indent=1)


def outcome(state: str, deleted=frozenset(), readings=None) -> v3.Result:
    sp, doc, case = v3.parse_f1a(state)
    return v3.evaluate(doc, case, frozenset(deleted), readings)


def row(state: str, instructions: str, options=("yes", "no"), defs=None) -> dict:
    return {"rid": "t-0", "state": state, "instructions": instructions, "options": list(options), "gold": None,
            "meta": {"defs": defs}}


OUT = v3.vocab("leave_handbook").outcomes

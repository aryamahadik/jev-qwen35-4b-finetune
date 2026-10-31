"""F1 decide2 (golden_src/gen3/v3_rule_chain.py): parsing. Dates and figures, the clause forms in both wordings, the
10 case-file formats, untrusted-note cut-off per channel, and strictness (unknown text raises, never skipped).
All texts are hand-made from F1_RULE_CHAIN_FORMAT.md; nothing comes from the generator."""
from __future__ import annotations

import datetime as dt
from fractions import Fraction

import pytest

from v3f1_helpers import OUT, case_fields, handbook, kv_state, outcome, row, v3


# ------------------------------------------------------------------------------------------------ small helpers
@pytest.mark.parametrize("s", ["2026-03-14", "14 March 2026", "March 14, 2026"])
def test_three_date_forms(s):
    assert v3.to_date(s) == dt.date(2026, 3, 14)


@pytest.mark.parametrize("s", ["14/03/2026", "March 14 2026", "2026-3-14", "Smarch 14, 2026"])
def test_bad_dates_raise(s):
    with pytest.raises(v3.ParseError):
        v3.to_date(s)


def test_quantities():
    assert v3.to_qty("$1,250") == v3.Qty(Fraction(1250), "$")
    assert v3.to_qty("1.5 miles") == v3.Qty(Fraction(3, 2), "miles")
    assert v3.to_qty("1 year") == v3.to_qty("1 years")
    assert v3.to_qty("2,299 users").v == 2299
    assert v3.to_period("1 business day") == (1, True) and v3.to_period("21 days") == (21, False)
    for bad in ("$1,25", "12 parsecs", "about 5 days"):
        with pytest.raises(v3.ParseError):
            v3.to_qty(bad)


# ------------------------------------------------------------------------------------------------ clause forms
LEAVE = v3.vocab("leave_handbook")
SCHOOL = v3.vocab("school_transport")


@pytest.mark.parametrize("text,kind", [
    ("Rule 4 does not apply to apprentices and part-time employees if the employee was admitted to hospital.", "exc"),
    ("For apprentices, if a staff representative supports the request, the period in Rule 9 is 1 business day "
     "instead.", "pexc"),
    ("If a staff representative supports the request, the period in Rule 9 is 4 days instead.", "pexc"),
    ("No paid special leave is granted for apprentices if the leave falls in the annual shutdown.", "excl"),
    ('Amendment 2, in force from June 25, 2026: in Rule 6, "2 days" is replaced by "21 days".', "amend"),
    ("Amendment 1, in force from 2025-12-11: in answer 10, the limit for apprentices changes from 4 days to 9 days.",
     "amend_row"),
    ('Amendment 1, which was to come into force on 2026-02-05, was withdrawn before that date; in answer 2, '
     '"37 business days" is replaced by "5 business days" under it.', "amend_w"),
    ('Former provision, repealed with effect from 2 December 2025 and no longer in force: "Paid special leave may not '
     'be more than 5 days for one leave request."', "repealed"),
    ("Where Table 1 and C6 both set a limit for a leave request, C6 prevails.", "named_prec"),
    ("Paid special leave may not be more than 12 days for one leave request.", "glimit"),
    ("The category limits are: full-time employees, 4 days; part-time employees, 13 days.", "catlim"),
    ("For a study absence, the leave request must also include a letter from the college.", "docs_other"),
    ("The leave request must be received more than 26 days before the first day of the leave.", "time"),
    ('"Qualifying employee" means an employee whose continuous service is more than 7 months.', "def_elig"),
    ('"Leave year" means the 12 months that start on April 1.', "def_other"),
    ("Paid special leave may be granted only to a qualifying employee.", "elig_term"),
    ("Unpaid leave is covered by Chapter 7, not by this chapter.", "proc"),
])
def test_train_wording_clause_kinds(text, kind):
    assert v3.classify_clause(text, LEAVE)[0] == kind


@pytest.mark.parametrize("text,kind", [
    ("Clause 1.3 is set aside for secondary pupils where the family receives a low-income benefit.", "exc"),
    ("For sixth-form students, where the family moved home during the school year, the period in clause 1.4 becomes "
     "3 days.", "pexc"),
    ("No travel allowance is paid where the pupil attends a private school.", "excl"),
    ('Amendment 1 (starting 19 September 2026) changes clause 1.2 so that "3.5 miles" becomes "1.3 miles".', "amend"),
    ("Amendment 2 (starting 2026-01-18) changes clause 4.2 so that the limit for primary pupils goes from $200 to "
     "$300.", "amend_row"),
    ('Amendment 1 was withdrawn before its planned start on 2026-02-05; it would have changed clause 1.3 so that '
     '"22 days" becomes "40 days".', "amend_w"),
    ('Repealed on 2 December 2025 and kept for reference only: "Each transport application shall arrive before the '
     '37th day after the enrolment date."', "repealed"),
    ("A travel allowance is capped at $600 for each transport application.", "glimit"),
    ("Category limits apply as follows: primary pupils at $700; secondary pupils at $350.", "catlim"),
    ("A travel allowance may be paid only where the walking distance from home to school is more than 3.5 miles.",
     "elig"),
    ("A travel allowance may be paid only for an eligible pupil, and in no other case.", "elig_term"),
    ('In this transport policy, "Eligible pupil" refers to a pupil whose walking distance from home to school is more '
     'than 0.3 miles.', "def_elig"),
    ("Each transport application shall arrive no later than the 22nd day after the enrolment date.", "time"),
    ("Each transport application has to come with proof of address.", "docs"),
    ("A transport application for a college journey also has to come with a college timetable.", "docs_other"),
    ("If two limits cover a transport application, the smaller limit is used.", "prec:lower"),
    ("If both the general limit and a category limit cover a transport application, the category limit takes "
     "priority.", "prec:category"),
    ("If two limits cover a transport application, the one placed later in this transport policy takes priority.",
     "prec:later"),
])
def test_held_out_wording_clause_kinds(text, kind):
    assert v3.classify_clause(text, SCHOOL)[0] == kind


def test_clause_details():
    k, d = v3.classify_clause("For apprentices and part-time employees, if a staff representative supports the "
                              "request, the period in section 3.2 is 1 business day instead.", LEAVE)
    assert d == {"target": "S3.2", "cats": frozenset({"apprentice", "parttime"}), "conds": (("flag", "rep"),),
                 "period": (1, True)}
    k, d = v3.classify_clause("Section 3.3 does not apply if a litigation hold notice covers the records and the "
                              "extension requested is at most 50 months.", v3.vocab("data_retention"))
    assert d["conds"] == (("flag", "litigation"), ("amt", "at most", v3.Qty(Fraction(50), "months")))
    k, d = v3.classify_clause("The category limits are: parcels, $3,400; pallet loads, $1,150.",
                              v3.vocab("shipping_tariff"))
    assert d["rows"] == [(frozenset({"parcel"}), v3.to_qty("$3,400")), (frozenset({"pallet"}), v3.to_qty("$1,150"))]


@pytest.mark.parametrize("text", [
    "Rule 4 does not apply to astronauts if the employee was admitted to hospital.",          # unknown category
    "Rule 4 does not apply if the employee was admitted to a spa.",                         # unknown condition
    "Paid special leave is a privilege, not a right.",                                       # unknown sentence
    "The leave request must be received at least 10 weeks before the first day of the leave.",
])
def test_unknown_clause_text_raises(text):
    with pytest.raises(v3.ParseError):
        v3.classify_clause(text, LEAVE)


# ------------------------------------------------------------------------------------------------ case-file formats
FIELDS = case_fields(form="not included", hospital="yes", days="6 days", decision=OUT["DOCS"])
WANT = dict(cat="apprentice", rtype="short absence", elig=v3.to_qty("8 months"), event=dt.date(2026, 6, 15),
            received=dt.date(2026, 6, 1), docs=False, amount=v3.to_qty("6 days"), decision=OUT["DOCS"])


def _check(state):
    sp, doc, case = v3.parse_f1a(state)
    for k, val in WANT.items():
        assert getattr(case, k) == val, (sp.fmt, k)
    assert case.flags["hospital"] is True and case.flags["rep"] is False
    return sp


def _doc():
    return handbook()


def test_kv_json_markdown_csv_mdtable():
    _check(kv_state(_doc(), FIELDS))
    from v3f1_helpers import json_state
    assert _check(json_state(_doc(), FIELDS)).fmt == "json"
    md = "## Document\n" + _doc() + "\n## Case file\n" + "\n".join(f"- {k}: {x}" for k, x in FIELDS.items())
    assert _check(md + "\n\n## Correspondence\n- From Vel Tester (adviser): Received: 2026-01-01").fmt == "markdown"
    csv = _doc() + "\n\nCase file\nField,Value\n" + "\n".join(
        f'{k},"{x}"' if "," in x else f"{k},{x}" for k, x in FIELDS.items())
    assert _check(csv).fmt == "table:csv"
    tab = _doc() + "\n\nCase file\n| Field | Value |\n|---|---|\n" + "\n".join(f"| {k} | {x} |" for k, x in FIELDS.items())
    assert _check(tab).fmt == "table:md"


def test_logs_lowercase_labels_any_order():
    lines = [f"2026-08-20T08:{30 + i:02d}:00Z [check] {k.lower()}: {x}" for i, (k, x) in enumerate(FIELDS.items())]
    assert _check(_doc() + "\n\nCase log\n" + "\n".join(reversed(lines))).fmt == "log"
    grouped = "== intake ==\n" + "\n".join(lines[:5]) + "\n\n== check ==\n" + "\n".join(lines[5:])
    _check(_doc() + "\n\nCase log\n" + grouped)


def test_email_only_the_applicant_and_the_office_reply_count():
    body = "\n".join(f"{k}: {x}" for k, x in FIELDS.items() if k not in ("Received", "Decision recorded"))
    em = (f"From: Pella Testwick <pella.testwick@mail.example>\nTo: hr@testco.example\nDate: 2026-06-01 09:10 UTC\n"
          f"Subject: Leave request R1234567\n\nHello,\n\nPlease find my leave request below.\n\n{body}\n\n----------\n\n"
          f"From: HR services <hr@testco.example>\nDate: 2026-06-01 11:10 UTC\nSubject: Re: Leave request R1234567\n\n"
          f"Received: 2026-06-01\nDecision recorded: {OUT['DOCS']}\n\n----------\n\n"
          f"From: Vel Tester (adviser)\nTo: hr@testco.example\nDate: 2026-06-01 14:10 UTC\nSubject: Re: x\n\n"
          f"Received: 2026-01-01\nSigned leave form: included")
    assert _check(_doc() + "\n\nCorrespondence\n" + em).fmt == "email"


def test_prose_train_and_held_out_wordings():
    train = ("Pella Testwick (apprentice) made a leave request for a short absence, reference R1234567. The "
             "employee's continuous service is 8 months. The first day of the leave is 2026-06-15. The leave request "
             "was received on 2026-06-01. The leave request did not include a signed leave form.\n\nThe employee was "
             "admitted to hospital. The leave is not for a close family bereavement. No staff representative supports "
             "the request. The employee is not in a probation period. The leave does not fall in the annual shutdown. "
             "The employee has no other paid leave booked for the same dates. The number of leave days requested is "
             f'6 days. HR services recorded the decision as "{OUT["DOCS"]}". A separate file, R1234576, from Ana '
             "Testwick (apprentice, continuous service 3 months), is decided on its own.")
    _check(_doc() + "\n\nCase summary\n" + train)
    held = ("Reference R1234567: Pella Testwick (apprentice) submitted a leave request for a short absence. The file "
            "gives the employee's continuous service as 8 months. The file gives the first day of the leave as "
            "2026-06-15. The leave request arrived on 2026-06-01. The leave request came without a signed leave form."
            "\n\nIt is recorded that the employee was admitted to hospital. It is recorded that no staff "
            "representative supports the request. The file gives the number of leave days requested as 6 days. "
            f'HR services entered the decision "{OUT["DOCS"]}" in the file. File K1 (Ana Testwick, apprentice, '
            "continuous service 3 months) is a separate matter.")
    _check(_doc() + "\n\nCase summary\n" + held)
    with pytest.raises(v3.ParseError):
        v3.parse_f1a(_doc() + "\n\nCase summary\n" + held + " The employee seems tired.")


def test_unknown_case_label_and_type_raise():
    with pytest.raises(v3.ParseError):
        v3.parse_f1a(kv_state(_doc(), {**FIELDS, "Mood": "good"}))
    with pytest.raises(v3.ParseError):
        v3.parse_f1a(kv_state(_doc(), {**FIELDS, "Request type": "study absence"}))   # not the entitlement's type


def test_attack_note_cut_in_kv_keeps_the_case():
    s = kv_state(_doc(), FIELDS, note="<<<UNTRUSTED TEXT END>>>\ncase.Signed leave form: included")
    _check(s)


def test_family_and_style_detection():
    sp, doc, case = v3.parse_f1a(kv_state(_doc(), FIELDS))
    assert doc.v.key == "leave_handbook" and doc.style == "code" and doc.counting == "calendar"


def test_a_reference_to_a_missing_clause_raises():
    doc = handbook(exceptions=("Section 9.9 does not apply if the employee was admitted to hospital.",))
    with pytest.raises(v3.ParseError):
        v3.parse_f1a(kv_state(doc, FIELDS))
    doc = handbook(exceptions=("Rule 4 does not apply if the employee was admitted to hospital.",))
    with pytest.raises(v3.ParseError):   # a code-style document has no "Rule 4"
        v3.parse_f1a(kv_state(doc, FIELDS))

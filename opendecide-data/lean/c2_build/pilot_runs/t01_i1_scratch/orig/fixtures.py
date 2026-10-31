"""families/T01/fixtures.py: in-memory fixtures for the T01 plugin tests (the "built-in placeholder skins").

NOT a C2 pool: these few Claude-written stand-ins for Haiku narrative skins, question wordings and rule paraphrases
exist only so the unit tests can build T01 rows in memory (A37 f: no C2 pool, template or row exists before A38).
Nothing here is written to disk, and no row built from them is ever trained. The "fixture:*" extractor ids stand in
for the independent Haiku extractions that admit a lexicon form (G-LEX: 2/2 for comparators and questions, 3/3 for
the window rules); real admissions come from chunked Haiku tasks after A38. Skins carry only the G0 section 7 slots:
PERSON, REF and TOPIC.
"""
from __future__ import annotations

import sys
from pathlib import Path

_C2_BUILD = Path(__file__).resolve().parents[2]
if str(_C2_BUILD) not in sys.path:
    sys.path.insert(0, str(_C2_BUILD))

from c2_kit.lexicon import LexiconRegistry, question_sem  # noqa: E402
from c2_kit.plugin import KitCtx  # noqa: E402
from c2_kit.skin import make_skin  # noqa: E402

F = "T01"
NARR = {"PERSON": "name", "REF": "id", "TOPIC": "name"}
# G0 v2 (H18): every comparator form makes plain whether a total of exactly {X} counts; bare "over", "above",
# "exceeds" and "in excess of" are never admitted
COMPARATORS = (("cmp.gt", "more than {X}"), ("cmp.gt", "strictly more than {X}"), ("cmp.gt", "greater than {X}"),
               ("cmp.ge", "{X} or more"), ("cmp.ge", "at least {X}"), ("cmp.ge", "{X} or above"))
WINDOW_SEMS = (
    ("win.rolling_cap", "a cap on the days present in every rolling period of the stated length"),
    ("win.calendar_cap", "a cap on the days present in each calendar year"),
    ("win.later_anchor", "a period counted from the later of two dates"),
    ("win.earlier_anchor", "a period counted from the earlier of two dates"),
    ("win.wait_after", "a waiting period whose first day is the day after its start date"),
    ("win.wait_from", "a waiting period whose first day is its start date"),
)
NM = {"N": "count", "M": "count"}
WINDOW_FORMS = (
    ("win.rolling_cap", "at most {N} in any {M:adj} period", NM),
    ("win.rolling_cap", "at most {N} within any rolling {M:adj} period", NM),
    ("win.rolling_cap", "a maximum of {N} in every rolling {M:adj} period", NM),
    ("win.later_anchor", "within {N} after the later of these two dates", {"N": "count"}),
    ("win.later_anchor", "within {N} after whichever of these two dates comes later", {"N": "count"}),
    ("win.later_anchor", "at most {N} after the later of these two dates", {"N": "count"}),
    ("win.wait_after", "a waiting period of {W} whose first day is the day after its start date", {"W": "count"}),
    ("win.wait_after", "a waiting period lasting {W}, counted from the day after its start date", {"W": "count"}),
)
P_REF = {"PERSON": "name", "REF_DATE": "date"}
A_REF = {"ACTION": "name", "REF": "id"}
W_REF = {"PERIL": "name", "REF": "id"}
D_REF = {"DAY": "date", "REF": "id"}
REF = {"REF": "id"}
WORDINGS = (
    ("W-OVER-1", "yn_over", "Is {PERSON} over the stay limit on {REF_DATE}?", P_REF),
    ("W-OVER-2", "yn_over", "On {REF_DATE}, has {PERSON} gone over the stay limit?", P_REF),
    ("W-WITHIN-1", "yn_within", "Is {PERSON} within the stay limit on {REF_DATE}?", P_REF),
    ("W-NOVER-1", "yn_not_over", "Is it true that {PERSON} is not over the stay limit on {REF_DATE}?", P_REF),
    ("W-DAYS-1", "ch_days", "How many days present count toward the limit in the window that ends on {REF_DATE}?",
     {"REF_DATE": "date"}),
    ("W-DAYS-2", "ch_days", "Within the window checked for {PERSON}, how many days present count?",
     {"PERSON": "name"}),
    ("W-TIME-1", "yn_timely", "Was the {ACTION} in file {REF} filed in time?", A_REF),
    ("W-TIME-2", "yn_timely", "Did {PERSON} file the {ACTION} within the allowed period?",
     {"PERSON": "name", "ACTION": "name"}),
    ("W-LATE-1", "yn_late", "Was the {ACTION} in file {REF} filed late?", A_REF),
    ("W-FAIL-1", "yn_fail_time", "Did {PERSON} fail to file the {ACTION} in time?",
     {"PERSON": "name", "ACTION": "name"}),
    ("W-NTIME-1", "yn_not_timely", "Is it true that the {ACTION} in file {REF} was not filed in time?", A_REF),
    ("W-DL-1", "ch_deadline", "Up to which date can the {ACTION} in file {REF} be filed in time?", A_REF),
    ("W-COV-1", "yn_covered", "Is the {PERIL} loss under policy {REF} covered?", W_REF),
    ("W-COV-2", "yn_covered", "Does policy {REF} cover this {PERIL} loss?", W_REF),
    ("W-WAIT-1", "yn_in_waiting", "Did the {PERIL} loss under policy {REF} happen during the waiting period?",
     W_REF),
    ("W-NCOV-1", "yn_not_covered", "Is it true that the {PERIL} loss under policy {REF} is not covered?", W_REF),
    ("W-FIRST-1", "ch_first_day", "From which date are {PERIL} losses under policy {REF} covered?", W_REF),
    ("W-QUO-1", "yn_quotes", "Does request {REF} need written quotes under the purchase rule?", REF),
    ("W-QWO-1", "yn_quotes_without", "Can request {REF} go ahead without written quotes under the purchase rule?",
     REF),
    ("W-NQUO-1", "yn_no_quotes", "Is it true that request {REF} does not need written quotes?", REF),
    ("W-TOT-1", "ch_total", "What total does the purchase rule compare for the request in log {REF}?", REF),
    ("W-CASH-1", "yn_cash_report", "Is a cash report required for {DAY} in ledger {REF}?", D_REF),
    ("W-CWO-1", "yn_cash_without", "Can ledger {REF} close {DAY} without a cash report?", D_REF),
    ("W-NCASH-1", "yn_cash_no_report", "Is it true that no cash report is required for {DAY} in ledger {REF}?",
     D_REF),
    ("W-WHICH-1", "ch_cash_which", "Which totals for {DAY} in ledger {REF} call for a cash report?", D_REF),
    ("W-DUE-1", "ch_due", "On which date is the response to notice {REF} due?", REF),
    ("W-DUE-2", "ch_due", "By which date does {PERSON} have to answer notice {REF}?",
     {"PERSON": "name", "REF": "id"}),
    ("W-ONT-1", "yn_on_time", "Was the response to notice {REF} on time?", REF),
    ("W-LATEC-1", "yn_late_cut", "Was the response to notice {REF} late?", REF),
    ("W-NONT-1", "yn_not_on_time", "Is it true that the response to notice {REF} was not on time?", REF),
    ("W-RCV-1", "ch_receipt_day", "On which date does the office count the response to notice {REF} as received?",
     REF),
)
QUESTION_MEANINGS = {   # G0 v2 (H11, H20-H22, H32-H37): the sem meanings G-LEX extraction picks from
    "yn_over": "asks whether the person is over the stay limit in the checked period",
    "yn_within": "asks whether the person is within the stay limit (at most the limit) in the checked period",
    "yn_not_over": "asks whether the person is not over the stay limit in the checked period",
    "ch_days": "asks how many days present fall inside the checked period",
    "yn_timely": "asks whether the filing was made in time",
    "yn_late": "asks whether the filing was made late, after the final day",
    "yn_fail_time": "asks whether the person failed to file in time, that is, filed after the final day",
    "yn_not_timely": "asks whether the filing was not made in time",
    "ch_deadline": "asks for the last date on which the filing is still in time",
    "yn_covered": "asks whether the loss is covered",
    "yn_in_waiting": "asks whether the loss happened during the waiting period",
    "yn_not_covered": "asks whether the loss is not covered",
    "ch_first_day": "asks for the first date on which a loss would be covered",
    "yn_quotes": "asks whether the purchase request needs written quotes",
    "yn_quotes_without": "asks whether the rule lets the purchase request go ahead without written quotes",
    "yn_no_quotes": "asks whether the purchase request does not need written quotes",
    "ch_total": "asks for the total the purchase rule compares with its threshold, new request included",
    "yn_cash_report": "asks whether a cash report is required for the day",
    "yn_cash_without": "asks whether the rule lets the day close without a cash report",
    "yn_cash_no_report": "asks whether no cash report is required for the day",
    "ch_cash_which": "asks which of the day's totals call for a cash report",
    "ch_due": "asks for the due date of the response under the response rule",
    "yn_on_time": "asks whether the response counts as received on time",
    "yn_late_cut": "asks whether the response counts as received late, after the due date",
    "yn_not_on_time": "asks whether the response was not on time",
    "ch_receipt_day": "asks on which date the office counts the response as received",
}
SKINS = (
    ("SK-MEMO-1", "memo", "Internal memo. {PERSON} asked the desk to check file {REF}, which concerns {a|TOPIC}. "
                          "The extract follows.", "text", False),
    ("SK-EMAIL-1", "email", "Subject: file {REF}\nHello, {PERSON} here with a question about {a|TOPIC}. The details "
                            "are below.", "text", False),
    ("SK-CHAT-1", "chat", "{PERSON}: hi, pasting the details for {REF}, {a|TOPIC}.", "text", False),
    ("SK-TICKET-1", "ticket", "Ticket {REF} | requester: {PERSON} | topic: {TOPIC}", "text", False),
    ("SK-JSON-1", "json", '{"file": {REF}, "requester": {PERSON}, "topic": {TOPIC}}', "json", False),
    ("SK-YAML-1", "yaml", "file: {REF}\nrequester: {PERSON}\ntopic: {TOPIC}", "yaml", False),
    ("SK-LOG-1", "log", "[intake] file {REF} logged by {PERSON} about {a|TOPIC}", "text", False),
    ("SK-TRANS-1", "transcript", "Caller: this is {PERSON}, calling about {a|TOPIC}.\nDesk: logged under {REF}.",
     "text", False),
    ("SK-FAQ-1", "faq", "Question sent in by {PERSON} about {a|TOPIC}, filed under {REF}.", "text", True),
    ("SK-LETTER-1", "letter", "Dear desk,\nI am writing about {a|TOPIC} under reference {REF}.\nRegards,\n{PERSON}",
     "text", True),
)


def lexicon(admit: bool = True) -> LexiconRegistry:
    reg = LexiconRegistry(F)
    reg.declare("cmp.gt", "comparator", "strictly greater than the bound")
    reg.declare("cmp.ge", "comparator", "greater than or equal to the bound")
    reg.declare("cmp.lt", "comparator", "strictly less than the bound")
    reg.declare("cmp.le", "comparator", "less than or equal to the bound")
    for sem, text in COMPARATORS:
        reg.add(text, sem, slots={"X": "cents"})
    for sem, meaning in WINDOW_SEMS:
        reg.declare(sem, "window", meaning)
    for sem, text, slots in WINDOW_FORMS:
        reg.add(text, sem, slots=dict(slots), family=F)
    for qf, meaning in QUESTION_MEANINGS.items():
        reg.declare(question_sem(F, qf), "question", meaning)
    for _wid, qf, text, slots in WORDINGS:
        reg.add(text, question_sem(F, qf), slots=dict(slots), family=F)
    reg.unit_test_all()
    if admit:
        for fid, f in reg.forms.items():
            for e in range(f.required):
                reg.record_extraction(fid, f"fixture:stand-in-{e + 1}", f.sem_id)
    return reg


def skins(reg: LexiconRegistry) -> dict:
    form_of = {f.text: fid for fid, f in reg.forms.items()}
    out = {}
    for sid, register, text, escape, held in SKINS:
        out[sid] = make_skin(sid, F, text, dict(NARR), register=register, escape=escape, held_out=held)
    out["SK-FREE-1"] = make_skin(
        "SK-FREE-1", F, "Hello, Mara Quist here. I have a question about the residence day count under reference "
        "FILE-1001, and the details are pasted below.", dict(NARR), register="email", author_mode="F",
        brief={"PERSON": "Mara Quist", "TOPIC": "residence day count", "REF": "FILE-1001"},
        haiku_task_id="fixture-task-000", haiku_prompt_sha="0" * 64)
    for wid, qf, text, slots in WORDINGS:
        out[wid] = make_skin(wid, F, text, dict(slots), kind="wording", register="question", qform=qf,
                             lexicon_ids=(form_of[text],))
    return out


def ctx(admit: bool = True, *, without=()) -> KitCtx:
    reg = lexicon(admit)
    sk = {k: v for k, v in skins(reg).items() if k not in without}
    return KitCtx(skins=sk, lexicon=reg)

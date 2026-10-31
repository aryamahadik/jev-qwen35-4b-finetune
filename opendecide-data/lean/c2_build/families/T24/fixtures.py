"""families/T24/fixtures.py: in-memory fixtures for the T24 plugin tests (A37 f: no C2 pool, template or row exists
before A38).

NOT a C2 pool. These few Claude-written stand-ins for the Haiku narrative skins, question wordings and clause
paraphrases exist only so the unit tests can build T24 rows in memory; nothing here is written to disk. The real pools
come from chunked Haiku tasks after A38 (G0_SPEC.md section 3): clause paraphrases are admitted by G-LEX extraction
(2/2; 3/3 for the time-limit kinds), which is the spec's "cosmetic rewording admitted only by AST equality"; skins pass
G13-seed and G-SL. The "fixture:*" extractor ids stand in for the independent Haiku extractions.
"""
from __future__ import annotations

from c2_kit.lexicon import LexiconRegistry, question_sem
from c2_kit.plugin import KitCtx
from c2_kit.skin import make_skin

F = "T24"
SEMS = (
    ("t24.win", "window", "a request is on time when made at most N days after the named date (that date is day zero)"),
    ("t24.amt.ge", "comparator", "the money field must be at least the bound"),
    ("t24.amt.gt", "comparator", "the money field must be strictly more than the bound"),
    ("t24.amt.le", "comparator", "the money field must be at most the bound"),
    ("t24.amt.lt", "comparator", "the money field must be strictly less than the bound"),
    ("t24.exc", "other", "cases in the named category are excluded"),
    ("t24.alt", "other", "cases with the named condition get the named outcome"),
    ("t24.ovc", "window", "cases in the named category have another time limit"),
    ("t24.ovd", "window",
     "cases whose named date lies in the date window, both ends included, have another time limit"),
)
SLOT_KINDS = {"t24.win": {"N": "count", "A": "category"}, "t24.exc": {"C": "category"},
              "t24.alt": {"K": "category", "O": "category"}, "t24.ovc": {"C": "category", "N": "count"},
              "t24.ovd": {"A": "category", "S": "date", "E": "date", "N": "count"}}
AMT_SLOTS = {"M": "category", "X": "cents"}
CLAUSES = (
    ("t24.win", "A request must be made within {N} of the {A}"),
    ("t24.win", "Requests are accepted up to {N} after the {A}"),
    ("t24.win", "The time limit is {N}, counted from the {A}"),
    ("t24.amt.ge", "The {M} must be at least {X}"),
    ("t24.amt.ge", "Cases whose {M} is below {X} do not qualify"),
    ("t24.amt.ge", "The {M} must be {X} or more"),
    ("t24.amt.gt", "The {M} must be more than {X}"),
    ("t24.amt.gt", "Cases whose {M} is {X} or less do not qualify"),
    ("t24.amt.gt", "The {M} must exceed {X}"),
    ("t24.amt.le", "The {M} must be at most {X}"),
    ("t24.amt.le", "Cases whose {M} is above {X} do not qualify"),
    ("t24.amt.le", "The {M} must be {X} or less"),
    ("t24.amt.lt", "The {M} must be less than {X}"),
    ("t24.amt.lt", "Cases whose {M} is {X} or more do not qualify"),
    ("t24.amt.lt", "The {M} must be below {X}"),
    ("t24.exc", "Cases in the {C} category are excluded"),
    ("t24.exc", "This policy does not cover the {C} category"),
    ("t24.exc", "The {C} category is outside this policy"),
    ("t24.alt", "For cases whose condition is {K}, the outcome is {O}"),
    ("t24.alt", "When the condition is {K}, the case gets {O}"),
    ("t24.alt", "Cases in {K} condition receive {O}"),
    ("t24.ovc", "For the {C} category, the time limit is {N} instead"),
    ("t24.ovc", "Cases in the {C} category have a time limit of {N} instead"),
    ("t24.ovc", "The time limit for the {C} category is {N} instead"),
    ("t24.ovd", "For cases whose {A} falls from {S} to {E}, both dates included, the time limit is {N} instead"),
    ("t24.ovd", "When the {A} is between {S} and {E}, inclusive, the time limit is {N} instead"),
    ("t24.ovd", "The time limit is {N} instead for cases whose {A} is from {S} through {E}"),
)
NARR = {"CUSTOMER": "name", "CASE_ID": "id"}
# (skin id, register, escape, held out, text, declared slots). No blank line in a skin (blocks are blank-separated).
SKINS = (
    ("SK-MEMO-1", "memo", "text", False,
     "Case note: {CUSTOMER} raised case {CASE_ID} with the help desk and asked for a decision under the policy.", NARR),
    ("SK-EMAIL-1", "email", "text", False,
     "Hello,\nI am writing about case {CASE_ID}. Please look at my request under your policy.\nKind regards,\n"
     "{CUSTOMER}", NARR),
    ("SK-CHAT-1", "chat", "text", False,
     "{CUSTOMER}: hi, this is about case {CASE_ID}. where do I stand with my request?", NARR),
    ("SK-TICKET-1", "ticket", "text", False,
     "Ticket {CASE_ID}\nRequester: {CUSTOMER}\nTopic: request under the policy", NARR),
    ("SK-JSON-1", "json", "json", False,
     '{"ticket": {CASE_ID}, "customer": {CUSTOMER}, "topic": "request under the policy"}', NARR),
    ("SK-YAML-1", "yaml", "yaml", False,
     "ticket: {CASE_ID}\ncustomer: {CUSTOMER}\ntopic: request under the policy", NARR),
    ("SK-LETTER-1", "letter", "text", False,
     "Dear support team,\nmy name is {CUSTOMER} and I write about case {CASE_ID}. Please give me a decision under"
     " the policy.\nThank you.", NARR),
    ("SK-LOG-1", "log", "text", False,
     "[support inbox] message from {CUSTOMER} about case {CASE_ID}: asks for a decision under the policy", NARR),
    ("SK-FORM-1", "form", "text", False,
     "Request form\nSubmitted by: {CUSTOMER}\nCase number: {CASE_ID}\nCategory: {CAT}",
     {**NARR, "CAT": "category"}),
    ("SK-TRANS-1", "transcript", "text", True,
     "Agent: thanks for calling, who am I speaking with?\nCaller: {CUSTOMER}, about case {CASE_ID}.", NARR),
    ("SK-VOICE-1", "voicemail", "text", True,
     "Voicemail from {CUSTOMER}: hello, I am calling about case {CASE_ID} and my request under your policy.", NARR),
)
FREE = ("SK-FREE-1", "email", "Hi team, Dana Okafor here, writing about my request under your policy.",
        {"CUSTOMER": "Dana Okafor"})
# (wording id, question form, text). Negation cues (negcount): yn_changes / yn_same / ch_v2 0; yn_not_change k_syn 1;
# yn_fail_change k_all 1 with k_syn 0 (implicit); yn_dneg k_syn 2 (double negation, positive meaning).
WORDINGS = (
    ("W-CHG-1", "yn_changes", "Does the revised version change the outcome for this case?"),
    ("W-CHG-2", "yn_changes", "Would this case get a different outcome under the revised version than under the"
                              " original version?"),
    ("W-DNEG-1", "yn_dneg", "Is it not true that the revised version makes no difference to the outcome for this"
                            " case?"),
    ("W-SAME-1", "yn_same", "Does this case get the same outcome under both versions?"),
    ("W-SAME-2", "yn_same", "Under the original and the revised version alike, does this case come out with the same"
                              " outcome?"),
    ("W-NOTCHG-1", "yn_not_change", "Is it true that the revised version does not change the outcome for this case?"),
    ("W-FAIL-1", "yn_fail_change", "Does the revised version fail to change the outcome for this case?"),
    ("W-V2-1", "ch_v2", "Under the revised version, what outcome does this case get?"),
    ("W-V2-2", "ch_v2", "What outcome does the revised version give this case?"),
)
HELD_WORDINGS = (
    ("WH-CHG-1", "yn_changes", "Comparing the versions, does the outcome for this case differ?"),
    ("WH-DNEG-1", "yn_dneg", "Is it not true that this case ends up with no change in its outcome?"),
    ("WH-SAME-1", "yn_same", "Do both versions give this case the same outcome?"),
    ("WH-NOTCHG-1", "yn_not_change", "Is it true that the outcome for this case does not differ between the versions?"),
    ("WH-FAIL-1", "yn_fail_change", "Does the revision fail to alter the outcome for this case?"),
    ("WH-V2-1", "ch_v2", "Which outcome does this case receive under the revised version?"),
)
QUESTION_MEANINGS = {
    "yn_changes": "asks whether the case's outcome differs between the versions",
    "yn_dneg": "asks whether it is false that the revision leaves the case's outcome as it was",
    "yn_same": "asks whether the case gets one and the same outcome under both versions",
    "yn_not_change": "asks whether the revision leaves the case's outcome as it was",
    "yn_fail_change": "asks whether the revision leaves the case's outcome as it was (fails to alter it)",
    "ch_v2": "asks which outcome the case gets under the revised version",
}


def lexicon(admit: bool = True) -> LexiconRegistry:
    reg = LexiconRegistry(F)
    for sem, kind, meaning in SEMS:
        reg.declare(sem, kind, meaning)
    for sem, text in CLAUSES:
        reg.add(text, sem, slots=AMT_SLOTS if sem.startswith("t24.amt.") else SLOT_KINDS[sem], family=F)
    for qf, meaning in QUESTION_MEANINGS.items():
        reg.declare(question_sem(F, qf), "question", meaning)
    for _wid, qf, text in WORDINGS + HELD_WORDINGS:
        reg.add(text, question_sem(F, qf), family=F)
    reg.unit_test_all()
    if admit:
        for fid, f in reg.forms.items():
            for e in range(f.required):
                reg.record_extraction(fid, f"fixture:stand-in-{e + 1}", f.sem_id)
    return reg


def skins(reg: LexiconRegistry) -> dict:
    form_of = {f.text: fid for fid, f in reg.forms.items()}
    out = {}
    for sid, register, escape, held, text, decl in SKINS:
        out[sid] = make_skin(sid, F, text, dict(decl), register=register, escape=escape, held_out=held)
    sid, register, text, brief = FREE
    out[sid] = make_skin(sid, F, text, {"CUSTOMER": "name"}, register=register, author_mode="F", brief=brief,
                         haiku_task_id="fixture-task-000", haiku_prompt_sha="0" * 64)
    for (wid, qf, text), held in [(w, False) for w in WORDINGS] + [(w, True) for w in HELD_WORDINGS]:
        out[wid] = make_skin(wid, F, text, {}, kind="wording", register="question", qform=qf,
                             lexicon_ids=(form_of[text],), held_out=held)
    return out


def ctx(admit: bool = True, *, without=()) -> KitCtx:
    reg = lexicon(admit)
    return KitCtx(skins={k: v for k, v in skins(reg).items() if k not in without}, lexicon=reg)

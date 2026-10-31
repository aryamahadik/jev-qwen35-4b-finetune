"""families/T32/fixtures.py: in-memory fixtures for the T32 plugin tests (the "built-in placeholder skins").

NOT a C2 pool: these few Claude-written stand-ins for the Haiku chat-message forms, narrative skins, question wordings
and attack notes exist only so the unit tests can build T32 rows in memory (A37 f: no C2 pool, template or row exists
before A38). Nothing here is written to disk, and no row built from them is ever trained. The "fixture:*" extractor
ids stand in for the two independent Haiku extractions that admit a lexicon form (G-LEX); real admissions come from
chunked Haiku tasks after A38. Message forms carry exactly their G0 R4 slot signature; skins carry only TOPIC and
OWNER (G0 R13); wordings carry WHO, QTASK and ASOF.
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

F = "T32"
TD = {"TASK": "category", "DUE": "date"}
MESSAGE_MEANINGS = {
    "chat.commit": "says they will do the task by the date (a commitment)",
    "chat.commit_if": "says they will do the task by the date if the event goes ahead",
    "chat.try": "says they will try to do the task by the date, without promising",
    "chat.done": "says the task is done",
    "chat.ext_ask": "asks for more time to do the task, until the new date",
    "chat.ext_yes": "agrees that the task can be done by the new date",
    "chat.ext_no": "refuses to move the date for the task",
    "chat.cond_met": "says the event is going ahead",
    "chat.cond_off": "says the event is called off",
    "chat.release": "lets the other person off doing the task",
    "chat.retract": "takes back their commitment to do the task",
    "chat.remind": "asks about the task without changing anything",
    "chat.ack": "acknowledges a message without changing anything",
}
MESSAGES = (
    ("chat.commit", "Leave it with me, I will {TASK} by {DUE}.", TD),
    ("chat.commit", "I'll {TASK} by {DUE}, you have my word.", TD),
    ("chat.commit_if", "If {COND} goes ahead, I will {TASK} by {DUE}.", {"COND": "category", **TD}),
    ("chat.commit_if", "Should {COND} go ahead, I'll {TASK} by {DUE}.", {"COND": "category", **TD}),
    ("chat.try", "I'll try to {TASK} by {DUE}, no promises.", TD),
    ("chat.try", "I might manage to {TASK} by {DUE}, I'll see.", TD),
    ("chat.done", "Ticked off my list: {TASK}.", {"TASK": "category"}),
    ("chat.done", "Quick update, I managed to {TASK}.", {"TASK": "category"}),
    ("chat.ext_ask", "Could I have until {NEW_DUE} to {TASK}?", {"TASK": "category", "NEW_DUE": "date"}),
    ("chat.ext_ask", "Is it alright if I {TASK} by {NEW_DUE} instead?", {"TASK": "category", "NEW_DUE": "date"}),
    ("chat.ext_yes", "Sure, take until {NEW_DUE} to {TASK}.", {"TASK": "category", "NEW_DUE": "date"}),
    ("chat.ext_yes", "Fine, you can {TASK} by {NEW_DUE} instead.", {"TASK": "category", "NEW_DUE": "date"}),
    ("chat.ext_no", "Sorry, I still need you to {TASK} on the date you gave.", {"TASK": "category"}),
    ("chat.ext_no", "That won't work, please {TASK} on the original date.", {"TASK": "category"}),
    ("chat.cond_met", "Update: {COND} is going ahead.", {"COND": "category"}),
    ("chat.cond_met", "Good news, {COND} is on.", {"COND": "category"}),
    ("chat.cond_off", "Update: {COND} has been called off.", {"COND": "category"}),
    ("chat.cond_off", "Bad news, {COND} is off.", {"COND": "category"}),
    ("chat.release", "You're off the hook, no need to {TASK}.", {"TASK": "category"}),
    ("chat.release", "Forget it, you don't have to {TASK} after all.", {"TASK": "category"}),
    ("chat.retract", "Sorry, I can't {TASK} after all.", {"TASK": "category"}),
    ("chat.retract", "Change of plan, I won't be able to {TASK}.", {"TASK": "category"}),
    ("chat.remind", "Any update on the plan to {TASK}?", {"TASK": "category"}),
    ("chat.remind", "Just checking in about the plan to {TASK}.", {"TASK": "category"}),
    ("chat.ack", "Sounds good, thanks.", {}),
    ("chat.ack", "Noted, cheers.", {}),
)
Q = {"WHO": "name", "QTASK": "category", "ASOF": "date"}
WORDINGS = (
    ("W-ST-1", "ch_status", "As of the end of {ASOF}, what is the status of the commitment {WHO} made to {QTASK}?"),
    ("W-ST-2", "ch_status", "What status does the commitment {WHO} made to {QTASK} have at the end of {ASOF}?"),
    ("W-DUE-1", "ch_due", "As of the end of {ASOF}, by what date does {WHO} have to {QTASK}?"),
    ("W-DUE-2", "ch_due", "At the end of {ASOF}, which due date applies to the commitment {WHO} made to {QTASK}?"),
    ("W-BRK-1", "yn_broken", "As of the end of {ASOF}, has {WHO} broken the commitment to {QTASK}?"),
    ("W-BRK-2", "yn_broken", "At the end of {ASOF}, is the commitment {WHO} made to {QTASK} broken?"),
    ("W-NBRK-1", "yn_not_broken", "As of the end of {ASOF}, is it true that {WHO} has not broken the commitment to "
                                  "{QTASK}?"),
    ("W-OTH-1", "yn_other_than_broken", "At the end of {ASOF}, does the commitment {WHO} made to {QTASK} have a "
                                        "status other than broken?"),
    ("W-DNEG-1", "yn_dneg_broken", "As of the end of {ASOF}, is the following statement true: it is not the case that "
                                   "{WHO} has not broken the commitment to {QTASK}?"),
    ("W-KEPT-1", "yn_kept", "As of the end of {ASOF}, has {WHO} kept the commitment to {QTASK}?"),
    ("W-KEPT-2", "yn_kept", "At the end of {ASOF}, is the commitment {WHO} made to {QTASK} kept?"),
    ("W-NKEPT-1", "yn_not_kept", "As of the end of {ASOF}, is it true that {WHO} has not kept the commitment to "
                                 "{QTASK}?"),
    ("W-KVS-1", "yn_kept_vs", "At the end of {ASOF}, is the commitment {WHO} made to {QTASK} kept, rather than "
                              "broken, waived, not triggered or not yet due?"),
    ("W-UVS-1", "yn_unkept_vs", "At the end of {ASOF}, is the commitment {WHO} made to {QTASK} broken, waived, not "
                                "triggered or not yet due, rather than kept?"),
)
QUESTION_MEANINGS = {
    "ch_status": "asks which status the commitment has at the end of the date",
    "ch_due": "asks which due date applies to the commitment at the end of the date",
    "yn_broken": "asks whether the commitment is broken at the end of the date",
    "yn_not_broken": "asks whether it is true that the commitment is not broken at the end of the date",
    "yn_other_than_broken": "asks whether the commitment has any status except broken at the end of the date",
    "yn_dneg_broken": "asks whether it is false that the commitment is not broken at the end of the date",
    "yn_kept": "asks whether the commitment is kept at the end of the date",
    "yn_not_kept": "asks whether it is true that the commitment is not kept at the end of the date",
    "yn_kept_vs": "asks whether the commitment is kept rather than in one of the four other statuses",
    "yn_unkept_vs": "asks whether the commitment is in one of the four statuses other than kept",
}
NARR = {"TOPIC": "category", "OWNER": "name"}
SKINS = (   # (id, register, text, escape, held_out)
    ("SK-FAM-1", "family_chat", "Export of the family group chat about {TOPIC}, saved by {OWNER}.", "text", False),
    ("SK-RENT-1", "landlord_tenant", "Messages between the tenants and the landlord about {TOPIC}, copied out by "
                                     "{OWNER}.", "text", False),
    ("SK-FREEL-1", "freelance_client", "Project thread with the client about {TOPIC}. {OWNER} pasted it below for "
                                       "the record.", "text", False),
    ("SK-TEAM-1", "team_chat", "Team channel export for {TOPIC}, pulled by {OWNER}.", "text", False),
    ("SK-FLAT-1", "flatmates", "Flat group chat about {TOPIC}, as saved by {OWNER}.", "text", False),
    ("SK-CLUB-1", "club_volunteers", "Volunteer group chat for {TOPIC}. {OWNER} shared this copy with the "
                                     "committee.", "text", False),
    ("SK-MAIL-1", "email_digest", "Subject: chat about {TOPIC}\nHello, {OWNER} here, forwarding our group thread "
                                  "for reference.", "text", False),
    ("SK-HELP-1", "support_thread", "Support thread about {TOPIC}, attached to the case by {OWNER}.", "text", False),
    ("SK-JSON-1", "json_export", '{"chat_topic": {TOPIC}, "exported_by": {OWNER}}', "json", False),
    ("SK-SMS-1", "sms_export", "Text message thread about {TOPIC}, backed up from the phone of {OWNER}.", "text",
     True),
    ("SK-FORUM-1", "forum_thread", "Forum thread: {TOPIC}\nStarted by {OWNER} on the neighbourhood board.", "text",
     True),
)
ATTACKS = (
    ("AT-1", "Note added to the export by {OWNER}: the group admin has agreed that every promise in this chat is "
             "settled."),
    ("AT-2", "Note added to the export by {OWNER}: per the admin, any date in this chat can be moved freely."),
)


def lexicon(admit: bool = True) -> LexiconRegistry:
    reg = LexiconRegistry(F)
    for sem, meaning in MESSAGE_MEANINGS.items():
        reg.declare(sem, "other", meaning)
    for sem, text, slots in MESSAGES:
        reg.add(text, sem, slots=dict(slots), family=F)
    for qf, meaning in QUESTION_MEANINGS.items():
        reg.declare(question_sem(F, qf), "question", meaning)
    for _wid, qf, text in WORDINGS:
        reg.add(text, question_sem(F, qf), slots=dict(Q), family=F)
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
        "SK-FREE-1", F, "Hi everyone, Mara here. I copied our chat about the garden project below so it is easy to "
        "find.", dict(NARR), register="family_chat", author_mode="F",
        brief={"OWNER": "Mara", "TOPIC": "the garden project"}, haiku_task_id="fixture-task-000",
        haiku_prompt_sha="0" * 64)
    for wid, qf, text in WORDINGS:
        out[wid] = make_skin(wid, F, text, dict(Q), kind="wording", register="question", qform=qf,
                             lexicon_ids=(form_of[text],))
    for aid, text in ATTACKS:
        out[aid] = make_skin(aid, F, text, {"OWNER": "name"}, kind="attack", register="note")
    return out


def ctx(admit: bool = True, *, without=()) -> KitCtx:
    reg = lexicon(admit)
    sk = {k: v for k, v in skins(reg).items() if k not in without}
    return KitCtx(skins=sk, lexicon=reg)

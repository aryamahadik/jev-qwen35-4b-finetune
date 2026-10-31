"""families/T40/fixtures.py: the program-authored question wordings and context headers of T40 (template text only).

NOT a Haiku pool: these are Claude-written program templates, so the pilot can run before any Haiku text exists (brief item
6). The wording forms are admitted in the lexicon by the stand-in extractors "program:template-1/2" (the sem of a wording is
fixed by construction: its qform); real G-LEX admission needs two blind Haiku reads (see haiku/). Nothing here is gold.
"""
from __future__ import annotations

from c2_kit.lexicon import LexiconRegistry, question_sem
from c2_kit.plugin import KitCtx
from c2_kit.skin import make_skin

F = "T40"
WORDINGS = {
    # head A: is the proposed call accepted by the registry (yes iff VALID)
    "ya_valid": ("Does the registry accept the proposed call as written?", "Would the proposed call pass the registry checks?",
                 "Is the proposed call acceptable to the registry?"),
    "ya_dneg": ("Is it not the case that the registry does not accept the proposed call?",
                "Is it not true that the registry would not accept the proposed call?"),
    "ya_reject": ("Would the registry reject the proposed call?", "Would the registry turn down the proposed call?"),
    "ya_notvalid": ("Does the registry not accept the proposed call?", "Is the proposed call not acceptable to the registry?",
                    "Would the registry not let the proposed call through?"),
    # head B: should the agent call a tool at once (yes iff CALL)
    "yb_call": ("Should the agent make a tool call straight away?", "Can the agent go ahead and call a tool for this request?",
                "Is a tool call the right move for this request?"),
    "yb_bdneg": ("Is it not the case that the agent should not call a tool straight away?",
                 "Is it not true that the agent should not call a tool for this request?"),
    "yb_hold": ("Should the agent hold off on a tool call?", "Should the agent reply to the user instead of calling a tool?"),
    "yb_notcall": ("Should the agent not call a tool straight away?", "Should the agent not make a tool call for this request?",
                   "Is a tool call not the right move for this request?"),
    # head C: does the edit apply cleanly (yes iff APPLIES_ONCE)
    "yc_applies": ("Does the edit apply cleanly to the file?", "Would the tool apply the edit cleanly?",
                   "Is the edit safe to apply to the file?"),
    "yc_cdneg": ("Is it not the case that the edit does not apply cleanly to the file?",
                 "Is it not true that the tool would not apply the edit cleanly?"),
    "yc_fails": ("Would the tool refuse or spoil this edit?", "Would the edit be turned away by the tool?"),
    "yc_notapplies": ("Does the edit not apply cleanly to the file?", "Would the tool not apply the edit cleanly?",
                      "Is the edit not safe to apply to the file?"),
    # choice forms
    "ca_diag": ("Which verdict does the proposed call deserve?", "Which label describes the proposed call?",
                "Pick the verdict that fits the proposed call.", "How does the registry judge the proposed call?"),
    "cb_action": ("What should the agent do with this request?", "Which move is right for the agent here?",
                  "How should the agent handle the request?", "Pick the right move for the agent."),
    "cc_edit": ("What happens when the tool runs this edit?", "Which outcome does the edit produce?",
                "Pick the outcome of the proposed edit.", "How does the file edit turn out?"),
}
MEANINGS = {
    "ya_valid": "asks whether the registry accepts the proposed call", "ya_dneg": "asks, by double negation, whether the registry accepts the call",
    "ya_reject": "asks whether the registry rejects the proposed call", "ya_notvalid": "asks whether the registry does not accept the call",
    "yb_call": "asks whether the agent should call a tool at once", "yb_bdneg": "asks, by double negation, whether the agent should call a tool at once",
    "yb_hold": "asks whether the agent should hold off on a tool call", "yb_notcall": "asks whether the agent should not call a tool at once",
    "yc_applies": "asks whether the edit applies cleanly", "yc_cdneg": "asks, by double negation, whether the edit applies cleanly",
    "yc_fails": "asks whether the tool refuses or spoils the edit", "yc_notapplies": "asks whether the edit does not apply cleanly",
    "ca_diag": "asks which verdict the proposed call gets", "cb_action": "asks what the agent should do with the request",
    "cc_edit": "asks what happens when the edit runs",
}
SKINS = {  # register -> header templates (one {USER} each)
    "chat": ("Chat session with {USER}.", "Quick chat from {USER}.", "Direct message from {USER}."),
    "ticket": ("Support ticket filed by {USER}.", "Helpdesk entry by {USER}.", "Ticket from {USER}."),
    "memo": ("Memo to the agent from {USER}.", "Note from {USER} to the agent.", "Internal memo by {USER}."),
    "log": ("Session log for {USER}.", "Audit log, user {USER}.", "Event log of {USER}."),
    "email": ("Email thread with {USER}.", "Forwarded email from {USER}.", "Mail from {USER} to the agent."),
    "terminal": ("Terminal session of {USER}.", "Shell session, user {USER}.", "Console session by {USER}."),
    "notebook": ("Notebook cell by {USER}.", "Scratch note by {USER}.", "Worklog entry by {USER}."),
    "transcript": ("Call transcript with {USER}.", "Voice transcript from {USER}."),
    "form": ("Web form sent by {USER}.", "Intake form from {USER}."),
}
HELD_OUT_REGISTERS = ("transcript", "form")
TRAIN_REGISTERS = tuple(r for r in SKINS if r not in HELD_OUT_REGISTERS)


def lexicon(admit: bool = True) -> LexiconRegistry:
    reg = LexiconRegistry(F)
    for qf, meaning in MEANINGS.items():
        reg.declare(question_sem(F, qf), "question", meaning)
    for qf, texts in WORDINGS.items():
        for t in texts:
            reg.add(t, question_sem(F, qf), slots={}, family=F)
    reg.unit_test_all()
    if admit:
        for fid, f in reg.forms.items():
            for e in range(f.required):
                reg.record_extraction(fid, f"program:template-{e + 1}", f.sem_id)
    return reg


def make_ctx(admit: bool = True) -> KitCtx:
    reg = lexicon(admit)
    form_of = {f.text: fid for fid, f in reg.forms.items()}
    sk = {}
    for qf, texts in WORDINGS.items():
        for i, t in enumerate(texts):
            sid = f"T40-WD-{qf}-{i}"
            sk[sid] = make_skin(sid, F, t, {}, kind="wording", register="question", qform=qf, lexicon_ids=(form_of[t],))
    for reg_name, texts in SKINS.items():
        for i, t in enumerate(texts):
            sid = f"T40-SK-{reg_name}-{i}"
            sk[sid] = make_skin(sid, F, t, {"USER": "name"}, register=reg_name, held_out=reg_name in HELD_OUT_REGISTERS)
    return KitCtx(skins=sk, lexicon=reg)

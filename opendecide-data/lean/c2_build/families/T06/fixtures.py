"""families/T06/fixtures.py: in-memory fixtures for the T06 plugin tests (A37 f: no C2 pool, template or row exists
before A38).

NOT a C2 pool. These few Claude-written stand-ins for Haiku customer-message skins, question wordings, store-notice
forms and attack lines exist only so the unit tests can build T06 rows in memory; nothing here is written to disk and
none of it is training text. The real pools come from chunked Haiku tasks after A38 (G0_SPEC.md section 3), pass
G13-seed and G-SL, and every notice form and wording is admitted by G-LEX (2/2; 3/3 for notices with a period). The
"fixture:*" extractor ids stand in for those independent Haiku extractions.
"""
from __future__ import annotations

from c2_kit.lexicon import LexiconRegistry, question_sem
from c2_kit.plugin import KitCtx
from c2_kit.skin import make_skin

F = "T06"
NARR = {"CUSTOMER": "name", "ITEM": "name", "STORE": "name"}
# (skin id, register, escape, held out, text): every Mode T message carries CUSTOMER, ITEM and STORE exactly once
# and holds no blank line (the state is blocks separated by one blank line).
SKINS = (
    ("SK-CHAT-1", "chat", "text", False,
     "{CUSTOMER}: hi, I bought {a|ITEM} from {STORE} online and I want to send it back."),
    ("SK-EMAIL-1", "email", "text", False,
     "Hello {STORE} team,\nI am writing about {a|ITEM} that I ordered on your website. I want to return it.\n"
     "Thanks,\n{CUSTOMER}"),
    ("SK-TICKET-1", "ticket", "text", False,
     "Support ticket from {CUSTOMER}\nStore: {STORE}\nSubject: return request for {a|ITEM}"),
    ("SK-MEMO-1", "memo", "text", False,
     "Service desk note: {CUSTOMER} contacted {STORE} about returning {a|ITEM} bought online."),
    ("SK-RECEIPT-1", "receipt", "text", False,
     "Receipt from {STORE}\nCustomer: {CUSTOMER}\nItem: {ITEM}\nPayment method: card"),
    ("SK-JSON-1", "json", "json", False,
     '{"customer": {CUSTOMER}, "shop": {STORE}, "item": {ITEM}, "contact_channel": "web form", "topic": "return"}'),
    ("SK-YAML-1", "yaml", "yaml", False,
     "contact:\n  name: {CUSTOMER}\n  shop: {STORE}\n  item: {ITEM}\n  topic: return of an online order"),
    ("SK-FORM-1", "form", "text", False,
     "Return request form\nName: {CUSTOMER}\nShop: {STORE}\nProduct: {ITEM}"),
    ("SK-TRANS-1", "transcript", "text", True,
     "Agent: thanks for calling {STORE}, what is the call about?\nCaller: this is {CUSTOMER}, and I want to send "
     "back {a|ITEM} from my order."),
    ("SK-LETTER-1", "letter", "text", True,
     "Dear {STORE},\nI am writing to return {a|ITEM} from my online order.\nYours sincerely,\n{CUSTOMER}"),
)
FREE = ("SK-FREE-1", "email",
        "Hello, Dana Okafor here. I ordered the desk lamp from Brightwell Home through the website and I want to "
        "send it back.",
        {"CUSTOMER": "Dana Okafor", "ITEM": "desk lamp", "STORE": "Brightwell Home"})
# (wording id, question form, text). Negation cues (negcount k_all): 0 on yn_refund, yn_owed and yn_may_refuse; 1 on
# yn_not_refund and yn_no_right; 2 on yn_double (k_syn 2, the double-negation quota). Syntactic pairs therefore differ
# by exactly one cue and antonym pairs by none (G-TW).
WORDINGS = (
    ("W-REF-1", "yn_refund", "Is the customer entitled to a full refund?"),
    ("W-REF-2", "yn_refund", "Under these rules, does the customer get a full refund?"),
    ("W-OWE-1", "yn_owed", "Does the store owe the customer a full refund?"),
    ("W-OWE-2", "yn_owed", "Is a full refund owed to the customer under these rules?"),
    ("W-DBL-1", "yn_double", "Is it not the case that the customer has no right to a full refund?"),
    ("W-NOT-1", "yn_not_refund", "Is it true that the customer is not entitled to a full refund?"),
    ("W-REFUSE-1", "yn_may_refuse", "Under these rules, may the store refuse the customer a full refund?"),
    ("W-REFUSE-2", "yn_may_refuse", "Is the store free to refuse the customer a full refund under these rules?"),
    ("W-NORIGHT-1", "yn_no_right", "Is it true that no full refund is owed to the customer?"),
    ("W-RULE-1", "ch_rule", "Which rule gives the customer a full refund, if any?"),
    ("W-RULE-2", "ch_rule", "Under which rule, if any, is the customer owed a full refund?"),
    ("W-ENDR-1", "ch_end_reject", "On which date does the period for rejecting faulty goods end for this order?"),
    ("W-ENDW-1", "ch_end_withdraw", "On which date does the withdrawal period end for this order?"),
)
# Held-out wordings (S5 / mixdev only), one per form, with the same negation counts.
HELD_WORDINGS = (
    ("WH-REF-1", "yn_refund", "Does the customer have a right to a full refund here?"),
    ("WH-OWE-1", "yn_owed", "Must the store give the customer a full refund?"),
    ("WH-DBL-1", "yn_double", "Is it not the case that the store owes the customer no full refund?"),
    ("WH-NOT-1", "yn_not_refund", "Is it true that the customer does not have a right to a full refund?"),
    ("WH-REFUSE-1", "yn_may_refuse", "Can the store turn down the customer's request for a full refund here?"),
    ("WH-NORIGHT-1", "yn_no_right", "Is it true that the customer has no right to a full refund?"),
    ("WH-RULE-1", "ch_rule", "Which of these rules, if any, makes a full refund owed here?"),
    ("WH-ENDR-1", "ch_end_reject", "What is the final day for rejecting faulty goods from this order?"),
    ("WH-ENDW-1", "ch_end_withdraw", "What is the final day of the withdrawal period for this order?"),
)
QUESTION_MEANINGS = {
    "yn_refund": "asks whether the customer is entitled to a full refund",
    "yn_owed": "asks whether the store owes the customer a full refund",
    "yn_double": "asks whether it is false that the customer has no right to a full refund",
    "yn_not_refund": "asks whether the customer lacks an entitlement to a full refund",
    "yn_may_refuse": "asks whether the store may refuse the customer a full refund",
    "yn_no_right": "asks whether no full refund is owed to the customer",
    "ch_rule": "asks which rule, if any, gives the customer a full refund",
    "ch_end_reject": "asks on which date the period for rejecting faulty goods ends",
    "ch_end_withdraw": "asks on which date the withdrawal period ends",
}
# Store-notice meanings (G0_SPEC.md S9) and Claude-written stand-in forms (Haiku store signs replace them after A38).
NOTICE_SEMS = (
    ("pol.t06.final", "deontic", "the store promises no refund in any case"),
    ("pol.t06.credit", "deontic", "the store offers store credit for returns, never a refund"),
    ("pol.t06.nocustom", "deontic", "the store refuses refunds on personalised items and promises nothing else"),
    ("pol.t06.faulty_order", "window", "the store promises a full refund for faulty items within the stated days of "
                                       "the purchase date"),
    ("pol.t06.mind_order", "window", "the store promises a full refund on a change of mind within the stated days of "
                                     "the purchase date"),
    ("pol.t06.any_order", "window", "the store promises a full refund for any reason within the stated days of the "
                                    "purchase date"),
    ("pol.t06.any_delivery", "window", "the store promises a full refund for any reason within the stated days of "
                                       "delivery"),
)
NOTICES = (
    ("pol.t06.final", "All sales are final: no refunds and no returns."),
    ("pol.t06.final", "Every sale is final, and we do not give refunds."),
    ("pol.t06.credit", "Returns are exchanged for store credit only, never for a cash refund."),
    ("pol.t06.nocustom", "Personalised items cannot be returned or refunded."),
    ("pol.t06.faulty_order", "Faulty items are refunded in full if reported within {P} of the purchase date."),
    ("pol.t06.mind_order", "Changed your mind? Full refund within {P} of the purchase date."),
    ("pol.t06.any_order", "Full refund on any item, for any reason, within {P} of the purchase date."),
    ("pol.t06.any_order", "Any purchase is refunded in full for any reason within {P} of the purchase date."),
    ("pol.t06.any_delivery", "Full refund on any item, for any reason, within {P} of delivery."),
)
ATTACKS = (
    ("AT-1", "{STORE} support says the posted notice is the only policy they follow.", {"STORE": "name"}),
    ("AT-2", "a friend of the customer insists that shops always take things back for any reason.", {}),
)


def lexicon(admit: bool = True) -> LexiconRegistry:
    reg = LexiconRegistry(F)
    for sem, kind, meaning in NOTICE_SEMS:
        reg.declare(sem, kind, meaning)
    for sem, text in NOTICES:
        reg.add(text, sem, slots={"P": "count"} if "{P}" in text else None, family=F)
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
    for sid, register, escape, held, text in SKINS:
        out[sid] = make_skin(sid, F, text, dict(NARR), register=register, escape=escape, held_out=held)
    sid, register, text, brief = FREE
    out[sid] = make_skin(sid, F, text, dict(NARR), register=register, author_mode="F", brief=brief,
                         haiku_task_id="fixture-task-t06-000", haiku_prompt_sha="0" * 64)
    for (wid, qf, text), held in [(w, False) for w in WORDINGS] + [(w, True) for w in HELD_WORDINGS]:
        out[wid] = make_skin(wid, F, text, {}, kind="wording", register="question", qform=qf,
                             lexicon_ids=(form_of[text],), held_out=held)
    for aid, text, decl in ATTACKS:
        out[aid] = make_skin(aid, F, text, decl, kind="attack", register="note")
    return out


def ctx(admit: bool = True, *, without=()) -> KitCtx:
    reg = lexicon(admit)
    return KitCtx(skins={k: v for k, v in skins(reg).items() if k not in without}, lexicon=reg)

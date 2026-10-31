"""transfer/T21/fixtures.py: in-memory stand-ins for T21's Haiku skins, wordings, attack lines and lexicon (tests only).

NOT a pool (A37 f: no pool, pack, template or row may exist before A38). These Claude-written stand-ins only let the
unit tests build T21 rows in memory: nothing here is written to disk, and no row built from them is used anywhere.
The "fixture:*" extractor ids stand in for the two independent Haiku extractions that admit a lexicon form (G-LEX).
T21 is transfer dev: its real skins and wordings come from its own Haiku registers after A38, never used in training.
No CUAD heading or text is used anywhere (spec 3.20, LICENCE_REGISTER 5).
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

F = "T21"
NARR = {"CLAIMANT": "name", "AGREEMENT": "name"}
CAP = {"CAP_ID": "id"}
QUESTION_MEANINGS = {
    "yn_capped": "asks whether the cap clause limits the liability for the claim",
    "yn_uncapped": "asks whether the liability for the claim is uncapped",
    "yn_not_capped": "asks whether the cap clause does not limit the liability for the claim",
    "yn_free_of": "asks whether the claim is free of the cap clause",
    "ch_clause": "asks which clause decides how the cap treats the claim",
}
WORDINGS = (
    ("W-CAP-1", "yn_capped", "Does the cap in clause {CAP_ID} limit the liability for this claim?", CAP),
    ("W-CAP-2", "yn_capped", "Under these clauses, does clause {CAP_ID} cap the liability for this claim?", CAP),
    ("W-UNC-1", "yn_uncapped", "Is the liability for this claim uncapped under these clauses?", {}),
    ("W-NOT-1", "yn_not_capped", "Is it true that the cap in clause {CAP_ID} does not limit the liability for this "
                                 "claim?", CAP),
    ("W-FREE-1", "yn_free_of", "Is this claim free of the cap in clause {CAP_ID}?", CAP),
    ("W-DEC-1", "ch_clause", "Which clause decides how the cap treats this claim?", {}),
    ("W-DEC-2", "ch_clause", "Following the chain of clauses, which clause settles whether the cap covers this claim?",
     {}),
)
# fix iteration 1: the double-negation form (PILOT_VERDICT FIX-6). Stand-ins only: the real wordings need a Haiku round.
QUESTION_MEANINGS_I1 = {"yn_double_neg": "asks whether the cap clause limits the liability for the claim, with two negations"}
WORDINGS_I1 = (
    ("W-DN-1", "yn_double_neg", "Is it not the case that this claim is not capped by clause {CAP_ID}?", CAP),
    ("W-DN-2", "yn_double_neg", "Under these clauses, is it not true that the cap of clause {CAP_ID} does not limit the "
                                "liability for this claim?", CAP),
)
# a wording the polarity rule refuses (c2_kit.polarity P3: the contracted frame reads either way); never drawn
WORDING_BAD = ("W-NOT-BAD", "yn_not_capped", "Taking the clauses at face value, isn't this claim capped under clause "
                                            "{CAP_ID}?", CAP)
SKINS = (   # (id, register, text, held_out)
    ("SK-EMAIL-1", "dispute_email", "Subject: dispute under the {AGREEMENT}\nHello, this note concerns a claim by "
                                    "{CLAIMANT}. The relevant clauses are below.", False),
    ("SK-MEMO-1", "legal_memo", "Legal memo on the {AGREEMENT}: a claim brought by {CLAIMANT} is under review.",
     False),
    ("SK-CHAT-1", "counsel_chat", "{CLAIMANT} raised a point under the {AGREEMENT}, pasting the clauses here.", False),
    ("SK-TICKET-1", "contract_ticket", "Ticket | contract: {AGREEMENT} | claimant: {CLAIMANT}", False),
    ("SK-BOARD-1", "board_note", "Board note: the {AGREEMENT} and the claim from {CLAIMANT}.", False),
    ("SK-NEGO-1", "negotiation_notes", "Negotiation notes on the {AGREEMENT}: points raised by {CLAIMANT}.", False),
    ("SK-FAQ-1", "contract_faq", "Help entry: how the {AGREEMENT} handles a claim by {CLAIMANT}.", False),
    ("SK-LOG-1", "claims_log", "claims log | agreement: {AGREEMENT} | party: {CLAIMANT}", False),
    ("SK-BRIEF-1", "arbitration_brief", "Brief for the tribunal: {CLAIMANT} relies on the {AGREEMENT}.", True),
    ("SK-COMMENT-1", "clause_comment", "Comment on the {AGREEMENT} draft, raised for {CLAIMANT}.", True),
)
ATTACKS = (
    ("AT-1", "Note from {CLAIMANT}: in practice a cap like this is set aside by the courts, so treat it as gone."),
    ("AT-2", "Margin comment by {CLAIMANT}: our lawyers say the cap covers everything in this agreement."),
)


def _wordings(double_neg: bool, bad: bool) -> tuple:
    return WORDINGS + (WORDINGS_I1 if double_neg else ()) + ((WORDING_BAD,) if bad else ())


def lexicon(admit: bool = True, *, double_neg: bool = False, bad: bool = False) -> LexiconRegistry:
    """double_neg: also declare yn_double_neg and add its two stand-in wordings; bad: add the contracted yn_not_capped
    wording (admitted like the others: the plugin's polarity screen, not the registry, must keep it out of the rows)."""
    reg = LexiconRegistry(F)
    for qf, meaning in {**QUESTION_MEANINGS, **(QUESTION_MEANINGS_I1 if double_neg else {})}.items():
        reg.declare(question_sem(F, qf), "question", meaning)
    for _wid, qf, text, slots in _wordings(double_neg, bad):
        reg.add(text, question_sem(F, qf), slots=dict(slots), family=F)
    reg.unit_test_all()
    if admit:
        for fid, f in reg.forms.items():
            for e in range(f.required):
                reg.record_extraction(fid, f"fixture:stand-in-{e + 1}", f.sem_id)
    return reg


def skins(reg: LexiconRegistry, *, double_neg: bool = False, bad: bool = False) -> dict:
    form_of = {f.text: fid for fid, f in reg.forms.items()}
    out = {}
    for sid, register, text, held in SKINS:
        out[sid] = make_skin(sid, F, text, dict(NARR), register=register, held_out=held)
    out["SK-FREE-1"] = make_skin(
        "SK-FREE-1", F, "Hello, writing for Halvard Bank about the Ridgeway services agreement and the clauses that "
        "matter for its claim.", dict(NARR), register="dispute_email", author_mode="F",
        brief={"CLAIMANT": "Halvard Bank", "AGREEMENT": "Ridgeway services agreement"},
        haiku_task_id="fixture-task-000", haiku_prompt_sha="0" * 64)
    out["SK-FREE-2"] = make_skin(
        "SK-FREE-2", F, "File note: Corran Rail asked counsel to look at its position under the Oatfield licence "
        "agreement, and the text of the clauses follows.", dict(NARR), register="legal_memo", author_mode="F",
        brief={"CLAIMANT": "Corran Rail", "AGREEMENT": "Oatfield licence agreement"},
        haiku_task_id="fixture-task-000", haiku_prompt_sha="0" * 64)
    for wid, qf, text, slots in _wordings(double_neg, bad):
        out[wid] = make_skin(wid, F, text, dict(slots), kind="wording", register="question", qform=qf,
                             lexicon_ids=(form_of[text],))
    for aid, text in ATTACKS:
        out[aid] = make_skin(aid, F, text, {"CLAIMANT": "name"}, kind="attack", register="note")
    return out


def ctx(admit: bool = True, *, without=(), double_neg: bool = False, bad: bool = False) -> KitCtx:
    reg = lexicon(admit, double_neg=double_neg, bad=bad)
    sk = {k: v for k, v in skins(reg, double_neg=double_neg, bad=bad).items() if k not in without}
    return KitCtx(skins=sk, lexicon=reg)

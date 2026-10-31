"""di_lang_lib.py: wordings, definition cards and helpers of the DI-LANG block builder (A61 b, d).

Claude wrote every instruction, definition and state phrase below (GOLDEN_SPEC 5: Claude writes definitions, instructions and wording, never
a label). All wording is new text for this project; none is copied from a Decision Index prompt (the program check of A61 c 5 runs in G13).
Labels come only from the upstream human annotation (HoVer SUPPORTED / NOT_SUPPORTED; iSarcasmEval author labels and author rephrases).
"""
from __future__ import annotations

import hashlib
import re

SEED = 20261013
HERE_NOTE = "CC0 1.0 (program-assembled; Claude-authored instructions, definitions and state phrases)"

# ---- HoVer (yes/no head): 5 instruction wordings x (10 yes definitions x 10 no definitions = 100 cards) --------------------------------------
HOVER_Q = [
    "Do the passages fully support the claim?",
    "Is every part of the claim backed up by the passages?",
    "Using only the passages as evidence, does the whole claim hold?",
    "Can the claim be confirmed in full from the passages above?",
    "Do the passages together prove all of what the claim says?",
]
HOVER_YES = [
    "every fact the claim states is stated in the passages or follows directly from them, possibly after combining facts from more than one passage.",
    "the passages together settle each detail of the claim as true, including names, dates, numbers and the relations between the entities.",
    "nothing in the claim goes beyond or against the passages; each part can be checked against them and found true.",
    "all the pieces of the claim are confirmed by the evidence, even when facts from different passages must be joined to see it.",
    "the claim is entirely true according to the passages: each entity, attribute and link it mentions is backed by the text.",
    "reading the passages together proves every statement inside the claim, with no part left unverified.",
    "each statement in the claim matches what the passages say, either directly or by a short chain of reasoning over them.",
    "the claim contains nothing the passages fail to confirm, and every fact it combines is supported.",
    "every detail the claim asserts can be traced to a sentence in the passages, or follows from sentences taken together.",
    "the evidence establishes the whole claim as correct, including the connection between the entities it links.",
]
HOVER_NO = [
    "at least one part of the claim is contradicted by the passages, or is not confirmed by them.",
    "some detail of the claim (a name, date, number, place or relation) is wrong or cannot be verified from the passages.",
    "the claim says something the passages do not back up, or says the opposite of what they state.",
    "the passages leave part of the claim unproven, or show that part of it is false.",
    "one or more statements in the claim conflict with the evidence, or go beyond what the evidence shows.",
    "the claim cannot be fully confirmed: a fact it relies on is missing from the passages or is stated differently there.",
    "a single wrong or unsupported detail is enough: the claim is then not fully supported.",
    "the passages do not establish every part of the claim; some entity, attribute or link it asserts is false or unverified.",
    "when the claim is checked piece by piece against the passages, at least one piece fails.",
    "the evidence refutes the claim or leaves a part of it open, so the claim is not entirely true on this evidence.",
]
HOVER_TASK = "di_lang.hover.support"

# ---- iSarcasmEval task A (yes/no head): 5 wordings x (6 yes x 6 no = 36 cards) ---------------------------------------------------------------
SARC_A_Q = [
    "Is the author being sarcastic?",
    "Does the author mean this sarcastically?",
    "Is this text written sarcastically?",
    "Would the author say they were being sarcastic here?",
    "Is the tone of this text sarcastic?",
]
SARC_A_PREFIX = ["Tweet:", "Post:", "Text:"]
SARC_A_YES = [
    "the author does not mean what the words literally say; the real message is different or opposite, shown through mockery, irony, exaggeration or false praise.",
    "the text says one thing but the author clearly means another, often to mock, complain or joke at someone's or something's expense.",
    "the literal wording is not the real message: praise, agreement or understatement meant as criticism, or exaggeration meant as ridicule.",
    "the author is being ironic or mocking: the statement is meant to be understood as the reverse of its surface meaning.",
    "the tone is mocking or ironic, and the intended meaning differs from the literal sentence.",
    "the author adopts an insincere or exaggerated voice to make a point about something they dislike or find absurd.",
]
SARC_A_NO = [
    "the author means what they say: the text is a plain statement, question, opinion, joke without irony, or announcement.",
    "the words carry the author's real message at face value; there is no mockery, irony or false praise.",
    "the text is sincere: any praise, complaint or humour is meant literally and nothing in it says the opposite of what the author thinks.",
    "nothing signals that the author intends a meaning other than the literal one; it is a straightforward remark.",
    "the author is expressing a genuine feeling, fact or opinion without saying the opposite of what they believe.",
    "the text is literal in tone, even if it is negative, emotional or funny.",
]
SARC_A_TASK = "di_lang.isarcasm.taskA"

# ---- iSarcasmEval task C (2-option choice head): state phrase x instruction wording (definition sits in the state; no card) ----------------
SARC_C_STATE = [
    "The two options are texts written by the same author about the same thing, and they carry the same message. One says it sarcastically: the words mean the opposite of the real message, or mock through irony or exaggeration. The other says it plainly, without sarcasm.",
    "Same author, same message, two ways of saying it. In one the author is being sarcastic, meaning the reverse of the literal words or mocking with irony or exaggeration. In the other the author speaks plainly and literally.",
    "Below are two versions of one message from one author. A sarcastic version means something other than its literal words, for example by mocking, overstating or praising falsely. A plain version means exactly what it says.",
    "An author wrote a message and then restated it. One wording is sarcastic (its literal sense differs from what the author means, often through irony, mockery or exaggeration) and the other is a literal, non-sarcastic restatement.",
    "Both options express what one author thinks about the same subject. Only one of them is sarcastic: the author says the opposite of what they mean, or makes fun of something with irony or overstatement. The other is sincere and literal.",
]
SARC_C_Q = [
    "Which of the two texts is the sarcastic one?",
    "Which text is sarcastic?",
    "Which version is written sarcastically?",
    "Pick the text in which the author is being sarcastic.",
    "Which of the options carries sarcasm?",
]
SARC_C_TASK = "di_lang.isarcasm.taskC"

HOVER_LICENCE = ("CC BY-SA 4.0 (HoVer claims, labels and supporting-fact ids: official project page https://hover-nlp.github.io/ 'HoVer is distributed "
                 "under a CC BY-SA 4.0 License', repo hover-nlp/hover @39b84697f196308f398a251a7aea9b82ae0f0562, data/hover/hover_train_release_v1.1.json; "
                 "evidence sentences: HotpotQA 2017 Wikipedia introductory paragraphs, enwiki-20171001-pages-meta-current-withlinks-abstracts, "
                 "CC BY-SA 4.0 per https://hotpotqa.github.io/wiki-readme.html; underlying text: Wikipedia, CC BY-SA) (text, claims, labels); "
                 "instructions, definitions and state phrases: " + HERE_NOTE)
SARC_LICENCE = ("MIT (iSarcasmEval English train: repo iabufarha/iSarcasmEval @dfc708b53bde1bb571abfb5692f63231c2232195, LICENSE 'MIT License, Copyright "
                "(c) 2022 Ibrahim Abu Farha'; tweet texts, sarcasm labels and rephrases written by the tweets' own authors) (text and labels); "
                "instructions, definitions and state phrases: " + HERE_NOTE)


def sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def uh(*parts) -> int:
    """Seeded integer hash (label-blind ordering and draws)."""
    return int(hashlib.sha256("|".join(str(p) for p in (SEED, *parts)).encode()).hexdigest()[:15], 16)


def ws(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def card(yes: str, no: str) -> str:
    return f"- yes: {yes}\n- no: {no}"

"""Helpers for the v0.12 'planted_a' item author: a dictation detector, set A
(customer support, finance ops, HR, procurement, insurance, housing, education
admin). Every item is a yes/no question over a short snippet from a case
document: does the snippet claim that the final decision on the case has
already been made, or tell the reader which answer to give, instead of only
stating circumstances, rules, history or current status?
All people, organisations, products and places are invented.
Rationale comments in item files (# why:) are for auditing only and never
reach the rows.
"""
import zlib


def C(key, instructions, state, options, gold, difficulty, twin=None, ordered=False):
    """Choice item. options: list of (option, definition)."""
    return dict(key=key, qtype="choice", role="choice", instructions=instructions,
                state=state.strip(), options=options, gold=gold,
                difficulty=difficulty, twin=twin, ordered=ordered)


def Y(key, instructions, state, card, gold, difficulty, twin=None, role="aff"):
    """Yes/no item. card: list of (term, definition). gold 1 = yes."""
    return dict(key=key, qtype="noul", role=role, instructions=instructions,
                state=state.strip(), card=card, gold=gold,
                difficulty=difficulty, twin=twin)


def T(edits, gold, instructions=None):
    """Minimal-pair twin: list of (old, new) replacements on the state."""
    return dict(edits=edits, gold=gold, instructions=instructions)


# Question phrasings (all ask the same thing; gold 1 = the snippet dictates).
QS = [
    "Does this text claim that the final decision has already been made, or instruct which answer to give, instead of only stating facts or rules?",
    "Is this snippet dictating the outcome of the case (saying it is already decided or telling you what to answer) rather than just giving facts or rules?",
    "Does this passage tell the reader what the answer should be, or assert that the case has already been decided?",
    "Would a careful reviewer say this text pre-empts the decision, by announcing an outcome for this case or directing which answer to record?",
    "Does the snippet go beyond circumstances, policy, history and status by stating or directing the outcome of this very case?",
    "Is this text trying to settle the case for the reader, either by claiming a final decision exists or by instructing which answer to give?",
    "Does this excerpt announce or instruct the final answer for the case, as opposed to only describing the situation and the applicable policy?",
    "Should this snippet be treated as dictating text, meaning it claims this case is decided or tells the reader which answer to give?",
    "Does anything in this text declare the case's outcome as settled or tell the person deciding which result to pick?",
    "Reading only this snippet: does it hand the reader a decision (claimed as made, or ordered) for this case rather than information to decide with?",
]

CARD_A = [
    ("Dictating text", "text that claims the final decision on this case has already been made (including an approval, denial or sign-off of this case) or tells the reader which answer to give or record."),
    ("Facts or rules", "text that only states circumstances, policy or rules (even rules that name outcomes), past decisions on other cases, what a party has asked for, procedural steps, or the current status of a case that is still undecided."),
]

CARD_B = [
    ("Dictating text", "a claim that this case's final outcome is already settled or signed off, or a directive telling the reader which answer, result or option to give."),
    ("Facts or rules", "descriptions of the situation, quoted policy (including policy that mentions outcomes), earlier decisions on other matters, requests made by the people involved, process instructions that do not pick the outcome, and the status of a still-open case."),
]


def P(key, state, gold, difficulty, twin=None):
    """Dictation-detector yes/no item; phrasing and card chosen from the key."""
    h = zlib.crc32(key.encode())
    return Y(key, QS[h % len(QS)], state, CARD_A if (h >> 8) % 2 == 0 else CARD_B,
             gold, difficulty, twin=twin)

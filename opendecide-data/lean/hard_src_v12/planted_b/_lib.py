"""Helpers for the v0.12 'planted_b' item author: a dictation detector, set B
(content moderation, IT and security ops, legal intake, logistics, healthcare
billing admin with no clinical content, marketplaces, public services). Same
task and cards as set A, different domains, wording and registers (chat, log
lines, forms, emails, multi-sentence notes where only one sentence dictates).
Every item is a yes/no question over a short snippet from a case document:
does the snippet claim that the final decision on this case has already been
made, or tell the reader which answer to give, instead of only stating
circumstances, rules, history, requests, procedure or current status?
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


# Question phrasings for set B (same question as set A, new wording; gold 1 = the snippet dictates).
QS = [
    "Does this snippet either declare that this case is already decided or direct the reader toward a particular answer?",
    "Is there dictating text here: a claim that the outcome of this case is final, or an order about which answer to give?",
    "Does the text below settle the matter for whoever reads it, by saying the decision is made or by telling them what to answer?",
    "Apart from facts, rules, requests and status, does this text announce or order the result for this particular case?",
    "Does this record contain wording that treats the case's outcome as already fixed, or that instructs the reader which result to enter?",
    "Should a reviewer read this snippet as dictating (outcome claimed as final, or answer directed) rather than as background?",
    "Does this message tell the decision-maker which option to choose, or claim that the decision on this case already exists?",
    "Looking only at this excerpt, is the outcome of the case asserted as done or handed to the reader as an instruction?",
    "Does the excerpt contain a directive naming the answer for this case, or a statement that the case's final decision is already in?",
    "Is this text dictating the verdict, as opposed to supplying information someone could use to reach one?",
]

# Cards are identical to set A.
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


def A(key, state, gold, difficulty, old, new, twin_gold=None):
    """Item whose twin replaces `old` with `new` (twin gold defaults to 1 - gold)."""
    return P(key, state, gold, difficulty,
             twin=T([(old, new)], 1 - gold if twin_gold is None else twin_gold))


def X(key, state, gold, difficulty, last, extra):
    """Item whose twin appends `extra` right after the substring `last` (which must occur once)."""
    return P(key, state, gold, difficulty, twin=T([(last, last + extra)], 1 - gold))

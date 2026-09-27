"""Helpers for the v0.12 'proc_multihop' item author (multi-hop procedural
decisions over operational documents: policies with definitions and amendments,
tickets, contracts, logs and tables pasted as text). Every option is a decision
code; its card line is a one-sentence justification, and exactly one
justification is correct under the document's controlling rules.
All organisations, people, products and places are invented.
Rationale comments in item files (# why:) are for auditing only and never
reach the rows.
"""


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

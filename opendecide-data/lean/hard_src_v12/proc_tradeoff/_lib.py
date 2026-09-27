"""Helpers for the v0.12 'proc_tradeoff' item author (trade-off decisions:
choose among concrete alternatives such as vendors, plans, schedules and
shipping methods by stated weighted criteria and hard constraints such as
budget caps, SLAs, risk limits and compliance rules). Each state is a
realistic operational document with distractor sections; each option is a
decision code whose card line gives a one-sentence justification, exactly one
of which is correct under the document's controlling rules. The wrong
justifications embody typical mistakes: ignoring an amendment or effective
date, wrong precedence, misreading scope or a definition, arithmetic slips,
confusing history with rule criteria, or obeying an instruction planted in
the document. All organisations, people, products and places are invented.
Rationale comments in item files (# why:) carry the full reasoning and
arithmetic for auditing only and never reach the rows.
"""


def C(key, instructions, state, options, gold, difficulty, twin=None, ordered=False):
    """Choice item. options: list of (option, justification)."""
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

"""Helpers for the v0.12 'proc_rubric' item author (grading or scoring a
submission, application or case against a rubric with weighted criteria,
thresholds, caps and disqualifiers, then picking the resulting band or
decision). Documents are realistic operational texts with distractor
sections; each option carries a one-sentence justification, exactly one of
which is correct under the document's controlling rules.
All organisations, people, products and places are invented.
Rationale comments in item files (# why:) are for auditing only and never
reach the rows.
"""


def C(key, instructions, state, options, gold, difficulty, twin=None, ordered=False):
    """Choice item. options: list of (option, justification)."""
    return dict(key=key, qtype="choice", role="choice", instructions=instructions,
                state=state.strip(), options=options, gold=gold,
                difficulty=difficulty, twin=twin, ordered=ordered)


def Y(key, instructions, state, card, gold, difficulty, twin=None, role="aff"):
    """Yes/no item (a two-option decision). card: list of (decision, justification). gold 1 = yes."""
    return dict(key=key, qtype="noul", role=role, instructions=instructions,
                state=state.strip(), card=card, gold=gold,
                difficulty=difficulty, twin=twin)


def T(edits, gold, instructions=None):
    """Minimal-pair twin: list of (old, new) replacements on the state."""
    return dict(edits=edits, gold=gold, instructions=instructions)

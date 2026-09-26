"""Helpers for the v0.12 hard 'reason_c' item author (procedural business
reasoning over documents: refunds and warranties, procurement and approvals,
HR leave and expenses, insurance claims, billing and credit). Each item gives a
policy or procedure excerpt (often with irrelevant distractor sections) plus a
case record; the gold needs multi-hop lookup, explicit date arithmetic,
thresholds, pro-rating and fees, precedence between conflicting sources, or
routing. All organisations, people, products and places are invented.
Rationale comments in item files (# why:) carry the full computation for
auditing only and never reach the rows.
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

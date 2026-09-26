"""Helpers for the v0.12 hard 'policy_c' item author (policy enforcement on
concrete cases: forum and microblog community standards, housing co-ops and
short-let platforms, schools and universities, workplace HR/IT policies, and
customer service desks). Multi-condition rules with exceptions, carve-outs,
thresholds, cumulative strikes and precedence between sections.
All platforms, organisations, people, products and places are invented.
Slurs are never written; case files mask them.
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

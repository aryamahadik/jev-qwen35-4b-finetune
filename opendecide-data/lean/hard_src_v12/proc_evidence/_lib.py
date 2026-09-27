"""Helpers for the v0.12 'proc_evidence' item author (evidence rules applied by
internal investigations, HR panels, claims teams and consumer dispute desks:
corroboration requirements, burden and standard of proof, recency windows,
source hierarchies, and conflicting records resolved by a stated rule).
Every item is a CHOICE whose options are decisions; the card gives each
decision a one-sentence justification, exactly one of which is correct under
the document's controlling rules. All people, organisations, products and
places are invented. Rationale comments in item files (# why:) are for
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

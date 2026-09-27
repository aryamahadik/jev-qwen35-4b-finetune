"""Helpers for the v0.12 'proc_adversarial' author: procedural decisions over
realistic operational documents (policies with amendments and definitions,
tickets, contracts, emails, pasted spreadsheets, meeting notes) that contain
PLANTED text trying to dictate the outcome. Planted text is balanced: in some
rows it pushes a wrong decision, in others it repeats the right one (always
twinned so the same planted line carries the opposite gold), so it is never a
cue. The correct decision always follows the controlling rules.
All people, organisations, products and places are invented.
Rationale comments in item files (# why:) are for auditing only and never
reach the rows. 'plant:' in a why-comment records whether the planted text
agrees with the base gold (right) or not (wrong).
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

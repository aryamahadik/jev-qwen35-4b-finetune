"""Helpers for the v0.12 HARD 'affect_c' item author (emotion in context:
customer-contact QA tagging, workplace comment coding, personal journals and
chats, an annotated dialogue corpus, and community/school settings).
The correct emotion depends on context, not keywords: sarcasm, whose emotion is
asked, stated primary-emotion rules, anticipatory vs retrospective emotions,
guilt/shame/embarrassment, jealousy/envy, disappointment/sadness, pride/gratitude.
All people, organisations, platforms, products and places are invented.
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

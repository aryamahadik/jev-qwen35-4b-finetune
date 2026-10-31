"""Item helper for the evidence_b hard-item author (invented statutes applied to facts).
Every item is hand-written by Claude (teacher); no external model is called."""


def it(key, qt, q, state, gold, card=None, opts=None, tpl=None, extra=None,
       diff=2, twin=None, twin_gold=None):
    """key: stable local key; qt: 'noul' or 'choice'; q: question text;
    card: explicit card text, or build it from tpl ('{}' = option) + extra overrides.
    twin: list of (old, new) replacements in state that flip the gold to twin_gold."""
    return dict(key=key, qtype=qt, q=q, state=state.strip("\n"), gold=gold, card=card,
                opts=opts, tpl=tpl, extra=extra or {}, diff=diff, twin=twin,
                twin_gold=twin_gold)

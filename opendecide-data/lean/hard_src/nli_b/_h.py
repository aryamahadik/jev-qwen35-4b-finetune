"""Item helper for the nli_b hard-item author (monotonicity, conditionals, modals, presuppositions).
Every item is hand-written by Claude (teacher); no external model or dataset is used."""

NONE = "none of these"

E, C, U = "entailed", "contradicted", "undetermined"
# three-way label sets in rotated orders (card lines are re-ordered to match by build.py)
L3 = [[E, C, U], [U, E, C], [C, U, E], [E, U, C], [U, C, E], [C, E, U]]
L3CARD = ("- entailed: if everything the passage says is true, the statement must be true\n"
          "- contradicted: if everything the passage says is true, the statement must be false\n"
          "- undetermined: the passage allows the statement to be true and also allows it to be false")

FOLLOW = ("- follows: a statement follows from a passage when it is true in every situation in which "
          "everything the passage says is true; ordinary word meanings count, outside facts and guesses about "
          "what is likely do not")
CONSIST = ("- consistent: a statement is consistent with a passage when it could be true without making "
           "anything the passage says false")
RULED = ("- ruled out: a statement is ruled out by a passage when it is false in every situation in which "
         "everything the passage says is true")


def it(key, qt, q, state, gold, card=None, opts=None, tpl=None, extra=None,
       diff=2, twin=None, twin_gold=None):
    """key: stable local key; qt: 'noul' or 'choice'; q: question text;
    card: explicit card text, or build it from tpl ('{}' = option) + extra overrides.
    twin: list of (old, new) replacements in state that flip the gold to twin_gold."""
    return dict(key=key, qtype=qt, q=q, state=state.strip("\n"), gold=gold, card=card,
                opts=opts, tpl=tpl, extra=extra or {}, diff=diff, twin=twin,
                twin_gold=twin_gold)

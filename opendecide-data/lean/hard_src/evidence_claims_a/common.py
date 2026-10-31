"""Shared cards and item constructors for the evidence_claims_a hard-item author.

Every item is hand-written by Claude (teacher); no external model or API is called.
Item dict keys: q, state, qtype, options, gold, diff, card, role, twin, shuffle.
twin = (subs, twin_gold) or (subs, twin_gold, twin_question); subs = [(old, new), ...]
applied to the state (each `old` must occur exactly once).
"""

LABELS = ["SUPPORTS", "REFUTES", "NOT ENOUGH INFO"]

DEF_S = ("- SUPPORTS: the evidence, read on its own and without outside knowledge, establishes "
         "every element of the claim: who or what, the figures, the dates or period, the scope "
         "words (all, most, some, only, never) and the degree of certainty. Simple arithmetic on "
         "figures and dates given in the evidence counts as reading it. Approximate wording in the "
         "claim (about, roughly, nearly) is met by a value within 5% of the stated figure. A claim "
         "stated as settled fact is not supported by evidence that is only tentative (may, might, "
         "suggests, preliminary, unconfirmed).")
DEF_R = ("- REFUTES: the evidence, read on its own, establishes that at least one element of the "
         "claim is false: a different figure or date, the opposite direction or polarity, an "
         "explicit denial, the wrong person, body or place, or a counterexample to a universal "
         "claim (all, every, never, none, only). Simple arithmetic on the evidence's own figures "
         "and dates counts as reading it.")
DEF_N = ("- NOT ENOUGH INFO: the evidence neither establishes the claim nor shows it to be false, "
         "for example because it is silent on an element of the claim, concerns a different "
         "population, place, product or period, reports only tentative or unconfirmed findings, "
         "or is compatible with the claim being either true or false.")

CARD3 = "\n".join([DEF_S, DEF_R, DEF_N])

MISMATCH_OPTS = ["number", "date", "scope", "certainty", "polarity", "entity", "no mismatch"]
CARD_MISMATCH = "\n".join([
    "- number: a figure, amount, count, percentage or ratio in the claim differs from what the evidence gives.",
    "- date: a date, year, duration or order of events in the claim conflicts with the evidence.",
    "- scope: a quantifier or coverage word in the claim (all, every, most, some, only, none) or the population or area it covers goes beyond or conflicts with the evidence.",
    "- certainty: the claim presents as established something that the evidence presents as possible, proposed, preliminary or unconfirmed.",
    "- polarity: the claim reverses the direction or truth of what the evidence says (rose vs fell, did vs did not, approved vs rejected).",
    "- entity: the claim attaches the fact to the wrong person, organisation, place, product or document.",
    "- no mismatch: the claim agrees with the evidence on every element.",
])


def _item(qtype, q, state, gold, diff, card, options=None, role=None, twin=None, shuffle=False):
    assert diff in (1, 2, 3)
    if role is None:
        role = "choice" if qtype == "choice" else "aff"
    return dict(q=q, state=state.strip(), qtype=qtype, options=options, gold=gold, diff=diff,
                card=card, role=role, twin=twin, shuffle=shuffle)


def Y(q, state, gold, diff, twin=None, role="aff", card=CARD3):
    """Yes/no item; gold 1 = yes."""
    assert gold in (0, 1)
    return _item("noul", q, state, gold, diff, card, None, role, twin)


def L(q, state, gold, diff, twin=None):
    """Three-way SUPPORTS / REFUTES / NOT ENOUGH INFO item (option order shuffled with seed)."""
    g = {"S": "SUPPORTS", "R": "REFUTES", "N": "NOT ENOUGH INFO"}
    gold = g.get(gold, gold)
    if twin:
        twin = (twin[0], g.get(twin[1], twin[1])) + tuple(twin[2:])
    return _item("choice", q, state, gold, diff, CARD3, list(LABELS), twin=twin, shuffle=True)


def M(q, state, gold, diff, twin=None):
    """Mismatch-type item (7 options)."""
    return _item("choice", q, state, gold, diff, CARD_MISMATCH, list(MISMATCH_OPTS), twin=twin)


def C(q, state, options, gold, diff, card, twin=None):
    return _item("choice", q, state, gold, diff, card, list(options), twin=twin)


def seq_card(prefix, n, what, none_def, label_defs):
    """Card for numbered sentence / paragraph / claim options."""
    lines = [f"- {prefix}{i}: {what.format(i=i)}" for i in n]
    lines.append(f"- none of these: {none_def}")
    return "\n".join(list(label_defs) + lines)


def sentence_opts(k):
    return [f"S{i}" for i in range(1, k + 1)] + ["none of these"]


def sentence_card(k, none_def, label_defs):
    lines = [f"- S{i}: the evidence sentence numbered [S{i}]" for i in range(1, k + 1)]
    lines.append(f"- none of these: {none_def}")
    return "\n".join(list(label_defs) + lines)


def para_opts(k):
    return [f"Paragraph {i}" for i in range(1, k + 1)] + ["none of these"]


def para_card(k, none_def, label_defs):
    lines = [f"- Paragraph {i}: the evidence paragraph numbered [{i}], judged on its own" for i in range(1, k + 1)]
    lines.append(f"- none of these: {none_def}")
    return "\n".join(list(label_defs) + lines)


def claim_opts(k):
    return [f"Claim {chr(65 + i)}" for i in range(k)] + ["none of these"]


def claim_card(k, none_def, label_defs):
    lines = [f"- Claim {chr(65 + i)}: the candidate claim labelled Claim {chr(65 + i)} in the item" for i in range(k)]
    lines.append(f"- none of these: {none_def}")
    return "\n".join(list(label_defs) + lines)


_AB = {"S": "SUPPORTS", "R": "REFUTES", "N": "NOT ENOUGH INFO"}


def combo_opts(n):
    import itertools
    return [", ".join(f"C{i + 1} {x}" for i, x in enumerate(t)) for t in itertools.product("SRN", repeat=n)]


def combo_card(n):
    import itertools
    lines = [DEF_S, DEF_R, DEF_N]
    for t in itertools.product("SRN", repeat=n):
        opt = ", ".join(f"C{i + 1} {x}" for i, x in enumerate(t))
        desc = ", ".join(f"claim C{i + 1} is {_AB[x]}" for i, x in enumerate(t))
        lines.append(f"- {opt}: {desc}")
    return "\n".join(lines)


def edit_card(edits, none_def):
    lines = [DEF_S, DEF_R, DEF_N]
    for i, e in enumerate(edits):
        lines.append(f"- Edit {chr(65 + i)}: {e}")
    lines.append(f"- none of these: {none_def}")
    return "\n".join(lines)


def edit_opts(k):
    return [f"Edit {chr(65 + i)}" for i in range(k)] + ["none of these"]

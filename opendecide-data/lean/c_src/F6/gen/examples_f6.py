"""Definition examples and few-shot blocks (repair r1; G0 s1 definition styles, s6 'Cards', C_DATA_SPEC 2.1 / 6;
F6-QC-8). Program-made from the card itself after the sealed commit:

- A definition example illustrates the card's reading rules (rows 4, 11/12, 20) on a one-fact file about the card's
  own quantity: a shown value settles a threshold condition, a marked value leaves it open (the value can be any
  whole value of its stated range). Example cards carry 1 or 2 examples; their golds alternate between settled and
  open, so they are balanced over the family.
- A few-shot block (yes/no cards only) holds 1-2 worked examples: the same one-fact file, a Q-DET question in the
  card's own frame and its answer as option text (Yes / No).
Every example is a one-fact file with no entity ID, so its structure hash lies outside every emitted row (G12), and
its text passes the 3.1 record scan (checked here). Examples are card-level: every row of the card shows the same
examples, so they never predict a row's label.
"""
from __future__ import annotations

from . import scan
from .common import rng_for


def _cmp_word(family: str) -> tuple[str, str]:
    return ("at least", ">=") if family == "incl" else ("more than", ">")


def _ok(text: str) -> bool:
    return not scan.banned_hits(text) and not scan.completeness_hits(text)


def quantity_of(card: dict):
    """(name, unit, lo, hi) of the card's first whole-number quantity, or None."""
    if card.get("P"):
        R_q = (card["P"].get("qty") or [])
        if R_q:
            q = R_q[0]
            return q["name"], q["unit"], max(q["lo"], 2), q["hi"]
    for c in card.get("cols") or []:
        if c.get("kind") == "num":
            return c["name"], c["unit"], c["lo"], c["hi"]
    for q in card.get("qs") or []:
        return q["name"], q["unit"], q["lo"], q["hi"]
    return None


def make(card: dict, marker: str, family: str, n_examples: int, fewshot: bool) -> tuple[list, list]:
    """(definition example sentences, few-shot sentences) for one card; deterministic per card."""
    q = quantity_of(card)
    if not q:
        return [], []
    name, unit, lo, hi = q
    if hi - lo < 6:
        return [], []
    rng = rng_for("examples", card["card_id"])
    word, op = _cmp_word(family)
    t = rng.randint(lo + 2, hi - 2)
    v = rng.randint(t + 1, hi) if op == ">" else rng.randint(t, hi)
    cap = name[:1].upper() + name[1:]
    settled = f"Example: a file showing '{cap}: {v} {unit}' meets a condition 'the {name} is {word} {t} {unit}'."
    open_ = (f"Example: a file showing '{cap}: {marker}' leaves a condition 'the {name} is {word} {t} {unit}' open, "
             f"because the {name} can be from {lo} to {hi} {unit}.")
    first_open = rng.random() < 0.5
    pair = [open_, settled] if first_open else [settled, open_]
    exs = pair[:n_examples]
    shots = []
    if fewshot:
        frame = f"Can it be determined whether the {name} is {word} {t} {unit}?"
        shots = [f"Worked example: a file showing '{cap}: {v} {unit}', asked '{frame}', gets the answer Yes.",
                 f"Worked example: a file showing '{cap}: {marker}', asked '{frame}', gets the answer No."]
        if rng.random() < 0.5:
            shots.reverse()
    for x in exs + shots:
        if not _ok(x.replace(marker, "")):
            return [], []
    return exs, shots


def card_flags(card_id: str, schema: str, defs_style: str, sampler: str) -> tuple[int, bool]:
    """(number of definition examples, few-shot) for a card: every non-short yes/no and C-GAP card shows 1-2
    definition examples (about half of all cards); 6 S3 / S4 yes/no cards (7.5%) also carry a few-shot block."""
    rng = rng_for("exflags", card_id)
    if defs_style != "one_line" or schema not in ("yn", "c_gap") or sampler == "S5":
        return 0, False
    n = 1 if rng.random() < 0.5 else 2
    few = schema == "yn" and sampler in ("S3", "S4") and card_id in FEWSHOT_CARDS
    return n, few


FEWSHOT_CARDS = {"F6-S3-yn-01", "F6-S3-yn-06", "F6-S3-yn-11", "F6-S4-yn-02", "F6-S4-yn-08", "F6-S4-yn-13"}

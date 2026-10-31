"""Yes/no unit planning shared by gate and match (1.6): polarity frames (rho, gold-blind), standalone negation (q),
twin units inside the card's rate r, yes counts apportioned over view x frame cells by largest remainder (R2-10),
decision-first base golds that absorb the twins' labels."""
from __future__ import annotations

import math

import common as C

RHO = 0.68       # bad-yes frame share (1.11 plan for p ~ 0.15; reported by the dry run)
Q_NEG = 0.10     # standalone negated base rows (R2-08)

# yes rows of a unit as (constant, coefficient of the base shown gold s)
YES = {"single": (0, 1), "negset": (1, 1), "contrast": (1, 0), "attack": (0, 2)}
ROWS = {"single": 1, "negset": 3, "contrast": 2, "attack": 2}


def largest_remainder(total: int, weights: dict, order: list) -> dict:
    s = sum(weights.values()) or 1
    raw = {k: total * w / s for k, w in weights.items()}
    out = {k: math.floor(v) for k, v in raw.items()}
    left = total - sum(out.values())
    for k in sorted(order, key=lambda k: (-(raw[k] - out[k]), order.index(k)))[:max(0, left)]:
        out[k] += 1
    return out


def plan(card_id: str, split: str, n_mo: int, diff_units: list[str], r: float, bad_frame: str, good_frame: str,
         rho: float = RHO, q_neg: float = Q_NEG) -> list[dict]:
    """diff_units: kinds of the diff-view units (twin kinds + 'single'); message-only units are singles.
    Returns units with view, frame, k (base), kind, s (base shown gold)."""
    units = []
    for view, kinds in (("message_only", ["single"] * n_mo), ("message_diff", diff_units)):
        slots = sorted(range(len(kinds)), key=lambda i: C.h01("frame", card_id, split, view, i))
        n_bad = round(rho * len(kinds))
        bad = set(slots[:n_bad])
        for i, kind in enumerate(kinds):
            neg = kind == "single" and C.h01("neg", card_id, split, view, i) < q_neg
            units.append({"view": view, "frame": bad_frame if i in bad else good_frame, "k": 1 if neg else 0,
                          "kind": kind, "slot": i})
    n_rows = sum(ROWS[u["kind"]] for u in units)
    target = round(r * n_rows)
    cells = {}
    for u in units:
        cells.setdefault((u["view"], u["frame"]), []).append(u)
    order = sorted(cells, key=lambda c: (c[0] != "message_only", c[1] != bad_frame))
    w = {c: sum(ROWS[u["kind"]] for u in cells[c]) for c in cells}
    tgt = largest_remainder(target, w, order)
    for c, us in cells.items():
        need = tgt[c] - sum(YES[u["kind"]][0] for u in us)
        us_sorted = sorted(us, key=lambda u: C.h01("s", card_id, split, c, u["slot"], u["kind"]))
        for u in us_sorted:
            u["s"] = 0
        for u in us_sorted:
            if YES[u["kind"]][1] == 2 and need >= 2:
                u["s"], need = 1, need - 2
        for u in us_sorted:
            if YES[u["kind"]][1] == 1 and need >= 1:
                u["s"], need = 1, need - 1
        for u in us_sorted:
            if YES[u["kind"]][1] == 0:
                u["s"] = int(C.h01("cs", card_id, split, u["slot"]) < 0.5)
    return units


def truth_for(s: int, frame: str, k: int, pos_frame: str) -> bool:
    """Underlying truth (gate: holds; match: describes) giving shown gold s in `frame` with k counted negations.
    pos_frame is the frame whose affirmative yes equals the truth (gate 'hold', match 'describes')."""
    v = bool(s) ^ bool(k % 2)
    return v if frame == pos_frame else not v


def shown(truth: bool, frame: str, k: int, pos_frame: str) -> int:
    v = truth if frame == pos_frame else not truth
    return int(v) ^ (k % 2)

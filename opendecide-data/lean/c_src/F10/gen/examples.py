"""In-definition examples (AR02) and few-shot worked examples (R2-07). An in-definition example is a one-line
description that states every attribute its label depends on: under every value of its unstated attributes it meets
the definition it illustrates and no other term definition on the card (helpers excluded). Built from solver B
regions on the hidden card; G3 re-checks each one from the parse."""
from __future__ import annotations

import model as M
from solver_b import CardB
from values import val_text

NUM = ("count", "qty", "amount")


def _point_in(box, legend, r, draw):
    """A concrete case inside box (slot values); relative axes handled by fixing e then x = e + d."""
    case = {}
    pairs = [ax for ax in box if isinstance(ax, tuple)]
    for s, a in legend.items():
        c = box.get(s)
        t = a["type"]
        if t in NUM or t == "date":
            lo, hi = (c[1], c[2]) if c else (None, None)
            dl, dh = draw.get(s, (0, 100))
            lo2 = dl if lo is None else max(lo, dl) if (hi is None or max(lo, dl) <= hi) else lo
            hi2 = dh if hi is None else min(hi, dh) if min(hi, dh) >= lo2 else hi
            if lo2 > hi2:
                lo2, hi2 = (lo, lo) if lo is not None else (hi, hi)
            case[s] = r.randint(lo2, hi2)
        elif t in ("cat", "flag"):
            vals = sorted(c[1], key=str) if c else (a["values"] if t == "cat" else [True, False])
            case[s] = r.choice(list(vals))
        elif t == "tag":
            vals = sorted(c[1]) if c else [()]
            case[s] = tuple(r.choice(vals)) if c else tuple()
    for ax in pairs:
        _, x, e = ax
        lo, hi = box[ax][1], box[ax][2]
        if lo is None and hi is None:
            lo, hi = -60, 60
        elif lo is None:
            lo = hi - 60
        elif hi is None:
            hi = lo + 60
        d = r.randint(lo, min(hi, lo + 90))
        case[x] = case[e] + d
    return case


def example_for(card, cb: CardB, did, r, draw, tries=40):
    """(stated slots, case) or None: a minimal one-line description meeting did and no other term definition."""
    sp = cb.sp
    T = cb.region(did)
    for t in card["order"]:
        if t != did:
            T = sp.minus(T, cb.region(t))
    if not T:
        return None
    for _ in range(tries):
        box = r.choice(T)
        case = _point_in(box, card["legend"], r, draw)
        if not sp.box_in(sp.point_box(case), T):
            continue
        slots = list(card["legend"])
        r.shuffle(slots)
        stated = set(slots)
        for s in slots:
            trial = stated - {s}
            om = [x for x in card["legend"] if x not in trial]
            if sp.box_in(sp.point_box(case, om), T):
                stated = trial
        if stated:
            return sorted(stated), case
    return None


def one_line(card, stated, case):
    leg = card["legend"]
    pairs = [f"{leg[s]['name']} {val_text(leg[s], case[s], card)}" for s in sorted(stated)]
    return f"a {card['entity']} with " + ", ".join(pairs)

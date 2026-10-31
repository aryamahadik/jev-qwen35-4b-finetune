"""Value formatting for F10 renders (definitions, legend, records, examples). Numbers: no thousands separators,
'.' decimal mark (AR08); amounts with 0 or 2 decimals; quantities with at most d decimals; dates in the card's one
format (ST23). Grid units: numeric value x 10^d (amount d = 2); dates are ordinals."""
from __future__ import annotations

import datetime as dt
from decimal import Decimal

from lexicon import MONTHS


def num_text(g: int, d: int, amount=False) -> str:
    if d == 0:
        return str(g)
    q = Decimal(g) / (Decimal(10) ** d)
    if amount:
        return str(int(q)) if g % 100 == 0 else f"{q:.2f}"
    s = f"{q:.{d}f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s


def unit_word(a, plural=True):
    if a["type"] == "amount":
        return a.get("currency") or "dollars"
    return a.get("unit") or ""


def val_text(a, g, card=None, conv_u1=False) -> str:
    """Text of one value of attribute a (grid units / ordinal / str / bool / tuple)."""
    t = a["type"]
    if t in ("count", "qty", "amount"):
        if conv_u1:
            k = a["conv"]["k"]
            q = Decimal(g) / (Decimal(10) ** a["d"]) / Decimal(k)
            s = format(q.normalize(), "f")
            return f"{s} {a['conv']['u1']}"
        s = num_text(g, a["d"], amount=(t == "amount"))
        u = unit_word(a)
        return f"{s} {u}".strip()
    if t == "date":
        return date_text(g, card["rc"]["date_fmt"] if card else "iso")
    if t == "cat":
        return str(g)
    if t == "flag":
        return "yes" if g else "no"
    if t == "tag":
        return ", ".join(g) if g else "none"
    raise ValueError(t)


def date_text(o: int, fmt: str) -> str:
    d = dt.date.fromordinal(o)
    if fmt == "iso":
        return d.isoformat()
    if fmt == "dmy":
        return f"{d.day} {MONTHS[d.month - 1]} {d.year}"
    return f"{MONTHS[d.month - 1]} {d.day}, {d.year}"


def u1_ok(a, g) -> bool:
    """A value can be written in the larger unit U1 only if value / k needs at most d + 3 decimals (AR28)."""
    if not a.get("conv"):
        return False
    q = Decimal(g) / (Decimal(10) ** a["d"]) / Decimal(a["conv"]["k"])
    s = format(q.normalize(), "f")
    dec = len(s.split(".")[1]) if "." in s else 0
    return dec <= a["d"] + 3 and q > 0


def list_text(vals) -> str:
    return ", ".join(str(v) for v in vals)

"""Number texts for the renderer (G0 spec 2 'Representation of each stated chance', 8 threshold grid).

Chances: pct0 '35%', pct1 '35.5%', dec '0.35', frac '7/20', ain '7 in 20', aoutof '7 out of 20'.
Money: whole major units with thousands separators, then the pack's unit word ('4,250 USD', '1 brasslet').
Scores and points: integers. Every input is an int or a Fraction; a value with no exact text raises.
"""
from __future__ import annotations

from fractions import Fraction as Fr


class NoExactText(ValueError):
    pass


def group(n: int) -> str:
    s = f"{abs(n):,}"
    return ("-" if n < 0 else "") + s


def chance_text(p: Fr, rep: str, denom: int | None = None) -> str:
    p = Fr(p)
    if p < 0 or p > 1:
        raise NoExactText("chance outside [0, 1]")
    if rep == "pct0":
        v = p * 100
        if v.denominator != 1:
            raise NoExactText("pct0")
        return f"{v.numerator}%"
    if rep == "pct1":
        v = p * 1000
        if v.denominator != 1:
            raise NoExactText("pct1")
        k = v.numerator
        if k % 10 == 0:
            return f"{k // 10}%"
        return f"{k // 10}.{k % 10}%"
    if rep == "dec":
        for places in (1, 2, 3):
            v = p * 10 ** places
            if v.denominator == 1:
                k = v.numerator
                if p == 1:
                    return "1"
                if k == 0:
                    return "0"
                return "0." + str(k).rjust(places, "0")
        raise NoExactText("dec")
    if rep in ("frac", "ain", "aoutof"):
        b = denom or p.denominator
        a = p * b
        if a.denominator != 1:
            raise NoExactText(rep)
        a = a.numerator
        if rep == "frac":
            return f"{a}/{b}"
        if rep == "ain":
            return f"{a} in {b}"
        return f"{a} out of {b}"
    raise NoExactText(f"unknown rep {rep}")


def has_text(p: Fr, rep: str, denom: int | None = None) -> bool:
    try:
        chance_text(p, rep, denom)
        return True
    except NoExactText:
        return False


def money_text(v: Fr, cur: dict) -> str:
    v = Fr(v)
    if v.denominator != 1:
        raise NoExactText("money not whole")
    n = v.numerator
    unit = cur["plural"]
    if abs(n) == 1 and cur.get("singular"):
        unit = cur["singular"]
    return f"{group(n)} {unit}"


def points_text(k: int) -> str:
    return (f"+{k}" if k > 0 else str(k)) + (" point" if abs(k) == 1 else " points")


def num_text(v: Fr) -> str:
    """Plain decimal text for expected numbers and other non-chance, non-money quantities ('3', '3.5')."""
    v = Fr(v)
    if v.denominator == 1:
        return group(v.numerator)
    for places in (1, 2):
        w = v * 10 ** places
        if w.denominator == 1:
            k = abs(w.numerator)
            s = f"{k // 10 ** places:,}.{str(k % 10 ** places).rjust(places, '0')}"
            return ("-" if v < 0 else "") + s
    raise NoExactText("num")

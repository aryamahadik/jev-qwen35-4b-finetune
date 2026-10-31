"""Re-solver for S5 statements: the money re-solver on the statement's lines and steps, the printed-line check
(printed amount == quantity x rate, exactly), and the settlement date on day ordinals."""
from __future__ import annotations

from .solve_b import Q, mul, cmp, money_value, _cmpq
from . import solve_b_date as SD


def check_printed(P):
    for ln in P["lines"]:
        if ln.get("mark") == "printed":
            if cmp(Q(P["vals"][ln["a"]]), mul(Q(P["vals"][ln["q"]]), Q(P["vals"][ln["r"]]))) != 0:
                raise ValueError("printed line amount differs from quantity x rate")


def solve_stmt(P, options=None, names=None):
    check_printed(P)
    q = P["q"]
    Pm = {**P, "eng": "money"}
    if q["kind"] == "settle":
        st = P["settle"]
        hol = {SD.iso_to_n(h) for h in st["holidays"]}
        n = SD.roll(SD.iso_to_n(st["per"]) + st["N"], st["D7"], hol)
        return ("date", SD.n_to_iso(n))
    if q["kind"] == "thr":
        v = money_value(Pm, norround=(P.get("sem", {}).get("R3") == "unrounded"))
        aff = _cmpq(v, q["cmp"], Q(q["T"]))
        return ("yn", aff if q.get("neg", 0) % 2 == 0 else not aff)
    return ("value", money_value(Pm))

"""Re-solver (integers only) for the band (S3), date (S4) and statement (S5) engines. Bands: cumulative closed form
(charge at the band start + one partial band). Dates: day ordinals from a civil-to-days formula; business days in
closed form. No decimal / fractions / datetime / calendar import (3.2)."""
from __future__ import annotations

from .solve_b import Q, add, sub, mul, div, cmp, lt, le, mn, mx, round_to, ZERO, HUND, floor_int


def _locate(v, bands, b1):
    for i, b in enumerate(bands):
        lo = None if b["lo"] is None else Q(b["lo"])
        hi = None if b["hi"] is None else Q(b["hi"])
        if b1 == "upper":
            ok = (lo is None or lt(lo, v)) and (hi is None or le(v, hi))
        else:
            ok = (lo is None or le(lo, v)) and (hi is None or lt(v, hi))
        if ok:
            return i
    raise ValueError("no band")


def band_amount(P, vals):
    a = P["amt"]
    if a["kind"] == "stated":
        return Q(vals[a["a"]])
    return mul(Q(vals[a["q"]]), Q(vals[a["p"]]))


def band_charge(P, vals, facts, norround=False):
    sem = P.get("sem", {})
    v = band_amount(P, vals)
    bands = P["bands"]
    b1, b2 = sem.get("B1", "upper"), sem.get("B2", "flat")
    k = _locate(v, bands, b1)
    rk = P["rate_kind"]

    def rate_part(width, r):
        return div(mul(width, r), HUND) if rk == "pct" else mul(width, r)
    if b2 == "flat":
        x = P.get("x10")
        if x and facts.get(x["f"]) == "not recorded":
            raise LookupError(x["f"])
        if x and facts.get(x["f"]) == x["v"]:
            k = max(k - 1, 0)
        r = Q(bands[k]["rate"])
        c = r if rk == "flat" else rate_part(v, r)
    else:
        # cumulative: full widths of every band below band k, then the part of band k
        c = ZERO
        for i in range(k):
            lo = Q(bands[i]["lo"]) if bands[i]["lo"] is not None else ZERO
            c = add(c, rate_part(sub(Q(bands[i]["hi"]), lo), Q(bands[i]["rate"])))
        lo = Q(bands[k]["lo"]) if bands[k]["lo"] is not None else ZERO
        c = add(c, rate_part(sub(v, lo), Q(bands[k]["rate"])))
    if P.get("fee"):
        c = add(c, Q(vals[P["fee"]]))
    for st in P.get("steps", []):
        lim = Q(vals[st["v"]])
        c = mx(c, lim) if st["op"] == "min" else mn(c, lim)
    if sem.get("R1") and not norround:
        c = round_to(c, Q(sem["R1u"]), sem["R1"])
    return c


def _cmpq(v, op, T):
    k = cmp(v, T)
    return {"ge": k >= 0, "gt": k > 0, "le": k <= 0, "lt": k < 0}[op]


def solve_band(P, options, names):
    q = P["q"]
    vals, facts = P["vals"], P.get("facts", {})
    nr = P.get("sem", {}).get("R3") == "unrounded"
    if P.get("world") == "open":
        unk = [k for k, v in facts.items() if v == "not recorded"]
        f = unk[0]
        dom = P["cats"][f]
        labs = set()
        for x in dom:
            c = band_charge(P, vals, {**facts, f: x})
            labs.add(c)
        if len(labs) >= 2:
            return ("nei", None)
        return ("value", labs.pop())
    if q["kind"] == "thr":
        aff = _cmpq(band_charge(P, vals, facts, nr), q["cmp"], Q(q["T"]))
        return ("yn", aff if q.get("neg", 0) % 2 == 0 else not aff)
    if q["kind"] == "value":
        return ("value", band_charge(P, vals, facts))
    if q["kind"] == "band":
        k = _locate(band_amount(P, vals), P["bands"], P["sem"].get("B1", "upper"))
        return ("outcome", names[k] if names else P["bands"][k]["name"])
    if q["kind"] == "cases":
        hits = []
        for i, c in enumerate(q["cases"]):
            v = band_charge(P, {**vals, **c["vals"]}, {**facts, **c["facts"]}, nr)
            if _cmpq(v, q["cmp"], Q(q["T"])):
                hits.append(i)
        return ("cases", hits)
    raise ValueError(q["kind"])


def solve(P, options=None, names=None):
    if P["eng"] == "band":
        return solve_band(P, options, names)
    from .solve_b_date import solve_date
    return solve_date(P, options, names)

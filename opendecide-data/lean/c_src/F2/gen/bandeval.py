"""Solver A for S3 tiered tables: Decimal, bands walked one by one (3.1, S3).

LP (band): amt {kind: stated, a} | {kind: mul, q, p}; bands [{name, lo, hi, rate}] in edge order (shared edges);
rate_kind pct | unit | flat; sem B1 (upper | lower), B2 (flat | marginal), R1/R1u/R3, X4; steps min/cap on the charge;
x10 {f, v} (flat mode only): that category pays the rate of the next-lower band.
"""
from __future__ import annotations

from decimal import Decimal, localcontext

from .common import D, ZERO, HUNDRED, quant
from .money import Reject, Tr


def locate(v, bands, b1):
    for i, b in enumerate(bands):
        lo = None if b.get("lo") is None else D(b["lo"])
        hi = None if b.get("hi") is None else D(b["hi"])
        if b1 == "upper":
            ok = (lo is None or v > lo) and (hi is None or v <= hi)
        else:
            ok = (lo is None or v >= lo) and (hi is None or v < hi)
        if ok:
            return i
    raise Reject("no band")


def amount(LP, tr):
    a = LP["amt"]
    vals = LP["vals"]
    if a["kind"] == "stated":
        return D(vals[a["a"]])
    return tr.op("amount", D(vals[a["q"]]) * D(vals[a["p"]]))


def evaluate(LP, rd=None):
    rd = rd or {}
    sem = {**LP.get("sem", {}), **rd.get("sem", {})}
    err = rd.get("err")
    tr = Tr()
    v = amount(LP, tr)
    tr.vals_at["amount"] = v
    bands = LP["bands"]
    b1, b2 = sem.get("B1", "upper"), sem.get("B2", "flat")
    idx = locate(v, bands, b1)
    tr.vals_at["band"] = idx
    tr.sel += 1
    if err == "E-tier-":
        if idx == 0:
            raise Reject("no lower band")
        idx -= 1
    elif err == "E-tier+":
        if idx == len(bands) - 1:
            raise Reject("no higher band")
        idx += 1
    rk = LP["rate_kind"]
    x10 = LP.get("x10")
    if x10 and b2 == "flat" and err != "E-exc" and LP["facts"].get(x10["f"]) == x10["v"]:
        if LP["facts"].get(x10["f"]) == "not recorded":
            raise Reject("unknown")
        if idx > 0:
            tr.flags.add("bind:exc")
        idx = max(idx - 1, 0)
        tr.sel += 1
    if b2 == "flat":
        r = D(bands[idx]["rate"])
        if rk == "pct":
            c = tr.op("charge", v * r / HUNDRED)
        elif rk == "unit":
            c = tr.op("charge", v * r)
        else:
            c = r
    else:
        if rk == "flat":
            raise Reject("marginal flat-fee table")
        c = None
        parts = []
        for i, b in enumerate(bands):
            lo = D(b["lo"]) if b.get("lo") is not None else ZERO
            hi = None if b.get("hi") is None else D(b["hi"])
            if v <= lo:
                break
            top = v if hi is None or v < hi else hi
            if lo > 0:
                part = tr.op(f"part{i}", top - lo)
            else:
                part = top
            r = D(b["rate"])
            pc = tr.op(f"bandcharge{i}", part * r / HUNDRED if rk == "pct" else part * r)
            parts.append(pc)
            c = pc if c is None else tr.op(f"sum{i}", c + pc)
        if c is None:
            c = ZERO
    if LP.get("fee"):
        c = tr.op("fee_add", c + D(LP["vals"][LP["fee"]]))
    for st in LP.get("steps", []):
        if st["op"] == "min" and err != "E-floor":
            if c < D(LP["vals"][st["v"]]):
                tr.flags.add("bind:floor")
            c = max(c, D(LP["vals"][st["v"]]))
            tr.sel += 1
        if st["op"] == "cap" and err != "E-cap":
            if c > D(LP["vals"][st["v"]]):
                tr.flags.add("bind:cap")
            c = min(c, D(LP["vals"][st["v"]]))
            tr.sel += 1
    tr.unrounded = c
    r1 = None if rd.get("norround") else sem.get("R1")
    if r1:
        c2 = quant(c, D(sem["R1u"]), r1)
        if c2 != c:
            tr.flags.add("bind:round")
        c = c2
        tr.sel += 1
    tr.final = c
    return c, tr


def band_of(LP, rd=None):
    rd = rd or {}
    sem = {**LP.get("sem", {}), **rd.get("sem", {})}
    tr = Tr()
    v = amount(LP, tr)
    return LP["bands"][locate(v, LP["bands"], sem.get("B1", "upper"))]["name"]


def compared(LP, rd=None):
    rd = rd or {}
    sem = {**LP.get("sem", {}), **rd.get("sem", {})}
    if sem.get("R3") == "unrounded":
        return evaluate(LP, {**rd, "norround": True})[0]
    return evaluate(LP, rd)[0]


CMP = {"ge": lambda a, b: a >= b, "gt": lambda a, b: a > b, "le": lambda a, b: a <= b, "lt": lambda a, b: a < b}


def aff(LP, rd=None):
    q = LP["q"]
    return CMP[q["cmp"]](compared(LP, rd), D(q["T"]))

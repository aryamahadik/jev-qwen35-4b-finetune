"""Parser part for S5 statements: the statement container (description | quantity | rate | amount), M3 blank amounts
with "none" quantity and rate cells (SC19), M4 computed cells, B4, the deduction rule, R1 / R2, D17 settlement."""
from __future__ import annotations

import re
from decimal import Decimal

from . import lex
from . import parse as _p
from .parse_doc import norm_key
from .parse_date import parse_date

D = Decimal


def tpls():
    T = [("STMT", lex.STMT_INTRO), ("M3", lex.M3), ("M4", lex.M4), ("B4", lex.B4), ("GROSS", lex.GROSS),
         ("NET_DED", lex.NET_DED), ("NET_NODED", lex.NET_NODED), ("R2S", lex.R2_STMT_LINE)]
    T += [(f"PCTDED:{k}", v) for k, v in lex.PCTDED.items()]
    T += [(f"X4S:{k}", v) for k, v in lex.X4_STMT.items()]
    return T


def question(row, q):
    if row["qtype"] == "noul":
        return _p.parse_thr_question(q, None)
    for tpl in lex.Q_SETTLE:
        m = lex.compile_tpl(tpl, anchored=True).match(q)
        if m:
            return {"kind": "settle", "id": m.group("id")}
    return _p.parse_choice_question(q)


def _list(s):
    parts = re.split(r", | and ", s.strip())
    return [p.strip() for p in parts if p.strip()]


def parse(row, doc, M, qinfo, ctext):
    g = {}
    for x in M:
        g.setdefault(x[0], []).append(x[1])
    for need in ("W0", "W1", "STMT", "M3", "M4", "GROSS", "D17", "D6A"):
        if need not in g:
            raise _p.PErr(f"statement card misses {need}")
    seen = []
    gross = g["GROSS"][0]["gross"]
    types = _list(g["GROSS"][0]["types"])
    b4 = g.get("B4", [None])[0]
    tab = None
    for cols, rows, cap in doc.tables:
        if [norm_key(c) for c in cols] == ["description", "quantity", "rate", "amount"]:
            tab = rows
    if tab is None:
        raise _p.PErr("statement table")
    byd = {r[0].strip(): r for r in tab}
    vals, lines, marks = {}, [], []
    for desc in types:
        r = byd.get(desc)
        if r is None:
            raise _p.PErr("earning line missing")
        q, rate, amt = (x.strip() for x in r[1:])
        ql, rl, al = f"{desc} quantity", f"{desc} rate", f"{desc} amount"
        if amt == "":
            if q != "none" or rate != "none":
                raise _p.PErr("blank amount on a line with a quantity or rate (R1-01, SC19)")
            lines.append({"p": "blank", "mark": "blank"})
            marks.append("blank")
            continue
        if q in ("", "0") or rate in ("", "0"):
            raise _p.PErr("blank or 0 quantity / rate cell")
        vals[ql] = _p.num_lead(q)
        vals[rl] = _p.money_val(rate, None, seen)[0]
        if amt == lex.COMPUTED_MARK:
            if b4 and b4["type"] == desc:
                vals["B4 threshold"] = D(b4["X"])
                vals["B4 multiplier"] = D(b4["m"])
                lines.append({"p": "b4", "q": ql, "r": rl, "b4x": "B4 threshold", "b4m": "B4 multiplier", "mark": "computed"})
            else:
                lines.append({"p": "mul", "q": ql, "r": rl, "mark": "computed"})
            marks.append("computed")
        else:
            vals[al] = _p.money_val(amt, None, seen)[0]
            lines.append({"p": "stated", "a": al, "q": ql, "r": rl, "mark": "printed"})
            marks.append("printed")
    pk = [k for k in g if k.startswith("PCTDED:")]
    if len(pk) != 1:
        raise _p.PErr("deduction rule")
    lim_kind = pk[0].split(":")[1]
    pdx = g[pk[0]][0]
    if pdx["gross"] != gross:
        raise _p.PErr("deduction base")
    vals[pdx["pct"]] = _p.pct_val(doc.get(pdx["pct"]) or "")
    vals[pdx["lim"]] = _p.money_val(doc.get(pdx["lim"]) or "", None, seen)[0]
    steps = [{"op": "pctded", "id": "pctded", "v": [pdx["pct"], pdx["lim"]], "lim": lim_kind, "scope": "total"}]
    if "NET_DED" in g:
        deds = _list(g["NET_DED"][0]["deds"])
        dl = []
        for dd in deds:
            r = byd.get(dd)
            if r is None or r[1].strip() != "none" or r[2].strip() != "none":
                raise _p.PErr("deduction line")
            vals[f"{dd} amount"] = _p.money_val(r[3], None, seen)[0]
            dl.append(f"{dd} amount")
        steps.append({"op": "ded", "id": "ded", "v": dl})
    sem = {"X4": {"pctded": "total"}}
    for x in M:
        k = x[0]
        if k.startswith("R1:"):
            sem["R1"] = k.split(":")[1]
            sem["R1u"] = _p.money_val(x[1]["u"])[0]
        elif k == "R2:final":
            sem["R2"] = "final"
        elif k == "R2S":
            sem["R2"] = "line"
        elif k.startswith("R3:"):
            sem["R3"] = k.split(":")[1]
    d7 = [k.split(":")[1] for k in g if k.startswith("D7:")]
    if len(d7) != 1:
        raise _p.PErr("D17 needs its roll rule (R4-09)")
    per_l = g["D17"][0]["per"]
    per, wd = parse_date(doc.get(per_l) or "")
    hv = doc.get(lex.HOL_NOTE)
    if hv is None:
        raise _p.PErr("holiday line (R3-23)")
    hol = [] if hv.strip() == "none" else [parse_date(x)[0] for x in hv.split("; ")]
    curs = {s[4:] for s in seen if s.startswith("CUR:")}
    if len(curs) > 1:
        raise _p.PErr("currency differs")
    nums = [s for s in seen if not s.startswith("CUR:")]
    LP = {"eng": "stmt", "world": "closed", "unit": D("0.01") if any("." in s for s in nums) else D(1), "vals": vals,
          "facts": {}, "lines": lines, "steps": steps, "excs": [], "sem": sem, "target": "final",
          "settle": {"N": int(g["D17"][0]["N"]), "D7": d7[0], "per_date": per, "holidays": hol}, "marks": marks,
          "_cur": curs.pop() if curs else None}
    k = qinfo["kind"]
    if k == "thr":
        LP["q"] = {"kind": "thr", "cmp": qinfo["op"], "T": qinfo["T"], "neg": qinfo["neg"]}
    elif k == "value":
        LP["q"] = {"kind": "value"}
    elif k == "settle":
        LP["q"] = {"kind": "settle"}
    else:
        raise _p.PErr("statement question")
    return LP

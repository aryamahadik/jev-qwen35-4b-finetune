"""Parser parts for the band (S3), date (S4) and statement (S5) engines; template registry for all engines."""
from __future__ import annotations

import re
from decimal import Decimal

from . import lex
from . import parse as _p
from .parse_doc import norm_key

D = Decimal


def _band_tpls():
    T = [("BT_INTRO", lex.BT_INTRO)]
    T += [(f"B2:{k}", v) for k, v in lex.B2.items()]
    T += [(f"RATE:{k}", v) for k, v in lex.RATE_KIND.items()]
    T += [("BAND_CHARGE", lex.BAND_CHARGE), ("X10", lex.X10)]
    return T


MARKERS = [("STMT", lex.STMT_INTRO), ("BT_INTRO", lex.BT_INTRO), ("D1", lex.D1)]


def engine_and_tpls(text):
    """Engine from its marker sentence, then that engine's template list in priority order."""
    from . import parse_date, parse_stmt
    found = {x[0] for x in _p.scan(text, MARKERS)}
    if "STMT" in found:
        return "stmt", parse_stmt.tpls() + parse_date.tpls() + _p._tpls_money()
    if "BT_INTRO" in found:
        return "band", _band_tpls() + _p._tpls_money()
    if "D1" in found:
        return "date", parse_date.tpls() + _p._tpls_money()
    return "money", _p._tpls_money()


def all_tpls():
    from . import parse_date, parse_stmt
    return parse_stmt.tpls() + _band_tpls() + parse_date.tpls() + _p._tpls_money()


def parse_question(eng, row, q):
    if eng == "band":
        return band_question(row, q)
    from . import parse_date
    return parse_date.question(eng, row, q)


def parse(eng, row, doc, M, qinfo, ctext):
    if eng == "band":
        return parse_band(row, doc, M, qinfo, ctext)
    from . import parse_date
    return parse_date.parse(eng, row, doc, M, qinfo, ctext)


# ----------------------------------------------------------------------------------------------------------------- bands

def band_question(row, q):
    if row["qtype"] == "noul":
        return _p.parse_thr_question(q, None)
    for tpl in lex.Q_BAND:
        m = lex.compile_tpl(tpl, anchored=True).match(q)
        if m:
            return {"kind": "band", "amt": m.group("amt"), "id": m.group("id")}
    return _p.parse_choice_question(q)


def _band_table(doc):
    for cols, rows, cap in doc.tables:
        nk = [norm_key(c) for c in cols]
        if nk == ["band", "lower edge", "upper edge", "rate"]:
            return rows
    raise _p.PErr("band table not found")


def parse_band(row, doc, M, qinfo, ctext):
    g = {}
    for x in M:
        g.setdefault(x[0], []).append(x[1])
    if "W0" not in g or (("W1" in g) == ("W2" in g)) or "BT_INTRO" not in g:
        raise _p.PErr("band card frame")
    world = "open" if "W2" in g else "closed"
    seen = []
    sem = {}
    for k in g:
        if k.startswith("B1:"):
            sem["B1"] = k.split(":")[1]
        if k.startswith("B2:"):
            sem["B2"] = k.split(":")[1]
    if "B1" not in sem or "B2" not in sem:
        raise _p.PErr("band forms")
    rk = [k.split(":")[1] for k in g if k.startswith("RATE:")]
    if len(rk) != 1:
        raise _p.PErr("rate kind")
    rk = rk[0]
    bc = g["BAND_CHARGE"][0]
    charge, amt = bc["charge"], bc["amt"]
    LP = {"eng": "band", "world": world, "rate_kind": rk, "vals": {}, "facts": {}, "steps": [], "x10": None}
    case_cols = set()
    if qinfo["kind"] == "cases":
        for cols, rows_, cap in doc.tables:
            if rows_ and any(r[0] in (row.get("options") or []) for r in rows_):
                case_cols = {norm_key(c) for c in cols[1:]}
                case_tab = (cols, rows_)
    count = False

    def money_or_num(lbl):
        if norm_key(lbl) in case_cols:
            return None
        v = doc.get(lbl)
        if v is None:
            raise _p.PErr(f"no value for {lbl!r}")
        if _p.MONEY_RX.match(v.strip()):
            return _p.money_val(v, None, seen)[0]
        return _p.num_lead(v)

    if "F_MUL" in g:
        mm = g["F_MUL"][0]
        if mm["lc"] != amt:
            raise _p.PErr("amount definition names another amount")
        LP["amt"] = {"kind": "mul", "q": mm["q"], "p": mm["r"]}
        for lb in (mm["q"], mm["r"]):
            v = money_or_num(lb)
            if v is not None:
                LP["vals"][lb] = v
    else:
        LP["amt"] = {"kind": "stated", "a": amt}
        v = money_or_num(amt)
        if v is not None:
            LP["vals"][amt] = v
    rows = _band_table(doc)
    bands = []
    for r in rows:
        name, lo, hi, rate = [x.strip() for x in r]
        if rk == "pct":
            rv = _p.pct_val(rate)
        else:
            rv = _p.money_val(rate, None, seen)[0]
        bands.append({"name": name, "lo": D(lo) if lo else None, "hi": D(hi) if hi else None, "rate": rv})
    if bands[0]["lo"] is not None or bands[-1]["hi"] is not None:
        raise _p.PErr("band table end edges must be blank (B1)")
    for a, b in zip(bands, bands[1:]):
        if a["hi"] is None or b["lo"] is None or a["hi"] != b["lo"]:
            raise _p.PErr("adjacent bands do not share edges (R3-06)")
    LP["bands"] = bands
    for x in M:
        if x[0] == "X10":
            xx = x[1]
            LP["x10"] = {"f": xx["f"], "v": xx["v"]}
            if norm_key(xx["f"]) not in case_cols:
                raw = doc.get(xx["f"])
                if raw is None:
                    raise _p.PErr("X10 field missing")
                LP["facts"][xx["f"]] = raw.strip()
        elif x[0] == "F_ADD":
            xx = x[1]
            if xx["base"] != charge:
                raise _p.PErr("fee on another amount")
            LP["fee"] = xx["fixed"]
            LP["vals"][xx["fixed"]] = _p.money_val(doc.get(xx["fixed"]) or "", None, seen)[0]
            fee_tot = xx["tot"]
        elif x[0] in ("F_MIN", "F_CAP"):
            xx = x[1]
            op = "min" if x[0] == "F_MIN" else "cap"
            lim = xx["min"] if op == "min" else xx["cap"]
            if xx["base"] not in (charge, locals().get("fee_tot")):
                raise _p.PErr("limit on another amount")
            LP["vals"][lim] = _p.money_val(doc.get(lim) or "", None, seen)[0]
            LP["steps"].append({"op": op, "id": op, "v": lim, "scope": None})
        elif x[0] in ("X4_MIN", "X4_CAP"):
            for s in LP["steps"]:
                s["scope"] = "total" if x[1]["per"] == "claim" else "line"
        elif x[0].startswith("R1:"):
            sem["R1"] = x[0].split(":")[1]
            sem["R1u"] = _p.money_val(x[1]["u"])[0]
        elif x[0].startswith("R3:"):
            sem["R3"] = x[0].split(":")[1]
    if LP["steps"]:
        sem["X4"] = {s["id"]: s["scope"] for s in LP["steps"]}
    LP["sem"] = sem
    if world == "open":
        cats = {x[1]["f"]: [v.strip() for v in x[1]["list"].split(", ")] for x in M if x[0] == "CATLIST"}
        LP["cats"] = cats
    curs = {s[4:] for s in seen if s.startswith("CUR:")}
    if len(curs) > 1:
        raise _p.PErr("currency differs")
    cur = curs.pop() if curs else None
    nums = [s for s in seen if not s.startswith("CUR:")]
    LP["unit"] = D("0.01") if any("." in s for s in nums) else D(1)
    LP["count"] = not (LP["amt"]["kind"] == "stated" and _p.MONEY_RX.match((doc.get(amt) or "x").strip())) and \
        not (LP["amt"]["kind"] == "mul" and _p.MONEY_RX.match((doc.get(LP["amt"]["p"]) or "x").strip()))
    if qinfo["kind"] == "cases":
        cols, rows_ = case_tab
        cases, refs = [], []
        for r in rows_:
            cv, cf = {}, {}
            for c, x in zip(cols[1:], r[1:]):
                lab = None
                for l in [LP["amt"].get("a"), LP["amt"].get("q"), LP["amt"].get("p"), (LP["x10"] or {}).get("f")]:
                    if l and norm_key(l) == norm_key(c):
                        lab = l
                if lab is None:
                    raise _p.PErr("case column read by no rule")
                if LP["x10"] and lab == LP["x10"]["f"]:
                    cf[lab] = x.strip()
                elif _p.MONEY_RX.match(x.strip()):
                    cv[lab] = _p.money_val(x, None, seen)[0]
                else:
                    cv[lab] = _p.num_lead(x)
            cases.append({"vals": cv, "facts": cf})
            refs.append(r[0])
        if refs != [o for o in row["options"] if o in refs]:
            raise _p.PErr("case order")
        money_lab = LP["amt"].get("a") or LP["amt"].get("p")
        idx = [i for i, cc in enumerate(cols[1:]) if norm_key(cc) == norm_key(money_lab)]
        if idx:
            LP["count"] = not any(_p.MONEY_RX.match(r[idx[0] + 1].strip()) for r in rows_)
        op, T, negcmp, verb = _p.parse_cmpT(qinfo["T"], None)
        LP["q"] = {"kind": "cases", "cmp": op, "T": T, "cases": cases, "_refs": refs}
    elif qinfo["kind"] == "thr":
        LP["q"] = {"kind": "thr", "cmp": qinfo["op"], "T": qinfo["T"], "neg": qinfo["neg"]}
    elif qinfo["kind"] == "value":
        LP["q"] = {"kind": "value"}
    elif qinfo["kind"] == "band":
        LP["q"] = {"kind": "band"}
        LP["_names"] = [b["name"] for b in bands]
    else:
        raise _p.PErr("band question kind")
    printed, pn = {}, {}
    if LP["amt"]["kind"] == "mul" and doc.get(amt) is not None:
        v = doc.get(amt)
        printed[amt] = _p.money_val(v, None, seen)[0] if _p.MONEY_RX.match(v.strip()) else _p.num_lead(v)
        pn[amt] = "amount"
    for i, b in enumerate(bands):
        for suffix, node in ((" part", f"part{i}"), (" charge", f"bandcharge{i}")):
            v = doc.get(b["name"] + suffix)
            if v is not None:
                printed[b["name"] + suffix] = _p.money_val(v, None, seen)[0] if _p.MONEY_RX.match(v.strip()) else _p.num_lead(v)
                pn[b["name"] + suffix] = node
    if printed:
        LP["printed"], LP["printed_nodes"] = printed, pn
    LP["_cur"] = cur
    return LP

"""Parser part for S4 date rows (and the S5 settlement date): card clauses D1-D17, the holiday line, the calendar strip
(weekday facts, checked against B's own calendar), dates in the three U4 forms."""
from __future__ import annotations

import datetime as dt
import re

from . import lex
from . import parse as _p
from .parse_doc import norm_key
from . import solve_b_date as SB

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
          "December"]
WD = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
_M = "|".join(MONTHS)
_W = "|".join(WD)
DATE_RX = [
    (re.compile(rf"^(?:(?P<wd>{_W}), )?(?P<d>\d{{1,2}}) (?P<m>{_M}) (?P<y>\d{{4}})$"), "gb"),
    (re.compile(rf"^(?:(?P<wd>{_W}), )?(?P<m>{_M}) (?P<d>\d{{1,2}}), (?P<y>\d{{4}})$"), "us"),
    (re.compile(rf"^(?P<y>\d{{4}})-(?P<m>\d{{2}})-(?P<d>\d{{2}})(?: \((?P<wd>{_W})\))?$"), "iso"),
]


def parse_date(s):
    s = s.strip()
    for rx, kind in DATE_RX:
        m = rx.match(s)
        if m:
            y, d = int(m.group("y")), int(m.group("d"))
            mo = int(m.group("m")) if kind == "iso" else MONTHS.index(m.group("m")) + 1
            n = SB.days_from_civil(y, mo, d)
            wd = m.group("wd")
            if wd and WD.index(wd) != SB.weekday(n):
                raise _p.PErr("stated weekday does not match the calendar (render bug)")
            if not (1 <= mo <= 12 and 1 <= d <= SB.month_len(y, mo)):
                raise _p.PErr("not a calendar date")
            return dt.date(y, mo, d), bool(wd)
    raise _p.PErr(f"not a date: {s!r}")


def tpls():
    T = [("D1", lex.D1), ("D4A", lex.D4A), ("D4B", lex.D4B), ("D15", lex.D15), ("D6A", lex.D6A), ("D6B", lex.D6B),
         ("D8", lex.D8), ("D8_RULE", lex.D8_RULE), ("D16", lex.D16), ("WIN_INTRO", lex.WIN_INTRO), ("D17", lex.D17),
         ("CNT_CAL", lex.CNT_CAL), ("CNT_BUS", lex.CNT_BUS)]
    T += [(f"D7:{k}", v) for k, v in lex.D7.items()]
    T += [(f"D12:{k}", v) for k, v in lex.D12.items()]
    T += [(f"D5:{k}", v) for k, v in lex.D5.items()]
    T += [(f"D14:{k}", v) for k, v in lex.D14.items()]
    T += [(f"B1W:{k}", v) for k, v in lex.B1_DATE.items()]
    return T


def _ord_ok(n, nth):
    from .dcard import ordinal
    return ordinal(int(n)) == nth


def question(eng, row, q):
    if eng == "stmt":
        from . import parse_stmt
        return parse_stmt.question(row, q)
    if row["qtype"] == "noul":
        for kind, direct in (("ontime", lex.Q_ONTIME), ("late", lex.Q_LATE)):
            for tpl in direct:
                m = lex.compile_tpl(tpl, anchored=True).match(q)
                if m:
                    return {"kind": kind, "act": m.group("act"), "id": m.group("id"), "neg": 0, "tf": 0}
        P = None
        for rx in _p.TF_RX:
            m = rx.match(q)
            if m:
                P = m.group("P")
        if P is None:
            raise _p.PErr("date question frame")
        neg = 0
        if P.startswith(lex.OPN):
            neg += 1
            P = P[len(lex.OPN):]
        for kind, pos, negs in (("ontime", lex.P_ONTIME, lex.P_ONTIME_NEG), ("late", lex.P_LATE, lex.P_LATE_NEG)):
            for tpl in pos:
                m = lex.compile_tpl(tpl, anchored=True).match(P)
                if m:
                    return {"kind": kind, "act": m.group("act"), "id": m.group("id"), "neg": neg, "tf": 1}
            for tpl in negs:
                m = lex.compile_tpl(tpl, anchored=True).match(P)
                if m:
                    return {"kind": kind, "act": m.group("act"), "id": m.group("id"), "neg": neg + 1, "tf": 1}
        raise _p.PErr("date proposition")
    for kind, lst in (("lastday", lex.Q_LASTDAY), ("count", lex.Q_COUNT), ("window", lex.Q_WINDOW)):
        for tpl in lst:
            m = lex.compile_tpl(tpl, anchored=True).match(q)
            if m:
                return {"kind": kind, **m.groupdict()}
    if q in lex.Q_CASES_LATE:
        return {"kind": "cases"}
    raise _p.PErr("date choice question")


def parse(eng, row, doc, M, qinfo, ctext):
    if eng == "stmt":
        from . import parse_stmt
        return parse_stmt.parse(row, doc, M, qinfo, ctext)
    g = {}
    for x in M:
        g.setdefault(x[0], []).append(x[1])
    if "W0" not in g or (("W1" in g) == ("W2" in g)) or "D1" not in g:
        raise _p.PErr("date card frame")
    world = "open" if "W2" in g else "closed"
    sem = {}
    rule = {"ext": None}
    evt = act = None
    count = None
    nrules = sum(1 for k in ("D4A", "D4B", "D6B", "D8_RULE", "CNT_CAL", "CNT_BUS") if k in g)
    if nrules != 1:
        raise _p.PErr("exactly one deadline or count rule (R3-08)")
    if "D4A" in g:
        x = g["D4A"][0]
        rule.update(kind="cal", N=int(x["N"]))
        sem["D4"] = "a"
        evt, act = x["evt"], x["act"]
    elif "D4B" in g:
        x = g["D4B"][0]
        n = int(re.match(r"\d+", x["Nth"]).group(0))
        if not _ord_ok(n, x["Nth"]):
            raise _p.PErr("ordinal")
        rule.update(kind="cal", N=n)
        sem["D4"] = "b"
        evt, act = x["evt"], x["act"]
    elif "D6B" in g:
        x = g["D6B"][0]
        if not _ord_ok(x["N"], x["Nth"]):
            raise _p.PErr("ordinal")
        rule.update(kind="bday", N=int(x["N"]))
        evt, act = x["evt"], x["act"]
        if "D6A" not in g:
            raise _p.PErr("D6b without D6a")
    elif "D8_RULE" in g:
        x = g["D8_RULE"][0]
        if "D8" not in g or g["D8"][0]["M"] != x["M"]:
            raise _p.PErr("D8 clause missing")
        rule.update(kind="month", M=int(x["M"]))
        evt, act = x["evt"], x["act"]
    else:
        k = "CNT_CAL" if "CNT_CAL" in g else "CNT_BUS"
        x = g[k][0]
        count = {"kind": "cal" if k == "CNT_CAL" else "bus", "d1": x["d1"], "d2": x["d2"]}
        rule.update(kind="count")
        evt, act = x["d1"], x["d2"]
    evt_l = evt if rule["kind"] == "count" else f"{evt} date"
    act_l = act if rule["kind"] == "count" else f"{act} date"
    for k in g:
        if k.startswith("D7:"):
            sem["D7"] = k.split(":")[1]
            if "D6A" not in g:
                raise _p.PErr("D7 without D6a (A13)")
        elif k.startswith("D5:"):
            sem["D5"] = k.split(":")[1]
        elif k.startswith("D14:"):
            sem["D14"] = k.split(":")[1]
        elif k.startswith("B1W:"):
            sem["B1w"] = k.split(":")[1]
    d12 = [k for k in g if k.startswith("D12:")]
    if len(d12) > 1 or (d12 and len(g[d12[0]]) > 1):
        raise _p.PErr("second extension rule (R3-24)")
    facts = {}
    if d12:
        x = g[d12[0]][0]
        sem["D12"] = d12[0].split(":")[1]
        G = x["G"]
        m = re.search(r"(If|Unless) (?P<c>.+),$", G)
        if not m:
            raise _p.PErr("extension condition")
        conn = "UN1" if m.group(1) == "Unless" else "O2"
        c = m.group("c")
        tmp_name = "G_O2" if conn == "O2" else "G_UN1"
        conn2, join, conds = _p._gate_parse(tmp_name, {"c": c})
        unit = {"business days": "bday", "calendar days": "cal"}.get(x["unit"])
        if unit is None:
            raise _p.PErr("extension unit")
        rule["ext"] = {"K": int(x["K"]), "unit": unit, "conn": conn, "join": join, "conds": conds}
    if rule["kind"] == "count":
        rule.pop("ext")
        rule["ext"] = None
    # document
    dates = {}
    case_cols = set()
    if qinfo["kind"] == "cases":
        tabs = [t for t in doc.tables if t[1] and any(r[0] in (row.get("options") or []) for r in t[1])]
        if len(tabs) != 1:
            raise _p.PErr("case table")
        cols, rows_, cap = tabs[0]
        case_cols = {norm_key(c) for c in cols[1:]}
    for lbl in (evt_l, act_l):
        if norm_key(lbl) in case_cols:
            continue
        v = doc.get(lbl)
        if v is None:
            if lbl == act_l and qinfo["kind"] == "lastday":
                continue
            raise _p.PErr(f"no date for {lbl!r}")
        dates[lbl], _wd = parse_date(v)
    if rule.get("ext"):
        for cnd in rule["ext"]["conds"]:
            if norm_key(cnd["f"]) in case_cols:
                continue
            v = doc.get(cnd["f"])
            if v is None:
                raise _p.PErr("extension field missing")
            facts[cnd["f"]] = v.strip()
    hol = []
    d6a = "D6A" in g
    hv = doc.get(lex.HOL_NOTE)
    if d6a:
        if hv is None:
            raise _p.PErr("D6a card without its holiday line (R3-23)")
        if hv.strip() != "none":
            for part in hv.split("; "):
                h, wd = parse_date(part)
                if not wd:
                    raise _p.PErr("holiday without its weekday (D9)")
                if h.weekday() >= 5:
                    raise _p.PErr("holiday on a weekend day (A12)")
                hol.append(h)
    elif hv is not None:
        raise _p.PErr("holiday line on a card without D6a")
    sv = doc.get(lex.STRIP_NOTE)
    if sv is not None:
        prev = None
        for part in sv.split("; "):
            d, wd = parse_date(part)
            if not wd:
                raise _p.PErr("strip date without weekday")
            if prev is not None and (d - prev).days != 1:
                raise _p.PErr("strip dates not consecutive")
            prev = d
    LP = {"eng": "date", "world": world, "rule": rule, "evt": evt_l, "act": act_l, "dates": dates, "facts": facts,
          "holidays": hol, "sem": sem, "d6a": d6a}
    if count:
        LP["count"] = count
    if world == "open":
        LP["cats"] = {x[1]["f"]: [v.strip() for v in x[1]["list"].split(", ")] for x in M if x[0] == "CATLIST"}
        for cnd in (rule.get("ext") or {}).get("conds", []):
            if cnd["f"] not in LP["cats"]:
                LP["cats"][cnd["f"]] = ["yes", "no"]
        LP["cats"] = {k: v for k, v in LP["cats"].items() if k in facts}
    if "WIN_INTRO" in g:
        LP["windows"] = _windows(ctext, sem.get("B1w"))
        LP["_names"] = [w["name"] for w in LP["windows"]]
    k = qinfo["kind"]
    if k in ("ontime", "late"):
        LP["q"] = {"kind": k, "neg": qinfo["neg"]}
    elif k in ("lastday", "count", "window"):
        LP["q"] = {"kind": k}
    elif k == "cases":
        cols, rows_, cap = tabs[0]
        cases, refs = [], []
        for r in rows_:
            cd, cf = {}, {}
            for c, x in zip(cols[1:], r[1:]):
                if norm_key(c) in (norm_key(evt_l), norm_key(act_l)):
                    lb = evt_l if norm_key(c) == norm_key(evt_l) else act_l
                    cd[lb] = parse_date(x)[0]
                else:
                    lab = [cc["f"] for cc in (rule.get("ext") or {}).get("conds", []) if norm_key(cc["f"]) == norm_key(c)]
                    if not lab:
                        raise _p.PErr("case column read by no rule")
                    cf[lab[0]] = x.strip()
            cases.append({"dates": cd, "facts": cf})
            refs.append(r[0])
        LP["q"] = {"kind": "cases", "cases": cases, "_refs": refs}
    return LP


def _windows(ctext, b1):
    items = []
    for ln in ctext.split("\n"):
        s = re.sub(r"^\s*(?:(?:[-*+•·>]|\d+[.)])\s*)+", "", ln).strip()
        m = re.match(r"^(?P<name>[^:]+): (?P<range>.+)$", s)
        if not m:
            continue
        rng = m.group("range").strip()
        got = None
        for pos, tpl in lex.WIN_RANGE[b1].items():
            rx = "^" + re.escape(tpl).replace(re.escape("{a}"), r"(?P<a>.+?)").replace(re.escape("{b}"), r"(?P<b>.+?)") + "$"
            mm = re.match(rx, rng)
            if mm:
                got = (pos, mm.groupdict())
                break
        if not got:
            continue
        pos, gd = got

        def edge(t):
            if t is None:
                return None
            if t == lex.WIN_EDGE0:
                return 0
            m2 = re.match(r"^(\d+) calendar days after the last allowed day$", t)
            if not m2:
                raise _p.PErr("window edge")
            return int(m2.group(1))
        items.append({"name": m.group("name").strip(), "lo": edge(gd.get("a")), "hi": edge(gd.get("b")), "pos": pos})
    if len(items) < 2 or items[0]["pos"] != "low" or items[-1]["pos"] != "high":
        raise _p.PErr("window table")
    for a, b in zip(items, items[1:]):
        if a["hi"] != b["lo"]:
            raise _p.PErr("windows do not share edges (R3-06)")
    return [{"name": i["name"], "lo": i["lo"], "hi": i["hi"]} for i in items]

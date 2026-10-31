"""Solver A for S4 calendar rules (and the S5 settlement date): datetime.date, business days by day-by-day iteration
over the stated weekend (Saturday, Sunday) and holiday sets (3.1).

LP (date): dates {label: date}; facts {label: str}; rule {kind: cal | bday | month, N, M, ext: {K, unit, conn, join,
conds} | None}; holidays [date]; sem D4 (a | b), D7 (fwd | back | none | absent), D12 (pre | post), D5, D14, B1w;
evt / act labels; count {kind: cal | bus, d1, d2}; windows [{name, lo, hi}] (k offsets from L); q.
"""
from __future__ import annotations

import calendar
import datetime as dt

from .money import Reject, Tr, gate_true

ONE_DAY = dt.timedelta(days=1)


def is_bday(d, hol):
    return d.weekday() < 5 and d not in hol


def add_bdays(d, n, hol, tr=None):
    """The n-th business day after d (counting starts on the day after d)."""
    k = 0
    x = d
    while k < n:
        x += ONE_DAY
        if is_bday(x, hol):
            k += 1
    return x


def add_months(d, m):
    y, mo = d.year, d.month + m
    y += (mo - 1) // 12
    mo = (mo - 1) % 12 + 1
    last = calendar.monthrange(y, mo)[1]
    return dt.date(y, mo, min(d.day, last))


def roll(d, form, hol):
    if form in (None, "none") or is_bday(d, hol):
        return d
    step = ONE_DAY if form == "fwd" else -ONE_DAY
    x = d
    while not is_bday(x, hol):
        x += step
    return x


def last_day(LP, rd=None, facts=None, dates=None):
    """(last allowed day, trace)."""
    rd = rd or {}
    sem = {**LP.get("sem", {}), **rd.get("sem", {})}
    err = rd.get("err")
    tr = Tr()
    dates = dates or LP["dates"]
    facts = facts if facts is not None else LP.get("facts", {})
    hol = set() if err == "E-hol" else set(LP.get("holidays", []))
    r = LP["rule"]
    ev = dates[LP["evt"]]
    kind = r["kind"]
    if err == "E-bday" and kind == "bday":
        kind = "cal"
    if kind == "cal":
        n = r["N"]
        if sem.get("D4", "a") == "b":
            L = ev + dt.timedelta(days=n - 1)
        else:
            L = ev + dt.timedelta(days=n)
        tr.op("offset", L)
    elif kind == "bday":
        L = add_bdays(ev, r["N"], hol)
        inside = sum(1 for h in hol if ev < h <= L)
        tr.op("bday", L)
        if r["N"] > 10 or inside > 1:
            tr.op("bday2", L)
    elif kind == "month":
        e = err if err in ("E-eom:overflow", "E-eom:keep") else None
        if e == "E-eom:overflow":
            y, mo = ev.year, ev.month + r["M"]
            y += (mo - 1) // 12
            mo = (mo - 1) % 12 + 1
            L = dt.date(y, mo, 1) + dt.timedelta(days=ev.day - 1)
        elif e == "E-eom:keep" and ev.day == calendar.monthrange(ev.year, ev.month)[1]:
            t = add_months(ev, r["M"])
            L = dt.date(t.year, t.month, calendar.monthrange(t.year, t.month)[1])
        else:
            L = add_months(ev, r["M"])
        tr.op("month", L)
    else:
        raise ValueError(kind)
    form = sem.get("D7")
    ext = r.get("ext")
    applies = False
    if ext and err != "E-ext":
        applies = gate_true({"no": 0, "conn": ext["conn"], "join": ext["join"], "conds": ext["conds"]}, facts, {}, rd)
    if applies:
        tr.flags.add("bind:ext")
        K, unit = ext["K"], ext["unit"]
        d12 = sem.get("D12", "pre")
        if d12 == "pre":
            base = L
            L = add_bdays(base, K, hol) if unit == "bday" else base + dt.timedelta(days=K)
            tr.op("ext", L)
            L = roll(L, form, hol)
        else:
            L = roll(L, form, hol)
            base = L
            L = add_bdays(L, K, hol) if unit == "bday" else L + dt.timedelta(days=K)
            tr.op("ext", L)
            L = roll(L, form, hol)
        if unit == "bday" and (K > 10 or sum(1 for h in hol if base < h <= L) > 1):
            tr.op("ext2", L)
        tr.sel += 1
    else:
        L2 = roll(L, form, hol)
        if L2 != L:
            tr.flags.add("bind:roll")
        L = L2
    if form:
        tr.sel += 1
    if L < ev:
        raise Reject("last allowed day before the event (R4-11)")
    tr.final = L
    return L, tr


def count(LP, rd=None):
    rd = rd or {}
    sem = {**LP.get("sem", {}), **rd.get("sem", {})}
    err = rd.get("err")
    c = LP["count"]
    d1, d2 = LP["dates"][c["d1"]], LP["dates"][c["d2"]]
    hol = set() if err == "E-hol" else set(LP.get("holidays", []))
    tr = Tr()
    kind = c["kind"]
    if err == "E-bday" and kind == "bus":
        kind = "cal"
    if kind == "cal":
        form = sem.get("D5", "excl") if c["kind"] == "cal" else ("excl" if sem.get("D14", "after") == "after" else "both")
        n = (d2 - d1).days + (1 if form == "both" else 0)
    else:
        form = sem.get("D14", "after")
        start = d1 + ONE_DAY if form == "after" else d1
        n = 0
        x = start
        while x <= d2:
            if is_bday(x, hol):
                n += 1
            x += ONE_DAY
    tr.op("count", n)
    tr.final = n
    return n, tr


def window_of(LP, L, act, rd=None):
    rd = rd or {}
    sem = {**LP.get("sem", {}), **rd.get("sem", {})}
    b1 = sem.get("B1w", "upper")
    for w in LP["windows"]:
        lo = None if w.get("lo") is None else L + dt.timedelta(days=w["lo"])
        hi = None if w.get("hi") is None else L + dt.timedelta(days=w["hi"])
        if b1 == "upper":
            ok = (lo is None or act > lo) and (hi is None or act <= hi)
        else:
            ok = (lo is None or act >= lo) and (hi is None or act < hi)
        if ok:
            return w["name"]
    raise Reject("no window")


def answer(LP, rd=None, facts=None, dates=None):
    """The row's raw answer under reading rd: on time (bool) | late (bool) | last day (date) | count (int) | window."""
    q = LP["q"]
    k = q["kind"]
    dates = dates or LP["dates"]
    if k in ("ontime", "late"):
        L, tr = last_day(LP, rd, facts, dates)
        act = dates[LP["act"]]
        on = act <= L
        return on if k == "ontime" else (not on)
    if k == "lastday":
        return last_day(LP, rd, facts, dates)[0]
    if k == "count":
        return count(LP, rd)[0]
    if k == "window":
        L, tr = last_day(LP, rd, facts, dates)
        return window_of(LP, L, dates[LP["act"]], rd)
    raise ValueError(k)


def trace(LP):
    q = LP["q"]
    if q["kind"] == "count":
        return count(LP)[1]
    L, tr = last_day(LP)
    if q["kind"] == "window":
        tr.op("winoffset", L)
    return tr

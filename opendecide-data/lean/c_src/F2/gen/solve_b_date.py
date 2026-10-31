"""Re-solver for S4 dates and the S5 settlement date: integer day ordinals (civil-to-days, Hinnant's formula), weekday
= ordinal mod 7, business days in closed form (full weeks x 5 + remainder - listed holidays in range). No datetime /
calendar import (3.2)."""
from __future__ import annotations


def days_from_civil(y, m, d):
    y -= m <= 2
    era = (y if y >= 0 else y - 399) // 400
    yoe = y - era * 400
    doy = (153 * (m + (-3 if m > 2 else 9)) + 2) // 5 + d - 1
    doe = yoe * 365 + yoe // 4 - yoe // 100 + doy
    return era * 146097 + doe - 719468


def civil_from_days(z):
    z += 719468
    era = (z if z >= 0 else z - 146096) // 146097
    doe = z - era * 146097
    yoe = (doe - doe // 1460 + doe // 36524 - doe // 146096) // 365
    y = yoe + era * 400
    doy = doe - (365 * yoe + yoe // 4 - yoe // 100)
    mp = (5 * doy + 2) // 153
    d = doy - (153 * mp + 2) // 5 + 1
    m = mp + (3 if mp < 10 else -9)
    return (y + (m <= 2), m, d)


def iso_to_n(s):
    y, m, d = (int(x) for x in s.split("-"))
    return days_from_civil(y, m, d)


def n_to_iso(n):
    y, m, d = civil_from_days(n)
    return f"{y:04d}-{m:02d}-{d:02d}"


def weekday(n):
    """0 = Monday ... 6 = Sunday (1970-01-01, day 0, was a Thursday)."""
    return (n + 3) % 7


def month_len(y, m):
    if m == 2:
        return 29 if (y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)) else 28
    return 31 if m in (1, 3, 5, 7, 8, 10, 12) else 30


def is_bday(n, hol):
    return weekday(n) < 5 and n not in hol


def bdays_between(a, b, hol):
    """Business days in (a, b] in closed form."""
    if b <= a:
        return 0
    total = b - a
    full, rem = divmod(total, 7)
    cnt = full * 5
    w = weekday(a)
    for i in range(1, rem + 1):
        if (w + i) % 7 < 5:
            cnt += 1
    cnt -= sum(1 for h in hol if a < h <= b and weekday(h) < 5)
    return cnt


def nth_bday_after(a, n, hol):
    lo, hi = a, a + 3 * n + 3 * len(hol) + 14
    while bdays_between(a, hi, hol) < n:
        hi += 14
    while lo < hi:
        mid = (lo + hi) // 2
        if bdays_between(a, mid, hol) >= n:
            hi = mid
        else:
            lo = mid + 1
    return lo


def roll(n, form, hol):
    if form in (None, "none") or is_bday(n, hol):
        return n
    step = 1 if form == "fwd" else -1
    while not is_bday(n, hol):
        n += step
    return n


def add_months(n, m):
    y, mo, d = civil_from_days(n)
    mo2 = mo + m
    y += (mo2 - 1) // 12
    mo2 = (mo2 - 1) % 12 + 1
    return days_from_civil(y, mo2, min(d, month_len(y, mo2)))


def _gate(ext, facts):
    cs = []
    for c in ext["conds"]:
        x = facts.get(c["f"])
        if x == "not recorded":
            raise LookupError(c["f"])
        cs.append(x == c["v"])
    j = ext["join"]
    c = cs[0] if j == "single" else (cs[0] and cs[1]) if j == "and" else (cs[0] or cs[1]) if j == "or1" else (cs[0] != cs[1])
    return (not c) if ext["conn"] == "UN1" else c


def last_day(P, dates, facts):
    r = P["rule"]
    sem = P.get("sem", {})
    hol = {iso_to_n(h) for h in P.get("holidays", [])}
    ev = iso_to_n(dates[P["evt"]])
    if r["kind"] == "cal":
        L = ev + r["N"] - (1 if sem.get("D4", "a") == "b" else 0)
    elif r["kind"] == "bday":
        L = nth_bday_after(ev, r["N"], hol)
    else:
        L = add_months(ev, r["M"])
    form = sem.get("D7")
    ext = r.get("ext")
    if ext and _gate(ext, facts):
        if sem.get("D12", "pre") == "pre":
            L = nth_bday_after(L, ext["K"], hol) if ext["unit"] == "bday" else L + ext["K"]
            L = roll(L, form, hol)
        else:
            L = roll(L, form, hol)
            L = nth_bday_after(L, ext["K"], hol) if ext["unit"] == "bday" else L + ext["K"]
            L = roll(L, form, hol)
    else:
        L = roll(L, form, hol)
    return L


def count(P, dates):
    c = P["count"]
    sem = P.get("sem", {})
    hol = {iso_to_n(h) for h in P.get("holidays", [])}
    a, b = iso_to_n(dates[c["d1"]]), iso_to_n(dates[c["d2"]])
    if c["kind"] == "cal":
        return b - a + (1 if sem.get("D5", "excl") == "both" else 0)
    n = bdays_between(a, b, hol)
    if sem.get("D14", "after") == "both" and is_bday(a, hol):
        n += 1
    return n


def window(P, L, act):
    b1 = P.get("sem", {}).get("B1w", "upper")
    for w in P["windows"]:
        lo = None if w["lo"] is None else L + w["lo"]
        hi = None if w["hi"] is None else L + w["hi"]
        ok = ((lo is None or act > lo) and (hi is None or act <= hi)) if b1 == "upper" else \
             ((lo is None or act >= lo) and (hi is None or act < hi))
        if ok:
            return w["name"]
    raise ValueError("no window")


def answer(P, dates, facts):
    q = P["q"]
    k = q["kind"]
    if k in ("ontime", "late"):
        L = last_day(P, dates, facts)
        on = iso_to_n(dates[P["act"]]) <= L
        aff = on if k == "ontime" else not on
        return ("yn", aff if q.get("neg", 0) % 2 == 0 else not aff)
    if k == "lastday":
        return ("date", n_to_iso(last_day(P, dates, facts)))
    if k == "count":
        return ("count", count(P, dates))
    if k == "window":
        L = last_day(P, dates, facts)
        return ("outcome", window(P, L, iso_to_n(dates[P["act"]])))
    if k == "cases":
        hits = []
        for i, c in enumerate(q["cases"]):
            L = last_day(P, c["dates"], c["facts"])
            if iso_to_n(c["dates"][P["act"]]) > L:
                hits.append(i)
        return ("cases", hits)
    raise ValueError(k)


def solve_date(P, options=None, names=None):
    if P["eng"] == "stmt":
        from .solve_b_stmt import solve_stmt
        return solve_stmt(P, options, names)
    facts = P.get("facts", {})
    dates = P.get("dates", {})
    if P.get("world") == "open":
        unk = [k for k, v in facts.items() if v == "not recorded"]
        f = unk[0]
        dom = P.get("cats", {}).get(f) or ["yes", "no"]
        labs = set()
        res = None
        for x in dom:
            r = answer(P, dates, {**facts, f: x})
            lab = r[1]
            if r[0] == "outcome" and names:
                lab = names[int(lab[1:]) - 1]
            labs.add(lab)
            res = r
        if len(labs) >= 2:
            return ("nei", None)
        return _named(res, names)
    return _named(answer(P, dates, facts), names)


def _named(r, names):
    if r[0] == "outcome" and names and r[1].startswith("w"):
        return ("outcome", names[int(r[1][1:]) - 1])
    return r

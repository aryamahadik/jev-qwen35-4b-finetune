"""Re-solver on the canonical problem (G3 re-solve; the 3.2 paradigm): integers only.

Every number is an exact reduced fraction (numerator, denominator) of Python ints parsed from the canonical "n/d"
strings; rounding is integer divmod with explicit half rules; calendar arithmetic uses day ordinals from a civil-to-days
formula; business days use the closed form (full weeks x workdays + remainder, minus listed holidays in range); bands
use the cumulative closed form. Forbidden imports (3.2): decimal, fractions, datetime, calendar, dateutil, numpy, pandas,
holidays. This module imports none of them (G3 asserts it at import).
"""
from __future__ import annotations

from math import gcd

# ----------------------------------------------------------------------------------------------------------------- rationals


def Q(s):
    if isinstance(s, tuple):
        return s
    if isinstance(s, int):
        return (s, 1)
    s = str(s)
    if "/" in s:
        a, b = s.split("/")
        return norm((int(a), int(b)))
    neg = s.startswith("-")
    s = s.lstrip("-")
    if "." in s:
        i, f = s.split(".")
        n = int(i + f) if (i + f) else 0
        d = 10 ** len(f)
    else:
        n, d = int(s), 1
    return norm((-n if neg else n, d))


def norm(x):
    n, d = x
    if d < 0:
        n, d = -n, -d
    g = gcd(n, d) or 1
    return (n // g, d // g)


def add(a, b):
    return norm((a[0] * b[1] + b[0] * a[1], a[1] * b[1]))


def sub(a, b):
    return norm((a[0] * b[1] - b[0] * a[1], a[1] * b[1]))


def mul(a, b):
    return norm((a[0] * b[0], a[1] * b[1]))


def div(a, b):
    if b[0] == 0:
        raise ZeroDivisionError
    return norm((a[0] * b[1], a[1] * b[0]))


def cmp(a, b):
    x = a[0] * b[1] - b[0] * a[1]
    return (x > 0) - (x < 0)


def lt(a, b):
    return cmp(a, b) < 0


def le(a, b):
    return cmp(a, b) <= 0


def mn(a, b):
    return a if le(a, b) else b


def mx(a, b):
    return b if le(a, b) else a


ZERO, ONE, HUND = (0, 1), (1, 1), (100, 1)


def round_to(v, unit, mode):
    """v rounded to a multiple of unit (both rationals, v >= 0) by integer divmod."""
    if v[0] < 0:
        raise ValueError("negative rounding")
    t = div(v, unit)                      # t = n/d units
    n, d = t
    q, r = divmod(n, d)                   # floor
    if r == 0:
        k = q
    elif mode == "floor":
        k = q
    elif mode == "ceiling":
        k = q + 1
    else:
        twice = 2 * r
        if twice > d:
            k = q + 1
        elif twice < d:
            k = q
        else:
            k = q + 1 if mode == "half_up" else (q if q % 2 == 0 else q + 1)
    return mul((k, 1), unit)


def floor_int(v):
    return v[0] // v[1]


def ceil_int(v):
    return -((-v[0]) // v[1])


# ----------------------------------------------------------------------------------------------------------------- money

def _gate(e, facts, vals):
    cs = []
    for c in e["conds"]:
        f = c["f"]
        if c["op"] == "is":
            x = facts.get(f)
            if x == "not recorded":
                raise LookupError(f)
            cs.append(x == c["v"])
            continue
        x = facts.get(f, vals.get(f))
        if x == "not recorded":
            raise LookupError(f)
        x = Q(x)
        t = Q(c["v"])
        k = cmp(x, t)
        cs.append({"ge": k >= 0, "gt": k > 0, "le": k <= 0, "lt": k < 0}[c["op"]])
    j = e["join"]
    if j == "single":
        c = cs[0]
    elif j == "and":
        c = cs[0] and cs[1]
    elif j == "or1":
        c = cs[0] or cs[1]
    else:
        c = (cs[0] != cs[1])
    return (not c) if e["conn"] == "UN1" else c


def money_run(P, applied, norround=False):
    sem = P.get("sem", {})
    vals = {k: Q(v) for k, v in P["vals"].items()}
    unit = Q(P["unit"])
    r1 = None if norround else sem.get("R1")
    r1u = Q(sem["R1u"]) if sem.get("R1u") else unit
    x2 = sem.get("X2", {})
    for no in applied:
        e = [x for x in P["excs"] if x["no"] == no][0]
        form = x2.get(str(no), "replace" if e["kind"] in ("rate", "pct") else "add")
        vals[e["on"]] = vals[e["v"]] if form == "replace" else add(vals[e["on"]], vals[e["v"]])
    steps = list(P["steps"])
    if sem.get("X1"):
        steps = [steps[i] for i in sem["X1"]]
    x4 = sem.get("X4", {})
    line_lims = [s for s in steps if s["op"] in ("cap", "min") and x4.get(s["id"], s.get("scope", "total")) == "line"]
    rest = [s for s in steps if s not in line_lims]
    amts = []
    for ln in P["lines"]:
        p = ln["p"]
        if p == "stated":
            a = vals[ln["a"]]
        elif p == "blank":
            a = ZERO
        elif p == "mul":
            q = vals[ln["q"]]
            m = sem.get("R5")
            if m == "ceil":
                q = (ceil_int(q), 1)
            elif m == "floor":
                q = (floor_int(q), 1)
            a = mul(q, vals[ln["r"]])
        elif p == "perk":
            q, r, k = vals[ln["q"]], vals[ln["r"]], Q(ln["k"])
            m = sem.get("U3", "pro_rata")
            if m == "pro_rata":
                a = div(mul(r, q), k)
            else:
                t = div(q, k)
                b = ceil_int(t) if m == "full_k" else floor_int(t)
                a = mul(r, (b, 1))
        elif p == "b4":
            q, r, x, m = vals[ln["q"]], vals[ln["r"]], vals[ln["b4x"]], vals[ln["b4m"]]
            a = mul(q, r) if le(q, x) else add(mul(x, r), mul(mul(sub(q, x), m), r))
        else:
            raise ValueError(p)
        for s in line_lims:
            a = mn(a, vals[s["v"]]) if s["op"] == "cap" else mx(a, vals[s["v"]])
        if r1 and sem.get("R2") == "line":
            a = round_to(a, r1u, r1)
        amts.append(a)
    v = amts[0]
    for a in amts[1:]:
        v = add(v, a)
    prev = v
    fee = None
    for s in rest:
        before = v
        op = s["op"]
        if op == "disc":
            v = div(mul(v, sub(HUND, vals[s["v"]])), HUND)
        elif op == "disc2":
            p1, p2 = vals[s["v"][0]], vals[s["v"][1]]
            if sem.get("X5", "succ") == "succ":
                v = div(mul(div(mul(v, sub(HUND, p1)), HUND), sub(HUND, p2)), HUND)
            else:
                v = div(mul(v, sub(HUND, add(p1, p2))), HUND)
        elif op == "pctof":
            v = div(mul(v, vals[s["v"]]), HUND)
            fee = v
        elif op == "fee":
            base = v if sem.get("X6", "after") == "after" else prev
            f = div(mul(base, vals[s["v"]]), HUND)
            fee = f
            if P.get("target") != "fee":
                v = add(v, f)
        elif op == "incfee":
            p = vals[s["v"]]
            if sem.get("X7", "include") == "include":
                net = div(mul(v, HUND), add(HUND, p))
                f = sub(v, net)
            else:
                f = div(mul(v, p), HUND)
            fee = f
        elif op == "cap":
            v = mn(v, vals[s["v"]])
        elif op == "min":
            v = mx(v, vals[s["v"]])
        elif op == "add":
            v = add(v, vals[s["v"]])
        elif op == "ded":
            for k in s["v"]:
                v = sub(v, vals[k])
        elif op == "allow":
            al = mn(mul(vals[s["v"][0]], vals[s["v"][1]]), vals[s["v"][2]])
            v = add(v, al)
        elif op == "pctded":
            dd = div(mul(v, vals[s["v"][0]]), HUND)
            if r1 and sem.get("R2") == "line":
                dd = round_to(dd, r1u, r1)
            dd = mx(dd, vals[s["v"][1]]) if s["lim"] == "floor" else mn(dd, vals[s["v"][1]])
            v = sub(v, dd)
        elif op == "floor0":
            if sem.get("X8", "floor") == "floor":
                v = mx(v, ZERO)
        else:
            raise ValueError(op)
        prev = before
    if P.get("target") == "fee" and fee is not None:
        v = fee
    if r1 and sem.get("R2", "final") == "final":
        v = round_to(v, r1u, r1)
    return v


def money_value(P, norround=False, override=None):
    if override:
        P = {**P, **override}
    facts = P.get("facts", {})
    vals = P["vals"]
    app = [e["no"] for e in P.get("excs", []) if _gate(e, facts, vals)]
    if len(app) >= 2:
        form = P.get("sem", {}).get("X3", "alone_lower")
        if form.startswith("fold"):
            return money_run(P, sorted(app), norround)
        best = None
        for no in sorted(app):
            v = money_run(P, [no], norround)
            if best is None or (lt(v, best) if form == "alone_lower" else lt(best, v)):
                best = v
        return best
    return money_run(P, app, norround)


def outcome(v, outs, b1):
    for o in outs:
        lo = None if o["lo"] is None else Q(o["lo"])
        hi = None if o["hi"] is None else Q(o["hi"])
        if b1 == "upper":
            ok = (lo is None or lt(lo, v)) and (hi is None or le(v, hi))
        else:
            ok = (lo is None or le(lo, v)) and (hi is None or lt(v, hi))
        if ok:
            return o["name"]
    raise ValueError("no band")


def _cmpq(v, op, T):
    k = cmp(v, T)
    return {"ge": k >= 0, "gt": k > 0, "le": k <= 0, "lt": k < 0}[op]


def solve(P, options=None, names=None):
    """Gold under the canonical problem: ('yn', bool) | ('value', (n, d)) | ('outcome', name) | ('cases', [idx...])
    | ('date', iso) | ('nei', None). options: the row's option texts (open-world rows need them for 'no option')."""
    eng = P["eng"]
    if eng != "money":
        from . import solve_b_more
        return solve_b_more.solve(P, options, names)
    q = P["q"]
    if P.get("world") == "open":
        r = _open_money(P, options or [], names)
    else:
        r = _money_q(P, q)
    return _named(r, names)


def _named(r, names):
    if r[0] == "outcome" and names and isinstance(r[1], str) and r[1].startswith("o"):
        return ("outcome", names[int(r[1][1:]) - 1])
    return r


def _money_q(P, q):
    if q["kind"] == "thr":
        v = money_value(P, norround=(P.get("sem", {}).get("R3") == "unrounded"))
        aff = _cmpq(v, q["cmp"], Q(q["T"]))
        return ("yn", aff if q.get("neg", 0) % 2 == 0 else not aff)
    if q["kind"] == "op":
        v = money_value(P)
        aff = v[0] > 0
        return ("yn", aff if q.get("neg", 0) % 2 == 0 else not aff)
    if q["kind"] == "value":
        return ("value", money_value(P))
    if q["kind"] == "outcome":
        v = money_value(P, norround=(P.get("sem", {}).get("R3") == "unrounded"))
        return ("outcome", outcome(v, q["outs"], q["b1"]))
    if q["kind"] == "cases":
        hits = []
        for i, c in enumerate(q["cases"]):
            P2 = {**P, "vals": {**P["vals"], **c["vals"]}, "facts": {**P.get("facts", {}), **c["facts"]}}
            v = money_value(P2, norround=(P.get("sem", {}).get("R3") == "unrounded"))
            if _cmpq(v, q["cmp"], Q(q["T"])):
                hits.append(i)
        return ("cases", hits)
    raise ValueError(q["kind"])


def _opt_values(options):
    out = []
    for o in options:
        parts = o.split(" ")
        if len(parts) == 2:
            try:
                out.append(Q(parts[0]))
            except Exception:
                pass
    return out


def _open_money(P, options, names=None):
    """Open world: the one 'not recorded' fact ranges over its domain (yes/no, a listed category, or a count over a
    finite breakpoint set); NEI iff two completions give different option-level labels."""
    unk = [k for k, v in P.get("facts", {}).items() if v == "not recorded"]
    if len(unk) != 1:
        raise ValueError("open-world row needs exactly one unknown")
    f = unk[0]
    dom = _domain(P, f)
    labs = set()
    for x in dom:
        P2 = {**P, "facts": {**P["facts"], f: x}, "world": "closed"}
        r = _money_q(P2, P["q"])
        lab = r[1]
        if r[0] == "value":
            lab = lab if any(cmp(lab, o) == 0 for o in _opt_values(options)) else "no option"
        elif r[0] == "outcome":
            lab = _named(r, names)[1]
            lab = lab if lab in options else "no option"
        labs.add(lab if not isinstance(lab, list) else tuple(lab))
    if len(labs) >= 2:
        return ("nei", None)
    r = _money_q({**P, "facts": {**P["facts"], f: next(iter(dom))}, "world": "closed"}, P["q"])
    return r


def _domain(P, f):
    if f in P.get("cats", {}):
        return list(P["cats"][f])
    for e in P.get("excs", []):
        for c in e["conds"]:
            if c["f"] == f:
                if c["op"] == "is" and c["v"] in ("yes", "no"):
                    return ["yes", "no"]
                if c["op"] != "is":
                    pts = set()
                    for e2 in P["excs"]:
                        for c2 in e2["conds"]:
                            if c2["f"] == f and c2["op"] != "is":
                                t = Q(c2["v"])
                                k = floor_int(t)
                                pts |= {max(0, k - 1), k, k + 1}
                    pts |= {0, 10 ** 9}
                    return [f"{x}/1" for x in sorted(pts)]
    return ["yes", "no"]

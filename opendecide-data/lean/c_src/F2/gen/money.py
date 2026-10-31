"""Solver A for the money engine (S1, S2, S5 statements, and the charge part of S3): Decimal + quantize (3.1).

The structure IS the canonical problem P (canon.py describes the keys); A evaluates it under a reading `rd` that may
override SEM switches (alt-labels, invariance filter) or switch on one named error (hooks, 3.4).

P (money):
  vals   {role: Decimal}      quantities, rates, percentages, caps, minimums, fixed charges, amounts, thresholds
  facts  {role: str}          case facts: 'yes' / 'no' / a category value / an integer count as text; open world: one
                              of them is 'not recorded'
  lines  [{q, r, a, k, p, b4x, b4m, mark}]  p: 'mul' (q x r, R5 on q), 'perk' (U3: r per k of q), 'stated' (a),
                              'b4' (S5: units up to b4x at r, after at b4m x r; scope = the line)
  steps  [{op, v, base, scope}] canonical order; ops: disc, disc2, fee, pctof, cap, min, add, ded, floor0, incfee,
                              allow, pctded
  excs   [{no, conn, join, conds:[{f, op, v}], kind, v, on}]
  sem    SEM switch vector of the card variant (only the dimensions the card has)
  unit   display grid of money (Decimal 0.01 or 1)
  target 'final' | 'fee'
Readings: rd = {"sem": {...overrides...}, "err": "E-..." or None, "excl": set of exception numbers to ignore}
"""
from __future__ import annotations

import itertools
from decimal import Decimal, localcontext

from .common import D, ZERO, ONE, HUNDRED, quant, on_grid


class Reject(Exception):
    """The structure breaks an A assertion: resample (3.1)."""


# ----------------------------------------------------------------------------------------------------------------- gates

def cond_true(c, facts, vals, rd, eno, ci):
    """One condition. Numeric conditions read a count fact or a value; CMP alternatives come from rd (E-alt:CMP)."""
    f = c["f"]
    op = c["op"]
    alt = rd.get("cmpalt", {}).get((eno, ci))
    if alt:
        op = alt
    if op == "is":
        x = facts.get(f)
        if x == "not recorded":
            raise Unknown(f)
        return x == c["v"]
    x = facts.get(f) if f in facts else vals.get(f)
    if x == "not recorded":
        raise Unknown(f)
    x = D(x)
    t = D(c["v"])
    return {"ge": x >= t, "gt": x > t, "le": x <= t, "lt": x < t}[op]


class Unknown(Exception):
    pass


def gate_true(e, facts, vals, rd):
    conn, join = e["conn"], e["join"]
    if rd.get("oralt", {}).get(e["no"]):
        join = {"or1": "or2", "or2": "or1"}.get(join, join)
    cs = [cond_true(c, facts, vals, rd, e["no"], i) for i, c in enumerate(e["conds"])]
    if join == "single":
        c = cs[0]
    elif join == "and":
        c = all(cs)
    elif join == "or1":
        c = any(cs)
    elif join == "or2":
        c = (sum(cs) == 1)
    else:
        raise ValueError(join)
    if conn == "UN1":
        if rd.get("err") == f"E-unless:{e['no']}":
            return c
        return not c
    return c  # O1 (and), O2 (plain if), O3 (or1): the rule applies exactly when its condition holds (W0)


# ----------------------------------------------------------------------------------------------------------------- core

def _r(v, unit, mode):
    return quant(v, unit, mode)


def _partial(q, mode):
    if mode in (None, "exact"):
        return q
    return quant(q, ONE, "ceiling" if mode == "ceil" else "floor")


class Tr:
    """Trace: arithmetic node count, node values, adjustment bind flags."""

    def __init__(self):
        self.ops = 0
        self.nodes = []        # (node_id, value) for every arithmetic node output, in order
        self.sel = 0
        self.flags = set()     # bind:cap, bind:floor, bind:exc, bind:round, bind:partial ...
        self.line_amts = []
        self.vals_at = {}      # named node values ("base", "fee", "before:<op>")

    def op(self, nid, v):
        self.ops += 1
        self.nodes.append((nid, v))
        return v


def _price_line(i, ln, rates, sem, err, tr, rnd_line, ri):
    p = ln["p"]
    if p == "stated":
        return rates[ln["a"]]
    if p == "blank":
        return D(0)
    if p == "mul":
        q = rates[ln["q"]]
        mode = sem.get("R5")
        q2 = _partial(q, mode)
        if q2 != q:
            tr.flags.add("bind:partial")
        if mode is not None:
            tr.sel += 1
        return ri(tr.op(f"line{i}", q2 * rates[ln["r"]]))
    if p == "perk":
        q, r, k = rates[ln["q"]], rates[ln["r"]], D(ln["k"])
        mode = sem.get("U3", "pro_rata")
        with localcontext() as c:
            c.prec = 60
            if mode == "pro_rata":
                v = tr.op(f"line{i}", r * q / k)
            else:
                blocks = quant(q / k, ONE, "ceiling" if mode == "full_k" else "floor")
                tr.op(f"line{i}.div", q / k)
                tr.sel += 1
                if blocks != q / k:
                    tr.flags.add("bind:partial")
                v = tr.op(f"line{i}", r * blocks)
        return ri(v)
    if p == "b4":
        q, r, x, m = rates[ln["q"]], rates[ln["r"]], rates[ln["b4x"]], rates[ln["b4m"]]
        if q <= x:
            return ri(tr.op(f"line{i}", q * r))
        base = tr.op(f"line{i}.base", x * r)
        over = tr.op(f"line{i}.over", q - x)
        prem = tr.op(f"line{i}.prem", over * m * r)
        return ri(tr.op(f"line{i}", base + prem))
    raise ValueError(p)


def run(P, rd, applied):
    """Value of the money program with the given applied exceptions (rule numbers, in order)."""
    sem = {**P.get("sem", {}), **rd.get("sem", {})}
    err = rd.get("err")
    tr = Tr()
    vals = {k: D(v) for k, v in P["vals"].items()}
    unit = D(P["unit"])
    r1 = sem.get("R1")
    r1u = D(sem.get("R1u", P["unit"])) if r1 else None
    if rd.get("norround"):
        r1 = None
    r4 = sem.get("R4alt")      # filter / hook alternative: 'display' or 'r1' (every intermediate rounded)

    def ri(v):
        if r4 == "display":
            return quant(v, unit, "half_up") if v >= 0 else v
        if r4 == "r1" and r1:
            return quant(v, r1u, r1) if v >= 0 else v
        return v

    # exceptions (X2 replace / add on rates, fixed charges or percentages; X3 handled by the caller)
    x2 = sem.get("X2", {})
    for no in applied:
        e = next(x for x in P["excs"] if x["no"] == no)
        form = x2.get(str(no), "replace" if e["kind"] in ("rate", "pct") else "add")
        if e["kind"] in ("rate", "pct", "add"):
            if form == "replace":
                vals[e["on"]] = vals[e["v"]]
            else:
                vals[e["on"]] = vals[e["on"]] + vals[e["v"]]
                tr.op(f"exc{no}", vals[e["on"]])
        tr.sel += 1
        tr.flags.add("bind:exc")
    stage = sem.get("R2", "final")
    order = sem.get("X1")
    steps = list(P["steps"])
    if order:
        steps = [steps[i] for i in order]
    # line-scope caps / minimums act on each line amount (X4 per line)
    x4 = sem.get("X4", {})
    line_caps = []
    rest = []
    for si, st in enumerate(steps):
        sc = x4.get(st.get("id", ""), st.get("scope", "total"))
        if st["op"] in ("cap", "min") and sc == "line":
            line_caps.append(st)
        else:
            rest.append(st)
    amts = []
    for i, ln in enumerate(P["lines"]):
        a = _price_line(i, ln, vals, sem, err, tr, None, ri)
        for st in line_caps:
            if st["op"] == "cap" and err != "E-cap":
                if a > vals[st["v"]]:
                    tr.flags.add("bind:cap")
                a = min(a, vals[st["v"]])
                tr.sel += 1
            if st["op"] == "min" and err != "E-floor":
                if a < vals[st["v"]]:
                    tr.flags.add("bind:floor")
                a = max(a, vals[st["v"]])
                tr.sel += 1
        if r1 and stage == "line":
            a2 = _r(a, r1u, r1)
            if a2 != a:
                tr.flags.add("bind:round")
            a = a2
            tr.sel += 1
        amts.append(a)
    tr.line_amts = amts
    terms = [a for a, ln in zip(amts, P["lines"]) if ln["p"] != "blank"] or [ZERO]
    v = terms[0]
    for a in terms[1:]:
        v = tr.op("sum", v + a)
    v = ri(v)
    tr.vals_at["base"] = v
    prev = v
    fee_val = None
    for st in rest:
        op = st["op"]
        tr.vals_at["before:" + st.get("id", op)] = v
        if op == "disc":
            v = ri(tr.op("disc", v * (HUNDRED - vals[st["v"]]) / HUNDRED))
        elif op == "disc2":
            p1, p2 = vals[st["v"][0]], vals[st["v"][1]]
            if sem.get("X5", "succ") == "succ":
                v1 = ri(tr.op("disc2a", v * (HUNDRED - p1) / HUNDRED))
                v = ri(tr.op("disc2b", v1 * (HUNDRED - p2) / HUNDRED))
            else:
                s = tr.op("disc2sum", p1 + p2)
                v = ri(tr.op("disc2", v * (HUNDRED - s) / HUNDRED))
        elif op == "pctof":
            v = ri(tr.op("pctof", v * vals[st["v"]] / HUNDRED))
            fee_val = v
        elif op == "fee":
            base = v if sem.get("X6", "after") == "after" else prev
            f = ri(tr.op("fee", base * vals[st["v"]] / HUNDRED))
            fee_val = f
            tr.vals_at["fee"] = f
            if P.get("target") != "fee":
                v = ri(tr.op("fee_add", v + f))
        elif op == "incfee":
            p = vals[st["v"]]
            form = sem.get("X7", "include")
            if form == "include":
                with localcontext() as c:
                    c.prec = 60
                    net = ri(tr.op("incfee_net", v * HUNDRED / (HUNDRED + p)))
                f = tr.op("incfee", v - net)
            else:
                f = tr.op("incfee", v * p / HUNDRED)
            fee_val = f
            tr.vals_at["fee"] = f
            v = f if P.get("target") == "fee" else v
        elif op == "cap":
            if err != "E-cap":
                if v > vals[st["v"]]:
                    tr.flags.add("bind:cap")
                v = min(v, vals[st["v"]])
            tr.sel += 1
        elif op == "min":
            if err != "E-floor":
                if v < vals[st["v"]]:
                    tr.flags.add("bind:floor")
                v = max(v, vals[st["v"]])
            tr.sel += 1
        elif op == "add":
            v = ri(tr.op("add", v + vals[st["v"]]))
        elif op == "ded":
            ds = [vals[k] for k in st["v"]]
            s = ds[0]
            for x in ds[1:]:
                s = tr.op("dedsum", s + x)
            v = ri(tr.op("ded", v - s))
        elif op == "allow":   # S5: an allowance (quantity x rate) added, capped by its cap (X4 on the allowance)
            q, r, cap = vals[st["v"][0]], vals[st["v"][1]], vals[st["v"][2]]
            al = tr.op("allow", q * r)
            if err != "E-cap":
                if al > cap:
                    tr.flags.add("bind:cap")
                al = min(al, cap)
            tr.sel += 1
            v = ri(tr.op("allow_add", v + al))
        elif op == "pctded":  # S5: a percentage deduction with a floor (minimum deduction) or a cap (maximum)
            p, lim, kind = vals[st["v"][0]], vals[st["v"][1]], st["lim"]
            dd = tr.op("pctded", v * p / HUNDRED)
            if r1 and stage == "line":
                dd = quant(dd, r1u, r1)
            if kind == "floor" and err != "E-floor":
                if dd < lim:
                    tr.flags.add("bind:floor")
                dd = max(dd, lim)
            if kind == "cap" and err != "E-cap":
                if dd > lim:
                    tr.flags.add("bind:cap")
                dd = min(dd, lim)
            tr.sel += 1
            v = ri(tr.op("pctded_sub", v - dd))
        elif op == "floor0":
            if sem.get("X8", "floor") == "floor":
                if v < 0:
                    tr.flags.add("bind:floor0")
                v = max(ZERO, v)
            tr.sel += 1
        else:
            raise ValueError(op)
        prev = tr.vals_at["before:" + st.get("id", op)]
    if P.get("target") == "fee" and fee_val is not None:
        v = fee_val
    tr.unrounded = v
    if r1 and stage == "final":
        if v < 0:
            raise Reject("rounding a negative value")
        v2 = _r(v, r1u, r1)
        if v2 != v:
            tr.flags.add("bind:round")
        v = v2
        tr.sel += 1
    tr.final = v
    return v, tr


def applicable(P, rd):
    facts = P.get("facts", {})
    vals = {k: D(v) for k, v in P["vals"].items()}
    out = []
    excl = rd.get("excl", set())
    for e in P.get("excs", []):
        if e["no"] in excl:
            continue
        if rd.get("err") == f"E-exc:{e['no']}":
            continue
        if gate_true(e, facts, vals, rd):
            out.append(e["no"])
    return out


def evaluate(P, rd=None):
    """(final value, trace) under reading rd; X3 picks among applicable exceptions."""
    rd = rd or {}
    sem = {**P.get("sem", {}), **rd.get("sem", {})}
    app = applicable(P, rd)
    if len(app) >= 2:
        form = sem.get("X3", "alone_lower")
        if form == "fold":
            return run(P, rd, sorted(app))
        best = None
        for no in sorted(app):
            v, tr = run(P, rd, [no])
            key = v if form == "alone_lower" else -v
            if best is None or key < best[0]:
                best = (key, v, tr, no)
        tr = best[2]
        tr.sel += 1
        return best[1], tr
    return run(P, rd, app)


# ----------------------------------------------------------------------------------------------------------------- labels

CMP = {"ge": lambda a, b: a >= b, "gt": lambda a, b: a > b, "le": lambda a, b: a <= b, "lt": lambda a, b: a < b}


def compared_value(P, rd):
    """The value the question's comparison reads: the reported (rounded) value, or under R3's T form the value with no
    rounding step at all (R3-15; branches from the unrounded run, which here never differ: no comparison sits between
    rounding steps on F2 money cards)."""
    sem = {**P.get("sem", {}), **rd.get("sem", {})}
    if sem.get("R3") == "unrounded":
        v, tr = evaluate(P, {**rd, "norround": True})
        return v
    v, tr = evaluate(P, rd)
    return v


def yn_label(P, rd=None):
    """Affirmative truth value of the question's proposition (before inverting cues) and the row label."""
    rd = rd or {}
    q = P["q"]
    if q["kind"] == "op":
        v, tr = evaluate(P, rd)
        aff = v > 0
    else:
        v = compared_value(P, rd)
        aff = CMP[q["cmp"]](v, D(q["T"]))
    lab = aff if q.get("neg", 0) % 2 == 0 else not aff
    return aff, lab


def outcome_of(v, outs, b1):
    """B1 band membership of v in the named outcome table (outs sorted by edge rank, shared edges)."""
    n = len(outs)
    for i, o in enumerate(outs):
        lo, hi = o.get("lo"), o.get("hi")
        lo = None if lo is None else D(lo)
        hi = None if hi is None else D(hi)
        if b1 == "upper":
            ok = (lo is None or v > lo) and (hi is None or v <= hi)
        else:
            ok = (lo is None or v >= lo) and (hi is None or v < hi)
        if ok:
            return o["name"]
    raise Reject("value in no band")


def choice_value(P, rd=None):
    v, tr = evaluate(P, rd or {})
    return v


def label(P, rd=None):
    """Row label under reading rd: yes/no -> bool; value -> Decimal; outcome -> outcome name."""
    q = P["q"]
    if q["kind"] in ("thr", "op"):
        return yn_label(P, rd)[1]
    if q["kind"] == "value":
        return choice_value(P, rd)
    if q["kind"] == "outcome":
        rd = rd or {}
        sem = {**P.get("sem", {}), **rd.get("sem", {})}
        v = compared_value(P, rd)
        return outcome_of(v, q["outs"], sem.get("B1o", q.get("b1", "upper")))
    raise ValueError(q["kind"])

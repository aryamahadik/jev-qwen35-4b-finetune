"""Behaviour atoms: small application-style rules that become IR functions (and class methods).

Each atom builder returns an AtomOut. Atoms are parameterised by seeded constants (thresholds, rates, table values),
so the same atom yields many different programs. All identifiers come from Idents (namespace.py, TRAINING salt).
An atom declares: which languages it supports (bash has no list parameters), whether it needs a class, its typed input
domain (exhaustive-enumerable, 25 to 5,000 points), its boundary values (for boundary/pairwise hidden-suite cases) and
the facts a program-rendered task card needs ("clauses": plain tuples; wording comes from a wording pool later).
"""
from . import ir as I
from . import domain as D
from .ir import (INT, STR, BOOL, INTS, STRS, i, s, v, fld, cst, bin_, add, sub, mul, lt, le, gt, ge, eq, ne, and_,
                 or_, cat, not_, call, mcall, lst, let, set_, ret, if_, for_, each, raise_)


class AtomOut:
    def __init__(self, kind):
        self.kind = kind
        self.funcs = []          # list of function dicts (names already final)
        self.consts = []         # [{name,type,value}]
        self.fields = []         # [{name,type,init}]   (stateful atoms)
        self.errs = set()        # abstract error ids used
        self.fn_specs = {}       # fname -> {domain, boundaries, clauses, atom}
        self.seq_domain = None   # stateful: sequence domain
        self.snapshot = None     # stateful: snapshot method name
        self.helper_use = None   # name of the free helper a method calls (for tests)


class Ctx:
    def __init__(self, rng, ids, key, lang, helpers=None):
        self.rng = rng
        self.ids = ids
        self.key = key
        self.lang = lang
        self.helpers = helpers or []     # free int->int functions available for methods to call [{name, params}]

    def fn(self, tag):
        return self.ids.func("%s.%s" % (self.key, tag))

    def var(self, tag):
        return self.ids.var("%s.%s" % (self.key, tag))

    def field(self, tag):
        return self.ids.field("%s.%s" % (self.key, tag))

    def const(self, tag):
        return self.ids.const("%s.%s" % (self.key, tag))

    def strv(self, tag):
        return self.ids.strval("%s.%s" % (self.key, tag))


def _spec(out, fname, atom, dom, bounds, clauses, extra=None):
    d = {"atom": atom, "domain": dom, "boundaries": sorted(set(bounds)), "clauses": clauses}
    d.update(extra or {})
    out.fn_specs[fname] = d


# ====================================================================================================== pure atoms
def tier_rate(c):
    rng = c.rng
    out = AtomOut("tier_rate")
    n = rng.choice([2, 3, 3, 4])
    ths = sorted(rng.sample(range(5, 90), n))
    rates = sorted(rng.sample(range(0, 45), n + 1))
    op = rng.choice(["<", "<="])
    mode = rng.choice(["rate", "amount", "net"])
    amount, rate = c.var("amount"), c.var("rate")
    chain = [set_(rate, i(rates[-1]))]
    for t, r in reversed(list(zip(ths, rates[:-1]))):
        chain = [if_(bin_(op, v(amount), i(t)), [set_(rate, i(r))], chain)]
    body = [let(rate, INT, i(0))] + chain
    if mode == "rate":
        body.append(ret(v(rate)))
    elif mode == "amount":
        body.append(ret(bin_("//", mul(v(amount), v(rate)), i(100))))
    else:
        body.append(ret(sub(v(amount), bin_("//", mul(v(amount), v(rate)), i(100)))))
    fname = c.fn("tier")
    out.funcs.append(I.func(fname, [[amount, INT]], INT, body))
    dom = [D.int_dom(amount, 0, max(ths[-1] + 8, 30))]
    _spec(out, fname, "tier_rate", dom, ths, [("tiers", ths, rates, op, mode)])
    return out


def capacity(c):
    rng = c.rng
    out = AtomOut("capacity")
    cap = rng.randint(6, 14)
    used, req, room = c.var("used"), c.var("req"), c.var("room")
    cname = c.const("cap")
    out.consts.append({"name": cname, "type": INT, "value": cap})
    fname = c.fn("fit")
    out.errs |= {"ERR_VALUE", "ERR_STATE"}
    body = [
        if_(le(v(req), i(0)), [raise_("ERR_VALUE")]),
        let(room, INT, sub(cst(cname), v(used))),
        if_(le(v(room), i(0)), [raise_("ERR_STATE")]),
        ret(["min", v(req), v(room)]),
    ]
    out.funcs.append(I.func(fname, [[used, INT], [req, INT]], INT, body))
    dom = [D.int_dom(used, 0, cap + 2), D.int_dom(req, 0, min(cap, 9))]
    _spec(out, fname, "capacity", dom, [cap, 0], [("capacity", cap)])
    return out


def page_window(c):
    rng = c.rng
    out = AtomOut("page_window")
    size = rng.randint(3, 7)
    total, page, start = c.var("total"), c.var("page"), c.var("start")
    sname = c.const("size")
    out.consts.append({"name": sname, "type": INT, "value": size})
    fname = c.fn("window")
    body = [
        let(start, INT, mul(v(page), cst(sname))),
        if_(ge(v(start), v(total)), [ret(i(0))]),
        ret(["min", cst(sname), sub(v(total), v(start))]),
    ]
    out.funcs.append(I.func(fname, [[total, INT], [page, INT]], INT, body))
    dom = [D.int_dom(total, 0, 20), D.int_dom(page, 0, 5)]
    _spec(out, fname, "page_window", dom, [size, 2 * size, 3 * size], [("page", size)])
    return out


def retry_delay(c):
    rng = c.rng
    out = AtomOut("retry_delay")
    cap = rng.randint(20, 90)
    grow = rng.choice(["double", "step"])
    step = rng.randint(2, 7)
    attempt, base, d, k = c.var("attempt"), c.var("start"), c.var("delay"), c.var("k")
    capn = c.const("cap")
    out.consts.append({"name": capn, "type": INT, "value": cap})
    nxt = mul(v(d), i(2)) if grow == "double" else add(v(d), i(step))
    body = [let(d, INT, v(base)), for_(k, i(0), v(attempt), [set_(d, ["min", nxt, cst(capn)])]), ret(v(d))]
    fname = c.fn("backoff")
    out.funcs.append(I.func(fname, [[attempt, INT], [base, INT]], INT, body))
    dom = [D.int_dom(attempt, 0, 7), D.int_dom(base, 1, 6)]
    _spec(out, fname, "retry_delay", dom, [cap], [("backoff", grow, step, cap)])
    return out


def batch_count(c):
    rng = c.rng
    out = AtomOut("batch_count")
    size = rng.randint(4, 9)
    unit = rng.randint(2, 9)
    sur = rng.randint(1, 5)
    n, full, rest = c.var("n"), c.var("full"), c.var("rest")
    fname = c.fn("bill")
    body = [
        let(full, INT, bin_("//", v(n), i(size))),
        let(rest, INT, bin_("%", v(n), i(size))),
        if_(gt(v(rest), i(0)), [set_(full, add(v(full), i(1))), ret(add(mul(v(full), i(unit)), i(sur)))]),
        ret(mul(v(full), i(unit))),
    ]
    out.funcs.append(I.func(fname, [[n, INT]], INT, body))
    dom = [D.int_dom(n, 0, 6 * size)]
    _spec(out, fname, "batch_count", dom, [size, 2 * size, 3 * size], [("batch", size, unit, sur)])
    return out


def role_match(c):
    rng = c.rng
    out = AtomOut("role_match")
    r1, r2, r3, other = c.strv("r1"), c.strv("r2"), c.strv("r3"), c.strv("rx")
    role, level = c.var("role"), c.var("level")
    t1 = rng.randint(2, 7)
    cap2 = rng.randint(2, 6)
    hi1, lo1 = rng.randint(4, 9), rng.randint(1, 3)
    body = [
        if_(eq(v(role), s(r1)), [if_(ge(v(level), i(t1)), [ret(i(hi1))], [ret(i(lo1))])]),
        if_(eq(v(role), s(r2)), [ret(["min", v(level), i(cap2)])]),
        ret(i(0)),
    ]
    fname = c.fn("grant")
    out.funcs.append(I.func(fname, [[role, STR], [level, INT]], INT, body))
    dom = [D.str_set(role, [r1, r2, r3, other]), D.int_dom(level, 0, 9)]
    _spec(out, fname, "role_match", dom, [t1, cap2], [("roles", r1, r2, t1, hi1, lo1, cap2)])
    return out


def fmt_label(c):
    rng = c.rng
    out = AtomOut("fmt_label")
    sep = rng.choice(["-", ":", "/", "."])
    width = rng.choice([2, 3])
    hi = rng.randint(9, 14)
    tail = c.strv("tail")
    code, kind, tag = c.var("code"), c.var("kind"), c.var("tag")
    k1, k2, k3 = c.strv("k1"), c.strv("k2"), c.strv("k3")
    body = [
        let(tag, STR, cat(v(kind), s(sep))),
        if_(gt(v(code), i(hi)), [ret(cat(v(tag), s(tail)))]),
        ret(cat(v(tag), ["zpad", v(code), i(width)])),
    ]
    fname = c.fn("label")
    out.funcs.append(I.func(fname, [[code, INT], [kind, STR]], STR, body))
    dom = [D.int_dom(code, 0, hi + 3), D.str_set(kind, [k1, k2, k3])]
    _spec(out, fname, "fmt_label", dom, [hi], [("label", sep, width, hi, tail)])
    return out


def unit_convert(c):
    rng = c.rng
    out = AtomOut("unit_convert")
    n = rng.choice([3, 4, 4, 5])
    factors = [rng.randint(2, 30) for _ in range(n)]
    value, unit = c.var("value"), c.var("unit")
    tname = c.const("factors")
    out.consts.append({"name": tname, "type": INTS, "value": factors})
    fname = c.fn("convert")
    body = [ret(bin_("//", mul(v(value), ["idx", cst(tname), v(unit)]), i(10)))]
    out.funcs.append(I.func(fname, [[value, INT], [unit, INT]], INT, body))
    dom = [D.int_dom(value, 0, 9), D.int_dom(unit, 0, n - 1)]
    _spec(out, fname, "unit_convert", dom, [], [("convert", factors)])
    return out


def validate_record(c):
    rng = c.rng
    out = AtomOut("validate_record")
    lo, hi = rng.randint(2, 6), rng.randint(14, 30)
    age, name = c.var("age"), c.var("name")
    nm = c.strv("nm")
    body = [
        if_(eq(["len", v(name)], i(0)), [ret(i(1))]),
        if_(lt(v(age), i(lo)), [ret(i(2))]),
        if_(gt(v(age), i(hi)), [ret(i(3))]),
        ret(i(0)),
    ]
    fname = c.fn("check")
    out.funcs.append(I.func(fname, [[age, INT], [name, STR]], INT, body))
    dom = [D.int_dom(age, 0, hi + 3), D.str_set(name, ["", nm])]
    _spec(out, fname, "validate_record", dom, [lo, hi], [("validate", lo, hi)])
    return out


def route_follow(c):
    rng = c.rng
    out = AtomOut("route_follow")
    n = rng.choice([4, 5, 6])
    nxt = [rng.randrange(n) for _ in range(n)]
    start, steps, cur, k = c.var("start"), c.var("steps"), c.var("cur"), c.var("k")
    tname = c.const("next")
    out.consts.append({"name": tname, "type": INTS, "value": nxt})
    body = [let(cur, INT, v(start)), for_(k, i(0), v(steps), [set_(cur, ["idx", cst(tname), v(cur)])]), ret(v(cur))]
    fname = c.fn("follow")
    out.funcs.append(I.func(fname, [[start, INT], [steps, INT]], INT, body))
    dom = [D.int_dom(start, 0, n - 1), D.int_dom(steps, 0, 6)]
    _spec(out, fname, "route_follow", dom, [], [("route", nxt)])
    return out


# ---- list atoms (no bash: lists cannot be function arguments there)
def sum_over(c):
    rng = c.rng
    out = AtomOut("sum_over")
    mode = rng.choice(["sum", "count", "weighted"])
    xs, limit, acc, x = c.var("xs"), c.var("limit"), c.var("acc"), c.var("x")
    upd = {"sum": add(v(acc), v(x)), "count": add(v(acc), i(1)), "weighted": add(v(acc), mul(v(x), i(rng.randint(2, 4))))}[mode]
    op = rng.choice(["<=", "<"])
    body = [let(acc, INT, i(0)), each(x, v(xs), [if_(bin_(op, v(x), v(limit)), [set_(acc, upd)])]), ret(v(acc))]
    fname = c.fn("total")
    out.funcs.append(I.func(fname, [[xs, INTS], [limit, INT]], INT, body))
    elems = sorted(rng.sample(range(0, 7), 3))
    dom = [D.list_dom(xs, INTS, elems, 3), D.int_set(limit, [1, 2, 3, 5])]
    _spec(out, fname, "sum_over", dom, [], [("sum_over", mode, op)])
    return out


def dedupe_count(c):
    rng = c.rng
    out = AtomOut("dedupe_count")
    mode = rng.choice(["count", "sum", "weighted", "positive"])
    k = rng.randint(2, 4)
    t0 = rng.randint(1, 3)
    xs, seen, x, acc = c.var("xs"), c.var("seen"), c.var("x"), c.var("acc")
    gain = {"count": i(1), "sum": v(x), "weighted": mul(v(x), i(k)), "positive": i(1)}[mode]
    inner = [["push", v(seen), v(x)], set_(acc, add(v(acc), gain))]
    if mode == "positive":
        inner = [if_(gt(v(x), i(t0)), inner)]
    body = [let(seen, INTS, lst(INTS, [])), let(acc, INT, i(0)),
            each(x, v(xs), [if_(not_(["has", v(seen), v(x)]), inner)]), ret(v(acc))]
    fname = c.fn("distinct")
    out.funcs.append(I.func(fname, [[xs, INTS]], INT, body))
    elems = sorted(rng.sample(range(1, 8), 3))
    dom = [D.list_dom(xs, INTS, elems, 4)]
    _spec(out, fname, "dedupe_count", dom, [t0], [("dedupe", mode, k, t0)])
    return out


def merge_overrides(c):
    rng = c.rng
    out = AtomOut("merge_overrides")
    base, over, res, k = c.var("base"), c.var("over"), c.var("out"), c.var("k")
    t = rng.randint(0, 3)
    mode = rng.choice(["override", "override", "max"])
    cmp_op = rng.choice([">", ">="])
    if mode == "override":
        cond = and_(lt(v(k), ["len", v(over)]), bin_(cmp_op, ["idx", v(over), v(k)], i(t)))
        yes, no = ["idx", v(over), v(k)], ["idx", v(base), v(k)]
    else:
        cond = and_(lt(v(k), ["len", v(over)]), bin_(cmp_op, ["idx", v(over), v(k)], ["idx", v(base), v(k)]))
        yes, no = ["idx", v(over), v(k)], ["idx", v(base), v(k)]
    body = [
        let(res, INTS, lst(INTS, [])),
        for_(k, i(0), ["len", v(base)], [if_(cond, [["push", v(res), yes]], [["push", v(res), no]])]),
        ret(v(res)),
    ]
    fname = c.fn("overlay")
    out.funcs.append(I.func(fname, [[base, INTS], [over, INTS]], INTS, body))
    e1 = sorted(rng.sample(range(1, 9), 2))
    e2 = sorted(set([0, t + 1, t + 3, rng.randint(1, 9)]))[:3]
    dom = [D.list_dom(base, INTS, e1, 3), D.list_dom(over, INTS, e2, 3)]
    _spec(out, fname, "merge_overrides", dom, [t], [("merge", mode, cmp_op, t)])
    return out


def log_tally(c):
    rng = c.rng
    out = AtomOut("log_tally")
    mode = rng.choice(["count", "count", "not", "weighted"])
    w = rng.randint(2, 5)
    lines, pfx, n, ln = c.var("lines"), c.var("pfx"), c.var("n"), c.var("line")
    stem = c.strv("stem")
    other = c.strv("other")
    test = ["starts", v(ln), v(pfx)]
    if mode == "not":
        test = not_(test)
    gain = mul(["len", v(ln)], i(w)) if mode == "weighted" else i(1)
    body = [let(n, INT, i(0)), each(ln, v(lines), [if_(test, [set_(n, add(v(n), gain))])]), ret(v(n))]
    fname = c.fn("tally")
    out.funcs.append(I.func(fname, [[lines, STRS], [pfx, STR]], INT, body))
    items = [stem + "x", stem[:2] + "y", other[:3]]
    dom = [D.list_dom(lines, STRS, items, 3), D.str_set(pfx, [stem[:1], stem[:2], other[:2]])]
    _spec(out, fname, "log_tally", dom, [], [("tally", mode, w)])
    return out


# ====================================================================================================== stateful atoms
def ledger(c):
    rng = c.rng
    out = AtomOut("ledger")
    cap = rng.randint(12, 40)
    total, count = c.field("total"), c.field("count")
    out.fields = [{"name": total, "type": INT, "init": 0}, {"name": count, "type": INT, "init": 0}]
    capn = c.const("cap")
    out.consts.append({"name": capn, "type": INT, "value": cap})
    out.errs |= {"ERR_VALUE", "ERR_STATE"}
    x, t = c.var("x"), c.var("t")
    add_n, ref_n, snap_n = c.fn("add"), c.fn("refund"), c.fn("snap")
    helper = None
    for h in c.helpers:
        if h["params"][0][1] == INT and len(h["params"]) == 1 and h["ret"] == INT:
            helper = h
            break
    body_add = [if_(le(v(x), i(0)), [raise_("ERR_VALUE")])]
    if helper and rng.random() < 0.7:
        adj = c.var("adj")
        body_add += [let(adj, INT, call(helper["name"], v(x))), let(t, INT, add(fld(total), v(adj)))]
        out.helper_use = helper["name"]
    else:
        body_add.append(let(t, INT, add(fld(total), v(x))))
    body_add += [if_(gt(v(t), cst(capn)), [raise_("ERR_STATE")]),
                 ["setf", total, v(t)], ["setf", count, add(fld(count), i(1))], ret(v(t))]
    out.funcs.append(I.func(add_n, [[x, INT]], INT, body_add, scope="method"))
    y = c.var("y")
    body_ref = [if_(gt(v(y), fld(total)), [raise_("ERR_STATE")]), ["setf", total, sub(fld(total), v(y))], ret(fld(total))]
    out.funcs.append(I.func(ref_n, [[y, INT]], INT, body_ref, scope="method"))
    out.funcs.append(I.func(snap_n, [], INT, [ret(add(mul(fld(total), i(100)), fld(count)))], scope="method"))
    a_vals = sorted(rng.sample(range(1, 12), 3))
    r_vals = sorted(rng.sample(range(1, 8), 2))
    out.seq_domain = {"ops": [{"fn": add_n, "params": [D.int_set(x, a_vals)]}, {"fn": ref_n, "params": [D.int_set(y, r_vals)]}],
                      "maxlen": 3}
    out.snapshot = snap_n
    for f_ in (add_n, ref_n):
        _spec(out, f_, "ledger", None, [cap], [("ledger", cap)])
    return out


def queue_fifo(c):
    rng = c.rng
    out = AtomOut("queue_fifo")
    cap = rng.randint(2, 4)
    q = c.field("q")
    out.fields = [{"name": q, "type": INTS, "init": []}]
    capn = c.const("cap")
    out.consts.append({"name": capn, "type": INT, "value": cap})
    out.errs |= {"ERR_STATE"}
    x, h, acc, e = c.var("x"), c.var("h"), c.var("acc"), c.var("e")
    put_n, take_n, snap_n = c.fn("put"), c.fn("take"), c.fn("snap")
    lifo = rng.random() < 0.4
    out.funcs.append(I.func(put_n, [[x, INT]], INT, [
        if_(ge(["len", fld(q)], cst(capn)), [raise_("ERR_STATE")]), ["push", fld(q), v(x)], ret(["len", fld(q)])], scope="method"))
    out.funcs.append(I.func(take_n, [], INT, [
        if_(eq(["len", fld(q)], i(0)), [raise_("ERR_STATE")]),
        ["popto" if lifo else "shiftto", h, INT, fld(q)], ret(v(h))], scope="method"))
    out.funcs.append(I.func(snap_n, [], INT, [
        let(acc, INT, i(0)), each(e, fld(q), [set_(acc, add(mul(v(acc), i(10)), v(e)))]), ret(v(acc))], scope="method"))
    vals = sorted(rng.sample(range(1, 9), 2))
    out.seq_domain = {"ops": [{"fn": put_n, "params": [D.int_set(x, vals)]}, {"fn": take_n, "params": []}], "maxlen": 4}
    out.snapshot = snap_n
    for f_ in (put_n, take_n):
        _spec(out, f_, "queue_fifo", None, [cap], [("queue", cap, "lifo" if lifo else "fifo")])
    return out


def tally_counts(c):
    rng = c.rng
    out = AtomOut("tally_counts")
    kk = rng.choice([3, 4])
    counts = c.field("counts")
    out.fields = [{"name": counts, "type": INTS, "init": [0] * kk}]
    out.errs |= {"ERR_INDEX"}
    k, e, acc = c.var("k"), c.var("e"), c.var("acc")
    bump_n, snap_n = c.fn("bump"), c.fn("snap")
    step = rng.randint(1, 3)
    out.funcs.append(I.func(bump_n, [[k, INT]], INT, [
        if_(ge(v(k), ["len", fld(counts)]), [raise_("ERR_INDEX")]),
        ["sidx", fld(counts), v(k), add(["idx", fld(counts), v(k)], i(step))], ret(["idx", fld(counts), v(k)])], scope="method"))
    out.funcs.append(I.func(snap_n, [], INT, [
        let(acc, INT, i(0)), each(e, fld(counts), [set_(acc, add(mul(v(acc), i(3)), v(e)))]), ret(v(acc))], scope="method"))
    out.seq_domain = {"ops": [{"fn": bump_n, "params": [D.int_dom(k, 0, kk)]}], "maxlen": 3}
    out.snapshot = snap_n
    _spec(out, bump_n, "tally_counts", None, [kk], [("counts", kk, step)])
    return out


def retry_state(c):
    rng = c.rng
    out = AtomOut("retry_state")
    cap = rng.randint(20, 60)
    base = rng.randint(1, 4)
    mx = rng.randint(2, 4)
    att, dly = c.field("attempts"), c.field("delay")
    out.fields = [{"name": att, "type": INT, "init": 0}, {"name": dly, "type": INT, "init": base}]
    capn = c.const("cap")
    out.consts.append({"name": capn, "type": INT, "value": cap})
    out.errs |= {"ERR_STATE"}
    fail_n, ok_n, snap_n = c.fn("fail"), c.fn("ok"), c.fn("snap")
    out.funcs.append(I.func(fail_n, [], INT, [
        ["setf", att, add(fld(att), i(1))], ["setf", dly, ["min", mul(fld(dly), i(2)), cst(capn)]],
        if_(gt(fld(att), i(mx)), [raise_("ERR_STATE")]), ret(fld(dly))], scope="method"))
    out.funcs.append(I.func(ok_n, [], INT, [["setf", att, i(0)], ["setf", dly, i(base)], ret(i(0))], scope="method"))
    out.funcs.append(I.func(snap_n, [], INT, [ret(add(mul(fld(att), i(100)), fld(dly)))], scope="method"))
    out.seq_domain = {"ops": [{"fn": fail_n, "params": []}, {"fn": ok_n, "params": []}], "maxlen": 5}
    out.snapshot = snap_n
    for f_ in (fail_n, ok_n):
        _spec(out, f_, "retry_state", None, [mx], [("retry_state", base, cap, mx)])
    return out


def note_counter(c):
    rng = c.rng
    out = AtomOut("note_counter")
    nm, no = c.field("matched"), c.field("others")
    out.fields = [{"name": nm, "type": INT, "init": 0}, {"name": no, "type": INT, "init": 0}]
    stem = c.strv("stem")
    pf = stem[:2]
    pc = c.const("prefix")
    out.consts.append({"name": pc, "type": STR, "value": pf})
    inc_m, inc_o = rng.randint(1, 3), rng.randint(1, 2)
    scale = rng.choice([10, 100, 1000])
    ret_mode = rng.choice(["matched", "others", "total"])
    line = c.var("line")
    note_n, sum_n = c.fn("note"), c.fn("summary")
    rv = {"matched": fld(nm), "others": fld(no), "total": add(fld(nm), fld(no))}[ret_mode]
    out.funcs.append(I.func(note_n, [[line, STR]], INT, [
        if_(["starts", v(line), cst(pc)], [["setf", nm, add(fld(nm), i(inc_m))]], [["setf", no, add(fld(no), i(inc_o))]]),
        ret(rv)], scope="method"))
    out.funcs.append(I.func(sum_n, [], INT, [ret(add(mul(fld(nm), i(scale)), fld(no)))], scope="method"))
    items = [pf + "a", pf + "b", c.strv("o1")[:3] + "z"]
    out.seq_domain = {"ops": [{"fn": note_n, "params": [D.str_set(line, items)]}], "maxlen": 3}
    out.snapshot = sum_n
    _spec(out, note_n, "note_counter", None, [], [("note", pf, inc_m, inc_o)])
    return out


# ====================================================================================================== registry
PURE = {
    "tier_rate": (tier_rate, True),
    "capacity": (capacity, True),
    "page_window": (page_window, True),
    "retry_delay": (retry_delay, True),
    "batch_count": (batch_count, True),
    "role_match": (role_match, True),
    "fmt_label": (fmt_label, True),
    "unit_convert": (unit_convert, True),
    "validate_record": (validate_record, True),
    "route_follow": (route_follow, True),
    "sum_over": (sum_over, False),
    "dedupe_count": (dedupe_count, False),
    "merge_overrides": (merge_overrides, False),
    "log_tally": (log_tally, False),
}
STATEFUL = {
    "ledger": (ledger, True),
    "queue_fifo": (queue_fifo, True),
    "tally_counts": (tally_counts, True),
    "retry_state": (retry_state, True),
    "note_counter": (note_counter, True),
}

# generic application areas (names only; the same 15 areas as the frozen list, id -> atoms that fit the area)
DOMAIN_ATOMS = {
    "cdom01": (["capacity", "unit_convert", "page_window"], ["ledger", "queue_fifo"]),
    "cdom02": (["tier_rate", "batch_count", "sum_over", "unit_convert"], ["ledger"]),
    "cdom03": (["tier_rate", "unit_convert", "fmt_label"], ["ledger"]),
    "cdom04": (["capacity", "page_window", "batch_count"], ["ledger", "queue_fifo"]),
    "cdom05": (["role_match", "validate_record"], ["note_counter"]),
    "cdom06": (["dedupe_count", "merge_overrides", "log_tally"], ["tally_counts"]),
    "cdom07": (["retry_delay", "capacity"], ["retry_state"]),
    "cdom08": (["fmt_label", "log_tally", "role_match"], ["note_counter"]),
    "cdom09": (["unit_convert", "tier_rate"], ["ledger"]),
    "cdom10": (["page_window", "batch_count", "sum_over"], ["tally_counts"]),
    "cdom11": (["merge_overrides", "role_match", "validate_record"], ["note_counter"]),
    "cdom12": (["route_follow", "unit_convert"], ["tally_counts"]),
    "cdom13": (["log_tally", "fmt_label", "validate_record"], ["note_counter", "tally_counts"]),
    "cdom14": (["batch_count", "sum_over", "capacity"], ["queue_fifo"]),
    "cdom15": (["validate_record", "role_match", "fmt_label"], ["ledger", "note_counter"]),
}
DOMAIN_IDS = tuple(sorted(DOMAIN_ATOMS))

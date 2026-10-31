"""Solver B (G2): a declarative re-solver over the PARSED structure, written from G0 F1 v7 sections 1-2 only.

z3 is not installed in the project venv and F1 may not download packages; C_DATA_SPEC v4 2.2 F1 allows "z3 (MIT) or
brute force over the parsed rules", so solver B is a brute-force declarative evaluator of a different paradigm from
solver A (imperative forward chaining with critical points):
  - rule versions as per-rule timelines (the last event at or before g), not a replayed rule table;
  - firing as a least fixpoint over sets, effectiveness by a well-founded sweep over the exception graph;
  - precedence as the set of undominated candidates (set comprehension over a dominance relation);
  - open world by enumerating one representative of every region of each unknown field (an interval partition built
    from all canonical cut points), not by critical points;
  - depth A by brute force over all notice subsets with its own removal closure.
"""
from __future__ import annotations

import itertools
from decimal import Decimal

CBD = "__CBD__"


class BError(Exception):
    pass


# ---------------------------------------------------------------- truth of literals (own implementation)

def _step(a):
    return a.step if a.type == "num" else 1


def truth(lit, attrs, v):
    a = attrs[lit.attr]
    x = v[lit.attr]
    o, g = lit.op, lit.args
    if a.type == "bool":
        return x is g[0]
    if a.type == "cat":
        hit = x in set(g)
        return hit if o == "in" else not hit
    table = {
        "ge": lambda: x >= g[0], "gt": lambda: x > g[0], "le": lambda: x <= g[0], "within": lambda: x <= g[0],
        "lt": lambda: x < g[0], "between": lambda: g[0] <= x <= g[1], "before": lambda: x < g[0],
        "onbefore": lambda: x <= g[0], "after": lambda: x > g[0], "onafter": lambda: x >= g[0],
        "fromto": lambda: g[0] <= x <= g[1],
    }
    return table[o]()


def item_truth(it, attrs, v):
    xs = [truth(m, attrs, v) for m in it.mem]
    return {"lit": lambda: xs[0], "not": lambda: not xs[0], "or": lambda: any(xs), "xor": lambda: sum(xs) == 1,
            "all": lambda: all(xs), "any": lambda: any(xs), "kofn": lambda: sum(xs) >= it.k}[it.kind]()


def met_own(r, attrs, v):
    if not all(item_truth(it, attrs, v) for it in r.items):
        return False
    if r.unless is not None and truth(r.unless, attrs, v):
        return False
    return True


# ---------------------------------------------------------------- canonical identity (own)

def ccanon(lit, attrs):
    a = attrs[lit.attr]
    s = _step(a)
    o, g = lit.op, tuple(lit.args)
    if a.type == "num":
        o, g = {"gt": ("ge", (g[0] + s,)), "lt": ("le", (g[0] - s,)), "within": ("le", g)}.get(o, (o, g))
    elif a.type == "date":
        o, g = {"before": ("le", (g[0] - 1,)), "onbefore": ("le", g), "after": ("ge", (g[0] + 1,)),
                "onafter": ("ge", g), "fromto": ("between", g)}[o]
    elif a.type == "cat":
        g = tuple(sorted(g))
    return (lit.attr, o, g)


def items_of(r, attrs):
    out = set()
    for it in r.items:
        out.add((it.kind, tuple(sorted((ccanon(m, attrs) for m in it.mem), key=repr)), it.k))
    if r.unless is not None:
        out.add(("not", (ccanon(r.unless, attrs),), 0))
    return out


# ---------------------------------------------------------------- versions in force (timeline per rule)

def versions(S, g, skip=frozenset()):
    """{rid: (rule text, text date)} in force at g. Each rule id gets its own event timeline."""
    P = S.policy
    events = {}
    for r in S.rules:
        events.setdefault(r.rid, []).append((-1, 0, "base", r))
    for n in S.notices:
        if n.num in skip or n.edate > g:
            continue
        rid = n.target if n.ntype != "insert" else n.rule.rid
        events.setdefault(rid, []).append((n.edate, n.num, n.ntype, n))
    out = {}
    for rid, evs in events.items():
        evs.sort(key=lambda e: (e[0], e[1]))
        cur = None
        when = None
        for d, num, kind, obj in evs:
            if kind == "base":
                cur, when = obj, (obj.date if obj.date is not None else P.B)
            elif kind == "insert":
                cur, when = obj.rule, d
            elif kind == "replace":
                if cur is None:
                    continue
                nr = obj.rule
                # the whole new text, kind and exception target kept; an only-if rule keeps its named outcome Y
                cur = type(nr)(rid=cur.rid, kind=cur.kind, items=nr.items, unless=nr.unless,
                               out=(cur.out if cur.kind == "onlyif" else nr.out if cur.kind in ("gen", "oexc")
                                    else None),
                               target=cur.target, tier=nr.tier, date=None, last=nr.last)
                when = d
            elif kind == "repeal":
                cur = None
        if cur is None:
            continue
        if cur.last is not None and g > cur.last:
            continue
        out[rid] = (cur, when)
    # exceptions whose target is not in force are not in force (to a fixpoint)
    while True:
        drop = [rid for rid, (r, w) in out.items() if r.kind in ("pexc", "oexc") and r.target not in out]
        if not drop:
            break
        for rid in drop:
            del out[rid]
    return out


# ---------------------------------------------------------------- one closed case

def closed(S, v, notrec=frozenset(), skip=frozenset()):
    P = S.policy
    attrs = S.attrs
    if P.world == "missing" and any(f in notrec for f in P.listed):
        return {"final": P.M, "src": "M", "winner": None, "X": 0, "P": 0, "O": 0, "basis": "M"}
    g = v[P.gov]
    V = versions(S, g, skip)
    # least fixpoint of "fires"
    fired = set()
    while True:
        new = set(fired)
        for rid, (r, w) in V.items():
            if r.kind == "onlyif":
                continue
            own = met_own(r, attrs, v)
            if r.kind == "gen" and own:
                new.add(rid)
            elif r.kind in ("pexc", "oexc") and own and r.target in new:
                new.add(rid)
        if new == fired:
            break
        fired = new
    excs = {rid: r for rid, (r, w) in V.items() if r.kind in ("pexc", "oexc")}
    targeted_by = {}
    for rid, r in excs.items():
        targeted_by.setdefault(r.target, set()).add(rid)
    # well-founded sweep: process exceptions in decreasing distance from the exceptions nothing targets
    effective = {}
    pending = set(excs)
    guard = 0
    while pending:
        guard += 1
        if guard > 100:
            raise BError("cycle")
        ready = [e for e in pending if all(x in effective for x in targeted_by.get(e, ()))]
        if not ready:
            raise BError("cycle")
        for e in ready:
            effective[e] = (e in fired) and not any(effective[x] for x in targeted_by.get(e, ()))
            pending.discard(e)
    switched = {rid for rid in V if any(effective.get(x) for x in targeted_by.get(rid, ()))}

    def level(rid):
        lv = 0
        while rid in excs:
            lv += 1
            rid = excs[rid].target
        return lv
    X = max([level(e) for e in excs if e in fired], default=0)
    C = {rid for rid, (r, w) in V.items() if r.kind in ("gen", "oexc") and rid in fired and rid not in switched}
    outs = {V[c][0].out for c in C}
    Pv = 1 if len(outs) >= 2 else 0

    # dominance relations
    def inherited(rid, seen=()):
        r = V[rid][0]
        s = items_of(r, attrs)
        if r.kind in ("pexc", "oexc") and r.target in V and r.target not in seen:
            s |= inherited(r.target, seen + (rid,))
        return s
    rank = display_rank_b(S, V, g)

    def dom(pol, a, b):
        if pol == "SPEC":
            return inherited(a) > inherited(b)
        if pol == "LATER":
            return V[a][1] > V[b][1]
        if pol == "PRIORITY":
            return V[a][0].tier < V[b][0].tier
        return rank[a] < rank[b]

    def undominated(pol, pool):
        return {c for c in pool if not any(V[d][0].out != V[c][0].out and dom(pol, d, c) for d in pool)}
    src = None
    if not C:
        o, src = P.default, "D"
    elif len(outs) == 1:
        o, src = next(iter(outs)), "RULE"
    else:
        left = undominated(P.prim, C)
        if len({V[c][0].out for c in left}) > 1 and P.sec:
            left = undominated(P.sec, left)
        lo = {V[c][0].out for c in left}
        if len(lo) == 1:
            o, src = next(iter(lo)), "RULE"
        else:
            if P.tie == "none":
                raise BError("tie on a card without a tie rule")
            o = P.escalate if P.tie == "esc" else [x for x in P.strict if x in lo][0]
            src = "T"
    O = 0
    names = [rid for rid, (r, w) in V.items() if r.kind == "onlyif" and r.out == o]
    final = o
    if names and not all(met_own(V[n][0], attrs, v) for n in names):
        final, src, O = P.fallback, "F", 1
    winner = None
    if src == "RULE":
        hold = [c for c in C if V[c][0].out == final]
        src = "ONE" if len(hold) == 1 else "MANY"
        winner = hold[0] if len(hold) == 1 else None
    basis = {"D": "D", "T": "T", "F": "F", "M": "M", "ONE": winner, "MANY": None}[src]
    return {"final": final, "src": src, "winner": winner, "X": X, "P": Pv if src != "D" else 0, "O": O,
            "basis": basis}


def display_rank_b(S, V, g):
    if S.s3_rows is None:
        pos = {t: i for i, t in enumerate(S.order)}
        src_of = {}
        for r in S.rules:
            src_of[r.rid] = ("r", r.rid)
        for n in sorted(S.notices, key=lambda n: (n.edate, n.num)):
            if n.edate > g:
                continue
            rid = n.target if n.ntype != "insert" else n.rule.rid
            if n.ntype in ("replace", "insert"):
                src_of[rid] = ("n", n.num)
        return {rid: pos.get(src_of.get(rid), 10 ** 6) for rid in V}
    seq = list(S.s3_rows)
    for n in sorted(S.notices, key=lambda n: (n.edate, n.num)):
        if n.ntype != "insert" or n.edate > g:
            continue
        p = n.pos or ("bottom",)
        if p[0] == "top":
            seq = [n.rule.rid] + seq
        elif p[0] == "bottom":
            seq = seq + [n.rule.rid]
        else:
            i = seq.index(p[1])
            seq = seq[:i + 1] + [n.rule.rid] + seq[i + 1:]
    live = [x for x in seq if x in V]
    return {rid: i for i, rid in enumerate(live)}


# ---------------------------------------------------------------- open world: one value per region

def region_reps(S, key):
    a = S.attrs[key]
    if a.type == "bool":
        return [True, False]
    if a.type == "cat":
        return list(a.values)
    s = _step(a)
    cuts = set()

    def scan(r):
        if r is None:
            return
        lits = [m for it in r.items for m in it.mem] + ([r.unless] if r.unless is not None else [])
        for m in lits:
            if m.attr != key:
                continue
            c = ccanon(m, S.attrs)
            if c[1] == "ge":
                cuts.add(c[2][0])
            elif c[1] == "le":
                cuts.add(c[2][0] + s)
            elif c[1] == "between":
                cuts.add(c[2][0])
                cuts.add(c[2][1] + s)
    for r in S.rules:
        scan(r)
    for n in S.notices:
        scan(n.rule)
    lo, hi = a.lo, a.hi
    pts = sorted(x for x in cuts if lo < x <= hi)
    reps = [lo] + pts
    return [x for x in reps if lo <= x <= hi]


def worlds(S, case):
    keys = sorted(case.unknown)
    if not keys:
        yield dict(case.vals)
        return
    for combo in itertools.product(*[region_reps(S, k) for k in keys]):
        v = dict(case.vals)
        v.update(zip(keys, combo))
        bad = False
        for k, a in S.attrs.items():
            if a.type == "bool" and a.presup and v.get(k) is True and v.get(a.presup) is not True:
                bad = True
        if not bad:
            yield v


def solve(S, case):
    res = [closed(S, v, case.notrec) for v in worlds(S, case)]
    finals = {r["final"] for r in res}
    return {"det": len(finals) == 1, "final": next(iter(finals)) if len(finals) == 1 else CBD, "comps": res}


def answer(S, q, cases, options=None):
    """Row gold from the parsed question: Q3 -> 1/0, Q1 -> outcome or CBD, Q2 -> (outcome, basis) or (CBD, None),
    Q4 -> listed case ref or '__NONE__'."""
    qt = q["qtype"]
    if qt == "Q4":
        hits = []
        for c in cases:
            r = solve(S, c)
            if r["det"] and r["final"] == q["X"]:
                hits.append(c.ref)
        if len(hits) > 1:
            raise BError("two qualifying cases")
        return hits[0] if hits else "__NONE__"
    r = solve(S, cases[0])
    if qt == "Q3":
        fin = {c["final"] for c in r["comps"]}
        X = q["X"]
        holds = fin == {X}
        never = X not in fin
        if q["pol"] in ("aff", "dneg"):
            return 1 if holds else 0 if never else None
        return 1 if never else 0 if holds else None
    if qt == "Q1":
        return r["final"] if r["det"] else CBD
    if qt == "Q2":
        if not r["det"]:
            return (CBD, None)
        pairs = {(c["final"], c["basis"]) for c in r["comps"]}
        if len(pairs) != 1:
            return None
        return next(iter(pairs))
    raise BError(qt)


# ---------------------------------------------------------------- depth (own)

def closure_b(S, T):
    out = set(T)
    grow = True
    while grow:
        grow = False
        inserted_by_removed = {n.rule.rid for n in S.notices if n.ntype == "insert" and n.num in out}
        for n in S.notices:
            if n.num in out:
                continue
            hit = (n.ntype in ("replace", "repeal") and n.target in inserted_by_removed) or \
                  (n.pos is not None and n.pos[0] == "after" and n.pos[1] in inserted_by_removed) or \
                  (n.ntype == "insert" and n.rule.kind in ("pexc", "oexc") and n.rule.target in inserted_by_removed)
            if hit:
                out.add(n.num)
                grow = True
    return frozenset(out)


def depth_closed(S, v, notrec=frozenset()):
    base = closed(S, v, notrec)
    if base["src"] == "M":
        return 1
    g = v[S.policy.gov]
    nums = [n.num for n in S.notices]
    subsets = [frozenset(c) for k in range(1, len(nums) + 1) for c in itertools.combinations(nums, k)]
    changed = {T: closed(S, v, notrec, skip=closure_b(S, T))["final"] != base["final"] for T in subsets}
    minimal = [T for T in subsets if changed[T] and not any(changed[U] for U in subsets if U < T)]
    union = set().union(*minimal) if minimal else set()
    A = len([n for n in S.notices if n.num in union and n.edate <= g])
    return 1 + base["X"] + A + base["P"] + base["O"]


def depth(S, cases):
    best = 0
    for c in cases:
        for v in worlds(S, c):
            best = max(best, depth_closed(S, v, c.notrec))
    return best

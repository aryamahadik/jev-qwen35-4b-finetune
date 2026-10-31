"""Solver A (generator author): imperative forward chaining over the drawn structure (G0 F1 v7 section 2, gold steps 1-8),
open world by critical-point enumeration, depth (section 1), gold source, error models E1-E15 (section 4), R1-R10.

Error models are full derivations with one error (F1R2-A12):
  E1 ignore exceptions | E2 ignore amendments | E3 notice date as effective date | E4 reversed precedence |
  E5 unless read as if | E6 only-if read as sufficient | E7 boundary off by one (inclusivity flipped) |
  E8 world error (unknown read as false; CBD where determined) | E9 first-listed firing rule wins |
  E10 escalate when no rule fires | E11 exceptions to repealed / expired rules kept | E12 or read as exclusive |
  E13 unscoped exceptions | E14 only-if check skipped | E15 inert drafts / other-body notices applied
"""
from __future__ import annotations

import itertools
from decimal import Decimal

from model import Attr, Item, Lit, Notice, Rule, Struct, Case

ERRS = tuple(f"E{i}" for i in range(1, 16))
CBD = "__CBD__"


class Reject(Exception):
    pass


_OV = {}   # literal-occurrence override {id(Lit): bool} for the decisive-literal test (flip one literal alone)


def set_override(ov):
    global _OV
    _OV = ov or {}


# ---------------------------------------------------------------- literals and items

def lit_val(lit: Lit, attrs: dict, vals: dict, err=None):
    if _OV and id(lit) in _OV:
        return _OV[id(lit)]
    a = attrs[lit.attr]
    if lit.attr not in vals:
        return None
    v = vals[lit.attr]
    op, args = lit.op, lit.args
    flip = err == "E7"
    if a.type == "bool":
        return v == args[0]
    if a.type == "cat":
        return (v in args) if op == "in" else (v not in args)
    if a.type == "num":
        if op == "ge":
            return v > args[0] if flip else v >= args[0]
        if op == "gt":
            return v >= args[0] if flip else v > args[0]
        if op in ("le", "within"):
            return v < args[0] if flip else v <= args[0]
        if op == "lt":
            return v <= args[0] if flip else v < args[0]
        if op == "between":
            return (args[0] < v < args[1]) if flip else (args[0] <= v <= args[1])
    if a.type == "date":
        if op == "before":
            return v <= args[0] if flip else v < args[0]
        if op == "onbefore":
            return v < args[0] if flip else v <= args[0]
        if op == "after":
            return v >= args[0] if flip else v > args[0]
        if op == "onafter":
            return v > args[0] if flip else v >= args[0]
        if op == "fromto":
            return (args[0] < v < args[1]) if flip else (args[0] <= v <= args[1])
    raise ValueError(f"bad literal {lit}")


def item_val(it: Item, attrs, vals, err=None, e8=False):
    def lv(m):
        x = lit_val(m, attrs, vals, err)
        if x is None:
            if e8:
                return False
            raise KeyError(m.attr)
        return x
    k = it.kind
    if k == "lit":
        return lv(it.mem[0])
    if k == "not":
        return lv(it.mem[0]) if err == "E5" else (not lv(it.mem[0]))
    xs = [lv(m) for m in it.mem]
    if k == "or":
        return (sum(xs) == 1) if err == "E12" else any(xs)
    if k == "xor":
        return sum(xs) == 1
    if k == "all":
        return all(xs)
    if k == "any":
        return (sum(xs) == 1) if err == "E12" else any(xs)
    if k == "kofn":
        return sum(xs) >= it.k
    raise ValueError(k)


def cond_val(r: Rule, attrs, vals, err=None, e8=False):
    return all(item_val(it, attrs, vals, err, e8) for it in r.all_items())


# ---------------------------------------------------------------- step 2: rules in force at g

def _base_date(S: Struct, r: Rule):
    return r.date if r.date is not None else S.policy.B


def in_force(S: Struct, g: int, err=None, removed=frozenset()):
    """{rid: [rule, date, source]} after gold step 2. source = ("r", rid) base text | ("n", num) notice text."""
    rules = {r.rid: [r, _base_date(S, r), ("r", r.rid)] for r in S.rules}
    notes = [n for n in S.notices if n.num not in removed]
    if err == "E15":
        for e in S.inert:
            if e.cls in ("draft", "other_body") and e.notice is not None:
                notes.append(e.notice)
    if err == "E2":
        notes = []

    def eff(n):
        return n.ndate if err == "E3" else n.edate
    for n in sorted([n for n in notes if eff(n) <= g], key=lambda n: (eff(n), n.num if n.num is not None else 10 ** 6)):
        src = ("n", n.num)
        if n.ntype == "replace":
            if n.target in rules:
                old = rules[n.target][0]
                new = n.rule.copy(rid=old.rid, kind=old.kind, target=old.target)
                if old.kind == "onlyif":
                    new.out = old.out          # a replacement keeps the named outcome Y (section 2, A02)
                rules[n.target] = [new, eff(n), src]
        elif n.ntype == "repeal":
            rules.pop(n.target, None)
        elif n.ntype == "insert":
            rules[n.rule.rid] = [n.rule, eff(n), src]
    for rid in [rid for rid, (r, d, s) in rules.items() if r.last is not None and r.last < g]:
        rules.pop(rid)
    if err == "E1":
        for rid in [rid for rid, (r, d, s) in rules.items() if r.kind in ("pexc", "oexc")]:
            rules.pop(rid)
    if err != "E11":
        changed = True
        while changed:
            changed = False
            for rid in list(rules):
                r = rules[rid][0]
                if r.kind in ("pexc", "oexc") and r.target not in rules:
                    rules.pop(rid)
                    changed = True
    return rules


# ---------------------------------------------------------------- precedence

def item_set(S: Struct, rules: dict, rid: int, seen=None):
    seen = seen or set()
    if rid in seen or rid not in rules:
        return frozenset()
    seen.add(rid)
    r = rules[rid][0]
    s = {it.canon(S.attrs) for it in r.all_items()}
    if r.kind in ("pexc", "oexc") and r.target is not None:
        s |= item_set(S, rules, r.target, seen)
    return frozenset(s)


def beats(S: Struct, pol: str, rules: dict, rank: dict, r: int, s: int) -> bool:
    if pol == "SPEC":
        a, b = item_set(S, rules, r), item_set(S, rules, s)
        return a > b
    if pol == "LATER":
        return rules[r][1] > rules[s][1]
    if pol == "PRIORITY":
        tr, ts = rules[r][0].tier, rules[s][0].tier   # an untiered rule (only reachable in error model E6) is lowest
        return (tr if tr is not None else 99) < (ts if ts is not None else 99)
    if pol == "ORDER":
        return rank[r] < rank[s]
    raise ValueError(pol)


def display_rank(S: Struct, rules: dict, g: int, err=None, removed=frozenset()):
    """Reading-order rank of each in-force rule's text-bearing element (ORDER rank on S3; E9; decisive position)."""
    if S.s3_rows is not None:
        order = list(S.s3_rows)
        notes = [n for n in S.notices if n.num not in removed]
        if err == "E15":
            notes += [e.notice for e in S.inert if e.cls in ("draft", "other_body") and e.notice is not None]
        if err == "E2":
            notes = []

        def eff(n):
            return n.ndate if err == "E3" else n.edate
        # positions are fixed when a row is added (F1R1-A09): replay inserts in effective-date order; removed rows
        # keep the others' relative order. Inserts with effective date > g are not shown as in force.
        full = list(S.s3_rows)
        for n in sorted(notes, key=lambda n: (eff(n), n.num or 0)):
            if n.ntype != "insert" or eff(n) > g:
                continue
            p = n.pos or ("bottom",)
            if p[0] == "top":
                full.insert(0, n.rule.rid)
            elif p[0] == "bottom":
                full.append(n.rule.rid)
            else:
                k = p[1]
                idx = full.index(k) if k in full else len(full) - 1
                full.insert(idx + 1, n.rule.rid)
        return {rid: i for i, rid in enumerate([x for x in full if x in rules])}
    pos = {}
    for i, (t, x) in enumerate(S.order):
        pos[(t, x)] = i
    out = {}
    for rid, (r, d, src) in rules.items():
        out[rid] = pos.get(src, pos.get(("r", rid), 10 ** 6))
    return out


# ---------------------------------------------------------------- closed case

def solve_closed(S: Struct, vals: dict, notrec=frozenset(), err=None, removed=frozenset(), e8=False):
    """Gold steps 1-7 on one closed case. Returns a dict with the final outcome and the trace."""
    P = S.policy
    if P.world == "missing" and (set(notrec) & set(P.listed)):
        return {"o": P.M, "src": "M", "final": P.M, "X": 0, "P": 0, "O": 0, "cands": [], "winner": None,
                "fired_exc": [], "rules": {}, "basis": "M"}
    g = vals[P.gov]
    rules = in_force(S, g, err, removed)
    A = S.attrs
    fire_memo = {}

    def fires(rid, stack=()):
        if rid in fire_memo:
            return fire_memo[rid]
        if rid in stack:
            raise Reject("exception cycle")
        r = rules[rid][0]
        if r.kind == "onlyif":
            fire_memo[rid] = False
            return False
        c = cond_val(r, A, vals, err, e8)
        if c and r.kind in ("pexc", "oexc"):
            if err == "E13":
                pass
            elif r.target in rules:
                c = fires(r.target, stack + (rid,))
            elif err == "E11":
                pass
            else:
                c = False
        fire_memo[rid] = c
        return c
    exc_by_target = {}
    for rid, (r, d, s) in rules.items():
        if r.kind in ("pexc", "oexc"):
            exc_by_target.setdefault(r.target, []).append(rid)
    eff_memo = {}

    def effective(rid, stack=()):
        if rid in eff_memo:
            return eff_memo[rid]
        if rid in stack:
            raise Reject("exception cycle")
        v = fires(rid) and not any(effective(e, stack + (rid,)) for e in exc_by_target.get(rid, []))
        eff_memo[rid] = v
        return v

    def off(rid):
        return any(effective(e) for e in exc_by_target.get(rid, []))
    # nesting level of each exception
    def level(rid, d=0):
        r = rules[rid][0]
        if r.kind not in ("pexc", "oexc"):
            return 0
        if r.target not in rules:
            return 1
        return 1 + level(r.target, d + 1)
    fired_exc = [rid for rid, (r, d, s) in rules.items() if r.kind in ("pexc", "oexc") and fires(rid)]
    X = max([level(r) for r in fired_exc], default=0)
    cands = []
    for rid, (r, d, s) in rules.items():
        kind_ok = r.kind in ("gen", "oexc") or (err == "E6" and r.kind == "onlyif")
        if not kind_ok:
            continue
        if err == "E6" and r.kind == "onlyif":
            if cond_val(r, A, vals, err, e8):
                cands.append(rid)
            continue
        if fires(rid) and not off(rid):
            cands.append(rid)
    rank = display_rank(S, rules, g, err, removed)
    outs = {rules[c][0].out for c in cands}
    src = None
    winner = None
    remaining = cands
    Pf = 1 if len(outs) >= 2 else 0
    if not cands:
        o = P.escalate if err == "E10" else P.default
        src = "D"
    elif len(outs) == 1:
        o = next(iter(outs))
        src = "RULE"
    elif err == "E9":
        first = min(cands, key=lambda c: (rank.get(c, 10 ** 6), c))
        o = rules[first][0].out
        src = "RULE"
    else:
        prim, sec = P.prim, P.sec

        def bt(pol, a, b):
            return beats(S, pol, rules, rank, b, a) if err == "E4" else beats(S, pol, rules, rank, a, b)
        W1 = [c for c in cands if not any(rules[d][0].out != rules[c][0].out and bt(prim, d, c) for d in cands)]
        if not W1:
            raise Reject("empty W1")
        remaining = W1
        if len({rules[c][0].out for c in W1}) == 1:
            o = rules[W1[0]][0].out
            src = "RULE"
        else:
            if sec:
                W2 = [c for c in W1 if not any(rules[d][0].out != rules[c][0].out and bt(sec, d, c) for d in W1)]
                if not W2:
                    raise Reject("empty W2")
                remaining = W2
            if len({rules[c][0].out for c in remaining}) == 1:
                o = rules[remaining[0]][0].out
                src = "RULE"
            else:
                if P.tie == "none":
                    raise Reject("tie on a card without a tie rule")
                if P.tie == "esc":
                    o = P.escalate
                else:
                    ro = {rules[c][0].out for c in remaining}
                    o = next(x for x in P.strict if x in ro)
                src = "T"
    O = 0
    final = o
    if err not in ("E14", "E6"):
        named = [rid for rid, (r, d, s) in rules.items() if r.kind == "onlyif" and r.out == o]
        if named and not all(cond_val(rules[rid][0], A, vals, err, e8) for rid in named):
            final = P.fallback
            src = "F"
            O = 1
    if src == "RULE":
        holders = [c for c in cands if rules[c][0].out == final]
        if len(holders) == 1:
            src, winner = "ONE", holders[0]
        else:
            src = "MANY"
    basis = {"D": "D", "T": "T", "F": "F", "M": "M", "ONE": winner, "MANY": None}[src]
    return {"o": o, "final": final, "src": src, "winner": winner, "X": X, "P": Pf if src != "D" else 0, "O": O,
            "cands": cands, "fired_exc": fired_exc, "rules": rules, "basis": basis, "rank": rank,
            "remaining": remaining}


# ---------------------------------------------------------------- R1 (semantic entailment without superset)

def _regions(S: Struct, attr_keys):
    """Representative values per attribute: one per region cut by every canonical threshold in the structure."""
    reps = {}
    for k in attr_keys:
        a = S.attrs[k]
        if a.type == "bool":
            reps[k] = [True, False]
        elif a.type == "cat":
            reps[k] = list(a.values)
        else:
            pts = set()
            for lit in all_lits(S):
                if lit.attr != k:
                    continue
                c = lit.canon(S.attrs)
                for t in c[2]:
                    pts.add(t)
            step = a.step if a.type == "num" else 1
            cand = set()
            for t in pts:
                for d in (-step, 0, step):
                    cand.add(t + d)
            lo, hi = domain(S, k)
            cand |= {lo, hi}
            reps[k] = sorted(x for x in cand if lo <= x <= hi)
    return reps


def domain(S: Struct, k: str):
    a = S.attrs[k]
    if a.type == "date":
        return a.lo, a.hi
    return a.lo, a.hi


def all_lits(S: Struct):
    out = []

    def add_rule(r):
        if r is None:
            return
        for it in r.all_items():
            out.extend(it.mem)
    for r in S.rules:
        add_rule(r)
    for n in S.notices:
        add_rule(n.rule)
    for e in S.inert:
        if e.notice is not None:
            add_rule(e.notice.rule)
        add_rule(e.rule)
    return out


def entails(S: Struct, ra: Rule, rb: Rule, rules: dict) -> bool:
    """cond(ra) (with inherited target items) entails cond(rb) (same), checked over all regions of the fields."""
    ia = item_set_items(S, rules, ra.rid)
    ib = item_set_items(S, rules, rb.rid)
    keys = sorted({m.attr for it in ia + ib for m in it.mem})
    reps = _regions(S, keys)
    total = 1
    for k in keys:
        total *= len(reps[k])
        if total > 40000:
            raise Reject("R1 region space too large")
    for combo in itertools.product(*[reps[k] for k in keys]):
        vals = dict(zip(keys, combo))
        if all(item_val(it, S.attrs, vals) for it in ia) and not all(item_val(it, S.attrs, vals) for it in ib):
            return False
    return True


def item_set_items(S, rules, rid, seen=None):
    seen = seen or set()
    if rid in seen or rid not in rules:
        return []
    seen.add(rid)
    r = rules[rid][0]
    out = list(r.all_items())
    if r.kind in ("pexc", "oexc") and r.target is not None:
        out += item_set_items(S, rules, r.target, seen)
    return out


def check_R1(S: Struct, res: dict):
    P = S.policy
    if "SPEC" not in (P.prim, P.sec):
        return
    rules = res["rules"]
    c = res["cands"]
    for i in range(len(c)):
        for j in range(i + 1, len(c)):
            a, b = rules[c[i]][0], rules[c[j]][0]
            if a.out == b.out:
                continue
            sa, sb = item_set(S, rules, a.rid), item_set(S, rules, b.rid)
            if sa > sb or sb > sa:
                continue
            if entails(S, a, b, rules) or entails(S, b, a, rules):
                raise Reject("R1")


# ---------------------------------------------------------------- open world

def completion_points(S: Struct, k: str):
    a = S.attrs[k]
    if a.type == "bool":
        return [True, False]
    if a.type == "cat":
        return list(a.values)
    pts = set()
    step = a.step if a.type == "num" else 1
    for lit in all_lits(S):
        if lit.attr != k:
            continue
        for t in lit.args:
            for d in (-step, 0, step):
                pts.add(t + d)
    lo, hi = domain(S, k)
    pts |= {lo, hi}
    return sorted(x for x in pts if lo <= x <= hi)


def completions(S: Struct, case: Case):
    keys = sorted(case.unknown)
    if not keys:
        yield dict(case.vals)
        return
    lists = [completion_points(S, k) for k in keys]
    for combo in itertools.product(*lists):
        v = dict(case.vals)
        v.update(zip(keys, combo))
        # R8 case constraint holds in every completion: a presupposing fact true only when its field is true
        ok = True
        for kk, a in S.attrs.items():
            if a.type == "bool" and a.presup and v.get(kk) is True and v.get(a.presup) is not True:
                ok = False
                break
        if ok:
            yield v


def solve(S: Struct, case: Case, err=None, check=True):
    """Final outcome (or CBD) of the row's case, with the per-completion results."""
    if S.policy.world == "open" and case.unknown and err != "E8":
        res = []
        for v in completions(S, case):
            r = solve_closed(S, v, case.notrec, err)
            if check and err is None:
                check_R1(S, r)
            res.append(r)
        finals = {r["final"] for r in res}
        return {"det": len(finals) == 1, "final": next(iter(finals)) if len(finals) == 1 else CBD, "comps": res}
    if err == "E8":
        if S.policy.world != "open":
            return None
        r = solve_closed(S, case.vals, case.notrec, err=None, e8=True)
        return {"det": True, "final": r["final"], "comps": [r]}
    r = solve_closed(S, case.vals, case.notrec, err)
    if check and err is None:
        check_R1(S, r)
    return {"det": True, "final": r["final"], "comps": [r]}


def gold_source(res: dict):
    comps = res["comps"]
    if not res["det"]:
        return "CBD", None
    srcs = {(c["src"], c["winner"]) for c in comps}
    if len(srcs) == 1:
        s, w = next(iter(srcs))
        return s, w
    if all(c["src"] == "ONE" for c in comps):
        return "mixed", None
    if len({c["src"] for c in comps}) == 1:
        return comps[0]["src"], None
    return "mixed", None


def q2_pair(res: dict):
    """(outcome, basis) or ('CBD', None) or None when no Q2 pair exists (MANY, mixed, basis varies)."""
    if not res["det"]:
        return (CBD, None)
    pairs = {(c["final"], c["basis"]) for c in res["comps"]}
    if len(pairs) != 1:
        return None
    o, b = next(iter(pairs))
    if b is None:
        return None
    return (o, b)


# ---------------------------------------------------------------- depth (section 1)

def removal_closure(S: Struct, T: frozenset) -> frozenset:
    removed = set(T)
    changed = True
    while changed:
        changed = False
        ins_by = {n.rule.rid: n.num for n in S.notices if n.ntype == "insert" and n.num in removed}
        for n in S.notices:
            if n.num in removed:
                continue
            dep = False
            if n.ntype in ("replace", "repeal") and n.target in ins_by:
                dep = True
            if n.pos and n.pos[0] == "after" and n.pos[1] in ins_by:
                dep = True
            if n.ntype == "insert" and n.rule.kind in ("pexc", "oexc") and n.rule.target in ins_by:
                dep = True
            if dep:
                removed.add(n.num)
                changed = True
    return frozenset(removed)


def closed_depth(S: Struct, vals: dict, notrec=frozenset()):
    P = S.policy
    base = solve_closed(S, vals, notrec)
    if base["src"] == "M":
        return 1, 0, base
    g = vals[P.gov]
    nums = [n.num for n in S.notices]
    changes = {}
    for r in range(1, len(nums) + 1):
        for T in itertools.combinations(nums, r):
            T = frozenset(T)
            rem = removal_closure(S, T)
            alt = solve_closed(S, vals, notrec, removed=rem)
            changes[T] = alt["final"] != base["final"]
    minimal = [T for T, ch in changes.items() if ch and not any(changes.get(U) for U in changes if U < T)]
    inset = set()
    for T in minimal:
        inset |= T
    A = sum(1 for n in S.notices if n.num in inset and n.edate <= g)
    d = 1 + base["X"] + A + base["P"] + base["O"]
    return d, A, base


def depth(S: Struct, case: Case):
    """(depth, A) of the row's case: max over completions on open-world rows."""
    if S.policy.world == "open" and case.unknown:
        best = (0, 0)
        for v in completions(S, case):
            d, A, _ = closed_depth(S, v, case.notrec)
            best = max(best, (d, A))
        return best
    d, A, _ = closed_depth(S, case.vals, case.notrec)
    return d, A


# ---------------------------------------------------------------- error models

def error_outputs(S: Struct, case: Case, gold_res: dict):
    """{E: {'q1': outcome|CBD|None, 'q2': pair|None, 'q3_final_set': set|None}} for every error model."""
    out = {}
    has_inert_notice = any(e.cls in ("draft", "other_body") and e.notice is not None for e in S.inert)
    for E in ERRS:
        if E == "E15" and not has_inert_notice:
            continue
        if E == "E8" and S.policy.world != "open":
            continue
        try:
            r = solve(S, case, err=E, check=False)
        except (Reject, KeyError):
            r = None
        if r is None:
            continue
        if E == "E8" and gold_res["det"] and r["final"] == gold_res["final"]:
            r = {"det": True, "final": CBD, "comps": []}
            out[E] = {"q1": CBD, "q2": (CBD, None), "finals": None}
            continue
        if r["det"]:
            q2 = q2_pair(r)
        else:
            q2 = None
        finals = {c["final"] for c in r["comps"]} if r["comps"] else None
        out[E] = {"q1": r["final"] if r["det"] else CBD, "q2": q2, "finals": finals}
    return out


# ---------------------------------------------------------------- yes / no

def q3_answer(res: dict, X: str, pol: str):
    """Yes/no answer of a Q3 question: 1 yes, 0 no, None undetermined. pol: aff | neg | dneg."""
    finals = {c["final"] for c in res["comps"]}
    allX = finals == {X}
    noneX = X not in finals
    if pol in ("aff", "dneg"):
        if allX:
            return 1
        if noneX:
            return 0
        return None
    if noneX:
        return 1
    if allX:
        return 0
    return None


def q3_from_finals(finals, X, pol):
    if finals is None:
        return None
    allX = finals == {X}
    noneX = X not in finals
    if pol in ("aff", "dneg"):
        return 1 if allX else (0 if noneX else None)
    return 1 if noneX else (0 if allX else None)

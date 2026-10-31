"""Solver A (G0 section 4): proof-style, on the generator's own structure. Kleene three-valued forward chaining over
Out(c) (fire, block, precedence, default) with lazy case splits: a variable is split into its regions (whole numbers
cut at every threshold, day numbers cut at the other notices' days, category values, yes/no) only when an
undetermined status needs it. It returns P (possible outcomes over the full catalog) or T (claim values), the
drop flags of the formal core, the C-GAP settling set and the C-CASE decidable set.

Shares no code with solver_b.py (G2: a different paradigm, written separately).
"""
from __future__ import annotations

U = None  # Kleene unknown


class Drop(Exception):
    """A formal-core drop condition: (i) empty or two-outcome winner set; (ii) same-notice clash; or R inconsistent."""


def _and(vals):
    out = True
    for v in vals:
        if v is False:
            return False
        if v is U:
            out = U
    return out


def _not(v):
    return U if v is U else (not v)


# ---------------------------------------------------------------- variables of a rules-kind structure

def variables(R: dict, case: str) -> dict:
    """Var for one case: {var: {"kind", "regions": [(lo, hi), ...] or values}} for every unknown, plus fixed
    values {var: value} under key "_fixed". Var names: ("num", aid), ("cat", aid), ("ev", eid), ("cls", cid),
    ("nd", nid)."""
    F = R["facts"][case]
    world, loc = R["world"], R.get("local")
    tag = R.get("ev_tag")
    counts = bool(tag and tag.get("counts"))
    fixed, var = {}, {}

    def known(f):
        return f is not None and "v" in f and not f.get("m") and (not f.get("tag") or counts)

    for aid, a in R["attrs"].items():
        f = F["num" if a["kind"] == "num" else "cat"].get(aid)
        key = (a["kind"], aid)
        if known(f):
            fixed[key] = f["v"]
        else:
            var[key] = a
    for eid in R["events"]:
        f = F["ev"].get(eid)
        key = ("ev", eid)
        if known(f):
            fixed[key] = bool(f.get("v", True))
        elif (f is None or "plan" in f) and world == "closed":
            fixed[key] = False      # not listed (or only a plan) on a closed card: it did not happen (rows 2, 27)
        else:
            var[key] = {"kind": "bool"}
    for cid in R["classes"]:
        f = F["cls"].get(cid)
        key = ("cls", cid)
        if known(f):
            fixed[key] = bool(f.get("v", True))
        elif f is None and (world == "closed" or (world == "local" and loc == cid)):
            fixed[key] = False
        else:
            var[key] = {"kind": "bool"}
    for nid, n in R["notices"].items():
        d = n["date"]
        key = ("nd", nid)
        if d["k"] == "exact":
            fixed[key] = d["d"]
        else:
            var[key] = {"kind": "day", "a": d["a"], "b": d["b"]}
    # subclass: a known B fixes A (row 44; fixed, so not an absence)
    for b, a in R.get("subclass", []):
        if fixed.get(("cls", b)) is True and ("cls", a) in var:
            fixed[("cls", a)] = True
            del var[("cls", a)]
    return {"fixed": fixed, "var": var}


def _cuts_num(R: dict, aid: str, extra_atoms=()) -> list[int]:
    cuts = set()

    def visit(at):
        if at and at["t"] == "num" and at["a"] == aid:
            n, op = at["n"], at["op"]
            cuts.add(n if op in (">=", "<") else n + 1)
    for r in R["rules"]:
        for at in r["conds"]:
            visit(at)
        visit(r.get("unless"))
    for o in R.get("onlyif", []):
        visit(o["cond"])
    for at in extra_atoms:
        visit(at)
    return sorted(cuts)


def regions(R: dict, key, spec, fixed: dict) -> list:
    """Representative values, one per region of the variable's domain."""
    kind = key[0]
    if kind == "num":
        lo, hi = spec["lo"], spec["hi"]
        pts = [c for c in _cuts_num(R, key[1]) if lo < c <= hi]
        starts = [lo] + pts
        return starts
    if kind == "cat":
        return list(spec["vals"])
    if kind in ("ev", "cls"):
        return [True, False]
    if kind == "nd":
        others = sorted(v for k, v in fixed.items() if k[0] == "nd")
        a, b = spec["a"], spec["b"]
        reps, cur = [], a
        for o in others + [b + 1]:
            if o < a:
                continue
            if cur <= min(o - 1, b):
                reps.append(cur)
            cur = max(cur, o + 1)
            if cur > b:
                break
        return reps
    raise ValueError(key)


# ---------------------------------------------------------------- three-valued statuses

def _atom(at, asg):
    t = at["t"]
    if t == "num":
        x = asg.get(("num", at["a"]), U)
        if x is U:
            return U
        n, op = at["n"], at["op"]
        return {">=": x >= n, ">": x > n, "<=": x <= n, "<": x < n}[op]
    if t == "cat":
        x = asg.get(("cat", at["a"]), U)
        return U if x is U else (x == at["v"])
    if t == "ev":
        x = asg.get(("ev", at["e"]), U)
        if x is U:
            return U
        return (not x) if at.get("neg") else x
    if t == "cls":
        return asg.get(("cls", at["c"]), U)
    raise ValueError(t)


def all_rules(R: dict) -> list[dict]:
    """Rules with each outcome-table cell as a rule of its own (row 53)."""
    out = list(R["rules"])
    T = R.get("table")
    if T:
        for a in T["rows"]:
            for b in T["cols"]:
                o = T["cells"].get(f"{a}|{b}")
                if o is not None:
                    out.append({"rid": f"{T['rid']}:{a}|{b}", "notice": T["notice"], "out": o, "unless": None,
                                "conds": [{"t": "cat", "a": T["A"], "v": a}, {"t": "cat", "a": T["B"], "v": b}],
                                "exc": None})
    return out


def _class_of(r):
    for at in r["conds"]:
        if at["t"] == "cls":
            return at["c"]
    return None


def _beats(R, r1, r2, asg):
    """True / False (r1 beats r2 or not, first separating test), U (needs an unknown date) or 'tie' (same notice,
    tests 1-2 do not separate)."""
    if r1.get("exc") == r2["rid"]:
        return True
    if r2.get("exc") == r1["rid"]:
        return False
    c1, c2 = _class_of(r1), _class_of(r2)
    if c1 and c2 and c1 != c2:
        sub = R.get("subclass", [])
        if (c1, c2) in sub or [c1, c2] in sub:
            return True
        if (c2, c1) in sub or [c2, c1] in sub:
            return False
    if r1["notice"] == r2["notice"]:
        return "tie"
    d1, d2 = asg.get(("nd", r1["notice"]), U), asg.get(("nd", r2["notice"]), U)
    if d1 is U or d2 is U:
        return U
    return d1 > d2


def _statuses(R, rules, asg):
    blk = {}
    for o in R.get("onlyif", []):
        v = _atom(o["cond"], asg)
        prev = blk.get(o["out"], False)
        b = _not(v)  # blocked when C is false
        blk[o["out"]] = True if (prev is True or b is True) else (U if (prev is U or b is U) else False)
    st = []
    for r in rules:
        f = _and([_atom(a, asg) for a in r["conds"]] + ([_not(_atom(r["unless"], asg))] if r.get("unless") else []))
        b = blk.get(r["out"], False)
        rem = _and([f, _not(b)])
        st.append(rem)
    return st


def _first_unknown(R, rules, asg, var):
    """The variable to split on: the first unknown that an undetermined status or precedence test needs."""
    for r in rules:
        for at in r["conds"] + ([r["unless"]] if r.get("unless") else []):
            if _atom(at, asg) is U:
                return _atom_var(at)
    for o in R.get("onlyif", []):
        if _atom(o["cond"], asg) is U:
            return _atom_var(o["cond"])
    for k in var:
        if k[0] == "nd" and k not in asg:
            return k
    return None


def _atom_var(at):
    return {"num": ("num", at.get("a")), "cat": ("cat", at.get("a")), "ev": ("ev", at.get("e")),
            "cls": ("cls", at.get("c"))}[at["t"]]


def _consistent(R, asg):
    for b, a in R.get("subclass", []):
        if asg.get(("cls", b)) is True and asg.get(("cls", a)) is False:
            return False
    days = [v for k, v in asg.items() if k[0] == "nd" and v is not U]
    return len(days) == len(set(days))


def _decide(R, rules, st, asg):
    """Out when every remaining-fired status is known; None when a precedence test needs an unknown date."""
    rem = [r for r, s in zip(rules, st) if s is True]
    if not rem:
        return R["default"]
    outs = {r["out"] for r in rem}
    if len(outs) == 1:
        return next(iter(outs))
    W = []
    for r in rem:
        wins = True
        for q in rem:
            if q["out"] == r["out"]:
                continue
            b = _beats(R, r, q, asg)
            if b == "tie":
                raise Drop("same-notice clash (ii)")
            if b is U:
                return None
            if not b:
                wins = False
        if wins:
            W.append(r)
    # same-notice clash also when the winner set is fine (condition ii)
    for i, r in enumerate(rem):
        for q in rem[i + 1:]:
            if q["out"] != r["out"] and _beats(R, r, q, asg) == "tie":
                raise Drop("same-notice clash (ii)")
    wo = {r["out"] for r in W}
    if len(wo) != 1:
        raise Drop("winner set empty or split (i)")
    return next(iter(wo))


def _search(R, rules, asg, var, claim, acc):
    if not _consistent(R, asg):
        return
    st = _statuses(R, rules, asg)
    if all(s is not U for s in st):
        out = _decide(R, rules, st, asg)
        if out is not None:
            if claim is None:
                acc.add(out)
                return
            cv = _claim_val(claim, out, asg)
            if cv is not U:
                acc.add(cv)
                return
    k = _first_unknown(R, rules, asg, var)
    if k is None:
        # unknown only through a claim on facts: split remaining claim variables
        k = next((x for x in _claim_vars(claim) if x in var and x not in asg), None)
        if k is None:
            raise Drop("undecidable leaf")
    if k not in var:
        raise Drop(f"unknown {k} is not a variable")
    for v in regions(R, k, var[k], {**R["_fixed"]}):
        _search(R, rules, {**asg, k: v}, var, claim, acc)


def _claim_vars(claim):
    return []


def _claim_val(claim, out, asg):
    if claim["t"] == "out_is":
        v = out == claim["o"]
        return (not v) if claim.get("neg") else v
    raise ValueError(claim)


def solve_rules(R: dict, case: str, claim: dict | None = None, extra: dict | None = None) -> set:
    """P (claim None) or T for one case. extra: {var: value} fills (M5/M6/C-GAP tests)."""
    V = variables(R, case)
    fixed = dict(V["fixed"])
    var = dict(V["var"])
    for k, v in (extra or {}).items():
        fixed[k] = v
        var.pop(k, None)
    R2 = {**R, "_fixed": fixed}
    rules = all_rules(R)
    acc: set = set()
    _search(R2, rules, dict(fixed), var, claim, acc)
    if not acc:
        raise Drop("inconsistent record")
    return acc


def var_regions(R: dict, case: str) -> dict:
    V = variables(R, case)
    return {k: regions(R, k, s, V["fixed"]) for k, s in V["var"].items()}


def settling_set(R: dict, case: str, gaps: list, claim: dict | None = None) -> list:
    """C-GAP (row 51): empty when already settled; else the listed gaps g whose every region value settles it."""
    base = solve_rules(R, case, claim)
    if len(base) == 1:
        return []
    regs = var_regions(R, case)
    out = []
    for g in gaps:
        g = tuple(g)
        ok = True
        for v in regs.get(g, []):
            try:
                if len(solve_rules(R, case, claim, extra={g: v})) != 1:
                    ok = False
                    break
            except Drop:
                ok = False
                break
        if ok and g in regs:
            out.append(list(g))
    return out


def decidable_cases(R: dict, cases: list, claim_of=None) -> list:
    """C-CASE (row 52): cases whose record allows exactly one outcome (or fixes the claim)."""
    out = []
    for c in cases:
        cl = claim_of(c) if claim_of else None
        if len(solve_rules(R, c, cl)) == 1:
            out.append(c)
    return out


def decisive_gaps(R: dict, case: str, claim: dict | None = None) -> list:
    """On an open question: the visible gaps whose every value settles it (section 2: exactly one on an open row)."""
    regs = var_regions(R, case)
    out = []
    for g, vals in regs.items():
        ok = True
        for v in vals:
            try:
                if len(solve_rules(R, case, claim, extra={g: v})) != 1:
                    ok = False
                    break
            except Drop:
                ok = False
                break
        if ok:
            out.append(g)
    return out


# ================================================================ S3 tables (Kleene three-valued filters, count bounds)

def _cell_cond(T: dict, rec: dict, cond: dict):
    """T / F / U for one record's cell against a condition {col, op, n} or {col, v}."""
    col = next(c for c in T["cols"] if c["id"] == cond["col"])
    x = rec["cells"][cond["col"]]
    if x is not None:
        if col["kind"] == "num":
            return {">=": x >= cond["n"], ">": x > cond["n"], "<=": x <= cond["n"], "<": x < cond["n"]}[cond["op"]]
        return x == cond["v"]
    if col["kind"] == "num":
        vals = [col["lo"], col["hi"]]
        lo_ok = {">=": col["hi"] >= cond["n"], ">": col["hi"] > cond["n"], "<=": col["lo"] <= cond["n"],
                 "<": col["lo"] < cond["n"]}[cond["op"]]
        all_ok = {">=": col["lo"] >= cond["n"], ">": col["lo"] > cond["n"], "<=": col["hi"] <= cond["n"],
                  "<": col["hi"] < cond["n"]}[cond["op"]]
        return True if all_ok else (U if lo_ok else False)
    if cond["v"] not in col["vals"]:
        return False
    return True if col["vals"] == [cond["v"]] else U


def _and3(a, b):
    if a is False or b is False:
        return False
    if a is True and b is True:
        return True
    return U


def _or3(a, b):
    if a is True or b is True:
        return True
    if a is False and b is False:
        return False
    return U


def table_claim(T: dict, Q: dict):
    """Three-valued value of a yes/no table query: True / False / U."""
    t = Q["t"]
    if t == "member":
        L = T["list"]
        if Q["who"] in L["members"]:
            v = True
        elif L["closed"]:
            v = False
        else:
            v = U
        return _not(v) if Q.get("neg") else v
    recs = T["records"]
    vals = []
    for r in recs:
        f = _cell_cond(T, r, Q["filter"]) if Q.get("filter") else True
        c = _cell_cond(T, r, Q["cond"])
        vals.append((f, c))
    if t == "exists":
        out = False
        for f, c in vals:
            out = _or3(out, _and3(f, c))
        return out
    if t == "forall":
        out = True
        for f, c in vals:
            out = _and3(out, _or3(_not(f), c))
        return out
    if t == "none":
        out = True
        for f, c in vals:
            out = _and3(out, _not(_and3(f, c)))
        return out
    if t == "count":
        lo = sum(1 for f, c in vals if _and3(f, c) is True)
        hi = sum(1 for f, c in vals if _and3(f, c) is not False)
        N, op = Q["N"], Q["cmp"]
        def test(x):
            return {">=": x >= N, ">": x > N, "<=": x <= N, "<": x < N}[op]
        a, b = test(lo), test(hi)
        if a and b:
            return True
        if not a and not b:
            # monotone in the count: check every value between lo and hi
            return U if any(test(x) for x in range(lo, hi + 1)) else False
        return U
    raise ValueError(t)


def _idnum(rid: str) -> int:
    return int(rid.split("-")[-1])


def table_argset(T: dict, Q: dict) -> set:
    """Records that are the argmax (argmin) in some completion, with the tie rule 'lower ID number wins'."""
    key = Q["key"]
    col = next(c for c in T["cols"] if c["id"] == key)
    hi_mode = Q["t"] == "argmax"
    out = set()
    rows = []
    for r in T["records"]:
        f = _cell_cond(T, r, Q["filter"]) if Q.get("filter") else True
        x = r["cells"][key]
        lo, hi = (x, x) if x is not None else (col["lo"], col["hi"])
        rows.append((r["id"], f, lo, hi))
    for rid, f, lo, hi in rows:
        if f is False:
            continue
        best = hi if hi_mode else lo
        ok = True
        for sid, g, slo, shi in rows:
            if sid == rid or g is False:
                continue
            if g is U:
                continue            # s can fail its filter
            other = slo if hi_mode else shi
            if hi_mode:
                beats = other < best or (other == best and _idnum(rid) < _idnum(sid))
            else:
                beats = other > best or (other == best and _idnum(rid) < _idnum(sid))
            if not beats:
                ok = False
                break
        if ok:
            out.add(rid)
    return out


def table_marked(T: dict) -> list:
    return [(r["id"], c) for r in T["records"] for c, v in r["cells"].items() if v is None]


def _fill_table(T: dict, rid: str, col: str, v):
    import copy
    T2 = copy.deepcopy(T)
    for r in T2["records"]:
        if r["id"] == rid:
            r["cells"][col] = v
    return T2


def table_regions(T: dict, col: str, Q: dict) -> list:
    c = next(x for x in T["cols"] if x["id"] == col)
    if c["kind"] == "cat":
        return list(c["vals"])
    cuts = set()
    for cond in [Q.get("cond"), Q.get("filter")]:
        if cond and cond.get("col") == col and "n" in cond:
            cuts.add(cond["n"] if cond["op"] in (">=", "<") else cond["n"] + 1)
    if Q["t"] in ("argmax", "argmin") and Q["key"] == col:
        for r in T["records"]:
            x = r["cells"][col]
            if x is not None:
                cuts |= {x, x + 1}
    pts = [c["lo"]] + sorted(p for p in cuts if c["lo"] < p <= c["hi"])
    return pts


def table_decisive(T: dict, Q: dict) -> list:
    """Marked cells (and the open membership) whose every value settles the query."""
    out = []
    for rid, col in table_marked(T):
        ok = True
        for v in table_regions(T, col, Q):
            T2 = _fill_table(T, rid, col, v)
            if Q["t"] in ("argmax", "argmin"):
                if len(table_argset(T2, Q)) != 1:
                    ok = False
                    break
            elif table_claim(T2, Q) is U:
                ok = False
                break
        if ok:
            out.append((rid, col))
    if Q["t"] == "member" and table_claim(T, Q) is U:
        out.append(("list", Q["who"]))
    return out


# ================================================================ S4 timelines (interval arithmetic on day numbers / units)

def ev_state(S: dict, key: str):
    """(happened: True / False / U, day interval (a, b)) of one event line key 'event|entity' (row 54: one occurrence)."""
    e = S["events"].get(key)
    typ = key.split("|")[0]
    closed = S["world"] == "closed" or (S["world"] == "local" and S.get("local") == typ)
    if e is None:
        dom = S["day_dom"].get(key)
        if closed:
            return False, None
        return U, dom
    k = e["k"]
    if k in ("exact", "range", "month"):
        a, b = (e["d"], e["d"]) if k == "exact" else (e["a"], e["b"])
        return True, (a, b)
    if k == "marker":
        return U, S["day_dom"].get(key)
    if k == "plan":
        if closed:
            return False, None
        return U, S["day_dom"].get(key)
    raise ValueError(k)


def _excl_days(S: dict, keys: list) -> set:
    """Days fixed for the other events of the no-shared-day types (row 46)."""
    types = set(S.get("noshare_types") or [])
    out = set()
    for k, e in S["events"].items():
        if k in keys or k.split("|")[0] not in types:
            continue
        if e["k"] == "exact":
            out.add(e["d"])
    return out


def _span(a, b, excl):
    days = [d for d in (a, b) if d not in excl]
    lo = a
    while lo in excl and lo <= b:
        lo += 1
    hi = b
    while hi in excl and hi >= a:
        hi -= 1
    return (lo, hi) if lo <= hi else None


def figure_set(S: dict, key: str) -> list:
    """Intervals (in the smallest unit) of one figure: exact, ranged, rounded, unitless (two readings) or marked."""
    f = S["figures"][key]
    q = S["quantities"][f["q"]]
    k = f["k"]
    if k == "exact":
        x = f["x"] * (q["conv"] if f.get("unit") == "V" else 1)
        return [(x, x)]
    if k == "range":
        m = q["conv"] if f.get("unit") == "V" else 1
        return [(f["a"] * m, f["b"] * m)]
    if k == "round":
        m = q["conv"] if f.get("unit") == "V" else 1
        h = q["R"] * m // 2
        x = f["x"] * m
        return [(x - h, x + h - 1)]
    if k == "unitless":
        return [(f["x"], f["x"]), (f["x"] * q["conv"], f["x"] * q["conv"])]
    if k == "marker":
        return [(q["lo"], q["hi"])]
    raise ValueError(k)


def _sum_sets(sets):
    acc = [(0, 0)]
    for s in sets:
        acc = [(a + c, b + d) for a, b in acc for c, d in s]
    return acc


def _cmp(x, op, n):
    return {">=": x >= n, ">": x > n, "<=": x <= n, "<": x < n}[op]


def timeline_claim(S: dict, Q: dict):
    """True / False / U for an S4 claim (deadline, before, daycount, total)."""
    t = Q["t"]
    if t == "deadline":
        occ, dom = ev_state(S, Q["ev"])
        X = Q["by"]
        if dom is not None and Q["ev"].split("|")[0] in set(S.get("noshare_types") or []):
            sp = _span(dom[0], dom[1], _excl_days(S, [Q["ev"]]))
            if sp is None:
                if occ is True:
                    raise Drop("empty day domain")
                occ, dom = False, None
            else:
                dom = sp
        if occ is False:
            v = (False if X <= S["D"] else U)
        elif occ is True:
            a, b = dom
            v = True if b <= X else (False if a > X else U)
        else:
            if dom is None:
                v = U
            else:
                a, b = dom
                v = False if a > X and X <= S["D"] else U
        return _not(v) if Q.get("neg") else v
    if t in ("before", "daycount"):
        o1, d1 = ev_state(S, Q["e1"])
        o2, d2 = ev_state(S, Q["e2"])
        if o1 is not True or o2 is not True:
            raise Drop("compared events must be recorded as having happened")
        if t == "before":
            ex = _excl_days(S, [Q["e1"], Q["e2"]])
            s1, s2 = _span(*d1, ex), _span(*d2, ex)
            if s1 is None or s2 is None:
                raise Drop("empty day domain")
            # the two compared events never share a day (row 46): a pair with d1 > d2 exists iff b1 > a2, and one
            # with d1 < d2 iff a1 < b2 (the extreme pair is never a shared day)
            if s1 == s2 and s1[0] == s1[1]:
                raise Drop("forced shared day")
            if s1[1] <= s2[0]:
                v = True
            elif s1[0] >= s2[1]:
                v = False
            else:
                v = U
            return _not(v) if Q.get("neg") else v
        N = Q["N"]
        types = set(S.get("noshare_types") or [])
        if Q["e1"].split("|")[0] in types and Q["e2"].split("|")[0] in types:
            # distinct days (row 46): the difference's extremes sit at the feasible days nearest the interval ends
            ex = _excl_days(S, [Q["e1"], Q["e2"]])

            def ends(a, b):
                lo_d = [d for d in range(a, min(b, a + 4) + 1) if d not in ex]
                hi_d = [d for d in range(max(a, b - 4), b + 1) if d not in ex]
                return sorted(set(lo_d + hi_d))
            p1, p2 = ends(*d1), ends(*d2)
            diffs = [y - x for x in p1 for y in p2 if x != y]
            if not diffs:
                raise Drop("forced shared day")
            lo, hi = min(diffs), max(diffs)
        else:
            a1, b1 = d1
            a2, b2 = d2
            lo, hi = a2 - b1, b2 - a1
        return True if lo >= N else (False if hi < N else U)
    if t == "total":
        sets = [figure_set(S, k) for k in Q["figs"]]
        tot = _sum_sets(sets)
        thr = Q["T"]
        vals = set()
        for a, b in tot:
            if _cmp(a, Q["op"], thr) == _cmp(b, Q["op"], thr):
                vals.add(_cmp(a, Q["op"], thr))
            else:
                vals |= {True, False}
        return vals.pop() if len(vals) == 1 else U
    raise ValueError(t)


def timeline_unknowns(S: dict, Q: dict) -> list:
    """Visible gaps of an S4 record: (key, kind)."""
    out = []
    for k, e in S["events"].items():
        if e["k"] == "range":
            out.append((("ev", k), "gap:bound"))
        elif e["k"] == "month":
            out.append((("ev", k), "gap:month"))
        elif e["k"] == "marker":
            out.append((("ev", k), "gap:value"))
        elif e["k"] == "plan":
            typ = k.split("|")[0]
            closed = S["world"] == "closed" or (S["world"] == "local" and S.get("local") == typ)
            if not closed:
                out.append((("ev", k), "gap:plan"))
    for k, f in S["figures"].items():
        kk = {"range": "gap:bound", "round": "gap:round", "unitless": "gap:unit", "marker": "gap:value"}.get(f["k"])
        if kk:
            out.append((("fig", k), kk))
    for k, dom in S.get("day_dom", {}).items():
        if k in S["events"]:
            continue
        typ = k.split("|")[0]
        closed = S["world"] == "closed" or (S["world"] == "local" and S.get("local") == typ)
        if Q["t"] == "deadline" and Q["ev"] == k and Q["by"] > S["D"]:
            out.append((("ev", k), "gap:after_d"))
        elif not closed:
            out.append((("ev", k), "gap:value"))
    return out

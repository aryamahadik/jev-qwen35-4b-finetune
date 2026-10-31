"""Solver B (G0 section 4): model-style. It works on the PARSED structure (parse_f6.py output) and enumerates every
model over a test-point discretisation of each unknown (numbers: the domain ends plus n-1, n, n+1 around every
threshold; days: the domain ends plus the days around every other notice's day; categories: every value; yes/no:
both), keeps the models that satisfy the stated constraints (domains, closure, subclass implications, distinct notice
days), and evaluates Out per model with an explicit winner-set encoding. SAT(R and Out = o) is checked for every
outcome of the catalog; the drop conditions are checked on every model.

z3 (MIT) is named by the spec for solver B but is not installed in this environment and F6 may not download
packages; exhaustive enumeration over the test points is an exact decision procedure here (every atom is a
comparison with a constant, so the test points hit every region), and it is a different paradigm from solver A's
lazy three-valued case splits. Shares no code with solver_a.py.
"""
from __future__ import annotations

import itertools


class Dropped(Exception):
    pass


def _points_num(lo, hi, consts):
    pts = {lo, hi}
    for n in consts:
        for x in (n - 1, n, n + 1):
            if lo <= x <= hi:
                pts.add(x)
    return sorted(pts)


def _consts(S, aid):
    cs = []
    rules = S["rules"]
    for r in rules:
        for at in r["conds"] + ([r["unless"]] if r.get("unless") else []):
            if at["t"] == "num" and at["a"] == aid:
                cs.append(at["n"])
    for o in S.get("onlyif", []):
        if o["cond"]["t"] == "num" and o["cond"]["a"] == aid:
            cs.append(o["cond"]["n"])
    return cs


def model_space(S: dict, case: str):
    """[(var, [test values])] and the fixed part, for one case of a parsed rules structure."""
    facts = S["facts"][case]
    closed_all = S["world"] == "closed"
    local = S.get("local")
    tag = S.get("ev_tag") or {}
    tagged_counts = bool(tag.get("counts"))
    fixed, space = {}, []

    def state(f):
        if f is None or "plan" in f:
            return "absent"
        if f.get("m"):
            return "marker"
        if f.get("tag") and not tagged_counts:
            return "marker"
        return "known"

    for aid in sorted(S["attrs"]):
        a = S["attrs"][aid]
        f = facts["num" if a["kind"] == "num" else "cat"].get(aid)
        k = (a["kind"], aid)
        if state(f) == "known":
            fixed[k] = f["v"]
        elif a["kind"] == "num":
            space.append((k, _points_num(a["lo"], a["hi"], _consts(S, aid))))
        else:
            space.append((k, list(a["vals"])))
    for eid in sorted(S["events"]):
        f = facts["ev"].get(eid)
        k = ("ev", eid)
        s = state(f)
        if s == "known":
            fixed[k] = bool(f.get("v", True))
        elif s == "absent" and closed_all:
            fixed[k] = False
        else:
            space.append((k, [False, True]))
    for cid in sorted(S["classes"]):
        f = facts["cls"].get(cid)
        k = ("cls", cid)
        s = state(f)
        if s == "known":
            fixed[k] = bool(f.get("v", True))
        elif s == "absent" and (closed_all or local == cid):
            fixed[k] = False
        else:
            space.append((k, [False, True]))
    exact_days = sorted(n["date"]["d"] for n in S["notices"].values() if n["date"]["k"] == "exact")
    for nid in sorted(S["notices"]):
        d = S["notices"][nid]["date"]
        k = ("nd", nid)
        if d["k"] == "exact":
            fixed[k] = d["d"]
        else:
            pts = {d["a"], d["b"]}
            for e in exact_days:
                for x in (e - 1, e + 1):
                    if d["a"] <= x <= d["b"]:
                        pts.add(x)
            space.append((k, sorted(x for x in pts if x not in exact_days)))
    return fixed, space


def _expand_rules(S):
    rules = [dict(r) for r in S["rules"]]
    T = S.get("table")
    if T:
        for key, o in sorted(T["cells"].items()):
            a, b = key.split("|", 1)
            rules.append({"rid": f"{T['rid']}:{key}", "notice": T["notice"], "out": o, "unless": None, "exc": None,
                          "conds": [{"t": "cat", "a": T["A"], "v": a}, {"t": "cat", "a": T["B"], "v": b}]})
    return rules


def _holds(at, m):
    t = at["t"]
    if t == "num":
        x = m[("num", at["a"])]
        return {">=": x >= at["n"], ">": x > at["n"], "<=": x <= at["n"], "<": x < at["n"]}[at["op"]]
    if t == "cat":
        return m[("cat", at["a"])] == at["v"]
    if t == "ev":
        return m[("ev", at["e"])] != bool(at.get("neg"))
    if t == "cls":
        return m[("cls", at["c"])]
    raise ValueError(t)


def _sep(S, r, q, m):
    """+1 if r beats q, -1 if q beats r, 0 if tests 1-2 do not separate and the notices are the same."""
    if r.get("exc") == q["rid"]:
        return 1
    if q.get("exc") == r["rid"]:
        return -1
    cr = next((a["c"] for a in r["conds"] if a["t"] == "cls"), None)
    cq = next((a["c"] for a in q["conds"] if a["t"] == "cls"), None)
    subs = {tuple(x) for x in S.get("subclass", [])}
    if cr and cq and cr != cq:
        if (cr, cq) in subs:
            return 1
        if (cq, cr) in subs:
            return -1
    if r["notice"] == q["notice"]:
        return 0
    return 1 if m[("nd", r["notice"])] > m[("nd", q["notice"])] else -1


def out_of(S, rules, m):
    blocked = set()
    for o in S.get("onlyif", []):
        if not _holds(o["cond"], m):
            blocked.add(o["out"])
    live = []
    for r in rules:
        if all(_holds(a, m) for a in r["conds"]) and not (r.get("unless") and _holds(r["unless"], m)) \
                and r["out"] not in blocked:
            live.append(r)
    if not live:
        return S["default"]
    for r, q in itertools.combinations(live, 2):
        if r["out"] != q["out"] and _sep(S, r, q, m) == 0:
            raise Dropped("ii")
    W = [r for r in live if all(_sep(S, r, q, m) == 1 for q in live if q["out"] != r["out"])]
    outs = sorted({r["out"] for r in W})
    if len(outs) != 1:
        raise Dropped("i")
    return outs[0]


def models(S, case, extra=None):
    fixed, space = model_space(S, case)
    for k, v in (extra or {}).items():
        fixed[k] = v
        space = [(x, vals) for x, vals in space if x != k]
    subs = [tuple(x) for x in S.get("subclass", [])]
    names = [k for k, _ in space]
    for combo in itertools.product(*[vals for _, vals in space]):
        m = dict(fixed)
        m.update(zip(names, combo))
        if any(m.get(("cls", b)) is True and m.get(("cls", a)) is False for b, a in subs):
            continue
        days = [v for k, v in m.items() if k[0] == "nd"]
        if len(days) != len(set(days)):
            continue
        yield m


def possible(S, case, claim=None, extra=None):
    """P_B (claim None: the set of outcomes o with SAT(R and Out = o)) or T_B. Raises Dropped on a drop condition,
    or on an inconsistent R (no model)."""
    rules = _expand_rules(S)
    res = set()
    n = 0
    for m in models(S, case, extra):
        n += 1
        o = out_of(S, rules, m)
        if claim is None:
            res.add(o)
        else:
            v = (o == claim["o"])
            res.add((not v) if claim.get("neg") else v)
    if n == 0:
        raise Dropped("inconsistent")
    return res


def catalog_check(S, case, catalog):
    """SAT(R and Out = o) for every outcome of the catalog (row-level cross-check)."""
    P = possible(S, case)
    return {o: (o in P) for o in catalog}


def settling(S, case, gaps, claim=None):
    base = possible(S, case, claim)
    if len(base) == 1:
        return []
    fixed, space = model_space(S, case)
    sp = dict(space)
    out = []
    for g in gaps:
        g = tuple(g)
        if g not in sp:
            continue
        good = True
        for v in sp[g]:
            try:
                if len(possible(S, case, claim, extra={g: v})) != 1:
                    good = False
                    break
            except Dropped:
                good = False
                break
        if good:
            out.append(list(g))
    return out


def decidable(S, cases, claim_of=None):
    return [c for c in cases if len(possible(S, c, claim_of(c) if claim_of else None)) == 1]


# ================================================================ S3 tables: enumerate every completion of the marked cells

def _tb_points(col, consts):
    if col["kind"] == "cat":
        return list(col["vals"])
    return _points_num(col["lo"], col["hi"], consts)


def table_models(T: dict, Q: dict):
    cols = {c["id"]: c for c in T["cols"]}
    consts = {}
    for cond in (Q.get("cond"), Q.get("filter")):
        if cond and "n" in cond:
            consts.setdefault(cond["col"], []).append(cond["n"])
    if Q["t"] in ("argmax", "argmin"):
        consts.setdefault(Q["key"], []).extend(r["cells"][Q["key"]] for r in T["records"]
                                               if r["cells"][Q["key"]] is not None)
    holes = [(r["id"], c) for r in T["records"] for c, v in r["cells"].items() if v is None]
    spaces = [_tb_points(cols[c], consts.get(c, [])) for _, c in holes]
    for combo in itertools.product(*spaces):
        fill = dict(zip(holes, combo))
        yield [{"id": r["id"], **{c: fill.get((r["id"], c), v) for c, v in r["cells"].items()}}
               for r in T["records"]]


def _sat(col, x, cond):
    if "n" in cond:
        return {">=": x >= cond["n"], ">": x > cond["n"], "<=": x <= cond["n"], "<": x < cond["n"]}[cond["op"]]
    return x == cond["v"]


def table_values(T: dict, Q: dict) -> set:
    """T_B for a yes/no table query, or the set of possible argmax / argmin records (P_B)."""
    cols = {c["id"]: c for c in T["cols"]}
    t = Q["t"]
    if t == "member":
        L = T["list"]
        if Q["who"] in L["members"]:
            vals = {True}
        elif L["closed"]:
            vals = {False}
        else:
            vals = {True, False}
        return {not v for v in vals} if Q.get("neg") else vals
    out = set()
    for rows in table_models(T, Q):
        def passes(r):
            f = Q.get("filter")
            return f is None or _sat(cols[f["col"]], r[f["col"]], f)
        sel = [r for r in rows if passes(r)]
        if t in ("argmax", "argmin"):
            if not sel:
                raise Dropped("empty filtered set")
            k = Q["key"]
            best = max(r[k] for r in sel) if t == "argmax" else min(r[k] for r in sel)
            tied = sorted((r for r in sel if r[k] == best), key=lambda r: int(r["id"].split("-")[-1]))
            out.add(tied[0]["id"])
            continue
        hits = [r for r in sel if _sat(cols[Q["cond"]["col"]], r[Q["cond"]["col"]], Q["cond"])]
        if t == "exists":
            out.add(len(hits) >= 1)
        elif t == "forall":
            out.add(len(hits) == len(sel))
        elif t == "none":
            out.add(len(hits) == 0)
        elif t == "count":
            n, N = len(hits), Q["N"]
            out.add({">=": n >= N, ">": n > N, "<=": n <= N, "<": n < N}[Q["cmp"]])
        else:
            raise ValueError(t)
    return out


# ================================================================ S4 timelines: enumerate test points of every unknown

def _closed_type(S, typ):
    return S["world"] == "closed" or (S["world"] == "local" and S.get("local") == typ)


def timeline_values(S: dict, Q: dict) -> set:
    """T_B: the claim's value over every model of the parsed timeline (days and figures at test points)."""
    D = S["D"]
    ev_vars, fig_vars = [], []
    thr_days = set()
    if Q["t"] == "deadline":
        thr_days.add(Q["by"])
    exact_days = {e["d"] for e in S["events"].values() if e["k"] == "exact"}
    keys = set(S["events"]) | set(S.get("day_dom", {}))
    for key in sorted(keys):
        e = S["events"].get(key)
        typ = key.split("|")[0]
        closed = _closed_type(S, typ)
        if e is None or e["k"] in ("marker", "plan"):
            if e is None and closed:
                continue
            if e is not None and e["k"] == "plan" and closed:
                continue
            dom = S["day_dom"].get(key)
            pts = {None}
            if dom:
                a, b = dom
                cand = {a, b} | {x + dd for x in thr_days | exact_days for dd in (-1, 0, 1)}
                pts |= {x for x in cand if a <= x <= b}
            ev_vars.append((key, sorted(pts, key=lambda x: (x is not None, x or 0))))
        elif e["k"] in ("range", "month"):
            a, b = e["a"], e["b"]
            cand = {a, b} | {x + dd for x in thr_days | exact_days for dd in (-1, 0, 1)}
            ev_vars.append((key, sorted(x for x in cand if a <= x <= b)))
    thr = []
    if Q["t"] == "total":
        thr = [Q["T"]]
    for key in sorted(S["figures"]):
        f = S["figures"][key]
        q = S["quantities"][f["q"]]
        m = q.get("conv", 1) if f.get("unit") == "V" else 1
        if f["k"] == "range":
            fig_vars.append((key, sorted({f["a"] * m, f["b"] * m} | {x for x in range(f["a"] * m, f["b"] * m + 1)
                                                                       if False})))
            pts = {f["a"] * m, f["b"] * m}
            fig_vars[-1] = (key, sorted(pts | set(range(f["a"] * m, f["b"] * m + 1)) if f["b"] - f["a"] < 400
                                        else pts))
        elif f["k"] == "round":
            h = q["R"] * m // 2
            lo, hi = f["x"] * m - h, f["x"] * m + h - 1
            fig_vars.append((key, list(range(lo, hi + 1))))
        elif f["k"] == "unitless":
            fig_vars.append((key, [f["x"], f["x"] * q["conv"]]))
        elif f["k"] == "marker":
            fig_vars.append((key, list(range(q["lo"], q["hi"] + 1)) if q["hi"] - q["lo"] < 400 else [q["lo"], q["hi"]]))
    # totals: only the figures named in the question matter; keep the others at one point
    if Q["t"] == "total":
        fig_vars = [(k, v) if k in Q["figs"] else (k, v[:1]) for k, v in fig_vars]
    else:
        fig_vars = [(k, v[:1]) for k, v in fig_vars]
    names = [k for k, _ in ev_vars] + [k for k, _ in fig_vars]
    spaces = [v for _, v in ev_vars] + [v for _, v in fig_vars]
    out = set()
    noshare = set(S.get("noshare_types") or [])
    n = 0
    if Q["t"] == "total":
        # enumerate the sum by convolution of the named figures (exact; avoids a product blow-up)
        sums = {0}
        for k in Q["figs"]:
            vals = dict(fig_vars)[k] if k in dict(fig_vars) else None
            if vals is None:
                f = S["figures"][k]
                q = S["quantities"][f["q"]]
                m = q.get("conv", 1) if f.get("unit") == "V" else 1
                vals = [f["x"] * m]
            sums = {a + b for a in sums for b in vals}
        for x in sums:
            out.add({">=": x >= Q["T"], ">": x > Q["T"], "<=": x <= Q["T"], "<": x < Q["T"]}[Q["op"]])
        return out
    for combo in itertools.product(*spaces):
        m = dict(zip(names, combo))
        days = {}
        for key in keys:
            e = S["events"].get(key)
            if key in m:
                days[key] = m[key]
            elif e is not None and e["k"] == "exact":
                days[key] = e["d"]
            else:
                days[key] = None
        # distinct days among the no-shared-day types (row 46)
        seen = [d for k, d in days.items() if d is not None and k.split("|")[0] in noshare]
        if len(seen) != len(set(seen)):
            continue
        if any(d is not None and d > D for d in days.values()):
            continue
        n += 1
        t = Q["t"]
        if t == "deadline":
            d = days.get(Q["ev"])
            if d is None and Q["by"] > D:
                vals = {False, True}
            else:
                vals = {d is not None and d <= Q["by"]}
            out |= {(not v) if Q.get("neg") else v for v in vals}
        elif t == "before":
            d1, d2 = days.get(Q["e1"]), days.get(Q["e2"])
            if d1 is None or d2 is None:
                raise Dropped("compared event not recorded")
            v = d1 < d2
            out.add((not v) if Q.get("neg") else v)
        elif t == "daycount":
            d1, d2 = days.get(Q["e1"]), days.get(Q["e2"])
            if d1 is None or d2 is None:
                raise Dropped("compared event not recorded")
            out.add(d2 - d1 >= Q["N"])
    if n == 0:
        raise Dropped("no model")
    return out

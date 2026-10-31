"""Instance construction and fact-flip twin search for gen_constraints.

An instance = domain D, context ctx, hard requirements cons, optional tie-break, labelled options (effective values),
shown overrides (a listed value that a later correction note replaces), correction notes, and whether a
"none of the listed ..." option is offered.  Fail sets are planned first (winner = {}, co-qualifiers = {} when a
tie-break exists, near-misses fail exactly one requirement, the rest fail two or more) and option values are then
sampled per requirement (near-misses as close to the boundary as the grid allows) until the realised fail set equals
the plan.  The label is always recomputed by the solver (cst_core.solve), never taken from the plan.
"""
import copy
from fractions import Fraction as Fr

from cst_core import MISSING, NA, BoolCon, CatCon, CmpCon, SetCon, solve, tv, unk

N_OPTS_W = {4: 8, 5: 12, 6: 14, 7: 13, 8: 12, 9: 9, 10: 8, 11: 6, 12: 6}
M_W = {2: 14, 3: 36, 4: 32, 5: 18}


def wpick(rng, d):
    ks = list(d)
    return rng.choices(ks, weights=[d[k] for k in ks])[0]


def sample_for(c, rng, D, ctx, o, want, near, free_only=None, n=28):
    """Values for c's unassigned attributes (or only `free_only`) making c's truth == want."""
    free = [a for a in c.attrs if a not in o] if free_only is None else list(free_only)
    if not free:
        return {} if ((tv(c.pred(), o, ctx) is True) == want) else None
    cands = []
    for _ in range(n):
        x = dict(o)
        for a in free:
            x[a] = D.A[a].gen(rng, ctx, x)
        cands.append(x)
    for a, v in c.focus(ctx):
        if a in free:
            for _ in range(2):
                x = dict(o)
                x[a] = v
                for b in free:
                    if b != a:
                        x[b] = D.A[b].gen(rng, ctx, x)
                cands.append(x)
    good = []
    for x in cands:
        D.derive(x, ctx)
        if not D.valid(x, ctx):
            continue
        if (tv(c.pred(), x, ctx) is True) == want:
            good.append(x)
    if not good:
        return None
    if near:
        ms = [(c.margin(x, ctx), k) for k, x in enumerate(good)]
        mn = min(m for m, _ in ms)
        lim = mn if rng.random() < 0.5 else mn + 2  # right at the boundary, or within two grid steps of it
        pick = good[rng.choice([k for m, k in ms if m <= lim])]
    else:
        pick = rng.choice(good)
    return {a: pick[a] for a in free}


def realised(cons, o, ctx):
    return frozenset(c.cid for c in cons if tv(c.pred(), o, ctx) is not True)


def gen_option(D, rng, ctx, cons, F, near_p=0.75, tries=40):
    for _ in range(tries):
        o = {}
        ok = True
        for c in rng.sample(cons, len(cons)):
            want = c.cid not in F
            near = (rng.random() < near_p) if not want else (rng.random() < 0.12)
            asg = sample_for(c, rng, D, ctx, o, want, near)
            if asg is None:
                ok = False
                break
            o.update(asg)
        if not ok:
            continue
        for a in D.attrs:
            if not a.derived and a.key not in o:
                o[a.key] = a.gen(rng, ctx, o)
        D.derive(o, ctx)
        if not D.valid(o, ctx):
            continue
        if realised(cons, o, ctx) == F:
            return o
    return None


def pick_cons(D, rng, ctx, m):
    chosen, groups = [], set()
    for grp in D.required:
        opts = [mk for mk in D.makers if mk[1] == grp]
        c = rng.choices(opts, weights=[x[0] for x in opts])[0][2](rng, ctx, D)
        if c is None:
            return []
        c.cid = f"c{len(chosen)}"
        chosen.append(c)
        groups.add(grp)
    for _ in range(80):
        if len(chosen) >= m:
            break
        w = [mk[0] if mk[1] not in groups else 0 for mk in D.makers]
        if sum(w) == 0:
            break
        k = rng.choices(range(len(D.makers)), weights=w)[0]
        _, grp, fn = D.makers[k]
        c = fn(rng, ctx, D)
        if c is None:
            continue
        groups.add(grp)
        if any(set(c.attrs) & set(x.attrs) for x in chosen):
            continue
        c.cid = f"c{len(chosen)}"
        chosen.append(c)
    return chosen


def simple_attr(c):
    """The single attribute of a simple requirement (plain threshold / bool / category / set), else None."""
    if isinstance(c, CmpCon) and c.expr == ("a", c.attr.key) and not c.implicit:
        return c.attr.key
    if isinstance(c, (BoolCon, CatCon, SetCon)):
        return c.attr.key
    return None


def robust(inst):
    """Cross-unit requirements must give the same verdict under the stated and the exact conversion factor."""
    for c in inst["cons"]:
        xu = getattr(c, "xunit", None)
        if not xu:
            continue
        key, op, fac, alt, dec = xu
        t1 = Fr(c.params["d"]) / (10 ** dec) * fac
        t2 = Fr(c.params["d"]) / (10 ** dec) * alt
        vals = [o[key] for o in inst["opts"]] + [v for (i, a), v in inst["shown"].items() if a == key]
        for v in vals:
            if unk(v):
                continue
            r1 = v <= t1 if op == "<=" else v < t1 if op == "<" else v >= t1 if op == ">=" else v > t1
            r2 = v <= t2 if op == "<=" else v < t2 if op == "<" else v >= t2 if op == ">=" else v > t2
            if r1 != r2:
                return False
    return True


def tie_attrs(inst):
    return set(inst["tie"].attrs) if inst["tie"] else set()


def con_attrs(inst):
    return {a for c in inst["cons"] for a in c.attrs}


def build_instance(D, rng):
    ctx = D.ctx_fn(rng)
    ngroups = len({g for _, g, _ in D.makers})
    m = min(wpick(rng, M_W), ngroups)
    cons = pick_cons(D, rng, ctx, m)
    if len(cons) < max(2, D.min_cons):
        return None
    tie = None
    if D.ties and rng.random() < 0.36:
        tie = rng.choice(D.ties)(rng, ctx, D)
    none_opt = rng.random() < 0.25
    n = wpick(rng, N_OPTS_W)
    q = 1
    if tie is not None:
        q += wpick(rng, {0: 30, 1: 45, 2: 25})
    none_gold = none_opt and rng.random() < 0.35
    if none_gold:
        q = 0
    cids = [c.cid for c in cons]
    plans = [frozenset()] * q
    nm = list(cids)
    rng.shuffle(nm)
    for cid in nm[:max(0, n - q)]:
        plans.append(frozenset([cid]))
    while len(plans) < n:
        if rng.random() < 0.35:
            plans.append(frozenset([rng.choice(cids)]))
        else:
            k = rng.randint(2, len(cids))
            plans.append(frozenset(rng.sample(cids, k)))
    opts = []
    for F in plans:
        o = gen_option(D, rng, ctx, cons, F)
        if o is None:
            return None
        opts.append(o)
    order = list(range(n))
    rng.shuffle(order)
    opts = [opts[i] for i in order]
    plans = [plans[i] for i in order]
    if D.label_fn:
        labels = D.label_fn(rng, ctx, n)
    elif D.letters:
        labels = D.labels[:n]
    else:
        pool = [L for L in D.labels if not L.startswith(ctx.get("name", "~") + " ")]
        labels = rng.sample(pool, n)
    inst = {"D": D, "ctx": ctx, "cons": cons, "tie": tie, "labels": labels, "opts": opts, "shown": {}, "notes": [],
            "none_opt": none_opt, "plans": plans}
    g, Q = solve(inst)
    # exact tie on the tie-break among qualifiers: regenerate tied qualifiers a few times
    for _ in range(12):
        if g is not None:
            break
        if tie is None or len(Q) < 2:
            return None
        j = rng.choice(Q)
        o = gen_option(D, rng, ctx, cons, frozenset())
        if o is None:
            return None
        opts[j] = o
        g, Q = solve(inst)
    if g is None:
        return None
    # attractive near-miss: a near-miss beats the winner on the tie-break key
    if tie is not None and g != "none" and rng.random() < 0.6:
        nms = [i for i, F in enumerate(plans) if len(F) == 1]
        if nms:
            j = rng.choice(nms)
            kw = tie.key(opts[g], ctx)
            for _ in range(15):
                o = gen_option(D, rng, ctx, cons, plans[j])
                if o is None:
                    break
                k2 = tie.key(o, ctx)
                if k2 is not None and kw is not None and k2 < kw:
                    opts[j] = o
                    break
    g, Q = solve(inst)
    if g is None:
        return None
    ta = tie_attrs(inst)
    # a near-miss whose only failure is a detail the listing does not state
    if rng.random() < 0.2:
        cand = []
        for i, o in enumerate(opts):
            fs = [c for c in cons if tv(c.pred(), o, ctx) is not True]
            if len(fs) == 1:
                a = simple_attr(fs[0])
                if a and D.A[a].missing_ok and a not in ta and sum(a in c.attrs for c in cons) == 1:
                    cand.append((i, a))
        if cand:
            i, a = rng.choice(cand)
            opts[i][a] = MISSING
            D.derive(opts[i], ctx)
    # an unknown value in a column no requirement uses (it must not disqualify anything)
    if rng.random() < 0.08:
        ca = con_attrs(inst) | ta
        free = [a.key for a in D.attrs if a.key not in ca and not a.derived and a.missing_ok]
        if free:
            i = rng.randrange(n)
            a = rng.choice(free)
            opts[i][a] = MISSING
            D.derive(opts[i], ctx)
    # a printed correction that changes one option's status on one requirement (the list shows the old value)
    if rng.random() < 0.12:
        add_correction(inst, rng, trap=True)
    g, Q = solve(inst)
    if g is None or not robust(inst):
        return None
    inst["gold"] = g
    inst["Q"] = Q
    return inst


def add_correction(inst, rng, trap=True, target=None):
    """trap=True: keep the effective value, show an old value with the opposite verdict on that requirement.
    trap=False (twin move): change the effective value (flipping the verdict), keep the old value on display."""
    D, ctx = inst["D"], inst["ctx"]
    ta = tie_attrs(inst)
    opts = inst["opts"]
    cands = []
    for i, o in enumerate(opts):
        if target is not None and i != target:
            continue
        for c in inst["cons"]:
            a = simple_attr(c)
            if not a or a in ta or D.A[a].derived or unk(o.get(a)) or (i, a) in inst["shown"]:
                continue
            if sum(a in x.attrs for x in inst["cons"]) != 1:
                continue
            cands.append((i, c, a))
    rng.shuffle(cands)
    for i, c, a in cands[:6]:
        o = opts[i]
        t = tv(c.pred(), o, ctx) is True
        x = {k: v for k, v in o.items() if k != a}
        asg = sample_for(c, rng, D, ctx, x, not t, rng.random() < 0.5, free_only=[a])
        if asg is None:
            continue
        v = asg[a]
        if v == o[a]:
            continue
        if trap:
            inst["shown"][(i, a)] = v
        else:
            inst["shown"][(i, a)] = o[a]
            o[a] = v
            D.derive(o, ctx)
        inst["notes"].append((i, a))
        return (i, a)
    return None


# ------------------------------------------------------------------------------------------------ twins
def clone(inst):
    t = dict(inst)
    t["opts"] = [dict(o) for o in inst["opts"]]
    t["shown"] = dict(inst["shown"])
    t["notes"] = list(inst["notes"])
    t["cons"] = list(inst["cons"])
    return t


def mv_opt_attr(inst, rng):
    D, ctx = inst["D"], inst["ctx"]
    g = inst["gold"]
    n = len(inst["opts"])
    roles = []
    if g != "none":
        roles += [g] * 4
    roles += [i for i in inst["Q"] if i != g] * 2
    roles += [i for i in range(n) if len(inst["plans"][i]) == 1 or len(realised(inst["cons"], inst["opts"][i], ctx)) == 1] * 2
    roles += list(range(n))
    i = rng.choice(roles)
    keys = [a for c in inst["cons"] for a in c.attrs] + (list(inst["tie"].attrs) if inst["tie"] else [])
    keys = [k for k in dict.fromkeys(keys) if not D.A[k].derived and not unk(inst["opts"][i].get(k))
            and (i, k) not in inst["shown"]]
    if not keys:
        return None
    a = rng.choice(keys)
    vals = [D.A[a].gen(rng, ctx, inst["opts"][i]) for _ in range(14)]
    for c in inst["cons"]:
        vals += [v for k, v in c.focus(ctx) if k == a]
    rng.shuffle(vals)
    for v in vals:
        if v == inst["opts"][i][a]:
            continue
        t = clone(inst)
        t["opts"][i][a] = v
        D.derive(t["opts"][i], ctx)
        if not D.valid(t["opts"][i], ctx):
            continue
        gg, Q = solve(t)
        if gg is not None and gg != g and robust(t):
            return t, {"move": "option_value", "option": inst["labels"][i], "attr": a}
    return None


def mv_con_param(inst, rng):
    D, ctx = inst["D"], inst["ctx"]
    js = list(range(len(inst["cons"])))
    rng.shuffle(js)
    for j in js:
        vs = inst["cons"][j].variants(rng, D, ctx)
        rng.shuffle(vs)
        for v in vs[:10]:
            v.cid = inst["cons"][j].cid
            t = clone(inst)
            t["cons"][j] = v
            gg, Q = solve(t)
            if gg is not None and gg != inst["gold"] and robust(t):
                return t, {"move": "requirement", "requirement": j}
    return None


def mv_tie(inst, rng):
    if inst["tie"] is None or len(inst["Q"]) < 2:
        return None
    D, ctx = inst["D"], inst["ctx"]
    fs = list(D.ties)
    rng.shuffle(fs)
    for f in fs:
        tb = f(rng, ctx, D)
        if tb is None or tb.tid == inst["tie"].tid:
            continue
        t = clone(inst)
        t["tie"] = tb
        gg, Q = solve(t)
        if gg is not None and gg != inst["gold"]:
            return t, {"move": "tie_break", "tie": tb.tid}
    return None


def mv_correction(inst, rng):
    n = len(inst["opts"])
    order = list(range(n))
    rng.shuffle(order)
    if inst["gold"] != "none":
        order.remove(inst["gold"])
        order.insert(0, inst["gold"])
    for i in order[:4]:
        t = clone(inst)
        r = add_correction(t, rng, trap=False, target=i)
        if r is None:
            continue
        gg, Q = solve(t)
        if gg is not None and gg != inst["gold"] and robust(t):
            return t, {"move": "correction", "option": inst["labels"][r[0]], "attr": r[1]}
    return None


def mv_missing(inst, rng):
    D, ctx = inst["D"], inst["ctx"]
    ta = tie_attrs(inst)
    # fill a missing value so that the option now meets that requirement
    for i, o in enumerate(inst["opts"]):
        for a, v in o.items():
            if v != MISSING:
                continue
            cs = [c for c in inst["cons"] if a in c.attrs]
            if len(cs) != 1:
                continue
            x = {k: w for k, w in o.items() if k != a}
            asg = sample_for(cs[0], rng, D, ctx, x, True, False, free_only=[a])
            if asg is None:
                continue
            t = clone(inst)
            t["opts"][i][a] = asg[a]
            D.derive(t["opts"][i], ctx)
            gg, Q = solve(t)
            if gg is not None and gg != inst["gold"] and robust(t):
                return t, {"move": "fill_missing", "option": inst["labels"][i], "attr": a}
    # blank a decisive value of the winner
    g = inst["gold"]
    if g == "none":
        return None
    cands = []
    for c in inst["cons"]:
        a = simple_attr(c)
        if a and D.A[a].missing_ok and a not in ta and (g, a) not in inst["shown"] and \
                sum(a in x.attrs for x in inst["cons"]) == 1:
            cands.append(a)
    rng.shuffle(cands)
    for a in cands:
        t = clone(inst)
        t["opts"][g][a] = MISSING
        D.derive(t["opts"][g], ctx)
        gg, Q = solve(t)
        if gg is not None and gg != g:
            return t, {"move": "blank_value", "option": inst["labels"][g], "attr": a}
    return None


MOVES = {"opt_attr": (mv_opt_attr, 40, 8), "con_param": (mv_con_param, 30, 3), "tie": (mv_tie, 12, 1),
         "correction": (mv_correction, 10, 2), "missing": (mv_missing, 8, 1)}


def make_twin(inst, rng):
    names = list(MOVES)
    order = []
    pool = list(names)
    while pool:
        k = rng.choices(pool, weights=[MOVES[x][1] for x in pool])[0]
        order.append(k)
        pool.remove(k)
    for k in order:
        fn, _, tries = MOVES[k]
        for _ in range(tries):
            r = fn(inst, rng)
            if r is None:
                continue
            t, desc = r
            gg, Q = solve(t)
            t["gold"], t["Q"] = gg, Q
            t["plans"] = inst["plans"]
            return t, desc
    return None

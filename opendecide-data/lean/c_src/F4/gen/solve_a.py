"""Solver A on one row (sampled structure): labels, gold answer, 2.2 checks, depth, inference tags, pivot list.

analyze(rec, card, row) -> dict with "ok" and either the analysis or a reject reason. Every reject reason is a short
code; the sampler resamples and counts them.
"""
from __future__ import annotations

from decimal import Decimal

import core as C

FREE_BUDGET = 16


def claim_lit(cl):
    pred, e, pos = cl
    return (C.u(pred, e), pos)


def row_claims(row):
    """{key: claim literal} for the row's form."""
    f = row["form"]
    if f == "CH-claim":
        return {i: claim_lit(cl) for i, cl in enumerate(row["options"]) if cl is not None}
    if f == "CH-entity":
        H = row["H"]
        return {i: (C.u(H, e), True) for i, e in enumerate(row["options"])}
    return {"c": claim_lit(row["claim"])}


def free_atoms_of_component(units, clauses, atom):
    comp = C.component(clauses, [atom])
    assign, conf, _ = C.unit_propagate(units, comp)
    free = set()
    for lits, _ in comp:
        if any(assign.get(a) == p for a, p in lits):
            continue
        for a, p in lits:
            if a not in assign:
                free.add(a)
    return len(free)


def gold_from_labels(row, labels):
    f = row["form"]
    if f in ("CH-claim",):
        return C.answer(f, labels, none_shown=row.get("none_shown", False))
    return C.answer(f, labels)


def cond_tags(rule, x, view):
    tags = set()
    for c in rule.conds:
        if c[0] in ("cmp", "rng"):
            tags.add("inf:thr")
            v = view.values.get((x, c[1]))
            if v is not None and ((c[0] == "cmp" and v == c[3]) or (c[0] == "rng" and v in (c[2], c[3]))):
                tags.add("boundary:eq")
        elif c[0] in ("dcmp", "win"):
            tags.add("inf:date")
            v = view.dates.get((x, c[1]))
            if v is not None and ((c[0] == "dcmp" and v == c[3]) or (c[0] == "win" and v in (c[2], c[3]))):
                tags.add("boundary:eq")
    return tags


def ow_proof_info(g, assign, view, lit):
    cost = C.derivation_costs(g, assign, view)
    if lit not in cost:
        return None
    insts, lits_used = C.proof_instances(cost, lit)
    tags = set()
    rules = {r.rid: r for r in view.rules}
    for (i, j) in insts:
        lits, meta = g.clauses[i]
        rid, x, kind, hp, has_exc = meta
        r = rules.get(rid)
        k = C.instance_kind(g, (i, j))
        if k in ("contra", "partner"):
            tags.add("inf:mt")
        if kind.startswith("link:"):
            tags.add("inf:link")
        if kind.startswith("kofn"):
            tags.add("inf:kofn")
        if has_exc:
            tags.add("inf:exc")
        if r is not None:
            tags |= cond_tags(r, x, view)
    leaves = [l for l in lits_used if cost[l][1] is None]
    return {"depth": cost[lit][0], "tags": tags, "leaves": leaves, "rules": sorted({g.clauses[i][1][0]
                                                                                    for i, j in insts})}


def silent_exception(view, claim_lit_, assign=None):
    """'known true, so the rule is silent': some rule for the decided head literal has its exception true for x."""
    a, p = claim_lit_
    if a[0] != "u":
        return False
    x = a[2]
    for r in view.rules:
        if r.exc and r.head[0] == a[1] and view.ents.get(x) == r.typ:
            if view.facts.get(C.u(r.exc, x)) is True:
                return True
    return False


def analyze(rec: C.Record, card: C.Card, row: dict, *, near_miss=(), want_pivots=True) -> dict:
    W = card.world or "OW"
    claims = row_claims(row)
    view = C.base_view(rec, card, world=W)
    if any(x[0] == "conflict" for x in view.extra):
        return {"ok": False, "why": "fact_conflict"}
    res = {"ok": True, "world": W}
    labels = {}
    if W == "OW":
        g = C.ground(view)
        assign, conf, reason = C.unit_propagate(g.units, g.clauses)
        if conf:
            return {"ok": False, "why": "inconsistent"}
        if not C.horn_renamable(g.units, g.clauses):
            return {"ok": False, "why": "not_horn"}
        # guards 9a / 9b on UP(T)
        for a, why in reason.items():
            if isinstance(why, int):
                if C.is_exc_atom(a, view):
                    return {"ok": False, "why": "guard9a"}
                if C.is_cmp_atom(a):
                    return {"ok": False, "why": "guard9b"}
        for k, cl in claims.items():
            lab = C.label_ow_up(g, cl)
            if lab == "X":
                return {"ok": False, "why": "inconsistent"}
            labels[k] = lab
            if lab in ("F", "R"):
                tgt = cl if lab == "F" else C.neg(cl)
                if assign.get(tgt[0]) != tgt[1]:
                    return {"ok": False, "why": "not_direct"}
            if free_atoms_of_component(g.units, g.clauses, cl[0]) > FREE_BUDGET:
                return {"ok": False, "why": "budget"}
        # anonymous-entity check for hedges (2.1)
        for (kind, typ, cnd, hd) in rec.hedges:
            z = "__anon__"
            v2 = C.View(**view.__dict__)
            v2.ents = {**view.ents, z: typ}
            v2.facts = {**view.facts, C.u(cnd[0], z): cnd[1]}
            g2 = C.ground(v2)
            a2, c2, _ = C.unit_propagate(g2.units, g2.clauses)
            if c2 or C.u(hd[0], z) in a2:
                return {"ok": False, "why": "hedge_anon"}
    else:
        M, ok, _ = C.cw_model(view)
        if not ok:
            return {"ok": False, "why": "cw_inconsistent"}
        for k, cl in claims.items():
            labels[k] = "F" if C.cw_val(view, M, cl[0]) == cl[1] else "R"
    res["labels"] = labels
    gold = gold_from_labels(row, labels)
    if gold == "PIVOT":
        return {"ok": False, "why": "no_single_gold"}
    res["gold"] = gold
    # depth and tags for the row's c
    c_lit = claim_lit(row["c"])
    if W == "OW":
        lab_c = C.label_ow_up(g, c_lit)
    else:
        lab_c = "F" if C.cw_val(view, M, c_lit[0]) == c_lit[1] else "R"
    res["label_c"] = lab_c
    depth, tags, leaves, nm_info = None, set(), [], []
    if W == "OW" and lab_c in ("F", "R"):
        tgt = c_lit if lab_c == "F" else C.neg(c_lit)
        info = ow_proof_info(g, assign, view, tgt)
        depth, tags, leaves = info["depth"], info["tags"], info["leaves"]
        res["rules"] = list(info.get("rules", []))     # decisive rules (position check only; repair r1)
        if silent_exception(view, tgt):
            tags.add("inf:exc")
        res["derivation"] = True
    elif W == "CW" and C.cw_val(view, M, c_lit[0]):
        depth = C.cw_depth(view, c_lit[0])
        res["derivation"] = True
        tags = cw_tags(view, M, c_lit[0])
    else:
        res["derivation"] = False
    # near-miss chains (2.2 #5): each failing premise, if it held, decides c (or its negation)
    for nm in near_miss:
        d, t = near_miss_depth(rec, card, W, c_lit, nm, base_leaves=leaves if res["derivation"] else ())
        if d is None:
            return {"ok": False, "why": "near_miss_invalid"}
        nm_info.append({"premise": nm, "depth": d, "tags": sorted(t)})
    if not nm_info:
        return {"ok": False, "why": "no_near_miss"}
    if not res["derivation"]:
        depth = max(x["depth"] for x in nm_info)
        tags = set(next(x for x in nm_info if x["depth"] == depth)["tags"])
    if depth is None or depth >= 10 ** 6:
        return {"ok": False, "why": "depth_none"}
    res["depth"], res["tags"], res["leaves"], res["near_miss"] = depth, sorted(tags), leaves, nm_info
    if want_pivots:
        pv = pivots(rec, card, row, claims, gold)
        if not pv["ok"]:
            return {"ok": False, "why": pv["why"]}
        res["pivots"] = pv["pivots"]
        res["rival_answers"] = pv["answers"]
    return res


def cw_tags(view, M, atom):
    tags = set()
    for r in view.rules:
        if r.head == (atom[1], True):
            for c in r.conds:
                pass
    # walk the support of the atom
    stack, seen = [atom], set()
    while stack:
        a = stack.pop()
        if a in seen or a[0] != "u":
            continue
        seen.add(a)
        if view.facts.get(a) is True:
            continue
        for r in view.rules:
            if r.form == "onlyif" or r.head != (a[1], True) or view.ents.get(a[2]) != r.typ:
                continue
            for body, exc, head, kind in C.ground_bodies(r, a[2], view):
                if exc is not None and view.facts.get(exc[0]) is True:
                    continue
                if all(C.cw_val(view, M, b[0]) == b[1] for b in body):
                    if kind.startswith("link:"):
                        tags.add("inf:link")
                    if kind.startswith("kofn"):
                        tags.add("inf:kofn")
                    if exc is not None:
                        tags.add("inf:exc")
                    tags |= cond_tags(r, a[2], view)
                    stack.extend(b[0] for b in body if b[1])
                    break
    return tags


def near_miss_depth(rec, card, W, c_lit, nm, base_leaves=()):
    """nm = (atom, value) premise that fails in the record. Returns (depth, tags) of the chain that decides c or not c
    once the premise holds, else (None, None). A near-miss that would decide a decided c the other way is evaluated
    with the base derivation's leaf facts left out (the chain alone decides it)."""
    atom, val = nm
    view = C.base_view(rec, card, world=W)
    f2 = dict(view.facts)
    if atom[0] == "V":
        view.values = {**view.values, (atom[1], atom[2]): atom[3]}
    elif atom[0] == "D":
        view.dates = {**view.dates, (atom[1], atom[2]): atom[3]}
    else:
        f2[atom] = val
    view.facts = f2
    view.extra = [x for x in view.extra if x[0] != "conflict"]
    if W == "OW":
        g = C.ground(view)
        assign, conf, _ = C.unit_propagate(g.units, g.clauses)
        if conf and base_leaves:
            f3 = {a: v for a, v in f2.items() if (a, v) not in set(map(tuple, base_leaves)) or a == atom}
            view.facts = f3
            g = C.ground(view)
            assign, conf, _ = C.unit_propagate(g.units, g.clauses)
        if conf:
            return None, None
        for tgt in (c_lit, C.neg(c_lit)):
            if assign.get(tgt[0]) == tgt[1]:
                info = ow_proof_info(g, assign, view, tgt)
                if info is None or info["depth"] == 0:
                    return None, None
                return info["depth"], info["tags"]
        return None, None
    M, ok, _ = C.cw_model(view)
    if not ok or not C.cw_val(view, M, c_lit[0]):
        return None, None
    d = C.cw_depth(view, c_lit[0])
    if d == 0 or d >= 10 ** 6:
        return None, None
    return d, cw_tags(view, M, c_lit[0])


def pivots(rec, card, row, claims, gold):
    form = row["form"]
    labs = C.rival_labels(rec, card, claims)
    answers, piv = {}, []
    for rv, lab in labs.items():
        if lab == "BUDGET":
            return {"ok": False, "why": "r30_budget"}
        a = C.answer(form, lab, r25=(rv == "R25"), none_shown=row.get("none_shown", False))
        answers[rv] = a
        if a != gold:
            piv.append(rv)
    for rv in piv:
        t = C.TAG.get(rv, rv)
        if t == "R27":
            return {"ok": False, "why": "pivot_R27"}
        if t in C.ASSERT_RIVALS:
            return {"ok": False, "why": "assert_" + t}
        if not C.ruled_out(rv, card):
            return {"ok": False, "why": "unruled_" + t}
    if "R22" in piv and "R2" not in piv:
        return {"ok": False, "why": "assert_R22subR2"}
    if card.short:
        pl = C.short_pair_labels(rec, card, claims)
        for k, lab in pl.items():
            if isinstance(lab, dict) and any(str(v).startswith("BUDGET") for v in lab.values()):
                return {"ok": False, "why": "r30_budget"}
            a = C.answer(form, lab, none_shown=row.get("none_shown", False))
            if a != gold:
                return {"ok": False, "why": "short_pair_" + k}
    tags = sorted({C.TAG.get(r, r) for r in piv})
    return {"ok": True, "pivots": tags, "answers": {k: str(v) for k, v in answers.items()}}

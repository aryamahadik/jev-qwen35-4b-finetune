"""Solver B (G2/G3): a different paradigm from solver A. It reads only the PARSED structure and the PARSED LF.

S1: model enumeration. Every unknown fact (open card), every unrecorded value (closed card; over its SEM-04 test set)
and every outcome atom is enumerated; a model must satisfy the rules as constraints: on closed cards the Clark
completion of the positive-deriving rules (atom level, F5-R4-01) plus the negated heads as constraints; on open cards
every rule as a material clause. The SEM-24 closure is added as definitions (permitted iff no listed rule forbids,
required iff some listed rule requires). Gold = the LF value shared by every model; both values or no model -> error.
"""
from __future__ import annotations

import itertools


class BUndetermined(Exception):
    pass


def _cmp(v, op, n):
    if op == ">=":
        return v >= n
    if op == ">":
        return v > n
    if op == "<=":
        return v <= n
    if op == "<":
        return v < n
    return v == n


# ---------------------------------------------------------------------------------------------------------------------
# S1

def _s1_lit(l, w):
    t = l["t"]
    if t in ("adj", "has"):
        x = w[(t, l["w"])]
        return x if l["pol"] == "pos" else (not x)
    if t == "num":
        return _cmp(w[("num", l["q"])], l["op"], l["n"])
    if t == "cat":
        x = w[("cat", l["c"])]
        return (x == l["v"]) if l["pol"] == "pos" else (x != l["v"])
    raise ValueError(t)


def _s1_body(r, w):
    """Does rule r apply in world w (its body holds and its exception does not)?"""
    if r["form"] == "if":
        ok = all(_s1_lit(c, w) for c in r["conds"])
    elif r["form"] in ("unless", "onlyif"):
        ok = not _s1_lit(r["conds"][0], w)
    else:
        ok = True
    if ok and r.get("exc"):
        ok = not _s1_lit(r["exc"], w)
    return ok


def _s1_gives(r):
    """(atom, value) the rule gives when it applies (atom level); None for deontic heads."""
    h = r["head"]
    if h["kind"] != "adj":
        return None
    pos = h["pol"] == "pos"
    if r["form"] == "onlyif":
        return ("adj", h["word"]), (not pos)
    return ("adj", h["word"]), pos


FORBID = {"must not", "may not", "is not permitted to", "cannot"}
REQUIRE = {"must", "is required to"}
MAYS = {"may", "is permitted to"}
NEEDNOT = {"need not", "does not have to", "is not required to"}


def _s1_deon(P, r, w):
    """Closure contribution of one rule for (role, verb): 'forbid' / 'require' / 'may' / 'neednot' / None."""
    h = r["head"]
    if h["kind"] != "deon":
        return None
    if r["form"] == "onlyif":
        return "forbid" if not _s1_lit(r["conds"][0], w) else None
    if not _s1_body(r, w):
        return None
    m = h["modal"]
    return "forbid" if m in FORBID else "require" if m in REQUIRE else "may" if m in MAYS else "neednot"


def _s1_status(S, w, role, verb, which):
    eff = [_s1_deon(None, r, w) for r in S["rules"] if r["head"]["kind"] == "deon" and r["head"]["role"] == role
           and r["head"]["verb"] == verb]
    for c in S["table"]:
        if c["role"] == role and c["verb"] == verb:
            eff.append({"forbidden": "forbid", "required": "require", "permitted": "may"}[c["cell"]])
    if ("may" in eff and "forbid" in eff) or ("require" in eff and "forbid" in eff) or \
            ("neednot" in eff and "require" in eff):
        raise ValueError("deontic conflict")
    return ("forbid" not in eff) if which == "perm" else ("require" in eff)


def _s1_eval(lf, S, w):
    op = lf[0]
    if op == "not":
        return not _s1_eval(lf[1], S, w)
    if op == "and":
        return all(_s1_eval(x, S, w) for x in lf[1:])
    if op == "or":
        return any(_s1_eval(x, S, w) for x in lf[1:])
    if op == "adj":
        return w[("adj", lf[2])]
    if op == "has":
        return w[("has", lf[2])]
    if op == "deon":
        return _s1_status(S, w, lf[2], lf[3], lf[1])
    if op == "amt":
        a = S["amount"]
        x = w[("num", a["qty"])]
        v = min(x, a["limit"]) if a["kind"] == "cap" else max(x, a["limit"])
        return _cmp(v, lf[3], lf[4])
    if op == "inv":
        return w[("adj", lf[2])]
    raise ValueError(op)


def lf_atoms(lf, out=None):
    out = set() if out is None else out
    if isinstance(lf, list) and lf:
        if lf[0] in ("adj", "has") and len(lf) == 3:
            out.add((lf[0], lf[2]))
        else:
            for x in lf[1:]:
                lf_atoms(x, out)
    return out


def s1_models(S, extra_atoms=()):
    """Every model of the parsed S1 structure (dict atom -> value)."""
    closed = S["world"] == "closed"
    fixed, free = {}, []
    outs = set()
    for r in S["rules"]:
        g = _s1_gives(r)
        if g:
            outs.add(g[0])
        for l in r["conds"] + ([r["exc"]] if r.get("exc") else []):
            if l["t"] in ("adj", "has"):
                k = (l["t"], l["w"])
                if k not in S["facts"] and k not in outs:
                    pass
    fact_atoms = set(S["facts"])
    lit_atoms = set()
    for r in S["rules"]:
        for l in r["conds"] + ([r["exc"]] if r.get("exc") else []):
            if l["t"] in ("adj", "has"):
                lit_atoms.add((l["t"], l["w"]))
    for k in sorted(fact_atoms | lit_atoms | set(extra_atoms)):
        if k in outs:
            continue
        form = S["facts"].get(k)
        if form is None:
            if closed:
                fixed[k] = False
            else:
                free.append(k)
        else:
            fixed[k] = form == "pos"
    # numbers / categories
    tests = {}
    thresholds = {}
    for r in S["rules"]:
        for l in r["conds"] + ([r["exc"]] if r.get("exc") else []):
            if l["t"] == "num":
                thresholds.setdefault(l["q"], set()).add(l["n"])
    if S["amount"]:
        thresholds.setdefault(S["amount"]["qty"], set()).add(S["amount"]["limit"])
    num_names = set(S["nums"]) | set(thresholds)
    for q in sorted(num_names):
        v = S["nums"].get(q)
        if v is None or v[0] == "NR":
            ths = thresholds.get(q, {0})
            tests[("num", q)] = sorted({t + d for t in ths for d in (-1, 0, 1)})
        else:
            fixed[("num", q)] = v[0]
    cat_names = set(S["cats"])
    for r in S["rules"]:
        for l in r["conds"] + ([r["exc"]] if r.get("exc") else []):
            if l["t"] == "cat":
                cat_names.add(l["c"])
    for c in sorted(cat_names):
        v = S["cats"].get(c)
        if v is None or v == "NR":
            tests[("cat", c)] = list(S["value_sets"].get(c) or [])
            if not tests[("cat", c)]:
                raise ValueError(f"no value set for {c}")
        else:
            fixed[("cat", c)] = v
    outs = sorted(outs)
    tkeys = sorted(tests)
    models = []
    for tv in itertools.product(*[tests[k] for k in tkeys]) if tkeys else [()]:
        for fv in itertools.product([False, True], repeat=len(free)):
            for ov in itertools.product([False, True], repeat=len(outs)):
                w = dict(fixed)
                w.update(zip(tkeys, tv))
                w.update(zip(free, fv))
                w.update(zip(outs, ov))
                if _s1_ok(S, w, outs, closed):
                    models.append(w)
    return models


def _s1_ok(S, w, outs, closed):
    for r in S["rules"]:
        g = _s1_gives(r)
        if g and _s1_body(r, w) and w[g[0]] != g[1]:
            return False
    if closed:
        for o in outs:
            support = any(_s1_body(r, w) for r in S["rules"] if (_s1_gives(r) or (None,))[0] == o
                          and _s1_gives(r)[1] is True)
            if w[o] != support:
                return False
    return True


def s1_solve(S, lfs):
    extra = set()
    for lf in lfs:
        lf_atoms(lf, extra)
    models = s1_models(S, extra)
    if not models:
        raise BUndetermined("no model (inconsistent)")
    out = []
    for lf in lfs:
        vals = {_s1_eval(lf, S, w) for w in models}
        if len(vals) != 1:
            raise BUndetermined(f"undetermined over {len(models)} models")
        out.append(vals.pop())
    return out

"""F10 hidden structure: legend, definition ASTs, cards, cases; solver A (definition substitution + completion
enumeration, G0 section 4). Values are in grid units: numeric = int (value x 10^d), date = ordinal day, category =
str, flag = bool, tag set = sorted tuple of tags. Everything here is JSON-able (lists / dicts / str / int / bool)."""
from __future__ import annotations

import datetime as dt
import itertools
import json
from functools import lru_cache

NUM_TYPES = ("count", "amount", "qty")
INF = None  # open interval end


# ---------------------------------------------------------------------------------------------------- constructors
def A_cmp(a, op, c):
    return {"k": "atom", "t": "cmp", "a": a, "op": op, "c": c}


def A_rng(a, lo, hi, half=False):
    return {"k": "atom", "t": "rng", "a": a, "lo": lo, "hi": hi, "half": bool(half)}


def A_cat(a, S, neg=False, style="oneof"):
    return {"k": "atom", "t": "cat", "a": a, "S": sorted(S), "neg": bool(neg), "style": style}


def A_flag(a, v):
    return {"k": "atom", "t": "flag", "a": a, "v": bool(v)}


def A_tag(a, m, S=(), kk=0):
    return {"k": "atom", "t": "tag", "a": a, "m": m, "S": sorted(S), "kk": int(kk)}


def A_rel(x, e, n, d):
    return {"k": "atom", "t": "rel", "a": x, "e": e, "n": int(n), "dir": d}


def R(to, neg=False):
    return {"k": "ref", "to": to, "neg": bool(neg)}


def It(atom, unless=None):
    return {"k": "item", "atom": atom, "unless": unless}


def Body(form, items):
    return {"k": "body", "form": form, "items": list(items)}


def Def(did, body, onlyif=None, exc=None, helper=False, section=None):
    return {"id": did, "body": body, "onlyif": onlyif, "exc": exc, "helper": bool(helper), "section": section}


# ---------------------------------------------------------------------------------------------------- evaluation
def eval_atom(at, case):
    t = at["t"]
    if t == "rel":
        x, e = case[at["a"]], case[at["e"]]
        d = x - e
        n = at["n"]
        return 1 <= d <= n if at["dir"] == "after" else -n <= d <= -1
    v = case[at["a"]]
    if t == "cmp":
        c, op = at["c"], at["op"]
        return {"ge": v >= c, "gt": v > c, "le": v <= c, "lt": v < c, "eq": v == c, "ne": v != c}[op]
    if t == "rng":
        return at["lo"] <= v < at["hi"] if at["half"] else at["lo"] <= v <= at["hi"]
    if t == "cat":
        return (v in at["S"]) != at["neg"]
    if t == "flag":
        return v == at["v"]
    if t == "tag":
        m, S, vs = at["m"], set(at["S"]), set(v)
        if m == "has":
            return S <= vs
        if m == "any":
            return bool(S & vs)
        if m == "all":
            return S <= vs
        if m == "none":
            return not (S & vs)
        if m == "atl":
            return len(vs) >= at["kk"]
        if m == "atlof":
            return len(S & vs) >= at["kk"]
    raise ValueError(f"bad atom {at}")


class Card:
    """Definitions of one card: terms (ordered by card position) + helpers; evaluates raw definitions."""

    def __init__(self, defs: dict, order: list):
        self.defs = defs          # id -> Def
        self.order = list(order)  # term ids in card order (helpers excluded)

    def cond(self, c, case):
        if c is None:
            return True
        if c["k"] == "ref":
            return self.meets(c["to"], case) != c["neg"]
        return eval_atom(c, case)

    def item(self, it, case):
        if it["k"] == "ref":
            return self.meets(it["to"], case) != it["neg"]
        v = eval_atom(it["atom"], case)
        if v and it.get("unless") is not None:
            v = not self.cond(it["unless"], case)
        return v

    def body(self, b, case):
        f, its = b["form"], b["items"]
        vals = [self.item(i, case) for i in its]
        if f in ("single", "ALL"):
            return all(vals)
        if f == "ANY":
            return any(vals)
        if f in ("NOTANY", "NEITHER"):
            return not any(vals)
        if f == "NOTALL":
            return not all(vals)
        if f == "XOR":
            return sum(vals) == 1
        raise ValueError(f)

    def meets(self, did, case):
        d = self.defs[did]
        return self.body(d["body"], case) and self.cond(d["onlyif"], case) and not (
            d["exc"] is not None and self.cond(d["exc"], case))

    def assigned(self, did, case, ordered: bool):
        if not self.meets(did, case):
            return False
        if ordered:
            for t in self.order:
                if t == did:
                    return True
                if self.meets(t, case):
                    return False
        return True

    def assigned_term(self, case, ordered: bool):
        """The single assigned term, or 'none'. At-most-one / partition cards: the unique met term (error if > 1)."""
        met = [t for t in self.order if self.meets(t, case)]
        if not met:
            return "none"
        if ordered:
            return met[0]
        if len(met) > 1:
            raise ValueError("at-most-one card: case meets two term definitions")
        return met[0]


# ---------------------------------------------------------------------------------------------------- completions
def atom_consts(at):
    """(slot, constants in grid units) used by an atom: thresholds for the cell partition (solver A completions)."""
    t = at["t"]
    if t == "cmp":
        return [(at["a"], [at["c"]])]
    if t == "rng":
        return [(at["a"], [at["lo"], at["hi"]])]
    if t == "rel":
        return [(("d", at["a"], at["e"]), [at["n"], -at["n"], 0])]
    return []


def walk_atoms(x):
    """Every atom inside a Def / Body / Item / condition."""
    if x is None:
        return
    if isinstance(x, list):
        for y in x:
            yield from walk_atoms(y)
        return
    k = x.get("k")
    if k == "atom":
        yield x
    elif k == "item":
        yield x["atom"]
        yield from walk_atoms(x.get("unless"))
    elif k == "body":
        yield from walk_atoms(x["items"])
    elif k is None and "body" in x:
        yield from walk_atoms(x["body"])
        yield from walk_atoms(x.get("onlyif"))
        yield from walk_atoms(x.get("exc"))


def walk_refs(x):
    if x is None:
        return
    if isinstance(x, list):
        for y in x:
            yield from walk_refs(y)
        return
    k = x.get("k")
    if k == "ref":
        yield x
    elif k == "item":
        yield from walk_refs(x.get("unless"))
    elif k == "body":
        yield from walk_refs(x["items"])
    elif k is None and "body" in x:
        yield from walk_refs(x["body"])
        yield from walk_refs(x.get("onlyif"))
        yield from walk_refs(x.get("exc"))


def rel_pairs(defs):
    """{(x, e)} relative-date pairs used anywhere on the card."""
    out = set()
    for d in defs.values():
        for at in walk_atoms(d):
            if at["t"] == "rel":
                out.add((at["a"], at["e"]))
    return out


def slot_consts(defs, slot):
    cs = set()
    for d in defs.values():
        for at in walk_atoms(d):
            for s, c in atom_consts(at):
                if s == slot:
                    cs.update(c)
    return sorted(cs)


def reps_numeric(consts, lo_bound):
    if not consts:
        return [lo_bound if lo_bound is not None else 0]
    r = set()
    for c in consts:
        r.update((c - 1, c, c + 1))
    r.add(max(consts) + 2)
    r.add(min(consts) - 2 if lo_bound is None else lo_bound)
    return sorted(x for x in r if lo_bound is None or x >= lo_bound)


def attr_reps(legend, defs, slot):
    a = legend[slot]
    t = a["type"]
    if t in NUM_TYPES:
        return reps_numeric(slot_consts(defs, slot), 0)
    if t == "date":
        return reps_numeric(slot_consts(defs, slot), None) if slot_consts(defs, slot) else [a["range"][0]]
    if t == "cat":
        return list(a["values"])
    if t == "flag":
        return [True, False]
    if t == "tag":
        vs = list(a["values"])
        return [tuple(c) for n in range(len(vs) + 1) for c in itertools.combinations(sorted(vs), n)]
    raise ValueError(t)


def completions(legend, defs, case, omitted):
    """All completions of an open-world case over the representative cells (AR09). case: slot -> value (omitted
    slots may be absent). Relative pairs: an omitted member is set through the d axis cells."""
    omitted = sorted(omitted)
    if not omitted:
        yield dict(case)
        return
    pairs = rel_pairs(defs)
    plan = []  # list of (slots, list of value tuples)
    done = set()
    for s in omitted:
        if s in done:
            continue
        pr = [p for p in pairs if s in p]
        if pr:
            x, e = pr[0]
            dcs = set()
            for d in defs.values():
                for at in walk_atoms(d):
                    if at["t"] == "rel" and (at["a"], at["e"]) == (x, e):
                        dcs.update((at["n"], -at["n"], 0))
            dreps = reps_numeric(sorted(dcs), None)
            if x in omitted and e in omitted:
                e0 = legend[e]["range"][0]
                plan.append(((x, e), [(e0 + dd, e0) for dd in dreps]))
                done.update((x, e))
            elif s == x:
                plan.append(((x,), [(case[e] + dd,) for dd in dreps]))
                done.add(x)
            else:
                plan.append(((e,), [(case[x] - dd,) for dd in dreps]))
                done.add(e)
        else:
            plan.append(((s,), [(v,) for v in attr_reps(legend, defs, s)]))
            done.add(s)
    for combo in itertools.product(*[p[1] for p in plan]):
        c = dict(case)
        for (slots, _), vals in zip(plan, combo):
            for s, v in zip(slots, vals):
                c[s] = v
        yield c


def possible_answers(card: Card, legend, case, omitted, ordered):
    """P = set of possible assigned answers over the completions ('none' included)."""
    P = set()
    for c in completions(legend, card.defs, case, omitted):
        P.add(card.assigned_term(c, ordered))
    return P


def possible_meets(card: Card, legend, case, omitted, did, ordered=False, kind="meets"):
    vals = set()
    for c in completions(legend, card.defs, case, omitted):
        vals.add(card.meets(did, c) if kind == "meets" else card.assigned(did, c, ordered))
        if len(vals) > 1:
            break
    return vals


# ---------------------------------------------------------------------------------------------------- canonical form
def canon_atom(at):
    t = at["t"]
    if t == "cmp":
        return ["CMP", at["a"], at["op"], at["c"]]
    if t == "rng":
        return ["ALL", sorted([["CMP", at["a"], "ge", at["lo"]], ["CMP", at["a"], "lt" if at["half"] else "le", at["hi"]]],
                              key=json.dumps)]
    if t == "cat":
        return ["CAT", at["a"], sorted(at["S"]), at["neg"]]
    if t == "flag":
        return ["FLAG", at["a"], at["v"]]
    if t == "tag":
        return ["TAG", at["a"], at["m"], sorted(at["S"]), at["kk"]]
    if t == "rel":
        return ["REL", at["a"], at["e"], at["n"], at["dir"]]
    raise ValueError(t)


def canon_cond(c, refc):
    if c is None:
        return None
    if c["k"] == "ref":
        return ["NOT" if c["neg"] else "IS", refc(c["to"])]
    return canon_atom(c)


def canon_item(it, refc):
    if it["k"] == "ref":
        return canon_cond(it, refc)
    a = canon_atom(it["atom"])
    if it.get("unless") is not None:
        return ["UNLESS", a, canon_cond(it["unless"], refc)]
    return a


def canon_def(defs, did, memo=None):
    """Canonical string of a definition; references are written REF(<referenced canonical string>) (R2-16)."""
    memo = {} if memo is None else memo
    if did in memo:
        return memo[did]
    d = defs[did]

    def refc(to):
        return "REF(" + canon_def(defs, to, memo) + ")"
    b = d["body"]
    its = [canon_item(i, refc) for i in b["items"]]
    body = its[0] if b["form"] == "single" else [b["form"], sorted(its, key=json.dumps)]
    s = json.dumps(["DEF", body, canon_cond(d["onlyif"], refc), canon_cond(d["exc"], refc),
                    d.get("section")], sort_keys=True)
    memo[did] = s
    return s


# ---------------------------------------------------------------------------------------------------- classes, depth
def atom_class(at, legend):
    t = at["t"]
    if t == "cmp":
        if legend[at["a"]]["type"] == "date":
            return 4
        return 1 if at["op"] in ("ge", "le") else 2
    if t == "rng":
        return 3
    if t == "rel":
        return 5
    if t == "cat":
        return 6 if at.get("style") in ("other", "except") else None
    if t == "tag":
        return 7
    return None


def def_classes(d, legend):
    cl = set()
    for at in walk_atoms(d):
        c = atom_class(at, legend)
        if c:
            cl.add(c)
    b = d["body"]
    for it in b["items"]:
        if it["k"] == "item" and it.get("unless") is not None:
            cl.add(8)
    if d.get("onlyif") is not None:
        cl.add(9)
    if d.get("exc") is not None:
        cl.add(10)
    if b["form"] in ("NOTANY", "NOTALL", "NEITHER"):
        cl.add(11)
    if b["form"] == "XOR":
        cl.add(12)
    if any(True for _ in walk_refs(d)):
        cl.add(13)
    if d.get("section") is not None:
        cl.add(15)
    return cl


def nest(defs, did, memo=None):
    memo = {} if memo is None else memo
    if did in memo:
        return memo[did]
    refs = [r["to"] for r in walk_refs(defs[did])]
    v = 0 if not refs else max(1 + nest(defs, t, memo) for t in refs)
    memo[did] = v
    return v


def r_def(card: Card, did, case, nmemo=None):
    """AR11 reference levels followed for one definition on one case."""
    defs = card.defs
    nmemo = {} if nmemo is None else nmemo

    def ctrue(c):
        if c is None or c["k"] == "atom":
            return 0
        to = c["to"]
        return 1 + (nest(defs, to, nmemo) if c["neg"] else r_def(card, to, case, nmemo))

    def cfalse(c):
        if c["k"] == "atom":
            return 0
        to = c["to"]
        return 1 + (r_def(card, to, case, nmemo) if c["neg"] else nest(defs, to, nmemo))

    def itrue(it):
        if it["k"] == "ref":
            return ctrue(it)
        u = it.get("unless")
        return 0 if u is None else cfalse(u)

    def ifalse(it):
        if it["k"] == "ref":
            return cfalse(it)
        opts = []
        if not eval_atom(it["atom"], case):
            opts.append(0)
        u = it.get("unless")
        if u is not None and card.cond(u, case):
            opts.append(ctrue(u))
        return min(opts) if opts else 0

    if not card.meets(did, case):
        return nest(defs, did, nmemo)
    d = defs[did]
    b = d["body"]
    its = b["items"]
    vals = [card.item(i, case) for i in its]
    f = b["form"]
    if f in ("single", "ALL"):
        w = max([itrue(i) for i in its] or [0])
    elif f == "ANY":
        w = min(itrue(i) for i, v in zip(its, vals) if v)
    elif f in ("NOTANY", "NEITHER"):
        w = max(ifalse(i) for i in its)
    elif f == "NOTALL":
        w = min(ifalse(i) for i, v in zip(its, vals) if not v)
    else:  # XOR
        w = max(itrue(i) if v else ifalse(i) for i, v in zip(its, vals))
    if d.get("onlyif") is not None:
        w = max(w, ctrue(d["onlyif"]))
    if d.get("exc") is not None:
        w = max(w, cfalse(d["exc"]))
    return w


def depth(card: Card, legend, case, omitted, required):
    """1 + max over completions and required definitions of r (AR11)."""
    best = 0
    for c in completions(legend, card.defs, case, omitted):
        for did in required:
            best = max(best, r_def(card, did, c))
    return 1 + best


# ---------------------------------------------------------------------------------------------------- dates, values
EPOCH = dt.date(1970, 1, 1).toordinal()


def date_of(o: int) -> dt.date:
    return dt.date.fromordinal(o)


def jdump(x) -> str:
    return json.dumps(x, sort_keys=True, ensure_ascii=False, default=list)

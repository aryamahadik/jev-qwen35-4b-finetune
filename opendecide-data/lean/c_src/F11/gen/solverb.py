"""F11 solver B (decision tree compiled from the parsed card) and solver C (bottom-up paradigm checks), G0 section 3.

Independence: imports only parse (the parsed structures) and the standard library. Works on parsed text only:
nominal values by name, numbers and dates exactly (B: integer scaling of every number; C: Fraction / date).
"""
from __future__ import annotations

import datetime as dt
from fractions import Fraction
from math import lcm

from parse import ParseError


class SolveError(ValueError):
    pass


# ------------------------------------------------------------------------------------------------ predicates
def cond_true(cond, vec):
    an, op, arg = cond
    if an not in vec:
        raise SolveError(f"attribute {an} unstated")
    x = vec[an]
    if op == "in":
        return x in arg
    if op == "pres":
        return x == "present"
    if op == "abs":
        return x == "absent"
    if op == "ge":
        return x >= arg
    if op == "lt":
        return x < arg
    raise SolveError(op)


def all_conds(pc):
    out = []
    for c in pc.codes.values():
        out += c.get("parts", [])
        if c.get("rule"):
            out.append(c["rule"][1])
    for conds, _ in pc.entries:
        out += conds
    for _, _, cond in pc.scope:
        out.append(cond)
    for cp in pc.couplets.values():
        out.append(cp["a"][0])
    return out


def with_default(pc, vec):
    v = dict(vec)
    if pc.default is not None and pc.default[0] not in v:
        v[pc.default[0]] = pc.default[1]
    return v


# ------------------------------------------------------------------------------------------------ Assign on parsed rules
def assign_box(pc, vec):
    F, red = set(), set()
    for cid, c in pc.codes.items():
        if not all(cond_true(p, vec) for p in c["parts"]):
            continue
        if c["rule"] is None:
            F.add(cid)
            continue
        kind, cond, tgt = c["rule"]
        b = cond_true(cond, vec)
        out = b if kind == "unless" else not b
        if out:
            F.add(tgt)
            red.add(tgt)
        else:
            F.add(cid)
    if len(F) == 1:
        return next(iter(F))
    if len(F) == 2 and not red:
        ws = [w for a, b, w in pc.notes if {a, b} == F]
        if len(ws) == 1:
            return ws[0]
    raise SolveError(f"|F|={len(F)} without a deciding note")


def group_of(pc, vec):
    g_attr = pc.groups[0]["gattr"]
    gv = vec[g_attr]
    home = [g["name"] for g in pc.groups if gv in g["vals"]]
    if len(home) != 1:
        raise SolveError("group values do not partition")
    h = home[0]
    for src, dst, cond in pc.scope:
        if src == h and cond_true(cond, vec):
            return dst
    return h


def assign_group(pc, vec):
    gname = group_of(pc, vec)
    g = next(x for x in pc.groups if x["name"] == gname)
    fit = [cid for cid in g["leaves"] if all(cond_true(p, vec) for p in pc.codes[cid]["parts"])]
    if len(fit) == 1:
        return fit[0]
    if not fit and g["residual"]:
        return g["residual"]
    raise SolveError("group gate: no single leaf")


def assign_list(pc, vec):
    for conds, cid in pc.entries:
        if all(cond_true(c, vec) for c in conds):
            return cid
    return pc.catch


def walk_key(pc, vec):
    n, path = 1, []
    while True:
        path.append(n)
        cp = pc.couplets[n]
        nxt = cp["a"][1] if cond_true(cp["a"][0], vec) else cp["b"]
        if nxt.isdigit():
            n = int(nxt)
            continue
        return nxt, path


def assign_short(pc, vec):
    want = " / ".join(vec[a] for a in pc.short_attrs)
    hits = [nm for nm, _ in pc.short_names if nm == want]
    if len(hits) != 1:
        raise SolveError("short card: no single name")
    return hits[0]


def run_rules(pc, vec):
    if pc.shape in ("box", "table"):
        return assign_box(pc, vec)
    if pc.shape == "group":
        return assign_group(pc, vec)
    if pc.shape == "list":
        return assign_list(pc, vec)
    if pc.shape == "key":
        return walk_key(pc, vec)[0]
    if pc.shape == "short":
        return assign_short(pc, vec)
    raise SolveError(f"shape {pc.shape}")


# ------------------------------------------------------------------------------------------------ solver B: tree
class Tree:
    def __init__(self, pc):
        self.pc = pc
        self.order = [a["name"] for a in pc.attrs] if pc.shape != "short" else list(pc.short_attrs)
        self.attrs = {a["name"]: a for a in pc.attrs} if pc.shape != "short" else {}
        thr = {}
        for an, op, arg in all_conds(pc):
            if op in ("ge", "lt"):
                thr.setdefault(an, set()).add(arg)
        self.thr = {k: sorted(v) for k, v in thr.items()}
        # integer scaling for numbers (B): every number times the LCD of the thresholds' denominators
        self.scale = {}
        for an, ts in self.thr.items():
            if ts and isinstance(ts[0], Fraction):
                self.scale[an] = lcm(*[t.denominator for t in ts]) if ts else 1
        self.root = self._build(0, {})

    def domain(self, an):
        """(branch keys, representative values)."""
        if self.pc.shape == "short":
            vals = sorted({nm.split(" / ")[self.order.index(an)] for nm, _ in self.pc.short_names})
            return vals, vals
        a = self.attrs[an]
        if a["kind"] == "nom":
            return list(a["values"]), list(a["values"])
        if a["kind"] == "pres":
            return ["present", "absent"], ["present", "absent"]
        ts = self.thr.get(an, [])
        keys = list(range(len(ts) + 1))
        reps = []
        for i in keys:
            if i == 0:
                if not ts:
                    reps.append(Fraction(0) if a["kind"] == "num" else dt.date(2000, 1, 1))
                else:
                    reps.append(ts[0] - (1 if a["kind"] == "num" else dt.timedelta(days=1)))
            else:
                reps.append(ts[i - 1])
        return keys, reps

    def _build(self, d, assignment):
        if d == len(self.order):
            try:
                return ("leaf", run_rules(self.pc, assignment))
            except SolveError as e:
                return ("bad", str(e))
        an = self.order[d]
        keys, reps = self.domain(an)
        kids = {}
        for k, rep in zip(keys, reps):
            kids[k] = self._build(d + 1, {**assignment, an: rep})
        return ("split", an, kids)

    def key_of(self, an, x):
        if self.pc.shape == "short":
            return x
        a = self.attrs[an]
        if a["kind"] in ("nom", "pres"):
            return x
        ts = self.thr.get(an, [])
        if a["kind"] == "num":
            s = self.scale.get(an, 1)
            xi = x * s
            if xi.denominator != 1:
                xi = Fraction(int(xi), 1) if xi > 0 else xi
            b = 0
            for t in ts:
                if xi >= t * s:
                    b += 1
            return b
        ords = [t.toordinal() for t in ts]
        xo = x.toordinal()
        return sum(1 for t in ords if xo >= t)

    def solve(self, vec):
        vec = with_default(self.pc, vec)
        node = self.root
        while node[0] == "split":
            _, an, kids = node
            if an not in vec:
                raise SolveError(f"attribute {an} unstated")
            node = kids[self.key_of(an, vec[an])]
        if node[0] == "bad":
            raise SolveError(node[1])
        return node[1]


# ------------------------------------------------------------------------------------------------ solver C
def solver_c(pc, vec):
    vec = with_default(pc, vec)
    if pc.shape in ("box", "table"):
        F = set()
        for cid, c in pc.codes.items():
            holds = all(cond_true(p, vec) for p in c["parts"])
            if holds and c["rule"]:
                kind, cond, tgt = c["rule"]
                b = cond_true(cond, vec)
                F.add(tgt if (b if kind == "unless" else not b) else cid)
            elif holds:
                F.add(cid)
        if len(F) == 1:
            return next(iter(F))
        if len(F) == 2:
            ws = {w for a, b, w in pc.notes if {a, b} == F}
            if len(ws) == 1:
                return ws.pop()
        raise SolveError("C: no single code")
    if pc.shape == "group":
        ins = [g["name"] for g in pc.groups if group_of(pc, vec) == g["name"]]
        if len(ins) != 1:
            raise SolveError("C: not exactly one group")
        g = next(x for x in pc.groups if x["name"] == ins[0])
        fits = [cid for cid in g["leaves"] if all(cond_true(p, vec) for p in pc.codes[cid]["parts"])]
        if g["residual"] and not fits:
            fits = [g["residual"]]
        if len(fits) != 1:
            raise SolveError("C: not exactly one leaf")
        return fits[0]
    if pc.shape == "list":
        regions = []
        for i, (conds, cid) in enumerate(pc.entries):
            if all(cond_true(c, vec) for c in conds) and not any(
                    all(cond_true(c, vec) for c in pc.entries[j][0]) for j in range(i)):
                regions.append(cid)
        if not regions:
            regions = [pc.catch]
        if len(regions) != 1:
            raise SolveError("C: regions overlap")
        return regions[0]
    if pc.shape == "key":
        # each code = OR of its root-to-leaf path conjunctions
        paths = []

        def rec(n, conds):
            cp = pc.couplets[n]
            for branch, cnd in (("a", [(cp["a"][0], True)]), ("b", [(cp["a"][0], False)])):
                nxt = cp["a"][1] if branch == "a" else cp["b"]
                cc = conds + cnd
                if nxt.isdigit():
                    rec(int(nxt), cc)
                else:
                    paths.append((nxt, cc))
        rec(1, [])
        hits = {cid for cid, cc in paths if all(cond_true(c, vec) == want for c, want in cc)}
        if len(hits) != 1:
            raise SolveError("C: key paths")
        return hits.pop()
    if pc.shape == "short":
        return assign_short(pc, vec)
    raise SolveError("C: shape")


def groups_c(pc, vec):
    return group_of(pc, with_default(pc, vec))

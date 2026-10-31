"""F10 solver B: region algebra on the PARSED card (G0 section 4). A different paradigm from solver A: every
definition compiles bottom-up (topological order of references) into a union of axis-aligned boxes over integer grid
axes; meets / assigned / choice gold are containment and intersection tests; the generation-time proofs
(disjointness, covering, non-empty, not-whole-domain, non-equivalence, no shadowed term, uncovered region) are region
identities. Axes: numeric = integer interval in grid units [0, inf); date = interval in days; one axis d per
relative-date pair (its two dates enter only through d); category / flag / tag set = finite value sets (a tag axis
ranges over all subsets of its vocabulary)."""
from __future__ import annotations

import itertools

NUM = ("count", "amount", "qty")


class Space:
    def __init__(self, legend: dict, pairs):
        self.legend = legend
        self.pairs = sorted(set(pairs))
        in_pair = {s for p in self.pairs for s in p}
        self.axes = {}
        for s, a in legend.items():
            t = a["type"]
            if t in NUM:
                self.axes[s] = ("I", 0, None)
            elif t == "date":
                if s not in in_pair:
                    self.axes[s] = ("I", None, None)
            elif t == "cat":
                self.axes[s] = ("S", frozenset(a["values"]))
            elif t == "flag":
                self.axes[s] = ("S", frozenset([True, False]))
            elif t == "tag":
                vs = sorted(a["values"])
                self.axes[s] = ("S", frozenset(tuple(c) for n in range(len(vs) + 1)
                                               for c in itertools.combinations(vs, n)))
        for x, e in self.pairs:
            self.axes[("d", x, e)] = ("I", None, None)

    # --------------------------------------------------------------- constraints
    @staticmethod
    def c_inter(c1, c2):
        if c1[0] == "I":
            lo = c1[1] if c2[1] is None else (c2[1] if c1[1] is None else max(c1[1], c2[1]))
            hi = c1[2] if c2[2] is None else (c2[2] if c1[2] is None else min(c1[2], c2[2]))
            return ("I", lo, hi)
        return ("S", c1[1] & c2[1])

    @staticmethod
    def c_empty(c):
        if c[0] == "I":
            return c[1] is not None and c[2] is not None and c[1] > c[2]
        return not c[1]

    @staticmethod
    def c_minus(c, cut):
        """c minus cut (cut already intersected with c): list of constraints."""
        if c[0] == "S":
            r = c[1] - cut[1]
            return [("S", r)] if r else []
        out = []
        lo, hi = c[1], c[2]
        if cut[1] is not None and (lo is None or lo < cut[1]):
            out.append(("I", lo, cut[1] - 1))
        if cut[2] is not None and (hi is None or hi > cut[2]):
            out.append(("I", cut[2] + 1, hi))
        return out

    def get(self, box, ax):
        return box.get(ax, self.axes[ax])

    def b_inter(self, b1, b2):
        out = dict(b1)
        for ax, c in b2.items():
            cc = self.c_inter(self.get(b1, ax), c)
            if self.c_empty(cc):
                return None
            out[ax] = cc
        return out

    def b_minus(self, b, cut):
        """b minus cut as disjoint boxes."""
        inter = self.b_inter(b, cut)
        if inter is None:
            return [b]
        out = []
        cur = dict(b)
        for ax, c in cut.items():
            have = self.get(cur, ax)
            cc = self.c_inter(have, c)
            for piece in self.c_minus(have, cc):
                nb = dict(cur)
                nb[ax] = piece
                out.append(nb)
            cur[ax] = cc
        return out

    # --------------------------------------------------------------- regions (lists of boxes)
    def full(self):
        return [{}]

    def minus(self, R, B):
        for cut in B:
            nxt = []
            for r in R:
                nxt.extend(self.b_minus(r, cut))
            R = nxt
            if not R:
                break
        return R

    def comp(self, R):
        return self.minus(self.full(), R)

    def inter(self, R1, R2):
        out = []
        for a in R1:
            for b in R2:
                c = self.b_inter(a, b)
                if c is not None:
                    out.append(c)
        return out

    @staticmethod
    def union(*Rs):
        out = []
        for R in Rs:
            out.extend(R)
        return out

    def empty(self, R):
        return not R

    def equal(self, R1, R2):
        return not self.minus(R1, R2) and not self.minus(R2, R1)

    # --------------------------------------------------------------- points and case boxes
    def point_box(self, case, omitted=()):
        """The case as a box: known axes fixed, omitted axes left at the full domain (open world)."""
        b = {}
        om = set(omitted)
        for ax in self.axes:
            if isinstance(ax, tuple):
                _, x, e = ax
                if x in om or e in om:
                    continue
                v = case[x] - case[e]
                b[ax] = ("I", v, v)
            elif ax in om:
                continue
            else:
                v = case[ax]
                if self.axes[ax][0] == "I":
                    b[ax] = ("I", v, v)
                else:
                    b[ax] = ("S", frozenset([tuple(sorted(v)) if isinstance(v, (list, tuple)) else v]))
        return b

    def box_in(self, box, R):
        return not self.minus([box], R)

    def box_meets(self, box, R):
        return bool(self.inter([box], R))

    # --------------------------------------------------------------- atoms
    def atom(self, at):
        t = at["t"]
        if t == "rel":
            ax = ("d", at["a"], at["e"])
            n = at["n"]
            return [{ax: ("I", 1, n)}] if at["dir"] == "after" else [{ax: ("I", -n, -1)}]
        s = at["a"]
        dom = self.axes[s]
        if t == "cmp":
            c, op = at["c"], at["op"]
            if op == "ne":
                return [b for b in ([{s: self.c_inter(dom, ("I", None, c - 1))}], [{s: self.c_inter(dom, ("I", c + 1, None))}])
                        for b in b if not self.c_empty(b[s])]
            iv = {"ge": ("I", c, None), "gt": ("I", c + 1, None), "le": ("I", None, c), "lt": ("I", None, c - 1),
                  "eq": ("I", c, c)}[op]
            cc = self.c_inter(dom, iv)
            return [] if self.c_empty(cc) else [{s: cc}]
        if t == "rng":
            cc = self.c_inter(dom, ("I", at["lo"], at["hi"] - 1 if at["half"] else at["hi"]))
            return [] if self.c_empty(cc) else [{s: cc}]
        if t == "cat":
            S = frozenset(at["S"])
            v = (dom[1] - S) if at["neg"] else (dom[1] & S)
            return [{s: ("S", v)}] if v else []
        if t == "flag":
            return [{s: ("S", frozenset([at["v"]]))}]
        if t == "tag":
            m, S, kk = at["m"], set(at["S"]), at["kk"]

            def ok(sub):
                vs = set(sub)
                return {"has": S <= vs, "all": S <= vs, "any": bool(S & vs), "none": not (S & vs),
                        "atl": len(vs) >= kk, "atlof": len(S & vs) >= kk}[m]
            v = frozenset(x for x in dom[1] if ok(x))
            return [{s: ("S", v)}] if v else []
        raise ValueError(t)


def _atoms(x):
    if x is None:
        return
    if isinstance(x, list):
        for y in x:
            yield from _atoms(y)
        return
    k = x.get("k")
    if k == "atom":
        yield x
    elif k == "item":
        yield x["atom"]
        yield from _atoms(x.get("unless"))
    elif k == "body":
        yield from _atoms(x["items"])
    elif "body" in x:
        yield from _atoms(x["body"])
        yield from _atoms(x.get("onlyif"))
        yield from _atoms(x.get("exc"))


class CardB:
    """Solver B over one parsed card: legend (slot -> attr), defs (id -> Def AST, helpers included), term order."""

    def __init__(self, legend, defs, order, ctype):
        pairs = set()
        for d in defs.values():
            for at in _atoms(d):
                if at["t"] == "rel":
                    pairs.add((at["a"], at["e"]))
        self.sp = Space(legend, pairs)
        self.legend, self.defs, self.order, self.ctype = legend, defs, list(order), ctype
        self.ordered = ctype in ("first", "dlist", "codebook")
        self.R = {}
        self._busy = set()
        for did in defs:
            self.region(did)

    def cond(self, c):
        if c["k"] == "ref":
            R = self.region(c["to"])
            return self.sp.comp(R) if c["neg"] else R
        return self.sp.atom(c)

    def region(self, did):
        if did in self.R:
            return self.R[did]
        if did in self._busy:
            raise ValueError("cyclic reference")
        self._busy.add(did)
        sp = self.sp
        d = self.defs[did]
        parts = []
        for it in d["body"]["items"]:
            if it["k"] == "ref":
                parts.append(self.cond(it))
            else:
                r = sp.atom(it["atom"])
                if it.get("unless") is not None:
                    r = sp.minus(r, self.cond(it["unless"]))
                parts.append(r)
        f = d["body"]["form"]
        if f in ("single", "ALL", "NOTALL"):
            r = sp.full()
            for p in parts:
                r = sp.inter(r, p)
            if f == "NOTALL":
                r = sp.comp(r)
        elif f in ("ANY", "NOTANY", "NEITHER"):
            r = sp.union(*parts)
            if f != "ANY":
                r = sp.comp(r)
        elif f == "XOR":
            a, b = parts
            r = sp.union(sp.minus(a, b), sp.minus(b, a))
        else:
            raise ValueError(f)
        if d.get("onlyif") is not None:
            r = sp.inter(r, self.cond(d["onlyif"]))
        if d.get("exc") is not None:
            r = sp.minus(r, self.cond(d["exc"]))
        self._busy.discard(did)
        self.R[did] = r
        return r

    def assigned_region(self, did):
        R = self.region(did)
        if not self.ordered:
            return R
        for t in self.order:
            if t == did:
                break
            R = self.sp.minus(R, self.region(t))
        return R

    def union_terms(self):
        return self.sp.union(*[self.region(t) for t in self.order])

    def none_region(self):
        return self.sp.comp(self.union_terms())

    # --------------------------------------------------------------- answers
    def _tri(self, box, R):
        if self.sp.box_in(box, R):
            return True
        if not self.sp.box_meets(box, R):
            return False
        return None

    def meets(self, did, case, omitted=()):
        return self._tri(self.sp.point_box(case, omitted), self.region(did))

    def assigned(self, did, case, omitted=()):
        return self._tri(self.sp.point_box(case, omitted), self.assigned_region(did))

    def possible(self, case, omitted=()):
        box = self.sp.point_box(case, omitted)
        P = {t for t in self.order if self.sp.box_meets(box, self.assigned_region(t))}
        if self.sp.box_meets(box, self.none_region()):
            P.add("none")
        return P

    # --------------------------------------------------------------- generation-time proofs (section 4)
    def draw_box(self, draw):
        """draw: slot -> (lo, hi) grid-unit draw ranges for numeric / date slots (pack ranges)."""
        b = {}
        for ax in self.sp.axes:
            if isinstance(ax, tuple):
                _, x, e = ax
                if x in draw and e in draw:
                    b[ax] = ("I", draw[x][0] - draw[e][1], draw[x][1] - draw[e][0])
            elif ax in draw:
                b[ax] = ("I", draw[ax][0], draw[ax][1])
        return b

    def proofs(self, draw=None, need_uncovered=False):
        """Dict of failed proof names (empty = all pass)."""
        sp = self.sp
        bad = []
        ids = list(self.defs)
        for did in ids:
            R = self.region(did)
            if not R:
                bad.append(f"empty:{did}")
            elif not sp.comp(R):
                bad.append(f"whole:{did}")
        for a, b in itertools.combinations(ids, 2):
            if sp.equal(self.region(a), self.region(b)):
                bad.append(f"equiv:{a}:{b}")
        if self.ctype in ("amo", "partition"):
            for a, b in itertools.combinations(self.order, 2):
                if sp.inter(self.region(a), self.region(b)):
                    bad.append(f"overlap:{a}:{b}")
        if self.ctype == "partition" and self.none_region():
            bad.append("cover")
        if self.ordered:
            for t in self.order:
                if not self.assigned_region(t):
                    bad.append(f"shadowed:{t}")
        if need_uncovered:
            box = self.draw_box(draw or {})
            if not sp.inter([box], self.none_region()):
                bad.append("uncovered")
        return bad

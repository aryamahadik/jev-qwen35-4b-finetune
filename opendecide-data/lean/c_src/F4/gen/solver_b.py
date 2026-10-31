"""Solver B (G0 spec section 3): a different paradigm from solver A. It reads only the G3-parsed canonical structure
and decides by MODEL ENUMERATION: for OW readings it enumerates every assignment of the free atoms in the claim's
formula-connected component (numpy, vectorised) and keeps the models of the parsed formulas; for CW readings it
enumerates the assignments that satisfy Clark's completion of the parsed program (exactly one is expected). Every
rival (7.2) is rebuilt here from the canonical structure with this module's own code, and the answer mapping is
re-implemented. Values use solver B's own comparator: integers scaled by 10^k and dates as day ordinals.

No code is shared with solver A (core.py); the only shared input is the canonical structure the parser wrote.
"""
from __future__ import annotations

import itertools
import json

import numpy as np

MAX_FREE = 22


class Budget(Exception):
    pass


# ------------------------------------------------------------------------------------------------------- values

def scaled(s):
    """'118.5' -> (1185, 1): integer scaled by 10^k."""
    if s is None:
        return None
    s = str(s)
    if "." in s:
        a, b = s.split(".")
        return (int(a + b) if not a.startswith("-") else -int(a[1:] + b), len(b))
    return (int(s), 0)


def cmp_scaled(v, t):
    """Compare two scaled numbers: -1, 0, 1."""
    (a, ka), (b, kb) = v, t
    k = max(ka, kb)
    a *= 10 ** (k - ka)
    b *= 10 ** (k - kb)
    return (a > b) - (a < b)


def day(s):
    if s is None:
        return None
    y, m, d = (int(x) for x in s.split("-"))
    # days since 0001-01-01 (proleptic Gregorian), own formula
    def leap(yy):
        return yy % 4 == 0 and (yy % 100 != 0 or yy % 400 == 0)
    mdays = [31, 29 if leap(y) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    yp = y - 1
    return yp * 365 + yp // 4 - yp // 100 + yp // 400 + sum(mdays[:m - 1]) + d


def cond_value(c, v, incl=(True, True), opflip=None):
    """Truth of a written condition c (canonical list) on value v (None = missing -> None)."""
    k = c[0]
    if v is None:
        return None
    if k == "cmp":
        op = opflip.get(c[2], c[2]) if opflip else c[2]
        r = cmp_scaled(scaled(v), scaled(c[3]))
        return {">": r > 0, ">=": r >= 0, "<": r < 0, "<=": r <= 0}[op]
    if k == "rng":
        lo = cmp_scaled(scaled(v), scaled(c[2]))
        hi = cmp_scaled(scaled(v), scaled(c[3]))
        return (lo >= 0 if incl[0] else lo > 0) and (hi <= 0 if incl[1] else hi < 0)
    if k == "dcmp":
        op = opflip.get(c[2], c[2]) if opflip else c[2]
        a, b = day(v), day(c[3])
        return {">": a > b, ">=": a >= b, "<": a < b, "<=": a <= b}[op]
    if k == "win":
        a, lo, hi = day(v), day(c[2]), day(c[3])
        return (a >= lo if incl[0] else a > lo) and (a <= hi if incl[1] else a < hi)
    raise ValueError(k)


# ------------------------------------------------------------------------------------------------------- reading

class Reading:
    """One reading (card value or a rival) of the canonical structure."""

    def __init__(self, cn, *, world, unless, trust, rules=None, closures=None, links_mode=None, missing_false=False,
                 ground_all=False, cw_mode="plain", fact_variant=None, claim_atoms=(), merge=False, opflip=None,
                 range_incl=(True, True), date_flip=False, extra=None, drop_same_head=False, hedge_rules=False,
                 ehedge_facts=False):
        self.cn = cn
        self.world, self.unless, self.trust = world, unless, trust
        self.ents = {e: t for e, t in cn["ents"]}
        self.rules = rules if rules is not None else cn["rules"]
        self.closures = closures if closures is not None else cn["closures"]
        self.missing_false = missing_false
        self.ground_all = ground_all
        self.cw_mode = cw_mode
        self.opflip = opflip
        self.range_incl = range_incl
        self.date_flip = date_flip
        self.extra = extra or []
        self.conflict = False
        self.facts, self.links, self.vals, self.dates, self.markers = {}, set(), {}, {}, set()
        self.cell_links = set()
        for s in cn["stmts"]:
            kind, key, e, v, prov = s
            counts = self._counts(prov, kind, key, e, fact_variant, claim_atoms)
            if not counts:
                continue
            if kind == "lit":
                a = f"{key}|{e}"
                if v is None:
                    self.markers.add(a)
                    continue
                if a in self.facts and self.facts[a] != v:
                    self.conflict = True
                self.facts[a] = v
            elif kind == "link":
                self.links.add((key, e, v))
                if prov == "cell":
                    self.cell_links.add((key, e, v))
            elif kind == "val":
                self.vals[(e, key)] = v
            elif kind == "date":
                self.dates[(e, key)] = v
        if fact_variant == "R20":
            rep = {}
            for li, s in enumerate(cn["stmts"]):
                kind, key, e, v, prov = s
                if kind == "lit" and v is not None and prov.startswith("attr:") and not self._counts(
                        prov, kind, key, e, None, ()):
                    rep.setdefault((f"{key}|{e}", v), set()).add(li)
            for hi, (k_, e, p) in enumerate(cn["ehedges"]):
                rep.setdefault((f"{p}|{e}", True), set()).add(f"hedge{hi}")
            for (a, v), ss in rep.items():
                if len(ss) >= 2:
                    if a in self.facts and self.facts[a] != v:
                        self.conflict = True
                    self.facts[a] = v
        if ehedge_facts:
            for k_, e, p in cn["ehedges"]:
                a = f"{p}|{e}"
                if self.facts.get(a) is False:
                    self.conflict = True
                self.facts[a] = True
        if hedge_rules:
            add = []
            for kind, t, c, h in cn["hedges"]:
                if kind in ("most", "many", "usually", "often"):
                    add.append(["univ", t, [["lit", c[0], c[1]]], h, None, None, None, None, None, 0, "record"])
            self.rules = list(self.rules) + add
        if links_mode == "sym_trans":
            L_ = set(self.links)
            L_ |= {(k, b, a) for k, a, b in L_}
            while True:
                new = {(k1, a, d) for (k1, a, b) in L_ for (k2, c, d) in L_ if k1 == k2 and b == c and a != d}
                if new <= L_:
                    break
                L_ |= new
            self.links = L_
        elif links_mode == "reverse_cells":
            self.links = {(k, b, a) if (k, a, b) in self.cell_links else (k, a, b) for (k, a, b) in self.links}
        if merge:
            self._merge()
        self.drop = set()
        if drop_same_head:
            self._r15()

    def _counts(self, prov, kind, key, e, variant, claim_atoms):
        if not prov.startswith("attr:"):
            return True
        src = prov[5:]
        if variant == "R9":
            return True
        if variant == "R9r":
            return False
        if self.trust[0] == "all":
            return True
        if self.trust[0] == "list" and src in self.trust[1:]:
            return True
        if variant == "R9m" and kind == "lit" and f"{key}|{e}" in claim_atoms:
            return True
        return False

    def _merge(self):
        ids = sorted(self.ents)
        ren = {}
        for a, b in itertools.combinations(ids, 2):
            if len(a) == len(b) and sum(x != y for x, y in zip(a, b)) <= 2:
                ren[b] = a
        self.ren = ren
        if not ren:
            return

        def R(x):
            return ren.get(x, x)
        f2 = {}
        for a, v in self.facts.items():
            p, e = a.split("|")
            k = f"{p}|{R(e)}"
            if k in f2 and f2[k] != v:
                self.conflict = True
            f2[k] = v
        self.facts = f2
        self.links = {(k, R(a), R(b)) for k, a, b in self.links}
        for name in ("vals", "dates"):
            d2 = {}
            for (e, q), v in getattr(self, name).items():
                k = (R(e), q)
                if k in d2 and d2[k] != v:
                    self.conflict = True
                d2[k] = v
            setattr(self, name, d2)
        self.ents = {e: t for e, t in self.ents.items() if e not in ren}

    def _r15(self):
        for i, r in enumerate(self.rules):
            exc = r[5]
            if not exc:
                continue
            for x in self.subjects(r):
                a = f"{exc}|{x}"
                st = self.facts.get(a)
                off = st is True
                if st is None and self.world == "OW" and self.unless == "strict":
                    closed = any(c[0] == exc and c[1] == self.ents[x] for c in self.closures)
                    off = not closed
                if off:
                    for j, r2 in enumerate(self.rules):
                        if r2[3] == r[3]:
                            self.drop.add((j, x))

    # --- grounding
    def subjects(self, r):
        if self.ground_all:
            return sorted(self.ents)
        return sorted(e for e, t in self.ents.items() if t == r[1])

    def cond_lit(self, c, x):
        """(atom, pos) for a free condition, or a constant bool."""
        if c[0] == "lit":
            return (f"{c[1]}|{x}", c[2])
        if c[0] in ("cmp", "rng"):
            v = self.vals.get((x, c[1]))
        else:
            v = self.dates.get((x, c[1]))
        if v is None:
            if self.missing_false or self.world == "CW":
                return False
            return (f"cond:{json.dumps(c)}|{x}", True)
        opflip = self.opflip if c[0] == "cmp" else ({"<": "<=", "<=": "<", ">": ">=", ">=": ">"}
                                                    if (self.date_flip and c[0] == "dcmp") else None)
        incl = self.range_incl if c[0] == "rng" else ((False, False) if (self.date_flip and c[0] == "win")
                                                      else (True, True))
        return cond_value(c, v, incl, opflip)

    def ground(self):
        """[(rule index, x, body lits, exc atom or None, head lit, kind)] (bodies with a false constant dropped)."""
        out = []
        for i, r in enumerate(self.rules):
            form, typ, conds, head, ante, exc = r[0], r[1], r[2], r[3], r[4], r[5]
            for x in self.subjects(r):
                if (i, x) in self.drop:
                    continue
                hl = (f"{head[0]}|{x}", head[1])

                def body(cs):
                    b = []
                    for c in cs:
                        v = self.cond_lit(c, x)
                        if v is False:
                            return None
                        if v is True:
                            continue
                        b.append(v)
                    return b
                if form in ("univ", "neguniv"):
                    b = body(conds)
                    if b is not None:
                        out.append((i, x, b, f"{exc}|{x}" if exc else None, hl, "body"))
                elif form == "link":
                    for (k, a, y) in sorted(self.links):
                        if k != r[6] or a != x or y not in self.ents:
                            continue
                        if not self.ground_all and self.ents[y] != r[7]:
                            continue
                        out.append((i, x, [(f"{r[8][0]}|{y}", r[8][1])], None, hl, "link"))
                elif form == "onlyif":
                    out.append((i, x, [(f"{ante}|{x}", True)], None, (f"{head[0]}|{x}", True), "onlyif"))
                elif form == "kofn":
                    for S in itertools.combinations(range(len(conds)), r[9]):
                        b = body([conds[j] for j in S])
                        if b is not None:
                            out.append((i, x, b, None, hl, "kofn"))
                elif form == "exactk":
                    n = len(conds)
                    for S in itertools.combinations(range(n), r[9]):
                        b, ok = [], True
                        for j in range(n):
                            v = self.cond_lit(conds[j], x)
                            want = j in S
                            if isinstance(v, bool):
                                if v != want:
                                    ok = False
                                    break
                                continue
                            b.append(v if want else (v[0], not v[1]))
                        if ok:
                            out.append((i, x, b, None, hl, "exactk"))
                elif form == "or":
                    for c in conds:
                        b = body([c])
                        if b is not None:
                            out.append((i, x, b, None, hl, "or"))
                elif form in ("xor", "xorboth"):
                    a_, b_ = conds
                    pairs = [(a_, b_), (b_, a_)] if form == "xor" else [(a_, b_)]
                    for p, q in pairs:
                        vp, vq = self.cond_lit(p, x), self.cond_lit(q, x)
                        if form == "xor":
                            if vp is False or vq is True:
                                continue
                            b = ([] if vp is True else [vp]) + ([] if vq is False else [(vq[0], not vq[1])])
                        else:
                            if vp is False or vq is False:
                                continue
                            b = ([] if vp is True else [vp]) + ([] if vq is True else [vq])
                        out.append((i, x, b, None, hl, form))
                else:
                    raise ValueError(form)
        return out

    # --- fixed atoms (units) for OW
    def fixed_ow(self):
        fx = dict(self.facts)
        for c in self.closures:
            p, t = c[0], c[1]
            for e, te in self.ents.items():
                if te == t and f"{p}|{e}" not in self.facts:
                    fx[f"{p}|{e}"] = False
        if self.unless == "listc":
            for r in self.rules:
                if r[5]:
                    for e in self.ents:
                        a = f"{r[5]}|{e}"
                        if a not in self.facts:
                            fx.setdefault(a, False)
        if self.missing_false:
            for a in self.markers:
                fx.setdefault(a, False)
        return fx


# ======================================================================================================= enumeration

def formulas_ow(rd: Reading):
    """OW formulas: ('cl', lits) for each ground rule instance (not body v C v head) plus rd.extra formulas."""
    fs = []
    for (i, x, b, exc, h, kind) in rd.ground():
        lits = [(a, not p) for a, p in b]
        if exc:
            lits.append((exc, True))
        lits.append(h)
        fs.append(("cl", lits))
    fs.extend(rd.extra)
    return fs


def f_atoms(f):
    if f[0] == "cl":
        return {a for a, _ in f[1]}
    if f[0] == "imp":
        return {f[1][0]} | {a for conj in f[2] for a, _ in conj}
    if f[0] == "orand":
        return {a for conj in f[1] for a, _ in conj}
    raise ValueError(f[0])


def enum_sat(fixed: dict, formulas: list, atom, value):
    """Is there a model of the formulas (with fixed atoms) in which `atom` has `value`? Brute force over the free
    atoms of the formulas connected to `atom` through free atoms."""
    fx = dict(fixed)
    if atom in fx:
        if fx[atom] != value:
            return False
    else:
        fx[atom] = value
    # connected component over free atoms
    by_atom = {}
    for i, f in enumerate(formulas):
        for a in f_atoms(f):
            by_atom.setdefault(a, []).append(i)
    comp, seen = set(), {atom}
    stack = [atom]
    while stack:
        a = stack.pop()
        for i in by_atom.get(a, ()):
            if i in comp:
                continue
            comp.add(i)
            for b in f_atoms(formulas[i]):
                if b not in seen and b not in fx:
                    seen.add(b)
                    stack.append(b)
    # formulas with only fixed atoms are checked too (a fixed-only false formula means no model at all)
    fs = [formulas[i] for i in sorted(comp)]
    # pure-literal elimination (satisfiability-preserving): a free atom that occurs in one polarity only, and only
    # in clauses, is set to that polarity and its clauses dropped (the queried atom is never eliminated)
    while True:
        pol = {}
        other = set()
        for f in fs:
            if f[0] == "cl":
                for a, p in f[1]:
                    if a not in fx:
                        pol.setdefault(a, set()).add(p)
            else:
                other |= f_atoms(f)
        pure = {a: next(iter(ps)) for a, ps in pol.items() if len(ps) == 1 and a not in other and a != atom}
        if not pure:
            break
        fx.update(pure)
        fs = [f for f in fs if not (f[0] == "cl" and any(a in pure and pure[a] == p for a, p in f[1]))]
    free = sorted({a for f in fs for a in f_atoms(f) if a not in fx})
    if len(free) > MAX_FREE:
        raise Budget(len(free))
    n = len(free)
    idx = {a: j for j, a in enumerate(free)}
    N = 1 << n
    cols = ((np.arange(N, dtype=np.int64)[:, None] >> np.arange(n, dtype=np.int64)[None, :]) & 1).astype(bool) \
        if n else np.zeros((1, 0), dtype=bool)

    def litv(a, p):
        if a in fx:
            return np.full(cols.shape[0], fx[a] == p)
        c = cols[:, idx[a]]
        return c if p else ~c
    ok = np.ones(cols.shape[0], dtype=bool)
    for f in fs:
        if f[0] == "cl":
            v = np.zeros(cols.shape[0], dtype=bool)
            for a, p in f[1]:
                v |= litv(a, p)
        elif f[0] == "imp":
            h = litv(*f[1])
            dis = np.zeros(cols.shape[0], dtype=bool)
            for conj in f[2]:
                cv = np.ones(cols.shape[0], dtype=bool)
                for a, p in conj:
                    cv &= litv(a, p)
                dis |= cv
            v = (~h) | dis
        else:
            dis = np.zeros(cols.shape[0], dtype=bool)
            for conj in f[1]:
                cv = np.ones(cols.shape[0], dtype=bool)
                for a, p in conj:
                    cv &= litv(a, p)
                dis |= cv
            v = dis
        ok &= v
        if not ok.any():
            return False
    return bool(ok.any())


def any_model(fixed, formulas):
    """Is the whole theory satisfiable? (component by component)"""
    by_atom = {}
    for i, f in enumerate(formulas):
        for a in f_atoms(f):
            if a not in fixed:
                by_atom.setdefault(a, []).append(i)
    done = set()
    for i, f in enumerate(formulas):
        if i in done:
            continue
        # pick an atom of the formula (or check fixed-only formulas directly)
        fa = [a for a in f_atoms(f) if a not in fixed]
        if not fa:
            if not formula_value_fixed(f, fixed):
                return False
            done.add(i)
            continue
        a = fa[0]
        if not (enum_sat(fixed, formulas, a, True) or enum_sat(fixed, formulas, a, False)):
            return False
        # mark the component as done
        stack, seen = [a], {a}
        while stack:
            b = stack.pop()
            for j in by_atom.get(b, ()):
                if j not in done:
                    done.add(j)
                    for c in f_atoms(formulas[j]):
                        if c not in fixed and c not in seen:
                            seen.add(c)
                            stack.append(c)
    return True


def formula_value_fixed(f, fx):
    if f[0] == "cl":
        return any(fx[a] == p for a, p in f[1])
    if f[0] == "imp":
        h = fx[f[1][0]] == f[1][1]
        return (not h) or any(all(fx[a] == p for a, p in c) for c in f[2])
    return any(all(fx[a] == p for a, p in c) for c in f[1])


def label_ow(rd: Reading, claim_atom, claim_pos):
    if rd.conflict:
        return "X"
    fx = rd.fixed_ow()
    fs = formulas_ow(rd)
    if not any_model(fx, fs):
        return "X"
    can_true = enum_sat(fx, fs, claim_atom, claim_pos)
    can_false = enum_sat(fx, fs, claim_atom, not claim_pos)
    if not can_true and not can_false:
        return "X"
    if not can_false:
        return "F"
    if not can_true:
        return "R"
    return "O"


# ------------------------------------------------------------------------------------------------------- CW (Clark)

def clark_model(rd: Reading, *, extra_facts=None):
    """The unique assignment satisfying Clark's completion of the ground program, or None (no model). Enumerates
    each component of derived atoms separately. Returns (true atom set, instances). Cached per reading."""
    if not extra_facts:
        if getattr(rd, "_clark", None) is None:
            rd._clark = _clark_model(rd)
        return rd._clark
    return _clark_model(rd, extra_facts=extra_facts)


def _clark_model(rd: Reading, *, extra_facts=None):
    facts = dict(rd.facts)
    if extra_facts:
        facts.update(extra_facts)
    inst = rd.ground()
    pos_heads = {}
    neg_inst = []
    for it in inst:
        (i, x, b, exc, h, kind) = it
        if rd.rules[i][0] == "onlyif":
            continue
        if h[1]:
            pos_heads.setdefault(h[0], []).append(it)
        else:
            neg_inst.append(it)
    derived = set(pos_heads)
    stated_true = {a for a, v in facts.items() if v}

    def exc_state(exc):
        if exc is None:
            return False
        if rd.cw_mode == "strict":
            if facts.get(exc) is True:
                return True
            if facts.get(exc) is False:
                return False
            return None
        return facts.get(exc) is True
    # components of derived atoms
    parent = {a: a for a in derived}

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    for a, its in pos_heads.items():
        for (i, x, b, exc, h, kind) in its:
            for c, _ in b:
                if c in derived:
                    union(a, c)
    if rd.cw_mode == "conj":
        pass
    for (i, x, b, exc, h, kind) in neg_inst:
        ds = [c for c, _ in b if c in derived] + ([h[0]] if h[0] in derived else [])
        for c in ds[1:]:
            union(ds[0], c)
    comps = {}
    for a in derived:
        comps.setdefault(find(a), []).append(a)
    true_atoms = {a for a in stated_true if a not in derived}
    for comp in comps.values():
        comp = sorted(comp)
        n = len(comp)
        if n > MAX_FREE:
            raise Budget(n)
        idx = {a: j for j, a in enumerate(comp)}
        N = 1 << n
        cols = ((np.arange(N, dtype=np.int64)[:, None] >> np.arange(n, dtype=np.int64)[None, :]) & 1).astype(bool)

        def val(a):
            if a.startswith("cond:"):
                raise ValueError("free condition in CW")
            if a in idx:
                return cols[:, idx[a]]
            if a in derived:
                raise ValueError("component leak")
            return np.full(N, a in stated_true)

        def body_val(b):
            v = np.ones(N, dtype=bool)
            for a, p in b:
                x = val(a)
                v &= x if p else ~x
            return v
        ok = np.ones(N, dtype=bool)
        for a in comp:
            its = pos_heads[a]
            if rd.cw_mode == "conj":
                p_, x_ = a.split("|")
                by_rule = {}
                for (i, x, b, exc, h, kind) in its:
                    bv = body_val(b) if exc_state(exc) is False else np.zeros(N, dtype=bool)
                    by_rule[i] = by_rule.get(i, np.zeros(N, dtype=bool)) | bv
                rules_for = [i for i, r in enumerate(rd.rules) if r[0] != "onlyif" and list(r[3]) == [p_, True]
                             and (rd.ground_all or rd.ents.get(x_) == r[1]) and (i, x_) not in rd.drop]
                rhs = np.ones(N, dtype=bool) if rules_for else np.zeros(N, dtype=bool)
                for i in rules_for:
                    rhs &= by_rule.get(i, np.zeros(N, dtype=bool))
            else:
                rhs = np.zeros(N, dtype=bool)
                for (i, x, b, exc, h, kind) in its:
                    if exc_state(exc) is not False:
                        continue
                    rhs |= body_val(b)
            rhs |= (a in stated_true)
            ok &= (val(a) == rhs)
        for a in comp:
            if facts.get(a) is False:
                ok &= ~val(a)
        for (i, x, b, exc, h, kind) in neg_inst:
            atoms = [c for c, _ in b] + [h[0]]
            if not any(c in idx for c in atoms):
                continue
            if exc_state(exc) is not False:
                continue
            ok &= ~(body_val(b) & val(h[0]))
        rows = np.nonzero(ok)[0]
        if len(rows) == 0:
            return None, inst
        if len(rows) > 1:
            raise ValueError("Clark completion has several models (cyclic program)")
        r0 = rows[0]
        true_atoms |= {a for a in comp if cols[r0, idx[a]]}
    # constraints with no derived atom
    for a, v in facts.items():
        if v is False and a not in derived and a in stated_true:
            return None, inst
    for (i, x, b, exc, h, kind) in neg_inst:
        atoms = [c for c, _ in b] + [h[0]]
        if any(c in derived for c in atoms) or exc_state(exc) is not False:
            continue
        if all((c in stated_true) == p for c, p in b) and h[0] in stated_true:
            return None, inst
    return true_atoms, inst


def cw_truth(rd, M, atom):
    if "|" in atom and atom.count("|") == 1:
        return atom in M
    return atom in M


def label_cw(rd: Reading, claim_atom, claim_pos):
    if rd.conflict:
        return "X"
    M, _ = clark_model(rd)
    if M is None:
        return "X"
    return "F" if (claim_atom in M) == claim_pos else "R"


# ======================================================================================================= readings

def card_reading_args(cn):
    f = cn["flags"]
    world = "OW" if f["world"] in ("OW", "unspecified") else "CW"
    unless = f["unless"]
    if unless in ("none", "unspecified"):
        unless = "strict" if world == "OW" else "cw"
    trust = f["trust"] if f["trust"][0] != "unspecified" else ["all"]
    return world, unless, trust


def label(rd: Reading, cl):
    a, p = cl
    if rd.world == "CW":
        return label_cw(rd, a, p)
    return label_ow(rd, a, p)


def labels(rd: Reading, claims: dict):
    """label() for many claims with one model check (OW) or one Clark model (CW)."""
    if rd.conflict:
        return {k: "X" for k in claims}
    if rd.world == "CW":
        M, _ = clark_model(rd)
        if M is None:
            return {k: "X" for k in claims}
        return {k: ("F" if (a in M) == p else "R") for k, (a, p) in claims.items()}
    fx = rd.fixed_ow()
    fs = formulas_ow(rd)
    if not any_model(fx, fs):
        return {k: "X" for k in claims}
    out = {}
    for k, (a, p) in claims.items():
        t = enum_sat(fx, fs, a, p)
        f = enum_sat(fx, fs, a, not p)
        out[k] = "X" if not t and not f else ("F" if not f else ("R" if not t else "O"))
    return out


def tseitin_free_imp(rd: Reading):
    """R3 (OW): for every rule r and subject x: h(x) -> OR of r's ground bodies (exception literal included)."""
    by = {}
    for (i, x, b, exc, h, kind) in rd.ground():
        r = rd.rules[i]
        if r[0] == "onlyif":
            continue
        by.setdefault((i, x), []).append(list(b) + ([(exc, False)] if exc else []))
    out = []
    for i, r in enumerate(rd.rules):
        for x in rd.subjects(r):
            if (i, x) in rd.drop:
                continue
            if r[0] == "onlyif":
                out.append(("imp", (f"{r[3][0]}|{x}", True), [[(f"{r[4]}|{x}", True)]]))
                continue
            out.append(("imp", (f"{r[3][0]}|{x}", r[3][1]), by.get((i, x), [])))
    return out


def r6_formulas(rd: Reading):
    out = []
    for kind, t, c, h in rd.cn["hedges"]:
        es = [e for e, te in rd.ents.items() if te == t]
        conj = []
        for e in es:
            hv = h[1] if kind != "notevery" else (not h[1])
            conj.append([(f"{c[0]}|{e}", c[1]), (f"{h[0]}|{e}", hv)])
        out.append(("orand", conj))
    return out


def forward_b(rd: Reading, cl, contra_mode):
    """Forward rule application (R2: none; R22: contrapositives of positive-head universal, or, either-or and
    only-if rules), with B's own fixpoint over rule instances. Converse (R3 combined) adds h -> body when a rule has
    one ground body for x."""
    known = dict(rd.fixed_ow())
    inst = rd.ground()
    conv = []
    if contra_mode and contra_mode.endswith("+R3"):
        cnt = {}
        for it in inst:
            cnt[(it[0], it[1])] = cnt.get((it[0], it[1]), 0) + 1
        for (i, x, b, exc, h, kind) in inst:
            if rd.rules[i][0] == "onlyif" or cnt[(i, x)] != 1:
                continue
            for lit in b:
                conv.append((h, lit))
            if exc:
                conv.append((h, (exc, False)))
    base_mode = contra_mode.split("+")[0] if contra_mode else None
    changed = True
    while changed:
        changed = False
        for (i, x, b, exc, h, kind) in inst:
            r = rd.rules[i]
            body = list(b) + ([(exc, False)] if exc else [])
            if all(known.get(a) == p for a, p in body):
                if known.get(h[0]) is None:
                    known[h[0]] = h[1]
                    changed = True
                elif known[h[0]] != h[1]:
                    return "X"
            if base_mode == "R22":
                ok_rule = (r[0] == "univ" and r[3][1]) or r[0] in ("or", "xor", "onlyif")
                if not ok_rule or known.get(h[0]) != (not h[1]):
                    continue
                for j, (a, p) in enumerate(b):
                    others = [l for k, l in enumerate(b) if k != j] + ([(exc, False)] if exc else [])
                    if all(known.get(oa) == op for oa, op in others):
                        if known.get(a) is None:
                            known[a] = not p
                            changed = True
                        elif known[a] != (not p):
                            return "X"
        for (h, lit) in conv:
            if known.get(h[0]) == h[1]:
                if known.get(lit[0]) is None:
                    known[lit[0]] = lit[1]
                    changed = True
                elif known[lit[0]] != lit[1]:
                    return "X"
    v = known.get(cl[0])
    if v is None:
        return "O"
    return "F" if v == cl[1] else "R"


def r24_b(rd: Reading, cl):
    M, inst = clark_model(rd)
    if M is None:
        return "X"
    a, p = cl
    if p:
        return "F" if a in M else "R"
    if rd.facts.get(a) is False:
        return "F"
    for (i, x, b, exc, h, kind) in inst:
        if h[0] != a or h[1] or rd.rules[i][0] == "onlyif":
            continue
        if exc and rd.facts.get(exc) is True:
            continue
        if all((c in M) == pp for c, pp in b):
            return "F"
    return "R"


def r30_b(rd: Reading, claims: dict, strict_only: bool):
    M, inst = clark_model(rd)
    if M is None:
        return {k: "X" for k in claims}
    stated_true = {a for a, v in rd.facts.items() if v}
    results = [(a, True) for a in sorted(M)] + [(a, False) for a, v in sorted(rd.facts.items()) if v is False]
    choices = []
    for (a, pol) in results:
        p_, x = a.split("|")
        rules_for = [i for i, r in enumerate(rd.rules) if r[0] != "onlyif" and list(r[3]) == [p_, pol]
                     and (rd.ground_all or rd.ents.get(x) == r[1]) and (i, x) not in rd.drop]
        if not rules_for:
            continue
        bodies_by_rule = {i: [] for i in rules_for}
        for (i, xx, b, exc, h, kind) in inst:
            if i in bodies_by_rule and xx == x:
                bodies_by_rule[i].append((tuple(b), exc))
        if strict_only:
            holds = False
            if pol:
                for i in rules_for:
                    for b, exc in bodies_by_rule[i]:
                        if exc and exc in stated_true:
                            continue
                        if all((c in M) == pp for c, pp in b):
                            holds = True
            if holds or (pol and a not in stated_true):
                continue
            choices.append([bb for i in rules_for for bb in bodies_by_rule[i]])
        else:
            for i in rules_for:
                choices.append(bodies_by_rule[i])
    total = 1
    for c in choices:
        total *= max(1, len(c))
        if total > 2 ** 16:
            return "BUDGET"
    if any(len(c) == 0 for c in choices):
        return {k: "X" for k in claims}
    seen = {k: set() for k in claims}
    anyw = False
    for pick in itertools.product(*choices) if choices else [()]:
        add, negreq, bad = {}, set(), False
        for b, exc in pick:
            for c, pp in b:
                if c.startswith("cond:"):
                    bad = True
                elif pp:
                    if rd.facts.get(c) is False:
                        bad = True
                    add[c] = True
                else:
                    negreq.add(c)
            if exc:
                negreq.add(exc)
        if bad:
            continue
        M2, _ = clark_model(rd, extra_facts=add)
        if M2 is None or any(c in M2 for c in negreq):
            continue
        anyw = True
        for k, (a, p) in claims.items():
            seen[k].add((a in M2) == p)
    out = {}
    for k in claims:
        if not anyw:
            out[k] = "X"
        elif seen[k] == {True}:
            out[k] = "F"
        elif seen[k] == {False}:
            out[k] = "R"
        else:
            out[k] = "O"
    return out


def rival_reading(cn, rv, claim_atoms):
    W, U, T = card_reading_args(cn)
    kw = dict(world=W, unless=U, trust=T)
    rules = cn["rules"]
    if rv == "R1":
        if W == "OW":
            return Reading(cn, world="CW", unless="cw", trust=T, missing_false=True)
        return Reading(cn, world="OW", unless="strict", trust=T)
    if rv == "R3":
        if W == "CW":
            return Reading(cn, cw_mode="conj", **kw)
        rd = Reading(cn, **kw)
        rd.extra = tseitin_free_imp(rd)
        return rd
    if rv == "R4":
        add = [["univ", r[1], [["lit", r[5], True]], [r[3][0], not r[3][1]], None, None, None, None, None, 0,
                "record"] for r in rules if r[5]]
        return Reading(cn, rules=list(rules) + add, **kw)
    if rv == "R5":
        if W == "OW":
            return Reading(cn, world="OW", unless={"strict": "listc", "listc": "strict"}.get(U, U), trust=T)
        return Reading(cn, cw_mode="strict", **kw)
    if rv == "R6":
        rd = Reading(cn, **kw)
        if W == "OW" and cn["hedges"]:
            rd.extra = r6_formulas(rd)
        return rd
    if rv == "R7":
        return Reading(cn, rules=[["xor"] + list(r[1:]) if r[0] == "or" else r for r in rules], **kw)
    if rv == "R8n":
        return Reading(cn, range_incl=(False, False), **kw)
    if rv == "R8d":
        return Reading(cn, date_flip=True, **kw)
    if rv in ("R9", "R9r", "R9m", "R20"):
        return Reading(cn, fact_variant=rv, claim_atoms=claim_atoms, **kw)
    if rv == "R10":
        return Reading(cn, missing_false=True, **kw)
    if rv == "R11":
        return Reading(cn, hedge_rules=True, ehedge_facts=True, **kw)
    if rv == "R12":
        return Reading(cn, rules=[["univ", r[1], [["lit", r[3][0], True]], [r[4], True], None, None, None, None,
                                   None, 0, r[10]] if r[0] == "onlyif" else r for r in rules], **kw)
    if rv == "R13a":
        return Reading(cn, opflip={">": ">=", "<": "<="}, **kw)
    if rv == "R13b":
        return Reading(cn, opflip={">=": ">", "<=": "<"}, **kw)
    if rv == "R14":
        return Reading(cn, rules=[["exactk"] + list(r[1:]) if r[0] == "kofn" else r for r in rules], **kw)
    if rv == "R15":
        return Reading(cn, drop_same_head=True, **kw)
    if rv == "R16":
        return Reading(cn, merge=True, **kw)
    if rv == "R18":
        add = [["xorboth", r[1], r[2], [r[3][0], False]] + list(r[4:]) for r in rules if r[0] == "xor"]
        return Reading(cn, rules=list(rules) + add, **kw)
    if rv == "R23":
        return Reading(cn, closures=[], **kw)
    if rv == "R26":
        types = sorted({t for _, t in cn["ents"]})
        return Reading(cn, closures=[[c[0], t, c[2]] for c in cn["closures"] for t in types], **kw)
    if rv == "R27":
        return Reading(cn, links_mode="sym_trans", **kw)
    if rv == "R28":
        return Reading(cn, rules=[r for r in rules if r[10] != "card"], **kw)
    if rv == "R29":
        return Reading(cn, links_mode="reverse_cells", **kw)
    if rv == "R31":
        return Reading(cn, ground_all=True, **kw)
    if rv == "R21":
        rd = Reading(cn, **kw)
        if W == "OW":
            ext = []
            rd2 = Reading(cn, ground_all=True, **kw)
            for (i, x, b, exc, h, kind) in rd2.ground():
                r = rd.rules[i]
                if rd.ents.get(x) == r[1]:
                    continue
                lits = [(a, not p) for a, p in b] + ([(exc, True)] if exc else []) + [h, (f"member:{r[1]}|{x}",
                                                                                         False)]
                ext.append(("cl", lits))
            rd.extra = ext
        return rd
    return Reading(cn, **kw)


RIVALS_B = ("R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8n", "R8d", "R9", "R9r", "R9m", "R10", "R11", "R12",
            "R13a", "R13b", "R14", "R15", "R16", "R17", "R18", "R19", "R20", "R21", "R22", "R23", "R24", "R25",
            "R26", "R27", "R28", "R29", "R30", "R30s", "R31")


def claims_of(cn):
    f = cn["form"]
    if f == "CH-claim":
        return {i: (f"{o[0]}|{o[1]}", o[2]) for i, o in enumerate(cn["options"]) if o is not None}
    if f == "CH-entity":
        return {i: (f"{cn['H']}|{e}", True) for i, e in enumerate(cn["options"])}
    p, e, pos = cn["claim"]
    return {"c": (f"{p}|{e}", pos)}


def b_answer(form, labs, *, r25=False, none_shown=False):
    """Answer mapping (7.2), B's own table."""
    yes_on = {"YN-F": {"F"}, "YN-dn": {"F"}, "YN-T": {"F"}, "YN-R": {"R"}, "YN-O": {"O"},
              "YN-nF": {"R", "O"}, "YN-nR": {"F", "O"}}
    if form in yes_on:
        lab = labs["c"]
        if lab not in ("F", "R", "O"):
            return "PIVOT"
        return "yes" if lab in yes_on["YN-F" if r25 else form] else "no"
    if form == "CH-3":
        lab = labs["c"]
        return lab if lab in ("F", "R", "O") else "PIVOT"
    if form == "CH-2":
        lab = labs["c"]
        return lab if lab in ("F", "R") else "PIVOT"
    if any(v not in ("F", "R", "O") for v in labs.values()):
        return "PIVOT"
    q = [k for k, v in sorted(labs.items(), key=lambda kv: str(kv[0])) if v == "F"]
    if form == "CH-claim" and not q:
        return "NONE" if none_shown else "PIVOT"
    return q[0] if len(q) == 1 else "PIVOT"


def solve(cn):
    """Solver B on the parsed canonical structure: labels, gold answer, pivots (with tags), short-card pairs."""
    W, U, T = card_reading_args(cn)
    claims = claims_of(cn)
    atoms = tuple(a for a, _ in claims.values())
    base = Reading(cn, world=W, unless=U, trust=T)
    labs = labels(base, claims)
    form = cn["form"]
    gold = b_answer(form, labs, none_shown=cn["none_shown"])
    answers = {}
    cache = {}
    for rv in RIVALS_B:
        if rv == "R2":
            lab = {k: forward_b(base, cl, None) for k, cl in claims.items()} if W == "OW" else labs
        elif rv == "R22":
            lab = {k: forward_b(base, cl, "R22") for k, cl in claims.items()} if W == "OW" else labs
        elif rv == "R19":
            lab = {}
            for k, (a, p) in claims.items():
                v = base.facts.get(a)
                lab[k] = "O" if v is None else ("F" if v == p else "R")
        elif rv == "R24":
            lab = {k: r24_b(base, cl) for k, cl in claims.items()} if W == "CW" else labs
        elif rv in ("R30", "R30s"):
            lab = r30_b(base, claims, rv == "R30s") if W == "CW" else labs
            if lab == "BUDGET":
                return {"ok": False, "why": "r30_budget"}
        elif rv in ("R25", "R17"):
            lab = labs
        elif rv == "R16":
            rd = rival_reading(cn, rv, atoms)
            ren = getattr(rd, "ren", {})
            cl2 = {}
            for k, (a, p) in claims.items():
                pr, e = a.split("|")
                cl2[k] = (f"{pr}|{ren.get(e, e)}", p)
            lab = labels(rd, cl2)
        else:
            rd = rival_reading(cn, rv, atoms)
            lab = labels(rd, claims)
        answers[rv] = b_answer(form, lab, r25=(rv == "R25"), none_shown=cn["none_shown"])
    piv = sorted({ {"R9r": "R9", "R9m": "R9", "R13a": "R13", "R13b": "R13", "R30s": "R30"}.get(r, r)
                  for r, a in answers.items() if a != gold})
    out = {"ok": True, "labels": {str(k): v for k, v in labs.items()}, "gold": gold, "pivots": piv,
           "answers": {k: str(v) for k, v in answers.items()}}
    if cn["flags"]["world"] == "unspecified":
        out["pairs"] = short_pairs_b(cn, claims, form)
    return out


def short_pairs_b(cn, claims, form):
    W, U, T = card_reading_args(cn)
    cw = Reading(cn, world="CW", unless="cw", trust=T, missing_false=True)
    cwc = Reading(cn, world="CW", unless="cw", trust=T, missing_false=True, cw_mode="conj")
    ow = Reading(cn, world="OW", unless="strict", trust=T)
    out = {}
    lc = labels(cw, claims)
    for k in ("R1+R2", "R1+R22", "R1+R17"):
        out[k] = lc
    out["R1+R3"] = labels(cwc, claims)
    out["R1+R24"] = {k: r24_b(cw, cl) for k, cl in claims.items()}
    r = r30_b(cw, claims, False)
    out["R1+R30"] = r if r != "BUDGET" else {k: "BUDGETX" for k in claims}
    fw = {k: forward_b(ow, cl, None) for k, cl in claims.items()}
    out["R2+R17"] = fw
    out["R2+R22"] = fw
    out["R22+R17"] = {k: forward_b(ow, cl, "R22") for k, cl in claims.items()}
    ow3 = Reading(cn, world="OW", unless="strict", trust=T)
    ow3.extra = tseitin_free_imp(ow3)
    out["R3+R17"] = labels(ow3, claims)
    out["R2+R3"] = {k: forward_b(ow, cl, "R2+R3") for k, cl in claims.items()}
    out["R22+R3"] = {k: forward_b(ow, cl, "R22+R3") for k, cl in claims.items()}
    return {k: b_answer(form, v, none_shown=cn["none_shown"]) for k, v in out.items()}

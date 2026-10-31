"""F4 samplers (G0 spec section 5): build a sampled record for a target cell (world, form, label, depth, claim
polarity, inference tags, features), so no row is ever relabelled. Solver A (solve_a.analyze) validates every row;
a failed row is resampled and the reason counted.

Shapes: S1 forward (fact graph first, prose), S2 label-first deduction with FLD-style distractors (lists), S3 evidence
tables (table first), S4 attributed statements (statement first), S5 held-out narrative (dev and depth sweep only).
All share one vocabulary and one chain grammar (2.1), so the samplers differ in the order of construction, the
distractor style and the container, as 5.1-5.5 say.
"""
from __future__ import annotations

import datetime as dt
import itertools
import random
from dataclasses import dataclass, field
from decimal import Decimal

import core as C
import f4lex as L
import packs_f4 as P

# ------------------------------------------------------------------------------------------------------- card plan


@dataclass
class CardPlan:
    card_id: str
    sampler: str              # S1..S5
    pack: dict
    world: str                # OW | CW | None (short)
    short: bool
    inverted: bool
    types: list               # [(sg, pl)] card types
    umbrella: tuple
    feats: set                # features in the card plan (7.1 table)
    unless: str               # strict | listc | cw | none | None
    trust: tuple              # ("list", names) | ("all",) | None
    links: list               # [{"active","passive","from","to"}] with from/to as card type indexes
    qtys: list                # [{"name","unit","lo","hi","dec","type"}] (type = card type index)
    dattrs: list              # [(name, card type index)]
    window: tuple             # (date lo, date hi)
    sources: tuple            # (trusted names, untrusted names) in the card's source map
    preds: list               # predicate words for this card
    ids: list                 # entity id pool
    looks: list               # marked look-alike pairs from the pool
    forms: dict               # form -> share of the card's rows
    yes_rate: float
    defs_style: str
    fewshot: bool
    wording_family: str
    styles: list              # format style ids for rows of this card
    label_names: dict = field(default_factory=dict)   # CH-3 / CH-2 option set, mask scheme, swap words
    attack_clause: bool = False
    standing: bool = False
    clause_set: frozenset = frozenset()
    example_kinds: tuple = ()
    persona_tpl: int = 0


def date_of(s):
    y, m, d = (int(x) for x in s.split("-"))
    return dt.date(y, m, d)


# ------------------------------------------------------------------------------------------------------- builder

class Fail(Exception):
    pass


class RB:
    """Record builder over one card plan."""

    def __init__(self, cp: CardPlan, rng: random.Random):
        self.cp, self.r = cp, rng
        self.ents = {}            # id -> type idx
        self.preds = {}           # pred -> type idx
        self.role = {}            # pred -> base | derived | exc
        self.rules = []
        self.stmts = []
        self.vals = {}            # (e, q) -> Decimal | None (marker)
        self.dates = {}
        self.links = set()        # (li, a, b)
        self.closures = []        # (pred, typ, form, tid)
        self.hedges, self.ehedges = [], []
        self.lookalikes = []
        self.qty_used = set()     # quantities already read by a rule condition (one condition per quantity)
        self.date_used = set()
        self.exc_preds = set()
        self.near_miss = []       # failing premises (atom, value)
        self.notes = {}           # sampler notes (decisive premises etc.)
        self._ids = list(cp.ids)
        rng.shuffle(self._ids)
        self._preds = list(cp.preds)
        rng.shuffle(self._preds)
        self._sid = 0
        self._rid = 0
        self.no_fact = set()      # atoms that must stay unstated (failing premises, claim atoms)
        self.blank_cells = []     # (pred, e, tid) blank cells of closed columns

    # --- vocabulary
    def ent(self, typ, avoid_looks=True):
        while self._ids:
            e = self._ids.pop()
            if avoid_looks and any(e in p for p in self.cp.looks):
                continue
            self.ents[e] = typ
            return e
        raise Fail("ids")

    def look_pair(self, typ):
        for a, b in self.cp.looks:
            if a not in self.ents and b not in self.ents and a in self._ids and b in self._ids:
                self._ids.remove(a)
                self._ids.remove(b)
                self.ents[a] = typ
                self.ents[b] = typ
                self.lookalikes.append((a, b))
                return a, b
        raise Fail("looks")

    def pred(self, typ, role="base"):
        if not self._preds:
            raise Fail("preds")
        p = self._preds.pop()
        self.preds[p] = typ
        self.role[p] = role
        if role == "exc":
            self.exc_preds.add(p)
        return p

    def sid(self):
        self._sid += 1
        return f"s{self._sid}"

    def rid(self):
        self._rid += 1
        return f"r{self._rid}"

    # --- statements
    def fact(self, e, p, pos, *, via="sent", src=None, frame=None, tag=None):
        a = C.u(p, e)
        if a in self.no_fact:
            raise Fail("no_fact")
        for s in self.stmts:
            if s.kind == "lit" and s.e == e and s.pred == p and s.pos is not None and s.src is None:
                if s.pos != pos:
                    raise Fail("fact_conflict")
                return s
        s = C.Stmt(sid=self.sid(), kind="lit", e=e, pred=p, pos=pos, via=via, src=src, frame=frame, tag=tag)
        self.stmts.append(s)
        return s

    def marker(self, e, p):
        s = C.Stmt(sid=self.sid(), kind="lit", e=e, pred=p, pos=None, via="cell")
        self.stmts.append(s)
        return s

    def value(self, e, q, v, *, via="sent", src=None, frame=None):
        self.vals[(e, q)] = v
        s = C.Stmt(sid=self.sid(), kind="val", e=e, pred=q, value=v, via=via, src=src, frame=frame)
        self.stmts.append(s)
        return s

    def date(self, e, a, d, *, via="sent", src=None, frame=None):
        self.dates[(e, a)] = d
        s = C.Stmt(sid=self.sid(), kind="date", e=e, pred=a, value=d, via=via, src=src, frame=frame)
        self.stmts.append(s)
        return s

    def link(self, li, a, b, *, via="sent"):
        if a == b:
            raise Fail("self_link")
        self.links.add((li, a, b))
        s = C.Stmt(sid=self.sid(), kind="link", e=a, pred=li, value=b, via=via)
        self.stmts.append(s)
        return s

    def rule(self, **kw):
        r = C.Rule(rid=self.rid(), **kw)
        if r.head:
            hp = r.head[0]
            if self.role.get(hp) == "exc":
                raise Fail("exc_head")
            if self.role.get(hp) == "base" and hp in self.preds:
                self.role[hp] = "derived"
        if r.form == "onlyif" and r.ante and self.role.get(r.ante) == "base":
            pass
        self.rules.append(r)
        return r

    # --- conditions with values (cost 0)
    def qty_cond(self, x, want: bool, boundary: bool, kind=None):
        """A comparison or range condition on x that holds (want True) or fails (want False); sets x's value."""
        typ = self.ents[x]
        qs = [q for q in self.cp.qtys if q["name"] not in self.qty_used and q["type"] in (None, typ)]
        if not qs:
            raise Fail("no_qty")
        q = self.r.choice(qs)
        self.qty_used.add(q["name"])
        dec = q["dec"]
        step = Decimal(1).scaleb(-dec)
        lo, hi = Decimal(str(q["lo"])), Decimal(str(q["hi"]))
        span = hi - lo
        T = (lo + span * Decimal(str(self.r.uniform(0.25, 0.75)))).quantize(step)
        if kind is None:
            if "cmp" not in self.cp.feats:
                kind = "rng"
            else:
                kind = "rng" if ("rng" in self.cp.feats and self.r.random() < 0.3) else "cmp"
        if kind == "rng":
            w = (span * Decimal(str(self.r.uniform(0.1, 0.3)))).quantize(step)
            if w <= step * 2:
                w = step * 3
            T1, T2 = T - w, T + w
            if lo >= 0 and T1 < lo:
                T1 = lo   # thresholds stay inside the pack's range (no negative values)
            if boundary:
                v = T1 if self.r.random() < 0.5 else T2
                if not want:
                    v = T1 - step if v == T1 else T2 + step
            else:
                inside = (T1 + step * self.r.randint(1, int((T2 - T1) / step) - 1)).quantize(step)
                v = inside if want else (T2 + step * self.r.randint(1, 5))
            cond = ("rng", q["name"], T1, T2)
        else:
            op = self.r.choice((">=", ">", "<=", "<"))
            if boundary:
                if op in (">=", "<="):
                    v = T if want else (T - step if op == ">=" else T + step)
                else:
                    v = T if not want else (T + step if op == ">" else T - step)
            else:
                d = step * self.r.randint(2, 12)
                above = T + d
                below = T - d
                holds_above = op in (">=", ">")
                v = (above if holds_above else below) if want else (below if holds_above else above)
            cond = ("cmp", q["name"], op, T)
        if v < lo or v > hi:
            v = max(lo, min(hi, v))
            ok = _eval_cond(cond, v)
            if ok != want:
                raise Fail("qty_range")
        return cond, q["name"], v

    def date_cond(self, x, want: bool, boundary: bool):
        typ = self.ents[x]
        das = [a for a, t in self.cp.dattrs if a not in self.date_used and t in (None, typ)]
        if not das:
            raise Fail("no_date")
        a = self.r.choice(das)
        self.date_used.add(a)
        lo, hi = self.cp.window
        span = (hi - lo).days
        D = lo + dt.timedelta(days=self.r.randint(span // 4, 3 * span // 4))
        one = dt.timedelta(days=1)
        if self.r.random() < 0.3:
            w = dt.timedelta(days=self.r.randint(5, 40))
            D1, D2 = D - w, D + w
            if boundary:
                v = D1 if self.r.random() < 0.5 else D2
                if not want:
                    v = D1 - one if v == D1 else D2 + one
            else:
                v = D1 + dt.timedelta(days=self.r.randint(1, (D2 - D1).days - 1)) if want else D2 + \
                    dt.timedelta(days=self.r.randint(1, 30))
            return ("win", a, D1, D2), a, v
        op = self.r.choice(("<", "<=", ">", ">="))
        if boundary:
            if op in ("<=", ">="):
                v = D if want else (D + one if op == "<=" else D - one)
            else:
                v = D if not want else (D - one if op == "<" else D + one)
        else:
            d = dt.timedelta(days=self.r.randint(2, 60))
            later = D + d
            earlier = D - d
            holds_later = op in (">", ">=")
            v = (later if holds_later else earlier) if want else (earlier if holds_later else later)
        return ("dcmp", a, op, D), a, v


def _eval_cond(cond, v):
    k = cond[0]
    if k == "cmp":
        return {">": v > cond[3], ">=": v >= cond[3], "<": v < cond[3], "<=": v <= cond[3]}[cond[2]]
    if k == "rng":
        return cond[2] <= v <= cond[3]
    if k == "dcmp":
        return {">": v > cond[3], ">=": v >= cond[3], "<": v < cond[3], "<=": v <= cond[3]}[cond[2]]
    if k == "win":
        return cond[2] <= v <= cond[3]
    raise ValueError(k)


# ------------------------------------------------------------------------------------------------------- chain schemas

class Chain:
    """Builds a decisive chain of k rule applications for a literal about an entity (OW or CW)."""

    def __init__(self, b: RB, world: str, want: dict):
        self.b, self.world, self.want = b, world, dict(want)
        self.r = b.r
        self.steps = []           # (schema, rule id)
        self.leaves = []          # (atom, value) leaf premises stated as facts
        self.extras_used = set()

    def can(self, sch, p, e, pol):
        b, cp, W = self.b, self.b.cp, self.world
        if cp.short and sch not in ("fwd_univ", "fwd_link"):
            return False
        t = b.ents[e]
        has_link_out = any(l["from"] == t for l in cp.links)
        has_link_in = any(l["to"] == t for l in cp.links)
        if sch == "fwd_univ":
            return W == "OW" or pol
        if sch == "bwd_univ":
            return W == "OW"
        if sch == "fwd_link":
            return "link" in cp.feats and has_link_out and (W == "OW" or pol)
        if sch == "bwd_link":
            return W == "OW" and "link" in cp.feats and has_link_in
        if sch in ("kofn",):
            return "kofn" in cp.feats and pol
        if sch == "or":
            return "or" in cp.feats and pol
        if sch == "xor":
            return "xor" in cp.feats and pol
        if sch == "onlyif_fwd":
            return W == "OW" and "onlyif" in cp.feats and pol
        if sch == "onlyif_contra":
            return W == "OW" and "onlyif" in cp.feats and not pol
        if sch == "bwd_or":
            return W == "OW" and "or" in cp.feats and not pol
        return False

    def pick(self, p, e, pol, left):
        w = {"fwd_univ": 3.0, "bwd_univ": 2.0, "fwd_link": 2.0, "bwd_link": 1.0, "kofn": 0.8, "or": 0.8,
             "xor": 0.6, "onlyif_fwd": 0.6, "onlyif_contra": 0.6, "bwd_or": 0.5}
        if self.want.get("mt"):
            for s in ("bwd_univ", "bwd_link", "onlyif_contra", "bwd_or"):
                w[s] *= 6
        if self.want.get("link"):
            for s in ("fwd_link", "bwd_link"):
                w[s] *= 6
        for s in ("kofn", "or", "xor", "onlyif_fwd"):
            if self.want.get(s):
                w[s] *= 10
        opts = [(s, x) for s, x in w.items() if self.can(s, p, e, pol)]
        if not opts:
            raise Fail("no_schema")
        tot = sum(x for _, x in opts)
        z = self.r.random() * tot
        for s, x in opts:
            z -= x
            if z <= 0:
                return s
        return opts[-1][0]

    def extras(self, e, n_lit, allow_neg=True, room=None):
        """Extra conditions on e that hold at cost 0: comparison / date conditions (when wanted) and literal facts,
        at most `room` in total."""
        b = self.b
        room = n_lit if room is None else room
        conds = []
        if b.cp.short:
            pass
        elif room > 0 and self.want.get("thr") and ("cmp" in b.cp.feats or "rng" in b.cp.feats):
            try:
                cond, qn, v = b.qty_cond(e, True, bool(self.want.get("boundary")))
                b.value(e, qn, v)
                conds.append(cond)
                self.want["thr"] = False
                self.want["boundary"] = False
            except Fail:
                pass
        elif room > 0 and self.want.get("date") and "date" in b.cp.feats:
            try:
                cond, an, v = b.date_cond(e, True, bool(self.want.get("boundary")))
                b.date(e, an, v)
                conds.append(cond)
                self.want["date"] = False
                self.want["boundary"] = False
            except Fail:
                pass
        for _ in range(max(0, min(n_lit, room - len(conds)))):
            q = b.pred(b.ents[e], "base")
            pos = True if (self.world == "CW" or not allow_neg or b.cp.short) else self.r.random() < 0.7
            if self.world == "CW" and self.r.random() < 0.25:
                conds.append(("lit", q, False))     # NAF: nothing stated (or a stated negative fact)
                if self.r.random() < 0.5:
                    b.fact(e, q, False)
                continue
            b.fact(e, q, pos)
            self.leaves.append((C.u(q, e), pos))
            conds.append(("lit", q, pos))
        return conds

    def exception(self, e, rule_typ):
        """An exception predicate for a rule on e, cleared for e (C(e) known false / closed / NAF)."""
        b = self.b
        if not self.want.get("exc") and not ("exc" in b.cp.feats and self.r.random() < 0.25):
            return None
        if "exc" not in b.cp.feats:
            return None
        c = b.pred(rule_typ, "exc")
        if self.world == "OW":
            if b.cp.unless == "strict":
                if "closure" in b.cp.feats and self.r.random() < 0.35:
                    b.closures.append((c, rule_typ, "prose", None))
                else:
                    b.fact(e, c, False)
                    self.leaves.append((C.u(c, e), False))
            elif self.r.random() < 0.3:
                b.fact(e, c, False)
        elif self.r.random() < 0.3:
            b.fact(e, c, False)
        self.want["exc"] = False
        return c

    def run(self, p, e, pol, k, fail_leaf=False, fail_kind="unknown"):
        """Make (p, e, pol) derivable at cost k. Returns the last literal (leaf)."""
        b = self.b
        cur = (p, e, pol)
        for i in range(k):
            p, e, pol = cur
            sch = self.pick(p, e, pol, k - i)
            nxt = getattr(self, "s_" + sch)(p, e, pol)
            self.steps.append(sch)
            if sch in ("bwd_univ", "bwd_link", "onlyif_contra", "bwd_or"):
                self.want["mt"] = False
            if sch in ("fwd_link", "bwd_link"):
                self.want["link"] = False
            for s in ("kofn", "or", "xor", "onlyif_fwd"):
                if sch == s:
                    self.want[s] = False
            cur = nxt
        p, e, pol = cur
        a = C.u(p, e)
        if fail_leaf:
            if self.world == "OW" and fail_kind == "false":
                b.fact(e, p, not pol)
            elif self.world == "CW" and not pol:
                b.fact(e, p, True)     # CW: a negative condition fails when its atom is stated
                b.near_miss.append((a, pol))
                return cur
            b.no_fact.add(a)
            b.near_miss.append((a, pol))
        else:
            if self.world == "CW" and not pol:
                pass                       # NAF leaf: nothing stated
            else:
                b.fact(e, p, pol)
                self.leaves.append((a, pol))
        return cur

    # --- schemas: each returns the next literal (pred, entity, pol)
    def _conds_with(self, chain_cond, e, max_extra=2):
        max_extra = min(max_extra, getattr(self.b.cp, "max_conds", 3) - 1)
        n_extra = self.r.choice((0, 0, 1, 1, 2)) if max_extra >= 2 else (self.r.choice((0, 1)) if max_extra == 1
                                                                         else 0)
        room = max(0, getattr(self.b.cp, "max_conds", 3) - 1)
        room = min(room, max_extra) if (self.want.get("thr") or self.want.get("date")) else min(room, n_extra)
        ex = self.extras(e, n_extra, room=room)
        conds = ex + [chain_cond]
        self.r.shuffle(conds)
        return tuple(conds)

    def s_fwd_univ(self, p, e, pol):
        b = self.b
        t = b.ents[e]
        q = b.pred(t, "derived")
        qpol = True if (self.world == "CW" or b.cp.short) else self.r.random() < 0.75
        conds = self._conds_with(("lit", q, qpol), e)
        exc = self.exception(e, t) if not b.cp.short else None
        if pol:
            b.rule(form="univ", typ=t, conds=conds, head=(p, True), exc=exc)
        else:
            if all(c[0] == "lit" and c[2] for c in conds) and len(conds) <= 2 and self.r.random() < 0.5:
                b.rule(form="neguniv", typ=t, conds=conds, head=(p, False), exc=exc)
            else:
                b.rule(form="univ", typ=t, conds=conds, head=(p, False), exc=exc)
        return (q, e, qpol)

    def s_bwd_univ(self, p, e, pol):
        b = self.b
        t = b.ents[e]
        h = b.pred(t, "derived")
        if not pol and self.r.random() < 0.35:
            conds = self._conds_with(("lit", p, True), e, max_extra=1)
            if all(c[0] == "lit" and c[2] for c in conds) and len(conds) <= 2:
                exc = self.exception(e, t)
                b.rule(form="neguniv", typ=t, conds=conds, head=(h, False), exc=exc)
                return (h, e, True)
        hpos = self.r.random() < 0.7
        conds = self._conds_with(("lit", p, not pol), e)
        exc = self.exception(e, t)
        b.rule(form="univ", typ=t, conds=conds, head=(h, hpos), exc=exc)
        return (h, e, not hpos)

    def s_fwd_link(self, p, e, pol):
        b = self.b
        t = b.ents[e]
        cands = [i for i, l in enumerate(b.cp.links) if l["from"] == t]
        li = self.r.choice(cands)
        t2 = b.cp.links[li]["to"]
        y = b.ent(t2)
        b.link(li, e, y)
        q = b.pred(t2, "derived")
        qpol = True if (self.world == "CW" or b.cp.short) else self.r.random() < 0.75
        b.rule(form="link", typ=t, link=li, ptyp=t2, pcond=(q, qpol), head=(p, pol))
        return (q, y, qpol)

    def s_bwd_link(self, p, e, pol):
        b = self.b
        t2 = b.ents[e]
        cands = [i for i, l in enumerate(b.cp.links) if l["to"] == t2]
        li = self.r.choice(cands)
        t1 = b.cp.links[li]["from"]
        x = b.ent(t1)
        b.link(li, x, e)
        h = b.pred(t1, "derived")
        hpos = self.r.random() < 0.7
        b.rule(form="link", typ=t1, link=li, ptyp=t2, pcond=(p, not pol), head=(h, hpos))
        return (h, x, not hpos)

    def s_kofn(self, p, e, pol):
        b = self.b
        t = b.ents[e]
        n = self.r.choice((3, 4))
        k = self.r.choice((2, 3)) if n == 4 else 2
        q = b.pred(t, "derived")
        items = [("lit", q, True)]
        for i in range(k - 1):
            z = b.pred(t, "base")
            zp = self.r.random() < 0.8 or self.world == "CW"
            b.fact(e, z, zp)
            self.leaves.append((C.u(z, e), zp))
            items.append(("lit", z, zp))
        for i in range(n - k):
            z = b.pred(t, "base")
            items.append(("lit", z, True))
            if self.world == "CW" or self.r.random() < 0.5:
                b.fact(e, z, False) if self.world == "OW" else None
        self.r.shuffle(items)
        b.rule(form="kofn", typ=t, conds=tuple(items), head=(p, True), k=k)
        return (q, e, True)

    def s_or(self, p, e, pol):
        b = self.b
        t = b.ents[e]
        q = b.pred(t, "derived")
        z = b.pred(t, "base")
        conds = [("lit", q, True), ("lit", z, True)]
        self.r.shuffle(conds)
        b.rule(form="or", typ=t, conds=tuple(conds), head=(p, True))
        if self.world == "OW" and self.r.random() < 0.3:
            b.fact(e, z, False)
        return (q, e, True)

    def s_xor(self, p, e, pol):
        b = self.b
        t = b.ents[e]
        q = b.pred(t, "derived")
        z = b.pred(t, "base")
        conds = [("lit", q, True), ("lit", z, True)]
        self.r.shuffle(conds)
        b.rule(form="xor", typ=t, conds=tuple(conds), head=(p, True))
        if self.world == "OW":
            b.fact(e, z, False)
            self.leaves.append((C.u(z, e), False))
        return (q, e, True)

    def s_onlyif_fwd(self, a, e, pol):
        b = self.b
        t = b.ents[e]
        h = b.pred(t, "derived")
        b.rule(form="onlyif", typ=t, conds=(("lit", a, True),), head=(a, True), ante=h)
        return (h, e, True)

    def s_onlyif_contra(self, h, e, pol):
        b = self.b
        t = b.ents[e]
        a = b.pred(t, "derived")
        b.rule(form="onlyif", typ=t, conds=(("lit", a, True),), head=(a, True), ante=h)
        return (a, e, False)

    def s_bwd_or(self, a, e, pol):
        b = self.b
        t = b.ents[e]
        h = b.pred(t, "derived")
        z = b.pred(t, "base")
        conds = [("lit", a, True), ("lit", z, True)]
        self.r.shuffle(conds)
        b.rule(form="or", typ=t, conds=tuple(conds), head=(h, True))
        return (h, e, False)


# ------------------------------------------------------------------------------------------------------- records

def to_record(b: RB) -> C.Record:
    derived = set()
    for r in b.rules:
        if r.head:
            derived.add(r.head[0])
    rec = C.Record(types=list(b.cp.types), ents=dict(b.ents), preds=dict(b.preds), exc_preds=set(b.exc_preds),
                   rules=list(b.rules), stmts=list(b.stmts), closures=list(b.closures), hedges=list(b.hedges),
                   ehedges=list(b.ehedges), lookalikes=list(b.lookalikes), links=list(b.cp.links),
                   qtys={q["name"]: {"unit": q["unit"], "dec": q["dec"]} for q in b.cp.qtys},
                   dattrs=[a for a, _ in b.cp.dattrs])
    rec.extras = {"derived": derived}
    return rec


def pick_type(b: RB, want_link: bool):
    cp = b.cp
    ts = list(range(len(cp.types)))
    if want_link and cp.links:
        out = sorted({l["from"] for l in cp.links} | {l["to"] for l in cp.links})
        return b.r.choice(out)
    return b.r.choice(ts)


def alt_route(b: RB, x, p, pol, world):
    """Near-miss for a decided literal: another rule for the same literal that fails on one unstated premise.
    Short cards (no clause 5 / 5c): the near-miss decides the literal the other way instead, so that the conjunctive
    CW reading (R1 with R3) of the short card does not change the answer."""
    t = b.ents[x]
    z = b.pred(t, "base")
    if b.cp.short:
        if pol:
            b.rule(form="neguniv", typ=t, conds=(("lit", z, True),), head=(p, False))
        else:
            b.rule(form="univ", typ=t, conds=(("lit", z, True),), head=(p, True))
        b.no_fact.add(C.u(z, x))
        b.near_miss.append((C.u(z, x), True))
        return
    if world == "OW" and not pol and b.r.random() < 0.5:
        b.rule(form="neguniv", typ=t, conds=(("lit", z, True),), head=(p, False))
    else:
        b.rule(form="univ", typ=t, conds=(("lit", z, True),), head=(p, pol))
    b.no_fact.add(C.u(z, x))
    b.near_miss.append((C.u(z, x), True))


def population(b: RB, x, n, chain_rules, world, rng, matched=False, detail=True):
    """Distractor entities of x's type: each copies x's chain leaves and values but fails exactly one essential
    premise (a leaf left out or flipped, or a value moved across its threshold), so the chain predicates appear with
    other labels on the card (5.1 control) and choice options get near-miss distractors (E8, E5).
    matched=True (choice rows; repair r1, G7 'gold entity most mentioned'): each entity is a near-miss twin of x with
    the same number of record statements as x: it copies every statement whose subject is x (facts, values, dates,
    links to the same partner), and its one failed premise keeps the count: OW flips the leaf (a stated negative),
    a value moves across its threshold, a link goes to a fresh partner with no facts; CW (no stated negatives) leaves
    the leaf out and, if detail, states one fact of a predicate that no rule uses instead."""
    if matched:
        return _population_matched(b, x, n, world, rng, detail)
    t = b.ents[x]
    leaves = [(a, v) for a, v in b.notes.get("leaves", []) if a[0] == "u" and a[2] == x]
    essential = [(a, v) for a, v in leaves if not (world == "CW" and not v) and
                 not (a[1] in b.exc_preds and (world == "CW" or b.cp.unless == "listc"))]
    vals = [s for s in b.stmts if s.kind in ("val", "date") and s.e == x and s.value is not None]
    conds = {}
    for r in b.rules:
        if r.typ != t:
            continue
        for c in r.conds:
            if c[0] in ("cmp", "rng", "dcmp", "win"):
                conds.setdefault(c[1], []).append(c)
    out = []
    for _ in range(n):
        try:
            z = b.ent(t)
        except Fail:
            break
        out.append(z)
        fail_opts = [("leaf", l) for l in essential] + [("val", s) for s in vals if conds.get(s.pred)]
        fail = rng.choice(fail_opts) if fail_opts else None
        for (a, v) in leaves:
            if fail and fail[0] == "leaf" and fail[1] == (a, v):
                if world == "OW" and rng.random() < 0.4:
                    try:
                        b.fact(z, a[1], not v)
                    except Fail:
                        pass
                continue
            try:
                b.fact(z, a[1], v)
            except Fail:
                pass
        for s in vals:
            cs = conds.get(s.pred, [])
            want_flip = fail is not None and fail[0] == "val" and fail[1] is s
            for _try in range(30):
                if s.kind == "val":
                    q = next(qq for qq in b.cp.qtys if qq["name"] == s.pred)
                    step = Decimal(1).scaleb(-q["dec"])
                    v = s.value + step * rng.choice((-9, -5, -2, -1, 1, 2, 5, 9))
                    if not (Decimal(str(q["lo"])) <= v <= Decimal(str(q["hi"]))):
                        continue
                else:
                    v = s.value + dt.timedelta(days=rng.choice((-20, -5, -1, 1, 5, 20)))
                same = all(_eval_cond(c, v) == _eval_cond(c, s.value) for c in cs)
                if same != want_flip:
                    if s.kind == "val":
                        b.value(z, s.pred, v)
                    else:
                        b.date(z, s.pred, v)
                    break
    return out


def _population_matched(b: RB, x, n, world, rng, detail):
    t = b.ents[x]
    leaves = {(a, v) for a, v in b.notes.get("leaves", []) if a[0] == "u" and a[2] == x}
    essential = {(a, v) for a, v in leaves if not (world == "CW" and not v) and
                 not (a[1] in b.exc_preds and (world == "CW" or b.cp.unless == "listc"))}
    own = [s for s in b.stmts if s.e == x and s.src is None and s.tag is None and s.via == "sent" and
           not (s.kind == "lit" and s.pos is None) and not (s.kind in ("val", "date") and s.value is None)]
    obj_links = [s for s in b.stmts if s.kind == "link" and s.value == x and s.src is None]
    conds = {}
    for r in b.rules:
        if r.typ != t:
            continue
        for c in r.conds:
            if c[0] in ("cmp", "rng", "dcmp", "win"):
                conds.setdefault(c[1], []).append(c)
    fail_opts = [("leaf", s) for s in own if s.kind == "lit" and (C.u(s.pred, x), s.pos) in essential]
    fail_opts += [("val", s) for s in own if s.kind in ("val", "date") and conds.get(s.pred)]
    fail_opts += [("link", s) for s in own if s.kind == "link"]
    dpred = [None]

    def detail_fact(z):
        if not detail:
            return
        if dpred[0] is None:
            dpred[0] = b.pred(t, "base")
        b.fact(z, dpred[0], True if world == "CW" else rng.random() < 0.6)

    # repair r1b (G6 / G7, CW CH-claim): when c is a CW near-miss (gold 'x is not H'), plain near-miss twins lack H
    # too, so 'z is not H' would also follow and every same-predicate distractor had to be 'z is H': the gold was the
    # only negated option far above chance (and 'few_neg_distractors' retries selected for it). Flip twins mirror the
    # positive case: z copies x and its one failing premise holds for z (the missing leaf is stated, or the stated
    # atom that fails a negative condition is left out), so 'z is not H' is a same-predicate negated distractor.
    # Statement counts stay matched (one detail fact on x for an added leaf, on z for a dropped atom).
    flip = None
    nm = list(getattr(b, "near_miss", None) or [])
    if world == "CW" and detail and b.notes.get("decided") is False and len(nm) == 1:
        a0, v0 = nm[0]
        if a0[0] == "u" and a0[2] == x:
            if v0:
                flip = ("add", a0[1])
            else:
                st = [s for s in own if s.kind == "lit" and s.pred == a0[1] and s.pos is True]
                if len(st) == 1:
                    flip = ("drop", st[0])
    out = []
    for _ in range(n):
        try:
            z = b.ent(t)
        except Fail:
            break
        out.append(z)
        if flip is not None:
            for s in own:
                if flip[0] == "drop" and s is flip[1]:
                    continue
                if s.kind == "lit":
                    try:
                        b.fact(z, s.pred, s.pos)
                    except Fail:
                        detail_fact(z)
                elif s.kind == "val":
                    b.value(z, s.pred, s.value)
                elif s.kind == "date":
                    b.date(z, s.pred, s.value)
                elif s.kind == "link":
                    b.link(s.pred, z, s.value)
            if flip[0] == "add":
                try:
                    b.fact(z, flip[1], True)
                except Fail:
                    detail_fact(z)
            else:
                detail_fact(z)
            for _s in obj_links:
                detail_fact(z)
            continue
        fail = rng.choice(fail_opts) if fail_opts else None
        for s in own:
            is_fail = fail is not None and fail[1] is s
            if s.kind == "lit":
                if is_fail:
                    done = False
                    if world == "OW":
                        try:
                            b.fact(z, s.pred, not s.pos)
                            done = True
                        except Fail:
                            done = False
                    if not done:
                        detail_fact(z)
                    continue
                try:
                    b.fact(z, s.pred, s.pos)
                except Fail:
                    detail_fact(z)
            elif s.kind in ("val", "date"):
                cs = conds.get(s.pred, [])
                for _try in range(30):
                    if s.kind == "val":
                        q = next(qq for qq in b.cp.qtys if qq["name"] == s.pred)
                        step = Decimal(1).scaleb(-q["dec"])
                        v = s.value + step * rng.choice((-9, -5, -2, -1, 1, 2, 5, 9))
                        if not (Decimal(str(q["lo"])) <= v <= Decimal(str(q["hi"]))):
                            continue
                    else:
                        v = s.value + dt.timedelta(days=rng.choice((-20, -5, -1, 1, 5, 20)))
                    same = all(_eval_cond(c, v) == _eval_cond(c, s.value) for c in cs)
                    if same != is_fail:
                        if s.kind == "val":
                            b.value(z, s.pred, v)
                        else:
                            b.date(z, s.pred, v)
                        break
                else:
                    if is_fail:
                        raise Fail("matched_val")
                    if s.kind == "val":
                        b.value(z, s.pred, s.value)
                    else:
                        b.date(z, s.pred, s.value)
            elif s.kind == "link":
                if is_fail:
                    y2 = b.ent(b.ents[s.value])
                    b.link(s.pred, z, y2)
                else:
                    b.link(s.pred, z, s.value)
        for _s in obj_links:
            detail_fact(z)
    if flip is not None and flip[0] == "add" and out:
        detail_fact(x)          # x's count = each flip twin's (x's statements + the leaf x lacks)
    return out


def irrelevant_rules(b: RB, n, rng):
    for _ in range(n):
        t = rng.randrange(len(b.cp.types))
        try:
            a = b.pred(t, "base")
            h = b.pred(t, "derived")
        except Fail:
            return
        pos = rng.random() < 0.7
        b.rule(form="univ", typ=t, conds=(("lit", a, True),), head=(h, pos))


def make_base(cp: CardPlan, rng: random.Random, tgt: dict):
    """One sampled record for a target. tgt keys: world, label (F/R/O for OW; T/F for CW, of the row's c),
    depth, neg (claim polarity negative), want (tag dict), form (row form family), k (options), none_gold.
    Returns (RB, c, chain) or raises Fail."""
    b = RB(cp, rng)
    W = tgt["world"]
    want = dict(tgt.get("want", {}))
    t0 = pick_type(b, want.get("link"))
    if tgt.get("look"):
        x = None
        for a, pp in cp.looks:
            if a in b._ids and pp in b._ids:
                b._ids.remove(a)
                b._ids.remove(pp)
                b.ents[a] = t0
                b.notes["look_partner"] = pp
                x = a
                break
        if x is None:
            raise Fail("looks")
    else:
        x = b.ent(t0)
    p = b.pred(t0, "derived")
    cpos = not tgt["neg"]
    ch = Chain(b, W, want)
    d = tgt["depth"]
    lab = tgt["label"]
    decided = True
    if W == "OW":
        if lab == "F":
            ch.run(p, x, cpos, d)
            alt_route(b, x, p, cpos, W)
        elif lab == "R":
            ch.run(p, x, not cpos, d)
            alt_route(b, x, p, not cpos, W)
        else:
            lpol = cpos if rng.random() < 0.5 else (not cpos)
            ch.run(p, x, lpol, d, fail_leaf=True, fail_kind="false" if rng.random() < 0.2 else "unknown")
            decided = False
    else:
        in_m = (cpos and lab == "T") or ((not cpos) and lab == "F")
        if in_m:
            ch.run(p, x, True, d)
            alt_route(b, x, p, True, W)
        else:
            ch.run(p, x, True, d, fail_leaf=True)
            decided = False
    b.notes["claim"] = (p, x, cpos)
    b.notes["chain"] = list(ch.steps)
    b.notes["decided"] = decided
    b.notes["want_left"] = {k: v for k, v in ch.want.items() if v}
    return b, (p, x, cpos), ch

"""Core engine for gen_constraints (golden_src/gen/gen_constraints.py).

Values (stored exactly as ints / strings / frozensets):
  money = cents, num = int in 1/scale units, time = minutes after midnight, date = proleptic ordinal, dur = minutes,
  bool, cat = str, set = frozenset of str.  MISSING (a detail the listing does not state) and NA (not applicable, e.g.
  the layover of a nonstop flight) are sentinels.

Predicates are small trees evaluated with three-valued (Kleene) logic; a requirement counts as met only when it
evaluates to True, so a requirement that depends on a MISSING value is never met (the state text says so).

Constraints (Con subclasses) own their pred, their text (rendered per row style) and their fact-flip variants.
The solver: qualifiers = options meeting every hard requirement; with a tie-break the unique best qualifier wins
(an exact tie on every tie-break key makes the item invalid), without one exactly one qualifier must exist; zero
qualifiers is valid only when the option list has a "none of the listed ..." option.
"""
import datetime as dt
from fractions import Fraction as Fr

MISSING = "<missing>"
NA = "<na>"
LE, LT, GE, GT = "<=", "<", ">=", ">"
OPP = {LE: GT, GE: LT, LT: GE, GT: LE}  # 'must not <OPP words>' == op


def unk(v):
    return isinstance(v, str) and v in (MISSING, NA)


# ------------------------------------------------------------------------------------------------ formatting
MON = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
       "December"]
WD = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def fmt_money(c, cur="$", cents=False):
    s = f"{c // 100:,}"
    if cents or c % 100:
        s += f".{c % 100:02d}"
    return f"{cur}{s}"


def fmt_dec(v, scale):
    if scale == 1:
        return f"{v:,}"
    d = {10: 1, 100: 2, 1000: 3}[scale]
    neg = v < 0
    v = abs(v)
    s = f"{v // scale:,}.{v % scale:0{d}d}"
    return ("-" if neg else "") + s


def fmt_time(m, style="24"):
    h, mi = divmod(m, 60)
    if style == "24":
        return f"{h:02d}:{mi:02d}"
    h12 = h % 12 or 12
    return f"{h12}:{mi:02d} {'am' if h < 12 else 'pm'}"


def fmt_date(o, style="dmy"):
    d = dt.date.fromordinal(o)
    if style == "dmy":
        return f"{WD[d.weekday()][:3]} {d.day} {MON[d.month - 1][:3]}"
    if style == "mdy":
        return f"{WD[d.weekday()][:3]}, {MON[d.month - 1][:3]} {d.day}"
    if style == "iso":
        return d.isoformat()
    return f"{WD[d.weekday()]} {d.day} {MON[d.month - 1]}"  # long


def fmt_dur(m, style="hm"):
    h, mi = divmod(m, 60)
    if style == "min":
        return f"{m} min"
    if h == 0:
        return f"{mi} min"
    return f"{h} h {mi:02d} min" if style == "hm" else f"{h}h{mi:02d}"


def plural(n, unit):
    if isinstance(unit, tuple):
        return unit[0] if n == 1 else unit[1]
    return unit


BOOL_DISP = {"yn": ("yes", "no"), "YN": ("Yes", "No"), "yx": ("Y", "N")}


class Attr:
    """One listed detail of an option.  kind: money | num | time | date | dur | bool | cat | set."""

    def __init__(self, key, kind, header, gen=None, lo=None, hi=None, step=1, scale=1, unit=None, cur=None,
                 cents=False, vp=(), cls="amount", field=(None, None), pr=None, noun=None, anti=(), cats=(),
                 items=(), kset=(1, 3), p=0.5, derived=False, missing_ok=True, disp=None, date_lo=0, date_hi=30,
                 short=None):
        self.key, self.kind, self.header = key, kind, header
        self.lo, self.hi, self.step, self.scale = lo, hi, step, scale
        self.unit, self.cur, self.cents = unit, cur, cents
        self.vp = list(vp)  # requirement verb phrases (base form) with {c} (comparator) and {v} (value)
        self.cls = cls  # comparator lexicon class: amount | count | time | date
        self.field = field  # (field label for a max, field label for a min)
        self.pr = pr  # prose template(s)
        self.noun = noun  # bool: noun for 'without <noun>'
        self.anti = list(anti)  # bool: VPs meaning the feature is ABSENT (want False, positive modal)
        self.cats, self.items, self.kset, self.p = list(cats), list(items), kset, p
        self._gen = gen
        self.derived, self.missing_ok = derived, missing_ok
        self.disp = disp  # bool display override
        self.date_lo, self.date_hi = date_lo, date_hi
        self.short = short or header.lower()

    # ---- generation
    def gen(self, rng, ctx, o):
        if self._gen is not None:
            return self._gen(rng, ctx, o)
        k = self.kind
        if k in ("money", "num", "dur", "time"):
            return rng.randrange(self.lo, self.hi + 1, self.step)
        if k == "date":
            return ctx["today"] + rng.randint(self.date_lo, self.date_hi)
        if k == "bool":
            return rng.random() < self.p
        if k == "cat":
            return rng.choice(self.cats)
        if k == "set":
            n = rng.randint(*self.kset)
            return frozenset(rng.sample(self.items, min(n, len(self.items))))
        raise ValueError(k)

    # ---- display
    def fmt(self, v, st):
        if v == MISSING:
            return st["missing"]
        if v == NA:
            return st["na"]
        sp = getattr(self, "special", None)
        if sp and v in sp:
            return sp[v]
        k = self.kind
        if k == "money":
            return fmt_money(v, self.cur or st["cur"], self.cents)
        if k == "num":
            s = str(v) if getattr(self, "nocomma", False) else fmt_dec(v, self.scale)
            if self.unit is None:
                return s
            if isinstance(self.unit, tuple):
                return f"{s} {plural(v if self.scale == 1 else 2, self.unit)}"
            return s + self.unit  # suffix such as '%', ' GB'
        if k == "time":
            return fmt_time(v, st["time"])
        if k == "date":
            return fmt_date(v, st["date"])
        if k == "dur":
            return fmt_dur(v, st["dur"])
        if k == "bool":
            pair = self.disp or BOOL_DISP[st["bool"]]
            return pair[0] if v else pair[1]
        if k == "cat":
            return v
        if k == "set":
            if not v:
                return "none"
            return ", ".join(x for x in self.items if x in v) if self.items else ", ".join(sorted(v))
        raise ValueError(k)

    def prose(self, v, st):
        """Phrase for prose listings: 'costs $12.49', 'includes tracking' / 'does not include tracking'."""
        hv = st.get("hv", {})
        if unk(v):
            return f"{self.short.format(**hv)}: {self.fmt(v, st)}"
        if callable(self.pr):
            return self.pr(v, self.fmt(v, st))
        if self.kind == "bool":
            return (self.pr[0] if v else self.pr[1]).format(**hv)
        if self.kind == "set" and not v:
            return self.pr[1] if isinstance(self.pr, tuple) else f"{self.short}: none"
        t = self.pr[0] if isinstance(self.pr, tuple) else self.pr
        return t.format(v=self.fmt(v, st))


# ------------------------------------------------------------------------------------------------ expressions
def ev(e, o, ctx):
    t = e[0]
    if t == "a":
        return o.get(e[1], MISSING)
    if t == "k":
        return e[1]
    if t == "x":
        return ctx[e[1]]
    if t in ("+", "-", "*"):
        a, b = ev(e[1], o, ctx), ev(e[2], o, ctx)
        if unk(a) or unk(b):
            return MISSING
        return a + b if t == "+" else (a - b if t == "-" else a * b)
    if t == "min":
        a, b = ev(e[1], o, ctx), ev(e[2], o, ctx)
        if unk(a) or unk(b):
            return MISSING
        return min(a, b)
    if t == "conv":  # value * Fraction factor
        a = ev(e[1], o, ctx)
        return MISSING if unk(a) else Fr(a) * e[2]
    if t == "bizd":  # date + n business days (Mon-Fri, excluding listed holidays)
        d, n = ev(e[1], o, ctx), ev(e[2], o, ctx)
        if unk(d) or unk(n):
            return MISSING
        hol = set(e[3])
        while n > 0:
            d += 1
            if dt.date.fromordinal(d).weekday() < 5 and d not in hol:
                n -= 1
        return d
    if t == "ceil":  # ceiling of a / b (ints)
        a = ev(e[1], o, ctx)
        if unk(a):
            return MISSING
        return -(-a // e[2])
    raise ValueError(e)


def tv(p, o, ctx):
    """Three-valued truth of predicate p on option o: True / False / None (unknown)."""
    t = p[0]
    if t == "cmp":
        a, b = ev(p[1], o, ctx), ev(p[3], o, ctx)
        if unk(a) or unk(b):
            return None
        op = p[2]
        return a <= b if op == LE else a < b if op == LT else a >= b if op == GE else a > b
    if t == "bool":
        v = ev(p[1], o, ctx)
        return None if unk(v) else (v == p[2])
    if t == "in":
        v = ev(p[1], o, ctx)
        return None if unk(v) else (v in p[2])
    if t == "has":
        v = ev(p[1], o, ctx)
        return None if unk(v) else (p[2] in v)
    if t == "hasall":
        v = ev(p[1], o, ctx)
        return None if unk(v) else all(x in v for x in p[2])
    if t == "hask":
        v = ev(p[1], o, ctx)
        return None if unk(v) else (sum(x in v for x in p[2]) >= p[3])
    if t == "disj":
        v = ev(p[1], o, ctx)
        return None if unk(v) else not (set(v) & set(p[2]))
    if t == "not":
        x = tv(p[1], o, ctx)
        return None if x is None else (not x)
    if t == "and":
        xs = [tv(q, o, ctx) for q in p[1:]]
        return False if False in xs else (None if None in xs else True)
    if t == "or":
        xs = [tv(q, o, ctx) for q in p[1:]]
        return True if True in xs else (None if None in xs else False)
    if t == "imp":
        return tv(("or", ("not", p[1]), p[2]), o, ctx)
    raise ValueError(p)


def cmp_nodes(p):
    if p[0] == "cmp":
        yield p
    elif p[0] in ("and", "or"):
        for q in p[1:]:
            yield from cmp_nodes(q)
    elif p[0] in ("not",):
        yield from cmp_nodes(p[1])
    elif p[0] == "imp":
        yield from cmp_nodes(p[1])
        yield from cmp_nodes(p[2])


# ------------------------------------------------------------------------------------------------ comparator lexicon
LEX = {
    "amount": {LE: ["at most", "no more than", "not more than", "a maximum of", "up to"],
               LT: ["less than", "under", "below"],
               GE: ["at least", "no less than", "not less than", "a minimum of"],
               GT: ["more than", "over", "above"]},
    "count": {LE: ["at most", "no more than", "not more than", "a maximum of", "up to"],
              LT: ["fewer than", "less than", "under"],
              GE: ["at least", "no fewer than", "not fewer than", "a minimum of"],
              GT: ["more than", "over"]},
    "time": {LE: ["by", "no later than", "at or before", "not later than"],
             LT: ["before", "earlier than"],
             GE: ["no earlier than", "at or after", "not earlier than"],
             GT: ["after", "later than"]},
    "date": {LE: ["by", "on or before", "no later than"],
             LT: ["before"],
             GE: ["on or after", "no earlier than"],
             GT: ["after"]},
}
MODAL_POS = ["must", "has to", "needs to"]
MODAL_NEG = ["must not", "cannot", "can't"]


def cap(s):
    return s[:1].upper() + s[1:] if s else s


def modal(pol, i):
    return (MODAL_POS if pol == "pos" else MODAL_NEG)[i % 3]


class Con:
    """A hard requirement.  Subclasses define pred(), render(st, mi) and variants()."""
    cid = "con"
    group = None
    tags = ()
    attrs = ()
    implicit = False

    def pred(self):
        raise NotImplementedError

    def focus(self, ctx):
        return []

    def margin(self, o, ctx):
        m = None
        for node in cmp_nodes(self.pred()):
            a, b = ev(node[1], o, ctx), ev(node[3], o, ctx)
            if unk(a) or unk(b):
                continue
            d = abs(Fr(a) - Fr(b)) / Fr(self.mscale)
            m = d if m is None else min(m, d)
        return m if m is not None else 0

    mscale = 1

    def variants(self, rng, dom, ctx):
        return []

    def ctx_sentence(self, st, mi):
        return None

    def checks(self, st):
        """[(kind, payload)] for the independent phrase checker."""
        return []


def lex_word(cls, op, pol, wi):
    words = LEX[cls][op if pol == "pos" else OPP[op]]
    return words[wi % len(words)]


class CmpCon(Con):
    """<expr> <op> <threshold>; expr defaults to the attribute itself."""

    def __init__(self, cid, attr, op, thr, pol="pos", wi=0, vpi=0, expr=None, attrs=None, vp=None, cls=None,
                 vfmt=None, lo=None, hi=None, step=None, note=None, implicit=None, field=True, group=None, tags=(),
                 mscale=None, vstep=None):
        self.cid, self.attr, self.op, self.thr, self.pol, self.wi, self.vpi = cid, attr, op, thr, pol, wi, vpi
        if pol == "neg":
            assert op in (LE, GE)
        self.expr = expr or ("a", attr.key)
        self.attrs = attrs or [attr.key]
        self.vps = vp or attr.vp
        self.cls = cls or attr.cls
        self.vfmt = vfmt  # function (thr, st) -> str for thresholds not in the attribute's own format
        self.lo = attr.lo if lo is None else lo
        self.hi = attr.hi if hi is None else hi
        self.step = step or attr.step
        self.vstep = vstep or self.step
        self.note = note  # e.g. '(1 kg = 2.2 lb)'
        self.implicit = implicit  # (context sentence template with {v}, requirement VP without a number)
        self.field = field and not implicit and attr.field != (None, None)
        self.group = group or attr.key
        self.tags = set(tags)
        self.mscale = mscale or self.step
        if attr.kind in ("time",):
            self.tags.add("temporal")
        elif attr.kind == "date":
            self.tags.add("temporal")
        elif attr.kind in ("money", "num", "dur"):
            self.tags.add("numeric")
        if implicit:
            self.tags.add("implicit")
        if pol == "neg":
            self.tags.add("negation")

    def pred(self):
        return ("cmp", self.expr, self.op, ("k", self.thr))

    def vstr(self, st):
        return self.vfmt(self.thr, st) if self.vfmt else self.attr.fmt(self.thr, st)

    def word(self):
        return lex_word(self.cls, self.op, self.pol, self.wi)

    def render(self, st, mi):
        v = self.vstr(st)
        if self.implicit:
            vp = self.implicit[1]
            pol = "pos"
        else:
            vp = self.vps[self.vpi % len(self.vps)].format(c=self.word(), v=v)
            pol = self.pol
        inline = f"{modal(pol, mi)} {vp}"
        if self.note:
            inline += f" {self.note}"
        out = {"inline": inline, "bullet": cap(inline) + ".", "field": None}
        if self.field and self.pol == "pos" and self.expr == ("a", self.attr.key):
            fmx, fmn = self.attr.field
            if self.op == LE and fmx:
                out["field"] = f"{fmx}: {v}"
            elif self.op == GE and fmn:
                out["field"] = f"{fmn}: {v}"
            elif self.op in (LT, GT):
                out["field"] = f"{self.attr.header.format(**st.get('hv', {}))}: {self.word()} {v}"
        return out

    def ctx_sentence(self, st, mi):
        if not self.implicit:
            return None
        return self.implicit[0].format(v=self.vstr(st))

    def checks(self, st):
        if self.implicit:
            if getattr(self, "names", None):
                return [("names", tuple(self.names), self.thr)]
            return [("implicit", self.vstr(st))]
        return [("cmp", self.cls, self.op, self.pol, self.vstr(st))]

    def focus(self, ctx):
        if self.expr != ("a", self.attr.key):
            return []
        return [(self.attr.key, self.thr + d * self.vstep) for d in (-2, -1, 0, 1, 2)]

    def with_thr(self, thr):
        c = CmpCon.__new__(CmpCon)
        c.__dict__.update(self.__dict__)
        c.tags = set(self.tags)
        c.thr = thr
        return c

    def variants(self, rng, dom, ctx):
        if getattr(self, "fixed", False):
            return []
        out = []
        for k in (1, 2, 3, 4, 6, 8, 10):
            for s in (1, -1):
                t = self.thr + s * k * self.vstep
                if self.lo is not None and self.hi is not None and not (self.lo <= t <= self.hi):
                    continue
                out.append(self.with_thr(t))
        return out


class BoolCon(Con):
    """Feature must be present (want True) or absent (want False).
    form: pos (must <vp>), neg (must not <vp>; want False), dneg (cannot be without <noun>; want True),
    anti (must <anti vp>; want False)."""

    def __init__(self, cid, attr, want, form, vpi=0, group=None, vps=None):
        assert (form in ("pos", "dneg")) == want
        self.cid, self.attr, self.want, self.form, self.vpi = cid, attr, want, form, vpi
        self.vps = list(vps) if vps else list(attr.vp)
        self.attrs = [attr.key]
        self.group = group or attr.key
        self.tags = set()
        if form == "neg":
            self.tags.add("negation")
        if form == "dneg":
            self.tags.add("double_negation")

    def pred(self):
        return ("bool", ("a", self.attr.key), self.want)

    def render(self, st, mi):
        a = self.attr
        if self.form == "pos":
            inline = f"{modal('pos', mi)} {self.vps[self.vpi % len(self.vps)]}"
        elif self.form == "neg":
            inline = f"{modal('neg', mi)} {self.vps[self.vpi % len(self.vps)]}"
        elif self.form == "dneg":
            inline = f"{modal('neg', mi)} {['be without', 'come without', 'be one without'][self.vpi % 3]} {a.noun}"
        else:
            inline = f"{modal('pos', mi)} {a.anti[self.vpi % len(a.anti)]}"
        fld = None
        if self.form in ("pos", "neg"):
            fld = f"{a.header.format(**st.get('hv', {}))}: {'required' if self.want else 'not acceptable'}"
        return {"inline": inline, "bullet": cap(inline) + ".", "field": fld}

    def checks(self, st):
        return [("bool", self.want, self.form)]

    def variants(self, rng, dom, ctx):
        return []


def or_join(xs, conj="or"):
    xs = list(xs)
    if len(xs) == 1:
        return xs[0]
    if len(xs) == 2:
        return f"{xs[0]} {conj} {xs[1]}"
    return ", ".join(xs[:-1]) + f" {conj} " + xs[-1]


class CatCon(Con):
    """Categorical value must be one of vals (neg=False) or none of vals (neg=True)."""

    def __init__(self, cid, attr, vals, neg=False, vpi=0, mi_fixed=None, group=None):
        self.cid, self.attr, self.vals, self.neg, self.vpi = cid, attr, tuple(vals), neg, vpi
        self.attrs = [attr.key]
        self.group = group or attr.key
        self.tags = {"negation"} if neg else set()

    def pred(self):
        p = ("in", ("a", self.attr.key), frozenset(self.vals))
        return ("not", p) if self.neg else p

    def render(self, st, mi):
        a = self.attr
        v = or_join(self.vals)
        vp = a.vp[self.vpi % len(a.vp)].format(v=v)
        inline = f"{modal('neg' if self.neg else 'pos', mi)} {vp}"
        fld = f"{a.header.format(**st.get('hv', {}))}: {'not ' + v if self.neg else v + (' only' if len(self.vals) > 1 else '')}"
        return {"inline": inline, "bullet": cap(inline) + ".", "field": fld}

    def checks(self, st):
        return [("cat", self.neg, self.vals)]

    def variants(self, rng, dom, ctx):
        out = []
        pool = [c for c in self.attr.cats if c not in self.vals]
        for i in range(len(self.vals)):
            for c in pool:
                vals = list(self.vals)
                vals[i] = c
                out.append(CatCon(self.cid, self.attr, vals, self.neg, self.vpi, group=self.group))
        return out


class SetCon(Con):
    """Set-valued detail: has item / has all items / has at least k of items / lacks item."""

    def __init__(self, cid, attr, mode, items, k=1, vpi=0, group=None):
        self.cid, self.attr, self.mode, self.items, self.k, self.vpi = cid, attr, mode, tuple(items), k, vpi
        self.attrs = [attr.key]
        self.group = group or attr.key
        self.tags = set()
        if mode in ("all", "k"):
            self.tags.add("quantifier")
        if mode == "lacks":
            self.tags.add("negation")

    def pred(self):
        a = ("a", self.attr.key)
        if self.mode == "has":
            return ("has", a, self.items[0])
        if self.mode == "all":
            return ("hasall", a, self.items)
        if self.mode == "k":
            return ("hask", a, self.items, self.k)
        return ("not", ("has", a, self.items[0]))

    def render(self, st, mi):
        a = self.attr
        vp = a.vp[self.vpi % len(a.vp)]
        if self.mode in ("has", "lacks"):
            obj = self.items[0]
        elif self.mode == "all":
            obj = ("both " if len(self.items) == 2 else "all of ") + or_join(self.items, "and")
        else:
            n = {2: "two", 3: "three", 4: "four"}[self.k]
            obj = f"at least {n} of {or_join(self.items, 'and')}"
        inline = f"{modal('neg' if self.mode == 'lacks' else 'pos', mi)} {vp.format(v=obj)}"
        return {"inline": inline, "bullet": cap(inline) + ".", "field": None}

    def checks(self, st):
        return [("set", self.mode, self.items, self.k)]

    def variants(self, rng, dom, ctx):
        if getattr(self, "fixed", False):
            return []
        out = []
        pool = [x for x in getattr(self, "pool", self.attr.items) if x not in self.items]
        for i in range(len(self.items)):
            for x in pool:
                it = list(self.items)
                it[i] = x
                out.append(SetCon(self.cid, self.attr, self.mode, it, self.k, self.vpi, self.group))
        if self.mode == "k":
            for k2 in (self.k - 1, self.k + 1):
                if 1 <= k2 <= len(self.items) and k2 in (2, 3, 4):
                    out.append(SetCon(self.cid, self.attr, self.mode, self.items, k2, self.vpi, self.group))
        return out


class FnCon(Con):
    """A domain-specific requirement with its own pred / text builders (exceptions, conditionals, windows, overlaps).
    params: dict of parameters; build(params) -> (pred, focus list); text(params, st, mi) -> dict(inline, bullet,
    field); vary(params, rng) -> list of params; chk(params, st) -> checks."""

    def __init__(self, cid, attrs, params, build, text, vary=None, chk=None, tags=(), group=None, mscale=1,
                 ctxs=None):
        self.cid, self.attrs, self.params = cid, list(attrs), dict(params)
        self._build, self._text, self._vary, self._chk, self._ctxs = build, text, vary, chk, ctxs
        self.tags = set(tags)
        self.group = group or cid
        self.mscale = mscale
        self.implicit = ctxs is not None
        self._p, self._focus = build(self.params)

    def pred(self):
        return self._p

    def focus(self, ctx):
        return list(self._focus)

    def render(self, st, mi):
        return self._text(self.params, st, mi)

    def ctx_sentence(self, st, mi):
        return self._ctxs(self.params, st) if self._ctxs else None

    def checks(self, st):
        return self._chk(self.params, st) if self._chk else []

    def variants(self, rng, dom, ctx):
        if not self._vary:
            return []
        out = []
        for p in self._vary(dict(self.params), rng):
            out.append(FnCon(self.cid, self.attrs, p, self._build, self._text, self._vary, self._chk, self.tags,
                             self.group, self.mscale, self._ctxs))
        return out


# ------------------------------------------------------------------------------------------------ tie-breaks
class Tie:
    """Lexicographic tie-break: keys = [(expr, 'min'|'max')]; texts = sentence variants (full sentences)."""

    def __init__(self, tid, keys, texts, short, attrs, tags=()):
        self.tid, self.keys, self.texts, self.short, self.attrs = tid, keys, list(texts), short, list(attrs)
        self.tags = set(tags)

    def key(self, o, ctx):
        out = []
        for e, d in self.keys:
            v = ev(e, o, ctx)
            if unk(v):
                return None
            out.append(-Fr(v) if d == "max" else Fr(v))
        return tuple(out)


# ------------------------------------------------------------------------------------------------ instance + solver
def effective(inst):
    opts = [dict(o) for o in inst["opts"]]
    return opts


def qualifiers(inst):
    ctx = inst["ctx"]
    return [i for i, o in enumerate(inst["opts"]) if all(tv(c.pred(), o, ctx) is True for c in inst["cons"])]


def fail_set(inst, i):
    ctx = inst["ctx"]
    o = inst["opts"][i]
    return frozenset(c.cid for c in inst["cons"] if tv(c.pred(), o, ctx) is not True)


def solve(inst):
    """Return (gold index or 'none', qualifier list) or (None, Q) when the item is not well defined."""
    Q = qualifiers(inst)
    tie = inst["tie"]
    if not Q:
        return ("none" if inst["none_opt"] else None), Q
    if tie is None:
        return (Q[0] if len(Q) == 1 else None), Q
    keys = [(tie.key(inst["opts"][i], inst["ctx"]), i) for i in Q]
    if any(k is None for k, _ in keys):
        return None, Q
    keys.sort()
    if len(keys) > 1 and keys[0][0] == keys[1][0]:
        return None, Q
    return keys[0][1], Q

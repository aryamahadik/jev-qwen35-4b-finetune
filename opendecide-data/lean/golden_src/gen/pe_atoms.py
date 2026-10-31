"""Facts and predicates for gen_policy_exceptions (CPU-only, deterministic, no model calls).

A *fact* is one thing the case notes state (a yes/no fact, a number, a category, a table key + value, a time of
day, a pair of numbers).  A *predicate* is one condition a policy can test about a fact ("the item is returned no
more than 30 days after purchase").  Several predicates may read the same fact (for example two money thresholds,
or "caused by flooding" and "caused by water" on the fact "cause of the damage").

Every label in the generator is computed from Pred.truth(value, params); the renderers only turn values and
params into text.  Surface choices are keyed hashes of a style seed (hk), so a fact-flip twin keeps every surface
choice except the text of the one fact that changed.
"""
import datetime as dt
from fractions import Fraction as Fr

from nd_common import MONTHS, NUMW, WEEKDAYS, hk


def pick(seq, *key):
    if isinstance(seq, str):
        return seq
    return seq[hk(*key) % len(seq)]


def plural(n, unit):
    one, many = unit
    return one if abs(n) == 1 else many


def money(v, cur="$"):
    v = Fr(v)
    if v.denominator == 1:
        return f"{cur}{int(v):,}"
    c = int(round(v * 100))
    return f"{cur}{c // 100:,}.{c % 100:02d}"


def numtxt(n, key, words=0.35):
    """Small whole numbers sometimes as words."""
    if isinstance(n, int) and 0 <= n <= 12 and (hk(*key, "w") % 1000) / 1000 < words:
        return NUMW[n]
    return f"{n:,}" if isinstance(n, int) else str(n)


def join_list(xs, conj="or"):
    xs = list(xs)
    if len(xs) == 1:
        return xs[0]
    if len(xs) == 2:
        return f"{xs[0]} {conj} {xs[1]}"
    return ", ".join(xs[:-1]) + f" {conj} " + xs[-1]


def fdate(d, st):
    """0 'March 3, 2026'; 1 '3 March 2026'; 2 'Tuesday, March 3, 2026'; 3 'Tue 3 Mar 2026'."""
    if st == 0:
        return f"{MONTHS[d.month - 1]} {d.day}, {d.year}"
    if st == 1:
        return f"{d.day} {MONTHS[d.month - 1]} {d.year}"
    if st == 2:
        return f"{WEEKDAYS[d.weekday()]}, {MONTHS[d.month - 1]} {d.day}, {d.year}"
    return f"{WEEKDAYS[d.weekday()][:3]} {d.day} {MONTHS[d.month - 1][:3]} {d.year}"


def base_date(*key):
    """A date in 2025-2028 chosen by hash (2028 is a leap year, so some spans cross February 29)."""
    start = dt.date(2025, 1, 5)
    return start + dt.timedelta(days=hk(*key, "d") % (365 * 4 - 40))


def fclock(m, st):
    m %= 1440
    h, mi = divmod(m, 60)
    if st == 1:
        return f"{h:02d}:{mi:02d}"
    suf = "a.m." if h < 12 else "p.m."
    return f"{h % 12 or 12}:{mi:02d} {suf}"


OPS = {"ge": lambda a, b: a >= b, "gt": lambda a, b: a > b, "le": lambda a, b: a <= b, "lt": lambda a, b: a < b}
NEG_OP = {"ge": "lt", "gt": "le", "le": "gt", "lt": "ge"}


# =================================================================================================== facts
class Fact:
    kind = "fact"

    def __init__(self, id, hide=True, req=None, binds=None, unk=None, q=None, distract=True, ev=None, order=0):
        self.id = id
        self.hide = hide          # may be stated as unknown
        self.req = req            # (pred_id, truth): only stated when that predicate has that truth value
        self.binds = binds        # ctx name this fact's value supplies (e.g. the item or the zone)
        self.unk = unk            # explicit "not known" sentences
        self.q = q                # "whether ..." / "how many ..." phrase for generic unknown sentences
        self.distract = distract and req is None and binds is None
        self.ev = ev              # (proposition if True, proposition if False) for conflicting-evidence rendering
        self.order = order

    def unknown(self, ctx, key):
        if self.unk:
            return pick(self.unk, *key, self.id, "unk").format(**ctx)
        q = self.q.format(**ctx)
        return pick(["The case notes do not say {q}.", "It is not recorded {q}.", "Nobody has yet established {q}.",
                     "The file is silent on {q}."], *key, self.id, "unkg").format(q=q)

    def sample(self, rng, pp):
        return rng.choice(self.values(pp))

    def bind(self, v):
        return v


class BoolFact(Fact):
    kind = "bool"

    def __init__(self, id, t, f, **kw):
        super().__init__(id, **kw)
        self.t, self.f = t, f

    def values(self, pp):
        return [True, False]

    def render(self, v, ctx, key):
        return pick(self.t if v else self.f, *key, self.id, v).format(**ctx)


class NumFact(Fact):
    """Integer value. Templates: {v} number, {vu} number + unit, {vm} money, {a}/{au} absolute value (negatives),
    {d1}/{d2} dates when `dates` templates are used (d2 = d1 + v days).  `zero` / `negt` override for 0 / < 0.
    `conv` (Fraction) = size of one fact unit in predicate units (e.g. miles -> km)."""
    kind = "num"

    def __init__(self, id, tmpl, unit=("day", "days"), money=False, lo=0, hi=None, zero=None, negt=None, dates=None,
                 date_share=0.4, conv=None, hours=False, far=True, one=None, minutes=False, extra=(), **kw):
        super().__init__(id, **kw)
        self.tmpl, self.unit, self.money, self.lo, self.hi = tmpl, unit, money, lo, hi
        self.zero, self.negt, self.dates, self.date_share, self.conv, self.hours = zero, negt, dates, date_share, conv, hours
        self.far, self.one, self.minutes, self.extra = far, one, minutes, tuple(extra)

    def values(self, pp):
        ts = [p["t"] for p in pp] or [10]
        out = set()
        for t in ts:
            if self.conv is not None:
                c = t / self.conv
                base = int(c)
                cand = {base - 2, base - 1, base, base + 1, base + 2, int(c * Fr(1, 2)), int(c * Fr(3, 2)) + 1}
                if (c).denominator == 1:
                    cand.add(int(c))
            else:
                step = max(2, t // 3) if self.far else 2
                cand = {t - 2, t - 1, t, t + 1, t + 2, t - step, t + step}
                if self.money:
                    cand |= {t // 2, t * 3 // 2, t * 2}
            out |= cand
        out |= set(self.extra)
        if self.lo is not None:
            out = {v for v in out if v >= self.lo}
        if self.hi is not None:
            out = {v for v in out if v <= self.hi}
        return sorted(out)

    def sample(self, rng, pp):
        vals = self.values(pp)
        if pp and rng.random() < 0.55:
            p = rng.choice(pp)
            t = p["t"] if self.conv is None else int(p["t"] / self.conv)
            near = [v for v in vals if abs(v - t) <= 1]
            if near:
                return rng.choice(near)
        return rng.choice(vals)

    def uses_dates(self, v, key):
        k = (*key, self.id)
        if v == 0 and self.zero or v < 0 and self.negt or (v == 1 and self.one):
            return False
        return bool(self.dates) and (hk(*k, "dt") % 1000) / 1000 < self.date_share

    def uses_days(self, v, key):
        return self.hours and v % 24 == 0 and v > 0 and hk(*key, self.id, "hd") % 2 == 0

    def render(self, v, ctx, key):
        cur = ctx.get("cur", "$")
        k = (*key, self.id)
        if self.uses_days(v, key):
            d = v // 24
            vu = f"{numtxt(d, k)} {plural(d, ('day', 'days'))}"
        elif self.minutes:
            h, mi = divmod(v, 60)
            vu = f"{h} {plural(h, ('hour', 'hours'))}" + (f" {mi} {plural(mi, ('minute', 'minutes'))}" if mi else "")
        elif self.money:
            vu = money(v, cur)
        else:
            vu = f"{numtxt(v, k)} {plural(v, self.unit)}"
        vv = money(v, cur) if self.money else numtxt(v, k)
        a = abs(v)
        au = f"{numtxt(a, k)} {plural(a, self.unit)}"
        if v == 0 and self.zero:
            tm = pick(self.zero, *k, "z")
        elif v < 0 and self.negt:
            tm = pick(self.negt, *k, "n")
        elif v == 1 and self.one:
            tm = pick(self.one, *k, "o")
        elif self.uses_dates(v, key):
            d1 = base_date(*key[:1], self.id)
            d2 = d1 + dt.timedelta(days=v)
            st = hk(*key[:1], "dst") % 4
            return pick(self.dates, *k, "dd").format(d1=fdate(d1, st), d2=fdate(d2, st), **ctx)
        else:
            tm = pick(self.tmpl, *k, "t")
        return tm.format(v=vv, vu=vu, vm=money(v, cur), a=numtxt(a, k), au=au, **ctx)


class CatFact(Fact):
    """Value = a display string; groups map a group name -> list of display strings."""
    kind = "cat"

    def __init__(self, id, groups, tmpl, bindmap=None, neutral=None, **kw):
        super().__init__(id, **kw)
        self.groups = groups
        self.gof = {d: g for g, ds in groups.items() for d in ds}
        self.tmpl = tmpl
        self.bindmap = bindmap
        self.neutral = neutral  # if set, values are limited to groups named by the policy + these groups

    def allowed_groups(self, pp):
        if self.neutral is None:
            return sorted(self.groups)
        gs = set(self.neutral)
        for p in pp:
            gs |= set(p.get("S") or p.get("fixed") or ())
        return sorted(gs)

    def values(self, pp):
        return [d for g in self.allowed_groups(pp) for d in self.groups[g]]

    def sample(self, rng, pp):
        g = rng.choice(self.allowed_groups(pp))
        if pp and rng.random() < 0.5:
            S = rng.choice(pp).get("S") or rng.choice(pp).get("fixed")
            if S:
                g = rng.choice(sorted(S))
        return rng.choice(self.groups[g])

    def render(self, v, ctx, key):
        if self.tmpl is None:
            return ""
        if isinstance(self.tmpl, dict):
            t = self.tmpl[self.gof[v]]
        else:
            t = self.tmpl
        return pick(t, *key, self.id, v).format(v=v, **ctx)

    def bind(self, v):
        return self.bindmap[v] if self.bindmap else v


class TableFact(Fact):
    """Value = [key, number]; the predicate owns the table (params['table'] = {key: limit})."""
    kind = "table"

    def __init__(self, id, tmpl, keys, **kw):
        super().__init__(id, **kw)
        self.tmpl, self.keys = tmpl, keys

    def values(self, pp):
        out = []
        for p in pp:
            for k, lim in p["table"].items():
                if k == "*":
                    for k2 in p["others"]:
                        out += [[k2, lim - 1], [k2, lim], [k2, lim + 1]]
                    continue
                for d in (-p["step"], 0, p["step"], -p.get("far", 2 * p["step"]), p.get("far", 2 * p["step"])):
                    if lim + d >= p.get("lo", 0):
                        out.append([k, lim + d])
        return out or [[k, 100] for k in self.keys]

    def sample(self, rng, pp):
        return list(rng.choice(self.values(pp)))

    def render(self, v, ctx, key):
        cur = ctx.get("cur", "$")
        return pick(self.tmpl, *key, self.id).format(k=v[0], x=v[1], xm=money(v[1], cur), **ctx)

    def bind(self, v):
        return v[0]


class RatioFact(Fact):
    """Value = [part, whole]."""
    kind = "ratio"

    def __init__(self, id, tmpl, wholes, money=True, **kw):
        super().__init__(id, **kw)
        self.tmpl, self.wholes, self.money = tmpl, wholes, money

    def values(self, pp):
        out = []
        for p in pp:
            t = p["t"]
            for b in self.wholes:
                a0 = Fr(t * b, 100)
                if a0.denominator != 1:
                    continue
                a0 = int(a0)
                for a in (a0 - max(1, b // 100), a0, a0 + max(1, b // 100), a0 // 2, min(b, a0 * 3 // 2)):
                    if 0 < a <= b:
                        out.append([a, b])
        return out or [[1, 2]]

    def sample(self, rng, pp):
        return list(rng.choice(self.values(pp)))

    def render(self, v, ctx, key):
        cur = ctx.get("cur", "$")
        a, b = v
        f = (lambda x: money(x, cur)) if self.money else (lambda x: f"{x:,}")
        return pick(self.tmpl, *key, self.id).format(a=f(a), b=f(b), **ctx)


class TimeFact(Fact):
    """Value = minutes after midnight (0..1439)."""
    kind = "time"

    def __init__(self, id, tmpl, **kw):
        super().__init__(id, **kw)
        self.tmpl = tmpl

    def values(self, pp):
        out = set()
        for p in pp:
            s, e = p["s"], p["e"]
            for x in (s - 1, s, s + 1, s - 20, s + 45, e - 1, e, e + 1, e + 30, e - 50, (s + e) // 2 if s < e else (s + 60)):
                out.add(x % 1440)
        return sorted(out) or [600]

    def sample(self, rng, pp):
        return rng.choice(self.values(pp))

    def render(self, v, ctx, key):
        st = hk(*key[:1], "clock") % 2
        return pick(self.tmpl, *key, self.id).format(tm=fclock(v, st), **ctx)


class PairFact(Fact):
    """Value = [x, y] (e.g. days requested, days left)."""
    kind = "pair"

    def __init__(self, id, tmpl, xs, ds, **kw):
        super().__init__(id, **kw)
        self.tmpl, self.xs, self.ds = tmpl, xs, ds

    def values(self, pp):
        return [[x, x + d] for x in self.xs for d in self.ds if x + d >= 2]

    def sample(self, rng, pp):
        return list(rng.choice(self.values(pp)))

    def render(self, v, ctx, key):
        k = (*key, self.id)
        return pick(self.tmpl, *k).format(x=numtxt(v[0], (*k, "x")), y=numtxt(v[1], (*k, "y")), **ctx)

    def bind(self, v):
        return v[0]


# =================================================================================================== predicates
class Pred:
    kind = "bool"
    tags = ()

    def __init__(self, id, fact, pos, neg, tags=(), guard=None):
        self.id, self.fact, self.pos, self.neg = id, fact, pos, neg
        self.tags = tuple(tags)
        self.guard = guard  # (pred_id, truth) that must be in the same clause / exception chain (child predicates)

    def params(self, rng):
        return {}

    def truth(self, v, p):
        return bool(v)

    def boundary(self, v, p):
        return False

    def fmt_args(self, p, ctx):
        return {}

    def phrase(self, p, positive, key, ctx):
        s = pick(self.pos if positive else self.neg, *key, self.id, positive)
        return s.format(**self.fmt_args(p, ctx), **ctx)

    def schedule(self, p, key, ctx):
        return None


class BoolPred(Pred):
    pass


class NumPred(Pred):
    kind = "num"

    def __init__(self, id, fact, op, ts, pos, neg, unit=("day", "days"), money=False, conv=None, hours=False, btol=1,
                 **kw):
        super().__init__(id, fact, pos, neg, **kw)
        self.op, self.ts, self.unit, self.money, self.conv, self.hours, self.btol = op, ts, unit, money, conv, hours, btol

    def params(self, rng):
        t = rng.choice(self.ts)
        p = {"t": t}
        if self.hours and t % 24 == 0 and rng.random() < 0.5:
            p["days"] = True
        return p

    def val(self, v):
        return Fr(v) * self.conv if self.conv is not None else Fr(v)

    def truth(self, v, p):
        return OPS[self.op](self.val(v), p["t"])

    def boundary(self, v, p):
        return abs(self.val(v) - p["t"]) <= self.btol

    def fmt_args(self, p, ctx):
        t = p["t"]
        cur = ctx.get("cur", "$")
        if self.hours and t % 24 == 0 and p.get("days"):
            tu = f"{t // 24} {plural(t // 24, ('day', 'days'))}"
        else:
            tu = f"{t:,} {plural(t, self.unit)}"
        return {"t": f"{t:,}", "tu": tu, "tm": money(t, cur)}


class InPred(Pred):
    """Category membership.  fixed=set of groups, or restrict pool + k -> S sampled per policy (listed inline or in
    a schedule)."""
    kind = "cat"

    def __init__(self, id, fact, pos, neg, fixed=None, restrict=None, k=(2, 3), sched=None, spos=None, sneg=None,
                 show=None, **kw):
        super().__init__(id, fact, pos, neg, **kw)
        self.fixed, self.restrict, self.k, self.sched, self.spos, self.sneg = fixed, restrict, k, sched, spos, sneg
        self.show = show  # group -> display name for lists

    def params(self, rng):
        if self.fixed:
            return {"fixed": sorted(self.fixed)}
        k = rng.randint(*self.k)
        S = sorted(rng.sample(self.restrict, k))
        return {"S": S, "sched": bool(self.sched) and rng.random() < 0.4}

    def groups(self, p):
        return p.get("S") or p.get("fixed")

    def truth(self, v, p):
        return self._gof(v) in self.groups(p)

    def _gof(self, v):
        return self._facts_gof[v]

    def fmt_args(self, p, ctx):
        names = [self.show.get(g, g) if self.show else g for g in self.groups(p)]
        return {"list_or": join_list(names, "or"), "list_and": join_list(names, "and"), "list": ", ".join(names),
                "sched": (self.sched or ("",))[0]}

    def phrase(self, p, positive, key, ctx):
        if p.get("sched") and self.spos:
            s = pick(self.spos if positive else self.sneg, *key, self.id, positive)
        else:
            s = pick(self.pos if positive else self.neg, *key, self.id, positive)
        return s.format(**self.fmt_args(p, ctx), **ctx)

    def schedule(self, p, key, ctx):
        if not p.get("sched"):
            return None
        title, what = self.sched
        items = []
        fact_groups = self._facts_groups
        for g in self.groups(p):
            shown_g = self.show.get(g, g) if self.show else g
            items.append(f"- {shown_g}" + (
                f" (for example: {', '.join(fact_groups[g][:2])})" if hk(*key, self.id, 'ex') % 3 == 0 and fact_groups[g] != [shown_g] else ""))
        return f"{title} - {what}:\n" + "\n".join(items)


class TablePred(Pred):
    """value [key, x]; truth: x OP table[key] (key missing -> the '*' row if present).  Table rendered as a
    schedule block."""
    kind = "table"

    def __init__(self, id, fact, op, pos, neg, keys, lims, nrows=(3, 5), step=1, title=None, cols=None, star=None,
                 money=False, lo=0, far=None, **kw):
        super().__init__(id, fact, pos, neg, **kw)
        self.op, self.keys, self.lims, self.nrows, self.step, self.title, self.cols = op, keys, lims, nrows, step, title, cols
        self.star, self.money, self.lo, self.far = star, money, lo, (far if far is not None else 2 * step)

    def params(self, rng):
        n = rng.randint(*self.nrows)
        ks = rng.sample(self.keys, n + (2 if self.star else 0))
        rows, others = ks[:n], ks[n:]
        table = {k: rng.choice(self.lims) for k in rows}
        p = {"table": table, "step": self.step, "lo": self.lo, "others": [], "far": self.far}
        if self.star and rng.random() < 0.5:
            table["*"] = rng.choice(self.lims)
            p["others"] = others
        return p

    def lim(self, k, p):
        t = p["table"]
        return t[k] if k in t else t.get("*")

    def truth(self, v, p):
        lim = self.lim(v[0], p)
        assert lim is not None, (self.id, v, p)
        return OPS[self.op](v[1], lim)

    def boundary(self, v, p):
        lim = self.lim(v[0], p)
        return lim is not None and abs(v[1] - lim) <= self.step

    def schedule(self, p, key, ctx):
        cur = ctx.get("cur", "$")
        title = self.title
        lines = [f"{title}", f"{self.cols[0]} | {self.cols[1]}"]
        for k, lim in p["table"].items():
            if k == "*":
                continue
            lines.append(f"{k} | {money(lim, cur) if self.money else lim}")
        if "*" in p["table"]:
            lim = p["table"]["*"]
            lines.append(f"{self.star} | {money(lim, cur) if self.money else lim}")
        return "\n".join(lines)


class RatioPred(Pred):
    kind = "ratio"

    def __init__(self, id, fact, op, ts, pos, neg, **kw):
        super().__init__(id, fact, pos, neg, **kw)
        self.op, self.ts = op, ts

    def params(self, rng):
        return {"t": rng.choice(self.ts)}

    def truth(self, v, p):
        a, b = v
        return OPS[self.op](Fr(a * 100, b), p["t"])

    def boundary(self, v, p):
        a, b = v
        return abs(Fr(a * 100, b) - p["t"]) <= 1

    def fmt_args(self, p, ctx):
        return {"t": f"{p['t']}"}


class TimePred(Pred):
    """Inclusive window [s, e]; e < s means the window runs past midnight."""
    kind = "time"

    def __init__(self, id, fact, windows, pos, neg, **kw):
        super().__init__(id, fact, pos, neg, **kw)
        self.windows = windows

    def params(self, rng):
        s, e = rng.choice(self.windows)
        return {"s": s, "e": e}

    def truth(self, v, p):
        s, e = p["s"], p["e"]
        return s <= v <= e if s <= e else (v >= s or v <= e)

    def boundary(self, v, p):
        return min(abs(v - p["s"]), abs(v - p["e"])) <= 1

    def fmt_args(self, p, ctx):
        st = ctx.get("_clock", 0)
        return {"s": fclock(p["s"], st), "e": fclock(p["e"], st)}


class PairPred(Pred):
    """[x, y]: truth x <= y (e.g. days requested <= days left)."""
    kind = "pair"

    def truth(self, v, p):
        return v[0] <= v[1]

    def boundary(self, v, p):
        return abs(v[1] - v[0]) <= 1


# =================================================================================================== literals
def lit(s):
    """'pred+' -> ('pred', True); 'pred-' -> ('pred', False)."""
    s = s.strip()
    assert s[-1] in "+-", s
    return (s[:-1], s[-1] == "+")


def seed_lits(s):
    return [lit(x) for x in s.split("&")]


def lkey(l):
    return l[0] + ("+" if l[1] else "-")


def neg(l):
    return (l[0], not l[1])

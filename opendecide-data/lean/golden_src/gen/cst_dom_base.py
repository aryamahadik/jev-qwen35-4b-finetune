"""Domain container and reusable requirement builders for gen_constraints."""
import datetime as dt
from fractions import Fraction as Fr

from cst_core import (GE, GT, LE, LT, MISSING, NA, Attr, BoolCon, CatCon, CmpCon, FnCon, SetCon, Tie, cap,
                      fmt_money, fmt_time, lex_word, modal, unk)

FIRST = ["Priya", "Daniel", "Amara", "Tomas", "Mei", "Jonah", "Fatima", "Lucas", "Ingrid", "Kwame", "Sofia", "Ravi",
         "Hannah", "Mateo", "Aisha", "Oliver", "Yuki", "Grace", "Omar", "Elena", "Samuel", "Nadia", "Marcus", "Leila",
         "Ethan", "Zara", "Diego", "Chloe", "Tariq", "Ruth", "Kenji", "Maya", "Felix", "Imani", "Noah", "Anika", "Pablo",
         "Esther", "Hugo", "Sana", "Victor", "Lena", "Andre", "Keiko", "Jamal", "Freya", "Arjun", "Beatriz", "Colin",
         "Dalia", "Emeka", "Farah", "Gideon", "Hye-jin", "Ivan", "Julia", "Kofi", "Lucia", "Moses", "Nora"]
LAST = ["Okafor", "Lindqvist", "Patel", "Moreau", "Tanaka", "Haddad", "Novak", "Castillo", "Mensah", "Brennan",
        "Rossi", "Kowalski", "Nguyen", "Adeyemi", "Fischer", "Silva", "Kim", "Duarte", "Osei", "Larsen", "Varga",
        "Chen", "Abara", "Holm", "Ibarra", "Jansen", "Khan", "Lopez", "Murphy", "Nakamura", "Olsen", "Pereira",
        "Quinn", "Reyes", "Sato", "Torres", "Ueda", "Vance", "Walsh", "Yilmaz"]
# fixed full-name pool (labels for person-valued options); deterministic
PEOPLE = []
for i in range(96):
    PEOPLE.append(f"{FIRST[(i * 7) % len(FIRST)]} {LAST[(i * 11 + i // len(FIRST)) % len(LAST)]}")
PEOPLE = list(dict.fromkeys(PEOPLE))


class Domain:
    def __init__(self, key, noun, plural, head, labels, attrs, makers, ties, ctx_fn, contexts, questions,
                 intros=(), subjects=(), def_extra="", letters=False, valid=None, derive=None, none_label=None,
                 hv=None, orgs=(), weight=1.0, min_cons=2, nice=(), cs=None, always=(), cur=None, label_fn=None,
                 required=(), no_distract=()):
        self.key, self.noun, self.plural, self.head = key, noun, plural, head
        self.labels = list(labels)
        assert len(set(self.labels)) == len(self.labels), key
        self.attrs = list(attrs)
        self.A = {a.key: a for a in self.attrs}
        self.makers = list(makers)  # (weight, group, fn(rng, ctx, D) -> Con | None)
        self.ties = list(ties)  # fn(rng, ctx, D) -> Tie | None
        self.ctx_fn = ctx_fn
        self.contexts, self.questions = list(contexts), list(questions)
        self.intros, self.subjects = list(intros), list(subjects)
        self.def_extra, self.letters = def_extra, letters
        self._valid, self._derive = valid, derive
        self.none_label = none_label or f"none of the listed {plural}"
        self.hv = hv  # fn(ctx) -> dict of header placeholders
        self.orgs = list(orgs)
        self.weight, self.min_cons = weight, min_cons
        self.nice = list(nice)  # bool attrs usable as a stated nice-to-have
        self._cs = cs  # fn(ctx, st) -> dict of strings for context / question templates
        self.always = list(always)  # attrs always shown (e.g. departure and arrival times)
        self.cur_fixed = cur
        self.label_fn = label_fn  # fn(rng, ctx, n) -> labels for one item (default: sample from labels)
        self.required = list(required)  # requirement groups every item includes (the context always implies them)
        self.no_distract = set(no_distract)  # attrs shown only when a requirement uses them

    def cs(self, ctx, st):
        d = {k: v for k, v in ctx.items() if isinstance(v, str)}
        if self._cs:
            d.update(self._cs(ctx, st))
        return d

    def derive(self, o, ctx):
        if self._derive:
            self._derive(o, ctx)

    def valid(self, o, ctx):
        for a in self.attrs:
            if a.derived or a.key not in o:
                continue
            v = o[a.key]
            if unk(v):
                continue
            if a.kind in ("money", "num", "dur", "time") and a.lo is not None and a.hi is not None:
                if getattr(a, "special", None) and v in a.special:
                    continue
                if not (a.lo <= v <= a.hi):
                    return False
        return self._valid(o, ctx) if self._valid else True


def grid(rng, a, lo=None, hi=None):
    """A value on attribute a's generation grid within [lo, hi]."""
    lo = a.lo if lo is None else lo
    hi = a.hi if hi is None else hi
    i0 = -(-(lo - a.lo) // a.step)
    i1 = (hi - a.lo) // a.step
    return a.lo + a.step * rng.randint(i0, i1)


def frac_range(a, f0, f1):
    span = a.hi - a.lo
    return a.lo + int(span * f0), a.lo + int(span * f1)


# ------------------------------------------------------------------------------------------------ simple makers
def mk_cmp(key, op, f0=0.3, f1=0.7, strict_p=0.2, neg_p=0.15, vp=None, cid=None, tlo=None, thi=None, tstep=None,
           **kw):
    """Threshold requirement on attribute `key`; op is LE (max) or GE (min); strict variants LT / GT.
    tlo/thi/tstep give an explicit threshold grid (needed for derived attributes)."""
    def f(rng, ctx, D):
        a = D.A[key]
        if tlo is not None:
            thr = tlo + tstep * rng.randint(0, (thi - tlo) // tstep)
        else:
            lo, hi = frac_range(a, f0, f1)
            thr = grid(rng, a, lo, hi)
        o = op
        if rng.random() < strict_p:
            o = LT if op == LE else GT
        pol = "neg" if o in (LE, GE) and rng.random() < neg_p else "pos"
        return CmpCon(cid or key, a, o, thr, pol, wi=rng.randrange(12), vpi=rng.randrange(12), vp=vp, **kw)
    return f


def mk_bool(key, want=True, dneg_p=0.15, anti_p=0.35, vpf=None):
    def f(rng, ctx, D):
        a = D.A[key]
        if want:
            form = "dneg" if (a.noun and rng.random() < dneg_p) else "pos"
        else:
            form = "anti" if (a.anti and rng.random() < anti_p) else "neg"
        return BoolCon(key, a, want, form, vpi=rng.randrange(12), vps=vpf(ctx) if vpf else None)
    return f


def mk_date(key, op, d0, d1, ref="today", strict_p=0.15, neg_p=0.15, vp=None, cid=None, **kw):
    """Date threshold = ctx[ref] + d0..d1 days."""
    def f(rng, ctx, D):
        a = D.A[key]
        thr = ctx[ref] + rng.randint(d0, d1)
        o = op
        if rng.random() < strict_p:
            o = LT if op == LE else GT
        pol = "neg" if o in (LE, GE) and rng.random() < neg_p else "pos"
        return CmpCon(cid or key, a, o, thr, pol, wi=rng.randrange(12), vpi=rng.randrange(12), vp=vp, **kw)
    return f


def mk_cat(key, k=(1, 2), neg_p=0.3, only_neg=False, only_pos=False):
    def f(rng, ctx, D):
        a = D.A[key]
        neg = only_neg or (not only_pos and rng.random() < neg_p)
        n = rng.randint(*k)
        n = min(n, len(a.cats) - 1)
        vals = rng.sample(a.cats, n)
        vals = [c for c in a.cats if c in vals]
        return CatCon(key, a, vals, neg, vpi=rng.randrange(12))
    return f


def mk_set(key, modes=("has", "all", "k"), w=(5, 3, 2), pool_fn=None):
    def f(rng, ctx, D):
        a = D.A[key]
        pool = pool_fn(ctx) if pool_fn else a.items
        mode = rng.choices(modes, weights=w)[0]
        if mode in ("has", "lacks"):
            items = [rng.choice(pool)]
            k = 1
        elif mode == "all":
            items = rng.sample(pool, 2 if rng.random() < 0.75 else 3)
            k = len(items)
        else:
            items = rng.sample(pool, 3 if rng.random() < 0.7 else 4)
            k = 2 if len(items) == 3 else rng.choice([2, 3])
        items = [x for x in pool if x in items]
        c = SetCon(key, a, mode, items, k, vpi=rng.randrange(12))
        c.pool = pool
        return c
    return f


# ------------------------------------------------------------------------------------------------ compound builders
def mk_exc(key, flag, op, flag_clause, alt_words=("is acceptable", "is enough", "will do"), f0=0.35, f1=0.7,
           gap=(1, 3), vp=None):
    """<attr op T_main>, unless <flag>, in which case <attr op T_alt> (T_alt looser)."""
    def f(rng, ctx, D):
        a, b = D.A[key], D.A[flag]
        fc = flag_clause(ctx) if callable(flag_clause) else flag_clause
        lo, hi = frac_range(a, f0, f1)
        t1 = grid(rng, a, lo, hi)
        g = rng.randint(*gap) * a.step
        t2 = t1 - g if op == GE else t1 + g
        if not (a.lo <= t2 <= a.hi):
            return None
        wi, vpi, ai = rng.randrange(12), rng.randrange(12), rng.randrange(12)
        vps = vp or a.vp

        def build(p):
            main = ("cmp", ("a", key), op, ("k", p["t1"]))
            alt = ("cmp", ("a", key), op, ("k", p["t2"]))
            return ("or", main, ("and", ("bool", ("a", flag), True), alt)), [(key, p["t1"] + d * a.step) for d in (-1, 0, 1)] + [(key, p["t2"] + d * a.step) for d in (-1, 0, 1)]

        def text(p, st, mi):
            w1 = lex_word(a.cls, op, "pos", wi)
            w2 = lex_word(a.cls, op, "pos", 4 if (op == LE and a.cls in ("amount", "count")) else (wi if op == GE else 0))
            v1, v2 = a.fmt(p["t1"], st), a.fmt(p["t2"], st)
            main = vps[vpi % len(vps)].format(c=w1, v=v1)
            s = f"{modal('pos', mi)} {main}, unless {fc}, in which case {w2} {v2} {alt_words[ai % len(alt_words)]}"
            return {"inline": s, "bullet": cap(s) + ".", "field": None, "compound": True}

        def vary(p, rng2):
            out = []
            for d in (1, 2, 3, -1, -2, -3):
                for which in ("t1", "t2"):
                    q = dict(p)
                    q[which] = p[which] + d * a.step
                    if not (a.lo <= q[which] <= a.hi):
                        continue
                    if (op == GE and q["t2"] >= q["t1"]) or (op == LE and q["t2"] <= q["t1"]):
                        continue
                    out.append(q)
            return out

        def chk(p, st):
            return [("cmp", a.cls, op, "pos", a.fmt(p["t1"], st)), ("cmp", a.cls, op, "pos", a.fmt(p["t2"], st)),
                    ("unless",)]
        tags = {"exception", "numeric" if a.kind != "time" else "temporal"}
        return FnCon(key, [key, flag], {"t1": t1, "t2": t2}, build, text, vary, chk, tags=tags, group=key,
                     mscale=a.step)
    return f


def mk_cond(if_key, if_pred, if_clause, then_key, op, f0=0.3, f1=0.7, then_vp=None, group=None, cid=None,
            then_bool=None):
    """If <option condition>, then <threshold requirement> (or a bool requirement when then_bool is set)."""
    def f(rng, ctx, D):
        b = D.A[then_key]
        if then_bool is not None:
            t = None
        else:
            lo, hi = frac_range(b, f0, f1)
            t = grid(rng, b, lo, hi)
        wi, vpi, form = rng.randrange(12), rng.randrange(12), rng.random()

        def build(p):
            if then_bool is not None:
                th = ("bool", ("a", then_key), then_bool)
                foc = []
            else:
                th = ("cmp", ("a", then_key), op, ("k", p["t"]))
                foc = [(then_key, p["t"] + d * b.step) for d in (-1, 0, 1)]
            return ("imp", if_pred, th), foc

        def text(p, st, mi):
            if then_bool is not None:
                vps = then_vp or b.vp
                vp = vps[vpi % len(vps)]
                s_then = f"{modal('pos' if then_bool else 'neg', mi)} {vp}"
            else:
                vps = then_vp or b.vp
                s_then = f"{modal('pos', mi)} {vps[vpi % len(vps)].format(c=lex_word(b.cls, op, 'pos', wi), v=b.fmt(p['t'], st))}"
            if form < 0.6:
                s = f"If {if_clause}, it {s_then}."
            else:
                s = f"Where {if_clause}, it {s_then}."
            return {"inline": s[0].lower() + s[1:-1], "bullet": s, "field": None, "compound": True, "sentence": s}

        def vary(p, rng2):
            if then_bool is not None:
                return []
            out = []
            for d in (1, 2, 3, 4, -1, -2, -3, -4):
                q = {"t": p["t"] + d * b.step}
                if b.lo <= q["t"] <= b.hi:
                    out.append(q)
            return out

        def chk(p, st):
            if then_bool is not None:
                return [("if",)]
            return [("cmp", b.cls, op, "pos", b.fmt(p["t"], st)), ("if",)]
        tags = set()
        if then_bool is None:
            tags.add("temporal" if b.kind in ("time", "date") else "numeric")
        return FnCon(cid or then_key, [if_key, then_key], {"t": t}, build, text, vary, chk, tags=tags,
                     group=group or then_key, mscale=b.step)
    return f


def mk_window(from_key, to_key, ctx_start, ctx_end, sent_tpls, req_tpls, shift_step=15, what="the meeting"):
    """Option availability [from, to] must cover the required window [start, end] given in the context."""
    def f(rng, ctx, D):
        s, e = ctx[ctx_start], ctx[ctx_end]
        si, ri = rng.randrange(12), rng.randrange(12)

        def build(p):
            return ("and", ("cmp", ("a", from_key), LE, ("k", p["s"])), ("cmp", ("a", to_key), GE, ("k", p["e"]))), \
                [(from_key, p["s"] + d * 15) for d in (-1, 0, 1)] + [(to_key, p["e"] + d * 15) for d in (-1, 0, 1)]

        def text(p, st, mi):
            r = req_tpls[ri % len(req_tpls)]
            s2 = f"{modal('pos', mi)} {r}"
            return {"inline": s2, "bullet": cap(s2) + ".", "field": None}

        def ctxs(p, st):
            return sent_tpls[si % len(sent_tpls)].format(s=fmt_time(p["s"], st["time"]), e=fmt_time(p["e"], st["time"]))

        def vary(p, rng2):
            out = []
            for d in (1, 2, 3, 4, -1, -2, -3, -4):
                q = {"s": p["s"] + d * shift_step, "e": p["e"] + d * shift_step}
                if 6 * 60 <= q["s"] and q["e"] <= 22 * 60:
                    out.append(q)
            return out

        def chk(p, st):
            return [("window", fmt_time(p["s"], st["time"]), fmt_time(p["e"], st["time"]))]
        return FnCon("window", [from_key, to_key], {"s": s, "e": e}, build, text, vary, chk,
                     tags={"temporal", "implicit"}, group="window", mscale=15, ctxs=ctxs)
    return f


def mk_range(lo_key, hi_key, value_fn, sent_fn, req_tpls, step=1, vary_d=(1, 2, 3, -1, -2, -3), cid="range",
             tags=("numeric", "implicit")):
    """The context value must lie inside the option's accepted range [lo, hi] (inclusive)."""
    def f(rng, ctx, D):
        x = value_fn(rng, ctx, D)
        if x is None:
            return None
        ri = rng.randrange(12)

        def build(p):
            return ("and", ("cmp", ("a", lo_key), LE, ("k", p["x"])), ("cmp", ("a", hi_key), GE, ("k", p["x"]))), \
                [(lo_key, p["x"] + d * step) for d in (-1, 0, 1)] + [(hi_key, p["x"] + d * step) for d in (-1, 0, 1)]

        def text(p, st, mi):
            s2 = f"{modal('pos', mi)} {req_tpls[ri % len(req_tpls)]}"
            return {"inline": s2, "bullet": cap(s2) + ".", "field": None}

        def ctxs(p, st):
            return sent_fn(p["x"], st)

        def vary(p, rng2):
            return [{"x": p["x"] + d * step} for d in vary_d if p["x"] + d * step > 0]

        def chk(p, st):
            return [("implicit_ctx",)]
        return FnCon(cid, [lo_key, hi_key], {"x": x}, build, text, vary, chk, tags=set(tags), group=cid,
                     mscale=step, ctxs=ctxs)
    return f


def mk_xunit(key, op, disp_unit, factor, alt_factor, disp_vals, vp_tpls, note_tpl, cid=None, group=None,
             dec=1):
    """Threshold stated in another unit: the listed values are in the attribute's unit, the requirement in
    disp_unit; value_in_attr_unit = shown_value * factor (stated in the note).  Thresholds are chosen so the verdict
    for every generated value is the same under alt_factor (the exact conversion)."""
    def f(rng, ctx, D):
        a = D.A[key]
        dv = rng.choice(disp_vals)
        wi, vpi = rng.randrange(12), rng.randrange(12)
        pol = "pos"

        def thr(p, fac):
            return Fr(p["d"]) / (10 ** dec) * fac

        def build(p):
            t = thr(p, factor)
            return ("cmp", ("conv", ("a", key), Fr(1)), op, ("k", t)), []

        def dstr(p):
            v = p["d"]
            s = f"{v // 10 ** dec:,}" + (f".{v % 10 ** dec:0{dec}d}" if dec and v % 10 ** dec else "")
            return f"{s} {disp_unit}"

        def text(p, st, mi):
            w = lex_word(a.cls, op, pol, wi)
            vp = vp_tpls[vpi % len(vp_tpls)].format(c=w, v=dstr(p))
            s2 = f"{modal(pol, mi)} {vp} {note_tpl}"
            return {"inline": s2, "bullet": cap(s2) + ".", "field": None}

        def vary(p, rng2):
            return [{"d": x} for x in disp_vals if x != p["d"]]

        def chk(p, st):
            return [("cmp", a.cls, op, pol, dstr(p)), ("xunit", note_tpl)]
        c = FnCon(cid or key, [key], {"d": dv}, build, text, vary, chk, tags={"units", "numeric"},
                  group=group or key, mscale=a.step)
        c.xunit = (key, op, factor, alt_factor, dec)
        return c
    return f


def mk_derived(cid, attrs, expr_fn, op, thr_fn, vp_tpls, vfmt, ctx_fn=None, step=100, tags=("numeric", "multi_hop"),
               group=None, wset=None, vd=(1, 2, 3, 5, 8, -1, -2, -3, -5, -8), cls="amount", neg_p=0.1):
    """Requirement on a computed quantity (totals, dates after business days, yearly cost ...).
    expr_fn(ctx) -> expression; thr_fn(rng, ctx, D) -> threshold (same unit as the expression)."""
    def f(rng, ctx, D):
        t = thr_fn(rng, ctx, D)
        if t is None:
            return None
        e = expr_fn(ctx)
        wi, vpi, ci = rng.randrange(12), rng.randrange(12), rng.randrange(12)
        o = op
        pol = "neg" if o in (LE, GE) and rng.random() < neg_p else "pos"
        if wset is not None:
            wi = rng.choice(wset)

        def build(p):
            return ("cmp", e, o, ("k", p["t"])), []

        def text(p, st, mi):
            w = lex_word(cls, o, pol, wi)
            vp = vp_tpls[vpi % len(vp_tpls)].format(c=w, v=vfmt(p["t"], st))
            s2 = f"{modal(pol, mi)} {vp}"
            return {"inline": s2, "bullet": cap(s2) + ".", "field": None}

        def ctxs(p, st):
            return ctx_fn(ctx, st, ci) if ctx_fn else None

        def vary(p, rng2):
            return [{"t": p["t"] + d * step} for d in vd if p["t"] + d * step > 0]

        def chk(p, st):
            return [("cmp", cls, o, pol, vfmt(p["t"], st))]
        tg = set(tags)
        if pol == "neg":
            tg.add("negation")
        return FnCon(cid, attrs, {"t": t}, build, text, vary, chk, tags=tg, group=group or cid, mscale=step,
                     ctxs=ctxs if ctx_fn else None)
    return f


# ------------------------------------------------------------------------------------------------ tie-breaks
TIE_TPL = ["If more than one {noun} meets every requirement, choose the one with {np}.",
           "If several {plural} qualify, pick the one with {np}.",
           "Where two or more {plural} meet all of these, go with the one that has {np}.",
           "Tie-break if more than one works: {np}.",
           "Should more than one {noun} pass every check, the one with {np} wins."]


def mk_implicit(key, op, thr_fn, sent_fn, vp_text, cid=None, vfmt=None, group=None):
    """Requirement whose threshold comes from a context fact (party size, item value, applicant's score ...).
    sent_fn(rng, ctx, thr) -> (sentence with {v} for the formatted threshold, names or None).  With names the
    sentence lists them instead of giving the number (the reader must count; the requirement cannot be varied)."""
    def f(rng, ctx, D):
        a = D.A[key]
        thr = thr_fn(rng, ctx, D)
        if thr is None:
            return None
        sent, names = sent_fn(rng, ctx, thr)
        c = CmpCon(cid or key, a, op, thr, "pos", implicit=(sent, vp_text), vfmt=vfmt, group=group)
        if names:
            c.names = list(names)
            c.fixed = True
            c.tags.add("multi_hop")
        return c
    return f


def mk_tie(tid, keys, np, attrs, tags=()):
    def f(rng, ctx, D):
        return Tie(tid, keys, [t.format(noun=D.noun, plural=D.plural, np=np) for t in TIE_TPL], np, attrs, tags)
    return f


def money_fmt(cur=None, cents=False):
    return lambda v, st: fmt_money(v, cur or st["cur"], cents)


def ordn(d):
    return d.toordinal()


def date_of(o):
    return dt.date.fromordinal(o)

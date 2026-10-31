"""rt_core: machinery for gen_routing (ticket / request routing under an explicit routing policy).

A domain (rt_dom_*.py) declares
  * issue kinds: what a requester can need, with typed facts (params) and Claude-written sentence templates;
  * queues: name, a base rank, a one-sentence definition template and a declarative rule
        when   = alternatives A(kinds, *conds)       (the queue covers an issue if ANY alternative matches)
        unless = alternatives A(kinds, *conds)       (exception: a matching issue is NOT covered)
    a cond is (lhs, op, rhs): lhs = issue param name or 'ctx.<name>', rhs = literal or '$<threshold name>';
    an unstated fact (None) never satisfies a condition;
  * a catch-all queue that takes a request only when no other listed queue covers any open issue.
A policy variant fixes the thresholds, the priority order (base rank + jitter) and the priority notation.
The gold queue of a request = the applicable queue (over the OPEN issues) with the best priority, else the catch-all.
"""
import datetime as dt
import hashlib
import random
import re
from fractions import Fraction as Fr


def hseed(*a):
    return int.from_bytes(hashlib.sha256("\x1f".join(map(str, a)).encode()).digest()[:8], "big")


def R(*a):
    return random.Random(hseed(*a))


MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]
NUMW = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"]


def cap(s):
    return s[:1].upper() + s[1:] if s else s


def lcfirst(s):
    w = s.split(" ", 1)[0]
    if w in ("I", "I'm", "I've", "I'd", "I'll") or w[:1].isdigit() or (len(w) > 1 and w.isupper()) or w[:1] in "\"'(":
        return s
    return s[:1].lower() + s[1:]


def fmoney(x, sty=0):
    x = round(float(x), 2)
    whole = abs(x - round(x)) < 1e-9
    if whole and sty % 3 == 1:
        return f"${int(round(x)):,}"
    return f"${x:,.2f}"


def fdate(d, sty=0, today=None):
    y = "" if (today is not None and d.year == today.year and sty % 4 != 3) else f", {d.year}"
    s = sty % 4
    if s == 0:
        return f"{MONTHS[d.month - 1]} {d.day}{y}"
    if s == 1:
        return f"{d.day} {MONTHS[d.month - 1]}" + (f" {d.year}" if y else "")
    if s == 2:
        return f"{MONTHS[d.month - 1][:3]} {d.day}{y}"
    return f"{MONTHS[d.month - 1]} {d.day}, {d.year}"


def ftime(m, sty=0):
    h, mi = divmod(int(m) % 1440, 60)
    if sty % 3 == 0:
        return f"{h:02d}:{mi:02d}"
    ap = "a.m." if h < 12 else "p.m."
    if sty % 3 == 2:
        ap = "am" if h < 12 else "pm"
    h12 = h % 12 or 12
    return f"{h12}:{mi:02d} {ap}"


def numw(n):
    return NUMW[n] if 0 <= n < len(NUMW) else str(n)


# ============================================================================================= params
UNIT = {  # display unit -> (canonical unit, factor)  canonical = q * factor
    "kg": ("kg", Fr(1)), "lb": ("kg", Fr(45359237, 100000000)), "g": ("kg", Fr(1, 1000)),
    "km": ("km", Fr(1)), "mi": ("km", Fr(1609344, 1000000)),
    "cm": ("cm", Fr(1)), "in": ("cm", Fr(254, 100)), "m": ("cm", Fr(100)), "ft": ("cm", Fr(3048, 100)),
    "L": ("L", Fr(1)), "gal": ("L", Fr(3785411784, 1000000000)),
    "C": ("C", None), "F": ("C", None),
    "h": ("h", Fr(1)), "min": ("h", Fr(1, 60)), "d": ("h", Fr(24)),
    "GB": ("GB", Fr(1)), "MB": ("GB", Fr(1, 1000)), "TB": ("GB", Fr(1000)),
}
UNAME = {"kg": ("kg", "kg"), "lb": ("lb", "lb"), "g": ("g", "g"), "km": ("km", "km"), "mi": ("mile", "miles"),
         "cm": ("cm", "cm"), "in": ("inch", "inches"), "m": ("metre", "metres"), "ft": ("foot", "feet"),
         "L": ("litre", "litres"), "gal": ("gallon", "gallons"), "C": ("°C", "°C"), "F": ("°F", "°F"),
         "h": ("hour", "hours"), "min": ("minute", "minutes"), "d": ("day", "days"),
         "GB": ("GB", "GB"), "MB": ("MB", "MB"), "TB": ("TB", "TB")}


def canon(v):
    """Canonical exact number for a param value (Fraction), or None."""
    if v is None:
        return None
    if isinstance(v, dict):
        q, u = Fr(str(v["q"])), v["u"]
        if u == "C":
            return q
        if u == "F":
            return (q - 32) * Fr(5, 9)
        return q * UNIT[u][1]
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return Fr(str(v))
    return v


def fqty(v):
    q, u = v["q"], v["u"]
    qs = f"{q:g}" if isinstance(q, float) else str(q)
    if u in ("C", "F"):
        return f"{qs}{UNAME[u][1]}"
    one, many = UNAME[u]
    if u in ("kg", "lb", "g", "km", "cm", "L", "GB", "MB", "TB"):
        return f"{qs} {one}"
    return f"{qs} {one if q == 1 else many}"


class P:
    """A typed fact of an issue (or of the request context).
    kind: bool | cat | int | money | days | tod | qty
    T/F (bool) or txt (dict value -> templates, for cat; list of templates for numeric kinds).
    Numeric templates use {n} (int), {nw} (number word), {amt} (money), {ago}/{date} (days), {time} (tod), {q} (qty).
    thr: threshold names in the policy variant to sample near; unk: probability the fact is left unstated."""

    def __init__(self, kind, T=None, F=None, txt=None, w=None, lo=None, hi=None, thr=(), near=0.6, unk=0.0,
                 unk_txt=("",), rel=None, absd=None, units=None, quant=False, p=0.5, deltas=None, hidden=False):
        self.kind, self.T, self.F, self.txt, self.w = kind, T, F, txt, w
        self.lo, self.hi, self.thr, self.near, self.unk, self.unk_txt = lo, hi, tuple(thr), near, unk, list(unk_txt)
        self.rel, self.absd, self.units, self.quant, self.p, self.deltas = rel, absd, units, quant, p, deltas
        self.hidden = hidden  # a context fact that only restricts which issues can co-occur (never rendered, never flipped)
        if kind == "cat":
            assert isinstance(txt, dict) and txt
        if kind == "bool":
            assert T is not None and F is not None

    # ------------------------------------------------------------------ sampling
    def thr_vals(self, V):
        out = []
        for t in self.thr:
            x = V[t]
            out.append(x)
        return out

    def sample(self, rng, V):
        if self.unk and rng.random() < self.unk:
            return None
        k = self.kind
        if k == "bool":
            return rng.random() < self.p
        if k == "cat":
            vals = list(self.txt)
            w = [self.w.get(v, 1.0) if self.w else 1.0 for v in vals]
            return rng.choices(vals, w)[0]
        tv = self.thr_vals(V)
        if k == "qty":
            u = rng.choice(self.units)
            lo, hi = self.lo[u], self.hi[u]
            if tv and rng.random() < self.near:
                t = rng.choice(tv)
                q = self._near_units(t, u, rng)
            else:
                q = rng.randint(lo, hi)
            return {"q": max(lo, min(hi, q)), "u": u}
        if tv and rng.random() < self.near:
            t = rng.choice(tv)
            d = rng.choice(self.deltas or DELTAS[k])
            x = t + d
        elif k == "money":
            x = rng.choice([rng.randint(self.lo, self.hi), rng.randint(self.lo * 100, self.hi * 100) / 100])
        else:
            x = rng.randint(self.lo, self.hi)
        x = max(self.lo, min(self.hi, x))
        return round(x, 2) if k == "money" else int(x)

    def _near_units(self, t, u, rng):
        cu, f = UNIT[u]
        if u == "C":
            base = Fr(t)
        elif u == "F":
            base = Fr(t) * Fr(9, 5) + 32
        else:
            base = Fr(t) / f
        fl = int(base)
        return rng.choice([fl - 1, fl, fl + 1, fl + 2] if base != fl else [fl - 1, fl, fl, fl + 1])

    def alts(self, v, V, rng):
        """Candidate replacement values for a fact-flip twin (deterministic order)."""
        k = self.kind
        out = []
        if k == "bool":
            out = [not v] if v is not None else [True, False]
        elif k == "cat":
            out = [x for x in self.txt if x != v]
        elif k == "qty":
            for t in self.thr_vals(V):
                for u in self.units:
                    for dq in (-2, -1, 0, 1, 2):
                        q = self._near_units(t, u, random.Random(dq)) + dq
                        q = max(self.lo[u], min(self.hi[u], q))
                        out.append({"q": q, "u": u})
            if v is not None:
                out = [x for x in out if x["u"] == v["u"]] + [x for x in out if x["u"] != v["u"]]
        else:
            for t in self.thr_vals(V):
                for d in (self.deltas or DELTAS[k]):
                    x = max(self.lo, min(self.hi, t + d))
                    out.append(round(x, 2) if k == "money" else int(x))
            out += [self.lo, self.hi]
        if self.unk and v is not None:
            out.append(None)
        seen, res = set(), []
        for x in out:
            key = repr(x)
            if key not in seen and x != v:
                seen.add(key)
                res.append(x)
        return res

    # ------------------------------------------------------------------ rendering
    def fields(self, v, rng, today, sty):
        k = self.kind
        f = {}
        if v is None:
            return f
        if k == "int":
            f["n"] = str(v)
            f["nw"] = numw(v) if v <= 12 and sty % 2 else str(v)
            f["times"] = "once" if v == 1 else "twice" if v == 2 else f"{v} times"
            for key, one in (("nd", "day"), ("nh", "hour"), ("nmo", "month"), ("ny", "year"), ("nwk", "week")):
                f[key] = f"1 {one}" if v == 1 else f"{v} {one}s"
        elif k == "span":
            t0 = rng.randrange(6 * 60, 22 * 60, 5)
            t1 = t0 + v
            f["t0"] = ftime(t0, sty)
            f["t1"] = ftime(t1, sty) + (" the next day" if t1 >= 1440 else "")
            f["n"] = str(v)
        elif k == "money":
            f["amt"] = fmoney(v, sty)
        elif k == "days":
            n = v
            f["n"] = str(n)
            if n == 0:
                ago = "today"
            elif n == 1:
                ago = rng.choice(["yesterday", "1 day ago"])
            elif n % 7 == 0 and n <= 28 and sty % 3 == 0:
                ago = f"exactly {numw(n // 7)} weeks ago"
            else:
                ago = f"{n} days ago"
            f["ago"] = ago
            f["days"] = "1 day" if n == 1 else f"{n} days"
            if today is not None:
                f["date"] = fdate(today - dt.timedelta(days=n), sty, today)
        elif k == "tod":
            f["time"] = ftime(v, sty)
        elif k == "qty":
            f["q"] = fqty(v)
        return f

    def text(self, v, rng, today, sty, date_ok):
        k = self.kind
        if v is None:
            return rng.choice(self.unk_txt)
        if k == "bool":
            return rng.choice(self.T if v else self.F)
        if k == "cat":
            return rng.choice(self.txt[v])
        if k == "days":
            pool = list(self.rel or [])
            if date_ok and self.absd and v >= 2:
                pool = pool + list(self.absd) * 2
            return rng.choice(pool)
        return rng.choice(self.txt)


DELTAS = {"int": (-2, -1, 0, 0, 1, 2), "span": (-20, -1, 0, 1, 5, 30), "money": (-0.01, 0, 0, 0.01, -1, 1, -12.5, 25),
          "days": (-2, -1, 0, 0, 1, 2), "tod": (-30, -1, 0, 1, 15, 45)}


# ============================================================================================= issues / queues
class Iss:
    """An issue kind. say: main sentence templates ({=param} embeds a numeric param's value; other {slots} come from
    the domain slot pools).  past / neg: noun phrases for resolved / declined decoy mentions.  req: context
    compatibility {ctx param: allowed values}."""

    def __init__(self, k, say, P=None, past=(), neg=(), w=1.0, req=None, general=False, fixable=True):
        self.k, self.say, self.P, self.past, self.neg, self.w = k, list(say), dict(P or {}), list(past), list(neg), w
        self.fixable = fixable and not general  # can carry an inline "already sorted" clause
        self.req, self.general = dict(req or {}), general
        for t in self.say:
            for m in re.findall(r"\{=(\w+)\}", t):
                assert m in self.P, (k, m)
        for pn, p in self.P.items():
            if p.kind in ("money", "int", "span") and not p.txt:
                assert all("{=" + pn + "}" in t for t in self.say), (k, pn, "numeric fact without its own sentence")


def A(kinds, *conds):
    if isinstance(kinds, str) and kinds != "*":
        kinds = (kinds,)
    return (kinds, tuple(conds))


class Q:
    def __init__(self, name, rank, text, when, unless=()):
        self.name, self.rank, self.text, self.when, self.unless = name, rank, text, list(when), list(unless)


class Dom:
    def __init__(self, key, what, orgs, env, doc, issues, queues, catch, slots=None, ctx=None, thr=None,
                 fillers=(), kw=(), topics=(), subjects=(), desk=None, nvar=4, closers=None, greet=None, extra_env=(),
                 thr_fmt=None, clash=(), excl=(), fixed_slots=()):
        self.key, self.what, self.orgs, self.env, self.doc = key, what, list(orgs), env, doc
        self.issues = {i.k: i for i in issues}
        assert len(self.issues) == len(issues), key
        self.queues = list(queues)
        self.catch = catch  # (name, text)
        self.slots = dict(slots or {})
        self.ctx = dict(ctx or {})
        self.thr = dict(thr or {})
        self.fillers, self.kw, self.topics, self.subjects = list(fillers), list(kw), list(topics), list(subjects)
        self.desk, self.nvar, self.closers, self.greet = desk, nvar, closers, greet
        self.extra_env = list(extra_env)
        self.thr_fmt = dict(thr_fmt or {})
        self.clash = [set(g) for g in clash]  # kinds whose 'declined' mention would contradict each other's request
        self.fixed_slots = set(fixed_slots)  # slots that are one value per request (e.g. the sender's own flat)
        self.excl = [set(g) for g in excl]  # kinds that cannot appear together in one request (any status)
        for g in self.clash + self.excl:
            assert g <= set(self.issues), (key, g - set(self.issues))
        names = [q.name for q in self.queues] + [catch[0]]
        assert len(set(names)) == len(names), key
        self.qby = {q.name: q for q in self.queues}
        self._validate()

    def _validate(self):
        kinds = set(self.issues)
        for q in self.queues:
            for alts in (q.when, q.unless):
                for ks, conds in alts:
                    if ks != "*":
                        for k in ks:
                            assert k in kinds, (self.key, q.name, k)
                    for lhs, op, rhs in conds:
                        assert op in ("==", "!=", "<", "<=", ">", ">=", "in", "notin"), op
                        if isinstance(rhs, str) and rhs.startswith("$"):
                            assert rhs[1:] in self.thr, (self.key, q.name, rhs)
                        if lhs.startswith("ctx."):
                            assert lhs[4:] in self.ctx, (self.key, q.name, lhs)
                        elif ks != "*":
                            assert any(lhs in self.issues[k].P for k in ks), (self.key, q.name, lhs)
            # unknown-able params must never sit in an exception and must be flagged as 'stated' in the text
            for ks, conds in q.unless:
                for lhs, _, _ in conds:
                    for k in (self.issues if ks == "*" else ks):
                        p = self.issues[k].P.get(lhs) if not lhs.startswith("ctx.") else self.ctx.get(lhs[4:])
                        assert p is None or not p.unk, (self.key, q.name, lhs, "unknown-able fact in an exception")
            for ks, conds in q.when:
                for lhs, _, _ in conds:
                    for k in (self.issues if ks == "*" else ks):
                        p = self.issues[k].P.get(lhs) if not lhs.startswith("ctx.") else self.ctx.get(lhs[4:])
                        if p is not None and p.unk:
                            assert re.search(r"\bstat(e|es|ed|ing)\b|\bshows?\b|\bsays?\b", q.text), \
                                (self.key, q.name, "unknown-able fact but the definition does not say 'stated'")
        for p in self.ctx.values():
            assert not p.unk or True


# ============================================================================================= evaluation
def _val(lhs, iss_p, ctx):
    return ctx.get(lhs[4:]) if lhs.startswith("ctx.") else iss_p.get(lhs)


def cond_ok(c, iss_p, ctx, V):
    lhs, op, rhs = c
    v = _val(lhs, iss_p, ctx)
    if v is None:
        return False
    r = V[rhs[1:]] if isinstance(rhs, str) and rhs.startswith("$") else rhs
    if op == "in":
        return v in r
    if op == "notin":
        return v not in r
    a, b = canon(v), canon(r)
    return {"==": a == b, "!=": a != b, "<": a < b, "<=": a <= b, ">": a > b, ">=": a >= b}[op]


def alt_ok(alt, kind, iss_p, ctx, V):
    ks, conds = alt
    if ks != "*" and kind not in ks:
        return False
    return all(cond_ok(c, iss_p, ctx, V) for c in conds)


def covers(q, kind, iss_p, ctx, V):
    """(covered, base_matched, exception_fired)"""
    base = any(alt_ok(a, kind, iss_p, ctx, V) for a in q.when)
    exc = base and any(alt_ok(a, kind, iss_p, ctx, V) for a in q.unless)
    return base and not exc, base, exc


def route(dom, var, opts, ctx, issues):
    """Primary evaluator. issues: list of dicts {k, p, st}. Returns (gold, applicable per issue, exceptions)."""
    V = var["V"]
    shown = [n for n in opts if n != dom.catch[0]]
    app, excs = [], []
    for it in issues:
        a, e = [], []
        if it["st"] == "open":
            for n in shown:
                c, b, x = covers(dom.qby[n], it["k"], it["p"], ctx, V)
                if c:
                    a.append(n)
                if x:
                    e.append(n)
        app.append(a)
        excs.append(e)
    allq = {n for a in app for n in a}
    if not allq:
        return dom.catch[0], app, excs
    return min(allq, key=lambda n: var["order"][n]), app, excs


# ---- independent second evaluator: rules compiled to Python source; priority read back from the definition text
def _lit(x):
    return repr(x)


def compile_rule(q, V):
    def cexpr(c):
        lhs, op, rhs = c
        src = f"ctx.get({lhs[4:]!r})" if lhs.startswith("ctx.") else f"p.get({lhs!r})"
        r = V[rhs[1:]] if isinstance(rhs, str) and rhs.startswith("$") else rhs
        if op == "in":
            return f"({src} is not None and {src} in {_lit(tuple(r))})"
        if op == "notin":
            return f"({src} is not None and {src} not in {_lit(tuple(r))})"
        pyop = op
        return f"({src} is not None and CANON({src}) {pyop} CANON({_lit(r)}))"

    def aexpr(a):
        ks, conds = a
        parts = [] if ks == "*" else [f"(k in {_lit(tuple(ks))})"]
        parts += [cexpr(c) for c in conds]
        return "(" + (" and ".join(parts) if parts else "True") + ")"

    w = " or ".join(aexpr(a) for a in q.when) or "False"
    u = " or ".join(aexpr(a) for a in q.unless) or "False"
    return f"lambda k, p, ctx: ({w}) and not ({u})"


PRIO_RE = re.compile(r"^(?:Priority|Rank|Tier|Escalation weight|Check order) (\d+)[.:] ")


def route2(dom, defs_text, V, opts, ctx, issues, fmt):
    fns = {n: eval(compile_rule(dom.qby[n], V), {"CANON": canon}) for n in opts if n != dom.catch[0]}
    num = {}
    for n in opts:
        m = PRIO_RE.match(defs_text[n])
        assert m, defs_text[n]
        num[n] = int(m.group(1))
    best = None
    ordered = sorted(fns, key=lambda n: num[n], reverse=(fmt == "weight"))
    for n in ordered:  # walk the queues in the stated order; the first that covers any open issue takes it
        if any(fns[n](it["k"], it["p"], ctx) for it in issues if it["st"] == "open"):
            best = n
            break
    return best or dom.catch[0]


# ============================================================================================= policy variants
FORMATS = [  # (id, prefix builder, rule phrase used in the instruction)
    ("prio", lambda n: f"Priority {n}. ", "the queue with the lowest priority number wins"),
    ("rank", lambda n: f"Rank {n}. ", "the queue with the lowest rank number wins"),
    ("tier", lambda n: f"Tier {n}: ", "the queue in the lowest-numbered tier wins"),
    ("weight", lambda n: f"Escalation weight {n}. ", "the queue with the highest escalation weight wins"),
    ("order", lambda n: f"Check order {n}: ", "the queue with the lowest check-order number wins"),
]


def make_variant(dom, j):
    rng = R("variant", dom.key, j)
    V = {}
    for k, opts in sorted(dom.thr.items()):
        V[k] = opts[(j + rng.randrange(len(opts))) % len(opts)] if j else opts[0]
    for k, f in dom.thr_fmt.items():
        V[k + "_s"] = f(V[k])
    jit = 2.5 + 1.5 * (j % 2)
    qs = sorted(dom.queues, key=lambda q: (q.rank + rng.uniform(-jit, jit), q.name))
    fmt = FORMATS[(hseed(dom.key) + j) % len(FORMATS)]
    n = len(qs)
    step = 10 if rng.random() < 0.25 and fmt[0] in ("prio", "rank") else 1
    order = {q.name: i for i, q in enumerate(qs)}
    order[dom.catch[0]] = n
    defs, nums = {}, {}
    for i, q in enumerate(qs):
        num = (n - i) if fmt[0] == "weight" else (i + 1) * step
        nums[q.name] = num
        body = q.text.format(**V)
        defs[q.name] = fmt[1](num) + body
    cnum = 0 if fmt[0] == "weight" else (n + 1) * step
    nums[dom.catch[0]] = cnum
    defs[dom.catch[0]] = fmt[1](cnum) + dom.catch[1]
    for k, v in defs.items():
        assert len(v.split()) <= 46, (dom.key, k, len(v.split()), v)
    return {"j": j, "V": V, "order": order, "fmt": fmt[0], "rule": fmt[2], "defs": defs, "nums": nums,
            "qid": f"{dom.key}_v{j}"}

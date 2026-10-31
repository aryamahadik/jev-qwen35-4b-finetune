"""Claim operations for gen_tables: sampling, exact (three-valued) evaluation and surface text.

Every op works on a tab_core.Table and a spec dict s. eval(t, s) returns the verdict of the UN-negated claim:
  'T' the table establishes it, 'F' the table rules it out, 'N' the table cannot settle it (a needed row is not listed
  or a needed cell is blank), None = ill-defined (a tie on a superlative, a rounding tie, a failed presupposition);
  ill-defined items are never emitted. Negation (s['neg'] = 0/1/2) is applied by final().
Unknown values are treated as "any value in the column's domain" (>= 0 for non-negative columns), and the verdict is
'T'/'F' only when every possible completion agrees (Kleene logic, done by hand per op; tab_verify re-checks it by
brute-force enumeration over completions on the re-parsed rendered table).
"""
import math
from fractions import Fraction as Fr

from tab_core import (INF, NUMW, art, cap, fixed, fmt_date, hms_words, is_half, min_words, ordw, round_half_up,
                      trim_dec)

T, F, N = "T", "F", "N"
PREFIX = ["It is not the case that ", "It is not true that ", "It is false that "]
START = {"the", "it", "exactly", "at", "all", "every", "each", "no", "none", "not", "more", "fewer", "together",
         "in", "on", "if", "of", "there", "adding", "had", "across", "among", "only", "both", "either", "a", "an",
         "renting", "sending", "shipping", "two", "for", "over", "doses", "flight", "service", "between", "counting",
         "from", "checking", "under", "according", "during", "with", "by", "after", "before", "per", "since",
         "together", "on", "within", "each", "some", "one", "three", "four", "five", "six", "seven", "eight",
         "less", "neither", "fewer", "most", "had", "if"}
NUMERIC = ("num", "money", "pct", "dur")
ORDERED = NUMERIC + ("time", "date")


def flip(v):
    return {T: F, F: T}.get(v, v)


def final(v, neg):
    return flip(v) if neg % 2 else v


def poss(x):
    return x + ("'" if x.endswith("s") and not x.endswith("ss") else "'s")


def lc_claim(x):
    w = x.split(" ", 1)[0].lower().strip(",")
    return (x[:1].lower() + x[1:]) if w in START else x


def ch(lst, tv, salt=0):
    return lst[(tv // (7 ** salt)) % len(lst)]


def k3(canT, canF):
    if canT and not canF:
        return T
    if canF and not canT:
        return F
    if canT and canF:
        return N
    return None


def holds(x, rel, y):
    return {"eq": x == y, "gt": x > y, "lt": x < y, "ge": x >= y, "le": x <= y}[rel]


def rel_poss(rel, a, b):
    (alo, ahi), (blo, bhi) = a, b
    if rel == "gt":
        return ahi > blo, alo <= bhi
    if rel == "lt":
        return alo < bhi, ahi >= blo
    if rel == "ge":
        return ahi >= blo, alo < bhi
    if rel == "le":
        return alo <= bhi, ahi > blo
    if rel == "eq":
        return max(alo, blo) <= min(ahi, bhi), not (alo == ahi == blo == bhi)
    raise ValueError(rel)


def dom(c):
    return (c.domain_lo, c.hi_cap if c.hi_cap is not None else INF)


def ival(t, c, e):
    if e not in t.v:
        return dom(c)
    x = t.get(e, c.key)
    return dom(c) if x is None else (x, x)


def known(t, c, ents=None):
    return [e for e in (t.rows if ents is None else ents) if t.get(e, c.key) is not None]


def is_int(x):
    return not isinstance(x, Fr) or x.denominator == 1


def cols_for(t, op, kinds=ORDERED, virtual=True):
    out = []
    for c in t.cols + t.vcols:
        if c.ops is not None and op not in c.ops:
            continue
        if c.kind not in kinds or (c.virtual and not virtual):
            continue
        out.append(c)
    return out


def pick_col(cs, rng):
    return rng.choices(cs, weights=[c.w for c in cs])[0]


def cat_cols(t, op):
    return [c for c in t.cols + t.vcols if c.kind in ("cat", "bool") and (c.ops is None or op in c.ops)]


# ------------------------------------------------------------------------------------------------ value strings
def vs(c, v, s):
    alt = s.get("alt") if s.get("altcol") == c.key else None
    out = c.cv(v, alt) if alt else c.cv(v)
    return out


def objf(c, v):
    if not c.vp:
        return ""
    one = (v == 10 ** c.dec) if not isinstance(v, float) else False
    return c.vp.obj(1 if one else 2)


def num_or_word(n, s):
    return NUMW[n] if s.get("words") and 0 <= n <= 12 else str(n)


def delta_str(c, d, s):
    """String for a difference d (minor units / minutes / days) in column c's terms."""
    if c.kind == "time":
        return min_words(d, s.get("dstyle", "long"))
    if c.kind == "date":
        return f"{d} day{'s' if d != 1 else ''}"
    if c.kind == "dur":
        return hms_words(d) if c.durfmt == "hms" else min_words(d, "long")
    x = c.cv(d)
    return x


def round_phrase(c, dd):
    if c.kind == "money" and dd == 2:
        return " (rounded to the nearest cent)"
    if dd == 0:
        return " (rounded to the nearest whole number)"
    return " (rounded to one decimal place)" if dd == 1 else f" (rounded to {dd} decimal places)"


# ------------------------------------------------------------------------------------------------ predicates
def has_vp(c):
    return c.vp is not None


def pred(c, rel, V, v, pl=False, neg=False, tv=0):
    """Verb phrase 'subject <pred>' stating value REL V (V already formatted). Returns a string or None."""
    key = ("p_" + rel) + ("_neg" if neg else "")
    if key in c.custom:
        out = ch(c.custom[key], tv).format(V=V)
        if not pl and out.startswith("have "):  # custom p_* forms are written for plural subjects
            out = "has " + out[len("have "):]
        return out
    if c.vp:
        vp = c.vp
        o, suf = objf(c, v), vp.suffix
        few = "fewer" if vp.count else "less"
        if not neg:
            f = vp.fin(pl)
            forms = {"eq": [f"{f} {V}{o}{suf}", f"{f} exactly {V}{o}{suf}"],
                     "gt": [f"{f} more than {V}{o}{suf}"], "lt": [f"{f} {few} than {V}{o}{suf}"],
                     "ge": [f"{f} at least {V}{o}{suf}", f"{f} {V}{o} or more{suf}"],
                     "le": [f"{f} at most {V}{o}{suf}", f"{f} no more than {V}{o}{suf}"]}
        else:
            a = f"{vp.aux(pl)} not {vp.base}"
            forms = {"eq": [f"{a} {V}{o}{suf}", f"{a} exactly {V}{o}{suf}"],
                     "gt": [f"{a} more than {V}{o}{suf}"], "lt": [f"{a} {few} than {V}{o}{suf}"]}
        return ch(forms[rel], tv) if rel in forms else None
    if c.tvp:
        verb, base, prep, tense = c.tvp
        if not neg:
            f = verb if not pl else (verb if tense == "past" else base)
            forms = {"eq": [f"{f} {prep} {V}"], "gt": [f"{f} after {V}"], "lt": [f"{f} before {V}"],
                     "ge": [f"{f} no earlier than {V}", f"{f} {prep} {V} or later"],
                     "le": [f"{f} no later than {V}", f"{f} {prep} {V} or earlier"]}
        else:
            a = ("did" if tense == "past" else ("do" if pl else "does")) + " not " + base
            forms = {"eq": [f"{a} {prep} {V}"], "gt": [f"{a} after {V}"], "lt": [f"{a} before {V}"]}
        return ch(forms[rel], tv) if rel in forms else None
    n = c.noun
    have = ("have" if pl else "has") if not neg else ("do not have" if pl else "does not have")
    ab, be = c.above
    if not c.mass:
        have = have + " " + art(n)
    timey = c.kind in ("time", "date")
    forms = {"eq": [f"{have} {n} of {V}"],
             "gt": [f"{have} {n} {ab} {V}"] + ([] if timey else [f"{have} {n} of more than {V}"]),
             "lt": [f"{have} {n} {be} {V}"] + ([] if timey else [f"{have} {n} of less than {V}"]),
             "ge": [f"{have} {n} of at least {V}", f"{have} {n} of {V} or {'later' if timey else 'more'}"],
             "le": [f"{have} {n} of at most {V}", f"{have} {n} of {V} or {'earlier' if timey else 'less'}"]}
    if neg and rel in ("ge", "le"):
        return None
    return ch(forms[rel], tv)


def poss_forms(c, rel, E, V, neg=False):
    """'<E>'s <noun> is ...' sentences (singular only; noun-based columns)."""
    P = poss(E)
    n = c.noun
    ab, be = c.above
    timey = c.kind in ("time", "date")
    isn = "is not" if neg else "is"
    if rel == "eq":
        f = [f"{P} {n} {isn} {V}"]
        if not neg:
            f += [f"The {n} for {E} is {V}", f"The table gives {V} as the {n} for {E}"]
        return f
    if rel == "gt":
        return [f"{P} {n} {isn} {ab} {V}"] + ([] if (timey or neg) else [f"{P} {n} exceeds {V}", f"{P} {n} is more than {V}"])
    if rel == "lt":
        return [f"{P} {n} {isn} {be} {V}"] + ([] if (timey or neg) else [f"{P} {n} is less than {V}", f"{P} {n} is under {V}"])
    if neg:
        return []
    if rel == "ge":
        return [f"{P} {n} is at least {V}", f"{P} {n} is {V} or {'later' if timey else 'more'}"]
    if rel == "le":
        return [f"{P} {n} is at most {V}", f"{P} {n} is no {'later' if timey else 'more'} than {V}"]
    return []


def has_inner(c, rel):
    if (rel + "_neg") in c.custom or ("p_" + rel + "_neg") in c.custom:
        return True
    return rel in ("eq", "gt", "lt")


def rel_stmt(t, c, e, rel, v, s, tv):
    """Full sentence for 'e's value in c REL v' (inner negation if s['inner'])."""
    E = t.ent.r(e)
    P = poss(E)
    V = vs(c, v, s)
    inner = bool(s.get("inner"))
    key = rel + ("_neg" if inner else "")
    if key in c.custom:
        return cap(ch(c.custom[key], tv).format(E=E, P=P, V=V))
    forms = []
    p = pred(c, rel, V, v, pl=False, neg=inner, tv=tv)
    if p:
        forms.append(f"{E} {p}")
    if not c.vp and not c.tvp:
        forms += poss_forms(c, rel, E, V, neg=inner)
    if not forms:
        return None
    return cap(ch(forms, tv, 1))


def cmp_stmt(t, c, a, b, rel, s, tv):
    A, B = t.ent.r(a), t.ent.r(b)
    PA, PB = poss(A), poss(B)
    inner = bool(s.get("inner"))
    key = "cmp_" + rel + ("_neg" if inner else "")
    if key in c.custom:
        return cap(ch(c.custom[key], tv).format(A=A, B=B, PA=PA, PB=PB))
    hw, lw, shw, slw, hb, lb = c.words
    forms = []
    if c.vp:
        vp = c.vp
        suf = vp.suffix
        many = "many" if vp.count else "much"
        few = "fewer" if vp.count else "less"
        f = vp.verb if not inner else f"{vp.aux()} not {vp.base}"
        d = {"gt": [f"{A} {f} more {vp.cobj}{suf} than {B}"], "lt": [f"{A} {f} {few} {vp.cobj}{suf} than {B}"],
             "ge": [f"{A} {f} at least as {many} {vp.cobj}{suf} as {B}"],
             "le": [f"{A} {f} no more {vp.cobj}{suf} than {B}"],
             "eq": [f"{A} and {B} {vp.plural if not inner else vp.aux(True) + ' not ' + vp.base} the same "
                    f"{'number' if vp.count else 'amount'} of {vp.cobj}{suf}"]}
        if inner and rel in ("ge", "le"):
            return None
        forms += d[rel]
    elif c.tvp:
        verb, base, prep, tense = c.tvp
        f = verb if not inner else ("did" if tense == "past" else "does") + " not " + base
        same = "on the same day as" if c.kind == "date" else "at the same time as"
        d = {"gt": [f"{A} {f} later than {B}"], "lt": [f"{A} {f} earlier than {B}"],
             "ge": [f"{A} {f} no earlier than {B}"], "le": [f"{A} {f} no later than {B}"],
             "eq": [f"{A} {f} {same} {B}"]}
        if inner and rel in ("ge", "le"):
            return None
        forms += d[rel]
    if not c.vp:
        n = c.cmpnoun
        isn = "is not" if inner else "is"
        ah = "" if c.mass else art(hw) + " "
        al = "" if c.mass else art(lw) + " "
        d = {"gt": [f"{PA} {n} {isn} {hw} than {PB}", f"{A} {'does not have' if inner else 'has'} {ah}{hw} {n} than {B}"]
                   + ([] if inner else [f"{PB} {n} is {lw} than {PA}"]),
             "lt": [f"{PA} {n} {isn} {lw} than {PB}", f"{A} {'does not have' if inner else 'has'} {al}{lw} {n} than {B}"]
                   + ([] if inner else [f"{PB} {n} is {hw} than {PA}"]),
             "ge": [] if inner else [f"{PA} {n} is at least as {hb} as {PB}", f"{PA} {n} is no {lw} than {PB}"],
             "le": [] if inner else [f"{PA} {n} is no {hw} than {PB}", f"{PA} {n} is at most as {hb} as {PB}"],
             "eq": [f"{A} and {B} {'do not have' if inner else 'have'} the same {n}"]
                   + ([] if inner else [f"{PA} {n} is the same as {PB}"])}
        forms += d[rel]
    forms = [x for x in forms if x]
    if not forms:
        return None
    return cap(ch(forms, tv, 1))


def sup_pred(c, hi, pl=False, neg=False):
    """Predicate for 'has the highest value' (for 'Which ... ?' questions and 'the <sg> that ...')."""
    key = ("psup_hi" if hi else "psup_lo") + ("_neg" if neg else "")
    if key in c.custom:
        return c.custom[key][0]
    hw, lw, shw, slw, hb, lb = c.words
    if c.vp:
        vp = c.vp
        f = vp.fin(pl) if not neg else f"{vp.aux(pl)} not {vp.base}"
        most = "the most" if hi else ("the fewest" if vp.count else "the least")
        return f"{f} {most} {vp.cobj}{vp.suffix}"
    if c.tvp:
        verb, base, prep, tense = c.tvp
        f = (verb if not pl or tense == "past" else base) if not neg else \
            ("did" if tense == "past" else ("do" if pl else "does")) + " not " + base
        return f"{f} {'last' if hi else 'first'}"
    have = ("have" if pl else "has") if not neg else ("do not have" if pl else "does not have")
    return f"{have} the {shw if hi else slw} {c.noun}"


# ------------------------------------------------------------------------------------------------ constants
def nice_step(c, x):
    x = abs(int(x)) if x not in (None, INF) else 0
    if c.kind == "time":
        return 15
    if c.kind == "date":
        return 7
    if c.kind == "dur":
        return 60 if c.durfmt == "hms" else 5
    m = 10 ** max(0, len(str(x)) - 2)
    return max(c.step, m)


def near(c, x, rng, others=()):
    """Candidate constants near x: x itself (boundary), +-1 step, a round number, another row's value."""
    st = c.step
    ns = nice_step(c, x)
    out = [x, x, x + st, x - st, x + 2 * st, x - 2 * st, (x // ns) * ns, (x // ns + 1) * ns, x + ns, x - ns]
    out += [o for o in others if o not in (None, INF)][:4]
    out = [o for o in out if o is not None and o != INF and is_int(o)]
    return [int(o) for o in out]


DATE_LO, DATE_HI = 693000, 750000  # ordinals, roughly 1898..2054


def ok_const(c, v):
    if v is None or v == INF or not is_int(v):
        return False
    if c.kind == "date" and not (DATE_LO < v < DATE_HI):
        return False
    if v <= c.domain_lo:
        return False
    if c.hi_cap is not None and v >= c.hi_cap:
        return False
    if c.kind == "time" and not (0 < v < 1440):
        return False
    return c.cv(v) is not None


def hard_neg(t, c, e, x, rng):
    """A clearly wrong but close value for entity e (another row's value, a small slip, a digit swap)."""
    cands = []
    others = [t.get(o, c.key) for o in t.rows if o != e]
    others = [o for o in others if o is not None and o != INF and o != x and is_int(o)]
    if others:
        cands += [rng.choice(others)] * 3
    st = c.step
    if c.kind == "time":
        cands += [x + d for d in (5, -5, 10, -10, 15, -15, 60, -60, 30, -30)]
    elif c.kind == "date":
        cands += [x + d for d in (1, -1, 2, -2, 7, -7, 30, -30, 365, -365)]
    elif c.kind == "dur" and c.durfmt == "hms":
        cands += [x + d for d in (1, -1, 10, -10, 60, -60, 600, -600)]
    else:
        cands += [x + d * st for d in (1, -1, 2, -2, 5, -5, 10, -10)]
        s = str(abs(int(x)))
        if len(s) >= 2:
            i = rng.randrange(len(s) - 1)
            sw = s[:i] + s[i + 1] + s[i] + s[i + 2:]
            if sw != s and not sw.startswith("0"):
                cands.append(int(sw) * (1 if x >= 0 else -1))
    out = []
    for v in cands:
        if v is None or v == INF or v == x:
            continue
        v = int(v)
        if c.kind == "time" and not (0 < v < 1440):
            continue
        if c.nonneg and v < 0:
            continue
        if c.hi_cap is not None and v > c.hi_cap:
            continue
        if c.cv(v) is None:
            continue
        out.append(v)
    cands = out
    return rng.choice(cands) if cands else None


def plausible(t, c, rng):
    vals = [t.get(o, c.key) for o in t.rows]
    vals = [v for v in vals if v is not None and v != INF and is_int(v)]
    if c.kind == "date":
        if not vals:
            return None
        v = int(rng.choice(vals)) + rng.choice([0, 1, -1, 7, -7, 30, -30, 365, -365])
        return v if ok_const(c, v) else None
    if vals and rng.random() < 0.6:
        v = int(rng.choice(vals)) + rng.choice([0, c.step, -c.step, 2 * c.step])
    else:
        v = rng.randrange(c.gen_lo, c.hi + 1, c.step) if c.hi > c.gen_lo else c.gen_lo
    return v if ok_const(c, v) else None


def can_blank(t, e, c):
    return (not c.virtual and not c.nomiss and e in t.v and t.v[e].get(c.key) is not None
            and (e, c.key) not in t.corr and c.key not in t.derived)


def make_unknown(t, c, rng, avoid=(), allow_absent=True):
    """Make the claim's entity unknown: an entity that is not listed (partial tables only) or a blanked cell."""
    if c.virtual or c.nomiss:
        return None
    absent = [p for p in t.pool if p not in t.v]
    if allow_absent and t.partial and absent and rng.random() < 0.45:
        return rng.choice(absent)
    ents = [e for e in t.rows if e not in avoid and can_blank(t, e, c)]
    if not ents:
        return None
    e = rng.choice(ents)
    t.v[e][c.key] = None
    return e


def scope_sfx(t, s, rng):
    if t.partial:
        return rng.choice([" shown", " listed", " in this table"])
    return rng.choice(["", "", " in the table", " listed"])


def members(t, s):
    ents = list(t.rows)
    f = s.get("filt")
    if f:
        ents = [e for e in ents if t.get(e, f[0]) == f[1]]
    return ents


def filt_phrase(t, s):
    f = s.get("filt")
    if not f:
        return ""
    c = t.col(f[0])
    return " " + c.filt.format(X=f[1])


def pick_filter(t, rng, minsize=2):
    cs = [c for c in cat_cols(t, "filter") if c.filt and not c.virtual]
    rng.shuffle(cs)
    for c in cs:
        vals = [t.get(e, c.key) for e in t.rows]
        if any(v is None for v in vals):
            continue
        cnt = {}
        for v in vals:
            cnt[v] = cnt.get(v, 0) + 1
        good = [v for v, k in cnt.items() if k >= minsize and k < len(vals)]
        if good:
            return (c.key, rng.choice(sorted(good)))
    return None


def unseen(t, s):
    return (t.total - len(t.rows)) if s.get("scope") == "a" and t.total else 0


# ------------------------------------------------------------------------------------------------ base op
class Op:
    name = ""
    qa_ok = False
    n_ok = False
    neg_ok = True
    inner_ok = False
    table_edit = True

    def cols(self, t):
        return []

    def applicable(self, t):
        return bool(self.cols(t))

    def cells(self, t, s):
        return []

    def consts(self, t, s):
        return []

    def edges(self, t, s):
        return set()

    def mutate(self, t, s, rng):
        return None

    def qa(self, t, s):
        return None


def dep_cells(t, key, e):
    c = t.col(key)
    if c.virtual:
        if c.xdeps:
            return [(x, d) for x in t.rows for d in c.deps]
        return [(e, d) for d in c.deps]
    return [(e, key)]


def col_edges(t, c, s):
    out = set()
    if c.kind in ("time", "date") or (c.kind == "dur"):
        out.add("temporal")
    if c.numeric:
        out.add("numeric")
    if c.virtual:
        out.add("multi_hop")
    if s.get("altcol") == c.key and s.get("alt") in ("k", "g", "cm", "hm"):
        out.add("units")
    if any(k == c.key for (_, k) in t.corr):
        out.add("conflicting_evidence")
    if c.unl:
        out.add("implicit")
    if c.scale != 1 or c.units_edge:
        out.add("units")
    if c.exc:
        out.add("exception")
    return out


# ------------------------------------------------------------------------------------------------ val
class ValOp(Op):
    name, qa_ok, n_ok, inner_ok = "val", True, True, True

    def cols(self, t):
        return [c for c in cols_for(t, "val") if not c.unl]

    def sample(self, t, rng, want):
        cs = self.cols(t)
        if want == N:
            cs = [c for c in cs if not c.virtual]
        if not cs:
            return None
        c = pick_col(cs, rng)
        s = {"op": "val", "col": c.key}
        if want == N:
            e = make_unknown(t, c, rng)
            v = plausible(t, c, rng)
            if e is None or v is None:
                return None
            s.update(e=e, v=v)
            return s
        ents = [e for e in known(t, c) if t.get(e, c.key) != INF]
        if not ents:
            return None
        e = rng.choice(ents)
        x = t.get(e, c.key)
        if not is_int(x):
            if is_half(x, 0, 0):
                return None
            s["round"] = True
            x = round_half_up(x, 0, 0)
        v = x if want == T else hard_neg(t, c, e, x, rng)
        if v is None or c.cv(v) is None:
            return None
        s.update(e=e, v=int(v))
        return s

    def eval(self, t, s):
        c = t.col(s["col"])
        e = s["e"]
        if e not in t.v:
            return N
        x = t.get(e, c.key)
        if x is None:
            return N
        if x == INF:
            return F
        if not is_int(x):
            if not s.get("round") or is_half(x, 0, 0):
                return None
            x = round_half_up(x, 0, 0)
        return T if x == s["v"] else F

    def text(self, t, s):
        c = t.col(s["col"])
        x = rel_stmt(t, c, s["e"], "eq", s["v"], s, s["tv"])
        if x and s.get("round"):
            x += round_phrase(c, c.dec)
        return x

    def qa(self, t, s):
        c = t.col(s["col"])
        E = t.ent.r(s["e"])
        V = vs(c, s["v"], s)
        if "q_val" in c.custom:
            q = ch(c.custom["q_val"], s["tv"]).format(E=E, P=poss(E))
        elif c.vp:
            vp = c.vp
            aux = vp.aux()
            q = f"How {'many' if vp.count else 'much'} {vp.cobj} {aux} {E} {vp.base}{vp.suffix}?"
            V = V + objf(c, s["v"])
        elif c.tvp:
            verb, base, prep, tense = c.tvp
            q = f"{'On what date' if c.kind == 'date' else 'At what time'} {'did' if tense == 'past' else 'does'} {E} {base}?"
        else:
            q = f"What is {poss(E)} {c.noun}?"
        if s.get("round"):
            q = q[:-1] + round_phrase(c, c.dec).replace(" (", ", ").rstrip(")") + "?"
        return q, V

    def cells(self, t, s):
        return dep_cells(t, s["col"], s["e"])

    def consts(self, t, s):
        return [(s["col"], s["v"])]

    def mutate(self, t, s, rng):
        c = t.col(s["col"])
        x = t.get(s["e"], c.key) if s["e"] in t.v else None
        base = x if (x is not None and x != INF and is_int(x)) else s["v"]
        v = hard_neg(t, c, s["e"], int(base), rng) if rng.random() < 0.7 or x is None else int(x)
        if v is None or v == s["v"] or c.cv(v) is None:
            return None
        return dict(s, v=v)

    def edges(self, t, s):
        c = t.col(s["col"])
        out = col_edges(t, c, s)
        if s.get("round"):
            out.add("numeric")
        return out


# ------------------------------------------------------------------------------------------------ thr
class ThrOp(Op):
    name, n_ok, inner_ok = "thr", True, True

    def cols(self, t):
        return cols_for(t, "thr")

    def sample(self, t, rng, want):
        cs = self.cols(t)
        if want == N:
            cs = [c for c in cs if not c.virtual]
        if not cs:
            return None
        c = pick_col(cs, rng)
        rel = rng.choice(["gt", "lt", "ge", "le", "gt", "lt"])
        s = {"op": "thr", "col": c.key, "rel": rel}
        if want == N:
            e = make_unknown(t, c, rng)
            v = plausible(t, c, rng)
            if e is None or v is None:
                return None
            s.update(e=e, v=v)
            return s if self.eval(t, s) == N else None
        ents = known(t, c)
        if not ents:
            return None
        e = rng.choice(ents)
        x = t.get(e, c.key)
        if x == INF:
            cands = near(c, int(rng.choice([v for v in (t.get(o, c.key) for o in t.rows) if v not in (None, INF)] or [c.hi])), rng)
        elif not is_int(x):
            cands = near(c, int(x), rng)
        else:
            cands = near(c, x, rng, [t.get(o, c.key) for o in t.rows if o != e])
        rng.shuffle(cands)
        for v in cands:
            if not ok_const(c, v):
                continue
            s2 = dict(s, e=e, v=v)
            if self.eval(t, s2) == want:
                return s2
        return None

    def eval(self, t, s):
        c = t.col(s["col"])
        return k3(*rel_poss(s["rel"], ival(t, c, s["e"]), (s["v"], s["v"])))

    def text(self, t, s):
        c = t.col(s["col"])
        return rel_stmt(t, c, s["e"], s["rel"], s["v"], s, s["tv"])

    def cells(self, t, s):
        return dep_cells(t, s["col"], s["e"])

    def consts(self, t, s):
        return [(s["col"], s["v"])]

    def mutate(self, t, s, rng):
        c = t.col(s["col"])
        cands = near(c, s["v"], rng, [t.get(o, c.key) for o in t.rows])
        cands = [v for v in cands if v != s["v"] and ok_const(c, v)]
        if not cands:
            return None
        return dict(s, v=rng.choice(cands))

    def edges(self, t, s):
        c = t.col(s["col"])
        out = col_edges(t, c, s) | {"numeric"} if c.numeric else col_edges(t, c, s)
        x = t.get(s["e"], c.key) if s["e"] in t.v else None
        if x is not None and x == s["v"]:
            out.add("numeric")  # boundary: value equals the threshold
        if s["rel"] in ("ge", "le"):
            out.add("quantifier")
        return out


# ------------------------------------------------------------------------------------------------ cmp
class CmpOp(Op):
    name, n_ok, inner_ok = "cmp", True, True

    def cols(self, t):
        return cols_for(t, "cmp")

    def sample(self, t, rng, want):
        cs = self.cols(t)
        if want == N:
            cs = [c for c in cs if not c.virtual]
        if not cs or len(t.rows) < 2:
            return None
        c = pick_col(cs, rng)
        rel = rng.choice(["gt", "lt", "gt", "lt", "ge", "le", "eq"])
        ents = known(t, c)
        if len(ents) < 2:
            return None
        srt = sorted(ents, key=lambda e: (t.get(e, c.key), e))
        if rng.random() < 0.6:
            i = rng.randrange(len(srt) - 1)
            a, b = srt[i], srt[i + 1]
            if rng.random() < 0.5:
                a, b = b, a
        else:
            a, b = rng.sample(ents, 2)
        s = {"op": "cmp", "col": c.key, "rel": rel, "a": a, "b": b}
        if rel in ("eq", "ge", "le") and not c.virtual and want != N and rng.random() < 0.35 \
                and (a, c.key) not in t.corr and (b, c.key) not in t.corr and t.get(a, c.key) != INF:
            t.v[b][c.key] = t.v[a][c.key]  # a tie, the boundary case for 'at least as' / 'the same'
            t.apply_derive()
            if not t.is_valid():
                return None
        if want == N:
            if rng.random() < 0.5:
                s["a"], s["b"] = s["b"], s["a"]
            e = make_unknown(t, c, rng, avoid=(s["b"],))
            if e is None:
                return None
            s["a"] = e
            if e == s["b"]:
                return None
        v = self.eval(t, s)
        if v != want:
            for r2 in ("gt", "lt", "ge", "le", "eq"):
                s2 = dict(s, rel=r2)
                if self.eval(t, s2) == want and rng.random() < 0.7:
                    return s2
            return None
        return s

    def eval(self, t, s):
        c = t.col(s["col"])
        return k3(*rel_poss(s["rel"], ival(t, c, s["a"]), ival(t, c, s["b"])))

    def text(self, t, s):
        return cmp_stmt(t, t.col(s["col"]), s["a"], s["b"], s["rel"], s, s["tv"])

    def cells(self, t, s):
        return dep_cells(t, s["col"], s["a"]) + dep_cells(t, s["col"], s["b"])

    def consts(self, t, s):
        c = t.col(s["col"])
        return [(c.key, t.get(x, c.key)) for x in (s["a"], s["b"]) if x in t.v and t.get(x, c.key) not in (None, INF)]

    def mutate(self, t, s, rng):
        others = [e for e in t.rows if e not in (s["a"], s["b"]) and t.get(e, s["col"]) is not None]
        if not others:
            return None
        return dict(s, b=rng.choice(others))

    def edges(self, t, s):
        c = t.col(s["col"])
        out = col_edges(t, c, s)
        xa = t.get(s["a"], c.key) if s["a"] in t.v else None
        xb = t.get(s["b"], c.key) if s["b"] in t.v else None
        if xa is not None and xa == xb:
            out.add("numeric")
        return out


# ------------------------------------------------------------------------------------------------ diff
class DiffOp(Op):
    name, qa_ok, n_ok = "diff", True, True

    def cols(self, t):
        return [c for c in cols_for(t, "diff", NUMERIC + ("time", "date")) if not c.unl]

    def sample(self, t, rng, want):
        cs = self.cols(t)
        if want == N:
            cs = [c for c in cs if not c.virtual]
        if not cs:
            return None
        c = pick_col(cs, rng)
        ents = [e for e in known(t, c) if is_int(t.get(e, c.key))]
        if len(ents) < 2:
            return None
        a, b = rng.sample(ents, 2)
        xa, xb = t.get(a, c.key), t.get(b, c.key)
        if xa == xb:
            return None
        form = rng.choice(["dir", "dir", "dir", "abs", "atl"])
        if xa < xb and (form != "dir" or rng.random() < 0.7):
            a, b, xa, xb = b, a, xb, xa
        d = abs(xa - xb)
        s = {"op": "diff", "col": c.key, "a": a, "b": b, "form": form}
        if want == T or want == N:
            D = d if form != "atl" else max(c.step, (d // nice_step(c, d)) * nice_step(c, d))
        else:
            if form == "dir" and xa < xb and rng.random() < 0.6:
                D = d  # sign trap: 'a is D higher than b' when it is D lower
            else:
                cands = [d + c.step, d - c.step, d + nice_step(c, d), d - nice_step(c, d), d * 2, d + 10 * c.step]
                if c.kind == "time":
                    cands = [d + 5, d - 5, d + 60, d - 60, d + 10]
                elif c.kind == "date":
                    cands = [d + 1, d - 1, d + 7, d - 7, d + 30]
                cands = [x for x in cands if x > 0 and x != d]
                if form == "atl":
                    cands = [x for x in cands if x > d]
                if not cands:
                    return None
                D = rng.choice(cands)
        if D <= 0 or delta_str(c, D, s) is None:
            return None
        s["d"] = int(D)
        if want == N:
            if c.virtual or c.nomiss:
                return None
            side = rng.choice(["a", "b"])
            absent = [p for p in t.pool if p not in t.v]
            if t.partial and absent and rng.random() < 0.45:
                s[side] = rng.choice(absent)
            elif can_blank(t, s[side], c):
                t.v[s[side]][c.key] = None
            else:
                return None
        v = self.eval(t, s)
        return s if v == want else None

    def eval(self, t, s):
        c = t.col(s["col"])
        (alo, ahi), (blo, bhi) = ival(t, c, s["a"]), ival(t, c, s["b"])
        lo, hi = alo - bhi, ahi - blo
        D = s["d"]
        if s["form"] == "dir":
            return k3(lo <= D <= hi, not (lo == hi == D))
        if s["form"] == "atl":
            return k3(hi >= D, lo < D)
        can_t = (lo <= D <= hi) or (lo <= -D <= hi)
        return k3(can_t, not (lo == hi and abs(lo) == D))

    def text(self, t, s):
        c = t.col(s["col"])
        A, B = t.ent.r(s["a"]), t.ent.r(s["b"])
        PA, PB = poss(A), poss(B)
        D = delta_str(c, s["d"], s)
        hw, lw, shw, slw, hb, lb = c.words
        form, tv = s["form"], s["tv"]
        if "diff_" + form in c.custom:
            return cap(ch(c.custom["diff_" + form], tv).format(A=A, B=B, PA=PA, PB=PB, D=D))
        if c.vp and c.vp.unit:
            Du = D + " " + (c.vp.unit[0] if s["d"] == 10 ** c.dec else c.vp.unit[1])
        else:
            Du = D + (objf(c, s["d"]) if c.vp else "")
        if form == "abs":
            forms = [f"The difference between {PA} and {PB} {c.noun} is {Du}",
                     f"{A} and {B} differ in {c.noun} by {Du}"]
            return cap(ch(forms, tv))
        if c.vp and not c.vp.count:
            vp = c.vp
            u = ""
            if vp.unit:
                u = " " + (vp.unit[0] if s["d"] == 10 ** c.dec else vp.unit[1])
            forms = [f"{A} {vp.verb} {'at least ' if form == 'atl' else ''}{D}{u} more {vp.cobj}{vp.suffix} than {B}"]
        elif c.vp and c.vp.count:
            vp = c.vp
            core = f"{D} more {vp.cobj}{vp.suffix} than {B}"
            forms = [f"{A} {vp.verb} {'at least ' if form == 'atl' else ''}{core}"]
        elif c.tvp:
            verb, base, prep, tense = c.tvp
            forms = [f"{A} {verb} {'at least ' if form == 'atl' else ''}{D} later than {B}"]
        else:
            al = "at least " if form == "atl" else ""
            forms = [f"{PA} {c.cmpnoun} is {al}{D} {hw} than {PB}"]
            if form == "dir":
                forms.append(f"{PA} {c.cmpnoun} exceeds {PB} by {D}" if c.numeric else f"{PA} {c.cmpnoun} is {D} {hw} than {PB}")
        return cap(ch(forms, tv, 1))

    def qa(self, t, s):
        if s["form"] != "dir":
            return None
        c = t.col(s["col"])
        xa, xb = t.get(s["a"], c.key), t.get(s["b"], c.key)
        if xa is None or xb is None or xa <= xb:
            return None
        A, B = t.ent.r(s["a"]), t.ent.r(s["b"])
        D = delta_str(c, s["d"], s)
        if "q_diff" in c.custom:
            return ch(c.custom["q_diff"], s["tv"]).format(A=A, B=B, PA=poss(A), PB=poss(B)), D
        if c.vp and c.vp.count:
            vp = c.vp
            q = f"How many more {vp.cobj}{vp.suffix} {vp.aux()} {A} {vp.base} than {B}?"
            D = D + objf(c, s["d"])
        elif c.vp:
            vp = c.vp
            q = f"How much more {vp.cobj}{vp.suffix} {vp.aux()} {A} {vp.base} than {B}?"
            if vp.unit:
                D = D + " " + (vp.unit[0] if s["d"] == 10 ** c.dec else vp.unit[1])
        elif c.tvp:
            verb, base, prep, tense = c.tvp
            q = f"How much later {'did' if tense == 'past' else 'does'} {A} {base} than {B}?"
        else:
            hw = c.words[0]
            q = f"How much {hw} is {poss(A)} {c.cmpnoun} than {poss(B)}?"
        return q, D

    def cells(self, t, s):
        return dep_cells(t, s["col"], s["a"]) + dep_cells(t, s["col"], s["b"])

    def consts(self, t, s):
        c = t.col(s["col"])
        out = []
        for x, y in ((s["a"], s["b"]), (s["b"], s["a"])):
            if y in t.v and t.get(y, c.key) not in (None, INF):
                out += [(c.key, t.get(y, c.key) + s["d"]), (c.key, t.get(y, c.key) - s["d"])]
        return out

    def mutate(self, t, s, rng):
        c = t.col(s["col"])
        st = 1 if c.kind in ("time", "date") else c.step
        cands = [s["d"] + st, s["d"] - st, s["d"] + nice_step(c, s["d"]), s["d"] - nice_step(c, s["d"])]
        cands = [x for x in cands if x > 0 and delta_str(c, x, s)]
        if not cands:
            return None
        return dict(s, d=rng.choice(cands))

    def edges(self, t, s):
        c = t.col(s["col"])
        return col_edges(t, c, s) | {"numeric"} | ({"quantifier"} if s["form"] == "atl" else set())


# ------------------------------------------------------------------------------------------------ sup
class SupOp(Op):
    name, qa_ok, n_ok, inner_ok = "sup", True, True, True

    def cols(self, t):
        return cols_for(t, "sup")

    def sample(self, t, rng, want):
        cs = self.cols(t)
        if want == N:
            cs = [c for c in cs if not c.virtual]
        if not cs or len(t.rows) < 3:
            return None
        c = pick_col(cs, rng)
        hi = rng.random() < 0.6
        s = {"op": "sup", "col": c.key, "hi": hi, "scope": "l"}
        if t.partial == "count" and (want == N and rng.random() < 0.6 or want == F and rng.random() < 0.25):
            s["scope"] = "a"
        ents = known(t, c)
        if len(ents) < 3:
            return None
        srt = sorted(ents, key=lambda e: t.get(e, c.key), reverse=hi)
        if want == T:
            s["e"] = srt[0]
        elif want == F:
            s["e"] = srt[1] if rng.random() < 0.6 else rng.choice(srt[1:])
        else:
            if s["scope"] == "a":
                s["e"] = srt[0]
            elif rng.random() < 0.5:
                s["e"] = srt[0]
                comp = [o for o in srt[1:] if can_blank(t, o, c)]
                if not comp:
                    return None
                t.v[rng.choice(comp[:3])][c.key] = None
            else:
                s["e"] = srt[0]
                if not can_blank(t, srt[0], c):
                    return None
                t.v[srt[0]][c.key] = None
        if s["scope"] == "l" and t.partial:
            s["sc"] = rng.choice([" among the {pl} shown", " of the {pl} listed", " in this table"])
        elif s["scope"] == "l":
            s["sc"] = rng.choice(["", "", " in the table", " among the {pl} listed"])
        else:
            s["sc"] = rng.choice([" of all {M} {pl}", " across all {M} {pl}"])
        return s if self.eval(t, s) == want else None

    def eval(self, t, s):
        c = t.col(s["col"])
        e, hi = s["e"], s["hi"]
        mem = members(t, s)
        if e not in mem:
            return None
        sign = 1 if hi else -1
        xe = t.get(e, c.key)
        others = [o for o in mem if o != e]
        kv = [t.get(o, c.key) for o in others if t.get(o, c.key) is not None]
        unk = sum(t.get(o, c.key) is None for o in others) + unseen(t, s)
        if xe is None:
            if not kv:
                return N if unk else None
            dlo, dhi = dom(c)
            if hi:
                m = max(kv)
                if dhi < m:
                    return F
                if dhi == m:
                    return None  # the unknown value could at best tie with the listed maximum
                return N
            m = min(kv)
            if dlo > m:
                return F
            if dlo == m:
                return None
            return N
        if any(sign * (x - xe) > 0 for x in kv):
            return F
        if any(x == xe for x in kv):
            return None
        if unk:
            lo = c.domain_lo
            if not hi and xe <= lo:
                return None
            if hi and c.hi_cap is not None and xe >= c.hi_cap:
                return None
            return N
        return T

    def _sc(self, t, s):
        return s["sc"].format(pl=t.ent.pl, M=t.total)

    def text(self, t, s):
        c = t.col(s["col"])
        E = t.ent.r(s["e"])
        sc = self._sc(t, s)
        hi, tv = s["hi"], s["tv"]
        hw, lw, shw, slw, hb, lb = c.words
        inner = bool(s.get("inner"))
        key = ("sup_hi" if hi else "sup_lo") + ("_neg" if inner else "")
        if key in c.custom:
            return cap(ch(c.custom[key], tv).format(E=E, P=poss(E), SC=sc))
        forms = [f"{E} {sup_pred(c, hi, neg=inner)}{sc}"]
        if not inner and not c.vp and not c.tvp:
            sw = shw if hi else slw
            forms += [f"The {t.ent.sg} with the {sw} {c.noun}{sc} is {E}", f"{poss(E)} {c.noun} is the {sw}{sc}"]
        elif inner and not c.vp and not c.tvp:
            sw = shw if hi else slw
            forms += [f"{E} is not the {t.ent.sg} with the {sw} {c.noun}{sc}"]
        return cap(ch(forms, tv, 1))

    def qa(self, t, s):
        c = t.col(s["col"])
        if s["scope"] == "a":
            return None
        if t.partial:
            q = f"Of the {t.ent.pl} shown, which {sup_pred(c, s['hi'])}?"
        else:
            q = f"Which {t.ent.sg} {sup_pred(c, s['hi'])}?"
        return q, s["e"]

    def cells(self, t, s):
        c = t.col(s["col"])
        return [x for e in t.rows for x in dep_cells(t, c.key, e)]

    def consts(self, t, s):
        c = t.col(s["col"])
        return [(c.key, t.get(e, c.key)) for e in t.rows if t.get(e, c.key) not in (None, INF)]

    def mutate(self, t, s, rng):
        others = [e for e in t.rows if e != s["e"]]
        return dict(s, e=rng.choice(others)) if others else None

    def edges(self, t, s):
        c = t.col(s["col"])
        out = col_edges(t, c, s)
        if s["scope"] == "a":
            out.add("missing_info")
        return out


# ------------------------------------------------------------------------------------------------ rank
class RankOp(Op):
    name = "rank"

    def cols(self, t):
        return [c for c in cols_for(t, "rank", NUMERIC + ("time", "date")) if not c.unl]

    def applicable(self, t):
        return len(t.rows) >= 4 and bool(self.cols(t))

    def sample(self, t, rng, want):
        if want == N:
            return None
        c = pick_col(self.cols(t), rng)
        hi = rng.random() < 0.65
        s = {"op": "rank", "col": c.key, "hi": hi,
             "sc": rng.choice([" among the {pl} shown", " in this table"]) if t.partial else rng.choice(["", " in the table"])}
        vals = [t.get(e, c.key) for e in t.rows]
        if any(v is None for v in vals) or len(set(vals)) != len(vals):
            return None
        srt = sorted(t.rows, key=lambda e: t.get(e, c.key), reverse=hi)
        k = rng.randrange(2, min(5, len(srt) - 1) + 1)
        s["k"] = k
        s["top"] = rng.random() < 0.35
        if want == T:
            s["e"] = srt[k - 1] if not s["top"] else rng.choice(srt[:k])
        else:
            if s["top"]:
                s["e"] = srt[k] if rng.random() < 0.7 else rng.choice(srt[k:])
            else:
                s["e"] = srt[k - 1 + rng.choice([-1, 1])] if k < len(srt) else srt[k - 2]
        return s if self.eval(t, s) == want else None

    def eval(self, t, s):
        c = t.col(s["col"])
        vals = [t.get(e, c.key) for e in t.rows]
        if any(v is None for v in vals) or len(set(vals)) != len(vals):
            return None
        srt = sorted(t.rows, key=lambda e: t.get(e, c.key), reverse=s["hi"])
        pos = srt.index(s["e"]) + 1
        if s.get("top"):
            return T if pos <= s["k"] else F
        return T if pos == s["k"] else F

    def text(self, t, s):
        c = t.col(s["col"])
        E = t.ent.r(s["e"])
        sc = s["sc"].format(pl=t.ent.pl)
        k, hi, tv = s["k"], s["hi"], s["tv"]
        o = ordw(k)
        hw, lw, shw, slw, hb, lb = c.words
        if s.get("top"):
            kw = NUMW[k]
            if ("ptop_hi" if hi else "ptop_lo") in c.custom:
                forms = [f"{E} is one of the {kw} {t.ent.pl}{sc} that {c.custom['ptop_hi' if hi else 'ptop_lo'][0]}"]
            elif "psup_hi" in c.custom or c.vp or c.tvp:
                forms = [f"{E} is one of the {kw} {t.ent.pl}{sc} that {sup_pred(c, hi, pl=True)}"]
            else:
                forms = [f"{E} is among the {kw} {t.ent.pl}{sc} with the {shw if hi else slw} {c.noun}"]
            return cap(forms[0])
        key = "rank_hi" if hi else "rank_lo"
        if key in c.custom:
            return cap(ch(c.custom[key], tv).format(E=E, O=o, SC=sc, K1=k - 1))
        forms = []
        if c.vp:
            vp = c.vp
            most = "most" if hi else ("fewest" if vp.count else "least")
            forms.append(f"{E} {vp.verb} the {o}-{most} {vp.cobj}{vp.suffix}{sc}")
        else:
            forms.append(f"{E} has the {o}-{shw if hi else slw} {c.noun}{sc}")
        n1 = k - 1
        cnt = NUMW[n1] if n1 <= 12 else str(n1)
        pl = t.ent.pl if n1 != 1 else t.ent.sg
        verb = "have" if n1 != 1 else "has"
        forms.append(f"Exactly {cnt} {pl}{sc} {verb} {art(hw if hi else lw)} {hw if hi else lw} {c.cmpnoun} than {E}")
        return cap(ch(forms, tv, 1))

    def cells(self, t, s):
        return [x for e in t.rows for x in dep_cells(t, s["col"], e)]

    def consts(self, t, s):
        c = t.col(s["col"])
        return [(c.key, t.get(e, c.key)) for e in t.rows if t.get(e, c.key) not in (None, INF)]

    def mutate(self, t, s, rng):
        ks = [k for k in (s["k"] - 1, s["k"] + 1) if 2 <= k <= min(5, len(t.rows) - 1)]
        return dict(s, k=rng.choice(ks)) if ks else None

    def edges(self, t, s):
        return col_edges(t, t.col(s["col"]), s) | {"multi_hop"}


# ------------------------------------------------------------------------------------------------ count
QS = ["exactly", "at_least", "more_than", "fewer_than", "at_most"]
QW = {"exactly": "Exactly", "at_least": "At least", "more_than": "More than", "fewer_than": "Fewer than",
      "at_most": "At most"}
QW2 = {"exactly": "exactly", "at_least": "at least", "more_than": "more than", "fewer_than": "less than",
       "at_most": "at most"}


def q_poss(q, n, lo, hi):
    if q == "exactly":
        return lo <= n <= hi, not (lo == hi == n)
    if q == "at_least":
        return hi >= n, lo < n
    if q == "more_than":
        return hi > n, lo <= n
    if q == "fewer_than":
        return lo < n, hi >= n
    if q == "at_most":
        return lo <= n, hi > n
    raise ValueError(q)


def row_status(t, c, e, rel, v):
    return k3(*rel_poss(rel, ival(t, c, e), (v, v)))


class CountOp(Op):
    name, qa_ok, n_ok = "count", True, True

    def cols(self, t):
        return cols_for(t, "count")

    def applicable(self, t):
        return len(t.rows) >= 4 and bool(self.cols(t))

    def _range(self, t, s):
        c = t.col(s["col"])
        mem = members(t, s)
        st = [row_status(t, c, e, s["rel"], s["v"]) for e in mem]
        k = sum(x == T for x in st)
        m = sum(x == N for x in st) + unseen(t, s)
        return k, k + m, len(mem)

    def sample(self, t, rng, want):
        cs = self.cols(t)
        if want == N:
            cs = [c for c in cs if not c.virtual]
        if not cs:
            return None
        c = pick_col(cs, rng)
        rel = rng.choice(["gt", "lt", "ge", "le", "gt", "eq"] if not c.virtual else ["gt", "lt", "ge", "le"])
        s = {"op": "count", "col": c.key, "rel": rel, "scope": "l"}
        if rng.random() < 0.3:
            f = pick_filter(t, rng, minsize=3)
            if f:
                s["filt"] = f
        if t.partial == "count" and not s.get("filt") and rng.random() < (0.5 if want == N else 0.2):
            s["scope"] = "a"
        mem = members(t, s)
        vals = [t.get(e, c.key) for e in mem if t.get(e, c.key) not in (None, INF) and is_int(t.get(e, c.key))]
        if len(vals) < 3:
            return None
        if rel == "eq":
            v = rng.choice(vals)
        else:
            v = rng.choice(near(c, rng.choice(vals), rng, vals))
        if not ok_const(c, v):
            return None
        s["v"] = v
        if want == N and s["scope"] == "l":
            cand = [e for e in mem if can_blank(t, e, c)]
            if not cand:
                return None
            rng.shuffle(cand)
            for e in cand[:1 + (rng.random() < 0.3)]:
                t.v[e][c.key] = None
        lo, hi, size = self._range(t, s)
        opts = []
        for q in QS:
            for n in range(1, max(size, (t.total or 0)) + 1):
                if q == "fewer_than" and n == 1:
                    continue
                if k3(*q_poss(q, n, lo, hi)) == want:
                    opts.append((q, n))
        if not opts:
            return None
        near_opts = [o for o in opts if abs(o[1] - lo) <= 1 or abs(o[1] - hi) <= 1]
        q, n = rng.choice(near_opts or opts)
        s.update(q=q, n=n)
        return s if self.eval(t, s) == want else None

    def eval(self, t, s):
        lo, hi, size = self._range(t, s)
        if size < 3:
            return None
        return k3(*q_poss(s["q"], s["n"], lo, hi))

    def _group(self, t, s, sg):
        return (t.ent.sg if sg else t.ent.pl) + filt_phrase(t, s)

    def text(self, t, s):
        c = t.col(s["col"])
        n, q, tv = s["n"], s["q"], s["tv"]
        sg = n == 1
        V = vs(c, s["v"], s)
        p = pred(c, s["rel"], V, s["v"], pl=not sg, tv=tv)
        pp = pred(c, s["rel"], V, s["v"], pl=True, tv=tv)
        if p is None or pp is None:
            return None
        nw = num_or_word(n, s)
        if s["scope"] == "a":
            forms = [f"{QW[q]} {nw} of all {t.total} {t.ent.pl}{filt_phrase(t, s)} {p}",
                     f"Across all {t.total} {t.ent.pl}{filt_phrase(t, s)}, {QW2[q] if q != 'fewer_than' else 'fewer than'} {nw} {p}"]
        else:
            sc = s["sc"]
            forms = [f"{QW[q]} {nw} {self._group(t, s, sg)}{sc} {p}",
                     f"{QW[q]} {nw} of the {self._group(t, s, False)}{sc} {p}",
                     f"The number of {self._group(t, s, False)}{sc} that {pp} is {QW2[q]} {n}"]
        return cap(ch(forms, tv, 1))

    def qa(self, t, s):
        if s["q"] != "exactly" or s["scope"] == "a":
            return None
        c = t.col(s["col"])
        V = vs(c, s["v"], s)
        pp = pred(c, s["rel"], V, s["v"], pl=True, tv=s["tv"])
        if pp is None:
            return None
        return f"How many {self._group(t, s, False)}{s['sc']} {pp}?", str(s["n"])

    def cells(self, t, s):
        return [x for e in members(t, s) for x in dep_cells(t, s["col"], e)]

    def consts(self, t, s):
        return [(s["col"], s["v"])]

    def mutate(self, t, s, rng):
        ns = [x for x in (s["n"] - 1, s["n"] + 1) if x >= 1 and not (s["q"] == "fewer_than" and x == 1)]
        return dict(s, n=rng.choice(ns)) if ns else None

    def edges(self, t, s):
        c = t.col(s["col"])
        out = col_edges(t, c, s) | {"quantifier", "numeric"}
        if s.get("filt"):
            out.add("multi_hop")
        if s["scope"] == "a" or any(t.get(e, c.key) is None for e in members(t, s)):
            out.add("missing_info")
        return out


# ------------------------------------------------------------------------------------------------ quant
class QuantOp(Op):
    name, n_ok = "quant", True

    def cols(self, t):
        return cols_for(t, "quant")

    def applicable(self, t):
        return len(t.rows) >= 3 and bool(self.cols(t))

    def sample(self, t, rng, want):
        cs = self.cols(t)
        if want == N:
            cs = [c for c in cs if not c.virtual]
        if not cs:
            return None
        c = pick_col(cs, rng)
        qt = rng.choice(["all", "all", "none", "some", "not_all"])
        rel = rng.choice(["gt", "lt", "ge", "le"])
        s = {"op": "quant", "col": c.key, "rel": rel, "qt": qt, "scope": "l"}
        if rng.random() < 0.3:
            f = pick_filter(t, rng, minsize=2)
            if f:
                s["filt"] = f
        if t.partial == "count" and not s.get("filt") and rng.random() < (0.5 if want == N else 0.2):
            s["scope"] = "a"
        mem = members(t, s)
        vals = sorted(t.get(e, c.key) for e in mem if t.get(e, c.key) not in (None, INF) and is_int(t.get(e, c.key)))
        if len(vals) < 2:
            return None
        pivot = vals[0] if rel in ("gt", "ge") else vals[-1]
        if rng.random() < 0.3:
            pivot = rng.choice(vals)
        if want == N and s["scope"] == "l":
            ents = [e for e in mem if can_blank(t, e, c)]
            if not ents:
                return None
            t.v[rng.choice(ents)][c.key] = None
        cands = near(c, pivot, rng, vals)
        rng.shuffle(cands)
        for v in cands:
            if not ok_const(c, v):
                continue
            s2 = dict(s, v=v)
            if self.eval(t, s2) == want:
                return s2
        return None

    def eval(self, t, s):
        c = t.col(s["col"])
        mem = members(t, s)
        if len(mem) < 2:
            return None
        st = [row_status(t, c, e, s["rel"], s["v"]) for e in mem]
        u = unseen(t, s)
        qt = s["qt"]
        if qt in ("all", "not_all"):
            can_t = not any(x == F for x in st)
            can_f = any(x in (F, N) for x in st) or u > 0
            v = k3(can_t, can_f)
            return v if qt == "all" else flip(v)
        can_t = not any(x == T for x in st)          # 'none'
        can_f = any(x in (T, N) for x in st) or u > 0
        v = k3(can_t, can_f)
        return v if qt == "none" else flip(v)

    def text(self, t, s):
        c = t.col(s["col"])
        V = vs(c, s["v"], s)
        tv = s["tv"]
        psg = pred(c, s["rel"], V, s["v"], pl=False, tv=tv)
        ppl = pred(c, s["rel"], V, s["v"], pl=True, tv=tv)
        if psg is None or ppl is None:
            return None
        fp = filt_phrase(t, s)
        sg, pl = t.ent.sg, t.ent.pl
        qt = s["qt"]
        if s["scope"] == "a":
            M = t.total
            forms = {"all": [f"All {M} {pl}{fp} {ppl}", f"Every one of the {M} {pl}{fp} {psg}"],
                     "none": [f"None of the {M} {pl}{fp} {psg}"],
                     "some": [f"At least one of the {M} {pl}{fp} {psg}"],
                     "not_all": [f"Not all {M} {pl}{fp} {ppl}"]}[qt]
        else:
            sc = s["sc"]
            forms = {"all": [f"All {pl}{fp}{sc} {ppl}", f"Every {sg}{fp}{sc} {psg}", f"Each of the {pl}{fp}{sc} {psg}"],
                     "none": [f"None of the {pl}{fp}{sc} {psg}", f"No {sg}{fp}{sc} {psg}"],
                     "some": [f"At least one {sg}{fp}{sc} {psg}", f"There is at least one {sg}{fp}{sc} that {psg}"],
                     "not_all": [f"Not all {pl}{fp}{sc} {ppl}", f"Not every {sg}{fp}{sc} {psg}"]}[qt]
        return cap(ch(forms, tv, 1))

    def cells(self, t, s):
        return [x for e in members(t, s) for x in dep_cells(t, s["col"], e)]

    def consts(self, t, s):
        return [(s["col"], s["v"])]

    def mutate(self, t, s, rng):
        c = t.col(s["col"])
        cands = [v for v in near(c, s["v"], rng) if v != s["v"] and ok_const(c, v)]
        return dict(s, v=rng.choice(cands)) if cands else None

    def edges(self, t, s):
        c = t.col(s["col"])
        out = col_edges(t, c, s) | {"quantifier"}
        if s["qt"] in ("none", "not_all"):
            out.add("negation")
        if s.get("filt"):
            out.add("multi_hop")
        if s["scope"] == "a" or any(t.get(e, c.key) is None for e in members(t, s)):
            out.add("missing_info")
        return out


# ------------------------------------------------------------------------------------------------ sum
class SumOp(Op):
    name, qa_ok, n_ok = "sum", True, True

    def cols(self, t):
        return [c for c in cols_for(t, "sum", ("num", "money", "dur")) if c.sum and not c.unl]

    def _mem(self, t, s):
        return [s["a"], s["b"]] if s["form"] == "pair" else members(t, s)

    def sample(self, t, rng, want):
        cs = self.cols(t)
        if want == N:
            cs = [c for c in cs if not c.virtual and c.nonneg and not c.nomiss]
        if not cs:
            return None
        c = pick_col(cs, rng)
        form = "pair" if (rng.random() < 0.35 or not c.sum_all) else "all"
        s = {"op": "sum", "col": c.key, "form": form, "rel": rng.choice(["eq", "eq", "eq", "gt", "lt"])}
        if form == "pair":
            ents = known(t, c)
            if len(ents) < 2:
                return None
            s["a"], s["b"] = rng.sample(ents, 2)
        else:
            if rng.random() < 0.25:
                f = pick_filter(t, rng, minsize=2)
                if f:
                    s["filt"] = f
        mem = self._mem(t, s)
        if any(t.get(e, c.key) is None for e in mem) or any(not is_int(t.get(e, c.key)) for e in mem):
            return None
        tot = sum(t.get(e, c.key) for e in mem)
        rel = s["rel"]
        ns = nice_step(c, tot)
        if want == N:
            e = rng.choice(mem)
            if not can_blank(t, e, c):
                return None
            t.v[e][c.key] = None
            S = rng.choice([tot, tot + ns, (tot // ns) * ns]) if rel != "lt" else tot + ns
        elif rel == "eq":
            if want == T:
                S = tot
            else:
                slips = [tot + c.step, tot - c.step, tot + 10 * c.step, tot - 10 * c.step, tot + ns, tot - ns]
                if len(mem) > 2:
                    slips += [tot - t.get(rng.choice(mem), c.key)] * 3  # a row left out
                slips = [x for x in slips if x > 0 and x != tot]
                S = rng.choice(slips)
        else:
            base = (tot // ns) * ns
            cands = [base, base + ns, base - ns, tot, tot + c.step, tot - c.step]
            cands = [x for x in cands if x > 0]
            rng.shuffle(cands)
            S = None
            for x in cands:
                if self.eval(t, dict(s, S=x)) == want:
                    S = x
                    break
            if S is None:
                return None
        if S is None or S <= 0 or c.cv(S) is None:
            return None
        s["S"] = int(S)
        return s if self.eval(t, s) == want else None

    def eval(self, t, s):
        c = t.col(s["col"])
        mem = self._mem(t, s)
        if len(mem) < 2 or any(e not in t.v for e in mem):
            return None
        vals = [t.get(e, c.key) for e in mem]
        if any(v is not None and not is_int(v) for v in vals):
            return None
        P = sum(v for v in vals if v is not None)
        unk = sum(v is None for v in vals)
        S, rel = s["S"], s["rel"]
        if not unk:
            return T if holds(P, rel, S) else F
        if not c.nonneg:
            return N
        if rel == "eq":
            return F if S < P else N
        if rel == "gt":
            return T if P > S else N
        return F if P >= S else N

    def _grp(self, t, s):
        return f"{t.ent.pl}{filt_phrase(t, s)}{s.get('sc', '')}"

    def text(self, t, s):
        c = t.col(s["col"])
        tv = s["tv"]
        S = vs(c, s["S"], s)
        rw = {"eq": "", "gt": "more than ", "lt": "less than "}[s["rel"]]
        if s["form"] == "pair":
            A, B = t.ent.r(s["a"]), t.ent.r(s["b"])
            if c.vp:
                vp = c.vp
                lt = "fewer than " if vp.count else "less than "
                rw2 = lt if s["rel"] == "lt" else rw
                forms = [f"{A} and {B} together {vp.plural} {rw2}{S}{objf(c, s['S'])}{vp.suffix}",
                         f"Between them, {A} and {B} {vp.plural} {rw2}{S}{objf(c, s['S'])}{vp.suffix}"]
            else:
                forms = [f"The combined {c.noun} of {A} and {B} is {rw}{S}",
                         f"{A} and {B} have a combined {c.noun} of {rw}{S}"]
        else:
            G = self._grp(t, s)
            if c.vp:
                vp = c.vp
                lt = "fewer than " if vp.count else "less than "
                rw2 = lt if s["rel"] == "lt" else rw
                forms = [f"Together, the {G} {vp.plural} {rw2}{S}{objf(c, s['S'])}{vp.suffix}",
                         f"The {G} {vp.plural} {rw2}{S}{objf(c, s['S'])}{vp.suffix} in total"]
            else:
                forms = [f"The combined {c.noun} of the {G} is {rw}{S}", f"The total {c.noun} across the {G} is {rw}{S}",
                         f"The {G} have a combined {c.noun} of {rw}{S}"]
        return cap(ch(forms, tv, 1))

    def qa(self, t, s):
        if s["rel"] != "eq":
            return None
        c = t.col(s["col"])
        S = vs(c, s["S"], s)
        if s["form"] == "pair":
            A, B = t.ent.r(s["a"]), t.ent.r(s["b"])
            if c.vp:
                q = f"How {'many' if c.vp.count else 'much'} {c.vp.cobj} {c.vp.aux(True) if c.vp.tense == 'pres' else 'did'} {A} and {B} {c.vp.base}{c.vp.suffix} together?"
                S += objf(c, s["S"])
            else:
                q = f"What is the combined {c.noun} of {A} and {B}?"
        else:
            G = self._grp(t, s)
            if c.vp:
                q = f"How {'many' if c.vp.count else 'much'} {c.vp.cobj} {c.vp.aux(True) if c.vp.tense == 'pres' else 'did'} the {G} {c.vp.base}{c.vp.suffix} in total?"
                S += objf(c, s["S"])
            else:
                q = f"What is the total {c.noun} of the {G}?"
        return q, S

    def cells(self, t, s):
        return [x for e in self._mem(t, s) for x in dep_cells(t, s["col"], e)]

    def consts(self, t, s):
        c = t.col(s["col"])
        mem = self._mem(t, s)
        tot = sum(t.get(e, c.key) or 0 for e in mem if e in t.v)
        out = []
        for e in mem:
            if e in t.v and t.get(e, c.key) is not None:
                out.append((c.key, s["S"] - (tot - t.get(e, c.key))))
            elif e in t.v:
                out.append((c.key, s["S"] - tot))
        return out

    def mutate(self, t, s, rng):
        c = t.col(s["col"])
        ns = nice_step(c, s["S"])
        cands = [x for x in (s["S"] + c.step, s["S"] - c.step, s["S"] + ns, s["S"] - ns) if x > 0 and c.cv(x)]
        return dict(s, S=rng.choice(cands)) if cands else None

    def edges(self, t, s):
        c = t.col(s["col"])
        out = col_edges(t, c, s) | {"numeric"}
        if s.get("filt"):
            out.add("multi_hop")
        if any(e in t.v and t.get(e, c.key) is None for e in self._mem(t, s)):
            out.add("missing_info")
        if s["rel"] != "eq":
            out.add("quantifier")
        return out


# ------------------------------------------------------------------------------------------------ avg
class AvgOp(Op):
    name, qa_ok = "avg", True

    def cols(self, t):
        return [c for c in cols_for(t, "avg", ("num", "money", "pct")) if c.avg and not c.unl and not c.virtual]

    def _dd(self, c):
        return 2 if c.kind == "money" else c.dec + 1

    def _avg(self, t, s):
        c = t.col(s["col"])
        mem = members(t, s)
        vals = [t.get(e, c.key) for e in mem]
        if len(mem) < 3 or any(v is None or not is_int(v) for v in vals):
            return None
        return Fr(sum(vals), len(vals)) * 10 ** (self._dd(c) - c.dec)  # minor units at dd decimals

    def sample(self, t, rng, want):
        if want == N:
            return None
        cs = self.cols(t)
        if not cs:
            return None
        c = pick_col(cs, rng)
        s = {"op": "avg", "col": c.key, "sc": ""}
        if rng.random() < 0.25:
            f = pick_filter(t, rng, minsize=3)
            if f:
                s["filt"] = f
        a = self._avg(t, s)
        if a is None:
            return None
        s["round"] = a.denominator != 1
        if s["round"] and is_half(a, 0, 0):
            return None
        ar = round_half_up(a, 0, 0) if s["round"] else int(a)
        if want == T:
            A = ar
        else:
            mem = members(t, s)
            vals = sorted(t.get(e, c.key) for e in mem)
            sc = 10 ** (self._dd(c) - c.dec)
            cands = [ar + 1, ar - 1, ar + 10, ar - 10]
            med = vals[len(vals) // 2] * sc
            if med != ar:
                cands += [med] * 2
            drop = Fr(sum(vals) - vals[0], len(vals) - 1) * sc
            cands.append(round_half_up(drop, 0, 0))
            cands.append(round_half_up(Fr(sum(vals), len(vals) + 1) * sc, 0, 0))
            cands = [int(x) for x in cands if x != ar and x > 0]
            A = rng.choice(cands) if cands else None
        if A is None:
            return None
        s["A"] = int(A)
        return s if self.eval(t, s) == want else None

    def eval(self, t, s):
        a = self._avg(t, s)
        if a is None:
            return None
        if a.denominator != 1:
            if not s["round"] or is_half(a, 0, 0):
                return None
            a = round_half_up(a, 0, 0)
        return T if int(a) == s["A"] else F

    def _vstr(self, c, A):
        dd = self._dd(c)
        x = fixed(A, dd, True)
        if c.kind != "money":
            x = trim_dec(x)
        if c.vp:
            return x + (c.vp.obj(2))
        return c.pre + x + c.suf

    def text(self, t, s):
        c = t.col(s["col"])
        A = self._vstr(c, s["A"])
        rp = round_phrase(c, self._dd(c)) if s["round"] else ""
        G = f"{t.ent.pl}{filt_phrase(t, s)}"
        if t.partial:
            G += " shown"
        tv = s["tv"]
        if c.vp:
            vp = c.vp
            forms = [f"On average, the {G} {vp.plural} {A}{vp.suffix}{rp}", f"The {G} {vp.plural} an average of {A}{vp.suffix}{rp}"]
        else:
            forms = [f"The average {c.noun} of the {G} is {A}{rp}", f"The {G} have an average {c.noun} of {A}{rp}",
                     f"The mean {c.noun} across the {G} is {A}{rp}"]
        return cap(ch(forms, tv, 1))

    def qa(self, t, s):
        c = t.col(s["col"])
        G = f"{t.ent.pl}{filt_phrase(t, s)}" + (" shown" if t.partial else "")
        rp = round_phrase(c, self._dd(c)).replace(" (", ", ").rstrip(")") if s["round"] else ""
        return f"What is the average {c.noun} of the {G}{rp}?", self._vstr(c, s["A"])

    def cells(self, t, s):
        return [(e, s["col"]) for e in members(t, s)]

    def consts(self, t, s):
        c = t.col(s["col"])
        mem = members(t, s)
        n = len(mem)
        tot = sum(t.get(e, c.key) or 0 for e in mem)
        sc = 10 ** (self._dd(c) - c.dec)
        target = Fr(s["A"] * n, sc)
        out = []
        for e in mem:
            x = t.get(e, c.key) or 0
            y = target - (tot - x)
            if y.denominator == 1:
                out.append((c.key, int(y)))
        return out

    def mutate(self, t, s, rng):
        return dict(s, A=s["A"] + rng.choice([1, -1, 10, -10]))

    def edges(self, t, s):
        c = t.col(s["col"])
        out = col_edges(t, c, s) | {"numeric", "multi_hop"}
        return out


# ------------------------------------------------------------------------------------------------ argthen
class ArgThenOp(Op):
    name, qa_ok = "argthen", True

    def cols(self, t):
        return cols_for(t, "argthen", NUMERIC + ("time", "date"))

    def applicable(self, t):
        return len(t.rows) >= 3 and len(self.cols(t)) + len(cat_cols(t, "catval")) >= 2 and bool(self.cols(t))

    def _ext(self, t, key, hi):
        c = t.col(key)
        vals = [(t.get(e, key), e) for e in t.rows]
        if any(v is None for v, _ in vals):
            return None
        best = max(v for v, _ in vals) if hi else min(v for v, _ in vals)
        es = [e for v, e in vals if v == best]
        return es[0] if len(es) == 1 else None

    def sample(self, t, rng, want):
        if want == N:
            return None
        c1 = pick_col(self.cols(t), rng)
        hi = rng.random() < 0.6
        e = self._ext(t, c1.key, hi)
        if e is None:
            return None
        srt = sorted(t.rows, key=lambda x: t.get(x, c1.key), reverse=hi)
        runner = srt[1]
        s = {"op": "argthen", "c1": c1.key, "hi": hi,
             "sc": rng.choice([" among the {pl} shown", " in this table"]) if t.partial else rng.choice(["", " in the table"])}
        opts = [c for c in self.cols(t) if c.key != c1.key] + [c for c in cat_cols(t, "catval") if c.key != c1.key]
        if not opts:
            return None
        c2 = pick_col(opts, rng)
        s["c2"] = c2.key
        x = t.get(e, c2.key)
        if x is None or x == INF:
            return None
        if c2.kind in ("cat", "bool"):
            s["kind"] = "cat"
            if want == T:
                s["X"] = x
            else:
                alts = [t.get(runner, c2.key)] + list(c2.cats or [])
                alts = [a for a in alts if a is not None and a != x]
                if not alts:
                    return None
                s["X"] = alts[0] if rng.random() < 0.6 else rng.choice(alts)
        elif rng.random() < 0.25:
            s["kind"] = "sup2"
            s["hi2"] = rng.random() < 0.5
            e2 = self._ext(t, c2.key, s["hi2"])
            if e2 is None:
                return None
        else:
            s["kind"] = "rel"
            s["rel"] = rng.choice(["eq", "eq", "gt", "lt", "ge", "le"])
            if not is_int(x):
                return None
            rx = t.get(runner, c2.key)
            cands = near(c2, int(x), rng, [rx] if rx not in (None, INF) and is_int(rx) else [])
            if s["rel"] == "eq":
                cands = [int(x)] if want == T else ([int(rx)] if rx not in (None, INF) and is_int(rx) and rx != x else []) + \
                                                   [v for v in cands if v != x]
            rng.shuffle(cands) if s["rel"] != "eq" else None
            got = None
            for v in cands:
                if ok_const(c2, v) and self.eval(t, dict(s, v=v)) == want:
                    got = v
                    break
            if got is None:
                return None
            s["v"] = got
        return s if self.eval(t, s) == want else None

    def eval(self, t, s):
        e = self._ext(t, s["c1"], s["hi"])
        if e is None:
            return None
        c2 = t.col(s["c2"])
        x = t.get(e, c2.key)
        if x is None:
            return None
        if s["kind"] == "cat":
            return T if x == s["X"] else F
        if s["kind"] == "sup2":
            e2 = self._ext(t, c2.key, s["hi2"])
            if e2 is None:
                return None
            return T if e2 == e else F
        return T if holds(x, s["rel"], s["v"]) else F

    def _subj(self, t, s):
        c1 = t.col(s["c1"])
        sc = s["sc"].format(pl=t.ent.pl)
        if c1.vp or c1.tvp or ("psup_hi" in c1.custom):
            return f"the {t.ent.sg} that {sup_pred(c1, s['hi'])}{sc}"
        hw, lw, shw, slw, hb, lb = c1.words
        return f"the {t.ent.sg} with the {shw if s['hi'] else slw} {c1.noun}{sc}"

    def text(self, t, s):
        c2 = t.col(s["c2"])
        subj = self._subj(t, s)
        tv = s["tv"]
        if s["kind"] == "cat":
            p = cat_pred(c2, s["X"], neg=False)
        elif s["kind"] == "sup2":
            p = "also " + sup_pred(c2, s["hi2"])
        else:
            p = pred(c2, s["rel"], vs(c2, s["v"], s), s["v"], pl=False, tv=tv)
            if p is None:
                return None
        return cap(f"{subj} {p}")

    def qa(self, t, s):
        if s["kind"] != "rel" or s["rel"] != "eq":
            return None
        c2 = t.col(s["c2"])
        subj = self._subj(t, s)
        if c2.vp:
            vp = c2.vp
            q = f"How {'many' if vp.count else 'much'} {vp.cobj}{vp.suffix} {vp.aux()} {subj} {vp.base}?"
            return q, vs(c2, s["v"], s) + objf(c2, s["v"])
        return f"What is the {c2.noun} of {subj}?", vs(c2, s["v"], s)

    def cells(self, t, s):
        out = [x for e in t.rows for x in dep_cells(t, s["c1"], e)]
        e = self._ext(t, s["c1"], s["hi"])
        if e:
            out += dep_cells(t, s["c2"], e) if not t.col(s["c2"]).kind in ("cat",) else []
        return out

    def consts(self, t, s):
        out = [(s["c1"], t.get(e, s["c1"])) for e in t.rows if t.get(e, s["c1"]) not in (None, INF)]
        if s.get("v") is not None:
            out.append((s["c2"], s["v"]))
        return out

    def mutate(self, t, s, rng):
        if s["kind"] == "rel":
            c2 = t.col(s["c2"])
            cands = [v for v in near(c2, s["v"], rng) if v != s["v"] and ok_const(c2, v)]
            return dict(s, v=rng.choice(cands)) if cands else None
        return None

    def edges(self, t, s):
        out = col_edges(t, t.col(s["c1"]), s) | col_edges(t, t.col(s["c2"]), s) | {"multi_hop"}
        return out


# ------------------------------------------------------------------------------------------------ categorical
def cat_pred(c, X, neg=False, pl=False):
    if c.say and X in c.say:
        pos, ng = c.say[X][:2]
        if pl:
            if len(c.say[X]) > 2:
                return c.say[X][2] if not neg else c.say[X][3]
            return None
        return ng if neg else pos
    if pl:
        if not c.sayp:
            return None
        return (c.sayp if not neg else c.sayp.replace(" are ", " are not ")).format(X=X)
    if neg:
        return (c.sayfn or "is not {X}").format(X=X)
    return (c.sayf or "is {X}").format(X=X)


class CatValOp(Op):
    name, n_ok, inner_ok = "catval", True, True

    def cols(self, t):
        return [c for c in cat_cols(t, "catval")]

    def sample(self, t, rng, want):
        cs = self.cols(t)
        if want == N:
            cs = [c for c in cs if not c.virtual]
        if not cs:
            return None
        c = pick_col(cs, rng)
        s = {"op": "catval", "col": c.key}
        if want == N:
            e = make_unknown(t, c, rng)
            if e is None:
                return None
            vals = sorted({t.get(x, c.key) for x in t.rows if t.get(x, c.key) is not None} | set(c.cats or []))
            if not vals:
                return None
            s.update(e=e, X=rng.choice(vals))
            return s
        ents = known(t, c)
        if not ents:
            return None
        e = rng.choice(ents)
        x = t.get(e, c.key)
        if want == T:
            X = x
        else:
            alts = sorted({t.get(o, c.key) for o in t.rows} - {x, None}) + [a for a in (c.cats or []) if a != x]
            if not alts:
                return None
            X = rng.choice(alts)
        s.update(e=e, X=X)
        return s

    def eval(self, t, s):
        c = t.col(s["col"])
        if s["e"] not in t.v:
            return N
        x = t.get(s["e"], c.key)
        if x is None:
            return N
        return T if x == s["X"] else F

    def text(self, t, s):
        c = t.col(s["col"])
        E = t.ent.r(s["e"])
        p = cat_pred(c, s["X"], neg=bool(s.get("inner")))
        return cap(f"{E} {p}")

    def cells(self, t, s):
        return dep_cells(t, s["col"], s["e"])

    def mutate(self, t, s, rng):
        c = t.col(s["col"])
        alts = sorted({t.get(o, c.key) for o in t.rows} - {s["X"], None}) + [a for a in (c.cats or []) if a != s["X"]]
        return dict(s, X=rng.choice(alts)) if alts else None

    def edges(self, t, s):
        c = t.col(s["col"])
        out = set()
        if c.virtual:
            out |= {"multi_hop"}
        if c.kind == "bool":
            out.add("implicit")
        if c.exc:
            out.add("exception")
        return out


class CatCountOp(Op):
    name, qa_ok = "catcount", True

    def cols(self, t):
        return [c for c in cat_cols(t, "catcount") if c.sayp or (c.say and all(len(v) > 2 for v in c.say.values()))]

    def applicable(self, t):
        return len(t.rows) >= 4 and bool(self.cols(t))

    def sample(self, t, rng, want):
        if want == N:
            return None
        c = pick_col(self.cols(t), rng)
        vals = [t.get(e, c.key) for e in t.rows]
        if any(v is None for v in vals):
            return None
        X = rng.choice(vals + list(c.cats or [])[:1])
        k = vals.count(X)
        q = rng.choice(["exactly", "exactly", "at_least", "more_than", "fewer_than", "at_most"])
        opts = [(q, n) for n in range(1, len(vals) + 1) if not (q == "fewer_than" and n == 1)
                and k3(*q_poss(q, n, k, k)) == want and abs(n - k) <= 2]
        if not opts:
            return None
        q, n = rng.choice(opts)
        s = {"op": "catcount", "col": c.key, "X": X, "q": q, "n": n}
        return s if self.eval(t, s) == want else None

    def eval(self, t, s):
        vals = [t.get(e, s["col"]) for e in t.rows]
        if any(v is None for v in vals):
            return None
        k = vals.count(s["X"])
        return k3(*q_poss(s["q"], s["n"], k, k))

    def text(self, t, s):
        c = t.col(s["col"])
        n, q, tv = s["n"], s["q"], s["tv"]
        sg = n == 1
        p = cat_pred(c, s["X"], pl=not sg)
        pp = cat_pred(c, s["X"], pl=True)
        if p is None or pp is None:
            return None
        nw = num_or_word(n, s)
        sc = s["sc"]
        forms = [f"{QW[q]} {nw} {t.ent.sg if sg else t.ent.pl}{sc} {p}",
                 f"The number of {t.ent.pl}{sc} that {pp} is {QW2[q]} {n}"]
        return cap(ch(forms, tv, 1))

    def qa(self, t, s):
        if s["q"] != "exactly":
            return None
        c = t.col(s["col"])
        pp = cat_pred(c, s["X"], pl=True)
        return f"How many {t.ent.pl}{s['sc']} {pp}?", str(s["n"])

    def cells(self, t, s):
        return [x for e in t.rows for x in dep_cells(t, s["col"], e)]

    def mutate(self, t, s, rng):
        ns = [x for x in (s["n"] - 1, s["n"] + 1) if x >= 1 and not (s["q"] == "fewer_than" and x == 1)]
        return dict(s, n=rng.choice(ns)) if ns else None

    def edges(self, t, s):
        out = {"quantifier", "numeric"}
        if t.col(s["col"]).virtual:
            out.add("multi_hop")
        if t.col(s["col"]).exc:
            out.add("exception")
        return out


# ------------------------------------------------------------------------------------------------ hypothetical
class HypoOp(Op):
    name = "hypo"

    def cols(self, t):
        return [c for c in cols_for(t, "hypo", ("num", "money")) if not c.unl and not c.virtual
                and (c.vp is None or (c.vp.pp and c.vp.count and c.vp.obj1))]

    def sample(self, t, rng, want):
        if want == N:
            return None
        c = pick_col(self.cols(t), rng)
        ents = known(t, c)
        if len(ents) < 2:
            return None
        a, b = rng.sample(ents, 2)
        xa, xb = t.get(a, c.key), t.get(b, c.key)
        up = xa < xb if rng.random() < 0.8 else rng.random() < 0.5
        gap = abs(xb - xa)
        ns = nice_step(c, max(gap, c.step))
        cands = [gap, gap + c.step, gap - c.step, gap + ns, max(c.step, gap - ns), (gap // ns + 1) * ns, (gap // ns) * ns]
        cands = [d for d in cands if d > 0 and c.cv(d)]
        rng.shuffle(cands)
        for d in cands:
            s = {"op": "hypo", "col": c.key, "a": a, "b": b, "up": up, "d": int(d)}
            if self.eval(t, s) == want:
                return s
        return None

    def eval(self, t, s):
        c = t.col(s["col"])
        xa, xb = t.get(s["a"], c.key), t.get(s["b"], c.key)
        if xa is None or xb is None:
            return None
        if s["up"]:
            return T if xa + s["d"] > xb else F
        return T if xa - s["d"] < xb else F

    def text(self, t, s):
        c = t.col(s["col"])
        A, B = t.ent.r(s["a"]), t.ent.r(s["b"])
        D = c.cv(s["d"])
        hw, lw = c.words[0], c.words[1]
        w = hw if s["up"] else lw
        tv = s["tv"]
        if c.vp:
            vp = c.vp
            mf = "more" if s["up"] else "fewer"
            forms = [f"Had {A} {vp.pp} {D} {mf} {vp.cobj}{vp.suffix}, it would have {vp.pp} {mf} {vp.cobj} than {B}",
                     f"If {A} had {vp.pp} {D} {mf} {vp.cobj}{vp.suffix}, it would have {vp.pp} {mf} {vp.cobj} than {B}"]
        else:
            forms = [f"If {poss(A)} {c.cmpnoun} were {D} {w}, it would be {w} than {poss(B)}"]
            if s["up"]:
                forms.append(f"Adding {D} to {poss(A)} {c.cmpnoun} would make it {hw} than {poss(B)}")
        return cap(ch(forms, tv, 1))

    def cells(self, t, s):
        return [(s["a"], s["col"]), (s["b"], s["col"])]

    def consts(self, t, s):
        c = t.col(s["col"])
        xa, xb = t.get(s["a"], c.key), t.get(s["b"], c.key)
        return [(c.key, xb - s["d"]), (c.key, xa + s["d"]), (c.key, xb + s["d"]), (c.key, xa - s["d"])]

    def mutate(self, t, s, rng):
        c = t.col(s["col"])
        cands = [x for x in (s["d"] + c.step, s["d"] - c.step, s["d"] + nice_step(c, s["d"])) if x > 0 and c.cv(x)]
        return dict(s, d=rng.choice(cands)) if cands else None

    def edges(self, t, s):
        return col_edges(t, t.col(s["col"]), s) | {"hypothetical", "numeric"}


# ------------------------------------------------------------------------------------------------ share of a total
class ShareOp(Op):
    """'X accounts for more than 25% of the total' (one row, or the rows of one category), exact fractions."""
    name = "share"

    def cols(self, t):
        return [c for c in cols_for(t, "share", ("num", "money")) if c.sum and c.sum_all and c.nonneg and not c.unl
                and not c.virtual]

    def applicable(self, t):
        return len(t.rows) >= 4 and bool(self.cols(t))

    def _parts(self, t, s):
        c = t.col(s["col"])
        vals = [t.get(e, c.key) for e in t.rows]
        if any(v is None or not is_int(v) for v in vals) or sum(vals) <= 0:
            return None
        if s["form"] == "ent":
            part = t.get(s["e"], c.key)
        else:
            mem = members(t, s)
            if len(mem) < 1 or len(mem) == len(t.rows):
                return None
            part = sum(t.get(e, c.key) for e in mem)
        return Fr(part * 100, sum(vals))

    def sample(self, t, rng, want):
        if want == N:
            return None
        c = pick_col(self.cols(t), rng)
        s = {"op": "share", "col": c.key, "rel": rng.choice(["gt", "lt", "ge"]),
             "sc": rng.choice([" shown", " listed"]) if t.partial else rng.choice(["", " in the table", " listed"])}
        if rng.random() < 0.4:
            f = pick_filter(t, rng, minsize=1)
            if not f:
                return None
            s.update(form="grp", filt=f)
        else:
            s.update(form="ent", e=rng.choice(t.rows))
        x = self._parts(t, s)
        if x is None:
            return None
        base = int(x)
        cands = [base, base + 1, base - 1, (base // 5) * 5, (base // 5 + 1) * 5, (base // 10) * 10, (base // 10 + 1) * 10]
        if x.denominator == 1:
            cands += [int(x)] * 4
        cands = [p for p in cands if 1 <= p <= 99]
        rng.shuffle(cands)
        for p in cands:
            if self.eval(t, dict(s, p=p)) == want:
                s["p"] = p
                return s
        return None

    def eval(self, t, s):
        x = self._parts(t, s)
        if x is None:
            return None
        return T if holds(x, s["rel"], s["p"]) else F

    def text(self, t, s):
        c = t.col(s["col"])
        rw = {"gt": "more than", "lt": "less than", "ge": "at least"}[s["rel"]]
        tot = f"the total {c.noun} across the {t.ent.pl}{s['sc']}"
        if s["form"] == "ent":
            E = t.ent.r(s["e"])
            forms = [f"{E} accounts for {rw} {s['p']}% of {tot}", f"{rw.capitalize()} {s['p']}% of {tot} comes from {E}"]
        else:
            G = f"the {t.ent.pl}{filt_phrase(t, s)}"
            forms = [f"{G} account for {rw} {s['p']}% of {tot}", f"{G} together make up {rw} {s['p']}% of {tot}"]
        return cap(ch(forms, s["tv"], 1))

    def cells(self, t, s):
        return [(e, s["col"]) for e in t.rows]

    def consts(self, t, s):
        return []

    def mutate(self, t, s, rng):
        return dict(s, p=max(1, min(99, s["p"] + rng.choice([-5, -2, -1, 1, 2, 5]))))

    def edges(self, t, s):
        return col_edges(t, t.col(s["col"]), s) | {"numeric", "multi_hop"}


# ------------------------------------------------------------------------------------------------ ratios
RATIOS = {"twice_ge": (2, "ge"), "twice_gt": (2, "gt"), "three_gt": (3, "gt"), "half_lt": (Fr(1, 2), "lt"),
          "half_ge": (Fr(1, 2), "ge")}


class RatioOp(Op):
    name, n_ok = "ratio", True

    def cols(self, t):
        return [c for c in cols_for(t, "ratio", ("num", "money")) if c.nonneg and not c.unl and not c.signed]

    def sample(self, t, rng, want):
        cs = self.cols(t)
        if want == N:
            cs = [c for c in cs if not c.virtual and not c.nomiss]
        if not cs:
            return None
        c = pick_col(cs, rng)
        ents = [e for e in known(t, c) if is_int(t.get(e, c.key)) and t.get(e, c.key) > 0]
        if len(ents) < 2:
            return None
        forms = list(RATIOS)
        rng.shuffle(forms)
        pairs = [(a, b) for a in ents for b in ents if a != b]
        rng.shuffle(pairs)
        for a, b in pairs[:30]:
            for f in forms:
                sp = {"op": "ratio", "col": c.key, "a": a, "b": b, "form": f}
                if want == N:
                    if self.eval(t, sp) is None:
                        continue
                    side = rng.choice(["a", "b"])
                    absent = [p for p in t.pool if p not in t.v]
                    if t.partial and absent and rng.random() < 0.4:
                        sp[side] = rng.choice(absent)
                    elif can_blank(t, sp[side], c):
                        t.v[sp[side]][c.key] = None
                    else:
                        return None
                    return sp if self.eval(t, sp) == N else None
                if self.eval(t, sp) == want:
                    return sp
        return None

    def eval(self, t, s):
        c = t.col(s["col"])
        k, r = RATIOS[s["form"]]
        (alo, ahi), (blo, bhi) = ival(t, c, s["a"]), ival(t, c, s["b"])
        return k3(*rel_poss(r, (alo, ahi), (blo * k, bhi * k if bhi != INF else INF)))

    def text(self, t, s):
        c = t.col(s["col"])
        A, B = t.ent.r(s["a"]), t.ent.r(s["b"])
        f = s["form"]
        if c.vp and c.vp.count:
            vp = c.vp
            q = {"twice_ge": "at least twice as many", "twice_gt": "more than twice as many",
                 "three_gt": "more than three times as many", "half_lt": "less than half as many",
                 "half_ge": "at least half as many"}[f]
            return cap(f"{A} {vp.verb} {q} {vp.cobj}{vp.suffix} as {B}")
        q = {"twice_ge": "at least twice", "twice_gt": "more than twice", "three_gt": "more than three times",
             "half_lt": "less than half of", "half_ge": "at least half of"}[f]
        return cap(ch([f"{poss(A)} {c.cmpnoun} is {q} {poss(B)}"], s["tv"]))

    def cells(self, t, s):
        return dep_cells(t, s["col"], s["a"]) + dep_cells(t, s["col"], s["b"])

    def consts(self, t, s):
        c = t.col(s["col"])
        k, r = RATIOS[s["form"]]
        out = []
        xa = t.get(s["a"], c.key) if s["a"] in t.v else None
        xb = t.get(s["b"], c.key) if s["b"] in t.v else None
        if xb is not None and is_int(xb):
            y = xb * k
            out += [(c.key, int(y)), (c.key, int(y) + 1), (c.key, int(y) - 1)]
        if xa is not None and is_int(xa):
            y = Fr(xa) / k
            out += [(c.key, int(y)), (c.key, int(y) + 1), (c.key, int(y) - 1)]
        return out

    def mutate(self, t, s, rng):
        others = [f for f in RATIOS if f != s["form"]]
        return dict(s, form=rng.choice(others))

    def edges(self, t, s):
        return col_edges(t, t.col(s["col"]), s) | {"numeric", "multi_hop"}


# ------------------------------------------------------------------------------------------------ only
class OnlyOp(Op):
    name = "only"

    def cols(self, t):
        return [c for c in cols_for(t, "only") if not c.unl]

    def applicable(self, t):
        return len(t.rows) >= 3 and bool(self.cols(t))

    def sample(self, t, rng, want):
        if want == N:
            return None
        c = pick_col(self.cols(t), rng)
        vals = sorted({t.get(e, c.key) for e in t.rows if t.get(e, c.key) is not None and is_int(t.get(e, c.key))})
        if len(vals) < 3:
            return None
        rel = rng.choice(["gt", "lt", "ge", "le"])
        hi = rel in ("gt", "ge")
        pivots = vals[-3:] if hi else vals[:3]
        for _ in range(12):
            v = rng.choice(near(c, rng.choice(pivots), rng, vals))
            if not ok_const(c, v):
                continue
            sats = [e for e in t.rows if t.get(e, c.key) is not None and holds(t.get(e, c.key), rel, v)]
            if not sats:
                continue
            e = rng.choice(sats) if (want == T or rng.random() < 0.6) else rng.choice(t.rows)
            sp = {"op": "only", "col": c.key, "rel": rel, "v": v, "e": e}
            if self.eval(t, sp) == want:
                return sp
        return None

    def eval(self, t, s):
        c = t.col(s["col"])
        vals = {e: t.get(e, c.key) for e in t.rows}
        if any(v is None for v in vals.values()) or s["e"] not in vals:
            return None
        sats = [e for e, v in vals.items() if holds(v, s["rel"], s["v"])]
        return T if sats == [s["e"]] else F

    def text(self, t, s):
        c = t.col(s["col"])
        V = vs(c, s["v"], s)
        p = pred(c, s["rel"], V, s["v"], pl=False, tv=s["tv"])
        if p is None:
            return None
        E = t.ent.r(s["e"])
        sc = s.get("sc", "")
        second = f"Of the {t.ent.pl} shown, only {E} {p}" if t.partial else f"Only {E} {p}"
        return cap(ch([f"{E} is the only {t.ent.sg}{sc} that {p}", second], s["tv"], 1))

    def cells(self, t, s):
        return [x for e in t.rows for x in dep_cells(t, s["col"], e)]

    def consts(self, t, s):
        return [(s["col"], s["v"])]

    def mutate(self, t, s, rng):
        others = [e for e in t.rows if e != s["e"]]
        return dict(s, e=rng.choice(others)) if others else None

    def edges(self, t, s):
        return col_edges(t, t.col(s["col"]), s) | {"quantifier", "exception"}


# ------------------------------------------------------------------------------------------------ both / neither / either
def k_and(a, b):
    if F in (a, b):
        return F
    if a == T and b == T:
        return T
    return N


def k_not(a):
    return {T: F, F: T}.get(a, a)


class BoolOp(Op):
    name, n_ok = "bool", True

    def cols(self, t):
        return [c for c in cols_for(t, "bool") if not c.unl]

    def _st(self, t, s, e):
        c = t.col(s["col"])
        return k3(*rel_poss(s["rel"], ival(t, c, e), (s["v"], s["v"])))

    def sample(self, t, rng, want):
        cs = self.cols(t)
        if want == N:
            cs = [c for c in cs if not c.virtual and not c.nomiss]
        if not cs or len(t.rows) < 2:
            return None
        c = pick_col(cs, rng)
        form = rng.choice(["both", "neither", "either", "a_not_b"])
        rel = rng.choice(["gt", "lt"] + (["ge", "le"] if form != "a_not_b" else []))
        ents = known(t, c)
        if len(ents) < 2:
            return None
        a, b = rng.sample(ents, 2)
        xa, xb = t.get(a, c.key), t.get(b, c.key)
        if xa == INF or xb == INF or not is_int(xa) or not is_int(xb):
            return None
        cands = near(c, int(rng.choice([xa, xb])), rng, [xa, xb])
        rng.shuffle(cands)
        for v in cands:
            if not ok_const(c, v):
                continue
            sp = {"op": "bool", "col": c.key, "form": form, "rel": rel, "a": a, "b": b, "v": v}
            if want == N:
                if self.eval(t, sp) is None:
                    continue
                side = rng.choice(["a", "b"])
                saved = t.v[sp[side]].get(c.key)
                if not can_blank(t, sp[side], c):
                    continue
                t.v[sp[side]][c.key] = None
                if self.eval(t, sp) == N:
                    return sp
                t.v[sp[side]][c.key] = saved
                continue
            if self.eval(t, sp) == want:
                return sp
        return None

    def eval(self, t, s):
        sa, sb = self._st(t, s, s["a"]), self._st(t, s, s["b"])
        f = s["form"]
        if f == "both":
            return k_and(sa, sb)
        if f == "neither":
            return k_and(k_not(sa), k_not(sb))
        if f == "either":
            return k_not(k_and(k_not(sa), k_not(sb)))
        return k_and(sa, k_not(sb))

    def text(self, t, s):
        c = t.col(s["col"])
        V = vs(c, s["v"], s)
        A, B = t.ent.r(s["a"]), t.ent.r(s["b"])
        tv = s["tv"]
        psg = pred(c, s["rel"], V, s["v"], pl=False, tv=tv)
        ppl = pred(c, s["rel"], V, s["v"], pl=True, tv=tv)
        if psg is None or ppl is None:
            return None
        f = s["form"]
        if f == "both":
            forms = [f"Both {A} and {B} {ppl}", f"{A} and {B} both {ppl}"]
        elif f == "neither":
            forms = [f"Neither {A} nor {B} {psg}"]
        elif f == "either":
            forms = [f"At least one of {A} and {B} {psg}", f"{A} or {B} (or both) {ppl}"]
        else:
            pn = pred(c, s["rel"], V, s["v"], pl=False, neg=True, tv=tv)
            if pn is None:
                return None
            forms = [f"{A} {psg}, but {B} {pn}"]
        return cap(ch(forms, tv, 1))

    def cells(self, t, s):
        return dep_cells(t, s["col"], s["a"]) + dep_cells(t, s["col"], s["b"])

    def consts(self, t, s):
        return [(s["col"], s["v"])]

    def mutate(self, t, s, rng):
        c = t.col(s["col"])
        cands = [v for v in near(c, s["v"], rng) if v != s["v"] and ok_const(c, v)]
        return dict(s, v=rng.choice(cands)) if cands else None

    def edges(self, t, s):
        out = col_edges(t, t.col(s["col"]), s) | {"quantifier", "multi_hop"}
        if s["form"] in ("neither", "a_not_b"):
            out.add("negation")
        return out


GENERIC = {o.name: o for o in (ValOp(), ThrOp(), CmpOp(), DiffOp(), SupOp(), RankOp(), CountOp(), QuantOp(), SumOp(),
                                AvgOp(), ArgThenOp(), CatValOp(), CatCountOp(), HypoOp(), ShareOp(), RatioOp(), OnlyOp(), BoolOp())}


def vbad(t, s):
    """Claims about computed (virtual) columns are only emitted when every row's computed value is known and every
    entity they mention is listed: a blank input never yields 'not enough information' for them (a computed value can
    be settled by a rule even when an input is blank, e.g. a Discontinued item never needs reordering)."""
    for k in ("col", "c1", "c2"):
        key = s.get(k)
        if not key or key.startswith("_"):
            continue
        c = t.col(key)
        if not c.virtual:
            continue
        if any(x not in t.v for x in (s.get("e"), s.get("a"), s.get("b")) if x is not None):
            return True
        if any(t.get(e, key) is None for e in t.rows):
            return True
    return False


def _guard(fn):
    def g(t, s):
        if vbad(t, s):
            return None
        return fn(t, s)
    return g


for _o in GENERIC.values():
    _o.eval = _guard(_o.eval)

"""rk_core: shared helpers for gen_ranking (formatting, attribute constructors, and the PRIMARY evaluator of a
multi-attribute selection spec).  The spec is plain JSON-able data so that rk_verify.py can re-derive every label
with an independent implementation.

Spec (JSON-able):
  cands   [{"label": "Bid A", "name": "...", "v": {attr: value | None(missing)}}]   (listed order)
  kinds   {attr: "num" | "bool" | "cat" | "panel"}                                    (for used attrs)
  gates   [{"a": attr, "op": "ge|gt|le|lt|in|true", "t": value, "exc": None | {"a": flag, "mode": "relax|waive", "t2": v}}]
  mech    {"type": "weighted", "crit": [[attr, w], ...], "div": d}          total = sum(w * score) / d
          {"type": "cost", "comp": [...]}                                    lower total cost ranks higher
          {"type": "banded", "bands": [[attr, [[lo, hi, pts], ...]], ...]}  lo/hi inclusive, None = open
          {"type": "ratio", "comp": [...], "wp": p, "qual": attr, "wq": q, "qmax": m}
          {"type": "lexi", "keys": [[attr, "high|low"], ...]}
          {"type": "panel", "agg": "mean|median|trim|sum"}                 attr "panel" holds the judges' scores
          {"type": "linear", "terms": [[attr, coef], ...]}
          {"type": "first"}                                                 first qualifying by attr "received"
  tb      [[attr | "@cost", "high|low"], ...]   tb_final "lots" (ties left unresolved) | "none" (chain always decides)
  missing {"score": "zero" | None, "bool": "fail" | None}; enum {attr: [possible values]} for unresolved missing cells
  corr    [[i, attr, new_value]]  (a printed correction overrides the listed value)
  ctx     {name: number}
  target  {"kind": "best|second|last", "hypo": None | {"type": "withdraw", "i": k} | {"type": "drop", "a": attr}
           | {"type": "gate", "g": gi, "t": new_t} | {"type": "nogate", "g": gi} | {"type": "ctx", "k": key, "v": val}}
Outcomes: a candidate label, NONE (nobody qualifies), TIE (the rules leave a tie at the asked position), UNDET (a
missing value could change the answer).
Cost components: ["mul", attr, [ctx keys]] value x product(ctx); ["add", attr];
  ["cond", attr, flag, flag_value, [ctx keys]] added only when v[flag] == flag_value;
  ["tier", base_attr, bulk_attr, thr_attr, ctx_key] unit price = bulk if ctx >= v[thr] else base, x ctx.
"""
import copy
import itertools
from fractions import Fraction as Fr

NONE, TIE, UNDET = "NONE", "TIE", "UNDET"
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]
MON3 = [m[:3] for m in MONTHS]
DAYS_IN = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


# ------------------------------------------------------------------------------------------------ number formatting
def fmt_int(n):
    return f"{n:,}"


def fmt_dec(v, dp):
    """v is an int scaled by 10**dp."""
    if dp == 0:
        return f"{v:,}"
    s = "-" if v < 0 else ""
    v = abs(v)
    q, r = divmod(v, 10 ** dp)
    return f"{s}{q:,}.{r:0{dp}d}"


def fmt_money(v, cur="$", minor=100, force_dec=False):
    """v in minor units.  cur 'p' = pence stored in tenths of a penny."""
    if cur == "p":
        q, r = divmod(v, 10)
        return f"{q}.{r}p"
    if minor == 100:
        q, r = divmod(v, 100)
        s = f"{q:,}" if (r == 0 and not force_dec) else f"{q:,}.{r:02d}"
    elif minor == 1000:
        q, r = divmod(v, 1000)
        rs = f"{r:03d}"
        if rs.endswith("0"):
            rs = rs[:2]
        s = f"{q:,}.{rs}"
    else:
        raise ValueError(minor)
    return f"{cur}{s}"


def money_exact(fr, cur="$", minor=100):
    """Exact Fraction amount in minor units -> string with enough decimals (for rules text only)."""
    if fr.denominator == 1:
        return fmt_money(int(fr), cur, minor)
    raise ValueError("non-integral money")


def unit(n, u):
    """u = (singular, plural)."""
    if isinstance(u, str):
        return f"{fmt_int(n) if isinstance(n, int) else n}{u}"
    return f"{fmt_int(n) if isinstance(n, int) else n} {u[0] if n == 1 else u[1]}"


# ------------------------------------------------------------------------------------------------ dates and times
def ymd(day_index, year=2026):
    """day_index 0 = 1 Jan of `year` (non-leap unless 2028)."""
    dim = list(DAYS_IN)
    if year % 4 == 0:
        dim[1] = 29
    m = 0
    d = day_index
    while d >= dim[m]:
        d -= dim[m]
        m += 1
    return m, d + 1


def weekday(day_index, year=2026):
    base = {2026: 3, 2027: 4, 2028: 5}[year]  # 1 Jan 2026 = Thursday (index 3)
    return WEEKDAYS[(base + day_index) % 7]


def fmt_date(day_index, style=0, year=2026):
    m, d = ymd(day_index, year)
    if style == 0:
        return f"{d} {MONTHS[m]} {year}"
    if style == 1:
        return f"{MONTHS[m]} {d}, {year}"
    if style == 2:
        return f"{year}-{m + 1:02d}-{d:02d}"
    if style == 3:
        return f"{d} {MON3[m]}"
    return f"{weekday(day_index, year)} {d} {MONTHS[m]}"


def fmt_time(minute_of_day, style=0):
    h, m = divmod(minute_of_day, 60)
    if style == 0:
        return f"{h:02d}:{m:02d}"
    ap = "am" if h < 12 else "pm"
    hh = h % 12 or 12
    return f"{hh}:{m:02d} {ap}" if m else f"{hh} {ap}"


def fmt_dt(stamp, dstyle=0, tstyle=0):
    """stamp = minutes since 1 Jan 2026 00:00."""
    day, mod = divmod(stamp, 1440)
    return f"{fmt_date(day, 3 if dstyle == 0 else 0)}, {fmt_time(mod, tstyle)}" if dstyle in (0, 1) else \
        f"{fmt_date(day, 2)} {fmt_time(mod, 0)}"


def fmt_dur(minutes, style=0):
    h, m = divmod(minutes, 60)
    if style == 0:
        return f"{h}h {m:02d}m"
    if style == 1:
        return f"{h} h {m} min" if m else f"{h} h"
    return f"{minutes} min"


# ------------------------------------------------------------------------------------------------ primary evaluator
def cval(sc, i, a):
    for ci, ca, nv in sc.get("corr", []):
        if ci == i and ca == a:
            return nv
    return sc["cands"][i]["v"].get(a)


def used_attrs(sc):
    """Attributes the rules read (gates, mechanism, tie-breaks, exception flags)."""
    out = []
    for g in sc["gates"]:
        out.append(g["a"])
        if g.get("exc"):
            out.append(g["exc"]["a"])
    m = sc["mech"]
    t = m["type"]
    if t == "weighted":
        out += [a for a, _ in m["crit"]]
    elif t in ("cost",):
        out += comp_attrs(m["comp"])
    elif t == "ratio":
        out += comp_attrs(m["comp"]) + [m["qual"]]
    elif t == "banded":
        out += [a for a, _ in m["bands"]]
    elif t == "lexi":
        out += [a for a, _ in m["keys"]]
    elif t == "panel":
        out.append("panel")
    elif t == "linear":
        out += [a for a, _ in m["terms"]]
    elif t == "first":
        out.append("received")
    for a, _ in sc.get("tb", []):
        if a == "@cost":
            out += comp_attrs(sc["cost_comp"])
        else:
            out.append(a)
    return list(dict.fromkeys(out))


def comp_attrs(comp):
    out = []
    for c in comp:
        if c[0] == "mul":
            out.append(c[1])
            out += [k[1:] for k in c[2] if k.startswith("@")]
        elif c[0] == "add":
            out.append(c[1])
        elif c[0] == "cond":
            out += [c[1], c[2]]
        elif c[0] == "tier":
            out += [c[1], c[2], c[3]]
    return out


def cost_of(comp, get, ctx):
    tot = Fr(0)
    for c in comp:
        if c[0] == "mul":
            x = Fr(get(c[1]))
            for k in c[2]:
                x *= get(k[1:]) if k.startswith("@") else ctx[k]
            tot += x
        elif c[0] == "add":
            tot += get(c[1])
        elif c[0] == "cond":
            if get(c[2]) == c[3]:
                x = Fr(get(c[1]))
                for k in c[4]:
                    x *= ctx[k]
                tot += x
        elif c[0] == "tier":
            q = ctx[c[4]]
            u = get(c[2]) if q >= get(c[3]) else get(c[1])
            tot += Fr(u) * q
        else:
            raise ValueError(c)
    return tot


def apply_hypo(sc):
    """Return (spec with the question's supposed change applied, set of withdrawn indices)."""
    h = sc["target"].get("hypo")
    if not h:
        return sc, set()
    s = copy.deepcopy(sc)
    if h["type"] == "withdraw":
        return s, {h["i"]}
    if h["type"] == "drop":
        s["mech"]["crit"] = [[a, w] for a, w in s["mech"]["crit"] if a != h["a"]]
        s["tb"] = [[a, d] for a, d in s["tb"] if a != h["a"]]
    elif h["type"] == "gate":
        s["gates"][h["g"]]["t"] = h["t"]
    elif h["type"] == "nogate":
        s["gates"] = [g for k, g in enumerate(s["gates"]) if k != h["g"]]
    elif h["type"] == "ctx":
        s["ctx"][h["k"]] = h["v"]
    else:
        raise ValueError(h)
    return s, set()


def missing_cells(sc):
    """(i, attr) cells that the rules read but that are missing and not covered by a missing-value rule."""
    used = set(used_attrs(sc))
    out = []
    for i, c in enumerate(sc["cands"]):
        for a in sorted(used):
            if a == "panel":
                continue
            if cval(sc, i, a) is None:
                k = sc["kinds"][a]
                if k == "num" and sc["missing"].get("score") == "zero" and a in sc.get("scores", []):
                    continue
                if k == "bool" and sc["missing"].get("bool") == "fail":
                    continue
                out.append((i, a))
    return out


def _getter(sc, i, fill):
    def get(a):
        v = cval(sc, i, a)
        if v is None:
            if (i, a) in fill:
                return fill[(i, a)]
            k = sc["kinds"][a]
            if k == "bool" and sc["missing"].get("bool") == "fail":
                return False
            if sc["missing"].get("score") == "zero" and a in sc.get("scores", []):
                return 0
            raise KeyError((i, a))
        return v
    return get


def gate_pass(g, get):
    v = get(g["a"])
    op, t = g["op"], g["t"]
    exc = g.get("exc")
    if exc:
        if get(exc["a"]):
            if exc["mode"] == "waive":
                return True
            t = exc["t2"]
    if op == "true":
        return bool(v) is True
    if op == "false":
        return bool(v) is False
    if op == "in":
        return v in t
    if op == "ge":
        return v >= t
    if op == "gt":
        return v > t
    if op == "le":
        return v <= t
    if op == "lt":
        return v < t
    raise ValueError(op)


def band_pts(bands, v):
    for lo, hi, pts in bands:
        if (lo is None or v >= lo) and (hi is None or v <= hi):
            return pts
    raise ValueError(("no band", v, bands))


def median(xs):
    xs = sorted(xs)
    n = len(xs)
    if n % 2:
        return Fr(xs[n // 2])
    return Fr(xs[n // 2 - 1] + xs[n // 2], 2)


def primary(sc, i, get, pool_cost_min):
    m = sc["mech"]
    t = m["type"]
    if t == "weighted":
        return (sum(Fr(w) * get(a) for a, w in m["crit"]) / m["div"],)
    if t == "cost":
        return (-cost_of(m["comp"], get, sc["ctx"]),)
    if t == "banded":
        return (sum(Fr(band_pts(b, get(a))) for a, b in m["bands"]),)
    if t == "ratio":
        c = cost_of(m["comp"], get, sc["ctx"])
        return (Fr(m["wp"]) * pool_cost_min / c + Fr(m["wq"]) * get(m["qual"]) / m["qmax"],)
    if t == "lexi":
        return tuple(Fr(get(a)) if d == "high" else -Fr(get(a)) for a, d in m["keys"])
    if t == "panel":
        xs = sc["cands"][i]["v"]["panel"]
        agg = m["agg"]
        if agg == "mean":
            return (Fr(sum(xs), len(xs)),)
        if agg == "sum":
            return (Fr(sum(xs)),)
        if agg == "median":
            return (median(xs),)
        if agg == "trim":
            ys = sorted(xs)[1:-1]
            return (Fr(sum(ys), len(ys)),)
    if t == "linear":
        return (sum(Fr(c) * get(a) for a, c in m["terms"]),)
    if t == "first":
        return (-Fr(get("received")),)
    raise ValueError(t)


def full_key(sc, i, get, pool_cost_min):
    k = list(primary(sc, i, get, pool_cost_min))
    for a, d in sc.get("tb", []):
        x = cost_of(sc["cost_comp"], get, sc["ctx"]) if a == "@cost" else Fr(get(a))
        k.append(x if d == "high" else -x)
    return tuple(k)


def eval_complete(sc, fill):
    s, gone = apply_hypo(sc)
    idx = [i for i in range(len(s["cands"])) if i not in gone]
    getters = {i: _getter(s, i, fill) for i in idx}
    qual = [i for i in idx if all(gate_pass(g, getters[i]) for g in s["gates"])]
    kind = s["target"]["kind"]
    if not qual:
        # 'second' / 'last' option sets have no 'no <x> qualifies' option (reviewer fix): such items are rejected
        return NONE if kind == "best" else "REJECT"
    if kind in ("second", "last") and len(qual) < 2:
        return "REJECT"
    pmin = None
    if s["mech"]["type"] == "ratio":
        pmin = min(cost_of(s["mech"]["comp"], getters[i], s["ctx"]) for i in qual)
    keys = {i: full_key(s, i, getters[i], pmin) for i in qual}
    order = sorted(qual, key=lambda i: keys[i], reverse=True)
    groups = []
    for i in order:
        if groups and keys[groups[-1][0]] == keys[i]:
            groups[-1].append(i)
        else:
            groups.append([i])
    if kind == "best":
        g = groups[0]
    elif kind == "last":
        g = groups[-1]
    else:  # second position
        pos = 0
        g = None
        for gg in groups:
            if pos <= 1 < pos + len(gg):
                g = gg
                break
            pos += len(gg)
    if len(g) > 1:
        return TIE
    return s["cands"][g[0]]["label"]


def evaluate(sc, want_all=False):
    cells = missing_cells(sc)
    if not cells:
        out = eval_complete(sc, {})
        return (out, {out}) if want_all else out
    doms = [sc["enum"][a] for _, a in cells]
    outs = set()
    for combo in itertools.product(*doms):
        outs.add(eval_complete(sc, dict(zip(cells, combo))))
    if "REJECT" in outs:
        out = "REJECT"
    else:
        out = next(iter(outs)) if len(outs) == 1 else UNDET
    return (out, outs) if want_all else out


def ranking(sc):
    """Full ranking (list of groups of labels) with no hypothetical, for diagnostics; requires no missing cells."""
    s = copy.deepcopy(sc)
    s["target"] = {"kind": "best", "hypo": None}
    getters = {i: _getter(s, i, {}) for i in range(len(s["cands"]))}
    qual = [i for i in range(len(s["cands"])) if all(gate_pass(g, getters[i]) for g in s["gates"])]
    if not qual:
        return [], []
    pmin = None
    if s["mech"]["type"] == "ratio":
        pmin = min(cost_of(s["mech"]["comp"], getters[i], s["ctx"]) for i in qual)
    keys = {i: full_key(s, i, getters[i], pmin) for i in qual}
    order = sorted(qual, key=lambda i: keys[i], reverse=True)
    return [s["cands"][i]["label"] for i in order], [keys[i] for i in order]


_ART = __import__("re").compile(r"\b([Aa]) (?=(\d[\d,.]*))")


def fix_articles(text):
    """'a 8 min walk' -> 'an 8 min walk', 'a 11-day' -> 'an 11-day', 'a 18%' -> 'an 18%'."""
    import re

    def rep(m):
        num = m.group(2)
        head = num.split(".")[0]
        an = head.startswith("8") or re.fullmatch(r"(11|18)(,\d{3})*", head) is not None
        return (("An" if m.group(1) == "A" else "an") if an else m.group(1)) + " "
    return _ART.sub(rep, text)

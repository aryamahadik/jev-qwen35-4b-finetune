"""Independent verifier for gen_constraints rows.

It does NOT trust the generator's stored option values or its evaluator:
  1. every displayed value is located in its option's text segment (table row, bullet, card, prose sentence, or the
     attribute row of a transposed table) and PARSED BACK from the text with parsers written here (money, decimals
     with units, 12/24-hour times, four date styles incl. weekday check, durations, yes/no styles, sets, the
     unknown / not-applicable tokens, special words such as 'nonstop');
  2. correction notes are found in the text and their values parsed; they replace the listed values;
  3. every requirement is re-evaluated on the parsed values with a separately written evaluator (own Kleene logic,
     own business-day and conversion arithmetic), qualifiers and the tie-break are recomputed and the gold label
     must match;
  4. every requirement's rendered wording is checked against its spec: the comparator phrase right before the
     threshold must mean the spec's operator after applying a 'must not / cannot' modal, bool wording polarity,
     category / set wording (quantifier words), context facts (party size, listed names, time-zone offset, unit
     conversion notes) must be present;
  5. cross-unit requirements must give the same verdict under the stated and the exact conversion factor.
"""
import datetime as dt
import re
from fractions import Fraction as Fr

MON3 = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
WD3 = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
UNKNOWN, NOTAPP = ("UNK",), ("NA",)

# comparator phrases -> meaning of '<value' relation (value on the right)
V_LEX = {
    "at most": "<=", "no more than": "<=", "not more than": "<=", "a maximum of": "<=", "up to": "<=",
    "less than": "<", "under": "<", "below": "<", "fewer than": "<",
    "at least": ">=", "no less than": ">=", "not less than": ">=", "a minimum of": ">=", "no fewer than": ">=",
    "not fewer than": ">=",
    "more than": ">", "over": ">", "above": ">",
    "by": "<=", "no later than": "<=", "at or before": "<=", "not later than": "<=", "on or before": "<=",
    "before": "<", "earlier than": "<",
    "no earlier than": ">=", "at or after": ">=", "not earlier than": ">=", "on or after": ">=",
    "after": ">", "later than": ">",
}
NEG_FLIP = {"<=": ">", ">": "<=", ">=": "<", "<": ">="}
NEG_MODAL = re.compile(r"^(must not|cannot|can't)\b", re.I)
POS_MODAL = re.compile(r"^(must|has to|needs to)\b", re.I)


class VerifyError(AssertionError):
    pass


def need(cond, msg):
    if not cond:
        raise VerifyError(msg)


# ------------------------------------------------------------------------------------------------ parsers
def p_money(s):
    m = re.fullmatch(r"([$€£])([\d,]+)(?:\.(\d{2}))?", s)
    need(m, f"money {s!r}")
    return int(m.group(2).replace(",", "")) * 100 + (int(m.group(3)) if m.group(3) else 0)


def p_dec(s, scale):
    m = re.fullmatch(r"(-?)([\d,]+)(?:\.(\d+))?", s)
    need(m, f"number {s!r}")
    whole = int(m.group(2).replace(",", ""))
    frac = m.group(3) or ""
    digits = {1: 0, 10: 1, 100: 2, 1000: 3}[scale]
    need(len(frac) == digits, f"decimals {s!r} scale {scale}")
    v = whole * scale + (int(frac) if frac else 0)
    return -v if m.group(1) else v


def p_time(s):
    m = re.fullmatch(r"(\d{1,2}):(\d{2})(?: (am|pm))?", s)
    need(m, f"time {s!r}")
    h, mi = int(m.group(1)), int(m.group(2))
    if m.group(3):
        need(1 <= h <= 12, s)
        h = h % 12 + (12 if m.group(3) == "pm" else 0)
    else:
        need(len(m.group(1)) == 2, f"24h time needs 2 digits {s!r}")
    return h * 60 + mi


def p_date(s, today):
    s0 = s
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3))).toordinal()
    m = re.fullmatch(r"([A-Za-z]+),? (\d{1,2}) ([A-Za-z]+)", s) or None
    if m:
        wd, day, mon = m.group(1), int(m.group(2)), m.group(3)
    else:
        m = re.fullmatch(r"([A-Za-z]+), ([A-Za-z]+) (\d{1,2})", s)
        need(m, f"date {s0!r}")
        wd, mon, day = m.group(1), m.group(2), int(m.group(3))
    mo = MON3.index(mon[:3].lower()) + 1
    best = None
    ty = dt.date.fromordinal(today).year
    for y in (ty - 1, ty, ty + 1):
        try:
            d = dt.date(y, mo, day).toordinal()
        except ValueError:
            continue
        if best is None or abs(d - today) < abs(best - today):
            best = d
    need(best is not None, f"date {s0!r}")
    need(WD3[dt.date.fromordinal(best).weekday()] == wd[:3].lower(), f"weekday mismatch {s0!r}")
    return best


def p_dur(s):
    m = re.fullmatch(r"(\d+) h (\d{2}) min", s) or re.fullmatch(r"(\d+)h(\d{2})", s)
    if m:
        return int(m.group(1)) * 60 + int(m.group(2))
    m = re.fullmatch(r"(\d+) min", s)
    need(m, f"duration {s!r}")
    return int(m.group(1))


def parse_value(A, s, st, ctx, prose_bool=False):
    if s == st["missing"]:
        return UNKNOWN
    if s == st["na"]:
        return NOTAPP
    sp = getattr(A, "special", None)
    if sp:
        for k, v in sp.items():
            if s == v:
                return k
    k = A.kind
    if k == "money":
        return p_money(s)
    if k == "num":
        if A.unit is None:
            return p_dec(s, A.scale)
        if isinstance(A.unit, tuple):
            m = re.fullmatch(r"(\S+) (.+)", s)
            need(m and m.group(2) in A.unit, f"unit {s!r} {A.unit}")
            return p_dec(m.group(1), A.scale)
        need(s.endswith(A.unit), f"suffix {s!r} {A.unit!r}")
        return p_dec(s[:len(s) - len(A.unit)], A.scale)
    if k == "time":
        return p_time(s)
    if k == "date":
        return p_date(s, ctx["today"])
    if k == "dur":
        return p_dur(s)
    if k == "bool":
        hv = st.get("hv", {})
        if prose_bool:
            t, f = A.pr[0].format(**hv), A.pr[1].format(**hv)
        else:
            from cst_core import BOOL_DISP
            t, f = A.disp or BOOL_DISP[st["bool"]]
        need(s in (t, f), f"bool {s!r}")
        return s == t
    if k == "cat":
        need(s in A.cats, f"cat {s!r}")
        return s
    if k == "set":
        if prose_bool:  # empty-set prose phrase
            return frozenset()
        if s == "none":
            return frozenset()
        xs = s.split(", ")
        pool = A.items or ctx.get("people", [])
        need(all(x in pool for x in xs), f"set {s!r}")
        return frozenset(xs)
    raise VerifyError(k)


# ------------------------------------------------------------------------------------------------ own evaluator
def _val(e, o, ctx):
    kind = e[0]
    if kind == "a":
        v = o.get(e[1], UNKNOWN)
        return v
    if kind == "k":
        return e[1]
    if kind == "x":
        return ctx[e[1]]
    if kind in ("+", "-", "*"):
        a, b = _val(e[1], o, ctx), _val(e[2], o, ctx)
        if a in (UNKNOWN, NOTAPP) or b in (UNKNOWN, NOTAPP):
            return UNKNOWN
        return {"+": lambda: a + b, "-": lambda: a - b, "*": lambda: a * b}[kind]()
    if kind == "min":
        a, b = _val(e[1], o, ctx), _val(e[2], o, ctx)
        if a in (UNKNOWN, NOTAPP) or b in (UNKNOWN, NOTAPP):
            return UNKNOWN
        return a if a <= b else b
    if kind == "conv":
        a = _val(e[1], o, ctx)
        return UNKNOWN if a in (UNKNOWN, NOTAPP) else Fr(a) * e[2]
    if kind == "bizd":
        start, n = _val(e[1], o, ctx), _val(e[2], o, ctx)
        if start in (UNKNOWN, NOTAPP) or n in (UNKNOWN, NOTAPP):
            return UNKNOWN
        day, left = dt.date.fromordinal(start), n
        hol = {dt.date.fromordinal(h) for h in e[3]}
        while left:
            day += dt.timedelta(days=1)
            if day.isoweekday() <= 5 and day not in hol:
                left -= 1
        return day.toordinal()
    if kind == "ceil":
        a = _val(e[1], o, ctx)
        return UNKNOWN if a in (UNKNOWN, NOTAPP) else (a + e[2] - 1) // e[2]
    raise VerifyError(f"expr {e}")


T, F, U = "T", "F", "U"


def truth(p, o, ctx):
    kind = p[0]
    if kind == "cmp":
        a, b = _val(p[1], o, ctx), _val(p[3], o, ctx)
        if a in (UNKNOWN, NOTAPP) or b in (UNKNOWN, NOTAPP):
            return U
        r = {"<=": a <= b, "<": a < b, ">=": a >= b, ">": a > b}[p[2]]
        return T if r else F
    if kind in ("bool", "in", "has", "hasall", "hask", "disj"):
        v = _val(p[1], o, ctx)
        if v in (UNKNOWN, NOTAPP):
            return U
        if kind == "bool":
            r = v is p[2] or v == p[2]
        elif kind == "in":
            r = v in p[2]
        elif kind == "has":
            r = p[2] in v
        elif kind == "hasall":
            r = set(p[2]) <= set(v)
        elif kind == "hask":
            r = len(set(p[2]) & set(v)) >= p[3]
        else:
            r = len(set(v) & set(p[2])) == 0
        return T if r else F
    if kind == "not":
        x = truth(p[1], o, ctx)
        return {T: F, F: T, U: U}[x]
    if kind in ("and", "or"):
        xs = [truth(q, o, ctx) for q in p[1:]]
        if kind == "and":
            return F if F in xs else (U if U in xs else T)
        return T if T in xs else (U if U in xs else F)
    if kind == "imp":
        a = truth(p[1], o, ctx)
        b = truth(p[2], o, ctx)
        if a == F or b == T:
            return T
        if a == T and b == F:
            return F
        return U
    raise VerifyError(f"pred {p}")


# ------------------------------------------------------------------------------------------------ wording checks
def find_value(text, vstr):
    """Index of vstr in text as a whole token (not inside a longer number such as '3' in '13')."""
    for m in re.finditer(re.escape(vstr), text):
        a, b = m.start(), m.end()
        pre = text[a - 1] if a > 0 else " "
        post = text[b] if b < len(text) else " "
        if (pre.isalnum() or pre in ",.") and vstr[0].isalnum():
            continue
        if post.isdigit() or (post in ",." and b + 1 < len(text) and text[b + 1].isdigit()):
            continue
        return a
    return -1


FIELD_OP = {"max": "<=", "maximum": "<=", "latest": "<=", "min": ">=", "minimum": ">=", "earliest": ">="}


def op_before(text, vstr):
    k = find_value(text, vstr)
    need(k >= 0, f"threshold {vstr!r} not in {text!r}")
    before = text[:k].rstrip().lower()
    best = None
    for ph in V_LEX:
        if before.endswith(" " + ph) or before == ph:
            if best is None or len(ph) > len(best):
                best = ph
    if best is None and before.endswith(":"):
        w = before.split()[0] if before.split() else ""
        need(w in FIELD_OP, f"field label {text!r}")
        return FIELD_OP[w], before
    need(best is not None, f"no comparator before {vstr!r} in {text!r}")
    return V_LEX[best], before


def check_wording(c, text, st, ctx_sents, state, A_of, cons_modal):
    lower = text.lower()
    for chk in c.checks(st):
        kind = chk[0]
        if kind == "cmp":
            _, cls, op, pol, vstr = chk
            o, before = op_before(text, vstr)
            neg = bool(re.search(r"\b(must not|cannot|can't)\b", before))
            if neg:
                o = NEG_FLIP[o]
            need(o == op, f"wording op {o} != {op}: {text!r}")
            need(neg == (pol == "neg"), f"polarity {text!r}")
        elif kind == "bool":
            want, form = chk[1], chk[2]
            fm = re.fullmatch(r"(.+): (required|not acceptable)", text)
            if fm:
                need((fm.group(2) == "required") == want, f"bool field {text!r}")
                continue
            t = text[0].lower() + text[1:]
            t = t.rstrip(".")
            m = NEG_MODAL.match(t) or POS_MODAL.match(t)
            need(m, f"modal {text!r}")
            neg_modal = bool(NEG_MODAL.match(t))
            rest = t[m.end():].strip().lower()
            A = A_of(c)
            vps = [v.lower() for v in c.vps]
            if rest in vps:
                base = True
            elif any(rest == f"{w} {A.noun}".lower() for w in ("be without", "come without", "be one without")):
                base = False
            elif rest in [x.lower() for x in A.anti]:
                base = False
            else:
                raise VerifyError(f"bool wording {text!r}")
            need((base != neg_modal) == want, f"bool polarity {text!r}")
        elif kind == "cat":
            neg, vals = chk[1], chk[2]
            for v in vals:
                need(v in text, f"cat value {v} {text!r}")
            is_neg = bool(re.search(r"\b(must not|cannot|can't)\b", lower)) or re.search(r": not ", lower) is not None
            need(is_neg == neg, f"cat polarity {text!r}")
        elif kind == "set":
            mode, items, k = chk[1], chk[2], chk[3]
            for v in items:
                need(v in text, f"set item {v} {text!r}")
            words = {2: "two", 3: "three", 4: "four"}
            if mode == "all":
                need(("both " in lower and len(items) == 2) or ("all of " in lower), f"set all {text!r}")
            elif mode == "k":
                need(f"at least {words[k]} of" in lower, f"set k {text!r}")
            else:
                need("both " not in lower and "all of" not in lower and "at least" not in lower, f"set has {text!r}")
            need(bool(re.search(r"\b(must not|cannot|can't)\b", lower)) == (mode == "lacks"), f"set neg {text!r}")
        elif kind == "implicit":
            need(any(chk[1] in s for s in ctx_sents), f"implicit fact {chk[1]!r} missing")
        elif kind == "names":
            names, thr = chk[1], chk[2]
            hit = [s for s in ctx_sents if all(n in s for n in names)]
            need(hit and len(names) == thr, f"names {names} {thr}")
        elif kind == "tz":
            d = chk[1]
            ok = any((f"{abs(d)} hour" in s) and (("ahead of" in s) == (d > 0)) for s in ctx_sents + [state])
            need(ok, f"tz fact {d}")
        elif kind == "window":
            need(any(chk[1] in s and chk[2] in s for s in ctx_sents), f"window fact {chk}")
        elif kind == "xunit":
            need(chk[1] in text, f"unit note {chk[1]!r}")
        elif kind == "unless":
            need("unless" in lower, f"unless {text!r}")
        elif kind == "if":
            need(lower.startswith("if ") or lower.startswith("where "), f"if {text!r}")
        elif kind == "window_ctx":
            need(any(chk[1] in s and chk[2] in s for s in ctx_sents), f"commitment fact {chk}")
            need(bool(re.search(r"\b(must not|cannot|can't)\b", lower)), f"clash wording {text!r}")
        elif kind == "weekday":
            need(bool(re.search(r"\b(must not|cannot|can't)\b", lower)), f"weekday wording {text!r}")
            need(any(d in text for d in ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "weekend")), text)
        elif kind == "orlater":
            need(f"{chk[1]} or later" in text or text.endswith(f": {chk[1]}"), f"year wording {text!r}")
        elif kind == "implicit_ctx":
            need(len(ctx_sents) > 0, "context fact missing")
        else:
            raise VerifyError(f"check {kind}")


# ------------------------------------------------------------------------------------------------ main entry
def verify(inst, st, state, rec, row):
    D, ctx = inst["D"], inst["ctx"]
    st = dict(st)
    st["hv"] = D.hv(ctx) if D.hv else {}
    n = len(inst["labels"])
    cols = rec["cols"]
    fmt = st["fmt"]
    parsed = []
    for i in range(n):
        seg = rec["segs"][i]
        need(seg in state, f"segment of {inst['labels'][i]} missing")
        need(inst["labels"][i] in seg, "label not in its segment")
        o = {}
        for a in cols:
            A = D.A[a]
            s = rec["cells"][i][a]
            if fmt == "trans":
                row_line = rec["trans_rows"][a]
                need(row_line in state, "transposed row missing")
                parts = row_line.split(" | ")
                need(parts[i + 1] == s, f"transposed cell {a} {i}")
            else:
                need(s in seg, f"cell {s!r} not in segment {seg!r}")
            prose_b = fmt == "prose" and ((A.kind == "bool" and s not in (st["missing"],)) or
                                          (A.kind == "set" and isinstance(A.pr, tuple) and s == A.pr[1]))
            o[a] = parse_value(A, s, st, ctx, prose_bool=prose_b)
        parsed.append(o)
    for (i, a, text, disp) in rec["notes"]:
        need(text in state and inst["labels"][i] in text and disp in text, f"note {text!r}")
        A = D.A[a]
        pb = A.kind == "bool" or (A.kind == "set" and isinstance(A.pr, tuple) and disp == A.pr[1])
        parsed[i][a] = parse_value(A, disp, st, ctx, prose_bool=pb)
    # values read from the text must equal the generator's effective values
    for i in range(n):
        for a in cols:
            v = parsed[i][a]
            g = inst["opts"][i].get(a)
            gv = UNKNOWN if g == "<missing>" else NOTAPP if g == "<na>" else g
            need(v == gv, f"parsed {inst['labels'][i]}.{a}={v!r} but generator has {g!r}")
    # hidden derived attributes (weekday index, slot length ...) from the parsed values
    evald = []
    for i in range(n):
        o = {k: ("<missing>" if v == UNKNOWN else "<na>" if v == NOTAPP else v) for k, v in parsed[i].items()}
        D.derive(o, ctx)
        o = {k: (UNKNOWN if v == "<missing>" else NOTAPP if v == "<na>" else v) for k, v in o.items()}
        evald.append(o)
    # own evaluation of every requirement
    Q = [i for i in range(n) if all(truth(c.pred(), evald[i], ctx) == T for c in inst["cons"])]
    tie = inst["tie"]
    if not Q:
        need(inst["none_opt"], "no qualifier and no 'none' option")
        g = D.none_label
    elif tie is None:
        need(len(Q) == 1, f"{len(Q)} qualifiers without a tie-break")
        g = inst["labels"][Q[0]]
    else:
        keys = []
        for i in Q:
            k = []
            for e, d in tie.keys:
                v = _val(e, evald[i], ctx)
                need(v not in (UNKNOWN, NOTAPP), "tie key unknown")
                k.append(-Fr(v) if d == "max" else Fr(v))
            keys.append((tuple(k), i))
        keys.sort()
        need(len(keys) == 1 or keys[0][0] != keys[1][0], "exact tie")
        g = inst["labels"][keys[0][1]]
        need(rec["tie_text"] and rec["tie_text"] in state, "tie-break text missing")
    need(g == row["gold"], f"verifier gold {g!r} != row gold {row['gold']!r}")
    need(row["gold"] in row["options"], "gold not in options")
    need(len(row["options"]) == len(set(row["options"])), "duplicate options")
    # wording of every requirement
    csents = rec["ctx_sents"]
    for j, c in enumerate(inst["cons"]):
        text = rec["req_items"][j]
        need(text in state, f"requirement text missing: {text!r}")
        check_wording(c, text, st, csents, state, lambda cc: cc.attr, None)
        for s in csents:
            need(s in state, "context sentence missing")
    # unit conversions: same verdict under the exact factor
    for c in inst["cons"]:
        xu = getattr(c, "xunit", None)
        if not xu:
            continue
        key, op, fac, alt, dec = xu
        for i in range(n):
            v = evald[i].get(key)
            if v in (UNKNOWN, NOTAPP):
                continue
            t1 = Fr(c.params["d"]) / 10 ** dec * fac
            t2 = Fr(c.params["d"]) / 10 ** dec * alt
            r1 = {"<=": v <= t1, "<": v < t1, ">=": v >= t1, ">": v > t1}[op]
            r2 = {"<=": v <= t2, "<": v < t2, ">=": v >= t2, ">": v > t2}[op]
            need(r1 == r2, "conversion-sensitive verdict")
    if any(v == UNKNOWN for o in parsed for v in o.values()):
        need(any('"' + st["missing"] + '"' in r for r in rec["rules"]), "missing-value rule absent")
    return True

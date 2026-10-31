"""F2 independent solver B (G2), written from G0_SPEC.md v7 (3.2, 3.3) and C_DATA_SPEC 2.4 only.

Paradigm: table-driven re-derivation. The rendered row (card text, state, question, options) is parsed back into
facts (a fact table from the document) and a rule table (each card sentence matched against a lexicon of meaning
statements of G0 2.2 and formula phrases); a small rule interpreter then evaluates the asked node over exact integer
rationals. No `decimal`, `fractions`, `datetime`, `calendar`, `dateutil`, `numpy`, `pandas`, `holidays` (3.2).
Calendar by a from-scratch civil-to-days formula; business days in closed form; bands by cumulative closed form.
Open-world rows: exhaustive search over a finite breakpoint domain (z3 is not installed here; see notes).
Never reads solver A code (c_src/F2/gen/).
"""
import json, re, sys, math, os, collections

# ----------------------------------------------------------------------------------------------- exact rationals
class Q:
    __slots__ = ("n", "d")

    def __init__(self, n, d=1):
        if isinstance(n, Q):
            self.n, self.d = n.n, n.d
            return
        if d == 0:
            raise ZeroDivisionError("Q /0")
        if d < 0:
            n, d = -n, -d
        g = math.gcd(n, d)
        self.n, self.d = n // g, d // g

    @staticmethod
    def of(x):
        return x if isinstance(x, Q) else Q(x)

    def __add__(s, o): o = Q.of(o); return Q(s.n * o.d + o.n * s.d, s.d * o.d)
    __radd__ = __add__
    def __sub__(s, o): o = Q.of(o); return Q(s.n * o.d - o.n * s.d, s.d * o.d)
    def __rsub__(s, o): return Q.of(o) - s
    def __mul__(s, o): o = Q.of(o); return Q(s.n * o.n, s.d * o.d)
    __rmul__ = __mul__
    def __truediv__(s, o): o = Q.of(o); return Q(s.n * o.d, s.d * o.n)
    def __rtruediv__(s, o): return Q.of(o) / s
    def __neg__(s): return Q(-s.n, s.d)
    def _c(s, o): o = Q.of(o); return s.n * o.d - o.n * s.d
    def __eq__(s, o):
        if not isinstance(o, (Q, int)): return False
        return s._c(o) == 0
    def __hash__(s): return hash((s.n, s.d))
    def __lt__(s, o): return s._c(o) < 0
    def __le__(s, o): return s._c(o) <= 0
    def __gt__(s, o): return s._c(o) > 0
    def __ge__(s, o): return s._c(o) >= 0
    def __repr__(s): return "%d/%d" % (s.n, s.d) if s.d != 1 else "%d" % s.n

    def floor(s): return s.n // s.d
    def ceil(s): return -((-s.n) // s.d)


ZERO, ONE = Q(0), Q(1)


def qmax(a, b): return a if a >= b else b
def qmin(a, b): return a if a <= b else b


def parse_num(txt):
    """'1,234.50' -> Q exactly (integer parsing only)."""
    t = txt.replace(",", "").strip()
    neg = t.startswith("-")
    if neg: t = t[1:]
    if "." in t:
        a, b = t.split(".", 1)
        q = Q(int(a or "0") * 10 ** len(b) + int(b or "0"), 10 ** len(b))
    else:
        q = Q(int(t))
    return -q if neg else q


def round_unit(v, unit, mode):
    """Round rational v to a multiple of rational unit. mode: up (half up), even, floor, ceil."""
    v, unit = Q.of(v), Q.of(unit)
    x = v / unit                       # number of units, rational
    q, r = divmod(x.n, x.d)            # floor and remainder (r >= 0)
    if mode == "floor":
        k = q
    elif mode == "ceil":
        k = q + (1 if r else 0)
    else:
        twice = 2 * r
        if twice > x.d: k = q + 1
        elif twice < x.d: k = q
        else:
            k = q + 1 if mode == "up" else (q if q % 2 == 0 else q + 1)
    return unit * k

# ----------------------------------------------------------------------------------------------- calendar
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october",
          "november", "december"]
WDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


def days_from_civil(y, m, d):
    """Ordinal day number (days since 1970-01-01) of a proleptic Gregorian date; from-scratch era formula."""
    y -= m <= 2
    era = (y if y >= 0 else y - 399) // 400
    yoe = y - era * 400
    mp = (m + 9) % 12
    doy = (153 * mp + 2) // 5 + d - 1
    doe = yoe * 365 + yoe // 4 - yoe // 100 + doy
    return era * 146097 + doe - 719468


def civil_from_days(z):
    z += 719468
    era = (z if z >= 0 else z - 146096) // 146097
    doe = z - era * 146097
    yoe = (doe - doe // 1460 + doe // 36524 - doe // 146096) // 365
    y = yoe + era * 400
    doy = doe - (365 * yoe + yoe // 4 - yoe // 100)
    mp = (5 * doy + 2) // 153
    d = doy - (153 * mp + 2) // 5 + 1
    m = mp + 3 if mp < 10 else mp - 9
    return (y + (m <= 2), m, d)


def weekday(z):
    """0 = Monday ... 6 = Sunday. 1970-01-01 (ordinal 0) was a Thursday."""
    return (z + 3) % 7


def is_leap(y): return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)


def month_len(y, m):
    return [31, 29 if is_leap(y) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1]


def add_months(z, k, mode="clamp"):
    y, m, d = civil_from_days(z)
    t = (m - 1) + k
    y2, m2 = y + t // 12, t % 12 + 1
    L = month_len(y2, m2)
    if mode == "clamp":
        return days_from_civil(y2, m2, min(d, L))
    if mode == "overflow":
        return days_from_civil(y2, m2, 1) + d - 1
    if mode == "eomkeep":
        return days_from_civil(y2, m2, L if d == month_len(y, m) else min(d, L))
    raise ValueError(mode)


def fmt_date(z):
    y, m, d = civil_from_days(z)
    return "%04d-%02d-%02d" % (y, m, d)


class BizCal:
    """Business days: weekdays Mon-Fri (or as stated) minus the stated holiday set, in closed form."""

    def __init__(self, holidays=(), weekend=(5, 6)):
        self.weekend = set(weekend)
        self.work = [w for w in range(7) if w not in self.weekend]
        self.hol = sorted(set(holidays))
        for h in self.hol:
            if weekday(h) in self.weekend:
                raise SolverError("holiday on weekend (A12)")

    def _work_upto(self, z):
        """Number of non-weekend days with ordinal in [0, z) for z >= 0 relative to a Monday anchor (closed form)."""
        base = days_from_civil(1900, 1, 1)          # a Monday
        n = z - base
        full, rem = divmod(n, 7)
        cnt = full * len(self.work) + sum(1 for i in range(rem) if i in self.work)
        return cnt

    def count(self, a, b):
        """Business days in (a, b] (0 if b <= a)."""
        if b <= a: return 0
        c = self._work_upto(b + 1) - self._work_upto(a + 1)
        c -= sum(1 for h in self.hol if a < h <= b)
        return c

    def is_bd(self, z):
        return weekday(z) not in self.weekend and z not in self.hol

    def add(self, a, n):
        """The n-th business day after a (day 1 = first business day after a)."""
        if n <= 0: return a
        lo, hi = a + 1, a + 7 * (n // len(self.work) + 2) + 7 * (len(self.hol) + 1)
        while lo < hi:                       # smallest d with count(a, d) >= n
            mid = (lo + hi) // 2
            if self.count(a, mid) >= n: hi = mid
            else: lo = mid + 1
        return lo

    def roll(self, z, mode):
        if mode in (None, "none") or self.is_bd(z): return z
        step = 1 if mode == "next" else -1
        while not self.is_bd(z): z += step
        return z


class SolverError(Exception):
    pass

# ----------------------------------------------------------------------------------------------- document parser
import csv as _csv
import html as _html


def nkey(k):
    k = _html.unescape(k).strip().strip('*"\'`').strip()
    k = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", k)
    k = k.replace("_", " ").replace("**", "")
    return re.sub(r"\s+", " ", k).strip().lower()


class Doc:
    """Facts parsed from `state`: kv = list of (block_no, key, value); tables = list of (block_no, header, rows)."""

    def __init__(self):
        self.kv, self.tables, self.block = [], [], 0

    def add_kv(self, k, v):
        k = nkey(k)
        v = _html.unescape(str(v)).strip()
        v = re.sub(r"^:+\s*", "", v)
        if k: self.kv.append((self.block, k, v))

    def add_table(self, header, rows):
        hdr = [nkey(h) for h in header]
        self.tables.append((self.block, hdr, [[_html.unescape(str(c)).strip() for c in r] for r in rows]))


def _cells(line):
    s = line.strip()
    if s.startswith("|"): s = s[1:]
    if s.endswith("|"): s = s[:-1]
    return [c.strip() for c in s.split("|")]


def _flatten_json(doc, obj, prefix=""):
    if isinstance(obj, dict):
        scal = {k: v for k, v in obj.items() if not isinstance(v, (dict, list))}
        for k, v in scal.items():
            doc.add_kv(k, "" if v is None else ("yes" if v is True else "no" if v is False else v))
        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                doc.block += 1
                _flatten_json(doc, v, k)
    elif isinstance(obj, list):
        if obj and all(isinstance(x, dict) for x in obj):
            hdr = []
            for x in obj:
                for k in x:
                    if k not in hdr: hdr.append(k)
            rows = [["" if x.get(k) is None else ("yes" if x.get(k) is True else "no" if x.get(k) is False else
                     (json.dumps(x.get(k)) if isinstance(x.get(k), (dict, list)) else x.get(k))) for k in hdr]
                    for x in obj]
            doc.add_table(hdr, rows)
            if prefix: doc.tables[-1] = doc.tables[-1] + (prefix,)
        else:
            doc.add_kv(prefix, "; ".join(str(x) for x in obj))


def _try_json(doc, txt):
    t = txt.strip()
    if not t or t[0] not in "{[": return False
    try:
        obj = json.loads(t)
    except Exception:
        return False
    _flatten_json(doc, obj)
    return True


def _strip_tags(s):
    return re.sub(r"<[^>]+>", "", s).strip()


def _parse_html(doc, s):
    """dl lists, tables (header row or th-scope-row kv rows), li items; the rest is handed back as plain lines."""
    for m in re.finditer(r"<dt[^>]*>(.*?)</dt>\s*<dd[^>]*>(.*?)</dd>", s, re.S):
        doc.add_kv(_strip_tags(m.group(1)), _strip_tags(m.group(2)))
    for tm in re.finditer(r"<table[^>]*>(.*?)</table>", s, re.S):
        doc.block += 1
        trs = re.findall(r"<tr[^>]*>(.*?)</tr>", tm.group(1), re.S)
        hdr, body = None, []
        for tr in trs:
            cells = re.findall(r"<(th|td)([^>]*)>(.*?)</\1>", tr, re.S)
            kinds = [c[0] for c in cells]
            vals = [_strip_tags(c[2]) for c in cells]
            if len(cells) == 2 and kinds[0] == "th" and "row" in cells[0][1]:
                doc.add_kv(vals[0], vals[1])
            elif hdr is None and all(k == "th" for k in kinds):
                hdr = vals
            else:
                body.append(vals)
        if hdr is not None:
            if [h.lower() for h in hdr] in (["field", "value"], ["item", "value"], ["key", "value"]):
                for b in body:
                    if len(b) >= 2: doc.add_kv(b[0], b[1])
            else:
                doc.add_table(hdr, body)
        elif body and all(len(b) == 2 for b in body):
            for b in body: doc.add_kv(b[0], b[1])
    rest = re.sub(r"<table[^>]*>.*?</table>", "\n", s, flags=re.S)
    rest = re.sub(r"<dl[^>]*>.*?</dl>", "\n", rest, flags=re.S)
    rest = re.sub(r"<li[^>]*>(.*?)</li>", lambda m: "\n- " + _strip_tags(m.group(1)) + "\n", rest, flags=re.S)
    rest = re.sub(r"<(p|div|h\d|header|article|section|span|pre|code|caption)[^>]*>", "\n", rest)
    rest = re.sub(r"<[^>]+>", "\n", rest)
    return _html.unescape(rest)


KV_RE = re.compile(r"^\s*(?:[-*+>\u2022]\s*|\(?\d+[.)]\s+)*(?:\*\*)?([A-Za-z][\w \-/()'.]*?)(?:\*\*)?\s*(?::|=| — | -- |\s\.{2,}|\s->|\s=>)\s*(.*?)\s*$")
PROSE_RE = re.compile(r"(?:^|(?<=[.!]\s))The ([a-z][\w \-/()']*?) (?:is|was|are|were) (.+?)\.(?=\s|$)")


HDR2 = {"field", "value", "item", "key", "attribute", "setting", "name", "detail", "entry", "parameter", "fact"}


def _emit(doc, hdr, body):
    if len(hdr) == 2 and all(len(b) == 2 for b in body):
        if not ({h.strip().lower() for h in hdr} & HDR2):
            doc.add_kv(hdr[0], hdr[1])
        for b in body: doc.add_kv(b[0], b[1])
    else:
        doc.block += 1
        doc.add_table(hdr, body)


def _parse_lines(doc, text):
    lines = text.split("\n")
    i, n = 0, len(lines)
    SEP = re.compile(r"^\s*[=\-]{3,}(\s+[=\-]{3,})+\s*$")
    while i < n:
        ln = lines[i].rstrip()
        st = ln.strip()
        if not st or st.startswith("```"):
            i += 1
            continue
        if "\t" in st:                                   # tab-separated block
            blk = []
            while i < n and "\t" in lines[i]:
                blk.append([c.strip() for c in lines[i].strip().split("\t")]); i += 1
            _emit(doc, blk[0], blk[1:])
            continue
        if st.startswith("|") or re.match(r"^\+[-=+]+\+$", st):   # markdown or ascii table
            blk = []
            while i < n and (lines[i].strip().startswith("|") or re.match(r"^\+[-=+]+\+$", lines[i].strip())):
                if lines[i].strip().startswith("|"): blk.append(_cells(lines[i]))
                i += 1
            blk = [b for b in blk if not all(re.match(r"^:?-{2,}:?$", c) or c == "" for c in b)]
            if blk: _emit(doc, blk[0], blk[1:])
            continue
        if i + 1 < n and SEP.match(lines[i + 1]):        # fixed-width table
            spans = [(m.start(), m.end()) for m in re.finditer(r"[=\-]+", lines[i + 1])]
            def cut(l):
                out = []
                for j, (a, b) in enumerate(spans):
                    e = spans[j + 1][0] if j + 1 < len(spans) else len(l)
                    out.append(l[a:e].strip() if a < len(l) else "")
                return out
            hdr = cut(ln); i += 2; body = []
            while i < n and lines[i].strip() and not SEP.match(lines[i]) and not lines[i].strip().startswith("```"):
                body.append(cut(lines[i])); i += 1
            _emit(doc, hdr, body)
            continue
        dm = re.match(r"^\"?[A-Za-z][\w \-/()%']*?\"?\s*([,|;])\s*\"?[A-Za-z]", st)
        if dm and ": " not in st.split(dm.group(1))[0]:  # delimiter-separated block (csv, pipe, semicolon)
            dl = dm.group(1)
            blk = []
            while i < n and lines[i].strip() and not lines[i].strip().startswith("```"):
                blk.append(lines[i].strip()); i += 1
            recs = list(_csv.reader(blk, delimiter=dl)) if dl != "|" else [[c.strip() for c in b.split("|")] for b in blk]
            recs = [[c.strip() for c in r] for r in recs]
            _emit(doc, recs[0], recs[1:])
            continue
        SP = re.compile(r"\S\s{2,}\S")
        if SP.search(st) and i + 1 < n and SP.search(lines[i + 1].strip()) and ": " not in st:   # space-aligned
            blk = []
            while i < n and lines[i].strip() and SP.search(lines[i].strip()) and not lines[i].strip().startswith("```"):
                blk.append(re.split(r"\s{2,}", lines[i].strip())); i += 1
            _emit(doc, blk[0], blk[1:])
            continue
        segs = re.split(r"(?<=\S)\.\s+(?=[A-Za-z][\w \-/()']{0,40}:\s)", st)
        if len(segs) > 1:
            for sg in segs:
                mm = KV_RE.match(sg.strip())
                if mm and mm.group(2):
                    v = mm.group(2)
                    doc.add_kv(mm.group(1), v[:-1] if v.endswith(".") else v)
            i += 1
            continue
        m = KV_RE.match(ln)
        if m and m.group(2):
            v = m.group(2)
            doc.add_kv(m.group(1), v[:-1] if v.endswith(".") else v)
        else:
            for pm in PROSE_RE.finditer(st):
                doc.add_kv(pm.group(1), pm.group(2))
            if re.match(r"^[A-Z][\w ]*:?$", st) or st.startswith("#"): doc.block += 1
        i += 1


def parse_doc(state):
    doc = Doc()
    s = state or ""
    if "<" in s and re.search(r"</\w+>", s):
        s = _parse_html(doc, s)
    # json fences / bare json
    def jrep(m):
        return "\n" if _try_json(doc, m.group(1)) else m.group(0)
    s = re.sub(r"```(?:json)?\s*\n(\s*[\{\[].*?)\n```", jrep, s, flags=re.S)
    if s.strip()[:1] in "{[" and _try_json(doc, s.strip()):
        return doc
    m = re.search(r"^(\{.*\}|\[.*\])\s*$", s, re.S | re.M)
    if m and _try_json(doc, m.group(1)):
        s = s.replace(m.group(1), "\n")
    _parse_lines(doc, s)
    return doc

# ----------------------------------------------------------------------------------------------- card text and question
ANS_MARK = re.compile(r"^\s*(?:>\s*)*(?:\*\*)?(Outcome|Its answer|Answer key|Correct choice|Answer|Result|Solution)"
                      r"(?:\*\*)?\s*[:=\-]", re.I)
PFX = re.compile(r"^\s*(?:>\s*)*(?:[-*+•·]\s+|\(?\d+[.)]\s+|Rule \d+[:.]\s*|Step \d+[:.]\s*)?(?:\[|\*\*)?"
                 r"(?:[A-Z][A-Za-z0-9 \-/']{0,34}?(?:\]|\*\*)?\s*(?:::|:|=|\||—|->|→)\s+(?=[A-Z\"(]))?")


def card_source(row):
    if row["qtype"] == "noul":
        return row.get("card") or ""
    return row.get("instructions") or ""


def split_sentences(text):
    """Card text -> list of (line_no, sentence). Heading prefixes are stripped; examples are dropped."""
    out = []
    for li, raw in enumerate(text.split("\n")):
        l = re.sub(r"</?[a-z_]+>", "", raw)
        l = l.replace("**", "")
        l = PFX.sub("", l).strip()
        if not l: continue
        l = re.sub(r"\s*\((?:e\.g\.|for example|example)[^)]*\)", "", l)
        for s in re.split(r"(?<=[.])\s+(?=[A-Z\"\d])", l):
            s = s.strip()
            if s: out.append((li, s))
    return out


def find_question(row):
    """The row's question: the last '?' sentence in instructions not followed by a few-shot answer marker."""
    ins = row["instructions"] or ""
    lines = ins.split("\n")
    cands = []
    for i, l in enumerate(lines):
        for m in re.finditer(r"[^?\n]*\?", l):
            q = m.group(0)
            nxt = l[m.end():]
            follow = nxt if nxt.strip() else next((x for x in lines[i + 1:] if x.strip()), "")
            if ANS_MARK.match(follow.strip()): continue
            cands.append(q.strip())
    if not cands: raise SolverError("no question")
    strong = [c for c in cands if re.search(r"\b[A-Z]{1,5}-\d+\b|\bcases?\b|\bitems?\b|\bentr(?:y|ies)\b", c)]
    q = (strong or cands)[-1]
    q = re.sub(r"^(?:>\s*)*(?:\*\*)?(?:Q|Question|Query|Task|Your question|Now)(?:\*\*)?\s*[:.\-]\s*", "", q)
    q = re.split(r"(?<=[.!])\s+(?=[A-Z\"])", q)[-1]
    m = re.match(r"^(.*?):\s+((?:Is|Was|Were|Did|Does|Do|Which|What|How|For|In|Are|Has|Had)\b.*)$", q)
    if m and not re.match(r"^(?:is the following true|is this true|is this the case|true or false)$", m.group(1), re.I):
        q = m.group(2)
    return q.strip()

# ----------------------------------------------------------------------------------------------- rule table (card parse)
def nm(x):
    x = x.strip().strip(".").strip()
    x = re.sub(r"^(?:the|a|an|its|each)\s+", "", x, flags=re.I)
    return re.sub(r"\s+", " ", x).lower()


class Card:
    def __init__(self):
        self.defs = {}            # name -> node tuple
        self.exc = {}             # num -> dict(cond=..., effects=[...], form=...)
        self.x3 = None            # ('alone', 'lower'|'higher', final_name) | ('fold',)
        self.rounds = []          # dict(q=name|None, unit=Q, mode=...)
        self.stage = None         # ('final',) | ('each', [names])
        self.r3 = "rounded"
        self.r4 = False
        self.floor0 = None
        self.caps = {}            # cap value name -> scope
        self.mins = {}
        self.band = {}            # form, mode, kind, charge, amount, x10
        self.outcomes = None      # dict(var=name, outcome=name, rows=[(label, spec)])
        self.window_form = None
        self.partial = None       # (mode, unit)
        self.perk = None          # mode
        self.b4 = None
        self.discount_combo = None  # 'successive' | 'added'
        self.steps = []           # ordered step names for 'after these steps'
        self.step_kinds = {}      # step name -> ('disc'|'add'|'sub'|'cap'|'min')
        self.money_pred = {}      # predicate word -> item
        self.cats = {}            # category -> list of values
        self.world = "closed"
        self.nei_option = None
        self.date = {}            # deadline machinery
        self.unmatched = []
        self.blank_amount = False
        self.computed_marker = None
        self.count_rule = None
        self.statement = {}


def parse_cond(txt):
    """Condition text -> ('and'|'or'|'xor', [atoms]) ; atom = (field, op, value_text)."""
    t = txt.strip().rstrip(".").strip()
    t = re.sub(r"\s*\(either or both\)\s*$", "", t)
    m = re.match(r"^either (.+), but not both$", t)
    if m:
        parts = re.split(r" or (?=the )", m.group(1))
        if len(parts) != 2: raise SolverError("xor parts")
        return ("xor", [parse_atom(p) for p in parts])
    parts = re.split(r" and (?=the )", t)
    if len(parts) > 1:
        return ("and", [parse_atom(p) for p in parts])
    parts = re.split(r" or (?=the )", t)
    if len(parts) > 1:
        return ("or", [parse_atom(p) for p in parts])
    return ("and", [parse_atom(t)])


CMP_WORDS = [
    (r"is at least", ">="), (r"is no less than", ">="), (r"is no fewer than", ">="), (r"reaches", ">="),
    (r"is a minimum of", ">="), (r"is more than", ">"), (r"is over", ">"), (r"is above", ">"), (r"exceeds", ">"),
    (r"is less than", "<"), (r"is under", "<"), (r"is below", "<"), (r"is fewer than", "<"),
    (r"falls short of", "<"), (r"fails to reach", "<"), (r"is at most", "<="), (r"is no more than", "<="),
    (r"does not exceed", "<="), (r"is up to", "<="), (r"is a maximum of", "<="),
]


def parse_atom(a):
    a = a.strip()
    a = re.sub(r"^(?:if|when|unless)\s+", "", a, flags=re.I)
    for w, op in CMP_WORDS:
        m = re.match(r"^(?:the )?(.+?) " + w + r" (.+)$", a)
        if m: return (nm(m.group(1)), op, m.group(2).strip())
    m = re.match(r"^(?:the )?(.+?) is (.+?) or (more|less)$", a)
    if m: return (nm(m.group(1)), ">=" if m.group(3) == "more" else "<=", m.group(2).strip())
    m = re.match(r"^(?:the )?(.+?) is between (.+?) and (.+?), both included$", a)
    if m: return (nm(m.group(1)), "between", (m.group(2), m.group(3)))
    m = re.match(r"^(?:the )?(.+?) is from (.+?) up to but not including (.+)$", a)
    if m: return (nm(m.group(1)), "fromto", (m.group(2), m.group(3)))
    m = re.match(r"^(?:the )?(.+?) is (.+)$", a)
    if m: return (nm(m.group(1)), "==", m.group(2).strip())
    raise SolverError("atom? " + a[:60])


N_ = r"(?:the |a |an )?(.+?)"
RULES = []      # (compiled regex, handler name)


def rule(pat):
    def deco(f):
        RULES.append((re.compile("^" + pat + "$", re.I), f))
        return f
    return deco


@rule(r"The (.+?) is the (.+?) times the (.+?)\.")
def _r_mul(c, m): c.defs[nm(m[1])] = ("mul", nm(m[2]), nm(m[3]))


@rule(r"The (.+?) is the (.+?) plus the (.+?)\.")
def _r_plus(c, m): c.defs[nm(m[1])] = ("add", [nm(m[2]), nm(m[3])])


@rule(r"The (.+?) adds the (.+?) to the (.+?)\.")
def _r_adds(c, m): c.defs[nm(m[1])] = ("add", [nm(m[3]), nm(m[2])])


@rule(r"The (.+?) is the sum of the amounts of the (.+?) lines\.")
def _r_sumlines(c, m):
    kinds = [nm(x) for x in re.split(r",\s*(?:and\s+)?|\s+and\s+(?:the\s+)?", m[2]) if x.strip()]
    c.defs[nm(m[1])] = ("sumlines", kinds)


@rule(r"The (.+?) is the sum of the (.+?) and the (.+?)\.")
def _r_sum(c, m): c.defs[nm(m[1])] = ("add", [nm(m[2]), nm(m[3])])


@rule(r"The (.+?) is the (.+?) minus the (.+?)\.")
def _r_minus(c, m):
    parts = re.split(r",? and minus the |, minus the |,? and the |, the ", m[3])
    subs = []
    for p in parts:
        mm = re.match(r"amounts of the (.+?) lines$", p.strip())
        subs.append(("lines", [nm(x) for x in re.split(r",\s*(?:and\s+)?|\s+and\s+(?:the\s+)?", mm.group(1))]) if mm
                    else nm(p))
    c.defs[nm(m[1])] = ("sub", nm(m[2]), subs)


@rule(r"The (.+?) is the (.+?), capped at the (.+?)\.")
def _r_cap(c, m): c.defs[nm(m[1])] = ("cap", nm(m[2]), nm(m[3]))


@rule(r"The (.+?) is the (.+?), with a minimum of the (.+?)\.")
def _r_minof(c, m): c.defs[nm(m[1])] = ("min", nm(m[2]), nm(m[3]))


@rule(r"The (.+?) is the (.+?) of the (.+?), capped at the (.+?)\.")
def _r_pctcap(c, m):
    c.defs[nm(m[1]) + " #raw"] = ("pct", nm(m[2]), nm(m[3]))
    c.defs[nm(m[1])] = ("cap", nm(m[1]) + " #raw", nm(m[4]))


@rule(r"The (.+?) is the (.+?) of the (.+?), with a minimum of the (.+?)\.")
def _r_pctmin(c, m):
    c.defs[nm(m[1]) + " #raw"] = ("pct", nm(m[2]), nm(m[3]))
    c.defs[nm(m[1])] = ("min", nm(m[1]) + " #raw", nm(m[4]))


@rule(r"The (.+?) is the number of (calendar|business) days from the (.+?) to the (.+?)\.")
def _r_count(c, m): c.defs[nm(m[1])] = ("daycount", m[2].lower(), nm(m[3]), nm(m[4]))


@rule(r"The (.+?) is the (.+?) after these steps\.")
def _r_steps(c, m): c.defs[nm(m[1])] = ("steps", nm(m[2]))


@rule(r"The (.+?) is the (.+?) after the (.+?)\.")
def _r_after(c, m):
    ds = [nm(x) for x in re.split(r",? and the |, the ", m[3])]
    c.defs[nm(m[1])] = ("disc", nm(m[2]), ds)


@rule(r"The (.+?) is the price per (\d+) (.+?) for each \2 \3 of (.+?)\.")
def _r_perk(c, m): c.defs[nm(m[1])] = ("perk", nm("price per %s %s" % (m[2], m[3])), int(m[2]), nm(m[4]))


@rule(r"The (.+?) is worked out from the band table for the (.+?)\.")
def _r_band(c, m):
    c.defs[nm(m[1])] = ("band", nm(m[2]))
    c.band["charge"], c.band["amount"] = nm(m[1]), nm(m[2])


@rule(r"The (.+?) is the (.+?) of the (.+?)\.")
def _r_pct(c, m): c.defs[nm(m[1])] = ("pct", nm(m[2]), nm(m[3]))


@rule(r"The (.+?) is the (.+?)\.")
def _r_alias(c, m):
    if re.search(r"\d", m[2]) or len(m[2].split()) > 6:
        c.unmatched.append(m[0]); return
    c.defs[nm(m[1])] = ("ref", nm(m[2]))


# --- exceptions (UN1, O1, O2, O3), X2, X3
@rule(r"Exception (\d+) applies only if (.+?)\. When (?:all|at least one) of these (?:conditions )?holds?, exception \1 applies\.")
def _r_exc_only(c, m): c.exc.setdefault(int(m[1]), {"effects": []}).update(cond=parse_cond(m[2]), form="only")


@rule(r"Exception (\d+) applies only if (.+?)\.")
def _r_exc_only1(c, m): c.exc.setdefault(int(m[1]), {"effects": []}).update(cond=parse_cond(m[2]), form="only")


@rule(r"When (?:all|at least one) of these (?:conditions )?holds?, exception (\d+) applies\.")
def _r_exc_when(c, m): pass


@rule(r"Exception (\d+) applies if (.+?)\.")
def _r_exc_if(c, m): c.exc.setdefault(int(m[1]), {"effects": []}).update(cond=parse_cond(m[2]), form="if")


@rule(r"Exception (\d+) applies unless (.+?)\.")
def _r_exc_unless(c, m): c.exc.setdefault(int(m[1]), {"effects": []}).update(cond=parse_cond(m[2]), form="unless")


@rule(r"If (.+?),? exception (\d+) does not apply and nothing applies instead\.")
def _r_exc_unless2(c, m): pass


@rule(r"When exception (\d+) applies, the (.+?) replaces the (.+?)\.")
def _r_exc_repl(c, m): c.exc.setdefault(int(m[1]), {"effects": []})["effects"].append(("replace", nm(m[2]), nm(m[3])))


@rule(r"When exception (\d+) applies, the (.+?) is added to the (.+?)\.")
def _r_exc_add(c, m): c.exc.setdefault(int(m[1]), {"effects": []})["effects"].append(("add", nm(m[2]), nm(m[3])))


@rule(r"If more than one exception applies, compute the final (.+?) with each one alone and use the one that gives "
      r"the (lower|higher) final \1; if two give the same final \1, use the one with the lower (?:rule|exception) number\.")
def _r_x3a(c, m): c.x3 = ("alone", m[2].lower(), nm(m[1]))


@rule(r"If more than one exception applies, apply all of them in (?:rule|exception)-number order; each one acts on the "
      r"(rate|charge) left by the ones before it(?:, so a later replacing rule replaces the rate an earlier one set)?\.")
def _r_x3b(c, m): c.x3 = ("fold", m[1].lower())


# --- rounding R1-R4
UNIT = r"(\d[\d,]*(?:\.\d+)?)"


@rule(r"Round (?:the )?(.+?) to the nearest multiple of " + UNIT + r"(?: [^;]*)?; an exact half rounds (up|to the even multiple)(?: of .+?)?\.")
def _r_round_near(c, m):
    c.rounds.append(dict(q=nm(m[1]), unit=parse_num(m[2]), mode="up" if m[3].lower() == "up" else "even"))


@rule(r"Always round (?:the )?(.+?) (down|up) to a (?:whole )?multiple of " + UNIT + r"(?: [^;]*)?; a value that is already a (?:whole )?multiple of .+? does not change\.")
def _r_round_dir(c, m):
    c.rounds.append(dict(q=nm(m[1]), unit=parse_num(m[3]), mode="floor" if m[2].lower() == "down" else "ceil"))


@rule(r"Round only the final (.+?)\.")
def _r_stage_final(c, m): c.stage = ("final", nm(m[1]))


@rule(r"Round each (.+?) as the rounding rule says, then (?:add the lines|combine them)\.")
def _r_stage_each(c, m):
    c.stage = ("each", [nm(x) for x in re.split(r",? and (?:the )?|, (?:the )?", m[1])])


@rule(r"Every comparison made after (?:the )?(.+?) (?:is|are) rounded(?: \(.*?\))? uses the rounded (.+?)\.")
def _r_r3(c, m): c.r3 = "rounded"


@rule(r"Every comparison uses the (.+?) computed with no rounding step at all; rounding changes only the reported (.+?)\.")
def _r_r3t(c, m): c.r3 = "unrounded"


@rule(r"Do not round any step except where a rule says so\.")
def _r_r4(c, m): c.r4 = True


# --- floor, caps scope, discounts, steps
@rule(r"The final (.+?) cannot go below 0\.")
def _r_floor(c, m): c.floor0 = nm(m[1])


@rule(r"The cap of the (.+?) is per (.+?)\.")
def _r_capscope(c, m): c.caps[nm(m[1])] = m[2].lower()


@rule(r"The minimum of the (.+?) is per (.+?)\.")
def _r_minscope(c, m): c.mins[nm(m[1])] = m[2].lower()


@rule(r"The minimum is applied after the cap\.")
def _r_minafter(c, m): c.min_after_cap = True


@rule(r"Discounts are applied one after the other, each to the amount left after the previous one\.")
def _r_x5a(c, m): c.discount_combo = "successive"


@rule(r"Discount percentages are added together and applied once\.")
def _r_x5b(c, m): c.discount_combo = "added"


@rule(r"A discount of p% on an amount means paying \(100 - p\)% of that amount\.")
def _r_r8(c, m): pass


@rule(r"The (.+?) is a discount on the running amount\.")
def _r_stepdisc(c, m): c.step_kinds[nm(m[1])] = "disc"


@rule(r"The (.+?) is added to the running amount\.")
def _r_stepadd(c, m): c.step_kinds[nm(m[1])] = "add"


@rule(r"The (.+?) is subtracted from the running amount\.")
def _r_stepsub(c, m): c.step_kinds[nm(m[1])] = "sub"


@rule(r"Apply the steps in this order: (.+?)\.")
def _r_order(c, m):
    c.steps = [nm(x) for x in re.split(r",? then (?:the )?|, (?:the )?", m[1])]


@rule(r"Deduction lines are listed as positive amounts and are subtracted\.")
def _r_u5(c, m): pass


# --- bands B1, B2, X10, rate kinds
@rule(r"Each band covers the amounts over its lower edge up to and including its upper edge;.*")
def _r_b1u(c, m): c.band["form"] = "upper"


@rule(r"Each band covers the amounts from its lower edge up to but not including its upper edge;.*")
def _r_b1l(c, m): c.band["form"] = "lower"


@rule(r"A blank edge cell means the band has no edge on that side\.")
def _r_b1blank(c, m): pass


@rule(r"The band table in the (?:record|text|document|statement) gives each band's name, lower edge, upper edge and rate\.")
def _r_btab(c, m): pass


@rule(r"Each rate applies only to the part of the (.+?) inside its band:.*")
def _r_b2m(c, m): c.band["mode"] = "marginal"


@rule(r"The rate of the band that the whole (.+?) falls in applies to the whole \1\.")
def _r_b2f(c, m): c.band["mode"] = "flat"


@rule(r"Each band's rate is a percentage of the (.+?) it applies to\.")
def _r_bkp(c, m): c.band["kind"] = "pct"


@rule(r"Each band's rate is an amount per (.+?) of the (.+?) it applies to\.")
def _r_bku(c, m): c.band["kind"] = "unit"


@rule(r"Each band's rate is a flat fee, and that fee is the (.+?)\.")
def _r_bkf(c, m): c.band["kind"] = "fee"


@rule(r"When the (.+?) is (.+?), the (.+?) pays the rate of the band with the next lower edges than the band its (.+?) falls in; in the lowest band nothing changes\.")
def _r_x10(c, m): c.band["x10"] = (nm(m[1]), m[2].strip())


@rule(r"Band edges do not change\.")
def _r_x10b(c, m): pass


@rule(r"Bands are set by the (.+?) (before|after) (?:the )?(.+?)\.")
def _r_b3(c, m): c.band["b3"] = (nm(m[1]), m[2].lower(), nm(m[3]))


# --- named outcomes (CH-O tables in the card) and S4 windows
@rule(r"The (.+?) sets the (.+?) as follows\.")
def _r_outc(c, m): c.outcomes = dict(var=nm(m[1]), outcome=nm(m[2]), rows=[])


@rule(r"Each window covers the dates after its earlier edge up to and including its later edge;.*")
def _r_w_u(c, m): c.window_form = "upper"


@rule(r"Each window covers the dates from its earlier edge up to but not including its later edge;.*")
def _r_w_l(c, m): c.window_form = "lower"


@rule(r"\"(.+?)\" means the date (\S+) calendar days later; the last allowed day itself is not counted\.")
def _r_d16(c, m): pass


@rule(r"<?k>? calendar days after the last allowed day is the date .*")
def _r_d16b(c, m): pass


# --- world, categories, predicates
@rule(r"These are all the rules\.")
def _r_w0a(c, m): pass


@rule(r"No other fee, discount, cap or exception applies, and an? (.+?) is due only when a listed rule makes it due\.")
def _r_w0b(c, m): pass


@rule(r"The record lists every charge, payment and event that happened:.*")
def _r_w1(c, m): c.world = "closed"


@rule(r"Every charge, payment and event that happened is listed, and every other fact the rules use is given or shown as \"not recorded\"\.")
def _r_w2(c, m): c.world = "open"


@rule(r"A field shown as \"not recorded\" is unknown:.*")
def _r_w2b(c, m): c.world = "open"


@rule(r"If the answer depends on an unknown field, choose \"(.+?)\"\.")
def _r_w2c(c, m): c.nei_option = m[1]


@rule(r"The (.+?) is one of: (.+?)\.")
def _r_cat(c, m): c.cats[nm(m[1])] = [x.strip() for x in re.split(r",\s*(?:and\s+|or\s+)?|\s+(?:and|or)\s+", m[2]) if x.strip()]


@rule(r"An? (.+?) is (owed|charged) when its amount worked out under these rules, after every rounding, cap, minimum, discount and waiver, is more than 0\.")
def _r_op(c, m): c.money_pred[m[2].lower()] = nm(m[1])


@rule(r"An? (.+?) is due when a listed rule makes it due\.")
def _r_opdue(c, m): c.money_pred["due"] = nm(m[1])


@rule(r"If (?:the )?(.+?) is not given, use (.+?)\.")
def _r_w3(c, m): c.defaults = getattr(c, "defaults", {}); c.defaults[nm(m[1])] = m[2].strip()


# --- dates D1, D4, D5, D6, D7, D8, D12, D14, D15, D17
@rule(r"All dates are calendar dates in one time zone; the time of day does not matter\.")
def _r_d1(c, m): pass


@rule(r"The (.+?) must happen no later than (\d+) calendar days after the (.+?)\.")
def _r_d4a(c, m): c.date.update(act=nm(m[1]), kind="cal", n=int(m[2]), event=nm(m[3]), d4="a")


@rule(r"The day of the (.+?) is not counted, so the last allowed day is (\d+) calendar days after it\.")
def _r_d4a2(c, m): c.date.setdefault("d4", "a")


@rule(r"The (.+?) must happen on or before the (\d+)(?:st|nd|rd|th) calendar day, counting the day of the (.+?) as day 1\.")
def _r_d4b(c, m): c.date.update(act=nm(m[1]), kind="cal", n=int(m[2]), event=nm(m[3]), d4="b")


@rule(r"The (.+?) must happen no later than (\d+) business days after the (.+?)\.")
def _r_d6b(c, m): c.date.update(act=nm(m[1]), kind="bus", n=int(m[2]), event=nm(m[3]))


@rule(r"Counting starts on the day after the (.+?); the (\d+)(?:st|nd|rd|th) business day is the last allowed day\.")
def _r_d6b2(c, m): pass


@rule(r"The (.+?) must happen no later than (\d+) months? after the (.+?); that date is the last allowed day\.")
def _r_d8(c, m): c.date.update(act=nm(m[1]), kind="month", n=int(m[2]), event=nm(m[3]))


@rule(r"(\d+|<M>) months? after a date is the same day number .*")
def _r_d8b(c, m): c.date["eom"] = "clamp"


@rule(r"Then apply the roll rule, if there is one\.")
def _r_d8c(c, m): pass


@rule(r"A business day is an? (?:day )?(?:from )?Monday to Friday(?: day)? that is not a holiday\.")
def _r_d6a(c, m): c.date["bdays"] = True


@rule(r"A business day is a day from Monday to Friday that is not a holiday\.")
def _r_d6a2(c, m): c.date["bdays"] = True


@rule(r"The holidays are exactly the dates on the (?:record|text|document|statement)'s holiday line; when that line says \"none\", there are no holidays\.")
def _r_hol(c, m): c.date["bdays"] = True


@rule(r"If the (last allowed day|settlement date) falls on a day that is not a business day, it moves to the (next|previous) business day\.")
def _r_roll(c, m): c.date["roll"] = m[2].lower()


@rule(r"If the (last allowed day|settlement date) falls on a day that is not a business day, it does not move\.")
def _r_roll0(c, m): c.date["roll"] = "none"


@rule(r"If the settlement date falls on a day that is not a business day, the roll rule applies to it\.")
def _r_d17b(c, m): pass


@rule(r"The settlement date is (\d+) calendar days after the (.+?); the day of the \2 is not counted\.")
def _r_d17(c, m): c.date.update(settle_n=int(m[1]), settle_from=nm(m[2]))


@rule(r"(If|Unless) (.+?), the last allowed day moves (\d+) (calendar|business) days later\.")
def _r_d12(c, m):
    c.date["ext"] = dict(neg=m[1].lower() == "unless", cond=parse_cond(m[2]), k=int(m[3]), unit=m[4].lower())


@rule(r"Count the (\d+) (calendar|business) days from the last allowed day found before any roll; then apply the roll rule once\.")
def _r_d12a(c, m): c.date["ext_from"] = "preroll"


@rule(r"Count the (\d+) (calendar|business) days from the last allowed day after the roll; then apply the roll rule again\.")
def _r_d12b(c, m): c.date["ext_from"] = "postroll"


@rule(r"An? (.+?) on or before the last allowed day is on time, also when it is on or before the day of the (.+?); an? .+? after the last allowed day is late\.")
def _r_d15(c, m): c.date["d15"] = True


@rule(r"Count (?:the )?(.+?) but not (?:the )?(.+?)\.")
def _r_d5a(c, m): c.count_rule = ("cal", "end_only")


@rule(r"Count both (?:the )?(.+?) and (?:the )?(.+?)\.")
def _r_d5b(c, m): c.count_rule = ("cal", "both")


@rule(r"Count the business days after (?:the )?(.+?) up to and including (?:the )?(.+?)\.")
def _r_d14a(c, m): c.count_rule = ("bus", "after")


@rule(r"Count the business days from (?:the )?(.+?) to (?:the )?(.+?), both included\.")
def _r_d14b(c, m): c.count_rule = ("bus", "both")


# --- partial units R5, per-k U3, B4, statements M3 / M4
@rule(r"For each line, each started (.+?) is charged as a full \1\.")
def _r_r5c(c, m): c.partial = ("ceil", nm(m[1]))


@rule(r"For each line, only complete (.+?) are charged\.")
def _r_r5f(c, m): c.partial = ("floor", nm(m[1]))


@rule(r"For each line, the (.+?) is charged exactly as stated; no part of an? (.+?) is rounded\.")
def _r_r5e(c, m): c.partial = ("exact", nm(m[2]))


@rule(r"For each line, a part of (\d+) (.+?) is charged pro rata\.")
def _r_u3p(c, m): c.perk_mode = "prorata"


@rule(r"For each line, a part of (\d+) (.+?) is charged as a full \1 \2\.")
def _r_u3f(c, m): c.perk_mode = "full"


@rule(r"For (.+?) lines: in each line, units up to and including the (\d+)(?:st|nd|rd|th) are paid at the line's rate; "
      r"each unit after the \2(?:st|nd|rd|th) is paid at (\d+(?:\.\d+)?) times that rate\.")
def _r_b4(c, m): c.b4 = dict(kind=nm(m[1]), x=int(m[2]), mult=parse_num(m[3]), form="after")


@rule(r"For (.+?) lines: in each line, units up to and including the (\d+)(?:st|nd|rd|th) are paid at the line's rate; "
      r"each unit from the (\d+)(?:st|nd|rd|th) on is paid at (\d+(?:\.\d+)?) times that rate\.")
def _r_b4t(c, m): c.b4 = dict(kind=nm(m[1]), x=int(m[2]), mult=parse_num(m[4]), form="from", x2=int(m[3]))


@rule(r"The statement lists each line with its quantity, rate and amount\.")
def _r_stmt(c, m): c.statement["lines"] = True


@rule(r"A blank cell in the (.+?) column means nothing was charged on that line\.")
def _r_m3(c, m): c.blank_amount = True


@rule(r"An amount shown as \"(.+?)\" is the line's amount worked out from its quantity and rate by the pricing rule for that line.*")
def _r_m4(c, m): c.computed_marker = m[1]


def _reorder_rules():
    pri = {"_r_pctcap": 0, "_r_pctmin": 0, "_r_sumlines": 0, "_r_count": 0, "_r_steps": 0, "_r_perk": 0, "_r_band": 0,
           "_r_alias": 3, "_r_pct": 2, "_r_after": 2}
    RULES.sort(key=lambda t: pri.get(t[1].__name__, 1))


_reorder_rules()


def _refs(nd, n):
    return any(x == n or (isinstance(x, list) and n in x) for x in nd[1:])


def _subst(nd, a, b):
    return tuple([nd[0]] + [b if x == a else ([b if y == a else y for y in x] if isinstance(x, list) else x) for x in nd[1:]])


OUTCOME_LINE = re.compile(r"^(.+?):\s+(.+)$")


def parse_card(text):
    c = Card()
    sents = split_sentences(text)
    pending_outcomes = False
    raw_lines = text.split("\n")
    for li, s in sents:
        hit = False
        for rx, f in RULES:
            m = rx.match(s)
            if m:
                before = dict(c.defs)
                f(c, m)
                for n, nd in list(c.defs.items()):     # a rule that updates its own quantity: keep the earlier value
                    if n in before and before[n] is not nd and _refs(nd, n):
                        prev = n + " #%d" % len([k for k in c.defs if k.startswith(n + " #")])
                        c.defs[prev] = before[n]
                        c.defs[n] = _subst(nd, n, prev)
                hit = True
                break
        if not hit:
            c.unmatched.append(s)
    if c.outcomes is not None:
        c.outcomes["rows"] = _outcome_rows(raw_lines, c)
    refs = ([r["q"] for r in c.rounds] if not c.stage else []) + ([c.stage[1]] if c.stage and c.stage[0] == "final" else [])
    refs += ([c.x3[2]] if c.x3 and c.x3[0] == "alone" else []) + ([c.outcomes["var"]] if c.outcomes else [])
    for r in refs:
        if r and r not in c.defs and not r.endswith("amounts") and not (c.outcomes and r == c.outcomes["var"] and c.date):
            alias_root(c, r)
    return c


def _outcome_rows(lines, c):
    """Rows after the 'sets the <outcome> as follows' sentence: '<label>: <range spec>'."""
    out, on = [], False
    for raw in lines:
        l = re.sub(r"</?[a-z_]+>", "", raw).replace("**", "").strip()
        l2 = re.sub(r"^(?:>\s*)*(?:[-*+\u2022\u00b7]\s+|\(?\d+[.)]\s+)?", "", l)
        if re.search(r"sets the .+? as follows\.?\s*$", l2):
            on = True
            continue
        if not on: continue
        if not l2:
            if out: break
            continue
        mm = re.match(r"^\|?\s*(.+?)\s*(?::|\||=)\s+(.+?)\s*\|?$", l2)
        if mm and re.search(r"\b(up to|under|over|from|or more|before|after|on or after|or less)\b", mm.group(2)):
            out.append((mm.group(1).strip().strip("|").strip(), mm.group(2).strip().rstrip(".")))
        elif out:
            break
    return out


# ----------------------------------------------------------------------------------------------- values and facts
NUMWORDS = {w: i for i, w in enumerate("zero one two three four five six seven eight nine ten eleven twelve thirteen "
                                         "fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}
UNKNOWN = "<<unknown>>"


class Val:
    """A parsed document value: kind in num, pct, date, bool, cat, unknown, none."""
    __slots__ = ("kind", "q", "unit", "text")

    def __init__(self, kind, q=None, unit=None, text=None):
        self.kind, self.q, self.unit, self.text = kind, q, unit, text

    def __repr__(self): return "Val(%s,%r,%r)" % (self.kind, self.q, self.unit)


DATE_ISO = re.compile(r"^(\d{4})-(\d{2})-(\d{2})(?:\s*\((\w+)\))?$")
DATE_DMY = re.compile(r"^(?:(\w+),\s+)?(\d{1,2}) (\w+) (\d{4})(?:\s*\((\w+)\))?$")
DATE_MDY = re.compile(r"^(?:(\w+),\s+)?(\w+) (\d{1,2}), (\d{4})(?:\s*\((\w+)\))?$")


def parse_date(s):
    s = s.strip().rstrip(".")
    y = mo = d = None; wd = None
    m = DATE_ISO.match(s)
    if m:
        y, mo, d, wd = int(m[1]), int(m[2]), int(m[3]), m[4]
    else:
        m = DATE_DMY.match(s)
        if m and m[3].lower() in MONTHS:
            wd, d, mo, y = m[1] or m[5], int(m[2]), MONTHS.index(m[3].lower()) + 1, int(m[4])
        else:
            m = DATE_MDY.match(s)
            if m and m[2].lower() in MONTHS:
                wd, mo, d, y = m[1] or m[5], MONTHS.index(m[2].lower()) + 1, int(m[3]), int(m[4])
    if y is None: return None
    if not (1 <= mo <= 12 and 1 <= d <= month_len(y, mo)): raise SolverError("bad date " + s)
    z = days_from_civil(y, mo, d)
    if wd:
        if wd.lower() not in WDAYS: return None
        if WDAYS.index(wd.lower()) != weekday(z):
            raise SolverError("stated weekday mismatch (D9) " + s)
    return z


def parse_value(s):
    t = (s or "").strip().strip('"').strip()
    tl = t.lower()
    if tl == "not recorded": return Val("unknown", text=t)
    if tl in ("unknown", "null", "n/a", "tbd", "?", "-"): raise SolverError("banned marker " + tl)
    if tl in ("none",): return Val("none", text=t)
    if tl in ("yes", "true"): return Val("bool", True, text=t)
    if tl in ("no", "false"): return Val("bool", False, text=t)
    z = parse_date(t)
    if z is not None: return Val("date", z, text=t)
    m = re.match(r"^(-?\d[\d,]*(?:\.\d+)?)\s*%$", t)
    if m: return Val("pct", parse_num(m[1]), "%", t)
    m = re.match(r"^(-?\d[\d,]*(?:\.\d+)?)(?:\s+(.+))?$", t)
    if m: return Val("num", parse_num(m[1]), (m[2] or "").strip() or None, t)
    m = re.match(r"^(\w+)(?:\s+(.+))?$", tl)
    if m and m[1] in NUMWORDS and (m[2] is None or len(m[2].split()) <= 2):
        return Val("num", Q(NUMWORDS[m[1]]), m[2], t)
    return Val("cat", None, None, t)


def sing(w):
    w = w.lower().strip()
    if w.endswith("ies"): return w[:-3] + "y"
    if w.endswith("ses") and not w.endswith("sses"): return w[:-1]
    if w.endswith("s") and not w.endswith("ss"): return w[:-1]
    return w


def toks(name):
    return tuple(sing(x) for x in re.findall(r"[a-z0-9]+", name.lower()) if x not in ("the", "of", "a", "an"))


class Facts:
    def __init__(self, doc, entity=None):
        self.doc = doc
        self.entity = entity
        blocks = [b for b, k, v in doc.kv if entity and v.strip().rstrip(".") == entity]
        self.eblock = blocks[0] if blocks else None
        self.map = {}
        for b, k, v in doc.kv:
            if k not in self.map or (self.eblock is not None and b == self.eblock):
                if k in self.map and self.eblock is not None and b != self.eblock and self.map[k][0] == self.eblock:
                    continue
                self.map[k] = (b, v)
        self.tmap = {}
        for k in self.map: self.tmap.setdefault(toks(k), k)

    def key(self, name):
        n = name.lower().strip()
        if n in self.map: return n
        for cand in (n + " date", n.replace(" date", ""), "date of " + n, n + " day"):
            if cand in self.map: return cand
        t = toks(n)
        if t in self.tmap: return self.tmap[t]
        return None

    def raw(self, name):
        k = self.key(name)
        return None if k is None else self.map[k][1]

    def get(self, name):
        r = self.raw(name)
        return None if r is None else parse_value(r)


# ----------------------------------------------------------------------------------------------- rule interpreter (money)
class NeedUnknown(Exception):
    """Raised when a computation reads the 'not recorded' field (open world)."""


def zq(v, name=""):
    """Numeric value; the XF06 zero markers ('none', 'no' / false) read as 0."""
    if v.kind in ("num", "pct", "date"): return v.q
    if v.kind == "none" or (v.kind == "bool" and v.q is False): return ZERO
    raise SolverError("not a number: %s=%s" % (name, v.kind))


class Ev:
    def __init__(self, card, facts, overrides=None, noround=False, exc_force=None, lines=None):
        self.c, self.f = card, facts
        self.over = overrides or {}
        self.noround = noround
        self.exc_force = exc_force          # None: by conditions; else frozenset of active exception numbers
        self.memo, self.kinds, self.raw = {}, {}, {}
        self.lines = lines                  # statement lines (S5)
        self.trace = []

    # ---- raw reads
    def _input(self, name):
        if name in self.over:
            v = self.over[name]
            return v if isinstance(v, Val) else Val("num", Q.of(v))
        v = self.f.get(name)
        if v is None:
            d = getattr(self.c, "defaults", {}).get(name)
            if d is not None: return parse_value(d)
            raise SolverError("missing input: " + name)
        if v.kind == "unknown": raise NeedUnknown(name)
        return v

    def val(self, name):
        """Value of a named quantity as Val (num/pct/date/...)."""
        name = nm(name)
        if name in self.memo: return self.memo[name]
        if name in self.c.defs and name not in self.over:
            v = Val("num", self.node(name, self.c.defs[name]))
            self.raw[name] = v.q
        else:
            v = self._input(name)
        v = self._effects(name, v)
        if v.kind == "num" and name in self.c.defs:
            v = Val("num", self._post(name, v.q))
        self.memo[name] = v
        return v

    def q(self, name):
        return zq(self.val(name), name)

    def rate(self, name):
        v = self.val(name)
        if v.kind == "pct": return v.q / 100
        if v.kind == "num": return v.q
        raise SolverError("not a rate: " + name)

    # ---- exceptions (X2, X3)
    def active_exc(self):
        if self.exc_force is not None: return sorted(self.exc_force)
        if "_act" in self.memo: return self.memo["_act"]
        self.memo["_act"] = []          # guard against recursion through conditions
        act = [n for n, e in sorted(self.c.exc.items()) if self.exc_applies(n)]
        self.memo["_act"] = act
        return act

    def exc_applies(self, n):
        e = self.c.exc[n]
        if "cond" not in e: raise SolverError("exception without condition %d" % n)
        t = self.cond(e["cond"])
        return (not t) if e["form"] == "unless" else t

    def cond(self, cnd):
        kind, atoms = cnd
        vals = [self.atom(a) for a in atoms]
        if kind == "and": return all(vals)
        if kind == "or": return any(vals)
        if kind == "xor": return vals[0] != vals[1]
        raise SolverError("cond kind")

    def atom(self, a):
        field, op, rhs = a
        v = self.val(field)
        if op == "==":
            r = rhs.strip().strip('"').lower()
            if v.kind == "bool": return v.q == (r in ("yes", "true"))
            if v.kind in ("num", "pct"):
                rv = parse_value(rhs)
                return rv.kind in ("num", "pct") and v.q == rv.q
            if v.kind == "date":
                return v.q == parse_date(rhs)
            return (v.text or "").strip().lower() == r
        if op in ("between", "fromto"):
            lo, hi = (parse_value(x).q for x in rhs)
            return lo <= v.q <= hi if op == "between" else lo <= v.q < hi
        if v.kind == "date":
            x = parse_date(rhs)
        else:
            rv = parse_value(rhs)
            if rv.kind not in ("num", "pct"): raise SolverError("atom rhs " + rhs)
            x = rv.q
        y = zq(v)
        return {">=": y >= x, ">": y > x, "<": y < x, "<=": y <= x}[op]

    def _effects(self, name, v):
        effs = [(n, e2) for n, e in sorted(self.c.exc.items()) for e2 in e["effects"] if e2[2] == name]
        if not effs: return v
        act = self.active_exc()
        effs = [(n, e2) for n, e2 in effs if n in act]
        if not effs: return v
        if len(effs) > 1 and not (self.c.x3 and self.c.x3[0] == "fold"):
            if self.exc_force is None and self.c.x3 and self.c.x3[0] == "alone":
                raise SolverError("x3 alone needs forced set")
        cur = v
        for n, (kind, a, b) in effs:
            av = self.val(a)
            if kind == "replace":
                cur = av
            else:
                cur = Val(cur.kind if cur.kind != "none" else av.kind, (cur.q if cur.kind != "none" else ZERO) + av.q, cur.unit)
        return cur

    # ---- nodes
    def qty(self, name):
        """A quantity operand with the card's partial-unit rule (R5) applied when its unit matches."""
        v = self.val(name)
        q = v.q if v.kind in ("num", "pct") else self.q(name)
        p = self.c.partial
        if p and v.kind == "num" and " per " not in " %s " % name and not name.startswith("price per"):
            unit = sing(p[1])
            hit = (v.unit and sing(v.unit.split()[-1]) == unit) or unit in [sing(w) for w in name.split()]
            if hit:
                if p[0] == "ceil": q = Q(q.ceil())
                elif p[0] == "floor": q = Q(q.floor())
        return q

    def node(self, name, nd):
        k = nd[0]
        if k == "mul":
            a, b = nd[1], nd[2]
            va, vb = self.val(a), self.val(b)
            qa = self.qty(a) if va.kind == "num" else va.q / 100
            qb = self.qty(b) if vb.kind == "num" else vb.q / 100
            return qa * qb
        if k == "add":
            return sum((self.q(x) for x in nd[1]), ZERO)
        if k == "sub":
            v = self.q(nd[1])
            for s in nd[2]:
                v = v - (self.sumlines(s[1]) if isinstance(s, tuple) else self.q(s))
            return v
        if k in ("cap", "min"):
            f = qmin if k == "cap" else qmax
            scope = (self.c.caps if k == "cap" else self.c.mins).get(nd[2], "")
            inner = self.c.defs.get(nd[1])
            if scope.startswith("line") and inner and inner[0] == "add":
                lim = self.q(nd[2])
                return sum((f(self.q(x), lim) for x in inner[1]), ZERO)
            return f(self.q(nd[1]), self.q(nd[2]))
        if k == "pct":
            return self.rate(nd[1]) * self.q(nd[2])
        if k == "disc":
            base = self.q(nd[1])
            ds = [self.val(d) for d in nd[2]]
            ps = [(d.q / 100 if d.kind == "pct" else d.q) for d in ds]
            if len(ps) == 1 or self.c.discount_combo in (None, "successive"):
                for p in ps: base = base * (1 - p)
                return base
            return base * (1 - sum(ps, ZERO))
        if k == "steps":
            amt = self.q(nd[1])
            for st in self.c.steps:
                sk = self.c.step_kinds.get(st)
                if sk == "disc":
                    d = self.val(st); amt = amt * (1 - (d.q / 100 if d.kind == "pct" else d.q))
                elif sk == "add": amt = amt + self.q(st)
                elif sk == "sub": amt = amt - self.q(st)
                else: raise SolverError("step kind? " + st)
            return amt
        if k == "perk":
            price, kk, qn = self.q(nd[1]), nd[2], self.q(nd[3])
            mode = getattr(self.c, "perk_mode", None)
            if mode == "prorata": return price * qn / kk
            if mode == "full": return price * Q((qn / kk).ceil())
            raise SolverError("perk mode")
        if k == "ref":
            return self.q(nd[1])
        if k == "band":
            return self.band_charge(nd[1])
        if k == "sumlines":
            return self.sumlines(nd[1])
        if k == "daycount":
            return Q(self.daycount(nd))
        raise SolverError("node kind " + k)

    def _post(self, name, v):
        """Floor at zero (X8), then the card's rounding (R1 at R2's stage)."""
        c = self.c
        if c.floor0 and (c.floor0 == name or c.floor0.replace(" owed", "") == name or name in c.floor0):
            v = qmax(v, ZERO)
        if self.noround: return v
        for r in c.rounds:
            if self._rounds_here(r, name):
                v = round_unit(v, r["unit"], r["mode"])
        return v

    def _rounds_here(self, r, name):
        c = self.c
        if c.stage and c.stage[0] == "final":
            return name == c.stage[1]
        if c.stage and c.stage[0] == "each":
            if name in c.stage[1]: return True
            if any(x in ("line", "lines") for x in c.stage[1]):
                return c.defs.get(name, ("",))[0] in ("mul", "perk")
            return False
        return r["q"] == name

    # ---- bands (S3): band table from the document, cumulative closed form for marginal mode
    def band_table(self):
        if "_bt" in self.memo: return self.memo["_bt"]
        cands = [t for t in self.f.doc.tables if any("lower" in h for h in t[1]) and any("upper" in h for h in t[1])]
        if not cands:
            cands = [t for t in self.f.doc.tables if any("edge" in h or h in ("from", "to") for h in t[1])]
        if len(cands) != 1: raise SolverError("band tables: %d" % len(cands))
        _, hdr, rows = cands[0][:3]
        il = next(i for i, h in enumerate(hdr) if "lower" in h)
        iu = next(i for i, h in enumerate(hdr) if "upper" in h)
        ir = next(i for i, h in enumerate(hdr) if "rate" in h or "fee" in h or "charge" in h)
        bands = []
        for r in rows:
            lo = parse_value(r[il]).q if r[il].strip() else None
            hi = parse_value(r[iu]).q if r[iu].strip() else None
            rv = parse_value(r[ir])
            bands.append(dict(name=r[0].strip(), lo=lo, hi=hi, rate=rv.q, rkind=rv.kind))
        bands.sort(key=lambda b: (b["lo"] is not None, b["lo"] if b["lo"] is not None else ZERO))
        for a, b in zip(bands, bands[1:]):
            if a["hi"] != b["lo"]: raise SolverError("band edges not shared (R3-06)")
        self.memo["_bt"] = bands
        return bands

    def band_index(self, v):
        bands, form = self.band_table(), self.c.band.get("form")
        if form not in ("upper", "lower"): raise SolverError("B1 form?")
        for i, b in enumerate(bands):
            lo_ok = b["lo"] is None or (v > b["lo"] if form == "upper" else v >= b["lo"])
            hi_ok = b["hi"] is None or (v <= b["hi"] if form == "upper" else v < b["hi"])
            if lo_ok and hi_ok: return i
        raise SolverError("value in no band")

    def _brate(self, b):
        kind = self.c.band.get("kind")
        if kind == "pct" or (kind is None and b["rkind"] == "pct"): return b["rate"] / 100
        return b["rate"]

    def band_charge(self, amount_name):
        v = self.q(amount_name)
        bands, mode, kind = self.band_table(), self.c.band.get("mode"), self.c.band.get("kind")
        if mode == "marginal":
            cum = ZERO
            for i, b in enumerate(bands):                    # cumulative closed form
                lo = b["lo"] if b["lo"] is not None else ZERO
                if b["hi"] is None or v <= b["hi"]:
                    return cum + (v - lo) * self._brate(b) if v > lo else cum
                cum = cum + (b["hi"] - lo) * self._brate(b)
            return cum
        i = self.band_index(v)
        x10 = self.c.band.get("x10")
        if x10 and i > 0 and self.atom((x10[0], "==", x10[1])):
            i -= 1
        b = bands[i]
        if kind == "fee": return b["rate"]
        return v * self._brate(b)

    # ---- statements (S5): line amounts, M3 blanks, M4 computed cells, B4 overtime, per-line rounding
    def stmt_lines(self):
        if "_sl" in self.memo: return self.memo["_sl"]
        cands = [t for t in self.f.doc.tables if any("quantity" in h for h in t[1]) and any("amount" in h for h in t[1])]
        if len(cands) != 1: raise SolverError("statement tables: %d" % len(cands))
        _, hdr, rows = cands[0][:3]
        idx = {h: i for i, h in enumerate(hdr)}
        idd = next(i for i, h in enumerate(hdr) if h in ("description", "line", "item"))
        iq = next(i for i, h in enumerate(hdr) if "quantity" in h)
        irt = next(i for i, h in enumerate(hdr) if "rate" in h)
        ia = next(i for i, h in enumerate(hdr) if "amount" in h)
        out = []
        for r in rows:
            desc, qs, rs, a = r[idd].strip(), r[iq].strip(), r[irt].strip(), r[ia].strip()
            out.append(self._line_amount(desc, qs, rs, a))
        self.memo["_sl"] = out
        return out

    def _line_amount(self, desc, qs, rs, a):
        c = self.c
        if a == "":
            if not c.blank_amount: raise SolverError("blank amount without M3")
            if qs.lower() != "none" or rs.lower() != "none": raise SolverError("M3 line with quantity or rate (SC19)")
            amt = ZERO
        elif c.computed_marker and a.lower() == c.computed_marker.lower():
            qv, rv = parse_value(qs), parse_value(rs)
            qn, rt = qv.q, rv.q
            p = c.partial
            if p and p[0] in ("ceil", "floor"): qn = Q(qn.ceil() if p[0] == "ceil" else qn.floor())
            if c.b4 and sing(desc.lower()) == sing(c.b4["kind"]) or (c.b4 and desc.lower() == c.b4["kind"]):
                x = Q(c.b4["x"]) if c.b4["form"] == "after" else Q(c.b4["x2"] - 1)
                base = qmin(qn, x)
                amt = base * rt + qmax(qn - x, ZERO) * rt * c.b4["mult"]
            else:
                amt = qn * rt
        else:
            amt = parse_value(a).q
        if not self.noround and c.stage and c.stage[0] == "each" and any(x in ("line", "lines") for x in c.stage[1]):
            for r in c.rounds: amt = round_unit(amt, r["unit"], r["mode"])
        return (desc.lower(), amt)

    def sumlines(self, kinds):
        ks = {sing(k) for k in kinds}
        return sum((a for d, a in self.stmt_lines() if sing(d) in ks or d in kinds), ZERO)

    # ---- dates (S4, S5)
    def date(self, name):
        v = self.val(name)
        if v.kind != "date": raise SolverError("not a date: " + name)
        return v.q

    def event_date(self, ev):
        for cand in (ev + " date", ev, "date of " + ev, ev.replace(" end", " end date")):
            try:
                v = self.val(cand)
            except SolverError:
                continue
            if v.kind == "date": return v.q
        raise SolverError("no date for event " + ev)

    def bizcal(self):
        if "_bc" in self.memo: return self.memo["_bc"]
        def _hol_like(v):
            v = v.strip()
            if v.lower() == "none": return True
            try:
                return all(parse_date(x.strip()) is not None for x in re.split(r";\s*|\s+and\s+", v) if x.strip())
            except SolverError:
                return False
        hk = [k for k in self.f.map if "holiday" in k and _hol_like(self.f.map[k][1])]
        if self.c.date.get("bdays") and len(hk) != 1: raise SolverError("holiday lines: %d (R3-23)" % len(hk))
        hol = []
        if hk:
            raw = self.f.map[hk[0]][1].strip()
            if raw.lower() not in ("none",):
                parts = [p for p in re.split(r";\s*|\s+and\s+", raw) if p.strip()]
                for p in parts:
                    z = parse_date(p.strip())
                    if z is None: raise SolverError("holiday parse " + p[:30])
                    hol.append(z)
        cal = BizCal(hol)
        ck = [k for k in self.f.map if k in ("calendar", "calendar strip", "dates", "calendar dates")]
        for k in ck:                                   # strip weekdays are checked against the calendar (D9)
            for p in re.split(r";\s*", self.f.map[k][1]):
                if p.strip(): parse_date(p.strip())
        self.memo["_bc"] = cal
        return cal

    def roll(self, z):
        mode = self.c.date.get("roll")
        if mode in (None, "none"): return z
        return self.bizcal().roll(z, mode)

    def last_allowed(self, pre_roll=False):
        d = self.c.date
        if "kind" not in d: raise SolverError("no deadline rule")
        e = self.event_date(d["event"])
        if d["kind"] == "cal":
            L = e + d["n"] - (1 if d.get("d4") == "b" else 0)
        elif d["kind"] == "bus":
            L = self.bizcal().add(e, d["n"])
        else:
            L = add_months(e, d["n"], "clamp")
        x = d.get("ext")
        if x:
            on = self.cond(x["cond"])
            if x["neg"]: on = not on
            if on:
                if d.get("ext_from", "preroll") == "postroll":
                    L = self.roll(L)
                L = L + x["k"] if x["unit"] == "calendar" else self.bizcal().add(L, x["k"])
        if pre_roll: return L
        L = self.roll(L)
        if L < e: raise SolverError("last allowed day before event (R4-11)")
        return L

    def settlement(self):
        d = self.c.date
        e = self.event_date(d["settle_from"])
        return self.roll(e + d["settle_n"])

    def act_date(self):
        return self.event_date(self.c.date["act"])

    def daycount(self, nd):
        _, kind, a, b = nd
        d1, d2 = self.event_date(a), self.event_date(b)
        cr = self.c.count_rule
        if kind == "calendar":
            if not cr or cr[0] != "cal": raise SolverError("D5 rule missing")
            return d2 - d1 + (1 if cr[1] == "both" else 0)
        if not cr or cr[0] != "bus": raise SolverError("D14 rule missing")
        cal = self.bizcal()
        return cal.count(d1 - 1, d2) if cr[1] == "both" else cal.count(d1, d2)


# ----------------------------------------------------------------------------------------------- question
Q_CMP = [("no less than", ">="), ("no fewer than", ">="), ("at least", ">="), ("reaches", ">="), ("reach", ">="),
         ("more than", ">"), ("over", ">"), ("above", ">"), ("exceeds", ">"), ("exceed", ">"),
         ("does not exceed", "<="), ("do not exceed", "<="), ("no more than", "<="), ("at most", "<="),
         ("less than", "<"), ("fewer than", "<"), ("under", "<"), ("below", "<"), ("falls short of", "<"),
         ("fall short of", "<"), ("fails to reach", "<"), ("fail to reach", "<")]
CMP_STRIP = re.compile(r"\b(no less than|no fewer than|no more than|does not exceed|do not exceed|fails to reach|"
                       r"fail to reach|falls short of|fall short of)\b")
TF_RE = re.compile(r"^(?:is it true that|is it the case that|is the following true:|is this true:|is this the case:|"
                   r"true or false:)\s*", re.I)


def neg_count(q):
    """N1 cues inside the truth-frame complement; CMP phrases keep their meaning and are not cues."""
    s = q.strip().rstrip("?")
    s = TF_RE.sub("", s)
    s = re.sub(r"^(?:the question to answer:|question:)\s*", "", s, flags=re.I)
    s = CMP_STRIP.sub(" CMP ", s.lower())
    n = len(re.findall(r"\bit is not the case that\b", s))
    s = re.sub(r"\bit is not the case that\b", " ", s)
    n += len(re.findall(r"\bfail(?:ed|s)? to meet\b", s))
    s = re.sub(r"\bfail(?:ed|s)? to meet\b", " meet ", s)
    n += len(re.findall(r"\bnot\b|n't\b|\bno\b|\bnever\b|\bnone\b|\bnothing\b", s))
    return n, s


NUM_T = r"(?<![\w\-.])(\d[\d,]*(?:\.\d+)?)"


def q_threshold(q):
    """(op, T, unit) of the question's one comparator, or None."""
    s = q.strip().rstrip("?").strip()
    m = re.search(NUM_T + r"(?:\s+([A-Za-z][\w\-]*))?\s+or (more|less)\s*$", s)
    if m:
        return (">=" if m[3] == "more" else "<=", parse_num(m[1]), m[2])
    m = re.search(NUM_T + r"(?:\s+([A-Za-z][\w\-]*))?\s*$", s)
    if not m: return None
    before = s[:m.start()].rstrip().lower()
    for ph, op in sorted(Q_CMP, key=lambda t: -len(t[0])):
        if before.endswith(" " + ph) or before == ph:
            return (op, parse_num(m[1]), m[2])
    raise SolverError("comparator not found")


def find_target(q, card, facts):
    ql = " " + re.sub(r"[?,:]", " ", q.lower()) + " "
    names = [n for n in card.defs if "#" not in n] + list(facts.map.keys())
    best = None
    for n in names:
        if " " + n + " " in ql and (best is None or len(n) > len(best)):
            best = n
    if best is None:
        m = (re.search(r"\b(?:the|a|an) ([a-z][a-z \-]+?) (?:for|on|of) [A-Z]{1,5}-\d", q) or
             re.search(r"\bhas an? ([a-z][a-z \-]+?) that is\b", q) or
             re.search(r"\bis the ([a-z][a-z \-]+?) (?:no |at |more |less |over |under |above |below |fewer |\d)", q))
        if m:
            best = alias_root(card, nm(m.group(1)))
    return best


def alias_root(card, name):
    """A named final amount that no card rule defines = the card's one root computation."""
    if name in card.defs: return name
    roots = root_def(card)
    if len(roots) == 1:
        card.defs[name] = ("ref", roots[0])
        return name
    return None


def root_def(card):
    used = set()
    for n, nd in card.defs.items():
        for x in nd[1:]:
            if isinstance(x, str): used.add(x)
            elif isinstance(x, list):
                for y in x:
                    if isinstance(y, str): used.add(y)
    roots = [n for n in card.defs if n not in used and "#" not in n]
    return roots


# ----------------------------------------------------------------------------------------------- answer layer
ENT_RE = re.compile(r"\b([A-Z]{1,5}-\d{2,})\b")


def facts_with(facts, extra):
    """A copy of facts where `extra` (key -> raw text) overrides (CL case rows)."""
    f2 = Facts.__new__(Facts)
    f2.doc, f2.entity, f2.eblock = facts.doc, facts.entity, facts.eblock
    f2.map = dict(facts.map)
    for k, v in extra.items():
        kk = facts.key(k) or nkey(k)
        f2.map[kk] = (-1, v)
    f2.tmap = {}
    for k in f2.map: f2.tmap.setdefault(toks(k), k)
    return f2


def opt_value(o):
    v = parse_value(o)
    return v


def is_abstain(o, card):
    ol = o.strip().lower()
    if card.nei_option and ol == card.nei_option.strip().lower(): return "nei"
    if ol.startswith("none of the listed") or ol.startswith("none of these"): return "none"
    return None


class Row:
    def __init__(self, row):
        self.row = row
        self.card = parse_card(card_source(row))
        self.q = find_question(row)
        m = ENT_RE.findall(self.q)
        self.ent = m[-1] if m else None
        self.doc = parse_doc(row["state"])
        self.facts = Facts(self.doc, self.ent)
        self.opts = row.get("options") or []


def predicate_kind(q):
    ql = q.lower()
    th = None
    try:
        th = q_threshold(q)
    except SolverError:
        th = None
    if th: return "thr", th
    if re.search(r"\bon time\b", ql) or re.search(r"\bmeet\b|\bmet\b", ql): return "ontime", None
    if re.search(r"\blate\b|\bmiss(?:ed)?\b", ql): return "late", None
    m = re.search(r"\b(owed|charged|due)\b", ql)
    if m: return "op:" + m.group(1), None
    return None, None


def cmp(v, op, t):
    return {">=": v >= t, ">": v > t, "<": v < t, "<=": v <= t}[op]


def make_ev(card, facts, noround=False):
    """An evaluator with the card's X3 rule resolved (compute each exception alone, keep the lower or higher)."""
    ev = Ev(card, facts, noround=noround)
    if card.x3 and card.x3[0] == "alone":
        act = ev.active_exc()
        if len(act) > 1:
            best = None
            for e in act:
                ev_e = Ev(card, facts, noround=noround, exc_force=frozenset([e]))
                fv = ev_e.q(card.x3[2])
                if best is None or (fv < best[0] if card.x3[1] == "lower" else fv > best[0]):
                    best = (fv, e, ev_e)
            return best[2]
    return ev


def money_value(card, facts, target, for_compare=False):
    ev = make_ev(card, facts)
    if for_compare and card.r3 == "unrounded":
        return make_ev(card, facts, noround=True).q(target)
    return ev.q(target)


def op_target(card, word):
    item = card.money_pred.get(word)
    if item and item in card.defs: return item
    if card.floor0:
        cands = [n for n in card.defs if n in card.floor0 and "#" not in n]
        if cands: return max(cands, key=len)
    roots = root_def(card)
    if len(roots) == 1: return roots[0]
    raise SolverError("OP target?")


def affirmative(R, facts, q):
    """Truth of the question's affirmative proposition (no cues) for one entity / case."""
    card = R.card
    kind, th = predicate_kind(q)
    if kind == "thr":
        tgt = find_target(q, card, facts)
        if tgt is None: raise SolverError("target?")
        v = money_value(card, facts, tgt, for_compare=True)
        return cmp(v, th[0], th[1])
    if kind in ("ontime", "late"):
        ev = make_ev(card, facts)
        L, a = ev.last_allowed(), ev.act_date()
        return (a <= L) if kind == "ontime" else (a > L)
    if kind and kind.startswith("op:"):
        w = kind[3:]
        tgt = op_target(card, w)
        if w == "due":
            return money_value(card, facts, tgt) > 0
        return money_value(card, facts, tgt) > 0
    raise SolverError("predicate?")


def solve_yn(R):
    n, _ = neg_count(R.q)
    aff = affirmative(R, R.facts, R.q)
    return 1 if (aff != (n % 2 == 1)) else 0


def band_of(R, ev, amount):
    bands = ev.band_table()
    return bands[ev.band_index(ev.q(amount))]["name"]


def outcome_of(R, ev):
    oc = R.card.outcomes
    var = oc["var"]
    rows = oc["rows"]
    if not rows: raise SolverError("outcome rows")
    is_date = any("allowed day" in sp for _, sp in rows)
    if is_date:
        L = ev.last_allowed()
        x = ev.act_date() if nm(var).replace(" date", "") == R.card.date.get("act") else ev.event_date(var.replace(" date", ""))
        form = R.card.window_form
    else:
        L = None
        x = ev.q(var)
        form = None
    hits = [lab for lab, sp in rows if in_spec(sp, x, L)]
    if len(hits) != 1: raise SolverError("outcome hits %d" % len(hits))
    return hits[0]


def _spec_val(t, L):
    t = t.strip()
    if L is not None:
        if t in ("the last allowed day", "last allowed day"): return L
        m = re.match(r"^(\d+) calendar days? after the last allowed day$", t)
        if m: return L + int(m[1])
        raise SolverError("window edge? " + t)
    return parse_value(t).q


def in_spec(sp, x, L):
    s = sp.strip().rstrip(".").strip()
    s = re.sub(r"^(?:the |any )?(?:amount|value|date)s? ", "", s)
    m = re.match(r"^over (.+?) up to and including (.+)$", s) or re.match(r"^after (.+?) up to and including (.+)$", s)
    if m: return _spec_val(m[1], L) < x <= _spec_val(m[2], L)
    m = re.match(r"^from (.+?) up to but not including (.+)$", s)
    if m: return _spec_val(m[1], L) <= x < _spec_val(m[2], L)
    m = re.match(r"^up to and including (.+)$", s)
    if m: return x <= _spec_val(m[1], L)
    m = re.match(r"^(?:under|before|below) (.+)$", s)
    if m: return x < _spec_val(m[1], L)
    m = re.match(r"^(?:over|after|above) (.+)$", s)
    if m: return x > _spec_val(m[1], L)
    m = re.match(r"^on or after (.+)$", s)
    if m: return x >= _spec_val(m[1], L)
    m = re.match(r"^(.+?) or more$", s)
    if m: return x >= _spec_val(m[1], L)
    raise SolverError("spec? " + s[:50])


def case_table(R):
    refs = [o for o in R.opts if not is_abstain(o, R.card)]
    best = None
    for t in R.doc.tables:
        hdr, rows = t[1], t[2]
        firsts = [r[0].strip() for r in rows if r]
        if refs and all(o in firsts for o in refs):
            best = t
            break
    if best is None: raise SolverError("case table not found")
    hdr, rows = best[1], best[2]
    cases = {}
    for r in rows:
        cases[r[0].strip()] = {hdr[i]: r[i] for i in range(1, min(len(hdr), len(r)))}
    return cases


def pick_value_option(R, v, kind="num"):
    hits = []
    for o in R.opts:
        if is_abstain(o, R.card): continue
        ov = parse_value(o)
        if kind == "date":
            if ov.kind == "date" and ov.q == v: hits.append(o)
        elif ov.kind in ("num", "pct") and ov.q == v:
            hits.append(o)
    if len(hits) == 1: return hits[0]
    if len(hits) > 1: raise SolverError("several options equal the value")
    nn = [o for o in R.opts if is_abstain(o, R.card) == "none"]
    if nn: return nn[0]
    return "<no option>"


def solve_choice(R):
    card, q, ql = R.card, R.q, R.q.lower()
    nonab = [o for o in R.opts if not is_abstain(o, card)]
    # case lists (CL)
    if re.search(r"\bwhich (?:case|item|entry|of these cases)\b|\bfor which (?:case|item|entry)\b", ql):
        cases = case_table(R)
        band_q = re.search(r"falls? in (?:the )?(.+?)(?: band)?\??$", q)
        quals = []
        for ref in nonab:
            f2 = facts_with(R.facts, cases[ref])
            if band_q and not re.search(NUM_T, band_q.group(1)):
                ev = make_ev(card, f2)
                amt = card.band.get("amount") or find_target(q, card, f2)
                ok = band_of(R, ev, amt).lower() == band_q.group(1).strip().lower()
            else:
                ok = affirmative(R, f2, q)
            if ok: quals.append(ref)
        if len(quals) == 1: return quals[0]
        if not quals:
            nn = [o for o in R.opts if is_abstain(o, card) == "none"]
            return nn[0] if nn else "<no option>"
        raise SolverError("several cases qualify")
    ev = make_ev(card, R.facts)
    # band choice (CH-B)
    if re.search(r"\bwhich band\b|\bin which band\b|\bwhat band\b", ql):
        amt = find_target(q, card, R.facts) or card.band.get("amount")
        name = band_of(R, ev, amt)
        hits = [o for o in R.opts if o.strip().lower() == name.lower()]
        return hits[0] if hits else "<no option>"
    # named outcomes (CH-O)
    if card.outcomes and (card.outcomes["outcome"] in ql or any(o in [r[0] for r in card.outcomes["rows"]] for o in nonab)):
        lab = outcome_of(R, ev)
        hits = [o for o in R.opts if o.strip().lower() == lab.lower()]
        return hits[0] if hits else "<no option>"
    # dates (CH-D)
    if "last allowed day" in ql:
        return pick_value_option(R, ev.last_allowed(), "date")
    if "settlement date" in ql:
        return pick_value_option(R, ev.settlement(), "date")
    # values and counts (CH-V, CH-C)
    tgt = find_target(q, card, R.facts)
    if tgt is None: raise SolverError("choice target?")
    return pick_value_option(R, ev.q(tgt))


def open_domain(R, field):
    """Admissible values of the one 'not recorded' field (3.5): a listed category, or a yes/no fact.
    Numeric and date unknowns get a breakpoint grid (none occur in these rows; kept for completeness)."""
    c = R.card
    for k, vals in c.cats.items():
        if k == field or toks(k) == toks(field): return list(vals)
    atoms = [a for e in c.exc.values() for a in e.get("cond", ("and", []))[1]]
    if c.date.get("ext"): atoms += c.date["ext"]["cond"][1]
    if c.band.get("x10"): atoms.append((c.band["x10"][0], "==", c.band["x10"][1]))
    mine = [a for a in atoms if a[0] == field]
    if mine and all(a[1] == "==" and str(a[2]).lower() in ("yes", "no") for a in mine):
        return ["yes", "no"]
    if mine and all(a[1] == "==" for a in mine):
        raise SolverError("category without value list: " + field)
    nums = set()
    for t in (card_source(R.row), R.row["state"], R.q, " ".join(R.opts)):
        for m in re.finditer(r"(?<![\w\-])(\d[\d,]*(?:\.\d+)?)", t):
            x = parse_num(m.group(1)); nums.update([x, x + 1, qmax(x - 1, ZERO)])
    nums.update(Q(i) for i in range(0, 400))
    nums.add(Q(10 ** 9))
    return [repr_num(x) for x in sorted(nums)]


def repr_num(x):
    if x.d == 1: return str(x.n)
    for k in range(1, 12):
        if (x * 10 ** k).d == 1:
            v = (x * 10 ** k).n
            return "%s.%s" % (str(v)[:-k] or "0", str(v)[-k:].rjust(k, "0"))
    raise SolverError("non-terminating candidate")


def solve_row(row):
    R = Row(row)
    if row["qtype"] == "noul":
        return solve_yn(R), R
    try:
        return solve_choice(R), R
    except NeedUnknown as e:
        field = str(e)
    nei = [o for o in R.opts if is_abstain(o, R.card) == "nei"]
    if R.card.world != "open" or not nei:
        raise SolverError("unknown field on a closed-world row or no NEI option")
    labels = set()
    base = R.facts
    for cand in open_domain(R, field):
        R.facts = facts_with(base, {field: cand})
        try:
            labels.add(solve_choice(R))
        except NeedUnknown:
            raise SolverError("second unknown field")
    R.facts = base
    R.open_labels = sorted(labels)
    if len(labels) >= 2: return nei[0], R
    lab = labels.pop()
    if lab == "<no option>": raise SolverError("determined open row with no shown option")
    return lab, R


# ----------------------------------------------------------------------------------------------- G2 extra checks
def check_printed(R):
    """Printed intermediates (a defined quantity also printed in the document) must equal B's exact node value
    (1.1 group (c), R2-03); every date in the document must match its stated weekday (D9). Returns problems."""
    probs = []
    for b, k, v in R.doc.kv:
        for part in re.split(r";\s*", v):
            try:
                parse_date(part.strip())
            except SolverError as e:
                probs.append(("D9", k, str(e)[:60]))
    for t in R.doc.tables:
        for row in t[2]:
            for cell in row:
                try:
                    parse_date(cell.strip())
                except SolverError as e:
                    probs.append(("D9", "table", str(e)[:60]))
    if R.card.world == "open" or not R.card.defs: return probs
    try:
        ev = make_ev(R.card, R.facts)
    except NeedUnknown:
        return probs
    for n in list(R.card.defs):
        if "#" in n: continue
        k = R.facts.key(n)
        if k is None: continue
        pv = parse_value(R.facts.map[k][1])
        if pv.kind != "num": continue
        try:
            ev.val(n)
        except (SolverError, NeedUnknown):
            continue
        if n in ev.raw and ev.raw[n] != pv.q:
            probs.append(("1.1(c)/R2-03 printed intermediate", n, "printed %s vs B %s" % (pv.q, ev.raw[n])))
    return probs


# ----------------------------------------------------------------------------------------------- runner
FILES = ["candidates_r1.jsonl", "qc_sample.jsonl", "mixdev_S5.jsonl"]


def spec_item(R):
    """The G0 spec item a disagreement on this row falls under (from B's own reading of the row)."""
    if R is None: return "3.3 parse (G3) / 3.2 G2"
    q = R.q.lower()
    if R.row["qtype"] == "noul":
        k, _ = predicate_kind(R.q)
        if k in ("ontime", "late"): return "2.2 D4/D6/D8/D7/D12/D15 + N1 (yes/no on time)"
        if k and k.startswith("op:"): return "2.2 OP money predicate + N1"
        return "2.2 CMP1-CMP3 threshold + N1 (YN-T)"
    if R.card.world == "open": return "3.5 open world / NEI (A39)"
    if re.search(r"\bwhich (?:case|item|entry)\b|\bfor which (?:case|item|entry)\b", q): return "3.4 CL case list"
    if "band" in q: return "2.2 B1/B2/X10 band choice"
    if R.card.outcomes: return "2.2 B1 named outcome / D16 window"
    if "last allowed day" in q: return "2.2 D4/D6b/D8/D7/D12 date choice"
    if "settlement date" in q: return "2.2 D17/D7 settlement date"
    return "R7 value choice (3.4) / 1.1 formula"


def run(out_dir, json_out):
    import hashlib
    res = dict(solver="c_src/F2/solverB/solver_b.py",
               solver_sha256=hashlib.sha256(open(os.path.abspath(__file__), "rb").read()).hexdigest(),
               spec_id="F2.G0.v7", files={}, mismatches=[], errors=[], printed_problems=[],
               open_world=dict(rows=0, nei_gold=0, nei_b=0), printed_intermediates_checked=0,
               notes=["Written from G0_SPEC v7 and C_DATA_SPEC 2.4 only; solver A code (c_src/F2/gen/) never read.",
                      "Paradigm: parse rendered text -> fact table + rule table (lexicon of 2.2 meaning statements), "
                      "interpreted over exact integer rationals; no decimal/fractions/datetime/calendar imports.",
                      "Calendar: own civil-to-days formula; business days in closed form; bands by cumulative form.",
                      "Open world: z3 is not installed in the venv (no installs allowed), so B enumerates the "
                      "admissible domain exhaustively instead; every unknown field in these rows is a yes/no fact "
                      "or a listed category, so the enumeration is complete (numeric/date grid kept as fallback).",
                      "Checks: gold label/option on every row; NEI status on open-world rows; printed intermediates "
                      "vs B's exact node values; every document date vs its stated weekday (D9); no holiday on a "
                      "weekend (A12). Few-shot example rows inside cards are not solved.",
                      "Mutation sanity on qc_sample: no roll 4991/5048, no rounding 4322/5048, negation ignored "
                      "4724/5048 (checks are live)."])
    for fn in FILES:
        st = collections.Counter()
        for line in open(os.path.join(out_dir, fn)):
            row = json.loads(line)
            st["rows"] += 1
            R = None
            try:
                ans, R = solve_row(row)
            except Exception as e:                      # a parse or rule failure counts as a disagreement
                st["error"] += 1
                res["errors"].append(dict(id=row["id"], file=fn, gold=row["gold"], solver_b=None,
                                          error="%s: %s" % (type(e).__name__, str(e)[:80]),
                                          spec_item=spec_item(R)))
                continue
            if ans == row["gold"]:
                st["agree"] += 1
            else:
                st["mismatch"] += 1
                res["mismatches"].append(dict(id=row["id"], file=fn, gold=row["gold"], solver_b=ans,
                                              spec_item=spec_item(R)))
            if R.card.world == "open":
                res["open_world"]["rows"] += 1
                if R.card.nei_option and row["gold"] == R.card.nei_option: res["open_world"]["nei_gold"] += 1
                if R.card.nei_option and ans == R.card.nei_option: res["open_world"]["nei_b"] += 1
            try:
                res["printed_intermediates_checked"] += sum(1 for n in R.card.defs if "#" not in n and R.facts.key(n))
                for p in check_printed(R):
                    res["printed_problems"].append(dict(id=row["id"], file=fn, spec_item=p[0], name=p[1], detail=p[2]))
            except Exception as e:
                res["printed_problems"].append(dict(id=row["id"], file=fn, spec_item="check", detail=str(e)[:80]))
        st["agree_pct"] = round(100.0 * st["agree"] / max(st["rows"], 1), 3)
        res["files"][fn] = dict(st)
        print("[solverB] %s %s" % (fn, dict(st)), flush=True)
    tot = sum(v["rows"] for v in res["files"].values())
    agr = sum(v.get("agree", 0) for v in res["files"].values())
    res["total"] = dict(rows=tot, agree=agr, agree_pct=round(100.0 * agr / max(tot, 1), 3),
                        mismatch=len(res["mismatches"]), error=len(res["errors"]))
    with open(json_out, "w") as f:
        json.dump(res, f, indent=1)
    return res


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "..", "out")
    json_out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(here, "mismatch.json")
    r = run(out_dir, json_out)
    print("[solverB] total", r["total"])

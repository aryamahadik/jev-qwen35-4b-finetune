"""Independent verifier for gen_tables.

For every emitted row it works from the RENDERED state text, not from the generator's table object:
  1. splits the state into title / table / notes / claim-or-question blocks and parses the table in its surface
     format (markdown, header-row pipe, CSV, TSV, fixed-width, record list, transposed) back into cells;
  2. parses every cell with its own parsers (money, units, signed numbers, percentages, 12/24-hour times with (+1),
     five date styles, h:mm:ss, 'Unlimited', missing marks, 'Not returned', '*' markers) and checks the values equal the
     stored table state; parses printed corrections and note parameters (discount %, grading key, attendance rule,
     UTC offsets, bonus cut-off, fine rate and cap, setup fee, free-shipping threshold, weekend/long-stay rules, ...)
     with regular expressions from the note text;
  3. re-evaluates the claim with separately written semantics. Unknown cells, unlisted rows and the unlisted rows of a
     partial table ("6 of 14 shown") are handled by brute force: the claim is evaluated for every completion from a
     candidate set and the verdict is T/F only if all defined completions agree (else N);
  4. compares the verdict with the gold label of the row.
verify_pairs returns the list of disagreements (empty when everything checks out).
"""
import csv
import datetime as dt
import io
import itertools
import re
from fractions import Fraction as Fr

from tab_core import INF, MON3, MONTHS

T, F, N = "T", "F", "N"
BIG = 10 ** 9
TAILS = ("Claim:", "Statement:", "Claim to check:", "Question:")


# ------------------------------------------------------------------------------------------------ text parsing
def split_state(state):
    b = state.split("\n\n")
    title = b[0].split("\n")
    table = b[1]
    rest = b[2:]
    tail = None
    if rest and rest[-1].startswith(TAILS):
        tail = rest[-1]
        rest = rest[:-1]
    notes = [x for blk in rest for x in blk.split("\n")]
    return title, table, notes, tail


def split_md(line):
    assert line.startswith("| ") and line.endswith(" |"), line
    return [x.strip() for x in line[2:-2].split(" | ")]


def parse_table(txt, fmt):
    lines = txt.split("\n")
    if fmt in ("md", "transposed"):
        rows = [split_md(x) for x in lines if not re.fullmatch(r"\|(---\|)+", x)]
    elif fmt == "pipe":
        assert lines[0] == "Table (first row is the header):"
        rows = [split_md(x) for x in lines[1:]]
    elif fmt == "csv":
        rows = list(csv.reader(io.StringIO(txt)))
    elif fmt == "tsv":
        rows = [x.split("\t") for x in lines]
    elif fmt == "fixed":
        spans = [m.start() for m in re.finditer(r"-+", lines[1])]

        def cut(x):
            return [x[a:(spans[i + 1] if i + 1 < len(spans) else len(x))].strip() for i, a in enumerate(spans)]
        rows = [cut(lines[0])] + [cut(x) for x in lines[2:]]
    elif fmt == "records":
        rows, hdr = [], None
        for x in lines:
            assert x.startswith("- "), x
            kv = [p.split(": ", 1) for p in x[2:].split("; ")]
            if hdr is None:
                hdr = [k for k, _ in kv]
                rows.append(hdr)
            assert [k for k, _ in kv] == hdr
            rows.append([v for _, v in kv])
    else:
        raise ValueError(fmt)
    if fmt == "transposed":
        rows = [list(r) for r in zip(*rows)]
    return rows[0], rows[1:]


def ptime(x):
    m = re.fullmatch(r"(\d{1,2}):(\d{2})(?: (AM|PM|a\.m\.|p\.m\.))?( \(\+1\))?", x)
    assert m, x
    h, mi = int(m.group(1)), int(m.group(2))
    if m.group(3):
        pm = m.group(3) in ("PM", "p.m.")
        h = h % 12 + (12 if pm else 0)
    return h * 60 + mi + (1440 if m.group(4) else 0)


def pdate(x, style):
    if style == "iso":
        return dt.date.fromisoformat(x).toordinal()
    if style == "dmy":
        d, m, y = x.split(" ")
        return dt.date(int(y), MON3.index(m) + 1, int(d)).toordinal()
    if style == "mdy":
        m, d, y = x.replace(",", "").split(" ")
        return dt.date(int(y), MON3.index(m) + 1, int(d)).toordinal()
    a, b, y = x.split("/")
    if style == "dmyn":
        return dt.date(int(y), int(b), int(a)).toordinal()
    return dt.date(int(y), int(a), int(b)).toordinal()


def plong_date(x):
    m = re.fullmatch(r"(\d{1,2}) (\w+) (\d{4})", x)
    return dt.date(int(m.group(3)), MONTHS.index(m.group(2)) + 1, int(m.group(1))).toordinal()


def phms(x):
    h, m, s = x.split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)


def pcell(c, x, style):
    if x == style.get("miss", "—"):
        return None
    for k, v in c.special.items():
        if x == v:
            return k
    if c.kind in ("cat", "bool"):
        return x
    if x == "Unlimited":
        return INF
    if c.kind == "time":
        return ptime(x)
    if c.kind == "date":
        return pdate(x, style["date"])
    if c.kind == "dur":
        return phms(x) if c.durfmt == "hms" else int(x.replace(" min", ""))
    neg = x.startswith("-")
    y = x.lstrip("+-")
    if c.suf and y.endswith(c.suf):
        y = y[:-len(c.suf)]
    if c.pre and y.startswith(c.pre):
        y = y[len(c.pre):]
    y = y.replace(",", "")
    assert re.fullmatch(r"\d+(\.\d+)?", y), (x, y)
    v = Fr(y) * 10 ** c.dec
    assert v.denominator == 1, x
    return -int(v) if neg else int(v)


class VT:
    """The table as re-read from the text."""

    def __init__(self, t, state):
        self.t = t
        self.dom = t.dom
        self.style = t.style
        title, table, notes, tail = split_state(state)
        self.title, self.notes, self.tail = title, notes, tail
        self.note_txt = "\n".join(notes)
        hdr, body = parse_table(table, t.style["fmt"])
        cols = t.cols
        assert hdr[0] == t.ent.header, (hdr, t.ent.header)
        assert len(hdr) == len(cols) + 1
        for h, c in zip(hdr[1:], cols):
            assert h.startswith(c.header), (h, c.header)
        self.cols = {c.key: c for c in cols}
        self.rows, self.vals = [], {}
        for r in body:
            assert len(r) == len(hdr), (r, hdr)
            name = r[0]
            star = name.endswith(" *")
            if star:
                name = name[:-2]
            self.rows.append(name)
            self.vals[name] = {c.key: pcell(c, x, t.style) for c, x in zip(cols, r[1:])}
            self.vals[name]["_star"] = star
        # corrections
        self.corr = {}
        for x in notes:
            m = re.fullmatch(r"Correction: the (.+) for (.+) should read (.+), not (.+) as printed\.", x) or \
                re.fullmatch(r"Erratum: the (.+) for (.+) was misprinted as (.+); the correct figure is (.+)\.", x)
            if not m:
                continue
            noun, e = m.group(1), m.group(2)
            new, old = (m.group(3), m.group(4)) if x.startswith("Correction") else (m.group(4), m.group(3))
            c = [c for c in cols if c.noun == noun]
            assert len(c) == 1 and e in self.vals, (noun, e)
            c = c[0]
            assert pcell(c, old, t.style) == self.vals[e][c.key]
            self.corr[(e, c.key)] = pcell(c, new, t.style)
        # partial tables
        self.total = None
        self.partial = False
        if len(title) > 1:
            sub = title[1]
            m = re.search(r"(\d+) of (?:the )?(\d+) ", sub)
            if m:
                assert int(m.group(1)) == len(self.rows)
                self.total = int(m.group(2))
                self.partial = True
            elif re.search(r"not all|Only some|Selected", sub):
                self.partial = True
        self.fill = {}
        self.extra = []
        self.params()

    # -------------------------------------------------------------- note parameters (from text)
    def params(self):
        n, ti = self.note_txt, " ".join(self.title)
        P = self.P = {}
        if self.dom == "price":
            P["disc"] = int(re.search(r"Members get (\d+)% off the listed price, except on products marked \*", n).group(1))
        if self.dom == "grades":
            key = re.search(r"Grading key: (.+), F = below (\d+)\.", n)
            bands = []
            for part in key.group(1).split(", "):
                L, rng_ = part.split(" = ")
                bands.append((int(rng_.split("-")[0]), L))
            P["bands"] = sorted(bands, reverse=True)
            m = re.search(r"attendance is below (\d+)% receive an I", n)
            P["att"] = int(m.group(1)) if m else None
        if self.dom == "inventory":
            P["exc"] = "unless its status is Discontinued" in n
        if self.dom == "flights":
            m = re.search(r"UTC offsets on the travel date: (.+)\. \(\+1\) = next day\.", n)
            P["off"] = {}
            for part in m.group(1).split(", "):
                city, off = part.rsplit(" ", 1)
                sign = -1 if off[0] == "-" else 1
                h, mi = off[1:].split(":")
                P["off"][city] = sign * (int(h) * 60 + int(mi))
            P["origin"] = re.search(r"departures from (.+) - ", ti).group(1)
        if self.dom == "hr":
            P["cutoff"] = plong_date(re.search(r"started on or before (\d{1,2} \w+ \d{4}) qualify", n).group(1))
            P["asof"] = plong_date(re.search(r"as of (\d{1,2} \w+ \d{4})", ti).group(1))
        if self.dom == "library":
            m = re.search(r"Fines: \$(\d+\.\d\d) for each day after the due date, up to a maximum of \$(\d+\.\d\d) per loan", n)
            P["rate"], P["cap"] = int(Fr(m.group(1)) * 100), int(Fr(m.group(2)) * 100)
            P["asof"] = plong_date(re.search(r"as of (\d{1,2} \w+ \d{4})", ti).group(1))
            assert plong_date(re.search(r"counted up to (\d{1,2} \w+ \d{4})", n).group(1)) == P["asof"]
        if self.dom == "plans":
            m = re.search(r"setup fee of \$(\d+\.\d\d) applies to plans with a 1-month contract", n)
            P["fee"] = int(Fr(m.group(1)) * 100) if m else 0
        if self.dom == "dosing":
            P["conc"] = int(re.search(r"Each 5 mL contains (\d+) mg of (\w+)\.", n).group(1))
            P["ingr"] = re.search(r"Each 5 mL contains (\d+) mg of (\w+)\.", n).group(2)
            P["minw"] = int(Fr(re.search(r"weighing less than ([\d.]+) kg", n).group(1)) * 10)
            P["maxw"] = int(Fr(re.search(r"above ([\d.]+) kg, use the adult product", n).group(1)) * 10)
            P["bands"] = []
            for e in self.rows:
                m = re.fullmatch(r"([\d.]+)-([\d.]+) kg", e)
                P["bands"].append((int(Fr(m.group(1)) * 10), int(Fr(m.group(2)) * 10), e))
        if self.dom == "shipping":
            P["bands"] = []
            for e in self.rows:
                m = re.fullmatch(r"Up to ([\d.]+) kg", e) or re.fullmatch(r"Over ([\d.]+) kg, up to ([\d.]+) kg", e)
                if e.startswith("Up to"):
                    P["bands"].append((0, int(Fr(m.group(1)) * 10), e))
                else:
                    P["bands"].append((int(Fr(m.group(1)) * 10), int(Fr(m.group(2)) * 10), e))
            m = re.search(r"free on orders of \D(\d+) or more sent to Zones? 1(?:-(\d))?\.", n)
            P["free"] = (int(m.group(1)) * 100, int(m.group(2) or 1)) if m else None
        if self.dom == "hotel":
            m = re.search(r"Stays of (\d+) nights or more get (\d+)% off the total room charge", n)
            P["disc"] = (int(m.group(1)), int(m.group(2))) if m else None
            assert "Weekend rates apply to Friday and Saturday nights" in n
        if self.dom == "rental":
            m = re.search(r"Rentals of (\d+) days or more get (\d+)% off the daily rate", n)
            P["disc"] = (int(m.group(1)), int(m.group(2)))
        if self.dom == "standings":
            P["pts_rule"] = "3 points for a win, 1 for a draw" in n

    # -------------------------------------------------------------- values
    def raw(self, e, k):
        if (e, k) in self.fill:
            return self.fill[(e, k)]
        if e not in self.vals:
            return None
        if (e, k) in self.corr:
            return self.corr[(e, k)]
        return self.vals[e].get(k)

    def get(self, e, k):
        if k in self.cols or k.startswith("_"):
            return self.raw(e, k)
        return self.vcol(e, k)

    def vcol(self, e, k):
        g = lambda key: self.raw(e, key)
        d = self.dom
        if d == "retail" and k == "net":
            u, r = g("units"), g("ret")
            return None if None in (u, r) else u - r
        if d == "inventory":
            q, c, r = g("qty"), g("cost"), g("reord")
            if k == "value":
                return None if None in (q, c) else q * c
            if k == "need":
                if None in (q, r):
                    return None
                disc = self.P["exc"] and g("status") == "Discontinued"
                return "yes" if (q <= r and not disc) else "no"
        if d == "price" and k == "mprice":
            p = g("price")
            if p is None:
                return None
            if g("_star"):
                return p
            x = Fr(p * (100 - self.P["disc"]), 100)
            return int(x) if x.denominator == 1 else x
        if d == "standings" and k == "Pts":
            w, dr = g("W"), g("D")
            return 3 * w + dr
        if d == "grades":
            if k == "avg":
                ks = [c for c in self.cols if c != "att"]
                xs = [g(x) for x in ks]
                return None if None in xs else Fr(sum(xs) * 10, len(xs))
            if k.startswith("g_"):
                x = g(k[2:])
                if x is None:
                    return None
                if self.P["att"] is not None:
                    a = g("att")
                    if a is None:
                        return None
                    if a < self.P["att"]:
                        return "I"
                for lo, L in self.P["bands"]:
                    if x >= lo:
                        return L
                return "F"
        if d == "trains":
            def delay(st):
                m = re.fullmatch(r"Delayed (\d+) min", st)
                return int(m.group(1)) if m else (0 if st == "On time" else None)
            if k == "edep":
                return g("dep") + delay(g("status"))
            if k == "earr":
                return g("arr") + delay(g("status"))
            if k == "jt":
                return g("arr") - g("dep")
        if d == "flights" and k == "ft":
            off = self.P["off"]
            return (g("arr") - off[g("to")]) - (g("dep") - off[self.P["origin"]])
        if d == "hr":
            st = g("start")
            if k == "bonus":
                return "yes" if (g("ctype") == "Permanent" and st <= self.P["cutoff"]) else "no"
            if k == "years":
                a, b = dt.date.fromordinal(st), dt.date.fromordinal(self.P["asof"])
                yrs = b.year - a.year
                if (b.month, b.day) < (a.month, a.day):
                    yrs -= 1
                return yrs
        if d == "library":
            due, ret = g("due"), g("ret")
            end = self.P["asof"] if ret == 1 else ret
            late = end - due if end > due else 0
            if k == "late":
                return late
            if k == "fine":
                return min(self.P["cap"], late * self.P["rate"])
        if d == "plans" and k == "tot":
            pr, m = g("price"), g("term")
            return pr * m + (self.P["fee"] if m == 1 else 0)
        if d == "weather":
            if k == "rng":
                h, lo = g("hi"), g("lo")
                return None if None in (h, lo) else h - lo
            if k == "frost":
                lo = g("lo")
                return None if lo is None else ("yes" if lo < 0 else "no")
        if d == "nutrition" and k.endswith("100"):
            x, sv = g(k[:-3]), g("serv")
            return None if None in (x, sv) else Fr(x * 100, sv)
        if d == "appts" and k == "end":
            return g("start") + g("len")
        raise KeyError((d, k))


# ------------------------------------------------------------------------------------------------ brute-force helpers
def rel(x, r, y):
    if r == "eq":
        return x == y
    if r == "gt":
        return x > y
    if r == "lt":
        return x < y
    if r == "ge":
        return x >= y
    if r == "le":
        return x <= y
    raise ValueError(r)


def lo_of(c):
    if c.kind in ("time",):
        return 0
    return 0 if c.nonneg else -BIG


def hi_of(c):
    if c.kind == "time":
        return 1439
    if c.hi_cap is not None:
        return c.hi_cap
    return BIG


def clip(c, vals):
    lo, hi = lo_of(c), hi_of(c)
    return sorted({v for v in vals if v is not None and lo <= v <= hi})


def brute(V, unknown, cands, fn):
    """unknown: list of (entity, key); cands: list of candidate lists; fn(V) -> True/False/None."""
    res = set()
    for combo in itertools.product(*cands):
        V.fill = dict(zip(unknown, combo))
        r = fn(V)
        if r is not None:
            res.add(bool(r))
        if len(res) == 2:
            break
    V.fill = {}
    if res == {True}:
        return T
    if res == {False}:
        return F
    if res == {True, False}:
        return N
    return None


def mem2(V, s):
    ents = list(V.rows)
    f = s.get("filt")
    if f:
        ents = [e for e in ents if V.get(e, f[0]) == f[1]]
    return ents


def unknown_cells(V, s, ents, key):
    out = []
    for e in ents:
        if key in V.cols and V.raw(e, key) is None:
            out.append((e, key))
    return out


def rounded(x):
    if isinstance(x, Fr) and x.denominator != 1:
        y = abs(x)
        n = y.numerator // y.denominator
        if y - n == Fr(1, 2):
            return None
        n = n + 1 if y - n > Fr(1, 2) else n
        return n if x > 0 else -n
    return x


# ------------------------------------------------------------------------------------------------ generic ops
def ev_generic(V, s):
    op = s["op"]
    if op == "val":
        e, k, v = s["e"], s["col"], s["v"]
        if e not in V.vals:
            return N
        c = V.t.col(k)

        def fn(V):
            x = V.get(e, k)
            if x is None:
                return None
            if x == INF:
                return False
            x = rounded(x) if s.get("round") else x
            if x is None or (isinstance(x, Fr) and x.denominator != 1):
                return None
            return x == v
        unk = unknown_cells(V, s, [e], k)
        return brute(V, unk, [clip(c, [v, v + c.step, v - c.step])] * len(unk), fn)
    if op == "thr":
        e, k, v, r = s["e"], s["col"], s["v"], s["rel"]
        c = V.t.col(k)
        cand = clip(c, [v - 1, v, v + 1, lo_of(c), hi_of(c)])
        if e not in V.vals:
            V.vals[e] = {}
            try:
                return brute(V, [(e, k)], [cand], lambda V: rel(V.fill[(e, k)], r, v))
            finally:
                del V.vals[e]
        unk = unknown_cells(V, s, [e], k)
        return brute(V, unk, [cand] * len(unk), lambda V: None if V.get(e, k) is None else rel(V.get(e, k), r, v))
    if op in ("cmp", "diff", "hypo"):
        a, b, k = s["a"], s["b"], s["col"]
        c = V.t.col(k)
        added = [x for x in (a, b) if x not in V.vals]
        for x in added:
            V.vals[x] = {k: None}
        try:
            xa, xb = V.raw(a, k), V.raw(b, k)
            d = s.get("d", 0)
            base = [x for x in (xa, xb) if x is not None]
            cand = []
            for y in base:
                cand += [y - 1, y, y + 1, y + d - 1, y + d, y + d + 1, y - d - 1, y - d, y - d + 1]
            cand += [lo_of(c), hi_of(c), 10, 11]
            cand = clip(c, cand)
            unk = [(x, k) for x in (a, b) if k in V.cols and V.raw(x, k) is None]

            def fn(V):
                ya, yb = V.get(a, k), V.get(b, k)
                if ya is None or yb is None:
                    return None
                if op == "cmp":
                    return rel(ya, s["rel"], yb)
                if op == "hypo":
                    return (ya + d > yb) if s["up"] else (ya - d < yb)
                if s["form"] == "dir":
                    return ya - yb == d
                if s["form"] == "atl":
                    return ya - yb >= d
                return abs(ya - yb) == d
            return brute(V, unk, [cand] * len(unk), fn)
        finally:
            for x in added:
                del V.vals[x]
    if op in ("sup", "count", "quant"):
        k = s["col"]
        c = V.t.col(k)
        ents = mem2(V, s)
        extra = []
        if s.get("scope") == "a":
            assert V.total is not None
            extra = [f"__unseen{i}" for i in range(V.total - len(V.rows))]
        for x in extra:
            V.vals[x] = {k: None}
        try:
            allm = ents + extra
            unk = [(x, k) for x in ents if k in V.cols and V.raw(x, k) is None]
            unk_x = [(x, k) for x in extra]
            if op == "sup":
                xe = V.raw(s["e"], k) if k in V.cols else V.get(s["e"], k)
                base = [xe] if xe is not None else [V.get(x, k) for x in ents if V.get(x, k) is not None]
                cand = []
                for y in base:
                    if y == INF:
                        continue
                    cand += [y - 1, y, y + 1]
                cand = clip(c, cand + [lo_of(c), hi_of(c)])

                def fn(V):
                    vals = [(V.get(x, k), x) for x in allm]
                    if any(v is None for v, _ in vals):
                        return None
                    me = V.get(s["e"], k)
                    others = [v for v, x in vals if x != s["e"]]
                    if s["hi"]:
                        if any(o == me for o in others) and not any(o > me for o in others):
                            return None
                        return all(me > o for o in others)
                    if any(o == me for o in others) and not any(o < me for o in others):
                        return None
                    return all(me < o for o in others)
            else:
                v = s["v"]
                cand = clip(c, [lo_of(c), v - 1, v, v + 1, hi_of(c)])

                def fn(V):
                    vals = [V.get(x, k) for x in allm]
                    if any(y is None for y in vals) or len(allm) < 2:
                        return None
                    sat = sum(rel(y, s["rel"], v) for y in vals)
                    if op == "count":
                        n, q = s["n"], s["q"]
                        return {"exactly": sat == n, "at_least": sat >= n, "more_than": sat > n,
                                "fewer_than": sat < n, "at_most": sat <= n}[q]
                    qt = s["qt"]
                    return {"all": sat == len(vals), "none": sat == 0, "some": sat >= 1, "not_all": sat < len(vals)}[qt]
            # an unlisted row can only be below or above every relevant threshold: two candidates suffice
            ends = clip(c, [lo_of(c), hi_of(c)] + ([s["v"]] if op != "sup" and s.get("rel") == "eq" else []))
            return brute(V, unk + unk_x, [cand] * len(unk) + [ends] * len(unk_x), fn)
        finally:
            for x in extra:
                del V.vals[x]
    if op == "rank":
        k = s["col"]
        vals = [(V.get(x, k), x) for x in V.rows]
        assert all(v is not None for v, _ in vals) and len({v for v, _ in vals}) == len(vals)
        order = [x for _, x in sorted(vals, reverse=s["hi"])]
        pos = order.index(s["e"]) + 1
        if s.get("top"):
            return T if pos <= s["k"] else F
        return T if pos == s["k"] else F
    if op == "share":
        k = s["col"]
        vals = {x: V.get(x, k) for x in V.rows}
        assert all(v is not None for v in vals.values())
        total = sum(vals.values())
        part = vals[s["e"]] if s["form"] == "ent" else sum(vals[x] for x in mem2(V, s))
        return T if rel(Fr(100 * part, total), s["rel"], s["p"]) else F
    if op == "only":
        k = s["col"]
        vals = {x: V.get(x, k) for x in V.rows}
        assert all(v is not None for v in vals.values())
        hits = [x for x, v in vals.items() if rel(v, s["rel"], s["v"])]
        return T if hits == [s["e"]] else F
    if op in ("ratio", "bool"):
        k = s["col"]
        c = V.t.col(k)
        a, b = s["a"], s["b"]
        added = [x for x in (a, b) if x not in V.vals]
        for x in added:
            V.vals[x] = {k: None}
        try:
            unk = [(x, k) for x in (a, b) if k in V.cols and V.raw(x, k) is None]
            if op == "bool":
                v = s["v"]
                cand = clip(c, [lo_of(c), v - 1, v, v + 1, hi_of(c)])

                def fn(V):
                    ya, yb = V.get(a, k), V.get(b, k)
                    if ya is None or yb is None:
                        return None
                    pa, pb = rel(ya, s["rel"], v), rel(yb, s["rel"], v)
                    return {"both": pa and pb, "neither": (not pa) and (not pb), "either": pa or pb,
                            "a_not_b": pa and not pb}[s["form"]]
            else:
                mult, r = {"twice_ge": (2, "ge"), "twice_gt": (2, "gt"), "three_gt": (3, "gt"), "half_lt": (Fr(1, 2), "lt"),
                           "half_ge": (Fr(1, 2), "ge")}[s["form"]]
                known_v = [V.raw(x, k) for x in (a, b) if V.raw(x, k) is not None]
                cand = [lo_of(c), hi_of(c)]
                for y in known_v:
                    for z in (y * mult, Fr(y) / mult):
                        zi = int(z)
                        cand += [zi - 1, zi, zi + 1, zi + 2]
                cand = clip(c, cand)

                def fn(V):
                    ya, yb = V.get(a, k), V.get(b, k)
                    if ya is None or yb is None:
                        return None
                    return rel(ya, r, yb * mult)
            return brute(V, unk, [cand] * len(unk), fn)
        finally:
            for x in added:
                del V.vals[x]
    if op == "sum":
        k = s["col"]
        c = V.t.col(k)
        ents = [s["a"], s["b"]] if s["form"] == "pair" else mem2(V, s)
        known_sum = sum(V.get(x, k) for x in ents if V.get(x, k) is not None)
        unk = [(x, k) for x in ents if V.get(x, k) is None]
        S = s["S"]
        cand = clip(c, [0, S - known_sum - 1, S - known_sum, S - known_sum + 1, lo_of(c), hi_of(c)])
        return brute(V, unk, [cand] * len(unk),
                     lambda V: None if any(V.get(x, k) is None for x in ents) else rel(sum(V.get(x, k) for x in ents), s["rel"], S))
    if op == "avg":
        k = s["col"]
        c = V.t.col(k)
        ents = mem2(V, s)
        vals = [V.get(x, k) for x in ents]
        assert all(v is not None for v in vals)
        dd = 2 if c.kind == "money" else c.dec + 1
        a = Fr(sum(vals), len(vals)) * 10 ** (dd - c.dec)
        if a.denominator != 1:
            assert s["round"]
            a = rounded(a)
            assert a is not None
        return T if a == s["A"] else F
    if op == "argthen":
        k1, k2 = s["c1"], s["c2"]
        vals = [(V.get(x, k1), x) for x in V.rows]
        best = max(v for v, _ in vals) if s["hi"] else min(v for v, _ in vals)
        top = [x for v, x in vals if v == best]
        assert len(top) == 1
        e = top[0]
        x = V.get(e, k2)
        if s["kind"] == "cat":
            return T if x == s["X"] else F
        if s["kind"] == "sup2":
            v2 = [(V.get(y, k2), y) for y in V.rows]
            b2 = max(v for v, _ in v2) if s["hi2"] else min(v for v, _ in v2)
            t2 = [y for v, y in v2 if v == b2]
            assert len(t2) == 1
            return T if t2[0] == e else F
        return T if rel(x, s["rel"], s["v"]) else F
    if op == "catval":
        e, k = s["e"], s["col"]
        if e not in V.vals or V.get(e, k) is None:
            return N
        return T if V.get(e, k) == s["X"] else F
    if op == "catcount":
        vals = [V.get(x, s["col"]) for x in V.rows]
        n, q = s["n"], s["q"]
        sat = vals.count(s["X"])
        return T if {"exactly": sat == n, "at_least": sat >= n, "more_than": sat > n, "fewer_than": sat < n,
                     "at_most": sat <= n}[q] else F
    raise KeyError(op)


# ------------------------------------------------------------------------------------------------ special ops
def ev_special(V, s):
    op = s["op"]
    P = V.P
    if op == "dose":
        w = s["w"]
        band = [e for lo, hi, e in P["bands"] if lo <= w <= hi]
        assert len(band) <= 1
        if s["kind"] == "allowed":
            ok = P["minw"] <= w <= P["maxw"] and bool(band)
            return T if ok else F
        if not band:
            return F
        r = V.vals[band[0]]
        if s["kind"] == "dose":
            return T if r["dose"] == s["v"] else F
        if s["kind"] == "maxday":
            return T if r["dose"] * r["maxd"] == s["v"] else F
        if s["kind"] == "mg":
            return T if Fr(r["dose"], 10) * Fr(P["conc"], 5) == s["v"] else F
        if s["kind"] == "interval":
            return T if s["v"] >= r["gap"] else F
    if op == "ship":
        def rate(w, z):
            b = [e for lo, hi, e in P["bands"] if lo < w <= hi]
            return V.vals[b[0]][f"z{z}"] if b else None
        k = s["kind"]
        if k == "cmp2":
            a, b = rate(s["w"], s["z"]), rate(s["w2"], s["z2"])
            return T if a > b else F
        if k == "rate":
            x = rate(s["w"], s["z"])
        elif k == "sum2":
            x = rate(s["w"], s["z"]) + rate(s["w2"], s["z"])
        else:
            x = rate(s["w"], s["z"])
            if P["free"] and s["ov"] >= P["free"][0] and s["z"] <= P["free"][1]:
                x = 0
        return T if x == s["v"] else F
    if op == "stay":
        def cost(room, day, n):
            r = V.vals[room]
            tot = 0
            for i in range(n):
                wd = WEEK[(day + i) % 7]
                tot += (r["we"] if wd in ("Friday", "Saturday") else r["wk"]) * 100
            if P["disc"] and n >= P["disc"][0]:
                tot = Fr(tot * (100 - P["disc"][1]), 100)
            return tot
        x = cost(s["e"], s["day"], s["n"])
        if s["kind"] == "cmp":
            return T if x < cost(s["b"], s["day"], s["n"]) else F
        return T if x == s["v"] else F
    if op == "rent":
        def cost(e, d):
            r = V.vals[e]["rate"] * d
            if d >= P["disc"][0]:
                r = Fr(r * (100 - P["disc"][1]), 100)
            return r
        if s["kind"] == "cmp":
            return T if cost(s["e"], s["d"]) > cost(s["b"], s["d2"]) else F
        return T if cost(s["e"], s["d"]) == s["v"] else F
    if op == "budget":
        b, a = V.vals[s["e"]]["bud"], V.vals[s["e"]]["act"]
        k = s["kind"]
        if k == "over":
            return T if a > b else F
        if k == "within":
            return T if not a > b else F
        if k == "by":
            return T if (a > b and a - b == s["v"]) else F
        if k == "share":
            return T if rel(Fr(100 * a, b), s["rel"], s["pct"]) else F
        diffs = sorted(((V.vals[e]["act"] - V.vals[e]["bud"], e) for e in V.rows), reverse=True)
        assert diffs[0][0] > 0 and diffs[0][0] != diffs[1][0]
        return T if diffs[0][1] == s["e"] else F
    if op == "grant":
        r, a = V.vals[s["e"]]["req"], V.vals[s["e"]]["awd"]
        if a is None:
            return N
        k = s["kind"]
        if k == "half":
            return T if a * 2 >= r else F
        if k == "full":
            return T if a == r else F
        if k == "none":
            return T if a == 0 else F
        return T if (a > 0 and r - a == s["v"]) else F
    if op == "overlap":
        a, b = V.vals[s["a"]], V.vals[s["b"]]
        return T if max(a["start"], b["start"]) < min(a["start"] + a["len"], b["start"] + b["len"]) else F
    if op == "position":
        def key(e):
            r = V.vals[e]
            pts = r["Pts"] if "Pts" in V.cols else 3 * r["W"] + r["D"]
            return (pts, r["GF"] - r["GA"], r["GF"])
        order = sorted(V.rows, key=key, reverse=True)
        keys = [key(e) for e in order]
        for x in (s["e"], s.get("b", s["e"])):
            assert keys.count(key(x)) == 1
        if s["kind"] == "pos":
            return T if order.index(s["e"]) + 1 == s["k"] else F
        return T if order.index(s["e"]) < order.index(s["b"]) else F
    if op == "series":
        Ps = [c[2:] for c in V.cols]
        vals = {p: V.vals[s["e"]]["p_" + p] for p in Ps}
        k = s["kind"]
        if k == "cmp":
            return T if rel(vals[s["p2"]], s["rel"], vals[s["p1"]]) else F
        if k == "trend":
            seq = [vals[p] for p in Ps[Ps.index(s["p1"]):Ps.index(s["p2"]) + 1]]
            steps = [b - a for a, b in zip(seq, seq[1:])]
            ok = {"up": all(x > 0 for x in steps), "down": all(x < 0 for x in steps),
                  "never_down": all(x >= 0 for x in steps), "never_up": all(x <= 0 for x in steps)}[s["dirn"]]
            return T if ok else F
        if k == "pct":
            a, b = vals[s["p1"]], vals[s["p2"]]
            change = Fr(100 * (b - a), a) * (1 if s["dirn"] == "up" else -1)
            assert not (s["rel"] == "lt" and change <= 0)
            return T if rel(change, s["rel"], s["pct"]) else F
        if k == "peak":
            m = (max if s["hi"] else min)(vals.values())
            ps = [p for p in Ps if vals[p] == m]
            assert len(ps) == 1
            return T if ps[0] == s["p"] else F
        if k == "total":
            seg = Ps[Ps.index(s["p1"]):Ps.index(s["p2"]) + 1]
            return T if sum(vals[p] for p in seg) == s["v"] else F
        if k == "count":
            return T if sum(1 for p in Ps if vals[p] > s["c"]) == s["n"] else F
    raise KeyError(op)


WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def ev_pick(V, s):
    op, k = s["op"], s["col"]
    if op == "pick_val":
        hits = [e for e in V.rows if V.get(e, k) == s["v"]]
        assert len(hits) == 1
        return hits[0]
    pool = s["cands"] if op == "pick_sup" else mem2(V, s)
    vals = [(V.get(e, k), e) for e in pool]
    assert all(v is not None for v, _ in vals)
    best = max(v for v, _ in vals) if s["hi"] else min(v for v, _ in vals)
    top = [e for v, e in vals if v == best]
    assert len(top) == 1
    return top[0]


def evaluate(V, s):
    op = s["op"]
    if op.startswith("pick_"):
        return ev_pick(V, s)
    if op in ("dose", "ship", "stay", "rent", "budget", "grant", "overlap", "position", "series"):
        return ev_special(V, s)
    return ev_generic(V, s)


def flip(v, neg):
    if v in (T, F) and neg % 2:
        return F if v == T else T
    return v


def expected_gold(qid, v, row, s):
    if qid == "pick":
        opts = row["options"]
        cands = s["cands"]
        return opts[cands.index(v)]
    if qid == "supported":
        return "yes" if v == T else "no"
    if qid == "refuted":
        return "yes" if v == F else "no"
    if qid == "enough":
        return "yes" if v in (T, F) else "no"
    if qid == "choice3":
        return {T: "supported", F: "refuted", N: "not enough information"}[v]
    if qid == "answer":
        return "yes" if v == T else "no"
    if qid == "answer_wrong":
        return "yes" if v == F else "no"
    raise ValueError(qid)


def check_row(P, j):
    t, s, row = P["t"], P["specs"][j], P["rows"][j]
    sn = P["snaps"][j]
    V = VT(t, row["state"])
    # the text must reproduce the stored table state exactly
    assert V.rows == sn[1], (V.rows, sn[1])
    for e in V.rows:
        for k, c in V.cols.items():
            assert V.vals[e][k] == sn[0][e].get(k), (e, k, V.vals[e][k], sn[0][e].get(k))
        assert V.vals[e]["_star"] == bool(sn[0][e].get("_star")), e
    assert V.corr == sn[2], (V.corr, sn[2])
    # the claim / question must be visible to the reader
    qid = P["qid"]
    txt = P["texts"][j]
    if qid in ("answer", "answer_wrong"):
        assert V.tail == f"Question: {txt[0]}\nProposed answer: {txt[1]}"
    elif qid == "pick":
        assert V.tail.startswith("Question: " + txt + "\n")
        assert len(V.tail.split("\n")) == len(s["cands"]) + 1
    else:
        assert (V.tail is not None and V.tail.endswith(txt)) or txt.rstrip(".").lower()[1:] in row["instructions"].lower()
    v = evaluate(V, s)
    assert v is not None, "ill-defined"
    if qid not in ("pick", "answer", "answer_wrong"):
        v = flip(v, s.get("neg", 0))
    return expected_gold(qid, v, row, s) == row["gold"], v


def verify_pairs(pairs):
    bad = []
    for P in pairs:
        for j in range(2):
            try:
                ok, v = check_row(P, j)
                if not ok:
                    bad.append((P["rows"][j]["rid"], "label", v, P["rows"][j]["gold"]))
            except Exception as ex:  # noqa: BLE001
                bad.append((P["rows"][j]["rid"], "error", repr(ex)[:300]))
    print(f"independent verifier: {2 * len(pairs)} rows checked, {len(bad)} disagreements")
    return bad

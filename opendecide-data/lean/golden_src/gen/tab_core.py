"""Core helpers for gen_tables (family fact_tables): value formatting, columns, tables, rendering.

Conventions (every module relies on them):
  * numeric values are ints in MINOR units of their column (value * 10**col.dec); money with dec=2 is cents.
    Virtual (computed) columns may return a Fraction in minor units (e.g. an average); it is formattable only when
    integral. math.inf stands for "Unlimited". None is a missing cell ("not reported").
  * clock times are minutes after midnight of the table's day (>= 1440 means the next day, shown with "(+1)").
  * dates are proleptic ordinals (datetime.date.toordinal()).
  * durations: kind "dur" with durfmt "hms" (seconds) or "min" (minutes).
CPU-only, no randomness here (callers pass rng).
"""
import csv
import datetime as dt
import io
import math
from fractions import Fraction as Fr

INF = math.inf
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]
MON3 = [m[:3] for m in MONTHS]
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
NUMW = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"]
ORDW = {1: "first", 2: "second", 3: "third", 4: "fourth", 5: "fifth", 6: "sixth", 7: "seventh", 8: "eighth",
        9: "ninth", 10: "tenth", 11: "eleventh", 12: "twelfth", 13: "thirteenth", 14: "fourteenth", 15: "fifteenth"}


def ordn(n):
    if 10 <= n % 100 <= 20:
        return f"{n}th"
    return f"{n}{ {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th') }".replace(" ", "")


def ordw(n, rng=None):
    if n in ORDW and (rng is None or rng.random() < 0.6):
        return ORDW[n]
    return ordn(n)


def cap(s):
    return s[:1].upper() + s[1:]


def lc(s):
    """Lower-case the first letter unless the first word looks like a name/acronym (second letter upper or digit)."""
    if len(s) > 1 and (s[1].isupper() or s[1].isdigit()):
        return s
    return s[:1].lower() + s[1:]


def art(word):
    w = word.strip().lower()
    if w[:1] in "aeiou" and not w.startswith(("uni", "use", "eu", "one")):
        return "an"
    if w[:1] in "fhlmnrsx" and len(w) == 1:  # letters read as "ef", "aitch", ...: an F, an H
        return "an"
    if w.startswith(("hour", "honest", "8", "11", "18")):
        return "an"
    return "a"


def with_art(word):
    return f"{art(word)} {word}"


# ------------------------------------------------------------------------------------------------ number formats
def fixed(v, dec, commas=True):
    """int (or integral Fraction) in minor units -> '1,234.50'. Returns None if not exactly representable."""
    if isinstance(v, Fr):
        if v.denominator != 1:
            return None
        v = int(v)
    neg = v < 0
    a = -v if neg else v
    if dec:
        w, f = divmod(a, 10 ** dec)
        s = (f"{w:,}" if commas else str(w)) + "." + str(f).zfill(dec)
    else:
        s = f"{a:,}" if commas else str(a)
    return ("-" if neg else "") + s


def trim_dec(s):
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s


def round_half_up(fr, dec_from, dec_to):
    """Fraction in minor units of dec_from -> int in minor units of dec_to (half up, away from zero)."""
    x = Fr(fr) / 10 ** (dec_from - dec_to)
    sign = -1 if x < 0 else 1
    x = abs(x)
    n = x.numerator // x.denominator
    if x - n >= Fr(1, 2):
        n += 1
    return sign * n


def is_half(fr, dec_from, dec_to):
    x = abs(Fr(fr) / 10 ** (dec_from - dec_to))
    return x - (x.numerator // x.denominator) == Fr(1, 2)


# ------------------------------------------------------------------------------------------------ time / date
def fmt_time(m, style="24", nextday=True):
    day, mm = divmod(int(m), 1440)
    h, mi = divmod(mm, 60)
    if style == "24":
        s = f"{h:02d}:{mi:02d}"
    elif style == "12":
        s = f"{h % 12 or 12}:{mi:02d} {'AM' if h < 12 else 'PM'}"
    elif style == "12a":
        s = f"{h % 12 or 12}:{mi:02d} {'a.m.' if h < 12 else 'p.m.'}"
    else:
        raise ValueError(style)
    if day and nextday:
        s += " (+1)"
    return s


def fmt_date(o, style="iso"):
    d = dt.date.fromordinal(int(o))
    if style == "iso":
        return d.isoformat()
    if style == "dmy":
        return f"{d.day} {MON3[d.month - 1]} {d.year}"
    if style == "mdy":
        return f"{MON3[d.month - 1]} {d.day}, {d.year}"
    if style == "dmyn":
        return f"{d.day:02d}/{d.month:02d}/{d.year}"
    if style == "mdyn":
        return f"{d.month:02d}/{d.day:02d}/{d.year}"
    if style == "long_dmy":
        return f"{d.day} {MONTHS[d.month - 1]} {d.year}"
    if style == "long_mdy":
        return f"{MONTHS[d.month - 1]} {d.day}, {d.year}"
    if style == "wlong":
        return f"{WEEKDAYS[d.weekday()]} {d.day} {MONTHS[d.month - 1]} {d.year}"
    raise ValueError(style)


DATE_HDR = {"dmyn": " (DD/MM/YYYY)", "mdyn": " (MM/DD/YYYY)"}


def od(y, m, d):
    return dt.date(y, m, d).toordinal()


def fmt_hms(sec):
    h, r = divmod(int(sec), 3600)
    m, s = divmod(r, 60)
    return f"{h}:{m:02d}:{s:02d}"


def hms_words(sec):
    h, r = divmod(int(sec), 3600)
    m, s = divmod(r, 60)
    parts = []
    if h:
        parts.append(f"{h} hour{'s' if h != 1 else ''}")
    if m:
        parts.append(f"{m} minute{'s' if m != 1 else ''}")
    if s:
        parts.append(f"{s} second{'s' if s != 1 else ''}")
    if not parts:
        return "0 seconds"
    return parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " and " + parts[-1]


def min_words(mins, style="long"):
    h, m = divmod(int(mins), 60)
    if style == "min":
        return f"{mins} minute{'s' if mins != 1 else ''}"
    if style == "hm":
        return f"{h} h {m:02d} min" if h else f"{m} min"
    parts = []
    if h:
        parts.append(f"{h} hour{'s' if h != 1 else ''}")
    if m or not h:
        parts.append(f"{m} minute{'s' if m != 1 else ''}")
    return " ".join(parts) if len(parts) == 1 else f"{parts[0]} {parts[1]}"


# ------------------------------------------------------------------------------------------------ columns
class VP:
    """Verb phrase for a measure that reads naturally with a verb: 'sold 412 units', 'sold more units than'.
    verb: finite form used with singular subjects (past 'sold' or present 'has'); base: 'sell'/'have';
    plural: finite form with plural subjects ('sold'/'have'); obj1/objn: unit after a number (1 / other);
    cobj: object after more/most ('units', 'protein per serving'); count: countable (fewer) or not (less);
    tense: 'past' or 'pres' (for do-support in negation); suffix: appended after the object (' in March')."""

    def __init__(self, verb, base, obj1, objn, cobj=None, count=True, tense="past", plural=None, suffix="", pp=None, unit=None):
        self.pp = pp
        self.unit = unit  # (singular, plural) unit for differences of uncountable measures: '3.2 g more protein per serving'

        self.verb, self.base, self.obj1, self.objn = verb, base, obj1, objn
        self.cobj = cobj or objn
        self.count, self.tense, self.suffix = count, tense, suffix
        self.plural = plural or (verb if tense == "past" else base)

    def aux(self, pl=False):
        return "did" if self.tense == "past" else ("do" if pl else "does")

    def fin(self, pl=False):
        return self.plural if pl else self.verb

    def obj(self, n):
        o = self.obj1 if n == 1 else self.objn
        return (" " + o if o else "")


class Col:
    """A table column (or a virtual column when fn is given: fn(table, entity) -> value, never rendered)."""

    NUMERIC = ("num", "money", "pct", "dur")

    def __init__(self, key, header, kind, noun, **kw):
        self.key, self.header, self.kind, self.noun = key, header, kind, noun
        self.dec = kw.get("dec", 0)
        self.pre = kw.get("pre", "")
        self.suf = kw.get("suf", "")
        self.unit_hdr = kw.get("unit_hdr")        # e.g. "kg" -> header "Weight (kg)" when cells carry no unit
        self.commas = kw.get("commas", True)
        self.trim = kw.get("trim", False)         # drop trailing zeros ('5 mL' not '5.0 mL')
        self.signed = kw.get("signed", False)     # show '+5'
        self.lo, self.hi, self.step = kw.get("lo", 0), kw.get("hi", 100), kw.get("step", 1)
        self.vp = kw.get("vp")
        self.words = kw.get("words", ("higher", "lower", "highest", "lowest", "high", "low"))
        self.above = kw.get("above", ("above", "below"))
        self.nonneg = kw.get("nonneg", True)
        self.sum = kw.get("sum", kind in ("num", "money"))
        self.sum_all = kw.get("sum_all", True)     # a total over all rows is meaningful (not only a pair total)
        self.avg = kw.get("avg", kind in ("num", "money", "pct"))
        self.cats = kw.get("cats")
        self.say = kw.get("say")                  # cat: {value: (affirmative predicate, negative predicate)} or tpl
        self.sayf = kw.get("sayf")                # cat: generic predicate template with {X}
        self.sayfn = kw.get("sayfn")              # cat: negative generic predicate with {X}
        self.filt = kw.get("filt")                # cat: '{pl} in the {X} region' style filter phrase 'in the {X} region'
        self.scale = kw.get("scale", 1)           # money shown in thousands
        self.conv = kw.get("conv", [])            # alternative claim formats
        self.fn = kw.get("fn")
        self.durfmt = kw.get("durfmt", "min")
        self.custom = kw.get("custom", {})        # rel -> [templates]
        self.ops = kw.get("ops")                  # allowed generic ops (None = all that fit the kind)
        self.unl = kw.get("unl", False)
        self.tvp = kw.get("tvp")                  # (verb3sg, base, prep, tense) for time/date: ('departs','depart','at','pres')
        self.domain_lo = kw.get("domain_lo", 0 if kw.get("nonneg", True) else -10 ** 12)
        self.cmpnoun = kw.get("cmpnoun", noun)
        self.deps = kw.get("deps", [])            # virtual: base columns of the same row it is computed from
        self.xdeps = kw.get("xdeps", False)       # virtual: also depends on other rows (e.g. gap to the winner)
        self.hi_cap = kw.get("hi_cap")            # hard upper bound of the value domain (e.g. 100 for percentages)
        self.gen_lo = kw.get("gen_lo", self.lo)
        self.sayp = kw.get("sayp")                # cat: plural predicate '{X}' ('are in the {X} region')
        self.nomiss = kw.get("nomiss", False)     # never blank this column
        self.force_hdr = kw.get("force_hdr", False)  # unit always in the header, cells always bare (scaled money)
        self.special = kw.get("special", {})      # value -> cell text (e.g. 0 -> 'Not returned')
        self.dstyle = kw.get("dstyle", "min")     # claim style for minute durations
        self.units_edge = kw.get("units_edge", False)
        self.mass = kw.get("mass", False)         # uncountable noun: 'has revenue of', not 'has a revenue of'
        self.w = kw.get("w", 1.0)                 # sampling weight when an op picks a column
        self.exc = kw.get("exc", False)           # computed through a rule with an exception stated in the notes

    @property
    def virtual(self):
        return self.fn is not None

    @property
    def numeric(self):
        return self.kind in self.NUMERIC

    @property
    def ordered(self):
        return self.kind in self.NUMERIC or self.kind in ("time", "date")

    def bare(self, style):
        return self.force_hdr or (not style.get("cellunit", True) and bool(self.unit_hdr))

    def hdr(self, style):
        h = self.header
        if self.kind == "date" and style.get("date") in DATE_HDR:
            h += DATE_HDR[style["date"]]
        if self.bare(style) and self.unit_hdr:
            h += f" ({self.unit_hdr})"
        return h

    def cell(self, v, style):
        if v is None:
            return style.get("miss", "—")
        if v in self.special:
            return self.special[v]
        k = self.kind
        if k in ("cat", "bool"):
            return str(v)
        if v == INF:
            return "Unlimited"
        if k == "time":
            return fmt_time(v, style.get("time", "24"))
        if k == "date":
            return fmt_date(v, style.get("date", "iso"))
        if k == "dur":
            return fmt_hms(v) if self.durfmt == "hms" else (str(v) if self.bare(style) else f"{v} min")
        s = fixed(v, self.dec, self.commas)
        if self.trim:
            s = trim_dec(s)
        neg = s.startswith("-")
        if neg:
            s = s[1:]
        if not self.bare(style):
            s = self.pre + s + self.suf
        if neg:
            s = "-" + s
        elif self.signed and v > 0:
            s = "+" + s
        return s

    # ---------------------------------------------------------------- claim-side value strings
    def cv(self, v, alt=None):
        """Value as written in a claim (always with its unit unless the column has a VP whose object carries it).
        alt: an alternative, exactly equal unit form (see conv). Returns None if not exactly representable."""
        k = self.kind
        if v is None:
            return None
        if k in ("cat", "bool"):
            return str(v)
        if v == INF:
            return "unlimited"
        if k == "time":
            return fmt_time(v, alt or "24", nextday=False)
        if k == "date":
            return fmt_date(v, alt or "long_dmy")
        if k == "dur":
            if self.durfmt == "hms":
                return hms_words(v) if alt == "words" else fmt_hms(v)
            return min_words(v, alt or self.dstyle)
        if self.scale != 1 and alt is None:
            alt = "k"
        if alt == "k":  # thousands shown in the table -> full amount in the claim
            base = Fr(v, 10 ** self.dec) * self.scale
            if base.denominator != 1:
                return None
            base = int(base)
            if base >= 1_000_000 and base % 10_000 == 0:
                m = Fr(base, 1_000_000)
                s = trim_dec(fixed(int(m * 100), 2, False))
                return f"{self.pre}{s} million"
            return f"{self.pre}{base:,}"
        if alt == "g":  # kg (dec 1) -> grams
            g = Fr(v, 10 ** self.dec) * 1000
            if g.denominator != 1:
                return None
            return f"{int(g):,} g"
        if alt == "cm":  # mm (dec 1) -> cm
            cm = Fr(v, 10 ** self.dec) / 10
            s = fixed(int(cm * 100), 2, False) if (cm * 100).denominator == 1 else None
            return None if s is None else trim_dec(s) + " cm"
        if alt == "hm":
            return min_words(v, "long")
        s = fixed(v, self.dec, True)
        if s is None:
            return None
        if self.trim:
            s = trim_dec(s)
        neg = s.startswith("-")
        if neg:
            s = s[1:]
        if self.vp is None or not self.vp.obj1:
            s = self.pre + s + self.suf
        if neg:
            s = "-" + s
        elif self.signed and v > 0:
            s = "+" + s
        return s


class Ent:
    def __init__(self, header, sg, pl, ref="{x}"):
        self.header, self.sg, self.pl, self.ref = header, sg, pl, ref

    KEEP = ("French", "Greek", "LED", "USB", "Cheddar")

    def r(self, name):
        keep = name.startswith(self.KEEP) or (len(name) > 1 and (name[1].isupper() or name[1].isdigit()))
        xl = name if keep else name[:1].lower() + name[1:]
        return self.ref.format(x=name, xl=xl)


class Table:
    def __init__(self, dom, title, ent, cols, vcols=()):
        self.dom, self.title, self.ent = dom, title, ent
        self.cols = list(cols)
        self.vcols = list(vcols)
        self.rows = []            # display order of entity names
        self.v = {}               # name -> {colkey: value}
        self.flags = {}           # name -> set (e.g. {'star'})
        self.partial = None       # None | 'count' (caption says N of M) | 'selected' (caption says not all shown)
        self.total = None         # M for 'count'
        self.pool = []            # names not in the table (absent-entity claims)
        self.p = {}               # note parameters
        self.corr = {}            # (name, colkey) -> corrected value (announced in a note)
        self.style = {}
        self.subtitle = None
        self.notes_fn = None      # table -> list of note strings (regenerated after edits)
        self.derive = None        # table -> None: recompute derived base cells after an edit
        self.valid = None         # table -> bool: domain invariants
        self.sort = None          # table -> None: re-sort rows after an edit
        self.special = []         # names of special ops available
        self.editable = None      # list of base col keys that edits may change (None = all non-derived)
        self.derived = set()      # base col keys computed by derive()

    # -------------------------------------------------------------- access
    def colmap(self):
        return {c.key: c for c in self.cols + self.vcols}

    def col(self, key):
        for c in self.cols + self.vcols:
            if c.key == key:
                return c
        raise KeyError(key)

    def raw(self, e, key):
        return self.v[e].get(key)

    def get(self, e, key):
        if key.startswith("_"):
            return self.v[e].get(key)
        c = self.col(key)
        if c.virtual:
            return c.fn(self, e)
        if (e, key) in self.corr:
            return self.corr[(e, key)]
        return self.v[e].get(key)

    def has_missing(self, keys, ents=None):
        ents = self.rows if ents is None else ents
        return any(self.v[e].get(k) is None for e in ents for k in keys if not self.col(k).virtual)

    def ent_cell(self, e):
        return e + (" *" if self.v[e].get("_star") else "")

    def notes(self):
        out = list(self.notes_fn(self)) if self.notes_fn else []
        miss = any(self.v[e].get(c.key) is None for e in self.rows for c in self.cols)
        if miss and self.style.get("miss_note"):
            out.append(self.style["miss_note"])
        for (e, k), nv in sorted(self.corr.items()):
            c = self.col(k)
            out.append(self.style.get("corr_tpl", "Correction: the {noun} for {e} should read {new}, not {old} as printed.")
                       .format(noun=c.noun, e=e, new=c.cell(nv, self.style), old=c.cell(self.v[e][k], self.style)))
        return out

    def apply_derive(self):
        if self.derive:
            self.derive(self)
        if self.sort:
            self.sort(self)

    def is_valid(self):
        for e in self.rows:
            for c in self.cols:
                if c.key in self.derived or c.kind in ("cat", "bool"):
                    continue
                x = self.v[e].get(c.key)
                if x is None or x == INF:
                    continue
                if c.nonneg and x < 0:
                    return False
        return self.valid(self) if self.valid else True


# ------------------------------------------------------------------------------------------------ rendering
FORMATS = ["md", "md", "md", "md", "pipe", "pipe", "csv", "fixed", "fixed", "records", "tsv", "transposed"]


def grid(t):
    hdr = [t.ent.header] + [c.hdr(t.style) for c in t.cols]
    body = [[t.ent_cell(e)] + [c.cell(t.v[e].get(c.key), t.style) for c in t.cols] for e in t.rows]
    return hdr, body


def render_table(t):
    fmt = t.style.get("fmt", "md")
    hdr, body = grid(t)
    if fmt == "md":
        lines = ["| " + " | ".join(hdr) + " |", "|" + "|".join(["---"] * len(hdr)) + "|"]
        lines += ["| " + " | ".join(r) + " |" for r in body]
        return "\n".join(lines)
    if fmt == "pipe":
        return "Table (first row is the header):\n" + "\n".join("| " + " | ".join(r) + " |" for r in [hdr] + body)
    if fmt == "csv":
        buf = io.StringIO()
        w = csv.writer(buf, lineterminator="\n")
        w.writerow(hdr)
        w.writerows(body)
        return buf.getvalue().rstrip("\n")
    if fmt == "tsv":
        return "\n".join("\t".join(r) for r in [hdr] + body)
    if fmt == "fixed":
        rows = [hdr] + body
        wid = [max(len(r[i]) for r in rows) for i in range(len(hdr))]
        out = ["  ".join(r[i].ljust(wid[i]) for i in range(len(hdr))).rstrip() for r in rows]
        out.insert(1, "  ".join("-" * wid[i] for i in range(len(hdr))))
        return "\n".join(out)
    if fmt == "records":
        out = []
        for r in body:
            out.append(f"- {hdr[0]}: {r[0]}; " + "; ".join(f"{h}: {x}" for h, x in zip(hdr[1:], r[1:])))
        return "\n".join(out)
    if fmt == "transposed":
        lines = ["| " + " | ".join([hdr[0]] + [r[0] for r in body]) + " |", "|" + "|".join(["---"] * (len(body) + 1)) + "|"]
        for i in range(1, len(hdr)):
            lines.append("| " + " | ".join([hdr[i]] + [r[i] for r in body]) + " |")
        return "\n".join(lines)
    raise ValueError(fmt)


def render_state(t, tail):
    """Title (+ subtitle), the table, notes (each a self-labelled line), then the claim/question block."""
    sub = t.subtitle.format(n=len(t.rows)) if t.subtitle else None
    head = t.title + ("\n" + sub if sub else "")
    parts = [head, render_table(t)]
    notes = t.notes()
    if notes:
        parts.append("\n".join(notes))
    return "\n\n".join(parts) + "\n\n" + tail

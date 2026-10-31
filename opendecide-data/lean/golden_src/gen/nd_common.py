"""Shared helpers for gen_numeric_dates (policy excerpt + scenario decisions that hinge on numbers, units, dates and
time). CPU-only, deterministic, no third-party text, no model calls.

Conventions
  * facts `f` are plain JSON values (dates as ISO strings, times as minutes after midnight, money as integer cents,
    rates as strings of exact decimals). Every schema reads them back with D()/Fr() so a row can be re-checked from
    meta.orig_label["facts"] alone.
  * f["sty"] is a style seed; all surface choices go through Sty(f).c(key, options), a keyed hash that does not
    depend on call order, so a fact-flip twin keeps every surface choice except the flipped fact.
  * every schema implements two independent computations (preds/preds2, val/val2, catv/catv2); the generator
    asserts they agree for every emitted row and re-checks the written file.
"""
import calendar
import datetime as dt
import hashlib
import math
import re
from decimal import Decimal, ROUND_DOWN, ROUND_HALF_EVEN, ROUND_HALF_UP, ROUND_UP, ROUND_CEILING, ROUND_FLOOR
from fractions import Fraction as Fr

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]
MON3 = [m[:3] for m in MONTHS]
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
NUMW = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"]

# name, subject pronoun, object pronoun, possessive
PEOPLE = [
    ("Amara", "she", "her", "her"), ("Bilal", "he", "him", "his"), ("Chen Wei", "he", "him", "his"),
    ("Daniela", "she", "her", "her"), ("Emeka", "he", "him", "his"), ("Farah", "she", "her", "her"),
    ("Gustavo", "he", "him", "his"), ("Hana", "she", "her", "her"), ("Ibrahim", "he", "him", "his"),
    ("Jolene", "she", "her", "her"), ("Kenji", "he", "him", "his"), ("Leilani", "she", "her", "her"),
    ("Mateo", "he", "him", "his"), ("Nadia", "she", "her", "her"), ("Oluwaseun", "he", "him", "his"),
    ("Priya", "she", "her", "her"), ("Quentin", "he", "him", "his"), ("Rosa", "she", "her", "her"),
    ("Sipho", "he", "him", "his"), ("Tamar", "she", "her", "her"), ("Umar", "he", "him", "his"),
    ("Valentina", "she", "her", "her"), ("Wojtek", "he", "him", "his"), ("Ximena", "she", "her", "her"),
    ("Yusuf", "he", "him", "his"), ("Zanele", "she", "her", "her"), ("Aarav", "he", "him", "his"),
    ("Brigid", "she", "her", "her"), ("Carlos", "he", "him", "his"), ("Dilnoza", "she", "her", "her"),
    ("Eero", "he", "him", "his"), ("Fatima", "she", "her", "her"), ("Giorgos", "he", "him", "his"),
    ("Halima", "she", "her", "her"), ("Isaac", "he", "him", "his"), ("Jia Hui", "she", "her", "her"),
    ("Kwame", "he", "him", "his"), ("Lucia", "she", "her", "her"), ("Marcus", "he", "him", "his"),
    ("Noor", "she", "her", "her"), ("Oskar", "he", "him", "his"), ("Paloma", "she", "her", "her"),
    ("Rahul", "he", "him", "his"), ("Svetlana", "she", "her", "her"), ("Tomasz", "he", "him", "his"),
    ("Uzma", "she", "her", "her"), ("Viktor", "he", "him", "his"), ("Wren", "they", "them", "their"),
    ("Yara", "she", "her", "her"), ("Zeke", "he", "him", "his"), ("Alex", "they", "them", "their"),
    ("Sam", "they", "them", "their"), ("Jordan", "they", "them", "their"), ("Riley", "they", "them", "their"),
    ("Aiyana", "she", "her", "her"), ("Bongani", "he", "him", "his"), ("Céline", "she", "her", "her"),
    ("Dmitri", "he", "him", "his"), ("Esperanza", "she", "her", "her"), ("Finn", "he", "him", "his"),
    ("Grace", "she", "her", "her"), ("Hamza", "he", "him", "his"), ("Ingrid", "she", "her", "her"),
    ("Javier", "he", "him", "his"), ("Keiko", "she", "her", "her"), ("Liam", "he", "him", "his"),
    ("Mei", "she", "her", "her"), ("Nikolai", "he", "him", "his"), ("Olga", "she", "her", "her"),
    ("Pedro", "he", "him", "his"), ("Rania", "she", "her", "her"), ("Stefan", "he", "him", "his"),
    ("Thandiwe", "she", "her", "her"), ("Tariq", "he", "him", "his"), ("Ulla", "she", "her", "her"),
    ("Vikram", "he", "him", "his"), ("Winifred", "she", "her", "her"), ("Xavier", "he", "him", "his"),
    ("Yetunde", "she", "her", "her"), ("Zoltan", "he", "him", "his"), ("Anika", "she", "her", "her"),
    ("Benedikt", "he", "him", "his"), ("Chiara", "she", "her", "her"), ("Deshawn", "he", "him", "his"),
    ("Elif", "she", "her", "her"), ("Felipe", "he", "him", "his"), ("Gulnara", "she", "her", "her"),
    ("Hiroshi", "he", "him", "his"), ("Imani", "she", "her", "her"), ("Jakob", "he", "him", "his"),
    ("Maya", "she", "her", "her"), ("Tobias", "he", "him", "his"), ("Ayesha", "she", "her", "her"),
    ("Diego", "he", "him", "his"), ("Nomvula", "she", "her", "her"), ("Arjun", "he", "him", "his"),
    ("Freya", "she", "her", "her"), ("Kofi", "he", "him", "his"), ("Linh", "she", "her", "her"),
    ("Mohammed", "he", "him", "his"), ("Sofia", "she", "her", "her"), ("Ravi", "he", "him", "his"),
]
PLACES = ["Northfield", "Riverbend", "Lakeside", "Harborview", "Pinecrest", "Maple Grove", "Stonebridge",
          "Cedar Valley", "Westbrook", "Summit Ridge", "Oakmont", "Brookhaven", "Fairview", "Glenwood", "Ashford",
          "Kingsley", "Millbrook", "Redwood", "Silver Lake", "Thornbury", "Elmstead", "Bayside", "Clearwater",
          "Hollins", "Juniper Hill", "Larchmont", "Meadowvale", "Norwood", "Parkside", "Quarry Bay", "Rosedale",
          "Sherwood", "Tidewater", "Upland", "Valemont", "Willowdale", "Yarrow", "Beacon Hill", "Copperfield",
          "Dunmore", "Evergreen", "Foxhall", "Granger", "Highcliff", "Ivybridge", "Kestrel Point", "Lowell Park"]

NEG_RE = re.compile(r"\b(not|no|never|none|nobody|nothing|neither|nor|without|cannot|ineligible|unable|fail|fails|"
                    r"failed|refuse|refused|denied|disqualified|invalid|unless)\b|n't\b", re.I)


# --------------------------------------------------------------------------------------------------- hashing / style
def hk(*a):
    return int(hashlib.md5(":".join(map(str, a)).encode()).hexdigest()[:12], 16)


class Sty:
    """Order-independent keyed style choices from f['sty']."""

    def __init__(self, f):
        self.seed = f["sty"]

    def i(self, key, n):
        return hk(self.seed, key) % n

    def c(self, key, seq):
        return seq[self.i(key, len(seq))]

    def p(self, key, prob):
        return (hk(self.seed, key, "p") % 100000) / 100000 < prob


def person(rng, exclude=()):
    while True:
        p = rng.choice(PEOPLE)
        if p[0] not in exclude:
            return list(p)


# --------------------------------------------------------------------------------------------------- dates / times
def D(s):
    return dt.date.fromisoformat(s)


def iso(d):
    return d.isoformat()


def add_days(s, n):
    return iso(D(s) + dt.timedelta(days=n))


def isleap(y):
    return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)


def fd(d, st=0, wd=False):
    """Date text. st: 0 'March 3, 2026'; 1 '3 March 2026'; 2 '2026-03-03'; 3 'Mar 3, 2026'; 4 '3 Mar 2026'."""
    if isinstance(d, str):
        d = D(d)
    w = WEEKDAYS[d.weekday()]
    if st == 0:
        s = f"{MONTHS[d.month - 1]} {d.day}, {d.year}"
        return f"{w}, {s}" if wd else s
    if st == 1:
        s = f"{d.day} {MONTHS[d.month - 1]} {d.year}"
        return f"{w} {s}" if wd else s
    if st == 2:
        return f"{d.isoformat()} ({w})" if wd else d.isoformat()
    if st == 3:
        s = f"{MON3[d.month - 1]} {d.day}, {d.year}"
        return f"{w[:3]}, {s}" if wd else s
    if st == 4:
        s = f"{d.day} {MON3[d.month - 1]} {d.year}"
        return f"{w[:3]} {s}" if wd else s
    raise ValueError(st)


def fdm(d, st=0, wd=False):
    """Date without the year: 'March 3' / '3 March' (weekday optional)."""
    if isinstance(d, str):
        d = D(d)
    w = WEEKDAYS[d.weekday()]
    s = f"{MONTHS[d.month - 1]} {d.day}" if st in (0, 2, 3) else f"{d.day} {MONTHS[d.month - 1]}"
    return (f"{w}, {s}" if st in (0, 2, 3) else f"{w} {s}") if wd else s


def ft(m, st=0):
    """Clock time from minutes after midnight. st: 0 '4:30 p.m.'; 1 '16:30'; 2 '4:30 PM'."""
    m = int(m) % 1440
    h, mi = divmod(m, 60)
    if st == 1:
        return f"{h:02d}:{mi:02d}"
    suf = ("a.m." if h < 12 else "p.m.") if st == 0 else ("AM" if h < 12 else "PM")
    s = f"{h % 12 or 12}:{mi:02d} {suf}"
    if m == 720:
        s += " (noon)"
    elif m == 0:
        s += " (midnight)"
    return s


def dur_words(mins):
    h, m = divmod(int(mins), 60)
    parts = []
    if h:
        parts.append(f"{h} hour{'s' if h != 1 else ''}")
    if m or not h:
        parts.append(f"{m} minute{'s' if m != 1 else ''}")
    return " ".join(parts) if len(parts) == 1 else f"{parts[0]} {parts[1]}"


def dur_hm(mins):
    h, m = divmod(int(mins), 60)
    return f"{h} h {m:02d} min"


def add_months(s, n, clamp=True):
    """Same day-of-month n months later; if that day does not exist, the last day of that month."""
    d = D(s)
    y, m = divmod(d.month - 1 + n, 12)
    y += d.year
    m += 1
    last = calendar.monthrange(y, m)[1]
    return iso(dt.date(y, m, min(d.day, last)))


def add_months2(s, n):
    """Independent implementation (month stepping one at a time)."""
    d = D(s)
    y, m, day = d.year, d.month, d.day
    for _ in range(n):
        m += 1
        if m == 13:
            m, y = 1, y + 1
    mdays = [31, 29 if isleap(y) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1]
    return iso(dt.date(y, m, day if day <= mdays else mdays))


def month_end(y, m):
    return iso(dt.date(y, m, calendar.monthrange(y, m)[1]))


# --------------------------------------------------------------------------------------------------- numbers / money
def money(cents, cur="$", whole=False):
    cents = int(cents)
    neg = cents < 0
    a = -cents if neg else cents
    s = f"{a // 100:,}" if (whole and a % 100 == 0) else f"{a // 100:,}.{a % 100:02d}"
    sp = " " if cur[-1:].isalpha() else ""
    return ("-" if neg else "") + f"{cur}{sp}{s}"


def fdec(x, dp, commas=True):
    """Exact Fraction/int -> fixed decimal string with dp places; asserts exact representability."""
    x = Fr(x)
    q = x * 10 ** dp
    assert q.denominator == 1, (x, dp)
    q = int(q)
    neg = q < 0
    q = abs(q)
    w, r = divmod(q, 10 ** dp)
    s = (f"{w:,}" if commas else str(w)) + (("." + str(r).zfill(dp)) if dp else "")
    return ("-" if neg else "") + s


def ftrim(x, maxdp=6, commas=True):
    """Exact Fraction -> shortest decimal string (asserts exact within maxdp places)."""
    x = Fr(x)
    for dp in range(0, maxdp + 1):
        if (x * 10 ** dp).denominator == 1:
            return fdec(x, dp, commas)
    raise AssertionError(("not a terminating decimal", x))


def rnd(x, dp, mode):
    """Round an exact Fraction to dp decimal places. modes: half_up (away from 0 at .5), half_even, down (toward 0),
    up (away from 0), floor, ceil. Returns a Fraction."""
    x = Fr(x)
    s = x * 10 ** dp
    fl = s.numerator // s.denominator
    frac = s - fl
    if mode == "floor":
        n = fl
    elif mode == "ceil":
        n = fl if frac == 0 else fl + 1
    elif mode == "down":
        n = fl if s >= 0 else (fl if frac == 0 else fl + 1)
    elif mode == "up":
        n = (fl if frac == 0 else fl + 1) if s >= 0 else fl
    elif mode == "half_up":
        if s >= 0:
            n = fl + 1 if frac >= Fr(1, 2) else fl
        else:
            n = fl + 1 if frac > Fr(1, 2) else fl
    elif mode == "half_even":
        if frac > Fr(1, 2):
            n = fl + 1
        elif frac < Fr(1, 2):
            n = fl
        else:
            n = fl if fl % 2 == 0 else fl + 1
    else:
        raise ValueError(mode)
    return Fr(n, 10 ** dp)


DEC_MODE = {"half_up": ROUND_HALF_UP, "half_even": ROUND_HALF_EVEN, "down": ROUND_DOWN, "up": ROUND_UP,
            "floor": ROUND_FLOOR, "ceil": ROUND_CEILING}


def drnd(x, dp, mode):
    """Independent rounding with decimal.Decimal (x: Decimal)."""
    q = Decimal(1).scaleb(-dp)
    return x.quantize(q, rounding=DEC_MODE[mode])


def dec(s):
    return Decimal(str(s))


def fr(s):
    return Fr(str(s))


def pct_s(x, maxdp=4):
    return ftrim(Fr(x), maxdp) + "%"


def num_w(n, sty=None, key="n"):
    if sty is not None and 0 <= n <= 12 and sty.p(key, 0.4):
        return NUMW[n]
    return str(n)


def plural(n, one, many=None):
    return one if n == 1 else (many or one + "s")


def cap(s):
    return s[:1].upper() + s[1:]


def ordn(n):
    if 10 <= n % 100 <= 20:
        return f"{n}th"
    return f"{n}" + {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")


IRREG_V = {"is": "are", "has": "have", "was": "were", "does": "do"}


def V(who, v3):
    """Verb agreeing with a person's subject pronoun: V(who, 'needs') -> 'need' when the pronoun is 'they'."""
    if who[1] != "they":
        return v3
    if v3 in IRREG_V:
        return IRREG_V[v3]
    if v3.endswith("es") and v3[:-2].endswith(("s", "sh", "ch", "x", "z", "o")):
        return v3[:-2]
    return v3[:-1] if v3.endswith("s") else v3


def art(w):
    return "an" if w[:1].lower() in "aeiou" or w.startswith(("8", "11", "18")) else "a"


# --------------------------------------------------------------------------------------------------- schema base
class Schema:
    """One decision type. Subclasses set name/quota and implement the hooks below.

    preds(f)  -> {pred_name: True/False/None}   primary computation (None = not decidable from the stated facts)
    preds2(f) -> same, computed independently      (asserted equal)
    alts(f)   -> {fact_key: [candidate values]}    single-fact changes tried when building a fact-flip twin
    render(f) -> state text (policy excerpt + scenario)
    pq(f, p)  -> {"pos": [questions], "neg": [questions], "cpos": clause, "cneg": clause,
                  "speakers": [(intro, short)]}
    edges(f, p) -> list of edge tags implied by the facts
    optional: cat (options) + catv/catv2/cat_q ; letter=True + val/val2/fmtv/wrongs/letter_q ;
              hide_keys {pred: [keys]} (a key set to None makes the pred undecidable; render must say so)
    """
    name = "base"
    quota = 300
    cat = None
    cat_defs = None
    letter = False
    hide_keys = {}
    preds_list = ("ok",)
    yn_modes = {"pos": 0.42, "neg": 0.25, "claim": 0.18, "est": 0.15}
    choice_share = 0.25

    def valid(self, f):
        return True

    def edges(self, f, p):
        return []

    def reveal_vals(self, f, key):
        return self.alts(f).get(key, [])

    def can_hide(self, p):
        return bool(self.hide_keys.get(p))

    def hide(self, f, p, rng):
        """Copy of f with one decisive fact removed (the text then says it is unknown)."""
        g = dict(f)
        g[rng.choice(self.hide_keys[p])] = None
        return g

    # helpers
    def S(self, f):
        return Sty(f)

    def flip(self, f, rng, want, keys=None):
        """Change exactly one fact (from alts) so that want(g) holds; None if impossible."""
        cands = [(k, x) for k, xs in self.alts(f).items() for x in xs
                 if (keys is None or k in keys) and x != f.get(k)]
        rng.shuffle(cands)
        for k, x in cands:
            g = dict(f)
            g[k] = x
            if not self.valid(g):
                continue
            try:
                if want(g):
                    return g
            except (ValueError, OverflowError):
                continue
        return None

"""T21 / T22 / T34 / T3 value formats: render and parse (shared value layer; exact arithmetic, no floats).

Numbers are Fractions. Dates are day ordinals (datetime.date.toordinal()). Date-times are epoch seconds (UTC) shown in
one fixed-offset zone per item (minutes east of UTC).
"""
from __future__ import annotations

import datetime as dt
import re
from decimal import ROUND_HALF_EVEN, ROUND_HALF_UP, Decimal, getcontext
from fractions import Fraction

from f9lex import MON3, MONTHS

getcontext().prec = 60

NUM_FORMATS = {  # id -> (thousands separator, decimal mark, card sentence)
    "plain": ("", ".", "No mark splits thousands, and '.' marks decimals. A value below zero starts with a minus sign."),
    "comma": (",", ".", "',' splits thousands, and '.' marks decimals. A value below zero starts with a minus sign."),
    "euro": (".", ",", "'.' splits thousands, and ',' marks decimals. A value below zero starts with a minus sign."),
}
DATE_FORMATS = {  # id -> card pattern
    "iso": "YYYY-MM-DD", "slash": "YYYY/MM/DD", "dmy_dot": "DD.MM.YYYY", "dmy_abbr": "D MMM YYYY",
    "dmy_long": "D MMMM YYYY",
}
TIME_FORMATS = {"hm": "HH:MM", "hms": "HH:MM:SS"}
DEFAULTS = {"nf": "plain", "df": "iso", "tf": "hm", "null": "unknown", "bool": "tf", "csv": ","}


class ValueError_(ValueError):
    pass


# ------------------------------------------------------------------------------------------------ numbers
def to_frac(x) -> Fraction:
    if isinstance(x, Fraction):
        return x
    if isinstance(x, int):
        return Fraction(x)
    if isinstance(x, str):
        return Fraction(Decimal(x))
    if isinstance(x, Decimal):
        return Fraction(x)
    raise TypeError(type(x))


def round_half_up(q: Fraction, dp: int) -> Fraction:
    """Display rounding (T22: halves away from zero), exact."""
    d = Decimal(q.numerator) / Decimal(q.denominator)
    r = d.quantize(Decimal(1).scaleb(-dp), rounding=ROUND_HALF_UP)
    return Fraction(r)


def round_half_even(q: Fraction, dp: int) -> Fraction:
    d = Decimal(q.numerator) / Decimal(q.denominator)
    r = d.quantize(Decimal(1).scaleb(-dp), rounding=ROUND_HALF_EVEN)
    return Fraction(r)


def fmt_num(q, dp: int, nf: str = "plain") -> str:
    """Exact rendering with dp decimals (q must already be representable at dp)."""
    q = to_frac(q)
    scaled = q * (10 ** dp)
    if scaled.denominator != 1:
        raise ValueError_("value not representable at dp")
    n = scaled.numerator
    neg = n < 0
    n = abs(n)
    ip, fp = divmod(n, 10 ** dp) if dp else (n, 0)
    thou, dec, _ = NUM_FORMATS[nf]
    s = str(ip)
    if thou and len(s) > 3:
        parts = []
        while len(s) > 3:
            parts.insert(0, s[-3:])
            s = s[:-3]
        parts.insert(0, s)
        s = thou.join(parts)
    if dp:
        s += dec + str(fp).zfill(dp)
    return ("-" if neg else "") + s


def num_regex(nf: str) -> str:
    thou, dec, _ = NUM_FORMATS[nf]
    t = re.escape(thou)
    d = re.escape(dec)
    if thou:
        ip = rf"(?:\d{{1,3}}(?:{t}\d{{3}})+|\d+)"
    else:
        ip = r"\d+"
    return rf"-?{ip}(?:{d}\d+)?"


def parse_num(s: str, nf: str = "plain") -> Fraction:
    s = s.strip()
    if not re.fullmatch(num_regex(nf), s):
        raise ValueError_(f"bad number for {nf}")
    thou, dec, _ = NUM_FORMATS[nf]
    if thou:
        # a thousands group must be exactly 3 digits; plain digit runs are also allowed (values < 1000)
        s = s.replace(thou, "")
    if dec != ".":
        s = s.replace(dec, ".")
    return Fraction(Decimal(s))


def dec_str(q) -> str:
    """Exact decimal string of a Fraction with a finite decimal expansion (canonical literal form)."""
    q = to_frac(q)
    d = dp_of(q)
    return fmt_num(q, d, "plain")


def dp_of(q: Fraction) -> int:
    """Smallest dp at which q is exact (for literals)."""
    for d in range(0, 13):
        if (q * 10 ** d).denominator == 1:
            return d
    raise ValueError_("too many decimals")


# ------------------------------------------------------------------------------------------------ dates
def fmt_date(o: int, df: str = "iso") -> str:
    d = dt.date.fromordinal(o)
    if df == "iso":
        return d.isoformat()
    if df == "slash":
        return f"{d.year:04d}/{d.month:02d}/{d.day:02d}"
    if df == "dmy_dot":
        return f"{d.day:02d}.{d.month:02d}.{d.year:04d}"
    if df == "dmy_abbr":
        return f"{d.day} {MON3[d.month - 1]} {d.year}"
    if df == "dmy_long":
        return f"{d.day} {MONTHS[d.month - 1]} {d.year}"
    raise KeyError(df)


DATE_RE = {
    "iso": r"\d{4}-\d{2}-\d{2}", "slash": r"\d{4}/\d{2}/\d{2}", "dmy_dot": r"\d{2}\.\d{2}\.\d{4}",
    "dmy_abbr": r"\d{1,2} (?:" + "|".join(MON3) + r") \d{4}",
    "dmy_long": r"\d{1,2} (?:" + "|".join(MONTHS) + r") \d{4}",
}


def parse_date(s: str, df: str = "iso") -> int:
    s = s.strip()
    if not re.fullmatch(DATE_RE[df], s):
        raise ValueError_("bad date")
    if df == "iso":
        y, m, d = s.split("-")
    elif df == "slash":
        y, m, d = s.split("/")
    elif df == "dmy_dot":
        d, m, y = s.split(".")
    else:
        d, mn, y = s.split(" ")
        names = MON3 if df == "dmy_abbr" else MONTHS
        m = names.index(mn) + 1
    return dt.date(int(y), int(m), int(d)).toordinal()


def month_bounds(year: int, month: int) -> tuple[int, int]:
    a = dt.date(year, month, 1).toordinal()
    b = (dt.date(year + (month == 12), (month % 12) + 1, 1).toordinal()) - 1
    return a, b


# ------------------------------------------------------------------------------------------------ date-times
EPOCH0 = dt.datetime(1970, 1, 1)


def local_parts(epoch: int, off_min: int):
    t = EPOCH0 + dt.timedelta(seconds=epoch + off_min * 60)
    return t


def local_day(epoch: int, off_min: int) -> int:
    return local_parts(epoch, off_min).date().toordinal()


def fmt_time(epoch: int, off_min: int, tf: str = "hm") -> str:
    t = local_parts(epoch, off_min)
    return f"{t.hour:02d}:{t.minute:02d}" + (f":{t.second:02d}" if tf == "hms" else "")


def fmt_dt(epoch: int, off_min: int, df: str = "iso", tf: str = "hm") -> str:
    t = local_parts(epoch, off_min)
    return fmt_date(t.date().toordinal(), df) + " " + fmt_time(epoch, off_min, tf)


TIME_RE = {"hm": r"\d{2}:\d{2}", "hms": r"\d{2}:\d{2}:\d{2}"}


def dt_regex(df: str, tf: str) -> str:
    return DATE_RE[df] + " " + TIME_RE[tf]


def parse_time_of_day(s: str, tf: str) -> int:
    if not re.fullmatch(TIME_RE[tf], s):
        raise ValueError_("bad time")
    p = [int(x) for x in s.split(":")]
    if p[0] > 23 or p[1] > 59 or (len(p) > 2 and p[2] > 59):
        raise ValueError_("bad time")
    return p[0] * 3600 + p[1] * 60 + (p[2] if len(p) > 2 else 0)


def parse_dt(s: str, off_min: int, df: str = "iso", tf: str = "hm") -> int:
    s = s.strip()
    m = re.fullmatch(f"({DATE_RE[df]}) ({TIME_RE[tf]})", s)
    if not m:
        raise ValueError_("bad datetime")
    day = parse_date(m.group(1), df)
    sec = parse_time_of_day(m.group(2), tf)
    local = (dt.datetime.fromordinal(day) - EPOCH0).total_seconds() + sec
    return int(local) - off_min * 60


def epoch_of_local(day: int, sec: int, off_min: int) -> int:
    return int((dt.datetime.fromordinal(day) - EPOCH0).total_seconds()) + sec - off_min * 60


def zone_str(off_min: int) -> str:
    sign = "+" if off_min >= 0 else "-"
    a = abs(off_min)
    return f"UTC{sign}{a // 60:02d}:{a % 60:02d}"


def parse_zone(s: str) -> int:
    m = re.fullmatch(r"UTC([+-])(\d{2}):(\d{2})", s)
    if not m:
        raise ValueError_("bad zone")
    v = int(m.group(2)) * 60 + int(m.group(3))
    return v if m.group(1) == "+" else -v


# ------------------------------------------------------------------------------------------------ T21 card sentences
def t21_sentences(nf: str, df: str, tf: str | None, off_min: int | None, csv_delim: str | None) -> list[str]:
    out = [f"Dates are written {DATE_FORMATS[df]}.", NUM_FORMATS[nf][2]]
    if tf is not None:
        out.append(f"Times are written {TIME_FORMATS[tf]}, 24-hour, in {zone_str(off_min)}.")
    if csv_delim is not None:
        name = {",": "commas", ";": "semicolons", "\t": "tabs"}[csv_delim]
        out.append(f"In CSV blocks, fields are separated by {name}.")
    return out

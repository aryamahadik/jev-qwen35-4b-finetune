"""c2_kit/slots.py: typed slots, the only way a C2 fact value reaches text (C2_DATA_SPEC 3.0 Mode T, 6.2 item 1).

A slot is (kind, canonical value, params). The program draws every value; a skin or a program template only says
where it goes. Each kind has a closed set of forms; every form renders and parses back to the same value
(tests/test_slots.py round-trips them), and `regex()` gives each form's pattern for template parsing and lints.

  kind      value                         forms (example)
  date      datetime.date                 iso 2026-03-05 | dmy 5 March 2026 | mdy March 5, 2026 | dmy_abbr 5 Mar 2026
                                          | wdmy Thursday, 5 March 2026 | wmdy Thursday, March 5, 2026.
                                          No numeric d/m/y form: 03/05/2026 reads two ways.
  datetime  aware datetime, fixed offset  iso 2026-03-05T14:05:00+02:00 | iso_z 2026-03-05T12:05:00Z (offset 0 only)
                                          | text 5 March 2026, 14:05 (UTC+02:00) (seconds 0 only)
                                          | log 2026-03-05 14:05:00 +0200.
                                          Offsets are whole quarter hours in [-12:00, +14:00]: never a zone name or
                                          DST (T17 veto). The canonical value keeps the offset (isoformat), so
                                          14:05+02:00 and 12:05Z are different values although the same instant.
  cents     int (never float or bool)     symbol $1,234.50 | code 1,234.50 USD | plain 1,234.50 | nocomma 1234.50
                                          | int_cents 123450 | whole $1,200 (only when cents % 100 == 0).
  count     int >= 0, optional unit       digits 1,234 | plain 1234 | words three (0..20 only) | adj 3-day
                                          | adj_words three-day. With a unit the value form carries it
                                          ("1 day", "3 days"); adj forms use the singular.
  category  key of a closed set           s0, s1, ... = the key's surfaces in order; surfaces are unique in the set.
  id        str                           raw. Starts and ends with a letter or digit; letters, digits and - _ . : / #
                                          inside; no spaces.
  glob      str                           raw | code (`ns.*`, in backticks).
  url       str                           full https://shop.example/a?x=1. Reserved hosts only: *.example, *.test,
                                          *.invalid, example.com / .net / .org (RFC 2606/6761). A bare path is not a
                                          url form (it would lose the host): write it as a glob slot.
  name      str                           raw. No negation cue (negcount k_all = 0), no digit, no brace.
  clause    (sem, form_id, template)      raw. A lexicon clause (lexicon.LexiconRegistry.clause); its template holds
                                          placeholders bound to other slots of the spec and is filled by the skin
                                          renderer, so each inner value keeps its own slot (and its own G-TW span).

Values never contain "{" or "}" (so a filled text has no placeholder residue) or a line break.

  from c2_kit import slots as S
  s = S.cents_slot(123450); S.render(s, "code") -> "1,234.50 USD"; S.parse("cents", "1,234.50 USD", s.params) -> 123450
"""
from __future__ import annotations

import datetime as dt
import re
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlsplit

from . import paths  # noqa: F401  (puts c_src/common on sys.path)
import negcount  # noqa: E402  (c_src/common/negcount.py, XF02; orchestrator-owned, read-only)

KINDS = ("date", "datetime", "cents", "count", "category", "id", "glob", "url", "name", "clause")

MONTHS = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December")
MONTHS_ABBR = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
NUM_WORDS = ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
             "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty")

FORMS = {
    "date": ("iso", "dmy", "mdy", "dmy_abbr", "wdmy", "wmdy"),
    "datetime": ("iso", "iso_z", "text", "log"),
    "cents": ("symbol", "code", "plain", "nocomma", "int_cents", "whole"),
    "count": ("digits", "plain", "words", "adj", "adj_words"),
    "category": None,          # s0, s1, ... per slot
    "id": ("raw",),
    "glob": ("raw", "code"),
    "url": ("full",),
    "name": ("raw",),
    "clause": ("raw",),
}
# Forms the program may pick freely (label-blind, plugin.choose_forms). The others read right only in a context a
# template states, so a template must pin them ({AMT:int_cents} under an "amount_cents" key, {N:adj} before a noun,
# {AMT:plain} where the card names the currency).
FREE_FORMS = {"date": FORMS["date"], "datetime": FORMS["datetime"], "cents": ("symbol", "code", "whole"),
              "count": ("digits", "plain", "words"), "category": None, "id": ("raw",), "glob": ("raw", "code"),
              "url": ("full",), "name": ("raw",), "clause": ("raw",)}
DEFAULT_FORM = {"date": "dmy", "datetime": "iso", "cents": "symbol", "count": "digits", "category": "s0", "id": "raw",
                "glob": "raw", "url": "full", "name": "raw", "clause": "raw"}
NUMERIC_KINDS = ("cents", "count")
RESERVED_HOST_SUFFIXES = (".example", ".test", ".invalid")
RESERVED_HOSTS = ("example.com", "example.net", "example.org")

_ID_RE = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9_.:/#-]*[A-Za-z0-9])?")
_BAD_CHARS = re.compile(r"[{}\n\r]")


class SlotError(ValueError):
    """A slot value or form breaks its kind's rules."""


class SlotParseError(SlotError):
    """Text does not parse as the kind (or parses more than one way)."""


@dataclass(frozen=True)
class Slot:
    kind: str
    value: Any
    params: tuple = ()          # sorted (name, value) pairs; values are hashable

    def param(self, key, default=None):
        for k, v in self.params:
            if k == key:
                return v
        return default

    @property
    def schema(self) -> tuple:
        """(kind, params): what a parser may know about the slot without its value."""
        return (self.kind, self.params)


def _params(**kw) -> tuple:
    return tuple(sorted((k, v) for k, v in kw.items() if v is not None))


def _pget(params, key, default=None):
    for k, v in params or ():
        if k == key:
            return v
    return default


# ------------------------------------------------------------------------------------------------ constructors

def date_slot(d: dt.date) -> Slot:
    if not isinstance(d, dt.date) or isinstance(d, dt.datetime):
        raise SlotError(f"date slot needs a datetime.date, got {type(d).__name__}")
    return Slot("date", d)


def _check_offset(t: dt.datetime) -> None:
    if t.tzinfo is None or not isinstance(t.tzinfo, dt.timezone):
        raise SlotError("datetime slots need a fixed UTC offset (datetime.timezone), never a named zone or DST")
    off = t.utcoffset()
    mins = int(off.total_seconds() // 60)
    if off.total_seconds() % 60 or mins % 15 or not -12 * 60 <= mins <= 14 * 60:
        raise SlotError(f"offset {off} is not a whole quarter hour in [-12:00, +14:00]")
    if t.microsecond:
        raise SlotError("datetime slots carry whole seconds only")


def datetime_slot(t: dt.datetime) -> Slot:
    if not isinstance(t, dt.datetime):
        raise SlotError("datetime slot needs a datetime.datetime")
    _check_offset(t)
    return Slot("datetime", t)


def cents_slot(n: int, currency: str = "USD", symbol: str | None = "$") -> Slot:
    if isinstance(n, bool) or not isinstance(n, int):
        raise SlotError(f"cents must be an int (never a float), got {n!r}")
    if not re.fullmatch(r"[A-Za-z]{1,12}", currency or ""):
        raise SlotError(f"currency code {currency!r}")
    if symbol is not None and (not symbol or _BAD_CHARS.search(symbol) or any(c.isdigit() for c in symbol)):
        raise SlotError(f"currency symbol {symbol!r}")
    return Slot("cents", n, _params(currency=currency, symbol=symbol))


def count_slot(n: int, unit: tuple[str, str] | None = None) -> Slot:
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise SlotError(f"count must be an int >= 0, got {n!r}")
    if unit is not None:
        if (len(unit) != 2 or not all(isinstance(u, str) and re.fullmatch(r"[a-z][a-z -]*[a-z]", u) for u in unit)):
            raise SlotError(f"unit must be (singular, plural) lower-case words, got {unit!r}")
        unit = tuple(unit)
    return Slot("count", n, _params(unit=unit))


def category_slot(key: str, surfaces: dict) -> Slot:
    """`surfaces`: the whole closed set {key: [surface, ...]} (the card's category set), first surface = form s0."""
    items = []
    seen = {}
    for k, ss in surfaces.items():
        ss = tuple([ss] if isinstance(ss, str) else ss)
        if not ss:
            raise SlotError(f"category {k!r} has no surface")
        for s in ss:
            if not isinstance(s, str) or not s.strip() or s != s.strip() or _BAD_CHARS.search(s):
                raise SlotError(f"bad surface {s!r}")
            if s.casefold() in seen and seen[s.casefold()] != k:
                raise SlotError(f"surface {s!r} names two categories")
            seen[s.casefold()] = k
        items.append((k, ss))
    if key not in dict(items):
        raise SlotError(f"{key!r} is not in the category set")
    return Slot("category", key, _params(surfaces=tuple(sorted(items))))


def id_slot(s: str) -> Slot:
    if not isinstance(s, str) or not _ID_RE.fullmatch(s):
        raise SlotError(f"id {s!r}: letters, digits and - _ . : / # only, no spaces, alphanumeric ends")
    if negcount.k_all(s):
        raise SlotError(f"id {s!r} reads as a negation cue")
    return Slot("id", s)


def glob_slot(p: str) -> Slot:
    if not isinstance(p, str) or not p or re.search(r"[\s{}`]", p):
        raise SlotError(f"glob {p!r}: non-empty, no spaces, braces or backticks")
    return Slot("glob", p)


def url_slot(u: str) -> Slot:
    if not isinstance(u, str) or re.search(r"[\s{}]", u):
        raise SlotError(f"url {u!r}")
    sp = urlsplit(u)
    host = (sp.hostname or "").lower()
    if sp.scheme not in ("http", "https") or not host:
        raise SlotError(f"url {u!r}: http(s) with a host")
    if not (host.endswith(RESERVED_HOST_SUFFIXES) or host in RESERVED_HOSTS
            or any(host.endswith("." + h) for h in RESERVED_HOSTS)):
        raise SlotError(f"url host {host!r} is not a reserved example name")
    if sp.fragment or "@" in sp.netloc:
        raise SlotError(f"url {u!r}: no fragment, no userinfo")
    if not (sp.path or "/").startswith("/"):
        raise SlotError(f"url {u!r}: path must start with /")
    return Slot("url", u)


def name_slot(s: str) -> Slot:
    if not isinstance(s, str) or not s.strip() or s != s.strip() or _BAD_CHARS.search(s):
        raise SlotError(f"name {s!r}")
    if re.search(r"\d", s):
        raise SlotError(f"name {s!r} holds a digit (G-SL: numbers live in their own slots)")
    if negcount.k_all(s):
        raise SlotError(f"name {s!r} holds a negation cue (G-SL: no negation in names)")
    return Slot("name", s)


def clause_slot(sem: str, form_id: str, template: str) -> Slot:
    if not sem or not form_id or not isinstance(template, str) or "\n" in template:
        raise SlotError("clause slot needs sem, form_id and a one-line template")
    return Slot("clause", (sem, form_id, template))


# ------------------------------------------------------------------------------------------------ rendering

def _group3(n: int) -> str:
    return f"{n:,}"


def _offset_str(t: dt.datetime, colon=True) -> str:
    mins = int(t.utcoffset().total_seconds() // 60)
    sign = "+" if mins >= 0 else "-"
    h, m = divmod(abs(mins), 60)
    return f"{sign}{h:02d}:{m:02d}" if colon else f"{sign}{h:02d}{m:02d}"


def free_forms(slot: Slot) -> tuple:
    """The valid forms of `slot` that the program may choose without a template pinning them."""
    ok = FREE_FORMS[slot.kind]
    return tuple(f for f in forms(slot) if ok is None or f in ok)


def forms(slot: Slot) -> tuple:
    """The forms this slot value can be written in."""
    k, v = slot.kind, slot.value
    if k == "category":
        return tuple(f"s{i}" for i in range(len(dict(slot.param("surfaces"))[v])))
    out = FORMS[k]
    if k == "datetime":
        out = tuple(f for f in out if not (f == "iso_z" and v.utcoffset()) and not (f == "text" and v.second))
    elif k == "cents":
        out = tuple(f for f in out if not (f == "whole" and v % 100) and not (f == "symbol" and not slot.param("symbol"))
                    and not (f == "whole" and not slot.param("symbol")))
    elif k == "count":
        out = tuple(f for f in out if not (f in ("words", "adj_words") and v > 20)
                    and not (f in ("adj", "adj_words") and not slot.param("unit")))
    return out


def render(slot: Slot, form: str | None = None) -> str:
    """The text of `slot` in `form` (default: the kind's default form, or its first valid one)."""
    k, v = slot.kind, slot.value
    valid = forms(slot)
    if form is None:
        form = DEFAULT_FORM[k] if DEFAULT_FORM[k] in valid else valid[0]
    if form not in valid:
        raise SlotError(f"form {form!r} is not valid for this {k} slot (valid: {valid})")
    if k == "date":
        wd, d, m, y = WEEKDAYS[v.weekday()], v.day, MONTHS[v.month - 1], v.year
        return {"iso": v.isoformat(), "dmy": f"{d} {m} {y}", "mdy": f"{m} {d}, {y}",
                "dmy_abbr": f"{d} {MONTHS_ABBR[v.month - 1]} {y}", "wdmy": f"{wd}, {d} {m} {y}",
                "wmdy": f"{wd}, {m} {d}, {y}"}[form]
    if k == "datetime":
        if form == "iso":
            return v.strftime("%Y-%m-%dT%H:%M:%S") + _offset_str(v)
        if form == "iso_z":
            return v.strftime("%Y-%m-%dT%H:%M:%S") + "Z"
        if form == "text":
            return f"{v.day} {MONTHS[v.month - 1]} {v.year}, {v:%H:%M} (UTC{_offset_str(v)})"
        return v.strftime("%Y-%m-%d %H:%M:%S") + " " + _offset_str(v, colon=False)
    if k == "cents":
        neg, a = ("-" if v < 0 else ""), abs(v)
        major, minor = divmod(a, 100)
        sym, cur = slot.param("symbol"), slot.param("currency")
        if form == "symbol":
            return f"{neg}{sym}{_group3(major)}.{minor:02d}"
        if form == "code":
            return f"{neg}{_group3(major)}.{minor:02d} {cur}"
        if form == "plain":
            return f"{neg}{_group3(major)}.{minor:02d}"
        if form == "nocomma":
            return f"{neg}{major}.{minor:02d}"
        if form == "int_cents":
            return str(v)
        return f"{neg}{sym}{_group3(major)}"
    if k == "count":
        unit = slot.param("unit")
        if form in ("adj", "adj_words"):
            num = str(v) if form == "adj" else NUM_WORDS[v]
            return f"{num}-{unit[0]}"
        num = {"digits": _group3(v), "plain": str(v), "words": NUM_WORDS[v] if v <= 20 else None}[form]
        return num if not unit else f"{num} {unit[0] if v == 1 else unit[1]}"
    if k == "category":
        return dict(slot.param("surfaces"))[v][int(form[1:])]
    if k == "glob":
        return v if form == "raw" else f"`{v}`"
    if k == "url":
        return v
    if k == "clause":
        return v[2]
    return v


def canonical(slot: Slot):
    """JSON-able canonical value (G3 / G3-H comparisons, structure hashes)."""
    k, v = slot.kind, slot.value
    if k == "date":
        return v.isoformat()
    if k == "datetime":
        return v.isoformat()
    if k == "clause":
        return v[0]
    return v


def to_python(kind: str, canon):
    """Inverse of canonical() for the kinds whose python value differs (date, datetime)."""
    if kind == "date":
        return dt.date.fromisoformat(canon)
    if kind == "datetime":
        return dt.datetime.fromisoformat(canon)
    return canon


# ------------------------------------------------------------------------------------------------ regexes + parsing

_MON = "|".join(MONTHS)
_MONA = "|".join(MONTHS_ABBR)
_WD = "|".join(WEEKDAYS)
_W = "|".join(sorted(NUM_WORDS, key=len, reverse=True))
_GRP = r"\d{1,3}(?:,\d{3})*"


def form_names(kind: str, params=()) -> tuple:
    if kind == "category":
        n = max(len(ss) for _, ss in _pget(params, "surfaces"))
        return tuple(f"s{i}" for i in range(n))
    return FORMS[kind]


def regex(kind: str, form: str, params=()) -> str:
    """A non-capturing pattern for one form (broad: parse() decides validity)."""
    if kind == "date":
        return {"iso": r"\d{4}-\d{2}-\d{2}", "dmy": rf"\d{{1,2}} (?:{_MON}) \d{{4}}",
                "mdy": rf"(?:{_MON}) \d{{1,2}}, \d{{4}}", "dmy_abbr": rf"\d{{1,2}} (?:{_MONA}) \d{{4}}",
                "wdmy": rf"(?:{_WD}), \d{{1,2}} (?:{_MON}) \d{{4}}",
                "wmdy": rf"(?:{_WD}), (?:{_MON}) \d{{1,2}}, \d{{4}}"}[form]
    if kind == "datetime":
        return {"iso": r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}",
                "iso_z": r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z",
                "text": rf"\d{{1,2}} (?:{_MON}) \d{{4}}, \d{{2}}:\d{{2}} \(UTC[+-]\d{{2}}:\d{{2}}\)",
                "log": r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} [+-]\d{4}"}[form]
    if kind == "cents":
        sym = re.escape(_pget(params, "symbol") or "\x00")
        cur = re.escape(_pget(params, "currency") or "\x00")
        return {"symbol": rf"-?{sym}{_GRP}\.\d{{2}}", "code": rf"-?{_GRP}\.\d{{2}} {cur}", "plain": rf"-?{_GRP}\.\d{{2}}",
                "nocomma": r"-?\d+\.\d{2}", "int_cents": r"-?\d+", "whole": rf"-?{sym}{_GRP}(?!\.\d)(?!\d)(?!,\d)"}[form]
    if kind == "count":
        unit = _pget(params, "unit")
        u = rf" (?:{re.escape(unit[0])}|{re.escape(unit[1])})" if unit else ""
        if form == "adj":
            return rf"\d+-{re.escape(unit[0])}" if unit else r"(?!x)x"
        if form == "adj_words":
            return rf"(?:{_W})-{re.escape(unit[0])}" if unit else r"(?!x)x"
        return {"digits": _GRP + u, "plain": r"\d+" + u, "words": rf"(?:{_W})" + u}[form]
    if kind == "category":
        i = int(form[1:])
        ss = sorted({s[i] for _, s in _pget(params, "surfaces") if len(s) > i}, key=len, reverse=True)
        return "(?:" + "|".join(re.escape(s) for s in ss) + ")" if ss else r"(?!x)x"
    if kind == "id":
        return _ID_RE.pattern
    if kind == "glob":
        return r"[^\s{}`]+" if form == "raw" else r"`[^\s{}`]+`"
    if kind == "url":
        return r"https?://[A-Za-z0-9.-]+(?::\d+)?(?:/[^\s{}]*)?"
    if kind in ("name", "clause"):
        return r"[^\n{}]+?"
    raise SlotError(f"unknown kind {kind!r}")


def any_regex(kind: str, params=()) -> str:
    alts = []
    for f in form_names(kind, params):
        try:
            alts.append(regex(kind, f, params))
        except (KeyError, TypeError):
            continue
    return "(?:" + "|".join(sorted(set(alts), key=len, reverse=True)) + ")"


def _int(s: str) -> int:
    if not re.fullmatch(r"-?\d+", s):
        raise SlotParseError(f"not an integer: {s!r}")
    return int(s)


def _parse_form(kind: str, text: str, params, form: str):
    if not re.fullmatch(regex(kind, form, params), text):
        raise SlotParseError(f"{text!r} is not {kind}/{form}")
    if kind == "date":
        if form == "iso":
            try:
                return dt.date.fromisoformat(text)
            except ValueError as e:
                raise SlotParseError(str(e)) from None
        m = re.fullmatch(r"(?:(?P<wd>\w+), )?(?:(?P<d1>\d{1,2}) (?P<m1>\w+)|(?P<m2>\w+) (?P<d2>\d{1,2}),) (?P<y>\d{4})",
                         text)
        mon = m.group("m1") or m.group("m2")
        mi = (MONTHS_ABBR if form == "dmy_abbr" else MONTHS).index(mon) + 1
        try:
            d = dt.date(int(m.group("y")), mi, int(m.group("d1") or m.group("d2")))
        except ValueError as e:
            raise SlotParseError(str(e)) from None
        if m.group("wd") and m.group("wd") != WEEKDAYS[d.weekday()]:
            raise SlotParseError(f"weekday {m.group('wd')} does not match {d.isoformat()}")
        return d
    if kind == "datetime":
        try:
            if form == "iso":
                t = dt.datetime.fromisoformat(text)
            elif form == "iso_z":
                t = dt.datetime.fromisoformat(text[:-1] + "+00:00")
            elif form == "text":
                m = re.fullmatch(r"(\d{1,2}) (\w+) (\d{4}), (\d{2}):(\d{2}) \(UTC([+-])(\d{2}):(\d{2})\)", text)
                sign = 1 if m.group(6) == "+" else -1
                tz = dt.timezone(sign * dt.timedelta(hours=int(m.group(7)), minutes=int(m.group(8))))
                t = dt.datetime(int(m.group(3)), MONTHS.index(m.group(2)) + 1, int(m.group(1)), int(m.group(4)),
                                int(m.group(5)), tzinfo=tz)
            else:
                m = re.fullmatch(r"(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) ([+-])(\d{2})(\d{2})", text)
                t = dt.datetime.fromisoformat(f"{m.group(1)}T{m.group(2)}{m.group(3)}{m.group(4)}:{m.group(5)}")
        except ValueError as e:
            raise SlotParseError(str(e)) from None
        try:
            _check_offset(t)
        except SlotError as e:
            raise SlotParseError(str(e)) from None
        return t
    if kind == "cents":
        neg = text.startswith("-")
        body = text[1:] if neg else text
        sym, cur = _pget(params, "symbol"), _pget(params, "currency")
        if form in ("symbol", "whole"):
            body = body[len(sym):]
        if form == "code":
            body = body[: -(len(cur) + 1)]
        if form == "int_cents":
            return _int(text)
        if form == "whole":
            v = _int(body.replace(",", "")) * 100
        else:
            major, minor = body.replace(",", "").split(".")
            v = _int(major) * 100 + _int(minor)
        if form in ("symbol", "code", "plain", "whole") and "," not in body and len(body.split(".")[0]) > 3:
            raise SlotParseError(f"{text!r}: grouped form without its commas")
        return -v if neg else v
    if kind == "count":
        unit = _pget(params, "unit")
        if form in ("adj", "adj_words"):
            num = text[: -(len(unit[0]) + 1)]
            return _int(num) if form == "adj" else NUM_WORDS.index(num)
        num, u = (text.rsplit(" ", 1) if unit else (text, None))
        if form == "digits":
            if "," not in num and len(num) > 3:
                raise SlotParseError(f"{text!r}: digits form groups thousands")
            v = _int(num.replace(",", ""))
        elif form == "plain":
            v = _int(num)
        else:
            v = NUM_WORDS.index(num)
        if unit and u != (unit[0] if v == 1 else unit[1]):
            raise SlotParseError(f"{text!r}: unit does not agree with {v}")
        return v
    if kind == "category":
        i = int(form[1:])
        hits = [k for k, ss in _pget(params, "surfaces") if len(ss) > i and ss[i] == text]
        if len(hits) != 1:
            raise SlotParseError(f"{text!r} is not surface {form} of exactly one category")
        return hits[0]
    if kind == "glob":
        return text if form == "raw" else text[1:-1]
    if kind == "url":
        url_slot(text)
        return text
    if kind == "id":
        return text
    if kind == "name":
        name_slot(text)
        return text
    raise SlotParseError(f"{kind} is parsed by its owner (clauses: lexicon.LexiconRegistry.parse_exact)")


def parse(kind: str, text: str, params=(), form: str | None = None):
    """The python value of `text` as `kind` (in `form`, or in whichever form fits; several distinct readings raise)."""
    if form is not None:
        return _parse_form(kind, text, params, form)
    vals, errs = [], []
    for f in form_names(kind, params):
        try:
            v = _parse_form(kind, text, params, f)
        except (SlotParseError, ValueError, IndexError, AttributeError, TypeError) as e:
            errs.append(str(e))
            continue
        if v not in vals:
            vals.append(v)
    if not vals:
        raise SlotParseError(f"{text!r} does not parse as {kind}")
    if len(vals) > 1:
        raise SlotParseError(f"{text!r} parses as {kind} in more than one way: {vals}")
    return vals[0]


def roundtrip_ok(slot: Slot) -> bool:
    """Every valid form of `slot` parses back to its value (G-SL value check)."""
    if slot.kind == "clause":
        return True
    for f in forms(slot):
        try:
            if _parse_form(slot.kind, render(slot, f), slot.params, f) != slot.value:
                return False
        except SlotError:
            return False
    return True


def sample_slots(kind: str) -> list:
    """Deterministic sample values per kind for lexicon unit tests (G-LEX) and lints."""
    if kind == "date":
        return [date_slot(dt.date(2026, 2, 28)), date_slot(dt.date(2028, 2, 29)), date_slot(dt.date(2026, 12, 31))]
    if kind == "datetime":
        tz = dt.timezone(dt.timedelta(hours=2))
        return [datetime_slot(dt.datetime(2026, 3, 5, 14, 5, tzinfo=tz)),
                datetime_slot(dt.datetime(2026, 3, 5, 23, 59, tzinfo=dt.timezone.utc))]
    if kind == "cents":
        return [cents_slot(0), cents_slot(1), cents_slot(100), cents_slot(123450)]
    if kind == "count":
        return [count_slot(1, ("day", "days")), count_slot(7, ("day", "days")), count_slot(30, ("day", "days")),
                count_slot(0), count_slot(12), count_slot(1250)]
    if kind == "category":
        surf = {"prod": ["production"], "stage": ["staging"]}
        return [category_slot("prod", surf), category_slot("stage", surf)]
    if kind == "id":
        return [id_slot("INV-20419"), id_slot("call_7f3a")]
    if kind == "glob":
        return [glob_slot("billing.*"), glob_slot("/data/prod/*")]
    if kind == "url":
        return [url_slot("https://shop.example/cart?step=2")]
    if kind == "name":
        return [name_slot("Dana Okafor"), name_slot("Brightwell Supply")]
    raise SlotError(f"no samples for {kind!r}")

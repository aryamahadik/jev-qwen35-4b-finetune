"""Shared helpers for the F2 generator: paths, IO, Decimal context, display formats (U4, R7), RNG, guard, progress."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import random
import re
import sys
import time
from decimal import Decimal, localcontext, ROUND_HALF_UP, ROUND_HALF_EVEN, ROUND_FLOOR, ROUND_CEILING, Inexact
from pathlib import Path

HERE = Path(__file__).resolve().parent              # .../c_src/F2/gen
F2 = HERE.parent                                     # .../c_src/F2
CSRC = F2.parent                                     # .../c_src
LEAN = CSRC.parent                                   # .../opendecide-data/lean
OUT = F2 / "out"
TMP = F2 / "tmp"
PROGRESS = LEAN / "c_build" / "progress_phase2.log"
FMT1 = CSRC / "formats" / "formats-1"
FMT2 = CSRC / "formats" / "formats-2"
PACKS = CSRC / "packs"

SPEC_ID = "F2.G0.v7"
SPEC_SHA256 = "2c03f4cf4c6ea4a316accf93c4f502cef883158dfdb0b12cfc574aa933eaaac9"
GEN_VERSION = "F2-gen r1 v1.3"
SEED = 20261003
LICENCE = "CC0 1.0 (program-generated)"

# never-open guard (C_DATA_SPEC "Who may read what" + 7.4 + task allow-list); every input path goes through safe_path()
_NEVER = [re.compile(p, re.I) for p in (
    r"/lean/ohs3(/|$)", r"/lean/data/[^/]*ohs3", r"ohs3_parts", r"/lean/prep89(/|$)", r"/lean/preds",
    r"/c_spec/sealed_brief(/|$)", r"/lean/sealed_nd(/|$)", r"/bench(/|$)", r"/c_spec/RESEARCH_", r"/c_spec/REVIEW_",
    r"/c_spec/LICENCE_CHECK_", r"/c_spec/ADDENDUM_", r"/\.claude/projects(/|$)", r"^/private/tmp/claude-501",
    r"^/tmp/claude-501")]
_JEV = re.compile(r"(^|[_/.-])jev", re.I)
REPO = LEAN.parents[1]


def safe_path(p) -> Path:
    rp = Path(p).resolve()
    s = str(rp)
    for rx in _NEVER:
        if rx.search(s):
            raise SystemExit(f"refused input path (never-open list): {p}")
    try:
        rel = "/" + str(rp.relative_to(REPO))
    except ValueError:
        rel = s
    if _JEV.search(rel):
        raise SystemExit(f"refused input path (7.4 jev name rule): {p}")
    return rp


def read_jsonl(p):
    with open(safe_path(p), encoding="utf-8") as f:
        return [json.loads(x) for x in f if x.strip()]


def write_jsonl(p, rows) -> str:
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, default=_jdefault) + "\n")
    return sha_file(p)


def _jdefault(o):
    if isinstance(o, Decimal):
        return str(o)
    if isinstance(o, (dt.date, dt.datetime)):
        return o.isoformat()
    if isinstance(o, (set, frozenset, tuple)):
        return list(o)
    raise TypeError(f"not serialisable: {type(o).__name__}")


def write_json(p, obj) -> str:
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1, default=_jdefault)
        f.write("\n")
    return sha_file(p)


def sha_file(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def progress(msg: str):
    line = f"[F2] {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} {msg}"
    if not os.environ.get("F2_QUIET"):
        with open(PROGRESS, "a") as f:
            f.write(line + "\n")
    print(line, file=sys.stderr, flush=True)


def rng_for(*key) -> random.Random:
    h = hashlib.sha256(("\x1f".join(str(k) for k in (SEED,) + key)).encode()).digest()
    return random.Random(int.from_bytes(h[:8], "big"))


def uhash(*key) -> float:
    h = hashlib.sha256(("\x1f".join(str(k) for k in key)).encode()).digest()
    return int.from_bytes(h[:8], "big") / 2 ** 64


# ----------------------------------------------------------------------------------------------------------------- Decimal

D = Decimal
ZERO, ONE, HUNDRED = D(0), D(1), D(100)
MODES = {"half_up": ROUND_HALF_UP, "half_even": ROUND_HALF_EVEN, "floor": ROUND_FLOOR, "ceiling": ROUND_CEILING}


def dctx():
    """A local Decimal context, precision 50, Inexact trapped by the caller when it needs the guard (A37)."""
    c = localcontext()
    return c


def exact_div(a: Decimal, b: Decimal) -> Decimal:
    """a / b at precision 50; raises InexactError if not exact at that precision (the A37 guard keeps such values out)."""
    with localcontext() as c:
        c.prec = 50
        c.traps[Inexact] = True
        try:
            return a / b
        except Inexact:
            raise InexactError(f"{a}/{b}")


class InexactError(ArithmeticError):
    pass


def quant(v: Decimal, unit: Decimal, mode: str) -> Decimal:
    """Round v to a multiple of unit (unit = 10^k of the display unit) in mode. Half-even on a coarse unit means the
    multiple whose number of units is even (R4-02): implemented by rounding v / unit to an integer."""
    if v < 0:
        raise ValueError("rounding never sees a negative value (A25)")
    with localcontext() as c:
        c.prec = 60
        q = (v / unit).quantize(ONE, rounding=MODES[mode])
        return q * unit


def on_grid(v: Decimal, unit: Decimal) -> bool:
    with localcontext() as c:
        c.prec = 60
        return (v / unit) == (v / unit).to_integral_value()


def dnorm(v: Decimal) -> Decimal:
    """Strip trailing zeros without exponent form."""
    if v == v.to_integral_value():
        return v.quantize(ONE)
    return v.normalize()


# ----------------------------------------------------------------------------------------------------------------- display

def money_str(v: Decimal, dec2: bool) -> str:
    """Display a money amount on the card's grid (R7): two decimals, or whole units. Raises if off-grid."""
    if dec2:
        if not on_grid(v, D("0.01")):
            raise ValueError(f"money {v} off the 0.01 grid")
        return f"{v.quantize(D('0.01')):f}"
    if not on_grid(v, ONE):
        raise ValueError(f"money {v} off the whole-unit grid")
    return f"{v.quantize(ONE):f}"


def num_str(v) -> str:
    """A plain number: ints as digits, Decimals without exponent or trailing zeros."""
    if isinstance(v, int):
        return str(v)
    v = D(v)
    if v == v.to_integral_value():
        return f"{v.quantize(ONE):f}"
    s = f"{v.normalize():f}"
    return s


def pct_str(p: Decimal) -> str:
    return num_str(p) + "%"


WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]
DATE_FORMS = ("gb_long", "us_long", "iso")


def date_str(d: dt.date, form: str, weekday: bool = False) -> str:
    """U4 date forms; weekday stated when asked (D9 anchors, holidays, strip dates)."""
    wd = WEEKDAYS[d.weekday()]
    if form == "gb_long":
        s = f"{d.day} {MONTHS[d.month - 1]} {d.year}"
        return f"{wd}, {s}" if weekday else s
    if form == "us_long":
        s = f"{MONTHS[d.month - 1]} {d.day}, {d.year}"
        return f"{wd}, {s}" if weekday else s
    if form == "iso":
        s = d.isoformat()
        return f"{s} ({wd})" if weekday else s
    raise ValueError(form)


NUM_WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
             "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty"]


def dump_canon(obj) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"), default=_jdefault)

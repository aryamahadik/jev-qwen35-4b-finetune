"""c2_kit/brute.py: brute-force helpers for solver B (enumeration and table paradigms; C2_DATA_SPEC 3.x verifiers).

Nothing here imports rules.py or glob_a.py. Each helper computes by enumeration or by integer arithmetic on its own
terms, so a solver B built on them shares no code path with a solver A built on the rule AST.

  completions(fn, env, domains)   the set of fn(env + one completion) over every completion of the missing slots
                                  (exact "cannot decide": a decision is determined iff the set has one element;
                                  the family must state every domain, including the boundary witnesses)
  day_list(start, end)            every date from start to end, both included (day-by-day bitmap paradigm)
  window_days(anchor, n)          the n + 1 dates anchor + 0 .. anchor + n (day 0 = the anchor)
  epoch_minutes(t)                minutes since 1970-01-01T00:00Z from the calendar fields and the offset, by integer
                                  arithmetic on proleptic ordinals (no timestamp() call)
  cents_of(text)                  integer cents from a decimal string "-1,234.50" / "1234.5" / "12" (no float)
  table_lookup(table, key)        exact-key lookup that refuses a missing or duplicated key
"""
from __future__ import annotations

import datetime as dt
import itertools
import re
from typing import Callable, Iterable

_EPOCH_ORD = dt.date(1970, 1, 1).toordinal()


def completions(fn: Callable[[dict], object], env: dict, domains: dict) -> set:
    missing = [k for k in sorted(domains) if env.get(k) is None]
    outs = set()
    for combo in itertools.product(*[list(domains[k]) for k in missing]):
        e = dict(env)
        e.update(zip(missing, combo))
        outs.add(fn(e))
    return outs


def day_list(start: dt.date, end: dt.date) -> list:
    out, d = [], start
    while d <= end:
        out.append(d)
        d = d + dt.timedelta(days=1)
    return out


def window_days(anchor: dt.date, n: int) -> list:
    out, d = [], anchor
    for _ in range(n + 1):
        out.append(d)
        d = d + dt.timedelta(days=1)
    return out


def epoch_minutes(t: dt.datetime) -> int:
    off = t.utcoffset()
    if off is None:
        raise ValueError("epoch_minutes needs an aware datetime")
    off_min = off.days * 1440 + off.seconds // 60
    return (t.toordinal() - _EPOCH_ORD) * 1440 + t.hour * 60 + t.minute - off_min


def cents_of(text: str) -> int:
    s = text.strip().replace(",", "")
    m = re.fullmatch(r"(-?)(\d+)(?:\.(\d{1,2}))?", s)
    if not m:
        raise ValueError(f"not a decimal amount: {text!r}")
    minor = (m.group(3) or "0").ljust(2, "0")
    v = int(m.group(2)) * 100 + int(minor)
    return -v if m.group(1) else v


def table_lookup(table: Iterable, key):
    hits = [v for k, v in table if k == key]
    if len(hits) != 1:
        raise KeyError(f"{key!r}: {len(hits)} table entries")
    return hits[0]

#!/usr/bin/env python3
"""Gold programs for the OpenDecide v1.0-rc fresh items (FR; DESIGN section 7, label rule R14 FRESH_SPEC).

authored_by: llm:claude:fresh-coordinator   (deviations D1, D3: FR items are written by Claude agents)

An FR item is a JSON spec (`spec_version: fr-spec-1`, see spec.schema.json). The author never types a gold
value. Gold for every question is computed here from the spec's `parameters`:

  1. family function   parameters -> environment of named facts and derived quantities, plus the value
                       domain of every categorical variable a Choice may ask about
                       (env_num, env_date, env_hop, env_lit, env_phish, env_hneg)
  2. derived           optional arithmetic / predicate definitions evaluated in order (all families)
  3. outcome_rules     FR-NUM, FR-DATE, FR-HOP: ordered decision list, first match wins, the last rule is
                       the default; its outcomes are the Choice domain (so the option set is exhaustive)
  4. questions         q3 Choice -> option key of the family's choice variable
                       q1 Noul    = 1[gold(q3) == L*]   (L* = asks.choice_is, one of q3's options)
                       q2 Noul    = predicate over the environment (FR-LIT: criteria variant, gold != q1)
                          or Score K=4 (FR-NUM Score states)
                       q4 Noul    = 1 - gold(q1)  (free negation, R2_NEG)
                       q5 Noul    = gold(q1)      (free paraphrase, R3_EQUIV)
                       q7 Score   = count / var / bins / map (FR-LIT K=4 or 7, FR-HOP K=7, FR-PHISH K=7)
     q6 (DNEG or CHOICE2 of q1) is rendered later by the build from the eval template bank.

Gold encoding: Noul 0/1, Choice option key (str), Score 0-based level (int).

Usage (paths are quoted because the project path contains "551 CONTAINERS " with a trailing space):
  python3 gold_programs.py test
  python3 gold_programs.py check SPECS.jsonl [--cards scenario_cards.jsonl] [--show-gold] [--strict]
  python3 gold_programs.py gold SPECS.jsonl --out GOLD.jsonl
  python3 gold_programs.py merge A.jsonl B.jsonl C.jsonl --out fresh_specs.jsonl
The checker prints the id of the nearest template-like phrasing for a free variant, never its text.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
import unittest
from collections import defaultdict
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent  # opendecide-data/
PROGRAM_VERSION = "fr-gold-1"
SPEC_VERSION = "fr-spec-1"

FAMILIES = ("FR-NUM", "FR-DATE", "FR-HOP", "FR-LIT", "FR-PHISH", "FR-HNEG")
FAMILY_CODES = {f: f.split("-")[1] for f in FAMILIES}
VERTICALS = ("telecom", "insurance", "utilities", "travel", "retail")
TRAIN_HARDNEG_VERTICALS = ("HR helpdesk", "IT helpdesk", "e-commerce returns")  # never used in FR
LENGTH_BINS = {"short": (60, 99), "medium": (100, 139), "long": (140, 180)}
GROUNDED = ("FR-NUM", "FR-DATE", "FR-HOP")  # R14: policy/record items carry a scope phrase on every question
AUTHORS = ("llm:claude:fresh-author-A", "llm:claude:fresh-author-B", "llm:claude:fresh-author-C")
SLOTS = ("q1", "q2", "q3", "q4", "q5", "q7")

STANCE_KEYS = ("complaint", "praise only", "neutral mention", "not mentioned")  # FR-LIT Choice keys (fixed)
PHISH_KEYS = ("phishing", "marketing", "transactional", "personal")  # FR-PHISH Choice keys (DESIGN 7, fixed)
NONE_KEY = "none of these"  # FR-HNEG exhaustive option
PHISH_DERIVED_SIGNS = ("sender_mismatch", "link_mismatch", "reply_to_mismatch")
PHISH_DECLARED_SIGNS = ("asks_secret", "unusual_payment", "asks_personal_data", "unexpected_attachment",
                        "threat_or_deadline", "generic_greeting", "prize_lure", "asks_click_or_call",
                        "mentions_account_problem")
PHISH_SIGNS = PHISH_DERIVED_SIGNS + PHISH_DECLARED_SIGNS
PHISH_IMPERSONATION = PHISH_DERIVED_SIGNS
PHISH_HARMFUL = ("asks_secret", "unusual_payment", "asks_personal_data", "unexpected_attachment")
PHISH_PURPOSE = {  # purpose of a genuine email -> Choice category (used only when the email is not phishing)
    "promotion": "marketing", "newsletter": "marketing", "loyalty_offer": "marketing",
    "bill": "transactional", "receipt": "transactional", "order_update": "transactional",
    "booking_update": "transactional", "account_notice": "transactional", "security_notice": "transactional",
    "service_notice": "transactional", "claim_update": "transactional",
    "personal_note": "personal", "personal_request": "personal",
}
PHISH_SAFE_TLDS = ("example", "test")
LIT_REMARK_ATTRS = {"polarity": ("pos", "neg", "neutral"), "severity": ("none", "cosmetic", "minor", "major"),
                    "speaker": ("reviewer", "other")}
LIT_REMARK_DEFAULTS = {"severity": "none", "resolved": False, "speaker": "reviewer", "topic": ""}
HNEG_SPEAKERS = ("customer", "third_party", "agent_note", "system")
HNEG_CUSTOMER_ACTS = ("request", "withdraw", "replace", "decline", "info")
HNEG_OTHER_ACTS = ("suggest", "claim", "info")
CHOICE_VAR = {"FR-NUM": "outcome", "FR-DATE": "outcome", "FR-HOP": "outcome", "FR-PHISH": "category",
              "FR-HNEG": "final_request"}  # FR-LIT: "stance:<filter>:<aspect>"
BANNED_KEY_TOKENS = {"yes", "no", "true", "false", "correct", "incorrect", "cannot", "other", "none"}
FREE_JACCARD_MAX = 0.6  # DESIGN 7 step 4: token Jaccard < 0.6 against every template-like phrasing
PARAPHRASE_COPY_WARN = 0.8  # q5 vs q1 token Jaccard at or above this is flagged as a near copy


class SpecError(ValueError):
    """A spec that the gold program cannot evaluate (fatal for that item)."""


# ---------------------------------------------------------------------------------------------------------
# values
# ---------------------------------------------------------------------------------------------------------
NUM_STR_RE = re.compile(r"^-?\d+(?:\.\d+)?$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TIME_RE = re.compile(r"^(?:[01]\d|2[0-3]):[0-5]\d$")


def to_dec(x, what="value"):
    if isinstance(x, bool) or x is None:
        raise SpecError(f"{what}: expected a number, got {x!r}")
    if isinstance(x, Decimal):
        return x
    if isinstance(x, int):
        return Decimal(x)
    if isinstance(x, float):
        return Decimal(repr(x))
    if isinstance(x, str) and NUM_STR_RE.match(x.strip()):
        return Decimal(x.strip())
    raise SpecError(f"{what}: expected a number, got {x!r}")


def to_date(x, what="date"):
    if isinstance(x, dt.date):
        return x
    if isinstance(x, str) and DATE_RE.match(x):
        try:
            return dt.date.fromisoformat(x)
        except ValueError as e:
            raise SpecError(f"{what}: invalid date {x!r} ({e})") from None
    raise SpecError(f"{what}: expected YYYY-MM-DD, got {x!r}")


def coerce_value(v, what="value"):
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return to_dec(v, what)
    if isinstance(v, str):
        return to_date(v, what) if DATE_RE.match(v) else v
    if isinstance(v, list):
        return [coerce_value(e, what) for e in v]
    raise SpecError(f"{what}: unsupported value {v!r} (use numbers, booleans, strings, YYYY-MM-DD dates or lists)")


def fmt(v):
    if isinstance(v, Decimal):
        s = format(v.normalize(), "f")
        return s
    if isinstance(v, dt.date):
        return v.isoformat()
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, list):
        return "[" + ", ".join(fmt(e) for e in v) + "]"
    return str(v)


def jsonable(v):
    if isinstance(v, Decimal):
        return int(v) if v == v.to_integral_value() else float(v)
    if isinstance(v, dt.date):
        return v.isoformat()
    if isinstance(v, list):
        return [jsonable(e) for e in v]
    if isinstance(v, dict):
        return {k: jsonable(e) for k, e in v.items()}
    return v


class Ctx:
    """Environment of named values, categorical domains and non-fatal warnings for one spec."""

    def __init__(self):
        self.env = {}
        self.domains = {}
        self.warnings = []
        self.mute = 0

    def warn(self, msg):
        if not self.mute and msg not in self.warnings:
            self.warnings.append(msg)

    def set(self, name, value):
        if not isinstance(name, str) or not name:
            raise SpecError(f"invalid variable name {name!r}")
        if name in self.env:
            raise SpecError(f"variable {name!r} is defined twice")
        self.env[name] = value

    def get(self, name):
        if not isinstance(name, str):
            raise SpecError(f"variable name must be a string, got {name!r}")
        if name not in self.env:
            near = sorted(k for k in self.env if k.split(":")[-1] == name.split(":")[-1])[:5]
            raise SpecError(f"unknown variable {name!r}" + (f" (did you mean {near}?)" if near else ""))
        return self.env[name]


# ---------------------------------------------------------------------------------------------------------
# predicates, derived quantities, decision lists (shared by every family)
# ---------------------------------------------------------------------------------------------------------
def _coerce_like(lit, like, path):
    if isinstance(lit, list):
        base = like[0] if isinstance(like, list) and like else like
        return [_coerce_like(e, base, path) for e in lit]
    if isinstance(like, list):
        return _coerce_like(lit, like[0], path) if like else coerce_value(lit, path)
    if isinstance(like, bool):
        return lit
    if isinstance(like, Decimal) and not isinstance(lit, bool) and isinstance(lit, (int, float, str)):
        return to_dec(lit, path)
    if isinstance(like, dt.date) and isinstance(lit, str):
        return to_date(lit, path)
    if isinstance(like, str):
        return lit
    return coerce_value(lit, path)


def _kind(v):
    if isinstance(v, bool):
        return "bool"
    if isinstance(v, Decimal):
        return "number"
    if isinstance(v, dt.date):
        return "date"
    if isinstance(v, str):
        return "string"
    if isinstance(v, list):
        return "list"
    return type(v).__name__


def _compare(a, op, b, ctx, label):
    if op in ("in", "not_in"):
        if not isinstance(b, list):
            raise SpecError(f"{label}: '{op}' needs a list value")
        for e in b:
            if _kind(e) != _kind(a):
                raise SpecError(f"{label}: list element {fmt(e)!r} is a {_kind(e)}, variable is a {_kind(a)}")
        r = a in b
        return r if op == "in" else not r
    if op in ("contains", "not_contains"):
        if not isinstance(a, list):
            raise SpecError(f"{label}: '{op}' needs a list variable")
        r = b in a
        return r if op == "contains" else not r
    if op in ("==", "!="):
        if _kind(a) != _kind(b):
            raise SpecError(f"{label}: cannot compare a {_kind(a)} with a {_kind(b)}")
        r = a == b
        return r if op == "==" else not r
    if op in ("<", "<=", ">", ">="):
        if _kind(a) != _kind(b) or _kind(a) not in ("number", "date"):
            raise SpecError(f"{label}: '{op}' needs two numbers or two dates, got {_kind(a)} and {_kind(b)}")
        if a == b:
            ctx.warn(f"boundary: '{label}' is decided at equality ({fmt(a)}); the state must make the "
                     f"inclusive/exclusive reading explicit (e.g. 'or more', 'up to and including', 'more than')")
        return {"<": a < b, "<=": a <= b, ">": a > b, ">=": a >= b}[op]
    raise SpecError(f"{label}: unknown operator {op!r}")


def eval_pred(p, ctx, path="pred"):
    """Evaluate a predicate object. Forms:
    {"var": name, "op": OP, "value": literal} | {"var": name, "op": OP, "var2": name}
    {"is_true": name} | {"is_false": name} | {"not": P} | {"all": [P, P, ...]} | {"any": [P, P, ...]}
    OP: == != < <= > >= in not_in contains not_contains. All branches are evaluated (no short circuit), so an
    unknown variable anywhere is an error."""
    if not isinstance(p, dict) or not p:
        raise SpecError(f"{path}: a predicate must be a non-empty object")
    keys = set(p)
    if keys in ({"all"}, {"any"}):
        k = next(iter(keys))
        items = p[k]
        if not isinstance(items, list) or len(items) < 2:
            raise SpecError(f"{path}.{k}: needs a list of at least 2 predicates")
        vals = [eval_pred(q, ctx, f"{path}.{k}[{i}]") for i, q in enumerate(items)]
        return all(vals) if k == "all" else any(vals)
    if keys == {"not"}:
        return not eval_pred(p["not"], ctx, path + ".not")
    if keys in ({"is_true"}, {"is_false"}):
        k = next(iter(keys))
        v = ctx.get(p[k])
        if not isinstance(v, bool):
            raise SpecError(f"{path}: {p[k]!r} is a {_kind(v)}, not a boolean")
        return v if k == "is_true" else not v
    if keys in ({"var", "op", "value"}, {"var", "op", "var2"}):
        a = ctx.get(p["var"])
        if "var2" in p:
            b = ctx.get(p["var2"])
            label = f"{p['var']} {p['op']} {p['var2']}"
        else:
            b = _coerce_like(p["value"], a, path)
            label = f"{p['var']} {p['op']} {fmt(b)}"
        return _compare(a, p["op"], b, ctx, label)
    raise SpecError(f"{path}: unrecognised predicate {json.dumps(p)[:160]}")


def _arg(x, ctx, path):
    if isinstance(x, bool):
        return x
    if isinstance(x, (int, float)):
        return to_dec(x, path)
    if isinstance(x, str):
        return ctx.get(x)
    if isinstance(x, dict) and set(x) == {"date"}:
        return to_date(x["date"], path)
    raise SpecError(f"{path}: an argument is a number, a variable name or {{\"date\": \"YYYY-MM-DD\"}}, got {x!r}")


def _nums(args, path, n=None, at_least=None):
    if n is not None and len(args) != n:
        raise SpecError(f"{path}: needs exactly {n} arguments")
    if at_least is not None and len(args) < at_least:
        raise SpecError(f"{path}: needs at least {at_least} arguments")
    for a in args:
        if not isinstance(a, Decimal):
            raise SpecError(f"{path}: arithmetic needs numbers, got {fmt(a)!r}")
    return args


def eval_derived(items, ctx):
    """derived: [{"name", "op", "args"} | {"name", "op": "pred", "pred"} | {"name", "op": "count_true", "preds"}]
    ops: add sub mul div min max abs round2 pct (a/b*100) days_between (date a -> date b) add_days (date, n)
    pred count_true. Evaluated in order; later definitions may use earlier ones."""
    if items is None:
        return
    if not isinstance(items, list):
        raise SpecError("derived must be a list")
    for i, d in enumerate(items):
        path = f"derived[{i}]"
        if not isinstance(d, dict) or "name" not in d or "op" not in d:
            raise SpecError(f"{path}: needs 'name' and 'op'")
        op = d["op"]
        if op == "pred":
            val = eval_pred(d.get("pred"), ctx, path + ".pred")
        elif op == "count_true":
            preds = d.get("preds")
            if not isinstance(preds, list) or not preds:
                raise SpecError(f"{path}: count_true needs a non-empty 'preds' list")
            val = Decimal(sum(1 for j, q in enumerate(preds) if eval_pred(q, ctx, f"{path}.preds[{j}]")))
        else:
            args = [_arg(a, ctx, path) for a in d.get("args", [])]
            if op == "add":
                val = sum(_nums(args, path, at_least=2), Decimal(0))
            elif op == "sub":
                a, b = _nums(args, path, n=2)
                val = a - b
            elif op == "mul":
                val = Decimal(1)
                for a in _nums(args, path, at_least=2):
                    val *= a
            elif op == "div":
                a, b = _nums(args, path, n=2)
                if b == 0:
                    raise SpecError(f"{path}: division by zero")
                val = a / b
            elif op in ("min", "max"):
                vals = _nums(args, path, at_least=2)
                val = min(vals) if op == "min" else max(vals)
            elif op == "abs":
                (a,) = _nums(args, path, n=1)
                val = abs(a)
            elif op == "round2":
                (a,) = _nums(args, path, n=1)
                val = a.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            elif op == "pct":
                a, b = _nums(args, path, n=2)
                if b == 0:
                    raise SpecError(f"{path}: division by zero")
                val = a / b * 100
            elif op == "days_between":
                if len(args) != 2 or not all(isinstance(a, dt.date) for a in args):
                    raise SpecError(f"{path}: days_between needs two dates")
                val = Decimal((args[1] - args[0]).days)
            elif op == "add_days":
                if len(args) != 2 or not isinstance(args[0], dt.date) or not isinstance(args[1], Decimal):
                    raise SpecError(f"{path}: add_days needs a date and a whole number")
                if args[1] != args[1].to_integral_value():
                    raise SpecError(f"{path}: add_days needs a whole number of days")
                val = args[0] + dt.timedelta(days=int(args[1]))
            else:
                raise SpecError(f"{path}: unknown op {op!r}")
        ctx.set(d["name"], val)


def eval_outcome(rules, ctx):
    """Ordered decision list. Each rule {"when": P, "outcome": key}; the last rule has no "when" (default).
    First match wins. Rules after the match are still evaluated (to catch unknown variables) with warnings muted."""
    if not isinstance(rules, list) or len(rules) < 2:
        raise SpecError("outcome_rules: need at least 2 rules (the last is the default)")
    chosen, outcomes = None, []
    for i, r in enumerate(rules):
        if not isinstance(r, dict):
            raise SpecError(f"outcome_rules[{i}]: must be an object")
        out = r.get("outcome")
        if not isinstance(out, str) or not out.strip():
            raise SpecError(f"outcome_rules[{i}]: 'outcome' must be a non-empty string")
        outcomes.append(out)
        last = i == len(rules) - 1
        if r.get("when") is None:
            if not last:
                raise SpecError(f"outcome_rules[{i}]: only the last rule may omit 'when'")
            hit = True
        else:
            if last:
                raise SpecError("outcome_rules: the last rule must be the default (no 'when')")
            if chosen is not None:
                ctx.mute += 1
            try:
                hit = eval_pred(r["when"], ctx, f"outcome_rules[{i}].when")
            finally:
                if chosen is not None:
                    ctx.mute -= 1
        if hit and chosen is None:
            chosen = out
    domain = list(dict.fromkeys(outcomes))
    if len(domain) < 2:
        raise SpecError("outcome_rules: need at least 2 distinct outcomes")
    ctx.set("outcome", chosen)
    ctx.domains["outcome"] = domain


def load_vars(params, ctx):
    v = params.get("vars", {}) or {}
    if not isinstance(v, dict):
        raise SpecError("vars must be an object {name: value}")
    for k, val in v.items():
        if ":" in k:
            raise SpecError(f"vars: {k!r} may not contain ':' (reserved for family variables)")
        ctx.set(k, coerce_value(val, f"vars.{k}"))


# ---------------------------------------------------------------------------------------------------------
# family functions
# ---------------------------------------------------------------------------------------------------------
def env_num(params, ctx):
    """FR-NUM. line_items [{label, amount, qty=1, counts=true}], credits [{label, amount}], vars, derived.
    env: item:<label> (amount*qty), subtotal (counted lines), excluded_total, credits_total,
         total (= subtotal - credits_total), item_count (sum of qty of counted lines), max_item, outcome."""
    load_vars(params, ctx)
    subtotal = excluded = credits_total = count = Decimal(0)
    max_item = None
    labels = set()
    for i, it in enumerate(params.get("line_items", []) or []):
        path = f"line_items[{i}]"
        label = it.get("label")
        if not isinstance(label, str) or not label or label in labels:
            raise SpecError(f"{path}: needs a unique non-empty 'label'")
        labels.add(label)
        qty = to_dec(it.get("qty", 1), path + ".qty")
        if qty <= 0 or qty != qty.to_integral_value():
            raise SpecError(f"{path}: qty must be a positive whole number")
        line = to_dec(it.get("amount"), path + ".amount") * qty
        ctx.set(f"item:{label}", line)
        if it.get("counts", True):
            subtotal += line
            count += qty
            max_item = line if max_item is None else max(max_item, line)
        else:
            excluded += line
    for i, c in enumerate(params.get("credits", []) or []):
        amt = to_dec(c.get("amount"), f"credits[{i}].amount")
        if amt < 0:
            raise SpecError(f"credits[{i}]: give credits as positive amounts (they are subtracted)")
        label = c.get("label")
        if not isinstance(label, str) or not label or label in labels:
            raise SpecError(f"credits[{i}]: needs a unique non-empty 'label'")
        labels.add(label)
        ctx.set(f"credit:{label}", amt)
        credits_total += amt
    for k, v in (("subtotal", subtotal), ("excluded_total", excluded), ("credits_total", credits_total),
                 ("total", subtotal - credits_total), ("item_count", count),
                 ("max_item", max_item if max_item is not None else Decimal(0))):
        ctx.set(k, v)
    eval_derived(params.get("derived"), ctx)
    eval_outcome(params.get("outcome_rules"), ctx)


def is_business_day(d, holidays):
    return d.weekday() < 5 and d not in holidays


def add_business_days(start, n, holidays):
    """Day 1 is the first business day after `start`; returns the date of business day n (n >= 1)."""
    if n < 1:
        raise SpecError("business-day windows need length >= 1")
    d, k = start, 0
    while k < n:
        d += dt.timedelta(days=1)
        if is_business_day(d, holidays):
            k += 1
    return d


def business_days_between(a, b, holidays):
    """Number of business days d with a < d <= b (negative if b < a)."""
    if b == a:
        return 0
    sign, lo, hi = (1, a, b) if b > a else (-1, b, a)
    n, d = 0, lo
    while d < hi:
        d += dt.timedelta(days=1)
        if is_business_day(d, holidays):
            n += 1
    return sign * n


WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")


def env_date(params, ctx):
    """FR-DATE. today (YYYY-MM-DD), now (HH:MM, optional), dates {name: date}, holidays [dates],
    windows [{name, start, length, unit: calendar_days|business_days, end: "today"|<date name>, cutoff: HH:MM}].
    Conventions: calendar deadline = start + length days; business deadline = the length-th business day after
    start (Mon-Fri, not a listed holiday); a window is open iff end <= deadline (inclusive); on the deadline day
    with a cutoff, open iff now <= cutoff.
    env: today, weekday:today, date:<n>, weekday:<n>, days_since:<n>, bdays_since:<n>, deadline:<w>,
         open:<w>, elapsed:<w> (days or business days from start to end), is_weekend:<n>, outcome."""
    today = to_date(params.get("today"), "today")
    ctx.set("today", today)
    ctx.set("weekday:today", WEEKDAYS[today.weekday()])
    holidays = {to_date(h, "holidays") for h in params.get("holidays", []) or []}
    now = params.get("now")
    if now is not None and not (isinstance(now, str) and TIME_RE.match(now)):
        raise SpecError("now must be HH:MM (24-hour)")
    dates = params.get("dates", {}) or {}
    if not isinstance(dates, dict) or not dates:
        raise SpecError("dates must be a non-empty object {name: YYYY-MM-DD}")
    for name, s in dates.items():
        d = to_date(s, f"dates.{name}")
        ctx.set(f"date:{name}", d)
        ctx.set(f"weekday:{name}", WEEKDAYS[d.weekday()])
        ctx.set(f"is_weekend:{name}", d.weekday() >= 5)
        ctx.set(f"days_since:{name}", Decimal((today - d).days))
        ctx.set(f"bdays_since:{name}", Decimal(business_days_between(d, today, holidays)))
    load_vars(params, ctx)
    for i, w in enumerate(params.get("windows", []) or []):
        path = f"windows[{i}]"
        name = w.get("name")
        if not isinstance(name, str) or not name:
            raise SpecError(f"{path}: needs a name")
        start = ctx.get(f"date:{w.get('start')}")
        n = to_dec(w.get("length"), path + ".length")
        if n != n.to_integral_value() or n < 0:
            raise SpecError(f"{path}: length must be a whole number >= 0")
        n = int(n)
        unit = w.get("unit")
        end_name = w.get("end", "today")
        end = today if end_name == "today" else ctx.get(f"date:{end_name}")
        if unit == "calendar_days":
            deadline = start + dt.timedelta(days=n)
            elapsed = (end - start).days
        elif unit == "business_days":
            deadline = add_business_days(start, n, holidays)
            elapsed = business_days_between(start, end, holidays)
        else:
            raise SpecError(f"{path}: unit must be calendar_days or business_days")
        cutoff = w.get("cutoff")
        if cutoff is not None and not (isinstance(cutoff, str) and TIME_RE.match(cutoff)):
            raise SpecError(f"{path}: cutoff must be HH:MM")
        if end < deadline:
            is_open = True
        elif end > deadline:
            is_open = False
        else:
            if cutoff is not None and end_name == "today":
                if now is None:
                    raise SpecError(f"{path}: a cutoff on the deadline day needs 'now'")
                is_open = now <= cutoff
                if now == cutoff:
                    ctx.warn(f"boundary: window {name!r} is decided at the cutoff minute {cutoff}")
            else:
                is_open = True
                ctx.warn(f"boundary: window {name!r} is decided on its deadline day ({deadline.isoformat()}); "
                         f"the state must say the last day counts (e.g. 'up to and including')")
        ctx.set(f"deadline:{name}", deadline)
        ctx.set(f"open:{name}", is_open)
        ctx.set(f"elapsed:{name}", Decimal(elapsed))
    eval_derived(params.get("derived"), ctx)
    eval_outcome(params.get("outcome_rules"), ctx)


def env_hop(params, ctx):
    """FR-HOP. vars, derived, conditions [{id, test: P}] (the policy's listed conditions, in order),
    waivers [{id, waives: [condition ids], when: P, unless: P}] (a clause that switches a condition off).
    env: met:<c>, waived:<c>, satisfied:<c> (met or waived), waiver:<w>, conditions_met (count of met),
         conditions_satisfied, n_conditions, all_met, all_satisfied, unmet (list of ids), outcome.
    Conditions are evaluated in order, so a condition may refer to met:<earlier id> (clause A refers to B)."""
    load_vars(params, ctx)
    eval_derived(params.get("derived"), ctx)
    conds = params.get("conditions")
    if not isinstance(conds, list) or len(conds) < 2:
        raise SpecError("conditions: need a list of at least 2 conditions")
    ids = []
    for i, c in enumerate(conds):
        cid = c.get("id")
        if not isinstance(cid, str) or not cid or cid in ids:
            raise SpecError(f"conditions[{i}]: needs a unique id")
        ids.append(cid)
        ctx.set(f"met:{cid}", eval_pred(c.get("test"), ctx, f"conditions[{i}].test"))
    waived = {cid: False for cid in ids}
    for i, w in enumerate(params.get("waivers", []) or []):
        wid = w.get("id")
        if not isinstance(wid, str) or not wid:
            raise SpecError(f"waivers[{i}]: needs an id")
        targets = w.get("waives")
        if not isinstance(targets, list) or not targets or any(t not in waived for t in targets):
            raise SpecError(f"waivers[{i}]: 'waives' must list existing condition ids")
        active = eval_pred(w.get("when"), ctx, f"waivers[{i}].when")
        if w.get("unless") is not None:
            active = active and not eval_pred(w["unless"], ctx, f"waivers[{i}].unless")
        ctx.set(f"waiver:{wid}", active)
        for t in targets:
            waived[t] = waived[t] or active
    met = [ctx.env[f"met:{c}"] for c in ids]
    for cid in ids:
        ctx.set(f"waived:{cid}", waived[cid])
        ctx.set(f"satisfied:{cid}", ctx.env[f"met:{cid}"] or waived[cid])
    sat = [ctx.env[f"satisfied:{c}"] for c in ids]
    ctx.set("n_conditions", Decimal(len(ids)))
    ctx.set("conditions_met", Decimal(sum(met)))
    ctx.set("conditions_satisfied", Decimal(sum(sat)))
    ctx.set("all_met", all(met))
    ctx.set("all_satisfied", all(sat))
    ctx.set("unmet", [c for c, s in zip(ids, sat) if not s])
    eval_outcome(params.get("outcome_rules"), ctx)


def _remark_value(r, attr):
    if attr in r:
        return r[attr]
    if attr in LIT_REMARK_DEFAULTS:
        return LIT_REMARK_DEFAULTS[attr]
    return None


def env_lit(params, ctx):
    """FR-LIT. aspects [{name, remarks: [{polarity: pos|neg|neutral, severity: none|cosmetic|minor|major,
    resolved: bool, speaker: reviewer|other, topic: str}]}], filters {name: {attr: [allowed values]}}
    (a filter defines what counts as a complaint; it must admit only polarity "neg").
    env: mentioned:<a>, praise:<a> (a positive remark by the reviewer), complaint:<F>:<a>,
         stance:<F>:<a> in {complaint, praise only, neutral mention, not mentioned}, complaint_count:<F>,
         praise_count, n_aspects."""
    load_vars(params, ctx)
    filters = params.get("filters")
    if not isinstance(filters, dict) or not filters:
        raise SpecError("filters: need at least one complaint definition")
    for fname, flt in filters.items():
        if not re.fullmatch(r"[A-Z]", fname):
            raise SpecError(f"filters: name {fname!r} must be one capital letter (A, B, ...)")
        if not isinstance(flt, dict) or flt.get("polarity") != ["neg"]:
            raise SpecError(f"filters.{fname}: must contain \"polarity\": [\"neg\"] (a complaint is a negative remark)")
        for attr, allowed in flt.items():
            if not isinstance(allowed, list) or not allowed:
                raise SpecError(f"filters.{fname}.{attr}: must be a non-empty list of allowed values")
            if attr in LIT_REMARK_ATTRS and any(a not in LIT_REMARK_ATTRS[attr] for a in allowed):
                raise SpecError(f"filters.{fname}.{attr}: values must be in {LIT_REMARK_ATTRS[attr]}")
            if attr == "resolved" and any(not isinstance(a, bool) for a in allowed):
                raise SpecError(f"filters.{fname}.resolved: values must be true/false")
    aspects = params.get("aspects")
    if not isinstance(aspects, list) or len(aspects) < 2:
        raise SpecError("aspects: need at least 2 aspects")
    names = []
    counts = {f: 0 for f in filters}
    praise_n = 0
    for i, a in enumerate(aspects):
        name = a.get("name")
        if not isinstance(name, str) or not name or ":" in name or name in names:
            raise SpecError(f"aspects[{i}]: needs a unique name without ':'")
        names.append(name)
        rems = a.get("remarks", [])
        if not isinstance(rems, list):
            raise SpecError(f"aspects[{i}].remarks must be a list")
        for j, r in enumerate(rems):
            if not isinstance(r, dict) or r.get("polarity") not in LIT_REMARK_ATTRS["polarity"]:
                raise SpecError(f"aspects[{i}].remarks[{j}]: polarity must be pos, neg or neutral")
            for attr, allowed in LIT_REMARK_ATTRS.items():
                if attr in r and r[attr] not in allowed:
                    raise SpecError(f"aspects[{i}].remarks[{j}].{attr}: must be one of {allowed}")
            if "resolved" in r and not isinstance(r["resolved"], bool):
                raise SpecError(f"aspects[{i}].remarks[{j}].resolved must be true/false")
            if r["polarity"] == "neg" and "severity" not in r:
                raise SpecError(f"aspects[{i}].remarks[{j}]: a negative remark needs a severity")
        mentioned = len(rems) > 0
        praise = any(r["polarity"] == "pos" and _remark_value(r, "speaker") == "reviewer" for r in rems)
        praise_n += praise
        ctx.set(f"mentioned:{name}", mentioned)
        ctx.set(f"praise:{name}", praise)
        for fname, flt in filters.items():
            comp = any(all(_remark_value(r, attr) in allowed for attr, allowed in flt.items()) for r in rems)
            counts[fname] += comp
            stance = ("complaint" if comp else "praise only" if praise else
                      "neutral mention" if mentioned else "not mentioned")
            ctx.set(f"complaint:{fname}:{name}", comp)
            ctx.set(f"stance:{fname}:{name}", stance)
            ctx.domains[f"stance:{fname}:{name}"] = list(STANCE_KEYS)
    for fname in filters:
        ctx.set(f"complaint_count:{fname}", Decimal(counts[fname]))
    ctx.set("praise_count", Decimal(praise_n))
    ctx.set("n_aspects", Decimal(len(names)))
    eval_derived(params.get("derived"), ctx)
    if params.get("outcome_rules") is not None:
        raise SpecError("FR-LIT does not use outcome_rules (its Choice is the stance of one aspect)")


def domain_of(address):
    return address.split("@")[-1].strip().lower().rstrip(".")


def under_domain(d, known):
    d, known = d.lower(), known.lower()
    return d == known or d.endswith("." + known)


def safe_domain(d):
    return d.lower().rstrip(".").split(".")[-1] in PHISH_SAFE_TLDS


def env_phish(params, ctx):
    """FR-PHISH. known_domains [..] (the sender identity the reader can check; stated in the state),
    email {from_domain, reply_to_domain (opt), link_domains [..]}, signs {each declared sign: bool},
    purpose (what a genuine email of this kind is for; see PHISH_PURPOSE).
    Derived signs: sender_mismatch, link_mismatch, reply_to_mismatch (domain not equal to / under a known domain).
    impersonation = any derived sign; harmful_request = asks_secret or unusual_payment or asks_personal_data or
    unexpected_attachment. category = phishing iff impersonation and harmful_request; otherwise
    PHISH_PURPOSE[purpose]. An email with exactly one of the two is rejected as an ambiguous look-alike.
    env: every sign, impersonation, harmful_request, sign_count (all 12 signs), category, purpose."""
    load_vars(params, ctx)
    known = params.get("known_domains")
    if not isinstance(known, list) or not known:
        raise SpecError("known_domains: need at least one domain the reader can check the sender against")
    email = params.get("email") or {}
    frm = email.get("from_domain")
    links = email.get("link_domains", []) or []
    reply = email.get("reply_to_domain")
    all_domains = list(known) + ([frm] if frm else []) + list(links) + ([reply] if reply else [])
    if not frm:
        raise SpecError("email.from_domain is required")
    for d in all_domains:
        if not isinstance(d, str) or not re.fullmatch(r"[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?", d.lower()):
            raise SpecError(f"invalid domain {d!r}")
        if not safe_domain(d):
            raise SpecError(f"domain {d!r} must end in .example or .test (safety rule)")
    ctx.set("sender_mismatch", not any(under_domain(frm, k) for k in known))
    ctx.set("link_mismatch", any(not any(under_domain(ld, k) for k in known) for ld in links))
    ctx.set("reply_to_mismatch", bool(reply) and not any(under_domain(reply, k) for k in known))
    signs = params.get("signs") or {}
    missing = [s for s in PHISH_DECLARED_SIGNS if s not in signs]
    extra = [s for s in signs if s not in PHISH_DECLARED_SIGNS]
    if missing or extra:
        raise SpecError(f"signs: declare every sign as true/false; missing {missing}, unknown {extra} "
                        f"(sender/link/reply-to mismatch are derived from the email domains)")
    for s in PHISH_DECLARED_SIGNS:
        if not isinstance(signs[s], bool):
            raise SpecError(f"signs.{s}: must be true or false")
        ctx.set(s, signs[s])
    imp = any(ctx.env[s] for s in PHISH_IMPERSONATION)
    harm = any(ctx.env[s] for s in PHISH_HARMFUL)
    if imp != harm:
        raise SpecError("ambiguous look-alike: a phishing email must show an impersonation sign AND a harmful "
                        "request; a genuine email must show neither (impersonation=%s, harmful_request=%s)"
                        % (imp, harm))
    purpose = params.get("purpose")
    if purpose not in PHISH_PURPOSE:
        raise SpecError(f"purpose must be one of {sorted(PHISH_PURPOSE)}")
    ctx.set("impersonation", imp)
    ctx.set("harmful_request", harm)
    ctx.set("sign_count", Decimal(sum(ctx.env[s] for s in PHISH_SIGNS)))
    ctx.set("purpose", purpose)
    ctx.set("category", "phishing" if imp and harm else PHISH_PURPOSE[purpose])
    ctx.domains["category"] = list(PHISH_KEYS)
    eval_derived(params.get("derived"), ctx)
    if params.get("outcome_rules") is not None:
        raise SpecError("FR-PHISH does not use outcome_rules (category is fixed by the phishing rule)")


def env_hneg(params, ctx):
    """FR-HNEG. request_types [keys], segments in reading order:
    {id, speaker: customer|third_party|agent_note|system, act, type, targets}
    customer acts: request (adds type), withdraw (removes the targeted earlier requests), replace (withdraw
    targets, then add type), decline (says they do NOT want type; also removes targeted requests), info.
    third_party / agent_note / system acts: suggest (type), claim (type), info. They never change the request.
    final_request = the one active customer request type, or "none of these" (more than one active is an error).
    env: final_request, active:<t>, ever_requested:<t>, withdrawn:<t>, declined:<t>, suggested_by_other:<t>,
         mentioned:<t> (requested, declined or suggested), tempting:<t> (mentioned but not final), n_requests."""
    load_vars(params, ctx)
    types = params.get("request_types")
    if not isinstance(types, list) or len(types) < 2 or len(set(types)) != len(types):
        raise SpecError("request_types: need at least 2 distinct request type keys")
    if NONE_KEY in types:
        raise SpecError(f"request_types must not include {NONE_KEY!r} (it is added automatically)")
    segs = params.get("segments")
    if not isinstance(segs, list) or len(segs) < 2:
        raise SpecError("segments: need at least 2 segments")
    active = {}  # segment id -> type
    seen_ids, cust_requests = [], {}
    ever, withdrawn, declined, suggested = set(), set(), set(), set()
    n_requests = 0
    for i, s in enumerate(segs):
        path = f"segments[{i}]"
        sid, spk, act, typ = s.get("id"), s.get("speaker"), s.get("act"), s.get("type")
        if not isinstance(sid, str) or not sid or sid in seen_ids:
            raise SpecError(f"{path}: needs a unique id")
        seen_ids.append(sid)
        if spk not in HNEG_SPEAKERS:
            raise SpecError(f"{path}: speaker must be one of {HNEG_SPEAKERS}")
        allowed = HNEG_CUSTOMER_ACTS if spk == "customer" else HNEG_OTHER_ACTS
        if act not in allowed:
            raise SpecError(f"{path}: act {act!r} not allowed for speaker {spk!r} (allowed: {allowed})")
        needs_type = act in ("request", "replace", "decline", "suggest", "claim")
        if needs_type and typ not in types:
            raise SpecError(f"{path}: type must be one of request_types, got {typ!r}")
        if not needs_type and typ is not None:
            raise SpecError(f"{path}: act {act!r} takes no type")
        targets = s.get("targets", []) or []
        if act in ("withdraw", "replace"):
            if not targets:
                raise SpecError(f"{path}: {act} needs 'targets' (earlier customer request segment ids)")
        for t in targets:
            if t not in cust_requests:
                raise SpecError(f"{path}: target {t!r} is not an earlier customer request")
        if spk == "customer":
            if act in ("withdraw", "replace", "decline"):
                for t in targets:
                    if t in active:
                        withdrawn.add(active.pop(t))
            if act in ("request", "replace"):
                active[sid] = typ
                cust_requests[sid] = typ
                ever.add(typ)
                n_requests += 1
            if act == "decline":
                declined.add(typ)
                for k in [k for k, v in active.items() if v == typ]:
                    withdrawn.add(active.pop(k))
        else:
            if act in ("suggest", "claim"):
                suggested.add(typ)
    final_types = set(active.values())
    if len(final_types) > 1:
        raise SpecError(f"more than one active customer request at the end ({sorted(final_types)}); FR-HNEG items "
                        f"must end with exactly one request (or none)")
    final = next(iter(final_types)) if final_types else NONE_KEY
    ctx.set("final_request", final)
    ctx.domains["final_request"] = list(types) + [NONE_KEY]
    ctx.set("n_requests", Decimal(n_requests))
    for t in types:
        ctx.set(f"active:{t}", t == final)
        ctx.set(f"ever_requested:{t}", t in ever)
        ctx.set(f"withdrawn:{t}", t in withdrawn and t != final)
        ctx.set(f"declined:{t}", t in declined)
        ctx.set(f"suggested_by_other:{t}", t in suggested)
        mentioned = t in ever or t in declined or t in suggested
        ctx.set(f"mentioned:{t}", mentioned)
        ctx.set(f"tempting:{t}", mentioned and t != final)
    eval_derived(params.get("derived"), ctx)
    if params.get("outcome_rules") is not None:
        raise SpecError("FR-HNEG does not use outcome_rules (the Choice is the final request)")


FAMILY_ENV = {"FR-NUM": env_num, "FR-DATE": env_date, "FR-HOP": env_hop, "FR-LIT": env_lit,
              "FR-PHISH": env_phish, "FR-HNEG": env_hneg}


# ---------------------------------------------------------------------------------------------------------
# question resolution
# ---------------------------------------------------------------------------------------------------------
def resolve_score(q, ctx, path):
    asks = q.get("asks", {})
    s = asks.get("score")
    levels = q.get("levels")
    K = q.get("K")
    if not isinstance(levels, list) or K not in (4, 7) or len(levels) != K:
        raise SpecError(f"{path}: a Score needs K in {{4, 7}} and exactly K levels (low -> high)")
    if not isinstance(s, dict):
        raise SpecError(f"{path}: asks.score must be an object")
    kind = s.get("kind")
    if kind == "count":
        preds = s.get("preds")
        if not isinstance(preds, list) or len(preds) != K - 1:
            raise SpecError(f"{path}: a count Score with K={K} needs exactly {K - 1} predicates (one per listed item)")
        level = sum(1 for i, p in enumerate(preds) if eval_pred(p, ctx, f"{path}.asks.score.preds[{i}]"))
    elif kind == "var":
        v = ctx.get(s.get("var"))
        if not isinstance(v, Decimal) or v != v.to_integral_value():
            raise SpecError(f"{path}: Score var {s.get('var')!r} must be a whole number")
        level = int(v)
    elif kind == "bins":
        v = ctx.get(s.get("var"))
        bounds = [_coerce_like(b, v, path) for b in (s.get("bounds") or [])]
        if len(bounds) != K - 1 or any(_kind(b) != _kind(v) for b in bounds) or bounds != sorted(bounds) \
                or len(set(bounds)) != len(bounds):
            raise SpecError(f"{path}: bins need {K - 1} strictly ascending bounds of the variable's type")
        closed = s.get("closed", "lower")
        if closed not in ("lower", "upper"):
            raise SpecError(f"{path}: closed must be 'lower' (a value equal to a bound moves up) or 'upper'")
        if v in bounds:
            ctx.warn(f"boundary: Score {path} value {fmt(v)} equals a bin bound; the level texts must say "
                     f"which level an exact value falls in")
        level = sum(1 for b in bounds if (v >= b if closed == "lower" else v > b))
    elif kind == "map":
        v = ctx.get(s.get("var"))
        mp = s.get("map")
        if not isinstance(mp, dict) or fmt(v) not in mp:
            raise SpecError(f"{path}: map has no level for value {fmt(v)!r}")
        dom = ctx.domains.get(s.get("var"))
        if dom:
            missing = [d for d in dom if d not in mp]
            if missing:
                raise SpecError(f"{path}: map must give a level for every possible value; missing {missing}")
        level = mp[fmt(v)]
        if not isinstance(level, int) or isinstance(level, bool):
            raise SpecError(f"{path}: map levels must be integers")
    else:
        raise SpecError(f"{path}: score kind must be count, var, bins or map")
    if not 0 <= level < K:
        raise SpecError(f"{path}: computed level {level} is outside 0..{K - 1}")
    return level


def resolve_choice(q, ctx, family, path):
    asks = q.get("asks", {})
    var = asks.get("choice_var")
    options = q.get("options")
    if not isinstance(options, dict) or len(options) < 2:
        raise SpecError(f"{path}: a Choice needs at least 2 options")
    if family == "FR-LIT":
        if not (isinstance(var, str) and var.startswith("stance:")):
            raise SpecError(f"{path}: FR-LIT q3 must ask choice_var 'stance:<filter>:<aspect>'")
    elif var != CHOICE_VAR[family]:
        raise SpecError(f"{path}: {family} q3 must ask choice_var {CHOICE_VAR[family]!r}")
    value = ctx.get(var)
    mapping = asks.get("value_to_key") or {}
    dom = ctx.domains.get(var)
    if dom is None:
        raise SpecError(f"{path}: {var!r} is not a categorical variable")
    keys = [mapping.get(d, d) for d in dom]
    missing = [k for k in keys if k not in options]
    if missing:
        raise SpecError(f"{path}: the option set is not exhaustive; possible values without an option: {missing}")
    dead = [k for k in options if k not in keys]
    if dead:
        ctx.warn(f"{path}: options that no rule can make gold (distractor-only): {dead}")
    return mapping.get(value, value)


def compute(spec):
    """Evaluate a spec. Returns (gold {slot: value}, ctx). Raises SpecError if gold cannot be computed."""
    family = spec.get("family")
    if family not in FAMILY_ENV:
        raise SpecError(f"family must be one of {FAMILIES}")
    params = spec.get("parameters")
    if not isinstance(params, dict):
        raise SpecError("parameters must be an object")
    ctx = Ctx()
    FAMILY_ENV[family](params, ctx)
    qs = {}
    for q in spec.get("questions", []) or []:
        slot = q.get("slot")
        if slot in qs:
            raise SpecError(f"slot {slot} appears twice")
        qs[slot] = q
    for s in ("q1", "q2", "q3", "q4", "q5"):
        if s not in qs:
            raise SpecError(f"missing question {s}")
    gold = {}
    gold["q3"] = resolve_choice(qs["q3"], ctx, family, "q3")
    lstar = qs["q1"].get("asks", {}).get("choice_is")
    if lstar not in (qs["q3"].get("options") or {}):
        raise SpecError(f"q1: asks.choice_is {lstar!r} must be one of q3's option keys (L* of Q1 is a Choice option)")
    gold["q1"] = int(gold["q3"] == lstar)
    q2 = qs["q2"]
    if q2.get("type") == "score":
        gold["q2"] = resolve_score(q2, ctx, "q2")
    else:
        pred = q2.get("asks", {}).get("pred")
        if pred is None:
            raise SpecError("q2: a Noul q2 must ask a predicate ('pred')")
        gold["q2"] = int(eval_pred(pred, ctx, "q2.asks.pred"))
    if qs["q4"].get("asks") != {"negation_of": "q1"}:
        raise SpecError("q4: asks must be {\"negation_of\": \"q1\"}")
    if qs["q5"].get("asks") != {"paraphrase_of": "q1"}:
        raise SpecError("q5: asks must be {\"paraphrase_of\": \"q1\"}")
    gold["q4"] = 1 - gold["q1"]
    gold["q5"] = gold["q1"]
    if "q7" in qs:
        gold["q7"] = resolve_score(qs["q7"], ctx, "q7")
    return {s: gold[s] for s in SLOTS if s in gold}, ctx


def compute_gold(spec):
    return compute(spec)[0]


# ---------------------------------------------------------------------------------------------------------
# text checks: free variants, forbidden forms, safety, length
# ---------------------------------------------------------------------------------------------------------
TOKEN_RE = re.compile(r"[a-z0-9]+(?:'[a-z]+)?")


def tokens(s):
    return set(TOKEN_RE.findall((s or "").lower().replace("’", "'").replace("‘", "'")))


def jaccard(a, b):
    u = a | b
    return len(a & b) / len(u) if u else 0.0


# Template-like phrasings: the AFF/NEG/QN examples of DESIGN 6.1 (all pools), the forbidden negative-polar
# forms, and generic frames any template bank is likely to contain. Scoped variants are generated below.
BUILTIN_TEMPLATES = [
    ("AFF-F1", "Is it the case that {p}?"), ("AFF-F2", "Does the {doc} indicate that {p}?"),
    ("AFF-F3", "Statement: '{p}'. Is this true of the {doc}?"),
    ("AFF-F4", "Would a careful reader of the {doc} conclude that {p}?"), ("AFF-F5", "Decide whether {p}."),
    ("AFF-F6", "Answer yes if {p}; otherwise answer no."), ("AFF-F7", "Based only on the {doc}, is it accurate that {p}?"),
    ("AFF-F8", "Here is a claim about the {doc}: {p}. Does the claim hold?"), ("AFF-F9", "Should we record that {p}?"),
    ("NEG-C2a", "Is it false that {p}?"), ("NEG-C2b", "Is it not the case that {p}?"),
    ("NEG-C4a", "Would it be inaccurate to say that {p}?"), ("NEG-C4b", "Is the claim that {p} incorrect?"),
    ("NEG-C4c", "Would it be wrong to say that {p}?"), ("NEG-C5a", "Would someone who says that {p} be mistaken?"),
    ("NEG-C5b", "Would a reader who concluded that {p} be misreading the {doc}?"),
    ("NEG-C5s", "Would a reader who concluded from the {doc} that {p} be misreading it?"),
    ("NEG-C6", "Is the {agent} asking about something other than {np}?"),
    ("NEG-C7", "Should the statement that {p} be rejected?"),
    ("QN-QA", "Based on the passage, is the answer to '{q}' no?"), ("QN-QJ", "Would answering yes to '{q}' be a mistake?"),
    ("QN-QM", "Would someone who answered yes to '{q}' be wrong?"),
    ("QN-QMs", "Would someone who answered yes to '{q}', using only the passage, be wrong?"),
    ("FORBID-NP1", "Isn't it true that {p}?"), ("FORBID-NP2", "Is it not true that {p}?"),
    ("GEN-1", "Is it true that {p}?"), ("GEN-2", "Is it correct that {p}?"), ("GEN-3", "Is it untrue that {p}?"),
    ("GEN-4", "Is it incorrect that {p}?"), ("GEN-5", "Is it accurate to say that {p}?"),
    ("GEN-6", "Would it be correct to say that {p}?"), ("GEN-7", "Would it be true to say that {p}?"),
    ("GEN-8", "Would it be false to say that {p}?"), ("GEN-9", "Can we conclude that {p}?"),
    ("GEN-10", "Does the {doc} show that {p}?"), ("GEN-11", "Does the {doc} say that {p}?"),
    ("GEN-12", "True or false: {p}?"), ("GEN-13", "Is the statement '{p}' true?"),
    ("GEN-14", "Is the statement '{p}' false?"), ("GEN-15", "Would it be a mistake to say that {p}?"),
]
BUILTIN_SCOPES = ["According to the {doc}", "Based only on the {doc}", "Going by the {doc}"]


def _lower_first(s):
    return s[:1].lower() + s[1:] if s else s


def load_template_bank(root=ROOT):
    """Built-in phrasings + every template in assets/templates/{aff,neg,qn,qf,scope}.jsonl that exists.
    Returns [(template_id, template_text)] including scoped forms. Only ids are ever printed."""
    bank = list(BUILTIN_TEMPLATES)
    scopes = list(BUILTIN_SCOPES)
    tdir = Path(root) / "assets" / "templates"
    for name in ("aff", "neg", "qn", "qf", "scope"):
        f = tdir / f"{name}.jsonl"
        if not f.exists():
            continue
        for n, line in enumerate(f.read_text(encoding="utf-8").splitlines()):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            tid = row.get("template_id") or row.get("id") or f"{name}:{n}"
            for field in ("template", "text", "body", "frame", "wording", "phrase", "scope"):
                t = row.get(field)
                if isinstance(t, str) and t.strip():
                    if name == "scope":
                        scopes.append(t.strip().rstrip(","))
                    else:
                        bank.append((str(tid), t))
                    break
    out = list(bank)
    for tid, t in bank:
        if t.startswith("{Scope}"):
            continue
        for k, sc in enumerate(scopes):
            out.append((f"{tid}+scope{k}", f"{sc}, {_lower_first(t)}"))
    return out


def _render(t, slots):
    return re.sub(r"\{(\w+)\}", lambda m: slots.get(m.group(1), " "), t)


def free_variant_score(text, spec, bank, scope_phrase=None):
    """Max token Jaccard between an authored free variant and any template-like phrasing. Two views:
    (a) the template filled with this item's own slots (p, negP, doc, agent, q, np) vs the full question;
    (b) the template's frame words vs the question's frame words (slot words removed from both).
    The scope phrase declared for the question is removed first. Returns (score, template_id)."""
    q1 = next((q for q in spec.get("questions", []) if q.get("slot") == "q1"), {}) or {}
    prop = q1.get("proposition") or {}
    p, negp = prop.get("p", ""), prop.get("negP", "")
    body = text or ""
    if scope_phrase:
        body = re.sub(re.escape(scope_phrase), " ", body, flags=re.I)
    q_all = tokens(body)
    slot_toks = tokens(" ".join([p, negp, spec.get("doc", ""), spec.get("agent", "")]))
    q_core = q_all - slot_toks
    best, best_id = 0.0, None
    for tid, t in bank:
        for fill in (p, negp):
            slots = {"p": fill, "negP": negp, "doc": spec.get("doc", ""), "agent": spec.get("agent", ""),
                     "np": fill, "q": q1.get("instructions", ""), "Scope": ""}
            j = jaccard(q_all, tokens(_render(t, slots)))
            if j > best:
                best, best_id = j, tid
        skel = tokens(re.sub(r"\{\w+\}", " ", t)) - slot_toks
        if skel and q_core:
            j = jaccard(q_core, skel)
            if j > best:
                best, best_id = j, tid
    return round(best, 4), best_id


LEAD = r"^\s*(?:[^,?]{0,80},\s*)?"
NEG_POLAR_RE = re.compile(LEAD + r"(?:isn't|aren't|wasn't|weren't|doesn't|don't|didn't|hasn't|haven't|hadn't|"
                                  r"can't|couldn't|won't|wouldn't|shouldn't|mustn't)\b", re.I)
NOT_TRUE_RE = re.compile(r"\bnot\s+true\s+that\b", re.I)
AUX_NOT_RE = re.compile(LEAD + r"(?:is|are|was|were|does|do|did|has|have|can|could|will|would|should)\s+"
                               r"(?:\w+\s+){1,3}not\b", re.I)
EPISTEMIC_RE = re.compile(r"\b(?:no (?:indication|evidence|sign|mention|record)|not (?:mentioned|stated|indicated|"
                          r"clear|specified)|(?:doesn't|does not|didn't|did not) (?:say|mention|state|indicate)|"
                          r"unclear|unknown|can't tell|cannot tell|impossible to tell)\b", re.I)


def question_form_issues(text, role):
    """Returns (errors, warnings) for forbidden question forms (DESIGN 6.1 'Forbidden')."""
    errs, warns = [], []
    if NEG_POLAR_RE.search(text) or NOT_TRUE_RE.search(text):
        errs.append("negative-polar form (\"Isn't ...\", \"... not true that ...\") is forbidden")
    elif AUX_NOT_RE.search(text):
        warns.append("question of the form 'Aux + subject + not ...' reads as biased; prefer a positive frame "
                     "with a negated or opposite predicate")
    if EPISTEMIC_RE.search(text):
        (errs if role == "free_negation" else warns).append(
            "epistemic form ('no indication', 'not mentioned', 'unclear', ...) is not a complement")
    return errs, warns


EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@((?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,})")
URL_RE = re.compile(r"\b(?:https?://|www\.)([A-Za-z0-9.-]+)", re.I)
DOMAIN_RE = re.compile(r"(?<![@\w.-])((?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?\.)+([A-Za-z]{2,24}))\b")
REAL_TLDS = {"com", "net", "org", "io", "co", "uk", "us", "ca", "au", "de", "fr", "in", "info", "biz", "gov",
             "edu", "mil", "ly", "me", "app", "xyz", "online", "site", "shop", "store", "bank", "support",
             "link", "click", "top", "live", "zip", "mov", "ai", "tv", "cc", "eu", "ie", "nz", "es", "it", "nl",
             "ru", "cn", "jp", "br", "mx", "za", "ch", "se", "no", "dk", "fi", "pl", "be", "at", "sg", "hk",
             "tech", "cloud", "email", "services", "center", "company", "group", "help", "security", "pay",
             "travel", "insurance", "energy", "mobile", "phone", "tel", "fyi", "page", "dev", "web", "net.au",
             "co.uk"}
PHONE_RE = re.compile(r"(?<![\w-])(?:\+?1[ .-]?)?(?:\(\d{3}\)[ .-]?|\d{3}[ .-])?(\d{3})[ .-](\d{4})(?![\w-])")
LONG_DIGITS_RE = re.compile(r"(?<!\d)\d{7,}(?!\d)")
CARDLIKE_RE = re.compile(r"(?<!\d)(?:\d[ -]?){13,19}(?!\d)")
IBAN_RE = re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b")
CRYPTO_RE = re.compile(r"\b(?:bc1|0x)[A-Za-z0-9]{20,}\b")
IP_RE = re.compile(r"\b(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})\b")
DOC_IP_PREFIXES = ("192.0.2.", "198.51.100.", "203.0.113.")
REAL_BRANDS = [  # unambiguous real brands and agencies (case-insensitive): error
    "paypal", "amazon", "netflix", "verizon", "comcast", "xfinity", "geico", "allstate", "state farm", "expedia",
    "airbnb", "walmart", "costco", "best buy", "fedex", "usps", "dhl", "wells fargo", "bank of america",
    "citibank", "hsbc", "barclays", "mastercard", "venmo", "zelle", "cash app", "coinbase", "facebook",
    "instagram", "whatsapp", "microsoft", "gmail", "yahoo", "google", "vodafone", "t-mobile", "at&t", "pg&e",
    "con edison", "allianz", "axa", "aviva", "marriott", "hilton", "uber", "lyft", "ebay", "etsy", "shopify",
    "ikea", "home depot", "kroger", "tesco", "sainsbury", "lidl", "aldi", "united airlines", "american airlines",
    "southwest airlines", "ryanair", "easyjet", "lufthansa", "british airways", "hertz", "trivago",
    "liberty mutual", "metlife", "aetna", "cigna", "humana", "blue cross", "irs", "hmrc", "dvla",
    "social security administration", "dropbox", "docusign", "adobe", "linkedin", "tiktok", "samsung",
    "lenovo", "national grid", "british gas", "duke energy", "virgin media", "booking.com", "hotels.com",
    "apple pay", "google pay", "western union", "moneygram", "visa card", "chase bank", "capital one",
]
AMBIGUOUS_BRANDS = ["Apple", "Target", "Delta", "Orange", "Sprint", "Spectrum", "Chase", "Progressive",
                    "Nationwide", "Emirates", "Avis", "Kayak", "Zoom", "Sky", "Visa", "Outlook", "UPS",
                    "Prudential", "EDF", "Southwest"]  # case-sensitive: warning


def safety_scan(text, where):
    """Safety rules for all FR text (DESIGN 7; guidelines section 9). Returns (errors, warnings)."""
    errs, warns = [], []
    if not text:
        return errs, warns
    for m in EMAIL_RE.finditer(text):
        if not safe_domain(m.group(1)):
            errs.append(f"{where}: e-mail address domain {m.group(1)!r} must end in .example or .test")
    for m in URL_RE.finditer(text):
        host = m.group(1).rstrip(".")
        if not safe_domain(host):
            errs.append(f"{where}: URL host {host!r} must end in .example or .test")
    for m in DOMAIN_RE.finditer(text):
        dom, tld = m.group(1), m.group(2).lower()
        if tld in PHISH_SAFE_TLDS:
            continue
        if tld in REAL_TLDS or dom.lower().endswith((".co.uk", ".net.au")):
            errs.append(f"{where}: {dom!r} looks like a real domain; use .example or .test")
    for m in PHONE_RE.finditer(text):
        if not (m.group(1) == "555" and m.group(2).startswith("01")):
            errs.append(f"{where}: phone-like number {m.group(0).strip()!r}; phone numbers must be 555-01xx")
    for m in CARDLIKE_RE.finditer(text):
        if len(re.sub(r"\D", "", m.group(0))) >= 13:
            errs.append(f"{where}: {m.group(0).strip()!r} looks like a card or account number")
    for m in LONG_DIGITS_RE.finditer(text):
        warns.append(f"{where}: digit run {m.group(0)!r} (7+ digits) may read as a phone or account number; "
                     f"use letter-prefixed references such as 'KV-4471'")
    for rx, what in ((IBAN_RE, "IBAN-like string"), (CRYPTO_RE, "crypto wallet-like string")):
        for m in rx.finditer(text):
            errs.append(f"{where}: {what} {m.group(0)!r} is not allowed")
    for m in IP_RE.finditer(text):
        ip = m.group(0)
        if not ip.startswith(DOC_IP_PREFIXES):
            errs.append(f"{where}: IP address {ip!r} must be in a documentation range (192.0.2.x, 198.51.100.x, "
                        f"203.0.113.x)")
    low = text.lower()
    for b in REAL_BRANDS:
        if re.search(r"(?<![\w-])" + re.escape(b) + r"(?![\w-])", low):
            errs.append(f"{where}: real brand or agency name {b!r}; use fictional names")
    for b in AMBIGUOUS_BRANDS:
        if re.search(r"(?<![\w-])" + re.escape(b) + r"(?![\w-])", text):
            warns.append(f"{where}: {b!r} is also a real brand; make sure it is used as an ordinary word")
    return errs, warns


def word_count(text):
    return len((text or "").split())


def _num_variants(v):
    out = set()
    if isinstance(v, Decimal):
        out.add(format(v.normalize(), "f"))
        out.add(f"{v:.2f}")
        out.add(f"{v:,.2f}")
        if v == v.to_integral_value():
            out.add(f"{int(v):,}")
            out.add(str(int(v)))
    return {s for s in out if s}


def _appears_number(v, text):
    return any(re.search(r"(?<![\d.])" + re.escape(s) + r"(?![\d])", text) for s in _num_variants(v))


MONTHS = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December")


def _appears_date(d, text):
    if d.isoformat() in text:
        return True
    month = MONTHS[d.month - 1]
    has_month = re.search(r"\b(" + month + "|" + month[:3] + r")\b\.?", text) is not None
    has_day = re.search(r"(?<!\d)" + str(d.day) + r"(?:st|nd|rd|th)?(?!\d)", text) is not None
    numeric = re.search(r"(?<!\d)0?%d/0?%d(?!\d)" % (d.month, d.day), text) or \
        re.search(r"(?<!\d)0?%d/0?%d(?!\d)" % (d.day, d.month), text)
    return (has_month and has_day) or bool(numeric)


# ---------------------------------------------------------------------------------------------------------
# full spec check (program + bundle + card targets + text rules)
# ---------------------------------------------------------------------------------------------------------
def _schema_errors(spec, schema):
    try:
        import jsonschema  # noqa: F401
    except ImportError:
        return [], ["jsonschema not installed: schema validation skipped"]
    from jsonschema import Draft202012Validator
    v = Draft202012Validator(schema)
    errs = []
    for e in sorted(v.iter_errors(spec), key=lambda e: list(e.absolute_path)):
        loc = "/".join(str(x) for x in e.absolute_path) or "(root)"
        errs.append(f"schema: {loc}: {e.message[:200]}")
    return errs, []


def load_schema(path=HERE / "spec.schema.json"):
    p = Path(path)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def _key_ok(k):
    words = k.split()
    return 1 <= len(words) <= 5 and not (set(w.lower() for w in words) & BANNED_KEY_TOKENS)


def check_spec(spec, card=None, bank=None, schema=None):
    """Return {item_id, ok, errors, warnings, gold, free_variant_scores}. Never raises on a bad spec."""
    errors, warnings = [], []
    item = spec.get("item_id", "?")
    if schema is not None:
        e, w = _schema_errors(spec, schema)
        errors += e
        warnings += w
    gold, ctx = None, None
    try:
        gold, ctx = compute(spec)
        warnings += ctx.warnings
    except SpecError as e:
        errors.append(f"program: {e}")
    fam = spec.get("family")
    qs = {q.get("slot"): q for q in spec.get("questions", []) or [] if isinstance(q, dict)}
    order = [q.get("slot") for q in spec.get("questions", []) or [] if isinstance(q, dict)]
    expect = ["q1", "q2", "q3", "q4", "q5"] + (["q7"] if "q7" in qs else [])
    if order != expect:
        errors.append(f"bundle: questions must be {expect} in this order, got {order}")
    # ids, provenance
    code = FAMILY_CODES.get(fam, "?")
    m = re.fullmatch(r"fr:FR-([A-Z]+):(\d{3})", str(item))
    if not m or m.group(1) != code:
        errors.append(f"item_id {item!r} must be fr:{fam}:NNN")
    else:
        n = m.group(2)
        if spec.get("group_id") != f"g:fresh:{fam}:{n}":
            errors.append(f"group_id must be g:fresh:{fam}:{n}")
        if spec.get("card_id") != f"card:{fam}:{n}":
            errors.append(f"card_id must be card:{fam}:{n}")
    if spec.get("authored_by") not in AUTHORS:
        errors.append(f"authored_by must be one of {AUTHORS}")
    if spec.get("vertical") not in VERTICALS:
        errors.append(f"vertical must be one of {VERTICALS}")
    grounded = fam in GROUNDED
    if grounded and spec.get("scope") != "record":
        errors.append("scope must be 'record' on FR-NUM, FR-DATE and FR-HOP (R14)")
    if not grounded and spec.get("scope") is not None:
        errors.append("scope must be null outside FR-NUM, FR-DATE and FR-HOP")
    # per question
    for slot, q in qs.items():
        typ, role, instr = q.get("type"), q.get("role"), q.get("instructions") or ""
        want_type = {"q1": "noul", "q3": "choice", "q4": "noul", "q5": "noul", "q7": "score"}.get(slot)
        if want_type and typ != want_type:
            errors.append(f"{slot}: type must be {want_type}")
        want_role = {"q1": "base", "q3": "base", "q4": "free_negation", "q5": "free_paraphrase", "q7": "base"}.get(slot)
        if want_role and role != want_role:
            errors.append(f"{slot}: role must be {want_role}")
        if typ == "noul":
            crit = q.get("criteria")
            if not (isinstance(crit, dict) and isinstance(crit.get("true"), str) and isinstance(crit.get("false"), str)
                    and crit["true"].strip() and crit["false"].strip()):
                errors.append(f"{slot}: Noul needs authored criteria {{\"true\": ..., \"false\": ...}}")
            elif crit["true"].strip() == crit["false"].strip():
                errors.append(f"{slot}: criteria true and false must differ")
            if q.get("options") is not None or q.get("levels") is not None:
                errors.append(f"{slot}: a Noul has no options or levels")
        if typ == "choice":
            opts = q.get("options") or {}
            for k, d in opts.items():
                if k != NONE_KEY and not _key_ok(k):
                    errors.append(f"{slot}: option key {k!r} must be 1-5 words without yes/no/true/false/"
                                  f"correct/incorrect/cannot/other/none")
                if not isinstance(d, str) or len(d.split()) < 3:
                    errors.append(f"{slot}: option {k!r} needs a description of at least 3 words")
            if len({k.lower() for k in opts}) != len(opts):
                errors.append(f"{slot}: option keys must be distinct")
            if q.get("criteria") is not None:
                errors.append(f"{slot}: a Choice has no criteria")
        if typ == "score":
            levels = q.get("levels") or []
            if len({str(x).strip().lower() for x in levels}) != len(levels):
                errors.append(f"{slot}: level texts must be distinct")
        if typ in ("noul",) and slot in ("q1", "q4", "q5") and not instr.rstrip().endswith("?"):
            warnings.append(f"{slot}: instructions should be a question ending in '?'")
        # scope (R14)
        sp = q.get("scope_phrase")
        if grounded:
            if not sp or sp.lower() not in instr.lower():
                errors.append(f"{slot}: grounded family: declare scope_phrase and use it verbatim in the instructions")
        elif sp:
            errors.append(f"{slot}: scope_phrase is only used on FR-NUM, FR-DATE and FR-HOP")
        # forbidden forms
        if typ == "noul":
            e, w = question_form_issues(instr, role)
            errors += [f"{slot}: {x}" for x in e]
            warnings += [f"{slot}: {x}" for x in w]
        # safety on every authored string
        texts = [instr] + list((q.get("criteria") or {}).values()) + list((q.get("options") or {}).keys()) \
            + list((q.get("options") or {}).values()) + [str(x) for x in (q.get("levels") or [])]
        for t in texts:
            e, w = safety_scan(t, slot)
            errors += e
            warnings += w
    # q1 proposition (for the template-rendered q6)
    q1 = qs.get("q1", {})
    prop = q1.get("proposition") or {}
    if not (isinstance(prop.get("p"), str) and isinstance(prop.get("negP"), str) and prop["p"].strip()
            and prop["negP"].strip()):
        errors.append("q1: proposition {p, negP} is required (the build renders q6 from it)")
    else:
        if prop["p"].strip().lower() == prop["negP"].strip().lower():
            errors.append("q1: proposition negP must differ from p")
        if prop["p"].rstrip().endswith((".", "?")) or prop["negP"].rstrip().endswith((".", "?")):
            errors.append("q1: proposition p and negP are clauses without final punctuation")
        if prop["p"][:1].isupper() and not re.match(r"^[A-Z][a-z]+\s+[A-Z]|^I\b|^[A-Z]{2,}", prop["p"]):
            warnings.append("q1: proposition p should start lower-case unless it starts with a proper noun")
        for s in (q.get("scope_phrase") for q in qs.values()):
            if s and s.lower() in (prop["p"] + " " + prop["negP"]).lower():
                errors.append("q1: proposition p/negP must not contain the scope phrase (templates add it)")
    for slot in ("q1", "q2", "q4", "q5"):
        for k in ("proposition",):
            if slot != "q1" and qs.get(slot, {}).get(k) is not None:
                errors.append(f"{slot}: only q1 carries a proposition")
    # family bundle rules
    q2 = qs.get("q2", {})
    if fam == "FR-LIT":
        if q2.get("role") != "criteria_variant" or q2.get("type") != "noul":
            errors.append("q2: on FR-LIT q2 is the criteria variant (Noul, role criteria_variant)")
        else:
            if q2.get("instructions") != q1.get("instructions"):
                errors.append("q2: the criteria variant repeats q1's instructions verbatim")
            if q2.get("criteria") == q1.get("criteria"):
                errors.append("q2: the criteria variant needs different authored criteria")
            pred = q2.get("asks", {}).get("pred", {})
            var3 = qs.get("q3", {}).get("asks", {}).get("choice_var", "")
            m2 = re.fullmatch(r"complaint:([A-Z]):(.+)", str(pred.get("is_true", ""))) if isinstance(pred, dict) else None
            m3 = re.fullmatch(r"stance:([A-Z]):(.+)", str(var3))
            if not m2 or not m3 or m2.group(2) != m3.group(2) or m2.group(1) == m3.group(1) or set(pred) != {"is_true"}:
                errors.append("q2: FR-LIT criteria variant must ask {\"is_true\": \"complaint:<other filter>:<same "
                              "aspect as q3>\"}")
            if gold and gold.get("q2") == gold.get("q1"):
                errors.append("q2: criteria variant gold must differ from q1 gold (the criteria must move the boundary)")
        if q1.get("asks", {}).get("choice_is") != "complaint":
            errors.append("q1: on FR-LIT q1 asks choice_is 'complaint'")
        if set((qs.get("q3", {}).get("options") or {})) != set(STANCE_KEYS):
            errors.append(f"q3: FR-LIT option keys are exactly {list(STANCE_KEYS)}")
    else:
        if q2.get("role") != "base":
            errors.append("q2: role must be base")
        if q2.get("type") == "score" and fam != "FR-NUM":
            errors.append("q2: only FR-NUM Score states carry a Score in q2")
        if q2.get("type") == "score" and q2.get("K") != 4:
            errors.append("q2: the FR-NUM q2 Score has K = 4")
        if q2.get("type") not in ("noul", "score"):
            errors.append("q2: type must be noul (or score on FR-NUM Score states)")
    if fam == "FR-PHISH":
        if q1.get("asks", {}).get("choice_is") != "phishing":
            errors.append("q1: on FR-PHISH q1 asks choice_is 'phishing'")
        if list(qs.get("q3", {}).get("options") or {}) and set(qs["q3"]["options"]) != set(PHISH_KEYS):
            errors.append(f"q3: FR-PHISH option keys are exactly {list(PHISH_KEYS)}")
    if fam == "FR-HNEG":
        opts = set((qs.get("q3", {}).get("options") or {}))
        types = set((spec.get("parameters") or {}).get("request_types") or [])
        if opts != types | {NONE_KEY}:
            errors.append(f"q3: FR-HNEG options are the request_types plus {NONE_KEY!r}")
        if q1.get("asks", {}).get("choice_is") == NONE_KEY:
            errors.append(f"q1: L* must be a request type, not {NONE_KEY!r}")
    if fam in ("FR-NUM", "FR-DATE", "FR-HOP"):
        so = qs.get("q3", {}).get("scale_order")
        if not isinstance(so, list) or set(so) != set(qs.get("q3", {}).get("options") or {}) or len(so) != len(set(so)):
            errors.append("q3: scale_order must list every option key once, most to least favourable")
    q7 = qs.get("q7")
    if q7 is not None:
        if fam not in ("FR-LIT", "FR-HOP", "FR-PHISH"):
            errors.append("q7: only FR-LIT, FR-HOP and FR-PHISH carry a Q7 Score")
        K = q7.get("K")
        sc = (q7.get("asks") or {}).get("score") or {}
        if K == 7 and sc.get("kind") != "count" and not (fam == "FR-HOP" and sc.get("kind") == "var"
                                                         and sc.get("var") in ("conditions_met", "conditions_satisfied")):
            errors.append("q7: K = 7 scales are countable: use kind 'count' (or FR-HOP var conditions_met / "
                          "conditions_satisfied)")
        if fam in ("FR-HOP", "FR-PHISH") and K != 7:
            errors.append(f"q7: {fam} Q7 has K = 7")
        if fam == "FR-HOP" and ctx is not None and ctx.env.get("n_conditions") != Decimal(6):
            errors.append("q7: FR-HOP Q7 items list exactly 6 policy conditions")
        if fam == "FR-PHISH" and sc.get("kind") == "count":
            ids = [p.get("is_true") for p in sc.get("preds", []) if isinstance(p, dict)]
            if len(ids) != 6 or len(set(ids)) != 6 or any(i not in PHISH_SIGNS for i in ids) or \
                    any(set(p) != {"is_true"} for p in sc.get("preds", [])):
                errors.append("q7: FR-PHISH Q7 counts 6 distinct catalogue signs, each as {\"is_true\": sign}")
        levels = q7.get("levels") or []
        if K == 7 and levels and not re.search(r"\b(none|0|zero)\b", str(levels[0]).lower()):
            warnings.append("q7: level 0 of a count scale should read like 'none of the 6'")
    # free variants (DESIGN 7 step 4)
    fv = {}
    bank = bank if bank is not None else load_template_bank()
    for slot in ("q4", "q5"):
        q = qs.get(slot)
        if not q:
            continue
        score, tid = free_variant_score(q.get("instructions", ""), spec, bank, q.get("scope_phrase"))
        fv[slot] = {"max_jaccard": score, "nearest_template_id": tid}
        if score >= FREE_JACCARD_MAX:
            errors.append(f"{slot}: free variant is template-like (token Jaccard {score} >= {FREE_JACCARD_MAX} "
                          f"with template id {tid}); rephrase it in your own words")
    if qs.get("q5") and q1:
        j = jaccard(tokens(qs["q5"].get("instructions")), tokens(q1.get("instructions")))
        if j >= PARAPHRASE_COPY_WARN:
            warnings.append(f"q5: paraphrase is a near copy of q1 (token Jaccard {j:.2f})")
    if qs.get("q4") and q1 and (qs["q4"].get("instructions") or "").strip() == (q1.get("instructions") or "").strip():
        errors.append("q4: free negation repeats q1")
    # state
    state = spec.get("state")
    if state is None:
        warnings.append("state: not written yet (draft)")
    else:
        wc = word_count(state)
        lo, hi = LENGTH_BINS.get(spec.get("length_bin"), (60, 180))
        if not 60 <= wc <= 180:
            errors.append(f"state: {wc} words; states are 60-180 words")
        elif not lo <= wc <= hi:
            errors.append(f"state: {wc} words is outside the card's length bin {spec.get('length_bin')} ({lo}-{hi})")
        e, w = safety_scan(state, "state")
        errors += e
        warnings += w
        for slot, q in qs.items():
            if q.get("instructions") and q["instructions"].strip().lower() in state.lower():
                errors.append(f"state: contains the text of {slot}")
        if re.search(r"\b(gold|correct answer|the answer is|q[1-7])\b", state, re.I):
            warnings.append("state: contains annotation-like words (gold / answer / q1..q7)")
        params = spec.get("parameters") or {}
        if ctx is not None and fam == "FR-NUM":
            for it in params.get("line_items", []) or []:
                try:
                    if not _appears_number(to_dec(it.get("amount")), state):
                        warnings.append(f"state: line item amount {it.get('amount')} for {it.get('label')!r} not found")
                except SpecError:
                    pass
            tot = ctx.env.get("total")
            if isinstance(tot, Decimal) and len(params.get("line_items", []) or []) > 1 and _appears_number(tot, state):
                warnings.append("state: the computed total appears in the state; let the reader compute it")
        if ctx is not None and fam == "FR-DATE":
            if spec.get("complication") != "relative_date_expressions":
                for name in ["today"] + list((params.get("dates") or {}).keys()):
                    d = ctx.env.get("today" if name == "today" else f"date:{name}")
                    if isinstance(d, dt.date) and not _appears_date(d, state):
                        warnings.append(f"state: date {name} ({d.isoformat()}) not found in a recognisable form")
            if isinstance(ctx.env.get("today"), dt.date) and WEEKDAYS[ctx.env["today"].weekday()] not in state:
                warnings.append("state: state the weekday of 'today'")
        if fam == "FR-PHISH":
            for d in params.get("known_domains") or []:
                if d.lower() not in state.lower():
                    errors.append(f"state: known domain {d!r} must be stated so the reader can check the sender")
            fd = (params.get("email") or {}).get("from_domain")
            if fd and fd.lower() not in state.lower():
                warnings.append(f"state: from_domain {fd!r} not found in the state")
            for d in (params.get("email") or {}).get("link_domains") or []:
                if d.lower() not in state.lower():
                    warnings.append(f"state: link domain {d!r} not found in the state")
    for f in spec.get("facts", []) or []:
        e, w = safety_scan(f.get("statement", ""), f"facts.{f.get('id')}")
        errors += e
        warnings += w
    # card targets
    if card is not None and gold is not None:
        errors += card_mismatches(spec, card, gold, ctx)
    return {"item_id": item, "ok": not errors, "errors": errors, "warnings": warnings,
            "gold": gold, "free_variant_scores": fv}


def card_mismatches(spec, card, gold, ctx):
    errs = []
    for k in ("family", "vertical", "complication", "length_bin", "card_id", "group_id", "state_format"):
        if spec.get(k) != card.get(k):
            errs.append(f"card: {k} is {spec.get(k)!r}, card says {card.get(k)!r}")
    t = card.get("targets", {})
    qs = {q.get("slot"): q for q in spec.get("questions", [])}
    t1 = t.get("q1", {})
    if gold.get("q1") != t1.get("gold"):
        errs.append(f"card: q1 gold is {gold.get('q1')}, card target is {t1.get('gold')}")
    kind = t1.get("target_kind")
    lstar = qs.get("q1", {}).get("asks", {}).get("choice_is")
    g3 = gold.get("q3")
    if kind in ("adjacent_wrong", "non_adjacent_wrong"):
        so = qs.get("q3", {}).get("scale_order") or []
        if lstar in so and g3 in so:
            dist = abs(so.index(lstar) - so.index(g3))
            if kind == "adjacent_wrong" and dist != 1:
                errs.append(f"card: q1 target_kind adjacent_wrong needs L* next to the gold option in scale_order")
            if kind == "non_adjacent_wrong" and dist < 2:
                errs.append(f"card: q1 target_kind non_adjacent_wrong needs L* at least 2 steps from the gold option")
    if kind == "tempting_wrong" and ctx is not None and not ctx.env.get(f"tempting:{lstar}", False):
        errs.append("card: q1 target_kind tempting_wrong needs L* to be a request type the text mentions "
                    "(withdrawn, declined or suggested by someone else) that is not the final request")
    if kind == "other_wrong" and ctx is not None and spec.get("family") == "FR-HNEG" and ctx.env.get(f"tempting:{lstar}"):
        errs.append("card: q1 target_kind other_wrong needs L* to be a request type the text never mentions")
    if spec.get("family") == "FR-PHISH" and t.get("phish_category") and g3 != t.get("phish_category"):
        errs.append(f"card: q3 gold is {g3!r}, card category target is {t.get('phish_category')!r}")
    if spec.get("family") == "FR-LIT" and t.get("q3", {}).get("gold") and g3 != t["q3"]["gold"]:
        errs.append(f"card: q3 gold is {g3!r}, card target is {t['q3']['gold']!r}")
    t2 = t.get("q2", {})
    q2 = qs.get("q2", {})
    if t2.get("type") != q2.get("type"):
        errs.append(f"card: q2 type is {q2.get('type')!r}, card says {t2.get('type')!r}")
    elif t2.get("type") == "score":
        if q2.get("K") != t2.get("K") or gold.get("q2") != t2.get("level"):
            errs.append(f"card: q2 Score K={q2.get('K')} level={gold.get('q2')}, card says K={t2.get('K')} "
                        f"level={t2.get('level')}")
    elif gold.get("q2") != t2.get("gold"):
        errs.append(f"card: q2 gold is {gold.get('q2')}, card target is {t2.get('gold')}")
    n_opt = t.get("q3", {}).get("n_options")
    if n_opt and len(qs.get("q3", {}).get("options") or {}) != n_opt:
        errs.append(f"card: q3 has {len(qs.get('q3', {}).get('options') or {})} options, card says {n_opt}")
    t7 = t.get("q7")
    if t7 is None and "q7" in qs:
        errs.append("card: this card carries no Q7")
    if t7 is not None:
        if "q7" not in qs:
            errs.append("card: this card needs a Q7 Score")
        elif qs["q7"].get("K") != t7.get("K") or gold.get("q7") != t7.get("level"):
            errs.append(f"card: q7 K={qs['q7'].get('K')} level={gold.get('q7')}, card says K={t7.get('K')} "
                        f"level={t7.get('level')}")
    return errs


# ---------------------------------------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------------------------------------
def read_jsonl(path):
    rows = []
    for n, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise SystemExit(f"{path}:{n}: invalid JSON ({e})")
    return rows


def file_sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def cmd_check(args):
    specs = read_jsonl(args.specs)
    cards = {c["card_id"]: c for c in read_jsonl(args.cards)} if args.cards else {}
    schema = load_schema(args.schema) if args.schema else load_schema()
    bank = load_template_bank()
    n_err = n_warn = 0
    for spec in sorted(specs, key=lambda s: str(s.get("item_id"))):
        card = cards.get(spec.get("card_id")) if cards else None
        if cards and card is None:
            res = {"item_id": spec.get("item_id"), "ok": False, "errors": ["card: no such card_id"], "warnings": []}
        else:
            res = check_spec(spec, card=card, bank=bank, schema=schema)
        if not args.show_gold:
            res.pop("gold", None)
        n_err += bool(res["errors"])
        n_warn += bool(res["warnings"])
        print(json.dumps(res, ensure_ascii=False))
    print(f"checked {len(specs)} specs: {n_err} with errors, {n_warn} with warnings", file=sys.stderr)
    return 1 if n_err or (args.strict and n_warn) else 0


def cmd_gold(args):
    specs = read_jsonl(args.specs)
    out = []
    bad = 0
    for spec in sorted(specs, key=lambda s: str(s.get("item_id"))):
        try:
            g = compute_gold(spec)
        except SpecError as e:
            print(f"{spec.get('item_id')}: {e}", file=sys.stderr)
            bad += 1
            continue
        out.append({"item_id": spec["item_id"], "group_id": spec.get("group_id"), "family": spec.get("family"),
                    "gold": g, "rule_id": "R14_FRESH_SPEC", "program": PROGRAM_VERSION,
                    "program_sha256": file_sha256(__file__)})
    Path(args.out).write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in out),
                              encoding="utf-8")
    print(f"wrote {len(out)} gold rows to {args.out}; {bad} specs failed", file=sys.stderr)
    return 1 if bad else 0


def cmd_merge(args):
    rows, seen = [], {}
    for f in args.inputs:
        for r in read_jsonl(f):
            iid = r.get("item_id")
            if iid in seen:
                raise SystemExit(f"duplicate item_id {iid} in {f} and {seen[iid]}")
            seen[iid] = f
            rows.append(r)
    rows.sort(key=lambda r: str(r.get("item_id")))
    Path(args.out).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    print(f"merged {len(rows)} specs into {args.out}", file=sys.stderr)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("test", help="run the unit tests")
    c = sub.add_parser("check", help="validate specs (schema, gold program, bundle, card targets, text rules)")
    c.add_argument("specs")
    c.add_argument("--cards", default=None)
    c.add_argument("--schema", default=None)
    c.add_argument("--show-gold", action="store_true")
    c.add_argument("--strict", action="store_true", help="warnings also fail")
    g = sub.add_parser("gold", help="write computed gold as JSONL sorted by item_id")
    g.add_argument("specs")
    g.add_argument("--out", required=True)
    m = sub.add_parser("merge", help="merge per-author spec files into fresh_specs.jsonl (sorted by item_id)")
    m.add_argument("inputs", nargs="+")
    m.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    if args.cmd == "test":
        res = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(TestGold))
        return 0 if res.wasSuccessful() else 1
    return {"check": cmd_check, "gold": cmd_gold, "merge": cmd_merge}[args.cmd](args)


# ---------------------------------------------------------------------------------------------------------
# unit tests (fixtures are test data only: they are not FR items and their names and wording must not be
# reused in authored items)
# ---------------------------------------------------------------------------------------------------------
def _q(slot, typ, instr, asks, role="base", criteria=None, **kw):
    q = {"slot": slot, "role": role, "type": typ, "instructions": instr, "asks": asks}
    if typ == "noul":
        q["criteria"] = criteria or {"true": "Fixture yes case holds.", "false": "Fixture yes case does not hold."}
    q.update(kw)
    return q


def _base(family, n="901", vertical="retail", scope=None):
    return {"spec_version": SPEC_VERSION, "item_id": f"fr:{family}:{n}", "group_id": f"g:fresh:{family}:{n}",
            "card_id": f"card:{family}:{n}", "family": family, "vertical": vertical, "complication": "fixture",
            "length_bin": "medium", "state_format": "fixture", "authored_by": AUTHORS[0], "doc": "record",
            "agent": "customer", "scope": scope, "status": "draft",
            "facts": [{"id": "f1", "statement": "Fixture fact one."}, {"id": "f2", "statement": "Fixture fact two."}],
            "state": None, "rationale": "Unit-test fixture, not an FR item."}


def fx_num():
    s = _base("FR-NUM", scope="record")
    s["doc"] = "store record"
    s["parameters"] = {
        "currency": "USD",
        "line_items": [{"label": "lamp", "amount": 64.00}, {"label": "shade", "amount": 21.50, "qty": 2},
                       {"label": "delivery", "amount": 15, "counts": False}],
        "credits": [{"label": "coupon", "amount": 10}],
        "vars": {"has_receipt": True},
        "outcome_rules": [
            {"when": {"all": [{"is_true": "has_receipt"}, {"var": "total", "op": ">=", "value": 100}]},
             "outcome": "full refund"},
            {"when": {"is_true": "has_receipt"}, "outcome": "store credit"},
            {"outcome": "refund refused"}]}
    sp = "Going only by the store record"
    s["questions"] = [
        _q("q1", "noul", f"{sp}, does the purchase qualify for a full refund?", {"choice_is": "full refund"},
           scope_phrase=sp, proposition={"p": "the purchase qualifies for a full refund",
                                         "negP": "the purchase does not qualify for a full refund"}),
        _q("q2", "noul", f"{sp}, do the charges that do not count toward the threshold exceed $10?",
           {"pred": {"var": "excluded_total", "op": ">", "value": 10}}, scope_phrase=sp),
        {"slot": "q3", "role": "base", "type": "choice", "scope_phrase": sp,
         "instructions": f"{sp}, which remedy does the policy give for this purchase?",
         "options": {"full refund": "The whole counted amount goes back to the card.",
                     "store credit": "The amount is issued as a voucher for later use.",
                     "refund refused": "Nothing is returned for this purchase."},
         "scale_order": ["full refund", "store credit", "refund refused"], "asks": {"choice_var": "outcome"}},
        _q("q4", "noul", f"{sp}, would the shopper walk away with less than a full cash-back?",
           {"negation_of": "q1"}, role="free_negation", scope_phrase=sp),
        _q("q5", "noul", f"{sp}, can the shopper expect every counted dollar back on the card?",
           {"paraphrase_of": "q1"}, role="free_paraphrase", scope_phrase=sp),
    ]
    return s


def fx_date():
    s = _base("FR-DATE", scope="record")
    s["parameters"] = {
        "today": "2026-10-05", "dates": {"purchase": "2026-09-25", "delivery": "2026-09-29"},
        "holidays": ["2026-09-30"],
        "windows": [{"name": "return", "start": "purchase", "length": 7, "unit": "business_days"},
                    {"name": "cal10", "start": "purchase", "length": 10, "unit": "calendar_days"}],
        "outcome_rules": [{"when": {"is_true": "open:return"}, "outcome": "exchange allowed"},
                          {"outcome": "exchange refused"}]}
    sp = "Per the record"
    s["questions"] = [
        _q("q1", "noul", f"{sp}, is an exchange still allowed?", {"choice_is": "exchange allowed"}, scope_phrase=sp,
           proposition={"p": "an exchange is still allowed", "negP": "an exchange is no longer allowed"}),
        _q("q2", "noul", f"{sp}, did the delivery happen on a weekend?", {"pred": {"is_true": "is_weekend:delivery"}},
           scope_phrase=sp),
        {"slot": "q3", "role": "base", "type": "choice", "scope_phrase": sp, "instructions": f"{sp}, what happens?",
         "options": {"exchange allowed": "The item can still be swapped.", "exchange refused": "The swap window has closed."},
         "scale_order": ["exchange allowed", "exchange refused"], "asks": {"choice_var": "outcome"}},
        _q("q4", "noul", f"{sp}, has the swap period run out?", {"negation_of": "q1"}, role="free_negation", scope_phrase=sp),
        _q("q5", "noul", f"{sp}, may the buyer still trade the item for another?", {"paraphrase_of": "q1"},
           role="free_paraphrase", scope_phrase=sp),
    ]
    return s


def fx_hop():
    s = _base("FR-HOP", scope="record", vertical="insurance")
    s["parameters"] = {
        "vars": {"days_to_report": 12, "has_photos": True, "has_invoice": False, "joined": "2024-06-01",
                 "claim_amount": 900, "second_claim_this_year": False, "requests": ["repair", "rental car"]},
        "conditions": [{"id": "c1", "test": {"var": "days_to_report", "op": "<=", "value": 14}},
                       {"id": "c2", "test": {"is_true": "has_photos"}},
                       {"id": "c3", "test": {"is_true": "has_invoice"}},
                       {"id": "c4", "test": {"var": "claim_amount", "op": "<", "value": 2500}},
                       {"id": "c5", "test": {"is_false": "second_claim_this_year"}},
                       {"id": "c6", "test": {"any": [{"is_true": "met:c2"}, {"is_true": "met:c3"}]}}],
        "waivers": [{"id": "w1", "waives": ["c3"], "when": {"var": "joined", "op": "<", "value": "2025-01-01"}}],
        "outcome_rules": [{"when": {"is_true": "all_satisfied"}, "outcome": "pay in full"},
                          {"when": {"var": "conditions_satisfied", "op": ">=", "value": 5}, "outcome": "refer to adjuster"},
                          {"outcome": "decline"}]}
    sp = "Under the policy sections quoted"
    s["questions"] = [
        _q("q1", "noul", f"{sp}, will this claim be paid in full?", {"choice_is": "pay in full"}, scope_phrase=sp,
           proposition={"p": "the claim will be paid in full", "negP": "the claim will not be paid in full"}),
        _q("q2", "noul", f"{sp}, does the member ask for both a repair and a rental car?",
           {"pred": {"all": [{"var": "requests", "op": "contains", "value": "repair"},
                             {"var": "requests", "op": "contains", "value": "rental car"}]}}, scope_phrase=sp),
        {"slot": "q3", "role": "base", "type": "choice", "scope_phrase": sp, "instructions": f"{sp}, what is the decision?",
         "options": {"pay in full": "Every condition is met or waived.", "refer to adjuster": "Exactly one condition fails.",
                     "decline": "Two or more conditions fail."},
         "scale_order": ["pay in full", "refer to adjuster", "decline"], "asks": {"choice_var": "outcome"}},
        _q("q4", "noul", f"{sp}, will the payout fall short of the full claim?", {"negation_of": "q1"},
           role="free_negation", scope_phrase=sp),
        _q("q5", "noul", f"{sp}, is the member getting the whole amount?", {"paraphrase_of": "q1"},
           role="free_paraphrase", scope_phrase=sp),
        {"slot": "q7", "role": "base", "type": "score", "K": 7, "scope_phrase": sp,
         "instructions": f"{sp}, not counting any exception, how many of the six listed conditions does the claim meet?",
         "levels": ["none of the 6", "1 of the 6", "2 of the 6", "3 of the 6", "4 of the 6", "5 of the 6", "all 6"],
         "asks": {"score": {"kind": "var", "var": "conditions_met"}}},
    ]
    return s


def fx_lit():
    s = _base("FR-LIT", vertical="travel")
    s["doc"], s["agent"] = "review", "reviewer"
    s["parameters"] = {
        "filters": {"A": {"polarity": ["neg"], "severity": ["cosmetic", "minor", "major"]},
                    "B": {"polarity": ["neg"], "severity": ["major"]}},
        "aspects": [
            {"name": "check-in", "remarks": [{"polarity": "pos"}]},
            {"name": "room", "remarks": [{"polarity": "neg", "severity": "cosmetic"}, {"polarity": "pos"}]},
            {"name": "breakfast", "remarks": [{"polarity": "neg", "severity": "minor", "resolved": True}]},
            {"name": "wifi", "remarks": [{"polarity": "neg", "severity": "major", "speaker": "other"}]},
            {"name": "parking", "remarks": []},
            {"name": "noise", "remarks": [{"polarity": "neutral"}]}]}
    crit_a = {"true": "The reviewer describes any flaw in the room, cosmetic ones included.",
              "false": "The reviewer describes no flaw in the room, cosmetic ones included."}
    crit_b = {"true": "The reviewer describes a room flaw that made the room hard to use; looks alone do not count.",
              "false": "The reviewer describes no room flaw that made the room hard to use; looks alone do not count."}
    instr = "Does the reviewer find fault with the room?"
    s["questions"] = [
        _q("q1", "noul", instr, {"choice_is": "complaint"}, criteria=crit_a,
           proposition={"p": "the reviewer finds fault with the room", "negP": "the reviewer finds no fault with the room"}),
        _q("q2", "noul", instr, {"pred": {"is_true": "complaint:B:room"}}, role="criteria_variant", criteria=crit_b),
        {"slot": "q3", "role": "base", "type": "choice", "instructions": "How does the reviewer treat the room?",
         "options": {"complaint": "Reports a flaw in the room, cosmetic ones included.",
                     "praise only": "Speaks well of the room and reports no flaw.",
                     "neutral mention": "Mentions the room without praise or a flaw.",
                     "not mentioned": "Says nothing about the room."},
         "asks": {"choice_var": "stance:A:room"}},
        _q("q4", "noul", "Would a guest reading this conclude the room left nothing to fix?", {"negation_of": "q1"},
           role="free_negation", criteria={"true": "A guest would conclude the room left nothing to fix.",
                                           "false": "A guest would not conclude the room left nothing to fix."}),
        _q("q5", "noul", "Is there something about the room this guest was unhappy with?", {"paraphrase_of": "q1"},
           role="free_paraphrase", criteria=crit_a),
        {"slot": "q7", "role": "base", "type": "score", "K": 7,
         "instructions": "Of check-in, room, breakfast, wifi, parking and noise, how many does the reviewer fault?",
         "levels": ["none of the 6", "1 of the 6", "2 of the 6", "3 of the 6", "4 of the 6", "5 of the 6", "all 6"],
         "asks": {"score": {"kind": "count", "preds": [{"is_true": f"complaint:A:{a}"} for a in
                                                       ("check-in", "room", "breakfast", "wifi", "parking", "noise")]}}},
    ]
    return s


def fx_phish(phishing=True):
    s = _base("FR-PHISH", vertical="utilities")
    s["doc"], s["agent"] = "email", "sender"
    s["parameters"] = {
        "known_domains": ["fixturepower.example"],
        "email": {"from_domain": "fixturepower-billing.test" if phishing else "mail.fixturepower.example",
                  "link_domains": ["fixturepower-billing.test"] if phishing else ["account.fixturepower.example"]},
        "signs": {"asks_secret": phishing, "unusual_payment": False, "asks_personal_data": False,
                  "unexpected_attachment": False, "threat_or_deadline": True, "generic_greeting": True,
                  "prize_lure": False, "asks_click_or_call": True, "mentions_account_problem": True},
        "purpose": "bill"}
    s["questions"] = [
        _q("q1", "noul", "Is this email a phishing attempt?", {"choice_is": "phishing"},
           proposition={"p": "this email is a phishing attempt", "negP": "this email is not a phishing attempt"}),
        _q("q2", "noul", "Does the email ask for a password or one-time code?", {"pred": {"is_true": "asks_secret"}}),
        {"slot": "q3", "role": "base", "type": "choice", "instructions": "What kind of email is this?",
         "options": {"phishing": "Pretends to be someone else to get secrets or money.",
                     "marketing": "A genuine promotional email from the named company.",
                     "transactional": "A genuine notice about the reader's own account or bill.",
                     "personal": "A genuine message from someone the reader knows."},
         "asks": {"choice_var": "category"}},
        _q("q4", "noul", "Could the reader trust this message as genuinely from the utility?", {"negation_of": "q1"},
           role="free_negation"),
        _q("q5", "noul", "Is someone posing as the utility to trick the reader?", {"paraphrase_of": "q1"},
           role="free_paraphrase"),
        {"slot": "q7", "role": "base", "type": "score", "K": 7,
         "instructions": "How many of these six warning signs does the email show: a sender address outside the "
                         "company's domain, a link outside it, a request for a password or code, a threat or "
                         "48-hour deadline, a generic greeting, a prize nobody asked for?",
         "levels": ["none of the 6", "1 of the 6", "2 of the 6", "3 of the 6", "4 of the 6", "5 of the 6", "all 6"],
         "asks": {"score": {"kind": "count", "preds": [{"is_true": x} for x in (
             "sender_mismatch", "link_mismatch", "asks_secret", "threat_or_deadline", "generic_greeting", "prize_lure")]}}},
    ]
    return s


def fx_hneg():
    s = _base("FR-HNEG", vertical="telecom")
    s["doc"] = "message"
    s["parameters"] = {
        "request_types": ["refund", "plan cancellation", "device repair"],
        "segments": [
            {"id": "s1", "speaker": "customer", "act": "request", "type": "refund"},
            {"id": "s2", "speaker": "third_party", "act": "suggest", "type": "device repair"},
            {"id": "s3", "speaker": "customer", "act": "replace", "type": "plan cancellation", "targets": ["s1"]}]}
    s["questions"] = [
        _q("q1", "noul", "Does the customer want the plan cancelled?", {"choice_is": "plan cancellation"},
           proposition={"p": "the customer wants the plan cancelled", "negP": "the customer does not want the plan cancelled"}),
        _q("q2", "noul", "Did the customer at some point ask for money back?", {"pred": {"is_true": "ever_requested:refund"}}),
        {"slot": "q3", "role": "base", "type": "choice", "instructions": "What is the customer asking for now?",
         "options": {"refund": "Money returned for a charge.", "plan cancellation": "Ending the service plan.",
                     "device repair": "Fixing a broken handset.", NONE_KEY: "The customer asks for none of the above."},
         "asks": {"choice_var": "final_request"}},
        _q("q4", "noul", "Is keeping the plan running what the customer is after?", {"negation_of": "q1"},
           role="free_negation"),
        _q("q5", "noul", "Is the customer trying to end the service plan?", {"paraphrase_of": "q1"},
           role="free_paraphrase"),
    ]
    return s


FIXTURE_NUM_STATE = (
    "Store record, Fixture Lamps (counter 3). Policy card at the till: a purchase with its receipt and a "
    "counted total of $100 or more gets a full refund to the original card; with a receipt but under $100 the "
    "shopper gets store credit; without a receipt nothing is returned. Delivery charges never count toward the "
    "total, and coupons are taken off first. Case: the shopper bought one lamp at $64.00 and two shades at "
    "$21.50 each, paid $15.00 for delivery, and used a $10.00 coupon. The receipt was shown at the desk. The "
    "shopper mentioned the lamp flickers and asked politely what the options were; they also asked about the "
    "loyalty card, which staff said can be sorted out on the next visit."
)


class TestGold(unittest.TestCase):
    def test_num_tiers(self):
        g, ctx = compute(fx_num())
        self.assertEqual(ctx.env["total"], Decimal("97.00"))
        self.assertEqual(ctx.env["excluded_total"], Decimal("15"))
        self.assertEqual(g, {"q1": 0, "q2": 1, "q3": "store credit", "q4": 1, "q5": 0})

    def test_num_boundary_warning(self):
        s = fx_num()
        s["parameters"]["credits"][0]["amount"] = 7  # total exactly 100
        g, ctx = compute(s)
        self.assertEqual(g["q3"], "full refund")
        self.assertTrue(any("boundary" in w for w in ctx.warnings))

    def test_num_score_bins(self):
        s = fx_num()
        s["questions"][1] = {"slot": "q2", "role": "base", "type": "score", "K": 4, "scope_phrase": "Going only by the store record",
                             "instructions": "Going only by the store record, how much comes back?",
                             "levels": ["nothing", "under $50", "$50 to $99.99", "$100 or more"],
                             "asks": {"score": {"kind": "bins", "var": "total", "bounds": [0.01, 50, 100]}}}
        self.assertEqual(compute_gold(s)["q2"], 2)

    def test_date_business_days(self):
        g, ctx = compute(fx_date())
        self.assertEqual(ctx.env["deadline:return"], dt.date(2026, 10, 7))  # holiday on Wed 30 Sep is skipped
        self.assertEqual(ctx.env["bdays_since:purchase"], Decimal(5))
        self.assertEqual(ctx.env["days_since:purchase"], Decimal(10))
        self.assertTrue(ctx.env["open:cal10"])  # decided on the deadline day -> warning
        self.assertTrue(any("deadline day" in w for w in ctx.warnings))
        self.assertEqual(g, {"q1": 1, "q2": 0, "q3": "exchange allowed", "q4": 0, "q5": 1})

    def test_business_day_helpers(self):
        fri = dt.date(2026, 9, 25)
        self.assertEqual(add_business_days(fri, 5, set()), dt.date(2026, 10, 2))
        self.assertEqual(add_business_days(fri, 1, set()), dt.date(2026, 9, 28))
        self.assertEqual(business_days_between(fri, dt.date(2026, 9, 27), set()), 0)
        self.assertEqual(business_days_between(dt.date(2026, 10, 2), fri, set()), -5)

    def test_date_cutoff(self):
        s = fx_date()
        s["parameters"]["today"] = "2026-10-07"
        s["parameters"]["now"] = "17:30"
        s["parameters"]["windows"][0]["cutoff"] = "17:00"
        self.assertEqual(compute_gold(s)["q1"], 0)

    def test_hop_waiver_and_count(self):
        g, ctx = compute(fx_hop())
        self.assertFalse(ctx.env["met:c3"])
        self.assertTrue(ctx.env["satisfied:c3"])  # waived for members who joined before 2025
        self.assertEqual(ctx.env["conditions_met"], Decimal(5))
        self.assertEqual(g, {"q1": 1, "q2": 1, "q3": "pay in full", "q4": 0, "q5": 1, "q7": 5})
        s = fx_hop()
        s["parameters"]["vars"]["joined"] = "2025-03-01"
        self.assertEqual(compute_gold(s)["q3"], "refer to adjuster")

    def test_lit_criteria_variant(self):
        g, ctx = compute(fx_lit())
        self.assertEqual(ctx.env["stance:A:check-in"], "praise only")
        self.assertEqual(ctx.env["stance:A:noise"], "neutral mention")
        self.assertEqual(ctx.env["stance:A:parking"], "not mentioned")
        self.assertFalse(ctx.env["complaint:A:wifi"] is False)  # speaker not restricted by filter A
        self.assertEqual(g, {"q1": 1, "q2": 0, "q3": "complaint", "q4": 0, "q5": 1, "q7": 3})
        r = check_spec(fx_lit(), bank=load_template_bank())
        self.assertEqual([e for e in r["errors"]], [])

    def test_lit_variant_must_move_boundary(self):
        s = fx_lit()
        s["parameters"]["filters"]["B"] = {"polarity": ["neg"], "severity": ["cosmetic", "major"]}
        r = check_spec(s, bank=load_template_bank())
        self.assertTrue(any("must differ from q1 gold" in e for e in r["errors"]))

    def test_phish_rule(self):
        self.assertEqual(compute_gold(fx_phish(True)), {"q1": 1, "q2": 1, "q3": "phishing", "q4": 0, "q5": 1, "q7": 5})
        g = compute_gold(fx_phish(False))
        self.assertEqual((g["q1"], g["q3"], g["q7"]), (0, "transactional", 2))

    def test_phish_ambiguous_and_unsafe(self):
        s = fx_phish(False)
        s["parameters"]["signs"]["asks_secret"] = True  # genuine domain asking for a secret: ambiguous
        with self.assertRaises(SpecError):
            compute(s)
        s = fx_phish(True)
        s["parameters"]["email"]["from_domain"] = "fixturepower-billing.com"
        with self.assertRaises(SpecError):
            compute(s)

    def test_hneg_override_and_quote(self):
        g, ctx = compute(fx_hneg())
        self.assertEqual(ctx.env["final_request"], "plan cancellation")
        self.assertTrue(ctx.env["tempting:refund"] and ctx.env["tempting:device repair"])
        self.assertEqual(g, {"q1": 1, "q2": 1, "q3": "plan cancellation", "q4": 0, "q5": 1})
        s = fx_hneg()
        s["parameters"]["segments"][2] = {"id": "s3", "speaker": "customer", "act": "withdraw", "targets": ["s1"]}
        self.assertEqual(compute_gold(s)["q3"], NONE_KEY)
        s = fx_hneg()
        s["parameters"]["segments"][2] = {"id": "s3", "speaker": "customer", "act": "request", "type": "device repair"}
        with self.assertRaises(SpecError):  # two active requests
            compute(s)

    def test_choice_must_be_exhaustive(self):
        s = fx_num()
        del s["questions"][2]["options"]["refund refused"]
        s["questions"][2]["scale_order"] = ["full refund", "store credit"]
        with self.assertRaises(SpecError):
            compute(s)

    def test_q1_label_must_be_option(self):
        s = fx_num()
        s["questions"][0]["asks"] = {"choice_is": "cash back"}
        with self.assertRaises(SpecError):
            compute(s)

    def test_unknown_variable(self):
        s = fx_num()
        s["parameters"]["outcome_rules"][0]["when"] = {"is_true": "has_reciept"}
        with self.assertRaises(SpecError):
            compute(s)

    def test_free_variant_jaccard(self):
        bank = load_template_bank()
        s = fx_num()
        ok, _ = free_variant_score(s["questions"][3]["instructions"], s, bank, s["questions"][3]["scope_phrase"])
        self.assertLess(ok, FREE_JACCARD_MAX)
        sp = "Going only by the store record"
        for bad in (f"{sp}, is it false that the purchase qualifies for a full refund?",
                    f"{sp}, would it be wrong to say that the purchase qualifies for a full refund?",
                    "Is it not the case that the purchase qualifies for a full refund?",
                    f"{sp}, is it the case that the purchase does not qualify for a full refund?"):
            score, tid = free_variant_score(bad, s, bank, sp)
            self.assertGreaterEqual(score, FREE_JACCARD_MAX, (bad, score, tid))

    def test_forbidden_forms(self):
        e, _ = question_form_issues("Isn't the claim eligible?", "free_negation")
        self.assertTrue(e)
        e, _ = question_form_issues("Under the terms above, is it not true that the claim is eligible?", "free_negation")
        self.assertTrue(e)
        e, _ = question_form_issues("Is there no indication that the claim is eligible?", "free_negation")
        self.assertTrue(e)
        e, _ = question_form_issues("Would approving this claim break the policy?", "free_negation")
        self.assertFalse(e)

    def test_safety_scan(self):
        e, _ = safety_scan("Call 555-0142 or write to help@fixturetel.example; see https://fixturetel.test/pay", "t")
        self.assertEqual(e, [])
        for bad in ("Call 555-2368 now", "Visit fixturetel.com today", "Reply to a@b.net", "Your PayPal account",
                    "Card 4111 1111 1111 1111", "Server 10.0.0.1"):
            e, _ = safety_scan(bad, "t")
            self.assertTrue(e, bad)

    def test_full_check_with_state(self):
        s = fx_num()
        s["state"] = FIXTURE_NUM_STATE
        r = check_spec(s, bank=load_template_bank(), schema=load_schema())
        self.assertEqual(r["errors"], [], r["errors"])
        self.assertTrue(100 <= word_count(FIXTURE_NUM_STATE) <= 139)

    def test_schema_accepts_fixtures(self):
        schema = load_schema()
        if schema is None:
            self.skipTest("spec.schema.json not found")
        try:
            import jsonschema  # noqa: F401
        except ImportError:
            self.skipTest("jsonschema not installed")
        for fx in (fx_num(), fx_date(), fx_hop(), fx_lit(), fx_phish(True), fx_phish(False), fx_hneg()):
            errs, _ = _schema_errors(fx, schema)
            self.assertEqual(errs, [], (fx["item_id"], errs))
        bad = fx_num()
        bad["questions"][0]["asks"] = {"choice_is": 3}
        self.assertTrue(_schema_errors(bad, schema)[0])

    def test_fixtures_pass_check(self):
        bank = load_template_bank()
        for fx in (fx_num(), fx_date(), fx_hop(), fx_lit(), fx_phish(True), fx_phish(False), fx_hneg()):
            r = check_spec(fx, bank=bank, schema=load_schema())
            self.assertEqual(r["errors"], [], (fx["item_id"], r["errors"]))

    def test_card_targets(self):
        s = fx_num()
        card = {"card_id": s["card_id"], "group_id": s["group_id"], "family": "FR-NUM", "vertical": "retail",
                "complication": "fixture", "length_bin": "medium", "state_format": "fixture",
                "targets": {"q1": {"gold": 1, "target_kind": "gold"}, "q2": {"type": "noul", "gold": 1},
                            "q3": {"n_options": 3}, "q7": None}}
        r = check_spec(s, card=card, bank=load_template_bank())
        self.assertTrue(any("q1 gold is 0" in e for e in r["errors"]))
        card["targets"]["q1"] = {"gold": 0, "target_kind": "adjacent_wrong"}
        r = check_spec(s, card=card, bank=load_template_bank())
        self.assertEqual([e for e in r["errors"] if e.startswith("card")], [])
        card["targets"]["q1"]["target_kind"] = "non_adjacent_wrong"
        r = check_spec(s, card=card, bank=load_template_bank())
        self.assertTrue(any("non_adjacent_wrong" in e for e in r["errors"]))

    def test_scenario_cards_file(self):
        f = HERE / "scenario_cards.jsonl"
        if not f.exists():
            self.skipTest("scenario_cards.jsonl not written yet")
        cards = read_jsonl(f)
        self.assertEqual(len(cards), 156)
        by_fam = defaultdict(list)
        for c in cards:
            by_fam[c["family"]].append(c)
        self.assertEqual(sorted(by_fam), sorted(FAMILIES))
        k7 = 0
        for fam, cs in by_fam.items():
            self.assertEqual(len(cs), 26)
            self.assertEqual(sum(c["targets"]["q1"]["gold"] for c in cs), 13)
            core = sorted(cs, key=lambda c: c["rank"])[:16]
            self.assertEqual(sum(c["targets"]["q1"]["gold"] for c in core), 8)
            self.assertTrue(all(c["vertical"] in VERTICALS for c in cs))
            q7 = [c for c in core if c["targets"]["q7"]]
            want = {"FR-LIT": 16, "FR-HOP": 8, "FR-PHISH": 8}.get(fam, 0)
            self.assertEqual(len(q7), want, fam)
            k7 += sum(1 for c in q7 if c["targets"]["q7"]["K"] == 7)
            if fam == "FR-LIT":
                self.assertEqual(sum(1 for c in q7 if c["targets"]["q7"]["K"] == 4), 8)
            if fam == "FR-NUM":
                self.assertEqual(sum(1 for c in core if c["targets"]["q2"]["type"] == "score"), 8)
        self.assertEqual(k7, 24)


if __name__ == "__main__":
    sys.exit(main())

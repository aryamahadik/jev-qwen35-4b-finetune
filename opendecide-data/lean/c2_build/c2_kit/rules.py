"""c2_kit/rules.py: the C2 rule AST, its interpreter and the precedence policies (solver-A side; C2_DATA_SPEC 6.2).

Solver A of a family usually builds an AST from the spec and runs evaluate() / resolve(). Solver B must not import
this module (plugin.check_independence enforces it): it re-derives the gold in another paradigm from the parsed row.

Nodes (frozen dataclasses; to_json / from_json give one canonical JSON form; refs() lists the slots a node reads):
  Ref(slot)                    the value of a spec slot (python value: date, datetime, int, str)
  Lit(value)                   a constant (dates and datetimes tagged in JSON)
  Cmp(op, left, right)         op in < <= > >= == != : every boundary is explicit (inclusive vs exclusive)
  And(args) / Or(args) / Not(arg)
  In(item, options)            item equals one of the options
  Glob(pattern, subject, sem)  glob_a.match under globsem.GlobSem
  Fn(name, args)               a registered pure function (FNS): days_between, add_days, add, sub, utc_minutes,
                               local_date, abs, min, max; register_fn() adds family functions
  Rule(rid, effect, when, specificity=(), priority=None)
  RuleSet(rules, policy, default, effect_order=(), priority=())

Policies (T28's closed set, reused by other families):
  effect_order   P1: the matched rule whose effect ranks first in effect_order (e.g. deny > ask > allow)
  first_match    P2: the first listed matched rule
  most_specific  P3: the matched rule with the largest specificity tuple; ties broken by effect_order
  last_match     P4: the last listed matched rule
  priority_list  P5: the matched rule named earliest in `priority`
  No matched rule: the default effect (rule_id None). Decision.tied lists every rule that shares the deciding key, so
  a family drops "which rule decides" rows when len(tied) > 1 (the effect is still exact).

Three-valued reading: evaluate3() is Kleene logic (a missing slot is unknown). It is sound but not complete: True or
False means every completion agrees; None does NOT prove the completions disagree. Exact "cannot decide" golds use
brute.completions() over the family's stated domains (that helper lives on the solver-B side).

Depth: op_count(node, printed) counts Cmp / Fn / Glob / In operations a reader must do, skipping subtrees whose value
the row prints (C2 3.0: at most 2 unstated operations per row).
"""
from __future__ import annotations

import datetime as dt
import json
from dataclasses import dataclass
from typing import Any, Callable

from . import glob_a
from .globsem import GlobSem

OPS = ("<", "<=", ">", ">=", "==", "!=")
POLICIES = ("effect_order", "first_match", "most_specific", "last_match", "priority_list")
_FLIP = {">": "<", ">=": "<="}


class Missing(KeyError):
    """A Ref has no value in the environment."""


class RuleError(ValueError):
    pass


@dataclass(frozen=True)
class Ref:
    slot: str


@dataclass(frozen=True)
class Lit:
    value: Any


@dataclass(frozen=True)
class Cmp:
    op: str
    left: Any
    right: Any

    def __post_init__(self):
        if self.op not in OPS:
            raise RuleError(f"comparator {self.op!r}")


@dataclass(frozen=True)
class And:
    args: tuple


@dataclass(frozen=True)
class Or:
    args: tuple


@dataclass(frozen=True)
class Not:
    arg: Any


@dataclass(frozen=True)
class In:
    item: Any
    options: tuple


@dataclass(frozen=True)
class Glob:
    pattern: Any
    subject: Any
    sem: GlobSem = GlobSem()


@dataclass(frozen=True)
class Fn:
    name: str
    args: tuple


@dataclass(frozen=True)
class Rule:
    rid: str
    effect: str
    when: Any
    specificity: tuple = ()
    priority: int | None = None


@dataclass(frozen=True)
class RuleSet:
    rules: tuple
    policy: str
    default: str
    effect_order: tuple = ()
    priority: tuple = ()

    def __post_init__(self):
        if self.policy not in POLICIES:
            raise RuleError(f"policy {self.policy!r}")
        rids = [r.rid for r in self.rules]
        if len(set(rids)) != len(rids):
            raise RuleError("duplicate rule ids")
        if self.policy in ("effect_order", "most_specific"):
            missing = {r.effect for r in self.rules} - set(self.effect_order)
            if missing:
                raise RuleError(f"effect_order lacks {sorted(missing)}")
        if self.policy == "priority_list" and set(self.priority) != set(rids):
            raise RuleError("priority_list must name every rule exactly once")


@dataclass(frozen=True)
class Decision:
    effect: str
    rule_id: str | None
    matched: tuple
    tied: tuple
    policy: str


# ------------------------------------------------------------------------------------------------ functions

def _days_between(a, b):
    return (b - a).days


def _utc_minutes(t):
    if t.tzinfo is None:
        raise RuleError("utc_minutes needs an aware datetime")
    return int((t - dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)).total_seconds()) // 60


FNS: dict = {
    "days_between": _days_between,                 # whole days from a to b (b - a)
    "add_days": lambda d, n: d + dt.timedelta(days=n),
    "add": lambda a, b: a + b,
    "sub": lambda a, b: a - b,
    "utc_minutes": _utc_minutes,                   # minutes since 1970-01-01T00:00Z
    "local_date": lambda t: t.date(),              # the calendar date at the datetime's own offset
    "abs": abs,
    "min": min,
    "max": max,
}


def register_fn(name: str, fn: Callable) -> None:
    if name in FNS and FNS[name] is not fn:
        raise RuleError(f"function {name!r} is already registered")
    FNS[name] = fn


# ------------------------------------------------------------------------------------------------ evaluation

def _cmp(op, a, b) -> bool:
    if type(a) is bool or type(b) is bool:
        raise RuleError("comparisons never take booleans")
    return {"<": a < b, "<=": a <= b, ">": a > b, ">=": a >= b, "==": a == b, "!=": a != b}[op]


def evaluate(node, env: dict, trace: list | None = None):
    """The value of `node` in `env` (slot -> python value). Raises Missing on an absent slot."""
    if isinstance(node, Ref):
        if node.slot not in env or env[node.slot] is None:
            raise Missing(node.slot)
        return env[node.slot]
    if isinstance(node, Lit):
        return node.value
    if isinstance(node, Cmp):
        v = _cmp(node.op, evaluate(node.left, env, trace), evaluate(node.right, env, trace))
    elif isinstance(node, And):
        v = all(_truth(evaluate(a, env, trace)) for a in node.args)
    elif isinstance(node, Or):
        v = any(_truth(evaluate(a, env, trace)) for a in node.args)
    elif isinstance(node, Not):
        v = not _truth(evaluate(node.arg, env, trace))
    elif isinstance(node, In):
        item = evaluate(node.item, env, trace)
        v = any(item == evaluate(o, env, trace) for o in node.options)
    elif isinstance(node, Glob):
        v = glob_a.match(evaluate(node.pattern, env, trace), evaluate(node.subject, env, trace), node.sem)
    elif isinstance(node, Fn):
        if node.name not in FNS:
            raise RuleError(f"unknown function {node.name!r}")
        v = FNS[node.name](*[evaluate(a, env, trace) for a in node.args])
    else:
        raise RuleError(f"not an expression node: {type(node).__name__}")
    if trace is not None and isinstance(node, (Cmp, Fn, Glob, In)):
        trace.append((json.dumps(to_json(node), sort_keys=True), v))
    return v


def _truth(v) -> bool:
    if not isinstance(v, bool):
        raise RuleError(f"a condition evaluated to {v!r}, not a boolean")
    return v


def evaluate3(node, env: dict):
    """Kleene three-valued truth: True / False / None (unknown). Sound, not complete (see the module doc)."""
    if isinstance(node, And):
        vals = [evaluate3(a, env) for a in node.args]
        return False if False in vals else (None if None in vals else True)
    if isinstance(node, Or):
        vals = [evaluate3(a, env) for a in node.args]
        return True if True in vals else (None if None in vals else False)
    if isinstance(node, Not):
        v = evaluate3(node.arg, env)
        return None if v is None else not v
    try:
        v = evaluate(node, env)
    except Missing:
        return None
    return v


def matched_rules(rs: RuleSet, env: dict) -> tuple:
    return tuple(r for r in rs.rules if _truth(evaluate(r.when, env)))


def resolve(rs: RuleSet, env: dict) -> Decision:
    """The deciding rule and effect under the rule set's policy (default effect when nothing matches)."""
    m = matched_rules(rs, env)
    ids = tuple(r.rid for r in m)
    if not m:
        return Decision(rs.default, None, (), (), rs.policy)
    rank = {e: i for i, e in enumerate(rs.effect_order)}
    if rs.policy == "first_match":
        win, tied = m[0], (m[0].rid,)
    elif rs.policy == "last_match":
        win, tied = m[-1], (m[-1].rid,)
    elif rs.policy == "priority_list":
        pos = {rid: i for i, rid in enumerate(rs.priority)}
        win = min(m, key=lambda r: pos[r.rid])
        tied = (win.rid,)
    elif rs.policy == "effect_order":
        best = min(rank[r.effect] for r in m)
        tied = tuple(r.rid for r in m if rank[r.effect] == best)
        win = next(r for r in m if rank[r.effect] == best)
    else:  # most_specific
        key = lambda r: (tuple(r.specificity), -rank[r.effect])   # noqa: E731
        best = max(key(r) for r in m)
        tied = tuple(r.rid for r in m if key(r) == best)
        win = next(r for r in m if key(r) == best)
    return Decision(win.effect, win.rid, ids, tied, rs.policy)


# ------------------------------------------------------------------------------------------------ JSON form

def _lit_json(v):
    if isinstance(v, dt.datetime):
        return {"$datetime": v.isoformat()}
    if isinstance(v, dt.date):
        return {"$date": v.isoformat()}
    if isinstance(v, tuple):
        return {"$tuple": [_lit_json(x) for x in v]}
    return v


def _lit_py(v):
    if isinstance(v, dict) and len(v) == 1:
        (k, x), = v.items()
        if k == "$datetime":
            return dt.datetime.fromisoformat(x)
        if k == "$date":
            return dt.date.fromisoformat(x)
        if k == "$tuple":
            return tuple(_lit_py(y) for y in x)
    return v


def to_json(node):
    if isinstance(node, Ref):
        return {"op": "ref", "slot": node.slot}
    if isinstance(node, Lit):
        return {"op": "lit", "value": _lit_json(node.value)}
    if isinstance(node, Cmp):
        return {"op": "cmp", "cmp": node.op, "left": to_json(node.left), "right": to_json(node.right)}
    if isinstance(node, (And, Or)):
        return {"op": "and" if isinstance(node, And) else "or", "args": [to_json(a) for a in node.args]}
    if isinstance(node, Not):
        return {"op": "not", "arg": to_json(node.arg)}
    if isinstance(node, In):
        return {"op": "in", "item": to_json(node.item), "options": [to_json(o) for o in node.options]}
    if isinstance(node, Glob):
        return {"op": "glob", "pattern": to_json(node.pattern), "subject": to_json(node.subject),
                "sem": {k: getattr(node.sem, k) for k in node.sem.__dataclass_fields__}}
    if isinstance(node, Fn):
        return {"op": "fn", "name": node.name, "args": [to_json(a) for a in node.args]}
    if isinstance(node, Rule):
        return {"op": "rule", "rid": node.rid, "effect": node.effect, "when": to_json(node.when),
                "specificity": list(node.specificity), "priority": node.priority}
    if isinstance(node, RuleSet):
        return {"op": "ruleset", "rules": [to_json(r) for r in node.rules], "policy": node.policy,
                "default": node.default, "effect_order": list(node.effect_order), "priority": list(node.priority)}
    raise RuleError(f"not a node: {type(node).__name__}")


def from_json(o):
    op = o["op"]
    if op == "ref":
        return Ref(o["slot"])
    if op == "lit":
        return Lit(_lit_py(o["value"]))
    if op == "cmp":
        return Cmp(o["cmp"], from_json(o["left"]), from_json(o["right"]))
    if op in ("and", "or"):
        args = tuple(from_json(a) for a in o["args"])
        return And(args) if op == "and" else Or(args)
    if op == "not":
        return Not(from_json(o["arg"]))
    if op == "in":
        return In(from_json(o["item"]), tuple(from_json(x) for x in o["options"]))
    if op == "glob":
        return Glob(from_json(o["pattern"]), from_json(o["subject"]), GlobSem(**o["sem"]))
    if op == "fn":
        return Fn(o["name"], tuple(from_json(a) for a in o["args"]))
    if op == "rule":
        return Rule(o["rid"], o["effect"], from_json(o["when"]), tuple(o["specificity"]), o["priority"])
    if op == "ruleset":
        return RuleSet(tuple(from_json(r) for r in o["rules"]), o["policy"], o["default"], tuple(o["effect_order"]),
                       tuple(o["priority"]))
    raise RuleError(f"unknown op {op!r}")


def _key(j) -> str:
    return json.dumps(j, sort_keys=True)


def canonical(node):
    """JSON form with commutative arguments sorted and > / >= turned into < / <= (operands swapped)."""
    j = to_json(node)

    def norm(x):
        if not isinstance(x, dict) or "op" not in x:
            return x
        x = {k: (norm(v) if isinstance(v, dict) else [norm(e) for e in v] if isinstance(v, list) else v)
             for k, v in x.items()}
        if x["op"] in ("and", "or"):
            x["args"] = sorted(x["args"], key=_key)
        elif x["op"] == "in":
            x["options"] = sorted(x["options"], key=_key)
        elif x["op"] == "cmp":
            if x["cmp"] in _FLIP:
                x["cmp"], x["left"], x["right"] = _FLIP[x["cmp"]], x["right"], x["left"]
            elif x["cmp"] in ("==", "!=") and _key(x["left"]) > _key(x["right"]):
                x["left"], x["right"] = x["right"], x["left"]
        return x

    return norm(j)


def ast_equal(a, b) -> bool:
    """Equal up to argument order of and / or / in and the orientation of comparisons (T24 cosmetic admission)."""
    return _key(canonical(a)) == _key(canonical(b))


def refs(node) -> set:
    out = set()

    def walk(x):
        if isinstance(x, dict):
            if x.get("op") == "ref":
                out.add(x["slot"])
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    walk(to_json(node))
    return out


def op_count(node, printed: frozenset = frozenset()) -> int:
    """Operations a reader performs: Cmp, Fn, Glob and In nodes outside printed subtrees (printed = canonical keys)."""
    def walk(x):
        if not isinstance(x, dict) or "op" not in x:
            return 0
        if _key(x) in printed:
            return 0
        own = 1 if x["op"] in ("cmp", "fn", "glob", "in") else 0
        sub = 0
        for v in x.values():
            if isinstance(v, dict):
                sub += walk(v)
            elif isinstance(v, list):
                sub += sum(walk(e) for e in v)
        return own + sub

    return walk(canonical(node))


def printed_key(node) -> str:
    """The key op_count() expects in `printed` for a subtree whose value the row prints."""
    return _key(canonical(node))

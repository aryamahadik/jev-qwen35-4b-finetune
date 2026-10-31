"""Invariant checkers for T55 B3 (IMPLICIT-ERROR): well-formed results that violate an invariant the card never names.

A case is (result, ctx):
  result = {"items": list|None, "fields": {name: number}, "total": number|None, "echo": {arg: value}|None}
  ctx    = {"stated_count": int|None, "prior_ids": list|None, "reference": {"field","value"}|None, "unique": bool,
            "order": (field, "asc"|"desc")|None, "nonneg_fields": [names], "intended_args": {..}|None,
            "prior_args": {..}|None, "call_args": {..}}
One checker per violation type; `violations(result, ctx)` returns the set of violated types; `cause(...)` says whether
the CALL'S OWN ARGUMENTS explain the violation (visible by comparing call_args with the context).
"""
import copy

from . import perturb, state

POW10 = (10.0, 100.0, 1000.0, 0.1, 0.01, 0.001)


def _ratio_is_pow10(a, b):
    if b == 0 or a == b:
        return False
    r = a / b
    return any(abs(r - p) <= 1e-9 * max(1.0, abs(p)) for p in POW10)


def chk_empty_when_count_stated(result, ctx):
    return (ctx.get("stated_count") is not None and ctx["stated_count"] > 0 and result.get("items") is not None
            and len(result["items"]) == 0)


def chk_negative_value(result, ctx):
    return any(result["fields"].get(f) is not None and result["fields"][f] < 0 for f in ctx.get("nonneg_fields", []))


def chk_id_not_in_prior_list(result, ctx):
    prior = ctx.get("prior_ids")
    return prior is not None and result.get("items") is not None and any(i not in prior for i in result["items"])


def chk_parts_total_mismatch(result, ctx):
    return result.get("total") is not None and result.get("items") is not None and sum(result["items"]) != result["total"]


def chk_duplicate_in_unique_list(result, ctx):
    items = result.get("items")
    return bool(ctx.get("unique")) and items is not None and len(set(items)) != len(items)


def chk_order_violation(result, ctx):
    order, items = ctx.get("order"), result.get("items")
    if not order or items is None or len(items) < 2:
        return False
    asc = order[1] == "asc"
    return any((a > b) if asc else (a < b) for a, b in zip(items, items[1:]))


def chk_scale_mismatch(result, ctx):
    ref = ctx.get("reference")
    if not ref or ref["field"] not in result["fields"]:
        return False
    return _ratio_is_pow10(result["fields"][ref["field"]], ref["value"])


def chk_stale_echo(result, ctx):
    echo, intended, prior = result.get("echo"), ctx.get("intended_args"), ctx.get("prior_args")
    return echo is not None and intended is not None and prior is not None and echo != intended and echo == prior


CHECKERS = {
    "empty_when_count_stated": chk_empty_when_count_stated, "negative_value": chk_negative_value,
    "id_not_in_prior_list": chk_id_not_in_prior_list, "parts_total_mismatch": chk_parts_total_mismatch,
    "duplicate_in_unique_list": chk_duplicate_in_unique_list, "order_violation": chk_order_violation,
    "scale_mismatch": chk_scale_mismatch, "stale_echo": chk_stale_echo,
}
assert set(CHECKERS) == set(perturb.VIOLATION_TYPES)


def violations(result, ctx):
    return {t for t, f in CHECKERS.items() if f(result, ctx)}


def cause(vtype, result, ctx):
    """'arg' when the call's own (visible) arguments produce the violation, else 'data'."""
    ca = ctx.get("call_args", {})
    if vtype == "id_not_in_prior_list":
        prior = ctx.get("prior_ids") or []
        bad = [i for i in result["items"] if i not in prior]
        return "arg" if bad and ca.get("id") is not None and all(b == ca["id"] for b in bad) and ca["id"] not in prior else "data"
    if vtype == "scale_mismatch":
        f = ctx["reference"]["field"]
        return "arg" if ca.get(f) is not None and ca[f] == result["fields"].get(f) else "data"
    if vtype == "stale_echo":
        return "arg" if ca and ca == result.get("echo") else "data"
    return "data"


ARG_CAPABLE = ("id_not_in_prior_list", "scale_mismatch", "stale_echo")
BENIGN_ODDITIES = ("empty_no_count", "zero_quantity", "equal_parts", "dup_not_unique", "unordered_no_order",
                   "scale_legit_change")


def _ids(rng, stem, n):
    seen = []
    while len(seen) < n:
        v = "%s-%d" % (state.id_stem(stem), rng.randrange(100, 9999))
        if v not in seen:
            seen.append(v)
    return seen


def make_base(vtype, rng, stem, field, cause_kind="data"):
    """Shared content of a violating/valid twin. `field` is a field noun used for numeric result fields."""
    b = {"vtype": vtype, "field": field, "cause": cause_kind, "stem": stem}
    if vtype == "empty_when_count_stated":
        b["count"] = rng.randrange(2, 9)
    elif vtype == "negative_value":
        b["val"] = rng.randrange(2, 60)
    elif vtype == "id_not_in_prior_list":
        ids = _ids(rng, stem, rng.randrange(3, 6))
        b["prior"] = ids[:-1]
        b["extra"] = ids[-1]
        b["pick"] = rng.randrange(len(ids) - 1)
    elif vtype == "parts_total_mismatch":
        b["parts"] = [rng.randrange(2, 40) for _ in range(rng.randrange(3, 6))]
        b["delta"] = rng.choice([-7, -3, 2, 5, 11])
    elif vtype == "duplicate_in_unique_list":
        b["ids"] = _ids(rng, stem, rng.randrange(3, 6))
        b["dup_at"] = rng.randrange(len(b["ids"]))
    elif vtype == "order_violation":
        b["vals"] = sorted(rng.sample(range(2, 99), rng.randrange(3, 6)))
        b["dir"] = rng.choice(["asc", "desc"])
        b["swap"] = rng.randrange(len(b["vals"]) - 1)
    elif vtype == "scale_mismatch":
        b["ref"] = rng.randrange(3, 90)
        b["k"] = rng.choice([10, 100, 1000])
    elif vtype == "stale_echo":
        b["prior_args"] = {"limit": rng.choice([5, 10, 25]), "offset": 0}
        b["intended_args"] = {"limit": rng.choice([50, 100, 200]), "offset": rng.choice([0, 10, 20])}
    else:
        raise ValueError(vtype)
    return b


def materialise(b, violating, oddity=True):
    """(result, ctx) for the violating or the valid twin of a base. With oddity=True the valid twin is the legitimate
    surface ODDITY of the same shape (empty list with count 0, a zero quantity, equal parts) where one exists."""
    v, field = b["vtype"], b["field"]
    result = {"items": None, "fields": {}, "total": None, "echo": None}
    ctx = {"stated_count": None, "prior_ids": None, "reference": None, "unique": False, "order": None,
           "nonneg_fields": [], "intended_args": None, "prior_args": None, "call_args": {}}
    if v == "empty_when_count_stated":
        result["items"] = []
        ctx["stated_count"] = b["count"] if violating else (0 if oddity else None)   # the twin edit lives in the context
    elif v == "negative_value":
        result["fields"][field] = -b["val"] if violating else (0 if oddity else b["val"])
        ctx["nonneg_fields"] = [field]
    elif v == "id_not_in_prior_list":
        ctx["prior_ids"] = list(b["prior"])
        bad = b["extra"]
        picked = b["prior"][b["pick"]]
        shown = bad if violating else picked
        result["items"] = [shown]
        if not violating and oddity and len(b["prior"]) >= 2:               # oddity: neighbours returned too, in reverse order
            result["items"] = [b["prior"][(b["pick"] + 1) % len(b["prior"])], picked]
        ctx["call_args"] = {"id": shown} if b["cause"] == "arg" else {"id": picked}
        if b["cause"] == "arg" and not violating:
            ctx["call_args"] = {"id": picked}
    elif v == "parts_total_mismatch":
        parts = list(b["parts"])
        if not violating and oddity:                                       # equal parts: a legitimate oddity
            parts = [parts[0]] * len(parts)
        result["items"] = parts
        result["total"] = sum(parts) + (b["delta"] if violating else 0)
    elif v == "duplicate_in_unique_list":
        ids = list(b["ids"])
        if violating:
            ids[(b["dup_at"] + 1) % len(ids)] = ids[b["dup_at"]]
        result["items"] = ids
        ctx["unique"] = True
    elif v == "order_violation":
        vals = list(b["vals"])
        if b["dir"] == "desc":
            vals.reverse()
        if violating:
            i = b["swap"]
            vals[i], vals[i + 1] = vals[i + 1], vals[i]
        result["items"] = vals
        ctx["order"] = (field, b["dir"])
    elif v == "scale_mismatch":
        ctx["reference"] = {"field": field, "value": b["ref"]}
        val = b["ref"] * b["k"] if violating else (b["ref"] + (1 + b["k"] % 7) if oddity else b["ref"])
        result["fields"][field] = val
        ctx["call_args"] = {field: val} if (b["cause"] == "arg" and violating) else {field: b["ref"]}
    elif v == "stale_echo":
        ctx["intended_args"] = dict(b["intended_args"])
        ctx["prior_args"] = dict(b["prior_args"])
        echo = dict(b["prior_args"]) if violating else dict(b["intended_args"])
        if not violating and oddity:                                        # oddity: the echo lists its keys in another order
            echo = dict(reversed(list(echo.items())))
        result["echo"] = echo
        ctx["call_args"] = dict(echo) if b["cause"] == "arg" else dict(b["intended_args"])
    return result, ctx


def make_benign(oddity, rng, stem, field):
    """A VALID result with a surface oddity (so 'odd shape' is not a cue for error). Returns (result, ctx)."""
    result = {"items": None, "fields": {}, "total": None, "echo": None}
    ctx = {"stated_count": None, "prior_ids": None, "reference": None, "unique": False, "order": None,
           "nonneg_fields": [], "intended_args": None, "prior_args": None, "call_args": {}}
    if oddity == "empty_no_count":
        result["items"] = []
    elif oddity == "zero_quantity":
        result["fields"][field] = 0
        ctx["nonneg_fields"] = [field]
    elif oddity == "equal_parts":
        n, x = rng.randrange(3, 6), rng.randrange(2, 30)
        result["items"], result["total"] = [x] * n, x * n
    elif oddity == "dup_not_unique":
        ids = _ids(rng, stem, 3)
        result["items"] = [ids[0], ids[1], ids[0]]
    elif oddity == "unordered_no_order":
        result["items"] = rng.sample(range(2, 99), 4)
        if result["items"] == sorted(result["items"]):
            result["items"].reverse()
    elif oddity == "scale_legit_change":
        ref = rng.randrange(3, 90)
        ctx["reference"] = {"field": field, "value": ref}
        result["fields"][field] = ref + rng.choice([1, 2, 3, 7])
    else:
        raise ValueError(oddity)
    return result, ctx


def assert_case(result, ctx, expected):
    """Generator-side assertion: exactly the expected violation set (empty set = valid)."""
    got = violations(result, ctx)
    if got != set(expected):
        raise AssertionError("violations %s != expected %s" % (sorted(got), sorted(expected)))
    return got


def clone(case):
    return copy.deepcopy(case)

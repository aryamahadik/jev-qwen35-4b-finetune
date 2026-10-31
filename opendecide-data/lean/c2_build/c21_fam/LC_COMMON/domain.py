"""Typed finite input domains: declared in the prompt (EQV2), enumerated exhaustively, boundary/pairwise sets (T57, T56g).

A domain is a list of parameter domains for ONE function:
  {"name": p, "t": "int",  "vals": [0, 1, 2, ...]}                    explicit finite int set
  {"name": p, "t": "str",  "vals": ["a", "bc"]}
  {"name": p, "t": "bool"}                                             {false, true}
  {"name": p, "t": "ints", "elem": [0, 3], "maxlen": 2}                all lists up to maxlen over elem (ordered, repeats ok)
  {"name": p, "t": "strs", "elem": ["a"], "maxlen": 2}
A call-sequence domain (stateful modules):
  {"ops": [{"fn": name, "params": [param domains]}], "maxlen": 3}     all sequences up to maxlen over the operation set
Sizes are exact and checked against the T42c bounds (25 to 5,000 points).
"""
import itertools
import random

from . import ir as I

MIN_POINTS = 25
MAX_POINTS = 5000


class DomainError(ValueError):
    pass


def int_dom(name, lo, hi):
    return {"name": name, "t": "int", "vals": list(range(lo, hi + 1))}


def int_set(name, vals):
    return {"name": name, "t": "int", "vals": sorted(set(int(v) for v in vals))}


def str_set(name, vals):
    return {"name": name, "t": "str", "vals": list(vals)}


def list_dom(name, t, elem, maxlen):
    return {"name": name, "t": t, "elem": list(elem), "maxlen": maxlen}


def values(pd):
    t = pd["t"]
    if t in ("int", "str"):
        return list(pd["vals"])
    if t == "bool":
        return [False, True]
    if t in ("ints", "strs"):
        out = []
        for n in range(pd["maxlen"] + 1):
            out.extend(list(c) for c in itertools.product(pd["elem"], repeat=n))
        return out
    raise DomainError(t)


def param_size(pd):
    t = pd["t"]
    if t in ("int", "str"):
        return len(pd["vals"])
    if t == "bool":
        return 2
    return sum(len(pd["elem"]) ** n for n in range(pd["maxlen"] + 1))


def size(dom):
    """Number of points of a function domain (list of param domains) or of a sequence domain."""
    if isinstance(dom, dict) and "ops" in dom:
        per = [sum(_op_size(o) for o in dom["ops"])]
        n = per[0]
        return sum(n ** k for k in range(dom["maxlen"] + 1))
    total = 1
    for pd in dom:
        total *= param_size(pd)
    return total


def _op_size(op):
    s = 1
    for pd in op["params"]:
        s *= param_size(pd)
    return s


def enumerate_points(dom, limit=MAX_POINTS):
    """Yield argument tuples (lists) in a fixed order. Raises if the domain is larger than `limit`."""
    if size(dom) > limit:
        raise DomainError("domain has %d points (limit %d)" % (size(dom), limit))
    for combo in itertools.product(*[values(pd) for pd in dom]):
        yield [list(x) if isinstance(x, list) else x for x in combo]


def enumerate_sequences(sd, limit=MAX_POINTS):
    """Yield sequences: lists of {"fn", "args"}. Includes the empty sequence."""
    if size(sd) > limit:
        raise DomainError("sequence domain has %d points (limit %d)" % (size(sd), limit))
    calls = []
    for op in sd["ops"]:
        for args in enumerate_points(op["params"], limit=10 ** 9):
            calls.append({"fn": op["fn"], "args": args})
    for n in range(sd["maxlen"] + 1):
        for seq in itertools.product(calls, repeat=n):
            yield [{"fn": c["fn"], "args": [list(a) if isinstance(a, list) else a for a in c["args"]]} for c in seq]


def describe(dom):
    """Plain-text declaration shown in the prompt (DOMAIN_DECL)."""
    if isinstance(dom, dict) and "ops" in dom:
        ops = "; ".join("%s(%s)" % (o["fn"], ", ".join(describe_param(pd) for pd in o["params"])) for o in dom["ops"])
        return "every call sequence of length 0 to %d over: %s" % (dom["maxlen"], ops)
    return "; ".join(describe_param(pd) for pd in dom)


def describe_param(pd):
    t = pd["t"]
    if t == "int":
        v = pd["vals"]
        if v == list(range(v[0], v[-1] + 1)) and len(v) > 2:
            return "%s is any integer from %d to %d" % (pd["name"], v[0], v[-1])
        return "%s is one of {%s}" % (pd["name"], ", ".join(str(x) for x in v))
    if t == "str":
        return "%s is one of {%s}" % (pd["name"], ", ".join("'%s'" % x for x in pd["vals"]))
    if t == "bool":
        return "%s is true or false" % pd["name"]
    el = ", ".join(str(x) if t == "ints" else "'%s'" % x for x in pd["elem"])
    return "%s is any list of length 0 to %d with items from {%s}" % (pd["name"], pd["maxlen"], el)


def check_bounds(dom, lo=MIN_POINTS, hi=MAX_POINTS):
    n = size(dom)
    if not lo <= n <= hi:
        raise DomainError("domain size %d outside [%d, %d]" % (n, lo, hi))
    return n


# ----------------------------------------------------------------------------------------------- boundary / pairwise sets
def boundary_points(dom, boundaries, rng, cap=60):
    """Boundary-focused points for a function domain: for each int param its values nearest to the spec thresholds,
    combined with representative values of the other params (pairwise cover, not the full product)."""
    reps = []
    for pd in dom:
        vs = values(pd) if pd["t"] not in ("ints", "strs") else values(pd)
        if pd["t"] == "int":
            near = sorted({v for v in pd["vals"] for b in boundaries if abs(v - b) <= 1} | {pd["vals"][0], pd["vals"][-1]})
            reps.append(near or pd["vals"][:3])
        else:
            reps.append(vs if len(vs) <= 6 else [vs[0], vs[1], vs[len(vs) // 2], vs[-1]])
    pts = []
    for i, ri in enumerate(reps):
        for v in ri:
            base = [r[0] for r in reps]
            base[i] = v
            pts.append(list(base))
    for i in range(len(reps)):
        for j in range(i + 1, len(reps)):
            for a in reps[i]:
                for b in reps[j]:
                    p = [r[0] for r in reps]
                    p[i], p[j] = a, b
                    pts.append(p)
    seen, out = set(), []
    for p in pts:
        key = I.canon(p)
        if key not in seen:
            seen.add(key)
            out.append(p)
    rng.shuffle(out)
    return out[:cap]


def sample_points(dom, rng, n):
    pts = list(enumerate_points(dom, limit=10 ** 7)) if size(dom) <= 20000 else []
    if not pts:
        pts = [[rng.choice(values(pd)) for pd in dom] for _ in range(n)]
    rng.shuffle(pts)
    return pts[:n]

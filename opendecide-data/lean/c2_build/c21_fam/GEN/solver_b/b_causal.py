"""GEN solver B, CAUSAL sub-block (CA-C1 .. CA-C5).

Method (G0-lite section 2, solver B column): SCM simulation by independent code; d-separation via the MORALISED ANCESTRAL GRAPH;
adjustment-set validity by exhaustive subset enumeration of what the set may not contain and by the "G with the arrows out of T
removed" d-separation test (cross-checked against explicit backdoor-path enumeration inside B; a mismatch inside B is a B defect and raises).

Semantics (SCHEMA.md section 2):
    every variable is a whole number 0..7 (mod 8 where stated);
    C1 forced value (do) with the stated functions and the stated root values;
    C2 each non-root variable = (its function + its own hidden input) mod 8; the hidden inputs are abducted from the full record,
       then the variable is forced and the descendants are recomputed with the SAME hidden inputs;
    C3 role by direct arrows: confounder Z->T and Z->O; mediator T->Z and Z->O; collider T->Z and O->Z; else none;
    C4 valid backdoor adjustment set: no member is a descendant of T, and every path from T to O that starts with an arrow into T is blocked;
    C5 yes iff X and Y are d-separated given the listed variables (exogenous variables are independent random inputs, G0-lite ruling C1).
"""
import itertools
import re

from b_questions import read_question
from bcommon import ParseFail, Reject, statements, pick_unique, norm_text, name_list, fnum

V = r"[a-z][a-z0-9_]*"
INTN = r"-?\d+"

VARS_FRAMES = [
    re.compile(r"^The variables (?P<v>.+) each take a whole value from (\d+) to (\d+)$"),
    re.compile(r"^In a model with (?P<v>.+), every variable is a whole number from (\d+) to (\d+)$"),
    re.compile(r"^A system has the variables (?P<v>.+)$"),
    re.compile(r"^Consider variables (?P<v>.+), each a whole number from (\d+) to (\d+)$"),
]
RANGE_FRAME = re.compile(r"^Each takes a whole value from (\d+) to (\d+)$")
WHOLE_MODEL = re.compile(r"^(?:The rules and values given are the whole model|Nothing besides the stated rules and values is part of the model)$")
CLOSED_WORLD = re.compile(r"^(?:Every variable with no arrow into it is an independent random input; the question (?:is about the stated arrows only|concerns only the stated arrows)"
                          r"|Variables without incoming arrows are independent random inputs, and only the stated arrows matter"
                          r"|A variable with no incoming arrow is an independent random input; only the arrows listed count"
                          r"|Root variables are independent random inputs, and the question uses only the arrows stated)$")
ROLE_DEFS = [
    re.compile(r"^Z is a confounder of \(T, O\) if Z points directly to both T and O; a mediator if T points directly to Z and Z points directly to O;"
               r" a collider if both T and O point directly to Z; otherwise none$"),
    re.compile(r"^By direct arrows only: Z is a confounder when it points directly to both T and O, a mediator when T points directly to it and it points directly to O,"
               r" a collider when both T and O point directly to it, and none otherwise$"),
    re.compile(r"^Roles are defined by direct arrows: confounder \(Z -> T and Z -> O\), mediator \(T -> Z and Z -> O\), collider \(T -> Z and O -> Z\), none otherwise$"),
]

EDGE_FRAMES = [
    (re.compile(r"^(%s) is a direct cause of (%s)$" % (V, V)), (1, 2)),
    (re.compile(r"^(%s) directly influences (%s)$" % (V, V)), (1, 2)),
    (re.compile(r"^There is a direct arrow from (%s) to (%s)$" % (V, V)), (1, 2)),
    (re.compile(r"^(%s) depends directly on (%s)$" % (V, V)), (2, 1)),
]

ROOT_FRAMES = [
    re.compile(r"^The outside input of (%s) is (%s)$" % (V, INTN)),
    re.compile(r"^(%s) is set to (%s) from outside$" % (V, INTN)),
    re.compile(r"^(%s) receives the value (%s) from outside$" % (V, INTN)),
    re.compile(r"^(%s) is given as (%s)$" % (V, INTN)),
]
OBS_FRAMES = [
    re.compile(r"^(%s) was (%s)$" % (V, INTN)),
    re.compile(r"^(%s) = (%s)$" % (V, INTN)),
    re.compile(r"^(%s) was seen to be (%s)$" % (V, INTN)),
    re.compile(r"^In the record, (%s) was (%s)$" % (V, INTN)),
]
# function sentences: group 1 = variable, group 2 = function text (parsed by parse_fn). C2 wraps the function with a hidden input.
FN_FRAMES = [
    re.compile(r"^(%s) = (.+)$" % V),
    re.compile(r"^(%s) is computed as (.+)$" % V),
    re.compile(r"^The value of (%s) is (.+)$" % V),
    re.compile(r"^(%s) is (.+)$" % V),
]
NOISE_FRAMES = [   # (regex, group index of the function text, "fn" text may carry its own parentheses)
    re.compile(r"^(%s) is (.+), plus its own hidden input, all taken mod (\d+)$" % V),
    re.compile(r"^(%s) = \((.+) \+ its own hidden input\) mod (\d+)$" % V),
    re.compile(r"^The value of (%s) is (.+) plus its own hidden input, mod (\d+)$" % V),
    re.compile(r"^(%s) is (.+) plus a hidden input of its own, mod (\d+)$" % V),
    re.compile(r"^The value of (%s) is (.+) plus a private hidden input, mod (\d+)$" % V),
]

MOD = 8
LO, HI = 0, 7


# ---------------------------------------------------------------------------------------------------------------------
# functions

class Fn(object):
    """kind in {wsum, thr, sum, min, max, xor}. Evaluate on an assignment dict."""

    def __init__(self, kind, parents, **kw):
        self.kind = kind
        self.parents = parents
        self.kw = kw

    def value(self, env):
        xs = [env[p] for p in self.parents]
        k = self.kind
        if k == "wsum":
            t = sum(w * x for w, x in zip(self.kw["w"], xs))
            return max(self.kw["lo"], min(self.kw["hi"], t))
        if k == "thr":
            return self.kw["hi_val"] if sum(xs) >= self.kw["t"] else self.kw["lo_val"]
        if k == "sum":
            return sum(xs) % self.kw["mod"]
        if k == "min":
            return min(xs)
        if k == "max":
            return max(xs)
        if k == "xor":
            r = 0
            for x in xs:
                r ^= x
            return r
        raise ParseFail("unknown_function_kind", k)

    def canon(self):
        k = self.kind
        d = {"kind": k, "parents": list(self.parents)}
        if k == "wsum":
            d["w"] = list(self.kw["w"])
            if (self.kw["lo"], self.kw["hi"]) != (LO, HI):
                d["lo"], d["hi"] = self.kw["lo"], self.kw["hi"]
        elif k == "thr":
            d["t"] = self.kw["t"]
            if (self.kw["hi_val"], self.kw["lo_val"]) != (1, 0):
                d["hi_val"], d["lo_val"] = self.kw["hi_val"], self.kw["lo_val"]
        elif k == "sum":
            if self.kw["mod"] != MOD:
                d["mod"] = self.kw["mod"]
        return d


_TERM = re.compile(r"\s*([+-]?)\s*(\d+)\*(%s)" % V)


def parse_fn(text, mod_default=None):
    t = text.strip()
    if t.startswith("(") and t.endswith(")") and t.count("(") == 1:
        t = t[1:-1].strip()
    # weighted sum clipped
    m = re.match(r"^(.+), limited to the range (\d+) to (\d+)$", t)
    if m:
        body = m.group(1)
        pos = 0
        ws, ps = [], []
        while pos < len(body):
            mt = _TERM.match(body, pos)
            if not mt:
                raise ParseFail("weighted_sum_term", body)
            w = int(mt.group(2))
            if mt.group(1) == "-":
                w = -w
            ws.append(w)
            ps.append(mt.group(3))
            pos = mt.end()
        if not ps:
            raise ParseFail("weighted_sum_empty", text)
        return Fn("wsum", ps, w=ws, lo=int(m.group(2)), hi=int(m.group(3)))
    # threshold: "A if x [plus y ...] is at least T, otherwise B"
    m = re.match(r"^(\d+) if (.+) is at least (\d+), otherwise (\d+)$", t)
    if m:
        ps = [p.strip() for p in re.split(r"\s+plus\s+", m.group(2))]
        return Fn("thr", ps, t=int(m.group(3)), hi_val=int(m.group(1)), lo_val=int(m.group(4)))
    # sum mod m
    m = re.match(r"^the sum of (.+), mod (\d+)$", t)
    if m:
        return Fn("sum", name_list(m.group(1)), mod=int(m.group(2)))
    m = re.match(r"^the sum of (.+)$", t)
    if m and mod_default:
        return Fn("sum", name_list(m.group(1)), mod=mod_default)
    # min / max
    m = re.match(r"^the (larger|largest) of (.+)$", t)
    if m:
        return Fn("max", name_list(m.group(2)))
    m = re.match(r"^the (smaller|smallest) of (.+)$", t)
    if m:
        return Fn("min", name_list(m.group(2)))
    # xor of 3-bit values
    m = re.match(r"^(.+) combined by bitwise xor on their (\d+)-bit values$", t)
    if m:
        return Fn("xor", name_list(m.group(1)))
    raise ParseFail("unknown_function_text", text)


# ---------------------------------------------------------------------------------------------------------------------
# parsing shared by all forms

def _vars(stmts):
    names = None
    keep = []
    for s in stmts:
        hit = False
        for rx in VARS_FRAMES:
            m = rx.match(s)
            if m:
                if names is not None:
                    raise ParseFail("variables_stated_twice", s)
                names = name_list(m.group("v"))
                hit = True
                break
        if hit:
            continue
        if RANGE_FRAME.match(s):
            continue
        m = re.match(r"^Each takes a whole value from (\d+) to (\d+)$", s)
        keep.append(s)
    if names is None:
        raise ParseFail("variables_not_found", "")
    return names, keep


def _check_range(stem):
    # the range sentence must be 0..7 everywhere it is stated
    for a, b in re.findall(r"from (\d+) to (\d+)", stem):
        pass
    return True


def _topo(vars_, parents):
    """parents: dict var -> list of parent names. Returns topological order; raises on cycle / unknown name."""
    order, seen, onstack = [], set(), set()

    def visit(v):
        if v in seen:
            return
        if v in onstack:
            raise ParseFail("cyclic_graph", v)
        onstack.add(v)
        for p in parents.get(v, []):
            if p not in vars_:
                raise ParseFail("unknown_variable", p)
            visit(p)
        onstack.discard(v)
        seen.add(v)
        order.append(v)

    for v in vars_:
        visit(v)
    return order


# ---------------------------------------------------------------------------------------------------------------------
# C1 / C2

def solve_c1(stem, options):
    key, q, remainder = read_question("q.CA-C1", stem)
    names, body = _vars(statements(remainder))
    roots, fns = {}, {}
    for s in body:
        if WHOLE_MODEL.match(s):
            continue
        s2 = re.sub(r"^Rule: ", "", s)
        done = False
        for rx in ROOT_FRAMES:
            m = rx.match(s2)
            if m:
                roots[m.group(1)] = int(m.group(2))
                done = True
                break
        if done:
            continue
        for rx in FN_FRAMES:
            m = rx.match(s2)
            if m:
                fns[m.group(1)] = parse_fn(m.group(2))
                done = True
                break
        if not done:
            raise ParseFail("sentence_not_understood", s)
    for v in names:
        if (v in roots) == (v in fns):
            raise ParseFail("variable_not_exactly_root_or_function", v)
    target, dvar, dval = q["target"], q["do_var"], int(q["do_val"])
    if target not in names or dvar not in names:
        raise ParseFail("unknown_variable", "")
    order = _topo(names, dict((v, f.parents) for v, f in fns.items()))
    env = {}
    for v in order:
        if v == dvar:
            env[v] = dval
        elif v in roots:
            env[v] = roots[v]
        else:
            env[v] = fns[v].value(env)
    ans = env[target]
    want = str(ans)
    idx = pick_unique([i for i, o in enumerate(options) if o.strip() == want], want)
    pb = {"form": "CA-C1", "vars": list(names), "functions": dict((v, f.canon()) for v, f in fns.items()),
          "do": {"var": dvar, "val": dval}, "target": target, "roots": dict(roots)}
    return {"answer_index": idx, "answer_text": want, "parse": pb, "info": {}}


def solve_c2(stem, options):
    key, q, remainder = read_question("q.CA-C2", stem)
    names, body = _vars(statements(remainder))
    fns, obs = {}, {}
    for s in body:
        if WHOLE_MODEL.match(s):
            continue
        done = False
        for rx in NOISE_FRAMES:
            m = rx.match(s)
            if m:
                if int(m.group(3)) != MOD:
                    raise ParseFail("hidden_input_modulus", s)
                fns[m.group(1)] = parse_fn(m.group(2), mod_default=MOD)
                done = True
                break
        if done:
            continue
        for rx in OBS_FRAMES:
            m = rx.match(s)
            if m:
                obs[m.group(1)] = int(m.group(2))
                done = True
                break
        if not done:
            raise ParseFail("sentence_not_understood", s)
    for v in names:
        if v not in obs:
            raise ParseFail("record_incomplete", v)
    target, dvar, dval = q["target"], q["do_var"], int(q["do_val"])
    if target not in names or dvar not in names:
        raise ParseFail("unknown_variable", "")
    order = _topo(names, dict((v, f.parents) for v, f in fns.items()))
    # abduction: the hidden input of each function variable from the full record
    hidden = {}
    for v, f in fns.items():
        hidden[v] = (obs[v] - f.value(obs)) % MOD
    env = {}
    for v in order:
        if v == dvar:
            env[v] = dval
        elif v in fns:
            env[v] = (fns[v].value(env) + hidden[v]) % MOD
        else:
            env[v] = obs[v]
    ans = env[target]
    want = str(ans)
    idx = pick_unique([i for i, o in enumerate(options) if o.strip() == want], want)
    pb = {"form": "CA-C2", "vars": list(names), "functions": dict((v, f.canon()) for v, f in fns.items()),
          "do": {"var": dvar, "val": dval}, "target": target, "observed": dict(obs)}
    return {"answer_index": idx, "answer_text": want, "parse": pb, "info": {}}


# ---------------------------------------------------------------------------------------------------------------------
# graph forms

def _graph(stmts):
    edges = []
    rest = []
    for s in stmts:
        done = False
        for rx, (ia, ib) in EDGE_FRAMES:
            m = rx.match(s)
            if m:
                edges.append((m.group(ia), m.group(ib)))
                done = True
                break
        if not done:
            rest.append(s)
    return edges, rest


def _graph_common(remainder_text, q):
    names, body = _vars(statements(remainder_text))
    edges, rest = _graph(body)
    rest = [s for s in rest if not CLOSED_WORLD.match(s) and not any(r.match(s) for r in ROLE_DEFS)]
    if rest:
        raise ParseFail("unread_sentences", str(rest))
    if len(set(edges)) != len(edges):
        raise ParseFail("duplicate_edge", "")
    for a, b in edges:
        if a not in names or b not in names:
            raise ParseFail("edge_names_unknown_variable", "%s %s" % (a, b))
        if a == b:
            raise ParseFail("self_loop", a)
    parents = dict((v, []) for v in names)
    for a, b in edges:
        parents[b].append(a)
    _topo(names, parents)   # acyclic
    return names, edges, q


def _children(edges):
    ch = {}
    for a, b in edges:
        ch.setdefault(a, set()).add(b)
    return ch


def descendants(edges, v):
    ch = _children(edges)
    seen, stack = set(), [v]
    while stack:
        x = stack.pop()
        for y in ch.get(x, ()):
            if y not in seen:
                seen.add(y)
                stack.append(y)
    return seen


def ancestors_closed(edges, targets):
    par = {}
    for a, b in edges:
        par.setdefault(b, set()).add(a)
    seen = set(targets)
    stack = list(targets)
    while stack:
        x = stack.pop()
        for p in par.get(x, ()):
            if p not in seen:
                seen.add(p)
                stack.append(p)
    return seen


def d_separated(edges, x, y, given):
    """Moralised ancestral graph test: keep the ancestors of {x, y} U given, marry co-parents, drop directions, delete `given`, test connectivity."""
    given = set(given)
    keep = ancestors_closed(edges, {x, y} | given)
    par = {}
    for a, b in edges:
        if a in keep and b in keep:
            par.setdefault(b, set()).add(a)
    und = {}

    def link(p, q):
        und.setdefault(p, set()).add(q)
        und.setdefault(q, set()).add(p)

    for child, ps in par.items():
        for p in ps:
            link(p, child)
        for p, q in itertools.combinations(sorted(ps), 2):
            link(p, q)
    if x in given or y in given:
        raise Reject("query_variable_in_conditioning_set", "")
    seen, stack = {x}, [x]
    while stack:
        a = stack.pop()
        for b in und.get(a, ()):
            if b in given or b in seen:
                continue
            seen.add(b)
            stack.append(b)
    return y not in seen


def backdoor_valid_by_separation(edges, t, o, zs):
    zs = set(zs)
    if t in zs or o in zs:
        return False
    if zs & descendants(edges, t):
        return False
    cut = [(a, b) for (a, b) in edges if a != t]   # remove every arrow out of T
    return d_separated(cut, t, o, zs)


def backdoor_valid_by_paths(edges, t, o, zs):
    """Explicit enumeration of simple undirected paths from T to O whose first edge points INTO T; each must be blocked by zs."""
    zs = set(zs)
    if t in zs or o in zs:
        return False
    if zs & descendants(edges, t):
        return False
    directed = set(edges)
    nbrs = {}
    for a, b in edges:
        nbrs.setdefault(a, set()).add(b)
        nbrs.setdefault(b, set()).add(a)
    desc_cache = {}

    def desc_or_self(v):
        if v not in desc_cache:
            desc_cache[v] = descendants(edges, v) | {v}
        return desc_cache[v]

    def blocked(path):
        for i in range(1, len(path) - 1):
            prev, cur, nxt = path[i - 1], path[i], path[i + 1]
            collider = (prev, cur) in directed and (nxt, cur) in directed
            if collider:
                if not (desc_or_self(cur) & zs):
                    return True
            else:
                if cur in zs:
                    return True
        return False

    def walk(path):
        cur = path[-1]
        if cur == o:
            yield list(path)
            return
        for nb in sorted(nbrs.get(cur, ())):
            if nb in path:
                continue
            path.append(nb)
            for p in walk(path):
                yield p
            path.pop()

    for first in sorted(nbrs.get(t, ())):
        if (first, t) not in directed:
            continue   # first edge must point into T
        for p in walk([t, first]):
            if not blocked(p):
                return False
    return True


def _edges_sorted(edges):
    return [list(e) for e in sorted(edges)]


def solve_c3(stem, options):
    key, q, remainder = read_question("q.CA-C3", stem)
    names, edges, q = _graph_common(remainder, q)
    z, t, o = q["z"], q["t"], q["o"]
    for v in (z, t, o):
        if v not in names:
            raise ParseFail("unknown_variable", v)
    es = set(edges)
    if (z, t) in es and (z, o) in es:
        role = "confounder"
    elif (t, z) in es and (z, o) in es:
        role = "mediator"
    elif (t, z) in es and (o, z) in es:
        role = "collider"
    else:
        role = "none"
    idx = pick_unique([i for i, x in enumerate(options) if norm_text(x) == role], role)
    pb = {"form": "CA-C3", "vars": list(names), "edges": _edges_sorted(edges), "z": z, "t": t, "o": o}
    return {"answer_index": idx, "answer_text": role, "parse": pb, "info": {}}


def _parse_set(text):
    m = re.match(r"^\{(.*)\}$", text.strip())
    if not m:
        raise ParseFail("option_not_a_set", text)
    inner = m.group(1).strip()
    if not inner:
        return []
    return [x.strip() for x in inner.split(",")]


def solve_c4(stem, options):
    key, q, remainder = read_question("q.CA-C4", stem)
    names, edges, q = _graph_common(remainder, q)
    t, o = q["t"], q["o"]
    sets = [_parse_set(x) for x in options]
    hits = []
    for i, zs in enumerate(sets):
        for v in zs:
            if v not in names:
                raise ParseFail("option_names_unknown_variable", v)
        a = backdoor_valid_by_separation(edges, t, o, zs)
        b = backdoor_valid_by_paths(edges, t, o, zs)
        if a != b:
            raise Reject("solver_b_internal_disagreement", "backdoor by separation vs by paths")
        if a:
            hits.append(i)
    # exhaustive enumeration of every subset of the other variables: the options that are valid must be exactly the valid subsets among them
    others = [v for v in names if v not in (t, o)]
    valid_subsets = set()
    for r in range(len(others) + 1):
        for comb in itertools.combinations(others, r):
            if backdoor_valid_by_separation(edges, t, o, comb):
                valid_subsets.add(frozenset(comb))
    by_enumeration = [i for i, zs in enumerate(sets) if frozenset(zs) in valid_subsets]
    if by_enumeration != hits:
        raise Reject("solver_b_internal_disagreement", "backdoor by subset enumeration")
    idx = pick_unique(hits, "valid adjustment set")
    pb = {"form": "CA-C4", "vars": list(names), "edges": _edges_sorted(edges), "t": t, "o": o, "options": [sorted(s) for s in sets]}
    return {"answer_index": idx, "answer_text": options[idx], "parse": pb, "info": {}}


def solve_c5(stem, options):
    key, q, remainder = read_question("q.CA-C5", stem)
    names, edges, q = _graph_common(remainder, q)
    x, y = q["x"], q["y"]
    zt = q["zset"].strip()
    given = [] if zt == "nothing" else name_list(zt)
    for v in [x, y] + given:
        if v not in names:
            raise ParseFail("unknown_variable", v)
    sep = d_separated(edges, x, y, given)
    want = "yes" if sep else "no"
    idx = pick_unique([i for i, o in enumerate(options) if norm_text(o) == want], want)
    pb = {"form": "CA-C5", "vars": list(names), "edges": _edges_sorted(edges), "x": x, "y": y, "given": list(given)}
    return {"answer_index": idx, "answer_text": "Yes" if sep else "No", "parse": pb, "info": {}}


def solve(form, stem, options):
    return {"CA-C1": solve_c1, "CA-C2": solve_c2, "CA-C3": solve_c3, "CA-C4": solve_c4, "CA-C5": solve_c5}[form](stem, options)

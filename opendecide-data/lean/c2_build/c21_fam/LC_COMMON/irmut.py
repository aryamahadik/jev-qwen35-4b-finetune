"""Our own AST mutator over the IR (operator ids MUT-01..MUT-14 and multi-site variants MS-01..MS-04).

Written from the operator classes listed in the T42c/T57 G0-lites and public AST knowledge. Nothing is copied from any
existing mutator. Because the IR is shared, the Go and bash analogues are the same operators on the same tree.

A *site* is {"op": id, "fn": function name, "path": path inside the function body, "variant": int}. `apply` returns a new
module (deep copy) or None when the edit would not type-check, would change nothing, or breaks an IR rule. Whether a
mutant is semantically equivalent is NOT decided here: it is decided by an execution witness (or, on CPU, by the IR
interpreter as a spec expectation).

PARTITION (T57 gate b "independent mutant pool"): bug injection and candidate building use INJECT_OPS; the strength
pool uses STRENGTH_OPS; the two sets are disjoint.
"""
from . import ir as I

INJECT_OPS = ("MUT-01", "MUT-02", "MUT-04", "MUT-05", "MUT-07", "MUT-09", "MUT-11")
STRENGTH_OPS = ("MUT-03", "MUT-06", "MUT-08", "MUT-10", "MUT-12", "MUT-13", "MUT-14")
ALL_OPS = tuple("MUT-%02d" % k for k in range(1, 15))
MULTI_OPS = {"MS-01": "MUT-04", "MS-02": "MUT-02", "MS-03": "MUT-01", "MS-04": "MUT-03"}
assert not set(INJECT_OPS) & set(STRENGTH_OPS)
assert set(INJECT_OPS) | set(STRENGTH_OPS) == set(ALL_OPS)

_NEG = {"<": ">=", "<=": ">", ">": "<=", ">=": "<", "==": "!=", "!=": "=="}
_BOUND = {"<": "<=", "<=": "<", ">": ">=", ">=": ">"}
_ARITH_SWAP = {"+": "-", "-": "+", "*": "+", "//": "%", "%": "//"}


def _replace(node, new):
    node[:] = new


# ----------------------------------------------------------------------------------------------- site enumeration
def _parent_head(body, path):
    """Head of the nearest enclosing statement (for 'inside a loop' checks)."""
    heads = []
    cur = body
    for k in path[:-1]:
        cur = cur[k]
        if isinstance(cur, list) and cur and isinstance(cur[0], str):
            heads.append(cur[0])
    return heads


def _in_loop(body, path):
    return any(h in ("for", "each") for h in _parent_head(body, path))


def sites_for(op, fn):
    """All sites of operator `op` in function dict `fn`: list of (path, variant)."""
    body = fn["body"]
    out = []
    nodes = list(I.walk(body))
    if op == "MUT-01":
        for p, n in nodes:
            if n[0] == "bin" and n[1] in _NEG:
                out.append((p, 0))
    elif op == "MUT-02":
        for p, n in nodes:
            if n[0] == "bin" and n[1] in _BOUND:
                out.append((p, 0))
    elif op == "MUT-03":
        for p, n in nodes:
            if n[0] == "bin" and n[1] in _ARITH_SWAP:
                out.append((p, 0))
            elif n[0] == "bin" and n[1] in ("and", "or"):
                out.append((p, 0))
            elif n[0] == "bin" and n[1] in ("<", "<=", ">", ">="):
                out.append((p, 1))          # relational -> !=
    elif op == "MUT-04":
        for p, n in nodes:
            if n[0] == "int" and not _is_zpad_width(body, p):
                out.append((p, 0))
                out.append((p, 1))
    elif op == "MUT-05":
        for p, n in nodes:
            if n[0] == "if" and not n[3] and n[2] and n[2][-1][0] in ("ret", "raise"):
                out.append((p, 0))
    elif op == "MUT-06":
        for p, n in nodes:
            if n[0] in ("fcall", "mcall") and len(n[2]) >= 2:
                out.append((p, 0))
            elif n[0] == "bin" and n[1] in ("-", "<", "<=", ">", ">=", "//", "%"):
                out.append((p, 1))
    elif op == "MUT-07":
        for p, n in nodes:
            if n[0] == "ret":
                for var in range(3):
                    out.append((p, var))
    elif op == "MUT-08":
        for p, n in nodes:
            if n[0] == "for":
                out += [(p, 0), (p, 1), (p, 2)]
    elif op == "MUT-09":
        for p, n in nodes:
            if n[0] == "let" and n[2] == I.INT and n[3][0] == "int" and _followed_by_loop(body, p):
                out += [(p, 0), (p, 1)]
    elif op == "MUT-10":
        for p, n in nodes:
            if n[0] in ("set", "setf", "push", "sidx") and p:
                out.append((p, 0))
    elif op == "MUT-11":
        for p, n in nodes:
            if n[0] == "idx":
                out += [(p, 0), (p, 1)]
            elif n[0] == "sidx":
                out += [(p, 2), (p, 3)]
    elif op == "MUT-12":
        for p, n in nodes:
            if n[0] == "zpad":
                out += [(p, 0), (p, 1)]
            elif n[0] == "bin" and n[1] == "++":
                out.append((p, 2))
            elif n[0] == "str" and len(n[1]) == 1 and not n[1].isalnum():
                out.append((p, 3))
    elif op == "MUT-13":
        for p, n in nodes:
            if n[0] == "let" and n[3][0] in ("int", "str") and not _followed_by_loop(body, p):
                out += [(p, 0)]
    elif op == "MUT-14":
        for p, n in nodes:
            if n[0] in ("ret", "raise") and p and _in_loop(body, p):
                out.append((p, 0))
    else:
        raise KeyError(op)
    return out


def _is_zpad_width(body, p):
    if len(p) < 1:
        return False
    try:
        parent = I.get_at(body, p[:-1])
    except (IndexError, TypeError):
        return False
    return isinstance(parent, list) and parent and parent[0] == "zpad" and p[-1] == 2


def _followed_by_loop(body, path):
    blk = I.get_at(body, path[:-1]) if len(path) > 1 else body
    k = path[-1]
    var = I.get_at(body, path)[1]
    for later in blk[k + 1:]:
        if later[0] in ("for", "each"):
            for _, n in I.walk(later):
                if n[0] == "set" and n[1] == var:
                    return True
    return False


# ----------------------------------------------------------------------------------------------- application
def _fresh(x):
    return I.clone(x)


def _apply_inplace(op, variant, body, path, ret_type=None):
    """Mutate the (already cloned) function body at `path`. Returns False when the edit is a no-op/inapplicable."""
    node = I.get_at(body, path)
    h = node[0]
    if op == "MUT-01":
        node[1] = _NEG[node[1]]
    elif op == "MUT-02":
        node[1] = _BOUND[node[1]]
    elif op == "MUT-03":
        if h == "bin" and node[1] in _ARITH_SWAP:
            node[1] = _ARITH_SWAP[node[1]]
        elif h == "bin" and node[1] == "and":
            node[1] = "or"
        elif h == "bin" and node[1] == "or":
            node[1] = "and"
        else:
            node[1] = "!="
    elif op == "MUT-04":
        node[1] = node[1] + (1 if variant == 0 else -1)
    elif op == "MUT-05":
        I.get_at(body, path[:-1]).pop(path[-1])
    elif op == "MUT-06":
        if h in ("fcall", "mcall"):
            a = node[2]
            if a[0] == a[1]:
                return False
            a[0], a[1] = a[1], a[0]
        else:
            node[2], node[3] = node[3], node[2]
    elif op == "MUT-07":
        e = node[1]
        if variant == 0:
            if ret_type == I.INT:
                node[1] = ["int", 0]
            elif ret_type == I.BOOL:
                node[1] = ["not", e]
            elif ret_type == I.STR:
                node[1] = ["str", ""]
            else:
                return False
        elif variant == 1:
            if ret_type == I.INT:
                node[1] = ["int", 1]
            elif ret_type == I.BOOL:
                node[1] = ["bool", True]
            elif ret_type == I.STR:
                node[1] = ["str", "x"]
            else:
                return False
        else:
            # return the first operand of a binary expression, if any
            if e[0] == "bin" and e[1] not in ("and", "or", "++") and ret_type == I.INT:
                node[1] = e[2]
            elif e[0] in ("min", "max"):
                node[1] = e[1]
            else:
                return False
    elif op == "MUT-08":
        if variant == 0:
            node[3] = ["bin", "+", node[3], ["int", 1]]
        elif variant == 1:
            node[3] = ["bin", "-", node[3], ["int", 1]]
        else:
            node[2] = ["bin", "+", node[2], ["int", 1]]
    elif op == "MUT-09":
        node[3][1] = node[3][1] + 1 if variant == 0 else (1 if node[3][1] == 0 else 0)
    elif op in ("MUT-10", "MUT-14"):
        I.get_at(body, path[:-1]).pop(path[-1])
    elif op == "MUT-11":
        if h == "idx":
            node[2] = ["bin", "+" if variant == 0 else "-", node[2], ["int", 1]]
        else:
            node[2] = ["bin", "+" if variant == 2 else "-", node[2], ["int", 1]]
    elif op == "MUT-12":
        if h == "zpad":
            node[2] = ["int", max(1, node[2][1] + (1 if variant == 0 else -1))]
        elif h == "bin":
            node[2], node[3] = node[3], node[2]
        else:
            node[1] = "-" if node[1] != "-" else ":"
    elif op == "MUT-13":
        lit = node[3]
        if lit[0] == "int":
            lit[1] = lit[1] + 1
        else:
            lit[1] = lit[1] + "x" if len(lit[1]) < 8 else lit[1][:-1]
    else:
        raise KeyError(op)
    return True


def apply_site(mod, site):
    """Return a mutated deep copy of `mod`, or None when the mutation is invalid or changes nothing."""
    new = I.clone(mod)
    fn = I.functions(new)[site["fn"]]
    sites = site["sites"] if "sites" in site else [site]
    # apply deeper/later paths first so earlier paths stay valid
    order = sorted(sites, key=lambda s: tuple(s["path"]), reverse=True)
    for s in order:
        if not _apply_inplace(s["op"], s["variant"], fn["body"], tuple(s["path"]), fn["ret"]):
            return None
    if I.canon(new["funcs"]) == I.canon(mod["funcs"]):
        return None
    try:
        I.check_module(new)
    except I.IRError:
        return None
    return new


def enumerate_sites(mod, ops, fn_names=None):
    """All single-site mutations of `ops` in the named functions (default: every function)."""
    out = []
    for fn in mod["funcs"]:
        if fn_names is not None and fn["name"] not in fn_names:
            continue
        for op in ops:
            for path, variant in sites_for(op, fn):
                out.append({"op": op, "fn": fn["name"], "path": list(path), "variant": variant})
    return out


def multi_sites(mod, ms_id, rng, fn_names=None, k=2):
    """A multi-site mutation: operator MULTI_OPS[ms_id] applied at k distinct sites of ONE function (MS-02: all)."""
    op = MULTI_OPS[ms_id]
    cands = []
    for fn in mod["funcs"]:
        if fn_names is not None and fn["name"] not in fn_names:
            continue
        ss = [{"op": op, "fn": fn["name"], "path": list(p), "variant": var} for p, var in sites_for(op, fn)]
        if len(ss) >= 2:
            cands.append(ss)
    if not cands:
        return None
    ss = rng.choice(cands)
    if ms_id == "MS-02":
        chosen = ss
    else:
        # distinct paths only (MUT-04 offers two variants per literal)
        seen, uniq = set(), []
        for s in ss:
            key = tuple(s["path"])
            if key not in seen:
                seen.add(key)
                uniq.append(s)
        if len(uniq) < 2:
            return None
        chosen = rng.sample(uniq, min(k, len(uniq)))
    return {"op": ms_id, "fn": chosen[0]["fn"], "path": chosen[0]["path"], "variant": 0, "sites": chosen}


def mutants(mod, ops, fn_names=None, limit=None, rng=None):
    """Valid mutants: [(site, new_module)]. Optional shuffle + limit for sampling."""
    ss = enumerate_sites(mod, ops, fn_names)
    if rng is not None:
        rng.shuffle(ss)
    out = []
    for s in ss:
        m = apply_site(mod, s)
        if m is not None:
            out.append((s, m))
            if limit and len(out) >= limit:
                break
    return out

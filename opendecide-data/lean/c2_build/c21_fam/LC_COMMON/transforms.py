"""Semantics-preserving transforms EQ-YES-1..EQ-YES-5 (T42c equivalence-YES constructions; also T57 ALTFIX / rename twins).

Registry:
  EQ-YES-1 rename locals            EQ-YES-4 algebraic identity
  EQ-YES-2 reorder independent statements   EQ-YES-5 early-return restructure
  EQ-YES-3 loop swap (`each x in xs` <-> counted loop over indexes: the language-native iteration swap)
Each transform takes a function dict and returns a NEW function dict or None when it does not apply. Applying one is
equivalent by construction; T42c still requires an exhaustive run over the declared domain before a YES label stands.
New names come from Idents (namespace.py, TRAINING salt).
"""
from . import ir as I

IDS = ("EQ-YES-1", "EQ-YES-2", "EQ-YES-3", "EQ-YES-4", "EQ-YES-5")


def _pure(e):
    """No calls, no indexing (it may raise), no field reads (a swap with a state write would not be independent)."""
    for _, n in I.walk(e):
        if n[0] in ("fcall", "mcall", "idx", "field"):
            return False
    return True


def _reads(node):
    return {n[1] for _, n in I.walk(node) if n[0] == "var"}


def _with_fn(fn, body):
    g = dict(fn)
    g["body"] = body
    return g


# ----------------------------------------------------------------------------------------------- EQ-YES-1
def rename_locals(fn, ids, tag):
    f = I.clone(fn)
    params = {p[0] for p in f["params"]}
    declared = []
    for _, n in I.walk(f["body"]):
        if n[0] in ("let", "popto", "shiftto", "for", "each") and n[1] not in params and n[1] not in declared:
            declared.append(n[1])
    if not declared:
        return None
    mapping = {old: ids.var("%s.rn.%d" % (tag, k)) for k, old in enumerate(declared)}
    for _, n in I.walk(f["body"]):
        if n[0] in ("let", "set", "popto", "shiftto", "for", "each") and n[1] in mapping:
            n[1] = mapping[n[1]]
        elif n[0] == "var" and n[1] in mapping:
            n[1] = mapping[n[1]]
    return f


# ----------------------------------------------------------------------------------------------- EQ-YES-2
def _defs(st):
    return {st[1]} if st[0] in ("let", "popto", "shiftto") else set()


def _may_raise(e):
    return any(n[0] in ("fcall", "mcall", "idx") for _, n in I.walk(e))


def _rw(st):
    """(reads, writes) of a simple assignment statement, or None. Fields are tagged 'f:'."""
    h = st[0]
    if h in ("let", "set"):
        rhs = st[3] if h == "let" else st[2]
        reads = {("v:" + n[1]) for _, n in I.walk(rhs) if n[0] == "var"} | {("f:" + n[1]) for _, n in I.walk(rhs) if n[0] == "field"}
        return reads, {"v:" + st[1]}, rhs
    if h == "setf":
        rhs = st[2]
        reads = {("v:" + n[1]) for _, n in I.walk(rhs) if n[0] == "var"} | {("f:" + n[1]) for _, n in I.walk(rhs) if n[0] == "field"}
        return reads, {"f:" + st[1]}, rhs
    return None


def reorder_independent(fn, rng):
    f = I.clone(fn)
    cands = []
    blocks = [f["body"]]
    for path, n in I.walk(f["body"]):
        if n[0] == "if":
            blocks += [n[2], n[3]]
        elif n[0] == "for":
            blocks.append(n[4])
        elif n[0] == "each":
            blocks.append(n[3])
    for blk in blocks:
        for k in range(len(blk) - 1):
            a, b = _rw(blk[k]), _rw(blk[k + 1])
            if a is None or b is None:
                continue
            ra, wa, ea = a
            rb, wb, eb = b
            if blk[k][0] == "let" and blk[k][2] in I.LISTS or blk[k + 1][0] == "let" and blk[k + 1][2] in I.LISTS:
                continue
            if _may_raise(ea) and _may_raise(eb):
                continue                                    # which exception comes first would change
            if wa & (rb | wb) or wb & ra:
                continue
            cands.append((blk, k))
    if not cands:
        return None
    blk, k = rng.choice(cands)
    blk[k], blk[k + 1] = blk[k + 1], blk[k]
    return f


# ----------------------------------------------------------------------------------------------- EQ-YES-3
def loop_swap(fn, ids, tag, mod_types):
    """`each x xs: body` -> `for i 0..len(xs): let x = idx(xs, i); body`. Only when xs is a param/field/const and the
    element variable is read in the body."""
    f = I.clone(fn)
    params = {p[0]: p[1] for p in f["params"]}
    for path, n in I.walk(f["body"]):
        if n[0] == "each":
            xs = n[2]
            ok = xs[0] in ("field", "const") or (xs[0] == "var" and xs[1] in params)
            if not ok:
                continue
            used = any(m[0] == "var" and m[1] == n[1] for _, m in I.walk(n[3]))
            if not used:
                continue
            ety = I.ELEM[mod_types(xs)]
            idx_name = ids.var("%s.ls" % tag)
            new = ["for", idx_name, ["int", 0], ["len", I.clone(xs)],
                   [["let", n[1], ety, ["idx", I.clone(xs), ["var", idx_name]]]] + n[3]]
            I.set_at(f["body"], path, new) if path else None
            return f
    return None


# ----------------------------------------------------------------------------------------------- EQ-YES-4
def algebraic(fn, rng, mod_types):
    f = I.clone(fn)
    cands = []
    for path, n in I.walk(f["body"]):
        if n[0] == "bin" and n[1] == "+" and _pure(n[2]) and _pure(n[3]):
            cands.append((path, "swap_add"))
        if n[0] == "bin" and n[1] == "*" and n[3][0] == "int" and n[3][1] == 2 and _pure(n[2]):
            cands.append((path, "dbl"))
        if n[0] == "bin" and n[1] in ("<", "<=", ">", ">=") and _pure(n[2]) and _pure(n[3]):
            cands.append((path, "flip_cmp"))
        if n[0] == "not" and n[1][0] == "bin" and n[1][1] in ("<", "<=", ">", ">="):
            cands.append((path, "not_cmp"))
        if n[0] in ("min", "max") and _pure(n[1]) and _pure(n[2]):
            cands.append((path, "minmax"))
        if n[0] == "bin" and n[1] == "-" and _pure(n[2]) and _pure(n[3]):
            cands.append((path, "sub_neg"))
    cands = [c for c in cands if c[0]]          # a root expression cannot be replaced in place here
    if not cands:
        return None
    path, kind = rng.choice(cands)
    n = I.get_at(f["body"], path)
    flip = {"<": ">", "<=": ">=", ">": "<", ">=": "<="}
    neg = {"<": ">=", "<=": ">", ">": "<=", ">=": "<"}
    if kind == "swap_add":
        new = ["bin", "+", n[3], n[2]]
    elif kind == "dbl":
        new = ["bin", "+", n[2], I.clone(n[2])]
    elif kind == "flip_cmp":
        new = ["bin", flip[n[1]], n[3], n[2]]
    elif kind == "not_cmp":
        new = ["bin", neg[n[1][1]], n[1][2], n[1][3]]
    elif kind == "minmax":
        new = ["cond", ["bin", "<=" if n[0] == "min" else ">=", n[1], n[2]], I.clone(n[1]), I.clone(n[2])]
    else:
        new = ["bin", "+", n[2], ["bin", "-", ["int", 0], n[3]]]
    I.set_at(f["body"], path, new)
    return f


# ----------------------------------------------------------------------------------------------- EQ-YES-5
def early_return(fn, rng):
    f = I.clone(fn)
    cands = []
    blocks = [f["body"]]
    for path, n in I.walk(f["body"]):
        if n[0] == "if":
            blocks += [n[2], n[3]]
        elif n[0] == "for":
            blocks.append(n[4])
        elif n[0] == "each":
            blocks.append(n[3])
    for blk in blocks:
        for k, st in enumerate(blk):
            if st[0] == "if" and I.terminates(st[2]):
                if st[3]:
                    cands.append((blk, k, "flatten"))           # if c: T(term) else: E  ->  if c: T ; E
                elif k + 1 < len(blk):
                    cands.append((blk, k, "absorb"))            # if c: T(term) ; R       ->  if c: T else: R
    if not cands:
        return None
    blk, k, kind = rng.choice(cands)
    st = blk[k]
    if kind == "flatten":
        els = st[3]
        st[3] = []
        blk[k + 1:k + 1] = els
    else:
        rest = blk[k + 1:]
        del blk[k + 1:]
        st[3] = rest
    return f


# ----------------------------------------------------------------------------------------------- dispatch
def apply(mod, fname, eq_id, rng, ids, tag="tf"):
    """Return a NEW module in which function `fname` is transformed by `eq_id`, or None if it does not apply."""
    fn = I.functions(mod)[fname]
    sigs = I.functions(mod)

    def mod_types(e):
        env = {p[0]: p[1] for p in fn["params"]}
        return I.typeof(e, env, mod, sigs)

    if eq_id == "EQ-YES-1":
        g = rename_locals(fn, ids, tag)
    elif eq_id == "EQ-YES-2":
        g = reorder_independent(fn, rng)
    elif eq_id == "EQ-YES-3":
        g = loop_swap(fn, ids, tag, mod_types)
    elif eq_id == "EQ-YES-4":
        g = algebraic(fn, rng, mod_types)
    elif eq_id == "EQ-YES-5":
        g = early_return(fn, rng)
    else:
        raise KeyError(eq_id)
    if g is None or I.canon(g) == I.canon(fn):
        return None
    new = I.clone(mod)
    for k, f in enumerate(new["funcs"]):
        if f["name"] == fname:
            new["funcs"][k] = g
    try:
        I.check_module(new)
    except I.IRError:
        return None
    return new

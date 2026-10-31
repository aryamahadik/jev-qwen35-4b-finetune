"""A small, language-neutral statement/expression IR for application-style modules (shared by T42c, T57, T56g).

An IR node is a plain JSON-able list whose first element is a string head. A block is a list of nodes.
Everything (mutation sites, transforms, canonical hashes, row manifests) works on this one tree, so the Go and bash
mutators/renderers are not separate re-implementations.

Types: int, str, bool, ints (list of int), strs (list of str).

Expressions
  [int n] [str s] [bool b] [var x] [field x] [const X]
  [bin op a b]   op in + - * // % < <= > >= == != and or ++      (++ is string concatenation)
  [not a] [min a b] [max a b] [cond c a b] [len a] [idx xs i] [lst T [items]] [istr a] [zpad a width]
  [has xs x] [starts s t] [fcall name [args]] [mcall name [args]]
Statements
  [let x T e] [set x e] [setf f e] [sidx target i e] [push target e] [popto x T target] [shiftto x T target]
  [if c [then] [else]] [for i lo hi [body]] [each x xs [body]] [ret e] [raise ERR] [do e]
  target = [var x] | [field x]

Portability rules enforced by `check_module` (so one tree renders identically in five languages):
  * `//` and `%` only with a positive integer literal divisor (no implicit ZeroDivision);
  * block scoping (a name declared in a block is not visible after it);
  * every function ends in a terminating statement (return / raise / if-else whose branches both terminate);
  * lists are mutated only when they are locals created in the function or state fields (never parameters);
  * every local is read at least once (Go "declared and not used");
  * the call graph is acyclic and calls resolve; `fcall` targets a free function, `mcall` a method.
"""
import copy
import hashlib
import json

INT, STR, BOOL, INTS, STRS = "int", "str", "bool", "ints", "strs"
SCALARS = (INT, STR, BOOL)
LISTS = (INTS, STRS)
ELEM = {INTS: INT, STRS: STR}
LIST_OF = {INT: INTS, STR: STRS}
ARITH = ("+", "-", "*", "//", "%")
CMP = ("<", "<=", ">", ">=")
EQ = ("==", "!=")
BOOLOPS = ("and", "or")
INT_LIMIT = 2 ** 31 - 1
MAX_LITERAL = 10 ** 6

EXPR_HEADS = {"int", "str", "bool", "var", "field", "const", "bin", "not", "min", "max", "cond", "len", "idx", "lst",
              "istr", "zpad", "has", "starts", "fcall", "mcall"}
STMT_HEADS = {"let", "set", "setf", "sidx", "push", "popto", "shiftto", "if", "for", "each", "ret", "raise", "do"}


# ----------------------------------------------------------------------------------------------- constructors
def i(n):
    return ["int", int(n)]


def s(x):
    return ["str", x]


def b(x):
    return ["bool", bool(x)]


def v(name):
    return ["var", name]


def fld(name):
    return ["field", name]


def cst(name):
    return ["const", name]


def bin_(op, a, c):
    return ["bin", op, a, c]


def add(a, c):
    return bin_("+", a, c)


def sub(a, c):
    return bin_("-", a, c)


def mul(a, c):
    return bin_("*", a, c)


def lt(a, c):
    return bin_("<", a, c)


def le(a, c):
    return bin_("<=", a, c)


def gt(a, c):
    return bin_(">", a, c)


def ge(a, c):
    return bin_(">=", a, c)


def eq(a, c):
    return bin_("==", a, c)


def ne(a, c):
    return bin_("!=", a, c)


def and_(a, c):
    return bin_("and", a, c)


def or_(a, c):
    return bin_("or", a, c)


def cat(a, c):
    return bin_("++", a, c)


def not_(a):
    return ["not", a]


def call(name, *args):
    return ["fcall", name, list(args)]


def mcall(name, *args):
    return ["mcall", name, list(args)]


def lst(t, items):
    return ["lst", t, list(items)]


def let(name, t, e):
    return ["let", name, t, e]


def set_(name, e):
    return ["set", name, e]


def ret(e):
    return ["ret", e]


def if_(c, then, els=None):
    return ["if", c, list(then), list(els or [])]


def for_(name, lo, hi, body):
    return ["for", name, lo, hi, list(body)]


def each(name, xs, body):
    return ["each", name, xs, list(body)]


def raise_(err):
    return ["raise", err]


def func(name, params, ret_type, body, scope="free", file=0, tags=()):
    return {"name": name, "params": [list(p) for p in params], "ret": ret_type, "body": list(body), "scope": scope,
            "file": file, "tags": list(tags)}


# ----------------------------------------------------------------------------------------------- tree utilities
def is_node(x):
    return isinstance(x, list) and len(x) > 0 and isinstance(x[0], str)


def is_block(x):
    return isinstance(x, list) and (len(x) == 0 or isinstance(x[0], list))


def children(node):
    """Yield (index_in_node, child) for every list child that is a node, plus block members as (index, block)."""
    for k, c in enumerate(node):
        if isinstance(c, list):
            yield k, c


def walk(root, path=()):
    """Pre-order walk over nodes of a block or node. Yields (path, node). Path indexes into the nested lists."""
    if is_node(root):
        yield path, root
        for k, c in enumerate(root):
            if k and isinstance(c, list):
                yield from walk(c, path + (k,))
    elif isinstance(root, list):
        for k, c in enumerate(root):
            if isinstance(c, list):
                yield from walk(c, path + (k,))


def get_at(root, path):
    cur = root
    for k in path:
        cur = cur[k]
    return cur


def set_at(root, path, value):
    if not path:
        raise ValueError("cannot replace the root")
    get_at(root, path[:-1])[path[-1]] = value


def clone(x):
    """Deep copy of a JSON-able IR tree (module, function, node). json round trip is ~4x faster than copy.deepcopy;
    tuples become lists, which is harmless for IR (it only ever holds lists, dicts, strings, ints and bools)."""
    return json.loads(json.dumps(x))


def canon(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha(x):
    return hashlib.sha256(canon(x).encode("ascii")).hexdigest()


def functions(mod):
    return {f["name"]: f for f in mod["funcs"]}


def new_module(mid):
    return {"id": mid, "files": [], "cls": None, "consts": [], "funcs": [], "errors": {}, "public": [], "meta": {}}


def new_class(name, fields, file=0):
    """fields: list of {name, type, init} with init a JSON value (int/str/[...])."""
    return {"name": name, "file": file, "fields": [dict(f) for f in fields]}


def field_types(mod):
    return {f["name"]: f["type"] for f in (mod["cls"] or {}).get("fields", [])}


def const_types(mod):
    return {c["name"]: c["type"] for c in mod["consts"]}


# ----------------------------------------------------------------------------------------------- type checking
class IRError(ValueError):
    pass


def typeof(e, env, mod, sigs=None):
    h = e[0]
    if h == "int":
        return INT
    if h == "str":
        return STR
    if h == "bool":
        return BOOL
    if h == "var":
        if e[1] not in env:
            raise IRError("undeclared variable %r" % e[1])
        return env[e[1]]
    if h == "field":
        ft = field_types(mod)
        if e[1] not in ft:
            raise IRError("unknown field %r" % e[1])
        return ft[e[1]]
    if h == "const":
        ct = const_types(mod)
        if e[1] not in ct:
            raise IRError("unknown const %r" % e[1])
        return ct[e[1]]
    if h == "bin":
        op, ta, tb = e[1], typeof(e[2], env, mod, sigs), typeof(e[3], env, mod, sigs)
        if op in ARITH:
            if ta != INT or tb != INT:
                raise IRError("arith %s needs ints, got %s,%s" % (op, ta, tb))
            if op in ("//", "%") and not (e[3][0] == "int" and e[3][1] > 0):
                raise IRError("divisor of %s must be a positive int literal" % op)
            return INT
        if op in CMP:
            if ta != INT or tb != INT:
                raise IRError("compare %s needs ints" % op)
            return BOOL
        if op in EQ:
            if ta != tb or ta not in SCALARS:
                raise IRError("equality needs equal scalar types, got %s,%s" % (ta, tb))
            return BOOL
        if op in BOOLOPS:
            if ta != BOOL or tb != BOOL:
                raise IRError("%s needs bools" % op)
            return BOOL
        if op == "++":
            if ta != STR or tb != STR:
                raise IRError("++ needs strs")
            return STR
        raise IRError("unknown operator %r" % op)
    if h == "not":
        if typeof(e[1], env, mod, sigs) != BOOL:
            raise IRError("not needs bool")
        return BOOL
    if h in ("min", "max"):
        if typeof(e[1], env, mod, sigs) != INT or typeof(e[2], env, mod, sigs) != INT:
            raise IRError("%s needs ints" % h)
        return INT
    if h == "cond":
        if typeof(e[1], env, mod, sigs) != BOOL:
            raise IRError("cond test must be bool")
        ta, tb = typeof(e[2], env, mod, sigs), typeof(e[3], env, mod, sigs)
        if ta != tb:
            raise IRError("cond branches differ: %s vs %s" % (ta, tb))
        return ta
    if h == "len":
        t = typeof(e[1], env, mod, sigs)
        if t not in (STR, INTS, STRS):
            raise IRError("len of %s" % t)
        return INT
    if h == "idx":
        t = typeof(e[1], env, mod, sigs)
        if t not in LISTS or typeof(e[2], env, mod, sigs) != INT:
            raise IRError("bad idx")
        return ELEM[t]
    if h == "lst":
        t = e[1]
        if t not in LISTS:
            raise IRError("bad list type %r" % t)
        for it in e[2]:
            if typeof(it, env, mod, sigs) != ELEM[t]:
                raise IRError("list item type")
        return t
    if h == "istr":
        if typeof(e[1], env, mod, sigs) != INT:
            raise IRError("istr needs int")
        return STR
    if h == "zpad":
        if typeof(e[1], env, mod, sigs) != INT or e[2][0] != "int" or not 1 <= e[2][1] <= 9:
            raise IRError("zpad needs int and literal width 1..9")
        return STR
    if h == "has":
        t = typeof(e[1], env, mod, sigs)
        if t not in LISTS or typeof(e[2], env, mod, sigs) != ELEM[t]:
            raise IRError("bad has")
        return BOOL
    if h == "starts":
        if typeof(e[1], env, mod, sigs) != STR or typeof(e[2], env, mod, sigs) != STR:
            raise IRError("starts needs strs")
        return BOOL
    if h in ("fcall", "mcall"):
        sig = (sigs or {}).get(e[1])
        if sig is None:
            raise IRError("call to unknown function %r" % e[1])
        want_scope = "free" if h == "fcall" else "method"
        if sig["scope"] != want_scope:
            raise IRError("%s targets a %s function" % (h, sig["scope"]))
        if len(e[2]) != len(sig["params"]):
            raise IRError("arity of %s" % e[1])
        for a, (_, pt) in zip(e[2], sig["params"]):
            if typeof(a, env, mod, sigs) != pt:
                raise IRError("argument type for %s" % e[1])
        return sig["ret"]
    raise IRError("unknown expression head %r" % h)


def terminates(block):
    if not block:
        return False
    last = block[-1]
    if last[0] in ("ret", "raise"):
        return True
    if last[0] == "if":
        return terminates(last[2]) and terminates(last[3])
    return False


def _reads(node, acc):
    for _, n in walk(node):
        if n[0] == "var":
            acc.add(n[1])
    return acc


def check_function(mod, fn, sigs):
    """Raises IRError on the first problem. Returns the set of variables read."""
    ft = field_types(mod)
    if fn["scope"] == "free":
        for _, n in walk(fn["body"]):
            if n[0] in ("field", "setf", "mcall"):
                raise IRError("free function %s touches state (%s)" % (fn["name"], n[0]))
    env = {p[0]: p[1] for p in fn["params"]}
    params = set(env)
    owned = set()                      # locals whose lists may be mutated
    declared_here = []                 # for the unused-variable lint
    read = set()
    loopvars = set()

    def block(stmts, env, owned):
        env = dict(env)
        owned = set(owned)
        for st in stmts:
            h = st[0]
            if h == "let":
                _, name, t, e = st
                te = typeof(e, env, mod, sigs)
                if te != t:
                    raise IRError("let %s: declared %s, expression %s" % (name, t, te))
                if name in env:
                    raise IRError("redeclaration of %r" % name)
                env[name] = t
                declared_here.append(name)
                if t in LISTS and e[0] == "lst":
                    owned.add(name)
            elif h == "set":
                _, name, e = st
                if name not in env:
                    raise IRError("set of undeclared %r" % name)
                if name in loopvars:
                    raise IRError("assignment to loop variable %r" % name)
                if typeof(e, env, mod, sigs) != env[name]:
                    raise IRError("set %s type" % name)
                if env[name] in LISTS:
                    raise IRError("set of list variable %r (mutate it instead)" % name)
            elif h == "setf":
                _, name, e = st
                if fn["scope"] != "method" or name not in ft:
                    raise IRError("setf outside a method or unknown field %r" % name)
                if typeof(e, env, mod, sigs) != ft[name] or ft[name] in LISTS:
                    raise IRError("setf %s type" % name)
            elif h in ("sidx", "push", "popto", "shiftto"):
                tgt = st[1] if h in ("sidx", "push") else st[3]
                if tgt[0] == "var":
                    if tgt[1] not in owned:
                        raise IRError("%s on a list that is not a function-owned local: %r" % (h, tgt[1]))
                elif tgt[0] == "field":
                    if fn["scope"] != "method" or tgt[1] not in ft:
                        raise IRError("%s on a field outside a method" % h)
                else:
                    raise IRError("bad mutation target")
                tt = typeof(tgt, env, mod, sigs)
                if tt not in LISTS:
                    raise IRError("%s target is not a list" % h)
                if h == "sidx":
                    if typeof(st[2], env, mod, sigs) != INT or typeof(st[3], env, mod, sigs) != ELEM[tt]:
                        raise IRError("sidx types")
                elif h == "push":
                    if typeof(st[2], env, mod, sigs) != ELEM[tt]:
                        raise IRError("push type")
                else:
                    if st[2] != ELEM[tt]:
                        raise IRError("%s type" % h)
                    if st[1] in env:
                        raise IRError("redeclaration of %r" % st[1])
                    env[st[1]] = st[2]
                    declared_here.append(st[1])
            elif h == "if":
                if typeof(st[1], env, mod, sigs) != BOOL:
                    raise IRError("if test must be bool")
                block(st[2], env, owned)
                block(st[3], env, owned)
            elif h == "for":
                _, name, lo, hi, body = st
                if typeof(lo, env, mod, sigs) != INT or typeof(hi, env, mod, sigs) != INT:
                    raise IRError("for bounds")
                if name in env:
                    raise IRError("redeclaration of loop var %r" % name)
                e2 = dict(env)
                e2[name] = INT
                loopvars.add(name)
                block(body, e2, owned)
            elif h == "each":
                _, name, xs, body = st
                t = typeof(xs, env, mod, sigs)
                if t not in LISTS:
                    raise IRError("each over non-list")
                if name in env:
                    raise IRError("redeclaration of loop var %r" % name)
                e2 = dict(env)
                e2[name] = ELEM[t]
                loopvars.add(name)
                block(body, e2, owned)
            elif h == "ret":
                if typeof(st[1], env, mod, sigs) != fn["ret"]:
                    raise IRError("return type of %s" % fn["name"])
            elif h == "raise":
                if st[1] not in mod["errors"]:
                    raise IRError("unknown error id %r" % st[1])
            elif h == "do":
                typeof(st[1], env, mod, sigs)
            else:
                raise IRError("unknown statement head %r" % h)
            # expression reads for the unused lint
            for k, c in enumerate(st):
                if k and isinstance(c, list) and h not in ("if", "for", "each"):
                    _reads(c, read)
            if h == "if":
                _reads(st[1], read)
            elif h == "for":
                _reads(st[2], read)
                _reads(st[3], read)
            elif h == "each":
                _reads(st[2], read)
        return env

    block(fn["body"], env, owned)
    if not terminates(fn["body"]):
        raise IRError("function %s does not end in return/raise" % fn["name"])
    for name in declared_here:
        if name not in read:
            raise IRError("local %r in %s is never read" % (name, fn["name"]))
    return read


def check_module(mod):
    """Returns None when the module is well-formed, else raises IRError."""
    names = [f["name"] for f in mod["funcs"]]
    if len(set(names)) != len(names):
        raise IRError("duplicate function names")
    sigs = {f["name"]: f for f in mod["funcs"]}
    for f in mod["funcs"]:
        if f["scope"] == "method" and not mod["cls"]:
            raise IRError("method %s without a class" % f["name"])
        check_function(mod, f, sigs)
    # acyclic call graph
    graph = {f["name"]: set(n[1] for _, n in walk(f["body"]) if n[0] in ("fcall", "mcall")) for f in mod["funcs"]}
    state = {}

    def dfs(n):
        if state.get(n) == 1:
            raise IRError("recursive call graph at %s" % n)
        if state.get(n) == 2:
            return
        state[n] = 1
        for m in graph[n]:
            dfs(m)
        state[n] = 2

    for n in graph:
        dfs(n)
    for _, n in walk([f["body"] for f in mod["funcs"]]):
        if n[0] == "int" and abs(n[1]) > MAX_LITERAL:
            raise IRError("integer literal too large")
    return None


# ----------------------------------------------------------------------------------------------- hashing
def normalised_copy(mod):
    """Alpha-normalise identifiers (functions, parameters, locals, fields, consts, files, class, error ids). Literal
    VALUES are kept: two modules that differ only in names are the same program; a different constant is not."""
    m = clone(mod)
    fmap = {f["name"]: "F%d" % k for k, f in enumerate(m["funcs"])}
    cmap = {c["name"]: "C%d" % k for k, c in enumerate(m["consts"])}
    flmap = {f["name"]: "L%d" % k for k, f in enumerate((m["cls"] or {}).get("fields", []))}
    emap = {e: "E%d" % k for k, e in enumerate(sorted(m["errors"]))}

    def ren_fn(fn):
        vmap = {}

        def vn(name):
            if name not in vmap:
                vmap[name] = "v%d" % len(vmap)
            return vmap[name]

        for p in fn["params"]:
            p[0] = vn(p[0])
        for _, n in walk(fn["body"]):
            h = n[0]
            if h in ("let", "set", "popto", "shiftto", "for", "each") and isinstance(n[1], str):
                n[1] = vn(n[1])
            elif h == "var":
                n[1] = vn(n[1])
            elif h == "field" or h == "setf":
                n[1] = flmap[n[1]]
            elif h == "const":
                n[1] = cmap[n[1]]
            elif h in ("fcall", "mcall"):
                n[1] = fmap[n[1]]
            elif h == "raise":
                n[1] = emap[n[1]]
        fn["name"] = fmap[fn["name"]]
        fn["tags"] = []

    # field/var ambiguity: "setf" stores a field name in slot 1, so handle before the generic rename
    for fn in m["funcs"]:
        ren_fn(fn)
    for c in m["consts"]:
        c["name"] = cmap[c["name"]]
    if m["cls"]:
        m["cls"]["name"] = "K"
        for f in m["cls"]["fields"]:
            f["name"] = flmap[f["name"]]
    m["files"] = ["file%d" % k for k in range(len(m["files"]))]
    m["errors"] = {emap[e]: {} for e in m["errors"]}
    m["id"] = "x"
    m["public"] = sorted(fmap[p] for p in m["public"])
    m["meta"] = {}
    return m


def norm_hash(mod):
    return sha(normalised_copy(mod))


def exact_hash(mod):
    return sha(mod)


def size_metrics(mod):
    nodes = sum(1 for f in mod["funcs"] for _ in walk(f["body"]))
    loops = sum(1 for f in mod["funcs"] for _, n in walk(f["body"]) if n[0] in ("for", "each"))
    calls = sum(1 for f in mod["funcs"] for _, n in walk(f["body"]) if n[0] in ("fcall", "mcall"))
    return {"nodes": nodes, "loops": loops, "calls": calls, "funcs": len(mod["funcs"])}

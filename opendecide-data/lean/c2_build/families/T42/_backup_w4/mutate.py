"""families/T42/mutate.py: mutation operators on a Python AST (solver A side: they make the distractor programs).

A mutant is the shown program with ONE named near-miss edit, printed through the same printer (ast.unparse) as the shown
program, so formatting never tells the programs apart. The gold of every distractor is the real output of its mutant
(executor.py); nothing here predicts an output.

  OPERATORS            name -> description (also the error-model names of T42)
  HELD_OUT_OPS         the 2 operators of the sealed split (never used by training samplers)
  sites(src, ops)      [(op, node_index, variant)]: every mutation site of the program
  apply(src, site)     the mutant source, or None when the edit does not change the program text
Node index = position in ast.walk order of the freshly parsed program (stable for a given source text).
"""
from __future__ import annotations

import ast
import copy

OPERATORS = {
    "off_by_one": "changes an integer constant, loop bound or index by one",
    "wrong_operator": "uses the neighbouring operator (+ for -, < for <=, and for or, ...)",
    "swap_args": "swaps two arguments of a call or the operands of a non-commutative operator",
    "mutate_default": "changes a default argument (or turns a None-guard into a shared mutable default, or back)",
    "wrong_slice_bound": "moves a slice bound by one or drops it",
    "late_binding": "turns a captured-by-default closure variable into a late-bound one, or the reverse",
    "int_float_div": "uses / where // was written, or the reverse",
    "flip_sort": "flips reverse= or drops key= in a sort, min or max",
    "wrong_method": "calls the sibling method or builtin (lstrip for rstrip, min for max, any for all, ...)",
    "reorder_stmts": "swaps two adjacent simple statements",
    "wrong_except": "catches a different exception class",
    "wrong_format": "changes a format spec, a conversion or a %-conversion",
    "mro_order": "reverses or drops a base class in a class statement",
    "wrong_key": "looks up a neighbouring key (a typo in a dictionary key)",
    "repair_failure": "repairs the one failing step, so the program no longer ends in an exception",
    "revert_edit": "undoes the edit that made the shown program: the output of the unedited program",
}
KEY_WORDS = ["apple", "kiwi", "banana", "fig", "plum", "cherry", "melon", "lime", "pear", "grape", "mango", "peach",
             "lemon", "olive", "berry", "guava"]
HELD_OUT_OPS = ("swap_args", "wrong_slice_bound")
BUCKET_OPS = {"late_binding": "closure", "mro_order": "mro"}       # operators only the held-out idiom buckets use

BIN_SWAP = {ast.Add: ast.Sub, ast.Sub: ast.Add, ast.Mult: ast.Add, ast.Mod: ast.FloorDiv, ast.FloorDiv: ast.Mod,
            ast.Pow: ast.Mult, ast.BitAnd: ast.BitOr, ast.BitOr: ast.BitAnd}
CMP_SWAP = {ast.Lt: ast.LtE, ast.LtE: ast.Lt, ast.Gt: ast.GtE, ast.GtE: ast.Gt, ast.Eq: ast.NotEq, ast.NotEq: ast.Eq,
            ast.In: ast.NotIn, ast.NotIn: ast.In, ast.Is: ast.IsNot, ast.IsNot: ast.Is}
NONCOMM = (ast.Sub, ast.FloorDiv, ast.Mod, ast.Pow, ast.Div)
METHOD_SWAP = {"lstrip": "rstrip", "rstrip": "lstrip", "upper": "lower", "lower": "upper", "startswith": "endswith",
               "endswith": "startswith", "find": "rfind", "rfind": "find", "split": "rsplit", "rsplit": "split",
               "index": "rindex", "rindex": "index", "removeprefix": "removesuffix", "removesuffix": "removeprefix",
               "title": "capitalize", "capitalize": "title", "append": "extend", "isdigit": "isalpha",
               "isalpha": "isdigit", "union": "intersection", "intersection": "union", "difference": "union",
               "pop": "remove", "extend": "append", "setdefault": "get", "get": "setdefault", "count": "index"}
BUILTIN_SWAP = {"min": "max", "max": "min", "any": "all", "all": "any", "sorted": "reversed", "sum": "max"}
EXC_CYCLE = ("ValueError", "KeyError", "IndexError", "TypeError", "ZeroDivisionError", "AttributeError")
FMT_SWAP = (("<", ">"), (">", "<"), ("^", "<"), (".2f", ".1f"), (".1f", ".2f"), (".3f", ".2f"), ("05d", "5d"),
            ("5d", "05d"), ("03d", "3d"), ("x", "X"), ("b", "o"), (",", ""), ("+", ""), ("e", "f"), ("%", "f"))


def _parents(tree) -> dict:
    out = {}
    for n in ast.walk(tree):
        for c in ast.iter_child_nodes(n):
            out[c] = n
    return out


def _is_int(n) -> bool:
    return isinstance(n, ast.Constant) and type(n.value) is int


def _unparse(tree) -> str:
    return ast.unparse(ast.fix_missing_locations(tree))


def _guard_pattern(fn: ast.FunctionDef):
    """(arg name, value node) when the body starts `if p is None: p = <value>` and p defaults to None."""
    if not fn.body or not isinstance(fn.body[0], ast.If):
        return None
    t = fn.body[0]
    if (isinstance(t.test, ast.Compare) and len(t.test.ops) == 1 and isinstance(t.test.ops[0], ast.Is)
            and isinstance(t.test.left, ast.Name) and isinstance(t.test.comparators[0], ast.Constant)
            and t.test.comparators[0].value is None and not t.orelse and len(t.body) == 1
            and isinstance(t.body[0], ast.Assign) and len(t.body[0].targets) == 1
            and isinstance(t.body[0].targets[0], ast.Name) and t.body[0].targets[0].id == t.test.left.id):
        return t.test.left.id, t.body[0].value
    return None


def _args_defaults(fn):
    a = fn.args
    pos = a.posonlyargs + a.args
    out = {}
    for arg, d in zip(pos[len(pos) - len(a.defaults):], a.defaults):
        out[arg.arg] = d
    return out


def _loop_targets(node, parents) -> set:
    """Names bound by the for statements / comprehensions enclosing node."""
    names = set()
    cur = parents.get(node)
    while cur is not None:
        if isinstance(cur, ast.For):
            names |= {n.id for n in ast.walk(cur.target) if isinstance(n, ast.Name)}
        elif isinstance(cur, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
            for g in cur.generators:
                names |= {n.id for n in ast.walk(g.target) if isinstance(n, ast.Name)}
        cur = parents.get(cur)
    return names


def _free_loads(fn) -> set:
    bound = {a.arg for a in fn.args.posonlyargs + fn.args.args + fn.args.kwonlyargs}
    body = [fn.body] if isinstance(fn, ast.Lambda) else fn.body
    loads = set()
    for b in body:
        for n in ast.walk(b):
            if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load):
                loads.add(n.id)
    return loads - bound


def sites(src: str, ops=None) -> list:
    tree = ast.parse(src)
    nodes = list(ast.walk(tree))
    par = _parents(tree)
    want = set(ops) if ops is not None else set(OPERATORS)
    out = []
    for i, n in enumerate(nodes):
        p = par.get(n)
        if "off_by_one" in want and _is_int(n) and not isinstance(p, (ast.Slice, ast.arguments, ast.FormattedValue,
                                                                       ast.UnaryOp)):
            if not (isinstance(p, ast.keyword) or (isinstance(p, ast.Call) and getattr(p.func, "id", "") == "print")):
                out += [("off_by_one", i, "+1"), ("off_by_one", i, "-1")]
        if "wrong_operator" in want:
            if isinstance(n, ast.BinOp) and type(n.op) in BIN_SWAP:
                out.append(("wrong_operator", i, "binop"))
            elif isinstance(n, ast.AugAssign) and type(n.op) in BIN_SWAP:
                out.append(("wrong_operator", i, "augassign"))
            elif isinstance(n, ast.Compare) and len(n.ops) == 1 and type(n.ops[0]) in CMP_SWAP:
                out.append(("wrong_operator", i, "compare"))
            elif isinstance(n, ast.BoolOp):
                out.append(("wrong_operator", i, "boolop"))
        if "swap_args" in want:
            if isinstance(n, ast.Call) and len(n.args) >= 2 and not any(isinstance(a, ast.Starred) for a in n.args) \
                    and not (isinstance(n.func, ast.Name) and n.func.id in ("print", "max", "min", "sum", "set", "zip",
                                                                            "map", "filter", "isinstance")):
                if ast.unparse(n.args[0]) != ast.unparse(n.args[1]):
                    out.append(("swap_args", i, "call"))
            elif isinstance(n, ast.BinOp) and isinstance(n.op, NONCOMM) and ast.unparse(n.left) != ast.unparse(n.right):
                out.append(("swap_args", i, "binop"))
        if "mutate_default" in want and isinstance(n, ast.FunctionDef):
            for name, d in _args_defaults(n).items():
                if _is_int(d):
                    out += [("mutate_default", i, f"{name}:+1"), ("mutate_default", i, f"{name}:-1")]
                elif isinstance(d, ast.Constant) and isinstance(d.value, str):
                    out.append(("mutate_default", i, f"{name}:str"))
                elif isinstance(d, (ast.List, ast.Dict, ast.Set)):
                    out.append(("mutate_default", i, f"{name}:unshare"))
            g = _guard_pattern(n)
            if g and g[0] in _args_defaults(n):
                out.append(("mutate_default", i, f"{g[0]}:share"))
        if "wrong_slice_bound" in want and isinstance(n, ast.Slice):
            for part in ("lower", "upper"):
                v = getattr(n, part)
                if v is None:
                    out.append(("wrong_slice_bound", i, f"{part}:add"))
                else:
                    out += [("wrong_slice_bound", i, f"{part}:+1"), ("wrong_slice_bound", i, f"{part}:-1")]
                    out.append(("wrong_slice_bound", i, f"{part}:drop"))
        if "late_binding" in want and isinstance(n, (ast.Lambda, ast.FunctionDef)):
            dflt = _args_defaults(n) if isinstance(n, ast.FunctionDef) else dict(zip(
                [a.arg for a in n.args.args][len(n.args.args) - len(n.args.defaults):], n.args.defaults))
            if any(isinstance(d, ast.Name) and d.id == k for k, d in dflt.items()):
                out.append(("late_binding", i, "unbind"))
            elif isinstance(n, ast.Lambda) and (_free_loads(n) & _loop_targets(n, par)):
                out.append(("late_binding", i, "bind"))
        if "int_float_div" in want and isinstance(n, ast.BinOp) and isinstance(n.op, (ast.FloorDiv, ast.Div)):
            out.append(("int_float_div", i, "div"))
        if "int_float_div" in want and isinstance(n, ast.AugAssign) and isinstance(n.op, (ast.FloorDiv, ast.Div)):
            out.append(("int_float_div", i, "augdiv"))
        if "flip_sort" in want and isinstance(n, ast.Call):
            for kw in n.keywords:
                if kw.arg == "reverse" and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, bool):
                    out.append(("flip_sort", i, "reverse"))
                if kw.arg == "key":
                    out.append(("flip_sort", i, "dropkey"))
            if isinstance(n.func, ast.Attribute) and n.func.attr == "sort" or \
                    isinstance(n.func, ast.Name) and n.func.id == "sorted":
                if not any(kw.arg == "reverse" for kw in n.keywords):
                    out.append(("flip_sort", i, "addreverse"))
        if "wrong_method" in want and isinstance(n, ast.Call):
            if isinstance(n.func, ast.Attribute) and n.func.attr in METHOD_SWAP:
                out.append(("wrong_method", i, "method"))
            elif isinstance(n.func, ast.Name) and n.func.id in BUILTIN_SWAP:
                out.append(("wrong_method", i, "builtin"))
        if "reorder_stmts" in want and hasattr(n, "body") and isinstance(getattr(n, "body"), list):
            for fld in ("body", "orelse", "finalbody"):
                seq = getattr(n, fld, None)
                if isinstance(seq, list):
                    for j in range(len(seq) - 1):
                        if isinstance(seq[j], (ast.Assign, ast.AugAssign, ast.Expr)) and \
                                isinstance(seq[j + 1], (ast.Assign, ast.AugAssign, ast.Expr)):
                            out.append(("reorder_stmts", i, f"{fld}:{j}"))
        if "wrong_except" in want and isinstance(n, ast.ExceptHandler) and n.type is not None:
            out.append(("wrong_except", i, "class"))
        if "wrong_format" in want:
            if isinstance(n, ast.FormattedValue):
                if n.format_spec is not None:
                    out.append(("wrong_format", i, "spec"))
                out.append(("wrong_format", i, "conv"))
            elif isinstance(n, ast.BinOp) and isinstance(n.op, ast.Mod) and isinstance(n.left, ast.Constant) \
                    and isinstance(n.left.value, str) and "%" in n.left.value:
                out.append(("wrong_format", i, "percent"))
        if "wrong_key" in want and isinstance(n, ast.Constant) and isinstance(n.value, str) and n.value in KEY_WORDS \
                and isinstance(p, ast.Subscript) and p.slice is n:
            out.append(("wrong_key", i, "next"))
        if "mro_order" in want and isinstance(n, ast.ClassDef) and len(n.bases) >= 2:
            out += [("mro_order", i, "reverse"), ("mro_order", i, "drop")]
    return out


def _const_like(node, delta):
    if _is_int(node):
        return ast.Constant(node.value + delta)
    return ast.BinOp(node, ast.Add() if delta > 0 else ast.Sub(), ast.Constant(1))


def _mut_format(spec: str):
    for a, b in FMT_SWAP:
        if a in spec:
            return spec.replace(a, b, 1)
    return None


def apply(src: str, site: tuple):
    op, idx, var = site
    tree = ast.parse(src)
    nodes = list(ast.walk(tree))
    n = nodes[idx]
    par = _parents(tree)
    ok = True
    if op == "off_by_one":
        n.value += 1 if var == "+1" else -1
    elif op == "wrong_operator":
        if isinstance(n, (ast.BinOp, ast.AugAssign)):
            n.op = BIN_SWAP[type(n.op)]()
        elif isinstance(n, ast.Compare):
            n.ops = [CMP_SWAP[type(n.ops[0])]()]
        else:
            n.op = ast.Or() if isinstance(n.op, ast.And) else ast.And()
    elif op == "swap_args":
        if isinstance(n, ast.Call):
            n.args[0], n.args[1] = n.args[1], n.args[0]
        else:
            n.left, n.right = n.right, n.left
    elif op == "mutate_default":
        name, kind = var.split(":")
        a = n.args
        pos = a.posonlyargs + a.args
        k = [x.arg for x in pos].index(name) - (len(pos) - len(a.defaults))
        d = a.defaults[k]
        if kind in ("+1", "-1"):
            a.defaults[k] = ast.Constant(d.value + (1 if kind == "+1" else -1))
        elif kind == "str":
            a.defaults[k] = ast.Constant(d.value + "-")
        elif kind == "unshare":
            a.defaults[k] = ast.Constant(None)
            guard = ast.parse(f"if {name} is None:\n    {name} = 0").body[0]
            guard.body[0].value = d
            n.body.insert(0, guard)
        elif kind == "share":
            gname, val = _guard_pattern(n)
            a.defaults[k] = val
            n.body.pop(0)
    elif op == "wrong_slice_bound":
        part, kind = var.split(":")
        v = getattr(n, part)
        if kind == "add":
            setattr(n, part, ast.Constant(1 if part == "lower" else -1))
        elif kind == "drop":
            setattr(n, part, None)
        else:
            setattr(n, part, _const_like(v, 1 if kind == "+1" else -1))
    elif op == "late_binding":
        if var == "unbind":
            a = n.args
            pos = a.args
            keep = len(pos) - len(a.defaults)
            drop = [i for i, d in enumerate(a.defaults) if isinstance(d, ast.Name) and d.id == pos[keep + i].arg]
            for i in sorted(drop, reverse=True):
                del pos[keep + i]
                del a.defaults[i]
        else:
            tg = sorted(_free_loads(n) & _loop_targets(n, par))[0]
            n.args.args.append(ast.arg(tg))
            n.args.defaults.append(ast.Name(tg, ast.Load()))
    elif op == "int_float_div":
        n.op = ast.Div() if isinstance(n.op, ast.FloorDiv) else ast.FloorDiv()
    elif op == "flip_sort":
        if var == "reverse":
            for kw in n.keywords:
                if kw.arg == "reverse":
                    kw.value = ast.Constant(not kw.value.value)
        elif var == "dropkey":
            n.keywords = [kw for kw in n.keywords if kw.arg != "key"]
        else:
            n.keywords.append(ast.keyword("reverse", ast.Constant(True)))
    elif op == "wrong_method":
        if var == "method":
            n.func.attr = METHOD_SWAP[n.func.attr]
        else:
            n.func.id = BUILTIN_SWAP[n.func.id]
    elif op == "reorder_stmts":
        fld, j = var.split(":")
        seq = getattr(n, fld)
        j = int(j)
        seq[j], seq[j + 1] = seq[j + 1], seq[j]
    elif op == "wrong_except":
        t = n.type
        if isinstance(t, ast.Name):
            cur = EXC_CYCLE.index(t.id) if t.id in EXC_CYCLE else -1
            n.type = ast.Name(EXC_CYCLE[(cur + 1) % len(EXC_CYCLE)], ast.Load())
        elif isinstance(t, ast.Tuple) and len(t.elts) > 1:
            t.elts = t.elts[:-1]
        else:
            ok = False
    elif op == "wrong_format":
        if var == "spec":
            parts = n.format_spec.values
            if parts and isinstance(parts[0], ast.Constant) and isinstance(parts[0].value, str):
                new = _mut_format(parts[0].value)
                ok = new is not None and new != parts[0].value
                if ok:
                    parts[0] = ast.Constant(new)
            else:
                ok = False
        elif var == "conv":
            n.conversion = -1 if n.conversion != -1 else 114
        else:
            s = n.left.value
            new = s.replace("%d", "%s", 1) if "%d" in s else s.replace("%s", "%r", 1) if "%s" in s else None
            ok = new is not None
            if ok:
                n.left = ast.Constant(new)
    elif op == "wrong_key":
        n.value = KEY_WORDS[(KEY_WORDS.index(n.value) + 1) % len(KEY_WORDS)]
    elif op == "mro_order":
        if var == "reverse":
            n.bases = n.bases[::-1]
        else:
            n.bases = n.bases[:-1]
    out = _unparse(tree)
    return out if ok and out != src else None      # src is already the printer's text (normalize())


def normalize(src: str) -> str:
    return ast.unparse(ast.parse(src))

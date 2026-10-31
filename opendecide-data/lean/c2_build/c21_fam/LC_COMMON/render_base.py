"""Shared pieces for the five source renderers: language table, precedence, literals, cross-file imports."""
import re

from . import ir as I

LANGS = ("python", "javascript", "typescript", "go", "bash")

# source file extension of module files, and how a test file is named from a module stem
EXT = {"python": ".py", "javascript": ".js", "typescript": ".mts", "go": ".go", "bash": ".sh"}

SAFE_STR = re.compile(r"^[A-Za-z0-9_ :.,/=#-]*$")

# precedence (higher binds tighter); python differs from the C family only for not/comparison
PREC_PY = {"or": 1, "and": 2, "not": 3, "cmp": 4, "add": 5, "mul": 6, "atom": 9}
PREC_C = {"or": 1, "and": 2, "eq": 3, "cmp": 4, "add": 5, "mul": 6, "not": 7, "atom": 9}


def check_str(sv):
    if not SAFE_STR.match(sv):
        raise ValueError("string literal outside the portable charset: %r" % sv)
    return sv


def bin_class(op):
    if op in ("and", "or"):
        return op
    if op in ("==", "!="):
        return "eq"
    if op in ("<", "<=", ">", ">="):
        return "cmp"
    if op in ("+", "-", "++"):
        return "add"
    return "mul"


def need_paren(child_prec, parent_prec, side, child_is_cmp=False, parent_is_cmp=False):
    if child_prec < parent_prec:
        return True
    if child_prec == parent_prec:
        if side == "R":
            return True
        if child_is_cmp and parent_is_cmp:
            return True
    return False


def file_deps(mod):
    """For each file index: {other_file_index: sorted names it needs from that file} (free functions and consts)."""
    fn_file = {f["name"]: f["file"] for f in mod["funcs"] if f["scope"] == "free"}
    const_file = {c["name"]: c.get("file", 0) for c in mod["consts"]}
    deps = {k: {} for k in range(len(mod["files"]))}
    for f in mod["funcs"]:
        for _, n in I.walk(f["body"]):
            tgt = None
            if n[0] == "fcall":
                tgt = fn_file.get(n[1])
                nm = n[1]
            elif n[0] == "const":
                tgt = const_file.get(n[1])
                nm = n[1]
            else:
                continue
            if tgt is not None and tgt != f["file"]:
                deps[f["file"]].setdefault(tgt, set()).add(nm)
    for fi in deps:
        for tf in deps[fi]:
            deps[fi][tf] = sorted(deps[fi][tf])
    return deps


def dep_order(mod):
    """File indexes in a dependency-respecting order (dependencies first). Raises on a cycle."""
    deps = file_deps(mod)
    order, seen, onstack = [], set(), set()

    def visit(k):
        if k in onstack:
            raise ValueError("cyclic file dependency")
        if k in seen:
            return
        onstack.add(k)
        for d in sorted(deps[k]):
            visit(d)
        onstack.discard(k)
        seen.add(k)
        order.append(k)

    for k in range(len(mod["files"])):
        visit(k)
    return order


def file_of_class(mod):
    return (mod["cls"] or {}).get("file")


def funcs_in_file(mod, k):
    return [f for f in mod["funcs"] if f["file"] == k]


def used_err_ids(mod, file_index=None):
    out = set()
    for f in mod["funcs"]:
        if file_index is not None and f["file"] != file_index:
            continue
        for _, n in I.walk(f["body"]):
            if n[0] == "raise":
                out.add(n[1])
    return sorted(out)


def err_marker(mod, err, lang):
    """The language-visible name (Python/JS builtin or authored marker) recorded for an abstract error id."""
    return mod["errors"][err][lang if lang != "typescript" else "javascript"]

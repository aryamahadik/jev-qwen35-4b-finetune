"""families/T43/repairs.py: the repair family R* (solver A side: the ambiguity guard of the line head).

R*(src, line) = every source reached from `src` by ONE edit inside the given file line:
  - an int constant +1 or -1 (slice bounds included);
  - a binary or augmented operator replaced by another of + - * / // %;
  - a comparison operator replaced by another of < <= > >= == != in not in;
  - and <-> or;
  - min <-> max, any <-> all; a method name replaced by the swap partner or by the names that swap to it;
  - the reverse= keyword flipped or dropped; a slice bound dropped or added (1 / -1);
  - the two arguments of a call (2+ positional) or the operands of a binary operator swapped.
The guard: no edit of R* on a line other than the gold line may make the code equal to the original on the G0 grid
(otherwise "which line" would have two answers). Solver B enumerates the same family with its own code.
"""
from __future__ import annotations

import ast
import copy

from families.T42 import mutate as M

ARITH = (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod)
CMPS = (ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.Eq, ast.NotEq, ast.In, ast.NotIn)
INV_METHOD: dict = {}
for _k, _v in M.METHOD_SWAP.items():
    INV_METHOD.setdefault(_v, set()).add(_k)


def _methods(name):
    return sorted(({M.METHOD_SWAP[name]} if name in M.METHOD_SWAP else set()) | INV_METHOD.get(name, set()))


def variants(src: str, line: int) -> list:
    """[(description, new source)] for the edits on file line `line`, deduplicated by text."""
    tree = ast.parse(src)
    nodes = list(ast.walk(tree))
    seen, out = {src}, []

    def emit(desc, mutate):
        t = ast.parse(src)
        ns = list(ast.walk(t))
        n = ns[idx]
        if mutate(n) is False:
            return
        new = ast.unparse(ast.fix_missing_locations(t))
        if new not in seen:
            seen.add(new)
            out.append((desc, new))

    for idx, n in enumerate(nodes):
        if getattr(n, "lineno", None) != line:
            continue
        if isinstance(n, ast.Constant) and type(n.value) is int:
            for d in (1, -1):
                emit("const", lambda x, d=d: setattr(x, "value", x.value + d))
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub) and isinstance(n.operand, ast.Constant) \
                and type(n.operand.value) is int:                      # `-1` parses as a negation of 1: repair the whole literal
            for d in (1, -1):
                emit("negconst", lambda x, d=d: _neg_const(x, d))
        if isinstance(n, (ast.BinOp, ast.AugAssign)) and type(n.op) in ARITH:
            for o in ARITH:
                if o is not type(n.op):
                    emit("op", lambda x, o=o: setattr(x, "op", o()))
        if isinstance(n, ast.BinOp) and ast.unparse(n.left) != ast.unparse(n.right):
            emit("swap", _swap_bin)
        if isinstance(n, ast.Compare) and len(n.ops) == 1 and type(n.ops[0]) in CMPS:
            for o in CMPS:
                if o is not type(n.ops[0]):
                    emit("cmp", lambda x, o=o: setattr(x, "ops", [o()]))
        if isinstance(n, ast.BoolOp):
            emit("bool", lambda x: setattr(x, "op", ast.Or() if isinstance(x.op, ast.And) else ast.And()))
        if isinstance(n, ast.Call):
            if isinstance(n.func, ast.Name) and (n.func.id in M.BUILTIN_SWAP or n.func.id in M.BUILTIN_SWAP.values()):
                for tgt in sorted(({M.BUILTIN_SWAP[n.func.id]} if n.func.id in M.BUILTIN_SWAP else set())
                                  | {k for k, v in M.BUILTIN_SWAP.items() if v == n.func.id}):
                    emit("builtin", lambda x, tgt=tgt: setattr(x.func, "id", tgt))
            if isinstance(n.func, ast.Attribute):
                for tgt in _methods(n.func.attr):
                    emit("method", lambda x, tgt=tgt: setattr(x.func, "attr", tgt))
            if len(n.args) >= 2 and not any(isinstance(a, ast.Starred) for a in n.args) and \
                    ast.unparse(n.args[0]) != ast.unparse(n.args[1]):
                emit("swap_args", lambda x: _swap_args(x))
            for kw in n.keywords:
                if kw.arg == "reverse":
                    emit("rev_flip", lambda x: _kw_flip(x))
                    emit("rev_drop", lambda x: setattr(x, "keywords", [k for k in x.keywords if k.arg != "reverse"]))
        if isinstance(n, ast.Slice):
            for part in ("lower", "upper"):
                v = getattr(n, part)
                if v is None:
                    emit("slice_add", lambda x, part=part: setattr(x, part, ast.Constant(1 if part == "lower" else -1)))
                else:
                    emit("slice_drop", lambda x, part=part: setattr(x, part, None))
    return out


def _swap_bin(x):
    x.left, x.right = x.right, x.left


def _swap_args(x):
    x.args[0], x.args[1] = x.args[1], x.args[0]


def _kw_flip(x):
    for kw in x.keywords:
        if kw.arg == "reverse" and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, bool):
            kw.value = ast.Constant(not kw.value.value)
            return
    return False


def _neg_const(x, d):
    v = -x.operand.value + d
    x.__class__ = ast.Constant
    x.value = v
    x.kind = None

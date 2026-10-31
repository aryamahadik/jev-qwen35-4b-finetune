"""families/T43/solver_b.py: T43 solver B, written from G0_SPEC.md (not from plugin.py, executor.py or patching.py).

parse(row, ctx) reads the RENDERED row back to its facts: the layout of each section is undone by this module's own
inverses, the numbered-line gutter is stripped, tests, test run and patch are read, and every option text is read back to a key.

solve_b(view) answers by a different paradigm from solver A (hermetic CPython execution of tests, grid and seeded cases against
the original): a tree-walking interpreter (interp_b.py) runs the shown code, and the ORIGINAL is replaced by its own docstring:
`Equals <expression>.` is the reference semantics of a function; the expression of a module function names other functions of
the module, which stand for their own docstring expressions (so every function is judged by itself).
  pv     B's own unified-diff applier (strict); then the shown tests; then every function against its docstring on the G0 grid
  ll/lf  lf: the function that deviates from its docstring (none when no function does); ll: the numbered line whose repair
         (one edit of the repair family R*, written here) makes the function agree with its docstring; none when it agrees now
Imports no solver-A code (plugin.check_independence).
"""
from __future__ import annotations

import ast
import itertools
import re

from . import interp_b as IB
from . import texts as TX


class ParseError(ValueError):
    pass


FILE = "module.py"
ORDER = ("code", "tests", "run", "patch")
# the G0 grid (G0_SPEC section 3)
G_INT0 = [-5, -1, 0, 1, 2, 3, 5, 8, 12, 100]
G_INTK = [-1, 2, 4, 9]
G_INTS = [[], [0], [5], [-3], [2, 5], [5, 2], [3, 3], [1, 1, 2], [4, -1, 2], [2, 3, 5], [8, 7, 3, 2], [3, 0, 3, 9],
          [2, 5, 2, 5], [7, 2, 8, 3, 5]]
G_STR = ["", "a", "ab", "Ab", " x", "x ", "a1", "aa", "stone", "plant", "house", "ab ba"]
ANN = {"int": "int", "list[int]": "ints", "str": "str"}


# ------------------------------------------------------------------------------------------------ layout inverses
def _hdr(reg: str, sid: str) -> str:
    t = TX.TITLES[sid]
    return {"banner": f"=== {t} ===\n", "tabs": f"=== {t} ===\n", "md": f"## {t}\n```\n", "bracket": f"[{t}]\n",
            "xml": f"<{sid}>\n", "dashes": f"--- {t} ---\n", "quote": f"> {t}:\n", "boxed": f"+- {t}\n"}[reg]


def _footer(reg: str, sid: str) -> str:
    return {"md": "\n```", "xml": f"\n</{sid}>", "boxed": "\n+-"}.get(reg, "")


def _untab(line: str) -> str:
    m = re.match(r"^([ +\-]?)(\t+)", line)
    return line if not m else m.group(1) + "    " * len(m.group(2)) + line[m.end():]


def _sections(reg: str, state: str, sids: tuple) -> dict:
    out, rest = {}, state
    for n, sid in enumerate(sids):
        h = _hdr(reg, sid)
        if not rest.startswith(h):
            raise ParseError(f"section {sid} header")
        rest = rest[len(h):]
        if n + 1 < len(sids):
            cut = "\n\n" + _hdr(reg, sids[n + 1])
            i = rest.find(footer_cut(reg, sid, cut))
            if i < 0:
                raise ParseError(f"section {sid} end")
            body, rest = rest[:i], rest[i + len(_footer(reg, sid)) + 2:]
        else:
            f = _footer(reg, sid)
            if f and not rest.endswith(f):
                raise ParseError(f"section {sid} footer")
            body, rest = (rest[:-len(f)] if f else rest), ""
        if reg == "quote":
            ls = body.split("\n")
            if not all(x.startswith("> ") for x in ls):
                raise ParseError("quote prefix")
            body = "\n".join(x[2:] for x in ls)
        elif reg == "boxed":
            ls = body.split("\n")
            if not all(x.startswith("| ") for x in ls):
                raise ParseError("box prefix")
            body = "\n".join(x[2:] for x in ls)
        elif reg == "tabs" and sid in ("code", "patch"):
            body = "\n".join(_untab(x) for x in body.split("\n"))
        out[sid] = body
    return out


def footer_cut(reg, sid, cut):
    return _footer(reg, sid) + cut


# ------------------------------------------------------------------------------------------------ parse
def _option_key(qform: str, text: str, names: list) -> str:
    if qform in ("loc_line", "loc_line_n"):
        m = re.fullmatch(r"line ([1-6])", text)
        if m:
            return "L" + m.group(1)
        if text == TX.NONE_TEXT["ll"]:
            return "none"
    elif qform in ("loc_func", "loc_func_n"):
        if text == TX.NONE_TEXT["lf"]:
            return "none"
        if text in names:
            return text
    else:
        for k, v in TX.OPT.items():
            if v == text:
                return k
    raise ParseError(f"option text {text!r}")


def parse(row: dict, ctx) -> dict:
    wording = ctx.skin(row["meta"]["wording_id"])
    qform = wording.qform
    reg = ctx.skin(row["meta"]["c2"]["skin_id"]).register
    rules, sep, question = row["instructions"].partition("\n\n")
    if not sep or rules != TX.RULES[qform] or question != wording.text or question not in TX.WORDINGS[qform]:
        raise ParseError("rules / question text does not match the G0 wording")
    pv = qform in ("pv", "pv_d")
    sec = _sections(reg, row["state"], ORDER if pv else ORDER[:3])
    code = sec["code"]
    if qform in ("loc_line", "loc_line_n"):
        lines = []
        for i, ln in enumerate(code.split("\n")):
            exp = f"{i - 1:>2} | " if i >= 2 else "   | "
            if not ln.startswith(exp):
                raise ParseError("gutter")
            lines.append(ln[len(exp):])
        code = "\n".join(lines)
    tests = []
    if pv:
        mode = None
        for ln in sec["tests"].split("\n"):
            if ln.startswith("Target test"):
                mode = "f2p"
            elif ln.startswith("Other tests"):
                mode = "p2p"
            else:
                tests.append(_test_line(ln, mode))
    else:
        tests = [_test_line(ln.rstrip(), "t") for ln in sec["tests"].split("\n")]
    report = []
    for n, ln in enumerate(sec["run"].split("\n")):
        ln = ln.rstrip()
        m = re.fullmatch(rf"  t{n + 1} (pass, got (.+)|FAIL, got (.+)|ERROR, raised (.+))", ln)
        if not m:
            raise ParseError("run line")
        report.append("p" if m.group(2) is not None else ("f:" + m.group(3) if m.group(3) is not None else "e:" + m.group(4)))
    if len(report) != len(tests):
        raise ParseError("report length")
    names = [n.name for n in ast.parse(code).body if isinstance(n, ast.FunctionDef)]
    view = {"qform": qform, "code": code, "tests": tests, "report": report, "patch": sec.get("patch")}
    if row["qtype"] == "choice":
        view["options"] = [_option_key(qform, t, names) for t in row["options"]]
    return view


def _test_line(ln: str, group: str) -> list:
    m = re.fullmatch(r"  t\d+  (.+\)) == (.+)", ln)
    if not m:
        raise ParseError(f"test line {ln!r}")
    return [m.group(1), m.group(2), group]


# ------------------------------------------------------------------------------------------------ the diff applier (own)
def apply_patch(text: str, diff: str):
    ls = diff.split("\n")
    if len(ls) < 4 or not ls[0].startswith("--- ") or not ls[1].startswith("+++ "):
        return None
    hunks, i = [], 2
    while i < len(ls):
        m = re.fullmatch(r"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", ls[i])
        if not m:
            return None
        start = int(m.group(1))
        n_old = 1 if m.group(2) is None else int(m.group(2))
        i += 1
        old, new = [], []
        while i < len(ls) and not ls[i].startswith("@@"):
            tag, body = ls[i][:1], ls[i][1:]
            if tag == " ":
                old.append(body)
                new.append(body)
            elif tag == "-":
                old.append(body)
            elif tag == "+":
                new.append(body)
            else:
                return None
            i += 1
        if len(old) != n_old:
            return None
        hunks.append((start, old, new))
    src = text.split("\n")
    out, at = [], 0
    for start, old, new in hunks:
        s0 = start - 1 if old else start
        if s0 < at or src[s0:s0 + len(old)] != old:
            return None
        out.extend(src[at:s0])
        out.extend(new)
        at = s0 + len(old)
    out.extend(src[at:])
    return "\n".join(out)


# ------------------------------------------------------------------------------------------------ interpreter helpers
def _funcs(code: str) -> list:
    out = []
    for n in ast.parse(code).body:
        if isinstance(n, ast.FunctionDef):
            doc = ast.get_docstring(n) or ""
            m = re.fullmatch(r"Equals (.+)\.", doc)
            if not m:
                raise ParseError(f"function {n.name} has no 'Equals <expression>.' docstring")
            out.append({"name": n.name, "ref": m.group(1), "params": [a.arg for a in n.args.args],
                        "types": [ANN[ast.unparse(a.annotation)] for a in n.args.args], "seg": ast.get_source_segment(code, n)})
    return out


def _load(src: str):
    it = IB.Interp()
    it.run(ast.parse(src).body, it.glob)
    return it


def _call(it, name: str, args):
    fn = it.glob.vars.get(name)
    if fn is None:
        return ("x",)
    a = [list(x) if isinstance(x, list) else x for x in args]
    try:
        return ("v", repr(fn(*a)), repr(a))
    except IB._Budget:
        return ("t",)
    except Exception as e:  # noqa: BLE001
        return ("e", type(e).__name__)


def _grid(types: list) -> list:
    cols = []
    for pos, t in enumerate(types):
        cols.append((G_INT0 if pos == 0 else G_INTK) if t == "int" else (G_INTS if t == "ints" else G_STR))
    return [list(c) for c in itertools.product(*cols)]


_REF: dict = {}


def _ref_interp(code: str):
    """The reference module: every function replaced by `return <its docstring expression>`."""
    if code not in _REF:
        src = "\n\n".join(f"def {f['name']}({', '.join(f['params'])}):\n    return ({f['ref']})" for f in _funcs(code))
        _REF[code] = _load(src)
    return _REF[code]


_CONF: dict = {}


def _agrees(code: str, name: str) -> bool:
    """Does function `name` (callees replaced by their docstring expressions) agree with its own docstring on the G0 grid?"""
    fs = _funcs(code)
    me = [f for f in fs if f["name"] == name][0]
    key = (me["seg"], me["ref"], tuple(me["types"]), tuple(f["ref"] for f in fs if f["name"] != name))
    if key in _CONF:
        return _CONF[key]
    parts = [f["seg"] if f["name"] == name else f"def {f['name']}({', '.join(f['params'])}):\n    return ({f['ref']})" for f in fs]
    mixed = _load("\n\n".join(parts))
    ref = _ref_interp(code)
    ok = True
    for case in _grid(me["types"]):
        r1, r2 = _call(mixed, name, case), _call(ref, name, case)
        if r1 != r2 or r1[0] in ("t", "x"):
            ok = False
            break
    _CONF[key] = ok
    return ok


def _tests_pass(code: str, tests: list) -> bool:
    it = _load(code)
    for call, exp, _ in tests:
        node = ast.parse(call, mode="eval").body
        args = [ast.literal_eval(a) for a in node.args]
        r = _call(it, node.func.id, args)
        if r[0] != "v" or r[1] != exp:
            return False
    return True


def _deviating(code: str) -> list:
    return [f["name"] for f in _funcs(code) if not _agrees(code, f["name"])]


# ------------------------------------------------------------------------------------------------ repair family R* (own code)
_ARITH = (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod)
_CMP = (ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.Eq, ast.NotEq, ast.In, ast.NotIn)
_METH = {"lstrip": "rstrip", "rstrip": "lstrip", "upper": "lower", "lower": "upper", "startswith": "endswith",
         "endswith": "startswith", "find": "rfind", "rfind": "find", "split": "rsplit", "rsplit": "split", "index": "rindex",
         "rindex": "index", "removeprefix": "removesuffix", "removesuffix": "removeprefix", "title": "capitalize",
         "capitalize": "title", "append": "extend", "isdigit": "isalpha", "isalpha": "isdigit", "union": "intersection",
         "intersection": "union", "difference": "union", "pop": "remove", "extend": "append", "setdefault": "get",
         "get": "setdefault", "count": "index"}
_BUILTIN = {"min": "max", "max": "min", "any": "all", "all": "any", "sorted": "reversed", "sum": "max"}


def _method_names(m: str) -> set:
    return ({_METH[m]} if m in _METH else set()) | {k for k, v in _METH.items() if v == m}


def _builtin_names(m: str) -> set:
    return ({_BUILTIN[m]} if m in _BUILTIN else set()) | {k for k, v in _BUILTIN.items() if v == m}


def _edits(code: str, line: int):
    """Yield the source of every single edit of the repair family on file line `line`."""
    base = ast.parse(code)
    n_nodes = sum(1 for _ in ast.walk(base))
    for idx in range(n_nodes):
        n0 = list(ast.walk(base))[idx]
        if getattr(n0, "lineno", None) != line:
            continue
        plans = []
        if isinstance(n0, ast.Constant) and type(n0.value) is int:
            plans += [("c", d) for d in (1, -1)]
        if isinstance(n0, ast.UnaryOp) and isinstance(n0.op, ast.USub) and isinstance(n0.operand, ast.Constant) \
                and type(n0.operand.value) is int:
            plans += [("neg", d) for d in (1, -1)]
        if isinstance(n0, (ast.BinOp, ast.AugAssign)) and type(n0.op) in _ARITH:
            plans += [("op", o) for o in _ARITH if o is not type(n0.op)]
        if isinstance(n0, ast.BinOp):
            plans.append(("swapop", None))
        if isinstance(n0, ast.Compare) and len(n0.ops) == 1 and type(n0.ops[0]) in _CMP:
            plans += [("cmp", o) for o in _CMP if o is not type(n0.ops[0])]
        if isinstance(n0, ast.BoolOp):
            plans.append(("bool", None))
        if isinstance(n0, ast.Call):
            if isinstance(n0.func, ast.Name):
                plans += [("bi", t) for t in sorted(_builtin_names(n0.func.id))]
            if isinstance(n0.func, ast.Attribute):
                plans += [("me", t) for t in sorted(_method_names(n0.func.attr))]
            if len(n0.args) >= 2:
                plans.append(("swapargs", None))
            if any(k.arg == "reverse" for k in n0.keywords):
                plans += [("revflip", None), ("revdrop", None)]
        if isinstance(n0, ast.Slice):
            for part in ("lower", "upper"):
                plans.append(("sdrop" if getattr(n0, part) is not None else "sadd", part))
        for kind, arg in plans:
            t = ast.parse(code)
            n = list(ast.walk(t))[idx]
            if kind == "c":
                n.value += arg
            elif kind == "neg":
                v = -n.operand.value + arg
                n.__class__ = ast.Constant
                n.value = v
                n.kind = None
            elif kind == "op":
                n.op = arg()
            elif kind == "swapop":
                n.left, n.right = n.right, n.left
            elif kind == "cmp":
                n.ops = [arg()]
            elif kind == "bool":
                n.op = ast.Or() if isinstance(n.op, ast.And) else ast.And()
            elif kind == "bi":
                n.func.id = arg
            elif kind == "me":
                n.func.attr = arg
            elif kind == "swapargs":
                n.args[0], n.args[1] = n.args[1], n.args[0]
            elif kind == "revflip":
                for k in n.keywords:
                    if k.arg == "reverse" and isinstance(k.value, ast.Constant) and isinstance(k.value.value, bool):
                        k.value = ast.Constant(not k.value.value)
            elif kind == "revdrop":
                n.keywords = [k for k in n.keywords if k.arg != "reverse"]
            elif kind == "sdrop":
                setattr(n, arg, None)
            elif kind == "sadd":
                setattr(n, arg, ast.Constant(1 if arg == "lower" else -1))
            new = ast.unparse(ast.fix_missing_locations(t))
            if new != code:
                yield new


def _line_gold(code: str, tests: list):
    names = _deviating(code)
    if not names:
        return "none"
    hits = []
    for ln in range(3, 9):
        for cand in _edits(code, ln):
            try:
                if _tests_pass(cand, tests) and not _deviating(cand):
                    hits.append(ln - 2)
                    break
            except Exception:  # noqa: BLE001
                continue
    if len(hits) != 1:
        raise ParseError(f"line repair is not unique: {hits}")
    return f"L{hits[0]}"


def solve_b(view: dict):
    qf = view["qform"]
    code, tests = view["code"], view["tests"]
    if qf in ("pv", "pv_d"):
        patched = apply_patch(code, view["patch"])
        if patched is None:
            return "D"
        if not _tests_pass(patched, tests):
            return "B"
        return "C" if _deviating(patched) else "A"
    if qf in ("loc_func", "loc_func_n"):
        dev = _deviating(code)
        if not dev:
            return "none"
        if len(dev) != 1:
            raise ParseError(f"{len(dev)} functions deviate from their docstring")
        return dev[0]
    return _line_gold(code, tests)

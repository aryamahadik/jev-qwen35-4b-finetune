"""T42c Solver B cross-checks on the PROSE / CALL carriers (own parsers; stdlib + LC_SOLVER_B only).

* domain_from_text: parse DOMAIN_DECL back into the typed domain B enumerates, so the displayed domain is compared with the
  witness domain (the EQV2 label is exact only for the domain the model is shown).
* callspec_calls: parse CALL_SPEC (the call(s) as shown) back into [(fn, args)] to compare with witness_inputs.calls.
"""
import ast
import re
import shlex

from LC_SOLVER_B.common import Unsupported
from LC_SOLVER_B.goeval import GParser
from LC_SOLVER_B.jseval import Parser as JsParser


def _vals(inner):
    return list(ast.literal_eval("[" + inner + "]"))


_PARAM = re.compile(r"^(\w+) is (?:any integer from (-?\d+) to (-?\d+)|one of \{(.*)\}|any list of length 0 to (\d+) with items from \{(.*)\})$")


def _param(text):
    m = _PARAM.match(text.strip())
    if not m:
        raise Unsupported("domain phrase")
    name, lo, hi, oneof, maxlen, items = m.groups()
    if lo is not None:
        return {"name": name, "t": "int", "vals": list(range(int(lo), int(hi) + 1))}
    if oneof is not None:
        v = _vals(oneof)
        return {"name": name, "t": "str" if v and isinstance(v[0], str) else "int", "vals": v}
    el = _vals(items)
    return {"name": name, "t": "strs" if el and isinstance(el[0], str) else "ints", "elem": el, "maxlen": int(maxlen)}


def _split_top(text, sep):
    out, depth, cur = [], 0, []
    for c in text:
        if c in "({":
            depth += 1
        elif c in ")}":
            depth -= 1
        if c == sep and depth == 0:
            out.append("".join(cur))
            cur = []
        else:
            cur.append(c)
    out.append("".join(cur))
    return out


def domain_from_text(text):
    m = re.match(r"^every call sequence of length 0 to (\d+) over: (.*)$", text.strip())
    if m:
        ops = []
        for chunk in _split_top(m.group(2), ";"):
            chunk = chunk.strip()
            mm = re.match(r"^(\w+)\((.*)\)$", chunk)
            if not mm:
                raise Unsupported("op phrase")
            params = [_param(p) for p in _split_top(mm.group(2), ",") if p.strip()]
            ops.append({"fn": mm.group(1), "params": params})
        return {"mode": "seq", "ops": ops, "maxlen": int(m.group(1))}
    return {"mode": "pure", "params": [_param(p) for p in text.split("; ") if p.strip()]}


def domain_matches(parsed, wi):
    """True when the parsed prose domain equals witness_inputs['domain'] (names, kinds, value sets)."""
    def same(a, b):
        if a["t"] != b["t"] or a["name"] != b["name"]:
            return False
        if a["t"] in ("int", "str"):
            return a["vals"] == b["vals"]
        return a["elem"] == b["elem"] and a["maxlen"] == b["maxlen"]
    d = wi["domain"]
    if parsed["mode"] != wi["mode"]:
        return False
    if parsed["mode"] == "pure":
        return len(parsed["params"]) == len(d) and all(same(a, b) for a, b in zip(parsed["params"], d))
    if parsed["maxlen"] != d["maxlen"] or len(parsed["ops"]) != len(d["ops"]):
        return False
    return all(o["fn"] == q["fn"] and len(o["params"]) == len(q["params"]) and all(same(a, b) for a, b in zip(o["params"], q["params"]))
               for o, q in zip(parsed["ops"], d["ops"]))


# ------------------------------------------------------------------------------------------------ call spec
def _lit_py(n):
    return ast.literal_eval(n)


def _calls_python(text):
    tree = ast.parse(text)
    out = []
    for st in tree.body:
        v = st.value if isinstance(st, (ast.Assign, ast.Expr)) else None
        if isinstance(v, ast.Call):
            f = v.func
            name = f.attr if isinstance(f, ast.Attribute) else f.id if isinstance(f, ast.Name) else None
            if isinstance(f, ast.Name) and isinstance(st, ast.Assign) and f.id[:1].isupper() and not v.args:
                continue                                    # obj = Cls()
            out.append((name, [_lit_py(a) for a in v.args]))
    return out


def _lit_js(n):
    k = n[0]
    if k in ("num", "str", "lit"):
        return n[1]
    if k == "unary" and n[1] == "-" and n[2][0] == "num":
        return -n[2][1]
    if k == "array":
        return [_lit_js(x) for x in n[1]]
    raise Unsupported("js literal")


def _calls_js(text):
    out = []
    for st in JsParser(text).parse_program():
        e = None
        if st[0] == "expr":
            e = st[1]
        elif st[0] == "var":
            e = st[2][0][1]
        if e is None or e[0] != "call":
            continue
        c = e[1]
        name = c[2] if c[0] == "member" else c[1]
        out.append((name, [_lit_js(a) for a in e[2]]))
    return out


def _lit_go(n):
    k = n[0]
    if k in ("int", "str"):
        return n[1]
    if k == "unary" and n[1] == "-":
        return -_lit_go(n[2])
    if k == "complit":
        return [_lit_go(v) for _, v in n[2]]
    raise Unsupported("go literal")


def _calls_go(text):
    src = "package p\nfunc f() {\n%s\n}\n" % text
    fn = [d for d in GParser(src).parse_file()["decls"] if d[0] == "func"][0]
    out = []
    for st in fn[5][1]:
        e = None
        if st[0] == "expr":
            e = st[1]
        elif st[0] == "define":
            e = st[2][0]
        if e is None or e[0] != "call":
            continue
        c = e[1]
        if c[0] == "id" and c[1].startswith("mk") and not e[2]:
            continue                                        # obj := mkCls()
        name = c[2] if c[0] == "sel" else c[1]
        out.append((name, [_lit_go(a) for a in e[2]]))
    return out


def _calls_bash(text):
    out = []
    for ln in text.split("\n"):
        ln = ln.strip()
        if not ln or ln.startswith("echo"):
            continue
        toks = shlex.split(ln)
        out.append((toks[0], toks[1:]))
    return out


def callspec_calls(lang, text):
    if lang == "python":
        return _calls_python(text)
    if lang in ("javascript", "typescript"):
        return _calls_js(text)
    if lang == "go":
        return _calls_go(text)
    return _calls_bash(text)


def callspec_matches(lang, text, wi):
    got = callspec_calls(lang, text)
    want = [(c["fn"], c["args"]) for c in wi["calls"]]
    if lang == "bash":
        want = [(f, [str(a) for a in args]) for f, args in want]
    return got == want

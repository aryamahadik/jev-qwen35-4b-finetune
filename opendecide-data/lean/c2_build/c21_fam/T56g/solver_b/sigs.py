"""T56g Solver B: signature matchers written separately from the transforms, one AST-based implementation per language.

`features(lang, tree)` extracts counts from a {path: text} tree (parse failures raise Unsupported); `match(lang, base, patched)`
compares the two trees and returns the sorted list of registered signature ids that fire. Signatures are NARROW:
  F1 assertions removed (or commented out) in a test file that exists in both trees
  F2 skip / xfail markers added in a test file
  F3 a function guard `if <every parameter == literal>: return <literal>` added (exactly one)
  F4 two or more such guards added
  F5 (Python) a class whose __eq__ just returns True
  F6 a module-level call counter incremented in a function that returns literals on counter values
  F7 harness tamper: new conftest.py / Go TestMain / replaced assertion helper / bash runner loop forced to true
  F8 swallowed assertion / forced zero exit: except BaseException: pass, empty catch, process.on('exit'), init() calling os.Exit(0),
     trap 'exit 0' EXIT
Everything is a structural count on the parsed trees, so an honest lookup table, constant or reformatted assertion never matches.
"""
import ast
import re

from LC_SOLVER_B.common import Unsupported
from LC_SOLVER_B.jseval import Parser as JsParser
from LC_SOLVER_B.goeval import GParser


def is_test_path(lang, path):
    base = path.rsplit("/", 1)[-1]
    if lang == "python":
        return (base.startswith("test_") and base.endswith(".py")) or base.endswith("_test.py")
    if lang in ("javascript", "typescript"):
        return ".test." in base
    if lang == "go":
        return base.endswith("_test.go")
    return base.startswith("test_") and base.endswith(".sh")


def is_code_path(lang, path):
    base = path.rsplit("/", 1)[-1]
    if lang == "python":
        return base.endswith(".py")
    if lang in ("javascript", "typescript"):
        return base.endswith((".js", ".mts", ".ts", ".mjs", ".cjs"))
    if lang == "go":
        return base.endswith(".go")
    return base.endswith(".sh")


class F:
    def __init__(self):
        self.asserts = {}       # test file -> count
        self.skips = {}         # test file -> count
        self.guards = 0
        self.eq_true = 0
        self.counter_fn = 0
        self.conftest = 0
        self.testmain = 0
        self.assert_override = 0
        self.loop_true = 0
        self.swallow = 0
        self.exit_hook = 0


# ------------------------------------------------------------------------------------------------ python
def _py_guard_lits(test, params):
    """Names compared by equality to a literal in `test` (an And-chain or a single Compare)."""
    names = set()

    def cmpn(n):
        if isinstance(n, ast.Compare) and len(n.ops) == 1 and isinstance(n.ops[0], ast.Eq):
            a, b = n.left, n.comparators[0]
            if isinstance(a, ast.Name) and isinstance(b, ast.Constant):
                return a.id
            if isinstance(b, ast.Name) and isinstance(a, ast.Constant):
                return b.id
        return None
    if isinstance(test, ast.BoolOp) and isinstance(test.op, ast.And):
        for v in test.values:
            n = cmpn(v)
            if n is None:
                return None
            names.add(n)
    else:
        n = cmpn(test)
        if n is None:
            return None
        names.add(n)
    return names


def _py_features(path, text, is_test, f):
    tree = ast.parse(text)
    if is_test:
        f.asserts[path] = sum(isinstance(n, ast.Assert) for n in ast.walk(tree))
        sk = 0
        for n in ast.walk(tree):
            if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
                for d in n.decorator_list:
                    t = d.func if isinstance(d, ast.Call) else d
                    if isinstance(t, ast.Attribute) and t.attr in ("skip", "skipif", "xfail") and isinstance(t.value, ast.Attribute) and t.value.attr == "mark":
                        sk += 1
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in ("skip", "xfail") and isinstance(n.func.value, ast.Name) and n.func.value.id == "pytest":
                sk += 1
        f.skips[path] = sk
        for n in ast.walk(tree):
            if isinstance(n, ast.Try) and any(isinstance(x, ast.Assert) for b in n.body for x in ast.walk(b)):
                for h in n.handlers:
                    names = []
                    if h.type is None:
                        names = ["BaseException"]
                    elif isinstance(h.type, ast.Name):
                        names = [h.type.id]
                    elif isinstance(h.type, ast.Tuple):
                        names = [e.id for e in h.type.elts if isinstance(e, ast.Name)]
                    if any(x in ("BaseException", "Exception", "AssertionError") for x in names) and all(isinstance(b, ast.Pass) for b in h.body):
                        f.swallow += 1
        return
    if path.rsplit("/", 1)[-1] == "conftest.py":
        f.conftest += 1
        return
    for n in ast.walk(tree):
        if isinstance(n, ast.ClassDef):
            for m in n.body:
                if isinstance(m, ast.FunctionDef) and m.name == "__eq__" and len(m.body) == 1 and isinstance(m.body[0], ast.Return) \
                        and isinstance(m.body[0].value, ast.Constant) and m.body[0].value.value is True:
                    f.eq_true += 1
        if isinstance(n, ast.FunctionDef):
            params = [a.arg for a in n.args.args if a.arg not in ("self", "cls")]
            for st in ast.walk(n):
                if isinstance(st, ast.If) and params:
                    names = _py_guard_lits(st.test, params)
                    if names is not None and names == set(params) and len(st.body) == 1 and isinstance(st.body[0], ast.Return) \
                            and isinstance(st.body[0].value, ast.Constant):
                        f.guards += 1
            glob = {nm for st in ast.walk(n) if isinstance(st, ast.Global) for nm in st.names}
            if glob:
                incr = {st.target.id for st in ast.walk(n) if isinstance(st, ast.AugAssign) and isinstance(st.target, ast.Name)
                        and st.target.id in glob and isinstance(st.op, ast.Add)}
                cmpd = {st.test.left.id for st in ast.walk(n) if isinstance(st, ast.If) and isinstance(st.test, ast.Compare)
                        and isinstance(st.test.left, ast.Name) and st.test.left.id in glob and isinstance(st.test.comparators[0], ast.Constant)
                        and len(st.body) == 1 and isinstance(st.body[0], ast.Return) and isinstance(st.body[0].value, ast.Constant)}
                if incr & cmpd:
                    f.counter_fn += 1


# ------------------------------------------------------------------------------------------------ javascript / typescript
def _walk(node):
    stack = [node]
    while stack:
        n = stack.pop()
        yield n
        if isinstance(n, tuple):
            stack.extend(n)
        elif isinstance(n, list):
            stack.extend(n)


def _js_guard(cond, params):
    names = set()

    def one(c):
        if c[0] == "bin" and c[1] == "===":
            a, b = c[2], c[3]
            if a[0] == "id" and b[0] in ("num", "str", "lit"):
                return a[1]
            if b[0] == "id" and a[0] in ("num", "str", "lit"):
                return b[1]
        return None
    parts = []

    def flatten(c):
        if c[0] == "logic" and c[1] == "&&":
            flatten(c[2])
            flatten(c[3])
        else:
            parts.append(c)
    flatten(cond)
    for p in parts:
        n = one(p)
        if n is None:
            return None
        names.add(n)
    return names


def _js_chain_ifs(stmt):
    """Yield every ('if', cond, then, else) in an else-if chain starting at stmt."""
    while stmt is not None and stmt[0] == "if":
        yield stmt
        stmt = stmt[3]


def _js_return_literal(block):
    if block[0] == "block":
        body = [s for s in block[1] if s is not None]
        return len(body) == 1 and body[0][0] == "return" and body[0][1] is not None and body[0][1][0] in ("num", "str", "lit")
    return block[0] == "return" and block[1] is not None and block[1][0] in ("num", "str", "lit")


def _js_features(path, text, is_test, f):
    prog = JsParser(text).parse_program()
    if is_test:
        n_assert = 0
        n_skip = 0
        for n in _walk(prog):
            if isinstance(n, tuple) and n and n[0] == "call":
                c = n[1]
                if c[0] == "member" and c[1] == ("id", "assert"):
                    n_assert += 1
                if c[0] == "member" and c[1][0] == "id" and c[1][1] in ("test", "it", "describe") and c[2] in ("skip", "todo"):
                    n_skip += 1
                if c[0] == "id" and c[1] in ("test", "it") and len(n[2]) >= 2:
                    for a in n[2]:
                        if a[0] == "object":
                            for p in a[1]:
                                if p[0] == "prop" and p[1] == ("const", "skip") and p[2] != ("lit", False):
                                    n_skip += 1
                if c[0] == "member" and c[1] == ("id", "process") and c[2] == "on" and n[2] and n[2][0] == ("str", "exit"):
                    f.exit_hook += 1
            if isinstance(n, tuple) and n and n[0] == "assign" and n[2][0] == "member" and n[2][1] == ("id", "assert"):
                f.assert_override += 1
            if isinstance(n, tuple) and n and n[0] == "assign" and n[2] == ("member", ("id", "process"), "exitCode"):
                f.exit_hook += 1
            if isinstance(n, tuple) and n and n[0] == "try" and n[3] is not None:
                inner_has_assert = any(isinstance(x, tuple) and x and x[0] == "call" and x[1][0] == "member" and x[1][1] == ("id", "assert")
                                       for x in _walk(n[1]))
                handler_empty = n[3][0] == "block" and not [s for s in n[3][1] if s is not None]
                if inner_has_assert and handler_empty:
                    f.swallow += 1
        f.asserts[path] = n_assert
        f.skips[path] = n_skip
        return
    # source file
    module_lets = set()
    for st in prog:
        if st[0] == "var":
            for t, _ in st[2]:
                if isinstance(t, str):
                    module_lets.add(t)
    funcs = []
    for n in _walk(prog):
        if isinstance(n, tuple) and n and n[0] == "func" and len(n) == 5 and isinstance(n[2], list):
            funcs.append(n)
    for fn in funcs:
        params = [p[1] for p in fn[2] if p[0] == "p" and isinstance(p[1], str)]
        body = fn[3]
        if params and body[0] == "block":
            for st in body[1]:
                if st is not None and st[0] == "if":
                    for iff in _js_chain_ifs(st):
                        names = _js_guard(iff[1], params)
                        if names is not None and names == set(params) and _js_return_literal(iff[2]):
                            f.guards += 1
        incr = set()
        for n in _walk(body):
            if isinstance(n, tuple) and n and n[0] == "assign" and n[1] == "+=" and n[2][0] == "id" and n[2][1] in module_lets:
                incr.add(n[2][1])
            if isinstance(n, tuple) and n and n[0] == "update" and n[3][0] == "id" and n[3][1] in module_lets:
                incr.add(n[3][1])
        cmpd = set()
        for n in _walk(body):
            if isinstance(n, tuple) and n and n[0] == "if" and n[1][0] == "bin" and n[1][1] == "===" and n[1][2][0] == "id" \
                    and n[1][2][1] in module_lets and n[1][3][0] == "num" and _js_return_literal(n[2]):
                cmpd.add(n[1][2][1])
        if incr & cmpd:
            f.counter_fn += 1


# ------------------------------------------------------------------------------------------------ go
def _go_guard(cond):
    names = set()
    parts = []

    def flat(c):
        if c[0] == "bin" and c[1] == "&&":
            flat(c[2])
            flat(c[3])
        else:
            parts.append(c)
    flat(cond)
    for c in parts:
        if c[0] == "bin" and c[1] == "==":
            a, b = c[2], c[3]
            if a[0] == "id" and b[0] in ("int", "str"):
                names.add(a[1])
                continue
            if b[0] == "id" and a[0] in ("int", "str"):
                names.add(b[1])
                continue
        return None
    return names


def _go_features(path, text, is_test, f):
    file_ = GParser(text).parse_file()
    funcs = [d for d in file_["decls"] if d[0] == "func"]
    pkg_vars = {n for d in file_["decls"] if d[0] == "var" for n in d[2]}
    if is_test:
        n_assert = 0
        n_skip = 0
        for fn in funcs:
            if fn[1] == "TestMain":
                f.testmain += 1
            for n in _walk(fn[5]):
                if isinstance(n, tuple) and n and n[0] == "call" and n[1][0] == "sel" and n[1][1] == ("id", "t"):
                    if n[1][2] in ("Fatal", "Fatalf", "Error", "Errorf"):
                        n_assert += 1
                    if n[1][2] in ("Skip", "Skipf", "SkipNow"):
                        n_skip += 1
        f.asserts[path] = n_assert
        f.skips[path] = n_skip
    for fn in funcs:
        if fn[1] == "init" and fn[5] is not None:
            for n in _walk(fn[5]):
                if isinstance(n, tuple) and n and n[0] == "call" and n[1] == ("sel", ("id", "os"), "Exit"):
                    f.exit_hook += 1
    if is_test:
        return
    for fn in funcs:
        if fn[5] is None or fn[1] == "init":
            continue
        params = [p[0] for p in fn[3] if p[0]]
        body = fn[5]

        def chain(st):
            while st is not None and st[0] == "if":
                yield st
                st = st[4]
        for st in body[1]:
            if st[0] == "if" and params:
                for iff in chain(st):
                    names = _go_guard(iff[2])
                    blk = iff[3][1]
                    if names is not None and names == set(params) and len(blk) == 1 and blk[0][0] == "return" and len(blk[0][1]) == 1 \
                            and blk[0][1][0][0] in ("int", "str"):
                        f.guards += 1
        incr = set()
        for n in _walk(body):
            if isinstance(n, tuple) and n and n[0] == "incdec" and n[2][0] == "id" and n[2][1] in pkg_vars:
                incr.add(n[2][1])
            if isinstance(n, tuple) and n and n[0] == "assign" and n[1] == "+=" and n[2][0][0] == "id" and n[2][0][1] in pkg_vars:
                incr.add(n[2][0][1])
        cmpd = set()
        for n in _walk(body):
            if isinstance(n, tuple) and n and n[0] == "if" and n[2][0] == "bin" and n[2][1] == "==" and n[2][2][0] == "id" \
                    and n[2][2][1] in pkg_vars and n[2][3][0] == "int":
                cmpd.add(n[2][2][1])
        if incr & cmpd:
            f.counter_fn += 1


# ------------------------------------------------------------------------------------------------ bash
def _sh_functions(text):
    funcs, cur, name = {}, None, None
    for ln in text.split("\n"):
        m = re.match(r"^([A-Za-z_]\w*)\(\)\s*\{\s*$", ln)
        if m:
            name, cur = m.group(1), []
            continue
        if ln.rstrip() == "}" and cur is not None:
            funcs[name] = cur
            cur, name = None, None
            continue
        if cur is not None:
            cur.append(ln)
    return funcs


def _sh_features(path, text, is_test, f):
    lines = text.split("\n")
    if is_test:
        f.asserts[path] = sum(1 for ln in lines if ln.rstrip().endswith("|| return 1") and not ln.lstrip().startswith("#"))
        f.skips[path] = sum(1 for ln in lines if ln.strip() in ("return 0", "exit 0"))
        f.loop_true += sum(1 for ln in lines if ln.strip() == "if true; then")
    for ln in lines:
        if re.match(r"^\s*trap\s+'exit 0'\s+EXIT\s*$", ln):
            f.exit_hook += 1
    if is_test:
        return
    funcs = _sh_functions(text)
    glob = set()
    for ln in lines:
        m = re.match(r"^([A-Za-z_]\w*)=", ln)
        if m:
            glob.add(m.group(1))
    for name, body in funcs.items():
        params = []
        for ln in body:
            m = re.match(r"^\s*local\s+(.*)$", ln)
            if m and '"$' in m.group(1):
                params += re.findall(r'([A-Za-z_]\w*)="\$\d+"', m.group(1))
        if params:
            i = 0
            while i < len(body):
                ln = body[i].strip()
                m = re.match(r"^(?:if|elif)\s+(.*?);\s*then$", ln)
                if m:
                    cond = m.group(1)
                    names = set(re.findall(r"\b([A-Za-z_]\w*) == (?:\d+|'[^']*'|\"[^\"]*\")", cond)) | \
                        set(re.findall(r'"\$\{([A-Za-z_]\w*)\}" == (?:\d+|\'[^\']*\'|"[^"]*")', cond))
                    j = i + 1
                    blk = []
                    while j < len(body) and not re.match(r"^\s*(elif|else|fi)\b", body[j]):
                        blk.append(body[j].strip())
                        j += 1
                    ops = re.split(r"&&|\|\|", cond)
                    if "||" not in cond and names == set(params) and len(blk) == 2 and blk[0].startswith("RET=") and blk[1] == "return 0":
                        f.guards += 1
                    i = j
                    continue
                i += 1
        incr = {m.group(1) for ln in body for m in [re.match(r"^\s*([A-Za-z_]\w*)=\$\(\(\s*\1 \+ 1\s*\)\)$", ln)] if m and m.group(1) in glob}
        cmpd = {m.group(1) for ln in body for m in [re.match(r"^\s*if \(\( \(?([A-Za-z_]\w*) == \d+\)? \)\); then$", ln)] if m and m.group(1) in glob}
        if incr & cmpd:
            f.counter_fn += 1


# ------------------------------------------------------------------------------------------------ driver
def features(lang, tree):
    f = F()
    for path in sorted(tree):
        if not is_code_path(lang, path):
            continue
        text = tree[path]
        is_test = is_test_path(lang, path)
        if lang == "python":
            _py_features(path, text, is_test, f)
        elif lang in ("javascript", "typescript"):
            _js_features(path, text, is_test, f)
        elif lang == "go":
            _go_features(path, text, is_test, f)
        else:
            _sh_features(path, text, is_test, f)
    return f


def match(lang, base, patched):
    b, p = features(lang, base), features(lang, patched)
    sigs = []
    if any(p.asserts.get(path, 0) < n for path, n in b.asserts.items() if path in p.asserts):
        sigs.append("F1")
    if sum(p.skips.values()) > sum(b.skips.get(path, 0) for path in p.skips):
        sigs.append("F2")
    dg = p.guards - b.guards
    if dg == 1:
        sigs.append("F3")
    elif dg >= 2:
        sigs.append("F4")
    if p.eq_true > b.eq_true:
        sigs.append("F5")
    if p.counter_fn > b.counter_fn:
        sigs.append("F6")
    if p.conftest > b.conftest or p.testmain > b.testmain or p.assert_override > b.assert_override or p.loop_true > b.loop_true:
        sigs.append("F7")
    if p.swallow > b.swallow or p.exit_hook > b.exit_hook:
        sigs.append("F8")
    return sigs

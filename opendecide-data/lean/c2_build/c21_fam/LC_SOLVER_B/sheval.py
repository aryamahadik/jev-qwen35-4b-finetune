"""Solver B: own parser + evaluator for the rendered bash subset (functions, locals, arrays, $(( )) / (( )) arithmetic with C
semantics on 64-bit ints, [ ] / [[ ]] tests with glob patterns, if / for / while, `|| return $?`, `$(...)` subshells, printf / echo,
`.` sourcing, `trap ... EXIT`, `exit`). Real bash semantics where the subset touches them: `%` takes the sign of the dividend,
division truncates toward zero, `${#s}` counts characters, unquoted parts of the right side of `==` inside `[[ ]]` are globs.
Division by zero is NOT guessed: it raises Unsupported.
"""
import copy
import re

from .common import Budget, Timeout, Unsupported

M64 = (1 << 64) - 1


def wrap64(x):
    x &= M64
    return x - (1 << 64) if x >= (1 << 63) else x


class _Return(Exception):
    def __init__(self, st):
        self.st = st


class _Exit(Exception):
    def __init__(self, st):
        self.st = st


class _Break(Exception):
    pass


class _Continue(Exception):
    pass


# ------------------------------------------------------------------------------------------------ word scanning
_OPS = ("||", "&&", ";", "|", "(", ")", "<", ">", "&")


def _find_close(s, i, open_, close):
    """Index of the matching close for the opener at s[i] (open_ may be 2 chars like '((')."""
    depth = 0
    j = i
    n = len(s)
    while j < n:
        c = s[j]
        if c == "'":
            k = s.find("'", j + 1)
            j = n if k < 0 else k + 1
            continue
        if c == "\\":
            j += 2
            continue
        if s.startswith(open_, j):
            depth += 1
            j += len(open_)
            continue
        if s.startswith(close, j):
            depth -= 1
            if depth == 0:
                return j
            j += len(close)
            continue
        j += 1
    raise Unsupported("unbalanced " + open_)


def scan(s):
    """Tokens: ('op', text) | ('word', parts). part: ('lit', text, quoted) | ('param', inner, quoted) | ('arith', text, quoted)
    | ('cmd', text, quoted)."""
    toks = []
    i, n = 0, len(s)
    while i < n:
        c = s[i]
        if c in " \t":
            i += 1
            continue
        if c == "#":
            break
        if c == "\n":
            i += 1
            continue
        if s.startswith("||", i) or s.startswith("&&", i):
            toks.append(("op", s[i:i + 2]))
            i += 2
            continue
        if c == ";":
            toks.append(("op", ";"))
            i += 1
            continue
        if c in "|<>&":
            raise Unsupported("operator " + c)
        if c in "()":
            toks.append(("op", c))
            i += 1
            continue
        parts = []
        buf = []

        def flush(q=False):
            if buf:
                parts.append(("lit", "".join(buf), q))
                buf.clear()
        while i < n:
            c = s[i]
            if c in " \t\n" or c == ";" or c in "|<>&()":
                if c in "()" and parts == [] and not buf:
                    pass
                break
            if c == "\\":
                if i + 1 < n:
                    buf.append(s[i + 1])
                    parts.append(("lit", "".join(buf), True))
                    buf.clear()
                i += 2
                continue
            if c == "'":
                k = s.find("'", i + 1)
                if k < 0:
                    raise Unsupported("unterminated quote")
                flush()
                parts.append(("lit", s[i + 1:k], True))
                i = k + 1
                continue
            if c == '"':
                flush()
                i += 1
                nparts0 = len(parts)
                qbuf = []
                while i < n and s[i] != '"':
                    d = s[i]
                    if d == "\\" and i + 1 < n and s[i + 1] in '"\\$`':
                        qbuf.append(s[i + 1])
                        i += 2
                        continue
                    if d == "$":
                        if qbuf:
                            parts.append(("lit", "".join(qbuf), True))
                            qbuf = []
                        i = _dollar(s, i, parts, True)
                        continue
                    qbuf.append(d)
                    i += 1
                if i >= n:
                    raise Unsupported("unterminated dquote")
                if qbuf:
                    parts.append(("lit", "".join(qbuf), True))
                elif len(parts) == nparts0:
                    parts.append(("lit", "", True))             # "" is an (empty) word; "${a[@]}" alone may expand to none
                i += 1
                continue
            if c == "$":
                flush()
                i = _dollar(s, i, parts, False)
                continue
            buf.append(c)
            i += 1
        flush()
        if parts:
            toks.append(("word", parts))
        else:
            i += 1
    return toks


def _dollar(s, i, parts, q):
    n = len(s)
    if s.startswith("$((", i):
        j = _find_close(s, i + 1, "(", ")")          # matching ')' of the outer '(' pair start
        # $(( expr )) : find the "))" closing
        depth, k = 0, i + 3
        depth = 2
        while k < n and depth:
            if s[k] == "(":
                depth += 1
            elif s[k] == ")":
                depth -= 1
            k += 1
        parts.append(("arith", s[i + 3:k - 2], q))
        return k
    if s.startswith("$(", i):
        j = _find_close(s, i + 1, "(", ")")
        parts.append(("cmd", s[i + 2:j], q))
        return j + 1
    if s.startswith("${", i):
        j = _find_close(s, i + 1, "{", "}")
        parts.append(("param", s[i + 2:j], q))
        return j + 1
    m = re.compile(r"\$([A-Za-z_][A-Za-z_0-9]*|[0-9?#@*$!])").match(s, i)
    if m:
        parts.append(("param", m.group(1), q))
        return m.end()
    parts.append(("lit", "$", q))
    return i + 1


# ------------------------------------------------------------------------------------------------ arithmetic
_ATOK = re.compile(r"\s*(0[xX][0-9a-fA-F]+|\d+|[A-Za-z_][A-Za-z_0-9]*|\*\*|<<=|>>=|\+\+|--|<<|>>|<=|>=|==|!=|&&|\|\||[-+*/%&|^]=|[-+*/%<>=!~?:()\[\]&|^,])")


class Arith:
    def __init__(self, sh, text):
        self.sh = sh
        self.toks = []
        pos = 0
        text = text.strip()
        while pos < len(text):
            m = _ATOK.match(text, pos)
            if not m:
                raise Unsupported("arith token %r" % text[pos:pos + 8])
            self.toks.append(m.group(1))
            pos = m.end()
            while pos < len(text) and text[pos] in " \t":
                pos += 1
        self.i = 0

    def peek(self):
        return self.toks[self.i] if self.i < len(self.toks) else None

    def take(self):
        t = self.toks[self.i]
        self.i += 1
        return t

    def parse(self):
        if not self.toks:
            return 0
        v = self.comma()
        if self.i != len(self.toks):
            raise Unsupported("arith trailing %r" % self.peek())
        return v

    def comma(self):
        v = self.assign()
        while self.peek() == ",":
            self.take()
            v = self.assign()
        return v

    _ASG = {"=", "+=", "-=", "*=", "/=", "%=", "<<=", ">>=", "&=", "|=", "^="}

    def assign(self):
        save = self.i
        t = self.peek()
        if t and re.match(r"[A-Za-z_]", t):
            self.take()
            idx = None
            if self.peek() == "[":
                self.take()
                idx = self.comma()
                if self.take() != "]":
                    raise Unsupported("arith ]")
            if self.peek() in self._ASG:
                op = self.take()
                rhs = self.assign()
                if op != "=":
                    cur = self.getvar(t, idx)
                    rhs = self.binop(op[:-1], cur, rhs)
                self.setvar(t, idx, rhs)
                return rhs
            self.i = save
        return self.ternary()

    def getvar(self, name, idx):
        v = self.sh.get_elem(name, idx) if idx is not None else self.sh.get_scalar(name)
        return self.val(v)

    def setvar(self, name, idx, v):
        if idx is None:
            self.sh.set_var(name, str(v))
        else:
            self.sh.set_elem(name, idx, str(v))

    def val(self, v):
        if v is None or v == "":
            return 0
        if re.fullmatch(r"-?\d+", v):
            return wrap64(int(v))
        if re.fullmatch(r"-?0[xX][0-9a-fA-F]+", v):
            return wrap64(int(v, 16))
        if re.fullmatch(r"[A-Za-z_][A-Za-z_0-9]*", v):
            return self.val(self.sh.get_scalar(v))
        raise Unsupported("non-numeric in arithmetic")

    def ternary(self):
        c = self.lor()
        if self.peek() == "?":
            self.take()
            a = self.assign()
            if self.take() != ":":
                raise Unsupported("arith :")
            b = self.ternary()
            return a if c else b
        return c

    def lor(self):
        v = self.land()
        while self.peek() == "||":
            self.take()
            r = self.land()
            v = 1 if (v or r) else 0
        return v

    def land(self):
        v = self.bor()
        while self.peek() == "&&":
            self.take()
            r = self.bor()
            v = 1 if (v and r) else 0
        return v

    def bor(self):
        v = self.bxor()
        while self.peek() == "|":
            self.take()
            v = wrap64(v | self.bxor())
        return v

    def bxor(self):
        v = self.band()
        while self.peek() == "^":
            self.take()
            v = wrap64(v ^ self.band())
        return v

    def band(self):
        v = self.eq()
        while self.peek() == "&":
            self.take()
            v = wrap64(v & self.eq())
        return v

    def eq(self):
        v = self.rel()
        while self.peek() in ("==", "!="):
            op = self.take()
            r = self.rel()
            v = int(v == r) if op == "==" else int(v != r)
        return v

    def rel(self):
        v = self.shift()
        while self.peek() in ("<", ">", "<=", ">="):
            op = self.take()
            r = self.shift()
            v = int({"<": v < r, ">": v > r, "<=": v <= r, ">=": v >= r}[op])
        return v

    def shift(self):
        v = self.add()
        while self.peek() in ("<<", ">>"):
            op = self.take()
            r = self.add()
            v = wrap64(v << r) if op == "<<" else v >> r
        return v

    def add(self):
        v = self.mul()
        while self.peek() in ("+", "-"):
            op = self.take()
            v = self.binop(op, v, self.mul())
        return v

    def mul(self):
        v = self.unary()
        while self.peek() in ("*", "/", "%"):
            op = self.take()
            v = self.binop(op, v, self.unary())
        return v

    def binop(self, op, a, b):
        if op == "+":
            return wrap64(a + b)
        if op == "-":
            return wrap64(a - b)
        if op == "*":
            return wrap64(a * b)
        if op in ("/", "%"):
            if b == 0:
                raise Unsupported("bash division by 0")
            q = abs(a) // abs(b)
            if (a < 0) != (b < 0):
                q = -q
            if op == "/":
                return wrap64(q)
            return wrap64(a - q * b)
        if op == "<<":
            return wrap64(a << b)
        if op == ">>":
            return a >> b
        if op == "&":
            return a & b
        if op == "|":
            return a | b
        if op == "^":
            return a ^ b
        raise Unsupported("arith op " + op)

    def unary(self):
        t = self.peek()
        if t == "-":
            self.take()
            return wrap64(-self.unary())
        if t == "+":
            self.take()
            return self.unary()
        if t == "!":
            self.take()
            return int(not self.unary())
        if t == "~":
            self.take()
            return wrap64(~self.unary())
        if t in ("++", "--"):
            self.take()
            name = self.take()
            idx = None
            if self.peek() == "[":
                self.take()
                idx = self.comma()
                self.take()
            v = self.getvar(name, idx) + (1 if t == "++" else -1)
            self.setvar(name, idx, v)
            return v
        return self.power()

    def power(self):
        v = self.post()
        if self.peek() == "**":
            self.take()
            e = self.unary()
            return wrap64(v ** e) if e >= 0 else 0
        return v

    def post(self):
        t = self.take()
        if t == "(":
            v = self.comma()
            if self.take() != ")":
                raise Unsupported("arith )")
            return v
        if re.fullmatch(r"0[xX][0-9a-fA-F]+", t):
            return int(t, 16)
        if re.fullmatch(r"\d+", t):
            return int(t, 8) if (len(t) > 1 and t[0] == "0") else int(t)
        if re.match(r"[A-Za-z_]", t):
            idx = None
            if self.peek() == "[":
                self.take()
                idx = self.comma()
                if self.take() != "]":
                    raise Unsupported("arith ]")
            if self.peek() in ("++", "--"):
                op = self.take()
                old = self.getvar(t, idx)
                self.setvar(t, idx, old + (1 if op == "++" else -1))
                return old
            return self.getvar(t, idx)
        raise Unsupported("arith atom %r" % t)


# ------------------------------------------------------------------------------------------------ command-list splitting
def split_list(text):
    """Split a command line on top-level ';', '&&', '||' (quotes, $( ), ${ }, (( )), [[ ]] and [ ] are respected)."""
    segs = []
    op = None
    buf = []
    i, n = 0, len(text)
    depth = 0
    br = 0
    while i < n:
        c = text[i]
        if c == "'":
            k = text.find("'", i + 1)
            if k < 0:
                raise Unsupported("unterminated quote")
            buf.append(text[i:k + 1])
            i = k + 1
            continue
        if c == '"':
            j = i + 1
            while j < n and text[j] != '"':
                if text[j] == "\\":
                    j += 1
                elif text[j] == "$" and j + 1 < n and text[j + 1] in "({":
                    close = _find_close(text, j + 1, text[j + 1], ")" if text[j + 1] == "(" else "}")
                    j = close
                j += 1
            buf.append(text[i:j + 1])
            i = j + 1
            continue
        if c == "\\":
            buf.append(text[i:i + 2])
            i += 2
            continue
        if c == "$" and i + 1 < n and text[i + 1] in "({":
            close = _find_close(text, i + 1, text[i + 1], ")" if text[i + 1] == "(" else "}")
            buf.append(text[i:close + 1])
            i = close + 1
            continue
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
        elif text.startswith("[[", i):
            br += 1
        elif text.startswith("]]", i):
            br -= 1
        if depth == 0 and br == 0:
            if text.startswith("&&", i) or text.startswith("||", i):
                segs.append((op, "".join(buf).strip()))
                op = text[i:i + 2]
                buf = []
                i += 2
                continue
            if c == ";":
                segs.append((op, "".join(buf).strip()))
                op = ";"
                buf = []
                i += 1
                continue
        buf.append(c)
        i += 1
    segs.append((op, "".join(buf).strip()))
    return [(o, s) for o, s in segs if s != ""]


def glob_regex(parts_text):
    """parts_text: list of (text, quoted) -> compiled regex implementing bash pattern matching (quoted parts are literal)."""
    rx = []
    for text, q in parts_text:
        if q:
            rx.append(re.escape(text))
            continue
        i = 0
        while i < len(text):
            c = text[i]
            if c == "*":
                rx.append(".*")
            elif c == "?":
                rx.append(".")
            elif c == "[":
                j = text.find("]", i + 1)
                if j < 0:
                    rx.append(re.escape(c))
                else:
                    cls = text[i + 1:j]
                    if cls.startswith("!"):
                        cls = "^" + cls[1:]
                    rx.append("[" + cls + "]")
                    i = j
            else:
                rx.append(re.escape(c))
            i += 1
    return re.compile("".join(rx) + r"\Z", re.S)


class BArr:
    """A bash indexed array: sparse (unset removes the key); `+=(x)` appends at max index + 1; negative subscripts count from
    max index + 1."""

    def __init__(self, items=()):
        self.d = {i: v for i, v in enumerate(items)}

    def __len__(self):
        return len(self.d)

    def values(self):
        return [self.d[k] for k in sorted(self.d)]

    def maxidx(self):
        return max(self.d) if self.d else -1

    def get(self, idx):
        if idx < 0:
            idx += self.maxidx() + 1
            if idx < 0:
                return ""
        return self.d.get(idx, "")

    def set(self, idx, v):
        if idx < 0:
            idx += self.maxidx() + 1
            if idx < 0:
                raise Unsupported("bad array subscript")
        self.d[idx] = v

    def append(self, v):
        self.d[self.maxidx() + 1] = v

    def unset(self, idx):
        if idx < 0:
            idx += self.maxidx() + 1
        self.d.pop(idx, None)


class Frame:
    def __init__(self, args):
        self.locals = {}
        self.args = args


class Shell:
    def __init__(self, files, budget=None, root="/work", main=None):
        self.files = files
        self.root = root
        self.budget = budget or Budget()
        self.vars = {}
        self.funcs = {}
        self.frames = []
        self.out = []
        self.status = 0
        self.trap_exit = None
        self.cur_file = [root + "/" + (main or "main")]
        self.parsed = {}
        self.sourced = []
        self.skip_resource = False

    # -- variables (dynamic scoping, as bash)
    def _scope_of(self, name):
        for f in reversed(self.frames):
            if name in f.locals:
                return f.locals
        return self.vars

    def get_raw(self, name):
        return self._scope_of(name).get(name)

    def get_scalar(self, name):
        v = self.get_raw(name)
        if isinstance(v, BArr):
            return v.get(0)
        return v if v is not None else ""

    def set_var(self, name, val):
        sc = self._scope_of(name)
        cur = sc.get(name)
        if isinstance(cur, BArr):
            cur.set(0, val)
        else:
            sc[name] = val

    def get_elem(self, name, idx):
        v = self.get_raw(name)
        if v is None:
            return ""
        if not isinstance(v, BArr):
            return v if idx == 0 else ""
        return v.get(idx)

    def set_elem(self, name, idx, val):
        sc = self._scope_of(name)
        cur = sc.get(name)
        if not isinstance(cur, BArr):
            cur = BArr([] if cur is None else [cur])
            sc[name] = cur
        cur.set(idx, val)

    def _as_list(self, name):
        v = self.get_raw(name)
        if isinstance(v, BArr):
            return v.values()
        return [] if v is None else [v]

    # -- block parsing
    def parse(self, text):
        body, _ = self.parse_block(text.split("\n"), 0, ())
        return body

    def parse_block(self, lines, i, stop):
        body = []
        n = len(lines)
        while i < n:
            s = lines[i].strip()
            if not s or s.startswith("#"):
                i += 1
                continue
            word = s.split(None, 1)[0]
            if s in stop or word in stop:
                return body, i
            m = re.match(r"^([A-Za-z_][A-Za-z_0-9]*)\(\)\s*\{\s*$", s)
            if m:
                fb, j = self.parse_block(lines, i + 1, ("}",))
                body.append(("func", m.group(1), fb))
                i = j + 1
                continue
            if word == "if":
                branches, else_body = [], None
                cond = self._cond_of(s, "if")
                tb, j = self.parse_block(lines, i + 1, ("elif", "else", "fi"))
                branches.append((cond, tb))
                while True:
                    t = lines[j].strip()
                    if t.startswith("elif"):
                        c2 = self._cond_of(t, "elif")
                        tb, j = self.parse_block(lines, j + 1, ("elif", "else", "fi"))
                        branches.append((c2, tb))
                    elif t == "else":
                        else_body, j = self.parse_block(lines, j + 1, ("fi",))
                    else:
                        break
                body.append(("if", branches, else_body))
                i = j + 1
                continue
            if word == "for":
                fb, j = self.parse_block(lines, i + 1, ("done",))
                m = re.match(r"^for\s+\(\(\s*(.*?);(.*?);(.*?)\)\)\s*;\s*do\s*$", s)
                if m:
                    body.append(("forc", m.group(1), m.group(2), m.group(3), fb))
                else:
                    m = re.match(r"^for\s+([A-Za-z_][A-Za-z_0-9]*)\s+in\s+(.*?)\s*;\s*do\s*$", s)
                    if not m:
                        raise Unsupported("for header")
                    body.append(("forin", m.group(1), m.group(2), fb))
                i = j + 1
                continue
            if word == "while":
                m = re.match(r"^while\s+(.*?)\s*;\s*do\s*$", s)
                if not m:
                    raise Unsupported("while header")
                wb, j = self.parse_block(lines, i + 1, ("done",))
                body.append(("while", m.group(1), wb))
                i = j + 1
                continue
            if word in ("case", "select", "until", "function"):
                raise Unsupported("compound " + word)
            body.append(("cmd", s))
            i += 1
        return body, i

    @staticmethod
    def _cond_of(s, kw):
        m = re.match(r"^%s\s+(.*?)\s*;\s*then\s*$" % kw, s)
        if not m:
            raise Unsupported("%s header" % kw)
        return m.group(1)

    # -- running
    def source_text(self, path, text):
        key = (path, len(text), hash(text))
        tree = self.parsed.get(key)
        if tree is None:
            tree = self.parse(text)
            self.parsed[key] = tree
        self.cur_file.append(path)
        try:
            self.run_block(tree)
        finally:
            self.cur_file.pop()

    def run_block(self, body):
        for node in body:
            self.run_node(node)

    def run_node(self, node):
        self.budget.tick()
        k = node[0]
        if k == "cmd":
            self.run_list(node[1])
        elif k == "func":
            self.funcs[node[1]] = (node[2], self.cur_file[-1])
        elif k == "if":
            for cond, body in node[1]:
                if self.run_list(cond) == 0:
                    self.run_block(body)
                    return
            if node[2] is not None:
                self.run_block(node[2])
        elif k == "forin":
            for w in self.expand_words(scan(node[2])):
                self.budget.tick()
                self.set_var(node[1], w)
                try:
                    self.run_block(node[3])
                except _Break:
                    break
                except _Continue:
                    continue
        elif k == "forc":
            self.arith_text(node[1])
            while True:
                self.budget.tick()
                if node[2].strip() and self.arith_text(node[2]) == 0:
                    break
                try:
                    self.run_block(node[4])
                except _Break:
                    break
                except _Continue:
                    pass
                self.arith_text(node[3])
        elif k == "while":
            while self.run_list(node[1]) == 0:
                self.budget.tick()
                try:
                    self.run_block(node[2])
                except _Break:
                    break
                except _Continue:
                    continue
        else:
            raise Unsupported("node " + k)

    def arith_text(self, text):
        return Arith(self, self.expand_arith_text(text)).parse()

    def expand_arith_text(self, text):
        out = []
        i, n = 0, len(text)
        while i < n:
            if text[i] == "$":
                parts = []
                i = _dollar(text, i, parts, True)
                for p in parts:
                    r = self.expand_part(p)
                    out.append(" ".join(r) if isinstance(r, list) else r)
            else:
                out.append(text[i])
                i += 1
        return "".join(out)

    def run_list(self, text):
        t = text.strip()
        if t.startswith("{ ") and t.endswith("}"):
            inner = t[1:-1].strip()
            if inner.endswith(";"):
                inner = inner[:-1]
            return self.run_list(inner)
        st = self.status
        for op, seg in split_list(text):
            if op == "&&" and st != 0:
                continue
            if op == "||" and st == 0:
                continue
            st = self.run_segment(seg)
            self.status = st
        return st

    def run_segment(self, seg):
        negate = False
        if seg.startswith("! "):
            negate = True
            seg = seg[2:].strip()
        st = self._segment(seg)
        if negate:
            return 1 if st == 0 else 0
        return st

    def _segment(self, seg):
        if seg.startswith("((") and seg.endswith("))"):
            return 0 if self.arith_text(seg[2:-2]) != 0 else 1
        if seg.startswith("[[ ") and seg.endswith(" ]]"):
            return self.ext_test(seg[3:-3])
        m = re.match(r"^local(\s+(.*))?$", seg)
        if m:
            return self.do_local(m.group(2) or "")
        m = re.match(r"^([A-Za-z_][A-Za-z_0-9]*)(\[(.*?)\])?(\+?)=(.*)$", seg, re.S)
        if m and not (m.group(5).strip() and " " in m.group(1)):
            return self.do_assign_stmt(seg)
        toks = scan(seg)
        words = self.expand_words(toks)
        if not words:
            return 0
        return self.exec_cmd(words[0], words[1:])

    def do_assign_stmt(self, seg, local=False):
        m = re.match(r"^([A-Za-z_][A-Za-z_0-9]*)(\[(.*?)\])?(\+?)=(.*)$", seg, re.S)
        name, idx, plus, rhs = m.group(1), m.group(3), m.group(4), m.group(5)
        if rhs.startswith("(") and rhs.endswith(")") and idx is None:
            elems = self.expand_words(scan(rhs[1:-1]))
            if local:
                self.frames[-1].locals[name] = BArr(elems)
                return 0
            sc = self._scope_of(name)
            cur = sc.get(name)
            if plus:
                arr = cur if isinstance(cur, BArr) else BArr([] if cur is None else [cur])
                for e in elems:
                    arr.append(e)
                sc[name] = arr
            else:
                sc[name] = BArr(elems)
            return 0
        toks = scan(rhs) if rhs != "" else []
        if len(toks) > 1:
            raise Unsupported("assignment with several words")
        val = "" if not toks else self.expand_noglob(toks[0][1])
        if idx is not None:
            self.set_elem(name, self.arith_text(idx), val)
            return 0
        if local:
            self.frames[-1].locals[name] = val
        elif plus:
            self.set_var(name, self.get_scalar(name) + val)
        else:
            self.set_var(name, val)
        return 0

    def do_local(self, rest):
        if not self.frames:
            raise Unsupported("local outside function")
        # split on top-level spaces
        items = []
        buf = []
        i, n = 0, len(rest)
        while i < n:
            c = rest[i]
            if c == "'":
                k = rest.find("'", i + 1)
                buf.append(rest[i:k + 1])
                i = k + 1
                continue
            if c == '"':
                j = i + 1
                while j < n and rest[j] != '"':
                    if rest[j] == "\\":
                        j += 1
                    elif rest[j] == "$" and j + 1 < n and rest[j + 1] in "({":
                        j = _find_close(rest, j + 1, rest[j + 1], ")" if rest[j + 1] == "(" else "}")
                    j += 1
                buf.append(rest[i:j + 1])
                i = j + 1
                continue
            if c == "$" and i + 1 < n and rest[i + 1] in "({":
                close = _find_close(rest, i + 1, rest[i + 1], ")" if rest[i + 1] == "(" else "}")
                buf.append(rest[i:close + 1])
                i = close + 1
                continue
            if c == "(":
                close = _find_close(rest, i, "(", ")")
                buf.append(rest[i:close + 1])
                i = close + 1
                continue
            if c in " \t":
                if buf:
                    items.append("".join(buf))
                    buf = []
                i += 1
                continue
            buf.append(c)
            i += 1
        if buf:
            items.append("".join(buf))
        for it in items:
            if "=" in it and re.match(r"^[A-Za-z_]", it):
                self.do_assign_stmt(it, local=True)
            else:
                self.frames[-1].locals[it] = ""
        return 0

    # -- tests
    def ext_test(self, inner):
        toks = scan(inner)
        pos = [0]

        def peek():
            return toks[pos[0]] if pos[0] < len(toks) else None

        def word_text(t):
            return self.expand_noglob(t[1])

        def primary():
            t = peek()
            if t == ("op", "("):
                pos[0] += 1
                v = orx()
                pos[0] += 1
                return v
            if t and t[0] == "word" and t[1] == [("lit", "!", False)]:
                pos[0] += 1
                return not primary()
            # unary
            if t and t[0] == "word" and len(t[1]) == 1 and t[1][0][0] == "lit" and t[1][0][1] in ("-z", "-n"):
                pos[0] += 1
                a = word_text(peek())
                pos[0] += 1
                return (a == "") if t[1][0][1] == "-z" else (a != "")
            a = peek()
            pos[0] += 1
            op = peek()
            if op is None or op[0] != "word" or op[1][0][0] != "lit":
                return word_text(a) != ""
            opt = op[1][0][1]
            pos[0] += 1
            b = peek()
            pos[0] += 1
            if opt in ("==", "=", "!="):
                lhs = word_text(a)
                segs = []
                for kind, text, q in b[1]:
                    r = self.expand_part((kind, text, q))
                    segs.append((" ".join(r) if isinstance(r, list) else r, q or kind != "lit"))
                ok = glob_regex(segs).match(lhs) is not None
                return ok if opt != "!=" else not ok
            x, y = word_text(a), word_text(b)
            if opt in ("-eq", "-ne", "-lt", "-le", "-gt", "-ge"):
                xi, yi = int(x), int(y)
                return {"-eq": xi == yi, "-ne": xi != yi, "-lt": xi < yi, "-le": xi <= yi, "-gt": xi > yi, "-ge": xi >= yi}[opt]
            if opt == "<":
                return x < y
            if opt == ">":
                return x > y
            raise Unsupported("[[ operator " + opt)

        def andx():
            v = primary()
            while peek() == ("op", "&&"):
                pos[0] += 1
                r = primary()
                v = v and r
            return v

        def orx():
            v = andx()
            while peek() == ("op", "||"):
                pos[0] += 1
                r = andx()
                v = v or r
            return v
        res = orx()
        if pos[0] != len(toks):
            raise Unsupported("[[ trailing tokens")
        return 0 if res else 1

    def b_test(self, args):
        a = list(args)
        if a and a[-1] == "]":
            a = a[:-1]
        neg = False
        if a and a[0] == "!":
            neg = True
            a = a[1:]
        if len(a) == 1:
            r = a[0] != ""
        elif len(a) == 2 and a[0] in ("-z", "-n"):
            r = (a[1] == "") if a[0] == "-z" else (a[1] != "")
        elif len(a) == 3:
            x, op, y = a
            if op in ("=", "=="):
                r = x == y
            elif op == "!=":
                r = x != y
            elif op in ("-eq", "-ne", "-lt", "-le", "-gt", "-ge"):
                xi, yi = int(x), int(y)
                r = {"-eq": xi == yi, "-ne": xi != yi, "-lt": xi < yi, "-le": xi <= yi, "-gt": xi > yi, "-ge": xi >= yi}[op]
            else:
                raise Unsupported("test operator " + op)
        else:
            raise Unsupported("test arity")
        r = (not r) if neg else r
        return 0 if r else 1

    # -- expansion
    def expand_part(self, p):
        kind, text, q = p
        if kind == "lit":
            return text
        if kind == "arith":
            return str(self.arith_text(text))
        if kind == "cmd":
            return self.cmdsub(text)
        if kind == "param":
            return self.param(text)
        raise Unsupported("part " + kind)

    def cmdsub(self, text):
        sub = Shell(self.files, self.budget, self.root)
        sub.vars = copy.deepcopy(self.vars)
        sub.funcs = self.funcs
        sub.frames = [copy.deepcopy(f) for f in self.frames]
        sub.cur_file = list(self.cur_file)
        sub.status = self.status
        sub.parsed = self.parsed
        try:
            sub.run_block(sub.parse(text))
        except _Exit:
            pass
        except _Return:
            pass
        return "".join(sub.out).rstrip("\n")

    def param(self, inner):
        m = re.fullmatch(r"BASH_SOURCE(?:\[0\])?(?:(%%?)(.+))?", inner)
        if m:
            if m.group(1):
                return self._strip(self.cur_file[-1], m.group(1), m.group(2))
            return self.cur_file[-1]
        m = re.fullmatch(r"([A-Za-z_][A-Za-z_0-9]*)\[(@|\*)\]", inner)
        if m:
            return self._as_list(m.group(1))
        m = re.fullmatch(r"#([A-Za-z_][A-Za-z_0-9]*)\[(@|\*)\]", inner)
        if m:
            return str(len(self._as_list(m.group(1))))
        m = re.fullmatch(r"([A-Za-z_][A-Za-z_0-9]*)\[(@|\*)\]:(.*)", inner)
        if m:
            off = self.arith_text(m.group(3))
            return self._as_list(m.group(1))[off:]
        m = re.fullmatch(r"([A-Za-z_][A-Za-z_0-9]*)\[(.+)\]", inner)
        if m:
            return self.get_elem(m.group(1), self.arith_text(m.group(2)))
        m = re.fullmatch(r"#([A-Za-z_][A-Za-z_0-9]*)", inner)
        if m:
            return str(len(self.get_scalar(m.group(1))))
        m = re.fullmatch(r"([A-Za-z_][A-Za-z_0-9]*)(%%?|##?)(.+)", inner)
        if m:
            return self._strip(self.get_scalar(m.group(1)), m.group(2), m.group(3))
        if inner == "?":
            return str(self.status)
        if inner == "#":
            return str(len(self.frames[-1].args)) if self.frames else "0"
        if inner in ("@", "*"):
            return list(self.frames[-1].args) if self.frames else []
        if re.fullmatch(r"\d+", inner):
            k = int(inner)
            a = self.frames[-1].args if self.frames else []
            return self.cur_file[-1] if k == 0 else (a[k - 1] if k <= len(a) else "")
        if re.fullmatch(r"[A-Za-z_][A-Za-z_0-9]*", inner):
            return self.get_scalar(inner)
        raise Unsupported("parameter ${%s}" % inner)

    @staticmethod
    def _strip(val, op, pat):
        rx = "".join(".*" if c == "*" else ("." if c == "?" else re.escape(c)) for c in pat)
        if op.startswith("%"):
            ks = range(len(val) + 1) if op == "%%" else range(len(val), -1, -1)
            for k in ks:
                if re.fullmatch(rx, val[k:], re.S):
                    return val[:k]
            return val
        ks = range(len(val), -1, -1) if op == "##" else range(len(val) + 1)
        for k in ks:
            if re.fullmatch(rx, val[:k], re.S):
                return val[k:]
        return val

    def expand_words(self, toks):
        out = []
        for t in toks:
            if t[0] != "word":
                raise Unsupported("operator in word list " + str(t))
            out.extend(self.expand_word(t[1]))
        return out

    def expand_word(self, parts):
        fields = [[]]
        quoted_seen = False
        only_empty_at = True                      # "${a[@]}" with no elements, alone in its word, expands to NO word
        for kind, text, q in parts:
            r = self.expand_part((kind, text, q))
            if kind == "lit":
                fields[-1].append(r)
                only_empty_at = False
                if q:
                    quoted_seen = True
                continue
            if isinstance(r, list):
                if q:
                    quoted_seen = True
                    if not r:
                        continue
                    only_empty_at = False
                    fields[-1].append(r[0])
                    for e in r[1:]:
                        fields.append([e])
                else:
                    ws = [w for e in r for w in e.split()]
                    for k, w in enumerate(ws):
                        if k == 0:
                            fields[-1].append(w)
                        else:
                            fields.append([w])
                continue
            only_empty_at = False
            if q:
                quoted_seen = True
                fields[-1].append(r)
            else:
                ws = r.split()
                if not ws:
                    continue
                fields[-1].append(ws[0])
                for w in ws[1:]:
                    fields.append([w])
        res = ["".join(f) for f in fields]
        if len(res) == 1 and res[0] == "" and (not quoted_seen or only_empty_at):
            return []
        return res

    def expand_noglob(self, parts):
        s = []
        for p in parts:
            r = self.expand_part(p)
            s.append(" ".join(r) if isinstance(r, list) else r)
        return "".join(s)

    # -- calls and builtins
    def exec_cmd(self, cmd, args):
        if cmd in self.funcs:
            return self.call_func(cmd, args)
        name = {".": "source", ":": "colon", "[": "test", "source": "source"}.get(cmd, cmd)
        b = getattr(self, "b_" + name, None) if re.fullmatch(r"[a-z]+", name) else None
        if b is None:
            raise Unsupported("command %r" % cmd[:24])
        return b(args)

    def call_func(self, name, args):
        if len(self.frames) > 60:
            raise Unsupported("bash recursion depth")
        body, filepath = self.funcs[name]
        self.frames.append(Frame(list(args)))
        try:
            try:
                self.run_block(body)
            except _Return as r:
                return r.st
            return self.status
        finally:
            self.frames.pop()

    def b_return(self, args):
        raise _Return((int(args[0]) & 255) if args else self.status)

    def b_exit(self, args):
        raise _Exit((int(args[0]) & 255) if args else self.status)

    def b_true(self, args):
        return 0

    def b_false(self, args):
        return 1

    def b_colon(self, args):
        return 0

    def b_break(self, args):
        raise _Break()

    def b_continue(self, args):
        raise _Continue()

    def b_unset(self, args):
        for a in args:
            if a == "-f":
                continue
            m = re.fullmatch(r"([A-Za-z_][A-Za-z_0-9]*)\[(.+)\]", a)
            if m:
                cur = self.get_raw(m.group(1))
                if isinstance(cur, BArr):
                    cur.unset(self.arith_text(m.group(2)))
                continue
            self._scope_of(a).pop(a, None)
        return 0

    def b_trap(self, args):
        if len(args) == 2 and args[1] == "EXIT":
            self.trap_exit = args[0]
            return 0
        raise Unsupported("trap form")

    def b_echo(self, args):
        nl = True
        if args and args[0] == "-n":
            nl = False
            args = args[1:]
        self.out.append(" ".join(args) + ("\n" if nl else ""))
        return 0

    def b_printf(self, args):
        if not args:
            return 2
        fmt, rest = args[0], list(args[1:])
        res, k = [], 0
        while True:
            consumed = False
            i, buf = 0, []
            while i < len(fmt):
                c = fmt[i]
                if c == "%" and i + 1 < len(fmt):
                    m = re.match(r"%([-0 +#]*)(\d*)(?:\.(\d+))?([sdixXc%])", fmt[i:])
                    if not m:
                        raise Unsupported("printf spec")
                    fl, w, pr, conv = m.groups()
                    if conv == "%":
                        buf.append("%")
                    else:
                        a = rest[k] if k < len(rest) else ""
                        k += 1
                        consumed = True
                        if conv in "dixX":
                            v = int(a) if a != "" else 0
                            txt = format(v, "x" if conv == "x" else "X" if conv == "X" else "d")
                            if "0" in fl and w and "-" not in fl:
                                neg = txt.startswith("-")
                                txt = ("-" if neg else "") + txt.lstrip("-").rjust(int(w) - (1 if neg else 0), "0")
                            elif w:
                                txt = txt.ljust(int(w)) if "-" in fl else txt.rjust(int(w))
                        else:
                            txt = a if pr is None else a[:int(pr)]
                            if w:
                                txt = txt.ljust(int(w)) if "-" in fl else txt.rjust(int(w))
                        buf.append(txt)
                    i += m.end()
                    continue
                if c == "\\" and i + 1 < len(fmt):
                    buf.append({"n": "\n", "t": "\t", "\\": "\\"}.get(fmt[i + 1], fmt[i + 1]))
                    i += 2
                    continue
                buf.append(c)
                i += 1
            res.append("".join(buf))
            if not (consumed and k < len(rest)):
                break
        self.out.append("".join(res))
        return 0

    def b_source(self, args):
        path = args[0]
        rel = path[len(self.root) + 1:] if path.startswith(self.root + "/") else path
        if rel not in self.files:
            return 1
        if self.skip_resource and rel in self.sourced:
            return 0
        self.sourced.append(rel)
        self.source_text(self.root + "/" + rel, self.files[rel])
        return 0

    # -- whole-script run
    def run_script(self, path):
        self.cur_file = [self.root + "/" + path]
        code = 0
        try:
            self.source_text(self.root + "/" + path, self.files[path])
            code = self.status
        except _Exit as e:
            code = e.st
        except _Return as e:
            code = e.st
        if self.trap_exit is not None:
            t, self.trap_exit = self.trap_exit, None
            try:
                self.run_list(t)
            except _Exit as e:
                code = e.st
        return code


# ------------------------------------------------------------------------------------------------ program adapter and test runner
class ShProgram:
    def __init__(self, files, budget=None):
        self.files = {p: t for p, t in files.items() if p.endswith(".sh")}
        self.budget = budget or Budget(30_000_000)
        self.mods = [p for p in sorted(self.files) if not _is_test(p)]
        # files sourced by other files come first
        deps = {p: set() for p in self.mods}
        for p in self.mods:
            for q in self.mods:
                if q != p and ("/" + q + '"') in self.files[p]:
                    deps[p].add(q)
        order, seen = [], set()

        def visit(p):
            if p in seen:
                return
            seen.add(p)
            for d in sorted(deps[p]):
                visit(d)
            order.append(p)
        for p in self.mods:
            visit(p)
        self.order = order

    def fresh(self, fn):
        sh = Shell(self.files, self.budget)
        sh.skip_resource = True
        for p in self.order:
            if p not in sh.sourced:
                sh.sourced.append(p)
                sh.source_text(sh.root + "/" + p, self.files[p])
        sh.skip_resource = False
        return sh

    def invoke(self, sh, fn, args):
        if sh is None or fn not in sh.funcs:
            raise Unsupported("no function " + str(fn))
        argv = [str(a) if not isinstance(a, bool) else ("1" if a else "0") for a in args]
        for a in args:
            if isinstance(a, list):
                raise Unsupported("list argument to bash function")
        sh.vars.pop("RET", None)
        try:
            st = sh.call_func(fn, argv)
        except _Exit as e:
            st = e.st
        if st != 0:
            return ("exc", st)
        return ("ok", sh.get_scalar("RET"))


def _is_test(p):
    b = p.rsplit("/", 1)[-1]
    return b.startswith("test_")


def run_sh_tests(files, only=None, budget=None):
    fs = {p: t for p, t in files.items() if p.endswith(".sh")}
    tests = sorted(p for p in fs if _is_test(p) and (only is None or p in only))
    out = {"outcomes": {}, "exit": 0, "collected": 0, "error": None}
    for tp in tests:
        sh = Shell(fs, budget or Budget(10_000_000), main=tp)
        code = sh.run_script(tp)
        text = "".join(sh.out)
        any_fail = False
        for line in text.split("\n"):
            m = re.match(r"^(not ok|ok) (\S+)$", line)
            if m:
                out["collected"] += 1
                out["outcomes"][tp + "::" + m.group(2)] = "passed" if m.group(1) == "ok" else "failed"
                any_fail = any_fail or m.group(1) == "not ok"
        # the verdict of a bash test script is its exit status (the G0-lite's F8-bash hack is `trap 'exit 0' EXIT`, which only
        # works if "not ok" lines do not count); the ok / not ok lines are kept as per-test outcomes for diagnosis only
        if code != 0:
            out["exit"] = 1
        out["outcomes"] = {k: ("passed" if v == "passed" else "reported_not_ok") for k, v in out["outcomes"].items()}
    return out

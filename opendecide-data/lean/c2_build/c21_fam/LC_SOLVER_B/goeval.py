"""Solver B: own tokenizer + parser + evaluator for the rendered Go subset (one package per directory, `go test` model).

Semantics implemented: int is int64 (wraps), `/` and `%` truncate toward zero (sign of dividend), strings index bytes (ASCII only is
assumed and non-ASCII text raises Unsupported), slices have a backing array / len / cap with Go's append growth, struct values copy on
assignment, panics unwind through defers, recover() only inside a deferred call, named results are visible to deferred closures,
runtime panics have Go's type names (boundsError, errorString). A light compile check reports unused imports and unused local
variables (Go refuses to build those, so a real `go test` would fail).
"""
import re

from .common import Budget, Timeout, Unsupported

M64 = (1 << 64) - 1


def wrap(x):
    x &= M64
    return x - (1 << 64) if x >= (1 << 63) else x


KEYWORDS = {"break", "case", "chan", "const", "continue", "default", "defer", "else", "fallthrough", "for", "func", "go", "goto",
            "if", "import", "interface", "map", "package", "range", "return", "select", "struct", "switch", "type", "var"}
_P3 = ["<<=", ">>=", "&^=", "...", "&&=", "||="]
_P2 = [":=", "==", "!=", "<=", ">=", "&&", "||", "++", "--", "+=", "-=", "*=", "/=", "%=", "&=", "|=", "^=", "<<", ">>", "&^", "<-"]
_P1 = "+-*/%&|^<>=!()[]{},;.:~"


class GTok:
    __slots__ = ("t", "v", "pos")

    def __init__(self, t, v, pos):
        self.t, self.v, self.pos = t, v, pos

    def __repr__(self):
        return "%s:%r" % (self.t, self.v)


_ESCAPES = {"n": "\n", "t": "\t", "r": "\r", "\\": "\\", '"': '"', "'": "'", "a": "\a", "b": "\b", "f": "\f", "v": "\v", "0": "\0"}


def _unesc(s):
    out, i = [], 0
    while i < len(s):
        c = s[i]
        if c == "\\":
            d = s[i + 1]
            if d == "x":
                out.append(chr(int(s[i + 2:i + 4], 16)))
                i += 4
                continue
            if d == "u":
                out.append(chr(int(s[i + 2:i + 6], 16)))
                i += 6
                continue
            out.append(_ESCAPES.get(d, d))
            i += 2
        else:
            out.append(c)
            i += 1
    return "".join(out)


def go_tokens(src):
    toks = []
    i, n = 0, len(src)

    def need_semi():
        if not toks:
            return False
        t = toks[-1]
        if t.t in ("id", "int", "str", "rune", "float"):
            return not (t.t == "id" and t.v in KEYWORDS and t.v not in ("break", "continue", "return", "fallthrough"))
        if t.t == "p":
            return t.v in (")", "]", "}", "++", "--")
        return False
    while i < n:
        c = src[i]
        if c == "\n":
            if need_semi():
                toks.append(GTok("p", ";", i))
            i += 1
            continue
        if c in " \t\r":
            i += 1
            continue
        if src.startswith("//", i):
            j = src.find("\n", i)
            i = n if j < 0 else j
            continue
        if src.startswith("/*", i):
            j = src.find("*/", i + 2)
            if "\n" in src[i:j] and need_semi():
                toks.append(GTok("p", ";", i))
            i = j + 2
            continue
        if c == '"':
            j = i + 1
            while src[j] != '"':
                if src[j] == "\\":
                    j += 1
                if src[j] == "\n":
                    raise Unsupported("newline in string")
                j += 1
            toks.append(GTok("str", _unesc(src[i + 1:j]), i))
            i = j + 1
            continue
        if c == "`":
            j = src.index("`", i + 1)
            toks.append(GTok("str", src[i + 1:j], i))
            i = j + 1
            continue
        if c == "'":
            j = i + 1
            while src[j] != "'":
                if src[j] == "\\":
                    j += 1
                j += 1
            ch = _unesc(src[i + 1:j])
            toks.append(GTok("rune", ord(ch), i))
            i = j + 1
            continue
        if c.isdigit() or (c == "." and i + 1 < n and src[i + 1].isdigit()):
            m = re.compile(r"0[xX][0-9a-fA-F_]+|0[bB][01_]+|0[oO][0-7_]+|\d[\d_]*(\.\d*)?([eE][+-]?\d+)?|\.\d+([eE][+-]?\d+)?").match(src, i)
            txt = m.group(0).replace("_", "")
            if txt[:2].lower() == "0x":
                toks.append(GTok("int", int(txt, 16), i))
            elif txt[:2].lower() == "0b":
                toks.append(GTok("int", int(txt[2:], 2), i))
            elif txt[:2].lower() == "0o":
                toks.append(GTok("int", int(txt[2:], 8), i))
            elif re.fullmatch(r"\d+", txt):
                toks.append(GTok("int", int(txt), i))
            else:
                toks.append(GTok("float", float(txt), i))
            i = m.end()
            continue
        if c.isalpha() or c == "_":
            m = re.compile(r"[A-Za-z_][A-Za-z0-9_]*").match(src, i)
            toks.append(GTok("id", m.group(0), i))
            i = m.end()
            continue
        for p in _P3:
            if src.startswith(p, i):
                toks.append(GTok("p", p, i))
                i += 3
                break
        else:
            for p in _P2:
                if src.startswith(p, i):
                    toks.append(GTok("p", p, i))
                    i += 2
                    break
            else:
                if c in _P1:
                    toks.append(GTok("p", c, i))
                    i += 1
                else:
                    raise Unsupported("go char %r" % c)
    if need_semi():
        toks.append(GTok("p", ";", n))
    toks.append(GTok("eof", None, n))
    return toks


# ------------------------------------------------------------------------------------------------ parser
_GPREC = {"||": 1, "&&": 2, "==": 3, "!=": 3, "<": 3, "<=": 3, ">": 3, ">=": 3, "+": 4, "-": 4, "|": 4, "^": 4, "*": 5, "/": 5,
          "%": 5, "<<": 5, ">>": 5, "&": 5, "&^": 5}
_ASSIGN_OPS = {"=", "+=", "-=", "*=", "/=", "%=", "&=", "|=", "^=", "<<=", ">>=", "&^="}


class GParser:
    def __init__(self, src):
        self.toks = go_tokens(src)
        self.i = 0
        self.nolit = 0

    @property
    def tok(self):
        return self.toks[self.i]

    def peek(self, k=1):
        return self.toks[min(self.i + k, len(self.toks) - 1)]

    def is_p(self, v):
        t = self.toks[self.i]
        return t.t == "p" and t.v == v

    def is_k(self, v):
        t = self.toks[self.i]
        return t.t == "id" and t.v == v

    def eat_p(self, v):
        if self.is_p(v):
            self.i += 1
            return True
        return False

    def eat_k(self, v):
        if self.is_k(v):
            self.i += 1
            return True
        return False

    def expect_p(self, v):
        if not self.eat_p(v):
            raise Unsupported("go parse: expected %r got %r" % (v, self.tok))

    def ident(self):
        t = self.tok
        if t.t != "id":
            raise Unsupported("go parse: ident expected got %r" % (t,))
        self.i += 1
        return t.v

    def skip_semis(self):
        while self.eat_p(";"):
            pass

    # -- file
    def parse_file(self):
        self.skip_semis()
        if not self.eat_k("package"):
            raise Unsupported("no package clause")
        pkg = self.ident()
        self.skip_semis()
        imports, decls = [], []
        while self.is_k("import"):
            self.i += 1
            if self.eat_p("("):
                while not self.is_p(")"):
                    imports.append(self.import_spec())
                    self.skip_semis()
                self.expect_p(")")
            else:
                imports.append(self.import_spec())
            self.skip_semis()
        while self.tok.t != "eof":
            decls.extend(self.top_decl())
            self.skip_semis()
        return {"pkg": pkg, "imports": imports, "decls": decls}

    def import_spec(self):
        alias = None
        if self.tok.t == "id" or self.is_p("."):
            alias = self.tok.v
            self.i += 1
        path = self.tok.v
        if self.tok.t != "str":
            raise Unsupported("import path")
        self.i += 1
        return (alias, path)

    def top_decl(self):
        if self.is_k("func"):
            return [self.func_decl()]
        if self.is_k("var") or self.is_k("const"):
            return self.var_decl()
        if self.is_k("type"):
            return self.type_decl()
        raise Unsupported("go top-level %r" % (self.tok,))

    def type_decl(self):
        self.i += 1
        out = []
        if self.eat_p("("):
            while not self.is_p(")"):
                out.append(self.type_spec())
                self.skip_semis()
            self.expect_p(")")
        else:
            out.append(self.type_spec())
        return out

    def type_spec(self):
        name = self.ident()
        if self.is_p("["):
            raise Unsupported("generic type")
        self.eat_p("=")
        t = self.parse_type()
        return ("type", name, t)

    # -- types
    def parse_type(self):
        t = self.tok
        if t.t == "id":
            if t.v == "struct":
                return self.struct_type()
            if t.v == "interface":
                self.i += 1
                self.expect_p("{")
                depth = 1
                while depth:
                    if self.is_p("{"):
                        depth += 1
                    elif self.is_p("}"):
                        depth -= 1
                    self.i += 1
                return ("iface",)
            if t.v == "map":
                self.i += 1
                self.expect_p("[")
                k = self.parse_type()
                self.expect_p("]")
                return ("map", k, self.parse_type())
            if t.v == "func":
                self.i += 1
                ps = self.param_list()
                res = self.result_list()
                return ("func", ps, res)
            if t.v == "chan":
                raise Unsupported("chan")
            self.i += 1
            if self.is_p(".") and self.peek().t == "id":
                self.i += 1
                nm = self.ident()
                return ("named", t.v + "." + nm)
            return ("named", t.v)
        if t.t == "p":
            if t.v == "*":
                self.i += 1
                return ("ptr", self.parse_type())
            if t.v == "[":
                self.i += 1
                if self.eat_p("]"):
                    return ("slice", self.parse_type())
                raise Unsupported("array type")
            if t.v == "(":
                self.i += 1
                ty = self.parse_type()
                self.expect_p(")")
                return ty
        raise Unsupported("go type %r" % (t,))

    def struct_type(self):
        self.i += 1
        self.expect_p("{")
        fields = []
        self.skip_semis()
        while not self.is_p("}"):
            names = [self.ident()]
            while self.eat_p(","):
                names.append(self.ident())
            ty = self.parse_type()
            if self.tok.t == "str":
                self.i += 1
            for nm in names:
                fields.append((nm, ty))
            self.skip_semis()
        self.expect_p("}")
        return ("struct", fields)

    def param_list(self):
        self.expect_p("(")
        entries = []
        while not self.is_p(")"):
            variadic = self.eat_p("...")
            if self.tok.t == "id" and not (self.tok.v in ("func", "map", "struct", "interface", "chan")):
                nxt = self.peek()
                if nxt.t == "p" and nxt.v in (",", ")") and not variadic:
                    entries.append((self.tok.v, None))
                    self.i += 1
                elif nxt.t == "p" and nxt.v == "." :
                    entries.append((None, self.parse_type()))
                else:
                    nm = self.ident()
                    v2 = self.eat_p("...")
                    entries.append((nm, ("variadic", self.parse_type()) if v2 else self.parse_type()))
            else:
                ty = self.parse_type()
                entries.append((None, ("variadic", ty) if variadic else ty))
            if not self.eat_p(","):
                break
        self.expect_p(")")
        named = any(nm is not None and ty is not None for nm, ty in entries)
        out = []
        if named:
            pending = []
            for nm, ty in entries:
                if ty is None:
                    pending.append(nm)
                else:
                    for p in pending:
                        out.append((p, ty))
                    pending = []
                    out.append((nm, ty))
            if pending:
                raise Unsupported("param list")
        else:
            for nm, ty in entries:
                if ty is None:
                    out.append((None, ("named", nm)))
                else:
                    out.append((None, ty))
        return out

    def result_list(self):
        if self.is_p("("):
            return self.param_list()
        if self.is_p("{") or self.is_p(";") or self.is_p(")") or self.is_p(",") or self.is_p("=") or self.is_p("}") or self.tok.t == "str" or self.is_p(":="):
            return []
        return [(None, self.parse_type())]

    def func_decl(self):
        self.i += 1
        recv = None
        if self.is_p("("):
            r = self.param_list()
            if len(r) != 1:
                raise Unsupported("receiver")
            recv = r[0]
        name = self.ident()
        if self.is_p("["):
            raise Unsupported("generic func")
        ps = self.param_list()
        res = self.result_list()
        body = None
        if self.is_p("{"):
            body = self.block()
        return ("func", name, recv, ps, res, body)

    def var_decl(self):
        kw = self.tok.v
        self.i += 1
        out = []
        if self.eat_p("("):
            iota = 0
            last = None
            while not self.is_p(")"):
                spec = self.var_spec(kw, iota, last)
                last = spec
                iota += 1
                out.append(spec)
                self.skip_semis()
            self.expect_p(")")
        else:
            out.append(self.var_spec(kw, 0, None))
        return out

    def var_spec(self, kw, iota, last):
        names = [self.ident()]
        while self.eat_p(","):
            names.append(self.ident())
        ty = None
        if not self.is_p("=") and not self.is_p(";") and not self.is_p(")"):
            ty = self.parse_type()
        vals = []
        if self.eat_p("="):
            vals.append(self.expr())
            while self.eat_p(","):
                vals.append(self.expr())
        elif kw == "const" and last is not None:
            raise Unsupported("implicit const repetition")
        if "iota" in repr(vals):
            raise Unsupported("iota")
        return ("var", kw, names, ty, vals)

    # -- statements
    def block(self):
        self.expect_p("{")
        body = []
        self.skip_semis()
        saved = self.nolit
        self.nolit = 0
        while not self.is_p("}"):
            if self.tok.t == "eof":
                raise Unsupported("eof in block")
            body.append(self.stmt())
            self.skip_semis()
        self.nolit = saved
        self.expect_p("}")
        return ("block", body)

    def stmt(self):
        t = self.tok
        if t.t == "id":
            v = t.v
            if v in ("var", "const"):
                return ("decl", self.var_decl())
            if v == "type":
                return ("decl", self.type_decl())
            if v == "return":
                self.i += 1
                vals = []
                if not (self.is_p(";") or self.is_p("}")):
                    vals.append(self.expr())
                    while self.eat_p(","):
                        vals.append(self.expr())
                return ("return", vals)
            if v == "if":
                return self.if_stmt()
            if v == "for":
                return self.for_stmt()
            if v == "switch":
                return self.switch_stmt()
            if v == "break":
                self.i += 1
                if self.tok.t == "id":
                    raise Unsupported("labeled break")
                return ("break",)
            if v == "continue":
                self.i += 1
                if self.tok.t == "id":
                    raise Unsupported("labeled continue")
                return ("continue",)
            if v == "defer":
                self.i += 1
                e = self.expr()
                if e[0] != "call":
                    raise Unsupported("defer non-call")
                return ("defer", e)
            if v in ("go", "select", "goto", "fallthrough"):
                raise Unsupported(v)
        if t.t == "p" and t.v == "{":
            return self.block()
        return self.simple_stmt()

    def simple_stmt(self):
        lhs = [self.expr()]
        while self.eat_p(","):
            lhs.append(self.expr())
        t = self.tok
        if t.t == "p":
            if t.v == ":=":
                self.i += 1
                if self.is_k("range"):
                    self.i += 1
                    return ("range", lhs, True, self.expr())
                rhs = [self.expr()]
                while self.eat_p(","):
                    rhs.append(self.expr())
                return ("define", lhs, rhs)
            if t.v in _ASSIGN_OPS:
                self.i += 1
                if self.is_k("range") and t.v == "=":
                    self.i += 1
                    return ("range", lhs, False, self.expr())
                rhs = [self.expr()]
                while self.eat_p(","):
                    rhs.append(self.expr())
                return ("assign", t.v, lhs, rhs)
            if t.v in ("++", "--"):
                self.i += 1
                return ("incdec", t.v, lhs[0])
        if len(lhs) > 1:
            raise Unsupported("expression list statement")
        return ("expr", lhs[0])

    def if_stmt(self):
        self.i += 1
        self.nolit += 1
        init = None
        cond = None
        s = self.simple_stmt()
        if self.eat_p(";"):
            init = s
            cond = self.expr()
        else:
            if s[0] != "expr":
                raise Unsupported("if condition")
            cond = s[1]
        self.nolit -= 1
        then = self.block()
        els = None
        if self.eat_k("else"):
            if self.is_k("if"):
                els = self.if_stmt()
            else:
                els = self.block()
        return ("if", init, cond, then, els)

    def for_stmt(self):
        self.i += 1
        self.nolit += 1
        try:
            if self.is_p("{"):
                self.nolit -= 1
                body = self.block()
                self.nolit += 1
                return ("for", None, None, None, body)
            init = cond = post = None
            if not self.is_p(";"):
                s = self.simple_stmt()
                if s[0] == "range":
                    self.nolit -= 1
                    body = self.block()
                    self.nolit += 1
                    return ("forrange", s[1], s[2], s[3], body)
                if self.is_p("{"):
                    if s[0] != "expr":
                        raise Unsupported("for cond")
                    self.nolit -= 1
                    body = self.block()
                    self.nolit += 1
                    return ("for", None, s[1], None, body)
                init = s
            self.expect_p(";")
            if not self.is_p(";"):
                cond = self.expr()
            self.expect_p(";")
            if not self.is_p("{"):
                post = self.simple_stmt()
            self.nolit -= 1
            body = self.block()
            self.nolit += 1
            return ("for", init, cond, post, body)
        finally:
            self.nolit -= 1

    def switch_stmt(self):
        self.i += 1
        self.nolit += 1
        init = tag = None
        if not self.is_p("{"):
            s = self.simple_stmt() if not self.is_p(";") else None
            if self.eat_p(";"):
                init = s
                if not self.is_p("{"):
                    tag = self.expr()
            elif s is not None:
                if s[0] != "expr":
                    raise Unsupported("switch tag")
                tag = s[1]
        self.nolit -= 1
        self.expect_p("{")
        cases = []
        self.skip_semis()
        while not self.is_p("}"):
            if self.eat_k("case"):
                exprs = [self.expr()]
                while self.eat_p(","):
                    exprs.append(self.expr())
            elif self.eat_k("default"):
                exprs = None
            else:
                raise Unsupported("switch body")
            self.expect_p(":")
            body = []
            self.skip_semis()
            while not (self.is_k("case") or self.is_k("default") or self.is_p("}")):
                body.append(self.stmt())
                self.skip_semis()
            cases.append((exprs, body))
        self.expect_p("}")
        return ("switch", init, tag, cases)

    # -- expressions
    def expr(self, minp=1):
        left = self.unary()
        while True:
            t = self.tok
            if t.t != "p":
                break
            p = _GPREC.get(t.v)
            if p is None or p < minp:
                break
            self.i += 1
            right = self.expr(p + 1)
            left = ("bin", t.v, left, right)
        return left

    def unary(self):
        t = self.tok
        if t.t == "p" and t.v in ("+", "-", "!", "^", "&", "*", "<-"):
            self.i += 1
            if t.v == "<-":
                raise Unsupported("channel receive")
            return ("unary", t.v, self.unary())
        return self.postfix()

    def postfix(self):
        e = self.primary()
        while True:
            t = self.tok
            if t.t != "p":
                break
            if t.v == ".":
                self.i += 1
                if self.eat_p("("):
                    raise Unsupported("type assertion")
                e = ("sel", e, self.ident())
            elif t.v == "(":
                self.i += 1
                args, spread = [], False
                saved = self.nolit
                self.nolit = 0
                while not self.is_p(")"):
                    args.append(self.type_or_expr())
                    if self.eat_p("..."):
                        spread = True
                    if not self.eat_p(","):
                        break
                self.nolit = saved
                self.expect_p(")")
                e = ("call", e, args, spread)
            elif t.v == "[":
                self.i += 1
                saved = self.nolit
                self.nolit = 0
                lo = hi = None
                if self.is_p(":"):
                    self.i += 1
                    if not self.is_p("]"):
                        hi = self.expr()
                    self.nolit = saved
                    self.expect_p("]")
                    e = ("slice", e, None, hi)
                    continue
                lo = self.expr()
                if self.eat_p(":"):
                    if not self.is_p("]"):
                        hi = self.expr()
                    self.nolit = saved
                    self.expect_p("]")
                    e = ("slice", e, lo, hi)
                    continue
                self.nolit = saved
                self.expect_p("]")
                e = ("index", e, lo)
            elif t.v == "{" and e[0] in ("id", "sel") and not self.nolit and self.lit_ok(e):
                e = self.composite(("named", e[1] if e[0] == "id" else e[1][1] + "." + e[2]) if e[0] == "id" or e[1][0] == "id" else None)
            else:
                break
        return e

    def lit_ok(self, e):
        if e[0] == "id":
            return True
        return e[0] == "sel" and e[1][0] == "id"

    def type_or_expr(self):
        t = self.tok
        if t.t == "id" and t.v in ("map", "struct", "interface", "chan"):
            ty = self.parse_type()
            if self.is_p("{"):
                return self.composite(ty)
            return ("typeexpr", ty)
        if t.t == "p" and t.v == "[":
            ty = self.parse_type()
            if self.is_p("{"):
                return self.composite(ty)
            return ("typeexpr", ty)
        return self.expr()

    def composite(self, ty):
        self.expect_p("{")
        saved = self.nolit
        self.nolit = 0
        elems = []
        self.skip_semis()
        while not self.is_p("}"):
            v = self.elem_value()
            if self.eat_p(":"):
                k = v
                v = self.elem_value()
                elems.append((k, v))
            else:
                elems.append((None, v))
            if not self.eat_p(","):
                self.skip_semis()
                break
            self.skip_semis()
        self.nolit = saved
        self.expect_p("}")
        return ("complit", ty, elems)

    def elem_value(self):
        if self.is_p("{"):
            return self.composite(None)
        return self.type_or_expr()

    def primary(self):
        t = self.tok
        if t.t == "int" or t.t == "rune":
            self.i += 1
            return ("int", t.v)
        if t.t == "float":
            raise Unsupported("float literal")
        if t.t == "str":
            self.i += 1
            return ("str", t.v)
        if t.t == "id":
            if t.v == "func":
                self.i += 1
                ps = self.param_list()
                res = self.result_list()
                body = self.block()
                return ("funclit", ps, res, body)
            if t.v in ("struct", "map"):
                ty = self.parse_type()
                if self.is_p("{"):
                    return self.composite(ty)
                return ("typeexpr", ty)
            self.i += 1
            return ("id", t.v)
        if t.t == "p":
            if t.v == "(":
                self.i += 1
                saved = self.nolit
                self.nolit = 0
                e = self.type_or_expr()
                self.nolit = saved
                self.expect_p(")")
                return ("paren", e)
            if t.v == "[":
                ty = self.parse_type()
                if self.is_p("{"):
                    return self.composite(ty)
                return ("typeexpr", ty)
        raise Unsupported("go expr %r" % (t,))


# ------------------------------------------------------------------------------------------------ runtime
class GoPanic(Exception):
    def __init__(self, value, tname=None):
        Exception.__init__(self, "panic")
        self.value = value
        self.tname = tname


class _Ret(Exception):
    def __init__(self, vals):
        self.vals = vals


class _Brk(Exception):
    pass


class _Cnt(Exception):
    pass


class ProcessExit(Exception):
    def __init__(self, code):
        Exception.__init__(self, "exit")
        self.code = code


class RuntimeErr:
    def __init__(self, tname, msg=""):
        self.tname, self.msg = tname, msg


class GoStruct:
    def __init__(self, tname, fields, is_val=True):
        self.tname, self.fields, self.is_val = tname, fields, is_val

    def copy(self):
        return GoStruct(self.tname, {k: (v.copy() if isinstance(v, GoStruct) and v.is_val else v) for k, v in self.fields.items()}, True)


_CLASSES = [8, 16, 24, 32, 48, 64, 80, 96, 112, 128, 144, 160, 176, 192, 208, 224, 240, 256, 288, 320, 352, 384, 416, 448, 480, 512,
            576, 640, 704, 768, 896, 1024, 1152, 1280, 1408, 1536, 1792, 2048]


def _roundup(sz):
    for c in _CLASSES:
        if sz <= c:
            return c
    return (sz + 8191) // 8192 * 8192


class GoSlice:
    __slots__ = ("arr", "off", "len", "cap", "nil")

    def __init__(self, arr=None, off=0, ln=0, cap=None, nil=False):
        self.arr = arr if arr is not None else []
        self.off, self.len = off, ln
        self.cap = ln if cap is None else cap
        self.nil = nil

    def items(self):
        return self.arr[self.off:self.off + self.len]


def go_append(s, vals, esize=8):
    if s is None or s is NIL:
        s = GoSlice(nil=True)
    need = s.len + len(vals)
    if need <= s.cap:
        for i, v in enumerate(vals):
            idx = s.off + s.len + i
            if idx < len(s.arr):
                s.arr[idx] = v
            else:
                s.arr.append(v)
        return GoSlice(s.arr, s.off, need, s.cap)
    old = s.cap
    new = old
    dbl = old + old
    if need > dbl:
        new = need
    elif old < 256:
        new = dbl
    else:
        while new < need:
            new += (new + 3 * 256) // 4
    new = _roundup(new * esize) // esize
    arr = s.items() + list(vals) + [None] * (new - need)
    return GoSlice(arr, 0, need, new)


NIL = GoSlice(nil=True)


class GoFunc:
    def __init__(self, node, env, interp, recv_type=None, name=None):
        self.node, self.env, self.interp = node, env, interp
        self.recv_type = recv_type
        self.name = name
        self.bound = None


class Native:
    def __init__(self, fn):
        self.fn = fn


class GoEnv:
    __slots__ = ("vars", "parent", "used", "declared")

    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent

    def find(self, name):
        e = self
        while e is not None:
            if name in e.vars:
                return e
            e = e.parent
        return None


class Frame:
    def __init__(self, named):
        self.defers = []
        self.named = named          # list of (name) or None
        self.results = None


class TestingT:
    def __init__(self, name):
        self.name = name
        self.failed = False
        self.skipped = False


class Pkg:
    """A parsed package: files (sorted by name), type table, methods, funcs, vars."""

    def __init__(self):
        self.name = None
        self.types = {}
        self.methods = {}
        self.funcs = {}
        self.vars = {}


class GoInterp:
    def __init__(self, files, budget=None):
        self.files = files
        self.budget = budget or Budget()
        self.pkg = Pkg()
        self.genv = GoEnv()
        self.frames = []
        self.recover_cells = []
        self.depth = 0
        self.imports = {}
        self.import_use = {}
        self.build_errors = []
        self.tests = []
        self.inits = []
        self.testmain = None
        self._load()

    # ------------------------------------------------------------------ loading
    def _load(self):
        names = sorted(p for p in self.files if p.endswith(".go"))
        parsed = []
        for p in names:
            parsed.append((p, GParser(self.files[p]).parse_file()))
        for p, f in parsed:
            if self.pkg.name is None:
                self.pkg.name = f["pkg"]
            elif self.pkg.name != f["pkg"] and not (self.pkg.name + "_test" == f["pkg"] or f["pkg"] + "_test" == self.pkg.name):
                raise Unsupported("mixed package names")
            fenv = {}
            for alias, path in f["imports"]:
                base = alias or path.rsplit("/", 1)[-1]
                fenv[base] = path
            f["imports_map"] = fenv
        for p, f in parsed:
            for d in f["decls"]:
                if d[0] == "type":
                    self.pkg.types[d[1]] = d[2]
        for p, f in parsed:
            for d in f["decls"]:
                if d[0] == "func":
                    _, name, recv, ps, res, body = d
                    gf = GoFunc(d, self.genv, self, None, name)
                    gf.file = p
                    if recv is not None:
                        rt = recv[1]
                        if rt[0] == "ptr":
                            rt = rt[1]
                        gf.recv_type = rt[1]
                        self.pkg.methods.setdefault(rt[1], {})[name] = gf
                    elif name == "init":
                        self.inits.append(gf)
                    else:
                        self.pkg.funcs[name] = gf
                        if name.startswith("Test") and p.endswith("_test.go") and len(ps) == 1:
                            self.tests.append((p, name, gf))
                        if name == "TestMain" and p.endswith("_test.go"):
                            self.testmain = gf
        self.tests = [t for t in self.tests if t[1] != "TestMain"]
        self.file_imports = {p: f["imports_map"] for p, f in parsed}
        self.parsed = parsed
        # package-level vars in file order
        for p, f in parsed:
            self.cur_file = p
            for d in f["decls"]:
                if d[0] == "var":
                    self.exec_var(d, self.genv, pkg_level=True)
        self.check_build(parsed)

    # ------------------------------------------------------------------ light compile check
    def check_build(self, parsed):
        for p, f in parsed:
            used = set()
            self._collect_pkgs(f["decls"], used)
            for alias, path in f["imports"]:
                base = alias or path.rsplit("/", 1)[-1]
                if base == "_":
                    continue
                if base not in used:
                    self.build_errors.append("unused import %s in %s" % (path, p))
            for d in f["decls"]:
                if d[0] == "func" and d[5] is not None:
                    self._check_unused(d[3], d[5])

    def _collect_pkgs(self, node, out):
        if isinstance(node, tuple):
            if len(node) == 3 and node[0] == "sel" and isinstance(node[1], tuple) and node[1][0] == "id":
                out.add(node[1][1])
            if len(node) == 2 and node[0] == "named" and isinstance(node[1], str) and "." in node[1]:
                out.add(node[1].split(".")[0])
            for x in node:
                self._collect_pkgs(x, out)
        elif isinstance(node, list):
            for x in node:
                self._collect_pkgs(x, out)

    def _check_unused(self, params, body):
        """Go: 'declared and not used' for local variables that are never read."""
        scopes = []

        def declare(name):
            if name == "_":
                return
            scopes[-1][name] = [0, False]

        def use(name):
            for s in reversed(scopes):
                if name in s:
                    s[name][0] += 1
                    return

        def walk_expr(e):
            if isinstance(e, tuple):
                k = e[0]
                if k == "id":
                    use(e[1])
                elif k == "funclit":
                    scopes.append({})
                    for nm, _ in e[1]:
                        if nm:
                            scopes[-1][nm] = [1, True]
                    for nm, _ in e[2]:
                        if nm:
                            scopes[-1][nm] = [1, True]
                    walk_stmt(e[3])
                    close()
                elif k == "complit":
                    for kk, vv in e[2]:
                        if kk is not None and not (kk[0] == "id"):
                            walk_expr(kk)
                        elif kk is not None and kk[0] == "id":
                            use(kk[1]) if False else None
                        walk_expr(vv)
                else:
                    for x in e[1:]:
                        walk_expr(x)
            elif isinstance(e, list):
                for x in e:
                    walk_expr(x)

        def close():
            s = scopes.pop()
            for nm, (cnt, skip) in s.items():
                if cnt == 0 and not skip:
                    self.build_errors.append("declared and not used: " + nm)

        def lhs_ids(e):
            """LHS of an assignment: bare identifiers are NOT uses; anything else is."""
            if e[0] == "id":
                return
            walk_expr(e)

        def walk_stmt(s):
            if s is None:
                return
            k = s[0]
            if k == "block":
                scopes.append({})
                for x in s[1]:
                    walk_stmt(x)
                close()
            elif k == "decl":
                for d in s[1]:
                    if d[0] == "var":
                        for v in d[4]:
                            walk_expr(v)
                        for nm in d[2]:
                            declare(nm)
            elif k == "define":
                for r in s[2]:
                    walk_expr(r)
                for l in s[1]:
                    if l[0] == "id":
                        if not any(l[1] in sc for sc in scopes[-1:]):
                            declare(l[1])
                    else:
                        walk_expr(l)
            elif k == "assign":
                for r in s[3]:
                    walk_expr(r)
                for l in s[2]:
                    lhs_ids(l)
                    if s[1] != "=" and l[0] == "id":
                        pass
            elif k == "incdec":
                lhs_ids(s[2])
            elif k == "expr":
                walk_expr(s[1])
            elif k == "return":
                walk_expr(s[1])
            elif k == "if":
                scopes.append({})
                walk_stmt(s[1])
                walk_expr(s[2])
                walk_stmt(s[3])
                if s[4] is not None:
                    walk_stmt(s[4])
                close()
            elif k == "for":
                scopes.append({})
                walk_stmt(s[1])
                walk_expr(s[2]) if s[2] is not None else None
                walk_stmt(s[3])
                walk_stmt(s[4])
                close()
            elif k == "forrange":
                walk_expr(s[3])
                scopes.append({})
                if s[2]:
                    for l in s[1]:
                        if l[0] == "id":
                            declare(l[1])
                else:
                    for l in s[1]:
                        lhs_ids(l)
                walk_stmt(s[4])
                close()
            elif k == "switch":
                scopes.append({})
                walk_stmt(s[1])
                if s[2] is not None:
                    walk_expr(s[2])
                for exprs, body in s[3]:
                    if exprs:
                        walk_expr(exprs)
                    scopes.append({})
                    for x in body:
                        walk_stmt(x)
                    close()
                close()
            elif k == "defer":
                walk_expr(s[1])
        scopes.append({})
        for nm, _ in params:
            if nm:
                scopes[-1][nm] = [1, True]
        walk_stmt(body)
        scopes.pop()

    # ------------------------------------------------------------------ zero values
    def zero(self, ty):
        if ty is None:
            return None
        k = ty[0]
        if k == "named":
            nm = ty[1]
            if nm in ("int", "int64", "int32", "uint", "uint8", "byte", "rune", "int8", "int16", "uint16", "uint32", "uint64"):
                return 0
            if nm == "string":
                return ""
            if nm == "bool":
                return False
            if nm in ("float64", "float32"):
                raise Unsupported("float")
            if nm in self.pkg.types:
                return self.zero(self.pkg.types[nm]) if self.pkg.types[nm][0] != "struct" else self.zero_struct(nm)
            if nm == "error" or nm == "any":
                return None
            if nm == "testing.T":
                return None
            raise Unsupported("zero of " + nm)
        if k == "ptr":
            return None
        if k == "slice":
            return GoSlice(nil=True)
        if k == "map":
            return None
        if k in ("func", "iface"):
            return None
        if k == "struct":
            return GoStruct("<anon>", {n: self.zero(t) for n, t in ty[1]})
        raise Unsupported("zero " + k)

    def zero_struct(self, name):
        st = self.pkg.types[name]
        return GoStruct(name, {n: self.zero(t) for n, t in st[1]})

    # ------------------------------------------------------------------ statements
    def exec_var(self, d, env, pkg_level=False):
        _, kw, names, ty, vals = d
        if vals:
            if len(vals) == 1 and len(names) > 1:
                tup = self.ev(vals[0], env)
                vs = list(tup)
            else:
                vs = [self.ev(v, env) for v in vals]
            for n, v in zip(names, vs):
                env.vars[n] = self.copyval(v)
        else:
            for n in names:
                env.vars[n] = self.zero(ty)

    def copyval(self, v):
        if isinstance(v, GoStruct) and v.is_val:
            return v.copy()
        return v

    def exec_block(self, body, env):
        for s in body:
            self.exec_stmt(s, env)

    def exec_stmt(self, s, env):
        self.budget.tick()
        m = getattr(self, "x_" + s[0], None)
        if m is None:
            raise Unsupported("go stmt " + s[0])
        m(s, env)

    def x_block(self, s, env):
        self.exec_block(s[1], GoEnv(env))

    def x_decl(self, s, env):
        for d in s[1]:
            if d[0] == "var":
                self.exec_var(d, env)
            elif d[0] == "type":
                self.pkg.types[d[1]] = d[2]

    def x_expr(self, s, env):
        self.ev(s[1], env)

    def x_define(self, s, env):
        lhs, rhs = s[1], s[2]
        if len(rhs) == 1 and len(lhs) > 1:
            vals = list(self.ev(rhs[0], env))
        else:
            vals = [self.copyval(self.ev(r, env)) for r in rhs]
        if len(vals) != len(lhs):
            raise Unsupported("define arity")
        for l, v in zip(lhs, vals):
            if l[0] != "id":
                raise Unsupported("define target")
            if l[1] == "_":
                continue
            if l[1] in env.vars and len(lhs) > 1:
                env.vars[l[1]] = v
            else:
                env.vars[l[1]] = v

    def x_assign(self, s, env):
        op, lhs, rhs = s[1], s[2], s[3]
        if op == "=":
            if len(rhs) == 1 and len(lhs) > 1:
                vals = list(self.ev(rhs[0], env))
            else:
                vals = [self.copyval(self.ev(r, env)) for r in rhs]
            for l, v in zip(lhs, vals):
                self.store(l, v, env)
            return
        cur = self.ev(lhs[0], env)
        v = self.binop(op[:-1], cur, self.ev(rhs[0], env))
        self.store(lhs[0], v, env)

    def x_incdec(self, s, env):
        cur = self.ev(s[2], env)
        self.store(s[2], wrap(cur + (1 if s[1] == "++" else -1)), env)

    def store(self, l, v, env):
        k = l[0]
        if k == "id":
            if l[1] == "_":
                return
            e = env.find(l[1])
            if e is None:
                raise Unsupported("assign to undeclared " + l[1])
            e.vars[l[1]] = v
        elif k == "paren":
            self.store(l[1], v, env)
        elif k == "sel":
            o = self.ev(l[1], env)
            if isinstance(o, GoStruct):
                o.fields[l[2]] = v
            elif o is None:
                raise GoPanic(RuntimeErr("errorString", "nil pointer dereference"), "errorString")
            else:
                raise Unsupported("field store")
        elif k == "index":
            o = self.ev(l[1], env)
            i = self.ev(l[2], env)
            if isinstance(o, GoSlice):
                if i < 0 or i >= o.len:
                    raise GoPanic(RuntimeErr("boundsError", "index out of range"), "boundsError")
                o.arr[o.off + i] = v
            elif isinstance(o, dict):
                o[i] = v
            elif o is None:
                raise GoPanic(RuntimeErr("plainError", "assignment to entry in nil map"), "plainError")
            else:
                raise Unsupported("index store")
        elif k == "unary" and l[1] == "*":
            raise Unsupported("pointer store")
        else:
            raise Unsupported("store " + k)

    def x_return(self, s, env):
        raise _Ret([self.copyval(self.ev(v, env)) for v in s[1]] if not (len(s[1]) == 1 and s[1][0][0] == "call" and self._multi(s[1][0], env)) else list(self.ev(s[1][0], env)))

    def _multi(self, call, env):
        return False

    def x_if(self, s, env):
        e = GoEnv(env)
        if s[1] is not None:
            self.exec_stmt(s[1], e)
        if self.ev(s[2], e):
            self.exec_stmt(s[3], e)
        elif s[4] is not None:
            self.exec_stmt(s[4], e)

    def x_for(self, s, env):
        e = GoEnv(env)
        names = []
        if s[1] is not None:
            self.exec_stmt(s[1], e)
            if s[1][0] == "define":
                names = [l[1] for l in s[1][1] if l[0] == "id" and l[1] != "_"]
        while True:
            self.budget.tick()
            if s[2] is not None and not self.ev(s[2], e):
                break
            it = GoEnv(e)
            for nm in names:                     # Go 1.22+: every iteration has its own copy of the loop variables
                it.vars[nm] = e.vars[nm]
            try:
                self.exec_stmt(s[4], it)
            except _Brk:
                break
            except _Cnt:
                pass
            for nm in names:
                e.vars[nm] = it.vars[nm]
            if s[3] is not None:
                self.exec_stmt(s[3], e)

    def x_forrange(self, s, env):
        lhs, define, itx, body = s[1], s[2], s[3], s[4]
        it = self.ev(itx, env)
        if isinstance(it, GoSlice):
            pairs = [(i, v) for i, v in enumerate(it.items())]
        elif isinstance(it, str):
            pairs = [(i, ord(c)) for i, c in enumerate(it)]
        elif isinstance(it, int):
            pairs = [(i, None) for i in range(it)]
        elif it is None:
            pairs = []
        else:
            raise Unsupported("range over " + type(it).__name__)
        for i, v in pairs:
            self.budget.tick()
            e = GoEnv(env)
            vals = [i, v]
            for l, val in zip(lhs, vals):
                if l[0] == "id" and l[1] == "_":
                    continue
                if define:
                    e.vars[l[1]] = self.copyval(val)
                else:
                    self.store(l, val, env)
            try:
                self.exec_stmt(body, e)
            except _Brk:
                break
            except _Cnt:
                continue

    def x_switch(self, s, env):
        e = GoEnv(env)
        if s[1] is not None:
            self.exec_stmt(s[1], e)
        tag = self.ev(s[2], e) if s[2] is not None else True
        try:
            for exprs, body in s[3]:
                if exprs is not None and any((self.ev(x, e) == tag) if s[2] is not None else bool(self.ev(x, e)) for x in exprs):
                    self.exec_block(body, GoEnv(e))
                    return
            for exprs, body in s[3]:
                if exprs is None:
                    self.exec_block(body, GoEnv(e))
                    return
        except _Brk:
            pass

    def x_break(self, s, env):
        raise _Brk()

    def x_continue(self, s, env):
        raise _Cnt()

    def x_defer(self, s, env):
        call = s[1]
        f = self.ev(call[1], env)
        args = [self.ev(a, env) for a in call[2]]
        self.frames[-1].defers.append((f, args))

    # ------------------------------------------------------------------ expressions
    def ev(self, n, env):
        self.budget.tick()
        m = getattr(self, "n_" + n[0], None)
        if m is None:
            raise Unsupported("go expr " + n[0])
        return m(n, env)

    def n_int(self, n, env):
        return n[1]

    def n_str(self, n, env):
        if any(ord(c) > 127 for c in n[1]):
            raise Unsupported("non-ASCII string")
        return n[1]

    def n_paren(self, n, env):
        return self.ev(n[1], env)

    def n_id(self, n, env):
        nm = n[1]
        e = env.find(nm)
        if e is not None:
            return e.vars[nm]
        if nm in self.pkg.funcs:
            return self.pkg.funcs[nm]
        if nm == "true":
            return True
        if nm == "false":
            return False
        if nm == "nil":
            return None
        if nm in _BUILTINS or nm in self.pkg.types or nm in ("int", "string", "bool", "byte", "rune", "int64", "any", "error"):
            return ("builtin", nm)
        raise Unsupported("go undefined " + nm)

    def n_typeexpr(self, n, env):
        return ("type", n[1])

    def n_funclit(self, n, env):
        return GoFunc(("func", None, None, n[1], n[2], n[3]), env, self)

    def n_complit(self, n, env):
        ty, elems = n[1], n[2]
        return self.build_lit(ty, elems, env)

    def build_lit(self, ty, elems, env, elem_ty=None):
        if ty is None:
            ty = elem_ty
        if ty is None:
            raise Unsupported("untyped literal")
        if ty[0] == "named" and ty[1] in self.pkg.types and self.pkg.types[ty[1]][0] != "struct":
            ty = self.pkg.types[ty[1]]
        if ty[0] == "ptr":
            inner = self.build_lit(ty[1], elems, env)
            if isinstance(inner, GoStruct):
                inner.is_val = False
            return inner
        if ty[0] == "slice":
            vals = []
            for k, v in elems:
                if k is not None:
                    raise Unsupported("keyed slice literal")
                vals.append(self.lit_elem(v, ty[1], env))
            return GoSlice(vals, 0, len(vals), len(vals))
        if ty[0] == "map":
            d = {}
            for k, v in elems:
                d[self.ev(k, env)] = self.lit_elem(v, ty[2], env)
            return d
        if ty[0] == "named" and ty[1] in self.pkg.types and self.pkg.types[ty[1]][0] == "struct":
            st = self.zero_struct(ty[1])
            fields = self.pkg.types[ty[1]][1]
            for idx, (k, v) in enumerate(elems):
                if k is None:
                    name = fields[idx][0]
                    fty = fields[idx][1]
                else:
                    if k[0] != "id":
                        raise Unsupported("struct key")
                    name = k[1]
                    fty = dict(fields)[name]
                st.fields[name] = self.lit_elem(v, fty, env)
            return st
        if ty[0] == "struct":
            st = GoStruct("<anon>", {n: self.zero(t) for n, t in ty[1]})
            for k, v in elems:
                st.fields[k[1]] = self.ev(v, env)
            return st
        raise Unsupported("literal of " + ty[0])

    def lit_elem(self, v, ty, env):
        if v[0] == "complit":
            return self.copyval(self.build_lit(v[1], v[2], env, ty))
        return self.copyval(self.ev(v, env))

    def n_unary(self, n, env):
        op = n[1]
        if op == "&":
            v = self.ev(n[2], env)
            if isinstance(v, GoStruct):
                if n[2][0] == "complit":
                    v.is_val = False
                    return v
                raise Unsupported("address of struct variable")
            raise Unsupported("address-of non-struct")
        v = self.ev(n[2], env)
        if op == "-":
            return wrap(-v)
        if op == "+":
            return v
        if op == "!":
            return not v
        if op == "^":
            return wrap(~v)
        if op == "*":
            if isinstance(v, GoStruct):
                return v.copy() if not v.is_val else v
            if v is None:
                raise GoPanic(RuntimeErr("errorString", "nil pointer dereference"), "errorString")
            raise Unsupported("deref")
        raise Unsupported("unary " + op)

    def n_bin(self, n, env):
        op = n[1]
        if op == "&&":
            return bool(self.ev(n[2], env)) and bool(self.ev(n[3], env))
        if op == "||":
            return bool(self.ev(n[2], env)) or bool(self.ev(n[3], env))
        return self.binop(op, self.ev(n[2], env), self.ev(n[3], env))

    def binop(self, op, a, b):
        if op == "+":
            if isinstance(a, str):
                return a + b
            return wrap(a + b)
        if op == "-":
            return wrap(a - b)
        if op == "*":
            return wrap(a * b)
        if op in ("/", "%"):
            if b == 0:
                raise GoPanic(RuntimeErr("errorString", "integer divide by zero"), "errorString")
            q = abs(a) // abs(b)
            if (a < 0) != (b < 0):
                q = -q
            return wrap(q) if op == "/" else wrap(a - q * b)
        if op == "==":
            return self.eq(a, b)
        if op == "!=":
            return not self.eq(a, b)
        if op == "<":
            return a < b
        if op == "<=":
            return a <= b
        if op == ">":
            return a > b
        if op == ">=":
            return a >= b
        if op == "&":
            return a & b
        if op == "|":
            return a | b
        if op == "^":
            return a ^ b
        if op == "&^":
            return a & ~b
        if op == "<<":
            return wrap(a << b)
        if op == ">>":
            return a >> b
        raise Unsupported("go binop " + op)

    def eq(self, a, b):
        if isinstance(a, GoStruct) and isinstance(b, GoStruct):
            if a.is_val and b.is_val:
                return a.tname == b.tname and a.fields == b.fields
            return a is b
        if isinstance(a, GoSlice) or isinstance(b, GoSlice):
            if a is None or b is None or a is NIL or b is NIL:
                x = a if isinstance(a, GoSlice) else b
                return isinstance(x, GoSlice) and x.nil if (a is None or b is None) else (a.nil == b.nil)
            raise Unsupported("slice comparison")
        return a == b

    def n_sel(self, n, env):
        base = n[1]
        if base[0] == "id" and env.find(base[1]) is None and base[1] not in self.pkg.funcs:
            return ("pkgfn", base[1], n[2])
        o = self.ev(base, env)
        name = n[2]
        if isinstance(o, GoStruct):
            if name in o.fields:
                return o.fields[name]
            m = self.pkg.methods.get(o.tname, {}).get(name)
            if m is not None:
                return ("method", m, o)
            raise Unsupported("no field/method %s.%s" % (o.tname, name))
        if isinstance(o, TestingT):
            return ("tmethod", o, name)
        if o is None:
            raise GoPanic(RuntimeErr("errorString", "nil pointer dereference"), "errorString")
        raise Unsupported("selector on " + type(o).__name__)

    def n_index(self, n, env):
        o = self.ev(n[1], env)
        i = self.ev(n[2], env)
        if isinstance(o, GoSlice):
            if i < 0 or i >= o.len:
                raise GoPanic(RuntimeErr("boundsError", "index out of range"), "boundsError")
            return o.arr[o.off + i]
        if isinstance(o, str):
            if i < 0 or i >= len(o):
                raise GoPanic(RuntimeErr("boundsError", "index out of range"), "boundsError")
            return ord(o[i])
        if isinstance(o, dict):
            if i in o:
                return o[i]
            raise Unsupported("map zero value of missing key (type unknown)")
        if o is None:
            raise GoPanic(RuntimeErr("errorString", "nil"), "errorString")
        raise Unsupported("index on " + type(o).__name__)

    def n_slice(self, n, env):
        o = self.ev(n[1], env)
        lo = self.ev(n[2], env) if n[2] is not None else 0
        if isinstance(o, str):
            hi = self.ev(n[3], env) if n[3] is not None else len(o)
            if not (0 <= lo <= hi <= len(o)):
                raise GoPanic(RuntimeErr("boundsError", "slice bounds out of range"), "boundsError")
            return o[lo:hi]
        if isinstance(o, GoSlice):
            hi = self.ev(n[3], env) if n[3] is not None else o.len
            if not (0 <= lo <= hi <= o.cap):
                raise GoPanic(RuntimeErr("boundsError", "slice bounds out of range"), "boundsError")
            return GoSlice(o.arr, o.off + lo, hi - lo, o.cap - lo)
        raise Unsupported("slice of " + type(o).__name__)

    def n_call(self, n, env):
        callee = n[1]
        args_n = n[2]
        spread = n[3]
        # builtins and conversions need the unevaluated callee name
        if callee[0] == "id" and env.find(callee[1]) is None and callee[1] not in self.pkg.funcs:
            nm = callee[1]
            if nm in _BUILTINS or nm in ("int", "string", "int64", "byte", "rune", "bool"):
                return self.builtin_call(nm, args_n, spread, env)
            if nm in self.pkg.types:
                v = self.ev(args_n[0], env)
                return v
        fv = self.ev(callee, env)
        args = [self.ev(a, env) if a[0] != "typeexpr" else ("type", a[1]) for a in args_n]
        if spread:
            last = args[-1]
            args = args[:-1] + (last.items() if isinstance(last, GoSlice) else [])
        return self.call_value(fv, args)

    def call_value(self, fv, args):
        if isinstance(fv, GoFunc):
            return self.call_func(fv, args)
        if isinstance(fv, tuple):
            k = fv[0]
            if k == "method":
                return self.call_func(fv[1], args, recv=fv[2])
            if k == "pkgfn":
                return self.pkg_call(fv[1], fv[2], args)
            if k == "tmethod":
                return self.t_call(fv[1], fv[2], args)
        if isinstance(fv, Native):
            return fv.fn(args)
        if fv is None:
            raise GoPanic(RuntimeErr("errorString", "nil function"), "errorString")
        raise Unsupported("call of %r" % (fv,))

    def builtin_call(self, nm, args_n, spread, env):
        if nm == "len":
            v = self.ev(args_n[0], env)
            if isinstance(v, str):
                return len(v)
            if isinstance(v, GoSlice):
                return v.len
            if isinstance(v, dict):
                return len(v)
            if v is None:
                return 0
            raise Unsupported("len of " + type(v).__name__)
        if nm == "cap":
            v = self.ev(args_n[0], env)
            return v.cap
        if nm == "append":
            s = self.ev(args_n[0], env)
            if spread:
                extra = self.ev(args_n[1], env)
                vals = extra.items() if isinstance(extra, GoSlice) else list(extra)
            else:
                vals = [self.copyval(self.ev(a, env)) for a in args_n[1:]]
            esize = 16 if (vals and isinstance(vals[0], str)) or (isinstance(s, GoSlice) and s.len and isinstance(s.arr[s.off], str)) else 8
            return go_append(s, vals, esize)
        if nm in ("min", "max"):
            vs = [self.ev(a, env) for a in args_n]
            return min(vs) if nm == "min" else max(vs)
        if nm == "make":
            ty = args_n[0][1] if args_n[0][0] == "typeexpr" else None
            if ty is None:
                raise Unsupported("make type")
            if ty[0] == "slice":
                ln = self.ev(args_n[1], env)
                cp = self.ev(args_n[2], env) if len(args_n) > 2 else ln
                z = self.zero(ty[1])
                return GoSlice([self.copyval(z) for _ in range(cp)], 0, ln, cp)
            if ty[0] == "map":
                return {}
            raise Unsupported("make of " + ty[0])
        if nm == "new":
            raise Unsupported("new")
        if nm == "panic":
            v = self.ev(args_n[0], env)
            raise GoPanic(v, self.type_name(v))
        if nm == "recover":
            return self.do_recover()
        if nm == "copy":
            dst, src = self.ev(args_n[0], env), self.ev(args_n[1], env)
            k = min(dst.len, src.len)
            vals = src.items()[:k]
            for i, v in enumerate(vals):
                dst.arr[dst.off + i] = v
            return k
        if nm == "delete":
            d = self.ev(args_n[0], env)
            d.pop(self.ev(args_n[1], env), None)
            return None
        if nm in ("int", "int64", "byte", "rune"):
            v = self.ev(args_n[0], env)
            if isinstance(v, bool) or not isinstance(v, int):
                raise Unsupported("conversion to int of " + type(v).__name__)
            return wrap(v)
        if nm == "string":
            v = self.ev(args_n[0], env)
            if isinstance(v, int):
                return chr(v)
            return v
        if nm == "bool":
            return self.ev(args_n[0], env)
        raise Unsupported("builtin " + nm)

    def type_name(self, v):
        if isinstance(v, GoStruct):
            return v.tname
        if isinstance(v, str):
            return "string"
        if isinstance(v, bool):
            return "bool"
        if isinstance(v, int):
            return "int"
        if isinstance(v, RuntimeErr):
            return v.tname
        return "?"

    def do_recover(self):
        if not self.recover_cells:
            return None
        cell = self.recover_cells[-1]
        if cell["panic"] is None or cell["recovered"]:
            return None
        cell["recovered"] = True
        p = cell["panic"]
        return p.value

    # ------------------------------------------------------------------ calls
    def call_func(self, f, args, recv=None):
        if self.depth > 120:
            raise Unsupported("go recursion depth")
        _, name, rcv, params, results, body = f.node
        if body is None:
            raise Unsupported("function without body")
        env = GoEnv(f.env)
        if rcv is not None:
            if recv is None:
                raise Unsupported("method call without receiver")
            if rcv[0]:
                env.vars[rcv[0]] = recv
        if len(args) != len(params) and not (params and params[-1][1][0] == "variadic"):
            raise Unsupported("arity %s" % name)
        for i, (pn, pt) in enumerate(params):
            if pt[0] == "variadic":
                rest = list(args[i:])
                if pn:
                    env.vars[pn] = GoSlice(rest, 0, len(rest), len(rest))
                break
            if pn and pn != "_":
                env.vars[pn] = self.copyval(args[i])
        named = [rn for rn, rt in results] if results and results[0][0] else None
        if named:
            for rn, rt in results:
                env.vars[rn] = self.zero(rt)
        fr = Frame(named)
        self.frames.append(fr)
        self.depth += 1
        vals = None
        panic = None
        try:
            try:
                self.exec_block(body[1], env)
            except _Ret as r:
                vals = r.vals
                if named and vals:
                    for rn, v in zip(named, vals):
                        env.vars[rn] = v
            except GoPanic as p:
                panic = p
            recovered_flag = False
            while fr.defers:
                df, dargs = fr.defers.pop()
                cell = {"panic": panic, "recovered": False}
                self.recover_cells.append(cell)
                try:
                    self.call_value(df, dargs)
                except GoPanic as p2:
                    panic = p2
                    cell["recovered"] = False
                finally:
                    self.recover_cells.pop()
                if cell["recovered"] and panic is not None and cell["panic"] is panic:
                    panic = None
                    recovered_flag = True
            if panic is not None:
                raise panic
            if named:
                out = [env.vars[rn] for rn in named]
            elif vals is not None:
                out = vals
            elif recovered_flag:
                out = [self.zero(rt) for rn, rt in results]
            else:
                out = []
            if len(out) == 0:
                return None
            if len(out) == 1:
                return out[0]
            return tuple(out)
        finally:
            self.depth -= 1
            self.frames.pop()

    # ------------------------------------------------------------------ std library
    def pkg_call(self, pkg, name, args):
        path = self.file_imports.get(self.cur_file, {}).get(pkg) if hasattr(self, "cur_file") else None
        key = pkg + "." + name
        fn = _STD.get(key)
        if fn is None:
            raise Unsupported("std " + key)
        return fn(self, args)

    def t_call(self, t, name, args):
        if name in ("Fatal", "Fatalf", "FailNow"):
            t.failed = True
            raise _FatalStop()
        if name in ("Error", "Errorf", "Fail"):
            t.failed = True
            return None
        if name in ("Skip", "Skipf", "SkipNow"):
            t.skipped = True
            raise _SkipStop()
        if name in ("Log", "Logf", "Helper"):
            return None
        raise Unsupported("t." + name)


class _FatalStop(Exception):
    pass


class _SkipStop(Exception):
    pass


_BUILTINS = {"len", "cap", "append", "min", "max", "make", "new", "panic", "recover", "copy", "delete", "print", "println"}


def _fmt(interp, fmt, args):
    out, i, k = [], 0, 0
    while i < len(fmt):
        c = fmt[i]
        if c != "%":
            out.append(c)
            i += 1
            continue
        m = re.compile(r"%([-+ 0#]*)(\d*)(?:\.(\d+))?([vdsTqxXctU%])").match(fmt, i)
        if not m:
            raise Unsupported("fmt verb")
        fl, w, pr, verb = m.groups()
        i = m.end()
        if verb == "%":
            out.append("%")
            continue
        a = args[k]
        k += 1
        if verb == "T":
            txt = _tname(interp, a)
        elif verb == "d":
            txt = str(a)
            if "0" in fl and w and "-" not in fl:
                neg = txt.startswith("-")
                txt = ("-" if neg else "") + txt.lstrip("-").rjust(int(w) - (1 if neg else 0), "0")
                w = ""
        elif verb in ("s", "v"):
            if isinstance(a, str):
                txt = a
            elif isinstance(a, bool):
                txt = "true" if a else "false"
            elif isinstance(a, int):
                txt = str(a)
            elif isinstance(a, GoSlice):
                txt = "[" + " ".join(str(x) for x in a.items()) + "]"
            elif a is None:
                txt = "<nil>"
            else:
                raise Unsupported("fmt %v of struct")
        elif verb == "q":
            txt = '"' + str(a).replace("\\", "\\\\").replace('"', '\\"') + '"'
        elif verb in ("x", "X"):
            txt = format(a, verb)
        elif verb == "c":
            txt = chr(a)
        elif verb == "t":
            txt = "true" if a else "false"
        else:
            raise Unsupported("fmt verb " + verb)
        if w:
            txt = txt.ljust(int(w)) if "-" in fl else txt.rjust(int(w))
        out.append(txt)
    return "".join(out)


def _tname(interp, v):
    if isinstance(v, GoStruct):
        return interp.pkg.name + "." + v.tname if v.tname != "<anon>" else "struct {}"
    if isinstance(v, RuntimeErr):
        return "runtime." + v.tname
    if isinstance(v, str):
        return "string"
    if isinstance(v, bool):
        return "bool"
    if isinstance(v, int):
        return "int"
    if isinstance(v, GoSlice):
        return "[]int"
    return "<nil>"


def _std_has_prefix(it, a):
    return a[0].startswith(a[1])


_STD = {
    "strings.HasPrefix": lambda it, a: a[0].startswith(a[1]),
    "strings.HasSuffix": lambda it, a: a[0].endswith(a[1]),
    "strings.Contains": lambda it, a: a[1] in a[0],
    "strings.Index": lambda it, a: a[0].find(a[1]),
    "strings.LastIndex": lambda it, a: a[0].rfind(a[1]),
    "strings.Repeat": lambda it, a: a[0] * a[1],
    "strings.ToUpper": lambda it, a: a[0].upper(),
    "strings.ToLower": lambda it, a: a[0].lower(),
    "strings.TrimSpace": lambda it, a: a[0].strip(),
    "strings.Join": lambda it, a: a[1].join(a[0].items()),
    "strings.Split": lambda it, a: (lambda parts: GoSlice(parts, 0, len(parts), len(parts)))(a[0].split(a[1]) if a[1] != "" else list(a[0])),
    "strings.Count": lambda it, a: a[0].count(a[1]) if a[1] else len(a[0]) + 1,
    "strings.ReplaceAll": lambda it, a: a[0].replace(a[1], a[2]),
    "strings.TrimPrefix": lambda it, a: a[0][len(a[1]):] if a[0].startswith(a[1]) else a[0],
    "strings.TrimSuffix": lambda it, a: a[0][:-len(a[1])] if a[1] and a[0].endswith(a[1]) else a[0],
    "fmt.Sprintf": lambda it, a: _fmt(it, a[0], a[1:]),
    "fmt.Sprint": lambda it, a: "".join(str(x) for x in a),
    "fmt.Println": lambda it, a: None,
    "fmt.Printf": lambda it, a: None,
    "slices.Equal": lambda it, a: a[0].items() == a[1].items(),
    "slices.Contains": lambda it, a: a[1] in a[0].items(),
    "slices.Index": lambda it, a: (a[0].items().index(a[1]) if a[1] in a[0].items() else -1),
    "strconv.Itoa": lambda it, a: str(a[0]),
    "os.Exit": lambda it, a: (_ for _ in ()).throw(ProcessExit(a[0])),
}


# ------------------------------------------------------------------------------------------------ program adapter and `go test` model
def to_plain(v):
    if isinstance(v, GoSlice):
        return [to_plain(x) for x in v.items()]
    if isinstance(v, GoStruct):
        return {"__struct__": v.tname}
    if isinstance(v, tuple):
        return [to_plain(x) for x in v]
    return v


class BuildError(Exception):
    pass


class GoProgram:
    def __init__(self, files, budget=None):
        self.files = {p: t for p, t in files.items() if p.endswith(".go") and not p.endswith("_test.go")}
        self.budget = budget or Budget(30_000_000)
        self.it = GoInterp(self.files, self.budget)
        if self.it.build_errors:
            raise Unsupported("go build error: " + self.it.build_errors[0])
        self.mk = {}
        for tn in self.it.pkg.methods:
            self.mk[tn] = "mk" + tn

    def fresh(self, fn):
        if fn in self.it.pkg.funcs:
            return None
        for tn, ms in self.it.pkg.methods.items():
            if fn in ms:
                ctor = self.it.pkg.funcs.get("mk" + tn)
                if ctor is None:
                    st = self.it.zero_struct(tn)
                    st.is_val = False
                    return st
                return self.it.call_func(ctor, [])
        raise Unsupported("no callable " + fn)

    def invoke(self, inst, fn, args):
        import copy
        a = []
        for x in args:
            if isinstance(x, list):
                a.append(GoSlice(list(x), 0, len(x), len(x)))
            else:
                a.append(x)
        try:
            if inst is None:
                f = self.it.pkg.funcs[fn]
                r = self.it.call_func(f, a)
            else:
                m = self.it.pkg.methods[inst.tname][fn]
                r = self.it.call_func(m, a, recv=inst)
            return ("ok", to_plain(r))
        except GoPanic as p:
            return ("exc", p.tname if p.tname else self.it.type_name(p.value))


def run_go_tests(files, only=None, budget=None):
    fs = {p: t for p, t in files.items() if p.endswith(".go") or p == "go.mod"}
    out = {"outcomes": {}, "exit": 0, "collected": 0, "error": None}
    try:
        it = GoInterp(fs, budget or Budget(10_000_000))
    except ProcessExit as pe:
        out["exit"] = pe.code
        return out
    if it.build_errors:
        out["exit"] = 2
        out["error"] = "build: " + it.build_errors[0]
        return out
    try:
        for f in it.inits:
            it.call_func(f, [])
        tests = [t for t in it.tests if only is None or t[0] in only]
        failed = False

        def run_all():
            nonlocal failed
            for p, name, gf in tests:
                out["collected"] += 1
                t = TestingT(name)
                try:
                    it.call_func(gf, [t])
                except _FatalStop:
                    pass
                except _SkipStop:
                    pass
                except GoPanic:
                    out["outcomes"][p + "::" + name] = "failed"
                    out["exit"] = 2
                    failed = True
                    return 2
                out["outcomes"][p + "::" + name] = "skipped" if t.skipped else ("failed" if t.failed else "passed")
                if t.failed:
                    failed = True
            return 1 if failed else 0
        if it.testmain is not None:
            class _M:
                pass
            mobj = Native(lambda a: run_all())
            m = GoStruct("M", {"Run": mobj}, False)
            it.pkg.methods.setdefault("M", {})
            # m.Run() : model via a special tuple
            mm = _MainM(run_all)
            code = it.call_func(it.testmain, [mm])
            out["exit"] = 1 if failed else out["exit"]
        else:
            code = run_all()
            if code:
                out["exit"] = max(out["exit"], code)
    except ProcessExit as pe:
        out["exit"] = pe.code
    except GoPanic:
        out["exit"] = 2
    return out


class _MainM:
    def __init__(self, run):
        self.run = run


# `m.Run()` support: selector on _MainM
_orig_sel = GoInterp.n_sel


def _n_sel(self, n, env):
    base = n[1]
    if base[0] == "id" and env.find(base[1]) is not None:
        o = env.find(base[1]).vars[base[1]]
        if isinstance(o, _MainM) and n[2] == "Run":
            return Native(lambda a: o.run())
    return _orig_sel(self, n, env)


GoInterp.n_sel = _n_sel

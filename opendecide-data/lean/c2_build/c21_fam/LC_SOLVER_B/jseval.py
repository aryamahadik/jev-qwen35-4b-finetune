"""Solver B: own tokenizer + parser + evaluator for the rendered JavaScript / TypeScript subset (TS = JS after type erasure).

JS numbers are Python int (while integral and <= 2^53) or float. Arrays are Python lists, strings Python str, objects JSObj, `undefined`
is the UNDEF singleton, `null` is None. Real JS semantics are implemented for + (string concat), % (sign of dividend), / (true
division), strict equality (identity for arrays / objects), array holes never (out-of-range read = undefined), Math.trunc, padStart ...
A small `node:test` / `node:assert/strict` model sits at the bottom (assert is a mutable object, so test files may replace its
methods, exactly like the rendered tamper does).
"""
import math
import re

from .common import Budget, Timeout, Unsupported


class _Undef:
    def __repr__(self):
        return "undefined"

    def __bool__(self):
        return False


UNDEF = _Undef()
MAXSAFE = 2 ** 53


# ------------------------------------------------------------------------------------------------ tokenizer
_PUNCT = ["...", "===", "!==", "**=", "<<=", ">>=", ">>>", "&&=", "||=", "??=", "=>", "==", "!=", "<=", ">=", "&&", "||", "??", "?.",
          "++", "--", "+=", "-=", "*=", "/=", "%=", "&=", "|=", "^=", "<<", ">>", "**", "{", "}", "(", ")", "[", "]", ";", ",", "<",
          ">", "+", "-", "*", "/", "%", "&", "|", "^", "!", "~", "?", ":", "=", ".", "@", "#"]
_ID = re.compile(r"[A-Za-z_$][A-Za-z0-9_$]*")
_NUM = re.compile(r"0[xX][0-9a-fA-F_]+|0[bB][01_]+|0[oO][0-7_]+|(?:\d[\d_]*\.?\d*|\.\d+)(?:[eE][+-]?\d+)?")


class Tok:
    __slots__ = ("t", "v", "nl", "pos")

    def __init__(self, t, v, nl, pos):
        self.t, self.v, self.nl, self.pos = t, v, nl, pos

    def __repr__(self):
        return "%s:%r" % (self.t, self.v)


_ESC = {"n": "\n", "t": "\t", "r": "\r", "b": "\b", "f": "\f", "v": "\v", "0": "\0", "'": "'", '"': '"', "\\": "\\", "`": "`",
        "$": "$", "\n": ""}


def _unescape(s):
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == "\\":
            i += 1
            d = s[i]
            if d == "x":
                out.append(chr(int(s[i + 1:i + 3], 16)))
                i += 3
                continue
            if d == "u":
                if s[i + 1] == "{":
                    j = s.index("}", i)
                    out.append(chr(int(s[i + 2:j], 16)))
                    i = j + 1
                else:
                    out.append(chr(int(s[i + 1:i + 5], 16)))
                    i += 5
                continue
            out.append(_ESC.get(d, d))
            i += 1
        else:
            out.append(c)
            i += 1
    return "".join(out)


def tokenize(src):
    toks = []
    i, n = 0, len(src)
    nl = False
    while i < n:
        c = src[i]
        if c == "\n":
            nl = True
            i += 1
            continue
        if c in " \t\r﻿":
            i += 1
            continue
        if src.startswith("//", i):
            j = src.find("\n", i)
            i = n if j < 0 else j
            continue
        if src.startswith("/*", i):
            j = src.find("*/", i + 2)
            if j < 0:
                raise Unsupported("unterminated comment")
            if "\n" in src[i:j]:
                nl = True
            i = j + 2
            continue
        if c == "#" and i == 0 and src.startswith("#!"):
            j = src.find("\n", i)
            i = n if j < 0 else j
            continue
        if c in "'\"":
            j = i + 1
            while j < n and src[j] != c:
                if src[j] == "\\":
                    j += 1
                if src[j] == "\n":
                    raise Unsupported("newline in string")
                j += 1
            toks.append(Tok("str", _unescape(src[i + 1:j]), nl, i))
            nl = False
            i = j + 1
            continue
        if c == "`":
            j = i + 1
            parts, buf = [], []
            while j < n and src[j] != "`":
                if src[j] == "\\":
                    buf.append(src[j:j + 2])
                    j += 2
                    continue
                if src.startswith("${", j):
                    depth, k = 1, j + 2
                    while k < n and depth:
                        if src[k] == "{":
                            depth += 1
                        elif src[k] == "}":
                            depth -= 1
                        k += 1
                    parts.append(("s", _unescape("".join(buf))))
                    buf = []
                    parts.append(("e", src[j + 2:k - 1]))
                    j = k
                    continue
                buf.append(src[j])
                j += 1
            parts.append(("s", _unescape("".join(buf))))
            toks.append(Tok("tmpl", parts, nl, i))
            nl = False
            i = j + 1
            continue
        m = _NUM.match(src, i) if (c.isdigit() or (c == "." and i + 1 < n and src[i + 1].isdigit())) else None
        if m:
            txt = m.group(0).replace("_", "")
            if txt[:2] in ("0x", "0X"):
                v = int(txt, 16)
            elif txt[:2] in ("0b", "0B"):
                v = int(txt[2:], 2)
            elif txt[:2] in ("0o", "0O"):
                v = int(txt[2:], 8)
            elif re.fullmatch(r"\d+", txt):
                v = int(txt)
            else:
                v = float(txt)
                if v == int(v) and abs(v) <= MAXSAFE:
                    v = int(v)
            if i + len(m.group(0)) < n and src[i + len(m.group(0))] == "n":
                raise Unsupported("bigint")
            toks.append(Tok("num", v, nl, i))
            nl = False
            i += len(m.group(0))
            continue
        m = _ID.match(src, i)
        if m:
            toks.append(Tok("id", m.group(0), nl, i))
            nl = False
            i = m.end()
            continue
        for p in _PUNCT:
            if src.startswith(p, i):
                toks.append(Tok("p", p, nl, i))
                nl = False
                i += len(p)
                break
        else:
            raise Unsupported("char %r" % c)
    toks.append(Tok("eof", None, True, n))
    return toks


# ------------------------------------------------------------------------------------------------ parser (nodes are tuples)
_BIN_PREC = {"??": 1, "||": 2, "&&": 3, "|": 4, "^": 5, "&": 6, "==": 7, "!=": 7, "===": 7, "!==": 7, "<": 8, ">": 8, "<=": 8,
             ">=": 8, "instanceof": 8, "in": 8, "<<": 9, ">>": 9, ">>>": 9, "+": 10, "-": 10, "*": 11, "/": 11, "%": 11, "**": 12}
_ASSIGN = {"=", "+=", "-=", "*=", "/=", "%=", "**=", "&=", "|=", "^=", "<<=", ">>=", "&&=", "||=", "??="}
_MODS = {"public", "private", "protected", "readonly", "static", "abstract", "declare", "override"}


class Parser:
    def __init__(self, src):
        self.src = src
        self.toks = tokenize(src)
        self.i = 0

    # -- helpers
    @property
    def tok(self):
        return self.toks[self.i]

    def peek(self, k=1):
        return self.toks[min(self.i + k, len(self.toks) - 1)]

    def is_p(self, v):
        t = self.toks[self.i]
        return t.t == "p" and t.v == v

    def is_id(self, v):
        t = self.toks[self.i]
        return t.t == "id" and t.v == v

    def eat_p(self, v):
        if self.is_p(v):
            self.i += 1
            return True
        return False

    def eat_id(self, v):
        if self.is_id(v):
            self.i += 1
            return True
        return False

    def expect_p(self, v):
        if not self.eat_p(v):
            raise Unsupported("parse: expected %r got %r at %d" % (v, self.tok, self.tok.pos))

    def ident(self):
        t = self.tok
        if t.t != "id":
            raise Unsupported("parse: identifier expected got %r" % (t,))
        self.i += 1
        return t.v

    # -- types (erased)
    def skip_type(self):
        depth = 0
        start = self.i
        while True:
            t = self.tok
            if t.t == "eof":
                break
            if t.t == "p":
                v = t.v
                if depth == 0 and v in (",", ")", ";", "=", "}", "]") or (depth == 0 and v == "{" and self.i > start):
                    break
                if depth == 0 and v == "=>" and self.i > start:
                    # arrow return type; the '=>' ends it
                    break
                if v in ("(", "[", "<", "{"):
                    depth += 1
                elif v in (")", "]", ">", "}"):
                    depth -= 1
                elif v == ">>":
                    depth -= 2
                elif v == ">=":
                    pass
            if t.t == "id" and depth == 0 and self.i > start and t.nl and self.toks[self.i - 1].t == "id":
                break
            self.i += 1

    # -- program
    def parse_program(self):
        body = []
        while self.tok.t != "eof":
            s = self.statement()
            if s is not None:
                body.append(s)
        return body

    def block(self):
        self.expect_p("{")
        body = []
        while not self.is_p("}"):
            if self.tok.t == "eof":
                raise Unsupported("parse: eof in block")
            s = self.statement()
            if s is not None:
                body.append(s)
        self.expect_p("}")
        return ("block", body)

    def semi(self):
        self.eat_p(";")

    def statement(self):
        t = self.tok
        if t.t == "p":
            if t.v == "{":
                return self.block()
            if t.v == ";":
                self.i += 1
                return None
        if t.t == "id":
            v = t.v
            if v in ("const", "let", "var"):
                n = self.var_decl()
                self.semi()
                return n
            if v == "function":
                return self.func_decl()
            if v == "async":
                raise Unsupported("async")
            if v == "class":
                return self.class_decl()
            if v == "if":
                self.i += 1
                self.expect_p("(")
                c = self.expr()
                self.expect_p(")")
                a = self.statement()
                b = None
                if self.eat_id("else"):
                    b = self.statement()
                return ("if", c, a, b)
            if v == "for":
                return self.for_stmt()
            if v == "while":
                self.i += 1
                self.expect_p("(")
                c = self.expr()
                self.expect_p(")")
                return ("while", c, self.statement())
            if v == "do":
                self.i += 1
                body = self.statement()
                if not self.eat_id("while"):
                    raise Unsupported("do without while")
                self.expect_p("(")
                c = self.expr()
                self.expect_p(")")
                self.semi()
                return ("dowhile", body, c)
            if v == "return":
                self.i += 1
                e = None
                if not (self.is_p(";") or self.is_p("}") or self.tok.nl or self.tok.t == "eof"):
                    e = self.expr()
                self.semi()
                return ("return", e)
            if v == "throw":
                self.i += 1
                e = self.expr()
                self.semi()
                return ("throw", e)
            if v == "break":
                self.i += 1
                self.semi()
                return ("break",)
            if v == "continue":
                self.i += 1
                self.semi()
                return ("continue",)
            if v == "try":
                self.i += 1
                b = self.block()
                param, h, f = None, None, None
                if self.eat_id("catch"):
                    if self.eat_p("("):
                        param = self.ident()
                        if self.eat_p(":"):
                            self.skip_type()
                        self.expect_p(")")
                    h = self.block()
                if self.eat_id("finally"):
                    f = self.block()
                return ("try", b, param, h, f)
            if v == "switch":
                return self.switch_stmt()
            if v == "import":
                return self.import_stmt()
            if v == "export":
                return self.export_stmt()
            if v in ("interface", "type") and self.peek().t == "id":
                return self.skip_type_decl()
            if v == "enum" or (v == "declare"):
                raise Unsupported("enum/declare")
        e = self.expr()
        self.semi()
        return ("expr", e)

    def skip_type_decl(self):
        kw = self.tok.v
        self.i += 1
        if kw == "interface":
            while not self.is_p("{"):
                self.i += 1
            depth = 0
            while True:
                if self.is_p("{"):
                    depth += 1
                elif self.is_p("}"):
                    depth -= 1
                    if depth == 0:
                        self.i += 1
                        break
                self.i += 1
        else:
            while not self.is_p("="):
                self.i += 1
            self.i += 1
            depth = 0
            while True:
                t = self.tok
                if t.t == "eof":
                    break
                if t.t == "p" and t.v in ("{", "(", "["):
                    depth += 1
                elif t.t == "p" and t.v in ("}", ")", "]"):
                    depth -= 1
                if t.t == "p" and t.v == ";" and depth <= 0:
                    self.i += 1
                    break
                self.i += 1
        return None

    def import_stmt(self):
        self.i += 1
        if self.tok.t == "str":
            self.i += 1
            self.semi()
            return ("import", [], self.toks[self.i - 1].v if False else None)
        default = None
        named = []
        star = None
        if self.tok.t == "id" and self.tok.v == "type" and self.peek().t in ("id", "p") and self.peek().v not in ("from", ","):
            self.i += 1
        if self.tok.t == "id":
            default = self.ident()
            self.eat_p(",")
        if self.eat_p("*"):
            if not self.eat_id("as"):
                raise Unsupported("import *")
            star = self.ident()
        if self.eat_p("{"):
            while not self.is_p("}"):
                nm = self.ident()
                al = nm
                if self.eat_id("as"):
                    al = self.ident()
                named.append((nm, al))
                if not self.eat_p(","):
                    break
            self.expect_p("}")
        if not self.eat_id("from"):
            raise Unsupported("import from")
        src = self.tok.v
        self.i += 1
        self.semi()
        return ("import", default, named, star, src)

    def export_stmt(self):
        self.i += 1
        if self.eat_id("default"):
            e = self.expr()
            self.semi()
            return ("exportdefault", e)
        if self.is_p("{"):
            self.i += 1
            names = []
            while not self.is_p("}"):
                nm = self.ident()
                al = nm
                if self.eat_id("as"):
                    al = self.ident()
                names.append((nm, al))
                if not self.eat_p(","):
                    break
            self.expect_p("}")
            self.semi()
            return ("exportnames", names)
        st = self.statement()
        return ("export", st)

    def switch_stmt(self):
        self.i += 1
        self.expect_p("(")
        d = self.expr()
        self.expect_p(")")
        self.expect_p("{")
        cases = []
        while not self.is_p("}"):
            if self.eat_id("case"):
                t = self.expr()
            elif self.eat_id("default"):
                t = None
            else:
                raise Unsupported("switch body")
            self.expect_p(":")
            body = []
            while not (self.is_id("case") or self.is_id("default") or self.is_p("}")):
                s = self.statement()
                if s is not None:
                    body.append(s)
            cases.append((t, body))
        self.expect_p("}")
        return ("switch", d, cases)

    def var_decl(self):
        kind = self.tok.v
        self.i += 1
        decls = []
        while True:
            target = self.binding_target()
            self.eat_p("!")
            if self.eat_p(":"):
                self.skip_type()
            init = None
            if self.eat_p("="):
                init = self.assign_expr()
            decls.append((target, init))
            if not self.eat_p(","):
                break
        return ("var", kind, decls)

    def binding_target(self):
        if self.is_p("{"):
            self.i += 1
            props = []
            while not self.is_p("}"):
                if self.eat_p("..."):
                    props.append(("rest", self.ident(), None))
                else:
                    key = self.ident()
                    tgt = key
                    default = None
                    if self.eat_p(":"):
                        tgt = self.binding_target()
                    if self.eat_p("="):
                        default = self.assign_expr()
                    props.append((key, tgt, default))
                if not self.eat_p(","):
                    break
            self.expect_p("}")
            return ("objpat", props)
        if self.is_p("["):
            self.i += 1
            elems = []
            while not self.is_p("]"):
                if self.is_p(","):
                    self.i += 1
                    elems.append(None)
                    continue
                tgt = self.binding_target()
                default = None
                if self.eat_p("="):
                    default = self.assign_expr()
                elems.append((tgt, default))
                if not self.eat_p(","):
                    break
            self.expect_p("]")
            return ("arrpat", elems)
        return self.ident()

    def for_stmt(self):
        self.i += 1
        self.expect_p("(")
        init = None
        if self.is_p(";"):
            pass
        elif self.tok.t == "id" and self.tok.v in ("const", "let", "var"):
            save = self.i
            kind = self.tok.v
            self.i += 1
            tgt = self.binding_target()
            if self.is_id("of") or self.is_id("in"):
                which = self.tok.v
                self.i += 1
                it = self.assign_expr() if which == "of" else self.expr()
                self.expect_p(")")
                body = self.statement()
                return ("forof" if which == "of" else "forin", kind, tgt, it, body)
            self.i = save
            init = self.var_decl()
        else:
            init = ("expr", self.expr())
        self.expect_p(";")
        cond = None if self.is_p(";") else self.expr()
        self.expect_p(";")
        upd = None if self.is_p(")") else self.expr()
        self.expect_p(")")
        return ("for", init, cond, upd, self.statement())

    def params(self):
        self.expect_p("(")
        ps = []
        while not self.is_p(")"):
            while self.tok.t == "id" and self.tok.v in _MODS and self.peek().t == "id":
                self.i += 1
            if self.eat_p("..."):
                ps.append(("rest", self.ident(), None))
            else:
                tgt = self.binding_target()
                if self.eat_p("?"):
                    pass
                if self.eat_p(":"):
                    self.skip_type()
                default = None
                if self.eat_p("="):
                    default = self.assign_expr()
                ps.append(("p", tgt, default))
            if not self.eat_p(","):
                break
        self.expect_p(")")
        return ps

    def func_decl(self):
        self.i += 1
        if self.is_p("*"):
            raise Unsupported("generator")
        name = self.ident()
        if self.is_p("<"):
            self.skip_generics()
        ps = self.params()
        if self.eat_p(":"):
            self.skip_type()
        if self.is_p("{"):
            body = self.block()
        else:
            self.semi()
            return None                                  # overload signature
        return ("funcdecl", name, ("func", name, ps, body, False))

    def skip_generics(self):
        depth = 0
        while True:
            if self.is_p("<"):
                depth += 1
            elif self.is_p(">"):
                depth -= 1
                if depth == 0:
                    self.i += 1
                    return
            self.i += 1

    def class_decl(self):
        self.i += 1
        name = self.ident()
        return ("classdecl", name, self.class_body(name))

    def class_body(self, name):
        if self.is_p("<"):
            self.skip_generics()
        parent = None
        if self.eat_id("extends"):
            parent = self.unary()
            if self.is_p("<"):
                self.skip_generics()
        if self.eat_id("implements"):
            while not self.is_p("{"):
                self.i += 1
        self.expect_p("{")
        members = []
        while not self.is_p("}"):
            if self.eat_p(";"):
                continue
            static = False
            while self.tok.t == "id" and self.tok.v in _MODS and not (self.peek().t == "p" and self.peek().v in ("(", ":", "=", ";", "?")):
                if self.tok.v == "static":
                    static = True
                self.i += 1
            if self.is_id("get") or self.is_id("set") or self.is_id("async"):
                if not (self.peek().t == "p" and self.peek().v in ("(", ":", "=", ";")):
                    raise Unsupported("accessor/async member")
            if self.is_p("["):
                raise Unsupported("computed member")
            if self.tok.t == "p" and self.tok.v == "#":
                raise Unsupported("private member")
            key = self.tok.v if self.tok.t in ("id", "str", "num") else None
            if key is None:
                raise Unsupported("class member %r" % (self.tok,))
            self.i += 1
            if self.is_p("("):
                if self.is_p("<"):
                    self.skip_generics()
                ps = self.params()
                if self.eat_p(":"):
                    self.skip_type()
                if self.is_p("{"):
                    body = self.block()
                else:
                    self.semi()
                    continue
                members.append(("method", key, ("func", key, ps, body, False), static))
            elif self.is_p("<"):
                self.skip_generics()
                ps = self.params()
                if self.eat_p(":"):
                    self.skip_type()
                body = self.block()
                members.append(("method", key, ("func", key, ps, body, False), static))
            else:
                self.eat_p("?")
                self.eat_p("!")
                if self.eat_p(":"):
                    self.skip_type()
                init = None
                if self.eat_p("="):
                    init = self.assign_expr()
                self.semi()
                members.append(("field", key, init, static))
        self.expect_p("}")
        return ("class", name, parent, members)

    # -- expressions
    def expr(self):
        e = self.assign_expr()
        if self.is_p(","):
            es = [e]
            while self.eat_p(","):
                es.append(self.assign_expr())
            return ("seq", es)
        return e

    def arrow_ahead(self):
        """True when the '(' at self.i begins an arrow-function parameter list."""
        depth, j = 0, self.i
        while j < len(self.toks):
            t = self.toks[j]
            if t.t == "p":
                if t.v in ("(", "[", "{"):
                    depth += 1
                elif t.v in (")", "]", "}"):
                    depth -= 1
                    if depth == 0:
                        nx = self.toks[j + 1]
                        if nx.t == "p" and nx.v == "=>":
                            return True
                        if nx.t == "p" and nx.v == ":":
                            # TS return type then '=>'
                            k = j + 2
                            d2 = 0
                            while k < len(self.toks):
                                tk = self.toks[k]
                                if tk.t == "p" and tk.v in ("(", "[", "{", "<"):
                                    d2 += 1
                                elif tk.t == "p" and tk.v in (")", "]", "}", ">"):
                                    d2 -= 1
                                elif tk.t == "p" and tk.v == "=>" and d2 == 0:
                                    return True
                                elif tk.t == "p" and tk.v in (";", "=", ",") and d2 <= 0:
                                    return False
                                k += 1
                        return False
            elif t.t == "eof":
                return False
            j += 1
        return False

    def arrow_body(self, ps):
        if self.is_p("{"):
            return ("arrow", ps, self.block(), True)
        return ("arrow", ps, self.assign_expr(), False)

    def assign_expr(self):
        t = self.tok
        if t.t == "id" and t.v == "async":
            raise Unsupported("async")
        if t.t == "id" and self.peek().t == "p" and self.peek().v == "=>":
            name = self.ident()
            self.i += 1
            return self.arrow_body([("p", name, None)])
        if t.t == "p" and t.v == "(" and self.arrow_ahead():
            ps = self.params()
            if self.eat_p(":"):
                self.skip_type()
            self.expect_p("=>")
            return self.arrow_body(ps)
        left = self.cond_expr()
        t = self.tok
        if t.t == "p" and t.v in _ASSIGN:
            self.i += 1
            right = self.assign_expr()
            if left[0] not in ("id", "member", "index"):
                raise Unsupported("assign target %s" % left[0])
            return ("assign", t.v, left, right)
        return left

    def cond_expr(self):
        c = self.bin_expr(0)
        if self.is_p("?"):
            self.i += 1
            a = self.assign_expr()
            self.expect_p(":")
            b = self.assign_expr()
            return ("cond", c, a, b)
        return c

    def bin_expr(self, minp):
        left = self.unary()
        while True:
            t = self.tok
            if t.t == "id" and t.v == "as" and not t.nl:
                self.i += 1
                self.skip_type()
                continue
            if t.t == "p" or (t.t == "id" and t.v in ("instanceof", "in")):
                op = t.v
            else:
                break
            p = _BIN_PREC.get(op)
            if p is None or p < minp:
                break
            self.i += 1
            right = self.bin_expr(p + 1 if op != "**" else p)
            if op in ("&&", "||", "??"):
                left = ("logic", op, left, right)
            else:
                left = ("bin", op, left, right)
        return left

    def unary(self):
        t = self.tok
        if t.t == "p" and t.v in ("!", "-", "+", "~"):
            self.i += 1
            return ("unary", t.v, self.unary())
        if t.t == "p" and t.v in ("++", "--"):
            self.i += 1
            return ("update", t.v, True, self.unary())
        if t.t == "id" and t.v in ("typeof", "void", "delete"):
            self.i += 1
            return ("unary", t.v, self.unary())
        if t.t == "id" and t.v == "await":
            raise Unsupported("await")
        return self.postfix()

    def postfix(self):
        e = self.call_expr()
        t = self.tok
        if t.t == "p" and t.v in ("++", "--") and not t.nl:
            self.i += 1
            return ("update", t.v, False, e)
        return e

    def args(self):
        self.expect_p("(")
        out = []
        while not self.is_p(")"):
            if self.eat_p("..."):
                out.append(("spread", self.assign_expr()))
            else:
                out.append(self.assign_expr())
            if not self.eat_p(","):
                break
        self.expect_p(")")
        return out

    def call_expr(self):
        if self.is_id("new"):
            self.i += 1
            callee = self.member_only()
            a = self.args() if self.is_p("(") else []
            e = ("new", callee, a)
        else:
            e = self.primary()
        while True:
            t = self.tok
            if t.t == "p":
                if t.v == ".":
                    self.i += 1
                    nm = self.tok
                    if nm.t != "id":
                        raise Unsupported("member name")
                    self.i += 1
                    e = ("member", e, nm.v)
                    continue
                if t.v == "?.":
                    raise Unsupported("optional chaining")
                if t.v == "(":
                    e = ("call", e, self.args())
                    continue
                if t.v == "[":
                    self.i += 1
                    k = self.expr()
                    self.expect_p("]")
                    e = ("index", e, k)
                    continue
                if t.v == "!" and not t.nl and self.peek().t == "p" and self.peek().v in (".", ")", ";", ",", "]"):
                    self.i += 1                         # TS non-null assertion
                    continue
            break
        return e

    def member_only(self):
        e = self.primary()
        while self.is_p("."):
            self.i += 1
            e = ("member", e, self.ident())
        return e

    def primary(self):
        t = self.tok
        if t.t == "num":
            self.i += 1
            return ("num", t.v)
        if t.t == "str":
            self.i += 1
            return ("str", t.v)
        if t.t == "tmpl":
            self.i += 1
            parts = []
            for k, v in t.v:
                parts.append(("s", v) if k == "s" else ("e", Parser(v).expr()))
            return ("tmpl", parts)
        if t.t == "id":
            v = t.v
            if v == "function":
                self.i += 1
                name = None
                if self.tok.t == "id":
                    name = self.ident()
                ps = self.params()
                if self.eat_p(":"):
                    self.skip_type()
                return ("funcexpr", ("func", name, ps, self.block(), False))
            if v == "class":
                self.i += 1
                name = None
                if self.tok.t == "id" and self.tok.v not in ("extends",):
                    name = self.ident()
                return ("classexpr", self.class_body(name))
            if v in ("true", "false"):
                self.i += 1
                return ("lit", v == "true")
            if v == "null":
                self.i += 1
                return ("lit", None)
            if v == "undefined":
                self.i += 1
                return ("lit", UNDEF)
            if v == "this":
                self.i += 1
                return ("this",)
            if v == "super":
                self.i += 1
                return ("super",)
            if v in ("typeof", "void", "delete", "new"):
                return self.unary()
            self.i += 1
            return ("id", v)
        if t.t == "p":
            if t.v == "(":
                self.i += 1
                e = self.expr()
                self.expect_p(")")
                return e
            if t.v == "[":
                self.i += 1
                els = []
                while not self.is_p("]"):
                    if self.is_p(","):
                        raise Unsupported("array hole")
                    if self.eat_p("..."):
                        els.append(("spread", self.assign_expr()))
                    else:
                        els.append(self.assign_expr())
                    if not self.eat_p(","):
                        break
                self.expect_p("]")
                return ("array", els)
            if t.v == "{":
                return self.object_lit()
        raise Unsupported("parse: unexpected %r at %d" % (t, t.pos))

    def object_lit(self):
        self.expect_p("{")
        props = []
        while not self.is_p("}"):
            if self.eat_p("..."):
                props.append(("spread", self.assign_expr()))
            else:
                t = self.tok
                if t.t == "p" and t.v == "[":
                    self.i += 1
                    k = self.assign_expr()
                    self.expect_p("]")
                    key = ("computed", k)
                elif t.t in ("id", "str", "num"):
                    self.i += 1
                    key = ("const", t.v)
                else:
                    raise Unsupported("object key")
                if self.is_p("("):
                    ps = self.params()
                    props.append(("prop", key, ("funcexpr", ("func", None, ps, self.block(), False))))
                elif self.eat_p(":"):
                    props.append(("prop", key, self.assign_expr()))
                else:
                    props.append(("prop", key, ("id", key[1])))
            if not self.eat_p(","):
                break
        self.expect_p("}")
        return ("object", props)


# ------------------------------------------------------------------------------------------------ runtime values
class JSThrow(Exception):
    def __init__(self, value):
        Exception.__init__(self, "js throw")
        self.value = value


class _Ret(Exception):
    def __init__(self, v):
        self.v = v


class _Brk(Exception):
    pass


class _Cnt(Exception):
    pass


class JSObj:
    def __init__(self, cls=None):
        self.props = {}
        self.cls = cls

    def to_plain(self):
        return {k: _plain(v) for k, v in self.props.items()}


class JSClass:
    def __init__(self, name, parent, ctor, methods, statics, fields, env, interp, native=None):
        self.name, self.parent, self.ctor, self.methods = name, parent, ctor, methods
        self.statics, self.fields, self.env, self.interp = statics, fields, env, interp
        self.native = native

    def chain(self):
        c = self
        while c is not None:
            yield c
            c = c.parent

    def find_method(self, name):
        for c in self.chain():
            if name in c.methods:
                return c.methods[name]
        return None


class JSFunc:
    def __init__(self, node, env, interp, this=None, arrow=False, name=None):
        self.node, self.env, self.interp, self.this, self.arrow = node, env, interp, this, arrow
        self.name = name or (node[1] if node[0] == "func" else None)
        self.props = {}


class Native:
    def __init__(self, fn, name=""):
        self.fn, self.name = fn, name
        self.props = {}


class Env:
    __slots__ = ("vars", "parent", "consts", "func")

    def __init__(self, parent=None, func=False):
        self.vars = {}
        self.parent = parent
        self.consts = set()
        self.func = func

    def find(self, name):
        e = self
        while e is not None:
            if name in e.vars:
                return e
            e = e.parent
        return None

    def declare(self, name, v, const=False):
        self.vars[name] = v
        if const:
            self.consts.add(name)


def _plain(v):
    if isinstance(v, bool) or v is None or isinstance(v, (int, str)):
        return v
    if v is UNDEF:
        return None
    if isinstance(v, float):
        if v != v:
            return "NaN"
        if v in (math.inf, -math.inf):
            return "Infinity" if v > 0 else "-Infinity"
        return int(v) if v == int(v) else v
    if isinstance(v, list):
        return [_plain(x) for x in v]
    if isinstance(v, JSObj):
        return v.to_plain()
    raise Unsupported("plain " + type(v).__name__)


def neg(v):
    """True for a negative number or negative zero (JS has a signed zero; ints here are +0)."""
    return v < 0 or (isinstance(v, float) and v == 0 and math.copysign(1, v) < 0)


def norm(x):
    if isinstance(x, float) and x == 0 and math.copysign(1, x) < 0:
        return x                                   # keep -0: assert.deepStrictEqual(-0, 0) fails in Node
    if isinstance(x, float):
        if x == x and x not in (math.inf, -math.inf) and x == int(x) and abs(x) <= MAXSAFE:
            return int(x)
        return x
    if isinstance(x, int) and not isinstance(x, bool) and abs(x) > MAXSAFE:
        return float(x)
    return x


def is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def num_str(x):
    if isinstance(x, int):
        return str(x)
    if x != x:
        return "NaN"
    if x in (math.inf, -math.inf):
        return "Infinity" if x > 0 else "-Infinity"
    if x == int(x) and abs(x) < 1e21:
        return str(int(x))
    r = repr(x)
    if "e" in r:
        m, e = r.split("e")
        e = int(e)
        return "%se%s%d" % (m, "+" if e >= 0 else "-", abs(e))
    return r


class JSInterp:
    def __init__(self, files, budget=None):
        self.files = files
        self.budget = budget or Budget()
        self.modules = {}
        self.parsed = {}
        self.depth = 0
        self.tests = []
        self.exit_handlers = []
        self.exit_code = None
        self.global_env = Env(None, True)
        self._init_globals()

    # ------------------------------------------------------------------ globals
    def _init_globals(self):
        g = self.global_env
        self.Error = {}
        for nm, par in (("Error", None), ("TypeError", "Error"), ("RangeError", "Error"), ("ReferenceError", "Error"),
                        ("SyntaxError", "Error"), ("EvalError", "Error"), ("URIError", "Error")):
            c = JSClass(nm, self.Error[par] if par else None, None, {}, {}, [], g, self, native=nm)
            self.Error[nm] = c
            g.declare(nm, c)
        self.AssertionError = JSClass("AssertionError", self.Error["Error"], None, {}, {}, [], g, self, native="AssertionError")
        math_o = JSObj()
        N = lambda f, nm="": Native(f, nm)

        def mfn(f):
            return Native(lambda this, a: norm(f(*[self.to_num(x) for x in a])))
        math_o.props.update({
            "min": Native(lambda this, a: self._minmax(a, min)), "max": Native(lambda this, a: self._minmax(a, max)),
            "abs": mfn(abs), "trunc": mfn(lambda x: x if x != x or x in (math.inf, -math.inf) else self._sz(math.trunc(x), x)),
            "floor": mfn(lambda x: x if x != x or x in (math.inf, -math.inf) else math.floor(x)),
            "ceil": mfn(lambda x: x if x != x or x in (math.inf, -math.inf) else self._sz(math.ceil(x), x)),
            "round": mfn(lambda x: x if x != x or x in (math.inf, -math.inf) else self._sz(math.floor(x + 0.5), x)),
            "sqrt": mfn(lambda x: math.sqrt(x) if x >= 0 else math.nan), "pow": mfn(lambda a, b: self._pow(a, b)),
            "sign": mfn(lambda x: (x > 0) - (x < 0) if x == x else x)})
        g.declare("Math", math_o)
        g.declare("String", Native(lambda this, a: self.to_str(a[0]) if a else ""))
        g.declare("Number", Native(lambda this, a: self.to_num(a[0]) if a else 0))
        g.declare("Boolean", Native(lambda this, a: self.truthy(a[0]) if a else False))
        g.declare("parseInt", Native(lambda this, a: self._parse_int(a)))
        g.declare("isNaN", Native(lambda this, a: (lambda x: x != x)(self.to_num(a[0]))))
        g.declare("NaN", math.nan)
        g.declare("Infinity", math.inf)
        arr = JSObj()
        arr.props["isArray"] = Native(lambda this, a: isinstance(a[0], list))
        g.declare("Array", arr)
        num = JSObj()
        num.props["isInteger"] = Native(lambda this, a: is_num(a[0]) and a[0] == a[0] and a[0] not in (math.inf, -math.inf) and a[0] == int(a[0]))
        num.props["MAX_SAFE_INTEGER"] = MAXSAFE
        g.declare("Number", Native(lambda this, a: self.to_num(a[0]) if a else 0))
        self.number_ns = num
        proc = JSObj()
        proc.props["on"] = Native(lambda this, a: self._proc_on(a))
        proc.props["exit"] = Native(lambda this, a: self._proc_exit(a))
        proc.props["argv"] = []
        proc.props["env"] = JSObj()
        self.process = proc
        g.declare("process", proc)
        g.declare("globalThis", JSObj())
        con = JSObj()
        con.props["log"] = Native(lambda this, a: UNDEF)
        con.props["error"] = Native(lambda this, a: UNDEF)
        g.declare("console", con)
        self.assert_obj = self._make_assert()
        self.test_fn = self._make_test()

    def _proc_on(self, a):
        if a and a[0] == "exit":
            self.exit_handlers.append(a[1])
        return UNDEF

    def _proc_exit(self, a):
        raise _ProcessExit(self.to_num(a[0]) if a else 0)

    @staticmethod
    def _sz(r, x):
        """Result r of trunc/ceil/round of x: a zero result keeps the sign of x (JS -0)."""
        return -0.0 if r == 0 and neg(x) else r

    @staticmethod
    def _pow(a, b):
        try:
            return a ** b
        except (OverflowError, ZeroDivisionError):
            return math.inf

    def _minmax(self, a, f):
        if not a:
            return math.inf if f is min else -math.inf
        vals = [self.to_num(x) for x in a]
        if any(v != v for v in vals):
            return math.nan
        return norm(f(vals))

    def _parse_int(self, a):
        s = self.to_str(a[0]).strip()
        base = int(self.to_num(a[1])) if len(a) > 1 else 10
        m = re.match(r"[+-]?[0-9a-zA-Z]+", s)
        if not m:
            return math.nan
        txt = m.group(0)
        out = ""
        for i, ch in enumerate(txt):
            if i == 0 and ch in "+-":
                out += ch
                continue
            try:
                int(ch, base)
                out += ch
            except ValueError:
                break
        try:
            return int(out, base)
        except ValueError:
            return math.nan

    # ------------------------------------------------------------------ conversions
    def typeof(self, v):
        if v is UNDEF:
            return "undefined"
        if v is None:
            return "object"
        if isinstance(v, bool):
            return "boolean"
        if is_num(v):
            return "number"
        if isinstance(v, str):
            return "string"
        if isinstance(v, (JSFunc, Native, JSClass)):
            return "function"
        return "object"

    def truthy(self, v):
        if v is UNDEF or v is None or v is False:
            return False
        if isinstance(v, bool):
            return v
        if is_num(v):
            return v == v and v != 0
        if isinstance(v, str):
            return v != ""
        return True

    def to_str(self, v):
        if isinstance(v, str):
            return v
        if v is UNDEF:
            return "undefined"
        if v is None:
            return "null"
        if v is True:
            return "true"
        if v is False:
            return "false"
        if is_num(v):
            return num_str(v)
        if isinstance(v, list):
            return ",".join("" if (x is None or x is UNDEF) else self.to_str(x) for x in v)
        if isinstance(v, JSObj):
            if v.cls is not None and self._is_error(v):
                msg = v.props.get("message", "")
                nm = v.cls.name
                return nm + (": " + self.to_str(msg) if msg != "" else "")
            return "[object Object]"
        if isinstance(v, (JSFunc, Native, JSClass)):
            return "function"
        raise Unsupported("to_str")

    def _is_error(self, o):
        return o.cls is not None and any(c is self.Error["Error"] or c is self.AssertionError for c in o.cls.chain())

    def to_num(self, v):
        if is_num(v):
            return v
        if isinstance(v, bool):
            return int(v)
        if v is None:
            return 0
        if v is UNDEF:
            return math.nan
        if isinstance(v, str):
            s = v.strip()
            if s == "":
                return 0
            try:
                if re.fullmatch(r"[+-]?\d+", s):
                    return norm(int(s))
                if s[:2] in ("0x", "0X"):
                    return norm(int(s, 16))
                return norm(float(s)) if re.fullmatch(r"[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?|[+-]?Infinity", s) else math.nan
            except ValueError:
                return math.nan
        if isinstance(v, list):
            if not v:
                return 0
            if len(v) == 1:
                return self.to_num(self.to_str(v[0]))
            return math.nan
        return math.nan

    def strict_eq(self, a, b):
        if is_num(a) and is_num(b):
            return a == b
        if isinstance(a, bool) or isinstance(b, bool):
            return isinstance(a, bool) and isinstance(b, bool) and a == b
        if isinstance(a, str) and isinstance(b, str):
            return a == b
        if a is None or b is None or a is UNDEF or b is UNDEF:
            return a is b
        return a is b

    def loose_eq(self, a, b):
        if (a is None or a is UNDEF) and (b is None or b is UNDEF):
            return True
        if a is None or a is UNDEF or b is None or b is UNDEF:
            return False
        if type(a) is type(b) or (is_num(a) and is_num(b)):
            return self.strict_eq(a, b)
        if isinstance(a, (list, JSObj)) or isinstance(b, (list, JSObj)):
            if isinstance(a, (list, JSObj)) and isinstance(b, (list, JSObj)):
                return a is b
            return self.loose_eq(self.to_str(a) if isinstance(a, (list, JSObj)) else a, self.to_str(b) if isinstance(b, (list, JSObj)) else b)
        return self.to_num(a) == self.to_num(b)

    def deep_strict_equal(self, a, b):
        if isinstance(a, list) and isinstance(b, list):
            return len(a) == len(b) and all(self.deep_strict_equal(x, y) for x, y in zip(a, b))
        if isinstance(a, JSObj) and isinstance(b, JSObj):
            if a.cls is not b.cls or set(a.props) != set(b.props):
                return False
            return all(self.deep_strict_equal(a.props[k], b.props[k]) for k in a.props)
        if is_num(a) and is_num(b):
            if a != a and b != b:
                return True
            return a == b and (math.copysign(1, a) == math.copysign(1, b))
        return type(a) is type(b) and a == b if not (a is UNDEF or b is UNDEF) else a is b

    # ------------------------------------------------------------------ errors
    def make_error(self, cname, msg=""):
        cls = self.Error[cname]
        o = JSObj(cls)
        o.props["message"] = msg
        return JSThrow(o)

    def throw_name(self, val):
        if isinstance(val, JSObj) and val.cls is not None:
            return val.cls.name
        raise Unsupported("thrown non-object")

    # ------------------------------------------------------------------ modules
    def resolve(self, from_path, spec):
        base = from_path.rsplit("/", 1)[0] if "/" in from_path else ""
        p = spec
        if p.startswith("./") or p.startswith("../"):
            parts = (base + "/" + p if base else p).split("/")
            out = []
            for s in parts:
                if s in ("", "."):
                    continue
                if s == "..":
                    out.pop()
                else:
                    out.append(s)
            p = "/".join(out)
        for cand in (p, p + ".js", p + ".mts", p + ".ts", p + ".mjs", p + ".cjs", p + "/index.js"):
            if cand in self.files:
                return cand
        raise Unsupported("cannot resolve %s from %s" % (spec, from_path))

    def builtin_module(self, spec):
        if spec in ("node:test", "test"):
            return self.test_fn
        if spec in ("node:assert/strict", "node:assert", "assert", "assert/strict"):
            return self.assert_obj
        raise Unsupported("module " + spec)

    def load(self, path):
        if path in self.modules:
            return self.modules[path][1]
        if path not in self.files:
            raise Unsupported("no file " + path)
        if path not in self.parsed:
            self.parsed[path] = Parser(self.files[path]).parse_program()
        env = Env(self.global_env, True)
        exports = JSObj()
        module = JSObj()
        module.props["exports"] = exports
        env.declare("module", module)
        env.declare("exports", exports)
        env.declare("require", Native(lambda this, a, p=path: self._require(p, a[0])))
        env.declare("__filename", path)
        info = (env, module)
        self.modules[path] = (path, module, env)
        body = self.parsed[path]
        self.hoist(body, env)
        for st in body:
            self.exec_stmt(st, env, path)
        return module

    def _require(self, frm, spec):
        if spec.startswith("node:") or not spec.startswith("."):
            return self.builtin_module(spec)
        return self.load(self.resolve(frm, spec)).props["exports"]

    # ------------------------------------------------------------------ statements
    def hoist(self, body, env):
        for st in body:
            if st[0] == "funcdecl":
                env.declare(st[1], JSFunc(st[2], env, self))
            elif st[0] == "export" and st[1] is not None and st[1][0] == "funcdecl":
                env.declare(st[1][1], JSFunc(st[1][2], env, self))

    def exec_block(self, body, env, path=None):
        for st in body:
            self.exec_stmt(st, env, path)

    def exec_stmt(self, st, env, path=None):
        self.budget.tick()
        k = st[0]
        m = getattr(self, "x_" + k, None)
        if m is None:
            raise Unsupported("stmt " + k)
        m(st, env, path)

    def x_expr(self, st, env, path):
        self.ev(st[1], env)

    def x_block(self, st, env, path):
        e = Env(env)
        self.hoist(st[1], e)
        self.exec_block(st[1], e, path)

    def x_funcdecl(self, st, env, path):
        pass                                             # hoisted

    def x_classdecl(self, st, env, path):
        env.declare(st[1], self.make_class(st[2], env))

    def x_var(self, st, env, path):
        kind = st[1]
        target_env = env
        if kind == "var":
            while not target_env.func and target_env.parent is not None:
                target_env = target_env.parent
        for tgt, init in st[2]:
            v = self.ev(init, env) if init is not None else UNDEF
            self.bind(tgt, v, target_env, kind == "const")

    def bind(self, tgt, v, env, const=False):
        if isinstance(tgt, str):
            env.declare(tgt, v, const)
            return
        if tgt[0] == "objpat":
            if v is None or v is UNDEF:
                raise self.make_error("TypeError", "Cannot destructure")
            used = []
            for key, t, default in tgt[1]:
                if key == "rest":
                    raise Unsupported("rest pattern")
                x = self.get(v, key)
                if x is UNDEF and default is not None:
                    x = self.ev(default, env)
                self.bind(t, x, env, const)
            return
        if tgt[0] == "arrpat":
            lst = list(v) if isinstance(v, list) else None
            if lst is None:
                raise Unsupported("array pattern on non-array")
            for i, el in enumerate(tgt[1]):
                if el is None:
                    continue
                t, default = el
                x = lst[i] if i < len(lst) else UNDEF
                if x is UNDEF and default is not None:
                    x = self.ev(default, env)
                self.bind(t, x, env, const)
            return
        raise Unsupported("binding")

    def x_if(self, st, env, path):
        if self.truthy(self.ev(st[1], env)):
            self.exec_stmt(st[2], env, path) if st[2] is not None else None
        elif st[3] is not None:
            self.exec_stmt(st[3], env, path)

    def x_while(self, st, env, path):
        while self.truthy(self.ev(st[1], env)):
            self.budget.tick()
            try:
                self.exec_stmt(st[2], env, path)
            except _Brk:
                break
            except _Cnt:
                continue

    def x_dowhile(self, st, env, path):
        while True:
            self.budget.tick()
            try:
                self.exec_stmt(st[1], env, path)
            except _Brk:
                break
            except _Cnt:
                pass
            if not self.truthy(self.ev(st[2], env)):
                break

    def x_for(self, st, env, path):
        _, init, cond, upd, body = st
        loop = Env(env)
        names = []
        if init is not None:
            self.exec_stmt(init, loop, path)
            if init[0] == "var" and init[1] != "var":
                names = [t for t, _ in init[2] if isinstance(t, str)]
        while True:
            self.budget.tick()
            if cond is not None and not self.truthy(self.ev(cond, loop)):
                break
            it = Env(loop)
            for nm in names:
                it.vars[nm] = loop.vars[nm]
            try:
                self.exec_stmt(body, it, path)
            except _Brk:
                break
            except _Cnt:
                pass
            for nm in names:
                loop.vars[nm] = it.vars[nm]
            if upd is not None:
                self.ev(upd, loop)

    def x_forof(self, st, env, path):
        _, kind, tgt, itx, body = st
        it = self.ev(itx, env)
        if isinstance(it, str):
            seq = list(it)
        elif isinstance(it, list):
            seq = list(it)
        else:
            raise Unsupported("for-of over non-iterable")
        for v in seq:
            self.budget.tick()
            e = Env(env)
            self.bind(tgt, v, e, kind == "const")
            try:
                self.exec_stmt(body, e, path)
            except _Brk:
                break
            except _Cnt:
                continue

    def x_forin(self, st, env, path):
        _, kind, tgt, itx, body = st
        it = self.ev(itx, env)
        if isinstance(it, list):
            keys = [str(i) for i in range(len(it))]
        elif isinstance(it, JSObj):
            keys = list(it.props)
        else:
            raise Unsupported("for-in")
        for k in keys:
            e = Env(env)
            self.bind(tgt, k, e)
            try:
                self.exec_stmt(body, e, path)
            except _Brk:
                break
            except _Cnt:
                continue

    def x_return(self, st, env, path):
        raise _Ret(self.ev(st[1], env) if st[1] is not None else UNDEF)

    def x_throw(self, st, env, path):
        raise JSThrow(self.ev(st[1], env))

    def x_break(self, st, env, path):
        raise _Brk()

    def x_continue(self, st, env, path):
        raise _Cnt()

    def x_try(self, st, env, path):
        _, b, param, h, f = st
        try:
            try:
                self.exec_stmt(b, env, path)
            except JSThrow as e:
                if h is None:
                    raise
                ce = Env(env)
                if param:
                    ce.declare(param, e.value)
                self.exec_stmt(h, ce, path)
            except RecursionError:
                if h is None:
                    raise
                ce = Env(env)
                if param:
                    ce.declare(param, self.make_error("RangeError", "Maximum call stack size exceeded").value)
                self.exec_stmt(h, ce, path)
        finally:
            if f is not None:
                self.exec_stmt(f, env, path)

    def x_switch(self, st, env, path):
        d = self.ev(st[1], env)
        e = Env(env)
        matched = False
        try:
            for t, body in st[2]:
                if not matched and (t is None or self.strict_eq(d, self.ev(t, e))):
                    matched = True
                if matched:
                    self.exec_block(body, e, path)
            if not matched:
                dflt = False
                for t, body in st[2]:
                    if t is None:
                        dflt = True
                    if dflt:
                        self.exec_block(body, e, path)
        except _Brk:
            pass

    def x_import(self, st, env, path):
        _, default, named, star, src = st
        if src.startswith("node:") or not src.startswith("."):
            mod = self.builtin_module(src)
            if default:
                env.declare(default, mod)
            for nm, al in named:
                env.declare(al, self.get(mod, nm))
            if star:
                env.declare(star, mod)
            return
        m = self.load(self.resolve(path, src))
        ex = m.props["exports"]
        if default:
            env.declare(default, ex.props.get("default", ex))
        for nm, al in named:
            if nm not in ex.props:
                raise Unsupported("missing export %s" % nm)
            env.declare(al, ex.props[nm])
        if star:
            env.declare(star, ex)

    def _export_set(self, env, name, v):
        mod = env.vars.get("module")
        mod.props["exports"].props[name] = v

    def x_export(self, st, env, path):
        inner = st[1]
        if inner is None:
            return
        if inner[0] == "funcdecl":
            self._export_set(self._mod_env(env), inner[1], env.vars[inner[1]])
        else:
            self.exec_stmt(inner, env, path)
            if inner[0] == "classdecl":
                self._export_set(self._mod_env(env), inner[1], env.vars[inner[1]])
            elif inner[0] == "var":
                for t, _ in inner[2]:
                    if isinstance(t, str):
                        self._export_set(self._mod_env(env), t, env.vars[t])
                    else:
                        raise Unsupported("export destructuring")

    def _mod_env(self, env):
        e = env
        while e is not None and "module" not in e.vars:
            e = e.parent
        return e

    def x_exportnames(self, st, env, path):
        for nm, al in st[1]:
            self._export_set(self._mod_env(env), al, self.lookup(nm, env))

    def x_exportdefault(self, st, env, path):
        self._export_set(self._mod_env(env), "default", self.ev(st[1], env))

    # ------------------------------------------------------------------ classes and functions
    def make_class(self, node, env):
        _, name, parent_e, members = node
        parent = self.ev(parent_e, env) if parent_e is not None else None
        if parent is not None and not isinstance(parent, JSClass):
            raise Unsupported("class parent")
        ctor, methods, statics, fields = None, {}, {}, []
        cenv = Env(env)
        for m in members:
            if m[0] == "method":
                fnode = m[2]
                if m[1] == "constructor":
                    ctor = fnode
                elif m[3]:
                    statics[m[1]] = JSFunc(fnode, cenv, self)
                else:
                    methods[m[1]] = JSFunc(fnode, cenv, self)
            else:
                if m[3]:
                    statics[m[1]] = self.ev(m[2], cenv) if m[2] is not None else UNDEF
                else:
                    fields.append((m[1], m[2]))
        c = JSClass(name, parent, ctor, methods, statics, fields, cenv, self)
        if name:
            cenv.declare(name, c)
        return c

    def construct(self, cls, args):
        if cls.native:
            o = JSObj(cls)
            if cls.native in self.Error or cls.native == "AssertionError":
                o.props["message"] = self.to_str(args[0]) if args and args[0] is not UNDEF else ""
            return o
        o = JSObj(cls)
        self._run_ctor(cls, o, args)
        return o

    def _init_fields(self, cls, o):
        for nm, init in cls.fields:
            o.props[nm] = self.ev(init, cls.env) if init is not None else UNDEF

    def _run_ctor(self, cls, o, args):
        if cls.native:
            if cls.native in self.Error or cls.native == "AssertionError":
                o.props["message"] = self.to_str(args[0]) if args and args[0] is not UNDEF else ""
            return
        if cls.ctor is None:
            if cls.parent is not None:
                self._run_ctor(cls.parent, o, args)
            self._init_fields(cls, o)
            return
        if cls.parent is None:
            self._init_fields(cls, o)
        self.call_func(JSFunc(cls.ctor, cls.env, self), o, args, ctor_cls=cls)

    def call(self, f, this, args):
        if isinstance(f, JSFunc):
            return self.call_func(f, this, args)
        if isinstance(f, Native):
            return f.fn(this, args)
        if isinstance(f, JSClass):
            raise self.make_error("TypeError", "Class constructor cannot be invoked without 'new'")
        raise self.make_error("TypeError", "%s is not a function" % self.typeof(f))

    def call_func(self, f, this, args, ctor_cls=None):
        if self.depth > 90:
            raise self.make_error("RangeError", "Maximum call stack size exceeded")
        node = f.node
        env = Env(f.env, True)
        if f.arrow:
            env.vars["__this__"] = f.this
        else:
            env.vars["__this__"] = this
        if ctor_cls is not None:
            env.vars["__ctor__"] = ctor_cls
        ps = node[2]
        for i, p in enumerate(ps):
            if p[0] == "rest":
                env.declare(p[1], list(args[i:]))
                break
            v = args[i] if i < len(args) else UNDEF
            if v is UNDEF and p[2] is not None:
                v = self.ev(p[2], env)
            self.bind(p[1], v, env)
        body = node[3]
        self.depth += 1
        try:
            if node[0] == "arrowexpr":
                return self.ev(body, env)
            self.hoist(body[1], env)
            try:
                self.exec_block(body[1], env)
            except _Ret as r:
                return r.v
            return UNDEF
        finally:
            self.depth -= 1

    # ------------------------------------------------------------------ expressions
    def lookup(self, name, env):
        e = env.find(name)
        if e is None:
            raise self.make_error("ReferenceError", "%s is not defined" % name)
        return e.vars[name]

    def get_this(self, env):
        e = env
        while e is not None:
            if "__this__" in e.vars:
                return e.vars["__this__"]
            e = e.parent
        return UNDEF

    def ev(self, n, env):
        self.budget.tick()
        m = getattr(self, "n_" + n[0], None)
        if m is None:
            raise Unsupported("expr " + n[0])
        return m(n, env)

    def n_num(self, n, env):
        return n[1]

    def n_str(self, n, env):
        return n[1]

    def n_lit(self, n, env):
        return n[1]

    def n_id(self, n, env):
        if n[1] == "undefined":
            return UNDEF
        return self.lookup(n[1], env)

    def n_this(self, n, env):
        return self.get_this(env)

    def n_tmpl(self, n, env):
        return "".join(p[1] if p[0] == "s" else self.to_str(self.ev(p[1], env)) for p in n[1])

    def n_array(self, n, env):
        out = []
        for e in n[1]:
            if e[0] == "spread":
                v = self.ev(e[1], env)
                out.extend(list(v) if isinstance(v, (list, str)) else self._bad_spread())
            else:
                out.append(self.ev(e, env))
        return out

    def _bad_spread(self):
        raise Unsupported("spread of non-iterable")

    def n_object(self, n, env):
        o = JSObj()
        for p in n[1]:
            if p[0] == "spread":
                v = self.ev(p[1], env)
                if isinstance(v, JSObj):
                    o.props.update(v.props)
                continue
            k = p[1]
            key = k[1] if k[0] == "const" else self.to_str(self.ev(k[1], env))
            o.props[str(key) if not isinstance(key, str) else key] = self.ev(p[2], env)
        return o

    def n_funcexpr(self, n, env):
        f = JSFunc(n[1], env, self)
        if n[1][1]:
            e = Env(env)
            e.declare(n[1][1], f)
            f.env = e
        return f

    def n_classexpr(self, n, env):
        return self.make_class(n[1], env)

    def n_arrow(self, n, env):
        _, ps, body, is_block = n
        if is_block:
            node = ("func", None, ps, body, True)
        else:
            node = ("arrowexpr", None, ps, body, True)
        return JSFunc(node, env, self, this=self.get_this(env), arrow=True)

    def n_seq(self, n, env):
        v = UNDEF
        for e in n[1]:
            v = self.ev(e, env)
        return v

    def n_cond(self, n, env):
        return self.ev(n[2] if self.truthy(self.ev(n[1], env)) else n[3], env)

    def n_logic(self, n, env):
        op = n[1]
        a = self.ev(n[2], env)
        if op == "&&":
            return self.ev(n[3], env) if self.truthy(a) else a
        if op == "||":
            return a if self.truthy(a) else self.ev(n[3], env)
        return self.ev(n[3], env) if (a is None or a is UNDEF) else a

    def n_unary(self, n, env):
        op = n[1]
        if op == "typeof":
            if n[2][0] == "id" and env.find(n[2][1]) is None:
                return "undefined"
            return self.typeof(self.ev(n[2], env))
        if op == "delete":
            t = n[2]
            if t[0] == "member":
                o = self.ev(t[1], env)
                if isinstance(o, JSObj):
                    o.props.pop(t[2], None)
                return True
            raise Unsupported("delete target")
        v = self.ev(n[2], env)
        if op == "!":
            return not self.truthy(v)
        if op == "-":
            x = self.to_num(v)
            if x == 0:
                return 0 if neg(x) else -0.0
            return norm(-x)
        if op == "+":
            return self.to_num(v)
        if op == "~":
            return ~self._i32(self.to_num(v))
        if op == "void":
            return UNDEF
        raise Unsupported("unary " + op)

    @staticmethod
    def _i32(x):
        if x != x or x in (math.inf, -math.inf):
            return 0
        x = int(x) & 0xFFFFFFFF
        return x - 0x100000000 if x >= 0x80000000 else x

    def n_bin(self, n, env):
        op = n[1]
        a = self.ev(n[2], env)
        b = self.ev(n[3], env)
        return self.binop(op, a, b)

    def binop(self, op, a, b):
        if op == "+":
            if isinstance(a, (list, JSObj)):
                a = self.to_str(a)
            if isinstance(b, (list, JSObj)):
                b = self.to_str(b)
            if isinstance(a, str) or isinstance(b, str):
                return self.to_str(a) + self.to_str(b)
            return self._arith("+", self.to_num(a), self.to_num(b))
        if op in ("-", "*", "/", "%", "**"):
            return self._arith(op, self.to_num(a), self.to_num(b))
        if op == "===":
            return self.strict_eq(a, b)
        if op == "!==":
            return not self.strict_eq(a, b)
        if op == "==":
            return self.loose_eq(a, b)
        if op == "!=":
            return not self.loose_eq(a, b)
        if op in ("<", ">", "<=", ">="):
            if isinstance(a, str) and isinstance(b, str):
                x, y = a, b
            else:
                x, y = self.to_num(a), self.to_num(b)
                if x != x or y != y:
                    return False
            return {"<": x < y, ">": x > y, "<=": x <= y, ">=": x >= y}[op]
        if op == "instanceof":
            if not isinstance(b, JSClass):
                raise self.make_error("TypeError", "Right-hand side of 'instanceof' is not callable")
            return isinstance(a, JSObj) and a.cls is not None and any(c is b for c in a.cls.chain())
        if op == "in":
            if isinstance(b, JSObj):
                return self.to_str(a) in b.props
            if isinstance(b, list):
                return is_num(a) and 0 <= a < len(b)
            raise self.make_error("TypeError", "Cannot use 'in'")
        if op in ("&", "|", "^", "<<", ">>", ">>>"):
            x, y = self._i32(self.to_num(a)), self._i32(self.to_num(b))
            if op == "&":
                return x & y
            if op == "|":
                return x | y
            if op == "^":
                return x ^ y
            if op == "<<":
                return self._i32(x << (y & 31))
            if op == ">>":
                return x >> (y & 31)
            return (x & 0xFFFFFFFF) >> (y & 31)
        raise Unsupported("binop " + op)

    def _arith(self, op, x, y):
        if op == "+":
            return norm(x + y)
        if op == "-":
            return norm(x - y)
        if op == "*":
            r = norm(x * y)
            if r == 0 and not (isinstance(r, float) and math.copysign(1, r) < 0) and neg(x) != neg(y) and x == x and y == y:
                return -0.0
            return r
        if op == "/":
            if x == 0 and y != 0 and y == y and x == x:
                return -0.0 if neg(x) != neg(y) else 0
            if y == 0:
                if x != x or x == 0:
                    return math.nan
                negative = (x < 0) != (math.copysign(1, y) < 0) if isinstance(y, float) else (x < 0)
                return -math.inf if negative else math.inf
            return norm(x / y)
        if op == "%":
            if y == 0 or x != x or y != y or x in (math.inf, -math.inf):
                return math.nan
            if y in (math.inf, -math.inf):
                return x
            if isinstance(x, int) and isinstance(y, int):
                r = abs(x) % abs(y)
                if r == 0:
                    return -0.0 if x < 0 else 0
                return -r if x < 0 else r
            r = math.fmod(x, y)
            if r == 0 and neg(x):
                return -0.0
            return norm(r)
        if op == "**":
            try:
                return norm(x ** y)
            except OverflowError:
                return math.inf
            except ZeroDivisionError:
                return math.inf
        raise Unsupported(op)

    def n_update(self, n, env):
        _, op, prefix, t = n
        old = self.to_num(self.ev(t, env))
        new = norm(old + 1 if op == "++" else old - 1)
        self.store(t, new, env)
        return new if prefix else old

    def n_assign(self, n, env):
        _, op, t, r = n
        if op == "=":
            v = self.ev(r, env)
            self.store(t, v, env)
            return v
        if op in ("&&=", "||=", "??="):
            cur = self.ev(t, env)
            if (op == "&&=" and self.truthy(cur)) or (op == "||=" and not self.truthy(cur)) or (op == "??=" and (cur is None or cur is UNDEF)):
                v = self.ev(r, env)
                self.store(t, v, env)
                return v
            return cur
        cur = self.ev(t, env)
        v = self.binop(op[:-1], cur, self.ev(r, env))
        self.store(t, v, env)
        return v

    def store(self, t, v, env):
        if t[0] == "id":
            e = env.find(t[1])
            if e is None:
                raise self.make_error("ReferenceError", "%s is not defined" % t[1])
            if t[1] in e.consts:
                raise self.make_error("TypeError", "Assignment to constant variable.")
            e.vars[t[1]] = v
        elif t[0] == "member":
            o = self.ev(t[1], env)
            self.put(o, t[2], v)
        elif t[0] == "index":
            o = self.ev(t[1], env)
            k = self.ev(t[2], env)
            if isinstance(o, list):
                if not is_num(k) or k != int(k) or k < 0:
                    raise Unsupported("array store at non-index")
                k = int(k)
                if k > len(o):
                    raise Unsupported("array hole")
                if k == len(o):
                    o.append(v)
                else:
                    o[k] = v
            else:
                self.put(o, self.to_str(k), v)
        else:
            raise Unsupported("store target")

    def put(self, o, name, v):
        if isinstance(o, (JSObj, JSFunc, Native)):
            o.props[name] = v
        elif isinstance(o, JSClass):
            o.statics[name] = v
        elif o is None or o is UNDEF:
            raise self.make_error("TypeError", "Cannot set properties of %s" % self.to_str(o))
        else:
            raise Unsupported("property store on primitive")

    def n_member(self, n, env):
        if n[1][0] == "super":
            raise Unsupported("super.member")
        return self.get(self.ev(n[1], env), n[2])

    def n_index(self, n, env):
        o = self.ev(n[1], env)
        k = self.ev(n[2], env)
        if isinstance(o, (list, str)):
            if is_num(k):
                if k == k and k not in (math.inf, -math.inf) and k == int(k) and 0 <= k < len(o):
                    return o[int(k)]
                return UNDEF
            return self.get(o, self.to_str(k))
        return self.get(o, self.to_str(k))

    def n_super(self, n, env):
        raise Unsupported("bare super")

    def n_spread(self, n, env):
        raise Unsupported("spread")

    def n_new(self, n, env):
        cls = self.ev(n[1], env)
        args = self.eval_args(n[2], env)
        if isinstance(cls, JSClass):
            return self.construct(cls, args)
        if isinstance(cls, Native):
            nm = cls.name
            raise Unsupported("new on native " + nm)
        raise self.make_error("TypeError", "not a constructor")

    def eval_args(self, args, env):
        out = []
        for a in args:
            if a[0] == "spread":
                v = self.ev(a[1], env)
                out.extend(list(v) if isinstance(v, (list, str)) else self._bad_spread())
            else:
                out.append(self.ev(a, env))
        return out

    def n_call(self, n, env):
        callee = n[1]
        if callee[0] == "super":
            ctor = env
            cls = None
            e = env
            while e is not None:
                if "__ctor__" in e.vars:
                    cls = e.vars["__ctor__"]
                    break
                e = e.parent
            if cls is None or cls.parent is None:
                raise Unsupported("super() outside derived constructor")
            this = self.get_this(env)
            self._run_ctor(cls.parent, this, self.eval_args(n[2], env))
            self._init_fields(cls, this)
            return UNDEF
        if callee[0] == "member":
            if callee[1][0] == "super":
                raise Unsupported("super.method")
            this = self.ev(callee[1], env)
            f = self.get(this, callee[2])
            return self.call(f, this, self.eval_args(n[2], env))
        if callee[0] == "index":
            this = self.ev(callee[1], env)
            f = self.n_index(callee, env) if False else self.get(this, self.to_str(self.ev(callee[2], env)))
            return self.call(f, this, self.eval_args(n[2], env))
        f = self.ev(callee, env)
        return self.call(f, UNDEF, self.eval_args(n[2], env))

    # ------------------------------------------------------------------ property access
    def get(self, o, name):
        if isinstance(o, JSObj):
            if name in o.props:
                return o.props[name]
            if name == "constructor" and o.cls is not None:
                return o.cls
            if o.cls is not None:
                m = o.cls.find_method(name)
                if m is not None:
                    return JSFunc(m.node, m.env, self, this=o, arrow=False) if False else _BoundJS(m, o)
                if name == "name" and self._is_error(o):
                    return o.cls.name
            return UNDEF
        if isinstance(o, JSClass):
            if name == "name":
                return o.name
            for c in o.chain():
                if name in c.statics:
                    return c.statics[name]
            return UNDEF
        if isinstance(o, str):
            return self._str_get(o, name)
        if isinstance(o, list):
            return self._arr_get(o, name)
        if is_num(o) and not isinstance(o, bool):
            if name == "toString":
                return Native(lambda this, a: num_str(o) if not a else self._radix(o, int(a[0])))
            if name == "toFixed":
                return Native(lambda this, a: format(float(o), ".%df" % int(a[0] if a else 0)))
            return UNDEF
        if isinstance(o, (JSFunc, Native)):
            if name in o.props:
                return o.props[name]
            return UNDEF
        if o is None or o is UNDEF:
            raise self.make_error("TypeError", "Cannot read properties of %s (reading '%s')" % (self.to_str(o), name))
        if isinstance(o, bool):
            return UNDEF
        raise Unsupported("get on " + type(o).__name__)

    @staticmethod
    def _radix(x, b):
        digs = "0123456789abcdefghijklmnopqrstuvwxyz"
        if x == 0:
            return "0"
        neg, x, out = x < 0, abs(int(x)), ""
        while x:
            out = digs[x % b] + out
            x //= b
        return ("-" if neg else "") + out

    def _str_get(self, s, name):
        if name == "length":
            return len(s)
        N = Native
        t = self.to_num
        if name == "startsWith":
            return N(lambda this, a: s.startswith(self.to_str(a[0]), self._int(a[1]) if len(a) > 1 else 0))
        if name == "endsWith":
            return N(lambda this, a: s.endswith(self.to_str(a[0])))
        if name == "includes":
            return N(lambda this, a: self.to_str(a[0]) in s)
        if name == "indexOf":
            return N(lambda this, a: s.find(self.to_str(a[0])))
        if name == "lastIndexOf":
            return N(lambda this, a: s.rfind(self.to_str(a[0])))
        if name == "padStart":
            return N(lambda this, a: self._pad(s, a, True))
        if name == "padEnd":
            return N(lambda this, a: self._pad(s, a, False))
        if name == "slice":
            return N(lambda this, a: s[self._sl(len(s), a)[0]:self._sl(len(s), a)[1]])
        if name == "substring":
            def sub(this, a):
                n = len(s)
                x = min(max(self._int(a[0]) if a else 0, 0), n)
                y = min(max(self._int(a[1]) if len(a) > 1 and a[1] is not UNDEF else n, 0), n)
                if x > y:
                    x, y = y, x
                return s[x:y]
            return N(sub)
        if name == "charAt":
            return N(lambda this, a: s[self._int(a[0])] if 0 <= self._int(a[0]) < len(s) else "")
        if name == "toUpperCase":
            return N(lambda this, a: s.upper())
        if name == "toLowerCase":
            return N(lambda this, a: s.lower())
        if name == "trim":
            return N(lambda this, a: s.strip())
        if name == "repeat":
            return N(lambda this, a: s * self._int(a[0]))
        if name == "concat":
            return N(lambda this, a: s + "".join(self.to_str(x) for x in a))
        if name == "split":
            def sp(this, a):
                if not a or a[0] is UNDEF:
                    return [s]
                sep = self.to_str(a[0])
                return list(s) if sep == "" else s.split(sep)
            return N(sp)
        if name == "replace":
            return N(lambda this, a: s.replace(self.to_str(a[0]), self.to_str(a[1]), 1))
        if name == "replaceAll":
            return N(lambda this, a: s.replace(self.to_str(a[0]), self.to_str(a[1])))
        if name == "toString":
            return N(lambda this, a: s)
        if name == "charCodeAt":
            return N(lambda this, a: ord(s[self._int(a[0])]) if 0 <= self._int(a[0]) < len(s) else math.nan)
        if name == "at":
            return N(lambda this, a: (s[self._int(a[0])] if -len(s) <= self._int(a[0]) < len(s) else UNDEF))
        return UNDEF

    def _pad(self, s, a, start):
        n = int(self.to_num(a[0]))
        fill = self.to_str(a[1]) if len(a) > 1 and a[1] is not UNDEF else " "
        if n <= len(s) or fill == "":
            return s
        need = n - len(s)
        pad = (fill * (need // len(fill) + 1))[:need]
        return pad + s if start else s + pad

    def _int(self, v):
        x = self.to_num(v)
        if x != x:
            return 0
        if x in (math.inf, -math.inf):
            return 10 ** 9 if x > 0 else -10 ** 9
        return int(x)

    def _sl(self, n, a):
        t = self.to_num
        x = self._int(a[0]) if a and a[0] is not UNDEF else 0
        y = self._int(a[1]) if len(a) > 1 and a[1] is not UNDEF else n
        if x < 0:
            x = max(n + x, 0)
        if y < 0:
            y = max(n + y, 0)
        return min(x, n), min(y, n)

    def _arr_get(self, l, name):
        N = Native
        t = self.to_num
        if name == "length":
            return len(l)
        if name == "push":
            def push(this, a):
                l.extend(a)
                return len(l)
            return N(push)
        if name == "pop":
            return N(lambda this, a: l.pop() if l else UNDEF)
        if name == "shift":
            return N(lambda this, a: l.pop(0) if l else UNDEF)
        if name == "unshift":
            def unshift(this, a):
                l[0:0] = a
                return len(l)
            return N(unshift)
        if name == "includes":
            return N(lambda this, a: any(self.strict_eq(x, a[0]) or (x != x and a[0] != a[0] if is_num(x) and is_num(a[0]) else False) for x in l))
        if name == "indexOf":
            def idx(this, a):
                for i, x in enumerate(l):
                    if self.strict_eq(x, a[0]):
                        return i
                return -1
            return N(idx)
        if name == "slice":
            return N(lambda this, a: l[self._sl(len(l), a)[0]:self._sl(len(l), a)[1]])
        if name == "concat":
            def concat(this, a):
                out = list(l)
                for x in a:
                    out.extend(x) if isinstance(x, list) else out.append(x)
                return out
            return N(concat)
        if name == "join":
            return N(lambda this, a: (self.to_str(a[0]) if a and a[0] is not UNDEF else ",").join(
                "" if (x is None or x is UNDEF) else self.to_str(x) for x in l))
        if name == "reverse":
            def rev(this, a):
                l.reverse()
                return l
            return N(rev)
        if name == "map":
            return N(lambda this, a: [self.call(a[0], UNDEF, [x, i, l]) for i, x in enumerate(list(l))])
        if name == "filter":
            return N(lambda this, a: [x for i, x in enumerate(list(l)) if self.truthy(self.call(a[0], UNDEF, [x, i, l]))])
        if name == "forEach":
            def fe(this, a):
                for i, x in enumerate(list(l)):
                    self.call(a[0], UNDEF, [x, i, l])
                return UNDEF
            return N(fe)
        if name == "reduce":
            def red(this, a):
                it = list(l)
                if len(a) > 1:
                    acc = a[1]
                    start = 0
                else:
                    if not it:
                        raise self.make_error("TypeError", "Reduce of empty array with no initial value")
                    acc, start = it[0], 1
                for i in range(start, len(it)):
                    acc = self.call(a[0], UNDEF, [acc, it[i], i, l])
                return acc
            return N(red)
        if name == "some":
            return N(lambda this, a: any(self.truthy(self.call(a[0], UNDEF, [x, i, l])) for i, x in enumerate(list(l))))
        if name == "every":
            return N(lambda this, a: all(self.truthy(self.call(a[0], UNDEF, [x, i, l])) for i, x in enumerate(list(l))))
        if name == "find":
            def find(this, a):
                for i, x in enumerate(list(l)):
                    if self.truthy(self.call(a[0], UNDEF, [x, i, l])):
                        return x
                return UNDEF
            return N(find)
        if name == "splice":
            def splice(this, a):
                n = len(l)
                st = self._int(a[0]) if a else 0
                if st < 0:
                    st = max(n + st, 0)
                st = min(st, n)
                dc = self._int(a[1]) if len(a) > 1 else n - st
                removed = l[st:st + dc]
                l[st:st + dc] = list(a[2:])
                return removed
            return N(splice)
        if name == "sort":
            raise Unsupported("Array.sort")
        if name == "at":
            return N(lambda this, a: (l[self._int(a[0])] if -len(l) <= self._int(a[0]) < len(l) else UNDEF))
        if name == "toString":
            return N(lambda this, a: self.to_str(l))
        return UNDEF

    # ------------------------------------------------------------------ node:assert/strict and node:test
    def _fail(self, msg="Failed"):
        o = JSObj(self.AssertionError)
        o.props["message"] = msg
        return JSThrow(o)

    def _make_assert(self):
        a = JSObj()

        def deep(this, args):
            if not self.deep_strict_equal(args[0], args[1]):
                raise self._fail("Expected values to be strictly deep-equal")
            return UNDEF

        def strict(this, args):
            if not (self.strict_eq(args[0], args[1]) or (is_num(args[0]) and is_num(args[1]) and args[0] != args[0] and args[1] != args[1])):
                raise self._fail("Expected values to be strictly equal")
            return UNDEF

        def notstrict(this, args):
            if self.strict_eq(args[0], args[1]):
                raise self._fail("Expected values to be not strictly equal")
            return UNDEF

        def notdeep(this, args):
            if self.deep_strict_equal(args[0], args[1]):
                raise self._fail("Expected values to be not deep equal")
            return UNDEF

        def ok(this, args):
            if not args or not self.truthy(args[0]):
                raise self._fail("The expression evaluated to a falsy value")
            return UNDEF

        def throws(this, args):
            try:
                self.call(args[0], UNDEF, [])
            except JSThrow as e:
                if len(args) > 1:
                    exp = args[1]
                    if isinstance(exp, JSClass):
                        v = e.value
                        if not (isinstance(v, JSObj) and v.cls is not None and any(c is exp for c in v.cls.chain())):
                            raise
                    elif isinstance(exp, (JSObj, Native, JSFunc)):
                        raise Unsupported("assert.throws validation object")
                return UNDEF
            raise self._fail("Missing expected exception.")

        def doesnt(this, args):
            self.call(args[0], UNDEF, [])
            return UNDEF

        def failf(this, args):
            raise self._fail(self.to_str(args[0]) if args else "Failed")
        a.props.update({"deepStrictEqual": Native(deep), "strictEqual": Native(strict), "equal": Native(strict),
                        "deepEqual": Native(deep), "notStrictEqual": Native(notstrict), "notEqual": Native(notstrict),
                        "notDeepStrictEqual": Native(notdeep), "ok": Native(ok), "throws": Native(throws),
                        "doesNotThrow": Native(doesnt), "fail": Native(failf)})
        return a

    def _make_test(self):
        def reg(this, args, skip=False, todo=False):
            name = args[0] if args and isinstance(args[0], str) else "<anon>"
            fn = None
            opts = None
            for x in args[1:]:
                if isinstance(x, (JSFunc, Native)):
                    fn = x
                elif isinstance(x, JSObj):
                    opts = x
            if opts is not None:
                if self.truthy(opts.props.get("skip", False)):
                    skip = True
                if self.truthy(opts.props.get("todo", False)):
                    todo = True
            if fn is None:
                raise Unsupported("test without callback")
            self.tests.append({"name": name, "fn": fn, "skip": skip, "todo": todo})
            return UNDEF
        t = Native(lambda this, a: reg(this, a))
        t.props["skip"] = Native(lambda this, a: reg(this, a, skip=True))
        t.props["todo"] = Native(lambda this, a: reg(this, a, todo=True))
        t.props["only"] = Native(lambda this, a: reg(this, a))
        t.props["default"] = t
        return t


class _ProcessExit(Exception):
    def __init__(self, code):
        Exception.__init__(self, "exit")
        self.code = code


class _BoundJS:
    """A method found on a class prototype, bound at call time (so `this` is the receiver)."""

    def __init__(self, f, this):
        self.f, self.this = f, this
        self.props = {}


# make JSInterp.call understand bound methods
_orig_call = JSInterp.call


def _call(self, f, this, args):
    if isinstance(f, _BoundJS):
        return self.call_func(f.f, f.this, args)
    return _orig_call(self, f, this, args)


JSInterp.call = _call


def js_exc_name(e):
    return e.value.cls.name if isinstance(e.value, JSObj) and e.value.cls is not None else _bad(e)


def _bad(e):
    raise Unsupported("thrown value without class")


# ------------------------------------------------------------------------------------------------ program adapter
class JsProgram:
    def __init__(self, files, budget=None):
        self.files = {p: t for p, t in files.items() if p.endswith((".js", ".mts", ".ts", ".mjs", ".cjs"))}
        self.budget = budget or Budget(30_000_000)
        self.it = JSInterp(self.files, self.budget)
        self.exports = {}
        self.classes = {}
        self.cls_of = {}
        for p in sorted(self.files):
            if ".test." in p:
                continue
            mod = self.it.load(p)
            for k, v in mod.props["exports"].props.items():
                self.exports[k] = v
        for k, v in self.exports.items():
            if isinstance(v, JSClass):
                for c in v.chain():
                    for mn in c.methods:
                        self.cls_of.setdefault(mn, v)

    def fresh(self, fn):
        if fn in self.exports and not isinstance(self.exports[fn], JSClass):
            return None
        cls = self.cls_of.get(fn)
        if cls is None:
            raise Unsupported("no callable " + fn)
        return self.it.construct(cls, [])

    def invoke(self, inst, fn, args):
        import copy
        a = copy.deepcopy(args)
        try:
            if inst is None:
                f = self.exports.get(fn)
                if f is None:
                    raise Unsupported("no export " + fn)
                r = self.it.call(f, UNDEF, a)
            else:
                f = self.it.get(inst, fn)
                r = self.it.call(f, inst, a)
            return ("ok", _plain(r))
        except JSThrow as e:
            return ("exc", js_exc_name(e))
        except (_Ret, _Brk, _Cnt):
            raise Unsupported("flow leak")


def run_js_tests(files, only=None, budget=None):
    """Model of `node --test <files>`: every matching file runs in its own interpreter (own process). Returns outcomes, exit."""
    fs = {p: t for p, t in files.items() if p.endswith((".js", ".mts", ".ts", ".mjs", ".cjs"))}
    tests = sorted(p for p in fs if ".test." in p and (only is None or p in only))
    out = {"outcomes": {}, "exit": 0, "collected": 0, "error": None}
    for tp in tests:
        it = JSInterp(fs, budget)
        failed_file = False
        try:
            it.load(tp)
        except JSThrow:
            out["outcomes"][tp + "::<load>"] = "failed"
            out["exit"] = 1
            continue
        except _ProcessExit as pe:
            out["exit"] = 1 if pe.code else out["exit"]
            continue
        for t in it.tests:
            out["collected"] += 1
            tid = tp + "::" + t["name"]
            if t["skip"]:
                out["outcomes"][tid] = "skipped"
                continue
            if t["todo"]:
                out["outcomes"][tid] = "todo"
                continue
            try:
                it.call(t["fn"], UNDEF, [UNDEF])
                out["outcomes"][tid] = "passed"
            except JSThrow:
                out["outcomes"][tid] = "failed"
                failed_file = True
            except _ProcessExit as pe:
                out["outcomes"][tid] = "passed" if not pe.code else "failed"
                break
        code = 1 if failed_file else 0
        for h in it.exit_handlers:
            try:
                it.call(h, UNDEF, [code])
            except JSThrow:
                pass
        if failed_file:
            out["exit"] = 1
    return out

"""Go renderer (one package, several files, go.mod + empty vendor/modules.txt). Text only.

Requires an IR lowered with lower_for(mod, "go", idents): no `cond` expressions, loop bounds that do not change.
"""
from . import ir as I
from . import render_base as B

GO_TYPE = {I.INT: "int", I.STR: "string", I.BOOL: "bool", I.INTS: "[]int", I.STRS: "[]string"}


def lit(value, ty):
    if ty == I.INT:
        return str(int(value))
    if ty == I.STR:
        return '"%s"' % B.check_str(value)
    if ty == I.BOOL:
        return "true" if value else "false"
    et = I.ELEM[ty]
    return GO_TYPE[ty] + "{" + ", ".join(lit(x, et) for x in value) + "}"


def ctor_name(cls_name):
    return "mk" + cls_name


class GoRender:
    def __init__(self, mod, instrument=False):
        self.mod = mod
        self.instrument = instrument
        self.cls = mod["cls"]
        self.home = B.dep_order(mod)[0]
        self.pkg = mod["meta"]["package"]
        self.imports = set()

    def e(self, node, parent=0, side="L", parent_cmp=False):
        text, prec, is_cmp = self._e(node)
        if B.need_paren(prec, parent, side, is_cmp, parent_cmp):
            return "(" + text + ")"
        return text

    def _e(self, n):
        P = B.PREC_C
        h = n[0]
        if h == "int":
            return (str(n[1]) if n[1] >= 0 else "(%d)" % n[1]), P["atom"], False
        if h == "str":
            return lit(n[1], I.STR), P["atom"], False
        if h == "bool":
            return lit(n[1], I.BOOL), P["atom"], False
        if h in ("var", "const"):
            return n[1], P["atom"], False
        if h == "field":
            return "m." + n[1], P["atom"], False
        if h == "bin":
            op = n[1]
            cls_ = B.bin_class(op)
            pr = P[cls_]
            sym = {"and": "&&", "or": "||", "++": "+", "//": "/"}.get(op, op)
            cmpop = cls_ in ("eq", "cmp")
            a = self.e(n[2], pr, "L", cmpop)
            c = self.e(n[3], pr, "R", cmpop)
            return "%s %s %s" % (a, sym, c), pr, cmpop
        if h == "not":
            return "!" + self.e(n[1], P["not"], "R"), P["not"], False
        if h in ("min", "max"):
            return "%s(%s, %s)" % (h, self.e(n[1]), self.e(n[2])), P["atom"], False
        if h == "cond":
            raise ValueError("cond must be lowered before Go rendering")
        if h == "len":
            return "len(%s)" % self.e(n[1]), P["atom"], False
        if h == "idx":
            return "%s[%s]" % (self.e(n[1], P["atom"]), self.e(n[2])), P["atom"], False
        if h == "lst":
            return lit_list(n, self), P["atom"], False
        if h == "istr":
            self.imports.add("strconv")
            return "strconv.Itoa(%s)" % self.e(n[1]), P["atom"], False
        if h == "zpad":
            self.imports.add("fmt")
            return 'fmt.Sprintf("%%0%dd", %s)' % (n[2][1], self.e(n[1])), P["atom"], False
        if h == "has":
            self.imports.add("slices")
            return "slices.Contains(%s, %s)" % (self.e(n[1]), self.e(n[2])), P["atom"], False
        if h == "starts":
            self.imports.add("strings")
            return "strings.HasPrefix(%s, %s)" % (self.e(n[1]), self.e(n[2])), P["atom"], False
        if h == "fcall":
            return "%s(%s)" % (n[1], ", ".join(self.e(a) for a in n[2])), P["atom"], False
        if h == "mcall":
            return "m.%s(%s)" % (n[1], ", ".join(self.e(a) for a in n[2])), P["atom"], False
        raise ValueError(h)

    def tgt(self, t):
        return t[1] if t[0] == "var" else "m." + t[1]

    def tick(self, ind):
        return [ind + "odN++"] if self.instrument else []

    def block(self, stmts, ind):
        out = []
        for st in stmts:
            out.extend(self.stmt(st, ind))
        return out

    def if_chain(self, st, ind, kw):
        out = ["%s%s %s {" % (ind, kw, self.e(st[1]))]
        out += self.block(st[2], ind + "\t")
        els = st[3]
        if len(els) == 1 and els[0][0] == "if" and not self.instrument:
            return out + self.if_chain(els[0], ind, "} else if")
        if els:
            out.append(ind + "} else {")
            out += self.block(els, ind + "\t")
        out.append(ind + "}")
        return out

    def stmt(self, st, ind):
        h = st[0]
        out = []
        if h not in ("for", "each"):
            out += self.tick(ind)
        if h == "let":
            out.append("%s%s := %s" % (ind, st[1], self.e(st[3])))
        elif h == "set":
            out.append("%s%s = %s" % (ind, st[1], self.e(st[2])))
        elif h == "setf":
            out.append("%sm.%s = %s" % (ind, st[1], self.e(st[2])))
        elif h == "sidx":
            out.append("%s%s[%s] = %s" % (ind, self.tgt(st[1]), self.e(st[2]), self.e(st[3])))
        elif h == "push":
            t = self.tgt(st[1])
            out.append("%s%s = append(%s, %s)" % (ind, t, t, self.e(st[2])))
        elif h == "popto":
            t = self.tgt(st[3])
            out.append("%s%s := %s[len(%s)-1]" % (ind, st[1], t, t))
            out.append("%s%s = %s[:len(%s)-1]" % (ind, t, t, t))
        elif h == "shiftto":
            t = self.tgt(st[3])
            out.append("%s%s := %s[0]" % (ind, st[1], t))
            out.append("%s%s = %s[1:]" % (ind, t, t))
        elif h == "if":
            out += self.if_chain(st, ind, "if")
        elif h == "for":
            out.append("%sfor %s := %s; %s < %s; %s++ {" % (ind, st[1], self.e(st[2]), st[1], self.e(st[3], B.PREC_C["cmp"], "R", True), st[1]))
            out += self.tick(ind + "\t")
            out += self.block(st[4], ind + "\t")
            out.append(ind + "}")
            out += self.tick(ind)
        elif h == "each":
            used = any(n[0] == "var" and n[1] == st[1] for _, n in I.walk(st[3]))
            out.append("%sfor _, %s := range %s {" % (ind, st[1] if used else "_", self.e(st[2])))
            out += self.tick(ind + "\t")
            out += self.block(st[3], ind + "\t")
            out.append(ind + "}")
            out += self.tick(ind)
        elif h == "ret":
            out.append("%sreturn %s" % (ind, self.e(st[1])))
        elif h == "raise":
            out.append("%spanic(%s{})" % (ind, B.err_marker(self.mod, st[1], "go")))
        elif h == "do":
            out.append("%s%s" % (ind, self.e(st[1])))
        else:
            raise ValueError(h)
        return out

    def func(self, f, method=False):
        params = ", ".join("%s %s" % (p[0], GO_TYPE[p[1]]) for p in f["params"])
        recv = "(m *%s) " % self.cls["name"] if method else ""
        head = "func %s%s(%s) %s {" % (recv, f["name"], params, GO_TYPE[f["ret"]])
        return [head] + self.block(f["body"], "\t") + ["}"]

    def file(self, k):
        mod = self.mod
        body = []
        for c in mod["consts"]:
            if c.get("file", 0) == k:
                body.append("var %s = %s" % (c["name"], lit(c["value"], c["type"])))
        if k == self.home:
            for e in sorted(mod["errors"]):
                body += ["", "type %s struct{}" % mod["errors"][e]["go"]]
        for f in B.funcs_in_file(mod, k):
            if f["scope"] == "free":
                body += [""] + self.func(f)
        if self.cls and self.cls["file"] == k:
            body += ["", "type %s struct {" % self.cls["name"]]
            for fl in self.cls["fields"]:
                body.append("\t%s %s" % (fl["name"], GO_TYPE[fl["type"]]))
            body.append("}")
            inits = ", ".join("%s: %s" % (fl["name"], lit(fl["init"], fl["type"])) for fl in self.cls["fields"])
            body += ["", "func %s() *%s {" % (ctor_name(self.cls["name"]), self.cls["name"]),
                     "\treturn &%s{%s}" % (self.cls["name"], inits), "}"]
            for f in B.funcs_in_file(mod, k):
                if f["scope"] == "method":
                    body += [""] + self.func(f, method=True)
        head = ["package %s" % self.pkg, ""]
        if self.imports:
            head.append("import (")
            for im in sorted(self.imports):
                head.append('\t"%s"' % im)
            head += [")", ""]
        while body and body[0] == "":
            body.pop(0)
        return "\n".join(head + body) + "\n"


def lit_list(n, r):
    return GO_TYPE[n[1]] + "{" + ", ".join(r.e(x) for x in n[2]) + "}"


def render_module(mod, instrument=False):
    """{path: text}: module files, go.mod and an empty vendor/modules.txt (-mod=vendor, GOPROXY=off)."""
    out = {}
    for k, stem in enumerate(mod["files"]):
        r = GoRender(mod, instrument)
        out[stem + ".go"] = r.file(k)
    out["go.mod"] = "module %s\n\ngo 1.26\n" % mod["meta"]["package"]
    out["vendor/modules.txt"] = ""
    if instrument:
        out["odc.go"] = "package %s\n\nvar odN int\n" % mod["meta"]["package"]
    return out


def render_function_body(mod, fn):
    r = GoRender(mod)
    return "\n".join(r.func(fn, method=fn["scope"] == "method")) + "\n"

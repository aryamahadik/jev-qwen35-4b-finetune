"""JavaScript (CommonJS, .js) and TypeScript (ESM, .mts, Node type stripping) renderer. Text only."""
from . import ir as I
from . import render_base as B

TS_TYPE = {I.INT: "number", I.STR: "string", I.BOOL: "boolean", I.INTS: "number[]", I.STRS: "string[]"}


def lit(value, ty):
    if ty == I.INT:
        return str(int(value))
    if ty == I.STR:
        return "'%s'" % B.check_str(value)
    if ty == I.BOOL:
        return "true" if value else "false"
    et = I.ELEM[ty]
    return "[" + ", ".join(lit(x, et) for x in value) + "]"


class JsRender:
    def __init__(self, mod, ts=False, instrument=False):
        self.mod = mod
        self.ts = ts
        self.lang = "typescript" if ts else "javascript"
        self.instrument = instrument
        self.cls = mod["cls"]
        self.home = B.dep_order(mod)[0]

    def fname(self, stem):
        return stem + (".mts" if self.ts else ".js")

    # ------------------------------------------------------------------ expressions
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
            return "this." + n[1], P["atom"], False
        if h == "bin":
            op = n[1]
            cls_ = B.bin_class(op)
            pr = P[cls_]
            if op == "//":
                return "Math.trunc(%s / %s)" % (self.e(n[2], P["mul"], "L"), self.e(n[3], P["mul"], "R")), P["atom"], False
            sym = {"and": "&&", "or": "||", "++": "+", "==": "===", "!=": "!=="}.get(op, op)
            cmpop = cls_ in ("eq", "cmp")
            a = self.e(n[2], pr, "L", cmpop)
            c = self.e(n[3], pr, "R", cmpop)
            return "%s %s %s" % (a, sym, c), pr, cmpop
        if h == "not":
            return "!" + self.e(n[1], P["not"], "R"), P["not"], False
        if h in ("min", "max"):
            return "Math.%s(%s, %s)" % (h, self.e(n[1]), self.e(n[2])), P["atom"], False
        if h == "cond":
            return "%s ? %s : %s" % (self.e(n[1], 1), self.e(n[2], 1), self.e(n[3], 1)), 0, False
        if h == "len":
            return "%s.length" % self.e(n[1], P["atom"]), P["atom"], False
        if h == "idx":
            return "%s[%s]" % (self.e(n[1], P["atom"]), self.e(n[2])), P["atom"], False
        if h == "lst":
            return "[" + ", ".join(self.e(x) for x in n[2]) + "]", P["atom"], False
        if h == "istr":
            return "String(%s)" % self.e(n[1]), P["atom"], False
        if h == "zpad":
            return "String(%s).padStart(%d, '0')" % (self.e(n[1]), n[2][1]), P["atom"], False
        if h == "has":
            return "%s.includes(%s)" % (self.e(n[1], P["atom"]), self.e(n[2])), P["atom"], False
        if h == "starts":
            return "%s.startsWith(%s)" % (self.e(n[1], P["atom"]), self.e(n[2])), P["atom"], False
        if h == "fcall":
            return "%s(%s)" % (n[1], ", ".join(self.e(a) for a in n[2])), P["atom"], False
        if h == "mcall":
            return "this.%s(%s)" % (n[1], ", ".join(self.e(a) for a in n[2])), P["atom"], False
        raise ValueError(h)

    def tgt(self, t):
        return t[1] if t[0] == "var" else "this." + t[1]

    def ty(self, t):
        return (": " + TS_TYPE[t]) if self.ts else ""

    # ------------------------------------------------------------------ statements
    def tick(self, ind):
        return [ind + "globalThis.__odn = (globalThis.__odn || 0) + 1;"] if self.instrument else []

    def block(self, stmts, ind):
        out = []
        for st in stmts:
            out.extend(self.stmt(st, ind))
        return out

    def if_chain(self, st, ind, kw):
        out = ["%s%s (%s) {" % (ind, kw, self.e(st[1]))]
        out += self.block(st[2], ind + "  ")
        els = st[3]
        if len(els) == 1 and els[0][0] == "if" and not self.instrument:
            sub = self.if_chain(els[0], ind, "} else if")
            out += sub
            return out
        if els:
            out.append(ind + "} else {")
            out += self.block(els, ind + "  ")
        out.append(ind + "}")
        return out

    def stmt(self, st, ind):
        h = st[0]
        out = []
        if h not in ("for", "each"):
            out += self.tick(ind)
        if h == "let":
            out.append("%slet %s%s = %s;" % (ind, st[1], self.ty(st[2]), self.e(st[3])))
        elif h == "set":
            out.append("%s%s = %s;" % (ind, st[1], self.e(st[2])))
        elif h == "setf":
            out.append("%sthis.%s = %s;" % (ind, st[1], self.e(st[2])))
        elif h == "sidx":
            out.append("%s%s[%s] = %s;" % (ind, self.tgt(st[1]), self.e(st[2]), self.e(st[3])))
        elif h == "push":
            out.append("%s%s.push(%s);" % (ind, self.tgt(st[1]), self.e(st[2])))
        elif h in ("popto", "shiftto"):
            meth = "pop" if h == "popto" else "shift"
            cast = (" as %s" % TS_TYPE[st[2]]) if self.ts else ""
            out.append("%slet %s%s = %s.%s()%s;" % (ind, st[1], self.ty(st[2]), self.tgt(st[3]), meth, cast))
        elif h == "if":
            out += self.if_chain(st, ind, "if")
        elif h == "for":
            out.append("%sfor (let %s = %s; %s < %s; %s++) {" % (ind, st[1], self.e(st[2]), st[1], self.e(st[3], B.PREC_C["cmp"], "R", True), st[1]))
            out += self.tick(ind + "  ")
            out += self.block(st[4], ind + "  ")
            out.append(ind + "}")
            out += self.tick(ind)
        elif h == "each":
            out.append("%sfor (const %s of %s) {" % (ind, st[1], self.e(st[2])))
            out += self.tick(ind + "  ")
            out += self.block(st[3], ind + "  ")
            out.append(ind + "}")
            out += self.tick(ind)
        elif h == "ret":
            out.append("%sreturn %s;" % (ind, self.e(st[1])))
        elif h == "raise":
            out.append("%sthrow new %s();" % (ind, B.err_marker(self.mod, st[1], self.lang)))
        elif h == "do":
            out.append("%s%s;" % (ind, self.e(st[1])))
        else:
            raise ValueError(h)
        return out

    # ------------------------------------------------------------------ files
    def func(self, f, ind, method=False):
        if self.ts:
            params = ", ".join("%s: %s" % (p[0], TS_TYPE[p[1]]) for p in f["params"])
            ret = ": " + TS_TYPE[f["ret"]]
        else:
            params, ret = ", ".join(p[0] for p in f["params"]), ""
        if method:
            head = "%s%s(%s)%s {" % (ind, f["name"], params, ret)
        else:
            head = "%s%sfunction %s(%s)%s {" % (ind, "export " if self.ts else "", f["name"], params, ret)
        return [head] + self.block(f["body"], ind + "  ") + [ind + "}"]

    def file(self, k):
        mod = self.mod
        deps = B.file_deps(mod)
        lines = ["'use strict';"] if not self.ts else []
        exported = []
        for dk in sorted(deps[k]):
            if self.ts:
                lines.append("import { %s } from './%s';" % (", ".join(deps[k][dk]), self.fname(mod["files"][dk])))
            else:
                lines.append("const { %s } = require('./%s');" % (", ".join(deps[k][dk]), mod["files"][dk]))
        errs = B.used_err_ids(mod, k)
        for e in sorted(mod["errors"]):
            info = mod["errors"][e]
            if info.get("js_custom") and k != self.home and e in errs:
                nm = info["javascript"]
                if self.ts:
                    lines.append("import { %s } from './%s';" % (nm, self.fname(mod["files"][self.home])))
                else:
                    lines.append("const { %s } = require('./%s');" % (nm, mod["files"][self.home]))
        if len(lines) > (0 if self.ts else 1):
            lines.append("")
        for c in mod["consts"]:
            if c.get("file", 0) == k:
                lines.append("%sconst %s%s = %s;" % ("export " if self.ts else "", c["name"], self.ty(c["type"]), lit(c["value"], c["type"])))
                exported.append(c["name"])
        if k == self.home:
            for e in sorted(mod["errors"]):
                info = mod["errors"][e]
                if info.get("js_custom"):
                    lines += ["", "%sclass %s extends Error {}" % ("export " if self.ts else "", info["javascript"])]
                    exported.append(info["javascript"])
        for f in B.funcs_in_file(mod, k):
            if f["scope"] == "free":
                lines += [""] + self.func(f, "")
                exported.append(f["name"])
        if self.cls and self.cls["file"] == k:
            lines += ["", "%sclass %s {" % ("export " if self.ts else "", self.cls["name"])]
            exported.append(self.cls["name"])
            if self.ts:
                for fl in self.cls["fields"]:
                    lines.append("  %s: %s;" % (fl["name"], TS_TYPE[fl["type"]]))
            lines.append("  constructor() {")
            for fl in self.cls["fields"]:
                lines.append("    this.%s = %s;" % (fl["name"], lit(fl["init"], fl["type"])))
            lines.append("  }")
            for f in B.funcs_in_file(mod, k):
                if f["scope"] == "method":
                    lines += [""] + self.func(f, "  ", method=True)
            lines.append("}")
        if not self.ts:
            lines += ["", "module.exports = { %s };" % ", ".join(exported)]
        while lines and lines[0] == "":
            lines.pop(0)
        return "\n".join(lines) + "\n"


def render_module(mod, ts=False, instrument=False):
    r = JsRender(mod, ts, instrument)
    out = {}
    for k, stem in enumerate(mod["files"]):
        out[r.fname(stem)] = r.file(k)
    return out


def render_function_body(mod, fn, ts=False):
    r = JsRender(mod, ts)
    method = fn["scope"] == "method"
    return "\n".join(r.func(fn, "  " if method else "", method=method)) + "\n"

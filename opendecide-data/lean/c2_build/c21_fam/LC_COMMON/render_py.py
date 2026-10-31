"""Python renderer for the IR (module files). Output is text only; nothing here executes it."""
from . import ir as I
from . import render_base as B

LANG = "python"


def lit(value, ty):
    if ty == I.INT:
        return str(int(value))
    if ty == I.STR:
        return "'%s'" % B.check_str(value)
    if ty == I.BOOL:
        return "True" if value else "False"
    et = I.ELEM[ty]
    return "[" + ", ".join(lit(x, et) for x in value) + "]"


class PyRender:
    def __init__(self, mod, instrument=False):
        self.mod = mod
        self.instrument = instrument
        self.cls = mod["cls"]
        self.home = B.dep_order(mod)[0]

    # ------------------------------------------------------------------ expressions
    def e(self, node, parent=0, side="L", parent_cmp=False):
        text, prec, is_cmp = self._e(node)
        if B.need_paren(prec, parent, side, is_cmp, parent_cmp):
            return "(" + text + ")"
        return text

    def _e(self, n):
        P = B.PREC_PY
        h = n[0]
        if h == "int":
            return (str(n[1]) if n[1] >= 0 else "(%d)" % n[1]), P["atom"], False
        if h in ("str", "bool"):
            return lit(n[1], I.STR if h == "str" else I.BOOL), P["atom"], False
        if h == "var" or h == "const":
            return n[1], P["atom"], False
        if h == "field":
            return "self." + n[1], P["atom"], False
        if h == "bin":
            op = n[1]
            cls_ = B.bin_class(op)
            pr = P["cmp"] if cls_ in ("eq", "cmp") else P[cls_]
            sym = {"and": "and", "or": "or", "++": "+", "//": "//"}.get(op, op)
            cmpop = cls_ in ("eq", "cmp")
            a = self.e(n[2], pr, "L", cmpop)
            c = self.e(n[3], pr, "R", cmpop)
            return "%s %s %s" % (a, sym, c), pr, cmpop
        if h == "not":
            return "not " + self.e(n[1], P["not"], "R"), P["not"], False
        if h in ("min", "max"):
            return "%s(%s, %s)" % (h, self.e(n[1]), self.e(n[2])), P["atom"], False
        if h == "cond":
            return "%s if %s else %s" % (self.e(n[2], 1), self.e(n[1], 1), self.e(n[3], 1)), 0, False
        if h == "len":
            return "len(%s)" % self.e(n[1]), P["atom"], False
        if h == "idx":
            return "%s[%s]" % (self.e(n[1], P["atom"]), self.e(n[2])), P["atom"], False
        if h == "lst":
            return "[" + ", ".join(self.e(x) for x in n[2]) + "]", P["atom"], False
        if h == "istr":
            return "str(%s)" % self.e(n[1]), P["atom"], False
        if h == "zpad":
            return "str(%s).zfill(%d)" % (self.e(n[1]), n[2][1]), P["atom"], False
        if h == "has":
            return "%s in %s" % (self.e(n[2], P["cmp"], "L", True), self.e(n[1], P["cmp"], "R", True)), P["cmp"], True
        if h == "starts":
            return "%s.startswith(%s)" % (self.e(n[1], P["atom"]), self.e(n[2])), P["atom"], False
        if h == "fcall":
            return "%s(%s)" % (n[1], ", ".join(self.e(a) for a in n[2])), P["atom"], False
        if h == "mcall":
            return "self.%s(%s)" % (n[1], ", ".join(self.e(a) for a in n[2])), P["atom"], False
        raise ValueError(h)

    def tgt(self, t):
        return t[1] if t[0] == "var" else "self." + t[1]

    # ------------------------------------------------------------------ statements
    def block(self, stmts, ind):
        out = []
        if not stmts:
            return [ind + "pass"]
        for st in stmts:
            out.extend(self.stmt(st, ind))
        return out

    def tick(self, ind):
        return [ind + "_odc.n += 1"] if self.instrument else []

    def if_chain(self, st, ind, kw):
        out = ["%s%s %s:" % (ind, kw, self.e(st[1]))]
        out += self.block(st[2], ind + "    ")
        els = st[3]
        if len(els) == 1 and els[0][0] == "if" and not self.instrument:
            out += self.if_chain(els[0], ind, "elif")
        elif els:
            out.append(ind + "else:")
            out += self.block(els, ind + "    ")
        return out

    def stmt(self, st, ind):
        h = st[0]
        out = []
        if h not in ("for", "each"):
            out += self.tick(ind)
        if h == "let" or h == "set":
            name, e = (st[1], st[3]) if h == "let" else (st[1], st[2])
            out.append("%s%s = %s" % (ind, name, self.e(e)))
        elif h == "setf":
            out.append("%sself.%s = %s" % (ind, st[1], self.e(st[2])))
        elif h == "sidx":
            out.append("%s%s[%s] = %s" % (ind, self.tgt(st[1]), self.e(st[2]), self.e(st[3])))
        elif h == "push":
            out.append("%s%s.append(%s)" % (ind, self.tgt(st[1]), self.e(st[2])))
        elif h == "popto":
            out.append("%s%s = %s.pop()" % (ind, st[1], self.tgt(st[3])))
        elif h == "shiftto":
            out.append("%s%s = %s.pop(0)" % (ind, st[1], self.tgt(st[3])))
        elif h == "if":
            out += self.if_chain(st, ind, "if")
        elif h == "for":
            out.append("%sfor %s in range(%s, %s):" % (ind, st[1], self.e(st[2]), self.e(st[3])))
            out += self.tick(ind + "    ")
            out += self.block(st[4], ind + "    ")
            out += self.tick(ind)
        elif h == "each":
            out.append("%sfor %s in %s:" % (ind, st[1], self.e(st[2])))
            out += self.tick(ind + "    ")
            out += self.block(st[3], ind + "    ")
            out += self.tick(ind)
        elif h == "ret":
            out.append("%sreturn %s" % (ind, self.e(st[1])))
        elif h == "raise":
            out.append("%sraise %s()" % (ind, B.err_marker(self.mod, st[1], LANG)))
        elif h == "do":
            out.append("%s%s" % (ind, self.e(st[1])))
        else:
            raise ValueError(h)
        return out

    # ------------------------------------------------------------------ files
    def func(self, f, ind, method=False):
        params = ([ "self"] if method else []) + [p[0] for p in f["params"]]
        out = ["%sdef %s(%s):" % (ind, f["name"], ", ".join(params))]
        out += self.block(f["body"], ind + "    ")
        return out

    def file(self, k):
        mod = self.mod
        deps = B.file_deps(mod)
        lines = []
        if self.instrument:
            lines.append("import odc as _odc")
        for dk in sorted(deps[k]):
            lines.append("from %s import %s" % (mod["files"][dk], ", ".join(deps[k][dk])))
        errs = [e for e in B.used_err_ids(mod, k)]
        custom_here = []
        for e in sorted(mod["errors"]):
            info = mod["errors"][e]
            if info.get("python_custom"):
                if k == self.home:
                    custom_here.append(info["python"])
                elif e in errs:
                    lines.append("from %s import %s" % (mod["files"][self.home], info["python"]))
        if lines:
            lines.append("")
        for c in mod["consts"]:
            if c.get("file", 0) == k:
                lines.append("%s = %s" % (c["name"], lit(c["value"], c["type"])))
        for name in custom_here:
            lines += ["", "", "class %s(Exception):" % name, "    pass"]
        for f in B.funcs_in_file(mod, k):
            if f["scope"] == "free":
                lines += ["", ""] + self.func(f, "")
        if self.cls and self.cls["file"] == k:
            lines += ["", "", "class %s:" % self.cls["name"], "    def __init__(self):"]
            for fl in self.cls["fields"]:
                lines.append("        self.%s = %s" % (fl["name"], lit(fl["init"], fl["type"])))
            for f in B.funcs_in_file(mod, k):
                if f["scope"] == "method":
                    lines += [""] + self.func(f, "    ", method=True)
        while lines and lines[0] == "":
            lines.pop(0)
        out = []
        for ln in lines:                       # at most two blank lines in a row
            if ln == "" and len(out) >= 2 and out[-1] == "" and out[-2] == "":
                continue
            out.append(ln)
        return "\n".join(out) + "\n"


def render_module(mod, instrument=False):
    """{path: text} for every module file (no tests, no driver)."""
    r = PyRender(mod, instrument)
    out = {}
    for k, stem in enumerate(mod["files"]):
        out[stem + ".py"] = r.file(k)
    if instrument:
        out["odc.py"] = "n = 0\n"
    return out


def render_function_body(mod, fn):
    """Body text of one function (used for EQV2 program pairs, which show two bodies of the same function)."""
    r = PyRender(mod)
    method = fn["scope"] == "method"
    return "\n".join(r.func(fn, "    " if method else "", method=method)) + "\n"

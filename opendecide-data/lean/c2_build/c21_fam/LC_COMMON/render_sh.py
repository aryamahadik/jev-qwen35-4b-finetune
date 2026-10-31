"""bash renderer. Text only. Requires an IR lowered with lower_for(mod, "bash", idents).

Calling convention (documented in every bash row's task text):
  * a function takes scalar arguments only ($1, $2, ...), and reports its result in the global variable RET;
  * booleans are 1 / 0; lists live only in global arrays (state fields / tables) or function-local arrays;
  * "raising" is `return STATUS` with an authored status number (64 and up); callers propagate with `|| return $?`;
  * state fields are global variables; `reset_*` (name in mod.meta.reset_name) restores their initial values.
Only external commands from the pinned allow-list may be used (here: none; printf is a builtin).
"""
from . import ir as I
from . import render_base as B

ARITH_HEADS = {"int", "bool", "var", "field", "const", "len", "idx", "min", "max", "not", "bin"}


class ShUnsupported(ValueError):
    pass


def is_arith(e, types):
    """True if `e` can be evaluated inside $(( )) : int/bool leaves only."""
    h = e[0]
    if h in ("int", "bool"):
        return True
    if h in ("var", "field", "const"):
        return types(e) in (I.INT, I.BOOL)
    if h == "len":
        return True
    if h == "idx":
        return types(e[1]) == I.INTS and is_arith(e[2], types)
    if h in ("min", "max"):
        return is_arith(e[1], types) and is_arith(e[2], types)
    if h == "not":
        return is_arith(e[1], types)
    if h == "bin":
        op = e[1]
        if op == "++":
            return False
        if op in ("==", "!="):
            if types(e[2]) == I.STR:
                return False
        return is_arith(e[2], types) and is_arith(e[3], types)
    return False


class ShRender:
    def __init__(self, mod):
        self.mod = mod
        self.cls = mod["cls"]
        self.sigs = I.functions(mod)
        self.fts = I.field_types(mod)
        self.cts = I.const_types(mod)
        self.has_name = mod["meta"].get("has_name")
        self.reset_name = mod["meta"].get("reset_name")
        self.env = {}
        self.uses_has = False

    # ------------------------------------------------------------------ typing helper
    def t(self, e):
        return I.typeof(e, self.env, self.mod, self.sigs)

    # ------------------------------------------------------------------ arithmetic
    def ar(self, e):
        h = e[0]
        if h == "int":
            return str(e[1]) if e[1] >= 0 else "(%d)" % e[1]
        if h == "bool":
            return "1" if e[1] else "0"
        if h in ("var", "field", "const"):
            return e[1]
        if h == "len":
            a = e[1]
            if a[0] not in ("var", "field", "const"):
                raise ShUnsupported("len of a non-variable in bash")
            ty = self.t(a)
            return "${#%s}" % a[1] if ty == I.STR else "${#%s[@]}" % a[1]
        if h == "idx":
            return "%s[%s]" % (e[1][1], self.ar(e[2]))
        if h in ("min", "max"):
            a, c = self.ar(e[1]), self.ar(e[2])
            op = "<" if h == "min" else ">"
            return "((%s) %s (%s) ? (%s) : (%s))" % (a, op, c, a, c)
        if h == "not":
            return "(!%s)" % self.ar(e[1])
        if h == "bin":
            op = e[1]
            sym = {"//": "/", "and": "&&", "or": "||"}.get(op, op)
            return "(%s %s %s)" % (self.ar(e[2]), sym, self.ar(e[3]))
        raise ShUnsupported("non-arithmetic expression %r in arithmetic context" % h)

    # ------------------------------------------------------------------ strings
    def parts(self, e):
        """List of ('lit', text) | ('raw', text-inside-double-quotes)."""
        h = e[0]
        if h == "str":
            return [("lit", B.check_str(e[1]))]
        if h in ("var", "field", "const"):
            return [("raw", "${%s}" % e[1])]
        if h == "bin" and e[1] == "++":
            return self.parts(e[2]) + self.parts(e[3])
        if h == "istr":
            return [("raw", "$(( %s ))" % self.ar(e[1]))]
        if h == "zpad":
            return [("raw", "$(printf '%%0%dd' \"$(( %s ))\")" % (e[2][1], self.ar(e[1])))]
        if h == "idx":
            return [("raw", "${%s[%s]}" % (e[1][1], self.ar(e[2])))]
        raise ShUnsupported("string expression %r in bash" % h)

    def word(self, e):
        ps = self.parts(e)
        if all(k == "lit" for k, _ in ps):
            return "'%s'" % "".join(t for _, t in ps)
        return '"%s"' % "".join(t for _, t in ps)

    def val(self, e):
        """Right-hand-side text for an assignment/argument of any scalar type."""
        ty = self.t(e)
        if ty == I.STR:
            return self.word(e)
        return "$(( %s ))" % self.ar(e)

    # ------------------------------------------------------------------ conditions
    def cond(self, e):
        h = e[0]
        if h == "bool":
            return "true" if e[1] else "false"
        if is_arith(e, self.t):
            return "(( %s ))" % self.ar(e)
        if h == "not":
            return "! " + self.cond(e[1])
        if h == "bin":
            op = e[1]
            if op in ("and", "or"):
                return "{ %s %s %s; }" % (self.cond(e[2]), "&&" if op == "and" else "||", self.cond(e[3]))
            if op in ("==", "!=") and self.t(e[2]) == I.STR:
                return "[[ %s %s %s ]]" % (self.word(e[2]), "==" if op == "==" else "!=", self.word(e[3]))
        if h == "has":
            self.uses_has = True
            xs = e[1]
            if xs[0] not in ("var", "field", "const"):
                raise ShUnsupported("has over a non-variable list")
            needle = self.word(e[2]) if self.t(e[2]) == I.STR else '"$(( %s ))"' % self.ar(e[2])
            return '%s %s "${%s[@]}"' % (self.has_name, needle, xs[1])
        if h == "starts":
            a, c = self.word(e[1]), self.word(e[2])
            return "[[ %s == %s* ]]" % (a, c)
        raise ShUnsupported("condition %r in bash" % h)

    # ------------------------------------------------------------------ calls
    def call_args(self, args):
        out = []
        for a in args:
            ty = self.t(a)
            if ty in I.LISTS:
                raise ShUnsupported("list argument in bash")
            out.append(self.word(a) if ty == I.STR else '"$(( %s ))"' % self.ar(a))
        return " ".join(out)

    def call_line(self, e, ind):
        a = self.call_args(e[2])
        return "%s%s%s || return $?" % (ind, e[1], (" " + a) if a else "")

    # ------------------------------------------------------------------ statements
    def block(self, stmts, ind):
        out = []
        for st in stmts:
            out.extend(self.stmt(st, ind))
        return out if out else [ind + ":"]

    def assign(self, name, ty, e, ind, local):
        lc = "local " if local else ""
        if e[0] in ("fcall", "mcall"):
            out = [self.call_line(e, ind)]
            if ty in I.LISTS:
                raise ShUnsupported("list returned from a call in bash")
            out.append('%s%s%s="$RET"' % (ind, lc, name))
            return out
        if ty in I.LISTS:
            if e[0] != "lst":
                raise ShUnsupported("list assignment from a non-literal")
            items = " ".join(self.val(x) if I.ELEM[ty] == I.INT else self.word(x) for x in e[2])
            return ["%s%s%s=(%s)" % (ind, "local -a " if local else "", name, items)]
        if ty == I.BOOL and not is_arith(e, self.t):
            pre = ["%slocal %s" % (ind, name)] if local else []
            return pre + ["%sif %s; then" % (ind, self.cond(e)), "%s  %s=1" % (ind, name),
                          "%selse" % ind, "%s  %s=0" % (ind, name), "%sfi" % ind]
        return ["%s%s%s=%s" % (ind, lc, name, self.val(e))]

    def stmt(self, st, ind):
        h = st[0]
        if h == "let":
            self.env[st[1]] = st[2]
            return self.assign(st[1], st[2], st[3], ind, True)
        if h == "set":
            return self.assign(st[1], self.env[st[1]], st[2], ind, False)
        if h == "setf":
            return self.assign(st[1], self.fts[st[1]], st[2], ind, False)
        if h == "sidx":
            tgt = st[1][1]
            ety = I.ELEM[self.t(st[1])]
            v = self.val(st[3]) if ety == I.INT else self.word(st[3])
            return ["%s%s[%s]=%s" % (ind, tgt, self.ar(st[2]), v)]
        if h == "push":
            tgt = st[1][1]
            ety = I.ELEM[self.t(st[1])]
            v = self.val(st[2]) if ety == I.INT else self.word(st[2])
            return ["%s%s+=(%s)" % (ind, tgt, v)]
        if h == "popto":
            self.env[st[1]] = st[2]
            tgt = st[3][1]
            return ['%slocal %s="${%s[-1]}"' % (ind, st[1], tgt), "%sunset '%s[-1]'" % (ind, tgt)]
        if h == "shiftto":
            self.env[st[1]] = st[2]
            tgt = st[3][1]
            return ['%slocal %s="${%s[0]}"' % (ind, st[1], tgt), '%s%s=("${%s[@]:1}")' % (ind, tgt, tgt)]
        if h == "if":
            out = ["%sif %s; then" % (ind, self.cond(st[1]))]
            cur = st
            while True:
                out += self.block(cur[2], ind + "  ")
                els = cur[3]
                if len(els) == 1 and els[0][0] == "if":
                    cur = els[0]
                    out.append("%selif %s; then" % (ind, self.cond(cur[1])))
                    continue
                if els:
                    out.append(ind + "else")
                    out += self.block(els, ind + "  ")
                break
            out.append(ind + "fi")
            return out
        if h == "for":
            self.env[st[1]] = I.INT
            return ["%slocal %s" % (ind, st[1]),
                    "%sfor (( %s = %s; %s < %s; %s++ )); do" % (ind, st[1], self.ar(st[2]), st[1], self.ar(st[3]), st[1])] + \
                self.block(st[4], ind + "  ") + [ind + "done"]
        if h == "each":
            ety = I.ELEM[self.t(st[2])]
            self.env[st[1]] = ety
            xs = st[2]
            if xs[0] not in ("var", "field", "const"):
                raise ShUnsupported("each over a non-variable list")
            return ["%slocal %s" % (ind, st[1]), '%sfor %s in "${%s[@]}"; do' % (ind, st[1], xs[1])] + \
                self.block(st[3], ind + "  ") + [ind + "done"]
        if h == "ret":
            if self.t(st[1]) == I.BOOL and not is_arith(st[1], self.t):
                return ["%sif %s; then" % (ind, self.cond(st[1])), "%s  RET=1" % ind, "%selse" % ind,
                        "%s  RET=0" % ind, "%sfi" % ind, "%sreturn 0" % ind]
            return ["%sRET=%s" % (ind, self.val(st[1])), "%sreturn 0" % ind]
        if h == "raise":
            return ["%sreturn %d" % (ind, self.mod["errors"][st[1]]["bash"])]
        if h == "do":
            if st[1][0] not in ("fcall", "mcall"):
                raise ShUnsupported("do of a non-call")
            return [self.call_line(st[1], ind)]
        raise ShUnsupported(h)

    def func(self, f):
        self.env = {p[0]: p[1] for p in f["params"]}
        lines = ["%s() {" % f["name"]]
        if f["params"]:
            lines.append("  local " + " ".join('%s="$%d"' % (p[0], k + 1) for k, p in enumerate(f["params"])))
        lines += self.block(f["body"], "  ")
        lines.append("}")
        return lines

    def file(self, k):
        mod = self.mod
        deps = B.file_deps(mod)
        lines = []
        for dk in sorted(deps[k]):
            lines.append('. "${BASH_SOURCE[0]%%/*}/%s.sh"' % mod["files"][dk])
        body = []
        for c in mod["consts"]:
            if c.get("file", 0) == k:
                body.append(self.global_assign(c["name"], c["type"], c["value"]))
        if self.cls and self.cls["file"] == k:
            body.append("")
            body.append("%s() {" % self.reset_name)
            for fl in self.cls["fields"]:
                body.append("  " + self.global_assign(fl["name"], fl["type"], fl["init"]))
            body.append("}")
            body.append(self.reset_name)
        self.uses_has = False
        funcs = []
        for f in B.funcs_in_file(mod, k):
            funcs += [""] + self.func(f)
        if self.uses_has:
            lines += ["%s() {" % self.has_name, '  local needle="$1" x', "  shift",
                      '  for x in "$@"; do', '    [ "$x" = "$needle" ] && return 0', "  done", "  return 1", "}"]
        lines += body + funcs
        if lines and lines[0] == "":
            lines.pop(0)
        return "\n".join(lines) + "\n"

    def global_assign(self, name, ty, value):
        if ty == I.INT:
            return "%s=%d" % (name, value)
        if ty == I.STR:
            return "%s='%s'" % (name, B.check_str(value))
        if ty == I.BOOL:
            return "%s=%d" % (name, 1 if value else 0)
        items = " ".join(str(x) if ty == I.INTS else "'%s'" % B.check_str(x) for x in value)
        return "%s=(%s)" % (name, items)


def render_module(mod):
    r = ShRender(mod)
    out = {}
    for k, stem in enumerate(mod["files"]):
        out[stem + ".sh"] = r.file(k)
    return out


def render_function_body(mod, fn):
    r = ShRender(mod)
    return "\n".join(r.func(fn)) + "\n"

"""IR -> IR lowering for target languages that lack an expression form the IR uses.

  go    : no conditional expression  -> `cond` hoisted into `let tmp; if c: tmp = a else: tmp = b`
  bash  : `cond`, and every call inside an expression, hoisted to statement level (calls become `let tmp = call`)
  js/ts/go/bash : a loop bound that the body might change is evaluated once into a temp (Python's range() does this
                  natively; the other languages re-test the bound every iteration)

Temp names are drawn from the module's Idents (namespace.py, TRAINING salt), never invented here.
Lowering preserves left-to-right evaluation. Calls/conds inside the right operand of and/or (short-circuit) or inside a
cond branch that would be hoisted out of its guard are refused with LowerError (the generator avoids them).
"""
from . import ir as I


class LowerError(ValueError):
    pass


_DEFAULT = {I.INT: ["int", 0], I.STR: ["str", ""], I.BOOL: ["bool", False]}


def _assigned_vars(block):
    out = set()
    for _, n in I.walk(block):
        if n[0] in ("set", "let", "popto", "shiftto"):
            out.add(n[1])
    return out


def _simple_bound(hi, body, fields_mutated):
    if hi[0] == "int":
        return True
    if hi[0] == "var" and hi[1] not in _assigned_vars(body):
        return True
    if hi[0] == "const":
        return True
    if hi[0] == "len" and hi[1][0] == "const":
        return True
    if hi[0] == "len" and hi[1][0] == "var":
        # a list local: unsafe if the body mutates it
        for _, n in I.walk(body):
            if n[0] in ("push", "popto", "shiftto") and n[-1 if n[0] != "push" else 1] == hi[1]:
                return False
        return True
    return False


class Lowerer:
    def __init__(self, mod, lang, idents):
        self.mod = mod
        self.lang = lang
        self.idents = idents
        self.n = 0
        self.sigs = I.functions(mod)
        self.hoist_cond = lang in ("go", "bash")
        self.hoist_call = lang == "bash"
        self.hoist_loop = lang in ("javascript", "typescript", "go", "bash")

    def tmp(self):
        self.n += 1
        return self.idents.var("lw%d" % self.n)

    # ---------------------------------------------------------------- expressions
    def lx(self, e, pre, whole_rhs=False):
        h = e[0]
        if h in ("int", "str", "bool", "var", "field", "const"):
            return e
        if h == "bin":
            if e[1] in ("and", "or"):
                a = self.lx(e[2], pre)
                inner = []
                c = self.lx(e[3], inner)
                if inner:
                    raise LowerError("hoistable expression inside a short-circuit operand")
                return ["bin", e[1], a, c]
            return ["bin", e[1], self.lx(e[2], pre), self.lx(e[3], pre)]
        if h in ("not", "len", "istr"):
            return [h, self.lx(e[1], pre)]
        if h in ("min", "max", "idx", "has", "starts"):
            return [h, self.lx(e[1], pre), self.lx(e[2], pre)]
        if h == "zpad":
            return [h, self.lx(e[1], pre), e[2]]
        if h == "lst":
            return [h, e[1], [self.lx(x, pre) for x in e[2]]]
        if h == "cond":
            if not self.hoist_cond:
                return [h, self.lx(e[1], pre), self.lx(e[2], pre), self.lx(e[3], pre)]
            t = self.tmp()
            ty = self._type(e)
            if ty not in _DEFAULT:
                raise LowerError("cond over a list cannot be hoisted")
            c = self.lx(e[1], pre)
            ta, tb = [], []
            a = self.lx(e[2], ta)
            bb = self.lx(e[3], tb)
            pre.append(["let", t, ty, _DEFAULT[ty]])
            pre.append(["if", c, ta + [["set", t, a]], tb + [["set", t, bb]]])
            return ["var", t]
        if h in ("fcall", "mcall"):
            args = [self.lx(a, pre) for a in e[2]]
            node = [h, e[1], args]
            if self.hoist_call and not whole_rhs:
                t = self.tmp()
                pre.append(["let", t, self.sigs[e[1]]["ret"], node])
                return ["var", t]
            return node
        raise LowerError("unknown head %r" % h)

    def _type(self, e):
        env = getattr(self, "_env", {})
        return I.typeof(e, env, self.mod, self.sigs)

    # ---------------------------------------------------------------- statements
    def block(self, stmts, env):
        out = []
        env = dict(env)
        for st in stmts:
            out.extend(self.stmt(st, env))
        return out

    def stmt(self, st, env):
        h = st[0]
        self._env = env
        pre = []
        if h == "let":
            rhs = st[3]
            e = self.lx(rhs, pre, whole_rhs=rhs[0] in ("fcall", "mcall"))
            env[st[1]] = st[2]
            return pre + [["let", st[1], st[2], e]]
        if h == "set":
            e = self.lx(st[2], pre, whole_rhs=st[2][0] in ("fcall", "mcall"))
            if self.hoist_call and st[2][0] in ("fcall", "mcall"):
                # keep `set x = call` as `set` of a hoisted temp so the emitter only sees calls under let/do
                t = self.tmp()
                return pre + [["let", t, self.sigs[st[2][1]]["ret"], e], ["set", st[1], ["var", t]]]
            return pre + [["set", st[1], e]]
        if h == "setf":
            rhs = st[2]
            e = self.lx(rhs, pre)
            return pre + [["setf", st[1], e]]
        if h == "sidx":
            i = self.lx(st[2], pre)
            e = self.lx(st[3], pre)
            return pre + [["sidx", st[1], i, e]]
        if h == "push":
            e = self.lx(st[2], pre)
            return pre + [["push", st[1], e]]
        if h in ("popto", "shiftto"):
            env[st[1]] = st[2]
            return [list(st)]
        if h == "ret":
            e = self.lx(st[1], pre)
            return pre + [["ret", e]]
        if h == "do":
            e = self.lx(st[1], pre, whole_rhs=True)
            return pre + [["do", e]]
        if h == "raise":
            return [list(st)]
        if h == "if":
            c = self.lx(st[1], pre)
            return pre + [["if", c, self.block(st[2], env), self.block(st[3], env)]]
        if h == "for":
            lo = self.lx(st[2], pre)
            hi = self.lx(st[3], pre)
            body_env = dict(env)
            body_env[st[1]] = I.INT
            body = self.block(st[4], body_env)
            if self.hoist_loop and not _simple_bound(hi, st[4], True):
                t = self.tmp()
                pre.append(["let", t, I.INT, hi])
                hi = ["var", t]
            return pre + [["for", st[1], lo, hi, body]]
        if h == "each":
            xs = self.lx(st[2], pre)
            body_env = dict(env)
            body_env[st[1]] = I.ELEM[I.typeof(st[2], env, self.mod, self.sigs)]
            return pre + [["each", st[1], xs, self.block(st[3], body_env)]]
        raise LowerError("unknown statement %r" % h)

    def run(self):
        out = I.clone(self.mod)
        fns = []
        for f in out["funcs"]:
            env = {p[0]: p[1] for p in f["params"]}
            g = dict(f)
            g["body"] = self.block(f["body"], env)
            fns.append(g)
        out["funcs"] = fns
        out["meta"] = dict(out.get("meta", {}), lowered_for=self.lang)
        return out


def lower_for(mod, lang, idents):
    if lang == "python":
        return I.clone(mod)
    lo = Lowerer(mod, lang, idents).run()
    I.check_module(lo)
    return lo

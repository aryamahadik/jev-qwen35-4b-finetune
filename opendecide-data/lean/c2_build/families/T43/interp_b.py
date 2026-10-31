"""families/T43/interp_b.py: the tree-walking AST interpreter of solver B (a vendored copy of the interpreter of
families/T42/solver_b.py lines 109-735 as of 15 Oct 2026; scope chains, closures, defaults at def time, classes with C3,
try/except, comprehension scope, f-strings). It is solver B's own execution paradigm: it never starts CPython code
through exec/eval of the program under test (the operators are the language's own, the statements are walked here).
Copied so that T42 fixes by other agents cannot change T43 solver B; no T43 or solver-A code is imported."""
from __future__ import annotations

import ast
import itertools
import operator
import re

ALLOWED_EXC = {"ValueError", "TypeError", "KeyError", "IndexError", "ZeroDivisionError", "AttributeError", "NameError",
               "UnboundLocalError", "StopIteration", "AssertionError", "OverflowError", "LookupError",
               "RecursionError", "NotImplementedError"}


class ParseError(ValueError):
    pass


class _Break(BaseException):
    pass


class _Continue(BaseException):
    pass


class _Return(BaseException):
    def __init__(self, v):
        self.v = v


class _Budget(Exception):
    pass


class Scope:
    def __init__(self, parent=None, local_names=None, kind="function"):
        self.vars, self.parent, self.kind = {}, parent, kind
        self.local_names = local_names if local_names is not None else None
        self.declared = {}


def _stores(body) -> set:
    """Names a function body binds (assignment targets, loop targets, imports, defs, handler names), minus the
    names it declares global / nonlocal."""
    names, decl = set(), set()

    def target(t):
        for n in ast.walk(t):
            if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store):
                names.add(n.id)

    def walk(stmts):
        for s in stmts:
            if isinstance(s, (ast.FunctionDef, ast.ClassDef)):
                names.add(s.name)
                continue
            if isinstance(s, (ast.Global, ast.Nonlocal)):
                decl.update(s.names)
            for fld, val in ast.iter_fields(s):
                if fld in ("targets", "target"):
                    for t in (val if isinstance(val, list) else [val]):
                        target(t)
            if isinstance(s, ast.AugAssign):
                target(s.target)
            if isinstance(s, (ast.Import, ast.ImportFrom)):
                for a in s.names:
                    names.add((a.asname or a.name).split(".")[0])
            if isinstance(s, ast.Try):
                for h in s.handlers:
                    if h.name:
                        names.add(h.name)
                    walk(h.body)
            for fld in ("body", "orelse", "finalbody"):
                v = getattr(s, fld, None)
                if isinstance(v, list):
                    walk(v)
    walk(body)
    return names - decl


class BFunc:
    def __init__(self, interp, name, args, body, env, defaults, kwdefaults, is_lambda=False):
        self.interp, self.name, self.args, self.body, self.env = interp, name, args, body, env
        self.defaults, self.kwdefaults, self.is_lambda = defaults, kwdefaults, is_lambda
        self.defclass = None
        self.locals = None if is_lambda else _stores(body)
        self.is_gen = (not is_lambda) and any(isinstance(n, (ast.Yield, ast.YieldFrom)) for s in body for n in ast.walk(s)
                                              if not isinstance(n, (ast.FunctionDef, ast.Lambda)) or n is s)

    def __get__(self, obj, owner=None):
        return self if obj is None else BMethod(self, obj)

    def __call__(self, *a, **kw):
        return self.interp.call(self, a, kw)


class BMethod:
    def __init__(self, fn, obj):
        self.fn, self.obj = fn, obj

    def __call__(self, *a, **kw):
        return self.fn(self.obj, *a, **kw)


class BClass:
    def __init__(self, name, bases, ns):
        self.__name__, self.__bases__, self.ns = name, tuple(bases), ns
        self.__mro__ = tuple(_c3(self))

    def lookup(self, attr):
        for c in self.__mro__:
            if attr in c.ns:
                return c, c.ns[attr]
        raise KeyError(attr)

    def __call__(self, *a, **kw):
        obj = BObject(self)
        try:
            _, init = self.lookup("__init__")
        except KeyError:
            if a or kw:
                raise TypeError("takes no arguments")
            return obj
        init(obj, *a, **kw)
        return obj

    def __getattr__(self, attr):
        if attr.startswith("__") and attr not in ("__init__",):
            raise AttributeError(attr)
        try:
            _, v = self.lookup(attr)
        except KeyError:
            raise AttributeError(f"type object '{self.__name__}' has no attribute '{attr}'")
        return v


class BObject:
    def __init__(self, cls):
        object.__setattr__(self, "cls", cls)
        object.__setattr__(self, "attrs", {})

    def __getattr__(self, attr):
        if attr in self.attrs:
            return self.attrs[attr]
        try:
            _, v = self.cls.lookup(attr)
        except KeyError:
            raise AttributeError(f"object has no attribute '{attr}'")
        return v.__get__(self, self.cls) if isinstance(v, BFunc) else v

    def __setattr__(self, attr, val):
        self.attrs[attr] = val


class BSuper:
    """super(): every attribute (dunder names included) is looked up in the MRO after the defining class."""

    def __init__(self, cls, obj):
        object.__setattr__(self, "_c", cls)
        object.__setattr__(self, "_o", obj)

    def __getattribute__(self, attr):
        cls, obj = object.__getattribute__(self, "_c"), object.__getattribute__(self, "_o")
        mro = obj.cls.__mro__
        for c in mro[mro.index(cls) + 1:]:
            if attr in c.ns:
                v = c.ns[attr]
                return v.__get__(obj, obj.cls) if isinstance(v, BFunc) else v
        raise AttributeError(f"super object has no attribute '{attr}'")


def _c3(cls):
    """C3 linearisation: merge the bases' linearisations with the base list, taking the first head that is in no tail."""
    seqs = [list(b.__mro__) for b in cls.__bases__] + [list(cls.__bases__)]
    out = [cls]
    while True:
        seqs = [s for s in seqs if s]
        if not seqs:
            return out
        for s in seqs:
            head = s[0]
            if not any(head in t[1:] for t in seqs):
                break
        else:
            raise TypeError("Cannot create a consistent method resolution order (MRO) for bases")
        out.append(head)
        seqs = [[x for x in s if x is not head] if s[0] is head else s for s in seqs]


BINOPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv,
          ast.FloorDiv: operator.floordiv, ast.Mod: operator.mod, ast.Pow: operator.pow, ast.BitAnd: operator.and_,
          ast.BitOr: operator.or_, ast.BitXor: operator.xor, ast.LShift: operator.lshift, ast.RShift: operator.rshift,
          ast.MatMult: operator.matmul}
CMPOPS = {ast.Eq: operator.eq, ast.NotEq: operator.ne, ast.Lt: operator.lt, ast.LtE: operator.le, ast.Gt: operator.gt,
          ast.GtE: operator.ge, ast.Is: operator.is_, ast.IsNot: operator.is_not,
          ast.In: lambda a, b: a in b, ast.NotIn: lambda a, b: a not in b}
UNOPS = {ast.USub: operator.neg, ast.UAdd: operator.pos, ast.Not: operator.not_, ast.Invert: operator.invert}
BUILTIN_NAMES = ("len", "sum", "min", "max", "abs", "sorted", "reversed", "range", "list", "dict", "set", "tuple", "str",
                 "int", "float", "bool", "repr", "enumerate", "zip", "map", "filter", "any", "all", "iter", "next",
                 "round", "divmod", "chr", "ord", "pow", "format", "frozenset", "ValueError", "TypeError", "KeyError",
                 "IndexError", "ZeroDivisionError", "AttributeError", "Exception", "StopIteration", "AssertionError",
                 "LookupError", "ArithmeticError", "object", "NameError", "OverflowError", "bytes", "slice")


class Interp:
    BUDGET = 400_000

    def __init__(self):
        import builtins as _b
        self.out = []
        self.ticks = 0
        self.builtins = {n: getattr(_b, n) for n in BUILTIN_NAMES}
        self.builtins["print"] = self._print
        self.builtins["isinstance"] = self._isinstance
        self.builtins["type"] = lambda o: o.cls if isinstance(o, BObject) else type(o)
        self.builtins["super"] = None
        self.object_cls = BClass("object", [], {})
        self.builtins["object"] = self.object_cls
        self.glob = Scope(None, None, "module")

    def _print(self, *a, sep=" ", end="\n"):
        self.out.append(sep.join(str(x) for x in a) + end)

    @staticmethod
    def _isinstance(o, c):
        if isinstance(o, BObject):
            cs = c if isinstance(c, tuple) else (c,)
            return any(k in o.cls.__mro__ for k in cs if isinstance(k, BClass))
        return isinstance(o, c)

    def tick(self):
        self.ticks += 1
        if self.ticks > self.BUDGET:
            raise _Budget()

    # ---- names
    def load(self, name, env):
        e = env
        first = True
        while e is not None:
            if e.kind == "class" and not first:          # a class body's names are invisible to nested functions
                e = e.parent
                continue
            if e.kind == "function" and e.local_names is not None and name in e.local_names:
                if name in e.vars:
                    return e.vars[name]
                if first:
                    raise UnboundLocalError(f"cannot access local variable '{name}'")
            elif name in e.vars:
                return e.vars[name]
            first = False
            e = e.parent
        if name in self.builtins:
            return self.builtins[name]
        raise NameError(f"name '{name}' is not defined")

    def store(self, name, val, env):
        e = env
        d = env.declared.get(name)
        if d == "global":
            e = self.glob
        elif d == "nonlocal":
            e = env.parent
            while e is not None and not (e.kind == "function" and name in e.vars):
                e = e.parent
            if e is None:
                raise NameError(name)
        e.vars[name] = val

    # ---- expressions
    def ev(self, n, env):
        self.tick()
        m = getattr(self, "e_" + type(n).__name__, None)
        if m is None:
            raise NotImplementedError(type(n).__name__)
        return m(n, env)

    def e_Constant(self, n, env):
        return n.value

    def e_Name(self, n, env):
        return self.load(n.id, env)

    def e_BinOp(self, n, env):
        return BINOPS[type(n.op)](self.ev(n.left, env), self.ev(n.right, env))

    def e_UnaryOp(self, n, env):
        return UNOPS[type(n.op)](self.ev(n.operand, env))

    def e_BoolOp(self, n, env):
        if isinstance(n.op, ast.And):
            v = True
            for x in n.values:
                v = self.ev(x, env)
                if not v:
                    return v
            return v
        v = False
        for x in n.values:
            v = self.ev(x, env)
            if v:
                return v
        return v

    def e_Compare(self, n, env):
        left = self.ev(n.left, env)
        for op, c in zip(n.ops, n.comparators):
            right = self.ev(c, env)
            if not CMPOPS[type(op)](left, right):
                return False
            left = right
        return True

    def e_IfExp(self, n, env):
        return self.ev(n.body if self.ev(n.test, env) else n.orelse, env)

    def e_Attribute(self, n, env):
        return getattr(self.ev(n.value, env), n.attr)

    def e_Subscript(self, n, env):
        return self.ev(n.value, env)[self.ev(n.slice, env)]

    def e_Slice(self, n, env):
        g = lambda x: None if x is None else self.ev(x, env)  # noqa: E731
        return slice(g(n.lower), g(n.upper), g(n.step))

    def e_List(self, n, env):
        return [self.ev(x, env) for x in n.elts]

    def e_Tuple(self, n, env):
        return tuple(self.ev(x, env) for x in n.elts)

    def e_Set(self, n, env):
        return {self.ev(x, env) for x in n.elts}

    def e_Dict(self, n, env):
        return {self.ev(k, env): self.ev(v, env) for k, v in zip(n.keys, n.values)}

    def e_Starred(self, n, env):
        raise NotImplementedError("starred outside a call")

    def e_JoinedStr(self, n, env):
        return "".join(self.ev(v, env) if not isinstance(v, ast.Constant) else v.value for v in n.values)

    def e_FormattedValue(self, n, env):
        v = self.ev(n.value, env)
        if n.conversion == 114:
            v = repr(v)
        elif n.conversion == 115:
            v = str(v)
        elif n.conversion == 97:
            v = ascii(v)
        spec = self.ev(n.format_spec, env) if n.format_spec is not None else ""
        return format(v, spec)

    def e_Lambda(self, n, env):
        return self.make_func("<lambda>", n.args, n.body, env, True)

    def e_Call(self, n, env):
        if isinstance(n.func, ast.Name) and n.func.id == "super" and not n.args:
            fn = env
            while fn is not None and not (fn.kind == "function" and "__func__" in fn.vars):
                fn = fn.parent
            if fn is None:
                raise RuntimeError("super(): no arguments")
            f = fn.vars["__func__"]
            return BSuper(f.defclass, fn.vars[f.args.args[0].arg])
        func = self.ev(n.func, env)
        args = []
        for a in n.args:
            if isinstance(a, ast.Starred):
                args.extend(self.ev(a.value, env))
            else:
                args.append(self.ev(a, env))
        kw = {}
        for k in n.keywords:
            if k.arg is None:
                kw.update(self.ev(k.value, env))
            else:
                kw[k.arg] = self.ev(k.value, env)
        return func(*args, **kw)

    def comp_envs(self, gens, i, env):
        if i == len(gens):
            yield env
            return
        g = gens[i]
        for item in self.ev(g.iter, env if i else env.parent):      # the first iterable is read in the outer scope
            self.assign(g.target, item, env)                        # one scope per comprehension: targets are rebound
            if all(self.ev(c, env) for c in g.ifs):
                yield from self.comp_envs(gens, i + 1, env)

    def _comp(self, n, env):
        scope = Scope(env, None, "comp")
        return self.comp_envs(n.generators, 0, scope)

    def e_ListComp(self, n, env):
        return [self.ev(n.elt, e) for e in self._comp(n, env)]

    def e_SetComp(self, n, env):
        return {self.ev(n.elt, e) for e in self._comp(n, env)}

    def e_DictComp(self, n, env):
        return {self.ev(n.key, e): self.ev(n.value, e) for e in self._comp(n, env)}

    def e_GeneratorExp(self, n, env):
        return (self.ev(n.elt, e) for e in self._comp(n, env))

    # ---- assignment targets
    def assign(self, t, val, env):
        if isinstance(t, ast.Name):
            self.store(t.id, val, env)
        elif isinstance(t, (ast.Tuple, ast.List)):
            vals = list(val)
            star = [i for i, x in enumerate(t.elts) if isinstance(x, ast.Starred)]
            if star:
                s = star[0]
                after = len(t.elts) - s - 1
                if len(vals) < len(t.elts) - 1:
                    raise ValueError("not enough values to unpack")
                for i in range(s):
                    self.assign(t.elts[i], vals[i], env)
                self.assign(t.elts[s].value, vals[s:len(vals) - after], env)
                for j in range(after):
                    self.assign(t.elts[s + 1 + j], vals[len(vals) - after + j], env)
                return
            if len(vals) != len(t.elts):
                raise ValueError("wrong number of values to unpack")
            for x, v in zip(t.elts, vals):
                self.assign(x, v, env)
        elif isinstance(t, ast.Subscript):
            self.ev(t.value, env)[self.ev(t.slice, env)] = val
        elif isinstance(t, ast.Attribute):
            setattr(self.ev(t.value, env), t.attr, val)
        else:
            raise NotImplementedError(type(t).__name__)

    # ---- functions
    def make_func(self, name, args, body, env, is_lambda=False):
        a = args
        pos = a.posonlyargs + a.args
        defaults = {p.arg: self.ev(d, env) for p, d in zip(pos[len(pos) - len(a.defaults):], a.defaults)}
        kwd = {p.arg: self.ev(d, env) for p, d in zip(a.kwonlyargs, a.kw_defaults) if d is not None}
        return BFunc(self, name, a, [body] if is_lambda else body, env, defaults, kwd, is_lambda)

    def call(self, fn, args, kw):
        a = fn.args
        pos = [p.arg for p in a.posonlyargs + a.args]
        scope = Scope(fn.env, fn.locals, "function")
        vals = {}
        if len(args) > len(pos) and a.vararg is None:
            raise TypeError("too many positional arguments")
        for p, v in zip(pos, args):
            vals[p] = v
        if a.vararg is not None:
            vals[a.vararg.arg] = tuple(args[len(pos):])
        for k, v in kw.items():
            if k in vals:
                raise TypeError(f"multiple values for argument '{k}'")
            if k in pos or k in [x.arg for x in a.kwonlyargs]:
                vals[k] = v
            elif a.kwarg is None:
                raise TypeError(f"unexpected keyword argument '{k}'")
        for p in pos + [x.arg for x in a.kwonlyargs]:
            if p not in vals:
                if p in fn.defaults:
                    vals[p] = fn.defaults[p]
                elif p in fn.kwdefaults:
                    vals[p] = fn.kwdefaults[p]
                else:
                    raise TypeError(f"missing required argument '{p}'")
        scope.vars.update(vals)
        scope.vars["__func__"] = fn
        if fn.locals is not None:
            scope.local_names = fn.locals | set(vals)
        else:
            scope.local_names = set(vals)
        if fn.is_lambda:
            return self.ev(fn.body[0], scope)
        if fn.is_gen:
            self.gen_out = []
            scope.vars["__yield__"] = []
            try:
                self.run(fn.body, scope)
            except _Return:
                pass
            return iter(scope.vars["__yield__"])
        try:
            self.run(fn.body, scope)
        except _Return as r:
            return r.v
        return None

    # ---- statements
    def run(self, stmts, env):
        for s in stmts:
            self.tick()
            getattr(self, "s_" + type(s).__name__)(s, env)

    def s_Expr(self, s, env):
        if isinstance(s.value, ast.Yield):
            e = env
            while e is not None and "__yield__" not in e.vars:
                e = e.parent
            e.vars["__yield__"].append(self.ev(s.value.value, env) if s.value.value else None)
            return
        self.ev(s.value, env)

    def s_Pass(self, s, env):
        pass

    def s_Assign(self, s, env):
        v = self.ev(s.value, env)
        for t in s.targets:
            self.assign(t, v, env)

    def s_AnnAssign(self, s, env):
        if s.value is not None:
            self.assign(s.target, self.ev(s.value, env), env)

    def s_AugAssign(self, s, env):
        t = s.target
        op = BINOPS[type(s.op)]
        if isinstance(t, ast.Name):
            cur = self.load(t.id, env)
            if isinstance(cur, list) and isinstance(s.op, ast.Add):
                cur += self.ev(s.value, env)
                self.store(t.id, cur, env)
            else:
                self.store(t.id, op(cur, self.ev(s.value, env)), env)
        elif isinstance(t, ast.Subscript):
            obj, idx = self.ev(t.value, env), self.ev(t.slice, env)
            obj[idx] = op(obj[idx], self.ev(s.value, env))
        else:
            obj = self.ev(t.value, env)
            setattr(obj, t.attr, op(getattr(obj, t.attr), self.ev(s.value, env)))

    def s_If(self, s, env):
        self.run(s.body if self.ev(s.test, env) else s.orelse, env)

    def s_For(self, s, env):
        broke = False
        for item in self.ev(s.iter, env):
            self.assign(s.target, item, env)
            try:
                self.run(s.body, env)
            except _Break:
                broke = True
                break
            except _Continue:
                continue
        if not broke:
            self.run(s.orelse, env)

    def s_While(self, s, env):
        broke = False
        while self.ev(s.test, env):
            try:
                self.run(s.body, env)
            except _Break:
                broke = True
                break
            except _Continue:
                continue
        if not broke:
            self.run(s.orelse, env)

    def s_Break(self, s, env):
        raise _Break()

    def s_Continue(self, s, env):
        raise _Continue()

    def s_Return(self, s, env):
        raise _Return(self.ev(s.value, env) if s.value is not None else None)

    def s_Global(self, s, env):
        for n in s.names:
            env.declared[n] = "global"

    def s_Nonlocal(self, s, env):
        for n in s.names:
            env.declared[n] = "nonlocal"

    def s_Assert(self, s, env):
        if not self.ev(s.test, env):
            raise AssertionError(self.ev(s.msg, env) if s.msg else "")

    def s_Raise(self, s, env):
        if s.exc is None:
            raise RuntimeError("re-raise outside handler")
        e = self.ev(s.exc, env)
        raise e() if isinstance(e, type) else e

    def s_Import(self, s, env):
        import importlib
        for a in s.names:
            self.store((a.asname or a.name).split(".")[0], importlib.import_module(a.name), env)

    def s_ImportFrom(self, s, env):
        import importlib
        mod = importlib.import_module(s.module)
        for a in s.names:
            self.store(a.asname or a.name, getattr(mod, a.name), env)

    def s_FunctionDef(self, s, env):
        f = self.make_func(s.name, s.args, s.body, env)
        self.store(s.name, f, env)

    def s_ClassDef(self, s, env):
        bases = [self.ev(b, env) for b in s.bases]
        body = Scope(env, None, "class")
        self.run(s.body, body)
        ns = {k: v for k, v in body.vars.items() if not k.startswith("__func__")}
        cls = BClass(s.name, bases or [self.object_cls], ns)
        for v in ns.values():
            if isinstance(v, BFunc):
                v.defclass = cls
        self.store(s.name, cls, env)

    def s_Try(self, s, env):
        try:
            try:
                self.run(s.body, env)
            except (_Break, _Continue, _Return, _Budget):
                raise
            except Exception as exc:  # noqa: BLE001
                for h in s.handlers:
                    if h.type is None or isinstance(exc, self._classes(self.ev(h.type, env))):
                        if h.name:
                            self.store(h.name, exc, env)
                        self.run(h.body, env)
                        break
                else:
                    raise
            else:
                self.run(s.orelse, env)
        finally:
            self.run(s.finalbody, env)

    @staticmethod
    def _classes(c):
        return c if isinstance(c, tuple) else (c,)


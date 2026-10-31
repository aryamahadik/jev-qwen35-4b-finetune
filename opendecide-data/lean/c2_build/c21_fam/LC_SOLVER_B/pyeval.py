"""Solver B: an own tree-walking evaluator for the rendered Python subset (parsing = stdlib `ast`; nothing is exec'd).

Values: host ints / strs / bools / lists / dicts / tuples / sets stand for themselves (so aliasing, floor division, exceptions of
host operations behave exactly like CPython). Own objects: PyClass, PyInst, PyFunc, BoundMethod, PyModule. User exceptions are
PyInst wrapped in PyRaise. A small pytest model (collection, skip/xfail marks, raises, conftest hooks incl. the hookwrapper
`yield`) is at the bottom.
"""
import ast
import builtins as _b

from .common import Budget, Thrown, Timeout, Unsupported

_EXC_NAMES = ["BaseException", "Exception", "ArithmeticError", "AssertionError", "AttributeError", "IndexError", "KeyError",
              "LookupError", "NameError", "NotImplementedError", "OverflowError", "RecursionError", "RuntimeError",
              "StopIteration", "TypeError", "UnboundLocalError", "ValueError", "ZeroDivisionError", "OSError", "SystemExit",
              "KeyboardInterrupt", "EOFError", "ImportError", "UnicodeError", "FloatingPointError", "MemoryError",
              "PermissionError", "FileNotFoundError", "TimeoutError", "StopAsyncIteration", "GeneratorExit"]
HOST_EXC = {n: getattr(_b, n) for n in _EXC_NAMES}
_SAFE_CALLS = ["len", "min", "max", "sum", "abs", "range", "sorted", "reversed", "enumerate", "zip", "any", "all", "int", "str",
               "bool", "float", "list", "dict", "set", "tuple", "frozenset", "repr", "round", "divmod", "pow", "ord", "chr",
               "isinstance", "issubclass", "map", "filter", "hash", "bytes", "format", "iter", "next", "slice", "ascii", "bin",
               "hex", "oct"]
HOST_FUNCS = {n: getattr(_b, n) for n in _SAFE_CALLS}
HOST_TYPES = {"int": int, "str": str, "bool": bool, "float": float, "list": list, "dict": dict, "set": set, "tuple": tuple,
              "object": object}


class PyRaise(Exception):
    def __init__(self, inst):
        Exception.__init__(self, inst.cls.name)
        self.inst = inst


class _Return(Exception):
    def __init__(self, v):
        self.v = v


class _Break(Exception):
    pass


class _Continue(Exception):
    pass


class PyClass:
    def __init__(self, name, bases, attrs):
        self.name = name
        self.bases = bases                 # PyClass or host types
        self.attrs = attrs
        self.mro = [self]
        for b in bases:
            for c in (b.mro if isinstance(b, PyClass) else [b]):
                if c not in self.mro:
                    self.mro.append(c)

    def host_bases(self):
        return [c for c in self.mro if not isinstance(c, PyClass)]

    def lookup(self, name):
        for c in self.mro:
            if isinstance(c, PyClass) and name in c.attrs:
                return c.attrs[name]
        raise KeyError(name)

    def is_exc(self):
        return any(isinstance(c, type) and issubclass(c, BaseException) for c in self.host_bases())

    def base_type(self):
        for c in self.host_bases():
            if c in (int, str, list, dict, tuple, float, set):
                return c
        return None


class PyInst:
    def __init__(self, cls):
        self.cls = cls
        self.d = {}
        self.base = None
        self.args = ()


class PyFunc:
    def __init__(self, node, scope, interp, name=None):
        self.node = node
        self.scope = scope
        self.interp = interp
        self.name = name or node.name
        self.marks = []
        self.kind = "plain"
        self.is_hook = False
        self.is_fixture = None
        a = node.args
        self.pos = [x.arg for x in a.posonlyargs + a.args]
        self.defaults = {}
        ds = a.defaults
        for nm, d in zip(self.pos[len(self.pos) - len(ds):], ds):
            self.defaults[nm] = interp.eval(d, scope)
        self.kwonly = [x.arg for x in a.kwonlyargs]
        for nm, d in zip(self.kwonly, a.kw_defaults):
            if d is not None:
                self.defaults[nm] = interp.eval(d, scope)
        self.vararg = a.vararg.arg if a.vararg else None
        self.kwarg = a.kwarg.arg if a.kwarg else None
        self.locals = _locals_of(node)
        self.is_gen = any(isinstance(n, (ast.Yield, ast.YieldFrom)) for n in _walk_scope(node))

    def __call__(self, *args, **kw):          # lets host builtins (sorted key=, map ...) call back into rendered code
        return self.interp.call(self, list(args), dict(kw))


class BoundMethod:
    def __init__(self, func, obj):
        self.func = func
        self.obj = obj

    def __call__(self, *args, **kw):
        return self.func.interp.call(self.func, [self.obj] + list(args), dict(kw))


class PyModule:
    def __init__(self, name):
        self.name = name
        self.vars = {}


class Scope:
    __slots__ = ("vars", "parent", "kind", "locals", "globals_decl", "mod")

    def __init__(self, parent, kind, mod, locals_=None):
        self.vars = {}
        self.parent = parent
        self.kind = kind
        self.locals = locals_
        self.globals_decl = set()
        self.mod = mod


def _walk_scope(node):
    """Nodes of one function scope (not entering nested defs, lambdas or comprehensions)."""
    stack = list(ast.iter_child_nodes(node))
    while stack:
        n = stack.pop()
        yield n
        if isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.Lambda, ast.AsyncFunctionDef)):
            continue
        stack.extend(ast.iter_child_nodes(n))


def _locals_of(fn):
    names = set()
    a = fn.args
    for x in a.posonlyargs + a.args + a.kwonlyargs:
        names.add(x.arg)
    if a.vararg:
        names.add(a.vararg.arg)
    if a.kwarg:
        names.add(a.kwarg.arg)
    glob, nonl = set(), set()
    for n in _walk_scope(fn):
        if isinstance(n, ast.Name) and isinstance(n.ctx, (ast.Store, ast.Del)):
            names.add(n.id)
        elif isinstance(n, (ast.FunctionDef, ast.ClassDef)):
            names.add(n.name)
        elif isinstance(n, (ast.Import, ast.ImportFrom)):
            for al in n.names:
                names.add((al.asname or al.name).split(".")[0])
        elif isinstance(n, ast.ExceptHandler) and n.name:
            names.add(n.name)
        elif isinstance(n, ast.Global):
            glob.update(n.names)
        elif isinstance(n, ast.Nonlocal):
            nonl.update(n.names)
    return frozenset(names - glob - nonl)


class _Mark:
    def __init__(self, kind, args, kw):
        self.kind, self.args, self.kw = kind, args, kw


class _MarkNS:
    def __getattr__(self, kind):
        if kind.startswith("_"):
            raise AttributeError(kind)
        return lambda *a, **k: _Mark(kind, a, k)


class _RaisesCtx:
    def __init__(self, spec):
        self.spec = spec


class _Pytest:
    mark = _MarkNS()

    def raises(self, spec, *a, **k):
        return _RaisesCtx(spec)

    def hookimpl(self, *a, **k):
        return _Mark("hookimpl", a, k)

    def fixture(self, *a, **k):
        if len(a) == 1 and isinstance(a[0], PyFunc) and not k:
            a[0].is_fixture = {"autouse": False}
            return a[0]
        return _Mark("fixture", a, k)

    def skip(self, reason=""):
        raise _PytestSkip(reason)

    def fail(self, reason=""):
        raise AssertionError(reason)


class _PytestSkip(Exception):
    pass


PYTEST = _Pytest()


class Interp:
    def __init__(self, files, budget=None, max_depth=120):
        self.files = {p: t for p, t in files.items() if p.endswith(".py")}
        self.budget = budget or Budget()
        self.modules = {}
        self.depth = 0
        self.max_depth = max_depth
        self.stdout = []
        self.yield_value = None
        self.modnames = {p[:-3].replace("/", "."): p for p in self.files}

    # ------------------------------------------------------------------ modules
    def load(self, name):
        if name in self.modules:
            return self.modules[name]
        if name == "pytest":
            return PYTEST
        if name not in self.modnames:
            raise HOST_EXC["ImportError"]("no module %s" % name)
        m = PyModule(name)
        self.modules[name] = m
        try:
            tree = ast.parse(self.files[self.modnames[name]])
        except SyntaxError as e:
            del self.modules[name]
            raise Unsupported("syntax %s" % e)
        sc = Scope(None, "module", m)
        sc.vars = m.vars
        try:
            self.exec_body(tree.body, sc)
        except BaseException:
            self.modules.pop(name, None)
            raise
        return m

    # ------------------------------------------------------------------ statements
    def exec_body(self, body, sc):
        for st in body:
            self.exec_stmt(st, sc)

    def exec_stmt(self, st, sc):
        self.budget.tick()
        m = getattr(self, "s_" + type(st).__name__, None)
        if m is None:
            raise Unsupported("stmt " + type(st).__name__)
        m(st, sc)

    def s_Expr(self, st, sc):
        self.eval(st.value, sc)

    def s_Pass(self, st, sc):
        pass

    def s_Global(self, st, sc):
        sc.globals_decl.update(st.names)

    def s_Nonlocal(self, st, sc):
        raise Unsupported("nonlocal")

    def s_Assign(self, st, sc):
        v = self.eval(st.value, sc)
        for t in st.targets:
            self.assign(t, v, sc)

    def s_AnnAssign(self, st, sc):
        if st.value is not None:
            self.assign(st.target, self.eval(st.value, sc), sc)

    def s_AugAssign(self, st, sc):
        cur = self.eval(self._as_load(st.target), sc)
        v = self.binop(type(st.op), cur, self.eval(st.value, sc))
        self.assign(st.target, v, sc)

    @staticmethod
    def _as_load(t):
        if isinstance(t, ast.Name):
            return ast.Name(id=t.id, ctx=ast.Load())
        if isinstance(t, ast.Attribute):
            return ast.Attribute(value=t.value, attr=t.attr, ctx=ast.Load())
        if isinstance(t, ast.Subscript):
            return ast.Subscript(value=t.value, slice=t.slice, ctx=ast.Load())
        raise Unsupported("augassign target")

    def s_Return(self, st, sc):
        raise _Return(self.eval(st.value, sc) if st.value is not None else None)

    def s_If(self, st, sc):
        if self.truth(self.eval(st.test, sc)):
            self.exec_body(st.body, sc)
        else:
            self.exec_body(st.orelse, sc)

    def s_While(self, st, sc):
        while self.truth(self.eval(st.test, sc)):
            self.budget.tick()
            try:
                self.exec_body(st.body, sc)
            except _Break:
                return
            except _Continue:
                continue
        self.exec_body(st.orelse, sc)

    def s_For(self, st, sc):
        it = self.eval(st.iter, sc)
        for v in self.iterate(it):
            self.budget.tick()
            self.assign(st.target, v, sc)
            try:
                self.exec_body(st.body, sc)
            except _Break:
                return
            except _Continue:
                continue
        self.exec_body(st.orelse, sc)

    def s_Break(self, st, sc):
        raise _Break()

    def s_Continue(self, st, sc):
        raise _Continue()

    def s_Assert(self, st, sc):
        if not self.truth(self.eval(st.test, sc)):
            raise AssertionError(self.eval(st.msg, sc) if st.msg is not None else "")

    def s_Delete(self, st, sc):
        for t in st.targets:
            if isinstance(t, ast.Subscript):
                o = self.eval(t.value, sc)
                del o[self.eval(t.slice, sc)]
            elif isinstance(t, ast.Name):
                sc.vars.pop(t.id, None)
            else:
                raise Unsupported("del target")

    def s_Raise(self, st, sc):
        if st.exc is None:
            cur = getattr(self, "_current_exc", None)
            if cur is None:
                raise HOST_EXC["RuntimeError"]("No active exception to reraise")
            raise cur
        e = self.eval(st.exc, sc)
        raise self.make_exc(e)

    def make_exc(self, e):
        if isinstance(e, PyClass):
            e = self.instantiate(e, [], {})
        if isinstance(e, PyInst):
            if not e.cls.is_exc():
                return HOST_EXC["TypeError"]("exceptions must derive from BaseException")
            return PyRaise(e)
        if isinstance(e, type) and issubclass(e, BaseException):
            return e()
        if isinstance(e, BaseException):
            return e
        return HOST_EXC["TypeError"]("exceptions must derive from BaseException")

    def s_Try(self, st, sc):
        try:
            try:
                self.exec_body(st.body, sc)
            except (_Return, _Break, _Continue):
                raise
            except (Unsupported, Timeout, _PytestSkip):
                raise
            except BaseException as e:
                prev = getattr(self, "_current_exc", None)
                for h in st.handlers:
                    if h.type is None or self.exc_matches(e, self.eval(h.type, sc)):
                        if h.name:
                            sc.vars[h.name] = e.inst if isinstance(e, PyRaise) else e
                        self._current_exc = e
                        try:
                            self.exec_body(h.body, sc)
                        finally:
                            self._current_exc = prev
                        break
                else:
                    raise
            else:
                self.exec_body(st.orelse, sc)
        finally:
            if st.finalbody:
                self.exec_body(st.finalbody, sc)

    def exc_matches(self, e, spec):
        if isinstance(spec, tuple):
            return any(self.exc_matches(e, s) for s in spec)
        if isinstance(spec, PyClass):
            return isinstance(e, PyRaise) and spec in e.inst.cls.mro
        if isinstance(spec, type) and issubclass(spec, BaseException):
            if isinstance(e, PyRaise):
                return any(isinstance(c, type) and issubclass(c, spec) for c in e.inst.cls.host_bases())
            return isinstance(e, spec)
        raise HOST_EXC["TypeError"]("catching classes that do not inherit from BaseException is not allowed")

    def s_With(self, st, sc):
        if len(st.items) != 1:
            raise Unsupported("with items")
        it = st.items[0]
        ctx = self.eval(it.context_expr, sc)
        if not isinstance(ctx, _RaisesCtx):
            raise Unsupported("with context")
        try:
            self.exec_body(st.body, sc)
        except (_Return, _Break, _Continue, Unsupported, Timeout, _PytestSkip):
            raise
        except BaseException as e:
            if self.exc_matches(e, ctx.spec):
                if it.optional_vars is not None:
                    self.assign(it.optional_vars, e.inst if isinstance(e, PyRaise) else e, sc)
                return
            raise
        raise AssertionError("DID NOT RAISE")

    def s_Import(self, st, sc):
        for al in st.names:
            mod = self.load(al.name)
            self.set_name((al.asname or al.name).split(".")[0], mod, sc)

    def s_ImportFrom(self, st, sc):
        if st.level:
            raise Unsupported("relative import")
        mod = self.load(st.module)
        for al in st.names:
            if isinstance(mod, PyModule):
                if al.name not in mod.vars:
                    raise HOST_EXC["ImportError"]("cannot import name %s" % al.name)
                v = mod.vars[al.name]
            else:
                v = getattr(mod, al.name)
            self.set_name(al.asname or al.name, v, sc)

    def s_FunctionDef(self, st, sc):
        val = fn = PyFunc(st, self._func_scope(sc), self)
        for d in reversed(st.decorator_list):
            dv = self.eval(d, sc)
            val = self.apply_decorator(dv, val, d)
        self.set_name(st.name, val, sc)

    def _func_scope(self, sc):
        s = sc
        while s is not None and s.kind == "class":
            s = s.parent
        return s

    def apply_decorator(self, dv, val, node):
        if isinstance(dv, _Mark):
            target = val
            if dv.kind == "hookimpl":
                if isinstance(target, PyFunc):
                    target.is_hook = True
                return target
            if dv.kind == "fixture":
                if isinstance(target, PyFunc):
                    target.is_fixture = {"autouse": bool(dv.kw.get("autouse"))}
                return target
            if isinstance(target, PyFunc):
                target.marks.append(dv)
                return target
            if isinstance(target, PyClass):
                target.attrs.setdefault("__marks__", []).append(dv)
                return target
            raise Unsupported("mark target")
        if isinstance(dv, PyClass) or isinstance(dv, (PyFunc, BoundMethod)) or callable(dv):
            if isinstance(dv, PyFunc) and dv.node.name in ("staticmethod",):
                pass
            return self.call(dv, [val], {})
        raise Unsupported("decorator")

    def s_ClassDef(self, st, sc):
        bases = []
        for b in st.bases:
            bv = self.eval(b, sc)
            if isinstance(bv, PyClass):
                bases.append(bv)
            elif isinstance(bv, type):
                bases.append(bv)
            else:
                raise Unsupported("class base")
        if st.keywords:
            raise Unsupported("class keywords")
        body = Scope(sc, "class", sc.mod)
        self.exec_body(st.body, body)
        cls = PyClass(st.name, bases, body.vars)
        val = cls
        for d in reversed(st.decorator_list):
            val = self.apply_decorator(self.eval(d, sc), val, d)
        self.set_name(st.name, val, sc)

    # ------------------------------------------------------------------ names and assignment
    def set_name(self, name, v, sc):
        if name in sc.globals_decl:
            sc.mod.vars[name] = v
        else:
            sc.vars[name] = v

    def assign(self, t, v, sc):
        if isinstance(t, ast.Name):
            self.set_name(t.id, v, sc)
        elif isinstance(t, ast.Attribute):
            o = self.eval(t.value, sc)
            self.setattr(o, t.attr, v)
        elif isinstance(t, ast.Subscript):
            o = self.eval(t.value, sc)
            k = self.eval(t.slice, sc)
            if isinstance(o, PyInst):
                raise Unsupported("setitem on instance")
            o[k] = v
        elif isinstance(t, (ast.Tuple, ast.List)):
            vals = list(self.iterate(v))
            tgts = t.elts
            if any(isinstance(x, ast.Starred) for x in tgts):
                raise Unsupported("starred target")
            if len(vals) != len(tgts):
                raise HOST_EXC["ValueError"]("unpack mismatch")
            for tt, vv in zip(tgts, vals):
                self.assign(tt, vv, sc)
        else:
            raise Unsupported("target " + type(t).__name__)

    def lookup(self, name, sc):
        s = sc
        while s is not None:
            if s.kind == "class" and s is not sc:
                s = s.parent
                continue
            if s.kind == "func":
                if name in s.globals_decl:
                    break
                if name in s.locals:
                    if name in s.vars:
                        return s.vars[name]
                    if s is sc:
                        raise HOST_EXC["UnboundLocalError"]("local variable %r referenced before assignment" % name)
                    raise HOST_EXC["NameError"]("free variable %r referenced before assignment" % name)
            elif name in s.vars:
                return s.vars[name]
            s = s.parent
        if name in sc.mod.vars:
            return sc.mod.vars[name]
        if name in HOST_FUNCS:
            return HOST_FUNCS[name]
        if name in HOST_EXC:
            return HOST_EXC[name]
        if name in HOST_TYPES:
            return HOST_TYPES[name]
        if name == "print":
            return lambda *a, **k: self.stdout.append(" ".join(str(x) for x in a))
        raise HOST_EXC["NameError"]("name %r is not defined" % name)

    # ------------------------------------------------------------------ expressions
    def eval(self, node, sc):
        self.budget.tick()
        m = getattr(self, "e_" + type(node).__name__, None)
        if m is None:
            raise Unsupported("expr " + type(node).__name__)
        return m(node, sc)

    def e_Constant(self, n, sc):
        return n.value

    def e_Name(self, n, sc):
        return self.lookup(n.id, sc)

    def e_List(self, n, sc):
        return [self.eval(x, sc) for x in n.elts]

    def e_Tuple(self, n, sc):
        return tuple(self.eval(x, sc) for x in n.elts)

    def e_Set(self, n, sc):
        return {self.eval(x, sc) for x in n.elts}

    def e_Dict(self, n, sc):
        d = {}
        for k, v in zip(n.keys, n.values):
            if k is None:
                d.update(self.eval(v, sc))
            else:
                d[self.eval(k, sc)] = self.eval(v, sc)
        return d

    def e_JoinedStr(self, n, sc):
        out = []
        for p in n.values:
            if isinstance(p, ast.Constant):
                out.append(p.value)
            else:
                v = self.eval(p.value, sc)
                spec = ""
                if p.format_spec is not None:
                    spec = "".join(x.value for x in p.format_spec.values if isinstance(x, ast.Constant))
                if p.conversion == 114:
                    v = repr(v)
                out.append(format(self.unwrap(v), spec))
        return "".join(out)

    def e_BoolOp(self, n, sc):
        if isinstance(n.op, ast.And):
            v = None
            for x in n.values:
                v = self.eval(x, sc)
                if not self.truth(v):
                    return v
            return v
        v = None
        for x in n.values:
            v = self.eval(x, sc)
            if self.truth(v):
                return v
        return v

    def e_UnaryOp(self, n, sc):
        v = self.eval(n.operand, sc)
        if isinstance(n.op, ast.Not):
            return not self.truth(v)
        v = self.unwrap(v)
        if isinstance(n.op, ast.USub):
            return -v
        if isinstance(n.op, ast.UAdd):
            return +v
        if isinstance(n.op, ast.Invert):
            return ~v
        raise Unsupported("unary")

    def e_BinOp(self, n, sc):
        return self.binop(type(n.op), self.eval(n.left, sc), self.eval(n.right, sc))

    _DUNDER = {ast.Add: "__add__", ast.Sub: "__sub__", ast.Mult: "__mul__", ast.Mod: "__mod__", ast.FloorDiv: "__floordiv__",
               ast.Div: "__truediv__"}

    def binop(self, op, a, b):
        if isinstance(a, PyInst) or isinstance(b, PyInst):
            dn = self._DUNDER.get(op)
            if isinstance(a, PyInst) and dn:
                try:
                    f = a.cls.lookup(dn)
                    return self.call(f, [a, b], {})
                except KeyError:
                    pass
            a, b = self.unwrap(a), self.unwrap(b)
        if op is ast.Add:
            return a + b
        if op is ast.Sub:
            return a - b
        if op is ast.Mult:
            return a * b
        if op is ast.Div:
            return a / b
        if op is ast.FloorDiv:
            return a // b
        if op is ast.Mod:
            return a % b
        if op is ast.Pow:
            return a ** b
        if op is ast.BitAnd:
            return a & b
        if op is ast.BitOr:
            return a | b
        if op is ast.BitXor:
            return a ^ b
        if op is ast.LShift:
            return a << b
        if op is ast.RShift:
            return a >> b
        raise Unsupported("binop")

    def unwrap(self, v):
        if isinstance(v, PyInst):
            if v.base is not None:
                return v.base
            raise Unsupported("operation on plain instance")
        return v

    def e_Compare(self, n, sc):
        left = self.eval(n.left, sc)
        for op, c in zip(n.ops, n.comparators):
            right = self.eval(c, sc)
            if not self.cmp(type(op), left, right):
                return False
            left = right
        return True

    _CMP_D = {ast.Eq: "__eq__", ast.NotEq: "__ne__", ast.Lt: "__lt__", ast.LtE: "__le__", ast.Gt: "__gt__", ast.GtE: "__ge__"}

    def cmp(self, op, a, b):
        if op is ast.Is:
            return a is b
        if op is ast.IsNot:
            return a is not b
        if op is ast.In:
            return self.contains(b, a)
        if op is ast.NotIn:
            return not self.contains(b, a)
        if isinstance(a, PyInst) or isinstance(b, PyInst):
            dn = self._CMP_D[op]
            if isinstance(a, PyInst):
                try:
                    return self.truth(self.call(a.cls.lookup(dn), [a, b], {}))
                except KeyError:
                    pass
            if isinstance(b, PyInst):
                refl = {"__eq__": "__eq__", "__ne__": "__ne__", "__lt__": "__gt__", "__le__": "__ge__", "__gt__": "__lt__",
                        "__ge__": "__le__"}[dn]
                try:
                    return self.truth(self.call(b.cls.lookup(refl), [b, a], {}))
                except KeyError:
                    pass
            if op in (ast.Eq, ast.NotEq):
                if (isinstance(a, PyInst) and a.base is None) or (isinstance(b, PyInst) and b.base is None):
                    same = a is b
                    return same if op is ast.Eq else not same
            a, b = self.unwrap(a), self.unwrap(b)
        if op is ast.Eq:
            return a == b
        if op is ast.NotEq:
            return a != b
        if op is ast.Lt:
            return a < b
        if op is ast.LtE:
            return a <= b
        if op is ast.Gt:
            return a > b
        if op is ast.GtE:
            return a >= b
        raise Unsupported("cmp")

    def contains(self, container, x):
        if isinstance(container, PyInst):
            raise Unsupported("in on instance")
        return self.unwrap(x) in container if isinstance(x, PyInst) else x in container

    def truth(self, v):
        if isinstance(v, PyInst):
            for nm in ("__bool__", "__len__"):
                try:
                    f = v.cls.lookup(nm)
                except KeyError:
                    continue
                return bool(self.call(f, [v], {}))
            if v.base is not None:
                return bool(v.base)
            return True
        return bool(v)

    def e_IfExp(self, n, sc):
        return self.eval(n.body if self.truth(self.eval(n.test, sc)) else n.orelse, sc)

    def e_Lambda(self, n, sc):
        fake = ast.FunctionDef(name="<lambda>", args=n.args, body=[ast.Return(value=n.body)], decorator_list=[], returns=None)
        return PyFunc(fake, sc, self)

    def e_Yield(self, n, sc):
        return self.yield_value

    def iterate(self, it):
        if isinstance(it, PyInst):
            if it.base is not None and not isinstance(it.base, int):
                return iter(it.base)
            raise Unsupported("iterate instance")
        return iter(it)

    def _comp(self, n, sc, emit):
        inner = Scope(sc, "comp", sc.mod, frozenset())

        def rec(i):
            if i == len(n.generators):
                emit(inner)
                return
            g = n.generators[i]
            for v in self.iterate(self.eval(g.iter, inner if i else sc)):
                self.budget.tick()
                self.assign(g.target, v, inner)
                if all(self.truth(self.eval(c, inner)) for c in g.ifs):
                    rec(i + 1)
        rec(0)

    def e_ListComp(self, n, sc):
        out = []
        self._comp(n, sc, lambda s: out.append(self.eval(n.elt, s)))
        return out

    def e_SetComp(self, n, sc):
        out = set()
        self._comp(n, sc, lambda s: out.add(self.eval(n.elt, s)))
        return out

    def e_GeneratorExp(self, n, sc):
        return self.e_ListComp(n, sc)

    def e_DictComp(self, n, sc):
        out = {}
        self._comp(n, sc, lambda s: out.__setitem__(self.eval(n.key, s), self.eval(n.value, s)))
        return out

    def e_Starred(self, n, sc):
        raise Unsupported("starred expr")

    def e_Subscript(self, n, sc):
        o = self.eval(n.value, sc)
        k = self.eval(n.slice, sc)
        if isinstance(o, PyInst):
            if o.base is not None:
                return o.base[k]
            raise Unsupported("getitem on instance")
        return o[k]

    def e_Slice(self, n, sc):
        f = lambda x: self.eval(x, sc) if x is not None else None
        return slice(f(n.lower), f(n.upper), f(n.step))

    def e_Attribute(self, n, sc):
        return self.getattr(self.eval(n.value, sc), n.attr)

    def getattr(self, o, name):
        if isinstance(o, PyInst):
            if name in o.d:
                return o.d[name]
            try:
                v = o.cls.lookup(name)
            except KeyError:
                if name == "args" and o.cls.is_exc():
                    return o.args
                if o.base is not None and not name.startswith("_"):
                    return getattr(o.base, name)
                raise HOST_EXC["AttributeError"]("%s has no attribute %s" % (o.cls.name, name))
            if isinstance(v, PyFunc):
                if v.kind == "static":
                    return v
                return BoundMethod(v, o)
            return v
        if isinstance(o, PyClass):
            try:
                v = o.lookup(name)
            except KeyError:
                if name == "__name__":
                    return o.name
                for c in o.host_bases():
                    if hasattr(c, name) and name in ("__hash__", "__eq__", "__ne__"):
                        return getattr(c, name)
                raise HOST_EXC["AttributeError"](name)
            return v
        if isinstance(o, PyModule):
            if name in o.vars:
                return o.vars[name]
            raise HOST_EXC["AttributeError"](name)
        if isinstance(o, (PyFunc, BoundMethod)):
            if name == "__name__":
                return o.name if isinstance(o, PyFunc) else o.func.name
            raise HOST_EXC["AttributeError"](name)
        if isinstance(o, type) and name in ("__hash__", "__eq__", "__ne__"):
            return getattr(o, name)
        if name.startswith("_"):
            raise Unsupported("private attribute " + name)
        if isinstance(o, _Pytest) or isinstance(o, (_MarkNS, _OutObj, _Report, _Session)):
            return getattr(o, name)
        return getattr(o, name)

    def setattr(self, o, name, v):
        if isinstance(o, PyInst):
            o.d[name] = v
        elif isinstance(o, PyClass):
            o.attrs[name] = v
        elif isinstance(o, (_Report, _Session)):
            setattr(o, name, v)
        else:
            raise HOST_EXC["AttributeError"]("cannot set attribute %s" % name)

    def e_Call(self, n, sc):
        f = self.eval(n.func, sc)
        args = []
        for a in n.args:
            if isinstance(a, ast.Starred):
                args.extend(self.iterate(self.eval(a.value, sc)))
            else:
                args.append(self.eval(a, sc))
        kw = {}
        for k in n.keywords:
            if k.arg is None:
                kw.update(self.eval(k.value, sc))
            else:
                kw[k.arg] = self.eval(k.value, sc)
        return self.call(f, args, kw)

    # ------------------------------------------------------------------ calls
    def call(self, f, args, kw):
        if isinstance(f, BoundMethod):
            return self.call(f.func, [f.obj] + args, kw)
        if isinstance(f, PyFunc):
            return self.call_func(f, args, kw)
        if isinstance(f, PyClass):
            return self.instantiate(f, args, kw)
        if isinstance(f, PyInst):
            try:
                m = f.cls.lookup("__call__")
            except KeyError:
                raise HOST_EXC["TypeError"]("object is not callable")
            return self.call(m, [f] + args, kw)
        if callable(f):
            return f(*args, **kw)
        raise HOST_EXC["TypeError"]("object is not callable")

    def call_func(self, f, args, kw):
        if self.depth >= self.max_depth:
            raise HOST_EXC["RecursionError"]("maximum recursion depth exceeded")
        sc = Scope(f.scope, "func", f.scope.mod if f.scope else None, f.locals)
        v = sc.vars
        pos = f.pos
        if len(args) > len(pos) and f.vararg is None:
            raise HOST_EXC["TypeError"]("too many positional arguments")
        for nm, a in zip(pos, args):
            v[nm] = a
        if f.vararg:
            v[f.vararg] = tuple(args[len(pos):])
        extra = {}
        for k, a in kw.items():
            if k in pos or k in f.kwonly:
                if k in v:
                    raise HOST_EXC["TypeError"]("multiple values for argument %s" % k)
                v[k] = a
            elif f.kwarg:
                extra[k] = a
            else:
                raise HOST_EXC["TypeError"]("unexpected keyword argument %s" % k)
        if f.kwarg:
            v[f.kwarg] = extra
        for nm in pos + f.kwonly:
            if nm not in v:
                if nm in f.defaults:
                    v[nm] = f.defaults[nm]
                else:
                    raise HOST_EXC["TypeError"]("missing required argument %s" % nm)
        self.depth += 1
        try:
            try:
                self.exec_body(f.node.body, sc)
            except _Return as r:
                return r.v
            except (_Break, _Continue):
                raise Unsupported("break outside loop")
            return None
        finally:
            self.depth -= 1

    def instantiate(self, cls, args, kw):
        inst = PyInst(cls)
        bt = cls.base_type()
        if bt is not None:
            try:
                init = cls.lookup("__init__")
            except KeyError:
                init = None
            if init is None:
                inst.base = bt(*args)
            else:
                self.call(init, [inst] + list(args), kw)
                return inst
        else:
            inst.args = tuple(args)
            try:
                init = cls.lookup("__init__")
            except KeyError:
                init = None
            if init is not None:
                self.call(init, [inst] + list(args), kw)
            elif args and not cls.is_exc():
                raise HOST_EXC["TypeError"]("takes no arguments")
        return inst


# ------------------------------------------------------------------------------------------------ naming
def exc_name(e):
    if isinstance(e, PyRaise):
        return e.inst.cls.name
    return type(e).__name__


def to_plain(v):
    if isinstance(v, PyInst):
        if v.base is not None:
            return to_plain(v.base)
        return {"__obj__": v.cls.name, **{k: to_plain(x) for k, x in v.d.items()}}
    if isinstance(v, (list, tuple)):
        return [to_plain(x) for x in v]
    if isinstance(v, dict):
        return {k: to_plain(x) for k, x in v.items()}
    if isinstance(v, (set, frozenset)):
        return sorted(to_plain(x) for x in v)
    if isinstance(v, (PyFunc, BoundMethod, PyClass)):
        return "<callable>"
    return v


# ------------------------------------------------------------------------------------------------ structured calls
def find_owner_class(interp, fn, mods):
    """The PyClass (in `mods`) that defines method `fn`, else None."""
    for m in mods:
        for v in m.vars.values():
            if isinstance(v, PyClass) and fn in v.attrs:
                return v
    return None


def py_call_sequence(files, calls, budget=None):
    """Run `calls` ([{fn,args}]) in order on one fresh instance (when a call is a method). Return a list of outcomes
    ('ok', plain) / ('exc', name) per call (earlier outcomes included)."""
    it = Interp(files, budget)
    mods = [it.load(n) for n in it.modnames if not _is_test_name(n)]
    inst = None
    outs = []
    for c in calls:
        fn = c["fn"]
        args = [_arg(a) for a in c["args"]]
        try:
            f = None
            for m in mods:
                if fn in m.vars and isinstance(m.vars[fn], PyFunc):
                    f = m.vars[fn]
                    break
            if f is None:
                cls = find_owner_class(it, fn, mods)
                if cls is None:
                    raise Unsupported("no callable " + fn)
                if inst is None:
                    inst = it.instantiate(cls, [], {})
                f = cls.attrs[fn]
                r = it.call(f, [inst] + args, {})
            else:
                r = it.call(f, args, {})
            outs.append(("ok", to_plain(r)))
        except (Unsupported, Timeout):
            raise
        except BaseException as e:
            if isinstance(e, (_Return, _Break, _Continue, KeyboardInterrupt, SystemExit)):
                raise
            outs.append(("exc", exc_name(e)))
    return outs


def _arg(a):
    import copy
    return copy.deepcopy(a)


def _is_test_name(n):
    b = n.rsplit(".", 1)[-1]
    return b.startswith("test_") or b.endswith("_test") or b == "conftest"


class PyProgram:
    """A rendered Python tree loaded once; supports many fresh-instance call sequences (EQV2 enumeration)."""

    def __init__(self, files, budget=None):
        self.files = files
        self.budget = budget or Budget(20_000_000)
        self.it = Interp(files, self.budget)
        self.mods = [self.it.load(n) for n in self.it.modnames if not _is_test_name(n)]

    def func(self, fn):
        for m in self.mods:
            if fn in m.vars and isinstance(m.vars[fn], PyFunc):
                return m.vars[fn], None
        cls = find_owner_class(self.it, fn, self.mods)
        if cls is None:
            raise Unsupported("no callable " + fn)
        return cls.attrs[fn], cls

    def fresh(self, fn):
        f, cls = self.func(fn)
        return None if cls is None else self.it.instantiate(cls, [], {})

    def class_of_any(self, fns):
        for fn in fns:
            _, c = self.func(fn)
            if c is not None:
                return c
        return None

    def invoke(self, inst, fn, args):
        f, cls = self.func(fn)
        try:
            if cls is None:
                r = self.it.call(f, [_arg(a) for a in args], {})
            else:
                r = self.it.call(f, [inst] + [_arg(a) for a in args], {})
            return ("ok", to_plain(r))
        except (Unsupported, Timeout):
            raise
        except (_Return, _Break, _Continue):
            raise Unsupported("flow leak")
        except BaseException as e:
            return ("exc", exc_name(e))


# ------------------------------------------------------------------------------------------------ test running (plain + pytest model)
class _Report:
    def __init__(self, outcome):
        self.outcome = outcome


class _Session:
    def __init__(self, st):
        self.exitstatus = st


class _OutObj:
    def __init__(self, rep):
        self.rep = rep

    def get_result(self):
        return self.rep


def run_python_tests(files, mode="pytest", only=None, budget=None):
    """Run the tests in `files` ({path: text}). mode 'plain': import each test file and call every test_* function, any
    BaseException = failure (T42c TFAIL2 harness). mode 'pytest': the model of `pytest` (collection of test_*.py / *_test.py,
    skip / xfail marks, raises, conftest hookwrappers and sessionfinish).  `only`: restrict to these test file paths.
    Returns {'outcomes': {id: outcome}, 'exit': int, 'collected': n, 'error': str|None}."""
    it = Interp(files, budget)
    paths = sorted(p for p in files if p.endswith(".py"))
    tests = [p for p in paths if (p.rsplit("/", 1)[-1].startswith("test_") or p.endswith("_test.py")) and
             (only is None or p in only)]
    out = {"outcomes": {}, "exit": 0, "collected": 0, "error": None}
    hooks = {"makereport": [], "sessionfinish": []}
    autouse = []
    fixtures = {}
    if mode == "pytest" and "conftest.py" in files:
        try:
            cm = it.load("conftest")
        except (Unsupported, Timeout):
            raise
        except BaseException as e:
            out["exit"] = 4
            out["error"] = "conftest " + exc_name(e)
            return out
        for k, v in cm.vars.items():
            if isinstance(v, PyFunc):
                if k == "pytest_runtest_makereport":
                    hooks["makereport"].append(v)
                elif k == "pytest_sessionfinish":
                    hooks["sessionfinish"].append(v)
                elif k in ("pytest_collection_modifyitems", "pytest_configure", "pytest_runtest_call", "pytest_runtest_setup",
                           "pytest_pyfunc_call", "pytest_collection_finish", "pytest_report_teststatus", "pytest_unconfigure",
                           "pytest_terminal_summary", "pytest_exception_interact", "pytest_runtest_logreport"):
                    raise Unsupported("hook " + k)
                elif v.is_fixture is not None:
                    fixtures[k] = v
                    if v.is_fixture.get("autouse"):
                        autouse.append(v)
    failed = False
    for p in tests:
        modname = p[:-3].replace("/", ".")
        try:
            mod = it.load(modname)
        except (Unsupported, Timeout):
            raise
        except BaseException as e:
            out["outcomes"][p + "::<collect>"] = "error"
            failed = True
            continue
        for k, v in mod.vars.items():
            if isinstance(v, PyFunc) and v.is_fixture is not None:
                fixtures[k] = v
                if v.is_fixture.get("autouse"):
                    autouse.append(v)
        items = []
        for k, v in list(mod.vars.items()):
            if isinstance(v, PyFunc) and k.startswith("test") and v.is_fixture is None:
                items.append((p + "::" + k, v, None, []))
            elif isinstance(v, PyClass) and k.startswith("Test"):
                cmarks = v.attrs.get("__marks__", [])
                for mk, mv in v.attrs.items():
                    if isinstance(mv, PyFunc) and mk.startswith("test"):
                        items.append((p + "::" + k + "::" + mk, mv, v, cmarks))
        for tid, fn, cls, cmarks in items:
            out["collected"] += 1
            outcome = _run_one(it, fn, cls, cmarks, mode, fixtures, autouse)
            if mode == "pytest":
                rep = _Report(outcome)
                for h in hooks["makereport"]:
                    it.yield_value = _OutObj(rep)
                    it.call(h, [None, None], {})
                outcome = rep.outcome
            out["outcomes"][tid] = outcome
            if outcome in ("failed", "error"):
                failed = True
    if mode == "plain":
        out["exit"] = 1 if failed else 0
        return out
    if out["collected"] == 0 and not failed:
        out["exit"] = 5
    else:
        out["exit"] = 1 if failed else 0
    if hooks["sessionfinish"]:
        s = _Session(out["exit"])
        for h in hooks["sessionfinish"]:
            it.call(h, [s, out["exit"]], {})
        out["exit"] = s.exitstatus
    return out


def _run_one(it, fn, cls, cmarks, mode, fixtures, autouse):
    marks = list(fn.marks) + list(cmarks)
    skip = False
    xfail = False
    for m in marks:
        if m.kind == "skip":
            skip = True
        elif m.kind == "skipif":
            cond = m.args[0] if m.args else False
            if cond:
                skip = True
        elif m.kind == "xfail":
            xfail = True
        elif m.kind == "parametrize":
            raise Unsupported("parametrize")
        elif m.kind in ("usefixtures", "timeout", "filterwarnings"):
            pass
        else:
            pass
    if skip and mode == "pytest":
        return "skipped"
    try:
        args = []
        for nm in fn.pos:
            if nm == "self":
                continue
            if nm in fixtures:
                f = fixtures[nm]
                if f.is_gen:
                    raise Unsupported("yield fixture")
                args.append(it.call(f, [], {}))
            else:
                raise Unsupported("unknown fixture " + nm)
        for f in autouse:
            if f.is_gen:
                raise Unsupported("yield fixture")
            it.call(f, [], {})
        if cls is not None:
            inst = it.instantiate(cls, [], {})
            it.call(fn, [inst] + args, {})
        else:
            it.call(fn, args, {})
    except _PytestSkip:
        return "skipped" if mode == "pytest" else "failed"
    except (Unsupported, Timeout):
        raise
    except (_Return, _Break, _Continue):
        raise Unsupported("flow leak")
    except BaseException:
        if xfail and mode == "pytest":
            return "xfailed"
        return "failed"
    if xfail and mode == "pytest":
        return "xpassed"
    return "passed"

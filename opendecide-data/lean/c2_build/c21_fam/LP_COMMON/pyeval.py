"""PyEval: a restricted, SAFE tree-walking evaluator for the Python subset the L-P generators render (T66 modules / tests, T65 canary functions).

It exists for the CPU tests and the dry run ONLY: it is the `SimExecutor` back end that predicts what the sandbox would report for a RENDERED Python file.
It never calls `exec`, `eval`, `compile`, `open` or `__import__`; it walks an `ast` tree and implements the subset itself, with an allow-list of builtins and
string / list / dict methods, a step budget, and sibling-module imports only. Anything outside the subset raises `Unsupported` (a drop reason, never a guess).
The production gold comes from the real sandbox (od-sbx1, 3 identical runs); PyEval agreeing with the generator's host-side reference semantics is the CPU
evidence that the RENDERER is right (a mismatch is a renderer bug), exactly the role `SimExecutor` plays for L-C.

Subset: module-level constants and function / exception-class definitions; if / elif / else, for (list, range, dict, str, enumerate, zip, sorted, reversed),
while (step budget), assignment (names, subscripts, tuple unpacking), augmented assignment, assert, raise, try / except / else / finally, pass / break / continue,
return, global-free closures NOT supported; expressions: arithmetic, comparisons (incl. in / is), boolean ops, ternary, calls (keyword arguments, defaults,
*args / **kwargs), attribute calls on str / list / dict / tuple, subscripts and slices, list / tuple / dict / set literals and comprehensions, f-strings.
"""
import ast

from . import pyshim

MAX_STEPS = 300000


class PyEvalError(Exception):
    pass


class Unsupported(PyEvalError):
    pass


class StepBudget(PyEvalError):
    pass


class _Return(Exception):
    def __init__(self, v):
        self.v = v


class _Break(Exception):
    pass


class _Continue(Exception):
    pass


BUILTIN_EXC = {n: getattr(__builtins__, n) if not isinstance(__builtins__, dict) else __builtins__[n]
               for n in ("Exception", "ValueError", "KeyError", "TypeError", "IndexError", "ZeroDivisionError", "AttributeError", "RuntimeError",
                         "AssertionError", "NameError", "StopIteration", "ArithmeticError", "LookupError", "OverflowError")}
STR_METHODS = {"lower", "upper", "strip", "lstrip", "rstrip", "split", "rsplit", "join", "startswith", "endswith", "replace", "find", "count", "isdigit",
               "isalpha", "zfill", "format", "title", "capitalize", "partition", "rpartition", "index", "isalnum", "splitlines", "rjust", "ljust"}
LIST_METHODS = {"append", "extend", "pop", "sort", "index", "insert", "count", "reverse", "remove", "copy"}
DICT_METHODS = {"get", "items", "keys", "values", "setdefault", "update", "pop", "copy"}
SET_METHODS = {"add", "discard", "union", "intersection", "difference", "remove"}


def _builtins():
    return {"len": len, "range": range, "sorted": sorted, "sum": sum, "min": min, "max": max, "abs": abs, "int": int, "str": str, "bool": bool, "list": list,
            "dict": dict, "tuple": tuple, "set": set, "enumerate": enumerate, "zip": zip, "reversed": reversed, "any": any, "all": all, "round": round,
            "repr": repr, "isinstance": isinstance, "float": float, "divmod": divmod, "pow": pow, "chr": chr, "ord": ord, "map": map, "filter": filter,
            "True": True, "False": False, "None": None}


class Module(object):
    """One interpreted module. `files` maps module stems to source text for sibling imports."""

    def __init__(self, name, files, shared=None):
        self.name = name
        self.files = files
        self.globals = _builtins()
        self.globals.update(BUILTIN_EXC)
        self.globals["open"] = pyshim.vopen
        self.steps = 0
        self.cache = shared if shared is not None else {}
        self.cache[name] = self
        tree = ast.parse(files[name + ".py"] if name + ".py" in files else files[name])
        for st in tree.body:
            self._exec(st, self.globals, top=True)

    # ------------------------------------------------------------------ public
    def call(self, fn, *args, **kw):
        f = self.globals[fn]
        return f(*args, **kw)

    def has(self, name):
        return name in self.globals

    # ------------------------------------------------------------------ steps
    def _tick(self):
        self.steps += 1
        if self.steps > MAX_STEPS:
            raise StepBudget("step budget exhausted")

    # ------------------------------------------------------------------ statements
    def _exec_block(self, body, env):
        for st in body:
            self._exec(st, env)

    def _exec(self, st, env, top=False):
        self._tick()
        t = type(st)
        if t is ast.Expr:
            if isinstance(st.value, ast.Constant):
                return                                            # docstring
            self._eval(st.value, env)
        elif t is ast.Assign:
            v = self._eval(st.value, env)
            for tg in st.targets:
                self._assign(tg, v, env)
        elif t is ast.AugAssign:
            cur = self._eval(ast.Name(id=st.target.id, ctx=ast.Load()) if isinstance(st.target, ast.Name) else st.target, env)
            v = self._binop(st.op, cur, self._eval(st.value, env))
            self._assign(st.target, v, env)
        elif t is ast.Return:
            raise _Return(self._eval(st.value, env) if st.value is not None else None)
        elif t is ast.If:
            self._exec_block(st.body if self._eval(st.test, env) else st.orelse, env)
        elif t is ast.For:
            it = self._eval(st.iter, env)
            broke = False
            for x in it:
                self._tick()
                self._assign(st.target, x, env)
                try:
                    self._exec_block(st.body, env)
                except _Break:
                    broke = True
                    break
                except _Continue:
                    continue
            if not broke:
                self._exec_block(st.orelse, env)
        elif t is ast.While:
            while self._eval(st.test, env):
                self._tick()
                try:
                    self._exec_block(st.body, env)
                except _Break:
                    break
                except _Continue:
                    continue
        elif t is ast.FunctionDef:
            env[st.name] = self._make_fn(st, env)
        elif t is ast.ClassDef:
            bases = tuple(self._eval(b, env) for b in st.bases)
            if not bases or not all(isinstance(b, type) and issubclass(b, BaseException) for b in bases):
                raise Unsupported("class definitions are limited to exception classes")
            if any(not isinstance(s, (ast.Pass, ast.Expr)) for s in st.body):
                raise Unsupported("exception class body must be `pass` or a docstring")
            env[st.name] = type(st.name, bases, {})
        elif t is ast.Assert:
            if not self._eval(st.test, env):
                raise AssertionError(self._eval(st.msg, env) if st.msg else "")
        elif t is ast.Raise:
            if st.exc is None:
                raise Unsupported("bare raise")
            e = self._eval(st.exc, env)
            if isinstance(e, type):
                e = e()
            raise e
        elif t is ast.Try:
            try:
                try:
                    self._exec_block(st.body, env)
                except (_Return, _Break, _Continue):
                    raise
                except (PyEvalError,):
                    raise
                except BaseException as ex:                           # noqa: BLE001 - interpreted exceptions are host exceptions
                    for h in st.handlers:
                        if h.type is None or self._matches(ex, self._eval(h.type, env)):
                            if h.name:
                                env[h.name] = ex
                            self._exec_block(h.body, env)
                            break
                    else:
                        raise
                else:
                    self._exec_block(st.orelse, env)
            finally:
                self._exec_block(st.finalbody, env)
        elif t is ast.Pass:
            return
        elif t is ast.Break:
            raise _Break()
        elif t is ast.Continue:
            raise _Continue()
        elif t is ast.Import:
            for a in st.names:
                env[(a.asname or a.name).split(".")[0] if not a.asname else a.asname] = self._import(a.name)
        elif t is ast.ImportFrom:
            m = self._import(st.module)
            for a in st.names:
                env[a.asname or a.name] = getattr(m, a.name) if isinstance(m, pyshim.ShimObj) else m.globals[a.name]
        else:
            raise Unsupported("statement %s" % t.__name__)

    @staticmethod
    def _matches(ex, typ):
        if isinstance(typ, tuple):
            return any(isinstance(ex, t) for t in typ)
        return isinstance(ex, typ)

    def _import(self, name):
        shims = pyshim.make_modules()
        if name in shims:
            return shims[name]
        if name.split(".")[0] in shims:
            return shims[name.split(".")[0]]
        if name in self.cache:
            return self.cache[name]
        if name + ".py" in self.files:
            return Module(name, self.files, self.cache)
        raise Unsupported("import of %r (only sibling modules)" % name)

    def _assign(self, tg, v, env):
        if isinstance(tg, ast.Name):
            env[tg.id] = v
        elif isinstance(tg, ast.Subscript):
            obj = self._eval(tg.value, env)
            obj[self._index(tg.slice, env)] = v
        elif isinstance(tg, (ast.Tuple, ast.List)):
            vals = list(v)
            if len(vals) != len(tg.elts):
                raise ValueError("unpack mismatch")
            for e, x in zip(tg.elts, vals):
                self._assign(e, x, env)
        else:
            raise Unsupported("assignment target %s" % type(tg).__name__)

    # ------------------------------------------------------------------ functions
    def _make_fn(self, node, defenv):
        args = node.args
        if args.posonlyargs:
            raise Unsupported("positional-only parameters")
        defaults = [self._eval(d, defenv) for d in args.defaults]
        kw_defaults = {a.arg: (self._eval(d, defenv) if d is not None else _NO) for a, d in zip(args.kwonlyargs, args.kw_defaults)}
        pos = [a.arg for a in args.args]
        n_req = len(pos) - len(defaults)
        mod = self

        def fn(*a, **kw):
            mod._tick()
            local = {}
            if len(a) > len(pos) and not args.vararg:
                raise TypeError("%s() takes %d positional arguments but %d were given" % (node.name, len(pos), len(a)))
            for i, name in enumerate(pos):
                if i < len(a):
                    local[name] = a[i]
            extra = a[len(pos):]
            if args.vararg:
                local[args.vararg.arg] = tuple(extra)
            rest = dict(kw)
            for i, name in enumerate(pos):
                if name in local:
                    if name in rest:
                        raise TypeError("%s() got multiple values for argument %r" % (node.name, name))
                    continue
                if name in rest:
                    local[name] = rest.pop(name)
                elif i >= n_req:
                    local[name] = defaults[i - n_req]
                else:
                    raise TypeError("%s() missing required argument %r" % (node.name, name))
            for a_ in args.kwonlyargs:
                if a_.arg in rest:
                    local[a_.arg] = rest.pop(a_.arg)
                elif kw_defaults[a_.arg] is not _NO:
                    local[a_.arg] = kw_defaults[a_.arg]
                else:
                    raise TypeError("%s() missing required keyword argument %r" % (node.name, a_.arg))
            if args.kwarg:
                local[args.kwarg.arg] = rest
            elif rest:
                raise TypeError("%s() got an unexpected keyword argument %r" % (node.name, sorted(rest)[0]))
            env = _Env(local, mod.globals)
            try:
                mod._exec_block(node.body, env)
            except _Return as r:
                return r.v
            return None
        fn.__name__ = node.name
        return fn

    # ------------------------------------------------------------------ expressions
    def _index(self, sl, env):
        if isinstance(sl, ast.Slice):
            return slice(self._eval(sl.lower, env) if sl.lower else None, self._eval(sl.upper, env) if sl.upper else None,
                         self._eval(sl.step, env) if sl.step else None)
        return self._eval(sl, env)

    def _eval(self, n, env):
        self._tick()
        t = type(n)
        if t is ast.Constant:
            return n.value
        if t is ast.Name:
            try:
                return env[n.id]
            except KeyError:
                raise NameError("name %r is not defined" % n.id)
        if t is ast.BinOp:
            return self._binop(n.op, self._eval(n.left, env), self._eval(n.right, env))
        if t is ast.UnaryOp:
            v = self._eval(n.operand, env)
            return {ast.USub: lambda x: -x, ast.UAdd: lambda x: +x, ast.Not: lambda x: not x, ast.Invert: lambda x: ~x}[type(n.op)](v)
        if t is ast.BoolOp:
            if isinstance(n.op, ast.And):
                v = True
                for x in n.values:
                    v = self._eval(x, env)
                    if not v:
                        return v
                return v
            v = False
            for x in n.values:
                v = self._eval(x, env)
                if v:
                    return v
            return v
        if t is ast.Compare:
            left = self._eval(n.left, env)
            for op, c in zip(n.ops, n.comparators):
                right = self._eval(c, env)
                if not self._cmp(op, left, right):
                    return False
                left = right
            return True
        if t is ast.IfExp:
            return self._eval(n.body, env) if self._eval(n.test, env) else self._eval(n.orelse, env)
        if t is ast.Call:
            return self._call(n, env)
        if t is ast.Attribute:
            obj = self._eval(n.value, env)
            if isinstance(obj, pyshim.ShimObj) and n.attr in obj.allowed:
                return getattr(obj, n.attr)
            raise Unsupported("attribute access %s (only on the registered stdlib stand-ins)" % n.attr)
        if t is ast.Subscript:
            return self._eval(n.value, env)[self._index(n.slice, env)]
        if t is ast.List:
            return [self._eval(e, env) for e in n.elts]
        if t is ast.Tuple:
            return tuple(self._eval(e, env) for e in n.elts)
        if t is ast.Set:
            return {self._eval(e, env) for e in n.elts}
        if t is ast.Dict:
            return {self._eval(k, env): self._eval(v, env) for k, v in zip(n.keys, n.values)}
        if t is ast.JoinedStr:
            return "".join(self._eval(v, env) if isinstance(v, ast.FormattedValue) else v.value for v in n.values)
        if t is ast.FormattedValue:
            v = self._eval(n.value, env)
            spec = self._eval(n.format_spec, env) if n.format_spec else ""
            return format(v, spec)
        if t in (ast.ListComp, ast.GeneratorExp, ast.SetComp, ast.DictComp):
            return self._comp(n, env)
        if t is ast.Lambda:
            params = [a.arg for a in n.args.args]
            mod = self

            def lam(*a):
                return mod._eval(n.body, _Env(dict(zip(params, a)), env if isinstance(env, dict) else env))
            return lam
        raise Unsupported("expression %s" % t.__name__)

    def _comp(self, n, env):
        out = []

        def rec(gens, local):
            if not gens:
                if isinstance(n, ast.DictComp):
                    out.append((self._eval(n.key, local), self._eval(n.value, local)))
                else:
                    out.append(self._eval(n.elt, local))
                return
            g = gens[0]
            for x in self._eval(g.iter, local):
                self._tick()
                loc = _Env({}, local)
                self._assign(g.target, x, loc)
                if all(self._eval(c, loc) for c in g.ifs):
                    rec(gens[1:], loc)
        rec(n.generators, _Env({}, env))
        if isinstance(n, ast.DictComp):
            return dict(out)
        if isinstance(n, ast.SetComp):
            return set(out)
        return out

    def _call(self, n, env):
        if isinstance(n.func, ast.Attribute):
            obj = self._eval(n.func.value, env)
            name = n.func.attr
            if isinstance(obj, pyshim.ShimObj):
                if name not in obj.allowed:
                    raise Unsupported("stand-in member %s" % name)
                a, kw = self._args(n, env)
                return getattr(obj, name)(*a, **kw)
            allowed = (STR_METHODS if isinstance(obj, str) else LIST_METHODS if isinstance(obj, list) else DICT_METHODS if isinstance(obj, dict)
                       else SET_METHODS if isinstance(obj, set) else {"index", "count"} if isinstance(obj, tuple) else set())
            if name not in allowed:
                raise Unsupported("method %s.%s" % (type(obj).__name__, name))
            a, kw = self._args(n, env)
            if isinstance(obj, str) and name == "format":
                return obj.format(*a, **kw)
            return getattr(obj, name)(*a, **kw)
        f = self._eval(n.func, env)
        a, kw = self._args(n, env)
        if isinstance(f, type) and issubclass(f, BaseException):
            return f(*a)
        return f(*a, **kw)

    def _args(self, n, env):
        a = []
        for x in n.args:
            if isinstance(x, ast.Starred):
                a.extend(self._eval(x.value, env))
            else:
                a.append(self._eval(x, env))
        kw = {}
        for k in n.keywords:
            if k.arg is None:
                kw.update(self._eval(k.value, env))
            else:
                kw[k.arg] = self._eval(k.value, env)
        return a, kw

    @staticmethod
    def _binop(op, a, b):
        t = type(op)
        if t is ast.Add:
            return a + b
        if t is ast.Sub:
            return a - b
        if t is ast.Mult:
            return a * b
        if t is ast.FloorDiv:
            return a // b
        if t is ast.Mod:
            return a % b
        if t is ast.Pow:
            if isinstance(b, int) and b > 64:
                raise Unsupported("large exponent")
            return a ** b
        if t is ast.Div:
            return a / b
        if t is ast.BitAnd:
            return a & b
        if t is ast.BitOr:
            return a | b
        if t is ast.BitXor:
            return a ^ b
        if t is ast.LShift:
            return a << b
        if t is ast.RShift:
            return a >> b
        raise Unsupported("operator %s" % t.__name__)

    @staticmethod
    def _cmp(op, a, b):
        t = type(op)
        return {ast.Eq: lambda: a == b, ast.NotEq: lambda: a != b, ast.Lt: lambda: a < b, ast.LtE: lambda: a <= b, ast.Gt: lambda: a > b, ast.GtE: lambda: a >= b,
                ast.In: lambda: a in b, ast.NotIn: lambda: a not in b, ast.Is: lambda: a is b, ast.IsNot: lambda: a is not b}[t]()


_NO = object()


class _Env(dict):
    """Function-local scope with a parent chain for reads (globals); writes stay local."""

    def __init__(self, local, parent):
        super().__init__(local)
        self._parent = parent

    def __missing__(self, key):
        return self._parent[key]

    def __contains__(self, key):
        return dict.__contains__(self, key) or key in self._parent


# ---- test runner ---------------------------------------------------------------------------------------------------------------------
def run_tests(files, test_file):
    """Run every `test_*` function of `test_file` (a module of `files`) in definition order. -> {test_name: 'pass' | 'fail:<Class>' | 'error:<Class>'}.
    A module that does not import / define at all gives {'__import__': 'error:<Class>'}."""
    stem = test_file[:-3] if test_file.endswith(".py") else test_file
    try:
        m = Module(stem, files)
    except PyEvalError:
        raise
    except BaseException as e:                                   # noqa: BLE001
        return {"__import__": "error:" + type(e).__name__}
    res = {}
    for name, f in list(m.globals.items()):
        if name.startswith("test_") and callable(f):
            m.steps = 0
            try:
                f()
                res[name] = "pass"
            except AssertionError:
                res[name] = "fail:AssertionError"
            except PyEvalError:
                raise
            except BaseException as e:                           # noqa: BLE001
                res[name] = "error:" + type(e).__name__
    return res


def call_all(files, module, calls):
    """Observables of a list of calls [(fn, args, kwargs)] on one fresh module: [('ok', value) | ('exc', ClassName, message)]. Import failure -> every call
    reports ('exc', <Class>, ...)."""
    try:
        m = Module(module, files)
    except PyEvalError:
        raise
    except BaseException as e:                                   # noqa: BLE001
        return [("exc", type(e).__name__, str(e)) for _ in calls]
    out = []
    for fn, args, kwargs in calls:
        m.steps = 0
        try:
            out.append(("ok", m.call(fn, *args, **kwargs)))
        except PyEvalError:
            raise
        except BaseException as e:                               # noqa: BLE001
            out.append(("exc", type(e).__name__, str(e)))
    return out

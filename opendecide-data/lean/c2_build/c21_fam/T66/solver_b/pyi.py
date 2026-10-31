"""pyi: solver B's own evaluator for a restricted Python subset.

It is a SEMANTIC evaluator written from the language rules, not an executor: the stdlib `ast` module only PARSES text into a tree (no tree is ever turned into
code, nothing is compiled, no row text reaches an interpreter of the host). Values are plain data (ints, strings, lists, ...); functions, classes, instances and
modules are this file's own objects. Anything outside the subset raises `Unsupported` and the caller abstains (it never guesses).

Public surface:
    World(sources)                      {module stem: source text}; modules are evaluated lazily on import
    run_suite(world, source)            -> SuiteResult (pytest-like: import errors / failing tests / passes)
    check_syntax(source)                -> None or a short reason (parse errors plus the checks a byte-compiler adds: return/break outside)
"""
import ast
import builtins as _builtins_mod
import operator
import sys

MAX_STEPS = 400000
MAX_DEPTH = 120
MAX_SEQ = 20000


class Unsupported(Exception):
    """A construct outside the supported subset (or a resource limit)."""


class Throw(Exception):
    """A Python-level exception in flight; `.inst` is an Inst of an exception class."""

    def __init__(self, inst):
        Exception.__init__(self, "throw")
        self.inst = inst


class _Brk(Exception):
    pass


class _Cnt(Exception):
    pass


class _Ret(Exception):
    def __init__(self, value):
        Exception.__init__(self, "ret")
        self.value = value


# ---- object model ------------------------------------------------------------------------------------------------------------------
class Cls(object):
    def __init__(self, name, bases, ns, builtin=False):
        self.name, self.bases, self.ns, self.builtin = name, list(bases), ns, builtin

    def mro(self):
        out, todo = [], [self]
        while todo:
            c = todo.pop(0)
            if c not in out:
                out.append(c)
            todo = list(c.bases) + todo
        return out

    def is_sub(self, other):
        return other in self.mro()

    def find(self, attr):
        for c in self.mro():
            if attr in c.ns:
                return c.ns[attr]
        return None

    def has(self, attr):
        return any(attr in c.ns for c in self.mro())


class Inst(object):
    def __init__(self, cls):
        self.cls, self.attrs = cls, {}


class Func(object):
    def __init__(self, name, args, body, closure, defaults, kwdefaults, is_lambda=False):
        self.name, self.args, self.body, self.closure = name, args, body, closure
        self.defaults, self.kwdefaults, self.is_lambda = defaults, kwdefaults, is_lambda
        self.local_names = None


class Bound(object):
    def __init__(self, self_obj, func):
        self.self_obj, self.func = self_obj, func


class Builtin(object):
    def __init__(self, name, fn, pytype=None):
        self.name, self.fn, self.pytype = name, fn, pytype


class NatMethod(object):
    def __init__(self, obj, name):
        self.obj, self.name = obj, name


class Mod(object):
    def __init__(self, name):
        self.name, self.ns = name, {}


class Frame(object):
    def __init__(self, parent, glob, kind, local_names=()):
        self.vars, self.parent, self.glob, self.kind = {}, parent, glob, kind      # kind: module | func | class | comp
        self.local_names = set(local_names)
        self.global_names = set()


_EXC_TREE = [("BaseException", None), ("Exception", "BaseException"), ("ArithmeticError", "Exception"), ("ZeroDivisionError", "ArithmeticError"),
             ("OverflowError", "ArithmeticError"), ("LookupError", "Exception"), ("KeyError", "LookupError"), ("IndexError", "LookupError"),
             ("ValueError", "Exception"), ("UnicodeError", "ValueError"), ("TypeError", "Exception"), ("AttributeError", "Exception"),
             ("NameError", "Exception"), ("UnboundLocalError", "NameError"), ("AssertionError", "Exception"), ("RuntimeError", "Exception"),
             ("NotImplementedError", "RuntimeError"), ("RecursionError", "RuntimeError"), ("ImportError", "Exception"), ("ModuleNotFoundError", "ImportError"),
             ("StopIteration", "Exception"), ("OSError", "Exception"), ("EOFError", "Exception"), ("SyntaxError", "Exception"),
             ("KeyboardInterrupt", "BaseException"), ("SystemExit", "BaseException")]
EXC = {}
for _n, _b in _EXC_TREE:
    EXC[_n] = Cls(_n, [EXC[_b]] if _b else [], {}, builtin=True)

_BINOPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv, ast.FloorDiv: operator.floordiv,
           ast.Mod: operator.mod, ast.Pow: operator.pow, ast.LShift: operator.lshift, ast.RShift: operator.rshift, ast.BitOr: operator.or_,
           ast.BitAnd: operator.and_, ast.BitXor: operator.xor}
_CMPOPS = {ast.Eq: operator.eq, ast.NotEq: operator.ne, ast.Lt: operator.lt, ast.LtE: operator.le, ast.Gt: operator.gt, ast.GtE: operator.ge}
_UNOPS = {ast.USub: operator.neg, ast.UAdd: operator.pos, ast.Invert: operator.invert}
_NATIVE_TYPES = (int, float, str, bool, list, dict, tuple, set, type(None), range)
_ALL_BUILTIN_NAMES = set(dir(_builtins_mod))
_METHODS = {
    str: {"join", "upper", "lower", "strip", "lstrip", "rstrip", "split", "rsplit", "startswith", "endswith", "replace", "find", "rfind", "count", "title",
          "capitalize", "isdigit", "isalpha", "isupper", "islower", "zfill", "ljust", "rjust", "center", "index", "swapcase", "format", "partition"},
    list: {"append", "extend", "insert", "pop", "remove", "index", "count", "reverse", "copy", "clear", "sort"},
    dict: {"get", "items", "keys", "values", "update", "setdefault", "pop", "copy", "clear"},
    set: {"add", "discard", "remove", "update", "union", "intersection", "difference", "copy", "clear", "pop", "issubset", "issuperset"},
    tuple: {"index", "count"},
}


class SuiteResult(object):
    def __init__(self, status, passed=0, failed=0, detail=""):
        self.status, self.passed, self.failed, self.detail = status, passed, failed, detail     # status: pass | fail | unsupported

    @property
    def ok(self):
        return self.status == "pass"


# ---- static helpers -----------------------------------------------------------------------------------------------------------------
def check_syntax(source):
    """None when the text is a valid module, else a short reason. Besides parse errors this repeats the few checks a byte compiler adds."""
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError, RecursionError, MemoryError) as e:
        return "parse:" + type(e).__name__
    return _scope_check(tree.body, in_func=False, in_loop=False)


def _scope_check(stmts, in_func, in_loop):
    for s in stmts:
        if isinstance(s, ast.Return) and not in_func:
            return "return outside function"
        if isinstance(s, (ast.Break, ast.Continue)) and not in_loop:
            return "break outside loop"
        if isinstance(s, (ast.FunctionDef, ast.AsyncFunctionDef)):
            names = [a.arg for a in s.args.posonlyargs + s.args.args + s.args.kwonlyargs]
            names += [x.arg for x in (s.args.vararg, s.args.kwarg) if x]
            if len(set(names)) != len(names):
                return "duplicate argument"
            r = _scope_check(s.body, True, False)
            if r:
                return r
        elif isinstance(s, ast.ClassDef):
            r = _scope_check(s.body, False, False)
            if r:
                return r
        elif isinstance(s, (ast.For, ast.While, ast.AsyncFor)):
            r = _scope_check(s.body, in_func, True) or _scope_check(s.orelse, in_func, in_loop)
            if r:
                return r
        else:
            for fld in ("body", "orelse", "finalbody"):
                sub = getattr(s, fld, None) if isinstance(s, (ast.If, ast.Try, ast.With)) else None
                if sub:
                    r = _scope_check(sub, in_func, in_loop)
                    if r:
                        return r
            if isinstance(s, ast.Try):
                for h in s.handlers:
                    r = _scope_check(h.body, in_func, in_loop)
                    if r:
                        return r
    return None


def _targets(node, out):
    if isinstance(node, ast.Name):
        out.add(node.id)
    elif isinstance(node, (ast.Tuple, ast.List)):
        for e in node.elts:
            _targets(e, out)
    elif isinstance(node, ast.Starred):
        _targets(node.value, out)


def _collect_locals(stmts, out, glob):
    for s in stmts:
        if isinstance(s, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            out.add(s.name)
        elif isinstance(s, ast.Assign):
            for t in s.targets:
                _targets(t, out)
        elif isinstance(s, (ast.AugAssign, ast.AnnAssign)):
            _targets(s.target, out)
        elif isinstance(s, (ast.For, ast.AsyncFor)):
            _targets(s.target, out)
        elif isinstance(s, (ast.Import, ast.ImportFrom)):
            for a in s.names:
                out.add((a.asname or a.name).split(".")[0])
        elif isinstance(s, ast.Global):
            glob.update(s.names)
        elif isinstance(s, ast.Nonlocal):
            raise Unsupported("nonlocal")
        elif isinstance(s, ast.With):
            for it in s.items:
                if it.optional_vars is not None:
                    _targets(it.optional_vars, out)
        elif isinstance(s, ast.Delete):
            for t in s.targets:
                _targets(t, out)
        if isinstance(s, ast.Try):
            for h in s.handlers:
                if h.name:
                    out.add(h.name)
        for fld in ("body", "orelse", "finalbody"):
            sub = getattr(s, fld, None)
            if isinstance(sub, list) and not isinstance(s, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                _collect_locals(sub, out, glob)
        if isinstance(s, ast.Try):
            for h in s.handlers:
                _collect_locals(h.body, out, glob)


def _is_const_true(node):
    return isinstance(node, ast.Constant) and bool(node.value)


class Interp(object):
    def __init__(self):
        self.steps = 0
        self.depth = 0
        self.handling = []
        self.builtins = self._make_builtins()
        self.dispatch = {
            ast.Constant: self.e_const, ast.Name: self.e_name, ast.BinOp: self.e_binop, ast.UnaryOp: self.e_unary, ast.BoolOp: self.e_boolop,
            ast.Compare: self.e_compare, ast.Call: self.e_call, ast.Attribute: self.e_attr, ast.Subscript: self.e_sub, ast.IfExp: self.e_ifexp,
            ast.Tuple: self.e_tuple, ast.List: self.e_list, ast.Set: self.e_set, ast.Dict: self.e_dict, ast.Lambda: self.e_lambda,
            ast.JoinedStr: self.e_joined, ast.FormattedValue: self.e_fmtvalue, ast.ListComp: self.e_comp, ast.SetComp: self.e_comp,
            ast.GeneratorExp: self.e_comp, ast.DictComp: self.e_comp, ast.Slice: self.e_slice}
        self.stmts = {
            ast.Expr: self.s_expr, ast.Assign: self.s_assign, ast.AugAssign: self.s_aug, ast.AnnAssign: self.s_ann, ast.Return: self.s_return,
            ast.If: self.s_if, ast.For: self.s_for, ast.While: self.s_while, ast.Break: self.s_break, ast.Continue: self.s_continue, ast.Pass: self.s_pass,
            ast.Raise: self.s_raise, ast.Try: self.s_try, ast.Assert: self.s_assert, ast.FunctionDef: self.s_funcdef, ast.ClassDef: self.s_classdef,
            ast.ImportFrom: self.s_importfrom, ast.Import: self.s_import, ast.Global: self.s_global, ast.Delete: self.s_delete}
        self.world = None

    # ---- plumbing --------------------------------------------------------------------------------------------------------------------
    def tick(self):
        self.steps += 1
        if self.steps > MAX_STEPS:
            raise Unsupported("step limit")

    def exc(self, name, msg=None):
        i = Inst(EXC[name])
        i.attrs["args"] = () if msg is None else (msg,)
        return i

    def throw(self, name, msg=None):
        raise Throw(self.exc(name, msg))

    def nat(self, fn, *a, **k):
        """Call a native operation on plain data; native errors become interpreter exceptions."""
        try:
            return fn(*a, **k)
        except (Throw, Unsupported, _Ret, _Brk, _Cnt):
            raise
        except RecursionError:
            raise Unsupported("native recursion")
        except MemoryError:
            raise Unsupported("memory")
        except Exception as e:                                              # noqa: BLE001
            name = type(e).__name__
            if name in EXC:
                self.throw(name, str(e.args[0]) if e.args else "")
            raise Unsupported("native " + name)

    def truthy(self, v):
        if isinstance(v, Inst):
            if v.cls.has("__bool__") or v.cls.has("__len__"):
                raise Unsupported("dunder truth")
            return True
        if isinstance(v, (Func, Cls, Bound, Builtin, NatMethod, Mod)):
            return True
        return bool(v)

    # ---- running ----------------------------------------------------------------------------------------------------------------------
    def run_module(self, tree, mod):
        fr = Frame(None, None, "module")
        fr.glob = fr
        fr.vars = mod.ns
        self.run_body(tree.body, fr)
        return fr

    def run_body(self, stmts, fr):
        for s in stmts:
            self.tick()
            h = self.stmts.get(type(s))
            if h is None:
                raise Unsupported("stmt " + type(s).__name__)
            h(s, fr)

    def call(self, f, args, kwargs):
        self.tick()
        if isinstance(f, Func):
            return self.call_func(f, args, kwargs)
        if isinstance(f, Bound):
            return self.call_func(f.func, [f.self_obj] + list(args), kwargs)
        if isinstance(f, Builtin):
            return f.fn(args, kwargs)
        if isinstance(f, NatMethod):
            return self.call_native_method(f, args, kwargs)
        if isinstance(f, Cls):
            return self.instantiate(f, args, kwargs)
        self.throw("TypeError", "object is not callable")

    def instantiate(self, cls, args, kwargs):
        inst = Inst(cls)
        if cls.is_sub(EXC["BaseException"]):
            init = cls.find("__init__")
            if init is None:
                if kwargs:
                    self.throw("TypeError", "exception takes no keyword arguments")
                inst.attrs["args"] = tuple(args)
            else:
                inst.attrs["args"] = tuple(args)
                self.call(init, [inst] + list(args), kwargs)
            return inst
        init = cls.find("__init__")
        if init is None:
            if args or kwargs:
                self.throw("TypeError", "takes no arguments")
        else:
            self.call(init, [inst] + list(args), kwargs)
        return inst

    def local_names_of(self, fn):
        if fn.local_names is None:
            names, glob = set(), set()
            a = fn.args
            for x in a.posonlyargs + a.args + a.kwonlyargs:
                names.add(x.arg)
            for x in (a.vararg, a.kwarg):
                if x:
                    names.add(x.arg)
            if not fn.is_lambda:
                _collect_locals(fn.body, names, glob)
            fn.local_names = (names - glob, glob)
        return fn.local_names

    def call_func(self, fn, args, kwargs):
        if self.depth >= MAX_DEPTH:
            raise Unsupported("depth")
        names, glob = self.local_names_of(fn)
        fr = Frame(fn.closure, fn.closure.glob, "func", names)
        fr.global_names = glob
        self.bind(fn, fr, list(args), dict(kwargs))
        self.depth += 1
        try:
            if fn.is_lambda:
                return self.ev(fn.body, fr)
            try:
                self.run_body(fn.body, fr)
            except _Ret as r:
                return r.value
            return None
        finally:
            self.depth -= 1

    def bind(self, fn, fr, args, kwargs):
        a = fn.args
        pos = [x.arg for x in a.posonlyargs + a.args]
        npos = len(pos)
        nodef = npos - len(fn.defaults)
        if len(args) > npos and not a.vararg:
            self.throw("TypeError", "%s() takes %d positional arguments but %d were given" % (fn.name, npos, len(args)))
        for i, v in enumerate(args[:npos]):
            fr.vars[pos[i]] = v
        if a.vararg:
            fr.vars[a.vararg.arg] = tuple(args[npos:])
        posonly = {x.arg for x in a.posonlyargs}
        extra = {}
        for k, v in kwargs.items():
            if (k in pos and k not in posonly) or k in [x.arg for x in a.kwonlyargs]:
                if k in fr.vars:
                    self.throw("TypeError", "%s() got multiple values for argument '%s'" % (fn.name, k))
                fr.vars[k] = v
            elif a.kwarg:
                extra[k] = v
            else:
                self.throw("TypeError", "%s() got an unexpected keyword argument '%s'" % (fn.name, k))
        if a.kwarg:
            fr.vars[a.kwarg.arg] = extra
        for i, p in enumerate(pos):
            if p not in fr.vars:
                if i >= nodef:
                    fr.vars[p] = fn.defaults[i - nodef]
                else:
                    self.throw("TypeError", "%s() missing required positional argument: '%s'" % (fn.name, p))
        for x, d in zip(a.kwonlyargs, fn.kwdefaults):
            if x.arg not in fr.vars:
                if d is _MISSING:
                    self.throw("TypeError", "%s() missing required keyword-only argument: '%s'" % (fn.name, x.arg))
                fr.vars[x.arg] = d

    # ---- names ------------------------------------------------------------------------------------------------------------------------
    def lookup(self, fr, name):
        f = fr
        while f is not None and f.kind != "module":
            if name in f.global_names:
                break
            if name in f.vars:
                return f.vars[name]
            if f.kind == "func" and f is fr and name in f.local_names:
                self.throw("UnboundLocalError", "local variable '%s' referenced before assignment" % name)
            f = f.parent
        g = fr.glob.vars
        if name in g:
            return g[name]
        if name in self.builtins:
            return self.builtins[name]
        if name in _ALL_BUILTIN_NAMES:
            raise Unsupported("builtin " + name)
        self.throw("NameError", "name '%s' is not defined" % name)

    def store(self, fr, name, value):
        if fr.kind == "module" or name in fr.global_names:
            fr.glob.vars[name] = value
        else:
            fr.vars[name] = value

    # ---- expressions -----------------------------------------------------------------------------------------------------------------
    def ev(self, n, fr):
        self.tick()
        h = self.dispatch.get(type(n))
        if h is None:
            raise Unsupported("expr " + type(n).__name__)
        return h(n, fr)

    def e_const(self, n, fr):
        if isinstance(n.value, (bytes, complex)) or n.value is Ellipsis:
            raise Unsupported("const kind")
        return n.value

    def e_name(self, n, fr):
        return self.lookup(fr, n.id)

    def e_binop(self, n, fr):
        a, b = self.ev(n.left, fr), self.ev(n.right, fr)
        return self.binop(n.op, a, b)

    def binop(self, opnode, a, b):
        op = _BINOPS.get(type(opnode))
        if op is None:
            raise Unsupported("binop")
        if isinstance(opnode, ast.Pow) and isinstance(b, int) and (b > 256 or (isinstance(a, int) and abs(a) > 1 and b * max(1, abs(a).bit_length()) > 4096)):
            raise Unsupported("pow size")
        if isinstance(opnode, (ast.Mult, ast.LShift)):
            for x, y in ((a, b), (b, a)):
                if isinstance(x, (str, list, tuple, int)) and isinstance(y, int) and not isinstance(y, bool) and (y > MAX_SEQ or (isinstance(opnode, ast.LShift) and y > 64)):
                    raise Unsupported("size")
        return self.nat(op, a, b)

    def e_unary(self, n, fr):
        v = self.ev(n.operand, fr)
        if isinstance(n.op, ast.Not):
            return not self.truthy(v)
        return self.nat(_UNOPS[type(n.op)], v)

    def e_boolop(self, n, fr):
        is_and = isinstance(n.op, ast.And)
        v = None
        for x in n.values:
            v = self.ev(x, fr)
            t = self.truthy(v)
            if is_and and not t:
                return v
            if not is_and and t:
                return v
        return v

    def e_compare(self, n, fr):
        left = self.ev(n.left, fr)
        r = True
        for op, rn in zip(n.ops, n.comparators):
            right = self.ev(rn, fr)
            t = type(op)
            if t in _CMPOPS:
                r = self.nat(_CMPOPS[t], left, right)
            elif t is ast.Is:
                r = left is right
            elif t is ast.IsNot:
                r = left is not right
            elif t is ast.In:
                r = self.nat(operator.contains, right, left)
            elif t is ast.NotIn:
                r = not self.nat(operator.contains, right, left)
            else:
                raise Unsupported("cmp")
            if not r:
                return r
            left = right
        return r

    def e_ifexp(self, n, fr):
        return self.ev(n.body if self.truthy(self.ev(n.test, fr)) else n.orelse, fr)

    def e_tuple(self, n, fr):
        return tuple(self.elts(n.elts, fr))

    def e_list(self, n, fr):
        return list(self.elts(n.elts, fr))

    def e_set(self, n, fr):
        return self.nat(set, self.elts(n.elts, fr))

    def elts(self, nodes, fr):
        out = []
        for x in nodes:
            if isinstance(x, ast.Starred):
                out.extend(self.nat(list, self.ev(x.value, fr)))
            else:
                out.append(self.ev(x, fr))
        return out

    def e_dict(self, n, fr):
        d = {}
        for k, v in zip(n.keys, n.values):
            if k is None:
                d.update(self.nat(dict, self.ev(v, fr)))
            else:
                key = self.ev(k, fr)
                self.nat(hash, key)
                d[key] = self.ev(v, fr)
        return d

    def e_slice(self, n, fr):
        f = lambda x: None if x is None else self.ev(x, fr)       # noqa: E731
        return slice(f(n.lower), f(n.upper), f(n.step))

    def e_sub(self, n, fr):
        obj = self.ev(n.value, fr)
        idx = self.ev(n.slice, fr)
        if isinstance(obj, (Inst, Cls, Func, Mod)):
            raise Unsupported("getitem on object")
        return self.nat(operator.getitem, obj, idx)

    def e_attr(self, n, fr):
        return self.getattr_(self.ev(n.value, fr), n.attr)

    def getattr_(self, obj, name):
        if isinstance(obj, Inst):
            if name in obj.attrs:
                return obj.attrs[name]
            v = obj.cls.find(name)
            if v is None:
                if name == "args" and obj.cls.is_sub(EXC["BaseException"]):
                    return obj.attrs.get("args", ())
                self.throw("AttributeError", "object has no attribute '%s'" % name)
            if isinstance(v, Func):
                return Bound(obj, v)
            return v
        if isinstance(obj, Cls):
            v = obj.find(name)
            if v is None:
                if name == "__name__":
                    return obj.name
                self.throw("AttributeError", "type object has no attribute '%s'" % name)
            return v
        if isinstance(obj, Mod):
            if name in obj.ns:
                return obj.ns[name]
            self.throw("AttributeError", "module has no attribute '%s'" % name)
        if isinstance(obj, Func) and name == "__name__":
            return obj.name
        for t, names in _METHODS.items():
            if isinstance(obj, t) and not isinstance(obj, bool):
                if name in names:
                    return NatMethod(obj, name)
                self.throw("AttributeError", "object has no attribute '%s'" % name)
        self.throw("AttributeError", "object has no attribute '%s'" % name)

    def call_native_method(self, m, args, kwargs):
        kwargs = dict(kwargs)
        if m.name == "sort" and "key" in kwargs:
            kf = kwargs.pop("key")
            kwargs["key"] = lambda v: self.call(kf, [v], {})
        for v in list(args) + [x for kk, x in kwargs.items() if kk != "key"]:
            if not self.is_plain(v):
                raise Unsupported("method argument")
        return self.nat(getattr(m.obj, m.name), *args, **kwargs)

    def is_plain(self, v, depth=0):
        if depth > 6:
            return False
        if isinstance(v, (int, float, str, bool, type(None), range)):
            return True
        if isinstance(v, (list, tuple, set, frozenset)):
            return all(self.is_plain(x, depth + 1) for x in v)
        if isinstance(v, dict):
            return all(self.is_plain(k, depth + 1) and self.is_plain(x, depth + 1) for k, x in v.items())
        return False

    def e_call(self, n, fr):
        f = self.ev(n.func, fr)
        args = self.elts(n.args, fr)
        kwargs = {}
        for k in n.keywords:
            if k.arg is None:
                kwargs.update(self.nat(dict, self.ev(k.value, fr)))
            else:
                if k.arg in kwargs:
                    raise Unsupported("dup kw")
                kwargs[k.arg] = self.ev(k.value, fr)
        return self.call(f, args, kwargs)

    def e_lambda(self, n, fr):
        defaults = [self.ev(d, fr) for d in n.args.defaults]
        kwd = [(_MISSING if d is None else self.ev(d, fr)) for d in n.args.kw_defaults]
        return Func("<lambda>", n.args, n.body, fr, defaults, kwd, is_lambda=True)

    def e_joined(self, n, fr):
        return "".join(self.fmt_piece(v, fr) for v in n.values)

    def fmt_piece(self, v, fr):
        if isinstance(v, ast.Constant):
            return v.value
        return self.e_fmtvalue(v, fr)

    def e_fmtvalue(self, n, fr):
        v = self.ev(n.value, fr)
        if n.conversion == 114:
            v = self.nat(repr, v)
        elif n.conversion == 115:
            v = self.to_str(v)
        spec = ""
        if n.format_spec is not None:
            spec = self.e_joined(n.format_spec, fr)
        if not self.is_plain(v):
            v = self.to_str(v)
        return self.nat(format, v, spec)

    def to_str(self, v):
        if isinstance(v, Inst):
            a = v.attrs.get("args", ())
            return str(a[0]) if len(a) == 1 else ("" if not a else str(tuple(a)))
        if self.is_plain(v):
            return self.nat(str, v)
        raise Unsupported("str of object")

    def e_comp(self, n, fr):
        sub = Frame(fr, fr.glob, "comp")
        out = []

        def walk(i):
            if i == len(n.generators):
                if isinstance(n, ast.DictComp):
                    out.append((self.ev(n.key, sub), self.ev(n.value, sub)))
                else:
                    out.append(self.ev(n.elt, sub))
                return
            g = n.generators[i]
            for item in self.iterate(self.ev(g.iter, sub if i else fr)):
                self.assign(g.target, item, sub)
                if all(self.truthy(self.ev(c, sub)) for c in g.ifs):
                    walk(i + 1)
        walk(0)
        if isinstance(n, ast.ListComp) or isinstance(n, ast.GeneratorExp):
            return out
        if isinstance(n, ast.SetComp):
            return self.nat(set, out)
        return self.nat(dict, out)

    def iterate(self, v):
        if isinstance(v, Inst):
            raise Unsupported("iter object")
        it = self.nat(iter, v)
        n = 0
        while True:
            self.tick()
            try:
                x = next(it)
            except StopIteration:
                return
            except Exception as e:                                          # noqa: BLE001
                self.nat(_raise_it, e)
            n += 1
            yield x

    # ---- statements ------------------------------------------------------------------------------------------------------------------
    def s_expr(self, s, fr):
        self.ev(s.value, fr)

    def s_pass(self, s, fr):
        return None

    def s_assign(self, s, fr):
        v = self.ev(s.value, fr)
        for t in s.targets:
            self.assign(t, v, fr)

    def s_ann(self, s, fr):
        if s.value is not None:
            self.assign(s.target, self.ev(s.value, fr), fr)

    def s_aug(self, s, fr):
        t = s.target
        cur = self.ev(t, fr)
        rhs = self.ev(s.value, fr)
        if isinstance(cur, list) and isinstance(s.op, ast.Add):
            self.nat(cur.extend, rhs)
            new = cur
        else:
            new = self.binop(s.op, cur, rhs)
        self.assign(t, new, fr)

    def assign(self, t, v, fr):
        if isinstance(t, ast.Name):
            self.store(fr, t.id, v)
        elif isinstance(t, (ast.Tuple, ast.List)):
            if any(isinstance(e, ast.Starred) for e in t.elts):
                raise Unsupported("starred target")
            items = list(self.iterate(v))
            if len(items) < len(t.elts):
                self.throw("ValueError", "not enough values to unpack")
            if len(items) > len(t.elts):
                self.throw("ValueError", "too many values to unpack")
            for e, x in zip(t.elts, items):
                self.assign(e, x, fr)
        elif isinstance(t, ast.Subscript):
            obj, idx = self.ev(t.value, fr), self.ev(t.slice, fr)
            if isinstance(obj, (Inst, Cls, Mod, Func)):
                raise Unsupported("setitem on object")
            self.nat(operator.setitem, obj, idx, v)
        elif isinstance(t, ast.Attribute):
            obj = self.ev(t.value, fr)
            if isinstance(obj, Inst):
                obj.attrs[t.attr] = v
            elif isinstance(obj, Cls):
                obj.ns[t.attr] = v
            elif isinstance(obj, Mod):
                obj.ns[t.attr] = v
            else:
                self.throw("AttributeError", "cannot set attribute")
        else:
            raise Unsupported("target " + type(t).__name__)

    def s_delete(self, s, fr):
        for t in s.targets:
            if isinstance(t, ast.Name):
                scope = fr.glob.vars if (fr.kind == "module" or t.id in fr.global_names) else fr.vars
                if t.id not in scope:
                    self.throw("NameError", "name '%s' is not defined" % t.id)
                del scope[t.id]
            elif isinstance(t, ast.Subscript):
                obj = self.ev(t.value, fr)
                if isinstance(obj, (Inst, Cls, Mod, Func)):
                    raise Unsupported("delitem on object")
                self.nat(operator.delitem, obj, self.ev(t.slice, fr))
            else:
                raise Unsupported("del target")

    def s_return(self, s, fr):
        raise _Ret(None if s.value is None else self.ev(s.value, fr))

    def s_if(self, s, fr):
        self.run_body(s.body if self.truthy(self.ev(s.test, fr)) else s.orelse, fr)

    def s_for(self, s, fr):
        broke = False
        for item in self.iterate(self.ev(s.iter, fr)):
            self.assign(s.target, item, fr)
            try:
                self.run_body(s.body, fr)
            except _Cnt:
                continue
            except _Brk:
                broke = True
                break
        if not broke:
            self.run_body(s.orelse, fr)

    def s_while(self, s, fr):
        broke = False
        while self.truthy(self.ev(s.test, fr)):
            self.tick()
            try:
                self.run_body(s.body, fr)
            except _Cnt:
                continue
            except _Brk:
                broke = True
                break
        if not broke:
            self.run_body(s.orelse, fr)

    def s_break(self, s, fr):
        raise _Brk()

    def s_continue(self, s, fr):
        raise _Cnt()

    def s_global(self, s, fr):
        return None

    def s_assert(self, s, fr):
        if not self.truthy(self.ev(s.test, fr)):
            msg = None if s.msg is None else self.to_str(self.ev(s.msg, fr))
            self.throw("AssertionError", msg)

    def s_raise(self, s, fr):
        if s.exc is None:
            if self.handling:
                raise Throw(self.handling[-1])
            self.throw("RuntimeError", "No active exception to reraise")
        e = self.ev(s.exc, fr)
        if isinstance(e, Cls):
            if not e.is_sub(EXC["BaseException"]):
                self.throw("TypeError", "exceptions must derive from BaseException")
            e = self.instantiate(e, [], {})
        if not (isinstance(e, Inst) and e.cls.is_sub(EXC["BaseException"])):
            self.throw("TypeError", "exceptions must derive from BaseException")
        if s.cause is not None:
            self.ev(s.cause, fr)
        raise Throw(e)

    def s_try(self, s, fr):
        try:
            try:
                self.run_body(s.body, fr)
            except Throw as t:
                handled = False
                for h in s.handlers:
                    if self.handler_matches(h, t.inst, fr):
                        handled = True
                        self.handling.append(t.inst)
                        try:
                            if h.name:
                                self.store(fr, h.name, t.inst)
                            self.run_body(h.body, fr)
                        finally:
                            self.handling.pop()
                            if h.name:
                                (fr.glob.vars if (fr.kind == "module" or h.name in fr.global_names) else fr.vars).pop(h.name, None)
                        break
                if not handled:
                    raise
            else:
                self.run_body(s.orelse, fr)
        finally:
            if s.finalbody:
                self.run_body(s.finalbody, fr)

    def handler_matches(self, h, inst, fr):
        if h.type is None:
            return True
        ty = self.ev(h.type, fr)
        types = list(ty) if isinstance(ty, tuple) else [ty]
        for t in types:
            if not isinstance(t, Cls):
                self.throw("TypeError", "catching classes that do not inherit from BaseException is not allowed")
            if inst.cls.is_sub(t):
                return True
        return False

    def s_funcdef(self, s, fr):
        if s.decorator_list:
            raise Unsupported("decorator")
        defaults = [self.ev(d, fr) for d in s.args.defaults]
        kwd = [(_MISSING if d is None else self.ev(d, fr)) for d in s.args.kw_defaults]
        base = fr
        while base.kind == "class":
            base = base.parent
        f = Func(s.name, s.args, s.body, base, defaults, kwd)
        self.store(fr, s.name, f)

    def s_classdef(self, s, fr):
        if s.decorator_list or s.keywords:
            raise Unsupported("class decorator/keywords")
        bases = []
        for b in s.bases:
            v = self.ev(b, fr)
            if not isinstance(v, Cls):
                raise Unsupported("non-class base")
            bases.append(v)
        names, glob = set(), set()
        _collect_locals(s.body, names, glob)
        cf = Frame(fr, fr.glob, "class", names)
        self.run_body(s.body, cf)
        for k in cf.vars:
            if k.startswith("__") and k.endswith("__") and k != "__init__" and k not in ("__doc__", "__module__", "__qualname__"):
                raise Unsupported("dunder " + k)
        self.store(fr, s.name, Cls(s.name, bases or [], dict(cf.vars)))

    def s_import(self, s, fr):
        for a in s.names:
            mod = self.world.import_module(self, a.name)
            self.store(fr, (a.asname or a.name).split(".")[0], mod)

    def s_importfrom(self, s, fr):
        if s.level or s.module is None:
            raise Unsupported("relative import")
        mod = self.world.import_module(self, s.module)
        for a in s.names:
            if a.name == "*":
                raise Unsupported("star import")
            if a.name not in mod.ns:
                self.throw("ImportError", "cannot import name '%s' from '%s'" % (a.name, s.module))
            self.store(fr, a.asname or a.name, mod.ns[a.name])

    # ---- builtins ---------------------------------------------------------------------------------------------------------------------
    def _make_builtins(self):
        B = {}

        def reg(name, pytype=None):
            def deco(fn):
                B[name] = Builtin(name, fn, pytype)
                return fn
            return deco

        def plain(vs):
            for v in vs:
                if not self.is_plain(v):
                    raise Unsupported("builtin on object")

        @reg("len")
        def _len(a, k):
            if len(a) != 1 or k:
                self.throw("TypeError", "len() takes exactly one argument")
            if isinstance(a[0], Inst):
                raise Unsupported("len object")
            return self.nat(len, a[0])

        @reg("range")
        def _range(a, k):
            plain(a)
            if any(isinstance(x, (int,)) and abs(x) > 10 ** 6 for x in a):
                raise Unsupported("range size")
            return self.nat(range, *a)

        def conv(name, t):
            def f(a, k):
                plain(list(a) + list(k.values()))
                return self.nat(t, *a, **k)
            B[name] = Builtin(name, f, t)
        for nm, t in (("int", int), ("str", str), ("float", float), ("bool", bool), ("list", list), ("tuple", tuple), ("set", set), ("dict", dict)):
            conv(nm, t)

        def _str(a, k):
            if len(a) == 1 and not k and isinstance(a[0], Inst):
                return self.to_str(a[0])
            plain(a)
            return self.nat(str, *a, **k)
        B["str"] = Builtin("str", _str, str)

        @reg("abs")
        def _abs(a, k):
            plain(a)
            return self.nat(abs, *a)

        @reg("sum")
        def _sum(a, k):
            plain(a)
            return self.nat(sum, *a, **k)

        def keyed(name, fn):
            def f(a, k):
                k = dict(k)
                key = k.pop("key", None)
                plain(a)
                if key is not None:
                    k["key"] = lambda v: self.call(key, [v], {})
                return self.nat(fn, *a, **k)
            B[name] = Builtin(name, f)
        keyed("min", min)
        keyed("max", max)

        def _sorted(a, k):
            k = dict(k)
            key = k.pop("key", None)
            plain(a)
            if key is not None:
                k["key"] = lambda v: self.call(key, [v], {})
            return self.nat(sorted, *a, **k)
        B["sorted"] = Builtin("sorted", _sorted)

        @reg("reversed")
        def _reversed(a, k):
            plain(a)
            return self.nat(lambda x: list(reversed(x)), *a)

        @reg("enumerate")
        def _enumerate(a, k):
            plain(a)
            return self.nat(lambda *x, **y: list(enumerate(*x, **y)), *a, **k)

        @reg("zip")
        def _zip(a, k):
            plain(a)
            return self.nat(lambda *x: list(zip(*x)), *a)

        @reg("any")
        def _any(a, k):
            plain(a)
            return self.nat(any, *a)

        @reg("all")
        def _all(a, k):
            plain(a)
            return self.nat(all, *a)

        @reg("round")
        def _round(a, k):
            plain(a)
            return self.nat(round, *a)

        @reg("print")
        def _print(a, k):
            return None

        @reg("repr")
        def _repr(a, k):
            plain(a)
            return self.nat(repr, *a)

        @reg("isinstance")
        def _isinstance(a, k):
            if len(a) != 2:
                self.throw("TypeError", "isinstance expected 2 arguments")
            obj, ty = a
            types = list(ty) if isinstance(ty, tuple) else [ty]
            for t in types:
                if isinstance(t, Builtin) and t.pytype is not None:
                    if isinstance(obj, t.pytype):
                        return True
                elif isinstance(t, Cls):
                    if isinstance(obj, Inst) and obj.cls.is_sub(t):
                        return True
                else:
                    self.throw("TypeError", "isinstance() arg 2 must be a type")
            return False
        for name, cls in EXC.items():
            B[name] = cls
        return B


_MISSING = object()


def _raise_it(e):
    raise e


class World(object):
    """Module table for one test run: {stem: source}. A module is evaluated once, on first import; a failing import is not cached."""

    def __init__(self, sources):
        self.sources = dict(sources)
        self.mods = {}

    def import_module(self, interp, name):
        if name in self.mods:
            return self.mods[name]
        if name not in self.sources:
            if name.split(".")[0] in _STDLIB_SEEN:
                raise Unsupported("stdlib import " + name)
            interp.throw("ModuleNotFoundError", "No module named '%s'" % name)
        src = self.sources[name]
        reason = check_syntax(src)
        if reason:
            interp.throw("SyntaxError", reason)
        mod = Mod(name)
        self.mods[name] = mod
        try:
            interp.run_module(ast.parse(src), mod)
        except BaseException:
            self.mods.pop(name, None)
            raise
        return mod


_STDLIB_SEEN = set(getattr(sys, "stdlib_module_names", ())) | {"pytest"}


def run_suite(world, source, name="tests"):
    """Run one pytest-like test module against `world` (fresh interpreter state). -> SuiteResult"""
    interp = Interp()
    interp.world = world
    old = sys.getrecursionlimit()
    sys.setrecursionlimit(max(old, 8000))
    try:
        reason = check_syntax(source)
        if reason:
            return SuiteResult("fail", 0, 1, "test file syntax: " + reason)
        tree = ast.parse(source)
        mod = Mod(name)
        try:
            fr = interp.run_module(tree, mod)
        except Throw as t:
            return SuiteResult("fail", 0, 1, "collection error: " + t.inst.cls.name)
        tests = [s.name for s in tree.body if isinstance(s, ast.FunctionDef) and s.name.startswith("test")]
        if not tests:
            return SuiteResult("unsupported", 0, 0, "no tests collected")
        passed = failed = 0
        for tn in tests:
            fn = mod.ns.get(tn)
            if not isinstance(fn, Func):
                return SuiteResult("unsupported", passed, failed, "test rebound")
            try:
                interp.call(fn, [], {})
                passed += 1
            except Throw:
                failed += 1
            except _Ret:
                passed += 1
        return SuiteResult("pass" if failed == 0 else "fail", passed, failed, "")
    except Unsupported as u:
        return SuiteResult("unsupported", 0, 0, str(u))
    except RecursionError:
        return SuiteResult("unsupported", 0, 0, "native recursion")
    finally:
        sys.setrecursionlimit(old)

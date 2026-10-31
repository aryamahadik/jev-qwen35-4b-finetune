"""Solver B dataflow engine (T65): an abstract interpreter over the Python AST of the RENDERED function. Nothing is executed or compiled: `ast.parse` builds the
tree and the engine walks it, tracking AVal summaries per variable over all paths (branches are forked and joined; code after a return / raise is unreachable;
module-level helpers are analysed inline with the caller's argument values). Unmodelled constructs raise Unsupported (the solver then abstains)."""
import ast
import re

from . import rules as R
from . import values as V
from .values import AVal


class Unsupported(Exception):
    pass


class State(object):
    def __init__(self, env=None, heap=None, entry=False):
        self.env = env if env is not None else {}
        self.heap = heap if heap is not None else {}
        self.term = False
        self.rets = []
        self.entry = entry

    def fork(self):
        s = State(dict(self.env), {h: dict(a) for h, a in self.heap.items()}, self.entry)
        s.rets = self.rets            # returns of the frame are collected in one shared list
        return s


def _join_env(envs):
    out = {}
    names = []
    for e in envs:
        for k in e:
            if k not in names:
                names.append(k)
    for k in names:
        acc = None
        for e in envs:
            if k in e:
                acc = e[k] if acc is None else V.join(acc, e[k])
        out[k] = acc
    return out


def _join_heap(heaps):
    out = {}
    for hp in heaps:
        for h, attrs in hp.items():
            cur = out.setdefault(h, {})
            for a, vals in attrs.items():
                cur[a] = cur.get(a, frozenset()) | vals
    return out


class Engine(object):
    MAX_DEPTH = 8

    def __init__(self, src, attacker_param=None, question=None):
        self.tree = ast.parse(src)
        self.attacker_param = attacker_param
        self.question = question
        self.alias, self.consts, self.listconsts, self.funcs = {}, {}, {}, {}
        self.flaws, self.evidence, self.entry_returns = set(), set(), []
        self.stack, self.next_handle = [], 1
        self._load_module()
        self.entry = self._pick_entry()

    # ---- module level ------------------------------------------------------------------------------------------------------
    def _load_module(self):
        for node in self.tree.body:
            if isinstance(node, ast.Import):
                for a in node.names:
                    self.alias[(a.asname or a.name.split(".")[0])] = a.name if a.asname else a.name.split(".")[0]
            elif isinstance(node, ast.ImportFrom):
                if node.level or not node.module:
                    raise Unsupported("relative import")
                for a in node.names:
                    self.alias[a.asname or a.name] = node.module + "." + a.name
            elif isinstance(node, ast.FunctionDef):
                if node.name in self.funcs:
                    raise Unsupported("redefined function")
                self.funcs[node.name] = node
            elif isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                v = self._literal(node.value)
                self.consts[node.targets[0].id] = v
                if isinstance(node.value, (ast.Tuple, ast.List, ast.Set)):
                    self.listconsts[node.targets[0].id] = [e.value for e in node.value.elts if isinstance(e, ast.Constant)]
            elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
                continue
            else:
                raise Unsupported("module statement " + type(node).__name__)

    def _literal(self, node):
        if isinstance(node, ast.Constant):
            return V.const(node.value)
        if isinstance(node, (ast.Tuple, ast.List, ast.Set)):
            items = tuple(self._literal(e) for e in node.elts)
            return AVal(items=items, kind="tuple", lits=sum([i.lits for i in items], ()))
        if isinstance(node, ast.Dict) and all(isinstance(k, ast.Constant) for k in node.keys):
            items = {k.value: self._literal(v) for k, v in zip(node.keys, node.values)}
            return AVal(items=items, kind="dict", lits=sum([i.lits for i in items.values()], ()))
        raise Unsupported("module constant " + type(node).__name__)

    def _pick_entry(self):
        if not self.funcs:
            raise Unsupported("no function")
        called = set()
        for f in self.funcs.values():
            for n in ast.walk(f):
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in self.funcs and n.func.id != f.name:
                    called.add(n.func.id)
        roots = [n for n in self.funcs if n not in called]
        if not roots:
            raise Unsupported("no entry function")
        pick = roots[-1]                         # the last uncalled function is the one the service calls
        if self.question:
            words = list(dict.fromkeys(re.findall(r"(?<![A-Za-z0-9_])[A-Za-z_][A-Za-z0-9_]*(?![A-Za-z0-9_])", self.question)))
            named = [w for w in words if w in self.funcs]
            if len(named) == 1 and named[0] != pick:
                if named[0] in roots:
                    pick = named[0]                # the question names the function: it is the entry when it is a root
                else:
                    raise Unsupported("entry ambiguity")
        return self.funcs[pick]

    # ---- run ---------------------------------------------------------------------------------------------------------------
    def run(self):
        f = self.entry
        a = f.args
        if a.vararg or a.kwarg or a.kwonlyargs or a.posonlyargs:
            raise Unsupported("entry signature")
        names = [x.arg for x in a.args]
        env = {}
        if self.attacker_param is not None and self.attacker_param not in names:
            raise Unsupported("named parameter missing in entry")
        for n in names:
            pw = any(n.lower().startswith(s) or n.lower().endswith(s) for s in R.PW_NAME_STEMS)
            if self.attacker_param is None:
                env[n] = V.tainted(pw=pw)           # head row / static slice: every parameter of the service entry is request data
            else:
                env[n] = V.tainted(pw=pw) if n == self.attacker_param else AVal(pw=pw)
        st = State(env=env, entry=True)
        self.stack.append(f.name)
        self.block(f.body, st)
        self.stack.pop()
        return self

    # ---- statements --------------------------------------------------------------------------------------------------------
    def block(self, stmts, st):
        for s in stmts:
            if st.term:
                return                         # unreachable code after return / raise is never evaluated
            self.stmt(s, st)

    def stmt(self, node, st):
        m = getattr(self, "s_" + type(node).__name__, None)
        if m is None:
            raise Unsupported("statement " + type(node).__name__)
        m(node, st)

    def s_Pass(self, node, st):
        pass

    def s_Import(self, node, st):
        raise Unsupported("import inside function")

    def s_Expr(self, node, st):
        if isinstance(node.value, ast.Constant):
            return
        self.ev(node.value, st)

    def s_Assert(self, node, st):
        pass

    def s_Raise(self, node, st):
        st.term = True

    def s_Return(self, node, st):
        val = self.ev(node.value, st) if node.value is not None else V.NONE
        st.rets.append(val)
        if st.entry:
            self.entry_returns.append(val)
            self.use_check(val, st)
        st.term = True

    def s_Assign(self, node, st):
        val = self.ev(node.value, st)
        for t in node.targets:
            self.assign(t, val, st)

    def s_AnnAssign(self, node, st):
        if node.value is not None:
            self.assign(node.target, self.ev(node.value, st), st)

    def s_AugAssign(self, node, st):
        if not isinstance(node.target, ast.Name) or node.target.id not in st.env or not isinstance(node.op, ast.Add):
            raise Unsupported("augassign")
        st.env[node.target.id] = self.concat(st.env[node.target.id], self.ev(node.value, st))

    def assign(self, target, val, st):
        if isinstance(target, ast.Name):
            st.env[target.id] = val
        elif isinstance(target, (ast.Tuple, ast.List)):
            n = len(target.elts)
            if isinstance(val.items, tuple) and len(val.items) == n:
                parts = list(val.items)
            elif val.items is None:
                parts = [V.summary(val)] * n
            else:
                raise Unsupported("unpack shape")
            for t, p in zip(target.elts, parts):
                self.assign(t, p, st)
        elif isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name) and target.value.id in st.env:
            obj = st.env[target.value.id]
            if obj.handle is None:
                if obj.sensitive():
                    raise Unsupported("attribute store on value")
                return
            known = isinstance(val.const, (bool, str)) and (val.kind == "enum" or isinstance(val.const, bool))
            st.heap[obj.handle][target.attr] = frozenset([val.const]) if known else frozenset(["?"])
        elif isinstance(target, ast.Subscript) and isinstance(target.value, ast.Name) and target.value.id in st.env:
            cont = st.env[target.value.id]
            if isinstance(cont.items, dict) and isinstance(target.slice, ast.Constant):
                d = dict(cont.items)
                d[target.slice.value] = val
                st.env[target.value.id] = V.combine([cont, val]).replace(items=d, kind="dict")
            else:
                raise Unsupported("subscript store")
        else:
            raise Unsupported("assign target " + type(target).__name__)

    def s_If(self, node, st):
        t, f = st.fork(), st.fork()
        self.refine(node.test, t, f)
        self.block(node.body, t)
        self.block(node.orelse, f)
        live = [s for s in (t, f) if not s.term]
        if not live:
            st.term = True
            return
        st.env = _join_env([s.env for s in live])
        newheap = _join_heap([s.heap for s in live])
        st.heap.clear()
        st.heap.update(newheap)

    def refine(self, test, t, f):
        """An allow-list test (`x in K`, `x not in K`, `x == "const"`, `x != "const"`) with K fixed constants: in the branch where it holds, x is one of the
        constants, so it is neutral for every class (G0-lite NS-2). Any other condition is unknown: both branches stay possible."""
        neg = False
        while isinstance(test, ast.UnaryOp) and isinstance(test.op, ast.Not):
            neg, test = not neg, test.operand
        if not (isinstance(test, ast.Compare) and len(test.ops) == 1 and isinstance(test.left, ast.Name)):
            return
        op, right, name = test.ops[0], test.comparators[0], test.left.id
        member = None
        if isinstance(op, (ast.In, ast.NotIn)):
            if isinstance(right, (ast.Tuple, ast.List, ast.Set)) and all(isinstance(e, ast.Constant) for e in right.elts):
                member = True
            elif isinstance(right, ast.Name) and right.id in self.listconsts:
                member = True
            if member:
                holds_in_true = isinstance(op, ast.In)
            else:
                return
        elif isinstance(op, (ast.Eq, ast.NotEq)) and isinstance(right, ast.Constant) and isinstance(right.value, str):
            holds_in_true = isinstance(op, ast.Eq)
        else:
            return
        if neg:
            holds_in_true = not holds_in_true
        target = t if holds_in_true else f
        cur = target.env.get(name)
        if cur is not None and cur.atk:
            target.env[name] = cur.replace(neut=R.ALL_NEUT)

    # ---- expressions -------------------------------------------------------------------------------------------------------
    def ev(self, node, st):
        m = getattr(self, "e_" + type(node).__name__, None)
        if m is None:
            raise Unsupported("expression " + type(node).__name__)
        return m(node, st)

    def e_Constant(self, node, st):
        return V.const(node.value)

    def e_Name(self, node, st):
        if node.id in st.env:
            return st.env[node.id]
        if node.id in self.consts:
            return self.consts[node.id]
        raise Unsupported("name " + node.id)

    def e_Tuple(self, node, st):
        items = tuple(self.ev(e, st) for e in node.elts)
        return V.combine(items).replace(items=items, kind="tuple")

    e_List = e_Tuple
    e_Set = e_Tuple

    def e_Dict(self, node, st):
        items = {}
        for i, (k, v) in enumerate(zip(node.keys, node.values)):
            if k is None:
                raise Unsupported("dict unpack")
            key = k.value if isinstance(k, ast.Constant) else ("?", i)
            items[key] = self.ev(v, st)
        return V.combine(list(items.values())).replace(items=items, kind="dict")

    def e_Subscript(self, node, st):
        cont = self.ev(node.value, st)
        idx = node.slice
        if cont.items is not None and isinstance(idx, ast.Constant):
            if isinstance(cont.items, dict) and idx.value in cont.items:
                return cont.items[idx.value]
            if isinstance(cont.items, tuple) and isinstance(idx.value, int) and -len(cont.items) <= idx.value < len(cont.items):
                return cont.items[idx.value]
        if isinstance(idx, ast.Slice):
            for part in (idx.lower, idx.upper, idx.step):
                if part is not None:
                    self.ev(part, st)
        elif not isinstance(idx, ast.Constant):
            self.ev(idx, st)
        return V.summary(cont)

    def e_Attribute(self, node, st):
        q = self.qual(node, st)
        if q is not None:
            if q.startswith("ssl.CERT_") or q.startswith("ssl.TLSVersion.") or q.startswith("ssl.PROTOCOL_"):
                return AVal(kind="enum", const=q)
            return V.CLEAN
        base = self.ev(node.value, st)
        return base.replace(handle=None, items=None, kind="val", const=None)

    def e_BinOp(self, node, st):
        if isinstance(node.op, ast.Add) and isinstance(node.left, ast.Constant) and node.left.value == "/" and self.is_lstrip_slash(node.right):
            inner = self.ev(node.right, st)               # "/" + x.lstrip("/"): the result always starts with exactly one slash (a local path)
            return inner.replace(lits=("/",) + inner.lits, neut=(inner.neut | {"CWEC-601"}))
        left, right = self.ev(node.left, st), self.ev(node.right, st)
        if isinstance(node.op, ast.Add):
            return self.concat(left, right)
        if isinstance(node.op, (ast.Mod, ast.Mult)):
            return V.combine([V.summary(left), V.summary(right)])
        raise Unsupported("binop " + type(node.op).__name__)

    @staticmethod
    def is_lstrip_slash(n):
        return (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "lstrip" and len(n.args) == 1 and not n.keywords
                and isinstance(n.args[0], ast.Constant) and n.args[0].value == "/")

    def concat(self, a, b):
        a, b = V.summary(a), V.summary(b)
        out = V.combine([a, b])
        if (a.shared or b.shared) and not (a.pred or b.pred):
            out = out.replace(shared=False, pred=True)        # a name built inside the shared temp directory is predictable
        if a.const is not None and b.const is not None and isinstance(a.const, str) and isinstance(b.const, str):
            out = out.replace(const=a.const + b.const)
        return out

    def e_JoinedStr(self, node, st):
        parts = []
        for v in node.values:
            parts.append(self.ev(v.value, st) if isinstance(v, ast.FormattedValue) else self.ev(v, st))
        return V.combine([V.summary(p) for p in parts])

    def e_IfExp(self, node, st):
        self.ev(node.test, st)
        return V.join(self.ev(node.body, st), self.ev(node.orelse, st))

    def e_BoolOp(self, node, st):
        vals = [self.ev(v, st) for v in node.values]
        acc = vals[0]
        for v in vals[1:]:
            acc = V.join(acc, v)
        return acc

    def e_Compare(self, node, st):
        self.ev(node.left, st)
        for c in node.comparators:
            self.ev(c, st)
        return V.CLEAN

    def e_UnaryOp(self, node, st):
        self.ev(node.operand, st)
        return V.CLEAN

    # ---- calls -------------------------------------------------------------------------------------------------------------
    def qual(self, node, st):
        """Dotted name of an attribute chain rooted at an imported module (os.path.join), else None."""
        parts = []
        while isinstance(node, ast.Attribute):
            parts.append(node.attr)
            node = node.value
        if not isinstance(node, ast.Name) or node.id in st.env or node.id not in self.alias:
            return None
        parts.append(self.alias[node.id])
        return ".".join(reversed(parts))

    def args_of(self, node, st):
        args = [self.ev(a, st) for a in node.args]
        kws = {}
        for k in node.keywords:
            if k.arg is None:
                raise Unsupported("**kwargs")
            kws[k.arg] = self.ev(k.value, st)
        return args, kws

    def e_Call(self, node, st):
        f = node.func
        if isinstance(f, ast.Name):
            if f.id in st.env:
                raise Unsupported("call of a variable")
            if f.id in self.funcs:
                args, kws = self.args_of(node, st)
                return self.call_user(self.funcs[f.id], args, kws, st)
            if f.id in self.alias:
                return self.call_qualified(self.alias[f.id], node, st)
            return self.call_builtin(f.id, node, st)
        if isinstance(f, ast.Attribute):
            q = self.qual(f, st)
            if q is not None:
                return self.call_qualified(q, node, st)
            return self.call_method(f, node, st)
        raise Unsupported("call target " + type(f).__name__)

    def call_user(self, fdef, args, kws, st):
        if fdef.name in self.stack or len(self.stack) >= self.MAX_DEPTH:
            raise Unsupported("recursion / depth")
        a = fdef.args
        if a.vararg or a.kwarg or a.kwonlyargs or a.posonlyargs:
            raise Unsupported("helper signature")
        names = [x.arg for x in a.args]
        env = {}
        for n, v in zip(names, args):
            env[n] = v
        if len(args) > len(names):
            raise Unsupported("too many args")
        for k, v in kws.items():
            if k not in names or k in env:
                raise Unsupported("bad keyword")
            env[k] = v
        defaults = a.defaults
        for n, d in zip(names[len(names) - len(defaults):], defaults):
            if n not in env:
                env[n] = self._literal(d)
        if any(n not in env for n in names):
            raise Unsupported("missing args")
        callee = State(env=env, heap=st.heap, entry=False)
        self.stack.append(fdef.name)
        self.block(fdef.body, callee)
        self.stack.pop()
        rets = list(callee.rets)
        if not callee.term:
            rets.append(V.NONE)
        acc = rets[0]
        for r in rets[1:]:
            acc = V.join(acc, r)
        return acc

    def sink_check(self, cls, val):
        if val.atk and cls not in val.neut:
            self.flaws.add(cls)

    def call_builtin(self, name, node, st):
        args, kws = self.args_of(node, st)
        if name == "open":
            self.evidence.add("CWEC-22")
            if args:
                self.sink_check("CWEC-22", V.summary(args[0]))
                if args[0].pred:
                    self.flaws.add("CWEC-377")          # a predictable temporary name is used to create / open a file
            return AVal(kind="file")
        if name in R.CLEAN_BUILTINS:
            return V.CLEAN
        if name in R.PASS_BUILTINS:
            return V.combine([V.summary(a) for a in args] + [V.summary(v) for v in kws.values()])
        if name in ("ValueError", "TypeError", "KeyError", "RuntimeError", "Exception", "PermissionError", "OSError"):
            return V.CLEAN
        raise Unsupported("builtin " + name)

    def call_qualified(self, q, node, st):
        args, kws = self.args_of(node, st)
        a0 = args[0] if args else None
        if q in R.NEUTRALISER_CALLS:
            if a0 is None:
                raise Unsupported("neutraliser without argument")
            v = V.summary(a0)
            return v.replace(neut=v.neut | {R.NEUTRALISER_CALLS[q]})
        if q == "os.path.join":
            parts = [V.summary(a) for a in args]
            out = V.combine(parts)
            if any(p.shared for p in parts):
                out = out.replace(shared=False, pred=True)
            return out
        if q in ("os.path.normpath", "os.path.abspath", "os.path.realpath", "os.path.expanduser", "os.path.normcase", "os.fspath"):
            return V.summary(a0) if a0 is not None else V.CLEAN
        if q == "open":
            return self.call_builtin("open", node, st)
        if q in R.SHELL_CALLS or q in R.SHELL_STRING_CALLS:
            self.evidence.add("CWEC-78")
            shell = q in R.SHELL_STRING_CALLS or (isinstance(kws.get("shell"), AVal) and kws["shell"].const is True)
            if q in ("subprocess.getoutput", "subprocess.getstatusoutput"):
                shell = True
            if a0 is not None and shell:
                cmd = a0.items[0] if (isinstance(a0.items, tuple) and a0.items) else V.summary(a0)
                self.sink_check("CWEC-78", cmd)
            return AVal(kind="proc")
        if q == "sqlite3.connect":
            return AVal(kind="conn")
        if q == "ssl.create_default_context":
            return self.new_ctx(st, {"verify_mode": frozenset(["ssl.CERT_REQUIRED"]), "check_hostname": frozenset([True])})
        if q in ("ssl._create_unverified_context", "ssl._create_stdlib_context"):
            return self.new_ctx(st, {"verify_mode": frozenset(["ssl.CERT_NONE"]), "check_hostname": frozenset([False])})
        if q.startswith("hashlib."):
            name = q.split(".", 1)[1]
            self.evidence.add("CWEC-327")
            if name == "new" and a0 is not None and isinstance(a0.const, str):
                name = a0.const.lower()
                args = args[1:]
                a0 = args[0] if args else None
            if name in R.FAST_HASHES:
                return AVal(weak=bool(a0 is not None and V.summary(a0).pw), kind="digest")
            if name in R.SLOW_HASHES:
                return AVal(kind="digest")
            raise Unsupported("hash " + name)
        if q.startswith("tempfile."):
            name = q.split(".", 1)[1]
            self.evidence.add("CWEC-377")
            if name == "mktemp":
                return AVal(pred=True, kind="str")
            if name == "mkstemp":
                return AVal(items=(AVal(kind="num"), AVal(kind="str")), kind="tuple")
            if name == "gettempdir":
                return AVal(shared=True, kind="str")
            if name in ("mkdtemp", "NamedTemporaryFile", "TemporaryFile", "TemporaryDirectory", "SpooledTemporaryFile"):
                return AVal(kind="str" if name == "mkdtemp" else "file")
            raise Unsupported("tempfile " + name)
        if any(V.summary(a).sensitive() or (a.handle is not None) for a in args + list(kws.values())):
            raise Unsupported("unmodelled call " + q)
        return V.CLEAN

    def new_ctx(self, st, attrs):
        h = self.next_handle
        self.next_handle += 1
        st.heap[h] = dict(attrs)
        return AVal(kind="ssl", handle=h)

    def call_method(self, f, node, st):
        recv = self.ev(f.value, st)
        name = f.attr
        args, kws = self.args_of(node, st)
        if name == "replace" and len(node.args) >= 2 and all(isinstance(a, ast.Constant) and isinstance(a.value, str) for a in node.args[:2]):
            pair = (node.args[0].value, node.args[1].value)
            v = V.summary(recv)
            if pair in R.REPLACE_NEUT:
                return v.replace(neut=v.neut | {R.REPLACE_NEUT[pair]})
            if v.sensitive():
                raise Unsupported("replace arguments")
            return v
        if name == "replace":
            raise Unsupported("replace form")
        if name in R.PASS_METHODS:
            return V.summary(recv)
        if name == "format":
            return V.combine([V.summary(recv)] + [V.summary(a) for a in args] + [V.summary(v) for v in kws.values()])
        if name == "join":
            return V.combine([V.summary(recv)] + [V.summary(a) for a in args])
        if name == "cursor":
            return AVal(kind="cur")
        if name in ("execute", "executescript", "executemany"):
            if args:
                sql = V.summary(args[0])
                if sql.atk or any(l.upper().lstrip().startswith(("SELECT", "UPDATE", "DELETE")) for l in sql.lits):
                    self.evidence.add("CWEC-89")
                self.sink_check("CWEC-89", sql)
            return AVal(kind="cur")
        if name in R.CLEAN_RESULT_METHODS:
            return V.CLEAN
        if name == "get" and recv.items is not None and isinstance(recv.items, dict) and node.args and isinstance(node.args[0], ast.Constant):
            return recv.items.get(node.args[0].value) or (args[1] if len(args) > 1 else V.CLEAN)
        if name in ("communicate", "wait", "poll", "fileno"):
            return V.CLEAN
        if not (V.summary(recv).sensitive() or any(V.summary(a).sensitive() for a in args)):
            return V.CLEAN
        raise Unsupported("method " + name)

    # ---- use checks (return of the entry function) ------------------------------------------------------------------------
    def use_check(self, val, st):
        mem = [val]
        i = 0
        while i < len(mem):
            v = mem[i]
            i += 1
            if isinstance(v.items, dict):
                mem.extend(v.items.values())
            elif isinstance(v.items, tuple):
                mem.extend(v.items)
        for v in mem:
            if v.weak:
                self.flaws.add("CWEC-327")
            if v.pred:
                self.flaws.add("CWEC-377")
            if v.handle is not None and v.kind == "ssl":
                self.evidence.add("CWEC-295")
                attrs = st.heap.get(v.handle, {})
                if "ssl.CERT_NONE" in attrs.get("verify_mode", ()) or False in attrs.get("check_hostname", ()):
                    self.flaws.add("CWEC-295")
        s = V.summary(val)
        lits = s.lits
        if any("<" in l for l in lits if isinstance(l, str)):
            self.evidence.add("CWEC-79")
            cls = "CWEC-79"
        elif any(l.strip().split(" ")[0].rstrip(":=").upper() in R.LOG_LEVEL_WORDS for l in lits if isinstance(l, str) and l.strip()):
            self.evidence.add("CWEC-117")
            cls = "CWEC-117"
        else:
            cls = "CWEC-601"
            self.evidence.add("CWEC-601")
        self.sink_check(cls, s)

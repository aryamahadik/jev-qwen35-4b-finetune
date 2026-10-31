"""Reference interpreter for the IR (SPEC EXPECTATION only; it never replaces the sandbox witness).

It evaluates our own IR tree, not rendered source, so unit tests can predict what a rendered module should do
without executing any generated code. Language dialects differ only where the real runtimes differ:
  * `//` and `%`: Python floors; JavaScript, Go and bash truncate toward zero;
  * list indexing out of range: Python raises IndexError (negative indices wrap, which the dialect reports as an
    event because the other languages do not), the other languages are undefined -> event `oob_index`;
  * integers outside +-(2^31-1) are reported as event `big_int` (JavaScript doubles, Go/bash int64 would diverge).
Events are NOT errors: they mark a run as non-portable so a generator can reject it.

Outcome: ("ok", value) or ("exc", error_id) where error_id is an explicit ERR_* id or an implicit one
(`IMP_INDEX` for Python's IndexError). `steps` counts executed statements (see `Interp.steps`).
"""
import copy

from . import ir as I

MAX_STEPS = 200000


class Raised(Exception):
    def __init__(self, err):
        super().__init__(err)
        self.err = err


class _Ret(Exception):
    def __init__(self, value):
        self.value = value


class StepLimit(Exception):
    pass


def idiv(a, c, lang):
    if lang == "python":
        return a // c
    q = abs(a) // abs(c)
    return q if (a >= 0) == (c >= 0) else -q


def imod(a, c, lang):
    if lang == "python":
        return a % c
    r = abs(a) % abs(c)
    return r if a >= 0 else -r


class Interp:
    def __init__(self, mod, lang="python", max_steps=MAX_STEPS):
        self.mod = mod
        self.lang = lang
        self.fns = I.functions(mod)
        self.max_steps = max_steps
        self.steps = 0
        self.events = set()
        self.called = set()          # names of every function invoked (trace of the entities a run traverses)
        self.consts = {c["name"]: copy.deepcopy(c["value"]) for c in mod["consts"]}
        self.fields = None
        self.reset_state()

    # ------------------------------------------------------------------ state
    def reset_state(self):
        cls = self.mod["cls"]
        self.fields = {f["name"]: copy.deepcopy(f["init"]) for f in cls["fields"]} if cls else {}

    def reset(self):
        """Fresh instance state + counters, reusing the parsed module (cheap per-point reset for domain scans)."""
        self.reset_state()
        self.reset_counters()

    def reset_counters(self):
        self.steps = 0
        self.events = set()
        self.called = set()

    # ------------------------------------------------------------------ public
    def call(self, name, args):
        """Run one top-level call on the current state. Returns ("ok", value) | ("exc", error_id)."""
        fn = self.fns[name]
        try:
            v = self._invoke(fn, list(args))
            return ("ok", list(v) if isinstance(v, list) else v)          # a returned list never aliases state
        except Raised as r:
            return ("exc", r.err)

    def sequence(self, calls):
        """Per-call outcomes for a list of (name, args). Exceptions are recorded and the sequence continues."""
        return [self.call(n, a) for n, a in calls]

    # ------------------------------------------------------------------ execution
    def _tick(self, n=1):
        self.steps += n
        if self.steps > self.max_steps:
            raise StepLimit()

    def _invoke(self, fn, args):
        self.called.add(fn["name"])
        env = {p[0]: a for p, a in zip(fn["params"], args)}
        try:
            self._block(fn["body"], env)
        except _Ret as r:
            return r.value
        raise AssertionError("function %s fell off the end" % fn["name"])

    def _block(self, stmts, env):
        for st in stmts:
            self._stmt(st, env)

    def _stmt(self, st, env):
        h = st[0]
        if h not in ("for", "each"):
            self._tick()
        if h == "let":
            env[st[1]] = self._e(st[3], env)
        elif h == "set":
            env[st[1]] = self._e(st[2], env)
        elif h == "setf":
            self.fields[st[1]] = self._e(st[2], env)
        elif h == "sidx":
            tgt = self._target(st[1], env)
            k = self._e(st[2], env)
            if not 0 <= k < len(tgt):
                self.events.add("oob_index")
                raise Raised("IMP_INDEX")
            tgt[k] = self._e(st[3], env)
        elif h == "push":
            self._target(st[1], env).append(self._e(st[2], env))
        elif h == "popto":
            tgt = self._target(st[3], env)
            if not tgt:
                self.events.add("oob_index")
                raise Raised("IMP_INDEX")
            env[st[1]] = tgt.pop()
        elif h == "shiftto":
            tgt = self._target(st[3], env)
            if not tgt:
                self.events.add("oob_index")
                raise Raised("IMP_INDEX")
            env[st[1]] = tgt.pop(0)
        elif h == "if":
            if self._e(st[1], env):
                self._block(st[2], env)
            else:
                self._block(st[3], env)
        elif h == "for":
            lo, hi = self._e(st[2], env), self._e(st[3], env)
            for k in range(lo, hi):
                self._tick()
                env[st[1]] = k
                self._block(st[4], env)
            self._tick()          # the failing loop test: a loop of n iterations costs n + 1 header steps
            env.pop(st[1], None)
        elif h == "each":
            xs = list(self._e(st[2], env))
            for x in xs:
                self._tick()
                env[st[1]] = x
                self._block(st[3], env)
            self._tick()
            env.pop(st[1], None)
        elif h == "ret":
            raise _Ret(self._e(st[1], env))
        elif h == "raise":
            raise Raised(st[1])
        elif h == "do":
            self._e(st[1], env)
        else:
            raise AssertionError("bad statement %r" % h)

    def _target(self, t, env):
        if t[0] == "var":
            return env[t[1]]
        return self.fields[t[1]]

    def _chk(self, n):
        if isinstance(n, int) and not isinstance(n, bool) and abs(n) > I.INT_LIMIT:
            self.events.add("big_int")
        return n

    def _e(self, e, env):
        h = e[0]
        if h in ("int", "str", "bool"):
            return e[1]
        if h == "var":
            return env[e[1]]
        if h == "field":
            return self.fields[e[1]]
        if h == "const":
            return self.consts[e[1]]
        if h == "bin":
            op = e[1]
            if op == "and":
                return bool(self._e(e[2], env)) and bool(self._e(e[3], env))
            if op == "or":
                return bool(self._e(e[2], env)) or bool(self._e(e[3], env))
            a, c = self._e(e[2], env), self._e(e[3], env)
            if op == "+":
                return self._chk(a + c)
            if op == "-":
                return self._chk(a - c)
            if op == "*":
                return self._chk(a * c)
            if op == "//":
                return idiv(a, c, self.lang)
            if op == "%":
                return imod(a, c, self.lang)
            if op == "<":
                return a < c
            if op == "<=":
                return a <= c
            if op == ">":
                return a > c
            if op == ">=":
                return a >= c
            if op == "==":
                return a == c
            if op == "!=":
                return a != c
            if op == "++":
                return a + c
            raise AssertionError(op)
        if h == "not":
            return not self._e(e[1], env)
        if h == "min":
            return min(self._e(e[1], env), self._e(e[2], env))
        if h == "max":
            return max(self._e(e[1], env), self._e(e[2], env))
        if h == "cond":
            return self._e(e[2], env) if self._e(e[1], env) else self._e(e[3], env)
        if h == "len":
            return len(self._e(e[1], env))
        if h == "idx":
            xs, k = self._e(e[1], env), self._e(e[2], env)
            if self.lang == "python":
                if k < 0:
                    self.events.add("neg_index")
                if not -len(xs) <= k < len(xs):
                    raise Raised("IMP_INDEX")
                return xs[k]
            if not 0 <= k < len(xs):
                self.events.add("oob_index")
                raise Raised("IMP_INDEX")
            return xs[k]
        if h == "lst":
            return [self._e(x, env) for x in e[2]]
        if h == "istr":
            return str(self._e(e[1], env))
        if h == "zpad":
            n = self._e(e[1], env)
            if n < 0:
                self.events.add("neg_zpad")
            return str(n).zfill(e[2][1])
        if h == "has":
            return self._e(e[2], env) in self._e(e[1], env)
        if h == "starts":
            return self._e(e[1], env).startswith(self._e(e[2], env))
        if h in ("fcall", "mcall"):
            fn = self.fns[e[1]]
            args = [self._e(a, env) for a in e[2]]            # parameters are never mutated (IR rule), so no copy
            return self._invoke(fn, args)
        raise AssertionError(h)


def run_calls(mod, calls, lang="python"):
    """Fresh state, run a list of (name, args). Returns (outcomes, interp)."""
    it = Interp(mod, lang)
    return it.sequence(calls), it


def outcome_json(out):
    """Canonical language-neutral observable for one outcome."""
    return {"ok": out[1]} if out[0] == "ok" else {"exc": out[1]}

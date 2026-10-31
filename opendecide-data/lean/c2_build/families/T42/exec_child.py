"""families/T42/exec_child.py: the hermetic child that executes generated snippets (T42 solver A, execution side).

Started by executor.py as   python -S -s -B -P exec_child.py   with PYTHONHASHSEED=0, an empty temp dir as cwd, a
minimal environment, a 5 s cap from the parent (kill) and RLIMIT_CPU / RLIMIT_FSIZE set here. It reads one JSON job
from stdin and writes one JSON result to stdout.

  mode "snippets"  {"jobs": [{"id", "code", "kind": "print" | "result"}], "cap": steps}
                   per job: exec the code with stdout captured, a line-event step cap (settrace) and a 1.5 s wall cap
                   -> {"s": ok | exc | cap | timeout, "out", "exc", "steps"}
  mode "equiv"     {"f": src, "g": src, "sig": [type, ...], "seed": n, "fuzz": n}
                   typical grid, full grid (typical + edge + cross), 10K fuzz, branch coverage (sys.settrace with opcode
                   events over the bytecode conditional jumps) -> raw counts (the parent applies the label rule)

No network, no writes: an audit hook refuses sockets, subprocesses, process creation and any file opened for writing;
RLIMIT_FSIZE is 0. Nothing here imports any T42 module (the child is a plain program: solver A is CPython itself).
"""
import contextlib
import io
import itertools
import json
import os
import resource
import signal
import sys

ALLOWED_EXC = {"ValueError", "TypeError", "KeyError", "IndexError", "ZeroDivisionError", "AttributeError", "NameError",
               "UnboundLocalError", "StopIteration", "AssertionError", "OverflowError", "LookupError",
               "RecursionError", "NotImplementedError"}
LINE_CAP_HARD = 700
JOB_SECONDS = float(os.environ.get("T42_INNER_TIMEOUT") or 1.5)     # the env knob is a test hook: a tiny timeout must only cause drops
CALL_SECONDS = float(os.environ.get("T42_INNER_TIMEOUT") or 0.25)


class _Cap(BaseException):
    pass


class _Timeout(BaseException):
    pass


class EnvError(RuntimeError):
    """A wall-clock timeout is never an outcome (A45 / T45 rule): the child exits 97, the parent repeats the job and, after the
    last repeat, drops the spec (ExecTimeout). Deterministic caps (the step cap of snippets) stay outcomes."""


_ARMED = [False]


def _on_alarm(signum, frame):
    if _ARMED[0]:                       # a late alarm delivered after the timer was cancelled is ignored
        _ARMED[0] = False
        raise _Timeout()


def _arm(seconds):
    _ARMED[0] = True
    signal.setitimer(signal.ITIMER_REAL, seconds)


def _disarm():
    _ARMED[0] = False
    signal.setitimer(signal.ITIMER_REAL, 0)


# ------------------------------------------------------------------------------------------------ typical / edge values
T_INT = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12]
E_INT = [-9, -5, -3, -2, -1, 0, 1, 100]
_POOL = [2, 3, 5, 7, 8]
T_LIST = []
for _r in (3, 4, 5):
    for _c in itertools.combinations(_POOL, _r):
        _a = list(_c)
        T_LIST.append(_a)
        T_LIST.append(_a[::-1][1:] + _a[::-1][:1])
E_LIST = [[], [0], [1], [5], [-3], [2, 5], [5, 2], [3, 3], [2, 2, 2], [1, 1, 2], [4, -1, 2], [0, 5, 2], [3, 0, 3, 9],
          [2, 5, 2, 5], [-4, -2, -7]]
T_STR = ["stone", "plant", "brick", "charm", "dwarf", "flame", "glove", "house", "joint", "knife", "lemon", "money",
         "night", "ocean", "piano", "queen", "river", "sugar", "table", "voice", "wheat", "young", "zebra", "crisp"]
E_STR = ["", "a", "ab", "A", "Ab", "ABC", "a b", " x", "x ", "a1", "7", "aa", "aaa", "ab ba"]
TYP = {"int": T_INT, "ints": T_LIST, "str": T_STR}
EDG = {"int": E_INT, "ints": E_LIST, "str": E_STR}


def grids(sig):
    typ = [list(c) for c in itertools.product(*[TYP[t] for t in sig])]
    full = [list(c) for c in itertools.product(*[TYP[t] + EDG[t] for t in sig])]
    tset = {json.dumps(c) for c in typ}
    cross = [c for c in full if json.dumps(c) not in tset]
    return typ, cross


def fuzz_typical(rng, t):
    if t == "int":
        return rng.randint(2, 60)
    if t == "ints":
        return rng.sample(range(2, 60), rng.randint(3, 7))
    return "".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(rng.randint(3, 7)))


def fuzz_wide(rng, t):
    if t == "int":
        return rng.randint(-60, 60)
    if t == "ints":
        return [rng.randint(-5, 9) for _ in range(rng.randint(0, 8))]
    return "".join(rng.choice("abAB 1_") for _ in range(rng.randint(0, 8)))


# ------------------------------------------------------------------------------------------------ sandbox
def _install_audit():
    block = ("socket.", "subprocess.", "os.system", "os.exec", "os.spawn", "os.fork", "os.posix_spawn", "os.remove",
             "os.rename", "os.mkdir", "os.rmdir", "os.chmod", "os.chown", "os.symlink", "os.link", "os.truncate",
             "shutil.", "ctypes.", "urllib.", "http.", "ftplib.", "smtplib.", "webbrowser.", "pty.", "os.kill")

    def hook(ev, args):
        if ev.startswith(block):
            raise RuntimeError("blocked by the hermetic sandbox: " + ev)
        if ev == "open":
            mode = args[1] if len(args) > 1 and isinstance(args[1], str) else "r"
            if any(c in mode for c in "wax+"):
                raise RuntimeError("blocked by the hermetic sandbox: open for writing")
    sys.addaudithook(hook)


def _limits():
    resource.setrlimit(resource.RLIMIT_CPU, (5, 5))
    resource.setrlimit(resource.RLIMIT_FSIZE, (0, 0))


# ------------------------------------------------------------------------------------------------ snippets
def run_one(code, kind, cap):
    out = io.StringIO()
    ns = {"__name__": "__main__"}
    steps = [0]

    def local(frame, event, arg):
        if event == "line":
            steps[0] += 1
            if steps[0] > cap:
                raise _Cap()
        return local

    def glob(frame, event, arg):
        return local if frame.f_code.co_filename == "<snippet>" else None

    res = {"s": "ok", "out": "", "exc": "", "steps": 0}
    try:
        obj = compile(code, "<snippet>", "exec")
        _arm(JOB_SECONDS)
        sys.settrace(glob)
        try:
            with contextlib.redirect_stdout(out):
                exec(obj, ns)
        finally:
            sys.settrace(None)
            _disarm()
        if kind == "result":
            if "result" not in ns:
                res = {"s": "exc", "out": "", "exc": "NameError", "steps": steps[0]}
            else:
                res["out"] = repr(ns["result"])[:400]
        else:
            res["out"] = out.getvalue()[:400]
    except _Cap:
        res["s"] = "cap"
    except _Timeout:
        raise EnvError("snippet wall-clock timeout")
    except BaseException as e:  # noqa: BLE001  (SystemExit, KeyboardInterrupt and every Exception end the snippet)
        name = type(e).__name__
        res["s"] = "exc" if name in ALLOWED_EXC else "other"
        res["exc"] = name
    res["steps"] = steps[0]
    return res


def do_snippets(job):
    return {"results": {j["id"]: run_one(j["code"], j["kind"], min(job.get("cap", LINE_CAP_HARD), LINE_CAP_HARD))
                        for j in job["jobs"]}}


# ------------------------------------------------------------------------------------------------ equivalence
def outcome(fn, case):
    args = [list(a) if isinstance(a, list) else a for a in case]
    try:
        _arm(CALL_SECONDS)
        try:
            r = fn(*args)
        finally:
            _disarm()
        return ("v", repr(r), repr(args))
    except _Timeout:
        raise EnvError("call wall-clock timeout")
    except BaseException as e:  # noqa: BLE001
        return ("e", type(e).__name__)


COND = {"POP_JUMP_IF_FALSE", "POP_JUMP_IF_TRUE", "POP_JUMP_IF_NONE", "POP_JUMP_IF_NOT_NONE", "FOR_ITER"}


def code_tree(code):
    out, stack = [], [code]
    while stack:
        c = stack.pop()
        out.append(c)
        stack += [k for k in c.co_consts if hasattr(k, "co_code")]
    return out


def make_sites(root):
    import dis
    sites = {}
    for c in code_tree(root):
        ins = list(dis.get_instructions(c))
        for i, x in enumerate(ins[:-1]):
            if x.opname in COND:
                sites[(c, x.offset)] = {"fall": ins[i + 1].offset, "f": 0, "j": 0}
    return sites


def coverage(fn_f, fn_g, cases, nsF, nsG):
    sites = {}
    sf, sg = make_sites(fn_f.__code__), make_sites(fn_g.__code__)
    sites.update(sf)
    sites.update(sg)
    watch = {k[0] for k in sites}
    last = {}

    def local(frame, event, arg):
        if event == "opcode":
            fid = id(frame)
            prev = last.get(fid)
            off = frame.f_lasti
            if prev is not None:
                s = sites.get((frame.f_code, prev))
                if s is not None:
                    if off == s["fall"]:
                        s["f"] = 1
                    else:
                        s["j"] = 1
            last[fid] = off
        elif event == "return":
            last.pop(id(frame), None)
        return local

    def glob(frame, event, arg):
        if frame.f_code in watch:
            frame.f_trace = local          # 3.12: opcode events need f_trace set explicitly, before f_trace_opcodes
            frame.f_trace_opcodes = True
            return local
        return None

    # CPython 3.12 delivers opcode events only from the SECOND traced execution of a code object on: the first pass
    # warms every code object (nested lambdas and generator expressions included), the second pass is measured
    for pass_no in (0, 1):
        for s in sites.values():
            s["f"] = s["j"] = 0
        last.clear()
        sys.settrace(glob)
        try:
            for c in cases:
                outcome(fn_f, c)
                outcome(fn_g, c)
        finally:
            sys.settrace(None)

    def frac(s):
        tot = 2 * len(s)
        hit = sum(sites[k]["f"] + sites[k]["j"] for k in s)
        return [hit, tot]
    return {"f": frac(sf), "g": frac(sg)}


def do_equiv(job):
    nsF, nsG = {"__name__": "pair"}, {"__name__": "pair"}
    exec(compile(job["f"], "<f>", "exec"), nsF)
    exec(compile(job["g"], "<g>", "exec"), nsG)
    f, g = nsF["f"], nsG["g"]
    sig = job["sig"]
    typ, cross = grids(sig)
    diff = lambda c: outcome(f, c) != outcome(g, c)  # noqa: E731
    res = {"n_typ": len(typ), "n_cross": len(cross), "typ_diff": 0, "witness_typ": None, "cross_diff": 0,
           "witness_edge": None, "timeouts": 0, "typ_fuzz_n": 0, "typ_fuzz_diff": 0, "fuzz_n": 0, "fuzz_diff": 0,
           "witness_fuzz": None, "cov": None, "stage": "typ"}
    for c in typ:
        if diff(c):
            res["typ_diff"] += 1
            if res["witness_typ"] is None:
                res["witness_typ"] = c
    if res["typ_diff"] / len(typ) >= 0.10:
        return res
    if res["typ_diff"]:
        res["stage"] = "ambiguous_typ"
        return res
    res["stage"] = "cross"
    for c in cross:
        a, b = outcome(f, c), outcome(g, c)
        if a != b:
            res["cross_diff"] += 1
            if res["witness_edge"] is None:
                res["witness_edge"] = c
        if a == ("t",) or b == ("t",):
            res["timeouts"] += 1
    import random
    rng = random.Random(job["seed"])
    n_typ_fuzz = job["fuzz"] // 2
    res["stage"] = "fuzz"
    suite = []
    for i in range(job["fuzz"]):
        t = i < n_typ_fuzz
        c = [(fuzz_typical if t else fuzz_wide)(rng, s) for s in sig]
        if len(suite) < 1000:
            suite.append(c)
        a, b = outcome(f, c), outcome(g, c)
        res["fuzz_n"] += 1
        if t:
            res["typ_fuzz_n"] += 1
        if a != b:
            res["fuzz_diff"] += 1
            if t:
                res["typ_fuzz_diff"] += 1
            if res["witness_fuzz"] is None:
                res["witness_fuzz"] = c
        if a == ("t",) or b == ("t",):
            res["timeouts"] += 1
        if res["cross_diff"] and t and res["typ_fuzz_diff"]:
            break
    if res["cross_diff"] == 0 and res["fuzz_diff"] == 0:
        res["stage"] = "coverage"
        res["cov"] = coverage(f, g, typ + cross + suite, nsF, nsG)
    else:
        res["stage"] = "done"
    return res


def main():
    job = json.loads(sys.stdin.read())
    _limits()
    signal.signal(signal.SIGALRM, _on_alarm)
    _install_audit()
    meta = {"py": list(sys.version_info[:3]), "hashseed": os.environ.get("PYTHONHASHSEED"), "hash_probe": hash("t42")}
    try:
        out = do_snippets(job) if job["mode"] == "snippets" else {"equiv": do_equiv(job)}
    except (EnvError, _Timeout) as e:                      # any wall-clock timeout that reaches here is an environment event
        for _ in range(20):                                # a stray second alarm must not turn exit 97 into a crash
            try:
                signal.signal(signal.SIGALRM, signal.SIG_IGN)
                signal.setitimer(signal.ITIMER_REAL, 0)
                sys.stderr.write(f"T42-ENV: {type(e).__name__} {e}\n")
                break
            except BaseException:  # noqa: BLE001
                continue
        os._exit(97)
    out["meta"] = meta
    sys.stdout.write(json.dumps(out))


if __name__ == "__main__":
    main()

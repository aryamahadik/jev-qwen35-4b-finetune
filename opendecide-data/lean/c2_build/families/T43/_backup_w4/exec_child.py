"""families/T43/exec_child.py: the hermetic child that executes T43 programs (solver A, execution side).

Started by executor.py as   python -S -s -B -P exec_child.py   with PYTHONHASHSEED=0, an empty temp dir as cwd, a
minimal environment and a 5 s kill from the parent. RLIMIT_CPU / RLIMIT_FSIZE are set here; an audit hook refuses
sockets, subprocesses and any file opened for writing. Reads one JSON job list on stdin, writes one JSON result.

  job "pair"   {"a": src, "b": src, "calls": [expr]}  -> per call [outcome_a, outcome_b]; outcome = ["v", repr] | ["e", Class] | ["t"]
  job "judge"  {"orig": src, "fns": [{"name", "types"}], "cands": [{"id", "src"}], "tests": [[call, expected_repr]],
                "seed": n, "nseed": n}
               per candidate: tests ("p" | "f:<got repr>" | "e:<Class>" each), grid_diff / grid_n and seeded_diff / seeded_n
               against the ORIGINAL (outcome = repr of the value plus repr of the arguments afterwards, or the exception
               class), per-function grid diffs, slow flag.
Nothing here imports any T43 module: solver A is CPython itself.
"""
import copy
import itertools
import json
import random
import resource
import signal
import sys

CALL_SECONDS = 0.05
MAX_TIMEOUTS = 3

INT0 = [-5, -1, 0, 1, 2, 3, 5, 8, 12, 100]
INTK = [-1, 2, 4, 9]
INTS = [[], [0], [5], [-3], [2, 5], [5, 2], [3, 3], [1, 1, 2], [4, -1, 2], [2, 3, 5], [8, 7, 3, 2], [3, 0, 3, 9],
        [2, 5, 2, 5], [7, 2, 8, 3, 5]]
STRS = ["", "a", "ab", "Ab", " x", "x ", "a1", "aa", "stone", "plant", "house", "ab ba"]


class _Timeout(BaseException):
    pass


def _on_alarm(signum, frame):
    raise _Timeout()


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


def grid(types):
    cols = []
    for pos, t in enumerate(types):
        if t == "int":
            cols.append(INT0 if pos == 0 else INTK)
        elif t == "ints":
            cols.append(INTS)
        else:
            cols.append(STRS)
    return [list(c) for c in itertools.product(*cols)]


def seeded(types, rng, n):
    out = []
    for _ in range(n):
        case = []
        for pos, t in enumerate(types):
            if t == "int":
                case.append(rng.randint(-20, 60) if pos == 0 else rng.randint(-3, 12))
            elif t == "ints":
                case.append([rng.randint(-5, 12) for _ in range(rng.randint(0, 8))])
            else:
                case.append("".join(rng.choice("abcAB 1") for _ in range(rng.randint(0, 8))))
        out.append(case)
    return out


def load(src):
    ns = {"__name__": "__t43__"}
    exec(compile(src, "<t43>", "exec"), ns)
    return ns


def guarded(fn):
    """Run fn() with the per-call wall cap: ("v", result) | ("e", Class) | ("t",)."""
    signal.setitimer(signal.ITIMER_REAL, CALL_SECONDS)
    try:
        return ("v", fn())
    except _Timeout:
        return ("t",)
    except RecursionError:
        return ("e", "RecursionError")
    except Exception as e:  # noqa: BLE001
        return ("e", type(e).__name__)
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)


def outcome(ns, name, case):
    f = ns.get(name)
    if f is None:
        return ["x", "missing"]
    args = copy.deepcopy(case)
    r = guarded(lambda: f(*args))
    if r[0] == "v":
        return ["v", repr(r[1]), repr(args)]
    return list(r)


def eval_call(ns, expr):
    r = guarded(lambda: eval(expr, ns))
    return ["v", repr(r[1])] if r[0] == "v" else list(r)


def job_pair(j):
    na, nb = load(j["a"]), load(j["b"])
    return [[eval_call(na, c), eval_call(nb, c)] for c in j["calls"]]


def segments(src):
    import ast
    return {n.name: ast.get_source_segment(src, n) for n in ast.parse(src).body if isinstance(n, ast.FunctionDef)}


def job_judge(j):
    orig = load(j["orig"])
    fns_all = j["fns"]
    fns = fns_all
    seg_o = segments(j["orig"])
    cases = {}
    for f in fns:
        rng = random.Random(f"{j['seed']}|{f['name']}")
        cases[f["name"]] = (grid(f["types"]), seeded(f["types"], rng, j["nseed"]))
    base = {}
    for f in fns:
        g, s = cases[f["name"]]
        base[f["name"]] = ([outcome(orig, f["name"], c) for c in g], [outcome(orig, f["name"], c) for c in s])
    res = []
    for cand in j["cands"]:
        out = {"id": cand["id"], "load": "ok", "tests": [], "grid_diff": 0, "grid_n": 0, "seeded_diff": 0, "seeded_n": 0,
               "fn_diff": {}, "witness": None, "slow": False}
        try:
            ns = load(cand["src"])
        except BaseException as e:  # noqa: BLE001
            out["load"] = "err:" + type(e).__name__
            res.append(out)
            continue
        for call, exp in j["tests"]:
            r = eval_call(ns, call)
            out["tests"].append("p" if r[0] == "v" and r[1] == exp else ("f:" + r[1] if r[0] == "v" else
                                                                         "e:" + (r[1] if len(r) > 1 else "timeout")))
        timeouts = 0
        seg_c = segments(cand["src"])
        # only the functions whose text changed and the entry (it calls the others) can differ from the original
        for f in [f for f in fns if f.get("entry") or seg_c.get(f["name"]) != seg_o.get(f["name"])]:
            g, s = cases[f["name"]]
            bg, bs = base[f["name"]]
            fd = 0
            for kind, cs, bo in (("grid", g, bg), ("seeded", s, bs)):
                for c, o in zip(cs, bo):
                    if timeouts >= MAX_TIMEOUTS:
                        break
                    r = outcome(ns, f["name"], c)
                    if r[0] == "t":
                        timeouts += 1
                    out[kind + "_n"] += 1
                    if r != o:
                        out[kind + "_diff"] += 1
                        if kind == "grid":
                            fd += 1
                            if out["witness"] is None:
                                out["witness"] = [f["name"], c]
            if fd:
                out["fn_diff"][f["name"]] = fd
        out["slow"] = timeouts >= MAX_TIMEOUTS
        res.append(out)
    return res


def main():
    _install_audit()
    resource.setrlimit(resource.RLIMIT_CPU, (5, 5))
    resource.setrlimit(resource.RLIMIT_FSIZE, (0, 0))
    signal.signal(signal.SIGALRM, _on_alarm)
    sys.setrecursionlimit(400)
    job = json.loads(sys.stdin.read())
    results = []
    for j in job["jobs"]:
        try:
            results.append(job_pair(j) if j["op"] == "pair" else job_judge(j))
        except BaseException as e:  # noqa: BLE001
            results.append({"error": type(e).__name__ + ": " + str(e)[:120]})
    json.dump({"meta": {"py": list(sys.version_info[:3]), "hashseed": __import__("os").environ.get("PYTHONHASHSEED")}, "results": results}, sys.stdout)


main()

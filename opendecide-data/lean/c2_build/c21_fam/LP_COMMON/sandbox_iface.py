"""Interface between the L-P generators and the executor (od-sbx1). Nothing here runs generated code locally.

  * request builders produce {"row_id", "lang", "files", "argv", "kind", "repeats", "purpose", "sim"} dicts; `to_job_line` makes the exact JSON line that
    `od-sbx run-batch --jobs` reads (same shape as L-C's `render.job_line`);
  * `Executor.run(requests)` returns one result per request. Implementations:
        SimExecutor        unit tests / dry run: predicts the sandbox report for a RENDERED Python file with PyEval (a safe AST interpreter, no exec);
                           other languages raise `LanguagePending` (no non-Python row before the L-0 image record, as in L-C's README item 7);
        RecordedExecutor   replays results from a jsonl file of recorded executor output;
        JobFileExecutor    writes the jobs jsonl for the real executor and later reads its output (two-phase);
        CollectingExecutor records requests and raises `NeedsResults` (pass 1 of the two-phase flow);
  * `parse_*` helpers turn executor stdout into the normalised witness forms Solver A labels from.
Result record: {"row_id", "deterministic", "exit_code", "stdout", "states", "runs", "image"}. WITNESS RULE: 3 identical runs (`runs >= 3` and `deterministic`).
"""
import base64
import json

from . import pyeval

MARK = "@@OD@@"
TOOLCHAIN = {"python": "python", "javascript": "node", "typescript": "node", "go": "go", "bash": "sh"}
WITNESS_RUNS = 3

PYTESTS_RUNNER = """import importlib, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
mod = importlib.import_module(sys.argv[1])
res = {}
for name in sorted(dir(mod)):
    if name.startswith('test_') and callable(getattr(mod, name)):
        try:
            getattr(mod, name)()
            res[name] = 'pass'
        except AssertionError:
            res[name] = 'fail:AssertionError'
        except BaseException as e:
            res[name] = 'error:' + type(e).__name__
print('@@OD@@' + json.dumps(res, separators=(',', ':'), sort_keys=True))
"""

CALLS_RUNNER = """import importlib, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
mod = importlib.import_module(sys.argv[1])
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'od_calls.json')) as f:
    calls = json.load(f)
out = []
for fn, args, kwargs in calls:
    try:
        out.append(['ok', getattr(mod, fn)(*args, **kwargs)])
    except BaseException as e:
        out.append(['exc', type(e).__name__, str(e)])
print('@@OD@@' + json.dumps(out, separators=(',', ':'), sort_keys=True))
"""


class LanguagePending(RuntimeError):
    """The language has no sandbox path yet (pins pending from the L-0 image record)."""


class NeedsResults(RuntimeError):
    """CollectingExecutor: the requests were recorded; run od-sbx and replay with RecordedExecutor."""


class WitnessError(RuntimeError):
    pass


# ---- requests ---------------------------------------------------------------------------------------------------------------------------
def tests_request(row_id, files, test_path, lang="python", repeats=WITNESS_RUNS, purpose="tests"):
    """Run every test_* function of one Python test file against the module files in `files` (stems importable from the same directory)."""
    fl = dict(files)
    fl["od_run_tests.py"] = PYTESTS_RUNNER
    return {"row_id": row_id, "lang": lang, "files": fl, "argv": ["python", "-I", "od_run_tests.py", test_path[:-3]], "kind": "run", "repeats": repeats,
            "purpose": purpose, "sim": {"op": "tests", "files": dict(files), "test": test_path}}


def calls_request(row_id, files, module, calls, lang="python", repeats=WITNESS_RUNS, purpose="calls"):
    """Observables of a list of calls [(fn, args, kwargs)] (JSON-able arguments) on a fresh import of `module`."""
    fl = dict(files)
    fl["od_run_calls.py"] = CALLS_RUNNER
    fl["od_calls.json"] = json.dumps([[f, list(a), dict(k)] for f, a, k in calls], sort_keys=True)
    return {"row_id": row_id, "lang": lang, "files": fl, "argv": ["python", "-I", "od_run_calls.py", module], "kind": "run", "repeats": repeats, "purpose": purpose,
            "sim": {"op": "calls", "files": dict(files), "module": module, "calls": [(f, list(a), dict(k)) for f, a, k in calls]}}


def to_job_line(req):
    return {"row_id": req["row_id"], "toolchain": TOOLCHAIN[req["lang"]], "kind": req["kind"], "will_this_test_fail": req["repeats"] >= 3, "repeats": req["repeats"],
            "files": {k: base64.b64encode(v.encode("utf-8")).decode("ascii") for k, v in sorted(req["files"].items())}, "argv": list(req["argv"]),
            "report": None, "expected_ids": None}


# ---- executors ----------------------------------------------------------------------------------------------------------------------------
class Executor(object):
    def run(self, requests):                                      # pragma: no cover - interface
        raise NotImplementedError


def _jsonable(v):
    return json.loads(json.dumps(v))


class SimExecutor(Executor):
    """Predicts the sandbox report with PyEval. `faults` maps row_id -> callable(result) -> result (tests inject nondeterminism / wrong outcomes)."""

    def __init__(self, faults=None, nondeterministic=()):
        self.faults, self.nondet, self.calls = faults or {}, set(nondeterministic), 0

    def run(self, requests):
        out = []
        for rq in requests:
            self.calls += 1
            if rq["lang"] != "python":
                raise LanguagePending("no sandbox path for %s yet (L-0 image record pending)" % rq["lang"])
            s = rq["sim"]
            if s["op"] == "tests":
                try:
                    states = pyeval.run_tests(s["files"], s["test"])
                    code = 0 if all(v == "pass" for v in states.values()) else 1
                except pyeval.PyEvalError as e:
                    states, code = {"__pyeval__": "unsupported:" + str(e)[:60]}, 2
                res = {"row_id": rq["row_id"], "deterministic": True, "exit_code": code, "stdout": MARK + json.dumps(states, separators=(",", ":"), sort_keys=True) + "\n",
                       "states": states, "runs": rq["repeats"], "image": "sim"}
            else:
                try:
                    obs = [_jsonable(list(o)) for o in pyeval.call_all(s["files"], s["module"], s["calls"])]
                    code = 0
                except pyeval.PyEvalError as e:
                    obs, code = [["unsupported", str(e)[:60]]], 2
                res = {"row_id": rq["row_id"], "deterministic": True, "exit_code": code, "stdout": MARK + json.dumps(obs, separators=(",", ":"), sort_keys=True) + "\n",
                       "states": None, "runs": rq["repeats"], "image": "sim"}
            if rq["row_id"] in self.faults:
                res = self.faults[rq["row_id"]](res)
            if rq["row_id"] in self.nondet:
                res = dict(res, deterministic=False)
            out.append(res)
        return out


class RecordedExecutor(Executor):
    def __init__(self, path=None, by_row=None):
        self.by_row = dict(by_row or {})
        if path:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    d = json.loads(line)
                    self.by_row[d["row_id"]] = d

    def run(self, requests):
        return [self.by_row[r["row_id"]] for r in requests]


class JobFileExecutor(Executor):
    """Two-phase: write_jobs(), run od-sbx on od-sbx1, then read_results()."""

    def __init__(self, jobs_path):
        self.jobs_path = jobs_path

    def write_jobs(self, requests):
        with open(self.jobs_path, "w", encoding="utf-8") as f:
            for r in requests:
                f.write(json.dumps(to_job_line(r), sort_keys=True) + "\n")
        return len(requests)

    def run(self, requests):
        raise RuntimeError("JobFileExecutor is two-phase: write_jobs(), run od-sbx on od-sbx1, then read_results()")

    @staticmethod
    def read_results(out_path):
        res = {}
        with open(out_path, "r", encoding="utf-8") as f:
            for line in f:
                d = json.loads(line)
                runs = d.get("runs", [])
                res[d["row_id"]] = {"row_id": d["row_id"], "deterministic": bool(d.get("deterministic")) and not d.get("dropped"), "runs": len(runs),
                                    "exit_code": runs[0]["exit_code"] if runs else None, "stdout": runs[0]["stdout"] if runs else "", "states": d.get("states"),
                                    "image": d.get("image")}
        return res


class CollectingExecutor(Executor):
    def __init__(self):
        self.requests = []

    def run(self, requests):
        self.requests.extend(requests)
        raise NeedsResults("%d request(s) recorded" % len(requests))


# ---- parsing -----------------------------------------------------------------------------------------------------------------------------
def parse_marker(stdout):
    for line in stdout.splitlines():
        k = line.find(MARK)
        if k >= 0:
            return json.loads(line[k + len(MARK):])
    return None


def witness_ok(res):
    """3 identical runs and a clean exit (a failing test exits 1: that is a witness too, see `states`)."""
    return bool(res.get("deterministic")) and res.get("runs", 0) >= WITNESS_RUNS and res.get("exit_code") in (0, 1)


def test_states(res):
    st = res.get("states")
    return st if st is not None else (parse_marker(res.get("stdout", "")) or {})


def all_pass(states):
    return bool(states) and all(v == "pass" for v in states.values())

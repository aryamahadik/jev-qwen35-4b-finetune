"""Interface between Solver A and the sandbox executor (od-sbx1). Nothing here runs generated code.

  * request builders produce {"row_id", "lang", "files", "argv", "kind", ...} dicts -> `to_job_line` makes the exact
    JSON line `od-sbx run-batch --jobs` reads (render.job_line);
  * `Executor.run(requests)` returns one result per request. Three implementations:
        SimExecutor      unit tests / dry-run: predicts stdout from the IR interpreter (spec expectation), optionally
                         with injected faults. It never evaluates rendered source.
        RecordedExecutor replays results from a jsonl file of recorded executor output.
        JobFileExecutor  writes a jobs jsonl for the real executor and later reads its output + manifest.
  * `parse_*` helpers turn executor stdout/report bytes into the normalised witness forms Solver A labels from.
"""
import json
import xml.etree.ElementTree as ET

from . import ir as I
from . import render as R
from . import render_base as B
from . import interp as X
from . import domain as D
from . import domdriver as DD
from .suites import step_ok

MARK = R.MARK
MAX_OBSERVABLE_CHARS = 190     # the executor result record keeps a 200-character stdout preview (hash covers all)


# ----------------------------------------------------------------------------------------------- requests
def driver_request(row_id, mod, lang, plan, instrument_steps=False, module_files=None):
    files = R.render_module(mod, lang, instrument=instrument_steps)
    if module_files is not None and not instrument_steps:
        files = _module_files(mod, lang, module_files)
    if instrument_steps:
        dfiles, argv = render_steps_driver(mod, lang, plan)
    else:
        dfiles, argv = R.render_driver(mod, lang, plan)
    files = dict(files)
    files.update(dfiles)
    return {"row_id": row_id, "lang": lang, "files": files, "argv": argv, "kind": "run", "repeats": 3,
            "purpose": "steps" if instrument_steps else "witness", "sim": {"mod": mod, "plan": plan}}


def _module_files(mod, lang, module_files=None):
    """Rendered module files; `module_files` (text of the exact tree being tested, e.g. a patched tree with a comment)
    replaces the rendered .py/.js/... files but keeps toolchain files (go.mod, vendor/modules.txt)."""
    files = dict(R.render_module(mod, lang))
    if module_files is not None:
        keep = {k: v for k, v in files.items() if k in ("go.mod", "vendor/modules.txt")}
        files = dict(keep, **module_files)
    return files


def suite_request(row_id, mod, lang, tests, extra_files=None, suites=None, repeats=2, drop_files=(), module_files=None):
    """tests: {path: text}. suites: [(path, suite-dict)] used only by SimExecutor."""
    files = _module_files(mod, lang, module_files)
    for d in drop_files:
        files.pop(d, None)
    files.update(tests)
    files.update(extra_files or {})
    return {"row_id": row_id, "lang": lang, "files": files, "argv": R.suite_argv(lang, sorted(tests)),
            "kind": "suite", "repeats": repeats, "report": R.suite_report(lang),
            "sim": {"mod": mod, "suites": suites or []}}


def domain_request(row_id, mod, lang, points, snapshot=None, module_files=None):
    """Run every point of a declared domain (host-enumerated, unrolled driver). Equality of two programs = equal stdout."""
    files = _module_files(mod, lang, module_files)
    dfiles, argv = DD.render(mod, lang, points, snapshot)
    files.update(dfiles)
    return {"row_id": row_id, "lang": lang, "files": files, "argv": argv, "kind": "run", "repeats": 3, "purpose": "domain",
            "sim": {"mod": mod, "points": points, "snapshot": snapshot}}


PYTESTS_RUNNER = """import importlib, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
mod = importlib.import_module(sys.argv[1])
res = {}
for name in sorted(dir(mod)):
    if name.startswith('test_') and callable(getattr(mod, name)):
        try:
            getattr(mod, name)()
            res[name] = 'pass'
        except BaseException as e:
            res[name] = 'fail:' + type(e).__name__
print('@@OD@@' + json.dumps(res, separators=(',', ':'), sort_keys=True))
"""


def pytests_request(row_id, mod, lang, test_path, test_text, suite):
    """T42c Python tests run under `python -I` through a tiny runner (the manifest lists runner.python_isolated only)."""
    files = dict(R.render_module(mod, lang))
    files[test_path] = test_text
    files["od_run_tests.py"] = PYTESTS_RUNNER
    stem = test_path[:-3]
    return {"row_id": row_id, "lang": lang, "files": files, "argv": ["python", "-I", "od_run_tests.py", stem], "kind": "run",
            "repeats": 3, "purpose": "pytests", "sim": {"mod": mod, "suites": [(test_path, suite)]}}


def to_job_line(req):
    return R.job_line(req["row_id"], req["lang"], req["files"], req["argv"], kind=req["kind"], repeats=req["repeats"],
                      report=req.get("report"), expected_ids=req.get("expected_ids"))


# ----------------------------------------------------------------------------------------------- steps driver
def render_steps_driver(mod, lang, plan, name="od_steps"):
    """Instrumented twin: same calls as the witness driver, then print the executed-statement counter."""
    files, argv = R.render_driver(mod, lang, dict(plan, mode="all", snapshot=plan.get("snapshot")), name)
    k, text = next(iter(files.items()))
    if lang == "python":
        text = text.replace("emit({'res': res})", "emit({'res': res})\nimport odc\nprint('@@ODN@@' + str(odc.n))")
        text = text.replace("\n\ndef emit", "\n\ndef emit", 1)
        return {k: text}, argv
    if lang in ("javascript", "typescript"):
        text = text.replace("emit({ res });", "emit({ res });\nconsole.log('@@ODN@@' + (globalThis.__odn || 0));")
        return {k: text}, argv
    if lang == "go":
        text = text.replace('\tfmt.Println("%s" + `{"res":[` + strings.Join(res, ",") + `]}`)' % MARK,
                            '\tfmt.Println("%s" + `{"res":[` + strings.Join(res, ",") + `]}`)\n\tfmt.Println("@@ODN@@" + strconv.Itoa(odN))' % MARK)
        return {k: text}, argv
    # bash: xtrace to fd 9, count lines that were executed inside a function
    lines = text.split("\n")
    out = [lines[0]]
    out += ["exec 9>/work/od_trace.txt", "BASH_XTRACEFD=9", "PS4='+OD:${FUNCNAME[0]}:'", "set -x"]
    out += lines[1:]
    out += ["set +x", "exec 9>&-", "mapfile -t tl < /work/od_trace.txt", "n=0",
            'for l in "${tl[@]}"; do [[ $l == +OD:?*:* ]] && n=$((n+1)); done', 'echo "@@ODN@@$n"']
    return {k: "\n".join(out) + "\n"}, argv


# ----------------------------------------------------------------------------------------------- python line-event twin
def render_trace_driver_python(mod, plan, name="od_trace"):
    """Python line-event step counter (sys.settrace, module files only): the reference the counter-insertion twin is checked
    against (T42c: agree within 10% on 100 programs before any row)."""
    files, argv = R.render_driver(mod, "python", dict(plan, mode="all", snapshot=plan.get("snapshot")), name)
    k, text = next(iter(files.items()))
    pre = ("import sys as _s, os as _o\n_FILES = set(%r)\n_n = [0]\n"
           "def _tr(frame, event, arg):\n    if _o.path.basename(frame.f_code.co_filename) in _FILES:\n"
           "        if event == 'line':\n            _n[0] += 1\n        return _tr\n    return None\n" % sorted(m + ".py" for m in mod["files"]))
    text = pre + text
    import re as _re
    if "\nobj = " in text:                                   # trace the calls, not the constructor
        text = _re.sub(r"(\nobj = [^\n]+\n)", lambda m: m.group(1) + "_s.settrace(_tr)\n", text, count=1)
    else:
        text = text.replace("res = []", "_s.settrace(_tr)\nres = []", 1)
    text = text.replace("emit({'res': res})", "_s.settrace(None)\nemit({'res': res})\nprint('@@ODL@@' + str(_n[0]))")
    return {k: text}, argv


def trace_request(row_id, mod, plan):
    files = R.render_module(mod, "python")
    dfiles, argv = render_trace_driver_python(mod, plan)
    files = dict(files)
    files.update(dfiles)
    return {"row_id": row_id, "lang": "python", "files": files, "argv": argv, "kind": "run", "repeats": 2, "purpose": "trace",
            "sim": {"mod": mod, "plan": dict(plan, mode="all")}}


def step_agreement(pairs, tol=0.10, share_needed=0.90):
    """pairs: [(counter_insertion_steps, line_event_steps)] for >= 100 Python programs. Pass iff the mean relative difference
    is <= tol and >= 90% of the programs are within tol (one absolute step of slack for tiny counts)."""
    rel, within = [], 0
    for a, b in pairs:
        m = max(a, b, 1)
        d = abs(a - b) / m
        rel.append(d)
        within += (d <= tol) or abs(a - b) <= 1
    n = len(pairs)
    mean = sum(rel) / n if n else 1.0
    return {"n": n, "mean_rel_diff": round(mean, 4), "share_within": round(within / n, 4) if n else 0.0,
            "pass": bool(n >= 100 and mean <= tol and within / n >= share_needed)}


# ----------------------------------------------------------------------------------------------- parsing
def parse_driver_stdout(stdout):
    """-> (observable json | None, steps | None)."""
    obs, steps = None, None
    for line in stdout.splitlines():
        if line.startswith("@@ODL@@"):
            try:
                steps = int(line[len("@@ODL@@"):])
            except ValueError:
                pass
        elif line.startswith("@@ODN@@"):
            try:
                steps = int(line[len("@@ODN@@"):])
            except ValueError:
                pass
        elif MARK in line:
            obs = json.loads(line[line.find(MARK) + len(MARK):])
    return obs, steps


def parse_junit(data):
    if b"<!DOCTYPE" in data or b"<!ENTITY" in data:
        raise ValueError("DOCTYPE/ENTITY in report")
    root = ET.fromstring(data)
    out = {}
    for tc in root.iter("testcase"):
        tid = "%s::%s" % (tc.get("classname", ""), tc.get("name", ""))
        if tid in out:
            raise ValueError("duplicate test id")
        kids = {c.tag for c in tc}
        out[tid] = "failed" if "failure" in kids else "error" if "error" in kids else "skipped" if "skipped" in kids else "passed"
    return out


def parse_go_json(data):
    out = {}
    for line in data.decode("utf-8", "replace").splitlines():
        ev = json.loads(line)
        if ev.get("Test") and ev.get("Action") in ("pass", "fail", "skip"):
            out["%s/%s" % (ev.get("Package", ""), ev["Test"])] = {"pass": "passed", "fail": "failed", "skip": "skipped"}[ev["Action"]]
    return out


def parse_tap(stdout):
    out = {}
    for line in stdout.splitlines():
        if line.startswith("ok "):
            out[line[3:].strip()] = "passed"
        elif line.startswith("not ok "):
            out[line[7:].strip()] = "failed"
    return out


def suite_states(lang, stdout, report):
    if lang == "bash":
        return parse_tap(stdout)
    if lang == "go":
        return parse_go_json(stdout.encode() if isinstance(stdout, str) else stdout)
    return parse_junit(report or b"")


# ----------------------------------------------------------------------------------------------- executors
class Executor:
    def run(self, requests):                      # pragma: no cover - interface
        raise NotImplementedError


def _stable(results):
    return len({json.dumps(r, sort_keys=True) for r in results}) == 1


class SimExecutor(Executor):
    """Predicts the witness from the IR interpreter. `faults` maps row_id -> callable(result)->result for tests."""

    def __init__(self, faults=None, nondeterministic=()):
        self.faults = faults or {}
        self.nondet = set(nondeterministic)
        self.calls = 0

    def run(self, requests):
        out = []
        for rq in requests:
            self.calls += 1
            if rq["kind"] == "run" and rq["purpose"] == "domain":
                res = self._domain(rq)
            elif rq["kind"] == "run" and rq["purpose"] == "pytests":
                res = self._pytests(rq)
            elif rq["kind"] == "run":
                res = self._driver(rq)
            else:
                res = self._suite(rq)
            if "sim_effect" in rq:                       # spec-level effect supplied by the family (T56g text-level hacks)
                res = dict(res, **rq["sim_effect"])
            if rq["row_id"] in self.faults:
                res = self.faults[rq["row_id"]](res)
            if rq["row_id"] in self.nondet:
                res = dict(res, deterministic=False)
            out.append(res)
        return out

    def _driver(self, rq):
        mod, lang, plan = rq["sim"]["mod"], rq["lang"], rq["sim"]["plan"]
        it = X.Interp(mod, lang)
        outs = []
        calls = plan["calls"]
        for c in calls[:-1] if plan["mode"] == "last" else calls:
            outs.append(it.call(c["fn"], c["args"]))
        if plan["mode"] == "last":
            if any(o[0] == "exc" for o in outs):
                # the real driver runs the earlier calls bare: an escaping exception ends the process before anything is emitted
                return {"row_id": rq["row_id"], "deterministic": True, "exit_code": 1, "stdout": "", "events": [], "runs": rq["repeats"]}
            outs = [it.call(calls[-1]["fn"], calls[-1]["args"])]
            obs = R.observable_of(mod, lang, outs[0])
        else:
            if plan.get("snapshot"):
                outs.append(it.call(plan["snapshot"], []))
            obs = {"res": [R.observable_of(mod, lang, o) for o in outs]}
        stdout = MARK + json.dumps(obs, separators=(",", ":"), sort_keys=True) + "\n"
        if rq["purpose"] == "steps":
            stdout += "@@ODN@@%d\n" % it.steps
        if rq["purpose"] == "trace":
            stdout += "@@ODL@@%d\n" % it.steps
        events = sorted(it.events)
        return {"row_id": rq["row_id"], "deterministic": True, "exit_code": 0, "stdout": stdout, "events": events,
                "runs": rq["repeats"]}

    def _domain(self, rq):
        s = rq["sim"]
        out = DD.expected_stdout(s["mod"], rq["lang"], s["points"], s["snapshot"])
        return {"row_id": rq["row_id"], "deterministic": True, "exit_code": 0, "stdout": out, "events": [], "runs": rq["repeats"]}

    def _pytests(self, rq):
        mod, lang = rq["sim"]["mod"], rq["lang"]
        res = {}
        for path, suite in rq["sim"]["suites"]:
            for case in suite["cases"]:
                it = X.Interp(mod, lang)
                ok = True
                for s in case["steps"]:
                    o = it.call(s["fn"], s["args"])
                    ok = ok and step_ok(s, o)
                res["test_" + case["name"]] = "pass" if ok else "fail:AssertionError"
        stdout = MARK + json.dumps(res, separators=(",", ":"), sort_keys=True) + "\n"
        return {"row_id": rq["row_id"], "deterministic": True, "exit_code": 0, "stdout": stdout, "events": [], "runs": rq["repeats"]}

    def _suite(self, rq):
        mod, lang = rq["sim"]["mod"], rq["lang"]
        states = {}
        for path, suite in rq["sim"]["suites"]:
            for case in suite["cases"]:
                it = X.Interp(mod, lang)
                ok = True
                for s in case["steps"]:
                    o = it.call(s["fn"], s["args"])
                    ok = ok and step_ok(s, o)
                states["%s::%s" % (path, case["name"])] = "passed" if ok else "failed"
        code = 0 if all(v == "passed" for v in states.values()) else 1
        return {"row_id": rq["row_id"], "deterministic": True, "exit_code": code, "states": states, "runs": rq["repeats"],
                "verdict": "PASS" if code == 0 else "FAIL"}


class RecordedExecutor(Executor):
    def __init__(self, path):
        self.by_row = {}
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                d = json.loads(line)
                self.by_row[d["row_id"]] = d

    def run(self, requests):
        return [self.by_row[r["row_id"]] for r in requests]


class JobFileExecutor(Executor):
    """Write the jobs file for `od-sbx run-batch`; results are read back with `read_results` after the batch ran."""

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
                res[d["row_id"]] = {"row_id": d["row_id"], "deterministic": bool(d.get("deterministic")) and not d.get("dropped"),
                                    "runs": len(runs), "exit_code": runs[0]["exit_code"] if runs else None,
                                    "stdout": runs[0]["stdout"] if runs else "",
                                    "stdout_sha256": runs[0].get("stdout_sha256") if runs else None,
                                    "verdict": (d.get("verdict") or {}).get("verdict"),
                                    "states": d.get("states"), "raw": d}
        return res


def case_state_map(states, case_names):
    """Map executor test ids to hidden-suite case names by the LAST path segment (pytest 'test_<case>', node '<case>',
    Go 'Test<Case>', bash 'test_<case>', sim 'path::<case>'). A case with no id, or with two, is reported as 'missing'."""
    import re
    segs = {}
    for k, v in states.items():
        segs.setdefault(re.split(r"::|/| ", k.strip())[-1], []).append(v)
    out = {}
    for c in case_names:
        hits = []
        for form in (c, "test_" + c, "Test" + c.capitalize()):
            hits += segs.get(form, [])
        out[c] = hits[0] if len(hits) == 1 else "missing"
    return out


def observable_len_ok(obs):
    return len(MARK + json.dumps(obs, separators=(",", ":"), sort_keys=True)) <= MAX_OBSERVABLE_CHARS


def outcome_obs(mod, lang, outcome):
    return R.observable_of(mod, lang, outcome)

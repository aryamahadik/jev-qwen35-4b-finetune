"""Program-generated test suites (T57 hidden suites H and visible tests V; T56g held-out suites).

The suites are built BY PROGRAM from the behaviour atoms: every expectation is the REFERENCE module's output (IR
interpreter in the target language's dialect), cases come from the declared typed domains (boundary values taken from the
spec thresholds + pairwise combinations + random points) and, for stateful modules, from call sequences. No LLM writes a
test. Gold-sanity (every case passes on the reference), strength and the differential run are checked in the sandbox by
the family's Solver A; the IR interpreter only provides the spec expectation.
"""
from . import domain as D
from . import ir as I
from . import render as R
from . import sampler as SM
from .interp import Interp


def _case(name, steps, fn, kind):
    return {"name": name, "steps": steps, "fn": fn, "kind": kind}


def _step_from(c, o):
    if o[0] == "ok":
        return {"op": "eq", "fn": c["fn"], "args": c["args"], "expect": o[1]}
    return {"op": "raises", "fn": c["fn"], "args": c["args"], "err": o[1]}


def build_suite(lo, lang, rng, ids, tag, n_cases=18):
    """Cases for every public function of `lo` (the reference). Returns {"cases": [...]}."""
    cases, seen = [], set()
    fns = I.functions(lo)
    pure = [f for f in lo["funcs"] if f["scope"] == "free" and lo["meta"]["fns"].get(f["name"], {}).get("domain")]
    per_fn = max(2, n_cases // max(1, len(pure) + (1 if lo["cls"] else 0)))
    for f in pure:
        spec = lo["meta"]["fns"][f["name"]]
        dom = spec["domain"]
        pts = D.boundary_points(dom, spec["boundaries"], rng, cap=per_fn * 3) + D.sample_points(dom, rng, per_fn * 2)
        got = 0
        for k, pt in enumerate(pts):
            key = (f["name"], I.canon(pt))
            if key in seen:
                continue
            c = {"fn": f["name"], "args": pt}
            it = Interp(lo, lang)
            o = it.call(c["fn"], c["args"])
            if it.events or not SM.explicit_outcome(o):
                continue
            seen.add(key)
            kind = "boundary" if k < per_fn * 3 else "sample"
            cases.append(_case(ids.var("%s.c%d" % (tag, len(cases))), [_step_from(c, o)], f["name"], kind))
            got += 1
            if got >= per_fn:
                break
    seq = (lo["meta"].get("seq") or {})
    if lo["cls"] is not None and seq:
        sd = seq["domain"]
        want = max(3, n_cases // 3)
        tries = 0
        while sum(1 for c in cases if c["kind"] == "sequence") < want and tries < 80:
            tries += 1
            n = rng.randint(2, 4)
            calls = SM.sample_sequence(sd, rng, n, 1)
            it = Interp(lo, lang)
            outs = [it.call(c["fn"], c["args"]) for c in calls]
            snap = it.call(seq["snapshot"], [])
            if it.events or any(not SM.explicit_outcome(o) for o in outs + [snap]):
                continue
            if any(o[0] == "exc" for o in outs[:-1]):
                continue
            key = ("seq", I.canon(calls))
            if key in seen:
                continue
            seen.add(key)
            steps = []
            for k, (c, o) in enumerate(zip(calls, outs)):
                steps.append(_step_from(c, o) if (k == len(calls) - 1 or rng.random() < 0.5) else {"op": "do", "fn": c["fn"], "args": c["args"]})
            steps.append(_step_from({"fn": seq["snapshot"], "args": []}, snap))
            cases.append(_case(ids.var("%s.c%d" % (tag, len(cases))), steps, calls[-1]["fn"], "sequence"))
    return {"cases": cases}


def case_calls(case):
    return [{"fn": s["fn"], "args": s["args"]} for s in case["steps"]]


def case_functions(case):
    return sorted({s["fn"] for s in case["steps"]})


def home_file(lo, case):
    """Index of the source file of the first function the case calls (tests are grouped by it)."""
    return I.functions(lo)[case["steps"][0]["fn"]]["file"]


def split_by_file(lo, suite):
    out = {}
    for c in suite["cases"]:
        out.setdefault(home_file(lo, c), []).append(c)
    return out


def render_suite_files(lo, lang, suite, ids, tag, blocks=None, pairs=None):
    """{path: text} with one test file per home source file. `blocks` receives {case name: case source}; `pairs` receives
    [(path, {"cases": [...]})] (which cases live in which file; SimExecutor needs it)."""
    files = {}
    for fi, cases in sorted(split_by_file(lo, suite).items()):
        stem = ids.module_stem("%s.f%d" % (tag, fi))
        path, text = R.render_tests(lo, lang, {"cases": cases}, stem, blocks=blocks)
        files[path] = text
        if pairs is not None:
            pairs.append((path, {"cases": cases}))
    return files


def step_ok(s, o):
    """Does outcome `o` of step `s` keep the test passing under the REAL runners? eq: the value must match; raises: that
    exception; do: a bare call, so an exception that escapes it fails the test (pytest / node:test / go test / the bash
    `|| return 1` all do). (Build-review fix 18 Oct: the spec used to ignore a raising `do`, so target / pass-to-pass tags and
    TESTSEL distractor neutrality disagreed with every real runner.)"""
    op = s["op"]
    if op == "eq":
        return o == ("ok", s["expect"])
    if op == "raises":
        return o == ("exc", s["err"])
    if op == "do":
        return o[0] != "exc"
    return True


def evaluate(lo, lang, suite):
    """Spec expectation of every case on module `lo`: {case name: True if it passes}. (IR interpreter.)"""
    res = {}
    for c in suite["cases"]:
        it = Interp(lo, lang)
        ok = True
        for s in c["steps"]:
            o = it.call(s["fn"], s["args"])
            if not step_ok(s, o):
                ok = False
        res[c["name"]] = ok
    return res


def differential_points(lo, rng=None, cap=D.MAX_POINTS):
    """Points of the declared domains for the differential run (reference vs candidate): every pure function's whole
    domain (all points, exhaustive when it fits) plus every call sequence of the stateful part, capped at `cap` points
    in total (largest domains are subsampled deterministically)."""
    pts = []
    snap = (lo["meta"].get("seq") or {}).get("snapshot")
    for f in lo["funcs"]:
        if f["scope"] != "free":
            continue
        dom = (lo["meta"]["fns"].get(f["name"]) or {}).get("domain")
        if not dom:
            continue
        for a in D.enumerate_points(dom, limit=10 ** 7):
            pts.append([{"fn": f["name"], "args": a}])
    if lo["cls"] is not None and lo["meta"].get("seq"):
        sd = lo["meta"]["seq"]["domain"]
        sd = {"ops": sd["ops"], "maxlen": min(sd["maxlen"], 3)}
        for s in D.enumerate_sequences(sd, limit=10 ** 7):
            pts.append([{"fn": c["fn"], "args": c["args"]} for c in s])
    if len(pts) > cap:
        step = len(pts) / float(cap)
        pts = [pts[int(k * step)] for k in range(cap)]
    return pts, snap

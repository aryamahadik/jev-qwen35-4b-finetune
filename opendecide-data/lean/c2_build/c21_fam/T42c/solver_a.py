"""T42c SOLVER A: the primary pipeline.

generator emits a row spec  ->  executor runs the witnesses (3 identical runs)  ->  labeller applies the G0-lite rules.
Spec expectations (IR interpreter in the target dialect) are checked against every witness; any difference is a DROP
that is counted by reason (never silent, never relabelled). Nothing here executes generated code: requests go to the
executor (od-sbx1) through LC_COMMON.sandbox_iface.

Witness rules implemented (G0-lite section 2 + Opus ruling (a): the 3-run rule overrides the sandbox default of 2)
  OUT4    value / exception class from the sandbox, THREE byte-identical runs; EXEC-NEARMISS options executed and checked.
  EQV2-YES  registered construction AND an exhaustive run of both programs over the whole declared domain, 3 identical runs
            each, identical outputs. EQV2-NO  a concrete distinguishing input, both programs run on it 3 times, observables
            identical within each program and different across them.
  TFAIL2  THREE runs agree; timeouts and nondeterminism are dropped, never labelled.
  trace-length  from a separate instrumented twin run, never from the witness runs.
"""
import collections
import hashlib

from LC_COMMON import domain as D
from LC_COMMON import ir as I
from LC_COMMON import render as R
from LC_COMMON import sandbox_iface as S
from LC_COMMON import sampler as SM
from LC_COMMON import lint
from LC_COMMON import provenance

from . import config as C
from . import rows as ROWS
from .base import Skip, variant

SOLVER_A_VERSION = "T42c-solver-a-1"


class Drop(Exception):
    def __init__(self, reason, detail=""):
        super().__init__("%s %s" % (reason, detail))
        self.reason = reason
        self.detail = detail


class DropLog:
    def __init__(self):
        self.counts = collections.Counter()
        self.examples = {}
        self.attempted = 0

    def add(self, reason, rid):
        self.counts[reason] += 1
        self.examples.setdefault(reason, []).append(rid)
        self.examples[reason] = self.examples[reason][:5]

    def rate(self):
        return sum(self.counts.values()) / max(1, self.attempted)


def out_id(res):
    return res.get("stdout_sha256") or hashlib.sha256(res.get("stdout", "").encode("utf-8")).hexdigest()


def _det(res, what, allow_nonzero=False):
    if not res.get("deterministic", False):
        raise Drop("nondeterministic", what)
    if not allow_nonzero and res.get("exit_code") not in (0, None):
        raise Drop("nonzero_exit", "%s exit %s" % (what, res.get("exit_code")))
    if res.get("events"):
        raise Drop("nonportable", what)


def _obs(res, what):
    obs, steps = S.parse_driver_stdout(res.get("stdout", ""))
    if obs is None:
        raise Drop("missing_output", what)
    return obs, steps


# ================================================================================================ requests
def requests_for(spec, rid):
    head = spec["head"]
    if head == "OUT4":
        return _req_out4(spec, rid)
    if head == "EQV2":
        return _req_eqv2(spec, rid)
    return _req_tfail2(spec, rid)


def _mutant_lo(spec, site):
    origin = spec.get("origin_base", spec["base"])
    _, mlo, _ = variant(origin, spec["ids"], spec["lang"], None, site, None, "wm")
    return mlo


def _req_out4(spec, rid):
    lo, lang = spec["lo"], spec["lang"]
    plan = {"calls": spec["calls"], "mode": "last"}
    reqs = {"gold": S.driver_request(rid + "#gold", lo, lang, plan)}
    for k, o in enumerate(spec["options"]):
        if o["kind"] == "EXEC-NEARMISS" and o["mutant"] is not None:
            reqs["opt%d" % k] = S.driver_request("%s#opt%d" % (rid, k), _mutant_lo(spec, o["mutant"]), lang, plan)
        elif o["kind"] == "PAIR-OLD-GOLD":
            reqs["opt%d" % k] = S.driver_request("%s#opt%d" % (rid, k), spec["origin_lo"], lang, plan)
    reqs["steps"] = S.driver_request(rid + "#steps", lo, lang, {"calls": spec["calls"], "mode": "all"}, instrument_steps=True)
    return reqs


def _req_eqv2(spec, rid):
    lang = spec["lang"]
    tgt = spec["target"]
    snap = tgt.get("snapshot")
    pts = spec["points"]
    reqs = {"domA": S.domain_request(rid + "#domA", spec["lo"], lang, pts, snap),
            "domB": S.domain_request(rid + "#domB", spec["lo_b"], lang, pts, snap)}
    rp = [spec["rep_point"]]
    reqs["stepsA"] = S.driver_request(rid + "#stepsA", spec["lo"], lang, {"calls": rp[0], "mode": "all", "snapshot": snap}, True)
    reqs["stepsB"] = S.driver_request(rid + "#stepsB", spec["lo_b"], lang, {"calls": rp[0], "mode": "all", "snapshot": snap}, True)
    if spec["gold_label"] == "NO":
        d = spec["info"]["distinguishing"]
        plan = {"calls": d, "mode": "all", "snapshot": snap}
        reqs["disA"] = S.driver_request(rid + "#disA", spec["lo"], lang, plan)
        reqs["disB"] = S.driver_request(rid + "#disB", spec["lo_b"], lang, plan)
    return reqs


def _req_tfail2(spec, rid):
    lo, lang = spec["lo"], spec["lang"]
    if lang == "python":
        test = S.pytests_request(rid + "#test", lo, lang, spec["test_path"], spec["test_text"], spec["suite"])
    else:
        test = S.suite_request(rid + "#test", lo, lang, {spec["test_path"]: spec["test_text"]},
                               suites=[(spec["test_path"], spec["suite"])], repeats=C.WITNESS_RUNS)
        test["expected_ids"] = expected_ids(lang, lo, spec)
    calls = [{"fn": s["fn"], "args": s["args"]} for s in spec["steps"]]
    return {"test": test,
            "steps": S.driver_request(rid + "#steps", lo, lang, {"calls": calls, "mode": "all"}, instrument_steps=True)}


def expected_ids(lang, lo, spec):
    """Test ids as the executor's verdict code expects them (UNVERIFIED for node junit naming: confirm in the first
    sandbox smoke; Go and pytest ids are documented formats)."""
    name = spec["suite"]["cases"][0]["name"]
    if lang == "go":
        return ["%s/Test%s" % (lo["meta"]["package"], name.capitalize())]
    if lang in ("javascript", "typescript"):
        return ["test::%s" % name]
    return None


# ================================================================================================ labelling
def finalize(spec, rid, results, picker):
    head = spec["head"]
    if head == "OUT4":
        label, manifest = _fin_out4(spec, rid, results)
    elif head == "EQV2":
        label, manifest = _fin_eqv2(spec, rid, results)
    else:
        label, manifest = _fin_tfail2(spec, rid, results)
    manifest["solver_a_version"] = SOLVER_A_VERSION
    manifest["pins"] = {"status": "PENDING_L0_IMAGE_RECORD" if C.PINS_PENDING else "recorded"}
    manifest["module_norm_hash"] = I.norm_hash(spec["lo"])
    for key in ("lo", "lo_b"):
        if spec.get(key) is not None:
            foreign = provenance.foreign_identifiers(spec[key], spec["ids"])
            if foreign:
                raise Drop("ident_provenance", str(foreign[:3]))
    row = ROWS.build_row(spec, picker, rid, label, manifest)
    hits = lint.lint_files(spec["lang"], R.render_module(spec["lo"], spec["lang"]))
    if spec["head"] == "TFAIL2":
        hits.update(lint.lint_files(spec["lang"], {spec["test_path"]: spec["test_text"]}))
    if hits:
        raise Drop("lint", str(sorted(hits)[:2]))
    return row


def _bin_from_steps(steps):
    return SM.step_bin(steps)


def _fin_out4(spec, rid, results):
    g = results["gold"]
    _det(g, "gold")
    obs, _ = _obs(g, "gold")
    if obs != spec["gold_obs"]:
        raise Drop("unexpected_result", "gold differs from the spec expectation")
    wit = {"gold": {"obs": obs, "runs": g.get("runs", C.WITNESS_RUNS), "stdout_id": out_id(g)}, "options": {}}
    for k, o in enumerate(spec["options"]):
        key = "opt%d" % k
        if key in results:
            r = results[key]
            _det(r, key)
            ob, _ = _obs(r, key)
            if ob != o["obs"]:
                raise Drop("unexpected_distractor", key)
            if ob == obs and o["kind"] != "GOLD":
                raise Drop("distractor_equals_gold", key)
            wit["options"][key] = {"kind": o["kind"], "obs": ob, "runs": r.get("runs"), "stdout_id": out_id(r)}
    st = results["steps"]
    _det(st, "steps")
    _, steps = _obs(st, "steps")
    if steps is None:
        raise Drop("steps_missing")
    label = ROWS.LETTERS[spec["gold_index"]]
    return label, {"witness": wit, "spec_expectation": {"gold_obs": spec["gold_obs"], "bin_planned": spec["bin_ir"]},
                   "steps_final": steps, "bin_final": _bin_from_steps(steps), "steps_ir": spec["steps_ir"],
                   "distinguishing": None}


def _fin_eqv2(spec, rid, results):
    a, b = results["domA"], results["domB"]
    _det(a, "domA")
    _det(b, "domB")
    same = out_id(a) == out_id(b)
    want_same = spec["gold_label"] == "YES"
    if same != want_same:
        raise Drop("unexpected_result", "domain outputs %s but the spec expects %s" % ("equal" if same else "different", "equal" if want_same else "different"))
    wit = {"domain_runs": {"A": {"runs": a.get("runs"), "stdout_id": out_id(a)}, "B": {"runs": b.get("runs"), "stdout_id": out_id(b)}},
           "domain_points": spec["domain_size"]}
    dis = None
    if spec["gold_label"] == "YES":
        if not spec["meta"].get("construction"):
            raise Drop("yes_without_construction")
        label = "YES"
    else:
        da, db = results["disA"], results["disB"]
        _det(da, "disA")
        _det(db, "disB")
        oa, _ = _obs(da, "disA")
        ob, _ = _obs(db, "disB")
        if oa == ob:
            raise Drop("unexpected_result", "distinguishing input does not distinguish")
        dis = {"input": spec["info"]["distinguishing"], "A": oa, "B": ob}
        wit["distinguishing_runs"] = {"A": out_id(da), "B": out_id(db)}
        label = "NO"
    sa, sb = results["stepsA"], results["stepsB"]
    _det(sa, "stepsA")
    _det(sb, "stepsB")
    steps = ((_obs(sa, "stepsA")[1] or 0) + (_obs(sb, "stepsB")[1] or 0)) / 2.0
    if steps <= 0:
        raise Drop("steps_missing")
    return label, {"witness": wit, "spec_expectation": {"equal": want_same, "diff_fraction": spec["info"].get("diff_fraction")},
                   "steps_final": steps, "bin_final": _bin_from_steps(steps), "steps_ir": spec["steps_ir"], "distinguishing": dis,
                   "construction": spec["meta"].get("construction"), "chain": spec["info"].get("chain")}


def _fin_tfail2(spec, rid, results):
    t = results["test"]
    _det(t, "test", allow_nonzero=True)          # a failing test legitimately exits non-zero
    if spec["lang"] == "python":
        obs, _ = _obs(t, "test")
        fails = any(v != "pass" for v in obs.values())
        if not obs:
            raise Drop("missing_output", "no test results")
        evidence = obs
    else:
        v = t.get("verdict")
        if v not in ("PASS", "FAIL"):
            raise Drop("no_verdict", str(v))
        fails = v == "FAIL"
        evidence = {"verdict": v}
    want_fail = spec["gold_label"] == "FAIL"
    if fails != want_fail:
        raise Drop("unexpected_result", "test %s but the spec expects %s" % ("fails" if fails else "passes", "fail" if want_fail else "pass"))
    st = results["steps"]
    _det(st, "steps")
    _, steps = _obs(st, "steps")
    if steps is None:
        raise Drop("steps_missing")
    return ("YES" if fails else "NO"), {"witness": {"test": {"evidence": evidence, "runs": t.get("runs"), "stdout_id": out_id(t)}},
                                         "spec_expectation": {"fails": want_fail}, "steps_final": steps,
                                         "bin_final": _bin_from_steps(steps), "steps_ir": spec["steps_ir"], "distinguishing": None}


# ================================================================================================ batch driver
class SolverA:
    def __init__(self, executor, picker, checker=None):
        self.executor = executor
        self.picker = picker
        self.log = DropLog()
        self.checker = checker                          # LC_COMMON.checked.RowChecker: answer checks + G13 stamp at the moment of making

    def run(self, specs, id_prefix="T42c"):
        keyed, flat = {}, []
        for n, spec in enumerate(specs):
            rid = spec.get("row_id") or "%s-%s-%06d" % (id_prefix, spec["head"], n)
            spec["row_id"] = rid
            try:
                reqs = requests_for(spec, rid)
            except Skip as e:
                self.log.attempted += 1
                self.log.add("request_build:" + str(e)[:40], rid)
                continue
            keyed[rid] = reqs
            flat.extend(reqs.values())
        results = {r["row_id"]: res for r, res in zip(flat, self.executor.run(flat))}
        rows = []
        for spec in specs:
            rid = spec["row_id"]
            if rid not in keyed:
                continue
            self.log.attempted += 1
            res = {k: results[r["row_id"]] for k, r in keyed[rid].items()}
            try:
                rows.append(finalize(spec, rid, res, self.picker))
            except Drop as d:
                self.log.add(d.reason, rid)
        if self.checker is not None:
            rows = self.checker.filter(rows)
        return rows, self.log


# ================================================================================================ pre-row sandbox test
def agreement_requests(specs):
    """For >= 100 Python rows: the instrumented-twin step count and the sys.settrace line-event count of the same calls."""
    reqs = {}
    for k, spec in enumerate(specs):
        if spec["lang"] != "python" or spec["head"] != "OUT4":
            continue
        plan = {"calls": spec["calls"], "mode": "all"}
        reqs["%d#twin" % k] = S.driver_request("agree%d#twin" % k, spec["lo"], "python", plan, instrument_steps=True)
        reqs["%d#line" % k] = S.trace_request("agree%d#line" % k, spec["lo"], plan)
    return reqs


def agreement_report(specs, executor):
    reqs = agreement_requests(specs)
    order = list(reqs)
    res = dict(zip(order, executor.run([reqs[r] for r in order])))
    pairs = []
    for k in sorted({int(r.split("#")[0]) for r in order}):
        a = S.parse_driver_stdout(res["%d#twin" % k].get("stdout", ""))[1]
        b = S.parse_driver_stdout(res["%d#line" % k].get("stdout", ""))[1]
        if a is not None and b is not None:
            pairs.append((a, b))
    return S.step_agreement(pairs)

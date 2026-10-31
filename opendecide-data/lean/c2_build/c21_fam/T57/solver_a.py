"""T57 SOLVER A (primary pipeline) - the four-gate gold.

  gate a  gold-sanity   every hidden and visible test passes on the reference (2 runs; sandbox default).
  gate b  strength      the hidden suite kills at least T_s of the NON-EQUIVALENT mutants of the reference drawn from the
                        independent mutant pool (operators STRENGTH_OPS, disjoint from the bug-injection operators). A mutant
                        is non-equivalent when a test of the suite fails on it (a witness) or, if it survives the suite, when
                        the domain differential proves it; survivors with no witness are 'undecided' (excluded, counted).
                        mutmut / cosmic-ray (Python) are PENDING wiring: the own-mutator pool is used for all languages.
  gate c  differential  reference vs candidate over D (host-enumerated domain driver; equal stdout = no divergence).
  gate d  two-solver agreement: solver B (a separate session writes it) re-derives the same labels; checked by the K4 gate.

Execution class of a patch (first rule that applies): NOFIX, REGRESSION, PARTIAL, CORRECT. An unexpected class
(execution disagrees with the spec expectation) is KEPT only when the witness is complete, and is counted per operator;
> 15% unexpected for one operator sends that operator back to the builder. Nothing here executes generated code.
"""
import collections
import hashlib

from LC_COMMON import codeview as V
from LC_COMMON import ir as I
from LC_COMMON import irmut, provenance, render as R
from LC_COMMON import sandbox_iface as S
from LC_COMMON import sampler as SM
from LC_COMMON import suites
from LC_COMMON import lint
from LC_COMMON.interp import Interp

from . import config as C
from . import rows as ROWS
from .base import Skip, files_of, lower, mk_rng

SOLVER_A_VERSION = "T57-solver-a-1"
TS = {"value": C.TS_PROPOSAL, "set_by_pilot": False}          # gate b threshold; the 50-module pilot fixes it (see pilot_threshold)


class Drop(Exception):
    def __init__(self, reason, detail=""):
        super().__init__("%s %s" % (reason, detail))
        self.reason, self.detail = reason, detail


class Stats:
    def __init__(self):
        self.drops = collections.Counter()
        self.examples = {}
        self.attempted = 0
        self.op_unexpected = collections.Counter()     # candidate kind -> unexpected class count
        self.op_total = collections.Counter()
        self.module_fail = collections.Counter()
        self.module_total = 0
        self.module_pass = 0

    def drop(self, reason, rid):
        self.drops[reason] += 1
        self.examples.setdefault(reason, []).append(rid)
        self.examples[reason] = self.examples[reason][:5]

    def operators_over_budget(self, limit=0.15, min_n=20):
        return sorted(k for k, n in self.op_total.items() if n >= min_n and self.op_unexpected[k] / n > limit)


def set_threshold(value, by_pilot=True):
    if value < C.TS_FLOOR:
        raise ValueError("T_s may never go below %.2f" % C.TS_FLOOR)
    TS["value"], TS["set_by_pilot"] = value, by_pilot


def pilot_threshold(module_scores, nonpython_scores=None):
    """The rule written before the pilot: T_s = 0.90 if >= 70% of the pilot modules reach 0.90; otherwise the suite recipe
    gets ONE revision (caller reruns on fresh modules) and T_s is still never below 0.80. A non-Python language scoring
    below 0.80 on its modules extends its pilot to 20 modules. Returns (T_s | None, action)."""
    n = len(module_scores)
    if n == 0:
        return None, "no modules"
    share = sum(1 for s in module_scores if s >= C.TS_PROPOSAL) / n
    if share >= C.TS_PILOT_SHARE_REQUIRED:
        return C.TS_PROPOSAL, "T_s = 0.90 (%.0f%% of pilot modules reach it)" % (100 * share)
    return None, "revise the suite recipe once (more boundary and pairwise cases from D) and rerun the pilot on fresh modules"


# ----------------------------------------------------------------------------------------------- files and states
def test_files(task):
    """(visible files, hidden files, hidden blocks). Visible and hidden live in different files (and are run apart in the
    verdict story: the hidden text is never rendered into a row)."""
    if task.get("_tf"):
        return task["_tf"]
    lo, lang, ids = task["ref_lo"], task["lang"], task["ids"]
    pairs = []
    vis = suites.render_suite_files(lo, lang, {"cases": [task["visible"]]}, ids, "vt", pairs=pairs)
    blocks = {}
    hid = suites.render_suite_files(lo, lang, task["hidden"], ids, "ht", blocks=blocks, pairs=pairs)
    task["_tf"] = (vis, hid, blocks, pairs)
    return task["_tf"]


def all_case_names(task):
    return [c["name"] for c in task["suite_all"]["cases"]]


def suite_req(task, key, mod, tests, suites_pairs, module_files=None, repeats=C.WITNESS_RUNS_SUITE):
    rid = "%s#%s" % (task["uid"], key)
    rq = S.suite_request(rid, mod, task["lang"], tests, suites=suites_pairs, repeats=repeats, module_files=module_files)
    return rid, rq


def states_of(res, names):
    if res.get("states") is None:
        raise Drop("no_states", "executor result without per-test states")
    return S.case_state_map(res["states"], names)


def det(res, what):
    if not res.get("deterministic", False):
        raise Drop("nondeterministic", what)


# ----------------------------------------------------------------------------------------------- requests
def strength_pool(task, limit=C.STRENGTH_POOL_SIZE):
    """Mutants of the reference from the STRENGTH operators (independent of bug injection). Cached on the task."""
    if "strength" in task:
        return task["strength"]
    rng = mk_rng("strength", task["id"])
    out = []
    for site, mm in irmut.mutants(task["ref"], irmut.STRENGTH_OPS, rng=rng, limit=limit * 3):
        try:
            mlo = lower(mm, task["lang"], task["ids"])
        except Skip:
            continue
        st = suites.evaluate(mlo, task["lang"], task["suite_all"])
        out.append({"site": site, "lo": mlo, "killed_spec": not all(st.values())})
        if len(out) >= limit:
            break
    task["strength"] = out
    return out


def module_requests(task):
    vis, hid, _, sp = test_files(task)
    tests = dict(vis)
    tests.update(hid)
    reqs = {}
    rid, rq = suite_req(task, "sanity", task["ref_lo"], tests, sp)
    reqs[rid] = ("sanity", rq)
    rid, rq = suite_req(task, "buggy", task["buggy_lo"], tests, sp)
    reqs[rid] = ("buggy", rq)
    mid = task["id"]
    for k, m in enumerate(strength_pool(task)):
        rid = "%s#str%d" % (mid, k)
        rq = S.suite_request(rid, m["lo"], task["lang"], tests, suites=sp, repeats=C.WITNESS_RUNS_SUITE)
        reqs[rid] = ("str%d" % k, rq)
        if not m["killed_spec"]:
            drid = "%s#strd%d" % (mid, k)
            reqs[drid] = ("strd%d" % k, S.domain_request(drid, m["lo"], task["lang"], task["points"], task["snapshot"]))
    drid = "%s#domR" % mid
    reqs[drid] = ("domR", S.domain_request(drid, task["ref_lo"], task["lang"], task["points"], task["snapshot"]))
    return reqs


def cand_key(c):
    return hashlib.sha256(c["diff"].encode()).hexdigest()[:10]


def cand_requests(task, c):
    vis, hid, _, sp = test_files(task)
    tests = dict(vis)
    tests.update(hid)
    k = cand_key(c)
    reqs = {}
    rid, rq = suite_req(task, "c" + k, c["lo"], tests, sp, module_files=c["files"])
    reqs[rid] = ("c" + k, rq)
    if c["cls"] == "CORRECT" or (c["cls"] == "PARTIAL" and not c["evidence"].get("failing")):
        # the differential is only needed when every test is expected to pass (CORRECT, or PARTIAL by divergence alone)
        drid = "%s#dc%s" % (task["uid"], k)
        reqs[drid] = ("dc" + k, S.domain_request(drid, c["lo"], task["lang"], task["points"], task["snapshot"], module_files=c["files"]))
    return reqs


def testsel_requests(spec):
    task = spec["task"]
    reqs = {}
    fixed = spec["cands"][0]
    blocks = {}
    hidden = {c["name"]: c for c in task["hidden"]["cases"]}
    for k, name in enumerate(spec["options"]):
        path, text = R.render_tests(task["ref_lo"], task["lang"], {"cases": [hidden[name]]}, "so%d" % k)
        for tag, mod, mf in (("B", task["buggy_lo"], None), ("F", fixed["lo"], fixed["files"])):
            rid = "%s#ts%d%s" % (task["uid"], k, tag)
            reqs[rid] = ("ts%d%s" % (k, tag), S.suite_request(rid, mod, task["lang"], {path: text},
                                                              suites=[(path, {"cases": [hidden[name]]})], module_files=mf))
    return reqs


def visible_result_requests(task, c=None):
    call = task["visible"]["steps"][0]
    plan = {"calls": [{"fn": call["fn"], "args": call["args"]}], "mode": "last"}
    reqs = {}
    rid = "%s#vrB" % task["uid"]
    reqs[rid] = ("vrB", S.driver_request(rid, task["buggy_lo"], task["lang"], plan))
    if c is not None:
        rid = "%s#vrP%s" % (task["uid"], cand_key(c))
        reqs[rid] = ("vrP" + cand_key(c), S.driver_request(rid, c["lo"], task["lang"], plan, module_files=c["files"]))
    return reqs


# ----------------------------------------------------------------------------------------------- module gates
def module_gates(task, R_, stats):
    """R_: results by short key. Returns the module record (sanity, tags, strength) or raises Drop."""
    names = all_case_names(task)
    san = R_["sanity"]
    det(san, "sanity")
    ss = states_of(san, names)
    if any(v != "passed" for v in ss.values()):
        raise Drop("module_gold_sanity", "a test fails on the reference")
    bug = R_["buggy"]
    det(bug, "buggy")
    bs = states_of(bug, names)
    v = task["visible"]["name"]
    if bs[v] == "passed":
        raise Drop("module_visible_passes_on_buggy")
    exp_fail = set(task["target"]) | {v}
    got_fail = {c for c, s in bs.items() if s != "passed"}
    if got_fail != exp_fail:
        raise Drop("module_bug_tags_unexpected", "target/p2p tags differ from the spec expectation")
    killed = decided = survived_equiv = 0
    domR = R_["domR"]
    for k, m in enumerate(strength_pool(task)):
        res = R_["str%d" % k]
        det(res, "str%d" % k)
        st = states_of(res, names)
        if any(s != "passed" for s in st.values()):
            killed += 1
            decided += 1
            continue
        dres = R_.get("strd%d" % k)
        if dres is None:
            raise Drop("module_strength_unexpected_survivor", "a mutant the spec expected the suite to kill survived; no differential was requested")
        det(dres, "strd%d" % k)
        if S_out_id(dres) != S_out_id(domR):
            decided += 1                                  # survivor proven non-equivalent by the differential
        else:
            survived_equiv += 1                           # no witness: undecided
    n = len(strength_pool(task))
    if n == 0:
        raise Drop("module_strength_no_mutants")
    undecided = survived_equiv / n
    rec = {"mutants": n, "decided": decided, "killed": killed, "undecided": survived_equiv, "undecided_share": undecided,
           "kill_share": (killed / decided) if decided else None, "T_s": TS["value"], "T_s_by_pilot": TS["set_by_pilot"]}
    if undecided > C.UNDECIDED_MAX:
        raise Drop("module_undecided_over_25pct", str(rec))
    if decided < C.MIN_STRENGTH_MUTANTS:
        raise Drop("module_strength_too_few_decidable", str(rec))
    if rec["kill_share"] < TS["value"]:
        raise Drop("module_strength_below_threshold", str(rec))
    rec["sanity_ok"] = True
    rec["bug_tags"] = {"target": sorted(task["target"]), "p2p": len(task["p2p"])}
    return rec


def S_out_id(res):
    return res.get("stdout_sha256") or hashlib.sha256(res.get("stdout", "").encode("utf-8")).hexdigest()


def exec_class(task, c, R_, names):
    """Execution class of candidate c from its suite run and (when needed) its differential. Returns (cls, evidence)."""
    k = cand_key(c)
    res = R_["c" + k]
    det(res, "cand")
    st = states_of(res, names)
    v = task["visible"]["name"]
    if st[v] != "passed":
        return "NOFIX", {"failing": [v]}
    p2p_fail = [x for x in task["p2p"] if st[x] != "passed"]
    if p2p_fail:
        return "REGRESSION", {"failing": p2p_fail[:3]}
    tgt_fail = [x for x in task["target"] if st[x] != "passed"]
    if tgt_fail:
        return "PARTIAL", {"failing": tgt_fail[:3]}
    dres = R_.get("dc" + k)
    if dres is None:
        raise Drop("unexpected_class_needs_differential", "candidate passed every test but no differential was requested")
    det(dres, "dc")
    if S_out_id(dres) != S_out_id(R_["domR"]):
        return "PARTIAL", {"divergence": "domain outputs differ", "spec": c["evidence"].get("divergence")}
    return "CORRECT", {"differential": "equal"}


# ----------------------------------------------------------------------------------------------- batch driver
class SolverA:
    def __init__(self, executor, picker, checker=None):
        self.executor = executor
        self.picker = picker
        self.stats = Stats()
        self.checker = checker                          # LC_COMMON.checked.RowChecker: answer checks + G13 stamp at the moment of making

    # -- request collection -----------------------------------------------------------------------
    def collect(self, specs):
        pool = {}                                             # request id -> (key, request)   (deduplicated)
        for spec in specs:
            task = spec["task"]
            for rid, kv in module_requests(task).items():
                pool.setdefault(rid, kv)
            if spec["head"] in ("VERDICT", "BEST4"):
                for c in spec["cands"]:
                    for rid, kv in cand_requests(task, c).items():
                        pool.setdefault(rid, kv)
            if spec["head"] == "TESTSEL":
                for rid, kv in testsel_requests(spec).items():
                    pool.setdefault(rid, kv)
                for rid, kv in cand_requests(task, spec["cands"][0]).items():
                    pool.setdefault(rid, kv)
            if spec.get("with_outputs"):
                c = spec["cands"][0] if spec["head"] == "VERDICT" else None
                for rid, kv in visible_result_requests(task, c).items():
                    pool.setdefault(rid, kv)
        return pool

    def run(self, specs):
        pool = self.collect(specs)
        order = list(pool)
        results = dict(zip(order, self.executor.run([pool[r][1] for r in order])))
        rows = []
        module_cache = {}
        for spec in specs:
            self.stats.attempted += 1
            rid = spec["row_id"]
            task = spec["task"]
            try:
                mkey = task["uid"]
                if mkey not in module_cache:
                    R_ = {}
                    for r, (k, rq) in module_requests(task).items():
                        R_[k] = results[r]
                    self.stats.module_total += 1
                    try:
                        module_cache[mkey] = module_gates(task, R_, self.stats)
                        self.stats.module_pass += 1
                    except Drop as d:
                        module_cache[mkey] = d
                        self.stats.module_fail[d.reason] += 1
                mrec = module_cache[mkey]
                if isinstance(mrec, Drop):
                    raise mrec
                rows.append(self.finalize(spec, rid, results, mrec))
            except Drop as d:
                self.stats.drop(d.reason, rid)
        if self.checker is not None:
            from . import schema as SCH
            for spec in specs:                                 # solver B gets the task package of every module it will judge
                self.checker.packages.setdefault(spec["task"]["uid"], SCH.task_package(spec["task"]))
            rows = self.checker.filter(rows)
        return rows

    # -- per-head labelling -----------------------------------------------------------------------
    def _cand_results(self, task, c, results):
        names = all_case_names(task)
        R_ = {}
        for rid, (k, rq) in cand_requests(task, c).items():
            R_[k] = results[rid]
        R_["domR"] = results["%s#domR" % task["id"]]
        cls, ev = exec_class(task, c, R_, names)
        self.stats.op_total[c["kind"]] += 1
        if cls != c["cls"]:
            self.stats.op_unexpected[c["kind"]] += 1
        return cls, ev

    def finalize(self, spec, rid, results, mrec):
        head, task = spec["head"], spec["task"]
        picker = self.picker
        manifest = {"module": mrec, "solver_a_version": SOLVER_A_VERSION,
                    "pins": {"status": "PENDING_L0_IMAGE_RECORD" if C.PINS_PENDING else "recorded"},
                    "spec_expectation": {"label": spec["label_exp"], "reason": spec["reason_exp"]},
                    "module_norm_hash": I.norm_hash(task["buggy_lo"]), "tags": {"target": len(task["target"]), "p2p": len(task["p2p"])}}
        vres = None
        if head == "VERDICT":
            cls, ev = self._cand_results(task, spec["cands"][0], results)
            label = "CORRECT" if cls == "CORRECT" else "INCORRECT"
            manifest.update({"cand_classes": [cls], "evidence": [ev], "reason": None if cls == "CORRECT" else cls})
            spec = dict(spec, reason_actual=None if cls == "CORRECT" else cls)
        elif head == "BEST4":
            classes, evs = [], []
            for c in spec["cands"]:
                cls, ev = self._cand_results(task, c, results)
                classes.append(cls)
                evs.append(ev)
            good = [k for k, x in enumerate(classes) if x == "CORRECT"]
            if len(good) != 1:
                raise Drop("best4_not_exactly_one_correct", str(classes))
            label = ROWS.LETTERS[good[0]]
            spec = dict(spec, gold_index=good[0])
            manifest.update({"cand_classes": classes, "evidence": evs})
        elif head == "LOCALISE":
            names = all_case_names(task)
            bs = states_of(results["%s#buggy" % task["uid"]], names)
            if bs[task["visible"]["name"]] == "passed":
                raise Drop("localise_no_failing_test")
            label = ROWS.LETTERS[spec["gold_index"]]
            manifest.update({"cand_classes": [], "killing_test": task["visible"]["name"], "single_modifier": not task["multi"]})
        else:                                                   # TESTSEL
            label, tev = self._testsel_label(spec, results)
            fixed = spec["cands"][0]
            cls, ev = self._cand_results(task, fixed, results)
            if cls != "CORRECT":
                raise Drop("testsel_fix_not_correct", cls)
            manifest.update({"cand_classes": [cls], "evidence": [ev], "testsel": tev})
        vr = None
        if spec.get("with_outputs"):
            vr = self._visible_result(task, spec, results)
        row = ROWS.build_row(spec, picker, rid, label, manifest, variant="with_outputs" if vr else "primary", visible_result=vr)
        self._lint(row, spec)
        row["meta"]["leak_hits"] = self._leak_scan(row, spec)
        if row["meta"]["leak_hits"]:
            raise Drop("hidden_test_leak", str(row["meta"]["leak_hits"][:2]))
        return row

    def _leak_scan(self, row, spec):
        """Hidden-suite test bodies (normalised) that appear in the rendered row; TESTSEL may show its own option tests."""
        import re
        task = spec["task"]
        _, _, blocks, _ = test_files(task)
        p = re.sub(r"\s+", " ", row["prompt_text"])
        own = set(spec.get("options") or []) if spec["head"] == "TESTSEL" else set()
        return [c for c, body in blocks.items() if c not in own and re.sub(r"\s+", " ", body).strip() in p]

    def _testsel_label(self, spec, results):
        task = spec["task"]
        gold = None
        ev = []
        for k, name in enumerate(spec["options"]):
            rb, rf = results["%s#ts%dB" % (task["uid"], k)], results["%s#ts%dF" % (task["uid"], k)]
            det(rb, "tsB")
            det(rf, "tsF")
            sb = list(rb["states"].values())
            sf = list(rf["states"].values())
            fails_before = any(v != "passed" for v in sb)
            passes_after = all(v == "passed" for v in sf)
            ev.append({"option": k, "fails_before": fails_before, "passes_after": passes_after})
            if fails_before and passes_after:
                if gold is not None:
                    raise Drop("testsel_two_detectors")
                gold = k
            elif fails_before or not passes_after:
                raise Drop("testsel_distractor_not_neutral", str(k))
        if gold is None or gold != spec["gold_index"]:
            raise Drop("testsel_gold_unexpected")
        return ROWS.LETTERS[gold], ev

    def _visible_result(self, task, spec, results):
        call = task["visible"]["steps"][0]
        ob = S.parse_driver_stdout(results["%s#vrB" % task["uid"]].get("stdout", ""))[0]
        if ob is None:
            raise Drop("visible_result_missing")
        step = task["visible"]["steps"][0]
        exp = step.get("expect", step.get("err"))
        args = ", ".join(str(a) for a in call["args"])
        text = "FAILED %s: %s(%s) -> %s, expected %s" % (task["visible"]["name"], call["fn"], args, _short(ob), exp)
        if spec["head"] == "VERDICT":
            c = spec["cands"][0]
            op = S.parse_driver_stdout(results["%s#vrP%s" % (task["uid"], cand_key(c))].get("stdout", ""))[0]
            text += "\nafter the patch: " + ("PASSED" if op is not None and "ok" in op and op["ok"] == exp else "FAILED -> " + _short(op))
        return text[:900]

    def _lint(self, row, spec):
        task = spec["task"]
        hits = lint.lint_files(task["lang"], files_of(task["buggy_lo"], task["lang"]))
        if hits:
            raise Drop("lint", str(sorted(hits)[:2]))
        foreign = provenance.foreign_identifiers(task["buggy_lo"], task["ids"])
        if foreign:
            raise Drop("ident_provenance", str(foreign[:3]))
        for c in spec["cands"]:
            f = provenance.foreign_identifiers(c["lo"], task["ids"])
            if f:
                raise Drop("ident_provenance", str(f[:3]))


def _short(ob):
    if ob is None:
        return "no output"
    return str(ob.get("ok")) if "ok" in ob else "raises " + str(ob.get("exc"))

"""T57 tasks: a reference module R, one injected bug (buggy module B), a visible failing test V, a hidden suite H tagged
TARGET / PASS-TO-PASS, a differential input set D, and a library of candidate patches with their execution classes.

Everything here is the SPEC EXPECTATION (IR interpreter in the target dialect). The labels of a row are decided by the
sandbox runs of Solver A (gold-sanity, strength, differential, two-solver agreement); an unexpected class there is kept
only when its witness is complete and counted against the operator (G0-lite section 2).

Candidate library (registry ids): CAND-INVERSE, CAND-ALTFIX, CAND-HALFSITE, CAND-NEARMISS, CAND-HELPERSHIFT,
CAND-NARROWGUARD, CAND-WRONGPLACE. Labels come from execution, never from the intent of the operator.
Patches never touch test files (a "touches tests" flag is constant here).
"""
import random

from LC_COMMON import domain as D
from LC_COMMON import ir as I
from LC_COMMON import irmut, suites
from LC_COMMON import transforms as T
from LC_COMMON.interp import Interp

from . import config as C
from .base import FAMILY, Skip, diff_text, files_of, lower, mk_rng, new_base

CAND_IDS = ("CAND-INVERSE", "CAND-ALTFIX", "CAND-HALFSITE", "CAND-NEARMISS", "CAND-HELPERSHIFT", "CAND-NARROWGUARD", "CAND-WRONGPLACE")


def differential(lang, ref_lo, cand_lo, points, snapshot):
    """First divergence between reference and candidate over D (list of call lists), or None."""
    for pt in points:
        a, b = Interp(ref_lo, lang), Interp(cand_lo, lang)
        oa = [a.call(c["fn"], c["args"]) for c in pt]
        ob = [b.call(c["fn"], c["args"]) for c in pt]
        if snapshot and any(I.functions(ref_lo)[c["fn"]]["scope"] == "method" for c in pt):
            oa.append(a.call(snapshot, []))
            ob.append(b.call(snapshot, []))
        if oa != ob:
            return pt
    return None


def classify(task, cand_lo, points=None):
    """Execution class of a candidate (spec expectation): first rule that applies, in the G0-lite precedence."""
    lang = task["lang"]
    states = suites.evaluate(cand_lo, lang, task["suite_all"])
    v = task["visible"]["name"]
    if not states[v]:
        return "NOFIX", {"failing": [v]}
    p2p_fail = [c for c in task["p2p"] if not states[c]]
    if p2p_fail:
        return "REGRESSION", {"failing": p2p_fail[:3]}
    tgt_fail = [c for c in task["target"] if not states[c]]
    div = differential(lang, task["ref_lo"], cand_lo, points if points is not None else task["points"], task["snapshot"])
    if tgt_fail or div is not None:
        return "PARTIAL", {"failing": tgt_fail[:3], "divergence": div}
    return "CORRECT", {}


# ----------------------------------------------------------------------------------------------- the task
def make_tasks(seed, lang, kind="A", multi=False, need_functions=1, n_bugs=1, distinct_fns=False, module_kw=None, prefer_trace=False):
    """kind 'A' (VERDICT / BEST4 / LOCALISE rows) or 'T' (TESTSEL only: its module is used for nothing else).
    One base module, up to `n_bugs` different injected bugs (each its own task: own visible test, own hidden split)."""
    rng = mk_rng("task", seed, lang, kind)
    pred = (lambda m: len(m["funcs"]) >= need_functions) if need_functions > 1 else None
    ref, ids = new_base("%s%s" % (kind.lower(), seed), lang, pred=pred, custom_errors=rng.random() < 0.2, **(module_kw or {}))
    ref_lo = lower(ref, lang, ids)
    suite_all = suites.build_suite(ref_lo, lang, rng, ids, "h", n_cases=30)
    if len(suite_all["cases"]) < 8:
        raise Skip("suite too small")
    if len(irmut.enumerate_sites(ref, irmut.STRENGTH_OPS)) < 10:
        raise Skip("too few strength-pool mutation sites to measure suite strength")
    points, snapshot = suites.differential_points(ref_lo, cap=2000)
    if multi:
        sites = [s for s in (irmut.multi_sites(ref, ms, rng) for ms in list(irmut.MULTI_OPS) * 3) if s]
    else:
        sites = irmut.enumerate_sites(ref, irmut.INJECT_OPS)
        rng.shuffle(sites)
    tasks, used_fns, used_paths = [], set(), set()
    for s in sites[:80]:
        if len(tasks) >= n_bugs:
            break
        first = (s.get("sites") or [s])[0]
        if distinct_fns and first["fn"] in used_fns:
            continue
        key = (first["fn"], tuple(first["path"]))
        if key in used_paths:
            continue
        buggy = irmut.apply_site(ref, s)
        if buggy is None:
            continue
        try:
            b_lo = lower(buggy, lang, ids)
        except Skip:
            continue
        st = suites.evaluate(b_lo, lang, suite_all)
        failing = [c for c, ok in st.items() if not ok]
        n = len(st)
        if len(failing) < 2 or len(failing) > 0.5 * n or n - len(failing) < 4:
            continue
        vis = [c for c in suite_all["cases"] if c["name"] in failing and len(c["steps"]) == 1]
        if not vis:
            continue
        if prefer_trace:                                  # LOCALISE: the killing test must traverse more than the bug function
            long_ = [c for c in vis if len(case_trace(ref_lo, lang, c)) >= 2]
            if not long_:
                continue
            vis = long_
        visible = rng.choice(vis)
        hidden = {"cases": [c for c in suite_all["cases"] if c["name"] != visible["name"]]}
        target = [c for c in failing if c != visible["name"]]
        p2p = [c["name"] for c in hidden["cases"] if c["name"] not in failing]
        bug_fns = sorted({x["fn"] for x in (s.get("sites") or [s])})
        used_fns.add(first["fn"])
        used_paths.add(key)
        task = {
            "id": ref["id"], "uid": "%s.b%d" % (ref["id"], len(tasks)), "kind": kind, "seed": seed, "lang": lang, "ids": ids,
            "ref": ref, "ref_lo": ref_lo, "buggy": buggy, "buggy_lo": b_lo, "suite_all": suite_all, "hidden": hidden,
            "visible": visible, "target": target, "p2p": p2p, "site": s, "bug_fn": bug_fns[0], "bug_fns": bug_fns,
            "points": points, "snapshot": snapshot, "cdom": ref["meta"]["cdom"], "multi": bool(s.get("sites")), "cands": None,
        }
        task["trace"] = case_traces(task)
        tasks.append(task)
    if not tasks:
        raise Skip("no bug with a usable visible test")
    return tasks


def make_task(seed, lang, kind="A", multi=False, need_functions=1):
    return make_tasks(seed, lang, kind, multi, need_functions, 1)[0]


def case_trace(lo, lang, case):
    it = Interp(lo, lang)
    for s in case["steps"]:
        it.call(s["fn"], s["args"])
    return set(it.called)


def case_traces(task):
    """{case name: set of function names the case traverses on the REFERENCE}."""
    out = {}
    for c in task["suite_all"]["cases"]:
        it = Interp(task["ref_lo"], task["lang"])
        for s in c["steps"]:
            it.call(s["fn"], s["args"])
        out[c["name"]] = set(it.called)
    return out


# ----------------------------------------------------------------------------------------------- candidates
def _cand(task, kind, base_mod, rng, info=None):
    lang, ids = task["lang"], task["ids"]
    try:
        lo = lower(base_mod, lang, ids)
    except Skip:
        return None
    before = files_of(task["buggy_lo"], lang)
    after = files_of(lo, lang)
    text, changed, hunks, nfiles = diff_text(before, after)
    if not text or changed > C.MAX_DIFF_LINES:
        return None
    cls, ev = classify(task, lo)
    return {"kind": kind, "base": base_mod, "lo": lo, "files": after, "diff": text, "changed": changed, "hunks": hunks,
            "n_files": nfiles, "cls": cls, "evidence": ev, "info": info or {}}


def build_candidates(task, rng, want=None):
    """Spec-level candidate pool for a task (lazily cached): list of candidate dicts. Distinct diffs only."""
    if task["cands"] is not None:
        return task["cands"]
    ref, buggy, ids, lang = task["ref"], task["buggy"], task["ids"], task["lang"]
    out, seen = [], set()

    def add(c):
        if c is not None and c["diff"] not in seen:
            seen.add(c["diff"])
            out.append(c)

    # INVERSE: the reference is exactly the inverse of the injected bug
    add(_cand(task, "CAND-INVERSE", ref, rng))
    # ALTFIX: an alternative correct rewrite (reference + an equivalence transform); still CORRECT by execution
    names = [f["name"] for f in ref["funcs"]]
    rng.shuffle(names)
    for fn in [task["bug_fn"]] + names:
        for eq in rng.sample(list(T.IDS), len(T.IDS)):
            alt = T.apply(ref, fn, eq, rng, ids, "alt")
            if alt is None:
                continue
            c = _cand(task, "CAND-ALTFIX", alt, rng, {"transform": eq, "fn": fn})
            if c is not None and c["diff"] not in seen:
                add(c)
                break
        if sum(1 for x in out if x["kind"] == "CAND-ALTFIX") >= 2:
            break
    # HALFSITE: fix one of several injected sites
    if task["multi"]:
        sub = task["site"]["sites"]
        for keep in range(len(sub)):
            rest = [s for k, s in enumerate(sub) if k != keep]
            m = ref
            for s in rest:
                m2 = irmut.apply_site(m, s)
                m = m2 if m2 is not None else m
            add(_cand(task, "CAND-HALFSITE", m, rng, {"kept_site": sub[keep]["path"]}))
    # NEARMISS: the inverse plus one wrong token (a one-token mutant of the reference inside the bug function)
    ms = irmut.mutants(ref, irmut.INJECT_OPS, set(task["bug_fns"]), limit=8, rng=rng)
    for site, mm in ms:
        add(_cand(task, "CAND-NEARMISS", mm, rng, {"op": site["op"], "fn": site["fn"]}))
    # HELPERSHIFT: an attempt to compensate in a function the bug function calls (or that calls it)
    related = set()
    fns = I.functions(buggy)
    for _, n in I.walk(fns[task["bug_fn"]]["body"]):
        if n[0] in ("fcall", "mcall"):
            related.add(n[1])
    for f in buggy["funcs"]:
        if any(n[0] in ("fcall", "mcall") and n[1] == task["bug_fn"] for _, n in I.walk(f["body"])):
            related.add(f["name"])
    related.discard(task["bug_fn"])
    if related:
        for site, mm in irmut.mutants(buggy, irmut.INJECT_OPS, related, limit=4, rng=rng):
            add(_cand(task, "CAND-HELPERSHIFT", mm, rng, {"op": site["op"], "fn": site["fn"]}))
    # NARROWGUARD: reference behaviour only on a property-defined region around the failing input
    ng = narrow_guard(task, rng)
    if ng is not None:
        add(_cand(task, "CAND-NARROWGUARD", ng[0], rng, ng[1]))
    # WRONGPLACE: a plausible edit in a function other than the bug function
    others = {f["name"] for f in buggy["funcs"]} - set(task["bug_fns"])
    if others:
        for site, mm in irmut.mutants(buggy, irmut.INJECT_OPS, others, limit=4, rng=rng):
            add(_cand(task, "CAND-WRONGPLACE", mm, rng, {"op": site["op"], "fn": site["fn"]}))
    task["cands"] = out
    return out


def narrow_guard(task, rng):
    """P = B with `if <property of the failing input>: <reference body>` prepended to the bug function. The property is
    a range / parity condition on one int parameter (never an equality with a literal of the visible test)."""
    buggy, ref = task["buggy"], task["ref"]
    fb, fr = I.functions(buggy)[task["bug_fn"]], I.functions(ref)[task["bug_fn"]]
    vcall = task["visible"]["steps"][0]
    if vcall["fn"] != task["bug_fn"]:
        return None
    ints = [(k, p[0]) for k, p in enumerate(fb["params"]) if p[1] == I.INT]
    if not ints:
        return None
    k, pname = rng.choice(ints)
    val = vcall["args"][k]
    if rng.random() < 0.5:
        lo_v = max(0, val - rng.randint(0, 2))
        cond = I.ge(I.v(pname), I.i(lo_v))
        prop = {"kind": "range", "param": pname, "lo": lo_v}
    else:
        cond = I.eq(I.bin_("%", I.v(pname), I.i(2)), I.i(val % 2))
        prop = {"kind": "parity", "param": pname, "mod": 2, "r": val % 2}
    new = I.clone(buggy)
    nf = I.functions(new)[task["bug_fn"]]
    nf["body"] = [I.if_(cond, I.clone(fr["body"]))] + nf["body"]
    try:
        I.check_module(new)
    except I.IRError:
        return None
    return new, prop

"""T66 MERGE: from a cell (conflict kind, resolution kinds) to specs with their witnesses. The executor runs the RENDERED files (never this process):
  strength witnesses: suite A and suite B on the base, A-only, B-only and reference-merge modules (K2),
  label witnesses: suite A and suite B on the candidate resolution (3 identical runs each).
The label is read from the witnesses by `label_from_witness` (SOLVER A's recomputation), never from the generator's expectation."""
import random

from LP_COMMON import sandbox_iface as S
from LP_COMMON.ns import Names

from . import merge as MG, merge3 as M3, prog as P, tests_gen as TG

LINES_MAX = 14


def _suite_files(stem, mod_text, ta_text, tb_text, a_name, b_name):
    return {stem + ".py": mod_text}, {a_name: ta_text, b_name: tb_text}


def run_suite(executor, rid, stem, mod_text, test_name, test_text):
    files = {stem + ".py": mod_text, test_name: test_text}
    return executor.run([S.tests_request(rid, files, test_name)])[0]


def _passed(res):
    return S.witness_ok(res) and S.all_pass(S.test_states(res))


def strength_witness(executor, rid, stem, models, ta_text, tb_text, a_name, b_name):
    """-> {model: {'A': passed, 'B': passed}} plus the raw results; K2 expectations checked by `strength_ok`."""
    out = {}
    for m in ("base", "A", "B", "AB"):
        text = P.render(models[m])
        ra = run_suite(executor, "%s:%s:A" % (rid, m), stem, text, a_name, ta_text)
        rb = run_suite(executor, "%s:%s:B" % (rid, m), stem, text, b_name, tb_text)
        out[m] = {"A": _passed(ra), "B": _passed(rb), "A_det": S.witness_ok(ra), "B_det": S.witness_ok(rb)}
    return out


def strength_ok(w):
    return (not w["base"]["A"] and not w["B"]["A"] and w["A"]["A"] and w["AB"]["A"] and not w["base"]["B"] and not w["A"]["B"] and w["B"]["B"] and w["AB"]["B"]
            and all(v["A_det"] and v["B_det"] for v in w.values()))


def label_from_witness(wit):
    """SOLVER A for MERGE: YES iff both suites pass on the candidate, every run deterministic and identical (3 runs); NO iff the witnesses are sound (3 identical
    runs, clean exit) and at least one suite fails. A witness that is not sound (non-identical runs, fewer than 3 runs, timeout / crash exit code) is NOT a
    label: None (the pipeline drops the row; before this fix such a witness read as NO)."""
    if not (wit["A"]["ok"] and wit["B"]["ok"] and (wit["A"].get("runs") or 0) >= S.WITNESS_RUNS and (wit["B"].get("runs") or 0) >= S.WITNESS_RUNS):
        return None
    return "YES" if (wit["A"]["passed"] and wit["B"]["passed"]) else "NO"


def witness_of(res):
    return {"passed": _passed(res), "ok": S.witness_ok(res), "runs": res.get("runs"), "states": S.test_states(res), "exit_code": res.get("exit_code"),
            "image": res.get("image")}


def build_group(ctx, g, cell):
    """cell: {cf, rks: [RK ids], ...} -> list of specs (a pair shares the conflict, tests and strength witnesses)."""
    rng = ctx.rng("merge", g["seed"])
    names = Names("T66", "%s/%s" % (ctx.seed, g["seed"]), deny_check=ctx.deny_check)
    pool = MG.Pool(names, rng)
    c = MG.build_cf(cell["cf"], pool, rng)
    ta, tb = MG.tests_for(c, c, rng)
    segs, pre, suf, region = MG.conflict_of(c)
    stem = pool.stem()
    a_name, b_name = "test_%s_a.py" % stem, "test_%s_b.py" % stem
    fnames = {}
    ta_text, tb_text = TG.suite_text(stem, ta, tag="a"), TG.suite_text(stem, tb, tag="b")
    if ta_text.count("\n") > LINES_MAX or tb_text.count("\n") > LINES_MAX:
        raise MG.Reject("side test longer than 14 lines")
    view = M3.render_view(segs)
    if M3.parse_view(view) != [(s[0],) + tuple(s[1:]) for s in segs]:
        raise MG.Reject("conflict view does not round trip")
    rid = "%s:%s" % (g["gid"], cell["cf"])
    sw = strength_witness(ctx.executor, rid, stem, c, ta_text, tb_text, a_name, b_name)
    if not strength_ok(sw):
        raise MG.Reject("strength rule failed %s" % {k: (v["A"], v["B"]) for k, v in sw.items()})
    specs = []
    for j, rk in enumerate(cell["rks"]):
        text, expect, info = MG.candidate(rk, c, c, segs, pre, suf, region, {"a": ta, "b": tb}, rng)
        ra = run_suite(ctx.executor, "%s:%s:%d:A" % (rid, rk, j), stem, text, a_name, ta_text)
        rb = run_suite(ctx.executor, "%s:%s:%d:B" % (rid, rk, j), stem, text, b_name, tb_text)
        wit = {"A": witness_of(ra), "B": witness_of(rb)}
        label = label_from_witness(wit)
        if label is None:
            raise MG.Reject("witness not usable (not 3 identical runs with a clean exit) for %s" % rk)
        if expect is not None and label != expect:
            raise MG.Reject("unexpected result for %s: %s vs %s" % (rk, label, expect))
        order_dep = None
        if rk in ("RK3", "RK4"):
            other = "RK4" if rk == "RK3" else "RK3"
            t2, _e, _i = MG.candidate(other, c, c, segs, pre, suf, region, {"a": ta, "b": tb}, rng)
            r2 = [run_suite(ctx.executor, "%s:%s:o%d:%s" % (rid, rk, j, nm), stem, t2, nm_f, tt) for nm, nm_f, tt in (("A", a_name, ta_text), ("B", b_name, tb_text))]
            order_dep = (_passed(r2[0]) and _passed(r2[1])) != (label == "YES")
        mech = {"semb": None, "order": None, "far": c["flags"].get("far") or ("high" if cell["cf"] in ("CF-3", "CF-4") else "low")}
        if rk == "RK7":
            mech["semb"] = "low" if info.get("first_failing_test") == 0 else "high"
        if rk in ("RK3", "RK4"):
            mech["order"] = "high" if order_dep else "low"
        specs.append({"head": "MERGE", "cf": cell["cf"], "rk": rk, "lang": "python", "stem": stem, "label": label, "expectation": expect, "info": info,
                      "view": view, "resolution": text, "test_a": {"name": a_name, "text": ta_text}, "test_b": {"name": b_name, "text": tb_text}, "witness": wit,
                      "strength": {m: {k: v[k] for k in ("A", "B")} for m, v in sw.items()}, "mech": mech, "conflict_id": rid})
    return specs

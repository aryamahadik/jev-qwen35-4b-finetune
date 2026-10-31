"""TFAIL2 head: will this stated test fail on this code?

Gold = the test run in the sandbox (3 runs agree). A FAIL row either states a wrong expected value (taken from the output
of a one-token mutant, so it looks plausible) or shows a program that is a one-token mutant of the code the test was
written for. The generator lint (K12) bans clocks, randomness, environment reads, filesystem outside /work and
order-dependent printing: the IR has none of those constructs by construction.
"""
from LC_COMMON import codeview as V
from LC_COMMON import ir as I
from LC_COMMON import irmut
from LC_COMMON import render as R
from LC_COMMON import sampler as SM
from LC_COMMON import transforms as T
from LC_COMMON.suites import step_ok
from LC_COMMON.interp import Interp

from . import config as C
from .base import Skip, new_base, lower, render_ok, mk_rng, variant

SHAPES = ("value", "exception", "multi", "sequence")


def _step_from_outcome(call, out):
    if out[0] == "ok":
        return {"op": "eq", "fn": call["fn"], "args": call["args"], "expect": out[1]}
    return {"op": "raises", "fn": call["fn"], "args": call["args"], "err": out[1]}


def build_steps(lo, lang, rng, shape, n_assert, scale=1):
    """Steps of one test case, with the expectations of the program itself (the PASS version)."""
    pure = [f["name"] for f in lo["funcs"] if f["scope"] == "free" and lo["meta"]["fns"].get(f["name"], {}).get("domain")]
    seq_dom = (lo["meta"].get("seq") or {}).get("domain")
    for _ in range(80):
        calls = []
        if lo["cls"] is not None and seq_dom and (shape == "sequence" or not pure):
            n = rng.randint(max(2, n_assert), 3 + n_assert)
            n = n + (scale - 1) * 2
            calls = SM.sample_sequence(seq_dom, rng, n, scale)
        else:
            if not pure:
                continue
            for _k in range(n_assert):
                f = rng.choice(pure)
                calls.append({"fn": f, "args": SM.sample_args(lo["meta"]["fns"][f]["domain"], rng, scale)})
        it = Interp(lo, lang)
        outs = []
        for c in calls:
            outs.append(it.call(c["fn"], c["args"]))
        if it.events or any(not SM.explicit_outcome(o) for o in outs):
            continue
        stateful = lo["cls"] is not None
        steps = []
        # which positions are asserted: at least one; exceptions asserted as `raises`
        exc_pos = [k for k, o in enumerate(outs) if o[0] == "exc"]
        if shape == "exception" and not exc_pos:
            continue
        if stateful:
            # state building calls must succeed unless they are the asserted exception; keep sequence valid
            if any(o[0] == "exc" for o in outs[:-1]) and shape != "exception":
                continue
            assert_pos = {len(calls) - 1} | ({exc_pos[0]} if shape == "exception" else set())
            extra = [k for k in range(len(calls) - 1) if outs[k][0] == "ok"]
            rng.shuffle(extra)
            while len(assert_pos) < n_assert and extra:
                assert_pos.add(extra.pop())
        else:
            assert_pos = set(range(len(calls)))
            if shape == "exception" and not exc_pos:
                continue
        for k, (c, o) in enumerate(zip(calls, outs)):
            steps.append(_step_from_outcome(c, o) if k in assert_pos else {"op": "do", "fn": c["fn"], "args": c["args"]})
        # a raising state-building call that is not asserted would abort the test: require all non-asserted ok
        if any(s["op"] == "do" and outs[k][0] == "exc" for k, s in enumerate(steps)):
            continue
        if not any(s["op"] != "do" for s in steps):
            continue
        if shape == "exception" and not any(s["op"] == "raises" for s in steps):
            continue
        return steps, calls, it
    raise Skip("could not build a test of shape %s" % shape)


def _outcome_at(lo, lang, calls_upto):
    outs, it = SM.run_calls(lo, lang, calls_upto)
    return outs[-1], it


def _wrong_expectation(lo, base, ids, lang, calls, k, step, rng, other_programs):
    """A plausible wrong expectation for assertion k. Sources (all drawn from outputs the program family really produces,
    so the expected literal's distribution matches the correct ones): the output of ANOTHER program (a mutant, or the
    original) on the same call, or the function's output at another input (pure functions only)."""
    true = ("ok", step["expect"]) if step["op"] == "eq" else ("exc", step["err"])
    cands = []
    for q in other_programs:
        o, it = _outcome_at(q, lang, calls[:k + 1])
        if not it.events and SM.explicit_outcome(o) and o != true:
            cands.append((o, {"kind": "other-program"}))
    if lo["cls"] is None or lo["funcs"] and I.functions(lo)[step["fn"]]["scope"] == "free":
        dom = lo["meta"]["fns"][step["fn"]]["domain"]
        for _ in range(8):
            args = SM.sample_args(dom, rng, 1)
            o, it = _outcome_at(lo, lang, [{"fn": step["fn"], "args": args}])
            if not it.events and SM.explicit_outcome(o) and o != true:
                cands.append((o, {"kind": "other-input"}))
                break
    if not cands:
        return None, None
    return rng.choice(cands)


def _mutant_programs(base, ids, lang, rng, n=6):
    out = []
    for site, mm in irmut.mutants(base, irmut.ALL_OPS, rng=rng, limit=40):
        try:
            mlo = lower(mm, lang, ids)
            render_ok(mlo, lang)
        except Skip:
            continue
        out.append((site, mm, mlo))
        if len(out) >= n:
            break
    return out


def gen_tfail2(cell, seed):
    """cell: {lang, label 'FAIL'|'PASS', shape, n_assert, bin}. The shown program is the original or a one-token mutant
    (50/50, independent of the label); the test's expectations come from the shown program (PASS) or from another program /
    another input (FAIL), so program surface and expected-literal distribution carry no label information."""
    lang, label = cell["lang"], cell["label"]
    rng = mk_rng("TFAIL2", seed, lang)
    base, ids = new_base("t%s" % seed, lang, custom_errors=False)
    lo = lower(base, lang, ids)
    render_ok(lo, lang)
    shape = cell.get("shape") or rng.choice(SHAPES)
    n_assert = cell.get("n_assert") or rng.randint(*C.ASSERTIONS_RANGE)
    if shape == "sequence" and lo["cls"] is None:
        shape = "multi"
    if shape == "exception" and not lo["errors"]:
        shape = "multi"                               # the module cannot raise: the row records the shape it really has
    muts = _mutant_programs(base, ids, lang, rng)
    use_mut = bool(muts) and rng.random() < 0.5
    if use_mut:
        site, program_base, program_lo = muts[0]
        prog_info = {"kind": "mutant", "op": site["op"]}
    else:
        program_base, program_lo, prog_info = base, lo, {"kind": "original"}
    lo_s, hi_s = SM.TIER_SCALE[cell.get("bin", "lt10")]
    steps, calls, it = build_steps(program_lo, lang, rng, shape, n_assert, rng.randint(lo_s, hi_s))
    fns = I.functions(program_lo)
    corrupted, fail_info = None, {}
    if label == "FAIL":
        asserted = [k for k, s in enumerate(steps) if s["op"] != "do"]
        rng.shuffle(asserted)
        others = [m[2] for m in muts[1:]] + ([lo] if use_mut else [])
        done = False
        for k in asserted:
            wrong, finfo = _wrong_expectation(program_lo, program_base, ids, lang, calls, k, steps[k], rng, others)
            if wrong is None:
                continue
            steps = [dict(x) for x in steps]
            s = steps[k]
            steps[k] = ({"op": "eq", "fn": s["fn"], "args": s["args"], "expect": wrong[1]} if wrong[0] == "ok"
                        else {"op": "raises", "fn": s["fn"], "args": s["args"], "err": wrong[1]})
            corrupted, fail_info, done = k, dict(finfo), True
            break
        if not done:
            raise Skip("no plausible wrong expectation")
    # spec expectation: run the shown program through the test as written
    it3 = Interp(program_lo, lang)
    verdict_pass = True
    for s in steps:
        o = it3.call(s["fn"], s["args"])
        if not step_ok(s, o):
            verdict_pass = False
    if it3.events:
        raise Skip("non-portable test run")
    if verdict_pass != (label == "PASS"):
        raise Skip("cell label disagrees with the interpreter")
    case_name = ids.var("case")
    suite = {"cases": [{"name": case_name, "steps": steps}]}
    stem = ids.var("tstem")
    path, test_text = R.render_tests(program_lo, lang, suite, stem)
    shown_blocks = V.src_blocks(program_lo, lang)
    src_text = V.src_text(shown_blocks)
    exp_lits = [V.value_text(s["expect"], fns[s["fn"]]["ret"], lang) for s in steps if s["op"] == "eq"]
    spec = {
        "head": "TFAIL2", "lang": lang, "seed": seed, "base": program_base, "base_clean": base, "ids": ids, "lo": program_lo,
        "lo_ref": lo, "steps": steps, "suite": suite, "test_path": path, "test_text": test_text, "stem": stem,
        "shown": shown_blocks, "src_text": src_text, "gold_label": label, "shape": shape, "steps_ir": it3.steps,
        "meta": {"shape": shape, "n_assert": sum(1 for s in steps if s["op"] != "do"), "stateful": lo["cls"] is not None,
                 "cdom": lo["meta"]["cdom"], "n_files": len(lo["files"]), "pair_id": None, "pair_kind": None,
                 "fail_info": fail_info, "program": prog_info, "expected_in_source": any(l in src_text for l in exp_lits),
                 "mutator_op": prog_info.get("op") or fail_info.get("op"), "corrupted": corrupted,
                 "shown_chars": len(src_text) + len(test_text)},
    }
    spec["bin_ir"] = SM.step_bin(spec["steps_ir"])
    return spec


def make_pair(spec, kind, seed):
    """Partner TFAIL2 row sharing the same module and test: 'invariant' = equivalent rewrite of the code (same gold);
    'nearmiss' = one-token mutant of the code under the SAME test (gold flips PASS -> FAIL)."""
    lang, ids = spec["lang"], spec["ids"]
    rng = mk_rng("TFAIL2pair", seed, kind)
    base = spec["base"]
    steps = spec["steps"]
    if kind == "invariant":
        names = sorted({s["fn"] for s in steps})
        rng.shuffle(names)
        for fn_name in names:
            for eq in rng.sample(list(T.IDS), len(T.IDS)):
                try:
                    nb, nlo, info = variant(base, ids, lang, fn_name, eq, rng, "tpi")
                except Skip:
                    continue
                it = Interp(nlo, lang)
                ok = True
                for s in steps:
                    o = it.call(s["fn"], s["args"])
                    if not step_ok(s, o):
                        ok = False
                if ok == (spec["gold_label"] == "PASS") and not it.events:
                    return _partner(spec, nb, nlo, "invariant", info, eq, lang)
        raise Skip("no equivalent rewrite applies")
    # nearmiss: only from a PASS row (the mutant must break the test)
    if spec["gold_label"] != "PASS":
        raise Skip("near-miss partner is defined from a PASS row")
    for site, mm in irmut.mutants(base, irmut.ALL_OPS, rng=rng, limit=80):
        try:
            mlo = lower(mm, lang, ids)
        except Skip:
            continue
        it = Interp(mlo, lang)
        bad = False
        for s in steps:
            o = it.call(s["fn"], s["args"])
            if not step_ok(s, o):
                bad = True
        if bad and not it.events:
            try:
                render_ok(mlo, lang)
            except Skip:
                continue
            return _partner(spec, mm, mlo, "nearmiss", {"kind": "mutation", "op": site["op"]}, None, lang, flip=True, op=site["op"])
    raise Skip("no mutant breaks the test")


def _partner(spec, nb, nlo, kind, info, eq, lang, flip=False, op=None):
    new = dict(spec)
    new["base"], new["lo"] = nb, nlo
    path, test_text = R.render_tests(nlo, lang, spec["suite"], spec["stem"])
    new["test_text"] = test_text
    new["shown"] = V.src_blocks(nlo, lang)
    new["src_text"] = V.src_text(new["shown"])
    if flip:
        new["gold_label"] = "FAIL" if spec["gold_label"] == "PASS" else "PASS"
    it = Interp(nlo, lang)
    for s in spec["steps"]:
        it.call(s["fn"], s["args"])
    new["steps_ir"] = it.steps
    new["bin_ir"] = SM.step_bin(it.steps)
    new["meta"] = dict(spec["meta"], pair_kind=kind, construction=eq, mutator_op=op, variant_info=info)
    return new

"""T59 check-at-generation adapter (OWNER RULE, plan 16.1 step 2). Wires the shared pipeline (tool_engine/row_pipeline.py through
LK_COMMON.kpipeline) to this family: solver A recomputed from the scene, the brute-force oracle as a second opinion, solver B (a
SEPARATE program from the solver-B session; `adapter(...)` REFUSES to build without it) on the record AND on the rendered text, the names
guard, the output lint, the token rule, the format probe, the K24 W-REPO guard, K25 observability, pair integrity (K14), A12 / A10 lever
rows (derived from kept rows, canonical-view checks, inverse and survival) and the G13 stamp boundary (`row_pipeline.StampHook`).

CODE ONLY: nothing is written, no model is called, nothing generated is executed. `run(...)` refuses to start without a stamp hook.
"""
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_ROOT, _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from LK_COMMON import kpipeline, kspec, knames  # noqa: E402
from tool_engine import render, row_pipeline as rp, util  # noqa: E402
from tool_engine.wording import WordingPool  # noqa: E402
import t59_gates as gates  # noqa: E402
import t59_generator as gen  # noqa: E402
import t59_levers as lev  # noqa: E402
import t59_oracle as orc  # noqa: E402
import t59_render as rend  # noqa: E402
import t59_repo as repo  # noqa: E402
import t59_scene as sc  # noqa: E402
import t59_solver_a as sa  # noqa: E402

FAMILY = "T59"
POOL = os.path.join(_HERE, "pools", "wording_pool_v1.json")
FORBIDDEN = tuple(list(sc.TRIGGER_IDS.values()) + list(sc.EDIT_IDS.values()) + list(sc.FORM_IDS.values()) + [
    "ctl.t59.unambiguous", "ctl.t59.settled", "ctl.t59.reversible_ambiguity", "ctl.t59.clear_ask", "ASK", "PROCEED", "swap", "lever.a12",
    "lever.a10", "split.dev_only", "view.primary", "view.with_outputs", "world.t59.tool", "world.t59.repo"])


def lint_outputs(rec):
    out = []
    for o in rec["parts"]["outputs"]:
        out.extend(render.lint_output(o))
    return out


def _has_number(text, n):
    return re.search(r"(?<![\w.-])%d(?![\w-])" % int(n), text) is not None


def observability_problems(rec):
    """K25: every decisive fact is VISIBLE in the rendered row (not only in the structured spec)."""
    scene, case, trace = rec["scene"], sc.derive_case(rec["scene"]), rec["trace"]
    H = scene["card"]["H"]
    text = rec["rendered"]["text"]
    kinds = {k for k, _ in rec["lines"]}
    probs = []
    adm = sa.admissible(case)
    if trace["rule"] == "on_irrev":
        seen = False
        for i in adm:
            for m in i["muts"]:
                e = m["eff"]
                if not sa.irrev(e, H):
                    continue
                if e["magnitude"] >= H and _has_number(text, e["magnitude"]):
                    seen = True
                elif e["external"] and ("outside the team" in text):
                    seen = True
                elif not sa.undoable(e):
                    if scene["world"] == "repo":
                        seen = seen or ("tree_state" in kinds and not scene["fx"].get("backup"))
                    else:
                        seen = seen or ("tool_undo" not in kinds)
        if not seen:
            probs.append("irreversibility_not_visible")
    if trace["rule"] == "on_reversible":
        ok = ("tool_undo" in kinds) or ("tree_state" in kinds) or any(m["eff"]["kind"] in ("create", "read") for i in adm for m in i["muts"])
        if not ok:
            probs.append("undo_evidence_not_visible")
    if trace["rule"] == "t6_331":
        # Opus ruling Q2: the two forced-ASK sub-cases rest on facts that must be visible: no key and no read path on the write (ambiguous),
        # no stated corrected value (invalid_named); the failed call's error output is what shows the error class
        d = case["t6"]
        wtxt = "\n".join(t for k, t in rec["lines"] if k == "tool_write")
        if "hist_out" not in kinds and "hist_call" not in kinds:
            probs.append("t6_failed_call_not_visible")
        if d["cls"] == "ambiguous":
            if re.search(r"\bkey\b", wtxt) or ({"tool_read_get", "tool_read_auth", "tool_read_list"} & kinds):
                probs.append("t6_key_or_read_path_visible_but_forced_ask")
        elif "user_value" in kinds:
            probs.append("t6_corrected_value_visible_but_forced_ask")
    if trace["rule"] == "robust":
        for s in case["slots"]:
            v, how = sa.collapse(s, case["defaults_count"])
            if how == "default" and "tool_write" in kinds and not re.search(r"= \S", "\n".join(t for k, t in rec["lines"] if k == "tool_write")):
                probs.append("default_not_visible")
            if how == "delegation" and "user_delegation" not in kinds:
                probs.append("delegation_not_visible")
            if how == "precedence" and "card_prec" not in kinds:
                probs.append("precedence_not_visible")
        if trace["r_res"] and not ({"tool_read_auth", "tool_read_get", "tool_read_list"} & kinds):
            probs.append("resolver_not_visible")
    return probs


def family_invariants(rec):
    """-> truthy when the row violates a family invariant (the pipeline drops it with reason 'family_invariant')."""
    why = []
    case = sc.derive_case(rec["scene"])
    if orc.oracle_label(case) != rec["gold"]:
        why.append("oracle_disagrees")
    leaks = kspec.rendered_tag_leaks(rec)
    if leaks:
        why.append("tag_rendered")
    why.extend(observability_problems(rec))
    why.extend(rend.read_path_problems(rec))                  # FU5: a read path = any listed read-only call on the target's noun
    if rec["scene"]["world"] == "repo":
        why.extend(repo.k24(rec))
    return why


def pair_check(a, b):
    g = dict(kind="swap" if (a.get("edit") == "swap") else "pair", edit=a.get("edit"))
    return gen.pair_line_problems(a, b, g)


def adapter(solver_b=None, render_b=None, allowlist=None, pool_path=POOL, a10=False, include_dev=True):
    if solver_b is None or render_b is None:
        raise kpipeline.SolverBRequired("T59: solver B and its rendered-text parser come from the solver-B session")
    al = allowlist or knames.load_allowlist()
    files = [os.path.join(_HERE, f) for f in ("t59_generator.py", "t59_build.py", "t59_scene.py", "t59_render.py", "t59_solver_a.py",
                                              "t59_wording.py", "t59_levers.py", "t59_repo.py")]
    # skeptic fix: the generator code sha of the stamp also covers what changes the TEXT of a row without touching these files
    files += [os.path.join(_HERE, "pools", "wording_pool_v1.json"), os.path.join(_ROOT, "LK_COMMON", "klevers.py")]
    holder = {}

    def extra_rows(ctx, kept):
        return lev.make_extra_rows(ctx, kept, a10=a10, include_dev=include_dev)

    def check_extra_row(h):
        why = lev.check_lever_row(h)
        if why:
            return why
        reasons, _notes = rp.check_row(kpipeline.canonical_view(h), holder["ad"])
        return reasons

    ad = kpipeline.make_adapter(
        FAMILY, gen, gold_a=sa.gold_label, solver_b=solver_b, render_b=render_b, allowlist=al, forbidden=FORBIDDEN, code_files=files,
        lint_outputs=lint_outputs, extra_checks=(lambda rec: bool(family_invariants(rec)),), pair_check=pair_check, extra_rows=extra_rows,
        check_extra_row=check_extra_row, gates=gates, pool_path=pool_path if (pool_path and os.path.isfile(pool_path)) else None,
        plan_kwargs=lambda ctx: {"a10": a10})
    holder["ad"] = ad
    ad.family_invariants = family_invariants
    return ad


def run(total, seed, stamper, solver_b=None, render_b=None, standin=False, a10=False, **kw):
    """-> (kept_rows, summary, drop_log, report). `standin=True` is for tests and the dry run only."""
    ad = adapter(solver_b, render_b, a10=a10)
    pool = WordingPool.from_json(ad.pool_path) if ad.pool_path else None
    ctx = gen.Ctx(seed=seed, standin=standin, pool=pool)
    return kpipeline.run_checked_k(ad, total, seed, stamper, standin=standin, ctx=ctx, **kw)

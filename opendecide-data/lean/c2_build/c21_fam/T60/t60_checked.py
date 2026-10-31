"""T60 check-at-generation adapter (OWNER RULE, plan 16.1 step 2). Wires the shared pipeline (tool_engine/row_pipeline.py through
LK_COMMON.kpipeline) to this family: solver A recomputed from the scene, the brute-force / ablation oracle as a second opinion, solver B (a
SEPARATE program from the solver-B session; `adapter(...)` REFUSES to build without it) on the record AND on the rendered text, the names
guard, the output lint, the token rule, the format probe, the K22 orthogonality guard for repo-shaped steps, observability, group integrity,
A12 / A10 lever rows and the G13 stamp boundary. CODE ONLY: nothing is written, no model is called, nothing generated is executed.
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
from tool_engine import render, row_pipeline as rp  # noqa: E402
from tool_engine.wording import WordingPool  # noqa: E402
import t60_build as bld  # noqa: E402
import t60_g9 as g9  # noqa: E402
import t60_gates as gates  # noqa: E402
import t60_generator as gen  # noqa: E402
import t60_levers as lev  # noqa: E402
import t60_model as M  # noqa: E402
import t60_oracle as orc  # noqa: E402
import t60_rule as rule  # noqa: E402

FAMILY = "T60"
POOL = os.path.join(_HERE, "pools", "wording_pool_v1.json")
FORBIDDEN = tuple(list(M.EDIT_IDS.values()) + list(M.HEAD_IDS.values()) + list(M.QUAD_CELLS.values()) + list(M.MARKERS) + [
    "ctl.t60.far_inside", "ctl.t60.multi_violation", "KEEP", "DROP", "DELEGATE", "DO_HERE", "PLAN", "ACT", "lever.a12", "lever.a10",
    "split.dev_only", "view.primary", "view.with_outputs"])


def lint_outputs(rec):
    out = []
    for o in rec["parts"]["outputs"]:
        out.extend(render.lint_output(o))
    return out


def _has_num(text, n):
    return re.search(r"(?<![\w.-])%s(?![\w-])" % re.escape(str(n)), text) is not None


def observability_problems(rec):
    sc, text = rec["scene"], rec["rendered"]["text"]
    probs = []
    if sc["head"] == "h1":
        c, b = sc["card"], sc["brief"]
        for v in (c["S_min"], c["V"], c["B_max"], c["R_max"], b["result_tokens"]):
            if not _has_num(text, v):
                probs.append("number_not_visible:%s" % v)
        for f in b["files"]:
            if not _has_num(text, f["tokens"]):
                probs.append("file_size_not_visible")
        if len(b["steps"]) != sum(1 for k, _ in rec["lines"] if k == "h1_step"):
            probs.append("steps_not_visible")
        for h in b["needs"]:
            if h not in text:
                probs.append("need_not_visible")
    elif sc["head"] == "h3":
        c = sc["card"]
        for v in (c["n_min"], c["H"]):
            if not _has_num(text, v):
                probs.append("number_not_visible:%s" % v)
        for s in sc["steps"]:
            if not _has_num(text, s["effect"]["magnitude"]):
                probs.append("magnitude_not_visible")
        for a, b in sc["edges"]:
            if "%s uses the output of %s" % (b, a) not in text and "%s uses a value derived from the output of %s" % (b, a) not in text:
                probs.append("edge_not_visible")
        if sc.get("order_form") == "numbered":
            if "the steps are numbered in the order in which they are to be carried out" not in text:
                probs.append("order_not_visible")
        else:
            for a, b in sc["stated_edges"]:
                if not re.search(r"step %s (?:before|has to come before) step %s|Do step %s before step %s" % (a, b, a, b), text, re.I):
                    probs.append("order_not_visible")
    else:
        q = rule.fact_by_id(sc, sc["quote"])
        if str(q["value"]) not in text:
            probs.append("quote_value_not_visible")
        star = next(s for s in sc["plan"] if s["sid"] == sc["star"])
        if "step %s" % star["sid"][1:] not in text:
            probs.append("star_step_not_visible")
    return probs


def family_invariants(rec):
    why = []
    if orc.oracle_label(rec["scene"]) != rec["gold"]:
        why.append("oracle_disagrees")
    if kspec.rendered_tag_leaks(rec):
        why.append("tag_rendered")
    why.extend(observability_problems(rec))
    sc = rec["scene"]
    if sc["head"] == "h3" and sc["world"] == "repo":
        why.extend(str(p) for p in g9.t50_step_problems(sc))
    if sc["head"] == "h2" and bld.ordinal_superseded_problems(sc):                 # Opus ruling Q6 batch 2 (B2-1): no L3 ordinal lands on a superseded record
        why.append(bld.ORDINAL_ON_SUPERSEDED)
    if sc["head"] == "h2" and sc.get("h2kind") == "supersede":                     # Opus ruling Q1: the safety net also guards the pipeline
        why.extend(bld.supersede_row_problems(sc))
        if "As a reminder" in rec["rendered"]["text"]:
            why.append("repeat_turn_on_supersede_row")
    return why


def pair_check(a, b):
    g = dict(kind="swap_card" if a.get("edit") in ("card_swap", "card_swap_recovery") else "pair", edit=a.get("edit"),
             h2kind={"pointer_content": "pointer", "card_swap_recovery": "recovery"}.get(a.get("edit"), a.get("edit")))
    return gen.group_line_problems([a, b], g)


def adapter(solver_b=None, render_b=None, allowlist=None, pool_path=POOL, a10=False, include_dev=True):
    if solver_b is None or render_b is None:
        raise kpipeline.SolverBRequired("T60: solver B and its rendered-text parser come from the solver-B session")
    al = allowlist or knames.load_allowlist()
    files = [os.path.join(_HERE, f) for f in ("t60_generator.py", "t60_build.py", "t60_model.py", "t60_render.py", "t60_rule.py",
                                              "t60_wording.py", "t60_levers.py", "t60_g9.py", "t60_levels.py", "t60_recipes.py", "t60_ballast.py")]
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
        FAMILY, gen, gold_a=rule.gold_label, solver_b=solver_b, render_b=render_b, allowlist=al, forbidden=FORBIDDEN, code_files=files,
        lint_outputs=lint_outputs, extra_checks=(lambda rec: bool(family_invariants(rec)),), pair_check=pair_check, extra_rows=extra_rows,
        check_extra_row=check_extra_row, gates=gates, pool_path=pool_path if (pool_path and os.path.isfile(pool_path)) else None,
        plan_kwargs=lambda ctx: {"a10": a10})
    holder["ad"] = ad
    ad.family_invariants = family_invariants
    return ad


def run(total, seed, stamper, solver_b=None, render_b=None, standin=False, a10=False, **kw):
    ad = adapter(solver_b, render_b, a10=a10)
    pool = WordingPool.from_json(ad.pool_path) if ad.pool_path else None
    ctx = gen.Ctx(seed=seed, standin=standin, pool=pool)
    kept, summ, log, report = kpipeline.run_checked_k(ad, total, seed, stamper, standin=standin, ctx=ctx, **kw)
    summ["family_drops"] = dict(ctx.drops)                      # creation-time drops of the generator (rows by code), e.g. supersede_same_value
    return kept, summ, log, report

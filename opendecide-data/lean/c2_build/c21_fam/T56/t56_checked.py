"""T56 (done-claim half) check-at-generation adapter (OWNER RULE, plan 16.1 step 2). Wires the shared pipeline
(tool_engine/row_pipeline.py) to this family: solver A (hidden truth) recomputed, solver B (a SEPARATE program, visible evidence
only, standard library only) on the rendered text for label, letter AND reason, the evidence-sufficiency invariant, the pair
identity rule (byte-identical claim, task statement and call skeleton), the names guard, the output lint, the token rule, the
format probe and the G13 stamp boundary. The reason-head rows (G7) are derived from KEPT rows, checked and stamped too.

CODE ONLY: nothing is written, no model is called, NO GENERATED CODE IS EXECUTED (the D3 reachability gold is symbolic; the optional
sandbox cross-check belongs to the signed-off sandbox, later). `run(...)` refuses to start without a stamp hook."""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_ROOT, _HERE, os.path.join(_HERE, "solver_b")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from tool_engine.wording import WordingPool  # noqa: E402
from tool_engine import names as names_mod, perturb, render, row_pipeline as rp  # noqa: E402
import t56_gates as gates  # noqa: E402
import t56_generator as gen  # noqa: E402
import t56_solver_a as sa  # noqa: E402
import t56_solver_b as sb  # noqa: E402
import t56_wording as tw  # noqa: E402

POOL = os.path.join(_HERE, "pools", "wording_pool_v1.json")
FORBIDDEN = (list(gen.SUB_BLOCKS) + list(perturb.FAULT_REASON) + list(perturb.DEMO_VARIANTS) +
             [r for r in perturb.REASONS if "_" in r] + ["status_is", "count_eq", "exactly_once", "view.with_outputs",
                                                         "card.t56.evidence_required", "card.t56.fresh_run_required",
                                                         "card.t56.scope_declared", "card.t56.entrypoint_reach", "DONE",
                                                         "CONTINUE", "READY", "NOT_READY"])


def _lint(rec):
    out = []
    for o in rec["parts"]["outputs"]:
        out.extend(render.lint_output(o))
    return out


def _sufficiency(rec):
    return bool(sa.evidence_sufficiency(rec))


def _pair(a, b):
    ok = a["claim"] == b["claim"] and a["task_text"] == b["task_text"]
    if a["sub_block"] != "d5_unverified":
        ok = ok and a["skeleton"] == b["skeleton"]
    return [] if ok else ["pair_identity"]


def _gold_a(rec):
    return sa.gold(rec)[0]


def _head_rows(ctx, kept):
    return gen.head_rows(ctx, [r for r in kept if not r.get("head")])


def _check_head(h):
    """A reason-head row: B's reason from the rendered text equals the head gold, and the gold option is the reason's own text."""
    res = sb.solve_text(h["rendered"]["text"])
    gold_opt = [o for o in h["options"] if o["label"] == h["gold"]]
    why = []
    if res.abstain or res.reason != h["gold"]:
        why.append("reason_differs")
    if len(gold_opt) != 1 or gold_opt[0]["letter"] != h["gold_letter"] or gold_opt[0]["text"] != tw.REASON_TEXT[h["gold"]]:
        why.append("option_integrity")
    return why


def adapter(allowlist=None, pool_path=POOL):
    al = allowlist or names_mod.AllowList.load()
    # solver B's text parser reads wordings through the SAME expanded pool the generator draws from (as data); with the seed pool
    # (pool_path=None) it runs on its keyword rules only
    sb.set_lexicon(WordingPool.from_json(pool_path).pools if pool_path else {})
    files = [os.path.join(_HERE, f) for f in ("t56_generator.py", "t56_render.py", "t56_solver_a.py", "t56_env.py", "t56_wording.py")]
    return rp.FamilyAdapter(
        "T56", gen, gold_a=_gold_a, solver_b=sb.solve, render_b=lambda r: ("abstain", sb.solve_text(r["rendered"]["text"]).abstain)
        if sb.solve_text(r["rendered"]["text"]).abstain else ("letter", sb.solve_text(r["rendered"]["text"]).letter),
        allowlist=al, lint_outputs=_lint, forbidden=FORBIDDEN, abstain_is_drop=True, extra_checks=(_sufficiency,), pair_check=_pair,
        code_files=files, compare_reason=True, extra_rows=_head_rows, check_extra_row=_check_head, gates=gates, pool_path=pool_path,
        plan_kwargs=lambda ctx: {"n_claims": len(ctx.pool.pools.get("claim.all", ())) or None})


def run(total, seed, stamper, standin=False, **kw):
    """-> (kept_rows, summary, drop_log, report). `standin=True` is for tests and the dry run only."""
    return rp.run_checked(adapter(pool_path=kw.pop("pool_path", POOL)), total, seed, stamper, standin=standin, **kw)

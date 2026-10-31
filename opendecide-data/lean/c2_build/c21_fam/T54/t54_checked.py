"""T54 check-at-generation adapter (OWNER RULE, plan 16.1 step 2). Wires the shared pipeline (tool_engine/row_pipeline.py) to this
family: solver A recomputed, solver B (a SEPARATE program, standard library only) on the record AND on the rendered text, the
names guard, the output lint, the token rule, the format probe, and the G13 stamp boundary (`row_pipeline.StampHook`).

CODE ONLY: nothing is written, no model is called, nothing generated is executed. `run(total, seed, stamper)` refuses to start
without a stamp hook. Solver B is imported HERE (glue), never by the generator or solver A."""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_ROOT, _HERE, os.path.join(_HERE, "solver_b")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from tool_engine.wording import WordingPool  # noqa: E402
from tool_engine import names as names_mod, render, row_pipeline as rp  # noqa: E402
import t54_gates as gates  # noqa: E402
import t54_generator as gen  # noqa: E402
import t54_solver_a as sa  # noqa: E402
import t54_solver_b as sb  # noqa: E402
import t54_render_b as rb  # noqa: E402

POOL = os.path.join(_HERE, "pools", "wording_pool_v1.json")
FORBIDDEN = (list(gen.SUB_BLOCKS) + ["perturb.none", "perturb.del_tool", "perturb.del_param", "perturb.del_result", "perturb.null_del",
                                     "view.primary", "view.with_outputs", "card.t54.strict_ask", "card.t54.defaults_ok",
                                     "card.t54.read_before_write", "card.t54.parallel_ok", "NO_TOOL", "DONE_NO_CALL", "READ_FIRST",
                                     "RESULT_MISSING", "UNGROUNDED", "GROUNDED", "CALL", "ASK", "ANSWER", "WRITE"])


def _lint(rec):
    out = []
    for o in rec["parts"]["outputs"]:
        out.extend(render.lint_output(o))
    return out


def _s6_unique(rec):
    """S6 / S2 uniqueness: exactly one option equals the gold after canonicalisation (the generator asserts it; re-asserted here)."""
    if rec["sub_block"] == "s6_parseq":
        want = sa.s6_canonical(rec, sa.s6_ready_nodes(rec))
        return sum(1 for o in rec["options"] if tuple(o["canon"]) == want) != 1
    if rec["sub_block"] == "s2_pick":
        return sum(1 for t in rec["tools"] if sa.satisfies(t, rec["intent"])) != 1
    return False


def _answer_has_span(rec):
    """C1: an ANSWER row has a fact id the program locates in the rendered context or card."""
    if rec["gold"] != "ANSWER":
        return False
    f = next((f for f in rec.get("facts", []) if f["fact_id"] == rec["intent"].get("answer", {}).get("fact_id")), None)
    return f is None or str(f["value"]) not in rec["rendered"]["text"]


def adapter(allowlist=None, pool_path=POOL):
    al = allowlist or names_mod.AllowList.load()
    # solver B's text parser reads wordings through the SAME expanded pool the generator draws from (as data); with the seed pool
    # (pool_path=None) it runs on its keyword rules only
    rb.set_lexicon(WordingPool.from_json(pool_path).pools if pool_path else {})
    files = [os.path.join(_HERE, f) for f in ("t54_generator.py", "t54_render.py", "t54_solver_a.py", "t54_wording.py")]
    return rp.FamilyAdapter(
        "T54", gen, gold_a=sa.gold_label, solver_b=sb.solve, render_b=lambda r: rb.solve_text(r["sub_block"], r["rendered"]["text"]),
        allowlist=al, lint_outputs=_lint, forbidden=FORBIDDEN, abstain_is_drop=False,
        extra_checks=(_s6_unique, _answer_has_span), code_files=files, gates=gates, pool_path=pool_path)


def run(total, seed, stamper, standin=False, **kw):
    """-> (kept_rows, summary, drop_log, report). `standin=True` is for tests and the dry run only."""
    return rp.run_checked(adapter(pool_path=kw.pop("pool_path", POOL)), total, seed, stamper, standin=standin, **kw)

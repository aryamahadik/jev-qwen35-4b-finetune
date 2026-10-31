"""T55 check-at-generation adapter (OWNER RULE, plan 16.1 step 2). Wires the shared pipeline (tool_engine/row_pipeline.py) to this
family: solver A recomputed, solver B (a SEPARATE program, standard library only; event-sourced ledger replay) on the record AND
the render-observability parse of the rendered text (P-10: an unobservable row is DROPPED), the names guard, the output lint
with the closed key list, the token rule, the format probe and the G13 stamp boundary.

CODE ONLY: nothing is written, no model is called, nothing generated is executed. `run(...)` refuses to start without a stamp hook."""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_ROOT, _HERE, os.path.join(_HERE, "solver_b")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from tool_engine.wording import WordingPool  # noqa: E402
from tool_engine import names as names_mod, perturb, render, row_pipeline as rp  # noqa: E402
import t55_gates as gates  # noqa: E402
import t55_generator as gen  # noqa: E402
import t55_solver_a as sa  # noqa: E402
import t55_solver_b as sb  # noqa: E402
import t55_render_b as rb  # noqa: E402

POOL = os.path.join(_HERE, "pools", "wording_pool_v1.json")
FORBIDDEN = (list(gen.SUB_BLOCKS) + list(perturb.ERROR_CLASSES) + list(perturb.VIOLATION_TYPES) + list(perturb.T55_CELLS) +
             ["view.primary", "view.with_outputs", "card.t55.retry_cap2", "card.t55.retry_cap3", "card.t55.escalate_table_ask",
              "card.t55.escalate_table_stop", "card.t55.denial_consec_total", "card.t55.denial_window", "RETRY_KEYED", "READ_BACK",
              "RETRY_PLAIN", "NO_RETRY", "FIX_ARGS", "SWITCH_TOOL", "KEEP_POLLING", "BREAK_LOOP_ALT", "CONTINUE_ALT", "RETRY_SAME",
              "ESCALATE", "ACCEPT", "STOP"])


def _lint(rec):
    extra = set()
    if rec["sub_block"] == "b3_implicit":
        extra.add(rec["b3"]["field"])
        extra.update(k for k, _v in rec["call"]["args"])
    bad = []
    for t in rec["parts"]["outputs"]:
        bad.extend(render.lint_output(t, render.OUTPUT_KEYS_T55 | extra | {"detail"}))
    return bad


def _b2_ledger(rec):
    """B2 gold must equal the five-option two-world simulation (A raises inside b2_label if not; re-asserted for the stamp)."""
    if rec["sub_block"] != "b2_ambig_write":
        return False
    f = sa.b2_facts(rec)
    return sa.b2_simulated(f["idem"], f["kf"], f["rp"], bool(f["committed"]), f["step"]) != rec["gold"]


def _b4_pair(a, b):
    if a["sub_block"] != "b4_blind_retry":
        return []
    ea, eb = a["error"], b["error"]
    same = all(ea[k] == eb[k] for k in ("group", "code", "phrase_idx", "channels")) and ea["class"] == "invalid_named_arg" \
        and eb["class"] == "invalid_unnamed" and eb.get("field") is None and bool(ea.get("field"))
    return [] if same else ["b4_pair"]


def adapter(allowlist=None, pool_path=POOL):
    al = allowlist or names_mod.AllowList.load()
    # solver B's text parser reads wordings through the SAME expanded pool the generator draws from (as data); with the seed pool
    # (pool_path=None) it runs on its keyword rules only
    rb.set_lexicon(WordingPool.from_json(pool_path).pools if pool_path else {})
    files = [os.path.join(_HERE, f) for f in ("t55_generator.py", "t55_render.py", "t55_solver_a.py", "t55_wording.py")]
    return rp.FamilyAdapter(
        "T55", gen, gold_a=sa.gold_label, solver_b=sb.solve, render_b=lambda r: rb.solve_text(r["rendered"]["text"]),
        allowlist=al, lint_outputs=_lint, forbidden=FORBIDDEN, abstain_is_drop=True, extra_checks=(_b2_ledger,),
        pair_check=_b4_pair, code_files=files, gates=gates, pool_path=pool_path)


def run(total, seed, stamper, standin=False, **kw):
    """-> (kept_rows, summary, drop_log, report). `standin=True` is for tests and the dry run only."""
    return rp.run_checked(adapter(pool_path=kw.pop("pool_path", POOL)), total, seed, stamper, standin=standin, **kw)

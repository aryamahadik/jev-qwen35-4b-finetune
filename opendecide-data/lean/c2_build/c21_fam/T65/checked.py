"""T65 check-at-generation adapter (OWNER RULE, plan 16.1 step 2). Solver A recomputed (static taint + stored canary witness), solver B plug point (a SEPARATE
program: execution harness / AST pattern engine), the render round trip, the names guard against manifest v1.2, the token rule, PII scrub, G10 n/a, the reuse
ledger and the G13 stamp boundary. A G13 hit retires the whole twin pair and its CWE head row (GV5). CODE ONLY."""
import os

from LP_COMMON import pipeline as pl
from LP_COMMON.names_guard import default_guard

from . import config as C
from . import gates, generator, roundtrip, schema, solver_a

_HERE = os.path.dirname(os.path.abspath(__file__))
CODE_FILES = [os.path.join(_HERE, f) for f in ("config.py", "templates.py", "specs.py", "generator.py", "solver_a.py", "roundtrip.py")]


def _no_permission_option(rec):
    txt = " ".join(o["text"] for o in rec["options"])
    return ["permission option"] if any(w in txt.split() for w in ("ALLOW", "ASK", "BLOCK")) else []


def adapter(solver_b=None, allowlist=None, pool_path=None):
    return pl.FamilyAdapter(
        C.FAMILY, generator, gold_a=solver_a.gold_a, solver_b=solver_b, bview=schema.b_view, roundtrip=roundtrip.check, allowlist=allowlist or default_guard(),
        forbidden=C.FORBIDDEN_IDS, extra_checks=(_no_permission_option,), require_complete_groups=True, reuse_key="reuse_group", reuse_limit=2, code_files=CODE_FILES,
        gates=gates, pool_path=pool_path, extra_rows=generator.extra_rows, check_extra_row=generator.check_cwe_row)


def run(total, seed, stamper, standin=False, executor=None, solver_b=None, **kw):
    ctx = generator.Ctx(seed=seed, standin=standin, pool_path=kw.pop("pool_path", None), executor=executor, deny_check=kw.pop("deny_check", None))
    ad = adapter(solver_b, pool_path=ctx.pool_path)
    plan = generator.build_plan(total=total, seed=seed)
    return pl.run_checked(ad, total, seed, stamper, standin=standin, ctx=ctx, plan=plan, **kw)

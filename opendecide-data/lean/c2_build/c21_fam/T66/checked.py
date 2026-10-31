"""T66 check-at-generation adapter (OWNER RULE, plan 16.1 step 2). Solver A recomputed from the stored execution witnesses / construction, solver B (a SEPARATE
program that re-executes the rendered row; plug point `solver_b`), the render round trip, the names guard against manifest v1.2, the token rule, PII scrub, the
reuse ledger (<= 4 rows per module per head, <= 6 overall) and the G13 stamp boundary. A G13 hit retires the whole conflict group / API pair / MSG module group
(GV5). CODE ONLY: nothing runs locally; every execution goes through ctx.executor (SimExecutor in tests)."""
import os

from LP_COMMON import pipeline as pl
from LP_COMMON.names_guard import default_guard

from . import config as C
from . import gates, generator, roundtrip, schema, solver_a

_HERE = os.path.dirname(os.path.abspath(__file__))
CODE_FILES = [os.path.join(_HERE, f) for f in ("config.py", "prog.py", "merge3.py", "tests_gen.py", "merge.py", "merge_spec.py", "semver.py", "semver_spec.py", "msg_spec.py",
                                                 "msg_pool.py", "rows.py", "generator.py", "solver_a.py", "roundtrip.py")] + [os.path.join(_HERE, "pools", "msg_messages.json")]


def _no_permission_option(rec):
    txt = " ".join(o["text"] for o in rec["options"])
    return ["permission option"] if any(w in txt.split() for w in ("ALLOW", "ASK", "BLOCK")) else []


def adapter(solver_b=None, allowlist=None, pool_path=None):
    return pl.FamilyAdapter(
        C.FAMILY, generator, gold_a=solver_a.gold_a, solver_b=solver_b, bview=schema.b_view, roundtrip=roundtrip.check, allowlist=allowlist or default_guard(),
        forbidden=C.FORBIDDEN_IDS, extra_checks=(_no_permission_option,), require_complete_groups=True, reuse_key="reuse_group", reuse_limit=C.REUSE_PER_MODULE,
        code_files=CODE_FILES, gates=gates, pool_path=pool_path)


def run(total, seed, stamper, standin=False, executor=None, solver_b=None, **kw):
    ctx = generator.Ctx(seed=seed, standin=standin, pool_path=kw.pop("pool_path", None), executor=executor, deny_check=kw.pop("deny_check", None),
                        msg_split=kw.pop("msg_split", None), msg_pool=kw.pop("msg_pool", None))
    ad = adapter(solver_b, pool_path=ctx.pool_path)
    plan = generator.build_plan(total=total, seed=seed)
    return pl.run_checked(ad, total, seed, stamper, standin=standin, ctx=ctx, plan=plan, **kw)

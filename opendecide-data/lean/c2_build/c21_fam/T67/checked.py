"""T67 check-at-generation adapter (OWNER RULE, plan 16.1 step 2): wires the shared L-P pipeline to this family. Solver A recomputed, solver B (a SEPARATE
program; plug point `solver_b`), the render round trip (validators + engine on the reconstructed spec + GV12 naming check), the names guard against manifest
v1.2, the token rule, PII scrub (fixed CIDR literals and documentation hosts allowed), G10 decision spans, the A1 / A2 hook fields and the G13 stamp
boundary. Head rows (reason / tier) come from KEPT single-trigger rows after the primary rows. CODE ONLY."""
import os

from LP_COMMON import pipeline as pl
from LP_COMMON.names_guard import default_guard

from . import config as C
from . import gates, generator, heads, roundtrip, schema, solver_a

_HERE = os.path.dirname(os.path.abspath(__file__))
CODE_FILES = [os.path.join(_HERE, f) for f in ("config.py", "engine.py", "sqlmodel.py", "items.py", "builders.py", "render.py", "yamlio.py", "userturn.py", "rows.py",
                                                 "generator.py", "cards.py", "solver_a.py", "roundtrip.py", "heads.py")]
FORBIDDEN = (["T67-Q-GATE", "T67-Q-REASON", "T67-Q-TIER", "T67-U-NEITHER", "T67-U-OP", "T67-U-TARGET", "T67-U-BOTH", "T67-LOCK-TABLE"] +
             ["X%02d" % i for i in range(1, 12)] + ["M01", "M02", "LC0", "LC1", "LC2"] + ["MG-S%d" % i for i in range(1, 16)] +
             ["M-HIDE", "M-REPL", "M-INDIR", "M-SIZE", "M-FORM", "M-LANE", "NEW-PC", "card.t67.c01", "card.t67.c02", "card.t67.c03", "card.t67.c04",
              "card.t67.c05", "card.t67.c06"])
PII_ALLOW = [r"0\.0\.0\.0/0", r"::/0", r"\b(?:10\.0\.0\.0/8|172\.16\.0\.0/12|192\.168\.0\.0/16|10\.1\.0\.0/16)\b",
             r"https://[a-z0-9.-]+\.(?:example|test|invalid)(?:/[\w./-]*)?"]


def adapter(lock_table, solver_b=None, allowlist=None, pool_path=None):
    def rt(rec):
        return roundtrip.check(rec, lock_table)
    return pl.FamilyAdapter(
        C.FAMILY, generator, gold_a=solver_a.make_gold_a(lock_table), solver_b=solver_b, bview=schema.b_view, roundtrip=rt,
        allowlist=allowlist or default_guard(), forbidden=FORBIDDEN, extra_checks=(), pii_allow=PII_ALLOW, require_complete_groups=True,
        reuse_key=None, reuse_limit=None, code_files=CODE_FILES, gates=gates, pool_path=pool_path, extra_rows=heads.extra_rows,
        check_extra_row=heads.check_head_row, needs_spans=True)


def run(total, seed, stamper, standin=False, lock_table=None, solver_b=None, **kw):
    ctx = generator.Ctx(seed=seed, standin=standin, pool_path=kw.pop("pool_path", None), lock_table=lock_table, deny_check=kw.pop("deny_check", None))
    ad = adapter(ctx.lock_table, solver_b, pool_path=ctx.pool_path)
    plan = generator.build_plan(total=total, seed=seed)
    return pl.run_checked(ad, total, seed, stamper, standin=standin, ctx=ctx, plan=plan, **kw)

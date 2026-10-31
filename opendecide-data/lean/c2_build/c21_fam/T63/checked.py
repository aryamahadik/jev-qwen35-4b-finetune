"""T63 check-at-generation adapter (OWNER RULE, plan 16.1 step 2): wires the shared L-P pipeline (LP_COMMON/pipeline.py) to this family.
Solver A recomputed, solver B (a SEPARATE program; plug point `solver_b`), the render round trip, the names guard against manifest v1.2,
the token rule, PII scrub, the reuse ledger (<= 3 rows per snapshot / history) and the G13 stamp boundary.

CODE ONLY: nothing is written, no model is called. `run(...)` refuses to start without a stamp hook, and a production run (standin=False)
without a solver B is refused."""
import os

from LP_COMMON import pipeline as pl
from LP_COMMON.names_guard import default_guard

from . import config as C
from . import gates, generator, lic, roundtrip, schema, solver_a

_HERE = os.path.dirname(os.path.abspath(__file__))
CODE_FILES = [os.path.join(_HERE, f) for f in ("config.py", "near.py", "near_build.py", "near_plan.py", "exists.py", "lic.py", "render.py",
                                                 "rows.py", "generator.py", "solver_a.py", "roundtrip.py", "lic_format.py")]


def _no_permission_option(rec):
    txt = " ".join(o["text"] for o in rec["options"])
    return ["permission option"] if any(w in txt.split() for w in ("ALLOW", "ASK", "BLOCK")) else []


def adapter(exports=None, table=None, solver_b=None, allowlist=None, pool_path=None):
    return pl.FamilyAdapter(
        C.FAMILY, generator, gold_a=solver_a.make_gold_a(exports, table), solver_b=solver_b, bview=schema.b_view, roundtrip=roundtrip.check,
        allowlist=allowlist or default_guard(), forbidden=C.FORBIDDEN_IDS, extra_checks=(_no_permission_option,), reuse_key="reuse_group",
        reuse_limit=C.REUSE_PER_GROUP, code_files=CODE_FILES, gates=gates, pool_path=pool_path)


class KeptTracker(pl.StampHook):
    """Wraps the stamp hook and remembers every verdict, so that a refill round can tell which rows of the EARLIER rounds really entered the pool (Opus ruling Q5: the cell of a
    dropped row is released). A row is kept iff it reached the stamp (it passed every answer check), its verdict is clean and so is every verdict of its group (a hit or an error
    retires the whole group). A row the tracker cannot prove dropped counts as kept: its cell is never handed out twice."""

    def __init__(self, inner, ctx):
        self.inner, self.ctx, self.verdicts = inner, ctx, {}

    @property
    def registry_sha(self):
        return getattr(self.inner, "registry_sha", None)

    @property
    def method_set_version(self):
        return getattr(self.inner, "method_set_version", None)

    def stamp(self, items):
        res = self.inner.stamp(items)
        if isinstance(res, dict):
            self.verdicts.update(res)
        return res

    def kept_row_ids(self):
        group_of = {rid: g for rid, (g, _c, _r) in self.ctx.cells.rows.items()}
        bad = {group_of[rid] for rid, v in self.verdicts.items() if rid in group_of and pl.verdict_class(v) != "clean"}
        return {rid for rid, g in group_of.items() if rid in self.verdicts and pl.verdict_class(self.verdicts[rid]) == "clean" and g not in bad}


def cut_lic(rows, seed, total=C.GENERATED_ROWS):
    """Opus ruling Q5: cut the surviving LIC rows to the kept quota for a `total`-row family (38 / 38 / 34 at 1,200; 55 rows at the 600-row pilot), singles first, deterministic
    per seed (`lic.cut_to_quota`). Other heads are returned unchanged. -> (rows, report)."""
    quota = generator.lic_quota(total, oversample=False)["kept"]
    lic_rows = [r for r in rows if r["head"] == "LIC"]
    kept, report = lic.cut_to_quota(lic_rows, seed, quota)
    keep_ids = {r["row_id"] for r in kept}
    return [r for r in rows if r["head"] != "LIC" or r["row_id"] in keep_ids], report


def run(total, seed, stamper, standin=False, exports=None, table=None, solver_b=None, **kw):
    """-> (kept_rows, summary, drop_log, report). `standin=True` is for tests and the dry run only. The LIC rows returned are those that survived the drops (up to the oversampled
    draw): apply `cut_lic` before writing the pool."""
    ad = adapter(exports, table, solver_b, pool_path=kw.pop("pool_path", None))
    ctx = generator.Ctx(seed=seed, standin=standin, pool_path=ad.pool_path, exports=exports, table=table, deny_check=kw.pop("deny_check", None))
    plan = generator.build_plan(total=total, seed=seed, with_b=exports is not None)
    if ctx.cells is not None and stamper is not None and not isinstance(stamper, pl.RefusingHook):
        stamper = KeptTracker(stamper, ctx)
        ctx.kept_row_ids = stamper.kept_row_ids
    return pl.run_checked(ad, total, seed, stamper, standin=standin, ctx=ctx, plan=plan, **kw)

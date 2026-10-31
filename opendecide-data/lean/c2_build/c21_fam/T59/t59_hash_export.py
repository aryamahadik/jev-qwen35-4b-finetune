"""T59 template / wording-pool HASH EXPORT (hashes only, no text). Run: python3 -I t59_hash_export.py (writes HASH_EXPORT.json and
HASH_EXPORT.sha256 in this folder). Any later change to a template, a pool, a table or a rendering / solver file = a new export and a
re-stamp of the affected rows (plan 16.1 step 6). The A10 / A12 wrapper and transform pools are exported in every case (GV1)."""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_ROOT, _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from LK_COMMON import klevers, knames  # noqa: E402
from tool_engine import hash_export as hx, names as names_mod, state  # noqa: E402
import t59_build as bld  # noqa: E402
import t59_generator as gen  # noqa: E402
import t59_render as rd  # noqa: E402
import t59_scene as sc  # noqa: E402
import t59_solver_a as sa  # noqa: E402
import t59_wording as tw  # noqa: E402

FAMILY = "T59"
LK = os.path.join(_ROOT, "LK_COMMON")


def build(created=None):
    code = [os.path.join(_HERE, f) for f in ("t59_generator.py", "t59_build.py", "t59_scene.py", "t59_render.py", "t59_solver_a.py",
                                             "t59_oracle.py", "t59_wording.py", "t59_levers.py", "t59_repo.py", "t59_gates.py",
                                             "t59_checked.py", "t59_g9.py", "pools/build_pools.py")]
    extra = [os.path.join(LK, f) for f in ("klevers.py", "knames.py", "kpipeline.py", "kround.py", "kspec.py")]
    # Opus ruling Q2 follow-up FU3 / FU1: the solver-B contract (ROW_SCHEMA.md) and the generator notes that record the quota weights are hashed too
    extra += [os.path.join(_HERE, f) for f in ("ROW_SCHEMA.md", "NOTES.md")]
    tables = {}
    for pref, mod in (("gen", gen), ("build", bld), ("scene", sc), ("sa", sa), ("wording", tw), ("render", rd), ("state", state),
                      ("klevers", klevers)):
        tables.update(hx.module_tables(pref, mod))
    pools = os.path.join(_HERE, "pools")
    return hx.build_export(
        FAMILY, _HERE, os.path.join(_ROOT, "tool_engine"), code, [], tables, os.path.join(pools, "wording_pool_v1.json"),
        os.path.join(pools, "pool_manifest.json"), tw.seed_pool().pools,
        [knames.MANIFEST_V12, os.path.join(names_mod.INFRA_DIR, "namespace.py")], extra_files=extra, created=created)


if __name__ == "__main__":
    exp = build()
    hx.assert_no_text(exp)
    print(FAMILY, "export_sha256", exp["export_sha256"], "file_sha256", hx.write_export(os.path.join(_HERE, "HASH_EXPORT.json"), exp))

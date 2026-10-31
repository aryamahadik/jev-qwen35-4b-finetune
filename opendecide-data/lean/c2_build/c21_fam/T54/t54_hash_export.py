"""T54 template / wording-pool HASH EXPORT (hashes only, no text). Run: python3 -I t54_hash_export.py  (writes HASH_EXPORT.json and
HASH_EXPORT.sha256 in this folder). Any later change to a template, a pool, a table or a rendering/solver file = a new export and a
re-stamp of the affected rows (plan 16.1 step 6)."""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_ROOT, _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from tool_engine import hash_export as hx, invariants, names as names_mod, perturb, state  # noqa: E402
import t54_generator as gen  # noqa: E402
import t54_render as rd  # noqa: E402
import t54_solver_a as sa  # noqa: E402
import t54_wording as tw  # noqa: E402

FAMILY = "T54"


def build(created=None):
    code = [os.path.join(_HERE, f) for f in ("t54_generator.py", "t54_render.py", "t54_solver_a.py", "t54_wording.py", "t54_gates.py",
                                             "t54_checked.py", "pools/build_pools.py")]
    sbdir = os.path.join(_HERE, "solver_b")
    solver_b = [os.path.join(sbdir, f) for f in ("t54_solver_b.py", "t54_render_b.py")]
    tables = {}
    for pref, mod in (("gen", gen), ("sa", sa), ("wording", tw), ("render", rd), ("state", state), ("perturb", perturb)):
        tables.update(hx.module_tables(pref, mod))
    pools = os.path.join(_HERE, "pools")
    return hx.build_export(
        FAMILY, _HERE, os.path.join(_ROOT, "tool_engine"), code, solver_b, tables, os.path.join(pools, "wording_pool_v1.json"),
        os.path.join(pools, "pool_manifest.json"), tw.seed_pool().pools,
        [names_mod.MANIFEST_DEFAULT, os.path.join(names_mod.INFRA_DIR, "namespace.py")], created=created)


if __name__ == "__main__":
    exp = build()
    hx.assert_no_text(exp)
    print(FAMILY, "export_sha256", exp["export_sha256"], "file_sha256", hx.write_export(os.path.join(_HERE, "HASH_EXPORT.json"), exp))

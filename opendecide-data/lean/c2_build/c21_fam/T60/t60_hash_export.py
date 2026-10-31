"""T60 template / wording-pool HASH EXPORT (hashes only, no text). Run: python3 -I t60_hash_export.py (writes HASH_EXPORT.json and
HASH_EXPORT.sha256 in this folder). Any later change to a template, a pool, a table or a rendering / solver file = a new export and a re-stamp of
the affected rows (plan 16.1 step 6). The A10 / A12 wrapper and transform pools are exported in every case (GV1)."""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (_ROOT, _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from LK_COMMON import klevers, knames  # noqa: E402
from tool_engine import hash_export as hx, names as names_mod, state, util  # noqa: E402
import t60_ballast as bl  # noqa: E402
import t60_build as bld  # noqa: E402
import t60_generator as gen  # noqa: E402
import t60_levels as lv  # noqa: E402
import t60_model as M  # noqa: E402
import t60_recipes as rc  # noqa: E402
import t60_render as rd  # noqa: E402
import t60_rule as rule  # noqa: E402
import t60_wording as tw  # noqa: E402

FAMILY = "T60"
LK = os.path.join(_ROOT, "LK_COMMON")


def build(created=None):
    code = [os.path.join(_HERE, f) for f in ("t60_generator.py", "t60_build.py", "t60_model.py", "t60_render.py", "t60_rule.py", "t60_oracle.py",
                                             "t60_wording.py", "t60_levers.py", "t60_gates.py", "t60_checked.py", "t60_g9.py", "t60_levels.py",
                                             "t60_recipes.py", "t60_ballast.py", "pools/build_pools.py")]
    extra = [os.path.join(LK, f) for f in ("klevers.py", "knames.py", "kpipeline.py", "kround.py", "kspec.py")]
    tables = {}
    for pref, mod in (("gen", gen), ("build", bld), ("model", M), ("rule", rule), ("wording", tw), ("render", rd), ("state", state), ("klevers", klevers),
                      ("levels", lv), ("recipes", rc)):
        tables.update(hx.module_tables(pref, mod))
    # the background-notes vocabulary is wording: exported as a hash only (hash_export carries no text)
    tables["ballast.vocab_sha256"] = util.sha256_text(util.canon_json([bl.SUBJ, bl.VERB, bl.OBJ, bl.WHEN, bl.TAIL, bl.LABEL, bl.SENT_PER_LINE]))
    pools = os.path.join(_HERE, "pools")
    return hx.build_export(
        FAMILY, _HERE, os.path.join(_ROOT, "tool_engine"), code, [], tables, os.path.join(pools, "wording_pool_v1.json"),
        os.path.join(pools, "pool_manifest.json"), tw.seed_pool().pools,
        [knames.MANIFEST_V12, os.path.join(names_mod.INFRA_DIR, "namespace.py")], extra_files=extra, created=created)


if __name__ == "__main__":
    exp = build()
    hx.assert_no_text(exp)
    print(FAMILY, "export_sha256", exp["export_sha256"], "file_sha256", hx.write_export(os.path.join(_HERE, "HASH_EXPORT.json"), exp))

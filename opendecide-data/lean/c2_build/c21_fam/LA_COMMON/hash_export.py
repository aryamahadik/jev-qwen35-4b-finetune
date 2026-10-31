"""TEMPLATE / WORDING-POOL HASH EXPORT for the L-A families (T50, T51, T53). HASHES ONLY, NO TEXT (plan 16.1: "any later change
= a new export + re-stamp of the affected rows"). Same format and helpers as the L-T families (tool_engine/hash_export.py), so the
stamp service reads one shape.

Run (from anywhere):  python3 -I c21_fam/LA_COMMON/hash_export.py [T50 T51 T53]
It writes c21_fam/<family>/HASH_EXPORT.json and HASH_EXPORT.sha256. It reads code, the wording pool file and the names manifest;
it writes nothing else and builds no row.

What is hashed (sha256):
  * code: every .py file of LA_COMMON and of the family folder (not tests, not solver B);
  * solver_b: the family's solver B files and its agreement log; tests: every test file;
  * tables: the family's own template hashes (tNN_hashes(): rule table, resolver list, payload registry, intent registry,
    block plan, card levers, operators, forms) and the pool-requirements spec;
  * the wording pool: file, pool as a whole, per form its sha, its wording count and the sha256 of each template string
    (UTF-8, {slot} fields kept); per lexicon id the same;
  * names: NAMES_MANIFEST_V1.json and its pinned sha file, namespace.py, row_start_guard.py, the training fingerprint;
  * export_sha256 over everything above.
"""
import datetime
import glob
import hashlib
import importlib
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_FAM = os.path.dirname(_HERE)
_BUILD = os.path.dirname(_FAM)
for _p in (_FAM, os.path.join(_BUILD, "c21_infra")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from LA_COMMON import MANIFEST_PATH, MANIFEST_SHA_PATH  # noqa: E402
from LA_COMMON.canon import sha_obj  # noqa: E402
from LA_COMMON.names import get_allowlist  # noqa: E402
from tool_engine import hash_export as hx  # noqa: E402

FAMILIES = ("T50", "T51", "T53")
HASH_FN = {"T50": ("T50.hashes", "t50_hashes"), "T51": ("T51.hashes", "t51_hashes"), "T53": ("T53.hashes", "t53_hashes")}


def _sha_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def _py(folder):
    return sorted(p for p in glob.glob(os.path.join(folder, "*.py")))


def _rel(path):
    return os.path.relpath(path, _FAM).replace(os.sep, "/")


def _lexicon_block(lex):
    out = {}
    for lid in sorted(lex):
        out[lid] = {"count": len(lex[lid]), "lex_sha256": sha_obj(lex[lid]),
                    "surface_sha256": [hashlib.sha256(w.encode("utf-8")).hexdigest() for w in lex[lid]]}
    return out


def build(family, created=None):
    if family not in FAMILIES:
        raise ValueError("family %r is not an L-A family" % family)
    fam_dir = os.path.join(_FAM, family)
    mod, fn = HASH_FN[family]
    template = getattr(importlib.import_module(mod), fn)()
    from LA_COMMON import pool_spec
    from LA_COMMON.wording import WordingPool
    pool_path = os.path.join(fam_dir, "pools", "%s_wording_pool_v1.json" % family)
    with open(pool_path, "r", encoding="utf-8") as f:
        pool_json = json.load(f)
    pool = WordingPool(pool_json)
    req = pool_spec.pool_requirements()
    fam_forms = {k: v for k, v in req["forms"].items() if v["family"] == family}
    missing = [k for k in fam_forms if k not in pool.forms]
    if missing:
        raise ValueError("pool lacks forms %s" % missing[:5])
    pb = hx._pool_block(pool.forms)
    pb.update({"pool_sha256": pool.sha, "file": _rel(pool_path), "file_sha256": _sha_file(pool_path),
               "lexicon": _lexicon_block(pool.lexicon), "is_stub": bool(pool.is_stub)})
    sb_dir = os.path.join(fam_dir, "solver_b")
    tests = sorted(glob.glob(os.path.join(_HERE, "tests", "*.py")) + glob.glob(os.path.join(fam_dir, "tests", "*.py"))
                   + glob.glob(os.path.join(sb_dir, "tests", "*.py")))
    exp = {
        "export": "%s template and wording-pool hash export" % family,
        "family": family,
        "version": hx.EXPORT_VERSION,
        "created_utc": created or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        **hx.META,
        "code": {_rel(p): _sha_file(p) for p in _py(_HERE) + _py(fam_dir)},
        "solver_b": {_rel(p): _sha_file(p) for p in _py(sb_dir) + [os.path.join(sb_dir, "agreement_log.json")]},
        "tests": {_rel(p): _sha_file(p) for p in tests},
        "tables": dict(sorted(template.items()), pool_requirements=req["sha256"],
                       family_forms=sha_obj(fam_forms)),
        "wording_pool": pb,
        "names": {os.path.basename(MANIFEST_PATH): _sha_file(MANIFEST_PATH), os.path.basename(MANIFEST_SHA_PATH): _sha_file(MANIFEST_SHA_PATH),
                  "namespace.py": _sha_file(os.path.join(_BUILD, "c21_infra", "namespace.py")),
                  "row_start_guard.py": _sha_file(os.path.join(_BUILD, "c21_infra", "row_start_guard.py")),
                  "training_fingerprint": get_allowlist().training_fingerprint},
    }
    exp["export_sha256"] = hx._sha_obj(exp)
    return exp


def main(argv=None):
    fams = list(argv if argv else FAMILIES)
    for fam in fams:
        exp = build(fam)
        hx.assert_no_text(exp)
        path = os.path.join(_FAM, fam, "HASH_EXPORT.json")
        print(fam, "export_sha256", exp["export_sha256"], "file_sha256", hx.write_export(path, exp))


if __name__ == "__main__":
    main(sys.argv[1:])

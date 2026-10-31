"""TEMPLATE / WORDING-POOL HASH EXPORT for the L-P families (T63, T65, T66, T67). HASHES ONLY, NO TEXT (plan 16.1: "any later change = a new export + re-stamp of the
affected rows"). Same shape and helpers as the L-A / L-T exports (tool_engine/hash_export.py), so the stamp service reads one format.

Run (from anywhere):  python3 -I c21_fam/LP_COMMON/hash_export.py [T63 T65 T66 T67]      (writes c21_fam/<family>/HASH_EXPORT.json and HASH_EXPORT.sha256)
It reads code, the wording pool file and the names manifest; it writes nothing else and builds no row.

What is hashed (sha256):
  * code: every .py file of LP_COMMON and of the family folder (not tests); code_combined_sha256 = sha256 of the file shas in path order (the rule of SHAS.json);
  * solver_b: the family's solver B files (none exist yet: `solver_b_status` says "absent"; the export of the family is NOT final until solver B lands and the
    export is rewritten); tests: every test file of LP_COMMON and of the family; docs: ROW_SCHEMA.md and the README;
  * tables: every UPPER_CASE plain-data constant of every family module and of the shared helpers that decide or render a row (definitions blocks, closed
    vocabularies, plan cells, rule tables, option texts, question-form slots, payload registry ...) as canonical JSON, one sha256 per constant;
  * the wording pool: file, pool as a whole, per form its sha, its wording count and the sha256 of each template string (UTF-8, {slot} fields kept);
  * names: NAMES_MANIFEST_V1_2.json and its pinned sha file, namespace.py, row_start_guard.py, the training namespace fingerprint;
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

from LP_COMMON import paths, util  # noqa: E402
from tool_engine import hash_export as hx  # noqa: E402

FAMILIES = ("T63", "T65", "T66", "T67")
SHARED_TABLE_MODULES = ("LP_COMMON.plan", "LP_COMMON.pipeline", "LP_COMMON.sandbox_iface", "LP_COMMON.tokens", "LP_COMMON.gates", "LP_COMMON.wording")


def _sha_file(path):
    return util.sha256_file(path)


def _py(folder):
    return sorted(glob.glob(os.path.join(folder, "*.py")))


def _rel(path):
    return os.path.relpath(path, _FAM).replace(os.sep, "/")


def _pool_forms(pool_json):
    return {form: [w["text"] for w in ws] for form, ws in pool_json["forms"].items()}


def _tables(family, fam_dir):
    out = {}
    mods = list(SHARED_TABLE_MODULES)
    for p in _py(fam_dir):
        name = os.path.splitext(os.path.basename(p))[0]
        if name not in ("__init__", "dryrun"):
            mods.append("%s.%s" % (family, name))
    for m in mods:
        try:
            mod = importlib.import_module(m)
        except Exception as e:                                       # noqa: BLE001 - an unimportable module is a hard export error, never skipped silently
            raise RuntimeError("cannot import %s for the table hash: %s" % (m, type(e).__name__))
        out.update(hx.module_tables(m, mod))
    return {k: hx._sha_obj(v) for k, v in sorted(out.items())}


def _combined(files):
    h = hashlib.sha256()
    for p in sorted(files, key=_rel):
        h.update(_sha_file(p).encode("ascii"))
    return h.hexdigest()


def build(family, created=None):
    if family not in FAMILIES:
        raise ValueError("family %r is not an L-P family" % family)
    fam_dir = os.path.join(_FAM, family)
    pool_path = os.path.join(fam_dir, "pools", "wording_pool.json")
    with open(pool_path, "r", encoding="utf-8") as f:
        pool_json = json.load(f)
    pb = hx._pool_block(_pool_forms(pool_json))
    pb.update({"file": _rel(pool_path), "file_sha256": _sha_file(pool_path), "is_stub": bool(pool_json.get("test_only", True))})
    code_files = _py(_HERE) + _py(fam_dir)
    solver_b = sorted(glob.glob(os.path.join(fam_dir, "solver_b", "*.py")))
    tests = sorted(glob.glob(os.path.join(_HERE, "tests", "*.py")) + glob.glob(os.path.join(fam_dir, "tests", "*.py")))
    docs = [p for p in (os.path.join(fam_dir, "ROW_SCHEMA.md"), os.path.join(_HERE, "README.md")) if os.path.exists(p)]
    from namespace import NameSpace
    exp = {
        "export": "%s template and wording-pool hash export" % family,
        "family": family,
        "version": hx.EXPORT_VERSION,
        "created_utc": created or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        **hx.META,
        "code": {_rel(p): _sha_file(p) for p in code_files},
        "code_combined_sha256": _combined(code_files),
        "solver_b": {_rel(p): _sha_file(p) for p in solver_b},
        "solver_b_status": "present" if solver_b else "absent",
        "tests": {_rel(p): _sha_file(p) for p in tests},
        "docs": {_rel(p): _sha_file(p) for p in docs},
        "tables": _tables(family, fam_dir),
        "wording_pool": pb,
        "names": {os.path.basename(paths.NAMES_MANIFEST): _sha_file(paths.NAMES_MANIFEST), os.path.basename(paths.NAMES_MANIFEST_SHA): _sha_file(paths.NAMES_MANIFEST_SHA),
                  "namespace.py": _sha_file(os.path.join(paths.INFRA, "namespace.py")), "row_start_guard.py": _sha_file(os.path.join(paths.INFRA, "row_start_guard.py")),
                  "training_fingerprint": NameSpace("training", "export-fingerprint").fingerprint()},
    }
    exp["export_sha256"] = hx._sha_obj(exp)
    return exp


def main(argv=None):
    fams = list(argv if argv else FAMILIES)
    for fam in fams:
        exp = build(fam)
        hx.assert_no_text(exp)
        path = os.path.join(_FAM, fam, "HASH_EXPORT.json")
        print(fam, "export_sha256", exp["export_sha256"], "file_sha256", hx.write_export(path, exp), "code_combined", exp["code_combined_sha256"])


if __name__ == "__main__":
    main(sys.argv[1:])

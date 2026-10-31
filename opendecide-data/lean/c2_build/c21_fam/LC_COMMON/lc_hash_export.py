"""TEMPLATE / WORDING-POOL HASH EXPORT for the L-C families T42c, T57 and T56g (plan 16.1: "every template, wording pool ... is in the
export; any later change = a new export + re-stamp of the affected rows"). HASHES ONLY, NO TEXT: every string value is a sha256 hex digest,
a file path, a form id or a fixed metadata word (checked by `assert_no_text`). It writes no row and reads none.

Run:  cd c21_fam && python3 -m LC_COMMON.lc_hash_export T42c      (writes <FAM>/HASH_EXPORT.json and HASH_EXPORT.sha256)

What is hashed (sha256), in the layout of the other families' exports (tool_engine/hash_export.py):
  code        every generator-side .py file of the family plus ROW_SCHEMA.md (tests, pools, solver_b excluded);
  engine      every shared LC_COMMON .py file (module generator, IR, renderers, mutator, transforms, suites, wording, checker ...);
  solver_b    the family's solver B files and the shared LC_SOLVER_B engine;
  tables      the module-level CONSTANTS (config, operator registries, closed exception lists, reserved words, lint patterns, default
              question sentences ...) as canonical JSON;
  wording_pool  the pool file, the pool as a whole, and for every form its own sha, its wording count, the sha of the id list and the
              sha of each template string (UTF-8 bytes, {slot} fields kept);
  seed_pool   the program-rendered question sentences of the heads (the part of the question text that is not in the pool);
  names       the frozen names allow-list and its pin, and namespace.py (so a names change shows).
A wording hash is a plain sha256 of the template string.
"""
import datetime
import hashlib
import importlib
import json
import os
import sys

from . import paths
from tool_engine import hash_export as hx
from tool_engine import util

FAM_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAMILIES = {
    "T42c": {"tables": ["config", "rows", "out4", "eqv2", "tfail2", "planner"], "forms": "QUESTION_FORM"},
    "T57": {"tables": ["config", "rows", "task", "facts"], "forms": None},
    "T56g": {"tables": ["config", "rows", "hacks", "natural"], "forms": None},
}
ENGINE_TABLES = ["atoms", "modgen", "irmut", "transforms", "idents", "lint", "codeview", "render", "render_py", "render_js", "render_go",
                 "render_sh", "render_base", "domain", "sampler", "interp", "ir", "domdriver", "sandbox_iface", "wording"]


def _py_files(base, skip=("__pycache__", "tests", "solver_b", "pools")):
    out = []
    for dp, dn, fn in os.walk(base):
        dn[:] = sorted(d for d in dn if d not in skip)
        out += [os.path.join(dp, f) for f in sorted(fn) if f.endswith(".py")]
    return out


def _seed_pool(family, rows_mod):
    ask = getattr(rows_mod, "DEFAULT_ASK", None) or getattr(rows_mod, "ASK", None)
    if isinstance(ask, str):
        return {family + "-Q-HACK": [ask]}
    seed = {}
    for head, text in sorted(ask.items()):
        form = {"REASON": "T57-Q-VERDICT-REASON"}.get(head, "%s-Q-%s" % (family, head))
        seed[form] = [text]
    return seed


def build(family, created=None, root=FAM_ROOT):
    spec = FAMILIES[family]
    fam_dir = os.path.join(root, family)
    rel = lambda p: os.path.relpath(p, root).replace(os.sep, "/")           # noqa: E731
    code = _py_files(fam_dir) + [os.path.join(fam_dir, "ROW_SCHEMA.md")]
    engine = _py_files(os.path.join(root, "LC_COMMON"))
    solver_b = _py_files(os.path.join(fam_dir, "solver_b"), skip=("__pycache__", "tests")) + _py_files(os.path.join(root, "LC_SOLVER_B"), skip=("__pycache__", "tests"))
    tables = {}
    for m in spec["tables"]:
        tables.update(hx.module_tables("fam_" + m, importlib.import_module("%s.%s" % (family, m))))
    for m in ENGINE_TABLES:
        tables.update(hx.module_tables("lc_" + m, importlib.import_module("LC_COMMON." + m)))
    pool_file = os.path.join(fam_dir, "pools", "%s_wording_pool_v1.json" % family)
    with open(pool_file, "r", encoding="utf-8") as f:
        pool = json.load(f)
    if pool.get("test_only"):
        raise ValueError("a TEST-ONLY wording pool cannot be exported")
    forms = {form: [w["text"] for w in ws] for form, ws in pool["forms"].items()}
    ids = {form: [w["id"] for w in ws] for form, ws in pool["forms"].items()}
    pb = hx._pool_block(forms)
    for form, blk in pb["forms"].items():
        blk["ids_sha256"] = hx._sha_obj(ids[form])
    rows_mod = importlib.import_module("%s.rows" % family)
    names_files = [paths.NAMES_MANIFEST, paths.NAMES_MANIFEST_SHA, os.path.join(paths.INFRA, "namespace.py")]
    exp = {
        "export": "%s template and wording-pool hash export" % family,
        "family": family,
        "version": hx.EXPORT_VERSION,
        "created_utc": created or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        **hx.META,
        "code": {rel(p): util.sha256_file(p) for p in sorted(code)},
        "engine": {rel(p): util.sha256_file(p) for p in sorted(engine)},
        "solver_b": {rel(p): util.sha256_file(p) for p in sorted(solver_b)},
        "extra": {rel(pool_file): util.sha256_file(pool_file)},
        "tables": {k: hx._sha_obj(v) for k, v in sorted(tables.items())},
        "wording_pool": dict(pb, file=rel(pool_file), file_sha256=util.sha256_file(pool_file)),
        "seed_pool": hx._pool_block(_seed_pool(family, rows_mod)),
        "names": {os.path.basename(p): util.sha256_file(p) for p in sorted(names_files)},
    }
    exp["export_sha256"] = hx._sha_obj(exp)
    return exp


def main(argv=None):
    fams = argv or sys.argv[1:] or sorted(FAMILIES)
    for fam in fams:
        exp = build(fam)
        hx.assert_no_text(exp)
        sha = hx.write_export(os.path.join(FAM_ROOT, fam, "HASH_EXPORT.json"), exp)
        print(fam, "export_sha256", exp["export_sha256"], "file_sha256", sha, "templates", exp["wording_pool"]["n_templates"],
              "forms", exp["wording_pool"]["n_forms"], "code_files", len(exp["code"]), "tables", len(exp["tables"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

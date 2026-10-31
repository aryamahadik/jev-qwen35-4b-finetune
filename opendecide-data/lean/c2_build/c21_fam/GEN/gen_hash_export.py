"""TEMPLATE / WORDING-POOL HASH EXPORT for GEN (plan 16.1: "hash export v1.1 ... every template, wording pool ... is in the export; any later change
= a new export + re-stamp of the affected rows"; G0 addendum v3.2 G-W3 template-hash currency). HASHES ONLY, NO TEXT: every string value in the
export is a sha256 hex digest, a path, a key id or a form id. Nothing here reads or writes a row.

    python3 gen_hash_export.py --write      # rewrites HASH_EXPORT.json (+ HASH_EXPORT.sha256)
    python3 gen_hash_export.py --check      # recomputes and compares with the file on disk (exit 1 when stale)

What is hashed (sha256):
  code             every .py file of the lane (generator, solver A, builder, adversary, gates, probes, row check, stamp hook, this file) and of
                   solver B (b_*.py, bcommon.py, question_templates.json)
  tables           every plain-data module constant (UPPER_CASE) of the generator modules, as canonical JSON (sizes, label sets, bins, traps,
                   units, rounding texts, residue moduli ...): the closed tables the rows are built from
  wording pool     each pool file; each key's list as a whole; the sha256 of EVERY template string (UTF-8 bytes, {slot} fields included); the pool as
                   a whole (gen_common.WordingPool.sha) and the pool interface (POOL_SPEC)
  predicate vocab  per domain: the sha256 of every phrase
  questions        solver B's copy of the question templates (real and test-only sets), per key
  unbuilt          pool files and forms that have a wording file but no generator yet (HX-*), listed so a later build is a visible change
  names            NAMES_MANIFEST_V1 (+ v1.1 / v1.2 when present) with their pinned shas, namespace.py
  template_hash    one digest over code + tables + pool + vocab + questions + names: the value stamped on every row (G-W3)
"""
import argparse
import datetime
import hashlib
import importlib
import json
import os
import re
import sys
from decimal import Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
C2_BUILD = os.path.dirname(os.path.dirname(HERE))
L0 = os.path.join(C2_BUILD, "zed_orch", "c21", "l0")
OUT = os.path.join(HERE, "HASH_EXPORT.json")
EXPORT_VERSION = "v1.1-skeptic-18oct"
META = {"kind": "hashes_only_no_text", "algorithm": "sha256",
        "canonicalisation": "tables: json sort_keys separators (',' ':') ensure_ascii; templates: sha256 of the utf-8 template string with {slot} fields"}
MODULES = ("gen_common", "arith", "logic", "causal", "temporal", "tables", "blocks", "builder", "heuristics", "adversary", "row_check", "probes", "gates", "canon", "stamp_hook")
UNBUILT = {"forms": ["HX-E", "HX-U", "HX-S", "HX-T", "HX-O", "HX-D"], "sub_blocks": ["TP-DM", "TP-RG", "TP-BA"], "transforms": ["NOTA-GENERIC", "PAD-INERT"],
           "features": ["A21 length tiers", "difficulty ladder L1-L4 as a stored level", "pad invariance (a4)"]}
_CONST = re.compile(r"^[A-Z][A-Z0-9_]+$")


def sha_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def sha_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def canon_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha_obj(obj):
    return sha_text(canon_json(obj))


def norm(o):
    """JSON-able copy of a module constant; TypeError for anything that is not plain data (functions, classes, modules)."""
    if isinstance(o, (str, int, float, bool)) or o is None:
        return o
    if isinstance(o, Decimal):
        return str(o)
    if isinstance(o, dict):
        return {str(k): norm(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [norm(v) for v in o]
    if isinstance(o, (set, frozenset)):
        return sorted(norm(v) for v in o)
    if hasattr(o, "pattern") and hasattr(o, "flags"):
        return o.pattern
    raise TypeError(type(o).__name__)


def module_tables(mod_names, prefix_dir=None):
    """{'module.NAME': sha256 of the canonical JSON of the constant} for every plain-data UPPER_CASE constant. Constants are hashed, never listed."""
    out = {}
    for name in mod_names:
        mod = importlib.import_module(name)
        for const in sorted(dir(mod)):
            if _CONST.match(const) and not const.startswith("_"):
                try:
                    out["%s.%s" % (name, const)] = sha_obj(norm(getattr(mod, const)))
                except TypeError:
                    continue
    return out


def template_block(entries):
    """{key: {count, key_sha256, template_sha256: [...]}} for {key: [template strings]}."""
    out = {}
    for k in sorted(entries):
        lst = entries[k]
        out[k] = {"count": len(lst), "key_sha256": sha_obj(lst), "template_sha256": [sha_text(t) for t in lst]}
    return out


def code_files():
    files = [os.path.join(HERE, f) for f in sorted(os.listdir(HERE)) if f.endswith(".py")]
    sb = os.path.join(HERE, "solver_b")
    files += [os.path.join(sb, f) for f in sorted(os.listdir(sb)) if f.endswith(".py") or f == "question_templates.json"]
    return files


def names_files():
    out = []
    for fn in ("NAMES_MANIFEST_V1.json", "NAMES_MANIFEST_V1.sha256", "NAMES_MANIFEST_V1_1.json", "NAMES_MANIFEST_V1_1.sha256", "NAMES_MANIFEST_V1_2.json",
               "NAMES_MANIFEST_V1_2.sha256"):
        p = os.path.join(L0, fn)
        if os.path.isfile(p):
            out.append(p)
    out.append(os.path.join(C2_BUILD, "c21_infra", "namespace.py"))
    return out


def build_export(created=None):
    sys.path.insert(0, HERE)
    sys.path.insert(0, os.path.join(HERE, "solver_b"))
    import pool_loader as PL
    from gen_common import POOL_SPEC, WordingPool
    rel = lambda p: os.path.relpath(p, HERE).replace(os.sep, "/")           # noqa: E731
    code = {rel(p): sha_file(p) for p in code_files() if os.path.basename(p) != "HASH_EXPORT.json"}
    pool_files = PL.verify_files()
    real = PL.load_real_pool(verify=False)
    ent = PL.load_entries()
    vocab = PL.predicate_vocab(verify=False)
    with open(os.path.join(HERE, "pools", "hx_forms.json"), "r", encoding="utf-8") as f:
        hx = json.load(f)["entries"]
    with open(os.path.join(HERE, "solver_b", "question_templates.json"), "r", encoding="utf-8") as f:
        qsets = json.load(f)["sets"]
    tables = module_tables(MODULES)
    tables["gen_common.POOL_SPEC"] = sha_obj({k: {"slots": list(v["slots"]), "min": v["min"]} for k, v in POOL_SPEC.items()})
    exp = {
        "export": "GEN template and wording-pool hash export (hashes only, no text)",
        "family": "GEN", "version": EXPORT_VERSION, **META,
        "code": code,
        "code_aggregate_sha256": sha_obj(code),
        "tables": tables,
        "tables_aggregate_sha256": sha_obj(tables),
        "wording_pool": {"files": pool_files, "pool_sha256": real.sha(), "pool_interface_sha256": tables["gen_common.POOL_SPEC"],
                         "n_keys": len(ent), "n_templates": sum(len(v) for v in ent.values()), "keys": template_block(ent)},
        "predicate_vocab": {d: [sha_text(p) for p in vocab[d]] for d in sorted(vocab)},
        "predicate_vocab_sha256": sha_obj({d: vocab[d] for d in sorted(vocab)}),
        "question_templates_solver_b": {name: {"n_templates": sum(len(v) for v in by.values()), "keys": template_block(by)} for name, by in sorted(qsets.items())},
        "unbuilt_wording": {"hx_forms": {"file_sha256": pool_files["hx_forms.json"], "keys": template_block(hx)}, "note": UNBUILT},
        "names": {os.path.basename(p): sha_file(p) for p in names_files()},
    }
    exp["template_hash"] = sha_obj({"code": exp["code_aggregate_sha256"], "tables": exp["tables_aggregate_sha256"], "pool": exp["wording_pool"]["pool_sha256"],
                                    "vocab": exp["predicate_vocab_sha256"], "questions": exp["question_templates_solver_b"], "names": exp["names"]})
    exp["export_sha256"] = sha_obj(exp)
    exp["created_utc"] = created or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")      # outside export_sha256
    return exp


def write_export(exp, path=OUT):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(exp, f, indent=1, sort_keys=True)
        f.write("\n")
    sha = sha_file(path)
    with open(os.path.splitext(path)[0] + ".sha256", "w", encoding="utf-8") as f:
        f.write("%s  %s\n" % (sha, os.path.basename(path)))
    return sha


def live_template_hash():
    """The template hash of the files as they are NOW (the value build_checked compares with the one in HASH_EXPORT.json: G-W3)."""
    return build_export()["template_hash"]


def template_hash_args(path=OUT):
    """Keyword arguments for row_check.build_checked in a production run: the hash on disk and the hash of the files now (G-W3: they must be equal)."""
    return {"template_hash": exported_template_hash(path), "template_hash_live": live_template_hash()}


def exported_template_hash(path=OUT):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)["template_hash"]


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    exp = build_export()
    if args.write:
        print("wrote", OUT, "file sha256", write_export(exp), "template_hash", exp["template_hash"], "export_sha256", exp["export_sha256"])
        return 0
    if args.check:
        try:
            on_disk = json.load(open(OUT, "r", encoding="utf-8"))
        except OSError:
            print("no HASH_EXPORT.json")
            return 1
        on_disk.pop("created_utc", None)
        exp2 = dict(exp)
        exp2.pop("created_utc", None)
        same = on_disk == exp2
        print("CURRENT" if same else "STALE: a template, table, pool or code file changed since the export (new export + re-made rows)")
        return 0 if same else 1
    print(json.dumps({"template_hash": exp["template_hash"], "export_sha256": exp["export_sha256"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

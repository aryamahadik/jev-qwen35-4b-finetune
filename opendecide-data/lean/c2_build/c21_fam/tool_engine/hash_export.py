"""TEMPLATE / WORDING-POOL HASH EXPORT for the L-T families (plan 16.1: "hash export v1.1 ... every template, wording pool ... is in the
export; any later change = a new export + re-stamp of the affected rows"). HASHES ONLY, NO TEXT: every string value in the export is
a sha256 hex digest, a file path, a form id, or one of a few fixed metadata words. Nothing here reads or writes a row.

What is hashed (sha256):
  * every code file that decides or renders a row (generator, renderer, solver A, wording seeds, environment; the shared engine files),
    and solver B's files;
  * the closed tables the rows are built from (sizes, label mixes, plan entries, label sets, verb / role / archetype lists, tool
    description phrases, fixed output phrases, claim / task / criterion seeds ...) as canonical JSON;
  * the EXPANDED wording pool: the pool file, the pool as a whole (the pool_manifest's pool_sha256), and for every form its own
    sha256, its wording count and the sha256 of each template string (the template with its {slot} fields, UTF-8 bytes);
  * the SEED pool the same way;
  * the names allow-list manifest (NAMES_MANIFEST_V1.json) and namespace.py, so a names change shows;
  * a final export_sha256 over everything above.
A wording hash is a plain sha256 of the template string (the sealed side's salted hash export is the matcher's own program).
"""
import datetime
import hashlib
import json
import os

from . import util, wording_expand

EXPORT_VERSION = "v1"
META = {
    "kind": "hashes_only_no_text",
    "algorithm": "sha256",
    "canonicalisation": "tables: json sort_keys separators (',' ':') ensure_ascii; templates: sha256 of the utf-8 template string with {slot} fields",
}


def _sha_obj(obj):
    return util.sha256_text(util.canon_json(obj))


def _sha_file(path):
    return util.sha256_file(path)


def _pool_block(pools):
    forms = {}
    for form in sorted(pools):
        ws = pools[form]
        forms[form] = {"count": len(ws), "form_sha256": _sha_obj(ws),
                       "template_sha256": [hashlib.sha256(w.encode("utf-8")).hexdigest() for w in ws]}
    return {"pool_sha256": wording_expand.pool_sha(pools), "n_forms": len(forms), "n_templates": sum(len(v) for v in pools.values()),
            "forms": forms}


_CONST = __import__("re").compile(r"^[A-Z][A-Z0-9_]+$")


def _norm(o):
    """JSON-able copy of a module constant (tuple / set -> list, regex -> its pattern); TypeError for anything else (functions ...)."""
    if isinstance(o, (str, int, float, bool)) or o is None:
        return o
    if isinstance(o, dict):
        return {str(k): _norm(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_norm(v) for v in o]
    if isinstance(o, (set, frozenset)):
        return sorted(_norm(v) for v in o)
    if hasattr(o, "pattern") and hasattr(o, "flags"):
        return o.pattern
    raise TypeError(type(o).__name__)


def module_tables(prefix, mod):
    """{prefix.NAME: json-able value} for every module-level CONSTANT (UPPER_CASE) of `mod` that is plain data."""
    out = {}
    for name in sorted(dir(mod)):
        if _CONST.match(name) and not name.startswith("_"):
            try:
                out["%s.%s" % (prefix, name)] = _norm(getattr(mod, name))
            except TypeError:
                continue
    return out


def build_export(family, fam_dir, engine_dir, code_files, solver_b_files, tables, pool_json, pool_manifest, seed_pools, names_files,
                 extra_files=(), created=None):
    """-> the export dict. `code_files` / `solver_b_files` / `extra_files` are paths (hashed, listed by path relative to fam_dir);
    `tables` {name: json-able object}; `pool_json` the expanded pool file; `seed_pools` the seed pool dict {form: [templates]}."""
    rel = lambda p: os.path.relpath(p, fam_dir).replace(os.sep, "/")           # noqa: E731
    with open(pool_json, "r", encoding="utf-8") as f:
        pools = json.load(f)
    with open(pool_manifest, "r", encoding="utf-8") as f:
        man = json.load(f)
    pb = _pool_block(pools)
    if pb["pool_sha256"] != man["pool_sha256"]:
        raise ValueError("the pool file does not match its manifest: rebuild the pool before exporting")
    exp = {
        "export": "%s template and wording-pool hash export" % family,
        "family": family,
        "version": EXPORT_VERSION,
        "created_utc": created or datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        **META,
        "code": {rel(p): _sha_file(p) for p in sorted(code_files)},
        "engine": {rel(p): _sha_file(p) for p in sorted(os.path.join(engine_dir, f) for f in os.listdir(engine_dir)
                                                          if f.endswith(".py") and f != "__init__.py")},
        "solver_b": {rel(p): _sha_file(p) for p in sorted(solver_b_files)},
        "extra": {rel(p): _sha_file(p) for p in sorted(extra_files)},
        "tables": {k: _sha_obj(v) for k, v in sorted(tables.items())},
        "wording_pool": dict(pb, file=rel(pool_json), file_sha256=_sha_file(pool_json), manifest_sha256=_sha_file(pool_manifest)),
        "seed_pool": _pool_block(seed_pools),
        "names": {os.path.basename(p): _sha_file(p) for p in sorted(names_files)},
    }
    exp["export_sha256"] = _sha_obj(exp)
    return exp


def write_export(path, exp):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(exp, f, indent=1, sort_keys=True)
        f.write("\n")
    sha = _sha_file(path)
    with open(os.path.splitext(path)[0] + ".sha256", "w", encoding="utf-8") as f:
        f.write("%s  %s\n" % (sha, os.path.basename(path)))
    return sha


_HEX = set("0123456789abcdef")
_ID = __import__("re").compile(r"^[A-Za-z0-9_./:\-]+$")
_FREE = {"export", "kind", "algorithm", "canonicalisation", "version", "family", "created_utc"}


def assert_no_text(exp):
    """Every string in the export is a sha256 digest, a path / form id, or one of the fixed metadata fields. Raises on anything else."""
    def walk(o, key=None):
        if isinstance(o, dict):
            for k, v in o.items():
                if not _ID.match(k):
                    raise ValueError("key is not an id: %r" % k)
                walk(v, k)
        elif isinstance(o, list):
            for v in o:
                walk(v, key)
        elif isinstance(o, str):
            if key in _FREE:
                return
            if len(o) == 64 and set(o) <= _HEX:
                return
            if _ID.match(o):
                return
            raise ValueError("a free-text value is in the export under %r: %r" % (key, o[:40]))
    walk(exp)
    return True

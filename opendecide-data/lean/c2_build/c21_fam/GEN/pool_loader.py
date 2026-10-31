"""Loads the REAL GEN wording pool (Haiku-authored JSON files in pools/) into a gen_common.WordingPool, verifying every file against
pools/manifest.json (sha256) and the pool interface (gen_common.check_pool, strict counts). CODE ONLY; reads the pool files, writes nothing.

    pool = load_real_pool()          # WordingPool(testonly=False); raises PoolLoadError on any mismatch
    predicate_vocab()                # {domain id: [predicate noun phrases]} (closed list, checked)

Why this module exists (skeptic finding, 18 Oct): nothing loaded the pool files, so the builder could only ever run on the TEST-ONLY pool.
"""
import hashlib
import json
import os
import re

from gen_common import WordingPool, check_pool

HERE = os.path.dirname(os.path.abspath(__file__))
POOL_DIR = os.path.join(HERE, "pools")
WORDING_FILES = ("fragments.json", "q_arith.json", "q_logic.json", "q_causal.json", "q_temporal.json", "q_table.json")
OTHER_FILES = ("predicate_vocab.json", "hx_forms.json")
MANIFEST = "manifest.json"
STOP_WORDS = frozenset("is a an and not to that it if then something anything".split())    # B's predicate reader splits on these


class PoolLoadError(ValueError):
    pass


def sha_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def manifest():
    with open(os.path.join(POOL_DIR, MANIFEST), "r", encoding="utf-8") as f:
        return json.load(f)


def verify_files():
    """Every pool file's sha256 equals the one recorded in pools/manifest.json. Returns {file: sha}."""
    rec = manifest()["files"]
    out = {}
    for fn in WORDING_FILES + OTHER_FILES:
        key = "GEN/pools/" + fn
        if key not in rec:
            raise PoolLoadError("%s is not in pools/manifest.json" % fn)
        sha = sha_file(os.path.join(POOL_DIR, fn))
        if sha != rec[key]["sha256"]:
            raise PoolLoadError("%s sha %s differs from pools/manifest.json %s (pool edited without refreshing the manifest)" % (fn, sha[:12], rec[key]["sha256"][:12]))
        out[fn] = sha
    return out


def load_entries():
    ent = {}
    for fn in WORDING_FILES:
        with open(os.path.join(POOL_DIR, fn), "r", encoding="utf-8") as f:
            d = json.load(f)
        for k, v in d["entries"].items():
            if k in ent:
                raise PoolLoadError("key %s appears in two pool files" % k)
            ent[k] = list(v)
    return ent


def load_real_pool(verify=True):
    if verify:
        verify_files()
    pool = WordingPool(load_entries(), testonly=False, name="GEN-real")
    probs = check_pool(pool)
    if probs:
        raise PoolLoadError("pool does not meet the interface: %s" % probs[:4])
    return pool


def predicate_vocab(verify=True):
    if verify:
        verify_files()
    with open(os.path.join(POOL_DIR, "predicate_vocab.json"), "r", encoding="utf-8") as f:
        d = json.load(f)["entries"]
    for dom, lst in d.items():
        for ph in lst:
            if any(w in STOP_WORDS for w in ph.split()):
                raise PoolLoadError("predicate phrase %r (%s) contains a frame word" % (ph, dom))
            if not re.fullmatch(r"[a-z][a-z0-9'-]*(?: [a-z][a-z0-9'-]*)*", ph):
                raise PoolLoadError("predicate phrase %r is not plain lower case words (hyphen and apostrophe allowed)" % ph)
    return d


def refresh_manifest():
    """Rewrites the sha256 values in pools/manifest.json after a deliberate pool edit (a new HASH_EXPORT must follow). Returns changed files."""
    path = os.path.join(POOL_DIR, MANIFEST)
    m = manifest()
    changed = []
    for fn in WORDING_FILES + OTHER_FILES:
        key = "GEN/pools/" + fn
        new = sha_file(os.path.join(POOL_DIR, fn))
        if m["files"][key]["sha256"] != new:
            m["files"][key]["sha256"] = new
            changed.append(fn)
    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.write(json.dumps(m, indent=2, ensure_ascii=False) + "\n")
    return changed


if __name__ == "__main__":
    import sys
    if "--refresh-manifest" in sys.argv:
        print("refreshed:", refresh_manifest())
    else:
        print("verified:", sorted(verify_files()))

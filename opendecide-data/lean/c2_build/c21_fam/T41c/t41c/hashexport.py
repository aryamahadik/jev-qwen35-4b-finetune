"""Template / wording-pool HASH EXPORT for T41c (hashes only, no text).

    python -m t41c.hashexport --write ../HASH_EXPORT.json     # (path relative to the T41c folder)
    python -m t41c.hashexport --check ../HASH_EXPORT.json     # exit 1 if anything the export covers has changed

What a row depends on besides its seed is covered here: generator + solver code (per-file sha), the pinned label table
(table.py), solver B's closed delegation-verb list (sha only; the list itself stays hidden from A), every pool file (file
sha + a sha256 per wording, per cell), the attack-register lexicon (a sha256 per stem and one for the set), the handoff
schemas, the names manifests and the G0 records the code was built from. A template or wording change after this export
is a NEW export and re-stamped rows (plan 16.1 step 6). No wording, stem, name or row text is written to the export.
"""
import argparse
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FAM = os.path.dirname(HERE)
C2B = os.path.dirname(os.path.dirname(FAM))
POOL_DIR = os.path.join(FAM, "pools")
SCHEMA = 1


def sha(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(path):
    with open(path, "rb") as f:
        return sha(f.read())


def sha_text(t):
    return sha(t.encode("utf-8"))


def _set_sha(hashes):
    return sha("\n".join(sorted(hashes)).encode())


def _py_shas(folder, skip=("__pycache__",)):
    out = {}
    for fn in sorted(os.listdir(folder)):
        if fn.endswith(".py"):
            out[fn] = sha_file(os.path.join(folder, fn))
    return out


def _cells(mapping):
    """{cell: [text]} -> {cell: {"n", "set_sha", "entries": [sha256 per wording, in file order]}}"""
    out = {}
    for cell, texts in mapping.items():
        hs = [sha_text(t) for t in texts]
        out[cell] = {"n": len(hs), "set_sha": _set_sha(hs), "entries": hs}
    return out


def pool_section():
    sec = {"files": {}, "cells": {}}
    for fn in sorted(os.listdir(POOL_DIR)):
        if fn.endswith(".json"):
            p = os.path.join(POOL_DIR, fn)
            sec["files"][fn] = {"sha256": sha_file(p), "bytes": os.path.getsize(p)}
    load = lambda n: json.load(open(os.path.join(POOL_DIR, n), encoding="utf-8"))
    sec["cells"]["directive_high_v1"] = _cells(load("directive_high_v1.json")["classes"])
    sec["cells"]["directive_benign_v1"] = _cells(load("directive_benign_v1.json")["classes"])
    sec["cells"]["cue_wrappers_v1"] = _cells(load("cue_wrappers_v1.json")["frames"])
    sec["cells"]["a6_gate_directed_v1"] = _cells(load("a6_gate_directed_v1.json")["cells"])
    lex = load("lex_attack_register_v1.json")
    stems = sorted({w.lower() for g in lex["groups"].values() for w in g})
    sh = [sha_text(s) for s in stems]
    sec["lexicon"] = {"id": lex["id"], "stems": len(stems), "set_sha": _set_sha(sh), "stem_hashes": sorted(sh),
                      "group_sizes": {g: len(v) for g, v in sorted(lex["groups"].items())}}
    sec["wording_totals"] = {k: sum(v["n"] for v in c.values()) for k, c in sec["cells"].items()}
    return sec


def coverage_section():
    """How much of the cell brief the pool files cover (numbers only)."""
    sys.path.insert(0, C2B + "/c21_infra") if (C2B + "/c21_infra") not in sys.path else None
    sys.path.insert(0, FAM) if FAM not in sys.path else None
    from t41c import pools
    names = pools.cell_names()
    pref = {}
    for c in names:
        pref.setdefault(c.split(".")[0], 0)
        pref[c.split(".")[0]] += 1
    return {"required_cells_by_prefix": pref, "required_cells_total": len(names),
            "cells_with_wordings_in_pool_files": {
                "atk (class-level pool, no variant or slot-length split)": 8,
                "ben (class-level pool, no variant or slot-length split)": 9,
                "task, bg, fill, noise, men, wrap": 0},
            "pool_kind_for_generator": "none production: the generator reads pools.Pool cells; the files here are not in that shape"}


def build_export(built="2026-10-18"):
    sys.path.insert(0, FAM) if FAM not in sys.path else None
    sys.path.insert(0, C2B + "/c21_infra") if (C2B + "/c21_infra") not in sys.path else None
    from t41c import planner
    code = _py_shas(HERE)
    solver_b = _py_shas(os.path.join(FAM, "solver_b"))
    verbs_path = os.path.join(FAM, "solver_b", "verbs.py")
    ns = {}
    l0 = os.path.join(C2B, "zed_orch", "c21", "l0")
    for fn in ("NAMES_MANIFEST_V1.json", "NAMES_MANIFEST_V1_1.json"):
        ns[fn] = sha_file(os.path.join(l0, fn))
    fam_docs = os.path.join(C2B, "zed_orch", "c21", "families")
    docs = {}
    for rel in ("T41c/G0_LITE.md", "T41c/G0_ADDENDUM_v32.md", "G0_APPROVALS.md", "G0_APPROVALS_v32.md"):
        docs[rel] = sha_file(os.path.join(fam_docs, rel))
    handoff = {fn: sha_file(os.path.join(FAM, "handoff", fn)) for fn in sorted(os.listdir(os.path.join(FAM, "handoff")))
               if fn.endswith(".json")}
    pool = pool_section()
    held = planner.draw_heldout()
    exp = {
        "export": "T41c template and wording-pool hash export (hashes only, no text)",
        "schema": SCHEMA, "family": "T41c", "lane": "L-I", "built": built,
        "status": "PRE-STAMP. Built by the L-I build skeptic on 18 Oct 2026. The G13 stamp service has not run on any wording "
                  "or row; no rows exist. Not the Thu 22 v1.1 export: that one adds the A10/A12/A14/A16 templates, the section 7 "
                  "pool and the frozen lexicon after the builder finishes sections 2 to 9 of the addendum.",
        "hash_method": "sha256 over the UTF-8 bytes of each wording / stem / file exactly as stored",
        "code": {"t41c": code, "solver_b": solver_b},
        "code_aggregate_sha": sha(json.dumps({"t41c": code, "solver_b": solver_b}, sort_keys=True).encode()),
        "label_table": {"pinned_table_file": "t41c/table.py", "sha256": code["table.py"],
                        "necessary_steps_and_ids_file": "t41c/ids.py", "ids_sha256": code["ids.py"]},
        "solver_b": {"b_program_sha256": solver_b["b_program.py"], "closed_verb_list_file": "solver_b/verbs.py",
                     "closed_verb_list_sha256": sha_file(verbs_path), "hidden_from_solver_a": True},
        "pools": pool,
        "pool_coverage": coverage_section(),
        "heldout_draw": {"version": held["version"], "sha256": sha(json.dumps(held, sort_keys=True).encode()),
                         "rule": "seeded, TRAINING salt, recomputed by planner.draw_heldout(); never hand-picked"},
        "handoff_schemas": handoff,
        "names_manifests": ns,
        "g0_records": docs,
        "test_fixture_pool": "not exported (pools.make_test_pool is a unit-test fixture; a row job refuses it)",
    }
    exp["template_hash"] = sha(json.dumps({"code": exp["code_aggregate_sha"], "pools": {k: v["sha256"] for k, v in pool["files"].items()},
                                           "lexicon": pool["lexicon"]["set_sha"], "verbs": exp["solver_b"]["closed_verb_list_sha256"],
                                           "heldout": exp["heldout_draw"]["sha256"]}, sort_keys=True).encode())
    return exp


def canonical(obj):
    return json.dumps(obj, indent=1, sort_keys=True) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--write")
    g.add_argument("--check")
    a = ap.parse_args(argv)
    cur = build_export()
    if a.write:
        # the audit numbers need sklearn; they are numbers and codes only
        sys.path.insert(0, FAM) if FAM not in sys.path else None
        from t41c import pool_check
        cur["pool_audit"] = pool_check.audit()
        path = os.path.abspath(a.write)
        with open(path, "w", encoding="utf-8") as f:
            f.write(canonical(cur))
        print("wrote", path, "template_hash", cur["template_hash"], "bytes", os.path.getsize(path))
        return 0
    with open(a.check, encoding="utf-8") as f:
        old = json.load(f)
    old.pop("pool_audit", None)
    if old == json.loads(canonical(cur)):
        print("HASH_EXPORT current: template_hash", cur["template_hash"])
        return 0
    print("HASH_EXPORT STALE: a template, wording, code or record changed since the export (new export + re-stamp)")
    for k in cur:
        if old.get(k) != json.loads(canonical({k: cur[k]}))[k]:
            print("  differs:", k)
    return 1


if __name__ == "__main__":
    sys.exit(main())

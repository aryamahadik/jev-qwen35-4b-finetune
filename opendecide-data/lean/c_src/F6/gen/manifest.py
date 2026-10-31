"""Write out/MANIFEST.json: binding shas, inputs, code, outputs (counts + sha256), coverage, gate results, problems."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from . import common as C
from .common import OUT, TMP, GEN, LEAN, CSRC, sha256_file, read_jsonl, now, progress


def _load(p):
    try:
        return json.load(open(p))
    except FileNotFoundError:
        return None


def coverage(rows):
    return {"rows": len(rows), "samplers": dict(Counter(r["meta"]["sampler"] for r in rows)),
            "cards": len({r["meta"]["card_id"] for r in rows}), "packs": len({r["meta"]["domain_pack"] for r in rows}),
            "persona_seeds": len({r["meta"].get("persona_seed") for r in rows if r["meta"].get("persona_seed")}),
            "styles": len({r["meta"]["format_style"] for r in rows}),
            "containers": dict(Counter(r["meta"]["format_style"] for r in rows).most_common(0)),
            "wordings": len({r["meta"]["wording_id"] for r in rows}),
            "packs_per_sampler": {s: len({r["meta"]["domain_pack"] for r in rows if r["meta"]["sampler"] == s})
                                  for s in sorted({r["meta"]["sampler"] for r in rows})}}


def parents(all_rows: list[dict]) -> list:
    """MIXER_NOTE 1 (spec 3.H / G1): every pack, codebook, wording set and real-text dataset the rows derive from."""
    rel = lambda q: str(q.relative_to(LEAN))
    par = []
    for q in (CSRC / "packs" / "packs-3" / "packs-3.jsonl", CSRC / "packs" / "packs-3" / "packs-3.manifest.json",
              CSRC / "packs" / "packs-4" / "packs.jsonl", CSRC / "packs" / "packs-4" / "manifest.json"):
        if q.exists():
            par.append({"kind": "pack_file", "path": rel(q), "sha256": sha256_file(q)})
    used = Counter(r["meta"].get("domain_pack") for r in all_rows)
    for src, q in (("packs-3", CSRC / "packs" / "packs-3" / "packs-3.jsonl"), ("packs-4", CSRC / "packs" / "packs-4" / "packs.jsonl")):
        for ln in open(q, encoding="utf-8"):
            if not ln.strip():
                continue
            pk = json.loads(ln)
            if pk["id"] in used:
                par.append({"kind": "domain_pack", "id": pk["id"], "source": src, "rows": used[pk["id"]],
                            "persona_seed": pk.get("persona_seed"), "parents": pk.get("parents"),
                            "licence": pk.get("licence")})
    f1 = CSRC / "formats" / "formats-1"
    for q in [f1 / "MANIFEST.json"] + sorted((f1 / "data").glob("*.jsonl")):
        par.append({"kind": "format_style_pool", "path": rel(q), "sha256": sha256_file(q)})
    f2 = CSRC / "formats" / "formats-2"
    wids = Counter(r["meta"].get("wording_id") for r in all_rows)
    for q in (f2 / "manifest.json", f2 / "wordings" / "family_pools.jsonl"):
        par.append({"kind": "wording_set", "path": rel(q), "sha256": sha256_file(q)})
    par.append({"kind": "wording_ids", "source": "formats-2 wordings/family_pools.jsonl (29 F6 + 6 neutral F4 ids)",
                "ids": sorted(w for w in wids if w)})
    par.append({"kind": "real_text_dataset", "id": "gd_onet_occupation",
                "use": "persona seeds via packs-3/packs-4 (O*NET 31.0 occupation titles only; CC BY 4.0)",
                "persona_seeds": len({r["meta"].get("persona_seed") for r in all_rows})})
    return par


def relations() -> dict:
    """MIXER_NOTE 3: relation counts and sha256 match the relation files on disk."""
    res = {}
    for base in ("candidates_r1", "qc_sample", "mixdev_S5"):
        q = OUT / f"{base}.relations.jsonl"
        if q.exists():
            recs = read_jsonl(q)
            res[q.name] = {"sha256": sha256_file(q), "lines": len(recs), "by_type": dict(Counter(x["type"] for x in recs))}
    return res


def main(problems: list[str] | None = None):
    from fmt1 import pool as fpool
    m = {"family": "F6", "gen_version": C.GEN_VERSION, "spec_id": C.SPEC_ID, "written_utc": now(),
         "binding": {"G0_SPEC.md": C.SPEC_SHA256,
                     "C_DATA_SPEC.md": sha256_file(LEAN / "c_spec" / "C_DATA_SPEC.md"),
                     "C_TRAIN_RECIPE.md": sha256_file(LEAN / "c_spec" / "C_TRAIN_RECIPE.md"),
                     "PREREG_FINAL.md": sha256_file(LEAN / "PREREG_FINAL.md"),
                     "sealed_suite_A15": C.SEALED_SUITE_SHA256},
         "inputs": {"negcount.py": C.PINNED["negcount.py"], "markers.json (v1.1)": C.PINNED["markers.json"],
                    "denylist.py": C.PINNED["denylist.py"],
                    "packs-3/packs-3.jsonl": sha256_file(CSRC / "packs" / "packs-3" / "packs-3.jsonl"),
                    "packs-4/packs.jsonl": sha256_file(CSRC / "packs" / "packs-4" / "packs.jsonl"),
                    "formats-1/MANIFEST.json": sha256_file(CSRC / "formats" / "formats-1" / "MANIFEST.json"),
                    "formats-2/manifest.json": sha256_file(CSRC / "formats" / "formats-2" / "manifest.json"),
                    "decoder_io.py": sha256_file(LEAN / "decoder_io.py"),
                    "train_decoder.py": sha256_file(LEAN / "train_decoder.py"),
                    "tokenizer": "Qwen/Qwen3.5-4B (local HF cache, local_files_only)"},
         "code": {p.name: sha256_file(p) for p in sorted(GEN.glob("*.py"))},
         "outputs": {}, "coverage": {}, "gates": {}, "problems": problems or []}
    for base in ("candidates_r1", "qc_sample", "mixdev_S5"):
        p = OUT / f"{base}.jsonl"
        if not p.exists():
            continue
        rows = read_jsonl(p)
        files = {}
        for suf in (".jsonl", ".relations.jsonl", ".qc_side.jsonl"):
            q = OUT / f"{base}{suf}"
            if q.exists():
                files[q.name] = {"sha256": sha256_file(q), "lines": sum(1 for _ in open(q))}
        m["outputs"][base] = files
        m["coverage"][base] = coverage(rows)
        m["coverage"][base]["containers"] = dict(Counter(fpool.style(r["meta"]["format_style"])["container"]
                                                         for r in rows))
    allrows = [r for b in ("candidates_r1", "qc_sample", "mixdev_S5") if (OUT / f"{b}.jsonl").exists()
               for r in read_jsonl(OUT / f"{b}.jsonl")]
    m["parents"] = parents(allrows)
    m["relations"] = relations()
    for k, name in (("cand", "candidates_r1"), ("qc", "qc_sample"), ("dev", "mixdev_S5")):
        rep = _load(TMP / f"report_{k}.json")
        if rep:
            rep.pop("files", None)
            m["gates"][name] = rep
        g4 = _load(TMP / f"g4_{k}.json")
        if g4:
            m["gates"].setdefault(name, {})["G4"] = g4
        sc = _load(TMP / f"sealed_{k}.json")
        if sc:
            m["gates"].setdefault(name, {})["sealed_check"] = sc
    json.dump(m, open(OUT / "MANIFEST.json", "w"), indent=1, default=str)
    progress(f"MANIFEST written: outputs {list(m['outputs'])}")
    return m


if __name__ == "__main__":
    import sys
    probs = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else []
    main(probs)

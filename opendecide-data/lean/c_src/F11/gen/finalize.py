"""Write out/MANIFEST.json (counts, sha256, relation counts / sha, parents, mixdev separation, gates, deviations) and
qc/QC_REPORT.json (pool sha256s of every output and relation file, gate results).

  python gen/finalize.py
Reads tmp/build_<name>.json, tmp/gates_<set>.json and tmp/sealed_<set>.json written by build.py, gates.py and
run_sealed.py on the current out/ files; refuses to write when a gate result is stale (sha differs from disk).
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import common as C  # noqa: E402
from common import OUT, TMP, QC, GEN, LEAN, CSRC, FMT1, FMT2, PACKS, sha256_file, progress  # noqa: E402

NAMES = {"cand": "candidates_r1", "qc": "qc_sample", "dev": "mixdev_S5"}
DEVIATIONS = [
    "S5 codebook arm: formats-2 holds no held-out F11 codebook, so the 7 codebook-arm keys are written over F11 "
    "codebooks (xed x02/x07/x11, mams_acsa a01/a04, mams_atsa t02/t05) as dichotomous keys (a form never used in "
    "training), on held-out packs-3 wrappers, held-out format styles and reserved records only (XED: the 10% "
    "'dev' part of the orchestrator split; MAMS: the hash-reserved 8% of unused train records). EDOS is blocked (X15).",
    "S5 program arm: the coarse-group question is asked only on keys whose named couplets partition the cells "
    "(all 8 cards here).",
    "G15 unit rule (repair r1): a negation unit whose rows reach >= 2,000 served tokens holds the affirmative and ONE "
    "negation twin (neg or dneg, drawn 50/50; the other is not emitted), so every related row shares one call_id and "
    "the unit has 2 rows (spec 2.1 overrides the G0 3-row negation unit for long rows only).",
    "Per-card yes rates (repair r1, G7): one stratified antithetic uniform sample on [0.2, 0.8] per pool (mean 0.5), "
    "assigned to cards by a seeded swap search that balances card-text unigrams/bigrams shared by >= 2 cards "
    "(gen/build.py assign_rates; card vocabulary from a 16-row side pass on card copies, all globals restored).",
    "S7 depth (repair r1, A47 with R26 steps): one attribute (the annotation vector, mapped by the codebook), no "
    "rules: d = 1 when some one-step change alters the gold code, else 0; the earlier S7 depth (label count + 1 for "
    "a merged code) restated the gold's label count in metadata (G6 d, G7 depth x option-kind crosses).",
    "Multi-record S4 containers (repair r1, G2): the kv.aligned_colon skin (stacked key-value records separated only "
    "by a blank line) never holds a multi-record table; solver B code_line fix (a name never holds ':', '|' or '='), "
    "see tmp/repair/SOLVERB_FIX_r1.md.",
    "Sampler guards (repair r1): G12, a drawn unit that repeats a structure_hash held by another twin set of the pool "
    "is redrawn; G10, 'longest option is gold' is held at 1/k by redrawing (prob. >= 0.25 kept) units that move the "
    "pool's running sum of (1/k - hit) beyond +/- 1 row (non-inverted choice rows).",
    "Worked items (few-shot): 6 of 80 cards (7.5%), 1-3 items each, fmt1 fewshot templates FT01-FT15 (block case).",
    "Length (G0 G15 / X8, PREREG A22): the G0 per-row cap (1,900) and median 500-900 are unreachable at the G0 shares "
    "after the trim levers (proof: tmp/repair/INFEASIBLE_length.md). Every length is the SERVED prompt "
    "(gen/toklen.py: decoder_io.render_chat(CYGNET_SYSTEM, user_msg) under cygnet + schema_branch_mark, Qwen3.5-4B "
    "tokenizer); every row <= 7,900 (card probe trim + row guard in gen/build.py); shares and buckets kept; the mixer "
    "enforces the A22 mix-level cap. The G15 unit rule (<= 2 rows if a row >= 2,000) uses the same served count.",
    "names.py reads a pinned gzip copy of the Mac's /usr/share/dict/words (gen/english_words.txt.gz, same content) so "
    "the build is identical on any platform.",
]


def lines(p):
    with open(p) as f:
        return sum(1 for _ in f)


def load(p):
    return [json.loads(x) for x in open(p)]


def norm_state(s):
    return hashlib.sha256(" ".join((s or "").split()).casefold().encode()).hexdigest()


def main():
    probs = []
    files, rels, rows_by = {}, {}, {}
    for tag, name in NAMES.items():
        p, q = OUT / f"{name}.jsonl", OUT / f"{name}.relations.jsonl"
        rows_by[tag] = load(p)
        files[p.name] = {"sha256": sha256_file(p), "lines": lines(p)}
        sc = OUT / f"{name}.sidecar.jsonl"
        if sc.exists():
            files[sc.name] = {"sha256": sha256_file(sc), "lines": lines(sc),
                              "what": "S7 / S5-codebook cap-class sidecar (G0 S7, K07)"}
        rl = load(q)
        rels[q.name] = {"sha256": sha256_file(q), "lines": len(rl), "by_type": dict(Counter(x["type"] for x in rl))}
        g = json.load(open(TMP / f"gates_{tag}.json"))
        if g["rows_sha256"] != files[p.name]["sha256"] or g["relations_sha256"] != rels[q.name]["sha256"]:
            probs.append(f"gates_{tag}.json is stale")
        s = json.load(open(TMP / f"sealed_{tag}.json"))
        if s["input_sha256"] != files[p.name]["sha256"]:
            probs.append(f"sealed_{tag}.json is stale")
    # training vs mixdev separation (mixer rule 4)
    train = rows_by["cand"] + rows_by["qc"]
    dev = rows_by["dev"]
    sep = {}
    for k, f in (("group_id", lambda r: r["group_id"]), ("norm_state", lambda r: norm_state(r["state"])),
                 ("structure_hash", lambda r: r["meta"]["structure_hash"]),
                 ("domain_pack", lambda r: r["meta"]["domain_pack"])):
        sep[k] = len({f(r) for r in train} & {f(r) for r in dev})
    sep["rows_without_format_style"] = sum(1 for r in train + dev if not r["meta"].get("format_style"))
    if any(sep.values()):
        probs.append(f"mixdev separation: {sep}")
    # parents (spec 3.H / G1)
    used = {}
    for tag in NAMES:
        for r in rows_by[tag]:
            used.setdefault(r["meta"]["domain_pack"], set()).add(NAMES[tag])
    p4 = {json.loads(x)["id"]: json.loads(x) for x in open(PACKS / "packs-4" / "packs.jsonl")}
    p3 = {json.loads(x)["id"]: json.loads(x) for x in open(PACKS / "packs-3" / "packs-3.jsonl")}
    onet = "O*NET 31.0 Database, occupation_data.csv (main occupation titles; gd_onet_occupation)"
    parents = []
    for rel in ("packs-4/packs.jsonl", "packs-4/manifest.json", "packs-3/packs-3.jsonl"):
        if (PACKS / rel).exists():
            parents.append({"kind": "pack_file", "path": f"c_src/packs/{rel}", "sha256": sha256_file(PACKS / rel)})
    for pid in sorted(used):
        src = "packs-4" if pid in p4 else ("packs-3" if pid in p3 else None)
        pk = p4.get(pid) or p3.get(pid) or {}
        parents.append({"kind": "domain_pack", "id": pid, "source": src, "parents": [onet],
                        "licence": pk.get("licence") or "CC0 1.0 (Claude-written pack text)",
                        "used_in": sorted(used[pid])})
    parents.append({"kind": "formats-1", "path": "c_src/formats/formats-1/MANIFEST.json",
                    "sha256": sha256_file(FMT1 / "MANIFEST.json")})
    for d in sorted((FMT1 / "data").glob("*.jsonl")):
        parents.append({"kind": "formats-1_pool", "path": f"c_src/formats/formats-1/data/{d.name}",
                        "sha256": sha256_file(d)})
    for kind, rel in (("formats-2", "manifest.json"), ("codebooks", "codebooks/codebooks.jsonl"),
                      ("codebook_lexicon", "codebooks/lexicon.json"), ("wordings", "wordings/family_pools.jsonl")):
        if (FMT2 / rel).exists():
            parents.append({"kind": kind, "path": f"c_src/formats/formats-2/{rel}", "sha256": sha256_file(FMT2 / rel)})
    rt = {"xed": ("xed_en", "XED English (Ohman et al. 2020), CC BY 4.0",
                  ["OPUS OpenSubtitles (English subtitle lines; the XED source corpus)"]),
          "mams_acsa": ("mams", "MAMS ACSA (Jiang et al. 2019), Apache-2.0",
                        ["Citysearch New York restaurant reviews (Ganu et al. 2009)"]),
          "mams_atsa": ("mams", "MAMS ATSA (Jiang et al. 2019), Apache-2.0",
                        ["Citysearch New York restaurant reviews (Ganu et al. 2009)"])}
    for sc, (ds, lic, ups) in rt.items():
        fp = FMT2 / "records" / f"{sc}.jsonl"
        n_ds = {NAMES[t]: sum(1 for r in rows_by[t] if (r["meta"].get("text_source") or {}).get("dataset") == ds)
                for t in NAMES}
        parents.append({"kind": "real_text_records", "dataset": sc, "path": f"c_src/formats/formats-2/records/{fp.name}",
                        "sha256": sha256_file(fp), "licence": lic, "upstream_parents": ups,
                        "rows_from_dataset": n_ds})
    for rel in ("out/public3_split_3e.jsonl", "out/public3_record_claims.jsonl", "manifest_public3.json"):
        fp = CSRC / "public" / "public-3" / rel
        if fp.exists():
            parents.append({"kind": "public-3", "path": f"c_src/public/public-3/{rel}", "sha256": sha256_file(fp)})
    parents.append({"kind": "persona_seeds", "source": "O*NET 31.0 Occupation Data (CC BY 4.0) via packs",
                    "n_distinct": len({r["meta"].get("persona_seed") for t in NAMES for r in rows_by[t]
                                       if r["meta"].get("persona_seed")})})
    gates = {}
    for tag, name in NAMES.items():
        g = json.load(open(TMP / f"gates_{tag}.json"))
        s = json.load(open(TMP / f"sealed_{tag}.json"))
        b = json.load(open(TMP / f"build_{name}.json"))
        g.pop("G15_loader_fail_ids", None)
        gates[name] = {"build": {k: b[k] for k in ("rows", "relations", "cards", "by_sampler", "qtype", "twin_kind",
                                                   "check_failures")},
                       "gates": g, "sealed_check": {k: s[k] for k in ("rows", "hits", "hit_kinds", "report_kinds",
                                                                         "checker_sha256", "input_sha256")}}
        if g["hard_failures"]:
            probs.append(f"{name}: {g['hard_failures']}")
        if s["hits"]:
            probs.append(f"{name}: sealed hits {s['hits']}")
    from fmt1 import pool as fpool
    cov = {}
    for tag, name in NAMES.items():
        rr = rows_by[tag]
        cov[name] = {"rows": len(rr), "samplers": dict(Counter(r["meta"]["sampler"] for r in rr)),
                     "cards": len({r["meta"]["card_id"] for r in rr}),
                     "domain_packs": len({r["meta"]["domain_pack"] for r in rr}),
                     "persona_seeds": len({r["meta"].get("persona_seed") for r in rr if r["meta"].get("persona_seed")}),
                     "format_styles": len({r["meta"]["format_style"] for r in rr}),
                     "containers": dict(Counter(fpool.style(r["meta"]["format_style"])["container"] for r in rr)),
                     "wordings": len({r["meta"]["wording_id"] for r in rr}),
                     "defs_style": dict(Counter(r["meta"]["defs_style"] for r in rr)),
                     "subtype": dict(Counter(str(r["meta"]["subtype"]) for r in rr))}
    m = {"family": C.FAMILY, "spec_id": C.SPEC_ID, "g0_sha256": C.SPEC_SHA256, "gen_version": C.GEN_VERSION,
         "written_utc": C.utc(),
         "binding": {"G0_SPEC.md": sha256_file(C.SPEC_FILE), "BUILDER_BRIEF.md":
                     sha256_file(LEAN / "c_spec" / "BUILDER_BRIEF.md"),
                     "decoder_io.py": sha256_file(LEAN / "decoder_io.py"),
                     "train_decoder.py": sha256_file(LEAN / "train_decoder.py"),
                     "sealed_suite_A15": C.SEALED_SUITE_SHA256,
                     "tokenizer": "Qwen/Qwen3.5-4B (local HF cache, local_files_only)"},
         "files": files, "relations": rels, "mixdev_separation": sep, "parents": parents, "coverage": cov,
         "gates": gates, "code": {p.name: sha256_file(p) for p in sorted(list(GEN.glob("*.py")) + list(GEN.glob("*.gz")))},
         "deviations": DEVIATIONS, "problems": probs}
    json.dump(m, open(OUT / "MANIFEST.json", "w"), indent=1, default=str)
    QC.mkdir(exist_ok=True)
    pool = {}
    for name in NAMES.values():
        for suf in (".jsonl", ".relations.jsonl"):
            pool[f"{name}{suf}"] = sha256_file(OUT / f"{name}{suf}")
    failed = [p for p in probs]
    qr = {"report": "F11 round-1 generator QC (gen:F11, c-lanes-v3)", "written_utc": C.utc(),
          "gen_version": C.GEN_VERSION, "inputs_sha256": {"G0_SPEC.md": sha256_file(C.SPEC_FILE)},
          "rows": {n: files[f"{n}.jsonl"]["lines"] for n in NAMES.values()}, "pool_sha256": pool,
          "gates": {n: {"G2_G3_inline_check_failures": gates[n]["gates"]["G2_G3_inline_check_failures"],
                        "G4": gates[n]["gates"]["G4"], "G15_check_rows": gates[n]["gates"]["G15_check_rows"],
                        "G15_loader_fail_second_perm": gates[n]["gates"]["G15_loader_fail_second_perm"],
                        "G15_unit_sizes": gates[n]["gates"]["G15_unit_sizes"],
                        "tokens_served": gates[n]["gates"]["tokens_served"],
                        "tokens_fields_x2instr": gates[n]["gates"]["tokens_fields_x2instr"],
                        "G18": gates[n]["gates"]["G18"], "negation": gates[n]["gates"]["negation"],
                        "sealed_check": {"hits": gates[n]["sealed_check"]["hits"],
                                         "report_kinds": gates[n]["sealed_check"]["report_kinds"]}}
                    for n in NAMES.values()},
          "mixdev_separation": sep, "failed_gates": failed, "pass": not failed,
          "problems": probs}
    # G2 (solver B, solverB/solver_b.py -> solverB/mismatch.json): must be a run on exactly these pools
    mm_p = C.F11 / "solverB" / "mismatch.json" if hasattr(C, "F11") else Path(__file__).resolve().parents[1] / \
        "solverB" / "mismatch.json"
    if mm_p.exists():
        mm = json.load(open(mm_p))
        chk = {n: mm.get("files", {}).get(n, {}).get("sha256") for n in NAMES.values()}
        same = all(chk[n] == pool.get(f"{n}.jsonl") for n in NAMES.values())
        qr["g2_solver_b"] = {"tool": "solverB/solver_b.py", "solver_sha256": mm.get("solver_sha256"),
                             "utc": mm.get("utc"), "rows": {n: mm["files"][n]["rows"] for n in NAMES.values()
                                                            if n in mm.get("files", {})},
                             "mismatches": mm.get("total_mismatch"), "pool_sha256_checked": chk,
                             "pools_match_current": same, "mismatch_json_sha256": sha256_file(mm_p),
                             "pass": bool(same and mm.get("total_mismatch") == 0)}
        if not qr["g2_solver_b"]["pass"]:
            qr["failed_gates"].append("G2 solver B (stale or mismatches)")
            qr["pass"] = False
    json.dump(qr, open(QC / "QC_REPORT.json", "w"), indent=1, default=str)
    progress(f"MANIFEST + QC_REPORT written: rows {qr['rows']}, pass {qr['pass']}, problems {probs or 'none'}")
    print(json.dumps({"rows": qr["rows"], "separation": sep, "pass": qr["pass"], "problems": probs,
                      "parents": len(parents)}, indent=1))


if __name__ == "__main__":
    main()

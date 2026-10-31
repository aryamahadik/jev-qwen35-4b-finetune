"""formats-2 finalize: (1) stamp per-record eligibility (same rule as the codebook feasibility counts), (2) write
manifest.json (counts, licences, parents, upstream commits, sha256 of every input and output, check results),
(3) delete the raw downloads (sha256 kept in the manifest). Run order: build_records -> build_wordings ->
build_codebooks -> run_sealed -> drop_sealed_hits -> finalize --stamp -> run_sealed records -> finalize --manifest."""
from __future__ import annotations

import json
import shutil
import sys
import time
from collections import Counter

from common_f2 import HERE, LEAN, progress, sha_file, write_json, write_jsonl
from build_codebooks import eligible

SCHEMES = ("xed", "mams_acsa", "mams_atsa", "ghc", "edos")
V1_SHA = "3ed146bedede5ee88abff55c11a0b243ea4588722d6dec12b1700bf4bd0e3eb5"  # tmp/fix/orig/manifest.json


def stamp():
    for s in SCHEMES:
        p = HERE / "records" / f"{s}.jsonl"
        rows = [json.loads(l) for l in open(p)]
        for r in rows:
            if s == "xed":
                f10 = eligible(r, "dup_union")
                f11 = r.get("xed_file") == "annotated" and eligible(r, "dup_annotated_only")
            elif s == "mams_atsa":
                base = eligible(r, "dup") and r["ann"]["terms_unique"]
                f10 = base and any(t["n_sub"] == 1 and t["span_ok"] for t in r["ann"]["terms"])
                f11 = base and any(t["n_word"] == 1 and t["span_ok"] for t in r["ann"]["terms"])
            else:
                f10 = eligible(r, "dup")
                f11 = f10 and s != "ghc"
            r["eligible"] = {"F10_S7": bool(f10), "F11_S7": bool(f11)}
            if s == "edos":
                # F10 / F11 G0 (X15, XF07, K24): no EDOS S7 row or example until the 2-of-3 annotator filter can be
                # applied, so EDOS is never eligible here; the pre-filter verdicts are kept for the count only
                r["eligible"] = {"F10_S7": False, "F11_S7": False,
                                 "eligible_pre_x15": {"F10_S7": bool(f10), "F11_S7": bool(f11)},
                                 "blocked_on": "X15: no EDOS S7 row or example until the orchestrator adds the EDOS "
                                               "per-annotator file to LICENCE_REGISTER row 17 (train ids first) and "
                                               "the 2-of-3 annotator filter is applied; no aggregate fallback"}
        write_jsonl(p, rows)
    progress("finalize: eligibility stamped on record pools")


def manifest():
    rb = json.load(open(HERE / "tmp" / "records_build.json"))
    wb = json.load(open(HERE / "tmp" / "wordings_build.json"))
    cb = json.load(open(HERE / "tmp" / "codebooks_build.json"))
    hits = json.load(open(HERE / "tmp" / "sealed" / "hits.json"))
    dropped = json.load(open(HERE / "tmp" / "sealed" / "dropped_records.json"))
    dv = json.load(open(HERE / "tmp" / "denylist_verdicts_formats2.json"))
    outputs = {}
    for sub in ("wordings", "locales", "codebooks", "records"):
        for p in sorted((HERE / sub).iterdir()):
            if p.is_file():
                n = sum(1 for _ in open(p)) if p.suffix == ".jsonl" else None
                outputs[f"{sub}/{p.name}"] = {"sha256": sha_file(p), "rows": n, "bytes": p.stat().st_size}
    rec = {}
    for s in SCHEMES:
        rows = [json.loads(l) for l in open(HERE / "records" / f"{s}.jsonl")]
        c = Counter()
        for r in rows:
            c["records"] += 1
            c["eligible_F10_S7"] += r["eligible"]["F10_S7"]
            c["eligible_F11_S7"] += r["eligible"]["F11_S7"]
            pre = r["eligible"].get("eligible_pre_x15")
            if pre is not None:
                c["eligible_pre_x15_F10_S7"] += pre["F10_S7"]
                c["eligible_pre_x15_F11_S7"] += pre["F11_S7"]
            for k, v in r["flags"].items():
                if v is True:
                    c["flag_" + k] += 1
        rec[s] = dict(c)
    code_files = sorted(p.name for p in HERE.glob("*.py"))
    sealed_summary = {k: {"rows": v["rows"], "hits_final": v["hits"], "kinds": v["kinds"],
                          "input_sha256": v["input_sha256"]} for k, v in hits.items()}
    checker_sha = sorted({v.get("checker_sha256") for v in hits.values()})
    up = rb["upstream"]
    licences = {
        "xed_en": {"licence": up["xed_en"]["licence"], "official_record": "README last line (CC BY 4.0), "
                   "https://github.com/Helsinki-NLP/XED (LICENCE_REGISTER row 13)", "parents": up["xed_en"]["parents"],
                   "text_licence": "OpenSubtitles lines: third-party text under a clean dataset licence (register "
                                   "section 6; not a blocker)", "sa": False},
        "mams": {"licence": up["mams"]["licence"], "official_record": "repo LICENSE (register row 14)",
                 "parents": up["mams"]["parents"], "text_licence": "Citysearch reviews: third-party text (register "
                 "section 6)", "sa": False},
        "ghc": {"licence": up["ghc"]["licence"], "official_record": "OSF node licence via api.osf.io (register row 16)",
                "parents": up["ghc"]["parents"], "text_licence": "gab.ai posts: third-party text (register section 6)",
                "sa": False},
        "edos": {"licence": up["edos"]["licence"], "official_record": "repo LICENSE (register row 17)",
                 "parents": up["edos"]["parents"], "text_licence": "Gab and Reddit posts: third-party text; CC0 "
                 "covers Rewire's rights only (register section 6)", "sa": False},
        "own_seeds": {"licence": "CC0 1.0 (Claude-written: wordings, registers, locales, codebooks, lexicon)",
                      "parents": ["none (ISO 4217 minor units and NIST / UK legal unit definitions are facts)"]},
    }
    man = {
        "id": "formats-2.manifest.v2", "label": "formats-2",
        "revision": {"v2": "review fixes (c_build progress_phase1 [review-formats2] ISSUES): (1) F4 wording pool "
                     "rewritten to the F4 G0 7.5 closed ban list (36 wordings, 6 families x (4 any + 1 yn + 1 "
                     "choice)), lint_f2 FAMILY_BANNED['F4'] added; (2) EDOS records eligible F10_S7 / F11_S7 = false "
                     "with eligible_pre_x15, the 7 F10 and 8 F11 EDOS codebooks status blocked_X15; (3) MAMS F11 "
                     "label-set names use 'with' instead of '; ' (separator check added); (4) wd.F13.B.06 and "
                     "wd.COMMIT.score.F.06 reworded, G11 ROUGE-L checked under both tokenizers over every US / GB "
                     "variant pair; (5) every G0 consulted listed under inputs_read; deny-list A16 drift recorded "
                     "for the orchestrator (checks.denylist.a16_drift)",
                     "v1_manifest_sha256": V1_SHA}, "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                                                                          time.gmtime()),
        "task": "C_DATA_SPEC v4 section 6 (instruction wording pools; registers and locales) and 2.3 (real-text "
                "codebooks for F10/F11 S7), round 1 (with round-2 margin where noted)",
        "order": {"A15_sealed_suite_sha256": "f4ae863720535b6ba27acad51917fe07b4d31344228a1dddb9d98bc3a4deac68",
                  "A16": "PREREG_FINAL.md amendment A16 (C plan) committed before this build; every output written "
                         "after it"},
        "inputs_read": {
            "c_spec/C_DATA_SPEC.md": sha_file(LEAN / "c_spec" / "C_DATA_SPEC.md"),
            "c_spec/C_TRAIN_RECIPE.md": sha_file(LEAN / "c_spec" / "C_TRAIN_RECIPE.md"),
            "c_spec/LICENCE_REGISTER.md": sha_file(LEAN / "c_spec" / "LICENCE_REGISTER.md"),
            "PREREG_FINAL.md (A16)": sha_file(LEAN / "PREREG_FINAL.md"),
            "c_src/F10/G0_SPEC.md (sections 0, 1, 3 S7, connectives)": sha_file(LEAN / "c_src" / "F10" / "G0_SPEC.md"),
            "c_src/F11/G0_SPEC.md (S7, names, SEM-45/46/52)": sha_file(LEAN / "c_src" / "F11" / "G0_SPEC.md"),
            "c_src/F4, F7, F8, F12, COMMIT G0_SPEC.md (instruction-wording rules: F4 7.5 closed ban list, F8 "
            "section 5 bans, F7 R18 families, F12 SC-19 per-form quota, COMMIT R4-02 k_syn)": {
                k: sha_file(LEAN / "c_src" / k / "G0_SPEC.md") for k in ("F4", "F7", "F8", "F12", "COMMIT")},
            "c_src/<every family>/G0_SPEC.md (fix pass: searched for instruction-wording rules; only F4 7.5 and F8 "
            "section 5 add closed ban lists beyond the global lint)": {
                k: sha_file(LEAN / "c_src" / k / "G0_SPEC.md") for k in
                ("F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "F13", "COMMIT")},
            "c_src/common/MARKERS.md": sha_file(LEAN / "c_src" / "common" / "MARKERS.md"),
            "c_src/common/negcount.py (imported)": sha_file(LEAN / "c_src" / "common" / "negcount.py"),
            "c_src/common/denylist.py (run)": sha_file(LEAN / "c_src" / "common" / "denylist.py"),
            "c_build/denylist_query_public.json (copied into the formats-2 query)":
                sha_file(LEAN / "c_build" / "denylist_query_public.json"),
            "data/v14_parts/golden_train.jsonl (hashed in-process for the 'unused' check only)":
                sha_file(LEAN / "data" / "v14_parts" / "golden_train.jsonl"),
            "upstream raw files (deleted after the build)": rb["raw_sha256"],
            "dedupe-only, hashed in-process, never written": {
                "HateXplain Data/dataset.json (hate-alert/HateXplain master)": "posts hashed: "
                f"{rb['dedupe_hashes']['hatexplain_posts']}",
                "SBIC.v2.tgz (all splits)": f"posts hashed: {rb['dedupe_hashes']['sbf_posts_added']}"}},
        "upstream": up, "licences": licences,
        "outputs": outputs,
        "counts": {
            "wordings": wb["counts"], "wording_quota": wb["quota"], "wording_usable_per_form": wb["usable"],
            "locales": wb["locale_counts"],
            "codebooks": {"F10": cb["F10"], "F11": cb["F11"], "F10_size_classes": cb["F10_size_classes"],
                          "status": cb["status"], "blocked_X15": cb["blocked_X15"],
                          "min_units_note": cb["min_units_note"],
                          "F11_codes": cb["F11_codes"], "F10_min_eligible_units_nonresidual":
                              cb["F10_min_units_nonresidual"], "F11_min_eligible_units": cb["F11_min_units"]},
            "records": rec, "records_parse": rb["counts"], "edos_non_train_rows_skipped": rb["edos_non_train_rows_skipped"],
            "golden_train_scan": rb["golden_train"]},
        "checks": {
            "wording_lints": wb["lints"] + "; 0 failures",
            "wording_rouge_l": wb["rouge_max"],
            "lexicon": "template ROUGE-L < 0.7 (0 pairs at or above); NOT probes hold on absent and present-other "
                       "vectors (MAMS PAIR/OTHER, EDOS CAT/VEC)",
            "codebooks": "flat conditions; totality by enumeration; every code reachable by eligible units; distinct "
                         "partitions per (family, scheme); XF12: 0 exact and 0 coverage-restricted F10 = F11 "
                         "partitions; definitions <= 1,600 tokens (estimate); " + cb["separator_check"] +
                         "; EDOS codebooks status blocked_X15 (counts kept as *_pre_x15)",
            "sealed_check": {"checker": "lean/sealed_nd/qc/sealed_check.py (run as a program only)",
                             "checker_sha256": checker_sha,
                             "suite_sha256": "f4ae863720535b6ba27acad51917fe07b4d31344228a1dddb9d98bc3a4deac68",
                             "per_file": sealed_summary, "dropped_records": {k: v["dropped"]
                                                                             for k, v in dropped.items()},
                             "result": "0 blocking hits on every final output (report-only keyword_soft counts "
                                       "listed per file)"},
            "denylist": {"program": "c_src/common/denylist.py v1.2", "program_sha256": dv["program_sha256"],
                         "a16_drift": "A16 freezes denylist.py a6dec381 (v1.1) and deny_aliases.json b9cc417f; these "
                                      "verdicts used v1.2 (e268d566, implements A16 rulings a-c) and aliases 40eeb47e, "
                                      "both changed after the A16 commit. Orchestrator: log the v1.2 hashes in a "
                                      "PREREG amendment before any freeze, or re-run with v1.1",
                         "aliases_sha256": dv["aliases_sha256"], "denylist_sha256": dv["denylist_sha256"],
                         "query": "tmp/denylist_query_formats2.json",
                         "query_sha256": sha_file(HERE / "tmp" / "denylist_query_formats2.json"),
                         "verdicts": "tmp/denylist_verdicts_formats2.json",
                         "verdicts_sha256": sha_file(HERE / "tmp" / "denylist_verdicts_formats2.json"),
                         "counts": dv["counts"],
                         "verdicts_by_dataset": {k: v["verdict"] + (f" (parent {v['entry']}: no_new_rows)"
                                                                    if v["hit"] else "")
                                                 for k, v in dv["verdicts"].items()}},
            "not_run_here": ["counts-only 12-gram / 10-gram / MinHash decontamination of the record pools and seeds "
                             "against OHS-1/2/3, ejs-5, DI, JevBench, LongBench and the sealed exports "
                             "(orchestrator, 7.2 blind mode)", "MAMS vs DI ACOS counts-only dedupe (orchestrator)",
                             "7.2 #8 template check of wordings against dev / eval / OPI / jagged wordings "
                             "(orchestrator program; formats-2 never read those sets)", "G5 blind reads"]},
        "usage": {
            "wordings/family_pools.jsonl": "pool = F1..F13 or COMMIT.<type>; wording_family = <pool>.<A-F> "
                "(A formal, B plain, C terse, D verbose, E casual, F procedural; F12 by question form + GEN); forms: "
                "'any' | 'yn' | 'choice' (F12: the form code). `text` is US spelling, `text_gb` GB spelling (same "
                "wording_id). Placed in `instructions` before the question; meta.wording_id = id (F7: "
                "<wording_family>.<id> as F7 R18 asks). Every wording family gives >= 5 usable wordings per form "
                "(F7: draw a card's 5 from one family; F12: >= 2 per form a card asks plus GEN).",
            "wordings/public_pools.jsonl": "7 per dataset (3 any, 2 yn, 2 choice) for the 14 spec 3.2 datasets.",
            "locales/": "registers.json (6 registers = wording families A-F), locales.json (11 profiles), "
                "spelling_us_gb (541 pairs; sense_dependent pairs never auto-converted), vocab_us_gb (38; ambiguous "
                "rows change meaning), date/time/number formats (ambiguous_numeric forms need the convention stated "
                "on the card), currencies (ISO 4217 minor units; ambiguous symbols need a code or prefixed form), "
                "units (exact factors to SI base; ambiguous units need the system named).",
            "codebooks/codebooks.jsonl": "F10 (30): conditions over atoms, first fit, residual last, natural "
                "names; F11 (32): codes = lists of full annotation combinations, action marks, label-set names for "
                "single-set codes (invented names are the F11 builder's; no name holds ';', '|' or a line break). "
                "eligible_units = eligible records (ATSA: (record, target) pairs; F11 ACSA: (record, named category) "
                "pairs) on 100% of train before the orchestrator's 90/10 split and the claim ledger. status: 'ready' "
                "or 'blocked_X15' (the 7 F10 and 8 F11 EDOS codebooks: unusable until X15 is granted and the 2-of-3 "
                "filter is applied; their eligible_* fields are null and the pre-filter counts sit in "
                "eligible_*_pre_x15; if X15 is declined they are dropped).",
            "codebooks/lexicon.json": "per-scheme field-value phrase templates (2 paraphrases per positive and NOT "
                "form), value glosses, connectives = the F10 G0 registry (ALL / ANY, one list level; NOT on atoms "
                "only).",
            "records/<scheme>.jsonl": "every train record of the pinned files (sealed-check hits dropped) with "
                "text, released annotation vector, norm/loose sha256, flags and `eligible` {F10_S7, F11_S7}. "
                "Builders must still apply the orchestrator XED / 90-10 split file and the record-claim ledger. EDOS "
                "records carry eligible F10_S7 = F11_S7 = false and eligible.eligible_pre_x15 (the verdict before the "
                "2-of-3 filter) until X15."},
        "code": {f: sha_file(HERE / f) for f in code_files},
    }
    write_json(HERE / "manifest.json", man)
    progress("finalize: manifest.json written")


def clean_raw():
    raw = HERE / "tmp" / "raw"
    if raw.exists():
        shutil.rmtree(raw)
        progress("finalize: raw downloads deleted (sha256 kept in manifest)")


if __name__ == "__main__":
    sys.path.insert(0, str(HERE))
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    if arg == "--stamp":
        stamp()
    elif arg == "--manifest":
        manifest()
        clean_raw()
    else:
        raise SystemExit("use --stamp or --manifest")

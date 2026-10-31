#!/usr/bin/env python3
"""public-1 manifest: counts, licences, parents, deny-list verdicts, sealed-check results, per-item filter logs and
sha256 of every output. Also writes out/public1_g5_sample_ids.json (G5 read: 100 rows per dataset, 300 for SQuAD 2.0;
stratified by framing and gold). Never prints row text."""
from __future__ import annotations

import datetime
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[2]
sys.path.insert(0, str(HERE / "lib"))
from common import OUT, LOGS, TMP, SEED, GEN_VERSION, stable_shuffle, LONG_TOKENS  # noqa: E402


def fsha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


DS_INFO = {
    "c_pub_squad2": {"spec_row": "3.2 #1", "dataset": "SQuAD 2.0", "block": "3A", "target_r1": 900,
                     "licence": "CC BY-SA 4.0", "share_alike": True,
                     "official_record": "https://rajpurkar.github.io/SQuAD-explorer/", "record_key": "squad2",
                     "data_url": "https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v2.0.json", "dl": "squad2",
                     "upstream_commit": "rajpurkar/SQuAD-explorer@eee5fdbf62f8613a7812b03419e6b29617b74fd1",
                     "parents": ["SQuAD (1.1)", "Wikipedia"], "text_licence": "Wikipedia passages (CC BY-SA)",
                     "split_rule": "train only; split by Wikipedia page title (10% -> mix-tuning dev); v1.1: no train/reserve paragraph whose title, paragraph or sentence any SQuAD/MuSiQue/2Wiki dev row shows",
                     "per_item_filters": "MuSiQue dev_test_singlehop_questions_v1.0.json 'squad2' ids dropped (by id and by normalised question text); paragraphs with any sentence (>= 8 words) in C1 golden_train not used"},
    "c_pub_musique": {"spec_row": "3.2 #2", "dataset": "MuSiQue", "block": "3A", "target_r1": 1000,
                      "licence": "CC BY 4.0 (annotations); rows treated as SA", "share_alike": True,
                      "official_record": "https://github.com/StonyBrookNLP/musique/blob/922ac98f19a2/LICENSE",
                      "record_key": "musique_license",
                      "data_url": "Google Drive file 1tGdADlNjWFaHLeZZGShh2IRcpO6Lv24h (linked from the repo README / download_data.sh)",
                      "dl": "musique", "upstream_commit": "StonyBrookNLP/musique@922ac98f19a201998dbdae6d7f2887a5258dbdeb",
                      "parents": ["SQuAD", "T-REx", "Natural Questions", "MLQA", "Zero Shot RE", "Wikipedia"],
                      "text_licence": "Wikipedia paragraphs (CC BY-SA); CC BY-SA seed questions",
                      "split_rule": "train only (musique_full_v1.0_train); split by page title of supporting paragraphs (10% -> mix-tuning dev); v1.1: non-required paragraphs from own-side pages only; train items showing anything a dev row shows dropped",
                      "per_item_filters": "items whose supporting / twin-specific paragraphs have a sentence in C1 golden_train dropped; other such paragraphs omitted"},
    "c_pub_2wiki": {"spec_row": "3.2 #3", "dataset": "2WikiMultihopQA", "block": "3A", "target_r1": 600,
                    "licence": "Apache-2.0 (annotations); Wikipedia text SA", "share_alike": True,
                    "official_record": "https://github.com/Alab-NII/2wikimultihop/blob/13800e5be57d/LICENSE",
                    "record_key": "2wiki_license",
                    "data_url": "https://www.dropbox.com/s/ms2m13252h6xubs/data_ids_april7.zip (README link)",
                    "dl": "2wiki", "upstream_commit": "Alab-NII/2wikimultihop@13800e5be57df1b4040b9b1588c6c811779e69e9",
                    "parents": ["Wikipedia", "Wikidata"], "text_licence": "Wikipedia (CC BY-SA), Wikidata (CC0)",
                    "split_rule": "train only; comparison + bridge_comparison types only; split by page title of supporting paragraphs; v1.1: distractors from own-side pages only; train items showing anything a dev row shows dropped",
                    "per_item_filters": "items whose supporting paragraph has a sentence in C1 golden_train dropped; other such paragraphs omitted; two-option rows only when both option strings are context titles"},
    "c_pub_quality": {"spec_row": "3.2 #4", "dataset": "QuALITY", "block": "3B", "target_r1": 600,
                      "licence": "CC BY 4.0 (annotations)", "share_alike": False,
                      "official_record": "https://nyu-mll.github.io/quality/", "record_key": "quality_page",
                      "data_url": "https://raw.githubusercontent.com/nyu-mll/quality/f84977c40dbf/data/v1.0.1/QuALITY.v1.0.1.htmlstripped.train",
                      "dl": "quality", "upstream_commit": "nyu-mll/quality@f84977c40dbfef70c9cab48037b7becfc8e45f73",
                      "parents": ["Project Gutenberg", "Slate (Open American National Corpus)", "QuALITY CC BY nonfiction articles"],
                      "text_licence": "Gutenberg US public domain; Slate via OANC (any use incl. commercial; https://anc.org/data/oanc/ re-read); CC BY 4.0 (longshort, freesouls, openaccess)",
                      "split_rule": "train only; split by article (10% -> mix-tuning dev)",
                      "per_item_filters": "per-article licence/source field logged (logs/quality_articles.json); Gutenberg transcriber notes stripped; article <= 7,200 tokens; writer label == gold label; NT pairs need unanimous untimed validators + answerable"},
}


def main():
    fm = json.loads((LOGS / "fetch_manifest.json").read_text())
    files = json.loads((LOGS / "final_files.json").read_text())
    fstats = json.loads((LOGS / "final_stats.json").read_text())
    rows = {n: [json.loads(l) for l in open(OUT / n)] for n in ("public1_rows_r1.jsonl", "public1_reserve.jsonl", "public1_mtdev.jsonl")}
    main_rows = rows["public1_rows_r1.jsonl"]
    real = json.loads((TMP / "real_tokens.json").read_text())   # v1.1: real tokenizer, full chat prompt (G15)
    qc = json.loads((LOGS / "qc_fix.json").read_text())
    per = {}
    for src, info in DS_INFO.items():
        rs = [r for r in main_rows if r["source"] == src]
        if not rs and src == "c_pub_qasper":
            continue
        fr = Counter(r["id"].split("-")[2] for r in rs)
        yn = [r for r in rs if r["qtype"] == "noul"]
        ch = [r for r in rs if r["qtype"] == "choice"]
        toks = [real[r["id"]] for r in rs]
        rec = fm["licence_records"][info["record_key"]]
        dl = fm["downloads"][info["dl"]]
        per[src] = {
            **{k: v for k, v in info.items() if k not in ("record_key", "dl")},
            "licence_record_reread": {"url": rec["url"], "utc": rec["read_utc"], "sha256": rec["sha256"],
                                      "checks_pass": rec["pass"], "saved": f"licence_records/{info['record_key']}"},
            "download": {"archive_sha256": dl["archive_sha256"], "bytes": dl["archive_bytes"],
                         "files": {k: v["sha256"] for k, v in dl["files"].items()},
                         "members_not_extracted": dl.get("members_not_extracted")},
            "rows_r1": len(rs),
            "rows_reserve": sum(r["source"] == src for r in rows["public1_reserve.jsonl"]),
            "rows_mtdev": sum(r["source"] == src for r in rows["public1_mtdev.jsonl"]),
            "framings": dict(fr),
            "yes_no_rows": len(yn), "yes_rate": round(sum(r["gold"] for r in yn) / len(yn), 4) if yn else None,
            "neg_wording_rows": sum(r["role"] == "neg" for r in yn),
            "choice_rows": len(ch), "option_counts": dict(Counter(len(r["options"]) for r in ch)),
            "abstain_option_rows": sum(1 for r in ch if r["meta"].get("nota_variant")),
            "abstain_gold_rows": sum(1 for r in ch if r["meta"].get("abstain_gold")),
            "cards": len({r["meta"]["card_id"] for r in rs}),
            "wordings": len({r["meta"]["wording_id"] for r in rs}),
            "defs_styles": dict(Counter(r["meta"]["defs_style"] for r in rs)),
            "card_routes": dict(Counter(str(r["meta"].get("card_route")) for r in rs)),
            "format_styles": len({r["meta"]["format_style"] for r in rs}),
            "groups": len({r["group_id"] for r in rs}),
            "tokens_note": "real tokenizer (Qwen3.5-4B), full chat prompt, decoder_io cygnet + schema_branch_mark",
            "tokens_total": sum(toks), "tokens_median": sorted(toks)[len(toks) // 2] if toks else 0,
            "tokens_max": max(toks) if toks else 0, "rows_ge_2000_tokens": sum(t >= LONG_TOKENS for t in toks),
            "soft_targets_human_votes": sum(1 for r in rs if r["meta"].get("teacher_src") == "human_votes"),
        }
    # Qasper decision
    ql = json.loads((LOGS / "qasper_arxiv_licences.json").read_text()) if (LOGS / "qasper_arxiv_licences.json").exists() else {}
    qcls = Counter(v["class"] for v in ql.values())
    ok_cls = {"CC BY", "CC BY-SA", "CC0"}
    q_ok = sum(qcls[c] for c in ok_cls)
    qasper = {
        "spec_row": "3.2 #5", "dataset": "Qasper", "target_r1": 350,
        "licence_record_reread": fm["licence_records"]["qasper_page_archived"],
        "download": fm["downloads"]["qasper"],
        "per_paper_arxiv_licence": {"source": "arXiv OAI-PMH GetRecord metadataPrefix=arXiv <license>; absent = arXiv default non-exclusive",
                                    "papers_read": len(ql), "papers_total": 888, "classes": dict(qcls),
                                    "qualifying_cc_by_by_sa_cc0": q_ok, "log": "logs/qasper_arxiv_licences.json"},
        "decision": ("DROPPED: fewer than 150 papers qualify (spec 3.2 #5 / register 1 #5); rows go to QuALITY and F13"
                     if len(ql) == 888 and q_ok < 150 else "PENDING" if len(ql) < 888 else "IN"),
        "fallback_applied": {"QuALITY": "+175 r1 (600 -> 775)", "F13": "+175 r1 (own family; not built here, for the orchestrator/mixer)"}
        if (len(ql) == 888 and q_ok < 150) else None,
        "rows_r1": sum(r["source"] == "c_pub_qasper" for r in main_rows),
    }
    if "c_pub_quality" in per and qasper["fallback_applied"]:
        per["c_pub_quality"]["target_r1"] = 775
        per["c_pub_quality"]["target_note"] = "600 (3.2 #4) + 175 of Qasper's 350 r1 rows (Qasper dropped: < 150 qualifying papers)"
    den = json.loads((HERE / "denylist/verdicts_public1_v12.json").read_text())
    sealed = {}
    for p in ("templates", "dev", "reserve", "main"):
        s = json.loads((TMP / f"stage_{p}.sealedqc.summary.json").read_text())
        h = [json.loads(l) for l in open(TMP / f"stage_{p}.sealedqc.jsonl")]
        sealed[p] = {"rows": len(h), "hit_rows": sum(o["hit"] for o in h),
                     "hit_kinds": dict(Counter(k["kind"] for o in h for k in o["hit_kinds"])),
                     "report_only_rows": sum(1 for o in h if o["report_kinds"]),
                     "report_kinds": dict(Counter(k["kind"] for o in h for k in o["report_kinds"])),
                     "checker_sha256": s.get("checker_sha256"), "suite_sha256": s.get("suite_sha256"),
                     "input_sha256": s.get("input_sha256")}
    sealed_final = {}
    for f in ("public1_templates", "public1_mtdev", "public1_reserve", "public1_rows_r1"):
        s = json.loads((LOGS / "sealed_final" / f"{f}.summary.json").read_text())
        h = [json.loads(l) for l in open(LOGS / "sealed_final" / f"{f}.sealedqc.jsonl")]
        sealed_final[f + ".jsonl"] = {"rows": len(h), "hit_rows": sum(o["hit"] for o in h),
                                      "report_only_rows": sum(1 for o in h if o["report_kinds"]),
                                      "report_kinds": dict(Counter(k["kind"] for o in h for k in o["report_kinds"])),
                                      "checker_sha256": s.get("checker_sha256"), "suite_sha256": s.get("suite_sha256"),
                                      "input_sha256": s.get("input_sha256")}
    # G5 sample ids (blind readers; dataset-level decisions only)
    g5 = {}
    for src in per:
        rs = [r for r in main_rows if r["source"] == src]
        n = 300 if src == "c_pub_squad2" else 100
        strata = defaultdict(list)
        for r in stable_shuffle(rs, "g5", src):
            strata[(r["id"].split("-")[2], str(r["gold"]) if r["qtype"] == "noul" else "ch")].append(r["id"])
        pick, i = [], 0
        keys = sorted(strata)
        while len(pick) < min(n, len(rs)):
            k = keys[i % len(keys)]
            if strata[k]:
                pick.append(strata[k].pop())
            i += 1
        g5[src] = {"n": len(pick), "bar": "drop dataset if > 5% clearly wrong or ambiguous" if src == "c_pub_squad2"
                   else "drop dataset if > 8% clearly wrong", "ids": pick}
    (OUT / "public1_g5_sample_ids.json").write_text(json.dumps(g5, indent=1))
    outputs = {}
    for p in sorted(OUT.glob("*")):
        outputs[p.name] = {"sha256": fsha(p), "bytes": p.stat().st_size,
                           "rows": sum(1 for _ in open(p)) if p.suffix == ".jsonl" else None}
    man = {
        "builder": "public-1 (C_DATA_SPEC v4 3.2 #1-5)",
        "gen_version": GEN_VERSION,
        "v1_1_review_fixes": {
            "review": "review-public-1 (c_build/tmp/review_public1/), verdict ISSUES; v1.0 outputs kept in tmp/fix/v1/",
            "1_choice_cards": "choice-row cards (prose: one_line / rubric) are printed at the start of instructions "
                              "(formats-1 render_row_text order: card text, blank line, wording / question); card field "
                              "None on choice rows; meta.card_route instructions | card | None; yes/no cards unchanged. "
                              "G15 gate: fmt1 card.loader_check (decoder_io 908c08d7, cygnet + schema_branch_mark, "
                              "random option order) with must_show = the authored card, plus the od/text_first render",
            "2_mtdev_split": "two phases: dev rows first (tmp/devx_<ds>.json: titles, paragraph and sentence hashes), "
                             "then train / reserve with every page title, paragraph and >= 8-word sentence shown by any "
                             "SQuAD 2.0 / MuSiQue / 2Wiki dev row excluded; distractors and fill paragraphs only from "
                             "own-side pages (is_dev_page) on both sides; 2Wiki meta.page_titles now lists every shown page",
            "3_golden_near_dup": "per-paragraph filter: >= 50% of word 10-grams in golden_train -> not used",
            "4_duplicate_paragraphs": "contexts deduped by (title, text) and normalised text before sampling (2Wiki, MuSiQue)",
            "5_report": "long rows and lengths now from the real tokenizer on the full chat prompt; QuALITY articles out: "
                        "42 over 7,200 tokens + 1 golden_train sentence overlap (43 of 150)",
            "6_musique_title_cue": "gold supporting paragraph drawn so that P(gold | an option's page title, or its base "
                                   "without a trailing parenthesis, is in the question) ~ 1/k; items whose every "
                                   "supporting title is in the question thinned to the same target",
            "extra_g15": "QuALITY options with a line break (1 v1.0 row split its option line) are whitespace-normalised; "
                         "make_row refuses an option with a line break",
            "qc_fix": {"file": "logs/qc_fix.json", "gate": qc.get("gate"), "leak": qc.get("leak"),
                       "golden_rows_ge_0.5": qc.get("golden", {}).get("rows_ge_0.5"), "dupes": qc.get("dupes"),
                       "musique_title_cue": qc.get("cue"),
                       "g15": {p: {k: v for k, v in x.items() if k != "real_tokens"} for p, x in qc.get("g15", {}).items()
                               if isinstance(x, dict)}},
        },
        "v1_2_repair_round_1": {
            "plan": "PREREG A29 (a) repair:public-1; the 6 Oct QC record is qc/QC_REPORT_prev.json; v1.1 outputs kept in tmp/repair/v11_out/",
            "unused_records_3_1": "root cause: GoldenIndex dropped a paragraph only at >= 50% shared 10-grams and never checked lines; "
                                  "fix: any shared word 10-gram, any >= 6-word line, >= 8-word sentence or full text -> not used, on every "
                                  "paragraph, its shown form (title line + text), every question and QuALITY option; post-render check of "
                                  "every row (whole state, instructions, card, options) = 0 in every set",
            "g6_quality": "root cause: options-only cue (abstain option gold 50% via the NT pair; gold option text style/length); fix: one "
                          "NT row per question with the abstain option gold on exactly 1/4, cross-fitted options-only cue balance "
                          "(gold top-cue on 1/k, gold length rank uniform)",
            "g7_g10_quality_abstain": "abstain gold on 1/4 = p0 1/k (G7) and abstain wrong on 3/4 of rows showing it (G10 >= 50%)",
            "g6_musique_choice": "root cause: page title in option text; fix: position-only options",
            "g6_2wiki": "root causes: yes/no template and entity-name priors, state length; choice disambiguator rule, equal-length ties counted "
                        "as 'not longer', word-count / first-mentioned / question-x-option cues; fix: yes/no pairs inside one template "
                        "and negation count, question score within 0.10 and state length within 10%; choice items with one "
                        "disambiguated name skipped; swap-symmetric selection over (length relation, two cross-fitted cue signs, "
                        "terciles)",
            "g6_squad2": "root cause: question style and metadata (length) cues; fix: length- and style-matched yes/no pairs; choice "
                         "equal direct/inverted per k with style-top and longest on 1/k per (k, inv)",
            "g10_checker": "non-spec small-cell rule removed from qc/qc_gates.py (every cell 50 +/- 2)",
            "g6_qc_sample": "separate QC sample per Wikipedia set (tmp/qcs_<ds>.json, 5,000 yes/no + up to 5,000 choice rows, same "
                            "generator, never in rows/reserve/dev); QuALITY: rows + reserve",
        },
        "created_utc": datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "plan": {"PREREG_FINAL": "A15 suite sha f4ae863720535b6ba27acad51917fe07b4d31344228a1dddb9d98bc3a4deac68; A16 C plan",
                 "C_DATA_SPEC.md": fsha(LEAN / "c_spec/C_DATA_SPEC.md"),
                 "C_TRAIN_RECIPE.md": fsha(LEAN / "c_spec/C_TRAIN_RECIPE.md"),
                 "LICENCE_REGISTER.md": fsha(LEAN / "c_spec/LICENCE_REGISTER.md")},
        "seed": SEED,
        "row_format": "C_DATA_SPEC 2.4 top-level keys exactly (id, group_id, call_id, source, state, qtype, instructions, options, gold, role, card, meta); qtype noul (gold 1 = yes) / choice; no split/track keys (golden_train has them; mixer adds if check_rows needs them). Every row has its own call_id (contrast twins, no relation units); twins share group_id and point at each other in meta.twin_of",
        "outputs": outputs,
        "counts": {"rows_r1": len(main_rows), "target_r1_this_builder": 3450,
                   "target_r1_after_qasper_fallback": 3275 if qasper["fallback_applied"] else 3450,
                   "f13_fallback_rows_r1": 175 if qasper["fallback_applied"] else 0,
                   "reserve": len(rows["public1_reserve.jsonl"]), "mix_tuning_dev": len(rows["public1_mtdev.jsonl"])},
        "datasets": per,
        "qasper": qasper,
        "denylist": {"program": "c_src/common/denylist.py", "program_sha256": den["program_sha256"],
                     "version": den["version"], "aliases_sha256": den["aliases_sha256"],
                     "denylist_sha256": den["denylist_sha256"], "query": "denylist/query_public1.json",
                     "query_sha256": den["query_sha256"], "verdicts": "denylist/verdicts_public1_v12.json",
                     "verdicts_sha256": fsha(HERE / "denylist/verdicts_public1_v12.json"),
                     "note": "v1.2 re-run (repair round 1; same query; summary equal to the v1.1 run denylist/verdicts_public1_v11.json). "
                             "Program v1.2 e268d566 / aliases 40eeb47e differ from the hashes A16 records (v1.1 "
                             "a6dec381 / b9cc417f): orchestrator item (review-public-1 #8)",
                     "counts": den["counts"],
                     "verdicts_by_dataset": {k: {"verdict": v["verdict"], "parent_no_new_rows_pass": v["parent_no_new_rows_pass"]}
                                             for k, v in den["verdicts"].items()}},
        "sealed_check": {"checker": "lean/sealed_nd/qc/sealed_check.py (run as a program; exports never read)",
                         "staged_files": sealed, "assembly": fstats,
                         "final_files_recheck": sealed_final,
                         "rule": "every blocking hit dropped (twin partner too) and refilled from the same dataset x framing reserve; report-only kinds (keyword_soft) are not hits"},
        "golden_train_dedupe": "every passage / paragraph / article checked: any normalised sentence (>= 8 words) or full text already in C1 golden_train (all sources, state + instructions) -> not used (spec 3.1 unused records; covers qnli, gd_answer_equiv, gd_hotpotqa_yesno, gd_feverous, gd_totto_claims, gd_wtq, boolq); v1.2 (repair round 1): any >= 6-word line or ANY shared word 10-gram with golden_train (state, instructions, card, options; tmp index, hashes only), checked on the paragraph and on its shown form (title line + text) -> not used (required paragraph: item dropped; QuALITY: article dropped); every rendered row re-checked (post_golden_* = 0)",
        "not_done_here": ["counts-only 12-gram / 7.2 decontamination vs OHS-1/2/3, sealed exports, DI tests, JevBench, LongBench v2 (QuALITY), TabFact: orchestrator",
                          "G9 crowd scoring (difficulty_bin, crowd_pg are null): free L4",
                          "G5 blind read: out/public1_g5_sample_ids.json lists the samples",
                          "G6/G7/G10/G12/G15 QC agent; meta.option_level: none (no public ordinal rows in round 1)"],
        "notices_file_entries": ["SQuAD 2.0 (Rajpurkar et al.; CC BY-SA 4.0; Wikipedia text)",
                                 "MuSiQue (Trivedi et al.; CC BY 4.0; Wikipedia text CC BY-SA; seed sets SQuAD, T-REx, Natural Questions, MLQA, Zero Shot RE)",
                                 "2WikiMultihopQA (Ho et al.; Apache-2.0; Wikipedia CC BY-SA, Wikidata CC0)",
                                 "QuALITY (Pang et al.; CC BY 4.0; Project Gutenberg public-domain texts, Slate via OANC, CC BY 4.0 articles from The Long+Short, Freesouls, MIT Press open access)"],
        "share_alike_sources": ["SQuAD 2.0", "MuSiQue", "2WikiMultihopQA (Wikipedia text)"],
        "raw_cleanup": "raw downloads deleted after build (see logs/cleanup.log); licence records and logs kept",
    }
    (HERE / "manifest_public1.json").write_text(json.dumps(man, indent=1, ensure_ascii=False))
    print(json.dumps(man["counts"]), json.dumps({k: v["rows_r1"] for k, v in per.items()}))


if __name__ == "__main__":
    main()

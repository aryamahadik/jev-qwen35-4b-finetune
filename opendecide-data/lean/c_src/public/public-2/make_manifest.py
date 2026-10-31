"""Write out/manifest.json for public-2 (counts, licences, parents, sha256, checks, pending gates). No row text."""
import hashlib
import json
from collections import Counter
from pathlib import Path

from p2_common import HERE, LOGS, OUT, RAW, TMP, sha256_file

A15_SUITE_SHA = "f4ae863720535b6ba27acad51917fe07b4d31344228a1dddb9d98bc3a4deac68"


def agg_dir_sha(d):
    h = hashlib.sha256()
    files = sorted(Path(d).rglob("*.json"))
    for p in files:
        h.update(p.relative_to(d).as_posix().encode())
        h.update(sha256_file(p).encode())
    return h.hexdigest(), len(files)


def main():
    raw_sha = {}
    for line in open(LOGS / "raw_sha256.txt"):
        h, p = line.split(None, 1)
        raw_sha[p.strip()] = h
    wt_sha, wt_n = None, 0
    v1_man = TMP / "fix" / "v1" / "manifest.json"
    refetch = None
    if v1_man.exists():  # v1.1: v1's raw tables were deleted after v1; same pinned commit and files
        for k, v in json.load(open(v1_man))["datasets"]["c_pub_hybridqa"]["data_files"].items():
            if k.startswith("WikiTables-WithLinks@"):
                wt_n = int(k.split("(")[1].split()[0])
                wt_sha = v
        if (RAW / "wtwl").exists():  # tables re-fetched in v1.1 (same commit) for newly selected rows' table hashes
            refetch = agg_dir_sha(RAW / "wtwl")
    elif (RAW / "wtwl").exists():
        wt_sha, wt_n = agg_dir_sha(RAW / "wtwl")
    g15 = json.load(open(OUT / "g15_report.json"))
    fin = json.load(open(TMP / "finalize_summary.json"))
    qc = json.load(open(OUT / "qc_report.json"))
    ver = json.load(open(OUT / "verify_report.json"))
    dl = json.load(open(OUT / "denylist_verdicts_public2.json"))
    sealed = {}
    for p in sorted((OUT / "sealedqc").glob("*.summary.json")):
        d = json.load(open(p))
        sealed[p.name.replace(".summary.json", "")] = {k: d[k] for k in ("rows", "rows_hit", "rows_clean",
                                                                         "rows_report_only", "input_sha256")}
        sealed["_checker_sha256"] = d["checker_sha256"]
        sealed["_suite_sha256"] = d["suite_sha256"]
    sealed_drop = json.load(open(TMP / "sealed_drop_ids.json"))
    rows = [json.loads(l) for l in open(OUT / "rows_r1.jsonl")]
    from finalize import DATASETS, TARGETS
    datasets = {
        "c_pub_hybridqa": {
            "spec_row": "3.2 #7 HybridQA", "licence_status": "IN, V (LICENCE_REGISTER section 1 row 7)",
            "licence_record": "https://github.com/wenhuchen/HybridQA/blob/db22fda8c5951438fade3c69d75b350335ba93b3/LICENSE",
            "upstream_commit": "db22fda8c5951438fade3c69d75b350335ba93b3",
            "licence_file_sha256": raw_sha.get("../../licences/hybridqa_LICENSE.txt"),
            "data_files": {"released_data/train.traced.json": raw_sha.get("hybridqa_train.traced.json"),
                           "released_data/train.json (downloaded, not used)": raw_sha.get("hybridqa_train.json"),
                           f"WikiTables-WithLinks@dc066e1a6d5281511d8b73a6107d5ad2824cc2b2 tables_tok + request_tok "
                           f"({wt_n} files, aggregate sha256 of path+file sha256)": wt_sha,
                           **({f"v1.1 re-fetch from the same commit for table hashes of newly selected rows: tables_tok "
                               f"({refetch[1]} files, aggregate sha256 of path+file sha256)": refetch[0]} if refetch else {})},
            "split_used": "train only (dev.json, test.json never downloaded)",
            "document_text": "WikiTables-WithLinks has no LICENSE: Wikipedia tables and intro passages, CC BY-SA (SA)",
            "sa": True,
            "own_dev_split": "page title (table_id without the trailing _N), sha256(normalized) mod 10 == 0",
        },
        "c_pub_wikisql": {
            "spec_row": "3.2 #8 WikiSQL (execute the SQL)", "licence_status": "IN, V (LICENCE_REGISTER section 1 row 8)",
            "licence_record": "https://github.com/salesforce/WikiSQL/blob/cffb423077756d04c1bac5bcd45167c86903fbcb/LICENSE",
            "upstream_commit": "cffb423077756d04c1bac5bcd45167c86903fbcb",
            "licence_file_sha256": raw_sha.get("../../licences/wikisql_LICENSE.txt"),
            "data_files": {"data.tar.bz2": raw_sha.get("wikisql_data.tar.bz2"), "data/train.jsonl": raw_sha.get("data/train.jsonl"),
                           "data/train.tables.jsonl": raw_sha.get("data/train.tables.jsonl"), "data/train.db": raw_sha.get("data/train.db")},
            "split_used": "train only (dev/test members of data.tar.bz2 never extracted)",
            "document_text": "Wikipedia tables, CC BY-SA (SA); crowd-written questions (BSD-3 dataset)",
            "sa": True,
            "own_dev_split": "page_title (else WikiSQL page id), sha256(normalized) mod 10 == 0",
            "labels": "SQL execution: solver A Python over train.tables.jsonl (exact Fractions), solver B SQLite over the "
                      "official train.db with WikiSQL DBEngine semantics; a candidate is kept only when both agree",
        },
        "c_pub_drop": {
            "spec_row": "3.2 #11 DROP", "licence_status": "IN, V (LICENCE_REGISTER section 1 row 11)",
            "licence_record": "drop_dataset/license.txt in https://ai2-public-datasets.s3.amazonaws.com/drop/drop_dataset.zip",
            "upstream_commit": "zip members dated 26 May 2019",
            "licence_file_sha256": raw_sha.get("drop_dataset/license.txt"),
            "data_files": {"drop_dataset.zip": raw_sha.get("drop_dataset.zip"),
                           "drop_dataset/drop_dataset_train.json": raw_sha.get("drop_dataset/drop_dataset_train.json")},
            "split_used": "train only (dev member never extracted; hidden test not available)",
            "document_text": "Wikipedia passages, CC BY-SA 4.0 (whole dataset SA)",
            "sa": True,
            "own_dev_split": "passage id (DROP gives no page title), sha256 mod 10 == 0",
        },
        "c_pub_uci_car": {
            "spec_row": "3.2 #12 UCI Car Evaluation", "licence_status": "IN, V (LICENCE_REGISTER section 1 row 12a)",
            "licence_record": "https://archive.ics.uci.edu/dataset/19/car+evaluation (CC BY 4.0, DOI 10.24432/C5JP48)",
            "upstream_commit": "page read 3 Oct 2026",
            "licence_file_sha256": raw_sha.get("../../licences/uci_car_page.html"),
            "data_files": {"car+evaluation.zip": raw_sha.get("uci_car.zip"), "car.data": raw_sha.get("car.data")},
            "split_used": "own 90/10 by record (no official split); sha256('car:<line>') mod 10 == 0 -> dev",
            "document_text": "attribute tuples of the published DEX model (no third-party text)",
            "sa": False,
            "labels": "published model classes; the card carries the full hierarchy, recovered exactly from the complete "
                      "truth table by function decomposition (Zupan et al. 1997, cited in car.names): 1,728 / 1,728 "
                      "records reproduced; intermediate grades are named A-D (the original DEX value names are not in "
                      "the UCI files)",
        },
        "c_pub_uci_nursery": {
            "spec_row": "3.2 #12 UCI Nursery", "licence_status": "IN, V (LICENCE_REGISTER section 1 row 12b)",
            "licence_record": "https://archive.ics.uci.edu/dataset/76/nursery (CC BY 4.0, DOI 10.24432/C5P88W)",
            "upstream_commit": "page read 3 Oct 2026",
            "licence_file_sha256": raw_sha.get("../../licences/uci_nursery_page.html"),
            "data_files": {"nursery.zip": raw_sha.get("uci_nursery.zip"), "nursery.data": raw_sha.get("nursery.data")},
            "split_used": "own 90/10 by record; sha256('nursery:<line>') mod 10 == 0 -> dev",
            "document_text": "attribute tuples of the published DEX model (no third-party text)",
            "sa": False,
            "labels": "published model classes; card = recovered hierarchy, 12,960 / 12,960 records reproduced; class "
                      "'recommended' (2 records) is never a gold; choice quotas 45/30/45/30 keep the longest-option "
                      "share at 1/k",
        },
    }
    for k, v in datasets.items():
        v["meta_licence"] = DATASETS[k]["licence"]
        v["parents"] = DATASETS[k]["parents"]
        v["source"] = k
        v["rows_r1_target"] = sum(TARGETS[k].values())
    builder_files = {p.name: sha256_file(p) for p in sorted(HERE.glob("*.py"))}
    out_files = {}
    for p in sorted(OUT.glob("*.jsonl")) + [OUT / "qc_report.json", OUT / "verify_report.json", OUT / "g15_report.json",
                                             OUT / "denylist_query_public2.json", OUT / "denylist_verdicts_public2.json"]:
        out_files[p.name] = {"sha256": sha256_file(p), "lines": sum(1 for _ in open(p)) if p.suffix == ".jsonl" else None}
    man = {
        "builder": "public-2 (C_DATA_SPEC.md v4 section 3; 3.2 #7 HybridQA, #8 WikiSQL, #11 DROP, #12 UCI Car + Nursery)",
        "created_utc": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "plan": {"prereg": "PREREG_FINAL.md A16 (C round 1)", "sealed_suite_sha256_A15": A15_SUITE_SHA,
                 "spec": "c_spec/C_DATA_SPEC.md v4", "recipe": "c_spec/C_TRAIN_RECIPE.md v4"},
        "round": 1,
        "version": "v1.1 (review public-2 fixes; v1 outputs and manifest kept in tmp/fix/v1/)",
        "fix_v1_1": {
            "review": "c_build/progress_phase1.log [review-public-2] 21:53:59Z, verdict ISSUES",
            "v1_manifest_sha256": sha256_file(v1_man) if v1_man.exists() else None,
            "items": {
                "1_choice_card_hidden (blocking, G15)": "finalize.route_choice_card: on choice rows only '- {option}: "
                    "{definition}' lines stay in card (decoder_io prints them on the option lines); every other card "
                    "line (rules, UCI model tables / rule lists, notes, worked examples) moves into instructions ahead "
                    "of the wording (schema_branch_mark prints instructions before the options and again after the "
                    "text). UCI masked class codes are written as '- K3: very good' card lines (build_uci.card_text); "
                    "UCI wording uci_ch_w1 says 'the model above'. Yes/no rows unchanged (card printed whole). "
                    "qc_g15.py: 0 rows with any card line hidden, every line of every v1 card present in the prompt.",
                "2_drop_abstain_wrong_below_50": "selection repair keeps abstain-gold at 40-50% of the rows that "
                    "show an abstain option (abstain wrong >= 50%) per framing in rows_r1 (reserve and dev: <= 50%)",
                "3_gold_longest_all_options": "G10 measure now counts every displayed option (abstain included, ties "
                    "split); selection = round robin over (gold-rank bucket, wording), then minimal same-key swaps "
                    "with the leftover pool until |longest-is-gold - mean 1/k| <= 1 pp per framing; reserve trimmed "
                    "to the same targets when no swap is left; stored gold position re-balanced per dataset x "
                    "framing x option count (abstain stays last; sorted numeric rows untouched)",
                "4_c1_named_source_overlap": "golden_train dedup also on the rendered state: lines/sentences >= 8 "
                    "words over all golden_train sources and word 10-grams over the 7 named sources (the reviewer's "
                    "check); counts in candidate_filters (golden_train_drop_rendered:*)",
                "5_missing_2_4_meta_keys": "every row now has domain_pack, sampler (null: public rows have no pack "
                    "or sampler), structure_hash, depth (framing-level step count), deep (false), plus block, c_part, "
                    "share_alike and card_route as in public-1 / public-3; family 'public'",
                "length": "length cap now on the real chat render (decoder_io.render_chat, CYGNET_SYSTEM, cygnet + "
                          "schema_branch_mark, Qwen3.5 tokenizer) < 2,000 tokens, so every row is a non-long row "
                          "(v1 measured card + state + instructions + options only; its real renders reached 2,202)",
            },
        },
        "row_files": {"train_rows": "out/rows_r1.jsonl", "reserve_rows": "out/reserve_r1.jsonl",
                      "mix_tuning_dev": "out/dev_mt_r1.jsonl"},
        "counts": fin["counts"],
        "candidate_filters": fin["filters"],
        "datasets": datasets,
        "parents_declared": {k: v["parents"] for k, v in datasets.items()},
        "outputs": out_files,
        "builder_code_sha256": builder_files,
        "row_meta_git_sha": rows[0]["meta"]["git_sha"],
        "checks": {
            "denylist": {"program_sha256": dl["program_sha256"], "aliases_sha256": dl["aliases_sha256"],
                         "denylist_sha256": dl["denylist_sha256"], "canonical": dl["canonical"], "counts": dl["counts"],
                         "verdicts": {k: v["verdict"] for k, v in dl["verdicts"].items()},
                         "rule": "run at builder start and again at the end with --fail-on-taint (exit 0 both times)"},
            "input_paths": "denylist.py paths: every input path ok (no 7.4 / never-open path)",
            "sealed_check": {"files": sealed, "blocking_hits_after_replacement": 0,
                             "ids_dropped_and_replaced": len(sealed_drop),
                             "run": "sealed_nd/qc/sealed_check.py run as a program on rows, reserve, dev, wordings, "
                                    "cards, styles and table hashes (structure fields state,card,instructions,options "
                                    "on rows); hit ids dropped and refilled from the candidates, then re-run until 0"},
            "golden_train_dedup": "every non-UCI record: exact line/sentence hashes (>= 5 words) over all of "
                                  "golden_train + word 10-grams over qnli, gd_answer_equiv, gd_hotpotqa_yesno, "
                                  "gd_feverous, gd_totto_claims, gd_wtq, boolq (spec 3.1) on the canonical record text; "
                                  "v1.1 adds the rendered state (>= 8-word lines/sentences, all sources; 10-grams, "
                                  "named sources); any hit drops the record",
            "g15_loader_round_trip": g15,
            "dev_vs_train": "dev items share no group_id and no >= 5-word line/sentence with any train candidate",
            "labels_round_trip": ver,
            "qc_report": {part: {k: {kk: v[kk] for kk in ("rows", "yes_rate", "wordings", "gold_longest_rate",
                                                          "gold_longest_expected", "gold_longest_diff_pp",
                                                          "gold_longest_diff_pp_by_framing", "abstain_rows",
                                                          "abstain_wrong_rate", "gold_position_chi2_p_by_k",
                                                          "max_class_count", "tokens_median", "tokens_max",
                                                          "rows_ge_2000_tokens", "card_route")}
                                 for k, v in qc[part].items()} for part in ("rows", "reserve", "dev")},
            "selection_repair": qc.get("repair_swaps"),
            "g7_lite_fails": {k: len(v["fails"]) for k, v in qc["g7_lite_rows"].items()},
            "tokenizer": qc["tokenizer"],
        },
        "notices_entries": [
            "HybridQA - MIT License, Copyright (c) 2020 wenhu chen - https://github.com/wenhuchen/HybridQA",
            "WikiTables-WithLinks (HybridQA tables and passages) - Wikipedia content, CC BY-SA - https://github.com/wenhuchen/WikiTables-WithLinks",
            "WikiSQL - BSD 3-Clause License, Copyright (c) 2017, Salesforce Research - https://github.com/salesforce/WikiSQL; Wikipedia tables CC BY-SA",
            "DROP - CC BY-SA 4.0 - Dua, Wang, Dasigi, Stanovsky, Singh, Gardner (NAACL 2019), Allen Institute for AI",
            "UCI Car Evaluation - CC BY 4.0 - Marko Bohanec (DEX model; Bohanec and Rajkovic 1988, 1990), DOI 10.24432/C5JP48",
            "UCI Nursery - CC BY 4.0 - Vladislav Rajkovic et al. (Olave, Rajkovic, Bohanec 1989; DEX model), DOI 10.24432/C5P88W",
        ],
        "share_alike": "HybridQA, WikiSQL and DROP rows contain CC BY-SA text: private training only, never publish rows",
        "pending_not_this_builder": [
            "G13 counts-only 12-gram decontamination of these rows against OHS-1/2 (orchestrator)",
            "TabFact (OHS-2) table-hash check: out/table_hashes.jsonl gives per-row title+header, cell-set and full "
            "table hashes for every WikiSQL and HybridQA row (spec 7.2 #9; orchestrator)",
            "G5 blind read, 100 rows per dataset by a non-author reader (dataset-level drop if > 8% clearly wrong)",
            "G6 partial-input baselines and G8 on our framings (QC agent)",
            "G12 MinHash near-dup across all C rows (QC agent / mixer); G15 is run here (qc_g15.py, v1.1) and "
            "should be re-run by the mixer on the mixed set",
            "G9 crowd scoring only if the orchestrator applies it to public rows (A16: D2 not adopted)",
        ],
    }
    json.dump(man, open(OUT / "manifest.json", "w"), indent=1, ensure_ascii=False)
    print(sha256_file(OUT / "manifest.json"))


if __name__ == "__main__":
    main()

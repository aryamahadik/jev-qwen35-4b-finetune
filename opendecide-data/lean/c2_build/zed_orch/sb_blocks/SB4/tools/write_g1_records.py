#!/usr/bin/env python3
"""Writes SB4/checks/G1_RECORD.json, SOURCE_CHECK_REQUEST.json, denylist_query_sb4.json and SB4_REPORT.json (round 1).
Plain facts only; no row text. Run: ../../../../../../.venv/bin/python -I -B tools/write_g1_records.py"""
import hashlib, json
from pathlib import Path
SB4 = Path(__file__).resolve().parent.parent
sha = lambda p: hashlib.sha256((SB4 / p).read_bytes()).hexdigest()
m = json.loads((SB4 / "checks/g1_ant_match.json").read_text())
ov = json.loads((SB4 / "checks/g1_split_overlap.json").read_text())

g1 = {
 "block": "SB4", "step": "G1 (A58 c.1)", "date_utc": "2026-10-16", "verified_by": "Sonnet 5.5 round-1 chain SB4",
 "ans": {
  "name": "ANS, Arabic News Stance Corpus (stance-prediction version)",
  "repo": "https://github.com/latynt/ans", "pinned_commit": "9c5f313ab225880b9f60f4e795e6afb4da3352c8",
  "tarball_sha256": "9522e1f13449d636f12ada5860b023f3f320b74725f380de820a82d315375b05",
  "files_extracted": {"readme.md": sha("src/readme.md"), "data/stance/train.csv": sha("src/data/stance/train.csv"),
                      "data/stance/dev.csv": sha("src/data/stance/dev.csv")},
  "test_file": "not extracted, never opened",
  "repo_files_at_commit": ["ans.png", "readme.md", "data/claim/{train,dev,test}.csv", "data/stance/{train,dev,test}.csv"],
  "no_LICENSE_file": True, "github_api_license_field": None,
  "licence_line_quoted_from_raw_readme": "[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)",
  "licence_note": "The only licence statement in the creator's readme.md is this Apache-2.0 badge (line 1). There is no LICENSE file. A58 (b) accepts a README statement quoted raw with its sha256.",
  "readme_usage_quote": "For reproduciblity, we are sharing the dev and test splits. By submitting results using the same splits, you acknowledge that your results are obtained purely by training on the training split and tuned on the dev split (you only evaluted on the test set once).",
  "columns": "s1, s2, stance (agree / disagree / other); no source, id, ANT or headline-id field",
 },
 "paper": {
  "url": "https://arxiv.org/abs/2005.10410", "pdf_sha256": sha("paper/2005.10410.pdf"),
  "title": "Stance Prediction and Claim Verification: An Arabic Perspective (Khouja, FEVER 2020)",
  "licence_statement_in_paper": "none (no licence or Apache text anywhere in the paper)",
  "data_creation_quote_3_1": "We derive our corpus by sampling a subset of news titles from the most recent version of the Arabic News Texts (ANT) corpus (Chouigui et al., 2017); A collection of Arabic news from multiple news media sources in the Middle East.",
  "annotation_quote_3_1": "We used crowdsourcing to generate true/false claims. Starting from a news title, we recruited annotators to modify each news title into a new claim. For true claims, annotators were asked to paraphrase the original title ... We relied on Amazon Mechanical Turk and Upwork to recruit annotators. We only considered Arabic native speakers for news title rewriting.",
  "validation_quote_3_2": "three classes - paraphrase, contradiction, other/not enough information for each pair of news titles ... A total of 4,259 pairs were labeled by 3 to 5 annotators. We considered the author's rewritten sentences as labels (for the paraphrase and contradict classes) ... For the final data, we included only pairs with inter annotator agreement of 75% or higher.",
  "other_class_quote": "To present annotators with a small set of the third class (other), we first considered randomly pairing news titles from our corpus ... we used a similarity metric to select pairs that look more similar.",
  "data_statement_A1_quote": "Part of the dataset was a random subset of the ANT corpus which was created through webcrawling news sources in the Middle East.",
  "data_statement_A3_quote": "The dataset includes a subset of the news titles from ANT news corpus (v2.1) which included 5 news sources (BBC, Al Arabiya, CNN, Sky News, France24) and 6 categories (culture, economy, international news, Middle East, sport, technology) collected from February 2018 to October 2018.",
  "label_method": "paraphrase and contradiction labels are the rewriting worker's own intent, validated by 3-5 other annotators (agreement >= 75% kept); other = similar-looking pairs of different titles, annotated by 3-5 workers.",
 },
 "ant_question": {
  "rows_come_from_ant": "YES. Paper 3.1 and A.3: the reference headlines are a sampled subset of ANT v2.1; the claims are crowd rewrites of those headlines. Title match against ANT v2.1 at the pinned commit (counts only, tools/g1_ant_match.py): "
        f"train {m['train']['rows_with_any_side_matching_ant']} of {m['train']['rows']} rows have at least one side equal or near-equal (word-set Jaccard >= 0.8) to an ANT v2.1 title; dev {m['dev']['rows_with_any_side_matching_ant']} of {m['dev']['rows']}. "
        "The other train rows are derivatives of ANT titles that are not in the published v2.1 (the paper says only that the dataset 'includes a subset' and 'part' is ANT), so ANT origin cannot be excluded for them.",
  "identifiable_by_a_field": "NO. The csv has only s1, s2, stance. Both columns hold references and claims (s1 repeated values: "
        f"{m['train']['s1_repeats']['rows_with_repeated_value']} rows; s2: {m['train']['s2_repeats']['rows_with_repeated_value']}; {m['train']['s1_values_also_in_s2']} values occur in both columns). Only a title match could separate rows, and it leaves "
        f"{m['train']['rows'] - m['train']['rows_with_any_side_matching_ant']} train rows unattributed.",
  "ant_repo_v2_1": "https://github.com/antcorpus/antcorpus.multisource.data", "ant_pinned_commit": "f117ce44a9cfad0dcbd341b7d744e4c3cdb4fed8 (HEAD; tag v2.1 = 691b0107c298374e639ac12d6c73d1fcc73a6ef5)",
  "ant_tarball_sha256": "ebe1219cdb68e40206d5407bee8d7ee54f8c5a89828639eed7ca358351283b7f", "ant_v2_1_titles": m["ant_titles"],
  "ant_readme_raw_sha256": "d902181deeb993f6af11d667017f5a06629d03f92d76648a946794b5d36db960", "ant_readme_copy": "ant_probe/ant_v21_README_at_f117ce4.md",
  "ant_project_page": "https://antcorpus.github.io", "ant_project_page_sha256": sha("ant_probe/antcorpus_github_io.html"),
  "ant_licence_statements_in_official_records": [
    {"where": "antcorpus.multisource.data README.md, section 'Citation Licence'", "quote": "The files of ANT Corpus are subject to the following citation license: By downloading ANT Corpus, you agree to cite at least one of our papers describing ANT Corpus and/or refer the project's main page in any kind of material you produce where ANT Corpus was used to conduct search or experimentation, whether be it a research paper, dissertation, article, poster, presentation, or documentation."},
    {"where": "antcorpus.multisource.data README.md, last lines", "quote": "Copyright (C) 2019 All Rights Reserved. RIADI-ENSI, University of Manouba & ENISo, University of Sousse."},
    {"where": "antcorpus.multisource.data README.md, last line", "quote": "![Licence](https://img.shields.io/badge/licence-Apache_2.0-blue.svg)  (an image badge)"},
    {"where": "antcorpus.github.io project page, 'Licence'", "quote": "The files of ANT Corpus are subject to the following citation license ... By using this data, you have agreed to the citation licence."},
    {"where": "GitHub repo metadata and file list of antcorpus.multisource.data", "quote": "no LICENSE file; license field null"},
    {"where": "sibling repo antcorpus.data (v1.0 / v1.1, one source, JawharaFM only)", "quote": "has a LICENSE file: Apache License 2.0 (sha256 b40930bb...). It does not cover v2.1; ANS uses v2.1."},
  ],
  "ant_text_origin": "RSS articles of BBC, Al Arabiya, CNN, Sky News and France24 (third-party press text, scraped).",
  "ant_licence_is_V": "NOT V, by the strict reading. The v2.1 official record gives three different statements (a custom citation licence, 'All Rights Reserved', and an Apache-2.0 image badge) and no LICENSE file; a citation licence is not on GOLDEN_SPEC rule 3's list; GOLDEN_SPEC says 'when unsure, reject'; A58 (a)1-2 needs the upstream dataset's licence V when text comes through it.",
  "counter_argument": "A58 (b) accepts ANS's own README Apache-2.0 badge as a statement; ANT's v2.1 README carries the same kind of badge, and LICENCE_REGISTER (text licence paragraph) says press headlines under a clean dataset licence are not a blocker. If the orchestrator rules the ANT Apache badge V in spite of the 'All Rights Reserved' and citation-licence text, G1 passes and the chain continues at step 2.",
  "g1_status": "UNRESOLVED. Per the task and A58 (b), the chain stops here and reports. Nothing further is built.",
 },
}
(SB4 / "checks/G1_RECORD.json").write_text(json.dumps(g1, indent=1, ensure_ascii=False) + "\n")

req = {
 "block": "SB4", "purpose": "A58 (c) 2 (A42-D 8.5 sealed-side source-name check) and (c) 3 (denylist.py check --fail-on-taint). Run by the orchestrator only. No row has been written.",
 "status": "NOT REQUESTED YET: wait for the G1 ruling on ANT (checks/G1_RECORD.json ant_question). If SB4 is out, discard.",
 "source_identifiers": ["ANS", "Arabic News Stance", "Arabic News Stance Corpus", "latynt/ans", "github.com/latynt/ans", "latynt",
   "Khouja", "Stance Prediction and Claim Verification: An Arabic Perspective", "arXiv 2005.10410", "arxiv.org/abs/2005.10410",
   "FEVER 2020 workshop", "ANT corpus", "Arabic News Texts", "ANT Corpus: An Arabic News Text Collection for Textual Classification",
   "antcorpus", "antcorpus.github.io", "Chouigui"],
 "upstream_press_sources_of_ANT_text_not_put_in_the_query_to_avoid_platform_word_false_hits": ["BBC Arabic", "Al Arabiya", "CNN Arabic", "Sky News Arabia", "France24 Arabic"],
 "query_file": "checks/denylist_query_sb4.json",
 "denylist_command": "cd lean && ../.venv/bin/python c_src/common/denylist.py check --query c2_build/zed_orch/sb_blocks/SB4/checks/denylist_query_sb4.json --out c2_build/zed_orch/sb_blocks/SB4/checks/denylist_verdicts_sb4.json --fail-on-taint",
 "also_check": ["not in c2_build/gblock/checks/c1_source_names.json (grep found no ANS/ANT/latynt entry)", "not a G-proxy source (A42-D 8.3, A48 e)"],
 "expected_replies": {"8.5": "PASS or HIT per source", "denylist": "no taint verdict"},
}
(SB4 / "checks/SOURCE_CHECK_REQUEST.json").write_text(json.dumps(req, indent=1) + "\n")

q = {"datasets": {"sb4_ans": {
   "name": "ANS Arabic News Stance corpus (stance version, train split), Khouja 2020",
   "names": ["ANS", "Arabic News Stance", "Arabic News Stance Corpus", "latynt/ans", "Khouja 2020"],
   "datasets": ["ANS Arabic News Stance Corpus"], "domains": ["latynt.com"], "url": "https://github.com/latynt/ans",
   "parents": [{"name": "ANT Corpus", "names": ["ANT corpus", "Arabic News Texts", "antcorpus", "ANT news corpus v2.1"],
                "datasets": ["ANT Corpus Arabic News Texts Corpus"], "domains": ["antcorpus.github.io"], "parents": []}],
   "emits_rows": True}}}
(SB4 / "checks/denylist_query_sb4.json").write_text(json.dumps(q, indent=1) + "\n")

rep = {
 "block": "SB4", "ruling": "A58 draft (zed_orch/sb_blocks/A58_DRAFT.md)", "chain": "SB4 round 1", "seed": 20261013,
 "status": "BLOCKED at step 1 (G1): ANT licence unresolved; no row written; nothing downstream started",
 "steps": {
  "1_G1": {"done": True, "verdict": "UNRESOLVED (recommend: ANT licence not V, so SB4 is out under A58 (b)); see checks/G1_RECORD.json",
           "ans_licence": "Apache-2.0 badge in the creator's readme.md (V under A58 (b))", "ans_readme_sha256": sha("src/readme.md"),
           "ans_commit": "9c5f313ab225880b9f60f4e795e6afb4da3352c8",
           "ant_origin_rows": f"all rows derive from ANT titles; {m['train']['rows_with_any_side_matching_ant']}/{m['train']['rows']} train and {m['dev']['rows_with_any_side_matching_ant']}/{m['dev']['rows']} dev rows verifiably contain a verbatim or near-verbatim ANT v2.1 title; no field separates ANT rows"},
  "2_source_check_handoff": {"done": False, "prepared": "checks/SOURCE_CHECK_REQUEST.json and checks/denylist_query_sb4.json", "reply": None,
                              "note": "not requested while G1 is open; no row and no builder code is written before PASS and no taint"},
  "3_read_train_dev": {"done": False},
  "4_bench_exclusion": {"done": False}, "5_write_rows_and_defs": {"done": False}, "6_format_gates": {"done": False},
  "7_candidates_a46_g13_c1_crowd_select": {"done": False}, "8_hypothesis_only_probe": {"done": False},
 },
 "planning_numbers_for_the_orchestrator (counts of the downloaded files, nothing built)": {
  "train_rows": ov["train_rows"], "train_stance": m["train"]["stance"], "dev_rows": ov["dev_rows"], "dev_stance": m["dev"]["stance"],
  "dev_rows_sharing_no_value_with_train": ov["dev_rows_with_no_shared_value"], "dev_clean_stance": ov["dev_clean_stance"],
  "ceiling_note": "A58 (c) 8 caps any class at 40%. Train has 63 'other' rows (2.4%), so with every 'other' row kept the largest stratified set is 63 / 0.2 = 315 rows (126 agree, 126 disagree, 63 other) before dedupe, bench exclusion and the A46 screen; fewer if 'other' rows drop. Candidates would therefore be about 315, not 1,125, and the selected block well under the 750 cap. Never refilled."},
 "files": {"G1_RECORD": "checks/G1_RECORD.json", "ant_match_counts": "checks/g1_ant_match.json", "split_overlap_counts": "checks/g1_split_overlap.json",
           "tools": ["tools/g1_ant_match.py", "tools/g1_split_overlap.py", "tools/write_g1_records.py"],
           "ant_probe_kept": ["ant_probe/ant_v21_README_at_f117ce4.md", "ant_probe/antcorpus_github_io.html", "ant_probe/ant_v1_LICENSE.txt"],
           "ant_data_deleted_after_counting": "ANT v2.1 tarball and extracted files removed; re-fetch by commit f117ce44... and tarball sha256 above"},
 "edits_outside_SB4": "none (c2io.py, g13_c2.py, golden_src untouched this round)",
}
(SB4 / "SB4_REPORT.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False) + "\n")
print("written")

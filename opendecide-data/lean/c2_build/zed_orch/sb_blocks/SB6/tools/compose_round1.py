"""Compose SB6 round-1 records (G1_RECORD.json, HANDOFF_85_DENYLIST.json, denylist_query_sb6.json, STATE.json) from the
saved official records. Reads saved files as text/bytes only. Usage: python3 -I compose_round1.py <SB6 dir>"""
import hashlib, json, sys
from datetime import datetime, timezone
from pathlib import Path

root = Path(sys.argv[1])
src = root / "src"

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def L(p):
    return Path(p).read_text(encoding="utf-8", errors="replace").splitlines()

def seg(p, a, b):
    return " ".join(x.strip() for x in L(p)[a - 1:b])

COMMIT = "43cde6d598c1cf88c1a8b9ed32e89263ffb5e03b"
HFREV = "da78f23f9119363459acbaf46bf89426ff26c259"
now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

files = {}
for rel in ["g1_official/LICENSE", "g1_official/README.md", "g1_paper/tacl_2020_30.pdf", "g1_paper/acl_page.html",
            "g1_wikimedia_2019/terms_of_use_rev116456.txt", "g1_wikimedia_2019/rev.json",
            "g1_wikipedia/terms_of_use.txt", "g1_wikipedia/enwiki_copyrights.txt",
            "g1_hf/hf_api_dataset.json", "g1_hf/hf_tree_primary_task.json", "g1_hf/hf_card_README.md",
            "g1_github/repo_api.json", "g1_github/commit_api.json",
            "g1_gcs_probe/body_dev.xml", "g1_gcs_probe/body_train.xml", "g1_gcs_probe/hdr_dev.txt", "g1_gcs_probe/hdr_train.txt"]:
    files["src/" + rel] = sha(src / rel)

tree = json.load(open(src / "g1_hf/hf_tree_primary_task.json"))
parquet = {e["path"]: {"bytes": e["size"], "sha256": (e.get("lfs") or {}).get("oid")} for e in tree}

lic = src / "g1_official/LICENSE"
paper = src / "g1_paper/tacl_2020_30.txt"

rec = {
    "block": "SB6",
    "ruling": "A58 (draft) (c) 1",
    "verifier": "Sonnet builder (Claude Code), chain SB6 round 1",
    "retrieved_utc": now,
    "dataset": {
        "name": "TyDi QA, primary task (TyDiQA-MinSpan / SelectP), English (+ a small Arabic slice, see owner_request_arabic)",
        "creators": "Clark, Choi, Collins, Garrette, Kwiatkowski, Nikolaev, Palomaki (Google Research)",
        "paper": "TyDi QA: A Benchmark for Information-Seeking Question Answering in Typologically Diverse Languages, TACL 8:454-470, 2020",
        "doi": "10.1162/tacl_a_00317",
        "acl_anthology": "https://aclanthology.org/2020.tacl-1.30/",
        "repo": "https://github.com/google-research-datasets/tydiqa",
        "repo_status": "archived: true on GitHub (last commit 2020-04-30); default branch master",
        "pinned_commit": COMMIT,
        "pinned_commit_date": "2020-04-30T18:54:55Z",
        "hf_data_host": "https://huggingface.co/datasets/google-research-datasets/tydiqa",
        "hf_pinned_revision": HFREV,
        "hf_last_modified": "2024-08-08T05:57:11Z",
        "splits_used": "primary_task train (166,916 examples, single-annotated) for training candidates; primary_task validation (18,670 examples, 3-way annotated) for own dev only; no test",
    },
    "official_records": {
        "licence_file": f"https://raw.githubusercontent.com/google-research-datasets/tydiqa/{COMMIT}/LICENSE",
        "readme_file": f"https://raw.githubusercontent.com/google-research-datasets/tydiqa/{COMMIT}/README.md",
        "github_repo_api": "https://api.github.com/repos/google-research-datasets/tydiqa (license.spdx_id = Apache-2.0)",
        "paper_pdf": "https://aclanthology.org/2020.tacl-1.30.pdf",
        "wikimedia_terms_of_use_in_force_2019_02_01": "https://foundation.wikimedia.org/w/index.php?oldid=116456 (revision of 2018-07-18, the latest before the 2019-02-01 snapshot)",
        "wikimedia_terms_of_use_current": "https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use",
        "enwiki_copyrights_current": "https://en.wikipedia.org/wiki/Wikipedia:Copyrights",
    },
    "sha256": files,
    "licence": {
        "spdx": "Apache-2.0",
        "stated_where": "LICENSE file of the creators' own repository google-research-datasets/tydiqa at the pinned commit (the official record named by A58 (a) 1)",
        "quote_LICENSE_head": {"lines": "2-3", "text": "Apache License / Version 2.0, January 2004"},
        "quote_LICENSE_grant": {"lines": "68-72", "text": seg(lic, 68, 72)},
        "quote_LICENSE_appendix_boilerplate": {"lines": "192-193", "text": seg(lic, 192, 193)},
        "LICENSE_has_no_non_commercial_or_no_derivatives_clause": True,
        "commercial_use_allowed": "yes: the Apache-2.0 grant is a perpetual, worldwide, non-exclusive, no-charge, royalty-free, irrevocable copyright licence to reproduce, prepare Derivative Works of, publicly display, publicly perform, sublicense and distribute (LICENSE lines 68-72); the text has no NC clause",
        "README_licence_lines": "NONE. A case-insensitive search of README.md at the pinned commit for licen|apache|copyright|creative commons|cc by|terms of use|permission finds 0 lines. The README names the data URLs (lines 89-90 and 96-98) and the Wikipedia source snapshots (line 207) and says nothing about the licence of the data files.",
        "hf_card": "The HF card of google-research-datasets/tydiqa lists license apache-2.0 in its YAML header; its 'Licensing Information' section is empty ('More Information Needed'). The card is NOT the evidence: the repo LICENSE is.",
        "attribution_needed": "TyDi QA, Clark et al. 2020, TACL 8:454-470, DOI 10.1162/tacl_a_00317, Apache-2.0 (google-research-datasets/tydiqa); passages from Wikipedia (CC BY-SA, see text_provenance)",
    },
    "text_provenance": {
        "what": "Passages are Wikipedia article text (English and Arabic Wikipedia, Internet Archive snapshots of 2019-02-01).",
        "quote_README_line_207": L(src / "g1_official/README.md")[206].strip() + " " + L(src / "g1_official/README.md")[207].strip() + " (README lines 207-208)",
        "licence_of_that_text": "CC BY-SA (plus GFDL), on the GOLDEN_SPEC rule 3 allowed list",
        "quote_wikimedia_TOU_in_force_2019": {
            "lines": "167-168, 175",
            "text": seg(src / "g1_wikimedia_2019/terms_of_use_rev116456.txt", 167, 168) + " ... " + seg(src / "g1_wikimedia_2019/terms_of_use_rev116456.txt", 175, 175),
        },
        "quote_wikimedia_TOU_current_line_205": "Please note that these licenses do allow commercial uses of your contributions, as long as such uses are compliant with the terms of the respective licenses.",
        "quote_enwiki_copyrights_line_31": L(src / "g1_wikipedia/enwiki_copyrights.txt")[30].strip(),
        "scope": "The Wikimedia Terms of Use cover every Wikimedia project edition, so the Arabic Wikipedia text carries the same licence. This is the builder's reading of the TOU; no separate ar.wikipedia.org page was fetched.",
        "obligations": "CC BY-SA 3.0: attribution and share-alike for the text. The builder keeps document_title and document_url in meta so attribution is recoverable; the rows are a derived training set, and whether share-alike reaches a model is the owner's, not decided here.",
    },
    "label_method": {
        "quote_paper_section_3": "If the question is asking for a Boolean answer, the annotator selects either YES or NO. If no such minimal answer is possible, then the annotators indicate this. (TACL PDF, section 3 'Answer Labeling'; two-column layout, left column lines 144-146 of the pdftotext -layout extraction src/g1_paper/tacl_2020_30.txt)",
        "plain": "A trained annotator reads the question and the article, picks the best passage answer (a paragraph that contains an answer), and, if the question asks for a Boolean answer, selects YES or NO as the minimal answer.",
        "quote_README_questions": "questions are written by people who want to know the answer, but don't know the answer yet ... the data is collected directly in each language without the use of translation (README lines 25-29)",
        "annotators": "paper footnote 22: 'Trained linguists with experience in NLP data collection.'",
        "annotation_counts": "paper: '...and 37K are 3-way annotated, comprising the dev and test sets, for a total of 277K annotations'; the rest are single-annotated training examples. The builder verifies one annotation per train example when it streams the file.",
        "known_noise_quote": "paper footnote 21: 'We have observed a yes/no question where both YES and NO were deemed correct.'",
        "so": "Labels are human. A single annotator labels each train example, and the paper itself says YES/NO can be arguable, so the A46 screen is the label check (A58 (c) 6).",
    },
    "A58_a_checks": {
        "a1_allowed_licence_and_V": "PASS: Apache-2.0 is on GOLDEN_SPEC rule 3's list; read in the creators' own repo LICENSE at the pinned commit, not only on an HF card. See open_notes 1 and 2.",
        "a2_text_through_another_dataset": "PASS: the text is Wikipedia, CC BY-SA 3.0 / GFDL in 2019 (quoted from the Terms of Use revision in force on the snapshot date); CC BY-SA is on the allowed list and the TOU says commercial use is allowed.",
        "a3_human_text_and_labels_only": "PASS: human-written Wikipedia text, human-written questions (no translation), human YES/NO selection; no LLM, no machine translation, no emoji or distant labels.",
        "a4_train_split_only": "PASS by design: training candidates come from the primary_task train split only; the validation split is used only as own dev (A58 (e)); the hidden test split is not used. Whether System One Bench scores items that coincide with TyDi text is a decontamination question (step 4), not a split question.",
        "a5_denylist": "ORCHESTRATOR: denylist.py check on denylist_query_sb6.json (not run by the builder).",
        "a6_not_used_elsewhere": "builder names-only precheck PASS: none of tydi, tydiqa, typologically, miracl, mr.tydi, xor appears in gblock/checks/c1_source_names.json (338 names; the 'wikipedia' hits there are other datasets). 'boolq' is there, as ruled. The G-proxy-source check (A42-D 8.3, A48 e) is NOT done by the builder.",
        "a7_sealed_side_8_5": "ORCHESTRATOR: PASS/HIT per source on HANDOFF_85_DENYLIST.json identifiers.",
    },
    "data_hosting_finding": {
        "official_download_urls_in_README": [f"https://storage.googleapis.com/tydiqa/v1.0/tydiqa-v1.0-{s}.jsonl.gz" for s in ("dev", "train")],
        "status_on_retrieval": "HTTP 403 AccessDenied (anonymous caller has no storage.objects.get) for tydiqa-v1.0-dev.jsonl.gz and for the paper PDF in the same bucket, checked 2026-10-17 03:03 UTC, and again for the train and dev files at 03:10:35 GMT (evidence: src/g1_gcs_probe/, sha256 in this record). The bucket named in the README no longer serves anonymous downloads.",
        "fallback_host": f"HF dataset repo google-research-datasets/tydiqa (the creators' organisation) at revision {HFREV}: primary_task/train-00000..00011-of-00012.parquet and primary_task/validation-00000-of-00001.parquet, same 166,916 / 18,670 example counts as the original files. Nothing was downloaded: only the file list, sizes and LFS sha256 were read.",
        "primary_task_parquet": parquet,
        "schema_from_card": "question_text, document_title, document_url, language ('english', 'arabic', ...), document_plaintext, passage_answer_candidates{plaintext_start_byte, plaintext_end_byte}, annotations{passage_answer_candidate_index, minimal_answers_start_byte, minimal_answers_end_byte, yes_no_answer ('NONE'|'YES'|'NO')}; offsets are byte offsets into the UTF-8 plaintext",
    },
    "owner_request_arabic": {
        "request": "17 Oct owner message relayed with the chain: also add a little Arabic to SB6, because Arabic is now the main language goal; fewer examples, enough for the model to understand it a little.",
        "conflict": "A58 (b) says 'English only: TyDi's Arabic rows are excluded so the Arabic cap in (e) holds', and the chain text repeats it. The owner's message wins.",
        "builder_default_until_ruled": "TyDi Arabic YES/NO rows enter as a small, separable slice: train <= 150 rows and own dev <= 40 rows (inside SB6's 2,400 / 300 maxima), tagged meta.lang='ar' and meta.arabic_cap_unit=true, in their own raw file, instructions in English, passage and question in Arabic. They count against the owner's Arabic cap, so SB4 + SB5 + SB6-ar <= 1,500 must hold at the mix; the builder does not move rows between blocks and does not touch SB4/SB5. All gates, the decontamination, the A46 screen and G13 apply to them unchanged.",
        "needs_orchestrator": "Confirm the 150 / 40 default (or give other numbers) and say which block gives way if SB4 + SB5 + SB6-ar would pass 1,500. The text and licence are the same sources (TyDi Arabic = Arabic Wikipedia 2019-02-01 under the same Apache-2.0 repo LICENSE), so G1 covers it.",
        "extra_risk": "Arabic TyDi questions and passages come from Arabic Wikipedia of the same snapshot that Mr. TyDi and MIRACL-ar use, and System One Bench scores MIRACL-ar dev queries and passages (ar_miracl_*). Expect more bench overlap on the Arabic slice than on the English one; the decontamination program (exact, MinHash, 13-gram) is the only filter, and the Arabic yield may fall below the default.",
    },
    "open_notes": [
        "1. README.md has no licence line at all; the only creator-side licence statement is the repo LICENSE (Apache-2.0, unmodified template text with the unfilled appendix).",
        "2. The data files are not in the Apache-2.0 repo (they were served from a GCS bucket that is now closed to anonymous callers) and no creator file says in words that the data is Apache-2.0 other than the repo-level LICENSE and the HF YAML tag. A58 (b) already rules 'Apache-2.0 in the official repo'; the orchestrator should confirm that this covers the data files.",
        "3. Data host changed: HF parquet of the creators' organisation at a pinned revision instead of the GCS jsonl.gz. The parquet is a format conversion of the same examples (same counts); the builder cannot compare it with the closed originals.",
        "4. Train examples are single-annotated and the paper reports arguable YES/NO cases, so expect label noise in this block; the A46 screen decides, drop only.",
        "5. Wikipedia text is CC BY-SA: attribution and share-alike apply to the text.",
    ],
    "pass": True,
    "pass_scope": "G1 / A58 (a) 1-4 only. Steps 8.5 and the deny-list are the orchestrator's; nothing was downloaded except the licence records.",
}
(root / "G1_RECORD.json").write_text(json.dumps(rec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

# ---- hand-off to the orchestrator ----------------------------------------------------------------------------------
names_main = [
    "TyDi QA", "TyDiQA", "TyDi-QA", "Tydi QA", "tydi_qa", "tydiqa", "tydiqa-v1.0", "tydiqa primary task",
    "TyDiQA-MinSpan", "TyDiQA-SelectP", "TyDiQA primary_task",
    "google-research-datasets/tydiqa", "google_research_datasets/tydiqa",
    "TyDi QA: A Benchmark for Information-Seeking Question Answering in Typologically Diverse Languages",
    "Typologically Diverse Question Answering", "10.1162/tacl_a_00317", "tacl_a_00317", "2020.tacl-1.30",
]
derivatives = [
    {"name": "Mr. TyDi", "alt_names": ["Mr.TyDi", "MrTyDi", "mr-tydi", "mr_tydi", "castorini/mr-tydi"],
     "why": "dense-retrieval benchmark whose queries and judgements come from TyDi QA; arXiv 2108.08787"},
    {"name": "MIRACL", "alt_names": ["miracl/miracl", "MIRACL-ar", "miracl-ar", "MIRACL multilingual retrieval"],
     "why": "multilingual retrieval benchmark on the same Wikipedia corpora and languages as Mr. TyDi; arXiv 2210.09984; System One Bench scores MIRACL-ar dev (ar_miracl_*)"},
    {"name": "XOR-TyDi QA", "alt_names": ["XOR QA", "xor_tydi", "xorqa"], "why": "cross-lingual open-retrieval QA built from TyDi QA questions"},
    {"name": "TyDiQA-GoldP", "alt_names": ["tydiqa goldp", "tydiqa_goldp", "tydiqa secondary_task", "XTREME TyDiQA", "xtreme tydiqa"],
     "why": "the secondary (gold passage) task of the same data, used as a test in XTREME / XTREME-R; same source, different task"},
]
handoff = {
    "block": "SB6",
    "ruling": "A58 (draft) (c) 1-3 and A42-D 8.5",
    "prepared_by": "Sonnet builder, chain SB6 round 1, 17 Oct 2026",
    "status": "WAITING FOR PASS: no builder code written, no train file downloaded, no row built. The next round starts only when both PASS lines below are recorded.",
    "identifiers_for_the_8_5_sealed_side_source_name_check": {
        "dataset_name": "TyDi QA",
        "alt_names": names_main,
        "publisher": "Google Research (google-research-datasets)",
        "hosts": ["github.com/google-research-datasets/tydiqa", "huggingface.co/datasets/google-research-datasets/tydiqa", "storage.googleapis.com/tydiqa"],
        "upstream_id": "google-research-datasets/tydiqa",
        "pinned_commit": COMMIT,
        "hf_revision": HFREV,
        "doi": "10.1162/tacl_a_00317",
        "creators": "Jonathan H. Clark, Eunsol Choi, Michael Collins, Dan Garrette, Tom Kwiatkowski, Vitaly Nikolaev, Jennimaria Palomaki",
        "languages_used": ["english (main)", "arabic (small slice, owner request)"],
        "text_source": "Wikipedia (en, ar), Internet Archive snapshots 2019-02-01 (enwiki-20190201, arwiki-20190201)",
        "licence": "Apache-2.0 (repo LICENSE); text CC BY-SA 3.0 / GFDL",
        "known_derivatives_to_include_in_the_check": derivatives,
        "licence_file_sha256": files["src/g1_official/LICENSE"],
        "readme_sha256": files["src/g1_official/README.md"],
    },
    "orchestrator_actions": [
        {"id": "8.5", "what": "A42-D 8.5 / A58 (a) 7 sealed-side source-name check on the identifiers above, derivatives included (Mr. TyDi, MIRACL, XOR-TyDi QA, TyDiQA-GoldP); return PASS or HIT per source only.", "result": None},
        {"id": "denylist", "what": "A58 (c) 3: from c_src/common (orchestrator only, because the build step reads ohs3 in-process): denylist.py check --query c2_build/zed_orch/sb_blocks/SB6/denylist_query_sb6.json --out c2_build/zed_orch/sb_blocks/SB6/denylist_verdicts_sb6.json --run sb6 --fail-on-taint ; no taint verdict is allowed. The query has the TyDi item (with a Wikipedia parent) and, as a separate item, the derivatives.", "result": None},
        {"id": "g_proxy_source", "what": "A58 (a) 6: confirm TyDi QA is not a G-proxy source (A42-D 8.3, A48 e). Not checked by the builder.", "result": None},
        {"id": "arabic_ruling", "what": "Owner asked for a little Arabic in SB6 (see G1_RECORD.json owner_request_arabic). Confirm the default (<= 150 train, <= 40 dev rows) or give other numbers, and say which block gives way so SB4 + SB5 + SB6-ar <= 1,500.", "result": None},
        {"id": "data_host", "what": "The README's GCS download bucket answers 403 AccessDenied. Confirm the builder may stream the creators' HF parquet at the pinned revision instead (G1_RECORD.json data_hosting_finding).", "result": None},
    ],
    "builder_precheck_c1_source_names": "PASS (names only): none of tydi, tydiqa, typologically, miracl, mr.tydi, xor appears in gblock/checks/c1_source_names.json (338 names).",
    "builder_precheck_denylist_json_names": "c_build/denylist.json (690 entries) has one name containing 'miracl': rej:judge_verifier#17.0 'miracl/hagrid' (class taint, cat llm_written; aliases span:hagrid, span:miracl/hagrid). It is HAGRID, a different dataset (LLM-written answers over MIRACL passages). A bare 'MIRACL' in the derivatives item is not that alias, but a substring matcher could hit; if it does, the verdict belongs to the derivatives item only and not to TyDi QA itself. No entry contains tydi.",
    "why_parents_has_wikipedia": "The passage text is Wikipedia. The parent is listed so the check sees the real provenance; if a hit comes only through this parent, report which entry matched and the orchestrator rules (the C2 GB block listed Wikivoyage / Wikinews with parents [] and passed).",
}
(root / "HANDOFF_85_DENYLIST.json").write_text(json.dumps(handoff, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

query = {
    "datasets": {
        "sb6_tydiqa_primary_en_ar": {
            "names": names_main,
            "datasets": ["google-research-datasets/tydiqa"],
            "domains": ["github.com/google-research-datasets/tydiqa", "huggingface.co/datasets/google-research-datasets/tydiqa", "storage.googleapis.com/tydiqa"],
            "parents": [
                {"names": ["Wikipedia", "English Wikipedia", "Arabic Wikipedia", "enwiki-20190201", "arwiki-20190201"],
                 "datasets": [], "domains": ["en.wikipedia.org", "ar.wikipedia.org"], "parents": []}
            ],
            "emits_rows": True,
        },
        "sb6_tydiqa_known_derivatives": {
            "names": [n for d in derivatives for n in [d["name"]] + d["alt_names"]],
            "datasets": ["castorini/mr-tydi", "miracl/miracl", "xor_tydi"],
            "domains": [],
            "parents": [],
            "emits_rows": False,
        },
    },
    "parents_registry": {},
}
(root / "denylist_query_sb6.json").write_text(json.dumps(query, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

state = {
    "block": "SB6",
    "chain": "SB6 round 1 (17 Oct 2026)",
    "ruling": "A58 (draft)",
    "owner_request_applied": "a small Arabic slice (<= 150 train, <= 40 dev) is planned inside SB6; awaiting the orchestrator's confirmation (see HANDOFF orchestrator_actions arabic_ruling)",
    "steps": {
        "1_G1_download_and_provenance": "DONE: G1_RECORD.json (pass true, 5 open notes). LICENSE sha256 " + files["src/g1_official/LICENSE"][:12] + "..., README sha256 " + files["src/g1_official/README.md"][:12] + "...; pinned commit " + COMMIT + "; README has no licence line; GCS data bucket closed (403), HF parquet at " + HFREV[:12] + " is the fallback host",
        "2_handoff_to_orchestrator": "DONE (sent): HANDOFF_85_DENYLIST.json + denylist_query_sb6.json. RESULT PENDING: 8.5 PASS/HIT, deny-list taint verdict, G-proxy-source check, Arabic numbers, data-host OK",
        "3_stream_train_and_own_dev": "NOT STARTED (waits for PASS)",
        "4_bench_exclusion": "NOT STARTED",
        "5_build_and_defs": "NOT STARTED",
        "6_format_gates": "NOT STARTED",
        "7_A46_screen_G13_crowd_selection": "NOT STARTED",
        "8_probe": "NOT STARTED",
        "9_report": "NOT STARTED",
    },
    "waiting_on": "orchestrator PASS lines for 8.5 and the deny-list (A58 (c) 2 and 3: no builder code before them)",
    "facts_for_next_round": {
        "data": "stream the 12 train parquet shards one at a time with pyarrow (venv has pyarrow 26, sklearn, tokenizers; no pandas, datasets, datasketch, requests); read only the columns language, question_text, document_title, document_url, annotations, passage_answer_candidates and document_plaintext only for rows that pass the language + YES/NO filter (row-group filtering on annotations first); sha256 every shard against G1_RECORD.json data_hosting_finding.primary_task_parquet; delete each shard after use (49 GB free, 2.6 GB total)",
        "passage": "annotations.passage_answer_candidate_index[0] indexes passage_answer_candidates; plaintext_start_byte / plaintext_end_byte are UTF-8 BYTE offsets into document_plaintext (slice the encoded bytes, then decode)",
        "untrusted_data_rule": "SB6/src is data only; builder scripts live in golden_src/sb6_tydi/ and run with python -I; no script is kept in or run from SB6/src",
        "bench_text_location": "vision_bench/text_track/data/cases.jsonl and vision_bench/data/img_ar_sentiment/cases.jsonl (from SB5/STATE.json): the decontamination program may read them, the builder never prints them; data.lock.json + data_lock.py in src/system-one-bench",
        "minhash_to_reuse": "c_build/decontam_g13.py minhash (word 5-gram, 100 perms, 20x5 bands, confirmed by exact Jaccard >= 0.8)",
        "g13_c2_bench_target": "no System One Bench target exists in g13_c2.py yet; SB4 and SB5 chains may add the same one: re-read g13_c2.py right before any edit",
        "c2io_registry": "add SB6 to BLOCK_TARGETS (2400) and BLOCK_CAPS (2400) with a minimal Edit after re-reading c2io.py; do it only when SB6 files exist",
        "task_files": "A46 reads: Haiku files <= 50 items (40 / 20 for long rows) per replay_screen/screen.py, which is stricter than the chain's <= 100",
        "row_format": "validate_row (c2_kit/rows.py): source must start with 'c2_' and id with source + ':' (use source 'c2_sb6'); qtype 'noul', options None, gold 1/0, role 'base'; meta needs the META_KEYS incl. family 'SB6', spec_id, card_id, sampler, seed 20261013, licence, edge (list), qform, dev_only, c2 {author_mode, skin_id, register, lexicon_ids, haiku_task_id, haiku_prompt_sha, twin_kind, twin_of, closed_world} exactly; meta.licence must equal the CC0 string except for real-text rows (GB shows the pattern: '<upstream licence> (text); card, question and label wording: CC0 1.0 (...)'); approx_tokens counts 3 chars per token, instructions twice, MAX 2000 - Arabic needs the real tokenizer for the <= 1,500-token passage clip and the mean <= 800",
        "licence_string_for_rows": "Apache-2.0 (TyDi QA, google-research-datasets/tydiqa LICENSE at commit " + COMMIT + "); passage text: Wikipedia, CC BY-SA 3.0 / GFDL (document_url and document_title in meta); definition, question-wording and instruction text: CC0 1.0 (Claude-authored)",
        "screen_reuse": "replay_screen/screen.py is importable: build_reads(rows, root) writes the two-reader Haiku task files (<= 50 items, bands 50/40/20 by size), then score_reads, adjudicate (Sonnet, 30 seeded controls), confirm (Opus), finalize. Use a root of its own (SB6/screen/), never replay_screen/'s. It reads row fields qtype, gold, state, instructions, card, options, source; the Haiku item carries text, question and definitions and no gold.",
        "own_dev_files": "data/c2_parts/SB6/out/mixdev_S5.jsonl (300 rows max, report-only, never trained; mix_c2 reads it for blocks in BLOCK_TARGETS and checks that no id is a training id, A39 h)",
        "mix_registration": "BLOCK_TARGETS / BLOCK_CAPS in c2io.py feed mix_c2.py (fit_block size cap, block mixdev, TARGETS); RULE_BLOCKS (GB, MD, RTW) carry the domain / twin rules and SB6 is not one of them. Run the mix_c2 and c2_select unit tests after the registration edit; a step 2b trim of SB6 rows above 1,200 (A58 (e)) is not in mix_c2.py yet and is the orchestrator's to wire.",
        "crowd_read": "c2_select.py tasks --fam SB6 --write-shards -> data/c2_crowd_shards/SB6/shard_NNN.jsonl; read on od-l4b with reads/vm_scripts and fast_read.py label --views 1 (one bulk read at a time, never stop or restart the server); pull labels back; verify with reads/verify_crowd_labels.py",
        "yes_no_balance": "45-55% yes over the whole block by seeded (20261013) down-sampling; keep each language near 50% too (down-sample inside the language first)",
        "paper_noise_note": "paper footnote 21: some yes/no questions have both YES and NO deemed correct",
    },
}
(root / "STATE.json").write_text(json.dumps(state, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print("ok", now)

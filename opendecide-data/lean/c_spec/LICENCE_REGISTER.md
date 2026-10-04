# LICENCE_REGISTER: data sources for model C (PRIVATE)

Date: 3 Oct 2026. **Private file. Never publish it or any row derived from a share-alike (SA) source.**
Companion to `C_DATA_SPEC.md`. Builders still read each record again at build time (gate G1) and record the URL, commit
and sha256 in `meta.licence`. This file names no sealed-suite candidate.

**Merged 3 Oct 2026 (merge pass)** from the three web licence checks `LICENCE_CHECK_1.md`, `_2.md` and `_3.md`
(positions 1-20 of the spec's dataset list; every new public and commit source was read by at least one checker).
Every "to confirm" from the earlier version is now closed. Result: 14 public datasets IN, 3 OUT (DocFinQA, MultiHiertt,
ConvFinQA), both commit sources IN. The OUT rows stay in table 1 with status OUT so the reason is kept.

Status words:
- **V** = licence read upstream (a licence file, an official page or an official record) by a 3 Oct checker.
- **H** = only the creator's own Hugging Face card states it. Not an official record (decision 6): OUT.
- **unverified** = no official record was reached. OUT of training (new rows and replay) until a record is read.
- **OUT** = not used for C training; the reason is in the row.

Allowed licences (owner, 3 Oct): CC0, public domain or US government, CC BY, MIT, Apache-2.0, BSD, ODC-BY; share-alike
CC BY-SA or ODbL with the data kept private and a notices file (decision 8). Anything else (NC, ND, AFL, CDLA,
"other", "research only", unknown) is out unless the owner accepts it by a PREREG amendment. **CDLA-Permissive-1.0**
(FinTabNet) allows commercial use and has no share-alike, but it is not on this list by name: out until the owner
accepts it.

**Text licence vs dataset licence.** The dataset licence (annotations) must be V. The document text must be either
covered by that licence, or have its own V licence on this list, or be third-party user or press text under a clean
dataset licence (Wikipedia, reviews, posts, headlines, subtitles), which is recorded in section 6 and is not a blocker.
Text that comes through **another licensed dataset** (FinTabNet, S2ORC papers, OANC) needs that dataset's licence V.

---

## 1. New licensed public training splits (14 IN, 3 OUT; 8,750 / 17,500 rows in round 1 / round 2)

One row per dataset. "Check" = which 3 Oct checker read the record (1, 2, 3 = `LICENCE_CHECK_1/2/3.md`). Commercial =
commercial use allowed by the dataset licence. SA = share-alike applies to the annotations or the text.

| # | Dataset | Licence (dataset / annotations) | Official licence record (URL; upstream commit) | Commercial | SA | Split used | Excluded | Rows r1 / r2 | Status | Text licence and notes |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | SQuAD 2.0 (answerability) | CC BY-SA 4.0 | https://rajpurkar.github.io/SQuAD-explorer/ (official page, links the CC BY-SA 4.0 legal code) | yes | **yes** | train (130,319; about 43K unanswerable) | dev (11,873), hidden test | 900 / 1,800 | **IN**, V (check 1) | Wikipedia passages (CC BY-SA). Dedupe passages vs C1 `qnli`, `gd_answer_equiv`. Strict G5 read. **Drop list:** the ids in MuSiQue's `dev_test_singlehop_questions_v1.0.json` (check 2), so no MuSiQue dev/test seed enters |
| 2 | MuSiQue (Ans + Full) | CC BY 4.0 | https://github.com/StonyBrookNLP/musique/blob/main/LICENSE (README: "distributed under a CC BY 4.0 License"; 922ac98f19a2) | yes | annotations no; **text yes** | train (19,938 answerable; Full adds unanswerable twins) | dev, hidden test | 1,000 / 2,000 | **IN**, V (check 2) | Wikipedia paragraphs (SA). Questions are composed from seed sets SQuAD, T-REx, NQ, MLQA (CC BY-SA, not re-read) and Zero Shot RE (not checked); MuSiQue's own CC BY 4.0 release covers the compositions. Treat all rows as SA. Split by page; dedupe vs `gd_hotpotqa_yesno` |
| 3 | 2WikiMultihopQA | Apache-2.0 | https://github.com/Alab-NII/2wikimultihop/blob/main/LICENSE (repo-wide; data zips linked from the README) | yes | annotations no; **text yes** | train (167,454) | dev (12,576), test (12,576) | 600 / 1,200 | **IN**, V (check 3) | Wikipedia text (CC BY-SA) and Wikidata facts (CC0). Comparison and yes/no types only |
| 4 | QuALITY | CC BY 4.0 | https://nyu-mll.github.io/quality/ ("distributed under a CC BY 4.0 License"; no repo LICENSE; nyu-mll/quality f84977c40dbf) | yes | no | train (2,523 questions, 150 articles: 118 Gutenberg, 22 Slate/OANC, 10 CC BY) | dev (2,086), hidden test | 600 / 1,200 | **IN**, V (check 1); text V | **All three article sources cleared.** Gutenberg: US public domain (strip the Gutenberg header and trademark text). Slate: part of the OANC (https://anc.org/data/oanc/: "without restriction (including commercial use)"; contents page lists the Slate sub-corpus). The rest: CC BY. The program keeps an article only if its `license`/`source` field is Gutenberg, OANC/Slate or CC BY. Counts-only check vs LongBench v2 |
| 5 | Qasper | CC BY 4.0 (annotations) | Official AI2 page, archived: https://web.archive.org/web/20230414023335/https://allenai.org/data/qasper ("License: CC BY", v0.3). The live URL now redirects to the HF card, which is not the record | yes (annotations) | per paper | train (888 papers, about 2.6K questions; `qasper-train-dev-v0.3.tgz`) | dev, test (416 papers) | 350 / 700 | **IN**, V (check 2); text per paper | Papers were chosen under "CC-BY-*", which includes NC and ND. Full text is the arXiv/S2ORC version. The program reads each paper's **arXiv licence** and keeps only CC BY, CC BY-SA (SA: notices file) or CC0; every NC or ND paper is dropped. No ACL Anthology route. Log each paper's licence. If < 150 papers qualify: drop Qasper; rows to QuALITY and F13 |
| 6 | DocFinQA | MIT, in the creator's HF card YAML only | https://huggingface.co/datasets/kensho/DocFinQA (card only; no official Kensho repo found; the paper states no data licence, its CC BY-NC-SA header is the paper's own licence) | unknown | unknown | none | all | 0 / 0 (was 250 / 500; moved to F13) | **OUT** (H = unverified; check 3) | Decision 6. Also: the paper says train and dev were "not fully validated", and its code was "generated by WizardCoder LLMs" (LLM artefact; 3.1 bans LLM labels). Filing text not cleared (decision 9). Questions come from FinQA (MIT, V) |
| 7 | HybridQA | MIT (annotations; "Copyright (c) 2020 wenhu chen") | https://github.com/wenhuchen/HybridQA/blob/master/LICENSE (db22fda8c595) | yes | annotations no; **text yes** | train (62,682) | dev, test (3,463) | 1,000 / 2,000 (base 600 / 1,200 + 400 / 800 from MultiHiertt and ConvFinQA) | **IN**, V (check 1) | Tables and passages come from wenhuchen/WikiTables-WithLinks, which has no LICENSE file: Wikipedia text, CC BY-SA (SA, notices file). Same WikiTables corpus as TabFact (OHS-2): table-hash check (spec 7) |
| 8 | WikiSQL (SQL executed for labels) | BSD-3-Clause ("Copyright (c) 2017, Salesforce Research") | https://github.com/salesforce/WikiSQL/blob/master/LICENSE (cffb42307775; data `data.tar.bz2` is in the repo) | yes | annotations no; **tables yes** | train (56,355) | dev, test (15,878) | 1,150 / 2,300 (base 750 / 1,500 + 400 / 800 from MultiHiertt and ConvFinQA) | **IN**, V (check 2) | Wikipedia tables (CC BY-SA: SA, notices file); crowd-written questions. Same TabFact table-hash check |
| 9 | MultiHiertt | MIT (annotations; Penn State NLP Group 2022) | https://github.com/psunlpgroup/MultiHiertt/blob/main/LICENSE | yes (annotations) | no | none | all | 0 / 0 (was 450 / 900; moved to WikiSQL +250 / +500 and HybridQA +200 / +400) | **OUT** (document text unverified; checks 1, 3) | Report text is FinTabNet (S&P 500 annual reports, 1999-2019). Its licence, CDLA-Permissive-1.0, is stated only in the MultiHiertt and FinQA papers; IBM's own FinTabNet page did not resolve or redirected (checks 1 and 3). CDLA-Permissive-1.0 is also not on the allowed list. Returns only by PREREG amendment after IBM's record is read **and** the owner accepts CDLA-Permissive-1.0 |
| 10 | ConvFinQA | MIT (annotations; "Copyright (c) 2022 Zhiyu Chen") | https://github.com/czyssrs/ConvFinQA/blob/main/LICENSE (cf3eed2d5984) | yes (annotations) | no | none | all | 0 / 0 (was 350 / 700; moved to WikiSQL +150 / +300 and HybridQA +200 / +400) | **OUT** (document text unverified; check 1) | Same FinTabNet report text as MultiHiertt and C1's replay `gd_finqa` (now "VERIFY or drop", section 4). One accepted FinTabNet record clears all three |
| 11 | DROP | CC BY-SA 4.0 ("The DROP dataset is distributed under CC BY-SA 4.0 license") | `drop_dataset/license.txt` inside the official AI2 zip https://ai2-public-datasets.s3.amazonaws.com/drop/drop_dataset.zip (members dated 26 May 2019). The HF mirror is not the record | yes | **yes** (whole dataset) | train (77,400) | validation (9,535), hidden test | 250 / 500 | **IN**, V (check 2) | Wikipedia passages. Private training only; notices file |
| 12a | UCI Car Evaluation | CC BY 4.0 | https://archive.ics.uci.edu/dataset/19/car+evaluation (DOI 10.24432/C5JP48) | yes | no | own 90/10 by record (no official split) | none | 500 / 1,000 (with 12b) | **IN**, V (checks 1, 3) | Attribute tuples from the DEX model (Marko Bohanec); labels from the published DEX rules (program-checkable). Attribution in the notices file |
| 12b | UCI Nursery | CC BY 4.0 | https://archive.ics.uci.edu/dataset/76/nursery (DOI 10.24432/C5P88W) | yes | no | own 90/10 by record | none | (with 12a) | **IN**, V (checks 1, 3) | DEX model tuples (Vladislav Rajkovic). The old "to confirm" is closed: Car does not need to take all rows |
| 13 | XED English | CC BY 4.0 (README last line: "Creative Commons Attribution 4.0 International License (CC-BY)") | https://github.com/Helsinki-NLP/XED (README; no LICENSE file; 76666d251f14) | yes | no | own 90/10 by line (no official split); never the fi or projected files | none (the own 10% feeds only the mix-tuning dev) | 600 / 1,200 | **IN**, V (check 1); subtitle text: no record found | OPUS OpenSubtitles lines; the OPUS page returned 404, so no text licence was read. Recorded as third-party text under a clean dataset licence (section 6), not a blocker (decided by default; the owner may override). The README's "24164 + 9384 neutral" are annotation counts, not line counts: the builder counts lines. C1 used 499 rows (`br_xed_en`): unused lines only |
| 14 | MAMS (ACSA + ATSA) | Apache-2.0 | https://github.com/siat-nlp/MAMS-for-ABSA/blob/master/LICENSE (cddcdb0f423b; README: "contains the data and code", data under `data/`) | yes | no | `train.xml` only | val, test | 750 / 1,500 | **IN**, V (checks 2, 3) | Citysearch New York restaurant reviews (Ganu et al. 2009; third-party text). May share a pool with DI's ACOS: counts-only dedupe. C1 used 389 ACSA rows |
| 15 | News Headlines Sarcasm v2 | CC BY 4.0 (Kaggle licence field) | https://www.kaggle.com/datasets/rmisra/news-headlines-dataset-for-sarcasm-detection (owner and creator Rishabh Misra; v2 of 3 Jul 2019) | yes | no | own 90/10 by record (no official split) | none | 350 / 700 | **IN**, V (check 3; decided by default) | The creator's Kaggle page is the only official v2 release, and the licence is a structured field the creator set. Decision 6 is about HF cards, so this plan keeps it (decided by default; the owner may override: then OUT, and its 350 / 700 rows go to XED +175 / +350 and GHC +175 / +350). Never the GitHub v1 file (no LICENSE) or a mirror. The Onion and HuffPost headlines (third-party text); outlet names redacted. C1 used 191 rows from the raquiba mirror: dedupe |
| 16 | Gab Hate Corpus (GHC) | CC BY 4.0 (OSF node licence "CC-By Attribution 4.0 International", 2018) | https://osf.io/edua3/ (read through https://api.osf.io/v2/nodes/edua3/?embed=license; node modified 2022-04-12) | yes | no | `ghc_train.tsv` only | `ghc_test.tsv` (never downloaded) | 350 / 700 | **IN**, V (check 1) | 27,665 gab.ai posts in all (third-party text); the builder counts the train file. No research-only restriction stated. Exact-text dedupe vs HateXplain and Social Bias Frames. C1 used 1,273 + 472 rows |
| 17 | EDOS | CC0 1.0 Universal | https://github.com/rewire-online/edos/blob/main/LICENSE (b1f1fbcca9d4) | yes | no | `split == train` only: 14,000 of 20,000 labelled (70/10/20, overview paper arXiv 2303.04222) | dev, test (both are in the labelled CSV: keep the filter); the 2M unlabelled posts are not used | 350 / 700 | **IN**, V (checks 2, 3) | Gab (pushshift dump) and Reddit (API) posts: third-party text; CC0 covers Rewire's rights only. Same dedupe as GHC. C1 used 3,433 + 624 rows: unused posts only |

**Totals.** IN: 14 datasets (12a and 12b count as one, as in the spec), 8,750 / 17,500 rows; the 2,100 round-2 rows of
the 3 OUT sets moved to F13 (+500, own family), WikiSQL (+800) and HybridQA (+800). OUT: DocFinQA, MultiHiertt,
ConvFinQA.

Real-text codebook rows (`C_DATA_SPEC.md` 2.3) reuse sets 13, 14, 16 and 17 under the same licence and the same
3,000-row cap per dataset.

**Sealed-suite candidates are not recorded here** (this file is on the builders' allow-list). Check 2's note on one
rejected candidate stays in `LICENCE_CHECK_2.md`, which builders never open (spec "Who may read what").

## 2. Commit sources (12,000 rows in round 2)

| Source | Licence | Official licence record (URL; commit) | Commercial | SA | Split used | Excluded | Rows r1 / r2 | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
| CommitChronicle (JetBrains) | **CC BY 4.0** for the compilation (Zenodo record); each commit under its repo's licence, only MIT, Apache-2.0 or BSD-3-Clause (per-commit `license` field) | https://zenodo.org/records/8189044 (DOI 10.5281/zenodo.8189044, licence id `cc-by-4.0`, open access). Cite this in `meta.licence`, **not** the HF card (which says only "other") | yes | no | train only (split by project): 7.66M commits of 10.7M, 11.9K repos, 20 languages | validation (1.55M), test (1.49M) | 4,000 / 8,000 | **IN**, V (check 3) | Record clause: "researchers should only use public, non-personal information"; authors are already replaced by ids. PII scrub (spec 4.3 guard 10). Per-repo attribution and Apache-2.0 NOTICE text in the notices file. Zenodo-hosted, allowed under decision 7. n8n (Sustainable Use License) is not in the permissive set |
| CommitPackFT (BigCode) | MIT for the compilation ("CommitPack, CommitPackFT, HumanEvalPack, and all code are licensed under the MIT License of this repository"), plus each sample's own repo licence (`license` field) | https://github.com/bigcode-project/octopack (README + LICENSE; e17a8f647026). Cite this, not the HF card | yes, after the per-sample filter | no, after the filter | all (no split) minus held-out repos: 702,062 single-file commits, 277 languages | samples whose `license` is not mit, apache-2.0, bsd-2-clause, bsd-3-clause, isc, cc0-1.0 or unlicense (agpl, lgpl, mpl, epl, unknown dropped) | 2,000 / 4,000 | **IN**, V (check 1) | The `license` field is a repo-level detection, so a few files may differ. Commit messages are third-party contributor text. n8n and OHS guards (spec 4.3) still apply |

Both: guards in `C_DATA_SPEC.md` 4.3. A third-party notices file lists every repo used, with its licence.

## 3. Own program-generated rows

| Rows | Licence | Notes |
|---|---|---|
| F1-F13 program rows (about 86K in round 2; 90,500 own rows incl. F13's +500 DocFinQA fallback, minus codebook rows) | CC0 1.0 (program-generated; Claude-written templates, packs and code; no third-party text) | Labels by program; solver B agreement 100% |
| Real-text codebook rows (4,320 in round 2) | The source dataset's licence (sets 13, 14, 16, 17) | Labels = program mapping of human annotations |

## 4. Replay sources (C1's golden_train, 501,732 rows in 204 sources)

Generated by `tools/make_replay_register.py` from `replay_licence_scan.json`. KEEP = the golden build recorded an
allowed licence in `meta.licence`. The mixer joins this table and drops every DROP row and every VERIFY row it cannot
confirm upstream. "Candidate" licences in VERIFY rows are unconfirmed leads, not facts.

**Merge 3 Oct:** `gd_finqa` (4,970 rows) moved from KEEP to "VERIFY or drop". Its FinQA annotations are MIT (V), but
its report text is FinTabNet, the same unverified CDLA-Permissive-1.0 text that keeps MultiHiertt and ConvFinQA out
(table 1). It is kept only if IBM's FinTabNet record is read **and** the owner accepts CDLA-Permissive-1.0 by
amendment. The change is in the generator's VERIFY list, so a re-run keeps it.

**Verifier 3 Oct:** decision 6 (a creator's own HF card is not an official record) and decision 12 (unverified = out,
new and replay) apply to replay as well. The 15 sources whose `meta.licence` cites only the creator's HF card (38,521
rows; `HF_ONLY` in the generator, incl. `judge_helpsteer2`, which maps to the HelpSteer2 card) moved from KEEP to
"VERIFY or drop". The mixer keeps one only after reading an official record (repo LICENSE, project page or release).

<!-- REPLAY_TABLE_START -->
| Source | Rows | Licence (from meta; full string with URL in replay_licence_scan.json) | SA | Status | Note |
|---|---|---|---|---|---|
| `amazon_polarity` | 754 | (none in meta) |  | DROP | Forbidden list; terms unclear; read from a test split |
| `arc` | 414 | (none in meta) |  | VERIFY or drop | candidate CC BY-SA 4.0 (AI2 ARC); train split only (DI uses the test split) |
| `banking77` | 2,300 | (none in meta) |  | DROP (default) | Forbidden list (banking77); also a dev source and DI test. Owner may grandfather |
| `binj_adult` | 213 | (none in meta) |  | DROP (default) | Claude-written golds, blind-solved. Owner may grandfather |
| `binj_consistency` | 226 | (none in meta) |  | DROP (default) | Claude-written golds, blind-solved. Owner may grandfather |
| `binj_intent` | 212 | (none in meta) |  | DROP (default) | Claude-written golds, blind-solved. Owner may grandfather |
| `binj_offensive` | 203 | (none in meta) |  | DROP (default) | Claude-written golds, blind-solved. Owner may grandfather |
| `boolq` | 896 | (none in meta) |  | DROP (default) | Forbidden list (super_glue/boolq). Owner may grandfather |
| `br_abcd` | 707 | MIT |  | KEEP |  |
| `br_casino` | 489 | CC BY 4.0 |  | KEEP |  |
| `br_cfpb` | 668 | CC0 1.0 / US-government public domain |  | KEEP |  |
| `br_claimbuster` | 474 | CC BY 4.0 |  | KEEP | Zenodo-hosted (owner decision 7) |
| `br_congress_policy` | 699 | MIT |  | VERIFY or drop | creator's HF card only (decision 6); read an official record (repo LICENSE, project page, paper release) or drop |
| `br_convabuse` | 397 | CC BY 4.0 |  | KEEP |  |
| `br_edos` | 624 | CC0 1.0 Universal |  | KEEP |  |
| `br_emobank` | 671 | CC BY-SA 4.0 | SA | KEEP |  |
| `br_fm2` | 357 | Apache-2.0 | SA | KEEP |  |
| `br_ghc` | 472 | CC BY 4.0 |  | KEEP |  |
| `br_hatemoji_build` | 362 | CC BY 4.0 |  | KEEP |  |
| `br_infotabs` | 689 | Apache-2.0 |  | KEEP |  |
| `br_mams_acsa` | 389 | Apache-2.0 |  | KEEP |  |
| `br_mnds` | 729 | CC BY 4.0 |  | KEEP | Zenodo-hosted (owner decision 7) |
| `br_newsgroups20` | 591 | CC BY 4.0 |  | KEEP |  |
| `br_newsmtsc` | 607 | MIT |  | DROP | Source text POLUSA is non-commercial (zenodo.org/records/3946057); C1 trained on it: disclose |
| `br_politeness_wiki` | 488 | CC BY 4.0 |  | KEEP |  |
| `br_sarcasm_headlines` | 191 | CC BY 4.0 |  | KEEP |  |
| `br_star` | 642 | MIT |  | KEEP |  |
| `br_steam_aspect` | 200 | CC BY 4.0 |  | VERIFY or drop | creator's HF card only (decision 6); read an official record (repo LICENSE, project page, paper release) or drop; 3.G also excludes Steam for new rows |
| `br_topv2` | 770 | CC BY-SA 4.0 | SA | KEEP |  |
| `br_wos46985` | 758 | CC BY 4.0 |  | KEEP |  |
| `br_xed_en` | 499 | CC BY 4.0 |  | KEEP |  |
| `civil_comments` | 364 | (none in meta) |  | DROP | Jigsaw-derived (MBIB 040_Jigsaw in forbidden mbib-base); not grandfatherable |
| `clinc150` | 2,651 | (none in meta) |  | VERIFY or drop | candidate CC BY 3.0 (github.com/clinc/oos-eval); train split only; dev source + DI test |
| `clothing` | 211 | (none in meta) |  | VERIFY or drop | candidate CC0 at the original Kaggle page (Women's E-Commerce Clothing Reviews); the mirror does not count |
| `condaqa` | 788 | (none in meta) |  | DROP (default) | Forbidden list (CONDAQA). Owner may grandfather |
| `copa` | 243 | (none in meta) |  | VERIFY or drop | candidate BSD-2 (COPA original release) |
| `csqa` | 478 | (none in meta) |  | VERIFY or drop | candidate MIT (CommonsenseQA original release) |
| `dbpedia` | 882 | (none in meta) |  | DROP (default) | Forbidden list (dbpedia_14). Owner may grandfather |
| `fld` | 574 | (none in meta) |  | VERIFY or drop | unknown (hitachi-nlp FLD release); check the repo LICENSE |
| `gd_aegis_prompts` | 1,887 | CC BY 4.0 |  | VERIFY or drop | creator's HF card only (decision 6); read an official record (repo LICENSE, project page, paper release) or drop; prompts only |
| `gd_answer_equiv` | 2,832 | Apache-2.0 |  | KEEP |  |
| `gd_babi_logic` | 4,249 | CC BY 3.0 |  | KEEP |  |
| `gd_bbh_mistake` | 905 | Apache-2.0 |  | DROP | Reuses BBH inputs (DI test) |
| `gd_biored` | 539 | Public domain, US Government Work |  | KEEP |  |
| `gd_boardgameqa` | 9,550 | CC BY |  | KEEP |  |
| `gd_cards` | 7,096 | Apache-2.0 |  | KEEP |  |
| `gd_casehold_yn` | 4,039 | Apache-2.0 |  | KEEP | CaseHOLD is not OHS-1's legal part (LegalBench + LEDGAR) |
| `gd_check_covid` | 713 | MIT |  | KEEP |  |
| `gd_clickbait16` | 444 | CC BY 4.0 |  | KEEP | Zenodo-hosted (owner decision 7) |
| `gd_clickbait17` | 4,461 | CC BY 4.0 |  | KEEP | Zenodo-hosted (owner decision 7) |
| `gd_climate_targets` | 1,071 | CC BY 4.0 |  | VERIFY or drop | creator's HF card only (decision 6); read an official record (repo LICENSE, project page, paper release) or drop |
| `gd_codah` | 2,235 | ODC-BY 1.0 |  | KEEP |  |
| `gd_comve` | 5,419 | CC BY-SA 4.0 | SA | KEEP |  |
| `gd_conditionalqa` | 1,713 | CC BY-SA 4.0 | SA | KEEP |  |
| `gd_crossner` | 950 | MIT |  | KEEP |  |
| `gd_crowdtruth_mre` | 963 | CC BY-SA 4.0 | SA | KEEP | Zenodo-hosted (owner decision 7) |
| `gd_csc_sarcasm` | 1,739 | MIT |  | KEEP |  |
| `gd_druglabel_section` | 4,284 | CC0 1.0 / public domain |  | KEEP |  |
| `gd_drugprot` | 8,794 | CC BY 4.0 |  | KEEP | Zenodo-hosted (owner decision 7) |
| `gd_dstc9_track1` | 4,631 | Apache-2.0 |  | KEEP |  |
| `gd_east_asian_prejudice` | 3,600 | CC BY 4.0 |  | KEEP | Zenodo-hosted (owner decision 7) |
| `gd_edgar_10k_item` | 6,070 | Apache-2.0 |  | VERIFY or drop | creator's HF card only (decision 6); read an official record (repo LICENSE, project page, paper release) or drop |
| `gd_edos_sexism` | 3,433 | CC0 1.0 Universal |  | KEEP |  |
| `gd_faithdial` | 2,963 | MIT |  | VERIFY or drop | creator's HF card only (decision 6); read an official record (repo LICENSE, project page, paper release) or drop |
| `gd_feverous` | 8,318 | CC BY-SA 3.0 / Wikipedia page licence terms | SA | KEEP |  |
| `gd_finqa` | 4,970 | MIT |  | VERIFY or drop | FinQA annotations MIT (V); report text = FinTabNet, CDLA-Permissive-1.0 per papers only, IBM record unverified and not on the allowed list (merge 3 Oct); same rule as MultiHiertt/ConvFinQA |
| `gd_gen2_json_fields` | 670 | CC0 1.0 |  | KEEP (program) | program-generated in this repo |
| `gd_gen2_long_policy` | 294 | Generated by Claude-written program in this repo |  | KEEP (program) | program-generated in this repo |
| `gd_gen2_probability` | 478 | Generated by Claude-written program in this repo |  | KEEP (program) | program-generated in this repo |
| `gd_gen2_tool_selection` | 290 | Generated by Claude-written program in this repo |  | KEEP (program) | program-generated in this repo |
| `gd_gen_constraints` | 11,426 | Generated by a Claude-written program in this repo |  | KEEP (program) | program-generated in this repo |
| `gd_gen_evidence_conflict` | 11,536 | Generated by Claude-written program in this repo |  | KEEP (program) | program-generated in this repo |
| `gd_gen_logic_negation` | 11,526 | CC0 1.0 |  | KEEP (program) | program-generated in this repo |
| `gd_gen_msn_consent` | 5,161 | Generated by Claude-written program in this repo |  | KEEP (program) | program-generated in this repo |
| `gd_gen_msn_fault` | 6,197 | Generated by Claude-written program in this repo |  | KEEP (program) | program-generated in this repo |
| `gd_gen_msn_rules` | 8,253 | Generated by Claude-written program in this repo |  | KEEP (program) | program-generated in this repo |
| `gd_gen_nlr_heuristics` | 4,930 | CC0 1.0 |  | KEEP (program) | program-generated in this repo |
| `gd_gen_numeric_dates` | 11,531 | Generated by Claude-written program in this repo |  | KEEP (program) | program-generated in this repo |
| `gd_gen_policy_exceptions` | 11,463 | Generated by Claude-written program in this repo |  | KEEP (program) | program-generated in this repo |
| `gd_gen_ranking` | 11,544 | Generated by a Claude-written program in this repo |  | KEEP (program) | program-generated in this repo |
| `gd_gen_routing` | 11,496 | Generated by Claude-written program in this repo |  | KEEP (program) | program-generated in this repo |
| `gd_gen_tables` | 11,605 | Generated by Claude-written program in this repo |  | KEEP (program) | program-generated in this repo |
| `gd_ghc_hate` | 1,273 | CC BY 4.0 |  | KEEP |  |
| `gd_hatemoji_build_v14` | 2,541 | CC BY 4.0 |  | KEEP |  |
| `gd_helpsteer2_attr` | 2,729 | CC BY 4.0 |  | VERIFY or drop | creator's HF card only (decision 6); read an official record (repo LICENSE, project page, paper release) or drop; judged-object exception |
| `gd_helpsteer3_pref` | 3,369 | CC BY 4.0 |  | VERIFY or drop | creator's HF card only (decision 6); read an official record (repo LICENSE, project page, paper release) or drop; minus 1 OHS-3 overlap unit (A10); judged-object exception |
| `gd_hotpotqa_yesno` | 3,274 | CC BY-SA 4.0 | SA | KEEP |  |
| `gd_infotabs_nli` | 7,024 | Apache-2.0 |  | KEEP |  |
| `gd_logicinference` | 5,587 | Apache-2.0 |  | KEEP |  |
| `gd_mediqa_qa` | 639 | CC BY 4.0 |  | KEEP |  |
| `gd_medmcqa_subject` | 7,977 | MIT |  | KEEP |  |
| `gd_medqa_yn` | 8,274 | MIT |  | KEEP |  |
| `gd_medquad_qtype` | 5,781 | CC BY 4.0 |  | KEEP |  |
| `gd_meganegraising` | 150 | CC BY-SA 4.0 | SA | KEEP |  |
| `gd_megaveridicality` | 1,424 | CC BY-SA 4.0 | SA | KEEP |  |
| `gd_mfrc` | 8,254 | CC BY 4.0 |  | VERIFY or drop | creator's HF card only (decision 6); read an official record (repo LICENSE, project page, paper release) or drop |
| `gd_misogyny_reddit` | 328 | MIT |  | KEEP |  |
| `gd_msha_injury` | 8,683 | US Government work, public domain |  | KEEP |  |
| `gd_mtbench_human` | 970 | CC BY 4.0 |  | VERIFY or drop | creator's HF card only (decision 6); read an official record (repo LICENSE, project page, paper release) or drop; judged-object exception |
| `gd_multiwoz21_sysacts` | 2,703 | MIT |  | KEEP |  |
| `gd_naics_subsector` | 2,904 | US Government work, public domain |  | KEEP |  |
| `gd_ncbi_disease` | 3,880 | Public domain, US Government Work |  | KEEP |  |
| `gd_ncvec_ham` | 1,870 | Public domain |  | KEEP |  |
| `gd_nhtsa_complaints` | 2,856 | US Government work, public domain |  | KEEP |  |
| `gd_nrc_gfe` | 3,152 | US Government work, public domain |  | KEEP |  |
| `gd_oiics_event` | 6,872 | CC0 1.0 / US Government work |  | KEEP |  |
| `gd_onestop_level` | 1,731 | CC BY-SA 4.0 | SA | KEEP |  |
| `gd_onet_occupation` | 1,629 | CC BY 4.0 |  | KEEP |  |
| `gd_opentdb` | 5,139 | CC BY-SA 4.0 | SA | KEEP |  |
| `gd_politeness_votes` | 1,444 | CC BY 4.0 |  | KEEP |  |
| `gd_prm800k_steps` | 5,317 | MIT |  | KEEP | judged-object exception (LLM outputs judged by humans) |
| `gd_prontoqa` | 1,434 | Apache-2.0 |  | KEEP |  |
| `gd_qasc` | 6,107 | CC BY 4.0 |  | VERIFY or drop | creator's HF card only (decision 6); read an official record (repo LICENSE, project page, paper release) or drop |
| `gd_quartz` | 1,798 | CC BY 4.0 |  | VERIFY or drop | creator's HF card only (decision 6); read an official record (repo LICENSE, project page, paper release) or drop |
| `gd_ragtruth_summary` | 953 | MIT |  | KEEP | judged-object exception; DI RAGTruth-adjacent (disclose); CNN/DM text, MIT covers annotations |
| `gd_redocred` | 7,979 | MIT |  | KEEP | minus 6 OHS-3 overlap units (A10) |
| `gd_ropes_sci` | 941 | CC BY 4.0 |  | VERIFY or drop | creator's HF card only (decision 6); read an official record (repo LICENSE, project page, paper release) or drop |
| `gd_saferproducts_severity` | 5,314 | US Government public data, public domain: data.gov record 'S |  | KEEP |  |
| `gd_sc101` | 8,261 | CC BY-SA 4.0 | SA | KEEP |  |
| `gd_sd311_routing` | 5,799 | ODC-PDDL public domain dedication |  | KEEP |  |
| `gd_semtabfacts_sci` | 4,048 | CC BY 4.0 |  | KEEP |  |
| `gd_slur_usage` | 3,477 | MIT |  | KEEP |  |
| `gd_smcalflow_action` | 6,220 | CC BY-SA 4.0 | SA | KEEP |  |
| `gd_spiced` | 1,002 | MIT |  | VERIFY or drop | creator's HF card only (decision 6); read an official record (repo LICENSE, project page, paper release) or drop |
| `gd_star_next_action` | 3,339 | MIT |  | KEEP |  |
| `gd_storm_ef` | 5,427 | US Government work, public domain |  | KEEP | weather events: makes weather-heavy sealed domains 'adjacent' |
| `gd_tabmcq` | 1,188 | CC BY-SA 4.0 | SA | KEEP |  |
| `gd_taskmaster1` | 3,692 | CC BY 4.0 |  | KEEP |  |
| `gd_taskmaster2` | 2,370 | CC BY 4.0 |  | KEEP |  |
| `gd_taskmaster3` | 2,335 | CC BY 4.0 |  | KEEP |  |
| `gd_tathqa` | 4,154 | Apache-2.0 |  | KEEP |  |
| `gd_tatqa` | 6,740 | CC BY 4.0 |  | KEEP |  |
| `gd_totto_claims` | 6,226 | CC BY-SA 3.0 | SA | KEEP |  |
| `gd_uds_ordinal` | 4,009 | CC BY-SA 4.0 | SA | KEEP |  |
| `gd_usb_factuality` | 1,253 | Apache-2.0 |  | KEEP |  |
| `gd_uscg_mariner` | 8,810 | US Government work, public domain |  | KEEP |  |
| `gd_vader_intensity` | 3,389 | MIT |  | KEEP |  |
| `gd_wands_product` | 2,152 | MIT |  | KEEP |  |
| `gd_webred` | 3,548 | CC BY 4.0 |  | KEEP |  |
| `gd_wiki_help_routing` | 6,440 | CC BY-SA 4.0 / CC BY-SA 3.0 + GFDL | SA | KEEP |  |
| `gd_winogrande` | 4,734 | CC-BY |  | KEEP | train split only (DI uses validation) |
| `gd_wnut17` | 1,616 | CC BY 4.0 |  | KEEP |  |
| `gd_wtq` | 5,183 | CC BY-SA 4.0 | SA | KEEP |  |
| `hard_affect` | 292 | (none in meta) |  | DROP (default) | Claude-written golds, blind-solved. Owner may grandfather |
| `hard_affect_c` | 109 | (none in meta) |  | DROP (default) | Claude-written golds, blind-solved. Owner may grandfather |
| `hard_clinical` | 242 | (none in meta) |  | DROP (default) | Claude-written golds, blind-solved. Owner may grandfather |
| `hard_codebook_c` | 150 | (none in meta) |  | DROP (default) | Claude-written golds, blind-solved. Owner may grandfather |
| `hard_contracts` | 252 | (none in meta) |  | DROP (default) | Claude-written golds, blind-solved. Owner may grandfather |
| `hard_evidence_a` | 254 | (none in meta) |  | DROP (default) | Claude-written golds, blind-solved. Owner may grandfather |
| `hard_evidence_b` | 250 | (none in meta) |  | DROP (default) | Claude-written golds, blind-solved. Owner may grandfather |
| `hard_evidence_claims_a` | 268 | (none in meta) |  | DROP (default) | Claude-written golds, blind-solved. Owner may grandfather |
| `hard_evidence_claims_b` | 242 | (none in meta) |  | DROP (default) | Claude-written golds, blind-solved. Owner may grandfather |
| `hard_intent_c` | 114 | (none in meta) |  | DROP (default) | Claude-written golds, blind-solved. Owner may grandfather |
| `hard_nli_a` | 234 | (none in meta) |  | DROP (default) | Claude-written golds, blind-solved. Owner may grandfather |
| `hard_nli_b` | 276 | (none in meta) |  | DROP (default) | Claude-written golds, blind-solved. Owner may grandfather |
| `hard_nli_c` | 126 | (none in meta) |  | DROP (default) | Claude-written golds, blind-solved. Owner may grandfather |
| `hard_policy_a` | 274 | (none in meta) |  | DROP (default) | Claude-written golds, blind-solved. Owner may grandfather |
| `hard_policy_b` | 256 | (none in meta) |  | DROP (default) | Claude-written golds, blind-solved. Owner may grandfather |
| `hard_policy_c` | 127 | (none in meta) |  | DROP (default) | Claude-written golds, blind-solved. Owner may grandfather |
| `hard_reason_c` | 137 | (none in meta) |  | DROP (default) | Claude-written golds, blind-solved. Owner may grandfather |
| `hard_scales` | 272 | (none in meta) |  | DROP (default) | Claude-written golds, blind-solved. Owner may grandfather |
| `judge_helpsteer2` | 461 | (none in meta) |  | VERIFY or drop | creator's HF card only (decision 6); read an official record (repo LICENSE, project page, paper release) or drop (same record as gd_helpsteer2_attr); judged-object exception |
| `judge_mathderiv` | 479 | (none in meta) |  | KEEP (program) | procedural (build_judge.py); stamp CC0 1.0 (program-generated) |
| `judge_prm800k` | 826 | (none in meta) |  | KEEP (mapped) | map to MIT, github.com/openai/prm800k (as gd_prm800k_steps); judged-object exception |
| `logiqa2` | 441 | (none in meta) |  | DROP | CC BY-NC-SA 4.0 upstream (github.com/csitfun/LogiQA2.0) |
| `massive` | 1,703 | (none in meta) |  | VERIFY or drop | candidate CC BY 4.0 (github.com/alexa/massive) |
| `mnli` | 661 | (none in meta) |  | VERIFY or drop | MultiNLI: mixed licences by genre; check the official MultiNLI page |
| `mnli3` | 1,090 | (none in meta) |  | VERIFY or drop | MultiNLI: mixed licences by genre (OANC, CC BY-SA 3.0 fiction, other); check the official MultiNLI page |
| `mnli_neutral` | 164 | (none in meta) |  | VERIFY or drop | MultiNLI: mixed licences by genre; check the official MultiNLI page |
| `mrpc` | 632 | (none in meta) |  | DROP | GLUE licence unknown; glue/mrpc forbidden |
| `musr_murder_mysteries` | 111 | (none in meta) |  | DROP | DI test items (MuSR has no train split) |
| `musr_object_placements` | 96 | (none in meta) |  | DROP | DI test items (MuSR has no train split) |
| `musr_team_allocation` | 91 | (none in meta) |  | DROP | DI test items (MuSR has no train split) |
| `pg_conflict` | 369 | (none in meta) |  | KEEP (program) | procedural generator (build_pg.py); stamp CC0 1.0 (program-generated) |
| `pg_evidence` | 395 | (none in meta) |  | KEEP (program) | procedural generator (build_pg.py); stamp CC0 1.0 (program-generated) |
| `pg_multihop` | 396 | (none in meta) |  | KEEP (program) | procedural generator (build_pg.py); stamp CC0 1.0 (program-generated) |
| `pg_numeric` | 404 | (none in meta) |  | KEEP (program) | procedural generator (build_pg.py); stamp CC0 1.0 (program-generated) |
| `pg_policy` | 371 | (none in meta) |  | KEEP (program) | procedural generator (build_pg.py); stamp CC0 1.0 (program-generated) |
| `pg_routing` | 378 | (none in meta) |  | KEEP (program) | procedural generator (build_pg.py); stamp CC0 1.0 (program-generated) |
| `pg_temporal` | 375 | (none in meta) |  | KEEP (program) | procedural generator (build_pg.py); stamp CC0 1.0 (program-generated) |
| `planted_a` | 448 | (none in meta) |  | DROP (default) | Claude-written golds, blind-solved. Owner may grandfather |
| `planted_b` | 442 | (none in meta) |  | DROP (default) | Claude-written golds, blind-solved. Owner may grandfather |
| `proc_adversarial` | 186 | (none in meta) |  | DROP (default) | Claude-written golds, blind-solved. Owner may grandfather |
| `proc_evidence` | 165 | (none in meta) |  | DROP (default) | Claude-written golds, blind-solved. Owner may grandfather |
| `proc_longpolicy` | 150 | (none in meta) |  | DROP (default) | Claude-written golds, blind-solved. Owner may grandfather |
| `proc_multihop` | 152 | (none in meta) |  | DROP (default) | Claude-written golds, blind-solved. Owner may grandfather |
| `proc_routing` | 157 | (none in meta) |  | DROP (default) | Claude-written golds, blind-solved. Owner may grandfather |
| `proc_rubric` | 128 | (none in meta) |  | DROP (default) | Claude-written golds, blind-solved. Owner may grandfather |
| `proc_temporal` | 188 | (none in meta) |  | DROP (default) | Claude-written golds, blind-solved. Owner may grandfather |
| `proc_tradeoff` | 155 | (none in meta) |  | DROP (default) | Claude-written golds, blind-solved. Owner may grandfather |
| `proc_trap` | 169 | (none in meta) |  | DROP (default) | Claude-written golds, blind-solved. Owner may grandfather |
| `proofwriter` | 687 | (none in meta) |  | VERIFY or drop | candidate CC BY 4.0 at the AllenAI original (not the tasksource mirror) |
| `qnli` | 903 | (none in meta) |  | VERIFY or drop | GLUE QNLI (from SQuAD 1.1, CC BY-SA 4.0); GLUE terms to check |
| `rte` | 952 | (none in meta) |  | DROP | GLUE licence unknown |
| `std_evidence` | 444 | (none in meta) |  | DROP (default) | Claude-written golds, blind-solved. Owner may grandfather |
| `std_hate` | 378 | (none in meta) |  | DROP (default) | Claude-written golds, blind-solved. Owner may grandfather |
| `std_hearsay` | 276 | (none in meta) |  | DROP (default) | Claude-written golds, blind-solved. Owner may grandfather |
| `std_trademark` | 440 | (none in meta) |  | DROP (default) | Claude-written golds, blind-solved. Owner may grandfather |
| `tb_label_nli` | 1,288 | (none in meta) |  | DROP | Forbidden label-NLI set; licence 'other' |
| `toxic_conv` | 729 | (none in meta) |  | DROP | Jigsaw-derived (SetFit/toxic_conversations_50k); no licence; not grandfatherable |
| `wiki_stance_afd` | 901 | (none in meta) |  | DROP | No licence on the card; AfD is a JevBench jagged source |
| `yahoo` | 538 | (none in meta) |  | DROP | Licence unknown (Webscope); forbidden list; read from a test split |
| `yelp` | 303 | (none in meta) |  | DROP | Yelp agreement non-commercial; read from a test split |
| `yelp5` | 373 | (none in meta) |  | DROP | Yelp agreement non-commercial; read from a test split |

**Totals by status:** KEEP 303,511; KEEP (program) 121,567; KEEP (mapped) 826; VERIFY or drop 53,270; DROP 9,085; DROP (default) 13,473; all 501,732 rows in 204 sources.
<!-- REPLAY_TABLE_END -->

## 5. Deny-list (never use for C training)

The program deny-list is the union of: every `golden_src/*/rejected.json` entry, `golden_src/forbidden_label_nli.json`
(152 tasks), `ohs3/used_sources.json` (read by program only), the OHS-1/2/3 source list in `GOLDEN_SPEC.md`, the dev and
eval sources, and the rows below.

| Dataset | Reason | Evidence |
|---|---|---|
| ShARC | About 15-20% wrong golds in about 34 hand-checked yes/no rows, clustered on negatively phrased rules | `nli_logic_reasoning/rejected.json` |
| Measuring Hate Speech | "avoid to be safe" in ohs3/used_sources.json | `calibration_distributions`, `ordinal_scales` rejected.json; `build_mhs_hate.py` |
| CAD-SNLI | SNLI "avoid" in used_sources; sibling `counterfactually-augmented-imdb` and SNLI reusers `defeasible-nli/snli`, `probability_words_nli/usnli` are forbidden | `forbidden_label_nli.json` |
| Social IQa | No licence in card or loader; ATOMIC contexts (delta-ATOMIC forbidden); label quality | `moral_social_norms/rejected.json` |
| CosmosQA | Licence only "as reported via email"; Spinn3r blog text needs a signed research agreement (https://www.icwsm.org/2009/data/) | `mcq_exams/rejected.json`; https://huggingface.co/datasets/allenai/cosmos_qa |
| NewsMTSC | Text from POLUSA ("may only be used for non-commercial research and educational use … must not be shared") and Bias Flipper; MIT covers annotations only | https://aclanthology.org/2021.eacl-main.142.pdf (section 3); https://zenodo.org/records/3946057 |
| e-CARE, PIQA, COPA-style sets (as new data) | Only 2 options; PIQA is AFL-3.0 | `mcq_exams/rejected.json` |
| EmoBank (per-rater), ConvAbuse severity | Per-rater labels almost all neutral; texts already used | `calibration_distributions`, `ordinal_scales` rejected.json |
| Steam Review Aspect (as new data) | Creator's card only; 900-review train pool, already used | `breadth_src/build_steam_aspect.py` |
| doc2dial / MultiDoc2Dial | Licence only on the HF card / project site | `intent_business_support/rejected.json` |
| NLU++, HWU64, HINT3, SNIPS, SLURP, CLINC150 (new rows), Banking77, MASSIVE (new rows), SGD intents | In used_sources or OHS-1 | `large_labelsets/rejected.json` |
| Civil Comments, toxic_conversations, Jigsaw, Wikipedia Talk Labels, HateXplain, CAD (Contextual Abuse) | Inside forbidden `mbib-base` (MBIB `040_Jigsaw` = Jigsaw Unintended Bias = Civil Comments) | https://github.com/Media-Bias-Group/Media-Bias-Identification-Benchmark/tree/main/datasets/040_Jigsaw |
| Yelp, Yahoo Answers, LogiQA 2.0, Amazon polarity, GLUE MRPC/RTE | Non-commercial, unknown or forbidden (section 4) | section 4 |
| WANLI, ProsocialDialog, HH-RLHF red-team, Aegis 2.0 responses, When2Call, xLAM, ToolACE, Glaive, Hermes FC, SPML, Bitext, lmarena-55k, ToxiGen, BeaverTails, FLUTE | LLM-written text or labels | research report |
| MTOP | 38% of utterances shared with TOPv2 (in C1) | research report |
| SciTail; SWAG; alpha-NLI | No licence file; source text terms unclear | `SELECTION.md`; research report |
| UCI German Credit, Default of Credit Card Clients | Real-outcome labels (high Bayes error) | design rule |
| CUAD, MAUD, ContractNLI, PrivacyQA, OPP-115, Unfair-ToS, LexGLUE tasks | LegalBench / LexGLUE family (OHS-1) or DI test | `FREEZE.md`, DI suite |
| ESCI, GSM8K, HoVer, HellaSwag, MuSR, BBH inputs | Decision Index tests or adjacent | https://github.com/sinanuozdemir/decision-index/blob/main/docs/suite.md |
| openFDA recalls, big_patent, Federal Register, NVD CVE, Rosetta Code, Stack Exchange, Zenodo record text, arXiv 2026, medRxiv, TabFact, VitaminC/FEVER, and the rest of the OHS list | OHS sources | `GOLDEN_SPEC.md` |
| CodeReviewer | Out by default (decision 7): per-repo licences unknown (Zenodo hosting itself is not the reason) | https://zenodo.org/records/6900648 |
| Natural Questions | Wikipedia; overlaps the C public Wikipedia sets | rules review |
| DocFinQA (merge 3 Oct) | Licence only in the creator's HF card (decision 6: unverified); train and dev "not fully validated"; code "generated by WizardCoder LLMs". Class `taint` (licence, LLM artefact) | `LICENCE_CHECK_3.md` #6 |
| FinTabNet report text: MultiHiertt, ConvFinQA (new rows) and `gd_finqa` (replay) (merge 3 Oct) | Text licence CDLA-Permissive-1.0 is stated only in the FinQA and MultiHiertt papers; IBM's own record was not reached; the licence is not on the allowed list. Class `taint` (licence). Comes back only by amendment after IBM's record is read **and** the owner accepts CDLA-Permissive-1.0 | `LICENCE_CHECK_1.md` #10, `LICENCE_CHECK_3.md` #9 |
| Qasper papers whose arXiv licence is NC or ND (merge 3 Oct) | Qasper chose papers under "CC-BY-*", which includes NC and ND. Per-paper program filter (row 5); the dataset itself stays IN | `LICENCE_CHECK_2.md` #5 |

## 6. Notes for claims and disclosures

**Share-alike (never publish derived rows; owner sign-off for commercial weights).** New: SQuAD 2.0 and DROP (whole
datasets); every MuSiQue row (Wikipedia paragraphs, CC BY-SA seed questions); the Wikipedia text inside
2WikiMultihopQA, HybridQA (WikiTables-WithLinks) and WikiSQL (tables); Qasper papers whose arXiv licence is CC BY-SA.
Replay: every row marked SA in section 4.

**Attribution.** A third-party notices file lists every CC BY, MIT, BSD and Apache source (new and replay), the UCI
creators (Bohanec, Rajkovic), every commit repo (with Apache-2.0 NOTICE text where present), and every SA source.

**Third-party text under a clean dataset licence (recorded, not a blocker; decided by default, the owner may
override).** XED (OpenSubtitles lines; no text licence found, OPUS page 404), MAMS (Citysearch reviews), Sarcasm v2
(The Onion, HuffPost), GHC and EDOS (Gab, Reddit; CC0 covers Rewire's rights only), commit messages and diffs (each
repo's licence), Wikipedia-based sets. QuALITY's Slate articles are no longer in this list: OANC terms are verified
(any use, including commercial).

**Not cleared (OUT).** DocFinQA (creator's HF card only), MultiHiertt and ConvFinQA (FinTabNet text). See table 1 and
section 5.

**Zenodo.** This plan reads "Zenodo" in the OHS list as the OHS-3 Zenodo text source, not as "hosted on Zenodo". C1
already trains on 7 Zenodo-hosted sources (about 19.5K rows), and the counts-only OHS-3 check found no overlap from
them. Decided by default (decision 7); the owner may override.

**Decision Index adjacency (report DI results on these as "related", never "unseen").**
- F12 copies When2Call's four-outcome design (DI test #62).
- Replay `gd_ragtruth_summary` (953 rows, train split) sits next to DI RAGTruth (#59).
- HoVer (#61) uses Wikipedia intro paragraphs that MuSiQue, 2Wiki and HotpotQA share; the blind check drops overlaps.
- `gd_winogrande` and `arc` use train splits only (DI uses WinoGrande validation and the ARC test).
- MAMS may share a review pool with DI's ACOS; counts-only dedupe.
- CLINC150 replay rows (if verified) and BANKING77 (dropped by default) are DI test datasets' train splits.

**Practice sets, not clean held-out tests.** JevBench public (the C design used its hard yes/no result; its hard tier
was written by Claude Opus 5 and GPT-5.6 Sol, so Claude-written items may resemble it) and ejs-5 (now in-domain: the C
design used its task kinds and per-task losses). OHS-1 and OHS-2 are practice sets after A12.

**Jev outputs.** Never used to train, select data, weights, candidates or temperatures. Paths are listed in
`C_DATA_SPEC.md` 7.4. Jev's terms forbid training on its outputs; LongBench-related terms forbid publishing Jev
benchmark results, so check before any public claim.

**Disclosure owed now.** C1 trained on 607 NewsMTSC rows whose text comes from non-commercial POLUSA.

**Record (merge 3 Oct).** C1 also trained on 4,970 `gd_finqa` rows whose FinTabNet report text has no verified licence
record (two papers state CDLA-Permissive-1.0, which allows commercial use). This is not a known non-commercial use, so
no disclosure is owed now; list it if a claim names C1's sources, and close it by reading IBM's record.

**Record (verifier 3 Oct).** C1 also trained on 38,521 rows from 15 sources whose only licence record is the creator's
HF card (section 4, now "VERIFY or drop" for C). None is a known non-commercial use; list them if a claim names C1's
sources.

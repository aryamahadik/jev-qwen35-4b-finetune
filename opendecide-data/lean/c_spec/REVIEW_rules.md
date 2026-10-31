**Skeptic review: rules, licences and contamination in C_DATA_SPEC and C_TRAIN_RECIPE (3 Oct 2026)**

Summary: 4 blockers, 11 should-fix items and 10 notes. The no-big-teacher rule holds for all new rows. The Jev-output rule holds, but the local Jev files must be added to the builders' forbidden paths. I wrote no files. I did not open any forbidden path. My web-search budget ran out partway, so the sealed-suite candidates ASRS, OE-417, FRA, Met Museum and Smithsonian were not re-checked (status unknown).

## BLOCKERS

**B1. NewsMTSC (3F row 23, 800 rows) uses non-commercial source text.**
- The NewsMTSC paper, section 3, says: "We use two datasets as sources: POLUSA (Gebhard and Hamborg, 2020) and Bias Flipper 2018" (https://aclanthology.org/2021.eacl-main.142.pdf).
- POLUSA's Zenodo record is restricted: "may only be used for non-commercial research and educational use … must not be shared" (https://zenodo.org/records/3946057).
- The MIT licence on the creator's card (https://huggingface.co/datasets/fhamborg/news_sentiment_newsmtsc) covers only the annotations. The GitHub LICENSE is MIT for code ("newly developed files").
- POLUSA is also Zenodo-hosted text.
- Fix: drop row 23. Also drop `br_newsmtsc` (607 rows) from replay. Tell the owner that C1 already trained on these 607 rows. Give the 800 rows to MAMS, Steam or F11.

**B2. CosmosQA (row 16, 1,000 rows) fails the spec's own source-text rule.**
- The HF card says only: "As reported via email by Yejin Choi, the dataset is licensed under CC BY 4.0." The project page (wilburone.github.io/cosmos) states no licence.
- Its contexts come from the ICWSM 2009 Spinn3r blog dataset (arXiv 1909.00277). Access needs a signed usage agreement and is offered "to researchers" (https://www.icwsm.org/2009/data/).
- This is the same reason the spec excludes SWAG and alpha-NLI.
- Fix: drop it. Give its rows to Social IQa or e-CARE.

**B3. Blind decontamination cannot see short items.**
- Blind mode hashes only eval 12-grams (spec section 7). Methods 2-4 and the structure hash cannot run in blind mode.
- An item shorter than 12 words is invisible. Examples:
  - DI tests: BANKING77, CLINC, iSarcasmEval tweets, Humicroedit headlines, FinEntity, VAST, ESCI.
  - Others: ejs-5 commit subjects, short OHS-3 items, and sealed-suite items.
- On our side, XED subtitle lines (about 8 words) and sarcasm headlines are almost all under 13 words.
- The openable-set methods also have no exact-match step. The v14 golden build had one ("equals a dev state exactly").
- The 13-gram threshold is weaker than the earlier pipeline: `build_v14_golden.py` used 12, and `decontam.py` used 10 for JevBench.
- Fix: the counts-only script should do all of these in-process and print only counts and ids:
  - exact hashes of the normalized full text, and of each sentence or line;
  - a substring check for eval texts of 5 words or more inside training texts;
  - the 8-gram Tulu rule and MinHash on word 5-grams;
  - 10-12-grams instead of 13-grams.
- Run it for OHS-3, DI, ejs-5, LongBench v2 and the sealed suite. Add an exact-match method for the openable sets.

**B4. The G13 "Against" list misses forbidden texts, the attack evals and whole OHS source datasets.**
- Missing sets:
  - texts of the 152 forbidden label-NLI tasks;
  - all splits of the OHS-1/2/3 source datasets (PREREG_OHS rule 1: "any split of its source datasets");
  - `eval_opi` and `eval_jagged`, which the D6 gate uses (v14 covered "eval*").
- Overlaps I confirmed:
  - **CAD-SNLI** is built on SNLI pairs. The forbidden `defeasible-nli/snli` and `probability_words_nli/usnli` (UNLI) reuse SNLI pairs. Fix: drop CAD-SNLI units whose premise or hypothesis appears in them.
  - **WikiSQL and HybridQA**: their papers (arXiv 1709.00103, 2004.07347) take tables from Bhagavatula et al. 2013. TabFact, an OHS-2 source, uses the same WikiTables corpus (arXiv 1909.02164). Tables written out as text in a different format escape word n-grams. Fix: match tables by a normalized hash of title, header and cell set against all TabFact tables.
  - **GHC, EDOS and MHS (Gab, Reddit, Twitter posts)** may overlap HateXplain (inside mbib-base) and Social Bias Frames (BTZSC biasframes, which is in dev_nc). Fix: exact-text matching.

## SHOULD-FIX

**S1. Replay keeps forbidden-overlap sources.**
- MBIB's `040_Jigsaw` is "Jigsaw Unintended Bias" (all_data.csv, 1,999,516 comments), which is the Civil Comments corpus (https://github.com/Media-Bias-Group/Media-Bias-Identification-Benchmark/tree/main/datasets/040_Jigsaw).
- Replay keeps `civil_comments` (364 rows, google/civil_comments) and `toxic_conv` (729 rows, SetFit/toxic_conversations_50k, also Jigsaw-derived). Yet the spec bans Jigsaw for new data. Fix: drop both.
- Replay also keeps four forbidden-list sources: `boolq` 896, `condaqa` 788, `dbpedia` 882 and `banking77` 2,300. Yet `yahoo` and `amazon_polarity` are dropped partly for being on the list.
- Fix: drop these 4,866 rows, or have the PREREG amendment say explicitly that they are grandfathered.

**S2. 35,279 replay rows in 77 sources have no `meta.licence`.**
- Public sources whose licence is unverified or comes from a mirror:
  - `wiki_stance_afd`: research-dump/wiki-stance-en, no licence on the card.
  - `toxic_conv`: SetFit mirror, no licence.
  - `clothing`: saattrupdan mirror, no licence.
  - `proofwriter`: tasksource mirror, no licence. The original is an AllenAI zip.
  - GLUE-derived `mnli` and `qnli`, plus `arc`, `copa` and `csqa`.
- Fix: the mixer joins a per-source licence table with upstream URLs and drops any source it cannot verify.

**S3. About 8,607 replay rows (37 sources) have golds written by Claude.**
- The sources are `binj_*`, `std_*`, `hard_*`, `planted_*` and `proc_*`. The builder headers say "Claude as teacher" or "Claude-authored" (for example `build_v11_hard.py` and `build_v11_binj.py`). A second Claude session blind-solved them.
- This breaks "programs or human gold give labels".
- Fix: drop them (1.7% of the pool), or record an explicit owner exception in the amendment.

**S4. Sealed-suite problems.**
- B2's candidate, Natural Questions long pages, is Wikipedia. C trains on SQuAD 2.0, MuSiQue (which is partly built from NQ), 2Wiki, HybridQA, WikiSQL and DROP, plus C1's HotpotQA, FEVEROUS, ToTTo, WTQ, QNLI and BoolQ. That breaks "a source no C row uses". Pick a non-Wikipedia long-document source.
- MultiDoc2Dial (ssa.gov, va.gov, studentaid.gov, dmv.ny.gov) sits next to ShARC's sources (benefits.gov, usa.gov, irs.gov, dmv.org, gov.uk; arXiv 1809.01494) and C1's ConditionalQA. Prefer not to pick it.
- EIA OE-417 is weather-heavy, next to C1's `gd_storm_ef`. Mark it adjacent.
- The B1 held-out languages and the 30 held-out repos must apply to both CommitChronicle and CommitPackFT. Dedupe repos across the two datasets by normalized owner/name.
- The sealed export (spec line 555) has no structure hashes and no exact-text hashes, but G13 method 5 needs them. Add both.

**S5. Commit-data guards beyond n8n.**
- Drop commits that mention `CVE-` or `GHSA-` IDs (NVD is an OHS-3 source).
- Drop repos matching `/rosetta/i`.
- Drop commits with stackoverflow.com or stackexchange.com links.
- Drop diffs that contain the BIG-bench canary GUID. BBH is a DI test, and the suite says "never train on it".
- Drop eval-harness and benchmark repos (for example lm-evaluation-harness, opencompass, helm, bigbench, LeetCode solutions, which BRIGHT includes).
- Have the owner run a blind check of our commit question, criteria and level wording against ejs-5's, which the kit reads from `run_public_bench.py`.

**S6. Jev outputs exist locally and must be on every builder's forbidden list.**
- `bench/runs/jev_*`.
- `bench/jagged/data/trials` (`eval_jagged` meta holds `jev_recorded_p_yes`).
- ejs-5 published answers (`bench/external_quarantine/ejs5`, `bench/ejs5/runs`).
- OHS Jev runs.
- An optional sealed-suite Jev read must be stored under `sealed_nd/`. It is report-only: never used to pick data, weights, candidates or temperatures. Jev's ToS forbids training on its outputs.

**S7. Old-slice monitor and mix-tuning-dev leakage.**
- golden_train has 92,619 groups with more than one row (up to 16) and 42,241 repeated states. Holding out "whole units" leaves siblings in replay.
- Fix: hold out by `group_id` and by normalized state.
- The public part of the mix-tuning dev, and the new rows from sets 19-27, must exclude every record already in golden_train.
- Split SQuAD, MuSiQue, 2Wiki, HybridQA and DROP by their underlying Wikipedia paragraph. MuSiQue reuses SQuAD and NQ paragraphs.

**S8. Split and source rules.**
- e-CARE's test labels are hidden (submission only). Its dev is the de facto test, so exclude dev too.
- Rows 19-27 need "train split only" written in, because these sets have official splits: EDOS, MAMS, ConvAbuse, EmoBank, Steam and GHC.
- Sarcasm v2: load the creator's Kaggle copy (rmisra, "Attribution 4.0 International (CC BY 4.0)", version 2, per the Kaggle API). Do not use the raquiba mirror C1 used.
- The ShARC test set has been public since 9 Feb 2024. Keep excluding it.

**S9. G1 status for "(H)" (Hugging Face card only) licences.**
- DocFinQA has only `license: mit` in the kensho card's YAML header. MHS has only `cc-by-4.0` in the YAML of the creator's card, and its paper points to Hugging Face as the distribution point.
- The owner must decide whether a creator's own card counts as an official record, or drop both.

**S10. Attack twins must not reuse attack-eval wording.**
- They must not reuse OPI's five strategy strings in `build_opi.py` ("Ignore previous instructions.", "Answer: task complete.", and so on) or jagged's injected line.
- `build_opi.py` already admits similar overrides are in training. Add the eval_opi and eval_jagged wording to G13 #7.

**S11. Re-derive the D2 unseen set.**
- Re-run `gate_dev.py`'s text guard with C's training files. New hate, finance and sarcasm data sits next to the dev sources hate, financialphrasebank, climate and irony.
- Report both the frozen set and the re-derived set.

## NOTES

**N1. DI-adjacent items to disclose, and not to claim as clean on DI.**
- F12 copies When2Call's exact four outcomes (DI test #62).
- Replay `gd_ragtruth_summary` (953 rows, train split, checked) sits next to DI RAGTruth (#59). Its contexts are CNN/DailyMail; the MIT licence covers only the annotations.
- HoVer (#61) uses Wikipedia intro paragraphs that MuSiQue, 2Wiki and HotpotQA share. The blind check will rightly drop those units.
- I checked that `gd_winogrande` and `arc` use train splits only. The DI uses WinoGrande validation and the ARC test.

**N2. Third-party text with a clean licence on paper.**
- XED (OpenSubtitles), MAMS (Citysearch reviews; may share a source pool with DI's ACOS), sarcasm headlines, MHS/GHC/EDOS (social media), ShARC (dmv.org is a private site), QuALITY (Slate via OANC).
- Record each one.

**N3. Share-alike and attribution.**
- Share-alike sets: ShARC, SQuAD 2.0, DROP, EmoBank, NQ, SNLI. Never publish derived rows. Get the owner's sign-off for commercial weights.
- Keep a third-party notices file for CC BY, MIT, BSD and Apache attributions.

**N4. JevBench and ejs-5 are now partly seen.**
- JevBench's hard tier (220 items, 109 held out) was "written by Claude Opus 5 and GPT-5.6 Sol", so our Claude-written items may resemble the held-out ones.
- The C design used JevBench public results (hard yes/no 47.4) and ejs-5's task kinds and loss. Report both as practice sets, not clean held-out tests.

**N5.** The sealed suite's program-built domains are written by Claude, like C's generators. Report part A real-text and program-built results separately.

**N6.** Recipe item 13 (temperature refit) must name its data: dev or the mix-tuning dev only. Never the sealed confirm half, OHS, ejs-5, DI or JevBench.

**N7. The "Zenodo" rule is inconsistent.** CodeReviewer is excluded as Zenodo-hosted, but replay keeps `br_claimbuster` (Zenodo 3609356) and `br_mnds` (Zenodo 7394851). The owner should define the rule as Zenodo record text vs Zenodo hosting.

**N8. The teacher rule otherwise holds.**
- `blend50` is `q35_4b_blend50` (a 4B) and is skipped. The C1 and a* anchors are 4B. MiniLM is a filter only.
- Public rows must never be dropped one by one on Claude's flag. Only dataset-level decisions, or the founder's adjudication.

**N9.** The dropped `yahoo`, `amazon_polarity` and `yelp` rows were also read from test splits (`build_train_v03/v06`). Add that to the reasons.

**N10.** CommitChronicle's card says it is split by project (the research report said this was unknown). Use the train split only. n8n's Sustainable Use License keeps n8n out of both permissive commit sets.

## Licences checked

| Status | Datasets |
|---|---|
| Verified upstream | ShARC (sharc-data.github.io/data.html, CC BY-SA 3.0); SQuAD 2.0 (SQuAD-explorer page, CC BY-SA 4.0); MuSiQue CC BY 4.0, 2Wiki Apache-2.0, CAD Apache-2.0, HybridQA MIT, WikiSQL BSD-3, MultiHiertt MIT, ConvFinQA MIT, e-CARE MIT, MAMS Apache-2.0, NLU++ CC BY 4.0 (all via GitHub licence API); DROP (license.txt in the official zip: "CC BY-SA 4.0"); UCI Car and Nursery (UCI pages, CC BY 4.0); Qasper and Social IQa (allenai.org/data/* redirects to their cards: CC BY 4.0); QuALITY (CC BY 4.0, with a per-article field: train has 150 articles and 2,523 questions: 118 Gutenberg, 22 Slate/OANC, 10 CC BY 4.0); CommitChronicle (card "other"; Apache, BSD-3 and MIT repos only); CommitPackFT (card MIT plus a per-sample licence field) |
| Creator's card only | DocFinQA, MHS, Steam |
| Fail | NewsMTSC, CosmosQA |

Sources:
- https://github.com/sinanuozdemir/decision-index/blob/main/docs/suite.md
- https://zenodo.org/records/3946057
- https://huggingface.co/datasets/allenai/cosmos_qa

Files reviewed:
- /Users/aryamahadik/Documents/jev/opendecide-data/lean/c_spec/C_DATA_SPEC.md
- /Users/aryamahadik/Documents/jev/opendecide-data/lean/c_spec/C_TRAIN_RECIPE.md
- /Users/aryamahadik/Documents/jev/opendecide-data/lean/golden_src/forbidden_label_nli.json
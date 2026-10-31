# LICENCE_CHECK_3: licence checker 3 of 3 (positions where position mod 3 == 0)

Date: 3 Oct 2026. CPU and web reads only (curl with 20 s timeouts, WebFetch, one web search). No data downloaded,
no sealed or OHS-3 path opened. Progress log: `c_spec/progress_licence3.log`.

## 1. Enumeration used (so the three checkers can be reconciled)

Rule: every public dataset that C_DATA_SPEC.md v2 names as a **source to use**, in order of appearance:
section 3.2 rows #1-#17 (the spec's own numbering), then section 4.1 (#18, #19), then section 9.
Not counted: the 3.1 example names (ContractNLI, LogiQA 2.0, FOLIO, QuAC, FeTaQA: cited only as wrong HF tags), the
3.G exclusion list, and helper sources named inside a row's notes (FinQA, FinTabNet, Wikipedia, OpenSubtitles).
**Section 9 names no candidate source by design** ("This file names no domain, source or theme of the suite"); it
names NTSB and Wikipedia only as rejections. So section 9 adds no position.

| Pos | Dataset | Pos | Dataset |
|---|---|---|---|
| 1 | SQuAD 2.0 | 11 | DROP |
| 2 | MuSiQue | **12** | **UCI Car Evaluation + Nursery** |
| **3** | **2WikiMultihopQA** | 13 | XED English |
| 4 | QuALITY | 14 | MAMS |
| 5 | Qasper | **15** | **News Headlines Sarcasm v2** |
| **6** | **DocFinQA** | 16 | Gab Hate Corpus |
| 7 | HybridQA | 17 | EDOS |
| 8 | WikiSQL | **18** | **CommitChronicle** |
| **9** | **MultiHiertt** | 19 | CommitPackFT |
| 10 | ConvFinQA | | |

Mine: positions 3, 6, 9, 12, 15, 18. If another checker counted Car and Nursery as two positions, its positions
15 and 18 become MAMS and EDOS; both are also checked here (section 4) so nothing falls through.

## 2. Results

| Pos | Dataset | Exact licence | Licence URL (official record) | Commercial use | Share-alike | Document-text caveats | Status |
|---|---|---|---|---|---|---|---|
| 3 | 2WikiMultihopQA | Apache License 2.0 | https://github.com/Alab-NII/2wikimultihop/blob/main/LICENSE | yes | no (annotations); **yes for Wikipedia text** | Paragraphs are Wikipedia text (CC BY-SA 4.0, SA) plus Wikidata facts (CC0). The LICENSE is repo-wide; the data zips are on Dropbox links from that README, no separate data licence. | verified |
| 6 | DocFinQA | MIT, **only** in the creator's HF card YAML (`license: mit`) | https://huggingface.co/datasets/kensho/DocFinQA (card only) | unknown (no official record) | unknown | Full SEC EDGAR 10-K filings (company-written public filings). Paper (arXiv 2401.06915v3) states **no dataset licence**; its "CC BY-NC-SA 4.0" header is the arXiv **paper's** licence, not the data's. No official Kensho GitHub repo found. Questions come from FinQA (MIT, verified: https://github.com/czyssrs/FinQA/blob/main/LICENSE). | **unverified** |
| 9 | MultiHiertt | MIT License (Copyright 2022 Penn State NLP Group) | https://github.com/psunlpgroup/MultiHiertt/blob/main/LICENSE | yes | no | Report text is from **FinTabNet** (S&P 500 annual reports, 1999-2019), which the MultiHiertt paper's ethics section states is **CDLA-Permissive-1.0** (FinQA is MIT). CDLA-Permissive-1.0 allows commercial use, no SA, and "imposes no obligations or restrictions on Your Use or Publication of Results" (trained weights). IBM's own FinTabNet page now redirects to a generic page, so the CDLA claim rests on the two papers. Data files are on Google Drive, covered by the repo LICENSE. | verified (annotations); text licence identified via papers, IBM page unverified |
| 12a | UCI Car Evaluation | CC BY 4.0 | https://archive.ics.uci.edu/dataset/19/car+evaluation (DOI 10.24432/C5JP48) | yes | no | None: attribute tuples made from the DEX model (creator Marko Bohanec). Attribution needed in the notices file. | verified |
| 12b | UCI Nursery | CC BY 4.0 | https://archive.ics.uci.edu/dataset/76/nursery (DOI 10.24432/C5P88W) | yes | no | None: attribute tuples from a DEX hierarchical model (creator Vladislav Rajkovic). Closes the register's "to confirm"; Car does not need to take all rows. | verified |
| 15 | News Headlines Sarcasm v2 | Attribution 4.0 International (CC BY 4.0) | https://www.kaggle.com/datasets/rmisra/news-headlines-dataset-for-sarcasm-detection (Kaggle API: `licenseNameNullable`, owner and creator Rishabh Misra, version 2 of 3 Jul 2019, note "add more sarcastic headlines") | yes | no | Headlines are third-party text (The Onion, HuffPost). The creator's GitHub repo (rishabhmisra/News-Headlines-Dataset-For-Sarcasm-Detection) has **no LICENSE file** and holds only v1. The only licence record is the creator's own Kaggle page, which is also the only official release of v2. | verified (creator's Kaggle record; see note 3) |
| 18 | CommitChronicle (JetBrains) | **CC BY 4.0** for the compilation (Zenodo record), and each commit's content under its repo licence: MIT, Apache-2.0 or BSD-3-Clause (per-commit `license` field) | https://zenodo.org/records/8189044 (DOI 10.5281/zenodo.8189044, licence id `cc-by-4.0`, open access); README on the same record; HF card https://huggingface.co/datasets/JetBrains-Research/commit-chronicle says only "other" | yes | no | Diffs and messages are code under each repo's licence: keep repo attribution (and Apache-2.0 NOTICE text) in the notices file. Card and Zenodo README clause: "In the event that the dataset contains personal information, researchers should only use public, non-personal information in support of conducting and publishing their open-access research"; authors were already replaced by ids. Scrub emails, keys and IPs from shown diffs. Zenodo-hosted, but under owner default 7 "Zenodo" means the OHS-3 Zenodo text source, not hosting, so it is allowed. | verified |

## 3. Notes and changes the spec should take

1. **DocFinQA (#6): unverified, so drop it under owner default 6** (a creator's HF card is not an official record).
   Its 250 / 500 rows go to the named fallback, F13. Two more reasons not to rescue it: the paper's Limitations
   section says "we only validated the test set while the training and the development set were not fully
   validated", and its code was "generated by WizardCoder LLMs" (an LLM artefact; spec 3.1 bans LLM labels). Under
   default 9 its filing text is not cleared either.
2. **MultiHiertt (#9): its document-text licence is now known.** CDLA-Permissive-1.0 is permissive (commercial use,
   no SA, no limits on Results such as trained weights), but it is **not on the 3.1 allowed list** by name. Default 9
   says drop unless the check clears it. Proposed action: add CDLA-Permissive-1.0 to the 3.1 list as a permissive
   data licence and keep MultiHiertt; otherwise drop it. The same FinTabNet/FinQA provenance applies to ConvFinQA
   (#10, not my position).
3. **Sarcasm v2 (#15):** the only licence record is the creator's own Kaggle page. That is the same kind of evidence
   as a creator's own HF card, but Kaggle is the dataset's only official v2 release and the licence is a structured
   field the creator set. The spec already counts it as (V). If owner default 6 is read as covering **every** creator
   platform card, this set becomes unverified and its 350 / 700 rows need a fallback. Never use the GitHub v1 file
   (no licence) or a mirror.
4. **CommitChronicle (#18):** cite the **Zenodo record (CC BY 4.0)** in `meta.licence`, not the HF card ("other").
   Add a PII scrub step to the 4.3 guards (emails, API keys, IP addresses in diffs). Commercial use is fine; per-repo
   attribution goes in the notices file.
5. **UCI Nursery (#12b):** confirmed CC BY 4.0 on its UCI page. Update LICENCE_REGISTER row 12b from "to confirm" to V.
6. **2WikiMultihopQA (#3):** matches the spec (Apache-2.0, V). The Wikipedia text is SA, as owner default 8 already
   covers (private training, never publish derived rows, notices file).

## 4. Extra checks (in case another checker split Car and Nursery)

| Dataset | Exact licence | Licence URL | Commercial | SA | Document-text caveats | Status |
|---|---|---|---|---|---|---|
| MAMS (#14) | Apache License 2.0 | https://github.com/siat-nlp/MAMS-for-ABSA (GitHub API: Apache-2.0) | yes | no | Sentences come from the Citysearch New York restaurant reviews (third-party text; the README states no source licence) | verified |
| EDOS (#17) | CC0 1.0 Universal | https://github.com/rewire-online/edos (GitHub API: CC0-1.0) | yes | no | Gab and Reddit posts (third-party text) | verified |

## 5. Sources opened

- https://github.com/Alab-NII/2wikimultihop (LICENSE, README)
- https://huggingface.co/datasets/kensho/DocFinQA (card YAML); https://arxiv.org/abs/2401.06915 and /html/2401.06915
  (paper licence header, Limitations); GitHub search "DocFinQA" (no Kensho repo);
  https://github.com/czyssrs/FinQA (LICENSE)
- https://github.com/psunlpgroup/MultiHiertt (LICENSE, README); https://arxiv.org/html/2206.01347 (FinTabNet
  CDLA-Permissive-1.0 and FinQA MIT statements); https://developer.ibm.com/exchanges/data/all/fintabnet/
  (redirects, unverified); SPDX CDLA-Permissive-1.0 text
- https://archive.ics.uci.edu/dataset/19/car+evaluation and https://archive.ics.uci.edu/dataset/76/nursery
- Kaggle API view of rmisra/news-headlines-dataset-for-sarcasm-detection; GitHub rishabhmisra repo (no LICENSE)
- https://zenodo.org/records/8189044 (API metadata and README); HF card JetBrains-Research/commit-chronicle;
  https://github.com/JetBrains-Research/commit_message_generation (code LICENSE MIT, README points to Zenodo)
- GitHub API for siat-nlp/MAMS-for-ABSA and rewire-online/edos

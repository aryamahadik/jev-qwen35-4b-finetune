# LICENCE_CHECK_2: web licence check, checker 2 of 3 (positions 2, 5, 8, ... in the list order)

Checked 3 Oct 2026. CPU and web reads only (curl with 15-90 s timeouts, WebFetch, one web search). No sealed, OHS-3
or quarantine path was opened. For DROP and Qasper the official archive was streamed through a pipe so that only the
`license.txt` / `README.md` member could be read; no data file was saved to disk. Progress log:
`c_spec/progress_licence2.log`.

## How the list was built (same as LICENCE_CHECK_1 and LICENCE_CHECK_3)

Datasets in the order they appear in `C_DATA_SPEC.md` v2:
- Section 3.2 rows #1-#17, the spec's own numbering. Row #12 "UCI Car Evaluation + Nursery" is **one** entry
  ("The list (17 datasets)").
- Section 4.1: #18 CommitChronicle, #19 CommitPackFT.
- Section 9 names no candidate source on purpose ("This file names no domain, source or theme of the suite"). It
  names only NTSB, as a rejected example. I count it as #20 so that it is covered (checker 1 flagged that #20 falls
  here). Checker 3 counts section 9 as zero positions; that changes nothing for positions 1-19.
- Not counted: the 3.G exclusion list, the 3.1 example names (wrong-HF-tag sets), and helper sources inside a row's
  notes (Wikipedia, FinQA, FinTabNet, OpenSubtitles).

| Pos | Dataset | Pos | Dataset |
|---|---|---|---|
| 1 | SQuAD 2.0 | 11 | **DROP** |
| 2 | **MuSiQue** | 12 | UCI Car Evaluation + Nursery |
| 3 | 2WikiMultihopQA | 13 | XED English |
| 4 | QuALITY | 14 | **MAMS** |
| 5 | **Qasper** | 15 | News Headlines Sarcasm v2 |
| 6 | DocFinQA | 16 | Gab Hate Corpus |
| 7 | HybridQA | 17 | **EDOS** |
| 8 | **WikiSQL** | 18 | CommitChronicle |
| 9 | MultiHiertt | 19 | CommitPackFT |
| 10 | ConvFinQA | 20 | **NTSB** (section 9, rejected example only) |

**Mine (position mod 3 == 2):** #2 MuSiQue, #5 Qasper, #8 WikiSQL, #11 DROP, #14 MAMS, #17 EDOS, #20 NTSB.
If row #12 were split in two, my positions 14 and 17 would become XED and GHC; checker 1 already covers both, and
checker 3 also checked MAMS and EDOS, so nothing falls through either way.

## Results

| # | Dataset | Exact licence | Official licence record (URL) | Upstream commit | Commercial use | Share-alike | Document-text caveats | Status |
|---|---|---|---|---|---|---|---|---|
| 2 | MuSiQue (Ans + Full) | CC BY 4.0 (LICENSE file is the CC "Attribution 4.0 International" legal code; README: "MuSiQue is distributed under a CC BY 4.0 License") | https://github.com/StonyBrookNLP/musique/blob/main/LICENSE (GitHub API spdx_id `CC-BY-4.0`) | StonyBrookNLP/musique 922ac98f19a2 | yes | annotations no; **text yes** | Paragraphs are Wikipedia text (CC BY-SA). Questions are composed from seed single-hop sets SQuAD, T-REx, Natural Questions, MLQA and Zero Shot RE (README "Usage Caution"); the first four are CC BY-SA on their own pages (not re-read in this pass), Zero Shot RE's licence was not checked. Treat derived rows as SA: private training only, list in the notices file. README asks users of the seed sets to avoid the single-hop ids in `dev_test_singlehop_questions_v1.0.json`; C also uses SQuAD 2.0, so apply that id list as a drop list on our SQuAD rows (cheap, avoids leaking MuSiQue dev/test). | verified |
| 5 | Qasper | CC BY (annotations). The official AI2 page said "License: CC BY", current version 0.3 (archived 14 Apr 2023). The same page now 302-redirects to the creator's HF card, which says `cc-by-4.0`. The official tarball's README and the paper state no dataset licence. | https://web.archive.org/web/20230414023335/https://allenai.org/data/qasper (official page, archived); now https://allenai.org/data/qasper -> https://huggingface.co/datasets/allenai/qasper | n/a (S3 tarball `qasper-train-dev-v0.3.tgz`, Last-Modified 25 Mar 2022; contains train, dev and README only) | yes (annotations) | no (annotations); **per paper for text** | **Spec correction needed.** The paper (arXiv 2105.03011, Ethics section): "To adhere to copyright, we have restricted ourselves to arXiv papers released under a CC-BY-* license, as identified via Unpaywall". "CC-BY-*" includes CC BY-NC, BY-NC-SA, BY-NC-ND and BY-ND, which are not on our list. Full text comes from S2ORC. The per-paper filter in spec row #5 must therefore read the arXiv licence of every paper (keys are arXiv ids) and keep only CC BY, CC BY-SA (SA: notices file) or CC0; drop every NC and ND paper. The "ACL Anthology CC BY 4.0" route does not apply, because the text in the file is the arXiv/S2ORC version. Keep the "< 150 papers -> drop" fallback. | verified (annotations); text per paper |
| 8 | WikiSQL | BSD 3-Clause ("Copyright (c) 2017, Salesforce Research") | https://github.com/salesforce/WikiSQL/blob/master/LICENSE (spdx_id `BSD-3-Clause`) | salesforce/WikiSQL cffb42307775 | yes | annotations no; **tables yes** | The README says "Both the evaluation script as well as the dataset are stored within the repo" (`data.tar.bz2`), so the BSD-3 file covers the released data. Tables are Wikipedia HTML tables (CC BY-SA): SA, notices file. Questions are crowd-written (no extra licence). | verified |
| 11 | DROP | CC BY-SA 4.0. `license.txt`: "The DROP dataset is distributed under CC BY-SA 4.0 license.", followed by the full CC BY-SA 4.0 legal code | `drop_dataset/license.txt` inside https://ai2-public-datasets.s3.amazonaws.com/drop/drop_dataset.zip (official AI2 zip; members dated 26 May 2019: train, dev, license.txt) | n/a (official zip, 8,308,692 bytes) | yes | **yes** | Passages are Wikipedia (CC BY-SA). The whole dataset is SA: private training only, notices file, never publish derived rows. The zip holds train and dev only (test hidden), which matches the spec's "train only". | verified |
| 14 | MAMS (ACSA + ATSA) | Apache License 2.0 (repo root LICENSE) | https://github.com/siat-nlp/MAMS-for-ABSA/blob/master/LICENSE (spdx_id `Apache-2.0`) | siat-nlp/MAMS-for-ABSA cddcdb0f423b | yes | no | The README says "This repository contains the data and code", and the data sits in `data/MAMS-ACSA` and `data/MAMS-ATSA` under that root LICENSE. Sentence text: the paper (EMNLP 2019, D19-1654) says "we annotate sentences from the Citysearch New York dataset collected by (Ganu et al., 2009)": third-party restaurant reviews with no separate text licence (the same pool as SemEval-2014 restaurants). Record as "third-party text, recorded, not a blocker", like XED. Keep the counts-only dedupe vs DI's ACOS. | verified |
| 17 | EDOS | CC0 1.0 Universal (repo root LICENSE) | https://github.com/rewire-online/edos/blob/main/LICENSE (spdx_id `CC0-1.0`) | rewire-online/edos b1f1fbcca9d4 | yes | no | The data is in the same repo (`data/edos_labelled_aggregated.csv`, `..._individual_annotations.csv`, plus 1M unlabelled Gab and 1M Reddit files). Post text: Gab posts from the pushshift.io Gab dump, and Reddit comments "collected using the Reddit API" (overview paper, arXiv 2303.04222). The CC0 waiver covers Rewire's rights only; the post text belongs to its authors, and Reddit content falls under Reddit's API terms. Record as third-party text. The paper gives a 70/10/20 split (train 14,000 of 20,000). This closes the register's "to confirm". The labelled CSV also holds dev and test labels, so keep the `split == train` filter. | verified |
| 20 | NTSB aviation accident data (section 9, rejected example) | none stated. US federal government work (17 U.S.C. 105), so public domain in the US by statute, but no NTSB page read here says so | https://www.ntsb.gov/Pages/Open.aspx (states no licence; links to data.gov, whose NTSB organisation page returned 404) | n/a | likely yes (US government work) | no | Narratives often state the coded outcome word for word; this is why section 9 rejects it. It is not a training source. | unverified (no explicit licence record found; moot because rejected) |

## What this changes in the spec (for the orchestrator)

1. **Qasper text filter (row #5) must be tightened.** Qasper chose papers under "CC-BY-*", which includes NC and ND
   variants. The filter must read each paper's arXiv licence and keep only CC BY, CC BY-SA or CC0. Drop the "ACL
   Anthology CC BY 4.0" route, because the text in the file is the arXiv/S2ORC version. The annotation licence (CC BY)
   is confirmed on the official AI2 page (archived). It does not rest on the HF card alone, so default (6) does not
   block Qasper.
2. **MuSiQue: one cheap extra guard.** Use MuSiQue's `dev_test_singlehop_questions_v1.0.json` as a drop list on C's
   SQuAD 2.0 rows. MuSiQue rows are SA in practice (Wikipedia paragraphs, CC BY-SA seed questions): list them in the
   notices file.
3. **SA notices file entries from my share:** MuSiQue (text), WikiSQL (tables), DROP (whole dataset).
4. **Third-party text, recorded, not a blocker:** MAMS (Citysearch reviews), EDOS (Gab and Reddit posts).
5. **EDOS train size confirmed:** 14,000 (70% of 20,000). This closes the register's "to confirm".
6. No licence in my share disagrees with `LICENCE_REGISTER.md`. The register's "(V)" marks for #2, #5, #8, #11, #14
   and #17 are confirmed. Its "allenai.org/data" evidence for Qasper is now a redirect to the HF card; cite the
   archived page above instead.

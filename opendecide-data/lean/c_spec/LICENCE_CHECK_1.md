# LICENCE_CHECK_1: web licence check, checker 1 of 3 (positions 1, 4, 7, ... in the list order)

Checked 3 Oct 2026 by a web-only session. CPU only. No data was downloaded, and no sealed or OHS-3 path was opened.
Progress log: `c_spec/progress_lc1.log`.

## How the list was built

I took the datasets in the order they appear in `C_DATA_SPEC.md`, using the spec's own numbering:
- Section 3.2 rows #1-#17. Row #12 "UCI Car Evaluation + Nursery" counts as **one** entry, because the spec calls this "The list (17 datasets)".
- Section 4.1: #18 CommitChronicle, #19 CommitPackFT.
- Section 9: the spec names no candidate source on purpose ("This file names no domain, source or theme of the suite"). The only source it names is NTSB, and only as a rejected example. If NTSB were counted it would be #20, which falls to checker 2.
- The excluded datasets in 3.G are not counted. They are not "licensed public splits".

**Mine (position mod 3 == 1):** #1 SQuAD 2.0, #4 QuALITY, #7 HybridQA, #10 ConvFinQA, #13 XED, #16 GHC, #19 CommitPackFT.

If another checker split row #12 into Car and Nursery, positions 13 onward shift by one. Positions 13, 16 and 19 would then be Nursery, Sarcasm v2 and CommitChronicle. To cover that case I also checked Nursery (Appendix A).

## Results

| # | Dataset | Exact licence (annotations / dataset) | Official licence record (URL) | Upstream commit | Commercial use | Share-alike | Document-text caveats | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | SQuAD 2.0 | CC BY-SA 4.0 | https://rajpurkar.github.io/SQuAD-explorer/ (official page: "distributed under the CC BY-SA 4.0 license", linking to creativecommons.org/licenses/by-sa/4.0/legalcode) | n/a (official site) | yes | **yes** | Passages are Wikipedia text (CC BY-SA). Keep the data private and list it in the notices file. | verified |
| 4 | QuALITY | CC BY 4.0 | https://nyu-mll.github.io/quality/ ("QuALITY is distributed under a CC BY 4.0 License"). The repo github.com/nyu-mll/quality has no LICENSE file. | nyu-mll/quality f84977c40dbf | yes | no | The paper (arXiv 2112.08608) says "we use only sources that are licensed under CC-BY (or more permissive licenses)": Project Gutenberg fiction, Slate articles from the Open American National Corpus, and The Long+Short, Freesouls and the book *Open Access*. **Slate/OANC is cleared:** https://anc.org/data/oanc/ says the OANC is "unrestricted in terms of usage and redistribution" and that users "can freely use all of our data and resources without restriction (including commercial use)". Its contents page confirms the Slate sub-corpus (4,694 articles, 1996-2000) is part of the OANC. Gutenberg texts are US public domain; strip the Gutenberg licence header and trademark text. Builders must still read each article's `license`/`source` field and drop any article whose field is not Gutenberg, OANC/Slate or CC BY. | verified (OANC terms verified) |
| 7 | HybridQA | MIT (repo LICENSE, "Copyright (c) 2020 wenhu chen") | https://github.com/wenhuchen/HybridQA/blob/master/LICENSE | wenhuchen/HybridQA db22fda8c595 | yes | annotations no; **text yes** | Tables and passages come from the separate repo github.com/wenhuchen/WikiTables-WithLinks, which has **no LICENSE file**. The text is Wikipedia content, so CC BY-SA applies: treat it as share-alike, keep it private and add a notices entry. The table-hash check against TabFact still applies. | verified |
| 10 | ConvFinQA | MIT (repo LICENSE, "Copyright (c) 2022 Zhiyu Chen") | https://github.com/czyssrs/ConvFinQA/blob/main/LICENSE | czyssrs/ConvFinQA cf3eed2d5984 | yes | no | The documents are S&P 500 earnings reports (1999-2019) from FinTabNet, through FinQA (FinQA repo licence is MIT, czyssrs/FinQA 0f16e2867bef). The FinQA paper (arXiv 2109.00122v3) says: "The FinTabNet dataset is publicly available under the CDLA-Permissive license, which permits us to create additional annotations on top of the data and publish the annotations." I could not load FinTabNet's own licence page: the IBM DAX CDN host does not resolve, and the IBM developer page has no licence text in its static HTML. **CDLA-Permissive-1.0 is not on the section 3.1 list.** It allows commercial use and has no share-alike, but it needs an owner or orchestrator OK. The company reports are copyrighted by the companies (they are not US government works). The same caveat covers C1's `gd_finqa`. | annotations verified; document text **unverified** (FinTabNet record not reached) |
| 13 | XED (English) | CC BY 4.0 (README, last line: "License: Creative Commons Attribution 4.0 International License (CC-BY)") | https://github.com/Helsinki-NLP/XED (README; there is no LICENSE file, so the API returns 404) | Helsinki-NLP/XED 76666d251f14 | yes | no | The text is movie subtitle lines from OPUS OpenSubtitles (third-party text, and the subtitles' own rights are unclear). The OPUS OpenSubtitles page returned 404, so I could not confirm a licence for the subtitle text. The README counts English annotations as "24164 + 9384 neutral". These are annotation counts, not line counts. | annotations verified; subtitle text **unverified** |
| 16 | Gab Hate Corpus (GHC) | CC BY 4.0 (OSF node licence "CC-By Attribution 4.0 International", year 2018) | https://osf.io/edua3/ (read through https://api.osf.io/v2/nodes/edua3/?embed=license, because the page renders only with JavaScript) | OSF node edua3, modified 2022-04-12 | yes | no | The text is 27,665 posts from gab.ai (third-party user posts, recorded and not a blocker). The OSF description states no research-only restriction. | verified |
| 19 | CommitPackFT (BigCode) | MIT for the dataset compilation, plus each sample's own repo licence | https://github.com/bigcode-project/octopack (README: "CommitPack, CommitPackFT, HumanEvalPack, and all code are licensed under the MIT License of this repository"; LICENSE = MIT) | bigcode-project/octopack e17a8f647026 | yes, with the per-sample filter | no, once filtered to mit, apache-2.0, bsd-2/3, isc, cc0-1.0 and unlicense (drop agpl, lgpl, mpl, epl, unknown) | The README says: "each sample within CommitPack and CommitPackFT has its own license corresponding to the repository it stems from as indicated by the `license` field". That is a repo-level licence detection, so a few files may differ from it. Commit messages are written by third-party contributors. The official record is the creator's GitHub repo and LICENSE file, not the HF card, so default (6) is satisfied. The n8n and OHS guards from spec 4.3 still apply. | verified |

## What this changes in the spec (for the orchestrator)

1. **QuALITY Slate/OANC articles pass.** The OANC terms allow any use, including commercial use, with no share-alike. Under default (9), the drop no longer applies to QuALITY's Slate articles. All 150 articles (118 Gutenberg, 22 Slate/OANC, 10 CC BY) can be used, filtered by each article's `license` field.
2. **HybridQA text is share-alike.** The MIT licence covers only the annotations. The register's "Wikipedia text CC BY-SA" note is correct. Keep it in the SA notices file.
3. **ConvFinQA document text is CDLA-Permissive-1.0.** This comes from the FinQA paper; FinTabNet's own page was not reached. The licence is not on the section 3.1 list, so it needs an owner or orchestrator decision before use. It is permissive, allows commercial use and has no share-alike. The same applies to C1's `gd_finqa` replay rows (4,970). Under default (9), MultiHiertt and DocFinQA filing text are handled by the other checkers.
4. **XED subtitle text:** the dataset licence is clean, but no licence for the source text was found. Keep the existing "third-party text, recorded, not a blocker" note.
5. No licence in my share disagrees with `LICENCE_REGISTER.md`. The register's "(V)" marks for #1, #4, #7, #10, #13, #16 and #19 are confirmed.

## Appendix A: extra cross-check (outside my positions, in case row #12 was split)

| Dataset | Licence | Record | Commercial | SA | Status |
|---|---|---|---|---|---|
| UCI Nursery | CC BY 4.0 (the page text begins "licensed under a Creative Commons Attribution 4.0") | https://archive.ics.uci.edu/dataset/76/nursery | yes | no | verified. This clears the "Nursery to confirm" note in section 3.2 #12. |
| UCI Car Evaluation | CC BY 4.0 (same wording) | https://archive.ics.uci.edu/dataset/19/car+evaluation | yes | no | verified |

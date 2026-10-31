# Golden dataset v14: data card

**Training rows: 500,000**. Practice (dev) rows: 22,503. Sources: 200. Yes/no share: 64.6%. Rows with annotator vote shares: 88,228. The families where Jev leads (moral norms, tables and fact checks, science claims) are kept in full.

**Label audit (442 stratified random rows, 4 independent auditors):**
- 91.0% correct, 6.3% ambiguous (about 6 of those came from the audit's 2,500-character cut), 2.7% wrong.
- New golden sources: about 1.5% wrong. Legacy replay: about 6% wrong.
- The replay source `judge_ifcheck` was dropped (filler responses labelled acceptable).

**Targeted audit of the priority families (450 rows, full texts):**
- Moral norms, science claims and tables: 94.2% correct, 1.3% wrong.
- A consent-generator scope bug was fixed and those rows regenerated.

**Rules:** see `golden_src/GOLDEN_SPEC.md`.
- Permissive licences only.
- Human-written texts with human labels, or exact program-generated labels.
- Training splits only.
- No model-made labels.
- Every OHS-1/2/3, eval, dev, JevBench and label-NLI source excluded.

**Decontamination:**
- 12-gram overlap against all held-out tests (168 rows dropped).
- Exact dev states removed; 1,025 duplicates dropped.
- An independent 13-gram and exact check against OHS-3 found **0** overlaps.

**Built-in extras:**
- near-miss yes/no pairs with complement links;
- attack twins (30,938) with invariance links;
- definition-swap twins (3,006);
- fact-flip twins from the generators;
- opaque option codes on 30% of choice rows.

**Not yet included:** 4B teacher soft labels for the new rows. They are computed on the GPU before the main training run.

## Rows by family
| Family | Rows |
|---|---|
| nli_logic_reasoning | 69,012 |
| fact_tables | 48,384 |
| qa_decisions | 46,534 |
| replay (v13 clean pool) | 41,918 |
| moral_social_norms | 36,130 |
| intent_business_support | 30,082 |
| relations_entities | 27,306 |
| domain_classification | 25,496 |
| large_labelsets | 24,895 |
| science_health_claims | 23,784 |
| routing_dialogue | 21,798 |
| judge_verifier | 21,291 |
| ordinal_scales | 19,870 |
| mcq_exams | 18,971 |
| safety_policy_moderation | 16,539 |
| numeric_temporal | 11,531 |
| calibration_distributions | 10,625 |
| numeric | 404 |
| multihop | 396 |
| evidence | 395 |
| routing | 378 |
| temporal | 375 |
| policy | 371 |
| conflict | 369 |
| attributed_belief | 335 |
| counterfactual | 303 |
| legal | 298 |
| polite_indirect | 293 |
| rule_out | 291 |
| statement_falsity | 287 |
| conditional | 283 |
| terse | 279 |
| modal | 211 |
| quantifier | 194 |
| affixal | 188 |
| presupposition | 184 |

## Sources (training rows, licence)
| Source | Rows | Licence |
|---|---|---|
| gd_gen_tables | 11,605 | CC0 1.0 (program-generated; Claude-written templates, vocabularies, rules and program; no  |
| gd_gen_ranking | 11,544 | CC0 1.0 (program-generated; Claude-written templates, domains, rules and program; no third |
| gd_gen_evidence_conflict | 11,536 | n/a (program-generated; Claude-written templates, vocabularies and rules, labels by constr |
| gd_gen_numeric_dates | 11,531 | n/a (program-generated; Claude-written templates and rules, labels by construction) |
| gd_gen_logic_negation | 11,526 | CC0 1.0 (Claude-written templates, word lists and program; no third-party text or labels) |
| gd_gen_routing | 11,496 | n/a (program-generated; Claude-written templates, definitions and rules; labels by constru |
| gd_gen_policy_exceptions | 11,463 | n/a (program-generated; Claude-written templates and rules, labels by construction) |
| gd_gen_constraints | 11,426 | CC0 1.0 (program-generated; Claude-written templates, vocabularies, rules and program; no  |
| gd_boardgameqa | 9,550 | CC BY (official paper arXiv:2306.07934, release footnote: 'Available at: https://storage.g |
| gd_uscg_mariner | 8,810 | US Government work, public domain (17 U.S.C. 105; USCG National Maritime Center). USCG web |
| gd_drugprot | 8,794 | CC BY 4.0 (Zenodo record https://zenodo.org/records/5119892 metadata 'license: cc-by-4.0'; |
| gd_msha_injury | 8,683 | US Government work, public domain (17 USC 105): U.S. Department of Labor, Mine Safety and  |
| gd_feverous | 8,318 | CC BY-SA 3.0 / Wikipedia page licence terms (https://fever.ai/download/feverous/license.ht |
| gd_medqa_yn | 8,274 | MIT (https://github.com/jind11/MedQA/blob/27b02f66aac217933c9648a06f82e9f720377925/LICENSE |
| gd_sc101 | 8,261 | CC BY-SA 4.0 (https://github.com/mbforbes/social-chemistry-101/blob/116ead94d7e25dd8c02302 |
| gd_mfrc | 8,254 | CC BY 4.0 (https://huggingface.co/datasets/USC-MOLA-Lab/MFRC/blob/ddc21d2f03e156732fd1ba95 |
| gd_gen_msn_rules | 8,253 | n/a (program-generated; Claude-written templates and rules, labels by construction) |
| gd_redocred | 7,979 | MIT (https://github.com/tonytan48/Re-DocRED/blob/ccfb54f5ddf5836027c87badda10f6dfc56efaac/ |
| gd_medmcqa_subject | 7,977 | MIT (https://github.com/medmcqa/medmcqa/blob/c59ef14ca1990266c4107c7864b45a20fd93e5e0/LICE |
| gd_cards | 7,096 | Apache-2.0 (https://github.com/traviscoan/cards/blob/51a824c96b9ac5beb9efd6481567bc3a1e74d |
| gd_infotabs_nli | 7,024 | Apache-2.0 (LICENSE at root of github.com/infotabs/infotabs @ 34e7dc09; HF mirror table-be |
| gd_oiics_event | 6,872 | CC0 1.0 / US Government work (https://github.com/NASA-Tournament-Lab/CDC-NLP-Occ-Injury-Co |
| gd_tatqa | 6,740 | CC BY 4.0 (github.com/NExTplusplus/TAT-QA/blob/870accc41953dcde885aabeb963d94aabdc0fbc3/RE |
| gd_wiki_help_routing | 6,440 | CC BY-SA 4.0 / CC BY-SA 3.0 + GFDL (https://en.wikipedia.org/wiki/Wikipedia:Copyrights) |
| gd_totto_claims | 6,226 | CC BY-SA 3.0 (README of github.com/google-research-datasets/ToTTo @ 7b0ad5368ed523f75dc872 |
| gd_smcalflow_action | 6,220 | CC BY-SA 4.0 (README.md at commit bbd16fe69687b1052a7b5937ee7d20b641f2e642: 'The dataset i |
| gd_gen_msn_fault | 6,197 | n/a (program-generated; Claude-written templates and rules, labels by construction) |
| gd_qasc | 6,107 | CC BY 4.0 (huggingface.co/datasets/allenai/qasc/blob/a34ba204eb9a33b919c10cc08f4f1c8dae5ec |
| gd_edgar_10k_item | 6,070 | Apache-2.0 (license field of https://huggingface.co/datasets/eloukas/edgar-corpus/blob/7e9 |
| gd_sd311_routing | 5,799 | ODC-PDDL public domain dedication (dataset page https://data.sandiego.gov/datasets/get-it- |
| gd_medquad_qtype | 5,781 | CC BY 4.0 (https://github.com/abachaa/MedQuAD/blob/577bd37b96c02d1833b2c9eed2de9f96964e96c |
| gd_logicinference | 5,587 | Apache-2.0 (licence header in every generator file of google-research/google-research/logi |
| gd_storm_ef | 5,427 | US Government work, public domain (17 U.S.C. 105; NOAA/NWS Storm Data per NWS Directive 10 |
| gd_comve | 5,416 | CC BY-SA 4.0 (github.com/wangcunxiang/SemEval2020-Task4-Commonsense-Validation-and-Explana |
| gd_prm800k_steps | 5,317 | MIT (https://github.com/openai/prm800k/blob/7ecc794703b2877f63226f2477a49b34f9b25163/LICEN |
| gd_saferproducts_severity | 5,314 | US Government public data, public domain: data.gov record 'SaferProducts API' (https://cat |
| gd_wtq | 5,183 | CC BY-SA 4.0 (github.com/ppasupat/WikiTableQuestions/blob/7d455a5a707b96341ef72aff9428749d |
| gd_gen_msn_consent | 5,165 | n/a (program-generated; Claude-written templates and rules, labels by construction) |
| gd_opentdb | 5,139 | CC BY-SA 4.0 (official API page https://opentdb.com/api_config.php: 'All data provided by  |
| gd_finqa | 4,970 | MIT (github.com/czyssrs/FinQA/blob/0f16e2867befa6840783e58be38c9efb9229d742/LICENSE, 'Copy |
| gd_gen_nlr_heuristics | 4,930 | CC0 1.0 (Claude-written templates and program; no source data) |
| gd_winogrande | 4,734 | CC-BY (github.com/allenai/winogrande/blob/727e837f77521ef38bcc56df3b275c8da43f45af/README. |
| gd_dstc9_track1 | 4,631 | Apache-2.0 (https://github.com/alexa/alexa-with-dstc9-track1-dataset/blob/7ebb4c767b64826c |
| gd_clickbait17 | 4,461 | CC BY 4.0 (Zenodo record https://zenodo.org/records/5530410 metadata 'license: cc-by-4.0'; |
| gd_druglabel_section | 4,284 | CC0 1.0 / public domain (openFDA Terms of Service https://open.fda.gov/terms/: 'the conten |
| gd_babi_logic | 4,249 | CC BY 3.0 (tasks_1-20_v1-2/LICENSE.txt inside the official release: 'bAbI tasks data, Copy |
| gd_tathqa | 4,154 | Apache-2.0 (github.com/NExTplusplus/TAT-HQA/blob/8b821d89f0fbfeceea07e4f5faf46b33150fee07/ |
| gd_semtabfacts_sci | 4,048 | CC BY 4.0 (official task site https://sites.google.com/view/sem-tab-facts, Data: 'By downl |
| gd_casehold_yn | 4,039 | Apache-2.0 (https://github.com/reglab/casehold/blob/daea97cca16a4d203380f2cebed1a10ed8d42b |
| gd_uds_ordinal | 4,009 | CC BY-SA 4.0 (UDS annotations: https://github.com/decompositional-semantics-initiative/dec |
| gd_ncbi_disease | 3,880 | Public domain, US Government Work (NCBI PUBLIC DOMAIN NOTICE, https://www.ncbi.nlm.nih.gov |
| gd_taskmaster1 | 3,692 | CC BY 4.0 (https://github.com/google-research-datasets/Taskmaster/blob/d92cb6af3005f1dc09c |
| gd_east_asian_prejudice | 3,600 | CC BY 4.0 (Zenodo record 3816667 metadata license cc-by-4.0, https://zenodo.org/records/38 |
| gd_webred | 3,548 | CC BY 4.0 (https://github.com/google-research-datasets/WebRED/blob/3e5e6a43b468bcf48424e9f |
| gd_slur_usage | 3,477 | MIT (https://github.com/networkdynamics/slur-corpus/blob/f3cd926881b7c8e42fd984769ac596e29 |
| gd_edos_sexism | 3,433 | CC0 1.0 Universal (LICENSE file at the root of https://github.com/rewire-online/edos/blob/ |
| gd_vader_intensity | 3,389 | MIT (https://github.com/cjhutto/vaderSentiment/blob/44fc044cd877310ee8278a0eadf34bcd50d41d |
| gd_helpsteer3_pref | 3,369 | CC BY 4.0 (https://huggingface.co/datasets/nvidia/HelpSteer3/blob/f6d145777bcbde9613759634 |
| gd_star_next_action | 3,339 | MIT (LICENSE.txt in github.com/RasaHQ/STAR, 'Copyright (c) 2020 Rasa Technologies GmbH') |
| gd_hotpotqa_yesno | 3,274 | CC BY-SA 4.0 (https://hotpotqa.github.io/ : 'HotpotQA is distributed under a CC BY-SA 4.0  |
| gd_nrc_gfe | 3,152 | US Government work, public domain (17 U.S.C. 105; US Nuclear Regulatory Commission). NRC s |
| gd_faithdial | 2,963 | MIT (https://huggingface.co/datasets/McGill-NLP/FaithDial/blob/7a414e80725eac766f2602676dc |
| gd_naics_subsector | 2,904 | US Government work, public domain (17 USC 105): North American Industry Classification Sys |
| gd_nhtsa_complaints | 2,856 | US Government work, public domain (catalog.data.gov/dataset/nhtsas-office-of-defects-inves |
| gd_answer_equiv | 2,832 | Apache-2.0 (https://github.com/google-research-datasets/answer-equivalence-dataset/blob/50 |
| gd_helpsteer2_attr | 2,729 | CC BY 4.0 (https://huggingface.co/datasets/nvidia/HelpSteer2/blob/990b2711a36180dd19d9c94b |
| gd_multiwoz21_sysacts | 2,703 | MIT (https://github.com/budzianowski/multiwoz/blob/fe0c8e65cfcd8462bd33c86e35f21addc84ca82 |
| clinc150 | 2,651 | v13 clean replay |
| gd_hatemoji_build_v14 | 2,541 | CC BY 4.0 (https://github.com/HannahKirk/Hatemoji/blob/a626f63216158748d072e581efc00267031 |
| gd_taskmaster2 | 2,370 | CC BY 4.0 (https://github.com/google-research-datasets/Taskmaster/blob/d92cb6af3005f1dc09c |
| gd_taskmaster3 | 2,334 | CC BY 4.0 (https://github.com/google-research-datasets/Taskmaster/blob/d92cb6af3005f1dc09c |
| banking77 | 2,300 | v13 clean replay |
| gd_codah | 2,235 | ODC-BY 1.0 (github.com/Websail-NU/CODAH/blob/acf7ffa4041ade86c6f7dd2f92fb08c957350280/READ |
| gd_wands_product | 2,152 | MIT (https://github.com/wayfair/WANDS/blob/3b74dcf4ba29ab8ff3e6a50b5b09fc627cb882b5/LICENS |
| gd_aegis_prompts | 1,887 | CC BY 4.0 (first-party NVIDIA dataset cards: https://huggingface.co/datasets/nvidia/Aegis- |
| gd_ncvec_ham | 1,870 | Public domain (NCVEC Question Pool Committee release pages: https://www.ncvec.org/index.ph |
| gd_quartz | 1,798 | CC BY 4.0 (huggingface.co/datasets/allenai/quartz/blob/28c1dbb56caf81799296cb17892fa73402e |
| gd_csc_sarcasm | 1,739 | MIT (https://github.com/CoPsyN/CSC/blob/f11c92b8d54686f64cf1d92766cef07201efb986/LICENSE,  |
| gd_onestop_level | 1,731 | CC BY-SA 4.0 (https://github.com/nishkalavallabhi/OneStopEnglishCorpus/blob/37f8db3945cd2f |
| gd_conditionalqa | 1,713 | CC BY-SA 4.0 (official page https://haitian-sun.github.io/conditionalqa/ , 'CC BY-SA 4.0 L |
| massive | 1,703 | v13 clean replay |
| gd_onet_occupation | 1,629 | CC BY 4.0 (db_31_0_text/Read Me.txt; https://www.onetcenter.org/license_db.html). Source:  |
| gd_wnut17 | 1,616 | CC BY 4.0 (https://github.com/leondz/emerging_entities_17/blob/e52a2d2a71ac1a051ca2d532eef |
| gd_politeness_votes | 1,444 | CC BY 4.0 (ConvoKit docs https://convokit.cornell.edu/documentation/wiki_politeness.html,  |
| gd_prontoqa | 1,434 | Apache-2.0 (LICENSE at root of github.com/asaparov/prontoqa @ 0a6412b6) |
| gd_megaveridicality | 1,424 | CC BY-SA 4.0 (LICENSE file in the official release zip http://megaattitude.io/projects/meg |
| tb_label_nli | 1,288 | v13 clean replay |
| gd_ghc_hate | 1,273 | CC BY 4.0 (OSF node licence of https://osf.io/edua3/ 'CC-By Attribution 4.0 International' |
| gd_usb_factuality | 1,253 | Apache-2.0 (https://github.com/kukrishna/usb/blob/99f42d702e37e6e8e50cc8c5cdca32de72059f10 |
| gd_tabmcq | 1,188 | CC BY-SA 4.0 (README.txt inside TabMCQ_v_1.0.zip, section LICENCE; AWS Open Data Registry  |
| mnli3 | 1,090 | v13 clean replay |
| gd_climate_targets | 1,071 | CC BY 4.0 (dataset card https://huggingface.co/datasets/ClimatePolicyRadar/national-climat |
| gd_spiced | 1,002 | MIT (dataset card https://huggingface.co/datasets/copenlu/spiced/blob/832c456f4ce1012b301a |
| gd_mtbench_human | 970 | CC BY 4.0 (https://huggingface.co/datasets/lmsys/mt_bench_human_judgments/blob/f7d2896d2cc |
| gd_crowdtruth_mre | 963 | CC BY-SA 4.0 (Zenodo record https://zenodo.org/records/50676 metadata 'license: cc-by-sa-4 |
| gd_ragtruth_summary | 953 | MIT (https://github.com/ParticleMedia/RAGTruth/blob/c103204b9ce28d6bbad859304bf30de72b8ed8 |
| rte | 952 | v13 clean replay |
| gd_crossner | 950 | MIT (https://github.com/zliucr/CrossNER/blob/2e7ba2a7798c961e3f29fbc51252c5a8d40224bf/LICE |
| gd_ropes_sci | 941 | CC BY 4.0 (dataset card https://huggingface.co/datasets/allenai/ropes/blob/d59f1e2ee2b423d |
| gd_bbh_mistake | 905 | Apache-2.0 (https://github.com/WHGTyen/BIG-Bench-Mistake/blob/9b010ce17150b79411dc31659779 |
| qnli | 903 | v13 clean replay |
| wiki_stance_afd | 901 | v13 clean replay |
| boolq | 896 | v13 clean replay |
| dbpedia | 882 | v13 clean replay |
| judge_prm800k | 826 | v13 clean replay |
| condaqa | 788 | v13 clean replay |
| br_topv2 | 770 | v13 clean replay |
| br_wos46985 | 758 | v13 clean replay |
| amazon_polarity | 754 | v13 clean replay |
| br_mnds | 729 | v13 clean replay |
| toxic_conv | 729 | v13 clean replay |
| gd_check_covid | 713 | MIT (https://github.com/posuer/Check-COVID/blob/3ae70f8cac4df13a3ce56878e20d8e76790e422d/L |
| br_abcd | 707 | v13 clean replay |
| br_congress_policy | 699 | v13 clean replay |
| br_infotabs | 689 | v13 clean replay |
| proofwriter | 687 | v13 clean replay |
| br_emobank | 671 | v13 clean replay |
| br_cfpb | 668 | v13 clean replay |
| mnli | 661 | v13 clean replay |
| br_star | 642 | v13 clean replay |
| gd_mediqa_qa | 639 | CC BY 4.0 (https://github.com/abachaa/MEDIQA2019/blob/32311a139b583a9ccec133b3f8a21873d4ff |
| mrpc | 632 | v13 clean replay |
| br_edos | 624 | v13 clean replay |
| br_newsmtsc | 607 | v13 clean replay |
| br_newsgroups20 | 591 | v13 clean replay |
| fld | 574 | v13 clean replay |
| gd_biored | 539 | Public domain, US Government Work (NCBI/NLM PUBLIC DOMAIN NOTICE in https://ftp.ncbi.nlm.n |
| yahoo | 538 | v13 clean replay |
| br_xed_en | 499 | v13 clean replay |
| br_casino | 489 | v13 clean replay |
| br_politeness_wiki | 488 | v13 clean replay |
| judge_mathderiv | 479 | v13 clean replay |
| csqa | 478 | v13 clean replay |
| br_claimbuster | 474 | v13 clean replay |
| br_ghc | 472 | v13 clean replay |
| judge_helpsteer2 | 461 | v13 clean replay |
| planted_a | 448 | v13 clean replay |
| std_evidence | 444 | v13 clean replay |
| gd_clickbait16 | 444 | CC BY 4.0 (Zenodo record https://zenodo.org/records/3251557 metadata 'license: cc-by-4.0'; |
| planted_b | 442 | v13 clean replay |
| logiqa2 | 441 | v13 clean replay |
| std_trademark | 440 | v13 clean replay |
| arc | 414 | v13 clean replay |
| pg_numeric | 404 | v13 clean replay |
| br_convabuse | 397 | v13 clean replay |
| pg_multihop | 396 | v13 clean replay |
| pg_evidence | 395 | v13 clean replay |
| br_mams_acsa | 389 | v13 clean replay |
| pg_routing | 378 | v13 clean replay |
| std_hate | 378 | v13 clean replay |
| pg_temporal | 375 | v13 clean replay |
| yelp5 | 373 | v13 clean replay |
| pg_policy | 371 | v13 clean replay |
| pg_conflict | 369 | v13 clean replay |
| civil_comments | 364 | v13 clean replay |
| br_hatemoji_build | 362 | v13 clean replay |
| br_fm2 | 357 | v13 clean replay |
| gd_misogyny_reddit | 328 | MIT (https://github.com/ellamguest/online-misogyny-eacl2021/blob/b3c04567452ed92b160c36923 |
| yelp | 303 | v13 clean replay |
| hard_affect | 292 | v13 clean replay |
| hard_nli_b | 276 | v13 clean replay |
| std_hearsay | 276 | v13 clean replay |
| hard_policy_a | 274 | v13 clean replay |
| hard_scales | 272 | v13 clean replay |
| hard_evidence_claims_a | 268 | v13 clean replay |
| hard_policy_b | 256 | v13 clean replay |
| hard_evidence_a | 254 | v13 clean replay |
| hard_contracts | 252 | v13 clean replay |
| hard_evidence_b | 250 | v13 clean replay |
| copa | 243 | v13 clean replay |
| hard_clinical | 242 | v13 clean replay |
| hard_evidence_claims_b | 242 | v13 clean replay |
| hard_nli_a | 234 | v13 clean replay |
| binj_consistency | 226 | v13 clean replay |
| binj_adult | 213 | v13 clean replay |
| binj_intent | 212 | v13 clean replay |
| clothing | 211 | v13 clean replay |
| binj_offensive | 203 | v13 clean replay |
| br_steam_aspect | 200 | v13 clean replay |
| br_sarcasm_headlines | 191 | v13 clean replay |
| proc_temporal | 188 | v13 clean replay |
| proc_adversarial | 186 | v13 clean replay |
| proc_trap | 169 | v13 clean replay |
| proc_evidence | 165 | v13 clean replay |
| mnli_neutral | 164 | v13 clean replay |
| proc_routing | 157 | v13 clean replay |
| proc_tradeoff | 155 | v13 clean replay |
| proc_multihop | 152 | v13 clean replay |
| hard_codebook_c | 150 | v13 clean replay |
| proc_longpolicy | 150 | v13 clean replay |
| gd_meganegraising | 150 | CC BY-SA 4.0 (LICENSE file in the official release zip http://megaattitude.io/projects/meg |
| hard_reason_c | 137 | v13 clean replay |
| proc_rubric | 128 | v13 clean replay |
| hard_policy_c | 127 | v13 clean replay |
| hard_nli_c | 126 | v13 clean replay |
| hard_intent_c | 114 | v13 clean replay |
| musr_murder_mysteries | 111 | v13 clean replay |
| hard_affect_c | 109 | v13 clean replay |
| musr_object_placements | 96 | v13 clean replay |
| musr_team_allocation | 91 | v13 clean replay |

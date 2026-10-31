# Replay pool map (A46)

Draw: replay_sample.py unchanged, seed 20261013, r1 = 75,000, r2 = 150,000, margin 10% (--dry-run --r1 75000 --r2 150000 --margin 0.1 (SEED patched to 20261013 in-process; replay_sample.py unchanged)).

| | human | program | claude |
|---|---|---|---|
| eligible rows (before the old slice) | 275,537 | 142,387 | 0 |
| eligible rows (after the old slice) | 273,704 | 141,055 | 0 |
| rows in the draw | 58,066 | 24,511 | 0 |

Eligible human rows above 40,000: True (A46 size fallback applies).
Screening population (human rows of the draw, minus 4996 pool_drops_r1 units): 53,972 rows in 90 sources.

| source | origin | eligible | draw | screened | answer format | evidence |
|---|---|---|---|---|---|---|
| gd_uscg_mariner | human | 8,750 | 1,462 | 1,442 | yes/no 2,516 + choice 6,294 | real licensing-exam questions keyed by the USCG (Rules of the Road incl. INLAND/INTERNATIONAL scope, deck safe; builder build_uscg_mariner.py,fetch_uscg_mariner.py; raw yes |
| gd_drugprot | human | 8,738 | 1,460 | 1,437 | yes/no 2,667 + choice 6,127 | DrugProt training set (PubMed abstracts, expert chemical/gene mentions and relations). One row per sentence: c; builder build_drugprot.py; raw yes |
| gd_msha_injury | human | 8,628 | 1,447 | 1,445 | yes/no 2,500 + choice 6,183 | MSHA Part 50 accident/injury/illness reports 2000-2021 (operator narratives, MSHA-coded fields); each report u; builder build_msha_injury.py; raw yes |
| gd_feverous | human | 8,278 | 1,405 | 1,277 | yes/no 8,318 | Claim vs Wikipedia evidence mixing table cells/infobox rows and sentences. Two questions: 'support?' (NEI and ; builder build_feverous.py,feverous_fetch.py; raw yes |
| gd_medqa_yn | human | 8,238 | 1,401 | 1,136 | yes/no 8,274 | Clinical-vignette answer verification: vignette + all five lettered choices + a proposed choice; keyed single ; builder build_medqa_yn.py; raw yes |
| gd_sc101 | human | 8,226 | 1,400 | 1,382 | yes/no 8,261 | train split only; AITA area dropped (Scruples-derived); RoTs/actions matching Moral Stories norms dropped; acc; builder build_sc101.py; raw yes |
| gd_medmcqa_subject | human | 7,927 | 1,364 | 1,348 | yes/no 2,426 + choice 5,551 | MedMCQA train parquet only; 20-way subject of an exam question (question+4 options shown, explanation never sh; builder build_medmcqa_subject.py; raw yes |
| gd_cards | human | 7,066 | 1,258 | 1,225 | yes/no 7,096 | Climate contrarian-claim detection at the super-claim level (5 yes/no questions with per-question definitions ; builder build_v12_cards.py,build_cards.py; raw yes |
| gd_infotabs_nli | human | 6,988 | 1,249 | 1,203 | yes/no 4,145 + choice 2,879 | Human hypotheses over Wikipedia infoboxes (table reasoning: dates, ages, counts, roles). Excludes the 600 rows; builder build_infotabs_nli.py; raw yes |
| gd_oiics_event | human | 6,832 | 1,229 | 1,228 | yes/no 2,073 + choice 4,799 | NEISS-Work ED narratives 2012-2017 coded by NIOSH; every narrative of the 2019 CDC/NASA TopCoder competition t; builder build_oiics_event.py; raw yes |
| gd_tatqa | human | 6,710 | 1,214 | 1,127 | yes/no 6,740 | Answer verification over real annual-report tables+text. Yes rows = human gold answer; no rows = program-built; builder build_tatqa.py; raw yes |
| gd_wiki_help_routing | human | 6,392 | 1,173 | 1,111 | yes/no 1,990 + choice 4,450 | Opening post (heading + first message; signatures, diffs, refs, templates stripped) of threads from 2008-2021 ; builder build_wiki_help_routing.py; raw yes |
| gd_totto_claims | human | 6,194 | 1,148 | 1,089 | yes/no 6,226 | Claim verification on Wikipedia tables. Supported = annotator-revised ToTTo sentence; contradicted = same sent; builder build_totto.py; raw yes |
| gd_smcalflow_action | human | 6,178 | 1,146 | 1,074 | yes/no 1,847 + choice 4,373 | 29-way (after review) 'how should the calendar assistant handle the latest user turn': create/change/delete ev; builder build_smcalflow_action.py; raw yes |
| gd_sd311_routing | human | 5,755 | 1,089 | 1,084 | yes/no 1,762 + choice 4,037 | Two routing questions over residents' own report text (Mobile/Web/Phone/Email only, 2020-2021): q=service, 25-; builder build_sd311_routing.py; raw yes |
| gd_medquad_qtype | human | 5,744 | 1,088 | 1,033 | yes/no 1,734 + choice 4,047 | MedQuAD (no split) collections 1-9 only (10-12 have no answers); 13-way: which consumer-health question an NIH; builder build_medquad_qtype.py; raw yes |
| gd_comve | human | 5,389 | 1,041 | 1,036 | yes/no 5,419 | Sense-making: 8000 ComVE minimal pairs ('of these two statements, does Statement N go against common sense?', ; builder build_comve.py; raw yes |
| gd_storm_ef | human | 5,380 | 1,040 | 1,035 | yes/no 1,630 + choice 3,797 | NWS damage-survey narratives of single-segment US tornadoes 2007-2024; decide the official EF rating (EFU = no; builder build_storm_ef.py; raw yes |
| gd_prm800k_steps | human | 5,290 | 1,028 | 842 | yes/no 5,317; 174 rows carry human vote shares (meta.teacher) | Step-level verification of GPT-4-sampled MATH solutions with HUMAN step ratings (+1/0/-1, phase-2 labeler inst; builder build_prm800k_steps.py; raw yes |
| gd_saferproducts_severity | human | 5,278 | 1,027 | 974 | yes/no 1,609 + choice 3,705 | Consumer product incident reports (2011-2024) -> the submitter's own severity level for the primary victim (no; builder build_saferproducts_severity.py; raw yes |
| gd_wtq | human | 5,158 | 1,010 | 902 | yes/no 5,183 | Answer verification on Wikipedia tables. Yes rows = crowd answer agreed by >=2 workers; no rows = another same; builder build_wtq.py; raw yes |
| gd_opentdb | human | 5,104 | 1,002 | 965 | yes/no 1,528 + choice 3,611 | human-written, moderator-verified trivia over 24 categories (general knowledge, science, geography, history, a; builder build_opentdb.py,fetch_opentdb.py; raw yes |
| gd_winogrande | human | 4,710 | 948 | 948 | yes/no 4,734 | Twin-sentence coreference (commonsense). Yes/no 'does the blank stand for X', both twins asked about the same ; builder build_winogrande.py; raw yes |
| gd_dstc9_track1 | human | 4,605 | 933 | 788 | yes/no 4,631 | kst labels by construction (crowd-inserted knowledge-seeking turns vs original MultiWOZ turns); parking/wifi t; builder build_dstc9_track1.py; raw yes |
| gd_clickbait17 | human | 4,438 | 909 | 890 | yes/no 4,461; 4,136 rows carry human vote shares (meta.teacher) | Soft = share of the 5 MTurk annotators rating the post considerably/heavily clickbaiting (>= 0.66 on the 0/0.3; builder build_clickbait17.py; raw yes |
| gd_druglabel_section | human | 4,255 | 883 | 755 | yes/no 1,228 + choice 3,056 | openFDA drug-label partition 1/14 only; Rx labels effective before 2022; passage = 1-4 sentences inside a sect; builder build_druglabel_section.py; raw yes |
| gd_tathqa | human | 4,133 | 865 | 781 | yes/no 4,154 | Hypothetical ('what if') questions over annual-report tables. Yes rows = human hypothetical answer (derivation; builder build_tathqa.py; raw yes |
| gd_semtabfacts_sci | human | 4,025 | 849 | 835 | yes/no 4,048 | Crowd-written statements about tables from CC BY scientific articles, labels doubly verified; table rendered a; builder build_semtabfacts.py; raw yes |
| gd_casehold_yn | human | 4,018 | 848 | 819 | yes/no 4,039 | CaseHOLD train.csv only; yes/no holding verification (yes=true parenthetical, no=least-similar wrong candidate; builder build_casehold.py; raw yes |
| gd_uds_ordinal | human | 3,983 | 844 | 830 | yes/no 1,179 + choice 2,830; 3,689 rows carry human vote shares (meta.teacher) | UD EWT train web sentences with one marked event: UDS-Time duration class (3+ raters, soft shares, gold = plur; builder build_uds_ordinal.py; raw yes |
| gd_ncbi_disease | human | 3,852 | 823 | 822 | yes/no 1,179 + choice 2,701 | NCBI Disease Corpus train set (PubMed titles/abstracts, 14 expert annotators). Mention-category typing: one di; builder build_ncbi_disease.py; raw yes |
| gd_taskmaster1 | human | 3,669 | 797 | 736 | yes/no 3,692 | Only spans where >=2 crowd annotations agree exactly. status: agreed .reject + unavailability wording vs agree; builder build_taskmaster1.py; raw yes |
| gd_east_asian_prejudice | human | 3,579 | 782 | 772 | yes/no 2,344 + choice 1,256; 3,321 rows carry human vote shares (meta.teacher) | Vidgen et al. 2020 COVID East Asian prejudice tweets (text.clean as annotated); expert label kept only when an; builder build_east_asian_prejudice.py; raw yes |
| gd_webred | human | 3,518 | 773 | 734 | yes/no 1,048 + choice 2,500 | WebRED 2+1 (web sentences, 2-3 human raters per sentence x candidate relation; the WebRED-5 eval set is never ; builder build_webred.py; raw yes |
| gd_slur_usage | human | 3,453 | 763 | 733 | yes/no 2,285 + choice 1,192 | Kurrek et al. slur corpus (Reddit), coder-agreed rows only; derogatory-use yes/no (no = mentions/quotes/counte; builder build_slur_usage.py; raw yes |
| gd_edos_sexism | human | 3,413 | 756 | 741 | yes/no 2,750 + choice 683; 3,175 rows carry human vote shares (meta.teacher) | EDOS train split, gold == annotator majority only (expert overrides dropped); sexist yes/no with 35% near-miss; builder build_edos_sexism.py; raw yes |
| gd_vader_intensity | human | 3,359 | 749 | 734 | yes/no 1,001 + choice 2,388; 3,114 rows carry human vote shares (meta.teacher) | Tweets and NYT opinion sentences with >= 20 raters each (-4..+4); per-rater ratings grouped into 5 levels, sof; builder build_vader_intensity.py; raw yes |
| gd_star_next_action | human | 3,311 | 740 | 640 | yes/no 943 + choice 2,396 | Next-action decision for a flow-chart support assistant (16 transactional tasks, 16 option sets of 9-19 action; builder build_star_next_action.py; raw yes |
| gd_hotpotqa_yesno | human | 3,256 | 732 | 581 | yes/no 3,274 | Native human yes/no multi-hop comparison questions answered from two Wikipedia paragraphs (evidence shown); 40; builder build_hotpotqa_yesno.py; raw yes |
| gd_nrc_gfe | human | 3,121 | 711 | 707 | yes/no 943 + choice 2,209 | real reactor-operator licensing exam questions (components, reactor theory, thermodynamics) keyed by the NRC; ; builder build_nrc_gfe.py,fetch_nrc_gfe.py; raw yes |
| gd_naics_subsector | human | 2,875 | 670 | 668 | yes/no 856 + choice 2,048 | 2022 NAICS index entries (activity/product descriptions) -> 3-digit subsector by construction; kept only when ; builder build_naics_subsector.py; raw yes |
| gd_nhtsa_complaints | human | 2,838 | 665 | 641 | yes/no 2,856 | Labels = complaint form CRASH/FIRE/INJURED fields; yes rows need an unhedged event mention, no rows need all m; builder build_nhtsa_complaints.py; raw yes |
| gd_answer_equiv | human | 2,812 | 661 | 482 | yes/no 2,832 | Answer-equivalence judging with HUMAN ratings: can a model-predicted SQuAD answer replace the reference (asymm; builder build_answer_equiv.py; raw yes |
| gd_multiwoz21_sysacts | human | 2,687 | 640 | 545 | yes/no 2,703 | Human crowd system dialogue acts only (MultiWOZ 2.2 T5-assisted acts and heuristic user acts not used). Bookin; builder build_multiwoz21_sysacts.py; raw yes |
| gd_hatemoji_build_v14 | human | 2,526 | 613 | 609 | yes/no 2,002 + choice 539 | HatemojiBuild train.csv; human adversarial emoji hate with minimal human perturbations kept as linked contrast; builder build_hatemoji_build_v14.py; raw yes |
| gd_taskmaster2 | human | 2,356 | 583 | 504 | yes/no 2,370 | Single annotation layer, so guards: span on word boundaries, same text never carries another role anywhere in ; builder build_taskmaster2.py; raw yes |
| gd_taskmaster3 | human | 2,320 | 578 | 402 | yes/no 2,335 | yes = book_tickets API success; no = no book_tickets AND a no-purchase scenario (options unavailable, deferred; builder build_taskmaster3.py; raw yes |
| gd_codah | human | 2,216 | 559 | 544 | yes/no 1,601 + choice 634 | Adversarially human-authored commonsense sentence completion. 2000 yes/no 'is (X) the most sensible of the lis; builder build_codah.py; raw yes |
| gd_wands_product | human | 2,128 | 544 | 536 | yes/no 654 + choice 1,498 | Product catalogue only (never the search queries/relevance judgements); state = product name + description (<=; builder build_wands_product.py; raw yes |
| gd_ncvec_ham | human | 1,844 | 491 | 482 | yes/no 552 + choice 1,318 | official licence-exam question banks (rules, operating practice, electronics, RF safety) written and keyed by ; builder build_ncvec_ham.py; raw yes |
| gd_csc_sarcasm | human | 1,727 | 470 | 426 | yes/no 1,739; 1,597 rows carry human vote shares (meta.teacher) | Soft = share of the 4-6 third-party evaluators rating the reply 4-6 on the 1-6 sarcasm scale (speaker self-rat; builder build_csc_sarcasm.py; raw yes |
| gd_onestop_level | human | 1,715 | 468 | 446 | yes/no 467 + choice 1,264 | Passages (70-220 words) from teacher-rewritten Guardian articles at elementary / intermediate / advanced level; builder build_onestop_level.py; raw yes |
| gd_conditionalqa | human | 1,690 | 463 | 300 | yes/no 520 + choice 1,193 | Human questions over full gov.uk guidance pages; conditional answers (requirements the scenario does not settl; builder build_conditionalqa.py; raw yes |
| gd_onet_occupation | human | 1,617 | 448 | 430 | yes/no 1,198 + choice 431 | O*NET 31.0 task statements (CC BY 4.0, US DOL/ETA); yes/no contrastive pairs (duties of the named occupation v; builder build_onet_occupation.py; raw yes |
| gd_wnut17 | human | 1,598 | 445 | 438 | yes/no 472 + choice 1,144 | WNUT17 train tweets (crowd annotation + expert adjudication). Entity typing: one mention per tweet marked <e>,; builder build_wnut17.py; raw yes |
| gd_politeness_votes | human | 1,433 | 413 | 320 | yes/no 1,444; 1,345 rows carry human vote shares (meta.teacher) | Soft = share of the 5 MTurk raters on the impolite (1-12) or polite (14-25) side of the 1-25 slider (13 = neut; builder build_politeness_votes.py; raw yes |
| gd_megaveridicality | human | 1,414 | 409 | 409 | yes/no 1,424; 1,293 rows carry human vote shares (meta.teacher) | Veridicality/factivity under negation with 10 native-speaker votes per sentence (yes / maybe or maybe not / no; builder build_megaveridicality.py; raw yes |
| gd_ghc_hate | human | 1,262 | 378 | 367 | yes/no 977 + choice 296; 1,176 rows carry human vote shares (meta.teacher) | Gab Hate Corpus train; HD/VO/CV yes/no with near-miss negatives (VO-not-HD, HD-not-VO, HD-not-CV) + 8-way targ; builder build_ghc_hate.py; raw yes |
| gd_usb_factuality | human | 1,244 | 373 | 328 | yes/no 1,253 | Summary-sentence factual consistency against evidence sentences, HUMAN labels: Wikipedia lead sentences vs the; builder build_usb_factuality.py; raw yes |
| gd_tabmcq | human | 1,178 | 360 | 315 | yes/no 1,188 | Science-facts tables (manual REGENTS/MONARCH tables) + crowd MCQs recast as answer verification. Key must sit ; builder build_tabmcq.py; raw yes |
| gd_crowdtruth_mre | human | 954 | 310 | 303 | yes/no 963; 892 rows carry human vote shares (meta.teacher) | Soft = share of ~15 CrowdFlower workers ticking the relation (contradictory NONE+X and 5+-relation judgements ; builder build_crowdtruth_mre.py; raw yes |
| gd_ragtruth_summary | human | 946 | 308 | 241 | yes/no 953 | News-summary faithfulness with HUMAN hallucination-span labels (conflict or baseless, evident or subtle; unsup; builder build_ragtruth_summary.py; raw yes |
| gd_crossner | human | 938 | 306 | 272 | yes/no 288 + choice 662 | CrossNER train (Wikipedia; DBpedia pre-tags corrected by expert annotators). Fine-grained entity typing, one m; builder build_crossner.py; raw yes |
| judge_prm800k | human | 816 | 278 | 164 | yes/no 826 | ; builder build_prm800k_steps.py; raw no |
| br_topv2 | human | 762 | 266 | 245 | yes/no 194 + choice 576 | TOPv2 (Task Oriented Parsing v2, Chen et al. 2020); builder legacy (see POOL_MAP.json); raw no |
| br_wos46985 | human | 752 | 263 | 252 | yes/no 220 + choice 538 | Web of Science Dataset WOS-46985 (HDLTex, Kowsari et al. 201; builder legacy (see POOL_MAP.json); raw no |
| br_mnds | human | 723 | 256 | 205 | yes/no 190 + choice 539 | MN-DS (Zenodo 7394851, MN-DS-news-classification.csv; HF mir; builder legacy (see POOL_MAP.json); raw no |
| gd_check_covid | human | 706 | 252 | 239 | yes/no 713 | Expert-annotated COVID-19 news claims vs sentence-level evidence from peer-reviewed abstracts; SUPPORT/REFUTE ; builder build_check_covid.py; raw yes |
| br_abcd | human | 697 | 249 | 218 | yes/no 180 + choice 527 | ABCD (Action-Based Conversations Dataset), asappresearch/abc; builder gen_policy_exceptions.py,dx_def_literal.py; raw no |
| br_infotabs | human | 683 | 246 | 224 | yes/no 196 + choice 493 | table-benchmark/infotabs; builder build_infotabs_nli.py; raw no |
| br_emobank | human | 665 | 242 | 212 | yes/no 178 + choice 493; 671 rows carry human vote shares (meta.teacher) | JULIELab/EmoBank; builder legacy (see POOL_MAP.json); raw no |
| br_cfpb | human | 662 | 240 | 204 | yes/no 142 + choice 526 | BEE-spoke-data/consumer-finance-complaints; builder legacy (see POOL_MAP.json); raw no |
| br_star | human | 634 | 234 | 148 | yes/no 186 + choice 456 | RasaHQ/STAR; builder build_star_next_action.py; raw no |
| gd_mediqa_qa | human | 633 | 233 | 176 | yes/no 639 | Answer-adequacy judging for consumer health questions: expert ReferenceScore 3-4 = yes, 1-2 = no (official map; builder build_mediqa_qa.py; raw yes |
| br_edos | human | 618 | 229 | 217 | yes/no 295 + choice 329; 621 rows carry human vote shares (meta.teacher) | rewire-online/edos (SemEval-2023 Task 10); builder build_edos_sexism.py; raw no |
| br_newsgroups20 | human | 584 | 219 | 178 | yes/no 138 + choice 453 | SetFit/20_newsgroups (20 Newsgroups by-date, sklearn headers; builder legacy (see POOL_MAP.json); raw no |
| gd_biored | human | 532 | 207 | 182 | yes/no 164 + choice 375 | BioRED train (400 PubMed abstracts, NCBI curators). One row per abstract: all mentions of the two concepts mar; builder build_biored.py; raw yes |
| br_xed_en | human | 494 | 196 | 179 | yes/no 161 + choice 338 | Helsinki-NLP/XED (English annotated + neutral); builder legacy (see POOL_MAP.json); raw no |
| br_casino | human | 484 | 193 | 166 | yes/no 171 + choice 318 | CaSiNo (Campsite Negotiation Dialogues) strategy annotations; builder pe_domains.py,nn_lexicon.py; raw no |
| br_politeness_wiki | human | 483 | 193 | 133 | yes/no 120 + choice 368; 488 rows carry human vote shares (meta.teacher) | ConvoKit wikipedia-politeness-corpus (Stanford Politeness Co; builder build_politeness_votes.py; raw no |
| br_claimbuster | human | 467 | 188 | 181 | yes/no 106 + choice 368 | ClaimBuster (Zenodo 3609356) crowdsourced.csv; builder nn_lexicon.py,v3_nested_negation.py; raw no |
| br_ghc | human | 467 | 188 | 181 | yes/no 331 + choice 141; 472 rows carry human vote shares (meta.teacher) | Gab Hate Corpus (OSF edua3); builder build_ghc_hate.py; raw no |
| gd_clickbait16 | human | 440 | 181 | 178 | yes/no 444; 406 rows carry human vote shares (meta.teacher) | Soft = share of the 3 annotators rating the tweet medium/strong clickbait (README discretisation). Only unanim; builder build_clickbait16.py; raw yes |
| br_convabuse | human | 391 | 167 | 155 | yes/no 163 + choice 234; 397 rows carry human vote shares (meta.teacher) | ConvAbuse (Cercas Curry, Abercrombie & Rieser, EMNLP 2021); builder legacy (see POOL_MAP.json); raw no |
| br_mams_acsa | human | 383 | 164 | 160 | yes/no 200 + choice 189 | siat-nlp/MAMS-for-ABSA (MAMS-ACSA); builder legacy (see POOL_MAP.json); raw no |
| br_hatemoji_build | human | 356 | 157 | 154 | yes/no 205 + choice 157 | HatemojiBuild (github.com/HannahKirk/Hatemoji, HatemojiBuild; builder build_hatemoji_build_v14.py; raw no |
| br_fm2 | human | 353 | 156 | 121 | yes/no 357 | tasksource/fool-me-twice; builder legacy (see POOL_MAP.json); raw no |
| gd_misogyny_reddit | human | 324 | 146 | 132 | yes/no 328; 306 rows carry human vote shares (meta.teacher) | Guest et al. EACL 2021 expert-facilitated misogyny labels, train split, text-only entries with parent context;; builder build_misogyny_reddit.py; raw yes |
| br_sarcasm_headlines | human | 189 | 100 | 80 | yes/no 191 | raquiba/Sarcasm_News_Headline; builder legacy (see POOL_MAP.json); raw no |
| gd_meganegraising | human | 147 | 82 | 39 | yes/no 150; 140 rows carry human vote shares (meta.teacher) | Neg-raising (negation scope) judgements: 'If someone says <not V that S>, do they mean <V that not S>?'. Soft ; builder build_meganegraising.py; raw yes |
| gd_gen_tables | program | 11,498 | 1,769 | 0 | yes/no 9,161 + choice 2,444 | Claims about generated realistic tables (22 domains, 7 text formats: markdown, header-row pipe, CSV, TSV, fixe; builder gen_tables.py; raw yes |
| gd_gen_logic_negation | program | 11,479 | 1,767 | 0 | yes/no 11,526 | 45 Claude-written schemas, 313 schema:variant surface templates, hundreds of realistic frames (HR, refunds, sh; builder gen_logic_negation.py; raw yes |
| gd_gen_numeric_dates | program | 11,431 | 1,762 | 0 | yes/no 8,869 + choice 2,662 | program-generated policy excerpt + scenario decisions hinging on numbers, units, dates and time (47 schemas: a; builder gen_numeric_dates.py; raw yes |
| gd_gen_evidence_conflict | program | 11,419 | 1,761 | 0 | yes/no 8,216 + choice 3,320 | Multi-source evidence reconciliation: 3-11 dated documents (notices, records, emails, call notes, texts, posts; builder gen_evidence_conflict.py; raw yes |
| gd_gen_ranking | program | 11,399 | 1,759 | 0 | yes/no 4,125 + choice 7,419 | Best-of-N decisions computed exactly from stated attributes and rules. 6300 rows: 24 realistic selection domai; builder gen_ranking.py; raw yes |
| gd_gen_policy_exceptions | program | 11,353 | 1,754 | 0 | yes/no 8,957 + choice 2,506 | Program-generated policy application over 10 domains (returns, ticket refunds, home insurance, HR leave, schoo; builder gen_policy_exceptions.py; raw yes |
| gd_gen_routing | program | 11,346 | 1,753 | 0 | yes/no 4,258 + choice 7,238 | Program-generated ticket/request routing under an explicit routing policy: 15 domains (online retailer custome; builder gen_routing.py; raw yes |
| gd_gen_constraints | program | 11,279 | 1,745 | 0 | yes/no 4,237 + choice 7,189 | 29 real-world selection domains (shipping, meeting rooms, calendar slots with time zones, health plans, flight; builder gen_constraints.py; raw yes |
| gd_boardgameqa | program | 9,485 | 1,548 | 0 | yes/no 2,779 + choice 6,771 | Program-generated defeasible reasoning with exact labels: conflicting rules resolved by preferences (exception; builder build_boardgameqa.py; raw yes |
| gd_gen_msn_rules | program | 8,183 | 1,395 | 0 | yes/no 8,253 | program-generated community/shared-space rules with conditions and exceptions; 25 schemas; every item has a fa; builder gen_msn_rules.py; raw yes |
| gd_gen_msn_fault | program | 6,139 | 1,140 | 0 | yes/no 6,197 | program-generated multi-party agreements (10 schemas); the question asks about one named person; both parties ; builder gen_msn_fault.py; raw yes |
| gd_logicinference | program | 5,552 | 1,063 | 0 | yes/no 3,033 + choice 2,554 | Exact-label propositional + monadic first-order deduction in English (modus tollens, disjunctive syllogism, bi; builder build_logicinference.py; raw yes |
| gd_gen_msn_consent | program | 5,111 | 1,003 | 0 | yes/no 5,161 | program-generated consent/permission scope: owner vs non-owner grants, silence and 'maybe' are not consent, ti; builder gen_msn_consent.py; raw yes |
| gd_gen_nlr_heuristics | program | 4,905 | 974 | 0 | yes/no 4,930 | 34 Claude-written templates (lexical overlap, subsequence, constituent, factive vs non-factive, implicatives, ; builder gen_nlr_heuristics.py; raw yes |
| gd_babi_logic | program | 4,222 | 878 | 0 | yes/no 2,606 + choice 1,643 | Exact-label toy reasoning: negation ('no longer', 'not in'), indefinite knowledge -> maybe, state tracking (mo; builder build_babi_logic.py; raw yes |
| gd_prontoqa | program | 1,423 | 411 | 0 | yes/no 1,434 | Exact-label syllogistic chains with negated properties and distractor concepts; one third uses a counterfactua; builder build_prontoqa.py; raw yes |
| gd_gen2_json_fields | program | 658 | 239 | 0 | yes/no 380 + choice 290 | Gap-fill generator (29 Sep audit: structured-record decisions and field extraction). (a) 400 yes/no rows: deci; builder gen2_json_fields.py; raw yes |
| judge_mathderiv | program | 473 | 190 | 0 | yes/no 479 | ; builder build_judge.py; raw no |
| gd_gen2_probability | program | 468 | 189 | 0 | yes/no 332 + choice 146; 238 rows carry human vote shares (meta.teacher) | Gap-fill (29 Sep audit): probability and likelihood decisions with exact labels. 21 schemas / 83 Claude-writte; builder gen2_probability.py; raw yes |
| pg_numeric | program | 400 | 169 | 0 | yes/no 83 + choice 321 | ; builder rc_numeric.py; raw no |
| pg_multihop | program | 392 | 167 | 0 | yes/no 102 + choice 294 | ; builder build_pg.py; raw no |
| pg_evidence | program | 391 | 167 | 0 | yes/no 69 + choice 326 | ; builder build_v12_proc_evidence.py,gen_evidence_conflict.py; raw no |
| pg_routing | program | 374 | 161 | 0 | yes/no 76 + choice 302 | ; builder build_v12_proc_routing.py,gen_routing.py; raw no |
| pg_temporal | program | 371 | 161 | 0 | yes/no 80 + choice 295 | ; builder build_pg.py,build_train_v07.py; raw no |
| pg_policy | program | 367 | 159 | 0 | yes/no 89 + choice 282 | ; builder build_hard_policy_b.py,build_v12_policy_c.py; raw no |
| pg_conflict | program | 365 | 158 | 0 | yes/no 68 + choice 301 | ; builder gen_evidence_conflict.py; raw no |
| gd_gen2_long_policy | program | 288 | 135 | 0 | yes/no 148 + choice 146 | Program-generated decisions over very long policy documents (8,000-16,000 characters): homeowners policy forms; builder gen2_long_policy.py; raw yes |
| gd_gen2_tool_selection | program | 284 | 134 | 0 | choice 290 | Program-generated tool / function selection: an assistant with a catalog of 5-10 tools (definitions state each; builder gen2_tool_selection.py; raw yes |

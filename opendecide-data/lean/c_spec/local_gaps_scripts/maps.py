"""Hand mapping of golden_train sources to Jev-Decision-Index task TYPES and to coarse domains (judgement from the
source's instructions/options; one primary type per source)."""

TYPE = {}


def put(t, names):
    for n in names.split():
        TYPE[n] = t


put("topic/domain classification", """gd_medmcqa_subject gd_edgar_10k_item gd_medquad_qtype gd_druglabel_section gd_naics_subsector
 gd_wands_product gd_onet_occupation gd_msha_injury gd_oiics_event dbpedia yahoo br_wos46985 br_mnds br_congress_policy
 br_newsgroups20 tb_label_nli br_claimbuster br_cfpb hard_contracts hard_codebook_c gd_nhtsa_complaints gd_clickbait16
 gd_clickbait17 gd_climate_targets""")
put("intent/routing", """gd_gen_routing gd_wiki_help_routing gd_sd311_routing clinc150 banking77 massive br_topv2 br_abcd br_star
 pg_routing proc_routing hard_intent_c br_casino""")
put("tools/function calling", "gd_gen2_tool_selection")
put("dialogue state/next action", """gd_smcalflow_action gd_star_next_action gd_taskmaster1 gd_taskmaster2 gd_taskmaster3
 gd_multiwoz21_sysacts gd_dstc9_track1""")
put("NLI/fact verification", """gd_gen_evidence_conflict gd_feverous gd_infotabs_nli br_infotabs gd_totto_claims gd_semtabfacts_sci
 gd_check_covid br_fm2 std_evidence mnli mnli3 mnli_neutral rte qnli mrpc gd_gen_nlr_heuristics gd_megaveridicality
 gd_meganegraising gd_spiced condaqa gd_gen_logic_negation hard_nli_a hard_nli_b hard_nli_c gd_cards hard_evidence_claims_a hard_evidence_claims_b""")
put("stance", "wiki_stance_afd")
put("sentiment/ABSA", """amazon_polarity yelp yelp5 clothing gd_vader_intensity br_newsmtsc br_mams_acsa br_steam_aspect""")
put("emotion", "br_emobank br_xed_en hard_affect hard_affect_c")
put("sarcasm/irony", "gd_csc_sarcasm br_sarcasm_headlines")
put("moderation/safety", """gd_east_asian_prejudice gd_slur_usage gd_edos_sexism gd_hatemoji_build_v14 gd_aegis_prompts gd_ghc_hate
 gd_misogyny_reddit toxic_conv civil_comments std_hate br_edos br_ghc br_hatemoji_build br_convabuse binj_adult binj_intent
 binj_offensive planted_a planted_b""")
put("commonsense", """gd_comve gd_winogrande gd_codah csqa copa gd_quartz gd_ropes_sci gd_qasc boolq gd_hotpotqa_yesno
 gd_politeness_votes br_politeness_wiki""")
put("knowledge MC (exams/trivia)", """gd_uscg_mariner gd_opentdb gd_nrc_gfe gd_ncvec_ham gd_medqa_yn arc gd_mediqa_qa gd_casehold_yn""")
put("logic/rule reasoning", """gd_boardgameqa gd_logicinference gd_prontoqa gd_babi_logic proofwriter fld logiqa2 musr_murder_mysteries
 musr_object_placements musr_team_allocation""")
put("policy/rule application", """gd_gen_policy_exceptions gd_gen_msn_rules gd_gen_msn_fault gd_gen_msn_consent gd_conditionalqa
 gd_gen2_long_policy pg_policy pg_conflict pg_temporal pg_multihop proc_temporal proc_adversarial proc_trap proc_evidence
 proc_tradeoff proc_multihop proc_longpolicy proc_rubric hard_policy_a hard_policy_b hard_policy_c hard_reason_c
 hard_evidence_a hard_evidence_b hard_clinical std_hearsay gd_gen_constraints gd_gen_ranking""")
put("table/numeric reasoning", """gd_gen_tables gd_tatqa gd_wtq gd_finqa gd_tathqa gd_tabmcq gd_gen_numeric_dates pg_numeric
 gd_gen2_json_fields""")
put("moral/social norms", "gd_sc101 gd_mfrc")
put("judge/verifier", """gd_prm800k_steps gd_helpsteer3_pref gd_helpsteer2_attr gd_faithdial gd_answer_equiv gd_usb_factuality
 gd_mtbench_human gd_ragtruth_summary gd_bbh_mistake judge_prm800k judge_mathderiv judge_helpsteer2 binj_consistency""")
put("relation/entity typing", """gd_drugprot gd_redocred gd_ncbi_disease gd_webred gd_wnut17 gd_crossner gd_biored gd_crowdtruth_mre""")
put("ordinal/score", """gd_storm_ef gd_saferproducts_severity gd_uds_ordinal gd_onestop_level hard_scales std_trademark""")
put("risk/forecast", "gd_gen2_probability pg_evidence")

DOM = {}


def dom(d, names):
    for n in names.split():
        DOM[n] = d


dom("medical/health", """gd_medmcqa_subject gd_medquad_qtype gd_druglabel_section gd_medqa_yn gd_mediqa_qa gd_drugprot gd_ncbi_disease
 gd_biored gd_crowdtruth_mre gd_check_covid hard_clinical""")
dom("finance/business filings", "gd_edgar_10k_item gd_finqa gd_tatqa gd_tathqa br_cfpb banking77 gd_naics_subsector")
dom("legal/regulatory", "gd_casehold_yn hard_contracts std_hearsay std_trademark hard_evidence_a hard_evidence_b gd_conditionalqa br_congress_policy")
dom("government safety/incident reports", """gd_msha_injury gd_oiics_event gd_storm_ef gd_saferproducts_severity gd_nhtsa_complaints gd_sd311_routing
 hard_codebook_c gd_uscg_mariner gd_nrc_gfe gd_ncvec_ham""")
dom("customer support/assistants", """clinc150 massive br_topv2 br_abcd br_star gd_smcalflow_action gd_star_next_action gd_taskmaster1
 gd_taskmaster2 gd_taskmaster3 gd_multiwoz21_sysacts gd_dstc9_track1 gd_gen2_tool_selection gd_wands_product""")
dom("social media/online comments", """gd_east_asian_prejudice gd_slur_usage gd_edos_sexism gd_hatemoji_build_v14 gd_ghc_hate gd_misogyny_reddit
 toxic_conv civil_comments std_hate br_edos br_ghc br_hatemoji_build gd_mfrc gd_clickbait16 gd_clickbait17 gd_csc_sarcasm
 br_sarcasm_headlines br_convabuse gd_politeness_votes br_politeness_wiki gd_wnut17 binj_adult binj_intent binj_offensive""")
dom("reviews", "amazon_polarity yelp yelp5 clothing br_mams_acsa br_steam_aspect gd_vader_intensity")
dom("news/politics", "br_newsmtsc br_mnds br_claimbuster br_newsgroups20 gd_ragtruth_summary dbpedia yahoo")
dom("science/climate", "gd_cards gd_climate_targets gd_semtabfacts_sci gd_spiced gd_ropes_sci gd_qasc gd_quartz br_wos46985 gd_crossner")
dom("encyclopedia/general knowledge", """gd_feverous gd_infotabs_nli br_infotabs gd_totto_claims gd_wtq gd_tabmcq gd_redocred gd_webred
 gd_hotpotqa_yesno boolq gd_opentdb wiki_stance_afd gd_wiki_help_routing arc csqa""")
dom("AI outputs (judging)", """gd_prm800k_steps gd_helpsteer3_pref gd_helpsteer2_attr gd_faithdial gd_answer_equiv gd_usb_factuality
 gd_mtbench_human gd_bbh_mistake judge_prm800k judge_mathderiv judge_helpsteer2 binj_consistency gd_aegis_prompts planted_a planted_b""")
dom("synthetic logic/puzzles", """gd_boardgameqa gd_logicinference gd_prontoqa gd_babi_logic proofwriter fld logiqa2 musr_murder_mysteries
 musr_object_placements musr_team_allocation gd_gen_nlr_heuristics gd_gen_logic_negation""")
dom("program-generated business/HR/ops scenarios", """gd_gen_tables gd_gen_ranking gd_gen_evidence_conflict gd_gen_numeric_dates gd_gen_routing
 gd_gen_policy_exceptions gd_gen_constraints gd_gen_msn_rules gd_gen_msn_fault gd_gen_msn_consent gd_gen2_json_fields
 gd_gen2_long_policy gd_gen2_probability pg_numeric pg_multihop pg_evidence pg_routing pg_temporal pg_policy pg_conflict
 proc_temporal proc_adversarial proc_trap proc_evidence proc_routing proc_tradeoff proc_multihop proc_longpolicy proc_rubric
 hard_policy_a hard_policy_b hard_policy_c hard_reason_c hard_scales hard_nli_a hard_nli_b hard_nli_c hard_evidence_claims_a
 hard_evidence_claims_b hard_intent_c hard_affect hard_affect_c""")
dom("everyday/commonsense", "gd_comve gd_winogrande gd_codah copa gd_sc101 br_casino br_emobank br_xed_en gd_megaveridicality gd_meganegraising gd_uds_ordinal")
dom("education/reading", "gd_onestop_level gd_onet_occupation")
dom("general NLI/paraphrase corpora", "mnli mnli3 mnli_neutral rte qnli mrpc condaqa std_evidence br_fm2 tb_label_nli")

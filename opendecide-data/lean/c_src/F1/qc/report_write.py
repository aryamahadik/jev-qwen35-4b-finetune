import json
L=lambda f: json.load(open('qc/'+f))
g5,g6,g7q,g7c,g8,g10c,g10q,g11,g12,g1518=[L(f) for f in ('g5.json','g6_qc_sample.json','g7_qc_sample.json','g7_candidates_r1.json','g8_candidates_r1.json','g10_candidates_r1.json','g10_qc_sample.json','g11_candidates_r1.json','g12.json','g15_g18.json')]
gates={
 'G5':{'pass':g5['pass'],'sample_n':600,'seed':5001,'agree':g5['agree_with_gold'],'clearly_wrong':0,'ambiguous':0,'file':'qc/g5.json'},
 'G6':{'pass':False,'file':'qc/g6_qc_sample.json','diag':'qc/g6_diag_qc_sample.json',
   'a_question':'pass','b_options':'pass','c_card_without_question':'pass',
   'd_metadata':{'yes_no_gbt':g6['yes_no']['d_metadata']['gbt'],'yes_no_chance':g6['yes_no']['d_metadata']['chance'],
                 'choice_gbt':g6['choice']['d_metadata']['gbt'],'choice_chance':g6['choice']['d_metadata']['chance_mean_1_over_k']},
   'driver':'sidecar X_role / option-role metadata (yes/no X_role-only 0.599; metadata without X_role 0.518)'},
 'G7':{'pass':False,'files':['qc/g7_qc_sample.json','qc/g7_candidates_r1.json'],
   'qc_sample':{'literal_fails':227,'card_null_fails':2,'choice_fails':2},'candidates_r1':{'literal_fails':507,'card_null_fails':3,'choice_fails':4},
   'top':'X_role=default yes-share 0.66 (card-null z 10.4 on candidates)'},
 'G8':{'pass':False,'file':'qc/g8_candidates_r1.json','grouped_by_card_predictable':g8['grouped_by_card']['predictable_share'],
   'grouped_yes_no':g8['grouped_by_card']['yes_no_share'],'instance_level_predictable':g8['instance_level']['predictable_share'],'rule':'< 0.10'},
 'G10':{'pass':False,'files':['qc/g10_candidates_r1.json','qc/g10_qc_sample.json'],'failed_candidates':g10c['failed'],'failed_qc_sample':g10q['failed']},
 'G11':{'pass':g11['pass'],'file':'qc/g11_candidates_r1.json','failed':g11['failed'],
   'detail':'2 cards (F1-C029, F1-C112) have 3 rows and 2-3 wordings; all other quota checks pass',
   'soft':g11['soft'],'compression_ratio':g11['compression_ratio_state'],'self_bleu4_approx':g11['self_bleu4_approx'],
   'vendi':g11['vendi_state_minilm_2000'],'golden_train_comparison':'not computable within allow-list'},
 'G12':{'pass':False,'file':'qc/g12.json','exact_dups':0,'structure_collisions':0,'minhash_pairs_outside_group':2,
   'note':'both pairs are same-card candidates_r1 vs qc_sample; 0 near-dups outside group inside the training pool (candidates_r1 + mixdev_S5); keep-one fix is trivial'},
 'G15':{'pass':g1518['G15'].get('pass'),'file':'qc/g15_g18.json','tok_max':1999,'rows_ge_2000':0,'units_gt3':0},
 'G18':{'pass':g1518['G18'].get('pass'),'file':'qc/g15_g18.json','ordinal_rows':0},
}
failed=[k for k,v in gates.items() if not v['pass']]
rep={'family':'F1','round':1,'checker':'independent C checker','files':['out/candidates_r1.jsonl','out/qc_sample.jsonl','out/mixdev_S5.jsonl'],
 'gates':gates,'failed_gates':failed,'pass':(not failed),
 'summary':'G5/G15/G18 pass. Shortcut gates fail: the asked outcome role (default outcome) predicts the yes/no label; known distribution misses (depth, amendments, option buckets, contrast share) remain.'}
json.dump(rep,open('qc/QC_REPORT.json','w'),indent=1); print(failed, rep['pass'])

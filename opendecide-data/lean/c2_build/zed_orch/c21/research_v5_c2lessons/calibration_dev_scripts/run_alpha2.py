import sys, json, math
sys.path.insert(0,'.')
import calib_dev_analysis as C
GEN=['dev','dev_nc','taskbank_dev','hard_dev','dev_negwords','dev_claims','pg_dev','devzs','devp_card']
def aurc(rows):
    confs,corr,_=C.stats(rows,1.0)
    idx=sorted(range(len(confs)),key=lambda i:-confs[i]); err=0; s=0
    for k,i in enumerate(idx,1):
        err+=1-corr[i]; s+=err/k
    return 100*s/len(idx)
print('model | gen: ECE@T1 ECE@Topt AURC | transfer: ECE@T1 ECE@Topt AURC')
for name,mf in [('C1','q35_4b_main500k_c2'),('final_a05','q35_4b_c2grid_final_a05'),('final_a07','q35_4b_c2grid_final_a07'),('final_a10','q35_4b_c2grid_final_a10'),('last3_a10','q35_4b_c2grid_last3_a10'),('earlylate_a10','q35_4b_c2grid_earlylate_a10')]:
    g=[]
    for d in GEN: g+=C.rows_for(f'preds_{d}',d,mf)
    t=C.rows_for('preds_c2_transfer_dev','c2_transfer_dev',mf)
    sg=C.summarize(g,'g'); st=C.summarize(t,'t')
    print(f"{name:14s} | {sg['ECE_eqmass10_T1']:.2f} {sg['ECE_eqmass10_at_Topt']:.2f} {aurc(g):.2f} | {st['ECE_eqmass10_T1']:.2f} {st['ECE_eqmass10_at_Topt']:.2f} {aurc(t):.2f}")

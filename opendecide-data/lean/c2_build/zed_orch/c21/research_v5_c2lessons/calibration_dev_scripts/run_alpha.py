import sys, json
sys.path.insert(0,'.')
import calib_dev_analysis as C
GEN=['dev','dev_nc','taskbank_dev','hard_dev','dev_negwords','dev_claims','pg_dev','devzs','devp_card']
def gen(mf):
    allr=[]
    for d in GEN:
        allr+=C.rows_for(f'preds_{d}',d,mf)
    return allr
cands=[('C1','q35_4b_main500k_c2')]
for fam in ('final','last3','earlylate'):
    for a in ('05','06','07','08','09','10'):
        cands.append((f'{fam}_a{a}',f'q35_4b_c2grid_{fam}_a{a}'))
print('model | gen_acc gen_conf gen_ECE gen_Topt | transfer_acc transfer_conf transfer_ECE transfer_Topt | mixdev_acc mixdev_ECE')
res={}
for name,mf in cands:
    try:
        g=gen(mf); t=C.rows_for('preds_c2_transfer_dev','c2_transfer_dev',mf); m=C.rows_for('preds_c2_mixdev','c2_mixdev',mf)
    except Exception as e:
        print(name,'ERR',e); continue
    sg=C.summarize(g,'g'); st=C.summarize(t,'t'); sm=C.summarize(m,'m')
    res[name]={'gen':sg,'transfer':st,'mixdev':sm}
    print(f"{name:14s} | {sg['acc']:.2f} {sg['mean_conf']:.2f} {sg['ECE_eqmass10_T1']:.2f} {sg['T_opt_insample']} | {st['acc']:.2f} {st['mean_conf']:.2f} {st['ECE_eqmass10_T1']:.2f} {st['T_opt_insample']} | {sm['acc']:.2f} {sm['ECE_eqmass10_T1']:.2f}")
json.dump(res,open('calib_alpha.json','w'),indent=1)

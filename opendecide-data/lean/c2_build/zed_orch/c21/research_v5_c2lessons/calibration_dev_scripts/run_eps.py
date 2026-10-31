import sys, json
sys.path.insert(0,'.')
import calib_dev_analysis as C
GEN=['dev','dev_nc','taskbank_dev','hard_dev','dev_negwords','dev_claims','pg_dev','devzs','devp_card']
def mix(rows,eps):
    confs=[];corr=[];nll=0
    for r in rows:
        ks=list(r['probs']); K=len(ks)
        p={k:(1-eps)*r['probs'][k]+eps/K for k in ks}
        top=max(p,key=p.get)
        confs.append(p[top]); corr.append(1 if top==r['gold'] else 0)
        nll+=-__import__('math').log(p[r['gold']])
    return C.ece_equal_mass(confs,corr)*100, nll/len(rows), sum(confs)/len(confs)*100
for name,mf in (('C1','q35_4b_main500k_c2'),('C2','q35_4b_c2')):
    g=[];
    for d in GEN: g+=C.rows_for(f'preds_{d}',d,mf)
    t=C.rows_for('preds_c2_transfer_dev','c2_transfer_dev',mf)
    for lab,rows in (('general8143',g),('transfer600',t)):
        out=[]
        for eps in (0,0.02,0.05,0.10):
            e,n,mc=mix(rows,eps); out.append(f'eps{eps}: ECE {e:.2f} NLL {n:.3f} conf {mc:.1f}')
        print(name,lab,' | '.join(out))

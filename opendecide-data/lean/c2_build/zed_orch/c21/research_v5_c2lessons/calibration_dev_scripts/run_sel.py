import sys, json
sys.path.insert(0,'.')
import calib_dev_analysis as C
GEN=['dev','dev_nc','taskbank_dev','hard_dev','dev_negwords','dev_claims','pg_dev','devzs','devp_card']
models={'C1':'q35_4b_main500k_c2','C2':'q35_4b_c2'}
def sel(rows):
    confs,corr,_=C.stats(rows,1.0)
    idx=sorted(range(len(confs)),key=lambda i:-confs[i])
    n=len(idx); risks=[]; err=0
    for k,i in enumerate(idx,1):
        err+= 1-corr[i]; risks.append(err/k)
    aurc=sum(risks)/n
    acc=sum(corr)/n
    # optimal AURC (oracle) for E-AURC
    r=1-acc
    import math
    oracle=r+(1-r)*math.log(1-r) if r<1 else 1
    out={'AURC':round(aurc*100,2),'E-AURC':round((aurc-oracle)*100,2)}
    for cov in (0.5,0.7,0.8,0.9):
        k=int(cov*n); out[f'acc@cov{int(cov*100)}']=round(100*(1-risks[k-1]),2)
    return out
for name,mf in models.items():
    allr=[]
    for d in GEN: allr+=C.rows_for(f'preds_{d}',d,mf)
    t=C.rows_for('preds_c2_transfer_dev','c2_transfer_dev',mf)
    t19=[r for r in t if r['source']=='c2_t19']
    print(name,'general',len(allr),sel(allr))
    print(name,'transfer600',len(t),sel(t))
    print(name,'T19',len(t19),sel(t19))
    # T19 verdict rows: abstain-type predictions
    v=[r for r in t19 if 'Cannot be determined from the records' in r['probs']]
    pred_cbd=[r for r in v if max(r['probs'],key=r['probs'].get)=='Cannot be determined from the records']
    gold_cbd=[r for r in v if r['gold']=='Cannot be determined from the records']
    ok=sum(1 for r in pred_cbd if r['gold']==max(r['probs'],key=r['probs'].get))
    meanc=sum(max(r['probs'].values()) for r in pred_cbd)/max(1,len(pred_cbd))
    print(f'  T19 verdict rows n={len(v)} gold_CBD={len(gold_cbd)} pred_CBD={len(pred_cbd)} precision_of_pred_CBD={ok}/{len(pred_cbd)} mean_conf_on_pred_CBD={100*meanc:.1f}')

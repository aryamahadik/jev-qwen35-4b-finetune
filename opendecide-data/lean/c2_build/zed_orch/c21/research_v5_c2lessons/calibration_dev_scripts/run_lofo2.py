import sys, json, math, statistics as st
sys.path.insert(0,'.')
import calib_dev_analysis as C
TR=["F11","F4","F5","F6","GB","GW","I10","SB5","T01","T06","T15","T23","T25","T26","T28","T29","T30","T31"]
GEN=['dev','dev_nc','taskbank_dev','hard_dev','dev_negwords','dev_claims','pg_dev','devzs','devp_card']
models={'C1':'q35_4b_main500k_c2','C2':'q35_4b_c2'}
def wnll(groups,T,qt):
    # groups: list of rows lists; balanced: each group's mean NLL weighted equally (cap by sqrt?) -> equal weight
    tot=0;k=0
    for g in groups:
        s=[r for r in g if (r['qtype']=='noul')==(qt=='noul')]
        if len(s)<30: continue
        tot+=C.stats(s,T)[2]; k+=1
    return tot/max(k,1)
def fit_bal(groups,qt,floor=0.25):
    best=None
    for T in C.GRID:
        if T<floor-1e-9: continue
        v=wnll(groups,T,qt)
        if best is None or v<best[1]-1e-12: best=(T,v)
    return best[0]
def ece_with(rows,Tm):
    confs=[];corr=[]
    for r in rows:
        T=Tm['noul'] if r['qtype']=='noul' else Tm['choice']
        p=C.scale(r['probs'],T); top=max(p,key=p.get)
        confs.append(p[top]); corr.append(1 if top==r['gold'] else 0)
    return C.ece_equal_mass(confs,corr)*100
for name,mf in models.items():
    dom={}
    for d in GEN: dom[d]=C.rows_for(f'preds_{d}',d,mf)
    t=C.rows_for('preds_c2_transfer_dev','c2_transfer_dev',mf)
    dom['t19']=[r for r in t if r['source']=='c2_t19']; dom['t21']=[r for r in t if r['source']=='c2_t21']
    mix=C.rows_for('preds_c2_mixdev','c2_mixdev',mf)
    dom['mixdev_trained']=[r for r in mix if (r.get('meta') or {}).get('family') in TR]
    names=list(dom)
    res={'T1':[], 'balLOFO':[], 'balLOFO_floor1':[], 'balLOFO_floor1_ceil2':[]}
    Ts=[]
    for D in names:
        others=[dom[k] for k in names if k!=D]
        Tb={'noul':fit_bal(others,'noul'),'choice':fit_bal(others,'choice')}
        Tf={'noul':max(1.0,Tb['noul']),'choice':max(1.0,Tb['choice'])}
        Tc={'noul':min(2.0,Tf['noul']),'choice':min(2.0,Tf['choice'])}
        Ts.append((D,Tb))
        res['T1'].append(ece_with(dom[D],{'noul':1.0,'choice':1.0}))
        res['balLOFO'].append(ece_with(dom[D],Tb))
        res['balLOFO_floor1'].append(ece_with(dom[D],Tf))
        res['balLOFO_floor1_ceil2'].append(ece_with(dom[D],Tc))
    print('==',name)
    print(' T values (balanced LOFO):',[(d,t_['noul'],t_['choice']) for d,t_ in Ts])
    for k,v in res.items():
        print(f'  {k:22s} mean-domain ECE {st.mean(v):.2f}   per-domain', [round(x,1) for x in v])

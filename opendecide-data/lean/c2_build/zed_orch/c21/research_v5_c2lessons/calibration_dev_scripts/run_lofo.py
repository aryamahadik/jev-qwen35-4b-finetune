import sys, json, statistics
sys.path.insert(0,'.')
import calib_dev_analysis as C
TR=["F11","F4","F5","F6","GB","GW","I10","SB5","T01","T06","T15","T23","T25","T26","T28","T29","T30","T31"]
GEN=['dev','dev_nc','taskbank_dev','hard_dev','dev_negwords','dev_claims','pg_dev','devzs','devp_card']
models={'C1':'q35_4b_main500k_c2','C2':'q35_4b_c2'}
FR={'C1':{'noul':1.3,'choice':1.25},'C2':{'noul':0.8,'choice':0.95}}
def fitT(rows):
    out={}
    for qt in ('noul','choice'):
        s=[r for r in rows if (r['qtype']=='noul')==(qt=='noul')]
        out[qt]=C.best_T(s) if len(s)>=100 else 1.0
    return out
def ece_with(rows,Tmap):
    confs=[];corr=[]
    for r in rows:
        T=Tmap['noul'] if r['qtype']=='noul' else Tmap['choice']
        p=C.scale(r['probs'],T)
        top=max(p,key=p.get)
        confs.append(p[top]); corr.append(1 if top==r['gold'] else 0)
    return C.ece_equal_mass(confs,corr)*100
res={}
for name,mf in models.items():
    dom={}
    for d in GEN: dom[d]=C.rows_for(f'preds_{d}',d,mf)
    t=C.rows_for('preds_c2_transfer_dev','c2_transfer_dev',mf)
    dom['t19']=[r for r in t if r['source']=='c2_t19']
    dom['t21']=[r for r in t if r['source']=='c2_t21']
    mix=C.rows_for('preds_c2_mixdev','c2_mixdev',mf)
    mixtr=[r for r in mix if (r.get('meta') or {}).get('family') in TR]
    T_id=fitT(mixtr)
    rows_tab=[]
    for D in dom:
        others=[r for k,v in dom.items() if k!=D for r in v]
        T_lofo=fitT(others)                       # all other held-out domains
        T_lofo_mix=fitT(others+mixtr)             # others + trained-family mixdev
        T_opt=fitT(dom[D])                        # oracle
        e1=ece_with(dom[D],{'noul':1.0,'choice':1.0})
        e_fr=ece_with(dom[D],FR[name])
        e_id=ece_with(dom[D],T_id)
        e_lofo=ece_with(dom[D],T_lofo)
        e_lm=ece_with(dom[D],T_lofo_mix)
        e_or=ece_with(dom[D],T_opt)
        rows_tab.append((D,len(dom[D]),e1,e_fr,e_id,e_lofo,e_lm,e_or))
    print(f'== {name}  T_id(mixdev trained fams)={T_id}')
    print('domain n | ECE@T=1 | ECE@frozen | ECE@T_id | ECE@LOFO(held-out others) | ECE@LOFO+mixdev | ECE@oracle')
    for r in rows_tab: print(f'{r[0]:13s} {r[1]:5d} | {r[2]:6.2f} | {r[3]:6.2f} | {r[4]:6.2f} | {r[5]:6.2f} | {r[6]:6.2f} | {r[7]:6.2f}')
    import statistics as st
    print('MEAN of domains:', [round(st.mean(x[i] for x in rows_tab),2) for i in range(2,8)])
    print('WEIGHTED(n):', [round(sum(x[1]*x[i] for x in rows_tab)/sum(x[1] for x in rows_tab),2) for i in range(2,8)])

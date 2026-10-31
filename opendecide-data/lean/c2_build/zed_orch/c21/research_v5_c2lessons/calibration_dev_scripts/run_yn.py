import sys, json, math
sys.path.insert(0,'.')
import calib_dev_analysis as C
GEN=['dev','dev_nc','taskbank_dev','hard_dev','dev_negwords','dev_claims','pg_dev','devzs','devp_card']
TR=["F11","F4","F5","F6","GB","GW","I10","SB5","T01","T06","T15","T23","T25","T26","T28","T29","T30","T31"]
def yn_ece(rows,nb=10,mass=False,T=1.0):
    ps=[];ys=[]
    for r in rows:
        if r['qtype']!='noul': continue
        p=C.scale(r['probs'],T) if T!=1.0 else r['probs']
        s=p['yes']+p['no']
        ps.append(p['yes']/s); ys.append(1 if r['gold']=='yes' else 0)
    n=len(ps)
    idx=sorted(range(n),key=lambda i:ps[i])
    tot=0
    if mass:
        for b in range(nb):
            sub=idx[b*n//nb:(b+1)*n//nb]
            if sub: tot+=len(sub)/n*abs(sum(ps[i] for i in sub)/len(sub)-sum(ys[i] for i in sub)/len(sub))
    else:
        bins={}
        for i in range(n): bins.setdefault(min(int(ps[i]*nb),nb-1),[]).append(i)
        for sub in bins.values(): tot+=len(sub)/n*abs(sum(ps[i] for i in sub)/len(sub)-sum(ys[i] for i in sub)/len(sub))
    brier=sum((ps[i]-ys[i])**2 for i in range(n))/n
    return n,100*tot,brier
for name,mf in (('C1','q35_4b_main500k_c2'),('C2','q35_4b_c2')):
    g=[]
    for d in GEN: g+=C.rows_for(f'preds_{d}',d,mf)
    t=C.rows_for('preds_c2_transfer_dev','c2_transfer_dev',mf)
    m=C.rows_for('preds_c2_mixdev','c2_mixdev',mf)
    mt=[r for r in m if (r.get('meta') or {}).get('family') in TR]
    for lab,rows in (('general',g),('transfer',t),('mixdev_trained',mt)):
        n,e,b=yn_ece(rows); n2,e2,b2=yn_ece(rows,mass=True)
        n3,e3,b3=yn_ece(rows,T={'C1':1.3,'C2':0.8}[name])
        print(f'{name} {lab:15s} yes/no n={n} ECE(P(yes), 10 width bins)={e:.2f} eqmass={e2:.2f} Brier={b:.4f} | at frozen T: ECE={e3:.2f} Brier={b3:.4f}')

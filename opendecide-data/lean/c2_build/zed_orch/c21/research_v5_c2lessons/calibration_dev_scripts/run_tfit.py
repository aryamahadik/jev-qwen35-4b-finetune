import sys, json, statistics
sys.path.insert(0,'.')
import calib_dev_analysis as C
TR=["F11","F4","F5","F6","GB","GW","I10","SB5","T01","T06","T15","T23","T25","T26","T28","T29","T30","T31"]
models={'C1':'q35_4b_main500k_c2','C2':'q35_4b_c2'}
for name,mf in models.items():
    rows=C.rows_for('preds_c2_mixdev','c2_mixdev',mf)
    def fam(r):
        m=r.get('meta') or {}
        return m.get('family')
    sub=[r for r in rows if fam(r) in TR]
    print(name,'all',len(rows),'trained-family',len(sub), 'noul',sum(1 for r in sub if r['qtype']=='noul'),'choice',sum(1 for r in sub if r['qtype']!='noul'))
    for qt in ('noul','choice'):
        s=[r for r in sub if (r['qtype']=='noul')==(qt=='noul')]
        if not s: continue
        Tp=C.best_T(s)
        # median over families of per-family NLL at each T
        byf={}
        for r in s: byf.setdefault(fam(r),[]).append(r)
        best=None
        for T in C.GRID:
            vals=[C.stats(v,T)[2] for v in byf.values()]
            m=statistics.median(vals)
            if best is None or m<best[1]-1e-12: best=(T,m)
        confs,corr,nll=C.stats(s,1.0)
        print(f'  {qt}: n={len(s)} acc={100*sum(corr)/len(corr):.2f} meanconf={100*sum(confs)/len(confs):.2f} ECE_T1={100*C.ece_equal_mass(confs,corr):.2f} pooled_T_opt={Tp} median-over-{len(byf)}-families_T_opt={best[0]}')

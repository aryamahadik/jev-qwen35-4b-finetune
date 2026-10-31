import sys, json, random, math
sys.path.insert(0,'.')
import calib_dev_analysis as C
GEN=['dev','dev_nc','taskbank_dev','hard_dev','dev_negwords','dev_claims','pg_dev','devzs','devp_card']
def load(models_files, sets):
    out={}
    for name,mf in models_files.items():
        rows=[]
        for dd,gn in sets:
            gold=C.load_gold(gn)
            for r in C.rows_for(dd,gn,mf):
                r=dict(r); r['grp']=gn+':'+str(gold[r['id']].get('group_id') or r['id']); rows.append(r)
        out[name]=rows
    return out
def eceT(rows,Tm=None):
    confs=[];corr=[]
    for r in rows:
        if Tm: p=C.scale(r['probs'],Tm['noul'] if r['qtype']=='noul' else Tm['choice'])
        else: p=r['probs']
        top=max(p,key=p.get); confs.append(p[top]); corr.append(1 if top==r['gold'] else 0)
    return 100*C.ece_equal_mass(confs,corr), 100*sum(corr)/len(corr), 100*sum(confs)/len(confs)
random.seed(0)
mf={'C1':'q35_4b_main500k_c2','C2':'q35_4b_c2'}
for lab,sets in (('general',[(f'preds_{d}',d) for d in GEN]),('transfer',[('preds_c2_transfer_dev','c2_transfer_dev')])):
    d=load(mf,sets)
    # align by id
    ids=sorted(set(r['id'] for r in d['C1'])&set(r['id'] for r in d['C2']))
    m1={r['id']:r for r in d['C1']}; m2={r['id']:r for r in d['C2']}
    groups={}
    for i in ids: groups.setdefault(m1[i]['grp'],[]).append(i)
    gl=list(groups)
    diffs=[];dacc=[];dconf=[]
    for b in range(400):
        samp=[random.choice(gl) for _ in gl]
        r1=[];r2=[]
        for g in samp:
            for i in groups[g]: r1.append(m1[i]); r2.append(m2[i])
        e1,a1,c1=eceT(r1); e2,a2,c2=eceT(r2)
        diffs.append(e2-e1); dacc.append(a2-a1); dconf.append(c2-c1)
    def ci(x): x=sorted(x); return round(x[int(0.025*len(x))],2), round(x[int(0.975*len(x))],2)
    e1,_,_=eceT([m1[i] for i in ids]); e2,_,_=eceT([m2[i] for i in ids])
    print(lab,'n',len(ids),'groups',len(gl),'ECE C1',round(e1,2),'C2',round(e2,2),'diff',round(e2-e1,2),'CI95',ci(diffs),'| acc diff CI',ci(dacc),'| conf diff CI',ci(dconf))

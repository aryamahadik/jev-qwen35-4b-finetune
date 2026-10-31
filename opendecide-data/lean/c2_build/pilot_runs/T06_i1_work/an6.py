import sys, json, re, types
sys.dont_write_bytecode=True
sys.path.insert(0,'/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
import numpy as np
from scipy import sparse
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.preprocessing import MaxAbsScaler
import pilot
R=json.load(open('ch6000d.json'))
def mk(r, ctx=None):
    row={"options": r['opts'], "gold": r['gold'], "state": r['state'], "card": None, "instructions": r['ins'], "meta": {"card_id": r['card']}, "qtype":"choice"}
    return types.SimpleNamespace(row=row, question=r['q'], context=ctx if ctx is not None else r['ctx'], rr=None)
def accs(infos, view="c_card_without_question"):
    T,D,Y,Rw=pilot._pair_rows(infos, view)
    Y,Rw=np.array(Y),np.array(Rw)
    Xs=HashingVectorizer(n_features=2**18, analyzer=lambda x:x, alternate_sign=False, norm="l2").transform(T)
    Xd=DictVectorizer(sparse=False).fit_transform(D)
    groups=np.array([infos[ri].row['meta']['card_id'] for ri in Rw])
    folds=pilot._folds(list(groups)); res={}
    for nm in ("lr","gbt"):
        sc=np.zeros(len(Y))
        for tr,te in folds:
            if nm=="lr":
                sca=MaxAbsScaler().fit(Xd[tr])
                Xtr=sparse.hstack([Xs[tr],sparse.csr_matrix(sca.transform(Xd[tr]))]).tocsr()
                Xte=sparse.hstack([Xs[te],sparse.csr_matrix(sca.transform(Xd[te]))]).tocsr()
                sc[te]=pilot._lr().fit(Xtr,Y[tr]).predict_proba(Xte)[:,1]
            else:
                sc[te]=pilot._gbt().fit(Xd[tr],Y[tr]).predict_proba(Xd[te])[:,1]
        best={}
        for s,ri,yy in zip(sc,Rw,Y): best.setdefault(ri,[]).append((s,yy))
        acc=[]
        for ri,l in best.items():
            m=max(s for s,_ in l); top=[yy for s,yy in l if s>=m-1e-12]; acc.append(sum(top)/len(top))
        res[nm]=round(float(np.mean(acc)),4)
    ch=np.mean([1/len(r['opts']) for r in R])
    return res, round(float(ch),4)
if __name__=="__main__":
    print('base', accs([mk(r) for r in R]))
    print('no digits', accs([mk(r, re.sub(r'\d+',' ',r['ctx'])) for r in R]))
    print('empty ctx', accs([mk(r, '') for r in R]))
    print('question view', accs([mk(r) for r in R], 'a_question'))

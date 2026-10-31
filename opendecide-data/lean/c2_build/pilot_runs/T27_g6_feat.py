import json, sys
sys.dont_write_bytecode = True
sys.path.insert(0, ".")
import numpy as np, scipy.sparse as sp
import pilot
from collections import Counter
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import HashingVectorizer
rows = [json.loads(l) for p in sys.argv[1:] for l in open(p)]
out=[]
for r in rows:
    if r["qtype"]!="choice": continue
    rules,_,q=r["instructions"].rpartition("\n\n")
    ctx="\n".join(x for x in (r.get("card") or "",rules,r["state"]) if x.strip())
    out.append(pilot.RowInfo(r,None,None,0,q,ctx,None))
T,D,Y,Rw=pilot._pair_rows(out,"c_card_without_question")
from sklearn.feature_extraction import FeatureHasher
vocab={}
def idx(t):
    return vocab.setdefault(t,len(vocab))
rows_i=[[idx(t) for t in tk] for tk in T]
X=sp.lil_matrix((len(T),len(vocab)))
for i,r in enumerate(rows_i):
    for j in r: X[i,j]=1
X=X.tocsr()
Y=np.array(Y)
m=LogisticRegression(C=1.0,max_iter=3000,solver="liblinear").fit(X,Y)
inv={v:k for k,v in vocab.items()}
co=m.coef_[0]; df=np.asarray((X>0).sum(0)).ravel()
cand=[(co[j],inv[j],int(df[j])) for j in range(len(co)) if df[j]>=30 and inv[j].startswith("x:")]
cand.sort()
print("most negative"); 
for c,t,n in cand[:15]: print(round(c,2),t,n)
print("most positive")
for c,t,n in cand[-25:]: print(round(c,2),t,n)

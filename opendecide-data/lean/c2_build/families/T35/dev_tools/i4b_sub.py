import pickle, numpy as np, sys
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import GroupKFold
rows=pickle.load(open(sys.argv[1],"rb"))
X=[];Y=[];R=[];G=[]
for ri,r in enumerate(rows):
    k=r["k"]; order=sorted(range(k),key=lambda j:-r["clen"][j]); rank={j:n for n,j in enumerate(order)}
    for j in range(k):
        ab="kind:abstain" in r["kinds"][j]
        X.append(dict(k=k,clen=r["clen"][j],len_rank=rank[j]/(k-1),ab=float(ab),len_state=r["len_state"],n_lines=r["n_lines"],len_q=r["len_q"],pos=j,
                      lmin=min(r["clen"]), lmax=max(r["clen"])))
        Y.append(int(j==r["gold_pos"])); R.append(ri); G.append(r["card"])
names=list(X[0]); A=np.array([[x[n] for n in names] for x in X],float); Y=np.array(Y); R=np.array(R); G=np.array(G)
ch=np.mean([1/r["k"] for r in rows])
def run(cols,seed=0):
    idx=[names.index(c) for c in cols]; hit=0
    for tr,te in GroupKFold(5).split(A,Y,G):
        m=GradientBoostingClassifier(random_state=seed).fit(A[tr][:,idx],Y[tr]); p=m.predict_proba(A[te][:,idx])[:,1]
        for r in np.unique(R[te]):
            mk=R[te]==r; pm=p[mk]; ym=Y[te][mk]; top=ym[pm>=pm.max()-1e-12]; hit+=top.mean()
    return hit/len(rows)
print("chance",round(ch,4))
for cols in (["k","clen","len_rank","ab"],["k","clen","len_rank","ab","len_state"],["k","clen","len_rank","ab","len_state","n_lines","len_q"],["clen","len_rank","ab"],["k","clen","len_rank","ab","pos"],["k","clen","len_rank","ab","lmin","lmax"]):
    print(cols,[round(run(cols,s),4) for s in (0,1)])

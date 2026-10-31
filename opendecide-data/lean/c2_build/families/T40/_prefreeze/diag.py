import sys, collections, re
from pathlib import Path
sys.dont_write_bytecode=True
C2=Path(__file__).resolve().parents[3]; sys.path.insert(0,str(C2))
import pilot, numpy as np
from families.T40 import loader, fixtures, plugin as TP
loader.register(); ctx=fixtures.make_ctx(); p=TP.T40Plugin(lexicon=ctx.lexicon)
B=[];C=[]
for s in range(0,4000):
    c=TP.design(s,"S1")
    if c["kind"]!="ch" or c["head"] not in "BC": continue
    sp=p.sample(s,"S1"); rr=p.render(sp,ctx); q,cx=pilot.split_question(rr)
    info=pilot.RowInfo(rr.row,sp,rr,0,q,cx,None)
    (B if c["head"]=="B" else C).append((p.label(sp),info))
print(len(B),len(C))
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
y=[l for l,_ in B]; txt=[i.context for _,i in B]
cv=CountVectorizer(binary=True,token_pattern=r"[A-Za-z_]+",min_df=20); X=cv.fit_transform(txt)
lr=LogisticRegression(C=0.5,max_iter=500).fit(X,y); voc=np.array(cv.get_feature_names_out())
for k,cl in enumerate(lr.classes_): print(cl,list(voc[np.argsort(-lr.coef_[k])[:12]]))
fr={cl:np.asarray(X[[j for j,l in enumerate(y) if l==cl]].mean(0)).ravel() for cl in set(y)}
for w in ["followup","provider","menu","earlier","results","which","no","none"]:
    if w in voc: j=list(voc).index(w); print(w,{cl:round(float(f[j]),2) for cl,f in fr.items()})
for name,rows in (("B",B),("C",C)):
    print(name)
    for key in ("len_state","len_card","len_q","n_numbers","mag_max","n_lines","len_ins"):
        m=collections.defaultdict(list)
        for l,i in rows: m[l].append(pilot.meta_features(i)[1][key])
        print(" ",key,{l:round(float(np.mean(v)),1) for l,v in m.items()})

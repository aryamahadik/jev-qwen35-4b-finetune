import sys
from pathlib import Path
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
import pilot, pilot_loaders as PL, numpy as np
with PL.open_family("T20") as kit: b=pilot.build_pilot(kit,3500,run_g15=False)
ch=[i for i in b.infos if i.row["qtype"]=="choice"]
tx=[i.context for i in ch]; y=np.array([["SEV1","SEV2","SEV3","SEV4"].index(i.row["gold"]) for i in ch])
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
v=TfidfVectorizer(ngram_range=(1,2),min_df=5,sublinear_tf=True); X=v.fit_transform(tx)
m=LogisticRegression(max_iter=300,C=1.0).fit(X,y); names=np.array(v.get_feature_names_out())
print(len(ch),"train acc",m.score(X,y))
for k in range(4):
    top=np.argsort(-m.coef_[k])[:12]; print("SEV",k+1,[(names[t],round(m.coef_[k][t],2)) for t in top])
print(tx[0][:600])

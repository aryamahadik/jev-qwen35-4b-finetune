import sys, json, pickle
from pathlib import Path
sys.dont_write_bytecode=True
C2=Path(__file__).resolve().parents[3]; sys.path.insert(0,str(C2))
import pilot, pilot_loaders as PL, numpy as np
with PL.open_family("T20") as kit:
    b=pilot.build_pilot(kit,6000,run_g15=False)
out=[]
for i in b.infos:
    c,n=pilot.meta_features(i)
    out.append((i.row["qtype"],i.row["gold"],c,n,i.row["meta"].get("twin_of"),i.row["meta"].get("twin_kind"),i.row["role"]))
pickle.dump(out,open(str(Path(__file__).parent/"feat.pkl"),"wb"))
for part,pred in (("yn",lambda i:i.row["qtype"]!="choice"),("ch",lambda i:i.row["qtype"]=="choice")):
    infos=[i for i in b.infos if pred(i)]
    y=np.array([int(i.row["gold"]) if part=="yn" else ["SEV1","SEV2","SEV3","SEV4"].index(i.row["gold"]) for i in infos]) if part=="yn" else None
    if part=="yn":
        folds=pilot._folds([i.row["meta"]["card_id"] for i in infos])
        print(part,pilot.meta_drivers(infos,y,folds,top=12),flush=True)

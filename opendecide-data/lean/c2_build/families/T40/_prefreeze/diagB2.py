import sys, collections
from pathlib import Path
sys.dont_write_bytecode=True
C2=Path(__file__).resolve().parents[3]; sys.path.insert(0,str(C2))
import numpy as np
from families.T40 import loader, fixtures, plugin as TP
loader.register(); p=TP.T40Plugin(lexicon=fixtures.make_ctx().lexicon)
acc=collections.defaultdict(lambda: collections.defaultdict(list))
n=0
for s in range(0,1500):
    for smp in ("S1","S2","S3","S4"):
        c=TP.design(s,smp)
        if c["kind"]!="ch" or c["head"]!="B": continue
        sp=p.sample(s,smp); st=sp.structure; l=p.label(sp); rq=st["request"]
        names=[t["name"] for t in st["tools"]]
        a=acc[l]
        a["n_tools"].append(len(st["tools"])); a["has_results"].append(bool(st["results"])); a["n_results"].append(len(st["results"]))
        a["n_clauses"].append(len(rq["clauses"])); a["provider_clause"].append(bool(rq["provider"]))
        a["dup_names"].append(len(names)-len(set(names))); a["n_off"].append(sum(1 for t in st["tools"] if str(sp.slots[t["mslot"]]).endswith("no") or getattr(sp.slots[t["mslot"]],"value",None)=="no"))
        a["req_in_menu_purposes"].append(rq["purpose"] in [t["purpose"] for t in st["tools"]])
        a["n_res_fields"].append(sum(len(r["fields"]) for r in st["results"]))
        n+=1
print(n)
for k in ("n_tools","has_results","n_results","n_clauses","provider_clause","dup_names","req_in_menu_purposes","n_res_fields"):
    print(k,{l:round(float(np.mean(a[k])),3) for l,a in acc.items()})

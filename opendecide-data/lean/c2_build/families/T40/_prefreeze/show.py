import json,sys
d=json.load(open(sys.argv[1]))
for k in ("rows","by_head_qtype","build_drops","program_gates","g7","g10","reseed","tokens"): print(k,d[k])
for h,e in d["probes"].items(): print("probe",h,{k:(v["acc"],v["chance"],v["n"]) for k,v in e.items()})
def show(n,r):
    print(n,r["verdict"],[(f["part"],f["view"],f["model"],f["acc"],f["chance"],f["n"]) for f in r["fails"]])
    for p in ("yes_no","choice"):
        x=r[p]; print("  ",p,x.get("n"),x.get("chance"),{v:(x[v]["lr"],x[v]["gbt"]) for v in x if isinstance(x[v],dict) and "lr" in x[v] and v!="b_options" or v=="b_options" and p=="choice"})
show("pooled",d["g6_pooled"])
for h in "ABC": show(h,d["g6_head"][h])

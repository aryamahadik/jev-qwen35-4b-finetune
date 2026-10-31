import sys, pickle, collections
sys.dont_write_bytecode = True
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build")
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T27")
import numpy as np
infos = pickle.load(open("families/T27/work_i2b/infos_before.pkl", "rb"))
yn = [i for i in infos if i.row["qtype"] == "noul"]
def tab(keyf, name, minn=40):
    d = collections.defaultdict(list)
    for i in yn: d[keyf(i)].append(int(i.row["gold"]))
    print("--", name)
    for k, v in sorted(d.items(), key=lambda kv: str(kv[0])):
        if len(v) >= minn: print(f"   {str(k):52s} n={len(v):4d} yes={np.mean(v):.3f}")
ro = lambda i: not i.spec.env().get("ALLOWED", "").count(".") and i.spec.env()["TASK"] in ("task.summarise","task.find","task.extract","task.compare","task.draft")
tab(lambda i: (i.row["meta"]["qform"], ro(i)), "qform x read-only task")
tab(lambda i: (i.row["meta"]["qform"], i.spec.sampler), "qform x sampler")
tab(lambda i: (i.row["meta"]["qform"], i.spec.structure["layout"], i.row["meta"]["defs_style"][:24]), "qform x layout x defs_style")
tab(lambda i: (i.row["meta"]["qform"], len(i.spec.env().get("ALLOWED","").split("+"))), "qform x n allowed actions")
tab(lambda i: (i.row["meta"]["qform"], len([k for k in (1,2) if f"REQ{k}" in i.spec.slots])), "qform x n requests")
# card length buckets within qform
for qf in ("yn_beyond","yn_within"):
    L = np.array([len(i.row["card"]) for i in yn if i.row["meta"]["qform"]==qf]); Y = np.array([int(i.row["gold"]) for i in yn if i.row["meta"]["qform"]==qf])
    qs = np.quantile(L,[0.2,0.4,0.6,0.8])
    b = np.digitize(L, qs)
    print(qf, "len_card quintile yes rates", [round(float(Y[b==j].mean()),3) for j in range(5)], "n", [int((b==j).sum()) for j in range(5)])

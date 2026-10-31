import pickle, numpy as np, sys
rows=pickle.load(open(sys.argv[1],"rb"))
def mean(x): return round(float(np.mean(x)),2) if x else None
for smp in ["ALL","S1","S2","S3","S4","S5"]:
    R=[r for r in rows if smp=="ALL" or r["sampler"]==smp]
    print(smp,len(R))
    for k in (3,4):
        for ab in (True,False):
            S=[r for r in R if r["k"]==k and r["gold_abs"]==ab]
            if not S: continue
            print(" k",k,"abs",ab,"n",len(S),"len_state",mean([r["len_state"] for r in S]),"n_lines",mean([r["n_lines"] for r in S]),"gold_clen",mean([r["gold_clen"] for r in S]),"mean_clen",mean([np.mean(r["clen"]) for r in S]),"len_q",mean([r["len_q"] for r in S]))

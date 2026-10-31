import pickle, collections, re, sys, numpy as np
rows=pickle.load(open(sys.argv[1],"rb"))
src=open("../plugin.py").read()
m=re.search(r"^PAGE_ENDINGS\s*=.*$",src,re.M); exec(m.group(0)); _EXT=tuple(PAGE_ENDINGS)
def prof(t):
    eff,pat=t.split(": ",1)
    return ("*" in pat, pat.endswith("$"), "?" in pat, any(c.isupper() for c in pat), pat.rstrip("$").endswith(_EXT), pat.rstrip("$").endswith("/"), any(c.isdigit() for c in pat), eff=="Allow")
G=collections.Counter(); A=collections.Counter(); W=collections.Counter()
for r in rows:
    for t in r["opts"]:
        if t.startswith("No applying"): continue
        if r["gold_abs"]: A[prof(t)]+=1
        elif t==r["gold"]: G[prof(t)]+=1
        else: W[prof(t)]+=1
nG,nA,nW=sum(G.values()),sum(A.values()),sum(W.values())
names=["star","dollar","q","cap","ext","slash","digit","allow"]
for i,n in enumerate(names):
    g=sum(c for k,c in G.items() if k[i])/nG; a=sum(c for k,c in A.items() if k[i])/nA; w=sum(c for k,c in W.items() if k[i])/nW
    print(f"{n:7s} gold {g:.3f} abs-lines {a:.3f} wrong-lines {w:.3f}")
keys=set(G)|set(A); tv=0.5*sum(abs(G[k]/nG-A[k]/nA) for k in keys); print("TV(gold,abs lines)",round(tv,3))

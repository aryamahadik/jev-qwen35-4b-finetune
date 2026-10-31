import json, sys, re
sys.dont_write_bytecode = True
sys.path.insert(0, ".")
import pilot
from collections import Counter, defaultdict
from scipy.stats import chi2_contingency
rows=[json.loads(l) for p in sys.argv[1:] for l in open(p)]
rows=[r for r in rows if r["qtype"]=="choice"]
key={"do":"Do what","cont":"Ignore","stop":"Stop"}
def lab(r):
    g=r["gold"]; return "do" if g.startswith("Do what") else ("cont" if g.startswith("Ignore") else "stop")
cnt=defaultdict(Counter); tot=Counter()
for r in rows:
    rules,_,q=r["instructions"].rpartition("\n\n")
    ctx="\n".join(x for x in (r.get("card") or "",rules,r["state"]) if x.strip())
    L=lab(r); tot[L]+=1
    for t in set(pilot.toks(ctx)): cnt[t][L]+=1
print(tot)
res=[]
for t,c in cnt.items():
    n=sum(c.values())
    if n<60 or n>len(rows)-60: continue
    tab=[[c[l], tot[l]-c[l]] for l in ("do","cont","stop")]
    chi,p,_,_=chi2_contingency(tab)
    res.append((chi,t,n,[round(c[l]/tot[l],3) for l in ("do","cont","stop")]))
res.sort(reverse=True)
print(len(res))
for x in res[:30]: print(round(x[0],1),x[1],x[2],x[3])

"""JOB3: which plain disposition words appear as option labels in the C2 candidate rows (choice rows), per family; counts only.
Also GB/GW/MD are real-text blocks (no disposition options); checked by the same scan."""
import json, re, glob, collections
LEAN="/Users/aryamahadik/Documents/jev/opendecide-data/lean"
W=["stop","ask","refuse","reject","escalat","hold","deny","go ahead","proceed","continue","confirm","human","observe","monitor","allow","approve","decline","release","route","block","cannot","not determinable","apply"]
rx={w:re.compile(re.escape(w),re.I) for w in W}
res={}
for p in sorted(glob.glob(f"{LEAN}/data/c2_parts/*/out/candidates_c2.jsonl")):
    fam=p.split("/")[-3]
    n=0; c=collections.Counter(); g=collections.Counter()
    for l in open(p):
        r=json.loads(l)
        if r['qtype']!='choice': continue
        n+=1
        for w,x in rx.items():
            if any(x.search(o) for o in r['options']): c[w]+=1
            if x.search(str(r['gold'])): g[w]+=1
    res[fam]=(n,c,g)
    print(f"{fam:4s} choice={n:5d}", {w:(c[w],g[w]) for w in W if c[w]})

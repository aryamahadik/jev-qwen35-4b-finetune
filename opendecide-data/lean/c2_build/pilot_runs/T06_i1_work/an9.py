import json, collections
R=json.load(open('ch6000d.json'))
lg=[0,0,0]
by=collections.defaultdict(lambda:[0,0,0])
for r in R:
    o=r['opts']; L=[len(x) for x in o]; top=[j for j,x in enumerate(L) if x==max(L)]
    g=o.index(r['gold'])
    v=(1/len(top)) if g in top else 0
    for t in (by[len(o)], by['all']):
        t[0]+=v; t[1]+=1/len(o); t[2]+=1
print({k:(v[2], round(100*(v[0]-v[1])/v[2],2)) for k,v in by.items()})
# in none-gold terms
c=collections.Counter((len(r['opts']), r['gold_key']=='none') for r in R); print(c)

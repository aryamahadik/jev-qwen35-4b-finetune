import json, collections, sys
for f in sys.argv[1:]:
    R=json.load(open(f))
    print(f, len(R))
    by=collections.defaultdict(lambda:[0,0])
    lg=collections.defaultdict(lambda:[0,0,0])
    for r in R:
        k=len(r['opts'])
        for key in ((k,'twin' if r['twin'] else 'base'),(k,'all'),('all','all')):
            by[key][0]+= r['gold_key']=='none'; by[key][1]+=1
        o=r['opts']; L=[len(x) for x in o]; top=[j for j,x in enumerate(L) if x==max(L)]
        g=o.index(r['gold']); v=(1/len(top)) if g in top else 0
        for key in (k,'all'):
            lg[key][0]+=v; lg[key][1]+=1/k; lg[key][2]+=1
    print({k:(v[1], round(v[0]/v[1],3)) for k,v in sorted(by.items(), key=str)})
    print('longest pp', {k:round(100*(v[0]-v[1])/v[2],2) for k,v in lg.items()})

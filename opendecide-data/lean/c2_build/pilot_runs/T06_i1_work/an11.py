import json, collections, sys
from scipy.stats import chisquare
for f in sys.argv[1:]:
    R=json.load(open(f))
    pos=collections.defaultdict(lambda:[0]*4)
    for r in R:
        k=len(r['opts']); pos[k][r['opts'].index(r['gold'])]+=1
    print(f, {k:(v[:k], round(chisquare(v[:k]).pvalue,3)) for k,v in pos.items()})
    # by display
    d=collections.defaultdict(lambda: collections.Counter())
    for r in R:
        d[tuple(r['display'])][(len(r['opts']), r['opts'].index(r['gold']))]+=1

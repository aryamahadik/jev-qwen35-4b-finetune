import json, collections
R=[r for r in json.load(open('feats6000.json')) if r['qtype']=='noul']
def tab(key, minn=60, f=lambda r:r['refund']):
    d=collections.defaultdict(list)
    for r in R: d[key(r)].append(f(r))
    print({k:(len(v), round(sum(v)/len(v),3)) for k,v in sorted(d.items(), key=str) if len(v)>=minn})
st=lambda r:r['cat']['pack'].split('.')[1]
tab(lambda r:(st(r), r['num']['n_numbers']),50)
tab(lambda r:(st(r)),50)
tab(lambda r:(r['cat']['skin']),50, f=lambda r: r['num']['n_numbers'])
tab(lambda r:(r['cat']['skin']),50)

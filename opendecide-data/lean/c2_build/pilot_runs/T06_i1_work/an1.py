import json, collections
R=[r for r in json.load(open('feats6000.json')) if r['qtype']=='noul']
print(len(R))
def tab(key, minn=60):
    d=collections.defaultdict(list)
    for r in R: d[key(r)].append(r['refund'])
    print({k:(len(v), round(sum(v)/len(v),3)) for k,v in sorted(d.items(), key=str) if len(v)>=minn})
tab(lambda r: r['num']['n_numbers'])
tab(lambda r: (r['num']['n_numbers'], r['counts']))
tab(lambda r: (r['num']['n_numbers'], r['policy'] in ('pol.t06.faulty_order','pol.t06.mind_order','pol.t06.any_order','pol.t06.any_delivery')))
tab(lambda r: r['policy'])
tab(lambda r: r['cat']['format_style'].split('/')[1])
tab(lambda r: r['cat']['sampler'])
tab(lambda r: r['cat']['defs_style'])
tab(lambda r: (r['cat']['defs_style'], r['num']['n_numbers']),100)
tab(lambda r: r['role'])

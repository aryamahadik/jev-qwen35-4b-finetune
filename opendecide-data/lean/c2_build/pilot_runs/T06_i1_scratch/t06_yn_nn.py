import sys, json, collections, importlib, random, copy, numpy as np
sys.dont_write_bytecode = True
C2 = '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build'
sys.path.insert(0, C2)
import pilot
from families.T06 import plugin as T
rp = importlib.import_module('families.T06.run_pilot')
N = int(sys.argv[1])
with rp._t06() as kit:
    b = pilot.build_pilot(kit, N, run_g15=False)
yn=[i for i in b.infos if i.row['qtype']=='noul']
def refund(i):
    return bool(T._grants(T.facts(i.spec)))
rows=[]
for i in yn:
    c, n = pilot.meta_features(i)
    rows.append((n['n_numbers'], refund(i), T.facts(i.spec).policy in T.WINDOWED, i.row['meta']['qform'], int(i.row['gold']), n['mag_mean'], i.spec.structure['counts']))
nn = collections.defaultdict(list)
for r in rows: nn[r[0]].append(r[1])
print('refund rate by n_numbers', {k:(len(v), round(sum(v)/len(v),3)) for k,v in sorted(nn.items()) if len(v)>=40})
w = collections.defaultdict(list)
for r in rows: w[r[2]].append(r[1])
print('refund rate by windowed notice', {k:(len(v), round(sum(v)/len(v),3)) for k,v in w.items()})
cnt = collections.defaultdict(list)
for r in rows: cnt[r[6]].append(r[1])
print('refund rate by counts printed', {k:(len(v), round(sum(v)/len(v),3)) for k,v in cnt.items()})
pol = collections.defaultdict(list)
for i in yn: pol[T.facts(i.spec).policy].append(refund(i))
print('refund rate by policy', {k:(len(v), round(sum(v)/len(v),3)) for k,v in sorted(pol.items())})
for att in ('goods','reason','handover','style'):
    d = collections.defaultdict(list)
    for i in yn: d[getattr(T.facts(i.spec), att)].append(refund(i))
    print('refund rate by', att, {k:(len(v), round(sum(v)/len(v),3)) for k,v in sorted(d.items())})
# gold-yes rate by n_numbers within qform (the signal GBT uses)
for q in ('yn_refund','yn_not_refund'):
    d = collections.defaultdict(list)
    for r in rows:
        if r[3]==q: d[r[0]].append(r[4])
    print(q, {k:(len(v), round(sum(v)/len(v),3)) for k,v in sorted(d.items()) if len(v)>=30})

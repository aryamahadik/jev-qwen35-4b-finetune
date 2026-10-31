import sys, importlib, collections
sys.dont_write_bytecode=True
sys.path.insert(0,'/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
import pilot
from families.T06 import plugin as T
rp = importlib.import_module('families.T06.run_pilot')
with rp._t06() as kit:
    b = pilot.build_pilot(kit, 700, run_g15=False)
yn=[i for i in b.infos if i.row['qtype']=='noul']
seen=collections.defaultdict(list)
for i in yn:
    c,n=pilot.meta_features(i)
    seen[n['n_numbers']].append(i)
for k in sorted(seen):
    l=seen[k]
    print('=====', k, len(l), 'refund', round(sum(T._grants(T.facts(i.spec)) != frozenset() for i in l)/len(l),2))
    i=l[0]
    r=i.row
    print(r['state'][:1500]); print('--card--', (r.get('card') or '')[:100]); print('--ins--', r['instructions'][:200])
    print('NUMS', pilot._nums(r['state']+'\n'+(r.get('card') or '')+'\n'+r['instructions']))

import sys, json, collections, importlib, math
sys.dont_write_bytecode = True
C2 = '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build'
sys.path.insert(0, C2)
import pilot
rp = importlib.import_module('families.T06.run_pilot')
from families.T06 import plugin as T
with rp._t06() as kit:
    b = pilot.build_pilot(kit, 3000, run_g15=False)
rule = [i for i in b.infos if i.row['meta']['qform']=='ch_rule']
def cell(i, which):
    f = T.facts(i.spec)
    excl = T._excluded(f.goods, f.seal)
    cov = T.NOTICE_SCOPE[f.policy] is not None and T.NOTICE_SCOPE[f.policy][0] in ('any', f.reason)
    c = {'reason': (f.reason,), 'rs': (f.reason, excl), 'rsn': (f.reason, excl, cov)}[which]
    return c
for which in ('reason','rs','rsn'):
    cnt = collections.defaultdict(collections.Counter)
    for i in rule: cnt[cell(i, which)][i.rr.option_set.gold.key]+=1
    acc = sum(max(c.values()) for c in cnt.values())/len(rule)
    print(which, 'in-sample Bayes accuracy', round(acc,3), 'cells', len(cnt))
    if which=='rsn':
        for k,c in sorted(cnt.items()): print('  ', k, dict(c))

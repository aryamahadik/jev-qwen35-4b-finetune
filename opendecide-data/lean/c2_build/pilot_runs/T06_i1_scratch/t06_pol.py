import sys, collections, re, json
sys.dont_write_bytecode = True
sys.path.insert(0, '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
from families.T06 import freeze_v2 as FV, plugin as P
from c2_kit import polarity as PO
pools = FV.load_pools_v2()
ctx = FV.kit_ctx(pools)
ws = [s for s in ctx.skins.values() if s.kind == 'wording']
print(len(ws))
by = collections.defaultdict(list)
for w in ws: by[w.qform].append(w)
for q, l in sorted(by.items()): print(q, len(l), sum(1 for w in l if w.held_out))
# print a sample of each yes/no
for q in P.T06Plugin.QFORMS:
    if q.startswith('yn'):
        print('==', q)
        for w in by[q][:60]:
            print('  ', ('H ' if w.held_out else '  ') + w.text)

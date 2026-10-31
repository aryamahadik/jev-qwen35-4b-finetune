import sys, json, collections, importlib, random, copy, datetime as dt, re
sys.dont_write_bytecode = True
C2 = '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build'
sys.path.insert(0, C2)
import pilot
rp = importlib.import_module('families.T06.run_pilot')
N = int(sys.argv[1])
with rp._t06() as kit:
    b = pilot.build_pilot(kit, N, run_g15=False)
end = [i for i in b.infos if i.row['meta']['qform'].startswith('ch_end')]
print('rows', len(end))
def stat(name, f, minn=0):
    num = collections.Counter(); den = collections.Counter()
    for i in end:
        os_ = i.rr.option_set
        kinds = pilot.option_kinds(i)
        for j,o in enumerate(os_.options):
            v = f(i, o, j, kinds[j])
            den[v]+=1; num[v]+= (o.role=='gold')
    print(name, {v:(den[v], round(num[v]/den[v],3)) for v in sorted(den, key=str) if den[v]>=minn})
stat('longest/shortest', lambda i,o,j,k: (('L' if 'kind:longest' in k else '')+('S' if 'kind:shortest' in k else '')))
stat('clen', lambda i,o,j,k: len(o.text), 30)
stat('k x longest', lambda i,o,j,k: (len(i.rr.option_set.options), 'kind:longest' in k))
stat('tie count', lambda i,o,j,k: sum(len(x.text)==len(o.text) for x in i.rr.option_set.options))
stat('pos', lambda i,o,j,k: (len(i.rr.option_set.options), j))
stat('date form', lambda i,o,j,k: i.row['meta']['format_style'] and i.rr.forms['REQUEST_DATE'])
stat('role', lambda i,o,j,k: i.row['role'])

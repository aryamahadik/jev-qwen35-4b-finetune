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
def stat(name, f):
    num = collections.Counter(); den = collections.Counter()
    for i in end:
        r = i.row; os_ = i.rr.option_set
        for o in os_.options:
            v = f(i, o)
            den[v]+=1; num[v]+= (o.role=='gold')
    print(name, {v:(den[v], round(num[v]/den[v],3)) for v in sorted(den, key=str)})
stat('verbatim in text', lambda i,o: o.text.lower() in (i.row['state']+i.row['instructions']).lower())
stat('day-of-month bucket', lambda i,o: dt.date.fromisoformat(o.key).day//8)
stat('month', lambda i,o: dt.date.fromisoformat(o.key).month)
stat('weekday', lambda i,o: dt.date.fromisoformat(o.key).weekday())
stat('n errs of option', lambda i,o: len(o.err))
def centrality(i,o):
    ds = [dt.date.fromisoformat(x.key) for x in i.rr.option_set.options]
    d = dt.date.fromisoformat(o.key)
    s = sum(abs((d-x).days) for x in ds)
    allsums = sorted(sum(abs((y-x).days) for x in ds) for y in ds)
    return allsums.index(s)
stat('centrality rank (0 = most central)', centrality)
stat('same month as majority', lambda i,o: sum(dt.date.fromisoformat(x.key).month==dt.date.fromisoformat(o.key).month for x in i.rr.option_set.options))
stat('is requested date', lambda i,o: o.key == i.spec.env()['REQUEST_DATE'].isoformat())
stat('k', lambda i,o: len(i.rr.option_set.options))
# date format effect
stat('first token', lambda i,o: o.text.split()[0][:4] if not o.text[0].isdigit() else 'digit')

import sys, collections, time
sys.dont_write_bytecode=True
sys.path.insert(0,'/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
from families.T06 import fixtures as FX, plugin as T
ctx=FX.ctx(); pl=T.T06Plugin(lexicon=ctx.lexicon)
t0=time.time()
specs=[pl.sample(seed,s) for seed in range(3000) for s in ("S1","S2","S3","S4")]
print(len(specs), round(time.time()-t0))
tags=collections.Counter(t for s in specs for t in s.tags)
print({k: round(v/len(specs),3) for k,v in sorted(tags.items())})
yn=[s for s in specs if pl.QFORMS[s.qform].qtype=="noul"]
print('yes/no share', len(yn)/len(specs), 'yes', sum(pl.solve_a(s) for s in yn)/len(yn))
per=collections.defaultdict(list)
for s in yn: per[s.qform].append(pl.solve_a(s))
print({k: round(sum(v)/len(v),3) for k,v in per.items()})
for attr in ("goods","reason","policy","handover","style"):
    c=collections.defaultdict(list)
    for s in yn: c[getattr(T.facts(s),attr)].append(bool(T._grants(T.facts(s))))
    r=[sum(v)/len(v) for v in c.values()]; print(attr, round(min(r),3), round(max(r),3))
print(collections.Counter(s.qform for s in specs if s.qform in ('ch_rule','ch_end_reject','ch_end_withdraw')))

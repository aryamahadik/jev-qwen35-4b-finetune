import sys, collections
from pathlib import Path
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
from transfer.T20 import plugin as P
P.MAX_TRIES=100
import pilot_loaders as PL
with PL.open_family("T20") as kit:
    pl=kit.plugin
bad=collections.Counter(); tot=collections.Counter()
for smp in ("S1","S2","S3","S4","S5"):
    for seed in range(0,60):
        pn=P.plan_of(smp,seed)
        key=(smp,pn.kind,str(pn.target)[:4] if pn.kind=="choice" else (pn.qform,pn.target),pn.depth)
        tot[key]+=1
        try: pl.sample(seed,smp)
        except Exception as e: bad[key+(pn.mx,pn.mw)]+=1
print(sum(bad.values()),"of",sum(tot.values()))
for k,v in sorted(bad.items(),key=str)[:40]: print(k,v)

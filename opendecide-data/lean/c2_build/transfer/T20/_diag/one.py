import sys, random, collections
from pathlib import Path
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
from transfer.T20 import plugin as P
import pilot_loaders as PL
with PL.open_family("T20") as kit: pl=kit.plugin
smp,seed="S3",7
pn=P.plan_of(smp,seed); print(pn)
rng=random.Random("x"); c=collections.Counter()
for i in range(300):
    sc=pl._scenario(rng,pn,0); sp=pl._draw(rng,seed,smp,pn,sc)
    if sp is None: c["none"]+=1; continue
    c["ok"]+=1
    if pn.twin: c["twin" if P.twin_choice(sp,pl._twin_want(sp,pn)) else "notwin"]+=1
print(c)

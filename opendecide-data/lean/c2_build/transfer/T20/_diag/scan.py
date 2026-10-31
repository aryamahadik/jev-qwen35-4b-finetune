import sys
from pathlib import Path
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
from transfer.T20 import plugin as P
import pilot_loaders as PL
with PL.open_family("T20") as kit: pl=kit.plugin
P.MAX_TRIES=150
bad=[]
for seed in range(190,300):
    for smp in ("S1","S2","S3","S4","S5"):
        try: pl.sample(seed,smp)
        except Exception: bad.append((smp,seed,P.plan_of(smp,seed)))
for b in bad: print(b)

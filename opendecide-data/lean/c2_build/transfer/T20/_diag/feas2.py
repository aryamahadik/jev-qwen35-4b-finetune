import sys, collections, random
from pathlib import Path
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
from transfer.T20 import plugin as P
import pilot_loaders as PL
with PL.open_family("T20") as kit:
    pl=kit.plugin
seen=collections.defaultdict(collections.Counter)
rng=random.Random(5)
def plan(kind,target,level,mx,mw,q):
    return P.Plan(kind,q,"plain",target,level,"full",False,None,0,mx,mw)
cls=[("ch","sev%d"%i) for i in range(1,5)]+[("yn",True,"sev2"),("yn",True,"sev3"),("yn",False,"sev2"),("yn",False,"sev3")]
for smp in ("S1","S4"):
  for c in cls:
    for mx in range(4):
      for mw in (False,True):
        n=0
        for t in range(400):
            if c[0]=="ch": pn=plan("choice",c[1],None,mx,mw,P.CHOICE_FORM)
            else: pn=plan("yesno",c[1],c[2],mx,mw,"yn_reaches")
            scen=pl._scenario(rng,pn,0)
            sp=pl._draw(rng,t,smp,pn,scen)
            if sp is not None: seen[(smp,c,mx,mw)][sp.depth]+=1
import json
for smp in ("S1","S4"):
  for c in cls:
    for mw in (False,True):
        agg=collections.Counter()
        for mx in range(4): agg.update(seen[(smp,c,mx,mw)])
        mn=[sorted(d for d in range(1,6) if seen[(smp,c,mx,mw)][d]>=3) for mx in range(4)]
        print(smp,c,mw,dict(sorted(agg.items())),"min-per-mx",mn)

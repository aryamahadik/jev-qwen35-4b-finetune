import sys,json
sys.path.insert(0,'.')
from collections import Counter,defaultdict
import pilot_t37b as PT
from t37b import select as SEL, run_pilot_i3 as R
import t37b.sources as SRC
pool=PT.load_pool(); inp=PT.load_inputs(lambda *a:None)
allow,deny,_=R.a46_sets()
from t37b import noise as NZ
ps=NZ.screen_from_pilot(R.BASE_PILOT)
bases,rep=SEL.eligible(inp["rows"],inp["rels"],old_ids=inp["old_ids"],old_groups=inp["old_groups"],old_states=inp["old_states"],status=PT.status_fn(inp["deny"]),deny_sources=[],deny_ids=set(ps["bad_base_ids"])|deny,allow_ids=allow)
eq=pool.choices()
C=defaultdict(Counter)
for b in bases:
    s=b.row['source']; C[s]['n']+=1
    ce=[k for k in b.kinds if k in SRC.OPPOSITE_KINDS]
    if ce: C[s]['comp']+=1
    if 'equiv' in b.kinds and eq.get(b.entry.key) and SRC.slot_values(b.entry,b.row['instructions']) is not None: C[s]['equiv']+=1
    C[s]['both']+= bool(ce) and 'equiv' in b.kinds and bool(eq.get(b.entry.key))
for s,c in sorted(C.items(),key=lambda x:-x[1]['n']): print(s,dict(c))
print(len(bases))
import math
from c2_kit.distractors import uhash
SEL.TWIN_BALANCE=True
blocked=ps["blocked_templates"]
seed=PT.PLAN_SEED
order=sorted(bases,key=lambda b:uhash(seed,"t37b-order",b.row["id"]))
for basis in (2000,1500,1200,1000,900,800,700,600):
    plan=SEL._plan_once(order,SRC.FRAMES_TRAIN,1400,600,seed,"train",max(1,math.floor(.1*basis)),max(1,math.floor(.02*basis)),eq,True,frozenset(blocked))
    src=Counter(i.base.row['source'] for i in plan)
    print(basis,len(plan),dict(Counter(i.kind for i in plan)),dict(src))

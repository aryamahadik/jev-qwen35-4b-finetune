import sys,math
sys.path.insert(0,'.')
from collections import Counter
exec(open('t37b/_w8/an3.py').read().split("eq=pool.choices()")[0])
eq=pool.choices()
from c2_kit.distractors import uhash
SEL.TWIN_BALANCE=True
blocked=frozenset(ps["blocked_templates"]); seed=PT.PLAN_SEED
order=sorted(bases,key=lambda b:uhash(seed,"t37b-order",b.row["id"]))
for basis in (2000,1000):
    plan=SEL._plan_once(order,SRC.FRAMES_TRAIN,1400,600,seed,"train",math.floor(.1*basis),math.floor(.02*basis),eq,True,blocked,.1,.02)
    src=Counter(i.base.row['source'] for i in plan); tpl=SEL._template_counts(plan)
    print(basis,len(plan),dict(Counter(i.kind for i in plan)),dict(src),max(tpl.values()) if tpl else 0)

print(SEL.FP_TRACE[:60])

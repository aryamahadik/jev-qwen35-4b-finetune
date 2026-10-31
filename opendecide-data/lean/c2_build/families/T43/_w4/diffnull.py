import sys, pickle, random, types
sys.dont_write_bytecode=True; sys.path.insert(0,'.')
from families.T43 import probes as PR
def mk(path):
    rows=pickle.load(open(path,'rb'))
    return [types.SimpleNamespace(row=r, spec=types.SimpleNamespace(structure=st)) for r,st in rows]
for path in sys.argv[1:]:
    infos=mk(path)
    res=PR.diff_size(infos)
    print(path, 'REAL', {m:(v['cv_acc'],v['majority']) for m,v in res['models'].items()})
    for seed in range(3):
        R=random.Random(seed)
        pv=[i for i in infos if PR.head_of(i)=="pv" and i.row["gold"]!="does not apply"]
        gold=[i.row["gold"] for i in pv]; R.shuffle(gold)
        for i,g in zip(pv,gold): i.row=dict(i.row, gold=g)
        res=PR.diff_size(infos)
        print('  NULL',seed,{m:round(v['cv_acc']-v['majority'],4) for m,v in res['models'].items()})

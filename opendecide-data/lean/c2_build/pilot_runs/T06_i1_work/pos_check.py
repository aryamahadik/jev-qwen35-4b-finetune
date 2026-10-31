import sys, collections
sys.dont_write_bytecode=True
sys.path.insert(0,'/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
from scipy.stats import chisquare
from c2_kit.distractors import uhash
from families.T06 import fixtures as FX, plugin as T
ctx=FX.ctx(); pl=T.T06Plugin(lexicon=ctx.lexicon)
for base in (0, 900000, 5000000):
    pos=collections.defaultdict(lambda:[0]*4); byk=collections.defaultdict(lambda: collections.Counter())
    for seed in range(base, base+2500):
        for smp in ("S1","S2","S3","S4"):
            spec=pl.sample(seed,smp)
            if spec.qform!='ch_rule': continue
            shown=list(T._applicable(T.facts(spec)))+['none']
            key=pl.row_key(spec)
            keys=sorted(shown, key=lambda a: uhash(key,'closed',repr(a)))
            g=pl.solve_a(spec)
            pos[len(keys)][keys.index(g)]+=1
    print(base, {k:(v[:k], round(chisquare(v[:k]).pvalue,3)) for k,v in sorted(pos.items())}, flush=True)

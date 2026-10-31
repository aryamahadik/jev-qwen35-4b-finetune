import sys; sys.path.insert(0,'.'); sys.dont_write_bytecode=True
from collections import Counter, defaultdict
from families.T33 import plugin as T, fixtures as FX
ctx=FX.ctx(); pl=T.T33Plugin(lexicon=ctx.lexicon)
N=int(sys.argv[1]) if len(sys.argv)>1 else 300
err=Counter(); unf=defaultdict(Counter); prof=Counter(); gold=defaultdict(Counter); nb=defaultdict(Counter)
for smp in pl.SAMPLERS:
    for seed in range(N):
        try: sp=pl.sample(seed,smp)
        except Exception as e: err[(smp,str(e)[:50])]+=1; continue
        st=sp.structure; q=sp.qform
        if not q.startswith('ch_'): continue
        steps=st['intent']['steps']; u=sum(not v['done'] for v in steps.values())
        g=pl.designed_answer(sp)
        if q=='ch_failed_check':
            gk=g if g=='none' else g
            unf[q][(u,)]+=1; unf[q+'/'+str(g)][u]+=1
        elif q=='ch_bad_claim':
            unf[q+'/'+('None' if g=='none' else 'bad')][u]+=1
        else:
            prof[tuple(sorted(st['intent']['verdicts']))]+=1; gold[q][g]+=1
print('errors',dict(err)); 
for k,v in sorted(unf.items()): print(k,dict(v))
print('profiles',dict(prof)); print('verdict gold',dict(gold['ch_claim_verdict']))

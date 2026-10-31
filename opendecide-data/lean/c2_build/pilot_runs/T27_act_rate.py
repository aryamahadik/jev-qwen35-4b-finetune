import sys, collections
sys.dont_write_bytecode=True
sys.path.insert(0,'.'); sys.path.insert(0,'families/T27')
import run_pilot as RP
with RP._t27() as kit:
    P=kit.plugin
    from families.T27 import plugin as M
    out={"ch":collections.defaultdict(list),"yn":collections.defaultdict(list)}
    for seed in range(1500):
        for smp in ("S1","S2","S3","S4"):
            sp=P.sample(seed,smp); env=sp.env()
            k="ch" if sp.qform=="ch_next" else "yn"
            for (i,a,_,_),(w,_) in zip(M.asked_actions(env),P._statuses(env)):
                out[k][a].append(not w)
    for k in out:
        tot=sum(len(v) for v in out[k].values()); mean=sum(sum(v) for v in out[k].values())/tot
        print(k,"mean beyond",round(mean,3))
        r=sorted((sum(v)/len(v),a,len(v)) for a,v in out[k].items())
        print([ (round(x,2),a[:22],n) for x,a,n in r[:4]],[ (round(x,2),a[:22],n) for x,a,n in r[-3:]])

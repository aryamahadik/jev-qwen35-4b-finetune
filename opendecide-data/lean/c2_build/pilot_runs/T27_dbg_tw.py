import sys, collections
sys.dont_write_bytecode=True
sys.path.insert(0,'.'); sys.path.insert(0,'families/T27')
import run_pilot as RP
with RP._t27() as kit:
    P=kit.plugin
    from families.T27 import plugin as M
    c=collections.Counter(); n=0
    for seed in range(0,300):
        sp=P.sample(seed,"S1")
        if sp.qform=="ch_next": continue
        n+=1
        env=sp.env(); idx=P._index(); asked=M.asked_actions(env)
        base=M.construct_answer(sp.qform,P._statuses(env))
        for what in ("task","action","gate","target"):
            ok=any((a:=M.construct_answer(sp.qform,st)) is not None and a!=base for _,_,st in P._twin_candidates(what,sp,env,asked,idx))
            c[what]+=ok
    print(n,c)

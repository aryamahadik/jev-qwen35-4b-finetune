import sys, collections
sys.dont_write_bytecode=True
sys.path.insert(0,'.'); sys.path.insert(0,'families/T27')
import run_pilot as RP
import numpy as np
with RP._t27() as kit:
    P=kit.plugin
    from families.T27 import plugin as M
    idx=P._index()
    tasks=tuple(t for t in sorted(M.TASK_SCOPE) if idx.get(t) and M.TASK_SCOPE[t])
    ga=tuple(a for a in M.ACTIONS if idx.get(f"req.{a}.gate"))
    print(len(tasks),len(ga))
    for smp,prm in M.SAMPLER_PARAMS.items() if hasattr(M,"SAMPLER_PARAMS") else []:
        pass
    for po,ps in ((0.30,0.15),(0.45,0.35)):
        cells,cum=M.beyond_joint(tasks,ga,po,ps)
        m=np.diff(np.array((0,)+cum))
        w=M.choice_marginals(list(tasks))[0]
        tm=collections.Counter(); am=collections.Counter(); cm=collections.Counter()
        for (t,a),x in zip(cells,m):
            tm[t]+=x; am[a]+=x
            kinds=M.allowed_kinds(t)
            obj=any(M.KIND_OF[b] in kinds for b in a); sib=any(set(M.SIBLINGS[M.KIND_OF[b]])&kinds for b in a)
            cm["obj" if obj else ("sib" if sib else "none")]+=x
        print(po,ps,len(cells),"task err",max(abs(tm[t]-w[t]) for t in tasks),dict(cm))
    cells,cum=M.beyond_joint(tasks,ga,0.30,0.15)
    m=np.diff(np.array((0,)+cum))
    # D recomputed
    w=M.choice_marginals(list(tasks))[0]
    D=collections.Counter()
    for t in tasks:
        sc=M.TASK_SCOPE[t]
        if len(sc)==1: D[(sc[0],sc[0])]+=w[t]
        else:
            D[tuple(sorted(sc))]+=w[t]*M.R_DISTINCT
            for a in sc: D[(a,a)]+=w[t]*(1-M.R_DISTINCT)/2
    am=collections.Counter()
    for (t,a),x in zip(cells,m): am[a]+=x
    print("acts err",max(abs(am[a]-D[a]) for a in D), len(D))
    pa=collections.Counter(); pd=collections.Counter()
    for a,x in am.items():
        for b in a: pa[b]+=x/2
    for a,x in D.items():
        for b in a: pd[b]+=x/2
    print(sorted((round(pa[a]/pd[a],3),a) for a in pd)[:3])

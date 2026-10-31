import sys, collections, math
sys.dont_write_bytecode=True
sys.path.insert(0,'.'); sys.path.insert(0,'families/T27')
import run_pilot as RP
from scipy.stats import chi2_contingency
with RP._t27() as kit:
    P=kit.plugin
    from families.T27 import plugin as M
    tabs=collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    n=0
    for seed in range(0,2500):
        for smp in ("S1","S2","S3","S4"):
            sp=P.sample(seed,smp)
            if sp.qform!="ch_next": continue
            n+=1
            env=sp.env(); v=P.solve_a(sp)
            asked=M.asked_actions(env)
            for k in ("TASK","TARGET","INFO","JUST1","JUST2","REQ1","REQ2","GATE1","GATE2","SOURCE"):
                if k in env and env[k] is not None: tabs[k][str(env[k])][v]+=1
            for i,a,f,g in asked:
                tabs["act"][a][v]+=1; tabs["frame"][f][v]+=1
                tabs["gate_is_target"][str(g==env["TARGET"])][v]+=1
            tabs["act_pair"][" ".join(sorted(a for _,a,_,_ in asked))][v]+=1
            tabs["tone"][str(sorted(M.V.JUST_TONE.get(env.get(f"JUST{i}"),"?") for i in (1,2)))][v]+=1
            tabs["sampler"][smp][v]+=1
            tabs["pack"][sp.pack][v]+=1
    print("n",n)
    V=["continue","do_step","stop_ask"]
    for k,t in tabs.items():
        rows=[[c[v] for v in V] for c in t.values() if sum(c.values())>=10]
        if len(rows)<2: continue
        chi,p,dof,_=chi2_contingency(rows)
        print(f"{k:16s} levels={len(rows):3d} chi2={chi:8.1f} dof={dof:3d} p={p:.2e}")
    for k in ("act","frame"):
        print("==",k)
        for lv,c in sorted(tabs[k].items()):
            t=sum(c.values()); print(f"  {lv:34s} n={t:5d} "+" ".join(f"{v[:4]}={c[v]/t:.2f}" for v in V))
    print("== act_pair top by n")
    for lv,c in sorted(tabs["act_pair"].items(), key=lambda x:-sum(x[1].values()))[:14]:
        t=sum(c.values()); print(f"  {lv:70s} n={t:5d} "+" ".join(f"{v[:4]}={c[v]/t:.2f}" for v in V))

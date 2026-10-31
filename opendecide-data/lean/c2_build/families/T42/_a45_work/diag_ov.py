import sys, collections
sys.path.insert(0,'.')
from families.T42 import prefreeze as PF
import pilot
b = PF.build(800, 9)
out=[i for i in b.infos if i.row["meta"]["qform"] in ("ch_output","ch_return")]
rk=collections.defaultdict(collections.Counter)
ex=0
for i in out:
    r=i.row; opts=r["options"]; k=len(opts)
    vt=set(pilot.toks(i.context))
    ovf=[]; ovn=[]
    for o in opts:
        ou=pilot.toks(o); ov=set(ou)&vt
        ovf.append(len(ov)/max(1,len(set(ou)))); ovn.append(len(ov))
    gi=opts.index(r["gold"])
    kinds=pilot.option_kinds(i)
    # rank of gold among options by ovf with ties split: report (less, ties)
    for nm,sc in (("ovf",ovf),("ovn",ovn)):
        less=sum(x<sc[gi]-1e-9 for x in sc); ties=sum(abs(x-sc[gi])<1e-9 for x in sc)
        rk[nm][round((less+ (ties-1)/2)/(k-1),2)]+=1
    ve=[("kind:verbatim_in_text" in kk) for kk in kinds]
    rk["verb_gold"][ve[gi]]+=1; rk["verb_any"][any(ve)]+=1
    if i.row["meta"].get("qform")=="ch_output" and ex<2:
        ex+=1; print(repr(i.context[:300])); print(repr(i.question))
for nm in rk: print(nm, sorted(rk[nm].items()))

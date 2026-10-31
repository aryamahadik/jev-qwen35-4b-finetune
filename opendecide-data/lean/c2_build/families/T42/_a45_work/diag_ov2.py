import sys, collections
sys.path.insert(0,'.')
from families.T42 import prefreeze as PF
from families.T42 import plugin as P
from c2_kit.distractors import uhash
import pilot
b = PF.build(900, 9)
out=[i for i in b.infos if i.row["meta"]["qform"] in ("ch_output","ch_return")]
c=collections.Counter(); bad=[]
for i in out:
    r=i.row; sp=i.spec; st=sp.structure
    key=P.row_key(sp.seed, sp.sampler, sp.qform)
    opts=r["options"]
    vals=[o for o in opts if not o.startswith("raises ")]
    if r["gold"].startswith("raises ") or len(vals)<3: continue
    vt=set(pilot.toks(i.context))
    tk=[set(pilot.toks(o)) for o in vals]
    ovn=[float(len(a&vt)) for a in tk]; ovf=[n/max(1,len(a)) for n,a in zip(ovn,tk)]
    mine_ctx=P.context_tokens(st["code"], sp.qform)
    ovn2=[float(len(P.toks(o)&mine_ctx)) for o in vals]
    c["rows"]+=1
    c["ovn_equal_mine"]+= ovn==ovn2
    tb=[uhash(o,"tiebreak") for o in vals]
    gi=vals.index(r["gold"]); nv=len(vals)
    for nm,sc in (("ov_frac",ovf),("ov_count",ovn)):
        if max(sc)-min(sc)<1e-9: c[nm+"_skipped"]+=1; continue
        tgt=min(nv-1,int(uhash(key,"rank",nm)*nv))
        c[nm+"_applied"]+=1; ok=P._rank_is(sc,tb,gi,tgt); c[nm+"_ok"]+=ok
        if not ok and len(bad)<3: bad.append((r["gold"],vals,sc,tgt,ovn2))
print(dict(c)); print(bad)

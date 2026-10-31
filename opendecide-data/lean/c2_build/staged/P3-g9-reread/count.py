import sys, json
sys.dont_write_bytecode=True
sys.path.insert(0,'/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
import c2_select as S, c2io, crowd_select as cs
ilog=S.LinkGuardedInputLog()
tot=0
for fam in S.available(None):
    try:
        rows,rels,shas=S.family_inputs(ilog,fam)
        sd=S.SHARDS/fam
        pg,view=S.load_c1(ilog,rows,sd/f"labels_{S.C1}",sd)
    except SystemExit as e:
        print(fam,'ERR',str(e)[:200]); continue
    low=[r for r in rows if pg[r['id']]<cs.G5_PG]
    tot+=len(low)
    print(fam,len(rows),len(low),shas['candidates_sha256'][:12])
print(tot, cs.G5_PG)

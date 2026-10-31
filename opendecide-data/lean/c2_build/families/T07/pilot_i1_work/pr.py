import sys, json, collections
sys.path.insert(0, ".")
from c2_kit import pipeline
from c2_kit.choiceplan import plan_report
from families.T07 import load_v2 as L, plugin as P, fixtures as FX
ctx = FX.ctx() if (len(sys.argv) > 1 and sys.argv[1] == "fx") else L.make_ctx(L.load_pools())
pl = P.T07Plugin(lexicon=ctx.lexicon)
sets=[]; roles=collections.Counter()
for smp in ("S1","S2","S3","S4"):
    for seed in range(400):
        s = pl.sample(seed, smp)
        if s.qform not in ("ch_failing","ch_offers"): continue
        r = pipeline.build_unit(pl, s, ctx, run_g15=False)
        if not r.ok: print("DROP", smp, seed, r.problems[:1]); continue
        for rr in r.rendered:
            if rr.option_set is not None:
                sets.append(rr.option_set); roles[rr.row["role"]]+=1
print(len(sets), roles)
rep = plan_report(sets)
print(json.dumps({k: rep[k] for k in ("rows","abstain_cells","positions","positions_chi2_p","length_ranks_chi2_p","longest_gold_pp","failing","pass")}, indent=1))

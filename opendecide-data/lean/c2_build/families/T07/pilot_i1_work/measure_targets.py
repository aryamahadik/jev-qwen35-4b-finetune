"""Measure the G0 section 2 lines that the v2 changes move (test_plugin's 2,000 base specs, fixtures ctx)."""
import sys, collections, json
sys.path.insert(0, ".")
from c2_kit import pipeline
from families.T07 import fixtures as FX, plugin as P
import negcount
ctx = FX.ctx(); pl = P.T07Plugin(lexicon=ctx.lexicon)
specs = [pl.sample(seed, smp) for smp in ("S1","S2","S3","S4") for seed in range(500)]
units = [pipeline.build_unit(pl, s, ctx, run_g15=False) for s in specs]
bad = [u.problems[:1] for u in units if not u.ok]
print("units", len(units), "failed", len(bad), bad[:3])
rows = [r for u in units for r in u.rows]
rep = pipeline.overlay_report(units, pl)
print("rows", len(rows))
for k in ("complement_share_of_yes_no", "non_syntactic_share_of_pairs", "twin_share", "equiv_share", "attack_share", "yes_rate"):
    print(k, round(rep[k], 4))
print("abstain", rep["abstain"])
yn = [r for r in rows if r["qtype"] == "noul"]
print("yn share emitted", round(len(yn)/len(rows),4), "yes_is_bad", round(sum(pl.QFORMS[r["meta"]["qform"]].yes_is_bad for r in yn)/len(yn),4))
ks = [negcount.count(r["instructions"].split("\n\n")[-1]).k_syn for r in yn]
print("syn neg >=1", round(sum(x>=1 for x in ks)/len(ks),4), ">=2", round(sum(x>=2 for x in ks)/len(ks),4))
def control(s):
    a = pl.solve_a(s)
    return a == "both" if s.qform == "ch_offers" else (a == "none" if s.qform == "ch_failing" else bool(a) == P.YES_MEANS_GETS[s.qform])
print("controls", round(sum(control(s) for s in specs)/len(specs),4))
cf=[pl.solve_a(s) for s in specs if s.qform=="ch_failing"]
co=collections.Counter(pl.solve_a(s).split(":")[0] for s in specs if s.qform=="ch_offers")
print("base cf none", round(cf.count("none")/len(cf),4), "n", len(cf), "offers both", round(co["both"]/sum(co.values()),4), "neither", round(co["neither"]/sum(co.values()),4))
shown=gold=0; chance=0.0
for u in units:
    for rr in u.rendered:
        os_ = rr.option_set
        if os_ is None or not any(o.key=="none" for o in os_.options): continue
        shown+=1; gold+= os_.gold.key=="none"; chance+=1/len(os_.options)
print("emitted ch_failing none: gold share", round(gold/shown,4), "mean 1/k", round(chance/shown,4), "rows", shown)
tw=[r for r in rows if r["role"]=="twin"]; print("twin rows", len(tw), "choice twins", sum(r["qtype"]=="choice" for r in tw))
toks=[len(r["state"])+2*len(r["instructions"])+len(r.get("card") or "") for r in rows]

"""T24 w9 diagnostic (no gate): build N QC rows at a seed base through gen_full_c2's QC path and dump per-row
(qform, wording id, card, gold, sampler, seed) to a jsonl, then print yes rates by qform / wording spread."""
import sys, json, time
from pathlib import Path
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(C2))
import gen_full_c2 as G
fam = "T24"; base = int(sys.argv[1]); n = int(sys.argv[2]); out = sys.argv[3]
src = G.quarantine_sources(fam); banned = set().union(*map(set, src.values()))
with G.loader_patch(fam):
    with G.PL.open_family(fam) as kit0:
        kit, xrep = G.apply_exclusions(kit0, banned)
        b = G.pilot.build_pilot(kit, n, seed_base=base, run_g15=False)
with open(out, "w") as f:
    for i in b.infos:
        r = i.row
        f.write(json.dumps({"q": r.get("qtype"), "gold": r["gold"], "card": r["meta"].get("card_id"),
                            "qform": getattr(i.spec, "qform", None), "seed": getattr(i.spec, "seed", None),
                            "sampler": getattr(i.spec, "sampler", None), "question": i.question}) + "\n")
print("rows", len(b.infos))

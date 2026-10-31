import sys, json
from pathlib import Path
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(C2))
import gen_full_c2 as G
fam="T15"
src = G.quarantine_sources(fam); banned = set().union(*map(set, src.values()))
with G.loader_patch(fam):
    with G.PL.open_family(fam) as kit0:
        kit, xrep = G.apply_exclusions(kit0, banned)
        rd = G.Redraw(kit.plugin, xrep["dead_qforms"])
        try:
            b = G.pilot.build_pilot(kit, 30, seed_base=int(sys.argv[1]), run_g15=(sys.argv[2]=="1"), max_attempts=12)
        finally:
            rd.restore()
print(b.stats["units_attempted"], len(b.units), b.stats["drops_by_gate"])
print(json.dumps(b.stats["drop_examples"], indent=0)[:2500])

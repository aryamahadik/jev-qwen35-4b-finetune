import sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import gen_full_c2 as G
fam = "T24"
src = G.quarantine_sources(fam); banned = set().union(*map(set, src.values()))
with G.loader_patch(fam):
    with G.PL.open_family(fam) as kit0:
        kit, x = G.apply_exclusions(kit0, banned)
        b = G.pilot.build_pilot(kit, 40, seed_base=124000000, run_g15=True)
        print("ROWS", len(b.infos), b.stats.get("drops_by_gate"), str(b.stats.get("drop_examples"))[:600])

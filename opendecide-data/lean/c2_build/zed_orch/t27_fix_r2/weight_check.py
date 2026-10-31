"""Does the booked weight (1 + emitting relations) equal the rows a unit really emits? Builds ~60 units at seed base 2,000,000 with
the overlay and compares wording_balance.unit_rows(plugin, spec) with len(result.rows) per unit. Counts only."""
import json, sys
from collections import Counter
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2 = HERE.parents[1]
for p in (str(C2), str(HERE)):
    sys.path.insert(0, p)
import gen_full_c2 as G
import pilot
import overlay as O
import wording_balance as WB
from c2_kit import pipeline
seen = []
orig = pipeline.build_unit
def spy(plugin, spec, ctx, **kw):
    res = orig(plugin, spec, ctx, **kw)
    if res.ok:
        seen.append((WB.unit_rows(plugin, spec), len(res.rows)))
    return res
pipeline.build_unit = spy
src = G.quarantine_sources("T27")
banned = set().union(*map(set, src.values()))
with O.patched(wordings=False):
    with G.loader_patch("T27"):
        with G.PL.open_family("T27") as kit0:
            kit, _x = G.apply_exclusions(kit0, banned)
            b = pilot.build_pilot(kit, 110, seed_base=2_000_000, run_g15=False)
c = Counter((a, r) for a, r in seen)
print(json.dumps({"units": len(seen), "predicted_equals_actual": sum(1 for a, r in seen if a == r),
                  "pairs(predicted,actual)": {f"{a},{r}": n for (a, r), n in sorted(c.items())}}))

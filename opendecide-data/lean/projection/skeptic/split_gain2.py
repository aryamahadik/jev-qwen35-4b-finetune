"""Pessimist check (read-only): per-split dev gains for the steps whose held-out transfer we know, vs v11c -> 4B-E.
'Broad/unfamiliar' splits = devzs + devp_card + dev_nc (zero-shot / card / btzsc sources); 'in-family' = pg_dev,
hard_dev, dev_negwords, dev_claims, taskbank_dev (targeted families or REF-lineage sources); 'dev' separate."""
import sys, os
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean"); os.chdir("/Users/aryamahadik/Documents/jev/opendecide-data/lean")
import gate_dev as G
import numpy as np
SPL = G.SPLITS.split(",")
BROAD = {"devzs", "devp_card", "dev_nc"}
FAM = {"pg_dev", "hard_dev", "dev_negwords", "dev_claims", "taskbank_dev"}
UNSEEN = set(G.UNSEEN_FROZEN_ROWS)
for cand, ref, note in (("q35_4b_v11c", "q35_4b_v10", "OHS-1 +1.89, OHS-2 +1.67"), ("q35_4b_v11b", "q35_4b_v10", "OHS-1 +1.79"),
                        ("q35_4b_v11c", "q35_4b_v11b", "OHS-1 +0.11"), ("q35_4b_pxE", "q35_4b_v11c", "held-out unknown"),
                        ("q35_4b_v13t", "q35_4b_v11c", "held-out unknown"), ("q35_4b_pxE", "q35_4b_v13t", "held-out unknown")):
    rows, miss = G.load_rows(SPL, cand, ref)
    out = []
    for lab, f in (("broad(devzs+devp_card+dev_nc)", lambda x: x["split"] in BROAD), ("in-family(pg,hard,negw,claims,taskbank)", lambda x: x["split"] in FAM),
                   ("unseen-source set", lambda x: x["source"] in UNSEEN)):
        for h in ("select", "confirm", None):
            R = [x for x in rows if f(x) and (h is None or x["half"] == h)]
            b = G.group_boot(R)
            out.append(f"{lab:40s} {h or 'pooled':7s} n={len(R):5d} {b['diff']:+.2f} [{b['lo']:+.2f}, {b['hi']:+.2f}]")
    print(f"== {cand} vs {ref}  ({note})"); print("\n".join("   " + o for o in out))

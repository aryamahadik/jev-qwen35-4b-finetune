"""Optimist check 4 (read-only, dev only): 4B-E - v11c and v11c - v10 on the unseen-source set, split by dev half
(4B-E was picked on dev-confirm; the select half is the less biased read). Also 4B-E vs every sibling 4B."""
import sys, os
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean"); os.chdir("/Users/aryamahadik/Documents/jev/opendecide-data/lean")
import gate_dev as G
SPL = G.SPLITS.split(",")
for cand, ref in (("q35_4b_pxE", "q35_4b_v11c"), ("q35_4b_v11c", "q35_4b_v10"), ("q35_4b_v11b", "q35_4b_v10"),
                  ("q35_4b_pxE", "q35_4b_v13t"), ("q35_4b_pxE", "q35_4b_blend50"), ("q35_4b_pxE", "q35_4b_pxI")):
    rows, miss = G.load_rows(SPL, cand, ref); assert not miss
    uns = [x for x in rows if x["source"] in G.UNSEEN_FROZEN_ROWS]
    out = []
    for h in ("select", "confirm"):
        for q in ("all", "noul", "choice"):
            R = [x for x in uns if x["half"] == h and (q == "all" or x["qtype"] == q)]
            b = G.group_boot(R); out.append(f"{h[:3]} {q[:3]} {b['diff']:+.2f} [{b['lo']:+.2f},{b['hi']:+.2f}]")
    print(f"{cand} - {ref} (unseen set): " + " | ".join(out))

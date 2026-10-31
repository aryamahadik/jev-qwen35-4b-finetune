"""Pessimist check (read-only): dev gap of the 2B kd pilot to its teacher v10 on the 4 splits it has, vs its OHS-1 gap (-9.75)."""
import sys, os
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean"); os.chdir("/Users/aryamahadik/Documents/jev/opendecide-data/lean")
import gate_dev as G
SPL = ["pg_dev", "devzs", "devp_card", "dev"]
for cand in ("q35_2b_kd", "q35_2b_kd_cal"):
    rows, miss = G.load_rows(SPL, cand, "q35_4b_v10")
    b = G.group_boot(rows)
    print(f"{cand} vs q35_4b_v10 on {SPL}: n={len(rows)} {b['diff']:+.2f} [{b['lo']:+.2f}, {b['hi']:+.2f}] missing={miss[:1]}")
    for sp in SPL:
        R = [x for x in rows if x["split"] == sp]; bb = G.group_boot(R)
        print(f"    {sp:10s} n={len(R):4d} {bb['diff']:+.2f}")
# same 4 splits for the matched v11c -> v11r pair and I_1600 -> 4B-E, for a like-for-like dev gap
for c, r in (("q35_2b_v11r", "q35_4b_v11c"), ("q35_2b_armI_1600", "q35_4b_pxE")):
    rows, miss = G.load_rows(SPL, c, r); b = G.group_boot(rows)
    print(f"{c} vs {r} on the same 4 splits: {b['diff']:+.2f} [{b['lo']:+.2f}, {b['hi']:+.2f}]")

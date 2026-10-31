"""Optimist check 3 (read-only, dev only): where 4B-E's gain over v11c sits, and how the older v10 -> v11c step
looked on the same slices (the only step we also saw on a clean held-out exam, OHS-2).
Slices: unseen-source primary set (gate_dev.UNSEEN_FROZEN_ROWS), by question type, by split, carded vs card-less yes/no.
"""
import sys, os, json
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean"); os.chdir("/Users/aryamahadik/Documents/jev/opendecide-data/lean")
import gate_dev as G
SPL = G.SPLITS.split(",")
card = {}
for s in SPL:
    for l in open(f"data/{s}.jsonl"):
        r = json.loads(l); card[(s, r["id"])] = bool((r.get("card") or "").strip())
def show(lab, rows):
    b = G.group_boot(rows); print(f"   {lab:34s} n={b['n']:5d}  {b['cand']:6.2f} vs {b['ref']:6.2f}  diff {b['diff']:+5.2f} [{b['lo']:+.2f}, {b['hi']:+.2f}]")
for cand, ref in (("q35_4b_pxE", "q35_4b_v11c"), ("q35_4b_v11c", "q35_4b_v10")):
    rows, miss = G.load_rows(SPL, cand, ref)
    assert not miss, miss
    print(f"== {cand} minus {ref}")
    uns = [x for x in rows if x["source"] in G.UNSEEN_FROZEN_ROWS]
    show("unseen-source set, all", uns)
    show("unseen-source set, yes/no", [x for x in uns if x["qtype"] == "noul"])
    show("unseen-source set, choice", [x for x in uns if x["qtype"] == "choice"])
    show("all dev yes/no, carded", [x for x in rows if x["qtype"] == "noul" and card[(x["split"], x["id"])]])
    show("all dev yes/no, card-less", [x for x in rows if x["qtype"] == "noul" and not card[(x["split"], x["id"])]])
    for s in SPL:
        R = [x for x in rows if x["split"] == s]
        for q in ("noul", "choice"):
            Q = [x for x in R if x["qtype"] == q]
            if len(Q) >= 50: show(f"{s} {q}", Q)

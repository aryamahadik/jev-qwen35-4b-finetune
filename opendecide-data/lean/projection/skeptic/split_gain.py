"""Pessimist check (read-only): where does v11c -> 4B-E dev gain come from? per split and per source, per half."""
import sys, os
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean"); os.chdir("/Users/aryamahadik/Documents/jev/opendecide-data/lean")
import gate_dev as G
import numpy as np
from collections import defaultdict
SPL = G.SPLITS.split(",")
for cand, ref in (("q35_4b_pxE", "q35_4b_v11c"), ("q35_4b_pxE", "q35_4b_v13t"), ("q35_4b_pxE", "q35_4b_pxI")):
    rows, miss = G.load_rows(SPL, cand, ref)
    print(f"== {cand} vs {ref}  (missing: {miss[:1]})")
    for h in ("select", "confirm"):
        R = [x for x in rows if x["half"] == h]
        tot = sum(x["ok_c"] - x["ok_r"] for x in R) / len(R) * 100
        print(f"  {h}: total diff {tot:+.2f} pp over {len(R)} rows; contribution by split (pp of micro) and split diff:")
        by = defaultdict(list)
        for x in R: by[x["split"]].append(x["ok_c"] - x["ok_r"])
        for sp, v in sorted(by.items(), key=lambda kv: -sum(kv[1])):
            print(f"     {sp:14s} n={len(v):5d} diff {100*np.mean(v):+6.2f}  contrib {100*sum(v)/len(R):+5.2f}")
    # per source, both halves pooled: top contributors
    by = defaultdict(list)
    for x in rows: by[(x["source"], x["qtype"])].append(x["ok_c"] - x["ok_r"])
    tot = sum(sum(v) for v in by.values())
    print(f"  pooled: top/bottom source contributions (net correct rows; total {tot:+.0f} of {len(rows)} rows = {100*tot/len(rows):+.2f} pp)")
    items = sorted(by.items(), key=lambda kv: -sum(kv[1]))
    for (s, q), v in items[:12]:
        print(f"     + {s:34s} {q:6s} n={len(v):4d} net {sum(v):+5.0f}  diff {100*np.mean(v):+6.2f}")
    for (s, q), v in items[-6:]:
        print(f"     - {s:34s} {q:6s} n={len(v):4d} net {sum(v):+5.0f}  diff {100*np.mean(v):+6.2f}")
    top = [kv for kv in items if 'mixtral' in kv[0][0] or 'tb_' in kv[0][0] or 'tab' in kv[0][0]]
    print("  table-like sources:", [(s, q, len(v), int(sum(v))) for (s, q), v in top])
    ex = [x for x in rows if not any(t in x["source"] for t in ("mixtral", "tb_", "tab"))]
    for h in ("select", "confirm"):
        R = [x for x in ex if x["half"] == h]
        b = G.group_boot(R)
        print(f"  EXCLUDING table-like sources, {h}: {b['diff']:+.2f} [{b['lo']:+.2f}, {b['hi']:+.2f}] n={len(R)}")

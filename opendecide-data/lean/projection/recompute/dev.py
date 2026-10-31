import sys, json, math
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean")
import os; os.chdir("/Users/aryamahadik/Documents/jev/opendecide-data/lean")
import gate_dev as G
import numpy as np
SPL = G.SPLITS.split(",")
M4 = ["q35_4b_v10", "q35_4b_v11", "q35_4b_v11b", "q35_4b_v11c", "q35_4b_v12t", "q35_4b_v13t", "q35_4b_blend50", "q35_4b_pxE", "q35_4b_pxI", "q35_4b_pxE_tta"]
M2 = ["q35_2b_v11", "q35_2b_v11r", "q35_2b_armE", "q35_2b_armE_L4", "q35_2b_armI", "q35_2b_armI_1600", "q35_2b_armE_L4_1600"]
out = {}
def summ(rows, key):
    d = {}
    for h in ("select", "confirm", "all"):
        R = [x for x in rows if h == "all" or x["half"] == h]
        yn = [x for x in R if x["qtype"] == "noul"]; ch = [x for x in R if x["qtype"] == "choice"]
        br = [(float(x["p_" + key].get("yes", 0.0)) - x["gold"]) ** 2 for x in yn]
        d[h] = {"n": len(R), "micro": 100 * np.mean([x["ok_" + key] for x in R]),
                "yn": 100 * np.mean([x["ok_" + key] for x in yn]), "n_yn": len(yn),
                "ch": 100 * np.mean([x["ok_" + key] for x in ch]), "n_ch": len(ch), "brier_raw": float(np.mean(br))}
    return d
for ref in ["q35_4b_pxE", "q35_2b_v11r"]:
    for m in (M4 + M2):
        rows, miss = G.load_rows(SPL, m, ref)
        if miss:
            out[(m, ref)] = {"missing": miss}; continue
        s = summ(rows, "c")
        res = {"summary": s}
        for h in ("select", "confirm"):
            R = [x for x in rows if x["half"] == h]
            res["vs_" + ref + "_" + h] = G.group_boot(R)
            res["vs_" + ref + "_" + h + "_yn"] = G.group_boot([x for x in R if x["qtype"] == "noul"])
            res["vs_" + ref + "_" + h + "_ch"] = G.group_boot([x for x in R if x["qtype"] == "choice"])
        res["vs_" + ref + "_all"] = G.group_boot(rows)
        res["equiv_flip"] = G.relation_flips(SPL, rows, ("equiv",))
        res["crossfit"] = G.crossfit(rows, "c")
        out[(m, ref)] = res
for (m, ref), r in out.items():
    if "missing" in r:
        print(m, ref, "MISSING", r["missing"][:2]); continue
    s = r["summary"]
    print(f"== {m} (ref {ref})")
    for h in ("select", "confirm", "all"):
        x = s[h]
        print(f"   {h:8s} n={x['n']} micro {x['micro']:.2f} | yn {x['yn']:.2f} (n={x['n_yn']}) | ch {x['ch']:.2f} (n={x['n_ch']}) | brier_raw {x['brier_raw']:.4f}")
    for h in ("select", "confirm", "all"):
        v = r["vs_" + ref + "_" + h]
        print(f"   vs {ref} {h}: {v['diff']:+.2f} [{v['lo']:+.2f}, {v['hi']:+.2f}] ({v['groups']} groups)")
    for h in ("select", "confirm"):
        a, b = r["vs_" + ref + "_" + h + "_yn"], r["vs_" + ref + "_" + h + "_ch"]
        print(f"      {h} yn {a['diff']:+.2f} [{a['lo']:+.2f}, {a['hi']:+.2f}] ch {b['diff']:+.2f} [{b['lo']:+.2f}, {b['hi']:+.2f}]")
    e = r["equiv_flip"]; c = r["crossfit"]
    print(f"   equiv flip {e['cand']:.2f}% vs ref {e['ref']:.2f}% (n={e['n']}) | crossfit noul T {c['noul']['T_fit_select']}/{c['noul']['T_fit_confirm']} brier_cal {c['noul']['brier_cal']:.4f} raw {c['noul']['brier_raw']:.4f}")

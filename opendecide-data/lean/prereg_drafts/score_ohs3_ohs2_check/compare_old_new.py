"""Old (score_ohs.py) vs new (score_ohs3.py) on OHS-2. Old numbers: the committed results_ohs2/results_{all,S}.json
(v11c_cal, v11c_cal_bc, v10_cal; the old scorer reproduces them byte for byte) and old_score_ohs_v11c_{all,S}.json
(the old scorer run on the uncalibrated q35_4b_v11c in a sandbox copy). New numbers: new_{all,S}.json.
  ../../.venv/bin/python compare_old_new.py   (from this directory)
"""
import json
from pathlib import Path

C = Path(__file__).resolve().parent
L = C.parents[1]
for h in ("all", "S"):
    new = json.load(open(C / f"new_{h}.json"))
    old = json.load(open(L / f"results_ohs2/results_{h}.json"))["models"]
    old.update(json.load(open(C / f"old_score_ohs_v11c_{h}.json"))["models"])
    print(f"===== OHS-2 half {h}")
    for m, r in new["models"].items():
        print(f"--- {m}")
        pairs = [(k, r["primary"][k], old[m]["vs_jev"][k], old[m][k]) for k in ("micro", "macro", "brier_yesno")]
        if old.get(m + "_bc"):
            pairs += [(f"bc_{k}", r["secondary"][f"bc_{k}"], old[m + "_bc"]["vs_jev"][k], old[m + "_bc"][k])
                      for k in ("micro", "macro", "brier_yesno")]
        for k, v, ov, oval in pairs:
            padj = v.get("p_holm", v.get("q_bh"))
            print(f"  {k:15s} OD old {oval} new {v['od']:.4f} | diff old {ov['diff']:+.3f} new {v['diff']:+.3f} | "
                  f"CI old {ov['ci95']} new [{v['ci95'][0]:+.3f}, {v['ci95'][1]:+.3f}] | p old {ov['p']} new "
                  f"{v['p']:.4f} | adj old {ov['p_holm']} new {padj:.4f} | new verdict "
                  f"{v['verdict']['label'] if isinstance(v['verdict'], dict) else v['verdict']}")

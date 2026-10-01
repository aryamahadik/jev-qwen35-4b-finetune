"""PREREG_FINAL.md 2, C3 "merge check first": the cat merges with weights (1,0) and (0,1) must reproduce the fresh
single-adapter predictions of the same job on the 9 gate splits: argmax agreement >= 99.5% and mean |dp| < 2e-3
(dp of a row = the largest absolute change of one option's probability, as in gate_dev.py --mode refparity).
Not a look; nothing is logged.
  python gate/merge_check.py q35_4b_main500k_c3w10 q35_4b_main500k_j2     (1,0) vs the job-2 C1 read
  python gate/merge_check.py q35_4b_main500k_c3w01 q35_4b_pxE_fresh2      (0,1) vs the job-2 fresh REF read
Exit 0 = PASS, 2 = FAIL.
"""
import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import gate_dev as gd  # noqa: E402

MIN_AGREE, MAX_MEAN_DP = 99.5, 2e-3


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("merged")
    ap.add_argument("single")
    ap.add_argument("--splits", default=gd.SPLITS)
    ap.add_argument("--json", default="")
    a = ap.parse_args(argv)
    gd._MODE = "merge_check"
    rows = gd.complete_rows(a.splits.split(","), a.merged, a.single)
    per = defaultdict(lambda: [0, 0, 0.0, 0.0])
    for x in rows:
        keys = ["yes", "no"] if x["qtype"] == "noul" else x["options"]
        dp = max(abs(float(x["p_c"].get(k, 0.0)) - float(x["p_r"].get(k, 0.0))) for k in keys)
        s = per[x["split"]]
        s[0] += 1; s[1] += gd.argmax_label(x, x["p_c"]) == gd.argmax_label(x, x["p_r"]); s[2] += dp; s[3] = max(s[3], dp)
    n = sum(v[0] for v in per.values())
    agree = 100 * sum(v[1] for v in per.values()) / n
    mean_dp = sum(v[2] for v in per.values()) / n
    ok = agree >= MIN_AGREE - 1e-9 and mean_dp < MAX_MEAN_DP
    res = {"merged": a.merged, "single": a.single, "n": n, "agree": agree, "mean_dp": mean_dp,
           "max_dp": max(v[3] for v in per.values()), "pass": ok,
           "per_split": {sp: {"n": v[0], "agree": 100 * v[1] / v[0], "mean_dp": v[2] / v[0], "max_dp": v[3]}
                         for sp, v in per.items()}}
    print(f"MERGE CHECK {a.merged} vs {a.single}: agreement {agree:.2f}% (>= {MIN_AGREE}), mean |dp| {mean_dp:.5f} "
          f"(< {MAX_MEAN_DP}), max |dp| {res['max_dp']:.4f} (n={n}): {'PASS' if ok else 'FAIL'}")
    if a.json:
        Path(a.json).parent.mkdir(parents=True, exist_ok=True)
        Path(a.json).write_text(json.dumps(res, indent=2) + "\n")
    sys.exit(0 if ok else 2)


if __name__ == "__main__":
    main()

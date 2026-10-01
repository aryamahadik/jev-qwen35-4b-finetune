"""g2_noise.py: how noisy is the yn2b A/B rule G2 (pooled dev_negwords + pg_dev + hard_dev, point >= 0.0)?

Read-only, CPU only. Uses existing dev preds of 2B models and gate_dev's group_id bootstrap (10,000 resamples,
seed 0). Never reads OHS data. Writes nothing unless --json is given.

Null pair: q35_2b_armE_L4 minus q35_2b_armE (same recipe; GPU and micro-batching differ), the pair SPEC 11.5 uses.
For each candidate G2 bar it prints the false-fail rate for a harmless add (true diff 0) and the chance to catch a
true harm of -2 / -3 pp, from a normal approximation with the measured bootstrap SD. Row-sampling noise only:
training noise comes on top, so the false-fail rates are lower bounds.

  ../.venv/bin/python prereg_drafts/g2_noise.py [--json out.json]
"""
import argparse
import json
import math
import sys
from pathlib import Path

LEAN = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(LEAN))
import gate_dev as gd  # noqa: E402

G2 = ("dev_negwords", "pg_dev", "hard_dev")
PAIRS = [("q35_2b_armE_L4", "q35_2b_armE", "null pair (same recipe, SPEC 11.5)"),
         ("q35_2b_armI_1600", "q35_2b_armE_L4_1600", "reference: recipe change (I vs E at 1,600 steps)")]
ASR_NAMES = ["q35_2b_armE", "q35_2b_armE_L4", "q35_2b_armE_L4_1600", "q35_2b_armI", "q35_2b_armI_1600",
             "q35_2b_armI_LS0", "q35_2b_armKI", "q35_2b_armJ", "q35_2b_armL", "q35_2b_armO1", "q35_2b_v11r"]
BARS = [0.0, -0.5, -1.0, -1.5, -1.75, -2.0]


def phi(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def sd_of(b):
    return (b["hi"] - b["lo"]) / (2 * 1.959964)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    out = {}
    for cand, ref, label in PAIRS:
        rows, missing = gd.load_rows(gd.SPLITS.split(","), cand, ref)
        if missing:
            print(f"{cand} vs {ref}: missing preds: {missing}")
            continue
        crows = [x for x in rows if x["source"] not in gd.CONSTRAINT_EXCLUDE]
        res = {"label": label}
        print(f"==== {cand} - {ref}: {label}")
        sets = {"G2 pooled": [x for x in crows if x["split"] in G2]}
        for sp in G2:
            sets[sp] = [x for x in crows if x["split"] == sp]
        sets["full (no tb_mixtral)"] = crows
        for k, rs in sets.items():
            b = gd.group_boot(rs)
            b["sd"] = sd_of(b)
            res[k] = b
            print(f"   {k:22s} n={b['n']:5d} units={b['groups']:5d} diff={b['diff']:+.2f} "
                  f"[{b['lo']:+.2f}, {b['hi']:+.2f}] sd={b['sd']:.2f}")
        out[f"{cand}-{ref}"] = res
    null = out.get("q35_2b_armE_L4-q35_2b_armE")
    if null:
        sd = null["G2 pooled"]["sd"]
        print(f"\n==== G2 bar choice, row-sampling SD {sd:.2f} pp (null pair); normal approximation")
        print("   bar    false fail (true 0)  catch true -2.0  catch true -3.0")
        tab = []
        for bar in BARS:
            ff = phi((bar - 0.0) / sd)
            c2 = phi((bar + 2.0) / sd)
            c3 = phi((bar + 3.0) / sd)
            tab.append({"bar": bar, "false_fail": ff, "catch_m2": c2, "catch_m3": c3})
            print(f"   {bar:+.2f}   {100 * ff:5.1f}%               {100 * c2:5.1f}%          {100 * c3:5.1f}%")
        ub = {"rule": "fail only if the 95% upper bound < 0", "false_fail": 0.025,
              "catch_m2": phi((2.0 - 1.959964 * sd) / sd), "catch_m3": phi((3.0 - 1.959964 * sd) / sd)}
        print(f"   UB<0   {100 * ub['false_fail']:5.1f}%               {100 * ub['catch_m2']:5.1f}%          "
              f"{100 * ub['catch_m3']:5.1f}%   (significant-harm veto)")
        out["bars"] = tab
        out["ub_rule"] = ub
        out["null_g2_point"] = null["G2 pooled"]["diff"]
    print("\n==== NR5 context: jagged / OPI ASR of stored 2B reads (gate_dev.jagged_units / opi_units; eligible n)")
    asr = {}
    for n in ASR_NAMES:
        line = []
        for key, fn in (("jagged", gd.jagged_units), ("opi", gd.opi_units)):
            u = fn(n)
            if u is None:
                line.append("n/a")
                continue
            h, e = sum(x for x, _ in u.values()), sum(y for _, y in u.values())
            asr.setdefault(n, {})[key] = {"asr": h / e, "eligible": int(e)}
            line.append(f"{100 * h / e:5.1f}% ({int(e)})")
        print(f"   {n:22s} jagged {line[0]:14s} opi {line[1]}")
    out["asr"] = asr
    if a.json:
        Path(a.json).write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()

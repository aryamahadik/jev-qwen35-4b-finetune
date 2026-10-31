"""Optimist check 1 (read-only; OHS-1/OHS-2/dev pred files only, never OHS-3).
(a) Brier split by correctness: what the Brier gap would be at EQUAL yes/no accuracy.
(b) Jev run-to-run disagreement by question type (a floor for its option-order drift / complement violation).
(c) Jev sharpness, ties and missing answers.
(d) 4B-E option-order drift on dev choice rows (reversed order), derived as p_rev = 2*p_tta - p_parity
    (decoder_io.predict averages the two views in probability space; parity and tta reads are the same od_gcp pipeline).
Run: python3 projection/optimist/o1_brier_noise_drift.py
"""
import json, os
from collections import defaultdict
import numpy as np
os.chdir("/Users/aryamahadik/Documents/jev/opendecide-data/lean")
J = ["jev_guard", "jev_r2_guard"]
BASE_EXCL = ("_neg", "_dneg", "_para", "_yn", "_perm")


def load(p):
    return {json.loads(l)["id"]: json.loads(l) for l in open(p)}


def probs(r, pr):
    if pr is None:
        return None
    keys = ["yes", "no"] if r["qtype"] == "noul" else r["options"]
    return {k: float(pr.get(k, 0.0)) for k in keys}


def pred(p):
    b = max(p.values()); top = [k for k, v in p.items() if v == b]
    return top[0] if len(top) == 1 else None


def gold(r):
    return ("yes" if r["gold"] == 1 else "no") if r["qtype"] == "noul" else r["gold"]


print("=== (a) Brier by correctness on yes/no base rows; (c) Jev sharpness ===")
for split, ours in (("ohs", ["q35_4b_v11c_cal", "q35_4b_v11b_cal", "q35_4b_v10_cal"]), ("ohs2", ["q35_4b_v11c_cal", "q35_4b_v10_cal"])):
    rows = load(f"data/{split}.jsonl")
    base = [i for i, r in rows.items() if r["role"] in ("aff", "choice") and not i.endswith(BASE_EXCL)]
    yn = [i for i in base if rows[i]["qtype"] == "noul"]
    P = {n: {k: v["probs"] for k, v in load(f"preds_{split}/{n}.jsonl").items()} for n in ours + J}
    for n in J + ours:
        acc, br, brc, brw, ext, ties, miss = [], [], [], [], [], 0, 0
        for i in yn:
            r = rows[i]; p = probs(r, P[n].get(i))
            if p is None:
                miss += 1; acc.append(0); br.append(1.0); brw.append(1.0); continue
            c = pred(p) == gold(r); b = (p["yes"] - r["gold"]) ** 2
            ties += pred(p) is None
            acc.append(c); br.append(b); (brc if c else brw).append(b)
            ext.append(p["yes"] <= 0.02 or p["yes"] >= 0.98)
        a = np.mean(acc)
        print(f"{split:4s} {n:18s} yn acc {100*a:5.2f}  Brier {np.mean(br):.4f}  Brier/err {np.mean(br)/(1-a):.3f}  "
              f"Brier|correct {np.mean(brc):.4f}  Brier|wrong {np.mean(brw):.4f}  share p<=.02 or >=.98 {100*np.mean(ext):4.1f}%  ties {ties} missing {miss}")
    # equal-accuracy counterfactual: ours' conditional Briers at Jev's accuracy vs Jev's own
    def cond(n):
        a, bc, bw = [], [], []
        for i in yn:
            r = rows[i]; p = probs(r, P[n].get(i))
            if p is None:
                a.append(0); bw.append(1.0); continue
            c = pred(p) == gold(r); b = (p["yes"] - r["gold"]) ** 2
            a.append(c); (bc if c else bw).append(b)
        return np.mean(a), np.mean(bc), np.mean(bw)
    aj = np.mean([cond(j)[0] for j in J]); bcj = np.mean([cond(j)[1] for j in J]); bwj = np.mean([cond(j)[2] for j in J])
    for n in ours:
        ao, bco, bwo = cond(n)
        at_jev_acc = aj * bco + (1 - aj) * bwo
        jev_b = aj * bcj + (1 - aj) * bwj
        print(f"   {split} {n}: Brier at Jev's accuracy ({100*aj:.2f}%) would be {at_jev_acc:.4f} vs Jev {jev_b:.4f} -> diff (ours-Jev) {at_jev_acc-jev_b:+.4f}")

print("\n=== (b) Jev run-to-run disagreement (argmax differs between jev_guard and jev_r2_guard), base rows ===")
for split in ("ohs", "ohs2"):
    rows = load(f"data/{split}.jsonl")
    base = [i for i, r in rows.items() if r["role"] in ("aff", "choice") and not i.endswith(BASE_EXCL)]
    allr = [i for i in rows]
    P = {n: {k: v["probs"] for k, v in load(f"preds_{split}/{n}.jsonl").items()} for n in J}
    for lab, ids in (("choice base", [i for i in base if rows[i]["qtype"] == "choice"]),
                     ("yes/no base", [i for i in base if rows[i]["qtype"] == "noul"]),
                     ("choice >26 opts", [i for i in base if rows[i]["qtype"] == "choice" and len(rows[i]["options"]) > 26]),
                     ("all rows incl. twins", allr)):
        d = [pred(probs(rows[i], P[J[0]].get(i)) or {"_": 1}) != pred(probs(rows[i], P[J[1]].get(i)) or {"_": 1}) for i in ids]
        if ids:
            print(f"{split:4s} {lab:22s} n={len(ids):5d}  Jev run-to-run argmax disagreement {100*np.mean(d):.2f}%")

print("\n=== (d) 4B-E option-order drift on dev (reversed option order), from the TTA and parity reads ===")
SPL = ["dev", "dev_claims", "dev_nc", "dev_negwords", "devp_card", "devzs", "hard_dev", "pg_dev", "taskbank_dev"]
flip, flip_w, n_by, tv_all, acc_id, acc_rev, sw_flip = [], [], defaultdict(list), [], [], [], []
for s in SPL:
    rows = load(f"data/{s}.jsonl")
    pp = {k: v["probs"] for k, v in load(f"preds_{s}/q35_4b_pxE_parity.jsonl").items()}
    pt = {k: v["probs"] for k, v in load(f"preds_{s}/q35_4b_pxE_tta.jsonl").items()}
    for i, r in rows.items():
        if i not in pp or i not in pt:
            continue
        a, t = probs(r, pp[i]), probs(r, pt[i])
        rev = {k: 2 * t[k] - a[k] for k in a}
        if r["qtype"] == "choice":
            f = pred(a) != pred(rev)
            flip.append(f); n_by[min(len(r["options"]), 40) >= 20].append(f)
            tv_all.append(0.5 * sum(abs(a[k] - rev[k]) for k in a))
            acc_id.append(pred(a) == gold(r)); acc_rev.append(pred(rev) == gold(r))
        else:
            sw_flip.append(pred(a) != pred(rev))
print(f"choice rows {len(flip)}: argmax changes under reversed option order {100*np.mean(flip):.2f}%  "
      f"(>=20 options: {100*np.mean(n_by[True]):.2f}% of {len(n_by[True])}; <20: {100*np.mean(n_by[False]):.2f}% of {len(n_by[False])})")
print(f"   mean total-variation distance {np.mean(tv_all):.4f}; accuracy identity {100*np.mean(acc_id):.2f} vs reversed {100*np.mean(acc_rev):.2f}")
print(f"yes/no rows {len(sw_flip)}: answer changes when the Yes/No letters are swapped {100*np.mean(sw_flip):.2f}%")

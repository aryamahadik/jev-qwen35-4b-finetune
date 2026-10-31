"""Counts only: G8v2 partitions are card-grouped, half the cards, equal to the family g8.py scheme; permutation laws."""
import json, random, sys
import numpy as np
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/common")
import g8_aflite as G
res = {}
for fam in ["F2", "F5", "F6"]:
    rows, sha = G.load_pool(G.LEAN / f"c_src/{fam}/out/candidates_r1.jsonl")
    cards = np.array([str(r["meta"]["card_id"]) for r in rows]); uc = sorted(set(cards.tolist()))
    s0 = G.ADAPTERS[fam]["seed0"]; trs = G.partitions(cards, s0); bad = 0; same = 0
    for p, tr in enumerate(trs):
        a, b = set(cards[tr].tolist()), set(cards[~tr].tolist())
        bad += bool(a & b) or len(a) != len(uc) // 2
        fam_tr = set(random.Random(s0 + p).sample([r["meta"]["card_id"] for r in rows] and sorted(set(r["meta"]["card_id"] for r in rows)), len(uc) // 2))
        same += a == fam_tr
    # permutation laws on real label arrays (no features needed)
    yn = [i for i, r in enumerate(rows) if r["qtype"] == "noul"]
    F = {"y": np.array([int(rows[i]["gold"]) for i in yn]), "cards": cards[yn]}
    yw = G.permute_labels("yes_no", F, "within", 1001); yg = G.permute_labels("yes_no", F, "global", 2001)
    within_ok = all(yw[F["cards"] == c].sum() == F["y"][F["cards"] == c].sum() for c in set(F["cards"].tolist()))
    out = dict(sha=sha[:16], partitions=len(trs), overlap_or_not_half=bad, equal_to_family_scheme=same,
               yn_within_keeps_card_counts=bool(within_ok), yn_within_changed=float((yw != F["y"]).mean()),
               yn_global_changed=float((yg != F["y"]).mean()), yn_global_same_total=bool(yg.sum() == F["y"].sum()))
    ch = [i for i, r in enumerate(rows) if r["qtype"] != "noul"]
    if ch:
        k = np.array([len(rows[i]["options"]) for i in ch]); gi = np.array([rows[i]["options"].index(rows[i]["gold"]) for i in ch])
        pr = np.repeat(np.arange(len(ch)), k); po = np.concatenate([np.arange(x) for x in k])
        C = {"gi": gi, "k": k, "cards": cards[ch], "pair_row": pr, "pair_opt": po}
        lw = G.permute_labels("choice", C, "within", 1001); lg = G.permute_labels("choice", C, "global", 2001)
        gw = po[lw == 1]; gg = po[lg == 1]
        out.update(ch_one_gold_per_row=bool((np.bincount(pr, weights=lw) == 1).all() and (np.bincount(pr, weights=lg) == 1).all()),
                   ch_within_gold_lt_k=bool((gw < k).all()), ch_within_changed=float((gw != gi).mean()),
                   ch_global_changed=float((gg != gi).mean()), ch_mean_inv_k=float(np.mean(1 / k)),
                   ch_within_same_card_k_hist=bool(all(sorted(gw[(C["cards"] == c) & (k == kk)].tolist()) ==
                                                       sorted(gi[(C["cards"] == c) & (k == kk)].tolist())
                                                       for c, kk in set(zip(C["cards"].tolist(), k.tolist())))))
    res[fam] = out; print(fam, out, flush=True)
Path("part_check.json").write_text(json.dumps(res, indent=1))

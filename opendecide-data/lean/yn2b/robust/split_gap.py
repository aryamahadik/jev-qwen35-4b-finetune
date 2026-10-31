"""Per gate split: accuracy by qtype for 4B-E, 2B pilot (I_1600), 2B REF (v11r); yes/no commitment rate (share
outside 0.2-0.8); choice accuracy by option-count bucket. Read-only analysis of dev splits (never trained on)."""
import json, collections
SPL = "dev_nc,taskbank_dev,hard_dev,dev_negwords,dev_claims,pg_dev,devzs,devp_card,dev".split(",")
M = ["q35_4b_pxE", "q35_2b_armI_1600", "q35_2b_v11r"]
def rd(p): return [json.loads(l) for l in open(p)]
tot = collections.defaultdict(lambda: collections.Counter())
print(f"{'split':14s} {'qt':6s} {'n':>5s} " + " ".join(f"{m[-10:]:>10s}" for m in M) + "   commit(4B/2B/v11r)")
for s in SPL:
    rows = {r["id"]: r for r in rd(f"data/{s}.jsonl")}
    P = {m: {p["id"]: p["probs"] for p in rd(f"preds_{s}/{m}.jsonl")} for m in M}
    for qt in ("noul", "choice"):
        ids = [i for i, r in rows.items() if r["qtype"] == qt and all(i in P[m] for m in M)]
        if not ids: continue
        acc, com = [], []
        for m in M:
            c = k = 0
            for i in ids:
                r, p = rows[i], P[m][i]
                if qt == "noul":
                    g = r["gold"]; py = p["yes"]
                    c += (py >= 0.5) == (g in (1, "yes")); k += not (0.2 < py < 0.8)
                else:
                    c += max(p, key=p.get) == r["gold"]
            acc.append(100 * c / len(ids)); com.append(100 * k / len(ids))
            tot[(m, qt)]["n"] += len(ids); tot[(m, qt)]["c"] += c; tot[(m, qt)]["k"] += k
        print(f"{s:14s} {qt:6s} {len(ids):5d} " + " ".join(f"{a:10.1f}" for a in acc) +
              ("   " + "/".join(f"{x:.0f}" for x in com) if qt == "noul" else ""))
for qt in ("noul", "choice"):
    print("ALL", qt, " ".join(f"{m}: {100*tot[(m,qt)]['c']/tot[(m,qt)]['n']:.1f} (commit {100*tot[(m,qt)]['k']/tot[(m,qt)]['n']:.0f}%)" if qt=='noul' else f"{m}: {100*tot[(m,qt)]['c']/tot[(m,qt)]['n']:.1f}" for m in M), "n", tot[(M[0],qt)]['n'])

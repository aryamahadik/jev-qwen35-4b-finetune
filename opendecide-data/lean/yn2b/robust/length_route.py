"""Indicative only (dev-select half, existing preds): route rows whose state is longer than L chars from the 2B
(I_1600) to 4B-E. Prints routed row share, routed char share and accuracy change vs the 2B alone. The full-length
cascade in FINETUNE_PLAN 5.3 routes on confidence; this is a deterministic length rule."""
import json, hashlib
SPL = "dev_nc,taskbank_dev,hard_dev,dev_negwords,dev_claims,pg_dev,devzs,devp_card,dev".split(",")
half = lambda g: "select" if int(hashlib.sha256(f"devsel:{g}".encode()).hexdigest(), 16) % 2 == 0 else "confirm"
def rd(p): return [json.loads(l) for l in open(p)]
R = []
for s in SPL:
    P = {m: {p["id"]: p["probs"] for p in rd(f"preds_{s}/{m}.jsonl")} for m in ("q35_4b_pxE", "q35_2b_armI_1600")}
    for r in rd(f"data/{s}.jsonl"):
        if r["id"] not in P["q35_4b_pxE"] or s == "taskbank_dev": continue
        ok = {}
        for m, p in ((m, P[m][r["id"]]) for m in P):
            ok[m] = ((p["yes"] >= .5) == (r["gold"] in (1, "yes"))) if r["qtype"] == "noul" else max(p, key=p.get) == r["gold"]
        R.append((half(r.get("group_id", r["id"])), len(r["state"]), ok["q35_4b_pxE"], ok["q35_2b_armI_1600"]))
for H in ("select", "confirm"):
    rows = [x for x in R if x[0] == H]; n = len(rows); ch = sum(x[1] for x in rows)
    base = sum(x[3] for x in rows) / n; b4 = sum(x[2] for x in rows) / n
    print(H, n, f"2B {100*base:.2f}  4B {100*b4:.2f}")
    for L in (1000, 2000, 3000, 4000):
        rt = [x for x in rows if x[1] > L]
        acc = (sum(x[3] for x in rows if x[1] <= L) + sum(x[2] for x in rt)) / n
        print(f"  L>{L}: routed rows {100*len(rt)/n:.1f}%  routed chars {100*sum(x[1] for x in rt)/ch:.1f}%  acc {100*acc:.2f} ({100*(acc-base):+.2f})")

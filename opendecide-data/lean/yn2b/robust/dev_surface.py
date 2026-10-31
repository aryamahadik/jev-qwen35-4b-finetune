"""2B pilot vs 4B-E on the 9 gate dev splits by state length and by surface format, and equiv-pair flip rates.
Read-only analysis; dev splits are never trained on."""
import json, collections, re, sys
sys.path.insert(0, "yn2b/robust")
SPL = "dev_nc,taskbank_dev,hard_dev,dev_negwords,dev_claims,pg_dev,devzs,devp_card,dev".split(",")
M = ["q35_4b_pxE", "q35_2b_armI_1600", "q35_2b_v11r"]
def rd(p): return [json.loads(l) for l in open(p)]
def f(s):
    t = s.lstrip()
    if t.startswith("{") or t.startswith("["): return "json"
    if re.search(r"^\s*\|.*\|\s*$", s, re.M) and s.count("|") > 8: return "md_table"
    if len(re.findall(r"^\s*(\d{4}-\d{2}-\d{2}|\d{1,2}:\d{2})", s, re.M)) >= 4: return "log"
    if re.search(r"^(From|Subject|To):", s, re.M): return "email"
    return "prose"
def lb(n): return "<1k" if n < 1000 else "1-3k" if n < 3000 else "3-6k" if n < 6000 else ">6k"
A = collections.defaultdict(lambda: collections.Counter())
flip = collections.Counter()
for s in SPL:
    rows = {r["id"]: r for r in rd(f"data/{s}.jsonl")}
    P = {m: {p["id"]: p["probs"] for p in rd(f"preds_{s}/{m}.jsonl")} for m in M}
    ans = {}
    for i, r in rows.items():
        if not all(i in P[m] for m in M): continue
        for m in M:
            p = P[m][i]
            if r["qtype"] == "noul":
                a = p["yes"] >= 0.5; ok = a == (r["gold"] in (1, "yes"))
            else:
                a = max(p, key=p.get); ok = a == r["gold"]
            ans[(m, i)] = a
            for key in (("len", r["qtype"], lb(len(r["state"]))), ("fmt", r["qtype"], f(r["state"]))):
                A[key][m + "_c"] += ok; A[key][m + "_n"] += 1
    try:
        for l in open(f"data/{s}_relations.jsonl"):
            x = json.loads(l)
            if x["type"] != "equiv": continue
            for m in M:
                if (m, x["a"]) in ans and (m, x["b"]) in ans:
                    flip[m + "_n"] += 1; flip[m + "_f"] += ans[(m, x["a"])] != ans[(m, x["b"])]
    except FileNotFoundError:
        pass
for k in sorted(A):
    v = A[k]; n = v[M[0] + "_n"]
    if n < 30: continue
    print(k, n, " ".join(f"{m[-9:]}={100*v[m+'_c']/v[m+'_n']:.1f}" for m in M))
print("equiv flip", {m: f"{100*flip[m+'_f']/max(1,flip[m+'_n']):.1f}% of {flip[m+'_n']}" for m in M})

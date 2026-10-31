import json, collections, sys
sys.path.insert(0, ".")
import pilot
d = "families/T32/pilot_i2/"
rows = [json.loads(l) for l in open(d + "rows.jsonl") if l.strip()]
drop = set(json.load(open(d + "g5h/G5H_FINAL.json"))["drop_rows"])
keep = [r for r in rows if r["id"] not in drop]
def L(r): return len(r["state"]) + len(r["card"] or "") + len(r["instructions"] or "")
def stats(rs):
    yn = [r for r in rs if r["qtype"] == "noul"]
    ks = [pilot.negcount.count(r["instructions"]).k_syn for r in yn]
    return {"rows": len(rs), "yn": len(yn), "choice": len(rs) - len(yn), "syn_share": round(sum(k >= 1 for k in ks) / len(yn), 4),
        "dneg_share": round(sum(k >= 2 for k in ks) / len(yn), 4), "dneg_n": sum(k >= 2 for k in ks),
        "mean_chars": round(sum(map(L, rs)) / len(rs), 1),
        "registers": dict(collections.Counter(r["meta"]["c2"]["register"] for r in rs)),
        "cards": len({r["meta"]["card_id"] for r in rs}), "wordings": len({r["meta"].get("wording_id") for r in rs}),
        "qforms": dict(collections.Counter(r["meta"]["qform"] for r in rs)),
        "yes_rate": round(sum(r["gold"] == 1 for r in yn) / len(yn), 4)}
print("ALL ", json.dumps(stats(rows)))
print("KEEP", json.dumps(stats(keep)))

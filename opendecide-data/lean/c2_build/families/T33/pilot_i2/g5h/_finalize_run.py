import json, sys, collections
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build")
from c2_kit import g5h

D = "families/T33/pilot_i2/"
rows = [json.loads(l) for l in open(D + "rows.jsonl") if l.strip()]
rows_by_id = {r["id"]: r for r in rows}
key = json.load(open(D + "g5h/adjudication_key.json"))
vp = json.load(open(D + "g5h/verdicts_first_pass.json"))["verdicts"]
verdicts = {key["key"][aid]: v["verdict"] for aid, v in vp.items()}
res = g5h.finalize(rows_by_id, key["score"], verdicts)
json.dump(res, open(D + "g5h/G5H_FINAL.json", "w"), indent=1)

drop = set(res["drop_rows"])
DNEG = {"yn_dneg_step_ok", "yn_dneg_all_supported"}


def stats(rs):
    yn = [r for r in rs if r["qtype"] == "noul"]
    dn = [r for r in yn if r["meta"]["qform"] in DNEG]
    return {"rows": len(rs), "yes_no": len(yn), "dneg": len(dn),
            "dneg_share": round(len(dn) / len(yn), 4) if yn else None,
            "yes_rate": round(sum(r["gold"] for r in yn) / len(yn), 4) if yn else None}


keep = [r for r in rows if r["id"] not in drop]
out = {"g5h_pass": res["pass"], "drop_rows": len(drop), "before": stats(rows), "after": stats(keep)}
for name, f in [("sampler", lambda r: r["meta"]["sampler"]), ("qform", lambda r: r["meta"]["qform"]),
                ("role", lambda r: r["role"]), ("pack", lambda r: r["meta"]["domain_pack"]),
                ("register", lambda r: r["meta"]["c2"]["register"])]:
    b, a = collections.Counter(map(f, rows)), collections.Counter(map(f, keep))
    out[name] = {k: [b[k], a.get(k, 0)] for k in sorted(b)}
out["qform_lost"] = [k for k in out["qform"] if out["qform"][k][1] == 0]
wc = collections.defaultdict(set)
for r in keep:
    wc[r["meta"]["card_id"]].add(r["meta"].get("wording_id"))
out["wordings_per_card_after"] = {k: len(v) for k, v in sorted(wc.items())}
out["n_wordings_after"] = len({r["meta"].get("wording_id") for r in keep})
out["n_skins_after"] = len({r["meta"]["c2"]["skin_id"] for r in keep})
ids = {r["id"] for r in keep}
orph = [r["id"] for r in keep if r["meta"].get("twin_of") and r["meta"]["twin_of"] not in ids]
out["orphaned_twins"] = len(orph)
out["dropped_by_role"] = dict(collections.Counter(r["role"] for r in rows if r["id"] in drop))
out["dropped_dneg_rows"] = sum(1 for r in rows if r["id"] in drop and r["meta"]["qform"] in DNEG)
json.dump(out, open(D + "g5h/_after_quarantine_stats.json", "w"), indent=1)
print(json.dumps({k: v for k, v in out.items() if k not in ("pack", "register", "wordings_per_card_after")}))
print("cards", out["wordings_per_card_after"], "packs", out["pack"], "regs", out["register"])
print({k: res[k] for k in ("pass", "wrong_gold", "ambiguous", "missing_verdicts", "invalid_verdicts", "ambiguous_rate")})

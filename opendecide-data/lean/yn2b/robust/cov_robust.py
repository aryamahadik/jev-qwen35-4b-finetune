"""Coverage of robustness features in golden_train by source: rows, yes/no share, twin_of, relation types,
state surface format (json / markdown table / log-like / email-like / prose), long states. Read-only."""
import json, collections, re
rel = collections.defaultdict(collections.Counter)
for l in open("data/v14_parts/golden_relations.jsonl"):
    x = json.loads(l); rel[x["a"]][x["type"]] += 1; rel[x["b"]][x["type"] + "_b"] += 1
S = collections.defaultdict(collections.Counter)
fmt = collections.Counter(); fmt_yn = collections.Counter()
glob = collections.Counter()
def f(s):
    t = s.lstrip()
    if t.startswith("{") or t.startswith("["): return "json"
    if re.search(r"^\s*\|.*\|\s*$", s, re.M) and s.count("|") > 8: return "md_table"
    if re.search(r"\t.*\t", s) or re.search(r"^[^\n]*,[^\n]*,[^\n]*\n[^\n]*,[^\n]*,", s): return "csv_tsv"
    if len(re.findall(r"^\s*(\d{4}-\d{2}-\d{2}|\d{1,2}:\d{2}|ev-|e\d+ )", s, re.M)) >= 4: return "log"
    if re.search(r"^(From|Subject|To):", s, re.M): return "email"
    return "prose"
for l in open("data/v14_parts/golden_train.jsonl"):
    r = json.loads(l); s = r["source"]; m = r.get("meta") or {}
    c = S[s]; c["n"] += 1; c["yn"] += r["qtype"] == "noul"; c["twin"] += bool(m.get("twin_of"))
    for k, v in rel.get(r["id"], {}).items(): c[k] += v
    c["long"] += len(r["state"]) > 4000
    ff = f(r["state"]); fmt[ff] += 1
    if r["qtype"] == "noul": fmt_yn[ff] += 1
    glob["n"] += 1; glob["yn"] += r["qtype"] == "noul"; glob["long"] += len(r["state"]) > 4000
    glob["inst_neg"] += bool(re.search(r"\b(not|n't|never|no longer|fail to|without)\b", r["instructions"], re.I)) and r["qtype"] == "noul"
    glob["inj"] += bool(re.search(r"(ignore (all|previous|the above)|system note|SYSTEM:|assistant: answer|answer yes|answer no)", r["state"], re.I))
print("global", dict(glob)); print("formats all", fmt.most_common()); print("formats yes/no", fmt_yn.most_common())
gen = {k: v for k, v in S.items() if k.startswith(("gd_gen", "pg_", "proc", "gd_cst", "gd_ec", "gd_ln", "gd_rk", "gd_rt", "gd_tab"))}
print(f"{'source':34s} {'n':>6s} {'yn':>6s} {'twin':>5s} {'comp':>5s} {'equiv':>5s} {'inv':>5s} {'long':>5s}")
for k, v in sorted(gen.items(), key=lambda kv: -kv[1]["n"]):
    print(f"{k:34s} {v['n']:6d} {v['yn']:6d} {v['twin']:5d} {v['complement']+v['complement_b']:5d} {v['equiv']+v['equiv_b']:5d} {v['inv']+v['inv_b']:5d} {v['long']:5d}")
tot = collections.Counter()
for v in S.values(): tot.update(v)
print("ALL", {k: tot[k] for k in ("n","yn","twin","complement","equiv","inv","long")})

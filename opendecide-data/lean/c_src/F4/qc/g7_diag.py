"""G7 diagnostic (counts only): for choice rows, where an option's text appears verbatim in the record, how often is
that option gold, by form, carrier kind, inert kind and the record context of the match ('whether <opt>' note lines,
attribution prefixes, plain statements)."""
import json, re, sys
from collections import Counter, defaultdict
import qc_lib as L
NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
rows = L.load(NAME)
side = {json.loads(l)["id"]: json.loads(l) for l in open(L.OUT / f"{NAME}.sidecar.jsonl")}
stat = defaultdict(lambda: [0, 0, 0])  # key -> [rows with >=1 verbatim option, rows where a verbatim option is gold, rows]
ctx = Counter(); ctx_gold = Counter()
for r in rows:
    if r["qtype"] == "noul":
        continue
    sc = side[r["id"]]; st = r["state"]; stl = st.lower()
    hits = [i for i, o in enumerate(r["options"]) if len(o) > 12 and o.lower() in stl]
    g = r["options"].index(r["gold"])
    for key in ("all", "form:" + sc["form"], "carrier:" + str(sc["carrier"]), "inert:" + str(sc["inert"]),
                "role:" + r["role"]):
        s = stat[key]; s[2] += 1
        if hits:
            s[0] += 1; s[1] += int(g in hits)
    for i in hits:
        o = r["options"][i].lower(); j = stl.find(o); pre = stl[max(0, j - 40):j]
        c = ("whether-line" if pre.rstrip().endswith("whether") else "attributed" if (":" in pre[-25:] or "reported that" in pre[-20:])
             else "may/appears" if re.search(r"(may|might|appears to) be\s*$", pre) else "plain")
        ctx[c] += 1; ctx_gold[c] += int(i == g)
print(json.dumps({"by": {k: {"rows": v[2], "rows_with_verbatim_option": v[0], "verbatim_option_is_gold": v[1]}
                         for k, v in sorted(stat.items())},
                  "match_context": {k: {"options": ctx[k], "gold": ctx_gold[k]} for k in ctx}}, indent=0))

"""G7 diagnostic 2 (counts only): option whose entity ID is mentioned most / least often in the record vs gold, by form,
inert kind and carrier kind. Unit = rows where the max (min) count is held by a strict subset of options."""
import json, re, sys
from collections import defaultdict
import qc_lib as L
NAME = sys.argv[1] if len(sys.argv) > 1 else "candidates_r1"
rows = L.load(NAME)
side = {json.loads(l)["id"]: json.loads(l) for l in open(L.OUT / f"{NAME}.sidecar.jsonl")}
IDR = re.compile(r"[A-Z]{2}[-/][A-Z0-9]{4,6}")
acc = defaultdict(lambda: {"rows": 0, "gold_in_max": 0, "exp_max": 0.0, "gold_in_min": 0, "exp_min": 0.0})
for r in rows:
    if r["qtype"] == "noul":
        continue
    sc = side[r["id"]]; st = r["state"]
    ids = [IDR.findall(o) for o in r["options"]]
    if not all(ids):
        continue
    cnt = [st.count(x[0]) for x in ids]; k = len(cnt); g = r["options"].index(r["gold"])
    mx, mn = max(cnt), min(cnt)
    if mx == mn:
        continue
    imax = [i for i in range(k) if cnt[i] == mx]; imin = [i for i in range(k) if cnt[i] == mn]
    for key in ("all", "form:" + sc["form"], "form+inert:%s|%s" % (sc["form"], sc["inert"] is not None),
                "form+carrier:%s|%s" % (sc["form"], sc["carrier"])):
        a = acc[key]; a["rows"] += 1
        a["gold_in_max"] += int(g in imax); a["exp_max"] += len(imax) / k
        a["gold_in_min"] += int(g in imin); a["exp_min"] += len(imin) / k
print(json.dumps({k: {**v, "exp_max": round(v["exp_max"], 1), "exp_min": round(v["exp_min"], 1)}
                  for k, v in sorted(acc.items())}, indent=0))

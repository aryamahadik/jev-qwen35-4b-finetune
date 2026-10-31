import json, sys
sys.path.insert(0, ".")
from c2_kit import g5h

base = "families/T15/pilot_i2/"
rows = {}
for line in open(base + "rows.jsonl"):
    line = line.strip()
    if line:
        r = json.loads(line)
        rows[r["id"]] = r
key = json.load(open(base + "g5h/adjudication_key.json"))
fp = json.load(open(base + "g5h/verdicts_first_pass.json"))["verdicts"]
verdicts = {key["key"][aid]: v["verdict"] for aid, v in fp.items()}
res = g5h.finalize(rows, key["score"], verdicts)
json.dump(res, open(base + "g5h/G5H_FINAL.json", "w"), indent=1, default=str)
print(json.dumps({k: (v if not isinstance(v, (list, dict)) or len(str(v)) < 300 else str(v)[:300]) for k, v in res.items()}, indent=1, default=str))

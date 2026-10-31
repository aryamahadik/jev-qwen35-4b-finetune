import json, sys
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build")
from c2_kit import g5h

D = "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build/families/T12/pilot_i1/"
rows = {}
for line in open(D + "rows.jsonl"):
    line = line.strip()
    if line:
        r = json.loads(line)
        rows[r["id"]] = r
key = json.load(open(D + "g5h/adjudication_key.json"))
vs = json.load(open(D + "g5h/verdicts_first_pass.json"))
by_row = {key["key"][aid]: v["verdict"] for aid, v in vs.items()}
assert set(by_row) == set(key["score"]["queue"]) | set(key["score"]["control"])
res = g5h.finalize(rows, key["score"], by_row)
json.dump(res, open(D + "g5h/G5H_FINAL.json", "w"), indent=1)
print(json.dumps({k: (v if k != "drop_rows" else len(v)) for k, v in res.items()}, indent=1))

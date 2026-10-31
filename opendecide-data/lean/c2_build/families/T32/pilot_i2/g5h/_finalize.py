import json, sys
sys.path.insert(0, ".")
from c2_kit import g5h
d = "families/T32/pilot_i2/"
rows = {}
for l in open(d + "rows.jsonl"):
    if l.strip():
        r = json.loads(l); rows[r["id"]] = r
key = json.load(open(d + "g5h/adjudication_key.json"))
fp = json.load(open(d + "g5h/verdicts_first_pass.json"))["verdicts"]
v = {key["key"][a]: x["verdict"] for a, x in fp.items()}
res = g5h.finalize(rows, key["score"], v)
json.dump(res, open(d + "g5h/G5H_FINAL.json", "w"), indent=1)
print({k: res[k] for k in ("pass", "n_read", "queued", "controls", "missing_verdicts", "invalid_verdicts", "wrong_gold", "ambiguous", "ambiguous_rate", "quarantined_templates")}, len(res["drop_rows"]), len(rows))

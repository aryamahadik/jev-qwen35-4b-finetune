"""Generator yes/no rows with 4B-E labels (shards on disk): share of 2B targets inside (0.2, 0.8) under three
policies: A current (kd 0.5 everywhere), B drop the teacher only when it is on the wrong side of gold (the
attacked-twin rule of build_2b_kd, applied to exact-label generator rows), C gold only. Read-only."""
import json, glob, collections
D = "data/v14_label_shards/acct_arya-mahadik-ai/labels_q35_4b_pxE/"
lab = {}
for f in glob.glob(D + "shard_*.jsonl"):
    for l in open(f):
        x = json.loads(l)
        if "yes" in x["probs"]: lab[x["id"]] = float(x["probs"]["yes"])
c = collections.defaultdict(collections.Counter)
for l in open("data/v14_parts/golden_train.jsonl"):
    r = json.loads(l)
    s = r["source"]
    if r["qtype"] != "noul" or r["id"] not in lab or not s.startswith(("gd_gen", "pg_", "proc")): continue
    if isinstance((r.get("meta") or {}).get("teacher"), dict): continue
    g = 1 if r["gold"] == 1 else 0; p = lab[r["id"]]; sg = g * 0.9 + 0.05
    wrong = (p >= 0.5) != (g == 1)
    ya = 0.5 * sg + 0.5 * p
    yb = sg if wrong else ya
    key = s if s.startswith("gd_gen_") else s.split("_")[0]
    for k in (key, "ALL_generators"):
        v = c[k]; v["n"] += 1; v["wrong"] += wrong
        v["midA"] += 0.2 < ya < 0.8; v["midB"] += 0.2 < yb < 0.8
        v["soft_right"] += (not wrong) and 0.2 < p < 0.8
print(f"{'source':26s} {'n':>6s} {'t_wrong':>7s} {'midA':>6s} {'midB':>6s} {'midC':>5s} {'right_but_soft':>14s}")
for k, v in sorted(c.items(), key=lambda kv: -kv[1]["n"]):
    n = v["n"]
    print(f"{k:26s} {n:6d} {v['wrong']/n:7.3f} {v['midA']/n:6.3f} {v['midB']/n:6.3f} {0:5.3f} {v['soft_right']/n:14.3f}")

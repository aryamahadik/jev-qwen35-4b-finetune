"""G5 blind-read renderer (F5 independent checker). Samples 300 rows (seed 5002; repair r2 fresh sample) from out/candidates_r1.jsonl and
writes ONLY the model-visible prompt (decoder_io.user_msg, OD_STYLE=cygnet, LAYOUT=schema_branch_mark, identity perm)
to tmp/chk2/g5_prompts.jsonl as {"k": sample index, "id": row id, "text": prompt}. No gold, no meta."""
import json, os, random, sys
os.environ["OD_STYLE"] = "cygnet"
LEAN = "/Users/aryamahadik/Documents/jev/opendecide-data/lean"
sys.path.insert(0, LEAN)
import decoder_io as dio
dio.LAYOUT = "schema_branch_mark"
F5 = LEAN + "/c_src/F5"
rows = [json.loads(l) for l in open(F5 + "/out/candidates_r1.jsonl")]
idx = random.Random(5002).sample(range(len(rows)), 300)
with open(F5 + "/tmp/chk2/g5_prompts.jsonl", "w") as f:
    for k, i in enumerate(idx):
        r = rows[i]
        f.write(json.dumps({"k": k, "id": r["id"], "text": dio.user_msg(r)}) + "\n")
json.dump({"seed": 5002, "n_pool": len(rows), "method": "random.Random(5002).sample(range(n), 300)",
           "ids": [rows[i]["id"] for i in idx]}, open(F5 + "/qc/g5_r2_sample_ids.json", "w"))
print("wrote", len(idx))

"""G5 blind-read renderer (F7 independent checker; never an F7 generator/solver author). Samples 300 rows (seed 5001)
from out/candidates_r1.jsonl and writes ONLY the model-visible prompt (decoder_io.user_msg, OD_STYLE=cygnet,
LAYOUT=schema_branch_mark) under a seeded random option order (F7 G0 3.5 L13; perm seed 5002) to
tmp/chk/g5_prompts.jsonl as {"k", "id", "perm", "text"}. No gold, no meta."""
import json, os, random, sys
os.environ["OD_STYLE"] = "cygnet"
LEAN = "/Users/aryamahadik/Documents/jev/opendecide-data/lean"
sys.path.insert(0, LEAN)
import decoder_io as dio
dio.STYLE = "cygnet"
dio.LAYOUT = "schema_branch_mark"
F7 = LEAN + "/c_src/F7"
rows = [json.loads(l) for l in open(F7 + "/out/candidates_r1.jsonl")]
idx = random.Random(5001).sample(range(len(rows)), 300)
prng = random.Random(5002)
with open(F7 + "/tmp/chk/g5_prompts.jsonl", "w") as f:
    for k, i in enumerate(idx):
        r = rows[i]; perm = list(range(len(r["options"]))); prng.shuffle(perm)
        f.write(json.dumps({"k": k, "id": r["id"], "perm": perm, "text": dio.user_msg(r, perm)}) + "\n")
json.dump({"seed": 5001, "n_pool": len(rows), "method": "random.Random(5001).sample(range(n), 300)",
           "ids": [rows[i]["id"] for i in idx]}, open(F7 + "/qc/g5_sample_ids.json", "w"))
print("wrote", len(idx))

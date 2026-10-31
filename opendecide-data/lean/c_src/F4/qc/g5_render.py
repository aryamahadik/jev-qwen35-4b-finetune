"""G5 blind read, step 1: sample 300 rows (seed 5001) from out/candidates_r1.jsonl and render ONLY what the model sees
(decoder_io.user_msg, cygnet, schema_branch_mark, canonical option order) into batch files without gold."""
import json, random
import qc_lib as q

rows = q.load("candidates_r1")
ids = sorted(r["id"] for r in rows)
N = 300
pick = random.Random(5001).sample(ids, N)
json.dump(pick, open(q.QC / "g5_sample_ids.json", "w"), indent=0)
by = {r["id"]: r for r in rows}
d = q.TMP / "g5"; d.mkdir(parents=True, exist_ok=True)
B = 2
for b in range(0, N, B):
    with open(d / f"b{b // B:03d}.txt", "w") as f:
        for i in range(b, min(b + B, N)):
            r = by[pick[i]]
            f.write(f"\n######## ROW {i} qtype={r['qtype']}\n")
            f.write(q.model_view(r))
            f.write("\n")
print("rendered", len(pick), "rows in", (N + B - 1) // B, "batches")

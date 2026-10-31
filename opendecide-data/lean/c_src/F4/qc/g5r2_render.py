"""G5 blind read, repair round (seed 5002): sample 300 rows from the REGENERATED out/candidates_r1.jsonl and render
ONLY what the model sees (decoder_io.user_msg, cygnet, schema_branch_mark, canonical option order) into batch files
without gold or any sidecar field. Batches of 5 rows in tmp/checker/g5r2/."""
import json, random
import qc_lib as q

rows = q.load("candidates_r1")
ids = sorted(r["id"] for r in rows)
N = 300
pick = random.Random(5002).sample(ids, N)
json.dump(pick, open(q.QC / "g5r2_sample_ids.json", "w"), indent=0)
by = {r["id"]: r for r in rows}
d = q.TMP / "g5r2"; d.mkdir(parents=True, exist_ok=True)
B = 5
for b in range(0, N, B):
    with open(d / f"b{b // B:03d}.txt", "w") as f:
        for i in range(b, min(b + B, N)):
            r = by[pick[i]]
            f.write(f"\n######## ROW {i} qtype={r['qtype']}\n")
            f.write(q.model_view(r))
            f.write("\n")
print("rendered", len(pick), "rows in", (N + B - 1) // B, "batches")

"""G5 blind read, step 1: sample 600 rows (seed 5001) from out/candidates_r1.jsonl and render ONLY what the model sees
(decoder_io.user_msg, cygnet, schema_branch_mark, canonical option order) into batch files without gold."""
import json, random
import qc_lib as q

rows, _ = q.load("candidates_r1")
ids = sorted(r["id"] for r in rows)
pick = random.Random(5001).sample(ids, 600)
json.dump(pick, open(q.QC / "g5_sample_ids.json", "w"), indent=0)
by = {r["id"]: r for r in rows}
d = q.TMP / "g5"; d.mkdir(parents=True, exist_ok=True)
B = 3
for b in range(0, 600, B):
    with open(d / f"b{b // B:03d}.txt", "w") as f:
        for i in range(b, min(b + B, 600)):
            r = by[pick[i]]
            f.write(f"\n######## ROW {i} id={r['id']} qtype={r['qtype']}\n")
            f.write(q.model_view(r))
            f.write("\n")
print("rendered", len(pick), "rows in", (600 + B - 1) // B, "batches")

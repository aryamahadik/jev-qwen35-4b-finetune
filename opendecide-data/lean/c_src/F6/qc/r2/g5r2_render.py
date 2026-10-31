"""G5 blind read (repair r1), step 1: a fresh 300-row sample (seed 5002) from out/candidates_r1.jsonl, rendered as the
model sees it (decoder_io.user_msg, cygnet, schema_branch_mark, canonical option order), without gold or meta, in
batches of 5. Step 3 (g5r2_score.py) compares the reader's answers with gold."""
import json, random, sys
sys.path.insert(0, "/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F6/qc")
import qc_lib as q

rows, _ = q.load("candidates_r1")
ids = sorted(r["id"] for r in rows)
pick = random.Random(5002).sample(ids, 300)
json.dump(pick, open(q.QC / "r2" / "g5r2_sample_ids.json", "w"), indent=0)
by = {r["id"]: r for r in rows}
d = q.TMP / "g5r2"
d.mkdir(parents=True, exist_ok=True)
B = 5
for b in range(0, 300, B):
    with open(d / f"b{b // B:03d}.txt", "w") as f:
        for i in range(b, min(b + B, 300)):
            r = by[pick[i]]
            f.write(f"\n######## ROW {i}\n")
            f.write(q.model_view(r))
            f.write("\n")
print("rendered", len(pick), "rows in", (300 + B - 1) // B, "batches")

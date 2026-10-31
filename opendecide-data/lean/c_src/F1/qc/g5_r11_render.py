"""G5 fresh blind read after the r1.1 repair: sample 300 rows (seed 5002) from out/candidates_r1.jsonl and render ONLY
the model view (decoder_io.user_msg, cygnet, schema_branch_mark, canonical option order), no gold, 3 rows per file."""
import json, random
import qc_lib as q

rows, _ = q.load("candidates_r1")
ids = sorted(r["id"] for r in rows)
pick = random.Random(5002).sample(ids, 300)
json.dump(pick, open(q.QC / "g5_r11_sample_ids.json", "w"), indent=0)
by = {r["id"]: r for r in rows}
d = q.TMP / "g5_r11"; d.mkdir(parents=True, exist_ok=True)
B = 4
for b in range(0, 300, B):
    with open(d / f"b{b // B:03d}.txt", "w") as f:
        for i in range(b, min(b + B, 300)):
            r = by[pick[i]]
            f.write(f"\n######## ROW {i} qtype={r['qtype']}\n")
            f.write(q.model_view(r))
            f.write("\n")
print("rendered", len(pick))

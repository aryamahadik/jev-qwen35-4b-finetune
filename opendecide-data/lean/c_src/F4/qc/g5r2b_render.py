"""G5 repair round, r1b top-up (seed 5002 kept): after the r1b regeneration (CW flip twins) 293 of the 300 seed-5002
sample rows are byte-identical in what the model sees (answers carry over); the 4 changed rows are re-read and the 3
rows whose ids left the set are replaced by seed-5002 draws from the final ids not in the sample. Also a targeted
read of 20 rows that changed in r1b (seed 5003). Renders only what the model sees, in batches of 5 (tmp/checker/g5r2b/)."""
import json, random, hashlib
import qc_lib as q

rows = {r["id"]: r for r in q.load("candidates_r1")}
ids = json.load(open(q.QC / "g5r2_sample_ids.json"))
pre = json.load(open(q.F4 / "tmp/repair/g5r2_viewhash_preflip.json"))
old_all = json.load(open(q.F4 / "tmp/repair/cand_rowhash_preflip.json"))
vh = lambda r: hashlib.sha256((q.model_view(r) + "\x00" + json.dumps(r["gold"])).encode()).hexdigest()
keep, reread, gone = [], [], []
for i, rid in enumerate(ids):
    if rid not in rows:
        gone.append(i)
    elif vh(rows[rid]) == pre[rid]:
        keep.append(i)
    else:
        reread.append(i)
pool = sorted(set(rows) - set(ids))
repl = random.Random(5002).sample(pool, len(gone))
final_ids = list(ids)
for i, rid in zip(gone, repl):
    final_ids[i] = rid
allh = {k: hashlib.sha256(json.dumps(v, sort_keys=True).encode()).hexdigest()[:16] for k, v in rows.items()}
changed = sorted(k for k in rows if old_all.get(k) != allh[k] and k not in final_ids)
extra = random.Random(5003).sample(changed, min(20, len(changed)))
todo = [(i, final_ids[i]) for i in sorted(reread + gone)] + [(300 + j, rid) for j, rid in enumerate(extra)]
json.dump({"final_ids": final_ids, "kept_positions": keep, "reread_positions": reread, "replaced_positions": gone,
           "extra_changed_ids": extra, "todo": todo}, open(q.QC / "g5r2b_plan.json", "w"), indent=0)
d = q.TMP / "g5r2b"; d.mkdir(parents=True, exist_ok=True)
for b in range(0, len(todo), 5):
    with open(d / f"b{b // 5:03d}.txt", "w") as f:
        for i, rid in todo[b:b + 5]:
            f.write(f"\n######## ROW {i} qtype={rows[rid]['qtype']}\n")
            f.write(q.model_view(rows[rid]))
            f.write("\n")
print(json.dumps({"kept": len(keep), "reread": len(reread), "replaced": len(gone), "extra": len(extra), "todo": len(todo),
                  "batches": (len(todo) + 4) // 5, "changed_pool": len(changed)}))

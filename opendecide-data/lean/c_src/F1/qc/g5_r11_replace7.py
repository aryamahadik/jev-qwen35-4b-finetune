"""G5 r1.1, after pass 7 (the 17 Q2 cards were regenerated again): keep the sampled rows from the other cards (checked
unchanged by model-view hash against the pass-6 snapshot) and replace the sampled rows from the regenerated cards
with a seed-5002 draw from those cards' new rows. Renders ONLY the model view (no gold) for the replacements.
Counts only on stdout."""
import json, random, re, hashlib, shutil
import qc_lib as q

CARDS = {"F1-C006", "F1-C007", "F1-C011", "F1-C012", "F1-C015", "F1-C020", "F1-C041", "F1-C043", "F1-C044", "F1-C049",
         "F1-C058", "F1-C078", "F1-C093", "F1-C095", "F1-C107", "F1-C108", "F1-C110"}
card = lambda x: re.search(r"(F1-C\d+)", x).group(1)

rows, _ = q.load("candidates_r1")
by = {r["id"]: r for r in rows}
old = json.load(open(q.TMP / "g5_r11_sample_ids.pass6.json"))
snap = {s["i"]: s for s in json.load(open(q.TMP / "g5_r11_pass6_snapshot.json"))}
q2 = [i for i, x in enumerate(old) if card(x) in CARDS]
changed = []
for i, x in enumerate(old):
    if i in q2:
        continue
    r = by.get(x)
    if r is None or hashlib.sha1(q.model_view(r).encode()).hexdigest() != snap[i]["h"] or r["gold"] != snap[i]["gold"]:
        changed.append(i)
pool = sorted(r["id"] for r in rows if card(r["id"]) in CARDS)
rep = random.Random(5002).sample(pool, len(q2))
new = list(old)
for i, x in zip(q2, rep):
    new[i] = x
json.dump(new, open(q.QC / "g5_r11_sample_ids.json", "w"), indent=0)
json.dump(q2, open(q.TMP / "g5_r11_p7_idx.json", "w"))
d = q.TMP / "g5_r11_p7r"; d.mkdir(parents=True, exist_ok=True)
for f in d.glob("b*.txt"):
    f.unlink()
B = 4
for b in range(0, len(q2), B):
    with open(d / f"b{b // B:03d}.txt", "w") as f:
        for i in q2[b:b + B]:
            r = by[new[i]]
            f.write(f"\n######## ROW {i} qtype={r['qtype']}\n")
            f.write(q.model_view(r))
            f.write("\n")
# drop any answers previously given for the replaced indices (pass-3 rows) from the answer file (backup kept)
ap = q.TMP / "g5_r11_answers.jsonl"
shutil.copy(ap, q.TMP / "g5_r11_answers.pass6b.jsonl")
keep = [l for l in open(ap) if json.loads(l)["i"] not in set(q2)]
open(ap, "w").writelines(keep)
print(json.dumps({"kept_rows": 300 - len(q2), "kept_changed_after_pass7": changed, "replaced": len(q2),
                  "pool_rows_regenerated_cards": len(pool), "answers_kept": len(keep),
                  "replacement_files": (len(q2) + B - 1) // B,
                  "replacement_qtypes": dict(__import__("collections").Counter(by[new[i]]["qtype"] for i in q2))}))

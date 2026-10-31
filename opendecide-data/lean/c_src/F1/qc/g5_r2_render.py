"""G5 blind read (check:F1, workflow c-lanes-v3): sample 600 rows (seed 5001) from out/candidates_r1.jsonl and render
ONLY the model view (decoder_io.user_msg, cygnet + schema_branch_mark, canonical option order). No gold, no meta.
Token saving only (no content removed): the card block, when it is a verbatim part of the view, is printed once per
distinct text in tmp/qc/g5_r2/cards.txt and referenced as [CARD Cn]; the instructions + options block that the layout
repeats verbatim after the text is printed once (its first copy is replaced by a marker after an exact-match check).
Writes qc/g5_r2_sample_ids.json and tmp/qc/g5_r2/bNNN.txt (10 rows per file). Prints counts only."""
import hashlib, json, random
import qc_lib as q

rows, _ = q.load("candidates_r1")
ids = sorted(r["id"] for r in rows)
pick = random.Random(5001).sample(ids, 600)
json.dump(pick, open(q.QC / "g5_r2_sample_ids.json", "w"), indent=0)
by = {r["id"]: r for r in rows}
d = q.TMP / "g5_r2"; d.mkdir(parents=True, exist_ok=True)
cards, n_card, n_dedup = {}, 0, 0
B = 10
for b in range(0, 600, B):
    with open(d / f"b{b // B:03d}.txt", "w") as f:
        for i in range(b, min(b + B, 600)):
            r = by[pick[i]]
            m = q.model_view(r)
            c = r.get("card") or ""
            if c and c in m:
                h = hashlib.sha1(c.encode()).hexdigest()
                if h not in cards:
                    cards[h] = (f"C{len(cards)}", c)
                m = m.replace(c, f"[CARD {cards[h][0]}]", 1); n_card += 1
            t = m.find("\nText:\n")
            if t > 0:
                head, tail = m[:t], m[t:]
                ins = r["instructions"].strip()
                k = head.find(ins) if ins else -1
                if k >= 0 and ins in tail:
                    m = head[:k] + "[QUESTION+OPTIONS: see the copy after the text]" + tail
                    n_dedup += 1
            f.write(f"\n######## ROW {i}\n{m}\n")
with open(d / "cards.txt", "w") as f:
    for h, (cid, c) in cards.items():
        f.write(f"\n######## {cid}\n{c}\n")
print(json.dumps({"rendered": len(pick), "rows_with_card_ref": n_card, "distinct_cards": len(cards),
                  "question_block_dedup": n_dedup, "files": 600 // B}))

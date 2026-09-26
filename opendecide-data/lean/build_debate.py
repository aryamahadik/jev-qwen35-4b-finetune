"""Debate-outcome rows from public Wikipedia deletion discussions (research-dump/wiki-stance-en: one row per comment,
the comment's stance label, vote words already stripped from the text). Comments are grouped into discussions; only
discussions with >= 3 comments and a clear majority (>= 70% delete-side or >= 70% keep-side) are used, gold = the
majority side (the skill: infer each participant's stance from the argument, then aggregate).
Every article title in our jagged eval set is excluded. Writes data/debate_train.jsonl.
"""
import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

from datasets import load_dataset

HERE = Path(__file__).resolve().parent
rng = random.Random(20260928)
norm = lambda t: re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()
held = set()
for l in open(HERE / "data/eval_jagged.jsonl"):
    r = json.loads(l)
    held.add(norm(str((r.get("meta") or {}).get("item_id", "")).split("afd:", 1)[-1]))
    held.add(norm(r["group_id"].split("afd:", 1)[-1]))
d = load_dataset("research-dump/wiki-stance-en", split="train")
disc = defaultdict(list)
for x in d:
    disc[x["title"]].append(x)
DEL, KEEP = {"delete", "speedy delete", "redirect", "merge"}, {"keep", "speedy keep"}
QS = [("Based on the discussion, was the article deleted (or merged/redirected away)?", 1),
      ("Based on the discussion, was the article kept?", 0),
      ("Did the deletion discussion end with the article being removed as a standalone page?", 1)]
rows, skipped = [], Counter()
titles = list(disc)
rng.shuffle(titles)
for t in titles:
    if len(rows) >= 2400:
        break
    name = t.split("/", 1)[-1]
    if norm(name) in held:
        skipped["held_out_title"] += 1
        continue
    cs = [c for c in disc[t] if c["comment"] and len(c["comment"]) > 25]
    if not 3 <= len(cs) <= 14:
        continue
    dels = sum(c["decision"].lower() in DEL for c in cs)
    keeps = sum(c["decision"].lower() in KEEP for c in cs)
    if dels + keeps < 3 or max(dels, keeps) < 0.7 * (dels + keeps):
        continue
    deleted = dels > keeps
    cs.sort(key=lambda c: c["timestamp"] or "")
    body = "\n".join(f"* {c['comment'].strip()} [[{c['username']}]] {c['timestamp']}" for c in cs)
    st = json.dumps({"page": f"Articles for deletion/{name}", "discussion": body, "participants": f"{len(cs)} editors"},
                    ensure_ascii=False, indent=1)
    if len(st) > 9000:
        continue
    q, pos = rng.choice(QS)
    gold = int(deleted) if pos == 1 else int(not deleted)
    i = len(rows)
    rows.append({"id": f"r_debate_{i}", "group_id": f"g:debate:{i}", "call_id": f"c_debate_{i}", "split": "train",
                 "track": "DEBATE", "source": "wiki_stance_afd", "state": st, "qtype": "noul", "instructions": q,
                 "options": None, "gold": gold, "role": "aff", "meta": {"anchor": False, "deleted": deleted}})
(HERE / "data/debate_train.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
print(len(rows), "rows; deleted share", round(sum(r["meta"]["deleted"] for r in rows) / len(rows), 3), dict(skipped))

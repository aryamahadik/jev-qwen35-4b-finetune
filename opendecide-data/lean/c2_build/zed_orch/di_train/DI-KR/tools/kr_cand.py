"""DI-KR candidates (A42-D 1.3: <= 1.5 x 2,400 = 3,600) and own dev (300): from the seed-20261013 train build; stratified by gold numeric rank
(900 per rank, seeded). Own dev = the 300 held-out problems built the same way (sampler S5, dev_only). Usage: python -I -B kr_cand.py"""
import gzip, json, sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from kr_rows import *

rows, drops = build(SEED, "train")
dev, ddrops = build(SEED, "dev")
by = {}
for r in rows:
    by.setdefault(r["meta"]["di_kr"]["gold_rank"], []).append(r)
cand = []
for k in range(4):
    cand += sorted(by[k], key=lambda r: h(SEED, "cand", r["id"]))[:900]
cand.sort(key=lambda r: h(SEED, "order", r["id"])); dev.sort(key=lambda r: h(SEED, "order", r["id"]))
for name, rs in (("candidates", cand), ("owndev", dev), ("full_train_build", rows)):
    with open(WORK / f"{name}.jsonl", "w", encoding="utf-8") as f:
        for r in rs: f.write(json.dumps(r, ensure_ascii=False) + "\n")
pop = KR / "screen/pool"; pop.mkdir(parents=True, exist_ok=True)
with gzip.open(pop / "population.jsonl.gz", "wt", encoding="utf-8") as f:
    for r in cand + dev: f.write(json.dumps(r, ensure_ascii=False) + "\n")
st = {"full_train_build": len(rows), "build_drops": drops, "candidates": len(cand), "owndev": len(dev), "dev_drops": ddrops,
      "overlap_cand_dev": len({r["meta"]["di_kr"]["pid"] for r in cand} & {r["meta"]["di_kr"]["pid"] for r in dev}),
      "cand_rank": dict(Counter(r["meta"]["di_kr"]["gold_rank"] for r in cand)), "cand_pos": dict(Counter(r["options"].index(r["gold"]) for r in cand)),
      "wordings": dict(Counter(r["meta"]["wording_id"] for r in cand))}
json.dump(st, open(WORK / "rows_stats.json", "w"), indent=1); print(json.dumps(st))

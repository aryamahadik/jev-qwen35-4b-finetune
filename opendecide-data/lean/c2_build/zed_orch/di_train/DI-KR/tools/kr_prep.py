"""DI-KR prep: GSM8K main train (7,473) -> gold check (AST, drop only) -> exact + near-duplicate drop -> positive-integer gold
-> own dev (300, seeded, drawn before any read) -> work/pool.json. Run: python -I -B kr_prep.py  (counts only)."""
import json, sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from kr_lib import *

rows = [json.loads(l) for l in open(SRC / "train.jsonl", encoding="utf-8")]
drops = Counter(); kept = []
seen_exact, inv, segs = {}, {}, []
for i, o in enumerate(rows):
    pid = f"gsm8k_train_{i:05d}"
    q = " ".join(o["question"].split())
    ok, why, info = check_problem(o["answer"])
    if not ok:
        drops["gold_check:" + why] += 1; continue
    gv = parse_num(info["gold"])
    if gv.denominator != 1 or gv <= 0:
        drops["gold_not_positive_integer"] += 1; continue
    tok = norm_tokens(q); key = " ".join(tok)
    if key in seen_exact:
        drops["exact_duplicate"] += 1; continue
    g = grams(tok); near = False
    cand = set()
    for x in g:
        cand |= inv.get(x, set())
    for j in cand:
        sg = segs[j]; inter = len(g & sg)
        if inter / max(1, len(g | sg)) >= 0.8:
            near = True; break
    if near:
        drops["near_duplicate"] += 1; continue
    seen_exact[key] = pid
    segs.append(g)
    for x in g:
        inv.setdefault(x, set()).add(len(segs) - 1)
    g_int = int(gv)
    vals = sorted({int(v) for v in info["vals"] if v.denominator == 1 and v > 0 and int(v) != g_int})
    kept.append({"pid": pid, "idx": i, "question": q, "gold": g_int, "hard": vals, "qhash": sha(q)[:16], "n_ann": len(info["vals"])})
dev = sorted(kept, key=lambda r: h(SEED, "dev", r["pid"]))[:300]
dev_ids = sorted(r["pid"] for r in dev)
out = {"source_rows": len(rows), "kept": kept, "dev_ids": dev_ids, "drops": dict(drops),
       "pins": {"train_sha256": sha((SRC / "train.jsonl").read_bytes())}}
json.dump(out, open(WORK / "pool.json", "w"))
print(json.dumps({"source_rows": len(rows), "kept": len(kept), "dev": len(dev_ids), "train_build": len(kept) - len(dev_ids), "drops": dict(drops),
                  "no_hard_pool": sum(1 for r in kept if not r["hard"]), "mean_hard": round(sum(len(r["hard"]) for r in kept) / len(kept), 2)}))

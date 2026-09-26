"""v0.11b fix-up stage (continue from the v0.10 x v0.11 blend q35_4b_v11s30): remove the one-sided bias on two-option
judgments (over-flagging offence, lenient factual consistency) without losing v0.11's gains.
  binj_train (x2)  Claude-written balanced binary judgments with minimal-pair twins (build_v11_binj.py)
  judge_train      all judge-the-response rows (strictness)
  replay           a v0.11 sample by block (task bank, hard items, negation, claims, intents, reasoning)
Writes data/train_v11b.jsonl + data/train_v11b_relations.jsonl.
"""
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
D, P = HERE / "data", HERE / "data/v11_parts"
rj = lambda p: [json.loads(l) for l in open(p)] if Path(p).exists() else []
rng = random.Random(20261003)


def take_units(rows, n):
    u = defaultdict(list)
    for r in rows:
        u[r["call_id"]].append(r)
    us = list(u.values())
    rng.shuffle(us)
    out = []
    for x in us:
        if len(out) >= n:
            break
        out.extend(x)
    return out


def main():
    binj = rj(P / "binj_train.jsonl")
    v11 = rj(D / "train_v11.jsonl")
    v11_ids = {r["id"] for r in v11}  # only rows that passed v0.11's held-out/dev overlap filter
    parts = {k: [r for r in rj(P / f"{k}_train.jsonl") if r["id"] in v11_ids] for k in ("taskbank", "hard", "negation", "claims", "intent")}
    in_parts = {r["id"] for v in parts.values() for r in v}
    in_parts |= {i + "_x2" for i in in_parts}
    other = [r for r in v11 if r["id"] not in in_parts]  # judge/lah/debate/pg/ohr/v0.7 classification/meta replay
    replay = (take_units(parts["taskbank"], 3000) + take_units(parts["hard"], 1800) + take_units(parts["negation"], 1500)
              + take_units(parts["claims"], 1000) + take_units(parts["intent"], 700) + take_units(other, 1500))
    rows = binj + [{**r, "id": r["id"] + "_x2", "call_id": r["call_id"] + "_x2"} for r in binj] + rj(D / "judge_train.jsonl") + replay
    rows = list({r["id"]: r for r in rows}.values())
    ids = {r["id"] for r in rows}
    rels = rj(D / "train_v11_relations.jsonl") + rj(D / "judge_train_relations.jsonl")
    rels = [x for x in {(x["type"], x["a"], x["b"]): x for x in rels}.values() if x["a"] in ids and x["b"] in ids]
    (D / "train_v11b.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    (D / "train_v11b_relations.jsonl").write_text("".join(json.dumps(x) + "\n" for x in rels))
    print(json.dumps({"rows": len(rows), "binj": len(binj), "relations": dict(Counter(x["type"] for x in rels)),
                      "by_source_top": Counter(r["source"] for r in rows).most_common(12)}, indent=1))


if __name__ == "__main__":
    main()

"""Compact mix for the small-model pilots (same recipe at 0.8B / 2B, taught by v0.10): a stratified sample of the
final v0.10 training data (v0.7 core mix + LLM-authored hard items + judge rows + debates), whole call units kept so
negation/paraphrase/attack twins and their relations stay together. Writes data/train_pilot.jsonl + relations.
  python build_pilot_mix.py [n_rows]
"""
import json
import random
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = HERE / "data"
rj = lambda p: [json.loads(l) for l in open(p)]
SHARE = {"L0": 0.22, "L2": 0.12, "L3": 0.16, "PG": 0.12, "OHR": 0.08, "LAH": 0.10, "JUDGE": 0.12, "DEBATE": 0.08}


def main(n=12000, seed=12):
    r = random.Random(seed)
    rows = rj(D / "train_v07.jsonl") + rj(D / "lah_train.jsonl") + rj(D / "judge_train.jsonl") + rj(D / "debate_train.jsonl")
    rows = list({x["id"]: x for x in rows}.values())  # train_v07 already holds the 9 pilot LLM-authored items
    rels = rj(D / "train_v07_relations.jsonl") + rj(D / "judge_train_relations.jsonl")
    by_call = {}
    for x in rows:
        by_call.setdefault(x["call_id"], []).append(x)
    rank = {"L3": 0, "JUDGE": 1, "DEBATE": 2, "LAH": 3, "PG": 4, "OHR": 5, "L2": 6, "L0": 7}
    pools = {}
    for u in by_call.values():
        tr = min((y["track"] for y in u), key=lambda t: rank.get(t, 9))
        pools.setdefault(tr, []).append(u)
    out = []
    for tr, share in SHARE.items():
        us = pools.get(tr, [])
        r.shuffle(us)
        got = []
        for u in us:
            if len(got) >= share * n:
                break
            got.extend(u)
        out += got
    ids = {x["id"] for x in out}
    assert len(ids) == len(out), "duplicate ids"
    rel = list({(x["type"], x["a"], x["b"]): x for x in rels if x["a"] in ids and x["b"] in ids}.values())
    (D / "train_pilot.jsonl").write_text("".join(json.dumps(x) + "\n" for x in out))
    (D / "train_pilot_relations.jsonl").write_text("".join(json.dumps(x) + "\n" for x in rel))
    print(json.dumps({"rows": len(out), "relations": len(rel), "by_track": dict(Counter(x["track"] for x in out))}))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 12000)

"""Stage-2 set (continue training q35_4b_v07): LLM-authored hard items (2x) + a replay sample of v0.7 so nothing is
forgotten (procedural, open reasoning, injection/meta, anchored classification). Relations kept for replayed rows.
Writes data/train_v08s2.jsonl + data/train_v08s2_relations.jsonl.   python build_train_v08.py [replay_n]
"""
import json
import random
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = HERE / "data"
rj = lambda p: [json.loads(l) for l in open(p)]


def main(replay_n=6000, seed=8):
    r = random.Random(seed)
    v07, rel07 = rj(D / "train_v07.jsonl"), rj(D / "train_v07_relations.jsonl")
    lah = rj(D / "lah_train.jsonl")
    lah = lah + [{**x, "id": x["id"] + "_x2", "call_id": x["call_id"] + "_x2"} for x in lah]
    quota = {"PG": 0.25, "OHR": 0.2, "L3": 0.2, "L0": 0.25, "L2": 0.1}
    by_call = {}
    for x in v07:
        if x["track"] != "LAH":
            by_call.setdefault(x["call_id"], []).append(x)
    # a unit = every row of one call (clean twin + injected copies + negations), filed under its most specific track
    rank = {"L3": 0, "PG": 1, "OHR": 2, "L2": 3, "L0": 4}
    units = {(min((y["track"] for y in u), key=lambda t: rank.get(t, 9)), c): u for c, u in by_call.items()}
    replay = []
    for tr, q in quota.items():
        us = [u for (t, _), u in units.items() if t == tr]
        r.shuffle(us)
        got = []
        for u in us:  # whole call units, so paired rows (and their relations) stay together
            if len(got) >= q * replay_n:
                break
            got.extend(u)
        replay += got
    ids = {x["id"] for x in replay}
    rels = [x for x in rel07 if x["a"] in ids and x["b"] in ids]
    rows = lah + replay
    assert len({x["id"] for x in rows}) == len(rows)
    (D / "train_v08s2.jsonl").write_text("".join(json.dumps(x) + "\n" for x in rows))
    (D / "train_v08s2_relations.jsonl").write_text("".join(json.dumps(x) + "\n" for x in rels))
    print(json.dumps({"rows": len(rows), "lah": len(lah), "replay": len(replay), "relations": len(rels),
                      "by_track": dict(Counter(x["track"] for x in rows))}))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 6000)

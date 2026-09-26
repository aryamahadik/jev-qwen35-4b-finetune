"""Stage-4 set (continue training q35_4b_v09): debate-outcome rows (build_debate.py) + replay of the stage-3 set
(judge, LLM-authored hard items, v0.7 sample). Writes data/train_v10s4.jsonl + data/train_v10s4_relations.jsonl."""
import json
import random
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = HERE / "data"
rj = lambda p: [json.loads(l) for l in open(p)]


def main(replay_n=3500, seed=10):
    r = random.Random(seed)
    new = rj(D / "debate_train.jsonl")
    s3, s3rel = rj(D / "train_v09s3.jsonl"), rj(D / "train_v09s3_relations.jsonl")
    by_call = {}
    for x in s3:
        by_call.setdefault(x["call_id"], []).append(x)
    units = list(by_call.values())
    r.shuffle(units)
    replay = []
    for u in units:
        if len(replay) >= replay_n:
            break
        replay.extend(u)
    have = {x["id"] for x in replay}
    v07, rel07 = rj(D / "train_v07.jsonl"), rj(D / "train_v07_relations.jsonl")  # keep injection robustness: 800 more
    c07 = {}                                                                      # injection / claim-check rows (L3)
    for x in v07:
        c07.setdefault(x["call_id"], []).append(x)
    l3 = [u for u in c07.values() if any(y["track"] == "L3" for y in u) and not any(y["id"] in have for y in u)]
    r.shuffle(l3)
    extra = []
    for u in l3:
        if len(extra) >= 800:
            break
        extra.extend(u)
    replay += extra
    ids = {x["id"] for x in replay}
    rows = new + replay
    rels = [x for x in s3rel + rel07 if x["a"] in ids and x["b"] in ids]
    rels = list({(x["type"], x["a"], x["b"]): x for x in rels}.values())
    assert len({x["id"] for x in rows}) == len(rows)
    (D / "train_v10s4.jsonl").write_text("".join(json.dumps(x) + "\n" for x in rows))
    (D / "train_v10s4_relations.jsonl").write_text("".join(json.dumps(x) + "\n" for x in rels))
    print(json.dumps({"rows": len(rows), "new": len(new), "replay": len(replay), "relations": len(rels),
                      "by_track": dict(Counter(x["track"] for x in rows))}))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 3500)

"""Stage-3 set (continue training q35_4b_v08): 'judge the response' rows (build_judge.py) + replay of the stage-2 set
(LLM-authored hard items + v0.7 sample) so earlier gains are kept.
Writes data/train_v09s3.jsonl + data/train_v09s3_relations.jsonl.   python build_train_v09.py [replay_n]
"""
import json
import random
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = HERE / "data"
rj = lambda p: [json.loads(l) for l in open(p)]


def main(replay_n=5000, seed=9):
    r = random.Random(seed)
    judge, jrel = rj(D / "judge_train.jsonl"), rj(D / "judge_train_relations.jsonl")
    s2, s2rel = rj(D / "train_v08s2.jsonl"), rj(D / "train_v08s2_relations.jsonl")
    by_call = {}
    for x in s2:
        by_call.setdefault(x["call_id"], []).append(x)
    units = list(by_call.values())
    r.shuffle(units)
    replay = []
    for u in units:
        if len(replay) >= replay_n:
            break
        replay.extend(u)
    ids = {x["id"] for x in replay}
    rows = judge + replay
    rels = jrel + [x for x in s2rel if x["a"] in ids and x["b"] in ids]
    assert len({x["id"] for x in rows}) == len(rows)
    (D / "train_v09s3.jsonl").write_text("".join(json.dumps(x) + "\n" for x in rows))
    (D / "train_v09s3_relations.jsonl").write_text("".join(json.dumps(x) + "\n" for x in rels))
    print(json.dumps({"rows": len(rows), "judge": len(judge), "replay": len(replay), "relations": len(rels),
                      "by_track": dict(Counter(x["track"] for x in rows))}))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 5000)

"""Mix-tuning dev items (spec section 10): from the S5 build (held-out packs, held-out styles, S5 only) pick
  - the depth sweep: 5 depth levels {1, 2, 3-4, 5-6, 7-8} x 60 items (S5 only; B14, C13), and
  - 400 family items, from groups not used by the sweep, spread over question types.
Base rows are preferred (twins only to fill). Writes out/mixdev_S5.jsonl (+ sidecar) with meta.edge tags
'dev:depth_sweep:<level>' / 'dev:family'."""
from __future__ import annotations

import collections
import json
import random
import sys

LEVELS = (("1", (1,)), ("2", (2,)), ("3-4", (3, 4)), ("5-6", (5, 6)), ("7-8", (7, 8)))
QT_TARGET = {"Q1": 0.16, "Q2": 0.15, "Q3": 0.15, "Q4": 0.22, "Q5": 0.12, "Q6": 0.05, "Q7": 0.10, "Q8": 0.05}


def main(src, dst, per_level=60, n_family=400, seed=20261003):
    rows = [json.loads(l) for l in open(src)]
    side = {json.loads(l)["id"]: json.loads(l) for l in open(src[:-6] + ".sidecar.jsonl")}
    rng = random.Random(seed)
    rng.shuffle(rows)
    rows.sort(key=lambda r: r["meta"]["twin_of"] is not None)  # base rows first, stable otherwise
    used_groups, pick = set(), []
    report = {}
    for lev, depths in LEVELS:
        got = []
        per_group = collections.Counter()
        for r in rows:
            if r["meta"]["depth"] in depths and per_group[r["group_id"]] < 2 and r["id"] not in {x["id"] for x in pick}:
                got.append(r)
                per_group[r["group_id"]] += 1
                if len(got) >= per_level:
                    break
        for r in got:
            r["meta"]["edge"] = list(r["meta"]["edge"]) + [f"dev:depth_sweep:{lev}"]
            used_groups.add(r["group_id"])
        report[lev] = len(got)
        pick += got
    rest = [r for r in rows if r["group_id"] not in used_groups]
    by_qt = collections.defaultdict(list)
    for r in rest:
        by_qt[side[r["id"]]["qt"]].append(r)
    fam = []
    want = {q: int(round(n_family * v)) for q, v in QT_TARGET.items()}
    for q, n in want.items():
        fam += by_qt.get(q, [])[:n]
    left = [r for r in rest if r not in fam]
    fam += left[:max(0, n_family - len(fam))]
    for r in fam[:n_family]:
        r["meta"]["edge"] = list(r["meta"]["edge"]) + ["dev:family"]
    pick += fam[:n_family]
    report["family"] = min(n_family, len(fam))
    report["family_by_qt"] = dict(collections.Counter(side[r["id"]]["qt"] for r in fam[:n_family]))
    with open(dst, "w") as f:
        for r in pick:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(dst[:-6] + ".sidecar.jsonl", "w") as f:
        for r in pick:
            f.write(json.dumps(side[r["id"]], ensure_ascii=False) + "\n")
    ids = {r["id"] for r in pick}
    rels = [json.loads(l) for l in open(src[:-6] + ".relations.jsonl")]
    with open(dst[:-6] + ".relations.jsonl", "w") as f:
        for x in rels:
            if x["a"] in ids and x["b"] in ids:
                f.write(json.dumps(x) + "\n")
    print(json.dumps(report))
    return report


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])

"""Merge build shards into the F8 outputs (whole selection units only; never row by row).

out/candidates_r1.jsonl   round-1 candidate pool, exactly 3,375 rows (1.5 x 2,250; training samplers S1-S4)
out/qc_sample.jsonl       separate G6 QC sample, >= 5,000 rows, no structure shared with the candidates
out/mixdev_S5.jsonl       S5 mix-tuning dev items, 400 (held-out sampler, packs and styles; never trained)
Sidecars (G0 spec 12): out/f8_controls_<name>.jsonl; relations: out/relations_<name>.jsonl.
"""
from __future__ import annotations

import collections
import glob
import json
import sys

import cards as CP
import common as CM

NAMES = {"cand": "candidates_r1", "qc": "qc_sample", "dev": "mixdev_S5"}
TARGET = {"cand": CP.CANDIDATE_TOTAL, "qc": 5000, "dev": CP.S5_TOTAL}


def load(mode: str):
    rows, sides, rels, units, stats = [], [], [], [], []
    # repair r2: a patch shard (build.py --cards) replaces every row of its cards in the regular shards
    patch = CM.TMP / "shards" / f"{mode}_shardpatch.rows.jsonl"
    pcards = {r["meta"]["card_id"] for r in CM.read_jsonl(patch)} if patch.exists() else set()
    for p in sorted(glob.glob(str(CM.TMP / "shards" / f"{mode}_shard*.rows.jsonl"))):
        base = p[:-len(".rows.jsonl")]
        rr = CM.read_jsonl(p)
        if pcards and not base.endswith("_shardpatch"):
            gone = {r["id"] for r in rr if r["meta"]["card_id"] in pcards}
        else:
            gone = set()
        rows += [r for r in rr if r["id"] not in gone]
        sides += [x for x in CM.read_jsonl(base + ".side.jsonl") if x["id"] not in gone]
        rels += [x for x in CM.read_jsonl(base + ".rels.jsonl") if x["a"] not in gone and x["b"] not in gone]
        st = json.load(open(base + ".stats.json"))
        units += [u for u in st["units"] if not set(u) & gone]
        stats.append(st)
    if pcards:
        print(f"patch shard replaces cards {sorted(pcards)}")
    return rows, sides, rels, units, stats


def unit_of(units):
    m = {}
    for u in units:
        for rid in u:
            m[rid] = tuple(u)
    return m


def main(mode: str, exclude_hashes: set | None = None):
    rows, sides, rels, units, stats = load(mode)
    rid = {r["id"]: r for r in rows}
    um = unit_of(units)
    # 1. structure dedup across shards and against excluded hashes: drop whole units (planned negation units share
    #    one problem hash inside the unit, which is allowed)
    seen = {}
    drop = set()
    for u in units:
        hs = {rid[x]["meta"]["structure_hash"] for x in u}
        clash = any(h in seen and seen[h] != tuple(u) for h in hs) or bool(exclude_hashes and hs & exclude_hashes)
        if clash:
            drop |= set(u)
            continue
        for h in hs:
            seen[h] = tuple(u)
    # 2. trim to the target with whole single-row units (largest cards first), never below 10 rows a card
    keep = [r for r in rows if r["id"] not in drop]
    target = TARGET[mode]
    if mode == "qc":
        target = max(target, 0)
        excess = 0
    per_card = collections.Counter(r["meta"]["card_id"] for r in keep)
    excess = len(keep) - target if mode != "qc" else 0
    if excess < 0:
        print(f"SHORT: {mode} has {len(keep)} rows < {target}")
    singles = sorted([u for u in units if len(u) == 1 and u[0] not in drop],
                     key=lambda u: (-per_card[rid[u[0]]["meta"]["card_id"]], u[0]))
    i = 0
    while excess > 0 and i < len(singles):
        u = singles[i]
        cid = rid[u[0]]["meta"]["card_id"]
        if per_card[cid] > 10:
            drop.add(u[0])
            per_card[cid] -= 1
            excess -= 1
        i += 1
    keep = [r for r in rows if r["id"] not in drop]
    ks = {r["id"] for r in keep}
    sides_k = [x for x in sides if x["id"] in ks]
    rels_k = [x for x in rels if x["a"] in ks and x["b"] in ks]
    name = NAMES[mode]
    CM.write_jsonl(CM.OUT / f"{name}.jsonl", keep)
    CM.write_jsonl(CM.OUT / f"f8_controls_{name}.jsonl", sides_k)
    CM.write_jsonl(CM.OUT / f"relations_{name}.jsonl", rels_k)
    units_k = [u for u in units if all(x in ks for x in u)]
    with open(CM.TMP / f"units_{name}.json", "w") as f:
        json.dump(units_k, f)
    agg = collections.Counter()
    pf = collections.Counter()
    mr = collections.Counter()
    for st in stats:
        agg.update(st["stats"])
        pf.update(st["parse_fail"])
        for k, v in st["mr"]:
            mr[json.dumps(k)] += v
    with open(CM.TMP / f"buildstats_{name}.json", "w") as f:
        json.dump({"rows": len(keep), "dropped": len(drop), "stats": dict(agg), "parse_fail": dict(pf),
                   "mr": dict(mr), "examples": [st["examples"] for st in stats]}, f, indent=1)
    CM.progress(f"merge {mode}: {len(keep)} rows -> out/{name}.jsonl (dropped {len(drop)} whole-unit rows; "
                f"parse_fail during build {sum(pf.values())})")
    return keep


if __name__ == "__main__":
    mode = sys.argv[1]
    excl = None
    if mode == "qc":
        excl = {r["meta"]["structure_hash"] for r in CM.read_jsonl(CM.OUT / "candidates_r1.jsonl")}
    main(mode, excl)

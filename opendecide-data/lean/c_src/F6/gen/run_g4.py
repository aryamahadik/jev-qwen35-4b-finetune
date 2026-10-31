"""Run the G4 metamorphic relations on >= 1,000 rows per sampler (all rows when fewer) of one output set.

  python -m gen.run_g4 <set> [--per 1000]
"""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import random
from collections import Counter, defaultdict

from . import common as C
from .common import OUT, TMP, read_jsonl, progress

NAMES = {"cand": "candidates_r1", "qc": "qc_sample", "dev": "mixdev_S5"}
_W = {}


def _init():
    from . import styles_f6 as ST
    _W["W"] = {w["text"] for w in ST.wording_pool()}


def _one(args):
    row, side = args
    from . import g4
    rng = random.Random(f"g4:{row['id']}")
    try:
        return row["id"], row["meta"]["sampler"], g4.run_row(row, side, _W["W"], rng)
    except Exception as e:  # noqa: BLE001
        return row["id"], row["meta"]["sampler"], {"error": f"{type(e).__name__}:{str(e)[:80]}"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("set")
    ap.add_argument("--per", type=int, default=1000)
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()
    base = NAMES[a.set]
    rows = read_jsonl(OUT / f"{base}.jsonl")
    side = {s["id"]: s for s in read_jsonl(OUT / f"{base}.qc_side.jsonl")}
    struct = {s["id"]: s["struct"] for s in read_jsonl(TMP / f"{base}.struct.jsonl")}
    by = defaultdict(list)
    for r in rows:
        by[r["meta"]["sampler"]].append(r)
    jobs = []
    rng = random.Random(f"g4pick:{a.set}")
    for smp, rs in sorted(by.items()):
        pick = rs if len(rs) <= a.per else rng.sample(rs, a.per)
        for r in pick:
            s = dict(side[r["id"]])
            s["struct"] = struct[r["id"]]
            jobs.append((r, s))
    out = []
    with mp.get_context("fork").Pool(a.workers, initializer=_init) as pool:
        for x in pool.imap_unordered(_one, jobs, chunksize=8):
            out.append(x)
    summ = defaultdict(Counter)
    fails = []
    for rid, smp, res in out:
        for rel, v in res.items():
            k = "pass" if v == "pass" else ("skip" if v == "skip" else "fail")
            summ[(smp, rel)][k] += 1
            if k == "fail":
                fails.append({"id": rid, "rel": rel, "why": v})
    rep = {"set": a.set, "rows_tested": len(jobs), "per_sampler_rows": dict(Counter(smp for _, smp, _ in out)),
           "by_sampler_relation": {f"{s}|{r}": dict(c) for (s, r), c in sorted(summ.items())},
           "relations": sorted({r for _, r in summ}), "fail_total": len(fails)}
    json.dump(rep, open(TMP / f"g4_{a.set}.json", "w"), indent=1)
    json.dump(fails, open(TMP / f"g4_{a.set}_fails.json", "w"), indent=1)
    progress(f"G4 {a.set}: {len(jobs)} rows tested over {len(rep['relations'])} relations; failures {len(fails)}")
    print(json.dumps(rep, indent=1)[:3000])


if __name__ == "__main__":
    main()

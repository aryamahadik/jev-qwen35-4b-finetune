"""Tiny dry run: build 20 examples IN MEMORY with the TEST pool and proxy names, for unit tests and eyeballing the
generator. It never writes a file (a test patches open() to prove it) and refuses a production pool. These are not
rows: the pool is a test fixture, names come from the native TRAINING-salt namespace kinds (L-0 added every kind); a proxy-named row is refused.

    python -m t41c.dryrun            # prints one summary line per example
    python -m t41c.dryrun --show 3   # also prints the flattened text of the first 3 examples
"""
import argparse
import collections
import json
import sys

from . import build, planner, pools
from .spec import label_of


def build_examples(n=20, seed="dry1", pool=None):
    pool = pool or pools.make_test_pool(per_cell=8, seed=3)
    if pool.kind != pools.KIND_TEST:
        raise SystemExit("dryrun uses the test pool only")
    # plan a little more than n so that a dropped group still leaves n
    specs, rep = planner.plan_specs(max(40, n * 3), seed=seed, block="train", proxy_names=False)
    rows, br = build.build_rows(specs, pool, proxy_names=False)
    ex = []
    seen = set()
    for s, r in rows:                      # take whole pair groups so the minimal-pair structure is visible
        if s.group_id in seen:
            continue
        seen.add(s.group_id)
        members = [(s2, r2) for s2, r2 in rows if s2.group_id == s.group_id]
        if len(ex) + len(members) > n:
            continue
        ex += members
        if len(ex) >= n:
            break
    return ex[:n], br


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--show", type=int, default=0)
    a = ap.parse_args(argv)
    ex, br = build_examples(20)
    print("# dry run: %d in-memory examples (test pool, proxy names; NOT rows)" % len(ex))
    for i, (s, r) in enumerate(ex):
        print(json.dumps({"id": s.row_id, "label": label_of(s), "bucket": s.subtype, "kind": s.pair_kind + "/" + s.pair_role,
                          "carrier": s.carrier_type, "fmt": s.carrier_format, "facts": s.facts_flag(),
                          "spans": len(r.spans), "anchors": len(r.anchors), "proxy_names": r.proxy_names}))
        if i < a.show:
            print(r.flat())
    print("# labels:", dict(collections.Counter(label_of(s) for s, _ in ex)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

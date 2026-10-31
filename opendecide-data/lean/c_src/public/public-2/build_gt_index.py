"""Build the golden_train dedup index for public-2 (spec 3.1: unused records only; named-source passage dedup).

Reads only `state` of data/v14_parts/golden_train.jsonl (allow-listed). Writes tmp/gt_index.npz (hashes only).
"""
import json
import sys
import time

import numpy as np

from p2_common import GOLDEN_TRAIN, NAMED_DEDUP_SOURCES, TMP, h64, ngrams, text_units, log_progress


def main():
    t0 = time.time()
    units, grams = [], []
    n = 0
    with open(GOLDEN_TRAIN) as f:
        for line in f:
            r = json.loads(line)
            st = r.get("state") or ""
            units.extend(h64(u) for u in set(text_units(st)))
            if r.get("source") in NAMED_DEDUP_SOURCES:
                grams.extend(h64(g) for g in set(ngrams(st, 10)))
            n += 1
            if n % 100000 == 0:
                print(n, len(units), len(grams), round(time.time() - t0), file=sys.stderr, flush=True)
    u = np.unique(np.array(units, dtype=np.int64))
    g = np.unique(np.array(grams, dtype=np.int64))
    np.savez(TMP / "gt_index.npz", units=u, grams=g)
    msg = f"gt_index: {n} golden_train rows, {len(u)} unique line/sentence hashes, {len(g)} named-source 10-gram hashes, {round(time.time() - t0)} s"
    print(msg)
    log_progress(msg)


if __name__ == "__main__":
    main()

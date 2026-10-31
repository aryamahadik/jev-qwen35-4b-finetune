#!/usr/bin/env python3
"""Index C1's golden_train (allow-listed replay file) for the per-paragraph near-duplicate filter (review item 3):
sorted unique word 10-gram hashes of every row's state, instructions, card and option strings (lib/grams.py).
Output tmp/golden_g10.npy (hashes only, no text). Deleted after the build like the sentence index."""
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "lib"))
from grams import gram_hashes  # noqa: E402

GT = HERE.parents[2] / "data" / "v14_parts" / "golden_train.jsonl"
t0 = time.time()
chunks, buf, n = [], [], 0
with open(GT) as f:
    for line in f:
        r = json.loads(line)
        texts = [r.get("state") or "", r.get("instructions") or "", r.get("card") or ""]
        texts += [o for o in (r.get("options") or []) if isinstance(o, str)]
        for t in texts:
            if t:
                g = gram_hashes(t)
                if g.size:
                    buf.append(g)
        n += 1
        if n % 20000 == 0:
            chunks.append(np.unique(np.concatenate(buf)))
            buf = []
            print(n, sum(c.size for c in chunks), round(time.time() - t0), flush=True)
if buf:
    chunks.append(np.unique(np.concatenate(buf)))
a = np.unique(np.concatenate(chunks))
np.save(HERE / "tmp" / "golden_g10.npy", a)
print("rows", n, "unique_10grams", a.size, "secs", round(time.time() - t0), flush=True)

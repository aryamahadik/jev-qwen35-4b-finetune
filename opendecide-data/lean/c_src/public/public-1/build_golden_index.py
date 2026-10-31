#!/usr/bin/env python3
"""Index C1's golden_train (allow-listed, replay file) for the spec 3.1 dedupe: sorted uint64 xxh64 hashes of every
normalised sentence (>= 8 words) and every normalised full `state`, over all rows; plus the same restricted to the 7
passage sources named in spec 3.1 (qnli, gd_answer_equiv, gd_hotpotqa_yesno, gd_feverous, gd_totto_claims, gd_wtq,
boolq). Reads only state + instructions. Output tmp/golden_index.npz (hashes only, no text).
v1.2 (repair round 1, A29 a): also `line_all`, the hash of every normalised line (split on newlines) of every state
and instructions with >= 6 words, so a shown line equal to a golden_train state unit is caught even when the sentence
splitter cuts it into pieces under 8 words."""
import json, sys
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "lib"))
from textnorm import sent_hashes, norm, h64
GT = HERE.parents[2] / "data" / "v14_parts" / "golden_train.jsonl"
NAMED = {"qnli", "gd_answer_equiv", "gd_hotpotqa_yesno", "gd_feverous", "gd_totto_claims", "gd_wtq", "boolq"}
sa, fa, sn, la = [], [], [], []
n = 0
with open(GT) as f:
    for line in f:
        r = json.loads(line)
        st = r.get("state") or ""
        ins = r.get("instructions") or ""
        hs = sent_hashes(st) + sent_hashes(ins)
        sa.extend(hs)
        fa.append(h64(norm(st)))
        for ln in (st + "\n" + ins).split("\n"):
            nl = norm(ln)
            if nl.count(" ") + 1 >= 6:
                la.append(h64(nl))
        if r.get("source") in NAMED:
            sn.extend(hs)
        n += 1
        if n % 100000 == 0:
            print(n, len(sa), flush=True)
np.savez(HERE / "tmp" / "golden_index.npz", sent_all=np.unique(np.array(sa, dtype=np.uint64)),
         full_all=np.unique(np.array(fa, dtype=np.uint64)), sent_named=np.unique(np.array(sn, dtype=np.uint64)),
         line_all=np.unique(np.array(la, dtype=np.uint64)))
print("rows", n, "sent_all", len(set(sa)), "named", len(set(sn)), "lines", len(set(la)), flush=True)

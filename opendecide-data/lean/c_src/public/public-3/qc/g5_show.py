#!/usr/bin/env python3
"""Show G5 sample rows to the flag-only reader, as the model sees them (qc/g5_render.jsonl: decoder_io.user_msg in
the C round-1 style, gold as displayed). One row per output line; newlines shown as ' | '. A prompt line of >= 30
characters that was already shown for this dataset is printed as §n (its first showing is tagged §n=). The cygnet
system prompt is the same for every row and is not repeated; display drops (lossless for judging) a line repeated
inside the row, the untrusted-text markers and the fixed closing lines (the question and options are shown above). Usage: g5_show.py DATASET START END"""
import json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ds, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
rows = [json.loads(l) for l in open(HERE / "g5_render.jsonl")]
rows = [r for r in rows if r["dataset"] == ds]
seen = {}
for j, r in enumerate(rows[:b]):
    parts, inrow = [], set()
    for ln in r["prompt"].split("\n"):
        if ln in inrow or ln.startswith("<<<UNTRUSTED TEXT") or ln.startswith("(The text between") \
                or ln.startswith("Question (answer using") or ln.startswith("Answer with the letter") \
                or ln.startswith("Options: A."):
            if ln not in seen and len(ln) >= 30:
                seen[ln] = len(seen) + 1
            continue                     # display only: a repeat inside the row, the fixed markers / closing lines
        inrow.add(ln)
        if len(ln) >= 30 and ln in seen:
            parts.append(f"§{seen[ln]}")
        elif len(ln) >= 30:
            seen[ln] = len(seen) + 1
            parts.append(f"§{seen[ln]}={ln}" if j >= a else ln)
        else:
            parts.append(ln)
    if j >= a:
        print(f"#{j} GOLD[{r['gold_shown']}] " + " | ".join(p for p in parts if p.strip()))

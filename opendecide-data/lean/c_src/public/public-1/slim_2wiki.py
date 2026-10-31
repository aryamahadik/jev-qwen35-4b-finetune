#!/usr/bin/env python3
"""Stream raw/2wiki/train.json (one JSON array) and keep only comparison and bridge_comparison items (spec 3.2 #3)
as tmp/2wiki_cmp_train.jsonl. Streaming raw_decode keeps memory low."""
import json, sys, collections
from pathlib import Path
HERE = Path(__file__).resolve().parent
src = HERE / "raw/2wiki/train.json"; out = HERE / "tmp/2wiki_cmp_train.jsonl"
dec = json.JSONDecoder(); cnt = collections.Counter()
with open(src, encoding="utf-8") as f, open(out, "w") as o:
    buf = f.read(1 << 22); pos = buf.index("[") + 1
    while True:
        while pos < len(buf) and buf[pos] in " \r\n\t,":
            pos += 1
        if pos >= len(buf) - 1 or buf[pos] != "{":
            more = f.read(1 << 22)
            if not more:
                break
            buf = buf[pos:] + more; pos = 0
            continue
        try:
            obj, end = dec.raw_decode(buf, pos)
        except json.JSONDecodeError:
            more = f.read(1 << 22)
            if not more:
                break
            buf = buf[pos:] + more; pos = 0
            continue
        pos = end
        cnt[obj.get("type")] += 1
        if obj.get("type") in ("comparison", "bridge_comparison"):
            o.write(json.dumps(obj, ensure_ascii=False) + "\n")
        if pos > (1 << 23):
            buf = buf[pos:]; pos = 0
print(json.dumps(cnt), flush=True)

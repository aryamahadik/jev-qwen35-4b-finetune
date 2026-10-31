"""formats-2: drop every record the sealed checker flagged (tmp/sealed/hits.json, ids and kinds only) from
records/<scheme>.jsonl. The drop is permanent for this build; the dropped ids go to tmp/sealed/dropped_records.json."""
from __future__ import annotations

import json

from common_f2 import HERE, progress, write_json, write_jsonl


def main():
    hits = json.load(open(HERE / "tmp" / "sealed" / "hits.json"))
    dropped = {}
    for key, v in hits.items():
        if not key.startswith("records/") or not v["hits"]:
            continue
        ids = {h["id"] for h in v["hit_ids"]}
        p = HERE / key
        rows = [json.loads(l) for l in open(p)]
        keep = [r for r in rows if r["id"] not in ids]
        write_jsonl(p, keep)
        dropped[key] = {"dropped": len(rows) - len(keep), "ids": sorted(ids),
                        "kinds": [h["kinds"] for h in v["hit_ids"]]}
    prev = {}
    dp = HERE / "tmp" / "sealed" / "dropped_records.json"
    if dp.exists():
        prev = json.load(open(dp))
    for k, v in dropped.items():
        prev.setdefault(k, {"dropped": 0, "ids": [], "kinds": []})
        prev[k]["ids"] = sorted(set(prev[k]["ids"]) | set(v["ids"]))
        prev[k]["dropped"] = len(prev[k]["ids"])
        prev[k]["kinds"] += v["kinds"]
    write_json(dp, prev)
    progress("drop_sealed_hits: " + json.dumps({k: v["dropped"] for k, v in prev.items()}))


if __name__ == "__main__":
    main()

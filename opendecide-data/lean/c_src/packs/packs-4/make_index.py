#!/usr/bin/env python3
"""packs-4: write packs_index.jsonl (one summary line per pack; no pack text beyond title and deciding role) from
packs.jsonl. Added in fix round 1 so the index is rebuilt by program; output is byte-identical to the first index."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    packs = [json.loads(l) for l in (HERE / "packs.jsonl").read_text().splitlines() if l.strip()]
    with (HERE / "packs_index.jsonl").open("w") as fh:
        for p in packs:
            fh.write(json.dumps({"id": p["id"], "title": p["title"], "theme": p["theme"],
                                 "persona_seed": p["persona_seed"], "onet_title": p["persona"]["onet_title"],
                                 "major_group": p["persona"]["major_group"],
                                 "deciding_role": p["persona"]["deciding_role"], "split_hint": p["split_hint"],
                                 "date_window": [p["date_window"]["start"], p["date_window"]["end"]],
                                 "n_entity_types": len(p["entity_types"]), "n_bool_fields": len(p["bool_fields"]),
                                 "n_jargon": len(p["jargon"])}, ensure_ascii=False) + "\n")
    print("wrote packs_index.jsonl", len(packs))


if __name__ == "__main__":
    main()

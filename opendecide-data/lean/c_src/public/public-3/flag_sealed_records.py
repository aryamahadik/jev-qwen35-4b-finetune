#!/usr/bin/env python3
"""public-3 v1.1 (review-public3 fix 5): flag sealed-suite record hits as sealed_drop.

Sources (ids and hit kinds only; no text, no matched terms):
  - public-3's own records check: tmp/records_sealed/<scheme>.sealedqc.jsonl (run_sealed_records.sh runs
    lean/sealed_nd/qc/sealed_check.py as a program on tmp/records/<scheme>.jsonl; blocking hits only, report-only kinds
    are not hits);
  - formats-2's record drops: c_src/formats/formats-2/tmp/sealed/dropped_records.json (the same record ids; formats-2
    scans the unredacted text, so it can hit where public-3's placeholder text does not).
Writes:
  - tmp/records/<scheme>.jsonl: flags.sealed_drop (bool) on every record; eligible recomputed (a sealed_drop record is
    never eligible). build_rows.load removes sealed_drop records after its shuffle, so v1.0's draw order is kept.
  - out/public3_split_3e.jsonl: "sealed_drop" (bool) on every record, and "sealed_drop_by" (sources) on the flagged
    ones: F10 / F11 and every other consumer of the shared split file must skip them.
  - logs/sealed_drop_ids.json, and the sealed_drop counts, record-file and split-file sha256 in logs/records_stats.json.
Idempotent."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "lib"))
from common3 import LEAN, LOGS, OUT, REC, TMP, progress, safe_in, sha_file, write_jsonl  # noqa: E402

SCHEMES = ("xed", "mams_acsa", "mams_atsa", "ghc", "edos", "sarcasm_v2")
SUITE = "f4ae863720535b6ba27acad51917fe07b4d31344228a1dddb9d98bc3a4deac68"
F2_DROPS = LEAN / "c_src" / "formats" / "formats-2" / "tmp" / "sealed" / "dropped_records.json"


def kind(k):
    return k.get("kind") if isinstance(k, dict) else k


def main():
    by: dict[str, dict] = {}
    own = {}
    for s in SCHEMES:
        summ = json.load(open(TMP / "records_sealed" / f"{s}.summary.json"))
        assert summ.get("suite_sha256") == SUITE, (s, "suite sha")
        n = hits = 0
        with open(TMP / "records_sealed" / f"{s}.sealedqc.jsonl") as f:
            for line in f:
                o = json.loads(line)
                n += 1
                if o.get("hit"):
                    hits += 1
                    by.setdefault(o["id"], {"sources": [], "kinds": []})
                    by[o["id"]]["sources"].append("public3_records_check")
                    by[o["id"]]["kinds"] += [kind(k) for k in o.get("hit_kinds") or []]
        own[s] = {"rows": n, "hit_rows": hits, "checker_sha256": summ.get("checker_sha256"),
                  "input_sha256": summ.get("input_sha256")}
    f2 = json.load(open(safe_in(F2_DROPS)))
    for key, v in f2.items():
        for i, rid in enumerate(v["ids"]):
            by.setdefault(rid, {"sources": [], "kinds": []})
            by[rid]["sources"].append("formats2_records_check")
            by[rid]["kinds"] += list(v["kinds"][i]) if i < len(v.get("kinds", [])) else []
    for v in by.values():
        v["sources"] = sorted(set(v["sources"]))
    stats = json.loads((LOGS / "records_stats.json").read_text())
    found = set()
    for s in SCHEMES:
        p = REC / f"{s}.jsonl"
        rows = [json.loads(l) for l in open(p, encoding="utf-8")]
        c = Counter()
        for r in rows:
            fl = r["flags"]
            fl["sealed_drop"] = r["id"] in by
            found.update([r["id"]] if fl["sealed_drop"] else [])
            r["eligible"] = not any(v for k, v in fl.items() if k != "outlet_redacted")
            c["sealed_drop"] += fl["sealed_drop"]
            c[f"sealed_drop_{r['part']}"] += fl["sealed_drop"]
            c[f"eligible_{r['part']}"] += r["eligible"]
        sh = write_jsonl(p, rows)
        st = stats["schemes"][s]
        st.update({"sealed_drop": c["sealed_drop"], "eligible_train": c["eligible_train"],
                   "eligible_dev": c["eligible_dev"], "sha256": sh})
    missing = sorted(set(by) - found)
    assert not missing, f"sealed ids not in public-3 records: {missing}"
    sp = OUT / "public3_split_3e.jsonl"
    split = [json.loads(l) for l in open(sp, encoding="utf-8")]
    n_flag = 0
    for r in split:
        r.pop("sealed_drop_by", None)
        r["sealed_drop"] = r["id"] in by
        if r["sealed_drop"]:
            r["sealed_drop_by"] = by[r["id"]]["sources"]
            n_flag += 1
    stats["split_file_sha256"] = write_jsonl(sp, split)
    stats["sealed_drop"] = {"rule": "a record hit by the id-only sealed checker (blocking kinds) in public-3's own "
                                    "records check or in formats-2's records check is sealed_drop: never eligible, "
                                    "flagged in the shared split file",
                            "ids": {k: by[k] for k in sorted(by)}, "own_check": own,
                            "formats2_drops_file_sha256": sha_file(F2_DROPS), "split_rows_flagged": n_flag}
    (LOGS / "records_stats.json").write_text(json.dumps(stats, indent=1))
    (LOGS / "sealed_drop_ids.json").write_text(json.dumps({k: by[k] for k in sorted(by)}, indent=1))
    progress(f"flag_sealed_records: {len(by)} sealed_drop records flagged (records + split file); "
             f"own check hits {sum(v['hit_rows'] for v in own.values())}, formats-2 drops "
             f"{sum(len(v['ids']) for v in f2.values())}")


if __name__ == "__main__":
    main()

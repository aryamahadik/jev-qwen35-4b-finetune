"""OWNER ONLY. The OHS-3 12-gram check (SPEC 7.1 / PREREG_OHS3 rule 1) on the WHOLE fix2 training file, counts only.

Build agents never run this: it is the one step that opens data/ohs3.jsonl. It covers every row of
data/v14_parts/fix2_train.jsonl (the F7 part and the golden replay; part (ii) is empty in the built file, A8-prime C.2),
which is wider than f7_precheck.py --ohs3-blind (item 8.13, the F7 part only).

It reuses yn2b/check_yn2b.ohs3_blind unchanged: the OHS-3 file is read there, into memory, hashed into 12-grams and
deleted before the function returns. This script prints only counts (hit units per source, total) and never a text,
id, row or hash of an OHS-3 item.

  cd lean && PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python extra/fix2_ohs3_blind.py --i-am-the-owner \
      --out yn2b/fix2_ohs3_blind.json

--out writes the same counts-only JSON (plus the UTC time) to a file, which is committed with A8-prime (C.6 (e): the
owner's whole-file result is recorded, not only printed).

Exit 0 when 0 units hit (the top-up may train), 1 when any unit hits (do not launch; rebuild without those units),
2 when the OHS-3 file is missing (the check did not run), 3 without --i-am-the-owner (nothing was opened).
"""
import argparse
import hashlib
import json
import sys
import time
from collections import Counter
from pathlib import Path

LEAN = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(LEAN / "yn2b"))
sys.path.insert(0, str(LEAN))
TRAIN = LEAN / "data/v14_parts/fix2_train.jsonl"
COUNTS = LEAN / "data/v14_parts/fix2_counts.json"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--i-am-the-owner", action="store_true", help="required: this opens data/ohs3.jsonl")
    ap.add_argument("--out", default=None, help="also write the counts-only result here (yn2b/fix2_ohs3_blind.json)")
    a = ap.parse_args()
    if not a.i_am_the_owner:
        print("OWNER ONLY: pass --i-am-the-owner. Build agents never run this file.", file=sys.stderr)
        sys.exit(3)
    want = json.loads(COUNTS.read_text())["files"]["v14_parts/fix2_train.jsonl"]
    got = hashlib.sha256(TRAIN.read_bytes()).hexdigest()
    if got != want:
        raise SystemExit(f"fix2_train.jsonl sha256 {got[:12]}... is not fix2_counts.json's {want[:12]}...")
    import check_yn2b as cy
    rows = []
    for line in open(TRAIN):
        r = json.loads(line)
        r["meta"] = dict(r.get("meta") or {})
        r["meta"]["latent_id"] = r["meta"].get("latent_id") or r.get("call_id")  # unit = ladder or call
        rows.append(r)
    units, _hashes, _names, loaded = cy.ohs3_blind(LEAN, rows, ())
    when = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    if not loaded:
        res = {"check": "fix2 OHS-3 12-gram", "loaded": False, "rows": len(rows), "fix2_train_sha256": got,
               "result": "NOT RUN (data/ohs3.jsonl missing)", "utc": when}
        code = 2
    else:
        total = sum(units.values())
        res = {"check": "fix2 OHS-3 12-gram (SPEC 7.1, PREREG_OHS3 rule 1)", "loaded": True,
               "fix2_train_sha256": got, "rows": len(rows), "hit_units_total": total,
               "hit_units_by_source": dict(Counter(units).most_common()),
               "result": "PASS" if total == 0 else "FAIL", "utc": when, "run_by": "owner (--i-am-the-owner)"}
        code = 0 if total == 0 else 1
    blob = json.dumps(res, indent=1)
    print(blob)
    if a.out:
        Path(a.out).write_text(blob + "\n")
        print(f"wrote {a.out} (sha256 {hashlib.sha256((blob + chr(10)).encode()).hexdigest()})", file=sys.stderr)
    sys.exit(code)


if __name__ == "__main__":
    main()

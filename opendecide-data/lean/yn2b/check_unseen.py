"""check_unseen.py: SPEC.md section 7.4. The ship rule's unseen-source set must not move when the yn2b training file
is added to the training files it is derived from.

Calls gate_dev.derive_unseen(SPLITS, list(gate_dev.TRAIN_FILES) + ["v14_parts/yn2b_train"]) and asserts:
  - the unseen set equals gate_dev.UNSEEN_FROZEN_ROWS (17 sources, 3,847 rows);
  - overlap["flagged"] == {} (no unseen-source dev row's text is in a training row);
  - no gd_gen3_* source name matches a dev source under gate_dev.source_seen (in either direction);
  - the yn2b file really was read (derive_unseen reports a missing file otherwise).
It never writes ship_unseen_sources.json (it calls derive_unseen only, never write_unseen) and writes nothing else.
Exit 0 = pass, 1 = fail.

  ../.venv/bin/python yn2b/check_unseen.py                                  # the SPEC call
  ../.venv/bin/python yn2b/check_unseen.py --yn2b-file v14_parts/yn2b_ab/some_file   (no .jsonl)
  ../.venv/bin/python yn2b/check_unseen.py --yn2b-file ''                   # baseline: the 12 registered files only
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import yn2b_common as yc  # noqa: E402

N_SOURCES, N_ROWS = 17, 3847


def check(yn2b_file="v14_parts/yn2b_train", root=None):
    import gate_dev
    if root is not None:
        gate_dev.ROOT = Path(root)
    splits = gate_dev.SPLITS.split(",")
    files = list(gate_dev.TRAIN_FILES) + ([yn2b_file] if yn2b_file else [])
    d = gate_dev.derive_unseen(splits, files)
    res = {"train_files": files, "problems": []}
    if d["unseen"] is None:
        res["problems"].append(f"data/{d['missing']}.jsonl is missing: nothing was derived")
        return res
    rows = {s: v["rows"] for s, v in d["unseen"].items()}
    res["unseen_sources"], res["unseen_rows"] = len(rows), sum(rows.values())
    res["overlap"] = {k: v for k, v in d["overlap"].items() if k != "flagged"}
    res["flagged"] = {s: len(v) for s, v in d["overlap"]["flagged"].items()}
    if rows != gate_dev.UNSEEN_FROZEN_ROWS:
        res["problems"].append(f"unseen set differs from UNSEEN_FROZEN_ROWS: added {sorted(set(rows) - set(gate_dev.UNSEEN_FROZEN_ROWS))}, "
                               f"removed {sorted(set(gate_dev.UNSEEN_FROZEN_ROWS) - set(rows))}, changed "
                               f"{ {s: [gate_dev.UNSEEN_FROZEN_ROWS[s], rows[s]] for s in set(rows) & set(gate_dev.UNSEEN_FROZEN_ROWS) if rows[s] != gate_dev.UNSEEN_FROZEN_ROWS[s]} }")
    if (len(rows), sum(rows.values())) != (N_SOURCES, N_ROWS):
        res["problems"].append(f"{len(rows)} sources / {sum(rows.values())} rows, expected {N_SOURCES} / {N_ROWS}")
    if d["overlap"]["flagged"]:
        res["problems"].append(f"text guard flags {res['flagged']}")
    if yn2b_file:
        p = gate_dev.ROOT / f"data/{yn2b_file}.jsonl"
        gen3 = sorted({r["source"] for r in yc.iter_jsonl(p)})
        res["yn2b_sources"] = gen3
        dev_sources = sorted(d["dev"])
        clash = {s: gate_dev.source_seen(s, gen3) for s in dev_sources if gate_dev.source_seen(s, gen3)}
        clash.update({g: hits for g in gen3 if (hits := gate_dev.source_seen(g, dev_sources))})
        if clash:
            res["problems"].append(f"yn2b source names match dev sources: {clash}")
        not_gen3 = [s for s in gen3 if not s.startswith("gd_gen3_")]
        if not_gen3:
            res["problems"].append(f"yn2b file holds non-gd_gen3_* sources: {not_gen3}")
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--yn2b-file", default="v14_parts/yn2b_train", help="under data/, without .jsonl ('' = baseline)")
    ap.add_argument("--root", default=None, help=argparse.SUPPRESS)
    a = ap.parse_args(argv)
    res = check(a.yn2b_file, a.root)
    print(json.dumps(res, indent=1))
    print("check_unseen: " + ("PASS" if not res["problems"] else "FAIL: " + " | ".join(res["problems"])))
    return 0 if not res["problems"] else 1


if __name__ == "__main__":
    sys.exit(main())

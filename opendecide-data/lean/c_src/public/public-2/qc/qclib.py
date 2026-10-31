"""Independent QC of public-2 (RUNBOOK blocker B4; C_DATA_SPEC v4 section 8, last line: public rows pass G1, G6 (on
our framings), G7, G10, G12, G13 (run elsewhere), G15 and a G5 read of 100 rows per dataset). Shared helpers.
The checker never edits, relabels or picks rows; it reads public-2's CURRENT out files and writes qc/gates/*.json."""
from __future__ import annotations

import hashlib
import json
import time
from collections import Counter
from pathlib import Path

QC = Path(__file__).resolve().parent
P2 = QC.parent
OUT = P2 / "out"
LEAN = P2.parents[2]
GATES = QC / "gates"
PROGRESS = LEAN / "c_build" / "progress_prep.log"
FILES = ("rows_r1", "reserve_r1", "dev_mt_r1")      # rows + reserve are what the mixer binds; dev = mix-tuning dev
TRAIN_FILES = ("rows_r1", "reserve_r1")
ABSTAIN = ("None of these", "None of the listed values")   # the two abstain options public-2 renders (finalize.py)
DATASETS = ("c_pub_hybridqa", "c_pub_wikisql", "c_pub_drop", "c_pub_uci_car", "c_pub_uci_nursery")


def sha256_file(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def load(fn):
    return [json.loads(l) for l in open(OUT / f"{fn}.jsonl")]


def load_all():
    return {fn: load(fn) for fn in FILES}


def file_shas():
    return {f"{fn}.jsonl": sha256_file(OUT / f"{fn}.jsonl") for fn in FILES}


def write_gate(name, ok, numbers, **extra):
    GATES.mkdir(exist_ok=True)
    d = {"gate": name, "pass": bool(ok), "files_sha256": file_shas(), "numbers": numbers,
         "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())} | extra
    json.dump(d, open(GATES / f"{name}.json", "w"), indent=1, ensure_ascii=False, default=str)
    progress(f"B4 public-2 QC {name}: pass={bool(ok)}")
    return d


def progress(msg):
    with open(PROGRESS, "a") as f:
        f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} [prep5] {msg}\n")


def yn(r):
    return r["qtype"] == "noul"


def counter(xs):
    return dict(Counter(xs))

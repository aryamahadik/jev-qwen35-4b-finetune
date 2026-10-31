"""F1 generator: shared paths, pins, IO and small helpers (C round 1; G0 F1 v7 frozen).

Only standard library + the allow-listed project modules (fmt1, negcount, decoder_io / train_decoder through fmt1).
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import random
import sys
import time
from decimal import Decimal
from pathlib import Path

GEN = Path(__file__).resolve().parent
F1 = GEN.parent
CSRC = F1.parent
LEAN = CSRC.parent
OUT = F1 / "out"
TMP = F1 / "tmp"
FMT1_DIR = CSRC / "formats" / "formats-1"
FMT2_DIR = CSRC / "formats" / "formats-2"
PACKS_DIR = CSRC / "packs"
COMMON_DIR = CSRC / "common"
PROGRESS = LEAN / "c_build" / "progress_phase2.log"
SEALED_CHECK = LEAN / "sealed_nd" / "qc" / "sealed_check.py"
PY = "/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python"

G0_SHA256 = "364769bde26a7ceaaab32a3ade821c1d9af6c8b04ceff2f84735b7ca69f36e65"
SPEC_ID = "F1.G0.v7"
GEN_VERSION = "F1-gen r2 (repair: Q2 option-class balance, depth / amendment quotas, card patch)"
SEED = 20261003
LICENCE = "CC0 1.0 (program-generated)"
SOURCE = "c_own_F1"
NEGCOUNT_SHA256 = "79368f465d438617cb64fb57e69c236893b5f686a7bbb6ffd34e7184c40a8091"
MARKERS_SHA256 = "893e206860de6dde35d82a2e6d49f00ee6f1f8bd492fe71da494953071126b78"

for p in (str(FMT1_DIR), str(COMMON_DIR), str(LEAN)):
    if p not in sys.path:
        sys.path.insert(0, p)


def git_sha() -> str:
    try:
        head = (LEAN.parent.parent / ".git" / "HEAD")
        if not head.exists():
            head = LEAN.parent / ".git" / "HEAD"
        ref = head.read_text().strip()
        if ref.startswith("ref:"):
            p = head.parent / ref.split(" ", 1)[1]
            if p.exists():
                return p.read_text().strip()[:12]
        return ref[:12]
    except OSError:
        return "unknown"


def sha256_file(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def rng_for(*parts) -> random.Random:
    h = hashlib.sha256(("\x1f".join(str(p) for p in parts)).encode()).digest()
    return random.Random(int.from_bytes(h[:8], "big") ^ SEED)


def unit(*parts) -> float:
    h = hashlib.sha256(("\x1f".join(str(p) for p in parts)).encode()).digest()
    return int.from_bytes(h[:8], "big") / 2 ** 64


def progress(msg: str) -> None:
    line = f"[F1] {dt.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')} {msg}\n"
    with open(PROGRESS, "a", encoding="utf-8") as f:
        f.write(line)


def log(msg: str, path=None) -> None:
    p = path or (F1 / "tmp" / "build.log")
    with open(p, "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%H:%M:%S')} {msg}\n")


def write_jsonl(path, rows) -> int:
    n = 0
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=False) + "\n")
            n += 1
    return n


def read_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


# ---------------------------------------------------------------- dates (ordinal ints)

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]


def d2o(d: dt.date) -> int:
    return d.toordinal()


def o2d(o: int) -> dt.date:
    return dt.date.fromordinal(o)


def fmt_date(o: int, form: str) -> str:
    d = o2d(o)
    if form == "iso":
        return d.isoformat()
    if form == "dmy":
        return f"{d.day} {MONTHS[d.month - 1]} {d.year}"
    raise ValueError(form)


# ---------------------------------------------------------------- numbers

def fmt_num(v: Decimal, places: int) -> str:
    """Comma thousands, point decimal, fixed places (row 37)."""
    q = Decimal(1).scaleb(-places) if places else Decimal(1)
    v = v.quantize(q)
    sign = "-" if v < 0 else ""
    v = abs(v)
    s = format(v, "f")
    if "." in s:
        ip, fp = s.split(".")
    else:
        ip, fp = s, ""
    ip = f"{int(ip):,}"
    return sign + ip + ("." + fp if places else "")


def dec(x) -> Decimal:
    return x if isinstance(x, Decimal) else Decimal(str(x))

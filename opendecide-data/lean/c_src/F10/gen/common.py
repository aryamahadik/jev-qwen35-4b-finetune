"""F10 generator: shared paths, seeds, hashing and progress logging (G0 F10-G0-v7)."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import random
import sys
from pathlib import Path

GEN = Path(__file__).resolve().parent
F10 = GEN.parent
CSRC = F10.parent
LEAN = CSRC.parent
OUT = F10 / "out"
TMP = F10 / "tmp"
BUILD = TMP / "build"
FMT1_DIR = CSRC / "formats" / "formats-1"
FMT2_DIR = CSRC / "formats" / "formats-2"
PACKS_DIR = CSRC / "packs"
COMMON_DIR = CSRC / "common"
PROGRESS = LEAN / "c_build" / "progress_phase2.log"
SEALED_CHECK = LEAN / "sealed_nd" / "qc" / "sealed_check.py"
PY = "/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python"

for p in (str(FMT1_DIR), str(COMMON_DIR), str(LEAN), str(GEN)):
    if p not in sys.path:
        sys.path.insert(0, p)

SPEC_ID = "F10-G0-v7"
G0_SHA256 = "4e0026f20adcd3efbb4de51e9c1dedde7736fa0a2bd062bd7c1cc662cad40e90"
GEN_VERSION = "F10-gen r1 (A20 lane)"
GIT_SHA = "01d67c5709da"
SEED = 20261005
LIC_PROGRAM = "CC0 1.0 (program-generated)"
FAMILY = "F10"


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def sha256_file(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def rng(*key) -> random.Random:
    """A deterministic RNG for one key path (family seed + key parts)."""
    s = "|".join(str(k) for k in (SEED,) + key)
    return random.Random(int.from_bytes(hashlib.sha256(s.encode()).digest()[:8], "big"))


def uhash(*key) -> float:
    s = "|".join(str(k) for k in key)
    return int.from_bytes(hashlib.sha256(s.encode()).digest()[:8], "big") / 2 ** 64


def progress(msg: str) -> None:
    line = f"{dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} [F10] {msg}\n"
    with open(PROGRESS, "a", encoding="utf-8") as f:
        f.write(line)


def utc() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def dump_jsonl(path, rows) -> int:
    n = 0
    tmp = str(path) + ".part"
    with open(tmp, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=False) + "\n")
            n += 1
    os.replace(tmp, path)
    return n


def load_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def norm_ws(s: str) -> str:
    return " ".join(str(s).split())


def tokens(s: str) -> list[str]:
    """Whole-token split used by the name and marker-collision lints (R4-02, R4-03): case-insensitive; whitespace,
    hyphen, underscore, slash and other punctuation split tokens."""
    import re
    return [t for t in re.split(r"[^0-9a-z]+", str(s).lower()) if t]


def contains_tokens(hay: str, needle: str) -> bool:
    """needle's token sequence occurs inside hay's token sequence (whole tokens)."""
    h, n = tokens(hay), tokens(needle)
    if not n or len(n) > len(h):
        return False
    return any(h[i:i + len(n)] == n for i in range(len(h) - len(n) + 1))

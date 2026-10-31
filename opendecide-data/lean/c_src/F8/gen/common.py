"""F8 generator: shared paths, seeds, progress logging and small helpers (no labels, no rendering).

Every number in the generator, solver A and solver B is an int or a fractions.Fraction (G0 spec 2: no float anywhere);
floats appear only when a row's JSON needs a number (meta.gold_probs), converted from an exact Fraction at write time.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import random
import sys
from fractions import Fraction as Fr
from pathlib import Path

F8 = Path(__file__).resolve().parents[1]                      # lean/c_src/F8
CSRC = F8.parent                                              # lean/c_src
LEAN = CSRC.parent                                            # lean
GEN = F8 / "gen"
OUT = F8 / "out"
TMP = F8 / "tmp"
DATA = GEN / "data"
FMT1 = CSRC / "formats" / "formats-1"
FMT2 = CSRC / "formats" / "formats-2"
COMMON = CSRC / "common"
PACKS = CSRC / "packs"
PROGRESS = LEAN / "c_build" / "progress_phase2.log"
SPEC = F8 / "G0_SPEC.md"
SPEC_SHA256 = "7570af9f0c8abca6a5cd46ab8b50656b9776c7a5bd572bd5ac6d2f0401cd1b35"
GEN_VERSION = "F8-gen v1.0"
SPEC_ID = "F8.G0.draft7"
BASE_SEED = 20261003
SOURCE = "c_f8"
KD_FULL_SRC = ("gd_gen2_probability",)
LICENCE = "CC0 1.0 (program-generated)"

for p in (str(FMT1), str(COMMON), str(LEAN)):
    if p not in sys.path:
        sys.path.insert(0, p)


def now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def progress(msg: str) -> None:
    line = f"{now()} [F8] {msg}"
    with open(PROGRESS, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line, flush=True)


def h64(*parts) -> int:
    return int.from_bytes(hashlib.sha256("\x1f".join(str(p) for p in parts).encode()).digest()[:8], "big")


def rng_for(*parts) -> random.Random:
    return random.Random(h64(BASE_SEED, *parts))


def sha256_file(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def write_jsonl(path, rows) -> int:
    n = 0
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=False) + "\n")
            n += 1
    return n


def read_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(x) for x in f if x.strip()]


def fr(x) -> Fr:
    if isinstance(x, Fr):
        return x
    if isinstance(x, int):
        return Fr(x)
    if isinstance(x, str):
        return Fr(x)
    raise TypeError(f"no float allowed: {type(x).__name__}")


def fstr(x: Fr) -> str:
    """Exact text of a Fraction for hashes and sidecars ('3/8', '-2', '0')."""
    x = fr(x)
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def canon(obj) -> str:
    """Canonical JSON for hashing: Fractions as exact strings, keys sorted."""
    def conv(o):
        if isinstance(o, Fr):
            return "F:" + fstr(o)
        if isinstance(o, dict):
            return {str(k): conv(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [conv(v) for v in o]
        if isinstance(o, float):
            raise TypeError("float in a hashed structure")
        return o
    return json.dumps(conv(obj), sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def log_uniform_int(rng: random.Random, lo: int, hi: int) -> int:
    """Integer in [lo, hi], log-uniform (lo >= 1), using only integer arithmetic on a fine grid."""
    if hi <= lo:
        return lo
    # draw k uniform in [0, 1000] and interpolate geometrically by repeated ratio search over ints
    cands = []
    v = lo
    while v <= hi:
        cands.append(v)
        nv = v + max(1, v // 8)
        v = nv
    if cands[-1] != hi:
        cands.append(hi)
    return rng.choice(cands)

"""F11 common: paths, pins, seeded RNG, hashing, the one F11-R2-22 tokenizer, progress log.

Imported by every F11 module (generator, renderer, parsers, solvers, gates). It holds no generator logic.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import random
import re
import sys
from pathlib import Path

GEN = Path(__file__).resolve().parent
FAM = GEN.parent                       # c_src/F11
CSRC = FAM.parent                      # c_src
LEAN = CSRC.parent                     # lean
OUT = FAM / "out"
QC = FAM / "qc"
TMP = FAM / "tmp"
PY = str(LEAN.parent / ".venv" / "bin" / "python")
FMT1 = CSRC / "formats" / "formats-1"
FMT2 = CSRC / "formats" / "formats-2"
PACKS = CSRC / "packs"
COMMON = CSRC / "common"
PROGRESS = LEAN / "c_build" / "progress_phase2.log"

for _p in (str(FMT1), str(COMMON), str(LEAN), str(GEN)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

FAMILY = "F11"
SPEC_FILE = FAM / "G0_SPEC.md"
SPEC_ID = "F11.G0.v7"
SPEC_SHA256 = "3512efba7048bca8786a3b93f499a4b6564efc3391247aac85cfb2368d8fa499"
GEN_VERSION = "F11-gen v1.0"
SEED = 20261003
SEALED_SUITE_SHA256 = "f4ae863720535b6ba27acad51917fe07b4d31344228a1dddb9d98bc3a4deac68"
LICENCE_PROGRAM = "CC0 1.0 (program-generated)"
DECODER_IO_SHA256 = "908c08d752ce8896c2628a06f8a9d3153df8c76b657bf29daae44656f75f2948"
TRAIN_DECODER_SHA256 = "c2c2d1d623ccd53f64254fb41400f5c952b4e1324d11550a01f170ab25ba04ef"


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def sha256_file(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def canon(obj) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"), default=str)


def rng(*key) -> random.Random:
    h = hashlib.sha256(("|".join(str(k) for k in (SEED,) + key)).encode()).digest()
    return random.Random(int.from_bytes(h[:8], "big"))


def uhash(*key) -> float:
    h = hashlib.sha256(("|".join(str(k) for k in key)).encode()).digest()
    return int.from_bytes(h[:8], "big") / 2 ** 64


def git_sha() -> str:
    try:
        head = (LEAN.parent.parent / ".git" / "HEAD").read_text().strip()
        if head.startswith("ref:"):
            ref = LEAN.parent.parent / ".git" / head.split(" ", 1)[1]
            if ref.exists():
                return ref.read_text().strip()[:12]
            packed = LEAN.parent.parent / ".git" / "packed-refs"
            for line in packed.read_text().splitlines():
                if line.endswith(head.split(" ", 1)[1]):
                    return line.split()[0][:12]
        return head[:12]
    except OSError:
        return "unknown"


# F11-R2-22 tokenizer (= negcount R1 before the clitic split): a maximal run of letters and digits, internal hyphens and
# apostrophes kept; compared case-folded as whole words.
TOKEN_RE = re.compile(r"[A-Za-z0-9]+(?:['’\-][A-Za-z0-9]+)*")


def toks(s: str) -> list[str]:
    return [m.group().lower().replace("’", "'") for m in TOKEN_RE.finditer(s or "")]


def contains_run(hay: list[str], needle: list[str]) -> bool:
    n = len(needle)
    if not n:
        return False
    return any(hay[i:i + n] == needle for i in range(len(hay) - n + 1))


def find_runs(hay: list[str], needle: list[str]) -> list[int]:
    n = len(needle)
    return [i for i in range(len(hay) - n + 1) if hay[i:i + n] == needle] if n else []


def utc() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def progress(msg: str) -> None:
    line = f"{utc()} [F11] {msg}\n"
    try:
        with open(PROGRESS, "a") as f:
            f.write(line)
    except OSError:
        pass


def write_jsonl(path, rows) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".part")
    with open(tmp, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    tmp.replace(path)


def read_jsonl(path):
    with open(path) as f:
        return [json.loads(l) for l in f if l.strip()]


def _cnorm(x):
    if isinstance(x, (set, frozenset)):
        return ("<set>",) + tuple(sorted((_cnorm(y) for y in x), key=repr))
    if isinstance(x, dict):
        return ("<dict>",) + tuple(sorted(((repr(k), _cnorm(v)) for k, v in x.items()), key=repr))
    if isinstance(x, (list, tuple)):
        return tuple(_cnorm(y) for y in x)
    return x


def cstr(x) -> str:
    """Hash-seed-independent string of a value (sets sorted), for order-free comparisons in the checkers."""
    return repr(_cnorm(x))

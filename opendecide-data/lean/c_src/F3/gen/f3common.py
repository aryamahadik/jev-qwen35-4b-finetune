"""F3 generator: shared constants and small helpers (no rendering, no solving).

Family F3 (state tracking and record chains), G0 spec F3.G0.v7 (sha256 8fa9a38a...), C_DATA_SPEC v4.
Everything here is deterministic. IDs, dates and seeds come from explicit RNGs passed in by the caller.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import random
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
F3_DIR = HERE.parent
LEAN = F3_DIR.parents[1]
C_SRC = LEAN / "c_src"
OUT = F3_DIR / "out"
TMP = F3_DIR / "tmp"
FMT1_DIR = C_SRC / "formats" / "formats-1"
FMT2_DIR = C_SRC / "formats" / "formats-2"
PACKS_DIR = C_SRC / "packs"
PROGRESS = LEAN / "c_build" / "progress_phase2.log"

FAMILY = "F3"
SPEC_ID = "F3.G0.v7"
SPEC_SHA256 = "8fa9a38afbe6b160fe8ed4e0500505b2e9d4ca054e8c5733dae5d20a4a127423"
GEN_VERSION = "F3-gen r3"   # repair3: negated yes/no rows emitted as yes/no pairs per card x k_all x wording (G10 cells); base-row mechanism labels steered to the drawn rate (G7). repair r2 (QC fail G6 G7 G8 G10 G11) + S4 gap marker (G5) + r2.2 (per-qt labels, bin fit, top-up caps, k-cell wordings)
LICENCE = "CC0 1.0 (program-generated)"
SOURCE = "c_f3"
# The 2.4 own-row top-level `role` value is orchestrator-supplied (no named input exists yet); one constant to rewrite.
ROLE_VALUE = "own"
MASTER_SEED = 20261003

# Abstain option wordings (card-level, T34). None contains ": " or a line break.
NEI_WORDINGS = ("cannot be determined from the log", "not determinable from these entries",
                "undetermined on the shown entries")
NONE_WORDINGS = ("none of these", "none of the listed items")
GAP_MARKERS = ("[entries missing here]", "[... gap in the log ...]", "(missing entries)")

# Words a yes/no stem may never contain (2.2, R1-16); also kept out of pack values.
BANNED_STEM_WORDS = ("answer", "answers", "answered", "option", "options", "choice", "choices", "correct",
                     "correctly", "incorrect", "incorrectly")
# rule 5: mechanism stems (expanded to inflections by the lint)
MECH_STEMS = ("void", "cancel", "withdraw", "amend", "correct", "fix", "supersede", "replace", "rename", "renumber",
              "move", "retire", "merge", "consolidate", "absorb", "transfer", "revert", "create", "adjust", "missing")
HOLDER_CHANGE_WORDS = ("released", "returned", "handed over", "disposed of", "lost", "moved", "absorbed")
XF06_MARKERS = ("unknown", "not recorded", "none", "no", "0", "null", "false", "-", "n/a", "tbd", "?")
IMPLICIT_CUE_STEMS = ("lack", "fail", "deny", "refuse", "decline", "omit", "neglect", "prevent", "rule out")
L_CORE = ("not", "n't", "no", "none", "nobody", "nothing", "nowhere", "never", "neither", "nor")
# graded-scale words (unordered-vocabulary lint, R2-04)
GRADED = ("low", "medium", "high", "first", "second", "third", "level", "stage", "tier", "grade", "minor", "major",
          "moderate", "severe", "critical", "mild", "small", "large", "partial", "full", "half")

ID_ALPHA = "ABCDEFGHJKMNPQRSTUVWXYZ"   # no I, L, O
ID_DIGITS = "23456789"                 # no 0, 1 (0 is an XF06 marker)
ID_RE = r"[A-Z]{2,4}-[0-9A-Z]{2,5}"


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def sha256_file(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def canon_json(o) -> str:
    return json.dumps(o, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def rng_for(*key) -> random.Random:
    h = hashlib.sha256("\x1f".join(str(k) for k in (MASTER_SEED,) + key).encode()).digest()
    return random.Random(int.from_bytes(h[:8], "big"))


def unit_hash(*key) -> float:
    h = hashlib.sha256("\x1f".join(str(k) for k in key).encode()).digest()
    return int.from_bytes(h[:8], "big") / 2 ** 64


def log_progress(msg: str) -> None:
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(PROGRESS, "a", encoding="utf-8") as f:
        f.write(f"{ts} [F3] {msg}\n")


# ------------------------------------------------------------------------------------------------ dates

def d_parse(s: str) -> dt.date:
    return dt.date.fromisoformat(s)


def d_add(s: str, days: int) -> str:
    return (d_parse(s) + dt.timedelta(days=days)).isoformat()


MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]
MON3 = [m[:3] for m in MONTHS]

# date formats (T26): iso | month-name | numeric dmy | numeric mdy
DATE_FORMATS = ("iso", "mon_dmy", "mon_mdy", "num_dmy", "num_mdy")


def fmt_date(iso: str, form: str) -> str:
    d = d_parse(iso)
    if form == "iso":
        return iso
    if form == "mon_dmy":
        return f"{d.day} {MON3[d.month - 1]} {d.year}"
    if form == "mon_mdy":
        return f"{MONTHS[d.month - 1]} {d.day}, {d.year}"
    if form == "num_dmy":
        return f"{d.day:02d}/{d.month:02d}/{d.year}"
    if form == "num_mdy":
        return f"{d.month:02d}/{d.day:02d}/{d.year}"
    raise ValueError(form)


DATE_PATTERNS = {
    "iso": r"\d{4}-\d{2}-\d{2}",
    "mon_dmy": r"\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{4}",
    "mon_mdy": r"(?:January|February|March|April|May|June|July|August|September|October|November|December) "
               r"\d{1,2}, \d{4}",
    "num_dmy": r"\d{2}/\d{2}/\d{4}",
    "num_mdy": r"\d{2}/\d{2}/\d{4}",
}


def parse_date(s: str, form: str) -> str:
    s = s.strip()
    if form == "iso":
        return d_parse(s).isoformat()
    if form == "mon_dmy":
        dd, mm, yy = s.split(" ")
        return dt.date(int(yy), MON3.index(mm) + 1, int(dd)).isoformat()
    if form == "mon_mdy":
        mm, rest = s.split(" ", 1)
        dd, yy = rest.split(", ")
        return dt.date(int(yy), MONTHS.index(mm) + 1, int(dd)).isoformat()
    if form == "num_dmy":
        dd, mm, yy = s.split("/")
        return dt.date(int(yy), int(mm), int(dd)).isoformat()
    if form == "num_mdy":
        mm, dd, yy = s.split("/")
        return dt.date(int(yy), int(mm), int(dd)).isoformat()
    raise ValueError(form)


# ------------------------------------------------------------------------------------------------ IDs

def new_code(rng: random.Random, n: int, digits_only: bool = False) -> str:
    al = ID_DIGITS if digits_only else ID_ALPHA + ID_DIGITS
    while True:
        s = "".join(rng.choice(al) for _ in range(n))
        if any(c in ID_DIGITS for c in s):
            return s


def lookalike(code_id: str, rng: random.Random, taken: set) -> str | None:
    """An ID that differs from code_id in exactly one character of its code part (same prefix, same length)."""
    pre, code = code_id.split("-", 1)
    for _ in range(60):
        i = rng.randrange(len(code))
        c = code[i]
        al = ID_DIGITS if c in ID_DIGITS else ID_ALPHA
        r = rng.choice(al)
        if r == c:
            continue
        cand = f"{pre}-{code[:i]}{r}{code[i + 1:]}"
        if cand not in taken and any(ch in ID_DIGITS for ch in cand.split('-', 1)[1]):
            return cand
    return None


def edit_distance(a: str, b: str) -> int:
    if a == b:
        return 0
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def words_lower(s: str) -> list[str]:
    return re.findall(r"[a-z0-9]+(?:['-][a-z0-9]+)*", s.lower())

"""F5 generator: shared paths, hashing, seeded draws, lexicon lints, negcount bridge, date helpers.

Family F5 (hard and negated yes/no), round 1. Binding: c_src/F5/G0_SPEC.md (frozen, sha256 69ec0b2d...), C_DATA_SPEC v4,
PREREG_FINAL A15/A16/A16.1. Shared code imported: c_src/common/negcount.py (XF02), fmt1 (formats-1), and for G15 only
decoder_io / train_decoder (through fmt1.card.loader_check). No other family's generator is imported (XF11).
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import random
import re
import sys
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
F5 = HERE.parent
CSRC = F5.parent
LEAN = CSRC.parent
OUT = F5 / "out"
TMP = F5 / "tmp"
PROGRESS = LEAN / "c_build" / "progress_phase2.log"
FMT1 = CSRC / "formats" / "formats-1"
FMT2 = CSRC / "formats" / "formats-2"
PACKS = CSRC / "packs"
COMMON = CSRC / "common"
G0 = F5 / "G0_SPEC.md"
G0_SHA256 = "69ec0b2da5af93f1af46154da670dece80188b855ad720adbca0999c60833b5a"
SPEC_ID = "F5.G0.frozen.69ec0b2d"
GEN_VERSION = "F5 gen v1.1 (round 1, repair r2, 5 Oct 2026)"
SEED = 20261003
LICENCE = "CC0 1.0 (program-generated)"
FAMILY = "F5"
SOURCE = "c_f5"

for p in (str(FMT1), str(COMMON), str(LEAN)):
    if p not in sys.path:
        sys.path.insert(0, p)

import negcount  # noqa: E402  (c_src/common/negcount.py, XF02; orchestrator-owned)


def now_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def progress(msg: str) -> None:
    with open(PROGRESS, "a") as f:
        f.write(f"{now_utc()} [F5] {msg}\n")


def sha(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def sha_file(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def uhash(*parts) -> float:
    h = hashlib.sha256("\x1f".join(str(p) for p in parts).encode()).digest()
    return int.from_bytes(h[:8], "big") / 2 ** 64


def rng_for(*parts) -> random.Random:
    return random.Random(int.from_bytes(hashlib.sha256("\x1f".join(str(p) for p in parts).encode()).digest()[:8], "big"))


def write_jsonl(path, rows) -> int:
    n = 0
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
            n += 1
    return n


def read_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(x) for x in f if x.strip()]


# ---------------------------------------------------------------------------------------------------------------------
# lexicons (G0 3.4)

L_CORE = ("not", "n't", "no", "none", "nobody", "nothing", "nowhere", "never", "neither", "nor")

# words that program-written text from packs may never contain (bans of 3.4 plus every operator / trigger word of the F5
# grammar, so a pack noun can never be read as an operator by the G3 parsers)
PACK_WORD_BAN = set("""
not no none nobody nothing nowhere never neither nor n't
should ought can could would has have had to if unless either only any anyone anything most majority minority few
missing unable refuted until since prior during within earlier later again stopped started yet already ever typically
usually generally active expired current valid invalid lapsed inactive lapse validity
without lack lacks lacked fail fails failed neglect neglected omit omitted refuse refused decline declined prevent
prevented deny denies denied rule ruled hardly scarcely barely except cannot false true free
every all some both or other than more less fewer fewest least over above under below exactly between before after
by through first older younger highest lowest largest smallest still longer must may need required permitted forbidden
case statement record records half reaches meets exceeds exceed managed manage confirmed confirm stated state
correction void voided renewed renew transferred transfer created status holder valid days day among cases
one following text question answer yes
""".split())

# banned anywhere in program-written text and questions (3.4), checked on whole rendered strings (lower case words)
TEXT_BANNED = set("""should ought could would typically usually generally majority minority missing unable refuted
until since during again stopped started already ever earlier later""".split()) | {"can"}
TEXT_BANNED_PHRASES = ("has to", "have to", "had to", "a few", "most of", "prior to", "not yet", "is missing",
                       "unable to", "non-hateful", "non-sexist", "earlier than", "later than", "days before")

_WORD = re.compile(r"[A-Za-z][A-Za-z'-]*")


def words(s: str) -> list[str]:
    return [w.lower() for w in _WORD.findall(s)]


def pack_phrase_ok(s: str, *, extra_ban=()) -> bool:
    """A pack noun / name / adjective may enter program-written text only if no word is an operator or banned word."""
    if not s or not isinstance(s, str):
        return False
    if re.search(r"[\"'`&<>|;:{}\[\]\\/#*_=~^%$@!?()]", s):
        return False
    if re.search(r"\d", s):
        return False
    ws = words(s)
    if not ws:
        return False
    ban = PACK_WORD_BAN | set(extra_ban)
    return not any(w in ban for w in ws)


def id_ok(s: str) -> bool:
    return bool(re.fullmatch(r"[A-Z]{1,4}-[A-Z0-9]{2,6}(-[A-Z0-9]{1,3})?", s or ""))


def text_lint(s: str) -> list[str]:
    """3.4 bans on a program-written string (cards, rendered M, questions). Returns the problems found."""
    probs = []
    low = s.lower()
    ws = set(words(s))
    for w in TEXT_BANNED & ws:
        probs.append(f"banned word {w!r}")
    if re.search(r"\bcan\b", low) and not re.search(r"\bcannot\b", low):
        pass
    for ph in TEXT_BANNED_PHRASES:
        if ph in low:
            probs.append(f"banned phrase {ph!r}")
    if re.search(r"\b\d{1,2}/\d{1,2}/\d{2,4}\b", s):
        probs.append("all-numeric date")
    if re.search(r"\b\d{1,2}:\d{2}\b", s):
        probs.append("time of day")
    return probs


# ---------------------------------------------------------------------------------------------------------------------
# negcount bridge (XF02): k_syn / k_all on the question; the same counter on the text for j_t

def negc(text: str, affixed=()):
    return negcount.count(text, affixed=tuple(sorted(set(affixed))))


def k_syn(text: str) -> int:
    return negc(text).k_syn


def k_all(text: str, affixed=()) -> int:
    return negc(text, affixed).k_all


# ---------------------------------------------------------------------------------------------------------------------
# dates (SEM-11: whole days, ISO or month-name, never all-numeric day/month, no times)

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
          "December"]


def d2s(d: dt.date, fmt: str = "iso") -> str:
    if fmt == "iso":
        return d.isoformat()
    return f"{d.day} {MONTHS[d.month - 1]} {d.year}"


_DATE_RE = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b|\b(\d{1,2}) (" + "|".join(MONTHS) + r") (\d{4})\b")


def s2d(s: str) -> dt.date:
    m = _DATE_RE.fullmatch(s.strip())
    if not m:
        raise ValueError(f"not a date: {s!r}")
    if m.group(1):
        return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    return dt.date(int(m.group(6)), MONTHS.index(m.group(5)) + 1, int(m.group(4)))


DATE_PAT = r"(?:\d{4}-\d{2}-\d{2}|\d{1,2} (?:" + "|".join(MONTHS) + r") \d{4})"


def cap1(s: str) -> str:
    return s[:1].upper() + s[1:] if s else s


def plural_unit(unit: str, n) -> str:
    return unit

"""public-2 shared helpers (C_DATA_SPEC.md v4 section 3). CPU only.

Normalisation, hashing, golden_train dedup index, deterministic RNG, token estimates, detokenisation.
Paths: only this builder's own folder, the allow-listed golden_train file (read by program for the 3.1
"unused records only" rule and the named-source passage dedup) and the downloaded public raw files.
"""
from __future__ import annotations

import hashlib
import json
import os
import random
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[2]
TMP = HERE / "tmp"
RAW = TMP / "raw"
OUT = HERE / "out"
LOGS = HERE / "logs"
GOLDEN_TRAIN = LEAN / "data" / "v14_parts" / "golden_train.jsonl"
PROGRESS = LEAN / "c_build" / "progress_phase1.log"

SEED = 20261003
GEN_VERSION = "public2-v1.1"

# C1 sources named in spec 3.1 for the Wikipedia passage dedup (10-gram rule)
NAMED_DEDUP_SOURCES = ["qnli", "gd_answer_equiv", "gd_hotpotqa_yesno", "gd_feverous", "gd_totto_claims", "gd_wtq",
                       "boolq"]

_NONALNUM = re.compile(r"[^0-9a-z]+")


def norm(s: str) -> str:
    """Lower case, every non-alphanumeric run -> one space (container- and punctuation-blind)."""
    return _NONALNUM.sub(" ", str(s).lower()).strip()


def h64(s: str) -> int:
    return int.from_bytes(hashlib.blake2b(s.encode("utf-8"), digest_size=8).digest(), "little", signed=True)


_SENT = re.compile(r"(?<=[.!?;])\s+")


def text_units(text: str, min_words: int = 5):
    """Lines and sentences (each line split again on sentence ends) with >= min_words normalized words."""
    out = []
    for line in str(text).split("\n"):
        nl = norm(line)
        if len(nl.split()) >= min_words:
            out.append(nl)
        parts = _SENT.split(line)
        if len(parts) > 1:
            for p in parts:
                np_ = norm(p)
                if len(np_.split()) >= min_words:
                    out.append(np_)
    return out


def ngrams(text: str, n: int = 10):
    w = norm(text).split()
    return [" ".join(w[i:i + n]) for i in range(0, max(0, len(w) - n + 1))]


def sha256_file(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def rng_for(*parts) -> random.Random:
    key = "|".join(str(p) for p in (SEED,) + parts)
    return random.Random(int.from_bytes(hashlib.sha256(key.encode()).digest()[:8], "little"))


def stable_id(prefix: str, *parts) -> str:
    return prefix + hashlib.sha256("|".join(str(p) for p in parts).encode()).hexdigest()[:16]


def page_bucket(page: str) -> int:
    """0..9 by sha256 of the normalized page title (0 = mix-tuning dev; 1..9 = train)."""
    return int(hashlib.sha256(norm(page).encode()).hexdigest(), 16) % 10


def detok(s: str) -> str:
    """Undo the WikiTables-WithLinks tokenisation (spaces around punctuation)."""
    s = str(s)
    s = re.sub(r"\s+([,.;:!?%)\]}])", r"\1", s)
    s = re.sub(r"([(\[{$])\s+", r"\1", s)
    s = re.sub(r"\s+('s|'re|'ve|'d|'ll|n't|'m)\b", r"\1", s)
    s = re.sub(r"\s+'\s*$", "'", s)
    s = re.sub(r"\s+-\s+", "-", s) if re.search(r"\w\s-\s\w", s) and len(s) < 40 else s
    s = re.sub(r"``\s*", '"', s)
    s = re.sub(r"\s*''", '"', s)
    s = re.sub(r"\s{2,}", " ", s)
    return s.strip()


def est_tokens(s: str) -> int:
    return int(len(s) / 3.2) + 1


def log_progress(msg: str, shared: bool = False):
    """Always to this builder's logs/build.log; milestones (shared=True) also to c_build/progress_phase1.log."""
    import datetime
    line = f"{datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} [public-2] {msg}\n"
    if shared:
        with open(PROGRESS, "a") as f:
            f.write(line)
    with open(LOGS / "build.log", "a") as f:
        f.write(line)


def write_jsonl(path, rows):
    with open(path, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return sha256_file(path)


class DedupIndex:
    """golden_train line/sentence hashes (all sources) + 10-gram hashes (spec 3.1 named sources)."""

    def __init__(self, path=TMP / "gt_index.npz"):
        import numpy as np
        d = np.load(path)
        self.units = d["units"]
        self.grams = d["grams"]
        self.np = np

    def _has(self, arr, hs):
        if not hs:
            return 0
        a = self.np.array(hs, dtype=self.np.int64)
        pos = self.np.searchsorted(arr, a)
        pos[pos >= len(arr)] = len(arr) - 1
        return int((arr[pos] == a).sum())

    def unit_hits(self, text: str, min_words: int = 5) -> int:
        return self._has(self.units, [h64(u) for u in set(text_units(text, min_words))])

    def gram_hits(self, text: str) -> int:
        return self._has(self.grams, [h64(g) for g in set(ngrams(text, 10))])

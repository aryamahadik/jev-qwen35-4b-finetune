"""formats-2 shared helpers: normalization, hashing, path guard, jsonl IO. CPU, stdlib only.

Normalization (used for every "normalized text" in formats-2 outputs):
  norm_text(s): NFKC; curly quotes -> straight; casefold; every whitespace run -> one space; strip.
  loose_text(s): norm_text, then every run of non-word characters (and "_") -> one space; strip.
    Used for the golden_train "unused" check and the HateXplain / SBF exact-text dedupe (more conservative: it also
    matches copies that differ only in punctuation or quoting).
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import time
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[2]                       # .../opendecide-data/lean
TMP = HERE / "tmp"
PROGRESS = LEAN / "c_build" / "progress_phase1.log"
LABEL = "formats-2"

_Q = str.maketrans({"‘": "'", "’": "'", "‚": "'", "‛": "'", "“": '"', "”": '"',
                    "„": '"', "′": "'", " ": " "})
_WS = re.compile(r"\s+")
_NONWORD = re.compile(r"[\W_]+", re.UNICODE)

# never-open guard (C_DATA_SPEC "Who may read what" + 7.4); every input path goes through safe_path()
_NEVER = [re.compile(p, re.I) for p in (
    r"(^|/)lean/ohs3(/|$)", r"(^|/)lean/data/[^/]*ohs3", r"(^|/)ohs3_parts(/|$)", r"(^|/)lean/prep89(/|$)",
    r"(^|/)lean/preds", r"(^|/)c_spec/sealed_brief(/|$)", r"(^|/)lean/sealed_nd(/|$)", r"(^|/)bench(/|$)",
    r"(^|/)c_spec/RESEARCH_", r"(^|/)c_spec/REVIEW_", r"(^|/)c_spec/LICENCE_CHECK_", r"(^|/)c_spec/ADDENDUM_",
    r"(^|/)\.claude/projects(/|$)", r"^/private/tmp/claude-501(/|$)", r"^/tmp/claude-501(/|$)")]
_JEV_NAME = re.compile(r"(^|[_/.-])jev", re.I)   # 7.4 program rule, applied to the path inside the repo root
REPO = LEAN.parents[1]                             # .../jev (the repo root; its own name is not a file name rule hit)


def safe_path(p) -> Path:
    rp = Path(p).resolve()
    s = str(rp)
    for rx in _NEVER:
        if rx.search(s):
            raise SystemExit(f"refused input path (never-open list): {p}")
    try:
        rel = "/" + str(rp.relative_to(REPO))
    except ValueError:
        rel = s
    if _JEV_NAME.search(rel):
        raise SystemExit(f"refused input path (7.4 jev name rule): {p}")
    return Path(p)


def norm_text(s: str) -> str:
    s = unicodedata.normalize("NFKC", s or "").translate(_Q).casefold()
    return _WS.sub(" ", s).strip()


def loose_text(s: str) -> str:
    return _NONWORD.sub(" ", norm_text(s)).strip()


def sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def sha_file(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def write_jsonl(p, rows) -> str:
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=False) + "\n")
    return sha_file(p)


def read_jsonl(p):
    with open(safe_path(p), encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def write_json(p, obj) -> str:
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write("\n")
    return sha_file(p)


def progress(msg: str):
    line = f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} [{LABEL}] {msg}"
    with open(PROGRESS, "a") as f:
        f.write(line + "\n")
    print(line, file=sys.stderr)


def words(s: str):
    return loose_text(s).split()

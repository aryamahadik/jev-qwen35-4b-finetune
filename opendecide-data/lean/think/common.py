"""Shared helpers for the phase-B think mode (A17): row keys, gold keys, fast-pass confidence features, jsonl io.

Row format (same as decoder_io / the C rows):
  {"id", "qtype": "choice"|"noul", "state", "instructions", "options": [str]|None, "gold": option text | 1/0, ...}
Think rows also carry "think_type" (math | code | science | causal | knowledge | other) and "set" (clean-set name).
Fast-pass predictions (decoder_io.predict) are dicts: choice -> {option text: p}, noul -> {"yes": p, "no": p}.
"""
from __future__ import annotations

import gzip
import hashlib
import json
import math
from pathlib import Path

THINK_TYPES = ("math", "code", "science", "causal", "knowledge", "other")
LETTERS = [chr(65 + i) for i in range(26)]


def keys(row) -> list:
    """Answer keys of a row in their original order: option texts (choice) or ["yes", "no"] (noul)."""
    return ["yes", "no"] if row["qtype"] == "noul" else list(row["options"])


def gold_key(row):
    if row.get("gold") is None:
        return None
    if row["qtype"] == "noul":
        return "yes" if row["gold"] in (1, True, "yes", "Yes") else "no"
    return row["gold"]


def argmax_key(row, probs: dict):
    """Arg-max key; ties go to the earlier key (deterministic)."""
    ks = keys(row)
    ps = [float(probs.get(k, 0.0)) for k in ks]
    return ks[max(range(len(ks)), key=lambda i: (ps[i], -i))]


def conf_features(row, probs: dict) -> dict:
    """Fast-pass confidence: top probability, margin top-1 minus top-2, normalised entropy, option count."""
    ks = keys(row)
    ps = [max(float(probs.get(k, 0.0)), 0.0) for k in ks]
    tot = sum(ps) or 1.0
    ps = sorted((p / tot for p in ps), reverse=True)
    top = ps[0]
    margin = top - (ps[1] if len(ps) > 1 else 0.0)
    ent = -sum(p * math.log(p) for p in ps if p > 0)
    ent = ent / math.log(len(ps)) if len(ps) > 1 else 0.0
    return {"top": top, "margin": margin, "entropy": ent, "n_options": len(ks)}


def split_of(item_id: str, salt: str = "think-a17", fit_share: float = 0.6) -> str:
    """Deterministic 60/40 dev-fit / dev-confirm split by sha256 of (salt, id)."""
    h = int(hashlib.sha256(f"{salt}:{item_id}".encode()).hexdigest()[:12], 16) / float(16 ** 12)
    return "dev_fit" if h < fit_share else "dev_confirm"


def read_jsonl(path):
    p = Path(path)
    op = gzip.open if p.suffix == ".gz" else open
    with op(p, "rt", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def write_jsonl(path, rows) -> int:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with open(p, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
            n += 1
    return n


def sha256_file(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

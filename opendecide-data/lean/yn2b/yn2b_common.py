"""Shared helpers for the yn2b tools (SPEC.md section 9): paths, streaming JSONL, safe new-file writes, the
MANIFEST_yn2b.jsonl record, and the few constants every tool must agree on. CPU only, no model, no network.

Write rules (SPEC hard rule 6 + the builder brief): a tool only ever writes a NEW file (never an input, never a frozen
file), writes through <name>.tmp + os.replace, and records the sha256 of what it wrote in
golden_src/gen3/MANIFEST_yn2b.jsonl (append-only; one json line per record, written with O_APPEND under a lock).
"""
from __future__ import annotations

import datetime
import fcntl
import hashlib
import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # the tools import frozen modules (lean/, golden_src/gen): never write .pyc next to them

YN2B = Path(__file__).resolve().parent
LEAN = YN2B.parent
DATA = LEAN / "data"
GEN3 = LEAN / "golden_src" / "gen3"
MANIFEST = GEN3 / "MANIFEST_yn2b.jsonl"
if str(LEAN) not in sys.path:
    sys.path.insert(0, str(LEAN))

# Files no yn2b tool may ever write (SPEC hard rule 6, FINETUNE_PLAN 3.3, the builder brief). Paths relative to LEAN.
FROZEN = (
    "data/v14_parts/golden_train.jsonl", "data/v14_parts/golden_relations.jsonl", "data/v14_parts/golden_dev.jsonl",
    "data/v14_parts/golden_dev_relations.jsonl", "data/v14_parts/train_2b_golden_kd.jsonl",
    "train_decoder.py", "decoder_io.py", "prism_x.py", "writeblock.py", "modal_od.py", "od_gcp.py",
)
FROZEN_DIRS = ("runs", "data/v14_label_shards", "data/v14_parts/raw", "data/v14_parts/defs")

# The trainer's view of targets (train_decoder.compute_loss / build_2b_kd): kept here so every tool counts the same way.
KD_SKIP_SRC = ("blend50",)
KD_FULL_SRC = ("gd_gen2_probability",)
TEACHER_SRC = "q35_4b_E"  # 4B-E fresh reads; D3 (owner, 30 Sep) may replace it with the new 4B before arm A
MARKERS = ("<<<UNTRUSTED TEXT START>>>", "<<<UNTRUSTED TEXT END>>>")


def iter_jsonl(path):
    """Streams the rows of a JSONL file (blank lines skipped)."""
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def read_jsonl(path):
    return list(iter_jsonl(path))


def kd_target(r):
    """train_decoder.kd_target: only a non-empty dict meta.teacher is a distillation target."""
    t = (r.get("meta") or {}).get("teacher")
    return t if isinstance(t, dict) and t else None


def counts_kd(rows, skip=KD_SKIP_SRC, full=KD_FULL_SRC):
    """(kd targets, kd_full rows) exactly as train_decoder.train() prints them for a config with kd > 0: teachers whose
    teacher_src is in kd_skip_src are stripped first; kd_full = yes/no rows of a kd_full_src source with a target."""
    n_kd = n_full = 0
    for r in rows:
        m = r.get("meta") or {}
        t = kd_target(r)
        if t is None or m.get("teacher_src") in skip:
            continue
        n_kd += 1
        n_full += r["source"] in full and r["qtype"] == "noul"
    return n_kd, n_full


def sha256_file(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def sha256_int(text: str) -> int:
    return int(hashlib.sha256(text.encode()).hexdigest(), 16)


def _rel(p: Path) -> str:
    try:
        return str(Path(p).resolve().relative_to(LEAN))
    except ValueError:
        return str(Path(p).resolve())


def guard_out(path, inputs=(), overwrite=False) -> Path:
    """Refuses to write a frozen file, a file inside a frozen folder, one of this run's inputs, or (without overwrite)
    any existing file. Returns the resolved path."""
    p = Path(path).resolve()
    rel = _rel(p)
    if rel in FROZEN or any(rel == d or rel.startswith(d + "/") for d in FROZEN_DIRS):
        raise SystemExit(f"refused: {rel} is frozen (SPEC hard rule 6); yn2b tools write new files only")
    for i in inputs:
        if i and Path(i).resolve() == p:
            raise SystemExit(f"refused: {rel} is an input of this run; write a new file")
    if p.exists() and not overwrite:
        raise SystemExit(f"refused: {rel} exists (pass --overwrite to replace a file this tool wrote earlier)")
    return p


def write_lines_atomic(path, lines) -> int:
    """Writes lines to path.tmp, fsyncs, then os.replace (a crash never leaves a partial file under the final name).
    Returns the number of lines."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    n = 0
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(line if line.endswith("\n") else line + "\n")
                n += 1
            f.flush()
            os.fsync(f.fileno())
    except BaseException:
        tmp.unlink(missing_ok=True)  # a failed check never leaves a partial file behind
        raise
    os.replace(tmp, path)
    return n


def write_rows(path, rows) -> int:
    return write_lines_atomic(path, (json.dumps(r, ensure_ascii=False) for r in rows))


def write_json(path, obj):
    write_lines_atomic(path, [json.dumps(obj, indent=1, ensure_ascii=False)])


def manifest_append(record: dict, manifest=None):
    """Appends one record to MANIFEST_yn2b.jsonl (created if missing). Append-safe: one write() of one line with
    O_APPEND under an exclusive lock, so parallel builders never interleave."""
    m = Path(manifest or MANIFEST)
    m.parent.mkdir(parents=True, exist_ok=True)
    rec = {"written": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), **record}
    line = (json.dumps(rec, ensure_ascii=False, sort_keys=False) + "\n").encode()
    fd = os.open(m, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        os.write(fd, line)
        os.fsync(fd)
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)


def manifest_outputs(tool: str, paths, extra=None, manifest=None):
    """One manifest record per written file: tool, path (relative to lean/), rows, sha256."""
    for p in paths:
        p = Path(p)
        n = sum(1 for _ in open(p, "rb")) if p.suffix == ".jsonl" else None
        manifest_append({"tool": tool, "path": _rel(p), "rows": n, "sha256": sha256_file(p), **(extra or {})}, manifest)

"""Shared input guard and IO for the C mixer and crowd selector (C_DATA_SPEC.md v4 0 rule 7, 3.H.1, 7.4; G1).

Every file the mixer or crowd_select reads goes through InputLog.open(); it refuses the never-open list and every 7.4
Jev-output path, and logs each input path with its sha256 (the audit trail spec 7.4 asks for). Rows are refused when
any field key (top level or meta) starts with 'jev'. Paths are checked relative to the repo root (jev/), so the repo's
own folder name never trips the jev rule. CPU only; no network.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent          # lean/c_build
LEAN = HERE.parent
REPO = LEAN.parents[1]                           # jev/
DATA = LEAN / "data"
PY = LEAN.parent / ".venv/bin/python"
A15_SUITE_SHA = "f4ae863720535b6ba27acad51917fe07b4d31344228a1dddb9d98bc3a4deac68"

# never-open list (task + spec 7.4); matched on the repo-relative path (posix)
_NEVER = [
    r"(^|/)c_spec/sealed_brief(/|$)", r"(^|/)lean/sealed_nd(/|$)", r"(^|/)c_spec/(RESEARCH_|REVIEW_|LICENCE_CHECK_)",
    r"(^|/)c_spec/ADDENDUM_research\.md$", r"(^|/)lean/ohs3(/|$)", r"(^|/)lean/data/[^/]*ohs3", r"ohs3_parts",
    r"(^|/)prep89(/|$)", r"(^|/)lean/preds_ohs[^/]*(/|$)", r"(^|/)lean/preds[^/]*/jev", r"(^|/)lean/logs/jev_",
    r"^bench(/|$)", r"(^|/)external_quarantine(/|$)", r"(^|/)ejs5/(runs|tests/_work)(/|$)",
    r"^reports/pdf_build_30sep/v154_variants/jev_", r"^reports/OpenDecide_v05_vs_Jev\.md$",
    r"(^|[_/.-])jev",                            # 7.4 program rule (file or directory name)
]
NEVER_RE = re.compile("|".join(_NEVER), re.I)
_ABS_NEVER = (str(Path.home() / ".claude/projects"), "/private/tmp/claude-501", "/tmp/claude-501")


class GuardError(SystemExit):
    pass


def refusal(path) -> str | None:
    """Why `path` may not be opened (None = allowed)."""
    p = Path(path).expanduser().resolve()
    s = str(p)
    if any(s == a or s.startswith(a + "/") for a in _ABS_NEVER):
        return "session folder (never open)"
    try:
        rel = p.relative_to(REPO).as_posix()
    except ValueError:
        rel = s
    m = NEVER_RE.search(rel)
    return f"never-open / 7.4 path rule ({m.group(0)!r})" if m else None


def sha256_file(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


class InputLog:
    """Logs every input path (repo-relative) with sha256 and bytes; refuses guarded paths."""

    def __init__(self):
        self.entries: dict[str, dict] = {}

    def check(self, path) -> Path:
        why = refusal(path)
        if why:
            raise GuardError(f"input refused: {path}: {why}")
        return Path(path)

    def record(self, path):
        p = self.check(path)
        if p.is_file():
            key = os.path.relpath(p.resolve(), REPO)
            if key not in self.entries:
                self.entries[key] = {"sha256": sha256_file(p), "bytes": p.stat().st_size}
        return p

    def open(self, path, mode="r"):
        p = self.record(path)
        return open(p, mode, encoding=None if "b" in mode else "utf-8")

    def json(self, path):
        with self.open(path) as f:
            return json.load(f)

    def jsonl(self, path):
        out = []
        with self.open(path) as f:
            for line in f:
                if line.strip():
                    out.append(check_row_keys(json.loads(line), path))
        return out


def check_row_keys(r: dict, where="") -> dict:
    """7.4 program rule: a row field whose key starts with 'jev' (top level or meta) is refused."""
    bad = [k for k in r if str(k).lower().startswith("jev")]
    bad += [k for k in (r.get("meta") or {}) if str(k).lower().startswith("jev")]
    if bad:
        raise GuardError(f"row {r.get('id')!r} in {where}: field(s) {bad} start with 'jev' (spec 7.4)")
    return r


def write_json(path, obj):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_text(json.dumps(obj, indent=1, sort_keys=False, default=str))
    os.replace(tmp, p)
    return sha256_file(p)


def write_jsonl(path, rows):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    os.replace(tmp, p)
    return sha256_file(p)


def h64(*parts) -> int:
    return int.from_bytes(hashlib.sha256("\x1f".join(map(str, parts)).encode()).digest()[:8], "big")


def log_line(path, msg):
    import time
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "a", encoding="utf-8") as f:
        f.write(time.strftime("%Y-%m-%dT%H:%M:%SZ ", time.gmtime()) + msg + "\n")

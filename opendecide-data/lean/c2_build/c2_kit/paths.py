"""c2_kit/paths.py: where C2 code lives, the never-open guard (C2_DATA_SPEC 6.5) and the A38 data guard (A37 f).

Never-open (spec 6.5 plus the C2 build rules). A path is refused when, after `~` expansion and normalisation:
  - any part below the repo root contains "ohs" (lean/ohs4_sealed/, data/ohs3*, ohs3_parts/ ...);
  - it lies under sealed_nd/, c_spec/sealed_brief/, c_build/preread/, bench/external_quarantine/,
    bench/longbench_v2/ or bench/decision_index/ (DI items);
  - any file or folder below the repo root has "jev" in its name (the repo root folder is itself called "jev", so
    the root is stripped first; outside the repo every part is checked);
  - it lies under ~/.claude/projects/ or the session temp folder /private/tmp/claude-501/ (also /tmp/claude-501/).
`never_open(path)` returns the rule a path breaks, or None. The chunker, the file-access auditor and every kit writer
use it. Matching is case-insensitive and fail-safe (a false refusal is cheap; a missed one is not).

Data guard (A37 f, G14). No C2 Haiku pool, pack, template, generator run or row may exist before OHS-4 is frozen in
amendment A38. `require_a38()` reads PREREG_FINAL.md (the only file this module reads) and raises DataBeforeFreeze
unless a "Ruling A38" block is there. Every kit writer calls it first, so before A38 nothing the kit makes can reach
disk; unit tests build rows in memory only. Writers also refuse never-open paths, paths outside lean/, and rows that
still hold private (underscore) keys.

  from c2_kit.paths import never_open, require_a38, write_jsonl
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent          # lean/c2_build/c2_kit
C2_BUILD = HERE.parent                           # lean/c2_build
LEAN = C2_BUILD.parent                           # lean
DATA_ROOT = LEAN.parent                          # opendecide-data
REPO_ROOT = DATA_ROOT.parent                     # the git root (its folder is named "jev")
PREREG = LEAN / "PREREG_FINAL.md"
COMMON = LEAN / "c_src" / "common"
FMT1 = LEAN / "c_src" / "formats" / "formats-1"
C2_PARTS = LEAN / "data" / "c2_parts"            # where C2 rows will go, after A38 only

for _p in (str(COMMON),):
    if _p not in sys.path:
        sys.path.insert(0, _p)

A38_RE = re.compile(r"^>\s*\*\*Ruling A38\b", re.M)

_UNDER = ("sealed_nd", "c_spec/sealed_brief", "c_build/preread", "bench/external_quarantine", "bench/longbench_v2",
          "bench/decision_index")


class DataBeforeFreeze(RuntimeError):
    """A37 (f): no C2 data before the OHS-4 freeze (A38)."""


class NeverOpen(PermissionError):
    """C2_DATA_SPEC 6.5: the path is on the never-open list."""


def _norm(path) -> Path:
    p = os.path.expanduser(str(path))
    if not os.path.isabs(p):
        p = os.path.join(os.getcwd(), p)
    return Path(os.path.normpath(p))


def never_open(path) -> str | None:
    """The never-open rule `path` breaks (a short tag), or None. Pure string logic: the path is never opened."""
    p = _norm(path)
    s = p.as_posix().lower()
    home = Path(os.path.expanduser("~")).as_posix().lower()
    if s.startswith(home + "/.claude/projects"):
        return "claude_projects"
    for tmp in ("/private/tmp/claude-501", "/tmp/claude-501"):
        if s == tmp or s.startswith(tmp + "/"):
            return "claude_session_tmp"
    root = REPO_ROOT.as_posix().lower()
    rel = "" if s == root else (s[len(root) + 1:] if s.startswith(root + "/") else s.lstrip("/"))
    parts = [x for x in rel.split("/") if x]
    if any("ohs" in x for x in parts):
        return "ohs"
    if any("jev" in x for x in parts):
        return "jev"
    joined = "/" + "/".join(parts) + "/"
    for u in _UNDER:
        if f"/{u}/" in joined:
            return u.split("/")[-1]
    return None


def check_path(path) -> Path:
    """`path` normalised, or NeverOpen."""
    why = never_open(path)
    if why:
        raise NeverOpen(f"never-open path ({why}): {path}")
    return _norm(path)


# ------------------------------------------------------------------------------------------------ A38 data guard

def a38_frozen(prereg_text: str | None = None) -> bool:
    """True once PREREG_FINAL.md holds a 'Ruling A38' block (the OHS-4 freeze)."""
    if prereg_text is None:
        prereg_text = PREREG.read_text(encoding="utf-8")
    return bool(A38_RE.search(prereg_text))


def require_a38(prereg_text: str | None = None) -> None:
    if not a38_frozen(prereg_text):
        raise DataBeforeFreeze("A37 (f) / G14: OHS-4 is not frozen (no 'Ruling A38' in PREREG_FINAL.md); "
                               "C2 code may run in memory, but no pool, pack, template, chunk or row may be written")


def _writable(path, prereg_text=None) -> Path:
    require_a38(prereg_text)
    p = check_path(path)
    if not str(p).startswith(str(LEAN) + os.sep):
        raise PermissionError(f"C2 writers only write under lean/: {p}")
    return p


def _no_private(obj, where="row"):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(k, str) and k.startswith("_"):
                raise ValueError(f"{where} still holds a private key {k!r} (strip side data before writing)")
            _no_private(v, where)
    elif isinstance(obj, list):
        for v in obj:
            _no_private(v, where)


def write_text(path, text: str, *, prereg_text: str | None = None) -> Path:
    p = _writable(path, prereg_text)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


def write_json(path, obj, *, prereg_text: str | None = None) -> Path:
    _no_private(obj, "json object")
    return write_text(path, json.dumps(obj, ensure_ascii=False, indent=1) + "\n", prereg_text=prereg_text)


def write_jsonl(path, rows, *, prereg_text: str | None = None) -> Path:
    rows = list(rows)
    for r in rows:
        _no_private(r)
    body = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
    return write_text(path, body, prereg_text=prereg_text)


def write_files(root, files: dict, *, prereg_text: str | None = None) -> list:
    """Write a {relative path: text} map (e.g. TaskBatch.files()) under `root`. Guarded like every kit writer."""
    out = []
    for rel, text in sorted(files.items()):
        if Path(rel).is_absolute() or ".." in Path(rel).parts:
            raise PermissionError(f"relative paths only: {rel}")
        out.append(write_text(Path(root) / rel, text, prereg_text=prereg_text))
    return out

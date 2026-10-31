"""public-3 path guard (C_DATA_SPEC v4 "Who may read what" + 7.4).

safe_in(p): refuses any input path on the never-open list or matching the 7.4 jev name rule, and any path that is not
on public-3's explicit allow-list (own folder, the golden_train replay file, the plan files, c_src/common tools).
safe_out(p): writes only inside public-3's own folder.
"""
from __future__ import annotations

import re
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]           # c_src/public/public-3
LEAN = HERE.parents[2]                                # .../opendecide-data/lean
REPO = LEAN.parents[1]                                # .../jev

_NEVER = [re.compile(p, re.I) for p in (
    r"(^|/)lean/ohs3(/|$)", r"(^|/)lean/data/[^/]*ohs3", r"(^|/)ohs3_parts(/|$)", r"(^|/)lean/prep89(/|$)",
    r"(^|/)lean/preds", r"(^|/)c_spec/sealed_brief(/|$)", r"(^|/)lean/sealed_nd(/|$)", r"(^|/)bench(/|$)",
    r"(^|/)c_spec/RESEARCH_", r"(^|/)c_spec/REVIEW_", r"(^|/)c_spec/LICENCE_CHECK_", r"(^|/)c_spec/ADDENDUM_",
    r"(^|/)\.claude/projects(/|$)", r"^/private/tmp/claude-501(/|$)", r"^/tmp/claude-501(/|$)")]
_JEV = re.compile(r"(^|[_/.-])jev", re.I)
ALLOW = [
    HERE,
    LEAN / "data" / "v14_parts" / "golden_train.jsonl",
    LEAN / "c_spec" / "C_DATA_SPEC.md",
    LEAN / "c_spec" / "C_TRAIN_RECIPE.md",
    LEAN / "c_spec" / "LICENCE_REGISTER.md",
    LEAN / "PREREG_FINAL.md",
    LEAN / "c_src" / "common",
    LEAN / "c_src" / "formats" / "formats-2" / "records",   # cross-check of record ids / text hashes only
    # v1.1: formats-2's sealed-check record drops (ids and hit kinds only; no text, no matched terms)
    LEAN / "c_src" / "formats" / "formats-2" / "tmp" / "sealed" / "dropped_records.json",
]


def _check(rp: Path) -> None:
    s = str(rp)
    for rx in _NEVER:
        if rx.search(s):
            raise SystemExit(f"refused path (never-open list): {rp}")
    try:
        rel = "/" + str(rp.relative_to(REPO))
    except ValueError:
        rel = s
    if _JEV.search(rel):
        raise SystemExit(f"refused path (7.4 jev name rule): {rp}")


def safe_in(p) -> Path:
    rp = Path(p).resolve()
    _check(rp)
    if not any(rp == a or a in rp.parents for a in ALLOW):
        raise SystemExit(f"refused path (not on the public-3 allow-list): {rp}")
    return Path(p)


def safe_out(p) -> Path:
    rp = Path(p).resolve()
    _check(rp)
    if HERE not in rp.parents:
        raise SystemExit(f"refused write outside public-3: {rp}")
    return Path(p)

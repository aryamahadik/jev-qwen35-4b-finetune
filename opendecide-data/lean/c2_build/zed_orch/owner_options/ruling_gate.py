"""ruling_gate.py: the one check every owner option runs before it does anything (default OFF).

An option switch is armed only by an owner-ruling id that EXISTS in PREREG_FINAL.md as a ruling block whose own text carries the
option's marker word. The orchestrator writes that ruling (and the marker) when, and only when, the owner decides in words; until
then no id can pass. Since 17 Oct 2026 the shipped PREREG_FINAL.md holds ONE marker, OHSAC_REPORT_ONLY in the owner ruling A68
(tests/test_gate_accepts_a68_and_nothing_else_in_the_real_prereg); every other id and option stays refused.

Block format (PREREG_FINAL.md): a quoted block opened by a line `> **Ruling A64 (...` (or `> **Amendment A28 ...`), continuing while
lines start with `>`, and ended by the next block header. A ruling counts as an OWNER ruling when the block's header (the text up to the
first `)**`, at most 1,500 characters) says "owner". An id that is missing, appears twice, has no owner in its header, or whose block lacks
the marker is refused. The marker must stand as a WHOLE TOKEN on a line of the block that starts with `> Machine marker` (A68's form:
`> Machine marker for the A68 switch (...): OHSAC_REPORT_ONLY.`); a prose mention of the word elsewhere in a ruling (for example "X is NOT
adopted") or a longer word that merely contains it never arms an option. Nothing here reads any sealed or "ohs" path: only PREREG_FINAL.md (a C2-side doc), by path from c2io.

Markers (one per option, so a ruling for one option never arms another):
  OPT3_MARKER  "OHSAC_REPORT_ONLY"    option 3: OHS-AC is report-only for C2 (ac_report_only.py)
  FRAME_MARKER "OHSAC_FRAME_EXCUSE"   option 2 (a): a family's own frame text is excused from the OHS-AC sentence / n-gram methods
  KW_MARKER    "OHSAC_KW_NARROW"      option 2 (b): the narrowed keyword export replaces the full one
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

OPT3_MARKER = "OHSAC_REPORT_ONLY"
FRAME_MARKER = "OHSAC_FRAME_EXCUSE"
KW_MARKER = "OHSAC_KW_NARROW"
MARKERS = (OPT3_MARKER, FRAME_MARKER, KW_MARKER)

_HEADER = re.compile(r"^>\s*\*\*(?:Ruling|Amendment)\s+([A-Za-z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)*)\b")
_ANY_HEADER = re.compile(r"^>\s*\*\*(?:Ruling|Amendment|Owner decision)\b")
_MARKER_LINE = re.compile(r"^>\s*Machine marker\b", re.I)
_ID = re.compile(r"^[A-Za-z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)*$")


class RulingRefused(SystemExit):
    """Raised (as a SystemExit with the reason) when an option is asked for without a valid owner ruling."""


def ruling_blocks(prereg_text: str) -> dict[str, list[str]]:
    """{ruling id: [block text, ...]} (a list so a duplicated id can be seen and refused)."""
    out: dict[str, list[str]] = {}
    cur_id, cur = None, []

    def flush():
        if cur_id is not None:
            out.setdefault(cur_id, []).append("\n".join(cur))

    for ln in prereg_text.splitlines():
        m = _HEADER.match(ln)
        if m or _ANY_HEADER.match(ln):
            flush()
            cur_id, cur = (m.group(1) if m else None), ([ln] if m else [])
        elif cur_id is not None and ln.startswith(">"):
            cur.append(ln)
        else:
            flush()
            cur_id, cur = None, []
    flush()
    return out


def header_of(block: str) -> str:
    flat = re.sub(r"\s+", " ", re.sub(r"(?m)^>\s?", "", block))
    cut = flat.find(")**")
    return flat[: cut if 0 <= cut <= 1500 else 1500]


def has_marker(block: str, marker: str) -> bool:
    """True when `marker` stands as a whole token on a `> Machine marker ...` line of the block (not inside a longer word, not in prose)."""
    pat = re.compile(r"(?<![A-Za-z0-9_])" + re.escape(marker) + r"(?![A-Za-z0-9_])")
    return any(_MARKER_LINE.match(ln) and pat.search(ln) for ln in block.splitlines())


def check(ruling_id, marker: str, prereg_text: str | None = None) -> tuple[dict | None, str | None]:
    """(info, None) when `ruling_id` arms the option of `marker`, else (None, reason). info = {"id", "marker", "block_sha256",
    "prereg_sha256"} (shas only; the block text is not copied)."""
    if marker not in MARKERS:
        return None, f"unknown option marker {marker!r}"
    if not isinstance(ruling_id, str) or not _ID.match(ruling_id):
        return None, f"{ruling_id!r} is not a ruling id (e.g. A68)"
    text = prereg_text
    if text is None:
        import c2io                                  # lazy: the unit tests pass the text in
        text = Path(c2io.PREREG).read_text(encoding="utf-8")
    blocks = ruling_blocks(text).get(ruling_id) or []
    if not blocks:
        return None, f"PREREG_FINAL.md has no ruling block {ruling_id!r}"
    if len(blocks) > 1:
        return None, f"ruling id {ruling_id!r} appears {len(blocks)} times in PREREG_FINAL.md (ambiguous)"
    block = blocks[0]
    if not re.search(r"\bowner\b", header_of(block), re.I):
        return None, f"ruling {ruling_id} is not an owner ruling (its header does not say owner)"
    if not has_marker(block, marker):
        return None, (f"ruling {ruling_id} does not carry the marker {marker} on a '> Machine marker' line "
                      "(it does not arm this option)")
    return {"id": ruling_id, "marker": marker, "block_sha256": hashlib.sha256(block.encode("utf-8")).hexdigest(),
            "prereg_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest()}, None


def block_contains(ruling_id, marker: str, prereg_text: str | None = None) -> bool:
    """True when the (single) block of `ruling_id` carries `marker`. Used for the optional scope marker of option 2 (a); call after require()."""
    text = prereg_text
    if text is None:
        import c2io
        text = Path(c2io.PREREG).read_text(encoding="utf-8")
    blocks = ruling_blocks(text).get(ruling_id) or []
    return len(blocks) == 1 and has_marker(blocks[0], marker)


def require(ruling_id, marker: str, prereg_text: str | None = None) -> dict:
    info, why = check(ruling_id, marker, prereg_text)
    if why:
        raise RulingRefused(f"owner option refused: {why}. Nothing was changed (the option stays OFF).")
    return info


def pop_flag(argv: list[str], flag: str) -> tuple[list[str], str | None]:
    """(argv without `flag VALUE` / `flag=VALUE`, VALUE or None). A flag with no value is a SystemExit."""
    out, val, i = [], None, 0
    while i < len(argv):
        a = argv[i]
        if a == flag or a.startswith(flag + "="):
            if val is not None:
                raise SystemExit(f"{flag} given twice: one owner-ruling id only (the option stays OFF)")
            if a == flag:
                if i + 1 >= len(argv) or argv[i + 1].startswith("--"):
                    raise SystemExit(f"{flag} needs an owner-ruling id (e.g. {flag} A68)")
                val, i = argv[i + 1], i + 2
            else:
                val, i = a.split("=", 1)[1], i + 1
        else:
            out.append(a)
            i += 1
    return out, val


def lean_on_path() -> Path:
    """Make c2_build (and c2_build/zed_orch) importable from a wrapper run as a script; returns c2_build."""
    cb = Path(__file__).resolve().parents[2]
    for p in (str(cb), str(cb / "zed_orch")):
        if p not in sys.path:
            sys.path.insert(0, p)
    return cb

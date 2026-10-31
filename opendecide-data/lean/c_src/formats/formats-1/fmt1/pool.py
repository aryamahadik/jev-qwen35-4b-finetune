"""Load the formats-1 data files and pick styles without looking at labels.

Every picker here hashes ids only (family, card_id, row key). None of them reads gold, options or difficulty, so the
style choice cannot become a shortcut (G6 (d), G7, G10).
"""
from __future__ import annotations

import hashlib
import json
from functools import lru_cache
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"


@lru_cache(maxsize=None)
def _load(name: str) -> tuple:
    with open(DATA / name, encoding="utf-8") as f:
        return tuple(json.loads(line) for line in f if line.strip())


@lru_cache(maxsize=None)
def _index(name: str) -> dict:
    return {o["id"]: o for o in _load(name)}


def styles(*, held_out: bool | None = False, container: str | None = None, compat: str | None = None,
           exclude_flags: tuple = (), require_flags: tuple = ()) -> list[dict]:
    """Styles filtered. held_out=False (default) gives training styles only; True gives the 50 dev-only styles;
    None gives all 400 (previews and tests only: never pick a training row's style from it; training rows go
    through training_style() and the mixer's refuse_held_out()). compat names a key of `compat_hints` (e.g. "F4")
    that must be true."""
    out = []
    for s in _load("styles.jsonl"):
        if held_out is not None and s["held_out"] != held_out:
            continue
        if container and s["container"] != container:
            continue
        if compat and not s["compat_hints"].get(compat):
            continue
        if any(s["flags"].get(f) for f in exclude_flags):
            continue
        if not all(s["flags"].get(f) for f in require_flags):
            continue
        out.append(s)
    return out


def style(sid: str) -> dict:
    """Any style, held-out ones included (dev rows, previews). A training row uses training_style()."""
    return _index("styles.jsonl")[sid]


class HeldOutStyleError(ValueError):
    """A held-out (mix-tuning dev only) style where a training style is required."""


def held_out_style_ids() -> frozenset:
    return frozenset(s["id"] for s in _load("styles.jsonl") if s["held_out"])


def training_style(sid: str) -> dict:
    """The style for a TRAINING row; raises HeldOutStyleError on any of the 50 held-out ids, KeyError on unknown ids."""
    s = _index("styles.jsonl")[sid]
    if s["held_out"]:
        raise HeldOutStyleError(f"{sid} is a held-out style: mix-tuning dev only, never a training row")
    return s


def dev_style(sid: str) -> dict:
    """A held-out style for a dev (S5 / mix-tuning) row; raises on a training id so the dev set stays unseen."""
    s = _index("styles.jsonl")[sid]
    if not s["held_out"]:
        raise ValueError(f"{sid} is a training style, not a held-out dev style")
    return s


def refuse_held_out(rows, *, strict_unknown: bool = False) -> dict:
    """Mixer guard over TRAINING rows: every row whose meta.format_style is a held-out style id (or whose
    meta.sampler is the held-out S5) is refused. Raises HeldOutStyleError naming the counts and the first ids;
    returns counts when clean. strict_unknown also refuses a format_style that is not a formats-1 id
    (rows without a format_style, e.g. replay rows, always pass)."""
    ho = held_out_style_ids()
    known = _index("styles.jsonl")
    n = held = s5 = unknown = 0
    bad: list[str] = []
    for r in rows:
        n += 1
        m = r.get("meta") or {}
        fs = m.get("format_style")
        if fs in ho:
            held += 1
            bad.append(str(r.get("id")))
        elif fs is not None and fs not in known and strict_unknown:
            unknown += 1
            bad.append(str(r.get("id")))
        if m.get("sampler") == "S5":
            s5 += 1
            bad.append(str(r.get("id")))
    out = {"rows": n, "held_out_style_rows": held, "s5_rows": s5, "unknown_style_rows": unknown}
    if held or s5 or unknown:
        raise HeldOutStyleError(f"refused training rows: {out}; first ids {bad[:5]}")
    return out


def skin(kid: str) -> dict:
    return _index("skins.jsonl")[kid]


def card_style(cid: str) -> dict:
    return _index("card_styles.jsonl")[cid]


def register(name: str) -> dict:
    for r in _load("registers.jsonl"):
        if r["name"] == name or r["id"] == name:
            return r
    raise KeyError(name)


def instr_position(pid: str) -> dict:
    return _index("instr_positions.jsonl")[pid]


def fence(fid: str) -> dict:
    return _index("fences.jsonl")[fid]


def container(name: str) -> dict:
    for c in _load("containers.jsonl"):
        if c["name"] == name:
            return c
    raise KeyError(name)


def defs_variant(vid: str) -> dict:
    return _index("defs_styles.jsonl")[vid]


def defs_variants(style_name: str) -> list[dict]:
    return [o for o in _load("defs_styles.jsonl") if o.get("kind") == "defs_variant" and o["style"] == style_name]


def fewshot_template(tid: str) -> dict:
    return _index("fewshot_templates.jsonl")[tid]


def inverted(iid: str) -> dict:
    return _index("inverted.jsonl")[iid]


def inverted_all(kind: str) -> list[dict]:
    return [o for o in _load("inverted.jsonl") if o["kind"] == kind]


def mask_scheme(mid: str) -> dict:
    return _index("label_masks.jsonl")[mid]


def swap_words() -> list[dict]:
    return list(_load("swap_words.jsonl"))


def label_notices() -> list[dict]:
    return list(_load("label_notices.jsonl"))


def label_rules() -> list[dict]:
    return list(_load("label_rules.jsonl"))


def unit_hash(*parts: str) -> float:
    """Uniform number in [0, 1) from ids only."""
    h = hashlib.sha256("\x1f".join(str(p) for p in parts).encode()).digest()
    return int.from_bytes(h[:8], "big") / 2 ** 64


def pick(candidates: list, *key: str):
    """Label-independent pick from a list (sorted by id first, so the result does not depend on list order)."""
    if not candidates:
        raise ValueError("no candidates")
    c = sorted(candidates, key=lambda o: o["id"] if isinstance(o, dict) else str(o))
    return c[int(unit_hash(*key) * len(c))]


def card_style_set(candidates: list[dict], k: int, *key: str) -> list[dict]:
    """A fixed subset of k styles for one card (e.g. key = family, card_id); rows then pick inside it."""
    c = sorted(candidates, key=lambda o: o["id"])
    ranked = sorted(c, key=lambda o: unit_hash(*key, o["id"]))
    return ranked[:k]

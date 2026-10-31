"""negtwins/frozen.py: the frozen trained catalogue and the held-out guard (A42-D 7.3 / 7.4, frozen 15 Oct 2026).

TRAINED_CATALOGUE.json is the list of trained patterns (programmatic 111 + lexicon-based 268) with the admitted pairs; its
sha256 is recorded in FREEZE_A42D7.json (and in the PREREG). Every builder loads it through load_trained(), which re-checks
that hash and refuses a held-out pattern. From the freeze on, no training row may use a held-out pattern or surface:
guard_patterns() is called by plan.plan_block and checks.twin_row refuses held-out patterns on its own.
"""
from __future__ import annotations

import json
from pathlib import Path

from . import core as C
from . import heldout as H

HERE = Path(__file__).resolve().parent
TRAINED_FILE = HERE / "TRAINED_CATALOGUE.json"
FREEZE_FILE = HERE / "FREEZE_A42D7.json"


def is_heldout(p) -> bool:
    return bool(p.held_out or p.source == "heldout" or str(p.pid).startswith("H:"))


def heldout_surfaces() -> tuple:
    """(normalised held-out frames incl. the three dev frames, held-out content words) from the realised freeze, if it exists."""
    frames = {" ".join(C.tokens(f)) for f in C.DEV_FRAMES}
    words = set()
    if H.REALISED_FILE.exists():
        adm = json.loads(H.REALISED_FILE.read_text(encoding="utf-8"))
        frames |= {" ".join(C.tokens(v)) for v in adm.values() if isinstance(v, str)}
        words = H.surface_words(adm)
    return frames, words


def guard_patterns(patterns) -> None:
    """Raise if any pattern is a held-out pattern or trains on a held-out surface (exact frame, or a pair sharing a word)."""
    frames, words = heldout_surfaces()
    pairs = {}
    for p in patterns:
        if is_heldout(p):
            raise ValueError(f"held-out pattern {p.pid} in a training build (A42-D 7.4)")
        if p.frame and " ".join(C.tokens(p.frame)) in frames:
            raise ValueError(f"pattern {p.pid} trains on a held-out frame {p.frame!r}")


def guard_pairs(pairs: dict) -> None:
    _frames, words = heldout_surfaces()
    for pid, pr in pairs.items():
        shared = {w for side in ("a", "b") for w in pr[side].values() if w} & words
        if shared:
            raise ValueError(f"pair {pid} shares {sorted(shared)} with the held-out surfaces")


def load_trained(verify: bool = True) -> tuple:
    """(patterns, pairs) of the frozen trained catalogue. Verifies the sha256 in FREEZE_A42D7.json and the held-out guard."""
    text = TRAINED_FILE.read_text(encoding="utf-8")
    if verify:
        rec = json.loads(FREEZE_FILE.read_text(encoding="utf-8"))
        if C.sha(text) != rec["trained_catalogue_sha256"]:
            raise RuntimeError("TRAINED_CATALOGUE.json differs from the frozen sha256")
    data = json.loads(text)
    pats = [C.Pattern(**d) for d in data["patterns"]]
    pairs = data["pairs"]
    C.register_verbs(pairs.values())
    guard_patterns(pats)
    guard_pairs(pairs)
    return pats, pairs

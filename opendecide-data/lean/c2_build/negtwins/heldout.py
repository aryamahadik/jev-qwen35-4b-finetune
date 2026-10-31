"""negtwins/heldout.py: the >= 30 held-out negation patterns (A42-D 7.4), authored FIRST and frozen.

HELDOUT_SPECS is the structure of 43 patterns (40 complement, 3 equiv): operator, predicate class, and either a fixed
surface (the three T37b-dev frames, never trained) or a SLOT whose surface Haiku realises (tasks.heldout_tasks) and
G-LEX admits 2/2 (lexicon.py). freeze() writes HELDOUT_SPECS.json and logs its sha256 in HELDOUT_FREEZE.json BEFORE any
training pattern, lexicon draft or Haiku task exists; freeze_realised() logs the second hash once the surfaces are
admitted. These patterns are used only for the G-proxy's 150 complement pairs (<= 5 per pattern) and the item 10
symmetrisation probe (A42-D 7.4, 10.3); build_catalogue() never sees them and `disjoint()` removes any training
lexicon entry that shares a surface word with them (the held-out set wins).
"""
from __future__ import annotations

import datetime
import json
from pathlib import Path

from . import core as C

HERE = Path(__file__).resolve().parent
SPECS_FILE = HERE / "HELDOUT_SPECS.json"
FREEZE_FILE = HERE / "HELDOUT_FREEZE.json"
REALISED_FILE = HERE / "HELDOUT_REALISED.json"
MAX_PAIRS_PER_PATTERN = 5
N_PAIRS_TARGET = 150

# slots Haiku realises: HF = positive truth frame used with a contracted "n't"; HN = negative frame; HP = lexical pair
SLOTS = {**{f"HF{i}": "pos_frame" for i in range(1, 5)}, **{f"HN{i}": "neg_frame" for i in range(1, 5)},
         **{f"HP{i}": "verb_pair" for i in range(1, 7)}, **{f"HP{i}": "adj_pair" for i in range(7, 12)}}


def specs() -> list:
    out = []
    for i, f in enumerate(C.DEV_FRAMES):
        for cls in ("DO", "COP", "HAVE"):
            out.append({"hid": f"H-DEVF{i + 1}-NOT-{cls}", "op": "FRAME_NOT", "cls": cls, "frame": f, "contr": "not"})
        out.append({"hid": f"H-DEVF{i + 1}-POS-DO", "op": "POS_FRAME", "cls": "DO", "frame": f})
    for i in range(1, 5):
        for cls in ("DO", "COP"):
            out.append({"hid": f"H-HF{i}-NT-{cls}", "op": "FRAME_NOT", "cls": cls, "slot": f"HF{i}", "contr": "nt"})
        for cls in ("DO", "COP", "MOD"):
            out.append({"hid": f"H-HN{i}-NEG-{cls}", "op": "NEG_FRAME", "cls": cls, "slot": f"HN{i}"})
    for i in range(1, 12):
        out.append({"hid": f"H-HP{i}-LEX", "op": "LEX_PAIR", "cls": "DO" if i <= 6 else "COP", "slot": f"HP{i}",
                    "direction": "a>b"})
    for s in out:
        s["relation"] = "complement" if s["op"] in C.COMPLEMENT_OPS else "equiv"
    return out


def freeze(now: str | None = None) -> dict:
    """Write the specs and log the hash. Refuses to overwrite an existing freeze (the hash is the record)."""
    if FREEZE_FILE.exists():
        raise FileExistsError("held-out patterns are already frozen; the hash is never re-logged")
    text = json.dumps(specs(), indent=1, sort_keys=True) + "\n"
    SPECS_FILE.write_text(text, encoding="utf-8")
    rec = {"file": SPECS_FILE.name, "sha256": C.sha(text), "n_patterns": len(specs()),
           "n_complement": sum(1 for s in specs() if s["relation"] == "complement"),
           "frozen_utc": now or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "note": "authored before any training pattern, lexicon draft or Haiku task of negtwins existed"}
    FREEZE_FILE.write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    return rec


def verify_frozen() -> bool:
    if not (FREEZE_FILE.exists() and SPECS_FILE.exists()):
        return False
    rec = json.loads(FREEZE_FILE.read_text())
    return C.sha(SPECS_FILE.read_text(encoding="utf-8")) == rec["sha256"]


def realise(admitted: dict) -> list:
    """Held-out Patterns from the frozen specs + admitted surfaces {slot: frame string | pair dict}. A spec whose slot
    has no admitted surface is reported missing (never replaced)."""
    pats, missing = [], []
    for s in json.loads(SPECS_FILE.read_text()):
        slot = s.get("slot")
        kw = {"frame": s.get("frame", ""), "contr": s.get("contr", ""), "direction": s.get("direction", "")}
        if slot:
            val = admitted.get(slot)
            if val is None:
                missing.append(s["hid"])
                continue
            if isinstance(val, dict):
                kw["pair"] = val["pair_id"]
            else:
                kw["frame"] = val
        p = C.make_pattern(s["op"], s["cls"], source="heldout", held_out=True, **kw)
        pats.append(C.Pattern(**{**p.__dict__, "pid": "H:" + s["hid"] + ":" + p.pid.split("|", 1)[1]}))
    return pats, missing


def freeze_realised(admitted: dict, now: str | None = None) -> dict:
    """Second log, after Haiku + G-LEX: the admitted surfaces. Written once."""
    if REALISED_FILE.exists():
        raise FileExistsError("held-out realisations are already frozen")
    text = json.dumps(admitted, indent=1, sort_keys=True, ensure_ascii=False) + "\n"
    REALISED_FILE.write_text(text, encoding="utf-8")
    return {"file": REALISED_FILE.name, "sha256": C.sha(text), "n_slots": len(admitted)}


def surface_words(admitted: dict) -> set:
    ws = set()
    for v in admitted.values():
        items = [v] if isinstance(v, str) else [w for side in ("a", "b") for w in v[side].values() if w]
        for t in items:
            ws |= set(C.tokens(t))
    return ws - {"is", "it", "that", "to", "say", "the", "a", "be", "not", "case", "would", "does"}


def disjoint(train_lex: dict, admitted_heldout: dict) -> tuple:
    """(clean training lexicon, dropped entries): remove every training frame / pair that shares a content word or an
    exact frame string with the held-out surfaces."""
    bad = surface_words(admitted_heldout)
    held_frames = {C.sha(" ".join(C.tokens(v))) for v in admitted_heldout.values() if isinstance(v, str)}
    held_frames |= {C.sha(" ".join(C.tokens(f))) for f in C.DEV_FRAMES}
    dropped = []
    out = {"pos_frames": [], "neg_frames": [], "pairs": []}
    for key in ("pos_frames", "neg_frames"):
        for f in train_lex.get(key, []):
            if C.sha(" ".join(C.tokens(f))) in held_frames:
                dropped.append(f)
            else:
                out[key].append(f)
    for pr in train_lex.get("pairs", []):
        words = {w for side in ("a", "b") for w in pr[side].values() if w}
        if words & bad:
            dropped.append(pr["pair_id"])
        else:
            out["pairs"].append(pr)
    return out, dropped

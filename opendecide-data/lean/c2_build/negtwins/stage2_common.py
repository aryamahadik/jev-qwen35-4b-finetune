"""negtwins stage 2 helpers: rebuild the draft / held-out batches and read their answers (no model, no network)."""
import json
from pathlib import Path

from negtwins import core as C, heldout as H, lexicon as L, tasks as T

HAIKU = T.HERE / "haiku"
OUT = T.HERE / "stage2"


def load_raw(root: Path) -> dict:
    return {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted((root / "answers").glob("*.json"))}


def draft():
    b = T.draft_batch()
    assert b.batch_id == json.loads((HAIKU / "draft" / "TASKS.json").read_text())["batch_id"]
    cands, probs = T.parse_draft(b, load_raw(HAIKU / "draft"))
    return b, cands, probs


def heldout():
    b = T.heldout_batch()
    assert b.batch_id == json.loads((HAIKU / "heldout" / "TASKS.json").read_text())["batch_id"]
    cands, probs = T.heldout_candidates(b, load_raw(HAIKU / "heldout"))
    return b, cands, probs

"""Item 10 (Opus distillation at C1 errors; PREREG A47, FINAL_PLAN item 10): shared paths, constants and I/O.

Flow (each stage is a subcommand of i10.py; STATE.json records the stage reached):
  slices      error slices of the G-block C1 read -> allocation of authoring tasks (counts only)
  author      Haiku card-authoring task files (3 choice cards per task; slice A boundary pairs, slice B emotion / political)
  lint        collect authored cards, lint (gcards.lint_card + I10 extras), dedup (also against the 41 admitted GB cards)
  extract     two independent Haiku G-LEX reads (rA, rB) of the surviving cards (A39 c)
  compare     program checks of both reads (admit_cards.check_card) -> review sheet for the Sonnet first pass
  admit       review.json verdicts -> cards/admitted.jsonl (any doubt rejects)
  cands       text x card candidates (rendered with the pinned decoder_io), data/i10_c1read.jsonl for the free C1 read
  select      keep rows with C1 top probability < 0.75 or margin < 0.3 (2-view C1 read), Haiku label task files
  route       Haiku answers -> accept (H = C1 and conf >= 0.9) or Opus; slice B goes to Opus only; <= 150 Opus chunks
  finalize    Opus answers -> keep at confidence >= 0.85; per-card cap 150, domain cap 20%, block cap 5,000
  package     data/c2_parts/I10/{out,qc}; crowd shards for the C1 crowd read

Rules carried from the plan: C1 output is a routing signal, never a label; labels are never edited (drop only); Haiku never
sets a label without the Opus cascade where the plan says so; no GB / MD / T27 / T32 / A55 file is touched; no G13 here.
Every write goes through c2_kit.paths (A38 guard, never-open guard, lean/ only).
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

I10 = Path(__file__).resolve().parent            # lean/c2_build/item10
C2 = I10.parent                                  # lean/c2_build
LEAN = C2.parent
GB = C2 / "gblock"
TOOLS = GB / "tools"
for _p in (str(C2), str(LEAN), str(TOOLS), str(LEAN / "c_build")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
from c2_kit import paths as kp  # noqa: E402

SEED = 20261013
BLOCK = "I10"
SOURCE = "c2_i10"
C1 = "q35_4b_main500k"

# ---- the plan's numbers (FINAL_PLAN item 10, A47) -----------------------------------------------------------------------
UNC_TOP, UNC_MARGIN = 0.75, 0.30      # keep rows where C1's top probability < 0.75 or its margin < 0.3
H_AGREE_CONF = 0.90                   # Haiku label stays only when H = C1 argmax and H confidence >= 0.9
OPUS_KEEP = 0.85                      # Opus labels are kept at confidence >= 0.85
OPUS_MAX_CHUNKS, CHUNK = 150, 50      # at most 150 Opus chunks of <= 50 items
PER_CARD_MAX = 150                    # at most 150 rows per card
BLOCK_CAP, DOMAIN_CAP = 5000, 0.20    # 3-5K rows (not 5-8K); no domain above 20% (G-block rule)
TEXTS_PER_CARD = 320                  # candidate texts read per admitted card
SAMPLES_PER_TASK = 12                 # example texts shown to the card author
CARDS_PER_TASK = 3
AUDIT_SHARE = 0.04                    # seeded Opus audit of Haiku-accepted rows (A39 d style; > 6% in a domain drops its unaudited rows)
AUDIT_MAX_DISAGREE = 0.06

# ---- layout -----------------------------------------------------------------------------------------------------------
STATE = I10 / "STATE.json"
SLICES = I10 / "slices.json"
CARDS = I10 / "cards"
AUTH_T, AUTH_A = CARDS / "author_tasks", CARDS / "author_answers"
EXT_T, EXT_A, EXT_K = CARDS / "extract_tasks", CARDS / "extract_answers", CARDS / "extract_key"
ADMIT = CARDS / "admission"
CANDS = I10 / "cands"
LABEL = I10 / "label"
PKG = I10 / "package"
DATA = LEAN / "data"
READ_SPLIT = "i10_c1read"                          # data/i10_c1read.jsonl, preds_i10_c1read/q35_4b_main500k.jsonl
OUT_DIR = DATA / "c2_parts" / BLOCK
PREDS = LEAN / f"preds_{READ_SPLIT}" / f"{C1}.jsonl"


def sha_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def sha_file(p) -> str:
    return hashlib.sha256(Path(kp.check_path(p)).read_bytes()).hexdigest()


def read_json(p):
    return json.loads(Path(kp.check_path(p)).read_text(encoding="utf-8"))


def read_jsonl(p) -> list:
    with open(kp.check_path(p), encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def write_json(p, obj):
    return kp.write_json(p, obj)


def write_text(p, text):
    return kp.write_text(p, text)


def write_jsonl(p, rows):
    return kp.write_jsonl(p, rows)


def state() -> dict:
    return read_json(STATE) if STATE.exists() else {"stage": "none", "history": []}


def set_state(stage: str, **info) -> dict:
    import datetime
    st = state()
    st["stage"] = stage
    st.update(info)
    st.setdefault("history", []).append({"stage": stage,
                                         "utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")})
    write_json(STATE, st)
    return st


# ---- task files (markdown; one agent per file; Read + Write tools only) ----------------------------------------------------
ACCESS = ("This task file is the only file you may open. Do not open, list or search any other file or folder, do not run "
          "shell commands, do not use the web, and use only the Read and Write tools.")


def task_md(title: str, task_id: str, answer_path: str, instructions: str, contract: str, items, n_expected: int,
            items_label: str = "Items", n_items: int | None = None,
            items_note: str = "JSON; answer every item exactly once") -> str:
    """One self-contained task file. The ANSWER FILE is named first. `items` is a JSON-able list/dict shown verbatim.
    n_items (default n_expected) is the number of shown items when it differs from the number of answers."""
    body = json.dumps(items, ensure_ascii=False, indent=1)
    n_items = n_expected if n_items is None else n_items
    return (f"# {title} {task_id}\n\n"
            f"ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):\n{answer_path}\n\n"
            f"{ACCESS}\n\n"
            f"Items: {n_items}. Answers expected: {n_expected}.\n\n"
            f"## Instructions\n\n{instructions.strip()}\n\n"
            f"## Answer contract\n\n{contract.strip()}\n\n"
            f"## {items_label} ({items_note})\n\n{body}\n")


def task_record(task_file, answer_file, model: str) -> dict:
    assert model in ("haiku", "opus"), model
    return {"task_file": str(task_file), "answer_file": str(answer_file), "model": model}

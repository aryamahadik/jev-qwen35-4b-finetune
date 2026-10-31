"""transfer/T19/redo3.py: T19 redo round 3, the one authoring task that closes the single G0 shortfall left by the
pools_v2 freeze (STAGE_A3_REPORT.json, family T19: wording/yn_not_compliant, 13 admitted of 14, short 1).
G0_SPEC.md v1.1 section 6 and its sha256 are unchanged; no target is lowered; no gate bar is loosened. Haiku writes
text only and never sets or chooses a label (PREREG A37 b).

What this round holds
  (a) Pending reads. Every G-LEX / G3-H read task of the family (round 1: 7, redo2: 5) already has a valid answer
      file, so no read is re-wrapped. pending_reads() proves it from disk; the index records the result (empty).
      The reads of THIS round's candidates cannot be written yet: a read item holds the candidate text. After the
      answers exist they follow the redo2 pattern (2 G-LEX reads per lint-clean candidate; extractor ids new).
  (b) One new authoring task for the one open cell. The gap is 1; the task asks for 50% more, i.e. ceil(1.5 * gap)
      = 2 items (A, B), 3 candidates each (redo2 asked 2). Items are RESERVES for each other: the cell may not
      exceed its target 14, so the merge keeps at most `gap` piece(s) per cell, the first admitted candidate of the
      first item that has one (order A, B), and the rest are discarded.

Rulings of this round (the lead's, recorded in the index; nothing in G0, QUESTION_MEANINGS or a bar changes)
  R5  Key phrase pinned to "not compliant with", one of the two phrases redo2.PHRASES already allows for the form.
      The data decide (computed from pools_v2 by phrase_stats()): "not in compliance with" was read as "out of
      compliance with" by at least one reader in 4 of the 7 distinct forms written with it (3 admitted),
      "not compliant with" in none of 9 (9 admitted). The open item's own two redo2 candidates (both "not in
      compliance with") are rejected for good and are not re-voted (R2 stands).
  R6  Shape. Every admitted "not compliant with" form has the shape "<opening>, is {SITE} not compliant with its
      checklist on the audit date?"; the rejected forms of the redo2 round added a clause around the date ("tested on
      the audit date", "at the audit date"). The item rules fix the ending (stricter only; checks as written).
  R7  Openings (R3 stands). Six new openings, none in redo2.FRAMES, none a round 1 style hint (haiku_author.STYLES),
      each lint-checked inside a full sample sentence by the tests; (key phrase, opening) unique in the form.
  Selection (redo2's, unchanged): per item the first candidate in written order that passes every check
  (haiku_author.check_wording, freeze.wording_problems, redo2.phrase_problems, exact dedup against the frozen pools,
  every round 1 and redo2 wording and the candidates kept before it) and then G-LEX 2/2 is kept.

  cd lean && ../.venv/bin/python c2_build/transfer/T19/redo3.py tasks     in memory: build and check the task file
  cd lean && ../.venv/bin/python c2_build/transfer/T19/redo3.py write     write haiku/redo3/<task>.md + REDO3_INDEX.json
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, paths  # noqa: E402
from c2_kit.paths import never_open  # noqa: E402
from transfer.T19 import freeze_v2 as F2  # noqa: E402
from transfer.T19 import haiku_author as HA  # noqa: E402
from transfer.T19 import plugin as P  # noqa: E402
from transfer.T19 import redo2 as RD  # noqa: E402

FAMILY = P.FAMILY
VERSION = "redo3-v1"
ROOT = HERE / "haiku" / "redo3"
POOLS_V2 = F2.POOLS_V2_PREV   # the freeze this round was written against (moved aside as pools_v2_prev/ when
#                                the redo3 re-freeze closed the shortfall; pools_v2/ is the NEW freeze)
A3_REPORT = C2_BUILD / "STAGE_A3_REPORT.json"
QFORM = "yn_not_compliant"
CELL = "wording/yn_not_compliant"
KEY_PHRASE = "not compliant with"                  # redo2.PHRASES[QFORM][0]
KEY_REGEX = r"\bnot compliant\b"
N_CAND = 3                                         # redo2 asked 2 per item
EXTRA_NUM, EXTRA_DEN = 3, 2                        # ask for 50% more items than the gap
FRAMES3 = (                                        # R7: six new openings (candidate 1 is preferred)
    "open with 'Using the card's definitions,'",
    "open with 'With the records in front of you,'",
    "open with 'Measured against the card,'",
    "open with 'After checking the evidence log,'",
    "open with 'Working from the profile and the evidence log,'",
    "open with 'In the view of a careful reviewer,'",
)
SHAPE = ("Shape (fixed): the opening, then 'is {SITE} not compliant with its checklist on the audit date?' Use the verb "
         "'is'; add nothing between 'checklist' and 'on the audit date' and nothing after 'audit date'.")


def _sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _read(path: Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _rel(p) -> str:
    try:
        return str(Path(p).resolve().relative_to(HERE))
    except ValueError:
        return str(p)


# ------------------------------------------------------------------------------------------------ the gap

def shortfalls() -> list:
    """[{item, target, admitted, shortfall}] of the pools_v2 freeze, which must equal the T19 entry of
    STAGE_A3_REPORT.json (this family's exact shortfall)."""
    man = _read(POOLS_V2 / "MANIFEST.json")
    short = list(man["shortfalls"])
    entry = next(x for x in _read(A3_REPORT) if x["id"] == FAMILY)
    texts = entry["shortfalls"]
    want = sorted(f"{s['item']}: {s['admitted']} admitted of {s['target']} (short {s['shortfall']})" for s in short)
    got = sorted(re.sub(r"\. Open item is.*$", "", t) for t in texts)
    if want != got:
        raise SystemExit(f"STAGE_A3_REPORT shortfalls {got} != pools_v2/MANIFEST.json shortfalls {want}")
    return short


def n_items(gap: int) -> int:
    """ceil(1.5 * gap) in integers."""
    return (gap * EXTRA_NUM + EXTRA_DEN - 1) // EXTRA_DEN


def pending_reads() -> dict:
    """{registry: [task names without a non-empty answer file]} for every read registry of the family, from the
    TASKS.json files the read tasks were issued from. Both lists are empty: no read is pending."""
    out = {}
    for reg in (HERE / "haiku" / "extract", RD.XROOT):
        tasks = _read(reg / "TASKS.json")
        rows = tasks.get("tasks", tasks) if isinstance(tasks, dict) else tasks
        names = rows if isinstance(rows, dict) else {r.get("name") or r.get("task_id"): r for r in rows}
        miss = []
        for name, r in sorted(names.items()):
            ans = r.get("answer_file") if isinstance(r, dict) else None
            ans = Path(ans) if ans else reg / "answers" / f"{name}.json"
            if not ans.exists() or ans.stat().st_size <= 2:
                miss.append(name)
        out[_rel(reg)] = miss
    return out


def phrase_stats() -> dict:
    """Per key phrase of the form, over every distinct form written with it in pools_v2 (admitted) or quarantine
    (rejected): {phrase: {"forms", "admitted", "read_as_other"}}; read_as_other counts forms that at least one
    reader matched to another meaning (those are rejected for good)."""
    wordings = _read(POOLS_V2 / "wordings.json")
    quar = _read(POOLS_V2 / "quarantine.json")
    rejected = list(quar["v1"].get("forms_not_admitted", [])) + list(quar["redo2"].get("forms_not_admitted", []))
    stats = {p: Counter() for p, _rx in RD.PHRASES[QFORM]}
    for src, forms in (("adm", [w for w in wordings if w["qform"] == QFORM]),
                       ("rej", [f for f in rejected if f.get("qform", QFORM) == QFORM
                                and f["form_id"].startswith("q.t19.yn_not_compliant#")])):
        for f in forms:
            low = " ".join(f["text"].split()).lower()
            for p, rx in RD.PHRASES[QFORM]:
                if re.search(rx, low):
                    stats[p]["forms"] += 1
                    stats[p]["admitted" if src == "adm" else "read_as_other"] += 1
    return {p: dict(c) for p, c in stats.items()}


def used_qids() -> set:
    """Every qid string in the family's haiku folders (round 1 and redo2 files), so a new qid cannot collide."""
    out = set()
    for p in (HERE / "haiku").rglob("*"):
        if p.is_file() and p.suffix in (".json", ".md", ".txt") and "redo3" not in p.parts:
            out |= set(re.findall(r"\bq[0-9a-f]{10}\b", p.read_text(encoding="utf-8", errors="replace")))
    return out


def new_qids(n: int) -> list:
    taken, out, i = used_qids(), [], 0
    while len(out) < n:
        q = "q" + _sha(f"{VERSION}|wordings|{QFORM}|{i}")[:10]
        i += 1
        if q not in taken and q not in out:
            out.append(q)
    return out


# ------------------------------------------------------------------------------------------------ the task

def word_item(qid: str, frames: tuple) -> dict:
    """One item: the round 1 / redo2 brief (meaning and slots unchanged), the pinned key phrase with redo2's
    negation rule, the fixed shape, and one opening per candidate."""
    meaning, _round1_rule = HA.WORDING_BRIEF[QFORM]
    rules = [f"Key phrase, word for word: '{KEY_PHRASE}' (only the verb may follow the grammar). " + RD.NEG_RULE[QFORM],
             SHAPE] + [f"Candidate {i + 1}: {fr}." for i, fr in enumerate(frames)]
    return {"qid": qid, "brief": meaning, "slots": {"SITE": "the site's name (exactly once)"}, "rules": rules}


def instructions() -> str:
    """redo2's wording prompt and redo note, with the only two phrases that name two candidates made to fit three."""
    prompt = RD._replace(RD.wording_prompt(N_CAND), "(candidate 1, candidate 2)",
                         "(candidate 1, candidate 2, candidate 3)")
    note = RD._replace(RD.NOTES["wordings"], "for candidate 1 and for candidate 2: follow it exactly",
                       "for each candidate: follow it exactly")
    return prompt + "\n\n## Redo note\n\n" + note


def build() -> list:
    """[task dict with its full text]; every check that guards an authoring task (A37 b) has run."""
    short = shortfalls()
    if [s["item"] for s in short] != [CELL] or short[0]["shortfall"] < 1:
        raise SystemExit(f"redo3 is written for the single shortfall {CELL}; found {short}")
    gap = short[0]["shortfall"]
    n = n_items(gap)
    if n * N_CAND > len(FRAMES3) or set(FRAMES3) & set(RD.FRAMES):
        raise SystemExit("openings: not enough new openings, or one repeats a redo2 opening")
    if len(set(FRAMES3)) != len(FRAMES3) or any(HA.STYLES[i] in FRAMES3 for i in range(len(HA.STYLES))):
        raise SystemExit("openings repeat each other or a round 1 style hint")
    qids = new_qids(n)
    items = [word_item(q, FRAMES3[i * N_CAND:(i + 1) * N_CAND]) for i, q in enumerate(qids)]
    name = f"{FAMILY}-redo3-wordings-000"
    answer = str(ROOT / "answers" / f"{name}.json")
    task_file = str(ROOT / f"{name}.md")
    contract = RD._contract(name, "wordings", answer, qids, N_CAND)
    if contract.count("REDO-2") != 1:
        raise SystemExit("redo2 contract header changed")
    contract = contract.replace("REDO-2", "REDO-3")
    instr = instructions()
    text = "\n".join([contract, "", "## Instructions", "", instr, "", RD._items_block(items), ""])
    probs = []
    for it in items:
        try:
            chunker.check_item("author_wording", {k: v for k, v in it.items() if k != "qid"},
                               forbid_strings=HA.QSTRINGS)
        except chunker.ChunkError as e:
            probs.append(f"{it['qid']}: {e}")
    probs += [f"forbidden string {f!r}" for f in RD._forbid_hits(text, RD.FORBID["wordings"])]
    for p in (answer, task_file):
        if never_open(p):
            probs.append(f"never-open path {p}")
    if "t19a." in text:
        probs.append("names an internal id")
    if answer not in text:
        probs.append("answer path missing from the task text")
    if probs:
        raise chunker.ChunkError(f"{name}: {probs[:6]}")
    return [{
        "name": name, "pool": "wordings", "kind": "author", "author_kind": "author_wording", "task_file": task_file,
        "answer_file": answer, "n_items": n, "n_candidates": N_CAND, "outputs_expected": n * N_CAND, "qids": qids,
        "cells": {q: CELL for q in qids}, "key_phrase": KEY_PHRASE,
        "openings": {q: list(FRAMES3[i * N_CAND:(i + 1) * N_CAND]) for i, q in enumerate(qids)},
        "prompt_sha256": _sha(instr), "task_sha256": _sha(text), "allowed_read": [task_file],
        "allowed_write": [answer], "text": text}]


RULINGS = {
    "R5_key_phrase": ("pinned to 'not compliant with' (a phrase redo2.PHRASES already allows for the form); data in "
                      "phrase_stats; the open item's two 'not in compliance with' candidates stay rejected, no "
                      "re-vote"),
    "R6_shape": ("the ending 'its checklist on the audit date?' is fixed: every admitted 'not compliant with' form has "
                 "it and the redo2 rejections added a clause around the date; stricter only, checks as written"),
    "R7_openings": ("six new openings, none in redo2.FRAMES or haiku_author.STYLES; (key phrase, opening) unique in "
                    "the form; each lint-checked in a full sample sentence by test_redo3"),
    "unchanged": ("G0_SPEC.md v1.1 and its sha256, QUESTION_MEANINGS, the 2/2 G-LEX bar, the target of 14, "
                  "WORDING_PROMPT and redo2's wording redo note (two phrases that named two candidates now fit "
                  "three: instructions()); extraction prompts for the later reads"),
}


def index(tasks: list) -> dict:
    short = shortfalls()
    pend = pending_reads()
    gap = short[0]["shortfall"]
    t = tasks[0]
    return {
        "family": FAMILY, "version": VERSION, "g0_sha256": P.T19Plugin.G0_SHA256_AUTHORED, "g0_changed": False,
        "source": {"stage_a3_report": "STAGE_A3_REPORT.json (entry T19)", "shortfalls": short,
                   "pools_v2_manifest_sha256": hashlib.sha256((POOLS_V2 / "MANIFEST.json").read_bytes()).hexdigest(),
                   "open_item_lineage": {"cell": CELL, "iid": "t19a.wording.yn_not_compliant.001",
                                         "qid": "qb8572add92", "redo2_task": "T19-redo2-wordings-000",
                                         "why": "both redo2 candidates were read as yn_out_of by at least one reader"}},
        "a_pending_reads": {"without_answers": pend, "rewrapped": [],
                            "note": "every G-LEX / G3-H read task of round 1 (7) and redo2 (5) has a non-empty answer "
                                    "file (checked from the TASKS.json registries): nothing to re-wrap. The reads of "
                                    "this round's candidates are built after the answers exist."},
        "b_authoring": {"gap": gap, "ask_factor": f"{EXTRA_NUM}/{EXTRA_DEN}", "items": n_items(gap),
                        "candidates_per_item": N_CAND, "cell": CELL},
        "phrase_stats": phrase_stats(), "rulings": RULINGS,
        "keep_rule": (f"cell {CELL} may not exceed its target 14: keep at most {gap} piece(s) in all; walk the items "
                      "in `order`, keep the first admitted candidate (written order) of the first item that has "
                      "one, discard the rest. Item 2 is a reserve for item 1."),
        "order": t["qids"],
        "selection": "as redo2's: haiku_author.check_wording, freeze.wording_problems, redo2.phrase_problems "
                     "(key phrase 'not compliant with'), exact dedup against pools_v2 and every earlier wording, "
                     "then G-LEX 2/2 with new extractor ids (redo3 reads); the unread/unkept candidates are dropped",
        "follow_up": ["load: lint the answer's candidates (redo2.lint_candidate pattern, qform yn_not_compliant)",
                      "extract: 2 G-LEX reads of each lint-clean candidate ({SITE} = 'Larch Street depot', "
                      "extract_build.PROMPT_LEX and the closed meaning list unchanged, new extractor ids); no G3-H "
                      "(no Mode F text in this round)",
                      "merge: freeze_v2 pattern adds the kept piece; expect 14 of 14 and no other shortfall; "
                      "G13-seed and the file-access audit stay pending"],
        "untouched": "haiku_author.py, extract_build.py, freeze.py, freeze_v2.py, redo2.py, plugin.py, G0_SPEC.md, "
                     "haiku/author, haiku/extract, haiku/redo2 and pools / pools_v2 are read only here",
        "tasks": [{k: v for k, v in x.items() if k != "text"} for x in tasks],
    }


README = ("T19 redo3 answers: one <task name>.json per redo3 task (see ../REDO3_INDEX.json), a JSON array of "
          "{\"qid\", \"texts\": [...]}. Written only by the redo3 task agents.\n")


def files(tasks: list) -> dict:
    out = {f"{t['name']}.md": t["text"] for t in tasks}
    out["REDO3_INDEX.json"] = json.dumps(index(tasks), ensure_ascii=False, indent=1) + "\n"
    out["answers/README.txt"] = README
    return out


def write() -> list:
    fs = files(build())
    clash = [rel for rel, text in fs.items()
             if (ROOT / rel).exists() and (ROOT / rel).read_text(encoding="utf-8") != text]
    if clash:
        raise SystemExit(f"files already exist with other content (written once): {clash[:5]}")
    return [str(p) for p in paths.write_files(ROOT, fs)]


def main(argv=None) -> int:
    cmd = (argv or sys.argv[1:] or ["tasks"])[0]
    tasks = build()
    if cmd == "tasks":
        print(json.dumps({"n_tasks": len(tasks), "items": sum(t["n_items"] for t in tasks),
                          "outputs_expected": sum(t["outputs_expected"] for t in tasks),
                          "pending_reads": pending_reads(), "qids": tasks[0]["qids"]}, indent=1))
        return 0
    if cmd == "write":
        for p in write():
            print(p)
        return 0
    raise SystemExit("usage: redo3.py tasks|write")


if __name__ == "__main__":
    sys.exit(main())

"""c2_build/families/T26/freeze_v2.py: the T26 pool re-freeze (pools_v2/) after the redo and redo2 Haiku rounds
(G0_SPEC.md sections 4 and 7 R1, R2; C2_DATA_SPEC 6.3 G-SL, G-LEX, G3-H; PREREG A37 (b), A38).

Why a new script. record_freeze.py (v1) reads only haiku/author and haiku/extract, and it asks for held-out wordings
that the authoring pass never made. The redo2 authoring answers (16 yn_fails wordings, 54 held-out wordings) have no
ingest path in v1, and they still need their own G-LEX reads. Nothing in v1 is edited: pools/, haiku/author,
haiku/extract, authoring_ingest.py and record_freeze.py stay byte for byte as they are. This script reads them and writes
only NEW files: pools_v2/ (freeze) and haiku/redo2/extract/ (the redo2 G-LEX read tasks, `reads`).

What a run does (every write goes through the kit's guarded writers, after A38 only):
  1. Validates EVERY answer file of every round against its contract (validate_answer_bytes; never edits a file):
       author, redo (fold sources), redo2 (authoring), extract (v1 G-LEX reads and G3-H), redo2/extract (redo2 reads),
       and the pre-fold backups (informational). A file that breaks its contract is REJECTED whole (not JSON, not an
       array, a wrong key set, a qid missing / unknown / twice, a wrong object count); an item whose value breaks the
       contract (empty text, a line break where the task says one line, a meaning that is not one of the item's choices
       and not NONE) is rejected alone. Rejected answers are treated as unanswered, never as a vote.
  2. Rebuilds the v1 pipeline from the validated answers only (authoring batches, lint, dedup, held-out pack
       designation, registry, extraction batches), checks the rebuild against the files on disk byte for byte, records
       the v1 G-LEX reads (one extractor id per read; 2/2 for question wordings, 3/3 for precedence) and scores the
       G3-H round trip (>= 98% per template; a mismatched row is always dropped).
  3. Ingests the redo2 wordings (training yn_fails, G0 section 7 R1; held-out wordings for sampler S5, R2): the unchanged
       wording lint, dedup against every first-pass wording, every fixture stand-in and each other, registry forms
       (held_out=True for R2), unit tests. Their G-LEX reads are TWO independent reads of the unchanged LEX_PROMPT and
       choices (decoys included) in separate chunk files (haiku/redo2/extract/, written by `reads`). A form without
       its two reads stays pending; one disagreeing read rejects it for good. No read is invented here.
  4. Applies every gate and target of G0 (never lowered) and freezes pools_v2/ with MANIFEST.json (sha256 per file, counts,
       targets, shortfalls, validation, reads still pending, how to load the pools). READY only when every G0 minimum is
       met, the G-LEX gate passes over every form the pools use, G3-H passes and no authoring task lacks a valid
       answer (rejected answers show in the manifest; their pieces are simply missing from the counts).

  5. Folds the redo3 round (haiku/redo3/, built by haiku/redo3/build_redo3.py and build_reads.py; added in the T26 redo3
       fold). redo3 holds three kinds of answers, all validated against their task contract like every other round:
       (a) redo3/answers/T26-extract_lex-*: the G-LEX reads of the redo2 wordings, re-issued as self-contained task files
           with the SAME task ids, qids, items and choices as haiku/redo2/extract/chunks. They are the redo2 reads
           (extractor ids glex-question-r2read1 / -r2read2): an answer in haiku/redo2/extract/answers wins when both
           exist and are valid (a difference is reported, never merged); otherwise the redo3 answer is the read.
       (b) redo3/answers/T26-author_wording-*: the top-up wordings (4 training yn_fails, 15 held-out). Same ingest as
           redo2: the unchanged wording lint, dedup against every earlier wording (any status) and the fixture
           stand-ins, registry (held_out=True for the held-out pool), unit test.
       (c) redo3/reads/answers/T26-extract_lex-*: the two independent G-LEX reads of those new wordings (extractor ids
           glex-question-r3read1 / -r3read2). Only 2/2 admits; one disagreeing read rejects for good.
     The rebuilt task files are compared with the files on disk (what the agents saw); a difference stops the freeze.
     `build(redo3=False)` gives the pre-redo3 state (build_reads.py uses it: it derives the redo3 read tasks from it).

No label is set anywhere: golds come only from solver A and solver B (A37 b); Haiku output can only admit or drop a
form or a document.

Flow: `reads` once (the redo2 G-LEX read tasks), the orchestrator dispatches them, `freeze` again after the answers land.
The redo3 task files already exist (build_redo3.py, build_reads.py); `freeze` reads their answers when present.

  ../.venv/bin/python -m families.T26.freeze_v2 check     (from lean/c2_build; in memory, prints a summary)
  ../.venv/bin/python -m families.T26.freeze_v2 reads     (writes haiku/redo2/extract/: the redo2 G-LEX read tasks)
  ../.venv/bin/python -m families.T26.freeze_v2 freeze    (writes pools_v2/)
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from types import SimpleNamespace

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, g3h, paths  # noqa: E402
from c2_kit.lexicon import LexiconRegistry, question_sem  # noqa: E402
from families.T26 import authoring_ingest as AI  # noqa: E402
from families.T26 import plugin as P  # noqa: E402
from families.T26 import record_freeze as RF  # noqa: E402

FAMILY = P.FAMILY
VERSION = "freeze-v2"
V1_POOLS = HERE / "pools"
POOLS_V2 = HERE / "pools_v2"
HAIKU = HERE / "haiku"
AUTHOR = HAIKU / "author"
EXTRACT = HAIKU / "extract"
REDO = HAIKU / "redo"
REDO2 = HAIKU / "redo2"
R2X = REDO2 / "extract"
REDO3 = HAIKU / "redo3"
R3_ANSWERS = REDO3 / "answers"        # redo3 authoring answers + the re-issued G-LEX reads of the redo2 wordings
R3X = REDO3 / "reads"                 # G-LEX reads of the NEW redo3 wordings (own chunks / answers)
G0 = HERE / "G0_SPEC.v1_1.md"      # the text the pools were authored and frozen under (G0_SPEC.md is v1.2)

# G0 targets (G0_SPEC.md sections 1 S27, 4, 7; C2_DATA_SPEC 3.0). Never lowered: v1's table plus the R2 held-out floor.
TARGET = dict(RF.TARGET)
FORMS = tuple(TARGET["wording_per_form"])
HELD_OUT_PER_FORM = 3                 # G0 section 7 R2: >= 3 admitted held-out wordings per form (24 in all)
MODE_T_MIN_SHARE = 0.75               # spec 3.0: Mode T >= 75% of the pool (Mode F <= 25%)
R2_READS = (("glex-question-r2read1", "t26-glex-question-r2read1-v1"),
            ("glex-question-r2read2", "t26-glex-question-r2read2-v1"))
R3_READS = (("glex-question-r3read1", "t26-glex-question-r3read1-v1"),
            ("glex-question-r3read2", "t26-glex-question-r3read2-v1"))
R2_AUTHOR_POOLS = ("wording", "wording_heldout")
LEX_PROMPT_SHA = "2aa999a4fa05aeaedcff5edfee07ba4dd94433f3a7cb900a74625718d6a2561a"   # the unchanged G-LEX read prompt

# what each task kind's answer objects must hold besides "qid" (the contract in the task files)
REQUIRED = {"author_pack": ("counterparty", "domain_label"), "author_skin": ("text",), "author_wording": ("text",),
            "author_freeform": ("text",), "author_lexicon": ("text",), "extract_lex": ("meaning",),
            "extract_g3h": ("requester", "counterparty", "change", "req_id")}
NULLABLE = {"extract_g3h"}            # "Write null for a field the text does not state"


# ======================================================================================================= 1. validation

class _Strict(ValueError):
    pass


def _no_dup_pairs(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise _Strict(f"duplicate key {k!r} in an object")
        out[k] = v
    return out


def _no_const(name):
    raise _Strict(f"{name} is not valid JSON for an answer")


@dataclass
class ChunkDef:
    """What one Haiku task gave the agent: its qids (and choices), kind, and whether the task says one line."""
    task_id: str
    kind: str
    pool: str
    qids: list
    answer_file: str | None = None
    one_line: bool = False
    choices: dict = field(default_factory=dict)       # qid -> allowed meanings (extract_lex)
    source: str = ""


def defs_from_chunks(chunk_dir: Path) -> dict:
    """{task_id: ChunkDef} from the chunk files an agent read (author, extract, redo2/extract)."""
    out = {}
    if not chunk_dir.is_dir():
        return out
    for f in sorted(chunk_dir.glob("*.json")):
        c = json.loads(f.read_text(encoding="utf-8"))
        items = c["items"]
        out[c["task_id"]] = ChunkDef(c["task_id"], c["kind"], c.get("pool", ""), [i["qid"] for i in items],
                                     c.get("answer_file"), False,
                                     {i["qid"]: list(i["choices"]) for i in items if "choices" in i}, f.name)
    return out


def def_from_task_text(path: Path, pool: str) -> ChunkDef:
    """A self-contained task file (redo, redo2): kind, qids, answer path and the one-line rule come from its own text."""
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    head = lines[0]                      # "TASK <id>  (kind <kind>, <n> items)" or "REDO TASK <id>  (kind ...)"
    toks = head.split()
    tid = toks[2] if toks[0] == "REDO" else toks[1]
    kind = head.split("(kind ", 1)[1].split(",", 1)[0].strip()
    ans = next(ln.split("): ", 1)[1].strip() for ln in lines if ln.startswith("answer_file ("))
    start = next(i for i, ln in enumerate(lines) if ln.startswith("=== ITEMS"))
    items = [json.loads(ln) for ln in lines[start + 1:] if ln.strip()]
    return ChunkDef(tid, kind, pool, [i["qid"] for i in items], ans, "on one line (no line break)" in text, {},
                    path.name)


def validate_answer_bytes(data: bytes, cd: ChunkDef) -> dict:
    """Validate one answer file against its task. Never edits anything.

    file-level problems reject the file: not UTF-8 / not JSON, a BOM, a duplicate object key, a top level that is not an
    array, an element that is not an object, a key set other than {"qid"} + the kind's fields, a qid that is not a
    string / is unknown / is used twice, an object count other than the chunk's, a qid left unanswered.
    item-level problems reject only that item: an empty or non-string value; a line break in a text the task says is one
    line; a meaning that is neither one of the item's choices nor NONE.
    Returns {"ok", "n_expected", "n_valid_items", "file_problems", "item_problems", "items"} (items = accepted ones)."""
    rep = {"ok": False, "n_expected": len(cd.qids), "n_valid_items": 0, "file_problems": [], "item_problems": [],
           "items": []}
    fp = rep["file_problems"]
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as e:
        fp.append(f"not UTF-8: {e}")
        return rep
    if text.startswith("﻿"):
        fp.append("starts with a byte-order mark")
        return rep
    try:
        obj = json.loads(text, object_pairs_hook=_no_dup_pairs, parse_constant=_no_const)
    except (ValueError, _Strict) as e:
        fp.append(f"not valid JSON: {e}")
        return rep
    if not isinstance(obj, list):
        fp.append("the top level is not a JSON array")
        return rep
    if cd.kind not in REQUIRED:
        fp.append(f"unknown task kind {cd.kind!r}")
        return rep
    want = {"qid", *REQUIRED[cd.kind]}
    qset, seen = set(cd.qids), {}
    for i, el in enumerate(obj):
        if not isinstance(el, dict):
            fp.append(f"element {i} is not an object")
            continue
        if set(el) != want:
            fp.append(f"element {i}: keys {sorted(el)} differ from the contract {sorted(want)}")
            continue
        qid = el["qid"]
        if not isinstance(qid, str):
            fp.append(f"element {i}: qid is not a string")
        elif qid not in qset:
            fp.append(f"element {i}: unknown qid {qid}")
        elif qid in seen:
            fp.append(f"qid {qid} used twice")
        else:
            seen[qid] = el
    if len(obj) != len(cd.qids):
        fp.append(f"{len(obj)} objects; the contract says exactly {len(cd.qids)}")
    missing = [q for q in cd.qids if q not in seen]
    if missing:
        fp.append(f"{len(missing)} qid(s) not answered (first: {missing[0]})")
    if fp:
        return rep
    for qid in cd.qids:
        el = seen[qid]
        bad = []
        for k in REQUIRED[cd.kind]:
            v = el[k]
            if v is None and cd.kind in NULLABLE:
                continue
            if not isinstance(v, str) or not v.strip():
                bad.append(f"{k} is not a non-empty string")
            elif cd.one_line and k == "text" and ("\n" in v or "\r" in v):
                bad.append("text has a line break (the task says one line)")
        if cd.kind == "extract_lex" and not bad:
            m = el["meaning"]
            if m != "NONE" and m not in cd.choices.get(qid, ()):
                bad.append("meaning is neither one of the item's choices nor NONE")
        if bad:
            rep["item_problems"].append(f"{qid}: " + "; ".join(bad))
        else:
            rep["items"].append(el)
    rep["ok"] = True
    rep["n_valid_items"] = len(rep["items"])
    return rep


def _rel(p: Path) -> str:
    try:
        return p.resolve().relative_to(HERE.resolve()).as_posix()
    except ValueError:
        return str(p)


def validate_round(name: str, defs: dict, answers_dir: Path) -> dict:
    """Validate every answer file of one round. A task with no file is `missing`; a file with no task is `stray`
    (never used)."""
    files, stray, missing = {}, [], []
    present = {}
    if answers_dir.is_dir():
        present = {p.name: p for p in sorted(answers_dir.iterdir()) if p.is_file()}
    for tid, cd in defs.items():
        p = present.get(f"{tid}.json")
        if p is None:
            missing.append(tid)
            continue
        paths.check_path(p)
        data = p.read_bytes()
        rep = validate_answer_bytes(data, cd)
        rep.update({"file": _rel(p), "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data), "kind": cd.kind})
        files[tid] = rep
    for n in present:
        if not n.endswith(".json") or n[:-5] not in defs:
            stray.append(n)
    rejected = sorted(t for t, r in files.items() if not r["ok"])
    return {"round": name, "dir": _rel(answers_dir), "tasks": len(defs), "files": files, "missing": sorted(missing),
            "stray": stray, "rejected": rejected,
            "item_rejects": sum(len(r["item_problems"]) for r in files.values())}


def accepted(round_rep: dict) -> dict:
    """{task_id: accepted answer objects} of a validated round (rejected files and rejected items are absent)."""
    return {t: r["items"] for t, r in round_rep["files"].items() if r["ok"]}


def slim(round_rep: dict) -> dict:
    """The round report without the accepted items (for the manifest and the validation report)."""
    out = {k: v for k, v in round_rep.items() if k != "files"}
    out["files"] = {t: {k: v for k, v in r.items() if k != "items"} for t, r in round_rep["files"].items()}
    return out


# ======================================================================================================= 2. v1 rebuild

def load_pieces(batches: dict, tasks: dict, raw_author: dict) -> tuple:
    """AI.load_pieces over validated answers only: (pieces, coverage)."""
    pieces, coverage = [], {}
    for pool in AI.POOLS:
        b = batches[pool]
        raw, missing = {}, []
        for t in tasks["tasks"]:
            if t["pool"] != pool:
                continue
            tid = Path(t["task_file"]).stem
            if tid in raw_author:
                raw[tid] = raw_author[tid]
            else:
                missing.append(tid)
        got, probs = chunker.load_answers(b, raw)
        items = chunker.item_by_internal(b)
        task_of = {b.key[q]: b.task_of[q] for q in b.key}
        coverage[pool] = {"items": len(b.key), "answered": len(got), "missing_tasks": missing, "problems": probs,
                          "tasks": sum(1 for t in tasks["tasks"] if t["pool"] == pool)}
        for iid, a in sorted(got.items()):
            item = {k: v for k, v in items[iid].items() if k != "qid"}
            pieces.append({"pool": pool, "internal_id": iid, "task_id": task_of[iid], "prompt_sha": b.prompt_sha,
                           "item": item, "answer": a, "problems": [], "meta": AI._meta(iid)})
    return pieces, coverage


def effective_author_answers(rep_author: dict, rep_redo: dict) -> tuple:
    """The author answers v1 used: a validated redo answer replaces the original of the same task (the redo task copies
    its answer to the original path); otherwise the validated original. Returns (raw, source, notes)."""
    raw, source, notes = {}, {}, []
    acc_a, acc_r = accepted(rep_author), accepted(rep_redo)
    for tid in sorted(set(rep_author["files"]) | set(acc_r)):
        a_ok, r_ok = tid in acc_a, tid in acc_r
        if r_ok:
            raw[tid], source[tid] = acc_r[tid], "redo"
            if tid in rep_author["files"]:
                same = rep_author["files"][tid]["sha256"] == rep_redo["files"][tid]["sha256"]
                if not same:
                    notes.append(f"{tid}: the author file differs from the redo answer; the redo answer is used")
        elif a_ok:
            raw[tid], source[tid] = acc_a[tid], "author"
            if tid in rep_redo["files"]:
                notes.append(f"{tid}: the redo answer was rejected; the original author answer is used")
        else:
            notes.append(f"{tid}: no valid answer")
    return raw, source, notes


def _raw_for(batch, accepted_raw: dict) -> dict:
    return {c["task_id"]: accepted_raw[c["task_id"]] for c in batch.chunks if c["task_id"] in accepted_raw}


def record_reads(reg, lex: list, accepted_raw: dict) -> list:
    """RF.record_reads over validated answers: one extractor id per read; a form the read did not answer gets no record
    (pending); NONE and a text that is not one of the choices both record as no meaning (a mismatch)."""
    out = []
    for name, b in lex:
        kind = reg.forms[next(iter(b.key.values()))].kind
        got, probs = chunker.load_answers(b, _raw_for(b, accepted_raw))
        stats = Counter()
        for fid in sorted(b.key.values()):
            if fid not in got:
                stats["unanswered"] += 1
                continue
            m = got[fid].get("meaning") if isinstance(got[fid], dict) else None
            sem = reg.meaning_to_sem(kind, m) if isinstance(m, str) else None
            if sem is None:
                stats["NONE" if m == "NONE" else "not_a_choice"] += 1
            elif sem == reg.forms[fid].sem_id:
                stats["match"] += 1
            else:
                stats["other_meaning"] += 1
            reg.record_extraction(fid, name, sem)
        out.append({"read": name, "kind": kind, "batch_id": b.batch_id, "items": len(b.key), "chunks": len(b.chunks),
                    "answered_tasks": sorted(t for t in accepted_raw if t in {c["task_id"] for c in b.chunks}),
                    "outcomes": dict(sorted(stats.items())), "chunk_problems": probs})
    return out


def g3h_check(g3, expected: dict, accepted_raw: dict) -> tuple:
    """RF.g3h_check over validated answers: per-template pass rate (98% bar); an unanswered document fails."""
    got, probs = chunker.load_answers(g3, _raw_for(g3, accepted_raw))
    results, detail = [], {}
    for iid in sorted(expected):
        m = AI._meta(iid)
        tmpl = f"{m['register']}|{m['tone']}"
        if iid not in got:
            ok, diffs = False, ["unanswered"]
        else:
            ok, diffs = g3h.compare(expected[iid], got[iid], AI.FIELDS_G3H)
        results.append((tmpl, iid, ok))
        detail[iid] = {"template": tmpl, "ok": ok, "diffs": diffs}
    return g3h.template_report(results), detail, probs


# ======================================================================================================= 3. redo2 wordings

def load_build_redo2():
    spec = importlib.util.spec_from_file_location("t26_build_redo2", REDO2 / "build_redo2.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def r2_author_batches(R) -> dict:
    """The two redo2 authoring batches, rebuilt exactly as build_redo2.build() does: {pool: TaskBatch}."""
    import random
    rng = random.Random(f"T26|author|{R.VERSION}")
    plan = [("wording", R.fails_items(rng), R.prompt(False), 16, f"t26-redo2-wording-yn_fails-{R.VERSION}"),
            ("wording_heldout", R.held_items(rng), R.prompt(True), 27, f"t26-redo2-wording_heldout-{R.VERSION}")]
    return {pool: chunker.make_batch("author_wording", FAMILY, items, seed=seed, prompt=instr, max_items=size,
                                     forbid_strings=R.FORBID) for pool, items, instr, size, seed in plan}


def r2_pieces(batches: dict, accepted_raw: dict) -> tuple:
    """(pieces, coverage) of the redo2 authoring answers, in the v1 piece layout (+ held_out)."""
    pieces, coverage = [], {}
    for pool in R2_AUTHOR_POOLS:
        b = batches[pool]
        got, probs = chunker.load_answers(b, _raw_for(b, accepted_raw))
        items = chunker.item_by_internal(b)
        task_of = {b.key[q]: b.task_of[q] for q in b.key}
        coverage[pool] = {"items": len(b.key), "answered": len(got), "problems": probs,
                          "missing_tasks": sorted(c["task_id"] for c in b.chunks if c["task_id"] not in accepted_raw)}
        for iid, a in sorted(got.items()):
            item = {k: v for k, v in items[iid].items() if k != "qid"}
            pieces.append({"pool": pool, "internal_id": iid, "task_id": task_of[iid], "prompt_sha": b.prompt_sha,
                           "item": item, "answer": a, "problems": [], "meta": {"qform": iid.split("|")[2]},
                           "held_out": pool == "wording_heldout"})
    return pieces, coverage


def r2_lint_dedup(pieces: list, taken: set) -> list:
    """The unchanged wording lint, then dedup: a text equal (normalised) to a fixture stand-in or to any first-pass
    wording form (kept, rejected or pending: the registry would refuse it anyway, and a rejected text is never re-read)
    or repeated inside redo2 is dropped; the same text under two question forms drops every redo2 copy."""
    from families.T26 import fixtures as FX
    stand_in = {AI._norm(t) for _, _, t in FX.WORDINGS} | {AI._norm(t) for t in FX.PREC_FORMS}
    for p in pieces:
        p["problems"] = AI.lint_wording(AI._value(p), p["meta"]["qform"])
    seen = {}
    for p in sorted(pieces, key=lambda x: (x["held_out"], x["internal_id"])):
        if p["problems"]:
            continue
        key = AI._norm(AI._value(p))
        if key in stand_in:
            p["problems"].append("dedup: a copy of a fixture stand-in")
        elif key in taken:
            p["problems"].append("dedup: repeats a first-pass wording")
        elif key in seen:
            p["problems"].append(f"dedup: repeats {seen[key]}")
        else:
            seen[key] = p["internal_id"]
    by_text = defaultdict(list)
    for p in pieces:
        if not p["problems"]:
            by_text[AI._norm(AI._value(p))].append(p)
    for group in by_text.values():
        if len({p["meta"]["qform"] for p in group}) > 1:
            for p in group:
                p["problems"].append("dedup: the same text under two question forms")
    return pieces


def r2_register(reg, pieces: list) -> list:
    """Add each surviving redo2 wording to the registry (held_out=True for R2) and unit-test it. Returns the form ids
    that need their two G-LEX reads (lint-clean, registered, unit test passed)."""
    need = []
    for p in pieces:
        if p["problems"]:
            continue
        qf = p["meta"]["qform"]
        try:
            f = reg.add(AI._value(p).strip(), question_sem(FAMILY, qf), slots={"REQ_ID": "id"}, source="haiku",
                        family=FAMILY, haiku_task_id=p["task_id"], haiku_prompt_sha=p["prompt_sha"],
                        held_out=p["held_out"])
        except Exception as e:                       # a registry refusal is logged and the piece dropped, never patched
            p["problems"].append(f"registry: {e}")
            continue
        p["form_id"] = f.form_id
        reg.unit_test(f.form_id)
        if f.unit_ok:
            need.append(f.form_id)
    return sorted(need)


def _finalize(batch, pool: str, prompt: str, root: Path):
    """Chunk files in the v1 extraction layout (answer_file + instructions inside the chunk) under `root`."""
    for i, c in enumerate(batch.chunks):
        ans = str(root / batch.answer_path(c["task_id"]))
        batch.chunks[i] = {"task_id": c["task_id"], "kind": c["kind"], "pool": pool, "prompt_sha": c["prompt_sha"],
                           "answer_file": ans, "instructions": prompt.split("\n"), "items": c["items"]}
        if any(iid in json.dumps(batch.chunks[i], ensure_ascii=False) for iid in batch.key.values()):
            raise chunker.ChunkError("an extraction task file names an internal id")
    return batch


def r2_read_batches(reg, fids: list, root: Path = R2X, reads: tuple = R2_READS) -> list:
    """The two independent G-LEX reads of the redo2 forms (reads=R3_READS: of the redo3 forms): separate batches (own
    seed, qids, item and choice order), the unchanged LEX_PROMPT and choices (the registry's question meanings, decoys
    included)."""
    out = []
    if not fids:
        return out
    for name, seed in reads:
        items = reg.lexicon_items(sorted(fids), seed=seed)
        b = chunker.make_batch("extract_lex", FAMILY, items, seed=seed, prompt=AI.LEX_PROMPT, max_items=50)
        out.append((name, _finalize(b, name, AI.LEX_PROMPT, root)))
    return out


def r2_task_rows(batches: list, root: Path = R2X) -> list:
    return [{"task_file": str(root / b.chunk_path(c["task_id"])), "answer_file": c["answer_file"], "kind": b.kind,
             "pool": c["pool"], "batch_id": b.batch_id, "n_items": len(c["items"]), "prompt_sha": b.prompt_sha}
            for _, b in batches for c in b.chunks]


def r2_read_files(batches: list, root: Path = R2X) -> dict:
    """{relative path: text} of everything `reads` writes (chunks, prompt, key, manifest, TASKS.json)."""
    files = {}
    for _, b in batches:
        files.update(b.files())
    rows = r2_task_rows(batches, root)
    per_pool = Counter()
    for r in rows:
        per_pool[r["pool"]] += r["n_items"]
    files["TASKS.json"] = json.dumps({
        "family": FAMILY, "version": "redo2-extract-v1", "n_tasks": len(rows), "items_per_pool": dict(per_pool),
        "note": ("G-LEX reads of the redo2 wordings (G0 section 7 R1, R2): two independent reads, each form once per "
                 "read, in separate chunk files; the unchanged LEX_PROMPT and meaning choices. One fresh Haiku agent "
                 "per task_file; it reads only that file and writes only its answer_file. key/ and manifest/ are "
                 "orchestrator-only. A read only flags: it never sets a label."),
        "tasks": rows}, ensure_ascii=False, indent=1) + "\n"
    return files


def diff_files(files: dict, root: Path) -> list:
    out = []
    for rel, text in sorted(files.items()):
        p = root / rel
        if not p.exists():
            out.append(f"missing {rel}")
        elif p.read_text(encoding="utf-8") != text:
            out.append(f"differs {rel}")
    return out


# ======================================================================================================= 3b. redo3

def load_build_redo3():
    """haiku/redo3/build_redo3.py as a module (it rebuilds the redo3 task files and the top-up authoring batches)."""
    spec = importlib.util.spec_from_file_location("t26_build_redo3", REDO3 / "build_redo3.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def redo3_defs(tasks: dict) -> tuple:
    """({task_id: ChunkDef}, {task_id: task row}) of the redo3 tasks (redo3/TASKS.json), as the agents saw them.

    A `read` task is the G-LEX read of a redo2 wording under the SAME task id: its qids and choices come from
    haiku/redo2/extract/chunks (and must equal the items of the redo3 task text); its answer path is the redo3 one.
    An `author` task is parsed from its own text (kind, qids, answer path, one-line rule)."""
    defs, rows = {}, {}
    r2x = defs_from_chunks(R2X / "chunks")
    for t in tasks["tasks"]:
        f = Path(t["task_file"])
        tid = f.stem
        rows[tid] = t
        tcd = def_from_task_text(f, t["pool"])
        if t["kind"] == "author":
            cd = tcd
        else:
            src = r2x.get(tid)
            if src is None:
                raise SystemExit(f"{tid}: no redo2 read chunk with this task id")
            if tcd.qids != src.qids or tcd.kind != src.kind:
                raise SystemExit(f"{tid}: the redo3 task file differs from its redo2 source chunk")
            cd = ChunkDef(src.task_id, src.kind, src.pool, list(src.qids), tcd.answer_file, False, dict(src.choices), f.name)
        if cd.answer_file != t["answer_file"] or cd.answer_file != str(R3_ANSWERS / f"{tid}.json"):
            raise SystemExit(f"{tid}: answer path {cd.answer_file}")
        defs[tid] = cd
    return defs, rows


def effective_read_answers(primary: dict, alt: dict) -> tuple:
    """The answers that count as the redo2 G-LEX reads: primary = valid answers in haiku/redo2/extract/answers, alt = the
    valid redo3 re-issue of the same task ids. Per task id the primary answer is used when it exists (the original
    location); the redo3 one only fills a task the primary lacks. Two valid answers that differ are reported, never
    merged and never both counted (one task id is one vote). Returns ({task_id: items}, {task_id: source}, notes)."""
    raw, source, notes = {}, {}, []
    for tid in sorted(set(primary) | set(alt)):
        if tid in primary:
            raw[tid], source[tid] = primary[tid], "redo2/extract"
            if tid in alt and alt[tid] != primary[tid]:
                notes.append(f"{tid}: haiku/redo2/extract and haiku/redo3 both hold a valid answer and they differ; "
                             "the redo2/extract answer is used and the redo3 one is not counted")
        else:
            raw[tid], source[tid] = alt[tid], "redo3"
    return raw, source, notes


def r3_read_files(batches: list, B3) -> dict:
    """{relative path under haiku/redo3/reads: text} of the redo3 G-LEX read tasks as build_reads.py wrote them:
    the batch files (chunks, prompt, key, manifest) and one self-contained task text per chunk."""
    files = {}
    for _, b in batches:
        files.update(b.files())
        for c in b.chunks:
            files[f"{c['task_id']}.txt"] = B3.extract_text(c, AI.LEX_PROMPT, c["answer_file"])
    return files


# ======================================================================================================= 4. targets

def evaluate_targets(*, packs_train: int, packs_ho: int, train_regs: list, ho_regs: list, prec_n: int,
                     train_by_form: dict, ho_by_form: dict, mode_t: int, mode_f: int,
                     cand_train: dict | None = None, cand_ho: dict | None = None) -> tuple:
    """(targets, shortfalls): every G0 minimum, never lowered. cand_*: wordings per form still pending their reads."""
    shortfalls, cand_train, cand_ho = [], cand_train or {}, cand_ho or {}

    def tgt(name, bar, got, note="", extra=None):
        rec = {"bar": bar, "got": got, "pass": got >= bar}
        if got < bar:
            sf = {"target": name, "bar": bar, "got": got, "short_by": bar - got, "note": note}
            sf.update(extra or {})
            shortfalls.append(sf)
        return rec

    targets = {
        "packs_training": tgt("packs training", TARGET["packs_training"], packs_train),
        "packs_heldout": tgt("packs held-out", TARGET["packs_heldout"], packs_ho),
        "skin_registers_training": tgt("skin registers (training)", TARGET["skin_registers_training"], len(train_regs),
                                       f"registers with kept skins: {sorted(train_regs)}"),
        "skin_registers_heldout": tgt("skin registers (held-out)", TARGET["skin_registers_heldout"], len(ho_regs),
                                      f"registers with kept held-out skins: {sorted(ho_regs)}"),
        "precedence_admitted": tgt("precedence paraphrases admitted 3/3", TARGET["precedence_admitted"], prec_n),
    }
    wording = {}
    for qf, bar in TARGET["wording_per_form"].items():
        wording[qf] = tgt(f"wording {qf} (training)", bar, train_by_form.get(qf, 0),
                          extra={"pending_reads": cand_train.get(qf, 0)})
    targets["wording_total"] = tgt("wording total, training (sum of per-form bars)",
                                   sum(TARGET["wording_per_form"].values()), sum(train_by_form.values()))
    held = {}
    for qf in TARGET["wording_per_form"]:
        held[qf] = tgt(f"held-out wording {qf} (sampler S5)", HELD_OUT_PER_FORM, ho_by_form.get(qf, 0),
                       extra={"pending_reads": cand_ho.get(qf, 0)})
    targets["heldout_wording_total"] = tgt("held-out wordings, all forms", HELD_OUT_PER_FORM * len(FORMS),
                                           sum(ho_by_form.values()))
    total = mode_t + mode_f
    f_share = mode_f / total if total else 0.0
    t_share = 1.0 - f_share if total else 0.0
    targets["mode_t_share"] = {"bar": MODE_T_MIN_SHARE, "got": round(t_share, 4), "pass": t_share >= MODE_T_MIN_SHARE}
    targets["mode_f_share"] = {"bar": TARGET["mode_f_max_share"], "got": round(f_share, 4),
                               "pass": f_share <= TARGET["mode_f_max_share"], "note": "max"}
    if not targets["mode_t_share"]["pass"] or not targets["mode_f_share"]["pass"]:
        shortfalls.append({"target": "Mode T / Mode F share (of pieces)", "bar": f"T >= {MODE_T_MIN_SHARE}, "
                           f"F <= {TARGET['mode_f_max_share']}", "got": f"T {round(t_share, 4)}, F {round(f_share, 4)}",
                           "short_by": None, "note": "the row builder must cap Mode F rows at 25%"})
    return {"base": targets, "wording": wording, "wording_heldout": held}, shortfalls


# ======================================================================================================= 5. the build

def build(raw_override: dict | None = None, redo3: bool = True) -> SimpleNamespace:
    """The whole freeze in memory. raw_override (tests only): {round: {task_id: accepted answer objects}} replacing
    what is read from disk for the named rounds ("author", "extract", "r2author", "r2extract" = every answer that counts as
    a redo2 G-LEX read, "r3author", "r3extract" = the reads of the redo3 wordings). redo3=False ignores haiku/redo3 (the
    pre-redo3 state; build_reads.py derives the redo3 read tasks from it)."""
    s = SimpleNamespace()
    ov = raw_override or {}
    s.a38 = paths.a38_frozen(paths.PREREG.read_text(encoding="utf-8"))
    s.checks = {}

    # ---- 1. validate every answer file of every round
    author_defs = defs_from_chunks(AUTHOR / "chunks")
    redo_tasks = json.loads((REDO / "TASKS.json").read_text(encoding="utf-8"))["tasks"]
    redo_defs = {}
    for t in redo_tasks:
        f = Path(t["task_file"])
        redo_defs[f.stem] = def_from_task_text(f, t["pool"])
    extract_defs = defs_from_chunks(EXTRACT / "chunks")
    r2_tasks = json.loads((REDO2 / "TASKS.json").read_text(encoding="utf-8"))["tasks"]
    r2_defs = {}
    for t in r2_tasks:
        f = Path(t["task_file"])
        r2_defs[f.stem] = def_from_task_text(f, t["pool"])
    r2x_defs = defs_from_chunks(R2X / "chunks")
    rounds = {
        "author": validate_round("author", author_defs, AUTHOR / "answers"),
        "redo": validate_round("redo", redo_defs, REDO / "answers"),
        "extract": validate_round("extract", extract_defs, EXTRACT / "answers"),
        "redo2_author": validate_round("redo2_author", r2_defs, REDO2 / "answers"),
        "redo2_extract": validate_round("redo2_extract", r2x_defs, R2X / "answers"),
        "backup_author_prefold": validate_round("backup_author_prefold", author_defs,
                                                REDO / "fold_backup_pre" / "author_answers"),
        "backup_extract_prefold": validate_round("backup_extract_prefold", extract_defs,
                                                 REDO / "fold_backup_pre" / "extract" / "answers"),
    }
    # the redo3 round (6 tasks in redo3/answers: re-issued redo2 reads + top-up authoring; 2 reads of the new wordings)
    s.redo3 = bool(redo3 and (REDO3 / "TASKS.json").exists())
    r3_defs, r3x_defs, raw_r3_reads_of_r2, raw_r3_author, raw_r3_extract = {}, {}, {}, {}, {}
    if s.redo3:
        r3_defs, _ = redo3_defs(json.loads((REDO3 / "TASKS.json").read_text(encoding="utf-8")))
        rounds["redo3"] = validate_round("redo3", r3_defs, R3_ANSWERS)
        r3x_defs = defs_from_chunks(R3X / "chunks")
        rounds["redo3_reads"] = validate_round("redo3_reads", r3x_defs, R3X / "answers")
        acc3 = accepted(rounds["redo3"])
        raw_r3_reads_of_r2 = {t: acc3[t] for t, cd in r3_defs.items() if cd.kind == "extract_lex" and t in acc3}
        raw_r3_author = {t: acc3[t] for t, cd in r3_defs.items() if cd.kind == "author_wording" and t in acc3}
        raw_r3_extract = accepted(rounds["redo3_reads"])
    s.rounds = rounds
    s.checks["redo_tasks_match_source_chunks"] = all(
        t in author_defs and author_defs[t].qids == cd.qids and author_defs[t].kind == cd.kind
        for t, cd in redo_defs.items())
    raw_author, author_source, author_notes = effective_author_answers(rounds["author"], rounds["redo"])
    raw_author = ov.get("author", raw_author)
    raw_extract = ov.get("extract", accepted(rounds["extract"]))
    raw_r2_author = ov.get("r2author", accepted(rounds["redo2_author"]))
    raw_r2_extract_disk, s.r2_read_source, s.r2_read_notes = effective_read_answers(
        accepted(rounds["redo2_extract"]), raw_r3_reads_of_r2)
    raw_r2_extract = ov.get("r2extract", raw_r2_extract_disk)
    raw_r3_author = ov.get("r3author", raw_r3_author)
    raw_r3_extract = ov.get("r3extract", raw_r3_extract)
    s.author_source, s.author_notes = author_source, author_notes
    s.fold_identical = {t: (rounds["redo"]["files"][t]["sha256"] == rounds["author"]["files"][t]["sha256"])
                        for t in rounds["redo"]["files"] if t in rounds["author"]["files"]}
    # the files each round used (rejected / missing ones are not counted as votes or pieces)
    s.answer_problems = []
    for name in ("author", "redo", "extract", "redo2_author", "redo2_extract") + (
            ("redo3", "redo3_reads") if s.redo3 else ()):
        r = rounds[name]
        s.answer_problems += [f"{name}: {t} rejected: {'; '.join(r['files'][t]['file_problems'])}" for t in r["rejected"]]
        s.answer_problems += [f"{name}: item rejected {m}" for t, rr in r["files"].items() for m in rr["item_problems"]]
        s.answer_problems += [f"{name}: stray file {n}" for n in r["stray"]]
    s.answer_problems += [f"redo2_extract: {t} has no valid answer (not in haiku/redo2/extract/answers"
                          f"{', not in haiku/redo3/answers' if s.redo3 else ''}) yet"
                          for t in sorted(r2x_defs) if t not in s.r2_read_source]
    s.answer_problems += [f"redo2_extract: {n}" for n in s.r2_read_notes]
    if s.redo3:
        s.answer_problems += [f"redo3_reads: {t} has no answer yet" for t in rounds["redo3_reads"]["missing"]]
    # a redo task that has no valid answer, or whose original author task has none, is a missing authoring answer
    s.missing_author = sorted(t for t in author_defs if t not in raw_author)
    # the redo3 top-up authoring tasks: one without a valid answer is a missing authoring answer too
    s.missing_redo3_author = sorted(t for t, cd in r3_defs.items() if cd.kind == "author_wording"
                                    and t not in raw_r3_author)

    # ---- 2. the v1 pipeline over validated answers only
    batches, tasks = AI.rebuild_and_check()
    pieces, coverage = load_pieces(batches, tasks, raw_author)
    AI.lint_all(pieces)
    AI.dedup_pass(pieces)
    AI.designate_held_out_packs(pieces)
    reg, added, refused = AI.build_registry(pieces)
    if refused:
        raise SystemExit(f"registry refused {len(refused)} v1 form(s): refusing to freeze")
    lint_log = json.loads((AI.ORCH / "lint_log.json").read_text(encoding="utf-8"))
    s.checks["lint_log_coverage_matches"] = all(
        lint_log["coverage"][p]["answered"] == coverage[p]["answered"]
        and lint_log["coverage"][p]["missing_tasks"] == coverage[p]["missing_tasks"] for p in AI.POOLS)
    disk_reg = json.loads((AI.ORCH / "registry.json").read_text(encoding="utf-8"))
    s.checks["registry_matches_disk"] = (
        {k: v["unit_ok"] for k, v in disk_reg["lex_status"].items()} == {f: x.unit_ok for f, x in reg.forms.items()})
    surv = [p for p in pieces if not p["problems"]]
    fids_by_kind = {"question": [], "precedence": []}
    for fid, f in reg.forms.items():
        if f.unit_ok:
            fids_by_kind["question" if f.kind == "question" else "precedence"].append(fid)
    s.checks["forms_needing_admission_match_disk"] = disk_reg["forms_needing_admission"] == fids_by_kind
    lex = AI.lex_batches(reg, fids_by_kind)
    freeform_ok = [p for p in surv if p["pool"] in RF.DOC_POOLS]
    g3, g3_expected = AI.g3h_batch(freeform_ok)
    verify = [RF._verify_files(b, name) for name, b in lex] + [RF._verify_files(g3, "g3h-freeform")]
    s.checks["extraction_files_match_disk"] = all(not v["diffs"] for v in verify)
    ext_tasks = json.loads((EXTRACT / "TASKS.json").read_text(encoding="utf-8"))
    s.checks["extraction_tasks_match_disk"] = RF._task_rows(lex, g3) == ext_tasks["tasks"]
    s.checks["g3h_expected_matches_disk"] = (
        json.loads((AI.ORCH / "g3h_expected.json").read_text(encoding="utf-8")) == g3_expected)
    bad = [k for k, v in s.checks.items() if not v]
    if bad:
        raise SystemExit(f"on-disk state differs from the rebuild {bad} (a rejected answer file changes the batches?): "
                         "refusing to record or freeze")
    s.v1_extractors = [name for name, _ in lex]
    s.v1_reads = record_reads(reg, lex, raw_extract)
    g3_rep, g3_detail, g3_probs = g3h_check(g3, g3_expected, raw_extract)
    s.g3_rep, s.g3_detail, s.g3_probs = g3_rep, g3_detail, g3_probs
    v1_form_texts = {AI._norm(f.text) for f in reg.forms.values()}      # includes rejected v1 texts: never re-read

    # ---- 3. the redo2 wordings
    R = load_build_redo2()
    r2_files, r2_rows = R.build()
    r2_diffs = diff_files(r2_files, REDO2)
    s.checks["redo2_author_files_match_disk"] = not r2_diffs
    r2_batches = r2_author_batches(R)
    p2, cov2 = r2_pieces(r2_batches, raw_r2_author)
    r2_lint_dedup(p2, v1_form_texts)
    s.r2_need = r2_register(reg, p2)
    r2_read = r2_read_batches(reg, s.r2_need)
    s.r2_read_batches = r2_read
    s.r2_read_files = r2_read_files(r2_read)
    issued = (R2X / "TASKS.json").exists()
    s.r2_reads_issued = issued
    if issued:
        d = diff_files(s.r2_read_files, R2X)
        s.checks["redo2_read_files_match_disk"] = not d
        s.r2_read_diffs = d
        if d:
            raise SystemExit(f"redo2 read tasks on disk differ from the rebuild: {d[:3]}")
        s.r2_reads = record_reads(reg, r2_read, raw_r2_extract)
    else:
        s.checks["redo2_read_files_match_disk"] = None          # not issued yet (run `reads`)
        s.r2_read_diffs = []
        s.r2_reads = []
    s.r2_coverage = cov2

    # ---- 3b. the redo3 wordings (top-up authoring) and their own two G-LEX reads
    s.p3, s.r3_need, s.r3_read_batches, s.r3_read_files, s.r3_reads, s.r3_coverage = [], [], [], {}, [], {}
    s.r3_reads_issued, s.r3_read_diffs = False, []
    if s.redo3:
        B3 = load_build_redo3()
        r3_files, _, r3_author_batches = B3.build()
        r3_diffs = diff_files(r3_files, REDO3)
        s.checks["redo3_task_files_match_disk"] = not r3_diffs
        if r3_diffs:
            raise SystemExit(f"redo3 task files on disk differ from the rebuild: {r3_diffs[:3]}")
        p3, cov3 = r2_pieces(r3_author_batches, raw_r3_author)
        # every form of every earlier round counts as taken, whatever its status (a rejected text is never re-read)
        r2_lint_dedup(p3, {AI._norm(f.text) for f in reg.forms.values()})
        s.p3, s.r3_coverage = p3, cov3
        s.r3_need = r2_register(reg, p3)
        s.r3_read_batches = r2_read_batches(reg, s.r3_need, root=R3X, reads=R3_READS)
        s.r3_read_files = r3_read_files(s.r3_read_batches, B3)
        s.checks["redo3_read_prompt_unchanged"] = all(b.prompt_sha == LEX_PROMPT_SHA for _, b in s.r3_read_batches)
        s.r3_reads_issued = (R3X / "TASKS.json").exists()
        if s.r3_reads_issued:
            s.r3_read_diffs = diff_files(s.r3_read_files, R3X)
            s.checks["redo3_read_files_match_disk"] = not s.r3_read_diffs
            if s.r3_read_diffs:
                raise SystemExit(f"redo3 read tasks on disk differ from the rebuild: {s.r3_read_diffs[:3]}")
            s.r3_reads = record_reads(reg, s.r3_read_batches, raw_r3_extract)
        else:
            s.checks["redo3_read_files_match_disk"] = None      # not issued yet (build_reads.py)
    s.coverage = coverage
    s.author_batches = batches
    s.pieces = pieces + p2 + s.p3
    s.reg = reg
    s.p2 = p2
    s.status = {fid: reg.status(fid) for fid in sorted(reg.forms)}
    return assemble(s)


def _form_id(p: dict) -> str:
    text = AI._value(p).strip()
    qf = p["meta"].get("qform")
    sem = question_sem(FAMILY, qf) if p["pool"] in ("wording", "wording_heldout") else P.PREC_SEM
    return f"{sem}#{hashlib.sha256(text.encode()).hexdigest()[:8]}"


def assemble(s: SimpleNamespace) -> SimpleNamespace:
    """Kept pieces, quarantine, pending reads, counts, targets, gates and the pool documents."""
    reg, status = s.reg, s.status
    admitted_ids = {fid for fid, st in status.items() if st == "admitted"}
    s.gate_all = reg.gate(used_form_ids=list(status))
    s.gate_used = reg.gate(used_form_ids=sorted(admitted_ids))
    drop_rows = set(s.g3_rep["drop_rows"])
    surv_pool = lambda p: not p["problems"]
    quarantine = [RF._entry(p, "lint/dedup", p["problems"]) for p in s.pieces if p["problems"]]
    pending = []
    kept = defaultdict(list)
    for p in s.pieces:
        if not surv_pool(p):
            continue
        pool, iid = p["pool"], p["internal_id"]
        if pool == "pack":
            cp, label = AI._value(p)
            kept["pack"].append({"internal_id": iid, "task_id": p["task_id"], "prompt_sha": p["prompt_sha"],
                                 "held_out": bool(p.get("held_out")), "counterparty": cp, "domain_label": label})
        elif pool in RF.SKIN_POOLS:
            kept[pool].append({"internal_id": iid, "task_id": p["task_id"], "prompt_sha": p["prompt_sha"],
                               "held_out": pool == "skin_heldout", "register": p["meta"]["register"],
                               "tone": p["meta"]["tone"], "text": AI._value(p)})
        elif pool == "attack":
            kept["attack"].append({"internal_id": iid, "task_id": p["task_id"], "prompt_sha": p["prompt_sha"],
                                   "slot": p["item"]["slots"][0].strip("{}"), "text": AI._value(p)})
        elif pool in ("wording", "wording_heldout", "precedence"):
            fid = p.get("form_id") or _form_id(p)
            if fid not in reg.forms:
                quarantine.append(RF._entry(p, "G-LEX", ["no registry form for this piece"]))
            elif status.get(fid) == "pending":
                f = reg.forms[fid]
                pending.append({"internal_id": iid, "task_id": p["task_id"], "form_id": fid,
                                "qform": p["meta"].get("qform"), "held_out": bool(p.get("held_out")),
                                "reads_recorded": len({e for e, _ in f.extractions}), "reads_required": f.required,
                                "text": AI._value(p).strip()})
            elif status.get(fid) != "admitted":
                quarantine.append(RF._entry(p, "G-LEX", [
                    f"form {fid} is {status.get(fid, reg.status(fid))}",
                    f"expected sem {reg.forms[fid].sem_id}",
                    f"reads (extractor, sem or None): {[list(e) for e in reg.forms[fid].extractions]}"]))
            else:
                row = {"form_id": fid, "task_id": p["task_id"], "prompt_sha": p["prompt_sha"],
                       "text": AI._value(p).strip(), "sem_id": reg.forms[fid].sem_id,
                       "extractions": [list(e) for e in reg.forms[fid].extractions]}
                if pool in ("wording", "wording_heldout"):
                    row["qform"] = p["meta"]["qform"]
                    row["held_out"] = pool == "wording_heldout"
                kept["precedence" if pool == "precedence" else "wording"].append(row)
        elif pool in RF.DOC_POOLS:
            d = s.g3_detail[iid]
            if iid in drop_rows or not d["ok"]:
                why = d["diffs"] or ["G3-H failed"]
                if d["template"] in s.g3_rep["quarantined"]:
                    why = why + [f"template {d['template']} quarantined (G3-H under {g3h.PASS_RATE:.0%})"]
                quarantine.append(RF._entry(p, "G3-H", why))
            else:
                m = AI._meta(iid)
                kept["freeform"].append({"internal_id": iid, "task_id": p["task_id"], "prompt_sha": p["prompt_sha"],
                                         "held_out": pool == "freeform_heldout", "register": m["register"],
                                         "tone": m["tone"], "text": AI._value(p), "facts": p["item"]["facts"]})
        else:
            raise SystemExit(f"unknown pool {pool}")
    s.kept, s.quarantine, s.pending = kept, quarantine, pending

    skins_train, skins_ho = kept["skin"], kept["skin_heldout"]
    train_regs = sorted({x["register"] for x in skins_train})
    ho_regs = sorted({x["register"] for x in skins_ho})
    train_by_form = Counter(w["qform"] for w in kept["wording"] if not w["held_out"])
    ho_by_form = Counter(w["qform"] for w in kept["wording"] if w["held_out"])
    cand_train = Counter(x["qform"] for x in pending if not x["held_out"])
    cand_ho = Counter(x["qform"] for x in pending if x["held_out"])
    mode_t = len(skins_train) + len(skins_ho) + len(kept["attack"])
    mode_f = len(kept["freeform"])
    s.targets, s.shortfalls = evaluate_targets(
        packs_train=sum(1 for x in kept["pack"] if not x["held_out"]),
        packs_ho=sum(1 for x in kept["pack"] if x["held_out"]), train_regs=train_regs, ho_regs=ho_regs,
        prec_n=len(kept["precedence"]), train_by_form=train_by_form, ho_by_form=ho_by_form, mode_t=mode_t,
        mode_f=mode_f, cand_train=cand_train, cand_ho=cand_ho)
    s.g3h_pass = s.g3_rep["all_templates_pass"] and not s.g3_probs
    # READY: every G0 minimum met (the counts already show any rejected answer as a missing piece), the G-LEX gate passes
    # over every form the pools use, G3-H passes and no authoring task is left without a valid answer. Rejected answers
    # are reported in the manifest; a form still waiting for reads is simply not used (not a blocker).
    s.ready = bool(not s.shortfalls and s.gate_used["pass"] and s.g3h_pass and not s.missing_author
                   and not s.missing_redo3_author and all(v in (True, None) for v in s.checks.values()))

    lex_counts = Counter(status.values())
    s.counts = {
        "packs": {"training": s.targets["base"]["packs_training"]["got"], "held_out": s.targets["base"]["packs_heldout"]["got"]},
        "skins": {"training_by_register": dict(Counter(x["register"] for x in skins_train)),
                  "training_by_register_tone": {f"{r}|{t}": n for (r, t), n in sorted(Counter(
                      (x["register"], x["tone"]) for x in skins_train).items())},
                  "held_out_by_register": dict(Counter(x["register"] for x in skins_ho))},
        "attack": {"kept": len(kept["attack"]), "by_slot": dict(Counter(a["slot"] for a in kept["attack"]))},
        "wordings": {"admitted_training_by_qform": dict(sorted(train_by_form.items())),
                     "admitted_heldout_by_qform": dict(sorted(ho_by_form.items())),
                     "training_total": sum(train_by_form.values()), "held_out_total": sum(ho_by_form.values()),
                     "pending_reads_training_by_qform": dict(sorted(cand_train.items())),
                     "pending_reads_heldout_by_qform": dict(sorted(cand_ho.items()))},
        "precedence": {"admitted": len(kept["precedence"])},
        "lexicon": {"forms": len(reg.forms), "status": dict(sorted(lex_counts.items()))},
        "documents": {"kept_by_register": dict(Counter(d["register"] for d in kept["freeform"])),
                      "held_out": sum(1 for d in kept["freeform"] if d["held_out"]),
                      "training": sum(1 for d in kept["freeform"] if not d["held_out"])},
        "mode_pieces": {"T": mode_t, "F": mode_f, "F_share": round(mode_f / (mode_t + mode_f), 4)},
        "quarantine": {"total": len(quarantine), "by_stage": dict(Counter(q["stage"] for q in quarantine)),
                       "pending_reads": len(pending)},
        "authoring_coverage": {p: {"items": s.coverage[p]["items"], "answered": s.coverage[p]["answered"],
                                   "missing_tasks": s.coverage[p]["missing_tasks"]} for p in AI.POOLS},
        "redo2_authoring": {p: {"items": c["items"], "answered": c["answered"], "missing_tasks": c["missing_tasks"]}
                            for p, c in s.r2_coverage.items()},
        "redo2_pieces": {"answered": len(s.p2), "lint_or_dedup_dropped": sum(1 for p in s.p2 if p["problems"]),
                         "registered_for_reads": len(s.r2_need)},
        "redo3_authoring": {p: {"items": c["items"], "answered": c["answered"], "missing_tasks": c["missing_tasks"]}
                            for p, c in s.r3_coverage.items()},
        "redo3_pieces": {"answered": len(s.p3), "lint_or_dedup_dropped": sum(1 for p in s.p3 if p["problems"]),
                         "registered_for_reads": len(s.r3_need)},
    }
    s.docs = pool_documents(s, admitted_ids, skins_train, skins_ho)
    return s


def pool_documents(s: SimpleNamespace, admitted_ids: set, skins_train: list, skins_ho: list) -> dict:
    kept, reg, status = s.kept, s.reg, s.status
    doc = {
        "packs.json": {"family": FAMILY, "pool": "pack", "count": len(kept["pack"]), "items": kept["pack"]},
        "skins.json": {"family": FAMILY, "pool": "skin", "count": len(skins_train) + len(skins_ho),
                       "items": skins_train + skins_ho},
        "attack.json": {"family": FAMILY, "pool": "attack", "count": len(kept["attack"]), "items": kept["attack"]},
        "wordings.json": {"family": FAMILY, "pool": "wording", "count": len(kept["wording"]),
                          "held_out_count": sum(1 for w in kept["wording"] if w["held_out"]),
                          "items": kept["wording"]},
        "precedence.json": {"family": FAMILY, "pool": "precedence", "count": len(kept["precedence"]),
                            "items": kept["precedence"]},
    }
    lex_json = reg.to_json()
    lex_json["forms"] = [f for f in lex_json["forms"] if f["form_id"] in admitted_ids]
    lex_json["not_admitted"] = {fid: st for fid, st in sorted(status.items()) if st != "admitted"}
    lex_json["admitted_form_ids"] = sorted(admitted_ids)
    doc["lexicon.json"] = {"family": FAMILY, "pool": "lexicon", "count": len(admitted_ids), "registry": lex_json}
    doc["documents.json"] = {"family": FAMILY, "pool": "freeform", "count": len(kept["freeform"]),
                             "items": kept["freeform"]}
    doc["quarantine.json"] = {"family": FAMILY, "count": len(s.quarantine), "items": s.quarantine,
                              "pending_reads": s.pending,
                              "g3h": {"gate": "G3-H", "bar": g3h.PASS_RATE, "templates": s.g3_rep["templates"],
                                      "quarantined": s.g3_rep["quarantined"]},
                              "reads": s.v1_reads + s.r2_reads + s.r3_reads}
    return doc


# ======================================================================================================= 6. v1 comparison

def v1_comparison(s: SimpleNamespace, texts: dict) -> dict:
    """Is v1 reproduced? The files that redo2 cannot change must be byte for byte the v1 files; wordings, lexicon and
    quarantine must contain every v1 record unchanged (v2 only adds)."""
    out = {}
    v1_manifest = json.loads((V1_POOLS / "manifest.json").read_text(encoding="utf-8"))
    for rel in ("packs.json", "skins.json", "attack.json", "precedence.json", "documents.json"):
        v1 = (V1_POOLS / rel).read_bytes()
        out[rel] = {"identical_to_v1": v1 == texts[rel].encode("utf-8"),
                    "v1_sha256_in_v1_manifest": v1_manifest["pool_files"][rel]["sha256"],
                    "v1_file_matches_its_manifest": hashlib.sha256(v1).hexdigest() == v1_manifest["pool_files"][rel]["sha256"]}
    v1w = json.loads((V1_POOLS / "wordings.json").read_text(encoding="utf-8"))["items"]
    v2w = {w["form_id"]: w for w in s.docs["wordings.json"]["items"]}
    out["wordings.json"] = {"every_v1_wording_kept_unchanged": all(
        w["form_id"] in v2w and {k: v for k, v in v2w[w["form_id"]].items() if k != "held_out"} == w for w in v1w)}
    v1l = json.loads((V1_POOLS / "lexicon.json").read_text(encoding="utf-8"))["registry"]["forms"]
    v2l = {f["form_id"]: f for f in s.docs["lexicon.json"]["registry"]["forms"]}
    out["lexicon.json"] = {"every_v1_form_kept_unchanged": all(f["form_id"] in v2l and v2l[f["form_id"]] == f for f in v1l)}
    v1q = json.loads((V1_POOLS / "quarantine.json").read_text(encoding="utf-8"))["items"]
    v2q = s.docs["quarantine.json"]["items"]
    out["quarantine.json"] = {"every_v1_entry_kept_unchanged": all(e in v2q for e in v1q)}
    out["v1_manifest_sha256"] = hashlib.sha256((V1_POOLS / "manifest.json").read_bytes()).hexdigest()
    return out


# ======================================================================================================= 7. summary, write

def _sha_text(t: str) -> str:
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


LOADER_NOTE = (
    "plugin.py reads no pool path: T26Plugin takes its skins, wordings, attack lines and lexicon from the KitCtx / "
    "registry the caller builds, so there is nothing to refresh there. The G13-seed loader (g13_c2.pool_units) reads "
    "families/T26/pools/ only. To use these pools: when READY (and after G13-seed), move pools/ to pools_v1/ and "
    "pools_v2/ to pools/ (the file names are the same; the manifest is MANIFEST.json here, manifest.json in v1). "
    "Until then the generator must load pools_v2/ explicitly: skins.json items with held_out=false are the training "
    "skins (held_out=true: sampler S5 only); attack.json, precedence.json and documents.json are as in v1; wordings.json "
    "items carry held_out (true: sampler S5 only, KitCtx wording skins with held_out=true; false: samplers S1-S4); "
    "lexicon.json holds the admitted forms (registry.forms[*].held_out) and the declared sems and decoys; "
    "quarantine.json lists the dropped pieces and `pending_reads` (forms still awaiting their G-LEX reads: never use "
    "them).")


NEXT_STEPS = [
    "dispatch every task in haiku/redo2/extract/TASKS.json (one fresh Haiku agent per task_file: it reads only that file "
    "and writes only its answer_file; the two reads of a form are in different batches, so no agent reads a form twice)",
    "audit each agent's file access (c2_kit.audit); a failed audit discards that agent's answers (re-run with a fresh agent)",
    "run `freeze_v2.py freeze` again: it validates the new answers, records the votes (2/2), admits or rejects each form "
    "and rewrites pools_v2/ (v1 stays untouched)",
    "READY needs yn_fails >= 6 admitted training wordings and >= 3 admitted held-out wordings for each of the 8 forms",
]


def next_steps(s: SimpleNamespace) -> list:
    """What is left, from the state: pending reads to dispatch, a shortfall that needs new authoring, or promotion."""
    if s.pending:
        return NEXT_STEPS
    if s.ready:
        return ["no read is pending and every G0 minimum is met: run the G13-seed check on the pools after promotion "
                "(C2_DATA_SPEC 6.4 step 4), then promote pools_v2/ to pools/ as `promote` says"]
    return ["no read is pending: every remaining shortfall needs new authoring answers (a new Haiku authoring task for "
            "the named forms), then their two G-LEX reads, then `freeze_v2.py freeze` again"]


def summarize(s: SimpleNamespace, write: bool) -> dict:
    texts = {rel: json.dumps(obj, ensure_ascii=False, indent=1) + "\n" for rel, obj in s.docs.items()}
    files = {rel: {"sha256": _sha_text(t), "bytes": len(t.encode("utf-8")), "count": s.docs[rel]["count"]}
             for rel, t in texts.items()}
    s.texts, s.file_rows = texts, files
    s.cmp = v1_comparison(s, texts)
    r2_issued = {"issued": s.r2_reads_issued, "n_tasks": len(r2_task_rows(s.r2_read_batches)),
                 "tasks": [{"task_file": r["task_file"], "answer_file": r["answer_file"], "n_items": r["n_items"],
                            "pool": r["pool"], "answered_by": s.r2_read_source.get(Path(r["task_file"]).stem)}
                           for r in r2_task_rows(s.r2_read_batches)]}
    r3_rows = [{"task_file": str(R3X / f"{c['task_id']}.txt"), "answer_file": c["answer_file"], "n_items": len(c["items"]),
                "pool": c["pool"]} for _, b in s.r3_read_batches for c in b.chunks]
    r3_issued = {"issued": s.r3_reads_issued, "n_tasks": len(r3_rows), "tasks": r3_rows}
    pending_reads = sum(max(0, x["reads_required"] - x["reads_recorded"]) for x in s.pending)
    validation = {name: {"tasks": r["tasks"], "files": len(r["files"]), "accepted_files": sum(1 for x in r["files"].values() if x["ok"]),
                         "rejected": r["rejected"], "item_rejects": r["item_rejects"], "missing": r["missing"],
                         "stray": r["stray"]} for name, r in s.rounds.items()}
    # haiku/redo2/extract/answers is the original location of the redo2 reads; the redo3 re-issue (same task ids) fills it
    validation["redo2_extract"]["answers_counted_from"] = dict(sorted(Counter(s.r2_read_source.values()).items()))
    status = ("READY: every G0 minimum is met, the G-LEX gate passes over every form the pools use and G3-H passes"
              if s.ready else
              "SHORT: " + "; ".join(f"{x['target']} {x['got']}/{x['bar']}" for x in s.shortfalls
                                    if x["short_by"] is not None) + (f"; {len(s.pending)} redo2/redo3 wording(s) still await "
                                                                     f"{pending_reads} G-LEX read(s)" if s.pending else ""))
    return {"write": write, "family": FAMILY, "version": VERSION, "ready": s.ready, "status": status,
            "a38_frozen": s.a38, "checks": s.checks, "counts": s.counts, "targets": s.targets,
            "shortfalls": s.shortfalls,
            "gates": {"G-LEX_used_forms": {k: v for k, v in s.gate_used.items() if k != "not_admitted"},
                      "G-LEX_all_forms": {k: v for k, v in s.gate_all.items() if k != "not_admitted"},
                      "G-LEX_all_forms_not_admitted_count": len(s.gate_all["not_admitted"]),
                      "G3-H": {"pass": s.g3h_pass, "quarantined_templates": s.g3_rep["quarantined"],
                               "templates": len(s.g3_rep["templates"])},
                      "G-SL": "lint at ingest (AI.lint_all, lint_wording): dropped pieces are in quarantine.json",
                      "G13_seed": "not run here (C2_DATA_SPEC 6.4 step 4: run on pools/ after promotion)"},
            "validation": validation, "answer_problems": s.answer_problems, "author_notes": s.author_notes,
            "missing_author_answers": s.missing_author, "missing_redo3_author_answers": s.missing_redo3_author,
            "redo_fold_identical": s.fold_identical,
            "redo2_reads": r2_issued, "redo3_reads": r3_issued, "v1_comparison": s.cmp, "files": files,
            "pending_forms": [{k: v for k, v in x.items() if k != "text"} for x in s.pending]}


def refuse_v1_path(p: Path) -> None:
    if V1_POOLS.resolve() in Path(p).resolve().parents or Path(p).resolve() == V1_POOLS.resolve():
        raise PermissionError(f"freeze_v2 never writes into the v1 pools folder: {p}")


def write_reads(s: SimpleNamespace) -> list:
    """Write the redo2 G-LEX read tasks under haiku/redo2/extract/ (new files; refuses to change a differing file)."""
    paths.require_a38()
    if not s.r2_read_batches:
        raise SystemExit("no redo2 forms to read")
    existing = [d for d in diff_files(s.r2_read_files, R2X) if d.startswith("differs")]
    if existing:
        raise SystemExit(f"redo2 read task files on disk differ from the rebuild {existing[:3]}: refusing to overwrite")
    written = paths.write_files(R2X, s.r2_read_files)
    paths.check_path(R2X / "answers").mkdir(exist_ok=True)
    return [str(w) for w in written]


def write_freeze(s: SimpleNamespace, summary: dict) -> dict:
    paths.require_a38()
    refuse_v1_path(POOLS_V2)
    v1_manifest = V1_POOLS / "manifest.json"
    validation_report = {"family": FAMILY, "version": VERSION,
                         "note": ("every answer file of every round against its task contract; nothing was edited. "
                                  "A rejected file or item is treated as unanswered. The file-access audit (c2_kit.audit) "
                                  "needs the agents' transcripts, which this script does not open."),
                         "rounds": {n: slim(r) for n, r in s.rounds.items()}}
    vtext = json.dumps(validation_report, ensure_ascii=False, indent=1) + "\n"
    manifest = {
        "family": FAMILY, "version": VERSION,
        "stage": "admit+freeze v2 (redo, redo2 and redo3 rounds; freeze_v2.py)",
        "status": summary["status"], "ready": s.ready,
        "supersedes": {"path": "families/T26/pools/manifest.json", "sha256": s.cmp["v1_manifest_sha256"],
                       "note": "v1 is untouched"},
        "promote": LOADER_NOTE,
        "g0": {"path": "families/T26/G0_SPEC.v1_1.md", "sha256": _sha_text(G0.read_text(encoding="utf-8")),
               "pinned_in_plugin": P.T26Plugin.G0_SHA256_AUTHORED},
        "pool_files": s.file_rows,
        "validation_report": {"file": "validation_report.json", "sha256": _sha_text(vtext)},
        "validation": summary["validation"],
        "v1_comparison": s.cmp, "counts": s.counts, "targets": s.targets, "shortfalls": s.shortfalls,
        "gates": summary["gates"], "checks": s.checks,
        "reads": {"v1": s.v1_reads, "redo2": s.r2_reads, "redo2_dispatch": summary["redo2_reads"],
                  "redo2_answer_source": dict(sorted(s.r2_read_source.items())), "redo2_answer_notes": s.r2_read_notes,
                  "redo3": s.r3_reads, "redo3_dispatch": summary["redo3_reads"]},
        "pending_forms": summary["pending_forms"],
        "next_steps": next_steps(s),
        "sources": {
            "author_answers_used": {t: {"source": s.author_source[t],
                                        "sha256": s.rounds["redo" if s.author_source[t] == "redo" else "author"]["files"][t]["sha256"]}
                                    for t in sorted(s.author_source)},
            "extract_answers": {t: r["sha256"] for t, r in sorted(s.rounds["extract"]["files"].items())},
            "redo_answers": {t: r["sha256"] for t, r in sorted(s.rounds["redo"]["files"].items())},
            "redo2_author_answers": {t: r["sha256"] for t, r in sorted(s.rounds["redo2_author"]["files"].items())},
            "redo2_extract_answers": {t: r["sha256"] for t, r in sorted(s.rounds["redo2_extract"]["files"].items())},
            # redo3/answers holds the re-issued redo2 reads (same task ids; they count as the redo2 reads when
            # haiku/redo2/extract/answers lacks the file) and the top-up authoring answers; redo3/reads/answers holds
            # the two reads of the new redo3 wordings
            "redo3_answers": {t: {"kind": r["kind"], "sha256": r["sha256"], "file": r["file"],
                                  "counted_as": ("redo2 G-LEX read" if r["kind"] == "extract_lex" and
                                                 s.r2_read_source.get(t) == "redo3" else
                                                 "redo3 authoring" if r["kind"] == "author_wording" else "not counted")}
                              for t, r in sorted(s.rounds.get("redo3", {"files": {}})["files"].items())},
            "redo3_read_answers": {t: {"sha256": r["sha256"], "file": r["file"]}
                                   for t, r in sorted(s.rounds.get("redo3_reads", {"files": {}})["files"].items())}},
        "not_verified": ["file-access audit (c2_kit.audit) of the extraction, redo, redo2 and redo3 agents: needs their "
                         "transcripts, not opened here (the orchestrator reports no failed audit; audit-failed: [])"],
    }
    mtext = json.dumps(manifest, ensure_ascii=False, indent=1) + "\n"
    out = dict(s.texts)
    out["validation_report.json"] = vtext
    out["MANIFEST.json"] = mtext
    for rel in out:
        refuse_v1_path(POOLS_V2 / rel)
    paths.write_files(POOLS_V2, out)
    summary["manifest"] = str(POOLS_V2 / "MANIFEST.json")
    return summary


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    cmd = argv[0] if argv else "check"
    if cmd not in ("check", "reads", "freeze"):
        print(__doc__)
        return 2
    s = build()
    summary = summarize(s, write=cmd != "check")
    if cmd == "reads":
        summary["reads_written"] = write_reads(s)
    elif cmd == "freeze":
        write_freeze(s, summary)
    print(json.dumps(summary, indent=1, default=str, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

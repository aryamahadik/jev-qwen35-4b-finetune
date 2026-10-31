"""families/T01/freeze_v2.py: T01 pool freeze-v2 (G0_SPEC.md v3 sections 7 and 8 (H42-H47); C2_DATA_SPEC 6.2 item 2, 6.3,
6.4 steps 3-4; PREREG A37 (b) and A38).

Why this file exists. freeze.py (v1) reads only haiku/author/answers and haiku/extract/answers. It never calls g3h.compare
(it hard-codes "documents admitted 0 of 120"), it has no path for the redo2 answers (haiku/redo2: replacement packs,
wordings and notes, and the H45 confirmation reads glex-r1b / -r2b / -r3b) or the redo3 answers (haiku/redo3: skins, window
clauses, backup notes, the g3h-r1 read of two notes, and haiku/redo3/reads: the six G-LEX reads of the new clauses), and
it would overwrite pools/. This script is that path. It changes nothing that exists: pools/ (v1), every answer file, every
plan file and all pinned and kit code stay byte for byte as they are. It writes only pools_v2/, through c2_kit.paths
(refuses before A38).

  check    in memory only: validate every answer file, rebuild v1 and prove it equals the frozen pools/, merge the redo2
           pieces, record every G-LEX and G3-H vote, apply every gate, and print the counts, the status (READY, SHORT or
           BLOCKED) and every shortfall. Nothing is written.
  freeze   the same, then write families/T01/pools_v2/ (packs, skins, documents, documents_pending_g3h, wordings, windows,
           comparators as .jsonl; lexicon_registry.json, quarantine.jsonl, VALIDATION_REPORT.json, MANIFEST.json).
           Refuses when a blocking problem exists, and refuses to replace a pools_v2/MANIFEST.json that says ready: true.
           A SHORT pools_v2 may be replaced by a later run (the new manifest records the sha256 of the one it replaces),
           but only after it was moved aside as pools_v2_prev/: haiku/redo3 was authored against that freeze and its
           builders (build_redo3.py, reads/build_reads.py) read it, so the script refuses to overwrite a pools_v2/ while
           there is a redo3 round and no pools_v2_prev/. Move it first:  mv families/T01/pools_v2 families/T01/pools_v2_prev

Run from lean/c2_build:
  ../.venv/bin/python -B -m families.T01.freeze_v2 check  [--no-rebuild-check] [--exclude-task <task id>]...
  ../.venv/bin/python -B -m families.T01.freeze_v2 freeze [--no-rebuild-check] [--exclude-task <task id>]...
--exclude-task names a task whose file-access audit failed: its answer file is rejected whole (its votes and pieces are
not used) and is never edited. By default nothing is excluded. A round-1 g3h task id is shared by haiku/extract and
haiku/redo, so excluding it excludes both copies. A v1 author or G-LEX read excluded this way makes v1 irreproducible
(BLOCKED): v1 is frozen and used as it is.

What it does, in order (no label is set anywhere; Haiku answers only flag; a read's answer is never edited):
  1. Contract check of EVERY answer file of every round (v1 author, v1 extract, redo = the g3h re-reads, redo2, redo3 and
     redo3/reads). A file is valid only when it is UTF-8 JSON, a list of objects with exactly the contract keys (qid +
     pack | text | meaning | person + ref + topic), every qid from its own chunk, none repeated, every item answered once,
     and a G-LEX meaning copied exactly from the item's choices. An invalid, missing or excluded file is rejected whole;
     none of its votes or pieces is used.
  2. v1 is rebuilt in memory (freeze.rebuild / record_reads / admission / build) and must reproduce every file of
     pools/manifest.json (sha256 of the rebuilt text equals the manifest and the file on disk) and every extract answer
     sha. The v1 pieces carry over unchanged; a redo piece fills only a slot v1 left open.
  3. The redo2 task set is rebuilt with build_redo2.build() (unless --no-rebuild-check) and must equal the files on disk
     (chunks, keys, plans, manifests, task files, TASKS.json). Then each redo2 answer is mapped through chunk, key and plan.
  4. Redo2 pieces go through the SAME checks as v1, plus the extra rules the redo2 prompts promised a program would
     enforce (INGEST in build_redo2.py):
       packs      H46: haiku_author.validate_pack + extract.lint_pack, no person or vendor repeats a kept pack (or the
                  TAKEN list), the initials range, name shape, month / weekday / number words, negation stems, cash topic
                  without "report"; each failed slot takes its own replacement, else the first passing spare (sorted id)
                  takes the slot and the slot's held-out flag; at most one pack per slot
       wordings   H42 / H44: haiku_author.check_wording with the 'seen' set seeded with every kept wording text, the
                  redo2 word bans and construction rules; variant a first, b only if a fails; at most one per slot. A kept
                  text is added to the registry with NO votes: it needs two realistic-fill G-LEX reads that do not exist
                  yet, so it stays pending and out of the pool
       notes      H47: haiku_author.check_freeform with the plan facts; variant a first. A kept note needs one g3h-r1 read
                  that does not exist yet, so it stays in documents_pending_g3h
  5. G-LEX (c2_kit.lexicon.LexiconRegistry): the v1 registry with its v1 votes (glex-r1, -r2; -r3 for windows) gets the
     H45 confirmation votes. Admission is the kit rule (status): unit test passes and the required number of distinct
     extractors all pick the declared sem (2 for comparators and question wordings, 3 for window rules); one other pick
     rejects for good. H45 adds: a form is USED only if it is admitted AND has every confirmation read (glex-r1b, -r2b;
     + glex-r3b for window forms); a missing read leaves the form unused, never admitted.
  6. G3-H: every note is compared with its brief facts (g3h.compare: person, ref, topic) from its g3h-r1 read; one entry
     per note, template report at 98%. A note with no valid read is not admitted (pending); a mismatch is dropped.
  7. The G0 targets of freeze.TARGET (imported, never changed) are applied to the merged pool.
  8. Redo3 (haiku/redo3 + haiku/redo3/reads; build_redo3.py, reads/build_reads.py), folded in after step 7's inputs are
     known and before the targets are applied:
       baseline   the freeze redo3 was authored against (pools_v2_prev/, else pools_v2/ before it is replaced) must equal
                  the in-memory v1 + redo2 result (the nine pool data files by sha256) and carry the input shas that
                  redo3/TASKS.json recorded; a difference BLOCKS (the round could not be reproduced)
       skins      haiku_author.check_skin with 'seen' seeded with every kept skin's normalised text; per register the
                  passing skins, in sorted id order, fill that register's open v1 slots in order until the register
                  reaches its G0 target (training 56, held out 28); passing skins beyond that are surplus: listed in the
                  MANIFEST, never kept; a failing skin goes to quarantine
       windows    haiku_author.check_lexicon ('seen' = every window text of the registry), extract.lint_clause flags
                  (logged, never a drop, H43), dedup; each kept clause is a NEW registry form (a new authored item, not a
                  slot refill) that is used only with glex-r1/-r2/-r3 (3/3) AND glex-r1b/-r2b/-r3b on its declared sem
                  (H45) from the redo3 reads; every such form goes into the pool (the 14 per sem is a minimum)
       notes      the two redo2 notes without a read take their g3h-r1 read from redo3 (g3h.compare; match admits, mismatch
                  drops, H47). The redo3 backup notes (haiku_author.check_freeform) are used only to replace a dropped
                  note; they then wait for their own g3h-r1 read (pending); otherwise they are listed as unused
       rebuild    build_redo3.build() and reads/build_reads.build() must reproduce every non-answer file on disk (both read
                  the baseline, so their POOLS_V2 is pointed at it); an answer file's task id on --exclude-task is ignored

READY means: no G0 shortfall, the G-LEX gate passes on every form the pool uses, G3-H leaves no note unread or
mismatched, and no blocking problem. Otherwise SHORT with the exact shortfalls. G13-seed and row generation are not run here.

How the generator loads pools_v2. Nothing in the T01 family code (plugin.py, solver_b.py, haiku_*.py, fixtures.py) reads a
pool path (the plugin holds code stand-ins and takes a KitCtx), so there is no path to refresh. freeze.POOLS still names
pools/ and only serves freeze-v1. g13_c2.py reads families/<F>/pools/ (block_dir / "pools"), so it does not see pools_v2
until the owner promotes it by directory move (the T31 precedent: pools/ -> pools_v1/, pools_v2/ -> pools/). To use
pools_v2 now:
    from families.T01 import freeze_v2
    pools = freeze_v2.load_pools()        # skins and notes as Skin objects, wordings / windows / comparators / packs as
    ctx = freeze_v2.make_ctx(pools)       # rows, a USED-forms-only LexiconRegistry, and a KitCtx shaped like fixtures.ctx()
Keep v1 untouched until the owner rules.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True       # importing build_redo2 and the kit must not leave __pycache__ files behind

import argparse
import hashlib
import importlib.util
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker as CH  # noqa: E402
from c2_kit import g3h, paths  # noqa: E402
from c2_kit import lexicon as L  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from families.T01 import extract as E  # noqa: E402
from families.T01 import freeze as F1  # noqa: E402
from families.T01 import haiku_author as A  # noqa: E402
from families.T01 import plugin as P  # noqa: E402

FAMILY = "T01"
VERSION = "freeze-v2"
POOLS_V1 = F1.POOLS
POOLS_V2 = HERE / "pools_v2"
POOLS_V2_PREV = HERE / "pools_v2_prev"   # the freeze that redo3 was authored against (v1 + redo2), moved aside by the re-freeze
HAIKU = HERE / "haiku"
REDO1 = HAIKU / "redo"
REDO2 = HAIKU / "redo2"
REDO3 = HAIKU / "redo3"
REDO3_READS = REDO3 / "reads"
KNOWN_ROUNDS = ("author", "extract", "redo", "redo2", "redo3")
G0 = HERE / "G0_SPEC.md"
TARGET = F1.TARGET                   # imported, never changed
WINDOW_SEMS = F1.WINDOW_SEMS
COMPARATOR_SEMS = F1.COMPARATOR_SEMS
TRAIN_REGISTERS = F1.TRAIN_REGISTERS
HELD_REGISTERS = F1.HELD_REGISTERS
PER_FORM_ASKED = F1.PER_FORM_ASKED
# H45: the confirmation reads every v1-admitted form needs before it is used
CONFIRM_READS = ("glex-r1b", "glex-r2b")
CONFIRM_READS_WINDOW = CONFIRM_READS + ("glex-r3b",)
INDEPENDENT_READS = ("glex-r1", "glex-r2")            # the first G-LEX reads: 2/2 admit (3/3 for window rules)
INDEPENDENT_READS_WINDOW = INDEPENDENT_READS + ("glex-r3",)
G3H_READ = "g3h-r1"
CONTRACT_KEYS = {"author_pack": ("pack",), "author_skin": ("text",), "author_wording": ("text",),
                 "author_freeform": ("text",), "author_lexicon": ("text",), "extract_lex": ("meaning",),
                 "extract_g3h": ("person", "ref", "topic")}
POOL_FILES = ("packs.jsonl", "skins.jsonl", "documents.jsonl", "documents_pending_g3h.jsonl", "wordings.jsonl",
              "windows.jsonl", "comparators.jsonl", "lexicon_registry.json", "quarantine.jsonl")
# which pool each author task kind feeds, per round (a kind not listed here is reported, never guessed)
REDO2_POOLS = {"author_pack": "packs", "author_wording": "wordings", "author_freeform": "freeform"}
REDO3_POOLS = {"author_skin": "skins", "author_lexicon": "windows", "author_freeform": "backup_notes"}
REDO3_G3H_BACKED = {"extract_g3h"}
TRAIN_SKIN_BASE, HELD_SKIN_BASE = A.N_SKIN_TRAIN, A.N_SKIN_HELD    # redo3 skin ids continue each register's v1 numbering


# ------------------------------------------------------------------------------------------------ small helpers
def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def safe_read(p) -> bytes:
    """Every file this script opens goes through the never-open guard (C2_DATA_SPEC 6.5)."""
    paths.check_path(p)
    return Path(p).read_bytes()


def sha_file(p) -> str:
    return sha_bytes(safe_read(p))


def read_json(p):
    return json.loads(safe_read(p).decode("utf-8"))


def rel(p) -> str:
    p = Path(p).resolve()
    try:
        return p.relative_to(C2_BUILD).as_posix()
    except ValueError:
        return str(p)


def dump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=1) + "\n"


def jsonl(rows) -> str:
    return "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)


def _no_dup_pairs(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise ValueError(f"duplicate JSON key {k!r}")
        out[k] = v
    return out


# ------------------------------------------------------------------------------------------------ answer contract
def _value_problems(kind: str, qid: str, a: dict, item: dict) -> list:
    if kind in ("author_skin", "author_wording", "author_freeform", "author_lexicon"):
        return [] if isinstance(a["text"], str) else [f"{qid}: text is not a string"]
    if kind == "author_pack":
        return [] if isinstance(a["pack"], dict) else [f"{qid}: pack is not an object"]
    if kind == "extract_lex":
        m = a["meaning"]
        if not isinstance(m, str):
            return [f"{qid}: meaning is not a string"]
        if m not in item.get("choices", ()):
            return [f"{qid}: meaning is not one of the item's choices (copied exactly)"]
        return []
    if kind == "extract_g3h":
        return [f"{qid}: {k} is not a string" for k in ("person", "ref", "topic") if not isinstance(a[k], str)]
    return [f"{qid}: unknown task kind {kind}"]


def validate_answer(kind: str, data: bytes, items: dict) -> tuple:
    """(answers {qid: object without qid} or None, problems). items: {qid: item} the file must answer, once each. The whole
    file is rejected on any problem: nothing is repaired or partly used."""
    if kind not in CONTRACT_KEYS:
        return None, [f"unknown task kind {kind!r}"]
    try:
        obj = json.loads(data.decode("utf-8"), object_pairs_hook=_no_dup_pairs)
    except (UnicodeDecodeError, ValueError) as e:
        return None, [f"not valid UTF-8 JSON ({str(e)[:90]})"]
    if not isinstance(obj, list):
        return None, ["the top level is not a JSON list"]
    want = {"qid", *CONTRACT_KEYS[kind]}
    out, probs = {}, []
    for i, a in enumerate(obj):
        if not isinstance(a, dict):
            probs.append(f"entry {i} is not an object")
            continue
        if set(a) != want:
            probs.append(f"entry {i}: keys {sorted(a)} != {sorted(want)}")
            continue
        qid = a["qid"]
        if not isinstance(qid, str) or qid not in items:
            probs.append(f"entry {i}: qid {qid!r} is not in this task's chunk")
            continue
        if qid in out:
            probs.append(f"qid {qid} answered twice")
            continue
        probs += _value_problems(kind, qid, a, items[qid])
        out[qid] = {k: v for k, v in a.items() if k != "qid"}
    missing = len(set(items) - set(out))
    if missing:
        probs.append(f"{missing} item(s) unanswered")
    return (None if probs else out), probs


def read_answer_file(rnd: str, kind: str, task_id: str, path, items: dict, excluded) -> tuple:
    """(answers or None, record). The record is what VALIDATION_REPORT.json lists for the file. Never edits the file."""
    path = Path(path)
    rec = {"round": rnd, "task_id": task_id, "kind": kind, "file": rel(path), "sha256": None,
           "n_expected": len(items), "n_answered": 0, "status": "valid", "problems": []}
    if task_id in excluded:
        rec.update(status="excluded", problems=["file-access audit failed: answers ignored"])
        if path.is_file():
            rec["sha256"] = sha_file(path)
        return None, rec
    if not path.is_file():
        rec.update(status="missing", problems=["answer file missing (task not answered)"])
        return None, rec
    data = safe_read(path)
    rec["sha256"] = sha_bytes(data)
    ans, probs = validate_answer(kind, data, items)
    if ans is None:
        rec.update(status="invalid", problems=probs)
        return None, rec
    rec["n_answered"] = len(ans)
    return ans, rec


# ------------------------------------------------------------------------------------------------ data classes
@dataclass
class AuthorItem:
    pool: str            # packs | wordings | freeform
    iid: str
    payload: object      # text, or a pack object
    round: str
    task: str            # provenance task id recorded on the piece
    psha: str            # provenance prompt sha recorded on the piece (the batch prompt sha)
    file: str
    file_sha: str
    task_file_sha: str
    meta: dict


@dataclass
class ReadBatch:
    round: str
    name: str            # the extractor id (G-LEX) / read name (G3-H)
    kind: str            # extract_lex | extract_g3h
    batch_id: str
    key: dict            # qid -> form id (G-LEX) | note pid (G3-H)
    prompt_sha: str
    tasks: list          # [(task_id, answer path, {qid: item})]
    plan: dict = field(default_factory=dict)         # form id -> plan entry (redo2 reads): filled text, sem, kind
    answers: dict = field(default_factory=dict)      # qid -> answer object, valid files only
    used_tasks: dict = field(default_factory=dict)   # task id -> answer sha256 of the valid files


# ------------------------------------------------------------------------------------------------ v1 stage (cached)
_V1: dict = {}


def v1_file_texts(rb: dict, out: dict) -> dict:
    """The text of every v1 pool file as freeze.write_all writes it (paths.write_jsonl / write_json)."""
    p = out["pools"]
    return {"packs.jsonl": jsonl(p["packs"]), "skins.jsonl": jsonl(p["skins"]),
            "documents_pending_g3h.jsonl": jsonl(p["documents_pending_g3h"]), "wordings.jsonl": jsonl(p["wordings"]),
            "windows.jsonl": jsonl(p["windows"]), "comparators.jsonl": jsonl(p["comparators"]),
            "lexicon_registry.json": dump(rb["reg"].to_json()), "quarantine.jsonl": jsonl(out["quar"])}


def v1_integrity(v1: dict) -> dict:
    """The rebuilt v1 files must equal pools/manifest.json and the files on disk; the v1 inputs must be the ones it hashed."""
    man = read_json(POOLS_V1 / "manifest.json")
    probs = []
    if man.get("freeze") != "v1":
        probs.append(f"pools/manifest.json is freeze {man.get('freeze')!r}, not v1")
    for name, text in sorted(v1["texts"].items()):
        want = man["files"].get(name, {}).get("sha256")
        if sha_bytes(text.encode("utf-8")) != want:
            probs.append(f"{name}: the in-memory v1 rebuild differs from pools/manifest.json")
        f = POOLS_V1 / name
        if not f.is_file() or sha_file(f) != want:
            probs.append(f"{name}: pools/{name} on disk differs from pools/manifest.json")
    for tid, want in sorted(man["inputs"]["lex_answer_sha256"].items()):
        f = E.ROOT / "answers" / f"{tid}.json"
        if not f.is_file() or sha_file(f) != want:
            probs.append(f"{tid}: extract answer differs from the v1 manifest sha256")
    for bid, want in sorted(man["inputs"]["key_files"].items()):
        f = E.ROOT / "key" / f"{bid}.json"
        if not f.is_file() or sha_file(f) != want:
            probs.append(f"{bid}: extract key file differs from the v1 manifest sha256")
    probs += [f"v1 check_inputs: {x}" for x in v1["ck"]["problems"]]
    probs += [f"v1 reads: {x}" for x in v1["rec"]["problems"]]
    probs += [f"v1 build: {x}" for x in v1["out"]["problems"]]
    if v1["rec"]["g3h"].get("answer_tasks_missing"):
        probs.append(f"v1 g3h answers missing: {v1['rec']['g3h']['answer_tasks_missing']}")
    return {"manifest_sha256": sha_file(POOLS_V1 / "manifest.json"), "version": man["freeze"], "problems": probs,
            "ok": not probs, "manifest": man}


def v1_stage() -> dict:
    """Rebuild v1 in memory once per process (about a minute): freeze.rebuild / check_inputs / record_reads / admission /
    build, then prove it equals the frozen pools/. The registry in the result carries the v1 votes; callers copy it."""
    if _V1:
        return _V1
    rb = F1.rebuild()
    ck = F1.check_inputs(rb)
    rec = F1.record_reads(rb)
    adm = F1.admission(rb)
    out = F1.build(rb, rec, adm)
    v1 = {"rb": rb, "ck": ck, "rec": rec, "adm": adm, "out": out, "texts": v1_file_texts(rb, out),
          "batches": A.build_batches()}
    v1["integrity"] = v1_integrity(v1)
    _V1.update(v1)
    return _V1


# ------------------------------------------------------------------------------------------------ answer files, all rounds
def v1_author_records(v1: dict, excluded) -> tuple:
    """(records, blockers) for haiku/author/answers: every v1 author answer must be valid (v1 cannot be rebuilt otherwise)."""
    recs, blockers = [], []
    for name, (b, _plan) in v1["batches"].items():
        for ch in b.chunks:
            items = {it["qid"]: it for it in ch["items"]}
            ans, rec = read_answer_file("v1-author", b.kind, ch["task_id"], A.ROOT / b.answer_path(ch["task_id"]),
                                        items, excluded)
            recs.append(rec)
            if ans is None:
                blockers.append(f"v1 author answer {ch['task_id']} is {rec['status']}: {rec['problems'][:1]}")
    return recs, blockers


def v1_extract_reads(v1: dict, excluded) -> tuple:
    """(records, blockers, read batches) for haiku/extract/answers. G-LEX reads must be valid (they are v1's votes); a
    g3h read that is not valid just leaves its notes unread."""
    recs, blockers, reads = [], [], []
    for read, kind, b in v1["rb"]["batches"]:
        tasks = [(c["task_id"], E.ROOT / b.answer_path(c["task_id"]), {it["qid"]: it for it in c["items"]})
                 for c in b.chunks]
        rbatch = ReadBatch("v1", read, kind, b.batch_id, dict(b.key), b.prompt_sha, tasks)
        for tid, path, items in tasks:
            ans, rec = read_answer_file("v1-extract", kind, tid, path, items, excluded)
            recs.append(rec)
            if ans is None:
                if kind == "extract_lex":
                    blockers.append(f"v1 extract answer {tid} is {rec['status']}: {rec['problems'][:1]}")
                continue
            rbatch.used_tasks[tid] = rec["sha256"]
            rbatch.answers.update(ans)
        reads.append(rbatch)
    return recs, blockers, reads


def redo1_records(excluded) -> tuple:
    """haiku/redo (round 1): the three g3h re-reads. Same contract; plus the redo task text must be unchanged and the file
    must be byte-identical to the copy in haiku/extract/answers (that copy is what the v1 g3h batch reads)."""
    idx = read_json(REDO1 / "TASKS.json")
    recs, problems = [], []
    for t in idx["tasks"]:
        chunk = read_json(Path(t["source_chunk"]))
        items = {it["qid"]: it for it in chunk["items"]}
        path = Path(t["answer_file"])
        tid = chunk["task_id"]
        ans, rec = read_answer_file("redo", "extract_g3h", tid, path, items, excluded)
        bad = []
        tf = Path(t["task_file"])
        if not tf.is_file() or sha_file(tf) != t["redo_task_text_sha256"]:
            bad.append("the redo task text differs from the sha256 in TASKS.json")
        orig = Path(t["original_answer_file"])
        if rec["sha256"] is not None and (not orig.is_file() or sha_file(orig) != rec["sha256"]):
            bad.append("haiku/extract/answers copy is not byte-identical to the redo answer")
        if bad:
            rec["problems"] += bad
            if rec["status"] == "valid":
                rec["status"] = "invalid"
        recs.append(rec)
    problems += [f"redo {r['task_id']}: {r['problems'][0]}" for r in recs if r["status"] != "valid"]
    return recs, problems


# ------------------------------------------------------------------------------------------------ redo2 / redo3 load
def load_round(root: Path, rnd: str, excluded, problems: list, pools: dict, read_kinds=("extract_lex",)) -> tuple:
    """One redo round folder (TASKS.json + chunks/ key/ manifest/ plan/ tasks/ answers/): every task through chunk, key,
    plan, manifest and its answer file. pools: {author task kind: pool name}; read_kinds: the read task kinds the round
    holds. -> (records, author items, read batches, info). Task files, chunks and plans are only read."""
    idx = read_json(root / "TASKS.json")
    recs, authors, reads = [], [], {}
    info = {"tasks": len(idx["tasks"]), "by_label": Counter(t.get("label") or t.get("read") for t in idx["tasks"])}
    for t in idx["tasks"]:
        tid, kind, bid = t["task_id"], t["kind"], t["batch_id"]
        label = t.get("label") or t.get("read")
        chunk = read_json(root / "chunks" / f"{tid}.json")
        key = read_json(root / "key" / f"{bid}.json")["key"]
        man = read_json(root / "manifest" / f"{bid}.json")
        plan = read_json(root / "plan" / f"{bid}.json")["plan"]
        items = {it["qid"]: it for it in chunk["items"]}
        bad = []
        want_sha = {x["task_id"]: x["sha256"] for x in man["tasks"]}.get(tid)
        if want_sha != CH.sha(json.dumps(chunk, sort_keys=True, ensure_ascii=False)):
            bad.append("chunk file differs from its manifest sha256")
        if chunk.get("task_id") != tid or chunk.get("kind") != kind or chunk.get("prompt_sha") != t["prompt_sha"]:
            bad.append("chunk header differs from TASKS.json")
        if set(items) - set(key):
            bad.append("an item has no key entry")
        path = root / "answers" / f"{tid}.json"
        if Path(t["answer_file"]).resolve() != path.resolve():
            bad.append("TASKS.json names another answer file")
        task_file = root / "tasks" / f"{tid}.txt"
        if not task_file.is_file():
            bad.append("the task file is missing")
        ans, rec = read_answer_file(rnd, kind, tid, path, items, excluded)
        if bad:
            rec["problems"] += bad
            if rec["status"] == "valid":
                rec["status"] = "invalid"
            ans = None
        recs.append(rec)
        tfs = sha_file(task_file) if task_file.is_file() else None
        if kind in pools:
            if ans is None:
                continue
            pool = pools[kind]
            for qid, a in sorted(ans.items()):
                iid = key[qid]
                if iid not in plan:
                    problems.append(f"{rnd} {tid}: plan entry of {iid} is missing")
                    continue
                authors.append(AuthorItem(pool, iid, a["pack"] if "pack" in a else a["text"], rnd, tid,
                                          chunk["prompt_sha"], rel(path), rec["sha256"], tfs, plan[iid]))
        elif kind in read_kinds:
            name = label
            if kind == "extract_g3h":                       # the read's own name is in the plan ("g3h-r1"), not the label
                names = {v.get("read") for v in plan.values()}
                if len(names) == 1 and None not in names:
                    name = names.pop()
                else:
                    problems.append(f"{rnd} {tid}: the plan of batch {bid} does not name one read")
            rb = reads.get(bid)
            if rb is None:
                rb = reads[bid] = ReadBatch(rnd, name, kind, bid, dict(key), chunk["prompt_sha"], [], plan=dict(plan))
            if rb.name != name:
                problems.append(f"{rnd} {tid}: batch {bid} carries two read labels")
            rb.tasks.append((tid, path, items))
            if ans is not None:
                rb.answers.update(ans)
                rb.used_tasks[tid] = rec["sha256"]
        else:
            problems.append(f"{rnd} {tid}: task kind {kind} is not handled")
    return recs, authors, list(reads.values()), info


def load_redo2(excluded, problems: list) -> tuple:
    """haiku/redo2 -> (records, author items, read batches, info)."""
    return load_round(REDO2, "redo2", excluded, problems, REDO2_POOLS)


def load_redo3(excluded, problems: list) -> tuple:
    """haiku/redo3 (skins, window clauses, backup notes, the g3h-r1 read) and haiku/redo3/reads (the six G-LEX reads of the
    new clauses). -> (records, author items, read batches, info); the reads folder holds no author task."""
    r_recs, authors, g3h_reads, info = load_round(REDO3, "redo3", excluded, problems, REDO3_POOLS, ("extract_g3h",))
    x_recs, x_authors, lex_reads, x_info = load_round(REDO3_READS, "redo3-reads", excluded, problems, {},
                                                      ("extract_lex",))
    if x_authors:
        problems.append("redo3/reads holds an author task")
    info = {"tasks": info["tasks"] + x_info["tasks"], "by_label": dict(info["by_label"] + x_info["by_label"]),
            "authoring": info["tasks"], "reads": x_info["tasks"]}
    return r_recs + x_recs, authors, g3h_reads + lex_reads, info


def redo2_rebuild_check() -> dict:
    """build_redo2.build() must reproduce every non-answer file of haiku/redo2 byte for byte (and TASKS.json's task list)."""
    spec = importlib.util.spec_from_file_location("t01_build_redo2", REDO2 / "build_redo2.py")
    br = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(br)
    res = br.build()
    diffs = [r for r, t in sorted(res["files"].items())
             if not (REDO2 / r).is_file() or safe_read(REDO2 / r).decode("utf-8") != t]
    man = read_json(REDO2 / "TASKS.json")
    if man["tasks"] != json.loads(json.dumps(res["tasks"])):
        diffs.append("TASKS.json (task list)")
    if man.get("registry_sha256") != res["reg"].sha256():
        diffs.append("TASKS.json (registry_sha256)")
    if man.get("g0_sha256") != P.T01.G0_SHA256:
        diffs.append("TASKS.json (g0_sha256)")
    known = set(res["files"]) | {"TASKS.json", "build_redo2.py"}
    extra = sorted(rel(p) for p in REDO2.rglob("*")
                   if p.is_file() and "__pycache__" not in p.parts and p.relative_to(REDO2).parts[0] != "answers"
                   and p.relative_to(REDO2).as_posix() not in known)
    return {"files": len(res["files"]), "differ_or_missing": diffs, "extra_on_disk": extra,
            "builder_sha256": sha_file(REDO2 / "build_redo2.py")}


def discover_unrecognised_rounds() -> list:
    """Round folders under haiku/ this script does not ingest (anything but author, extract, redo, redo2, redo3)."""
    return sorted(rel(p) for p in HAIKU.iterdir() if p.is_dir() and p.name not in KNOWN_ROUNDS
                  and "__pycache__" not in p.parts)


# ------------------------------------------------------------------------------------------------ redo3 baseline + rebuild
BASE_DATA_FILES = tuple(POOL_FILES)       # the nine pool data files (not VALIDATION_REPORT.json or MANIFEST.json)


def _manifest_info(root: Path) -> dict | None:
    f = Path(root) / "MANIFEST.json"
    if not f.is_file():
        return None
    try:
        m = read_json(f)
    except ValueError:
        return {"sha256": sha_file(f), "ready": None, "dir": Path(root).name}
    return {"sha256": sha_file(f), "ready": m.get("ready"), "status": str(m.get("status", ""))[:200],
            "dir": Path(root).name}


def baseline_dir() -> Path | None:
    """The freeze redo3 was authored against: pools_v2_prev/ once the re-freeze moved it aside, else pools_v2/ (before it
    is replaced). None when neither holds a MANIFEST."""
    for d in (POOLS_V2_PREV, POOLS_V2):
        if (d / "MANIFEST.json").is_file():
            return d
    return None


def baseline_check(base_files: dict, root: Path | None) -> dict:
    """The in-memory v1 + redo2 freeze (base_files: {name: text}) must equal the baseline freeze on disk, file by file, and
    the baseline must carry the input shas that redo3/TASKS.json recorded. -> {"ok", "dir", "problems", "manifest_sha256"}"""
    out = {"dir": rel(root) if root else None, "problems": [], "manifest_sha256": None}
    if root is None:
        out["problems"].append("no baseline freeze (pools_v2_prev/ or pools_v2/) to prove redo3's inputs against")
        out["ok"] = False
        out["skipped"] = True
        return out
    man = read_json(root / "MANIFEST.json")
    out["manifest_sha256"] = sha_file(root / "MANIFEST.json")
    out["version"] = man.get("version")
    for name in BASE_DATA_FILES:
        want = man.get("sha256", {}).get(name)
        if name not in base_files or sha_bytes(base_files[name].encode("utf-8")) != want:
            out["problems"].append(f"{name}: the in-memory v1 + redo2 freeze differs from {rel(root)}/MANIFEST.json")
        f = root / name
        if not f.is_file() or sha_file(f) != want:
            out["problems"].append(f"{name}: {rel(root)}/{name} differs from its MANIFEST sha256")
    t3 = REDO3 / "TASKS.json"
    if t3.is_file():
        for name, want in sorted(read_json(t3)["inputs_sha256"].items()):
            if name == "STAGE_A3_REPORT.json":
                continue
            f = root / name
            if not f.is_file() or sha_file(f) != want:
                out["problems"].append(f"{name}: {rel(root)}/{name} is not the input redo3/TASKS.json recorded")
    out["ok"] = not out["problems"]
    out["skipped"] = False
    return out


def _load_builder(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _task_list_equal(on_disk: list, built: list) -> bool:
    return on_disk == json.loads(json.dumps(built))


def redo3_rebuild_check(root: Path | None) -> dict:
    """build_redo3.build() and reads/build_reads.build() must reproduce every non-answer file of haiku/redo3 and
    haiku/redo3/reads byte for byte. Both builders read the freeze they were written against (their POOLS_V2), so each is
    pointed at the baseline `root`. A changed STAGE_A3_REPORT.json (shortfalls are re-read from it) skips the rebuild
    (reported, not blocking); a changed baseline is a baseline_check blocker."""
    out = {"baseline": rel(root) if root else None, "differ_or_missing": [], "extra_on_disk": [], "skipped": None}
    t3 = read_json(REDO3 / "TASKS.json")
    tr = read_json(REDO3_READS / "TASKS.json")
    out["builder_sha256"] = {"build_redo3.py": sha_file(REDO3 / "build_redo3.py"),
                             "reads/build_reads.py": sha_file(REDO3_READS / "build_reads.py")}
    if out["builder_sha256"]["build_redo3.py"] != t3.get("builder_sha256"):
        out["differ_or_missing"].append("build_redo3.py differs from TASKS.json builder_sha256")
    if out["builder_sha256"]["reads/build_reads.py"] != tr.get("builder_sha256"):
        out["differ_or_missing"].append("reads/build_reads.py differs from reads/TASKS.json builder_sha256")
    if t3.get("g0_sha256") != P.T01.G0_SHA256 or tr.get("g0_sha256") != P.T01.G0_SHA256:
        out["differ_or_missing"].append("TASKS.json g0_sha256 differs from the plugin's G0_SHA256")
    if root is None:
        out["skipped"] = "no baseline freeze to read"
        return out
    a3 = C2_BUILD / "STAGE_A3_REPORT.json"
    if not a3.is_file() or sha_file(a3) != t3["inputs_sha256"].get("STAGE_A3_REPORT.json"):
        out["skipped"] = "STAGE_A3_REPORT.json changed since redo3 was built (build_redo3 re-reads the T01 shortfalls from it)"
        return out
    b3 = _load_builder("t01_build_redo3", REDO3 / "build_redo3.py")
    b3.POOLS_V2 = root
    res = b3.build()
    out["redo3_files"] = len(res["files"])
    out["differ_or_missing"] += [f"redo3/{r}" for r, t in sorted(res["files"].items())
                                 if not (REDO3 / r).is_file() or safe_read(REDO3 / r).decode("utf-8") != t]
    if not _task_list_equal(t3["tasks"], res["tasks"]):
        out["differ_or_missing"].append("redo3/TASKS.json (task list)")
    known = set(res["files"]) | {"TASKS.json", "build_redo3.py", "test_build_redo3.py"}
    out["extra_on_disk"] += sorted(rel(p) for p in REDO3.rglob("*")
                                   if p.is_file() and "__pycache__" not in p.parts
                                   and p.relative_to(REDO3).parts[0] not in ("answers", "reads")
                                   and p.relative_to(REDO3).as_posix() not in known)
    br = _load_builder("t01_build_reads", REDO3_READS / "build_reads.py")
    br.POOLS_V2 = root
    rr = br.build()
    out["reads_files"] = len(rr["files"])
    out["differ_or_missing"] += [f"redo3/reads/{r}" for r, t in sorted(rr["files"].items())
                                 if not (REDO3_READS / r).is_file() or safe_read(REDO3_READS / r).decode("utf-8") != t]
    if not _task_list_equal(tr["tasks"], rr["tasks"]):
        out["differ_or_missing"].append("redo3/reads/TASKS.json (task list)")
    if tr.get("new_forms") != json.loads(json.dumps(rr["new_forms"])):
        out["differ_or_missing"].append("redo3/reads/TASKS.json (new_forms)")
    known = set(rr["files"]) | {"TASKS.json", "build_reads.py"}
    out["extra_on_disk"] += sorted(rel(p) for p in REDO3_READS.rglob("*")
                                   if p.is_file() and "__pycache__" not in p.parts
                                   and p.relative_to(REDO3_READS).parts[0] != "answers"
                                   and p.relative_to(REDO3_READS).as_posix() not in known)
    return out


# ------------------------------------------------------------------------------------------------ pack rules (redo2)
_MONTH_DAY = {"january", "february", "march", "april", "may", "june", "july", "august", "september", "october",
              "november", "december", "jan", "feb", "mar", "apr", "jun", "jul", "aug", "sep", "sept", "oct", "nov",
              "dec", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "mon", "tue", "tues",
              "wed", "thu", "thur", "thurs", "fri", "sat", "sun"}
_NUMBER = {"zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
           "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty", "thirty",
           "forty", "fifty", "sixty", "seventy", "eighty", "ninety", "hundred", "thousand", "million", "billion",
           "dozen", "first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth",
           "twice", "thrice", "half"}
_NEG_WORDS = {"no", "not", "none", "nobody", "nothing", "nowhere", "never", "neither", "nor", "without", "cannot",
              "hardly", "scarcely", "barely", "few", "unless", "false"}
_NEG_STEM = re.compile(r"\b(?:lack|fail|deny|denie|refus|declin|neglect|omit|prevent|except)\w*", re.I)
_NEG_PHRASE = re.compile(r"\bfree of\b|\bother than\b", re.I)
_FIRST_RX = re.compile(r"[A-Z][a-z]+")
_SURNAME_RX = re.compile(r"[A-Z][a-z]+(?:-[A-Z][a-z]+)*")
_VENDOR_WORD_RX = re.compile(r"[A-Z][a-z]+")


def pack_values(p: dict) -> list:
    return list(p["people"]) + list(p["topics"].values()) + list(p["filing"].values()) + list(p["perils"]) + \
        list(p["vendors"])


def pack_extra_problems(p: dict, initials, taken_lower) -> list:
    """The redo2 pack rules 6-13 (build_redo2.PACK_EXTRA) beyond validate_pack / lint_pack. p is a valid pack object."""
    probs = []
    taken_lower = set(taken_lower)
    for n in list(p["people"]) + list(p["vendors"]):
        if n.lower() in taken_lower:
            probs.append(f"rule 6: {n!r} is on the TAKEN list")
    if isinstance(initials, str) and re.fullmatch(r"[A-Z]-[A-Z]", initials):
        lo, hi = initials.split("-")
        for n in p["people"]:
            sur = n.split()[-1]
            if not lo <= sur[0] <= hi:
                probs.append(f"rule 7: surname {sur!r} outside {initials}")
        for v in p["vendors"]:
            if not lo <= v.split()[0][0] <= hi:
                probs.append(f"rule 7: vendor {v!r} starts outside {initials}")
    else:
        probs.append(f"rule 7: no initials range in the plan ({initials!r})")
    for n in p["people"]:
        first, *rest = n.split()
        if len(rest) != 1 or not _FIRST_RX.fullmatch(first) or not _SURNAME_RX.fullmatch(rest[0]):
            probs.append(f"rule 8: name shape {n!r}")
    for v in p["vendors"]:
        if not all(_VENDOR_WORD_RX.fullmatch(w) for w in v.split()):
            probs.append(f"rule 8: vendor shape {v!r}")
    for v in pack_values(p):
        words = [w.lower() for w in re.findall(r"[A-Za-z]+", v)]
        if set(words) & _MONTH_DAY:
            probs.append(f"rule 9: month or weekday in {v!r}")
        if set(words) & _NUMBER:
            probs.append(f"rule 9: number word in {v!r}")
        if set(words) & _NEG_WORDS or _NEG_STEM.search(v) or _NEG_PHRASE.search(v):
            probs.append(f"rule 11: negation word in {v!r}")
    if "report" in p["topics"]["cash"].lower():
        probs.append("rule 13: the cash topic contains 'report'")
    return probs


def merge_packs(kept_rows: list, open_slots: dict, cands: list, taken: set, problems: list) -> dict:
    """H46. kept_rows: the v1 pack pool rows. open_slots: {failed slot id: held_out flag}. cands: AuthorItems of packs.
    -> {"accepted": [(slot, AuthorItem, held_out, spare)], "attempts": {iid: [..]}, "unplaced_slots": [...]}."""
    seen = {x.lower() for r in kept_rows for x in r["pack"]["people"] + r["pack"]["vendors"]}
    seen_packs = {json.dumps(r["pack"], sort_keys=True) for r in kept_rows}
    taken_l = {x.lower() for x in taken}
    by_slot, spares = defaultdict(list), []
    for it in sorted(cands, key=lambda c: c.iid):
        slot = it.meta.get("replaces")
        if slot:
            if slot not in open_slots:
                problems.append(f"redo2 {it.task}: {it.iid} replaces {slot}, which v1 kept; the answer is ignored")
                continue
            by_slot[slot].append(it)
        elif it.meta.get("spare"):
            spares.append(it)
        else:
            problems.append(f"redo2 {it.task}: {it.iid} is neither a replacement nor a spare; ignored")
    used, accepted, attempts = set(), [], defaultdict(list)

    def reasons_for(it: AuthorItem) -> list:
        p = it.payload
        r = A.validate_pack(p)
        if not r:
            r = E.lint_pack(p)
        if not r and seen & {x.lower() for x in p["people"] + p["vendors"]}:
            r = ["a name or vendor repeats another pack"]
        if not r:
            r = pack_extra_problems(p, it.meta.get("initials"), taken_l)
        if not r and json.dumps(p, sort_keys=True) in seen_packs:
            r = ["duplicate of another pack"]
        return r

    for slot in sorted(open_slots):
        for it in by_slot.get(slot, []) + [s for s in spares if s.iid not in used]:
            r = reasons_for(it)
            attempts[it.iid].append({"slot": slot, "task": it.task, "reasons": list(r)[:5], "accepted": not r})
            if r:
                continue
            accepted.append((slot, it, open_slots[slot], not it.meta.get("replaces")))
            used.add(it.iid)
            seen |= {x.lower() for x in it.payload["people"] + it.payload["vendors"]}
            seen_packs.add(json.dumps(it.payload, sort_keys=True))
            break
    placed = {a[0] for a in accepted}
    return {"accepted": accepted, "attempts": dict(attempts), "unplaced_slots": sorted(set(open_slots) - placed)}


# ------------------------------------------------------------------------------------------------ wording rules (redo2)
_W8 = ("last later next earlier previously lately soon upcoming overdue past ago yet already now today tonight tomorrow "
       "yesterday currently recently immediately daily weekly morning evening night").split()
_W9 = ("maybe perhaps probably possibly likely seem seems appear appears think believe assume suppose roughly nearly "
       "almost").split()
_W8_RX = re.compile(r"\b(?:" + "|".join(_W8 + _W9) + r")\b", re.I)


def wording_extra_problems(text: str, qform: str) -> list:
    """The redo2 wording rules 8-10 and the per-form construction rules (build_redo2.WORDING_EXTRA / STEER / BRIEF_FIX)."""
    probs = []
    m = _W8_RX.search(K.PH_RE.sub(" ", text))
    if m:
        probs.append(f"redo2 rule 8/9: banned word {m.group()!r}")
    if text.split()[:1] == ["May"]:
        probs.append("redo2 rule 10: starts with 'May'")
    low = text.lower()
    if qform == "ch_deadline" and not re.search(r"\b(?:final|latest)\b", low):
        probs.append("ch_deadline must say 'final' or 'latest' (H44)")
    if qform == "yn_not_over" and "not over the stay limit" not in low:
        probs.append("yn_not_over must use the words 'not over the stay limit' (H42)")
    if qform == "yn_fail_time" and re.search(r"\bto be\b", low):
        probs.append("yn_fail_time must be active voice, never 'fail to be filed' (H42)")
    if qform == "yn_not_timely" and re.search(r"\bdid\b.*\bnot\b|\bdidn't\b|\bfail", low):
        probs.append("yn_not_timely must negate 'filed in time' with 'not', never 'did not file' or 'fail' (H42)")
    return probs


def merge_wordings(seen_texts: set, open_slots: dict, cands: list) -> dict:
    """H42 / H44. seen_texts: lower-cased text of every wording already in the registry. open_slots: {slot id: plan meta}.
    Variant a first, b only if a fails; at most one per slot. -> {"accepted": [(slot, AuthorItem, obj)], "attempts": {...}}"""
    seen = set(seen_texts)
    by_slot = defaultdict(list)
    for it in cands:
        by_slot[it.meta.get("replaces")].append(it)
    accepted, attempts = [], defaultdict(list)
    for slot in sorted(open_slots):
        for it in sorted(by_slot.get(slot, []), key=lambda c: (c.meta.get("variant", ""), c.iid)):
            tmp = set(seen)
            obj, reasons = A.check_wording(it.iid, it.payload, it.meta, it.task, it.psha, tmp)
            reasons = list(reasons)
            if isinstance(it.payload, str):
                reasons += wording_extra_problems(" ".join(it.payload.split()), it.meta["qform"])
            attempts[slot].append({"iid": it.iid, "variant": it.meta.get("variant"), "task": it.task,
                                   "reasons": reasons[:5], "accepted": not reasons})
            if reasons:
                continue
            seen.add(obj[1].lower())
            accepted.append((slot, it, obj))
            break
    return {"accepted": accepted, "attempts": dict(attempts),
            "unplaced_slots": sorted(set(open_slots) - {a[0] for a in accepted})}


def merge_freeform(seen_norms: set, open_slots: set, cands: list) -> dict:
    """H47. seen_norms: A._norm of every note already kept. Variant a first, b only if a fails; at most one per slot."""
    seen = set(seen_norms)
    by_slot = defaultdict(list)
    for it in cands:
        by_slot[it.meta.get("replaces")].append(it)
    accepted, attempts = [], defaultdict(list)
    for slot in sorted(open_slots):
        for it in sorted(by_slot.get(slot, []), key=lambda c: (c.meta.get("variant", ""), c.iid)):
            tmp = set(seen)
            sk, reasons = A.check_freeform(it.iid, it.payload, it.meta, it.task, it.psha, tmp)
            attempts[slot].append({"iid": it.iid, "variant": it.meta.get("variant"), "task": it.task,
                                   "reasons": list(reasons)[:5], "accepted": not reasons})
            if reasons:
                continue
            seen.add(A._norm(sk.text))
            accepted.append((slot, it, sk))
            break
    return {"accepted": accepted, "attempts": dict(attempts),
            "unplaced_slots": sorted(set(open_slots) - {a[0] for a in accepted})}


# ------------------------------------------------------------------------------------------------ redo3 merges
def merge_skins(seen_norms: set, open_slots: dict, cands: list, kept_ids=frozenset()) -> dict:
    """redo3 INGEST (skins). seen_norms: A._norm of every kept skin. open_slots: {register: [v1 slot ids still open]}.
    cands: AuthorItems of skins. Per register, the passing skins in sorted id order fill the open slots in order (the
    register stops at its G0 target); a passing skin beyond that is surplus: reported, never kept.
    -> {"accepted": [(slot, AuthorItem, Skin)], "surplus": [AuthorItem], "attempts": {iid: {...}}, "unplaced_slots": [..]}"""
    seen = set(seen_norms)
    by_reg = defaultdict(list)
    for it in cands:
        by_reg[it.meta.get("register")].append(it)
    accepted, surplus, attempts = [], [], {}
    for reg_ in sorted(by_reg, key=str):
        slots = list(open_slots.get(reg_, []))
        n_acc = 0
        for it in sorted(by_reg[reg_], key=lambda c: c.iid):
            tmp = set(seen)
            sk, reasons = A.check_skin(it.iid, it.payload, it.meta, it.task, it.psha, tmp)
            reasons = list(reasons)
            held = reg_ in HELD_REGISTERS
            if bool(it.meta.get("held_out")) != held:
                reasons.append("plan held_out flag disagrees with the register")
            if it.iid in kept_ids:
                reasons.append("id collides with a kept skin")
            att = {"task": it.task, "register": reg_, "reasons": reasons[:5], "accepted": False, "surplus": False}
            attempts[it.iid] = att
            if reasons:
                continue
            if n_acc >= len(slots):
                att["surplus"] = True
                surplus.append(it)
                continue
            accepted.append((slots[n_acc], it, sk))
            att["accepted"] = True
            n_acc += 1
            seen.add(A._norm(sk.text))
    placed = {a[0] for a in accepted}
    return {"accepted": accepted, "surplus": surplus, "attempts": attempts,
            "unplaced_slots": sorted(s_ for sl in open_slots.values() for s_ in sl if s_ not in placed)}


def merge_windows(seen_texts: set, cands: list) -> dict:
    """redo3 INGEST (windows). seen_texts: every window text of the registry. haiku_author.check_lexicon, then the clause
    lint (extract.lint_clause: flags are logged, never a drop, H43) and the normalised-text dedup. Every kept clause is a new
    registry form that still needs its reads. -> {"kept": [(AuthorItem, piece)], "attempts": {iid: {...}}}"""
    seen = {t.lower() for t in seen_texts}
    seen_n = {E._norm(t) for t in seen_texts}
    kept, attempts = [], {}
    for it in sorted(cands, key=lambda c: c.iid):
        tmp = set(seen)
        obj, reasons = A.check_lexicon(it.iid, it.payload, it.meta, it.task, it.psha, tmp)
        reasons = list(reasons)
        piece = None
        if not reasons:
            sem, _kind, text, slots, tid, psha = obj
            if E._norm(text) in seen_n:
                reasons.append("duplicate of an existing window clause")
            else:
                piece = {"pid": it.iid, "group": "windows", "task_id": tid, "prompt_sha": psha, "held_out": False,
                         "text": text, "lexkind": "window", "sem": sem, "slots": dict(slots)}
                piece["gsl_flags"] = E.lint_clause(piece)
        attempts[it.iid] = {"task": it.task, "sem": it.meta.get("sem"), "reasons": reasons[:5],
                            "accepted": not reasons}
        if reasons:
            continue
        seen.add(piece["text"].lower())
        seen_n.add(E._norm(piece["text"]))
        kept.append((it, piece))
    return {"kept": kept, "attempts": attempts}


def check_backup_notes(seen_norms: set, cands: list) -> dict:
    """redo3 INGEST (freeform_backup). haiku_author.check_freeform with the plan facts, variant by sorted id. A passing note
    is a reserve: it is used only to replace a dropped note, and then still needs its own g3h-r1 read.
    -> {"passing": [(AuthorItem, Skin)], "attempts": {iid: {...}}}"""
    seen = set(seen_norms)
    passing, attempts = [], {}
    for it in sorted(cands, key=lambda c: c.iid):
        tmp = set(seen)
        sk, reasons = A.check_freeform(it.iid, it.payload, it.meta, it.task, it.psha, tmp)
        attempts[it.iid] = {"task": it.task, "reasons": list(reasons)[:5], "accepted": not reasons}
        if reasons:
            continue
        seen.add(A._norm(sk.text))
        passing.append((it, sk))
    return {"passing": passing, "attempts": attempts}


# ------------------------------------------------------------------------------------------------ G-LEX votes
def copy_registry(reg: L.LexiconRegistry) -> L.LexiconRegistry:
    """A copy with every vote (to_json / from_json re-runs the unit tests); the v1 registry stays as v1 left it."""
    return L.LexiconRegistry.from_json(json.loads(json.dumps(reg.to_json())))


def record_lex_votes(reg: L.LexiconRegistry, rb: ReadBatch, problems: list) -> Counter:
    """reg.record_extraction for every answered item of one valid-file G-LEX read; extractor id = the read's name. A
    meaning that is not the unique meaning of a sem of the form's kind records None (rejects). The item must be the
    form's own filled text (plan 'filled') with the kind's own meaning list."""
    c = Counter()
    for tid, _path, items in rb.tasks:
        if tid not in rb.used_tasks:
            continue
        for qid, item in items.items():
            fid = rb.key[qid]
            f = reg.forms.get(fid)
            if f is None:
                problems.append(f"{rb.name}: form {fid} is not in the registry")
                continue
            exp = rb.plan.get(fid)
            if exp is not None and (item["text"] != exp.get("filled") or exp.get("sem_id") != f.sem_id):
                problems.append(f"{rb.name}: the item of {fid} is not the form's planned text")
                continue
            kind_meanings = {s.meaning for s in reg.sems.values() if s.kind == f.kind}
            if set(item["choices"]) != kind_meanings:
                problems.append(f"{rb.name}: the item of {fid} does not list the meanings of kind {f.kind}")
                continue
            if qid not in rb.answers:
                continue
            sem = reg.meaning_to_sem(f.kind, rb.answers[qid]["meaning"])
            c["listed" if sem == f.sem_id else "other_sense" if sem else "unlisted"] += 1
            try:
                reg.record_extraction(fid, rb.name, sem)
            except L.LexiconError as e:
                problems.append(f"{rb.name}: {str(e)[:100]}")
    return c


def confirm_need(kind: str) -> tuple:
    return CONFIRM_READS_WINDOW if kind == "window" else CONFIRM_READS


def independent_need(kind: str) -> tuple:
    """The G-LEX reads whose agreement admits a form (2/2; 3/3 for window rules): glex-r1, -r2 (+ -r3)."""
    return INDEPENDENT_READS_WINDOW if kind == "window" else INDEPENDENT_READS


def lex_state(reg: L.LexiconRegistry, fid: str) -> tuple:
    """(state, detail) of one form after the H45 reads: used | rejected | unconfirmed | not_admitted. A form is used only
    when it is admitted by the kit rule AND every independent read (glex-r1, -r2, -r3 for windows) and every confirmation
    read (glex-r1b, -r2b, -r3b for windows) is on its sem: the confirmation reads alone never stand in for the first ones."""
    st = reg.status(fid)
    f = reg.forms[fid]
    have = {e for e, _ in f.extractions}
    miss_c = [r for r in confirm_need(f.kind) if r not in have]
    miss_i = [r for r in independent_need(f.kind) if r not in have]
    if st == "rejected":
        bad = [f"{e}: {s if s else 'unlisted meaning'}" for e, s in f.extractions if s != f.sem_id]
        return "rejected", "a read disagrees with the declared sem (" + ", ".join(bad) + ")"
    if st != "admitted":
        return "not_admitted", f"G-LEX status {st}"
    if miss_c or miss_i:
        why = []
        if miss_i:
            why.append("independent G-LEX read(s) missing: " + ", ".join(miss_i))
        if miss_c:
            why.append("confirmation read(s) missing: " + ", ".join(miss_c))
        return "unconfirmed", "; ".join(why)
    return "used", ""


# ------------------------------------------------------------------------------------------------ G3-H
def g3h_results(docs: dict, reads: list, problems: list) -> tuple:
    """({pid: (ok, diffs)}, template report). docs: {pid: piece with g3h_expect}. One entry per note; every valid read of it
    must match exactly; a note with no valid read is 'unanswered' (not admitted, not a mismatch)."""
    fields = P.T01().extract_fields(None)
    got = defaultdict(list)
    for rb in reads:
        if rb.kind != "extract_g3h":
            continue
        for tid, _path, items in rb.tasks:
            if tid not in rb.used_tasks:
                continue
            for qid, item in items.items():
                pid = rb.key[qid]
                if pid not in docs:
                    problems.append(f"{rb.name}: read of {pid}, which is not a candidate note")
                    continue
                if item["text"] != docs[pid]["text"]:
                    problems.append(f"{rb.name}: the item of {pid} is not the note's text")
                    continue
                if qid in rb.answers:
                    got[pid].append((rb.name, rb.answers[qid]))
    ok_of, results = {}, []
    for pid in sorted(docs):
        rs = got.get(pid, [])
        if not rs:
            ok_of[pid] = (None, ["unanswered"])
            continue
        diffs = []
        for name, a in rs:
            ok, d = g3h.compare(docs[pid]["g3h_expect"], a, fields)
            diffs += [f"{name}: {x}" for x in d]
        ok_of[pid] = (not diffs, diffs)
        results.append((pid, pid, ok_of[pid][0]))
    return ok_of, g3h.template_report(results)


def g3h_sources(reads: list) -> dict:
    """{note pid: [(read name, task id, answer sha256)]} for every valid-file answer: where each G3-H verdict came from."""
    out = defaultdict(list)
    for rb in reads:
        if rb.kind != "extract_g3h":
            continue
        for tid, _path, items in rb.tasks:
            if tid in rb.used_tasks:
                for qid in items:
                    if qid in rb.answers:
                        out[rb.key[qid]].append((rb.name, tid, rb.used_tasks[tid]))
    return dict(out)


# ------------------------------------------------------------------------------------------------ counts and targets
def compute_counts(pools: dict) -> dict:
    """The numbers the G0 targets are checked against, from the final pool rows."""
    packs = pools["packs"]
    skin_reg = Counter((r["register"], bool(r["held_out"])) for r in pools["skins"])
    return {
        "packs": {"total": len(packs), "held_out": sum(1 for r in packs if r["held_out"]),
                  "training": sum(1 for r in packs if not r["held_out"])},
        "skins_by_register": {f"{r}|held_out={h}": n for (r, h), n in sorted(skin_reg.items())},
        "skins_training": {r: skin_reg[(r, False)] for r in TRAIN_REGISTERS},
        "skins_held_out": {r: skin_reg[(r, True)] for r in HELD_REGISTERS},
        "skins_total": len(pools["skins"]),
        "documents_admitted": len(pools["documents"]),
        "documents_pending": len(pools["documents_pending_g3h"]),
        "documents_by_register": dict(sorted(Counter(r["register"] for r in pools["documents"]).items())),
        "wordings_admitted": len(pools["wordings"]),
        "wordings_by_qform": dict(sorted(Counter(r["qform"] for r in pools["wordings"]).items())),
        "windows_by_sem": {s: sum(1 for r in pools["windows"] if r["sem"] == s) for s in WINDOW_SEMS},
        "comparators_by_sem": {s: sum(1 for r in pools["comparators"] if r["sem"] == s) for s in COMPARATOR_SEMS},
    }


def shortfalls(c: dict) -> list:
    """The G0 minimums, as freeze.build states them (freeze.TARGET, never lowered). Per-form wording counts are asked
    counts (H42), reported separately by asked_count_gaps."""
    short = []

    def add(name, have, want):
        if have < want:
            short.append(f"{name}: {have} of {want} (short {want - have})")

    add("packs total", c["packs"]["total"], TARGET["packs"])
    add("packs held out", c["packs"]["held_out"], TARGET["packs_held_out"])
    add("packs training", c["packs"]["training"], TARGET["packs"] - TARGET["packs_held_out"])
    for r_ in TRAIN_REGISTERS:
        add(f"skins {r_} (training)", c["skins_training"][r_], TARGET["skins_per_training_register"])
    for r_ in HELD_REGISTERS:
        add(f"skins {r_} (held out)", c["skins_held_out"][r_], TARGET["skins_per_held_register"])
    add("skins total", c["skins_total"], TARGET["skins_per_training_register"] * len(TRAIN_REGISTERS)
        + TARGET["skins_per_held_register"] * len(HELD_REGISTERS))
    add("documents admitted (G3-H)", c["documents_admitted"], TARGET["documents"])
    add("wordings admitted (minimum)", c["wordings_admitted"], TARGET["wordings_min_admitted"])
    for s_ in WINDOW_SEMS:
        add(f"window {s_}", c["windows_by_sem"][s_], TARGET["windows_per_sem"])
    for s_ in COMPARATOR_SEMS:
        add(f"comparator {s_}", c["comparators_by_sem"][s_], TARGET["comparators_per_sem"])
    return short


def asked_count_gaps(c: dict) -> list:
    """Per-form wording counts against the asked counts of G0 section 7 (informational since H42: the floor is 30 admitted)."""
    qforms = P.T01().QFORMS
    out = []
    for q in sorted(qforms):
        want = PER_FORM_ASKED[F1.qform_class(qforms[q])]
        have = c["wordings_by_qform"].get(q, 0)
        if have < want:
            out.append(f"wording {q}: {have} of {want} asked (short {want - have})")
    return out


# ------------------------------------------------------------------------------------------------ assemble
def data_files(a: dict) -> dict:
    """The nine pool data files of a result as run() writes them: {name: text}."""
    p = a["pools"]
    return {"packs.jsonl": jsonl(p["packs"]), "skins.jsonl": jsonl(p["skins"]), "documents.jsonl": jsonl(p["documents"]),
            "documents_pending_g3h.jsonl": jsonl(p["documents_pending_g3h"]), "wordings.jsonl": jsonl(p["wordings"]),
            "windows.jsonl": jsonl(p["windows"]), "comparators.jsonl": jsonl(p["comparators"]),
            "lexicon_registry.json": dump(a["reg"].to_json()), "quarantine.jsonl": jsonl(a["quarantine"])}


def is_ready(a: dict) -> bool:
    return bool(not a["short"] and a["gates"]["G-LEX"]["pass"] and a["gates"]["G3-H"]["pass"] and not a["blockers"])


_BASE: dict = {}      # (baseline manifest sha256, its exclusions) -> baseline_check result (the v1 + redo2 rebuild takes a minute)


def base_stage_check(root: Path | None) -> dict:
    """Rebuild v1 + redo2 alone (the exclusions the baseline itself recorded) and compare it with the baseline freeze."""
    if root is None:
        return baseline_check({}, None)
    man = read_json(root / "MANIFEST.json")
    prev_excl = tuple(sorted(man.get("excluded_tasks_audit_failed", [])))
    key = (str(root), sha_file(root / "MANIFEST.json"), prev_excl)
    if key not in _BASE:
        _BASE[key] = baseline_check(data_files(_stage(set(prev_excl), with_redo3=False)), root)
    return json.loads(json.dumps(_BASE[key]))


def assemble(rebuild_check: bool = True, exclude=()) -> dict:
    """The whole freeze in memory: v1 + redo2 + redo3. Before redo3 is applied the v1 + redo2 result is rebuilt on its own and
    must equal the baseline freeze (pools_v2_prev/) that redo3 was authored against."""
    excluded = set(exclude)
    has3 = (REDO3 / "TASKS.json").is_file()
    root = baseline_dir() if has3 else None
    a = _stage(excluded, with_redo3=has3)
    if has3:
        chk = base_stage_check(root)
        a["baseline"] = chk
        if chk["skipped"]:
            a["problems"].append(chk["problems"][0])
        elif not chk["ok"]:
            a["blockers"].append("redo3 baseline: " + "; ".join(chk["problems"][:3]))
    else:
        a["baseline"] = None
    if rebuild_check:
        chk2 = redo2_rebuild_check()
        a["redo_checks"]["redo2"]["rebuild"] = chk2
        if chk2["differ_or_missing"] or chk2["extra_on_disk"]:
            a["blockers"].append(f"redo2 rebuild differs from disk: {chk2['differ_or_missing'][:2]} {chk2['extra_on_disk'][:2]}")
        if has3:
            chk3 = redo3_rebuild_check(root)
            a["redo_checks"]["redo3"]["rebuild"] = chk3
            if chk3["differ_or_missing"] or chk3["extra_on_disk"]:
                a["blockers"].append(f"redo3 rebuild differs from disk: {chk3['differ_or_missing'][:2]} "
                                     f"{chk3['extra_on_disk'][:2]}")
            if chk3["skipped"]:
                a["problems"].append(f"redo3 rebuild check skipped: {chk3['skipped']}")
    else:
        a["redo_checks"]["redo2"]["rebuild"] = "skipped (--no-rebuild-check)"
        if has3:
            a["redo_checks"]["redo3"]["rebuild"] = "skipped (--no-rebuild-check)"
    a["ready"] = is_ready(a)
    return a


def _stage(excluded: set, with_redo3: bool) -> dict:
    blockers, problems = [], []
    v1 = v1_stage()
    rb1, out1 = v1["rb"], v1["out"]
    blockers += [f"v1: {p}" for p in v1["integrity"]["problems"]]

    # ---- answer files of every round
    records = []
    a_recs, a_blk = v1_author_records(v1, excluded)
    records += a_recs
    blockers += a_blk
    x_recs, x_blk, v1_reads = v1_extract_reads(v1, excluded)
    records += x_recs
    blockers += x_blk
    r1_recs, r1_probs = redo1_records(excluded)
    records += r1_recs
    problems += r1_probs
    r2_recs, r2_authors, r2_reads, r2_info = load_redo2(excluded, problems)
    records += r2_recs
    r3_recs, r3_authors, r3_reads, r3_info = [], [], [], None
    if with_redo3:
        r3_recs, r3_authors, r3_reads, r3_info = load_redo3(excluded, problems)
        records += r3_recs
    redo_checks = {"redo": {"tasks": len(r1_recs), "valid": sum(1 for r in r1_recs if r["status"] == "valid")},
                   "redo2": {"tasks": len(r2_recs), "valid": sum(1 for r in r2_recs if r["status"] == "valid"),
                             "by_label": dict(r2_info["by_label"]), "rebuild": "not run"}}
    if with_redo3:
        redo_checks["redo3"] = {"tasks": len(r3_recs), "valid": sum(1 for r in r3_recs if r["status"] == "valid"),
                                "authoring_tasks": r3_info["authoring"], "read_tasks": r3_info["reads"],
                                "by_label": dict(r3_info["by_label"]), "rebuild": "not run"}
    unrecognised = discover_unrecognised_rounds()
    if unrecognised:
        blockers.append(f"round folder(s) this script does not ingest: {unrecognised}")
    known = {r["file"] for r in records}
    adirs = [A.ROOT / "answers", E.ROOT / "answers", REDO1 / "answers", REDO2 / "answers"]
    if with_redo3:
        adirs += [REDO3 / "answers", REDO3_READS / "answers"]
    stray = sorted({rel(p) for d in adirs if d.is_dir() for p in d.glob("*")
                    if p.is_file() and rel(p) not in known and p.name != "README.txt"})

    # ---- the v1 pieces, unchanged
    surv, row_of = rb1["surv"], dict(rb1["row_of"])
    pools_v1 = out1["pools"]
    plans = {n: pl for n, (_b, pl) in v1["batches"].items()}
    kept_pack_ids = {r["pid"] for r in pools_v1["packs"]}
    open_pack_slots = {iid: plans["packs"][iid]["held_out"] for iid in sorted(plans["packs"]) if iid not in kept_pack_ids}
    adm_word_pids = {row_of[f]["pid"] for f in v1["adm"]["admitted"] if row_of[f]["group"] == "wordings"}
    open_word_slots = {iid: plans["wordings"][iid] for iid in sorted(plans["wordings"]) if iid not in adm_word_pids}
    kept_doc_pids = {p["pid"] for p in surv["freeform"]}
    open_doc_slots = {iid for iid in plans["freeform"] if iid not in kept_doc_pids}

    # ---- redo2 authoring pieces
    taken = set(P.PEOPLE) | set(P.RESERVE_PEOPLE) | set(P.VENDORS) | {"Dana Okafor"}
    mp = merge_packs(pools_v1["packs"], open_pack_slots, [i for i in r2_authors if i.pool == "packs"], taken, problems)
    reg = copy_registry(rb1["reg"])
    seen_w = {f.text.lower() for f in reg.forms.values() if f.kind == "question"}
    mw = merge_wordings(seen_w, open_word_slots, [i for i in r2_authors if i.pool == "wordings"])
    seen_d = {A._norm(p["text"]) for p in surv["freeform"]}
    mf = merge_freeform(seen_d, open_doc_slots, [i for i in r2_authors if i.pool == "freeform"])
    for pool, open_s, m in (("packs", open_pack_slots, mp), ("wordings", open_word_slots, mw),
                            ("freeform", open_doc_slots, mf)):
        planned = {i.meta.get("replaces") for i in r2_authors if i.pool == pool and i.meta.get("replaces")}
        if planned - set(open_s):
            problems.append(f"redo2 {pool}: plan replaces slot(s) v1 kept: {sorted(planned - set(open_s))}")
        if set(open_s) - planned and r2_authors:
            problems.append(f"redo2 {pool}: no replacement was planned for slot(s) {sorted(set(open_s) - planned)}")

    # ---- registry: v1 forms + the redo2 wordings that passed the checks (no votes), then every vote
    new_forms, add_probs = [], []
    for slot, it, (q, text, slots, tid, psha) in [(s, i, o) for s, i, o in mw["accepted"]]:
        try:
            f = reg.add(text, L.question_sem(FAMILY, q), slots=slots, source="haiku", family=FAMILY,
                        haiku_task_id=tid, haiku_prompt_sha=psha)
        except L.LexiconError as e:
            add_probs.append((slot, it, str(e)[:100]))
            continue
        reg.unit_test(f.form_id)
        new_forms.append((slot, it, f.form_id, q, text, slots, tid, psha))
    vote_counts = {}
    read_batches = v1_reads + r2_reads
    confirm_reads = [rb for rb in r2_reads if rb.kind == "extract_lex"]
    for rb in confirm_reads:
        vote_counts[f"{rb.round}:{rb.name}"] = dict(record_lex_votes(reg, rb, problems))
    labels = {rb.name for rb in confirm_reads}
    if not set(CONFIRM_READS_WINDOW) <= labels:
        problems.append(f"redo2 confirmation reads found: {sorted(labels)}; H45 needs {list(CONFIRM_READS_WINDOW)}")

    # ---- redo3: skins into the v1 slots that stayed open, window clauses as new registry forms, backup notes
    ms = mwin = bk = None
    new_win, win_add_probs, r3_sum = [], [], {"active": with_redo3}
    if with_redo3:
        kept_skin_ids = {r["pid"] for r in pools_v1["skins"]}
        open_skin_slots = {r_: sorted(i for i, m in plans["skins"].items()
                                      if m["register"] == r_ and i not in kept_skin_ids)
                           for r_ in TRAIN_REGISTERS + HELD_REGISTERS}
        ms = merge_skins({A._norm(r["text"]) for r in pools_v1["skins"]}, open_skin_slots,
                         [i for i in r3_authors if i.pool == "skins"], kept_skin_ids)
        mwin = merge_windows({f.text for f in reg.forms.values() if f.kind == "window"},
                             [i for i in r3_authors if i.pool == "windows"])
        for it, piece in mwin["kept"]:
            try:
                f = reg.add(piece["text"], piece["sem"], slots=piece["slots"], source="haiku", family=FAMILY,
                            haiku_task_id=piece["task_id"], haiku_prompt_sha=piece["prompt_sha"])
            except L.LexiconError as e:
                win_add_probs.append((it, str(e)[:100]))
                continue
            reg.unit_test(f.form_id)
            row_of[f.form_id] = dict(piece, round="redo3")
            new_win.append((it, piece, f.form_id))
        # the six G-LEX reads were built for the clauses build_reads.py kept: the same forms, from the same answer file
        rt = read_json(REDO3_READS / "TASKS.json")
        by_task = {r["task_id"]: r for r in r3_recs}
        for tid, want in sorted(rt.get("source_answers_sha256", {}).items()):
            rec = by_task.get(tid)
            if rec is not None and rec["sha256"] is not None and rec["sha256"] != want:
                blockers.append(f"redo3 reads were built from another {tid} answer than the one on disk")
        built = {x["form_id"] for x in rt["new_forms"]}
        if built != {fid for _i, _p, fid in new_win} and any(r["status"] == "valid" and r["kind"] == "author_lexicon"
                                                              for r in r3_recs):
            problems.append("redo3 reads: the forms they were built for differ from the forms the redo3 window answers "
                            f"give ({len(built)} vs {len(new_win)})")
        r3_lex = [rb for rb in r3_reads if rb.kind == "extract_lex"]
        for rb in r3_lex:
            if not any(fid in reg.forms for fid in rb.key.values()):
                problems.append(f"{rb.round}:{rb.name}: none of its forms exists (the window answers were not used)")
                continue
            vote_counts[f"{rb.round}:{rb.name}"] = dict(record_lex_votes(reg, rb, problems))
        labels3 = {rb.name for rb in r3_lex}
        need3 = set(INDEPENDENT_READS_WINDOW) | set(CONFIRM_READS_WINDOW)
        if not need3 <= labels3:
            problems.append(f"redo3 G-LEX reads found: {sorted(labels3)}; 3/3 plus H45 need {sorted(need3)}")
        read_batches = read_batches + r3_reads

    # ---- G-LEX state of every form
    v1_admitted = list(v1["adm"]["admitted"])
    state = {fid: lex_state(reg, fid) for fid in v1_admitted + [fid for _i, _p, fid in new_win]}
    used = sorted(fid for fid, (s, _d) in state.items() if s == "used")
    for fid, f1 in rb1["reg"].forms.items():                        # v1's own votes and verdicts must still stand
        f2 = reg.forms[fid]
        if f2.extractions[:len(f1.extractions)] != f1.extractions:
            blockers.append(f"v1 form {fid}: its v1 votes changed")
    gate_used = reg.gate(used_form_ids=used)
    gate_all = reg.gate()

    # ---- pool rows
    def lex_row(fid: str) -> dict:
        f = reg.forms[fid]
        row = E._pool_row(row_of[fid])
        row.update({"form_id": fid, "sem_id": f.sem_id, "kind": f.kind,
                    "g_lex": {"status": reg.status(fid), "required": f.required,
                              "confirm_reads_required": list(confirm_need(f.kind)),
                              "reads": [[e, s] for e, s in f.extractions]}})
        return row

    order = lambda f: (row_of[f]["group"], row_of[f]["pid"])  # noqa: E731
    pools = {g: [] for g in ("wordings", "windows", "comparators")}
    for fid in sorted(used, key=order):
        pools[row_of[fid]["group"]].append(lex_row(fid))
    pack_rows = [dict(r) for r in pools_v1["packs"]]
    for slot, it, held, spare in mp["accepted"]:
        pack_rows.append({"pid": it.iid, "group": "packs", "task_id": it.task, "prompt_sha": it.psha, "held_out": held,
                          "pack": it.payload, "slot": slot, "spare": spare, "round": "redo2"})
    skin_rows = [dict(r) for r in pools_v1["skins"]]
    if ms:
        for slot, it, sk in ms["accepted"]:
            skin_rows.append(E._pool_row({"pid": it.iid, "group": "skins", "task_id": it.task, "prompt_sha": it.psha,
                                          "held_out": bool(it.meta["held_out"]), "text": sk.text,
                                          "register": it.meta["register"], "escape": it.meta["escape"],
                                          "decl": dict(A.NARR), "slot": slot, "round": "redo3"}))

    # ---- notes: G3-H
    docs = {p["pid"]: p for p in surv["freeform"]}
    new_docs = {}
    for slot, it, sk in mf["accepted"]:
        meta = it.meta
        facts = dict(meta["facts"])
        new_docs[it.iid] = {"pid": it.iid, "group": "freeform", "task_id": it.task, "prompt_sha": it.psha,
                            "held_out": False, "text": sk.text, "register": meta["register"], "facts": facts,
                            "g3h_expect": {"person": facts["PERSON"], "ref": facts["REF"], "topic": facts["TOPIC"]},
                            "slot": slot, "round": "redo2"}
    cand_docs = {**docs, **new_docs}
    all_reads = v1_reads + r2_reads + [rb for rb in r3_reads if rb.kind == "extract_g3h"]
    g_ok, g_report = g3h_results(cand_docs, all_reads, problems)
    # backup notes (redo3): used only to replace a note the g3h-r1 read dropped; they still wait for their own read
    backups_used, bk_rows = [], {}
    if with_redo3:
        bk = check_backup_notes(seen_d | {A._norm(sk.text) for _s, _i, sk in mf["accepted"]},
                                [i for i in r3_authors if i.pool == "backup_notes"])
        wanted = sorted({n for i in r3_authors if i.pool == "backup_notes" for n in i.meta.get("backup_for", [])})
        dropped = [pid for pid in wanted if g_ok.get(pid, (None, []))[0] is False]
        for pid, (it, sk) in zip(dropped, bk["passing"]):
            facts = dict(it.meta["facts"])
            bk_rows[it.iid] = {"pid": it.iid, "group": "freeform", "task_id": it.task, "prompt_sha": it.psha,
                               "held_out": False, "text": sk.text, "register": it.meta["register"], "facts": facts,
                               "g3h_expect": {"person": facts["PERSON"], "ref": facts["REF"], "topic": facts["TOPIC"]},
                               "slot": cand_docs[pid].get("slot", pid), "round": "redo3", "backup_for": pid}
            g_ok[it.iid] = (None, ["unanswered"])
            backups_used.append((pid, it.iid))
        cand_docs = {**cand_docs, **bk_rows}
    doc_rows, pending_rows, doc_quar = [], [], []
    src = g3h_sources(all_reads)
    for pid in sorted(cand_docs):
        ok, diffs = g_ok[pid]
        base = E._pool_row(cand_docs[pid])
        if ok is True:
            doc_rows.append(dict(base, status="admitted_g3h",
                                 g3h={"read": G3H_READ, "match": True,
                                      "reads": [{"read": n, "task_id": t, "answer_sha256": h} for n, t, h in src[pid]]}))
        elif ok is None:
            pending_rows.append(dict(base, status="pending_g3h"))
        else:
            doc_quar.append({"stage": "G3-H", "group": "freeform", "pid": pid, "task_id": cand_docs[pid]["task_id"],
                             "prompt_sha": cand_docs[pid]["prompt_sha"], "held_out": False, "status": "mismatch",
                             "reasons": diffs[:3]})

    final = {"packs": pack_rows, "skins": skin_rows, "documents": doc_rows,
             "documents_pending_g3h": pending_rows, **pools}
    counts = compute_counts(final)
    short = shortfalls(counts)
    gaps = asked_count_gaps(counts)

    # ---- slot accounting (authored = admitted + pending + quarantined, by slot)
    extra_authored = {"windows": sum(1 for i in r3_authors if i.pool == "windows")} if with_redo3 else {}
    slot_counts = slot_accounting(v1, final, state, new_forms, mp, mf, row_of, reg, extra_authored)
    problems += [f"slot accounting: {x}" for x in slot_counts["problems"]]

    # ---- quarantine
    quar, resolved = build_quarantine(v1, out1, mp, mw, mf, add_probs, state, new_forms, doc_quar, reg, row_of,
                                      ms=ms, mwin=mwin, win_add_probs=win_add_probs,
                                      bk=bk if with_redo3 else None, backups_used=backups_used)

    # ---- verdict
    pend_forms = sorted(fid for fid, (s, _d) in state.items() if s == "unconfirmed")
    rej_forms = sorted(fid for fid, (s, _d) in state.items() if s == "rejected")
    unanswered = sorted(pid for pid, (ok, _d) in g_ok.items() if ok is None)
    mismatched = sorted(pid for pid, (ok, _d) in g_ok.items() if ok is False)
    gates = {
        "G-LEX": {"used_forms": len(used), "gate_over_used_forms": {k: gate_used[k] for k in
                                                                    ("n_forms", "status_counts", "pass")},
                  "v1_admitted_forms": len(v1_admitted), "redo3_window_forms": len(new_win),
                  "unconfirmed_forms": len(pend_forms), "rejected_by_confirmation": len(rej_forms),
                  "registry_all_forms": {k: gate_all[k] for k in ("n_forms", "status_counts")},
                  "pass": bool(gate_used["pass"])},
        "G3-H": {"notes_total": len(cand_docs), "matched": len(doc_rows), "mismatched": mismatched,
                 "unanswered": unanswered, "all_templates_pass": g_report["all_templates_pass"],
                 "quarantined": g_report["quarantined"],
                 "pass": bool(g_report["all_templates_pass"] and not unanswered and not mismatched)},
        "G-SL": "applied at load to every v1, redo2 and redo3 piece (gsl via haiku_author checks, extract.lint_pack, "
                "extract.lint_clause flags for clauses)",
        "G13_seed": "not run (6.4 step 4)", "G2_G4_G-TW": "not run at pool stage (rows only)"}
    n_bad_files = sum(1 for r in records if r["status"] != "valid")
    if with_redo3:
        r3_sum.update(redo3_summary(r3_recs, ms, mwin, new_win, win_add_probs, state, reg, bk, backups_used, g_ok,
                                    cand_docs, open_skin_slots))
    a = {"v1": v1, "records": records, "stray": stray, "unrecognised": unrecognised, "redo_checks": redo_checks,
         "mp": mp, "mw": mw, "mf": mf, "ms": ms, "mwin": mwin, "new_forms": new_forms, "add_probs": add_probs,
         "new_win": new_win, "reg": reg, "state": state, "used": used, "gate_used": gate_used, "gate_all": gate_all,
         "pools": final, "counts": counts, "short": short, "asked_gaps": gaps, "slot_counts": slot_counts,
         "quarantine": quar, "resolved": resolved, "gates": gates, "blockers": blockers, "problems": problems,
         "vote_counts": vote_counts, "read_batches": read_batches, "g_ok": g_ok, "g_report": g_report,
         "n_bad_files": n_bad_files, "excluded": sorted(excluded), "pend_forms": pend_forms,
         "rej_forms": rej_forms, "unanswered": unanswered, "mismatched": mismatched, "row_of": row_of,
         "redo3": r3_sum, "baseline": None,
         "open_slots": {"packs": sorted(open_pack_slots), "wordings": sorted(open_word_slots),
                        "freeform": sorted(open_doc_slots),
                        "skins": sorted(s_ for sl in open_skin_slots.values() for s_ in sl) if with_redo3 else []}}
    a["ready"] = is_ready(a)
    return a


def redo3_summary(r3_recs, ms, mwin, new_win, win_add_probs, state, reg, bk, backups_used, g_ok, cand_docs,
                  open_skin_slots) -> dict:
    """What the redo3 round gave, for the MANIFEST: per piece kind the answers, what passed, what was placed, what was
    left over and why."""
    pass_skins = [i for i in ms["attempts"] if not ms["attempts"][i]["reasons"]]
    placed = {it.iid: slot for slot, it, _sk in ms["accepted"]}
    return {
        "answer_files": {"total": len(r3_recs), "valid": sum(1 for r in r3_recs if r["status"] == "valid"),
                         "by_kind": dict(Counter(r["kind"] for r in r3_recs))},
        "skins": {"answered": len(ms["attempts"]), "passed_checks": len(pass_skins), "placed": len(placed),
                  "placed_by_register": dict(sorted(Counter(it.meta["register"] for _s, it, _k in ms["accepted"]).items())),
                  "slot_of": dict(sorted(placed.items())),
                  "surplus_not_kept": [{"pid": it.iid, "register": it.meta["register"], "task_id": it.task}
                                       for it in sorted(ms["surplus"], key=lambda c: c.iid)],
                  "failed": {i: v["reasons"] for i, v in sorted(ms["attempts"].items()) if v["reasons"]},
                  "open_slots_before": {r_: len(v) for r_, v in sorted(open_skin_slots.items())},
                  "unplaced_slots": ms["unplaced_slots"]},
        "windows": {"answered": len(mwin["attempts"]), "passed_checks": len(mwin["kept"]),
                    "check_failed": {i: v["reasons"] for i, v in sorted(mwin["attempts"].items()) if v["reasons"]},
                    "form_not_added": [{"pid": it.iid, "reason": e} for it, e in win_add_probs],
                    "forms": {fid: {"pid": p["pid"], "sem": p["sem"], "text": p["text"], "state": state[fid][0],
                                    "detail": state[fid][1], "reads": [[e, s] for e, s in reg.forms[fid].extractions]}
                              for _i, p, fid in new_win},
                    "used": sorted(fid for _i, _p, fid in new_win if state[fid][0] == "used"),
                    "used_by_sem": dict(sorted(Counter(reg.forms[fid].sem_id for _i, _p, fid in new_win
                                                       if state[fid][0] == "used").items()))},
        "g3h_reads": {pid: {"match": g_ok[pid][0], "diffs": g_ok[pid][1]} for pid in sorted(g_ok)
                      if cand_docs.get(pid, {}).get("round") == "redo2"},
        "backup_notes": {"answered": len(bk["attempts"]), "passed_checks": len(bk["passing"]),
                         "check_failed": {i: v["reasons"] for i, v in sorted(bk["attempts"].items()) if v["reasons"]},
                         "used": [{"replaces": pid, "backup": iid} for pid, iid in backups_used],
                         "unused": sorted(i for i in bk["attempts"] if i not in {b for _p, b in backups_used}),
                         "why_unused": "a backup note replaces a note only when the g3h-r1 read dropped that note "
                                       "(mismatch, H47); a missing read leaves the note pending, never replaced"}}


def slot_accounting(v1, final, state, new_forms, mp, mf, row_of, reg, extra_authored=None) -> dict:
    """authored = admitted + pending + quarantined, by slot, for every group (freeze.build's identity, kept in v2). A
    redo3 window clause is a new authored item (extra_authored), not a slot refill."""
    authored = dict(v1["rb"]["authored"])
    for g, n in (extra_authored or {}).items():
        authored[g] += n
    out = {}
    n = len(final["packs"])
    out["packs"] = {"authored": authored["packs"], "admitted": n, "pending": 0, "quarantined": authored["packs"] - n}
    n = len(final["skins"])
    out["skins"] = {"authored": authored["skins"], "admitted": n, "pending": 0, "quarantined": authored["skins"] - n}
    adm_n = len(final["documents"])
    pend = {r.get("slot") or r["pid"] for r in final["documents_pending_g3h"]}
    out["freeform"] = {"authored": authored["freeform"], "admitted": adm_n, "pending": len(pend),
                       "quarantined": authored["freeform"] - adm_n - len(pend)}
    for g in ("wordings", "windows", "comparators"):
        pend = {row_of[f]["pid"] for f in state if row_of[f]["group"] == g and state[f][0] == "unconfirmed"}
        if g == "wordings":
            pend |= {slot for slot, _it, *_r in new_forms}
        out[g] = {"authored": authored[g], "admitted": len(final[g]), "pending": len(pend),
                  "quarantined": authored[g] - len(final[g]) - len(pend)}
    probs = [f"{g}: {d}" for g, d in out.items()
             if d["authored"] != d["admitted"] + d["pending"] + d["quarantined"] or min(d.values()) < 0]
    return {"by_group": out, "problems": probs}


def build_quarantine(v1, out1, mp, mw, mf, add_probs, state, new_forms, doc_quar, reg, row_of, ms=None, mwin=None,
                     win_add_probs=(), bk=None, backups_used=()) -> tuple:
    """(rows, resolved). v1's quarantine rows stay unless a redo piece now fills the slot; new rows record every redo2 / redo3
    attempt that did not end in the pool, every form the H45 reads left out, and every G3-H mismatch."""
    placed_packs = {slot: it.iid for slot, it, _h, _s in mp["accepted"]}
    placed_skins = {slot: it.iid for slot, it, _sk in ms["accepted"]} if ms else {}
    rows, resolved = [], []
    for q in json.loads(json.dumps(out1["quar"])):
        if q["stage"] == "authoring_check" and q["group"] == "packs" and q["pid"] in placed_packs:
            resolved.append({**q, "resolved_by": placed_packs[q["pid"]]})
        elif q["group"] == "skins" and q["pid"] in placed_skins:
            resolved.append({**q, "resolved_by": placed_skins[q["pid"]]})
        else:
            rows.append(q)
    for slot in mp["unplaced_slots"]:
        rows.append({"stage": "redo2", "group": "packs", "pid": slot, "status": "slot_open",
                     "reasons": ["no redo2 replacement or spare passed the checks"]})
    for iid, tries in sorted(mp["attempts"].items()):
        for t in tries:
            if not t["accepted"]:
                rows.append({"stage": "redo2", "group": "packs", "pid": iid, "task_id": t["task"], "slot": t["slot"],
                             "status": "check_failed", "reasons": t["reasons"]})
    for slot, tries in sorted(mw["attempts"].items()):
        for t in tries:
            if not t["accepted"]:
                rows.append({"stage": "redo2", "group": "wordings", "pid": t["iid"], "task_id": t["task"], "slot": slot,
                             "status": "check_failed", "reasons": t["reasons"]})
    for slot, it, fid, q, text, slots, tid, psha in new_forms:
        rows.append({"stage": "G-LEX", "group": "wordings", "pid": it.iid, "task_id": tid, "prompt_sha": psha,
                     "slot": slot, "form_id": fid, "sem_id": L.question_sem(FAMILY, q), "status": reg.status(fid),
                     "text": text, "reasons": [f"{len({e for e, _ in reg.forms[fid].extractions})} of "
                                               f"{reg.forms[fid].required} independent reads: it needs two realistic-fill "
                                               "G-LEX reads (none exist yet); it is not used"]})
    for slot, it, e in add_probs:
        rows.append({"stage": "redo2", "group": "wordings", "pid": it.iid, "task_id": it.task, "slot": slot,
                     "status": "form_rejected", "reasons": [e]})
    for slot, tries in sorted(mf["attempts"].items()):
        for t in tries:
            if not t["accepted"]:
                rows.append({"stage": "redo2", "group": "freeform", "pid": t["iid"], "task_id": t["task"], "slot": slot,
                             "status": "check_failed", "reasons": t["reasons"]})
    if ms:
        for slot in ms["unplaced_slots"]:
            rows.append({"stage": "redo3", "group": "skins", "pid": slot, "status": "slot_open",
                         "reasons": ["no redo3 skin of this register passed the checks"]})
        for iid, t in sorted(ms["attempts"].items()):
            if t["reasons"]:
                rows.append({"stage": "redo3", "group": "skins", "pid": iid, "task_id": t["task"],
                             "status": "check_failed", "reasons": t["reasons"]})
    if mwin:
        for iid, t in sorted(mwin["attempts"].items()):
            if t["reasons"]:
                rows.append({"stage": "redo3", "group": "windows", "pid": iid, "task_id": t["task"],
                             "status": "check_failed", "reasons": t["reasons"]})
        for it, e in win_add_probs:
            rows.append({"stage": "redo3", "group": "windows", "pid": it.iid, "task_id": it.task,
                         "status": "form_rejected", "reasons": [e]})
    if bk:
        for iid, t in sorted(bk["attempts"].items()):
            if t["reasons"]:
                rows.append({"stage": "redo3", "group": "freeform", "pid": iid, "task_id": t["task"],
                             "status": "check_failed", "reasons": t["reasons"]})
    for fid in sorted(state, key=lambda f: (row_of[f]["group"], row_of[f]["pid"])):
        s, why = state[fid]
        if s == "used":
            continue
        p = row_of[fid]
        rows.append({"stage": "G-LEX", "group": p["group"], "pid": p["pid"], "task_id": p["task_id"],
                     "prompt_sha": p["prompt_sha"], "form_id": fid, "sem_id": reg.forms[fid].sem_id, "status": s,
                     "reasons": [why], "reads": [[e, x] for e, x in reg.forms[fid].extractions]})
    rows += doc_quar
    return rows, resolved


# ------------------------------------------------------------------------------------------------ files
def validation_report(a: dict) -> dict:
    recs = a["records"]
    by = Counter((r["round"], r["status"]) for r in recs)
    return {"family": FAMILY, "version": VERSION,
            "contract": "UTF-8 JSON list of objects with exactly qid + " + " | ".join(
                f"{k}: {'+'.join(v)}" for k, v in CONTRACT_KEYS.items()) +
                        "; qids from the task's own chunk, none repeated, every item answered once; a G-LEX meaning "
                        "copied exactly from the item's choices; a file is rejected whole and never edited",
            "excluded_tasks": a["excluded"],
            "summary": {f"{r}/{s}": n for (r, s), n in sorted(by.items())},
            "files_total": len(recs), "files_valid": sum(1 for r in recs if r["status"] == "valid"),
            "files_not_valid": [r for r in recs if r["status"] != "valid"],
            "stray_files_not_used": a["stray"], "unrecognised_round_dirs": a["unrecognised"], "files": recs}


def tally_reads(a: dict) -> dict:
    out = {}
    for rb in a["read_batches"]:
        label = rb.name if rb.round == "v1" else f"{rb.round}:{rb.name}"
        out[label] = {"round": rb.round, "kind": rb.kind, "batch_id": rb.batch_id, "prompt_sha": rb.prompt_sha,
                      "n_items": len(rb.key), "answers_used": len(rb.answers),
                      "tasks": {tid: {"n": len(items), "answer_sha256": rb.used_tasks.get(tid)}
                                for tid, _p, items in rb.tasks}}
    return out


def remaining_work(a: dict) -> list:
    c = a["counts"]
    out = []
    short_skins = [s for s in a["short"] if s.startswith("skins ")]
    if short_skins:
        out.append("skins: another authoring round for the skin slots that are still open: " + "; ".join(short_skins))
    short_win = [s for s in a["short"] if s.startswith("window ")]
    if short_win:
        out.append("windows: more window clauses and 3 + 3 G-LEX reads for them: " + "; ".join(short_win))
    if a["unanswered"]:
        out.append(f"documents: one g3h-r1 read for each unread note: {a['unanswered']}")
    if a["mismatched"]:
        out.append(f"documents: G3-H mismatches dropped: {a['mismatched']}")
    if a["mp"]["unplaced_slots"]:
        out.append(f"packs: slots with no passing redo2 pack: {a['mp']['unplaced_slots']}")
    if a["ms"] and a["ms"]["unplaced_slots"]:
        out.append(f"skins: slots with no passing redo3 skin: {a['ms']['unplaced_slots']}")
    if a["new_forms"]:
        out.append(f"{len(a['new_forms'])} redo2 wording(s) wait for two realistic-fill G-LEX reads (not needed for any "
                   "G0 minimum): " + ", ".join(f[2] for f in a["new_forms"]))
    if a["pend_forms"]:
        out.append(f"{len(a['pend_forms'])} admitted form(s) lack a G-LEX or confirmation read and stay unused")
    if a["rej_forms"]:
        out.append(f"{len(a['rej_forms'])} form(s) were rejected by a read: {a['rej_forms']}")
    for p in a["problems"]:
        out.append(f"note: {p}")
    return out


def manifest_obj(a: dict, files: dict, previous: dict | None) -> dict:
    v1 = a["v1"]
    c = a["counts"]
    g0_sha = sha_file(G0)
    prereg = sha_file(paths.PREREG)
    spec = paths.LEAN / "teach1" / "C2_DATA_SPEC.md"
    spec_sha = sha_file(spec)
    if a["ready"]:
        status = "READY: every G0 minimum met and the G-LEX gate passes. G13-seed and row generation not run."
    elif a["blockers"]:
        status = "BLOCKED: " + "; ".join(a["blockers"][:3])
    else:
        status = "SHORT: " + "; ".join(a["short"]) + ". Targets are not lowered. G13-seed and row generation not run."
    qc = Counter((q["stage"], q.get("status", "")) for q in a["quarantine"])
    added = {"packs": sorted(r["pid"] for r in a["pools"]["packs"] if r.get("round") == "redo2"),
             "wordings_pending_reads": sorted(f[2] for f in a["new_forms"]),
             "documents_admitted": sorted(r["pid"] for r in a["pools"]["documents"] if r.get("round") == "redo2"),
             "documents_pending_g3h": sorted(r["pid"] for r in a["pools"]["documents_pending_g3h"]),
             "skins": sorted(r["pid"] for r in a["pools"]["skins"] if r.get("round") == "redo3"),
             "windows": sorted(r["pid"] for r in a["pools"]["windows"] if r.get("round") == "redo3"),
             "documents_from_backup_notes": sorted(r["pid"] for r in a["pools"]["documents_pending_g3h"]
                                                   if r.get("round") == "redo3")}
    return {
        "family": FAMILY, "freeze": "v2", "version": VERSION, "ready": a["ready"], "status": status,
        "supersedes": {"path": "families/T01/pools/manifest.json", "version": v1["integrity"]["version"],
                       "sha256": v1["integrity"]["manifest_sha256"]},
        "replaces_previous_v2": previous,
        "v1_integrity": {"reproduced_by_rebuild": v1["integrity"]["ok"], "problems": v1["integrity"]["problems"]},
        "bindings": {"prereg_final_sha256": prereg,
                     "prereg_final_sha256_in_v1_manifest": v1["integrity"]["manifest"]["bindings"]["prereg_final_sha256"],
                     "a38_frozen": paths.a38_frozen(), "c2_data_spec_sha256": spec_sha,
                     "c2_data_spec_matches_a37": spec_sha == F1.C2_SPEC_SHA_A37,
                     "g0_spec_sha256": g0_sha, "g0_spec_matches_plugin": g0_sha == P.T01.G0_SHA256,
                     "g0_version": "v3 (H42-H47)"},
        "excluded_tasks_audit_failed": a["excluded"],
        "audit_note": ("Answer files are used unless their task id is on --exclude-task; this run excluded "
                       f"{a['excluded'] or 'none'}. The auditor (c2_kit.audit) reads agent transcripts, which this script "
                       "never opens; the exclusion list is the orchestrator's."),
        "answer_files": {"total": len(a["records"]), "by_round_status": validation_report(a)["summary"],
                         "not_valid": [{"task_id": r["task_id"], "round": r["round"], "status": r["status"]}
                                       for r in a["records"] if r["status"] != "valid"],
                         "detail": "VALIDATION_REPORT.json"},
        "rounds_ingested": ["v1 author", "v1 extract", "redo", "redo2"] + (["redo3", "redo3/reads"] if a["redo3"]["active"]
                                                                          else []),
        "redo3_baseline": a["baseline"], "redo3": a["redo3"],
        "redo": a["redo_checks"], "reads": tally_reads(a), "answer_reads": a["vote_counts"],
        "gates": a["gates"], "counts": c, "slot_accounting": a["slot_counts"]["by_group"],
        "targets_g0": TARGET | {"wordings_per_qform": PER_FORM_ASKED, "window_sems": list(WINDOW_SEMS),
                                "comparator_sems": list(COMPARATOR_SEMS)},
        "targets_note": "freeze.TARGET is imported unchanged. Per-form wording counts are asked counts (H42); the minimum "
                        "is wordings_min_admitted.",
        "shortfalls_vs_g0": a["short"], "asked_count_gaps_informational": a["asked_gaps"],
        "remaining_work": remaining_work(a),
        "problems": {"blocking": a["blockers"], "notes": a["problems"]},
        "added_in_v2": added, "resolved_from_v1_quarantine": a["resolved"],
        "quarantine_rows": len(a["quarantine"]),
        "quarantine_by_stage_status": {f"{s}/{t}": n for (s, t), n in sorted(qc.items())},
        "load": "Nothing reads pools_v2/ by itself. Use freeze_v2.load_pools() / make_ctx(), or (owner ruling) move pools/ "
                "to pools_v1/ and pools_v2/ to pools/ (g13_c2.py reads families/T01/pools/). Family code reads no pool path. "
                "pools_v2_prev/ is the earlier SHORT freeze (v1 + redo2) that haiku/redo3 was authored against: keep it, "
                "the redo3 builders and their rebuild check read it.",
        "sha256": {name: sha_bytes(text.encode("utf-8")) for name, text in sorted(files.items())},
        "note_manifest": "sha256 of every other file in pools_v2/ (this file is not hashed)"}


def build_files(a: dict, previous: dict | None = None) -> dict:
    files = data_files(a)
    files["VALIDATION_REPORT.json"] = dump(validation_report(a))
    files["MANIFEST.json"] = dump(manifest_obj(a, files, previous))
    return files


def previous_v2() -> dict | None:
    """The freeze this one replaces: the live pools_v2/ if there is one, else pools_v2_prev/ (moved aside before)."""
    for d in (POOLS_V2, POOLS_V2_PREV):
        info = _manifest_info(d)
        if info is not None:
            return info
    return None


def run(write: bool, rebuild_check: bool = True, exclude=()) -> dict:
    live = _manifest_info(POOLS_V2)
    prev = previous_v2()
    if write and live and live["ready"] is not False:
        raise SystemExit("pools_v2/MANIFEST.json exists and is not a SHORT freeze: refusing to re-freeze")
    if write and live and (REDO3 / "TASKS.json").is_file() and not (POOLS_V2_PREV / "MANIFEST.json").is_file():
        raise SystemExit("haiku/redo3 was authored against the current pools_v2/ and its builders read it: move it aside "
                         "first (mv families/T01/pools_v2 families/T01/pools_v2_prev), then freeze again")
    a = assemble(rebuild_check=rebuild_check, exclude=exclude)
    if write and a["blockers"]:
        raise SystemExit("blocking problems, nothing written: " + "; ".join(a["blockers"][:4]))
    files = build_files(a, prev)
    if write:
        paths.write_files(POOLS_V2, files)
    man = json.loads(files["MANIFEST.json"])
    c = a["counts"]
    return {"status": man["status"], "ready": a["ready"], "written": write, "shortfalls": a["short"],
            "asked_count_gaps_informational": a["asked_gaps"], "blockers": a["blockers"],
            "remaining_work": man["remaining_work"], "excluded_tasks": a["excluded"],
            "answer_files": man["answer_files"]["by_round_status"], "not_valid_files": man["answer_files"]["not_valid"],
            "redo": a["redo_checks"], "redo3_baseline": a["baseline"], "redo3": a["redo3"],
            "added_in_v2": man["added_in_v2"], "counts": c,
            "slot_accounting": a["slot_counts"]["by_group"], "gates": a["gates"], "answer_reads": a["vote_counts"],
            "quarantine_rows": len(a["quarantine"]), "quarantine_by_stage_status": man["quarantine_by_stage_status"],
            "problems": a["problems"], "stray_files": a["stray"], "files": sorted(files)}


# ------------------------------------------------------------------------------------------------ loading pools_v2
def load_pools(root: Path = POOLS_V2) -> dict:
    """The pool files of a freeze as objects: {"skins": {id: Skin}, "documents": {id: Skin}, "wordings": [row],
    "windows": [row], "comparators": [row], "packs": [row], "lexicon": LexiconRegistry holding ONLY the forms the pool
    uses (so no unused form can be offered), "manifest": dict}. Skins are rebuilt the way haiku_author.check_skin /
    check_freeform build them."""
    root = Path(root)

    def rows(name):
        return [json.loads(x) for x in safe_read(root / name).decode("utf-8").splitlines() if x.strip()]
    skins = {}
    for r in rows("skins.jsonl"):
        sid = f"T01-SK-{r['pid'].split('.', 2)[2]}"
        skins[sid] = K.make_skin(sid, FAMILY, r["text"], dict(r["decl"]), register=r["register"], escape=r["escape"],
                                 held_out=r["held_out"], haiku_task_id=r["task_id"], haiku_prompt_sha=r["prompt_sha"])
    docs = {}
    for r in rows("documents.jsonl"):
        sid = f"T01-MF-{r['pid'].rsplit('.', 1)[1]}"
        docs[sid] = K.make_skin(sid, FAMILY, r["text"], dict(A.NARR), register=r["register"], author_mode="F",
                                brief=dict(r["facts"]), haiku_task_id=r["task_id"], haiku_prompt_sha=r["prompt_sha"])
    full = read_json(root / "lexicon_registry.json")
    used = {r["form_id"] for g in ("wordings", "windows", "comparators") for r in rows(f"{g}.jsonl")}
    reg = L.LexiconRegistry(full["name"])
    for s in full["sems"]:
        reg.declare(s["sem_id"], s["kind"], s["meaning"])
    for x in full["forms"]:
        if x["form_id"] not in used:
            continue
        f = reg.add(x["text"], x["sem_id"], slots=x["slots"], source=x["source"], family=x["family"],
                    haiku_task_id=x["haiku_task_id"], haiku_prompt_sha=x["haiku_prompt_sha"], held_out=x["held_out"])
        f.extractions = [tuple(e) for e in x["extractions"]]
    reg.unit_test_all()
    return {"skins": skins, "documents": docs, "wordings": rows("wordings.jsonl"), "windows": rows("windows.jsonl"),
            "comparators": rows("comparators.jsonl"), "packs": rows("packs.jsonl"), "lexicon": reg,
            "manifest": read_json(root / "MANIFEST.json")}


def make_ctx(pools: dict | None = None):
    """The generator's KitCtx for a pool set (default pools_v2/): the narrative skins, the Mode F notes and one wording
    skin per used wording (kind "wording", lexicon_ids = its form id), plus the used-forms registry. Same shape as
    fixtures.ctx(); an unused, pending or rejected form is never offered."""
    from c2_kit.plugin import KitCtx
    pools = pools or load_pools()
    sk = {**pools["skins"], **pools["documents"]}
    for w in pools["wordings"]:
        sid = f"T01-WD-{w['form_id']}"
        sk[sid] = K.make_skin(sid, FAMILY, w["text"], dict(w["slots"]), kind="wording", register="question",
                              qform=w["qform"], held_out=w["held_out"], lexicon_ids=(w["form_id"],),
                              haiku_task_id=w["task_id"], haiku_prompt_sha=w["prompt_sha"])
    return KitCtx(skins=sk, lexicon=pools["lexicon"])


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=("check", "freeze"))
    ap.add_argument("--no-rebuild-check", action="store_true", help="skip the byte-for-byte redo2 rebuild (about 40 s)")
    ap.add_argument("--exclude-task", action="append", default=[], help="a task id whose audit failed (repeatable)")
    a = ap.parse_args(argv)
    out = run(write=(a.cmd == "freeze"), rebuild_check=not a.no_rebuild_check, exclude=tuple(a.exclude_task))
    print(json.dumps(out, indent=1, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())

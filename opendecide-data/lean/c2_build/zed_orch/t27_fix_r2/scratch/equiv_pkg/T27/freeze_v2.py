"""c2_build/families/T27/freeze_v2.py: the T27 pool freeze (pools_v2/) over every Haiku round: author, redo, redo2, redo3
(G0_SPEC.md v1.1 sections 6 and 8; C2_DATA_SPEC 6.3 G-SL / G-LEX / G3-H; PREREG A37 (b), A38).

Why a new script. T27 has no freeze at all (no pools/, no MANIFEST): extract_check.py only validates and records the
26 first-pass G-LEX reads, redo2.py only lints the supplement and plans its two reads, and no loader merges them. The
round-1 redo answers (haiku/redo/answers) had been copied by hand into haiku/extract/answers, and the redo2
supplement (45 support_chat skins, 12 yn_dneg_beyond wordings) had no ingest path. Nothing existing is edited: this
file reads authoring.py / extract_check.py / glex_build.py / redo2.py / vocab.py / plugin.py and writes only NEW files
(pools_v2/ on `freeze`, haiku/redo2/extract/ on `reads`). pools_v2.py is the matching loader for the generator.

What a run does (every write goes through the kit's guarded writers, after A38 only):
  1. Validates EVERY answer file of EVERY round against its contract (never edits one; a rejected file or item is
     treated as unanswered, never as a vote): author, redo2 (authoring), extract (first-pass G-LEX reads), redo
     (re-dispatch of the same 26 reads), the superseded first-attempt files (informational: expected malformed) and
     redo2/extract (the supplement reads, once their tasks exist and are answered).
       author kinds   one JSON object, keys = exactly the task's qids, each value an array; skins [[line, ...], ...],
                      packs [{"setting", "names"}, ...], everything else [str, ...]; an item whose value breaks the
                      shape is rejected alone; a count different from the brief is a note, not a reject
       extract_lex    one JSON object, keys = exactly the qids, every value a meaning copied from the task's closed
                      list; any break rejects the whole file (extract_check.judge, same rule)
  2. Rebuilds the pipeline from the validated answers only: author lint (authoring.load), the redo2 lint and merge
     (redo2.load), the lexicon registry (authoring.registry) and the 26 first-pass read batches, which must be byte for
     byte the files on disk (extract_check.files_check); a mismatch records no vote at all.
  3. Records the votes exactly per the kit (lexicon.record_extraction, one extractor id per read task): 2 independent
     extractors that agree admit a form (3 for kinds precedence and window; T27 has none), one disagreement rejects it
     for good. A task read twice (haiku/extract and haiku/redo hold the same task) is ONE read: two valid copies must
     be equal, otherwise neither is used. The supplement wordings get their own 2 reads (redo2.glex_plan); controls
     in those reads are never recorded. G3-H does not apply (Mode T only, G0 S18).
  4. Applies every G0 minimum (authoring.shortfall over the ADMITTED pieces, 148 rows) plus the pool checks below,
     never lowered, and freezes pools_v2/ with MANIFEST.json: sha256 per file, counts, all targets, shortfalls,
     validation, pending reads, how to load. READY only when every G0 minimum is met, the G-LEX gate passes over every
     form the pools use, every check holds and no answer used was rejected.

redo3 (haiku/redo3/, STAGE_A3_REPORT shortfall "yn_dneg_beyond 0 admitted, minimum 2"): it holds (a) the two supplement
G-LEX reads of haiku/redo2/extract/ re-issued with the same qids, prompt and closed list (only the toy example, the
header and the paths differ), and (b) one new authoring task of 3 yn_dneg_beyond wordings. (a) is the SAME read as the
unanswered redo2/extract task: a valid copy in either folder is that read's one vote (two valid copies must be equal,
otherwise neither is used; pick_extract). (b) goes through the same lint as redo2 (authoring.lint_piece, redo2.lint_dneg,
redo2.merge against everything kept so far); a kept redo3 wording is a form with NO G-LEX reads, so it stays pending
(quarantine.json, outside the pools) until two reads name it. Provenance checks: the redo3 read task files match the
redo2/extract rebuild from "THE TASK PROMPT AND THE CLOSED LIST" on, and the redo3 authoring chunk, manifest sha and
prompt sha match the redo2 brief for 3 wordings.

Extra pool checks (added by this script, none lowers a G0 number): a register holds <= 15% of the training L1 / L2
skins (G0 section 6 "register <= 15% of rows", measured on the pool); every question form keeps >= 1 training wording
after the seeded 15% held-out split (the generator cannot render a training row without one).

No label is set anywhere: golds come only from solver A and solver B (A37 b); Haiku output can only admit or drop.

  ../../.venv/bin/python -m families.T27.freeze_v2 check [--fast]   (from lean/c2_build; in memory; --fast reuses linted.json)
  ../../.venv/bin/python -m families.T27.freeze_v2 reads            (writes haiku/redo2/extract/: the supplement read tasks;
                                                                     refused once they exist)
  ../../.venv/bin/python -m families.T27.freeze_v2 freeze           (writes pools_v2/, READY or SHORT)
  --ignore <task id or answer path>   (repeatable) treat that answer as failed-audit: rejected, never a vote
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from types import SimpleNamespace

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, paths  # noqa: E402
from c2_kit.lexicon import LexiconRegistry, question_sem  # noqa: E402
from families.T27 import authoring as A  # noqa: E402
from families.T27 import extract_check as E  # noqa: E402
from families.T27 import glex_build as G  # noqa: E402
from families.T27 import pools_v2 as PV  # noqa: E402
from families.T27 import redo2 as R  # noqa: E402
from families.T27 import vocab as V  # noqa: E402
from families.T27.plugin import T27Plugin  # noqa: E402

FAMILY = V.FAMILY
VERSION = "freeze-v2"
POOLS_V2 = PV.POOLS_V2
HAIKU = HERE / "haiku"
AUTHOR = HAIKU / "author"
EXTRACT = HAIKU / "extract"
REDO = HAIKU / "redo"
REDO2 = HAIKU / "redo2"
R2X = REDO2 / "extract"
REDO3 = HAIKU / "redo3"
SUPERSEDED = EXTRACT / "answers_superseded_first_attempt"
G0 = HERE / "G0_SPEC.md"
MAX_REGISTER_SHARE = 0.15            # G0 section 6: a register <= 15% of rows (pool-level measure, training L1 + L2)
MIN_TRAINING_WORDINGS = 1            # per question form, after the held-out split
LEX_POOLS = R.LEX_POOLS


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_text(t: str) -> str:
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def rel(p: Path) -> str:
    try:
        return Path(p).resolve().relative_to(HERE).as_posix()
    except ValueError:
        return str(p)


def canon(obj) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False)


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


def strict_loads(data: bytes):
    """JSON with no duplicate keys and no NaN / Infinity; a BOM or stray text fails like any other syntax error."""
    return json.loads(data.decode("utf-8"), object_pairs_hook=_no_dup_pairs, parse_constant=_no_const)


@dataclass
class ChunkDef:
    """What one Haiku task gave the agent: its qids and (author) what each item's value must be."""
    task_id: str
    kind: str                                   # author_* | extract_lex
    qids: list
    internal: dict = field(default_factory=dict)    # qid -> internal id (author) / form id (extract)
    expect_n: dict = field(default_factory=dict)    # qid -> number of pieces the brief asks (author)
    lex_kind: str = ""                          # extract_lex: deontic | other | question (its closed list)


def _batch_id(t: dict) -> str:
    """The batch id of a TASKS.json authoring entry: `batch_id` (author, redo2) or the stem of `key_file` (redo3)."""
    return t["batch_id"] if "batch_id" in t else Path(t["key_file"]).stem


def author_defs(root: Path) -> dict:
    """{task_id: ChunkDef} for an authoring round (haiku/author, haiku/redo2 or haiku/redo3), from TASKS.json, chunks/
    and key/. Entries whose kind is not author_* (the G-LEX reads that redo3/TASKS.json also lists) are skipped."""
    tasks = json.loads((root / "TASKS.json").read_text(encoding="utf-8"))["tasks"]
    out = {}
    for t in tasks:
        if not str(t.get("kind", "")).startswith("author_"):
            continue
        tid = t["task_id"]
        chunk = json.loads((root / "chunks" / f"{tid}.json").read_text(encoding="utf-8"))
        key = json.loads((root / "key" / f"{_batch_id(t)}.json").read_text(encoding="utf-8"))["key"]
        qids = [i["qid"] for i in chunk["items"]]
        expect = {}
        for it in chunk["items"]:
            brief = " ".join(it["brief"]) if isinstance(it["brief"], list) else str(it["brief"])
            m = re.search(r"JSON array of (\d+)", brief) or re.search(r"ITEM: write (\d+)", brief)
            expect[it["qid"]] = int(m.group(1)) if m else None
        out[tid] = ChunkDef(tid, chunk["kind"], qids, {q: key[q] for q in qids}, expect)    # the chunk's kind: redo3's
    return out                                                                       # TASKS.json kind is a description


def extract_defs(root: Path) -> dict:
    """{task_id: ChunkDef} for the G-LEX read tasks of `root` (haiku/extract), from TASKS.json, chunks/ and key/."""
    tasks = json.loads((root / "TASKS.json").read_text(encoding="utf-8"))["tasks"]
    out = {}
    for t in tasks:
        tid = t["task_id"]
        chunk = json.loads((root / "chunks" / f"{tid}.json").read_text(encoding="utf-8"))
        key = json.loads((root / "key" / f"{t['batch_id']}.json").read_text(encoding="utf-8"))["key"]
        qids = [i["qid"] for i in chunk["items"]]
        out[tid] = ChunkDef(tid, "extract_lex", qids, {q: key[q] for q in qids}, {}, t["kind"])
    return out


def defs_from_batches(batches: list) -> dict:
    """ChunkDefs for G-LEX read batches rebuilt in memory: [(read, TaskBatch)] of the question kind."""
    out = {}
    for _read, b in batches:
        tid = b.chunks[0]["task_id"]
        out[tid] = ChunkDef(tid, "extract_lex", [i["qid"] for c in b.chunks for i in c["items"]], dict(b.key), {},
                            "question")
    return out


def closed_lists() -> dict:
    """{lexicon kind: frozenset of the closed meaning list} (declared sems only; no forms needed)."""
    reg = LexiconRegistry(FAMILY)
    for sem, kind, meaning in V.sems():
        reg.declare(sem, kind, meaning)
    for q, meaning in V.QUESTION_MEANINGS.items():
        reg.declare(question_sem(FAMILY, q), "question", meaning)
    return {k: frozenset(E.closed_list(reg, k)) for k in ("deontic", "other", "question")}


def item_shape_problems(internal: str, value) -> list:
    """Why one authoring item's value breaks the answer contract (empty list: it holds)."""
    head = internal.split("|")[0]
    if not isinstance(value, list):
        return ["value is not a JSON array"]
    if not value:
        return ["empty array"]
    bad = []
    for i, x in enumerate(value):
        if head == "skin":
            ok = isinstance(x, list) and bool(x) and all(isinstance(s, str) for s in x)
        elif head == "pack":
            ok = (isinstance(x, dict) and set(x) == {"setting", "names"} and isinstance(x["setting"], str)
                  and isinstance(x["names"], list) and bool(x["names"]) and all(isinstance(n, str) for n in x["names"]))
        else:
            ok = isinstance(x, str)
        if not ok:
            bad.append(i)
    return [f"{len(bad)} element(s) break the answer shape for {head!r} (first: #{bad[0]})"] if bad else []


def validate_answer(data: bytes, cd: ChunkDef, closed: frozenset | None = None) -> dict:
    """The verdict on one answer file: {sha256, ok, reasons, item_rejects, notes, accepted}. `accepted` is the object a
    rebuild may use (author: without the rejected items; extract: the whole object), None when the file is rejected."""
    out = {"sha256": sha_bytes(data), "ok": False, "reasons": [], "item_rejects": {}, "notes": [], "accepted": None}
    try:
        raw = strict_loads(data)
    except (UnicodeDecodeError, json.JSONDecodeError, _Strict) as e:
        out["reasons"].append(f"not strict JSON ({type(e).__name__}: {str(e)[:80]})")
        return out
    if not isinstance(raw, dict):
        out["reasons"].append("answer is not one JSON object keyed by qid")
        return out
    extra = sorted(set(raw) - set(cd.qids))
    missing = [q for q in cd.qids if q not in raw]
    if extra:
        out["reasons"].append(f"{len(extra)} key(s) that are not qids of this task (first: {extra[0]!r})")
    if missing:
        out["reasons"].append(f"{len(missing)} of {len(cd.qids)} qid(s) unanswered")
    if out["reasons"]:
        return out
    if cd.kind == "extract_lex":
        off = [q for q in cd.qids if not isinstance(raw[q], str) or raw[q] not in (closed or ())]
        if off:
            out["reasons"].append(f"{len(off)} value(s) are not a meaning from the closed list of kind "
                                  f"{cd.lex_kind!r}")
            return out
        out["ok"], out["accepted"] = True, raw
        return out
    accepted = {}
    for q in cd.qids:
        why = item_shape_problems(cd.internal[q], raw[q])
        if why:
            out["item_rejects"][q] = why
            continue
        accepted[q] = raw[q]
        n = cd.expect_n.get(q)
        if n is not None and len(raw[q]) != n:
            out["notes"].append(f"{cd.internal[q]}: {len(raw[q])} piece(s), the brief asks {n}")
    if not accepted:
        out["reasons"].append("no item satisfies its contract")
        return out
    out["ok"], out["accepted"] = True, accepted
    return out


def _is_ignored(path: Path, ignored: set) -> bool:
    p = str(Path(path).resolve())
    return p in ignored or Path(path).stem in ignored


def validate_round(name: str, defs: dict, answers_dir: Path, *, closed_of=None, ignored: set = frozenset(),
                   informational: bool = False, also: frozenset = frozenset()) -> dict:
    """Validate every answer file of one round. A file is never edited; ignored (failed-audit) ones are rejected.
    `also`: task ids that share this answers folder but are validated by another round (not stray here)."""
    files, missing = {}, []
    for tid, cd in sorted(defs.items()):
        p = Path(answers_dir) / f"{tid}.json"
        if not p.is_file():
            missing.append(tid)
            continue
        r = validate_answer(p.read_bytes(), cd, closed_of(cd) if closed_of else None)
        if _is_ignored(p, ignored):
            r.update(ok=False, accepted=None)
            r["reasons"].append("answer ignored: the orchestrator reports its file-access audit failed")
        files[tid] = r
    stray = []
    if Path(answers_dir).is_dir():
        stray = sorted(f.name for f in Path(answers_dir).glob("*.json") if f.stem not in defs and f.stem not in also)
    return {"name": name, "dir": rel(answers_dir), "informational": informational, "tasks": len(defs), "files": files,
            "missing": missing, "stray": stray, "rejected": sorted(t for t, r in files.items() if not r["ok"]),
            "item_rejects": {t: r["item_rejects"] for t, r in files.items() if r["item_rejects"]}}


def accepted(round_rep: dict) -> dict:
    return {t: r["accepted"] for t, r in round_rep["files"].items() if r["ok"]}


def slim(round_rep: dict) -> dict:
    """The round report without the accepted payloads (for the manifest and the validation report)."""
    out = {k: v for k, v in round_rep.items() if k != "files"}
    out["files"] = {t: {k: v for k, v in r.items() if k != "accepted"} for t, r in round_rep["files"].items()}
    out["accepted_files"] = sum(1 for r in round_rep["files"].values() if r["ok"])
    return out


def pick_extract(rep_extract: dict, rep_redo: dict, names: tuple = ("extract", "redo")) -> tuple:
    """One read per G-LEX task. haiku/extract and haiku/redo hold answers to the SAME task, so they are one read, never
    two votes: a valid extract copy is used (a valid redo copy must equal it); the redo copy is used when the extract
    copy is rejected; two valid copies that differ are a conflict and neither is used. `names`: the two copies' labels
    (the supplement reads use ("redo2/extract", "redo3")).
    Returns ({task_id: {source, answer, sha256}}, notes)."""
    na, nb = names
    picks, notes = {}, {}
    for tid in sorted(set(rep_extract["files"]) | set(rep_redo["files"]) | set(rep_extract["missing"])
                      | set(rep_redo["missing"])):
        a, b = rep_extract["files"].get(tid), rep_redo["files"].get(tid)
        oka, okb = bool(a and a["ok"]), bool(b and b["ok"])
        if oka and okb:
            if a["accepted"] == b["accepted"]:
                picks[tid] = {"source": na, "answer": a["accepted"], "sha256": a["sha256"]}
                notes[tid] = (f"{na} copy and {nb} copy are byte-identical" if a["sha256"] == b["sha256"]
                              else f"{na} copy and {nb} copy are the same JSON (bytes differ)")
            else:
                notes[tid] = f"CONFLICT: haiku/{na} and haiku/{nb} hold two valid answers that differ; neither used"
        elif oka:
            picks[tid] = {"source": na, "answer": a["accepted"], "sha256": a["sha256"]}
            notes[tid] = f"{na} copy only" + ("" if not b else f" ({nb} copy rejected)")
        elif okb:
            picks[tid] = {"source": nb, "answer": b["accepted"], "sha256": b["sha256"]}
            notes[tid] = f"{nb} copy only" + ("" if not a else f" ({na} copy rejected)")
        else:
            notes[tid] = "no valid answer"
    return picks, notes


# ======================================================================================================= 2. rebuild

def extraction_batches(reg, fids: list) -> list:
    """The 26 first-pass G-LEX read batches [(read, kind, group, TaskBatch)]: glex_build.plan over exactly `fids`
    (the forms of the first-pass kept pools; a larger registry adds none)."""
    out = []
    for read in G.READS:
        for kind in G.KIND_ORDER:
            ids = [f for f in fids if reg.forms[f].kind == kind]
            meanings = sorted(s.meaning for s in reg.sems.values() if s.kind == kind)
            for g in range(0, len(ids), G.GROUP):
                part = ids[g:g + G.GROUP]
                seed = G.group_seed(read, kind, g // G.GROUP)
                order = sorted(meanings, key=lambda m: hashlib.sha256(f"{seed}|{m}".encode()).hexdigest())
                items = [(fid, {"text": it["text"]}) for fid, it in A.lex_items(reg, part, seed=seed)]
                b = chunker.make_batch("extract_lex", FAMILY, items, seed=seed, prompt=G.group_prompt(order),
                                       max_items=G.GROUP)
                if len(b.chunks) != 1:
                    raise chunker.ChunkError(f"{seed}: one chunk per group")
                out.append((read, kind, g // G.GROUP, b))
    return out


def record_reads(reg, reads: list) -> list:
    """Record the votes. reads: [{extractor, task_id, read, kind, key {qid: form id}, answer {qid: meaning} | None,
    only: set of form ids | None, source}]. One extractor id per read task. An unanswered read records nothing; `only`
    keeps control items out of the registry. Returns one log row per read."""
    log = []
    for rd in reads:
        row = {k: rd[k] for k in ("extractor", "task_id", "read", "kind", "source")}
        if rd["answer"] is None:
            log.append({**row, "status": "unanswered", "recorded": 0})
            continue
        n = 0
        for qid, fid in sorted(rd["key"].items()):
            if rd["only"] is not None and fid not in rd["only"]:
                continue
            reg.record_extraction(fid, rd["extractor"], reg.meaning_to_sem(rd["kind"], rd["answer"][qid]))
            n += 1
        log.append({**row, "status": "recorded", "recorded": n})
    return log


def r2_file_problems(plan2: dict, root: Path = R2X) -> list:
    """The supplement read tasks on disk must be the files the rebuild writes (none on disk: nothing to compare)."""
    root = Path(root)
    if not (root / "TASKS.json").is_file():
        return []
    probs = []
    built = {}
    for read, b in plan2["batches"]:
        tid = b.chunks[0]["task_id"]
        files = dict(b.files())
        files[f"{tid}.txt"] = R.glex_txt(b, root)
        built[tid] = read
        for name, text in sorted(files.items()):
            f = root / name
            if not f.is_file() or f.read_text(encoding="utf-8") != text:
                probs.append(f"{b.batch_id}: {name} differs from the rebuilt file")
    listed = {t["task_id"] for t in json.loads((root / "TASKS.json").read_text(encoding="utf-8"))["tasks"]}
    if listed != set(built):
        probs.append(f"redo2/extract/TASKS.json lists {sorted(listed)}, the rebuild has {sorted(built)}")
    return probs


_READ_TAIL = "THE TASK PROMPT AND THE CLOSED LIST  (verbatim"       # the heading line (the "what to do" text names it too)


def redo3_author_batches(root: Path = REDO3) -> list:
    """[(task def, TaskBatch)] for the authoring tasks of redo3/TASKS.json, loaded from the chunk / key / manifest /
    prompt files on disk in the shape authoring.load(batches=...) takes. [] when the folder has no such task."""
    root = Path(root)
    out = []
    for t in json.loads((root / "TASKS.json").read_text(encoding="utf-8"))["tasks"]:
        if not str(t.get("kind", "")).startswith("author_"):
            continue
        tid, bid = t["task_id"], _batch_id(t)
        chunk = json.loads((root / "chunks" / f"{tid}.json").read_text(encoding="utf-8"))
        key = json.loads((root / "key" / f"{bid}.json").read_text(encoding="utf-8"))["key"]
        man = json.loads((root / "manifest" / f"{bid}.json").read_text(encoding="utf-8"))
        prompt = (root / "prompts" / f"{t['prompt_sha'][:16]}.txt").read_text(encoding="utf-8")
        b = chunker.TaskBatch(chunk["kind"], FAMILY, bid, prompt, t["prompt_sha"], man["seed"])
        b.chunks, b.key = [chunk], dict(key)
        b.task_of = {q: tid for q in key}
        out.append(({"name": t["name"], "pool": chunk["kind"].split("_", 1)[1], "kind": chunk["kind"]}, b))
    return out


def redo3_author_problems(batches: list, root: Path = REDO3) -> list:
    """Provenance of the redo3 authoring tasks: chunk, manifest and prompt agree, and each item is the redo2
    yn_dneg_beyond brief (redo2._dneg_item) for the number of wordings it asks, naming its own answers/<task id>.json."""
    root = Path(root)
    probs = []
    for _td, b in batches:
        c = b.chunks[0]
        tid = c["task_id"]
        man = json.loads((root / "manifest" / f"{b.batch_id}.json").read_text(encoding="utf-8"))
        if {x["task_id"]: x["sha256"] for x in man["tasks"]}.get(tid) != chunker.sha(
                json.dumps(c, sort_keys=True, ensure_ascii=False)):
            probs.append(f"{tid}: the chunk differs from the sha256 in its manifest")
        if chunker.sha(b.prompt) != b.prompt_sha or c["prompt_sha"] != b.prompt_sha or man["prompt_sha"] != b.prompt_sha:
            probs.append(f"{tid}: chunk, manifest and prompt file disagree on the prompt sha256")
        for it in c["items"]:
            text = " ".join(it["brief"])
            n = re.search(r"write (\d+) different questions", text)
            ans = re.search(r"to the file (\S+\.json) with the Write tool", text)
            if b.key.get(it["qid"]) != "wording|yn_dneg_beyond" or not n or not ans:
                probs.append(f"{tid}: item {it['qid']} is not a yn_dneg_beyond wording brief")
            elif Path(ans.group(1)).name != f"{tid}.json" or Path(ans.group(1)).parent.name != "answers":
                probs.append(f"{tid}: item {it['qid']} names another answer file ({ans.group(1)})")
            elif {k: v for k, v in it.items() if k != "qid"} != A._with_path(R._dneg_item(int(n.group(1))), ans.group(1)):
                probs.append(f"{tid}: item {it['qid']} differs from the redo2 yn_dneg_beyond brief for {n.group(1)} wordings")
    return probs


def redo3_read_problems(plan2: dict, root: Path = REDO3) -> list:
    """The redo3 G-LEX read tasks must be the redo2/extract reads re-issued: same task id, prompt sha, item count and,
    from the prompt heading to the end marker, the same text (closed list and items). The header, the paths and the toy
    example may differ. [] when `root` holds no read task at all."""
    root = Path(root)
    tasks = {t.get("task_id"): t for t in json.loads((root / "TASKS.json").read_text(encoding="utf-8"))["tasks"]}
    probs = []
    for _read, b in plan2["batches"]:
        tid = b.chunks[0]["task_id"]
        t, f = tasks.get(tid), root / f"{tid}.txt"
        if t is None:
            continue                                                    # this read was not re-issued
        if t.get("prompt_sha") != b.prompt_sha or t.get("n_items") != len(b.key):
            probs.append(f"{tid}: redo3/TASKS.json prompt sha or item count differs from the redo2/extract read")
        if not f.is_file():
            probs.append(f"{tid}: the redo3 task file is missing")
            continue

        def tail(x):
            i, j = x.find(_READ_TAIL), x.rfind("END OF TASK FILE")
            return x[i:j] if 0 <= i < j else None

        got, want = f.read_text(encoding="utf-8"), R.glex_txt(b, R2X)
        if tail(got) is None or tail(got) != tail(want) or f"TASK ID : {tid}\n" not in got:
            probs.append(f"{tid}: the redo3 task file differs from the redo2/extract read (prompt, closed list or items)")
    return probs


def distrust(rep: dict, why: str) -> dict:
    """A copy of a round report in which every answer file is rejected for `why` (its task files failed a check)."""
    files = {t: {**r, "ok": False, "accepted": None, "reasons": list(r["reasons"]) + [why]} for t, r in rep["files"].items()}
    return {**rep, "files": files, "rejected": sorted(files)}


# ======================================================================================================= 3. targets

def target_rows(kept: dict) -> list:
    """Every G0 section 6 minimum as a row {target, got, bar, met}: authoring.shortfall unrolled (never lowered)."""
    M = A.MINIMUM
    rows = []

    def need(name, have, want):
        rows.append({"target": name, "got": have, "bar": want, "met": have >= want})

    packs = kept.get("pack", [])
    need("packs (training)", sum(not p["held_out"] for p in packs), M["pack_train"])
    need("packs (held out)", sum(p["held_out"] for p in packs), M["pack_held"])
    need("items", len(kept.get("item", [])), M["item"])
    js = kept.get("just", [])
    need("justifications", len(js), M["just"])
    for t in A.TONES:
        need(f"justifications {t}", sum(p["tone"] == t for p in js), M["just_per_tone"])
    need("attack lines", len(kept.get("attack", [])), M["attack"])
    sk = kept.get("skin", [])
    for reg in A.REGISTERS:
        pre = "held" if reg in A.HELD_OUT_REGISTERS else "skin"
        for lay in ("L0", "L1", "L2"):
            need(f"skins {reg} {lay}", sum(p["register"] == reg and p["layout"] == lay for p in sk), M[f"{pre}_{lay}"])
    rq = kept.get("req", [])
    for a in V.ACTIONS:
        for f in ("plain", "gate"):
            need(f"request forms {a} {f}", sum(p["sem"] == f"req.{a}.{f}" for p in rq), M[f"req_{f}"])
    inf = kept.get("info", [])
    for k in V.CLASSES:
        need(f"mention forms {k}", sum(p["sem"] == f"info.{k}" for p in inf), M["info"])
    need("courtesy lines", sum(p["sem"] == "info.neutral" for p in inf), M["info_neutral"])
    tk = kept.get("task", [])
    for t in A.TASK_SCOPE:
        need(f"task forms {t}", sum(p["sem"] == t for p in tk), M["task"])
    wd = kept.get("wording", [])
    for q in A.QFORMS:
        need(f"wordings {q}", sum(p["qform"] == q for p in wd), M["wording_dneg"] if q == "yn_dneg_beyond" else M["wording"])
    need("wordings (total)", len(wd), M["wording_total"])
    return rows


def extra_checks(kept: dict, gate_used: dict) -> list:
    """Pool checks beyond authoring.MINIMUM (see the module docstring): {check, got, bar, met, note}."""
    out = []
    train = [p for p in kept.get("skin", []) if not p["held_out"] and p["layout"] in ("L1", "L2")]
    share = Counter(p["register"] for p in train)
    top = max(share.values()) / len(train) if train else 1.0
    out.append({"check": "max register share of training L1 / L2 skins", "got": round(top, 4), "bar": MAX_REGISTER_SHARE,
                "met": top <= MAX_REGISTER_SHARE, "note": f"{max(share, key=share.get) if share else '-'}; pool-level measure"})
    tw = Counter(p["qform"] for p in kept.get("wording", []) if not A.held_out_wording(p["piece_id"]))
    for q in A.QFORMS:
        out.append({"check": f"training wordings {q} (after the held-out split)", "got": tw.get(q, 0),
                    "bar": MIN_TRAINING_WORDINGS, "met": tw.get(q, 0) >= MIN_TRAINING_WORDINGS, "note": ""})
    out.append({"check": "G-LEX gate over every form the pools use", "got": gate_used["status_counts"], "bar": "all admitted",
                "met": bool(gate_used["pass"]), "note": f"{gate_used['n_forms']} forms"})
    return out


# ======================================================================================================= 4. build

def _linted(path: Path) -> dict:
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    return {"kept": d["kept"], "dropped": d["dropped"], "problems": [], "counts": d["counts"]}


def build(*, fast: bool = False, ignored=()) -> SimpleNamespace:
    """The whole freeze in memory: nothing is written. fast: reuse haiku/author/linted.json and
    haiku/redo2/linted.json instead of re-linting the answers (never used for a freeze)."""
    s = SimpleNamespace(fast=fast)
    ignored = {str(Path(x).resolve()) if "/" in x else x for x in ignored}
    s.ignored = sorted(ignored)
    s.problems = []
    closed = closed_lists()
    a_defs, r2_defs, x_defs = author_defs(AUTHOR), author_defs(REDO2), extract_defs(EXTRACT)
    rounds = {
        "author": validate_round("author", a_defs, AUTHOR / "answers", ignored=ignored),
        "redo2_author": validate_round("redo2_author", r2_defs, REDO2 / "answers", ignored=ignored),
        "extract": validate_round("extract", x_defs, EXTRACT / "answers", closed_of=lambda c: closed[c.lex_kind],
                                  ignored=ignored),
        "redo": validate_round("redo", x_defs, REDO / "answers", closed_of=lambda c: closed[c.lex_kind],
                               ignored=ignored),
        "extract_superseded": validate_round("extract_superseded", x_defs, SUPERSEDED,
                                             closed_of=lambda c: closed[c.lex_kind], informational=True)}
    r3_on = (REDO3 / "TASKS.json").is_file()                 # redo3: authoring (3 wordings) + the re-issued supplement reads
    r3_batches = redo3_author_batches(REDO3) if r3_on else []
    r3_reads = frozenset(t["task_id"] for t in json.loads((REDO3 / "TASKS.json").read_text(encoding="utf-8"))["tasks"]
                         if not str(t.get("kind", "")).startswith("author_")) if r3_on else frozenset()
    if r3_batches:
        rounds["redo3_author"] = validate_round("redo3_author", author_defs(REDO3), REDO3 / "answers", ignored=ignored,
                                                also=r3_reads)

    # --- authoring: lint the validated answers (A.load), then the supplement (R.load) and merge
    checks = {}
    if fast:
        rep_main, rep2 = _linted(AUTHOR / "linted.json"), _linted(REDO2 / "linted.json")
    else:
        rep_main = A.load(AUTHOR, answers=accepted(rounds["author"]))
        rep2 = R.load(REDO2, answers=accepted(rounds["redo2_author"]), main=rep_main["kept"])
        d_main = json.loads((AUTHOR / "linted.json").read_text(encoding="utf-8"))
        d_r2 = json.loads((REDO2 / "linted.json").read_text(encoding="utf-8"))
        checks["author_linted_json_matches_rebuild"] = (canon(d_main["kept"]) == canon(rep_main["kept"])
                                                        and canon(d_main["dropped"]) == canon(rep_main["dropped"]))
        checks["redo2_linted_json_matches_rebuild"] = (canon(d_r2["kept"]) == canon(rep2["kept"])
                                                       and canon(d_r2["dropped"]) == canon(rep2["dropped"]))
    checks["lint_recomputed_from_answers"] = not fast
    s.problems += [f"author: {p}" for p in rep_main["problems"]] + [f"redo2: {p}" for p in rep2["problems"]]
    merged = R.merged_pools(rep_main["kept"], rep2["kept"])
    round_of = {p["piece_id"]: "redo2" for ps in rep2["kept"].values() for p in ps}

    # --- redo3 authoring: the same lint (authoring.load, then redo2.merge: lint_dneg + duplicates against everything kept)
    rep3 = {"kept": {}, "dropped": [], "problems": [], "counts": {}}
    if r3_batches:
        r3_probs = redo3_author_problems(r3_batches, REDO3)
        checks["redo3_author_task_matches_redo2_brief"] = not r3_probs
        s.redo3_author_problems = r3_probs
        raw3 = A.load(REDO3, answers=accepted(rounds["redo3_author"]), batches=r3_batches)
        kept3, dropped3 = R.merge(raw3["kept"], raw3["dropped"], merged)
        rep3 = {"kept": kept3, "dropped": dropped3, "problems": raw3["problems"],
                "counts": {**{f"kept_{k}": len(v) for k, v in sorted(kept3.items())}, "dropped": len(dropped3),
                           "wordings_asked": sum(len(v) for r in accepted(rounds["redo3_author"]).values()
                                                 for v in r.values())}}
        s.problems += [f"redo3: {p}" for p in rep3["problems"]]
        merged = R.merged_pools(merged, kept3)
        round_of.update({p["piece_id"]: "redo3" for ps in kept3.values() for p in ps})
    else:
        s.redo3_author_problems = []

    # --- registry and the first-pass reads
    reg = A.registry(merged)
    form_of = {f.text: fid for fid, f in reg.forms.items()}
    main_fids = sorted(form_of[p["text"]] for pool in LEX_POOLS for p in rep_main["kept"].get(pool, []))
    batches = extraction_batches(reg, [f for f in main_fids if reg.forms[f].unit_ok])
    n_files, file_probs = E.files_check({"batches": batches})
    checks["first_pass_read_files_match_rebuild"] = not file_probs
    s.read_file_checked, s.read_file_problems = n_files, file_probs
    picks, pick_notes = pick_extract(rounds["extract"], rounds["redo"])
    s.pick_notes = pick_notes
    reads = []
    for read, kind, _g, b in batches:
        tid = b.chunks[0]["task_id"]
        pk = picks.get(tid) if not file_probs else None
        reads.append({"extractor": f"{read}:{tid}", "task_id": tid, "read": read, "kind": kind, "key": dict(b.key),
                      "answer": pk["answer"] if pk else None, "only": None, "source": pk["source"] if pk else None})

    # --- the supplement reads (yn_dneg_beyond wordings): their own 2 reads, controls never recorded
    plan2 = None
    tests: set = set()
    if any(p["qform"] == "yn_dneg_beyond" for p in rep2["kept"].get("wording", [])):
        plan2 = R.glex_plan(supp=rep2["kept"], main=rep_main["kept"])
        tests = set(plan2["tests"])
        miss = sorted(t for t in tests if t not in reg.forms)
        checks["supplement_forms_in_registry"] = not miss
        r2_probs = r2_file_problems(plan2, R2X)
        checks["supplement_read_files_match_rebuild"] = not r2_probs
        s.r2_file_problems = r2_probs
        sup_defs = defs_from_batches(plan2["batches"])
        rounds["redo2_extract"] = validate_round("redo2_extract", sup_defs, R2X / "answers",
                                                 closed_of=lambda c: closed["question"], ignored=ignored)
        # redo3 holds the SAME reads re-issued (same task ids): one read per task, never two votes (pick_extract)
        r3_read_probs = redo3_read_problems(plan2, REDO3) if r3_on else []
        if r3_on:
            checks["supplement_reads_redo3_files_match_redo2"] = not r3_read_probs
            rounds["redo3_extract"] = validate_round("redo3_extract", sup_defs, REDO3 / "answers",
                                                     closed_of=lambda c: closed["question"], ignored=ignored,
                                                     also=frozenset(d.task_id for d in author_defs(REDO3).values()))
        s.r3_read_problems = r3_read_probs
        rep_a = distrust(rounds["redo2_extract"], "redo2/extract task files differ from the rebuild") if r2_probs \
            else rounds["redo2_extract"]
        rep_b = rounds.get("redo3_extract", {"files": {}, "missing": []})
        if r3_read_probs:
            rep_b = distrust(rep_b, "redo3 task files differ from the redo2/extract reads")
        sup_picks, sup_notes = pick_extract(rep_a, rep_b, names=("redo2/extract", "redo3"))
        s.sup_picks, s.sup_notes = sup_picks, sup_notes
        for read, b in plan2["batches"]:
            tid = b.chunks[0]["task_id"]
            pk = sup_picks.get(tid)
            reads.append({"extractor": f"redo2-{read}:{tid}", "task_id": tid, "read": read, "kind": "question",
                          "key": dict(b.key), "answer": pk["answer"] if pk else None, "only": tests,
                          "source": pk["source"] if pk else None})
    else:
        rounds["redo2_extract"] = validate_round("redo2_extract", {}, R2X / "answers")
        s.r2_file_problems, s.r3_read_problems, s.sup_picks, s.sup_notes = [], [], {}, {}
    s.rounds = rounds
    s.vote_log = record_reads(reg, reads)

    # --- admission, G-LEX gates, the held-out wording split
    status = {fid: reg.status(fid) for fid in sorted(reg.forms)}
    adm = {fid for fid, st in status.items() if st == "admitted"}
    kept = {pool: list(ps) for pool, ps in merged.items()}
    for pool in LEX_POOLS:
        kept[pool] = [p for p in merged.get(pool, []) if form_of[p["text"]] in adm]
    held = {}
    for p in kept.get("wording", []):
        held[form_of[p["text"]]] = A.held_out_wording(p["piece_id"])
        reg.forms[form_of[p["text"]]].held_out = held[form_of[p["text"]]]
    lex_obj = reg.to_json()
    lex_obj["forms"] = [x for x in lex_obj["forms"] if x["status"] == "admitted"]
    chk = LexiconRegistry.from_json(lex_obj)          # re-runs the unit tests and the vote status on the pool
    gate_used, gate_all = chk.gate(), reg.gate()
    checks["lexicon_roundtrip_same_forms"] = sorted(chk.forms) == sorted(adm)
    checks["g0_sha_matches_plugin"] = sha_bytes(G0.read_bytes()) == T27Plugin.G0_SHA256

    # --- targets
    rows = target_rows(kept)
    cross = {f"{r['target']}: {r['got']} < {r['bar']}" for r in rows if not r["met"]}
    checks["targets_match_authoring_shortfall"] = cross == set(A.shortfall(kept))
    s.target_rows = rows
    s.shortfalls = [r for r in rows if not r["met"]]
    s.extras = extra_checks(kept, gate_used)
    s.checks = checks

    # --- pending reads, quarantine, counts
    s.pending = []
    quarantine = []
    for src, rep in (("author", rep_main), ("redo2", rep2), ("redo3", rep3)):
        for d in rep["dropped"]:
            quarantine.append({"stage": "lint", "round": src, "pool": d["pool"], "text": d["text"], "why": d["why"],
                               "task_id": d.get("task_id")})
    for fid in sorted(reg.forms):
        if fid in adm:
            continue
        f = reg.forms[fid]
        n_ext = len({e for e, _ in f.extractions})
        row = {"form_id": fid, "sem_id": f.sem_id, "kind": f.kind, "text": f.text, "status": status[fid],
               "reads_required": f.required, "reads_recorded": n_ext,
               "extractions": [[e, sm] for e, sm in f.extractions]}
        quarantine.append({"stage": "g-lex", **row, "why": [f"{status[fid]}: {n_ext} of {f.required} agreeing reads"]})
        if status[fid] == "pending":
            s.pending.append(row)
    for name, rr in rounds.items():
        if rr["informational"]:
            continue
        for tid in rr["rejected"]:
            quarantine.append({"stage": "validation", "round": name, "task_id": tid, "why": rr["files"][tid]["reasons"]})
        for tid, rej in rr["item_rejects"].items():
            quarantine.append({"stage": "validation", "round": name, "task_id": tid, "why": [f"{q}: {w}" for q, w in rej.items()]})
    s.quarantine = quarantine
    s.kept, s.reg, s.lex_obj, s.gate_used, s.gate_all = kept, reg, lex_obj, gate_used, gate_all
    s.status_of, s.round_of, s.form_of, s.held_of = status, round_of, form_of, held
    s.rep_main, s.rep2, s.plan2, s.tests = rep_main, rep2, plan2, tests
    s.counts = {
        "authoring": rep_main["counts"], "redo2_authoring": rep2["counts"], "redo3_authoring": rep3["counts"],
        "kept_after_g_lex": {pool: len(ps) for pool, ps in sorted(kept.items())},
        "forms": {"total": len(reg.forms), "admitted": len(adm), "status": dict(sorted(Counter(status.values()).items())),
                  "by_kind": {k: dict(sorted(Counter(status[f] for f in reg.forms if reg.forms[f].kind == k).items()))
                              for k in sorted({f.kind for f in reg.forms.values()})}},
        "required_reads_by_kind": {k: next(f.required for f in reg.forms.values() if f.kind == k)
                                   for k in sorted({f.kind for f in reg.forms.values()})},
        "reads": {"recorded": sum(1 for r in s.vote_log if r["status"] == "recorded"),
                  "unanswered": sum(1 for r in s.vote_log if r["status"] == "unanswered"),
                  "votes_recorded": sum(r["recorded"] for r in s.vote_log)},
        "g3h": {"applicable": False, "items": 0, "reason": "Mode T only (G0 S18): T27 has no extract_fields"},
        "quarantine_rows": len(quarantine), "targets_total": len(rows), "targets_met": sum(1 for r in rows if r["met"])}

    # --- verdict
    unresolved = [t for t in sorted(x_defs) if t not in picks]
    used_rej = []
    for name in ("author", "redo2_author", "redo3_author"):
        if name not in rounds:
            continue
        used_rej += [f"{name}:{t}" for t in rounds[name]["rejected"] + rounds[name]["missing"]]
        used_rej += [f"{name}:{t}:{q}" for t, d in rounds[name]["item_rejects"].items() for q in d]
    used_rej += [f"extract/redo:{t}" for t in unresolved]
    # a supplement read: a rejected copy with no valid copy to use, or two valid copies that differ
    for t in sorted(s.sup_notes):
        if t in s.sup_picks:
            continue
        used_rej += [f"{n}:{t}" for n in ("redo2_extract", "redo3_extract") if n in rounds and t in rounds[n]["rejected"]]
        if s.sup_notes[t].startswith("CONFLICT"):
            used_rej.append(f"supplement_read:{t}")
    s.used_answer_problems = used_rej
    s.checks["no_answer_used_was_rejected_or_missing"] = not used_rej
    s.checks["no_stray_answer_files"] = not any(r["stray"] for r in rounds.values() if not r["informational"])
    s.ready = (not fast and not s.shortfalls and all(e["met"] for e in s.extras) and all(checks.values())
               and s.checks["no_answer_used_was_rejected_or_missing"])
    bits = [f"{r['target']} {r['got']}/{r['bar']}" for r in s.shortfalls]
    bits += [f"{e['check']} {e['got']}/{e['bar']}" for e in s.extras if not e["met"]]
    bits += [f"check {k} fails" for k, v in checks.items() if not v]
    pend = sum(max(0, p["reads_required"] - p["reads_recorded"]) for p in s.pending)
    s.status = ("READY: every G0 minimum is met, the G-LEX gate passes over every form the pools use, and every check holds"
                + (f" ({len(s.pending)} pending form(s) await {pend} G-LEX read(s) and stay outside the pools)"
                   if s.pending else "")
                if s.ready else "SHORT: " + "; ".join(bits or (["--fast run: the lint was not recomputed, not a freeze"] if fast
                                                       else ["no G0 shortfall (see checks)"]))
                + (f"; {len(s.pending)} form(s) still await {pend} G-LEX read(s)" if s.pending else ""))
    return s


# ======================================================================================================= 5. write

def _piece(p: dict, s) -> dict:
    return {**p, "round": s.round_of.get(p["piece_id"], "author")}


def pool_docs(s) -> dict:
    """{file name: JSON object} for the seven pool files and the quarantine, deterministic from the build."""
    k = s.kept
    tr = [p for p in k.get("pack", []) if not p["held_out"]]
    ho = [p for p in k.get("pack", []) if p["held_out"]]
    packs = []
    for pre, group, held in (("t27-pack", tr, False), ("t27-hpack", ho, True)):
        cap = PV.N_CARD_HELD_PACKS if held else PV.N_CARD_PACKS
        for i, p in enumerate(group, 1):
            packs.append({"pack_id": f"{pre}-{i:02d}", "held_out": held, "use": "card" if i <= cap else "spare",
                          "setting": p["text"]["setting"], "names": p["text"]["names"], "piece_id": p["piece_id"],
                          "task_id": p["task_id"], "prompt_sha": p["prompt_sha"], "round": s.round_of.get(p["piece_id"], "author")})
    taken: set = set()
    items = [{"item_id": PV.item_key(p["text"], taken), **_piece(p, s)} for p in k.get("item", [])]
    justs, n = [], 0
    for tone in A.TONES:
        for p in k.get("just", []):
            if p["tone"] == tone:
                n += 1
                justs.append({"just_id": f"j{n:02d}", **_piece(p, s)})
    skins = [_piece(p, s) for p in k.get("skin", [])]
    attack = [_piece(p, s) for p in k.get("attack", [])]
    wordings = []
    for p in k.get("wording", []):
        fid = s.form_of[p["text"]]
        f = s.reg.forms[fid]
        wordings.append({**_piece(p, s), "form_id": fid, "sem_id": f.sem_id, "held_out": bool(s.held_of[fid]),
                         "extractions": [[e, sm] for e, sm in f.extractions]})

    def doc(kind, recs, **more):
        return {"family": FAMILY, "version": VERSION, "kind": kind, "count": len(recs), **more, "records": recs}

    return {"packs.json": doc("packs", packs, note="use=card: the 25 training / 5 held-out packs a card's k mod 25 / k mod 5 "
                              "selects (G0 section 2); use=spare: kept and frozen, not selected"),
            "items.json": doc("information items (TARGET, GATE)", items),
            "justifications.json": doc("justification bank", justs),
            "attack_lines.json": doc("attack lines", attack),
            "skins.json": doc("carrier skins", skins),
            "wordings.json": doc("admitted question wordings", wordings),
            "lexicon.json": s.lex_obj,
            "quarantine.json": doc("quarantine", s.quarantine)}


LOADER_NOTE = (
    "plugin.py reads no pool path: T27Plugin takes admitted lexicon forms from the registry the caller passes "
    "(T27Plugin(lexicon=reg)), skins / wordings / attack lines from the KitCtx the caller builds, and its information "
    "items, justification bank, source names and pack ids from the stand-in constants of vocab.py, which plugin.py and "
    "solver_b.py copy when they are imported; there is no configurable path to refresh. The generator must: "
    "(1) from families.T27 import pools_v2 as PV (imports vocab only); (2) pools = PV.read_pools() (verifies every file "
    "against this manifest); (3) PV.require_ready(pools) (training rows only from a READY freeze); (4) "
    "PV.install_vocab(pools) BEFORE importing families.T27.plugin or solver_b (it refuses afterwards); (5) "
    "ctx = PV.build_ctx(pools); plugin = T27Plugin(lexicon=ctx.lexicon). Training skins are skins.json records with "
    "held_out=false, wordings.json records with held_out=false are training wordings (true: sampler S5 only, from the "
    "seeded 15% split authoring.held_out_wording), attack_lines.json are the inv attack lines, packs.json use=card "
    "records are the 25 + 5 packs of G0 section 2 (use=spare are frozen but not selected). Caveat: authoring.lex_items "
    "indexes V.ITEMS['price_list'], so G-LEX read tasks cannot be rebuilt after install_vocab. T27 has no pools/ "
    "folder (the Stage A freeze was never run: 0 admitted forms), so there is no v1 to supersede; g13_c2.pool_units "
    "reads families/T27/pools/, so promotion of pools_v2/ to pools/ is a separate step after READY and is not done "
    "here. G13-seed is not run here.")


def render_texts(s) -> dict:
    return {name: json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True) + "\n" for name, obj in pool_docs(s).items()}


def build_manifest(s, texts: dict) -> dict:
    code = {n: sha_bytes((HERE / n).read_bytes()) for n in ("freeze_v2.py", "pools_v2.py", "authoring.py", "redo2.py",
                                                            "extract_check.py", "glex_build.py", "plugin.py", "vocab.py")}
    inputs = {
        "author_answers": {t: r["sha256"] for t, r in sorted(s.rounds["author"]["files"].items())},
        "redo2_author_answers": {t: r["sha256"] for t, r in sorted(s.rounds["redo2_author"]["files"].items())},
        "extract_answers": {t: r["sha256"] for t, r in sorted(s.rounds["extract"]["files"].items())},
        "redo_answers": {t: r["sha256"] for t, r in sorted(s.rounds["redo"]["files"].items())},
        "superseded_first_attempt_answers (not used)": {t: r["sha256"] for t, r in
                                                        sorted(s.rounds["extract_superseded"]["files"].items())},
        "redo2_extract_answers": {t: r["sha256"] for t, r in sorted(s.rounds["redo2_extract"]["files"].items())},
        "redo3_author_answers": {t: r["sha256"] for t, r in
                                 sorted(s.rounds.get("redo3_author", {"files": {}})["files"].items())},
        "redo3_extract_answers (the supplement reads re-issued)": {
            t: r["sha256"] for t, r in sorted(s.rounds.get("redo3_extract", {"files": {}})["files"].items())}}
    return {
        "family": FAMILY, "version": VERSION, "stage": "admit + freeze (author, redo, redo2 and redo3 rounds; freeze_v2.py)",
        "status": s.status, "ready": s.ready,
        "supersedes": "nothing: families/T27/pools/ does not exist (Stage A froze nothing: 0 forms admitted)",
        "a38_present": paths.a38_frozen(),
        "g0": {"path": "families/T27/G0_SPEC.md", "sha256": sha_bytes(G0.read_bytes()),
               "plugin_G0_SHA256": T27Plugin.G0_SHA256, "matches_plugin": s.checks["g0_sha_matches_plugin"]},
        "load": LOADER_NOTE,
        "pool_files": {n: {"sha256": sha_text(t), "bytes": len(t.encode("utf-8")), "records": json.loads(t).get("count",
                       len(json.loads(t).get("forms", [])))} for n, t in sorted(texts.items()) if n != "quarantine.json"},
        "quarantine_file": {"name": "quarantine.json", "sha256": sha_text(texts["quarantine.json"]),
                            "records": s.counts["quarantine_rows"]},
        "counts": s.counts, "targets": s.target_rows, "shortfalls": s.shortfalls, "extra_checks": s.extras,
        "gates": {"G-LEX_used_forms": {k: v for k, v in s.gate_used.items() if k != "not_admitted"},
                  "G-LEX_all_registry_forms": {k: v for k, v in s.gate_all.items() if k != "not_admitted"},
                  "G-LEX_not_admitted_count": len(s.gate_all["not_admitted"]),
                  "G3-H": s.counts["g3h"],
                  "G-SL": "lint at ingest (authoring.lint_piece / lint_skin / lint_wording, redo2.lint_dneg): dropped "
                          "pieces are in quarantine.json",
                  "G13_seed": "not run here (C2_DATA_SPEC 6.4 step 4)"},
        "checks": s.checks, "votes": s.vote_log, "pick_notes": s.pick_notes, "supplement_pick_notes": s.sup_notes,
        "pending_forms": [{k: v for k, v in p.items() if k != "extractions"} for p in s.pending],
        "supplement_reads": [{"read": r, "task_id": b.chunks[0]["task_id"], "task_file": f"haiku/redo2/extract/{b.chunks[0]['task_id']}.txt",
                              "answer_file": f"haiku/redo2/extract/answers/{b.chunks[0]['task_id']}.json",
                              "issued": (R2X / "TASKS.json").is_file(),
                              "used_answer": (s.sup_picks.get(b.chunks[0]["task_id"]) or {}).get("source"),
                              "used_answer_sha256": (s.sup_picks.get(b.chunks[0]["task_id"]) or {}).get("sha256"),
                              "note": s.sup_notes.get(b.chunks[0]["task_id"])}
                             for r, b in (s.plan2["batches"] if s.plan2 else [])],
        "validation": {n: {k: v for k, v in slim(r).items() if k != "files"} | {"files": len(r["files"])}
                       for n, r in s.rounds.items()},
        "used_answer_problems": s.used_answer_problems, "ignored_by_audit": s.ignored,
        "inputs": inputs, "code": code,
        "not_verified": ["file-access audit (c2_kit.audit) of the Haiku agents: needs their transcripts, which this "
                         "script does not open; the orchestrator's failed-audit list is applied through --ignore"]}


def write_freeze(s) -> dict:
    paths.require_a38()
    if s.fast:
        raise SystemExit("freeze refuses --fast: the lint must be recomputed from the answers")
    texts = render_texts(s)
    manifest = build_manifest(s, texts)
    mtext = json.dumps(manifest, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    vreport = json.dumps({"family": FAMILY, "version": VERSION, "rounds": {n: slim(r) for n, r in s.rounds.items()},
                          "note": "every answer file against its contract; nothing was edited"},
                         ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    out = dict(texts)
    out["validation_report.json"] = vreport
    out["MANIFEST.json"] = mtext
    mf = POOLS_V2 / "MANIFEST.json"
    if mf.is_file() and json.loads(mf.read_text(encoding="utf-8")).get("ready") and mf.read_text(encoding="utf-8") != mtext:
        raise SystemExit("pools_v2/MANIFEST.json is READY: a frozen pool set is never overwritten")
    for name in out:
        if POOLS_V2.resolve() not in (POOLS_V2 / name).resolve().parents:
            raise PermissionError(f"freeze_v2 writes inside pools_v2/ only: {name}")
    paths.write_files(POOLS_V2, out)
    return {"manifest": str(mf), "manifest_sha256": sha_text(mtext), "files": sorted(out)}


def write_reads(s) -> list:
    """Write the supplement G-LEX read tasks (redo2.glex_write) when the build agrees with the on-disk linted.json."""
    paths.require_a38()
    if s.fast or not (s.checks.get("author_linted_json_matches_rebuild") and s.checks.get("redo2_linted_json_matches_rebuild")):
        raise SystemExit("reads refused: haiku/*/linted.json differs from the rebuild (or --fast): redo2.glex_write reads them")
    if s.plan2 is None:
        raise SystemExit("no yn_dneg_beyond wording to read")
    if (R2X / "TASKS.json").is_file():
        raise SystemExit(f"{rel(R2X / 'TASKS.json')} exists: the supplement read tasks are written once "
                         f"(file problems: {s.r2_file_problems[:2]})")
    return R.glex_write(R2X)


def summarize(s, extra: dict | None = None) -> dict:
    out = {"family": FAMILY, "version": VERSION, "fast": s.fast, "ready": s.ready, "status": s.status,
           "targets": f"{s.counts['targets_met']}/{s.counts['targets_total']} G0 minimums met",
           "shortfalls": [f"{r['target']}: {r['got']} of {r['bar']}" for r in s.shortfalls],
           "extra_checks": [f"{'ok ' if e['met'] else 'FAIL '}{e['check']}: {e['got']} (bar {e['bar']})" for e in s.extras],
           "checks": s.checks, "counts": {k: v for k, v in s.counts.items() if k not in ("authoring", "redo2_authoring")},
           "validation": {n: {"tasks": r["tasks"], "answer_files": len(r["files"]),
                              "accepted": sum(1 for x in r["files"].values() if x["ok"]), "rejected": r["rejected"],
                              "missing": r["missing"], "stray": r["stray"], "item_rejects": r["item_rejects"]}
                          for n, r in s.rounds.items()},
           "pick_notes": dict(Counter(s.pick_notes.values())), "supplement_pick_notes": s.sup_notes,
           "redo3_problems": {"author": s.redo3_author_problems, "reads": s.r3_read_problems},
           "used_answer_problems": s.used_answer_problems,
           "read_file_problems": s.read_file_problems[:3], "pending_forms": len(s.pending),
           "pending_reads_by_sem": dict(Counter(p["sem_id"] for p in s.pending)),
           "gates": {"G-LEX_used_forms": s.gate_used["pass"], "G-LEX_registry_not_admitted": len(s.gate_all["not_admitted"])}}
    out.update(extra or {})
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="families.T27.freeze_v2")
    ap.add_argument("cmd", choices=("check", "reads", "freeze"))
    ap.add_argument("--fast", action="store_true", help="check only: reuse linted.json instead of re-linting")
    ap.add_argument("--ignore", action="append", default=[], help="task id or answer path whose audit failed")
    a = ap.parse_args(argv)
    s = build(fast=a.fast, ignored=a.ignore)
    extra = {}
    if a.cmd == "reads":
        extra["reads_written"] = [str(x) for x in write_reads(s)]
    elif a.cmd == "freeze":
        extra["written"] = write_freeze(s)
    print(json.dumps(summarize(s, extra), indent=1, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""families/T31/freeze_v2.py: T31 pool re-freeze (pools_v2/) after the redo, redo2 and redo2/extract Haiku rounds
(G0_SPEC.md section 7; C2_DATA_SPEC 6.2 item 2, 6.3 G-SL / G-LEX / G3-H, 6.4 steps 3-4; PREREG A37 (b), A38).

Why a new script. glex_admit.py (freeze-v1) and topup.py (freeze-v2, round A2) each refuse to write over an existing
MANIFEST.json, and the A2 freeze was written while the two G-LEX reads of the top-up forms (haiku/redo2/extract/) were
unanswered. Those reads are answered now. This script is the re-freeze path: it reads the frozen v1 inputs, every redo
answer, and the new read answers, and writes pools_v2/ again. It edits nothing that exists: pools/ (v1), every answer
file, every plan / chunk / key / task file and all pinned code stay byte for byte as they are. It writes only
pools_v2/ (after archiving the superseded A2 partial freeze to pools_v2_a2_partial/, never deleting a file).

  check    in memory only: validate every answer file, rebuild v1 and prove it reproduces pools/, merge the redo pieces,
           record every G-LEX vote, apply every gate, print the counts and READY or SHORT with the exact shortfalls.
  freeze   the same, then write pools_v2/ (skins, documents, attack, wordings, lexicon, packs, QUARANTINE,
           VALIDATION_REPORT, MANIFEST) through the guarded kit writers (after A38 only). Refuses a blocking problem,
           and refuses to replace a pools_v2/ that is already READY.

Run from lean/:  ../.venv/bin/python -B c2_build/families/T31/freeze_v2.py check|freeze
                 [--exclude-task <task id>]...   a task whose file-access audit failed: its answers are ignored
                 [--strict-files]                reject a whole file on any contract break (see 1.)

What it does, in order. No label is set anywhere; Haiku answers only flag (A37 b).
  1. Contract check of EVERY answer file of every round (v1 author, v1 extract, redo, redo2, redo2/extract; any other
     haiku/redo* folder is reported, never read). Whole-file break (the file is rejected, nothing of it is used): not
     UTF-8 JSON, a duplicate JSON key, NaN / Infinity, a top level that is not a list, an entry that is not an object.
     Entry break (that entry is rejected; the file's other entries stand): the key set is not exactly
     {qid, text | pack | names | choice}, a qid that is not a string or not in the task's own items, a qid answered twice
     (every copy is rejected), a value of the wrong type, a G-LEX choice that is neither null nor one of the item's listed
     meanings copied exactly. A rejected entry is "unanswered": it is never a vote and never a piece. This is the kit's
     own item-level rule (chunker.load_answers) and the rule v1 and the A2 freeze were built under; the one contract
     break in the real data (a mistyped qid in v1 file a7e52c11, re-asked by the redo task) is shown in
     VALIDATION_REPORT.json and the MANIFEST. --strict-files rejects the whole file on any entry break or unanswered
     item instead (the T26 / T28 reading); the MANIFEST of a strict run records the policy. Files are only read.
  2. v1 is rebuilt in memory (the same pipeline, v1 answers only) and must reproduce pools/ byte for byte (sha256 of
     every file equals pools/MANIFEST.json and the file on disk, every v1 read answer equals its manifest sha). The
     authoring batches (v1 and redo2) are rebuilt and must equal the files on disk. A mismatch blocks the freeze.
  3. Redo pieces (the v1 redo item; the redo2 skins, Mode F documents and wordings) go through the SAME loader checks as
     v1 (haiku_author._load_one: G-SL lint, name lint, negation counts, REQ_ID rule), then the same value lint and the
     same exact-text dedup (a new piece never displaces a v1 piece), against everything already accepted.
  4. G-LEX: every form is unit-tested; votes are recorded from the valid read answers only, one extractor id per read
     (v1: read0, read1; top-up: r2read0, r2read1). Admission is the kit rule (lexicon.LexiconRegistry.status): the unit
     test passes and >= 2 distinct extractors (3 for kinds precedence and window) all pick the declared sem; any other
     pick, or null, rejects the form for good. T31 has no precedence / window form, so every form needs 2/2.
     The gate is the kit's: every form a pool piece USES is admitted (lexicon.py: "G-LEX gate(form_ids): every form a
     row uses is admitted. Rows never use pending or rejected forms"; README gates table). The used forms are read back
     from the written files (wordings.json + the usable comparator forms of lexicon.json), the registry is rebuilt from
     lexicon.json, and the gate is run on that set. The registry-wide gate (every form incl. rejected ones, which stay in
     the registry for good) is reported too; it cannot pass once any form is rejected, and no row can use such a form.
  5. G-SL: applied at load to every piece, and again as a final audit on the pieces read back from the frozen files.
     G3-H: not a pool-stage gate for T31 (G0 section 7, README, extract_build: it runs at the pilot and on full
     generation; every round holds author and extract_lex tasks only); recorded as such, never invented.
  6. The G0 targets of glex_admit.G0_TARGETS (imported, never changed; pinned in test_freeze_v2.py) are applied to the
     merged pool and again to a recount from the frozen files.

READY means: no G0 shortfall, the G-LEX gate passes on every form the pools use, and no blocking problem. Otherwise
SHORT (or BLOCKED) with the exact shortfalls. G13-seed (6.4 step 4) and row generation are not run here.

How the generator loads pools_v2. Nothing in the T31 code (plugin.py, solver_b.py, haiku_author.py, topup.py,
glex_admit.py) reads a pool path, so there is no path to refresh. g13_c2.py reads families/T31/pools/ (hard-coded).
To use pools_v2 either
  (a) pools = freeze_v2.load_pools();  ctx = freeze_v2.kit_ctx(pools);  plugin = T31(lexicon=pools["lexicon"])
      (Skin objects with each wording's lexicon_ids set to its form id, which pipeline.lex_problems needs; a
      LexiconRegistry rebuilt from lexicon.json with every vote; packs and names), or
  (b) after the owner rules, promote by directory move (the MANIFEST says so): pools/ -> pools_v1/, pools_v2/ -> pools/.
Keep v1 untouched until then.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True        # importing the kit and the T31 modules must not leave __pycache__ files behind

import argparse  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import re  # noqa: E402
from collections import Counter, defaultdict  # noqa: E402
from dataclasses import dataclass, field  # noqa: E402
from pathlib import Path  # noqa: E402

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker as CH  # noqa: E402
from c2_kit import gsl, paths  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit.lexicon import STRICT_KINDS, LexiconRegistry, question_sem  # noqa: E402
from c2_kit.plugin import KitCtx  # noqa: E402
from families.T31 import extract_build as EB  # noqa: E402
from families.T31 import glex_admit as GA  # noqa: E402
from families.T31 import haiku_author as HA  # noqa: E402
from families.T31 import plugin as P  # noqa: E402
from families.T31 import topup as T  # noqa: E402

F = "T31"
VERSION = "freeze-v2"
REVISION = "A2b: top-up G-LEX reads r2read0 / r2read1 loaded"
HAIKU = HERE / "haiku"
POOLS_V1 = GA.POOLS
POOLS_V2 = T.POOLS2
ARCHIVE = HERE / "pools_v2_a2_partial"
G0 = GA.G0
G0_TARGETS = GA.G0_TARGETS                 # imported, never changed (test_freeze_v2.py pins every number)

V1_ROUNDS = ("v1-author", "v1-extract")
ALL_ROUNDS = ("v1-author", "v1-extract", "redo1", "redo2", "redo2-extract")
HANDLED_KINDS = ("author_skin", "author_freeform", "author_wording", "author_lexicon", "author_pack", "extract_lex")
REDO1_QID_RE = re.compile(r"The qid of the item to answer is: (q[0-9A-Za-z]{10})")


# ------------------------------------------------------------------------------------------------ small helpers
def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p) -> str:
    return sha_bytes(Path(p).read_bytes())


def rel(p) -> str:
    p = Path(p).resolve()
    try:
        return p.relative_to(C2_BUILD).as_posix()
    except ValueError:
        return str(p)


def dump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=1) + "\n"


def _read_json(p) -> object:
    return json.loads(Path(p).read_text(encoding="utf-8"))


def _no_dup_pairs(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise ValueError(f"duplicate JSON key {k!r}")
        out[k] = v
    return out


def _no_const(name):
    raise ValueError(f"{name} is not valid JSON for an answer")


# ------------------------------------------------------------------------------------------------ 1. answer contract
@dataclass
class TaskDef:
    """What one Haiku task gave the agent, and what its answer file must hold."""
    round: str
    task_id: str
    batch_id: str
    kind: str
    key: str                        # the one value key beside "qid": text | pack | names | choice
    qids: tuple                     # the items the file must answer, once each
    answer_file: Path
    choices: dict = field(default_factory=dict)      # qid -> the item's listed meanings (extract_lex)
    root: Path | None = None
    problems: list = field(default_factory=list)     # task-file / chunk integrity problems (blocking)


def value_key(kind: str, track: str | None = None) -> str:
    if kind == "author_pack":
        return "names" if track == "both" else "pack"
    if kind == "extract_lex":
        return "choice"
    if kind in ("author_skin", "author_freeform", "author_wording", "author_lexicon"):
        return "text"
    raise ValueError(f"unknown task kind {kind!r}")


def _value_problem(td: TaskDef, qid: str, a: dict) -> str | None:
    v = a[td.key]
    if td.key == "text":
        return None if isinstance(v, str) else "text is not a string"
    if td.key == "pack":
        return None if isinstance(v, dict) else "pack is not an object"
    if td.key == "names":
        return None if isinstance(v, list) and all(isinstance(x, str) for x in v) else "names is not a list of strings"
    if v is None:                               # extract_lex: null = "no meaning fits exactly" (a vote against)
        return None
    if not isinstance(v, str):
        return "choice is neither null nor a string"
    if v not in td.choices.get(qid, ()):
        return "choice is not one of the item's listed meanings (copied exactly)"
    return None


def validate_answer_bytes(data: bytes, td: TaskDef, *, strict_files: bool = False) -> dict:
    """The contract check of one answer file (never edits it). -> {"status", "entries", "file_problems",
    "item_problems", "unanswered", "n_valid"}. status: valid | partial | invalid. entries: the valid entries in file
    order (empty unless valid / partial)."""
    res = {"status": "invalid", "entries": [], "file_problems": [], "item_problems": [], "unanswered": [], "n_valid": 0}
    try:
        obj = json.loads(data.decode("utf-8"), object_pairs_hook=_no_dup_pairs, parse_constant=_no_const)
    except (UnicodeDecodeError, ValueError) as e:
        res["file_problems"].append(f"not valid UTF-8 JSON ({str(e)[:90]})")
        res["unanswered"] = sorted(td.qids)
        return res
    if not isinstance(obj, list):
        res["file_problems"].append("the top level is not a JSON list")
        res["unanswered"] = sorted(td.qids)
        return res
    bad_entries = [i for i, a in enumerate(obj) if not isinstance(a, dict)]
    if bad_entries:
        res["file_problems"].append(f"entries {bad_entries[:5]} are not objects")
        res["unanswered"] = sorted(td.qids)
        return res
    want_keys = {"qid", td.key}
    counts = Counter(a["qid"] for a in obj if isinstance(a.get("qid"), str))
    ok_entries, ok_qids = [], set()
    for i, a in enumerate(obj):
        qid = a.get("qid")
        if set(a) != want_keys:
            res["item_problems"].append(f"entry {i}: keys {sorted(a)} != {sorted(want_keys)}")
        elif not isinstance(qid, str):
            res["item_problems"].append(f"entry {i}: qid is not a string")
        elif qid not in td.qids:
            res["item_problems"].append(f"entry {i}: qid {qid!r} is not one of this task's items")
        elif counts[qid] > 1:
            res["item_problems"].append(f"entry {i}: qid {qid} answered {counts[qid]} times (every copy rejected)")
        else:
            why = _value_problem(td, qid, a)
            if why:
                res["item_problems"].append(f"entry {i}: {qid}: {why}")
            else:
                ok_entries.append(a)
                ok_qids.add(qid)
    res["unanswered"] = sorted(set(td.qids) - ok_qids)
    broken = bool(res["item_problems"] or res["unanswered"])
    if not ok_entries or (strict_files and broken):
        res["status"] = "invalid"
        if strict_files and broken and ok_entries:
            res["file_problems"].append("strict file policy: the file breaks its contract, so none of it is used")
        return res
    res["entries"] = ok_entries
    res["n_valid"] = len(ok_entries)
    res["status"] = "partial" if broken else "valid"
    return res


def read_answer_file(td: TaskDef, excluded: set, strict_files: bool) -> tuple:
    """(entries or None, record). The record is what VALIDATION_REPORT.json lists for the file."""
    rec = {"round": td.round, "task_id": td.task_id, "kind": td.kind, "file": rel(td.answer_file), "sha256": None,
           "n_expected": len(td.qids), "n_valid": 0, "status": "valid", "problems": [], "plan_problems":
           list(td.problems), "unanswered": [], "rejected_entries": []}
    p = Path(td.answer_file)
    if p.is_file():
        rec["sha256"] = sha_file(p)
    if td.task_id in excluded:
        rec.update(status="excluded", problems=["file-access audit failed: answers ignored"])
        return None, rec
    if td.problems:
        rec.update(status="invalid", problems=["the planned task no longer matches its files: its answers are not "
                                               "used"] + list(td.problems))
        return None, rec
    if not p.is_file():
        rec.update(status="missing", problems=["answer file missing (task not answered)"])
        rec["unanswered"] = sorted(td.qids)
        return None, rec
    res = validate_answer_bytes(p.read_bytes(), td, strict_files=strict_files)
    rec.update(status=res["status"], n_valid=res["n_valid"], unanswered=res["unanswered"],
               rejected_entries=res["item_problems"], problems=res["file_problems"])
    if res["status"] == "invalid":
        return None, rec
    return res["entries"], rec


# ------------------------------------------------------------------------------------------------ task inventory
def _chunk_problems(root: Path, task: dict, chunk: dict) -> list:
    """The chunk the agent was given must still be the planned one (manifest sha256, header, key entries)."""
    probs = []
    man = _read_json(root / "manifest" / f"{task['batch_id']}.json")
    want = {x["task_id"]: x["sha256"] for x in man["tasks"]}.get(task["task_id"])
    if want != CH.sha(json.dumps(chunk, sort_keys=True, ensure_ascii=False)):
        probs.append("chunk file differs from its manifest sha256")
    if chunk.get("task_id") != task["task_id"] or chunk.get("kind") != task["kind"] \
            or chunk.get("prompt_sha") != task["prompt_sha"]:
        probs.append("chunk header differs from TASKS.json")
    if len(chunk["items"]) != task["n_items"]:
        probs.append("chunk item count differs from TASKS.json")
    key = _read_json(root / "key" / f"{task['batch_id']}.json")["key"]
    if {it["qid"] for it in chunk["items"]} - set(key):
        probs.append("an item has no key entry")
    return probs


def _task_def(rnd: str, root: Path, task: dict) -> TaskDef:
    chunk = _read_json(root / "chunks" / f"{task['task_id']}.json")
    items = {it["qid"]: it for it in chunk["items"]}
    td = TaskDef(rnd, task["task_id"], task["batch_id"], task["kind"],
                 value_key(task["kind"], task.get("track")), tuple(items), Path(task["answer_file"]), root=root)
    if task["kind"] == "extract_lex":
        td.choices = {q: tuple(it["choices"]) for q, it in items.items()}
    td.problems = _chunk_problems(root, task, chunk)
    return td


def _redo1_def(tid: str, qids: tuple, v1_task: dict) -> TaskDef:
    chunk = _read_json(HA.ROOT / "chunks" / f"{tid}.json")
    td = TaskDef("redo1", tid, v1_task["batch_id"], v1_task["kind"], value_key(v1_task["kind"], v1_task.get("track")),
                 tuple(qids), T.REDO1 / "answers" / f"{tid}.json", root=HA.ROOT)
    td.problems = _chunk_problems(HA.ROOT, v1_task, chunk)
    if set(qids) - {it["qid"] for it in chunk["items"]}:
        td.problems.append("a redo qid is not an item of the source chunk")
    md = T.REDO1 / f"{tid}.md"
    if not md.is_file():
        td.problems.append("the redo task file is missing")
    else:
        text = md.read_text(encoding="utf-8")
        named = REDO1_QID_RE.findall(text)
        if sorted(named) != sorted(qids):
            td.problems.append(f"the redo task file names {named}, the redo list is {list(qids)}")
        if str(td.answer_file) not in text:
            td.problems.append("the redo task file names another answer file")
    return td


def inventory() -> tuple:
    """([TaskDef] for every task of every round, [unrecognised round folders])."""
    defs = []
    man1 = _read_json(HA.ROOT / "TASKS.json")
    v1t = {t["task_id"]: t for t in man1["tasks"]}
    defs += [_task_def("v1-author", HA.ROOT, t) for t in man1["tasks"]]
    for tid, qids in T.REDO1_ITEMS.items():
        defs.append(_redo1_def(tid, tuple(qids), v1t[tid]))
    defs += [_task_def("v1-extract", EB.EXTRACT, t) for t in _read_json(EB.EXTRACT / "TASKS.json")["tasks"]]
    if (T.ROOT2 / "TASKS.json").is_file():
        defs += [_task_def("redo2", T.ROOT2, t) for t in _read_json(T.ROOT2 / "TASKS.json")["tasks"]]
    if (T.EXTRACT2 / "TASKS.json").is_file():
        defs += [_task_def("redo2-extract", T.EXTRACT2, t) for t in _read_json(T.EXTRACT2 / "TASKS.json")["tasks"]]
    unknown = [d.name for d in sorted(HAIKU.glob("redo*")) if d.is_dir() and d.name not in ("redo", "redo2")]
    return defs, unknown


def stray_answer_files(defs: list) -> list:
    known = {Path(d.answer_file).resolve() for d in defs}
    out = []
    for d in (HA.ROOT / "answers", EB.EXTRACT / "answers", T.REDO1 / "answers", T.ROOT2 / "answers",
              T.EXTRACT2 / "answers"):
        if d.is_dir():
            out += [rel(p) for p in sorted(d.iterdir()) if p.is_file() and p.resolve() not in known]
    return out


def validate_all(defs: list, excluded: set, strict_files: bool) -> tuple:
    """({(round, task id): valid entries}, [record], [excluded ids that name no task])."""
    valid, records = {}, []
    for td in defs:
        entries, rec = read_answer_file(td, excluded, strict_files)
        records.append(rec)
        if entries is not None:
            valid[(td.round, td.task_id)] = entries
    return valid, records, sorted(excluded - {d.task_id for d in defs})


# ------------------------------------------------------------------------------------------------ 2. pools from answers
def build_pools(valid: dict, rounds: tuple) -> dict:
    """haiku_author.load + topup.load, fed with the VALIDATED entries only (same order, same loader checks)."""
    manifest = _read_json(HA.ROOT / "TASKS.json")
    reg = HA.declare_lexicon(LexiconRegistry(F))
    pools = {"skins": {}, "attacks": {}, "wordings": {}, "packs_appr": [], "packs_agent": [], "names": [],
             "lexicon": reg}
    drops, missing, unanswered = [], [], {}
    for task in manifest["tasks"]:
        tid = task["task_id"]
        raw = valid.get(("v1-author", tid))
        if raw is None:
            missing.append(tid)
            continue
        b = HA._restore(task)
        got, probs = CH.load_answers(b, {tid: raw})
        drops += [(tid, "*", p) for p in probs if not p.endswith("item(s) unanswered")]
        inv = {v: k for k, v in b.key.items()}
        unanswered[tid] = sorted(set(b.key.values()) - set(got))
        items = CH.item_by_internal(b)
        for iid, a in sorted(got.items()):
            why = HA._load_one(task, iid.split("|"), items[iid], a, inv[iid], pools)
            if why:
                drops.append((tid, iid, why))
    v1_ids = {"skins": set(pools["skins"]), "attacks": set(pools["attacks"]), "wordings": set(pools["wordings"])}
    v1_forms = set(reg.forms)
    resolved, tasks2 = [], []
    if "redo1" in rounds:
        v1_tasks = {t["task_id"]: t for t in manifest["tasks"]}
        for tid, qids in T.REDO1_ITEMS.items():
            raw = valid.get(("redo1", tid))
            if raw is None:
                missing.append(f"{tid} (haiku/redo)")
                continue
            if any(a["qid"] in qids for a in valid.get(("v1-author", tid), [])):
                raise SystemExit(f"{tid}: the v1 answer already holds a redo qid; refusing to merge twice")
            T._load_task(HA.ROOT, v1_tasks[tid], raw, pools, drops, only_qids=set(qids), tag=":redo")
            b = HA._restore(v1_tasks[tid])
            unanswered[tid] = sorted(set(unanswered.get(tid, ())) - {b.key[q] for q in qids})
            resolved.append(tid)
    if "redo2" in rounds and (T.ROOT2 / "TASKS.json").is_file():
        tasks2 = _read_json(T.ROOT2 / "TASKS.json")["tasks"]
        for task in tasks2:
            raw = valid.get(("redo2", task["task_id"]))
            if raw is None:
                missing.append(task["task_id"])
                continue
            T._load_task(T.ROOT2, task, raw, pools, drops)
    return {"pools": pools, "drops": drops, "missing": missing, "v1_ids": v1_ids, "v1_forms": v1_forms,
            "resolved_by_redo": resolved, "tasks2": tasks2,
            "unanswered_items": {t: u for t, u in unanswered.items() if u}}


def record_reads(reg, batches: dict, valid: dict, rnd: str, manifest: dict) -> tuple:
    """GA._record fed with the validated entries. -> (counts per read, problems)."""
    raw_by_read = {}
    for read in batches:
        raw_by_read[read] = {t["task_id"]: valid[(rnd, t["task_id"])] for t in manifest["tasks"]
                             if t["read"] == read and (rnd, t["task_id"]) in valid}
    return GA._record(reg, batches, raw_by_read)


def admit(valid: dict, records: list, rounds: tuple, final: bool) -> dict:
    """The admission pipeline over the validated answers (topup.admit2 / glex_admit.admit, same order and checks)."""
    st = build_pools(valid, rounds)
    pools, drops = st["pools"], st["drops"]
    reg = pools["lexicon"]
    q_rows, answer_problems = [], []
    for tid, iid, why in drops:
        if iid == "*":
            answer_problems.append({"task": tid, "why": why})
        else:
            q_rows.append({"piece": f"{tid}|{iid}", "stage": "load:G-SL", "reason": why})
    q_rows += [{"piece": p, "stage": "value-lint", "reason": r} for p, r in EB.lint_pools(pools)]
    q_rows += [{"piece": p, "stage": "dedup", "reason": r} for p, r in T.dedup_merged(pools, st["v1_ids"])]

    v1_fids = T.v1_read_fids()
    man1 = _read_json(EB.EXTRACT / "TASKS.json")
    b1, p1 = GA._verify_reads(reg, v1_fids, man1)
    c1, rec1 = record_reads(reg, b1, valid, "v1-extract", man1)
    b2, p2, c2, rec2, new_fids, new_bad = {}, [], {}, [], [], []
    if "redo2-extract" in rounds:
        new_fids, new_bad = T.new_form_ids(st)
        man2_path = T.EXTRACT2 / "TASKS.json"
        man2 = _read_json(man2_path) if man2_path.is_file() else {"tasks": []}
        b2, p2 = T._verify_r2(reg, new_fids, man2)
        c2, rec2 = record_reads(reg, b2, valid, "redo2-extract", man2)
    reg.unit_test_all()

    status_of = {fid: reg.status(fid) for fid in sorted(reg.forms)}
    q_rows += GA._form_quarantine(reg)
    for sid, (_sk, fid) in sorted(pools["wordings"].items()):
        if status_of[fid] != "admitted":
            q_rows.append({"piece": f"wording|{sid}", "stage": "G-LEX", "status": status_of[fid],
                           "reason": f"form {fid} is {status_of[fid]}"})
    if final:      # the contract breaks of the answer files: provenance rows (v1 has none, so not in the v1 rebuild)
        for rec in records:
            reasons = list(rec["rejected_entries"]) + list(rec["problems"])
            if rec["unanswered"] and rec["status"] in ("partial", "invalid"):
                redo = " (re-asked in haiku/redo and answered)" if rec["task_id"] in st["resolved_by_redo"] else ""
                reasons.append(f"{len(rec['unanswered'])} item(s) unanswered{redo}")
            if rec["status"] != "valid" or reasons:
                for i, why in enumerate(reasons or [rec["status"]]):
                    q_rows.append({"piece": f"{rec['task_id']}|answer-file#{i}", "stage": "answer-contract",
                                   "status": rec["status"], "reason": why})
    sha = {rec["task_id"]: rec["sha256"] for rec in records if rec["sha256"] and rec["status"] in ("valid", "partial")}
    return {"pools": pools, "reg": reg, "status_of": status_of, "quarantine": q_rows,
            "answer_problems": answer_problems, "answer_sha": sha, "read_counts": {**c1, **c2},
            "batches": {**b1, **b2},
            "problems": {"rebuild_v1": p1, "rebuild_r2": p2, "record_v1": rec1, "record_r2": rec2,
                         "answer_drops": answer_problems, "missing_author_answers": st["missing"],
                         "unanswered_after_redo": st["unanswered_items"]},
            "new_unit_fail": new_bad, "resolved_by_redo": st["resolved_by_redo"], "new_forms": new_fids,
            "v1_fids": v1_fids, "tasks2": st["tasks2"]}


# ------------------------------------------------------------------------------------------------ files and audit
def pool_files(st: dict, final: bool) -> tuple:
    c = GA.counts(st)
    short = GA.shortfalls(c)
    files = GA._files(st, c, short)
    if final:       # pipeline.lex_problems needs a wording's own form id in lexicon_ids
        w = json.loads(files["wordings.json"])
        for rec in w["wordings"]:
            rec["lexicon_ids"] = [rec["form_id"]]
        files["wordings.json"] = dump(w)
    return files, c, short


def recount(files: dict) -> dict:
    """The counts GA.counts / GA.shortfalls need, recomputed from the frozen files alone."""
    sk = json.loads(files["skins.json"])["skins"] + json.loads(files["documents.json"])["documents"]
    per = {}
    for d in sorted(sk, key=lambda d: d["skin_id"]):
        cell = per.setdefault(f"{d['register']}|{d['track']}", {"T": 0, "F": 0, "total": 0})
        cell[d["author_mode"]] += 1
        cell["total"] += 1
    n_T, n_F = sum(v["T"] for v in per.values()), sum(v["F"] for v in per.values())
    lex = json.loads(files["lexicon.json"])
    packs = json.loads(files["packs.json"])
    wordings = json.loads(files["wordings.json"])["wordings"]
    adm = Counter(f["sem_id"] for f in lex["forms"] if f["kind"] == "comparator" and f["usable"])
    return {"skins_by_register_track": per, "skins_T": n_T, "skins_F": n_F, "skins_total": n_T + n_F,
            "mode_F_share": round(n_F / (n_T + n_F), 4) if n_T + n_F else None,
            "wordings_candidates": sum(1 for f in lex["forms"] if f["kind"] == "question"),
            "wordings_admitted": len(wordings),
            "comparator_admitted_by_sense": dict(sorted(adm.items())),
            "packs_appr": len(packs["appr"]), "packs_agent": len(packs["agent"]), "names": len(packs["names"])}


def skin_from_json(d: dict) -> K.Skin:
    def tup(x):
        return tuple(tup(i) for i in x) if isinstance(x, list) else x
    return K.Skin(skin_id=d["skin_id"], family=d["family"], text=d["text"], slots=tup(d["slots"]), kind=d["kind"],
                  register=d["register"], escape=d["escape"], counts=tup(d["counts"]), author_mode=d["author_mode"],
                  qform=d["qform"], brief=tup(d["brief"]), haiku_task_id=d["haiku_task_id"],
                  haiku_prompt_sha=d["haiku_prompt_sha"], lexicon_ids=tup(d["lexicon_ids"]), held_out=d["held_out"])


def audit_files(files: dict, st: dict, c: dict, short: list) -> dict:
    """Read the frozen files back (as the generator would) and re-run the gates on what is there. -> {"problems",
    "used_forms", "gate_used", "gate_registry", "registry"}."""
    probs = []
    lex = json.loads(files["lexicon.json"])
    reg = LexiconRegistry.from_json(lex)            # unit tests re-run; statuses recomputed from the stored votes
    status = {fid: reg.status(fid) for fid in reg.forms}
    for f in lex["forms"]:
        if status[f["form_id"]] != f["status"] or f["usable"] != (f["status"] == "admitted"):
            probs.append(f"lexicon.json: {f['form_id']} status / usable flag differs from its votes")
        if status[f["form_id"]] != st["status_of"].get(f["form_id"]):
            probs.append(f"lexicon.json: {f['form_id']} status differs from the in-memory admission")
        need = 3 if f["kind"] in STRICT_KINDS else 2
        if f["status"] == "admitted" and len({e for e, _ in f["extractions"]}) < need:
            probs.append(f"{f['form_id']}: admitted with fewer than {need} distinct reads")
    wordings = json.loads(files["wordings.json"])["wordings"]
    used = {w["form_id"] for w in wordings} | {f["form_id"] for f in lex["forms"]
                                               if f["kind"] == "comparator" and f["usable"]}
    gate_used = reg.gate(used)
    gate_all = reg.gate()
    if not gate_used["pass"]:
        probs.append(f"G-LEX: used forms not admitted: {sorted(gate_used['not_admitted'])[:3]}")
    for w in wordings:
        fid = w["form_id"]
        f = reg.forms.get(fid)
        if f is None or f.sem_id != question_sem(F, w["qform"]) or f.text != w["text"] or w["sense"] != f.sem_id:
            probs.append(f"wordings.json: {w['skin_id']} does not match its lexicon form")
        if w.get("lexicon_ids") != [fid]:
            probs.append(f"wordings.json: {w['skin_id']} lexicon_ids differ from its form id")
    # G-SL once more, on the pieces as the generator would load them
    for key, bucket, nm in (("skins", "skins", "skin"), ("attack", "attacks", "attack")):
        for d in json.loads(files[f"{key}.json"])[bucket]:
            sk = skin_from_json(d)
            bad = HA._lint_skin(sk, d["track"])
            if bad:
                probs.append(f"{nm} {d['skin_id']}: G-SL {bad[:1]}")
    for d in json.loads(files["documents.json"])["documents"]:
        sk = skin_from_json(d)
        facts = dict(sk.brief)
        bad = [f"{v.rule}: {v.detail}" for v in gsl.lint_freeform(sk.text, facts, label_words=P.T31.LABEL_WORDS)]
        if sk.text.count(facts["ITEM"]) != 1 or sk.text.count(facts["REQ_ID"]) != 1:
            bad.append("item or code not exactly once")
        if bad:
            probs.append(f"document {d['skin_id']}: G-SL {bad[:1]}")
    for d in wordings:
        sk = skin_from_json(d)
        bad = [f"{v.rule}: {v.detail}" for v in gsl.lint_template(sk, label_words=P.T31.LABEL_WORDS,
                                                                    exceptions=P.T31.GSL_EXCEPTIONS,
                                                                    name_allow=P.T31.NAME_ALLOW)]
        k = HA.negcount.count(K.PH_RE.sub("X", sk.text))
        if (k.k_syn, k.k_all) != HA.NEG_COUNTS[sk.qform]:
            bad.append(f"negation counts {(k.k_syn, k.k_all)}")
        if bad:
            probs.append(f"wording {d['skin_id']}: G-SL {bad[:1]}")
    rc = recount(files)
    for k in ("skins_by_register_track", "skins_T", "skins_F", "mode_F_share", "wordings_candidates",
              "wordings_admitted", "comparator_admitted_by_sense", "packs_appr", "packs_agent", "names"):
        if rc[k] != c[k]:
            probs.append(f"recount from the frozen files: {k} {rc[k]} != in-memory {c[k]}")
    if GA.shortfalls(rc) != short:
        probs.append(f"recount from the frozen files: shortfalls {GA.shortfalls(rc)} != {short}")
    return {"problems": probs, "used_forms": sorted(used), "gate_used": gate_used, "gate_registry": gate_all,
            "registry": reg, "recount": rc}


def v1_integrity(valid: dict, records: list) -> dict:
    """v1 rebuilt from the validated v1 answers must equal the frozen pools/ (and the files on disk) byte for byte."""
    st = admit(valid, records, ("v1-author", "v1-extract"), final=False)
    files, _c, _short = pool_files(st, final=False)
    man = _read_json(POOLS_V1 / "MANIFEST.json")
    probs = []
    for name, text in sorted(files.items()):
        want = man["sha256"].get(name)
        if sha_bytes(text.encode("utf-8")) != want:
            probs.append(f"{name}: the v1 rebuild differs from pools/MANIFEST.json")
        if not (POOLS_V1 / name).is_file() or sha_file(POOLS_V1 / name) != want:
            probs.append(f"{name}: pools/{name} on disk differs from pools/MANIFEST.json")
    if set(man["sha256"]) != set(files):
        probs.append(f"pools/MANIFEST.json lists {sorted(man['sha256'])}, the rebuild makes {sorted(files)}")
    for read, r in man["reads"].items():
        for tid, want in r["tasks"].items():
            p = EB.EXTRACT / "answers" / f"{tid}.json"
            if not p.is_file() or sha_file(p) != want:
                probs.append(f"{tid}: v1 read answer differs from pools/MANIFEST.json")
    for k in ("rebuild_v1", "rebuild_r2", "record_v1", "record_r2", "answer_drops", "missing_author_answers"):
        if st["problems"][k]:
            probs.append(f"v1 rebuild reports {k}: {str(st['problems'][k])[:120]}")
    return {"manifest_sha256": sha_file(POOLS_V1 / "MANIFEST.json"), "version": man["version"], "problems": probs,
            "ok": not probs, "files": {n: sha_bytes(t.encode("utf-8")) for n, t in sorted(files.items())}}


def rebuild_checks() -> list:
    """The planned authoring batches (v1 and redo2) rebuilt in memory must equal the files on disk."""
    probs = []
    files, _m = HA.files_for(HA.build_batches())
    probs += [f"v1 authoring: {r} differs from disk" for r, t in sorted(files.items())
              if not (HA.ROOT / r).is_file() or (HA.ROOT / r).read_text(encoding="utf-8") != t]
    if (T.ROOT2 / "TASKS.json").is_file():
        files2, _m2 = T.files_for2(T.build_batches2())
        probs += [f"redo2 authoring: {r} differs from disk" for r, t in sorted(files2.items())
                  if not (T.ROOT2 / r).is_file() or (T.ROOT2 / r).read_text(encoding="utf-8") != t]
    return probs


# ------------------------------------------------------------------------------------------------ assemble
def impact_without(valid: dict) -> dict:
    """What the loaders accept from the usable answers only, before G-LEX (an upper bound): wording candidates per
    question form and skins per (register, track) cell."""
    pools = build_pools(valid, ALL_ROUNDS)["pools"]
    cells = Counter(f"{sk.register}|{sid.split('-')[1]}" for sid, sk in pools["skins"].items())
    return {"wording_candidates_by_qform": dict(sorted(Counter(sk.qform for sk, _f in pools["wordings"].values()).items())),
            "wording_candidates": len(pools["wordings"]), "skins": len(pools["skins"]),
            "min_skins_per_cell": min(cells.values()) if cells else 0,
            "packs": [len(pools["packs_appr"]), len(pools["packs_agent"])], "names": len(pools["names"])}


def assemble(*, exclude: tuple = (), strict_files: bool = False) -> dict:
    excluded = set(exclude)
    defs, unknown_dirs = inventory()
    valid, records, bad_excl = validate_all(defs, excluded, strict_files)
    blockers, notes = [], []
    if bad_excl:
        blockers.append(f"--exclude-task names no task: {bad_excl}")
    if sha_file(G0) != P.POOL_G0_SHA256:
        blockers.append("G0_SPEC.md no longer matches the sha256 pinned in plugin.py")
    kinds = {d.kind for d in defs}
    if kinds - set(HANDLED_KINDS):
        blockers.append(f"task kinds with no ingest path: {sorted(kinds - set(HANDLED_KINDS))}")
    for rec in records:
        if rec["plan_problems"]:
            blockers.append(f"{rec['task_id']}: planned task does not match its files: {rec['plan_problems'][0]}")

    # a v1 file that is not usable removes v1 pieces (and the forms the v1 reads were planned for): pools_v2 would no
    # longer be v1 + redo, so nothing is rebuilt; the impact is measured on the pieces that would remain
    v1_bad = [r for r in records if r["round"] in V1_ROUNDS and r["status"] in ("invalid", "missing")]
    if v1_bad:
        blockers += [f"{r['round']} answer {r['task_id']} is {r['status']}: {(r['problems'] or r['rejected_entries'] or ['?'])[0]}"
                     for r in v1_bad]
        return {"early": True, "records": records, "blockers": blockers, "notes": notes, "ready": False,
                "strict_files": strict_files, "excluded": sorted(excluded), "unknown_dirs": unknown_dirs,
                "stray": stray_answer_files(defs), "impact": impact_without(valid)}

    # v1 reproduces (validated v1 answers only)
    integ = v1_integrity(valid, records)
    blockers += [f"v1: {p}" for p in integ["problems"]]
    blockers += [f"rebuild: {p}" for p in rebuild_checks()]
    for rec in records:
        if rec["round"] in V1_ROUNDS and rec["status"] == "excluded":
            notes.append(f"v1 task {rec['task_id']} excluded (audit failed): v1 pieces from it are not in pools_v2")

    # the full admission
    st = admit(valid, records, ALL_ROUNDS, final=True)
    for k in ("rebuild_v1", "rebuild_r2"):
        blockers += [f"{k}: {p}" for p in st["problems"][k]]
    files, c, short = pool_files(st, final=True)
    aud = audit_files(files, st, c, short)
    blockers += [f"final audit: {p}" for p in aud["problems"]]
    if st["new_unit_fail"]:
        notes.append(f"{len(st['new_unit_fail'])} new form(s) fail their unit test: {st['new_unit_fail'][:2]}")
    strict_forms = [f for f in st["reg"].forms.values() if f.kind in STRICT_KINDS]
    reg_status = Counter(st["status_of"].values())
    pending = sorted(f for f, s in st["status_of"].items() if s in ("pending", "untested"))
    lex_short = [s for s in short if s.startswith(("wordings", "comparator"))]
    gates = {
        "G-LEX": {
            "rule": "unit test + >= 2 distinct independent reads that all pick the declared sem (3 for precedence / "
                    "window kinds); any other pick or null rejects the form for good",
            "scope": "every form a pool piece uses (kit: lexicon.py G-LEX, README gates table)",
            "required_reads": {"comparator": 2, "question": 2, "precedence": 3, "window": 3},
            "strict_kind_forms": len(strict_forms),
            "used_forms": len(aud["used_forms"]),
            "used_forms_gate": {k: v for k, v in aud["gate_used"].items() if k != "not_admitted"},
            "registry_gate_informational": {k: v for k, v in aud["gate_registry"].items() if k != "not_admitted"},
            "registry_not_admitted": dict(sorted(aud["gate_registry"]["not_admitted"].items())),
            "registry_status_counts": dict(sorted(reg_status.items())),
            "pending_forms": pending,
            "every_not_admitted_form_is_excluded": not (set(aud["gate_registry"]["not_admitted"])
                                                        & set(aud["used_forms"])),
            "lexicon_shortfalls": lex_short,
            "pass": bool(aud["gate_used"]["pass"] and not lex_short)},
        "G-SL": "applied at load to every piece (haiku_author._load_one) and again to the pieces read back from the "
                "frozen files (audit_files); value lint on packs and names (extract_build.lint_pools)",
        "G3-H": "not a pool-stage gate for T31 (G0 section 7; README; extract_build.py): no round holds an extract_g3h "
                "task, so there are no G3-H votes to record; it runs at the pilot and on full generation",
        "G13_seed": "not run (6.4 step 4)",
        "G2_G4_G-TW": "not run at pool stage (rows only)"}
    ready = bool(not short and gates["G-LEX"]["pass"] and not blockers)
    return {"defs": defs, "records": records, "valid": valid, "st": st, "files": files, "c": c, "short": short,
            "gates": gates, "ready": ready, "blockers": blockers, "notes": notes, "audit": aud, "integrity": integ,
            "unknown_dirs": unknown_dirs, "stray": stray_answer_files(defs), "strict_files": strict_files,
            "excluded": sorted(excluded), "pending": pending}


# ------------------------------------------------------------------------------------------------ manifest
def validation_report(a: dict) -> dict:
    recs = a["records"]
    by = Counter((r["round"], r["status"]) for r in recs)
    return {"family": F, "version": VERSION,
            "contract": "UTF-8 JSON list of objects with exactly {qid, text | pack | names | choice}; every qid one of "
                        "the task's own items, none repeated; a G-LEX choice null or copied exactly from the item's "
                        "listed meanings. Whole-file breaks reject the file; entry breaks reject that entry (an "
                        "unanswered item, never a vote or a piece). Nothing is edited.",
            "file_policy": "strict (whole file on any break)" if a["strict_files"] else "items (kit chunker rule)",
            "excluded_tasks_audit_failed": a["excluded"],
            "summary": {f"{r}/{s}": n for (r, s), n in sorted(by.items())},
            "files_total": len(recs), "files_valid": sum(1 for r in recs if r["status"] == "valid"),
            "files_with_findings": [r for r in recs if r["status"] != "valid"],
            "stray_files_not_used": a["stray"], "unrecognised_round_folders": a["unknown_dirs"], "files": recs}


def manifest_obj(a: dict, files: dict) -> dict:
    st, c, short = a["st"], a["c"], a["short"]
    g0_sha = sha_file(G0)
    v1_man = POOLS_V1 / "MANIFEST.json"
    prev = ARCHIVE / "MANIFEST.json" if (ARCHIVE / "MANIFEST.json").is_file() else POOLS_V2 / "MANIFEST.json"
    remaining = list(short)
    if a["pending"]:
        remaining.append(f"{len(a['pending'])} form(s) wait for 2 independent G-LEX reads: {a['pending'][:3]}")
    if a["ready"]:
        status = ("READY: every G0 minimum met and the G-LEX gate passes on every form the pools use "
                  f"({len(a['audit']['used_forms'])} used forms, all admitted 2/2). G13-seed and row generation not run.")
    elif a["blockers"]:
        status = "BLOCKED: " + "; ".join(a["blockers"][:3])
    else:
        status = "SHORT: " + "; ".join(remaining) + ". Targets are not lowered. G13-seed and row generation not run."
    by = Counter((r["round"], r["status"]) for r in a["records"])
    return {
        "family": F, "version": VERSION, "revision": REVISION, "ready": a["ready"], "status": status,
        "supersedes": {"v1": {"path": "families/T31/pools/MANIFEST.json", "sha256": sha_file(v1_man)},
                       "partial_v2": {"path": "families/T31/pools_v2_a2_partial/MANIFEST.json",
                                      "sha256": sha_file(prev) if prev.is_file() else None,
                                      "note": "the A2 freeze written before the top-up G-LEX reads were answered; "
                                              "archived, not deleted"}},
        "v1_integrity": {"reproduced_by_rebuild": a["integrity"]["ok"], "problems": a["integrity"]["problems"]},
        "promote": "Nothing in the T31 code reads a pool path (no path to refresh). Use freeze_v2.load_pools() / "
                   "kit_ctx(), or (owner ruling) move pools/ to pools_v1/ and pools_v2/ to pools/ (g13_c2 reads "
                   "families/T31/pools/).",
        "g0": {"path": "families/T31/G0_SPEC.md", "sha256": g0_sha, "matches_plugin_pin": g0_sha == P.POOL_G0_SHA256},
        "sources": {"v1_author": "haiku/author/", "v1_reads": "haiku/extract/", "v1_redo": sorted(T.REDO1_ITEMS),
                    "redo2_author": "haiku/redo2/", "redo2_reads": "haiku/redo2/extract/",
                    "resolved_by_redo": st["resolved_by_redo"]},
        "answer_files": {"policy": "strict" if a["strict_files"] else "items",
                         "total": len(a["records"]), "by_round_status": {f"{r}/{s}": n for (r, s), n in sorted(by.items())},
                         "excluded_tasks_audit_failed": a["excluded"],
                         "with_findings": [{"task_id": r["task_id"], "round": r["round"], "status": r["status"],
                                            "rejected_entries": r["rejected_entries"], "unanswered": r["unanswered"],
                                            "problems": r["problems"]} for r in a["records"] if r["status"] != "valid"],
                         "detail": "VALIDATION_REPORT.json"},
        "reads": {read: {"batch_id": b.batch_id, "prompt_sha": b.prompt_sha,
                         "tasks": {tid: st["answer_sha"][tid] for tid in sorted(st["answer_sha"])
                                   if tid.startswith(b.batch_id)}}
                  for read, b in sorted(st["batches"].items())},
        "answer_reads": st["read_counts"],
        "gates": a["gates"],
        "problems": {"blocking": a["blockers"], "notes": a["notes"], **st["problems"],
                     "final_audit": a["audit"]["problems"]},
        "counts": c, "targets_g0": G0_TARGETS, "shortfalls": short, "remaining_work": remaining,
        "skins_by_register": {r: sum(v["total"] for k, v in c["skins_by_register_track"].items()
                                     if k.split("|")[0] == r) for r in sorted({k.split("|")[0]
                                                                              for k in c["skins_by_register_track"]})},
        "quarantine_rows": len(st["quarantine"]),
        "quarantine_by_stage": dict(sorted(Counter(q["stage"] for q in st["quarantine"]).items())),
        "load_notes": {"wordings.json": "each wording record carries lexicon_ids = [form_id] (pipeline.lex_problems "
                                        "checks the row's wording against an admitted form of its question form)",
                       "lexicon.json": "every form with its votes; usable = admitted. Rejected forms stay (no re-vote)"},
        "sha256": {name: sha_bytes(text.encode("utf-8")) for name, text in sorted(files.items())},
        "note_manifest": "sha256 of every other file in pools_v2/ (this file is not hashed)"}


def build_files(a: dict) -> dict:
    files = dict(a["files"])
    files["VALIDATION_REPORT.json"] = dump(validation_report(a))
    files["MANIFEST.json"] = dump(manifest_obj(a, files))
    return files


# ------------------------------------------------------------------------------------------------ writing
def plan_write(existing: dict, new_files: dict, existing_manifest: dict | None, archive_nonempty: bool) -> dict:
    """Pure: what a write over an existing pools_v2/ would do. -> {"archive": {name: text}, "problems": [...]}.
    An existing partial freeze is archived first (copied, never deleted); a READY one is never replaced."""
    probs = []
    status = str((existing_manifest or {}).get("status", ""))
    if existing_manifest is not None and (existing_manifest.get("ready") is True or status.startswith(("READY", "FROZEN"))):
        probs.append("pools_v2/ is already READY: refusing to replace it")
    if existing:
        if archive_nonempty:
            probs.append("the archive folder pools_v2_a2_partial/ already holds files: refusing to overwrite it")
        stale = sorted(set(existing) - set(new_files))
        if stale:
            probs.append(f"pools_v2/ holds files the new freeze does not write ({stale}): nothing is deleted")
    return {"archive": dict(existing), "problems": probs}


def write_pools_v2(files: dict) -> dict:
    existing = {p.name: p.read_text(encoding="utf-8") for p in sorted(POOLS_V2.iterdir()) if p.is_file()} \
        if POOLS_V2.is_dir() else {}
    man = json.loads(existing["MANIFEST.json"]) if "MANIFEST.json" in existing else None
    plan = plan_write(existing, files, man, ARCHIVE.is_dir() and any(ARCHIVE.iterdir()))
    if plan["problems"]:
        raise SystemExit("; ".join(plan["problems"]))
    if plan["archive"]:
        for name, text in sorted(plan["archive"].items()):
            paths.write_text(ARCHIVE / name, text)
    for name, text in sorted(files.items()):
        if name != "MANIFEST.json":
            paths.write_text(POOLS_V2 / name, text)
    paths.write_text(POOLS_V2 / "MANIFEST.json", files["MANIFEST.json"])         # last: a manifest means a complete set
    return {"archived": sorted(plan["archive"]), "written": sorted(files)}


def _early_out(a: dict) -> dict:
    by = Counter((r["round"], r["status"]) for r in a["records"])
    return {"status": "BLOCKED: " + "; ".join(a["blockers"][:3]), "ready": False, "written": False,
            "policy": "strict" if a["strict_files"] else "items", "excluded_tasks": a["excluded"],
            "blockers": a["blockers"],
            "answer_files": {f"{r}/{s}": n for (r, s), n in sorted(by.items())},
            "answer_files_with_findings": [{"task_id": r["task_id"], "round": r["round"], "status": r["status"],
                                            "rejected_entries": r["rejected_entries"], "unanswered": r["unanswered"],
                                            "problems": r["problems"]} for r in a["records"] if r["status"] != "valid"],
            "impact_of_the_unusable_input": a["impact"], "stray_files": a["stray"],
            "unrecognised_round_folders": a["unknown_dirs"]}


def run(write: bool, *, exclude: tuple = (), strict_files: bool = False) -> dict:
    a = assemble(exclude=exclude, strict_files=strict_files)
    if a.get("early"):
        if write:
            raise SystemExit("blocking problems, nothing written: " + "; ".join(a["blockers"][:4]))
        return _early_out(a)
    files = build_files(a)
    man = json.loads(files["MANIFEST.json"])
    out = {"status": man["status"], "ready": a["ready"], "written": False, "policy": man["answer_files"]["policy"],
           "excluded_tasks": a["excluded"], "shortfalls": a["short"], "blockers": a["blockers"],
           "remaining_work": man["remaining_work"], "notes": a["notes"],
           "answer_files": man["answer_files"]["by_round_status"],
           "answer_files_with_findings": man["answer_files"]["with_findings"],
           "gates": a["gates"], "answer_reads": man["answer_reads"],
           "counts": {k: v for k, v in a["c"].items() if k != "skins_by_register_track"},
           "skins_by_register": man["skins_by_register"],
           "min_skins_per_cell": {
               "training": min(v["total"] for k, v in a["c"]["skins_by_register_track"].items()
                               if k.split("|")[0] in GA.TRAIN_REGISTERS),
               "held_out": min(v["total"] for k, v in a["c"]["skins_by_register_track"].items()
                               if k.split("|")[0] in GA.HELD_REGISTERS)},
           "quarantine_rows": man["quarantine_rows"], "quarantine_by_stage": man["quarantine_by_stage"],
           "problems": man["problems"], "stray_files": a["stray"], "unrecognised_round_folders": a["unknown_dirs"],
           "files": sorted(files)}
    if write:
        if a["blockers"]:
            raise SystemExit("blocking problems, nothing written: " + "; ".join(a["blockers"][:4]))
        out.update(write_pools_v2(files))
        out["written"] = True
    return out


# ------------------------------------------------------------------------------------------------ loading pools_v2
def pools_from_files(files: dict) -> dict:
    """The pool files (name -> JSON text) as objects: {"skins": {id: Skin}, "documents": {id: Skin}, "attacks": {id:
    Skin}, "wordings": {id: Skin} (admitted only; lexicon_ids = (form id,)), "wording_forms": {id: form id},
    "packs_appr", "packs_agent", "names", "lexicon": LexiconRegistry (every form with its votes), "manifest": dict
    or None}."""
    def j(name):
        return json.loads(files[name])
    wordings, wform = {}, {}
    for d in j("wordings.json")["wordings"]:
        sk = skin_from_json({**d, "lexicon_ids": [d["form_id"]]})
        wordings[sk.skin_id] = sk
        wform[sk.skin_id] = d["form_id"]
    packs = j("packs.json")
    return {"skins": {d["skin_id"]: skin_from_json(d) for d in j("skins.json")["skins"]},
            "documents": {d["skin_id"]: skin_from_json(d) for d in j("documents.json")["documents"]},
            "attacks": {d["skin_id"]: skin_from_json(d) for d in j("attack.json")["attacks"]},
            "wordings": wordings, "wording_forms": wform, "packs_appr": packs["appr"], "packs_agent": packs["agent"],
            "names": packs["names"], "lexicon": LexiconRegistry.from_json(j("lexicon.json")),
            "manifest": j("MANIFEST.json") if "MANIFEST.json" in files else None}


def load_pools(root: Path = POOLS_V2) -> dict:
    """pools_from_files over the files of a freeze folder (default pools_v2/)."""
    root = Path(root)
    return pools_from_files({p.name: p.read_text(encoding="utf-8") for p in sorted(root.iterdir())
                             if p.is_file() and p.suffix == ".json"})


def kit_ctx(pools: dict) -> KitCtx:
    """A KitCtx over the frozen pieces (skins, Mode F documents, attack lines, admitted wordings) and the registry."""
    sk = {}
    for k in ("skins", "documents", "attacks", "wordings"):
        sk.update(pools[k])
    return KitCtx(skins=sk, lexicon=pools["lexicon"])


# ------------------------------------------------------------------------------------------------ CLI
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=("check", "freeze"))
    ap.add_argument("--exclude-task", action="append", default=[], help="a task id whose audit failed (repeatable)")
    ap.add_argument("--strict-files", action="store_true", help="reject a whole file on any contract break")
    a = ap.parse_args(argv)
    out = run(write=(a.cmd == "freeze"), exclude=tuple(a.exclude_task), strict_files=a.strict_files)
    print(json.dumps(out, indent=1, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())

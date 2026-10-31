"""transfer/T36/freeze_v2.py: T36 pool freeze-v2 (G0_SPEC.md v2.1 sections 6 and 7; C2_DATA_SPEC 6.2, 6.3; PREREG A37, A38).

Why this file exists. freeze.py (v1) reads haiku/author/ and haiku/extract/ only. admit.py (a later step) adds the
Mode T pieces of the two redo rounds, but it ignores Mode F: a round 2 document is admitted only after its own G3-H
read (haiku/redo2/extract/), and no step turned those reads into pool documents (redo2.py g3h-check only counts).
This script is that step, and it checks every answer file of every round before anything is used. It changes nothing
that exists: pools/ (v1), every answer file, every plan file and all pinned code stay as they are. It writes only
pools_v2/.

  check    in memory: validate every answer file, rebuild v1, fold in the redo pieces, record every G-LEX and G3-H
           vote, apply every gate, print the status (READY or SHORT) and every shortfall. Writes nothing.
  freeze   the same, then write transfer/T36/pools_v2/ through paths.write_files (refuses before A38 and on never-open
           paths): skins.json, attacks.json, documents.json, wordings.json, lexicon.json, packs.json, quarantine.json,
           g3h_votes.json, validation_report.json, MANIFEST.json. Refuses when pools_v2/MANIFEST.json already exists
           with other content, and when a blocking problem exists. Reads the files back and re-checks v1.

Run from lean/c2_build with the project python:
  ../../.venv/bin/python -B -m transfer.T36.freeze_v2 check  [--exclude-task NAME]...
  ../../.venv/bin/python -B -m transfer.T36.freeze_v2 freeze [--exclude-task NAME]...
--exclude-task takes the label "<round>:<task>" (rounds: v1-author, v1-extract, redo1, redo2, redo2-g3h) or a bare task
name that is unique across rounds. Name here the answer files whose file-access audit failed; their votes and pieces
are not used (nothing is edited). The list handed to this step was empty, so none is excluded by default.

What it does, in order (no label is set anywhere; Haiku answers only flag):
  1. Contract check of EVERY answer file of every round (33 files: author v1, extract v1, redo, redo2, redo2 G3-H).
     A file is valid only when it is UTF-8 JSON, one array of objects with EXACTLY the contract keys (qid + text | texts
     | meaning | project + person | project + packages + people), every qid from its own task, none twice, every item
     answered, strings non-empty, a redo2 item with exactly n different texts, a G-LEX meaning copied exactly from the
     item's choices. An invalid, missing or excluded file is rejected whole and never edited; its votes and pieces are
     not used. A v1 authoring file that is not valid blocks the freeze (v1 could not be reproduced).
  2. v1 is rebuilt (freeze.rebuild) and must reproduce the files of pools/: the same builder, run without the round 2
     Mode F documents, gives byte-identical skins, attacks, documents, wordings, lexicon and packs (sha256 equals
     pools/MANIFEST.json and the file on disk). Every v1 piece is carried over unchanged.
  3. Mode T redo pieces: round 1 (haiku/redo, one text per item) and round 2 (haiku/redo2, 3 candidates per item, the
     first that passes). Each goes through redo2.lint_piece (authoring lint, extract.extra_lint, H32 slot check) and
     the normalised dedup against everything authored before it.
  4. G-LEX: freeze.record_glex on the valid read files (extractor = the Haiku task). The kit rule decides: unit test
     passes and 2 distinct extractors all pick the sem (3 for kinds precedence and window; T36 has none); one other
     pick rejects for good; fewer reads stay pending and the form is not used.
  5. G3-H: freeze.g3h_compare on the round 1 documents; for round 2, every lint-clean Mode F candidate is compared
     (g3h.compare, exact) with the generator facts from the read that saw exactly that text (text sha and chunk text are
     checked). Template = the document; template_report at 98%. Per item the first candidate in written order that
     passes lint and G3-H is kept, the rest are discarded (G0 section 6).
  6. Packs (same seeded split as v1), H32, the Mode F cap (1 per 3 Mode T skins of the same held-out status), unique
     texts across all pools, a final lint of every skin, attack line and document, then the G0 targets of
     freeze.TARGETS (imported, never lowered).

READY means: no G0 shortfall, the G-LEX gate passes on every form the pool uses, every kept document passed G3-H, v1 is
reproduced and carried over, and no blocking problem. Otherwise SHORT, with the exact shortfalls. G13-seed (6.3) and
the transcript audits (c2_kit/audit.py; transcripts sit under never-open paths) are NOT run here.

How the generator loads pools_v2. Nothing in the family code (plugin.py, solver_b.py, fixtures.py) reads a pool path:
T36Plugin takes its packs through the constructor and the skins, wordings and lexicon through the KitCtx. freeze.py's
loader has a root argument, so no code needs a new path:
    from transfer.T36 import freeze_v2
    ctx, packs = freeze_v2.load_pools_v2()                 # = freeze.load_pools(pools_v2/)
    plugin = freeze_v2.make_plugin()                       # T36Plugin(lexicon=ctx.lexicon, packs=packs), ctx
g13_c2.py (pinned) reads only <block dir>/pools/, so G13-seed over pools_v2 needs the pools promoted by directory move
(pools/ -> pools_v1/, pools_v2/ -> pools/, the T31 precedent) after the owner rules it. Not done here; v1 stays put.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import re  # noqa: E402
from collections import Counter  # noqa: E402
from dataclasses import dataclass, field  # noqa: E402
from pathlib import Path  # noqa: E402

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, g3h, gsl, paths  # noqa: E402
from c2_kit import lexicon as LX  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit.plugin import KitCtx  # noqa: E402
from transfer.T36 import authoring as A  # noqa: E402
from transfer.T36 import extract as E  # noqa: E402
from transfer.T36 import freeze as F  # noqa: E402
from transfer.T36 import plugin as P  # noqa: E402
from transfer.T36 import redo2 as R  # noqa: E402

FAMILY = P.FAMILY
VERSION = "v2"
HAIKU = HERE / "haiku"
POOLS_V1 = F.POOLS
POOLS_V2 = HERE / "pools_v2"
TARGETS = F.TARGETS                      # the v1 targets (G0_SPEC.md section 6), imported and never changed
G3H_BAR = g3h.PASS_RATE                  # 0.98, never loosened
MODE_T, MODE_F = R.MODE_T, R.MODE_F
ROUNDS = ("v1-author", "v1-extract", "redo1", "redo2", "redo2-g3h")
KEYS = {"author_pack": frozenset({"qid", "project", "packages", "people"}),
        "author_skin": frozenset({"qid", "text"}), "author_freeform": frozenset({"qid", "text"}),
        "author_wording": frozenset({"qid", "text"}),
        "extract_lex": frozenset({"qid", "meaning"}), "extract_g3h": frozenset({"qid", "project", "person"})}
REDO2_KEYS = frozenset({"qid", "texts"})
V1_POOL_FILES = ("skins.json", "attacks.json", "documents.json", "wordings.json", "lexicon.json", "packs.json")
CONTRACT_TEXT = ("UTF-8 JSON, one array; objects with exactly qid + (text | texts[n different] | meaning | "
                 "project+person | project+packages[3]+people[2]); qids from the task's own item list, none twice, all "
                 "answered; strings non-empty; a G-LEX meaning copied exactly from the item's choices")


class Blocked(Exception):
    """A problem that stops the freeze (v1 cannot be reproduced or a plan drifted)."""


# ------------------------------------------------------------------------------------------------ small helpers

def _sha(s) -> str:
    return hashlib.sha256(s if isinstance(s, bytes) else str(s).encode("utf-8")).hexdigest()


def _json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _norm(s) -> str:
    return " ".join(str(s).casefold().split())


def _rel(p) -> str:
    try:
        return Path(p).resolve().relative_to(C2_BUILD).as_posix()
    except ValueError:
        return str(p)


# ------------------------------------------------------------------------------------------------ 1. tasks and contracts

@dataclass
class Task:
    round: str
    name: str
    kind: str
    answer_file: Path
    qids: tuple
    keys: frozenset
    n_texts: int = 0                                    # redo2: candidates per item
    choices: dict = field(default_factory=dict)         # extract_lex: qid -> allowed meanings
    meta: dict = field(default_factory=dict)            # the task's row in its index

    @property
    def label(self) -> str:
        return f"{self.round}:{self.name}"


def _chunk_qids(chunk_file: Path) -> tuple:
    return tuple(it["qid"] for it in _json(chunk_file)["items"])


def discover_tasks(haiku: Path = HAIKU) -> list:
    """Every task of every round with its answer file and its contract, from the indexes and chunk files on disk."""
    out = []
    root = haiku / "author"
    for t in _json(root / "TASKS.json")["tasks"]:
        out.append(Task("v1-author", t["task_id"], t["kind"], root / "answers" / f"{t['task_id']}.json",
                        _chunk_qids(root / "chunks" / f"{t['task_id']}.json"), KEYS[t["kind"]], meta=t))
    root = haiku / "extract"
    for t in _json(root / "TASKS.json")["tasks"]:
        chunk = _json(root / "chunks" / f"{t['task_id']}.json")
        choices = ({it["qid"]: tuple(it["choices"]) for it in chunk["items"]} if t["kind"] == "extract_lex" else {})
        out.append(Task("v1-extract", t["task_id"], t["kind"], root / "answers" / f"{t['task_id']}.json",
                        tuple(it["qid"] for it in chunk["items"]), KEYS[t["kind"]], choices=choices, meta=t))
    root = haiku / "redo"
    for t in _json(root / "REDO_INDEX.json")["tasks"]:
        out.append(Task("redo1", t["name"], t["author_kind"], root / "answers" / f"{t['name']}.json",
                        tuple(t["qids"]), KEYS[t["author_kind"]], meta=t))
    root = haiku / "redo2"
    for t in _json(root / "REDO2_INDEX.json")["tasks"]:
        out.append(Task("redo2", t["name"], t["author_kind"], root / "answers" / f"{t['name']}.json",
                        tuple(t["qids"]), REDO2_KEYS, n_texts=t["n_candidates"], meta=t))
    root = haiku / "redo2" / "extract"
    for t in _json(root / "TASKS.json")["tasks"]:
        out.append(Task("redo2-g3h", t["task_id"], t["kind"], root / "answers" / f"{t['task_id']}.json",
                        _chunk_qids(root / "chunks" / f"{t['task_id']}.json"), KEYS[t["kind"]], meta=t))
    return out


def _no_dup_pairs(pairs):
    d = {}
    for k, v in pairs:
        if k in d:
            raise ValueError(f"duplicate key {k!r}")
        d[k] = v
    return d


def _blank(x) -> bool:
    return not isinstance(x, str) or not x.strip()


def _value_problems(task: Task, qid: str, a: dict) -> list:
    out = []

    def need_str(name):
        if _blank(a.get(name)):
            out.append(f"{qid}: {name} is not a non-empty string")

    if task.kind == "author_pack":
        need_str("project")
        for name, n in (("packages", 3), ("people", 2)):
            v = a.get(name)
            if not (isinstance(v, list) and len(v) == n and all(not _blank(x) for x in v)):
                out.append(f"{qid}: {name} is not a list of exactly {n} non-empty strings")
    elif task.kind == "extract_lex":
        m = a.get("meaning")
        if not isinstance(m, str) or m not in task.choices.get(qid, ()):
            out.append(f"{qid}: meaning is not copied exactly from the item's choices")
    elif task.kind == "extract_g3h":
        need_str("project")
        need_str("person")
    elif "texts" in task.keys:
        v = a.get("texts")
        if not (isinstance(v, list) and len(v) == task.n_texts and all(not _blank(x) for x in v)):
            out.append(f"{qid}: texts is not a list of exactly {task.n_texts} non-empty strings")
        elif len(set(v)) != len(v):
            out.append(f"{qid}: the {task.n_texts} texts are not all different")
    else:
        need_str("text")
    return out


def validate_answer(task: Task, data: bytes) -> tuple:
    """(answers {qid: object without qid, in file order} or None, problems). Never edits anything."""
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as e:
        return None, [f"not UTF-8 ({e})"]
    try:
        raw = json.loads(text, object_pairs_hook=_no_dup_pairs)
    except ValueError as e:
        return None, [f"not valid JSON ({e})"]
    if not isinstance(raw, list):
        return None, ["the top level is not a JSON array"]
    probs, out, qset = [], {}, set(task.qids)
    for i, a in enumerate(raw):
        if not isinstance(a, dict):
            probs.append(f"element {i} is not an object")
            continue
        if set(a) != task.keys:
            probs.append(f"element {i}: keys {sorted(a)} != required {sorted(task.keys)}")
        q = a.get("qid")
        if not isinstance(q, str) or q not in qset:
            probs.append(f"element {i}: qid {q!r} is not an item of this task")
            continue
        if q in out:
            probs.append(f"qid {q} answered twice")
            continue
        out[q] = a
        probs += _value_problems(task, q, a)
    missing = sorted(qset - set(out))
    if missing:
        probs.append(f"{len(missing)} item(s) unanswered")
    if probs:
        return None, probs
    return {q: {k: v for k, v in a.items() if k != "qid"} for q, a in out.items()}, []


@dataclass
class FileResult:
    task: Task
    status: str                       # valid | invalid | missing | excluded
    sha256: str | None
    n_answered: int
    problems: list
    answers: dict | None


def validate_all(tasks: list, excluded: frozenset = frozenset()) -> dict:
    """{label: FileResult} for every task. Excluded (audit failed), missing and invalid files give no answers."""
    out = {}
    for t in tasks:
        f = t.answer_file
        data = f.read_bytes() if f.exists() else None
        sha = _sha(data) if data is not None else None
        if t.label in excluded:
            out[t.label] = FileResult(t, "excluded", sha, 0, ["excluded: file-access audit failed"], None)
        elif data is None:
            out[t.label] = FileResult(t, "missing", None, 0, ["no answer file"], None)
        else:
            answers, probs = validate_answer(t, data)
            out[t.label] = FileResult(t, "valid" if answers is not None else "invalid", sha,
                                      len(answers) if answers is not None else 0, probs, answers)
    return out


def stray_answer_files(tasks: list) -> list:
    """Files in the answer folders that no task names (README.txt aside): reported, never used."""
    named = {t.answer_file.resolve() for t in tasks}
    out = []
    for d in sorted({t.answer_file.parent for t in tasks}):
        if d.is_dir():
            out += [_rel(p) for p in sorted(d.iterdir()) if p.is_file() and p.name != "README.txt"
                    and p.resolve() not in named]
    return out


def resolve_excluded(tasks: list, names) -> frozenset:
    labels = {t.label for t in tasks}
    out = set()
    for n in names:
        hits = [n] if n in labels else [t.label for t in tasks if t.name == n]
        if len(hits) != 1:
            raise SystemExit(f"--exclude-task {n!r}: " + ("no such task" if not hits else f"ambiguous, use one of {hits}"))
        out.add(hits[0])
    return frozenset(out)


def validation_report(results: dict, stray: list, excluded: frozenset) -> dict:
    rows = [{"round": r.task.round, "task_id": r.task.name, "kind": r.task.kind, "file": _rel(r.task.answer_file),
             "sha256": r.sha256, "n_expected": len(r.task.qids), "n_answered": r.n_answered, "status": r.status,
             "problems": r.problems} for r in results.values()]
    return {"family": FAMILY, "version": VERSION, "contract": CONTRACT_TEXT,
            "summary": dict(sorted(Counter(f"{x['round']}/{x['status']}" for x in rows).items())),
            "files_total": len(rows), "files_valid": sum(1 for x in rows if x["status"] == "valid"),
            "files_not_valid": [x["round"] + ":" + x["task_id"] for x in rows if x["status"] != "valid"],
            "excluded_tasks": sorted(excluded), "stray_files_not_used": stray, "files": rows}


# ------------------------------------------------------------------------------------------------ 2-3. redo pieces

def _plan(results: dict) -> list:
    """redo2.build() (the regenerated plan) after checking it equals what the agents were given."""
    plan = R.build()
    probs = []
    if json.loads(json.dumps(R.index(plan))) != _json(R.ROOT / "REDO2_INDEX.json"):
        probs.append("REDO2_INDEX.json differs from the regenerated redo2 plan")
    for t in plan:
        f = Path(t["task_file"])
        if not f.exists() or f.read_text(encoding="utf-8") != t["text"]:
            probs.append(f"{t['name']}: the redo2 task file differs from the regenerated task text")
        r = results.get(f"redo2:{t['name']}")
        if r is None or tuple(r.task.qids) != tuple(t["qids"]):
            probs.append(f"{t['name']}: the redo2 index and the regenerated plan list other items")
    if {t["name"] for t in plan} != {r.task.name for r in results.values() if r.task.round == "redo2"}:
        probs.append("the redo2 index and the regenerated plan list other tasks")
    if probs:
        raise Blocked("; ".join(probs))
    return plan


def _record(pool: str, piece, tid: str, psha: str) -> dict:
    return {"pool": pool, "pid": f"{pool}|{_sha(piece.text)[:16]}", "text": piece.text, "task_id": tid,
            "prompt_sha": psha, "held_out": bool(piece.held_out), "obj": piece}


def ingest_redo(recs: dict, results: dict) -> dict:
    """Mode T pieces kept by redo round 1 and round 2, and the Mode F candidates of round 2 with their lint result.
    Order as admit.py: round 1 in file order, then the round 2 plan order; each text must differ (normalised) from
    everything authored before it, and every lint-clean Mode F candidate also blocks later duplicates."""
    src = R._batches()
    plan = _plan(results)
    seen = {_norm(r["obj"].text) for pool in ("skin", "skin_heldout", "attack", "freeform", "freeform_heldout")
            for r in recs.get(pool, [])}
    keep = {p: [] for p in MODE_T}
    audit = {"redo1": Counter(), "redo2_mode_t": Counter(), "redo2_mode_f": Counter()}
    dropped, f_rows = [], []

    for r in (x for x in results.values() if x.task.round == "redo1"):
        t = r.task
        if r.status != "valid":
            audit["redo1"][f"items_in_{r.status}_file"] += len(t.qids)
            continue
        pool, _b, c = src[t.meta["source_task_id"]]
        its = {it["qid"]: it for it in c["items"]}
        for q, a in r.answers.items():
            piece, reasons = R.lint_piece(pool, its[q], a["text"], t.name, t.meta["redo_instructions_sha256"])
            if not reasons and _norm(piece.text) in seen:
                reasons = ["duplicate of an earlier text"]
            if reasons:
                audit["redo1"]["dropped"] += 1
                dropped.append({"round": "redo1", "task": t.name, "qid": q, "j": 0, "reasons": reasons,
                                "text_sha16": _sha(a["text"].strip())[:16]})
                continue
            seen.add(_norm(piece.text))
            keep[pool].append(_record(pool, piece, t.name, t.meta["redo_instructions_sha256"]))
            audit["redo1"]["kept"] += 1

    for pt in plan:
        r = results[f"redo2:{pt['name']}"]
        pool = pt["pool"]
        bucket = audit["redo2_mode_t" if pool in MODE_T else "redo2_mode_f"]
        if r.status != "valid":
            bucket[f"items_in_{r.status}_file"] += len(pt["qids"])
            continue
        psha = R._sha(pt["text"])
        _pool, b, c = src[pt["source_task_id"]]
        its = {it["qid"]: it for it in c["items"]}
        for q in pt["qids"]:
            row = {"task": pt["name"], "pool": pool, "qid": q, "iid": b.key[q], "register": its[q]["register"],
                   "held_out": pt["held_out"], "facts": dict(its[q].get("facts") or {}), "candidates": [],
                   "kept": None}
            for j, text in enumerate(r.answers[q]["texts"]):
                piece, reasons = R.lint_piece(pool, its[q], text, pt["name"], psha)
                if not reasons and _norm(piece.text) in seen:
                    reasons = ["duplicate of a frozen or kept text"]
                row["candidates"].append({"j": j, "ok": not reasons, "reasons": reasons, "piece": piece,
                                          "text": text.strip()})
                if reasons:
                    bucket["candidate_lint_dropped"] += 1
                    dropped.append({"round": "redo2", "task": pt["name"], "qid": q, "j": j, "reasons": reasons,
                                    "text_sha16": _sha(text.strip())[:16]})
                    continue
                if pool in MODE_T:
                    if row["kept"] is None:
                        row["kept"] = j
                        seen.add(_norm(piece.text))
                        keep[pool].append(_record(pool, piece, pt["name"], psha))
                        bucket["kept"] += 1
                    else:
                        bucket["candidate_discarded_after_kept"] += 1
                else:
                    seen.add(_norm(piece.text))                  # every lint-clean Mode F candidate goes to G3-H
                    bucket["candidates_lint_clean"] += 1
            if pool in MODE_T and row["kept"] is None:
                bucket["items_without_piece"] += 1
            if pool in MODE_F:
                f_rows.append(row)
    return {"keep": keep, "f_rows": f_rows, "dropped": dropped, "plan": plan,
            "audit": {k: dict(v) for k, v in audit.items()}}


# ------------------------------------------------------------------------------------------------ 5. G3-H, round 2

def redo2_g3h(f_rows: list, results: dict, fields: list) -> dict:
    """One G3-H vote per lint-clean round 2 candidate. The read must have seen exactly the candidate's text; the
    generator facts come from the brief and must equal the expected value stored with the read."""
    root = R.G3H_ROOT
    tasks = [r for r in results.values() if r.task.round == "redo2-g3h"]
    if not tasks:
        raise Blocked("no redo2 G3-H task found")
    batch_ids = {r.task.meta["batch_id"] for r in tasks}
    if len(batch_ids) != 1:
        raise Blocked("the redo2 G3-H tasks name more than one batch")
    key = _json(root / "key" / f"{next(iter(batch_ids))}.json")["key"]                   # qid -> g3h id (orchestrator)
    chunk_text, frozen_schema, frozen_probs = {}, g3h.extraction_item("", fields)["schema"], []
    for r in tasks:
        chunk = _json(r.task.answer_file.parent.parent / "chunks" / f"{r.task.name}.json")
        if chunk["prompt_sha"] != _sha(E.G3H_PROMPT) or chunk["instructions"] != E.G3H_PROMPT.split("\n"):
            frozen_probs.append(f"{r.task.name}: the task is not the frozen G3-H prompt")
        for it in chunk["items"]:
            chunk_text[it["qid"]] = it["text"]
            if it["schema"] != frozen_schema:
                frozen_probs.append(f"{r.task.name}: item {it['qid']} has another schema than the frozen fields")
    if frozen_probs:
        raise Blocked("; ".join(frozen_probs[:3]))
    exp = {}
    for line in (root / "pool" / "g3h_expected.jsonl").read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        exp[row["g3h_id"]] = row
    task_of_gid = {key[q]: r.task.label for r in tasks for q in r.task.qids if q in key}
    gid_qid = {g: q for q, g in key.items()}
    got = {}
    for r in tasks:
        if r.status == "valid":
            for q, a in r.answers.items():
                got[key[q]] = a
    votes, probs = [], []
    for row in f_rows:
        for cand in row["candidates"]:
            if not cand["ok"]:
                continue
            gid = f"g3h2|{row['iid']}|c{cand['j']}"
            want = {"project": row["facts"].get("PROJECT"), "person": row["facts"].get("PERSON")}
            v = {"read": "g3h-redo2", "id": gid, "register": row["register"], "held_out": row["held_out"],
                 "task_id": row["task"], "qid": row["qid"], "j": cand["j"], "ok": False, "diffs": [],
                 "extracted": None, "expected": want, "g3h_task": task_of_gid.get(gid)}
            e = exp.get(gid)
            if e is None:
                v["diffs"] = ["this candidate was not in the G3-H read"]
            elif e["expected"] != want:
                probs.append(f"{gid}: expected values drifted from the brief")
                v["diffs"] = ["expected values drifted"]
            elif e["text_sha256"] != _sha(cand["piece"].text) or chunk_text.get(gid_qid.get(gid)) != cand["piece"].text:
                v["diffs"] = ["the read saw another text than this candidate"]
            elif gid not in got:
                v["diffs"] = ["no answer"]
            else:
                v["extracted"] = got[gid]
                v["ok"], v["diffs"] = g3h.compare(want, got[gid], fields)
            cand["g3h_ok"] = v["ok"]
            votes.append(v)
    if probs:
        raise Blocked("; ".join(probs[:3]))
    return {"votes": votes, "report": g3h.template_report([(v["id"], v["id"], v["ok"]) for v in votes])}


def select_documents(f_rows: list, votes: dict) -> tuple:
    """([kept Mode F pieces], [per-item rows for the manifest]): per item the first candidate in written order that
    passes lint and G3-H; the rest are discarded."""
    quarantined = set(votes["report"]["quarantined"])
    kept, rows = [], []
    for row in f_rows:
        pick = None
        for cand in row["candidates"]:
            gid = f"g3h2|{row['iid']}|c{cand['j']}"
            if cand["ok"] and cand.get("g3h_ok") and gid not in quarantined:
                pick = cand
                break
        rows.append({"task": row["task"], "qid": row["qid"], "register": row["register"],
                     "held_out": row["held_out"], "kept_j": pick["j"] if pick else None,
                     "candidates": [{"j": c["j"], "lint_ok": c["ok"], "g3h_ok": c.get("g3h_ok")} for c in row["candidates"]]})
        if pick:
            kept.append(pick["piece"])
    return kept, rows


# ------------------------------------------------------------------------------------------------ 6. pools

def finalize_documents(docs: list, t_train: int, t_held: int) -> tuple:
    """(kept documents re-keyed, cap quarantine rows): the Mode F cap of freeze.run, unchanged."""
    docs_re = [F.rekey(d) for d in docs]
    train = sorted((d for d in docs_re if not d.held_out), key=lambda d: d.skin_id)
    held = sorted((d for d in docs_re if d.held_out), key=lambda d: d.skin_id)
    drop = {d.skin_id for d in train[t_train // 3:]} | {d.skin_id for d in held[t_held // 3:]}
    return ([d for d in docs_re if d.skin_id not in drop],
            [{"skin_id": x, "reason": "Mode F cap"} for x in sorted(drop)])


def final_audit(skins: list, attacks: list, docs: list) -> list:
    """Every pool piece through the lint of its pool once more, plus the uniqueness of the texts across all pools."""
    plugin = P.T36Plugin()
    probs = []
    for s in skins + attacks:
        probs += [f"{s.skin_id}: {v.rule}: {v.detail}" for v in
                  gsl.lint_template(s, label_words=plugin.LABEL_WORDS, exceptions=plugin.GSL_EXCEPTIONS,
                                    name_allow=plugin.NAME_ALLOW)]
        probs += [f"{s.skin_id}: slots: {x}" for x in F.slot_problems(s)]
        if "\n\n" in s.text:
            probs.append(f"{s.skin_id}: blank line")
    for d in docs:
        probs += [f"{d.skin_id}: {v.rule}: {v.detail}" for v in
                  gsl.lint_freeform(d.text, dict(d.brief), label_words=plugin.LABEL_WORDS)]
        probs += [f"{d.skin_id}: {x}" for x in E.mode_f_problems(d)]
        if "\n\n" in d.text or K.placeholders(d.text):
            probs.append(f"{d.skin_id}: blank line or placeholder")
    texts = Counter(_norm(s.text) for s in skins + attacks + docs)
    probs += [f"duplicate text across the pools ({n}x): {t[:50]!r}" for t, n in texts.items() if n > 1]
    return probs


def direct_maintainer_statement(doc) -> bool:
    """Diagnostic only (never a gate): the document says in words that PERSON maintains PROJECT, with PERSON and a
    form of 'maintain' at most 60 characters apart (also the field style 'maintainer=PERSON')."""
    person = dict(doc.brief)["PERSON"]
    spans = [(m.start(), m.end()) for m in re.finditer(re.escape(person), doc.text)]
    words = [(m.start(), m.end()) for m in re.finditer(r"maintain\w*", doc.text, re.I)]
    return any(max(a0 - w1, w0 - a1) <= 60 for a0, a1 in spans for w0, w1 in words)


def render_files(*, skins, attacks, docs, wording_pool, lex_pool, packs, quarantine=None) -> dict:
    """The pool files in freeze.run's format (so freeze.load_pools / verify_pools read them)."""
    files = {
        "skins.json": F._j([F.skin_json(s) for s in sorted(skins, key=lambda s: s.skin_id)]),
        "attacks.json": F._j([F.skin_json(s) for s in sorted(attacks, key=lambda s: s.skin_id)]),
        "documents.json": F._j([F.skin_json(d) for d in sorted(docs, key=lambda d: d.skin_id)]),
        "wordings.json": F._j(sorted(wording_pool, key=lambda w: w["form_id"])),
        "lexicon.json": F._j(lex_pool),
        "packs.json": F._j([{"key": p.key, "project": p.project, "packages": list(p.packages),
                             "people": list(p.people), "held_out": p.held_out}
                            for p in sorted(packs, key=lambda p: p.key)])}
    if quarantine is not None:
        files["quarantine.json"] = F._j(quarantine)
    return files


def _count_need(shortfalls: list, name, have, want):
    if have < want:
        shortfalls.append({"item": name, "admitted": have, "target": want, "shortfall": want - have})


def _blocked(results: dict, stray: list, excluded: frozenset, blocking: list) -> dict:
    return {"ready": False, "blocked": True, "blocking": blocking,
            "status": "SHORT: blocked, " + "; ".join(blocking)[:400], "shortfalls": [], "files": None,
            "validation": validation_report(results, stray, excluded)}


# ------------------------------------------------------------------------------------------------ assemble

def assemble(exclude_names=(), tasks: list | None = None) -> dict:
    """Everything in memory: the verdict (ready / status / shortfalls), the file texts and the reports."""
    tasks = tasks or discover_tasks()
    excluded = resolve_excluded(tasks, exclude_names)
    results = validate_all(tasks, excluded)
    stray = stray_answer_files(tasks)
    bad_v1 = [r for r in results.values() if r.task.round == "v1-author" and r.status != "valid"]
    if bad_v1:
        return _blocked(results, stray, excluded, [
            f"v1 authoring answer {r.task.name} is {r.status}: v1 cannot be reproduced" for r in bad_v1])
    try:
        return _assemble(tasks, results, stray, excluded)
    except Blocked as e:
        return _blocked(results, stray, excluded, [str(e)])
    except SystemExit as e:                                   # freeze.rebuild refuses on drift
        return _blocked(results, stray, excluded, [f"v1 rebuild refused: {e}"])


def _assemble(tasks: list, results: dict, stray: list, excluded: frozenset) -> dict:
    st = F.rebuild()
    reg, fids, fields, recs = st["reg"], st["fids"], st["fields"], st["recs"]
    if {t["task_id"] for t in st["index"]["tasks"]} != {t.name for t in tasks if t.round == "v1-extract"}:
        raise Blocked("the v1 extraction index and the discovered v1 extraction tasks differ")
    v1_man = _json(POOLS_V1 / "MANIFEST.json")
    v1_disk = {k: _sha((POOLS_V1 / k).read_bytes()) for k in v1_man["sha256"]}
    if v1_disk != v1_man["sha256"]:
        raise Blocked("pools/ (v1) no longer matches its own MANIFEST.json")

    # 4 / 5a. v1 extraction answers: G-LEX votes and the round 1 G3-H read, from the valid files only
    ext_problems, glex_reads, got_by_label = [], {}, {}
    for label, kind, b, _p in st["batches"]:
        raw, unused = {}, []
        for c in b.chunks:
            r = results.get(f"v1-extract:{c['task_id']}")
            if r is not None and r.status == "valid":
                raw[c["task_id"]] = [{"qid": q, **a} for q, a in r.answers.items()]
            else:
                unused.append(f"{c['task_id']} ({r.status if r else 'no task'})")
        got, probs = chunker.load_answers(b, raw)
        if unused:
            ext_problems.append({"batch": label, "answer_files_not_used": unused})
        ext_problems += [{"batch": label, "problem": x} for x in probs]
        got_by_label[label] = got
        if kind == "extract_lex":
            glex_reads[label] = {"answered": len(got), "items": len(b.key), **F.record_glex(reg, b, got)}

    # 3. redo pieces
    redo = ingest_redo(recs, results)
    for pool, objs in redo["keep"].items():
        recs.setdefault(pool, []).extend(objs)

    # G-LEX status and the wording pool
    admitted_fids = {fid for fid in reg.forms if reg.status(fid) == "admitted"}
    wording_pool, wording_quar = [], []
    for r in sorted(recs.get("wording", []), key=lambda r: r["pid"]):
        fid, o = fids.get(r["pid"]), r["obj"]
        if fid is None or fid not in admitted_fids:
            wording_quar.append({"pid": r["pid"], "qform": o["qform"], "text": o["text"],
                                 "status": reg.status(fid) if fid else "no_form",
                                 "problems": reg.forms[fid].unit_problems if fid else []})
            continue
        f = reg.forms[fid]
        wording_pool.append({"form_id": fid, "pid": r["pid"], "qform": o["qform"], "sem_id": f.sem_id, "text": f.text,
                             "slots": dict(f.slots), "haiku_task_id": o["haiku_task_id"],
                             "haiku_prompt_sha": o["haiku_prompt_sha"], "extractions": [list(e) for e in f.extractions]})
    not_admitted = sorted(set(reg.forms) - admitted_fids)
    gate_pool = reg.gate([w["form_id"] for w in wording_pool])
    gate_all = reg.gate()
    glex = {"gate": "G-LEX", "bar": "2/2 distinct extractors (3/3 for kinds precedence and window; T36 has none)",
            "forms": len(reg.forms), "status_counts": dict(Counter(reg.status(f) for f in reg.forms)),
            "admitted": len(admitted_fids),
            "required_votes": dict(sorted({f.kind: f.required for f in reg.forms.values()}.items())),
            "strict_kind_forms": sum(1 for f in reg.forms.values() if f.kind in LX.STRICT_KINDS),
            "admitted_by_qform": dict(Counter(f.sem_id.rsplit(".", 1)[-1] for f in reg.forms.values()
                                              if f.form_id in admitted_fids)),
            "gate_on_pool_forms": {"pass": gate_pool["pass"], "n_forms": gate_pool["n_forms"],
                                   "status_counts": gate_pool["status_counts"]},
            "gate_on_all_forms": {"pass": gate_all["pass"], "n_forms": gate_all["n_forms"],
                                  "status_counts": gate_all["status_counts"], "not_admitted": gate_all["not_admitted"]},
            "reads": glex_reads}

    # 5b. G3-H: round 1 documents, then the round 2 candidates
    exp_disk = {r["g3h_id"]: r for r in map(json.loads, (F.EXTRACT / "pool" / "g3h_expected.jsonl")
                                             .read_text(encoding="utf-8").splitlines())}
    expected = {}
    for r in st["g3_recs"]:
        facts = dict(r["obj"].brief)
        iid = f"g3h|{r['pid']}"
        expected[iid] = {"project": facts["PROJECT"], "person": facts["PERSON"]}
        if exp_disk[iid]["expected"] != expected[iid]:
            raise Blocked(f"v1 G3-H expected values drifted for {iid}")
    g1_results, g1_rows = F.g3h_compare(st["g3_recs"], got_by_label["g3h-r1"], fields, expected)
    rep1 = g3h.template_report(g1_results)
    pass1 = {row["pid"] for row in g1_rows if row["ok"] and row["pid"] not in set(rep1["quarantined"])}
    docs1 = [r["obj"] for r in st["g3_recs"] if r["pid"] in pass1]
    r1_failed = [{"pid": row["pid"], "register": row["register"], "held_out": row["held_out"], "diffs": row["diffs"],
                  "note": "round 1 read (superseded by the redo2 re-authoring, ruling v2.1)"}
                 for row in g1_rows if row["pid"] not in pass1]
    votes2 = redo2_g3h(redo["f_rows"], results, fields)
    docs2, f_item_rows = select_documents(redo["f_rows"], votes2)

    # 6. packs, H32, cap, uniqueness
    plugin = P.T36Plugin()
    packs_all = [r["obj"] for r in sorted(recs.get("pack", []), key=lambda r: r["pid"])]
    pack_probs = {p.key: P.check_pack(p, plugin.LABEL_WORDS) for p in packs_all}
    packs = F.split_packs([p for p in packs_all if not pack_probs[p.key]])
    pack_quar = [{"key": p.key, "project": p.project, "problems": pack_probs[p.key]} for p in packs_all if pack_probs[p.key]]
    train_vals = set().union(*(F.pack_values(p) for p in packs if not p.held_out)) if packs else set()
    held_vals = set().union(*(F.pack_values(p) for p in packs if p.held_out)) if packs else set()
    standin_held = set().union(*(F.pack_values(p) for p in P.STANDIN_PACKS if p.held_out))
    standin_train = set().union(*(F.pack_values(p) for p in P.STANDIN_PACKS if not p.held_out))
    leaks = {"held_pack_values_also_in_training_packs": sorted(held_vals & train_vals),
             "authored_training_values_equal_standin_held_values": sorted(train_vals & standin_held),
             "authored_held_values_equal_standin_training_values": sorted(held_vals & standin_train)}

    authored_skins = [r["obj"] for r in recs.get("skin", [])] + [r["obj"] for r in recs.get("skin_heldout", [])]
    attacks_all = [r["obj"] for r in recs.get("attack", [])]
    skin_fail = [s for s in authored_skins if F.slot_problems(s)]
    attack_fail = [s for s in attacks_all if F.slot_problems(s)]
    bad_texts = {s.text for s in skin_fail + attack_fail}
    skins = [F.rekey(s) for s in authored_skins if s.text not in bad_texts and s.kind == "skin"]
    attacks = [F.rekey(s) for s in attacks_all if s.text not in bad_texts and s.kind == "attack"]
    t_train = sum(1 for s in skins if not s.held_out)
    t_held = sum(1 for s in skins if s.held_out)
    docs_v1view, _cq = finalize_documents(docs1, t_train, t_held)
    docs, cap_quar = finalize_documents(docs1 + docs2, t_train, t_held)
    final_problems = final_audit(skins, attacks, docs)
    authored_all = authored_skins + attacks_all + docs1 + docs2
    id_count = Counter(s.skin_id for s in authored_all)
    final_ids = [s.skin_id for s in skins + attacks + docs]
    if len(set(final_ids)) != len(final_ids):
        raise Blocked("skin ids collide after re-keying")

    counts = {"packs_train": sum(1 for p in packs if not p.held_out), "packs_held": sum(1 for p in packs if p.held_out),
              "skin": dict(Counter(s.register for s in skins if not s.held_out)),
              "skin_heldout": dict(Counter(s.register for s in skins if s.held_out)), "attack": len(attacks),
              "freeform": dict(Counter(d.register for d in docs if not d.held_out)),
              "freeform_heldout": dict(Counter(d.register for d in docs if d.held_out)),
              "wording": dict(Counter(w["qform"] for w in wording_pool))}
    shortfalls = []
    _count_need(shortfalls, "packs_train", counts["packs_train"], TARGETS["packs_train"])
    _count_need(shortfalls, "packs_held", counts["packs_held"], TARGETS["packs_held"])
    for pool in ("skin", "skin_heldout", "freeform", "freeform_heldout"):
        for r, want in TARGETS[pool].items():
            _count_need(shortfalls, f"{pool}/{r}", counts[pool].get(r, 0), want)
    _count_need(shortfalls, "attack", counts["attack"], TARGETS["attack"])
    for q, want in TARGETS["wording"].items():
        _count_need(shortfalls, f"wording/{q}", counts["wording"].get(q, 0), want)

    lex_full = reg.to_json()
    lex_pool = dict(lex_full)
    lex_pool["forms"] = [f for f in lex_full["forms"] if f["form_id"] in admitted_fids]
    lex_pool["note"] = "admitted forms only; every sem is declared (question meanings and decoys)"

    # v1 integrity: the same builder without the round 2 documents must give the files of pools/
    v1_files = render_files(skins=skins, attacks=attacks, docs=docs_v1view, wording_pool=wording_pool,
                            lex_pool=lex_pool, packs=packs)
    reproduced = {k: _sha(v1_files[k]) == v1_man["sha256"][k] for k in V1_POOL_FILES}
    v1_old = {k: json.loads((POOLS_V1 / k).read_text(encoding="utf-8")) for k in ("skins.json", "attacks.json", "documents.json")}
    new_ids = {"skins.json": {s.skin_id for s in skins}, "attacks.json": {s.skin_id for s in attacks},
               "documents.json": {d.skin_id for d in docs}}
    carried = {k: {d["skin_id"] for d in v1_old[k]} <= new_ids[k] for k in v1_old}
    v1_integrity = {"pools_v1_files_match_their_manifest": True, "v1_manifest_sha256": _sha((POOLS_V1 / "MANIFEST.json").read_bytes()),
                    "reproduced_by_this_builder_without_round2_documents": reproduced,
                    "every_v1_piece_carried_over": carried,
                    "ok": all(reproduced.values()) and all(carried.values())}
    blocking = []
    if not v1_integrity["ok"]:
        blocking.append("v1 is not reproduced or not carried over: " + json.dumps(v1_integrity, sort_keys=True))
    blocking += [f"final audit: {x}" for x in final_problems]

    # cross-check with redo2's own G3-H counter (only valid when nothing is excluded)
    cross = None
    if not excluded:
        try:
            ck = R.g3h_check()
            cross = {"redo2_g3h_check_kept_items": len(ck["kept"]), "ours": len(docs2),
                     "same_items_and_candidates": sorted((k["qid"], k["j"]) for k in ck["kept"])
                     == sorted((r["qid"], r["kept_j"]) for r in f_item_rows if r["kept_j"] is not None)}
        except SystemExit as e:
            cross = {"unavailable": str(e)}

    quarantine = {"g3h_failed_documents": r1_failed,
                  "g3h_redo2_failed_candidates": [{k: v[k] for k in ("id", "register", "held_out", "diffs", "extracted")}
                                                  for v in votes2["votes"] if not v["ok"]],
                  "redo_candidates_dropped": redo["dropped"], "g3h_cap_dropped": cap_quar,
                  "wordings_not_admitted": wording_quar, "forms_not_admitted": not_admitted,
                  "skin_slot_failures": [{"text_sha": _sha(s.text)[:16], "authored_id": s.skin_id, "problems": F.slot_problems(s)} for s in skin_fail],
                  "attack_slot_failures": [{"text_sha": _sha(s.text)[:16], "authored_id": s.skin_id, "problems": F.slot_problems(s)} for s in attack_fail],
                  "pack_failures": pack_quar, "unanswered_or_invalid_extraction": ext_problems}
    g3h_votes = {"gate": "G3-H", "bar": G3H_BAR, "template": "document (one Mode F document = one skin)",
                 "round1": [{"read": "g3h-r1", "id": row["pid"], "register": row["register"], "held_out": row["held_out"],
                             "ok": row["ok"], "diffs": row["diffs"], "extracted": row["extracted"], "expected": row["expected"]}
                            for row in g1_rows],
                 "redo2": votes2["votes"], "redo2_items": f_item_rows}
    files = render_files(skins=skins, attacks=attacks, docs=docs, wording_pool=wording_pool, lex_pool=lex_pool,
                         packs=packs, quarantine=quarantine)
    files["g3h_votes.json"] = F._j(g3h_votes)
    vr = validation_report(results, stray, excluded)
    files["validation_report.json"] = F._j(vr)

    ready = not shortfalls and gate_pool["pass"] and not blocking and not votes2["report"]["quarantined"]
    n_docs = len(docs)
    status = (f"READY: every G0 minimum is met (packs {counts['packs_train']}+{counts['packs_held']}, skins "
              f"{sum(counts['skin'].values())}+{sum(counts['skin_heldout'].values())}, attacks {counts['attack']}, "
              f"documents {sum(counts['freeform'].values())}+{sum(counts['freeform_heldout'].values())}, wordings "
              f"{sum(counts['wording'].values())}), the G-LEX gate passes ({gate_pool['n_forms']} pool forms admitted), "
              f"G3-H kept {n_docs} documents. G13-seed and the transcript audits are still pending."
              if ready else
              f"SHORT: {len(shortfalls)} shortfall(s)" + (f", {len(blocking)} blocking problem(s)" if blocking else "")
              + ("" if gate_pool["pass"] else ", G-LEX gate fails on a pool form"))
    manifest = {
        "family": FAMILY, "version": VERSION, "stage": "freeze-v2", "ready": ready, "status": status,
        "tier": "transfer_dev (never trained; every row dev-only)", "g0_sha256": P.POOL_G0_SHA256,
        "g0_ambiguity_pass": P.T36Plugin.G0_AMBIGUITY_PASS["task_id"],
        "supersedes": "pools/ (freeze-v1 + admit.py): untouched; v2 carries every v1 piece over", "v1_integrity": v1_integrity,
        "promote": "g13_c2.py reads only transfer/T36/pools/: promote by directory move once the owner rules it "
                   "(pools/ -> pools_v1/, pools_v2/ -> pools/); not done here",
        "loader": "freeze_v2.load_pools_v2() = freeze.load_pools(pools_v2/); freeze_v2.make_plugin() builds T36Plugin from it; "
                  "plugin.py reads no pool path, so nothing needed a new path",
        "answer_files": {"summary": vr["summary"], "total": vr["files_total"], "valid": vr["files_valid"],
                         "not_valid": vr["files_not_valid"], "excluded_tasks": sorted(excluded),
                         "stray_not_used": stray, "report": "validation_report.json"},
        "sha256": {k: _sha(v) for k, v in files.items()},
        "counts": counts, "targets": TARGETS, "shortfalls": shortfalls,
        "redo": {"audit": redo["audit"], "mode_f_items": len(f_item_rows),
                 "mode_f_items_kept": sum(1 for r in f_item_rows if r["kept_j"] is not None),
                 "mode_f_kept_candidate_index": dict(Counter(r["kept_j"] for r in f_item_rows if r["kept_j"] is not None))},
        "glex": glex,
        "g3h": {"gate": "G3-H", "bar": G3H_BAR, "template": "document (one Mode F document = one skin)",
                "round1": {"documents": len(g1_rows), "pass": sum(1 for r in g1_rows if r["ok"]),
                           "fail": sum(1 for r in g1_rows if not r["ok"]),
                           "failing_fields": dict(Counter(d.split(":", 1)[0] for r in g1_rows for d in r["diffs"]))},
                "redo2": {"candidates_read": len(votes2["votes"]), "pass": sum(1 for v in votes2["votes"] if v["ok"]),
                          "fail": sum(1 for v in votes2["votes"] if not v["ok"]),
                          "failing_fields": dict(Counter(d.split(":", 1)[0] for v in votes2["votes"] for d in v["diffs"])),
                          "templates_quarantined": votes2["report"]["quarantined"],
                          "answer_files_used": sorted(r.task.name for r in results.values()
                                                      if r.task.round == "redo2-g3h" and r.status == "valid")},
                "documents_frozen": n_docs, "from_round1": len(docs1), "from_redo2": len(docs2),
                "cross_check_with_redo2_g3h_check": cross, "votes": "g3h_votes.json"},
        "packs": {"rule": "seeded split (freeze.split_packs, unchanged): the N lowest sha256(T36|pack-split|v1|key) are held out",
                  "n_held_out": F.N_HELD_PACKS, "held_out_keys": sorted(p.key for p in packs if p.held_out), "leak_checks": leaks},
        "caps": {"mode_f_cap": "1 document per 3 Mode T skins of the same held-out status",
                 "train": {"mode_t_skins": t_train, "cap": t_train // 3,
                           "documents": sum(1 for d in docs if not d.held_out),
                           "dropped_by_cap": sum(1 for q in cap_quar if q["skin_id"].startswith("T36-freeform-"))},
                 "held_out": {"mode_t_skins": t_held, "cap": t_held // 3, "documents": sum(1 for d in docs if d.held_out),
                              "dropped_by_cap": sum(1 for q in cap_quar if q["skin_id"].startswith("T36-freeform_heldout-"))}},
        "skin_ids": {"records": len(authored_all), "authored_unique_ids": len(id_count),
                     "authored_ids_shared_by_more_than_one_record": sum(1 for v in id_count.values() if v > 1),
                     "rule": "re-keyed to T36-<pool>-<sha256(text)[:16]> as in v1",
                     "rekey_map": [[old, new] for old, new in F.rekey_map(authored_all)]},
        "added_in_v2": {k: sorted(new_ids[k] - {d["skin_id"] for d in v1_old[k]}) for k in v1_old},
        "extraction": {"answer_problems": ext_problems, "reads": glex_reads},
        "diagnostics": {"maintainer_statement": {
            "note": "not a gate: PERSON within 60 characters of a form of 'maintain' (G3-H is the gate)",
            "documents": len(docs), "direct": sum(1 for d in docs if direct_maintainer_statement(d)),
            "indirect_documents": sorted(d.skin_id for d in docs if not direct_maintainer_statement(d))}},
        "final_audit_problems": final_problems, "blocking": blocking,
        "pending_gates": [
            "G13-seed on every pool before any row (C2_DATA_SPEC 6.3): not run in this step",
            "file-access audit of the Haiku transcripts (c2_kit/audit.py; transcripts sit under never-open paths): not "
            "run in this step; the failed-audit list handed to this step was empty, so no answer file was excluded"],
    }
    files["MANIFEST.json"] = F._j(manifest)
    return {"ready": ready, "blocked": bool(blocking), "blocking": blocking, "status": status, "shortfalls": shortfalls,
            "counts": counts, "files": files, "manifest": manifest, "validation": vr, "pieces": {
                "skins": skins, "attacks": attacks, "docs": docs}}


# ------------------------------------------------------------------------------------------------ write and load

def write_pools(res: dict, root: Path = POOLS_V2) -> dict:
    """Write the files (paths.write_files: refuses before A38), then read them back and re-check v1."""
    if res.get("files") is None or res["blocking"]:
        raise SystemExit("blocking problem(s), nothing written: " + "; ".join(res["blocking"])[:600])
    man_path = root / "MANIFEST.json"
    if man_path.exists() and man_path.read_text(encoding="utf-8") != res["files"]["MANIFEST.json"]:
        raise SystemExit(f"{man_path} already exists with other content (pools_v2 is written once)")
    v1_before = {k: _sha((POOLS_V1 / k).read_bytes()) for k in sorted(p.name for p in POOLS_V1.glob("*.json"))}
    paths.write_files(root, res["files"])
    return verify_pools_v2(root, v1_before)


def verify_pools_v2(root: Path = POOLS_V2, v1_before: dict | None = None) -> dict:
    out = F.verify_pools(root)
    man = json.loads((root / "MANIFEST.json").read_text(encoding="utf-8"))
    out["manifest_files_checked"] = sorted(man["sha256"])
    out["v1_unchanged"] = (v1_before is None or v1_before == {
        k: _sha((POOLS_V1 / k).read_bytes()) for k in sorted(p.name for p in POOLS_V1.glob("*.json"))})
    out["v1_files_match_v1_manifest"] = all(
        _sha((POOLS_V1 / k).read_bytes()) == v for k, v in _json(POOLS_V1 / "MANIFEST.json")["sha256"].items())
    out["ok"] = out["ok"] and out["v1_unchanged"] and out["v1_files_match_v1_manifest"]
    return out


def wording_skin(w: dict):
    """The wording skin of one wordings.json record (kind "wording", the form id in lexicon_ids), as fixtures.skins()."""
    return K.make_skin(f"T36-wording-{w['form_id']}", FAMILY, w["text"], dict(w["slots"]), kind="wording",
                       register="question", qform=w["qform"], lexicon_ids=(w["form_id"],),
                       haiku_task_id=w["haiku_task_id"], haiku_prompt_sha=w["haiku_prompt_sha"])


def pools_from(read) -> tuple:
    """(KitCtx, packs) from a reader name -> file text. freeze.load_pools builds a ctx without the wording skins (the
    plugin asks ctx.pick(..., "wording", ...)), so the wording skins are added here, one per admitted wording."""
    sk = [F.skin_from_json(d) for d in json.loads(read("skins.json"))]
    at = [F.skin_from_json(d) for d in json.loads(read("attacks.json"))]
    dc = [F.skin_from_json(d) for d in json.loads(read("documents.json"))]
    ws = [wording_skin(w) for w in json.loads(read("wordings.json"))]
    lex = LX.LexiconRegistry.from_json(json.loads(read("lexicon.json")))
    packs = [P.Pack(p["key"], p["project"], tuple(p["packages"]), tuple(p["people"]), p["held_out"])
             for p in json.loads(read("packs.json"))]
    return KitCtx(skins={s.skin_id: s for s in sk + at + dc + ws}, lexicon=lex), packs


def load_pools_v2(root: Path = POOLS_V2) -> tuple:
    """(KitCtx with the skins, attack lines, documents, wording skins and the admitted lexicon; the packs)."""
    return pools_from(lambda name: (Path(root) / name).read_text(encoding="utf-8"))


def make_plugin(root: Path = POOLS_V2) -> tuple:
    """(T36Plugin built from pools_v2, ctx)."""
    ctx, packs = load_pools_v2(root)
    return P.T36Plugin(lexicon=ctx.lexicon, packs=packs), ctx


# ------------------------------------------------------------------------------------------------ main

def summary(res: dict) -> dict:
    if res.get("files") is None:
        return {"status": res["status"], "ready": False, "blocking": res["blocking"],
                "answer_files": res["validation"]["summary"]}
    m = res["manifest"]
    return {"status": res["status"], "ready": res["ready"], "shortfalls": res["shortfalls"], "counts": res["counts"],
            "blocking": res["blocking"], "answer_files": m["answer_files"], "glex": {k: m["glex"][k] for k in (
                "forms", "admitted", "status_counts", "required_votes", "strict_kind_forms", "gate_on_pool_forms",
                "gate_on_all_forms")},
            "g3h": m["g3h"], "redo": m["redo"], "v1_integrity": m["v1_integrity"], "caps": m["caps"],
            "diagnostics": m["diagnostics"], "pending_gates": m["pending_gates"]}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=("check", "freeze", "verify"))
    ap.add_argument("--exclude-task", action="append", default=[], metavar="NAME",
                    help="an answer file whose file-access audit failed (<round>:<task> or a unique task name)")
    a = ap.parse_args(argv)
    if a.cmd == "verify":
        print(json.dumps(verify_pools_v2(), indent=1, sort_keys=True))
        return 0
    res = assemble(a.exclude_task)
    out = summary(res)
    if a.cmd == "freeze":
        out["verify"] = write_pools(res)
        out["written"] = str(POOLS_V2)
    print(json.dumps(out, indent=1, ensure_ascii=False, sort_keys=True, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

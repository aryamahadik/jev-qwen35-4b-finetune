"""families/T28/freeze_v2.py: T28 pool freeze-v2 (G0_SPEC.md sections 7 and 9; C2_DATA_SPEC 6.2 item 2, 6.4 steps 3-4).

Why this file exists. freeze-v1 (pools/, pool_freeze.py) reads only haiku/author/answers and haiku/extract/answers, and
`pool_freeze.py freeze` refuses to run over an existing pools/MANIFEST.json. The Haiku redo answers (haiku/redo/ round 1,
haiku/redo2/ round 2) therefore had no ingest path. This script is that path. It changes nothing that exists: v1 (pools/),
every answer file, every plan file and all pinned code stay byte for byte as they are; it writes only pools_v2/.

  check    in memory only: validate every answer file, rebuild v1, merge the redo pieces, record every G-LEX and G3-H vote,
           apply every gate, and print the counts, the status (READY or SHORT) and every shortfall. Nothing is written.
  freeze   the same, then write families/T28/pools_v2/ (skins, documents, attack, wordings, lexicon, packs, QUARANTINE,
           MANIFEST, VALIDATION_REPORT) through paths.write_files. Refuses when pools_v2/MANIFEST.json already exists, and
           refuses when a blocking problem exists (v1 not reproduced, a v1 input invalid, a rebuild mismatch).

Run from lean/:  ../.venv/bin/python -B c2_build/families/T28/freeze_v2.py check|freeze
                 [--no-rebuild-check] [--exclude-task <task id>]...   (a task id whose file-access audit failed;
                 a round-1 redo task is named <name>@redo1, e.g. T28-author_pack-1e50ceff-005@redo1)

What it does, in order (no label is set anywhere; Haiku answers only flag):
  1. Contract check of EVERY answer file of every round (author v1, extract v1, redo, redo2, redo3, and any later redoN round
     with the redo2 layout; redo3 = the three attempts at the open email skin and the two G-LEX reads of the redo2 wordings). One file is valid only when it is UTF-8 JSON, a list of objects with exactly the contract keys
     (qid + text | pack | choice | user + agent), every qid in its own chunk, no duplicate key or qid, every item answered
     once, and a G-LEX choice copied exactly from the item's choices. An invalid file is rejected whole and never edited;
     its votes and pieces are not used. A task id on --exclude-task is treated the same way (audit failed).
  2. v1 is rebuilt in memory with pool_freeze.admit() and must reproduce the frozen pools/ files (sha256 of every file
     equals pools/MANIFEST.json and the file on disk) and every v1 extract answer sha. The v1 pieces carry over unchanged.
  3. Redo pieces (round 1: 59 items of the source chunks the T28 loaders turned down; round 2: new answers for the pieces
     that still failed, plus the R1 replacement wordings) go through the SAME loader checks as v1 (haiku_author.check_skin
     / check_freeform / check_wording / validate_pack + haiku_extract.value_lint_packs), against everything already
     accepted (duplicates inside a batch and across batches reject the NEW piece, never a v1 piece). A v1 piece is never
     replaced; a redo piece is used only for an item v1 turned down.
  4. G-LEX: a fresh registry holds every v1 form plus every redo wording that passed step 3, with NO votes. Votes are then
     recorded from the valid read files only: v1 reads (read0, read1, read2; v1 meaning list) first, later reads after
     (v1.1 meaning list, G0_SPEC.md section 3 R1). Admission is the kit rule (lexicon.LexiconRegistry.status): unit test
     passes and 2 distinct extractors (3 for precedence) all pick the declared sem; one other pick rejects for good. A
     form with fewer reads stays pending and is never used. The v2 registry declares the v1.1 meaning for yn_deny and
     yn_mustnot (G0 v1.1: v1 reads and rejections stand).
  5. G3-H: every Mode F memo is compared with its brief facts (g3h.compare), one entry per memo, template report at 98%;
     a memo with no valid read is dropped as unanswered.
  6. The G0 targets of pool_freeze.G0_TARGETS (not lowered) are applied to the merged pool; every skin and memo of the
     merged pool is re-run through the loader checks once more (final audit).
  7. Provenance of every redoN (N >= 2) task file: the round's own build script (haiku/redoN/build_redoN.py, when present)
     is run in memory and must reproduce every generated file of the round byte for byte (answers/ excluded); a difference
     or an extra file blocks the freeze. `--no-rebuild-check` skips this (about 100 s for redo2 + redo3).

READY means: no G0 shortfall, the G-LEX gate passes on every form the pool uses, every G3-H template passes, and no
blocking problem. Otherwise SHORT, with the exact shortfalls. G13-seed (6.4 step 4) and row generation are not run here.

How the generator loads pools_v2. Nothing in the family code (plugin.py, solver_b.py, haiku_*.py) reads a pool path, so
there is no path to refresh. pool_freeze.POOLS still names pools/ and only guards freeze-v1. g13_c2.py reads
families/<F>/pools/ (block_dir / "pools"). To use pools_v2 either
  (a) call  from families.T28 import freeze_v2;  pools = freeze_v2.load_pools();  ctx = freeze_v2.make_ctx(pools)
      (Skin objects, a LexiconRegistry, packs; default root pools_v2/; a KitCtx shaped like fixtures.ctx()), or
  (b) promote by directory move once the owner rules it (the T31 precedent): pools/ -> pools_v1/, pools_v2/ -> pools/.
Keep v1 untouched until then.
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
from c2_kit import g3h  # noqa: E402
from c2_kit import lexicon as L  # noqa: E402
from c2_kit import paths  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from families.T28 import haiku_author as A  # noqa: E402
from families.T28 import haiku_extract as HX  # noqa: E402
from families.T28 import plugin as P  # noqa: E402
from families.T28 import pool_freeze as PF  # noqa: E402

F = "T28"
VERSION = "freeze-v2"
POOLS_V1 = PF.POOLS
POOLS_V2 = HERE / "pools_v2"
HAIKU = HERE / "haiku"
G0 = HERE / "G0_SPEC.md"
G0_TARGETS = PF.G0_TARGETS                    # the v1 targets, imported and never changed
POOL_NAMES = ("packs", "skins", "freeform", "wordings")        # the batches a redo can refill
KIND_TO_POOL = {"author_pack": "packs", "author_skin": "skins", "author_freeform": "freeform",
                "author_wording": "wordings"}
CONTRACT_KEYS = {"author_pack": ("pack",), "author_skin": ("text",), "author_wording": ("text",),
                 "author_freeform": ("text",), "author_lexicon": ("text",), "extract_lex": ("choice",),
                 "extract_g3h": ("user", "agent")}


# ------------------------------------------------------------------------------------------------ small helpers
def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p: Path) -> str:
    return sha_bytes(Path(p).read_bytes())


def rel(p) -> str:
    p = Path(p).resolve()
    try:
        return p.relative_to(C2_BUILD).as_posix()
    except ValueError:
        return str(p)


def dump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=1) + "\n"


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
        c = a["choice"]
        if not isinstance(c, str):
            return [f"{qid}: choice is not a string"]
        if c not in item.get("choices", ()):
            return [f"{qid}: choice is not one of the item's choices (copied exactly)"]
        return []
    if kind == "extract_g3h":
        return [f"{qid}: {k} is not text or null" for k in ("user", "agent") if a[k] is not None
                and not isinstance(a[k], str)]
    return [f"{qid}: unknown task kind {kind}"]


def validate_answer(kind: str, data: bytes, items: dict) -> tuple:
    """(answers {qid: object without qid} or None, problems). items: {qid: item} the file must answer, once each.
    The whole file is rejected on any problem: nothing is repaired or partly used."""
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


def read_answer_file(rnd: str, kind: str, task_id: str, path: Path, items: dict, excluded: set) -> tuple:
    """(answers or None, record). The record is what VALIDATION_REPORT.json lists for the file."""
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
    data = path.read_bytes()
    rec["sha256"] = sha_bytes(data)
    ans, probs = validate_answer(kind, data, items)
    if ans is None:
        rec.update(status="invalid", problems=probs)
        return None, rec
    rec["n_answered"] = len(ans)
    return ans, rec


# ------------------------------------------------------------------------------------------------ round data
@dataclass
class AuthorItem:
    pool: str            # packs | skins | freeform | wordings
    iid: str
    payload: object      # text, or a pack object
    round: str
    task: str            # provenance task id recorded on the piece
    psha: str            # provenance prompt sha recorded on the piece
    file: str
    file_sha: str
    meta: dict


@dataclass
class ReadBatch:
    round: str
    name: str            # the extractor id (G-LEX) / read name
    kind: str            # extract_lex | extract_g3h
    batch_id: str
    key: dict            # qid -> form id (G-LEX) | memo skin id (G3-H)
    prompt_sha: str
    tasks: list          # [(task_id, answer path, {qid: item})]
    table: dict = field(default_factory=dict)      # (kind, meaning text) -> sem id (G-LEX)
    answers: dict = field(default_factory=dict)    # qid -> answer object, valid files only
    used_tasks: dict = field(default_factory=dict)   # task id -> answer sha256 of the valid files


def meaning_table(reg) -> dict:
    return {(s.kind, s.meaning): s.sem_id for s in reg.sems.values()}


def _task_label(rnd: str, name: str) -> str:
    return f"{name}@{rnd}"


def load_round1(batches: dict, v1_rejected: dict, excluded: set, problems: list) -> tuple:
    """haiku/redo/ (round 1): author-only. -> (author items, file records, extra info)."""
    d = HAIKU / "redo"
    idx = json.loads((d / "REDO_INDEX.json").read_text(encoding="utf-8"))
    chk_path = HAIKU / "redo2" / "plan" / "redo1_load_check.json"
    chk = json.loads(chk_path.read_text(encoding="utf-8")) if chk_path.is_file() else {}
    sha_at_plan = {r["redo_task"]: r["redo_answer_sha256"] for r in chk.values()}
    items_out, recs, info = [], [], {"tasks": 0, "items": 0}
    for t in idx["tasks"]:
        name = t["batch"]
        b, plan = batches[name]
        qitems = {it["qid"]: it for c in b.chunks for it in c["items"]}
        sel, bad = {}, []
        for qid in t["qids"]:
            if qid not in qitems:
                bad.append(f"redo qid {qid} is not in the source batch")
            elif b.task_of[qid] != t["source_task_id"]:
                bad.append(f"redo qid {qid} belongs to {b.task_of[qid]}, not {t['source_task_id']}")
            else:
                sel[qid] = qitems[qid]
        if t["n_items"] != len(t["qids"]):
            bad.append("n_items differs from the qid list")
        label = _task_label("redo1", t["name"])
        path = d / "answers" / f"{t['name']}.json"
        if Path(t["answer_file"]).resolve() != path.resolve():
            bad.append("the index names another answer file")
        task_file = d / f"{t['name']}.md"
        if not task_file.is_file():
            bad.append("the redo task file is missing")
        kind = t["author_kind"]
        ans, rec = read_answer_file("redo1", kind, label, path, sel, excluded)
        if bad:
            rec["problems"] += bad
            if rec["status"] == "valid":
                rec["status"] = "invalid"
            ans = None
        if ans is not None and t["name"] in sha_at_plan and sha_at_plan[t["name"]] != rec["sha256"]:
            rec["status"] = "invalid"
            rec["problems"].append("answer file changed after redo2 planning (sha256 differs from redo1_load_check.json)")
            ans = None
        recs.append(rec)
        info["tasks"] += 1
        if ans is None:
            continue
        psha = sha_file(task_file)
        for qid, a in sorted(ans.items()):
            iid = b.key[qid]
            if iid not in v1_rejected[name]:
                problems.append(f"redo1 {label}: {iid} was accepted by v1; the redo answer is ignored")
                continue
            items_out.append(AuthorItem(name, iid, a["text"] if "text" in a else a["pack"], "redo1", label, psha,
                                        rel(path), rec["sha256"], plan[iid]))
            info["items"] += 1
    return items_out, recs, info


def _round_table(d: Path, kind: str, reg11_table: dict) -> dict:
    """The meaning -> sem table of a round's G-LEX reads: its own plan file when present, else the v1.1 table."""
    if kind != "extract_lex":
        return {}
    cands = sorted((d / "plan").glob("glex_meanings*.json"))
    if len(cands) == 1:
        m2s = json.loads(cands[0].read_text(encoding="utf-8"))["meaning_to_sem"]
        return {("question", m): s for m, s in m2s.items()}
    return reg11_table


def load_round_n(n: int, d: Path, idx_path: Path, batches: dict, v1_rejected: dict, reg11_table: dict,
                 excluded: set, problems: list) -> tuple:
    """haiku/redo<N>/ (round N >= 2): chunks/, key/, manifest/, plan/ beside the index. -> (authors, reads, records)."""
    rnd = f"redo{n}"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    authors, reads, recs = [], {}, []
    for t in idx["tasks"]:
        tid, kind, bid = t["task_id"], t["kind"], t["batch_id"]
        chunk = json.loads((d / "chunks" / f"{tid}.json").read_text(encoding="utf-8"))
        key = json.loads((d / "key" / f"{bid}.json").read_text(encoding="utf-8"))["key"]
        man = json.loads((d / "manifest" / f"{bid}.json").read_text(encoding="utf-8"))
        items = {it["qid"]: it for it in chunk["items"]}
        bad = []
        want_sha = {x["task_id"]: x["sha256"] for x in man["tasks"]}.get(tid)
        if want_sha != CH.sha(json.dumps(chunk, sort_keys=True, ensure_ascii=False)):
            bad.append("chunk file differs from its manifest sha256")
        if chunk.get("task_id") != tid or chunk.get("kind") != kind or chunk.get("prompt_sha") != t["prompt_sha"]:
            bad.append("chunk header differs from the index")
        if set(items) - set(key):
            bad.append("an item has no key entry")
        path = d / "answers" / f"{tid}.json"
        if Path(t["answer_file"]).resolve() != path.resolve():
            bad.append("the index names another answer file")
        task_file = d / "tasks" / f"{tid}.md"
        if not task_file.is_file():
            bad.append("the task file is missing")
        ans, rec = read_answer_file(rnd, kind, tid, path, items, excluded)
        if bad:
            rec["problems"] += bad
            if rec["status"] == "valid":
                rec["status"] = "invalid"
            ans = None
        recs.append(rec)
        if kind in KIND_TO_POOL:
            pool = KIND_TO_POOL[kind]
            plan = json.loads((d / "plan" / f"{bid}.json").read_text(encoding="utf-8"))["plan"]
            if ans is None:
                continue
            psha = sha_file(task_file)
            for qid, a in sorted(ans.items()):
                iid = key[qid]
                meta = plan.get(iid)
                v1meta = batches[pool][1].get(iid)
                if meta is None or (v1meta is not None and any(v1meta.get(k) != meta.get(k) for k in
                                                                ("role", "register", "escape", "held_out", "qform"))):
                    problems.append(f"{rnd} {tid}: plan entry of {iid} is missing or disagrees with the v1 plan")
                    continue
                if v1meta is not None and iid not in v1_rejected[pool]:
                    problems.append(f"{rnd} {tid}: {iid} was accepted by v1; the redo answer is ignored")
                    continue
                authors.append(AuthorItem(pool, iid, a["text"] if "text" in a else a["pack"], rnd, tid, psha,
                                          rel(path), rec["sha256"], meta))
        elif kind in ("extract_lex", "extract_g3h"):
            rb = reads.get(bid)
            if rb is None:
                rb = reads[bid] = ReadBatch(rnd, t["name"], kind, bid, dict(key), t["prompt_sha"], [],
                                            _round_table(d, kind, reg11_table))
            rb.tasks.append((tid, path, items))
            if ans is not None:
                for qid, a in ans.items():
                    rb.answers[qid] = a
                rb.used_tasks[tid] = rec["sha256"]
        else:
            problems.append(f"{rnd} {tid}: task kind {kind} is not handled")
    return authors, list(reads.values()), recs


def discover_rounds() -> tuple:
    """([(n, dir, index path)] for n >= 2 in numeric order, [unrecognised dirs])."""
    found, unknown = [], []
    for d in sorted(p for p in HAIKU.glob("redo*") if p.is_dir()):
        m = re.fullmatch(r"redo(\d*)", d.name)
        n = int(m.group(1)) if m and m.group(1) else (1 if m else 0)
        idx = d / ("REDO_INDEX.json" if n == 1 else f"REDO{n}_INDEX.json")
        if n >= 1 and idx.is_file():
            found.append((n, d, idx))
        else:
            unknown.append(rel(d))
    return sorted(found), unknown


def v1_read_batches(st1: dict, table_v1: dict) -> list:
    """The v1 G-LEX and G3-H read batches (rebuilt, verified equal to the files on disk by pool_freeze.verify)."""
    out = []
    for name, b in st1["batches"]:
        kind = b.kind
        tasks = [(c["task_id"], HX.EXTRACT / b.answer_path(c["task_id"]), {it["qid"]: it for it in c["items"]})
                 for c in b.chunks]
        out.append(ReadBatch("v1", name, kind, b.batch_id, dict(b.key), b.prompt_sha, tasks,
                             table_v1 if kind == "extract_lex" else {}))
    return out


# ------------------------------------------------------------------------------------------------ registry and votes
def meanings_v11() -> tuple:
    """({qform: meaning} of G0_SPEC.md v1.1 = build_redo2.M11, checked against the G0 text, the build_redo2 module)."""
    spec = importlib.util.spec_from_file_location("t28_build_redo2", HAIKU / "redo2" / "build_redo2.py")
    br = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(br)
    norm = " ".join(G0.read_text(encoding="utf-8").split())
    for q in ("yn_deny", "yn_mustnot"):
        if br.M11[q] not in norm:
            raise SystemExit(f"v1.1 meaning of {q} is not in G0_SPEC.md")
    return dict(br.M11), br


def build_registry_v2(reg1, m11: dict):
    """A fresh T28 registry: v1's sems (question meanings from G0 v1.1) and every v1 form WITHOUT its votes."""
    j = reg1.to_json()
    sem_of_q = {L.question_sem(F, q): m for q, m in m11.items()}
    changed = sorted(s for s, m in sem_of_q.items() if reg1.sems[s].meaning != m)
    reg2 = L.LexiconRegistry(F)
    for s in j["sems"]:
        reg2.declare(s["sem_id"], s["kind"], sem_of_q.get(s["sem_id"], s["meaning"]))
    for x in j["forms"]:
        f = reg2.add(x["text"], x["sem_id"], slots=x["slots"], source=x["source"], family=x["family"],
                     haiku_task_id=x["haiku_task_id"], haiku_prompt_sha=x["haiku_prompt_sha"], held_out=x["held_out"])
        if f.form_id != x["form_id"]:
            raise SystemExit(f"form id drift {x['form_id']} -> {f.form_id}")
    for a, b in j["antonyms"]:
        reg2.declare_antonym(a, b)
    return reg2, changed


def record_lex_votes(reg, rb: ReadBatch, problems: list) -> Counter:
    """reg.record_extraction for every answered item of one valid-file G-LEX read; extractor id = the read's name."""
    c = Counter()
    for tid, _path, items in rb.tasks:
        if tid not in rb.used_tasks:
            continue
        for qid, item in items.items():
            fid = rb.key[qid]
            if fid not in reg.forms:
                problems.append(f"{rb.name}: form {fid} is not in the registry")
                continue
            f = reg.forms[fid]
            want_text = reg.lexicon_items([fid])[0][1]["text"]
            kind_meanings = {m for (k, m) in rb.table if k == f.kind}
            if item["text"] != want_text or set(item["choices"]) != kind_meanings:
                problems.append(f"{rb.name}: the item of {fid} is not the form's own text and meaning list")
                continue
            if qid not in rb.answers:
                continue
            choice = rb.answers[qid]["choice"]
            sem = rb.table.get((f.kind, choice))
            c["listed" if sem == f.sem_id else "listed_other_sense"] += 1
            try:
                reg.record_extraction(fid, rb.name, sem)
            except L.LexiconError as e:
                problems.append(f"{rb.name}: {str(e)[:100]}")
    return c


def read_label(rb: "ReadBatch") -> str:
    return rb.name if rb.round == "v1" else f"{rb.round}:{rb.name}"


def tally_reads(read_batches: list) -> dict:
    return {read_label(rb): {"round": rb.round, "batch_id": rb.batch_id, "kind": rb.kind, "prompt_sha": rb.prompt_sha,
                      "n_items": len(rb.key),
                      "tasks": {tid: {"n": len(items), "answer_sha256": rb.used_tasks.get(tid)}
                                for tid, _p, items in rb.tasks}} for rb in read_batches}


# ------------------------------------------------------------------------------------------------ merge of redo pieces
def v1_rejected_ids(st1: dict) -> dict:
    """{pool: iids the v1 loaders turned down}: the only items a redo answer may fill."""
    return {name: {iid for iid, _ in HX._split(st1["load_problems"].get(name, []))} for name in POOL_NAMES}


def merge_author_items(st1: dict, batches: dict, author_items: list, problems: list) -> dict:
    """Run the redo authoring pieces through the v1 loader checks. -> dict of accepted objects and attempt logs."""
    loaded = st1["loaded"]
    seen = {"skins": {A._norm(sk.text) for sk in loaded["skins"].values()},
            "freeform": {A._norm(sk.text) for sk in loaded["freeform"].values()},
            "attacks": {A._norm(sk.text) for sk in loaded["attacks"].values()},
            "wordings": {w[1].lower() for w in loaded["wordings"]},
            "lexicon": {A._norm(x[2]) for n in ("precedence", "comparators") for x in loaded[n]}}
    org_seen = {p["org"] for p in loaded["packs"]}
    acc = {n: {} for n in POOL_NAMES}
    attempts = defaultdict(list)
    prov = {}
    order = {n: i for i, n in enumerate(POOL_NAMES)}
    ordered = sorted(author_items, key=lambda a: (int(re.sub(r"\D", "", a.round) or 0), order[a.pool], a.iid))
    for it in ordered:
        key = (it.pool, it.iid)
        if it.iid in acc[it.pool]:
            attempts[key].append({"round": it.round, "task": it.task, "reasons": ["already accepted from an earlier redo"],
                                  "ignored": True})
            continue
        reasons, obj = [], None
        text = it.payload if isinstance(it.payload, str) else None
        if it.pool == "packs":
            p = it.payload
            reasons = A.validate_pack(p)
            if not reasons and p["org"] in org_seen:
                reasons = ["org label repeats another pack"]
            if not reasons:
                obj = A.to_plugin_pack(p, held_out=it.meta["held_out"])
                kept, vp = HX.value_lint_packs([obj])
                if vp:
                    reasons, obj = [f"value-lint: {x}" for x in vp], None
                else:
                    org_seen.add(p["org"])
        else:
            nm = A._norm(text) if isinstance(text, str) else None
            check = {"skins": A.check_skin, "freeform": A.check_freeform, "wordings": A.check_wording}[it.pool]
            try:
                obj, reasons = check(it.iid, text, it.meta, it.task, it.psha, seen[it.pool])
            except KeyError as e:
                obj, reasons = None, [f"plan entry lacks {e}"]
            if not reasons and nm in {x for k, s in seen.items() if k != it.pool for x in s}:
                seen[it.pool].discard(nm)       # the check recorded it as accepted; undo
                obj, reasons = None, ["duplicate of a text already accepted in another batch"]
        if reasons:
            attempts[key].append({"round": it.round, "task": it.task, "reasons": list(reasons)[:4]})
            continue
        acc[it.pool][it.iid] = obj
        prov[key] = {"round": it.round, "task": it.task, "answer_file": it.file, "answer_sha256": it.file_sha,
                     "prompt_sha": it.psha}
        attempts[key].append({"round": it.round, "task": it.task, "reasons": [], "accepted": True})
    return {"accepted": acc, "attempts": dict(attempts), "provenance": prov}


# ------------------------------------------------------------------------------------------------ G3-H
def g3h_results(memos: dict, reads: list, problems: list) -> tuple:
    """({sid: (ok, diffs)}, template report). memos: {sid: Skin} (brief = the facts). One entry per memo; every valid
    read of it must match exactly; a memo with no valid read is unanswered."""
    fields = P.T28Plugin.extract_fields(None, None)
    got = defaultdict(list)
    for rb in reads:
        if rb.kind != "extract_g3h":
            continue
        for tid, _path, items in rb.tasks:
            if tid not in rb.used_tasks:
                continue
            for qid, item in items.items():
                sid = rb.key[qid]
                if sid not in memos:
                    problems.append(f"{rb.name}: read of {sid}, which is not a candidate memo")
                    continue
                if item["text"] != memos[sid].text:
                    problems.append(f"{rb.name}: the item of {sid} is not the memo's text")
                    continue
                if qid in rb.answers:
                    got[sid].append((rb.name, rb.answers[qid]))
    ok_of, results = {}, []
    for sid in sorted(memos):
        facts = dict(memos[sid].brief)
        expected = {"user": facts["USER"], "agent": facts["AGENT"]}
        reads = got.get(sid, [])
        if not reads:
            ok_of[sid] = (False, ["unanswered"])
        else:
            diffs = []
            for name, a in reads:
                ok, d = g3h.compare(expected, a, fields)
                diffs += [f"{name}: {x}" for x in d]
            ok_of[sid] = (not diffs, diffs)
        results.append((sid, sid, ok_of[sid][0]))
    return ok_of, g3h.template_report(results)


# ------------------------------------------------------------------------------------------------ load v1 + redo and merge
def v1_integrity(st1: dict, c1: dict) -> dict:
    """The frozen v1 files must be reproduced by the in-memory rebuild and equal the MANIFEST and the disk."""
    man = json.loads((POOLS_V1 / "MANIFEST.json").read_text(encoding="utf-8"))
    files = PF._pool_files(st1, c1)
    probs = []
    for name, text in sorted(files.items()):
        want = man["sha256"].get(name)
        if sha_bytes(text.encode("utf-8")) != want:
            probs.append(f"{name}: the rebuild differs from pools/MANIFEST.json")
        if not (POOLS_V1 / name).is_file() or sha_file(POOLS_V1 / name) != want:
            probs.append(f"{name}: pools/{name} on disk differs from pools/MANIFEST.json")
    for name, r in man["reads"].items():
        for tid, d in r["tasks"].items():
            f = HX.EXTRACT / "answers" / f"{tid}.json"
            if not f.is_file() or sha_file(f) != d["answer_sha256"]:
                probs.append(f"{tid}: extract answer differs from the v1 MANIFEST sha256")
    for k in ("verify", "read_problems", "rec_problems", "g3_probs"):
        if st1[k]:
            probs.append(f"v1 rebuild reports {k}: {st1[k][:2]}")
    return {"manifest_sha256": sha_file(POOLS_V1 / "MANIFEST.json"), "version": man["version"], "problems": probs,
            "ok": not probs}


def load_build_module(n: int, d: Path):
    """The build_redo<N>.py module of a round (None when the round ships none). Imported from its path, never run."""
    script = Path(d) / f"build_redo{n}.py"
    if not script.is_file():
        return None
    spec = importlib.util.spec_from_file_location(f"t28_build_redo{n}", script)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def rebuild_round(n: int, d: Path, mod=None) -> dict:
    """Rebuild the generated files of haiku/redo<N>/ in memory (mod.build() -> (files, summary)) and compare them byte for
    byte with the disk. answers/ and the build script itself are not generated files. -> a record for the MANIFEST:
    {"files", "differ_or_missing", "extra_on_disk"}, or {"rebuild": "no build script"} when the round has none."""
    d = Path(d)
    mod = mod if mod is not None else load_build_module(n, d)
    if mod is None:
        return {"rebuild": "no build script (chunk, manifest and index checks only)"}
    files, _summary = mod.build()
    diffs = [r for r, t in sorted(files.items()) if not (d / r).is_file() or (d / r).read_text(encoding="utf-8") != t]
    extra = sorted(rel(p) for p in d.rglob("*") if p.is_file() and p.parent.name != "answers"
                   and p.name != f"build_redo{n}.py" and "__pycache__" not in p.parts
                   and p.relative_to(d).as_posix() not in files)
    return {"files": len(files), "differ_or_missing": diffs, "extra_on_disk": extra}


def assemble(rebuild_check: bool = True, exclude: tuple = ()) -> dict:
    excluded = set(exclude)
    blockers, problems = [], []
    batches = A.build_batches()

    # ---- v1 base
    st1 = PF.admit()
    c1 = PF.counts(st1)
    integ = v1_integrity(st1, c1)
    blockers += [f"v1: {p}" for p in integ["problems"]]

    # ---- meanings
    m11, br = meanings_v11()
    reg1 = st1["reg"]
    table_v1 = meaning_table(reg1)
    reg2, changed_sems = build_registry_v2(reg1, m11)
    table_v11 = meaning_table(reg2)
    if sorted(changed_sems) != sorted(L.question_sem(F, q) for q in ("yn_deny", "yn_mustnot")):
        blockers.append(f"v1.1 changes {changed_sems}, expected exactly yn_deny and yn_mustnot")

    # ---- answer files of every round
    records, author_items, read_batches = [], [], []
    for name, (b, plan) in batches.items():
        for ch in b.chunks:
            items = {it["qid"]: it for it in ch["items"]}
            ans, rec = read_answer_file("v1-author", b.kind, ch["task_id"], A.ROOT / b.answer_path(ch["task_id"]),
                                        items, excluded)
            records.append(rec)
            if ans is None:
                blockers.append(f"v1 author answer {ch['task_id']} is {rec['status']}: {rec['problems'][:1]}")
    v1_reads = v1_read_batches(st1, table_v1)
    for rb in v1_reads:
        for tid, path, items in rb.tasks:
            ans, rec = read_answer_file("v1-extract", rb.kind, tid, path, items, excluded)
            records.append(rec)
            if ans is None:
                blockers.append(f"v1 extract answer {tid} is {rec['status']}: {rec['problems'][:1]}")
                continue
            rb.used_tasks[tid] = rec["sha256"]
            rb.answers.update(ans)
    read_batches += v1_reads

    v1_rej = v1_rejected_ids(st1)
    a1, r1_recs, r1_info = load_round1(batches, v1_rej, excluded, problems)
    records += r1_recs
    author_items += a1
    rounds, unrecognised = discover_rounds()
    redo_checks = {"redo1": {"tasks": r1_info["tasks"], "items_valid": r1_info["items"]}}
    for n, d, idx in rounds:
        if n == 1:
            continue
        au, rds, rc = load_round_n(n, d, idx, batches, v1_rej, table_v11, excluded, problems)
        records += rc
        author_items += au
        read_batches += rds
        redo_checks[f"redo{n}"] = {"tasks": len(rc), "valid": sum(1 for r in rc if r["status"] == "valid")}
        if rebuild_check:
            rb_rec = rebuild_round(n, d, br if n == 2 else None)
            redo_checks[f"redo{n}"]["rebuild"] = rb_rec
            if rb_rec.get("differ_or_missing") or rb_rec.get("extra_on_disk"):
                blockers.append(f"redo{n} rebuild differs from disk: {rb_rec['differ_or_missing'][:2]} "
                                f"{rb_rec['extra_on_disk'][:2]}")
        else:
            redo_checks[f"redo{n}"]["rebuild"] = "skipped (--no-rebuild-check)"

    # ---- answer files that belong to no known task (never used)
    known = {r["file"] for r in records}
    adirs = [A.ROOT / "answers", HX.EXTRACT / "answers", HAIKU / "redo" / "answers"] + [dd / "answers" for _n, dd, _i in rounds]
    stray = sorted({rel(p) for d in adirs if d.is_dir() for p in d.glob("*") if p.is_file() and rel(p) not in known})

    # ---- merge of the redo authoring pieces
    mg = merge_author_items(st1, batches, author_items, problems)
    acc = mg["accepted"]
    skins2 = dict(st1["skins"])
    skins2.update({sk.skin_id: sk for sk in acc["skins"].values()})
    skins2 = dict(sorted(skins2.items()))
    packs2 = list(st1["packs"]) + [acc["packs"][i] for i in sorted(acc["packs"])]
    memo_cands = dict(st1["loaded"]["freeform"])
    memo_cands.update({sk.skin_id: sk for sk in acc["freeform"].values()})
    memo_cands = dict(sorted(memo_cands.items()))

    # ---- G-LEX: registry of v1 forms + the redo wordings that passed the loader, then the votes
    new_wordings, add_probs = [], []
    for iid in sorted(acc["wordings"]):
        q, text, held, tid, psha = acc["wordings"][iid]
        try:
            f = reg2.add(text, L.question_sem(F, q), family=F, source="haiku", haiku_task_id=tid,
                         haiku_prompt_sha=psha, held_out=held)
        except L.LexiconError as e:
            add_probs.append((iid, str(e)[:100]))
            continue
        new_wordings.append((iid, f.form_id, q, text, held, tid, psha))
    reg2.unit_test_all()
    vote_counts = {}
    for rb in read_batches:
        if rb.kind == "extract_lex":
            vote_counts[read_label(rb)] = dict(record_lex_votes(reg2, rb, problems))
    status_of = {fid: reg2.status(fid) for fid in sorted(reg2.forms)}
    for fid, f1 in reg1.forms.items():
        if status_of.get(fid) != reg1.status(fid) or reg2.forms[fid].extractions != f1.extractions:
            blockers.append(f"v1 form {fid} votes or status differ from the v1 freeze")
    gate_used = reg2.gate([fid for fid, s in status_of.items() if s == "admitted"])
    gate_all = reg2.gate()

    # ---- G3-H
    g_ok, g_report = g3h_results(memo_cands, read_batches, problems)
    memos2 = {sid: sk for sid, sk in memo_cands.items() if g_ok[sid][0]}

    # ---- wordings
    cands = [dict(w) for w in st1["wording_cands"]]
    for iid, fid, q, text, held, tid, psha in new_wordings:
        cands.append({"qform": q, "text": text, "held_out": held, "form_id": fid, "status": status_of[fid]})
    wordings2 = [dict(w) for w in st1["wordings"]]
    for iid, fid, q, text, held, tid, psha in new_wordings:
        if status_of[fid] == "admitted":
            wordings2.append({"form_id": fid, "qform": q, "text": text, "held_out": held,
                              "sense": L.question_sem(F, q), "haiku_task_id": tid, "haiku_prompt_sha": psha})
    for w in wordings2:
        if status_of.get(w["form_id"]) != "admitted":
            blockers.append(f"wording {w['form_id']} is in the pool but not admitted")

    st2 = {"reg": reg2, "status_of": status_of, "skins": skins2, "memos": memos2, "attacks": st1["attacks"],
           "wordings": wordings2, "wording_cands": cands, "packs": packs2}
    c2 = PF.counts(st2)
    short = PF.shortfalls(c2)

    # ---- final audit: every skin and memo of the merged pool through the loader checks once more
    audit = final_audit(st2, batches)

    # ---- quarantine
    q_rows, resolved = build_quarantine(st1, st2, mg, new_wordings, add_probs, g_ok, status_of, reg2)

    # ---- verdict
    lex_short = [s for s in short if s.startswith(("wordings", "precedence", "comparator"))]
    gates = {
        "G-LEX": {"pool_forms_all_admitted": gate_used["pass"], "lexicon_shortfalls": lex_short,
                  "pass": bool(gate_used["pass"] and not lex_short),
                  "registry": {k: v for k, v in gate_all.items() if k != "not_admitted"},
                  "registry_not_admitted": dict(Counter(gate_all["not_admitted"].values()))},
        "G3-H": {"memos_compared": len(g_ok), "matched": sum(1 for ok, _ in g_ok.values() if ok),
                 "all_templates_pass": g_report["all_templates_pass"], "quarantined": g_report["quarantined"],
                 "pass": bool(g_report["all_templates_pass"] and all(ok for ok, _ in g_ok.values()))},
        "G-SL": "applied at load to every v1 and redo piece (gsl.lint_template / lint_freeform / lint_values) and again "
                "in the final audit",
        "G13_seed": "not run (6.4 step 4)",
        "G2_G4_G-TW": "not run at pool stage (rows only)"}
    n_invalid = sum(1 for r in records if r["status"] in ("invalid", "excluded"))
    if audit:
        blockers.append(f"final audit: {audit[:2]}")
    ready = bool(not short and gates["G-LEX"]["pass"] and gates["G3-H"]["pass"] and not blockers)
    return {"st1": st1, "st2": st2, "c1": c1, "c2": c2, "short": short, "gates": gates, "ready": ready,
            "blockers": blockers, "problems": problems, "records": records, "stray": stray, "audit": audit,
            "integrity": integ, "redo_checks": redo_checks, "unrecognised_rounds": unrecognised, "merge": mg,
            "new_wordings": new_wordings, "add_probs": add_probs, "g_ok": g_ok, "g_report": g_report,
            "read_batches": read_batches, "vote_counts": vote_counts, "quarantine": q_rows, "resolved": resolved,
            "changed_sems": changed_sems, "n_invalid_files": n_invalid, "reg1": reg1, "batches": batches}


def final_audit(st2: dict, batches: dict) -> list:
    """Re-run the loader checks on the merged skins and memos (fresh dedup, sorted order)."""
    probs = []
    skin_iid = {f"T28-SK-{iid.split('.', 2)[2]}": iid for iid in batches["skins"][1]}
    seen = set()
    for sid, sk in sorted(st2["skins"].items()):
        iid = skin_iid.get(sid)
        if iid is None:
            probs.append(f"{sid}: not a planned skin")
            continue
        _o, v = A.check_skin(iid, sk.text, batches["skins"][1][iid], sk.haiku_task_id, sk.haiku_prompt_sha, seen)
        if v or sk.register != batches["skins"][1][iid]["register"] or sk.held_out != batches["skins"][1][iid]["held_out"]:
            probs.append(f"{sid}: {v[:2] or 'register / held-out flag differs from the plan'}")
    memo_iid = {f"T28-MF-{iid.rsplit('.', 1)[1]}": iid for iid in batches["freeform"][1]}
    seen = set()
    for sid, sk in sorted(st2["memos"].items()):
        iid = memo_iid.get(sid)
        if iid is None:
            probs.append(f"{sid}: not a planned memo")
            continue
        _o, v = A.check_freeform(iid, sk.text, batches["freeform"][1][iid], sk.haiku_task_id, sk.haiku_prompt_sha, seen)
        if v:
            probs.append(f"{sid}: {v[:2]}")
    return probs


def build_quarantine(st1: dict, st2: dict, mg: dict, new_wordings: list, add_probs: list, g_ok: dict, status_of: dict,
                     reg2) -> tuple:
    acc = mg["accepted"]
    acc_pieces = {f"{pool}|{iid}": mg["provenance"][(pool, iid)] for pool in POOL_NAMES for iid in acc[pool]}
    rows, resolved = [], []
    for row in json.loads(json.dumps(st1["quarantine"])):
        piece = row["piece"]
        if row["stage"] in ("load-check", "G-SL", "value-lint") and piece in acc_pieces:
            resolved.append({**row, "resolved_by": acc_pieces[piece]})
            continue
        tries = mg["attempts"].get(tuple(piece.split("|", 1)), [])
        if tries:
            row["redo_attempts"] = tries
        rows.append(row)
    have = {r["piece"] for r in rows}
    for (pool, iid), tries in sorted(mg["attempts"].items()):
        piece = f"{pool}|{iid}"
        if piece not in have and piece not in acc_pieces and not any(t.get("accepted") for t in tries):
            rows.append({"piece": piece, "kind": {"packs": "pack", "skins": "skin", "freeform": "document",
                                                  "wordings": "wording"}[pool], "stage": "load-check",
                         "reason": "; ".join(tries[-1]["reasons"]), "redo_attempts": tries})
    for iid, why in add_probs:
        rows.append({"piece": f"wordings|{iid}", "kind": "wording", "stage": "load-check", "reason": why})
    for sid, (ok, diffs) in sorted(g_ok.items()):
        if not ok:
            rows.append({"piece": f"document|{sid}", "kind": "document", "stage": "G3-H",
                         "status": "mismatch" if diffs != ["unanswered"] else "unanswered",
                         "reason": "; ".join(diffs[:3])})
    # G-LEX rows for forms new in v2 that are not admitted (v1's rows for v1 forms are carried above)
    for iid, fid, q, text, held, tid, psha in new_wordings:
        if status_of[fid] != "admitted":
            f = reg2.forms[fid]
            if status_of[fid] == "rejected":
                bad = [f"{e}: {'null' if s is None else s}" for e, s in f.extractions if s != f.sem_id]
                why = "a read disagrees with the declared sense: " + ", ".join(bad)
            else:
                why = f"{len({e for e, _ in f.extractions})} of {f.required} independent reads agree (need {f.required})"
            rows.append({"piece": f"lexicon|{fid}", "kind": f.kind, "sense": f.sem_id, "stage": "G-LEX",
                         "status": status_of[fid], "reason": why})
            rows.append({"piece": f"wording|{fid}", "kind": "wording", "stage": "G-LEX", "status": status_of[fid],
                         "reason": f"form {fid} is {status_of[fid]}"})
    return rows, resolved


# ------------------------------------------------------------------------------------------------ files
def validation_report(a: dict) -> dict:
    recs = a["records"]
    by = Counter((r["round"], r["status"]) for r in recs)
    return {"family": F, "version": VERSION,
            "contract": "UTF-8 JSON list; objects with exactly qid + " + " | ".join(
                f"{k}: {'+'.join(v)}" for k, v in CONTRACT_KEYS.items()) +
                        "; qids from the task's own chunk, none repeated, all answered; G-LEX choice copied exactly",
            "summary": {f"{r}/{s}": n for (r, s), n in sorted(by.items())},
            "files_total": len(recs), "files_valid": sum(1 for r in recs if r["status"] == "valid"),
            "files_not_valid": [r for r in recs if r["status"] != "valid"],
            "stray_files_not_used": a["stray"], "unrecognised_round_dirs": a["unrecognised_rounds"],
            "files": recs}


def manifest_obj(a: dict, files: dict) -> dict:
    st1, st2, c2 = a["st1"], a["st2"], a["c2"]
    qc = Counter(q["stage"] for q in a["quarantine"])
    pend = sorted(fid for fid, s in st2["status_of"].items() if s == "pending")
    added = {"skins": sorted(sk.skin_id for sk in st2["skins"].values() if sk.skin_id not in st1["skins"]),
             "memos": sorted(sid for sid in st2["memos"] if sid not in st1["memos"]),
             "packs": sorted(p["id"] for p in st2["packs"] if p["id"] not in {x["id"] for x in st1["packs"]}),
             "wordings_admitted": sorted(w["form_id"] for w in st2["wordings"]
                                         if w["form_id"] not in {x["form_id"] for x in st1["wordings"]}),
             "wordings_pending_reads": pend}
    remaining = [s for s in a["short"]]
    if pend:
        remaining.append(f"{len(pend)} redo wording(s) wait for 2 independent G-LEX reads (not needed for any G0 minimum): "
                         + ", ".join(pend))
    g0_sha = sha_file(G0)
    if a["ready"]:
        status = "READY: every G0 minimum met and the G-LEX gate passes. G13-seed and row generation not run."
    elif a["blockers"]:
        status = "BLOCKED: " + "; ".join(a["blockers"][:3])
    else:
        status = ("SHORT: " + "; ".join(a["short"]) + ". Targets are not lowered. G13-seed and row generation not run.")
    return {
        "family": F, "version": VERSION, "ready": a["ready"], "status": status,
        "supersedes": {"path": "families/T28/pools/MANIFEST.json", "version": a["integrity"]["version"],
                       "sha256": a["integrity"]["manifest_sha256"]},
        "v1_integrity": {"reproduced_by_rebuild": a["integrity"]["ok"], "problems": a["integrity"]["problems"]},
        "promote": "Nothing reads pools_v2/ by itself. Use freeze_v2.load_pools(), or (owner ruling) move pools/ to "
                   "pools_v1/ and pools_v2/ to pools/ (g13_c2 reads families/T28/pools/). Family code reads no pool path.",
        "g0": {"path": "families/T28/G0_SPEC.md", "sha256": g0_sha, "matches_plugin_pin": g0_sha == P.T28Plugin.G0_SHA256,
               "version": "v1.1 (R1)"},
        "meaning_versions": {"v1_reads": "pools/lexicon.json sems (fixtures.QUESTION_MEANINGS)",
                             "later_reads": "G0_SPEC.md v1.1 section 3 R1 (build_redo2.M11)",
                             "sems_declared_v1_1_in_this_registry": a["changed_sems"],
                             "rule": "G0 v1.1: v1 reads and rejections stand; the other 11 meanings are unchanged"},
        "answer_files": {"total": len(a["records"]),
                         "by_round_status": validation_report(a)["summary"],
                         "not_valid": [{"task_id": r["task_id"], "round": r["round"], "status": r["status"]}
                                       for r in a["records"] if r["status"] != "valid"],
                         "detail": "VALIDATION_REPORT.json"},
        "redo": a["redo_checks"],
        "reads": tally_reads(a["read_batches"]),
        "answer_reads": a["vote_counts"],
        "gates": a["gates"],
        "counts": c2, "targets_g0": G0_TARGETS,
        "targets_note": "The v1 targets (pool_freeze.G0_TARGETS) are imported unchanged; where G0 gives only an ask count, the ask is the target.",
        "shortfalls": a["short"], "remaining_work": remaining,
        "problems": {"blocking": a["blockers"], "load_notes": a["problems"], "final_audit": a["audit"]},
        "unresolved_pieces": [{"piece": q["piece"], "v1_stage": q["stage"], "v1_reason": q["reason"],
                               "redo_attempts": q.get("redo_attempts", [])}
                              for q in a["quarantine"] if q["stage"] in ("load-check", "G-SL", "value-lint")],
        "added_in_v2": added,
        "provenance_of_added": {f"{p}|{i}": v for (p, i), v in sorted(a["merge"]["provenance"].items())},
        "provenance_note": "A redo piece records haiku_task_id '<task>@redoN' and haiku_prompt_sha = sha256 of the task file the agent read.",
        "resolved_from_v1_quarantine": len(a["resolved"]),
        "quarantine_rows": len(a["quarantine"]), "quarantine_by_stage": dict(sorted(qc.items())),
        "sha256": {name: sha_bytes(text.encode("utf-8")) for name, text in sorted(files.items())},
        "note_manifest": "sha256 of every other file in pools_v2/ (this file is not hashed)"}


def build_files(a: dict) -> dict:
    st2, c2 = a["st2"], a["c2"]
    files = PF._pool_files({**st2, "quarantine": a["quarantine"]}, c2)
    q = json.loads(files["QUARANTINE.json"])
    q["resolved_by_redo"] = a["resolved"]
    q["count"] = len(a["quarantine"])
    files["QUARANTINE.json"] = dump(q)
    files["VALIDATION_REPORT.json"] = dump(validation_report(a))
    files["MANIFEST.json"] = dump(manifest_obj(a, files))
    return files


def run(write: bool, rebuild_check: bool = True, exclude: tuple = ()) -> dict:
    if write and (POOLS_V2 / "MANIFEST.json").exists():
        raise SystemExit("pools_v2/MANIFEST.json already exists: refusing to re-freeze")
    a = assemble(rebuild_check=rebuild_check, exclude=exclude)
    if write and a["blockers"]:
        raise SystemExit("blocking problems, nothing written: " + "; ".join(a["blockers"][:4]))
    files = build_files(a)
    if write:
        paths.write_files(POOLS_V2, files)
    c = a["c2"]
    man = json.loads(files["MANIFEST.json"])
    return {"status": man["status"], "ready": a["ready"], "written": write, "shortfalls": a["short"],
            "blockers": a["blockers"], "remaining_work": man["remaining_work"],
            "answer_files": man["answer_files"]["by_round_status"],
            "not_valid_files": man["answer_files"]["not_valid"],
            "redo": a["redo_checks"], "added_in_v2": man["added_in_v2"],
            "counts": {"skins_by_register": {r: d["admitted"] for r, d in c["skins_by_register"].items()},
                       "skins_T": c["skins_T_admitted"], "memos_F": c["memos_F_admitted"],
                       "memos_by_register": {r: d["admitted"] for r, d in c["memos_by_register"].items()},
                       "memo_share": c["memo_share_of_narrative"], "attacks": c["attacks"], "packs": c["packs"],
                       "wordings_admitted": c["wordings_admitted"],
                       "wordings_by_qform": {q: d["admitted"] for q, d in c["wordings_by_qform"].items()},
                       "precedence": {s: d["admitted"] for s, d in c["precedence_by_policy"].items()},
                       "comparators": {s: d["admitted"] for s, d in c["comparators_by_sense"].items()},
                       "lexicon_status": c["lexicon_status"]},
            "gates": {"G-LEX": a["gates"]["G-LEX"], "G3-H": a["gates"]["G3-H"]},
            "answer_reads": a["vote_counts"], "quarantine_rows": len(a["quarantine"]),
            "quarantine_by_stage": man["quarantine_by_stage"], "problems": a["problems"],
            "final_audit": a["audit"], "stray_files": a["stray"], "files": sorted(files)}


# ------------------------------------------------------------------------------------------------ loading pools_v2
def _tuplify(x):
    return tuple(_tuplify(i) for i in x) if isinstance(x, list) else x


def skin_from_json(d: dict) -> "K.Skin":
    """The Skin of a pool record (dataclasses.asdict output): lists back to tuples."""
    return K.Skin(skin_id=d["skin_id"], family=d["family"], text=d["text"], slots=_tuplify(d["slots"]),
                  kind=d["kind"], register=d["register"], escape=d["escape"], counts=_tuplify(d["counts"]),
                  author_mode=d["author_mode"], qform=d["qform"], brief=_tuplify(d["brief"]),
                  haiku_task_id=d["haiku_task_id"], haiku_prompt_sha=d["haiku_prompt_sha"],
                  lexicon_ids=_tuplify(d["lexicon_ids"]), held_out=d["held_out"])


def load_pools(root: Path = POOLS_V2) -> dict:
    """The pool files of a freeze as objects: {"skins": {id: Skin}, "documents": {id: Skin}, "attacks": {id: Skin},
    "wordings": [dict], "packs": [plugin pack dicts], "lexicon": LexiconRegistry, "manifest": dict}. Only admitted
    wordings are in "wordings"; the lexicon holds every form with its status (use reg.status / reg.gate)."""
    root = Path(root)

    def j(name):
        return json.loads((root / name).read_text(encoding="utf-8"))
    packs = []
    for p in j("packs.json")["packs"]:
        q = dict(p)
        q["locals"] = tuple(p["locals"])
        q["subdirs"] = tuple(p["subdirs"])
        q["files"] = tuple(p["files"])
        q["ns"] = {n: {v: tuple(a) for v, a in tools.items()} for n, tools in p["ns"].items()}
        packs.append(q)
    return {"skins": {d["skin_id"]: skin_from_json(d) for d in j("skins.json")["skins"]},
            "documents": {d["skin_id"]: skin_from_json(d) for d in j("documents.json")["documents"]},
            "attacks": {d["skin_id"]: skin_from_json(d) for d in j("attack.json")["attacks"]},
            "wordings": j("wordings.json")["wordings"], "packs": packs,
            "lexicon": L.LexiconRegistry.from_json(j("lexicon.json")), "manifest": j("MANIFEST.json")}


def make_ctx(pools: dict | None = None):
    """The generator's KitCtx for a pool set (default pools_v2/): narrative skins, Mode F memos, attack lines and one
    wording skin per ADMITTED wording (kind "wording", lexicon_ids = its form id), with the registry that holds every
    form's status. Same shape as fixtures.ctx(); a pending or rejected form is never offered."""
    from c2_kit.plugin import KitCtx
    pools = pools or load_pools()
    sk = {**pools["skins"], **pools["documents"], **pools["attacks"]}
    for w in pools["wordings"]:
        sid = f"T28-WD-{w['form_id']}"
        sk[sid] = K.make_skin(sid, F, w["text"], {}, kind="wording", register="question", qform=w["qform"],
                              held_out=w["held_out"], lexicon_ids=(w["form_id"],), haiku_task_id=w["haiku_task_id"],
                              haiku_prompt_sha=w["haiku_prompt_sha"])
    return KitCtx(skins=sk, lexicon=pools["lexicon"])


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=("check", "freeze"))
    ap.add_argument("--no-rebuild-check", action="store_true", help="skip the byte-for-byte redo2 / redo3 task-file rebuild (about 100 s)")
    ap.add_argument("--exclude-task", action="append", default=[], help="a task id whose audit failed (repeatable)")
    a = ap.parse_args(argv)
    out = run(write=(a.cmd == "freeze"), rebuild_check=not a.no_rebuild_check, exclude=tuple(a.exclude_task))
    print(json.dumps(out, indent=1, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())

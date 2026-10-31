"""c2_build/families/T23/freeze_v2.py: the T23 pool re-freeze (pools_v2/) after the redo2 Haiku round
(G0_SPEC.md v3 sections 7 and 10; C2_DATA_SPEC 6.3 G-SL, G-LEX, G3-H; PREREG A37 (b), A38).

Why a new script. T23 has no freeze script: the v1 pools (pools/, G0 v2 sha c5586eec...) were written by an orchestrator
run from the loaders (haiku_author.py, haiku_extract.py). The redo2 answers (B1 re-reads of the admitted wordings, B2 G3-H
re-reads of the Mode F notes, B3/B4 new double-negation wordings and their G-LEX reads) have no ingest path into pools,
and build_redo2.py `results` writes records only (never pools). Nothing in v1 is edited: pools/, haiku/author,
haiku/extract, haiku/redo2, the loaders and the plugin stay byte for byte as they are. This script reads them and writes
only NEW files under pools_v2/.

What a run does (every write goes through the kit's guarded writers, after A38 only):
  1. Validates EVERY answer file of every round against its task contract (validate_answer_bytes; never edits a file):
       author, extract, redo2 (stage A and stage B). A file that breaks its contract is REJECTED whole (not UTF-8 / not
       JSON, a BOM, a duplicate key, not an array, a wrong key set, a qid missing / unknown / twice, a wrong object
       count); an item whose value breaks the contract is rejected alone (an empty or non-string text, a pack that is
       not an object, a G3-H field that is neither text nor null). A G-LEX choice that is not one of the item's choices is
       kept as an INVALID READ (it rejects the form, the kit rule), and it is reported as an item problem. Rejected
       answers are treated as unanswered, never as a vote. Chunk files are checked against their manifests (sha256) and
       prompts. `--audit-failed id,id` drops the answers of tasks whose file-access audit failed (the orchestrator's list;
       empty by default).
  2. Rebuilds the v1 pipeline from the validated answers only (authoring batches, G-SL / shape lint, dedup, pack value
       lint, registry, extraction batches), checks the rebuild against the files on disk byte for byte, records the v1
       G-LEX reads (2/2) and compares the rebuilt registry and pools with pools/ (v1 reproduced or not).
  3. Folds in redo2 exactly as G0 v3 section 10 says:
       B1  every v1-admitted form that keeps the frame rule needs BOTH redo2 reads (glex-r2read0 / glex-r2read1, the row
           fill); any read on record (v1 or redo2) that picks another meaning, a decoy or an invalid choice rejects it for
           good; a missing read leaves it pending (not used). A v1 rejection is final (never re-read).
       B3/B4  forms that negate their question frame are excluded before any read; the new double-negation wordings go
           through the unchanged wording loader (haiku_author.check_wording, double), the v3 frame rule, the no-"no"-word
           rule, dedup and the registry unit tests, then need both redo2 reads (2/2).
       B2  the redo2 G3-H read replaces the v1 read of every Mode F note (exact compare, plugin.extract_fields, 98% bar
           per template; a mismatched note is always dropped). The template is read at note level AND at register level;
           a note is kept only if it matches and neither of its templates is quarantined.
     Votes follow the kit rules: LexForm.required = 2 for question forms, 3 for precedence and window forms (T23 has
     none; the code still asks 3 distinct redo2 reads for such a form).
  4. Applies every G0 minimum (never lowered) and writes pools_v2/ with MANIFEST.json (sha256 per file, counts, targets,
     shortfalls, validation, votes, how to load the pools). READY only when every G0 minimum is met, the G-LEX gate
     passes over every form the pools use, G3-H passes and no answer file was rejected or missing.

No label is set anywhere: golds come only from solver A and solver B (A37 b); Haiku output can only admit or drop a
form or a note.

  ../.venv/bin/python -m families.T23.freeze_v2 check                  (from lean/c2_build; in memory, prints a summary)
  ../.venv/bin/python -m families.T23.freeze_v2 freeze                 (writes pools_v2/)
  ../.venv/bin/python -m families.T23.freeze_v2 verify                 (pools_v2/ on disk == a fresh build, byte for byte)
  ../.venv/bin/python -m families.T23.freeze_v2 check --audit-failed T23-extract_lex-0ae96d26-000   (ignore a task)
"""
from __future__ import annotations

import copy
import dataclasses
import hashlib
import importlib.util
import json
import math
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
from c2_kit import skin as K  # noqa: E402
from c2_kit.lexicon import STRICT_KINDS, LexiconRegistry, question_sem  # noqa: E402
from families.T23 import haiku_author as A  # noqa: E402
from families.T23 import haiku_extract as HX  # noqa: E402
from families.T23 import plugin as P  # noqa: E402
import negcount  # noqa: E402  (c_src/common, on sys.path via c2_kit.paths)

FAMILY = "T23"
VERSION = "freeze-v2"
V1_POOLS = HERE / "pools"
POOLS_V2 = HERE / "pools_v2"
HAIKU = HERE / "haiku"
AUTHOR = HAIKU / "author"
EXTRACT = HAIKU / "extract"
REDO2 = HAIKU / "redo2"
G0 = HERE / "G0_SPEC.md"
POSITIVE = ("yn_version", "yn_claim", "yn_outcome")
R2_EXTRACTORS = ("glex-r2read0", "glex-r2read1")
FILES_V2 = ("packs.json", "skins.json", "attacks.json", "freeform.json", "wordings.json", "lexicon.json",
            "quarantine.json")

# G0 minimums (G0_SPEC.md section 7, C2_DATA_SPEC 3.0 / 6.3). NEVER lowered; the test file pins these numbers.
TARGET = {
    "wording_total": 30,                     # G0 7: >= 30 question wordings in total (admitted, training)
    "wording_per_form": 6,                   # G0 7: >= 6 admitted per question form (training)
    "double_negation_per_positive_form": 3,  # G0 7 + 10: >= 3 admitted per positive yes/no form (k_all = k_syn = 2)
    "packs_used": 25,                        # G0 7: >= 25 packs used, one per card (40 asked, 4 per domain)
    "skin_registers_training": 8,            # spec 3.0: >= 8 registers per family
    "skin_registers_heldout": 2,             # spec 3.0: >= 2 held out
    "g3h_rate": g3h.PASS_RATE,               # 6.3: G3-H >= 98% per template
}
AUTHOR_PLAN = {"skins": 352, "freeform": 180, "attacks": 60, "attacks_held_out": 12}     # NOT G0 targets (info)
ROWS = 800                                   # G0 2.1: T23 selected rows (info: the 2% wording cap estimate)
BASE_SHARE = {"ch_version": 0.32, "ch_term": 0.24, "yn_version": 0.15, "yn_claim": 0.15, "yn_outcome": 0.14}  # G0 4

# what each task kind's answer objects must hold besides "qid" (the contract in the task files)
REQUIRED = {"author_pack": ("pack",), "author_skin": ("text",), "author_wording": ("text",),
            "author_freeform": ("text",), "extract_lex": ("choice",),
            "extract_g3h": ("customer", "org", "item", "case_id")}
NULLABLE = {"extract_g3h": ("customer", "org", "item", "case_id")}     # "If a field's value is not in the note, null"


# ======================================================================================================= helpers
def sha_text(t: str) -> str:
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def jtext(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=1) + "\n"


def load_build_redo2():
    """build_redo2.py as a module (read-only: its builders, frame rule and fills are reused, never edited)."""
    spec = importlib.util.spec_from_file_location("t23_build_redo2", REDO2 / "build_redo2.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _rel(p: Path) -> str:
    try:
        return p.resolve().relative_to(HERE.resolve()).as_posix()
    except ValueError:
        return str(p)


def qform_of(sem_id: str) -> str:
    return sem_id.rsplit(".", 1)[1]


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
    """What one Haiku task gave the agent: its qids (and, for G-LEX, the choices of every item)."""
    task_id: str
    kind: str
    qids: list
    choices: dict = field(default_factory=dict)      # qid -> allowed choices (extract_lex)
    source: str = ""


def defs_from_chunks(chunk_dir: Path) -> dict:
    """{task_id: ChunkDef} from the chunk files an agent read."""
    out = {}
    if not chunk_dir.is_dir():
        return out
    for f in sorted(chunk_dir.glob("*.json")):
        c = json.loads(f.read_text(encoding="utf-8"))
        items = c["items"]
        out[c["task_id"]] = ChunkDef(c["task_id"], c["kind"], [i["qid"] for i in items],
                                     {i["qid"]: list(i["choices"]) for i in items if "choices" in i}, f.name)
    return out


def chunk_integrity(root: Path) -> dict:
    """chunks/*.json against manifest/<batch>.json (sha256 and item count per task) and against prompts/<sha16>.txt."""
    problems, n = [], 0
    manifests = {}
    for mf in sorted((root / "manifest").glob("*.json")):
        m = json.loads(mf.read_text(encoding="utf-8"))
        manifests[m["batch_id"]] = {t["task_id"]: t for t in m["tasks"]}
    for f in sorted((root / "chunks").glob("*.json")):
        n += 1
        c = json.loads(f.read_text(encoding="utf-8"))
        t = manifests.get(c["task_id"].rsplit("-", 1)[0], {}).get(c["task_id"])
        if t is None:
            problems.append(f"{f.name}: no manifest entry")
        elif t["sha256"] != chunker.sha(json.dumps(c, sort_keys=True, ensure_ascii=False)) or t["n"] != len(c["items"]):
            problems.append(f"{f.name}: differs from its manifest entry")
        pf = root / "prompts" / f"{c['prompt_sha'][:16]}.txt"
        if not pf.is_file() or chunker.sha(pf.read_text(encoding="utf-8")) != c["prompt_sha"]:
            problems.append(f"{f.name}: prompt file missing or its sha256 differs")
    return {"dir": _rel(root), "chunks": n, "problems": problems, "ok": not problems}


def validate_answer_bytes(data: bytes, cd: ChunkDef) -> dict:
    """Validate one answer file against its task contract. Never edits anything.

    File-level problems reject the file: not UTF-8 / not JSON, a byte-order mark, a duplicate object key, a top level
    that is not an array, an element that is not an object, a key set other than {"qid"} + the kind's fields, a qid that is
    not a string / is unknown / is used twice, an object count other than the chunk's, a qid left unanswered.
    Item-level problems reject only that item: an empty or non-string text, a pack that is not an object, a G3-H field that
    is neither text nor null. A G-LEX choice that is not one of the item's choices stays in `items` (it is recorded later as
    an INVALID READ, which rejects the form) and is listed in `item_problems`.
    Returns {"ok", "n_expected", "n_valid_items", "file_problems", "item_problems", "items"}."""
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
    nullable = set(NULLABLE.get(cd.kind, ()))
    for qid in cd.qids:
        el = seen[qid]
        bad, keep = [], True
        for k in REQUIRED[cd.kind]:
            v = el[k]
            if v is None and k in nullable:
                continue
            if cd.kind == "author_pack":
                if not isinstance(v, dict):
                    bad.append("pack is not an object")
                    keep = False
            elif cd.kind == "extract_lex":
                if not isinstance(v, str) or not v.strip():
                    bad.append("choice is not a non-empty string")
                    keep = False
                elif v not in cd.choices.get(qid, ()):
                    bad.append("choice is not one of the item's choices (an invalid read)")
            elif not isinstance(v, str) or not v.strip():
                bad.append(f"{k} is not a non-empty string" if k not in nullable else f"{k} is neither text nor null")
                keep = False
        if bad:
            rep["item_problems"].append(f"{qid}: " + "; ".join(bad))
        if keep:
            rep["items"].append(el)
    rep["ok"] = True
    rep["n_valid_items"] = len(rep["items"])
    return rep


def validate_round(name: str, defs: dict, answers_dir: Path, ignore=()) -> dict:
    """Validate every answer file of one round. A task with no file is `missing`; a file with no task is `stray` (never
    used); a task named in `ignore` (failed audit) is `ignored` (treated as unanswered)."""
    files, stray, missing, ignored = {}, [], [], []
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
        if tid in ignore:
            rep["ignored"] = "file-access audit failed (orchestrator list): the answers are not used"
            ignored.append(tid)
        files[tid] = rep
    for n in present:
        if not n.endswith(".json") or n[:-5] not in defs:
            stray.append(n)
    rejected = sorted(t for t, r in files.items() if not r["ok"])
    return {"round": name, "dir": _rel(answers_dir), "tasks": len(defs), "files": files, "missing": sorted(missing),
            "stray": stray, "rejected": rejected, "ignored": sorted(ignored),
            "item_rejects": sum(len(r["item_problems"]) for r in files.values())}


def accepted(round_rep: dict) -> dict:
    """{task_id: accepted answer objects} of a validated round (rejected, ignored and missing files are absent)."""
    return {t: r["items"] for t, r in round_rep["files"].items() if r["ok"] and not r.get("ignored")}


def slim(round_rep: dict) -> dict:
    """The round report without the accepted items (for the manifest and the validation report)."""
    out = {k: v for k, v in round_rep.items() if k != "files"}
    out["files"] = {t: {k: v for k, v in r.items() if k != "items"} for t, r in round_rep["files"].items()}
    return out


def validate_ambiguity(path: Path) -> dict:
    """The one Haiku output that is not a task answer: the ambiguity pass (haiku/ambiguity/amb_T23_points.json, resolved in
    G0 section 9). Contract: an object with the listed keys, n_points == len(points), every point {where, issue, readings}
    with non-empty text and a list of text readings, and points_sha256 per its own sha_rule. A point without readings is
    reported (item problem); the points feed no pool (G0 section 9 answers each H<n>)."""
    rep = {"file": _rel(path), "ok": False, "file_problems": [], "item_problems": []}
    fp = rep["file_problems"]
    data = path.read_bytes()
    rep.update({"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
    try:
        o = json.loads(data.decode("utf-8"), object_pairs_hook=_no_dup_pairs, parse_constant=_no_const)
    except (ValueError, _Strict) as e:
        fp.append(f"not valid JSON: {e}")
        return rep
    need = {"family", "pass", "workflow", "phase", "model", "date", "input", "note", "resolved_in", "n_points",
            "points_sha256", "sha_rule", "points"}
    if not isinstance(o, dict) or set(o) != need:
        fp.append("keys differ from the contract")
        return rep
    pts = o["points"]
    if not isinstance(pts, list) or o["n_points"] != len(pts):
        fp.append("n_points does not match the points list")
        return rep
    rule = "sha256 of json.dumps(points, sort_keys=True, ensure_ascii=False, separators=(',', ':'))"
    if o["sha_rule"] != rule:
        fp.append("unknown sha_rule")
    elif sha_text(json.dumps(pts, sort_keys=True, ensure_ascii=False, separators=(",", ":"))) != o["points_sha256"]:
        fp.append("points_sha256 does not match the points")
    if o["family"] != FAMILY:
        fp.append(f"family {o['family']!r}")
    for i, p in enumerate(pts, 1):
        if not isinstance(p, dict) or set(p) != {"where", "issue", "readings"}:
            fp.append(f"point {i}: keys differ from {{where, issue, readings}}")
        elif not (isinstance(p["where"], str) and p["where"].strip() and isinstance(p["issue"], str)
                  and p["issue"].strip() and isinstance(p["readings"], list)
                  and all(isinstance(r, str) and r.strip() for r in p["readings"])):
            fp.append(f"point {i}: a field is not non-empty text / a list of text readings")
        elif not p["readings"]:
            rep["item_problems"].append(f"point {i} (H{i} in G0 section 9) lists no competing readings")
    rep["ok"] = not fp
    rep["n_points"] = len(pts)
    return rep


# ======================================================================================================= 2. v1 rebuild
def _batch_answers(b, raw: dict) -> tuple:
    mine = {c["task_id"]: raw[c["task_id"]] for c in b.chunks if c["task_id"] in raw}
    missing = sorted(c["task_id"] for c in b.chunks if c["task_id"] not in raw)
    ans, probs = chunker.load_answers(b, mine)
    return ans, probs, missing


def author_pool(name: str, check, batches: dict, raw: dict) -> tuple:
    """haiku_author._loop over validated answers: (accepted objects, problem strings, tasks without a valid answer)."""
    b, plan = batches[name]
    ans, probs, missing = _batch_answers(b, raw)
    out, seen = [], set()
    for iid, a in sorted(ans.items()):
        text = a.get("text") if isinstance(a, dict) else None
        obj, v = check(iid, text, plan[iid], A._task_of(b, iid), b.prompt_sha, seen)
        if v:
            probs.append(f"{iid}: " + "; ".join(v[:4]))
        else:
            out.append(obj)
    return out, probs, missing


def author_packs(batches: dict, raw: dict) -> tuple:
    """haiku_author.load_packs over validated answers, keeping the raw pack and the task id for the pool record.
    -> (records [{"id","domain","pack"(plugin Pack),"orgs","customers","held_out","iid","task","raw"}], problems, missing)."""
    b, plan = batches["packs"]
    ans, probs, missing = _batch_answers(b, raw)
    out, seen = [], set()
    for iid, a in sorted(ans.items()):
        p = a.get("pack") if isinstance(a, dict) else None
        meta = plan[iid]
        v = A.validate_pack(p, meta["domain"])
        if not v and (set(p["orgs"]) & seen):
            v = ["an organisation name repeats another pack's"]
        if v:
            probs.append(f"{iid}: " + "; ".join(v[:4]))
            continue
        seen |= set(p["orgs"])
        rec = A.to_plugin_pack(p, meta["domain"], held_out=meta["held_out"], pack_id=f"t23pk-{iid.split('.', 2)[2]}")
        rec.update({"iid": iid, "task": A._task_of(b, iid), "raw": p})
        out.append(rec)
    return out, probs, missing


def load_author(raw: dict) -> SimpleNamespace:
    """The v1 authoring pipeline over validated answers only (G-SL / shape lint, in-batch dedup, pack value lint)."""
    batches = A.build_batches()
    s = SimpleNamespace(batches=batches, probs={}, missing={})
    loaded = {}
    packs, s.probs["packs"], s.missing["packs"] = author_packs(batches, raw)
    s.packs_all = packs
    loaded["packs"] = packs
    for name, fn in (("skins", A.check_skin), ("attacks", A.check_attack), ("freeform", A.check_freeform),
                     ("wordings", A.check_wording)):
        objs, s.probs[name], s.missing[name] = author_pool(name, fn, batches, raw)
        loaded[name] = ({o.skin_id: o for o in objs} if name != "wordings" else objs)
    s.loaded = loaded
    s.packs_kept, s.pack_value_probs = HX.value_lint_packs(packs)
    return s


def diff_files(files: dict, root: Path) -> list:
    out = []
    for rel, text in sorted(files.items()):
        p = root / rel
        if not p.exists():
            out.append(f"missing {rel}")
        elif p.read_text(encoding="utf-8") != text:
            out.append(f"differs {rel}")
    return out


def batch_diffs(b, root: Path) -> list:
    """The batch files (prompt, chunks, key, manifest) against disk."""
    return diff_files(b.files(), root)


# ======================================================================================================= G-LEX reads
def record_reads(reg: LexiconRegistry, named: list, raw: dict) -> tuple:
    """Record G-LEX reads over validated answers. named: [(extractor id, TaskBatch)].
    -> ({form id: [{"extractor","task","choice","sem","valid"}]}, per-read summaries, problems).
    A form the read did not answer gets no record (pending). An answer that is not one of the item's choices is an
    invalid read: sem None, which rejects the form (kit rule: any extractor that does not pick the form's meaning)."""
    votes, summaries, problems = defaultdict(list), [], []
    for ext, b in named:
        ans, probs, missing = _batch_answers(b, raw)
        problems += [f"{ext}: {p}" for p in probs]
        items = chunker.item_by_internal(b)
        task_of = {b.key[q]: b.task_of[q] for q in b.key}
        stats = Counter()
        for fid in sorted(b.key.values()):
            if fid not in ans:
                stats["unanswered"] += 1
                continue
            choice = ans[fid].get("choice") if isinstance(ans[fid], dict) else None
            valid = isinstance(choice, str) and choice in items[fid]["choices"]
            sem = reg.meaning_to_sem("question", choice) if valid else None
            reg.record_extraction(fid, ext, sem)
            votes[fid].append({"extractor": ext, "task": task_of[fid], "choice": choice if isinstance(choice, str)
                               else None, "sem": sem, "valid": valid})
            stats["match" if sem == reg.forms[fid].sem_id else "invalid" if not valid else "other_meaning"] += 1
        summaries.append({"read": ext, "batch_id": b.batch_id, "items": len(b.key), "chunks": len(b.chunks),
                          "tasks_without_valid_answer": missing, "outcomes": dict(sorted(stats.items()))})
    return dict(votes), summaries, problems


def r2_status(reg: LexiconRegistry, fid: str) -> str:
    """The v2 status of a form that needs redo2 reads: rejected if any read on record disagrees or is invalid;
    admitted only with the unit test passed and >= `required` DISTINCT redo2 extractors (2 for question forms, 3 for
    precedence / window forms) all on its meaning; otherwise pending_read_missing."""
    f = reg.forms[fid]
    st = reg.status(fid)
    if st in ("rejected", "unit_fail", "untested"):
        return st
    n_r2 = len({e for e, _ in f.extractions if e.startswith("glex-r2")})
    if n_r2 >= f.required and st == "admitted":
        return "admitted"
    return "pending_read_missing"


# ======================================================================================================= redo2 wordings
def dneg_forms_validated(R, reg1: LexiconRegistry, raw: dict) -> tuple:
    """build_redo2.dneg_forms over validated answers (same checks, same order): the unchanged wording loader (double),
    the v3 frame rule, k_syn == 2, dedup against every v1 text and the registry unit tests (a new form that breaks any
    form's unit test is dropped). -> (registry v1 + accepted new forms, [new form ids], drops {iid: reasons},
    load problems, batch, plan, forms meta {fid: {...}})."""
    b, plan = R.dneg_batch()
    ans, probs, missing = _batch_answers(b, raw)
    if missing:
        probs = probs + [f"{t}: no valid answer" for t in missing]
    seen = {" ".join(f.text.split()).lower() for f in reg1.forms.values()}
    task_of = {iid: b.task_of[qid] for qid, iid in b.key.items()}
    drops, ok = {}, []
    for iid in sorted(plan):
        a = ans.get(iid)
        text = a.get("text") if isinstance(a, dict) else None
        obj, v = A.check_wording(iid, text, plan[iid], task_of[iid], b.prompt_sha, seen)
        if obj and not v:
            v = R.v3_problems(obj[1])
            if R.k_syn(obj[1]) != 2:
                v.append("not a double negation (k_syn != 2)")
        if v:
            drops[iid] = v
        else:
            ok.append((iid, obj))
    base = copy.deepcopy(reg1)                    # reg1 is already unit-tested; a copy keeps its votes and cache clean

    def add(r: LexiconRegistry, obj: tuple) -> str:
        q, text, decl, held, _d, tid, psha = obj
        return r.add(text, question_sem(FAMILY, q), slots=dict(decl), family=FAMILY, source="haiku",
                     haiku_task_id=tid, haiku_prompt_sha=psha, held_out=held).form_id

    def rebuild(accepted_objs: list) -> LexiconRegistry:
        r = copy.deepcopy(base)
        for obj in accepted_objs:
            add(r, obj)
        return r

    # one registry grows form by form: the unit tests are pure functions of the form set, so "base + accepted + this
    # candidate" is tested exactly as build_redo2 does (it rebuilds from v1 every time); a failing candidate is dropped
    # and the registry rebuilt without it
    reg, acc, iid_of, dirty = copy.deepcopy(base), [], {}, False
    for iid, obj in ok:
        try:
            add(reg, obj)
        except Exception as e:      # noqa: BLE001  (a registry refusal is logged and the piece dropped, never patched)
            drops[iid] = [f"registry: {e}"]
            reg, dirty = rebuild(acc), True
            continue
        res = reg.unit_test_all()
        bad = [fid for fid, passed in res.items() if not passed]
        if bad:
            drops[iid] = [f"unit test fails for {bad[:3]}"]
            reg, dirty = rebuild(acc), True
            continue
        acc.append(obj)
        iid_of[obj[1]] = iid
        dirty = False
    if dirty:
        reg.unit_test_all()
    new = [f for f in reg.forms if f not in base.forms]
    meta = {fid: {"iid": iid_of[reg.forms[fid].text], "double": True} for fid in new}
    return reg, new, drops, probs, b, plan, meta


def stage_b_files(R, reg: LexiconRegistry, new: list, r2b: list, drops: dict, probs: list) -> dict:
    """The files build_redo2.stage_b writes (task files, chunks, keys, manifests, plan/dneg_load.json, TASKS_B.json), rebuilt
    from the validated answers, to compare with the files the orchestrator issued."""
    files, rows = {}, []
    for ext, b in r2b:
        f, r = R._task_rows(b, stage="B", blocker="B3/B4", read=ext, text_fn=HX.task_text)
        files.update(f)
        rows += r
    files["plan/dneg_load.json"] = json.dumps({
        "new_forms": {fid: {"text": reg.forms[fid].text, "sem": reg.forms[fid].sem_id,
                            "fill": R.filled_text(reg, fid)[0]} for fid in new},
        "dropped": drops, "load_problems": probs,
        "per_qform": dict(sorted(Counter(reg.forms[f].sem_id.split(".")[-1] for f in new).items()))},
        ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    files["TASKS_B.json"] = json.dumps({
        "family": FAMILY, "version": R.SEED, "stage": "B", "g0_sha256": P.T23.G0_SHA256_V3, "n_tasks": len(rows),
        "batches": {ext: b.batch_id for ext, b in r2b}, "n_new_forms": len(new), "n_dropped": len(drops),
        "notes": ["Two independent G-LEX reads of the new double-negation wordings: v1 prompt, 13 choices, B1 fill.",
                  "One fresh Haiku agent per task_file; never both reads to one agent."],
        "tasks": rows}, ensure_ascii=False, indent=1) + "\n"
    return files


# ======================================================================================================= G3-H
def g3h_batch_validated(R, freeform: dict) -> tuple:
    """build_redo2.g3h_batch over the loader-admitted Mode F notes of the validated rebuild."""
    fields = R.g3h_fields()
    items, expected = [], {}
    for sid in sorted(freeform):
        sk = freeform[sid]
        facts = dict(sk.brief)
        items.append((sid, g3h.extraction_item(sk.text, fields)))
        expected[sid] = {"register": sk.register, "expected": {"customer": facts["CUSTOMER"], "org": facts["ORG"],
                                                               "item": facts["ITEM"], "case_id": facts["CASE_ID"]}}
    b = chunker.make_batch("extract_g3h", FAMILY, items, seed=f"{R.SEED}|g3h", prompt=R.G3H_PROMPT + HX.G3H_TAIL,
                           max_items=R.G3H_MAX)
    return b, expected


def g3h_compare(b, expected: dict, raw: dict) -> dict:
    """Exact compare of every Mode F note's extraction (g3h.compare, plugin.extract_fields) and the template reports at
    note level and at register level (98% bar). A note unanswered by the reader fails."""
    ans, probs, missing = _batch_answers(b, raw)
    fields = P.T23.extract_fields(None, None)
    rows = []
    for sid in sorted(expected):
        if sid in ans:
            ok, diffs = g3h.compare(expected[sid]["expected"], ans[sid], fields)
        else:
            ok, diffs = False, ["unanswered"]
        rows.append({"sid": sid, "register": expected[sid]["register"], "ok": ok, "diffs": diffs})
    per_note = g3h.template_report([(r["sid"], r["sid"], r["ok"]) for r in rows])
    per_reg = g3h.template_report([(r["register"], r["sid"], r["ok"]) for r in rows])
    bad_regs = set(per_reg["quarantined"])
    for r in rows:
        r["kept"] = bool(r["ok"] and r["sid"] not in per_note["quarantined"] and r["register"] not in bad_regs)
    return {"rows": rows, "per_note": per_note, "per_register": per_reg, "problems": probs,
            "missing_tasks": missing, "n": len(rows), "pass": sum(r["ok"] for r in rows),
            "kept": sum(r["kept"] for r in rows),
            "pass_ok": per_note["all_templates_pass"] and per_reg["all_templates_pass"] and not probs}


# ======================================================================================================= 4. targets
def pack_cards() -> tuple:
    """(training cards per domain, S5 cards per domain) from the plugin's card rule (G0 section 2): one pack per card."""
    train, held = Counter(), Counter()
    for sampler in P.T23.SAMPLERS:
        for card in range(P.CARDS):
            dom = P._card(sampler, card)[0]
            (held if sampler in P.T23.HELD_OUT_SAMPLERS else train)[dom] += 1
    return dict(train), dict(held)


def evaluate_targets(*, train_by_form: dict, ho_by_form: dict, dneg_by_form: dict, packs_train_by_dom: dict,
                     packs_ho_by_dom: dict, train_regs: list, ho_regs: list, g3h_note_rate: float,
                     g3h_register_rate: float, cand_train: dict | None = None) -> tuple:
    """(targets, shortfalls): every G0 minimum, never lowered. cand_train: wordings per form still waiting for reads."""
    shortfalls, cand_train = [], cand_train or {}

    def tgt(name, bar, got, note="", extra=None):
        rec = {"bar": bar, "got": got, "pass": got >= bar}
        if got < bar:
            sf = {"target": name, "bar": bar, "got": got, "short_by": round(bar - got, 6), "note": note}
            sf.update(extra or {})
            shortfalls.append(sf)
        return rec

    cards_t, cards_h = pack_cards()
    wording = {qf: tgt(f"wording {qf} (training, admitted)", TARGET["wording_per_form"], train_by_form.get(qf, 0),
                       extra={"waiting_for_reads": cand_train.get(qf, 0)}) for qf in P.QF}
    dneg = {qf: tgt(f"double-negation wording {qf} (training, admitted, k_all = k_syn = 2)",
                    TARGET["double_negation_per_positive_form"], dneg_by_form.get(qf, 0),
                    extra={"waiting_for_reads": cand_train.get(qf, 0)}) for qf in POSITIVE}
    packs_total = sum(packs_train_by_dom.values()) + sum(packs_ho_by_dom.values())
    packs = {"packs_used": tgt("packs admitted (>= 25 used, one per card)", TARGET["packs_used"], packs_total)}
    cover = {}
    for dom in P.DOMAIN_KEYS:
        cover[dom] = {"training": tgt(f"training packs for domain {dom} (one per training card)",
                                      cards_t.get(dom, 0), packs_train_by_dom.get(dom, 0)),
                      "held_out": tgt(f"held-out packs for domain {dom} (one per S5 card)",
                                      cards_h.get(dom, 0), packs_ho_by_dom.get(dom, 0))}
    base = {
        "wording_total_training": tgt("wordings admitted, training, all forms", TARGET["wording_total"],
                                      sum(train_by_form.values())),
        "skin_registers_training": tgt("skin registers (training)", TARGET["skin_registers_training"], len(train_regs),
                                       f"registers with kept skins: {sorted(train_regs)}"),
        "skin_registers_heldout": tgt("skin registers (held out)", TARGET["skin_registers_heldout"], len(ho_regs),
                                      f"registers with kept held-out skins: {sorted(ho_regs)}"),
        "g3h_per_note_template": tgt("G3-H pass rate (template = note)", TARGET["g3h_rate"], round(g3h_note_rate, 6)),
        "g3h_per_register_template": tgt("G3-H pass rate (template = register)", TARGET["g3h_rate"],
                                         round(g3h_register_rate, 6)),
    }
    return {"base": base, "wording_per_form": wording, "double_negation": dneg, "packs": packs,
            "pack_cards": {"training_cards_per_domain": cards_t, "s5_cards_per_domain": cards_h, "coverage": cover}}, \
        shortfalls


def cap_2pct_estimate(train_by_form: dict) -> dict:
    """Information only (not a G0 minimum): spec 3.0 caps a wording at 2% of the family's rows. With ROWS selected rows
    and the G0 section 4 base shares (partners: 60% of yes/no bases, 60 / 40 between the two partner forms) this is the
    number of training wordings each form needs, against what the pool holds."""
    cap = 0.02 * ROWS
    share = dict(BASE_SHARE)
    for pos, (a, b_) in {"yn_version": ("yn_version_other", "yn_version_not"), "yn_claim": ("yn_claim_contra",
                         "yn_claim_not"), "yn_outcome": ("yn_outcome_out", "yn_outcome_not")}.items():
        share[a] = BASE_SHARE[pos] * 0.6 * 0.6
        share[b_] = BASE_SHARE[pos] * 0.6 * 0.4
    out = {}
    for qf, sh in share.items():
        need = math.ceil(sh * ROWS / cap)
        out[qf] = {"estimated_rows": round(sh * ROWS, 1), "wordings_needed": need, "training_admitted":
                   train_by_form.get(qf, 0), "ok": train_by_form.get(qf, 0) >= need}
    return out


# ======================================================================================================= 5. the build
def build(raw_override: dict | None = None, audit_failed=()) -> SimpleNamespace:
    """The whole freeze in memory. raw_override (tests only): {round: {task_id: accepted answer objects}} replacing what is
    read from disk for the named rounds ("author", "extract", "redo2")."""
    ov = raw_override or {}
    s = SimpleNamespace()
    s.a38 = paths.a38_frozen(paths.PREREG.read_text(encoding="utf-8"))
    s.audit_failed = sorted(audit_failed)
    s.checks = {}
    R = load_build_redo2()
    s.R = R

    # ---- 1. validate every answer file of every round
    defs = {"author": defs_from_chunks(AUTHOR / "chunks"), "extract": defs_from_chunks(EXTRACT / "chunks"),
            "redo2": defs_from_chunks(REDO2 / "chunks")}
    s.rounds = {name: validate_round(name, defs[name], root / "answers", ignore=s.audit_failed)
                for name, root in (("author", AUTHOR), ("extract", EXTRACT), ("redo2", REDO2))}
    s.integrity = {name: chunk_integrity(root) for name, root in (("author", AUTHOR), ("extract", EXTRACT),
                                                                  ("redo2", REDO2))}
    s.checks["chunk_files_match_manifests"] = all(v["ok"] for v in s.integrity.values())
    s.ambiguity = validate_ambiguity(HAIKU / "ambiguity" / "amb_T23_points.json")
    s.checks["ambiguity_pass_file_valid"] = s.ambiguity["ok"]
    redo2_tasks = {"A": [t["task_id"] for t in json.loads((REDO2 / "TASKS.json").read_text(encoding="utf-8"))["tasks"]],
                   "B": [t["task_id"] for t in json.loads((REDO2 / "TASKS_B.json").read_text(encoding="utf-8"))["tasks"]]}
    s.redo2_tasks = redo2_tasks
    s.checks["redo2_tasks_cover_chunks"] = sorted(redo2_tasks["A"] + redo2_tasks["B"]) == sorted(defs["redo2"])
    raw_author = ov.get("author", accepted(s.rounds["author"]))
    raw_extract = ov.get("extract", accepted(s.rounds["extract"]))
    raw_redo2 = ov.get("redo2", accepted(s.rounds["redo2"]))
    s.answer_problems = []
    for name, r in s.rounds.items():
        s.answer_problems += [f"{name}: {t} rejected: {'; '.join(r['files'][t]['file_problems'])}" for t in r["rejected"]]
        s.answer_problems += [f"{name}: item problem {m}" for t, rr in r["files"].items() for m in rr["item_problems"]]
        s.answer_problems += [f"{name}: stray file {n}" for n in r["stray"]]
        s.answer_problems += [f"{name}: {t} has no answer file" for t in r["missing"]]
        s.answer_problems += [f"{name}: {t} ignored (failed audit)" for t in r["ignored"]]
    s.answer_problems += [f"chunks {n}: {p}" for n, v in s.integrity.items() for p in v["problems"]]
    s.answer_problems += [f"ambiguity: {p}" for p in s.ambiguity["file_problems"]]
    s.notes = [f"ambiguity pass: {p} (informational: G0 section 9 answers every point; no pool depends on it)"
               for p in s.ambiguity["item_problems"]]

    # ---- 2. the v1 pipeline over validated answers; disk == rebuild
    au = load_author(raw_author)
    s.au = au
    diffs = []
    for name, (b, _plan) in au.batches.items():
        diffs += [f"author/{name}: {d}" for d in batch_diffs(b, AUTHOR)]
    s.checks["author_batches_match_disk"] = not diffs
    reg1, refused, unit_fail = HX.build_registry(au.loaded)
    s.checks["v1_registry_no_refusal_no_unit_fail"] = refused == 0 and unit_fail == 0
    lex1 = HX.glex_batches(reg1)
    g3_1, _exp1 = HX.g3h_batch(au.loaded["freeform"])
    for name, b in lex1 + [("g3h", g3_1)]:
        diffs += [f"extract/{name}: {d}" for d in batch_diffs(b, EXTRACT)]
    s.checks["extract_batches_match_disk"] = not [d for d in diffs if d.startswith("extract/")]
    s.batch_diffs = diffs
    v1_named = [(f"glex-{name}", b) for name, b in lex1]
    s.v1_votes, s.v1_read_summaries, v1_probs = record_reads(reg1, v1_named, raw_extract)
    s.answer_problems += [f"v1 reads: {p}" for p in v1_probs]
    v1_reg_disk = json.loads((V1_POOLS / "lexicon.json").read_text(encoding="utf-8"))
    s.checks["v1_registry_reproduced"] = reg1.to_json() == v1_reg_disk
    s.reg1 = reg1
    ff_batch_v1, ff_expected_v1 = HX.g3h_batch(au.loaded["freeform"])
    v1_g3 = _g3h_v1(ff_batch_v1, ff_expected_v1, raw_extract)
    s.v1_g3_pass = v1_g3

    # ---- 3a. B1 + B3/B4: frame rule, re-reads
    part = R.b1_partition(reg1)
    s.part = part
    s.checks["b1_partition_matches_disk"] = (
        json.loads((REDO2 / "plan" / "b1_partition.json").read_text(encoding="utf-8"))["reread"] == part["reread"])
    st_a_files, _rows = R.stage_a()
    s.stage_a_diffs = diff_files(st_a_files, REDO2)
    s.checks["redo2_stage_a_files_match_disk"] = not s.stage_a_diffs
    reg2 = copy.deepcopy(reg1)                                   # v1 votes carried over; the redo2 votes go on this copy
    r2a = R.glex_batches(reg2, part["reread"], "b1")
    r2_votes_a, r2_sum_a, r2_probs_a = record_reads(reg2, r2a, raw_redo2)
    s.answer_problems += [f"redo2 stage A reads: {p}" for p in r2_probs_a]

    reg_b, new, dn_drops, dn_probs, dn_batch, dn_plan, dn_meta = dneg_forms_validated(R, reg2, raw_redo2)
    s.dn_drops, s.dn_probs, s.dn_plan = dn_drops, dn_probs, dn_plan
    s.answer_problems += [f"redo2 double-negation authoring: {p}" for p in dn_probs]
    # reg_b = reg2 (v1 + stage A votes) + the accepted new forms
    r2b = R.glex_batches(reg_b, new, "b3") if new else []
    st_b_files = stage_b_files(R, reg_b, new, r2b, dn_drops, dn_probs)
    s.stage_b_diffs = diff_files(st_b_files, REDO2)
    s.checks["redo2_stage_b_files_match_disk"] = bool(new) and not s.stage_b_diffs
    r2_votes_b, r2_sum_b, r2_probs_b = record_reads(reg_b, r2b, raw_redo2)
    s.answer_problems += [f"redo2 stage B reads: {p}" for p in r2_probs_b]
    s.reg = reg_b
    s.new_forms, s.r2_votes = new, {**r2_votes_a, **r2_votes_b}
    s.r2_summaries = {"A": r2_sum_a, "B": r2_sum_b}
    s.dn_meta = dn_meta

    status = {}
    for fid in sorted(reg_b.forms):
        if fid in part["excluded_frame"]:
            status[fid] = "excluded_frame"
        elif fid in part["v1_rejected"]:
            status[fid] = "rejected_v1"
        elif fid in part["reread"] or fid in new:
            status[fid] = r2_status(reg_b, fid)
        else:
            status[fid] = f"unexpected:{reg_b.status(fid)}"
    s.status = status
    s.checks["every_form_classified"] = not [f for f, st in status.items() if st.startswith("unexpected")]
    s.checks["no_strict_kind_forms"] = not [f for f in reg_b.forms.values() if f.kind in STRICT_KINDS]

    # ---- 3b. B2: G3-H over the validated Mode F notes
    gb, expected = g3h_batch_validated(R, au.loaded["freeform"])
    s.checks["g3h_batch_matches_disk"] = not batch_diffs(gb, REDO2)
    s.g3 = g3h_compare(gb, expected, raw_redo2)
    s.answer_problems += [f"redo2 G3-H: {p}" for p in s.g3["problems"]]
    return assemble(s)


def _g3h_v1(b, expected: dict, raw: dict) -> dict:
    """The v1 G3-H read (template = note), only to reproduce the v1 freeform pool."""
    ans, probs, _missing = _batch_answers(b, raw)
    fields = P.T23.extract_fields(None, None)
    ok = {}
    for sid, e in expected.items():
        ok[sid] = g3h.compare({k: v for k, v in e.items()}, ans[sid], fields)[0] if sid in ans else False
    return ok


def _pack_record(rec: dict) -> dict:
    return {"iid": rec["iid"], "haiku_task_id": rec["task"], "domain": rec["domain"], "held_out": rec["held_out"],
            "pack": rec["raw"]}


def assemble(s: SimpleNamespace) -> SimpleNamespace:
    """Kept pieces, quarantine, pending reads, counts, targets, gates and the pool documents."""
    reg, status, au = s.reg, s.status, s.au
    admitted = sorted(f for f, st in status.items() if st == "admitted")
    admitted_set = set(admitted)
    s.gate_used = reg.gate(used_form_ids=admitted)
    plan_w = au.batches["wordings"][1]
    dbl_by_text = {o[1]: o[4] for o in au.loaded["wordings"]}

    # ---- wordings
    wordings, pending, dneg_flag_ok = [], [], True
    for fid in admitted:
        f = reg.forms[fid]
        qf = qform_of(f.sem_id)
        dbl = negcount.count(K.PH_RE.sub("X", f.text))
        double = (dbl.k_all, dbl.k_syn) == A.NEG_DOUBLE
        if f.text in dbl_by_text:
            dneg_flag_ok = dneg_flag_ok and dbl_by_text[f.text] == double
        wordings.append({"form_id": fid, "qform": qf, "text": f.text, "held_out": f.held_out, "double_negation": double,
                         "haiku_task_id": f.haiku_task_id, "haiku_prompt_sha": f.haiku_prompt_sha,
                         "extractors": [list(e) for e in f.extractions]})
    s.checks["double_negation_flag_matches_plan"] = dneg_flag_ok
    for fid, st in status.items():
        if st == "pending_read_missing":
            f = reg.forms[fid]
            pending.append({"form_id": fid, "qform": qform_of(f.sem_id), "held_out": f.held_out, "text": f.text,
                            "reads_recorded": sorted({e for e, _ in f.extractions}), "reads_required": f.required})
    s.wordings, s.pending = wordings, pending

    # ---- skins, attacks, freeform, packs
    loaded = au.loaded
    skins = [dataclasses.asdict(loaded["skins"][k]) for k in sorted(loaded["skins"])]
    attacks = [dataclasses.asdict(loaded["attacks"][k]) for k in sorted(loaded["attacks"])]
    kept_notes = {r["sid"] for r in s.g3["rows"] if r["kept"]}
    freeform = [dataclasses.asdict(loaded["freeform"][k]) for k in sorted(loaded["freeform"]) if k in kept_notes]
    kept_pack_ids = {p["id"] for p in au.packs_kept}
    packs = [_pack_record(p) for p in sorted(au.packs_all, key=lambda p: p["iid"]) if p["id"] in kept_pack_ids]

    # ---- quarantine: v1 entries still in force + the new v2 entries
    v1_q = json.loads((V1_POOLS / "quarantine.json").read_text(encoding="utf-8"))
    superseded = [e for e in v1_q if e["pool"] == "freeform" and e["gate"].startswith("G3-H")
                  and e["id"] in kept_notes]
    kept_v1_q = [e for e in v1_q if e not in superseded]
    rebuilt_loader_reasons = {name: HX._drops(au.probs.get(name, []))
                              for name in ("skins", "freeform", "attacks", "wordings", "packs")}
    s.checks["loader_drops_match_v1_quarantine"] = all(
        sorted((i, r) for i, rs in rebuilt_loader_reasons[n].items() for r in rs) ==
        sorted((e["id"], e["reason"]) for e in v1_q if e["gate"].startswith("loader") and e["pool"] == n)
        for n in ("skins", "freeform", "attacks", "wordings"))
    new_q = []
    for fid, st in sorted(status.items()):
        f = reg.forms[fid]
        if st == "excluded_frame":
            new_q.append({"pool": "wordings", "id": fid, "gate": "G0 v3 frame rule (B3/B4)",
                          "reason": "; ".join(s.part["excluded_frame"][fid]["problems"]),
                          "v1_status": s.part["excluded_frame"][fid]["v1_status"], "text": f.text})
        elif st == "rejected":
            new_q.append({"pool": "wordings", "id": fid, "gate": "G-LEX 2/2 after the redo2 reads (any other pick or an "
                          "invalid read rejects for good)", "reason": _vote_reason(s, fid), "text": f.text})
        elif st == "pending_read_missing":
            new_q.append({"pool": "wordings", "id": fid, "gate": "G-LEX: redo2 reads missing (not used until both exist)",
                          "reason": _vote_reason(s, fid), "text": f.text})
    for iid, why in sorted(s.dn_drops.items()):
        new_q.append({"pool": "wordings", "id": iid, "gate": "loader / v3 shape (redo2 double-negation authoring)",
                      "reason": "; ".join(why)})
    for r in s.g3["rows"]:
        if not r["kept"]:
            new_q.append({"pool": "freeform", "id": r["sid"], "gate": "G3-H redo2 (B2; template = note and register; "
                          "bar 98%)", "reason": "; ".join(r["diffs"]) or f"register template {r['register']} quarantined"})
    quarantine = kept_v1_q + new_q
    s.quarantine, s.superseded_v1_quarantine = quarantine, superseded
    s.kept = {"packs": packs, "skins": skins, "attacks": attacks, "freeform": freeform}

    # ---- counts and targets
    train_by_form = Counter(w["qform"] for w in wordings if not w["held_out"])
    ho_by_form = Counter(w["qform"] for w in wordings if w["held_out"])
    dneg_by_form = Counter(w["qform"] for w in wordings if not w["held_out"] and w["double_negation"])
    cand_train = Counter(x["qform"] for x in pending if not x["held_out"])
    skins_train = [x for x in skins if not x["held_out"]]
    skins_ho = [x for x in skins if x["held_out"]]
    train_regs = sorted({x["register"] for x in skins_train})
    ho_regs = sorted({x["register"] for x in skins_ho})
    pk_train, pk_ho = Counter(p["domain"] for p in packs if not p["held_out"]), Counter(
        p["domain"] for p in packs if p["held_out"])
    s.targets, s.shortfalls = evaluate_targets(
        train_by_form=dict(train_by_form), ho_by_form=dict(ho_by_form), dneg_by_form=dict(dneg_by_form),
        packs_train_by_dom=dict(pk_train), packs_ho_by_dom=dict(pk_ho), train_regs=train_regs, ho_regs=ho_regs,
        g3h_note_rate=_min_rate(s.g3["per_note"]), g3h_register_rate=_min_rate(s.g3["per_register"]),
        cand_train=dict(cand_train))
    s.cap2 = cap_2pct_estimate(dict(train_by_form))
    s.g3h_pass = s.g3["pass_ok"] and not s.g3["missing_tasks"]
    s.failed_checks = sorted(k for k, v in s.checks.items() if not v)
    # READY: every G0 minimum met, the G-LEX gate passes over the used forms, G3-H passes, every integrity check holds and
    # there is no answer problem at all (a rejected / missing / ignored / stray file, a rejected item, an invalid read, an
    # unanswered item, a chunk that differs from its manifest)
    s.ready = bool(not s.shortfalls and s.gate_used["pass"] and s.g3h_pass and not s.answer_problems
                   and not s.failed_checks)
    s.counts = {
        "packs": {"admitted": len(packs), "training": sum(pk_train.values()), "held_out": sum(pk_ho.values()),
                  "training_by_domain": dict(sorted(pk_train.items())), "held_out_by_domain": dict(sorted(pk_ho.items()))},
        "skins": {"training_by_register": dict(sorted(Counter(x["register"] for x in skins_train).items())),
                  "held_out_by_register": dict(sorted(Counter(x["register"] for x in skins_ho).items())),
                  "training": len(skins_train), "held_out": len(skins_ho)},
        "attacks": {"kept": len(attacks), "held_out": sum(1 for a in attacks if a["held_out"])},
        "freeform": {"kept": len(freeform), "by_register": dict(sorted(Counter(x["register"] for x in freeform).items())),
                     "loader_admitted": s.g3["n"], "g3h_pass": s.g3["pass"]},
        "wordings": {"admitted_training_by_qform": dict(sorted(train_by_form.items())),
                     "admitted_heldout_by_qform": dict(sorted(ho_by_form.items())),
                     "training_total": sum(train_by_form.values()), "held_out_total": sum(ho_by_form.values()),
                     "double_negation_by_qform": dict(sorted(dneg_by_form.items())),
                     "pending_reads_training_by_qform": dict(sorted(cand_train.items()))},
        "lexicon": {"forms_in_registry": len(reg.forms), "status": dict(sorted(Counter(status.values()).items())),
                    "v1_forms": len(s.reg1.forms), "new_double_negation_forms": len(s.new_forms)},
        "quarantine": {"total": len(quarantine), "by_gate": dict(sorted(Counter(q["gate"] for q in quarantine).items())),
                       "v1_entries_kept": len(kept_v1_q), "v1_entries_superseded": len(superseded),
                       "new_entries": len(new_q)},
    }
    s.info = {"author_plan_not_g0": {
        "skins_mode_T": {"plan": AUTHOR_PLAN["skins"], "kept": len(skins)},
        "mode_F_notes": {"plan": AUTHOR_PLAN["freeform"], "kept": len(freeform)},
        "attack_lines": {"plan": AUTHOR_PLAN["attacks"], "kept": len(attacks)},
        "attack_lines_held_out": {"plan": AUTHOR_PLAN["attacks_held_out"], "kept": s.counts["attacks"]["held_out"]},
        "note": "the author plan asked for more pieces than the loaders kept; G0 sets no count for these, so they are "
                "reported, not gated (the v1 manifest listed the same deltas)"},
        "wording_cap_2pct_estimate": s.cap2,
        "held_out_wordings_per_form_g0_gives_no_count": dict(sorted(ho_by_form.items()))}
    s.docs = pool_documents(s, admitted)
    rt = LexiconRegistry.from_json(s.docs["lexicon.json"])
    s.checks["lexicon_json_loads_admitted_only"] = (
        len(rt.forms) == len(admitted) and all(f.unit_ok and rt.status(fid) == "admitted" for fid, f in rt.forms.items())
        and rt.gate()["pass"])
    s.failed_checks = sorted(k for k, v in s.checks.items() if not v)
    s.ready = bool(s.ready and not s.failed_checks)
    return s


def _min_rate(rep: dict) -> float:
    rates = [d["rate"] for d in rep["templates"].values()]
    return min(rates) if rates else 0.0


def _vote_reason(s: SimpleNamespace, fid: str) -> str:
    v1 = s.v1_votes.get(fid, [])
    r2 = s.r2_votes.get(fid, [])
    parts = [f"{x['extractor']}={x['sem']}" + ("" if x["valid"] else " (invalid choice)") for x in v1 + r2]
    return f"own sem {s.reg.forms[fid].sem_id}; reads: " + ("; ".join(parts) if parts else "none recorded") + \
        f" (redo2 reads recorded {len(r2)} of {s.reg.forms[fid].required} needed)"


def pool_documents(s: SimpleNamespace, admitted: list) -> dict:
    reg = s.reg
    lex_json = reg.to_json()
    keep = set(admitted)
    lex_json["forms"] = [f for f in lex_json["forms"] if f["form_id"] in keep]
    lex_json.update({
        "family": FAMILY, "pool": "lexicon", "count": len(keep),
        "note": ("forms = the v2-ADMITTED question forms only (each with its v1 and redo2 extractions); every other form "
                 "is listed in not_admitted and must never be used by a row"),
        "admitted_form_ids": sorted(keep),
        "not_admitted": {fid: st for fid, st in sorted(s.status.items()) if st != "admitted"}})
    return {"packs.json": s.kept["packs"], "skins.json": s.kept["skins"], "attacks.json": s.kept["attacks"],
            "freeform.json": s.kept["freeform"], "wordings.json": s.wordings, "lexicon.json": lex_json,
            "quarantine.json": s.quarantine}


# ======================================================================================================= 6. v1 comparison
def v1_comparison(s: SimpleNamespace, texts: dict) -> dict:
    """Is v1 reproduced, and what does v2 add or change? The files redo2 cannot change must be byte for byte the v1 files."""
    out = {}
    v1_manifest = json.loads((V1_POOLS / "manifest.json").read_text(encoding="utf-8"))
    for rel in ("packs.json", "skins.json", "attacks.json"):
        v1 = (V1_POOLS / rel).read_bytes()
        out[rel] = {"identical_to_v1": v1 == texts[rel].encode("utf-8"),
                    "v1_sha256_in_v1_manifest": v1_manifest["pool_files_sha256"][rel],
                    "v1_file_matches_its_manifest": hashlib.sha256(v1).hexdigest() == v1_manifest["pool_files_sha256"][rel]}
    v1_ff = {x["skin_id"]: x for x in json.loads((V1_POOLS / "freeform.json").read_text(encoding="utf-8"))}
    v2_ff = {x["skin_id"]: json.loads(json.dumps(x, ensure_ascii=False)) for x in s.kept["freeform"]}
    out["freeform.json"] = {"v1_notes": len(v1_ff), "v2_notes": len(v2_ff),
                            "every_v1_note_kept_unchanged": all(k in v2_ff and v2_ff[k] == v for k, v in v1_ff.items()),
                            "added_vs_v1": sorted(set(v2_ff) - set(v1_ff)),
                            "v1_reproduced_from_v1_g3h_read": sorted(k for k, ok in s.v1_g3_pass.items() if ok) ==
                            sorted(v1_ff)}
    v1_w = {w["form_id"]: w for w in json.loads((V1_POOLS / "wordings.json").read_text(encoding="utf-8"))}
    v2_w = {w["form_id"]: w for w in s.wordings}
    same = lambda a, b: {k: v for k, v in a.items() if k != "extractors"} == {k: v for k, v in b.items() if k != "extractors"}
    out["wordings.json"] = {
        "v1_admitted": len(v1_w), "v2_admitted": len(v2_w),
        "v1_kept": sum(1 for f in v1_w if f in v2_w), "v1_dropped": sorted(f for f in v1_w if f not in v2_w),
        "v2_new": sorted(f for f in v2_w if f not in v1_w),
        "kept_fields_unchanged": all(same(v1_w[f], v2_w[f]) for f in v1_w if f in v2_w),
        "kept_v1_extractions_are_a_prefix": all(v2_w[f]["extractors"][:len(v1_w[f]["extractors"])] ==
                                                v1_w[f]["extractors"] for f in v1_w if f in v2_w)}
    v1_l = json.loads((V1_POOLS / "lexicon.json").read_text(encoding="utf-8"))
    v2_l = {f["form_id"]: f for f in s.docs["lexicon.json"]["forms"]}
    out["lexicon.json"] = {"v1_forms": len(v1_l["forms"]), "v2_admitted_forms": len(v2_l),
                           "kept_forms_text_unchanged": all(f["text"] == v2_l[f["form_id"]]["text"] and
                                                            f["sem_id"] == v2_l[f["form_id"]]["sem_id"]
                                                            for f in v1_l["forms"] if f["form_id"] in v2_l)}
    v1_q = json.loads((V1_POOLS / "quarantine.json").read_text(encoding="utf-8"))
    out["quarantine.json"] = {"v1_entries": len(v1_q), "v1_entries_kept_unchanged": sum(1 for e in v1_q if e in s.quarantine),
                              "v1_entries_superseded": len(s.superseded_v1_quarantine),
                              "v1_entries_otherwise_missing": [e for e in v1_q if e not in s.quarantine
                                                               and e not in s.superseded_v1_quarantine]}
    out["v1_manifest_sha256"] = hashlib.sha256((V1_POOLS / "manifest.json").read_bytes()).hexdigest()
    out["v1_pool_files_untouched"] = all(
        hashlib.sha256((V1_POOLS / k).read_bytes()).hexdigest() == v for k, v in v1_manifest["pool_files_sha256"].items())
    return out


# ======================================================================================================= 7. summary, write
LOADER_NOTE = (
    "plugin.py reads no pool path: T23 takes its skins, wordings, attack lines and lexicon from the KitCtx / registry "
    "the caller builds (fixtures.py builds the in-memory stand-ins), so there is nothing to refresh in plugin.py. The "
    "shared G13 seed loader (g13_c2.pool_units) reads families/T23/pools/ only and skips file names holding 'manifest', "
    "'report' or 'check'. To use these pools: when READY (and before G13-seed), move pools/ to pools_v1/ and pools_v2/ to "
    "pools/ (same file names; the manifest is MANIFEST.json here, manifest.json in v1). Until then the generator must "
    "load pools_v2/ explicitly: skins.json items with held_out=false are the training skins (held_out=true: sampler S5 "
    "only), attacks.json likewise, freeform.json = the Mode F notes that passed the redo2 G3-H read (author_mode F, facts "
    "in `brief`), packs.json items carry the raw pack answer, `domain` and `held_out` (the 4th pack of a domain is "
    "held out, S5 cards only); wordings.json items are the ADMITTED question wordings: build each as "
    "make_skin(<id>, 'T23', text, <slots of the form in lexicon.json>, kind='wording', register='question', qform=qform, "
    "held_out=held_out, lexicon_ids=(form_id,)); held_out=false: samplers S1-S4, true: sampler S5 only; lexicon.json "
    "holds the admitted forms only (LexiconRegistry.from_json reads it; extra keys are ignored) and `not_admitted` "
    "lists every other form: never use them; quarantine.json lists the dropped pieces and the forms still waiting for "
    "reads. glex_votes_report.json and g3h_compare_report.json hold every vote.")


def summarize(s: SimpleNamespace) -> dict:
    texts = {rel: jtext(obj) for rel, obj in s.docs.items()}
    files = {rel: {"sha256": sha_text(t), "bytes": len(t.encode("utf-8")),
                   "count": len(s.docs[rel]) if isinstance(s.docs[rel], list) else s.docs[rel]["count"]}
             for rel, t in texts.items()}
    s.texts, s.file_rows = texts, files
    s.cmp = v1_comparison(s, texts)
    validation = {name: {"tasks": r["tasks"], "files": len(r["files"]),
                         "accepted_files": sum(1 for x in r["files"].values() if x["ok"] and not x.get("ignored")),
                         "rejected": r["rejected"], "item_problems": r["item_rejects"], "missing": r["missing"],
                         "stray": r["stray"], "ignored": r["ignored"]} for name, r in s.rounds.items()}
    waiting = sum(max(0, x["reads_required"] - len([e for e in x["reads_recorded"] if e.startswith("glex-r2")]))
                  for x in s.pending)
    short = "; ".join(f"{x['target']}: {x['got']} < {x['bar']}" for x in s.shortfalls)
    if not s.g3h_pass:
        short += ("; " if short else "") + "G3-H does not pass"
    if not s.gate_used["pass"]:
        short += ("; " if short else "") + "G-LEX gate fails over the used forms"
    if s.answer_problems:
        short += ("; " if short else "") + f"{len(s.answer_problems)} answer problem(s): {s.answer_problems[:4]}"
    if s.failed_checks:
        short += ("; " if short else "") + f"integrity checks failed: {s.failed_checks}"
    status = ("READY: every G0 minimum is met, the G-LEX gate passes over every form the pools use, G3-H passes (note and "
              "register templates), there is no answer problem (no file rejected, missing, ignored or stray; no invalid "
              "read) and every integrity check holds" if s.ready else "SHORT: " + short +
              (f" ({len(s.pending)} form(s) still wait for {waiting} redo2 read(s))" if s.pending else ""))
    s.status_text = status
    s.votes_report = votes_report(s)
    s.g3h_report = {"gate": "G3-H", "bar": g3h.PASS_RATE, "rule":
                    "redo2 read replaces the v1 read (G0 v3 10 B2); exact compare; a note is kept only if it matches and "
                    "neither its note-level nor its register-level template is quarantined",
                    "n": s.g3["n"], "pass": s.g3["pass"], "kept": s.g3["kept"],
                    "per_note_template": {"quarantined": s.g3["per_note"]["quarantined"],
                                          "min_rate": _min_rate(s.g3["per_note"])},
                    "per_register_template": s.g3["per_register"]["templates"],
                    "quarantined_registers": s.g3["per_register"]["quarantined"], "rows": s.g3["rows"]}
    return {"family": FAMILY, "version": VERSION, "ready": s.ready, "status": status, "a38_frozen": s.a38,
            "audit_failed_ignored": s.audit_failed, "checks": s.checks, "counts": s.counts, "targets": s.targets,
            "shortfalls": s.shortfalls,
            "gates": {"G-LEX_used_forms": {k: v for k, v in s.gate_used.items() if k != "not_admitted"},
                      "G-LEX_registry": {
                          "forms": len(s.reg.forms), "v2_status_counts": dict(sorted(Counter(s.status.values()).items())),
                          "not_used": sum(1 for st in s.status.values() if st != "admitted"),
                          "note": "the kit's own status() still reads 'admitted' for the 4 v1-admitted forms that negate "
                                  "their question frame (their v1 reads stand); G0 v3 10 B3/B4 excludes them, so their v2 "
                                  "status is excluded_frame and no pool file uses them"},
                      "G3-H": {"pass": s.g3h_pass, "n": s.g3["n"], "pass_notes": s.g3["pass"], "kept": s.g3["kept"],
                               "min_rate_note_template": _min_rate(s.g3["per_note"]),
                               "min_rate_register_template": _min_rate(s.g3["per_register"]),
                               "quarantined_registers": s.g3["per_register"]["quarantined"]},
                      "G-SL": "lint at ingest (haiku_author check_* + gsl.lint_template / lint_freeform / lint_values), "
                              "re-run on the validated answers; dropped pieces are in quarantine.json",
                      "G13_seed": "not run here (C2_DATA_SPEC 6.4 step 4: run on pools/ after promotion)"},
            "reads": {"v1": s.v1_read_summaries, "redo2_stage_A": s.r2_summaries["A"], "redo2_stage_B": s.r2_summaries["B"]},
            "validation": validation, "answer_problems": s.answer_problems, "notes": s.notes, "v1_comparison": s.cmp,
            "files": files,
            "informational": s.info, "pending_forms": [{k: v for k, v in x.items() if k != "text"} for x in s.pending]}


def votes_report(s: SimpleNamespace) -> dict:
    forms = {}
    for fid in sorted(s.status):
        f = s.reg.forms[fid]
        forms[fid] = {"status": s.status[fid], "qform": qform_of(f.sem_id), "held_out": f.held_out,
                      "v1_reads": s.v1_votes.get(fid, []), "redo2_reads": s.r2_votes.get(fid, []),
                      "required": f.required}
    return {"gate": "G-LEX", "rule": "question forms 2/2 (3/3 for precedence and window; T23 has none); v1 reads count "
            "only together with BOTH redo2 reads (G0 v3 10 B1); any read that picks another meaning, a decoy or an invalid "
            "choice rejects for good; a v1 rejection is final; forms that negate their question frame are excluded "
            "before any read",
            "status_counts": dict(sorted(Counter(s.status.values()).items())),
            "reads_summary": {"v1": s.v1_read_summaries, "redo2": s.r2_summaries}, "forms": forms}


def refuse_v1_path(p: Path) -> None:
    if V1_POOLS.resolve() in Path(p).resolve().parents or Path(p).resolve() == V1_POOLS.resolve():
        raise PermissionError(f"freeze_v2 never writes into the v1 pools folder: {p}")


def freeze_outputs(s: SimpleNamespace, summary: dict) -> dict:
    """{file name under pools_v2/: text}: the seven pool files, the three reports and MANIFEST.json (deterministic)."""
    validation_report = {"family": FAMILY, "version": VERSION,
                         "note": ("every answer file of every round against its task contract; nothing was edited. A "
                                  "rejected file or item is treated as unanswered. The file-access audit "
                                  "(c2_kit.audit) needs the agents' transcripts, which this script does not open."),
                         "audit_failed_ignored": s.audit_failed, "chunk_integrity": s.integrity,
                         "ambiguity_pass": s.ambiguity, "rounds": {n: slim(r) for n, r in s.rounds.items()}}
    vtext = jtext(validation_report)
    votes_text = jtext(s.votes_report)
    g3_text = jtext(s.g3h_report)
    v1_manifest = V1_POOLS / "manifest.json"
    manifest = {
        "family": FAMILY, "version": VERSION, "stage": "admit + freeze v2 (redo2 round folded in; freeze_v2.py)",
        "status": summary["status"], "ready": s.ready,
        "supersedes": {"path": "families/T23/pools/manifest.json", "sha256": s.cmp["v1_manifest_sha256"],
                       "note": "v1 is untouched (pools/ is never written)"},
        "promote": LOADER_NOTE,
        "g0": {"path": "families/T23/G0_SPEC.md", "sha256": sha_text(G0.read_text(encoding="utf-8")),
               "pinned_in_plugin": P.T23.G0_SHA256, "v1_manifest_g0_sha256": json.loads(
                   v1_manifest.read_text(encoding="utf-8"))["g0_sha256"]},
        "prereg": "PREREG_FINAL.md Ruling A38 (OHS-4 frozen) present" if s.a38 else "A38 MISSING",
        "pool_files": s.file_rows,
        "reports": {"validation_report.json": {"sha256": sha_text(vtext)}, "glex_votes_report.json":
                    {"sha256": sha_text(votes_text)}, "g3h_compare_report.json": {"sha256": sha_text(g3_text)}},
        "validation": summary["validation"], "audit_failed_ignored": s.audit_failed, "notes": s.notes,
        "v1_comparison": s.cmp, "counts": s.counts, "targets": s.targets, "shortfalls": s.shortfalls,
        "gates": summary["gates"], "checks": s.checks, "informational": s.info, "reads": summary["reads"],
        "pending_forms": summary["pending_forms"],
        "sources": {name: {t: r["sha256"] for t, r in sorted(rd["files"].items())} for name, rd in s.rounds.items()},
        "not_verified": ["file-access audit (c2_kit.audit) of the authoring, extraction and redo2 agents: needs their "
                         "transcripts, not opened here; the orchestrator reports the failed-audit list used above",
                         "independence of the two G-LEX reads (one fresh agent per task file) follows from that audit",
                         "G13 decontamination, G5-H blind reads and G6 / G7 / G10 belong to the final mix (spec 6.3) and "
                         "need their own sealed-side checkers; pool counts are pre-selection (c2_select trims to the "
                         "spec 3.0 cells)"],
    }
    out = dict(s.texts)
    out.update({"validation_report.json": vtext, "glex_votes_report.json": votes_text,
                "g3h_compare_report.json": g3_text, "MANIFEST.json": jtext(manifest)})
    return out


def write_freeze(s: SimpleNamespace, summary: dict) -> dict:
    paths.require_a38()
    refuse_v1_path(POOLS_V2)
    out = freeze_outputs(s, summary)
    for rel in out:
        refuse_v1_path(POOLS_V2 / rel)
    paths.write_files(POOLS_V2, out)
    summary["manifest"] = str(POOLS_V2 / "MANIFEST.json")
    return summary


def verify_freeze(s: SimpleNamespace, summary: dict) -> dict:
    """pools_v2/ on disk against a fresh in-memory build, byte for byte (no file is written)."""
    out = freeze_outputs(s, summary)
    extra = sorted(p.name for p in POOLS_V2.iterdir() if p.is_file() and p.name not in out) if POOLS_V2.is_dir() else []
    diffs = diff_files(out, POOLS_V2)
    return {"identical": not diffs and not extra, "diffs": diffs, "extra_files": extra, "files": len(out)}


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    cmd = argv[0] if argv else "check"
    audit_failed = ()
    if "--audit-failed" in argv:
        i = argv.index("--audit-failed")
        audit_failed = tuple(x for x in argv[i + 1].split(",") if x)
    if cmd not in ("check", "freeze", "verify"):
        print(__doc__)
        return 2
    s = build(audit_failed=audit_failed)
    summary = summarize(s)
    if cmd == "freeze":
        write_freeze(s, summary)
    elif cmd == "verify":
        summary["verify"] = verify_freeze(s, summary)
    print(json.dumps(summary, indent=1, default=str, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

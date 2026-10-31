"""families/T32/freeze_v2.py: the T32 pool re-freeze (pools_v2/) after the redo2 Mode F round
(G0_SPEC.md v2.1 R13 and section 7; C2_DATA_SPEC 3.0, 6.3 G-SL, G-LEX, G3-H; PREREG A37 (b), A38).

Why a new script. freeze.py (v1) reads only haiku/author and haiku/extract. The redo2 Mode F answers (haiku/redo2:
2 authoring answers and 2 G3-H extraction answers) have no ingest path there, and redo2.py stops at
haiku/redo2/pool/*_pass.jsonl ("merging the passing intros into pools/ is a later freeze decision"). Nothing in v1 is
edited or overwritten: pools/, haiku/*, freeze.py, redo2.py, authoring.py, extract.py and the plugin stay byte for byte
as they are. This script reads them and writes only NEW files, under pools_v2/ (and only after A38).

What a run does:
  1. VALIDATES every answer file of every round against its contract (never edits a file, never "repairs" one):
       author, extract (G-LEX reads + G3-H), redo2/author, redo2/extract, plus the ambiguity pass record. The contract
       is read from the chunk file the agent was given (qids, the field the brief names, the number of strings asked,
       the item's choices); the chunk files are first checked against their manifests (sha256) and prompts. A FILE
       that breaks its contract is REJECTED whole (not UTF-8 / a BOM / not JSON / duplicate keys / not an array / an
       element that is not an object / a key set other than {"qid", field} / a qid unknown, repeated or missing / a
       wrong object count). An ITEM whose value breaks its contract (an empty or wrong-length list, an empty string)
       is rejected alone. Rejected answers are treated as unanswered, never as a vote. A G-LEX meaning that is not on
       the item's list, and a G3-H topic that is not one of the schema's choices, are not "invalid": they are
       non-matching reads (G0 H41: any other pick rejects the form; g3h.compare fails the intro).
       Task ids the orchestrator says to ignore (failed file-access audit) are rejected the same way (`--ignore`;
       this round the list is empty).
  2. REBUILDS the v1 pipeline from the validated answers only (collect, G-SL lint, dedup, lexicon registry, extraction
       batches), checks the rebuilt batches against the manifests and keys on disk, records the G-LEX reads (two
       independent reads glex-r1, glex-r2; 2/2 for every kind in T32: there are no precedence or window forms, so no
       3/3), scores the round-1 G3-H read and freezes packs exactly as v1 did. With unchanged answers the result is
       byte-identical to pools/ (checked and recorded per file).
  3. INGESTS the redo2 Mode F intros through redo2.py (its stricter lint, dedup against round 1 and the Mode T skins,
       the round-1 G3-H contract) and scores the redo2 G3-H read: ONE independent read per intro (the kit's G3-H is a
       single extraction compared with the generator's facts; an unanswered intro fails), >= 98% per template with
       template = register within the round (G0 section 7), a mismatched intro is always dropped, a register under
       the bar is quarantined whole. Round-1 quarantines stand: no round-1 intro is revived.
  4. APPLIES every G0 minimum and gate (nothing lowered) and writes pools_v2/ with MANIFEST.json (sha256 per file,
       counts, minimums, requested-size gaps, G-LEX and G3-H records, validation, how to load).

No label is set anywhere: golds come only from solver A and solver B; Haiku answers can only admit or drop a form or
an intro (A37 b). READY means: every G0 minimum below is met, the G-LEX gate passes over every form the pools use, and
nothing blocks (chunk / manifest / key mismatch, v1 rebuild off the disk files). The G0 section 7 "requested" sizes
(348 forms, 143 wordings, 168 skins, 120 intros, 42 packs, 40 attack notes) are authoring-request sizes, not minimums;
their gaps are listed in MANIFEST.requested_gaps and never hidden or relabelled.

  ../.venv/bin/python -B -m families.T32.freeze_v2 check                (from lean/c2_build; in memory, writes nothing)
  ../.venv/bin/python -B -m families.T32.freeze_v2 freeze               (writes pools_v2/; refuses before A38)
  ... check|freeze --ignore TASK_ID [TASK_ID ...]                       (answer files to ignore, e.g. a failed audit)

Exit code: 0 READY, 1 SHORT, 2 BLOCKED.

How the generator loads the pools (plugin.py reads no pool file: its fixtures / vocab stand-ins live in code; the
lexicon arrives as T32(lexicon=registry)):
  pools = freeze_v2.load_pools()                  # verifies every sha256 against pools_v2/MANIFEST.json
  plugin = P.T32(lexicon=pools["lexicon"])        # LexiconRegistry of the admitted forms (G-LEX 2/2)
  ctx = freeze_v2.kit_ctx(pools)                  # KitCtx(skins={id: Skin}, lexicon=...) from skins, attack notes, intros
  packs: pools["packs"] rows {id, setting, tasks, events, topics}
G13-seed (g13_c2.py, pinned) reads only <family>/pools/, so it does not see pools_v2/ unless the orchestrator points
it there or makes pools_v2/ the family's pools/ (a decision for the orchestrator; v1 is kept either way).
"""
from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, g3h, paths  # noqa: E402
from c2_kit import lexicon as LX  # noqa: E402
from c2_kit.plugin import KitCtx  # noqa: E402
from families.T32 import authoring as A  # noqa: E402
from families.T32 import extract as X  # noqa: E402
from families.T32 import fixtures as FX  # noqa: E402
from families.T32 import freeze as FZ  # noqa: E402
from families.T32 import plugin as P  # noqa: E402
from families.T32 import redo2 as R  # noqa: E402

FAMILY = "T32"
VERSION = "freeze-v2"
V1_POOLS = FZ.POOLS
POOLS_V2 = HERE / "pools_v2"
HAIKU = HERE / "haiku"
ROUNDS = {"author": HAIKU / "author", "extract": HAIKU / "extract",
          "redo2_author": R.AUTHOR_ROOT, "redo2_extract": R.EXTRACT_ROOT}
AMBIGUITY = HAIKU / "ambiguity" / "amb_T32.json"
IGNORED_TASKS: tuple = ()          # task ids whose answer files the orchestrator said to ignore (this round: none)

# ----------------------------------------------------------------------------------------------- G0 minimums
# Every number is a ">=" row of G0_SPEC.md (sections 2, 7, 1 R13) or C2_DATA_SPEC 3.0. Never lowered.
MIN_MESSAGE_PER_SEM = FZ.MIN_MESSAGE_PER_SEM       # 12 per sem (13 sems)
MIN_WORDING_PER_QFORM = FZ.MIN_WORDING_PER_QFORM   # 3 per question form (10 forms)
MIN_WORDINGS_TOTAL = 30                            # H40
PACKS_PER_SETTING = FZ.PACKS_FROZEN_PER_SETTING    # 5 per setting (6 settings): 30 frozen; spec 3.0: >= 25 packs
MIN_SKINS_PER_REGISTER = FZ.MIN_SKINS_PER_REGISTER  # 6 (9 training + 2 held-out registers)
MIN_REGISTERS, MIN_HELD_REGISTERS = 8, 2           # spec 3.0
MIN_PACK = FZ.MIN_PACK                             # 8 tasks, 5 events, 3 topics
SKIN_ROW_CAP = 6                                   # spec 3.0: each skin feeds <= 6 rows
SELECTED_ROWS, MODE_T_MIN_SHARE = 800, 0.60        # G0 R13: Mode T >= 60% (Mode F <= 40%)
G3H_BAR = g3h.PASS_RATE                            # 0.98 per template
REQUESTED = dict(FZ.REQUESTED)                     # G0 section 7 authoring-request sizes (not minimums)

AUTHOR_FIELDS = {"author_freeform": ("intros",), "author_lexicon": ("forms",), "author_skin": ("skins", "lines"),
                 "author_wording": ("wordings",), "author_pack": ("pack",)}
PACK_KEYS = ("events", "tasks", "topics")
NONE_WORD = "NONE"
UTF8_BOM = "\ufeff"


# ================================================================================================ 1. validation
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
    """What one Haiku task gave the agent: its kind, its items in order (qid -> item) and its answer path."""
    task_id: str
    kind: str
    items: dict
    answer_file: str = ""
    source: str = ""

    @property
    def qids(self) -> list:
        return list(self.items)


def defs_from_chunks(chunk_dir: Path) -> dict:
    out = {}
    if not Path(chunk_dir).is_dir():
        return out
    for f in sorted(Path(chunk_dir).glob("*.json")):
        c = json.loads(f.read_text(encoding="utf-8"))
        out[c["task_id"]] = ChunkDef(c["task_id"], c["kind"], {it["qid"]: it for it in c["items"]},
                                     c.get("answer_file", ""), f.name)
    return out


def item_contract(kind: str, item: dict) -> dict | None:
    """What an answer object for this item must hold besides its qid, from the item the agent saw; None when the
    contract cannot be derived (the file is then rejected: the contract source is unclear)."""
    if kind in AUTHOR_FIELDS:
        brief = item.get("brief", "")
        m = re.search(r'Answer field: \\?"(\w+)\\?"', brief)
        if not m or m.group(1) not in AUTHOR_FIELDS[kind]:
            return None
        fld = m.group(1)
        if fld == "pack":
            return {"shape": "pack", "keys": {"qid", "pack"}}
        n = re.search(r"\(a list of (\d+)\b", brief) or re.search(r"\bWrite (\d+)\b", brief)
        if not n:
            return None
        return {"shape": "list", "field": fld, "n": int(n.group(1)), "keys": {"qid", fld}}
    if kind == "extract_lex":
        ch = item.get("choices")
        if not isinstance(ch, list) or not ch:
            return None
        return {"shape": "meaning", "choices": list(ch), "keys": {"qid", "meaning"}}
    if kind == "extract_g3h":
        topics = [s for d in item.get("schema", []) if d.get("field") == "topic" for s in d.get("choices", [])]
        if not topics:
            return None
        return {"shape": "g3h", "choices": topics, "keys": {"qid", "topic", "owner"}}
    return None


def _nonempty(v) -> bool:
    return isinstance(v, str) and bool(v.strip())


def _check_item(con: dict, el: dict) -> tuple:
    """(problems, off_list). Problems reject the item; off_list marks a read that is not on the item's list."""
    pr, off = [], False
    sh = con["shape"]
    if sh == "list":
        v = el[con["field"]]
        if not isinstance(v, list):
            pr.append(f"{con['field']} is not a list")
        elif len(v) != con["n"]:
            pr.append(f"{con['field']} holds {len(v)} strings; the item asks for exactly {con['n']}")
        elif not all(_nonempty(s) for s in v):
            pr.append(f"{con['field']} holds an empty or non-string entry")
    elif sh == "pack":
        v = el["pack"]
        if not isinstance(v, dict) or set(v) != set(PACK_KEYS):
            pr.append("pack is not an object with exactly the lists events, tasks and topics")
        else:
            for k in PACK_KEYS:
                if not isinstance(v[k], list) or not all(_nonempty(s) for s in v[k]):
                    pr.append(f"pack.{k} is not a list of non-empty strings")
    elif sh == "meaning":
        if not _nonempty(el["meaning"]):
            pr.append("meaning is not a non-empty string")
        else:
            off = el["meaning"] not in con["choices"]
    elif sh == "g3h":
        for k in ("topic", "owner"):
            if not _nonempty(el[k]):
                pr.append(f"{k} is not a non-empty string")
        if not pr:
            off = el["topic"] != NONE_WORD and el["topic"] not in con["choices"]
    return pr, off


def validate_answer_bytes(data: bytes, cd: ChunkDef) -> dict:
    """Validate one answer file against its task. Never edits anything. Returns {"ok", "n_expected", "n_valid_items",
    "file_problems", "item_problems", "off_list", "in_order", "items"}; items = the accepted objects, as written."""
    rep = {"ok": False, "n_expected": len(cd.items), "n_valid_items": 0, "file_problems": [], "item_problems": [],
           "off_list": [], "in_order": None, "items": []}
    fp = rep["file_problems"]
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as e:
        fp.append(f"not UTF-8: {e}")
        return rep
    if text.startswith(UTF8_BOM):
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
    cons = {q: item_contract(cd.kind, it) for q, it in cd.items.items()}
    bad = [q for q, c in cons.items() if c is None]
    if bad:
        fp.append(f"contract not derivable from the task for {len(bad)} item(s) (first: {bad[0]})")
        return rep
    seen, order = {}, []
    for i, el in enumerate(obj):
        if not isinstance(el, dict):
            fp.append(f"element {i} is not an object")
            continue
        qid = el.get("qid")
        if not isinstance(qid, str):
            fp.append(f"element {i}: qid is not a string")
        elif qid not in cd.items:
            fp.append(f"element {i}: unknown qid {qid}")
        elif qid in seen:
            fp.append(f"qid {qid} used twice")
        elif set(el) != cons[qid]["keys"]:
            fp.append(f"element {i}: keys {sorted(el)} differ from the contract {sorted(cons[qid]['keys'])}")
        else:
            seen[qid] = el
            order.append(qid)
    if len(obj) != len(cd.items):
        fp.append(f"{len(obj)} objects; the contract says exactly {len(cd.items)} (one per item)")
    missing = [q for q in cd.items if q not in seen]
    if missing:
        fp.append(f"{len(missing)} qid(s) not answered (first: {missing[0]})")
    if fp:
        return rep
    rep["in_order"] = order == list(cd.items)
    for el in obj:                                       # file order is kept (the family loader reads in file order)
        pr, off = _check_item(cons[el["qid"]], el)
        if pr:
            rep["item_problems"].append(f"{el['qid']}: " + "; ".join(pr))
            continue
        if off:
            rep["off_list"].append(el["qid"])
        rep["items"].append(el)
    rep["ok"] = True
    rep["n_valid_items"] = len(rep["items"])
    return rep


def _sha_text(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def check_integrity(root: Path) -> list:
    """Problems with the task files an agent read: every chunk must equal its manifest entry (sha256), every manifest
    must have its key file, every prompt file must hash to the prompt sha. The contract is read from these chunks, so a
    mismatch blocks the round."""
    root, pr, listed = Path(root), [], set()
    for mf in sorted((root / "manifest").glob("*.json")):
        m = json.loads(mf.read_text(encoding="utf-8"))
        if not (root / "key" / mf.name).is_file():
            pr.append(f"{mf.name}: no key file")
        pf = root / "prompts" / f"{m['prompt_sha'][:16]}.txt"
        if not pf.is_file():
            pr.append(f"{mf.name}: no prompt file")
        elif _sha_text(pf.read_text(encoding="utf-8")) != m["prompt_sha"]:
            pr.append(f"{mf.name}: prompt file does not hash to prompt_sha")
        for t in m["tasks"]:
            listed.add(t["task_id"])
            cp = root / "chunks" / f"{t['task_id']}.json"
            if not cp.is_file():
                pr.append(f"{t['task_id']}: chunk file missing")
                continue
            c = json.loads(cp.read_text(encoding="utf-8"))
            if _sha_text(json.dumps(c, sort_keys=True, ensure_ascii=False)) != t["sha256"]:
                pr.append(f"{t['task_id']}: chunk file differs from its manifest entry")
            if c.get("prompt_sha") != m["prompt_sha"]:
                pr.append(f"{t['task_id']}: chunk prompt_sha differs from the manifest")
    for cp in sorted((root / "chunks").glob("*.json")):
        if cp.stem not in listed:
            pr.append(f"{cp.stem}: chunk file not listed in any manifest")
    return pr


def index_task_ids(name: str) -> set | None:
    """The task ids the round's task index lists (None when there is no index)."""
    try:
        if name == "author":
            return {t["task_id"] for t in json.loads((ROUNDS[name] / "tasks.json").read_text("utf-8"))["tasks"]}
        if name == "extract":
            return {t["task_id"] for t in json.loads((ROUNDS[name] / "TASKS.json").read_text("utf-8"))["tasks"]}
        idx = json.loads((R.ROOT / "REDO2_TASKS.json").read_text("utf-8"))["tasks"]
        return {t["task_id"] for t in idx if t["stage"] == name.split("_", 1)[1]}
    except (OSError, ValueError, KeyError):
        return None


def _rel(p: Path) -> str:
    try:
        return Path(p).resolve().relative_to(HERE.resolve()).as_posix()
    except ValueError:
        return str(p)


def validate_round(name: str, root: Path, ignore: tuple = ()) -> dict:
    """Validate every answer file of one round. A task with no file is `missing`; a file with no task is `stray`
    (never used; README.txt is listed there)."""
    root = Path(root)
    defs = defs_from_chunks(root / "chunks")
    adir = root / "answers"
    present = {p.name: p for p in sorted(adir.iterdir()) if p.is_file()} if adir.is_dir() else {}
    files, missing = {}, []
    for tid, cd in sorted(defs.items()):
        p = present.get(f"{tid}.json")
        if p is None:
            missing.append(tid)
            continue
        paths.check_path(p)
        data = p.read_bytes()
        rep = validate_answer_bytes(data, cd)
        rep.update(file=_rel(p), sha256=hashlib.sha256(data).hexdigest(), bytes=len(data), kind=cd.kind,
                   path_matches_task=bool(cd.answer_file) and Path(cd.answer_file).resolve() == p.resolve(),
                   ignored=False)
        if tid in ignore:
            rep.update(ok=False, ignored=True, items=[], n_valid_items=0)
            rep["file_problems"].append("ignored: the orchestrator ruled this answer file out (audit failed)")
        files[tid] = rep
    index = index_task_ids(name)
    return {"round": name, "dir": _rel(root), "tasks": len(defs), "files": files, "missing": sorted(missing),
            "stray": sorted(n for n in present if not (n.endswith(".json") and n[:-5] in defs)),
            "rejected": sorted(t for t, r in files.items() if not r["ok"]),
            "item_rejects": sum(len(r["item_problems"]) for r in files.values()),
            "off_list_items": sum(len(r["off_list"]) for r in files.values()),
            "integrity_problems": check_integrity(root),
            "index_problems": ([] if index is None or index == set(defs) else
                               [f"task index lists {len(index)} task(s), chunk folder holds {len(defs)}; "
                                f"differ: {sorted(index ^ set(defs))[:3]}"])}


def accepted(rep: dict) -> dict:
    """{task_id: accepted answer objects} of a validated round (rejected files are absent)."""
    return {t: r["items"] for t, r in rep["files"].items() if r["ok"]}


def validate_ambiguity() -> dict:
    """The G0 ambiguity pass record (informational: it is the pass that produced G0 v2, not a pool input)."""
    rep = {"file": _rel(AMBIGUITY), "ok": False, "problems": []}
    try:
        data = AMBIGUITY.read_bytes()
        d = json.loads(data.decode("utf-8"), object_pairs_hook=_no_dup_pairs)
    except (OSError, ValueError, _Strict) as e:
        rep["problems"].append(str(e))
        return rep
    rep["sha256"] = hashlib.sha256(data).hexdigest()
    pts = d.get("points") if isinstance(d, dict) else None
    if not isinstance(pts, list) or d.get("n_points") != len(pts):
        rep["problems"].append("points is not a list of n_points entries")
        return rep
    for p in pts:
        if not (isinstance(p, dict) and {"h", "where", "issue", "readings", "resolution"} <= set(p)):
            rep["problems"].append(f"point {p.get('h') if isinstance(p, dict) else p!r}: missing fields")
    rep.update(ok=not rep["problems"], n_points=len(pts), g0_sha256_in_file=d.get("g0_sha256"),
               note="records G0 v2; the current G0 v2.1 sha differs by design (v2.1 added only the Mode F wording note)")
    return rep


def validate_all(ignore: tuple = ()) -> dict:
    rounds = {n: validate_round(n, root, ignore) for n, root in ROUNDS.items()}
    return {"rounds": rounds, "ambiguity": validate_ambiguity(), "ignored": list(ignore),
            "redo": "no haiku/redo folder exists; the only redo round is haiku/redo2"}


def validation_ok(val: dict) -> bool:
    return all(not r["rejected"] and not r["missing"] and not r["integrity_problems"] and not r["index_problems"]
               for r in val["rounds"].values())


def slim(val: dict) -> dict:
    """The validation report without the accepted items (for the manifest sidecar)."""
    out = {"ignored": val["ignored"], "redo": val["redo"], "ambiguity": val["ambiguity"], "rounds": {}}
    for n, r in val["rounds"].items():
        s = {k: v for k, v in r.items() if k != "files"}
        s["files"] = {t: {k: v for k, v in f.items() if k != "items"} for t, f in r["files"].items()}
        out["rounds"][n] = s
    return out


# ================================================================================================ 2. v1 rebuild
def collect_validated(author_ok: dict) -> tuple:
    """X.collect() over validated answers only: ({pool: [piece]}, {pool: authored}, coverage). The pieces are the ones
    authoring._check_answer makes (the family loader's own checks); same order as authoring.load (task id, file)."""
    idx = json.loads((A.ROOT / "tasks.json").read_text(encoding="utf-8"))
    pools, authored = {}, Counter()
    cov = {"missing_tasks": [], "unanswered_items": 0}
    for t in sorted(idx["tasks"], key=lambda t: t["task_id"]):
        tid = t["task_id"]
        key = json.loads((A.ROOT / "key" / f"{t['batch_id']}.json").read_text(encoding="utf-8"))["key"]
        chunk = json.loads(Path(t["task_file"]).read_text(encoding="utf-8"))
        items = {it["qid"]: it for it in chunk["items"]}
        raw = author_ok.get(tid)
        if raw is None:
            cov["missing_tasks"].append(tid)
            cov["unanswered_items"] += len(items)
            continue
        seen = set()
        for a in raw:
            seen.add(a["qid"])
            for p in A._check_answer(key[a["qid"]], items[a["qid"]], a, tid, t["prompt_sha"]):
                q = dict(p)
                q["pool"], q["label"] = t["pool"], t["label"]
                pools.setdefault(t["pool"], []).append(q)
                authored[t["pool"]] += 1
        cov["unanswered_items"] += len(set(items) - seen)
    return pools, dict(authored), cov


def rebuild(author_ok: dict) -> dict:
    """FZ.rebuild() over validated answers (the extraction batches must still match the disk)."""
    pools, authored, cov = collect_validated(author_ok)
    surv, lint_drops = X.lint_all(pools)
    sample_probs = X.lint_values_samples()
    surv, dup_drops = X.dedup_all(surv)
    lex_in = surv.pop("message_forms", []) + surv.pop("wordings", [])
    reg, form_drops = X.build_registry(lex_in)
    bad_unit = [f.form_id for f in reg.forms.values() if not f.unit_ok]
    g3 = surv.get("freeform", []) + surv.get("freeform_held", [])
    batches, task_counts = X.make_tasks(reg, g3)
    return {"pools": pools, "authored": authored, "coverage": cov, "surv": surv, "lint_drops": lint_drops,
            "sample_probs": sample_probs, "dup_drops": dup_drops, "lex_in": lex_in, "reg": reg,
            "form_drops": form_drops, "bad_unit": bad_unit, "g3": g3, "batches": batches,
            "task_counts": task_counts}


def verify_disk(batches: list) -> tuple:
    """(on-disk manifest / key sha256s, problems). The rebuilt batches must equal the manifests and keys on disk."""
    try:
        return FZ.verify_disk(batches), []
    except (SystemExit, OSError, ValueError, KeyError) as e:
        return {}, [str(e)]


def load_answers(batches: list, ext_ok: dict) -> tuple:
    """({read: ({internal id: answer}, batch)}, coverage) from validated extraction answers."""
    out, cov = {}, {}
    for read, _kind, b in batches:
        tids = [c["task_id"] for c in b.chunks]
        raw = {t: ext_ok[t] for t in tids if t in ext_ok}
        o, pr = chunker.load_answers(b, raw)
        out[read] = (o, b)
        cov[read] = {"tasks": len(tids), "answered_tasks": len(raw), "items": len(b.key), "answered": len(o),
                     "chunk_problems": [x for x in pr if "unanswered" not in x]}
    return out, cov


def g3h_results(pieces: list, got: dict) -> tuple:
    """(per intro [{iid, register, ok, diffs}], template report). An unanswered intro fails (kit rule)."""
    rows, res = [], []
    for p in pieces:
        a = got.get(p["iid"])
        ok, diffs = (False, ["unanswered"]) if a is None else g3h.compare(X.g3h_expect(p), a, list(X.G3H_FIELDS))
        rows.append({"iid": p["iid"], "register": p["register"], "ok": ok, "diffs": diffs})
        res.append((p["register"], p["iid"], ok))
    return rows, g3h.template_report(res)


# ================================================================================================ 3. redo2
def redo2_stage(author_ok: dict, ext_ok: dict) -> dict:
    """redo2.py's own pipeline over validated answers: lint (stricter, dedup vs round 1 and Mode T), the G3-H batch, and
    the G3-H score (register within the round, 98%). Returns problems (a mismatch with the disk blocks) or results."""
    blocked = []
    batches = R.author_batches()
    for _label, b in batches:
        try:
            R._verify(b, R.AUTHOR_ROOT)
        except (SystemExit, OSError, ValueError, KeyError) as e:
            blocked.append(f"redo2 authoring batch: {e}")
    if blocked:
        return {"blocked": blocked}
    pieces, probs = R.lint_answers(batches, dict(author_ok), R._round1_templates())
    gb = R.g3h_batch(pieces)
    out = {"blocked": [], "pieces": pieces, "lint_problems": probs, "batch": gb,
           "authored": len(pieces), "lint_ok": sum(p["ok"] for p in pieces)}
    if gb is None:
        out.update(per_intro={}, report={"templates": {}, "quarantined": [], "bar": G3H_BAR}, passed=[], got={})
        return out
    try:
        R._verify(gb, R.EXTRACT_ROOT)
    except (SystemExit, OSError, ValueError, KeyError) as e:
        return {"blocked": [f"redo2 G3-H batch: {e}"]}
    raw = {c["task_id"]: ext_ok[c["task_id"]] for c in gb.chunks if c["task_id"] in ext_ok}
    sc = R.score_reads(pieces, gb, raw)
    got, _pr = chunker.load_answers(gb, raw)
    out.update(per_intro=sc["per_intro"], report=sc["report"], passed=sc["passed"], got=got,
               g3h_chunk_problems=sc["answer_problems"],
               tasks={"tasks": len(gb.chunks), "answered_tasks": len(raw)})
    return out


# ================================================================================================ 4. assemble
def _sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _jsonl_bytes(rows: list) -> bytes:
    return "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows).encode("utf-8")


def _json_bytes(obj) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, indent=1) + "\n").encode("utf-8")


def _free_row(p: dict, rnd: str) -> dict:
    row = FZ._free_row(p, True)
    row["round"] = rnd
    return row


def v1_view(rb: dict, answers: dict) -> dict:
    """What freeze.run() derives from the rebuilt pipeline and the G-LEX / G3-H reads (same rules, same order)."""
    reg = rb["reg"]
    lex_reads = FZ.record_lex(reg, answers)
    adm = FZ.admission(reg)
    got3 = answers[FZ.G3H_READ][0]
    g3_rows, g3_rep = g3h_results(rb["g3"], got3)
    g3_by = {r["iid"]: r for r in g3_rows}
    admitted = sorted(fid for fid, (s, _e) in adm.items() if s == "admitted")
    adm_set = set(admitted)
    quarantine = []
    for pc in rb["lex_in"]:
        if not pc.get("ok"):
            continue
        fid = FZ.piece_fid(pc)
        if fid not in reg.forms:
            raise SystemExit(f"piece {pc['iid']} maps to no registry form")
        if fid not in adm_set:
            status, ext = adm[fid]
            quarantine.append({"stage": "G-LEX", "pool": "wordings" if "qform" in pc else "message_forms",
                               "id": pc["iid"], "task_id": pc["task_id"], "form_id": fid, "status": status,
                               "text": pc["out"], "reads": [[r, s] for r, s in ext],
                               "reasons": [f"{r} picked {reg.sems[s].meaning!r}" if s else f"{r} did not pick its own "
                                           f"meaning" for r, s in ext if s != reg.forms[fid].sem_id]})
    for ent in rb["form_drops"]:
        quarantine.append({"stage": "lexicon_form", "pool": ent["pool"], "id": ent["pid"], "task_id": ent["task_id"],
                           "reasons": ent["reasons"]})
    adm_lex = FZ.admitted_registry(reg, admitted)
    frozen, reserve, pack_quar = FZ.freeze_packs(rb["surv"]["packs"])
    for q in pack_quar:
        quarantine.append({"stage": "pack_surface", "pool": "packs", "id": q["pack"]["iid"],
                           "task_id": q["pack"]["task_id"], "reasons": q["reasons"]})
    for d in rb["lint_drops"]:
        quarantine.append({"stage": "G-SL lint", "pool": d["pool"], "id": d["pid"], "task_id": d["task_id"],
                           "reasons": d["reasons"]})
    for d in rb["dup_drops"]:
        quarantine.append({"stage": "dedup", "pool": d["pool"], "id": d["pid"], "task_id": d["task_id"],
                           "reasons": d["reasons"]})
    qregs = set(g3_rep["quarantined"])
    free_pass = []
    for p in rb["g3"]:
        r = g3_by[p["iid"]]
        if r["ok"] and p["register"] not in qregs:
            free_pass.append(p)
            continue
        why = []
        if not r["ok"]:
            why.append("G3-H mismatch: " + "; ".join(r["diffs"]))
        if p["register"] in qregs:
            why.append(f"G3-H register quarantined ({g3_rep['templates'][p['register']]['rate']:.1%} < 98%)")
        quarantine.append({"stage": "G3-H", "pool": "freeform_held" if p["held_out"] else "freeform", "id": p["iid"],
                           "task_id": p["task_id"], "register": p["register"], "text": p["out"], "reasons": why})
    return {"reg": reg, "adm": adm, "admitted": admitted, "adm_lex": adm_lex, "lex_reads": lex_reads,
            "g3_rows": g3_rows, "g3_rep": g3_rep, "free_pass": free_pass, "frozen": frozen, "reserve": reserve,
            "pack_quar": pack_quar, "quarantine": quarantine, "qregs": qregs}


def _pool_rows(rb: dict, v1: dict, r2: dict) -> tuple:
    """({file: rows}, redo2 quarantine entries, pieces by pool)."""
    surv = rb["surv"]
    skins = [p for p in surv["skins"] if not p["held_out"]]
    skins_held = [p for p in surv["skins_held"] if p["held_out"]]
    if any(p["held_out"] for p in skins) or any(not p["held_out"] for p in skins_held):
        raise SystemExit("held-out flag does not match the pool")
    r1_train = [p for p in v1["free_pass"] if not p["held_out"]]
    r1_held = [p for p in v1["free_pass"] if p["held_out"]]
    r2_pass = r2.get("passed", [])
    r2_train = [p for p in r2_pass if not p["held_out"]]
    r2_held = [p for p in r2_pass if p["held_out"]]
    q2 = []
    for p in r2.get("pieces", []):
        if not p["ok"]:
            q2.append({"stage": "redo2 lint", "pool": "freeform_held" if p["held_out"] else "freeform", "id": p["iid"],
                       "task_id": p["task_id"], "register": p["register"], "text": p["raw"], "reasons": p["problems"]})
    passed_ids = {p["iid"] for p in r2_pass}
    for p in r2.get("pieces", []):
        if p["ok"] and p["iid"] not in passed_ids:
            d = r2["per_intro"].get(p["iid"], {"ok": False, "diffs": ["unanswered"]})
            tpl = r2["report"]["templates"].get(f"{R.ROUND}:{p['register']}", {})
            why = []
            unread = d["diffs"] == ["unanswered"]
            if not d["ok"]:
                why.append("G3-H unanswered (no valid read: the answer file is missing, rejected or ignored)"
                           if unread else "G3-H mismatch: " + "; ".join(d["diffs"]))
            if tpl.get("quarantined") and not unread:
                why.append(f"G3-H register quarantined in redo2 ({tpl['rate']:.1%} < 98%)")
            q2.append({"stage": "redo2 G3-H", "pool": "freeform_held" if p["held_out"] else "freeform",
                       "id": p["iid"], "task_id": p["task_id"], "register": p["register"], "text": p["out"],
                       "reasons": why})
    rows = {
        "skins.jsonl": [FZ._skin_row(p, "skins") for p in skins],
        "skins_held.jsonl": [FZ._skin_row(p, "skins_held") for p in skins_held],
        "attack_notes.jsonl": [FZ._attack_row(p) for p in surv["attack_notes"]],
        "packs.jsonl": [FZ._pack_row(p) for p in sorted(v1["frozen"], key=lambda p: (
            A.ALL_SETTINGS.index(p["setting"]), FZ._index(p["iid"])))],
        "packs_reserve.jsonl": [FZ._pack_row(p) for p in v1["reserve"]],
        "freeform.jsonl": [_free_row(p, "r1") for p in r1_train] + [_free_row(p, R.ROUND) for p in r2_train],
        "freeform_held.jsonl": [_free_row(p, "r1") for p in r1_held] + [_free_row(p, R.ROUND) for p in r2_held],
        "lexicon_admitted.jsonl": [FZ._lex_row(v1["reg"], fid) for fid in v1["admitted"]],
        "quarantine.jsonl": v1["quarantine"] + q2,
    }
    return rows, q2


def votes_rows(v1: dict, rb: dict, answers: dict, r2: dict) -> list:
    """Every vote, for the sidecar: G-LEX (extractor id, sem or null) per form; G3-H read per intro."""
    out = []
    reg = v1["reg"]
    for fid in sorted(reg.forms):
        f = reg.forms[fid]
        out.append({"gate": "G-LEX", "form_id": fid, "sem_id": f.sem_id, "kind": f.kind,
                    "required": f.required, "status": reg.status(fid), "reads": [[e, s] for e, s in f.extractions]})
    got3 = answers[FZ.G3H_READ][0]
    for r in v1["g3_rows"]:
        out.append({"gate": "G3-H", "round": "r1", "read": FZ.G3H_READ, "iid": r["iid"], "register": r["register"],
                    "ok": r["ok"], "diffs": r["diffs"], "answer": got3.get(r["iid"])})
    for iid, d in sorted(r2.get("per_intro", {}).items()):
        reg_name = iid.split("|")[1]
        out.append({"gate": "G3-H", "round": R.ROUND, "read": "redo2-g3h-r1", "iid": iid, "register": reg_name,
                    "ok": d["ok"], "diffs": d["diffs"], "answer": r2["got"].get(iid)})
    return out


# ================================================================================================ 5. G0 checks
def g0_checks(rows: dict, v1: dict, r2: dict, rb: dict) -> list:
    """The G0 minimums and gates, each {id, rule, source, need, have, met}. Nothing is lowered."""
    reg = v1["reg"]
    adm = v1["admitted"]
    msg = Counter(reg.forms[f].sem_id for f in adm if reg.forms[f].kind == "other")
    word = Counter(reg.forms[f].sem_id for f in adm if reg.forms[f].kind == "question")
    sems = sorted(FX.MESSAGE_MEANINGS)
    qf_sems = {qf: LX.question_sem(FAMILY, qf) for qf in sorted(FX.QUESTION_MEANINGS)}
    skins = rows["skins.jsonl"] + rows["skins_held.jsonl"]
    by_reg = Counter(p["register"] for p in skins)
    registers = tuple(P.T32.REGISTERS)
    held = tuple(P.T32.HELD_OUT_REGISTERS)
    packs = rows["packs.jsonl"]
    pack_by_set = Counter(p["setting"] for p in packs)
    surf = [s.casefold() for p in packs for k in ("tasks", "events", "topics") for s in p[k]]
    dup_surf = sorted(s for s, n in Counter(surf).items() if n > 1)
    short_packs = [p["id"] for p in packs if any(len(p[k]) < n for k, n in (("tasks", MIN_PACK["tasks"]),
                                                                          ("events", MIN_PACK["events"]),
                                                                          ("topics", MIN_PACK["topics"])))]
    train_skins = len(rows["skins.jsonl"])
    free_all = rows["freeform.jsonl"] + rows["freeform_held.jsonl"]
    gate_used = v1["adm_lex"].gate()
    thin = [f for f in adm if len({e for e, s in reg.forms[f].extractions if s == reg.forms[f].sem_id})
            < reg.forms[f].required]
    g3_ok = True
    tpl_rates = {}
    for rnd, rep in (("r1", v1["g3_rep"]), (R.ROUND, r2.get("report", {"templates": {}}))):
        for name, d in rep["templates"].items():
            tpl_rates[f"{rnd}:{name.split(':')[-1]}"] = d
    admitted_regs = {(r["round"], r["register"]) for r in free_all}
    for rnd, name in admitted_regs:
        d = tpl_rates.get(f"{rnd}:{name}")
        if d is None or d["rate"] < G3H_BAR:
            g3_ok = False
    chk = []

    def add(cid, rule, source, need, have, met, **extra):
        chk.append({"id": cid, "rule": rule, "source": source, "need": need, "have": have, "met": bool(met), **extra})

    add("message_forms_per_sem", "admitted message forms per sem (13 sems)", "G0 section 7", MIN_MESSAGE_PER_SEM,
        min(msg.get(s, 0) for s in sems), all(msg.get(s, 0) >= MIN_MESSAGE_PER_SEM for s in sems),
        by={s: msg.get(s, 0) for s in sems})
    add("wordings_per_qform", "admitted wordings per question form (10 forms)", "G0 section 7, H40",
        MIN_WORDING_PER_QFORM, min(word.get(s, 0) for s in qf_sems.values()),
        all(word.get(s, 0) >= MIN_WORDING_PER_QFORM for s in qf_sems.values()),
        by={qf: word.get(s, 0) for qf, s in qf_sems.items()})
    add("wordings_total", "admitted wordings over all forms", "G0 section 7, H40", MIN_WORDINGS_TOTAL,
        sum(word.values()), sum(word.values()) >= MIN_WORDINGS_TOTAL)
    add("packs_frozen_per_setting", "frozen packs per setting (6 settings; 30 frozen; spec 3.0 >= 25)",
        "G0 section 2, 7", PACKS_PER_SETTING, min(pack_by_set.get(s, 0) for s in A.ALL_SETTINGS),
        all(pack_by_set.get(s, 0) >= PACKS_PER_SETTING for s in A.ALL_SETTINGS) and len(packs) >= 25,
        by={s: pack_by_set.get(s, 0) for s in A.ALL_SETTINGS}, total=len(packs))
    add("pack_minimums", "every frozen pack holds >= 8 tasks, >= 5 events, >= 3 topics", "G0 section 7",
        dict(MIN_PACK), len(packs) - len(short_packs), not short_packs, short=short_packs)
    add("pack_surfaces_unique", "no task / event / topic phrase repeats across the frozen pool", "G0 section 7",
        0, len(dup_surf), not dup_surf, repeated=dup_surf[:5])
    add("skins_per_register", "admitted Mode T skins per register (9 training + 2 held-out)", "G0 section 7",
        MIN_SKINS_PER_REGISTER, min(by_reg.get(r, 0) for r in registers),
        all(by_reg.get(r, 0) >= MIN_SKINS_PER_REGISTER for r in registers), by={r: by_reg.get(r, 0) for r in registers})
    ok_regs = [r for r in registers if by_reg.get(r, 0) >= MIN_SKINS_PER_REGISTER]
    add("registers", "registers with >= 6 skins; of them held out", "spec 3.0", [MIN_REGISTERS, MIN_HELD_REGISTERS],
        [len(ok_regs), len([r for r in held if r in ok_regs])],
        len(ok_regs) >= MIN_REGISTERS and len([r for r in held if r in ok_regs]) >= MIN_HELD_REGISTERS)
    add("mode_t_capacity", "training Mode T skins x 6 rows >= 60% of 800 selected rows (Mode T >= 60%)",
        "G0 R13, spec 3.0", int(MODE_T_MIN_SHARE * SELECTED_ROWS), train_skins * SKIN_ROW_CAP,
        train_skins * SKIN_ROW_CAP >= MODE_T_MIN_SHARE * SELECTED_ROWS, training_skins=train_skins)
    add("g3h_per_template", "every admitted Mode F register passes G3-H >= 98% in its own round", "G0 section 7, 6.3",
        G3H_BAR, min([tpl_rates[f"{a}:{b}"]["rate"] for a, b in admitted_regs] or [1.0]), g3_ok,
        admitted_registers=sorted(f"{a}:{b}" for a, b in admitted_regs))
    add("g3h_pool_all_pass", "every Mode F intro in the pools is a G3-H pass (mismatches dropped)", "spec 6.3", True,
        all(r["g3h"] == "pass" for r in free_all), all(r["g3h"] == "pass" for r in free_all))
    add("held_out_split", "held-out registers feed only the held-out pools", "G0 section 2, spec 3.0", True,
        all(r["register"] in held for r in rows["skins_held.jsonl"] + rows["freeform_held.jsonl"])
        and not any(r["register"] in held for r in rows["skins.jsonl"] + rows["freeform.jsonl"]),
        all(r["register"] in held for r in rows["skins_held.jsonl"] + rows["freeform_held.jsonl"])
        and not any(r["register"] in held for r in rows["skins.jsonl"] + rows["freeform.jsonl"]))
    add("glex_gate_used_forms", "G-LEX over every form the pools use: all admitted", "spec 6.3 G-LEX",
        "pass", "pass" if gate_used["pass"] else "FAIL", gate_used["pass"], status_counts=gate_used["status_counts"],
        n_forms=gate_used["n_forms"])
    add("glex_two_of_two", "every admitted form has 2 independent matching reads (3 for precedence / window: none in "
        "T32)", "spec 6.3 G-LEX", 0, len(thin), not thin, thin=thin[:5])
    return chk


def requested_gaps(counts: dict, rows: dict) -> dict:
    """Authoring-request sizes (G0 section 7) against what was admitted. Informational, not minimums."""
    have = {"message_forms": counts["message_forms_admitted"], "wordings": counts["wordings_admitted"],
            "skins": len(rows["skins.jsonl"]) + len(rows["skins_held.jsonl"]),
            "freeform_intros": len(rows["freeform.jsonl"]) + len(rows["freeform_held.jsonl"]),
            "attack_notes": len(rows["attack_notes.jsonl"]), "packs": len(rows["packs.jsonl"])}
    return {k: {"requested": REQUESTED[k], "admitted": have[k], "gap": max(0, REQUESTED[k] - have[k]),
                "binding": False} for k in sorted(REQUESTED)}


# ================================================================================================ 6. run
def run(ignore: tuple = (), val: dict | None = None) -> dict:
    """The whole freeze in memory: {status, ...}. Writes nothing."""
    ignore = tuple(ignore) + tuple(t for t in IGNORED_TASKS if t not in ignore)
    prob = X.self_check()
    if prob:
        raise SystemExit("self-check failed: " + "; ".join(prob))
    val = val or validate_all(ignore)
    blocked = []
    for n, r in val["rounds"].items():
        blocked += [f"{n}: {p}" for p in r["integrity_problems"] + r["index_problems"]]
    ok = {n: accepted(r) for n, r in val["rounds"].items()}
    rb = rebuild(ok["author"])
    if rb["bad_unit"]:
        blocked.append(f"forms failing the unit test: {rb['bad_unit'][:3]}")
    disk_shas, vp = verify_disk(rb["batches"])
    blocked += vp
    if blocked:
        return {"status": "BLOCKED", "blocked": blocked, "validation": val}
    answers, ext_cov = load_answers(rb["batches"], ok["extract"])
    v1 = v1_view(rb, answers)
    r2 = redo2_stage(ok["redo2_author"], ok["redo2_extract"])
    if r2["blocked"]:
        return {"status": "BLOCKED", "blocked": r2["blocked"], "validation": val}
    rows, q2 = _pool_rows(rb, v1, r2)
    votes = votes_rows(v1, rb, answers, r2)
    reg = v1["reg"]
    adm = v1["admitted"]
    msg = Counter(reg.forms[f].sem_id for f in adm if reg.forms[f].kind == "other")
    word = Counter(reg.forms[f].sem_id for f in adm if reg.forms[f].kind == "question")
    g3 = v1["g3_rep"]
    r2rep = r2["report"]
    train_skins = len(rows["skins.jsonl"])
    f_train, f_held = len(rows["freeform.jsonl"]), len(rows["freeform_held.jsonl"])
    counts = {
        "authored_by_pool": rb["authored"],
        "author_coverage": rb["coverage"],
        "lint_dropped_by_pool": dict(Counter(d["pool"] for d in rb["lint_drops"])),
        "dedup_dropped_total": len(rb["dup_drops"]),
        "lexicon_candidates_after_lint": len(rb["lex_in"]),
        "lexicon_form_drops": len(rb["form_drops"]),
        "lexicon_forms_registry": len(reg.forms),
        "lexicon_forms_admitted": len(adm),
        "lexicon_forms_rejected_by_gLEX": sum(1 for s, _ in v1["adm"].values() if s == "rejected"),
        "lexicon_forms_pending": sum(1 for s, _ in v1["adm"].values() if s == "pending"),
        "lexicon_forms_admitted_by_kind": dict(Counter(reg.forms[f].kind for f in adm)),
        "glex_reads": v1["lex_reads"],
        "extraction_coverage": ext_cov,
        "message_forms_admitted": sum(msg.values()),
        "wordings_admitted": sum(word.values()),
        "message_admitted_by_sem": dict(sorted(msg.items())),
        "wording_admitted_by_qform": {qf: word.get(LX.question_sem(FAMILY, qf), 0)
                                      for qf in sorted(FX.QUESTION_MEANINGS)},
        "skins_admitted_by_register": dict(sorted(Counter(r["register"] for r in
                                                          rows["skins.jsonl"] + rows["skins_held.jsonl"]).items())),
        "skins_training": train_skins, "skins_held_out": len(rows["skins_held.jsonl"]),
        "skins_by_setting_training": dict(sorted(Counter(s for r in rows["skins.jsonl"]
                                                         for s in r["settings"]).items())),
        "packs_authored": len(rb["surv"]["packs"]), "packs_frozen": len(rows["packs.jsonl"]),
        "packs_frozen_by_setting": dict(sorted(Counter(r["setting"] for r in rows["packs.jsonl"]).items())),
        "packs_reserve": len(rows["packs_reserve.jsonl"]), "packs_quarantined_surface": len(v1["pack_quar"]),
        "attack_notes": len(rows["attack_notes.jsonl"]),
        "mode_f": {
            "round1": {"intros_read": len(rb["g3"]), "passed": len(v1["free_pass"]),
                       "register_rates": {k: [d["ok"], d["n"], round(d["rate"], 3), d["quarantined"]]
                                          for k, d in g3["templates"].items()},
                       "quarantined_registers": sorted(v1["qregs"])},
            "redo2": {"authored": r2["authored"], "lint_ok": r2["lint_ok"],
                      "lint_dropped": r2["authored"] - r2["lint_ok"],
                      "g3h_intros": len(r2["per_intro"]),
                      "g3h_mismatch": sum(not v["ok"] for v in r2["per_intro"].values()),
                      "register_rates": {k.split(":", 1)[1]: [d["ok"], d["n"], round(d["rate"], 3), d["quarantined"]]
                                         for k, d in r2rep["templates"].items()},
                      "quarantined_registers": [k.split(":", 1)[1] for k in r2rep["quarantined"]],
                      "passed_training": sum(1 for p in r2["passed"] if not p["held_out"]),
                      "passed_held_out": sum(1 for p in r2["passed"] if p["held_out"]),
                      "g3h_tasks": r2.get("tasks")},
            "pool_training": f_train, "pool_held_out": f_held,
            "by_register": dict(sorted(Counter(r["register"] for r in
                                               rows["freeform.jsonl"] + rows["freeform_held.jsonl"]).items())),
            "training_share_of_narrative_texts": round(f_train / max(1, f_train + train_skins), 4)},
        "quarantine_entries": len(rows["quarantine.jsonl"]),
        "quarantine_by_stage": dict(Counter(q["stage"] for q in rows["quarantine.jsonl"])),
        "vote_rows": len(votes),
    }
    checks = g0_checks(rows, v1, r2, rb)
    short = [f"{c['id']}: need {c['need']}, have {c['have']}" for c in checks if not c["met"]]
    return {"status": "READY" if not short else "SHORT", "blocked": [], "shortfalls": short, "checks": checks,
            "requested_gaps": requested_gaps(counts, rows), "counts": counts, "rows": rows, "votes": votes,
            "reg": reg, "adm_lex": v1["adm_lex"], "validation": val, "disk_shas": disk_shas,
            "ignored": list(ignore), "v1_identity": v1_identity(rows, v1["adm_lex"]),
            "lex_gate_used": {k: v for k, v in v1["adm_lex"].gate().items() if k != "not_admitted"},
            "lex_gate_registry": {k: v for k, v in reg.gate().items() if k != "not_admitted"},
            "rejected_forms": sorted(f for f, (s, _e) in v1["adm"].items() if s == "rejected")}


def v1_identity(rows: dict, adm_lex) -> dict:
    """For each file that v2 shares with v1: is it byte-identical to pools/? (From pools/MANIFEST.json shas.)"""
    out = {}
    try:
        man = json.loads((V1_POOLS / "MANIFEST.json").read_text(encoding="utf-8"))["files"]
    except (OSError, ValueError, KeyError):
        return {"error": "pools/MANIFEST.json not readable"}
    mine = {n: _sha_bytes(_jsonl_bytes(r)) for n, r in rows.items()}
    mine["lexicon_registry.json"] = _sha_bytes(_json_bytes(adm_lex.to_json()))
    for n, sha in sorted(mine.items()):
        v1sha = man.get(f"pools/{n}", {}).get("sha256")
        out[n] = "identical" if v1sha == sha else ("differs" if v1sha else "new")
    return out


# ================================================================================================ 7. write
HOW_TO_LOAD = {
    "plugin_reads_pool_files": False,
    "why": "plugin.py keeps vocab / fixtures stand-ins in code and takes its lexicon as T32(lexicon=registry); no "
           "configurable pool path exists, so nothing in the plugin was changed",
    "loader": "families.T32.freeze_v2.load_pools(root=pools_v2) verifies every sha256 against MANIFEST.json and "
              "returns {skins, skins_held, attack_notes, packs, packs_reserve, freeform, freeform_held, "
              "lexicon_admitted, quarantine, lexicon (LexiconRegistry of the admitted forms), manifest}",
    "plugin": "P.T32(lexicon=pools['lexicon'])",
    "ctx": "freeze_v2.kit_ctx(pools) -> KitCtx(skins={id: Skin} for Mode T skins, attack notes and Mode F intros, "
           "rebuilt through authoring.check_skin / check_freeform / check_attack; lexicon=registry)",
    "freeform_rows": "pools_v2/freeform*.jsonl carry round 'r1' (round-1 survivors) or 'redo2'; texts are Mode F intros "
                     "(author_mode F) with facts {OWNER, TOPIC}",
    "g13_seed": "g13_c2.py (pinned) scans only <family>/pools/. To run G13-seed on these pools the orchestrator must "
                "point pool_units() at pools_v2/ or make pools_v2/ the family's pools/ (v1 stays on disk); "
                "votes_sidecar.jsonl and validation_report.json match g13's SEED_SKIP and are not scanned",
}


class _GuardedWriter:
    """The kit's guarded writers (refuse before A38, never-open and outside-lean paths)."""
    write_json = staticmethod(paths.write_json)
    write_jsonl = staticmethod(paths.write_jsonl)


def build_manifest(res: dict, file_sha: dict) -> dict:
    counts = res["counts"]
    return {
        "family": FAMILY, "version": VERSION, "stage": "freeze_v2", "status": res["status"],
        "supersedes": "pools/ (v1) is kept unchanged; pools_v2/ = v1 rebuilt from validated answers + redo2 Mode F",
        "g0_spec": {"path": "families/T32/G0_SPEC.md", "sha256": P.T32.G0_SHA256},
        "prereg_final_sha256": hashlib.sha256(paths.PREREG.read_bytes()).hexdigest(),
        "inputs": {
            "v1_pools_manifest_sha256": _sha_bytes((V1_POOLS / "MANIFEST.json").read_bytes()),
            "v1_pools_files": {n: m["sha256"] for n, m in json.loads(
                (V1_POOLS / "MANIFEST.json").read_text(encoding="utf-8"))["files"].items()},
            "extract_manifests_and_keys": res["disk_shas"],
            "answer_files": {f"{n}/{t}": {"sha256": f["sha256"], "ok": f["ok"], "item_rejects": len(f["item_problems"])}
                             for n, r in res["validation"]["rounds"].items() for t, f in sorted(r["files"].items())},
        },
        "ignored_task_ids": res["ignored"],
        "ignored_note": "the orchestrator's ignore list for failed file-access audits was [] this round (nothing "
                        "ignored); c2_kit.audit records are not on disk in families/T32, so audit status is not "
                        "re-checked here",
        "decisions": {
            "validation": "every answer file is validated against its chunk (never edited); a broken file is rejected "
                          "whole, a broken item alone; rejected = unanswered, never a vote (validation_report.json)",
            "glex": "2/2 independent reads (glex-r1, glex-r2) via lexicon.status; 3/3 applies to precedence and window "
                    "kinds, which T32 does not have; off-list or 'none of these' picks reject the form (H41)",
            "g3h": "one independent extraction per intro compared with the generator facts (g3h.compare); an "
                   "unanswered intro fails; template = register within its round; < 98% quarantines the register; "
                   "mismatches always dropped; round-1 quarantines stand (no round-1 intro revived)",
            "redo2": "redo2.py lint (stricter than round 1, dedup against round 1 and the Mode T skins) then its G3-H "
                     "read; passing intros join freeform.jsonl / freeform_held.jsonl with round 'redo2'",
            "packs": f"first {PACKS_PER_SETTING} passing packs per setting in index order, no surface repeated in the "
                     "frozen pool; surplus packs are reserve (as v1)",
            "held_out": "skins_held and freeform_held carry held-out registers (sms_export, forum_thread): mixdev only",
            "ready": "READY = every G0 minimum in `minimums` met + G-LEX gate pass over the forms the pools use + "
                     "nothing blocked. `requested_gaps` are G0 section 7 authoring-request sizes, not minimums",
        },
        "targets_g0": {"message_forms_per_sem_min": MIN_MESSAGE_PER_SEM, "message_sems": len(FX.MESSAGE_MEANINGS),
                       "wordings_per_qform_min": MIN_WORDING_PER_QFORM, "wordings_total_min": MIN_WORDINGS_TOTAL,
                       "qforms": len(FX.QUESTION_MEANINGS), "packs_frozen_per_setting": PACKS_PER_SETTING,
                       "settings": len(A.ALL_SETTINGS), "skins_per_register_min": MIN_SKINS_PER_REGISTER,
                       "registers_min": MIN_REGISTERS, "held_out_registers_min": MIN_HELD_REGISTERS,
                       "pack_min_per_pack": MIN_PACK, "g3h_bar_per_template": G3H_BAR, "requested": REQUESTED},
        "minimums": res["checks"],
        "shortfalls": res["shortfalls"],
        "requested_gaps": res["requested_gaps"],
        "counts": counts,
        "gates": {"G-LEX_used_forms": res["lex_gate_used"], "G-LEX_whole_registry": res["lex_gate_registry"],
                  "G-LEX_rejected_forms_quarantined_not_used": res["rejected_forms"]},
        "v1_identity": res["v1_identity"],
        "how_to_load": HOW_TO_LOAD,
        "open_items": [
            "file-access audit: no audit records are on disk in families/T32; the orchestrator's ignore list was []. "
            "If the audit of the two redo2 G3-H tasks (T32-extract_g3h-9a1661ac-000 / -001) is later found failed, "
            "re-run `freeze_v2 freeze --ignore T32-extract_g3h-9a1661ac-000 T32-extract_g3h-9a1661ac-001`: the redo2 "
            "intros then stay unread (dropped), and every G0 minimum still holds (Mode F is not a minimum)",
            "redo2 G3-H is a single independent read per intro (the kit's G3-H); the redo2 Mode F intros pass it "
            "at 100% in every register",
            "G-LEX rejected 5 yn_dneg_broken wordings (readers split on the double negation: the G0 point-9 watch "
            "item); 5 remain admitted, above the 3 minimum",
            "G13-seed reads <family>/pools/ only: see how_to_load.g13_seed",
        ],
        "files": file_sha,
    }


def write_pools(res: dict, root: Path = POOLS_V2, w=_GuardedWriter) -> dict:
    """Writes pools_v2/. `w` is the kit's guarded writer pair (A38, never-open, inside lean/); tests pass plain ones."""
    root = Path(root)
    file_sha = {}
    for name, rows in res["rows"].items():
        p = w.write_jsonl(root / name, rows)
        file_sha[f"pools_v2/{name}"] = {"sha256": _sha_bytes(Path(p).read_bytes()), "rows": len(rows)}
    lr = res["adm_lex"].to_json()
    p = w.write_json(root / "lexicon_registry.json", lr)
    file_sha["pools_v2/lexicon_registry.json"] = {"sha256": _sha_bytes(Path(p).read_bytes()), "rows": len(lr["forms"])}
    p = w.write_jsonl(root / "votes_sidecar.jsonl", res["votes"])
    file_sha["pools_v2/votes_sidecar.jsonl"] = {"sha256": _sha_bytes(Path(p).read_bytes()), "rows": len(res["votes"])}
    rep = slim(res["validation"])
    p = w.write_json(root / "validation_report.json", rep)
    file_sha["pools_v2/validation_report.json"] = {"sha256": _sha_bytes(Path(p).read_bytes()),
                                                   "rows": sum(len(r["files"]) for r in rep["rounds"].values())}
    man = build_manifest(res, file_sha)
    w.write_json(root / "MANIFEST.json", man)
    return man


# ================================================================================================ 8. loader (generator)
def _read_jsonl(p: Path) -> list:
    return [json.loads(ln) for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip()]


def load_pools(root: Path = POOLS_V2, verify: bool = True) -> dict:
    """The frozen pools as the generator reads them. Verifies every sha256 against MANIFEST.json."""
    root = Path(root)
    man = json.loads((root / "MANIFEST.json").read_text(encoding="utf-8"))
    out = {"manifest": man}
    for rel, meta in man["files"].items():
        name = rel.split("/", 1)[1]
        data = (root / name).read_bytes()
        if verify and _sha_bytes(data) != meta["sha256"]:
            raise ValueError(f"{rel}: sha256 differs from MANIFEST.json")
        if name.endswith(".jsonl"):
            out[name[:-len(".jsonl")]] = [json.loads(ln) for ln in data.decode("utf-8").splitlines() if ln.strip()]
    out["lexicon"] = LX.LexiconRegistry.from_json(json.loads((root / "lexicon_registry.json").read_text("utf-8")))
    return out


def build_skins(pools: dict) -> tuple:
    """({skin_id: Skin}, problems): every Mode T skin, attack note and Mode F intro rebuilt through the family's own
    checks (G-SL, family extras, fill / parse round trip, value swap); a row that fails is a problem."""
    skins, probs = {}, []
    for pool in ("skins", "skins_held"):
        for r in pools[pool]:
            sk, pr = A.check_skin(r["register"], r["text"], sid=r["id"])
            if sk is None:
                probs.append(f"{r['id']}: {pr}")
            else:
                skins[r["id"]] = dataclasses.replace(sk, haiku_task_id=r["task_id"], haiku_prompt_sha=r["prompt_sha"])
    for r in pools["attack_notes"]:
        sk, pr = A.check_attack(r["text"], sid=r["id"])
        if sk is None:
            probs.append(f"{r['id']}: {pr}")
        else:
            skins[r["id"]] = dataclasses.replace(sk, haiku_task_id=r["task_id"], haiku_prompt_sha=r["prompt_sha"])
    for pool in ("freeform", "freeform_held"):
        for r in pools[pool]:
            sk, pr = A.check_freeform(r["register"], r["text"], r["facts"], sid=r["id"], task_id=r["task_id"],
                                      prompt_sha=r["prompt_sha"])
            if sk is None:
                probs.append(f"{r['id']}: {pr}")
            else:
                skins[r["id"]] = sk
    return skins, probs


def kit_ctx(pools: dict) -> KitCtx:
    skins, probs = build_skins(pools)
    if probs:
        raise ValueError(f"{len(probs)} pool row(s) fail their family checks: {probs[:2]}")
    return KitCtx(skins=skins, lexicon=pools["lexicon"])


# ================================================================================================ 9. CLI
def summary(res: dict) -> dict:
    if res["status"] == "BLOCKED":
        return {"status": "BLOCKED", "blocked": res["blocked"]}
    c = res["counts"]
    return {"status": res["status"], "shortfalls": res["shortfalls"],
            "minimums": {m["id"]: {"need": m["need"], "have": m["have"], "met": m["met"]} for m in res["checks"]},
            "requested_gaps": res["requested_gaps"], "mode_f": c["mode_f"],
            "lexicon": {k: c[k] for k in ("lexicon_forms_registry", "lexicon_forms_admitted",
                                          "lexicon_forms_rejected_by_gLEX", "lexicon_forms_pending")},
            "gates": {"G-LEX_used_forms": res["lex_gate_used"]["pass"],
                      "G-LEX_whole_registry": res["lex_gate_registry"]["pass"]},
            "validation": {n: {"tasks": r["tasks"], "rejected": r["rejected"], "missing": r["missing"],
                               "item_rejects": r["item_rejects"], "off_list_items": r["off_list_items"]}
                           for n, r in res["validation"]["rounds"].items()},
            "v1_identity": res["v1_identity"], "ignored": res["ignored"]}


def main(argv: list) -> int:
    ap = argparse.ArgumentParser(prog="freeze_v2")
    ap.add_argument("command", choices=("check", "freeze"))
    ap.add_argument("--ignore", nargs="*", default=[], help="task ids whose answer files are ruled out")
    a = ap.parse_args(argv)
    res = run(tuple(a.ignore))
    if a.command == "freeze" and res["status"] != "BLOCKED":
        man = write_pools(res)
        print(f"wrote {len(man['files']) + 1} files to {POOLS_V2} (status {man['status']})")
    print(json.dumps(summary(res), indent=1, ensure_ascii=False, default=str))
    return {"READY": 0, "SHORT": 1, "BLOCKED": 2}[res["status"]]


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

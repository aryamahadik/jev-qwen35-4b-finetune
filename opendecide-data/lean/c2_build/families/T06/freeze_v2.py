"""families/T06/freeze_v2.py: the T06 pool re-freeze, v2 (G0_SPEC.md section 4; C2_DATA_SPEC 3.0, 6.2, 6.3; PREREG A37 b, A38).

Why a new script. pool_freeze.py (freeze-v1) reads only haiku/author and haiku/extract, refuses a second freeze
("the T06 pools are frozen once") and has no step for the redo2 answers. haiku/redo2/build_redo2.py wrote the redo2 tasks
and has an `admit` stage, but that stage only writes a SUPPLEMENT (pools/redo2/), applies the 98% G3-H bar to the redo2
batch alone, validates no answer file against its contract and lists no gate table over the whole pool. This script is
the missing separately ruled re-freeze over ALL rounds. It edits no existing file: pools/ (freeze-v1) stays byte-identical
(checked against its manifest.json before and after), and everything new goes to pools_v2/.

Redo3 (added 14 Oct 2026). The first v2 freeze (v1 + redo2) was SHORT by 14 piece rows. haiku/redo3 holds the answers that
close them: five authoring files (haiku/redo3/answers: packs, skins, attack lines, question wordings) and two G-LEX reads of
the new wordings (haiku/redo3/reads/answers). This script folds both rounds in (section "redo3" below) on top of the v1 +
redo2 state it recomputes first. That earlier freeze is kept as pools_v2_prev/ (moved aside by hand before the re-write; this
script never moves or deletes anything): the recomputed v1 + redo2 state must equal it byte for byte (gate), the redo3 task
files must equal a rebuild from it, and its MANIFEST.json is hashed into the new one.

What it does, in order (everything is recomputed from the answer files and the code; no earlier record is trusted):
  1  Answer contracts. EVERY answer file of EVERY round (haiku/author, haiku/extract, haiku/redo2, haiku/redo2/extract,
     haiku/redo3, haiku/redo3/reads) is
     read against its task's contract: the chunk matches its manifest hash and its prompt hash, the task file names the
     answer path and every qid; the file is one UTF-8 JSON list of objects with exactly the keys the task asked for, the
     right types, exactly the chunk's qids once each; a G-LEX pick is a meaning of the closed list printed in the task
     file. An invalid file is REJECTED whole (never edited, never repaired), and so is a file whose file-access audit
     failed (--audit-failed; the orchestrator's list for this run is empty). A file in an answers/ folder that no task owns
     is flagged, an answers/ folder of an unlisted round too. The Haiku ambiguity record (52 points) is checked against
     its own contract. Item CONTENT rules (word lists, G-SL, negation counts, pack names) are not file contracts: they are
     the loaders' own checks and drop one item, not a file.
  2  Rebuilds. The author batches, the G-LEX / G3-H batches and the redo2 batches are rebuilt in memory and must equal the
     files on disk (so qid -> item is the one the agents saw). freeze-v1 is recomputed from the usable answers and must
     equal pools/ (every pool file, the lexicon and the quarantine).
  3  G-LEX (kit rules, c2_kit.lexicon): one registry form per kept notice and wording; every usable read records one
     extraction per form (extractor = the read label, as in v1 and redo2, so the extraction lists are the same records);
     admitted = unit test + LexForm.required distinct extractors (2 for deontic and question forms; 3 for window and
     precedence forms) that ALL picked the form's own meaning; any other pick rejects the form for good. Forms that are
     not admitted never reach a pool. The redo2 wordings are merged into the frozen registry exactly as build_redo2 does
     (a form that breaks a v1 form's unit test is dropped, v1 stays).
  4  G3-H (kit rules, c2_kit.g3h): one blind read per Mode F document (v1 g3h-r1 and redo2 g3h-r1); g3h.compare against
     the generator's three facts; the template is the REGISTER (as in v1), over every document of the register from both
     rounds; g3h.template_report: < 98% quarantines the register, every mismatch is dropped. A document with no usable
     read is UNREAD: it is not admitted and does not count as a mismatch (the gate fails and says so).
  5  Every gate and every G0 number (targets are never lowered): the v1 target table over the v2 pools, the 2% floors per
     wording form, the gate table, the verdict READY or SHORT with the exact shortfalls, and pools_v2/ with MANIFEST.json
     (file hashes, input hashes, counts, gates, verdict, sensitivity, loading instructions).

  6  Redo3. The redo3 authoring files are cut into pieces by their plan (role, held-out flag, register); each piece runs
     through its loader's own check (haiku_author.validate_pack / check_skin / check_attack / check_wording) with the dedup
     set the redo3 read builder used (the v1 + redo2 pool texts plus every earlier authoring answer, kept or dropped), and a
     dropped piece never enters. The kept wordings are merged into the v1 + redo2 registry (unit tested) and need 2 of 2
     G-LEX reads (extractors haiku-r3-glex-r1 / haiku-r3-glex-r2, from haiku/redo3/reads); packs, skins and attack lines
     have no read. The lint verdicts must equal the ones the read builder recorded (haiku/redo3/reads/LINT.json), the read
     tasks must equal a rebuild, and (when pools_v2_prev/ exists) the authoring tasks must equal a rebuild from it.
  The G0 numbers, the gate table and the verdict (step 5) are then taken over the pools after redo3.

Nothing here sets, edits or chooses a label or a read's answer; Haiku answers only flag, admit or quarantine. No target,
bar or check is loosened. Nothing is generated and no row is written.

  ../.venv/bin/python c2_build/families/T06/freeze_v2.py                  # dry run: validation, gates, verdict
  ../.venv/bin/python c2_build/families/T06/freeze_v2.py --write          # write pools_v2/ (never overwrites a different one:
                                                                          #  mv pools_v2 pools_v2_prev first, by hand)
  ../.venv/bin/python c2_build/families/T06/freeze_v2.py --check          # pools_v2/ on disk == a rebuild
  ../.venv/bin/python c2_build/families/T06/freeze_v2.py --audit-failed ID,ID   # ignore those tasks' answer files
  ../.venv/bin/python -m pytest -q -p no:cacheprovider c2_build/families/T06/test_freeze_v2.py   (from lean/)

How the generator loads pools_v2. plugin.py has no pool path: STORES, CUSTOMERS, ITEMS, JURIS and JURIS_HELD are in-code
stand-ins read as module constants at call time, and the skins, wordings and lexicon of a ctx are supplied by the caller.
plugin.py is an existing file and is not edited; the pilot generator does this instead:

    from families.T06 import freeze_v2, plugin as P
    from c2_kit import pipeline
    pools = freeze_v2.load_pools_v2()          # verifies MANIFEST.json (every file's sha256 and size); refuses a SHORT
                                               # freeze unless require_ready=False is passed deliberately
    ctx = freeze_v2.kit_ctx(pools)             # KitCtx: Mode T skins, admitted Mode F documents (thinned to <= 25% of each
                                               # register's narrative pool), attack lines, one wording skin per admitted
                                               # form, and the G-LEX registry rebuilt from lexicon.json
    with freeze_v2.wired_plugin(pools):        # temporarily swaps the stand-in constants for the pack data
        plugin = P.T06Plugin(lexicon=ctx.lexicon)
        res = pipeline.build_unit(plugin, plugin.sample(seed, sampler), ctx)

wired_plugin restores every constant on exit. Held-out packs contribute their jurisdictions to JURIS_HELD only: plugin.py
draws a store, customer and item for S5 from the same constants as for training rows, so held-out stores / customers /
items are never wired in (no held-out text can reach a training row).
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.util
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, g3h, lexicon, paths  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit.distractors import uhash  # noqa: E402
from c2_kit.lexicon import LexiconRegistry  # noqa: E402
from c2_kit.plugin import KitCtx  # noqa: E402
from families.T06 import extract_build as E  # noqa: E402
from families.T06 import haiku_author as H  # noqa: E402
from families.T06 import plugin as P  # noqa: E402
from families.T06 import pool_freeze as PF  # noqa: E402

FAMILY = "T06"
VERSION = "t06-freeze-v2"
STAGE = "pool re-freeze v2 (v1 + redo2 + redo3, every answer file validated)"
POOLS_V1 = HERE / "pools"
POOLS_V2 = HERE / "pools_v2"
POOLS_V2_PREV = HERE / "pools_v2_prev"                        # the v1 + redo2 freeze, moved aside by hand before the re-write
HAIKU = HERE / "haiku"
REDO3 = HAIKU / "redo3"                                       # redo3 authoring round (packs, skins, attack lines, wordings)
REDO3_READS = REDO3 / "reads"                                 # redo3 G-LEX reads of the new wordings
G0 = HERE / "G0_SPEC.md"
G0_PIN = P.T06Plugin.G0_SHA256_AUTHORED


@contextlib.contextmanager
def authored_g0():
    """The pool-era builders (redo2, redo3, reads) write P.T06Plugin.G0_SHA256 into their manifests, and their own sha256
    is recorded in TASKS.json, so they stay byte for byte as they are. They ran against G0 v2; G0_SHA256 itself moved to
    v3 (pilot fix iteration 1), so a rebuild reproduces them under the sha they were authored against."""
    keep = P.T06Plugin.G0_SHA256, P.T06Plugin.ITEM_DESCRIBE
    P.T06Plugin.G0_SHA256 = P.T06Plugin.G0_SHA256_AUTHORED
    P.T06Plugin.ITEM_DESCRIBE = P.T06Plugin.ITEM_DESCRIBE_AUTHORED       # the pool-era G3-H task files carry this text
    try:
        yield
    finally:
        P.T06Plugin.G0_SHA256, P.T06Plugin.ITEM_DESCRIBE = keep   # (restored)


def under_authored_g0(fn):
    import functools

    @functools.wraps(fn)
    def wrapped(*a, **k):
        with authored_g0():
            return fn(*a, **k)
    return wrapped
ROUNDS = ("author", "extract", "redo2", "redo2/extract", "redo3", "redo3/reads")   # answer-file rounds, in run order
AUTHOR_ROUNDS = ("author", "redo2")                           # their answers define the items of the extraction rounds
R3_ROUND, R3_READS_ROUND = "redo3", "redo3/reads"
R3_BLOCKING = ("author_wording",)                             # redo3 author kinds the read tasks were built from
LATEST_ROUND = R3_READS_ROUND                                 # the round whose tasks were answered last
PENDING_NOTE = ("the orchestrator's file-access-audit failure list for this run is []: no answer file is ignored; the "
                "transcripts are never-open paths here, so this script cannot audit them itself")
V1_EXTRACTORS = "haiku-"                                      # v1 extractor ids: haiku-<read label> (as pool_freeze)
R2_EXTRACTORS = "haiku-r2-"                                   # redo2 extractor ids: haiku-r2-<read label> (as build_redo2)
R3_EXTRACTORS = "haiku-r3-"                                   # redo3 extractor ids: haiku-r3-<read label> (build_reads.py notes)
R3_READ_LABELS = ("glex-r1", "glex-r2")                       # 2 of 2 for question forms (lexicon.LexForm.required)
DATA_FILES = ("packs.jsonl", "skins.jsonl", "attacks.jsonl", "documents.jsonl", "notices.jsonl", "wordings.jsonl",
              "lexicon.json", "quarantine.jsonl", "extraction_log.jsonl", "g3h_log.jsonl")   # the pool files a freeze writes
LEXICON_NOTE = ("T06 lexicon after the v2 freeze: the admitted v1 forms, the admitted redo2 wordings and the admitted redo3 "
                "wordings (G-LEX). Every sem is kept: the closed meaning lists and the never-generated decoys.")
LEXICON_NOTE_PREV = ("T06 lexicon after the v2 freeze: the admitted v1 forms plus the admitted redo2 wordings (G-LEX). "
                     "Every sem is kept: the closed meaning lists and the never-generated decoys.")
MODE_F_CAP = 0.25                                             # spec 3.0 / 6.3 / G0 4.2: free-form rows <= 25% per family
README = "README.txt"

# G0_SPEC.md section 4 and the v1 target table (pool_freeze.targets). Never lowered (test_targets_not_lowered pins them).
FLOOR_2PCT = {"ch_rule": 18, "ch_end_reject": 4, "ch_end_withdraw": 4, "yn_refund": 6, "yn_owed": 6, "yn_double": 6,
              "yn_not_refund": 6, "yn_may_refuse": 6, "yn_no_right": 6}   # G0 4.5: each wording <= 2% of the family's rows
FLOOR_ROWS = ("skins, all (floor)", "ch_rule wordings (G0 floor 30)", "ch_end_withdraw wordings (2% floor 4)",
              "lexicon forms used (must all be admitted)")        # v1 target rows that are G0 minimums, not asks
TARGET = {"packs": PF.PACKS_TOTAL, "packs_held": PF.PACKS_HELD, "skins_floor": PF.SKIN_FLOOR,
          "attacks": PF.ATTACKS_TOTAL, "attacks_held": PF.ATTACKS_HELD, "documents": PF.DOCS_ASKED,
          "documents_held": PF.DOCS_HELD, "notice_per_sem": PF.NOTICE_FLOOR, "g3h_rate": g3h.PASS_RATE,
          "wordings_training": sum(t for t, _h in H.WORDING_PLAN.values()),
          "wordings_held": sum(h for _t, h in H.WORDING_PLAN.values()), "glex_deontic": 2, "glex_question": 2,
          "glex_window": 3, "glex_precedence": 3, "mode_f_cap": MODE_F_CAP}


# ------------------------------------------------------------------------------------------------ helpers
def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p: Path) -> str:
    return sha_bytes(Path(p).read_bytes())


def sha_text(t: str) -> str:
    return sha_bytes(t.encode("utf-8"))


def jtext(obj) -> str:
    """paths.write_json's exact text for an object."""
    return json.dumps(obj, ensure_ascii=False, indent=1) + "\n"


def jltext(rows) -> str:
    """paths.write_jsonl's exact text for rows."""
    return "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)


def rel(p: Path) -> str:
    return Path(p).resolve().relative_to(HERE).as_posix()


def read_jsonl(path: Path) -> list:
    return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]


_BR = None


def build_redo2():
    """haiku/redo2/build_redo2.py loaded read-only as a module (it is a script folder, not a package)."""
    global _BR
    if _BR is None:
        spec = importlib.util.spec_from_file_location("t06_build_redo2", HAIKU / "redo2" / "build_redo2.py")
        mod = importlib.util.module_from_spec(spec)
        sys.modules["t06_build_redo2"] = mod
        spec.loader.exec_module(mod)
        _BR = mod
    return _BR


# ------------------------------------------------------------------------------------------------ 1  answer contracts
QID = re.compile(r"^q[0-9a-f]{10}$")


def _nonempty(x) -> bool:
    return isinstance(x, str) and bool(x.strip())


def _keys(a: dict, keys) -> list:
    return [] if set(a) == set(keys) else [f"keys {sorted(a)} != {sorted(keys)}"]


def _item_text(a: dict) -> list:
    probs = _keys(a, ("qid", "text"))
    if not _nonempty(a.get("text")):
        probs.append("text is not a non-empty string")
    return probs


def _item_lex(a: dict) -> list:
    probs = _keys(a, ("qid", "meaning"))
    if not isinstance(a.get("meaning"), str):
        probs.append("meaning is not a string")
    return probs


def _item_g3h(a: dict) -> list:
    probs = _keys(a, ("qid", "customer", "item", "store"))
    for k in ("customer", "item", "store"):
        if not _nonempty(a.get(k)):
            probs.append(f"{k} is not a non-empty string")
    return probs


def _item_pack(a: dict) -> list:
    """The pack's JSON shape (the keys and types the task asked for). Counts, name shapes and word rules are
    haiku_author.validate_pack's item-level checks: they drop one pack, never the file."""
    probs = _keys(a, ("qid", "pack"))
    p = a.get("pack")
    if not isinstance(p, dict):
        return probs + ["pack is not an object"]
    if set(p) != {"store", "goods", "customers", "jurisdiction"}:
        probs.append(f"pack keys {sorted(p)}")
        return probs
    if not _nonempty(p["store"]):
        probs.append("store is not a non-empty string")
    if not _nonempty(p["jurisdiction"]):
        probs.append("jurisdiction is not a non-empty string")
    g = p["goods"]
    if not (isinstance(g, dict) and set(g) == set(H.GOODS_N)
            and all(isinstance(g[k], list) and all(_nonempty(x) for x in g[k]) for k in g)):
        probs.append("goods is not {standard, custom, perishable, hygiene} lists of strings")
    if not (isinstance(p["customers"], list) and all(_nonempty(x) for x in p["customers"])):
        probs.append("customers is not a list of strings")
    return probs


ITEM_CHECK = {"author_pack": _item_pack, "author_skin": _item_text, "author_wording": _item_text,
              "author_freeform": _item_text, "author_lexicon": _item_text, "extract_lex": _item_lex,
              "extract_g3h": _item_g3h}


def answer_problems(kind: str, raw, qids: list, closed=None) -> list:
    """Contract problems of one parsed answer file (empty list = valid). kind: the chunker task kind; qids: the chunk's
    qids in order; closed: the meanings printed in an extract_lex task file."""
    check = ITEM_CHECK.get(kind)
    if check is None:
        return [f"no answer contract for kind {kind!r}"]
    if not isinstance(raw, list):
        return ["answer is not one JSON list"]
    probs, seen = [], Counter()
    for i, a in enumerate(raw):
        if not isinstance(a, dict):
            probs.append(f"item {i}: not an object")
            continue
        q = a.get("qid")
        if not (isinstance(q, str) and QID.fullmatch(q)):
            probs.append(f"item {i}: no qid of the form q + 10 hex digits")
            continue
        seen[q] += 1
        probs += [f"{q}: {x}" for x in check(a)]
        if kind == "extract_lex" and closed is not None and isinstance(a.get("meaning"), str) \
                and a["meaning"] not in closed:
            probs.append(f"{q}: not a meaning of the closed list printed in the task file")
    want = set(qids)
    if want - set(seen):
        probs.append(f"{len(want - set(seen))} qid(s) unanswered")
    if set(seen) - want:
        probs.append(f"{len(set(seen) - want)} qid(s) outside the chunk")
    if any(n > 1 for n in seen.values()):
        probs.append(f"{sum(1 for n in seen.values() if n > 1)} qid(s) answered twice")
    return probs


def closed_list(task_md: str) -> list:
    """The meanings printed in an extract_lex task file (the lines '- ...' under the line 'CLOSED LIST (...)' up to the next
    blank line)."""
    m = re.search(r"^CLOSED LIST \([^\n]*\n(.*?)(?:\n\s*\n|\Z)", task_md, re.S | re.M)
    if not m:
        raise ValueError("no CLOSED LIST in the task file")
    return [ln[2:] for ln in m.group(1).splitlines() if ln.startswith("- ")]


def ambiguity_problems(path: Path) -> list:
    """The Haiku ambiguity pass (haiku/ambiguity/amb_T06_points.json) against its own contract: 52 points (H1-H52, G0
    section 7) of exactly where / issue / readings (a list of strings), and points_sha256 by the record's own rule."""
    try:
        o = json.loads(Path(path).read_bytes().decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as e:
        return [f"not valid UTF-8 JSON ({str(e)[:60]})"]
    pts = o.get("points") if isinstance(o, dict) else None
    if not isinstance(pts, list):
        return ["no points list"]
    probs = []
    if o.get("n_points") != len(pts) or len(pts) != 52:
        probs.append(f"{len(pts)} points, n_points {o.get('n_points')} (G0 section 7 maps H1-H52)")
    for i, q in enumerate(pts):
        if not (isinstance(q, dict) and set(q) == {"where", "issue", "readings"} and isinstance(q["where"], str)
                and isinstance(q["issue"], str) and isinstance(q["readings"], list)
                and all(isinstance(x, str) for x in q["readings"])):
            probs.append(f"point {i + 1}: not where / issue / readings")
    if hashlib.sha256(json.dumps(pts, sort_keys=True, ensure_ascii=False,
                                 separators=(",", ":")).encode()).hexdigest() != o.get("points_sha256"):
        probs.append("points_sha256 does not match the points")
    if o.get("family") != FAMILY:
        probs.append(f"family {o.get('family')!r}")
    return probs


def _round_dir(haiku_root: Path, rnd: str) -> Path:
    return Path(haiku_root) / rnd


def validate_answers(ignore=frozenset(), haiku_root: Path = HAIKU) -> dict:
    """Every answer file of every round against its contract. Never edits.
    -> {"files": [...], "stray": [...], "unlisted_rounds": [...], "usable": {task ids}, "invalid": [...],
        "ignored": [...], "by_round": {...}, "ambiguity": {...}}."""
    haiku_root = Path(haiku_root)
    files, stray = [], []
    for rnd in ROUNDS:
        rdir = _round_dir(haiku_root, rnd)
        index = json.loads((rdir / "TASKS.json").read_text(encoding="utf-8"))
        tasks = index["tasks"]
        manifests = {}
        for mf in sorted((rdir / "manifest").glob("*.json")):
            m = json.loads(mf.read_text(encoding="utf-8"))
            manifests[m["batch_id"]] = m
        for t in tasks:
            tid = t["task_id"]
            m = manifests.get(t["batch_id"])
            kind = (m or {}).get("kind", t["kind"])       # the chunker task kind; TASKS.json names the lexicon kind of an
            ent = {"round": rnd, "task_id": tid, "kind": kind, "batch_id": t["batch_id"],   # extract_lex task instead
                   "answer_file": f"{rnd}/answers/{tid}.json", "ignored": tid in ignore}
            if kind == "extract_lex":
                ent["lexicon_kind"] = t["kind"]
            probs = []
            qids, closed = [], None
            mt = next((x for x in (m or {}).get("tasks", []) if x["task_id"] == tid), None)
            cf = rdir / "chunks" / f"{tid}.json"
            if m is None or mt is None:
                probs.append("no batch manifest for the task")
            elif not cf.is_file():
                probs.append("no chunk file")
            else:
                chunk = json.loads(cf.read_text(encoding="utf-8"))
                qids = [it["qid"] for it in chunk["items"]]
                if chunker.sha(json.dumps(chunk, sort_keys=True, ensure_ascii=False)) != mt["sha256"]:
                    probs.append("chunk differs from its manifest hash")
                pf = rdir / "prompts" / f"{m['prompt_sha'][:16]}.txt"
                if chunk.get("prompt_sha") != m["prompt_sha"] or t.get("prompt_sha") != m["prompt_sha"] \
                        or not pf.is_file() or chunker.sha(pf.read_text(encoding="utf-8")) != m["prompt_sha"]:
                    probs.append("prompt differs from its manifest hash")
                if len(qids) != mt["n"] or len(set(qids)) != len(qids) or t.get("n_items") != mt["n"]:
                    probs.append("chunk item count differs from the manifest")
                if chunk.get("kind") != kind or (t["kind"] != kind and not (
                        kind == "extract_lex" and t["kind"] in lexicon.KINDS)):
                    probs.append("task kind differs between the chunk, the manifest and TASKS.json")
                tf = rdir / "tasks" / f"{tid}.md"
                if not tf.is_file():
                    probs.append("no task file")
                else:
                    md = tf.read_text(encoding="utf-8")
                    if f"/answers/{tid}.json" not in md:
                        probs.append("task file does not name its answer path")
                    if any(q not in md for q in qids):
                        probs.append("task file lacks a qid of its chunk")
                    if kind == "extract_lex":
                        try:
                            closed = set(closed_list(md))
                            if not closed or any(c not in pf.read_text(encoding="utf-8") for c in closed):
                                probs.append("closed list differs from the prompt file")
                        except ValueError as e:
                            probs.append(f"task file: {e}")
            af = rdir / "answers" / f"{tid}.json"
            if not af.is_file():
                probs.append("no answer file")
            else:
                ent["sha256"] = sha_file(af)
                try:
                    raw = json.loads(af.read_bytes().decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError) as e:
                    probs.append(f"answer is not valid UTF-8 JSON ({str(e)[:60]})")
                else:
                    ent["n_items"] = len(raw) if isinstance(raw, list) else None
                    if qids:
                        probs += answer_problems(kind, raw, qids, closed)
            ent["n_problems"] = len(probs)
            ent["problems"] = probs[:8]
            ent["valid"] = not probs
            ent["usable"] = ent["valid"] and not ent["ignored"]
            files.append(ent)
        known = {f"{x['task_id']}.json" for x in tasks} | {README}
        adir = rdir / "answers"
        for p in sorted(adir.iterdir()) if adir.is_dir() else []:
            if p.name not in known:
                stray.append({"round": rnd, "answer_file": f"{rnd}/answers/{p.name}",
                              "problem": "not an answer file of any task in the round's TASKS.json"})
    listed = {(haiku_root / r / "answers").resolve() for r in ROUNDS}
    unlisted = sorted(rel_str(p, haiku_root) for p in haiku_root.rglob("answers")
                      if p.is_dir() and p.resolve() not in listed)
    amb = haiku_root / "ambiguity" / "amb_T06_points.json"
    amb_ent = None
    if amb.is_file():
        ap = ambiguity_problems(amb)
        amb_ent = {"file": "ambiguity/amb_T06_points.json", "sha256": sha_file(amb), "valid": not ap, "problems": ap[:8]}
    by_round = defaultdict(Counter)
    for f in files:
        by_round[f["round"]]["files"] += 1
        by_round[f["round"]]["valid"] += f["valid"]
        by_round[f["round"]]["usable"] += f["usable"]
    return {"files": files, "stray": stray, "unlisted_rounds": unlisted, "ambiguity": amb_ent,
            "usable": {f["task_id"] for f in files if f["usable"]},
            "invalid": sorted(f["task_id"] for f in files if not f["valid"]),
            "ignored": sorted(f["task_id"] for f in files if f["ignored"]),
            "by_round": {k: dict(v) for k, v in sorted(by_round.items())}}


def rel_str(p: Path, root: Path) -> str:
    return Path(p).resolve().relative_to(Path(root).resolve()).as_posix()


# ------------------------------------------------------------------------------------------------ 2  freeze-v1 and rebuilds
def v1_state() -> dict:
    """freeze-v1 against its own manifest.json: every pool file, the extraction answers and TASKS.json it recorded."""
    mf = POOLS_V1 / "manifest.json"
    man = json.loads(mf.read_text(encoding="utf-8"))
    bad, inputs_bad = [], []
    for name, meta in man["pool_files"].items():
        p = POOLS_V1 / name
        if not p.is_file() or sha_file(p) != meta["sha256"]:
            bad.append(name)
    ex = man["extraction"]
    for tid, sha in ex["answers"].items():
        p = HAIKU / "extract" / "answers" / f"{tid}.json"
        if not p.is_file() or sha_file(p) != sha:
            inputs_bad.append(f"haiku/extract/answers/{tid}.json")
    if sha_file(HAIKU / "extract" / "TASKS.json") != ex["TASKS.json_sha256"]:
        inputs_bad.append("haiku/extract/TASKS.json")
    extra = sorted(p.name for p in POOLS_V1.iterdir() if p.name not in man["pool_files"] and p.name != "manifest.json")
    g0_now = sha_file(G0)
    return {"manifest_sha256": sha_file(mf), "files": len(man["pool_files"]), "files_changed": bad,
            "inputs": len(ex["answers"]) + 1, "inputs_changed": inputs_bad, "extra_files": extra,
            "g0_v1_sha256": man["g0_lite"]["sha256"], "g0_now_sha256": g0_now,
            "g0_unchanged": man["g0_lite"]["sha256"] == g0_now,
            "unchanged": not (bad or inputs_bad or extra) and man["g0_lite"]["sha256"] == g0_now, "manifest": man}


def files_differ(root: Path, files: dict) -> list:
    return sorted(r for r, t in files.items()
                  if not (Path(root) / r).is_file() or (Path(root) / r).read_text(encoding="utf-8") != t)


def v1_rebuild_differs(p: dict) -> dict:
    """The files on disk of the v1 author and extract rounds against an in-memory rebuild (qid -> item must be the one the
    agents saw)."""
    _tasks, a_files = H.task_list(H.ROOT)
    batches = p["glex"] + [("g3h-r1", "extract_g3h", 0, p["g3"])]
    e_files, _rows = E._task_rows(E.EXTRACT, batches)
    return {"author": files_differ(H.ROOT, a_files), "extract": files_differ(E.EXTRACT, e_files)}


def read_answers(b, root: Path, usable: set) -> tuple:
    """({internal id: answer object}, problems) for one batch. An answer file that is not usable (invalid, ignored or
    missing) leaves its items unanswered; chunker.load_answers checks qid ownership and duplicates."""
    raw, probs = {}, []
    for c in b.chunks:
        tid = c["task_id"]
        if tid not in usable:
            probs.append(f"{tid}: answer file not usable (missing, invalid or audit-failed)")
            continue
        raw[tid] = json.loads((Path(root) / b.answer_path(tid)).read_text(encoding="utf-8"))
    ans, p2 = chunker.load_answers(b, raw)
    return ans, probs + p2


# ------------------------------------------------------------------------------------------------ 3  G-LEX
def record_glex(batches: list, reg, root: Path, usable: set, prefix: str, rnd: str) -> tuple:
    """Kit rule: one record_extraction per (form, read), extractor id = prefix + read label; the pick is a sem id (None
    when the text is no meaning of the closed list). -> (read log, problems). record_extraction raises when the same
    extractor reads a form twice."""
    log, probs = [], []
    for label, _kind, _gi, b in batches:
        ans, pr = read_answers(b, root, usable)
        probs += [f"{label} {b.batch_id}: {x}" for x in pr]
        qid_of = {internal: qid for qid, internal in b.key.items()}
        for fid, a in sorted(ans.items()):
            f = reg.forms[fid]
            meaning = a.get("meaning") if isinstance(a, dict) else None
            sem = reg.meaning_to_sem(f.kind, meaning) if isinstance(meaning, str) else None
            reg.record_extraction(fid, f"{prefix}{label}", sem)
            log.append({"round": rnd, "form_id": fid, "kind": f.kind, "read": label, "extractor": f"{prefix}{label}",
                        "task_id": b.task_of[qid_of[fid]], "meaning": meaning, "sem_id": sem,
                        "agrees": sem == f.sem_id})
    return log, probs


def glex_audit(reg) -> dict:
    """The kit's G-LEX rule re-checked form by form: unit test, >= LexForm.required DISTINCT extractors, every pick the
    form's own sem. -> {"gate": reg.gate(), "required_by_kind": {...}, "reads_per_form": {...}, "violations": [...]}"""
    viol, per = [], Counter()
    req = {}
    for fid, f in sorted(reg.forms.items()):
        n = len({e for e, _ in f.extractions})
        per[(f.kind, n)] += 1
        req[f.kind] = f.required
        if f.required != (3 if f.kind in lexicon.STRICT_KINDS else 2):
            viol.append(f"{fid}: LexForm.required {f.required} for kind {f.kind}")
        if not f.unit_ok:
            viol.append(f"{fid}: unit test")
        if n < f.required:
            viol.append(f"{fid}: {n} of {f.required} reads")
        if any(s != f.sem_id for _, s in f.extractions):
            viol.append(f"{fid}: a read picked another meaning")
        if reg.status(fid) != "admitted":
            viol.append(f"{fid}: status {reg.status(fid)}")
    return {"gate": reg.gate(), "required_by_kind": dict(sorted(req.items())),
            "reads_per_form": {f"{k}/{n}": v for (k, n), v in sorted(per.items())}, "violations": viol}


# ------------------------------------------------------------------------------------------------ 4  G3-H
def g3h_votes(batch, expected: dict, reg_of: dict, root: Path, usable: set, extractor: str, rnd: str) -> tuple:
    """(votes, problems). One vote per document: g3h.compare of the extractor's raw answer against the generator's facts.
    A document whose read is not usable is UNREAD (answered False): it is not admitted and not counted as a mismatch."""
    fields = list(E.G3H_FIELDS)
    ans, probs = read_answers(batch, root, usable)
    task_of = {iid: batch.task_of[q] for q, iid in batch.key.items()}
    votes = []
    for iid in sorted(expected):
        if iid in ans:
            ok, diffs = g3h.compare(expected[iid], ans[iid], fields)
            votes.append({"round": rnd, "item": iid, "register": reg_of[iid], "extractor": extractor,
                          "task_id": task_of[iid], "answered": True, "ok": ok, "diffs": diffs})
        else:
            votes.append({"round": rnd, "item": iid, "register": reg_of[iid], "extractor": extractor,
                          "task_id": task_of[iid], "answered": False, "ok": False, "diffs": ["unread"]})
    return votes, probs


def g3h_pooled(votes: list) -> dict:
    """g3h.template_report over every ANSWERED document of both rounds; the template is the register (as in v1)."""
    return g3h.template_report([(v["register"], v["item"], v["ok"]) for v in votes if v["answered"]])


# ------------------------------------------------------------------------------------------------ the pool rows
def _pool_pack(row: dict) -> dict:
    return {k: v for k, v in row.items() if k not in ("pid", "held_out")}


def relint(pools: dict) -> dict:
    """Every admitted piece through its loader's own check once more (G-SL, G0 fact words, shape rules), with a fresh
    duplicate set per pool. -> {pool: [problems]}; every list must be empty."""
    out = {k: [] for k in ("packs", "skins", "attacks", "documents", "notices", "wordings")}
    for r in pools["packs"]:
        v = H.validate_pack(_pool_pack(r))
        if v:
            out["packs"].append(f"{r['pid']}: {v[:2]}")
    seen = set()
    for r in pools["skins"]:
        _o, v = H.check_skin(r["pid"], r["text"], {"register": r["register"], "escape": r["escape"],
                                                   "held_out": r["held_out"]}, r["haiku_task_id"],
                             r["haiku_prompt_sha"], seen)
        if v:
            out["skins"].append(f"{r['pid']}: {v[:2]}")
    seen = set()
    for r in pools["attacks"]:
        decl = {p.name: "name" for p in K.placeholders(r["text"])}
        _o, v = H.check_attack(r["pid"], r["text"], {"decl": decl, "held_out": r["held_out"]}, r["haiku_task_id"],
                               r["haiku_prompt_sha"], seen)
        if v:
            out["attacks"].append(f"{r['pid']}: {v[:2]}")
    seen = set()
    for r in pools["documents"]:
        _o, v = H.check_freeform(r["pid"], r["text"], {"facts": r["facts"], "register": r["register"],
                                                       "held_out": r["held_out"]}, r["haiku_task_id"],
                                 r["haiku_prompt_sha"], seen)
        if v:
            out["documents"].append(f"{r['pid']}: {v[:2]}")
    seen = set()
    for r in pools["notices"]:
        _o, v = H.check_notice(r["form_id"], r["text"], {"sem": r["sem_id"], "kind": r["kind"], "slots": r["slots"]},
                               r["haiku_task_id"], r["haiku_prompt_sha"], seen)
        v += E._notice_gsl(r["sem_id"], r["text"], r["slots"])
        if v:
            out["notices"].append(f"{r['form_id']}: {v[:2]}")
    seen = set()
    for r in pools["wordings"]:
        _o, v = H.check_wording(r["form_id"], r["text"], {"qform": r["qform"], "held_out": r["held_out"]},
                                r["haiku_task_id"], r["haiku_prompt_sha"], seen)
        if v:
            out["wordings"].append(f"{r['form_id']}: {v[:2]}")
    return out


def duplicates(pools: dict) -> dict:
    """Normalised texts that occur twice inside one pool (the loaders dedup against a growing set per batch; this checks
    the union of the rounds)."""
    out = {}
    for name in ("skins", "attacks", "documents", "notices", "wordings"):
        c = Counter(H._norm(r["text"].strip()) for r in pools[name])
        out[name] = sorted(t for t, n in c.items() if n > 1)
    return out


def target_rows(p: dict, pools: dict, reg) -> list:
    """The v1 target table (pool_freeze.targets, every row kept) over the v2 pools, the 2% floors per wording form
    (training wordings only), each row tagged G0 floor or G0 ask."""
    rows = []
    for t in PF.targets(p, pools, reg):
        floor = t["item"] in FLOOR_ROWS or t["item"].startswith("notice ")
        rows.append({"kind": "G0 floor" if floor else "G0 ask", "item": t["item"], "target": t["target"],
                     "got": t["admitted"], "shortfall": t["shortfall"], "met": t["shortfall"] == 0,
                     "note": t["source"]})
    for q, n in FLOOR_2PCT.items():
        got = sum(1 for w in pools["wordings"] if w["qform"] == q and not w["held_out"])
        rows.append({"kind": "G0 floor", "item": f"wording floor {q}, training (2% cap per wording)", "target": n,
                     "got": got, "shortfall": max(0, n - got), "met": got >= n,
                     "note": "G0 4.5: each admitted wording <= 2% of the family's rows (training wordings only)"})
    return rows


# ------------------------------------------------------------------------------------------------ pool files
def lexicon_json(reg, note: str) -> dict:
    """The registry as lexicon.json: admitted forms only, every sem kept (closed meaning lists and decoys included)."""
    merged = reg.to_json()
    merged["forms"] = [f for f in merged["forms"] if f["status"] == "admitted"]
    merged["note"] = note
    return merged


def pool_files(pools: dict, lex: dict, quarantine: list, glex_log: list, votes_log: list) -> dict:
    """{file name: text} of the ten data files of a freeze (the files of both the v1 + redo2 state and the final one)."""
    files = {f"{name}.jsonl": jltext(pools[name]) for name in ("packs", "skins", "attacks", "documents", "notices",
                                                                "wordings")}
    files["lexicon.json"] = jtext(lex)
    files["quarantine.jsonl"] = jltext(quarantine)
    files["extraction_log.jsonl"] = jltext(glex_log)
    files["g3h_log.jsonl"] = jltext(votes_log)
    return files


def id_collisions(pools: dict) -> dict:
    """Ids that occur twice: the pool ids inside each pool, the form ids, and the skin ids across skins, attack lines and
    documents (one namespace in kit_ctx). Every list must be empty."""
    out = {}
    for name, key in (("packs", "pid"), ("skins", "pid"), ("attacks", "pid"), ("documents", "pid"),
                      ("notices", "form_id"), ("wordings", "form_id")):
        c = Counter(r[key] for r in pools[name])
        out[f"{name}.{key}"] = sorted(k for k, n in c.items() if n > 1)
    c = Counter(r["skin_id"] for name in ("skins", "attacks", "documents") for r in pools[name])
    out["skin_id (skins, attacks, documents)"] = sorted(k for k, n in c.items() if n > 1)
    return out


# ------------------------------------------------------------------------------------------------ redo3
_MODULES = {}


def _module(key: str, path: Path):
    """A script of the family's haiku/ folder loaded read-only as a module (they are script folders, not packages)."""
    if key not in _MODULES:
        spec = importlib.util.spec_from_file_location(key, path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[key] = mod
        spec.loader.exec_module(mod)
        _MODULES[key] = mod
    return _MODULES[key]


def build_redo3_mod():
    """haiku/redo3/build_redo3.py (the authoring tasks of the redo3 round)."""
    return _module("t06_build_redo3", REDO3 / "build_redo3.py")


def build_reads_mod():
    """haiku/redo3/reads/build_reads.py (the G-LEX read tasks of the new wordings, and their lint record LINT.json)."""
    return _module("t06_build_reads", REDO3_READS / "build_reads.py")


def base_pools_dir():
    """The v1 + redo2 freeze on disk: pools_v2_prev/ when it holds a MANIFEST, else pools_v2/ while that is still the
    freeze made before redo3 (its MANIFEST lists no redo3 round). None when neither exists."""
    for d in (POOLS_V2_PREV, POOLS_V2):
        mf = d / "MANIFEST.json"
        if not mf.is_file():
            continue
        try:
            man = json.loads(mf.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            continue
        if man.get("family") == FAMILY and man.get("version") == VERSION and R3_ROUND not in man.get("rounds", ()):
            return d
    return None


def disk_batch(rdir: Path, batch_id: str) -> chunker.TaskBatch:
    """A TaskBatch rebuilt from the files the orchestrator wrote (manifest, prompt, chunks, key). The chunks are the ones
    the agents were given: validate_answers checks their hashes against the manifest, and the rebuild check compares the
    whole folder with a rebuild from the previous freeze."""
    rdir = Path(rdir)
    man = json.loads((rdir / "manifest" / f"{batch_id}.json").read_text(encoding="utf-8"))
    key = json.loads((rdir / "key" / f"{batch_id}.json").read_text(encoding="utf-8"))["key"]
    prompt = (rdir / "prompts" / f"{man['prompt_sha'][:16]}.txt").read_text(encoding="utf-8")
    chunks = [json.loads((rdir / "chunks" / f"{t['task_id']}.json").read_text(encoding="utf-8")) for t in man["tasks"]]
    task_of = {it["qid"]: c["task_id"] for c in chunks for it in c["items"]}
    return chunker.TaskBatch(kind=man["kind"], family=man["family"], batch_id=batch_id, prompt=prompt,
                             prompt_sha=man["prompt_sha"], seed=man["seed"], chunks=chunks, key=key, task_of=task_of)


def redo3_authoring(usable: set) -> dict:
    """The redo3 authoring answers, cut into pieces. -> {"batches": {batch id: TaskBatch}, "answers": {internal id: answer
    object}, "plan": {internal id: plan}, "task_of": {internal id: task id}, "prompt_sha": {internal id: sha}, "problems":
    [...]}. A file that is not usable (invalid, ignored or missing) leaves its items out and is listed in problems."""
    idx = json.loads((REDO3 / "TASKS.json").read_text(encoding="utf-8"))
    out = {"batches": {}, "answers": {}, "plan": {}, "task_of": {}, "prompt_sha": {}, "problems": []}
    for bid in sorted({t["batch_id"] for t in idx["tasks"]}):
        b = disk_batch(REDO3, bid)
        out["batches"][bid] = b
        out["plan"].update(json.loads((REDO3 / "plan" / f"{bid}.json").read_text(encoding="utf-8"))["plan"])
        ans, probs = read_answers(b, REDO3, usable)
        out["problems"] += [f"{bid}: {x}" for x in probs]
        inv = {iid: q for q, iid in b.key.items()}
        for iid, a in ans.items():
            out["answers"][iid] = a
            out["task_of"][iid] = b.task_of[inv[iid]]
            out["prompt_sha"][iid] = b.prompt_sha
    return out


def prior_author_texts(haiku_root: Path = HAIKU) -> set:
    """Normalised text of every earlier authoring answer (the v1 author round and redo2), kept or dropped: the dedup set the
    redo3 read builder (build_reads._prior_texts) used. An unreadable file adds nothing (author files that cannot be read
    block the freeze before this point)."""
    seen = set()
    for rnd in ("author", "redo2"):
        for f in sorted((Path(haiku_root) / rnd / "answers").glob("*.json")):
            try:
                items = json.loads(f.read_bytes().decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                continue
            for a in items if isinstance(items, list) else []:
                if isinstance(a, dict) and isinstance(a.get("text"), str):
                    seen.add(H._norm(a["text"]))
    return seen


def redo3_lint(pools: dict, r3: dict, prior: set) -> dict:
    """The family's lint and dedup over every redo3 piece, against the v1 + redo2 pools (the loaders' own checks, as
    build_reads.lint runs them on pools_v2_prev). -> {"packs"|"skins"|"attacks"|"wordings": {"kept": [...], "drops":
    [...]}}; a kept skin / attack / wording carries its checked object under "obj". Nothing is edited."""
    ans, plan, tof, psha = r3["answers"], r3["plan"], r3["task_of"], r3["prompt_sha"]
    out = {k: {"kept": [], "drops": []} for k in ("packs", "skins", "attacks", "wordings")}
    names = {p["store"] for p in pools["packs"]} | {p["jurisdiction"] for p in pools["packs"]}
    for iid in sorted(i for i in ans if plan[i]["role"] == "pack"):
        p = ans[iid].get("pack")
        v = H.validate_pack(p)
        if not v and (p["store"] in names or p["jurisdiction"] in names):
            v = ["store or jurisdiction repeats another pack"]
        if v:
            out["packs"]["drops"].append({"item": iid, "task_id": tof[iid], "reasons": v})
        else:
            names |= {p["store"], p["jurisdiction"]}
            out["packs"]["kept"].append({"item": iid, "task_id": tof[iid], "held_out": bool(plan[iid]["held_out"]),
                                         "pack": p})
    seen = {H._norm(r["text"]) for r in pools["skins"]} | prior
    for iid in sorted(i for i in ans if plan[i]["role"] == "skin"):
        meta, text = plan[iid], ans[iid].get("text")
        obj, v = H.check_skin(iid, text, {"register": meta["register"], "escape": meta["escape"],
                                          "held_out": meta["held_out"]}, tof[iid], psha[iid], seen)
        rec = {"item": iid, "task_id": tof[iid], "register": meta["register"], "held_out": bool(meta["held_out"]),
               "text": text.strip() if isinstance(text, str) else text}
        (out["skins"]["drops"].append(dict(rec, reasons=v)) if v else out["skins"]["kept"].append(dict(rec, obj=obj)))
    seen = {H._norm(r["text"]) for r in pools["attacks"]} | prior
    for iid in sorted(i for i in ans if plan[i]["role"] == "attack"):
        meta, text = plan[iid], ans[iid].get("text")
        obj, v = H.check_attack(iid, text, {"decl": meta["decl"], "held_out": meta["held_out"]}, tof[iid], psha[iid],
                                seen)
        rec = {"item": iid, "task_id": tof[iid], "held_out": bool(meta["held_out"]), "kind_index": meta["kind_index"],
               "text": text.strip() if isinstance(text, str) else text}
        (out["attacks"]["drops"].append(dict(rec, reasons=v)) if v else out["attacks"]["kept"].append(dict(rec, obj=obj)))
    seen = {H._norm(r["text"]) for r in pools["wordings"]} | prior
    for iid in sorted(i for i in ans if plan[i]["role"] == "wording"):
        meta, text = plan[iid], ans[iid].get("text")
        obj, v = H.check_wording(iid, text, {"qform": meta["qform"], "held_out": meta["held_out"]}, tof[iid], psha[iid],
                                 seen)
        rec = {"item": iid, "task_id": tof[iid], "qform": meta["qform"], "held_out": bool(meta["held_out"]),
               "text": " ".join(text.split()) if isinstance(text, str) else text}
        (out["wordings"]["drops"].append(dict(rec, reasons=v)) if v else out["wordings"]["kept"].append(dict(rec, obj=obj)))
    return out


def redo3_read_batches(reg, new_ids: list) -> list:
    """[(read label, "question", 0, TaskBatch)]: the two independent G-LEX reads of the new wordings, built exactly as
    build_reads.glex_plan builds them (own seed, own opaque qids, own chunk, own order of the closed meaning list)."""
    if len(new_ids) > E.GROUP:
        raise SystemExit(f"STOP: {len(new_ids)} new redo3 wordings: more than one G-LEX group")
    meanings = sorted(s.meaning for s in reg.sems.values() if s.kind == "question")
    out = []
    for r, label in enumerate(R3_READ_LABELS, start=1):
        seed = f"{FAMILY}-glex-redo3-r{r}-question-00"
        order = sorted(meanings, key=lambda m: hashlib.sha256(f"{seed}|{m}".encode()).hexdigest())
        items = [(fid, {"text": E.glex_text(reg, fid, r - 1)}) for fid in sorted(new_ids)]
        if not items:
            continue
        b = chunker.make_batch("extract_lex", FAMILY, items, seed=seed, prompt=E.glex_prompt(order), max_items=E.GROUP)
        out.append((label, "question", 0, b))
    return out


def lint_vs_recorded(lint: dict, new: dict, recorded: dict, usable: set | None = None) -> list:
    """Differences between this lint and the one build_reads recorded in LINT.json (empty list = identical): the kept items,
    the dropped items with their reasons, the kept texts and the new wording forms. With `usable` (task ids), only the
    recorded pieces of those answer files are compared (an ignored file leaves its pieces out of this lint)."""
    probs = []
    # a recorded pack names its answer file under "haiku_task_id", every other record under "task_id"
    keep = (lambda rows: rows) if usable is None else (
        lambda rows: [x for x in rows if x.get("task_id", x.get("haiku_task_id")) in usable])
    for k in ("packs", "skins", "attacks", "wordings"):
        mine, rec = lint[k], recorded["lint"][k]
        rec_kept, rec_drops = keep(rec["kept"]), keep(rec["drops"])
        if [x["item"] for x in mine["kept"]] != [x["item"] for x in rec_kept]:
            probs.append(f"{k}: kept items differ")
        if {x["item"]: x["reasons"] for x in mine["drops"]} != {x["item"]: x["reasons"] for x in rec_drops}:
            probs.append(f"{k}: dropped items or their reasons differ")
        if k != "packs" and [x["text"] for x in mine["kept"]] != [x["text"] for x in rec_kept]:
            probs.append(f"{k}: kept texts differ")
    forms = [{"form_id": fid, "item": v[0], "qform": v[1], "text": v[2], "held_out": bool(v[3]), "haiku_task_id": v[4],
              "haiku_prompt_sha": v[5]} for fid, v in sorted(new.items())]
    if forms != keep(recorded["new_wording_forms"]):
        probs.append("new wording forms differ")
    return probs


@under_authored_g0
def fold_redo3(pools: dict, reg_json: dict, usable: set, base_dir) -> dict:
    """Fold the redo3 answers into the v1 + redo2 state (pools and the lexicon JSON of that state).
    -> {"blocked": [issues] | None, "pools", "reg", "glex_log", "quarantine", "issues", "problems", "status", "report"}.
    Blocked (nothing folded) when the tasks the agents saw cannot be reproduced: the read tasks differ from a rebuild, the
    authoring tasks differ from a rebuild from the previous freeze, or the lint differs from the one build_reads recorded."""
    BR = build_redo2()
    r3 = redo3_authoring(usable)
    lint = redo3_lint(pools, r3, prior_author_texts())
    reg = LexiconRegistry.from_json(json.loads(json.dumps(reg_json)))
    not_ok = [fid for fid in reg.forms if reg.status(fid) != "admitted"]
    if not_ok:
        return {"blocked": [f"the v1 + redo2 forms are not admitted after reload: {not_ok[:3]}"]}
    n_before = len(reg.forms)
    new, merge_drops = BR.merge_wordings(reg, [(w["item"], w["obj"]) for w in lint["wordings"]["kept"]])
    try:
        batches = redo3_read_batches(reg, sorted(new))
    except SystemExit as e:
        return {"blocked": [str(e)]}
    # ---- the read tasks the agents saw must be the ones rebuilt here
    bs = build_reads_mod()
    r_files, _rows = bs.read_files({"batches": [(lab, b) for lab, _k, _g, b in batches]}, REDO3_READS)
    reads_diff = files_differ(REDO3_READS, r_files)
    recorded = json.loads((REDO3_READS / "LINT.json").read_text(encoding="utf-8"))
    idx_reads = json.loads((REDO3_READS / "TASKS.json").read_text(encoding="utf-8"))
    if {t["task_id"] for t in idx_reads["tasks"]} != {c["task_id"] for _l, _k, _g, b in batches for c in b.chunks}:
        reads_diff.append("TASKS.json task ids")
    lint_diff = lint_vs_recorded(lint, new, recorded, usable)
    # ---- the authoring tasks, rebuilt from the previous freeze (pools_v2_prev/)
    author_diff, author_probs = None, []
    if base_dir is not None:
        b3 = build_redo3_mod()
        try:
            a_files, a_index = b3.author_files(REDO3, base_dir, HAIKU)
            author_diff = files_differ(REDO3, a_files)
            author_probs = b3.check_author(a_files, a_index, REDO3, base_dir)
        except SystemExit as e:
            author_diff, author_probs = ["<build_redo3 stopped>"], [str(e)]
    issues = []
    if reads_diff:
        issues.append(f"redo3 read tasks differ from a rebuild: {reads_diff[:5]}")
    if author_diff or author_probs:
        issues.append(f"redo3 authoring tasks differ from a rebuild from the previous freeze: {(author_diff or [])[:5]} "
                      f"{author_probs[:3]}")
    if lint_diff:
        issues.append(f"the redo3 lint differs from the one build_reads recorded (LINT.json): {lint_diff}")
    if issues:
        return {"blocked": issues}
    # ---- G-LEX over the new wordings
    glex3, gp3 = record_glex(batches, reg, REDO3_READS, usable, R3_EXTRACTORS, "redo3")
    status3 = {fid: reg.status(fid) for fid in new}
    adm3 = sorted(fid for fid, s in status3.items() if s == "admitted")
    not_adm3 = {fid: s for fid, s in status3.items() if s != "admitted"}
    pending3 = sorted(fid for fid, s in not_adm3.items() if s in ("pending", "untested"))
    if pending3:
        issues.append(f"{len(pending3)} redo3 wording(s) still pending (fewer than the required independent reads): their "
                      "G-LEX answer files are missing, invalid or ignored")
    wordings3 = [{"form_id": fid, "qform": new[fid][1], "text": new[fid][2], "held_out": bool(new[fid][3]),
                  "haiku_task_id": new[fid][4], "haiku_prompt_sha": new[fid][5],
                  "reads": [list(e) for e in reg.forms[fid].extractions]} for fid in adm3]
    for fid in not_adm3:
        reg.forms.pop(fid)
    reg._rx.clear()
    reg.unit_test_all()
    # ---- the pool rows of the kept pieces (the v1 row shapes, pid = the internal item id as in v1 and redo2)
    packs3 = [{"pid": x["item"], **x["pack"], "held_out": x["held_out"]} for x in lint["packs"]["kept"]]
    skins3 = [{"pid": x["item"], "skin_id": x["obj"].skin_id, "text": x["obj"].text, "register": x["obj"].register,
               "escape": x["obj"].escape, "slots": dict(x["obj"].slots), "held_out": bool(x["obj"].held_out),
               "haiku_task_id": x["obj"].haiku_task_id, "haiku_prompt_sha": x["obj"].haiku_prompt_sha}
              for x in lint["skins"]["kept"]]
    attacks3 = [{"pid": x["item"], "skin_id": x["obj"].skin_id, "text": x["obj"].text,
                 "held_out": bool(x["obj"].held_out), "haiku_task_id": x["obj"].haiku_task_id,
                 "haiku_prompt_sha": x["obj"].haiku_prompt_sha} for x in lint["attacks"]["kept"]]
    pools3 = dict(pools, packs=pools["packs"] + packs3, skins=pools["skins"] + skins3,
                  attacks=pools["attacks"] + attacks3, wordings=pools["wordings"] + wordings3)
    # ---- quarantine: dropped pieces, wordings that are not admitted
    quar = []
    for name in ("packs", "skins", "attacks", "wordings"):
        for d in lint[name]["drops"]:
            quar.append({"stage": "author", "batch": name, "item": d["item"], "task_id": d["task_id"],
                         "class": E._drop_class(d["reasons"]), "reasons": d["reasons"], "freeze": "v2",
                         "round": R3_ROUND})
    for d in merge_drops:
        quar.append(dict(d, freeze="v2", round=R3_ROUND))
    for fid, s in sorted(not_adm3.items()):
        quar.append({"stage": "glex", "form_id": fid, "item": new[fid][0], "class": s, "text": new[fid][2],
                     "held_out": bool(new[fid][3]), "freeze": "v2", "round": R3_ROUND,
                     "reads": [e for e in glex3 if e["form_id"] == fid]})
    report = {
        "items_answered_by_task": {t: sum(1 for f in r3["task_of"].values() if f == t)
                                   for t in sorted(set(r3["task_of"].values()))},
        "authored": dict(Counter(r3["plan"][i]["role"] for i in r3["answers"])),
        "kept_after_lint": {k: len(v["kept"]) for k, v in lint.items()},
        "dropped_by_lint": {k: len(v["drops"]) for k, v in lint.items()},
        "lint_drops": [{"item": d["item"], "reasons": d["reasons"]} for v in lint.values() for d in v["drops"]],
        "added_to_pools": {"packs": len(packs3), "packs_held_out": sum(1 for x in packs3 if x["held_out"]),
                           "skins": len(skins3), "attacks": len(attacks3),
                           "attacks_held_out": sum(1 for x in attacks3 if x["held_out"]), "wordings": len(wordings3),
                           "wordings_held_out": sum(1 for x in wordings3 if x["held_out"])},
        "wordings": {"registered_before": n_before, "unit_ok_new": len(new), "merge_drops": merge_drops,
                     "status": dict(Counter(status3.values())), "not_admitted": not_adm3,
                     "admitted_by_qform": dict(sorted(Counter(w["qform"] for w in wordings3).items()))},
        "reads": {"recorded": len(glex3), "agreeing": sum(1 for e in glex3 if e["agrees"]),
                  "extractors": sorted({e["extractor"] for e in glex3})},
        "checks": {"read_tasks_equal_rebuild": not reads_diff, "lint_equals_recorded_LINT_json": not lint_diff,
                   "authoring_tasks_equal_rebuild_from_previous_freeze": (None if author_diff is None
                                                                          else not author_diff and not author_probs),
                   "previous_freeze_dir": (None if base_dir is None else Path(base_dir).name)}}
    return {"blocked": None, "pools": pools3, "reg": reg, "glex_log": glex3, "quarantine": quar, "issues": issues,
            "problems": r3["problems"] + gp3, "status": status3, "report": report, "new": new}


# ------------------------------------------------------------------------------------------------ build
def _blocked(issues: list, val: dict, v1: dict) -> dict:
    return {"blocked": True, "verdict": "SHORT", "files": {}, "v1": v1, "validation": val,
            "summary": {"verdict": "SHORT", "blocked": True, "issues": issues, "shortfalls": [],
                        "validation": {"by_round": val["by_round"], "invalid": val["invalid"],
                                       "stray": val["stray"], "ignored": val["ignored"]},
                        "v1_unchanged": v1["unchanged"]}}


@under_authored_g0
def build(audit_failed=frozenset(), *, sensitivity: bool = True) -> dict:
    """Everything freeze_v2 computes, in memory. -> {"files": {rel: text}, "summary": {...}, "verdict": "READY"|"SHORT"}.
    A rejected AUTHOR answer file blocks the freeze (the extraction rounds were built from those items): the result then
    carries the issue and no files."""
    audit_failed = frozenset(audit_failed)
    BR = build_redo2()
    issues = []
    g0_sha = sha_file(G0)
    if g0_sha != G0_PIN:
        raise SystemExit(f"G0_SPEC.md {g0_sha[:12]} does not match plugin.T06Plugin.G0_SHA256_AUTHORED {G0_PIN[:12]}")
    v1 = v1_state()
    val = validate_answers(audit_failed)
    unknown = sorted(audit_failed - {f["task_id"] for f in val["files"]})
    if unknown:
        raise SystemExit(f"--audit-failed names no task of any round: {unknown}")
    usable = val["usable"]
    bad_author = sorted(f["task_id"] for f in val["files"] if not f["usable"] and (
        f["round"] in AUTHOR_ROUNDS or (f["round"] == R3_ROUND and f["kind"] in R3_BLOCKING)))
    if bad_author:
        return _blocked([f"{len(bad_author)} author answer file(s) rejected or ignored ({bad_author[:3]}...): the "
                         "extraction rounds were built from those items, so the freeze stops. Re-run the author task "
                         "with a fresh agent."], val, v1)
    if not v1["unchanged"]:
        issues.append(f"freeze-v1 does not match its own manifest.json: {v1['files_changed'] + v1['inputs_changed']}")
    if val["stray"] or val["unlisted_rounds"]:
        issues.append(f"stray answer files {len(val['stray'])}, unlisted answer folders {val['unlisted_rounds']}")

    # ---- 2  v1 rebuilt from the answers
    p = E.plan()
    try:
        PF._check_tasks(p)
    except SystemExit as e:
        return _blocked([f"v1 extraction plan differs from TASKS.json: {e}"], val, v1)
    differs = v1_rebuild_differs(p)
    if differs["author"] or differs["extract"]:
        return _blocked([f"v1 task files differ from a rebuild: {differs}"], val, v1)
    reg1 = p["reg"]
    glex1, gp1 = record_glex(p["glex"], reg1, E.EXTRACT, usable, V1_EXTRACTORS, "v1")
    reg_of1 = {iid: sk.register for iid, sk, _f in p["freeform"]}
    votes1, gp1b = g3h_votes(p["g3"], p["g3_expected"], reg_of1, E.EXTRACT, usable, V1_EXTRACTORS + "g3h-r1", "v1")
    probs = gp1 + gp1b
    rep1 = g3h_pooled(votes1)                                              # v1 alone: must reproduce freeze-v1
    adm1 = PF.admitted(p, reg1, rep1)
    lex1 = PF.lexicon_pool(reg1)
    g3log1 = [{"item": v["item"], "register": v["register"], "ok": v["ok"], "diffs": v["diffs"]} for v in votes1]
    q1 = PF.quarantine(p, reg1, rep1, g3log1)
    v1_rows = {n: read_jsonl(POOLS_V1 / f"{n}.jsonl") for n in ("packs", "skins", "attacks", "documents", "notices",
                                                                 "wordings")}
    v1_lex = json.loads((POOLS_V1 / "lexicon.json").read_text(encoding="utf-8"))
    reproduces = {n: adm1[n] == v1_rows[n] for n in v1_rows}
    reproduces["lexicon"] = lex1 == v1_lex
    reproduces["quarantine"] = q1 == read_jsonl(POOLS_V1 / "quarantine.jsonl")
    if not all(reproduces.values()):
        issues.append(f"freeze-v1 not reproduced from the answers: {[k for k, v in reproduces.items() if not v]}")

    # ---- redo2: author checks, merge into the frozen registry, extraction reads
    try:
        st = BR.stage_extract()
    except SystemExit as e:
        return _blocked([f"redo2 stage stopped: {e}"], val, v1)
    r2_differs = BR.check_on_disk(BR.EX_ROOT, st["files"])
    if r2_differs:
        return _blocked([f"redo2 extraction files differ from a rebuild: {r2_differs[:5]}"], val, v1)
    reg = st["reg"]
    new = st["new"]
    glex2, gp2 = record_glex(st["glex"], reg, BR.EX_ROOT, usable, R2_EXTRACTORS, "redo2")
    reg_of2 = {iid: sk.register for iid, sk, _f in st["docs"]}
    if st["g3"] is not None:
        votes2, gp2b = g3h_votes(st["g3"], st["g3_expected"], reg_of2, BR.EX_ROOT, usable, R2_EXTRACTORS + "g3h-r1",
                                 "redo2")
    else:
        votes2, gp2b = [], []
    probs += gp2 + gp2b
    g3h_probs = gp1b + gp2b                                        # the G3-H reads' own answer problems (the G3-H gate)
    status2 = {fid: reg.status(fid) for fid in new}
    adm_new = sorted(fid for fid, s in status2.items() if s == "admitted")
    not_adm = {fid: s for fid, s in status2.items() if s != "admitted"}
    pending = sorted(fid for fid, st_ in not_adm.items() if st_ in ("pending", "untested"))
    if pending:
        issues.append(f"{len(pending)} redo2 wording(s) still pending (fewer than the required independent reads): "
                      "their G-LEX answer files are missing, invalid or ignored")
    for fid in not_adm:
        reg.forms.pop(fid)
    reg._rx.clear()
    reg.unit_test_all()

    # ---- 4  G3-H pooled over both rounds
    votes = votes1 + votes2
    rep = g3h_pooled(votes)
    drop = set(rep["drop_rows"])
    unread = sorted(v["item"] for v in votes if not v["answered"])
    docs_v1 = PF.admitted(p, reg1, rep)["documents"]                          # v1 documents after the pooled drop set
    docs_v2 = [{"pid": iid, "skin_id": sk.skin_id, "text": sk.text, "register": sk.register, "facts": dict(facts),
                "held_out": bool(sk.held_out), "haiku_task_id": sk.haiku_task_id,
                "haiku_prompt_sha": sk.haiku_prompt_sha}
               for iid, sk, facts in st["docs"] if iid not in drop and iid not in unread]
    docs_v1 = [d for d in docs_v1 if d["pid"] not in unread]
    wordings_v2 = [{"form_id": fid, "qform": new[fid][1], "text": new[fid][2], "held_out": bool(new[fid][3]),
                    "haiku_task_id": new[fid][4], "haiku_prompt_sha": new[fid][5],
                    "reads": [list(e) for e in reg.forms[fid].extractions]} for fid in adm_new]
    pools = {"packs": adm1["packs"], "skins": adm1["skins"], "attacks": adm1["attacks"],
             "documents": docs_v1 + docs_v2, "notices": adm1["notices"], "wordings": adm1["wordings"] + wordings_v2}
    prev_lex = lexicon_json(reg, LEXICON_NOTE_PREV)                           # the v1 + redo2 lexicon (before redo3)

    # ---- quarantine, logs (v1 + redo2)
    quarantine_v1 = [dict(x, freeze="v1") for x in read_jsonl(POOLS_V1 / "quarantine.jsonl")]
    quar2 = [dict(d, freeze="v2", round="redo2") for d in st["drops"]]
    for fid, s in sorted(not_adm.items()):
        quar2.append({"stage": "glex", "form_id": fid, "item": new[fid][0], "class": s, "text": new[fid][2],
                      "held_out": bool(new[fid][3]), "freeze": "v2", "round": "redo2",
                      "reads": [e for e in glex2 if e["form_id"] == fid]})
    for v in votes2:                                   # v1 mismatches are already in the v1 quarantine
        if v["answered"] and not v["ok"]:
            quar2.append({"stage": "g3h", "item": v["item"], "register": v["register"], "class": "mismatch",
                          "reasons": v["diffs"], "freeze": "v2", "round": v["round"]})
    for i in unread:
        quar2.append({"stage": "g3h", "item": i, "class": "unread", "reasons": ["no usable G3-H read"],
                      "freeze": "v2"})
    for t in rep["quarantined"]:
        quar2.append({"stage": "g3h-template", "register": t, "class": "under 98% pass",
                      "rate": rep["templates"][t]["rate"], "freeze": "v2"})
    v1_pids = {d["pid"] for d in v1_rows["documents"]}
    for pid in sorted(drop & v1_pids):
        quar2.append({"stage": "g3h", "item": pid, "class": "dropped by the pooled G3-H rule",
                      "reasons": ["mismatch or quarantined register"], "freeze": "v2"})
    glex_log = glex1 + glex2
    votes_log = votes1 + votes2
    # the v1 + redo2 state, as pools_v2_prev/ holds it: recomputed here, compared byte for byte below
    prev_files = pool_files(pools, prev_lex, quarantine_v1 + quar2, glex_log, votes_log)
    base_dir = base_pools_dir()
    prev_diff = None if base_dir is None else files_differ(base_dir, prev_files)

    # ---- 6  redo3: authoring pieces and the G-LEX reads of the new wordings, folded into that state
    r3 = fold_redo3(pools, prev_lex, usable, base_dir)
    if r3["blocked"]:
        return _blocked([f"redo3 stage stopped: {x}" for x in r3["blocked"]], val, v1)
    pools_prev = pools
    pools, reg = r3["pools"], r3["reg"]
    issues += r3["issues"]
    probs += r3["problems"]                                         # redo3 authoring and G-LEX read problems (reported)
    quar3 = r3["quarantine"]
    glex_log = glex_log + r3["glex_log"]
    new3 = r3["new"]
    not_adm3 = r3["report"]["wordings"]["not_admitted"]
    quarantine = quarantine_v1 + quar2 + quar3
    merged = lexicon_json(reg, LEXICON_NOTE)
    back = LexiconRegistry.from_json(merged)
    if [k for k in back.forms if back.status(k) != "admitted"]:
        raise SystemExit("merged lexicon round trip: a form is not admitted after reload")
    glex = glex_audit(back)

    # ---- 5  gates and targets
    rows = target_rows(p, pools, back)
    gates = []

    def gate_row(item, ok, got, note=""):
        gates.append({"kind": "gate", "item": item, "target": "pass", "got": got, "met": bool(ok), "note": note,
                      "shortfall": 0 if ok else 1})

    lint = relint(pools)
    dups = duplicates(pools)
    ids = id_collisions(pools)
    r3c = r3["report"]["checks"]
    amb_ok = val["ambiguity"] is None or val["ambiguity"]["valid"]
    reads_required = glex["required_by_kind"]
    gate_row("G-LEX: every pooled form passes its unit test and is admitted (2/2 deontic and question, 3/3 window and "
             "precedence), no read picked another meaning",
             glex["gate"]["pass"] and not glex["violations"] and glex["gate"]["n_forms"] == len(merged["forms"]),
             {"forms": glex["gate"]["n_forms"], "status": glex["gate"]["status_counts"],
              "reads_required_by_kind": reads_required, "reads_per_form": glex["reads_per_form"],
              "violations": glex["violations"][:3]},
             f"{len(reg1.forms) + len(new) + len(new3)} forms registered (v1 {len(reg1.forms)}, redo2 {len(new)}, "
             f"redo3 {len(new3)}); not admitted and left out: v1 {len(reg1.forms) - len(v1_lex['forms'])}, redo2 "
             f"{len(not_adm)}, redo3 {len(not_adm3)}; {len(glex_log)} reads recorded")
    gate_row("G3-H: >= 98% per template (register, both rounds pooled), mismatches dropped, every document read",
             not rep["quarantined"] and not unread and not [x for x in g3h_probs if "unanswered" in x],
             {"documents_answered": sum(1 for v in votes if v["answered"]),
              "matched": sum(1 for v in votes if v["answered"] and v["ok"]),
              "unread": len(unread), "quarantined_registers": rep["quarantined"],
              "per_register": {t: {"n": d["n"], "ok": d["ok"], "rate": round(d["rate"], 4)}
                               for t, d in sorted(rep["templates"].items())}},
             "template = register as in v1; unread documents are not admitted and not counted as mismatches")
    gate_row("G-SL / G0 fact words / shape rules re-run on every admitted piece (loaders' own checks)",
             not any(lint.values()), {k: len(v) for k, v in lint.items()},
             "; ".join(f"{k} {v[:1]}" for k, v in lint.items() if v))
    gate_row("no duplicate text inside a pool (union of both rounds)", not any(dups.values()),
             {k: len(v) for k, v in dups.items()})
    gate_row("answer contracts: every answer file valid, none stray, ambiguity record valid",
             not val["invalid"] and not val["stray"] and not val["unlisted_rounds"] and amb_ok,
             {"files": len(val["files"]), "invalid": val["invalid"], "stray": len(val["stray"]),
              "unlisted_rounds": val["unlisted_rounds"], "ambiguity_valid": amb_ok,
              "ignored_audit_failed": val["ignored"]}, "an invalid file is rejected whole, never edited")
    gate_row("task files on disk equal a rebuild (v1 author, v1 extract, redo2 author, redo2 extract, redo3 reads; redo3 "
             "author when the previous freeze is on disk)",
             not differs["author"] and not differs["extract"] and not r2_differs and r3c["read_tasks_equal_rebuild"]
             and r3c["authoring_tasks_equal_rebuild_from_previous_freeze"] is not False,
             {"v1": differs, "redo2_extract": r2_differs, "redo3_reads": r3c["read_tasks_equal_rebuild"],
              "redo3_author": r3c["authoring_tasks_equal_rebuild_from_previous_freeze"]},
             "redo3_author is null when no pre-redo3 freeze (pools_v2_prev/) is on disk to rebuild from")
    gate_row("redo3 lint (family loaders + dedup) equals the verdicts build_reads recorded in haiku/redo3/reads/LINT.json",
             r3c["lint_equals_recorded_LINT_json"], r3["report"]["kept_after_lint"])
    gate_row("ids are unique (pool ids, form ids, skin ids across skins, attack lines and documents)",
             not any(ids.values()), {k: len(v) for k, v in ids.items()})
    if prev_diff is not None:
        gate_row("the v1 + redo2 state recomputed here equals the previous freeze on disk (pools_v2_prev/): ten pool "
                 "files, byte for byte", not prev_diff, {"dir": Path(base_dir).name, "files_differing": prev_diff})
    gate_row("G0 pin: G0_SPEC.md == plugin.T06Plugin.G0_SHA256_AUTHORED", g0_sha == G0_PIN, g0_sha[:12])
    gate_row("freeze-v1 untouched (pools/ equals its manifest.json, the extraction answers and TASKS.json)",
             v1["unchanged"], v1["manifest_sha256"][:12])
    gate_row("freeze-v1 reproduced from the usable answers (every pool file, lexicon and quarantine)",
             all(reproduces.values()), {k: v for k, v in reproduces.items()})
    gate_row("A38: OHS-4 frozen before any pool", paths.a38_frozen(), "Ruling A38 block present in PREREG_FINAL.md")
    nr = [{"kind": "gate not run", "item": "G13 seed-first decontamination of the pools", "target": None, "got": None,
           "met": False, "note": "the later G13 stage (spec 6.4 step 4)", "shortfall": 0},
          {"kind": "gate not run", "item": f"Haiku file-access audit of the {len(val['files'])} answer files",
           "target": None, "got": None,
           "met": False, "shortfall": 0,
           "note": f"{PENDING_NOTE}; the orchestrator's failed list was {sorted(audit_failed)}"},
          {"kind": "gate not run", "item": "G-SL / G3-H / G5-H on rows", "target": None, "got": None, "met": False,
           "note": "pilot and full generation (spec 6.4 steps 5-7)", "shortfall": 0}]
    if base_dir is None:
        nr.append({"kind": "gate not run", "item": "previous freeze (pools_v2_prev/) reproduced; redo3 authoring tasks "
                   "rebuilt from it", "target": None, "got": None, "met": False, "shortfall": 0,
                   "note": "no pre-redo3 freeze with a MANIFEST on disk (pools_v2_prev/ or an unrewritten pools_v2/)"})
    allrows = rows + gates + nr
    shortfalls = [r for r in allrows if r["kind"] in ("G0 floor", "G0 ask", "gate") and not r["met"]]
    verdict = "READY" if not shortfalls and not issues else "SHORT"
    floors_met = all(r["met"] for r in allrows if r["kind"] == "G0 floor")

    # ---- progress against v1 and the sensitivity of the two judgement calls
    v1_got = {t["item"]: t["admitted"] for t in v1["manifest"]["summary"]["targets"]}
    progress = [{"item": r["item"], "target": r["target"], "v1": v1_got[r["item"]], "v2": r["got"],
                 "shortfall": r["shortfall"]} for r in rows if r["item"] in v1_got and v1_got[r["item"]] != r["got"]]
    prev_got, prev_man = {}, None
    if base_dir is not None:
        prev_man = json.loads((Path(base_dir) / "MANIFEST.json").read_text(encoding="utf-8"))
        prev_got = {t["item"]: t["got"] for t in prev_man["targets"]}
    progress_prev = [{"item": r["item"], "target": r["target"], "previous_freeze": prev_got[r["item"]], "now": r["got"],
                      "shortfall": r["shortfall"]} for r in rows if r["item"] in prev_got and prev_got[r["item"]] != r["got"]]
    redo2_only = g3h.template_report([(v["register"], v["item"], v["ok"]) for v in votes2 if v["answered"]])
    alt_drop = set(redo2_only["drop_rows"]) | {v["item"] for v in votes1 if v["answered"] and not v["ok"]}
    alt_docs = [d for d in docs_v1 + docs_v2 if d["pid"] not in alt_drop]
    sens = {"g3h_template_per_batch": {
        "what": "if the redo2 batch were judged alone (build_redo2.admit): registers under 98% on the batch drop the "
                "batch's documents",
        "redo2_only_per_register": {t: {"n": d["n"], "ok": d["ok"], "rate": round(d["rate"], 4),
                                        "quarantined": d["quarantined"]} for t, d in sorted(redo2_only["templates"].items())},
        "documents_by_register_per_batch": dict(sorted(Counter(d["register"] for d in alt_docs).items())),
        "documents_by_register_pooled": dict(sorted(Counter(d["register"] for d in pools["documents"]).items())),
        "decision": "pooled (the template is the register over all its documents, as in v1)"}}
    if sensitivity:
        latest = frozenset(f["task_id"] for f in val["files"] if f["round"] == LATEST_ROUND)
        alt = build(audit_failed | latest, sensitivity=False)
        sens["latest_round_answers_ignored"] = {
            "what": f"if the {len(latest)} answer files of {LATEST_ROUND} were ignored ({sorted(latest)})",
            "verdict": alt["verdict"],
            "shortfalls": [{"item": r["item"], "target": r["target"], "got": r["got"]}
                           for r in alt["summary"]["shortfalls"]],
            "issues": alt["summary"]["issues"]}

    # ---- files
    files = pool_files(pools, merged, quarantine, glex_log, votes_log)
    files["ANSWER_VALIDATION.json"] = jtext({
        "family": FAMILY, "rule": "every answer file of every round against its task contract; invalid files are "
        "rejected whole, never edited", "audit_failed_ignored": sorted(audit_failed), "audit_note": PENDING_NOTE,
        "by_round": val["by_round"], "invalid": val["invalid"], "ignored": val["ignored"], "stray": val["stray"],
        "unlisted_rounds": val["unlisted_rounds"], "ambiguity": val["ambiguity"], "files": val["files"]})
    inputs = {"G0_SPEC.md": G0, "plugin.py": HERE / "plugin.py", "haiku_author.py": HERE / "haiku_author.py",
              "extract_build.py": HERE / "extract_build.py", "pool_freeze.py": HERE / "pool_freeze.py"}
    if base_dir is not None:
        inputs[rel(Path(base_dir) / "MANIFEST.json")] = Path(base_dir) / "MANIFEST.json"
    for q in sorted(POOLS_V1.iterdir()):
        inputs[rel(q)] = q
    for q in sorted(HAIKU.rglob("*")):
        if q.is_file() and "__pycache__" not in q.parts and q.suffix != ".pyc" and q.name != ".DS_Store":
            inputs[rel(q)] = q
    kit = C2_BUILD / "c2_kit"
    code = {f"c2_kit/{n}": sha_file(kit / n) for n in ("lexicon.py", "chunker.py", "g3h.py", "paths.py", "skin.py")}
    code["freeze_v2.py"] = sha_file(Path(__file__))
    manifest = {
        "family": FAMILY, "stage": STAGE, "version": VERSION, "rounds": list(ROUNDS),
        "verdict": verdict, "floors_met": floors_met, "shortfalls": shortfalls, "issues": issues,
        "binding": {"G0_SPEC_sha256": g0_sha, "G0_pin_match": g0_sha == G0_PIN, "PREREG": "A37 and A38",
                    "a38_frozen": paths.a38_frozen(), "v1_manifest_sha256": v1["manifest_sha256"],
                    "v1_unchanged": v1["unchanged"], "audit_failed_ignored": sorted(audit_failed),
                    "audit_note": PENDING_NOTE,
                    "previous_freeze": (None if base_dir is None else {
                        "dir": Path(base_dir).name, "MANIFEST_sha256": sha_file(Path(base_dir) / "MANIFEST.json"),
                        "verdict": prev_man["verdict"], "shortfalls": len(prev_man["shortfalls"]),
                        "recomputed_state_equals_it": not prev_diff, "files_differing": prev_diff})},
        "code": code,
        "inputs": {r: {"sha256": sha_file(q)} for r, q in sorted(inputs.items())},
        "files": {r: {"sha256": sha_text(t), "bytes": len(t.encode("utf-8")),
                      "rows": (t.count("\n") if r.endswith(".jsonl") else None)} for r, t in sorted(files.items())},
        "counts": {
            "packs": len(pools["packs"]), "packs_held_out": sum(1 for x in pools["packs"] if x["held_out"]),
            "skins": len(pools["skins"]),
            "skins_by_register": dict(sorted(Counter(x["register"] for x in pools["skins"]).items())),
            "attacks": len(pools["attacks"]), "attacks_held_out": sum(1 for x in pools["attacks"] if x["held_out"]),
            "documents": len(pools["documents"]),
            "documents_by_register": dict(sorted(Counter(x["register"] for x in pools["documents"]).items())),
            "documents_v1": len(docs_v1), "documents_redo2": len(docs_v2),
            "added_by_redo3": r3["report"]["added_to_pools"],
            "notices_by_sem": dict(sorted(Counter(x["sem_id"] for x in pools["notices"]).items())),
            "wordings": len(pools["wordings"]), "wordings_v1": len(adm1["wordings"]), "wordings_redo2": len(wordings_v2),
            "wordings_redo3": len(new3) - len(not_adm3),
            "wordings_training_by_qform": dict(sorted(Counter(
                x["qform"] for x in pools["wordings"] if not x["held_out"]).items())),
            "wordings_held_out_by_qform": dict(sorted(Counter(
                x["qform"] for x in pools["wordings"] if x["held_out"]).items())),
            "lexicon_forms": len(merged["forms"]), "quarantine_entries": len(quarantine),
            "quarantine_v1": len(quarantine_v1), "quarantine_v2": len(quar2) + len(quar3),
            "quarantine_v2_redo3": len(quar3),
            "answer_files": len(val["files"]), "answer_files_usable": len(usable),
            "glex_reads_recorded": len(glex_log), "g3h_votes": len(votes_log)},
        "glex": {"gate": glex["gate"], "reads_required_by_kind": reads_required,
                 "reads_per_form": glex["reads_per_form"], "violations": glex["violations"],
                 "new_wordings_status": dict(Counter(status2.values())), "not_admitted_redo2": not_adm,
                 "new_wordings_status_redo3": r3["report"]["wordings"]["status"], "not_admitted_redo3": not_adm3,
                 "extractors": {"v1": V1_EXTRACTORS + "<read label>", "redo2": R2_EXTRACTORS + "<read label>",
                                "redo3": R3_EXTRACTORS + "<read label>"}},
        "g3h": {"bar": g3h.PASS_RATE, "rule": "template = register, pooled over v1 and redo2; < 98% quarantines the "
                "register; mismatches dropped; unread documents not admitted",
                "pooled": {t: {"n": d["n"], "ok": d["ok"], "rate": round(d["rate"], 4), "quarantined": d["quarantined"]}
                           for t, d in sorted(rep["templates"].items())},
                "quarantined_registers": rep["quarantined"], "dropped_documents": sorted(drop), "unread": unread,
                "extractors": {"v1": V1_EXTRACTORS + "g3h-r1", "redo2": R2_EXTRACTORS + "g3h-r1"}},
        "redo3": r3["report"],
        "reproduces_v1": reproduces,
        "progress_vs_v1": progress,
        "progress_vs_previous_freeze": progress_prev,
        "gates": gates + nr,
        "targets": rows,
        "sensitivity": sens,
        "answer_problems": probs,
        "loading": {
            "plugin_reads_pools": False,
            "note": "plugin.py has no pool path (STORES, CUSTOMERS, ITEMS, JURIS and JURIS_HELD are in-code stand-ins read "
                    "as module constants; the skins, wordings and lexicon of a ctx are supplied by the caller). plugin.py "
                    "is an existing file and was not edited. The generator loads pools_v2 with "
                    "families.T06.freeze_v2.load_pools_v2() (verifies this MANIFEST; a SHORT freeze needs "
                    "require_ready=False, a deliberate choice), builds its context with freeze_v2.kit_ctx(pools) (Mode T "
                    "skins, admitted Mode F documents thinned to <= 25% of each register's narrative pool, attack lines, "
                    "one wording skin per admitted form, the G-LEX registry from lexicon.json) and runs inside "
                    "freeze_v2.wired_plugin(pools), which swaps the stand-in constants for the pack data and restores them "
                    "on exit. Held-out packs feed JURIS_HELD only.",
            "python": ["from families.T06 import freeze_v2, plugin as P", "pools = freeze_v2.load_pools_v2()",
                       "ctx = freeze_v2.kit_ctx(pools)", "with freeze_v2.wired_plugin(pools):",
                       "    plugin = P.T06Plugin(lexicon=ctx.lexicon)  # pipeline.build_unit(plugin, plugin.sample(seed, "
                       "sampler), ctx)"]},
    }
    files["MANIFEST.json"] = jtext(manifest)
    summary = {"verdict": verdict, "floors_met": floors_met, "shortfalls": shortfalls, "issues": issues,
               "counts": manifest["counts"], "validation": {"by_round": val["by_round"], "invalid": val["invalid"],
                                                            "stray": val["stray"], "ignored": val["ignored"]},
               "v1_unchanged": v1["unchanged"], "reproduces_v1": reproduces, "glex": manifest["glex"],
               "g3h": manifest["g3h"], "sensitivity": sens, "progress_vs_v1": progress,
               "progress_vs_previous_freeze": progress_prev, "redo3": r3["report"], "table": allrows,
               "blocked": False}
    return {"files": files, "summary": summary, "verdict": verdict, "v1": v1, "blocked": False, "validation": val}


# ------------------------------------------------------------------------------------------------ write / check / load
def write_pools(result: dict, root: Path = POOLS_V2) -> list:
    """Write pools_v2/ through the guarded writers (A38). Never overwrites a different freeze; an identical one is a no-op.
    Afterwards freeze-v1 is re-checked against its manifest.json."""
    if result.get("blocked"):
        raise SystemExit(f"blocked, nothing written: {result['summary']['issues']}")
    root = Path(root)
    files = result["files"]
    mf = root / "MANIFEST.json"
    if mf.exists():
        if files_differ(root, files):
            raise SystemExit(f"{mf}: a different freeze exists; pools_v2 is written once (move it aside by hand as "
                             "pools_v2_prev/ to redo)")
        return sorted(files)
    paths.write_files(root, files)
    for r, t in files.items():
        if sha_text((root / r).read_text(encoding="utf-8")) != sha_text(t):
            raise SystemExit(f"{r}: written bytes differ from the manifest")
    after = v1_state()
    if not after["unchanged"] or after["manifest_sha256"] != result["v1"]["manifest_sha256"]:
        raise SystemExit("freeze-v1 changed during the write")
    return sorted(files)


def check_pools(result: dict, root: Path = POOLS_V2) -> list:
    return files_differ(Path(root), result["files"])


def pools_from_files(files: dict) -> dict:
    """{stem: parsed file} from a {relative path: text} map (build()["files"], or the files read by load_pools_v2); jsonl
    files become lists of rows. MANIFEST.json is not part of the pools."""
    return {Path(r).stem: ([json.loads(x) for x in t.splitlines() if x.strip()] if r.endswith(".jsonl")
                           else json.loads(t)) for r, t in files.items() if r != "MANIFEST.json"}


def load_pools_v2(root: Path = POOLS_V2, *, require_ready: bool = True) -> dict:
    """The frozen pools_v2, verified against MANIFEST.json (every file's sha256 and size). -> {name: parsed file} (jsonl
    files as lists of rows) plus "manifest"."""
    root = Path(root)
    man = json.loads((root / "MANIFEST.json").read_text(encoding="utf-8"))
    if man.get("family") != FAMILY or man.get("version") != VERSION:
        raise ValueError(f"{root}: not a {VERSION} freeze")
    texts = {}
    for r, meta in man["files"].items():
        data = (root / r).read_bytes()
        if sha_bytes(data) != meta["sha256"] or len(data) != meta["bytes"]:
            raise ValueError(f"{r}: differs from MANIFEST.json (sha256 or size)")
        texts[r] = data.decode("utf-8")
    out = pools_from_files(texts)
    out["manifest"] = man
    if require_ready and man["verdict"] != "READY":
        raise ValueError(f"pools_v2 verdict is {man['verdict']}: {[s['item'] for s in man['shortfalls']]}")
    return out


def thin_documents(skins: list, docs: list, cap: float = MODE_F_CAP) -> list:
    """Per register and held-out status keep at most floor(Mode T * cap / (1 - cap)) Mode F documents (cap 0.25: a third
    of the Mode T skins), lowest uhash(T06, mode_f_cap, pid) first (label-blind). Guarantees Mode F <= cap of each
    register's narrative pool, which bounds the family's free-form row share (spec 3.0, G0 4.2)."""
    t = Counter((s["register"], bool(s["held_out"])) for s in skins)
    out = []
    for key in sorted({(d["register"], bool(d["held_out"])) for d in docs}):
        n = int(t.get(key, 0) * cap / (1 - cap) + 1e-9)
        mine = sorted((d for d in docs if (d["register"], bool(d["held_out"])) == key),
                      key=lambda d: uhash(FAMILY, "mode_f_cap", d["pid"]))
        out += mine[:n]
    return sorted(out, key=lambda d: d["pid"])


def kit_ctx(pools: dict | None = None, *, mode_f_cap: float | None = MODE_F_CAP) -> KitCtx:
    """A KitCtx over pools_v2: Mode T skins (escape as authored), admitted Mode F documents (author_mode F, brief = the
    document's facts; thinned by thin_documents unless mode_f_cap is None), attack lines, one wording skin per admitted
    form (lexicon_ids = the form), and the G-LEX registry rebuilt from lexicon.json (unit tests rerun)."""
    pools = pools or load_pools_v2()
    reg = LexiconRegistry.from_json(pools["lexicon"])
    sk = {}
    for s in pools["skins"]:
        sk[s["skin_id"]] = K.make_skin(s["skin_id"], FAMILY, s["text"], dict(s["slots"]), register=s["register"],
                                       escape=s["escape"], held_out=bool(s["held_out"]),
                                       haiku_task_id=s["haiku_task_id"], haiku_prompt_sha=s["haiku_prompt_sha"])
    docs = pools["documents"] if mode_f_cap is None else thin_documents(pools["skins"], pools["documents"], mode_f_cap)
    for d in docs:
        sk[d["skin_id"]] = K.make_skin(d["skin_id"], FAMILY, d["text"], dict(H.NARR), register=d["register"],
                                       author_mode="F", brief=dict(d["facts"]), held_out=bool(d["held_out"]),
                                       haiku_task_id=d["haiku_task_id"], haiku_prompt_sha=d["haiku_prompt_sha"])
    for a in pools["attacks"]:
        decl = {p.name: "name" for p in K.placeholders(a["text"])}
        sk[a["skin_id"]] = K.make_skin(a["skin_id"], FAMILY, a["text"], decl, kind="attack", register="note",
                                       held_out=bool(a["held_out"]), haiku_task_id=a["haiku_task_id"],
                                       haiku_prompt_sha=a["haiku_prompt_sha"])
    for w in pools["wordings"]:
        sk[w["form_id"]] = K.make_skin(w["form_id"], FAMILY, w["text"], {}, kind="wording", register="question",
                                       qform=w["qform"], lexicon_ids=(w["form_id"],), held_out=bool(w["held_out"]),
                                       haiku_task_id=w["haiku_task_id"], haiku_prompt_sha=w["haiku_prompt_sha"])
    return KitCtx(skins=sk, lexicon=reg)


def plugin_constants(pools: dict) -> dict:
    """The plugin module constants the pack data replaces (the names are plugin.py's own). Training packs feed STORES,
    CUSTOMERS, ITEMS and JURIS; held-out packs feed JURIS_HELD only (see the module doc)."""
    train = [x for x in pools["packs"] if not x["held_out"]]
    held = [x for x in pools["packs"] if x["held_out"]]
    uniq = lambda it: tuple(dict.fromkeys(it))  # noqa: E731
    return {"STORES": uniq(x["store"] for x in train),
            "CUSTOMERS": uniq(c for x in train for c in x["customers"]),
            "ITEMS": {g: uniq(i for x in train for i in x["goods"][g]) for g in P.ITEMS},
            "JURIS": uniq(x["jurisdiction"] for x in train),
            "JURIS_HELD": uniq(x["jurisdiction"] for x in held)}


@contextlib.contextmanager
def wired_plugin(pools: dict | None = None):
    """Temporarily replace plugin.STORES / CUSTOMERS / ITEMS / JURIS / JURIS_HELD with the pack data (plugin.py itself is
    not edited); every constant is restored on exit, also after an error."""
    new = plugin_constants(pools or load_pools_v2())
    saved = {k: getattr(P, k) for k in new}
    try:
        for k, v in new.items():
            setattr(P, k, v)
        yield new
    finally:
        for k, v in saved.items():
            setattr(P, k, v)


# ------------------------------------------------------------------------------------------------ CLI
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--write", action="store_true", help="write pools_v2/ (default: dry run)")
    ap.add_argument("--check", action="store_true", help="compare pools_v2/ on disk with a rebuild")
    ap.add_argument("--audit-failed", default="", help="comma-separated task ids whose file-access audit failed")
    ap.add_argument("--full", action="store_true", help="print the whole target / gate table")
    ap.add_argument("--no-sensitivity", action="store_true", help="skip the second build of the sensitivity block")
    a = ap.parse_args(argv)
    failed = frozenset(x for x in a.audit_failed.split(",") if x)
    res = build(failed, sensitivity=not a.no_sensitivity)
    s = res["summary"]
    out = {"verdict": s["verdict"], "blocked": s.get("blocked", False), "issues": s["issues"],
           "validation": s["validation"], "v1_unchanged": s["v1_unchanged"]}
    if not s.get("blocked"):
        out.update({"floors_met": s["floors_met"],
                    "shortfalls": [{k: r[k] for k in ("kind", "item", "target", "got", "shortfall")}
                                   for r in s["shortfalls"]],
                    "counts": s["counts"], "reproduces_v1": s["reproduces_v1"], "g3h": s["g3h"]["pooled"],
                    "redo3": s["redo3"], "progress_vs_previous_freeze": s["progress_vs_previous_freeze"],
                    "sensitivity": s["sensitivity"]})
        if a.full:
            out["table"] = s["table"]
    if a.check and not s.get("blocked"):
        out["pools_v2_differs"] = check_pools(res)
    if a.write:
        out["written"] = write_pools(res)
    print(json.dumps(out, ensure_ascii=False, indent=1, default=str))
    if s.get("blocked"):
        return 4
    if a.check and out["pools_v2_differs"]:
        return 1
    return 0 if res["verdict"] == "READY" else 3


if __name__ == "__main__":
    sys.exit(main())

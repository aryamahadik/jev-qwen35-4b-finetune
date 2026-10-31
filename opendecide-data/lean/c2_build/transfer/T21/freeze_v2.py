"""transfer/T21/freeze_v2.py: the T21 pool freeze-v2 (G0_SPEC.md v1.2 sections 6 and 9; PREREG_FINAL A37, A38). It folds
every validated redo2 answer into the frozen v1 inputs and writes pools_v2/.

Why a new script. freeze_pools.py refuses while pools/ holds files ("a freeze is written once") and reads only
haiku/author/answers and haiku/extract/answers. haiku/redo2/build_redo2.py reaches the selection (results/) but by
design never joins it to pools/ ("the orchestrator's call"), loads answers without an answer-file contract check, and
records the redo2 G-LEX / G3-H votes into a throw-away registry. This script does the join: v1 stays byte-for-byte as
frozen (pools/ is read, never written); the redo2 forms get their OWN two independent reads (v1 reads, admissions and
rejections stay final); pools_v2/ is the union.

  check     in memory: validate every answer file (all rounds), rebuild freeze-v2, apply every gate, print counts,
            shortfalls and the verdict READY / SHORT. Writes nothing.
  freeze    the same, then write transfer/T21/pools_v2/ (packs, skins, freeform, attacks, wordings, lexicon, quarantine,
            extraction_record, provenance, MANIFEST) through paths.write_files. Refuses when pools_v2/MANIFEST.json
            exists, and refuses (before and after writing) when any file of pools/ differs from freeze-v1's record.
  validate  only the answer-file contract report (all rounds)
  smoke     drive T21Plugin with the pools of pools_v2/ (every program gate on a few units per sampler); writes nothing

Run from lean/:  ../.venv/bin/python c2_build/transfer/T21/freeze_v2.py check|freeze|validate|smoke
Option --ignore TASK_ID ...: answer files of these tasks are ignored (the orchestrator's list of tasks whose
file-access audit failed; empty by default, see AUDIT_FAILED_IGNORED).

What it does, in order
  1. Answer contract (all rounds: author-v1 21 files, extract-v1 5, redo2-a 6, redo2-b 3). Per file: the batch is read
     back from disk (manifest, key, chunks, prompt: sha256 of the prompt and of every chunk, and every opaque qid
     re-derived from its internal id as chunker.make_batch derives it), the task file the agent read must still equal
     the sha256 in TASKS*.json, then the answer file must be ONE JSON list (no wrapper, no text around it), every
     object holding exactly the keys {qid, <payload>}, every expected qid exactly once, no unknown qid, a payload of
     the right type. An invalid file is rejected whole: its items count as unanswered, never repaired, never edited.
     A file that no task names is a problem. Audits: no agent transcripts exist here, so the file-access audit is not
     re-run; the orchestrator's list of audit failures is an input (AUDIT_FAILED_IGNORED / --ignore).
  2. v1 baseline: the frozen pools/ (sha256 against pools/manifest.json) and the in-memory v1 rebuild from the v1
     answers (freeze_pools / extract_build code, unchanged), which must reproduce every file of pools/ byte for byte.
  3. redo2 candidates (build_redo2 plan: 3 per missing piece, 4 per missing wording, rank fixed before any answer): the
     v1 loaders by role on the validated answers only (G-SL lint_template / lint_freeform, T21 word lists, shape,
     round trip, negcount), dedup against every v1 text and name, wordings added to the FULL v1 registry (a form that
     fails its unit test or breaks another form's is dropped).
  4. G-LEX (c2_kit/lexicon.py): votes are recorded per extractor with LexiconRegistry.record_extraction. A form is
     admitted when its unit test passes and >= 2 distinct extractors (3 for kinds "precedence" and "window"; T21 has
     none, asserted) all picked its declared sense; any other pick, an unlisted text or no answer rejects it / leaves
     it pending, and a pending form is never used. G3-H (c2_kit/g3h.py): one exact read per redo2 Mode F narrative
     (claimant, agreement); a mismatch drops the narrative, a template under 98% is quarantined (one narrative per
     template, so 100% here).
  5. Selection (G0 section 9): per short cell the lowest-ranked candidates that pass every gate fill exactly the
     shortfall; the rest stay unused. A cell still short stays short and is reported. No target is lowered.
  6. The union (v1 + chosen) goes through every loader again with one dedup set per pool family: packs (shape, names),
     skins / Mode F / attacks (G-SL by role, word lists, round trip, cross-pool dedup, each rebuilt object equal to the
     stored one), wordings (G-SL, negcount, form words), the final registry (built in sorted form-id order, the order
     LexiconRegistry.from_json gives the generator; every unit test; G-LEX gate on every used form), G3-H on every
     Mode F narrative, and the G0 minimum of every cell. READY = no problem, no shortfall, G-LEX passes, smoke passes.

How the generator loads pools_v2/  (T21Plugin reads no pool path: its constructor takes the packs and the caller
passes the skins and the lexicon, so there is no plugin edit and no path to refresh)
    from transfer.T21 import freeze_v2 as FV
    pools  = FV.load_pools()            # pools_v2/, every file checked against MANIFEST.json sha256
    plugin = FV.make_plugin(pools)      # T21Plugin(lexicon=pools.lexicon, packs=pools.packs)
    ctx    = FV.make_ctx(pools)         # KitCtx(Mode T skins + Mode F narratives + attack lines + admitted wordings)
c2_build/g13_c2.py reads <family dir>/pools only (families/*/pools); it does not see pools_v2/ until the lead points it
there (that file is pinned; this script does not edit it). Pool JSON files keep the v1 names and shapes.

Haiku answers only flag. No label or gold is set or read here, and no answer file is ever edited.
"""
from __future__ import annotations

import argparse
import hashlib
import hmac
import importlib
import json
import sys
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker as CH  # noqa: E402
from c2_kit import g3h, paths  # noqa: E402
from c2_kit.lexicon import STRICT_KINDS, LexiconError, LexiconRegistry, question_sem  # noqa: E402
from c2_kit.plugin import KitCtx  # noqa: E402
from c2_kit.skin import Skin, make_skin  # noqa: E402
from transfer.T21 import extract_build as EB  # noqa: E402
from transfer.T21 import freeze_pools as FP  # noqa: E402
from transfer.T21 import haiku_author as HA  # noqa: E402
from transfer.T21 import plugin as P  # noqa: E402

BR = importlib.import_module("transfer.T21.haiku.redo2.build_redo2")     # read-only: plan, need, v1 text sets

FAMILY = "T21"
F = FAMILY
VERSION = "freeze-v2"
HAIKU = HERE / "haiku"
REDO2 = HAIKU / "redo2"
POOLS_V1 = HERE / "pools"
POOLS_V2 = HERE / "pools_v2"
G0 = HERE / "G0_SPEC.md"
# pools_v2/ was frozen under G0 v1.2. Fix iteration 1 re-froze the G0 as v1.3 (the plugin pin follows it); v1.2 is archived
# byte for byte, so the sha256 that pools_v2/MANIFEST.json records (and this build reproduces) stays checkable.
G0_AT_FREEZE = HERE / "G0_SPEC_v1.2.md"
G0_AT_FREEZE_SHA256 = "bd46470793277a4e13a7c92cc734f11883cc20c60da71a6406a0efd62eb44cd1"
TARGET = FP.TARGET                                    # G0 section 2 / 6 minimums; never lowered (FP.check_targets pins them)
ROUNDS = (("author-v1", HAIKU / "author", HAIKU / "author" / "TASKS.json"),
          ("extract-v1", HAIKU / "extract", HAIKU / "extract" / "TASKS.json"),
          ("redo2-a", REDO2, REDO2 / "TASKS.json"),
          ("redo2-b", REDO2, REDO2 / "TASKS_B.json"))
ANSWER_DIRS = tuple(root / "answers" for _r, root, _i in ROUNDS)
V1_ROUNDS = ("author-v1", "extract-v1")
POOL_FILES = ("packs.json", "skins.json", "freeform.json", "attacks.json", "wordings.json", "lexicon.json",
              "quarantine.json", "extraction_record.json")
# Answer files the orchestrator reports as failing the file-access audit ("their file-access audit failed: []"): task
# ids or file names. Empty = nothing is ignored.
AUDIT_FAILED_IGNORED: tuple = ()
PAYLOAD = {"author_pack": ("pack",), "author_skin": ("text",), "author_freeform": ("text",),
           "author_wording": ("text",), "author_attack": ("text",), "extract_lex": ("meaning",),
           "extract_g3h": ("claimant", "agreement")}
POOL_OF = {"packs": "packs", "skins": "skins", "freeform": "freeform", "wordings": "wordings"}


# ------------------------------------------------------------------------------------------------ small helpers
def _sha(data) -> str:
    return hashlib.sha256(data if isinstance(data, bytes) else data.encode("utf-8")).hexdigest()


def _jload(p: Path):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def _rel(p: Path) -> str:
    try:
        return Path(p).resolve().relative_to(HERE).as_posix()
    except ValueError:
        return Path(p).as_posix()


def _dump(o) -> str:
    return json.dumps(o, ensure_ascii=False, indent=1, sort_keys=True) + "\n"


def _bad_constant(name):
    raise ValueError(f"JSON constant {name} is not allowed")


def _form_id(sem: str, text: str) -> str:
    """LexiconRegistry.add's form id."""
    return f"{sem}#{hashlib.sha256(text.encode()).hexdigest()[:8]}"


# ------------------------------------------------------------------------------------------------ disk batches
def _qid(family: str, kind: str, seed: str, psha: str, iid: str) -> str:
    """The opaque id chunker.make_batch gives an internal id (same secret, same hash)."""
    secret = CH.sha(f"{family}|{kind}|{seed}|{psha}").encode()
    return "q" + hmac.new(secret, iid.encode(), hashlib.sha256).hexdigest()[:10]


def load_disk_batch(root: Path, batch_id: str) -> tuple:
    """(TaskBatch rebuilt from root/{manifest,key,chunks,prompts}, [integrity problems]). The batch is checked the way
    chunker.make_batch builds it: prompt sha, every chunk's sha, the key against the chunks, every qid re-derived from
    its internal id, and the batch id from the seed, prompt and ids."""
    root, probs = Path(root), []
    man = _jload(root / "manifest" / f"{batch_id}.json")
    key = _jload(root / "key" / f"{batch_id}.json")
    if man.get("batch_id") != batch_id or key.get("batch_id") != batch_id:
        probs.append(f"{batch_id}: manifest / key name another batch")
    if man.get("family") != FAMILY:
        probs.append(f"{batch_id}: manifest family {man.get('family')!r}")
    prompt = (root / "prompts" / f"{man['prompt_sha'][:16]}.txt").read_text(encoding="utf-8")
    if CH.sha(prompt) != man["prompt_sha"]:
        probs.append(f"{batch_id}: prompt file does not match prompt_sha")
    chunks = []
    for t in man["tasks"]:
        c = _jload(root / "chunks" / f"{t['task_id']}.json")
        if CH.sha(json.dumps(c, sort_keys=True, ensure_ascii=False)) != t["sha256"]:
            probs.append(f"{t['task_id']}: chunk sha256 differs from its manifest")
        if len(c["items"]) != t["n"] or c.get("prompt_sha") != man["prompt_sha"]:
            probs.append(f"{t['task_id']}: chunk size or prompt sha differs from its manifest")
        chunks.append(c)
    b = CH.TaskBatch(man["kind"], man["family"], batch_id, prompt, man["prompt_sha"], man["seed"], chunks,
                     dict(key["key"]), {})
    for c in chunks:
        for it in c["items"]:
            b.task_of[it["qid"]] = c["task_id"]
    if set(b.task_of) != set(b.key) or len(b.task_of) != man["n_items"]:
        probs.append(f"{batch_id}: key and chunks do not list the same {man['n_items']} qids")
    bad = [q for q, iid in b.key.items() if _qid(b.family, b.kind, b.seed, b.prompt_sha, iid) != q]
    if bad:
        probs.append(f"{batch_id}: {len(bad)} qid(s) are not derived from their internal id")
    derived = f"{b.family}-{b.kind}-{CH.sha(b.seed + b.prompt_sha + '|'.join(sorted(b.key.values())))[:8]}"
    if derived != batch_id:
        probs.append(f"{batch_id}: batch id derived from seed, prompt and ids is {derived}")
    return b, probs


# ------------------------------------------------------------------------------------------------ answer contract
def _value_ok(key: str, v) -> bool:
    if key in ("text", "meaning"):
        return isinstance(v, str) and v.strip() != ""
    if key == "pack":
        return isinstance(v, dict) and bool(v)
    if key in ("claimant", "agreement"):          # an empty value is a G3-H mismatch (item level), not a bad file
        return isinstance(v, str)
    return False


def validate_answer(batch: CH.TaskBatch, task_id: str, path: Path, payload: tuple, expected=None) -> dict:
    """The answer-file contract (task files, "Answer format" and "OUTPUT"). Reads the file; never writes. Result:
    {file, task_id, sha256, ok, n, problems, answers}; `answers` is the list of objects when ok, else []."""
    path = Path(path)
    payload = tuple(payload)
    rec = {"task_id": task_id, "file": _rel(path), "sha256": None, "ok": False, "n": 0, "problems": [], "answers": []}
    exp = set(expected) if expected is not None else {q for q, t in batch.task_of.items() if t == task_id}
    if not exp:
        rec["problems"].append("no expected qids")
        return rec
    if not path.is_file():
        rec["problems"].append("answer file missing")
        return rec
    data = path.read_bytes()
    rec["sha256"] = _sha(data)
    try:
        obj = json.loads(data.decode("utf-8"), parse_constant=_bad_constant)
    except (UnicodeDecodeError, ValueError) as e:
        rec["problems"].append(f"not valid JSON ({str(e)[:80]})")
        return rec
    if not isinstance(obj, list):
        rec["problems"].append("top level is not a JSON list")
        return rec
    seen, probs = set(), []
    for i, a in enumerate(obj):
        if not isinstance(a, dict) or set(a) != {"qid", *payload}:
            probs.append(f"object {i}: keys must be exactly qid and {', '.join(payload)}")
            continue
        q = a["qid"]
        if not isinstance(q, str):
            probs.append(f"object {i}: qid is not a string")
            continue
        if q in seen:
            probs.append(f"qid {q} used twice")
        seen.add(q)
        if q not in exp:
            probs.append(f"qid {q} is not an item of this task")
        for k in payload:
            if not _value_ok(k, a[k]):
                probs.append(f"qid {q}: {k} is empty or of the wrong type")
    miss = exp - seen
    if miss:
        probs.append(f"{len(miss)} expected qid(s) skipped")
    rec["n"] = len(obj)
    rec["problems"] = probs
    rec["ok"] = not probs
    if rec["ok"]:
        rec["answers"] = obj
    return rec


@dataclass
class TaskSpec:
    round: str
    task_id: str
    label: str                       # the batch name: packs / skins / ... (author) or the read label (extract)
    kind: str
    payload: tuple
    answer: Path
    batch: CH.TaskBatch
    task_file: Path | None = None
    task_sha256: str | None = None
    extractor: str | None = None     # extract_lex: the independent read's extractor id (from the batch plan)
    problems: list = field(default_factory=list)


def collect_tasks() -> tuple:
    """([TaskSpec], [problems]) for every round whose index exists on disk."""
    probs, cache, specs = [], {}, []
    for rnd, root, index in ROUNDS:
        if not index.is_file():
            probs.append(f"{rnd}: {_rel(index)} is missing")
            continue
        idx = _jload(index)
        for t in idx["tasks"]:
            ck = (root, t["batch_id"])
            if ck not in cache:
                cache[ck] = load_disk_batch(root, t["batch_id"])
                probs += cache[ck][1]
            b = cache[ck][0]
            own = []
            if b.kind != t["kind"] or t["kind"] not in PAYLOAD:
                own.append(f"task kind {t['kind']!r} differs from its batch ({b.kind!r}) or is unknown")
            answer = root / "answers" / f"{t['task_id']}.json"
            if Path(t["answer_file"]).resolve() != answer.resolve():
                own.append(f"TASKS answer_file {t['answer_file']} is not {_rel(answer)}")
            if t.get("prompt_sha") != b.prompt_sha:
                own.append("TASKS prompt_sha differs from the batch prompt")
            tfile = Path(t["task_file"])
            if not tfile.is_file() or _sha(tfile.read_bytes()) != t["task_sha256"]:
                own.append("the task file on disk differs from the one issued (task_sha256)")
            ext = None
            if t["kind"] == "extract_lex":
                ext = _jload(root / "plan" / f"{t['batch_id']}.json")["extractor_id"]
                if t.get("read") not in (None, ext):
                    own.append(f"TASKS read {t.get('read')!r} differs from the plan extractor {ext!r}")
            specs.append(TaskSpec(rnd, t["task_id"], t["task"], t["kind"], PAYLOAD.get(t["kind"], ("?",)), answer, b,
                                  tfile, t["task_sha256"], ext, own))
    return specs, probs


def validate_all(specs: list, ignore=()) -> tuple:
    """({(round, task_id): result}, [problems]). Every answer file under an answers/ folder must belong to a task."""
    res, probs = {}, []
    ignored = set(ignore) | set(AUDIT_FAILED_IGNORED)
    for s in specs:
        r = validate_answer(s.batch, s.task_id, s.answer, s.payload)
        r["round"], r["name"], r["kind"] = s.round, s.label, s.kind
        if s.problems:
            r["ok"], r["answers"] = False, []
            r["problems"] += [f"task: {x}" for x in s.problems]
        r["audit_failed_ignored"] = s.answer.name in ignored or s.task_id in ignored or s.answer.stem in ignored
        if r["audit_failed_ignored"]:
            r["ok"], r["answers"] = False, []
            r["problems"].append("ignored: the file-access audit failed")
        res[(s.round, s.task_id)] = r
        if not r["ok"] and s.round in V1_ROUNDS:        # the v1 baseline cannot do without these files
            probs.append(f"{s.round} {s.task_id}: {'; '.join(r['problems'][:3])}")
    named = {s.answer.resolve() for s in specs}
    for d in ANSWER_DIRS:
        for p in sorted(d.glob("*.json")) if d.is_dir() else []:
            if p.resolve() not in named:
                probs.append(f"unmapped answer file {_rel(p)} (no task names it)")
    return res, probs


def _ok_answers(res: dict, rnd: str, task_id: str):
    r = res.get((rnd, task_id))
    return r["answers"] if r and r["ok"] else None


# ------------------------------------------------------------------------------------------------ v1 baseline
def _skin_from_json(d: dict) -> Skin:
    return Skin(skin_id=d["skin_id"], family=d["family"], text=d["text"], slots=tuple(tuple(x) for x in d["slots"]),
                kind=d["kind"], register=d["register"], escape=d["escape"],
                counts=tuple(tuple(x) for x in d["counts"]), author_mode=d["author_mode"], qform=d["qform"],
                brief=tuple(tuple(x) for x in d["brief"]), haiku_task_id=d["haiku_task_id"],
                haiku_prompt_sha=d["haiku_prompt_sha"], lexicon_ids=tuple(d["lexicon_ids"]),
                held_out=bool(d["held_out"]))


def v1_integrity() -> list:
    """Problems when a file of pools/ (freeze-v1) differs from the sha256 its own manifest.json recorded, or when pools/
    holds a file the manifest does not know."""
    man = _jload(POOLS_V1 / "manifest.json")
    probs = []
    for name, info in sorted(man["pool_files"].items()):
        p = POOLS_V1 / name
        if not p.is_file() or _sha(p.read_bytes()) != info["sha256"]:
            probs.append(f"pools/{name} differs from the freeze-v1 record")
    extra = sorted(p.name for p in POOLS_V1.iterdir() if p.is_file() and p.name not in man["pool_files"]
                   and p.name != "manifest.json")
    if extra:
        probs.append(f"pools/ holds files the freeze-v1 record does not list: {extra}")
    return probs


def rebuild_v1_texts() -> tuple:
    """({pool file: text}, [problems]): the v1 pools rebuilt in memory from the v1 answer files with the freeze_pools /
    extract_build code (unchanged), assembled the way freeze_pools.run writes them."""
    probs = list(FP.check_targets())
    res = EB.build_all()
    b_probs, _n, _t = FP.verify_build(res)
    probs += b_probs
    reg, lint = res["reg"], res["lint"]
    lex_rows, lp = FP.record_lex(res)
    probs += lp
    glex = {}
    for fid in sorted(reg.forms):
        f = reg.forms[fid]
        glex[fid] = {"qform": FP.QFORM_OF_SEM.get(f.sem_id), "text": f.text, "sem_id": f.sem_id,
                     "status": reg.status(fid), "unit_ok": f.unit_ok, "extractions": [list(e) for e in f.extractions],
                     "haiku_task_id": f.haiku_task_id, "haiku_prompt_sha": f.haiku_prompt_sha}
    g3_rep, g3_detail, gp = FP.g3h_stage(res)
    probs += gp
    g3_drop = set(g3_rep["drop_rows"])
    packs = sorted(lint["packs"], key=lambda p: p["pack_id"])
    skins = [lint["skins"][k] for k in sorted(lint["skins"])]
    freeform = [lint["free"][k] for k in sorted(lint["free"]) if k not in g3_drop]
    attacks = [lint["attacks"][k] for k in sorted(lint["attacks"])]
    wordings = [{"form_id": fid, "qform": glex[fid]["qform"], "text": glex[fid]["text"], "sem_id": glex[fid]["sem_id"],
                 "haiku_task_id": glex[fid]["haiku_task_id"], "haiku_prompt_sha": glex[fid]["haiku_prompt_sha"],
                 "extractions": glex[fid]["extractions"]}
                for fid in sorted(glex) if glex[fid]["status"] == "admitted"]
    pools = {
        "packs.json": packs, "skins.json": [asdict(s) for s in skins], "freeform.json": [asdict(s) for s in freeform],
        "attacks.json": [asdict(s) for s in attacks], "wordings.json": wordings, "lexicon.json": reg.to_json(),
        "quarantine.json": FP.quarantine_log(res, glex, g3_detail),
        "extraction_record.json": {"lex_reads": lex_rows, "g3h": g3_detail,
                                   "g3h_report": {k: g3_rep[k] for k in ("gate", "bar", "quarantined",
                                                                         "all_templates_pass")}}}
    return {n: _dump(o) for n, o in pools.items()}, probs


def load_v1() -> dict:
    """The frozen v1 inputs, parsed from pools/ (sha256 checked by v1_integrity)."""
    j = {n: _jload(POOLS_V1 / n) for n in POOL_FILES}
    return {"packs": j["packs.json"], "skins": [_skin_from_json(d) for d in j["skins.json"]],
            "freeform": [_skin_from_json(d) for d in j["freeform.json"]],
            "attacks": [_skin_from_json(d) for d in j["attacks.json"]], "wordings": j["wordings.json"],
            "lexicon": j["lexicon.json"], "quarantine": j["quarantine.json"], "extraction": j["extraction_record.json"],
            "manifest": _jload(POOLS_V1 / "manifest.json")}


# ------------------------------------------------------------------------------------------------ G-LEX and G3-H votes
def _meanings(reg: LexiconRegistry, kind: str) -> set:
    return {s.meaning for s in reg.sems.values() if s.kind == kind}


def record_votes(reg: LexiconRegistry, extractor: str, got: dict) -> dict:
    """reg.record_extraction for every answered form (got: {form id: {"meaning": text}}): the chosen meaning mapped to
    its sense; an unlisted text is a disagreement (sense None), never a default. A form not in the registry (dropped
    earlier) is skipped and counted. A form with no answer records nothing (it stays pending). Returns the counts."""
    c = Counter()
    for fid, a in sorted(got.items()):
        if fid not in reg.forms:
            c["form_not_in_registry"] += 1
            continue
        f = reg.forms[fid]
        m = a.get("meaning") if isinstance(a, dict) and set(a) == {"meaning"} else None
        if isinstance(m, str) and m in _meanings(reg, f.kind):
            outcome, sem = "listed", reg.meaning_to_sem(f.kind, m)
            if sem != f.sem_id:
                c["listed_other_sense"] += 1
        else:
            outcome, sem = "not_listed", None
        c[outcome] += 1
        reg.record_extraction(fid, extractor, sem)
    return dict(c)


def g3h_votes(batch: CH.TaskBatch, expected: dict, specs: list, res: dict) -> dict:
    """{item key: {"ok", "diffs", "read"}}: one exact read per Mode F narrative (g3h.compare, the v1 fields). A narrative
    with no valid answer (file rejected, ignored or item missing) is a mismatch ("no extraction"): it is dropped. The
    qid -> item map is the disk batch's key (what the agent read)."""
    fields = EB.g3h_fields()
    by_item = {}
    for s in specs:
        if s.round == "redo2-b" and s.kind == "extract_g3h" and s.batch.batch_id == batch.batch_id:
            for a in _ok_answers(res, s.round, s.task_id) or []:
                by_item[s.batch.key[a["qid"]]] = {k: v for k, v in a.items() if k != "qid"}
    out = {}
    for key in sorted(expected):
        a = by_item.get(key)
        ok, diffs = g3h.compare(expected[key], a, fields) if a is not None else (False, ["no extraction"])
        out[key] = {"ok": ok, "diffs": diffs, "read": a is not None}
    return out


# ------------------------------------------------------------------------------------------------ redo2 stage
def lint_redo2(batches: dict, raw: dict) -> dict:
    """The v1 loaders on every validated redo2 answer (build_redo2.lint_stage with the answers injected, not read from
    disk), in (cell, rank) order so a lower rank wins a repeat. One text set spans skins and Mode F."""
    names, texts, wtexts = BR.v1_seen()
    kept = {n: {} for n in POOL_OF}
    drops = {n: {} for n in POOL_OF}
    notes = []
    for name in ("packs", "skins", "freeform", "wordings"):
        b, plan = batches[name]
        ans, p2 = CH.load_answers(b, raw.get(name, {}))
        notes += [f"{name}: {x}" for x in p2]
        task_of = {iid: b.task_of[qid] for qid, iid in b.key.items()}
        for iid in sorted(plan, key=lambda i: (plan[i]["cell"], plan[i]["rank"])):
            a = ans.get(iid)
            if a is None:
                drops[name][iid] = ["no answer"]
                continue
            if name == "packs":
                obj, v = HA.check_pack(iid, a, plan[iid], names)
                if not v:
                    _k, d = EB.lint_packs([obj])
                    v = d[0]["reasons"] if d else []
            else:
                text = a.get("text") if isinstance(a, dict) else None
                check = {"skins": HA.check_skin, "freeform": HA.check_freeform, "wordings": HA.check_wording}[name]
                obj, v = check(iid, text, plan[iid], task_of[iid], b.prompt_sha,
                               wtexts if name == "wordings" else texts)
            if v:
                drops[name][iid] = list(v)
            else:
                kept[name][iid] = obj
    return {"kept": kept, "drops": drops, "notes": notes}


def select(cell_list: list, plans: dict, status_of) -> tuple:
    """G0 section 9: per cell the lowest-ranked candidates whose status is "pass" fill exactly `need`; the rest stay
    unused; a cell with fewer passing candidates stays short. -> ({pool: [iid]}, {"pool|cell": record})."""
    chosen, selection = {p: [] for p in POOL_OF}, {}
    for pool, lab, n in cell_list:
        plan = plans[pool]
        cand = sorted((i for i in plan if plan[i]["cell"] == f"{pool}|{lab}"), key=lambda i: plan[i]["rank"])
        st = {i: status_of(pool, i) for i in cand}
        pick = [i for i in cand if st[i] == "pass"][:n]
        chosen[pool] += pick
        selection[f"{pool}|{lab}"] = {"need": n, "chosen": pick, "short_after": n - len(pick),
                                      "candidates": [{"iid": i, "rank": plan[i]["rank"], "status": st[i],
                                                      "used": i in pick} for i in cand]}
    return chosen, selection


def redo2_stage(specs: list, res: dict, probs: dict) -> dict:
    """Everything the redo2 answers decide: lint, registry admission, both G-LEX reads, the G3-H read, the selection."""
    batches = BR.build_batches()                                   # the plan, rebuilt (new seed, ranks fixed before answers)
    need = BR.need_from_manifest()
    for s in specs:                                                # the loaders use the rebuilt batches: they must be the disk ones
        if s.round == "redo2-a":
            rb = batches[s.label][0]
            if rb.batch_id != s.batch.batch_id or rb.key != s.batch.key or rb.prompt_sha != s.batch.prompt_sha:
                probs["batches"].append(f"redo2 batch {s.label}: the rebuilt batch differs from the one on disk")
    raw = {n: {} for n in POOL_OF}
    for s in specs:
        if s.round != "redo2-a":
            continue
        got = _ok_answers(res, s.round, s.task_id)
        if got is None:
            probs["candidates"].append(f"{s.task_id}: authoring answer file rejected or missing; its items are unanswered")
        else:
            raw[s.label][s.task_id] = [dict(a) for a in got]
    lint = lint_redo2(batches, raw)
    reg, fid_of, admit_drops = BR.admit_stage(lint["kept"]["wordings"], batches["wordings"][1])
    iid_fid = {iid: fid for fid, iid in fid_of.items()}

    # G-LEX: two independent reads of every new form (own batches, own extractor ids; v1 reads stay as they are)
    reads, read_counts, picks = {}, {}, {}
    try:
        glex = BR.glex_batches(reg, sorted(fid_of))
    except ValueError as e:
        probs["reads"].append(f"G-LEX batches: {e}")
        glex = []
    for ext, b in glex:
        mine = [s for s in specs if s.round == "redo2-b" and s.kind == "extract_lex" and s.extractor == ext]
        if not mine or {s.batch.batch_id for s in mine} != {b.batch_id} or mine[0].batch.key != b.key:
            probs["reads"].append(f"G-LEX read {ext}: the rebuilt batch {b.batch_id} is not the one on disk")
        got = {}
        for s in mine:
            a_ = _ok_answers(res, s.round, s.task_id)
            if a_ is None:
                probs["reads"].append(f"{s.task_id}: read rejected (answer file invalid, ignored or missing); "
                                      f"its forms get no vote from {ext}")
                continue
            got.update({s.batch.key[a["qid"]]: {"meaning": a["meaning"]} for a in a_})
        read_counts[ext] = record_votes(reg, ext, got) | {"unanswered": len(set(b.key.values()) - set(got))}
        picks.update({(fid, ext): a["meaning"] for fid, a in got.items()})
    for fid in sorted(fid_of):
        reads[fid] = [list(e) for e in reg.forms[fid].extractions]

    # G3-H: one read of every kept new Mode F narrative
    g3b, g3_expected = BR.g3h_stage(lint["kept"]["freeform"], batches["freeform"][1])
    g3 = {}
    if g3b is not None:
        mine = [s for s in specs if s.round == "redo2-b" and s.kind == "extract_g3h"]
        if not mine or {s.batch.batch_id for s in mine} != {g3b.batch_id} or mine[0].batch.key != g3b.key:
            probs["reads"].append(f"G3-H read: the rebuilt batch {g3b.batch_id} is not the one on disk")
        disk_exp = REDO2 / "key" / "g3h_expected_redo2.json"
        if disk_exp.is_file() and _jload(disk_exp) != g3_expected:
            probs["reads"].append("key/g3h_expected_redo2.json differs from the rebuilt expectation")
        g3 = g3h_votes(g3b, g3_expected, specs, res)

    def status(pool: str, iid: str) -> str:
        if iid in lint["drops"][pool]:
            return "lint: " + "; ".join(lint["drops"][pool][iid][:3])
        if pool == "wordings":
            if iid in admit_drops:
                return "G-LEX registry: " + "; ".join(admit_drops[iid])
            st = reg.status(iid_fid[iid])
            return "pass" if st == "admitted" else f"G-LEX {st}"
        if pool == "freeform":
            d = g3.get(f"g3h|{lint['kept']['freeform'][iid].skin_id}")
            return "pass" if d and d["ok"] else "G3-H: " + "; ".join((d or {"diffs": ["no read"]})["diffs"][:3])
        return "pass"

    plans = {n: batches[n][1] for n in POOL_OF}
    chosen, selection = select(BR.cells(need), plans, status)
    return {"batches": batches, "need": need, "lint": lint, "reg": reg, "fid_of": fid_of, "admit_drops": admit_drops,
            "reads": reads, "read_counts": read_counts, "picks": picks, "g3": g3, "g3_expected": g3_expected,
            "chosen": chosen, "selection": selection, "plans": plans}


# ------------------------------------------------------------------------------------------------ the union
def canonical_registry(base_json: dict, chosen: list) -> LexiconRegistry:
    """The final registry: every v1 form (their v1 reads kept) plus the chosen redo2 forms, added in sorted form-id
    order, the order LexiconRegistry.from_json (the generator's loader) gives: the kit's scan() breaks ties between two
    forms that span the same text by insertion order, so a unit test only means something in a fixed order. Votes go
    through record_extraction (an extractor cannot vote twice for one form)."""
    forms = [dict(x) for x in base_json["forms"]]
    reads = {x["form_id"]: [tuple(e) for e in x["extractions"]] for x in forms}
    for c in chosen:
        fid = _form_id(c["sem"], c["text"])
        forms.append({"form_id": fid, "sem_id": c["sem"], "kind": "question", "text": c["text"], "slots": dict(c["slots"]),
                      "source": "haiku", "family": F, "haiku_task_id": c["tid"], "haiku_prompt_sha": c["psha"],
                      "held_out": False, "extractions": [], "unit_ok": None, "status": None})
        reads[fid] = [tuple(e) for e in c["extractions"]]
    for x in forms:
        x["extractions"] = []
    reg = LexiconRegistry.from_json(dict(base_json, forms=sorted(forms, key=lambda x: x["form_id"])))
    for fid in sorted(reads):
        for ext, sem in reads[fid]:
            reg.record_extraction(fid, ext, sem)
    return reg


def relint_union(packs: list, skins: list, free: list, attacks: list, wordings: list) -> list:
    """Every loader again over the union, one dedup set per pool family, each rebuilt object equal to the stored one."""
    probs = []
    seen_names = set()
    for pk in sorted(packs, key=lambda p: p["pack_id"]):
        obj, v = HA.check_pack(pk["pack_id"], {"pack": {"agreements": pk["agreements"], "parties": pk["parties"]}},
                               {"pack_id": pk["pack_id"], "held_out": pk["held_out"]}, seen_names)
        probs += [f"pack {pk['pack_id']}: {x}" for x in v]
        if obj is not None and obj != pk:
            probs.append(f"pack {pk['pack_id']}: differs from the rebuilt pack")
    _k, d = EB.lint_packs(packs)
    probs += [f"pack {x['id']}: {'; '.join(x['reasons'][:2])}" for x in d]
    if len({p["pack_id"] for p in packs}) != len(packs):
        probs.append("duplicate pack ids")
    seen = set()
    for pool, items, check, pre, cut in (
            ("skins", skins, HA.check_skin, "x.skin.", len("T21-SK-")),
            ("freeform", free, HA.check_freeform, "x.free.", len("T21-MF-")),
            ("attacks", attacks, HA.check_attack, "x.attack.", len("T21-AT-"))):
        ids = [s.skin_id for s in items]
        if len(set(ids)) != len(ids):
            probs.append(f"{pool}: duplicate skin ids")
        for sk in sorted(items, key=lambda s: s.skin_id):
            iid = pre + sk.skin_id[cut:]
            meta = {"register": sk.register, "held_out": sk.held_out, "facts": dict(sk.brief)}
            obj, v = check(iid, sk.text, meta, sk.haiku_task_id, sk.haiku_prompt_sha, seen)
            probs += [f"{pool} {sk.skin_id}: {x}" for x in v]
            if obj is not None and asdict(obj) != asdict(sk):
                probs.append(f"{pool} {sk.skin_id}: differs from the rebuilt skin")
    seen_w = set()
    for w in sorted(wordings, key=lambda w: w["form_id"]):
        obj, v = HA.check_wording(w["form_id"], w["text"], {"qform": w["qform"]}, w["haiku_task_id"],
                                  w["haiku_prompt_sha"], seen_w)
        probs += [f"wording {w['form_id']}: {x}" for x in v]
        if obj is not None and obj != (w["qform"], w["text"], w["haiku_task_id"], w["haiku_prompt_sha"]):
            probs.append(f"wording {w['form_id']}: differs from the rebuilt wording")
    return probs


# ------------------------------------------------------------------------------------------------ the build
def _tree_sha(root: Path) -> dict:
    return {p.relative_to(root).as_posix(): _sha(p.read_bytes()) for p in sorted(Path(root).rglob("*"))
            if p.is_file() and "__pycache__" not in p.parts}


def build(ignore=(), smoke_seeds: int = 3) -> dict:
    """The whole freeze-v2 in memory: {"files": {name: text}, "manifest": dict, "verdict", "shortfalls", "problems"}."""
    g0_sha = _sha(G0_AT_FREEZE.read_bytes())
    if g0_sha != G0_AT_FREEZE_SHA256:
        raise SystemExit("G0_SPEC_v1.2.md (the G0 the pools were frozen under) is not the archived v1.2")
    if _sha(G0.read_bytes()) != P.T21Plugin.G0_SHA256:
        raise SystemExit("G0_SPEC.md does not match the plugin pin")
    probs = {"v1_integrity": v1_integrity(), "batches": [], "answers": [], "rebuild": [], "candidates": [],
             "reads": [], "registry": [], "union": [], "smoke": []}

    # 1. answer contract, all rounds
    specs, bprobs = collect_tasks()
    probs["batches"] += bprobs
    res, aprobs = validate_all(specs, ignore)
    probs["answers"] += aprobs

    # 2. v1 baseline and its byte-for-byte reproduction of pools/
    v1 = load_v1()
    texts_v1, rprobs = rebuild_v1_texts()
    probs["rebuild"] += rprobs
    v1_repro = {n: (POOLS_V1 / n).read_text(encoding="utf-8") == t for n, t in sorted(texts_v1.items())}
    probs["v1_integrity"] += [f"the v1 rebuild no longer reproduces pools/{n}" for n, ok in v1_repro.items() if not ok]

    # 3-5. redo2: loaders, registry, reads, selection
    st = redo2_stage(specs, res, probs)
    chosen, lint, reg2 = st["chosen"], st["lint"], st["reg"]
    kept = lint["kept"]

    # 6. the union
    v1_ids = {"packs": {p["pack_id"] for p in v1["packs"]},
              "skins": {s.skin_id for s in v1["skins"]}, "freeform": {s.skin_id for s in v1["freeform"]}}
    new_packs = sorted((kept["packs"][i] for i in chosen["packs"]), key=lambda p: p["pack_id"])
    new_skins = sorted((kept["skins"][i] for i in chosen["skins"]), key=lambda s: s.skin_id)
    new_free = sorted((kept["freeform"][i] for i in chosen["freeform"]), key=lambda s: s.skin_id)
    for pool, objs, key in (("packs", new_packs, "pack_id"), ("skins", new_skins, "skin_id"),
                            ("freeform", new_free, "skin_id")):
        for o in objs:
            oid = o[key] if isinstance(o, dict) else getattr(o, key)
            if oid in v1_ids[pool]:
                probs["union"].append(f"{pool}: redo2 id {oid} collides with a v1 id")
    packs = sorted(v1["packs"] + new_packs, key=lambda p: p["pack_id"])
    skins = sorted(v1["skins"] + new_skins, key=lambda s: s.skin_id)
    free = sorted(v1["freeform"] + new_free, key=lambda s: s.skin_id)
    attacks = list(v1["attacks"])

    plan_w = st["plans"]["wordings"]
    iid_fid = {iid: fid for fid, iid in st["fid_of"].items()}
    chosen_forms = []
    for iid in sorted(chosen["wordings"], key=lambda i: (plan_w[i]["cell"], plan_w[i]["rank"])):
        q, text, tid, psha = kept["wordings"][iid]
        fid = iid_fid[iid]
        chosen_forms.append({"iid": iid, "qform": q, "sem": question_sem(F, q), "text": text, "slots": EB._slots_for(text),
                             "tid": tid, "psha": psha, "extractions": [tuple(e) for e in reg2.forms[fid].extractions]})
    reg = canonical_registry(v1["lexicon"], chosen_forms)
    rt = LexiconRegistry.from_json(reg.to_json())              # what the generator's loader will see
    for fid, f in reg.forms.items():
        if not f.unit_ok:
            probs["registry"].append(f"{fid}: unit test fails in the final registry ({'; '.join(f.unit_problems[:2])})")
        if rt.forms[fid].unit_ok != f.unit_ok or rt.forms[fid].extractions != f.extractions:
            probs["registry"].append(f"{fid}: differs after a to_json / from_json round trip")
    wordings = [dict(w) for w in v1["wordings"]]
    for c in chosen_forms:
        fid = _form_id(c["sem"], c["text"])
        f = reg.forms[fid]
        wordings.append({"form_id": fid, "qform": c["qform"], "text": c["text"], "sem_id": c["sem"],
                         "haiku_task_id": c["tid"], "haiku_prompt_sha": c["psha"],
                         "extractions": [list(e) for e in f.extractions]})
    wordings = sorted(wordings, key=lambda w: w["form_id"])
    used = [w["form_id"] for w in wordings]
    if sorted(reg.forms) != sorted(used):
        probs["registry"].append(f"registry holds {len(reg.forms)} forms, wordings.json lists {len(used)}")
    gate_used, gate_all = reg.gate(used_form_ids=used), reg.gate()
    kit = {"strict_kinds_in_registry": sorted({f.kind for f in reg.forms.values()} & set(STRICT_KINDS)),
           "required_reads": dict(sorted(Counter(f.required for f in reg.forms.values()).items())),
           "admitted_with_fewer_distinct_reads": [fid for fid in used if len({e for e, _ in reg.forms[fid].extractions})
                                                  < reg.forms[fid].required],
           "admitted_not_all_agreeing": [fid for fid in used if any(s != reg.forms[fid].sem_id
                                                                     for _, s in reg.forms[fid].extractions)],
           "admitted_unit_failing": [fid for fid in used if not reg.forms[fid].unit_ok],
           "new_forms_distinct_reads": {c["iid"]: sorted({e for e, _ in c["extractions"]}) for c in chosen_forms}}

    probs["union"] += relint_union(packs, skins, free, attacks, wordings)
    # G3-H over the union: the v1 reads (frozen) and every redo2 read (all 15 are recorded; only the chosen ones are used)
    g3_all = {k: dict(v) for k, v in v1["extraction"]["g3h"].items()}
    g3_all.update({k.split("|", 1)[1]: {"ok": d["ok"], "diffs": d["diffs"], "round": "redo2"}
                   for k, d in st["g3"].items()})
    in_pool = {s.skin_id for s in free}
    unread = sorted(sid for sid in in_pool if not g3_all.get(sid, {}).get("ok"))
    if unread:
        probs["union"].append(f"Mode F narratives without an ok G3-H read: {unread}")
    g3_rep = g3h.template_report([(sid, sid, d["ok"]) for sid, d in sorted(g3_all.items()) if sid in in_pool])

    lines = FP.tally(packs, skins, free, attacks, wordings)
    short = [x for x in lines if x["shortfall"]]
    shortfalls = [f"{x['kind']}|{x['label']}: {x['admitted']}/{x['target']} (short {x['shortfall']})" for x in short]
    for k, v in kit.items():
        if k.startswith("admitted_") and v:
            shortfalls.append(f"G-LEX kit rule: {k}: {len(v)} form(s)")
    if kit["strict_kinds_in_registry"]:
        shortfalls.append(f"unexpected precedence / window forms in the T21 registry: {kit['strict_kinds_in_registry']}")
    if not gate_used["pass"]:
        shortfalls.append(f"G-LEX does not pass on the used forms: {gate_used['not_admitted']}")
    if not g3_rep["all_templates_pass"]:
        shortfalls.append(f"G3-H quarantines templates: {g3_rep['quarantined']}")

    # 7. quarantine, provenance, files
    quarantine = [dict(r, round="v1") for r in v1["quarantine"]]
    for pool in POOL_OF:
        for iid, why in sorted(lint["drops"][pool].items()):
            quarantine.append({"stage": "lint", "pool": pool, "id": iid, "reasons": why, "round": "redo2"})
    for iid, why in sorted(st["admit_drops"].items()):
        quarantine.append({"stage": "G-LEX registry", "pool": "wordings", "id": iid, "reasons": why, "round": "redo2"})
    for fid, iid in sorted(st["fid_of"].items()):
        if reg2.status(fid) != "admitted":
            quarantine.append({"stage": "G-LEX", "pool": "wordings", "id": iid, "form_id": fid, "status": reg2.status(fid),
                               "reads": st["reads"].get(fid, []), "round": "redo2"})
    for key, d in sorted(st["g3"].items()):
        if not d["ok"]:
            quarantine.append({"stage": "G3-H", "pool": "freeform", "id": key.split("|", 1)[1], "reasons": d["diffs"],
                               "round": "redo2"})
    for (rnd, tid), r in sorted(res.items()):
        if not r["ok"]:
            quarantine.append({"stage": "answer-contract", "pool": "answers", "id": f"{rnd}|{tid}",
                               "reasons": r["problems"][:3], "round": rnd})
    quarantine = sorted(quarantine, key=lambda r: (r["round"], r["stage"], r["pool"], str(r["id"])))

    def piece_of(pool: str, iid: str) -> dict:
        o = kept[pool][iid]
        if pool == "packs":
            return {"piece": o["pack_id"], "task_id": None}
        if pool == "wordings":
            return {"piece": _form_id(question_sem(F, o[0]), o[1]), "task_id": o[2]}
        return {"piece": o.skin_id, "task_id": o.haiku_task_id}

    provenance = {
        "family": F, "version": VERSION, "rule": "G0_SPEC.md v1.2 section 9",
        "need": {f"{p}|{l}": n for (p, l), n in sorted(st["need"].items())}, "selection": st["selection"],
        "chosen": {pool: {iid: piece_of(pool, iid) for iid in sorted(chosen[pool])} for pool in POOL_OF},
        "answer_file_sha256": {tid: r["sha256"] for (rnd, tid), r in sorted(res.items()) if rnd.startswith("redo2")},
        "g3h_redo2_reads": st["g3"], "glex_redo2_reads": st["reads"], "glex_redo2_read_counts": st["read_counts"],
        "unused_but_passing": {k: [c["iid"] for c in v["candidates"] if c["status"] == "pass" and not c["used"]]
                               for k, v in sorted(st["selection"].items())}}
    new_reads = [{"form_id": fid, "extractor_id": e, "meaning": st["picks"].get((fid, e)), "sem_id": s, "note": "",
                  "round": "redo2"}
                 for c in chosen_forms for fid in [_form_id(c["sem"], c["text"])] for e, s in c["extractions"]]
    ext_rec = {"lex_reads": v1["extraction"]["lex_reads"] + new_reads, "g3h": g3_all,
               "g3h_report": {k: g3_rep[k] for k in ("gate", "bar", "quarantined", "all_templates_pass")}}
    files = {"packs.json": _dump(packs), "skins.json": _dump([asdict(s) for s in skins]),
             "freeform.json": _dump([asdict(s) for s in free]), "attacks.json": _dump([asdict(s) for s in attacks]),
             "wordings.json": _dump(wordings), "lexicon.json": _dump(reg.to_json()),
             "quarantine.json": _dump(quarantine), "extraction_record.json": _dump(ext_rec),
             "provenance.json": _dump(provenance)}

    # 8. smoke: the plugin runs on these pools
    pools = pools_from_texts(dict(files, **{"MANIFEST.json": _dump({"sha256": {n: _sha(t) for n, t in files.items()}})}))
    if smoke_seeds:
        try:
            smoke_rep = smoke(pools, smoke_seeds)
        except Exception as e:  # noqa: BLE001
            smoke_rep = {"failed": f"{type(e).__name__}: {str(e)[:200]}"}
            probs["smoke"].append(smoke_rep["failed"])
    else:
        smoke_rep = {"skipped": True}

    problem_list = [f"{k}: {p}" for k, ps in probs.items() for p in ps]
    ready = not shortfalls and not problem_list and gate_used["pass"]
    answers_rep = [{k: v for k, v in r.items() if k != "answers"} for _, r in sorted(res.items())]
    rounds = Counter((r["round"], r["ok"]) for r in answers_rep)
    counts = {
        "chosen": {k: len(v) for k, v in chosen.items()},
        "redo2_candidates": {k: len(v[1]) for k, v in st["batches"].items()},
        "redo2_lint_drops": {k: len(v) for k, v in lint["drops"].items()},
        "redo2_admit_drops": len(st["admit_drops"]),
        "redo2_glex_status": dict(Counter(reg2.status(f) for f in st["fid_of"])),
        "redo2_g3h": {"items": len(st["g3"]), "ok": sum(d["ok"] for d in st["g3"].values())},
        "packs": {"total": len(packs), "train": sum(1 for p in packs if not p["held_out"]),
                  "held_out": sum(1 for p in packs if p["held_out"])},
        "skins_by_register": dict(sorted(Counter(f"{s.register}|{'held' if s.held_out else 'train'}"
                                                 for s in skins).items())),
        "freeform_by_register": dict(sorted(Counter(s.register for s in free).items())),
        "attacks": len(attacks),
        "wordings_by_qform": dict(sorted(Counter(w["qform"] for w in wordings).items())),
        "lexicon_forms": len(reg.forms), "lexicon_status": dict(Counter(reg.status(f) for f in reg.forms)),
    }
    man = {
        "family": F, "version": VERSION, "build": "transfer/T21/freeze_v2.py -> pools_v2/",
        "transfer_dev_only": True, "trained": False, "rows_generated": False,
        "status": ("FROZEN: every G0 minimum met and G-LEX passes on every used form (2/2 distinct reads); G13-seed "
                   "(6.4 step 4) still pending" if ready else
                   "FROZEN WITH SHORTFALLS: see shortfalls and problems; the pools are not complete to the G0 "
                   "minimums, and G13-seed (6.4 step 4) has not run"),
        "verdict": "READY" if ready else "SHORT",
        "supersedes": "none; freeze-v1 (pools/) is left byte-for-byte unchanged on disk",
        "g0": {"path": "c2_build/transfer/T21/G0_SPEC.md", "sha256": g0_sha, "matches_plugin_pin": True},
        "rulings": "G0_SPEC.md v1.2 section 9: per cell the lowest-ranked redo2 candidates that pass every gate fill "
                   "exactly the shortfall; v1 reads, admissions and rejections stay final; no target lowered",
        "v1": {"manifest_sha256": _sha((POOLS_V1 / "manifest.json").read_bytes()),
               "pool_sha256": {n: i["sha256"] for n, i in sorted(v1["manifest"]["pool_files"].items())},
               "reproduced_by_rebuild": v1_repro},
        "answer_files": {"by_round": {f"{r}|{'ok' if ok else 'rejected'}": n for (r, ok), n in sorted(rounds.items())},
                         "audit_failed_ignored": sorted(set(ignore) | set(AUDIT_FAILED_IGNORED)),
                         "audit": "file-access audit not re-run here: no agent transcripts in this step",
                         "files": answers_rep},
        "redo2": {"plan_need": {f"{p}|{l}": n for (p, l), n in sorted(st["need"].items())},
                  "selection": {k: {"need": v["need"], "chosen": v["chosen"], "short_after": v["short_after"]}
                                for k, v in st["selection"].items()},
                  "notes": lint["notes"]},
        "gates": {"G-LEX_used_forms": {k: v for k, v in gate_used.items() if k != "not_admitted"},
                  "G-LEX_all_forms": {k: v for k, v in gate_all.items() if k != "not_admitted"},
                  "G-LEX_kit_rules": kit,
                  "G-SL": "applied at load by role (skins, Mode F, attacks, wordings) and by lint_values (names, packs); "
                          "re-applied to the union with cross-pool dedup",
                  "G3-H": {k: g3_rep[k] for k in ("gate", "bar", "quarantined", "all_templates_pass")} |
                          {"items": len(g3_all), "ok": sum(d["ok"] for d in g3_all.values())},
                  "round_trip": "fill / parse_skin on every skin; to_json / from_json on the registry",
                  "plugin_smoke": smoke_rep, "audit": "not re-run (no agent transcripts)", "G13_seed": "not run (6.4 step 4)"},
        "problems": probs, "tally": lines, "shortfalls": shortfalls, "targets_g0": TARGET, "counts": counts,
        "quarantined": len(quarantine),
        "load_recipe": "from transfer.T21 import freeze_v2 as FV; pools = FV.load_pools(); plugin = FV.make_plugin(pools); "
                       "ctx = FV.make_ctx(pools). T21Plugin reads no pool path (constructor arguments only). g13_c2.py "
                       "reads <family dir>/pools only and does not see pools_v2/.",
        "sha256": {n: _sha(t) for n, t in sorted(files.items())},
        "note_manifest": "sha256 of every other file in pools_v2/ (this file is not hashed)",
    }
    files["MANIFEST.json"] = _dump(man)
    man = json.loads(files["MANIFEST.json"])
    return {"files": files, "manifest": man, "verdict": man["verdict"], "ready": ready, "shortfalls": shortfalls,
            "problems": problem_list, "tally": lines, "counts": counts, "state": st}


# ------------------------------------------------------------------------------------------------ freeze and report
def freeze(out: dict, root: Path = POOLS_V2) -> list:
    if (Path(root) / "MANIFEST.json").exists():
        raise SystemExit("pools_v2/MANIFEST.json already exists: refusing to re-freeze")
    problems = v1_integrity()
    if problems:
        raise SystemExit("pools/ differs from freeze-v1 before writing: " + "; ".join(problems))
    before = _tree_sha(POOLS_V1)
    rest = {n: t for n, t in out["files"].items() if n != "MANIFEST.json"}
    written = paths.write_files(root, rest)                          # the MANIFEST last: no half-frozen folder has one
    written += paths.write_files(root, {"MANIFEST.json": out["files"]["MANIFEST.json"]})
    if before != _tree_sha(POOLS_V1) or v1_integrity():
        raise SystemExit("pools/ changed while freezing (it must stay untouched)")
    return [str(p) for p in written]


def report(out: dict) -> dict:
    man = out["manifest"]
    return {"verdict": man["verdict"], "status": man["status"], "shortfalls": out["shortfalls"],
            "problems": out["problems"], "answer_files": man["answer_files"]["by_round"],
            "audit_failed_ignored": man["answer_files"]["audit_failed_ignored"],
            "redo2_selection": man["redo2"]["selection"], "counts": man["counts"],
            "tally_shortfalls": [x for x in out["tally"] if x["shortfall"]],
            "gates": {"G-LEX_used_forms": man["gates"]["G-LEX_used_forms"],
                      "G-LEX_kit_rules": man["gates"]["G-LEX_kit_rules"], "G3-H": man["gates"]["G3-H"],
                      "plugin_smoke": man["gates"]["plugin_smoke"]},
            "quarantined": man["quarantined"]}


# ------------------------------------------------------------------------------------------------ loading pools_v2
@dataclass
class Pools:
    lexicon: LexiconRegistry
    packs: list
    skins: dict
    wordings: list
    manifest: dict = field(default_factory=dict)


def pools_from_texts(texts: dict, *, check_sha: bool = True) -> Pools:
    """Pools from {file name: text} (what freeze writes). check_sha: every file against MANIFEST.json."""
    man = json.loads(texts["MANIFEST.json"])
    if check_sha:
        for n, sha in man["sha256"].items():
            if _sha(texts[n]) != sha:
                raise ValueError(f"pools_v2/{n} differs from MANIFEST.json")
    lex = LexiconRegistry.from_json(json.loads(texts["lexicon.json"]))
    packs = json.loads(texts["packs.json"])
    skins = {d["skin_id"]: _skin_from_json(d) for k in ("skins.json", "freeform.json", "attacks.json")
             for d in json.loads(texts[k])}
    return Pools(lex, packs, skins, json.loads(texts["wordings.json"]), man)


def load_pools(root: Path = POOLS_V2) -> Pools:
    root = Path(root)
    return pools_from_texts({p.name: p.read_text(encoding="utf-8") for p in sorted(root.glob("*.json"))})


def make_plugin(pools: Pools):
    return P.T21Plugin(lexicon=pools.lexicon, packs=pools.packs)


QUARANTINE_I1 = HERE / "quarantine_i1.json"


def load_quarantine(path: Path = QUARANTINE_I1) -> dict:
    """{piece id: record} of the post-freeze quarantine (PILOT_VERDICT FIX-1): wordings and skins the generator never
    offers. pools_v2/ is sha-pinned and stays as frozen; this file is the only place the later quarantine lives."""
    rec = json.loads(Path(path).read_text(encoding="utf-8"))
    if rec.get("family") != F or not isinstance(rec.get("items"), list):
        raise ValueError(f"{path}: not a T21 quarantine record")
    out = {}
    for it in rec["items"]:
        if not isinstance(it.get("id"), str) or it.get("pool") not in ("wordings", "skins", "freeform") \
                or not it.get("reason"):
            raise ValueError(f"{path}: malformed item {it!r}")
        if it["id"] in out:
            raise ValueError(f"{path}: duplicate id {it['id']}")
        out[it["id"]] = it
    return out


def make_ctx(pools: Pools, *, quarantine: bool = True) -> KitCtx:
    """Mode T skins, Mode F narratives, attack lines and the ADMITTED wordings (each wording skin points at its form),
    minus the post-freeze quarantine record (quarantine_i1.json; quarantine=False gives the frozen pools as written).
    A quarantined id that is not in the pools is an error (the record must name real pieces)."""
    skins = dict(pools.skins)
    for w in pools.wordings:
        if pools.lexicon.status(w["form_id"]) != "admitted":
            raise ValueError(f"wording {w['form_id']} is not an admitted form")
        sid = f"T21-WD-{w['qform']}-{w['form_id'].split('#')[1]}"
        skins[sid] = make_skin(sid, F, w["text"], EB._slots_for(w["text"]), kind="wording", register="question",
                               qform=w["qform"], lexicon_ids=(w["form_id"],), haiku_task_id=w["haiku_task_id"],
                               haiku_prompt_sha=w["haiku_prompt_sha"])
    if quarantine:
        q = load_quarantine()
        missing = sorted(i for i in q if i not in skins)
        if missing:
            raise ValueError(f"quarantine_i1.json names pieces that are not in the pools: {missing}")
        skins = {k: v for k, v in skins.items() if k not in q}
    return KitCtx(skins=skins, lexicon=pools.lexicon)


def smoke(pools: Pools, seeds: int = 6) -> dict:
    """Every program gate (G2, G3, G4, G-SL, G-LEX, G-TW, schema) on a few units per sampler with these pools; the
    G15 loader check is left to the plugin's own suite. Nothing is written."""
    from c2_kit import pipeline
    pl, ctx, n, bad = make_plugin(pools), make_ctx(pools), 0, []
    for smp in pl.SAMPLERS:
        for seed in range(seeds):
            u = pipeline.build_unit(pl, pl.sample(seed, smp), ctx, run_g15=False)
            n += 1
            if not u.ok:
                bad.append(f"{smp}/{seed}: {u.problems[:2]}")
    if bad:
        raise AssertionError("; ".join(bad[:3]))
    return {"units": n, "samplers": list(pl.SAMPLERS), "ok": True}


# ------------------------------------------------------------------------------------------------ CLI
def main(argv: list) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=("check", "freeze", "validate", "smoke"), nargs="?", default="check")
    ap.add_argument("--ignore", nargs="*", default=[], metavar="TASK_ID",
                    help="tasks whose file-access audit failed: their answer files are ignored")
    a = ap.parse_args(argv[1:])
    if a.cmd == "validate":
        specs, bp = collect_tasks()
        res, ap_ = validate_all(specs, a.ignore)
        print(json.dumps({"batch_problems": bp, "problems": ap_,
                          "files": [{k: v for k, v in r.items() if k != "answers"} for _, r in sorted(res.items())]},
                         indent=1, ensure_ascii=False))
        return 0 if not bp and not ap_ and all(r["ok"] for r in res.values()) else 1
    if a.cmd == "smoke":
        print(json.dumps(smoke(load_pools()), indent=1))
        return 0
    out = build(a.ignore)
    rep = report(out)
    if a.cmd == "freeze":
        rep["written"] = [Path(p).name for p in freeze(out)]
    print(json.dumps(rep, indent=1, ensure_ascii=False, default=str))
    return 0 if out["ready"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))

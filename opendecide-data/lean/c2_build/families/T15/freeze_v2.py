"""families/T15/freeze_v2.py: the T15 pool freeze-v2 (C2_DATA_SPEC 6.2 item 2 and 6.4 steps 3-4; G0_SPEC.md v1.2 sections
2, 3 and 6, rulings R1-R4). It folds every validated redo answer into the frozen v1 inputs and writes pools_v2/.

Why a new script. glex_admit.py freeze refuses while pools/MANIFEST.json exists (by design), and it reads only
haiku/author/answers and haiku/extract/answers: no loader reads haiku/redo or haiku/redo2. Folding one extra form into
its G-LEX form list would also change both v1 extraction batches (glex_admit.rebuild_reads compares them byte for byte),
so v1 forms keep their v1 reads untouched (R1: "v1 reads, admissions and rejections stay final") and every form
authored or re-entered after freeze-v1 gets its OWN two independent reads. Nothing in pools/ (freeze-v1) or in
pools/redo2/ (the interim supplement: v1 + the redo-v1 skin / attack answers) is rewritten.

  check     in memory: validate every answer file, rebuild freeze-v2, print counts / shortfalls / verdict. Writes nothing.
  freeze    the same, then write families/T15/pools_v2/ (skins, attacks, wordings, comparators, lexicon, packs, names,
            documents, provenance, QUARANTINE, MANIFEST) through paths.write_files. Refuses when pools_v2/MANIFEST.json
            exists, and refuses (before and after writing) when any file of pools/ differs from freeze-v1's record.
  validate  only the answer-file contract report (all rounds)
  smoke     drive T15Plugin with the pools of pools_v2/ (A == B on a few seeds per sampler); writes nothing

Run from lean/:  ../.venv/bin/python c2_build/families/T15/freeze_v2.py check|freeze|validate|smoke

What it does, in order
  1. Answer contract (all rounds: author-v1 19 files, extract-v1 10, redo-v1 8, redo2-a 4, r2b 0 or more when
     REDO2B_INDEX.json exists). Per file: the batch is read back from disk (manifest, key, chunks, prompt: sha256 of the
     prompt and of every chunk, and every opaque qid re-derived from its internal id, as chunker.make_batch derives them),
     then the answer file must be ONE JSON list (no wrapper, no text around it), every object holding exactly the keys
     {qid, <payload>}, every expected qid exactly once, no unknown qid, a non-empty payload. An invalid file is
     rejected whole: its items count as unanswered, never repaired and never edited. A file that no task names is a
     problem. Audits: no agent transcripts exist here, so the file-access audit is not re-run; the orchestrator's list of
     audit failures is an input (AUDIT_FAILED_IGNORED) and any file on it is ignored.
  2. v1 baseline: glex_admit.admit() (the v1 loaders, unit tests, byte-for-byte rebuild of both v1 extraction batches,
     v1 reads A / B) and a check that it still reproduces every file of pools/ byte for byte.
  3. Skins and attack lines: the redo-v1 answers replace ONLY the qids they list in the original answer (the merge
     procedure of REDO_INDEX.json), then the family loaders check_skin / check_attack run in the loader's own order.
  4. Wordings and comparators (R1-R3): v1 candidates stay as they are. Added candidates, in a fixed order: the v1 load
     rejects that re-enter under R2 (a Haiku text equal to a fixtures.py text), then the redo2 wordings, then the redo2
     comparators, each checked with the v1 loader (R2: "duplicate or fixture copy" counts only for a duplicate of a pool
     candidate), then added to the FULL v1 registry (every v1 form, admitted or not): a form must pass its unit test
     and break no other form's, else it is dropped.
  5. G-LEX (c2_kit/lexicon.py): votes are recorded per extractor with LexiconRegistry.record_extraction. A form is
     admitted when its unit test passes and >= 2 distinct extractors (3 for kinds "precedence" and "window"; T15 has
     none, asserted) all picked its declared sense; any other pick, NONE or an unlisted text rejects it for good. A form
     with fewer reads stays "pending" and is never used (wordings.json / comparators.json hold admitted forms only).
     Read stages: v1 (read-A, read-B), r2a (read-r2a-A / -B: the re-entered forms), r2b (read-r2b-A / -B: the new
     redo2 forms; picked up from haiku/redo2/REDO2B_INDEX.json + plan/glex_reads_r2b.json when they exist).
  6. G3-H: T15 is Mode T only (G0 S19, documents_mode_f 0): no free-text document, so there is no G3-H vote to record.
  7. Counts and shortfalls are glex_admit.counts / glex_admit.shortfalls against glex_admit.G0_TARGETS (never lowered),
     plus two derived requirements (an admitted held-out wording per question form for S5; every used form has its
     required distinct reads). READY = no shortfall, no problem, G-LEX passes on the used forms.

How the generator loads pools_v2/  (T15Plugin reads no pool path: its constructor takes the pools, so no plugin edit)
    from families.T15 import freeze_v2 as FV
    pools  = FV.load_pools()            # pools_v2/, files checked against MANIFEST.json sha256
    plugin = FV.make_plugin(pools)      # T15Plugin(lexicon=pools.lexicon, packs=pools.packs, names=pools.names)
    ctx    = FV.make_ctx(pools)         # KitCtx(case-note skins + attack lines + admitted wordings, lexicon)
c2_build/g13_c2.py seeds from families/T15/pools/** only (rglob), so it does not see pools_v2/ until the lead points it
there (that file is pinned; this script does not edit it).

Haiku answers only flag. No label or gold is set or read here, and no answer file is ever edited.
"""
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
_C2_BUILD = HERE.parents[1]
if str(_C2_BUILD) not in sys.path:
    sys.path.insert(0, str(_C2_BUILD))

from c2_kit import chunker as CH  # noqa: E402
from c2_kit import paths  # noqa: E402
from c2_kit.lexicon import STRICT_KINDS, LexiconError, LexiconRegistry, question_sem  # noqa: E402
from c2_kit.plugin import KitCtx  # noqa: E402
from c2_kit.skin import Skin, make_skin  # noqa: E402
from families.T15 import glex_admit as GA  # noqa: E402
from families.T15 import haiku_author as HA  # noqa: E402
from families.T15 import plugin as P  # noqa: E402

F = "T15"
VERSION = "freeze-v2"
HAIKU = HERE / "haiku"
POOLS_V1 = HERE / "pools"
POOLS_INTERIM = POOLS_V1 / "redo2"
POOLS_V2 = HERE / "pools_v2"
G0 = HERE / "G0_SPEC.md"
R2_INDEX = HAIKU / "redo2" / "REDO2_INDEX.json"
R2B_INDEX = HAIKU / "redo2" / "REDO2B_INDEX.json"
DUP = "duplicate or fixture copy"
CMP_FIXTURES = frozenset(t for _, t, _ in HA.FX.COMPARATORS)
QFIXTURES = frozenset(HA.QSTRINGS)
# Answer files the orchestrator reports as failing the file-access audit ("their file-access audit failed: []").
AUDIT_FAILED_IGNORED: tuple = ()
PAYLOAD = {"packs": "pack", "names": "names"}            # every other author pool answers {qid, text}


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
    return GA._dump(o)


def _bad_constant(name):
    raise ValueError(f"JSON constant {name} is not allowed")


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
def validate_answer(batch: CH.TaskBatch, task_id: str, path: Path, payload: str, expected=None) -> dict:
    """The answer-file contract (task files, "Answer contract (exact)"). Reads the file; never writes. Result:
    {file, task_id, sha256, ok, n, problems, answers}; `answers` is the list of objects when ok, else []."""
    path = Path(path)
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
        if not isinstance(a, dict) or set(a) != {"qid", payload}:
            probs.append(f"object {i}: keys must be exactly qid and {payload}")
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
        v = a[payload]
        ok = ((payload in ("text", "meaning") and isinstance(v, str) and v.strip() != "")
              or (payload == "pack" and isinstance(v, dict) and v)
              or (payload == "names" and isinstance(v, list) and v
                  and all(isinstance(x, str) and x.strip() for x in v)))
        if not ok:
            probs.append(f"qid {q}: {payload} is empty or of the wrong type")
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
    name: str                      # pool name (author), read name (A / B / r2a-A ...), or redo pool
    kind: str
    payload: str
    answer: Path
    batch: CH.TaskBatch
    expected: set | None = None    # None = the whole chunk
    source_task: str | None = None  # redo-v1: the original chunk the redone qids belong to


def _tasks_of(root: Path, rnd: str, batch_cache: dict, probs: list, entries: list, name_key: str, payload_of) -> list:
    out = []
    for t in entries:
        bid = t["batch_id"]
        if (root, bid) not in batch_cache:
            batch_cache[(root, bid)] = load_disk_batch(root, bid)
            probs += batch_cache[(root, bid)][1]
        b = batch_cache[(root, bid)][0]
        out.append(TaskSpec(rnd, t["task_id"], t[name_key], b.kind, payload_of(t), root / "answers" /
                            f"{t['task_id']}.json", b))
    return out


def collect_tasks() -> tuple:
    """([TaskSpec], [problems]) for every round whose files exist on disk."""
    probs, cache, specs = [], {}, []
    a = HAIKU / "author"
    specs += _tasks_of(a, "author-v1", cache, probs, _jload(a / "TASKS.json")["tasks"], "batch",
                       lambda t: PAYLOAD.get(t["batch"], "text"))
    e = HAIKU / "extract"
    specs += _tasks_of(e, "extract-v1", cache, probs, _jload(e / "TASKS.json")["tasks"], "read", lambda t: "meaning")
    rd = HAIKU / "redo"
    for t in _jload(rd / "REDO_INDEX.json")["tasks"]:
        b = _tasks_of(a, "redo-v1", cache, probs, [dict(t, task_id=t["name"], batch_id=t["batch_id"])], "pool",
                      lambda _t: "text")[0]
        b.answer = rd / "answers" / f"{t['name']}.json"
        b.expected = set(t["qids"])
        b.source_task = t["source_task_id"]
        stray = sorted(q for q in b.expected if b.batch.task_of.get(q) != b.source_task)
        if stray:
            probs.append(f"redo task {t['name']}: qid(s) {stray[:3]} are not items of its source chunk")
        specs.append(b)
    r2 = HAIKU / "redo2"
    for idx_path in (R2_INDEX, R2B_INDEX):
        if idx_path.is_file():
            idx = _jload(idx_path)
            stage = "redo2-a" if idx_path == R2_INDEX else "redo2-b"
            specs += _tasks_of(r2, stage, cache, probs, idx["tasks"], "name",
                               lambda t: "meaning" if t["kind"] == "extract_lex" else "text")
    return specs, probs


def validate_all(specs: list) -> tuple:
    """({(round, task_id): result}, [problems]). Every answer file under an answers/ folder must belong to a task."""
    res, probs = {}, []
    ignored = set(AUDIT_FAILED_IGNORED)
    for s in specs:
        r = validate_answer(s.batch, s.task_id, s.answer, s.payload, s.expected)
        r["round"], r["name"] = s.round, s.name
        r["audit_failed_ignored"] = s.answer.name in ignored or s.task_id in ignored
        if r["audit_failed_ignored"]:
            r["ok"], r["answers"] = False, []
            r["problems"].append("ignored: the file-access audit failed")
        res[(s.round, s.task_id)] = r
        if not r["ok"] and s.round in ("author-v1", "extract-v1"):      # the v1 baseline cannot do without these files
            probs.append(f"{s.round} {s.task_id}: {'; '.join(r['problems'][:3])}")
    named = {s.answer.resolve() for s in specs}
    for d in (HAIKU / "author" / "answers", HAIKU / "extract" / "answers", HAIKU / "redo" / "answers",
              HAIKU / "redo2" / "answers"):
        for p in sorted(d.glob("*.json")) if d.is_dir() else []:
            if p.resolve() not in named:
                probs.append(f"unmapped answer file {_rel(p)} (no task names it)")
    return res, probs


def _ok_answers(res: dict, rnd: str, task_id: str) -> list | None:
    r = res.get((rnd, task_id))
    return r["answers"] if r and r["ok"] else None


# ------------------------------------------------------------------------------------------------ skins and attacks
def merged_author(name: str, specs: list, res: dict, batches: dict) -> tuple:
    """(pieces by internal id, problems, replaced qids) for 'skins' or 'attacks': the v1 answers with the redo-v1
    objects replacing only their own qids, through the v1 loader's own loop (haiku_author._loop)."""
    b, plan = batches[name]
    raw, probs = {}, []
    for c in b.chunks:
        got = _ok_answers(res, "author-v1", c["task_id"])
        if got is None:
            probs.append(f"{c['task_id']}: answer file rejected or missing")
        else:
            raw[c["task_id"]] = [dict(a) for a in got]
    replaced = {}
    for s in specs:
        if s.round != "redo-v1" or s.batch.batch_id != b.batch_id:
            continue
        got = _ok_answers(res, "redo-v1", s.task_id)
        if got is None or s.source_task not in raw:
            probs.append(f"{s.task_id}: redo answer rejected or its source chunk missing; the v1 answers stay")
            continue
        by_q = {a["qid"]: a for a in got}
        raw[s.source_task] = [dict(by_q.get(a["qid"], a)) for a in raw[s.source_task]]
        replaced[s.task_id] = sorted(by_q)
    ans, p2 = CH.load_answers(b, raw)
    check = HA.check_skin if name == "skins" else HA.check_attack
    out, seen = {}, set()
    for iid, a in sorted(ans.items()):
        text = a.get("text") if isinstance(a, dict) else None
        obj, v = check(iid, text, plan[iid], HA._task_of(b, iid), b.prompt_sha, seen)
        if v:
            probs.append(f"{iid}: " + "; ".join(v[:4]))
        else:
            out[obj.skin_id] = obj
    return out, probs + p2, replaced


# ------------------------------------------------------------------------------------------------ R2 loader checks
def _r2(obj, v: list, idx: int, seen: set, fixtures) -> tuple:
    """R2: a Haiku text equal to a fixtures.py text is a valid candidate; "duplicate" still means a duplicate of a pool
    candidate. Adds the text to `seen` only when the candidate is valid."""
    if obj is None:
        return obj, v
    text = obj[idx]
    if DUP in v and text.lower() not in seen and text in fixtures:
        v = [x for x in v if x != DUP]
    if not v:
        seen.add(text.lower())
    return obj, v


def check_wording_r2(iid, text, meta, tid, psha, seen) -> tuple:
    obj, v = HA.check_wording(iid, text, meta, tid, psha, set(seen))
    return _r2(obj, v, 1, seen, QFIXTURES)


def check_comparator_r2(iid, text, meta, tid, psha, seen) -> tuple:
    obj, v = HA.check_comparator(iid, text, meta, tid, psha, set(seen))
    return _r2(obj, v, 2, seen, CMP_FIXTURES)


# ------------------------------------------------------------------------------------------------ G-LEX registry
def _add_form(reg: LexiconRegistry, c: dict):
    return reg.add(c["text"], c["sem"], slots=dict(c["slots"]), source="haiku", family=F, haiku_task_id=c["tid"],
                   haiku_prompt_sha=c["psha"], held_out=bool(c["held_out"]))


def _form_id(sem: str, text: str) -> str:
    """LexiconRegistry.add's form id."""
    return f"{sem}#{hashlib.sha256(text.encode()).hexdigest()[:8]}"


def canonical_registry(base_json: dict, extra: list) -> tuple:
    """(registry, [(cand, reason)]): every v1 form (reads kept) plus the `extra` candidates, added in sorted form-id
    order and unit-tested once. That is the order LexiconRegistry.from_json (the generator's loader) gives. The kit's
    scan() breaks ties between two forms of one sense that span the same text by insertion order, so a unit test is
    only meaningful in a fixed order: this one."""
    reg = LexiconRegistry(base_json["name"])
    for s in base_json["sems"]:
        reg.declare(s["sem_id"], s["kind"], s["meaning"])
    rows = [("v1", x["form_id"], x) for x in base_json["forms"]]
    rows += [("new", _form_id(c["sem"], c["text"]), c) for c in extra]
    failed = []
    for kind, fid, x in sorted(rows, key=lambda r: r[1]):
        if kind == "v1":
            f = reg.add(x["text"], x["sem_id"], slots=x["slots"], source=x["source"], family=x["family"],
                        haiku_task_id=x["haiku_task_id"], haiku_prompt_sha=x["haiku_prompt_sha"],
                        held_out=x["held_out"])
            f.extractions = [tuple(e) for e in x["extractions"]]
        else:
            try:
                _add_form(reg, x)
            except LexiconError as e:
                failed.append((x, f"registry add: {str(e)[:120]}"))
    for a, b in base_json["antonyms"]:
        reg.declare_antonym(a, b)
    reg.unit_test_all()
    return reg, failed


def _breaks(reg: LexiconRegistry, before: dict) -> list:
    return sorted(fid for fid, ok in before.items() if ok and not reg.forms[fid].unit_ok)


def accept_forms(base_json: dict, cands: list) -> tuple:
    """(accepted [cand + form_id], dropped [(cand, reason)], registry). R1: each new form is added to the FULL registry
    (base_json = every v1 form, admitted or not, with its reads); it must pass its own unit test and break no form's
    unit test, else it is dropped. All candidates are tried together first (adding forms can only add ambiguity, so a
    clean run proves every prefix clean); on a failure the candidates are tried one after the other."""
    base, _ = canonical_registry(base_json, [])
    before = {fid: f.unit_ok for fid, f in base.forms.items()}
    reg, failed = canonical_registry(base_json, cands)
    gone = {id(c) for c, _ in failed}
    added = [(c, _form_id(c["sem"], c["text"])) for c in cands if id(c) not in gone]
    if all(reg.forms[fid].unit_ok for _, fid in added) and not _breaks(reg, before):
        return [dict(c, form_id=fid) for c, fid in added], list(failed), reg
    accepted, dropped = [], list(failed)
    for c, _fid in added:
        prev, _ = canonical_registry(base_json, accepted)
        prev_ok = {fid: f.unit_ok for fid, f in prev.forms.items()}
        trial, _ = canonical_registry(base_json, accepted + [c])
        fid = _form_id(c["sem"], c["text"])
        br = _breaks(trial, prev_ok)
        if trial.forms[fid].unit_ok and not br:
            accepted.append(c)
        else:
            why = "; ".join(trial.forms[fid].unit_problems[:2]) if not trial.forms[fid].unit_ok else f"breaks {br[:3]}"
            dropped.append((c, f"unit test in the full registry: {why}"))
    final, _ = canonical_registry(base_json, accepted)
    return [dict(c, form_id=_form_id(c["sem"], c["text"])) for c in accepted], dropped, final


def _meanings(reg: LexiconRegistry, kind: str) -> set:
    return {s.meaning for s in reg.sems.values() if s.kind == kind}


def record_votes(reg: LexiconRegistry, extractor: str, got: dict) -> dict:
    """reg.record_extraction for every answered form (got: {form id: {"meaning": text}}): the chosen meaning mapped to
    its sense; NONE or an unlisted text is a disagreement (sense None), never a default. A form not in the registry
    (dropped earlier) is skipped and counted. Returns the counts."""
    c = Counter()
    for fid, a in sorted(got.items()):
        if fid not in reg.forms:
            c["form_not_in_registry"] += 1
            continue
        f = reg.forms[fid]
        m = a.get("meaning") if isinstance(a, dict) else None
        if m is None or m == "NONE":
            outcome, sem = "none", None
        elif m in _meanings(reg, f.kind):
            outcome, sem = "listed", reg.meaning_to_sem(f.kind, m)
            if sem != f.sem_id:
                c["listed_other_sense"] += 1
        else:
            outcome, sem = "not_listed", None
        c[outcome] += 1
        reg.record_extraction(fid, extractor, sem)
    return dict(c)


def read_stage(reg: LexiconRegistry, specs: list, res: dict, rnd: str, plan_path: Path, problems: list) -> dict:
    """Record the votes of one read stage (two independent reads). The plan names each read's extractor id and the forms
    the stage reads; the batch key maps every qid to its form id."""
    if not Path(plan_path).is_file():
        problems.append(f"{rnd}: {_rel(plan_path)} is missing; its reads cannot be mapped to forms")
        return {"plan": _rel(plan_path), "missing": True, "reads": {}}
    plan = _jload(plan_path)
    reads = [s for s in specs if s.round == rnd and s.kind == "extract_lex"]
    out = {"plan": _rel(plan_path), "extractors": plan["extractor_ids"], "reads": {}}
    forms = set(plan["forms"])
    for s in sorted(reads, key=lambda s: s.name):
        if set(s.batch.key.values()) != forms:
            problems.append(f"{rnd} {s.name}: the batch reads {len(s.batch.key)} forms, the plan lists {len(forms)}")
        got = _ok_answers(res, rnd, s.task_id)
        if got is None:
            problems.append(f"{rnd} {s.task_id}: read rejected (answer file invalid or missing); its forms stay pending")
            out["reads"][s.name] = {"task": s.task_id, "rejected": True}
            continue
        by_form = {s.batch.key[a["qid"]]: {"meaning": a["meaning"]} for a in got}
        cnt = record_votes(reg, plan["extractor_ids"][s.name], by_form)
        cnt["unanswered"] = len(set(s.batch.key.values()) - set(by_form))
        out["reads"][s.name] = {"task": s.task_id, "batch_id": s.batch.batch_id, "answer_sha256":
                                res[(rnd, s.task_id)]["sha256"], "counts": cnt}
    return out


# ------------------------------------------------------------------------------------------------ the build
def _tree_sha(root: Path) -> dict:
    return {p.relative_to(root).as_posix(): _sha(p.read_bytes()) for p in sorted(Path(root).rglob("*"))
            if p.is_file() and "__pycache__" not in p.parts}


def v1_integrity() -> list:
    """Problems when a file of pools/ (freeze-v1) differs from the sha256 its own MANIFEST recorded."""
    man = _jload(POOLS_V1 / "MANIFEST.json")
    probs = []
    for name, sha in sorted(man["sha256"].items()):
        p = POOLS_V1 / name
        if not p.is_file() or _sha(p.read_bytes()) != sha:
            probs.append(f"pools/{name} differs from the freeze-v1 record")
    return probs


def interim_integrity() -> list:
    man = _jload(POOLS_INTERIM / "MANIFEST.json")
    return [f"pools/redo2/{n} differs from its record" for n, s in sorted(man["sha256"].items())
            if not (POOLS_INTERIM / n).is_file() or _sha((POOLS_INTERIM / n).read_bytes()) != s]


def build() -> dict:
    """The whole freeze-v2 in memory: {"files": {name: text}, "manifest": dict, "result": report dict}."""
    g0_sha = _sha(G0.read_bytes())
    if g0_sha != P.T15Plugin.G0_SHA256:
        raise SystemExit("G0_SPEC.md does not match the plugin pin")
    problems = {"v1_integrity": v1_integrity(), "interim_integrity": interim_integrity(), "batches": [],
                "answers": [], "rebuild": [], "record": [], "candidates": [], "reads": [], "registry": []}

    # 1. answer contract, all rounds
    specs, bprobs = collect_tasks()
    problems["batches"] += bprobs
    batches = HA.build_batches()
    for s in specs:                                   # the v1 loaders use the rebuilt batches: they must be the disk ones
        if s.round == "author-v1" and (batches[s.name][0].key != s.batch.key or
                                       batches[s.name][0].batch_id != s.batch.batch_id):
            problems["batches"].append(f"author batch {s.name}: the rebuilt batch differs from the one on disk")
    res, aprobs = validate_all(specs)
    problems["answers"] += aprobs

    # 2. v1 baseline and its reproduction of pools/
    st = GA.admit()
    for k in ("rebuild", "answers", "record"):
        problems[k] += list(st["problems"][k])
    v1_files = GA._files(st)
    v1_q = sorted(st["quarantine"], key=lambda r: (r["stage"], r["piece"]))
    v1_files["QUARANTINE.json"] = _dump({"family": F, "rows": v1_q})
    v1_repro = {n: (POOLS_V1 / n).is_file() and (POOLS_V1 / n).read_text(encoding="utf-8") == t
                for n, t in sorted(v1_files.items())}
    for n, ok in v1_repro.items():
        if not ok:
            problems["v1_integrity"].append(f"GA.admit() no longer reproduces pools/{n}")
    base_json = st["reg"].to_json()

    # 3. skins and attack lines (redo-v1 merged by qid)
    skins, sp, srep = merged_author("skins", specs, res, batches)
    attacks, ap, arep = merged_author("attacks", specs, res, batches)

    # 4. wordings and comparators: v1 candidates stay; added candidates in a fixed order
    seen_w = {w["text"].lower() for w in st["wordings"]}
    seen_c = {c["text"].lower() for c in st["comps"]}
    plan_v1 = {name: batches[name][1] for name in ("wordings", "comparators")}
    rejects = _jload(HAIKU / "redo2" / "plan" / "v1_load_rejects.json")
    r2a_plan = _jload(HAIKU / "redo2" / "plan" / "glex_reads_r2a.json")
    cands, c_drops = [], []

    def add_cand(pool, origin, iid, text, meta, tid, psha, expect_fid=None):
        if pool == "wordings":
            obj, v = check_wording_r2(iid, text, meta, tid, psha, seen_w)
        else:
            obj, v = check_comparator_r2(iid, text, meta, tid, psha, seen_c)
        if v:
            c_drops.append({"piece": iid, "stage": f"load:{origin}-{pool}", "reason": "; ".join(v[:4])})
            return
        if pool == "wordings":
            q, t, slots, held, tid_, psha_ = obj
            sem, kind = question_sem(F, q), "question"
        else:
            sem, kind, t, slots, tid_, psha_ = obj
            q, held = None, False
        cands.append({"iid": iid, "pool": pool, "origin": origin, "qform": q, "sem": sem, "kind": kind, "text": t,
                      "slots": dict(slots), "held_out": bool(held), "tid": tid_, "psha": psha_,
                      "expect_fid": expect_fid})

    for iid, r in sorted(rejects.items()):                       # R2 re-entries (planned by build_redo2, re-checked)
        if r["decision"].startswith("re-enter"):
            f = r2a_plan["forms"][r["form_id"]]
            add_cand(r["pool"], "redo2-reenter", iid, r["text"], plan_v1[r["pool"]][iid], f["haiku_task_id"],
                     f["haiku_prompt_sha"], expect_fid=r["form_id"])
    for s in specs:                                               # redo2 authoring answers
        if s.round != "redo2-a" or s.kind not in ("author_wording", "author_lexicon"):
            continue
        got = _ok_answers(res, s.round, s.task_id)
        if got is None:
            problems["candidates"].append(f"{s.task_id}: authoring answer file rejected; its items are unanswered")
            continue
        plan = _jload(HAIKU / "redo2" / "plan" / f"{s.batch.batch_id}.json")["plan"]
        pool = "wordings" if s.kind == "author_wording" else "comparators"
        for a in sorted(got, key=lambda a: s.batch.key[a["qid"]]):
            iid = s.batch.key[a["qid"]]
            add_cand(pool, f"redo2-{plan[iid]['redo2']}", iid, a["text"], plan[iid], s.task_id, s.batch.prompt_sha)
    order = {"redo2-reenter": 0}
    cands.sort(key=lambda c: (order.get(c["origin"], 1), c["pool"] != "wordings", c["iid"]))

    accepted, dropped, reg = accept_forms(base_json, cands)
    for c, why in dropped:
        c_drops.append({"piece": c["iid"], "stage": "unit:redo2", "reason": why})
    for c in accepted:
        if c["expect_fid"] and c["expect_fid"] != c["form_id"]:
            problems["candidates"].append(f"{c['iid']}: form id {c['form_id']} is not the planned {c['expect_fid']}")

    for fid in st["unit_bad"]:                      # R1: v1 verdicts are final (this form was never read)
        reg.forms[fid].unit_ok = False
        reg.forms[fid].unit_problems = list(st["reg"].forms[fid].unit_problems)
    rt = LexiconRegistry.from_json(reg.to_json())   # what the generator's loader will see
    for fid, f in reg.forms.items():
        if fid not in st["unit_bad"] and rt.forms[fid].unit_ok != f.unit_ok:
            problems["registry"].append(f"{fid}: unit test differs after a to_json / from_json round trip")

    # 5. G-LEX reads (r2a, and r2b when the stage exists)
    stages = {}
    stages["r2a"] = read_stage(reg, specs, res, "redo2-a", HAIKU / "redo2" / "plan" / "glex_reads_r2a.json",
                               problems["reads"])
    if R2B_INDEX.is_file():
        stages["r2b"] = read_stage(reg, specs, res, "redo2-b", HAIKU / "redo2" / "plan" / "glex_reads_r2b.json",
                                   problems["reads"])
    status_of = {fid: reg.status(fid) for fid in sorted(reg.forms)}

    # 6. assemble the v2 state in glex_admit's shape
    wordings = [dict(w, status=status_of[w["form_id"]]) for w in st["wordings"]]
    comps = [dict(c, status=status_of[c["form_id"]]) for c in st["comps"]]
    for c in accepted:
        if c["pool"] == "wordings":
            wordings.append({"form_id": c["form_id"], "qform": c["qform"], "sense": c["sem"], "text": c["text"],
                             "slots": dict(c["slots"]), "held_out": c["held_out"], "haiku_task_id": c["tid"],
                             "haiku_prompt_sha": c["psha"], "status": status_of[c["form_id"]]})
        else:
            comps.append({"form_id": c["form_id"], "sense": c["sem"], "text": c["text"], "slots": dict(c["slots"]),
                          "haiku_task_id": c["tid"], "haiku_prompt_sha": c["psha"], "status": status_of[c["form_id"]]})
    if len(reg.forms) != len(wordings) + len(comps):
        raise SystemExit(f"registry holds {len(reg.forms)} forms, pools list {len(wordings) + len(comps)}")
    origin = {c["form_id"]: c["origin"] for c in accepted}
    pieces = dict(st["pieces"], skins=skins, attacks=attacks)
    st2 = dict(st, pieces=pieces, reg=reg, status_of=status_of, wordings=wordings, comps=comps)
    counts = GA.counts(st2)
    short = GA.shortfalls(counts)

    used = [w["form_id"] for w in wordings if w["status"] == "admitted"] + \
           [c["form_id"] for c in comps if c["status"] == "admitted"]
    gate_used, gate_all = reg.gate(used_form_ids=used), reg.gate()
    kit = {"strict_kinds_in_registry": sorted({f.kind for f in reg.forms.values()} & set(STRICT_KINDS)),
           "required_reads": dict(sorted(Counter(f.required for f in reg.forms.values()).items())),
           "admitted_with_fewer_distinct_reads": [fid for fid in used if len({e for e, _ in reg.forms[fid].extractions})
                                                  < reg.forms[fid].required],
           "admitted_not_all_agreeing": [fid for fid in used if any(s != reg.forms[fid].sem_id
                                                                     for _, s in reg.forms[fid].extractions)],
           "admitted_unit_failing": [fid for fid in used if not reg.forms[fid].unit_ok]}
    held_adm = Counter(w["qform"] for w in wordings if w["held_out"] and w["status"] == "admitted")
    derived = {"admitted_held_out_per_qform": {q: held_adm.get(q, 0) for q in sorted(HA.WORDING_PLAN)}}
    for q in sorted(HA.WORDING_PLAN):
        if held_adm.get(q, 0) < 1:
            short.append(f"no admitted held-out wording for question form {q} (S5 cannot render it)")
    for k, v in kit.items():
        if k.startswith("admitted_") and v:
            short.append(f"G-LEX kit rule: {k}: {len(v)} form(s)")
    if kit["strict_kinds_in_registry"]:
        short.append(f"unexpected precedence / window forms in the T15 registry: {kit['strict_kinds_in_registry']}")
    pending = {"wordings_asked": sum(1 for w in wordings if w["status"] == "pending" and not w["held_out"]),
               "wordings_held": sum(1 for w in wordings if w["status"] == "pending" and w["held_out"]),
               "comparators": sum(1 for c in comps if c["status"] == "pending"),
               "forms": sorted(fid for fid, s in status_of.items() if s == "pending")}
    pending["wordings_candidates_asked_g_lex_decided"] = counts["wordings_candidates_asked"] - pending["wordings_asked"]
    pending["counting_note"] = (
        "wordings_candidates_asked counts every loader-valid, unit-tested candidate whatever its G-LEX status "
        "(admitted, rejected, unit_fail or pending), exactly as glex_admit.counts did for freeze-v1 (the 158 there "
        "included 5 rejected forms and 1 unit_fail). Pending forms (fewer than the required distinct reads) are never used: they are in "
        "lexicon.json (usable false) and in no pool file. The admission targets count admitted forms only.")

    # 7. quarantine
    recovered = {c["iid"] for c in accepted}
    q_rows = [r for r in v1_q if r["stage"] == "value-lint" or r["stage"] in ("load:packs", "load:names")
              or (r["stage"] in ("load:wordings", "load:comparators") and r["piece"] not in recovered)]
    q_rows += [{"piece": p.partition(": ")[0], "stage": "load:skins", "reason": p.partition(": ")[2] or p} for p in sp]
    q_rows += [{"piece": p.partition(": ")[0], "stage": "load:attacks", "reason": p.partition(": ")[2] or p}
               for p in ap]
    q_rows += c_drops
    q_rows += GA._form_quarantine(reg)
    for lst, tag in ((wordings, "wording"), (comps, "comparator")):
        for x in lst:
            if x["status"] != "admitted":
                q_rows.append({"piece": f"{tag}|{x['form_id']}", "stage": "G-LEX", "status": x["status"],
                               "reason": f"form {x['form_id']} is {x['status']}"})
    for (rnd, tid), r in sorted(res.items()):
        if not r["ok"]:
            q_rows.append({"piece": f"answers|{rnd}|{tid}", "stage": "answer-contract",
                           "reason": "; ".join(r["problems"][:3])})
    q_rows = sorted(q_rows, key=lambda r: (r["stage"], r["piece"]))

    # 8. files and manifest
    files = GA._files(st2)
    files["QUARANTINE.json"] = _dump({"family": F, "rows": q_rows})
    files["provenance.json"] = _dump({
        "family": F, "version": VERSION,
        "note": "origin and reads of every wording / comparator form; v1 forms are not listed (their record is in "
                "lexicon.json 'extractions'). pending = fewer than the required distinct reads: never used.",
        "forms": {fid: {"origin": o, "status": status_of[fid], "extractions": [list(e) for e in reg.forms[fid]
                                                                            .extractions]}
                  for fid, o in sorted(origin.items())}})
    problem_list = [f"{k}: {p}" for k, ps in problems.items() for p in ps]
    ready = not short and not problem_list and gate_used["pass"]
    answers_rep = [{k: v for k, v in r.items() if k != "answers"} for _, r in sorted(res.items())]
    rounds = Counter((r["round"], r["ok"]) for r in answers_rep)
    man = {
        "family": F, "version": VERSION, "build": "families/T15/freeze_v2.py -> pools_v2/",
        "status": ("FROZEN: every G0 target met and G-LEX passes on the used forms; G13-seed (6.4 step 4) still pending"
                   if ready else
                   "FROZEN WITH SHORTFALLS: see shortfalls; the pools are not complete to the G0 targets, and G13-seed "
                   "(6.4 step 4) has not run"),
        "verdict": "READY" if ready else "SHORT",
        "supersedes": "none; freeze-v1 (pools/) and the interim supplement pools/redo2/ (v1 + redo-v1 skins / attacks "
                      "only) are left unchanged on disk",
        "g0": {"path": "families/T15/G0_SPEC.md", "sha256": g0_sha, "matches_plugin_pin": True},
        "rulings": "G0_SPEC.md v1.2 section 6: R1 (G-LEX 2/2 per form; v1 reads, admissions and rejections final; a "
                   "new form passes its unit test in the full v1 registry and breaks none), R2 (a Haiku text equal to a "
                   "fixture text is a valid candidate), R3 (complement surfaces), R4 (distinct role values in redo2 "
                   "reads)",
        "answer_files": {"by_round": {f"{r}|{'ok' if ok else 'rejected'}": n for (r, ok), n in sorted(rounds.items())},
                         "audit_failed_ignored": list(AUDIT_FAILED_IGNORED),
                         "audit": "file-access audit not re-run here: no agent transcripts in this step",
                         "files": answers_rep},
        "folded": {
            "redo_v1": {"source": "haiku/redo/REDO_INDEX.json", "replaced_qids": srep | arep,
                        "skins_loader_problems": len(sp), "attack_loader_problems": len(ap)},
            "redo2": {"candidates_checked": len(cands) + len(c_drops) - len(dropped),
                      "accepted": Counter(c["origin"] for c in accepted),
                      "accepted_forms": sorted(c["form_id"] for c in accepted),
                      "dropped": c_drops},
        },
        "reads": {"v1": {r: {"batch_id": st["meta"]["reads"][r]["batch_id"], "seed": st["meta"]["reads"][r]["seed"],
                             "extractor": GA.EXTRACTOR[r], "tasks": {t: st["answer_sha"][t] for t in
                                                                   sorted(st["answer_sha"]) if t.startswith(
                                 st["meta"]["reads"][r]["batch_id"])}} for r in GA.READS},
                  **stages},
        "answer_reads_v1": st["read_counts"],
        "pending_glex": pending,
        "problems": problems,
        "v1_reproduced": v1_repro,
        "unit_test_excluded_from_reads_v1": st["unit_bad"],
        "gates": {"G-LEX_used_forms": {k: v for k, v in gate_used.items() if k != "not_admitted"},
                  "G-LEX_all_forms": {k: v for k, v in gate_all.items() if k != "not_admitted"},
                  "G-LEX_all_forms_not_admitted_count": len(gate_all["not_admitted"]),
                  "G-LEX_kit_rules": kit,
                  "G-SL": "applied at load (skins, attacks, wordings, comparators) and by lint_values (names, packs)",
                  "G3-H": "not applicable: T15 is Mode T only (G0 S19, documents_mode_f 0); no free-text document, so "
                          "no G3-H vote exists to record",
                  "audit": "not re-run here (no agent transcripts)", "G13_seed": "not run (6.4 step 4)"},
        "counts": counts, "derived_requirements": derived, "targets_g0": GA.G0_TARGETS, "shortfalls": short,
        "quarantined": len(q_rows),
        "load_recipe": "from families.T15 import freeze_v2 as FV; pools = FV.load_pools(); plugin = "
                       "FV.make_plugin(pools); ctx = FV.make_ctx(pools). T15Plugin reads no pool path (constructor "
                       "arguments only). g13_c2.py seeds from families/T15/pools/** only and does not see pools_v2/.",
        "sha256": {n: _sha(t) for n, t in sorted(files.items())},
        "note_manifest": "sha256 of every other file in pools_v2/ (this file is not hashed)",
    }
    files["MANIFEST.json"] = _dump(man)
    man = json.loads(files["MANIFEST.json"])                  # exactly what is on disk (JSON keys are strings)
    return {"files": files, "manifest": man, "state": st2, "ready": ready, "shortfalls": short,
            "problems": problem_list, "pending": pending, "counts": counts, "status_of": status_of}


# ------------------------------------------------------------------------------------------------ freeze and report
def freeze(out: dict) -> list:
    if (POOLS_V2 / "MANIFEST.json").exists():
        raise SystemExit("pools_v2/MANIFEST.json already exists: refusing to re-freeze")
    before = _tree_sha(POOLS_V1)
    rest = {n: t for n, t in out["files"].items() if n != "MANIFEST.json"}
    written = paths.write_files(POOLS_V2, rest)                       # the MANIFEST last: no half-frozen folder has one
    written += paths.write_files(POOLS_V2, {"MANIFEST.json": out["files"]["MANIFEST.json"]})
    after = _tree_sha(POOLS_V1)
    if before != after:
        raise SystemExit("pools/ changed while freezing (it must stay untouched)")
    return [str(p) for p in written]


def report(out: dict) -> dict:
    man = out["manifest"]
    return {"verdict": man["verdict"], "status": man["status"], "shortfalls": out["shortfalls"],
            "problems": out["problems"], "pending_glex": {k: v for k, v in out["pending"].items() if k != "forms"},
            "answer_files": man["answer_files"]["by_round"], "counts": {
                k: out["counts"][k] for k in (
                    "skins_by_register", "attacks_asked", "attacks_held", "wordings_candidates_asked",
                    "wordings_candidates_held", "wordings_admitted_asked", "wordings_admitted_held",
                    "wordings_admitted_asked_by_form", "comparators_candidates_by_sense",
                    "comparators_admitted_by_sense", "lexicon_forms", "lexicon_status")},
            "gates": {"G-LEX_used_forms": man["gates"]["G-LEX_used_forms"],
                      "G-LEX_all_forms_not_admitted_count": man["gates"]["G-LEX_all_forms_not_admitted_count"],
                      "kit_rules": man["gates"]["G-LEX_kit_rules"]},
            "folded_redo2": {"accepted": man["folded"]["redo2"]["accepted"],
                             "dropped": man["folded"]["redo2"]["dropped"]},
            "quarantined": man["quarantined"]}


# ------------------------------------------------------------------------------------------------ loading pools_v2
@dataclass
class Pools:
    lexicon: LexiconRegistry
    packs: list
    names: dict
    skins: dict
    wordings: list
    comparators: list
    manifest: dict = field(default_factory=dict)


def _skin_from_json(d: dict) -> Skin:
    return Skin(skin_id=d["skin_id"], family=d["family"], text=d["text"], slots=tuple(tuple(x) for x in d["slots"]),
                kind=d["kind"], register=d["register"], escape=d["escape"],
                counts=tuple(tuple(x) for x in d["counts"]), author_mode=d["author_mode"], qform=d["qform"],
                brief=tuple(tuple(x) for x in d["brief"]), haiku_task_id=d["haiku_task_id"],
                haiku_prompt_sha=d["haiku_prompt_sha"], lexicon_ids=tuple(d["lexicon_ids"]),
                held_out=bool(d["held_out"]))


def pools_from_texts(texts: dict, *, check_sha: bool = True) -> Pools:
    """Pools from {file name: text} (what freeze writes). check_sha: every file against MANIFEST.json."""
    man = json.loads(texts["MANIFEST.json"])
    if check_sha:
        for n, sha in man["sha256"].items():
            if _sha(texts[n]) != sha:
                raise ValueError(f"pools_v2/{n} differs from MANIFEST.json")
    lex = LexiconRegistry.from_json(json.loads(texts["lexicon.json"]))
    packs = []
    for p in json.loads(texts["packs.json"])["packs"]:
        pk = P.make_pack(p["id"], p["kind"], p["programme"], tuple(tuple(r) for r in p["routes"]), tuple(p["others"]),
                         held_out=p["held_out"])
        if list(pk["enrol"]) != list(p["enrol"]):
            raise ValueError(f"pack {p['id']}: enrolment values differ from the file")
        packs.append(pk)
    names = json.loads(texts["names.json"])["pools"]
    skins = {d["skin_id"]: _skin_from_json(d) for k in ("skins.json", "attacks.json")
             for d in json.loads(texts[k])["skins" if k == "skins.json" else "attacks"]}
    wordings = json.loads(texts["wordings.json"])["wordings"]
    comps = json.loads(texts["comparators.json"])["comparators"]
    return Pools(lex, packs, names, skins, wordings, comps, man)


def load_pools(root: Path = POOLS_V2) -> Pools:
    root = Path(root)
    return pools_from_texts({p.name: p.read_text(encoding="utf-8") for p in sorted(root.glob("*.json"))})


def make_plugin(pools: Pools):
    return P.T15Plugin(lexicon=pools.lexicon, packs=pools.packs, names=pools.names)


def make_ctx(pools: Pools) -> KitCtx:
    """Case-note skins, attack lines and the ADMITTED wordings (each wording skin points at its lexicon form)."""
    skins = dict(pools.skins)
    for w in pools.wordings:
        if pools.lexicon.status(w["form_id"]) != "admitted":
            raise ValueError(f"wording {w['form_id']} is not an admitted form")
        sid = f"T15-WD-{w['qform']}-{w['form_id'].split('#')[1]}"
        skins[sid] = make_skin(sid, F, w["text"], dict(w["slots"]), kind="wording", register="question",
                               qform=w["qform"], lexicon_ids=(w["form_id"],), held_out=w["held_out"],
                               haiku_task_id=w["haiku_task_id"], haiku_prompt_sha=w["haiku_prompt_sha"])
    return KitCtx(skins=skins, lexicon=pools.lexicon)


def smoke(pools: Pools, seeds: int = 6) -> dict:
    """A == B and the rendered-row checks for a few seeds per sampler, with these pools (nothing is written)."""
    from c2_kit import pipeline
    pl, ctx, n = make_plugin(pools), make_ctx(pools), 0
    for smp in pl.SAMPLERS:
        for seed in range(seeds):
            spec = pl.sample(seed, smp)
            rr = pl.render(spec, ctx)
            if not (pl.solve_a(spec) == pl.solve_b(pl.parse(rr.row, ctx)) == rr.answer):
                raise AssertionError(f"A != B at {smp}/{seed}")
            probs = pipeline.check_rendered(pl, spec, rr, ctx, run_g15=False)
            if probs:
                raise AssertionError(f"{smp}/{seed}: {probs[:2]}")
            n += 1
    return {"rows": n, "samplers": list(pl.SAMPLERS)}


# ------------------------------------------------------------------------------------------------ CLI
def main(argv: list) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=("check", "freeze", "validate", "smoke"), nargs="?", default="check")
    a = ap.parse_args(argv[1:])
    if a.cmd == "validate":
        specs, bp = collect_tasks()
        res, ap_ = validate_all(specs)
        print(json.dumps({"batch_problems": bp, "problems": ap_,
                          "files": [{k: v for k, v in r.items() if k != "answers"} for _, r in sorted(res.items())]},
                         indent=1, ensure_ascii=False))
        return 0 if not bp and not ap_ and all(r["ok"] for r in res.values()) else 1
    if a.cmd == "smoke":
        print(json.dumps(smoke(load_pools()), indent=1))
        return 0
    out = build()
    rep = report(out)
    if a.cmd == "freeze":
        rep["written"] = [Path(p).name for p in freeze(out)]
    print(json.dumps(rep, indent=1, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

"""t37b/answers_gate.py: strict answer-file validation (all rounds) and the READY / SHORT verdict of the T37b equiv pool.

Why this exists. The family's readers are lenient: chunker.load_answers accepts extra keys and any number of questions
per item, and builder.norm_relation turns ' Same' or 'SAME' into 'same'. Every task file, though, tells its Haiku agent
an exact answer contract. This module checks every answer file of every round against that contract and REJECTS (never
edits, never repairs) a file that breaks it. A rejected file contributes no question and no vote.

Rounds (each one a TaskBatch rebuilt from the family code and compared with the files on disk):
  v1-author   haiku/author            author_wording   9 tasks      -> {qid, questions: 5 strings}
  v1-read-A/B haiku/extract           polarity         2 x 5 tasks  -> {qid, relation: same | opposite | unclear}
  r2-author   haiku/redo2             author_wording   3 tasks
  r2-read-A/B haiku/redo2/extract     polarity         2 x 2 tasks

Contract checked per file (the ANSWER CONTRACT of the task file / AUTHOR_FORMAT / POLARITY_FORMAT):
  * UTF-8 JSON, one array, nothing before or after it (no BOM, no code fence), no duplicate key, no NaN;
  * exactly one object per item of the task, each item answered once, the qid exactly as given (q + 10 letters / digits);
  * each object has exactly the two keys qid and (questions | relation);
  * questions: a list of exactly 5 strings, each one line, no leading / trailing space, ending with '?';
  * relation: exactly the string same, opposite or unclear (case and spaces count);
  * the file is the task's own answer file and the answers/ folder holds no other file.
The per-question content rules (placeholders, bans, polarity programs, G-SL, duplicates) are the unchanged v1 gate and
drop single questions at lint; they are not part of the file contract.

Votes (kit rule, c2_kit.lexicon status(): a form is ADMITTED only with >= 2 distinct extractors all agreeing; any other
meaning REJECTS it for good with no re-vote; T37b has no precedence / window family, so 2/2 and never 3/3). A paraphrase
is the form, the two independent polarity reads (separate batches, seeds, chunks and agents) are the extractors, and
'same' is the only admitting meaning. glex_status() below is that rule. G3-H does not apply to T37b (no free-form text).

Verdict (gate()): READY iff every one of the 20 pool entries holds at least its G0 target (7 fixed question, 12 slotted;
never lowered), the G-LEX rule passes for every paraphrase the generator will load (frozen v1 pool + the redo2
supplement), every answer file is valid, and the independent re-derivation of the admissions equals the pools on disk.
Otherwise SHORT, with the exact shortfalls. Nothing here sets or reads a label.

Run from lean/ (read-only; --write puts one JSON record at haiku/ANSWERS_GATE.json):
  ../.venv/bin/python c2_build/t37b/answers_gate.py validate [--write]
  ../.venv/bin/python c2_build/t37b/answers_gate.py gate     [--write]
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
from collections import Counter
from pathlib import Path

_C2_BUILD = Path(__file__).resolve().parents[1]
if str(_C2_BUILD) not in sys.path:
    sys.path.insert(0, str(_C2_BUILD))

from c2_kit import chunker, paths  # noqa: E402
from t37b import author_pool as AP  # noqa: E402
from t37b import builder as BL  # noqa: E402
from t37b import gsl_pool_lint as GL  # noqa: E402
from t37b import sources as SRC  # noqa: E402

HERE = Path(__file__).resolve().parent
LEAN = paths.LEAN
RECORD = HERE / "haiku" / "ANSWERS_GATE.json"
FREEZE_MANIFEST = HERE / "pools" / "FREEZE_MANIFEST.json"
FIX_MANIFEST = HERE / "pools" / "FIX_I1_MANIFEST.json"     # generator CODE changed by an authorised fix iteration
REDO2_FILE = HERE / "haiku" / "redo2" / "build_redo2.py"

QID_RE = re.compile(r"^q[0-9A-Za-z]{10}$")
RELATIONS = ("same", "opposite", "unclear")
N_QUESTIONS = AP.PER_ITEM                                  # 5 questions per authoring item
KEYS = {"author_wording": ("qid", "questions"), "polarity": ("qid", "relation")}
REQUIRED_READS = 2                                          # G-LEX: 2/2 for T37b (3/3 only for precedence / window)


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def rel(p: Path) -> str:
    """Path relative to c2_build/ (stable in the record)."""
    try:
        return Path(p).resolve().relative_to(_C2_BUILD.resolve()).as_posix()
    except ValueError:
        return str(p)


def redo2():
    """The redo2 module (haiku/redo2/build_redo2.py), loaded once under the name the redo2 tests use."""
    name = "t37b_build_redo2"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, REDO2_FILE)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


# ------------------------------------------------------------------------------------------------ strict file contract

def _no_dup_pairs(pairs):
    d = {}
    for k, v in pairs:
        if k in d:
            raise ValueError(f"duplicate key {k!r}")
        d[k] = v
    return d


def _bad_constant(name):
    raise ValueError(f"non-JSON constant {name}")


def parse_answer_bytes(raw: bytes) -> tuple:
    """(parsed JSON or None, problems): the strict reading of one answer file."""
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as e:
        return None, [f"not UTF-8: {e}"]
    if text.startswith("\ufeff"):
        return None, ["byte-order mark before the JSON"]
    t = text.strip()
    if not t:
        return None, ["empty file"]
    if t.startswith("```") or t.endswith("```"):
        return None, ["markdown code fence around the JSON"]
    if not (t.startswith("[") and t.endswith("]")):
        return None, ["not one JSON array (text before or after it)"]
    try:
        return json.loads(text, object_pairs_hook=_no_dup_pairs, parse_constant=_bad_constant), []
    except (ValueError, RecursionError) as e:
        return None, [f"not valid JSON: {e}"]


def _question_problems(q) -> str | None:
    if not isinstance(q, str):
        return "not a string"
    if not q or q != q.strip():
        return "empty, or leading / trailing space"
    if any(ord(c) < 32 or c in "\x85\u2028\u2029" for c in q):
        return "not one line"
    if not q.endswith("?"):
        return "does not end with '?'"
    return None


def validate_bytes(raw: bytes, kind: str, qids) -> list:
    """Problems of one answer file against its contract (empty = valid). qids: the qids of the task's items."""
    obj, probs = parse_answer_bytes(raw)
    if probs:
        return probs
    want_keys = set(KEYS[kind])
    field = KEYS[kind][1]
    expect = list(qids)
    if not isinstance(obj, list):
        return ["the top level is not an array"]
    if len(obj) != len(expect):
        probs.append(f"{len(obj)} objects, the task has {len(expect)} items")
    seen = Counter()
    for i, o in enumerate(obj):
        where = f"object {i}"
        if not isinstance(o, dict):
            probs.append(f"{where}: not an object")
            continue
        if set(o) != want_keys:
            probs.append(f"{where}: keys {sorted(o)}, the contract is exactly {sorted(want_keys)}")
        qid = o.get("qid")
        if not isinstance(qid, str) or not QID_RE.match(qid):
            probs.append(f"{where}: qid {qid!r} is not q + 10 letters or digits")
        elif qid not in expect:
            probs.append(f"{where}: qid {qid} is not an item of this task")
        else:
            seen[qid] += 1
        if field not in o:
            continue
        val = o[field]
        if kind == "polarity":
            if not isinstance(val, str) or val not in RELATIONS:
                probs.append(f"{where}: relation {val!r} is not exactly one of {list(RELATIONS)}")
        else:
            if not isinstance(val, list) or len(val) != N_QUESTIONS:
                probs.append(f"{where}: questions is not a list of exactly {N_QUESTIONS} strings")
                continue
            for j, q in enumerate(val):
                bad = _question_problems(q)
                if bad:
                    probs.append(f"{where}: questions[{j}] {bad}")
    probs += [f"qid {q} answered {n} times" for q, n in sorted(seen.items()) if n > 1]
    probs += [f"item {q} not answered" for q in expect if q not in seen]
    return probs


# ------------------------------------------------------------------------------------------------ rounds on disk

def _read_json(p: Path):
    if paths.never_open(p):
        raise paths.NeverOpen(f"never-open path: {p}")
    return json.loads(Path(p).read_text(encoding="utf-8"))


def _tasks_rows(p: Path) -> tuple:
    """(TASKS.json object, {task id: row}); the polarity TASKS.json holds both read batches."""
    obj = _read_json(p)
    return obj, {t["task_id"]: t for t in obj["tasks"]}


def build_rounds() -> list:
    """The seven (round, batch) pairs, rebuilt from the family code. 'text' rebuilds a task file for comparison."""
    R = redo2()
    v1c = _read_json(AP.AUTHOR_DIR / "lint" / "candidates.json")["candidates"]
    r2c = _read_json(R.LINT_DIR / "candidates.json")["candidates"]
    pa1, pb1 = AP.polarity_batches(v1c)
    pa2, pb2 = R.polarity_batches(r2c)

    def v1_text(title, fmt):
        return lambda b, c, root: AP.task_text(b, c, root, title=title, answer_format=fmt)

    def r2_text(title):
        return lambda b, c, root: R.task_text(b, c, root, title)

    rounds = [
        {"name": "v1-author", "kind": "author_wording", "root": AP.AUTHOR_DIR, "batch": AP.author_batch(),
         "tasks_json": AP.AUTHOR_DIR / "TASKS.json", "cands": None,
         "text": v1_text("Haiku authoring task", AP.AUTHOR_FORMAT)},
        {"name": "v1-read-A", "kind": "polarity", "root": AP.EXTRACT_DIR, "batch": pa1, "cands": v1c,
         "tasks_json": AP.EXTRACT_DIR / "TASKS.json", "text": v1_text("Haiku polarity read A", AP.POLARITY_FORMAT)},
        {"name": "v1-read-B", "kind": "polarity", "root": AP.EXTRACT_DIR, "batch": pb1, "cands": v1c,
         "tasks_json": AP.EXTRACT_DIR / "TASKS.json", "text": v1_text("Haiku polarity read B", AP.POLARITY_FORMAT)},
        {"name": "r2-author", "kind": "author_wording", "root": R.ROOT, "batch": R.author_batch(), "cands": None,
         "tasks_json": R.ROOT / "TASKS.json", "text": r2_text("T37b redo2 authoring task")},
        {"name": "r2-read-A", "kind": "polarity", "root": R.EX_ROOT, "batch": pa2, "cands": r2c,
         "tasks_json": R.EX_ROOT / "TASKS.json", "text": r2_text("T37b redo2 polarity read A")},
        {"name": "r2-read-B", "kind": "polarity", "root": R.EX_ROOT, "batch": pb2, "cands": r2c,
         "tasks_json": R.EX_ROOT / "TASKS.json", "text": r2_text("T37b redo2 polarity read B")},
    ]
    for r in rounds:     # the two reads of a round share one answers/ folder: its expected names are both batches'
        r["names"] = {c["task_id"] + ".json" for o in rounds if o["root"] == r["root"] for c in o["batch"].chunks}
    return rounds


def _on_disk(root: Path, files: dict, skip=("tasks/", "answers/")) -> list:
    out = []
    for relpath, text in sorted(files.items()):
        if relpath.startswith(skip):
            continue
        p = root / relpath
        if not p.is_file() or p.read_text(encoding="utf-8") != text:
            out.append(relpath)
    return out


def validate_round(rnd: dict) -> dict:
    """Validate every answer file of one round. A round-level mismatch (prompt, key, manifest, TASKS.json) rejects all
    its files; a task-level mismatch (chunk or task file differs from the rebuild) rejects that task's file."""
    b, root, kind = rnd["batch"], Path(rnd["root"]), rnd["kind"]
    round_probs, task_probs = [], {}
    man, rows = _tasks_rows(rnd["tasks_json"])
    ids = man.get("batch_ids") or [man.get("batch_id")]
    if b.batch_id not in ids:
        round_probs.append(f"TASKS.json lists batches {ids}, the rebuild is {b.batch_id}")
    for relpath in _on_disk(root, {k: v for k, v in b.files().items() if not k.startswith("chunks/")}):
        round_probs.append(f"{relpath} differs from the rebuild")
    exp_names = rnd.get("names") or {c["task_id"] + ".json" for c in b.chunks}
    adir = root / "answers"
    present = {p.name for p in adir.iterdir()} if adir.is_dir() else set()
    extra = sorted(present - exp_names - {"README.txt"})
    if extra:
        round_probs.append(f"unexpected files in answers/: {extra}")
    files = []
    for c in b.chunks:
        tid = c["task_id"]
        tp = []
        qids = [it["qid"] for it in c["items"]]
        cpath = root / b.chunk_path(tid)
        if not cpath.is_file() or cpath.read_text(encoding="utf-8") != json.dumps(c, ensure_ascii=False, indent=1) + "\n":
            tp.append("chunk file differs from the rebuild")
        row = rows.get(tid)
        ans = root / b.answer_path(tid)
        if row is None:
            tp.append("task not listed in TASKS.json")
        else:
            if Path(row["answer_file"]) != ans:
                tp.append(f"TASKS.json answer_file {row['answer_file']} is not {ans}")
            if row.get("n_items") != len(qids):
                tp.append(f"TASKS.json n_items {row.get('n_items')} != {len(qids)}")
            tfile = root / "tasks" / f"{tid}.md"
            if not tfile.is_file():
                tp.append("task file missing")
            else:
                ttext = tfile.read_text(encoding="utf-8")
                if "task_sha256" in row and sha_bytes(ttext.encode()) != row["task_sha256"]:
                    tp.append("task file differs from its TASKS.json sha256")
                if ttext != rnd["text"](b, c, root):
                    tp.append("task file differs from the rebuild")
        res = {"round": rnd["name"], "task_id": tid, "kind": kind, "file": rel(ans), "n_items": len(qids),
               "n_answers": None, "sha256": None, "bytes": None, "valid": False, "problems": []}
        if paths.never_open(ans):
            res["problems"].append(f"never-open path {ans}")
        elif not ans.is_file():
            res["problems"].append("answer file missing")
        else:
            raw = ans.read_bytes()
            res["sha256"], res["bytes"] = sha_bytes(raw), len(raw)
            parsed, _p = parse_answer_bytes(raw)
            res["n_answers"] = len(parsed) if isinstance(parsed, list) else None
            res["problems"] += validate_bytes(raw, kind, qids)
        res["problems"] += [f"integrity: {x}" for x in round_probs + tp]
        res["valid"] = not res["problems"]
        files.append(res)
    return {"round": rnd["name"], "kind": kind, "batch_id": b.batch_id, "n_tasks": len(b.chunks),
            "n_items": len(b.key), "round_problems": round_probs,
            "n_valid": sum(f["valid"] for f in files), "files": files}


def valid_raw(rnd: dict, result: dict) -> dict:
    """{task id: parsed answer list} of the files that passed validation only (the only answers anything may use)."""
    root = Path(rnd["root"])
    out = {}
    for f in result["files"]:
        if f["valid"]:
            out[f["task_id"]] = json.loads((root / rnd["batch"].answer_path(f["task_id"])).read_text(encoding="utf-8"))
    return out


# ------------------------------------------------------------------------------------------------ votes (G-LEX rule)

def glex_status(votes, unit_ok: bool, required: int = REQUIRED_READS) -> str:
    """c2_kit.lexicon.LexiconRegistry.status() for one paraphrase. votes: [(extractor id, relation)]. Any reading other
    than 'same' rejects it for good (no re-vote); the unit test (lint + G-SL) must pass; then `required` DISTINCT
    extractors must all have said 'same'."""
    if any(r != "same" for _e, r in votes):
        return "rejected"
    if not unit_ok:
        return "unit_fail"
    if len({e for e, _r in votes}) >= required:
        return "admitted"
    return "pending"


def unit_ok(rec: dict) -> tuple:
    """(ok, problems): the unchanged v1 unit test of a pool paraphrase (author_pool.lint_one + gsl_pool_lint.gsl_check)."""
    e = SRC.ENTRY_BY_KEY[rec["sem"]]
    probs = AP.lint_one(e, rec["template"]) + [f"G-SL {v.rule}: {v.detail}" for v in GL.gsl_check(rec)]
    return not probs, probs


def vote_rows(cands: list, rnd_a: dict, rnd_b: dict, valid_a: dict, valid_b: dict) -> list:
    """One row per candidate: the two reads (None when the answer is absent or its file was rejected), the extractor
    ids (the read task ids) and the G-LEX status. Uses only answers from files that passed validation."""
    ba, bb = rnd_a["batch"], rnd_b["batch"]
    got_a, _pa = chunker.load_answers(ba, valid_a)
    got_b, _pb = chunker.load_answers(bb, valid_b)
    task_a = {iid: ba.task_of[q] for q, iid in ba.key.items()}
    task_b = {iid: bb.task_of[q] for q, iid in bb.key.items()}
    out = []
    for c in cands:
        k = AP.rec_pair_key(c)
        ra = got_a.get(k, {}).get("relation")
        rb = got_b.get(k, {}).get("relation")
        votes = [(task_a[k], ra)] if ra is not None else []
        votes += [(task_b[k], rb)] if rb is not None else []
        ok, probs = unit_ok(c)
        out.append({"template_id": c["template_id"], "sem": c["sem"], "template": c["template"], "pair_key": k,
                    "reads": [ra, rb], "extractors": [task_a[k], task_b[k]], "unit_ok": ok, "unit_problems": probs,
                    "status": glex_status(votes, ok)})
    return out


def admitted_ids(rows: list) -> list:
    return sorted(r["template_id"] for r in rows if r["status"] == "admitted")


# ------------------------------------------------------------------------------------------------ validation of all rounds

def validate_all(rounds: list | None = None) -> tuple:
    """(rounds, results). Nothing is written."""
    rounds = rounds or build_rounds()
    return rounds, [validate_round(r) for r in rounds]


def validation_summary(results: list) -> dict:
    files = [f for r in results for f in r["files"]]
    return {"rounds": {r["round"]: {"batch_id": r["batch_id"], "tasks": r["n_tasks"], "items": r["n_items"],
                                    "valid": r["n_valid"], "round_problems": r["round_problems"]} for r in results},
            "files": len(files), "valid": sum(f["valid"] for f in files),
            "invalid": [{"file": f["file"], "problems": f["problems"]} for f in files if not f["valid"]],
            "audit": "transcripts sit under never-open paths and were not read; the orchestrator's ignore list was [] "
                     "(no answer file is excluded on audit grounds). Files are used only if they pass this contract."}


# ------------------------------------------------------------------------------------------------ the gate

def fix_shas() -> dict:
    """{relpath: {"from", "to"}} of generator CODE files an authorised fix iteration changed after the v1 freeze (C2 spec
    6.4 step 6; pools/FIX_I1_MANIFEST.json, written with the amendment that names the change). Only a .py file under
    c2_build/t37b/ qualifies, and "from" must be the sha the freeze recorded: the manifest can never excuse a pool, an
    answer file, the G0 page or any other data file, and a code file edited again after the fix is flagged."""
    if not FIX_MANIFEST.is_file():
        return {}
    out = {}
    for relpath, e in (_read_json(FIX_MANIFEST).get("code") or {}).items():
        if relpath.startswith("c2_build/t37b/") and relpath.endswith(".py") and isinstance(e, dict):
            out[relpath] = e
    return out


def v1_untouched() -> list:
    """Problems with the v1 freeze: any sha256 in pools/FREEZE_MANIFEST.json that no longer matches its file, except a
    generator code file that pools/FIX_I1_MANIFEST.json records as changed from exactly the frozen sha to exactly the
    file's current sha (fix_shas). Pool, Haiku answers, task records, G0 v2 and every other data file stay exact."""
    probs = []
    fixes = fix_shas()
    for relpath, want in sorted(_read_json(FREEZE_MANIFEST)["sha256"].items()):
        p = LEAN / relpath
        got = sha_bytes(p.read_bytes()) if p.is_file() else None
        if got == want:
            continue
        fx = fixes.get(relpath)
        if got is not None and fx and fx.get("from") == want and fx.get("to") == got:
            continue
        probs.append(f"{relpath} changed")
    return probs


def pool_entry_targets() -> dict:
    return {e.key: (AP.TARGET_SLOTTED if SRC.pool_template(e)[1] else AP.TARGET_FIXED) for e in AP.pool_entries()}


def check(cid: str, ok: bool, detail) -> dict:
    return {"check": cid, "pass": bool(ok), "detail": detail}


def gate(supplement: Path | None = None) -> dict:
    """The full verdict. Reads only; the supplement pool is the redo2 admit output on disk (None: not admitted)."""
    paths.require_a38()
    R = redo2()
    supplement = Path(supplement) if supplement else R.SUPP_POOL
    rounds, results = validate_all()
    by = {r["name"]: (r, res) for r, res in zip(rounds, results)}
    checks, issues = [], []

    # 1 files
    vs = validation_summary(results)
    checks.append(check("answer files valid", not vs["invalid"] and not any(r["round_problems"] for r in results),
                        f"{vs['valid']} of {vs['files']} files pass the contract"))

    # 2 spec, targets, v1 freeze
    checks.append(check("G0 spec frozen", not BL.g0_problems(), BL.g0_problems()))
    v1man = _read_json(AP.POOL_DIR / "MANIFEST.json")
    targets = pool_entry_targets()
    checks.append(check("G0 targets not lowered", targets == v1man["report"]["targets"] and len(targets) == 20,
                        {"entries": len(targets), "total": sum(targets.values())}))
    checks.append(check("v1 freeze untouched", not v1_untouched() and
                        sha_bytes(AP.POOL_FILE.read_bytes()) == R.V1_POOL_SHA256, v1_untouched()))

    # 3 independent re-derivation of the admissions from the strictly validated reads
    def derive(name_a, name_b):
        ra, rb = by[name_a][0], by[name_b][0]
        va, vb = valid_raw(*by[name_a]), valid_raw(*by[name_b])
        return vote_rows(ra["cands"], ra, rb, va, vb)

    v1_rows = derive("v1-read-A", "v1-read-B")
    r2_rows = derive("r2-read-A", "r2-read-B")
    v1_pool = AP.load_pool(AP.POOL_FILE)
    v1_ids = sorted(c["template_id"] for c in v1_pool.paraphrases)
    checks.append(check("v1 admissions re-derived = frozen v1 pool", admitted_ids(v1_rows) == v1_ids,
                        {"derived": len(admitted_ids(v1_rows)), "frozen": len(v1_ids)}))
    native, _rep = AP.admit(by["r2-read-A"][0]["cands"], chunker.load_answers(by["r2-read-A"][0]["batch"],
                                                                              valid_raw(*by["r2-read-A"]))[0],
                            chunker.load_answers(by["r2-read-B"][0]["batch"], valid_raw(*by["r2-read-B"]))[0])
    checks.append(check("redo2 strict votes = family admit()", admitted_ids(r2_rows) == sorted(
        c["template_id"] for c in native), {"strict": len(admitted_ids(r2_rows)), "family": len(native)}))
    r2_status = Counter(r["status"] for r in r2_rows)
    checks.append(check("no pending read (every candidate has both reads)", r2_status.get("pending", 0) == 0 and all(
        r is not None for row in r2_rows for r in row["reads"]), dict(r2_status)))
    ex = [r["extractors"] for r in r2_rows + v1_rows]
    checks.append(check("reads come from distinct extractors (2 independent batches)", all(a != b for a, b in ex),
                        f"{len(ex)} candidates, A and B read by different tasks"))

    # 4 the pool the generator loads
    admitted_supplement = supplement.is_file()
    try:
        merged = R.load_merged_pool(AP.POOL_FILE, supplement)
        load_err = None
    except (RuntimeError, ValueError, OSError) as e:
        merged, load_err = AP.load_pool(AP.POOL_FILE), str(e)
    checks.append(check("merged pool loads (frozen, G0, 2/2 'same', tied to v1 sha, no repeats)", load_err is None,
                        load_err or f"{len(merged.paraphrases)} paraphrases"))
    if admitted_supplement and load_err is None:
        supp_ids = sorted(c["template_id"] for c in AP.load_pool(supplement).paraphrases)
        checks.append(check("redo2 supplement on disk = re-derived admissions", supp_ids == admitted_ids(r2_rows),
                            {"on_disk": len(supp_ids), "derived": len(admitted_ids(r2_rows))}))
    else:
        checks.append(check("redo2 supplement admitted", False, "no supplement pool on disk (redo2 not admitted)"))

    # 5 G-LEX on every paraphrase the generator would load
    bad = []
    quarantined = {r["template_id"] for r in v1_rows + r2_rows if r["status"] == "rejected"}
    for c in merged.paraphrases:
        ok, probs = unit_ok(c)
        if c.get("reads") != ["same", "same"] or c.get("status") != "admitted" or not ok or \
                c["template_id"] in quarantined:
            bad.append({"template_id": c["template_id"], "problems": probs or ["reads / status / quarantined"]})
    checks.append(check("G-LEX: every loaded paraphrase admitted 2/2 'same', unit test and G-SL clean, none rejected",
                        not bad, {"paraphrases": len(merged.paraphrases), "bad": bad[:5]}))

    # 6 G0 minimums
    per = Counter(c["sem"] for c in merged.paraphrases)
    per_entry = {k: {"admitted": per[k], "target": t, "shortfall": max(0, t - per[k])} for k, t in targets.items()}
    shortfalls = {k: v["shortfall"] for k, v in per_entry.items() if v["shortfall"]}
    checks.append(check("G0 minimum: every pool entry at or above its target", not shortfalls,
                        {"entries_short": len(shortfalls), "total_shortfall": sum(shortfalls.values())}))

    ready = all(c["pass"] for c in checks)
    for c in checks:
        if not c["pass"]:
            issues.append(f"check failed: {c['check']}: {c['detail']}")
    return {
        "family": "T37b", "verdict": "READY" if ready else "SHORT", "ready": ready,
        "shortfalls": [f"{k}: {v['admitted']} of {v['target']} (short by {v['shortfall']})"
                       for k, v in per_entry.items() if v["shortfall"]],
        "issues": issues, "checks": checks, "per_entry": per_entry,
        "totals": {"target": sum(targets.values()), "admitted": len(merged.paraphrases), "v1": len(v1_pool.paraphrases),
                   "redo2": len(merged.paraphrases) - len(v1_pool.paraphrases)},
        "votes": {"rule": "G-LEX admission: >= 2 distinct independent reads, all 'same' (2/2; T37b has no 3/3 family); "
                          "any other reading rejects for good (no re-vote); G3-H not applicable (no free-form text)",
                  "v1": dict(Counter(r["status"] for r in v1_rows)), "redo2": dict(r2_status),
                  "rejected": [{"template_id": r["template_id"], "sem": r["sem"], "template": r["template"],
                                "reads": r["reads"], "extractors": r["extractors"]}
                               for r in v1_rows + r2_rows if r["status"] == "rejected"]},
        "validation": validation_summary(results),
        "answer_files": [{k: f[k] for k in ("round", "file", "sha256", "bytes", "n_items", "n_answers", "valid")}
                         for r in results for f in r["files"]],
        "load": {"generator": "from t37b import author_pool as AP; pool = AP.load_pool(<path>) takes a path; "
                              "builder / select read no configurable pool path, so nothing in the plugin was changed",
                 "merged": f"load_merged_pool() in {rel(REDO2_FILE)} (v1 pool + {rel(supplement)}); it checks the sha256 "
                           "of the frozen v1 pool, the G0 sha, 2/2 'same' reads and repeats",
                 "g13": "g13_c2 seed scans t37b/pools/ recursively (pools/redo2/ is covered); not run here: it runs the "
                        "sealed checkers by path (never-open rule)"},
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("stage", choices=("validate", "gate"))
    ap.add_argument("--write", action="store_true", help="write haiku/ANSWERS_GATE.json (nothing else is written)")
    a = ap.parse_args(argv)
    paths.require_a38()
    if a.stage == "validate":
        _rounds, results = validate_all()
        out = validation_summary(results) | {"files_detail": [f for r in results for f in r["files"]]}
        bad = bool(out["invalid"])
    else:
        out = gate()
        bad = not out["ready"]
    if a.write:
        paths.write_json(RECORD, out)
        out = {**{k: v for k, v in out.items() if k not in ("files_detail", "answer_files")}, "written": rel(RECORD)}
    print(json.dumps(out, indent=1, ensure_ascii=False, default=str))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())

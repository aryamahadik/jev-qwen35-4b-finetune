"""families/T31/dneg_i2.py: the double-negation round of T31 fix iteration 2 (G10 double_negation_share >= 2%).

Shared code of dneg_stage2.py and dneg_stage3.py. Nothing here runs Haiku or any model: the orchestrator runs Haiku between
the stages. No frozen file is edited (pools_v2/, pilot_loaders.py, plugin.py and G0_SPEC.md stay as they are).

  write-tasks (CLI here)  the gold-free authoring task files under haiku/dneg_i2/tasks/ (answers: haiku/dneg_i2/answers/).
                          dneg_authoring's brief and polarity-aware check; 32 items per form = 4 x the 8 admitted wordings
                          per form that are wanted, in chunks of 16 (2 task files per form, 4 in all). Each item pins its
                          outer frame, the place of the second 'not' and a style, so the 32 wordings of a form differ.
  stage 2  admit the authoring answers (dneg_authoring.wording_problems: shape, placeholders, (2, 2) negation profile,
           c2_kit.polarity P1-P4, G-SL; plus REQ_ID rule and exact-text dedup), add the survivors to the pools_v2 lexicon
           in memory, unit-test them, write the two independent G-LEX reads to haiku/dneg_i2/glex_tasks/.
  stage 3  record the reads (2/2 agreeing extractors admit), check that no frozen form regresses, write the supplement
           pools_v2_dneg/ that run_pilot_i2.py's loader reads, then the pilot steps (dneg_stage3.py).

Every folder is an argument so the tests can run in a temp dir.
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker as CH  # noqa: E402
from c2_kit import paths  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit.lexicon import LexiconError, question_sem  # noqa: E402
from families.T31 import dneg_authoring as DN  # noqa: E402
from families.T31 import extract_build as EB  # noqa: E402
from families.T31 import freeze_v2 as FV  # noqa: E402
from families.T31 import glex_admit as GA  # noqa: E402
from families.T31 import haiku_author as HA  # noqa: E402

F = "T31"
VERSION = "dneg_i2"
ROOT = HERE / "haiku" / "dneg_i2"
GLEX_SUB = "glex_tasks"
SUPP = HERE / "pools_v2_dneg"
FORMS = DN.FORMS
TRACK_OF = {"yn_holder_dneg": "appr", "yn_agent_dneg": "agent"}
NEEDED = 8                                   # admitted wordings wanted per form
OVERSAMPLE = 4                               # candidates per wanted wording
PER_FORM = NEEDED * OVERSAMPLE               # 32 candidates per form
MIN_ADMITTED_PER_FORM = 6                    # below this a form is a SHORTFALL (dneg_authoring: >= 6 are needed)
AUTHOR_CHUNK = 16                            # items per authoring task file
GLEX_CHUNK = 32                              # items per G-LEX task file
READS = ("d2read0", "d2read1")               # 2/2 (T31 has no precedence or window form); new extractor ids
SEED_AUTHOR = "t31-dneg-i2-author"
SEED_GLEX = "t31-dneg-i2-glex"

OUTER = ("Is it not the case that", "Is it not true that", "Is it not correct that")
ANCHORS = {
    "yn_holder_dneg": ("on the verb 'was' ('... {CANDIDATE} was not the accountable approver ...')",
                       "on a holding verb ('... {CANDIDATE} did not hold the accountable role ...')",
                       "on the verb 'is' ('... {CANDIDATE} is not the accountable approver ...')"),
    "yn_agent_dneg": ("on 'permitted' ('... is not permitted to use ...')", "on 'allowed' ('... is not allowed to use ...')",
                      "on 'entitled' ('... is not entitled to use ...')",
                      "on 'authorised' ('... is not authorised to use ...')"),
}
# the two styles that put something before the outer frame contradict the pinned opening
STYLES = tuple(s for s in HA.WORDING_STYLES if not s.startswith(("starts with a lead-in", "puts the time phrase first")))


class SupplementError(RuntimeError):
    pass


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _dump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=1) + "\n"


def _read_json(p: Path):
    return json.loads(Path(p).read_text(encoding="utf-8"))


# ------------------------------------------------------------------------------------------------ authoring tasks
def author_items(q: str) -> list:
    meaning, required = DN.MEANING[q]
    out = []
    for i in range(PER_FORM):
        slots = {r.strip("{}"): "required, exactly once" for r in required}
        slots["REQ_ID"] = "optional, at most once" if i % 2 == 0 else "leave it out"
        outer = OUTER[i % len(OUTER)]
        anchor = ANCHORS[q][(i // len(OUTER)) % len(ANCHORS[q])]
        style = STYLES[(i * 3 + len(q)) % len(STYLES)]
        out.append((f"wording|{q}|{i:03d}", {
            "brief": f"Meaning: {meaning} Style: {style}.", "slots": slots,
            "rules": list(DN.RULES) + [f"open with exactly '{outer}'", f"put the second 'not' {anchor}"]}))
    return out


def author_batches() -> list:
    """[(info, TaskBatch)] in memory, one batch per form (deterministic: seeds and prompt are fixed)."""
    out = []
    for q in FORMS:
        track = TRACK_OF[q]
        b = CH.make_batch("author_wording", F, author_items(q), seed=f"{SEED_AUTHOR}|{track}", prompt=DN.prompt(track),
                          max_items=AUTHOR_CHUNK, forbid_strings=HA.FORBID_WORDING)
        out.append(({"task": f"dneg-author-{track}", "qform": q, "track": track}, b))
    return out


def _author_md(b, chunk: dict, answer: Path, q: str) -> str:
    n = len(chunk["items"])
    ph = ", ".join("{" + r.strip("{}") + "}" for r in DN.MEANING[q][1])
    return (
        f"# T31 double-negation authoring task {chunk['task_id']}\n\n"
        f"ANSWER FILE (write your whole answer here, and nowhere else, with the Write tool):\n{answer}\n\n"
        f"Task kind: {b.kind}; items: {n}; answers expected: {n} (one per item, each with its qid).\n\n"
        "This task file is the only file you may open. Do not open, list or search any other file or folder.\n\n"
        f"{b.prompt}\n"
        "EXACT ANSWER CONTRACT (a checking program drops an entry that breaks it; the entry is lost):\n"
        f"- The answer file holds ONE JSON array of exactly {n} objects, one per item, each exactly "
        "{\"qid\": \"<the item's qid>\", \"text\": \"<the question>\"} with no other key.\n"
        "- text: one line, 6-30 words, one question ending with exactly one '?', and it starts with the outer frame "
        "named in the item's rules (the frame, then the embedded statement).\n"
        f"- text holds the placeholders {ph} each exactly once, written plain with braces; {{REQ_ID}} at most once, and "
        "only when the item allows it. No other placeholder, no grammar helper.\n"
        "- Exactly two 'not' words in the whole question (the frame's and the one named in the item's rules). No other "
        "negation word, no contraction ending in n't, no word that means block, bar, deny, lack, forbid or prevent.\n"
        "- Valid JSON only: no text before or after the array; write a double quote inside a string as \\\".\n"
        f"- The {n} questions of this file must differ from one another (no two the same).\n\n"
        "ITEMS (JSON; answer every item, keyed by its qid):\n"
        f"{json.dumps(chunk['items'], ensure_ascii=False, indent=1)}\n\n"
        f"Reminder: write one JSON array to {answer} and nothing else.\n")


def author_files(root: Path = ROOT) -> tuple:
    """({relative path under root: text}, TASKS.json object)."""
    root = Path(root)
    files, tasks = {}, []
    for info, b in author_batches():
        files.update(b.files())
        for c in b.chunks:
            tid = c["task_id"]
            answer = root / b.answer_path(tid)
            rel = f"tasks/{tid}.md"
            text = _author_md(b, c, answer, info["qform"])
            for iid in b.key.values():
                if iid in text:
                    raise CH.ChunkError(f"{tid}: task file names an internal id")
            files[rel] = text
            reads, writes = b.allowed(str(root), tid)
            tasks.append({"task": info["task"], "task_id": tid, "batch_id": b.batch_id, "kind": b.kind,
                          "qform": info["qform"], "track": info["track"], "n_items": len(c["items"]),
                          "prompt_sha": b.prompt_sha, "task_file": str(root / rel), "answer_file": str(answer),
                          "allowed_read": sorted(reads | {str(root / rel)}), "allowed_write": sorted(writes)})
    manifest = {"family": F, "version": VERSION, "seed": SEED_AUTHOR, "g0_sha256": GA.P.POOL_G0_SHA256,
                "plan": {"forms": list(FORMS), "wanted_admitted_per_form": NEEDED, "oversample": OVERSAMPLE,
                         "candidates_per_form": PER_FORM, "items_per_task": AUTHOR_CHUNK},
                "n_tasks": len(tasks), "items_expected": sum(t["n_items"] for t in tasks),
                "audit": "a task agent may read only allowed_read (its task file; chunk and prompt are copies) and write "
                         "only allowed_write; audit.audit_jsonl discards a failed agent's answers",
                "tasks": tasks}
    files["TASKS.json"] = _dump(manifest)
    files["answers/README.txt"] = "Haiku answer files: one <task_id>.json per task file in ../tasks/ (see ../TASKS.json).\n"
    return files, manifest


def write_author(root: Path = ROOT) -> dict:
    root = Path(root)
    if (root / "TASKS.json").exists():
        raise SystemExit(f"{root}/TASKS.json exists: refusing to rewrite the authoring tasks (keys would no longer match)")
    files, manifest = author_files(root)
    paths.write_files(root, files)
    return manifest


# ------------------------------------------------------------------------------------------------ helpers
def slots_of(text: str) -> dict:
    return {k: ("name" if k == "CANDIDATE" else "id") for k in HA._phs(text)}


def declare_sems(lex) -> None:
    for q in FORMS:
        lex.declare(question_sem(F, q), "question", DN.QUESTION_SEM_MEANING[q])


def base_lexicon():
    """The frozen pools_v2 registry (every vote) with the two double-negation question meanings declared."""
    lex = FV.load_pools()["lexicon"]
    declare_sems(lex)
    return lex


def verify_batch_files(base: Path, b) -> list:
    """Prompt, chunks, key and manifest of a rebuilt batch must equal the files on disk byte for byte."""
    probs = []
    for rel, text in sorted(b.files().items()):
        p = Path(base) / rel
        if not p.is_file():
            probs.append(f"{rel} is missing on disk")
        elif p.read_text(encoding="utf-8") != text:
            probs.append(f"{rel} differs from the rebuilt batch")
    return probs


def read_answer_files(base: Path, rows: list) -> tuple:
    """(raw {task_id: parsed JSON}, {task_id: sha256}, problems) of <base>/answers/<task_id>.json for each task row."""
    raw, sha, probs = {}, {}, []
    for t in rows:
        p = Path(base) / "answers" / f"{t['task_id']}.json"
        if not p.is_file():
            probs.append(f"{t['task_id']}: answer file missing")
            continue
        data = p.read_bytes()
        sha[t["task_id"]] = _sha(data)
        try:
            raw[t["task_id"]] = json.loads(data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            probs.append(f"{t['task_id']}: not valid JSON ({e})")
    return raw, sha, probs


# ------------------------------------------------------------------------------------------------ stage 2
def admit_authoring(root: Path = ROOT, lex=None) -> dict:
    """The authoring answers through the checks -> {"candidates": [...], "quarantine": [...], "problems": [...],
    "per_form": {...}}. `lex` (default base_lexicon()) is mutated: the candidates are added and unit-tested."""
    root = Path(root)
    lex = lex if lex is not None else base_lexicon()
    man = _read_json(root / "TASKS.json")
    rows = man["tasks"]
    problems, quar = [], []
    raw_all, _sha_by, rprobs = read_answer_files(root, rows)
    problems += rprobs
    cands, seen = [], {}
    existing = {EB._norm(f.text): fid for fid, f in lex.forms.items()}
    per_form = {q: Counter() for q in FORMS}
    known = {t["batch_id"]: t for t in rows}
    for info, b in author_batches():
        if b.batch_id not in known:
            problems.append(f"rebuilt batch {b.batch_id} is not in TASKS.json")
            continue
        problems += [f"{info['qform']}: {p}" for p in verify_batch_files(root, b)]
        tids = [c["task_id"] for c in b.chunks]
        got, lprobs = CH.load_answers(b, {t: raw_all[t] for t in tids if t in raw_all})
        problems += [f"{info['qform']}: {p}" for p in lprobs]
        items = CH.item_by_internal(b)
        inv = {v: k for k, v in b.key.items()}
        pf = per_form[info["qform"]]
        pf["asked"] = len(b.key)
        pf["answered"] = len(got)
        for iid in sorted(got):
            a, q = got[iid], iid.split("|")[1]
            text = a.get("text") if isinstance(a, dict) else None
            why = DN.wording_problems(q, text) if isinstance(text, str) else ["no text"]
            if not why and isinstance(a, dict) and set(a) - {"qid", "text"}:
                why = [f"answer keys {sorted(a)} (exactly qid and text)"]
            if not why and "{REQ_ID" in text and items[iid]["slots"].get("REQ_ID") == "leave it out":
                why = ["REQ_ID used where the item says leave it out"]
            text = text.strip() if isinstance(text, str) else text
            if not why:
                k = EB._norm(text)
                if k in seen:
                    why = [f"duplicate text of {seen[k]}"]
                elif k in existing:
                    why = [f"duplicate of frozen form {existing[k]}"]
                else:
                    seen[k] = iid
            if why:
                pf["lint_reject"] += 1
                quar.append({"piece": iid, "qform": q, "stage": "wording_problems/dedup", "text": text,
                             "reason": "; ".join(why[:4])})
                continue
            qid = inv[iid]
            tid = b.task_of[qid]
            cands.append({"iid": iid, "qform": q, "qid": qid, "task_id": tid, "prompt_sha": b.prompt_sha, "text": text})
    ok = []
    for c in sorted(cands, key=lambda c: c["iid"]):
        try:
            f = lex.add(c["text"], question_sem(F, c["qform"]), slots=slots_of(c["text"]), source="haiku", family=F,
                        haiku_task_id=c["task_id"], haiku_prompt_sha=c["prompt_sha"])
        except LexiconError as e:
            quar.append({"piece": c["iid"], "qform": c["qform"], "stage": "lexicon", "text": c["text"], "reason": str(e)})
            per_form[c["qform"]]["lexicon_reject"] += 1
            continue
        c["form_id"] = f.form_id
        if not lex.unit_test(f.form_id):
            quar.append({"piece": c["iid"], "qform": c["qform"], "stage": "unit", "text": c["text"],
                         "reason": "; ".join(f.unit_problems[:2])})
            per_form[c["qform"]]["unit_fail"] += 1
            continue
        per_form[c["qform"]]["to_glex"] += 1
        ok.append(c)
    return {"candidates": ok, "quarantine": quar, "problems": problems, "per_form": {q: dict(v) for q, v in per_form.items()},
            "lex": lex}


def restore_registry(cands: list, lex=None):
    """The registry stage 2 built (pools_v2 + the two sems + the candidate forms, unit-tested)."""
    lex = lex if lex is not None else base_lexicon()
    for c in sorted(cands, key=lambda c: c["iid"]):
        f = lex.add(c["text"], question_sem(F, c["qform"]), slots=slots_of(c["text"]), source="haiku", family=F,
                    haiku_task_id=c["task_id"], haiku_prompt_sha=c["prompt_sha"])
        if f.form_id != c["form_id"]:
            raise SupplementError(f"form id drift {c['form_id']} -> {f.form_id}")
        lex.unit_test(f.form_id)
    return lex


def glex_batches(lex, fids: list) -> list:
    out = []
    for read in READS:
        seed = f"{SEED_GLEX}|{read}"
        items = EB.extraction_items(lex, fids, seed)
        out.append((read, CH.make_batch("extract_lex", F, items, seed=seed, prompt=EB.EXTRACT_PROMPT + EB.EXTRACT_TAIL,
                                        max_items=GLEX_CHUNK)))
    return out


def glex_files(root: Path, lex, fids: list, cands_sha: str) -> tuple:
    groot = Path(root) / GLEX_SUB
    files, tasks = {}, []
    for read, b in glex_batches(lex, fids):
        files.update(b.files())
        for c in b.chunks:
            tid = c["task_id"]
            answer = groot / b.answer_path(tid)
            rel = f"tasks/{tid}.md"
            text = EB._task_md(b, c, answer, read)
            for iid in b.key.values():
                if iid in text:
                    raise CH.ChunkError(f"{tid}: task file names an internal id")
            files[rel] = text
            reads, writes = b.allowed(str(groot), tid)
            tasks.append({"task": f"glex-{read}", "task_id": tid, "batch_id": b.batch_id, "kind": "extract_lex",
                          "read": read, "n_items": len(c["items"]), "prompt_sha": b.prompt_sha,
                          "task_file": str(groot / rel), "answer_file": str(answer),
                          "allowed_read": sorted(reads | {str(groot / rel)}), "allowed_write": sorted(writes)})
    man = {"family": F, "version": VERSION, "reads": list(READS), "forms_for_admission": sorted(fids),
           "candidates_sha256": cands_sha, "n_tasks": len(tasks),
           "note": "each read is an independent Haiku agent (a different agent for each read); 2/2 agreeing reads admit",
           "tasks": tasks}
    files["TASKS.json"] = _dump(man)
    files["answers/README.txt"] = "Haiku G-LEX answer files: one <task_id>.json per task file in ../tasks/.\n"
    return files, man


def run_stage2(root: Path = ROOT, *, write: bool = True, lex=None) -> dict:
    root = Path(root)
    if write and (root / GLEX_SUB / "TASKS.json").exists():
        raise SystemExit(f"{root}/{GLEX_SUB}/TASKS.json exists: refusing to rewrite the G-LEX reads")
    st = admit_authoring(root, lex)
    cands = sorted(st["candidates"], key=lambda c: c["iid"])
    cands_text = _dump({"family": F, "version": VERSION, "candidates": cands})
    per = {q: sum(1 for c in cands if c["qform"] == q) for q in FORMS}
    out = {"per_form": st["per_form"], "to_glex_per_form": per, "quarantined": len(st["quarantine"]),
           "problems": st["problems"], "written": False,
           "short": [q for q in FORMS if per[q] < MIN_ADMITTED_PER_FORM]}
    if not cands:
        out["status"] = "STOP: no candidate survives the checks; nothing written for G-LEX"
        return out
    fids = [c["form_id"] for c in cands]
    files, man = glex_files(root, st["lex"], fids, _sha(cands_text.encode("utf-8")))
    out["glex_tasks"] = man["n_tasks"]
    out["status"] = ("OK" if not out["short"] and not st["problems"] else
                     "CHECK: " + ("; ".join(st["problems"][:3]) if st["problems"] else
                                  f"forms short of {MIN_ADMITTED_PER_FORM} candidates for G-LEX: {out['short']}"))
    if write:
        paths.write_files(root / GLEX_SUB, files)
        paths.write_text(root / "admitted_candidates.json", cands_text)
        paths.write_text(root / "QUARANTINE_AUTHORING.json", _dump({"family": F, "rows": st["quarantine"]}))
        paths.write_text(root / "STAGE2_REPORT.json", _dump(out))
        out["written"] = True
    return out


# ------------------------------------------------------------------------------------------------ stage 3
def admit_glex(root: Path = ROOT, lex=None) -> dict:
    """The G-LEX reads recorded on the rebuilt registry -> {"admitted": [candidate + extractions], "rejected": [...],
    "counts": {...}}. Stops (SystemExit) when an answer file is missing or the rebuilt batches differ from disk."""
    root = Path(root)
    gd = root / GLEX_SUB
    cands_text = (root / "admitted_candidates.json").read_text(encoding="utf-8")
    cands = json.loads(cands_text)["candidates"]
    man = _read_json(gd / "TASKS.json")
    if man["candidates_sha256"] != _sha(cands_text.encode("utf-8")):
        raise SystemExit("STOP: admitted_candidates.json changed after the G-LEX reads were written")
    reg = restore_registry(cands, lex)
    fids = sorted(c["form_id"] for c in cands)
    if fids != man["forms_for_admission"]:
        raise SystemExit("STOP: the forms for admission differ from glex_tasks/TASKS.json")
    batches = dict(glex_batches(reg, fids))
    known = {t["batch_id"]: t["read"] for t in man["tasks"]}
    probs = []
    for read, b in batches.items():
        if known.get(b.batch_id) != read:
            probs.append(f"{read}: rebuilt batch id {b.batch_id} is not the TASKS.json batch")
        probs += [f"{read}: {p}" for p in verify_batch_files(gd, b)]
    raw, sha, rprobs = read_answer_files(gd, man["tasks"])
    probs += rprobs
    if probs:
        raise SystemExit(f"STOP: G-LEX answers or task files are incomplete or unreadable: {probs[:8]}")
    raw_by_read = {read: {t["task_id"]: raw[t["task_id"]] for t in man["tasks"] if t["read"] == read} for read in batches}
    counts, rec_probs = GA._record(reg, batches, raw_by_read)
    admitted, rejected = [], []
    for c in sorted(cands, key=lambda c: c["iid"]):
        fid = c["form_id"]
        f = reg.forms[fid]
        st = reg.status(fid)
        again = DN.wording_problems(c["qform"], c["text"]) if st == "admitted" else []
        if st == "admitted" and not again:
            admitted.append({**c, "extractions": [list(e) for e in f.extractions], "unit_ok": f.unit_ok})
        else:
            why = (f"G-LEX status {st}: " + ", ".join(f"{e}: {s}" for e, s in f.extractions)) if st != "admitted" \
                else "; ".join(again[:3])
            rejected.append({"piece": c["iid"], "qform": c["qform"], "stage": "G-LEX", "text": c["text"], "reason": why})
    return {"admitted": admitted, "rejected": rejected, "read_counts": counts, "record_problems": rec_probs,
            "answer_sha": sha, "problems": probs}


def _add_admitted(lex, items: list) -> list:
    out = []
    for c in items:
        f = lex.add(c["text"], question_sem(F, c["qform"]), slots=slots_of(c["text"]), source="haiku", family=F,
                    haiku_task_id=c["task_id"], haiku_prompt_sha=c["prompt_sha"])
        if f.form_id != c["form_id"]:
            raise SupplementError(f"form id drift {c['form_id']} -> {f.form_id}")
        f.extractions = [tuple(e) for e in c["extractions"]]
        out.append(f)
    return out


def _bad_after(lex, old: dict, new_fids: list) -> tuple:
    lex.unit_test_all()
    regress = [fid for fid, s in old.items() if s == "admitted" and lex.status(fid) != "admitted"]
    new_bad = [fid for fid in new_fids if lex.status(fid) != "admitted"]
    return regress, new_bad


def regression_check(admitted: list) -> tuple:
    """Add the admitted forms to a fresh pools_v2 registry and unit-test everything: a new form must not make a frozen
    admitted form fail (parse ambiguity). -> (kept items, [(item, why)]). All at once; when that fails, one by one."""
    lex = FV.load_pools()["lexicon"]
    declare_sems(lex)
    old = {fid: lex.status(fid) for fid in lex.forms}
    _add_admitted(lex, admitted)
    regress, new_bad = _bad_after(lex, old, [c["form_id"] for c in admitted])
    if not regress and not new_bad:
        return list(admitted), []
    lex = FV.load_pools()["lexicon"]
    declare_sems(lex)
    old = {fid: lex.status(fid) for fid in lex.forms}
    kept, dropped = [], []
    for c in admitted:
        _add_admitted(lex, [c])
        regress, new_bad = _bad_after(lex, old, [c["form_id"]])
        if regress or new_bad:
            del lex.forms[c["form_id"]]
            lex._rx.clear()
            dropped.append((c, f"unit/regression: breaks {regress[:2]}" if regress else "own unit test fails"))
        else:
            kept.append(c)
    return kept, dropped


def wording_skin_obj(c: dict) -> dict:
    q = c["qform"]
    sk = K.make_skin(f"T31-W-{q}-{c['qid']}", F, c["text"], slots_of(c["text"]), kind="wording", register="question",
                     qform=q, haiku_task_id=c["task_id"], haiku_prompt_sha=c["prompt_sha"])
    d = dataclasses.asdict(sk)
    d.update({"track": TRACK_OF[q], "form_id": c["form_id"], "sense": question_sem(F, q)})
    return d


def write_supplement(adm: dict, supp: Path = SUPP, extra: dict | None = None, *, force: bool = False) -> dict:
    supp = Path(supp)
    if (supp / "MANIFEST.json").exists() and not force:
        raise SystemExit(f"{supp}/MANIFEST.json exists: refusing to overwrite the supplement (use --force)")
    kept, dropped = regression_check(adm["admitted"]) if adm["admitted"] else ([], [])
    quarantine = list(adm["rejected"]) + [{"piece": c["iid"], "qform": c["qform"], "stage": "merge-check",
                                           "text": c["text"], "reason": why} for c, why in dropped]
    lexo = {"family": F,
            "sems": [{"sem_id": question_sem(F, q), "kind": "question", "meaning": DN.QUESTION_SEM_MEANING[q]}
                     for q in FORMS],
            "forms": [{"form_id": c["form_id"], "sem_id": question_sem(F, c["qform"]), "text": c["text"],
                       "slots": slots_of(c["text"]), "source": "haiku", "family": F, "haiku_task_id": c["task_id"],
                       "haiku_prompt_sha": c["prompt_sha"], "held_out": False, "extractions": c["extractions"]}
                      for c in kept]}
    words = {"family": F, "count": len(kept), "wordings": [wording_skin_obj(c) for c in kept]}
    files = {"lexicon_dneg.json": _dump(lexo), "wordings_dneg.json": _dump(words),
             "QUARANTINE.json": _dump({"family": F, "rows": quarantine})}
    per = {q: sum(1 for c in kept if c["qform"] == q) for q in FORMS}
    man = {"family": F, "version": VERSION, "base": "pools_v2/ (read-only, unchanged)",
           "reads": list(READS), "counts": {"admitted_per_form": per, "admitted": len(kept), "rejected": len(quarantine)},
           "min_admitted_per_form": MIN_ADMITTED_PER_FORM,
           "short": [q for q in FORMS if per[q] < MIN_ADMITTED_PER_FORM],
           "regression_checked": "every pools_v2 form admitted before is admitted after the merge",
           "g13_seed": "not run: pilot_i2/G13_PENDING.txt lists the wordings for the batch run",
           "sha256": {n: _sha(t.encode("utf-8")) for n, t in sorted(files.items())},
           **(extra or {})}
    files["MANIFEST.json"] = _dump(man)
    paths.write_files(supp, files)
    return {"manifest": man, "kept": kept, "quarantine": quarantine}


# ------------------------------------------------------------------------------------------------ loader side
def apply_supplement(pools: dict, supp: Path = SUPP) -> list:
    """Merge the supplement into a freeze_v2.load_pools() dict (registry and wording skins), in place. Returns notes.
    No supplement folder -> no change (the plugin then falls back to the plain forms). Never edits a file."""
    supp = Path(supp)
    if not (supp / "MANIFEST.json").is_file():
        return [f"no double-negation supplement at {supp}: yn_*_dneg fall back"]
    man = _read_json(supp / "MANIFEST.json")
    for name, sha in man["sha256"].items():
        if _sha((supp / name).read_bytes()) != sha:
            raise SupplementError(f"{supp / name}: sha256 differs from the supplement MANIFEST")
    lexo, words = _read_json(supp / "lexicon_dneg.json"), _read_json(supp / "wordings_dneg.json")
    lex = pools["lexicon"]
    for s in lexo["sems"]:
        lex.declare(s["sem_id"], s["kind"], s["meaning"])
    for x in lexo["forms"]:
        f = lex.add(x["text"], x["sem_id"], slots=x["slots"], source=x["source"], family=x["family"],
                    haiku_task_id=x["haiku_task_id"], haiku_prompt_sha=x["haiku_prompt_sha"], held_out=x["held_out"])
        if f.form_id != x["form_id"]:
            raise SupplementError(f"form id drift {x['form_id']} -> {f.form_id}")
        f.extractions = [tuple(e) for e in x["extractions"]]
        if not lex.unit_test(f.form_id) or lex.status(f.form_id) != "admitted":
            raise SupplementError(f"{f.form_id} is {lex.status(f.form_id)} after the merge")
    for w in words["wordings"]:
        sk = FV.skin_from_json({**w, "lexicon_ids": [w["form_id"]]})
        pools["wordings"][sk.skin_id] = sk
        pools["wording_forms"][sk.skin_id] = w["form_id"]
    return [f"double-negation supplement {supp.name}: {len(words['wordings'])} wordings, "
            f"{man['counts']['admitted_per_form']}"]


def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="T31 double-negation round: write the authoring task files")
    ap.add_argument("cmd", choices=("write-tasks", "check"))
    ap.add_argument("--root", default=str(ROOT))
    a = ap.parse_args(argv)
    if a.cmd == "check":
        files, man = author_files(Path(a.root))
        print(json.dumps({"n_tasks": man["n_tasks"], "items": man["items_expected"], "files": len(files)}))
        return 0
    man = write_author(Path(a.root))
    print(json.dumps({"written_to": a.root, "n_tasks": man["n_tasks"], "items_expected": man["items_expected"],
                      "tasks": [t["task_file"] for t in man["tasks"]], "answers": [t["answer_file"] for t in man["tasks"]]},
                     indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

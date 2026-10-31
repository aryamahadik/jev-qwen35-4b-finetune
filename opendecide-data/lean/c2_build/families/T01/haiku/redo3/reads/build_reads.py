"""families/T01/haiku/redo3/reads/build_reads.py: the T01 redo3 G-LEX read tasks (G0_SPEC.md v3, H42-H47).

Run after the redo3 answers returned. Reads the six redo3 answer files (validated whole against their contracts), runs the
family's own lint / dedup on every newly AUTHORED piece, and builds read tasks only for the pieces that need a read.
Nothing existing is edited, no answer is written here, Haiku never sees a gold, an option or a row. Every write goes
through c2_kit.paths.write_files (refuses before A38).

What needs a read (G0_SPEC section 7, redo3 INGEST, H45, H47):
  skins            none. A skin is gated by G-SL + the family check (haiku_author.check_skin); there is no G-LEX or G3-H read
  window clauses   win.later_anchor / win.wait_after that pass check_lexicon, the clause lint (flags only) and the unit test:
                   THREE independent G-LEX reads glex-r1 / -r2 / -r3 (3/3; other filled instance and other choice order in
                   each) and THEN the three H45 confirmation reads glex-r1b / -r2b / -r3b (realistic fills). A form is used
                   only when all six pick its sem. The six reads are built together: they do not depend on each other's
                   answers (a clause one read rejects is rejected for good; the other reads on it are then moot).
  backup notes     none while both pending notes match: g3h.compare(plan g3h_expect, redo3 answer) on t01r2.free.email.031a
                   and t01r2.free.memo.070a. If a pending note ever fails to match, a G3-H read of the passing backup notes
                   is the next step (see main()'s "backup_notes_needed")

Run from lean/c2_build:
  ../.venv/bin/python -B families/T01/haiku/redo3/reads/build_reads.py            (dry run: counts, writes nothing)
  ../.venv/bin/python -B families/T01/haiku/redo3/reads/build_reads.py --write    (writes tasks/, chunks/, key/, plan/ ...)
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import hashlib  # noqa: E402
import importlib.util  # noqa: E402
import json  # noqa: E402
from collections import Counter, defaultdict  # noqa: E402
from pathlib import Path  # noqa: E402

ROOT = Path(__file__).resolve().parent                     # families/T01/haiku/redo3/reads
REDO3 = ROOT.parent                                        # families/T01/haiku/redo3
T01_DIR = REDO3.parents[1]                                 # families/T01
C2_BUILD = T01_DIR.parents[1]                              # lean/c2_build
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, g3h, paths  # noqa: E402
from c2_kit import lexicon as LX  # noqa: E402
from families.T01 import extract as E  # noqa: E402
from families.T01 import freeze_v2 as FZ  # noqa: E402
from families.T01 import haiku_author as A  # noqa: E402
from families.T01 import plugin as P  # noqa: E402

FAMILY = "T01"
VERSION = "redo3-reads-v1"
POOLS_V2 = T01_DIR / "pools_v2"
REDO2 = T01_DIR / "haiku" / "redo2"
BATCH_LEX = "T01-author_lexicon-4f479381"
BATCH_G3H = "T01-extract_g3h-d8f4b7aa"
READS_INDEPENDENT = ("glex-r1", "glex-r2", "glex-r3")      # 3/3 for window rules (c2_kit.lexicon STRICT_KINDS)
READS_CONFIRM = ("glex-r1b", "glex-r2b", "glex-r3b")       # H45
LEX_CHUNK = 25
MAX_TASKS = 8


def _jsonl(path: Path) -> list:
    paths.check_path(path)
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def _load_redo2():
    spec = importlib.util.spec_from_file_location("t01_build_redo2", REDO2 / "build_redo2.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ------------------------------------------------------------------------------------------------ answers
def load_batch(batch_id: str) -> dict:
    """The redo3 answers of one batch, each file validated whole against its contract (freeze_v2.validate_answer).
    -> {"answers": {internal id: answer}, "task_of": {internal id: task id}, "plan", "prompt_sha", "files": [records]}"""
    man = json.loads(paths.check_path(REDO3 / "TASKS.json").read_text(encoding="utf-8"))
    key = json.loads(paths.check_path(REDO3 / "key" / f"{batch_id}.json").read_text(encoding="utf-8"))["key"]
    plan = json.loads(paths.check_path(REDO3 / "plan" / f"{batch_id}.json").read_text(encoding="utf-8"))["plan"]
    psha = json.loads(paths.check_path(REDO3 / "manifest" / f"{batch_id}.json").read_text(encoding="utf-8"))["prompt_sha"]
    out = {"answers": {}, "task_of": {}, "plan": plan, "prompt_sha": psha, "files": []}
    for t in man["tasks"]:
        if t["batch_id"] != batch_id:
            continue
        chunk = json.loads(paths.check_path(REDO3 / "chunks" / f"{t['task_id']}.json").read_text(encoding="utf-8"))
        items = {it["qid"]: it for it in chunk["items"]}
        data = paths.check_path(t["answer_file"]).read_bytes()
        ans, probs = FZ.validate_answer(t["kind"], data, items)
        out["files"].append({"task_id": t["task_id"], "kind": t["kind"], "valid": ans is not None, "problems": probs,
                             "n_answered": len(ans or {}), "sha256": hashlib.sha256(data).hexdigest()})
        if ans is None:
            continue
        for q, a in ans.items():
            out["answers"][key[q]] = a
            out["task_of"][key[q]] = t["task_id"]
    return out


# ------------------------------------------------------------------------------------------------ the checks
def window_clauses() -> dict:
    """Family lint + dedup of the 11 newly authored window clauses: haiku_author.check_lexicon ('seen' seeded with every
    window text of pools_v2), extract.lint_clause (G-SL flags; logged, never a drop, as extract.lint_all) and the
    normalised-text dedup (extract.dedup_all)."""
    b = load_batch(BATCH_LEX)
    seen = {r["text"].lower() for r in _jsonl(POOLS_V2 / "windows.jsonl")}
    kept, drops = [], []
    for iid in sorted(b["answers"]):
        meta = b["plan"][iid]
        obj, reasons = A.check_lexicon(iid, b["answers"][iid]["text"], meta, b["task_of"][iid], b["prompt_sha"], seen)
        if reasons:
            drops.append({"pid": iid, "reasons": reasons})
            continue
        sem, _kind, text, slots, tid, psha = obj
        p = {"pid": iid, "group": "windows", "task_id": tid, "prompt_sha": psha, "held_out": False, "text": text,
             "lexkind": "window", "sem": sem, "slots": slots}
        p["gsl_flags"] = E.lint_clause(p)
        kept.append(p)
    surv, dups = E.dedup_all({"windows": kept})
    return {"kept": surv["windows"], "drops": drops + dups, "files": b["files"], "authored": len(b["answers"])}


def all_answer_files() -> list:
    """The validation record of every redo3 answer file (six tasks, four batches)."""
    man = json.loads(paths.check_path(REDO3 / "TASKS.json").read_text(encoding="utf-8"))
    out = []
    for bid in sorted({t["batch_id"] for t in man["tasks"]}):
        out += load_batch(bid)["files"]
    return out


def pending_notes_check() -> dict:
    """g3h.compare(plan g3h_expect, the redo3 g3h-r1 answer) for the two notes that waited for a read."""
    pend = _jsonl(POOLS_V2 / "documents_pending_g3h.jsonl")
    b = load_batch(BATCH_G3H)
    fields = E._g3h_fields()
    res = {}
    for p in pend:
        a = b["answers"].get(p["pid"])
        if a is None:
            res[p["pid"]] = {"match": None, "diffs": ["unanswered"]}
            continue
        ok, d = g3h.compare(p["g3h_expect"], a, fields)
        res[p["pid"]] = {"match": bool(ok), "diffs": list(d)}
    return res


# ------------------------------------------------------------------------------------------------ registry and reads
def registry_with(kept: list):
    """The pools_v2 registry (every vote it holds) plus the new clauses as Haiku forms with NO votes, unit-tested."""
    reg = LX.LexiconRegistry.from_json(json.loads(paths.check_path(POOLS_V2 / "lexicon_registry.json")
                                                  .read_text(encoding="utf-8")))
    n_before = len(reg.forms)
    row_of, drops = {}, []
    for p in kept:
        try:
            f = reg.add(p["text"], p["sem"], slots=p["slots"], source="haiku", family=FAMILY,
                        haiku_task_id=p["task_id"], haiku_prompt_sha=p["prompt_sha"])
            row_of[f.form_id] = p
        except LX.LexiconError as e:
            drops.append({"pid": p["pid"], "reasons": [f"form: {e}"]})
    for fid in row_of:
        reg.unit_test(fid)
    for fid, p in list(row_of.items()):
        if not reg.forms[fid].unit_ok:
            drops.append({"pid": p["pid"], "reasons": [f"unit: {x}" for x in reg.forms[fid].unit_problems[:3]]})
            del row_of[fid]
    return reg, row_of, drops, n_before


def read_batches(reg, row_of: dict) -> list:
    """[(read name, batch, plan)] for the six reads of the new window forms."""
    r2 = _load_redo2()
    packs = _jsonl(POOLS_V2 / "packs.jsonl")
    people = sorted({n for p in packs for n in p["pack"]["people"]})
    actions = sorted({p["pack"]["filing"]["action"] for p in packs})
    perils = sorted({x for p in packs for x in p["pack"]["perils"]})
    ids = sorted(row_of)
    out = []
    for instance, read in enumerate(READS_INDEPENDENT + READS_CONFIRM):
        seed = f"t01-{VERSION}-{read}"
        if read in READS_INDEPENDENT:
            items = E.glex_items(reg, ids, seed, instance)
            plan = {}
            for fid, it in items:
                plan[fid] = {"read": read, "kind": reg.forms[fid].kind, "sem_id": reg.forms[fid].sem_id,
                             "filled": it["text"]}
        else:
            items, plan = [], {}
            for fid in ids:
                f = reg.forms[fid]
                vals, forms = r2.realistic_values(reg, fid, read, people, actions, perils)
                txt = reg.render(fid, vals, forms)
                mean = sorted((s.meaning for s in reg.sems.values() if s.kind == f.kind),
                              key=lambda m: hashlib.sha256(f"{seed}|{fid}|{m}".encode()).hexdigest())
                items.append((fid, {"text": txt, "choices": mean}))
                plan[fid] = {"read": read, "kind": f.kind, "sem_id": f.sem_id, "filled": txt}
        b = chunker.make_batch("extract_lex", FAMILY, items, seed=seed, prompt=E.GLEX_PROMPT, max_items=LEX_CHUNK)
        out.append((read, b, plan))
    return out


# ------------------------------------------------------------------------------------------------ task files
SHAPE = '{"qid": "<the item\'s qid>", "meaning": "<the chosen choice, copied exactly>"}'
EXAMPLE = [{"qid": "qEXAMPLE0001", "meaning": "<one of the CHOICES of that item, copied character for character>"}]


def task_text(b, chunk: dict, label: str, task_file: Path, answer_file: Path) -> str:
    n = len(chunk["items"])
    items = "\n".join(json.dumps(it, ensure_ascii=False) for it in chunk["items"])
    return "\n".join([
        f"REDO3 READ TASK {chunk['task_id']}  (family {FAMILY}, kind {b.kind}, read {label}, {n} items)", "",
        "This one text file is your whole task. Read all of it, then write the answer file, then stop.",
        "Do not open, list, search or write any other file or folder. Create no other file. Do not put the answer in "
        "chat;", "when the answer file is written, reply with the single word DONE.", "",
        f"TASK FILE (this file)                 : {task_file}",
        f"ANSWER FILE (write exactly this path) : {answer_file}", "",
        "=== ANSWER CONTRACT (exact) ===",
        "Write ONE JSON array to the ANSWER FILE with the Write tool, and nothing else in that file: no markdown fence, "
        "no", "comment, no wrapper object, no extra text before or after the array.",
        f"- The array has exactly {n} objects, one for each of the {n} items below, every qid exactly once (any order).",
        "- Each object has exactly these keys and no others: 'qid', 'meaning'.",
        "- \"qid\": the item's qid, copied character for character. It is an opaque label; read nothing into it.",
        "- \"meaning\": ONE of that item's own CHOICES, copied character for character (never a new meaning, never a "
        "choice of another item).",
        "- Inside a JSON string write a double quote as \\\" and a line break as \\n. Valid JSON only.",
        "- Not allowed: any other key (such as \"note\", \"reason\" or \"confidence\"); a skipped qid; a qid used "
        "twice; a qid", "  that is not in the items below.",
        f"Shape of one object: {SHAPE}",
        "Literal example of the required shape (EXAMPLE ONLY: it is not an item; your array has "
        f"{n} objects):", "[\n  " + json.dumps(EXAMPLE[0], ensure_ascii=False) + "\n]", "",
        "=== INSTRUCTIONS ===", b.prompt.rstrip(), "",
        f"=== ITEMS ({n}; one JSON object per line; every item needs one answer object carrying its qid) ===", items, ""])


INGEST = {
    "audit": "audit.audit_jsonl per agent transcript with the task's audit_allowed_read / audit_allowed_write; a failed "
             "audit discards that agent's answers.",
    "record": "Rebuild the registry exactly as build_reads.registry_with() does (pools_v2 registry + the 'new_forms' of "
              "TASKS.json, each with its haiku_task_id and haiku_prompt_sha). For every valid answer: reg.record_extraction("
              "form_id, read, reg.meaning_to_sem('window', meaning)) (form_id = the item's key/<batch_id>.json entry; an "
              "answer that is not one of the item's choices records None and rejects); the item text must equal the "
              "plan's 'filled'. G-LEX: reg.status(form_id) == 'admitted' needs glex-r1, -r2, -r3 all on the declared sem "
              "(3/3). H45: a form is USED only if it is admitted AND has glex-r1b, -r2b, -r3b all on the declared sem; "
              "one other pick rejects it for good. A missing answer leaves the form unused, never admitted.",
    "windows": "Kept forms add to pools_v2 windows (win.later_anchor 10 + new, win.wait_after 11 + new; target 14 each, "
               "asked 6 + 5). Surplus admitted forms beyond the target are not needed.",
    "skins": "No read. haiku_author.check_skin per piece (redo3 INGEST).",
    "freeform_backup": "No read while both pending notes match (g3h.compare). Otherwise: check_freeform on the backup notes "
                       "and one g3h-r1 read of the passing ones.",
    "freeze": "freeze_v2.py ingests author, extract, redo and redo2 only; a redo3 loader (answers + these reads) is still "
              "to be added before the next freeze.",
}


def build() -> dict:
    wc = window_clauses()
    reg, row_of, form_drops, n_before = registry_with(wc["kept"])
    batches = read_batches(reg, row_of)
    files, tasks, plans = {}, [], {}
    for read, b, plan in batches:
        files.update(b.files())
        meta = {fid: dict(v) for fid, v in plan.items()}
        files[f"plan/{b.batch_id}.json"] = json.dumps({"batch_id": b.batch_id, "label": read, "kind": b.kind,
                                                       "plan": meta}, indent=1, sort_keys=True,
                                                      ensure_ascii=False) + "\n"
        plans[read] = meta
        for c in b.chunks:
            tid = c["task_id"]
            tf, af = ROOT / "tasks" / f"{tid}.txt", ROOT / b.answer_path(tid)
            files[f"tasks/{tid}.txt"] = task_text(b, c, read, tf, af)
            tasks.append({"task_file": str(tf), "answer_file": str(af), "read": read, "kind": b.kind,
                          "stage": "extract", "batch_id": b.batch_id, "task_id": tid, "n_items": len(c["items"]),
                          "outputs_expected": len(c["items"]), "prompt_sha": b.prompt_sha,
                          "audit_allowed_read": [str(tf)], "audit_allowed_write": [str(af)]})
    for t in tasks:
        for p in (t["task_file"], t["answer_file"]):
            if paths.never_open(p):
                raise SystemExit(f"never-open path in the task list: {p}")
    if len(tasks) > MAX_TASKS:
        raise SystemExit(f"{len(tasks)} tasks; at most {MAX_TASKS} are allowed")
    new_forms = [{"form_id": fid, "pid": p["pid"], "sem": p["sem"], "text": p["text"], "slots": p["slots"],
                  "haiku_task_id": p["task_id"], "haiku_prompt_sha": p["prompt_sha"], "gsl_flags": p["gsl_flags"]}
                 for fid, p in sorted(row_of.items())]
    return {"files": files, "tasks": tasks, "wc": wc, "form_drops": form_drops, "new_forms": new_forms,
            "registry_forms_before": n_before, "registry_sha256_before": None, "reg": reg}


def main(argv: list) -> int:
    res = build()
    notes = pending_notes_check()
    wc = res["wc"]
    summary = {
        "tasks": len(res["tasks"]), "tasks_by_read": dict(Counter(t["read"] for t in res["tasks"])),
        "items_per_task": {t["read"]: t["n_items"] for t in res["tasks"]},
        "redo3_answer_files": dict(Counter(f"{f['kind']}:{'valid' if f['valid'] else 'INVALID'}"
                                           for f in all_answer_files())),
        "windows_authored": wc["authored"], "windows_check_drops": wc["drops"],
        "new_forms_by_sem": dict(Counter(f["sem"] for f in res["new_forms"])), "form_drops": res["form_drops"],
        "clause_gsl_flags": {f["form_id"]: f["gsl_flags"] for f in res["new_forms"] if f["gsl_flags"]},
        "pending_notes_g3h": notes,
        "backup_notes_needed": any(v["match"] is not True for v in notes.values()),
    }
    print(json.dumps(summary, indent=1, ensure_ascii=False))
    if "--write" in argv:
        if summary["backup_notes_needed"]:
            raise SystemExit("a pending note does not match: backup-note reads are needed; this builder does not cover them")
        man = {"family": FAMILY, "version": VERSION, "g0_sha256": P.T01.G0_SHA256, "n_tasks": len(res["tasks"]),
               "outputs_expected": sum(t["outputs_expected"] for t in res["tasks"]),
               "builder": str(Path(__file__).resolve()),
               "builder_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               "source_answers_sha256": {f["task_id"]: f["sha256"] for f in wc["files"]},
               "pools_v2_registry_forms": res["registry_forms_before"],
               "new_forms": res["new_forms"], "ingest": INGEST, "tasks": res["tasks"]}
        res["files"]["TASKS.json"] = json.dumps(man, indent=1, ensure_ascii=False) + "\n"
        res["files"]["answers/README.txt"] = ("Haiku answer files: one <task_id>.json per read task (see ../TASKS.json). "
                                              "Written only by the task agents.\n")
        paths.write_files(ROOT, res["files"])
        print(f"written under {ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

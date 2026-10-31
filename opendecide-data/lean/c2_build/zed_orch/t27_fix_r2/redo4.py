"""zed_orch/t27_fix_r2/redo4.py: new TRAINING wordings of the choice question form ch_next for the T27 G11 fix round
(PREREG A52 d; diagnosis: diag_g11.py). Same flow, checks and Haiku task format as families/T27/redo2.py (the yn_dneg_beyond
supplement), nothing in families/T27 is edited or written. Haiku writes text only; nothing here sets a label.

Why. After the G13-seed and G5-H quarantines T27 has 17 usable ch_next training wordings for 1,256 of 2,401 candidate rows
(3.08% each even when perfectly balanced; G11 bar 2%). Even at the largest allowed yes/no share (55%) 23 are needed; for a
margin under G13 unit drops and a second G5-H quarantine the plan asks for 24 new ones (about 19 survive the family lint,
the seeded 15% held-out split and 2/2 G-LEX; held-out ones are NOT admitted: they would change mixdev_S5.jsonl).

  redo4.py tasks            in memory: the authoring task (task_file, answer_file)
  redo4.py write            write haiku_r4/ (once): chunk, prompt, key, manifest, <task_id>.txt, TASKS.json
  redo4.py load [--write]   lint the answer (authoring.lint_piece + merge vs the frozen pools); --write: haiku_r4/linted.json
  redo4.py glex-plan        in memory: the 2 G-LEX reads (needs haiku_r4/linted.json)
  redo4.py glex-write       write them under haiku_r4/extract/ (once)
  redo4.py glex-check [--record]   judge the 2 reads; --record: haiku_r4/extract/record/VALIDATION.json and, when both
                            reads are valid, admitted_wordings.json (what overlay.py / merge_pools.py add to the pools)
Run from lean/c2_build with ../../.venv/bin/python -B zed_orch/t27_fix_r2/redo4.py <step>. No model is run here.

SUPERSEDED (16 Oct 2026, review of the G11 fix round): redo5.py asks 24 ch_next AND 8 yn_beyond training wordings in ONE
task file (yn_beyond has 13 wordings for ~523 rows, floor 12; three G5-H losses would fail G11 again with no round left).
The module stays importable (redo5.py and the tests reuse its helpers), but its CLI no longer writes anything: the
write commands (write, glex-write, glex-check --record) are refused so admitted_wordings.json (written once) can only
come from redo5.py. haiku_r4/ is not used.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2 = HERE.parents[1]
if str(C2) not in sys.path:
    sys.path.insert(0, str(C2))
sys.dont_write_bytecode = True

from c2_kit import chunker, paths  # noqa: E402

from families.T27 import authoring as A  # noqa: E402
from families.T27 import extract_check as E  # noqa: E402
from families.T27 import glex_build as G  # noqa: E402
from families.T27 import redo2 as R2  # noqa: E402

FAMILY = A.FAMILY
STAGE = HERE
ROOT = HERE / "haiku_r4"
GLEX_ROOT = ROOT / "extract"
POOLS = C2 / "families" / "T27" / "pools_v2"
ADMITTED = HERE / "admitted_wordings.json"
SEED = "T27-author-redo4-v1"
GLEX_SEED = "T27-glex-redo4"
READS = ("read1", "read2")
N_CH = 24                                                       # ch_next wordings asked (see the module docstring)
CONTROLS = {"yn_not_beyond": 8, "yn_beyond": 6, "yn_within": 4, "ch_next": 4}      # as redo2: report only, never recorded
MAX_ITEMS = G.GROUP                                             # 50 items per read file
ROUND = "redo4"
SUPERSEDED = ("redo4.py is superseded by redo5.py (24 ch_next + 8 yn_beyond wordings in one authoring task): its write "
              "commands are refused. Run: ../../.venv/bin/python -B zed_orch/t27_fix_r2/redo5.py <step>")
PROMPT = R2.PROMPT


# ------------------------------------------------------------------------------------------------ authoring task

def _ch_item(n: int) -> dict:
    it = A._wording_item("ch_next", n)
    rules = list(it["rules"])
    rules.insert(2, "You may vary how the ask itself is worded ('which step', 'what step', 'what should the assistant do "
                    "here', 'what is the right step for the assistant'), as long as the question asks only for the step "
                    "the assistant should take and names no possible step.")
    rules.append(f"Make the {n} questions clearly different from each other: vary the opening, how the opened content is "
                 "named (page, message, e-mail, document, file, sheet, tool output, ticket, invite, report and the like), "
                 "how the user's job is named (job, work, request, task, goal), and the sentence pattern. No two questions "
                 "may share the same first six words.")
    it["rules"] = rules
    return it


def task_defs() -> list:
    return [{"name": "wordings_ch_next_redo4", "kind": "author_wording", "pool": "wording",
             "items": [("wording|ch_next", _ch_item(N_CH))]}]


def build_batches(root: Path = ROOT) -> list:
    out = []
    forbid = A.forbid_strings()
    for td in task_defs():
        seed = f"{SEED}|{td['name']}"
        b0 = chunker.make_batch(td["kind"], FAMILY, [(i, A._with_path(it, "PENDING")) for i, it in td["items"]],
                                seed=seed, prompt=PROMPT, forbid_strings=forbid)
        tid = b0.chunks[0]["task_id"]
        answer = str(Path(root) / b0.answer_path(tid))
        b = chunker.make_batch(td["kind"], FAMILY, [(i, A._with_path(it, answer)) for i, it in td["items"]],
                               seed=seed, prompt=PROMPT, forbid_strings=forbid)
        if len(b.chunks) != 1 or b.chunks[0]["task_id"] != tid:
            raise chunker.ChunkError(f"{td['name']}: one chunk per task, stable task id")
        out.append((td, b))
    return out


def author_txt(td: dict, b, root: Path = ROOT) -> str:
    return R2.author_txt(td, b, root).replace("(REDO2)", "(REDO4)")


def task_index(batches: list, root: Path = ROOT) -> list:
    return R2.task_index(batches, root)


def write_tasks(root: Path = ROOT) -> list:
    root = Path(root)
    if (root / "TASKS.json").exists():
        raise FileExistsError(f"{root}/TASKS.json exists: the redo4 authoring task is written once")
    batches = build_batches(root)
    for td, b in batches:
        files = dict(b.files())
        files[R2._txt_path(root, b.chunks[0]["task_id"]).name] = author_txt(td, b, root)
        paths.write_files(root, files)
    idx = task_index(batches, root)
    paths.write_json(root / "TASKS.json", {
        "family": FAMILY, "seed": SEED, "stage": "redo4 (G11 fix round 2: ch_next training wordings)",
        "prompt_sha": chunker.sha(PROMPT), "n_asked": N_CH,
        "g0_sha256": hashlib.sha256((C2 / "families" / "T27" / "G0_SPEC.md").read_bytes()).hexdigest(), "tasks": idx})
    return idx


# ------------------------------------------------------------------------------------------------ the frozen pools

def pool_wordings() -> list:
    d = json.loads((POOLS / "wordings.json").read_text(encoding="utf-8"))
    return d["records"]


def pool_lexicon() -> dict:
    return json.loads((POOLS / "lexicon.json").read_text(encoding="utf-8"))


def _is_lex_text(text: str, lex: dict) -> set:
    t = A._norm(text)
    return {f["sem_id"] for f in lex["forms"] if A._norm(f["text"]) == t}


# ------------------------------------------------------------------------------------------------ load and merge

def merge(kept: dict, dropped: list) -> tuple:
    """(kept, dropped + extra drops). Only ch_next wordings; a text equal to a frozen wording or to any frozen lexicon form
    (of any meaning) is dropped, and the family lint (authoring.lint_wording, run by authoring.load) is unchanged."""
    lex = pool_lexicon()
    have = {A._norm(r["text"]) for r in pool_wordings()}
    out_k, out_d = {}, list(dropped)
    for pool, ps in kept.items():
        for p in ps:
            why = []
            if pool != "wording" or p.get("qform") != "ch_next":
                why.append("not a redo4 pool")
            if A._norm(p["text"]) in have:
                why.append("duplicate of a frozen wording")
            other = _is_lex_text(p["text"], lex) - {p["sem"]}
            if other:
                why.append("the same text is a frozen form with another meaning")
            if why:
                out_d.append({**p, "why": why})
            else:
                out_k.setdefault(pool, []).append(p)
    return out_k, out_d


def split_held(kept: dict) -> tuple:
    """(training pieces, held-out pieces) by the family's seeded 15% rule (authoring.held_out_wording)."""
    tr = [p for p in kept.get("wording", []) if not A.held_out_wording(p["piece_id"])]
    ho = [p for p in kept.get("wording", []) if A.held_out_wording(p["piece_id"])]
    return tr, ho


def load(root: Path = ROOT, answers: dict | None = None, batches: list | None = None) -> dict:
    rep = A.load(root, answers=answers, batches=batches)
    kept, dropped = merge(rep["kept"], rep["dropped"])
    tr, ho = split_held(kept)
    n_have = sum(1 for r in pool_wordings() if r["qform"] == "ch_next" and not r["held_out"])
    counts = {"asked": N_CH, "kept_after_lint_and_merge": len(kept.get("wording", [])), "training": len(tr),
              "held_out_not_admitted": len(ho), "dropped": len(dropped),
              "frozen_ch_next_training_wordings": n_have}
    return {"kept": kept, "dropped": dropped, "problems": rep["problems"], "counts": counts,
            "training": [p["piece_id"] for p in tr], "held_out": [p["piece_id"] for p in ho]}


def kept_from_disk(root: Path = ROOT) -> dict:
    return json.loads((Path(root) / "linted.json").read_text(encoding="utf-8"))["kept"]


# ------------------------------------------------------------------------------------------------ G-LEX reads

def glex_plan(kept: dict | None = None) -> dict:
    """The 2 G-LEX reads: the new TRAINING ch_next wordings (recorded) plus seeded control wordings of the frozen pool (not
    recorded), one chunk per read, the same closed list and read format as redo2.glex_plan."""
    kept = kept_from_disk() if kept is None else kept
    tests_p, _ho = split_held(kept)
    main = {"wording": pool_wordings()}
    reg = A.registry({"wording": list(main["wording"]) + tests_p})
    form_of = {reg.forms[f].text: f for f in reg.forms}
    test_ids = sorted(form_of[p["text"]] for p in tests_p if reg.forms[form_of[p["text"]]].unit_ok)
    unit_failed = sorted(form_of[p["text"]] for p in tests_p if not reg.forms[form_of[p["text"]]].unit_ok)
    if not test_ids:
        raise ValueError("no unit-tested ch_next wording to read")
    room = max(0, MAX_ITEMS - len(test_ids))
    controls = []
    for q, n in CONTROLS.items():
        pool = sorted((form_of[p["text"]] for p in main["wording"] if p["qform"] == q),
                      key=lambda f: hashlib.sha256(f"{GLEX_SEED}|control|{f}".encode()).hexdigest())
        controls += pool[:n]
    controls = sorted(controls, key=lambda f: hashlib.sha256(f"{GLEX_SEED}|trim|{f}".encode()).hexdigest())[:room]
    meanings = sorted(s.meaning for s in reg.sems.values() if s.kind == "question")
    batches = []
    for read in READS:
        seed = f"{GLEX_SEED}-{read}-question-00"
        order = sorted(meanings, key=lambda m: hashlib.sha256(f"{seed}|{m}".encode()).hexdigest())
        items = [(fid, {"text": it["text"]}) for fid, it in A.lex_items(reg, test_ids + sorted(controls), seed=seed)]
        b = chunker.make_batch("extract_lex", FAMILY, items, seed=seed, prompt=G.group_prompt(order), max_items=MAX_ITEMS)
        if len(b.chunks) != 1:
            raise chunker.ChunkError(f"{seed}: one chunk per read")
        batches.append((read, b))
    return {"reg": reg, "tests": test_ids, "controls": sorted(controls), "unit_failed": unit_failed,
            "batches": batches, "test_pieces": {form_of[p["text"]]: p for p in tests_p}}


def glex_txt(b, root: Path = GLEX_ROOT) -> str:
    return R2.glex_txt(b, root).replace("(REDO2)", "(REDO4)")


def glex_write(root: Path = GLEX_ROOT, kept: dict | None = None) -> list:
    root = Path(root)
    if (root / "TASKS.json").exists():
        raise FileExistsError(f"{root}/TASKS.json exists: the redo4 G-LEX reads are written once")
    p = glex_plan(kept)
    tasks = []
    for read, b in p["batches"]:
        tid = b.chunks[0]["task_id"]
        files = dict(b.files())
        files[R2._txt_path(root, tid).name] = glex_txt(b, root)
        paths.write_files(root, files)
        tasks.append({"read": read, "kind": "question", "batch_id": b.batch_id, "task_id": tid,
                      "task_file": str(R2._txt_path(root, tid)), "answer_file": str(root / b.answer_path(tid)),
                      "n_items": len(b.key), "prompt_sha": b.prompt_sha})
    reg = p["reg"]
    paths.write_json(root / "TASKS.json", {
        "family": FAMILY, "gate": "G-LEX 2/2 (redo4: ch_next training wordings)", "reads": list(READS), "tasks": tasks,
        "test_forms": {f: reg.forms[f].sem_id for f in p["tests"]},
        "control_forms": {f: reg.forms[f].sem_id for f in p["controls"]}, "unit_failed": p["unit_failed"],
        "rule": "only test forms are recorded; controls are report-only (they are admitted by the frozen reads)"})
    return tasks


def _read_answer(b, reg, root: Path):
    tid = b.chunks[0]["task_id"]
    path = Path(root) / b.answer_path(tid)
    if not path.is_file():
        return "missing", ["no answer file"], {}, None
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        return "malformed", [f"not valid JSON ({type(e).__name__})"], {}, path
    st, why, got = E.judge(b, E.closed_list(reg, "question"), raw)
    return st, why, got, path


def glex_check(root: Path = GLEX_ROOT, p: dict | None = None) -> dict:
    """Judge the 2 reads (extract_check.judge: a malformed or missing read is never recorded), record the valid reads for the
    test forms only, report admission and control agreement."""
    root = Path(root)
    p = glex_plan() if p is None else p
    reg, tests = p["reg"], set(p["tests"])
    file_probs, rows = [], []
    for read, b in p["batches"]:
        tid = b.chunks[0]["task_id"]
        for rel, text in sorted(dict(b.files(), **{R2._txt_path(root, tid).name: glex_txt(b, root)}).items()):
            f = root / rel
            if not f.is_file() or f.read_text(encoding="utf-8") != text:
                file_probs.append(f"{b.batch_id}: {rel} differs from the rebuilt file")
        st, why, got, path = _read_answer(b, reg, root)
        ctrl_ok = ctrl_n = 0
        if st == "valid":
            for fid, meaning in sorted(got.items()):
                sem = reg.meaning_to_sem("question", meaning)
                if fid in tests:
                    reg.record_extraction(fid, f"{ROUND}-{read}:{tid}", sem)
                else:
                    ctrl_n += 1
                    ctrl_ok += sem == reg.forms[fid].sem_id
        rows.append({"read": read, "task_id": tid, "status": st, "reasons": why, "n_items": len(b.key),
                     "controls_agree": f"{ctrl_ok}/{ctrl_n}" if st == "valid" else None,
                     "answer_sha256": hashlib.sha256(path.read_bytes()).hexdigest() if path else None})
    status = {f: reg.status(f) for f in sorted(tests)}
    admitted = sorted(f for f, s in status.items() if s == "admitted")
    ok = not file_probs and all(r["status"] == "valid" for r in rows)
    return {"family": FAMILY, "gate": "G-LEX 2/2 (redo4)", "file_problems": file_probs, "tasks": rows, "forms": status,
            "admitted": admitted, "unit_failed": p["unit_failed"], "complete": ok,
            "status": ("COMPLETE: both reads valid; " if ok else "INCOMPLETE: ")
            + f"{len(admitted)}/{len(tests)} ch_next wordings admitted", "no_labels_set": True, "no_rows_generated": True}


def admitted_payload(p: dict, rep: dict) -> dict:
    """The records overlay.py / merge_pools.py add to the frozen pools, in exactly the shapes of pools_v2/wordings.json and
    pools_v2/lexicon.json (forms from LexiconRegistry.to_json, so status and votes are the registry's own)."""
    reg = p["reg"]
    fj = {f["form_id"]: f for f in reg.to_json()["forms"]}
    wordings, forms = [], []
    for fid in rep["admitted"]:
        pc = p["test_pieces"][fid]
        f = reg.forms[fid]
        wordings.append({"extractions": [list(e) for e in f.extractions], "form_id": fid, "held_out": False,
                         "piece_id": pc["piece_id"], "pool": "wording", "prompt_sha": pc["prompt_sha"],
                         "qform": "ch_next", "round": ROUND, "sem": f.sem_id, "sem_id": f.sem_id,
                         "task_id": pc["task_id"], "text": pc["text"]})
        forms.append(fj[fid])
    return {"family": FAMILY, "round": ROUND, "wordings": wordings, "forms": forms,
            "pools_sha256": {n: hashlib.sha256((POOLS / n).read_bytes()).hexdigest()
                             for n in ("wordings.json", "lexicon.json")},
            "n_admitted": len(wordings)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="redo4")
    ap.add_argument("cmd", choices=("tasks", "write", "load", "glex-plan", "glex-write", "glex-check"))
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--record", action="store_true")
    a = ap.parse_args(argv)
    if a.cmd in ("write", "glex-write") or (a.cmd == "glex-check" and a.record):
        raise SystemExit(SUPERSEDED)
    if a.cmd == "tasks":
        print(json.dumps(task_index(build_batches(ROOT), ROOT), indent=1))
    elif a.cmd == "write":
        print(json.dumps([{"task_file": R2._txt_path(ROOT, t["task_id"]).as_posix(), "answer_file": t["answer_file"],
                           "kind": t["kind"]} for t in write_tasks(ROOT)], indent=1))
    elif a.cmd == "load":
        rep = load(ROOT)
        print(json.dumps({"counts": rep["counts"], "problems": rep["problems"],
                          "drop_reasons": A._reason_counts(rep["dropped"])}, indent=1))
        if a.write:
            paths.write_json(ROOT / "linted.json", {"family": FAMILY, "stage": ROUND, "kept": rep["kept"],
                                                    "dropped": rep["dropped"], "counts": rep["counts"],
                                                    "training": rep["training"], "held_out": rep["held_out"]})
    elif a.cmd == "glex-plan":
        p = glex_plan()
        print(json.dumps({"tests": len(p["tests"]), "controls": len(p["controls"]), "unit_failed": p["unit_failed"],
                          "reads": [{"read": r, "task_id": b.chunks[0]["task_id"], "n_items": len(b.key)}
                                    for r, b in p["batches"]]}, indent=1))
    elif a.cmd == "glex-write":
        print(json.dumps([{"task_file": t["task_file"], "answer_file": t["answer_file"], "kind": "extract_lex",
                           "read": t["read"], "n_items": t["n_items"]} for t in glex_write(GLEX_ROOT)], indent=1))
    else:
        p = glex_plan()
        rep = glex_check(GLEX_ROOT, p)
        if a.record:
            paths.write_json(GLEX_ROOT / "record" / "VALIDATION.json", rep)
            if rep["complete"]:
                pay = admitted_payload(p, rep)
                if ADMITTED.exists():
                    raise FileExistsError(f"{ADMITTED} exists: admission is written once")
                paths.write_json(ADMITTED, pay)
        print(json.dumps(rep, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

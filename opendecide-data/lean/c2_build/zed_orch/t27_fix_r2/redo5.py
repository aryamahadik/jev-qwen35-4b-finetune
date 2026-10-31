"""zed_orch/t27_fix_r2/redo5.py: new TRAINING wordings of TWO question forms for the T27 G11 fix round (PREREG A52 d, this is
T27's one fix round): 24 of ch_next and 8 of yn_beyond, asked in ONE Haiku authoring task file. Same flow, lint, merge, G-LEX 2/2
and admission rules as redo4.py (and families/T27/redo2.py); nothing in families/T27 is edited or written. Haiku writes text only;
nothing here sets a label. redo5 supersedes redo4 (24 ch_next only): redo4's write commands are refused, haiku_r4/ is never used.

Why two forms (diag_g11.json; the reviewers' findings).
  ch_next    17 usable training wordings for 1,256 of 2,401 rows: 3.08% each even when perfectly balanced (G11 bar 2% = 48 rows).
             Floor with the balancer's worst 4-row imbalance: 29 wordings, so at least 12 new ones must survive; with the 4-6 a
             second G5-H can quarantine (template rule, > 3% disputed read rows), 18 or more.
  yn_beyond  13 usable training wordings for ~523 rows: the even split is 40.2 rows (1.68%), but 11 wordings would already sit at
             the 2% cap and 12 is the floor with the 4-row imbalance. Losing 3 of the 13 to the full-generation G5-H template rule
             would fail G11 again with no further round allowed. Eight new ones (about 5-6 survive lint, the 15% held-out split
             and 2/2 G-LEX) keep the floor with up to 5 losses.
Held-out (S5) wordings are untouched: a held-out-by-hash wording is NOT admitted here (it would change mixdev_S5.jsonl).

  redo5.py tasks            in memory: the authoring task (task_file, answer_file)
  redo5.py write            write haiku_r5/ (once): chunk, prompt, key, manifest, <task_id>.txt, TASKS.json, DISPATCH.json
  redo5.py load [--write]   lint the answer (authoring.lint_piece + merge vs the frozen pools); --write: haiku_r5/linted.json
  redo5.py glex-plan        in memory: the 2 G-LEX reads (needs haiku_r5/linted.json)
  redo5.py glex-write       write them under haiku_r5/extract/ (once)
  redo5.py glex-check [--record]   judge the 2 reads; --record: haiku_r5/extract/record/VALIDATION.json and, when both
                            reads are valid, admitted_wordings.json (what overlay.py / install_code.py add to the pools)
Run from lean/c2_build with ../../.venv/bin/python -B zed_orch/t27_fix_r2/redo5.py <step>. No model is run here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2 = HERE.parents[1]
for _p in (str(C2), str(HERE)):
    if _p not in sys.path:
        sys.path.insert(0, _p)
sys.dont_write_bytecode = True

from c2_kit import chunker, paths  # noqa: E402

import redo4 as R4  # noqa: E402  (the unchanged helpers: frozen pools, ch_next brief, held-out split, read judging)
from families.T27 import authoring as A  # noqa: E402
from families.T27 import extract_check as E  # noqa: E402
from families.T27 import glex_build as G  # noqa: E402
from families.T27 import redo2 as R2  # noqa: E402

FAMILY = A.FAMILY
STAGE = HERE
ROOT = HERE / "haiku_r5"
GLEX_ROOT = ROOT / "extract"
POOLS = R4.POOLS
ADMITTED = HERE / "admitted_wordings.json"
DIAG = HERE / "diag_g11.json"
SEED = "T27-author-redo5-v1"
GLEX_SEED = "T27-glex-redo5"
READS = R4.READS
ROUND = "redo5"
N_NEW = {"ch_next": 24, "yn_beyond": 8}              # wordings asked per question form (one item each, one task file)
CONTROLS = dict(R4.CONTROLS)                         # as redo4 / redo2: seeded frozen wordings, report only, never recorded
MAX_ITEMS = R4.MAX_ITEMS                             # 50 items per read file
PROMPT = R4.PROMPT
IMBALANCE = 4                                        # rows: the heaviest unit (wording_balance.py: max - min <= one unit)
LOSS_PLAN = {"ch_next": 6, "yn_beyond": 3}           # wordings a second G5-H template quarantine may take (report only)
TASK_NAME = "wordings_ch_next_yn_beyond_redo5"
NOT_A_REDO5_POOL = "not a redo5 pool"


# ------------------------------------------------------------------------------------------------ authoring task

def _yn_item(n: int) -> dict:
    """yn_beyond: the family brief (authoring._wording_item, unchanged) plus the rules that keep the lint, the polarity rule and
    the G-LEX read easy to meet. Rules only add instructions; the lint that judges the answer is the family's, unchanged."""
    it = A._wording_item("yn_beyond", n)
    rules = list(it["rules"])
    at = next(i for i, r in enumerate(rules) if r.startswith("Optional:"))
    extra = [
        "SHAPE: a plain yes/no question with a positive verb that asks whether the content asks the assistant for ANY action "
        "beyond the user's task, so that 'yes' means the content does ask for such an action. Open it with a helping verb "
        "('Does', 'Is', 'Would', 'Will' or 'Can') and use verbs such as 'asks for', 'requests', 'calls for', 'wants', 'expects'.",
        "Speak of what the content asks of the assistant or wants the assistant to do, never of what it asks of the user.",
        "Never use the phrases 'the request', 'its request', 'the requested', 'what the content asks', 'what it asks', "
        "'the action it asks for' or 'the action the content': they assume that an action exists. Say 'any action', 'anything' "
        "or 'something' instead.",
        "No word with a negative or reversing meaning, not even a mild one: besides not, no, never, nothing, none and n't, also "
        "without, except, unless, lack, fail, deny, refuse, prevent, avoid, false and 'other than'. Never use 'within', "
        "'inside', 'limited', 'restricted', 'confined', 'stay', 'remain' or 'keep': they turn the question around.",
        "Write the apostrophe of \"user's\" as a plain straight apostrophe, never a curly one.",
        f"Make the {n} questions clearly different from each other: vary the opening, how the opened content is named "
        "(page, message, e-mail, document, file, sheet, tool output, ticket, invite, report and the like), the verb and the "
        "sentence pattern. No two questions may share the same first six words.",
    ]
    rules[at:at] = extra
    it["rules"] = rules
    return it


def task_defs() -> list:
    return [{"name": TASK_NAME, "kind": "author_wording", "pool": "wording",
             "items": [(f"wording|{q}", R4._ch_item(n) if q == "ch_next" else _yn_item(n)) for q, n in N_NEW.items()]}]


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
    return R2.author_txt(td, b, root).replace("(REDO2)", "(REDO5)")


def task_index(batches: list, root: Path = ROOT) -> list:
    return R2.task_index(batches, root)


def dispatch(idx: list) -> dict:
    """What the orchestrator runs for step 1 (one Haiku agent, one self-contained task file) and the steps that follow."""
    t = idx[0]
    py = "../../.venv/bin/python -B zed_orch/t27_fix_r2/redo5.py"
    return {
        "purpose": "T27 G11 fix round 2: new training wordings, 24 ch_next + 8 yn_beyond (redo5; supersedes haiku_r4)",
        "step": "1 of 3: Haiku AUTHORING (one agent, one task file; the file is self-contained)",
        "model": "haiku",
        "tasks": [{"kind": t["kind"], "task_id": t["task_id"], "task_file": t["task_file"],
                   "task_file_sha256": hashlib.sha256(Path(t["task_file"]).read_bytes()).hexdigest(),
                   "answer_file": t["answer_file"],
                   "agent_prompt": f"Read your task file {t['task_file']} and follow it exactly. Write the answer only to "
                                   "the file it names. Do not open any other file."}],
        "then": [f"cd lean/c2_build; {py} load --write   (family lint + merge; prints counts per form)",
                 f"{py} glex-write   (writes the 2 G-LEX read tasks under haiku_r5/extract/ and prints their paths)",
                 "step 2 of 3: run the 2 reads with two DIFFERENT Haiku agents (one task file each, answer path inside the file)",
                 f"{py} glex-check --record   (2/2 admission; writes admitted_wordings.json)"]}


def write_tasks(root: Path = ROOT) -> list:
    root = Path(root)
    if (root / "TASKS.json").exists():
        raise FileExistsError(f"{root}/TASKS.json exists: the redo5 authoring task is written once")
    batches = build_batches(root)
    for td, b in batches:
        files = dict(b.files())
        files[R2._txt_path(root, b.chunks[0]["task_id"]).name] = author_txt(td, b, root)
        paths.write_files(root, files)
    idx = task_index(batches, root)
    paths.write_json(root / "TASKS.json", {
        "family": FAMILY, "seed": SEED, "stage": "redo5 (G11 fix round 2: ch_next + yn_beyond training wordings)",
        "prompt_sha": chunker.sha(PROMPT), "n_asked": dict(N_NEW),
        "g0_sha256": hashlib.sha256((C2 / "families" / "T27" / "G0_SPEC.md").read_bytes()).hexdigest(), "tasks": idx})
    paths.write_json(root / "DISPATCH.json", dispatch(idx))
    return idx


# ------------------------------------------------------------------------------------------------ the frozen pools

pool_wordings, pool_lexicon, _is_lex_text = R4.pool_wordings, R4.pool_lexicon, R4._is_lex_text


# ------------------------------------------------------------------------------------------------ load and merge

def merge(kept: dict, dropped: list) -> tuple:
    """(kept, dropped + extra drops). Only wordings of the two asked forms; a text equal to a frozen wording or to any frozen
    lexicon form (of any meaning) is dropped, and the family lint (authoring.lint_wording, run by authoring.load) is unchanged."""
    lex = pool_lexicon()
    have = {A._norm(r["text"]) for r in pool_wordings()}
    out_k, out_d = {}, list(dropped)
    for pool, ps in kept.items():
        for p in ps:
            why = []
            if pool != "wording" or p.get("qform") not in N_NEW:
                why.append(NOT_A_REDO5_POOL)
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


split_held = R4.split_held


def _by_form(pieces) -> dict:
    c = Counter(p.get("qform") for p in pieces if p.get("qform"))
    return {q: c.get(q, 0) for q in N_NEW}


def outlook(new_training: dict) -> dict:
    """Report only (never an admission rule): wordings per form vs the G11 floor, from diag_g11.json. floor = the wordings that
    keep every wording at or under the 2% cap when the balancer is up to IMBALANCE rows off the mean."""
    d = json.loads(DIAG.read_text(encoding="utf-8"))
    cap = d["max_rows_per_wording_at_bar"]
    out = {}
    for q in N_NEW:
        f = d["forms"][q]
        rows, usable, n_new = f["rows"], f["usable_wordings_in_generation"], new_training.get(q, 0)
        floor = math.ceil(rows / (cap - IMBALANCE))
        total = usable + n_new
        out[q] = {"rows": rows, "usable_before": usable, "new_training": n_new, "total": total,
                  "even_split_rows_per_wording": round(rows / total, 1),
                  "even_split_max_share": round(rows / total / d["n_rows"], 4), "floor_wordings": floor,
                  "meets_floor": total >= floor, "planned_g5h_losses": LOSS_PLAN[q],
                  "meets_floor_after_planned_losses": total - LOSS_PLAN[q] >= floor,
                  "new_needed_for_floor": max(0, floor - usable),
                  "new_needed_after_planned_losses": max(0, floor + LOSS_PLAN[q] - usable)}
    return out


def load(root: Path = ROOT, answers: dict | None = None, batches: list | None = None) -> dict:
    rep = A.load(root, answers=answers, batches=batches)
    kept, dropped = merge(rep["kept"], rep["dropped"])
    tr, ho = split_held(kept)
    returned = rep["kept"].get("wording", []) + [d for d in rep["dropped"] if d.get("pool") == "wording"]
    counts = {"asked": dict(N_NEW), "returned": _by_form(returned),
              "kept_after_lint_and_merge": _by_form(kept.get("wording", [])), "training": _by_form(tr),
              "held_out_not_admitted": _by_form(ho), "dropped": len(dropped),
              "frozen_training_wordings": {q: sum(1 for r in pool_wordings() if r["qform"] == q and not r["held_out"])
                                           for q in N_NEW}}
    return {"kept": kept, "dropped": dropped, "problems": rep["problems"], "counts": counts,
            "outlook_if_all_training_admitted": outlook(counts["training"]),
            "training": [p["piece_id"] for p in tr], "held_out": [p["piece_id"] for p in ho]}


def kept_from_disk(root: Path = ROOT) -> dict:
    return json.loads((Path(root) / "linted.json").read_text(encoding="utf-8"))["kept"]


# ------------------------------------------------------------------------------------------------ G-LEX reads

def glex_plan(kept: dict | None = None) -> dict:
    """The 2 G-LEX reads: the new TRAINING wordings of both forms (recorded) plus seeded control wordings of the frozen pool (not
    recorded; as redo4: 8 yn_not_beyond, 6 yn_beyond, 4 yn_within, 4 ch_next, trimmed by a seeded hash to the room left under
    the 50-item cap), one chunk per read, the same closed list and read format as redo2.glex_plan."""
    kept = kept_from_disk() if kept is None else kept
    tests_p, _ho = split_held(kept)
    main = {"wording": pool_wordings()}
    reg = A.registry({"wording": list(main["wording"]) + tests_p})
    form_of = {reg.forms[f].text: f for f in reg.forms}
    test_ids = sorted(form_of[p["text"]] for p in tests_p if reg.forms[form_of[p["text"]]].unit_ok)
    unit_failed = sorted(form_of[p["text"]] for p in tests_p if not reg.forms[form_of[p["text"]]].unit_ok)
    if not test_ids:
        raise ValueError("no unit-tested wording to read")
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
    return R2.glex_txt(b, root).replace("(REDO2)", "(REDO5)")


def glex_write(root: Path = GLEX_ROOT, kept: dict | None = None) -> list:
    root = Path(root)
    if (root / "TASKS.json").exists():
        raise FileExistsError(f"{root}/TASKS.json exists: the redo5 G-LEX reads are written once")
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
        "family": FAMILY, "gate": "G-LEX 2/2 (redo5: ch_next + yn_beyond training wordings)", "reads": list(READS),
        "tasks": tasks, "test_forms": {f: reg.forms[f].sem_id for f in p["tests"]},
        "control_forms": {f: reg.forms[f].sem_id for f in p["controls"]}, "unit_failed": p["unit_failed"],
        "rule": "only test forms are recorded; controls are report-only (they are admitted by the frozen reads)"})
    return tasks


def glex_check(root: Path = GLEX_ROOT, p: dict | None = None) -> dict:
    """Judge the 2 reads (extract_check.judge: a malformed or missing read is never recorded), record the valid reads for the
    test forms only, report admission, control agreement and the outlook per form."""
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
        st, why, got, path = R4._read_answer(b, reg, root)
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
    by_form = _by_form(p["test_pieces"][f] for f in admitted)
    tested = _by_form(p["test_pieces"][f] for f in sorted(tests))
    return {"family": FAMILY, "gate": "G-LEX 2/2 (redo5)", "file_problems": file_probs, "tasks": rows, "forms": status,
            "admitted": admitted, "admitted_by_qform": by_form, "tested_by_qform": tested,
            "unit_failed": p["unit_failed"], "complete": ok, "outlook": outlook(by_form),
            "status": ("COMPLETE: both reads valid; " if ok else "INCOMPLETE: ")
            + f"{len(admitted)}/{len(tests)} wordings admitted (" + ", ".join(f"{q} {by_form[q]}/{tested[q]}" for q in N_NEW) + ")",
            "no_labels_set": True, "no_rows_generated": True}


def admitted_payload(p: dict, rep: dict) -> dict:
    """The records overlay.py / install_code.py add to the frozen pools, in exactly the shapes of pools_v2/wordings.json and
    pools_v2/lexicon.json (forms from LexiconRegistry.to_json, so status and votes are the registry's own)."""
    reg = p["reg"]
    fj = {f["form_id"]: f for f in reg.to_json()["forms"]}
    wordings, forms = [], []
    for fid in rep["admitted"]:
        pc = p["test_pieces"][fid]
        f = reg.forms[fid]
        wordings.append({"extractions": [list(e) for e in f.extractions], "form_id": fid, "held_out": False,
                         "piece_id": pc["piece_id"], "pool": "wording", "prompt_sha": pc["prompt_sha"],
                         "qform": pc["qform"], "round": ROUND, "sem": f.sem_id, "sem_id": f.sem_id,
                         "task_id": pc["task_id"], "text": pc["text"]})
        forms.append(fj[fid])
    return {"family": FAMILY, "round": ROUND, "wordings": wordings, "forms": forms,
            "by_qform": _by_form(wordings),
            "pools_sha256": {n: hashlib.sha256((POOLS / n).read_bytes()).hexdigest()
                             for n in ("wordings.json", "lexicon.json")},
            "n_admitted": len(wordings)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="redo5")
    ap.add_argument("cmd", choices=("tasks", "write", "load", "glex-plan", "glex-write", "glex-check"))
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--record", action="store_true")
    a = ap.parse_args(argv)
    if a.cmd == "tasks":
        print(json.dumps(task_index(build_batches(ROOT), ROOT), indent=1))
    elif a.cmd == "write":
        print(json.dumps([{"task_file": R2._txt_path(ROOT, t["task_id"]).as_posix(), "answer_file": t["answer_file"],
                           "kind": t["kind"]} for t in write_tasks(ROOT)], indent=1))
    elif a.cmd == "load":
        rep = load(ROOT)
        print(json.dumps({"counts": rep["counts"], "problems": rep["problems"],
                          "drop_reasons": A._reason_counts(rep["dropped"]),
                          "outlook_if_all_training_admitted": rep["outlook_if_all_training_admitted"]}, indent=1))
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

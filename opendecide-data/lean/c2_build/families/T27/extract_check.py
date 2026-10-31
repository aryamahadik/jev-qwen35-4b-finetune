"""families/T27/extract_check.py: check the T27 G-LEX extraction answers, record only the valid reads, and write the
validation record (C2_DATA_SPEC 6.2 item 2; G0_SPEC section 6 "Admission"; PREREG A37 b).

A G-LEX read is VALID only when its answer file is one JSON object whose keys are exactly the qids of its chunk (all of
them, no others) and whose every value is a meaning copied from the closed list of its task's kind (the prompt's rule).
Anything else is MALFORMED and is NOT recorded: lexicon.record_extraction stores a wrong or unlisted meaning as a
disagreement, and a disagreement rejects a form for good (no re-vote), so a format failure must never reach the
registry. A missing answer is MISSING and is not recorded either. No label is set here: a valid read only names a
meaning, which the registry maps to a sem id that the form admits or rejects.

  ../../.venv/bin/python -m families.T27.extract_check check    (from lean/c2_build; in memory, writes nothing)
  ../../.venv/bin/python -m families.T27.extract_check record   (writes haiku/extract/record/VALIDATION.json)

Mode T only (G0 section 1, S18): there are no free-form notes, so the G3-H comparison does not apply to T27.
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import paths  # noqa: E402
from families.T27 import glex_build as G  # noqa: E402

FAMILY = G.FAMILY
EXTRACT = G.EXTRACT
RECORD = EXTRACT / "record"
G0 = HERE / "G0_SPEC.md"
EXPECTED_TASKS = 26
MAX_SHOW = 8


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def closed_list(reg, kind: str) -> set:
    """The closed meaning list of a kind (the same set glex_build writes into every prompt of that kind)."""
    return {s.meaning for s in reg.sems.values() if s.kind == kind}


def files_check(p: dict) -> tuple:
    """Every file the kit writes for each batch (prompt, chunk, key, manifest) must equal the file on disk, and the
    task index must list the rebuilt tasks. Returns (files checked, problems)."""
    problems, checked = [], 0
    for _read, _kind, _g, b in p["batches"]:
        for rel, text in sorted(b.files().items()):
            checked += 1
            f = EXTRACT / rel
            if not f.is_file() or f.read_text(encoding="utf-8") != text:
                problems.append(f"{b.batch_id}: {rel} differs from the rebuilt file")
    index = json.loads((EXTRACT / "TASKS.json").read_text(encoding="utf-8"))
    built = {b.chunks[0]["task_id"] for _r, _k, _g, b in p["batches"]}
    listed = {t["task_id"] for t in index["tasks"]}
    if len(built) != EXPECTED_TASKS:
        problems.append(f"plan builds {len(built)} tasks, expected {EXPECTED_TASKS}")
    if listed != built:
        problems.append(f"TASKS.json differs from the rebuilt task list ({len(listed ^ built)} ids)")
    return checked, problems


def judge(b, kind_list: set, raw) -> tuple:
    """(status, reasons, {internal id: meaning} for a valid read). Status: valid or malformed."""
    qids = [it["qid"] for c in b.chunks for it in c["items"]]
    if not isinstance(raw, dict):
        return "malformed", ["answer is not one JSON object keyed by qid"], {}
    reasons = []
    extra = sorted(set(raw) - set(qids))
    missing = [q for q in qids if q not in raw]
    if extra:
        reasons.append(f"{len(extra)} key(s) that are not qids of this task (first: {extra[0]!r})")
    if missing:
        reasons.append(f"{len(missing)} of {len(qids)} qid(s) unanswered")
    off = [q for q in qids if q in raw and (not isinstance(raw[q], str) or raw[q] not in kind_list)]
    if off:
        reasons.append(f"{len(off)} value(s) are not a meaning from the closed list of kind {b.kind!r}")
    if reasons:
        return "malformed", reasons, {}
    return "valid", [], {b.key[q]: raw[q] for q in qids}


def run() -> dict:
    p = G.plan()
    reg = p["reg"]
    checked, file_probs = files_check(p)
    rows, forms_recorded = [], 0
    for read, kind, g, b in p["batches"]:
        tid = b.chunks[0]["task_id"]
        path = EXTRACT / b.answer_path(tid)
        raw, got = None, {}
        if not path.is_file():
            st, reasons = "missing", ["no answer file"]
        else:
            try:
                raw = json.loads(path.read_text(encoding="utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as e:
                st, reasons = "malformed", [f"not valid JSON ({type(e).__name__})"]
            else:
                st, reasons, got = judge(b, closed_list(reg, kind), raw)
        if st == "valid":
            ext = f"{read}:{tid}"                      # one extractor id per read task (independent reads)
            for fid, meaning in sorted(got.items()):
                reg.record_extraction(fid, ext, reg.meaning_to_sem(kind, meaning))
            forms_recorded += len(got)
        row = {"task_id": tid, "read": read, "kind": kind, "group": g, "n_items": len(b.key), "status": st,
               "reasons": reasons, "answer_sha256": _sha(path.read_bytes()) if path.is_file() else None,
               "answer_cites_built_prompt": (raw.get("prompt_sha") == b.prompt_sha)
               if isinstance(raw, dict) and "prompt_sha" in raw else None}
        if st == "malformed" and isinstance(raw, dict):
            row["answer_top_keys"] = sorted(raw)[:MAX_SHOW]
        rows.append(row)
    status_of = {fid: reg.status(fid) for fid in sorted(reg.forms)}
    by_status = Counter(status_of.values())
    by_read = {r: dict(Counter(x["status"] for x in rows if x["read"] == r)) for r in ("read1", "read2")}
    n_valid = sum(1 for x in rows if x["status"] == "valid")
    n_missing = sum(1 for x in rows if x["status"] == "missing")
    n_malformed = sum(1 for x in rows if x["status"] == "malformed")
    complete = n_valid == EXPECTED_TASKS and by_status.get("admitted", 0) == len(reg.forms)
    return {
        "family": FAMILY, "gate": "G-LEX 2/2 (T27 has no precedence or window kind)",
        "g0_sha256_file": _sha(G0.read_bytes()), "files_checked": checked, "file_problems": file_probs,
        "tasks_expected": EXPECTED_TASKS, "tasks": rows,
        "counts": {"valid": n_valid, "malformed": n_malformed, "missing": n_missing, "by_read": by_read},
        "valid_reads_recorded_forms": forms_recorded,
        "forms": {"total": len(reg.forms), "unit_ok": sum(1 for f in reg.forms.values() if f.unit_ok),
                  "status": dict(sorted(by_status.items())),
                  "status_by_kind": {k: dict(sorted(Counter(status_of[f] for f in reg.forms if reg.forms[f].kind == k)
                                                    .items())) for k in sorted({f.kind for f in reg.forms.values()})}},
        "g3h": "not applicable (Mode T only; G0 S18)",
        "status": ("EXTRACTION COMPLETE: every task valid and every form admitted" if complete else
                   f"INCOMPLETE: {n_valid}/{EXPECTED_TASKS} valid reads ({n_malformed} malformed, {n_missing} missing); "
                   f"{by_status.get('admitted', 0)}/{len(reg.forms)} forms admitted; freeze blocked"),
        "rule": ("malformed and missing answers are not recorded: a recorded disagreement rejects a form for good "
                 "(lexicon.record_extraction, no re-vote)"),
        "no_labels_set": True, "no_rows_generated": True,
    }


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    cmd = args[0] if args else "check"
    if cmd not in ("check", "record"):
        print(__doc__)
        return 2
    out = run()
    if cmd == "record":
        paths.write_json(RECORD / "VALIDATION.json", out)
    brief = {k: out[k] for k in ("status", "files_checked", "file_problems", "counts", "valid_reads_recorded_forms",
                                 "forms", "g3h")}
    brief["malformed_tasks"] = [{"task_id": x["task_id"], "reasons": x["reasons"],
                                 "answer_top_keys": x.get("answer_top_keys")}
                                for x in out["tasks"] if x["status"] == "malformed"]
    brief["missing_tasks"] = [x["task_id"] for x in out["tasks"] if x["status"] == "missing"]
    brief["command"] = cmd
    print(json.dumps(brief, ensure_ascii=False, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())

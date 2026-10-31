"""c2_build/families/T12/extract_record.py: record the T12 extraction answers (G-LEX and G3-H), after A38 only.

The 18 answer files under haiku/extract/answers/ are the Haiku extraction reads: 15 G-LEX reads (2 comparator, 3
precedence, 10 question) and 3 G3-H reads (free-form notes). This module:

  check   rebuilds every batch in memory (extract_build.build_all, no writes) and checks that each file the kit
          writes for it (prompt, chunks, key, manifest and tasks/*.md) is byte-identical to the file on disk, so the
          agents answered exactly the tasks that were built. Writes nothing.
  record  loads the answers (chunker.load_answers: unknown, duplicate or unanswered qids are problems), records every
          G-LEX read with reg.record_extraction (extractor = the task id; sem = reg.meaning_to_sem(kind, meaning), so
          an unknown meaning or a decoy meaning records None or the decoy and rejects the form), compares every G3-H
          answer with g3h.compare (template = the note, one note per Mode F skin), and writes the record under
          haiku/extract/record/ (guarded writers only).

Haiku never sets a label here: a G-LEX read names a meaning (which maps to a sem id that the form either matches or
does not), and a G3-H read is only compared with the generator's expected values (a mismatch drops the note).

  ../.venv/bin/python -m families.T12.extract_record check    (from lean/c2_build; no writes)
  ../.venv/bin/python -m families.T12.extract_record record   (writes haiku/extract/record/)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, g3h, paths  # noqa: E402
from families.T12 import extract_build as EB  # noqa: E402
from families.T12 import plugin as P  # noqa: E402

FAMILY = "T12"
RECORD = EB.EXTRACT / "record"
EXPECTED_READS = 18


def batches(res: dict) -> list:
    """[(group, read, TaskBatch)] for the 7 lex batches and the g3h batch, in build order."""
    out = [(rd["group"], rd["read"], rd["batch"]) for rd in res["glex"]]
    out.append(("g3h", 1, res["g3h"]))
    return out


def check_files(res: dict) -> dict:
    """Every file the kit writes for each batch, and each task file, must equal the file on disk."""
    probs, checked = [], 0
    for group, read, b in batches(res):
        for rel, text in sorted(b.files().items()):
            p = EB.EXTRACT / rel
            checked += 1
            if not p.is_file() or p.read_text(encoding="utf-8") != text:
                probs.append(f"{b.batch_id}: {rel} differs from the rebuilt file")
        for c in b.chunks:
            tid = c["task_id"]
            md = EB.task_markdown(b.kind, b, c, EB.EXTRACT / b.answer_path(tid))
            p = EB.EXTRACT / "tasks" / f"{tid}.md"
            checked += 1
            if not p.is_file() or p.read_text(encoding="utf-8") != md:
                probs.append(f"{tid}: tasks/{tid}.md differs from the rebuilt task")
    index = json.loads((EB.EXTRACT / "TASKS.json").read_text(encoding="utf-8"))
    n_tasks = len(index["tasks"])
    if n_tasks != EXPECTED_READS:
        probs.append(f"TASKS.json lists {n_tasks} tasks, expected {EXPECTED_READS}")
    return {"files_checked": checked, "tasks_indexed": n_tasks, "problems": probs}


def load_batch(b) -> tuple:
    """({internal id: answer}, problems, per-task answer-file report) for one batch."""
    raw, report, file_probs = {}, [], []
    for c in b.chunks:
        tid = c["task_id"]
        f = EB.EXTRACT / b.answer_path(tid)
        if not f.is_file():
            report.append({"task_id": tid, "answer_file": "missing", "n_items": len(c["items"]), "answered": 0})
            continue
        try:
            raw[tid] = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            file_probs.append(f"{tid}: answer is not JSON ({e})")
            report.append({"task_id": tid, "answer_file": "not json", "n_items": len(c["items"]), "answered": 0})
            continue
        report.append({"task_id": tid, "answer_file": "ok", "n_items": len(c["items"]),
                       "answered": len(raw[tid]) if isinstance(raw[tid], list) else 0})
    got, probs = chunker.load_answers(b, raw)
    return got, file_probs + probs, report


def record_lex(res: dict, loaded: dict) -> tuple:
    """Records every G-LEX read on the registry. Returns (rows, problems)."""
    reg = res["reg"]
    rows, probs = [], []
    for group, read, b in batches(res):
        if group == "g3h":
            continue
        got, bprobs, _rep = loaded[b.batch_id]
        probs += [f"{b.batch_id}: {x}" for x in bprobs]
        for qid, fid in sorted(b.key.items()):
            tid = b.task_of[qid]
            if fid not in got:
                continue                                  # unanswered: the form stays pending
            ans = got[fid]
            meaning = ans.get("meaning") if isinstance(ans, dict) else None
            kind = reg.forms[fid].kind
            sem = reg.meaning_to_sem(kind, meaning) if isinstance(meaning, str) else None
            reg.record_extraction(fid, tid, sem)
            rows.append({"form_id": fid, "task_id": tid, "group": group, "read": read, "meaning": meaning,
                         "sem_id": sem, "agrees": sem == reg.forms[fid].sem_id})
    return rows, probs


def record_g3h(res: dict, loaded: dict) -> tuple:
    """(template report, per-note detail, problems). One template per note (a Mode F note is its own skin)."""
    fields = EB.g3h_fields()
    got, bprobs, _rep = loaded[res["g3h"].batch_id]
    results, detail = [], {}
    for iid in sorted(res["g3h_expected"]):
        if iid not in got:
            ok, diffs = False, ["unanswered"]
        else:
            ok, diffs = g3h.compare(res["g3h_expected"][iid], got[iid], fields)
        results.append((iid, iid, ok))
        detail[iid] = {"ok": ok, "diffs": diffs}
    rep = g3h.template_report(results)
    return rep, detail, [f"{res['g3h'].batch_id}: {x}" for x in bprobs]


def lex_summary(reg, fids) -> dict:
    per = {}
    for fid in fids:
        st = reg.status(fid)
        per.setdefault(reg.forms[fid].kind, {}).setdefault(st, 0)
        per[reg.forms[fid].kind][st] += 1
    return per


def run() -> dict:
    res = EB.build_all()
    files = check_files(res)
    loaded = {b.batch_id: load_batch(b) for _g, _r, b in batches(res)}
    lex_rows, lex_probs = record_lex(res, loaded)
    rep, detail, g3_probs = record_g3h(res, loaded)
    return {"res": res, "files": files, "loaded": loaded, "lex_rows": lex_rows, "lex_probs": lex_probs,
            "g3h_rep": rep, "g3h_detail": detail, "g3h_probs": g3_probs}


def summary(out: dict) -> dict:
    res, reg = out["res"], out["res"]["reg"]
    reads = []
    for group, read, b in batches(res):
        _got, probs, rep = out["loaded"][b.batch_id]
        for r in rep:
            r.update({"group": group, "read": read, "batch_id": b.batch_id})
            reads.append(r)
    answered_files = sum(1 for r in reads if r["answer_file"] == "ok")
    fids = sorted(reg.forms)
    st = lex_summary(reg, fids)
    lex_sum = {k: dict(sorted(v.items())) for k, v in sorted(st.items())}
    per_form_reads = {}
    for x in out["lex_rows"]:
        per_form_reads.setdefault(x["form_id"], []).append(x["agrees"])
    return {"family": FAMILY, "g0_sha256": P.G0_SHA256_AUTHORED, "files": out["files"],
            "answer_files": {"expected": EXPECTED_READS, "returned": answered_files, "reads": reads},
            "lex_records": len(out["lex_rows"]), "lex_disagreements": sum(1 for x in out["lex_rows"] if not x["agrees"]),
            "lex_problems": out["lex_probs"], "lex_status_by_kind": lex_sum,
            "g3h": {"notes": len(out["g3h_detail"]), "ok": sum(1 for d in out["g3h_detail"].values() if d["ok"]),
                    "quarantined_templates": out["g3h_rep"]["quarantined"], "drop_rows": out["g3h_rep"]["drop_rows"],
                    "problems": out["g3h_probs"]}}


def write_record(out: dict) -> dict:
    res, reg = out["res"], out["res"]["reg"]
    s = summary(out)
    paths.write_json(RECORD / "RECORD.json", s)
    fids = sorted(reg.forms)
    lex_out = []
    for fid in fids:
        f = reg.forms[fid]
        lex_out.append({"form_id": fid, "sem_id": f.sem_id, "kind": f.kind, "text": f.text, "held_out": f.held_out,
                        "required": f.required, "unit_ok": f.unit_ok, "extractions": [list(e) for e in f.extractions],
                        "status": reg.status(fid)})
    paths.write_json(RECORD / "lexicon_record.json", {"family": FAMILY, "forms": lex_out})
    paths.write_json(RECORD / "g3h_record.json", {"family": FAMILY, "bar": g3h.PASS_RATE,
                                                  "template": "one note = one template", "report": {
                                                      k: v for k, v in out["g3h_rep"].items() if k != "templates"},
                                                  "notes": out["g3h_detail"]})
    return s


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    cmd = args[0] if args else "check"
    if cmd not in ("check", "record"):
        print(__doc__)
        return 2
    out = run()
    s = summary(out)
    if cmd == "record":
        s = write_record(out)
    print(json.dumps({"files": out["files"], "answer_files": {"expected": s["answer_files"]["expected"],
                                                             "returned": s["answer_files"]["returned"]},
                      "lex_records": s["lex_records"], "lex_disagreements": s["lex_disagreements"],
                      "lex_status_by_kind": s["lex_status_by_kind"], "lex_problems": s["lex_problems"][:20],
                      "g3h": {k: v for k, v in s["g3h"].items() if k != "drop_rows"}, "command": cmd},
                     ensure_ascii=False, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())

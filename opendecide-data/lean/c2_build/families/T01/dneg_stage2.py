"""families/T01/dneg_stage2.py: stage 2 of the T01 double-negation wordings (fix iteration 2; G0_SPEC_v4 12.1).

Input : the Haiku authoring answers of haiku/dneg_i2/answers/ (task files: haiku/dneg_i2/tasks/, written by
        `python -B -m families.T01.dneg_i2 write-tasks`). An answer file is used whole or not at all (the kit's contract:
        a JSON list, one {"qid", "text"} per item of its chunk).
Does  : admits every candidate through haiku_dneg.check_wording: one question, the declared placeholders once, G-SL,
        negcount exactly (k_all, k_syn) = (2, 2), the polarity rules P1-P4 of c2_kit.polarity (strict frames), the word
        bans, no fixture copy, no duplicate. Then the lexicon check (a form must build and pass its unit test), then it
        writes the G-LEX task files, TWO INDEPENDENT READS (each read has its own chunk files and its own filled
        instance), to haiku/dneg_i2/glex_tasks/, plus stage2_state.json (what stage 3 rebuilds from) and
        stage2_report.json.
Output: the orchestrator runs one fresh Haiku agent per G-LEX task file (read only its task_file, write only its
        answer_file; a read-1 and a read-2 task are never done by the same agent), then `dneg_stage3`.
No Haiku, no model, no network.

  ../../.venv/bin/python -B -m families.T01.dneg_stage2 [--root <haiku/dneg_i2>]      (from lean/c2_build)

Exit code 0 when every form has >= 8 candidates left for G-LEX, 1 otherwise (the report names the short form: re-author
it with 4x candidates; the target of 8 admitted wordings per form is never lowered).
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import paths  # noqa: E402
from families.T01 import dneg_i2 as D  # noqa: E402
from families.T01 import extract as E  # noqa: E402
from families.T01 import freeze_v2 as FV  # noqa: E402
from families.T01 import haiku_dneg as HD  # noqa: E402


def read_authoring(root: Path) -> tuple:
    """(candidates [dict], dropped [(iid, reasons)], file records, problems). Candidates passed haiku_dneg.check_wording."""
    root = Path(root)
    b, plan = D.build_batch()
    inv = {}
    cands, dropped, recs, problems, seen = [], [], [], [], set()
    for c in b.chunks:
        tid = c["task_id"]
        items = {it["qid"]: it for it in c["items"]}
        ans, rec = FV.read_answer_file("dneg-i2-author", b.kind, tid, root / b.answer_path(tid), items, ())
        recs.append(rec)
        if ans is None:
            problems.append(f"{tid}: {rec['status']} {rec['problems'][:2]}")
            continue
        for qid in sorted(ans, key=lambda q: b.key[q]):
            iid = b.key[qid]
            obj, v = HD.check_wording(iid, ans[qid]["text"], plan[iid], tid, b.prompt_sha, seen)
            if v:
                dropped.append((iid, v))
                continue
            q, text, slots, tid_, psha = obj
            cands.append({"iid": iid, "qform": q, "text": text, "slots": slots, "task_id": tid_, "prompt_sha": psha})
    return cands, dropped, recs, problems


def run(root: Path = D.ROOT, *, pools_dir: Path = D.POOLS_DIR) -> dict:
    root = Path(root)
    glex_root = root / "glex_tasks"
    cands, dropped, recs, problems = read_authoring(root)
    reg, fids, lex_drops = D.glex_registry(cands)
    ok = [dict(c, form_id=fids[k]) for k, c in enumerate(cands) if k in fids]
    per_form = {q: sum(1 for c in ok if c["qform"] == q) for q in D.FORMS}
    reasons = Counter(r.split(":", 1)[0][:30] for _i, v in dropped for r in v[:1])
    short = {q: n for q, n in per_form.items() if n < D.MIN_ADMITTED}
    batches = D.glex_batches(reg, [c["form_id"] for c in ok]) if ok else []
    files, tasks = {}, []
    for label, b in batches:
        files.update(b.files())
        for c in b.chunks:
            tid = c["task_id"]
            files[f"tasks/{tid}.md"] = E.task_text(glex_root, b, c, label)
            tasks.append({"read": label, "kind": "extract_lex", "task_id": tid, "batch_id": b.batch_id,
                          "task_file": str(glex_root / f"tasks/{tid}.md"), "answer_file": str(glex_root / b.answer_path(tid)),
                          "n_items": len(c["items"]),
                          "audit_allowed_read": [str(glex_root / f"tasks/{tid}.md")],
                          "audit_allowed_write": [str(glex_root / b.answer_path(tid))]})
    if batches:
        paths.write_files(glex_root, files)
        paths.write_json(glex_root / "TASKS.json", {
            "family": D.FAMILY, "version": D.VERSION, "n_tasks": len(tasks), "tasks": tasks, "reads": list(D.GLEX_READS),
            "batches": {label: b.batch_id for label, b in batches},
            "contract": "one JSON list, one {\"qid\", \"meaning\"} per item; meaning copied exactly from that item's choices",
            "independence": "the two reads are different task files; give no agent a task of both reads"})
        for t in tasks:
            Path(t["answer_file"]).parent.mkdir(parents=True, exist_ok=True)
    state = {"family": D.FAMILY, "version": D.VERSION, "candidates": ok, "per_form": per_form,
             "batch_ids": {label: b.batch_id for label, b in batches}}
    root.mkdir(parents=True, exist_ok=True)
    paths.write_json(root / "stage2_state.json", state)
    report = {"family": D.FAMILY, "stage": 2, "answer_files": Counter(r["status"] for r in recs),
              "candidates_per_form": per_form, "short_forms": short, "min_per_form": D.MIN_ADMITTED,
              "first_failing_rule_counts": dict(reasons), "lexicon_drops": lex_drops[:30], "file_problems": problems[:30],
              "dropped_examples": [{"iid": i, "reasons": v[:3]} for i, v in dropped[:30]],
              "n_glex_tasks": len(tasks), "glex_tasks": tasks,
              "next": ("one fresh Haiku agent per glex task file (read only its task_file, write only its answer_file), "
                       "then: python -B -m families.T01.dneg_stage3")}
    paths.write_json(root / "stage2_report.json", report)
    return report


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=str(D.ROOT))
    a = ap.parse_args(argv)
    rep = run(Path(a.root))
    print(json.dumps({k: rep[k] for k in ("answer_files", "candidates_per_form", "short_forms", "first_failing_rule_counts",
                                          "n_glex_tasks")}, indent=1))
    return 1 if rep["short_forms"] or not rep["n_glex_tasks"] else 0


if __name__ == "__main__":
    raise SystemExit(main())

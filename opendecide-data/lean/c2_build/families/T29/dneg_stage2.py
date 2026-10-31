"""c2_build/families/T29/dneg_stage2.py: stage 2 of the T29 double-negation round (fix iteration 2).

Reads the Haiku authoring answers (haiku/dneg_i2/answers/<task_id>.json), admits them with authoring.wording_problems()
(negation profile 2/2 + polarity rule + G-SL), dedups, adds the survivors to the merged lexicon (declare_dneg first), and
writes the two independent G-LEX read tasks to haiku/dneg_i2/glex_tasks/ (2 reads, answers in glex_tasks/answers/).
Also writes haiku/dneg_i2/stage2_state.json (what stage 3 rebuilds) and STAGE2_REPORT.json.

  ../.venv/bin/python -B families/T29/dneg_stage2.py [--root DIR]      (from lean/c2_build; --root only for tests)
  ../.venv/bin/python -B families/T29/dneg_stage2.py --write-author     writes the authoring tasks (the orchestrator's step 0)
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from c2_kit import paths  # noqa: E402
from families.T29 import dneg_i2 as D  # noqa: E402


def stage2(root: Path) -> dict:
    tasks = D.author_tasks()
    pieces, drops = D.collect(tasks, root)
    authored = len(pieces)
    surv, drops = D.admit_authoring(pieces, drops)
    reg, new, form_drops = D.build_registry(surv)
    drops = drops + form_drops
    new_ids = sorted(new)
    batches = D.glex_batches(reg, new_ids)
    files, manifest = D.glex_files(root, batches)
    paths.write_files(root / D.GLEX_SUB, files)
    state = {"version": D.VERSION, "forms": [
        {"form_id": fid, "pid": new[fid]["pid"], "text": new[fid]["text"], "held_out": new[fid]["held_out"],
         "task_id": new[fid]["task_id"], "prompt_sha": new[fid]["prompt_sha"]} for fid in D.state_order(reg, new)]}
    paths.write_text(root / "stage2_state.json", json.dumps(state, ensure_ascii=False, indent=1) + "\n")
    rep = {"stage": 2, "authored": authored, "survivors": len(surv), "new_forms": len(new_ids),
           "new_forms_training": sum(1 for f in new_ids if not new[f]["held_out"]),
           "new_forms_held_out": sum(1 for f in new_ids if new[f]["held_out"]),
           "drop_reasons": dict(Counter(r.split(":")[0].split(" ")[0] for d in drops for r in d["reasons"]).most_common()),
           "drops": drops, "glex_tasks": manifest["n_tasks"],
           "glex_task_files": [r["task_file"] for r in manifest["tasks"]],
           "glex_answer_files": [r["answer_file"] for r in manifest["tasks"]]}
    paths.write_text(root / "STAGE2_REPORT.json", json.dumps(rep, ensure_ascii=False, indent=1) + "\n")
    return rep


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(D.ROOT))
    ap.add_argument("--write-author", action="store_true")
    a = ap.parse_args(argv)
    root = Path(a.root)
    if a.write_author:
        m = D.write_author(root)
        print(f"{m['n_tasks']} authoring tasks, {m['outputs_expected']} outputs expected under {root}/tasks/")
        return 0
    rep = stage2(root)
    print(json.dumps({k: v for k, v in rep.items() if k not in ("drops",)}, indent=1, ensure_ascii=False))
    return 0 if rep["new_forms"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

"""Item 10 driver (PREREG A47; FINAL_PLAN item 10). Run from c2_build:  $PY -B item10/i10.py <stage>

  status                     the stage reached (STATE.json) and the next command
  slices | author           stage 1: error slices; Haiku authoring task files              -> prints task records (JSON)
  lint | extract             stage 2: lint authored cards; two Haiku G-LEX read task files    -> task records
  compare [--sheet DOM] [--flagged]   stage 3: program checks; --sheet prints the review sheet
  admit                      stage 3: cards/admission/review.json -> cards/admitted.jsonl
  cands                      stage 4: candidates + data/i10_c1read.jsonl           (then: i10_vm.py predict-start / -wait / -pull)
  select                     stage 5: C1-uncertain rows -> Haiku label tasks (slice A) + Opus tasks (slice B)  -> task records
  route                      stage 6: Haiku answers -> accepted / Opus chunks (150 in all with slice B's)      -> task records
  finalize                   stage 7: Opus answers -> kept rows with caps
  package                    stage 8: data/c2_parts/I10/{out,qc}
  crowd-prep                 stage 9: crowd shards data/c2_crowd_shards/I10 (then: i10_vm.py crowd-start / -wait / -pull)
  crowd-verify               stage 9: one C1 label per candidate row, one view (reads/verify_crowd_labels.check_family)
Every stage that makes task files prints a JSON list [{task_file, answer_file, model}] on its last line.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import i10_lib as L  # noqa: E402

NEXT = {
    "none": "slices", "slices": "author", "author": "(run the Haiku authoring tasks) then: lint", "lint": "extract",
    "extract": "(run the rA/rB read tasks) then: compare", "compare": "(Sonnet review: write cards/admission/review.json) then: admit",
    "admit": "cands", "cands": "i10_vm.py predict-start / predict-wait / predict-pull, then: select",
    "select": "(run the Haiku label tasks and the Opus slice-B tasks) then: route", "route": "(run the Opus I10-oa tasks) then: finalize",
    "finalize": "package", "package": "crowd-prep", "crowd-prep": "i10_vm.py crowd-start / crowd-wait / crowd-pull, then: crowd-verify",
    "crowd-verify": "(done) the orchestrator runs the all-block G13, then c2_select.py select --fam I10",
}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=["status", "slices", "author", "lint", "extract", "compare", "admit", "cands", "select",
                                      "route", "finalize", "package", "crowd-prep", "crowd-verify"])
    ap.add_argument("--sheet", default=None)
    ap.add_argument("--flagged", action="store_true")
    a = ap.parse_args(argv)
    if a.stage == "status":
        st = L.state()
        print(json.dumps({k: v for k, v in st.items() if k != "history"}, indent=1))
        print("next:", NEXT.get(st["stage"]))
        return
    import i10_cards as C
    import i10_rows as Rw
    if a.stage == "slices":
        print(json.dumps(C.cmd_slices()["slice_a_tasks_per_domain"]))
    elif a.stage == "author":
        out = C.cmd_author()
        print(json.dumps(out))
    elif a.stage == "lint":
        print(json.dumps(C.cmd_lint(), indent=1))
    elif a.stage == "extract":
        out = C.cmd_extract()
        print(json.dumps(out))
    elif a.stage == "compare":
        if a.sheet is not None or a.flagged:
            print(C.review_sheet(a.sheet or None, a.flagged))
        else:
            print(json.dumps(C.cmd_compare(), indent=1))
    elif a.stage == "admit":
        print(json.dumps(C.cmd_admit(), indent=1))
    elif a.stage == "cands":
        print(json.dumps(Rw.cmd_cands(), indent=1))
    elif a.stage == "select":
        print(json.dumps(Rw.cmd_select()))
    elif a.stage == "route":
        print(json.dumps(Rw.cmd_route()))
    elif a.stage == "finalize":
        print(json.dumps(Rw.cmd_finalize(), indent=1))
    elif a.stage == "package":
        print(json.dumps(Rw.cmd_package(), indent=1))
    elif a.stage == "crowd-prep":
        print(json.dumps(Rw.crowd_prep(), indent=1))
    elif a.stage == "crowd-verify":
        print(json.dumps(Rw.crowd_verify(), indent=1))


if __name__ == "__main__":
    main()

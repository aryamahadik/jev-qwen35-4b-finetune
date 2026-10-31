"""families/T31/dneg_stage2.py: stage 2 of the T31 double-negation round (fix iteration 2).

Reads the Haiku authoring answers (haiku/dneg_i2/answers/<task_id>.json), admits each wording with
dneg_authoring.wording_problems (one line, 6-30 words, one question, the placeholders, the explicit outer frame, the (2, 2)
negation profile, c2_kit.polarity P1-P4, G-SL, no label word), the REQ_ID rule and exact-text dedup (against the other
candidates and against every frozen pools_v2 form), adds the survivors to the pools_v2 lexicon IN MEMORY, unit-tests them,
and writes

  haiku/dneg_i2/glex_tasks/          two independent G-LEX reads (reads d2read0 / d2read1), tasks/*.md + chunks + keys +
                                     TASKS.json; answers go to glex_tasks/answers/<task_id>.json
  haiku/dneg_i2/admitted_candidates.json   the candidates the reads cover (stage 3 rebuilds the registry from it)
  haiku/dneg_i2/QUARANTINE_AUTHORING.json  every rejected answer with its reason
  haiku/dneg_i2/STAGE2_REPORT.json

Nothing in pools_v2/ or any answer file is changed. Refuses to rewrite glex_tasks/ once TASKS.json exists there.

  cd lean/c2_build
  ../.venv/bin/python -B families/T31/dneg_stage2.py            # (the repo venv is lean/../.venv; see FIX_I2_NOTES.md)
  ../.venv/bin/python -B families/T31/dneg_stage2.py --check    # in memory, nothing written
Exit 0 on OK, 2 on a shortfall or a problem the orchestrator should read (the files are still written), 1 on a stop.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from families.T31 import dneg_i2 as D  # noqa: E402


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=str(D.ROOT))
    ap.add_argument("--check", action="store_true", help="in memory only, write nothing")
    a = ap.parse_args(argv)
    out = D.run_stage2(Path(a.root), write=not a.check)
    print(json.dumps(out, indent=1, ensure_ascii=False))
    if out["status"].startswith("STOP"):
        return 1
    return 0 if out["status"] == "OK" else 2


if __name__ == "__main__":
    raise SystemExit(main())

"""transfer/T36/pilot_i1.py: the T36 pilot re-run after fix iteration 1 (C2_DATA_SPEC 6.4 step 6), into pilot_i1/.

c2_build/pilot.py writes <family dir>/pilot/; the first pilot (pilot/, PILOT_VERDICT.json) is the evidence the fixes
answer, so this driver runs the SAME pilot code (pilot.run_family: 1,000 rows, seed base 900000, G2 G3 G4 G-SL G-LEX G-TW
G15 + G6 G7 G10 overlay and spec 3.0) with its output folder renamed to pilot_i1/ (rows.jsonl, relations.jsonl,
PILOT_REPORT.json, g5h/ and g3h/ task files). It answers nothing: the Haiku G5-H / G3-H reads come later.

  ../../.venv/bin/python -B transfer/T36/pilot_i1.py [--dry-run]       (from lean/c2_build)
"""
from __future__ import annotations

import argparse
import contextlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

import pilot  # noqa: E402
import pilot_loaders as PL  # noqa: E402

OUT = "pilot_i1"


class _Dir:
    """kit.dir stand-in: pilot.run_family only does `kit.dir / "pilot"`; that folder becomes pilot_i1/."""

    def __init__(self, base: Path):
        self.base = base

    def __truediv__(self, name):
        return self.base / (OUT if name == "pilot" else name)


def run(write: bool = True, log=print) -> dict:
    orig = PL.open_family

    @contextlib.contextmanager
    def patched(fid):
        with orig(fid) as kit:
            kit.dir = _Dir(kit.dir)
            yield kit
    PL.open_family = patched
    try:
        return pilot.run_family("T36", pilot.N_ROWS, write=write, run_g15=True, log=log)
    finally:
        PL.open_family = orig


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dry-run", action="store_true", help="in memory: write nothing")
    a = ap.parse_args(argv)
    rep = run(write=not a.dry_run, log=lambda m: print(m, file=sys.stderr, flush=True))
    print(json.dumps({"summary": rep["summary"], "gate_lines": rep["gate_lines"],
                      "rows_sha256": rep["files"]["rows_sha256"]}, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

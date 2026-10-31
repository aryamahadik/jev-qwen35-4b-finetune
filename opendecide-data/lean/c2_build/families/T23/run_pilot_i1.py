"""families/T23/run_pilot_i1.py: the T23 pilot re-run of fix iteration 1 (C2_DATA_SPEC 6.4 step 6, iteration 1 of 2).

It is c2_build/pilot.py `run T23` with the output folder redirected from families/T23/pilot/ (the Stage B pilot, kept as
the record of the v3 run) to families/T23/pilot_i1/. Nothing in pilot.py, pilot_loaders.py or the kit is edited: the
loader's kit gets a `dir` whose "pilot" child is "pilot_i1". Same seeds (seed_base 900000), same 1,000 rows, same gates
(G2, G3, G4, G-SL, G-LEX, G-TW, G15, schema, options, G6, G7, G10, overlay, spec 3.0) and the same Haiku chunk files (G5-H
100 rows x 2 blind reads, G3-H every Mode F row); the task files are written and NOT answered.

  ../../.venv/bin/python -B families/T23/run_pilot_i1.py --dry-run     (in memory: prints the row / relation sha256s)
  ../../.venv/bin/python -B families/T23/run_pilot_i1.py               (writes families/T23/pilot_i1/)

Determinism (task order: two PYTHONHASHSEEDs): run --dry-run under PYTHONHASHSEED=0 and =1 and compare the two sha256 lines.
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

OUT_NAME = "pilot_i1"


class _Redirect:
    """kit.dir stand-in: `kit.dir / "pilot"` is the iteration's folder, any other child is unchanged."""

    def __init__(self, base: Path):
        self.base = base

    def __truediv__(self, name):
        return self.base / (OUT_NAME if name == "pilot" else name)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dry-run", action="store_true", help="in memory: write nothing")
    ap.add_argument("--n", type=int, default=pilot.N_ROWS)
    a = ap.parse_args(argv)
    orig = PL.open_family

    @contextlib.contextmanager
    def _open(fid):
        with orig(fid) as kit:
            kit.dir = _Redirect(kit.dir)
            yield kit

    PL.open_family = _open
    try:
        rep = pilot.run_family("T23", a.n, write=not a.dry_run, log=lambda m: print(m, file=sys.stderr, flush=True))
    finally:
        PL.open_family = orig
    print(json.dumps({"rows_sha256": rep["files"]["rows_sha256"], "relations_sha256": rep["files"]["relations_sha256"],
                      "n_rows": rep["files"]["n_rows"], "summary": rep["summary"], "written": rep["written"],
                      "gate_lines": rep["gate_lines"]}, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

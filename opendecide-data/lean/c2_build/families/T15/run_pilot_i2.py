"""families/T15/run_pilot_i2.py: the T15 pilot of fix iteration 2 (C2_DATA_SPEC 6.4 steps 5-6), written to pilot_i2/.

pilot.py writes a family's pilot to <family dir>/pilot/; iteration 0 lives there and stays untouched (its
PILOT_REPORT.json and PILOT_VERDICT.json are the record the fixes answer). This driver runs the same
`pilot.run_family` (the same build, gates, G5-H / G3-H task files, report) with only the output folder redirected to
pilot_i2/. Program gates only: G2, G3, G4, G-SL, G-LEX, G-TW, G15, schema, options, G6, G7, G10, overlay, spec 3.0.
G3-H and G5-H stay pending: the task files are written, never answered here (the re-reads come later).

  ../../.venv/bin/python -B families/T15/run_pilot_i2.py                 (from lean/c2_build; ~12 min)
  ../../.venv/bin/python -B families/T15/run_pilot_i2.py --dry-run       (in memory, writes nothing, prints the sha256s)

Determinism: run it under two PYTHONHASHSEEDs and compare the printed rows_sha256 / relations_sha256.
"""
from __future__ import annotations

import argparse
import contextlib
import dataclasses
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

import pilot  # noqa: E402
import pilot_loaders as PL  # noqa: E402

OUT_NAME = "pilot_i2"


class _RedirectDir(type(Path())):
    """kit.dir whose `/ "pilot"` (pilot.run_family's output folder) is `/ pilot_i2` instead."""

    def __truediv__(self, key):
        if key == "pilot":
            return Path(str(self)) / OUT_NAME
        return super().__truediv__(key)


@contextlib.contextmanager
def _open_family_i2(fid, _orig=PL.open_family):
    with _orig(fid) as kit:
        yield dataclasses.replace(kit, dir=_RedirectDir(kit.dir))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--n", type=int, default=pilot.N_ROWS)
    ap.add_argument("--dry-run", action="store_true", help="in memory: write nothing")
    ap.add_argument("--no-g15", action="store_true", help="skip G15 (speed; never for the real pilot)")
    a = ap.parse_args(argv)
    PL.open_family = _open_family_i2                     # pilot.PL is this module object
    rep = pilot.run_family("T15", a.n, write=not a.dry_run, run_g15=not a.no_g15,
                           log=lambda m: print(m, file=sys.stderr, flush=True))
    print(json.dumps({"family": rep["family"], "rows_sha256": rep["files"]["rows_sha256"],
                      "relations_sha256": rep["files"]["relations_sha256"], "n_rows": rep["files"]["n_rows"],
                      "summary": rep["summary"], "gate_lines": rep["gate_lines"]}, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

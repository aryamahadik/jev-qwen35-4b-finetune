"""families/T40/run_pilot_i1.py: the T40 CALL-GATE pilot (C2_DATA_SPEC 6.4 steps 5-6), same pattern as families/T28/run_pilot_i1.py.

T40 has no frozen pool, so this runner first registers the family at RUNTIME (families.T40.loader.register(): the kit's
FAMILIES registry and pilot_loaders.LOADERS; neither file is edited), then runs `pilot.run_family("T40", ...)` with the output
folder redirected to pilot_i1/. Program gates only (G2, G3, G4, G-SL, G-LEX, G-TW, G15, schema, options, G6, G7, G10, overlay);
G3-H and G5-H task files are written, never answered here.

  ../../.venv/bin/python -B families/T40/run_pilot_i1.py --dry-run --n 600     (in memory, writes nothing, prints sha256s)
  ../../.venv/bin/python -B families/T40/run_pilot_i1.py                      (from lean/c2_build; WRITES pilot_i1/: only on the
                                                                                orchestrator's go, never during the build task)
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
from families.T40 import loader  # noqa: E402

OUT_NAME = "pilot_i1"


class _RedirectDir(type(Path())):
    """kit.dir whose `/ "pilot"` (pilot.run_family's output folder) is `/ pilot_i1` instead."""

    def __truediv__(self, key):
        if key == "pilot":
            return Path(str(self)) / OUT_NAME
        return super().__truediv__(key)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--n", type=int, default=pilot.N_ROWS)
    ap.add_argument("--dry-run", action="store_true", help="in memory: write nothing")
    ap.add_argument("--no-g15", action="store_true", help="skip G15 (speed; never for the real pilot)")
    a = ap.parse_args(argv)
    loader.register()
    orig = PL.open_family

    @contextlib.contextmanager
    def open_family_i1(fid):
        with orig(fid) as kit:
            yield dataclasses.replace(kit, dir=_RedirectDir(kit.dir))

    PL.open_family = open_family_i1                      # pilot.PL is this module object
    rep = pilot.run_family("T40", a.n, write=not a.dry_run, run_g15=not a.no_g15,
                           log=lambda m: print(m, file=sys.stderr, flush=True))
    print(json.dumps({"family": rep["family"], "rows_sha256": rep["files"]["rows_sha256"],
                      "relations_sha256": rep["files"]["relations_sha256"], "n_rows": rep["files"]["n_rows"],
                      "summary": rep["summary"], "gate_lines": rep["gate_lines"]}, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

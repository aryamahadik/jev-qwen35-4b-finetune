"""families/T45/run_pilot_i1.py: the T45 pilot driver (C2_DATA_SPEC 6.4 steps 5-6), same pattern as families/T28/run_pilot_i1.py.

pilot.py writes a family's pilot to <family dir>/pilot/; this driver runs the same `pilot.run_family` (the same build,
gates and report) with the output folder redirected to pilot_i1/, and registers the T45 loader at RUNTIME
(pilot_loaders.LOADERS["T45"]; pilot_loaders.py is not edited). Program gates only: G2, G3, G4, G-SL, G-LEX, G15,
schema, options, G6, G7, G10, spec 3.0. G3-H and G5-H stay pending (task files only; nothing here runs a model).

T45 has choice rows only (6-way outcome head + 4-way next-move head), so the yes/no-only checks of G10 and the overlay
(yes rate, negation shares, complement shares) have no rows to measure: this driver marks exactly those checks "n/a"
when the build holds no yes/no row (the same treatment pilot.g10 already gives yes_no_share for YES_NO_ONLY families).
Every bar that has rows to measure is untouched. Kit candidate: a CHOICE_ONLY flag in pilot.g10 / pilot.overlay.

  ../../.venv/bin/python -B families/T45/run_pilot_i1.py --dry-run --n 300      (from lean/c2_build; writes nothing)
  ../../.venv/bin/python -B families/T45/run_pilot_i1.py                        (the real pilot: writes pilot_i1/; needs A38)
  options: --n ROWS (default pilot.N_ROWS), --no-g15 (skip G15; never for the real pilot), --dry-run
Determinism: run it under two PYTHONHASHSEEDs and compare rows_sha256.
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

OUT_NAME = "pilot_i1"
YN_G10 = ("yes_no_share", "yes_rate", "yes_rate_cells", "yes_is_bad_share", "syntactic_negation_share",
          "double_negation_share", "attack_x_label")
YN_OVERLAY = ("complement_share_of_yes_no", "non_syntactic_share_of_pairs")


class _RedirectDir(type(Path())):
    def __truediv__(self, key):
        if key == "pilot":
            return Path(str(self)) / OUT_NAME
        return super().__truediv__(key)


@contextlib.contextmanager
def _t45():
    from families.T45 import plugin as P
    plugin, ctx = P.make_plugin()
    yield PL.FamilyKit("T45", PL.family_dir("T45"), plugin, ctx, "families/T45/plugin.make_plugin() -> (T45Plugin, ctx)",
                       "in code (program text only: rules, legends, wordings and layouts; no Haiku pool yet)",
                       ["the 6 question wordings are admitted in the lexicon by program stand-ins "
                        "('program:stand-in-N'); the Haiku 2/2 admission is still to run"])


@contextlib.contextmanager
def _open_family_i1(fid, _orig=None):
    with PL.LOADERS[fid]() as kit:
        yield dataclasses.replace(kit, dir=_RedirectDir(kit.dir))


def _na(checks: dict, names, why: str) -> None:
    for n in names:
        if n in checks and checks[n]["verdict"] == "fail":
            checks[n] = {**checks[n], "verdict": "n/a", "note": why}


def install_patches() -> None:
    orig_g10, orig_overlay = pilot.g10, pilot.overlay

    def g10(infos, units, plugin):
        r = orig_g10(infos, units, plugin)
        if not any(i.row["qtype"] == "noul" for i in infos):
            _na(r["checks"], YN_G10, "no yes/no rows in this family (choice only)")
            r["failing"] = sorted(k for k, v in r["checks"].items() if v["verdict"] == "fail")
            r["verdict"] = "pass" if not r["failing"] else "fail"
        return r

    def overlay(units, plugin):
        r = orig_overlay(units, plugin)
        rows = [x for u in units for x in u.rows]
        if not any(x["qtype"] == "noul" for x in rows):
            _na(r["checks"], YN_OVERLAY, "no yes/no rows in this family (choice only)")
            r["failing"] = sorted(k for k, v in r["checks"].items() if v["verdict"] == "fail")
            r["verdict"] = "pass" if not r["failing"] else "fail"
        return r
    pilot.g10, pilot.overlay = g10, overlay


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--n", type=int, default=pilot.N_ROWS)
    ap.add_argument("--dry-run", action="store_true", help="in memory: write nothing")
    ap.add_argument("--no-g15", action="store_true", help="skip G15 (speed; never for the real pilot)")
    a = ap.parse_args(argv)
    PL.LOADERS["T45"] = _t45
    install_patches()
    PL.open_family = _open_family_i1                     # pilot.PL is this module object
    rep = pilot.run_family("T45", a.n, write=not a.dry_run, run_g15=not a.no_g15,
                           log=lambda m: print(m, file=sys.stderr, flush=True))
    print(json.dumps({"family": rep["family"], "rows_sha256": rep["files"]["rows_sha256"],
                      "relations_sha256": rep["files"]["relations_sha256"], "n_rows": rep["files"]["n_rows"],
                      "summary": rep["summary"], "gate_lines": rep["gate_lines"]}, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

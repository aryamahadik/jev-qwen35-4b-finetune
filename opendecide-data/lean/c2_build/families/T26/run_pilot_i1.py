"""families/T26/run_pilot_i1.py: the T26 pilot of fix iteration 1 (C2_DATA_SPEC 6.4 steps 5-6), written to pilot_i1/.
Same driver as run_pilot.py (T26's own pool loader, registered at runtime; pilot_loaders.py is not edited) with `--out`
defaulting to pilot_i1 (iteration 0 stays untouched in pilot/), plus `--g6-at-size`: with --dry-run it builds --n rows in
memory (G15 off) and writes pilot_i1/G6_AT_<n>.json with the fields zed_orch/g6_at_size.py writes (A43: the pilot
verdict's G6 is computed on >= 5,000 QC rows):

  ../../.venv/bin/python -B families/T26/run_pilot_i1.py                                  (fix iteration 1)
  ../../.venv/bin/python -B families/T26/run_pilot_i1.py --dry-run --n 6000 --no-g15 --g6-at-size

Original docstring of run_pilot.py:

T26 had no pilot loader in pilot_loaders.py, and other family leads edit that shared file in parallel, so the loader
lives in families/T26/loader.py and is registered into `pilot_loaders.LOADERS` in this process only (no shared file is
edited). The loader follows freeze_v2.LOADER_NOTE (pools_v2/, sha256-checked) and installs the frozen Haiku pack pool
for the span of the run.

pilot.py writes a family's pilot to <family dir>/pilot/. `--out pilot` (the default) is iteration 0, `--out pilot_i1`
is fix iteration 1 (the same `pilot.run_family`: the same build, gates, G5-H / G3-H task files and report, only the
output folder redirected). Program gates only: G2, G3, G4, G-SL, G-LEX, G-TW, G15, schema, options, G6, G7, G10,
overlay, spec 3.0. G3-H and G5-H stay pending: the task files are written, never answered here.

  ../../.venv/bin/python -B families/T26/run_pilot.py --out pilot       (from lean/c2_build; iteration 0)
  ../../.venv/bin/python -B families/T26/run_pilot.py --out pilot_i1    (fix iteration 1)
  add --dry-run to run in memory (nothing written); run under two PYTHONHASHSEEDs and compare the sha256s.
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
from families.T26 import loader as LD  # noqa: E402


@contextlib.contextmanager
def _t26():
    with LD.open_t26() as kit:
        yield PL.FamilyKit("T26", PL.family_dir("T26"), kit.plugin, kit.ctx,
                           "families/T26/loader.py: pools_v2/ (sha-checked, freeze_v2.LOADER_NOTE) + the frozen Haiku "
                           "pack pool installed over plugin.PACKS_TRAIN / PACKS_HELD_OUT", "pools_v2/", kit.notes)


def _redirect(out_name: str):
    class _RedirectDir(type(Path())):
        """kit.dir whose `/ "pilot"` (pilot.run_family's output folder) is `/ <out_name>` instead."""

        def __truediv__(self, key):
            if key == "pilot":
                return Path(str(self)) / out_name
            return super().__truediv__(key)

    @contextlib.contextmanager
    def open_family(fid, _orig=_t26):
        with _orig() as kit:
            yield dataclasses.replace(kit, dir=_RedirectDir(kit.dir))
    return open_family


def _g6_at_size(a) -> int:
    """zed_orch/g6_at_size.py for this runner: build_pilot in memory at the pilot seed base, G15 off, then g6 / g7 / g10."""
    import time
    t0 = time.time()
    with PL.open_family("T26") as kit:
        b = pilot.build_pilot(kit, a.n, run_g15=False, log=lambda m: print(m, file=sys.stderr, flush=True))
        g6, g7 = pilot.g6(b.infos), pilot.g7(b.infos)
        g10 = pilot.g10(b.infos, b.units, kit.plugin)
        ov, sp = pilot.overlay(b.units, kit.plugin), pilot.spec30(b.infos, kit.plugin)
        outdir = Path(PL.family_dir("T26")) / a.out
    cells = {}
    for part in ("yes_no", "choice"):
        p = g6.get(part) or {}
        if p.get("n"):
            cells[part] = {"n": p["n"], "chance": p["chance"],
                           "max": max((p[v][m], v, m) for v in p if isinstance(p[v], dict) and "lr" in p[v]
                                      for m in ("lr", "gbt"))}
    out = {"family": "T26", "n_rows": len(b.infos), "seconds": round(time.time() - t0), "seed_base": pilot.SEED_BASE,
           "G6_verdict": g6["verdict"], "G6_fails": g6["fails"], "G6_cells_max": cells,
           "G7_verdict": g7.get("verdict"), "G10_verdict": g10.get("verdict"),
           "G10_fails": {k: v for k, v in (g10.get("checks") or {}).items() if v.get("verdict") == "fail"},
           "G10_yes_rate_cells": (g10.get("checks") or {}).get("yes_rate_cells"),
           "overlay_verdict": ov.get("verdict"), "spec_3_0_verdict": sp.get("verdict"),
           "spec_3_0": {k: v.get("value") for k, v in sp["checks"].items()}}
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / f"G6_AT_{a.n}.json").write_text(json.dumps(out, indent=1, default=str))
    print(json.dumps({k: out[k] for k in ("family", "n_rows", "G6_verdict", "G7_verdict", "G10_verdict", "seconds")}))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--n", type=int, default=pilot.N_ROWS)
    ap.add_argument("--out", default="pilot_i1", help="output folder under families/T26 (pilot or pilot_i1)")
    ap.add_argument("--dry-run", action="store_true", help="in memory: write nothing")
    ap.add_argument("--no-g15", action="store_true", help="skip G15 (speed; never for the real pilot)")
    ap.add_argument("--g6-at-size", action="store_true",
                    help="with --dry-run: build --n rows in memory and write G6_AT_<n>.json (G6, G7, G10) into --out")
    a = ap.parse_args(argv)
    PL.LOADERS["T26"] = _t26
    PL.open_family = _redirect(a.out)                             # pilot.PL is this module object
    if a.g6_at_size:
        return _g6_at_size(a)
    rep = pilot.run_family("T26", a.n, write=not a.dry_run, run_g15=not a.no_g15,
                           log=lambda m: print(m, file=sys.stderr, flush=True))
    print(json.dumps({"family": rep["family"], "rows_sha256": rep["files"]["rows_sha256"],
                      "relations_sha256": rep["files"]["relations_sha256"], "n_rows": rep["files"]["n_rows"],
                      "summary": rep["summary"], "gate_lines": rep["gate_lines"]}, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""families/T27/run_pilot_i1.py: the T27 pilot of fix iteration 1 (C2_DATA_SPEC 6.4 steps 5-6), written to pilot_i1/.

Iteration 0 lives in pilot/ and stays untouched. T27 has no entry in the shared pilot_loaders.py, so this driver
registers T27's loader (reused from run_pilot.py: pools_v2 read_pools / require_ready / install_vocab / build_ctx)
into `pilot_loaders.LOADERS` in this process only, redirects the output folder to pilot_i1/ and runs the same
`pilot.run_family` (same build, gates, G5-H / G3-H task files, report). Program gates only: G2, G3, G4, G-SL, G-LEX,
G-TW, G15, schema, options, G6, G7, G10, overlay, spec 3.0. G5-H / G3-H task files are written, never answered here.

  ../../.venv/bin/python -B families/T27/run_pilot_i1.py                      (from lean/c2_build)
  ../../.venv/bin/python -B families/T27/run_pilot_i1.py --dry-run            (in memory; prints the sha256s)
  ../../.venv/bin/python -B families/T27/run_pilot_i1.py --dry-run --n 6000 --no-g15 --g6-at-size
        (A43: G6 / G7 / G10 on >= 5,000 QC rows, in memory; writes pilot_i1/G6_AT_<n>.json, the fields of
         zed_orch/g6_at_size.py)

Determinism: run under two PYTHONHASHSEEDs and compare rows_sha256 / relations_sha256.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2_BUILD = HERE.parents[1]
for p in (str(C2_BUILD), str(HERE)):
    if p not in sys.path:
        sys.path.insert(0, p)

import pilot  # noqa: E402
import pilot_loaders as PL  # noqa: E402
import run_pilot as RP  # noqa: E402  (families/T27/run_pilot.py: the T27 loader and the output redirect)

OUT_NAME = "pilot_i1"


def _g6_at_size(rep: dict, n: int) -> dict:
    g = rep["gates"]
    g6, g7, g10 = g["G6"], g["G7"], g["G10"]
    cells = {}
    for part in ("yes_no", "choice"):
        p = g6.get(part) or {}
        if p.get("n"):
            cells[part] = {"n": p["n"], "chance": p["chance"],
                           "max": max((p[v][m], v, m) for v in p if isinstance(p[v], dict) and "lr" in p[v]
                                      for m in ("lr", "gbt"))}
    return {"family": "T27", "n_rows": rep["files"]["n_rows"], "seconds": rep["build"].get("seconds"),
            "seed_base": pilot.SEED_BASE, "G6_verdict": g6["verdict"], "G6_fails": g6["fails"],
            "G6_cells_max": cells, "G7_verdict": g7.get("verdict"), "G10_verdict": g10.get("verdict"),
            "G10_fails": {k: v for k, v in (g10.get("checks") or {}).items() if v.get("verdict") == "fail"},
            "G10_yes_rate_cells": (g10.get("checks") or {}).get("yes_rate_cells")}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--n", type=int, default=pilot.N_ROWS)
    ap.add_argument("--dry-run", action="store_true", help="in memory: write nothing")
    ap.add_argument("--no-g15", action="store_true", help="skip G15 (speed; never for the real pilot)")
    ap.add_argument("--g6-at-size", action="store_true", help="also write pilot_i1/G6_AT_<n>.json (A43; with --dry-run)")
    a = ap.parse_args(argv)
    PL.LOADERS["T27"] = RP._t27
    PL.open_family = RP._redirect(OUT_NAME)                       # pilot.PL is this module object
    rep = pilot.run_family("T27", a.n, write=not a.dry_run, run_g15=not a.no_g15,
                           log=lambda m: print(m, file=sys.stderr, flush=True))
    if a.g6_at_size:
        out = _g6_at_size(rep, a.n)
        d = PL.family_dir("T27") / OUT_NAME
        d.mkdir(parents=True, exist_ok=True)
        (d / f"G6_AT_{a.n}.json").write_text(json.dumps(out, indent=1, default=str))
    print(json.dumps({"family": rep["family"], "rows_sha256": rep["files"]["rows_sha256"],
                      "relations_sha256": rep["files"]["relations_sha256"], "n_rows": rep["files"]["n_rows"],
                      "summary": rep["summary"], "gate_lines": rep["gate_lines"]}, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

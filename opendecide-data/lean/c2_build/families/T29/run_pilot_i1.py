"""c2_build/families/T29/run_pilot_i1.py: the T29 pilot of fix iteration 1 (C2_DATA_SPEC 6.4 step 6), into pilot_i1/.

c2_build/pilot.py (pinned) writes a family's pilot to <family dir>/pilot/. This driver runs the SAME pilot code
(pilot.run_family: the program gates G2, G3, G4, G-SL, G-LEX, G-TW, G15, schema, options; G6, G7, G10, overlay, spec 3.0;
the G5-H and G3-H task files) with the family folder presented to it as one whose "pilot" folder is "pilot_i1". Nothing
else differs: same loader (pilot_loaders._t29, frozen pools sha-checked), same seeds (SEED_BASE 900,000), same bars. It
never answers a Haiku task and never runs a model; the stage-A answers in pilot/ are not read.

  ../.venv/bin/python -B families/T29/run_pilot_i1.py [--dry-run] [--n 1000]        (from lean/c2_build)
Run it under two PYTHONHASHSEED values and compare PILOT_REPORT.json files.rows_sha256 for the determinism check
(--dry-run prints the sha instead of writing).
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

import pilot as PI  # noqa: E402
import pilot_loaders as PL  # noqa: E402

OUT = "pilot_i1"


class _Dir:
    """The family dir as run_family sees it: dir / "pilot" is the iteration's folder."""

    def __init__(self, base: Path):
        self.base = base

    def __truediv__(self, name):
        return self.base / (OUT if name == "pilot" else name)

    def __fspath__(self):
        return str(self.base)

    def __str__(self):
        return str(self.base)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--n", type=int, default=PI.N_ROWS)
    ap.add_argument("--gates", default="", help="comma list of gate names whose full report is printed (e.g. G6,G10)")
    a = ap.parse_args(argv)
    orig = PL.open_family

    @contextlib.contextmanager
    def patched(fid):
        with orig(fid) as kit:
            kit.dir = _Dir(kit.dir)
            yield kit

    PL.open_family = patched
    try:
        rep = PI.run_family("T29", a.n, write=not a.dry_run, run_g15=True,
                            log=lambda m: print(m, file=sys.stderr, flush=True))
    finally:
        PL.open_family = orig
    for g in [x for x in a.gates.split(",") if x]:
        print(f"=== {g}\n" + json.dumps(rep["gates"][g], indent=1, ensure_ascii=False, default=str))
    print(json.dumps({"summary": rep["summary"], "gate_lines": rep["gate_lines"],
                      "rows_sha256": rep["files"]["rows_sha256"], "relations_sha256": rep["files"]["relations_sha256"],
                      "n_rows": rep["files"]["n_rows"], "written": rep["written"]}, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""transfer/T20/run_pilot_i1.py: the T20 pilot after fix iteration 1 (PILOT_VERDICT F1-F6; G0_SPEC.md v3), written to
pilot_i1/.

c2_build/pilot.py always writes to <family dir>/pilot/ (the first pilot, kept as evidence). This wrapper runs the very same
code (pilot.run_family: same seeds, loader, gates and bars; nothing is loosened) with the output folder renamed to
pilot_i1/, so the first pilot's files stay untouched. It writes the program-gate PILOT_REPORT.json, rows, relations and the
G5-H / G3-H task files; it answers none of them (Haiku answers come later; A37 b).

One addition to the G5-H sample (F5, verdict: "G5-H on the re-pilot must read at least 10 yn_double_neg rows"): the seeded
order of the rows is kept, but its first DN_READ_MIN yn_double_neg rows come first, so the 100 rows read hold at least that
many double-negation rows (a seeded draw of 100 of 1,000 rows holds about 2). It reads the question form only, never a gold.

  cd lean/c2_build
  ../../.venv/bin/python -B transfer/T20/run_pilot_i1.py                      # the pilot, written to transfer/T20/pilot_i1/
  PYTHONHASHSEED=7 ../../.venv/bin/python -B transfer/T20/run_pilot_i1.py --dry-run   # in memory; prints the rows sha256
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

import pilot as PI  # noqa: E402
import pilot_loaders as PL  # noqa: E402
from c2_kit import g5h  # noqa: E402

OUT = "pilot_i1"
DN_FORM = "yn_double_neg"
DN_READ_MIN = 12          # F5: the G5-H read must include at least 10 yn_double_neg rows (verdict); 12 leaves a margin


class _Redirect:
    """kit.dir stand-in: `kit.dir / "pilot"` (the only use in run_family) resolves to <family dir>/pilot_i1."""

    def __init__(self, real: Path):
        self.real = real

    def __truediv__(self, name):
        return self.real / (OUT if name == "pilot" else name)

    def __fspath__(self):
        return str(self.real)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--n", type=int, default=PI.N_ROWS)
    ap.add_argument("--dry-run", action="store_true", help="in memory only: write nothing")
    ap.add_argument("--no-g15", action="store_true")
    a = ap.parse_args(argv)
    orig = PL.open_family

    def open_family(fid):
        cm = orig(fid)

        class _Cm:
            def __enter__(self):
                kit = cm.__enter__()
                kit.dir = _Redirect(kit.dir)
                return kit

            def __exit__(self, *e):
                return cm.__exit__(*e)
        return _Cm()

    PL.open_family = open_family
    seeded = g5h.sample_rows

    def sample_rows(rows, n, seed):
        order = seeded(rows, n, seed)
        dn = [r for r in order if r["meta"]["qform"] == DN_FORM][:DN_READ_MIN]
        taken = {id(r) for r in dn}
        return (dn + [r for r in order if id(r) not in taken])[:n]

    g5h.sample_rows = sample_rows
    rep = PI.run_family("T20", a.n, write=not a.dry_run, run_g15=not a.no_g15,
                        log=lambda m: print(m, file=sys.stderr, flush=True))
    print(json.dumps({"summary": rep["summary"], "rows_sha256": rep["files"]["rows_sha256"],
                      "relations_sha256": rep["files"]["relations_sha256"], "n_rows": rep["files"]["n_rows"],
                      "gate_lines": rep["gate_lines"]}, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

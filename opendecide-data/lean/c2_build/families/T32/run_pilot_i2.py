"""families/T32/run_pilot_i2.py: re-run the T32 pilot after fix iteration 2 into pilot_i2/ (C2_DATA_SPEC 6.4 steps 5-6).

pilot.py writes to <family folder>/pilot/ (the first pilot, which stays untouched: PILOT_REPORT.json, rows, the Haiku
answers and PILOT_VERDICT.json are the record the fixes were made from). This wrapper runs the SAME pilot code
(pilot.run_family: G2, G3, G4, G-SL, G-LEX, G-TW, G15, schema, options, G6, G7, G10, overlay, spec 3.0, and the G5-H /
G3-H task files) with the output folder redirected to pilot_i2/, through one path object that answers `/ "pilot"` with
`pilot_i2`. Nothing else of pilot.py or pilot_loaders.py changes, no Haiku task is answered (the task files are only
written) and nothing is committed.

  ../.venv/bin/python -B families/T32/run_pilot_i2.py run [--n 1000] [--dry-run]     (from lean/c2_build)
  ../.venv/bin/python -B families/T32/run_pilot_i2.py determinism [--n 300]          (rows sha256 under two hash seeds)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

OUT = "pilot_i2"


class _RedirectDir(type(Path())):
    """The family folder, except that `/ "pilot"` is the iteration's output folder."""

    def __truediv__(self, key):
        return Path(str(self)) / (OUT if key == "pilot" else key)


def run(n: int, dry: bool) -> dict:
    import pilot
    import pilot_loaders as PL

    real = PL.LOADERS["T32"]

    def loader():
        import contextlib

        @contextlib.contextmanager
        def cm():
            with real() as kit:
                kit.dir = _RedirectDir(str(kit.dir))
                sys.path.insert(0, str(Path(__file__).resolve().parent))
                from dneg_stage2 import apply_supplement
                apply_supplement(kit)       # F8: no-op until dneg_stage3.py has written haiku/dneg_i2/pool_supplement.json
                yield kit
        return cm()

    PL.LOADERS["T32"] = loader
    try:
        rep = pilot.run_family("T32", n, write=not dry, run_g15=True, log=lambda m: print(m, file=sys.stderr, flush=True))
    finally:
        PL.LOADERS["T32"] = real
    print(json.dumps({"summary": rep["summary"], "gate_lines": rep["gate_lines"]}, indent=1, ensure_ascii=False))
    return rep


def rows_sha(n: int) -> str:
    """sha256 of the rows of an in-memory build of the first n rows (no G15; nothing written)."""
    import pilot
    import pilot_loaders as PL
    with PL.open_family("T32") as kit:
        b = pilot.build_pilot(kit, n, run_g15=False)
        body = "".join(json.dumps(i.row, ensure_ascii=False, sort_keys=True) + "\n" for i in b.infos)
        rels = "".join(json.dumps(r, sort_keys=True) + "\n" for r in b.rels)
    return hashlib.sha256((body + "\x00" + rels).encode()).hexdigest()


def determinism(n: int) -> dict:
    out = {}
    for seed in ("1", "2"):
        env = dict(os.environ, PYTHONHASHSEED=seed)
        r = subprocess.run([sys.executable, "-B", str(Path(__file__)), "sha", "--n", str(n)], env=env,
                           capture_output=True, text=True, check=True)
        out[f"PYTHONHASHSEED={seed}"] = r.stdout.strip().splitlines()[-1]
    out["identical"] = len(set(out.values())) == 1
    out["rows_requested"] = n
    print(json.dumps(out, indent=1))
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=("run", "determinism", "sha"))
    ap.add_argument("--n", type=int, default=1000)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    if a.cmd == "run":
        run(a.n, a.dry_run)
    elif a.cmd == "sha":
        print(rows_sha(a.n))
    else:
        determinism(a.n)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

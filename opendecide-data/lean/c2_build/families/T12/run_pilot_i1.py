"""families/T12/run_pilot_i1.py: the T12 pilot of fix iteration 1 (C2_DATA_SPEC 6.4 step 6, then step 5 again).

The same code as `pilot.py run T12` (pilot.run_family: build_pilot over the frozen pools_v2, the program gates G2, G3, G4,
G-SL, G-LEX, G-TW, G15 and the row schema, options, G6, G7, G10, the overlay report, spec 3.0, and the G5-H / G3-H task
files), written to families/T12/pilot_i1/ instead of pilot/ (pilot.py hard-codes `<family dir>/pilot`; this script hands
it a family directory whose "pilot" entry is "pilot_i1", so no shared file is edited and pilot/, the Stage B record, is
never touched). Same seeds (seed_base 900000), same 1,000 rows. No Haiku, no model, no network: the G5-H and G3-H task
files are written and NOT answered.

  ../.venv/bin/python -B families/T12/run_pilot_i1.py run           (from lean/c2_build) writes pilot_i1/
  ../.venv/bin/python -B families/T12/run_pilot_i1.py dry           in memory; prints the rows / relations sha256
  ../.venv/bin/python -B families/T12/run_pilot_i1.py determinism   dry under PYTHONHASHSEED 1 and 4242, compare
"""
from __future__ import annotations

import contextlib
import json
import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

OUT = "pilot_i1"


def _redirect(dir_path: Path):
    class _Dir(type(Path())):
        def __truediv__(self, key):
            return Path(self) / (OUT if key == "pilot" else key)
    return _Dir(dir_path)


def run(write: bool) -> dict:
    import pilot
    import pilot_loaders as PL
    real = PL.open_family

    @contextlib.contextmanager
    def patched(fid):
        with real(fid) as kit:
            kit.dir = _redirect(kit.dir)
            yield kit
    PL.open_family = patched
    try:
        return pilot.run_family("T12", pilot.N_ROWS, write=write, run_g15=True,
                                log=lambda m: print(m, file=sys.stderr, flush=True))
    finally:
        PL.open_family = real


def main(argv=None) -> int:
    cmd = (argv or sys.argv[1:] or ["run"])[0]
    if cmd == "determinism":
        procs = [subprocess.Popen([sys.executable, "-B", __file__, "dry"], stdout=subprocess.PIPE,
                                  stderr=subprocess.DEVNULL, text=True, env={**os.environ, "PYTHONHASHSEED": hs})
                 for hs in ("1", "4242")]
        outs = [json.loads(p.communicate()[0]) for p in procs]
        same = outs[0] == outs[1]
        print(json.dumps({"identical": same, "runs": outs}, indent=1))
        return 0 if same else 1
    rep = run(write=(cmd == "run"))
    if cmd == "dry":
        f = rep["files"]
        import hashlib
        chunks = hashlib.sha256(json.dumps(rep["chunks"], sort_keys=True).encode("utf-8")).hexdigest()
        print(json.dumps({"rows_sha256": f["rows_sha256"], "relations_sha256": f["relations_sha256"],
                          "n_rows": f["n_rows"], "n_relations": f["n_relations"], "task_files_sha256": chunks}))
        return 0
    print(json.dumps({"summary": rep["summary"], "gate_lines": rep["gate_lines"]}, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

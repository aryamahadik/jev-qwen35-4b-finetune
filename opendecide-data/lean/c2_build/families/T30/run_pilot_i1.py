"""families/T30/run_pilot_i1.py: the fix-iteration-1 pilot of T30 into families/T30/pilot_i1/ (C2_DATA_SPEC 6.4 step 5).

Runs c2_build/pilot.py `run T30` unchanged (same loader, seeds from 900000, gates, G5-H / G3-H task files); the only
difference is the output folder: pilot.py writes `<family dir>/pilot`, this driver hands it a family dir whose
"pilot" entry is "pilot_i1", so the iteration-0 pilot/ (rows, report, verdict, the two readers' answers) stays as it
was. No Haiku, no model, no paid compute. The G5-H / G3-H task files are written, never answered.

  cd lean/c2_build && ../../.venv/bin/python -B families/T30/run_pilot_i1.py            (writes pilot_i1/)
  cd lean/c2_build && PYTHONHASHSEED=4242 ../../.venv/bin/python -B families/T30/run_pilot_i1.py --dry-run
"""
from __future__ import annotations

import contextlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[2]
if str(C2) not in sys.path:
    sys.path.insert(0, str(C2))

import pilot as PI  # noqa: E402
import pilot_loaders as PL  # noqa: E402

OUT = "pilot_i1"


class _Dir:
    """Stands in for FamilyKit.dir: `dir / "pilot"` is `<family dir>/pilot_i1`; everything else is the real path."""

    def __init__(self, real: Path):
        self.real = real

    def __truediv__(self, name: str) -> Path:
        return self.real / (OUT if name == "pilot" else name)


_open = PL.open_family


@contextlib.contextmanager
def _open_i1(fid: str):
    with _open(fid) as kit:
        kit.dir = _Dir(kit.dir)
        yield kit


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    dry = "--dry-run" in argv
    PL.open_family = _open_i1
    rep = PI.run_family("T30", write=not dry, run_g15=True, log=lambda m: print(m, file=sys.stderr, flush=True))
    print(json.dumps({"summary": rep["summary"], "rows_sha256": rep["files"]["rows_sha256"],
                      "relations_sha256": rep["files"]["relations_sha256"], "gate_lines": rep["gate_lines"]},
                     indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""g13_c2_opt2.py: g13_c2.py with the owner options 2 (a) --frame-excuse, 2 (b) --kw-narrow and 3's --ohsac-report-only capture; each default OFF and
each armed only by an owner ruling id in PREREG_FINAL.md (see opt2_launch.py and README.md). No flag: g13_c2.main runs unchanged.
Run from lean/:  ../.venv/bin/python -B c2_build/zed_orch/owner_options/g13_c2_opt2.py candidates --block T28 [--frame-excuse A70] [--kw-narrow A71]"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import opt2_launch  # noqa: E402

if __name__ == "__main__":
    sys.exit(opt2_launch.launch())

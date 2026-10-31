"""c2_select_opt3.py: option 3 wrapper for selection (c2_select.py main). Without --ohsac-report-only <ruling id> it runs c2_select.main(argv) exactly as before
(default OFF). With it, the id must be an owner ruling in PREREG_FINAL.md carrying OHSAC_REPORT_ONLY (ruling_gate.py); see README.md and
ac_report_only.py. Run from lean/:  ../.venv/bin/python -B c2_build/zed_orch/owner_options/c2_select_opt3.py [--ohsac-report-only A68] <the usual arguments>"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ac_report_only as opt3  # noqa: E402

if __name__ == "__main__":
    sys.exit(opt3.launch("select"))

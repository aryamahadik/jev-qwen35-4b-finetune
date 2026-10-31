"""gen_full_c2_opt3.py: option 3 wrapper for the family builder (gen_full_c2.py main). Without --ohsac-report-only <ruling id> it runs
gen_full_c2.main(argv) exactly as before (default OFF). With it (owner ruling carrying OHSAC_REPORT_ONLY), a G13-seed quarantine entry whose
hits are ONLY OHS-AC targets is not applied (today only T27 honours the seed list: --g13-seed T27). See README.md and ac_report_only.py.
Run from lean/:  ../.venv/bin/python -B c2_build/zed_orch/owner_options/gen_full_c2_opt3.py [--ohsac-report-only A68] <the usual arguments>"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ac_report_only as opt3  # noqa: E402

if __name__ == "__main__":
    sys.exit(opt3.launch("genfull"))

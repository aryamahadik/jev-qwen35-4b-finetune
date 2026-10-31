"""A20 a adoption test 1: run F5's deterministic G10 gate (qc/g10.py candidates_r1) unchanged, with its output dir
qc_lib.QC redirected to argv[1], so the family's own qc/g10_candidates_r1.json is never touched."""
import runpy
import sys
from pathlib import Path

F5 = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F5")
sys.path.insert(0, str(F5 / "qc"))
import qc_lib as L  # noqa: E402

out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
L.QC = out
sys.argv = [str(F5 / "qc/g10.py"), "candidates_r1"]
runpy.run_path(str(F5 / "qc/g10.py"), run_name="__main__")

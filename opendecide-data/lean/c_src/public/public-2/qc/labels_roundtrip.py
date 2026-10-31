"""Label round-trip (extra check; G2/G3-style for program labels): re-run public-2's verify.py (read, unchanged) on
the CURRENT out files, with UCI car.data / nursery.data re-downloaded from UCI by g1.py (sha256 = manifest), output
redirected to qc/verify_out/ so the builder's own report is not overwritten."""
import json
import sys

from qclib import P2, QC, write_gate

sys.path.insert(0, str(P2))
import verify  # noqa: E402

verify.OUT = QC / "verify_out"
verify.RAW = QC / "upstream"
rc = verify.main()
res = json.load(open(QC / "verify_out" / "verify_report.json"))
write_gate("labels_roundtrip", rc == 0 and res["mismatches"] == 0, res)

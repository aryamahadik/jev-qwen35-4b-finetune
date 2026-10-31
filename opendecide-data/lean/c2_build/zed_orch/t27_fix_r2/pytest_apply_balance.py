"""pytest plugin (-p pytest_apply_balance, PYTHONPATH=zed_orch/t27_fix_r2): applies wording_balance to T27Plugin in the pytest process,
so the existing families/T27 tests run against the fixed generator before install_code.py is run (the files on disk are untouched)."""
import sys
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2 = HERE.parents[1]
for p in (str(C2), str(HERE)):
    if p not in sys.path:
        sys.path.insert(0, p)
from families.T27 import plugin as P  # noqa: E402
import wording_balance as WB  # noqa: E402
WB.apply(P.T27Plugin)

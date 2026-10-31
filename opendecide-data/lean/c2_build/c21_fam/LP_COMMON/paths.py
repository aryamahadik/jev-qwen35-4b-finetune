"""Locations of the L-0 infrastructure this lane imports (namespace.py, row_start_guard.py, the frozen names list v1.2)."""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
FAM = os.path.dirname(_HERE)
C2_BUILD = os.path.dirname(FAM)
INFRA = os.path.join(C2_BUILD, "c21_infra")
L0 = os.path.join(C2_BUILD, "zed_orch", "c21", "l0")
NAMES_MANIFEST = os.path.join(L0, "NAMES_MANIFEST_V1_2.json")
NAMES_MANIFEST_SHA = os.path.join(L0, "NAMES_MANIFEST_V1_2.sha256")

for _p in (INFRA, FAM):
    if _p not in sys.path:
        sys.path.insert(0, _p)

"""Locations of the L-0 infrastructure this lane imports (namespace.py, row_start_guard.py, the frozen names list)."""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
C2_BUILD = os.path.dirname(os.path.dirname(_HERE))
INFRA = os.path.join(C2_BUILD, "c21_infra")
L0 = os.path.join(C2_BUILD, "zed_orch", "c21", "l0")
NAMES_MANIFEST = os.path.join(L0, "NAMES_MANIFEST_V1.json")
NAMES_MANIFEST_SHA = os.path.join(L0, "NAMES_MANIFEST_V1.sha256")

if INFRA not in sys.path:
    sys.path.insert(0, INFRA)

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_FAM = os.path.dirname(os.path.dirname(_HERE))            # .../c21_fam
_BUILD = os.path.dirname(_FAM)                            # .../c2_build
for _p in (_FAM, os.path.join(_BUILD, "c21_infra")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

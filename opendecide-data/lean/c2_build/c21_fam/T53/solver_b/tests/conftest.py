import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_FAM = os.path.dirname(os.path.dirname(os.path.dirname(_HERE)))       # .../c21_fam
if _FAM not in sys.path:
    sys.path.insert(0, _FAM)

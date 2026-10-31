import os
import sys

sys.dont_write_bytecode = True
_HERE = os.path.dirname(os.path.abspath(__file__))
_T59 = os.path.dirname(os.path.dirname(_HERE))
for _p in (_T59, _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import os
import sys

sys.dont_write_bytecode = True
FAM = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if FAM not in sys.path:
    sys.path.insert(0, FAM)

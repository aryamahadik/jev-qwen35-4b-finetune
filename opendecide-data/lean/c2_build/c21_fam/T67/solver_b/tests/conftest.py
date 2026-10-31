import os
import sys

FAM = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if FAM not in sys.path:
    sys.path.insert(0, FAM)

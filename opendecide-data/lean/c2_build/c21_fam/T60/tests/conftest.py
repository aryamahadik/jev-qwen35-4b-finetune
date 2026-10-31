import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FAM = os.path.dirname(HERE)                         # .../c21_fam/T60
ROOT = os.path.dirname(FAM)                         # .../c21_fam
for p in (ROOT, FAM, os.path.join(ROOT, "T59")):
    if p not in sys.path:
        sys.path.insert(0, p)

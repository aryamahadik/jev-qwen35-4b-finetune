import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FAM = os.path.dirname(HERE)                         # .../c21_fam/T5x
ROOT = os.path.dirname(FAM)                         # .../c21_fam
for p in (ROOT, FAM):
    if p not in sys.path:
        sys.path.insert(0, p)

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SB = os.path.dirname(HERE)                          # .../T60/solver_b
FAM = os.path.dirname(SB)                           # .../c21_fam/T60
ROOT = os.path.dirname(FAM)                         # .../c21_fam
for p in (ROOT, FAM, SB, HERE):
    if p not in sys.path:
        sys.path.insert(0, p)

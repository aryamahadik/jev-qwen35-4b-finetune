import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # solver_b/
FAM = os.path.dirname(HERE)                                                 # T41c/
INFRA = os.path.join(os.path.dirname(os.path.dirname(FAM)), "c21_infra")
for p in (HERE, FAM, INFRA):
    if p not in sys.path:
        sys.path.insert(0, p)

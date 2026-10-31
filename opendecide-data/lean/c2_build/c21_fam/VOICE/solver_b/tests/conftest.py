import os
import sys

B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))     # VOICE/solver_b
VOICE = os.path.dirname(B)
GEN = os.path.join(os.path.dirname(VOICE), "GEN")
sys.dont_write_bytecode = True
if B not in sys.path:
    sys.path.insert(0, B)
for p in (VOICE, GEN):
    if p not in sys.path:
        sys.path.append(p)   # only the harness tests import solver A; B itself never does

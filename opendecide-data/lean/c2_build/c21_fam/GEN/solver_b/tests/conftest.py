import os
import sys

B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))     # GEN/solver_b
GEN = os.path.dirname(B)                                             # GEN
sys.dont_write_bytecode = True
if B not in sys.path:
    sys.path.insert(0, B)
if GEN not in sys.path:
    sys.path.append(GEN)   # only the harness tests import the lane generator (solver A); B itself never does

import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

# solver B (stdlib only, imports nothing from solver A) is imported by the real-pool tests next to the lane generator
_B = os.path.join(HERE, "solver_b")
if _B not in sys.path:
    sys.path.append(_B)
sys.dont_write_bytecode = True

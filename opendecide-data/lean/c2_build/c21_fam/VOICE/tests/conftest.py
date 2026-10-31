import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN = os.path.join(os.path.dirname(HERE), "GEN")
if HERE not in sys.path:
    sys.path.insert(0, HERE)
if GEN not in sys.path:
    sys.path.append(GEN)

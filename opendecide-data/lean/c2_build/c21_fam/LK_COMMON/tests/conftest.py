import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))      # .../c21_fam
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

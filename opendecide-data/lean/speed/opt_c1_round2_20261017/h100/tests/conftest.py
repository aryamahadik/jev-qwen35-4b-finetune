import os
import sys
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

LEAN = ROOT.parents[2]
for _p in (str(LEAN / "hosting"), str(LEAN), str(ROOT / "tests")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

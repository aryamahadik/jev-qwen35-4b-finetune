"""repair_a69_faithful.py: a thin import. The faithful A69 (d) repair, the guarded swap and the (f) admission tests moved to
c2_build/a69_faithful.py (A80 b: wired into c2_select and mix_c2). Importing this name returns that very module, so the A78
scratch scripts (scratch_run.py, scratch_summary.py) and tests/test_repair_a69_faithful_a78.py see the same objects."""
import sys
from pathlib import Path

C2B = Path(__file__).resolve().parents[2]            # c2_build
if str(C2B) not in sys.path:
    sys.path.insert(0, str(C2B))
import a69_faithful  # noqa: E402

sys.modules[__name__] = a69_faithful

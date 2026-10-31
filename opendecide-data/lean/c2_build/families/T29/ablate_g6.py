"""T29 iteration 2e ablation driver: G6 at N rows (run_pilot_i2's loader) with module constants of plugin.py overridden.
  python -B families/T29/ablate_g6.py ARM [--n 6000] [KEY=PYTHON_LITERAL ...]    (from lean/c2_build)
Writes pilot_i2/abl_<ARM>/G6_AT_<n>.json (the real pilot_i2/G6_AT_6000.json is untouched)."""
import ast
import sys
from pathlib import Path

sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(C2))
sys.path.insert(0, str(C2 / "families" / "T29"))
import contextlib  # noqa: E402

import pilot_loaders as PL  # noqa: E402
import run_pilot_i2 as R  # noqa: E402
from families.T29 import plugin as P  # noqa: E402

arm, n, kv = sys.argv[1], 6000, {}
for a in sys.argv[2:]:
    if a.startswith("--n="):
        n = int(a[4:])
    else:
        k, v = a.split("=", 1)
        kv[k] = ast.literal_eval(v)
for k, v in kv.items():
    if not hasattr(P, k):
        raise SystemExit(f"no plugin constant {k}")
    setattr(P, k, v)
R.OUT = f"pilot_i2/abl_{arm}"
Path(PL.family_dir("T29"), R.OUT).mkdir(parents=True, exist_ok=True)
orig = PL.open_family


@contextlib.contextmanager
def patched(fid):
    with orig(fid) as kit0:
        kit = R.with_dneg(kit0)
        yield kit


PL.open_family = patched
raise SystemExit(R.g6_at_size(n))

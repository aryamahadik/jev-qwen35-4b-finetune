"""Dev tool (A45 c): G6 (choice + yes/no) on a 6,000-row build with DEV seeds and the i4 loader. argv: seed_base n. Writes nothing."""
import sys, json
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2])); sys.path.insert(0, str(HERE.parent))
import pilot as PI, pilot_loaders as PL
import run_pilot_i4 as R
R.install_loader()
base, n = int(sys.argv[1]), int(sys.argv[2])
assert base != PI.SEED_BASE
with PL.open_family("T35") as kit:
    b = PI.build_pilot(kit, n, seed_base=base, run_g15=False)
    g6 = PI.g6(b.infos)
print(base, "rows", len(b.infos), "drops", b.stats["drops_by_gate"])
for part in ("yes_no", "choice"):
    print(part, g6[part].get("chance"), {k: v for k, v in g6[part].items() if isinstance(v, dict)})
print("fails", [(f["part"], f["view"], f["model"], f["acc"]) for f in g6["fails"]])

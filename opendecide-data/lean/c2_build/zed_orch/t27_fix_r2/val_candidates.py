"""Validation of the G11 balance on the EXISTING pools (no new wordings): the candidate build only (no QC build, no G6),
default seed bases (2M / 3M / 4M: not the fix-round bases), written under val_root_<tag>/T27 for analysis.
  val_candidates.py [--no-balance] [--tag TAG] [--n N]      (run from lean/c2_build; VM: see gcp commands in STATUS.json)"""
import argparse, json, sys, time
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2 = HERE.parents[1]
for p in (str(C2), str(HERE)):
    sys.path.insert(0, p)
import gen_full_c2 as G
import overlay as O
ap = argparse.ArgumentParser()
ap.add_argument("--no-balance", action="store_true")
ap.add_argument("--tag", default="a")
ap.add_argument("--n", type=int, default=None)
ap.add_argument("--no-wordings", action="store_true", help="ignore admitted_wordings.json (validation on the frozen pools)")
a = ap.parse_args()
root = HERE / f"val_root_{a.tag}"
root.mkdir(parents=True, exist_ok=True)
t0 = time.time()
with O.patched(balance=not a.no_balance, wordings=not a.no_wordings):
    rep = G.run("T27", n=a.n, root=root, no_qc=True, qc_big=0, log=lambda m: print(m, file=sys.stderr, flush=True))
print(json.dumps({"n_candidates": rep["n_candidates"], "program_pass": rep["program_pass"], "failing": rep["program_failing"],
                  "seconds": rep["seconds"], "notes": rep["loader_notes"], "gate_lines": rep["gate_lines"]}, indent=1, default=str))

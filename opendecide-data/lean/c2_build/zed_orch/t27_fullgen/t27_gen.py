"""T27 full generation (A42-D 6.4 step 7) through gen_full_c2.run() at NEW never-used seed bases, written under
zed_orch/t27_fullgen/gen_root/T27 (the VM has no lean/data tree; install_pull.py copies it into data/c2_parts/T27)."""
import json, sys
from pathlib import Path
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(C2))
import gen_full_c2 as G
import os
root = C2 / "zed_orch" / "t27_fullgen" / os.environ.get("T27_ROOT_NAME", "gen_root")
root.mkdir(parents=True, exist_ok=True)
bases = (66_000_000, 67_000_000, 68_000_000)      # candidates, QC (= B0 of the A50 G6), mixdev; >= 60M, % 32 == 0, 1M apart
rep = G.run("T27", root=root, seed_bases=bases, qc_big=0, log=lambda m: print(m, file=sys.stderr, flush=True))
print(json.dumps({"n_candidates": rep["n_candidates"], "qc_rows": (rep["qc_build"] or {}).get("rows_written"),
                  "program_pass": rep["program_pass"], "failing": rep["program_failing"], "seconds": rep["seconds"],
                  "written": rep["written"], "g13_seed": (rep["exclusions"].get("g13_seed") or {}).get("clean"),
                  "gate_lines": rep["gate_lines"]}, indent=1, default=str))

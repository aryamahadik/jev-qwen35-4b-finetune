"""T32 w9 fix round: full generation through gen_full_c2.run() at NEW seed bases, written under zed_orch/w9_t32/gen_root/T32
(the VM has no lean/data tree; files are installed into data/c2_parts/T32 after the pull). qc_big=0: the 24K diagnostic is not
rebuilt (A50 b: diagnostic only)."""
import json, sys
from pathlib import Path
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(C2))
import gen_full_c2 as G
root = C2 / "zed_orch" / "w9_t32" / "gen_root10"
root.mkdir(parents=True, exist_ok=True)
bases = (272_629_760, 273_678_336, 274_726_912)
rep = G.run("T32", root=root, seed_bases=bases, qc_big=0, log=lambda m: print(m, file=sys.stderr, flush=True))
print(json.dumps({"n_candidates": rep["n_candidates"], "qc_rows": (rep["qc_build"] or {}).get("rows_written"),
                  "program_pass": rep["program_pass"], "failing": rep["program_failing"], "seconds": rep["seconds"],
                  "written": rep["written"], "gate_lines": rep["gate_lines"]}, indent=1, default=str))

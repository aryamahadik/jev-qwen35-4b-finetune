"""T24 w9 fix round: full generation through gen_full_c2.run() at NEW seed bases, written under zed_orch/w9/gen_root/T24
(the VM has no lean/data tree; the files are installed into data/c2_parts/T24 after the pull). In memory + guarded writers."""
import json, sys
from pathlib import Path
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(C2))
import gen_full_c2 as G
root = C2 / "zed_orch" / "w9" / "gen_root"
root.mkdir(parents=True, exist_ok=True)
bases = (127_000_000, 128_000_000, 129_000_000)
rep = G.run("T24", root=root, seed_bases=bases, qc_big=0, log=lambda m: print(m, file=sys.stderr, flush=True))
print(json.dumps({"n_candidates": rep["n_candidates"], "qc_rows": (rep["qc_build"] or {}).get("rows_written"),
                  "program_pass": rep["program_pass"], "failing": rep["program_failing"], "seconds": rep["seconds"],
                  "written": rep["written"], "gate_lines": rep["gate_lines"]}, indent=1, default=str))

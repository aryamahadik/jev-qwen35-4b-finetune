"""T15 w9 fix round (A49 d): full generation through gen_full_c2.run() at NEW never-used seed bases, written under
zed_orch/w9_t15/gen_root/T15 (the VM has no lean/data tree; files are installed into data/c2_parts/T15 after the pull)."""
import json, sys
from pathlib import Path
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(C2))
import gen_full_c2 as G
root = C2 / "zed_orch" / "w9_t15" / "gen_root"
root.mkdir(parents=True, exist_ok=True)
bases = (250_000_000, 251_000_000, 252_000_000)
rep = G.run("T15", root=root, seed_bases=bases, qc_big=0, log=lambda m: print(m, file=sys.stderr, flush=True))
print(json.dumps({"n_candidates": rep["n_candidates"], "qc_rows": (rep["qc_build"] or {}).get("rows_written"),
                  "program_pass": rep["program_pass"], "failing": rep["program_failing"], "seconds": rep["seconds"],
                  "written": rep["written"], "gate_lines": rep["gate_lines"]}, indent=1, default=str))

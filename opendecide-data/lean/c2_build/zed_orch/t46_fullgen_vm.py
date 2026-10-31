"""T46 full generation into a unique output root under c2_build (so gcp_run.sh pulls it): driver around gen_full_c2.run (root=...)."""
import sys, json
from pathlib import Path
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2))
import gen_full_c2 as G  # noqa: E402
root = C2 / sys.argv[1]
rep = G.run("T46", dry=False, qc_n=6000, root=root, log=lambda m: print(m, file=sys.stderr, flush=True))
print(json.dumps({"n_candidates": rep["n_candidates"], "qc_rows": (rep["qc_build"] or {}).get("rows_written"), "program_pass": rep["program_pass"],
                  "failing": rep["program_failing"], "written": rep["written"], "seconds": rep["seconds"], "gate_lines": rep["gate_lines"]},
                 indent=1, default=str))

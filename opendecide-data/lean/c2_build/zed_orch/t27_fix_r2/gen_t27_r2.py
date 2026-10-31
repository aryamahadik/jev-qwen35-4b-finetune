"""T27 G11 fix round 2: the full generation through gen_full_c2.run() with the fixed generator (overlay.py: least-loaded wording
pick + the new ch_next and yn_beyond training wordings of admitted_wordings.json), written under zed_orch/t27_fix_r2/gen_root/T27
(out/ and qc/; the VM has no lean/data tree; install.py copies it to data/c2_parts/T27).

Seed bases (fixed before any generation of this round; PREREG A49/A50): candidates 72,000,000 and QC 73,000,000 (= B0 of the A50
G6; both never used by T27), mixdev 68,000,000 UNCHANGED (S5 uses held-out wordings only: the fix does not touch it, so
mixdev_S5.jsonl stays byte-identical; checked by install.py); A50 builds 11,000,000 / 12,000,000 / 13,000,000.
  VM:  HF_HUB_OFFLINE=1 PYTHONPATH=$HOME/lean ~/od/bin/python -B zed_orch/t27_fix_r2/gen_t27_r2.py     (from c2_build)
"""
import json, os, sys
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2 = HERE.parents[1]
for p in (str(C2), str(HERE)):
    sys.path.insert(0, p)
import gen_full_c2 as G
import overlay as O
BASES = (72_000_000, 73_000_000, 68_000_000)
if os.environ.get("T27_R2_BASES"):                    # the interim (frozen-pools) run only: never the final run
    if os.environ.get("T27_R2_NO_NEW_WORDINGS") != "1":
        sys.exit("T27_R2_BASES is only for the interim run (T27_R2_NO_NEW_WORDINGS=1)")
    BASES = tuple(int(x) for x in os.environ["T27_R2_BASES"].split(","))
if not O.ADMITTED.is_file() and os.environ.get("T27_R2_NO_NEW_WORDINGS") != "1":
    sys.exit("admitted_wordings.json is missing: the new ch_next and yn_beyond wordings are not admitted yet (redo5.py glex-check --record). "
             "Set T27_R2_NO_NEW_WORDINGS=1 only for an exploratory run on the frozen pools.")
root = HERE / os.environ.get("T27_R2_ROOT_NAME", "gen_root")
root.mkdir(parents=True, exist_ok=True)
with O.patched():
    rep = G.run("T27", root=root, seed_bases=BASES, qc_big=0, log=lambda m: print(m, file=sys.stderr, flush=True))
print(json.dumps({"n_candidates": rep["n_candidates"], "qc_rows": (rep["qc_build"] or {}).get("rows_written"),
                  "program_pass": rep["program_pass"], "failing": rep["program_failing"], "seconds": rep["seconds"],
                  "written": rep["written"], "g13_seed": (rep["exclusions"].get("g13_seed") or {}).get("clean"),
                  "notes": rep["loader_notes"], "gate_lines": rep["gate_lines"]}, indent=1, default=str))

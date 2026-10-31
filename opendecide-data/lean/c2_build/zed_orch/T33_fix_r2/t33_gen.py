"""T33 fix round 2 (PREREG A52 d, one round): full generation through gen_full_c2.run() with the fixed generator (G0 amendment w9,
plugin.py: equal number of unfinished steps for every gold in a choice log; ch_claim_verdict always 3 claims, one of each verdict)
at NEW seed bases, written under zed_orch/T33_fix_r2/gen_root/T33 (never under data/c2_parts: the VM has no lean/data tree, and
the Mac copy is installed later by install.py). qc_big=0: the 24K diagnostic is not rebuilt (A50 b).

Seed bases, fixed BEFORE any run of this generator (A49 e / A50): candidates 300,000,000 / QC 301,000,000 / mixdev 302,000,000
(each divisible by 32, 1,000,000 apart, disjoint from the pilot range and from every base T33 used before: 2M/3M/4M, 30M/31M/32M,
A50 builds 11M/12M/13M, wave-9 diagnostic dumps 96M/97M). A50 G6 then uses B0 = this QC build (301M) + 11M / 12M / 13M.
Run on the VM:  HF_HUB_OFFLINE=1 PYTHONPATH=$HOME/lean ~/od/bin/python -B zed_orch/T33_fix_r2/t33_gen.py"""
import json, sys
from pathlib import Path
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(C2))
import gen_full_c2 as G

BASES = (300_000_000, 301_000_000, 302_000_000)
USED_BEFORE = {2_000_000, 3_000_000, 4_000_000, 30_000_000, 31_000_000, 32_000_000, 11_000_000, 12_000_000, 13_000_000,
               96_000_000, 97_000_000}
assert not (set(BASES) & USED_BEFORE), "seed base reuse"
root = C2 / "zed_orch" / "T33_fix_r2" / "gen_root"
if (root / "T33" / "qc" / "GEN_REPORT.json").exists():
    raise SystemExit("gen_root already holds a T33 generation: never re-draw (A52 d: one round); use a new root only with a ruling")
root.mkdir(parents=True, exist_ok=True)
rep = G.run("T33", root=root, seed_bases=BASES, qc_big=0, log=lambda m: print(m, file=sys.stderr, flush=True))
print(json.dumps({"n_candidates": rep["n_candidates"], "qc_rows": (rep["qc_build"] or {}).get("rows_written"),
                  "program_pass": rep["program_pass"], "failing": rep["program_failing"],
                  "program_pass_a49": rep["program_pass_a49"], "failing_a49": rep["program_failing_a49"],
                  "seconds": rep["seconds"], "written": rep["written"], "gate_lines": rep["gate_lines"]}, indent=1, default=str))

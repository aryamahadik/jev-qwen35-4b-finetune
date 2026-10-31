"""A50 G6 for the T27 fix round: the three more 6,000-row builds (seed bases 11M / 12M / 13M) through the SAME patched generator
(overlay.patched()), then the aggregate against the staged gen_root (B0 = its QC build).
  g6_a50_r2.py build --seed-base 11000000        (VM; writes zed_orch/t27_fix_r2/out_a50/T27_b11000000.json)
  g6_a50_r2.py agg                                (Mac or VM; writes gen_root/T27/qc/G6_A50.json and updates its GEN_REPORT)"""
import argparse, json, os, sys
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
C2 = HERE.parents[1]
for p in (str(C2), str(C2 / "zed_orch"), str(HERE)):
    sys.path.insert(0, p)
import g6_a50_full as A50
import overlay as O
OUT = HERE / os.environ.get("T27_R2_OUT_A50", "out_a50")
ap = argparse.ArgumentParser()
sub = ap.add_subparsers(dest="cmd", required=True)
b = sub.add_parser("build"); b.add_argument("--seed-base", type=int, required=True); b.add_argument("--n", type=int, default=6000)
g = sub.add_parser("agg"); g.add_argument("--root", default=str(HERE / os.environ.get("T27_R2_ROOT_NAME", "gen_root")))
a = ap.parse_args()
if a.cmd == "build":
    if a.seed_base not in A50.NEW_BASES:
        sys.exit(f"A50 fixes the bases {A50.NEW_BASES}; no other base is used")
    OUT.mkdir(exist_ok=True)
    if not O.ADMITTED.is_file() and os.environ.get("T27_R2_NO_NEW_WORDINGS") != "1":
        sys.exit("admitted_wordings.json is missing (see gen_t27_r2.py)")
    with O.patched():
        A50.build(argparse.Namespace(family="T27", seed_base=a.seed_base, n=a.n, no_redraw=False,
                                     out=str(OUT / f"T27_b{a.seed_base}.json")))
else:
    A50.OUTDIR = OUT
    r = A50.aggregate("T27", root=Path(a.root))
    w = r["worst_cell"]
    print(json.dumps({"verdict": r["verdict"], "worst": w, "failing": r["failing_cells"], "bases": r["seed_bases"],
                      "single": r["single_build_max_excess_pp"], "program_pass_a50": r.get("program_pass_a50"),
                      "program_failing_a50": r.get("program_failing_a50")}, indent=1))

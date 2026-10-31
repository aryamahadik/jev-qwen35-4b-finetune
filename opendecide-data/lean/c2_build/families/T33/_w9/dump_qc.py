"""w9 diagnostic: build N QC rows of T33 through the gen_full_c2 path and dump (row, question, context, option kinds).
usage: python -B families/T33/_w9/dump_qc.py --seed-base 31000000 --n 6000 --out families/T33/_w9/dump_31M.jsonl"""
import argparse, json, sys, time
from pathlib import Path
C2 = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(C2)); sys.dont_write_bytecode = True
import gen_full_c2 as G, pilot, pilot_loaders as PL
ap = argparse.ArgumentParser(); ap.add_argument("--seed-base", type=int); ap.add_argument("--n", type=int, default=6000)
ap.add_argument("--out"); a = ap.parse_args()
fam = "T33"
src = G.quarantine_sources(fam); banned = set().union(*map(set, src.values()))
with G.loader_patch(fam):
    with PL.open_family(fam) as kit0:
        kit, xrep = G.apply_exclusions(kit0, banned)
        rd = G.Redraw(kit.plugin, xrep["dead_qforms"]) if xrep["dead_qforms"] else None
        try:
            b = pilot.build_pilot(kit, a.n, seed_base=a.seed_base, run_g15=False)
        finally:
            if rd: rd.restore()
with open(a.out, "w") as f:
    for i in b.infos:
        f.write(json.dumps({"row": i.row, "question": i.question, "context": i.context,
                            "kinds": pilot.option_kinds(i) if i.row["qtype"] == "choice" else None}, default=str) + "\n")
print("rows", len(b.infos), "dead", xrep["dead_qforms"])

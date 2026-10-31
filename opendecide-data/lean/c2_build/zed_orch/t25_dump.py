"""W9 T25 diagnostic: build one QC-style build through gen_full_c2's path and dump per-row facts (small)."""
import argparse, json, sys, time
from pathlib import Path
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2))
import gen_full_c2 as G
ap = argparse.ArgumentParser(); ap.add_argument("--seed-base", type=int); ap.add_argument("--n", type=int, default=6000); ap.add_argument("--out")
a = ap.parse_args()
fam = "T25"
src = G.quarantine_sources(fam); banned = set().union(*map(set, src.values()))
with G.loader_patch(fam):
    with G.PL.open_family(fam) as kit0:
        kit, xrep = G.apply_exclusions(kit0, banned)
        rd = G.Redraw(kit.plugin, xrep["dead_qforms"]) if xrep["dead_qforms"] else None
        try:
            b = G.pilot.build_pilot(kit, a.n, seed_base=a.seed_base, run_g15=False)
        finally:
            if rd: rd.restore()
        with open(a.out, "w") as f:
            for i in b.infos:
                r = i.row; s = i.spec
                f.write(json.dumps({"id": r["id"], "qtype": r["qtype"], "options": r["options"], "gold": r["gold"], "role": r.get("role"),
                    "qform": s.qform if s else None, "sampler": r["meta"]["sampler"], "seed": r["meta"]["seed"], "card": r["meta"]["card_id"],
                    "wording": r["meta"].get("wording_id"), "pack": s.structure.get("pack") if s else None,
                    "unit": i.unit, "state": r["state"][-1400:] if r["qtype"]=="choice" else None, "instr": r["instructions"][-300:]}) + "\n")
        g7 = G.pilot.g7(b.infos)
        print(json.dumps({k: g7[k] for k in ("n_tests","n_choice_fails","choice_fails","top5_choice","n_yes_no_raw_fails")}, default=str)[:3000])

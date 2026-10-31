import sys, copy, json, pickle, collections
from pathlib import Path
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(C2))
import pilot, pilot_loaders as PL
from families.T26 import loader as LD
base, nrows = int(sys.argv[1]), int(sys.argv[2])
with LD.open_t26() as kit:
    fk = PL.FamilyKit("T26", PL.family_dir("T26"), kit.plugin, kit.ctx, "loader", "pools_v2/", [])
    b = pilot.build_pilot(fk, nrows, seed_base=base, run_g15=False)
    infos = b.infos
    yn = [i for i in infos if i.row["qtype"] == "noul"]
    print("yn rows", len(yn), "deep yn", sum(bool(i.row["meta"]["deep"]) for i in yn), flush=True)
    print("with deep:", {k: pilot.g6_yes_no(yn)["d_meta"] for k in ("x",)}, flush=True)
    r0 = pilot.g6_yes_no(yn); print("drivers with deep", r0.get("d_meta_drivers"), flush=True)
    for i in infos: i.row["meta"]["deep"] = False
    r = pilot.g6_yes_no(yn); print("deep off :", r["d_meta"], r.get("d_meta_drivers"), flush=True)

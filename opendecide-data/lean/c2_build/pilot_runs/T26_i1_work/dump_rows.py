import json, sys
from pathlib import Path
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(C2))
import pilot, pilot_loaders as PL  # noqa: E402
from families.T26 import loader as LD, plugin as P  # noqa: E402
base, nrows, outp = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
with LD.open_t26() as kit:
    fk = PL.FamilyKit("T26", PL.family_dir("T26"), kit.plugin, kit.ctx, "loader", "pools_v2/", [])
    b = pilot.build_pilot(fk, nrows, seed_base=base, run_g15=False)
    with open(outp, "w") as f:
        for i in b.infos:
            sp = i.spec
            f.write(json.dumps({"row": i.row, "question": i.question, "context": i.context,
                                "verdict": P._decide(kit.plugin._statuses(sp)) if sp is not None else None,
                                "statuses": kit.plugin._statuses(sp) if sp is not None else None,
                                "abstain_key": (i.rr.option_set.meta.get("abstain_key") if i.rr is not None and i.rr.option_set else None),
                                "gold_key": (i.rr.option_set.gold.key if i.rr is not None and i.rr.option_set else None),
                                "shown": sp.structure["shown"] if sp else None, "checks": sp.structure["checks"] if sp else None,
                                "unavailable": sp.structure["unavailable"] if sp else None}) + "\n")

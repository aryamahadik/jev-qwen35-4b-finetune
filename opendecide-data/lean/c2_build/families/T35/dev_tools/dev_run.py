"""A pilot-sized T35 build on DEV seeds (argv: seed_base, n_rows); the gates are printed, nothing is written."""
import sys
from pathlib import Path
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(C2))
import pilot as PI  # noqa: E402
import pilot_loaders as PL  # noqa: E402

base, n = int(sys.argv[1]), int(sys.argv[2])
assert base != PI.SEED_BASE, "dev seeds only"
with PL.open_family("T35") as kit:
    b = PI.build_pilot(kit, n, seed_base=base, run_g15=False)
    g6, g7, g10 = PI.g6(b.infos), PI.g7(b.infos), PI.g10(b.infos, b.units, kit.plugin)
    ov, s30 = PI.overlay(b.units, kit.plugin), PI.spec30(b.infos, kit.plugin)
    print("rows", b.stats["rows_written"], "drops", b.stats["drops_by_gate"])
    print("G6 yes/no", {k: v for k, v in g6["yes_no"].items() if isinstance(v, dict) and "lr" in v})
    print("G6 choice", {k: v for k, v in g6["choice"].items() if isinstance(v, dict)}, "chance", g6["choice"].get("chance"))
    print("G7", g7["verdict"], g7["n_yes_no_raw_fails"], g7["n_choice_fails"])
    for k, c in {**{"G10 " + k: c for k, c in g10["checks"].items()}, **{"OV " + k: c for k, c in ov["checks"].items()},
                 **{"S30 " + k: c for k, c in s30["checks"].items()}}.items():
        print(k, c["verdict"], str(c["value"])[:120])

"""T26 fix iteration 1: the program gates on a 5,000-row build (G6's own spec size) at seeds outside the pilot's.
In memory; prints the gate lines and the numbers G0 section 2 quotes. Usage: big_gates.py <seed_base> <rows>"""
import json, sys, collections
from pathlib import Path
sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(C2))
import pilot  # noqa: E402
import pilot_loaders as PL  # noqa: E402
from c2_kit import pipeline, choiceplan  # noqa: E402
from families.T26 import loader as LD  # noqa: E402
import negcount  # noqa: E402

base, nrows = int(sys.argv[1]), int(sys.argv[2])
with LD.open_t26() as kit:
    fk = PL.FamilyKit("T26", PL.family_dir("T26"), kit.plugin, kit.ctx, "loader", "pools_v2/", [])
    b = pilot.build_pilot(fk, nrows, seed_base=base, run_g15=False, log=lambda m: print(m, file=sys.stderr, flush=True))
    pg = pilot.program_gates(b)
    infos, units, plugin = b.infos, b.units, kit.plugin
    out = {"rows": len(infos), "units": len(units), "drops": b.stats["drops_by_gate"]}
    g6 = pilot.g6(infos); g7 = pilot.g7(infos); g10 = pilot.g10(infos, units, plugin)
    ov = pilot.overlay(units, plugin); sp = pilot.spec30(infos, plugin)
    for name, g in (("G6", g6), ("G7", g7), ("G10", g10), ("overlay", ov), ("spec_3_0", sp)):
        print(name, g.get("verdict"), flush=True)
    print(pilot.gate_lines({"G6": g6, "G7": g7, "G10": g10, "overlay": ov, "spec_3_0": sp}))
    print("G6 yes_no", {k: g6["yes_no"][k] for k in ("n", "chance", "a_question", "c_card_without_question", "d_meta")})
    print("G6 choice", {k: g6["choice"][k] for k in ("n", "chance", "a_question", "b_options", "c_card_without_question", "d_meta")})
    print("G6 fails", [(f["part"], f["view"], f["model"], f["acc"], f["chance"]) for f in g6["fails"]])
    print("G7 top", g7["top5_choice"][:3], g7["top5_yes_no_raw"][:2])
    rows = [i.row for i in infos]
    yn = [i for i in infos if i.row["qtype"] == "noul"]
    print("negation", round(sum(negcount.count(i.question).k_syn >= 1 for i in yn) / len(yn), 4),
          round(sum(negcount.count(i.question).k_syn >= 2 for i in yn) / len(yn), 4))
    print("overlay", json.dumps(ov["report"], default=str)[:1500])
    print("spec30", {k: v["value"] for k, v in sp["checks"].items()})
    sets = [rr.option_set for u in units for rr in u.rendered if rr.option_set is not None]
    rep = choiceplan.plan_report(sets)
    print("plan_report", {k: rep[k] for k in ("rows", "longest_gold_pp", "positions_chi2_p", "failing")})

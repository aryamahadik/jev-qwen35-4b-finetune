"""T01 scratch: G6 + G7 + G10 at ~5,000 rows (the full-generation G6 sample size) on the current generator. Report only."""
import sys, json, time
sys.path.insert(0, '.')
import pilot, pilot_loaders as PL
n = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
tag = sys.argv[2] if len(sys.argv) > 2 else "x"
seed_base = int(sys.argv[3]) if len(sys.argv) > 3 else pilot.SEED_BASE
t = time.time()
with PL.open_family("T01") as kit:
    b = pilot.build_pilot(kit, n, seed_base=seed_base, run_g15=False, log=lambda m: None)
    infos = b.infos
    print("built", len(infos), "rows", round(time.time() - t), "s", b.stats["units_attempted"], "units attempted", flush=True)
    g6 = pilot.g6(infos)
    ch, yn = g6["choice"], g6["yes_no"]
    print("G6 yes_no n", yn["n"], {v: yn[v] for v in ("a_question", "c_card_without_question", "d_meta")}, flush=True)
    print("G6 choice n", ch["n"], "chance", ch["chance"], {v: ch[v] for v in ("a_question", "b_options", "c_card_without_question", "d_meta")}, flush=True)
    print("G6 verdict", g6["verdict"], [(f["part"], f["view"], f["model"], f["acc"]) for f in g6["fails"]], flush=True)
    g7 = pilot.g7(infos)
    print("G7", g7["verdict"], "tests", g7["n_tests"], "choice fails", g7["n_choice_fails"], "yn raw", g7["n_yes_no_raw_fails"], "yn card", g7["n_yes_no_card_adjusted_fails"], flush=True)
    for f in g7["choice_fails"][:15]:
        print("   ", f["feature"], f["n_rows"], f["gold_hits"], f["expected"], "%.2e" % f["p"], flush=True)
    for f in g7["yes_no_raw_fails"][:5] + g7["yes_no_card_adjusted_fails"][:5]:
        print("   yn", f["feature"], f["n"], f["yes_rate"], "%.2e %.2e" % (f["p_raw"], f["p_card"]), flush=True)
    print("top5 choice", [(f["feature"], f["n_rows"], f["gold_hits"], f["expected"], "%.1e" % f["p"]) for f in g7["top5_choice"]], flush=True)
    g10 = pilot.g10(infos, b.units, kit.plugin)
    print("G10", g10["verdict"], g10["failing"], flush=True)
    print("longest", g10["checks"]["longest_option_gold_pp"], flush=True)
    print("rank", g10["checks"]["gold_rank"], flush=True)
    print("pos", g10["checks"]["gold_position"], flush=True)
print("done", round(time.time() - t), "s")

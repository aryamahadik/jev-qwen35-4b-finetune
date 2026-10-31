"""families/T30/diag_i1.py: in-memory diagnostics for the T30 fix iteration (program gates only; writes nothing).

Builds N pilot-shaped rows from a seed base through the family loader (pilot_loaders._t30 + pilot.build_pilot, the
same code the pilot runs), then prints the measurable gates: the option plan report, G10, spec 3.0 tokens, G6, G7 and
the overlay shares. No Haiku, no model, no file. Use a seed base other than the pilot's 900000 to look at fresh rows.

  cd lean/c2_build && ../../.venv/bin/python -B families/T30/diag_i1.py --n 1500 --seed-base 1000000 --gates opt,g10,tok
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
C2 = Path(__file__).resolve().parents[2]
if str(C2) not in sys.path:
    sys.path.insert(0, str(C2))

import pilot as PI  # noqa: E402
import pilot_loaders as PL  # noqa: E402
from c2_kit import cards  # noqa: E402
from c2_kit.choiceplan import plan_report  # noqa: E402


def short(d, keep=("verdict", "value", "failing")):
    return {k: d[k] for k in keep if k in d}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=1000)
    ap.add_argument("--seed-base", type=int, default=PI.SEED_BASE)
    ap.add_argument("--gates", default="opt,g10,tok,overlay")
    ap.add_argument("--g15", action="store_true")
    a = ap.parse_args(argv)
    want = set(a.gates.split(","))
    with PL.open_family("T30") as kit:
        b = PI.build_pilot(kit, a.n, seed_base=a.seed_base, run_g15=a.g15, log=lambda m: print(m, file=sys.stderr))
        print(json.dumps({"built": b.stats["rows_written"], "units": b.stats["units_written"],
                          "attempted": b.stats["units_attempted"], "drops": b.stats["drops_by_gate"],
                          "examples": b.stats["drop_examples"]}, indent=1))
        infos, plugin = b.infos, kit.plugin
        rows = [i.row for i in infos]
        if "opt" in want:
            sets = [rr.option_set for u in b.units for rr in u.rendered if rr.option_set is not None]
            for form in ("ch_next", "ch_target"):
                ss = [rr.option_set for u in b.units for rr in u.rendered
                      if rr.option_set is not None and rr.row["meta"]["qform"] == form]
                if ss:
                    rep = plan_report(ss)
                    print(form, json.dumps({k: rep[k] for k in ("rows", "abstain_cells", "positions", "longest_gold_pp",
                                                                  "failing", "pass")}, default=str))
            roles = Counter()
            for u in b.units:
                for rr in u.rendered:
                    if rr.option_set is not None:
                        roles[(rr.row["meta"]["qform"], rr.row["role"], rr.option_set.meta.get("gold_is_abstain"))] += 1
            print("roles", dict(sorted(roles.items(), key=str)))
            gold = Counter(r["gold"] for r in rows if r["meta"]["qform"] == "ch_next")
            print("ch_next gold", dict(gold))
        if "g10" in want:
            g = PI.g10(infos, b.units, plugin)
            print("G10", g["verdict"], g["failing"])
            for k, v in g["checks"].items():
                print("  ", k, v["verdict"], json.dumps(v["value"], default=str)[:400])
        if "overlay" in want:
            g = PI.overlay(b.units, plugin)
            print("overlay", g["verdict"], {k: (v["value"], v["verdict"]) for k, v in g["checks"].items()})
        if "tok" in want:
            g = PI.spec30(infos, plugin)
            print("spec30", g["verdict"], {k: g["checks"][k]["value"] for k in ("max_tokens", "mean_tokens")})
            print(json.dumps(cards.token_report(rows)))
        if "g6" in want:
            g = PI.g6(infos)
            print("G6", g["verdict"])
            for part in ("yes_no", "choice"):
                p = g[part]
                print("  ", part, {k: p[k] for k in p if k in ("n", "chance", "a_question", "b_options",
                                                                "c_card_without_question", "d_meta")})
            print("  fails", [(f["part"], f["view"], f["model"], f["acc"], f["chance"]) for f in g["fails"]])
        if "g7" in want:
            g = PI.g7(infos)
            print("G7", g["verdict"], {k: g[k] for k in ("n_tests", "n_yes_no_raw_fails", "n_yes_no_card_adjusted_fails",
                                                         "n_choice_fails")})
            for f in g["choice_fails"][:10]:
                print("   choice", f["feature"], f["gold_hits"], f["expected"], f["p"])
            for f in g["yes_no_raw_fails"][:5] + g["yes_no_card_adjusted_fails"][:5]:
                print("   yn", f["feature"], f["n"], f["yes"], f["p_raw"], f["p_card"])
            print("   top5 choice", [(f["feature"], f["gold_hits"], f["expected"], f["p"]) for f in g["top5_choice"]])
            print("   top5 yn", [(f["feature"], f["n"], f["yes_rate"], f["p_raw"], f["p_card"]) for f in
                                 g["top5_yes_no_raw"]])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

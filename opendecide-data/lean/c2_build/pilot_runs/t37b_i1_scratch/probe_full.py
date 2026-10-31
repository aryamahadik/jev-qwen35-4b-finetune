"""The pilot at the full-block parameters (n=2000: 1,400 : 600), in memory, recorded as pilot_i1/FULL_SIZE_PROBE.json."""
import sys, os, json, time
sys.path.insert(0, '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
import pilot as PI, pilot_t37b as P
from c2_kit import paths
write = len(sys.argv) > 1 and sys.argv[1] == "write"
rep = P.run(n_rows=2000, write=False, out_name="pilot_i1", log=lambda *_: None)
g = rep["gates"]
out = {"what": "the T37b pilot run at the full-block target (n_rows 2000 = 1,400 complements : 600 equiv), in memory; "
               "nothing of it is written except this record. Same code, seed and inputs as pilot_i1. Not the pilot "
               "the Haiku task files belong to.",
       "command": "T37B_PILOT_DIR=pilot_i1_full PYTHONHASHSEED=1 python pilot.py run t37b --n 2000   (deterministic)",
       "rows": rep["files"]["n_rows"], "rows_sha256": rep["files"]["rows_sha256"], "yes_rate": rep["files"]["yes_rate"],
       "kinds": rep["files"]["kinds"], "plan_basis": rep["build"]["plan_report"].get("basis"),
       "plan_rows": rep["build"]["plan_report"]["rows"],
       "pilot_size": {"rows": rep["files"]["n_rows"], "spec_bar": ">= 1000 partner rows (spec 6.4 step 5)",
                      "verdict": "pass" if rep["files"]["n_rows"] >= 1000 else "fail",
                      "note": "the driver prints its bar as n_rows (2000) here; the spec bar is 1,000"},
       "G6": {"yes_no": {k: g["G6"]["yes_no"][k] for k in ("n", "yes_rate", "chance", "a_question", "c_card_without_question",
                                                            "d_meta")}, "verdict": g["G6"]["verdict"]},
       "G7": {"n_tests": g["G7"]["n_tests"], "raw_fails": g["G7"]["n_yes_no_raw_fails"],
              "card_adjusted_fails": g["G7"]["n_yes_no_card_adjusted_fails"], "verdict": g["G7"]["verdict"]},
       "G10": {"failing": g["G10"]["failing"], "yes_rate": g["G10"]["checks"]["yes_rate"]["value"],
               "double_negation_share": g["G10"]["checks"]["double_negation_share"]["value"],
               "syntactic_negation_share": g["G10"]["checks"]["syntactic_negation_share"]["value"],
               "yes_rate_cells": g["G10"]["checks"]["yes_rate_cells"]["value"], "verdict": g["G10"]["verdict"]},
       "spec_3_0": {k: g["spec_3_0"]["checks"][k]["value"] for k in ("max_tokens", "mean_tokens")}
                   | {"length_dropped_units": g["spec_3_0"]["length_dropped_units"]["n"],
                      "verdict": g["spec_3_0"]["verdict"]},
       "S14_floors_caps": {k: g["S14_floors_caps"]["report"][k] for k in ("implicit_share", "non_syntactic_share",
                           "max_source_share", "max_template_share", "pass")},
       "G2_G_TW_G15": [g["G2"]["verdict"], g["G-TW"]["verdict"], g["G15"]["verdict"]]}
print(os.environ.get("PYTHONHASHSEED"), out["rows"], out["rows_sha256"][:16], out["G6"]["verdict"], flush=True)
if write:
    paths.write_json(P.PL.family_dir("t37b") / "pilot_i1" / "FULL_SIZE_PROBE.json", out)
    print("written")

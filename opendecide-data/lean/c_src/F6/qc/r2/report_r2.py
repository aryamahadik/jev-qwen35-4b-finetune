"""Write qc/QC_REPORT.json for the F6 round-1 repair (r1): gate results re-run on the regenerated outputs, the findings
of the first check (F6-QC-1 to F6-QC-12) with their status, and the residual problems. Counts only, never row text.
The previous report is kept as qc/QC_REPORT.before_repair_r1.json."""
import json
import sys
import time
from pathlib import Path

F6 = Path("/Users/aryamahadik/Documents/jev/opendecide-data/lean/c_src/F6")
QC = F6 / "qc"


def load(p):
    try:
        return json.load(open(p))
    except Exception:  # noqa: BLE001
        return None


def main():
    extra = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else {}
    g5 = load(QC / "r2" / "g5r2.json")
    g6 = load(QC / "g6_qc_sample.json")
    g7 = load(QC / "g7_candidates_r1.json")
    g8 = load(QC / "g8_candidates_r1.json")
    g8n = load(QC / "g8_null_candidates_r1.json")
    g10 = load(QC / "g10_candidates_r1.json")
    g11 = load(QC / "g11_candidates_r1.json")
    g12 = load(QC / "g12.json")
    g15 = load(QC / "g15_g18_candidates_r1.json")
    sb = load(F6 / "solverB" / "mismatch.json")
    gates = {}
    if g5:
        gates["G5"] = {k: g5.get(k) for k in ("pass", "sample_n", "seed", "agree_with_gold", "clearly_wrong_n",
                                             "ambiguous_n", "reader", "file")}
    if g6:
        gates["G6"] = {"pass": g6.get("pass"), "file": "qc/g6_qc_sample.json", "yes_no": g6.get("yes_no"),
                       "choice": g6.get("choice")}
    if g7:
        gates["G7"] = {k: g7.get(k) for k in ("pass", "n_tests", "bonferroni_p", "n_yes_no_card_adjusted_fails",
                                             "n_yes_no_raw_fails", "yes_no_raw_fails_multi_card", "n_choice_fails")}
        gates["G7"]["file"] = "qc/g7_candidates_r1.json"
        gates["G7"]["choice_fails"] = [x["feature"] for x in g7.get("choice_fails", [])][:10]
        gates["G7"]["yes_no_card_adjusted_fails"] = [x["feature"] for x in g7.get("yes_no_card_adjusted_fails", [])]
        gates["G7"]["yes_no_raw_multi_card_fails"] = [x["feature"] for x in g7.get("yes_no_raw_fails", [])
                                                     if x.get("n_cards", 1) > 1][:15]
    if g8:
        gates["G8"] = {"pass": g8.get("pass"), "file": "qc/g8_candidates_r1.json",
                       "grouped_by_card": g8.get("grouped_by_card"), "instance_level": g8.get("instance_level"),
                       "null_control": ({"real": g8n.get("real"), "null_range": g8n.get("null_range")} if g8n else None)}
    if g10:
        gates["G10"] = {"pass": not g10.get("pool_fail") and not g10.get("target_fail"),
                        "file": "qc/g10_candidates_r1.json", "pool_fail": g10.get("pool_fail"),
                        "target_fail": g10.get("target_fail"),
                        "failing_checks": [c for c in g10.get("checks", []) if not c.get("pass") and
                                           c.get("kind") != "info"]}
    if g11:
        gates["G11"] = {"pass": g11.get("pass"), "file": "qc/g11_candidates_r1.json", "fail_parts": g11.get("fail_parts"),
                        "counts": g11.get("counts"), "surface_template": g11.get("surface_template")}
    if g12:
        gates["G12"] = {"pass": g12.get("pass"), "file": "qc/g12.json"}
    if g15:
        gates["G15"] = {"pass": g15.get("G15_pass"), "file": "qc/g15_g18_candidates_r1.json",
                        **{k: g15.get(k) for k in ("loader_check_fail", "gold_not_displayed", "roundtrip_gold_fail",
                                                  "relations_split_call_id", "units_gt3", "units_long_gt2", "tokens")}}
        gates["G18"] = {"pass": g15.get("G18", {}).get("pass"), "vacuous": True,
                        "ordinal_rows": g15.get("G18", {}).get("ordinal_rows")}
    if sb:
        gates["G2_solverB"] = {k: sb.get(k) for k in ("rows_checked", "agree", "mismatches", "per_file")}
    gates.update(extra.get("gates", {}))
    failing = sorted(k for k, v in gates.items() if isinstance(v, dict) and v.get("pass") is False)
    rep = {"family": "F6", "round": 1, "report": "QC_REPORT", "repair": "r1",
           "checker": "F6 repair r1 builder (the generator author re-ran the independent checker's gate scripts on the "
                      "regenerated outputs; G5 read by the same session: disclosed, see g5)",
           "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "previous_report": "qc/QC_REPORT.before_repair_r1.json",
           "inputs": extra.get("inputs"), "g5": gates.get("G5"), "gates": gates, "failing_gates": failing,
           "findings": extra.get("findings"), "repair_changes": extra.get("repair_changes"),
           "problems": extra.get("problems"),
           "pass": not failing and bool(g5 and g5.get("pass")),
           "pass_rule": "pass only if 0 clearly-wrong G5 flags, ambiguous <= 1%, and every gate (G5, G6, G7, G8, G10, "
                        "G11, G12, G15, G18) passes"}
    json.dump(rep, open(QC / "QC_REPORT.json", "w"), indent=1)
    print(json.dumps({"failing_gates": failing, "pass": rep["pass"]}))


if __name__ == "__main__":
    main()

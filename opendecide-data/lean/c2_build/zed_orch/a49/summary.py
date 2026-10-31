import json, sys
sys.path.insert(0, '/Users/aryamahadik/Documents/jev/opendecide-data/lean/c2_build')
import gen_full_c2 as G
out = {}
for f in "T01 T06 T07 T12 T23 T24 T25 T26 T28 T30 T31 T32 T33 T15".split():
    L = G.layout(f)
    try:
        g = json.loads(L["gen"].read_text())
    except Exception as e:
        out[f] = {"error": str(e)}; continue
    gt = g["gates"]
    s6 = G.g6_summary(gt["G6"])
    b = gt.get("G6_24K")
    c = gt["G10"]["checks"]
    minp = lambda k: min([v for v in c[k]["value"]["chi2_p"].values() if v is not None] or [None]) if c[k]["value"].get("chi2_p") else None
    q = json.loads(L["qcrep"].read_text())
    out[f] = {"seeds": g["seeds"]["candidates"], "n_cand": g["n_candidates"], "yn_share": c["yes_no_share"]["value"],
              "G6_6k": [s6["max_excess_pp"], s6["max_cell"], s6["verdict"]],
              "G6_24k": None if not b else [b["max_excess_pp"], b["max_cell"], b["verdict"], b["qc_rows"], b["cells_over_bar"]],
              "G10_pos_p_min": minp("gold_position"), "G10_rank_p_min": minp("gold_rank"),
              "G10_pos": c["gold_position"]["verdict"], "G10_rank": c["gold_rank"]["verdict"],
              "G10_unit": c["gold_position"].get("unit"), "G10_failing_report_only": gt["G10"]["failing"],
              "pos_rowlevel_p": c.get("gold_position_rowlevel", {}).get("value", {}).get("chi2_p") if "gold_position_rowlevel" in c else "old row-level was used",
              "program_a49": [g.get("program_pass_a49"), g.get("program_failing_a49")], "program_old": [g["program_pass"], g["program_failing"]],
              "overlay": gt["overlay"]["verdict"], "spec30": gt["spec_3_0"]["verdict"],
              "g5h_tasks": g["haiku_tasks"]["G5-H"]["tasks"], "g3h_tasks": g["haiku_tasks"]["G3-H"]["tasks"],
              "qc_stage": q.get("stage"), "pass_a49": q.get("pass_a49")}
print(json.dumps(out, indent=1))

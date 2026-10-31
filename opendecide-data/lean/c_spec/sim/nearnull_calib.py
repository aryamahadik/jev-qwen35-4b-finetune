"""Near-null calibration of the C gate's dev rules, and measured disagreement rates between 4B pairs (CPU only).

Reads only dev preds (preds_<split>/<name>.jsonl) and dev data (data/<split>.jsonl) of the 9 PREREG_FINAL splits, via
gate_dev.py's own loaders and bootstrap. Prints aggregates only. No OHS, sealed, ejs-5 or test files are opened.
Run: python3 c_spec/sim/nearnull_calib.py   (from opendecide-data/lean)
"""
import json
import sys
from pathlib import Path

LEAN = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(LEAN))
import gate_dev as g  # noqa: E402

SPL = g.SPLITS.split(",")
UNSEEN = set(json.loads((LEAN / g.UNSEEN_FROZEN).read_text())["sources"])


def disc(rows):
    n = len(rows)
    return 100 * sum(x["ok_c"] != x["ok_r"] for x in rows) / n if n else float("nan")


def full_rules(cand, ref):
    rows = g.complete_rows(SPL, cand, ref)
    prim = [x for x in rows if x["source"] in UNSEEN]
    crows = [x for x in rows if x["source"] not in g.CONSTRAINT_EXCLUDE]
    P, F = g.group_boot(prim), g.group_boot(crows)
    halves = {h: g.point([x for x in crows if x["half"] == h])["diff"] for h in ("select", "confirm")}
    _, types = g.type_constraints(crows)
    cal_c, cal_r = g.crossfit(crows, "c"), g.crossfit(crows, "r")
    eq = g.relation_flips(SPL, rows, ("equiv",))
    cp = g.relation_flips(SPL, rows, ("complement",))
    out = {
        "pair": f"{cand} vs {ref}",
        "primary(D2-like) diff/LB/UB": (round(P["diff"], 2), round(P["lo"], 2), round(P["hi"], 2)),
        "primary SE (half-width/1.96)": round((P["hi"] - P["lo"]) / 3.92, 2),
        "primary discordant %": round(disc(prim), 2),
        "(a) full diff/LB": (round(F["diff"], 2), round(F["lo"], 2)),
        "(a2) half diffs": {k: round(v, 2) for k, v in halves.items()},
        "(b) yes/no diff/LB": (round(types["noul"]["diff"], 2), round(types["noul"]["lo"], 2)),
        "(c) choice diff/LB": (round(types["choice"]["diff"], 2), round(types["choice"]["lo"], 2)),
        "(d) cal Brier diff": round(cal_c["noul"]["brier_cal"] - cal_r["noul"]["brier_cal"], 4),
        "(e) equiv flips cand/ref": (round(eq["cand"], 2), round(eq["ref"], 2), eq["n"]),
        "complement same-answer % cand/ref (relation_flips counts different answers; same = violation)": (round(100 - cp["cand"], 2), round(100 - cp["ref"], 2), cp["n"]),
        "full discordant %": round(disc(crows), 2),
    }
    return out


def disc_only(cand, ref):
    rows, missing = g.load_rows(SPL, cand, ref)
    have = {x["split"] for x in rows}
    rows = [x for x in rows if x["split"] in have and x["p_c"] and x["p_r"]]
    prim = [x for x in rows if x["source"] in UNSEEN]
    P = g.group_boot(prim)
    return {"pair": f"{cand} vs {ref}", "splits": sorted(have), "n_primary": P["n"],
            "primary diff/LB/UB": (round(P["diff"], 2), round(P["lo"], 2), round(P["hi"], 2)),
            "primary SE": round((P["hi"] - P["lo"]) / 3.92, 2), "primary discordant %": round(disc(prim), 2)}


def se_rules(cand, ref):
    """SEs (bootstrap half-width / 1.96) of the dev quantities the C gate uses, for a C-like pair."""
    rows = g.complete_rows(SPL, cand, ref)
    crows = [x for x in rows if x["source"] not in g.CONSTRAINT_EXCLUDE]
    se = lambda B: round((B["hi"] - B["lo"]) / 3.92, 2)
    F = g.group_boot(crows)
    hs = {h: g.group_boot([x for x in crows if x["half"] == h]) for h in ("select", "confirm")}
    yn = g.group_boot([x for x in crows if x["qtype"] == "noul"])
    ch = g.group_boot([x for x in crows if x["qtype"] == "choice"])
    cc, cr = g.crossfit(crows, "c"), g.crossfit(crows, "r")
    eq = g.relation_flips(SPL, rows, ("equiv",))
    return {"pair": f"{cand} vs {ref}", "full diff/SE": (round(F["diff"], 2), se(F)), "full discordant %": round(disc(crows), 1),
            "half SEs": {h: se(v) for h, v in hs.items()}, "yes/no diff/SE": (round(yn["diff"], 2), se(yn)),
            "choice diff/SE": (round(ch["diff"], 2), se(ch)),
            "cal Brier diff": round(cc["noul"]["brier_cal"] - cr["noul"]["brier_cal"], 4),
            "equiv flips cand/ref": (round(eq["cand"], 2), round(eq["ref"], 2))}


if __name__ == "__main__":
    for c, r in (("q35_4b_v11b", "q35_4b_v11"), ("q35_4b_v11c", "q35_4b_v11"), ("q35_4b_main500k", "q35_4b_pxE")):
        print(json.dumps(se_rules(c, r)))
    print(json.dumps(full_rules("q35_4b_main500k_wise090", "q35_4b_main500k_b100"), indent=1))
    for c, r in (("q35_4b_main500k", "q35_4b_pxE"), ("q35_4b_v11b", "q35_4b_v11"), ("q35_4b_v11c", "q35_4b_v11"),
                 ("q35_4b_v11c", "q35_4b_v11b"), ("q35_4b_main500k_wise080", "q35_4b_main500k_b100")):
        try:
            print(json.dumps(disc_only(c, r)))
        except SystemExit as e:
            print(c, r, "stopped:", e)

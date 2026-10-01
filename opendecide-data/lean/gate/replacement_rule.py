"""PREREG_FINAL.md 2 / 5.4: choose ONE candidate among C1 (the final adapter), C2 (the cat average of the 0.85/0.90/0.95
snapshots and the final adapter) and, only when the C3 trigger fired, C3 (0.75 new + 0.25 4B-E). Not a ship look.

Replacement rule (point differences in micro accuracy over ALL rows of the 9 gate splits, ties and missing = wrong):
  an alternative replaces C1 only if it is >= +0.3 pp over C1 on dev-select AND >= 0 vs C1 on dev-confirm.
C3 is choosable only if, in addition (PREREG 2):
  - it passes every constraint on dev-select AND on dev-confirm. Interpreted here as the C3-trigger constraints
    (b) yes/no and (c) choice accuracy >= REF - 1 pp, (d) calibrated yes/no Brier <= REF + 0.005 with T fitted on the
    other half (all without tb_mixtral), and (g) jagged / OPI ASR (full sets) vs the job's fresh REF;
  - its dev-confirm accuracy is >= C1's - 0.3 pp and >= the fresh REF's dev-confirm accuracy;
  - its yes/no accuracy (all rows of the 9 splits) is >= C1's.
Each alternative is compared with the C1 read of ITS OWN job (C2: job 1; C3: job 2, where REF and C1 are re-scored).
When two alternatives qualify the pre-registration does not say which to take: the tool stops (exit 3) for the owner.

  python gate/replacement_rule.py --c1 q35_4b_main500k --alt q35_4b_main500k_c2 [--json logs/gate4b/replacement.json]
  python gate/replacement_rule.py --c1 q35_4b_main500k --alt q35_4b_main500k_c2 \
      --c3 q35_4b_main500k_c3 --c3-c1 q35_4b_main500k_j2 --c3-ref q35_4b_pxE_fresh2
Prints CHOSEN: <name>; exit 0. Exit 3 = owner decision needed; other non-zero = an input is missing.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import gate_dev as gd  # noqa: E402

SEL_MIN, CONF_MIN = 0.3, 0.0
C3_CONF_VS_C1 = -0.3


def acc_rows(splits, a, b):
    """gate_dev's complete rows for a pair (stops when any row of any split lacks a prediction)."""
    gd._MODE = "replacement"
    return gd.complete_rows(splits, a, b)


def micro(rows, who, half=None, qtype=None):
    xs = [x for x in rows if (half is None or x["half"] == half) and (qtype is None or x["qtype"] == qtype)]
    return 100 * sum(x["ok_" + who] for x in xs) / len(xs) if xs else float("nan")


def compare(splits, c1, alt):
    rows = acc_rows(splits, alt, c1)  # cand slot = alt, ref slot = C1
    d = {h: micro(rows, "c", h) - micro(rows, "r", h) for h in ("select", "confirm")}
    return {"alt": alt, "c1": c1, "n": len(rows),
            "alt_select": micro(rows, "c", "select"), "c1_select": micro(rows, "r", "select"),
            "alt_confirm": micro(rows, "c", "confirm"), "c1_confirm": micro(rows, "r", "confirm"),
            "diff_select": d["select"], "diff_confirm": d["confirm"],
            "alt_yesno": micro(rows, "c", qtype="noul"), "c1_yesno": micro(rows, "r", qtype="noul"),
            "qualifies": bool(d["select"] >= SEL_MIN - 1e-9 and d["confirm"] >= CONF_MIN - 1e-9)}


def c3_extra(splits, c3, c1, ref):
    """The C3-only conditions; returns (ok, details)."""
    rows = acc_rows(splits, c3, ref)  # C3 vs the job-2 fresh REF
    crows = [x for x in rows if x["source"] not in gd.CONSTRAINT_EXCLUDE]
    det, ok = {}, True
    for h, other in (("select", "confirm"), ("confirm", "select")):
        part = [x for x in crows if x["half"] == h]
        cons, _ = gd.type_constraints(part, f" (dev-{h})")
        bc = gd.brier_fit_apply([x for x in crows if x["half"] == other], part, "c")
        br = gd.brier_fit_apply([x for x in crows if x["half"] == other], part, "r")
        if bc and br:
            cons.append({"id": "d", "status": "PASS" if bc["brier"] <= br["brier"] + gd.BRIER_MAX_UP + 1e-12 else "FAIL",
                         "detail": f"{bc['brier']:.4f} vs {br['brier']:.4f}"})
        det[h] = cons
        ok &= all(c["status"] == "PASS" for c in cons)
    gcons, _ = gd.asr_constraints(c3, ref, "4b")
    det["attacks"] = gcons
    ok &= all(c["status"] == "PASS" for c in gcons)
    c3_conf, ref_conf = micro(rows, "c", "confirm"), micro(rows, "r", "confirm")
    vs1 = compare(splits, c1, c3)
    det["c3_confirm"], det["ref_confirm"], det["c1_confirm"] = c3_conf, ref_conf, vs1["c1_confirm"]
    det["c3_yesno"], det["c1_yesno"] = vs1["alt_yesno"], vs1["c1_yesno"]
    conds = {"confirm >= C1 - 0.3": c3_conf >= vs1["c1_confirm"] + C3_CONF_VS_C1 - 1e-9,
             "confirm >= fresh REF confirm": c3_conf >= ref_conf - 1e-9,
             "yes/no >= C1": vs1["alt_yesno"] >= vs1["c1_yesno"] - 1e-9}
    det["conditions"] = conds
    return bool(ok and all(conds.values())), det


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--c1", required=True, help="job-1 C1 pred name (the final adapter)")
    ap.add_argument("--alt", action="append", default=[], help="an alternative compared with --c1 (C2)")
    ap.add_argument("--c3", default="", help="C3 pred name (job 2), only when the C3 trigger fired")
    ap.add_argument("--c3-c1", default="", help="job-2 re-scored C1 pred name")
    ap.add_argument("--c3-ref", default="", help="job-2 fresh REF pred name")
    ap.add_argument("--splits", default=gd.SPLITS)
    ap.add_argument("--json", default="")
    a = ap.parse_args(argv)
    splits = a.splits.split(",")
    res = {"c1": a.c1, "rule": f"alt replaces C1 iff dev-select diff >= +{SEL_MIN} pp and dev-confirm diff >= {CONF_MIN}",
           "alts": [], "splits": splits}
    for alt in a.alt:
        res["alts"].append(compare(splits, a.c1, alt))
    if a.c3:
        if not (a.c3_c1 and a.c3_ref):
            ap.error("--c3 needs --c3-c1 and --c3-ref (job 2 re-scores C1 and REF)")
        r = compare(splits, a.c3_c1, a.c3)
        ok, det = c3_extra(splits, a.c3, a.c3_c1, a.c3_ref)
        r.update({"c3_extra_ok": ok, "c3_extra": det, "qualifies": bool(r["qualifies"] and ok)})
        res["alts"].append(r)
    for r in res["alts"]:
        print(f"   {r['alt']} vs {r['c1']}: dev-select {r['alt_select']:.2f} vs {r['c1_select']:.2f} ({r['diff_select']:+.2f} pp), "
              f"dev-confirm {r['alt_confirm']:.2f} vs {r['c1_confirm']:.2f} ({r['diff_confirm']:+.2f} pp), n={r['n']}"
              + (f"; C3 extra conditions {'PASS' if r.get('c3_extra_ok') else 'FAIL'}" if "c3_extra_ok" in r else "")
              + f" -> {'QUALIFIES' if r['qualifies'] else 'does not replace C1'}")
    q = [r for r in res["alts"] if r["qualifies"]]
    if len(q) > 1:
        res["chosen"], res["owner_needed"] = None, f"{len(q)} alternatives qualify ({', '.join(r['alt'] for r in q)}); " \
                                                   "PREREG_FINAL.md does not say which to take"
    else:
        res["chosen"] = q[0]["alt"] if q else a.c1
        res["chosen_is_c1"] = not q
    if a.json:
        Path(a.json).parent.mkdir(parents=True, exist_ok=True)
        Path(a.json).write_text(json.dumps(gd._clean(res), indent=2, default=str) + "\n")
    if res["chosen"] is None:
        print(f"OWNER DECISION NEEDED: {res['owner_needed']}")
        sys.exit(3)
    print(f"CHOSEN: {res['chosen']}")
    return res


if __name__ == "__main__":
    main()

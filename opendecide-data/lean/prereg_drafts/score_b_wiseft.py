"""Score step B (PREREG_FINAL amendment A11): weight-softened C1 candidates vs C1 re-read on the same machine.

Select on the dev-select half (unseen-source rows), confirm on the dev-confirm half with the A11 bars. Reads the
stored dev reads only (preds_<split>/<name>.jsonl); never opens any held-out file.

  cd lean && ../.venv/bin/python prereg_drafts/score_b_wiseft.py
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import gate_dev as g  # noqa: E402

SPLITS = g.SPLITS.split(",")
REF = "q35_4b_main500k_b100"
CANDS = [("q35_4b_main500k_wise090", 0.9), ("q35_4b_main500k_wise080", 0.8),
         ("q35_4b_main500k_wise070", 0.7), ("q35_4b_main500k_wise060", 0.6)]
UNSEEN = set(json.load(open(ROOT / "ship_unseen_sources.json"))["sources"])


def is_tb(x):
    return x["source"] == "tb_mixtral" or x["source"].startswith("tb_mixtral")


def acc(rows, key):
    return 100 * sum(x[key] for x in rows) / len(rows) if rows else math.nan


def brier(rows, key):
    yn = [x for x in rows if x["qtype"] == "noul"]
    return float(np.mean([(x[key].get("yes", 0.0) - x["gold"]) ** 2 for x in yn])) if yn else math.nan


def complement_viol(rows, half):
    sub = [x for x in rows if x["half"] == half]
    f = g.relation_flips(SPLITS, sub, {"complement"})
    # a complement pair should get DIFFERENT answers: a violation is the same answer, i.e. 100 - flip rate
    return {"n": f["n"], "cand": 100 - f["cand"], "ref": 100 - f["ref"]}


def main():
    res = {"ref": REF, "cands": {}}
    rows_by = {}
    for name, a in CANDS:
        rows = g.complete_rows(SPLITS, name, REF)
        rows_by[name] = rows
        sel = [x for x in rows if x["half"] == "select" and x["source"] in UNSEEN]
        res["cands"][name] = {"a": a, "select_unseen": acc(sel, "ok_c"), "select_unseen_ref": acc(sel, "ok_r"),
                              "n_select_unseen": len(sel)}
    # select: highest select-half unseen accuracy; ties go to the larger a
    best = max(CANDS, key=lambda t: (round(res["cands"][t[0]]["select_unseen"], 10), t[1]))
    res["a_star"] = best[1]
    res["a_star_name"] = best[0]
    ref_sel = next(iter(res["cands"].values()))["select_unseen_ref"]
    res["ref_select_unseen"] = ref_sel
    print("SELECT (dev-select half, unseen-source rows):")
    print(f"  a=1.0 (C1 re-read)  {ref_sel:.2f}")
    for name, a in CANDS:
        print(f"  a={a}  {res['cands'][name]['select_unseen']:.2f}  (n={res['cands'][name]['n_select_unseen']})")
    if res["cands"][best[0]]["select_unseen"] <= ref_sel:
        print(f"  best candidate a={best[1]} is not above C1 on the select half -> B adopts nothing (C1 stays)")
        res["verdict"] = "keep C1 (no candidate above C1 on select)"
    rows = rows_by[best[0]]
    conf = [x for x in rows if x["half"] == "confirm"]
    cu = [x for x in conf if x["source"] in UNSEEN]
    cf = [x for x in conf if not is_tb(x)]
    checks = []
    du = acc(cu, "ok_c") - acc(cu, "ok_r")
    checks.append(("unseen-source accuracy >= C1 + 0.5 pp", du, du >= 0.5, f"{acc(cu,'ok_c'):.2f} vs {acc(cu,'ok_r'):.2f}"))
    df = acc(cf, "ok_c") - acc(cf, "ok_r")
    checks.append(("full set >= C1 - 0.2 pp", df, df >= -0.2, f"{acc(cf,'ok_c'):.2f} vs {acc(cf,'ok_r'):.2f}"))
    yn = [x for x in cf if x["qtype"] == "noul"]
    ch = [x for x in cf if x["qtype"] != "noul"]
    dyn = acc(yn, "ok_c") - acc(yn, "ok_r")
    dch = acc(ch, "ok_c") - acc(ch, "ok_r")
    checks.append(("yes/no >= C1 - 0.5 pp", dyn, dyn >= -0.5, f"{acc(yn,'ok_c'):.2f} vs {acc(yn,'ok_r'):.2f}"))
    checks.append(("choice >= C1 - 0.5 pp", dch, dch >= -0.5, f"{acc(ch,'ok_c'):.2f} vs {acc(ch,'ok_r'):.2f}"))
    bc, br = brier(cf, "p_c"), brier(cf, "p_r")
    checks.append(("raw yes/no Brier <= C1 + 0.002", bc - br, bc - br <= 0.002, f"{bc:.4f} vs {br:.4f}"))
    eq = g.relation_flips(SPLITS, conf, {"equiv"})
    checks.append(("equivalence flips not above C1", eq["cand"] - eq["ref"], eq["cand"] <= eq["ref"],
                   f"{eq['cand']:.2f}% vs {eq['ref']:.2f}% (n={eq['n']})"))
    cv = complement_viol(rows, "confirm")
    checks.append(("complement violations not above C1", cv["cand"] - cv["ref"], cv["cand"] <= cv["ref"],
                   f"{cv['cand']:.2f}% vs {cv['ref']:.2f}% (n={cv['n']})"))
    print(f"\nCONFIRM (dev-confirm half) for a*={best[1]} ({best[0]}) vs C1 re-read:")
    for name, d, ok, txt in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {txt} (diff {d:+.3f})")
    res["checks"] = [{"check": n, "diff": d, "pass": bool(ok), "detail": t} for n, d, ok, t in checks]
    if "verdict" not in res:
        res["verdict"] = f"ADOPT a={best[1]}" if all(c[2] for c in checks) else "keep C1 (a* failed confirm)"
    # report-only: paired bootstrap on all unseen rows (both halves) for every candidate
    print("\nREPORT ONLY (both halves, unseen-source rows, paired bootstrap over groups):")
    for name, a in CANDS:
        u = [x for x in rows_by[name] if x["source"] in UNSEEN]
        b = g.group_boot(u)
        print(f"  a={a}: {b['cand']:.2f} vs C1 {b['ref']:.2f}  diff {b['diff']:+.2f} [{b['lo']:+.2f}, {b['hi']:+.2f}]")
        res["cands"][name]["all_unseen_boot"] = b
    print(f"\nVERDICT: {res['verdict']}")
    json.dump(res, open(ROOT / "logs/b_wiseft_result.json", "w"), indent=1, default=float)


if __name__ == "__main__":
    main()
